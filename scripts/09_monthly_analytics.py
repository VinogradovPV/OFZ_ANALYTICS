"""Этап 9.2: помесячный слой показателей для объяснения накопленного итога."""

from __future__ import annotations

import sys
from calendar import monthrange
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Sequence

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, report_params, utils
else:
    from . import config, report_params, utils


MONTHLY_METRICS_CSV = config.PROCESSED_DATA_DIR / "ofz_monthly_metrics.csv"
MONTHLY_ANALYTICS_REPORT = config.get_doc_path("monthly_analytics_report.md")


@dataclass(frozen=True)
class SourceDataset:
    """Источник данных для помесячной аналитики."""

    dataframe: pd.DataFrame
    source_path: Path
    source_kind: str
    limitations: list[str]


def main(argv: Sequence[str] | None = None) -> int:
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт Этапа 9.2: помесячная аналитика")

    params = report_params.parse_report_args(argv)
    config.ensure_output_directories()
    source = read_source_dataset(params)
    metrics, limitations = build_monthly_metrics(source.dataframe, params)
    limitations.extend(source.limitations)

    suffix = make_output_suffix(params)
    csv_path = config.EXPORTS_ANALYTICAL_CSV_DIR / f"monthly_metrics_{suffix}.csv"
    xlsx_path = config.REPORTS_MONTHLY_TABLES_DIR / f"monthly_metrics_{suffix}.xlsx"

    config.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.EXPORTS_ANALYTICAL_CSV_DIR.mkdir(parents=True, exist_ok=True)
    config.REPORTS_MONTHLY_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(MONTHLY_METRICS_CSV, index=False, encoding="utf-8")
    metrics.to_csv(csv_path, index=False, encoding="utf-8")
    saved_xlsx_path = write_xlsx_with_fallback(metrics, xlsx_path, limitations)

    report = build_report(
        params=params,
        metrics=metrics,
        source_path=source.source_path,
        source_kind=source.source_kind,
        csv_path=csv_path,
        xlsx_path=saved_xlsx_path,
        limitations=limitations,
    )
    utils.write_markdown(MONTHLY_ANALYTICS_REPORT, report)

    logger.info("Помесячный processed dataset сохранен: %s", MONTHLY_METRICS_CSV)
    logger.info("Помесячный CSV export сохранен: %s", csv_path)
    logger.info("Помесячный XLSX export сохранен: %s", saved_xlsx_path)
    logger.info("Отчет помесячной аналитики сохранен: %s", MONTHLY_ANALYTICS_REPORT)
    logger.info("Этап 9.2 завершен")
    return 0


def read_source_dataset(params: report_params.ReportParams) -> SourceDataset:
    """Прочитать report scope или построить горизонт напрямую из feature dataset."""
    limitations: list[str] = []
    if config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.exists():
        scope = pd.read_csv(config.OFZ_AUCTIONS_REPORT_SCOPE_CSV)
        filtered = filter_report_scope(scope, params)
        if not filtered.empty:
            return SourceDataset(
                dataframe=filtered,
                source_path=config.OFZ_AUCTIONS_REPORT_SCOPE_CSV,
                source_kind="report_scope",
                limitations=limitations,
            )
        limitations.append(
            "Существующий report scope не содержит строк для выбранных параметров; "
            "monthly layer построен напрямую из feature dataset по тем же периодам."
        )

    if not config.OFZ_AUCTIONS_FEATURES_CSV.exists():
        raise FileNotFoundError(
            "Не найден источник для помесячной аналитики: отсутствуют "
            f"{config.OFZ_AUCTIONS_REPORT_SCOPE_CSV} и {config.OFZ_AUCTIONS_FEATURES_CSV}."
        )

    features = pd.read_csv(config.OFZ_AUCTIONS_FEATURES_CSV)
    scoped = build_scope_from_features(features, params)
    limitations.append(
        "Monthly layer построен из feature dataset; для полной воспроизводимости рекомендуется сначала выполнить period_filter.py."
    )
    return SourceDataset(
        dataframe=scoped,
        source_path=config.OFZ_AUCTIONS_FEATURES_CSV,
        source_kind="features",
        limitations=limitations,
    )


