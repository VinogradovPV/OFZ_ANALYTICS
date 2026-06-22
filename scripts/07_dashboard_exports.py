"""Этап 9.1: экспорт dashboard-ready datasets для BI и интерактивного dashboard."""

from __future__ import annotations

import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, report_params, utils, yield_policy
else:
    from . import config, report_params, utils, yield_policy


DASHBOARDS_DIR = config.DASHBOARDS_DIR
DASHBOARDS_MONTHLY_DIR = config.DASHBOARDS_MONTHLY_DIR
DASHBOARDS_SEMANTIC_LAYER_DIR = config.DASHBOARDS_SEMANTIC_LAYER_DIR
DASHBOARD_EXPORTS_REPORT = config.get_doc_path("dashboard_exports_report.md")
DASHBOARD_EXPORTS_LIMITATIONS = config.get_doc_path("dashboard_exports_limitations.md")


@dataclass(frozen=True)
class ExportResult:
    dataset_name: str
    path: Path
    row_count: int
    description: str


def main(argv: Sequence[str] | None = None) -> int:
    """Сформировать dashboard-ready exports из параметризованного report scope."""
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт Этапа 9.1: dashboard exports")

    params = report_params.parse_report_args(argv)
    limitations: list[str] = []
    source = read_report_scope()
    scope = filter_scope(source, params)
    if scope.empty:
        raise ValueError(build_empty_scope_message(source, params))

    prepared = prepare_dashboard_scope(scope, limitations)
    ensure_dashboard_directories()
    suffix = make_suffix(params)

    exports: list[ExportResult] = []
    exports.append(write_dataset("auction_level", build_auction_level(prepared, limitations), suffix, params, "Строки уровня отдельного размещения / аукциона."))
    exports.append(write_dataset("period_summary", build_period_summary(prepared), suffix, params, "Периодная сводка спроса, предложения, размещения и доходности."))
    exports.append(write_dataset("kpi_summary", build_kpi_summary(prepared), suffix, params, "KPI в long-format для карточек dashboard."))
    exports.append(write_dataset("maturity_structure", build_maturity_structure(prepared), suffix, params, "Структура размещения по срокам обращения."))
    exports.append(write_dataset("yield_distribution", build_yield_distribution(prepared), suffix, params, "Распределение доходности ОФЗ-ПД по периодам."))
    exports.append(write_dataset("demand_supply", build_demand_supply(prepared, limitations), suffix, params, "Спрос и предложение по периодам и форматам."))

    metadata_path = write_metadata(prepared, params, suffix, limitations)
    exports.append(ExportResult("metadata", metadata_path, 1, "JSON metadata по dashboard exports."))

    dictionary = build_data_dictionary()
    exports.append(write_dataset("data_dictionary", dictionary, suffix, params, "Словарь данных dashboard exports."))

    exports.extend(build_semantic_layer_exports(params, suffix))

    monthly_exports = build_monthly_dashboard_exports(params, suffix, limitations)
    exports.extend(monthly_exports)

    utils.write_markdown(DASHBOARD_EXPORTS_REPORT, build_report(params, prepared, exports))
    utils.write_markdown(DASHBOARD_EXPORTS_LIMITATIONS, build_limitations_report(params, limitations))

    logger.info("Dashboard exports сформированы: %s", [str(item.path) for item in exports])
    logger.info("Этап 9.1 завершен")
    return 0


def read_report_scope() -> pd.DataFrame:
    """Прочитать report scope или остановиться с понятным сообщением."""
    if not config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.exists():
        raise FileNotFoundError(
            "Не найден data/processed/ofz_auctions_report_scope.csv. "
            "Сначала выполните этап parameterized report scope."
        )
    return pd.read_csv(config.OFZ_AUCTIONS_REPORT_SCOPE_CSV)


def filter_scope(scope: pd.DataFrame, params: report_params.ReportParams) -> pd.DataFrame:
    """Оставить только периоды, соответствующие параметрам отчета."""
    required = {"report_period_label", "report_period_type", "aggregation_mode"}
    missing = required.difference(scope.columns)
    if missing:
        raise ValueError(f"В report scope отсутствуют обязательные колонки: {', '.join(sorted(missing))}.")

    labels = {str(period["label"]) for period in params.periods}
    mask = (
        scope["report_period_label"].astype("string").isin(labels)
        & (scope["report_period_type"].astype("string") == params.period_type)
        & (scope["aggregation_mode"].astype("string") == params.aggregation_mode)
    )
    return scope.loc[mask].copy()


def build_empty_scope_message(scope: pd.DataFrame, params: report_params.ReportParams) -> str:
    """Сформировать понятное сообщение, если report scope не соответствует параметрам запуска."""
    expected_labels = [str(period["report_period_label"]) for period in params.periods]
    available_summary = summarize_available_scope(scope)
    command = (
        ".\\.venv\\Scripts\\python.exe scripts\\period_filter.py "
        f"--report-date {params.report_date.isoformat()} "
        f"--retrospective-years {params.retrospective_years} "
        f"--period-type {params.period_type} "
        f"--aggregation-mode {params.aggregation_mode}"
    )
    return (
        "Report scope пуст после фильтрации по параметрам отчета; dashboard exports не сформированы.\n"
        f"Запрошенные параметры: period_type={params.period_type}, "
        f"aggregation_mode={params.aggregation_mode}, report_date={params.report_date.isoformat()}, "
        f"retrospective_years={params.retrospective_years}.\n"
        f"Ожидаемые report_period_label: {', '.join(expected_labels)}.\n"
        f"Доступные периоды в data/processed/ofz_auctions_report_scope.csv: {available_summary}.\n"
        "Сначала пересоберите parameterized report scope командой:\n"
        f"{command}"
    )


def summarize_available_scope(scope: pd.DataFrame) -> str:
    """Кратко описать доступные периоды в существующем report scope."""
    required = ["report_period_type", "aggregation_mode", "report_period_label"]
    if any(column not in scope.columns for column in required):
        return "невозможно определить: в report scope нет обязательных period columns"
    summary = (
        scope[required]
        .drop_duplicates()
        .sort_values(required)
        .head(20)
        .astype(str)
        .agg("/".join, axis=1)
        .tolist()
    )
    if not summary:
        return "report scope не содержит периодов"
    suffix = "" if len(summary) < 20 else "; ..."
    return "; ".join(summary) + suffix


