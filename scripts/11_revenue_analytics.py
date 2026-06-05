"""Этап 10: аналитика выручки от реализации ОФЗ.

Скрипт строит отдельный слой revenue analytics поверх report scope dataset.
Исходные данные `data/raw/` не изменяются.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, report_params, utils
else:
    from . import config, report_params, utils


REVENUE_REPORT_DOC = config.get_doc_path("revenue_analytics_report.md")
REVENUE_SOURCE_CANDIDATES = (
    "revenue_volume",
    "proceeds_volume",
    "placement_revenue",
    "placement_revenue_mln_rub",
    "revenue_amount_mln_rub",
    "proceeds_mln_rub",
    "объем выручки",
    "выручка от реализации",
    "выручка",
)
PLACEMENT_SOURCE_CANDIDATES = ("placement_volume", "placement_amount_mln_rub")
PERIOD_GROUP_COLUMNS = [
    "report_period_label",
    "report_period_start",
    "report_period_end",
    "report_year",
    "aggregation_mode",
]
MATURITY_ORDER = {
    "long_term": 1,
    "medium_term": 2,
    "short_term": 3,
    "requires_review": 99,
}


@dataclass(frozen=True)
class RevenueOutputs:
    """Пути сформированных revenue outputs."""

    xlsx_path: Path
    csv_paths: list[Path]
    report_path: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Сформировать revenue analytics tables и отчет ограничений."""
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт Этапа 10: revenue analytics")
    params = report_params.parse_report_args(argv)
    config.ensure_output_directories()

    scope = read_report_scope()
    filtered = filter_scope_by_params(scope, params)
    if filtered.empty:
        raise ValueError(
            "Report scope пуст для выбранных параметров; сначала выполните period_filter.py "
            "с теми же report-date, period-type, aggregation-mode и retrospective-years."
        )

    prepared, revenue_source, limitations = prepare_revenue_data(filtered)
    tables = build_revenue_tables(prepared)
    suffix = make_output_suffix(params)
    outputs = write_outputs(tables, suffix, limitations)
    utils.write_markdown(
        REVENUE_REPORT_DOC,
        build_report(params, revenue_source, prepared, tables, outputs, limitations),
    )

    logger.info("Revenue summary XLSX сохранен: %s", outputs.xlsx_path)
    for csv_path in outputs.csv_paths:
        logger.info("Revenue CSV сохранен: %s", csv_path)
    logger.info("Revenue analytics report сохранен: %s", REVENUE_REPORT_DOC)
    return 0


def read_report_scope() -> pd.DataFrame:
    """Прочитать основной report scope dataset."""
    if not config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.exists():
        raise FileNotFoundError(
            f"Не найден {config.OFZ_AUCTIONS_REPORT_SCOPE_CSV}. "
            "Сначала выполните этап parameterized report scope."
        )
    return pd.read_csv(config.OFZ_AUCTIONS_REPORT_SCOPE_CSV)


def filter_scope_by_params(scope: pd.DataFrame, params: report_params.ReportParams) -> pd.DataFrame:
    """Оставить строки report scope, соответствующие параметрам запуска."""
    required = {"report_period_label", "report_period_type", "aggregation_mode"}
    missing = required.difference(scope.columns)
    if missing:
        raise ValueError(f"В report scope отсутствуют колонки: {', '.join(sorted(missing))}.")
    labels = {str(period["report_period_label"]) for period in params.periods}
    mask = (
        scope["report_period_label"].astype("string").isin(labels)
        & (scope["report_period_type"].astype("string") == params.period_type)
        & (scope["aggregation_mode"].astype("string") == params.aggregation_mode)
    )
    return scope.loc[mask].copy()