def filter_report_scope(scope: pd.DataFrame, params: report_params.ReportParams) -> pd.DataFrame:
    """Оставить только строки report scope, соответствующие параметрам запуска."""
    required = {"report_period_label", "report_period_type", "aggregation_mode"}
    missing = required.difference(scope.columns)
    if missing:
        return pd.DataFrame(columns=scope.columns)

    labels = {str(period["report_period_label"]) for period in params.periods}
    mask = (
        scope["report_period_label"].astype("string").isin(labels)
        & (scope["report_period_type"].astype("string") == params.period_type)
        & (scope["aggregation_mode"].astype("string") == params.aggregation_mode)
    )
    return scope.loc[mask].copy()


def build_scope_from_features(features: pd.DataFrame, params: report_params.ReportParams) -> pd.DataFrame:
    """Сформировать временный report scope из features без записи основного report scope."""
    date_column = detect_auction_date_column(features)
    df = features.copy()
    df["_auction_date_for_filter"] = pd.to_datetime(df[date_column], errors="coerce")

    parts: list[pd.DataFrame] = []
    for period in params.periods:
        start_date = pd.Timestamp(period["period_start"])
        end_date = pd.Timestamp(period["period_end"])
        mask = df["_auction_date_for_filter"].between(start_date, end_date, inclusive="both")
        period_df = df.loc[mask].copy()
        period_df["aggregation_mode"] = str(period["aggregation_mode"])
        period_df["report_period_start"] = start_date.date().isoformat()
        period_df["report_period_end"] = end_date.date().isoformat()
        period_df["report_period_label"] = str(period["report_period_label"])
        period_df["report_period_display_label"] = str(period["report_period_display_label"])
        period_df["report_period_file_label"] = str(period["report_period_file_label"])
        period_df["report_period_order"] = int(period["report_period_order"])
        period_df["report_year"] = int(period["report_year"])
        period_df["report_period_type"] = str(period["period_type"])
        period_df["is_target_period"] = bool(period["is_target_period"])
        if not period_df.empty:
            parts.append(period_df)

    if not parts:
        return make_empty_scope(features)
    scoped = pd.concat(parts, ignore_index=True)
    return scoped.drop(columns=["_auction_date_for_filter"], errors="ignore")


def make_empty_scope(features: pd.DataFrame) -> pd.DataFrame:
    """Вернуть пустой scope с колонками источника и метаданными периода."""
    columns = list(features.columns)
    for column in [
        "aggregation_mode",
        "report_period_start",
        "report_period_end",
        "report_period_label",
        "report_period_display_label",
        "report_period_file_label",
        "report_period_order",
        "report_year",
        "report_period_type",
        "is_target_period",
    ]:
        if column not in columns:
            columns.append(column)
    return pd.DataFrame(columns=columns)


def detect_auction_date_column(df: pd.DataFrame) -> str:
    """Определить основную дату размещения."""
    candidates = ["auction_date", "date", "Дата", "Дата аукциона"]
    for column in candidates:
        if column in df.columns:
            parsed = pd.to_datetime(df[column], errors="coerce")
            if parsed.notna().any():
                return column
    raise ValueError("Не удалось определить колонку даты размещения для monthly layer.")


def build_monthly_metrics(
    source: pd.DataFrame,
    params: report_params.ReportParams,
) -> tuple[pd.DataFrame, list[str]]:
    """Построить помесячные и накопленные показатели для выбранного горизонта."""
    limitations: list[str] = []
    month_grid = build_month_grid(params)
    prepared = prepare_source(source, limitations)

    rows: list[dict[str, Any]] = []
    for _, month_info in month_grid.iterrows():
        month_rows = select_month_rows(prepared, month_info)
        rows.append(build_month_row(month_info, month_rows))

    metrics = pd.DataFrame(rows)
    metrics = add_cumulative_fields(metrics)
    metrics["data_quality_flag"] = metrics.apply(build_quality_flag, axis=1)
    add_context_limitations(prepared, metrics, params, limitations)
    return metrics[monthly_output_columns()], limitations


def build_month_grid(params: report_params.ReportParams) -> pd.DataFrame:
    """Сформировать календарную сетку месяцев внутри каждого отчетного интервала."""
    rows: list[dict[str, Any]] = []
    for period in params.periods:
        start_date = pd.Timestamp(period["period_start"]).date()
        end_date = pd.Timestamp(period["period_end"]).date()
        current = date(start_date.year, start_date.month, 1)
        while current <= end_date:
            month_end = date(current.year, current.month, monthrange(current.year, current.month)[1])
            if month_end > end_date:
                month_end = end_date
            rows.append(
                {
                    "report_year": int(period["report_year"]),
                    "month": current.strftime("%Y-%m"),
                    "month_number": current.month,
                    "month_label": current.strftime("%Y-%m"),
                    "month_start": current.isoformat(),
                    "month_end": month_end.isoformat(),
                    "report_period_label": str(period["report_period_label"]),
                    "aggregation_mode": str(period["aggregation_mode"]),
                    "is_target_year": bool(period["is_target_period"]),
                    "report_period_order": int(period["report_period_order"]),
                }
            )
            current = add_month(current)
    return pd.DataFrame(rows)