def prepare_dashboard_scope(scope: pd.DataFrame, limitations: list[str]) -> pd.DataFrame:
    """Подготовить стабильные dashboard-поля без изменения исходного report scope."""
    df = scope.copy()

    df["auction_date"] = get_text(df, "auction_date")
    df["issue_code"] = get_text(df, "issue_code")
    df["ofz_type"] = get_text(df, "ofz_type", default="Не определено")
    df["format"] = get_text(df, "format", default="Не определено")
    df["report_period_label"] = get_text(df, "report_period_label")
    df["report_period_type"] = get_text(df, "report_period_type")
    df["aggregation_mode"] = get_text(df, "aggregation_mode")
    df["report_year"] = get_numeric(df, ["report_year"]).astype("Int64")
    df["is_target_period"] = get_bool(df, "is_target_period")

    df["demand_volume"] = get_numeric(df, ["demand_volume", "demand_amount_mln_rub"])
    df["supply_volume"] = get_numeric(df, ["supply_volume", "offer_amount_mln_rub"])
    df["placement_volume"] = get_numeric(df, ["placement_volume", "placement_amount_mln_rub"])
    df["revenue_volume"] = get_numeric(df, ["revenue_volume", "revenue_amount_mln_rub", "placement_revenue_mln_rub"])
    df["weighted_avg_yield"] = get_numeric(df, ["weighted_avg_yield", "weighted_avg_yield_pct", "yield"])
    df["cutoff_yield"] = get_numeric(df, ["cutoff_yield", "cutoff_yield_pct"])
    df["cutoff_price"] = get_numeric(df, ["cutoff_price", "cutoff_price_pct"])
    df["weighted_avg_price"] = get_numeric(df, ["weighted_avg_price", "weighted_avg_price_pct"])
    df["discount_to_nominal"] = get_numeric(df, ["discount_to_nominal"])
    if df["discount_to_nominal"].isna().all() and df["cutoff_price"].notna().any():
        df["discount_to_nominal"] = 100 - df["cutoff_price"]

    df["demand_satisfaction_ratio"] = get_numeric(df, ["demand_satisfaction_ratio"])
    calculated_satisfaction = safe_divide(df["placement_volume"], df["demand_volume"])
    df["demand_satisfaction_ratio"] = df["demand_satisfaction_ratio"].combine_first(calculated_satisfaction)
    df["demand_to_placement_ratio"] = safe_divide(df["demand_volume"], df["placement_volume"])
    df["bid_to_cover_ratio"] = safe_divide(df["demand_volume"], df["supply_volume"])

    df["maturity_years"] = get_numeric(df, ["maturity_years"])
    if df["maturity_years"].isna().all() and "days_to_maturity" in df.columns:
        df["maturity_years"] = get_numeric(df, ["days_to_maturity"]) / 365.25
    df["maturity_bucket"] = get_text(df, "maturity_bucket")
    missing_bucket = df["maturity_bucket"].isna() | (df["maturity_bucket"].astype("string").str.len() == 0)
    df.loc[missing_bucket, "maturity_bucket"] = df.loc[missing_bucket, "maturity_years"].map(classify_maturity)
    df["maturity_bucket_label"] = get_text(df, "maturity_bucket_label")
    missing_label = df["maturity_bucket_label"].isna() | (df["maturity_bucket_label"].astype("string").str.len() == 0)
    df.loc[missing_label, "maturity_bucket_label"] = df.loc[missing_label, "maturity_bucket"].map(maturity_label)

    df["data_quality_flag"] = get_text(df, "data_quality_flag", default="ok")

    normalized = yield_policy.apply_base_yield_policy(
        df,
        ("weighted_avg_yield", "cutoff_yield"),
    )
    for column in (
        "weighted_avg_yield",
        "cutoff_yield",
        "yield_applicable",
        "yield_exclusion_reason",
        "yield_scope",
    ):
        df[column] = normalized[column]

    register_missing_fields(df, limitations)
    register_context_limitations(df, limitations)
    return df


def get_text(df: pd.DataFrame, column: str, default: str = "") -> pd.Series:
    if column in df.columns:
        return df[column].astype("string")
    return pd.Series(default, index=df.index, dtype="string")