def prepare_revenue_data(df: pd.DataFrame) -> tuple[pd.DataFrame, str | None, list[str]]:
    """Нормализовать placement/revenue и зафиксировать source mapping."""
    limitations: list[str] = []
    result = df.copy()
    placement_source = detect_column(result, PLACEMENT_SOURCE_CANDIDATES)
    revenue_source = detect_column(result, REVENUE_SOURCE_CANDIDATES)

    if placement_source is None:
        result["_placement"] = pd.Series(pd.NA, index=result.index, dtype="Float64")
        limitations.append("Не найдена колонка объема размещения по номиналу; placement metrics пустые.")
    else:
        result["_placement"] = pd.to_numeric(result[placement_source], errors="coerce")

    if revenue_source is None:
        result["_revenue"] = pd.Series(pd.NA, index=result.index, dtype="Float64")
        limitations.append(
            "Не найдена надежная колонка выручки от реализации; revenue metrics не рассчитываются и помечаются data_quality_flag."
        )
    else:
        result["_revenue"] = pd.to_numeric(result[revenue_source], errors="coerce")
        limitations.append(f"Выручка от реализации нормализована из колонки `{revenue_source}`.")

    if "auction_date" in result.columns:
        result["_auction_date"] = pd.to_datetime(result["auction_date"], errors="coerce")
        result["auction_month"] = result.get("auction_month", result["_auction_date"].dt.month)
    else:
        result["_auction_date"] = pd.NaT

    if "maturity_bucket" not in result.columns:
        result["maturity_bucket"] = "requires_review"
    if "maturity_bucket_label" not in result.columns:
        result["maturity_bucket_label"] = result["maturity_bucket"]
    if "format" not in result.columns:
        result["format"] = "requires_review"
    if "ofz_type" not in result.columns:
        result["ofz_type"] = "requires_review"

    return result, revenue_source, limitations


def detect_column(df: pd.DataFrame, candidates: Sequence[str]) -> str | None:
    """Найти первую доступную колонку из списка кандидатов без учета регистра."""
    lookup = {str(column).strip().lower(): str(column) for column in df.columns}
    for candidate in candidates:
        key = candidate.strip().lower()
        if key in lookup:
            return lookup[key]
    return None


def build_revenue_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Построить основную таблицу и дополнительные срезы."""
    tables = {
        "summary": aggregate_revenue(df, PERIOD_GROUP_COLUMNS),
        "by_ofz_type": aggregate_revenue(df, PERIOD_GROUP_COLUMNS + ["ofz_type"]),
        "by_maturity": aggregate_revenue(df, PERIOD_GROUP_COLUMNS + ["maturity_bucket", "maturity_bucket_label"]),
        "by_format": aggregate_revenue(df, PERIOD_GROUP_COLUMNS + ["format"]),
        "monthly": aggregate_monthly_revenue(df),
    }
    return tables


def aggregate_revenue(df: pd.DataFrame, group_columns: list[str]) -> pd.DataFrame:
    """Агрегировать выручку и номинальное размещение по заданным измерениям."""
    rows: list[dict[str, Any]] = []
    for keys, group in df.groupby(group_columns, dropna=False):
        key_tuple = keys if isinstance(keys, tuple) else (keys,)
        row = dict(zip(group_columns, key_tuple))
        placement = group["_placement"].sum(min_count=1)
        revenue = group["_revenue"].sum(min_count=1)
        gap = placement - revenue if pd.notna(placement) and pd.notna(revenue) else pd.NA
        row.update(
            {
                "placement_volume": placement,
                "placement_volume_bln": divide_or_na(placement, 1000.0),
                "revenue_volume": revenue,
                "revenue_volume_bln": divide_or_na(revenue, 1000.0),
                "nominal_revenue_gap": gap,
                "nominal_revenue_gap_bln": divide_or_na(gap, 1000.0),
                "revenue_to_nominal_ratio": safe_divide(revenue, placement),
                "nominal_discount_ratio": safe_divide(gap, placement),
                "auction_count": int(len(group)),
                "data_quality_flag": revenue_quality_flag(group),
            }
        )
        rows.append(row)
    result = pd.DataFrame(rows)
    if result.empty:
        return result
    result = add_sort_columns(result)
    return sort_table(result)


def aggregate_monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Сформировать помесячный срез revenue analytics внутри выбранного горизонта."""
    month_col = "auction_month" if "auction_month" in df.columns else None
    if month_col is None:
        result = aggregate_revenue(df, PERIOD_GROUP_COLUMNS)
        result["month_number"] = pd.NA
        result["month_label"] = pd.NA
        return result
    data = df.copy()
    data["month_number"] = pd.to_numeric(data[month_col], errors="coerce").astype("Int64")
    data["month_label"] = data["month_number"].map(month_label_ru)
    group_columns = PERIOD_GROUP_COLUMNS + ["month_number", "month_label"]
    return aggregate_revenue(data, group_columns)