def add_month(value: date) -> date:
    """Перейти к первому дню следующего месяца."""
    if value.month == 12:
        return date(value.year + 1, 1, 1)
    return date(value.year, value.month + 1, 1)


def prepare_source(source: pd.DataFrame, limitations: list[str]) -> pd.DataFrame:
    """Подготовить числовые и календарные поля для агрегации."""
    df = source.copy()
    date_column = detect_auction_date_column(df)
    df["_auction_date"] = pd.to_datetime(df[date_column], errors="coerce")
    df["_month_start"] = df["_auction_date"].dt.to_period("M").dt.to_timestamp()

    df["_demand"] = resolve_numeric(df, ["demand_volume", "demand_amount_mln_rub"], "спрос", limitations)
    df["_supply"] = resolve_numeric(df, ["supply_volume", "offer_amount_mln_rub"], "предложение", limitations)
    df["_placement"] = resolve_numeric(df, ["placement_volume", "placement_amount_mln_rub"], "размещение", limitations)
    df["_revenue"] = resolve_numeric(df, ["revenue_volume", "revenue_amount_mln_rub"], "выручка", limitations)
    df["_yield"] = resolve_numeric(df, ["weighted_avg_yield", "yield", "weighted_avg_yield_pct"], "доходность", limitations)

    if "format" not in df.columns:
        df["format"] = pd.NA
        limitations.append("Колонка `format` отсутствует; объемы аукционов и ДРПА не разделены.")
    if "maturity_bucket" not in df.columns:
        df["maturity_bucket"] = pd.NA
        limitations.append("Колонка `maturity_bucket` отсутствует; структура по срокам может быть неполной.")
    if "ofz_type" not in df.columns:
        df["ofz_type"] = pd.NA
        limitations.append("Колонка `ofz_type` отсутствует; структура по видам ОФЗ может быть неполной.")
    return df


def resolve_numeric(
    df: pd.DataFrame,
    candidates: list[str],
    metric_name: str,
    limitations: list[str],
) -> pd.Series:
    """Найти числовую колонку среди кандидатов."""
    for column in candidates:
        if column in df.columns:
            return pd.to_numeric(df[column], errors="coerce")
    limitations.append(f"Не найдена колонка для показателя `{metric_name}`; связанные значения будут пустыми.")
    return pd.Series(pd.NA, index=df.index, dtype="Float64")


def select_month_rows(prepared: pd.DataFrame, month_info: pd.Series) -> pd.DataFrame:
    """Выбрать строки конкретного месяца внутри конкретного отчетного периода."""
    month_start = pd.Timestamp(str(month_info["month_start"]))
    month_end = pd.Timestamp(str(month_info["month_end"]))
    mask = prepared["_auction_date"].between(month_start, month_end, inclusive="both")

    if "report_period_label" in prepared.columns:
        mask = mask & (prepared["report_period_label"].astype("string") == str(month_info["report_period_label"]))
    if "aggregation_mode" in prepared.columns:
        mask = mask & (prepared["aggregation_mode"].astype("string") == str(month_info["aggregation_mode"]))
    return prepared.loc[mask].copy()