def get_bool(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        return pd.Series(False, index=df.index, dtype="bool")
    values = df[column]
    if pd.api.types.is_bool_dtype(values):
        return values.fillna(False).astype(bool)
    return values.astype("string").str.lower().isin({"true", "1", "yes", "да"})


def get_numeric(df: pd.DataFrame, candidates: Sequence[str]) -> pd.Series:
    for column in candidates:
        if column in df.columns:
            return pd.to_numeric(df[column], errors="coerce")
    return pd.Series(pd.NA, index=df.index, dtype="Float64")


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    denominator_numeric = pd.to_numeric(denominator, errors="coerce")
    numerator_numeric = pd.to_numeric(numerator, errors="coerce")
    result = numerator_numeric / denominator_numeric
    return result.mask(denominator_numeric.isna() | (denominator_numeric <= 0))


def classify_maturity(value: Any) -> str:
    if pd.isna(value):
        return "requires_review"
    years = float(value)
    if years <= 5:
        return "short_term"
    if years <= 10:
        return "medium_term"
    return "long_term"


def maturity_label(bucket: Any) -> str:
    mapping = {
        "short_term": "Краткосрочные (до 5 лет включительно)",
        "medium_term": "Среднесрочные (свыше 5 до 10 лет включительно)",
        "long_term": "Долгосрочные (более 10 лет)",
        "requires_review": "Требует проверки",
    }
    return mapping.get(str(bucket), "Требует проверки")


def register_missing_fields(df: pd.DataFrame, limitations: list[str]) -> None:
    checks = {
        "revenue_volume": "Объем выручки отсутствует или полностью пуст; соответствующие поля экспортируются пустыми.",
        "cutoff_yield": "Доходность отсечения отсутствует или полностью пуста; анализ отсечения ограничен.",
        "cutoff_price": "Цена отсечения отсутствует или полностью пуста; discount_to_nominal может быть недоступен.",
        "weighted_avg_price": "Средневзвешенная цена отсутствует или полностью пуста.",
        "weighted_avg_yield": "Средневзвешенная доходность отсутствует или полностью пуста; yield-аналитика ограничена.",
        "supply_volume": "Объем предложения отсутствует или полностью пуст; bid_to_cover_ratio не рассчитывается.",
    }
    for column, message in checks.items():
        if column not in df.columns or df[column].isna().all():
            limitations.append(message)


def register_context_limitations(df: pd.DataFrame, limitations: list[str]) -> None:
    zero_placement = int((pd.to_numeric(df["placement_volume"], errors="coerce") <= 0).sum())
    if zero_placement:
        limitations.append(f"Строки с нулевым или отрицательным размещением: {zero_placement}; demand_to_placement_ratio по ним пустой.")

    drpa = int(df["format"].astype("string").str.upper().str.contains("ДРПА", na=False).sum())
    if drpa:
        limitations.append(f"Строки ДРПА: {drpa}; они не должны смешиваться с demand-based ratios без проверки валидности спроса.")

    review = int(df["maturity_bucket"].astype("string").eq("requires_review").sum())
    if review:
        limitations.append(f"Строки с maturity_bucket = requires_review: {review}; сроковая структура требует проверки.")


def build_auction_level(df: pd.DataFrame, limitations: list[str]) -> pd.DataFrame:
    columns = [
        "auction_date",
        "report_period_label",
        "report_year",
        "report_period_type",
        "aggregation_mode",
        "is_target_period",
        "issue_code",
        "ofz_type",
        "format",
        "maturity_years",
        "maturity_bucket",
        "maturity_bucket_label",
        "demand_volume",
        "supply_volume",
        "placement_volume",
        "revenue_volume",
        "weighted_avg_yield",
        "cutoff_yield",
        "cutoff_price",
        "weighted_avg_price",
        "discount_to_nominal",
        "demand_satisfaction_ratio",
        "demand_to_placement_ratio",
        "bid_to_cover_ratio",
        "data_quality_flag",
    ]
    for column in columns:
        if column not in df.columns:
            df[column] = pd.NA
            limitations.append(f"В auction-level export отсутствовало поле `{column}`; колонка создана пустой.")
    return df[columns].copy()


def build_period_summary(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["report_period_label", "report_year", "report_period_type", "aggregation_mode", "is_target_period"]
    grouped = df.groupby(group_cols, dropna=False)
    yield_data = df.loc[
        yield_policy.base_yield_cohort_mask(df, "weighted_avg_yield", "placement_volume")
    ]
    yield_grouped = yield_data.groupby(group_cols, dropna=False)
    result = grouped.agg(
        auction_count=("report_period_label", "size"),
        total_demand=("demand_volume", "sum"),
        total_supply=("supply_volume", "sum"),
        total_placement_volume=("placement_volume", "sum"),
        total_revenue_volume=("revenue_volume", "sum"),
    ).reset_index()
    yield_summary = yield_grouped.agg(
        yield_min=("weighted_avg_yield", "min"),
        yield_median=("weighted_avg_yield", "median"),
        yield_max=("weighted_avg_yield", "max"),
    ).reset_index()
    result = result.merge(yield_summary, on=group_cols, how="left")
    result["bid_to_cover_ratio"] = safe_divide(result["total_demand"], result["total_supply"])
    result["demand_to_placement_ratio"] = safe_divide(result["total_demand"], result["total_placement_volume"])
    result["weighted_avg_yield_by_placement"] = [
        weighted_average_by_placement(part, "weighted_avg_yield") for _, part in grouped
    ]
    return result[
        group_cols
        + [
            "auction_count",
            "total_demand",
            "total_supply",
            "total_placement_volume",
            "total_revenue_volume",
            "bid_to_cover_ratio",
            "demand_to_placement_ratio",
            "weighted_avg_yield_by_placement",
            "yield_min",
            "yield_median",
            "yield_max",
        ]
    ]


def weighted_average_by_placement(df: pd.DataFrame, value_column: str) -> float | None:
    values = pd.to_numeric(df[value_column], errors="coerce")
    weights = pd.to_numeric(df["placement_volume"], errors="coerce")
    mask = yield_policy.base_yield_cohort_mask(df, value_column, "placement_volume")
    if not mask.any():
        return None
    return float((values.loc[mask] * weights.loc[mask]).sum() / weights.loc[mask].sum())


def build_kpi_summary(df: pd.DataFrame) -> pd.DataFrame:
    period_summary = build_period_summary(df)
    rows: list[dict[str, Any]] = []
    for _, row in period_summary.iterrows():
        period_df = df.loc[df["report_period_label"].astype("string") == str(row["report_period_label"])]
        placement_total = float(row["total_placement_volume"]) if pd.notna(row["total_placement_volume"]) else 0.0
        rows.extend(kpi_rows_for_period(row, period_df, placement_total))
    return pd.DataFrame(rows)


def kpi_rows_for_period(row: pd.Series, period_df: pd.DataFrame, placement_total: float) -> list[dict[str, Any]]:
    base = {
        "report_period_label": row["report_period_label"],
        "report_year": row["report_year"],
        "aggregation_mode": row["aggregation_mode"],
        "is_target_period": row["is_target_period"],
    }
    kpis = [
        ("Спрос", "Совокупный спрос", row["total_demand"], "млн руб.", "Емкость спроса инвесторов"),
        ("Предложение", "Совокупное предложение", row["total_supply"], "млн руб.", "Объявленный объем предложения"),
        ("Размещение", "Объем размещения", row["total_placement_volume"], "млн руб.", "Фактически размещенный объем"),
        ("Размещение", "Объем выручки", row["total_revenue_volume"], "млн руб.", "Денежная выручка, если поле доступно"),
        ("Спрос", "Bid-to-cover", row["bid_to_cover_ratio"], "ratio", "Спрос / предложение"),
        ("Спрос", "Спрос / размещение", row["demand_to_placement_ratio"], "ratio", "Спрос / фактическое размещение"),
        ("Доходность", "Средневзвешенная доходность", row["weighted_avg_yield_by_placement"], "%", "Взвешено по placement_volume"),
        ("Доходность", "Минимальная доходность", row["yield_min"], "%", "Минимальная валидная доходность"),
        ("Доходность", "Медианная доходность", row["yield_median"], "%", "Медианная валидная доходность"),
        ("Доходность", "Максимальная доходность", row["yield_max"], "%", "Максимальная валидная доходность"),
        ("Формат", "Доля аукционов", format_share(period_df, "Аукцион", placement_total), "share", "Доля размещения формата Аукцион"),
        ("Формат", "Доля ДРПА", format_share(period_df, "ДРПА", placement_total), "share", "Доля размещения формата ДРПА"),
        ("Срок", "Доля долгосрочных", maturity_share(period_df, "long_term", placement_total), "share", "Доля долгосрочных размещений"),
        ("Срок", "Доля среднесрочных", maturity_share(period_df, "medium_term", placement_total), "share", "Доля среднесрочных размещений"),
        ("Срок", "Доля краткосрочных", maturity_share(period_df, "short_term", placement_total), "share", "Доля краткосрочных размещений"),
    ]
    rows = []
    quality = collapse_quality_flag(period_df)
    for group, name, value, unit, interpretation in kpis:
        item = dict(base)
        item.update(
            {
                "kpi_group": group,
                "kpi_name": name,
                "kpi_value": value,
                "kpi_unit": unit,
                "interpretation": interpretation,
                "data_quality_flag": quality,
            }
        )
        rows.append(item)
    return rows


def format_share(df: pd.DataFrame, value: str, total: float) -> float | None:
    if total <= 0:
        return None
    mask = df["format"].astype("string").str.upper().str.contains(value.upper(), na=False)
    return float(pd.to_numeric(df.loc[mask, "placement_volume"], errors="coerce").sum() / total)


def maturity_share(df: pd.DataFrame, bucket: str, total: float) -> float | None:
    if total <= 0:
        return None
    mask = df["maturity_bucket"].astype("string") == bucket
    return float(pd.to_numeric(df.loc[mask, "placement_volume"], errors="coerce").sum() / total)


def build_maturity_structure(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["report_period_label", "aggregation_mode", "maturity_bucket", "maturity_bucket_label"]
    grouped = df.groupby(group_cols, dropna=False)
    result = grouped.agg(
        placement_volume=("placement_volume", "sum"),
        auction_count=("report_period_label", "size"),
    ).reset_index()
    totals = result.groupby(["report_period_label", "aggregation_mode"], dropna=False)["placement_volume"].transform("sum")
    result["placement_volume_share"] = safe_divide(result["placement_volume"], totals)
    result["weighted_avg_yield_by_placement"] = [
        weighted_average_by_placement(part, "weighted_avg_yield") for _, part in grouped
    ]
    return result[
        group_cols
        + [
            "placement_volume",
            "placement_volume_share",
            "auction_count",
            "weighted_avg_yield_by_placement",
        ]
    ]


def build_yield_distribution(df: pd.DataFrame) -> pd.DataFrame:
    data = df.dropna(subset=["weighted_avg_yield"]).copy()
    group_cols = ["report_period_label", "aggregation_mode", "ofz_type"]
    rows: list[dict[str, Any]] = []
    for keys, part in data.groupby(group_cols, dropna=False):
        period_label, aggregation_mode, ofz_type = keys
        yields = pd.to_numeric(part["weighted_avg_yield"], errors="coerce").dropna()
        rows.append(
            {
                "report_period_label": period_label,
                "aggregation_mode": aggregation_mode,
                "ofz_type": ofz_type,
                "yield_min": yields.min(),
                "yield_q1": yields.quantile(0.25),
                "yield_median": yields.median(),
                "yield_q3": yields.quantile(0.75),
                "yield_max": yields.max(),
                "yield_weighted_avg": weighted_average_by_placement(part, "weighted_avg_yield"),
                "auction_count": len(part),
                "placement_volume": pd.to_numeric(part["placement_volume"], errors="coerce").sum(),
            }
        )
    return pd.DataFrame(rows)


def build_demand_supply(df: pd.DataFrame, limitations: list[str]) -> pd.DataFrame:
    group_cols = ["report_period_label", "aggregation_mode", "format"]
    grouped = df.groupby(group_cols, dropna=False)
    result = grouped.agg(
        total_demand=("demand_volume", "sum"),
        total_supply=("supply_volume", "sum"),
        total_placement_volume=("placement_volume", "sum"),
        auction_count=("report_period_label", "size"),
    ).reset_index()
    result["bid_to_cover_ratio"] = safe_divide(result["total_demand"], result["total_supply"])
    result["demand_to_placement_ratio"] = safe_divide(result["total_demand"], result["total_placement_volume"])
    result["demand_satisfaction_ratio"] = safe_divide(result["total_placement_volume"], result["total_demand"])
    result["data_quality_flag"] = [
        demand_supply_quality(part, limitations) for _, part in grouped
    ]
    return result[
        group_cols
        + [
            "total_demand",
            "total_supply",
            "total_placement_volume",
            "bid_to_cover_ratio",
            "demand_to_placement_ratio",
            "demand_satisfaction_ratio",
            "auction_count",
            "data_quality_flag",
        ]
    ]


def demand_supply_quality(part: pd.DataFrame, limitations: list[str]) -> str:
    format_values = part["format"].dropna().astype(str)
    format_value = format_values.iloc[0] if not format_values.empty else ""
    has_missing_demand = part["demand_volume"].isna().any()
    has_missing_supply = part["supply_volume"].isna().any()
    is_drpa = "ДРПА" in format_value.upper()
    if is_drpa and has_missing_demand:
        limitations.append("В demand/supply export есть ДРПА без спроса; demand-based ratios по ним требуют ограничения.")
        return "drpa_missing_demand"
    if has_missing_demand or has_missing_supply:
        return "missing_demand_or_supply"
    return "ok"


def collapse_quality_flag(df: pd.DataFrame) -> str:
    if "data_quality_flag" not in df.columns:
        return "ok"
    values = set(df["data_quality_flag"].dropna().astype(str))
    if not values:
        return "ok"
    if values == {"ok"}:
        return "ok"
    return "; ".join(sorted(values))


def ensure_dashboard_directories() -> None:
    """Создать директории dashboard exports без смешивания с reports и chart_data."""
    for directory in (DASHBOARDS_DIR, DASHBOARDS_MONTHLY_DIR, DASHBOARDS_SEMANTIC_LAYER_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def dashboard_output_dir(params: report_params.ReportParams, dataset_name: str) -> Path:
    """Вернуть целевую папку dashboard export."""
    if "semantic" in dataset_name.lower():
        return DASHBOARDS_SEMANTIC_LAYER_DIR
    if params.period_type == "month":
        return DASHBOARDS_MONTHLY_DIR
    return DASHBOARDS_DIR


def write_dataset(
    dataset_name: str,
    data: pd.DataFrame,
    suffix: str,
    params: report_params.ReportParams,
    description: str,
) -> ExportResult:
    path = dashboard_output_dir(params, dataset_name) / f"dashboard_{dataset_name}_{suffix}.csv"
    data.to_csv(path, index=False, encoding="utf-8")
    return ExportResult(dataset_name=dataset_name, path=path, row_count=len(data), description=description)


def write_semantic_dataset(
    dataset_name: str,
    data: pd.DataFrame,
    suffix: str,
    description: str,
) -> ExportResult:
    """Сохранить таблицу semantic layer в outputs/dashboards/semantic_layer/."""
    path = DASHBOARDS_SEMANTIC_LAYER_DIR / f"dashboard_semantic_layer_{dataset_name}_{suffix}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path, index=False, encoding="utf-8")
    return ExportResult(
        dataset_name=f"semantic_layer_{dataset_name}",
        path=path,
        row_count=len(data),
        description=description,
    )


def build_semantic_layer_exports(
    params: report_params.ReportParams,
    suffix: str,
) -> list[ExportResult]:
    """Сформировать semantic layer для BI: поля, меры, измерения, связи и manifest."""
    results: list[ExportResult] = []
    fields = build_semantic_fields_catalog()
    metrics = build_semantic_metrics_catalog()
    dimensions = build_semantic_dimensions_catalog()
    relationships = build_semantic_relationships_catalog()

    results.append(
        write_semantic_dataset(
            "fields",
            fields,
            suffix,
            "Каталог полей semantic layer: русские названия, technical names, units и правила расчета.",
        )
    )
    results.append(
        write_semantic_dataset(
            "metrics",
            metrics,
            suffix,
            "Каталог управленческих метрик semantic layer с формулами и ограничениями.",
        )
    )
    results.append(
        write_semantic_dataset(
            "dimensions",
            dimensions,
            suffix,
            "Каталог измерений, рекомендуемых фильтров и default sorting для dashboard.",
        )
    )
    results.append(
        write_semantic_dataset(
            "relationships",
            relationships,
            suffix,
            "Контракт связей между dashboard-ready таблицами.",
        )
    )

    manifest_path = write_semantic_manifest(params, suffix, results)
    results.append(
        ExportResult(
            dataset_name="semantic_layer_manifest",
            path=manifest_path,
            row_count=1,
            description="JSON manifest semantic layer с параметрами отчета и списком semantic exports.",
        )
    )
    return results


def build_semantic_fields_catalog() -> pd.DataFrame:
    """Собрать единый каталог полей из основного и помесячного словаря данных."""
    dictionaries = [build_data_dictionary(), build_monthly_data_dictionary()]
    fields = pd.concat(dictionaries, ignore_index=True)
    fields["semantic_role"] = fields["column_name"].map(semantic_role_for_column)
    fields["data_type"] = fields["unit"].map(data_type_for_unit)
    fields["default_aggregation"] = fields["column_name"].map(default_aggregation_for_column)
    fields["display_format_ru"] = fields["unit"].map(display_format_for_unit)
    fields["recommended_filter"] = fields["semantic_role"].eq("dimension")
    return fields[
        [
            "dataset_name",
            "column_name",
            "russian_name",
            "description_ru",
            "technical_name",
            "semantic_role",
            "data_type",
            "unit",
            "display_format_ru",
            "default_aggregation",
            "calculation_rule",
            "source_fields",
            "limitations",
            "recommended_filter",
        ]
    ]


def build_semantic_metrics_catalog() -> pd.DataFrame:
    """Описать ключевые меры dashboard semantic layer."""
    rows = [
        (
            "Совокупный спрос",
            "total_demand",
            "млн руб.",
            "sum(demand_volume)",
            "dashboard_auction_level",
            "demand_volume",
            "period / format / ofz_type / maturity_bucket",
            "Спрос суммируется по аукционам и ДРПА только при валидном поле спроса.",
        ),
        (
            "Совокупное предложение",
            "total_supply",
            "млн руб.",
            "sum(supply_volume)",
            "dashboard_auction_level",
            "supply_volume",
            "period / format / ofz_type / maturity_bucket",
            "Не заменять предложением объем размещения.",
        ),
        (
            "Объем размещения по номиналу",
            "total_placement_volume",
            "млн руб.",
            "sum(placement_volume)",
            "dashboard_auction_level",
            "placement_volume",
            "period / format / ofz_type / maturity_bucket",
            "Для визуализаций отображается в млрд рублей без изменения source values.",
        ),
        (
            "Bid-to-cover",
            "bid_to_cover_ratio",
            "ratio",
            "sum(demand_volume) / sum(supply_volume)",
            "dashboard_period_summary",
            "demand_volume, supply_volume",
            "period",
            "Не равно demand_to_placement_ratio.",
        ),
        (
            "Спрос / размещение",
            "demand_to_placement_ratio",
            "ratio",
            "sum(demand_volume) / sum(placement_volume)",
            "dashboard_period_summary",
            "demand_volume, placement_volume",
            "period",
            "Не называть классическим bid-to-cover.",
        ),
        (
            "Коэффициент удовлетворения спроса",
            "demand_satisfaction_ratio",
            "ratio",
            "sum(placement_volume) / sum(demand_volume)",
            "dashboard_demand_supply",
            "placement_volume, demand_volume",
            "period / format",
            "Пусто при отсутствующем или нулевом спросе.",
        ),
        (
            "Средневзвешенная доходность",
            "weighted_avg_yield_by_placement",
            "%",
            "sum(weighted_avg_yield * placement_volume) / sum(placement_volume)",
            "dashboard_period_summary",
            "weighted_avg_yield, placement_volume",
            "period",
            "Пусто при отсутствии валидной доходности или размещения.",
        ),
        (
            "Минимальная доходность",
            "yield_min",
            "%",
            "min(weighted_avg_yield)",
            "dashboard_yield_distribution",
            "weighted_avg_yield",
            "period / ofz_type",
            "Строки без доходности исключаются из yield distribution.",
        ),
        (
            "Медианная доходность",
            "yield_median",
            "%",
            "median(weighted_avg_yield)",
            "dashboard_yield_distribution",
            "weighted_avg_yield",
            "period / ofz_type",
            "Статистическая интерпретация ограничена при n < 3.",
        ),
        (
            "Максимальная доходность",
            "yield_max",
            "%",
            "max(weighted_avg_yield)",
            "dashboard_yield_distribution",
            "weighted_avg_yield",
            "period / ofz_type",
            "Выбросы не скрываются; проверяются через data_quality_flag.",
        ),
    ]
    return pd.DataFrame(
        rows,
        columns=[
            "russian_name",
            "technical_name",
            "unit",
            "calculation_rule",
            "source_dataset",
            "source_fields",
            "grain",
            "limitations",
        ],
    )


def build_semantic_dimensions_catalog() -> pd.DataFrame:
    """Описать измерения и фильтры dashboard."""
    rows = [
        ("Отчетный период", "report_period_label", "period", "dashboard_period_summary", "report_period_order/report_period_start", "Основная ось сравнения."),
        ("Год", "report_year", "period", "dashboard_period_summary", "report_year", "Используется для ретроспективы."),
        ("Режим агрегации", "aggregation_mode", "parameter", "all", "cumulative before point", "cumulative и point не смешиваются."),
        ("Вид ОФЗ", "ofz_type", "security", "dashboard_auction_level", "ofz_type", "Не ограничивать только ОФЗ-ПД."),
        ("Формат", "format", "auction_format", "dashboard_auction_level", "format", "ДРПА не смешивать с demand-based ratios без проверки спроса."),
        ("Сроковая категория", "maturity_bucket", "maturity", "dashboard_auction_level", "short_term, medium_term, long_term, requires_review", "Классификация: до 5 лет; свыше 5 до 10; более 10."),
        ("Код выпуска", "issue_code", "security", "dashboard_auction_level", "issue_code", "Drill-down уровень выпуска."),
        ("Дата размещения", "auction_date", "date", "dashboard_auction_level", "auction_date", "Drill-down внутри периода."),
    ]
    return pd.DataFrame(
        rows,
        columns=[
            "russian_name",
            "technical_name",
            "dimension_group",
            "source_dataset",
            "default_sort",
            "limitations",
        ],
    )


def build_semantic_relationships_catalog() -> pd.DataFrame:
    """Описать связи между dashboard-ready таблицами."""
    rows = [
        ("dashboard_auction_level", "report_period_label", "dashboard_period_summary", "report_period_label", "many_to_one", "single", "Связь размещений с периодной сводкой."),
        ("dashboard_auction_level", "report_period_label", "dashboard_kpi_summary", "report_period_label", "many_to_many_limited", "single", "Использовать через периодные фильтры и KPI group."),
        ("dashboard_auction_level", "report_period_label", "dashboard_maturity_structure", "report_period_label", "many_to_many_limited", "single", "Структура сроков по периоду."),
        ("dashboard_auction_level", "report_period_label", "dashboard_yield_distribution", "report_period_label", "many_to_many_limited", "single", "Доходность по периоду и виду ОФЗ."),
        ("dashboard_auction_level", "report_period_label", "dashboard_demand_supply", "report_period_label", "many_to_many_limited", "single", "Спрос/предложение по периоду и формату."),
        ("dashboard_monthly_metrics", "report_period_label", "dashboard_period_summary", "report_period_label", "many_to_one", "single", "Monthly layer объясняет состав cumulative period."),
    ]
    return pd.DataFrame(
        rows,
        columns=[
            "from_dataset",
            "from_column",
            "to_dataset",
            "to_column",
            "relationship_type",
            "filter_direction",
            "description_ru",
        ],
    )


def write_semantic_manifest(
    params: report_params.ReportParams,
    suffix: str,
    semantic_exports: Sequence[ExportResult],
) -> Path:
    """Сохранить JSON manifest semantic layer."""
    manifest = {
        "report_date": params.report_date.isoformat(),
        "period_type": params.period_type,
        "aggregation_mode": params.aggregation_mode,
        "retrospective_years": params.retrospective_years,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "semantic_layer_dir": str(DASHBOARDS_SEMANTIC_LAYER_DIR.relative_to(config.ROOT_DIR)),
        "exports": [
            {
                "dataset_name": item.dataset_name,
                "path": str(item.path.relative_to(config.ROOT_DIR)),
                "row_count": item.row_count,
                "description": item.description,
            }
            for item in semantic_exports
        ],
        "volume_policy": "placement_volume хранится в млн рублей; визуализации могут отображать placement_volume_bln в млрд рублей.",
        "ratio_policy": {
            "bid_to_cover_ratio": "demand_volume / supply_volume",
            "demand_to_placement_ratio": "demand_volume / placement_volume",
            "demand_satisfaction_ratio": "placement_volume / demand_volume",
        },
    }
    path = DASHBOARDS_SEMANTIC_LAYER_DIR / f"dashboard_semantic_layer_manifest_{suffix}.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def semantic_role_for_column(column: str) -> str:
    """Определить роль поля для BI semantic layer."""
    if column in {"auction_date", "report_period_label", "report_year", "report_period_type", "aggregation_mode", "month", "month_number", "month_label", "month_start", "month_end"}:
        return "dimension"
    if column in {"issue_code", "ofz_type", "format", "maturity_bucket", "maturity_bucket_label", "data_quality_flag"}:
        return "dimension"
    if column.startswith("is_"):
        return "flag"
    if "ratio" in column or "yield" in column or "volume" in column or column.endswith("_count") or column.startswith("total_") or column.startswith("cumulative_"):
        return "measure"
    return "attribute"


def data_type_for_unit(unit: Any) -> str:
    """Определить тип данных по единице измерения словаря."""
    value = str(unit).lower()
    if value in {"date", "year", "month"}:
        return "date"
    if value in {"text", "label", "category", "flag", "mode", "boolean"}:
        return "text"
    if value in {"ratio", "share", "%", "count", "number"} or "руб" in value:
        return "number"
    return "mixed"


def default_aggregation_for_column(column: str) -> str:
    """Назначить рекомендуемую агрегацию по умолчанию."""
    if column.endswith("_count") or column.startswith("total_") or "volume" in column or column in {"demand_volume", "supply_volume", "placement_volume", "revenue_volume"}:
        return "sum"
    if "yield" in column:
        return "weighted_average_or_statistic"
    if "ratio" in column:
        return "recalculate_from_components"
    return "none"


def display_format_for_unit(unit: Any) -> str:
    """Вернуть рекомендуемый формат отображения в BI."""
    value = str(unit).lower()
    if "руб" in value:
        return "число с разделителем тысяч; для графиков объема размещения показывать млрд рублей"
    if value == "%":
        return "процент, 2 знака после запятой"
    if value in {"ratio", "share"}:
        return "коэффициент, 2-3 знака после запятой"
    if value == "count":
        return "целое число"
    return "текст/категория"


def build_monthly_dashboard_exports(
    params: report_params.ReportParams,
    suffix: str,
    limitations: list[str],
) -> list[ExportResult]:
    """Сформировать dashboard-ready exports для помесячного слоя, если он уже создан."""
    monthly_path = config.PROCESSED_DATA_DIR / "ofz_monthly_metrics.csv"
    if not monthly_path.exists():
        limitations.append(
            "Monthly dashboard exports не сформированы: отсутствует `data/processed/ofz_monthly_metrics.csv`. "
            "Сначала выполните `scripts/09_monthly_analytics.py`."
        )
        return []

    monthly = pd.read_csv(monthly_path)
    monthly = filter_monthly_metrics(monthly, params)
    if monthly.empty:
        limitations.append(
            "Monthly dashboard exports не сформированы: `ofz_monthly_metrics.csv` не содержит строк для выбранных параметров отчета."
        )
        return []

    prepared = prepare_monthly_dashboard_metrics(monthly)
    dictionary = build_monthly_data_dictionary()

    monthly_metrics_path = DASHBOARDS_MONTHLY_DIR / f"dashboard_monthly_metrics_{suffix}.csv"
    monthly_dictionary_path = DASHBOARDS_MONTHLY_DIR / f"dashboard_monthly_data_dictionary_{suffix}.csv"
    monthly_metrics_path.parent.mkdir(parents=True, exist_ok=True)
    prepared.to_csv(monthly_metrics_path, index=False, encoding="utf-8")
    dictionary.to_csv(monthly_dictionary_path, index=False, encoding="utf-8")

    return [
        ExportResult(
            "monthly_metrics",
            monthly_metrics_path,
            len(prepared),
            "BI-ready помесячные показатели для объяснения накопленного итога.",
        ),
        ExportResult(
            "monthly_data_dictionary",
            monthly_dictionary_path,
            len(dictionary),
            "Словарь данных помесячного dashboard layer.",
        ),
    ]


def filter_monthly_metrics(
    monthly: pd.DataFrame,
    params: report_params.ReportParams,
) -> pd.DataFrame:
    """Оставить только месяцы выбранного отчетного горизонта."""
    required = {"report_period_label", "aggregation_mode", "report_year"}
    missing = required.difference(monthly.columns)
    if missing:
        raise ValueError(f"В monthly metrics отсутствуют обязательные колонки: {', '.join(sorted(missing))}.")

    labels = {str(period["report_period_label"]) for period in params.periods}
    years = {int(period["report_year"]) for period in params.periods}
    report_year = pd.to_numeric(monthly["report_year"], errors="coerce").astype("Int64")
    mask = (
        monthly["report_period_label"].astype("string").isin(labels)
        & (monthly["aggregation_mode"].astype("string") == params.aggregation_mode)
        & report_year.isin(years)
    )
    return monthly.loc[mask].copy()


def prepare_monthly_dashboard_metrics(monthly: pd.DataFrame) -> pd.DataFrame:
    """Подготовить стабильный BI-ready порядок и типы колонок monthly layer."""
    result = monthly.copy()
    for column in monthly_dashboard_columns():
        if column not in result.columns:
            result[column] = pd.NA

    numeric_columns = [
        "report_year",
        "month_number",
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
        "yield_observation_count",
    ]
    for column in numeric_columns:
        result[column] = pd.to_numeric(result[column], errors="coerce")
    if "is_target_year" in result.columns:
        result["is_target_year"] = result["is_target_year"].astype("string").str.lower().isin({"true", "1", "yes"})
    result["mixed_security_types"] = result["mixed_security_types"].astype("string").str.lower().isin(
        {"true", "1", "yes"}
    )
    return result[monthly_dashboard_columns()].sort_values(["report_year", "month_number"]).reset_index(drop=True)


def monthly_dashboard_columns() -> list[str]:
    """Контракт колонок dashboard_monthly_metrics."""
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
        "yield_scope",
        "yield_observation_count",
        "mixed_security_types",
        "cumulative_demand",
        "cumulative_supply",
        "cumulative_placement_volume",
        "cumulative_revenue_volume",
        "cumulative_bid_to_cover_ratio",
        "cumulative_weighted_avg_yield",
        "cumulative_auction_count",
        "data_quality_flag",
    ]


def write_metadata(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    suffix: str,
    limitations: list[str],
) -> Path:
    periods = sorted(df["report_period_label"].dropna().astype(str).unique().tolist())
    target_periods = sorted(df.loc[df["is_target_period"], "report_period_label"].dropna().astype(str).unique().tolist())
    metadata = {
        "report_date": params.report_date.isoformat(),
        "period_type": params.period_type,
        "aggregation_mode": params.aggregation_mode,
        "retrospective_years": params.retrospective_years,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_file": str(config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.relative_to(config.ROOT_DIR)),
        "row_count": int(len(df)),
        "periods_included": periods,
        "target_period": target_periods[0] if target_periods else None,
        "maturity_bucket_rule": {
            "short_term": "до 5 лет включительно",
            "medium_term": "свыше 5 и до 10 лет включительно",
            "long_term": "более 10 лет",
            "requires_review": "срок нельзя определить",
        },
        "demand_ratio_definitions": {
            "demand_satisfaction_ratio": "placement_volume / demand_volume",
            "demand_to_placement_ratio": "demand_volume / placement_volume",
            "bid_to_cover_ratio": "demand_volume / supply_volume",
        },
        "known_limitations": sorted(set(limitations)),
    }
    path = dashboard_output_dir(params, "metadata") / f"dashboard_metadata_{suffix}.json"
    path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def build_data_dictionary() -> pd.DataFrame:
    rows = [
        ("auction_level", "auction_date", "Дата размещения", "auction_date", "date", "исходное поле", "auction_date", ""),
        ("auction_level", "report_period_label", "Отчетный период", "report_period_label", "label", "этап 4", "period_filter", ""),
        ("auction_level", "aggregation_mode", "Режим агрегации периода", "aggregation_mode", "mode", "параметр отчета", "period_filter", "cumulative и point не смешиваются в одном export"),
        ("auction_level", "issue_code", "Код выпуска", "issue_code", "text", "исходное поле", "issue_code", ""),
        ("auction_level", "ofz_type", "Вид ОФЗ", "ofz_type", "text", "feature engineering", "security_type / issue_code", ""),
        ("auction_level", "format", "Формат размещения", "format", "text", "cleaning", "Формат", "до 2024 может быть предположением"),
        ("auction_level", "maturity_bucket", "Сроковая категория", "maturity_bucket", "category", "по maturity_years", "days_to_maturity", ""),
        ("auction_level", "demand_volume", "Совокупный спрос", "demand_volume", "млн руб.", "нормализованное поле", "Совокупный объем спроса по номиналу", ""),
        ("auction_level", "supply_volume", "Объем предложения", "supply_volume", "млн руб.", "нормализованное поле", "Объем предложения", ""),
        ("auction_level", "placement_volume", "Объем размещения", "placement_volume", "млн руб.", "нормализованное поле", "Объем размещения по номиналу", ""),
        ("auction_level", "weighted_avg_yield", "Средневзвешенная доходность", "weighted_avg_yield", "%", "нормализованное поле", "Средневзвешенная доходность", ""),
        ("auction_level", "bid_to_cover_ratio", "Спрос / предложение", "bid_to_cover_ratio", "ratio", "demand_volume / supply_volume", "расчет", "не равно спрос / размещение"),
        ("auction_level", "demand_to_placement_ratio", "Спрос / размещение", "demand_to_placement_ratio", "ratio", "demand_volume / placement_volume", "расчет", "не называть bid-to-cover"),
        ("auction_level", "demand_satisfaction_ratio", "Коэффициент удовлетворения спроса", "demand_satisfaction_ratio", "ratio", "placement_volume / demand_volume", "расчет или исходное поле", ""),
        ("period_summary", "weighted_avg_yield_by_placement", "Доходность, взвешенная по размещению", "weighted_avg_yield_by_placement", "%", "sum(yield * placement) / sum(placement)", "расчет", "пусто без placement_volume"),
        ("kpi_summary", "kpi_value", "Значение KPI", "kpi_value", "mixed", "зависит от KPI", "расчет", ""),
    ]
    dictionary = pd.DataFrame(
        rows,
        columns=[
            "dataset_name",
            "column_name",
            "description_ru",
            "technical_name",
            "unit",
            "calculation_rule",
            "source_column",
            "limitations",
        ],
    )
    return enrich_dictionary_contract(dictionary)


def build_monthly_data_dictionary() -> pd.DataFrame:
    """Словарь данных для dashboard_monthly_metrics."""
    rows = [
        ("monthly_metrics", "report_year", "Год отчетного периода", "report_year", "year", "из monthly layer", "report_params / period_filter", ""),
        ("monthly_metrics", "month", "Месяц в формате YYYY-MM", "month", "month", "календарный месяц строки", "auction_date", ""),
        ("monthly_metrics", "month_number", "Номер месяца", "month_number", "number", "месяц из month_start", "auction_date", ""),
        ("monthly_metrics", "month_label", "Подпись месяца", "month_label", "label", "отображаемая метка месяца", "month", ""),
        ("monthly_metrics", "month_start", "Первый день месяца", "month_start", "date", "начало календарного месяца", "auction_date", ""),
        ("monthly_metrics", "month_end", "Последний день месяца в отчетном горизонте", "month_end", "date", "конец календарного месяца или конец report period", "report_params", ""),
        ("monthly_metrics", "report_period_label", "Отчетный период сравнения", "report_period_label", "label", "период из выбранного горизонта", "report_params", ""),
        ("monthly_metrics", "aggregation_mode", "Режим агрегации", "aggregation_mode", "mode", "cumulative или point", "CLI", "cumulative и point не смешиваются в одном export"),
        ("monthly_metrics", "is_target_year", "Признак целевого отчетного года", "is_target_year", "boolean", "true для целевого периода", "report_params", ""),
        ("monthly_metrics", "auction_count", "Количество размещений в месяце", "auction_count", "count", "count строк месяца", "ofz_monthly_metrics", ""),
        ("monthly_metrics", "total_demand", "Совокупный спрос за месяц", "total_demand", "млн руб.", "sum(demand_volume)", "demand_volume", "ДРПА интерпретируются с учетом data_quality_flag"),
        ("monthly_metrics", "total_supply", "Совокупное предложение за месяц", "total_supply", "млн руб.", "sum(supply_volume)", "supply_volume", ""),
        ("monthly_metrics", "total_placement_volume", "Объем размещения за месяц", "total_placement_volume", "млн руб.", "sum(placement_volume)", "placement_volume", ""),
        ("monthly_metrics", "total_revenue_volume", "Объем выручки за месяц", "total_revenue_volume", "млн руб.", "sum(revenue_volume)", "revenue_volume", "пусто, если поле недоступно"),
        ("monthly_metrics", "bid_to_cover_ratio", "Спрос / предложение за месяц", "bid_to_cover_ratio", "ratio", "total_demand / total_supply", "расчет", "не равно спрос / размещение"),
        ("monthly_metrics", "demand_to_placement_ratio", "Спрос / размещение за месяц", "demand_to_placement_ratio", "ratio", "total_demand / total_placement_volume", "расчет", "не называть bid-to-cover"),
        ("monthly_metrics", "demand_satisfaction_ratio", "Коэффициент удовлетворения спроса за месяц", "demand_satisfaction_ratio", "ratio", "total_placement_volume / total_demand", "расчет", ""),
        ("monthly_metrics", "yield_weighted_avg", "Средневзвешенная доходность ОФЗ-ПД за месяц", "yield_weighted_avg", "%", "sum(yield * placement) / sum(placement) для ОФЗ-ПД", "weighted_avg_yield, placement_volume, yield_scope", "пусто без валидной доходности ОФЗ-ПД или положительного размещения"),
        ("monthly_metrics", "yield_min", "Минимальная доходность ОФЗ-ПД за месяц", "yield_min", "%", "min(yield) для ОФЗ-ПД", "weighted_avg_yield, yield_scope", ""),
        ("monthly_metrics", "yield_median", "Медианная доходность ОФЗ-ПД за месяц", "yield_median", "%", "median(yield) для ОФЗ-ПД", "weighted_avg_yield, yield_scope", ""),
        ("monthly_metrics", "yield_max", "Максимальная доходность ОФЗ-ПД за месяц", "yield_max", "%", "max(yield) для ОФЗ-ПД", "weighted_avg_yield, yield_scope", ""),
        ("monthly_metrics", "placement_volume_auction", "Размещение через аукционы", "placement_volume_auction", "млн руб.", "sum(placement_volume where format != ДРПА)", "format, placement_volume", ""),
        ("monthly_metrics", "placement_volume_drpa", "Размещение через ДРПА", "placement_volume_drpa", "млн руб.", "sum(placement_volume where format = ДРПА)", "format, placement_volume", ""),
        ("monthly_metrics", "placement_volume_short_term", "Размещение краткосрочных ОФЗ", "placement_volume_short_term", "млн руб.", "sum(placement_volume where maturity_bucket=short_term)", "maturity_bucket, placement_volume", "до 5 лет включительно"),
        ("monthly_metrics", "placement_volume_medium_term", "Размещение среднесрочных ОФЗ", "placement_volume_medium_term", "млн руб.", "sum(placement_volume where maturity_bucket=medium_term)", "maturity_bucket, placement_volume", "свыше 5 и до 10 лет включительно"),
        ("monthly_metrics", "placement_volume_long_term", "Размещение долгосрочных ОФЗ", "placement_volume_long_term", "млн руб.", "sum(placement_volume where maturity_bucket=long_term)", "maturity_bucket, placement_volume", "более 10 лет"),
        ("monthly_metrics", "ofz_pd_placement_volume", "Размещение ОФЗ-ПД", "ofz_pd_placement_volume", "млн руб.", "sum(placement_volume where ofz_type contains ПД)", "ofz_type, placement_volume", ""),
        ("monthly_metrics", "ofz_in_placement_volume", "Размещение ОФЗ-ИН", "ofz_in_placement_volume", "млн руб.", "sum(placement_volume where ofz_type contains ИН)", "ofz_type, placement_volume", ""),
        ("monthly_metrics", "ofz_pk_placement_volume", "Размещение ОФЗ-ПК", "ofz_pk_placement_volume", "млн руб.", "sum(placement_volume where ofz_type contains ПК)", "ofz_type, placement_volume", ""),
        ("monthly_metrics", "cumulative_demand", "Накопленный спрос", "cumulative_demand", "млн руб.", "cumsum(total_demand) с января", "monthly layer", ""),
        ("monthly_metrics", "cumulative_supply", "Накопленное предложение", "cumulative_supply", "млн руб.", "cumsum(total_supply) с января", "monthly layer", ""),
        ("monthly_metrics", "cumulative_placement_volume", "Накопленное размещение", "cumulative_placement_volume", "млн руб.", "cumsum(total_placement_volume) с января", "monthly layer", ""),
        ("monthly_metrics", "cumulative_revenue_volume", "Накопленная выручка", "cumulative_revenue_volume", "млн руб.", "cumsum(total_revenue_volume) с января", "monthly layer", "пусто или 0 при недоступной выручке"),
        ("monthly_metrics", "cumulative_bid_to_cover_ratio", "Накопленный спрос / предложение", "cumulative_bid_to_cover_ratio", "ratio", "cumulative_demand / cumulative_supply", "расчет", ""),
        ("monthly_metrics", "cumulative_weighted_avg_yield", "Накопленная средневзвешенная доходность ОФЗ-ПД", "cumulative_weighted_avg_yield", "%", "sum(yield * placement) / sum(placement) с января только для ОФЗ-ПД", "monthly layer", ""),
        ("monthly_metrics", "yield_scope", "Область расчета доходности", "yield_scope", "scope", "фиксированное значение ofz_pd_only", "yield policy", "ОФЗ-ПК и ОФЗ-ИН исключены из базовых yield metrics"),
        ("monthly_metrics", "yield_observation_count", "Число валидных наблюдений доходности ОФЗ-ПД", "yield_observation_count", "count", "count(ОФЗ-ПД с numeric yield и placement > 0)", "monthly layer", ""),
        ("monthly_metrics", "mixed_security_types", "Признак смешанного состава типов бумаг", "mixed_security_types", "boolean", "true при наличии более одного security_type в месяце", "monthly layer", "не меняет volume totals"),
        ("monthly_metrics", "cumulative_auction_count", "Накопленное количество размещений", "cumulative_auction_count", "count", "cumsum(auction_count) с января", "monthly layer", ""),
        ("monthly_metrics", "data_quality_flag", "Флаг качества данных", "data_quality_flag", "flag", "сводный флаг monthly layer", "monthly layer", "указывает пустые месяцы, ДРПА, отсутствие спроса/предложения/доходности"),
    ]
    dictionary = pd.DataFrame(
        rows,
        columns=[
            "dataset_name",
            "column_name",
            "description_ru",
            "technical_name",
            "unit",
            "calculation_rule",
            "source_column",
            "limitations",
        ],
    )
    return enrich_dictionary_contract(dictionary)


def enrich_dictionary_contract(dictionary: pd.DataFrame) -> pd.DataFrame:
    """Добавить поля словаря, удобные для BI и semantic layer."""
    result = dictionary.copy()
    if "russian_name" not in result.columns:
        result.insert(2, "russian_name", result["description_ru"])
    if "source_fields" not in result.columns:
        source_index = list(result.columns).index("source_column") + 1
        result.insert(source_index, "source_fields", result["source_column"])
    return result


def build_report(
    params: report_params.ReportParams,
    df: pd.DataFrame,
    exports: Sequence[ExportResult],
) -> str:
    periods = ", ".join(sorted(df["report_period_label"].dropna().astype(str).unique().tolist()))
    target = ", ".join(sorted(df.loc[df["is_target_period"], "report_period_label"].dropna().astype(str).unique().tolist()))
    lines = [
        "# Dashboard exports report",
        "",
        f"Дата формирования: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`.",
        "",
        "## Параметры",
        "",
        f"- `report_date`: `{params.report_date.isoformat()}`",
        f"- `period_type`: `{params.period_type}`",
        f"- `aggregation_mode`: `{params.aggregation_mode}`",
        f"- `retrospective_years`: `{params.retrospective_years}`",
        f"- Периоды: `{periods}`",
        f"- Целевой период: `{target}`",
        f"- Источник: `{config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.relative_to(config.ROOT_DIR).as_posix()}`",
        f"- Строк в source scope после фильтрации: `{len(df)}`",
        "",
        "## Структура сохранения",
        "",
        "- Dashboard-ready файлы сохраняются только в `outputs/dashboards/`.",
        "- Monthly dashboard exports сохраняются в `outputs/dashboards/monthly/`.",
        "- Semantic layer, если он формируется как dashboard export, сохраняется в `outputs/dashboards/semantic_layer/`.",
        "- Dashboard exports не переносятся в `outputs/reports/` и не смешиваются с `outputs/exports/chart_data/`.",
        "",
        "## Созданные exports",
        "",
        "| Dataset | Файл | Строк | Назначение |",
        "|---|---|---:|---|",
    ]
    for item in exports:
        rel_path = item.path.relative_to(config.ROOT_DIR).as_posix()
        lines.append(f"| `{item.dataset_name}` | `{rel_path}` | {item.row_count} | {item.description} |")

    period_summary = build_period_summary(df)
    target_summary = period_summary.loc[period_summary["is_target_period"] == True]
    lines.extend(["", "## Ключевые KPI", ""])
    if not target_summary.empty:
        row = target_summary.iloc[0]
        lines.extend(
            [
                f"- Совокупный спрос: `{format_number(row['total_demand'])}` млн руб.",
                f"- Совокупное предложение: `{format_number(row['total_supply'])}` млн руб.",
                f"- Объем размещения: `{format_number(row['total_placement_volume'])}` млн руб.",
                f"- Bid-to-cover: `{format_number(row['bid_to_cover_ratio'], 3)}`.",
                f"- Спрос / размещение: `{format_number(row['demand_to_placement_ratio'], 3)}`.",
                f"- Средневзвешенная доходность: `{format_number(row['weighted_avg_yield_by_placement'], 2)}`%.",
            ]
        )
    else:
        lines.append("- Целевой период не найден в отфильтрованном scope.")

    lines.extend(
        [
            "",
            "## Использование в BI/dashboard",
            "",
            "- `dashboard_auction_level` использовать как detail fact table.",
            "- `dashboard_period_summary` использовать для временных KPI и trend charts.",
            "- `dashboard_kpi_summary` использовать для KPI cards в long-format.",
            "- `dashboard_maturity_structure` использовать для структуры сроков.",
            "- `dashboard_yield_distribution` использовать для boxplot и yield analytics.",
            "- `dashboard_demand_supply` использовать для demand/supply views с учетом формата.",
            "- `dashboard_monthly_metrics` использовать для помесячных dashboard views и объяснения накопленного итога.",
            "- `dashboard_monthly_data_dictionary` использовать как словарь полей помесячного слоя.",
            "- `dashboard_metadata` использовать для отображения параметров отчета и методологии.",
            "- `dashboard_data_dictionary` использовать как технический слой описания полей.",
            "",
        ]
    )
    return "\n".join(lines)


def build_limitations_report(params: report_params.ReportParams, limitations: Sequence[str]) -> str:
    lines = [
        "# Dashboard exports limitations",
        "",
        f"Дата формирования: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`.",
        "",
        f"Параметры: `{params.period_type}`, `{params.aggregation_mode}`, `{params.report_date.isoformat()}`, ретроспектива `{params.retrospective_years}`.",
        "",
        "## Ограничения",
        "",
    ]
    if limitations:
        for item in sorted(set(limitations)):
            lines.append(f"- {item}")
    else:
        lines.append("- Критических ограничений не выявлено.")
    lines.extend(
        [
            "",
            "## Методологические правила",
            "",
            "- `bid_to_cover_ratio = demand_volume / supply_volume`.",
            "- `demand_to_placement_ratio = demand_volume / placement_volume`.",
            "- `demand_satisfaction_ratio = placement_volume / demand_volume`.",
            "- ДРПА не смешиваются с demand-based ratios без проверки валидности спроса.",
            "- Сроки классифицируются как: краткосрочные до 5 лет включительно; среднесрочные свыше 5 и до 10 лет включительно; долгосрочные более 10 лет.",
            "",
        ]
    )
    return "\n".join(lines)


def format_number(value: Any, digits: int = 1) -> str:
    if value is None or pd.isna(value):
        return ""
    return f"{float(value):,.{digits}f}".replace(",", " ")


def make_suffix(params: report_params.ReportParams) -> str:
    return (
        f"{params.period_type}_{params.aggregation_mode}_{params.report_date.isoformat()}_"
        f"retrospective_{params.retrospective_years}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