def revenue_quality_flag(group: pd.DataFrame) -> str:
    """Вернуть флаг качества для revenue group."""
    flags: list[str] = []
    if group["_revenue"].isna().all():
        flags.append("revenue_missing")
    elif group["_revenue"].isna().any():
        flags.append("revenue_partial")
    else:
        flags.append("ok")
    if group["_placement"].isna().all():
        flags.append("placement_missing")
    elif (pd.to_numeric(group["_placement"], errors="coerce") <= 0).any():
        flags.append("zero_or_negative_placement_present")
    if "data_quality_flag" in group.columns:
        source_flags = group["data_quality_flag"].fillna("").astype(str)
        if source_flags.str.contains("requires_review", regex=False).any():
            flags.append("source_requires_review")
    return "; ".join(dict.fromkeys(flags))


def add_sort_columns(result: pd.DataFrame) -> pd.DataFrame:
    """Добавить служебные поля сортировки, если они доступны."""
    sorted_result = result.copy()
    if "report_period_start" in sorted_result.columns:
        sorted_result["_period_sort"] = pd.to_datetime(sorted_result["report_period_start"], errors="coerce")
    if "maturity_bucket" in sorted_result.columns:
        sorted_result["maturity_bucket_order"] = (
            sorted_result["maturity_bucket"].astype(str).map(MATURITY_ORDER).fillna(99).astype(int)
        )
    return sorted_result


def sort_table(result: pd.DataFrame) -> pd.DataFrame:
    """Отсортировать таблицу сначала по периоду, затем по аналитическому срезу."""
    sort_columns = [column for column in ["aggregation_mode", "_period_sort"] if column in result.columns]
    for column in ["ofz_type", "maturity_bucket_order", "maturity_bucket_label", "format", "month_number"]:
        if column in result.columns:
            sort_columns.append(column)
    if sort_columns:
        result = result.sort_values(sort_columns, kind="stable").reset_index(drop=True)
    return result.drop(columns=["_period_sort"], errors="ignore")


def write_outputs(tables: dict[str, pd.DataFrame], suffix: str, limitations: list[str]) -> RevenueOutputs:
    """Сохранить revenue tables в XLSX workbook и CSV exports."""
    xlsx_path = config.REPORTS_ANALYTICAL_TABLES_DIR / f"revenue_summary_{suffix}.xlsx"
    csv_paths: list[Path] = []
    for name, table in tables.items():
        csv_name = "revenue_summary" if name == "summary" else f"revenue_{name}"
        csv_path = config.EXPORTS_ANALYTICAL_CSV_DIR / f"{csv_name}_{suffix}.csv"
        table.to_csv(csv_path, index=False, encoding="utf-8")
        csv_paths.append(csv_path)

    try:
        write_revenue_workbook(tables, xlsx_path)
        saved_xlsx_path = xlsx_path
    except PermissionError:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fallback_path = xlsx_path.with_name(f"{xlsx_path.stem}_{timestamp}{xlsx_path.suffix}")
        write_revenue_workbook(tables, fallback_path)
        saved_xlsx_path = fallback_path
        limitations.append(
            f"Основной XLSX-файл был заблокирован; fallback создан в той же папке: `{fallback_path.name}`."
        )
    return RevenueOutputs(saved_xlsx_path, csv_paths, REVENUE_REPORT_DOC)