def build_month_row(month_info: pd.Series, month_rows: pd.DataFrame) -> dict[str, Any]:
    """Рассчитать месячные показатели для одной строки календарной сетки."""
    total_demand = sum_numeric(month_rows, "_demand")
    total_supply = sum_numeric(month_rows, "_supply")
    total_placement = sum_numeric(month_rows, "_placement")
    total_revenue = sum_numeric(month_rows, "_revenue")
    yield_values = month_rows["_yield"] if "_yield" in month_rows.columns else pd.Series(dtype="Float64")

    return {
        "report_year": int(month_info["report_year"]),
        "month": str(month_info["month"]),
        "month_number": int(month_info["month_number"]),
        "month_label": str(month_info["month_label"]),
        "month_start": str(month_info["month_start"]),
        "month_end": str(month_info["month_end"]),
        "report_period_label": str(month_info["report_period_label"]),
        "aggregation_mode": str(month_info["aggregation_mode"]),
        "is_target_year": bool(month_info["is_target_year"]),
        "auction_count": int(len(month_rows)),
        "total_demand": total_demand,
        "total_supply": total_supply,
        "total_placement_volume": total_placement,
        "total_revenue_volume": total_revenue,
        "bid_to_cover_ratio": safe_divide(total_demand, total_supply),
        "demand_to_placement_ratio": safe_divide(total_demand, total_placement),
        "demand_satisfaction_ratio": safe_divide(total_placement, total_demand),
        "yield_weighted_avg": weighted_average(month_rows, "_yield", "_placement"),
        "yield_min": min_numeric(yield_values),
        "yield_median": median_numeric(yield_values),
        "yield_max": max_numeric(yield_values),
        "placement_volume_auction": placement_by_format(month_rows, "auction"),
        "placement_volume_drpa": placement_by_format(month_rows, "drpa"),
        "placement_volume_short_term": placement_by_bucket(month_rows, "short_term"),
        "placement_volume_medium_term": placement_by_bucket(month_rows, "medium_term"),
        "placement_volume_long_term": placement_by_bucket(month_rows, "long_term"),
        "ofz_pd_placement_volume": placement_by_ofz_type(month_rows, "ПД"),
        "ofz_in_placement_volume": placement_by_ofz_type(month_rows, "ИН"),
        "ofz_pk_placement_volume": placement_by_ofz_type(month_rows, "ПК"),
        "cumulative_demand": pd.NA,
        "cumulative_supply": pd.NA,
        "cumulative_placement_volume": pd.NA,
        "cumulative_revenue_volume": pd.NA,
        "cumulative_bid_to_cover_ratio": pd.NA,
        "cumulative_weighted_avg_yield": pd.NA,
        "cumulative_auction_count": pd.NA,
        "_yield_weighted_numerator": weighted_numerator(month_rows, "_yield", "_placement"),
        "_yield_weighted_denominator": weighted_denominator(month_rows, "_yield", "_placement"),
        "_has_drpa": has_drpa(month_rows),
    }


def add_cumulative_fields(metrics: pd.DataFrame) -> pd.DataFrame:
    """Добавить накопленные показатели с января до текущего месяца включительно."""
    result = metrics.sort_values(["report_year", "month_number", "report_period_label"]).reset_index(drop=True)
    group_columns = ["report_period_label", "report_year", "aggregation_mode"]

    for source_column, target_column in [
        ("total_demand", "cumulative_demand"),
        ("total_supply", "cumulative_supply"),
        ("total_placement_volume", "cumulative_placement_volume"),
        ("total_revenue_volume", "cumulative_revenue_volume"),
        ("auction_count", "cumulative_auction_count"),
    ]:
        numeric_source = pd.to_numeric(result[source_column], errors="coerce").fillna(0)
        result[target_column] = numeric_source.groupby(
            [result[column] for column in group_columns],
            dropna=False,
        ).cumsum()

    result["_cumulative_yield_numerator"] = result.groupby(group_columns, dropna=False)["_yield_weighted_numerator"].cumsum()
    result["_cumulative_yield_denominator"] = result.groupby(group_columns, dropna=False)["_yield_weighted_denominator"].cumsum()
    result["cumulative_bid_to_cover_ratio"] = result.apply(
        lambda row: safe_divide(row["cumulative_demand"], row["cumulative_supply"]),
        axis=1,
    )
    result["cumulative_weighted_avg_yield"] = result.apply(
        lambda row: safe_divide(row["_cumulative_yield_numerator"], row["_cumulative_yield_denominator"]),
        axis=1,
    )
    return result


def sum_numeric(df: pd.DataFrame, column: str) -> Any:
    """Просуммировать числовую колонку с учетом полностью пустого месяца."""
    if df.empty or column not in df.columns:
        return pd.NA
    value = df[column].sum(min_count=1)
    return float(value) if pd.notna(value) else pd.NA


def min_numeric(series: pd.Series) -> Any:
    value = pd.to_numeric(series, errors="coerce").min()
    return float(value) if pd.notna(value) else pd.NA


def median_numeric(series: pd.Series) -> Any:
    value = pd.to_numeric(series, errors="coerce").median()
    return float(value) if pd.notna(value) else pd.NA


def max_numeric(series: pd.Series) -> Any:
    value = pd.to_numeric(series, errors="coerce").max()
    return float(value) if pd.notna(value) else pd.NA


def safe_divide(numerator: Any, denominator: Any) -> Any:
    """Безопасное деление для ratio-показателей."""
    if pd.isna(numerator) or pd.isna(denominator):
        return pd.NA
    denominator_float = float(denominator)
    if denominator_float == 0:
        return pd.NA
    return float(numerator) / denominator_float


def weighted_average(df: pd.DataFrame, value_column: str, weight_column: str) -> Any:
    numerator = weighted_numerator(df, value_column, weight_column)
    denominator = weighted_denominator(df, value_column, weight_column)
    return safe_divide(numerator, denominator)


def weighted_numerator(df: pd.DataFrame, value_column: str, weight_column: str) -> float:
    if df.empty or value_column not in df.columns or weight_column not in df.columns:
        return 0.0
    values = pd.to_numeric(df[value_column], errors="coerce")
    weights = pd.to_numeric(df[weight_column], errors="coerce")
    valid = values.notna() & weights.notna() & (weights > 0)
    return float((values.loc[valid] * weights.loc[valid]).sum()) if valid.any() else 0.0


def weighted_denominator(df: pd.DataFrame, value_column: str, weight_column: str) -> float:
    if df.empty or value_column not in df.columns or weight_column not in df.columns:
        return 0.0
    values = pd.to_numeric(df[value_column], errors="coerce")
    weights = pd.to_numeric(df[weight_column], errors="coerce")
    valid = values.notna() & weights.notna() & (weights > 0)
    return float(weights.loc[valid].sum()) if valid.any() else 0.0


def placement_by_format(df: pd.DataFrame, kind: str) -> Any:
    if df.empty:
        return pd.NA
    format_text = df["format"].astype("string").str.upper()
    if kind == "drpa":
        mask = format_text.str.contains("ДРПА|DRPA", regex=True, na=False)
    else:
        mask = ~format_text.str.contains("ДРПА|DRPA", regex=True, na=False)
    return sum_numeric(df.loc[mask], "_placement")


def placement_by_bucket(df: pd.DataFrame, bucket: str) -> Any:
    if df.empty:
        return pd.NA
    mask = df["maturity_bucket"].astype("string") == bucket
    return sum_numeric(df.loc[mask], "_placement")


def placement_by_ofz_type(df: pd.DataFrame, token: str) -> Any:
    if df.empty:
        return pd.NA
    ofz_type = df["ofz_type"].astype("string").str.upper()
    mask = ofz_type.str.contains(token, regex=False, na=False)
    return sum_numeric(df.loc[mask], "_placement")


def has_drpa(df: pd.DataFrame) -> bool:
    if df.empty or "format" not in df.columns:
        return False
    return bool(df["format"].astype("string").str.upper().str.contains("ДРПА|DRPA", regex=True, na=False).any())


def build_quality_flag(row: pd.Series) -> str:
    """Собрать флаги качества для месячной строки."""
    flags: list[str] = []
    if int(row["auction_count"]) == 0:
        flags.append("empty_month")
    if pd.isna(row["total_demand"]):
        flags.append("no_demand")
    if pd.isna(row["total_supply"]):
        flags.append("no_supply")
    if pd.isna(row["total_placement_volume"]):
        flags.append("no_placement")
    if pd.isna(row["yield_weighted_avg"]):
        flags.append("no_weighted_yield")
    if bool(row.get("_has_drpa", False)):
        flags.append("drpa_present")
    return "; ".join(flags) if flags else "ok"