def write_revenue_workbook(tables: dict[str, pd.DataFrame], path: Path) -> None:
    """Сохранить все revenue-срезы в один XLSX workbook."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path) as writer:
        for sheet_name, table in tables.items():
            table.to_excel(writer, sheet_name=sheet_name[:31], index=False)


def build_report(
    params: report_params.ReportParams,
    revenue_source: str | None,
    prepared: pd.DataFrame,
    tables: dict[str, pd.DataFrame],
    outputs: RevenueOutputs,
    limitations: list[str],
) -> str:
    """Сформировать markdown-отчет по revenue analytics."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Revenue analytics: выручка от реализации ОФЗ",
        "",
        f"Дата формирования: `{now}`.",
        "",
        "## Параметры",
        "",
        f"- `report_date`: `{params.report_date.isoformat()}`",
        f"- `period_type`: `{params.period_type}`",
        f"- `aggregation_mode`: `{params.aggregation_mode}`",
        f"- `retrospective_years`: `{params.retrospective_years}`",
        "",
        "## Источник",
        "",
        f"- Dataset: `{config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.relative_to(config.PROJECT_ROOT).as_posix()}`",
        f"- Колонка выручки: `{revenue_source}`" if revenue_source else "- Колонка выручки: не найдена.",
        f"- Строк в расчетном scope: `{len(prepared)}`",
        "",
        "## Outputs",
        "",
        f"- XLSX workbook: `{outputs.xlsx_path.relative_to(config.PROJECT_ROOT).as_posix()}`",
    ]
    lines.extend(f"- CSV: `{path.relative_to(config.PROJECT_ROOT).as_posix()}`" for path in outputs.csv_paths)
    lines.extend(["", "## Срезы", ""])
    for name, table in tables.items():
        lines.append(f"- `{name}`: {len(table)} строк.")
    lines.extend(["", "## Основная таблица `revenue_summary`", ""])
    lines.extend(markdown_table(tables["summary"].head(20)))
    lines.extend(["", "## Методика", ""])
    lines.extend(
        [
            "- `placement_volume` — сумма объема размещения по номиналу, млн рублей.",
            "- `revenue_volume` — сумма выручки от реализации, млн рублей.",
            "- `nominal_revenue_gap = placement_volume - revenue_volume`.",
            "- `revenue_to_nominal_ratio = revenue_volume / placement_volume`.",
            "- `nominal_discount_ratio = nominal_revenue_gap / placement_volume`.",
            "- Значения `_bln` являются отображением в млрд рублей и не изменяют исходные млн рублей.",
        ]
    )
    lines.extend(["", "## Ограничения", ""])
    if limitations:
        lines.extend(f"- {item}" for item in limitations)
    else:
        lines.append("- Существенные ограничения не выявлены.")
    return "\n".join(lines)


def markdown_table(df: pd.DataFrame) -> list[str]:
    """Сформировать простую markdown-таблицу без зависимости от tabulate."""
    if df.empty:
        return ["Нет строк для отображения."]
    display = df.copy()
    display = display.where(pd.notna(display), "")
    columns = [str(column) for column in display.columns]
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in display.iterrows():
        values = [format_markdown_cell(row[column]) for column in display.columns]
        lines.append("| " + " | ".join(values) + " |")
    return lines


def format_markdown_cell(value: Any) -> str:
    """Отформатировать значение для markdown-таблицы."""
    if isinstance(value, float):
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value).replace("|", "\\|")


def make_output_suffix(params: report_params.ReportParams) -> str:
    """Вернуть суффикс output-файлов с учетом aggregation_mode."""
    return (
        f"{params.period_type}_{params.aggregation_mode}_{params.report_date.isoformat()}_"
        f"retrospective_{params.retrospective_years}"
    )


def month_label_ru(month_number: Any) -> str:
    """Вернуть компактную русскую подпись месяца."""
    names = {
        1: "январь",
        2: "февраль",
        3: "март",
        4: "апрель",
        5: "май",
        6: "июнь",
        7: "июль",
        8: "август",
        9: "сентябрь",
        10: "октябрь",
        11: "ноябрь",
        12: "декабрь",
    }
    try:
        return names.get(int(month_number), "")
    except (TypeError, ValueError):
        return ""


def safe_divide(numerator: Any, denominator: Any) -> Any:
    """Безопасно разделить два скаляра."""
    if pd.isna(numerator) or pd.isna(denominator):
        return pd.NA
    denominator_float = float(denominator)
    if denominator_float == 0:
        return pd.NA
    return float(numerator) / denominator_float


def divide_or_na(value: Any, denominator: float) -> Any:
    """Разделить значение или вернуть NA."""
    if pd.isna(value):
        return pd.NA
    return float(value) / denominator


if __name__ == "__main__":
    raise SystemExit(main())