def add_context_limitations(
    prepared: pd.DataFrame,
    metrics: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> None:
    """Добавить методические ограничения, зависящие от данных."""
    empty_months = int((metrics["auction_count"] == 0).sum())
    if empty_months:
        limitations.append(f"В monthly layer есть месяцы без размещений: {empty_months}; строки сохранены для непрерывной временной оси.")
    if "_has_drpa" in metrics.columns and bool(metrics["_has_drpa"].any()):
        limitations.append(
            "В отдельных месяцах присутствуют ДРПА; demand-based ratios следует интерпретировать с учетом флага `drpa_present`."
        )
    if params.aggregation_mode == "cumulative":
        limitations.append(
            "Месячные поля считаются за конкретный месяц, а cumulative-поля - с января до текущего месяца включительно."
        )
    if prepared.empty:
        limitations.append("В выбранном отчетном горизонте нет строк исходных размещений.")


def monthly_output_columns() -> list[str]:
    """Контракт колонок monthly layer."""
    return [
        "report_year",
        "month",
        "month_number",
        "month_label",
        "month_start",
        "month_end",
        "report_period_label",
        "aggregation_mode",
        "is_target_year",
        "auction_count",
        "total_demand",
        "total_supply",
        "total_placement_volume",
        "total_revenue_volume",
        "bid_to_cover_ratio",
        "demand_to_placement_ratio",
        "demand_satisfaction_ratio",
        "yield_weighted_avg",
        "yield_min",
        "yield_median",
        "yield_max",
        "placement_volume_auction",
        "placement_volume_drpa",
        "placement_volume_short_term",
        "placement_volume_medium_term",
        "placement_volume_long_term",
        "ofz_pd_placement_volume",
        "ofz_in_placement_volume",
        "ofz_pk_placement_volume",
        "cumulative_demand",
        "cumulative_supply",
        "cumulative_placement_volume",
        "cumulative_revenue_volume",
        "cumulative_bid_to_cover_ratio",
        "cumulative_weighted_avg_yield",
        "cumulative_auction_count",
        "data_quality_flag",
    ]


def make_output_suffix(params: report_params.ReportParams) -> str:
    return (
        f"{params.period_type}_{params.aggregation_mode}_{params.report_date.isoformat()}_"
        f"retrospective_{params.retrospective_years}"
    )


def write_xlsx_with_fallback(
    metrics: pd.DataFrame,
    xlsx_path: Path,
    limitations: list[str],
) -> Path:
    """Записать XLSX; при блокировке файла создать соседний fallback."""
    try:
        metrics.to_excel(xlsx_path, index=False)
        return xlsx_path
    except PermissionError:
        fallback = xlsx_path.with_name(
            f"{xlsx_path.stem}_fallback_{datetime.now().strftime('%Y%m%d_%H%M%S')}{xlsx_path.suffix}"
        )
        metrics.to_excel(fallback, index=False)
        limitations.append(f"Основной XLSX был заблокирован; создан fallback-файл `{fallback.name}`.")
        return fallback


def build_report(
    params: report_params.ReportParams,
    metrics: pd.DataFrame,
    source_path: Path,
    source_kind: str,
    csv_path: Path,
    xlsx_path: Path,
    limitations: list[str],
) -> str:
    """Сформировать Markdown-отчет по monthly layer."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    periods = sorted(metrics["report_period_label"].dropna().astype(str).unique().tolist())
    lines = [
        "# Помесячная аналитика ОФЗ",
        "",
        f"Дата формирования: `{now}`.",
        "",
        "## Параметры",
        "",
        f"- `report_date`: `{params.report_date.isoformat()}`",
        f"- `retrospective_years`: `{params.retrospective_years}`",
        f"- `period_type`: `{params.period_type}`",
        f"- `aggregation_mode`: `{params.aggregation_mode}`",
        f"- Периодов сравнения: `{len(params.periods)}`",
        "",
        "## Источник",
        "",
        f"- Тип источника: `{source_kind}`",
        f"- Файл: `{source_path.relative_to(config.PROJECT_ROOT).as_posix()}`",
        "",
        "## Назначение слоя",
        "",
        "- Monthly layer объясняет структуру накопленного итога через месячные значения.",
        "- Месячные поля считаются за конкретный календарный месяц.",
        "- Накопленные поля считаются с января до текущего месяца включительно.",
        "- Для `month + cumulative + report_date=2026-05-01` слой должен содержать январь, февраль, март и апрель по каждому году ретроспективы.",
        "",
        "## Output",
        "",
        f"- Processed dataset: `{MONTHLY_METRICS_CSV.relative_to(config.PROJECT_ROOT).as_posix()}`",
        f"- CSV export: `{csv_path.relative_to(config.PROJECT_ROOT).as_posix()}`",
        f"- XLSX export: `{xlsx_path.relative_to(config.PROJECT_ROOT).as_posix()}`",
        f"- Строк monthly layer: `{len(metrics)}`",
        "",
        "## Периоды",
        "",
    ]
    for period in periods:
        part = metrics.loc[metrics["report_period_label"].astype(str) == period]
        month_min = part["month"].min() if not part.empty else ""
        month_max = part["month"].max() if not part.empty else ""
        lines.append(f"- `{period}`: `{month_min}` - `{month_max}`, месяцев: `{len(part)}`")

    lines.extend(
        [
            "",
            "## Ограничения",
            "",
        ]
    )
    if limitations:
        for limitation in limitations:
            lines.append(f"- {limitation}")
    else:
        lines.append("- Существенных ограничений не выявлено.")

    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
