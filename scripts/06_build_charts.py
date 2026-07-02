"""Этап 8: построение графиков для параметризуемой аналитики ОФЗ."""

from __future__ import annotations

import sys
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Sequence

import pandas as pd

px: Any = None
go: Any = None
make_subplots: Any = None
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    pass

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, palette, report_params, scatter_chart_policy, utils
    from scripts.charts.common import (
        format_bln,
        format_hover_number,
        format_metric_value,
        format_number_text,
        format_percent_label,
        format_ru_number,
        format_signed_metric_value,
    )
    from scripts.charts.chart_metadata import chart_data_dir_for_name as chart_data_dir_for_metadata_name
    from scripts.charts.chart_metadata import make_report_suffix
    from scripts.charts.export_utils import ensure_directories, write_chart_artifacts
    from scripts.charts.line_marker_style import (
        REFERENCE_LINE_MARKER_COLORS,
        apply_reference_line_marker_layout,
        apply_reference_line_marker_trace,
        build_collision_safe_value_annotations,
    )
    from scripts.reference_data.cbr_key_rate import (
        build_metadata as build_cbr_key_rate_metadata,
        make_daily_frame as make_cbr_key_rate_daily_frame,
        make_monthly_frame as make_cbr_key_rate_monthly_frame,
        read_xlsx_key_rate,
        write_outputs as write_cbr_key_rate_outputs,
    )
else:
    from . import config, palette, report_params, scatter_chart_policy, utils
    from .charts.common import (
        format_bln,
        format_hover_number,
        format_metric_value,
        format_number_text,
        format_percent_label,
        format_ru_number,
        format_signed_metric_value,
    )
    from .charts.chart_metadata import chart_data_dir_for_name as chart_data_dir_for_metadata_name
    from .charts.chart_metadata import make_report_suffix
    from .charts.export_utils import ensure_directories, write_chart_artifacts
    from .charts.line_marker_style import (
        REFERENCE_LINE_MARKER_COLORS,
        apply_reference_line_marker_layout,
        apply_reference_line_marker_trace,
        build_collision_safe_value_annotations,
    )
    from .reference_data.cbr_key_rate import (
        build_metadata as build_cbr_key_rate_metadata,
        make_daily_frame as make_cbr_key_rate_daily_frame,
        make_monthly_frame as make_cbr_key_rate_monthly_frame,
        read_xlsx_key_rate,
        write_outputs as write_cbr_key_rate_outputs,
    )


ChartBuilder = Callable[[pd.DataFrame, report_params.ReportParams, list[str]], "ChartResult | None"]
MAX_SCATTER_LABELS = scatter_chart_policy.MAX_SCATTER_LABELS
MAX_YIELD_DISCOUNT_FACET_LABELS_PER_FACET = 3
MAX_YIELD_DISCOUNT_FACET_LABELS_TOTAL = 15
MAX_YIELD_DISCOUNT_MAIN_LABELS_TOTAL = 25
MAX_YIELD_DISCOUNT_OUTLIERS_LABELS_TOTAL = 30
YIELD_DISCOUNT_LABEL_MIN_DISTANCE_NORM = 0.07
MIN_SEGMENT_LABEL_SHARE = 0.02
MIN_SEGMENT_LABEL_VALUE_BLN = 20.0
RU_MONTH_ABBR = {
    1: "Янв",
    2: "Фев",
    3: "Мар",
    4: "Апр",
    5: "Май",
    6: "Июн",
    7: "Июл",
    8: "Авг",
    9: "Сен",
    10: "Окт",
    11: "Ноя",
    12: "Дек",
}

QUALITATIVE_COLORS = palette.QUALITATIVE_PALETTE
SEQUENTIAL_COLORS = palette.SEQUENTIAL_PALETTE
CONTRAST_SEQUENTIAL_COLORS = palette.CONTRAST_SEQUENTIAL_PALETTE
BINARY_COLORS = palette.BINARY_PALETTE
HIGHLIGHT_COLORS = {
    "stable": palette.STATUS_PALETTE["норма"],
    "warning": palette.STATUS_PALETTE["предупреждение"],
    "risk": palette.STATUS_PALETTE["риск"],
}
MATURITY_COLOR_MAP = palette.MATURITY_COLOR_MAP
FORMAT_COLOR_MAP = palette.FORMAT_COLOR_MAP
DIMENSION_COLOR_MAP = palette.DIMENSION_COLOR_MAP
MATURITY_CATEGORY_ORDER = palette.MATURITY_CATEGORY_ORDER
STRUCTURE_COLORS = palette.STRUCTURE_PALETTE
FORMAT_DISCOUNT_COMPONENT_COLORS = {
    "Аукцион — выручка": "#06245A",
    "Аукцион — дисконтный разрыв": "#3F5F9F",
    "ДРПА — выручка": "#2FA7D6",
    "ДРПА — дисконтный разрыв": "#8DD6EA",
}
METRIC_LABELS = {
    "_placement": "Объем размещения по номиналу",
    "_demand": "Спрос",
    "_supply": "Предложение",
    "_yield": "Доходность",
    "_bid_to_cover": "Bid-to-cover",
    "_demand_to_placement": "Спрос к размещению",
    "_discount_to_nominal": "Дисконт к номиналу",
    "_cutoff_yield": "Доходность отсечения",
    "total_demand": "Совокупный спрос",
    "total_supply": "Совокупное предложение",
    "yield_weighted_avg": "Средневзвешенная доходность",
}


@dataclass(frozen=True)
class ChartResult:
    name: str
    figure: Any
    export_data: pd.DataFrame
    html_path: Path
    csv_path: Path


def main(argv: Sequence[str] | None = None) -> int:
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт Этапа 8: построение графиков")

    params = report_params.parse_report_args(argv)
    limitations: list[str] = []

    if not plotly_available():
        limitations.append("Библиотека Plotly недоступна; графики не построены.")
        write_limitations(params, limitations)
        logger.warning("Plotly недоступен, Этап 8 завершен с ограничениями")
        return 0

    scope = read_report_scope()
    scope = filter_scope(scope, params)
    if scope.empty:
        limitations.append("После фильтрации по параметрам отчета report scope пуст; графики не построены.")
        write_limitations(params, limitations, results=[])
        logger.warning("Report scope пуст после фильтрации, Этап 8 завершен с ограничениями")
        return 0
    prepared = prepare_scope(scope, limitations)

    ensure_directories(
        config.CHARTS_DIR,
        config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR,
        config.EXPORTS_CHART_DATA_SANKEY_DIR,
        config.EXPORTS_CHART_DATA_BOXPLOT_DIR,
        config.EXPORTS_CHART_DATA_STRUCTURE_DIR,
        config.EXPORTS_CHART_DATA_YIELD_DIR,
        config.EXPORTS_TECHNICAL_REVIEW_REQUIRED_DIR,
    )

    results: list[ChartResult] = []
    for builder in chart_builders():
        try:
            result = builder(prepared, params, limitations)
        except Exception as error:
            builder_name = getattr(builder, "__name__", "unknown_builder")
            message = f"График `{builder_name}` не построен из-за ошибки: {error}"
            limitations.append(message)
            logger.exception(message)
            continue
        if result is None:
            continue
        write_chart_artifacts(
            result.figure,
            result.export_data,
            result.html_path,
            result.csv_path,
            csv_encoding="utf-8",
        )
        results.append(result)
        logger.info("График сохранен: %s", result.html_path)

    write_limitations(params, limitations, results)
    logger.info("Построено графиков: %s", len(results))
    logger.info("Этап 8 завершен")
    return 0


def plotly_available() -> bool:
    return px is not None and go is not None and make_subplots is not None


def read_report_scope() -> pd.DataFrame:
    if not config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.exists():
        raise FileNotFoundError(
            f"Report scope dataset не найден: {config.OFZ_AUCTIONS_REPORT_SCOPE_CSV}. "
            "Сначала выполните Этап 4."
        )
    return pd.read_csv(config.OFZ_AUCTIONS_REPORT_SCOPE_CSV)


def filter_scope(
    scope: pd.DataFrame,
    params: report_params.ReportParams,
) -> pd.DataFrame:
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


def prepare_scope(scope: pd.DataFrame, limitations: list[str]) -> pd.DataFrame:
    df = scope.copy()
    df["_placement"] = resolve_numeric(df, ["placement_volume", "placement_amount_mln_rub"], "объем размещения", limitations)
    df["placement_volume_bln"] = df["_placement"] / 1000.0
    df["placement_volume_unit"] = "млн рублей"
    df["_demand"] = resolve_numeric(df, ["demand_volume", "demand_amount_mln_rub"], "спрос", limitations)
    df["_supply"] = resolve_numeric(df, ["supply_volume", "offer_amount_mln_rub"], "предложение", limitations)
    df["_yield"] = resolve_numeric(df, ["yield", "weighted_avg_yield", "weighted_avg_yield_pct"], "доходность", limitations)
    df["_bid_to_cover"] = safe_divide_series(df["_demand"], df["_supply"])
    df["_demand_to_placement"] = safe_divide_series(df["_demand"], df["_placement"])
    df["_demand_satisfaction"] = resolve_numeric(df, ["demand_satisfaction_ratio"], "коэффициент удовлетворения спроса", limitations)
    df["_cutoff_price"] = resolve_numeric(df, ["cutoff_price", "cutoff_price_pct"], "цена отсечения", limitations)
    df["_weighted_avg_price"] = resolve_numeric(df, ["weighted_avg_price", "weighted_avg_price_pct"], "средневзвешенная цена", limitations)
    df["_cutoff_yield"] = resolve_numeric(df, ["cutoff_yield", "cutoff_yield_pct"], "доходность отсечения", limitations)
    df["_weighted_avg_yield"] = resolve_numeric(df, ["weighted_avg_yield", "weighted_avg_yield_pct", "yield"], "средневзвешенная доходность", limitations)
    df["_discount_to_nominal"] = resolve_numeric(df, ["discount_to_nominal"], "дисконт к номиналу", limitations)
    if df["_discount_to_nominal"].isna().all() and df["_cutoff_price"].notna().any():
        df["_discount_to_nominal"] = 100 - df["_cutoff_price"]
    df["_cutoff_yield_spread"] = resolve_numeric(df, ["cutoff_yield_spread"], "спред доходности отсечения", limitations)
    if df["_cutoff_yield_spread"].isna().all() and df["_cutoff_yield"].notna().any() and df["_weighted_avg_yield"].notna().any():
        df["_cutoff_yield_spread"] = df["_cutoff_yield"] - df["_weighted_avg_yield"]
    if "ratio_basis" not in df.columns:
        df["ratio_basis"] = "bid_to_cover=demand/supply; demand_to_placement=demand/placement"

    if "maturity_bucket_label" not in df.columns and "maturity_bucket" in df.columns:
        df["maturity_bucket_label"] = df["maturity_bucket"].map(
            {
                "short_term": "Краткосрочные",
                "medium_term": "Среднесрочные",
                "long_term": "Долгосрочные",
                "requires_review": "Требует проверки",
            }
        )
    elif "maturity_bucket_label" in df.columns:
        df["maturity_bucket_label"] = df["maturity_bucket_label"].replace(
            {
                "short_term": "Краткосрочные",
                "medium_term": "Среднесрочные",
                "long_term": "Долгосрочные",
                "requires_review": "Требует проверки",
            }
        )
    return df


def safe_divide_series(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    denominator_numeric = pd.to_numeric(denominator, errors="coerce")
    numerator_numeric = pd.to_numeric(numerator, errors="coerce")
    return numerator_numeric / denominator_numeric.mask(denominator_numeric == 0)


def is_missing_value(value: object) -> bool:
    """Return True for scalar missing values without confusing static checkers."""
    if value is None:
        return True
    try:
        missing = pd.Series([value]).isna().iloc[0]
    except (TypeError, ValueError):
        return False
    return bool(missing)


def to_optional_float(value: object) -> float | None:
    """Convert a scalar-like value to float, returning None for missing/non-numeric values."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if is_missing_value(numeric):
        return None
    return float(numeric)


def get_bool_series(data: pd.DataFrame, column: str, default: bool = True) -> pd.Series:
    """Return a boolean Series for optional DataFrame flags."""
    if column not in data.columns:
        return pd.Series(default, index=data.index, dtype=bool)
    return data[column].fillna(default).astype(bool)


def resolve_numeric(
    df: pd.DataFrame,
    candidates: list[str],
    metric_name: str,
    limitations: list[str],
) -> pd.Series:
    for column in candidates:
        if column in df.columns:
            return pd.to_numeric(df[column], errors="coerce")
    limitations.append(f"Не найдено поле `{metric_name}`; связанные графики могут быть пропущены.")
    return pd.Series(pd.NA, index=df.index, dtype="Float64")


def chart_builders() -> list[ChartBuilder]:
    return [
        build_placement_volume_chart,
        build_demand_supply_chart,
        build_bid_to_cover_chart,
        build_yield_by_type_chart,
        build_ofz_pd_yield_key_rate_chart,
        build_maturity_structure_chart,
        build_format_structure_chart,
        build_format_discount_chart,
        build_format_terms_comparison_chart,
        build_format_terms_delta_by_format_chart,
        build_risk_quadrant_chart,
        build_retrospective_risk_quadrant_chart,
        build_report_year_demand_to_placement_risk_chart,
        build_yield_boxplot_by_ofz_type_chart,
        build_yield_boxplot_ofz_pd_chart,
        build_demand_cutoff_explanation_chart,
        build_yield_vs_demand_chart,
        build_discount_vs_demand_chart,
        build_discount_vs_demand_outliers_chart,
        build_discount_vs_demand_logx_chart,
        build_yield_vs_discount_chart,
        build_yield_vs_discount_outliers_chart,
        build_yield_vs_discount_facet_chart,
        build_format_terms_aggregate_scatter_chart,
        build_format_terms_scatter_chart,
        build_risk_quadrant_retrospective_outliers_chart,
        build_risk_quadrant_retrospective_logx_chart,
        build_risk_quadrant_retrospective_facet_chart,
        build_sankey_chart,
        build_sankey_period_maturity_type_format_chart,
        build_sankey_period_format_type_maturity_chart,
        build_sankey_period_format_maturity_type_chart,
        build_sankey_target_period_chart,
    ]


def apply_common_layout(figure: Any, legend_title: str | None = None) -> None:
    figure.update_layout(
        template="plotly_white",
        font={"family": "Arial, sans-serif", "color": "#1F2933"},
        colorway=QUALITATIVE_COLORS,
        legend_title_text=legend_title,
        separators=", ",
        margin={"l": 72, "r": 32, "t": 72, "b": 64},
        uniformtext_minsize=10,
        uniformtext_mode="hide",
    )


def apply_reference_style_to_line_marker_figure(
    figure: Any,
    title: str | None = None,
    show_yaxis_labels: bool = True,
) -> None:
    """Apply the shared reference styling to existing line+marker figures."""
    for index, trace in enumerate(figure.data):
        mode = str(getattr(trace, "mode", "") or "")
        if "lines" not in mode:
            continue
        line = getattr(trace, "line", None)
        color = getattr(line, "color", None) or QUALITATIVE_COLORS[index % len(QUALITATIVE_COLORS)]
        text_position = getattr(trace, "textposition", None) or "top center"
        apply_reference_line_marker_trace(trace, color, text_position=text_position)
    apply_reference_line_marker_layout(figure, title=title, show_yaxis_labels=show_yaxis_labels)


def volume_to_bln(value: Any) -> Any:
    """Перевести объем из млн рублей в млрд рублей для визуализаций."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return pd.NA
    return float(numeric) / 1000.0

def add_placement_bln_columns(data: pd.DataFrame, source_column: str = "_placement") -> pd.DataFrame:
    """Добавить display-колонки объема размещения без изменения исходных млн рублей."""
    result = data.copy()
    result["placement_volume"] = pd.to_numeric(result[source_column], errors="coerce")
    result["placement_volume_bln"] = result["placement_volume"] / 1000.0
    result["placement_volume_unit"] = "млн рублей"
    return result


def add_stacked_structure_metrics(
    data: pd.DataFrame,
    x_column: str,
    category_column: str,
    min_segment_label_share: float = MIN_SEGMENT_LABEL_SHARE,
    min_segment_label_value_bln: float = MIN_SEGMENT_LABEL_VALUE_BLN,
    always_label_categories: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Добавить totals и доли для stacked structure charts."""
    result = data.copy()
    result["column_total"] = result.groupby(x_column)["placement_volume_bln"].transform("sum")
    grand_total = pd.to_numeric(result["placement_volume_bln"], errors="coerce").sum()
    result["segment_share_in_column"] = result["placement_volume_bln"] / result["column_total"]
    result["segment_share_total"] = result["placement_volume_bln"] / grand_total if grand_total else pd.NA
    label_categories = [item.lower() for item in (always_label_categories or [])]
    category_text = result[category_column].fillna("").astype(str).str.lower()
    always_visible = category_text.map(lambda value: any(item in str(value) for item in label_categories))
    values = pd.to_numeric(result["placement_volume_bln"], errors="coerce")
    shares = pd.to_numeric(result["segment_share_in_column"], errors="coerce")
    result["label_visible"] = (
        values.gt(0)
        & (
            shares.ge(min_segment_label_share)
            | values.ge(min_segment_label_value_bln)
            | always_visible
        )
    )
    result["label_reason"] = ""
    result.loc[shares.ge(min_segment_label_share), "label_reason"] = "segment_share_threshold"
    result.loc[values.ge(min_segment_label_value_bln), "label_reason"] = result.loc[
        values.ge(min_segment_label_value_bln), "label_reason"
    ].map(lambda value: "; ".join(part for part in [value, "segment_value_threshold"] if part))
    result.loc[always_visible, "label_reason"] = result.loc[always_visible, "label_reason"].map(
        lambda value: "; ".join(part for part in [value, "format_comparison_required"] if part)
    )
    result.loc[~result["label_visible"], "label_reason"] = "small_segment_hover_only"
    result["label_position"] = "inside"
    result.loc[result["label_visible"] & shares.lt(0.08), "label_position"] = "outside"
    result.loc[result["label_visible"] & always_visible, "label_position"] = "inside_bottom"
    result.loc[~result["label_visible"], "label_position"] = "hidden"
    result["label_display"] = values.map(lambda value: format_bln(value, suffix=False))
    result.loc[~result["label_visible"], "label_display"] = ""
    result["Подпись"] = result["label_display"]
    result["Объем, млрд руб."] = result["placement_volume_bln"].map(lambda value: format_bln(value, suffix=False))
    result["Объем, млн руб."] = result["placement_volume"].map(lambda value: format_hover_number(value, 1))
    result["Доля в столбце, %"] = result["segment_share_in_column"].map(lambda value: format_percent_label(value))
    result["Доля в общей сумме, %"] = result["segment_share_total"].map(lambda value: format_percent_label(value))
    result["Итого по столбцу"] = result["column_total"].map(lambda value: format_bln(value, suffix=False))
    result["total_placement_volume_bln"] = result["column_total"]
    result["format_share_pct"] = result["segment_share_in_column"] * 100.0
    result["Сегмент"] = result[category_column].astype("string")
    return result

def combine_quality_flags(values: pd.Series) -> str:
    """Свернуть флаги качества данных в короткий список уникальных значений."""
    flags = [
        str(value).strip()
        for value in values.dropna().tolist()
        if str(value).strip() and str(value).strip().lower() != "nan"
    ]
    return "; ".join(dict.fromkeys(flags))


def data_quality_display(value: Any) -> str:
    """Перевести технические флаги качества данных в человекочитаемое описание."""
    raw = "" if pd.isna(value) else str(value).strip()
    if not raw:
        return "без явных ограничений"
    mapping = {
        "missing_demand": "нет данных о спросе",
        "source_markers": "требуется проверка признаков источника",
        "demand_amount_mln_rub": "требуется проверка спроса",
        "demand_satisfaction_ratio": "требуется проверка коэффициента удовлетворения спроса",
        "missing_discount_to_nominal": "нет данных для расчета дисконта",
        "zero_yield_check": "требуется проверка нулевой доходности",
        "missing_yield": "нет данных о доходности",
        "no_drpa": "ДРПА отсутствует в периоде",
        "no_auction": "аукцион отсутствует в периоде",
        "auction_metric_missing": "не хватает метрики по аукциону",
        "drpa_metric_missing": "не хватает метрики по ДРПА",
        "delta_not_calculated": "дельта не рассчитана",
    }
    parts: list[str] = []
    for token in raw.replace("|", ";").split(";"):
        normalized = token.strip()
        if not normalized or normalized.lower() == "ok":
            continue
        lower = normalized.lower()
        if lower.startswith("source markers") or lower.startswith("source_markers"):
            parts.append("требуется проверка признаков источника")
        elif lower in {
            "cutoff price pct",
            "cutoff_price_pct",
            "weighted avg price pct",
            "weighted_avg_price_pct",
            "cutoff yield pct",
            "cutoff_yield_pct",
            "weighted avg yield pct",
            "weighted_avg_yield_pct",
            "demand amount mln rub",
            "demand_amount_mln_rub",
        }:
            parts.append("требуется проверка признаков источника")
        elif lower in {"failed or no deal", "failed_or_no_deal"}:
            parts.append("несостоявшийся или ограниченный аукцион")
        elif lower in {"requires_review", "review_required"}:
            parts.append("требуется ручная проверка")
        else:
            parts.append(mapping.get(normalized, normalized.replace("_", " ")))
    return "; ".join(dict.fromkeys(parts)) if parts else "без явных ограничений"


def data_quality_display_short(value: Any) -> str:
    """Сжать описание качества данных для компактного hover."""
    full = data_quality_display(value)
    if full == "без явных ограничений":
        return full
    lowered = full.lower()
    groups: list[str] = []
    if "доходност" in lowered:
        groups.append("доходность")
    if "спрос" in lowered:
        groups.append("спрос")
    if "дисконт" in lowered:
        groups.append("дисконт")
    if "источник" in lowered or "признак" in lowered:
        groups.append("признаки источника")
    if "дрпа отсутствует" in lowered or "аукцион отсутствует" in lowered:
        return full
    if groups:
        return "Есть ограничения по данным: " + ", ".join(dict.fromkeys(groups))
    return full


def discount_calc_method_display(value: Any) -> str:
    """Перевести метод расчета дисконта в пользовательскую формулировку."""
    raw = "" if pd.isna(value) else str(value).strip().lower()
    if "discount_to_nominal" in raw:
        return "дисконт рассчитан по готовому полю discount_to_nominal"
    if "cutoff" in raw or "100 - cutoff" in raw:
        return "дисконт рассчитан по цене отсечения"
    if not raw:
        return "нет данных для расчета дисконта"
    return str(value)


def add_stacked_total_labels(
    figure: Any,
    data: pd.DataFrame,
    x_column: str,
    total_column: str = "column_total",
) -> None:
    """Добавить итоговую сумму над stacked-столбцом."""
    assert go is not None
    segment_counts = data.groupby(x_column)["Сегмент"].nunique()
    totals = data[[x_column, total_column]].drop_duplicates().copy()
    totals = totals.loc[totals[x_column].map(segment_counts).fillna(0).astype(int) >= 2]
    if totals.empty:
        return
    totals["Итого подпись"] = totals[total_column].map(lambda value: format_bln(value, suffix=False))
    figure.add_trace(
        go.Scatter(
            x=totals[x_column],
            y=totals[total_column],
            text=totals["Итого подпись"],
            mode="text",
            textposition="top center",
            textfont={"size": 11, "color": "#1F2933"},
            hoverinfo="skip",
            showlegend=False,
            name="Итого",
        )
    )


def add_format_discount_total_labels(
    figure: Any,
    data: pd.DataFrame,
    x_column: str,
    total_column: str = "column_total",
) -> None:
    """Добавить отдельные итоговые подписи над format_discount stacked bars."""
    assert go is not None
    if not {x_column, total_column, "total_label_display"}.issubset(data.columns):
        add_stacked_total_labels(figure, data, x_column, total_column)
        return
    segment_counts = data.groupby(x_column)["Сегмент"].nunique()
    total_columns = [x_column, total_column, "total_label_display", "total_label_visible"]
    if "total_label_y" in data.columns:
        total_columns.append("total_label_y")
    totals = data[total_columns].drop_duplicates().copy()
    totals = totals.loc[
        totals[x_column].map(segment_counts).fillna(0).astype(int).ge(2)
        & totals["total_label_visible"].astype(bool)
    ]
    if totals.empty:
        return
    y_column = "total_label_y" if "total_label_y" in totals.columns else total_column
    figure.add_trace(
        go.Scatter(
            x=totals[x_column],
            y=totals[y_column],
            text=totals["total_label_display"],
            mode="text",
            textposition="top center",
            textfont={"size": 11, "color": "#1F2933"},
            hoverinfo="skip",
            showlegend=False,
            name="Итого",
        )
    )


def add_format_bottom_segment_labels(
    figure: Any,
    data: pd.DataFrame,
    x_column: str,
    category_column: str = "format",
) -> None:
    """Разместить подписи ДРПА у нижней границы сегмента, отдельно от total label."""
    assert go is not None
    required = {x_column, category_column, "placement_volume_bln", "label_display"}
    if not required.issubset(data.columns):
        return
    work = data.copy()
    work["_format_order"] = work[category_column].astype(str).map(format_stack_order)
    work = work.sort_values([x_column, "_format_order"]).copy()
    if "segment_base_y" not in work.columns or "segment_height" not in work.columns:
        work["segment_base_y"] = work.groupby(x_column)["placement_volume_bln"].cumsum() - work["placement_volume_bln"]
        work["segment_height"] = work["placement_volume_bln"]
    work["segment_label_y"] = work["segment_base_y"] + (work["segment_height"] * 0.28)
    mask = (
        work[category_column].fillna("").astype(str).str.lower().str.contains("дрпа|drpa", regex=True)
        & work["label_display"].fillna("").astype(str).str.strip().ne("")
    )
    labels = work.loc[mask].copy()
    if labels.empty:
        return
    for trace in figure.data:
        trace_name = str(getattr(trace, "name", "")).strip().lower()
        if "дрпа" in trace_name or "drpa" in trace_name:
            trace.update(text=["" for _ in getattr(trace, "x", [])])
    figure.add_trace(
        go.Scatter(
            x=labels[x_column],
            y=labels["segment_label_y"],
            text=labels["label_display"],
            mode="text",
            textposition="middle center",
            textfont={"size": 10, "color": "#1F2933"},
            hoverinfo="skip",
            showlegend=False,
            name="Подпись ДРПА",
        )
    )


def add_format_discount_badges(
    figure: Any,
    data: pd.DataFrame,
    x_column: str,
    category_column: str = "format",
) -> None:
    """Добавить annotation-бейджи дисконта внутри соответствующих stacked-сегментов."""
    required = {
        x_column,
        category_column,
        "discount_bar_visible",
        "discount_bar_norm",
        "segment_mid_y",
        "segment_label_position",
        "segment_discount_label",
    }
    if not required.issubset(data.columns):
        return
    work = data.loc[data["discount_bar_visible"].astype(bool)].copy()
    if work.empty:
        return
    for _, row in work.iterrows():
        discount_label = str(row.get("segment_discount_label", "")).strip()
        if not discount_label or discount_label == "н.д.":
            continue
        norm = pd.to_numeric(pd.Series([row.get("discount_bar_norm")]), errors="coerce").iloc[0]
        if pd.isna(norm):
            continue
        blocks_count = max(1, min(6, int(round(float(norm) * 6))))
        marker = "▰" * blocks_count
        is_drpa = "дрпа" in str(row.get(category_column, "")).lower() or "drpa" in str(row.get(category_column, "")).lower()
        xshift = 42 if is_drpa else -34
        yshift = 0 if is_drpa else -8
        showarrow = bool(is_drpa)
        text_color = "#111827" if is_drpa else "#F9FAFB"
        bgcolor = "rgba(255,255,255,0.78)" if is_drpa else "rgba(31,41,55,0.68)"
        bordercolor = "rgba(31,41,55,0.35)"
        figure.add_annotation(
            x=row[x_column],
            y=row["segment_mid_y"],
            text=f"{marker} {discount_label}",
            showarrow=showarrow,
            arrowhead=2,
            arrowsize=0.6,
            arrowwidth=1,
            arrowcolor="#64748B",
            ax=28 if is_drpa else 0,
            ay=0,
            xshift=xshift,
            yshift=yshift,
            font={"size": 9, "color": text_color},
            bgcolor=bgcolor,
            bordercolor=bordercolor,
            borderwidth=1,
            borderpad=2,
            name="Мини-индикатор дисконта",
        )


def format_stack_order(value: object) -> int:
    """Вернуть порядок форматов в stacked bar: аукцион ниже, ДРПА выше."""
    text = "" if is_missing_value(value) else str(value).strip().lower()
    if "аукцион" in text or "auction" in text:
        return 1
    if "дрпа" in text or "drpa" in text:
        return 2
    return 99


def apply_bln_yaxis(figure: Any, title: str = "Объем размещения по номиналу, млрд рублей") -> None:
    """Отключить технические suffix M/B/k и закрепить человекочитаемую ось объема."""
    figure.update_yaxes(
        title_text=title,
        tickformat=",.0f",
        separatethousands=True,
        exponentformat="none",
        showexponent="none",
    )


def label_for_metric(metric: object) -> str:
    return METRIC_LABELS.get(str(metric), str(metric))


def select_ratio_column(df: pd.DataFrame, limitations: list[str]) -> tuple[str | None, str, str]:
    if "_bid_to_cover" in df.columns and df["_bid_to_cover"].notna().any():
        return "_bid_to_cover", "bid-to-cover", "Bid-to-cover (спрос / предложение)"
    if "_demand_to_placement" in df.columns and df["_demand_to_placement"].notna().any():
        limitations.append(
            "Для ratio-графика использован `demand_to_placement_ratio`, поэтому показатель не называется bid-to-cover."
        )
        return "_demand_to_placement", "отношение спроса к размещению", "Спрос / размещение"
    return None, "", ""


def select_demand_to_placement_ratio(df: pd.DataFrame, limitations: list[str]) -> tuple[str | None, str, str]:
    if "_demand_to_placement" in df.columns and df["_demand_to_placement"].notna().any():
        return "_demand_to_placement", "кратность спроса к размещению", "Спрос / объем размещения"
    limitations.append(
        "`demand_to_placement_ratio` недоступен: нет спроса или положительного объема размещения."
    )
    return None, "", ""


def filter_bid_to_cover_rows(df: pd.DataFrame, limitations: list[str]) -> pd.DataFrame:
    data = df.copy()
    before = len(data)
    data = data.dropna(subset=["_demand", "_supply"]).copy()
    data = data.loc[data["_supply"] > 0].copy()
    if "format" in data.columns:
        format_values = data["format"].astype("string").str.strip().str.lower()
        data = data.loc[format_values.eq("аукцион") | format_values.eq("auction")].copy()
    else:
        limitations.append("Для bid-to-cover отсутствует колонка `format`; фильтр формата аукциона не применен.")
    if "data_quality_flag" in data.columns:
        quality = data["data_quality_flag"].astype("string").str.lower()
        data = data.loc[~quality.str.contains("requires_review", na=False)].copy()
    data["_bid_to_cover"] = safe_divide_series(data["_demand"], data["_supply"])
    removed = before - len(data)
    if removed:
        limitations.append(
            f"Из расчета bid-to-cover исключено строк: {removed} "
            "(неаукционные форматы, отсутствующий спрос/предложение, нулевое предложение или requires_review)."
        )
    return data


def write_bid_to_cover_outliers(data: pd.DataFrame) -> None:
    columns = [
        "auction_date",
        "report_period_label",
        "issue_code",
        "format",
        "_demand",
        "_supply",
        "_placement",
        "_bid_to_cover",
        "source_file",
        "data_quality_flag",
    ]
    output_columns = [
        "auction_date",
        "report_period_label",
        "issue_code",
        "format",
        "demand_volume",
        "supply_volume",
        "placement_volume",
        "bid_to_cover_ratio",
        "source_file",
        "data_quality_flag",
    ]
    report = data.loc[data["_bid_to_cover"] > 5, [column for column in columns if column in data.columns]].copy()
    rename_map = {
        "_demand": "demand_volume",
        "_supply": "supply_volume",
        "_placement": "placement_volume",
        "_bid_to_cover": "bid_to_cover_ratio",
    }
    report = report.rename(columns=rename_map)
    for column in output_columns:
        if column not in report.columns:
            report[column] = pd.NA
    report = report[output_columns].sort_values("bid_to_cover_ratio", ascending=False)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Выбросы bid-to-cover",
        "",
        f"Дата формирования: `{now}`.",
        "",
        "Отчет содержит строки, где `bid_to_cover_ratio = demand_volume / supply_volume` больше 5.",
        "Порог `> 10` является критическим подмножеством этого отчета.",
        "",
        f"- Строк `bid_to_cover_ratio > 5`: `{int((report['bid_to_cover_ratio'] > 5).sum()) if not report.empty else 0}`",
        f"- Строк `bid_to_cover_ratio > 10`: `{int((report['bid_to_cover_ratio'] > 10).sum()) if not report.empty else 0}`",
        "",
    ]
    if report.empty:
        lines.append("Выбросы не найдены.")
    else:
        lines.append(markdown_table(report))
    lines.append("")
    utils.write_markdown(config.get_doc_path("bid_to_cover_outliers.md"), "\n".join(lines))


def build_placement_volume_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = ["report_period_label", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"График объема размещения пропущен: нет {', '.join(missing)}.")
        return None
    data = df.groupby("report_period_label", dropna=False).agg(
        _placement=("_placement", "sum"),
        auction_count=("_placement", "size"),
    ).reset_index()
    data = add_placement_bln_columns(data)
    data["Подпись"] = data["placement_volume_bln"].map(lambda value: format_bln(value, suffix=False))
    data["Объем, млрд руб."] = data["placement_volume_bln"].map(lambda value: format_bln(value, suffix=False))
    data["Объем, млн руб."] = data["placement_volume"].map(lambda value: format_hover_number(value, 1))
    assert px is not None
    fig = px.bar(
        data,
        x="report_period_label",
        y="placement_volume_bln",
        text="Подпись",
        title="Объем размещения ОФЗ по номиналу",
        color_discrete_sequence=[QUALITATIVE_COLORS[0]],
        labels={
            "report_period_label": "Период",
            "placement_volume_bln": "Объем размещения по номиналу, млрд рублей",
        },
        custom_data=["Объем, млрд руб.", "Объем, млн руб.", "auction_count"],
    )
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "Период: %{x}<br>"
            "Объем размещения по номиналу, млрд рублей: %{customdata[0]}<br>"
            "Объем размещения по номиналу, млн рублей: %{customdata[1]}<br>"
            "Количество размещений: %{customdata[2]}<extra></extra>"
        ),
    )
    fig.add_annotation(
        text="Показан объем размещения по номиналу, млрд рублей",
        xref="paper",
        yref="paper",
        x=0,
        y=1.10,
        showarrow=False,
        align="left",
        font={"size": 12, "color": "#1F2933"},
    )
    apply_common_layout(fig)
    apply_bln_yaxis(fig)
    fig.update_layout(xaxis_title="Период", margin={"l": 72, "r": 32, "t": 110, "b": 64})
    return make_result("placement_volume", fig, data, params)


def build_demand_supply_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = ["report_period_label", "_demand", "_supply"]
    if missing := missing_columns(df, required):
        limitations.append(f"График спроса и предложения пропущен: нет {', '.join(missing)}.")
        return None
    data = (
        df.groupby("report_period_label", dropna=False)
        .agg(total_demand=("_demand", "sum"), total_supply=("_supply", "sum"))
        .reset_index()
    )
    melted = data.melt("report_period_label", var_name="metric", value_name="value")
    melted["Показатель"] = melted["metric"].map(label_for_metric)
    melted["Подпись"] = format_number_text(melted["value"])
    assert px is not None
    fig = px.bar(
        melted,
        x="report_period_label",
        y="value",
        color="Показатель",
        text="Подпись",
        barmode="group",
        title="Спрос и предложение",
        color_discrete_sequence=BINARY_COLORS,
        labels={"report_period_label": "Период", "value": "Объем", "Показатель": "Показатель"},
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(xaxis_title="Период", yaxis_title="Объем")
    apply_common_layout(fig, legend_title="Показатель")
    return make_result("demand_supply", fig, data, params)


def build_bid_to_cover_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = ["report_period_label", "_demand", "_supply"]
    if missing := missing_columns(df, required):
        limitations.append(f"График покрытия предложения спросом пропущен: нет {', '.join(missing)}.")
        return None
    eligible = filter_bid_to_cover_rows(df, limitations)
    write_bid_to_cover_outliers(eligible)
    if eligible.empty:
        limitations.append("График покрытия предложения спросом пропущен: нет строк после фильтра demand-based анализа.")
        return None
    data = (
        eligible.groupby("report_period_label", dropna=False)
        .agg(
            total_demand=("_demand", "sum"),
            total_supply=("_supply", "sum"),
            auction_count=("report_period_label", "size"),
            row_bid_to_cover_mean=("_bid_to_cover", "mean"),
            row_bid_to_cover_median=("_bid_to_cover", "median"),
        )
        .reset_index()
    )
    data["bid_to_cover_period"] = safe_divide_series(data["total_demand"], data["total_supply"])
    data["Метод расчета"] = "Совокупный спрос / совокупное предложение"
    data["Подпись"] = format_number_text(data["bid_to_cover_period"], digits=2)
    data["Совокупный спрос"] = data["total_demand"].map(lambda value: format_hover_number(value, 1))
    data["Совокупное предложение"] = data["total_supply"].map(lambda value: format_hover_number(value, 1))
    data["Bid-to-cover"] = data["bid_to_cover_period"].map(lambda value: format_hover_number(value, 3))
    assert px is not None
    fig = px.line(
        data,
        x="report_period_label",
        y="bid_to_cover_period",
        markers=True,
        text="Подпись",
        title="Покрытие предложения спросом",
        color_discrete_sequence=[QUALITATIVE_COLORS[1]],
        custom_data=[
            "report_period_label",
            "Совокупный спрос",
            "Совокупное предложение",
            "auction_count",
            "Bid-to-cover",
            "Метод расчета",
            "row_bid_to_cover_mean",
            "row_bid_to_cover_median",
        ],
        labels={"report_period_label": "Период", "bid_to_cover_period": "Спрос / предложение"},
    )
    fig.update_traces(
        textposition="top center",
        hovertemplate=(
            "Период: %{customdata[0]}<br>"
            "Совокупный спрос: %{customdata[1]}<br>"
            "Совокупное предложение: %{customdata[2]}<br>"
            "Количество аукционов: %{customdata[3]}<br>"
            "Bid-to-cover: %{customdata[4]}<br>"
            "Метод расчета: %{customdata[5]}<br>"
            "Среднее строковых ratio: %{customdata[6]:.3f}<br>"
            "Медиана строковых ratio: %{customdata[7]:.3f}"
            "<extra></extra>"
        ),
    )
    fig.add_hline(
        y=1,
        line_dash="dash",
        line_color=HIGHLIGHT_COLORS["risk"],
        annotation_text="Спрос = предложение",
        annotation_position="top right",
    )
    fig.add_annotation(
        text="Расчет: совокупный спрос / совокупное предложение",
        xref="paper",
        yref="paper",
        x=0,
        y=1.12,
        showarrow=False,
        align="left",
        font={"size": 12, "color": "#1F2933"},
    )
    apply_common_layout(fig)
    apply_reference_style_to_line_marker_figure(
        fig,
        title="Покрытие предложения спросом",
        show_yaxis_labels=True,
    )
    fig.update_layout(xaxis_title="Период", yaxis_title="Спрос / предложение", margin={"l": 72, "r": 32, "t": 110, "b": 64})
    limitations.append(
        "График покрытия предложения спросом рассчитывает периодный bid-to-cover как "
        "`sum(demand_volume) / sum(supply_volume)`, а не как среднее строковых ratios."
    )
    return make_result("bid_to_cover", fig, data, params)


def build_yield_by_type_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = ["report_period_label", "ofz_type", "_yield", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"График доходности по видам ОФЗ пропущен: нет {', '.join(missing)}.")
        return None
    data = (
        df.groupby(["report_period_label", "ofz_type"], dropna=False)
        .apply(lambda group: weighted_average(group["_yield"], group["_placement"]))
        .rename("yield_weighted_avg")
        .reset_index()
    )
    data["Подпись"] = format_number_text(data["yield_weighted_avg"], digits=2)
    assert px is not None
    fig = px.line(
        data,
        x="report_period_label",
        y="yield_weighted_avg",
        color="ofz_type",
        markers=True,
        text="Подпись",
        title="Средневзвешенная доходность ОФЗ-ПД",
        color_discrete_sequence=QUALITATIVE_COLORS,
        labels={
            "report_period_label": "Период",
            "yield_weighted_avg": "Средневзвешенная доходность",
            "ofz_type": "Вид ОФЗ",
        },
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(xaxis_title="Период", yaxis_title="Доходность")
    apply_common_layout(fig, legend_title="Вид ОФЗ")
    apply_reference_style_to_line_marker_figure(
        fig,
        title="Средневзвешенная доходность ОФЗ-ПД",
        show_yaxis_labels=True,
    )
    return make_result("yield_by_type", fig, data, params)


def build_ofz_pd_yield_key_rate_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = ["auction_date", "_yield"]
    if missing := missing_columns(df, required):
        limitations.append(f"OFZ-PD key rate chart skipped: missing {', '.join(missing)}.")
        return None
    data = df.copy()
    data["auction_month"] = pd.to_datetime(data["auction_date"], errors="coerce").dt.to_period("M").dt.to_timestamp()
    data["_yield_numeric"] = pd.to_numeric(data["_yield"], errors="coerce")
    data = data.loc[data["auction_month"].notna() & data["_yield_numeric"].notna()].copy()
    data = data.loc[ofz_pd_yield_mask(data)].copy()
    if data.empty:
        limitations.append("OFZ-PD key rate chart skipped: no OFZ-PD rows with valid yield.")
        return None

    monthly_yield = (
        data.groupby("auction_month", dropna=False)
        .agg(
            ofz_pd_yield_max=("_yield_numeric", "max"),
            ofz_pd_yield_min=("_yield_numeric", "min"),
            ofz_pd_observation_count=("_yield_numeric", "count"),
        )
        .reset_index()
        .rename(columns={"auction_month": "month"})
    )

    cbr = ensure_cbr_key_rate_processed(limitations)
    if cbr.empty:
        limitations.append("OFZ-PD key rate chart skipped: CBR key rate dataset is unavailable.")
        return None
    cbr["month"] = pd.to_datetime(cbr["period_month"], errors="coerce")
    chart_data = monthly_yield.merge(cbr, on="month", how="left", suffixes=("", "_cbr"))
    chart_data = chart_data.sort_values("month").reset_index(drop=True)
    chart_data["month_label"] = chart_data["month"].map(format_ru_month_label)
    chart_data["period_month"] = chart_data["month"].dt.strftime("%Y-%m-01")
    chart_data["period_label"] = chart_data["month_label"]
    chart_data["ofz_pd_yield_max_pct"] = chart_data["ofz_pd_yield_max"]
    chart_data["ofz_pd_yield_min_pct"] = chart_data["ofz_pd_yield_min"]
    chart_data["key_rate_available"] = chart_data["key_rate_month_end_pct"].notna()
    chart_data["yield_scope"] = "ofz_pd_only"

    missing_key_rate = chart_data.loc[~chart_data["key_rate_available"], "month_label"].astype(str).tolist()
    if missing_key_rate:
        limitations.append(
            "OFZ-PD key rate chart has months without CBR key rate, no interpolation applied: "
            + ", ".join(missing_key_rate[:12])
        )

    assert go is not None
    fig = go.Figure()
    series = [
        ("ofz_pd_yield_max", "ofz_pd_yield_max", "Максимальная доходность ОФЗ-ПД", 2, "top center"),
        ("ofz_pd_yield_min", "ofz_pd_yield_min", "Минимальная доходность ОФЗ-ПД", 2, "bottom center"),
        ("key_rate", "key_rate_month_end_pct", "Ключевая ставка Банка России", 2, "top center"),
    ]
    for series_key, value_column, name, decimals, text_position in series:
        color = REFERENCE_LINE_MARKER_COLORS[series_key]
        trace = go.Scatter(
            x=chart_data["month_label"],
            y=chart_data[value_column],
            name=name,
            customdata=chart_data[
                [
                    "month_label",
                    "ofz_pd_yield_max",
                    "ofz_pd_yield_min",
                    "key_rate_month_end_pct",
                    "key_rate_date",
                    "key_rate_source_rule",
                    "key_rate_month_is_partial",
                    "ofz_pd_observation_count",
                    "yield_scope",
                    "key_rate_available",
                ]
            ],
            hovertemplate=(
                "Месяц: %{customdata[0]}<br>"
                "Максимальная доходность ОФЗ-ПД: %{customdata[1]:.2f}%<br>"
                "Минимальная доходность ОФЗ-ПД: %{customdata[2]:.2f}%<br>"
                "Ключевая ставка Банка России: %{customdata[3]:.1f}%<br>"
                "Инфляция, г/г: %{customdata[4]:.2f}%<br>"
                "Цель по инфляции: %{customdata[5]:.1f}%<br>"
                "Наблюдений ОФЗ-ПД: %{customdata[6]}<br>"
                "Контур доходности: %{customdata[7]}<br>"
                "Ключевая ставка доступна: %{customdata[8]}<extra></extra>"
            ),
        )
        trace.update(
            hovertemplate=(
                "\u041c\u0435\u0441\u044f\u0446: %{customdata[0]}<br>"
                "\u041c\u0430\u043a\u0441. \u0434\u043e\u0445\u043e\u0434\u043d\u043e\u0441\u0442\u044c \u041e\u0424\u0417-\u041f\u0414: %{customdata[1]:.2f}%<br>"
                "\u041c\u0438\u043d. \u0434\u043e\u0445\u043e\u0434\u043d\u043e\u0441\u0442\u044c \u041e\u0424\u0417-\u041f\u0414: %{customdata[2]:.2f}%<br>"
                "\u041a\u043b\u044e\u0447\u0435\u0432\u0430\u044f \u0441\u0442\u0430\u0432\u043a\u0430 \u0411\u0430\u043d\u043a\u0430 \u0420\u043e\u0441\u0441\u0438\u0438: %{customdata[3]:.2f}%<br>"
                "\u0414\u0430\u0442\u0430 \u043a\u043b\u044e\u0447\u0435\u0432\u043e\u0439 \u0441\u0442\u0430\u0432\u043a\u0438: %{customdata[4]}<br>"
                "\u041f\u0440\u0430\u0432\u0438\u043b\u043e: %{customdata[5]}<br>"
                "\u041d\u0435\u043f\u043e\u043b\u043d\u044b\u0439 \u043c\u0435\u0441\u044f\u0446: %{customdata[6]}<br>"
                "\u041d\u0430\u0431\u043b\u044e\u0434\u0435\u043d\u0438\u0439 \u041e\u0424\u0417-\u041f\u0414: %{customdata[7]}<br>"
                "\u041a\u043e\u043d\u0442\u0443\u0440 \u0434\u043e\u0445\u043e\u0434\u043d\u043e\u0441\u0442\u0438: %{customdata[8]}<br>"
                "\u041a\u043b\u044e\u0447\u0435\u0432\u0430\u044f \u0441\u0442\u0430\u0432\u043a\u0430 \u0434\u043e\u0441\u0442\u0443\u043f\u043d\u0430: %{customdata[9]}<extra></extra>"
            )
        )
        apply_reference_line_marker_trace(trace, color)
        fig.add_trace(trace)

    title = "Динамика доходности ОФЗ-ПД и ключевой ставки Банка России, %"
    apply_reference_line_marker_layout(fig, title=title, show_yaxis_labels=False)
    fig.add_annotation(
        text=(
            "\u041a\u043b\u044e\u0447\u0435\u0432\u0430\u044f \u0441\u0442\u0430\u0432\u043a\u0430 "
            "\u0411\u0430\u043d\u043a\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 "
            "\u0443\u043a\u0430\u0437\u0430\u043d\u0430 \u043d\u0430 "
            "\u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0438\u0439 "
            "\u0434\u043e\u0441\u0442\u0443\u043f\u043d\u044b\u0439 "
            "\u0434\u0435\u043d\u044c \u043c\u0435\u0441\u044f\u0446\u0430."
        ),
        xref="paper",
        yref="paper",
        x=0,
        y=-0.18,
        showarrow=False,
        xanchor="left",
        yanchor="top",
        font={"size": 11, "color": "#4B5563"},
    )
    for annotation in build_collision_safe_value_annotations(chart_data, series, x_column="month_label"):
        fig.add_annotation(**annotation)
    fig.update_yaxes(title_text="Проценты годовых")
    fig.update_xaxes(title_text="Месяц")

    export = chart_data.copy()
    export["month"] = export["month"].dt.strftime("%Y-%m-01")
    return make_result("ofz_pd_yield_key_rate", fig, export[ofz_pd_key_rate_export_columns(export)], params)


def ofz_pd_yield_mask(data: pd.DataFrame) -> pd.Series:
    """Return rows eligible for OFZ-PD yield metrics without relying only on display encoding."""
    mask = pd.Series(True, index=data.index, dtype=bool)
    if "yield_scope" in data.columns:
        mask &= data["yield_scope"].astype("string").str.lower().eq("ofz_pd_only").fillna(False)
    if "ofz_type" in data.columns:
        ofz_type = data["ofz_type"].astype("string")
        decoded_pd = ofz_type.str.contains("ПД", na=False)
        legacy_pd = ofz_type.str.contains("ÏÄ", na=False)
        if (decoded_pd | legacy_pd).any():
            mask &= decoded_pd | legacy_pd
    return mask


def ensure_cbr_key_rate_processed(limitations: list[str]) -> pd.DataFrame:
    """Load reference CBR key rate monthly data, creating XLSX fallback outputs when needed."""
    if not config.CBR_KEY_RATE_MONTHLY_CSV.exists():
        if not config.CBR_KEY_RATE_RAW_XLSX.exists():
            limitations.append(f"CBR key rate raw XLSX not found: {config.CBR_KEY_RATE_RAW_XLSX}.")
            return pd.DataFrame()
        result = read_xlsx_key_rate(config.CBR_KEY_RATE_RAW_XLSX)
        daily = make_cbr_key_rate_daily_frame(result.observations)
        to_date = max(observation.date for observation in result.observations)
        from_date = min(observation.date for observation in result.observations)
        monthly = make_cbr_key_rate_monthly_frame(result.observations, to_date)
        metadata = build_cbr_key_rate_metadata(
            source_url=config.CBR_KEY_RATE_RAW_XLSX.as_posix(),
            from_date=from_date,
            to_date=to_date,
            retrieved_at=datetime.now(UTC),
            page_last_modified=None,
            html=None,
            row_count=len(daily),
            parser=result.parser,
        )
        write_cbr_key_rate_outputs(
            daily=daily,
            monthly=monthly,
            metadata=metadata,
            daily_output_csv=config.CBR_KEY_RATE_DAILY_CSV,
            daily_meta_json=config.CBR_KEY_RATE_DAILY_META_JSON,
            monthly_output_csv=config.CBR_KEY_RATE_MONTHLY_CSV,
        )
        limitations.append(
            "CBR key rate reference datasets were generated lazily from the emergency XLSX fallback; "
            "processed reference CSV/JSON files are generated artifacts and must not be staged."
        )
    return pd.read_csv(config.CBR_KEY_RATE_MONTHLY_CSV)


def format_ru_month_label(value: object) -> str:
    timestamp = pd.to_datetime(value, errors="coerce")
    if pd.isna(timestamp):
        return ""
    return f"{RU_MONTH_ABBR[int(timestamp.month)]}-{str(int(timestamp.year))[-2:]}"


def ofz_pd_key_rate_export_columns(data: pd.DataFrame) -> list[str]:
    columns = [
        "period_month",
        "period_label",
        "ofz_pd_yield_min_pct",
        "ofz_pd_yield_max_pct",
        "key_rate_month_end_pct",
        "key_rate_date",
        "key_rate_source_rule",
        "key_rate_month_is_partial",
    ]
    return [column for column in columns if column in data.columns]


def build_maturity_structure_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = ["report_period_label", "maturity_bucket", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"График сроковой структуры пропущен: нет {', '.join(missing)}.")
        return None
    label_column = "maturity_bucket_label" if "maturity_bucket_label" in df.columns else "maturity_bucket"
    data = (
        df.groupby(["report_period_label", "maturity_bucket", label_column], dropna=False)["_placement"]
        .sum()
        .reset_index()
    )
    data = add_placement_bln_columns(data)
    data = add_stacked_structure_metrics(data, "report_period_label", label_column)
    assert px is not None
    fig = px.bar(
        data,
        x="report_period_label",
        y="placement_volume_bln",
        color=label_column,
        text="Подпись",
        title="Структура размещения ОФЗ по срокам",
        color_discrete_map=MATURITY_COLOR_MAP,
        color_discrete_sequence=STRUCTURE_COLORS,
        category_orders={label_column: MATURITY_CATEGORY_ORDER},
        labels={
            "report_period_label": "Период",
            "placement_volume_bln": "Объем размещения по номиналу, млрд рублей",
            label_column: "Срок обращения",
        },
        custom_data=[
            "Объем, млрд руб.",
            "Объем, млн руб.",
            "Доля в столбце, %",
            "Итого по столбцу",
            "Доля в общей сумме, %",
        ],
    )
    fig.update_traces(
        textposition="inside",
        hovertemplate=(
            "Период: %{x}<br>"
            "Срок обращения: %{fullData.name}<br>"
            "Объем размещения по номиналу, млрд рублей: %{customdata[0]}<br>"
            "Объем размещения по номиналу, млн рублей: %{customdata[1]}<br>"
            "Доля сегмента в столбце, %: %{customdata[2]}<br>"
            "Итого по столбцу, млрд рублей: %{customdata[3]}<br>"
            "Доля сегмента в общей сумме, %: %{customdata[4]}<extra></extra>"
        ),
    )
    add_stacked_total_labels(fig, data, "report_period_label")
    apply_common_layout(fig, legend_title="Срок обращения")
    apply_bln_yaxis(fig)
    fig.update_layout(xaxis_title="Период")
    return make_result("maturity_structure", fig, data, params)


def build_format_structure_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = ["report_period_label", "format", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"График форматов размещения пропущен: нет {', '.join(missing)}.")
        return None
    group_columns = ["report_period_label", "format"]
    for optional_column in ["report_year", "report_period_type", "aggregation_mode"]:
        if optional_column in df.columns:
            group_columns.append(optional_column)
    aggregations: dict[str, Any] = {"_placement": ("_placement", "sum")}
    if "data_quality_flag" in df.columns:
        aggregations["data_quality_flag"] = ("data_quality_flag", combine_quality_flags)
    data = df.groupby(group_columns, dropna=False).agg(**aggregations).reset_index()
    if "data_quality_flag" not in data.columns:
        data["data_quality_flag"] = ""
    if "report_year" not in data.columns:
        period_years = {
            str(period.get("label") or period.get("report_period_label")): period.get("report_year")
            for period in params.periods
        }
        data["report_year"] = data["report_period_label"].astype(str).map(period_years)
    if "report_period_type" not in data.columns:
        data["report_period_type"] = params.period_type
    if "aggregation_mode" not in data.columns:
        data["aggregation_mode"] = params.aggregation_mode
    data = add_placement_bln_columns(data)
    data["_format_order"] = data["format"].map(format_stack_order)
    data = data.sort_values(["report_period_label", "_format_order"]).copy()
    data = add_stacked_structure_metrics(
        data,
        "report_period_label",
        "format",
        min_segment_label_share=MIN_SEGMENT_LABEL_SHARE,
        min_segment_label_value_bln=MIN_SEGMENT_LABEL_VALUE_BLN,
        always_label_categories=["дрпа", "drpa"],
    )
    assert px is not None
    fig = px.bar(
        data,
        x="report_period_label",
        y="placement_volume_bln",
        color="format",
        text="Подпись",
        title="Форматы размещения ОФЗ",
        color_discrete_map=FORMAT_COLOR_MAP,
        color_discrete_sequence=STRUCTURE_COLORS,
        labels={
            "report_period_label": "Период",
            "placement_volume_bln": "Объем размещения по номиналу, млрд рублей",
            "format": "Формат",
        },
        custom_data=[
            "report_year",
            "Объем, млрд руб.",
            "Объем, млн руб.",
            "Доля в столбце, %",
            "Итого по столбцу",
            "Доля в общей сумме, %",
            "aggregation_mode",
            "report_period_type",
            "data_quality_flag",
            "label_reason",
        ],
    )
    fig.update_traces(
        textposition="auto",
        hovertemplate=(
            "Период: %{x}<br>"
            "Формат: %{fullData.name}<br>"
            "Год: %{customdata[0]}<br>"
            "Объем сегмента, млрд рублей: %{customdata[1]}<br>"
            "Объем сегмента, млн рублей: %{customdata[2]}<br>"
            "Доля формата в общем объеме, %: %{customdata[3]}<br>"
            "Общий объем за период, млрд рублей: %{customdata[4]}<br>"
            "Доля сегмента в общей сумме, %: %{customdata[5]}<br>"
            "aggregation_mode: %{customdata[6]}<br>"
            "period_type: %{customdata[7]}<br>"
            "data_quality_flag: %{customdata[8]}<br>"
            "Причина подписи: %{customdata[9]}<extra></extra>"
        ),
    )
    add_format_bottom_segment_labels(fig, data, "report_period_label")
    add_stacked_total_labels(fig, data, "report_period_label")
    apply_common_layout(fig, legend_title="Формат")
    apply_bln_yaxis(fig)
    fig.update_layout(xaxis_title="Период")
    return make_result("format_structure", fig, data, params)


def build_format_discount_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Построить grouped bar: средневзвешенный дисконт к номиналу по форматам."""
    required = ["report_period_label", "format", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"График дисконта по форматам пропущен: нет {', '.join(missing)}.")
        return None
    component_data = aggregate_format_discount_data(df, params, limitations)
    if component_data.empty:
        limitations.append("График дисконта по форматам пропущен: нет размещений с валидным форматом.")
        return None

    data = component_data.drop_duplicates(["report_period_label", "format"]).copy()
    if "weighted_avg_discount_to_nominal" not in data.columns:
        data["weighted_avg_discount_to_nominal"] = pd.NA
    data = data.sort_values(["report_period_label", "_format_order"]).copy()
    data["placement_volume_bln"] = data.get("nominal_volume_bln", pd.NA)
    data["placement_volume_bln_display"] = data["placement_volume_bln"].map(lambda value: format_bln(value, suffix=False))
    data["weighted_avg_discount_display"] = data["weighted_avg_discount_to_nominal"].map(format_discount_value)
    data["min_discount_display"] = data.get("min_discount_to_nominal", pd.Series(pd.NA, index=data.index)).map(format_discount_value)
    data["max_discount_display"] = data.get("max_discount_to_nominal", pd.Series(pd.NA, index=data.index)).map(format_discount_value)
    data["revenue_volume_display"] = data.get("revenue_volume_bln", pd.Series(pd.NA, index=data.index)).map(lambda value: format_bln(value, suffix=False))
    data["discount_gap_display"] = data.get("discount_gap_bln", pd.Series(pd.NA, index=data.index)).map(lambda value: format_bln(value, suffix=False))
    data["label_display"] = data["weighted_avg_discount_display"]
    data["label_visible"] = data["weighted_avg_discount_to_nominal"].notna()
    data.loc[~data["label_visible"], "label_display"] = ""
    data["placement_volume_unit"] = "млрд рублей"
    data["revenue_volume_unit"] = "млрд рублей"
    data["nominal_revenue_gap_unit"] = "млрд рублей"
    data["total_nominal_volume_unit"] = "млрд рублей"

    assert px is not None
    title = (
        "Средневзвешенный дисконт к номиналу по форматам"
        "<br><sup>Y = средневзвешенный дисконт к номиналу, п.п.; размер размещения доступен в hover и CSV</sup>"
    )
    fig = px.bar(
        data,
        x="report_period_label",
        y="weighted_avg_discount_to_nominal",
        color="format",
        text="label_display",
        title=title,
        barmode="group",
        color_discrete_map=FORMAT_COLOR_MAP,
        labels={
            "report_period_label": "Период",
            "weighted_avg_discount_to_nominal": "Средневзвешенный дисконт к номиналу, п.п.",
            "format": "Формат",
        },
        custom_data=[
            "report_year",
            "format",
            "weighted_avg_discount_display",
            "min_discount_display",
            "max_discount_display",
            "placement_volume_bln_display",
            "revenue_volume_display",
            "discount_gap_display",
            "auction_count",
            "discount_calc_method_display",
            "data_quality_display",
        ],
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate=(
            "Период: %{x}<br>"
            "Год: %{customdata[0]}<br>"
            "Формат: %{customdata[1]}<br>"
            "Средневзвешенный дисконт к номиналу, п.п.: %{customdata[2]}<br>"
            "Минимальный дисконт, п.п.: %{customdata[3]}<br>"
            "Максимальный дисконт, п.п.: %{customdata[4]}<br>"
            "Объем размещения по номиналу, млрд рублей: %{customdata[5]}<br>"
            "Выручка, млрд рублей: %{customdata[6]}<br>"
            "Номинал минус выручка, млрд рублей: %{customdata[7]}<br>"
            "Количество размещений: %{customdata[8]}<br>"
            "Метод расчета: %{customdata[9]}<br>"
            "Качество данных: %{customdata[10]}<extra></extra>"
        ),
    )
    apply_common_layout(fig, legend_title="Формат")
    fig.update_layout(
        xaxis_title="Период",
        yaxis_title="Средневзвешенный дисконт к номиналу, п.п.",
        yaxis=dict(ticksuffix="", separatethousands=True),
    )
    return make_result("format_discount", fig, data, params)


def build_format_terms_comparison_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Построить small multiples: сравнение условий размещения Аукцион / ДРПА."""
    required = ["report_period_label", "format", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(
            f"График сравнения условий размещения по форматам пропущен: нет {', '.join(missing)}."
        )
        return None
    data = aggregate_format_terms_comparison_data(df, params, limitations)
    if data.empty:
        limitations.append("График `format_terms_comparison` пропущен: нет данных по форматам Аукцион / ДРПА.")
        return None

    panel_metrics = [
        (
            "yield_weighted_avg",
            "Средневзвешенная доходность размещения, % годовых",
            "% годовых",
            2,
            "weighted_avg_yield",
            "weighted_average_by_placement_volume",
            "placement_volume",
        ),
        (
            "weighted_avg_discount_to_nominal",
            "Средневзвешенный дисконт к номиналу, п.п.",
            "п.п.",
            1,
            "discount_to_nominal",
            "weighted_average_by_placement_volume",
            "placement_volume",
        ),
        (
            "revenue_to_nominal_pct",
            "Выручка / номинал, %",
            "%",
            1,
            "proceeds_mln_rub; placement_volume",
            "sum(revenue_volume) / sum(placement_volume) * 100",
            "",
        ),
        (
            "nominal_revenue_gap_bln",
            "Номинал минус выручка, млрд рублей",
            "млрд рублей",
            1,
            "placement_volume; proceeds_mln_rub",
            "(sum(placement_volume) - sum(revenue_volume)) / 1000",
            "",
        ),
    ]
    long_rows: list[dict[str, Any]] = []
    for _, row in data.iterrows():
        base: dict[str, Any] = dict(row.to_dict())
        for metric_code, metric_name_ru, metric_unit, digits, source_column, aggregation_method, weight_field in panel_metrics:
            actual_source_column = source_column
            if metric_code in {"revenue_to_nominal_pct", "nominal_revenue_gap_bln"}:
                actual_source_column = f"{row.get('revenue_source_column') or 'revenue_volume'}; placement_volume"
            metric_value = pd.to_numeric(pd.Series([row.get(metric_code)]), errors="coerce").iloc[0]
            label_value_display = "" if pd.isna(metric_value) else format_metric_value(metric_value, digits)
            placement_count = int(row.get("placement_count") or 0)
            label_count_visible = bool(pd.notna(metric_value) and placement_count > 0)
            label_count_display = f"n={placement_count}" if label_count_visible else ""
            label_display = (
                f"{label_value_display}<br>{label_count_display}"
                if label_value_display and label_count_visible
                else label_value_display
            )
            long_rows.append(
                {
                    **base,
                    "metric_code": metric_code,
                    "metric_name": metric_code,
                    "metric_name_ru": metric_name_ru,
                    "metric_label": metric_name_ru,
                    "metric_unit": metric_unit,
                    "metric_value": metric_value,
                    "source_column": actual_source_column,
                    "aggregation_method": aggregation_method,
                    "weight_field": weight_field,
                    "label_value_display": label_value_display,
                    "label_count_display": label_count_display,
                    "label_count_visible": label_count_visible,
                    "label_display": label_display,
                    "label_visible": bool(label_value_display),
                    "value_display": label_value_display,
                }
            )
    plot_data = pd.DataFrame(long_rows)
    export_data = plot_data.copy()
    plot_data = plot_data.loc[plot_data["format_available"]].dropna(subset=["metric_value"]).copy()
    if plot_data.empty:
        limitations.append("График `format_terms_comparison` пропущен: ключевые метрики по форматам пустые.")
        return None

    period_order = [
        str(period.get("label") or period.get("report_period_label"))
        for period in params.periods
    ]
    metric_order = [item[1] for item in panel_metrics]
    assert px is not None
    title = (
        "Сравнение условий размещения по форматам"
        "<br><sup>Доходность и дисконт рассчитаны средневзвешенно по объему размещения по номиналу; n — количество размещений формата в периоде</sup>"
    )
    fig = px.bar(
        plot_data,
        x="report_period_label",
        y="metric_value",
        color="format",
        facet_col="metric_label",
        facet_col_wrap=2,
        barmode="group",
        text="label_display",
        title=title,
        color_discrete_map=FORMAT_COLOR_MAP,
        category_orders={
            "report_period_label": period_order,
            "metric_label": metric_order,
            "format": ["Аукцион", "ДРПА"],
        },
        labels={
            "report_period_label": "Период",
            "metric_value": "Значение",
            "format": "Формат",
            "metric_label": "Показатель",
        },
        custom_data=[
            "report_year",
            "report_period_display_label",
            "format",
            "metric_label",
            "value_display",
            "metric_unit",
            "placement_volume_bln_display",
            "placement_count",
            "data_quality_display",
            "source_column",
            "aggregation_method",
            "weight_field",
            "yield_weighted_avg_display",
            "weighted_avg_discount_to_nominal_display",
            "revenue_to_nominal_pct_display",
            "nominal_revenue_gap_bln_display",
            "avg_placement_volume_bln_display",
            "median_placement_volume_bln_display",
            "demand_to_placement_ratio_display",
            "bid_to_cover_ratio_display",
        ],
    )
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "Год: %{customdata[0]}<br>"
            "Период: %{customdata[1]}<br>"
            "Формат: %{customdata[2]}<br>"
            "Показатель: %{customdata[3]}<br>"
            "Значение: %{customdata[4]} %{customdata[5]}<br>"
            "Единица измерения: %{customdata[5]}<br>"
            "Количество размещений формата: %{customdata[7]}<br>"
            "Метод агрегации: %{customdata[10]}<br>"
            "Исходное поле: %{customdata[9]}<br>"
            "Поле веса: %{customdata[11]}<br>"
            "Объем размещения по номиналу, млрд рублей: %{customdata[6]}<br>"
            "Средневзвешенная доходность размещения, % годовых: %{customdata[12]}<br>"
            "Средневзвешенный дисконт к номиналу, п.п.: %{customdata[13]}<br>"
            "Выручка / номинал, %: %{customdata[14]}<br>"
            "Номинал минус выручка, млрд рублей: %{customdata[15]}<br>"
            "Средний объем размещения, млрд рублей: %{customdata[16]}<br>"
            "Медианный объем размещения, млрд рублей: %{customdata[17]}<br>"
            "Спрос / объем размещения: %{customdata[18]}<br>"
            "Спрос / предложение: %{customdata[19]}<br>"
            "Качество данных: %{customdata[8]}<extra></extra>"
        ),
    )
    fig.for_each_annotation(
        lambda annotation: annotation.update(
            text=annotation.text.replace("metric_label=", "").replace("Показатель=", "").replace("Метрика=", "")
        )
    )
    fig.update_yaxes(matches=None, title_text="")
    fig.update_xaxes(title_text="Период")
    apply_common_layout(fig, legend_title="Формат")
    fig.update_yaxes(title_text="")
    fig.update_layout(
        height=760,
        margin={"l": 72, "r": 36, "t": 92, "b": 72},
        uniformtext_minsize=9,
        uniformtext_mode="hide",
    )
    export_columns = [
        "report_period_label",
        "report_period_display_label",
        "report_period_order",
        "report_year",
        "aggregation_mode",
        "format",
        "format_available",
        "metric_code",
        "metric_name",
        "metric_name_ru",
        "metric_label",
        "metric_value",
        "metric_unit",
        "source_column",
        "aggregation_method",
        "weight_field",
        "label_display",
        "label_visible",
        "label_value_display",
        "label_count_display",
        "label_count_visible",
        "placement_volume",
        "placement_volume_bln",
        "yield_weighted_avg",
        "weighted_avg_discount_to_nominal",
        "revenue_volume",
        "revenue_volume_bln",
        "revenue_to_nominal_pct",
        "nominal_revenue_gap_bln",
        "avg_placement_volume_bln",
        "median_placement_volume_bln",
        "demand_to_placement_ratio",
        "bid_to_cover_ratio",
        "auction_count",
        "data_quality_flag",
        "placement_count",
        "data_quality_display",
    ]
    return make_result("format_terms_comparison", fig, export_data[export_columns], params)


def build_format_terms_delta_by_format_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Построить график разницы условий ДРПА минус Аукцион."""
    aggregate = aggregate_format_terms_comparison_data(df, params, limitations)
    delta_data = build_format_terms_delta_data(aggregate)
    if delta_data.empty:
        limitations.append(
            "График `format_terms_delta_by_format` пропущен: нет периодов, где одновременно присутствуют Аукцион и ДРПА."
        )
        return None
    plot_data = delta_data.loc[delta_data["delta_available"]].copy()
    if plot_data.empty:
        limitations.append(
            "График `format_terms_delta_by_format` пропущен: дельты не рассчитаны из-за отсутствия одного из форматов в периодах."
        )
        fig = go.Figure()
        fig.update_layout(title="Разница условий размещения: ДРПА минус Аукцион")
        return make_result("format_terms_delta_by_format", fig, delta_data, params)
    plot_data["delta_display"] = plot_data.apply(
        lambda row: format_signed_metric_value(row["delta_drpa_minus_auction"], 1 if row["metric_unit"] != "п.п." else 2),
        axis=1,
    )
    plot_data["label_display"] = plot_data.apply(
        lambda row: f"{row['delta_display']}<br>{row['assessment_label_short']}",
        axis=1,
    )
    metric_order = [
        "Разница доходности, п.п.",
        "Разница дисконта к номиналу, п.п.",
        "Разница выручки / номинала, п.п.",
        "Разница номинал − выручка, млрд рублей",
    ]
    period_order = [
        str(period.get("label") or period.get("report_period_label"))
        for period in params.periods
    ]
    assert px is not None
    fig = px.bar(
        plot_data,
        x="report_period_label",
        y="delta_drpa_minus_auction",
        color="drpa_condition_assessment_ru",
        facet_col="metric_name_ru",
        facet_col_wrap=2,
        text="label_display",
        title=(
            "Разница условий размещения: ДРПА минус Аукцион<br>"
            "<sup>Δ = ДРПА − Аукцион; цвет показывает аналитическую оценку различия с учетом направления метрики</sup>"
        ),
        category_orders={
            "report_period_label": period_order,
            "metric_name_ru": metric_order,
            "drpa_condition_assessment_ru": ["ДРПА хуже", "ДРПА лучше", "Различие малозначимо"],
        },
        color_discrete_map={
            "ДРПА хуже": "#B91C1C",
            "ДРПА лучше": "#0F766E",
            "Различие малозначимо": "#6B7280",
        },
        labels={
            "report_period_label": "Период",
            "delta_drpa_minus_auction": "ДРПА минус Аукцион",
            "drpa_condition_assessment_ru": "Оценка",
            "metric_name_ru": "",
        },
        custom_data=[
            "report_period_display_label",
            "metric_name_ru",
            "drpa_value_display",
            "auction_value_display",
            "delta_display",
            "metric_unit",
            "drpa_condition_assessment_ru",
            "drpa_placement_count",
            "auction_placement_count",
            "drpa_placement_volume_bln",
            "auction_placement_volume_bln",
            "aggregation_method",
            "data_quality_display_short",
            "metric_caveat",
        ],
    )
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "Период: %{customdata[0]}<br>"
            "Метрика: %{customdata[1]}<br>"
            "Значение ДРПА: %{customdata[2]} %{customdata[5]}<br>"
            "Значение Аукцион: %{customdata[3]} %{customdata[5]}<br>"
            "Δ ДРПА − Аукцион: %{customdata[4]} %{customdata[5]}<br>"
            "Оценка: %{customdata[6]}<br>"
            "Количество размещений ДРПА: %{customdata[7]}<br>"
            "Количество размещений Аукцион: %{customdata[8]}<br>"
            "Объем размещения ДРПА, млрд рублей: %{customdata[9]:,.1f}<br>"
            "Объем размещения Аукцион, млрд рублей: %{customdata[10]:,.1f}<br>"
            "Метод агрегации: %{customdata[11]}<br>"
            "Качество данных: %{customdata[12]}<br>"
            "%{customdata[13]}<extra></extra>"
        ),
    )
    if "Различие малозначимо" not in set(plot_data["drpa_condition_assessment_ru"].dropna().astype(str)):
        fig.add_bar(
            x=[None],
            y=[None],
            name="Различие малозначимо",
            marker_color="#6B7280",
            showlegend=True,
            hoverinfo="skip",
        )
    fig.add_hline(y=0, line_color="#4B5563", line_width=1, line_dash="dot")
    fig.for_each_annotation(
        lambda annotation: annotation.update(
            text=annotation.text.replace("metric_name_ru=", "").replace("Показатель=", "")
        )
    )
    fig.update_yaxes(matches=None, zeroline=True, title_text="")
    fig.update_xaxes(title_text="Период")
    apply_common_layout(fig, legend_title="Оценка")
    fig.update_layout(
        height=760,
        margin={"l": 78, "r": 42, "t": 96, "b": 72},
        uniformtext_minsize=9,
        uniformtext_mode="hide",
    )
    limitations.append(
        "График `format_terms_delta_by_format` рассчитывает дельты только для периодов, где есть оба формата; отсутствующие пары не рисуются как нулевые значения."
    )
    return make_result("format_terms_delta_by_format", fig, delta_data, params)


def assess_drpa_delta(
    delta_value: Any,
    preference_direction: str,
    threshold: float,
    delta_available: bool,
) -> tuple[str, str, str]:
    """Оценить, лучше или хуже условия ДРПА с учетом направления метрики."""
    if not delta_available:
        return "not_applicable", "Не применимо", ""
    numeric = pd.to_numeric(pd.Series([delta_value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return "not_applicable", "Не применимо", ""
    value = float(numeric)
    if abs(value) <= threshold:
        return "neutral_or_small_difference", "Различие малозначимо", "≈"
    if preference_direction == "lower_is_better":
        if value > threshold:
            return "drpa_worse", "ДРПА хуже", "хуже"
        return "drpa_better", "ДРПА лучше", "лучше"
    if preference_direction == "higher_is_better":
        if value > threshold:
            return "drpa_better", "ДРПА лучше", "лучше"
        return "drpa_worse", "ДРПА хуже", "хуже"
    return "not_applicable", "Не применимо", ""


def build_format_terms_delta_data(aggregate: pd.DataFrame) -> pd.DataFrame:
    """Собрать таблицу дельт ДРПА минус Аукцион по периодам и метрикам."""
    if aggregate.empty:
        return pd.DataFrame()
    metrics = [
        (
            "delta_yield_pp",
            "Разница доходности, п.п.",
            "п.п.",
            "yield_weighted_avg",
            "weighted_avg_yield",
            "weighted_average_by_placement_volume",
            "placement_volume",
            2,
            "lower_is_better",
            0.10,
            "",
        ),
        (
            "delta_discount_pp",
            "Разница дисконта к номиналу, п.п.",
            "п.п.",
            "weighted_avg_discount_to_nominal",
            "discount_to_nominal",
            "weighted_average_by_placement_volume",
            "placement_volume",
            2,
            "lower_is_better",
            0.10,
            "",
        ),
        (
            "delta_revenue_to_nominal_pp",
            "Разница выручки / номинала, п.п.",
            "п.п.",
            "revenue_to_nominal_pct",
            "revenue_volume; placement_volume",
            "sum(revenue_volume) / sum(placement_volume) * 100",
            "",
            2,
            "higher_is_better",
            0.10,
            "",
        ),
        (
            "delta_nominal_revenue_gap_bln",
            "Разница номинал − выручка, млрд рублей",
            "млрд рублей",
            "nominal_revenue_gap_bln",
            "placement_volume; revenue_volume",
            "(sum(placement_volume) - sum(revenue_volume)) / 1000",
            "",
            1,
            "lower_is_better",
            10.0,
            "Абсолютная разница зависит от объема размещения; для относительного сравнения см. выручку / номинал.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for period_label, period_group in aggregate.groupby("report_period_label", dropna=False):
        format_available = get_bool_series(period_group, "format_available", default=True)
        auction_rows = period_group.loc[(period_group["format"] == "Аукцион") & format_available]
        drpa_rows = period_group.loc[(period_group["format"] == "ДРПА") & format_available]
        auction = auction_rows.iloc[0] if not auction_rows.empty else None
        drpa = drpa_rows.iloc[0] if not drpa_rows.empty else None
        period_display = first_available_from_rows(period_group, "report_period_display_label", str(period_label))
        report_year = first_available_from_rows(period_group, "report_year", pd.NA)
        for (
            metric_code,
            metric_name_ru,
            metric_unit,
            value_column,
            source_column,
            aggregation_method,
            weight_field,
            digits,
            preference_direction,
            assessment_threshold,
            metric_caveat,
        ) in metrics:
            auction_value = auction.get(value_column) if auction is not None else pd.NA
            drpa_value = drpa.get(value_column) if drpa is not None else pd.NA
            auction_numeric = to_optional_float(auction_value)
            drpa_numeric = to_optional_float(drpa_value)
            delta_available = auction is not None and drpa is not None and auction_numeric is not None and drpa_numeric is not None
            delta_value = drpa_numeric - auction_numeric if delta_available else pd.NA
            missing_parts: list[str] = []
            if auction is None:
                missing_parts.append("no_auction")
            if drpa is None:
                missing_parts.append("no_drpa")
            if auction is not None and pd.isna(auction_value):
                missing_parts.append("auction_metric_missing")
            if drpa is not None and pd.isna(drpa_value):
                missing_parts.append("drpa_metric_missing")
            raw_quality = combine_quality_flags(
                pd.Series(
                    [
                        auction.get("data_quality_flag", "") if auction is not None else "",
                        drpa.get("data_quality_flag", "") if drpa is not None else "",
                        "|".join(missing_parts),
                    ]
                )
            )
            if not delta_available and not raw_quality:
                raw_quality = "delta_not_calculated"
            assessment, assessment_ru, assessment_short = assess_drpa_delta(
                delta_value,
                preference_direction,
                assessment_threshold,
                delta_available,
            )
            label_display = (
                f"{format_signed_metric_value(delta_value, digits)}<br>{assessment_short}"
                if delta_available
                else ""
            )
            full_quality = data_quality_display(raw_quality)
            rows.append(
                {
                    "report_period_label": str(period_label),
                    "report_period_display_label": period_display,
                    "report_year": report_year,
                    "metric_code": metric_code,
                    "metric_name_ru": metric_name_ru,
                    "metric_unit": metric_unit,
                    "auction_value": auction_value,
                    "drpa_value": drpa_value,
                    "delta_drpa_minus_auction": delta_value,
                    "metric_preference_direction": preference_direction,
                    "assessment_threshold": assessment_threshold,
                    "drpa_condition_assessment": assessment,
                    "drpa_condition_assessment_ru": assessment_ru,
                    "assessment_label_short": assessment_short,
                    "auction_placement_count": int(auction.get("placement_count", 0)) if auction is not None else 0,
                    "drpa_placement_count": int(drpa.get("placement_count", 0)) if drpa is not None else 0,
                    "auction_placement_volume_bln": auction.get("placement_volume_bln", pd.NA) if auction is not None else pd.NA,
                    "drpa_placement_volume_bln": drpa.get("placement_volume_bln", pd.NA) if drpa is not None else pd.NA,
                    "aggregation_method": aggregation_method,
                    "source_column": source_column,
                    "weight_field": weight_field,
                    "label_display": label_display,
                    "label_visible": bool(delta_available),
                    "metric_caveat": metric_caveat,
                    "delta_available": bool(delta_available),
                    "data_quality_flag": raw_quality,
                    "data_quality_display": full_quality,
                    "data_quality_display_short": data_quality_display_short(raw_quality),
                    "data_quality_display_full": full_quality,
                    "auction_value_display": format_metric_value(auction_value, digits),
                    "drpa_value_display": format_metric_value(drpa_value, digits),
                }
            )
    result = pd.DataFrame(rows)
    if result.empty:
        return result
    metric_order = {code: index for index, (code, *_rest) in enumerate(metrics, start=1)}
    result["_metric_order"] = result["metric_code"].map(metric_order)
    return result.sort_values(["report_period_label", "_metric_order"]).drop(columns=["_metric_order"])


def first_available_from_rows(rows: pd.DataFrame, column: str, fallback: Any) -> Any:
    """Вернуть первое непустое значение из DataFrame."""
    if column not in rows.columns:
        return fallback
    values = rows[column].dropna()
    return values.iloc[0] if not values.empty else fallback


def aggregate_format_terms_comparison_data(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> pd.DataFrame:
    """Агрегировать показатели условий размещения по периоду и формату."""
    data = df.dropna(subset=["report_period_label", "format"]).copy()
    if data.empty:
        return pd.DataFrame()
    data["format"] = data["format"].astype(str).str.strip()
    data = data[data["format"].isin(["Аукцион", "ДРПА"])].copy()
    if data.empty:
        return pd.DataFrame()

    revenue_column = first_existing_column(
        data,
        ["revenue_volume", "proceeds_volume", "placement_revenue", "proceeds_mln_rub"],
    )
    if revenue_column is None:
        limitations.append("Для `format_terms_comparison` не найдена колонка выручки; revenue-панели будут пустыми.")
    period_order_map = {
        str(period.get("label") or period.get("report_period_label")): int(index)
        for index, period in enumerate(params.periods, start=1)
    }
    period_display_map = {
        str(period.get("label") or period.get("report_period_label")): str(
            period.get("report_period_display_label")
            or period.get("display_label")
            or period.get("label")
            or period.get("report_period_label")
        )
        for period in params.periods
    }
    period_year_map = {
        str(period.get("label") or period.get("report_period_label")): period.get("report_year")
        for period in params.periods
    }

    rows: list[dict[str, Any]] = []
    for (period_label, format_name), group in data.groupby(["report_period_label", "format"], dropna=False):
        placement = pd.to_numeric(group["_placement"], errors="coerce")
        placement_sum = float(placement.sum()) if placement.notna().any() else pd.NA
        revenue_values = (
            pd.to_numeric(group[revenue_column], errors="coerce")
            if revenue_column
            else pd.Series(pd.NA, index=group.index, dtype="Float64")
        )
        revenue_sum = float(revenue_values.sum()) if revenue_values.notna().any() else pd.NA
        demand_sum = pd.to_numeric(group.get("_demand"), errors="coerce").sum() if "_demand" in group else pd.NA
        supply_sum = pd.to_numeric(group.get("_supply"), errors="coerce").sum() if "_supply" in group else pd.NA
        yield_source = "_weighted_avg_yield" if "_weighted_avg_yield" in group.columns else "_yield"
        yield_weighted = weighted_average_or_na(group[yield_source], placement)
        discount_weighted = weighted_average_or_na(group["_discount_to_nominal"], placement)
        gap = (
            float(placement_sum) - float(revenue_sum)
            if pd.notna(placement_sum) and pd.notna(revenue_sum)
            else pd.NA
        )
        revenue_ratio = (
            float(revenue_sum) / float(placement_sum) * 100.0
            if pd.notna(revenue_sum) and pd.notna(placement_sum) and float(placement_sum) > 0
            else pd.NA
        )
        placement_count = group_placement_count(group)
        row = {
            "report_period_label": str(period_label),
            "report_period_display_label": period_display_map.get(str(period_label), str(period_label)),
            "report_period_order": period_order_map.get(str(period_label), pd.NA),
            "report_year": first_non_null(group, "report_year", period_year_map.get(str(period_label))),
            "aggregation_mode": first_non_null(group, "aggregation_mode", params.aggregation_mode),
            "format": str(format_name),
            "placement_volume": placement_sum,
            "placement_volume_bln": float(placement_sum) / 1000.0 if pd.notna(placement_sum) else pd.NA,
            "yield_weighted_avg": yield_weighted,
            "weighted_avg_discount_to_nominal": discount_weighted,
            "revenue_volume": revenue_sum,
            "revenue_source_column": revenue_column or "",
            "revenue_volume_bln": float(revenue_sum) / 1000.0 if pd.notna(revenue_sum) else pd.NA,
            "revenue_to_nominal_pct": revenue_ratio,
            "nominal_revenue_gap_bln": float(gap) / 1000.0 if pd.notna(gap) else pd.NA,
            "avg_placement_volume_bln": float(placement.mean()) / 1000.0 if placement.notna().any() else pd.NA,
            "median_placement_volume_bln": float(placement.median()) / 1000.0 if placement.notna().any() else pd.NA,
            "demand_to_placement_ratio": (
                float(demand_sum) / float(placement_sum)
                if pd.notna(demand_sum) and pd.notna(placement_sum) and float(placement_sum) > 0
                else pd.NA
            ),
            "bid_to_cover_ratio": (
                float(demand_sum) / float(supply_sum)
                if pd.notna(demand_sum) and pd.notna(supply_sum) and float(supply_sum) > 0
                else pd.NA
            ),
            "auction_count": placement_count,
            "placement_count": placement_count,
            "format_available": True,
            "aggregation_method": "weighted_average_by_placement_volume; sums for volume/revenue metrics",
            "weight_field": "placement_volume",
            "data_quality_flag": combine_quality_flags(group["data_quality_flag"]) if "data_quality_flag" in group.columns else "",
        }
        rows.append(row)

    result = pd.DataFrame(rows)
    if result.empty:
        return result
    result = add_missing_format_terms_rows(result, params, period_order_map, period_display_map, period_year_map)
    result["_format_order"] = result["format"].map(format_stack_order)
    result = result.sort_values(["report_period_order", "_format_order", "format"]).copy()
    result["data_quality_display"] = result["data_quality_flag"].map(data_quality_display)
    display_columns = {
        "placement_volume_bln": 1,
        "yield_weighted_avg": 2,
        "weighted_avg_discount_to_nominal": 1,
        "revenue_volume_bln": 1,
        "revenue_to_nominal_pct": 1,
        "nominal_revenue_gap_bln": 1,
        "avg_placement_volume_bln": 1,
        "median_placement_volume_bln": 1,
        "demand_to_placement_ratio": 2,
        "bid_to_cover_ratio": 2,
    }
    for column, digits in display_columns.items():
        result[f"{column}_display"] = result[column].map(lambda value, d=digits: format_metric_value(value, d))
    return result


def add_missing_format_terms_rows(
    result: pd.DataFrame,
    params: report_params.ReportParams,
    period_order_map: dict[str, int],
    period_display_map: dict[str, str],
    period_year_map: dict[str, Any],
) -> pd.DataFrame:
    """Добавить контрольные строки для отсутствующих форматов без отрисовки нулевых баров."""
    existing = {
        (str(row["report_period_label"]), str(row["format"]))
        for _, row in result[["report_period_label", "format"]].drop_duplicates().iterrows()
    }
    rows: list[dict[str, Any]] = []
    for period in params.periods:
        period_label = str(period.get("label") or period.get("report_period_label"))
        for format_name in ("Аукцион", "ДРПА"):
            if (period_label, format_name) in existing:
                continue
            rows.append(
                {
                    "report_period_label": period_label,
                    "report_period_display_label": period_display_map.get(period_label, period_label),
                    "report_period_order": period_order_map.get(period_label, pd.NA),
                    "report_year": period_year_map.get(period_label),
                    "aggregation_mode": params.aggregation_mode,
                    "format": format_name,
                    "placement_volume": pd.NA,
                    "placement_volume_bln": pd.NA,
                    "yield_weighted_avg": pd.NA,
                    "weighted_avg_discount_to_nominal": pd.NA,
                    "revenue_volume": pd.NA,
                    "revenue_source_column": "",
                    "revenue_volume_bln": pd.NA,
                    "revenue_to_nominal_pct": pd.NA,
                    "nominal_revenue_gap_bln": pd.NA,
                    "avg_placement_volume_bln": pd.NA,
                    "median_placement_volume_bln": pd.NA,
                    "demand_to_placement_ratio": pd.NA,
                    "bid_to_cover_ratio": pd.NA,
                    "auction_count": 0,
                    "placement_count": 0,
                    "format_available": False,
                    "aggregation_method": "not_applicable_no_placements",
                    "weight_field": "",
                    "data_quality_flag": "format_absent_in_period",
                }
            )
    if not rows:
        return result
    return pd.concat([result, pd.DataFrame(rows)], ignore_index=True)


def group_placement_count(group: pd.DataFrame) -> int:
    """Вернуть количество размещений группы, используя auction_count как источник при наличии."""
    if "auction_count" in group.columns:
        values = pd.to_numeric(group["auction_count"], errors="coerce")
        if values.notna().any():
            return int(values.fillna(0).sum())
    return int(len(group))


def weighted_average_or_na(values: pd.Series, weights: pd.Series) -> Any:
    """Посчитать средневзвешенное значение с защитой от пустых весов."""
    numeric_values = pd.to_numeric(values, errors="coerce")
    numeric_weights = pd.to_numeric(weights, errors="coerce")
    valid = numeric_values.notna() & numeric_weights.gt(0)
    if not valid.any():
        return pd.NA
    weight_sum = numeric_weights.loc[valid].sum()
    if weight_sum <= 0:
        return pd.NA
    return float((numeric_values.loc[valid] * numeric_weights.loc[valid]).sum() / weight_sum)


def first_non_null(group: pd.DataFrame, column: str, fallback: Any = pd.NA) -> Any:
    """Вернуть первое непустое значение группы или fallback."""
    if column not in group.columns:
        return fallback
    values = group[column].dropna()
    return values.iloc[0] if not values.empty else fallback

def aggregate_format_discount_data(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> pd.DataFrame:
    """Агрегировать номинал и разложить его на выручку и дисконтный разрыв."""
    data = df.dropna(subset=["report_period_label", "format"]).copy()
    if data.empty:
        return pd.DataFrame()
    revenue_column = first_existing_column(
        data,
        ["revenue_volume", "proceeds_volume", "placement_revenue", "proceeds_mln_rub"],
    )
    if "_discount_to_nominal" not in data.columns:
        data["_discount_to_nominal"] = pd.NA
    if data["_discount_to_nominal"].isna().all():
        limitations.append("Для `format_discount` не найден валидный `discount_to_nominal`; дисконтный разрыв будет рассчитан только при наличии выручки.")
    group_columns = ["report_period_label", "format"]
    for optional_column in ["report_year", "report_period_type", "aggregation_mode"]:
        if optional_column in data.columns:
            group_columns.append(optional_column)

    rows: list[dict[str, Any]] = []
    for keys, group in data.groupby(group_columns, dropna=False):
        key_values = keys if isinstance(keys, tuple) else (keys,)
        row = dict(zip(group_columns, key_values))
        placement = pd.to_numeric(group["_placement"], errors="coerce").sum()
        discounts = pd.to_numeric(group["_discount_to_nominal"], errors="coerce")
        weights = pd.to_numeric(group["_placement"], errors="coerce")
        valid_discount = discounts.notna() & weights.gt(0)
        weighted_discount = (
            float((discounts.loc[valid_discount] * weights.loc[valid_discount]).sum() / weights.loc[valid_discount].sum())
            if valid_discount.any() and weights.loc[valid_discount].sum() > 0
            else pd.NA
        )
        revenue_values = pd.to_numeric(group[revenue_column], errors="coerce") if revenue_column else pd.Series(dtype="float64")
        actual_revenue = float(revenue_values.sum()) if revenue_column and revenue_values.notna().any() else pd.NA
        revenue = actual_revenue
        gap = placement - revenue if pd.notna(revenue) else pd.NA
        calc_method = discount_calc_method(group)
        quality_parts = [combine_quality_flags(group["data_quality_flag"])] if "data_quality_flag" in group.columns else []
        if pd.isna(revenue) and pd.notna(weighted_discount):
            revenue = placement * (100.0 - float(weighted_discount)) / 100.0
            gap = placement - revenue
            calc_method = f"{calc_method}; fallback revenue = nominal * (100 - discount_pp) / 100"
            quality_parts.append("revenue_estimated_from_discount")
        if not valid_discount.any() and pd.isna(gap):
            quality_parts.append("missing_discount_to_nominal")
        if pd.notna(gap) and float(gap) < -0.000001:
            quality_parts.append("negative_discount_gap")
            revenue = placement
            gap = pd.NA
        row.update(
            {
                "placement_volume": placement,
                "nominal_volume_bln": placement / 1000.0,
                "weighted_avg_discount_to_nominal": weighted_discount,
                "weighted_avg_discount_pp": weighted_discount,
                "min_discount_to_nominal": float(discounts.min()) if discounts.notna().any() else pd.NA,
                "min_discount_pp": float(discounts.min()) if discounts.notna().any() else pd.NA,
                "max_discount_to_nominal": float(discounts.max()) if discounts.notna().any() else pd.NA,
                "max_discount_pp": float(discounts.max()) if discounts.notna().any() else pd.NA,
                "revenue_volume": revenue,
                "revenue_volume_bln": revenue / 1000.0 if pd.notna(revenue) else pd.NA,
                "nominal_revenue_gap": gap,
                "nominal_revenue_gap_bln": gap / 1000.0 if pd.notna(gap) else pd.NA,
                "discount_gap_bln": gap / 1000.0 if pd.notna(gap) else pd.NA,
                "auction_count": int(len(group)),
                "discount_calc_method": calc_method,
                "data_quality_flag": "; ".join(part for part in quality_parts if part),
            }
        )
        rows.append(row)

    result = pd.DataFrame(rows)
    if result.empty:
        return result
    if "report_year" not in result.columns:
        period_years = {
            str(period.get("label") or period.get("report_period_label")): period.get("report_year")
            for period in params.periods
        }
        result["report_year"] = result["report_period_label"].astype(str).map(period_years)
    if "report_period_type" not in result.columns:
        result["report_period_type"] = params.period_type
    if "aggregation_mode" not in result.columns:
        result["aggregation_mode"] = params.aggregation_mode
    result["_format_order"] = result["format"].map(format_stack_order)
    result = result.sort_values(["report_period_label", "_format_order"]).copy()
    total_nominal = result.groupby("report_period_label")["nominal_volume_bln"].transform("sum")
    result["format_share_pct"] = result["nominal_volume_bln"] / total_nominal * 100.0
    total_nominal_by_period = result.groupby("report_period_label")["nominal_volume_bln"].sum()
    total_revenue_by_period = result.groupby("report_period_label")["revenue_volume_bln"].sum(min_count=1)
    total_gap_by_period = result.groupby("report_period_label")["discount_gap_bln"].sum(min_count=1)
    component_rows: list[dict[str, Any]] = []
    for _, row in result.iterrows():
        component_rows.extend(format_discount_component_rows(row))
    component_data = pd.DataFrame(component_rows)
    if component_data.empty:
        return component_data
    component_data = component_data.sort_values(["report_period_label", "_format_order", "component_order"]).copy()
    component_data["column_total"] = component_data["report_period_label"].map(total_nominal_by_period)
    component_data["total_nominal_volume_bln"] = component_data["column_total"]
    component_data["total_revenue_volume_bln"] = component_data["report_period_label"].map(total_revenue_by_period)
    component_data["total_discount_gap_bln"] = component_data["report_period_label"].map(total_gap_by_period)
    component_data["total_label_display"] = component_data["column_total"].map(lambda value: f"Итого {format_bln(value, suffix=False)}")
    component_data["data_quality_display"] = component_data["data_quality_flag"].map(data_quality_display)
    component_data["discount_calc_method_display"] = component_data["discount_calc_method"].map(discount_calc_method_display)
    component_data["component_display"] = component_data["component_volume_bln"].map(lambda value: format_bln(value, suffix=False))
    component_data["nominal_volume_display"] = component_data["nominal_volume_bln"].map(lambda value: format_bln(value, suffix=False))
    component_data["revenue_volume_display"] = component_data["revenue_volume_bln"].map(lambda value: format_bln(value, suffix=False))
    component_data["discount_gap_display"] = component_data["discount_gap_bln"].map(lambda value: format_bln(value, suffix=False))
    component_data["format_share_pct_display"] = component_data["format_share_pct"].map(format_plain_percent_value)
    component_data["weighted_avg_discount_display"] = component_data["weighted_avg_discount_pp"].map(format_discount_value)
    component_data["total_label_visible"] = True
    y_max = pd.to_numeric(component_data["column_total"], errors="coerce").max()
    offset = float(y_max) * 0.025 if pd.notna(y_max) and float(y_max) > 0 else 0.0
    component_data["total_label_y"] = pd.to_numeric(component_data["column_total"], errors="coerce") + offset
    component_data["Сегмент"] = component_data["component_label"]
    component_data["Подпись"] = component_data["label_display"]
    validate_format_discount_components(component_data, limitations)
    return component_data


def format_discount_component_rows(row: pd.Series) -> list[dict[str, Any]]:
    """Развернуть форматный сегмент в компоненты выручки и дисконтного разрыва."""
    format_name = str(row.get("format", "")).strip()
    nominal = pd.to_numeric(pd.Series([row.get("nominal_volume_bln")]), errors="coerce").iloc[0]
    revenue = pd.to_numeric(pd.Series([row.get("revenue_volume_bln")]), errors="coerce").iloc[0]
    gap = pd.to_numeric(pd.Series([row.get("discount_gap_bln")]), errors="coerce").iloc[0]
    if pd.isna(nominal) or float(nominal) <= 0:
        return []
    base = row.to_dict()
    common = {
        key: base.get(key)
        for key in [
            "report_period_label",
            "report_year",
            "report_period_type",
            "aggregation_mode",
            "format",
            "_format_order",
            "nominal_volume_bln",
            "revenue_volume_bln",
            "discount_gap_bln",
            "weighted_avg_discount_to_nominal",
            "weighted_avg_discount_pp",
            "min_discount_to_nominal",
            "min_discount_pp",
            "max_discount_to_nominal",
            "max_discount_pp",
            "format_share_pct",
            "auction_count",
            "discount_calc_method",
            "data_quality_flag",
        ]
    }
    rows: list[dict[str, Any]] = []
    component_specs = [
        ("revenue", "выручка", revenue, 1),
        ("discount_gap", "дисконтный разрыв", gap, 2),
    ]
    for component_type, component_display_name, value, order in component_specs:
        if pd.isna(value) or float(value) <= 0:
            continue
        label = f"{format_name} — {component_display_name}"
        visible = float(value) >= MIN_SEGMENT_LABEL_VALUE_BLN or float(value) / float(nominal) >= MIN_SEGMENT_LABEL_SHARE
        rows.append(
            {
                **common,
                "component_type": component_type,
                "component_display_name": component_display_name.capitalize(),
                "component_label": label,
                "component_order": order,
                "component_volume_bln": float(value),
                "label_display": format_bln(value, suffix=False) if visible else "",
                "label_visible": bool(visible),
            }
        )
    return rows


def validate_format_discount_components(data: pd.DataFrame, limitations: list[str]) -> None:
    """Проверить базовые равенства компонента: revenue + discount_gap = nominal."""
    if data.empty:
        return
    pairs = data.drop_duplicates(["report_period_label", "format"])
    for _, row in pairs.iterrows():
        revenue = pd.to_numeric(pd.Series([row.get("revenue_volume_bln")]), errors="coerce").iloc[0]
        gap = pd.to_numeric(pd.Series([row.get("discount_gap_bln")]), errors="coerce").iloc[0]
        nominal = pd.to_numeric(pd.Series([row.get("nominal_volume_bln")]), errors="coerce").iloc[0]
        if pd.notna(revenue) and pd.notna(gap) and pd.notna(nominal):
            if abs((float(revenue) + float(gap)) - float(nominal)) > 0.01:
                limitations.append(
                    f"`format_discount`: revenue + discount_gap != nominal для {row.get('report_period_label')} / {row.get('format')}."
                )


def add_format_discount_labels(data: pd.DataFrame) -> pd.DataFrame:
    """Добавить подписи номинала и дисконта для composite-графика."""
    result = data.copy()
    result["label_nominal_display"] = result["placement_volume_bln"].map(lambda value: format_bln(value, suffix=False))
    result["label_discount_display"] = result["weighted_avg_discount_to_nominal"].map(format_discount_label)
    result["format_discount_label_display"] = result.apply(
        lambda row: f"{row['label_nominal_display']}<br>{row['label_discount_display']}",
        axis=1,
    )
    for column, display_column in [
        ("placement_volume_bln", "placement_volume_bln_display"),
        ("revenue_volume_bln", "revenue_volume_bln_display"),
        ("nominal_revenue_gap_bln", "nominal_revenue_gap_bln_display"),
    ]:
        result[display_column] = result[column].map(lambda value: format_bln(value, suffix=False)) if column in result.columns else ""
    for column, display_column in [
        ("weighted_avg_discount_to_nominal", "weighted_avg_discount_display"),
        ("min_discount_to_nominal", "min_discount_display"),
        ("max_discount_to_nominal", "max_discount_display"),
    ]:
        result[display_column] = result[column].map(format_discount_value)
    return result


def format_discount_segment_label(row: pd.Series) -> str:
    """Сформировать двухстрочную подпись сегмента: номинал и дисконт."""
    nominal = str(row.get("label_nominal_display", "")).strip()
    discount = str(row.get("label_discount_display", "")).strip() or "н.д."
    if not nominal:
        return ""
    if bool(row.get("discount_label_visible", False)):
        return f"{nominal}<br>дисконт {discount}"
    return f"{nominal}<br>дисконт н.д."


def format_discount_label(value: Any) -> str:
    """Отформатировать дисконт для подписи сегмента."""
    text = format_discount_value(value)
    return f"{text} п.п." if text else "н.д."


def format_discount_value(value: Any) -> str:
    """Отформатировать дисконт без единицы измерения."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return ""
    return f"{float(numeric):,.1f}".replace(",", " ").replace(".", ",")


def format_plain_percent_value(value: Any) -> str:
    """Отформатировать процентное значение без знака процента для hover."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return ""
    return f"{float(numeric):,.1f}".replace(",", " ").replace(".", ",")


def discount_calc_method(group: pd.DataFrame) -> str:
    """Описать метод расчета дисконта для группы."""
    if "discount_to_nominal" in group.columns and pd.to_numeric(group["discount_to_nominal"], errors="coerce").notna().any():
        return "source: discount_to_nominal"
    if "_cutoff_price" in group.columns and pd.to_numeric(group["_cutoff_price"], errors="coerce").notna().any():
        return "fallback: 100 - cutoff_price"
    return "нет данных для расчета дисконта"


def first_existing_column(data: pd.DataFrame, candidates: Sequence[str]) -> str | None:
    """Вернуть первую существующую колонку из списка кандидатов."""
    for column in candidates:
        if column in data.columns:
            return column
    return None


def add_format_discount_markers(figure: Any, data: pd.DataFrame) -> None:
    """Добавить легкие маркеры дисконта внутри соответствующего stacked-сегмента."""
    assert go is not None
    if data.empty or "weighted_avg_discount_to_nominal" not in data.columns:
        return
    work = data.copy()
    work["_format_order"] = work["format"].map(format_stack_order)
    work = work.sort_values(["report_period_label", "_format_order"]).copy()
    work["segment_base_bln"] = work.groupby("report_period_label")["placement_volume_bln"].cumsum() - work["placement_volume_bln"]
    work["segment_mid_bln"] = work["segment_base_bln"] + work["placement_volume_bln"] / 2
    markers = work.dropna(subset=["weighted_avg_discount_to_nominal", "segment_mid_bln"]).copy()
    if markers.empty:
        return
    figure.add_trace(
        go.Scatter(
            x=markers["report_period_label"],
            y=markers["segment_mid_bln"],
            mode="markers",
            marker={
                "symbol": "line-ew",
                "size": 22,
                "color": "#1F2933",
                "line": {"width": 2, "color": "#1F2933"},
            },
            customdata=markers[
                [
                    "format",
                    "weighted_avg_discount_display",
                    "placement_volume_bln_display",
                    "discount_calc_method",
                    "data_quality_flag",
                ]
            ],
            hovertemplate=(
                "Период: %{x}<br>"
                "Формат: %{customdata[0]}<br>"
                "Маркер дисконта, п.п.: %{customdata[1]}<br>"
                "Номинал сегмента, млрд рублей: %{customdata[2]}<br>"
                "Метод расчета: %{customdata[3]}<br>"
                "data_quality_flag: %{customdata[4]}<extra></extra>"
            ),
            showlegend=False,
            name="Маркер дисконта",
        )
    )


def build_risk_quadrant_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = ["report_period_label", "_yield", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"Квадрант риска по отчетному периоду пропущен: нет {', '.join(missing)}.")
        return None
    ratio_column, ratio_title, x_axis_title = select_demand_to_placement_ratio(df, limitations)
    if ratio_column is None:
        limitations.append("Квадрант риска по отчетному периоду пропущен: нет ratio спроса с данными.")
        return None
    target_labels = {str(period["label"]) for period in params.periods if period.get("is_target_period")}
    data = df[df["report_period_label"].astype("string").isin(target_labels)].copy()
    if data.empty:
        limitations.append("Квадрант риска по отчетному периоду пропущен: в target period нет строк.")
        return None
    if "maturity_bucket_label" in data.columns:
        color_column = "maturity_bucket_label"
    elif "maturity_bucket" in data.columns:
        data["maturity_bucket_label"] = data["maturity_bucket"].map(
            {
                "short_term": "Краткосрочные",
                "medium_term": "Среднесрочные",
                "long_term": "Долгосрочные",
                "requires_review": "Требует проверки",
            }
        )
        color_column = "maturity_bucket_label"
    else:
        color_column = None
    hover_columns = [
        column
        for column in [
            "issue_code",
            "ofz_type",
            "format",
            "report_period_label",
            "auction_date",
            "auction_quarter",
            "demand_volume",
            "supply_volume",
            "placement_volume",
            "_demand_to_placement",
            "_bid_to_cover",
            "_weighted_avg_yield",
            "_cutoff_price",
            "_weighted_avg_price",
            "_demand",
            "_supply",
            "_placement",
            "ratio_basis",
            "maturity_bucket",
        ]
        if column in data.columns
    ]
    data = data.dropna(subset=[ratio_column, "_yield"]).copy()
    if data.empty:
        limitations.append(f"Квадрант риска по отчетному периоду пропущен: нет строк с доходностью и `{ratio_column}`.")
        return None
    data = scatter_chart_policy.add_scatter_labels(
        data,
        ratio_column,
        "_yield",
        placement_column="_placement",
        yield_column="_yield",
        max_labels=MAX_SCATTER_LABELS,
    )
    data["ratio_basis"] = scatter_chart_policy.ratio_basis_for(ratio_column)
    if "ratio_basis" not in hover_columns:
        hover_columns.append("ratio_basis")
    assert px is not None
    fig = px.scatter(
        data,
        x=ratio_column,
        y="_yield",
        size="_placement",
        color=color_column,
        text="scatter_label",
        hover_data=hover_columns,
        title=f"Квадрант риска: {ratio_title} и доходность",
        color_discrete_map=MATURITY_COLOR_MAP,
        color_discrete_sequence=QUALITATIVE_COLORS,
        labels={
            ratio_column: x_axis_title,
            "_demand_to_placement": "demand_to_placement_ratio",
            "_bid_to_cover": "bid_to_cover_ratio",
            "_yield": "Доходность",
            "_weighted_avg_yield": "Средневзвешенная доходность",
            "_cutoff_price": "Цена отсечения",
            "_weighted_avg_price": "Средневзвешенная цена",
            "_placement": "Объем размещения по номиналу",
            "_demand": "Спрос",
            "_supply": "Предложение",
            "maturity_bucket_label": "Срок обращения",
        },
    )
    fig.update_traces(textposition=data["scatter_textposition"].tolist(), textfont={"size": 9})
    fig.add_vline(x=1, line_dash="dash", line_color=HIGHLIGHT_COLORS["risk"])
    fig.add_annotation(
        text="Размер точки = объем размещения по номиналу",
        xref="paper",
        yref="paper",
        x=0,
        y=1.08,
        showarrow=False,
        align="left",
        font={"size": 12, "color": "#1F2933"},
    )
    fig.update_layout(xaxis_title=scatter_chart_policy.ratio_axis_title(ratio_column, x_axis_title), yaxis_title="Доходность")
    apply_common_layout(fig, legend_title="Срок обращения")
    export_columns = unique_columns(hover_columns + [ratio_column, "_yield", "_placement", "ratio_basis", "scatter_label", "scatter_label_reason"])
    return make_result("risk_quadrant", fig, data[export_columns], params)


def build_retrospective_risk_quadrant_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = ["report_period_label", "_yield", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"Ретроспективный квадрант риска пропущен: нет {', '.join(missing)}.")
        return None
    ratio_column, ratio_title, x_axis_title = select_demand_to_placement_ratio(df, limitations)
    if ratio_column is None:
        limitations.append("Ретроспективный квадрант риска пропущен: нет ratio спроса с данными.")
        return None
    data = df.dropna(subset=[ratio_column, "_yield"]).copy()
    if data.empty:
        limitations.append(f"Ретроспективный квадрант риска пропущен: нет строк с доходностью и `{ratio_column}`.")
        return None
    data = add_retrospective_risk_hover_and_labels(data, ratio_column)
    data = scatter_chart_policy.add_scatter_labels(
        data,
        ratio_column,
        "_yield",
        placement_column="_placement",
        yield_column="_yield",
        max_labels=MAX_SCATTER_LABELS,
    )
    data["ratio_basis"] = scatter_chart_policy.ratio_basis_for(ratio_column)
    assert px is not None
    period_labels = sorted(data["report_period_label"].dropna().astype(str).unique().tolist(), key=period_sort_key)
    period_color_map = palette.build_period_color_map(period_labels)
    fig = px.scatter(
        data,
        x=ratio_column,
        y="_yield",
        size="_placement",
        color="report_period_label",
        text="scatter_label",
        custom_data=[
            "Период",
            "Дата",
            "Код выпуска",
            "Тип ОФЗ",
            "Формат",
            "Спрос",
            "Размещение",
            "Предложение",
            "Спрос / размещение",
            "Спрос / предложение",
            "Доходность",
            "Объем размещения",
            "Сроковая категория",
            "scatter_label_reason",
            "ratio_basis",
        ],
        title=f"Ретроспективный квадрант риска: {ratio_title} и доходность",
        category_orders={"report_period_label": period_labels},
        color_discrete_map=period_color_map,
        color_discrete_sequence=QUALITATIVE_COLORS,
        labels={
            ratio_column: x_axis_title,
            "_demand_to_placement": "demand_to_placement_ratio",
            "_bid_to_cover": "bid_to_cover_ratio",
            "_yield": "Доходность",
            "_weighted_avg_yield": "Средневзвешенная доходность",
            "_cutoff_price": "Цена отсечения",
            "_weighted_avg_price": "Средневзвешенная цена",
            "_placement": "Объем размещения по номиналу",
            "_demand": "Спрос",
            "_supply": "Предложение",
            "report_period_label": "Период",
        },
    )
    fig.update_traces(
        textposition=data["scatter_textposition"].tolist(),
        textfont={"size": 9},
        hovertemplate=(
            "Период: %{customdata[0]}<br>"
            "Дата: %{customdata[1]}<br>"
            "Код выпуска: %{customdata[2]}<br>"
            "Тип ОФЗ: %{customdata[3]}<br>"
            "Формат: %{customdata[4]}<br>"
            "Спрос: %{customdata[5]}<br>"
            "Размещение: %{customdata[6]}<br>"
            "Предложение: %{customdata[7]}<br>"
            "Спрос / размещение: %{customdata[8]}<br>"
            "Спрос / предложение: %{customdata[9]}<br>"
            "Доходность: %{customdata[10]}<br>"
            "Объем размещения по номиналу: %{customdata[11]}<br>"
            "Сроковая категория: %{customdata[12]}<br>"
            "Причина подписи: %{customdata[13]}<br>"
            "Формула ratio: %{customdata[14]}"
            "<extra></extra>"
        ),
    )
    median_yield = data["_yield"].median(skipna=True)
    fig.add_vline(
        x=1,
        line_dash="dash",
        line_color=HIGHLIGHT_COLORS["risk"],
        annotation_text="Спрос равен размещению",
        annotation_position="top right",
    )
    if pd.notna(median_yield):
        fig.add_hline(
            y=float(median_yield),
            line_dash="dot",
            line_color=HIGHLIGHT_COLORS["warning"],
            annotation_text="Медианная доходность",
            annotation_position="bottom right",
        )
    fig.add_annotation(
        text="X: спрос / фактическое размещение; Y: доходность; Размер точки = объем размещения по номиналу",
        xref="paper",
        yref="paper",
        x=0,
        y=1.12,
        showarrow=False,
        align="left",
        font={"size": 12, "color": "#1F2933"},
    )
    y_axis_title = "Средневзвешенная доходность, % годовых"
    fig.update_layout(xaxis_title=scatter_chart_policy.ratio_axis_title(ratio_column, "Спрос / объем размещения"), yaxis_title=y_axis_title, margin={"l": 72, "r": 40, "t": 115, "b": 64})
    apply_common_layout(fig, legend_title="Период")
    limitations.append(
        "На ретроспективном квадранте риска по умолчанию подписываются только ключевые выбросы, "
        "чтобы избежать наложения подписей. Все остальные значения доступны через hover."
    )
    return make_result(
        "risk_quadrant_retrospective",
        fig,
        data[
            unique_columns(
                [
                    "report_period_label",
                    "auction_date",
                    "issue_code",
                    "ofz_type",
                    "format",
                    "maturity_bucket_label",
                    ratio_column,
                    "_bid_to_cover",
                    "_yield",
                    "_placement",
                    "ratio_basis",
                    "scatter_label",
                    "scatter_label_reason",
                ]
            )
        ],
        params,
    )


def build_report_year_demand_to_placement_risk_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = ["report_year", "auction_quarter", "_demand_to_placement", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"Квадрант риска отчетного года пропущен: нет {', '.join(missing)}.")
        return None
    y_column = "_weighted_avg_yield" if "_weighted_avg_yield" in df.columns and df["_weighted_avg_yield"].notna().any() else "_yield"
    if y_column not in df.columns or not df[y_column].notna().any():
        limitations.append("Квадрант риска отчетного года пропущен: нет валидной доходности.")
        return None
    y_axis_title = (
        "Средневзвешенная доходность, % годовых"
        if y_column == "_weighted_avg_yield"
        else "Доходность отсечения, % годовых"
        if y_column == "_cutoff_yield"
        else "Доходность, % годовых"
    )
    hover_y_title = (
        "Средневзвешенная доходность, %"
        if y_column == "_weighted_avg_yield"
        else "Доходность отсечения, %"
        if y_column == "_cutoff_yield"
        else "Доходность, %"
    )
    data = df.loc[df["report_year"].astype("Int64") == params.report_date.year].copy()
    data = data.dropna(subset=["_demand_to_placement", y_column, "_placement"])
    data = data.loc[data["_placement"] > 0]
    if data.empty:
        limitations.append("Квадрант риска отчетного года пропущен: нет строк с доходностью, спросом и положительным размещением.")
        return None
    data["_bid_to_cover"] = safe_divide_series(data["_demand"], data["_supply"])
    data["ratio_basis"] = scatter_chart_policy.ratio_basis_for("_demand_to_placement")
    quarter_count = int(data["auction_quarter"].dropna().nunique())
    if quarter_count <= 1:
        limitations.append(
            "В графике отчетного года цветовая детализация по кварталам может быть ограничена, если в выборке присутствует только один квартал."
        )
    auction_quarter = pd.to_numeric(data["auction_quarter"], errors="coerce")
    data["Квартал размещения"] = auction_quarter.map(lambda value: f"Q{int(value)}" if pd.notna(value) else "Не определен")
    data = add_report_year_risk_hover_and_labels(data, y_column)
    data = scatter_chart_policy.add_scatter_labels(
        data,
        "_demand_to_placement",
        y_column,
        placement_column="_placement",
        yield_column=y_column,
        max_labels=MAX_SCATTER_LABELS,
    )
    median_yield = data[y_column].median(skipna=True)
    custom_data = [
        "Код выпуска",
        "Дата размещения",
        "Отчетный период",
        "Квартал размещения",
        "Тип ОФЗ",
        "Формат",
        "Спрос, млн руб.",
        "Предложение, млн руб.",
        "Размещение, млн руб.",
        "Спрос / размещение",
        "Спрос / предложение",
        "Доходность",
        "Цена отсечения",
        "Сроковая категория",
        "scatter_label_reason",
        "ratio_basis",
    ]
    assert px is not None
    fig = px.scatter(
        data,
        x="_demand_to_placement",
        y=y_column,
        size="_placement",
        color="Квартал размещения",
        text="scatter_label",
        custom_data=custom_data,
        title="Квадрант риска: спрос к размещению и доходность, отчетный год",
        color_discrete_sequence=QUALITATIVE_COLORS,
        labels={
            "_demand_to_placement": "Спрос / объем размещения",
            y_column: y_axis_title,
            "_placement": "Объем размещения по номиналу",
            "Квартал размещения": "Квартал размещения",
        },
    )
    fig.update_traces(
        textfont={"size": 9},
        hovertemplate=(
            "Код выпуска: %{customdata[0]}<br>"
            "Дата размещения: %{customdata[1]}<br>"
            "Отчетный период: %{customdata[2]}<br>"
            "Квартал размещения: %{customdata[3]}<br>"
            "Тип ОФЗ: %{customdata[4]}<br>"
            "Формат: %{customdata[5]}<br>"
            "Спрос, млн руб.: %{customdata[6]}<br>"
            "Предложение, млн руб.: %{customdata[7]}<br>"
            "Размещение, млн руб.: %{customdata[8]}<br>"
            "Спрос / размещение: %{customdata[9]}<br>"
            "Спрос / предложение: %{customdata[10]}<br>"
            f"{hover_y_title}: %{{customdata[11]}}<br>"
            "Цена отсечения: %{customdata[12]}<br>"
            "Сроковая категория: %{customdata[13]}<br>"
            "Причина подписи: %{customdata[14]}<br>"
            "Формула ratio: %{customdata[15]}<extra></extra>"
        ),
    )
    for trace in fig.data:
        trace_name = str(getattr(trace, "name", ""))
        trace_data = data.loc[data["Квартал размещения"].astype("string") == trace_name]
        if not trace_data.empty:
            trace.update(textposition=trace_data["scatter_textposition"].tolist())
    fig.add_vline(
        x=1,
        line_dash="dash",
        line_color=HIGHLIGHT_COLORS["risk"],
        annotation_text="Спрос равен размещению",
        annotation_position="top right",
    )
    if pd.notna(median_yield):
        fig.add_hline(
            y=float(median_yield),
            line_dash="dot",
            line_color=HIGHLIGHT_COLORS["warning"],
            annotation_text="Медианная доходность отчетного года",
            annotation_position="bottom right",
        )
        limitations.append("В квадранте риска отчетного года горизонтальная линия показывает медианную доходность отчетного года.")
        add_report_year_risk_quadrant_annotations(fig, data, float(median_yield), y_column)
    fig.add_annotation(
        text="Размер пузыря — объем размещения по номиналу",
        xref="paper",
        yref="paper",
        x=0,
        y=1.08,
        showarrow=False,
        align="left",
        font={"size": 12, "color": QUALITATIVE_COLORS[4]},
    )
    fig.update_layout(xaxis_title=scatter_chart_policy.ratio_axis_title("_demand_to_placement"), yaxis_title=y_axis_title)
    apply_common_layout(fig, legend_title="Квартал размещения")
    limitations.append(
        "Квадрант риска отчетного года использует X = `demand_volume / placement_volume`; "
        "показатель `bid_to_cover_ratio` в подсказке пересчитывается как `demand_volume / supply_volume`."
    )
    export_columns = unique_columns(
        custom_data
        + ["_demand_to_placement", "_bid_to_cover", y_column, "_placement", "ratio_basis", "scatter_label", "scatter_label_reason"]
    )
    return make_result("risk_quadrant_demand_to_placement_by_quarter", fig, data[export_columns], params)


def add_report_year_risk_hover_and_labels(data: pd.DataFrame, y_column: str, top_n: int = 3) -> pd.DataFrame:
    result = data.copy()
    result["Код выпуска"] = result["issue_code"].astype("string") if "issue_code" in result.columns else ""
    result["Дата размещения"] = result["auction_date"].astype("string") if "auction_date" in result.columns else ""
    result["Отчетный период"] = result["report_period_label"].astype("string") if "report_period_label" in result.columns else ""
    result["Тип ОФЗ"] = result["ofz_type"].astype("string") if "ofz_type" in result.columns else ""
    result["Формат"] = result["format"].astype("string") if "format" in result.columns else ""
    result["Спрос, млн руб."] = result["_demand"].map(lambda value: format_hover_number(value, 1))
    result["Предложение, млн руб."] = result["_supply"].map(lambda value: format_hover_number(value, 1))
    result["Размещение, млн руб."] = result["_placement"].map(lambda value: format_hover_number(value, 1))
    result["Спрос / размещение"] = result["_demand_to_placement"].map(lambda value: format_hover_number(value, 3))
    result["Спрос / предложение"] = result["_bid_to_cover"].map(lambda value: format_hover_number(value, 3))
    result["Доходность"] = result[y_column].map(lambda value: format_hover_number(value, 2))
    result["Цена отсечения"] = result["_cutoff_price"].map(lambda value: format_hover_number(value, 2)) if "_cutoff_price" in result.columns else ""
    if "maturity_bucket_label" in result.columns:
        result["Сроковая категория"] = result["maturity_bucket_label"].astype("string")
    elif "maturity_bucket" in result.columns:
        result["Сроковая категория"] = result["maturity_bucket"].astype("string")
    else:
        result["Сроковая категория"] = ""

    label_indexes: set[Any] = set()
    label_indexes.update(pd.to_numeric(result["_demand_to_placement"], errors="coerce").nlargest(top_n).index.tolist())
    label_indexes.update(pd.to_numeric(result[y_column], errors="coerce").nlargest(top_n).index.tolist())
    label_indexes.update(pd.to_numeric(result[y_column], errors="coerce").nsmallest(top_n).index.tolist())
    label_indexes.update(pd.to_numeric(result["_placement"], errors="coerce").nlargest(top_n).index.tolist())

    median_yield = pd.to_numeric(result[y_column], errors="coerce").median()
    high_risk = result.loc[
        (pd.to_numeric(result["_demand_to_placement"], errors="coerce") > 2)
        & (pd.to_numeric(result[y_column], errors="coerce") > median_yield)
    ]
    label_indexes.update(high_risk.index.tolist())

    result["Подпись"] = ""
    for index in label_indexes:
        if index not in result.index:
            continue
        issue_code = str(result.at[index, "Код выпуска"]) if pd.notna(result.at[index, "Код выпуска"]) else ""
        ratio_value = pd.to_numeric(pd.Series([result.at[index, "_demand_to_placement"]]), errors="coerce").iloc[0]
        if issue_code:
            result.at[index, "Подпись"] = f"{issue_code}<br>x={format_hover_number(ratio_value, 2)}"

    x_median = pd.to_numeric(result["_demand_to_placement"], errors="coerce").median()
    y_median = pd.to_numeric(result[y_column], errors="coerce").median()
    result["Позиция подписи"] = "bottom right"
    high_x = pd.to_numeric(result["_demand_to_placement"], errors="coerce") >= x_median
    high_y = pd.to_numeric(result[y_column], errors="coerce") >= y_median
    result.loc[high_x & high_y, "Позиция подписи"] = "top left"
    result.loc[~high_x & high_y, "Позиция подписи"] = "top right"
    result.loc[high_x & ~high_y, "Позиция подписи"] = "bottom left"
    return result


def add_report_year_risk_quadrant_annotations(
    figure: Any,
    data: pd.DataFrame,
    median_yield: float,
    y_column: str,
) -> None:
    max_x = pd.to_numeric(data["_demand_to_placement"], errors="coerce").max()
    max_y = pd.to_numeric(data[y_column], errors="coerce").max()
    min_y = pd.to_numeric(data[y_column], errors="coerce").min()
    if pd.isna(max_x) or pd.isna(max_y) or pd.isna(min_y):
        return
    high_x = max(float(max_x) * 0.78, 1.08)
    high_y = float(median_yield + (float(max_y) - median_yield) * 0.62)
    low_y = float(float(min_y) + (median_yield - float(min_y)) * 0.38)
    for text, x_value, y_value in [
        ("Высокий спрос / высокая доходность", high_x, high_y),
        ("Высокий спрос / умеренная доходность", high_x, low_y),
    ]:
        figure.add_annotation(
            x=x_value,
            y=y_value,
            text=text,
            showarrow=False,
            bgcolor="rgba(255,255,255,0.78)",
            bordercolor="#90A7C8",
            borderwidth=1,
            font={"size": 11, "color": QUALITATIVE_COLORS[0]},
        )


def add_retrospective_risk_hover_and_labels(data: pd.DataFrame, ratio_column: str, top_n: int = 5) -> pd.DataFrame:
    result = data.copy()
    result["Период"] = result["report_period_label"].astype("string") if "report_period_label" in result.columns else ""
    result["Дата"] = result["auction_date"].astype("string") if "auction_date" in result.columns else ""
    result["Код выпуска"] = result["issue_code"].astype("string") if "issue_code" in result.columns else ""
    result["Тип ОФЗ"] = result["ofz_type"].astype("string") if "ofz_type" in result.columns else ""
    result["Формат"] = result["format"].astype("string") if "format" in result.columns else ""
    result["Спрос"] = result["_demand"].map(lambda value: format_hover_number(value, 1))
    result["Размещение"] = result["_placement"].map(lambda value: format_hover_number(value, 1))
    result["Предложение"] = result["_supply"].map(lambda value: format_hover_number(value, 1))
    result["Спрос / размещение"] = result[ratio_column].map(lambda value: format_hover_number(value, 3))
    result["Спрос / предложение"] = result["_bid_to_cover"].map(lambda value: format_hover_number(value, 3))
    result["Доходность"] = result["_yield"].map(lambda value: format_hover_number(value, 2))
    result["Объем размещения"] = result["_placement"].map(lambda value: format_hover_number(value, 1))
    if "maturity_bucket_label" in result.columns:
        result["Сроковая категория"] = result["maturity_bucket_label"].astype("string")
    elif "maturity_bucket" in result.columns:
        result["Сроковая категория"] = result["maturity_bucket"].astype("string")
    else:
        result["Сроковая категория"] = ""

    label_indexes: set[Any] = set()
    for column in [ratio_column, "_yield", "_placement"]:
        top = pd.to_numeric(result[column], errors="coerce").nlargest(top_n)
        label_indexes.update(top.index.tolist())

    for _, group in result.groupby("report_period_label", dropna=False):
        yields = pd.to_numeric(group["_yield"], errors="coerce").dropna()
        ratios = pd.to_numeric(group[ratio_column], errors="coerce").dropna()
        if not yields.empty:
            label_indexes.add(yields.idxmin())
            label_indexes.add(yields.idxmax())
        if not ratios.empty:
            label_indexes.add(ratios.idxmax())

    result["Подпись"] = ""
    for index in label_indexes:
        issue_code = str(result.at[index, "Код выпуска"]) if "Код выпуска" in result.columns else ""
        yield_value = pd.to_numeric(pd.Series([result.at[index, "_yield"]]), errors="coerce").iloc[0]
        result.at[index, "Подпись"] = f"{issue_code}<br>{yield_value:.2f}" if pd.notna(yield_value) else issue_code

    median_x = pd.to_numeric(result[ratio_column], errors="coerce").median()
    median_y = pd.to_numeric(result["_yield"], errors="coerce").median()
    result["Позиция подписи"] = "bottom right"
    high_x = pd.to_numeric(result[ratio_column], errors="coerce") >= median_x
    high_y = pd.to_numeric(result["_yield"], errors="coerce") >= median_y
    result.loc[high_x & high_y, "Позиция подписи"] = "top left"
    result.loc[~high_x & high_y, "Позиция подписи"] = "top right"
    result.loc[high_x & ~high_y, "Позиция подписи"] = "bottom left"
    return result


def period_sort_key(label: object) -> tuple[int, int, str]:
    text = str(label)
    match = re.search(r"(\d{4})-Q([1-4])", text)
    if match:
        return int(match.group(1)), int(match.group(2)), text
    year_match = re.search(r"(\d{4})", text)
    if year_match:
        return int(year_match.group(1)), 0, text
    return 0, 0, text


def build_yield_boxplot_by_ofz_type_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = ["ofz_type", "_yield"]
    if missing := missing_columns(df, required):
        limitations.append(f"Boxplot доходности по видам ОФЗ пропущен: нет {', '.join(missing)}.")
        return None
    data = df.dropna(subset=["ofz_type", "_yield"]).copy()
    if data.empty:
        limitations.append("Boxplot доходности по видам ОФЗ пропущен: нет строк с валидной доходностью.")
        return None
    data["yield_column_used"] = detect_yield_column_used(data)
    color_column = "report_period_label" if "report_period_label" in data.columns else "report_year"
    color_label = "Период" if color_column == "report_period_label" else "Год"
    if color_column in data.columns:
        data["Цвет периода"] = data[color_column].astype("string")
    else:
        data["Цвет периода"] = "Период не определен"
    data["Период boxplot"] = data["report_period_label"].astype("string") if "report_period_label" in data.columns else data["Цвет периода"]
    data["Период X boxplot"] = build_yield_boxplot_x_period(data)
    period_order = yield_boxplot_period_order(data, params)
    ofz_type_order = sorted(data["ofz_type"].dropna().astype(str).unique().tolist())
    ofz_type_to_x = {ofz_type: index for index, ofz_type in enumerate(ofz_type_order)}
    period_offsets = centered_float_offset_map(period_order, step=0.22, limit=0.32)
    data["x_base"] = data["ofz_type"].astype(str).map(ofz_type_to_x)
    data["period_offset"] = data["Период boxplot"].astype(str).map(period_offsets).fillna(0.0)
    data["x_group"] = data["x_base"] + data["period_offset"]
    chart_mode = "facet_by_ofz_type" if len(period_order) > 3 else "grouped_by_ofz_type"
    label_mode = "compact" if chart_mode == "facet_by_ofz_type" else "full"
    if "format" in data.columns and data["format"].dropna().nunique() > 1:
        limitations.append(
            "Boxplot доходности включает разные форматы размещения; формат доступен в tooltip и может влиять на интерпретацию."
        )
    data = mark_near_zero_floating_rate_yields(data, limitations)
    data = data.dropna(subset=["_yield"]).copy()
    if data.empty:
        limitations.append("Boxplot доходности пропущен: после проверки около-нулевых доходностей не осталось валидных наблюдений.")
        return None
    period_order = yield_boxplot_period_order(data, params)
    data["Период X boxplot"] = build_yield_boxplot_x_period(data)
    period_x_order = yield_boxplot_x_order(data, period_order)
    ofz_type_order = sorted(data["ofz_type"].dropna().astype(str).unique().tolist())
    ofz_type_to_x = {ofz_type: index for index, ofz_type in enumerate(ofz_type_order)}
    period_offsets = centered_float_offset_map(period_order, step=0.22, limit=0.32)
    data["x_base"] = data["ofz_type"].astype(str).map(ofz_type_to_x)
    data["period_offset"] = data["Период boxplot"].astype(str).map(period_offsets).fillna(0.0)
    data["x_group"] = data["x_base"] + data["period_offset"]
    chart_mode = "facet_by_ofz_type" if len(period_order) > 3 else "grouped_by_ofz_type"
    label_mode = "compact" if chart_mode == "facet_by_ofz_type" else "full"
    data["chart_mode"] = chart_mode
    data["label_mode"] = label_mode
    data = add_yield_boxplot_hover_columns(data)
    stats = build_yield_boxplot_stats(
        data,
        color_label,
        period_order,
        period_x_order,
        ofz_type_order,
        period_offsets,
        label_mode,
        chart_mode,
    )
    data = add_yield_boxplot_outlier_flags(data, stats)
    write_yield_boxplot_stats_export(stats, params)
    if not stats.empty and (stats["auction_count"] == 1).any():
        limitations.append("Boxplot доходности содержит группы с `n=1`; такие коробки не интерпретируются как распределение.")
    if not stats.empty and (stats["auction_count"] < 3).any():
        limitations.append("Boxplot доходности содержит группы с `n<3`; распределение статистически ограничено.")
    assert go is not None
    fig = go.Figure()
    period_color_map = palette.build_period_color_map(period_order)
    shown_periods: set[str] = set()
    for ofz_type in ofz_type_order:
        for period_label in period_order:
            group = data.loc[
                (data["ofz_type"].astype(str) == ofz_type)
                & (data["Период boxplot"].astype(str) == period_label)
            ].copy()
            if group.empty:
                continue
            custom_data = yield_boxplot_custom_data(group)
            fig.add_trace(
                go.Box(
                    x=group["x_group"],
                    y=group["_yield"],
                    name=period_label,
                    legendgroup=period_label,
                    showlegend=period_label not in shown_periods,
                    marker={"color": period_color_map.get(period_label, QUALITATIVE_COLORS[0]), "size": 5},
                    line={"color": period_color_map.get(period_label, QUALITATIVE_COLORS[0])},
                    fillcolor=hex_to_rgba(period_color_map.get(period_label, QUALITATIVE_COLORS[0]), 0.30),
                    boxpoints="all",
                    jitter=0.16,
                    pointpos=0,
                    width=0.16,
                    customdata=custom_data,
                    hovertemplate=yield_boxplot_hover_template(),
                )
            )
            shown_periods.add(period_label)
    add_yield_boxplot_compact_stat_trace(fig, stats)
    fig.add_annotation(
        text="Точки — отдельные размещения; коробка показывает межквартильный диапазон",
        xref="paper",
        yref="paper",
        x=0,
        y=1.12,
        showarrow=False,
        align="left",
        font={"size": 12, "color": "#1F2933"},
    )
    fig.update_layout(
        title="Распределение доходности ОФЗ-ПД",
        xaxis_title="Вид ОФЗ",
        yaxis_title="Доходность, % годовых",
        margin={"l": 72, "r": 72, "t": 120, "b": 92},
    )
    apply_common_layout(fig, legend_title=color_label)
    fig.update_xaxes(
        tickmode="array",
        tickvals=list(ofz_type_to_x.values()),
        ticktext=ofz_type_order,
        range=[-0.55, max(ofz_type_to_x.values(), default=0) + 0.55],
    )
    if chart_mode == "grouped_by_ofz_type":
        limitations.append(
            "Для короткого boxplot доходности используется grouped mode: на графике показаны min, med, max и n; "
            "q1, q3, lower fence и upper fence доступны в hover и `outputs/exports/chart_data/boxplot/yield_boxplot_stats_<...>.csv`."
        )
    if chart_mode == "facet_by_ofz_type":
        fig = build_yield_boxplot_facet_figure(
            data,
            stats,
            period_order,
            period_x_order,
            ofz_type_order,
            period_color_map,
        )
        limitations.append(
            "Boxplot доходности автоматически переключен в facet mode, потому что выбрано больше трех периодов; "
            "на графике показаны компактные подписи медианы и n, а полные статистики доступны в hover и export."
        )
    export_columns = unique_columns(
        [
            "report_period_label",
            "auction_date",
            "issue_code",
            "ofz_type",
            "format",
            "_yield",
            "placement_volume",
            "maturity_bucket",
            "x_base",
            "period_offset",
            "x_group",
            "Период X boxplot",
            "yield_column_used",
            "data_quality_flag",
            "chart_mode",
            "label_mode",
            "Цвет периода",
            "Предупреждение качества",
            "Признак выброса",
        ]
    )
    return make_result("yield_boxplot_by_ofz_type", fig, data[export_columns], params)


def build_yield_boxplot_ofz_pd_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Построить отдельный boxplot доходности только для ОФЗ-ПД."""
    required = ["ofz_type", "_yield"]
    if missing := missing_columns(df, required):
        limitations.append(f"Boxplot ОФЗ-ПД пропущен: нет {', '.join(missing)}.")
        return None
    mask = df["ofz_type"].fillna("").astype(str).str.upper().str.contains("ПД|PD", regex=True)
    data = df.loc[mask].dropna(subset=["_yield"]).copy()
    if data.empty:
        limitations.append("Boxplot ОФЗ-ПД пропущен: нет строк ОФЗ-ПД с валидной доходностью.")
        return None
    data["yield_column_used"] = detect_yield_column_used(data)
    data["Цвет периода"] = data["report_period_label"].astype("string") if "report_period_label" in data.columns else data["report_year"].astype("string")
    data["Период boxplot"] = data["report_period_label"].astype("string") if "report_period_label" in data.columns else data["Цвет периода"]
    data["Период X boxplot"] = build_yield_boxplot_x_period(data)
    period_order = yield_boxplot_period_order(data, params)
    single_period_mode = len(period_order) <= 2
    data["chart_mode"] = "ofz_pd_single_period_strip_box" if single_period_mode else "ofz_pd_period_boxplot"
    data["label_mode"] = "full"
    data = add_yield_boxplot_hover_columns(data)
    period_x_order = yield_boxplot_x_order(data, period_order)
    stats = build_yield_boxplot_ofz_pd_stats(data, period_order, period_x_order)
    if stats.empty:
        limitations.append("Boxplot ОФЗ-ПД пропущен: не удалось рассчитать статистики.")
        return None
    if single_period_mode:
        stats["chart_mode"] = "ofz_pd_single_period_strip_box"
    data = add_yield_boxplot_outlier_flags(data, stats)
    write_yield_boxplot_ofz_pd_stats_export(stats, params)

    assert go is not None
    fig = go.Figure()
    period_color_map = palette.build_period_color_map(period_order)
    if single_period_mode:
        for x_index, period_label in enumerate(period_order):
            group = data.loc[data["Период boxplot"].astype(str) == period_label].copy()
            period_stats = stats.loc[stats["report_period_label"].astype(str) == period_label].copy()
            if group.empty or period_stats.empty:
                continue
            add_yield_boxplot_ofz_pd_single_period_fallback(
                fig,
                group,
                period_stats,
                x_center=float(x_index),
                color=period_color_map.get(period_label, QUALITATIVE_COLORS[0]),
            )
        update_yield_boxplot_ofz_pd_single_period_yaxis(fig, data)
    else:
        for period_label in period_order:
            group = data.loc[data["Период boxplot"].astype(str) == period_label].copy()
            if group.empty:
                continue
            x_value = str(group["Период X boxplot"].iloc[0])
            fig.add_trace(
                go.Box(
                    x=[x_value] * len(group),
                    y=group["_yield"],
                    name=x_value,
                    marker={"color": period_color_map.get(period_label, QUALITATIVE_COLORS[0]), "size": 5},
                    line={"color": period_color_map.get(period_label, QUALITATIVE_COLORS[0])},
                    fillcolor=hex_to_rgba(period_color_map.get(period_label, QUALITATIVE_COLORS[0]), 0.30),
                    boxpoints="all",
                    jitter=0.18,
                    pointpos=0,
                    width=0.50,
                    customdata=yield_boxplot_custom_data(group),
                    hovertemplate=yield_boxplot_hover_template(),
                )
            )
        add_yield_boxplot_ofz_pd_stat_annotations(fig, stats)
        add_yield_boxplot_ofz_pd_stats_hover_trace(fig, stats)
    fig.add_annotation(
        text="ОФЗ-ПД: min/max подписаны у усов; q1/q3/fences/outliers доступны в hover и export",
        xref="paper",
        yref="paper",
        x=0,
        y=1.12,
        showarrow=False,
        align="left",
        font={"size": 12, "color": "#1F2933"},
    )
    fig.update_layout(
        title="Распределение доходности ОФЗ-ПД",
        xaxis_title="Период",
        yaxis_title="Доходность, % годовых",
        showlegend=False,
        margin={"l": 72, "r": 72, "t": 120, "b": 92},
    )
    if single_period_mode:
        tickvals = list(range(len(period_x_order)))
        fig.update_xaxes(tickmode="array", tickvals=tickvals, ticktext=period_x_order, range=[-0.72, max(tickvals) + 0.72])
    else:
        fig.update_xaxes(categoryorder="array", categoryarray=period_x_order)
    apply_common_layout(fig, legend_title="Период")
    limitations.append(
        "Создан отдельный boxplot ОФЗ-ПД: X = период, Y = доходность; на графике показаны min, median, max и n."
    )
    export_columns = unique_columns(
        [
            "report_period_label",
            "auction_date",
            "issue_code",
            "ofz_type",
            "format",
            "_yield",
            "placement_volume",
            "maturity_bucket",
            "yield_column_used",
            "data_quality_flag",
            "chart_mode",
            "label_mode",
            "Предупреждение качества",
            "Признак выброса",
        ]
    )
    return make_result("yield_boxplot_ofz_pd", fig, data[export_columns], params)


def build_demand_cutoff_explanation_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = ["_demand_to_placement", "_yield", "_demand", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"График отсечения спроса пропущен: нет {', '.join(missing)}.")
        return None
    data = filter_target_period_for_cutoff_chart(df, params, limitations)
    data = data.dropna(subset=["_demand_to_placement", "_yield", "_demand", "_placement"]).copy()
    data = data.loc[(data["_placement"] > 0) & (data["_demand"] > 0)]
    if data.empty:
        limitations.append(
            "График отсечения спроса пропущен: после фильтра целевого периода, аукционов, "
            "валидного спроса и положительного размещения строк не осталось."
        )
        return None
    if "_discount_to_nominal" in data.columns and data["_discount_to_nominal"].notna().any():
        y_column = "_discount_to_nominal"
        y_title = "Дисконт к номиналу, п.п."
        data = data.dropna(subset=[y_column]).copy()
        limitations.append("График отсечения спроса использует `discount_to_nominal = 100 - cutoff_price`.")
    elif "_cutoff_price" in data.columns and data["_cutoff_price"].notna().any():
        y_column = "_discount_to_nominal"
        y_title = "Дисконт к номиналу, п.п."
        data["_discount_to_nominal"] = 100 - data["_cutoff_price"]
        data = data.dropna(subset=[y_column]).copy()
        limitations.append("`discount_to_nominal` был рассчитан как `100 - cutoff_price` для целевого периода.")
    else:
        y_column = "_yield"
        y_title = "Доходность"
        limitations.append(
            "Цена отсечения отсутствует; невозможно анализировать дисконт как возможную причину неудовлетворения спроса. "
            "Построена fallback-визуализация кратности спроса к размещению и доходности."
        )
    if data.empty:
        limitations.append("График отсечения спроса пропущен: нет строк с валидным дисконтом или fallback-доходностью.")
        return None
    color_column = "_cutoff_yield" if "_cutoff_yield" in data.columns and data["_cutoff_yield"].notna().any() else "_weighted_avg_yield"
    colorbar_title = "Доходность, %"
    size_column = "_placement"
    data = add_cutoff_hover_and_labels(data, y_column, color_column)
    data = scatter_chart_policy.add_scatter_labels(
        data,
        "_demand_to_placement",
        y_column,
        placement_column="_placement",
        yield_column=color_column,
        max_labels=MAX_SCATTER_LABELS,
    )
    data["ratio_basis"] = scatter_chart_policy.ratio_basis_for("_demand_to_placement")
    data["x_value"] = data["_demand_to_placement"]
    data["y_value"] = data[y_column]
    data["bubble_size_value"] = data[size_column]
    data["placement_volume_bln"] = pd.to_numeric(data[size_column], errors="coerce") / 1000.0
    data["placement_volume_bln_label"] = data["placement_volume_bln"].map(lambda value: format_hover_number(value, 1))
    data["label_display"] = data["scatter_label"].fillna("").astype(str)
    data["label_visible"] = data["label_display"].str.strip().ne("")
    data["label_reason"] = data["scatter_label_reason"].fillna("").astype(str)
    if "data_quality_flag" not in data.columns:
        data["data_quality_flag"] = ""
    median_discount = data[y_column].median(skipna=True) if y_column == "_discount_to_nominal" else pd.NA
    assert px is not None
    fig = px.scatter(
        data,
        x="_demand_to_placement",
        y=y_column,
        size=size_column,
        size_max=42,
        color=color_column,
        text="scatter_label",
        custom_data=[
            "Дата",
            "Период",
            "Код выпуска",
            "Тип ОФЗ",
            "Формат",
            "Спрос",
            "Предложение",
            "Размещение",
            "Спрос / размещение",
            "Спрос / предложение",
            "Коэффициент удовлетворения спроса",
            "Цена отсечения",
            "Дисконт к номиналу",
            "Доходность отсечения",
            "Средневзвешенная доходность",
            "Сроковая категория",
            "scatter_label_reason",
            "ratio_basis",
            "placement_volume_bln_label",
            "data_quality_flag",
        ],
        title="Отсечение спроса: кратность спроса, дисконт и доходность",
        color_continuous_scale=CONTRAST_SEQUENTIAL_COLORS,
        labels={
            "_demand_to_placement": "Спрос / объем размещения",
            y_column: y_title,
            "_placement": "Объем размещения по номиналу",
            "_cutoff_yield": "Доходность отсечения",
            "_weighted_avg_yield": "Средневзвешенная доходность",
        },
    )
    fig.update_traces(
        textposition="top center",
        hovertemplate=(
            "<b>%{customdata[2]}</b><br>"
            "Дата: %{customdata[0]}<br>"
            "Период: %{customdata[1]}<br>"
            "Тип ОФЗ: %{customdata[3]}<br>"
            "Формат: %{customdata[4]}<br>"
            "Спрос: %{customdata[5]}<br>"
            "Предложение: %{customdata[6]}<br>"
            "Размещение: %{customdata[7]}<br>"
            "Объем размещения по номиналу, млрд рублей: %{customdata[18]}<br>"
            "Спрос / размещение: %{customdata[8]}<br>"
            "Спрос / предложение: %{customdata[9]}<br>"
            "Коэффициент удовлетворения спроса: %{customdata[10]}<br>"
            "Цена отсечения: %{customdata[11]}<br>"
            "Дисконт к номиналу: %{customdata[12]}<br>"
            "Доходность отсечения: %{customdata[13]}<br>"
            "Средневзвешенная доходность: %{customdata[14]}<br>"
            "Сроковая категория: %{customdata[15]}<br>"
            "Причина подписи: %{customdata[16]}<br>"
            "Формула ratio: %{customdata[17]}<br>"
            "Флаг качества данных: %{customdata[19]}"
            "<extra></extra>"
        ),
    )
    max_size = pd.to_numeric(data[size_column], errors="coerce").max()
    if pd.notna(max_size) and float(max_size) > 0:
        fig.update_traces(
            marker={
                "sizemode": "area",
                "sizeref": float(max_size) / (42.0**2),
                "sizemin": 6,
                "opacity": 0.78,
                "line": {"width": 0.6, "color": "rgba(31,41,51,0.35)"},
            }
        )
    fig.update_traces(textposition=data["scatter_textposition"].tolist(), textfont={"size": 9})
    fig.add_vline(
        x=1,
        line_dash="dash",
        line_color=HIGHLIGHT_COLORS["risk"],
        annotation_text="Спрос равен размещению",
        annotation_position="top right",
    )
    if pd.notna(median_discount):
        fig.add_hline(
            y=float(median_discount),
            line_dash="dot",
            line_color=HIGHLIGHT_COLORS["warning"],
            annotation_text="Медианный дисконт отчетного периода",
            annotation_position="bottom right",
        )
        add_cutoff_quadrant_annotations(fig, data, float(median_discount), y_column)
    fig.add_annotation(
        text=(
            "Только целевой отчетный период. X: спрос / размещение; "
            "Y: дисконт к номиналу; цвет: доходность; Размер точки = объем размещения по номиналу"
        ),
        xref="paper",
        yref="paper",
        x=0,
        y=1.12,
        showarrow=False,
        align="left",
        font={"size": 12, "color": "#1F2933"},
    )
    add_bubble_size_annotation(fig)
    fig.update_layout(xaxis_title="Спрос / объем размещения", yaxis_title=y_title)
    apply_common_layout(fig)
    fig.update_layout(
        showlegend=False,
        margin={"l": 80, "r": 170, "t": 120, "b": 72},
        coloraxis_colorbar={
            "title": colorbar_title,
            "x": 1.03,
            "y": 0.5,
            "len": 0.78,
            "thickness": 18,
        },
    )
    limitations.append(
        "График `demand_cutoff_explanation` строится только по целевому отчетному периоду, "
        "только по аукционам с валидным спросом и положительным размещением; ретроспективные периоды не включаются."
    )
    export_columns = unique_columns(
        [
            "auction_date",
            "report_period_label",
            "issue_code",
            "ofz_type",
            "format",
            "maturity_bucket",
            "_demand",
            "_supply",
            "_placement",
            "_demand_to_placement",
            "_bid_to_cover",
            "_demand_satisfaction",
            "_cutoff_price",
            "_discount_to_nominal",
            "_cutoff_yield",
            "_weighted_avg_yield",
            y_column,
            size_column,
            color_column,
            "ratio_basis",
            "scatter_label",
            "scatter_label_reason",
            "x_value",
            "y_value",
            "bubble_size_value",
            "placement_volume_bln",
            "label_display",
            "label_reason",
            "data_quality_flag",
        ]
    )
    return make_result("demand_cutoff_explanation", fig, data[export_columns], params)


def prepare_retrospective_risk_scatter_data(
    df: pd.DataFrame,
    limitations: list[str],
) -> tuple[pd.DataFrame, str | None, str]:
    """Подготовить данные ретроспективного risk scatter с единой политикой подписей."""
    ratio_column, ratio_title, _ = select_demand_to_placement_ratio(df, limitations)
    if ratio_column is None:
        return pd.DataFrame(), None, ratio_title
    data = df.dropna(subset=[ratio_column, "_yield"]).copy()
    if data.empty:
        return data, ratio_column, ratio_title
    data = add_retrospective_risk_hover_and_labels(data, ratio_column)
    data = scatter_chart_policy.add_scatter_labels(
        data,
        ratio_column,
        "_yield",
        placement_column="_placement",
        yield_column="_yield",
        max_labels=MAX_SCATTER_LABELS,
    )
    data["ratio_basis"] = scatter_chart_policy.ratio_basis_for(ratio_column)
    return data, ratio_column, ratio_title


def build_risk_quadrant_retrospective_outliers_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    data, ratio_column, ratio_title = prepare_retrospective_risk_scatter_data(df, limitations)
    if ratio_column is None or data.empty:
        limitations.append("Outliers-версия ретроспективного квадранта риска пропущена: нет данных.")
        return None
    data = scatter_chart_policy.outlier_subset(data)
    if data.empty:
        limitations.append("Outliers-версия ретроспективного квадранта риска пропущена: подписанные выбросы не найдены.")
        return None
    fig = build_policy_scatter_figure(
        data=data,
        x_column=ratio_column,
        y_column="_yield",
        color_column="report_period_label",
        title=f"Ретроспективный квадрант риска: выбросы ({ratio_title})",
        x_title=scatter_chart_policy.ratio_axis_title(ratio_column),
        y_title="Доходность, % годовых",
        legend_title="Период",
    )
    return make_result("risk_quadrant_retrospective_outliers", fig, scatter_export_data(data, ratio_column, "_yield"), params)


def build_risk_quadrant_retrospective_logx_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    data, ratio_column, ratio_title = prepare_retrospective_risk_scatter_data(df, limitations)
    if ratio_column is None or data.empty:
        limitations.append("Log-X версия ретроспективного квадранта риска пропущена: нет данных.")
        return None
    data = data.loc[pd.to_numeric(data[ratio_column], errors="coerce") > 0].copy()
    if data.empty:
        limitations.append("Log-X версия ретроспективного квадранта риска пропущена: нет положительных X.")
        return None
    fig = build_policy_scatter_figure(
        data=data,
        x_column=ratio_column,
        y_column="_yield",
        color_column="report_period_label",
        title=f"Ретроспективный квадрант риска: log-X ({ratio_title})",
        x_title=scatter_chart_policy.ratio_axis_title(ratio_column),
        y_title="Доходность, % годовых",
        legend_title="Период",
        log_x=True,
    )
    return make_result("risk_quadrant_retrospective_logx", fig, scatter_export_data(data, ratio_column, "_yield"), params)


def build_risk_quadrant_retrospective_facet_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    data, ratio_column, ratio_title = prepare_retrospective_risk_scatter_data(df, limitations)
    if ratio_column is None or data.empty or "report_period_label" not in data.columns:
        limitations.append("Facet-версия ретроспективного квадранта риска пропущена: нет периодов.")
        return None
    fig = build_policy_scatter_figure(
        data=data,
        x_column=ratio_column,
        y_column="_yield",
        color_column="report_period_label",
        title=f"Ретроспективный квадрант риска: small multiples ({ratio_title})",
        x_title=scatter_chart_policy.ratio_axis_title(ratio_column),
        y_title="Доходность, % годовых",
        legend_title="Период",
        facet_column="report_period_label",
    )
    return make_result("risk_quadrant_retrospective_facet", fig, scatter_export_data(data, ratio_column, "_yield"), params)


def build_yield_vs_demand_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = ["_demand", "_yield", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"График yield_vs_demand пропущен: нет {', '.join(missing)}.")
        return None
    data = df.dropna(subset=["_demand", "_yield"]).copy()
    if data.empty:
        limitations.append("График yield_vs_demand пропущен: нет спроса и доходности.")
        return None
    data = add_retrospective_risk_hover_and_labels(data, "_demand")
    data = scatter_chart_policy.add_scatter_labels(
        data,
        "_demand",
        "_yield",
        placement_column="_placement",
        yield_column="_yield",
        max_labels=MAX_SCATTER_LABELS,
    )
    fig = build_policy_scatter_figure(
        data=data,
        x_column="_demand",
        y_column="_yield",
        color_column="report_period_label" if "report_period_label" in data.columns else None,
        title="Доходность и спрос",
        x_title="Спрос, млн рублей",
        y_title="Доходность, % годовых",
        legend_title="Период",
    )
    return make_result("yield_vs_demand", fig, scatter_export_data(data, "_demand", "_yield"), params)


def _build_discount_vs_demand_chart_legacy(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    if "_discount_to_nominal" not in df.columns and "_cutoff_price" in df.columns:
        data = df.copy()
        data["_discount_to_nominal"] = 100 - data["_cutoff_price"]
    else:
        data = df.copy()
    required = ["_demand_to_placement", "_discount_to_nominal", "_placement"]
    if missing := missing_columns(data, required):
        limitations.append(f"График discount_vs_demand пропущен: нет {', '.join(missing)}.")
        return None
    data = data.dropna(subset=["_demand_to_placement", "_discount_to_nominal"]).copy()
    if data.empty:
        limitations.append("График discount_vs_demand пропущен: нет спроса и дисконта.")
        return None
    data = add_cutoff_hover_and_labels(data, "_discount_to_nominal", "_yield" if "_yield" in data.columns else "_discount_to_nominal")
    data = scatter_chart_policy.add_scatter_labels(
        data,
        "_demand_to_placement",
        "_discount_to_nominal",
        placement_column="_placement",
        yield_column="_yield" if "_yield" in data.columns else "_discount_to_nominal",
        max_labels=MAX_SCATTER_LABELS,
    )
    data["ratio_basis"] = scatter_chart_policy.ratio_basis_for("_demand_to_placement")
    fig = build_policy_scatter_figure(
        data=data,
        x_column="_demand_to_placement",
        y_column="_discount_to_nominal",
        color_column="report_period_label" if "report_period_label" in data.columns else None,
        title="Дисконт к номиналу и спрос",
        x_title=scatter_chart_policy.ratio_axis_title("_demand_to_placement"),
        y_title="Дисконт к номиналу, п.п.",
        legend_title="Период",
    )
    return make_result("discount_vs_demand", fig, scatter_export_data(data, "_demand_to_placement", "_discount_to_nominal"), params)


def prepare_discount_vs_demand_data(
    df: pd.DataFrame,
    limitations: list[str],
    *,
    append_missing_limitations: bool = True,
) -> pd.DataFrame:
    """Подготовить данные для dense scatter `discount_vs_demand`."""
    data = df.copy()
    if "_discount_to_nominal" not in data.columns and "_cutoff_price" in data.columns:
        data["_discount_to_nominal"] = 100 - data["_cutoff_price"]
    if "_revenue" not in data.columns:
        data["_revenue"] = resolve_numeric(data, ["revenue_volume", "proceeds_mln_rub", "revenue_amount_mln_rub"], "выручка от реализации", limitations)
    required = ["_demand_to_placement", "_discount_to_nominal", "_placement"]
    missing = missing_columns(data, required)
    if missing:
        if append_missing_limitations:
            limitations.append(f"График discount_vs_demand пропущен: нет {', '.join(missing)}.")
        return pd.DataFrame()
    data = data.dropna(subset=["_demand_to_placement", "_discount_to_nominal"]).copy()
    data = data.loc[pd.to_numeric(data["_placement"], errors="coerce").fillna(0) > 0]
    if data.empty:
        if append_missing_limitations:
            limitations.append("График discount_vs_demand пропущен: нет строк со спросом, дисконтом и положительным размещением.")
        return data
    data = add_cutoff_hover_and_labels(data, "_discount_to_nominal", "_yield" if "_yield" in data.columns else "_discount_to_nominal")
    data = scatter_chart_policy.add_scatter_labels(
        data,
        "_demand_to_placement",
        "_discount_to_nominal",
        placement_column="_placement",
        yield_column="_yield" if "_yield" in data.columns else "_discount_to_nominal",
        max_labels=MAX_SCATTER_LABELS,
    )
    data["ratio_basis"] = scatter_chart_policy.ratio_basis_for("_demand_to_placement")
    data["label_reason"] = data["scatter_label_reason"]
    data["x_value"] = data["_demand_to_placement"]
    data["y_value"] = data["_discount_to_nominal"]
    return data


def clip_dense_scatter_data(data: pd.DataFrame, x_column: str, y_column: str) -> pd.DataFrame:
    """Сформировать main clipped выборку: крайние значения остаются в outliers/log-X версиях."""
    result = data.copy()
    for column in (x_column, y_column):
        values = pd.to_numeric(result[column], errors="coerce").dropna()
        if len(values) < 8:
            continue
        lower = values.quantile(0.01)
        upper = values.quantile(0.99)
        result = result.loc[pd.to_numeric(result[column], errors="coerce").between(lower, upper, inclusive="both")]
    return result if not result.empty else data


def build_discount_vs_demand_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Main clipped версия плотного scatter: дисконт против спроса к размещению."""
    data = prepare_discount_vs_demand_data(df, limitations)
    if data.empty:
        return None
    clipped = clip_dense_scatter_data(data, "_demand_to_placement", "_discount_to_nominal")
    fig = build_policy_scatter_figure(
        data=clipped,
        x_column="_demand_to_placement",
        y_column="_discount_to_nominal",
        color_column="report_period_label" if "report_period_label" in clipped.columns else None,
        title="Дисконт к номиналу и спрос",
        x_title=scatter_chart_policy.ratio_axis_title("_demand_to_placement"),
        y_title="Дисконт к номиналу, п.п.",
        legend_title="Период",
        subtitle="Размер точки = объем размещения по номиналу; main clipped версия ограничивает крайние X/Y для читаемости.",
    )
    limitations.append(
        "Для `discount_vs_demand` используется scatter label policy: подписываются только выбросы, top placement_volume, top X/Y, target period и data_quality_flag; максимум подписей ограничен."
    )
    return make_result("discount_vs_demand", fig, scatter_export_data(data, "_demand_to_placement", "_discount_to_nominal"), params)


def build_discount_vs_demand_outliers_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Outliers-версия dense scatter."""
    data = prepare_discount_vs_demand_data(df, limitations, append_missing_limitations=False)
    outliers = scatter_chart_policy.outlier_subset(data)
    if outliers.empty:
        limitations.append("Outliers-версия discount_vs_demand пропущена: нет подписанных выбросов или проблемных точек.")
        return None
    fig = build_policy_scatter_figure(
        data=outliers,
        x_column="_demand_to_placement",
        y_column="_discount_to_nominal",
        color_column="report_period_label" if "report_period_label" in outliers.columns else None,
        title="Дисконт к номиналу и спрос: выбросы",
        x_title=scatter_chart_policy.ratio_axis_title("_demand_to_placement"),
        y_title="Дисконт к номиналу, п.п.",
        legend_title="Период",
        subtitle="Показаны только точки, выбранные scatter label policy.",
    )
    return make_result("discount_vs_demand_outliers", fig, scatter_export_data(outliers, "_demand_to_placement", "_discount_to_nominal"), params)


def build_discount_vs_demand_logx_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Log-X версия dense scatter."""
    data = prepare_discount_vs_demand_data(df, limitations, append_missing_limitations=False)
    data = data.loc[pd.to_numeric(data["_demand_to_placement"], errors="coerce") > 0].copy()
    if data.empty:
        limitations.append("Log-X версия discount_vs_demand пропущена: нет положительных значений X.")
        return None
    fig = build_policy_scatter_figure(
        data=data,
        x_column="_demand_to_placement",
        y_column="_discount_to_nominal",
        color_column="report_period_label" if "report_period_label" in data.columns else None,
        title="Дисконт к номиналу и спрос: log-X",
        x_title=scatter_chart_policy.ratio_axis_title("_demand_to_placement"),
        y_title="Дисконт к номиналу, п.п.",
        legend_title="Период",
        log_x=True,
        subtitle="Логарифмическая шкала X помогает читать плотные и асимметричные значения спроса к размещению.",
    )
    return make_result("discount_vs_demand_logx", fig, scatter_export_data(data, "_demand_to_placement", "_discount_to_nominal"), params)


def humanize_data_quality_flag(value: Any) -> str:
    """Перевести технический флаг качества данных в короткую русскую формулировку для hover."""
    text = "" if pd.isna(value) else str(value).strip()
    if not text or text.lower() in {"ok", "nan", "none"}:
        return "без специальных ограничений"
    lower = text.lower()
    labels: list[str] = []
    if "missing_demand" in lower or "no_demand" in lower:
        labels.append("нет данных о спросе")
    if "source_markers" in lower or "requires_review" in lower:
        demand_markers = ("demand", "bid_to_cover", "placement_ratio", "satisfaction")
        if any(marker in lower for marker in demand_markers):
            labels.append("требуется проверка спроса")
        else:
            labels.append("требуется проверка источника")
    if "missing_yield" in lower:
        labels.append("нет данных о доходности")
    if "zero_placement" in lower:
        labels.append("нулевое размещение")
    if "drpa" in lower:
        labels.append("ДРПА: спрос ограниченно сопоставим")
    if not labels:
        labels.append("требуется проверка данных")
    return "; ".join(dict.fromkeys(labels))


def humanize_scatter_label_reason(value: Any) -> str:
    """Перевести причины scatter label policy в понятные пользователю подписи."""
    text = "" if pd.isna(value) else str(value).strip()
    if not text:
        return ""
    mapping = {
        "x_outlier": "выброс по дисконту",
        "yield_outlier": "выброс по доходности",
        "zero_yield_check": "проверка около нулевой доходности",
        "top placement_volume": "крупное размещение",
        "top x_value": "высокий дисконт",
        "top y_value": "высокая доходность",
        "top_y_value": "высокая доходность",
        "top_discount": "высокий дисконт",
        "top_discount_to_nominal": "высокий дисконт",
        "top_yield": "высокая доходность",
        "top_placement": "крупное размещение",
        "top_placement_volume": "крупное размещение",
        "outlier": "выброс",
        "target_period": "отчетный период",
        "data_quality_flag": "есть ограничение качества данных",
    }
    parts = [humanize_scatter_label_reason_part(part.strip(), mapping) for part in text.split(";") if part.strip()]
    return "; ".join(dict.fromkeys(parts))


def humanize_scatter_label_reason_part(reason: str, mapping: dict[str, str]) -> str:
    """Вернуть безопасную русскую формулировку для одного технического токена причины подписи."""
    if reason in mapping:
        return mapping[reason]
    lower = reason.lower()
    if "missing_demand" in lower or "no_demand" in lower:
        return "нет данных о спросе"
    if "source_markers" in lower:
        if any(marker in lower for marker in ("demand", "bid_to_cover", "placement_ratio", "satisfaction")):
            return "требуется проверка спроса"
        return "требуется проверка источника"
    if "yield" in lower or "y_value" in lower:
        return "высокая доходность"
    if "discount" in lower or "x_value" in lower:
        return "высокий дисконт"
    if "placement" in lower or "volume" in lower:
        return "крупное размещение"
    if "data_quality" in lower or "requires_review" in lower:
        return "есть ограничение качества данных"
    if "outlier" in lower:
        return "выброс"
    return "причина подписи требует проверки"


def build_yield_discount_facet_labels(data: pd.DataFrame) -> pd.Series:
    """Сформировать человекочитаемые заголовки facet-панелей: год и диапазон месяцев."""
    if "report_year" not in data.columns:
        return pd.Series("", index=data.index, dtype="string")
    labels = data["report_year"].astype("string")
    if "auction_date" not in data.columns:
        return labels
    dates = pd.to_datetime(data["auction_date"], errors="coerce")
    month_names = {
        1: "янв",
        2: "фев",
        3: "мар",
        4: "апр",
        5: "май",
        6: "июн",
        7: "июл",
        8: "авг",
        9: "сен",
        10: "окт",
        11: "ноя",
        12: "дек",
    }
    result = pd.Series("", index=data.index, dtype="string")
    for year, indexes in data.groupby("report_year", dropna=False).groups.items():
        month_values = sorted(dates.loc[indexes].dropna().dt.month.unique().tolist())
        year_text = "" if pd.isna(year) else str(int(year))
        if month_values:
            start_label = month_names.get(int(month_values[0]), str(month_values[0]))
            end_label = month_names.get(int(month_values[-1]), str(month_values[-1]))
            result.loc[indexes] = f"{year_text}: {start_label}–{end_label}"
        else:
            result.loc[indexes] = year_text
    return result


def yield_discount_month_range_label(start_month: int, end_month: int) -> str:
    """Вернуть короткий русский диапазон месяцев для пометки неполного периода."""
    month_names = {
        1: "янв",
        2: "фев",
        3: "мар",
        4: "апр",
        5: "май",
        6: "июн",
        7: "июл",
        8: "авг",
        9: "сен",
        10: "окт",
        11: "ноя",
        12: "дек",
    }
    start_label = month_names.get(int(start_month), f"{int(start_month):02d}")
    end_label = month_names.get(int(end_month), f"{int(end_month):02d}")
    if start_label == end_label:
        return start_label
    return f"{start_label}–{end_label}"


def add_yield_discount_period_metadata(data: pd.DataFrame) -> pd.DataFrame:
    """Добавить месячный охват и флаг неполного периода для yield_vs_discount."""
    result = data.copy()
    dates = pd.to_datetime(result["auction_date"], errors="coerce") if "auction_date" in result.columns else pd.Series(pd.NaT, index=result.index)
    result["period_month_start"] = pd.NA
    result["period_month_end"] = pd.NA
    result["is_incomplete_period"] = False
    result["incomplete_period_reason"] = ""

    expected_start = (
        pd.to_datetime(result["report_period_start"], errors="coerce")
        if "report_period_start" in result.columns
        else pd.Series(pd.NaT, index=result.index)
    )
    expected_end = (
        pd.to_datetime(result["report_period_end"], errors="coerce")
        if "report_period_end" in result.columns
        else pd.Series(pd.NaT, index=result.index)
    )
    group_columns = [column for column in ["report_year", "report_period_label"] if column in result.columns]
    if not group_columns:
        group_columns = ["yield_vs_discount_facet"] if "yield_vs_discount_facet" in result.columns else []
    if not group_columns:
        return result

    for _, indexes in result.groupby(group_columns, dropna=False).groups.items():
        group_dates = dates.loc[indexes].dropna()
        if group_dates.empty:
            continue
        actual_start_month = int(group_dates.dt.month.min())
        actual_end_month = int(group_dates.dt.month.max())
        result.loc[indexes, "period_month_start"] = actual_start_month
        result.loc[indexes, "period_month_end"] = actual_end_month

        expected_start_month = expected_start.loc[indexes].dropna().dt.month.min()
        expected_end_month = expected_end.loc[indexes].dropna().dt.month.max()
        if pd.isna(expected_start_month) or pd.isna(expected_end_month):
            continue
        is_incomplete = actual_start_month > int(expected_start_month) or actual_end_month < int(expected_end_month)
        if is_incomplete:
            actual_text = yield_discount_month_range_label(actual_start_month, actual_end_month)
            result.loc[indexes, "is_incomplete_period"] = True
            result.loc[indexes, "incomplete_period_reason"] = (
                f"доступны данные только за {actual_text}"
            )
    return result


def apply_yield_vs_discount_facet_label_policy(data: pd.DataFrame) -> pd.DataFrame:
    """Ограничить подписи yield_vs_discount_facet: максимум 3 на панель и 15 всего."""
    return apply_yield_vs_discount_label_policy(data, mode="facet")


def apply_yield_vs_discount_label_policy(data: pd.DataFrame, *, mode: str) -> pd.DataFrame:
    """Единая политика подписей yield_vs_discount с сохранением скрытых кандидатов в CSV."""
    result = data.copy()
    candidates = build_yield_vs_discount_label_candidates(result, mode=mode)
    result["label_display"] = ""
    result["label_reason"] = ""
    for index, reasons in candidates.items():
        label = str(result.at[index, "issue_code"]) if "issue_code" in result.columns else str(index)
        result.at[index, "label_display"] = label
        result.at[index, "label_reason"] = "; ".join(sorted(reasons, key=yield_discount_reason_priority))
    result["label_reason_display"] = result["label_reason"].map(humanize_scatter_label_reason)

    if mode == "facet":
        selected = select_yield_discount_labels(
            result,
            candidates,
            total_limit=MAX_YIELD_DISCOUNT_FACET_LABELS_TOTAL,
            per_group_limit=MAX_YIELD_DISCOUNT_FACET_LABELS_PER_FACET,
            group_column="yield_vs_discount_facet" if "yield_vs_discount_facet" in result.columns else "report_year",
        )
    elif mode == "outliers":
        selected = select_yield_discount_labels(
            result,
            candidates,
            total_limit=MAX_YIELD_DISCOUNT_OUTLIERS_LABELS_TOTAL,
            per_group_limit=None,
            group_column=None,
        )
    else:
        selected = select_yield_discount_labels(
            result,
            candidates,
            total_limit=MAX_YIELD_DISCOUNT_MAIN_LABELS_TOTAL,
            per_group_limit=None,
            group_column=None,
        )

    result["scatter_label"] = ""
    result["scatter_label_reason"] = result["label_reason"]
    result["label_display"] = ""
    result["label_visible"] = False
    result.loc[list(candidates.keys()), "label_display"] = [
        str(result.at[index, "issue_code"]) if "issue_code" in result.columns else str(index)
        for index in candidates
    ]
    for index in selected:
        result.at[index, "scatter_label"] = result.at[index, "label_display"]
        result.at[index, "label_visible"] = True
    result["scatter_textposition"] = scatter_chart_policy.dynamic_text_positions(result, "_discount_to_nominal", "_yield")
    result["label_visible"] = result["label_visible"].fillna(False).astype(bool)
    if mode == "facet":
        result["median_discount"] = result["median_discount_period"]
        result["median_yield"] = result["median_yield_period"]
        result["median_scope"] = "period"
    elif "median_scope" not in result.columns:
        result["median_scope"] = "global"
    return result


def build_yield_vs_discount_label_candidates(data: pd.DataFrame, *, mode: str) -> dict[Any, set[str]]:
    """Собрать кандидатов на подписи с приоритетными причинами."""
    candidates: dict[Any, set[str]] = {}

    def add_reason(indexes: Sequence[Any], reason: str) -> None:
        for index in indexes:
            if index in data.index:
                candidates.setdefault(index, set()).add(reason)

    facet_column = "yield_vs_discount_facet" if "yield_vs_discount_facet" in data.columns else "report_year"
    groups = data.groupby(facet_column, dropna=False) if mode == "facet" and facet_column in data.columns else [(None, data)]
    for _, group in groups:
        add_reason(pd.to_numeric(group["_discount_to_nominal"], errors="coerce").nlargest(1).index.tolist(), "top_discount")
        add_reason(pd.to_numeric(group["_yield"], errors="coerce").nlargest(1).index.tolist(), "top_yield")
        add_reason(pd.to_numeric(group["placement_volume_bln"], errors="coerce").nlargest(1).index.tolist(), "top_placement")
        outlier_indexes = set(scatter_chart_policy.outlier_indexes(group["_discount_to_nominal"]))
        outlier_indexes.update(scatter_chart_policy.outlier_indexes(group["_yield"]))
        add_reason(list(outlier_indexes), "outlier")

        if "data_quality_flag" in group.columns:
            quality = group["data_quality_flag"].fillna("").astype(str).str.strip()
            flagged = quality.loc[quality.ne("") & quality.str.lower().ne("ok")]
            add_reason(flagged.index.tolist(), "data_quality_flag")

        if "is_target_period" in group.columns:
            target_mask = group["is_target_period"].astype("string").str.lower().isin({"true", "1", "yes"})
            target_group = group.loc[target_mask]
            if not target_group.empty:
                add_reason(pd.to_numeric(target_group["placement_volume_bln"], errors="coerce").nlargest(2).index.tolist(), "target_period")
    return candidates


def select_yield_discount_labels(
    data: pd.DataFrame,
    candidates: dict[Any, set[str]],
    *,
    total_limit: int,
    per_group_limit: int | None,
    group_column: str | None,
) -> list[Any]:
    """Выбрать видимые подписи с учетом приоритета и минимальной дистанции."""
    selected: list[Any] = []
    selected_by_group: dict[str, list[Any]] = {}
    ordered = sorted(
        candidates,
        key=lambda index: (
            yield_discount_candidate_priority(candidates[index]),
            -safe_numeric_value(data.at[index, "placement_volume_bln"]),
            -safe_numeric_value(data.at[index, "_yield"]),
            -safe_numeric_value(data.at[index, "_discount_to_nominal"]),
        ),
    )
    for index in ordered:
        if len(selected) >= total_limit:
            break
        group_key = str(data.at[index, group_column]) if group_column and group_column in data.columns else "__all__"
        group_selected = selected_by_group.setdefault(group_key, [])
        if per_group_limit is not None and len(group_selected) >= per_group_limit:
            continue
        if is_too_close_to_selected(data, index, group_selected if group_column else selected):
            continue
        selected.append(index)
        group_selected.append(index)
    return selected


def yield_discount_candidate_priority(reasons: set[str]) -> int:
    """Вернуть приоритет кандидата по лучшей причине подписи."""
    return min((yield_discount_reason_priority(reason) for reason in reasons), default=99)


def yield_discount_reason_priority(reason: str) -> int:
    """Порядок причин подписи: чем меньше число, тем выше приоритет."""
    order = {
        "data_quality_flag": 1,
        "top_yield": 2,
        "top_discount": 3,
        "top_placement": 4,
        "outlier": 5,
        "target_period": 6,
    }
    return order.get(reason, 99)


def is_too_close_to_selected(data: pd.DataFrame, index: Any, selected: Sequence[Any]) -> bool:
    """Проверить близость подписи к уже выбранным подписям в нормированных координатах."""
    if not selected:
        return False
    x_values = pd.to_numeric(data["_discount_to_nominal"], errors="coerce")
    y_values = pd.to_numeric(data["_yield"], errors="coerce")
    x_range = float(x_values.max() - x_values.min()) if x_values.notna().any() else 0.0
    y_range = float(y_values.max() - y_values.min()) if y_values.notna().any() else 0.0
    if x_range <= 0 or y_range <= 0:
        return False
    x = safe_numeric_value(data.at[index, "_discount_to_nominal"])
    y = safe_numeric_value(data.at[index, "_yield"])
    for selected_index in selected:
        sx = safe_numeric_value(data.at[selected_index, "_discount_to_nominal"])
        sy = safe_numeric_value(data.at[selected_index, "_yield"])
        distance = ((x - sx) / x_range) ** 2 + ((y - sy) / y_range) ** 2
        if distance**0.5 < YIELD_DISCOUNT_LABEL_MIN_DISTANCE_NORM:
            return True
    return False


def add_yield_discount_period_medians(data: pd.DataFrame) -> pd.DataFrame:
    """Добавить медианы дисконта и доходности по периоду/facet-панели."""
    result = data.copy()
    facet_column = "yield_vs_discount_facet" if "yield_vs_discount_facet" in result.columns else "report_period_label"
    if facet_column not in result.columns:
        result["median_discount_period"] = pd.NA
        result["median_yield_period"] = pd.NA
        result["median_scope"] = "period"
        return result
    result["median_discount_period"] = result.groupby(facet_column)["_discount_to_nominal"].transform("median")
    result["median_yield_period"] = result.groupby(facet_column)["_yield"].transform("median")
    result["median_scope"] = "period"
    return result


def safe_numeric_value(value: Any) -> float:
    """Вернуть число для сортировки; NaN считать минимальным."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return float("-inf")
    return float(numeric)


def prepare_yield_vs_discount_data(
    df: pd.DataFrame,
    limitations: list[str],
    *,
    append_missing_limitations: bool = True,
) -> pd.DataFrame:
    """Подготовить данные для квадранта доходности и дисконта без синтетического расчета дисконта."""
    data = df.copy()
    if "discount_to_nominal" not in data.columns:
        if append_missing_limitations:
            limitations.append(
                "График yield_vs_discount пропущен: в source dataset нет `discount_to_nominal`; дисконт не восстанавливается из цены отсечения."
            )
        return pd.DataFrame()
    data["_discount_to_nominal"] = pd.to_numeric(data["discount_to_nominal"], errors="coerce")
    required = ["_discount_to_nominal", "_yield", "_placement"]
    missing = missing_columns(data, required)
    if missing:
        if append_missing_limitations:
            limitations.append(f"График yield_vs_discount пропущен: нет {', '.join(missing)}.")
        return pd.DataFrame()

    data = data.dropna(subset=["_discount_to_nominal", "_yield", "_placement"]).copy()
    data = data.loc[pd.to_numeric(data["_placement"], errors="coerce").fillna(0) > 0]
    if data.empty:
        if append_missing_limitations:
            limitations.append(
                "График yield_vs_discount пропущен: нет строк с валидными discount_to_nominal, доходностью и положительным размещением."
            )
        return data

    if "data_quality_flag" not in data.columns:
        data["data_quality_flag"] = ""
    if "maturity_bucket_label" in data.columns and data["maturity_bucket_label"].notna().any():
        color_column = "maturity_bucket_label"
    elif "ofz_type" in data.columns:
        color_column = "ofz_type"
    else:
        data["Группа"] = "Все размещения"
        color_column = "Группа"
    data["yield_vs_discount_color"] = data[color_column].fillna("Требует проверки").astype("string")
    if "report_year" not in data.columns or data["report_year"].isna().all():
        if "auction_date" in data.columns:
            data["report_year"] = pd.to_datetime(data["auction_date"], errors="coerce").dt.year
        else:
            data["report_year"] = pd.NA
    data["report_year"] = pd.to_numeric(data["report_year"], errors="coerce").astype("Int64")
    data["yield_vs_discount_color"] = data["report_year"].astype("string").fillna("Год не указан")
    if "report_period_order" not in data.columns:
        year_order = {year: index for index, year in enumerate(sorted(data["yield_vs_discount_color"].dropna().unique()))}
        data["report_period_order"] = data["yield_vs_discount_color"].map(year_order).fillna(999).astype(int)
    data["yield_vs_discount_facet"] = build_yield_discount_facet_labels(data)
    data = add_yield_discount_period_metadata(data)
    data = add_placement_bln_columns(data, "_placement")
    data["bubble_size_value"] = pd.to_numeric(data["_placement"], errors="coerce")
    data["x_value"] = pd.to_numeric(data["_discount_to_nominal"], errors="coerce")
    data["y_value"] = pd.to_numeric(data["_yield"], errors="coerce")
    data = add_yield_discount_period_medians(data)
    data["median_discount"] = pd.to_numeric(data["_discount_to_nominal"], errors="coerce").median()
    data["median_yield"] = pd.to_numeric(data["_yield"], errors="coerce").median()
    data["median_scope"] = "global"
    data = apply_yield_vs_discount_label_policy(data, mode="main")
    data["data_quality_display"] = data["data_quality_flag"].map(humanize_data_quality_flag)
    incomplete_reason = data["incomplete_period_reason"].fillna("").astype(str)
    data.loc[incomplete_reason.str.strip().ne(""), "data_quality_display"] = (
        data.loc[incomplete_reason.str.strip().ne(""), "data_quality_display"].astype(str)
        + "; "
        + incomplete_reason.loc[incomplete_reason.str.strip().ne("")]
    )
    data["placement_volume_bln_label"] = data["placement_volume_bln"].map(lambda value: format_bln(value, suffix=True))
    data["demand_label"] = data["_demand"].map(lambda value: format_hover_number(value, 1)) if "_demand" in data.columns else ""
    data["supply_label"] = data["_supply"].map(lambda value: format_hover_number(value, 1)) if "_supply" in data.columns else ""
    data["demand_to_placement_label"] = (
        data["_demand_to_placement"].map(lambda value: format_hover_number(value, 3))
        if "_demand_to_placement" in data.columns
        else ""
    )
    data["bid_to_cover_label"] = (
        data["_bid_to_cover"].map(lambda value: format_hover_number(value, 3)) if "_bid_to_cover" in data.columns else ""
    )
    data["discount_label"] = data["_discount_to_nominal"].map(lambda value: format_hover_number(value, 2))
    data["yield_label"] = data["_yield"].map(lambda value: format_hover_number(value, 2))
    data["cutoff_price_label"] = (
        data["_cutoff_price"].map(lambda value: format_hover_number(value, 2)) if "_cutoff_price" in data.columns else ""
    )
    data["discount_to_nominal"] = data["_discount_to_nominal"]
    data["weighted_avg_yield"] = data["_yield"]
    data["demand_volume"] = data["_demand"] if "_demand" in data.columns else pd.NA
    data["supply_volume"] = data["_supply"] if "_supply" in data.columns else pd.NA
    data["demand_to_placement_ratio"] = data["_demand_to_placement"] if "_demand_to_placement" in data.columns else pd.NA
    data["bid_to_cover_ratio"] = data["_bid_to_cover"] if "_bid_to_cover" in data.columns else pd.NA
    data["maturity_label"] = (
        data["maturity_bucket_label"].fillna("Требует проверки").astype("string")
        if "maturity_bucket_label" in data.columns
        else ""
    )
    data["report_period_label"] = data["report_period_label"].astype("string") if "report_period_label" in data.columns else ""
    limitations.append(
        "График `yield_vs_discount` строится только по строкам с валидными `discount_to_nominal`, доходностью и положительным объемом размещения; дисконт не восстанавливается из цены отсечения."
    )
    return data


def build_yield_vs_discount_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Основной квадрант риска: дисконт к номиналу и доходность."""
    data = prepare_yield_vs_discount_data(df, limitations)
    if data.empty:
        return None
    fig = build_yield_vs_discount_figure(
        data=data,
        title="Квадрант риска: дисконт к номиналу и доходность",
        subtitle="Размер точки — объем размещения по номиналу",
        facet_column=None,
    )
    return make_result("yield_vs_discount", fig, yield_vs_discount_export_data(data), params)


def build_yield_vs_discount_outliers_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Версия квадранта доходность/дисконт только для подписанных выбросов и важных точек."""
    data = prepare_yield_vs_discount_data(df, limitations, append_missing_limitations=False)
    outliers = scatter_chart_policy.outlier_subset(data)
    if outliers.empty:
        limitations.append("Outliers-версия yield_vs_discount пропущена: нет точек, выбранных scatter label policy.")
        return None
    outliers = apply_yield_vs_discount_label_policy(outliers, mode="outliers")
    fig = build_yield_vs_discount_figure(
        data=outliers,
        title="Квадрант риска: дисконт к номиналу и доходность — выбросы",
        subtitle="Показаны точки с экстремальными значениями дисконта, доходности или объема размещения; размер точки — объем размещения по номиналу",
        facet_column=None,
    )
    return make_result("yield_vs_discount_outliers", fig, yield_vs_discount_export_data(outliers), params)


def build_yield_vs_discount_facet_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Facet-версия квадранта доходность/дисконт для длинной ретроспективы."""
    data = prepare_yield_vs_discount_data(df, limitations, append_missing_limitations=False)
    if data.empty or "report_period_label" not in data.columns:
        return None
    period_count = data["report_period_label"].dropna().astype(str).nunique()
    if period_count <= 3 and len(data) <= 80:
        limitations.append("Facet-версия yield_vs_discount пропущена: периодов мало и основной график остается читаемым.")
        return None
    data = apply_yield_vs_discount_facet_label_policy(data)
    fig = build_yield_vs_discount_figure(
        data=data,
        title="Квадрант риска: дисконт к номиналу и доходность — по периодам",
        subtitle="Пунктирные линии — медианы периода; размер точки — объем размещения по номиналу",
        facet_column="yield_vs_discount_facet",
    )
    return make_result("yield_vs_discount_facet", fig, yield_vs_discount_export_data(data), params)


def build_format_terms_aggregate_scatter_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Построить основной агрегированный scatter условий размещения по форматам."""
    data = prepare_format_terms_aggregate_scatter_data(df, params, limitations)
    if data.empty:
        limitations.append(
            "График `format_terms_aggregate_scatter` пропущен: нет агрегированных точек период × формат с валидными дисконтом, доходностью и объемом."
        )
        return None
    assert px is not None
    fig = px.scatter(
        data_frame=data,
        x="weighted_avg_discount_to_nominal",
        y="weighted_avg_yield",
        color="format",
        size="placement_volume_bln",
        size_max=52,
        text="label_text",
        custom_data=[
            "report_period_display",
            "format",
            "weighted_avg_discount_display",
            "weighted_avg_yield_display",
            "placement_volume_bln_display",
            "revenue_volume_bln_display",
            "nominal_revenue_gap_bln_display",
            "revenue_to_nominal_ratio_display",
            "placement_count",
            "aggregation_method_yield",
            "aggregation_method_discount",
            "data_quality_display",
        ],
        title=(
            "Средние условия размещения по форматам<br>"
            "<sup>Одна точка — формат размещения в периоде; размер точки — объем размещения по номиналу</sup>"
        ),
        color_discrete_map=FORMAT_COLOR_MAP,
        color_discrete_sequence=QUALITATIVE_COLORS,
        labels={
            "weighted_avg_discount_to_nominal": "Средневзвешенный дисконт к номиналу, п.п.",
            "weighted_avg_yield": "Средневзвешенная доходность размещения, % годовых",
            "placement_volume_bln": "Объем размещения по номиналу, млрд рублей",
            "format": "Формат",
        },
    )
    fig.update_traces(
        textposition="top center",
        textfont={"size": 10},
        marker={
            "sizemode": "area",
            "sizemin": 8,
            "opacity": 0.82,
            "line": {"width": 0.9, "color": "rgba(31,41,51,0.38)"},
        },
        hovertemplate=(
            "Период: %{customdata[0]}<br>"
            "Формат: %{customdata[1]}<br>"
            "Средневзвешенный дисконт, п.п.: %{customdata[2]}<br>"
            "Средневзвешенная доходность, % годовых: %{customdata[3]}<br>"
            "Объем размещения по номиналу, млрд рублей: %{customdata[4]}<br>"
            "Выручка, млрд рублей: %{customdata[5]}<br>"
            "Номинал минус выручка, млрд рублей: %{customdata[6]}<br>"
            "Выручка / номинал, %: %{customdata[7]}<br>"
            "Количество размещений формата: %{customdata[8]}<br>"
            "Метод агрегации доходности: %{customdata[9]}<br>"
            "Метод агрегации дисконта: %{customdata[10]}<br>"
            "Качество данных: %{customdata[11]}<extra></extra>"
        ),
    )
    median_discount = pd.to_numeric(data["weighted_avg_discount_to_nominal"], errors="coerce").median()
    median_yield = pd.to_numeric(data["weighted_avg_yield"], errors="coerce").median()
    if pd.notna(median_discount):
        fig.add_vline(
            x=float(median_discount),
            line_dash="dash",
            line_color="#7C3AED",
            annotation_text="мед. дисконт",
            annotation_position="top left",
        )
    if pd.notna(median_yield):
        fig.add_hline(
            y=float(median_yield),
            line_dash="dash",
            line_color="#059669",
            annotation_text="мед. доходность",
            annotation_position="bottom right",
        )
    add_bubble_size_annotation(fig)
    fig.update_layout(
        xaxis_title="Средневзвешенный дисконт к номиналу, п.п.",
        yaxis_title="Средневзвешенная доходность размещения, % годовых",
        margin={"l": 82, "r": 170, "t": 116, "b": 78},
    )
    apply_common_layout(fig, legend_title="Формат")
    limitations.append(
        "График `format_terms_aggregate_scatter` агрегирует строки до уровня report_period_label × format; доходность и дисконт считаются средневзвешенно по placement_volume."
    )
    return make_result("format_terms_aggregate_scatter", fig, format_terms_aggregate_scatter_export_data(data), params)


def prepare_format_terms_aggregate_scatter_data(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> pd.DataFrame:
    """Агрегировать условия размещения до уровня период × формат для основного scatter."""
    required = ["report_period_label", "format", "_discount_to_nominal", "_weighted_avg_yield", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"График `format_terms_aggregate_scatter` пропущен: нет {', '.join(missing)}.")
        return pd.DataFrame()
    data = df.dropna(subset=["report_period_label", "format"]).copy()
    data["format"] = data["format"].astype(str).str.strip()
    data = data[data["format"].isin(["Аукцион", "ДРПА"])].copy()
    if data.empty:
        return pd.DataFrame()

    revenue_column = first_existing_column(
        data,
        ["revenue_volume", "proceeds_volume", "placement_revenue", "proceeds_mln_rub"],
    )
    period_order_map = {
        str(period.get("label") or period.get("report_period_label")): int(index)
        for index, period in enumerate(params.periods, start=1)
    }
    period_display_map = {
        str(period.get("label") or period.get("report_period_label")): str(
            period.get("report_period_display_label")
            or period.get("display_label")
            or period.get("label")
            or period.get("report_period_label")
        )
        for period in params.periods
    }
    yield_source = "_weighted_avg_yield" if "_weighted_avg_yield" in data.columns else "_yield"
    yield_source_column = "weighted_avg_yield" if yield_source == "_weighted_avg_yield" else "yield"

    rows: list[dict[str, Any]] = []
    for (period_label, format_name), group in data.groupby(["report_period_label", "format"], dropna=False):
        placement = pd.to_numeric(group["_placement"], errors="coerce")
        placement_sum = placement.sum(min_count=1)
        revenue_values = (
            pd.to_numeric(group[revenue_column], errors="coerce")
            if revenue_column
            else pd.Series(pd.NA, index=group.index, dtype="Float64")
        )
        revenue_sum = revenue_values.sum(min_count=1)
        weighted_yield = weighted_average_or_na(group[yield_source], placement)
        weighted_discount = weighted_average_or_na(group["_discount_to_nominal"], placement)
        if pd.isna(weighted_yield) or pd.isna(weighted_discount) or pd.isna(placement_sum) or float(placement_sum) <= 0:
            continue
        gap = float(placement_sum) - float(revenue_sum) if pd.notna(revenue_sum) else pd.NA
        revenue_ratio = (
            float(revenue_sum) / float(placement_sum) * 100.0
            if pd.notna(revenue_sum) and float(placement_sum) > 0
            else pd.NA
        )
        period_label_str = str(period_label)
        placement_count = group_placement_count(group)
        data_quality_flag = combine_quality_flags(group["data_quality_flag"]) if "data_quality_flag" in group.columns else ""
        rows.append(
            {
                "report_period_label": period_label_str,
                "report_period_display_label": period_display_map.get(period_label_str, period_label_str),
                "report_period_order": period_order_map.get(period_label_str, pd.NA),
                "report_year": first_non_null(group, "report_year", pd.NA),
                "format": str(format_name),
                "weighted_avg_discount_to_nominal": weighted_discount,
                "weighted_avg_yield": weighted_yield,
                "placement_volume": float(placement_sum),
                "placement_volume_bln": float(placement_sum) / 1000.0,
                "revenue_volume": float(revenue_sum) if pd.notna(revenue_sum) else pd.NA,
                "revenue_volume_bln": float(revenue_sum) / 1000.0 if pd.notna(revenue_sum) else pd.NA,
                "nominal_revenue_gap_bln": float(gap) / 1000.0 if pd.notna(gap) else pd.NA,
                "revenue_to_nominal_ratio": revenue_ratio,
                "placement_count": placement_count,
                "aggregation_method_yield": "weighted_average_by_placement_volume",
                "source_column_yield": yield_source_column,
                "weight_field_yield": "placement_volume",
                "aggregation_method_discount": "weighted_average_by_placement_volume",
                "source_column_discount": "discount_to_nominal",
                "weight_field_discount": "placement_volume",
                "data_quality_flag": data_quality_flag,
                "data_quality_display": data_quality_display(data_quality_flag),
            }
        )
    result = pd.DataFrame(rows)
    if result.empty:
        return result
    result["_format_order"] = result["format"].map(format_stack_order)
    result = result.sort_values(["report_period_order", "_format_order", "format"]).copy()
    result["report_period_display"] = result["report_period_display_label"].fillna(result["report_period_label"]).astype(str)
    result["label_display"] = result["report_period_display"] + "<br>" + result["format"].astype(str)
    result["label_visible"] = choose_format_terms_aggregate_labels(result)
    result["label_text"] = result["label_display"].where(result["label_visible"], "")
    result["weighted_avg_discount_display"] = result["weighted_avg_discount_to_nominal"].map(lambda value: format_metric_value(value, 1))
    result["weighted_avg_yield_display"] = result["weighted_avg_yield"].map(lambda value: format_metric_value(value, 2))
    result["placement_volume_bln_display"] = result["placement_volume_bln"].map(lambda value: format_bln(value, suffix=True))
    result["revenue_volume_bln_display"] = result["revenue_volume_bln"].map(lambda value: format_bln(value, suffix=True))
    result["nominal_revenue_gap_bln_display"] = result["nominal_revenue_gap_bln"].map(lambda value: format_bln(value, suffix=True))
    result["revenue_to_nominal_ratio_display"] = result["revenue_to_nominal_ratio"].map(lambda value: format_metric_value(value, 1))
    return result


def choose_format_terms_aggregate_labels(data: pd.DataFrame) -> pd.Series:
    """Выбрать подписи агрегированных точек: все при малом числе, иначе отчетный период и экстремумы."""
    visible = pd.Series(False, index=data.index)
    if len(data) <= 14:
        visible.loc[:] = True
        return visible
    if "report_period_order" in data.columns and data["report_period_order"].notna().any():
        max_order = pd.to_numeric(data["report_period_order"], errors="coerce").max()
        visible |= pd.to_numeric(data["report_period_order"], errors="coerce").eq(max_order)
    for column in ["weighted_avg_discount_to_nominal", "weighted_avg_yield", "placement_volume_bln", "nominal_revenue_gap_bln"]:
        numeric = pd.to_numeric(data[column], errors="coerce")
        visible.loc[numeric.nlargest(2).index] = True
    return visible


def format_terms_aggregate_scatter_export_data(data: pd.DataFrame) -> pd.DataFrame:
    """Собрать CSV-контракт основного агрегированного scatter по форматам."""
    export_columns = [
        "report_period_label",
        "report_year",
        "format",
        "weighted_avg_discount_to_nominal",
        "weighted_avg_yield",
        "placement_volume_bln",
        "placement_volume_unit",
        "revenue_volume_bln",
        "revenue_volume_unit",
        "nominal_revenue_gap_bln",
        "nominal_revenue_gap_unit",
        "revenue_to_nominal_ratio",
        "placement_count",
        "aggregation_method_yield",
        "source_column_yield",
        "weight_field_yield",
        "aggregation_method_discount",
        "source_column_discount",
        "weight_field_discount",
        "label_display",
        "label_visible",
        "data_quality_flag",
        "data_quality_display",
    ]
    result = data.copy()
    result["placement_volume_unit"] = "млрд рублей"
    result["revenue_volume_unit"] = "млрд рублей"
    result["nominal_revenue_gap_unit"] = "млрд рублей"
    for column in export_columns:
        if column not in result.columns:
            result[column] = pd.NA
    return result[export_columns]


def build_format_terms_scatter_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Построить scatter условий отдельных размещений по форматам Аукцион / ДРПА."""
    data = prepare_format_terms_scatter_data(df, limitations)
    if data.empty:
        limitations.append(
            "График `format_terms_scatter` пропущен: нет строк с валидными дисконтом, доходностью и положительным объемом размещения."
        )
        return None
    assert px is not None
    symbol_column = "ofz_type" if "ofz_type" in data.columns else None
    kwargs: dict[str, Any] = {
        "data_frame": data,
        "x": "discount_to_nominal",
        "y": "weighted_avg_yield",
        "color": "format",
        "size": "placement_volume_bln",
        "size_max": 44,
        "text": "label_text",
        "custom_data": [
            "issue_code_display",
            "auction_date_display",
            "report_year_display",
            "report_period_display",
            "format_display",
            "ofz_type_display",
            "maturity_bucket_display",
            "yield_display",
            "discount_display",
            "cutoff_price_display",
            "placement_volume_bln_display",
            "revenue_volume_bln_display",
            "nominal_revenue_gap_bln_display",
            "revenue_to_nominal_ratio_display",
            "demand_to_placement_display",
            "data_quality_display",
            "label_reason_display",
        ],
        "title": "Условия размещения ОФЗ по форматам<br><sup>Цвет — формат; форма — вид ОФЗ; размер — объем размещения по номиналу</sup>",
        "color_discrete_map": FORMAT_COLOR_MAP,
        "color_discrete_sequence": QUALITATIVE_COLORS,
        "labels": {
            "discount_to_nominal": "Дисконт к номиналу, п.п.",
            "weighted_avg_yield": "Средневзвешенная доходность размещения, % годовых",
            "placement_volume_bln": "Объем размещения по номиналу, млрд рублей",
            "format": "Формат",
            "ofz_type": "Вид ОФЗ",
        },
    }
    if symbol_column:
        kwargs["symbol"] = symbol_column
    fig = px.scatter(**kwargs)
    fig.update_traces(
        textposition="top center",
        textfont={"size": 9},
        marker={
            "sizemode": "area",
            "sizemin": 6,
            "opacity": 0.78,
            "line": {"width": 0.7, "color": "rgba(31,41,51,0.35)"},
        },
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Дата размещения: %{customdata[1]}<br>"
            "Год: %{customdata[2]}<br>"
            "Период: %{customdata[3]}<br>"
            "Формат: %{customdata[4]}<br>"
            "Вид ОФЗ: %{customdata[5]}<br>"
            "Сроковая категория: %{customdata[6]}<br>"
            "Средневзвешенная доходность размещения, % годовых: %{customdata[7]}<br>"
            "Дисконт к номиналу, п.п.: %{customdata[8]}<br>"
            "Цена отсечения: %{customdata[9]}<br>"
            "Объем размещения по номиналу, млрд рублей: %{customdata[10]}<br>"
            "Выручка, млрд рублей: %{customdata[11]}<br>"
            "Номинал минус выручка, млрд рублей: %{customdata[12]}<br>"
            "Выручка / номинал, %: %{customdata[13]}<br>"
            "Спрос / объем размещения: %{customdata[14]}<br>"
            "Качество данных: %{customdata[15]}<br>"
            "Причина подписи: %{customdata[16]}<extra></extra>"
        ),
    )
    add_bubble_size_annotation(fig)
    fig.update_layout(
        xaxis_title="Дисконт к номиналу, п.п.",
        yaxis_title="Средневзвешенная доходность размещения, % годовых",
        margin={"l": 78, "r": 170, "t": 112, "b": 72},
    )
    apply_common_layout(fig, legend_title="Формат")
    limitations.append(
        "График `format_terms_scatter` показывает отдельные размещения; подписи ограничены MAX_LABELS_TOTAL=25, остальные детали доступны в hover и CSV."
    )
    return make_result("format_terms_scatter", fig, format_terms_scatter_export_data(data), params)


def prepare_format_terms_scatter_data(df: pd.DataFrame, limitations: list[str]) -> pd.DataFrame:
    """Подготовить строки размещений для scatter условий по форматам."""
    required = ["format", "_discount_to_nominal", "_weighted_avg_yield", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"График `format_terms_scatter` пропущен: нет {', '.join(missing)}.")
        return pd.DataFrame()
    data = df.dropna(subset=["format", "_discount_to_nominal", "_weighted_avg_yield", "_placement"]).copy()
    data = data.loc[pd.to_numeric(data["_placement"], errors="coerce") > 0].copy()
    if data.empty:
        return data
    revenue_column = first_existing_column(
        data,
        ["revenue_volume", "proceeds_volume", "placement_revenue", "proceeds_mln_rub"],
    )
    data["revenue_volume"] = pd.to_numeric(data[revenue_column], errors="coerce") if revenue_column else pd.NA
    data["revenue_volume_bln"] = pd.to_numeric(data["revenue_volume"], errors="coerce") / 1000.0
    data["nominal_revenue_gap"] = pd.to_numeric(data["_placement"], errors="coerce") - pd.to_numeric(data["revenue_volume"], errors="coerce")
    data["nominal_revenue_gap_bln"] = data["nominal_revenue_gap"] / 1000.0
    data["placement_volume"] = pd.to_numeric(data["_placement"], errors="coerce")
    data["placement_volume_bln"] = data["placement_volume"] / 1000.0
    data["revenue_to_nominal_ratio"] = safe_divide_series(data["revenue_volume"], data["placement_volume"]) * 100.0
    data["bubble_size_value"] = data["placement_volume_bln"]
    data["discount_to_nominal"] = pd.to_numeric(data["_discount_to_nominal"], errors="coerce")
    data["weighted_avg_yield"] = pd.to_numeric(data["_weighted_avg_yield"], errors="coerce")
    data["yield_value"] = data["weighted_avg_yield"]
    data["yield_metric_name_ru"] = "Средневзвешенная доходность размещения, % годовых"
    data["source_column_yield"] = "weighted_avg_yield"
    data["aggregation_method_yield"] = "row_level_value"
    data["weight_field_yield"] = ""
    data["demand_to_placement_ratio"] = pd.to_numeric(data["_demand_to_placement"], errors="coerce") if "_demand_to_placement" in data.columns else pd.NA
    data["bid_to_cover_ratio"] = pd.to_numeric(data["_bid_to_cover"], errors="coerce") if "_bid_to_cover" in data.columns else pd.NA
    data["cutoff_price"] = pd.to_numeric(data["_cutoff_price"], errors="coerce") if "_cutoff_price" in data.columns else pd.NA
    if "data_quality_flag" not in data.columns:
        data["data_quality_flag"] = ""
    data["data_quality_display"] = data["data_quality_flag"].map(data_quality_display)
    data["label_reason"] = build_format_terms_scatter_label_reasons(data)
    data["label_reason_display"] = data["label_reason"].map(format_terms_label_reason_display)
    data["label_display"] = data["issue_code"].fillna("").astype(str) if "issue_code" in data.columns else ""
    data.loc[data["label_display"].str.lower().eq("nan"), "label_display"] = ""
    data = apply_format_terms_scatter_label_policy(data)
    data["label_text"] = data["label_display"].where(data["label_visible"], "")
    data["issue_code_display"] = data["issue_code"].fillna("").astype(str) if "issue_code" in data.columns else ""
    data["auction_date_display"] = data["auction_date"].fillna("").astype(str) if "auction_date" in data.columns else ""
    data["report_year_display"] = data["report_year"].fillna("").astype(str) if "report_year" in data.columns else ""
    if "report_period_display_label" in data.columns:
        data["report_period_display"] = data["report_period_display_label"].fillna(data["report_period_label"]).astype(str)
    else:
        data["report_period_display"] = data["report_period_label"].fillna("").astype(str)
    data["format_display"] = data["format"].fillna("").astype(str)
    data["ofz_type_display"] = data["ofz_type"].fillna("").astype(str) if "ofz_type" in data.columns else ""
    data["maturity_bucket_display"] = data["maturity_bucket_label"].fillna("").astype(str) if "maturity_bucket_label" in data.columns else ""
    data["yield_display"] = data["weighted_avg_yield"].map(lambda value: format_metric_value(value, 2))
    data["discount_display"] = data["discount_to_nominal"].map(lambda value: format_metric_value(value, 1))
    data["cutoff_price_display"] = data["cutoff_price"].map(lambda value: format_metric_value(value, 2))
    data["placement_volume_bln_display"] = data["placement_volume_bln"].map(lambda value: format_bln(value, suffix=True))
    data["revenue_volume_bln_display"] = data["revenue_volume_bln"].map(lambda value: format_bln(value, suffix=True))
    data["nominal_revenue_gap_bln_display"] = data["nominal_revenue_gap_bln"].map(lambda value: format_bln(value, suffix=True))
    data["revenue_to_nominal_ratio_display"] = data["revenue_to_nominal_ratio"].map(lambda value: format_metric_value(value, 1))
    data["demand_to_placement_display"] = data["demand_to_placement_ratio"].map(lambda value: format_metric_value(value, 2))
    data["x_value"] = data["discount_to_nominal"]
    data["y_value"] = data["weighted_avg_yield"]
    return data


def build_format_terms_scatter_label_reasons(data: pd.DataFrame) -> pd.Series:
    """Вернуть причины-кандидаты для подписей format_terms_scatter."""
    reasons = pd.Series("", index=data.index, dtype="object")
    for reason, column in [
        ("top_discount", "discount_to_nominal"),
        ("top_yield", "weighted_avg_yield"),
        ("top_nominal_revenue_gap", "nominal_revenue_gap_bln"),
        ("top_placement_volume", "placement_volume_bln"),
    ]:
        numeric = pd.to_numeric(data[column], errors="coerce")
        for index in numeric.nlargest(5).index:
            current = str(reasons.at[index]).strip()
            reasons.at[index] = ";".join(part for part in [current, reason] if part)
    if "data_quality_flag" in data.columns:
        quality = data["data_quality_flag"].fillna("").astype(str)
        quality_mask = quality.str.strip().ne("") & ~quality.str.lower().eq("ok")
        for index in data.loc[quality_mask].index:
            current = str(reasons.at[index]).strip()
            reasons.at[index] = ";".join(part for part in [current, "data_quality_flag"] if part)
    if "is_target_period" in data.columns:
        target_mask = data["is_target_period"].fillna(False).astype(bool)
        for index in data.loc[target_mask].index:
            current = str(reasons.at[index]).strip()
            reasons.at[index] = ";".join(part for part in [current, "target_period"] if part)
    return reasons


def apply_format_terms_scatter_label_policy(data: pd.DataFrame) -> pd.DataFrame:
    """Ограничить подписи format_terms_scatter до 25 видимых точек с дистанцией между labels."""
    result = data.copy()
    result["label_visible"] = False
    priorities = {
        "data_quality_flag": 1,
        "top_yield": 2,
        "top_discount": 3,
        "top_nominal_revenue_gap": 4,
        "top_placement_volume": 5,
        "target_period": 6,
    }
    candidates = result.loc[result["label_reason"].fillna("").astype(str).str.strip().ne("")].copy()
    if candidates.empty:
        return result
    candidates["_label_priority"] = candidates["label_reason"].map(
        lambda value: min((priorities.get(part.strip(), 99) for part in str(value).split(";") if part.strip()), default=99)
    )
    candidates["_label_score"] = (
        pd.to_numeric(candidates["discount_to_nominal"], errors="coerce").rank(ascending=False).fillna(999)
        + pd.to_numeric(candidates["weighted_avg_yield"], errors="coerce").rank(ascending=False).fillna(999)
        + pd.to_numeric(candidates["placement_volume_bln"], errors="coerce").rank(ascending=False).fillna(999)
    )
    x_values = pd.to_numeric(result["discount_to_nominal"], errors="coerce")
    y_values = pd.to_numeric(result["weighted_avg_yield"], errors="coerce")
    x_range = float(x_values.max() - x_values.min()) if x_values.notna().any() else 0.0
    y_range = float(y_values.max() - y_values.min()) if y_values.notna().any() else 0.0
    selected_points: list[tuple[float, float]] = []
    for index, row in candidates.sort_values(["_label_priority", "_label_score"]).iterrows():
        if len(selected_points) >= 25:
            break
        x_value = pd.to_numeric(pd.Series([row.get("discount_to_nominal")]), errors="coerce").iloc[0]
        y_value = pd.to_numeric(pd.Series([row.get("weighted_avg_yield")]), errors="coerce").iloc[0]
        if pd.isna(x_value) or pd.isna(y_value):
            continue
        x_norm = 0.5 if x_range <= 0 else (float(x_value) - float(x_values.min())) / x_range
        y_norm = 0.5 if y_range <= 0 else (float(y_value) - float(y_values.min())) / y_range
        too_close = any(((x_norm - prev_x) ** 2 + (y_norm - prev_y) ** 2) ** 0.5 < 0.07 for prev_x, prev_y in selected_points)
        if too_close and "data_quality_flag" not in str(row.get("label_reason", "")):
            continue
        result.at[index, "label_visible"] = True
        selected_points.append((x_norm, y_norm))
    return result


def format_terms_label_reason_display(value: Any) -> str:
    """Перевести причины подписи format_terms_scatter в русский аналитический вид."""
    mapping = {
        "top_discount": "высокий дисконт",
        "top_yield": "высокая доходность",
        "top_nominal_revenue_gap": "крупная разница номинала и выручки",
        "top_placement": "крупное размещение",
        "top_placement_volume": "крупное размещение",
        "data_quality_flag": "требуется проверка качества данных",
        "target_period": "отчетный период",
    }
    parts = [mapping.get(part.strip(), part.strip()) for part in str(value).split(";") if part.strip()]
    return "; ".join(dict.fromkeys(parts))


def format_terms_scatter_export_data(data: pd.DataFrame) -> pd.DataFrame:
    """Собрать CSV-контракт format_terms_scatter."""
    result = data.copy()
    if "demand_volume" not in result.columns:
        result["demand_volume"] = result["_demand"] if "_demand" in result.columns else pd.NA
    if "supply_volume" not in result.columns:
        result["supply_volume"] = result["_supply"] if "_supply" in result.columns else pd.NA
    export_columns = [
        "report_year",
        "report_period_label",
        "report_period_display_label",
        "auction_date",
        "issue_code",
        "format",
        "ofz_type",
        "maturity_bucket",
        "maturity_bucket_label",
        "discount_to_nominal",
        "weighted_avg_yield",
        "yield_value",
        "yield_metric_name_ru",
        "source_column_yield",
        "aggregation_method_yield",
        "weight_field_yield",
        "cutoff_price",
        "placement_volume",
        "placement_volume_bln",
        "revenue_volume",
        "revenue_volume_bln",
        "nominal_revenue_gap",
        "nominal_revenue_gap_bln",
        "revenue_to_nominal_ratio",
        "demand_volume",
        "supply_volume",
        "demand_to_placement_ratio",
        "bid_to_cover_ratio",
        "x_value",
        "y_value",
        "bubble_size_value",
        "label_display",
        "label_visible",
        "label_reason",
        "label_reason_display",
        "data_quality_flag",
        "data_quality_display",
    ]
    for column in export_columns:
        if column not in result.columns:
            result[column] = pd.NA
    return result[export_columns]


def build_yield_vs_discount_figure(
    data: pd.DataFrame,
    title: str,
    subtitle: str,
    *,
    facet_column: str | None,
) -> Any:
    """Построить scatter-квадрант доходность/дисконт с единым hover и reference lines."""
    assert px is not None
    custom_data = [
        "report_year",
        "issue_code",
        "auction_date",
        "report_period_label",
        "ofz_type",
        "format",
        "maturity_label",
        "discount_label",
        "yield_label",
        "cutoff_price_label",
        "placement_volume_bln_label",
        "demand_label",
        "supply_label",
        "demand_to_placement_label",
        "bid_to_cover_label",
        "data_quality_display",
        "label_reason_display",
    ]
    for column in custom_data:
        if column not in data.columns:
            data[column] = ""
    kwargs: dict[str, Any] = {
        "data_frame": data,
        "x": "_discount_to_nominal",
        "y": "_yield",
        "size": "placement_volume_bln",
        "size_max": 42,
        "color": "yield_vs_discount_color",
        "text": "scatter_label",
        "title": title,
        "labels": {
            "_discount_to_nominal": "Дисконт к номиналу, п.п.",
            "_yield": "Доходность, % годовых",
            "_placement": "Объем размещения по номиналу",
            "yield_vs_discount_color": "Год",
            "report_period_label": "Период",
            "yield_vs_discount_facet": "Период",
        },
        "custom_data": custom_data,
        "color_discrete_sequence": QUALITATIVE_COLORS,
    }
    years = sorted(data["yield_vs_discount_color"].dropna().astype(str).unique().tolist())
    kwargs["category_orders"] = {"yield_vs_discount_color": years}
    kwargs["color_discrete_map"] = palette.build_period_color_map(years)
    if facet_column:
        facet_order = data[[facet_column, "report_period_order"]].drop_duplicates()
        facet_order = facet_order.sort_values("report_period_order")[facet_column].astype(str).tolist()
        kwargs["category_orders"][facet_column] = facet_order
        kwargs["facet_col"] = facet_column
        kwargs["facet_col_wrap"] = 3
    fig = px.scatter(**kwargs)
    max_size = pd.to_numeric(data["_placement"], errors="coerce").max()
    if pd.notna(max_size) and float(max_size) > 0:
        fig.update_traces(
            marker={
                "sizemode": "area",
                "sizeref": float(max_size) / (42.0**2),
                "sizemin": 6,
                "opacity": 0.78,
                "line": {"width": 0.6, "color": "rgba(31,41,51,0.35)"},
            }
        )
    fig.update_traces(
        textposition=data["scatter_textposition"].tolist() if "scatter_textposition" in data.columns else "top center",
        textfont={"size": 9},
        hovertemplate=yield_vs_discount_hover_template(),
    )
    x_median = pd.to_numeric(data["_discount_to_nominal"], errors="coerce").median()
    y_median = pd.to_numeric(data["_yield"], errors="coerce").median()
    if facet_column:
        add_yield_discount_period_median_lines(fig, data, facet_column)
    else:
        if pd.notna(x_median):
            fig.add_vline(
                x=float(x_median),
                line_dash="dash",
                line_color=HIGHLIGHT_COLORS["warning"],
                annotation_text="мед. дисконт",
            )
        if pd.notna(y_median):
            fig.add_hline(
                y=float(y_median),
                line_dash="dash",
                line_color=HIGHLIGHT_COLORS["stable"],
                annotation_text="мед. доходность",
            )
    if facet_column is None:
        add_yield_discount_quadrant_annotations(fig, data)
    fig.add_annotation(
        text=subtitle,
        xref="paper",
        yref="paper",
        x=0,
        y=1.13,
        showarrow=False,
        align="left",
        font={"size": 12, "color": "#1F2933"},
    )
    add_bubble_size_annotation(fig)
    fig.update_xaxes(title_text="Дисконт к номиналу, п.п.")
    fig.update_yaxes(title_text="Доходность, % годовых")
    if facet_column is not None:
        clean_yield_vs_discount_facet_axes(fig)
    apply_common_layout(fig, legend_title="Год")
    fig.update_layout(legend_title_text="Год")
    if facet_column is not None:
        fig.update_layout(margin={"l": 104, "r": 48, "t": 118, "b": 104})
    return fig


def yield_vs_discount_hover_template() -> str:
    """Русский hover для квадранта доходности и дисконта."""
    return (
        "Год: %{customdata[0]}<br>"
        "Выпуск: %{customdata[1]}<br>"
        "Дата размещения: %{customdata[2]}<br>"
        "Период: %{customdata[3]}<br>"
        "Вид ОФЗ: %{customdata[4]}<br>"
        "Формат: %{customdata[5]}<br>"
        "Сроковая категория: %{customdata[6]}<br>"
        "Дисконт к номиналу, п.п.: %{customdata[7]}<br>"
        "Доходность, % годовых: %{customdata[8]}<br>"
        "Цена отсечения: %{customdata[9]}<br>"
        "Объем размещения по номиналу, млрд рублей: %{customdata[10]}<br>"
        "Спрос, млн рублей: %{customdata[11]}<br>"
        "Предложение, млн рублей: %{customdata[12]}<br>"
        "Спрос / объем размещения: %{customdata[13]}<br>"
        "Спрос / предложение: %{customdata[14]}<br>"
        "Качество данных: %{customdata[15]}<br>"
        "Причина подписи: %{customdata[16]}"
        "<extra></extra>"
    )


def add_yield_discount_period_median_lines(figure: Any, data: pd.DataFrame, facet_column: str) -> None:
    """Добавить пунктирные медианы периода в каждую facet-панель yield_vs_discount."""
    if facet_column not in data.columns:
        return
    group_by_facet = {str(facet): group for facet, group in data.groupby(facet_column, dropna=False)}
    label_added = True
    used_axes: set[tuple[str, str]] = set()
    for trace in figure.data:
        xaxis_ref = getattr(trace, "xaxis", "x") or "x"
        yaxis_ref = getattr(trace, "yaxis", "y") or "y"
        axis_key = (str(xaxis_ref), str(yaxis_ref))
        if axis_key in used_axes:
            continue
        used_axes.add(axis_key)

        facet_value = ""
        custom_data = getattr(trace, "customdata", None)
        if custom_data is not None and len(custom_data) > 0:
            first = custom_data[0]
            if len(first) > 0:
                year_text = str(first[0])
                matching = data.loc[data["yield_vs_discount_color"].astype(str).eq(year_text), facet_column].dropna()
                if not matching.empty:
                    facet_value = str(matching.iloc[0])
        if not facet_value:
            continue
        group = group_by_facet.get(facet_value)
        if group is None or group.empty:
            continue
        median_discount = pd.to_numeric(group["_discount_to_nominal"], errors="coerce").median()
        median_yield = pd.to_numeric(group["_yield"], errors="coerce").median()
        if pd.notna(median_discount):
            figure.add_shape(
                type="line",
                x0=float(median_discount),
                x1=float(median_discount),
                y0=0,
                y1=1,
                xref=xaxis_ref,
                yref=f"{yaxis_ref} domain",
                line={"dash": "dash", "color": HIGHLIGHT_COLORS["warning"], "width": 1.5},
            )
        if pd.notna(median_yield):
            figure.add_shape(
                type="line",
                x0=0,
                x1=1,
                y0=float(median_yield),
                y1=float(median_yield),
                xref=f"{xaxis_ref} domain",
                yref=yaxis_ref,
                line={"dash": "dash", "color": HIGHLIGHT_COLORS["stable"], "width": 1.5},
            )
        if not label_added:
            if pd.notna(median_discount):
                figure.add_annotation(
                    text="мед. дисконт",
                    x=float(median_discount),
                    y=1.02,
                    xref=xaxis_ref,
                    yref=f"{yaxis_ref} domain",
                    showarrow=False,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="rgba(255,255,255,0.78)",
                    font={"size": 10, "color": "#4B5563"},
                )
            if pd.notna(median_yield):
                figure.add_annotation(
                    text="мед. доходность",
                    x=0.98,
                    y=float(median_yield),
                    xref=f"{xaxis_ref} domain",
                    yref=yaxis_ref,
                    showarrow=False,
                    xanchor="right",
                    yanchor="bottom",
                    bgcolor="rgba(255,255,255,0.78)",
                    font={"size": 10, "color": "#4B5563"},
                )
            label_added = True


def clean_yield_vs_discount_facet_axes(figure: Any) -> None:
    """Оставить в facet-графике один общий X/Y-title и убрать повторяющиеся подписи осей."""
    layout_keys = figure.layout.to_plotly_json().keys()
    x_axes: list[tuple[str, Any]] = [(name, getattr(figure.layout, name)) for name in layout_keys if name.startswith("xaxis")]
    y_axes: list[tuple[str, Any]] = [(name, getattr(figure.layout, name)) for name in layout_keys if name.startswith("yaxis")]

    x_domain_by_anchor: dict[str, tuple[float, float]] = {}
    y_domain_by_anchor: dict[str, tuple[float, float]] = {}
    for name, axis in x_axes:
        domain = getattr(axis, "domain", None)
        anchor = "x" if name == "xaxis" else "x" + name.replace("xaxis", "")
        if domain:
            x_domain_by_anchor[anchor] = (float(domain[0]), float(domain[1]))
    for name, axis in y_axes:
        domain = getattr(axis, "domain", None)
        anchor = "y" if name == "yaxis" else "y" + name.replace("yaxis", "")
        if domain:
            y_domain_by_anchor[anchor] = (float(domain[0]), float(domain[1]))
    min_y0 = min((domain[0] for domain in y_domain_by_anchor.values()), default=0.0)
    min_x0 = min((domain[0] for domain in x_domain_by_anchor.values()), default=0.0)

    for name, axis in x_axes:
        axis.update(title_text="")
        anchor = getattr(axis, "anchor", "y")
        y_domain = y_domain_by_anchor.get(str(anchor), (min_y0, min_y0))
        axis.update(showticklabels=abs(y_domain[0] - min_y0) < 1e-6)
        if name != "xaxis":
            axis.update(matches="x")
    for name, axis in y_axes:
        axis.update(title_text="")
        anchor = getattr(axis, "anchor", "x")
        x_domain = x_domain_by_anchor.get(str(anchor), (min_x0, min_x0))
        axis.update(showticklabels=abs(x_domain[0] - min_x0) < 1e-6)
        if name != "yaxis":
            axis.update(matches="y")

    figure.for_each_annotation(
        lambda annotation: annotation.update(
            text=str(annotation.text)
            .replace("yield_vs_discount_facet=", "")
            .replace("Период=", "")
            .replace("None", "")
        )
    )
    figure.add_annotation(
        text="Дисконт к номиналу, п.п.",
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.075,
        showarrow=False,
        font={"size": 12, "color": "#1F2933"},
    )
    figure.add_annotation(
        text="Доходность, % годовых",
        xref="paper",
        yref="paper",
        x=-0.055,
        y=0.5,
        textangle=-90,
        showarrow=False,
        font={"size": 12, "color": "#1F2933"},
    )


def add_yield_discount_quadrant_annotations(figure: Any, data: pd.DataFrame) -> None:
    """Добавить подписи квадрантов относительно медианного дисконта и медианной доходности."""
    x_values = pd.to_numeric(data["_discount_to_nominal"], errors="coerce").dropna()
    y_values = pd.to_numeric(data["_yield"], errors="coerce").dropna()
    if x_values.empty or y_values.empty:
        return
    x_min, x_max = float(x_values.min()), float(x_values.max())
    y_min, y_max = float(y_values.min()), float(y_values.max())
    x_median, y_median = float(x_values.median()), float(y_values.median())
    if x_min == x_max or y_min == y_max:
        return
    positions = [
        (x_median + (x_max - x_median) * 0.58, y_median + (y_max - y_median) * 0.72, "высокий дисконт / высокая доходность"),
        (x_median + (x_max - x_median) * 0.58, y_min + (y_median - y_min) * 0.28, "высокий дисконт / низкая доходность"),
        (x_min + (x_median - x_min) * 0.42, y_median + (y_max - y_median) * 0.72, "низкий дисконт / высокая доходность"),
        (x_min + (x_median - x_min) * 0.42, y_min + (y_median - y_min) * 0.28, "низкий дисконт / низкая доходность"),
    ]
    for x_pos, y_pos, text in positions:
        figure.add_annotation(
            x=x_pos,
            y=y_pos,
            text=text,
            showarrow=False,
            bgcolor="rgba(255,255,255,0.72)",
            bordercolor="rgba(31,41,51,0.18)",
            borderwidth=1,
            font={"size": 10, "color": "#1F2933"},
        )


def yield_vs_discount_export_data(data: pd.DataFrame) -> pd.DataFrame:
    """Сформировать CSV-основу квадранта доходность/дисконт."""
    columns = unique_columns(
        [
            "auction_date",
            "report_year",
            "report_period_label",
            "report_period_display_label",
            "report_period_order",
            "period_month_start",
            "period_month_end",
            "is_incomplete_period",
            "incomplete_period_reason",
            "is_target_period",
            "issue_code",
            "ofz_type",
            "format",
            "maturity_bucket",
            "maturity_bucket_label",
            "discount_to_nominal",
            "weighted_avg_yield",
            "placement_volume",
            "placement_volume_bln",
            "demand_volume",
            "supply_volume",
            "demand_to_placement_ratio",
            "bid_to_cover_ratio",
            "_discount_to_nominal",
            "_yield",
            "_cutoff_price",
            "_placement",
            "placement_volume_unit",
            "bubble_size_value",
            "_demand",
            "_supply",
            "_demand_to_placement",
            "_bid_to_cover",
            "x_value",
            "y_value",
            "yield_vs_discount_color",
            "scatter_label",
            "scatter_textposition",
            "label_display",
            "label_visible",
            "label_reason",
            "label_reason_display",
            "median_discount",
            "median_yield",
            "median_discount_period",
            "median_yield_period",
            "median_scope",
            "data_quality_flag",
            "data_quality_display",
        ]
    )
    export = data.copy()
    defaults: dict[str, Any] = {
        "label_display": "",
        "label_visible": False,
        "label_reason": "",
        "label_reason_display": "",
        "data_quality_flag": "",
        "data_quality_display": "",
        "bubble_size_value": pd.NA,
        "placement_volume_bln": pd.NA,
        "median_discount": pd.NA,
        "median_yield": pd.NA,
        "median_scope": "",
        "is_incomplete_period": False,
        "incomplete_period_reason": "",
    }
    for column, value in defaults.items():
        if column not in export.columns:
            export[column] = value
    export["label_visible"] = export["label_visible"].fillna(False).astype(bool)
    export["is_incomplete_period"] = export["is_incomplete_period"].fillna(False).astype(bool)
    return export[[column for column in columns if column in export.columns]].copy()


def build_policy_scatter_figure(
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    color_column: str | None,
    title: str,
    x_title: str,
    y_title: str,
    legend_title: str,
    *,
    log_x: bool = False,
    facet_column: str | None = None,
    subtitle: str | None = None,
) -> Any:
    """Построить scatter-график по общей политике подписей."""
    assert px is not None
    plot_data = ensure_scatter_hover_columns(data)
    custom_data_columns = scatter_custom_data_columns()
    kwargs: dict[str, Any] = {
        "data_frame": plot_data,
        "x": x_column,
        "y": y_column,
        "size": "_placement" if "_placement" in data.columns else None,
        "color": color_column,
        "text": "scatter_label",
        "title": title,
        "color_discrete_sequence": QUALITATIVE_COLORS,
        "labels": {
            x_column: x_title,
            y_column: y_title,
            "_placement": "Объем размещения по номиналу",
            "report_period_label": "Период",
        },
        "custom_data": custom_data_columns,
    }
    if "_placement" in data.columns:
        kwargs["size_max"] = 42
    if facet_column:
        kwargs["facet_col"] = facet_column
        kwargs["facet_col_wrap"] = 3
    if log_x:
        kwargs["log_x"] = True
    fig = px.scatter(**{key: value for key, value in kwargs.items() if value is not None})
    if "_placement" in plot_data.columns:
        max_size = pd.to_numeric(plot_data["_placement"], errors="coerce").max()
        if pd.notna(max_size) and float(max_size) > 0:
            fig.update_traces(
                marker={
                    "sizemode": "area",
                    "sizeref": float(max_size) / (42.0**2),
                    "sizemin": 6,
                    "opacity": 0.78,
                    "line": {"width": 0.6, "color": "rgba(31,41,51,0.35)"},
                }
            )
    fig.update_traces(
        textposition=plot_data["scatter_textposition"].tolist() if "scatter_textposition" in plot_data.columns and not facet_column else "top center",
        textfont={"size": 9},
        hovertemplate=scatter_hover_template(),
    )
    fig.add_annotation(
        text="Размер точки = объем размещения по номиналу; hover является основным источником детализации",
        xref="paper",
        yref="paper",
        x=0,
        y=1.10,
        showarrow=False,
        align="left",
        font={"size": 12, "color": "#1F2933"},
    )
    if subtitle:
        fig.add_annotation(
            text=subtitle,
            xref="paper",
            yref="paper",
            x=0,
            y=1.17,
            showarrow=False,
            align="left",
            font={"size": 12, "color": "#1F2933"},
        )
    add_bubble_size_annotation(fig)
    fig.update_layout(xaxis_title=x_title, yaxis_title=y_title)
    fig.update_xaxes(title_text=x_title)
    fig.update_yaxes(title_text=y_title)
    apply_common_layout(fig, legend_title=legend_title)
    return fig


def scatter_custom_data_columns() -> list[str]:
    """Единый набор hover-полей для policy scatter."""
    return [
        "report_period_label",
        "auction_date",
        "issue_code",
        "ofz_type",
        "format",
        "_demand",
        "_supply",
        "_placement",
        "_revenue",
        "_demand_to_placement",
        "_bid_to_cover",
        "_yield",
        "_discount_to_nominal",
        "_cutoff_price",
        "maturity_bucket_label",
        "ratio_basis",
        "scatter_label_reason",
        "data_quality_flag",
    ]


def add_bubble_size_annotation(figure: Any) -> None:
    """Добавить текстовую легенду размера пузыря для dense scatter."""
    figure.add_annotation(
        text="Размер точки — объем размещения по номиналу<br>ориентиры: 50 / 250 / 500 млрд руб.",
        xref="paper",
        yref="paper",
        x=1,
        y=-0.18,
        showarrow=False,
        align="right",
        font={"size": 11, "color": "#1F2933"},
    )


def ensure_scatter_hover_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Добавить пустые hover-колонки, чтобы шаблон не ломался при разных источниках."""
    result = data.copy()
    for column in scatter_custom_data_columns():
        if column not in result.columns:
            result[column] = ""
    if "scatter_textposition" not in result.columns:
        result["scatter_textposition"] = "top center"
    if "scatter_label" not in result.columns:
        result["scatter_label"] = ""
    return result


def _scatter_hover_template_legacy() -> str:
    return (
        "Период: %{customdata[0]}<br>"
        "Дата: %{customdata[1]}<br>"
        "Код выпуска: %{customdata[2]}<br>"
        "Тип ОФЗ: %{customdata[3]}<br>"
        "Формат: %{customdata[4]}<br>"
        "Спрос: %{customdata[5]}<br>"
        "Предложение: %{customdata[6]}<br>"
        "Размещение: %{customdata[7]}<br>"
        "Спрос / размещение: %{customdata[8]}<br>"
        "Спрос / предложение: %{customdata[9]}<br>"
        "Доходность: %{customdata[10]}<br>"
        "Дисконт к номиналу: %{customdata[11]}<br>"
        "Сроковая категория: %{customdata[12]}<br>"
        "Формула ratio: %{customdata[13]}<br>"
        "Причина подписи: %{customdata[14]}<br>"
        "Флаг качества: %{customdata[15]}"
        "<extra></extra>"
    )


def scatter_hover_template() -> str:
    """Русифицированный hover для dense scatter-графиков второй модернизации."""
    return (
        "Период: %{customdata[0]}<br>"
        "Дата: %{customdata[1]}<br>"
        "Выпуск: %{customdata[2]}<br>"
        "Тип ОФЗ: %{customdata[3]}<br>"
        "Формат: %{customdata[4]}<br>"
        "Спрос: %{customdata[5]} млн руб.<br>"
        "Предложение: %{customdata[6]} млн руб.<br>"
        "Объем размещения по номиналу: %{customdata[7]} млн руб.<br>"
        "Выручка от реализации: %{customdata[8]} млн руб.<br>"
        "Спрос / объем размещения: %{customdata[9]}<br>"
        "Спрос / предложение: %{customdata[10]}<br>"
        "Доходность: %{customdata[11]}<br>"
        "Дисконт к номиналу: %{customdata[12]}<br>"
        "Цена отсечения: %{customdata[13]}<br>"
        "Сроковая категория: %{customdata[14]}<br>"
        "Формула ratio: %{customdata[15]}<br>"
        "Причина подписи: %{customdata[16]}<br>"
        "Флаг качества данных: %{customdata[17]}"
        "<extra></extra>"
    )


def scatter_export_data(data: pd.DataFrame, x_column: str, y_column: str) -> pd.DataFrame:
    export = data.copy()
    if "label_display" not in export.columns:
        if "scatter_label" in export.columns:
            export["label_display"] = export["scatter_label"].fillna("").astype(str)
        else:
            export["label_display"] = ""
    if "label_reason" not in export.columns:
        if "scatter_label_reason" in export.columns:
            export["label_reason"] = export["scatter_label_reason"].fillna("").astype(str)
        else:
            export["label_reason"] = ""
    columns = unique_columns(
        scatter_custom_data_columns()
        + [
            x_column,
            y_column,
            "x_value",
            "y_value",
            "scatter_label",
            "scatter_textposition",
            "label_display",
            "label_reason",
            "placement_volume_bln",
            "placement_volume_unit",
        ]
    )
    return export[[column for column in columns if column in export.columns]].copy()


def mark_near_zero_floating_rate_yields(data: pd.DataFrame, limitations: list[str]) -> pd.DataFrame:
    """Отметить около-нулевую доходность ОФЗ-ПК как требующую методологической проверки."""
    result = data.copy()
    if "ofz_type" not in result.columns or "_yield" not in result.columns:
        return result
    ofz_type = result["ofz_type"].astype("string").str.upper()
    yield_values = pd.to_numeric(result["_yield"], errors="coerce")
    near_zero_mask = ofz_type.str.contains("ПК", na=False) & yield_values.notna() & (yield_values.abs() <= 0.01)
    if not near_zero_mask.any():
        return result
    if "data_quality_flag" not in result.columns:
        result["data_quality_flag"] = ""
    quality_text = result["data_quality_flag"].fillna("").astype(str).str.lower()
    suspect_missing_mask = near_zero_mask & quality_text.str.contains("missing|requires_review|invalid", regex=True)
    if suspect_missing_mask.any():
        result.loc[suspect_missing_mask, "_yield"] = pd.NA
        near_zero_mask = near_zero_mask & ~suspect_missing_mask
        limitations.append(
            "Из boxplot доходности исключены около-нулевые значения ОФЗ-ПК с флагами missing/requires_review/invalid; "
            "они трактуются как возможная замена пропуска на 0."
        )
    if not near_zero_mask.any():
        return result
    current_flags = result.loc[near_zero_mask, "data_quality_flag"].fillna("").astype(str)
    result.loc[near_zero_mask, "data_quality_flag"] = current_flags.map(
        lambda value: "near_zero_yield_requires_review"
        if not value
        else f"{value}; near_zero_yield_requires_review"
    )
    limitations.append(
        "В boxplot доходности обнаружены ОФЗ-ПК с доходностью около нуля; строки не удаляются автоматически, "
        "но помечаются `near_zero_yield_requires_review` и требуют сверки с исходной колонкой доходности."
    )
    return result


def detect_yield_column_used(data: pd.DataFrame) -> str:
    """Определить исходную колонку доходности, из которой сформирована `_yield`."""
    for column in ["yield", "weighted_avg_yield", "weighted_avg_yield_pct"]:
        if column in data.columns and pd.to_numeric(data[column], errors="coerce").notna().any():
            return column
    return "_yield"


def add_yield_boxplot_hover_columns(data: pd.DataFrame) -> pd.DataFrame:
    result = data.copy()
    result["Период"] = result["report_period_label"].astype("string") if "report_period_label" in result.columns else ""
    result["Дата размещения"] = result["auction_date"].astype("string") if "auction_date" in result.columns else ""
    result["Код выпуска"] = result["issue_code"].astype("string") if "issue_code" in result.columns else ""
    result["Тип ОФЗ"] = result["ofz_type"].astype("string") if "ofz_type" in result.columns else ""
    result["Формат"] = result["format"].astype("string") if "format" in result.columns else ""
    result["Доходность"] = result["_yield"].map(lambda value: format_hover_number(value, 2))
    result["Объем размещения"] = result["_placement"].map(lambda value: format_hover_number(value, 1))
    result["Сроковая категория"] = result["maturity_bucket"].astype("string") if "maturity_bucket" in result.columns else ""
    grouping = result.groupby(["ofz_type", "Цвет периода"], dropna=False)["_yield"].transform("count")
    result["Предупреждение качества"] = ""
    result.loc[grouping == 1, "Предупреждение качества"] = "n=1; распределение не интерпретируется"
    result.loc[(grouping > 1) & (grouping < 3), "Предупреждение качества"] = "n<3; статистически ограничено"
    result["Используемая колонка доходности"] = result["yield_column_used"].astype("string") if "yield_column_used" in result.columns else "_yield"
    result["Data quality flag"] = result["data_quality_flag"].astype("string") if "data_quality_flag" in result.columns else ""
    return result


def yield_boxplot_period_order(data: pd.DataFrame, params: report_params.ReportParams) -> list[str]:
    order_from_params = [
        str(period["label"])
        for period in params.periods
        if str(period.get("label", "")) in set(data["Период boxplot"].dropna().astype(str))
    ]
    if order_from_params:
        return sorted(order_from_params, key=period_sort_key)
    return sorted(data["Период boxplot"].dropna().astype(str).unique().tolist(), key=period_sort_key)


def build_yield_boxplot_x_period(data: pd.DataFrame) -> pd.Series:
    """Вернуть видимую категорию периода для оси X в facet-mode."""
    if "report_period_type" in data.columns and "report_year" in data.columns:
        period_types = data["report_period_type"].dropna().astype(str).str.lower().unique().tolist()
        if period_types and set(period_types) == {"year"}:
            years = pd.to_numeric(data["report_year"], errors="coerce")
            if years.notna().any():
                return years.astype("Int64").astype("string")
    if "report_period_display_label" in data.columns:
        values = data["report_period_display_label"].astype("string").fillna("").str.strip()
        if values.ne("").any():
            return values.where(values.ne(""), data["Период boxplot"].astype("string"))
    if "report_year" in data.columns:
        years = pd.to_numeric(data["report_year"], errors="coerce")
        if years.notna().any():
            return years.astype("Int64").astype("string")
    return data["Период boxplot"].astype("string")


def yield_boxplot_x_order(data: pd.DataFrame, period_order: list[str]) -> list[str]:
    """Сохранить хронологический порядок X-категорий для длинного boxplot."""
    if "Период X boxplot" not in data.columns:
        return period_order
    pairs = (
        data[["Период boxplot", "Период X boxplot"]]
        .dropna()
        .astype(str)
        .drop_duplicates()
    )
    x_by_period = dict(zip(pairs["Период boxplot"], pairs["Период X boxplot"]))
    ordered = [x_by_period[label] for label in period_order if label in x_by_period]
    if ordered:
        return list(dict.fromkeys(ordered))
    return sorted(data["Период X boxplot"].dropna().astype(str).unique().tolist(), key=period_sort_key)


def first_non_empty_group_value(group: pd.DataFrame, column: str) -> Any:
    """Вернуть первое непустое значение группы для export-статистик."""
    if column not in group.columns:
        return pd.NA
    values = group[column].dropna()
    if values.empty:
        return pd.NA
    return values.iloc[0]


def build_yield_boxplot_stats(
    data: pd.DataFrame,
    color_label: str,
    period_order: list[str],
    period_x_order: list[str],
    ofz_type_order: list[str],
    period_offsets: dict[str, float],
    label_mode: str,
    chart_mode: str,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    order_lookup = {period: index + 1 for index, period in enumerate(period_order)}
    x_order_lookup = {period: index + 1 for index, period in enumerate(period_x_order)}
    ofz_lookup = {ofz_type: index for index, ofz_type in enumerate(ofz_type_order)}
    for (ofz_type, period_label), group in data.groupby(["ofz_type", "Период boxplot"], dropna=False):
        yields = pd.to_numeric(group["_yield"], errors="coerce").dropna()
        if yields.empty:
            continue
        n = int(len(yields))
        placement_volume = pd.to_numeric(group["_placement"], errors="coerce").sum(min_count=1)
        q1 = float(yields.quantile(0.25))
        q3 = float(yields.quantile(0.75))
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr
        inlier_values = yields.loc[(yields >= lower_fence) & (yields <= upper_fence)]
        lower_whisker = float(inlier_values.min()) if not inlier_values.empty else float(yields.min())
        upper_whisker = float(inlier_values.max()) if not inlier_values.empty else float(yields.max())
        lower_outliers = yields.loc[yields < lower_fence]
        upper_outliers = yields.loc[yields > upper_fence]
        outlier_min = float(lower_outliers.min()) if not lower_outliers.empty else pd.NA
        outlier_max = float(upper_outliers.max()) if not upper_outliers.empty else pd.NA
        outliers_count = int(len(lower_outliers) + len(upper_outliers))
        if n == 1:
            data_quality_flag = "n_1_not_distribution"
            compact_label = f"n=1<br>значение: {float(yields.iloc[0]):.2f}"
        elif n < 3:
            data_quality_flag = "n_less_3_limited_distribution"
            compact_label = f"мед: {float(yields.median()):.2f}<br>n={n}"
        else:
            data_quality_flag = "ok"
            compact_label = f"мед: {float(yields.median()):.2f}<br>n={n}"
        if "data_quality_flag" in group.columns:
            group_flags = group["data_quality_flag"].fillna("").astype(str)
            if group_flags.str.contains("near_zero_yield_requires_review", regex=False).any():
                data_quality_flag = f"{data_quality_flag}; near_zero_yield_requires_review"
        if n == 1:
            label_y = float(yields.iloc[0])
        else:
            label_y = float(yields.median())
        display_label = first_non_empty_group_value(group, "report_period_display_label")
        if pd.isna(display_label):
            display_label = str(period_label)
        x_period_value = (
            str(group["Период X boxplot"].iloc[0])
            if "Период X boxplot" in group.columns
            else str(period_label)
        )
        rows.append(
            {
                "report_period_label": str(period_label),
                "report_period_start": first_non_empty_group_value(group, "report_period_start"),
                "report_period_display_label": display_label,
                "report_period_order": order_lookup.get(str(period_label), 0),
                "report_year": first_non_empty_group_value(group, "report_year"),
                "ofz_type": ofz_type,
                "boxplot_x_period": x_period_value,
                "boxplot_x_order": x_order_lookup.get(
                    x_period_value,
                    order_lookup.get(str(period_label), 0),
                ),
                "x_base": ofz_lookup.get(str(ofz_type), 0),
                "period_offset": period_offsets.get(str(period_label), 0.0),
                "x_group": float(group["x_group"].iloc[0]) if "x_group" in group.columns else ofz_lookup.get(str(ofz_type), 0),
                "Цвет периода": str(group["Цвет периода"].iloc[0]) if "Цвет периода" in group.columns else str(period_label),
                "legend_title": color_label,
                "yield_min_actual": float(yields.min()),
                "min": float(yields.min()),
                "yield_q1": q1,
                "q1": q1,
                "yield_median": float(yields.median()),
                "median": float(yields.median()),
                "yield_q3": q3,
                "q3": q3,
                "yield_max_actual": float(yields.max()),
                "max": float(yields.max()),
                "lower_whisker": lower_whisker,
                "upper_whisker": upper_whisker,
                "lower_fence": float(lower_fence),
                "upper_fence": float(upper_fence),
                "outlier_min": outlier_min,
                "outlier_max": outlier_max,
                "has_outliers": outliers_count > 0,
                "outliers_count": outliers_count,
                "auction_count": n,
                "n": n,
                "placement_volume": placement_volume,
                "yield_column_used": str(group["yield_column_used"].iloc[0]) if "yield_column_used" in group.columns else "_yield",
                "data_quality_flag": data_quality_flag,
                "label_mode": label_mode,
                "chart_mode": chart_mode,
                "compact_label": compact_label,
                "label_y": label_y,
                "xshift": 0,
            }
        )
    columns = [
        "report_period_label",
        "report_period_start",
        "report_period_display_label",
        "report_period_order",
        "report_year",
        "ofz_type",
        "boxplot_x_period",
        "boxplot_x_order",
        "x_base",
        "period_offset",
        "x_group",
        "yield_min_actual",
        "min",
        "yield_q1",
        "q1",
        "yield_median",
        "median",
        "yield_q3",
        "q3",
        "yield_max_actual",
        "max",
        "lower_whisker",
        "upper_whisker",
        "lower_fence",
        "upper_fence",
        "outlier_min",
        "outlier_max",
        "has_outliers",
        "outliers_count",
        "auction_count",
        "n",
        "placement_volume",
        "yield_column_used",
        "data_quality_flag",
        "Цвет периода",
        "label_mode",
        "chart_mode",
        "legend_title",
        "compact_label",
        "label_y",
        "xshift",
    ]
    return pd.DataFrame(rows, columns=columns)


def centered_shift_map(values: list[str], step: int = 34, limit: int = 58) -> dict[str, int]:
    if not values:
        return {}
    middle = (len(values) - 1) / 2
    result: dict[str, int] = {}
    for index, value in enumerate(values):
        shift = int(round((index - middle) * step))
        result[value] = max(-limit, min(limit, shift))
    return result


def centered_float_offset_map(values: list[str], step: float = 0.22, limit: float = 0.32) -> dict[str, float]:
    if not values:
        return {}
    middle = (len(values) - 1) / 2
    result: dict[str, float] = {}
    for index, value in enumerate(values):
        offset = (index - middle) * step
        result[value] = max(-limit, min(limit, offset))
    return result


def add_yield_boxplot_outlier_flags(data: pd.DataFrame, stats: pd.DataFrame) -> pd.DataFrame:
    result = data.copy()
    result["Признак выброса"] = ""
    if stats.empty:
        return result
    bounds = {
        (str(row["ofz_type"]), str(row["report_period_label"])): (
            float(row["lower_whisker"]),
            float(row["upper_whisker"]),
        )
        for _, row in stats.iterrows()
    }
    for index, row in result.iterrows():
        key = (str(row.get("ofz_type", "")), str(row.get("Период boxplot", "")))
        if key not in bounds:
            continue
        lower_whisker, upper_whisker = bounds[key]
        value = pd.to_numeric(pd.Series([row.get("_yield")]), errors="coerce").iloc[0]
        if pd.isna(value):
            continue
        if float(value) < lower_whisker:
            result.at[index, "Признак выброса"] = "нижний выброс"
        elif float(value) > upper_whisker:
            result.at[index, "Признак выброса"] = "верхний выброс"
    return result


def write_yield_boxplot_stats_export(stats: pd.DataFrame, params: report_params.ReportParams) -> None:
    if stats.empty:
        return
    suffix = make_suffix(params)
    export_data = stats.copy()
    if "placement_volume" in export_data.columns:
        export_data["placement_volume_bln"] = pd.to_numeric(export_data["placement_volume"], errors="coerce") / 1000.0
        export_data["placement_volume_unit"] = "млн рублей"
        export_data["placement_volume_bln_unit"] = "млрд рублей"
    export_columns = [
        "report_period_start",
        "report_period_display_label",
        "report_period_order",
        "ofz_type",
        "n",
        "min",
        "q1",
        "median",
        "q3",
        "max",
        "lower_fence",
        "upper_fence",
        "has_outliers",
        "outliers_count",
        "report_period_label",
        "report_year",
        "boxplot_x_period",
        "boxplot_x_order",
        "x_base",
        "period_offset",
        "x_group",
        "yield_min_actual",
        "yield_max_actual",
        "lower_whisker",
        "upper_whisker",
        "outlier_min",
        "outlier_max",
        "auction_count",
        "placement_volume",
        "placement_volume_bln",
        "placement_volume_unit",
        "placement_volume_bln_unit",
        "yield_column_used",
        "data_quality_flag",
        "label_mode",
        "chart_mode",
    ]
    path = config.EXPORTS_CHART_DATA_BOXPLOT_DIR / f"yield_boxplot_stats_{suffix}.csv"
    export_data[export_columns].to_csv(path, index=False, encoding="utf-8")


def build_yield_boxplot_ofz_pd_stats(
    data: pd.DataFrame,
    period_order: list[str],
    period_x_order: list[str],
) -> pd.DataFrame:
    """Рассчитать статистику отдельного boxplot по ОФЗ-ПД с привязкой к периоду на оси X."""
    prepared = data.copy()
    period_to_x = {period: index for index, period in enumerate(period_order)}
    prepared["x_base"] = prepared["Период boxplot"].astype(str).map(period_to_x).fillna(0.0)
    prepared["period_offset"] = 0.0
    prepared["x_group"] = prepared["x_base"]
    ofz_type_order = sorted(prepared["ofz_type"].dropna().astype(str).unique().tolist())
    stats = build_yield_boxplot_stats(
        prepared,
        color_label="Период",
        period_order=period_order,
        period_x_order=period_x_order,
        ofz_type_order=ofz_type_order,
        period_offsets={period: 0.0 for period in period_order},
        label_mode="full",
        chart_mode="ofz_pd_period_boxplot",
    )
    if stats.empty:
        return stats
    stats["x_group"] = stats["boxplot_x_period"].astype(str)
    stats["x_base"] = stats["report_period_label"].astype(str).map(period_to_x).fillna(0).astype(float)
    stats["period_offset"] = 0.0
    stats["label_mode"] = "full"
    stats["chart_mode"] = "ofz_pd_period_boxplot"
    return stats


def write_yield_boxplot_ofz_pd_stats_export(stats: pd.DataFrame, params: report_params.ReportParams) -> None:
    """Сохранить таблицу статистик отдельного boxplot ОФЗ-ПД."""
    if stats.empty:
        return
    suffix = make_suffix(params)
    export_data = stats.copy()
    if "placement_volume" in export_data.columns:
        export_data["placement_volume_bln"] = pd.to_numeric(export_data["placement_volume"], errors="coerce") / 1000.0
        export_data["placement_volume_unit"] = "млн рублей"
        export_data["placement_volume_bln_unit"] = "млрд рублей"
    export_columns = [
        "report_period_start",
        "report_period_display_label",
        "report_period_order",
        "report_year",
        "ofz_type",
        "n",
        "min",
        "q1",
        "median",
        "q3",
        "max",
        "lower_fence",
        "upper_fence",
        "has_outliers",
        "outliers_count",
        "report_period_label",
        "boxplot_x_period",
        "boxplot_x_order",
        "yield_min_actual",
        "yield_q1",
        "yield_median",
        "yield_q3",
        "yield_max_actual",
        "lower_whisker",
        "upper_whisker",
        "outlier_min",
        "outlier_max",
        "auction_count",
        "placement_volume",
        "placement_volume_bln",
        "placement_volume_unit",
        "placement_volume_bln_unit",
        "yield_column_used",
        "data_quality_flag",
        "label_mode",
        "chart_mode",
    ]
    available_columns = [column for column in export_columns if column in export_data.columns]
    path = config.EXPORTS_CHART_DATA_BOXPLOT_DIR / f"yield_boxplot_ofz_pd_stats_{suffix}.csv"
    export_data[available_columns].to_csv(path, index=False, encoding="utf-8")


def add_yield_boxplot_ofz_pd_single_period_fallback(
    figure: Any,
    group: pd.DataFrame,
    stats: pd.DataFrame,
    *,
    x_center: float,
    color: str,
) -> None:
    """Render a readable one-period OFZ-PD distribution as jittered strip + summary ticks."""
    if group.empty or stats.empty:
        return
    assert go is not None
    row = stats.iloc[0]
    prepared = group.sort_values(["_yield", "issue_code"], na_position="last").copy()
    x_offsets = single_period_jitter_offsets(len(prepared), spread=0.45)
    prepared["single_period_x"] = [x_center + offset for offset in x_offsets]

    figure.add_trace(
        go.Scatter(
            x=prepared["single_period_x"],
            y=prepared["_yield"],
            mode="markers",
            name="single_period_strip_points",
            showlegend=False,
            marker={
                "color": color,
                "size": 9,
                "opacity": 0.55,
                "line": {"color": "#1F2933", "width": 0.8},
            },
            customdata=yield_boxplot_custom_data(prepared),
            hovertemplate=yield_boxplot_hover_template(),
        )
    )

    q1 = float(row["yield_q1"])
    q3 = float(row["yield_q3"])
    median_value = float(row["yield_median"])
    min_value = float(row["yield_min_actual"])
    max_value = float(row["yield_max_actual"])
    box_half_width = 0.24
    tick_half_width = 0.38
    figure.add_shape(
        type="rect",
        x0=x_center - box_half_width,
        x1=x_center + box_half_width,
        y0=q1,
        y1=q3,
        line={"color": color, "width": 1.6},
        fillcolor=hex_to_rgba(color, 0.18),
        layer="below",
    )
    for value, width, line_color, line_width in [
        (min_value, tick_half_width, "#166A75", 1.8),
        (median_value, 0.44, "#1F2933", 2.3),
        (max_value, tick_half_width, QUALITATIVE_COLORS[5], 1.8),
    ]:
        figure.add_shape(
            type="line",
            x0=x_center - width,
            x1=x_center + width,
            y0=value,
            y1=value,
            line={"color": line_color, "width": line_width},
        )

    annotation_x = x_center + 0.50
    annotations = [
        (max_value, f"макс: {max_value:.2f}", 12, QUALITATIVE_COLORS[5], "single_period_max_tick"),
        (median_value, f"мед: {median_value:.2f}<br>n={int(row['auction_count'])}", 0, "#1F2933", "single_period_median_tick"),
        (min_value, f"мин: {min_value:.2f}", -12, "#166A75", "single_period_min_tick"),
    ]
    for value, text, yshift, font_color, name in annotations:
        figure.add_annotation(
            x=annotation_x,
            y=value,
            text=text,
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            yshift=yshift,
            align="left",
            font={"size": 10, "color": font_color},
            bgcolor="rgba(255,255,255,0.74)",
            name=name,
        )
    figure.add_annotation(
        text="Один период: точки разведены по горизонтали; отметки показывают min, median, max.",
        xref="paper",
        yref="paper",
        x=0,
        y=1.04,
        showarrow=False,
        align="left",
        font={"size": 11, "color": "#4B5563"},
        name="single_period_strip_box_note",
    )

    hover_stats = prepare_yield_boxplot_hover_stats(stats.copy())
    figure.add_trace(
        go.Scatter(
            x=[x_center],
            y=hover_stats["yield_median"],
            mode="markers",
            name="single_period_stats_hover",
            marker={"size": 22, "color": "rgba(0,0,0,0)"},
            showlegend=False,
            hoverinfo="text",
            customdata=yield_boxplot_stats_hover_data(hover_stats),
            hovertemplate=yield_boxplot_stats_hover_template(),
        )
    )
    figure.update_layout(meta={"ofz_pd_boxplot_mode": "single_period_strip_box", "single_period_jitter": 0.45})


def update_yield_boxplot_ofz_pd_single_period_yaxis(figure: Any, data: pd.DataFrame) -> None:
    """Add vertical padding for short-horizon OFZ-PD strip-box fallback."""
    values = pd.to_numeric(data["_yield"], errors="coerce").dropna()
    if values.empty:
        return
    y_min = float(values.min())
    y_max = float(values.max())
    y_padding = max((y_max - y_min) * 0.18, 0.25)
    figure.update_yaxes(range=[y_min - y_padding, y_max + y_padding])


def single_period_jitter_offsets(count: int, spread: float) -> list[float]:
    """Return deterministic horizontal offsets for one-period strip points."""
    if count <= 0:
        return []
    if count == 1:
        return [0.0]
    step = (spread * 2) / (count - 1)
    return [round(-spread + index * step, 6) for index in range(count)]


def add_yield_boxplot_ofz_pd_stat_annotations(figure: Any, stats: pd.DataFrame) -> None:
    """Добавить подписи min / median / max / n рядом с boxplot ОФЗ-ПД."""
    if stats.empty:
        return
    for _, row in stats.iterrows():
        x_position = str(row["boxplot_x_period"])
        auction_count = int(row["auction_count"])
        median_value = float(row["yield_median"])
        if auction_count == 1:
            figure.add_annotation(
                x=x_position,
                y=median_value,
                text=f"n=1<br>значение: {median_value:.2f}",
                showarrow=False,
                xshift=26,
                yshift=10,
                align="left",
                font={"size": 10, "color": "#1F2933"},
                bgcolor="rgba(255,255,255,0.74)",
            )
            continue
        figure.add_annotation(
            x=x_position,
            y=float(row["yield_max_actual"]),
            text=f"макс: {float(row['yield_max_actual']):.2f}",
            showarrow=False,
            xshift=8,
            yshift=14,
            font={"size": 10, "color": QUALITATIVE_COLORS[5]},
            bgcolor="rgba(255,255,255,0.68)",
        )
        figure.add_annotation(
            x=x_position,
            y=median_value,
            text=f"мед: {median_value:.2f}<br>n={auction_count}",
            showarrow=False,
            xshift=28,
            yshift=0,
            align="left",
            font={"size": 10, "color": "#1F2933"},
            bgcolor="rgba(255,255,255,0.74)",
        )
        figure.add_annotation(
            x=x_position,
            y=float(row["yield_min_actual"]),
            text=f"мин: {float(row['yield_min_actual']):.2f}",
            showarrow=False,
            xshift=-8,
            yshift=-14,
            font={"size": 10, "color": "#166A75"},
            bgcolor="rgba(255,255,255,0.68)",
        )


def add_yield_boxplot_ofz_pd_stats_hover_trace(figure: Any, stats: pd.DataFrame) -> None:
    """Добавить невидимые hover-точки со статистикой boxplot ОФЗ-ПД."""
    if stats.empty:
        return
    assert go is not None
    hover_stats = prepare_yield_boxplot_hover_stats(stats)
    figure.add_trace(
        go.Scatter(
            x=hover_stats["boxplot_x_period"].astype(str),
            y=hover_stats["yield_median"],
            mode="markers",
            marker={"size": 18, "color": "rgba(0,0,0,0)"},
            showlegend=False,
            hoverinfo="text",
            customdata=yield_boxplot_stats_hover_data(hover_stats),
            hovertemplate=yield_boxplot_stats_hover_template(),
        )
    )


def yield_boxplot_custom_data(group: pd.DataFrame) -> Any:
    """Подготовить русифицированные поля hover для boxplot доходности."""
    columns = [
        "Период",
        "Дата размещения",
        "Код выпуска",
        "Тип ОФЗ",
        "Формат",
        "Доходность",
        "Объем размещения",
        "Сроковая категория",
        "Используемая колонка доходности",
        "Признак выброса",
        "Data quality flag",
    ]
    prepared = group.copy()
    for column in columns:
        if column not in prepared.columns:
            prepared[column] = ""
    return prepared[columns].to_numpy()


def yield_boxplot_hover_template() -> str:
    """Вернуть hover-шаблон без технических названий колонок."""
    return (
        "Период: %{customdata[0]}<br>"
        "Дата размещения: %{customdata[1]}<br>"
        "Код выпуска: %{customdata[2]}<br>"
        "Вид ОФЗ: %{customdata[3]}<br>"
        "Формат: %{customdata[4]}<br>"
        "Доходность, % годовых: %{customdata[5]}<br>"
        "Объем размещения по номиналу, млн руб.: %{customdata[6]}<br>"
        "Сроковая категория: %{customdata[7]}<br>"
        "Используемая колонка доходности: %{customdata[8]}<br>"
        "Признак выброса: %{customdata[9]}<br>"
        "Data quality flag: %{customdata[10]}"
        "<extra></extra>"
    )


def build_yield_boxplot_facet_figure(
    data: pd.DataFrame,
    stats: pd.DataFrame,
    period_order: list[str],
    period_x_order: list[str],
    ofz_type_order: list[str],
    period_color_map: dict[str, str],
) -> Any:
    """Построить facet/subplot boxplot для длинной ретроспективы."""
    assert go is not None
    assert make_subplots is not None
    column_count = max(1, len(ofz_type_order))
    if not stats.empty and "boxplot_x_period" in stats.columns:
        period_to_x: dict[str, str] = {
            str(row["report_period_label"]): str(row["boxplot_x_period"])
            for _, row in stats[["report_period_label", "boxplot_x_period"]]
            .dropna()
            .drop_duplicates()
            .iterrows()
        }
    else:
        period_to_x = {str(period): str(period) for period in period_order}
    figure = make_subplots(
        rows=1,
        cols=column_count,
        shared_yaxes=True,
        subplot_titles=ofz_type_order,
        horizontal_spacing=0.05 if column_count <= 3 else 0.035,
    )
    for column_index, ofz_type in enumerate(ofz_type_order, start=1):
        for period_label in period_order:
            group = data.loc[
                (data["ofz_type"].astype(str) == ofz_type)
                & (data["Период boxplot"].astype(str) == period_label)
            ].copy()
            if group.empty:
                continue
            x_value = str(group["Период X boxplot"].iloc[0]) if "Период X boxplot" in group.columns else period_label
            color = period_color_map.get(period_label, QUALITATIVE_COLORS[0])
            figure.add_trace(
                go.Box(
                    x=[x_value] * len(group),
                    y=group["_yield"],
                    name=period_label,
                    legendgroup=period_label,
                    showlegend=False,
                    marker={"color": color, "size": 5},
                    line={"color": color},
                    fillcolor=hex_to_rgba(color, 0.30),
                    boxpoints="all",
                    jitter=0.24,
                    pointpos=0,
                    width=0.55,
                    customdata=yield_boxplot_custom_data(group),
                    hovertemplate=yield_boxplot_hover_template(),
                ),
                row=1,
                col=column_index,
            )
        figure.update_xaxes(
            title_text="Период",
            categoryorder="array",
            categoryarray=period_x_order,
            tickangle=-35,
            row=1,
            col=column_index,
        )
    add_yield_boxplot_long_period_annotations(figure, stats, ofz_type_order, period_order, period_to_x)
    add_yield_boxplot_facet_stats_hover_trace(figure, stats, ofz_type_order)
    figure.add_annotation(
        text=(
            "Точки — отдельные размещения; панели разделяют виды ОФЗ; "
            "chart_mode=facet_by_ofz_type; label_mode=compact"
        ),
        xref="paper",
        yref="paper",
        x=0,
        y=1.12,
        showarrow=False,
        align="left",
        font={"size": 12, "color": "#1F2933"},
    )
    apply_common_layout(figure, legend_title=None)
    figure.update_layout(
        title="Распределение доходности ОФЗ-ПД",
        yaxis_title="Доходность, % годовых",
        margin={"l": 72, "r": 48, "t": 130, "b": 120},
        boxmode="group",
        showlegend=False,
        height=680,
    )
    return figure


def add_yield_boxplot_facet_stats_hover_trace(
    figure: Any,
    stats: pd.DataFrame,
    ofz_type_order: list[str],
) -> None:
    """Добавить невидимые hover-точки со статистиками boxplot для длинной ретроспективы."""
    if stats.empty:
        return
    assert go is not None
    hover_stats = prepare_yield_boxplot_hover_stats(stats)
    for column_index, ofz_type in enumerate(ofz_type_order, start=1):
        panel_stats = hover_stats.loc[hover_stats["ofz_type"].astype(str) == ofz_type].copy()
        if panel_stats.empty:
            continue
        figure.add_trace(
            go.Scatter(
                x=panel_stats["boxplot_x_period"].astype(str),
                y=panel_stats["label_y"],
                mode="markers",
                marker={"size": 18, "color": "rgba(0,0,0,0)"},
                showlegend=False,
                hoverinfo="text",
                customdata=yield_boxplot_stats_hover_data(panel_stats),
                hovertemplate=yield_boxplot_stats_hover_template(),
            ),
            row=1,
            col=column_index,
        )


def add_yield_boxplot_long_period_annotations(
    figure: Any,
    stats: pd.DataFrame,
    ofz_type_order: list[str],
    period_order: list[str],
    period_to_x: dict[str, str],
) -> None:
    """Добавить компактные подписи для facet mode без перегрузки min/max."""
    if stats.empty:
        return
    for column_index, ofz_type in enumerate(ofz_type_order, start=1):
        panel_stats = stats.loc[stats["ofz_type"].astype(str) == ofz_type].copy()
        for _, row in panel_stats.iterrows():
            period_label = str(row["report_period_label"])
            x_position = period_to_x.get(period_label, period_label)
            auction_count = int(row["auction_count"])
            median_value = float(row["yield_median"])
            text = (
                f"n=1<br>значение: {median_value:.2f}"
                if auction_count == 1
                else f"мед: {median_value:.2f}<br>n={auction_count}"
            )
            figure.add_annotation(
                x=x_position,
                y=median_value,
                text=text,
                showarrow=False,
                xshift=0,
                yshift=14,
                align="center",
                font={"size": 9, "color": "#1F2933"},
                bgcolor="rgba(255,255,255,0.70)",
                row=1,
                col=column_index,
            )


def add_yield_boxplot_compact_stat_trace(figure: Any, stats: pd.DataFrame) -> None:
    if stats.empty:
        return
    assert go is not None
    hover_stats = prepare_yield_boxplot_hover_stats(stats)
    hover_data = yield_boxplot_stats_hover_data(hover_stats)
    figure.add_trace(
        go.Scatter(
            x=stats["x_group"],
            y=stats["label_y"],
            mode="markers",
            marker={"size": 18, "color": "rgba(0,0,0,0)"},
            showlegend=False,
            hoverinfo="text",
            customdata=hover_data,
            hovertemplate=yield_boxplot_stats_hover_template(),
        )
    )
    for _, row in stats.iterrows():
        xshift = int(row["xshift"])
        if int(row["auction_count"]) == 1:
            figure.add_annotation(
                x=row["x_group"],
                y=row["yield_median"],
                text=row["compact_label"],
                showarrow=False,
                xshift=xshift + 20,
                yshift=18,
                align="left",
                font={"size": 9, "color": "#1F2933"},
                bgcolor="rgba(255,255,255,0.72)",
            )
            continue
        has_lower_outlier = pd.notna(row["outlier_min"])
        has_upper_outlier = pd.notna(row["outlier_max"])
        figure.add_annotation(
            x=row["x_group"],
            y=row["upper_whisker"],
            text=f"верхний ус: {float(row['upper_whisker']):.2f}" if has_upper_outlier else f"макс: {float(row['yield_max_actual']):.2f}",
            showarrow=False,
            xshift=xshift,
            yshift=12,
            font={"size": 9, "color": QUALITATIVE_COLORS[5]},
            bgcolor="rgba(255,255,255,0.60)",
        )
        if has_upper_outlier:
            figure.add_annotation(
                x=row["x_group"],
                y=row["yield_max_actual"],
                text=f"макс/выброс: {float(row['yield_max_actual']):.2f}",
                showarrow=False,
                xshift=xshift + 14,
                yshift=16,
                font={"size": 9, "color": "#F06969"},
                bgcolor="rgba(255,255,255,0.66)",
            )
        figure.add_annotation(
            x=row["x_group"],
            y=row["lower_whisker"],
            text=f"нижний ус: {float(row['lower_whisker']):.2f}" if has_lower_outlier else f"мин: {float(row['yield_min_actual']):.2f}",
            showarrow=False,
            xshift=xshift,
            yshift=-12,
            font={"size": 9, "color": "#166A75"},
            bgcolor="rgba(255,255,255,0.60)",
        )
        if has_lower_outlier:
            figure.add_annotation(
                x=row["x_group"],
                y=row["yield_min_actual"],
                text=f"мин/выброс: {float(row['yield_min_actual']):.2f}",
                showarrow=False,
                xshift=xshift - 14,
                yshift=-16,
                font={"size": 9, "color": "#F06969"},
                bgcolor="rgba(255,255,255,0.66)",
            )
        figure.add_annotation(
            x=row["x_group"],
            y=row["yield_median"],
            text=row["compact_label"],
            showarrow=False,
            xshift=xshift + 22,
            yshift=0,
            align="left",
            font={"size": 9, "color": "#1F2933"},
            bgcolor="rgba(255,255,255,0.70)",
        )


def prepare_yield_boxplot_hover_stats(stats: pd.DataFrame) -> pd.DataFrame:
    """Подготовить строковые значения статистик для hover."""
    hover_stats = stats.copy()
    for column in [
        "yield_min_actual",
        "yield_q1",
        "yield_median",
        "yield_q3",
        "yield_max_actual",
        "lower_whisker",
        "upper_whisker",
        "lower_fence",
        "upper_fence",
        "outlier_min",
        "outlier_max",
    ]:
        hover_stats[f"{column}_label"] = hover_stats[column].map(lambda value: format_hover_number(value, 2))
    hover_stats["placement_volume_label"] = hover_stats["placement_volume"].map(lambda value: format_hover_number(value, 1))
    return hover_stats


def yield_boxplot_stats_hover_data(hover_stats: pd.DataFrame) -> Any:
    """Вернуть customdata для hover статистик boxplot."""
    return hover_stats[
        [
            "report_period_display_label",
            "ofz_type",
            "yield_min_actual_label",
            "lower_whisker_label",
            "yield_q1_label",
            "yield_median_label",
            "yield_q3_label",
            "upper_whisker_label",
            "yield_max_actual_label",
            "upper_fence_label",
            "lower_fence_label",
            "outlier_min_label",
            "outlier_max_label",
            "auction_count",
            "placement_volume_label",
            "yield_column_used",
            "data_quality_flag",
        ]
    ].to_numpy()


def yield_boxplot_stats_hover_template() -> str:
    """Вернуть hover-шаблон для статистик boxplot."""
    return (
        "Период: %{customdata[0]}<br>"
        "Тип ОФЗ: %{customdata[1]}<br>"
        "Фактический минимум: %{customdata[2]}<br>"
        "Нижний ус: %{customdata[3]}<br>"
        "Q1: %{customdata[4]}<br>"
        "Медиана: %{customdata[5]}<br>"
        "Q3: %{customdata[6]}<br>"
        "Верхний ус: %{customdata[7]}<br>"
        "Фактический максимум: %{customdata[8]}<br>"
        "Upper fence: %{customdata[9]}<br>"
        "Lower fence: %{customdata[10]}<br>"
        "Нижний выброс: %{customdata[11]}<br>"
        "Верхний выброс: %{customdata[12]}<br>"
        "n: %{customdata[13]}<br>"
        "Объем размещения по номиналу: %{customdata[14]}<br>"
        "Колонка доходности: %{customdata[15]}<br>"
        "Флаг качества: %{customdata[16]}"
        "<extra></extra>"
    )


def demand_risk_hover_columns(data: pd.DataFrame) -> list[str]:
    return [
        column
        for column in [
            "auction_date",
            "report_period_label",
            "auction_quarter",
            "issue_code",
            "ofz_type",
            "format",
            "demand_volume",
            "supply_volume",
            "placement_volume",
            "_demand_to_placement",
            "_bid_to_cover",
            "_weighted_avg_yield",
            "_cutoff_price",
            "_weighted_avg_price",
            "maturity_bucket",
            "ratio_basis",
        ]
        if column in data.columns
    ]


def filter_target_period_for_cutoff_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> pd.DataFrame:
    data = df.copy()
    if "is_target_period" in data.columns:
        target_mask = data["is_target_period"].astype("string").str.lower().isin({"true", "1", "yes"})
        data = data.loc[target_mask].copy()
    elif "report_period_label" in data.columns:
        target_labels = {str(period["label"]) for period in params.periods if period.get("is_target_period")}
        data = data.loc[data["report_period_label"].astype("string").isin(target_labels)].copy()
        limitations.append("Колонка `is_target_period` отсутствует; целевой период определен по `report_period_label`.")
    else:
        limitations.append("График отсечения спроса не может определить целевой отчетный период.")
        return data.iloc[0:0].copy()

    if "format" in data.columns:
        before_format = len(data)
        format_values = data["format"].astype("string").str.strip().str.lower()
        data = data.loc[format_values.eq("аукцион") | format_values.eq("auction")].copy()
        removed = before_format - len(data)
        if removed:
            limitations.append(
                f"Из графика отсечения спроса исключены неаукционные строки: {removed}; анализ строится только по аукционам."
            )
    else:
        limitations.append("Колонка `format` отсутствует; фильтр `format = Аукцион` не применен.")
    return data


def add_cutoff_hover_and_labels(
    data: pd.DataFrame,
    y_column: str,
    color_column: str,
    top_n: int = 3,
) -> pd.DataFrame:
    result = data.copy()
    result["Дата"] = result["auction_date"].astype("string") if "auction_date" in result.columns else ""
    result["Период"] = result["report_period_label"].astype("string") if "report_period_label" in result.columns else ""
    result["Код выпуска"] = result["issue_code"].astype("string") if "issue_code" in result.columns else ""
    result["Тип ОФЗ"] = result["ofz_type"].astype("string") if "ofz_type" in result.columns else ""
    result["Формат"] = result["format"].astype("string") if "format" in result.columns else ""
    result["Спрос"] = result["_demand"].map(lambda value: format_hover_number(value, 1))
    result["Предложение"] = result["_supply"].map(lambda value: format_hover_number(value, 1))
    result["Размещение"] = result["_placement"].map(lambda value: format_hover_number(value, 1))
    result["Спрос / размещение"] = result["_demand_to_placement"].map(lambda value: format_hover_number(value, 3))
    result["Спрос / предложение"] = result["_bid_to_cover"].map(lambda value: format_hover_number(value, 3))
    result["Коэффициент удовлетворения спроса"] = result["_demand_satisfaction"].map(lambda value: format_hover_number(value, 3))
    result["Цена отсечения"] = result["_cutoff_price"].map(lambda value: format_hover_number(value, 2))
    result["Дисконт к номиналу"] = result["_discount_to_nominal"].map(lambda value: format_hover_number(value, 2))
    result["Доходность отсечения"] = result["_cutoff_yield"].map(lambda value: format_hover_number(value, 2))
    result["Средневзвешенная доходность"] = result["_weighted_avg_yield"].map(lambda value: format_hover_number(value, 2))
    result["Сроковая категория"] = result["maturity_bucket"].astype("string") if "maturity_bucket" in result.columns else ""

    label_indexes: set[Any] = set()
    for column in ["_demand_to_placement", y_column, color_column, "_placement"]:
        if column in result.columns:
            top = pd.to_numeric(result[column], errors="coerce").nlargest(top_n)
            label_indexes.update(top.index.tolist())

    result["Подпись"] = ""
    for index in label_indexes:
        issue_code = str(result.at[index, "Код выпуска"]) if "Код выпуска" in result.columns else ""
        auction_date = str(result.at[index, "Дата"]) if "Дата" in result.columns else ""
        result.at[index, "Подпись"] = f"{issue_code}<br>{auction_date}" if auction_date else issue_code
    return result


def add_cutoff_quadrant_annotations(figure: Any, data: pd.DataFrame, median_discount: float, y_column: str) -> None:
    max_x = pd.to_numeric(data["_demand_to_placement"], errors="coerce").max()
    max_y = pd.to_numeric(data[y_column], errors="coerce").max()
    min_y = pd.to_numeric(data[y_column], errors="coerce").min()
    high_x = max(float(max_x) * 0.78, 1.08) if pd.notna(max_x) else 1.2
    low_x = 0.55 if max_x is pd.NA or pd.isna(max_x) or float(max_x) > 0.8 else 0.8
    high_y = float(median_discount + (float(max_y) - median_discount) * 0.65) if pd.notna(max_y) else median_discount
    low_y = float(float(min_y) + (median_discount - float(min_y)) * 0.35) if pd.notna(min_y) else median_discount
    annotations = [
        (high_x, high_y, "Высокий спрос / высокий дисконт"),
        (high_x, low_y, "Высокий спрос / умеренный дисконт"),
        (low_x, high_y, "Низкий спрос / высокий дисконт"),
        (low_x, low_y, "Низкий спрос / умеренный дисконт"),
    ]
    for x_value, y_value, text in annotations:
        figure.add_annotation(
            x=x_value,
            y=y_value,
            text=text,
            showarrow=False,
            bgcolor="rgba(255,255,255,0.72)",
            bordercolor="rgba(31,41,51,0.25)",
            borderwidth=1,
            font={"size": 11, "color": "#1F2933"},
        )


def build_sankey_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    return build_sankey_result(
        df=df,
        params=params,
        limitations=limitations,
        name="sankey_structure",
        title="Структура объема размещения ОФЗ: период → вид бумаги → срок → формат",
        subtitle=(
            "Ширина потока соответствует объему размещения по номиналу; "
            "проценты показывают долю от общего объема выбранных периодов"
        ),
        chain=(
            ("report_period_label", "Период"),
            ("ofz_type", "Вид бумаги"),
            ("maturity_bucket_label", "Срок"),
            ("format", "Формат"),
        ),
    )
    required = ["report_period_label", "ofz_type", "maturity_bucket", "format", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"Sankey diagram пропущен: нет {', '.join(missing)}.")
        return None
    data = (
        df.groupby(["report_period_label", "ofz_type", "maturity_bucket", "format"], dropna=False)["_placement"]
        .sum()
        .reset_index()
    )
    data["Срок обращения"] = data["maturity_bucket"].map(
        {
            "short_term": "Краткосрочные",
            "medium_term": "Среднесрочные",
            "long_term": "Долгосрочные",
            "requires_review": "Требует проверки",
        }
    ).fillna(data["maturity_bucket"])
    data = data.rename(columns={"_placement": "placement_volume"})
    flows = build_sankey_flows(data)
    if flows.empty:
        limitations.append("Sankey-график пропущен: не удалось сформировать потоки по объему размещения.")
        return None
    labels, node_indices, node_labels, node_colors = build_sankey_nodes(flows)
    source = flows["source"].map(node_indices).tolist()
    target = flows["target"].map(node_indices).tolist()
    value = flows["placement_volume"].astype(float).tolist()
    link_colors = flows["period_color"].tolist()
    custom_data = flows[
        [
            "source",
            "target",
            "placement_volume_label",
            "share_total_label",
            "share_source_label",
            "auction_count",
        ]
    ].to_numpy()

    assert go is not None
    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node={
                    "label": node_labels,
                    "color": node_colors,
                    "pad": 26,
                    "thickness": 22,
                    "line": {"color": "rgba(31,41,51,0.35)", "width": 0.7},
                    "hovertemplate": "%{label}<extra></extra>",
                },
                link={
                    "source": source,
                    "target": target,
                    "value": value,
                    "color": link_colors,
                    "customdata": custom_data,
                    "hovertemplate": (
                        "Источник: %{customdata[0]}<br>"
                        "Получатель: %{customdata[1]}<br>"
                        "Объем размещения по номиналу, млн руб.: %{customdata[2]}<br>"
                        "Доля в общем объеме, %: %{customdata[3]}<br>"
                        "Доля внутри узла-источника, %: %{customdata[4]}<br>"
                        "Количество размещений: %{customdata[5]}"
                        "<extra></extra>"
                    ),
                },
            )
        ]
    )
    fig.update_layout(
        title_text="Структура объема размещения ОФЗ: период → вид бумаги → срок → формат",
        height=880,
        font={"size": 14, "family": "Arial, sans-serif", "color": "#1F2933"},
        margin={"l": 32, "r": 32, "t": 120, "b": 40},
    )
    fig.add_annotation(
        text="Ширина потока соответствует объему размещения по номиналу",
        xref="paper",
        yref="paper",
        x=0,
        y=1.08,
        showarrow=False,
        align="left",
        font={"size": 13, "color": "#1F2933"},
    )
    apply_common_layout(fig)
    fig.update_layout(
        height=880,
        font={"size": 14, "family": "Arial, sans-serif", "color": "#1F2933"},
        margin={"l": 32, "r": 32, "t": 120, "b": 40},
    )
    limitations.append(
        "Sankey-график использует `placement_volume` как value потоков; малые категории не удаляются и могут быть визуально тонкими."
    )
    return make_result("sankey_structure", fig, flows.drop(columns=["period_color", "placement_volume_label", "share_total_label", "share_source_label"]), params)


def build_sankey_flows(data: pd.DataFrame) -> pd.DataFrame:
    total_placement = pd.to_numeric(data["placement_volume"], errors="coerce").sum()
    period_labels = sorted(data["report_period_label"].dropna().astype(str).unique().tolist(), key=period_sort_key)
    period_color_map = {
        label: hex_to_rgba(color, 0.48)
        for label, color in palette.build_period_color_map(period_labels).items()
    }
    flow_specs = [
        ("report_period_label", "ofz_type", "Период", "Вид бумаги"),
        ("ofz_type", "Срок обращения", "Вид бумаги", "Срок"),
        ("Срок обращения", "format", "Срок", "Формат"),
    ]
    parts: list[pd.DataFrame] = []
    for source_column, target_column, source_layer, target_layer in flow_specs:
        grouped = (
            data.groupby([source_column, target_column], dropna=False)
            .agg(placement_volume=("placement_volume", "sum"), auction_count=("placement_volume", "size"))
            .reset_index()
            .rename(columns={source_column: "source", target_column: "target"})
        )
        grouped["source_layer"] = source_layer
        grouped["target_layer"] = target_layer
        parts.append(grouped)
    flows = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    if flows.empty:
        return flows
    source_totals = flows.groupby(["source_layer", "source"], dropna=False)["placement_volume"].transform("sum")
    flows["share_total"] = flows["placement_volume"] / total_placement if total_placement else pd.NA
    flows["share_source"] = flows["placement_volume"] / source_totals.mask(source_totals == 0)
    flows["placement_volume_label"] = flows["placement_volume"].map(lambda value: format_hover_number(value, 1))
    flows["share_total_label"] = (flows["share_total"] * 100).map(lambda value: format_hover_number(value, 2))
    flows["share_source_label"] = (flows["share_source"] * 100).map(lambda value: format_hover_number(value, 2))
    period_lookup = data[["ofz_type", "report_period_label"]].drop_duplicates()
    period_by_type = period_lookup.groupby("ofz_type")["report_period_label"].first().to_dict()
    flows["period_for_color"] = flows["source"].where(flows["source_layer"] == "Период")
    flows["period_for_color"] = flows["period_for_color"].fillna(flows["source"].map(period_by_type))
    flows["period_for_color"] = flows["period_for_color"].fillna(period_labels[0] if period_labels else "")
    flows["period_color"] = flows["period_for_color"].map(period_color_map).fillna(hex_to_rgba(QUALITATIVE_COLORS[0], 0.42))
    return flows[
        [
            "source",
            "target",
            "placement_volume",
            "share_total",
            "share_source",
            "auction_count",
            "source_layer",
            "target_layer",
            "period_color",
            "placement_volume_label",
            "share_total_label",
            "share_source_label",
        ]
    ]


def build_sankey_nodes(flows: pd.DataFrame) -> tuple[list[str], dict[str, int], list[str], list[str]]:
    node_names = unique_columns(flows["source"].astype(str).tolist() + flows["target"].astype(str).tolist())
    node_indices = {label: index for index, label in enumerate(node_names)}
    incoming = flows.groupby("target")["placement_volume"].sum()
    outgoing = flows.groupby("source")["placement_volume"].sum()
    node_volume = {
        label: max(float(incoming.get(label, 0.0)), float(outgoing.get(label, 0.0)))
        for label in node_names
    }
    total = max(flows["placement_volume"].sum() / 3, 1.0)
    node_labels = [
        f"{label}<br>{format_hover_number(node_volume[label] / 1000, 1)} млрд руб.<br>{format_hover_number(node_volume[label] / total * 100, 1)}%"
        for label in node_names
    ]
    layer_color_map = DIMENSION_COLOR_MAP
    layer_by_node: dict[str, str] = {}
    for _, row in flows.iterrows():
        layer_by_node[str(row["source"])] = str(row["source_layer"])
        layer_by_node[str(row["target"])] = str(row["target_layer"])
    node_colors = [layer_color_map.get(layer_by_node.get(label, ""), QUALITATIVE_COLORS[1]) for label in node_names]
    return node_names, node_indices, node_labels, node_colors


def build_sankey_period_maturity_type_format_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    return build_sankey_result(
        df=df,
        params=params,
        limitations=limitations,
        name="sankey_period_maturity_type_format",
        title="Структура размещений ОФЗ: период → срок → вид бумаги → формат",
        subtitle=(
            "Ширина потока соответствует объему размещения по номиналу; "
            "проценты показывают долю от общего объема выбранных периодов"
        ),
        chain=(
            ("report_period_label", "Период"),
            ("maturity_bucket_label", "Срок"),
            ("ofz_type", "Вид бумаги"),
            ("format", "Формат"),
        ),
    )


def build_sankey_period_format_type_maturity_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    return build_sankey_result(
        df=df,
        params=params,
        limitations=limitations,
        name="sankey_period_format_type_maturity",
        title="Структура размещений ОФЗ: период → формат → вид бумаги → срок",
        subtitle=(
            "Ширина потока соответствует объему размещения по номиналу; "
            "проценты показывают долю от общего объема выбранных периодов"
        ),
        chain=(
            ("report_period_label", "Период"),
            ("format", "Формат"),
            ("ofz_type", "Вид бумаги"),
            ("maturity_bucket_label", "Срок"),
        ),
    )


def build_sankey_period_format_maturity_type_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    return build_sankey_result(
        df=df,
        params=params,
        limitations=limitations,
        name="sankey_period_format_maturity_type",
        title="Структура размещений ОФЗ: период → формат → срок → вид бумаги",
        subtitle=(
            "Ширина потока соответствует объему размещения по номиналу; "
            "проценты показывают долю от общего объема выбранных периодов"
        ),
        chain=(
            ("report_period_label", "Период"),
            ("format", "Формат"),
            ("maturity_bucket_label", "Срок"),
            ("ofz_type", "Вид бумаги"),
        ),
    )


def build_sankey_target_period_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    suffix = make_suffix(params)
    target_labels = ", ".join(str(period["label"]) for period in params.periods if period.get("is_target_period"))
    return build_sankey_result(
        df=df,
        params=params,
        limitations=limitations,
        name="sankey_target_period",
        title=f"Структура размещений ОФЗ в отчетном периоде: {target_labels}",
        subtitle=(
            "Вид бумаги → срок обращения → формат; "
            "ширина потока соответствует объему размещения по номиналу"
        ),
        chain=(
            ("ofz_type", "Вид бумаги"),
            ("maturity_bucket_label", "Срок"),
            ("format", "Формат"),
        ),
        target_only=True,
        csv_path=config.EXPORTS_CHART_DATA_SANKEY_DIR / f"sankey_target_period_structure_{suffix}.csv",
    )


def build_sankey_result(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
    name: str,
    title: str,
    subtitle: str,
    chain: tuple[tuple[str, str], ...],
    target_only: bool = False,
    csv_path: Path | None = None,
) -> ChartResult | None:
    data = prepare_sankey_data(df, params, limitations, target_only=target_only)
    chain_columns = [column for column, _ in chain]
    if missing := missing_columns(data, chain_columns + ["placement_volume"]):
        limitations.append(f"Sankey `{name}` пропущен: нет {', '.join(missing)}.")
        return None
    data = data.dropna(subset=chain_columns + ["placement_volume"]).copy()
    data = data.loc[pd.to_numeric(data["placement_volume"], errors="coerce") > 0].copy()
    if data.empty:
        limitations.append(f"Sankey `{name}` пропущен: нет строк с положительным `placement_volume`.")
        return None
    flows = build_sankey_flows_for_chain(data, chain)
    if flows.empty:
        limitations.append(f"Sankey `{name}` пропущен: не удалось сформировать потоки по объему размещения.")
        return None
    figure = build_sankey_figure_v2(flows, title, subtitle)
    limitations.append(
        f"Sankey `{name}` использует `placement_volume` как value потоков; "
        "малые категории не удаляются и могут быть визуально тонкими."
    )
    result = make_result(name, figure, sankey_export_columns(flows), params)
    if csv_path is None:
        return result
    return ChartResult(
        name=result.name,
        figure=result.figure,
        export_data=result.export_data,
        html_path=result.html_path,
        csv_path=csv_path,
    )


def prepare_sankey_data(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
    target_only: bool,
) -> pd.DataFrame:
    required = ["ofz_type", "format", "_placement"]
    if missing := missing_columns(df, required):
        limitations.append(f"Sankey пропущен: нет {', '.join(missing)}.")
        return pd.DataFrame()
    data = df.copy()
    data["placement_volume"] = pd.to_numeric(data["_placement"], errors="coerce")
    if "maturity_bucket_label" not in data.columns:
        if "maturity_bucket" not in data.columns:
            limitations.append("Sankey пропущен: нет `maturity_bucket_label` или `maturity_bucket`.")
            return pd.DataFrame()
        data["maturity_bucket_label"] = data["maturity_bucket"].map(sankey_maturity_label).fillna(data["maturity_bucket"])
    else:
        data["maturity_bucket_label"] = data["maturity_bucket_label"].fillna("Требует проверки")
    data["maturity_bucket_label"] = data["maturity_bucket_label"].map(sankey_maturity_label)
    if target_only:
        data = filter_target_sankey_period(data, params, limitations)
    return data


def sankey_maturity_label(value: object) -> str:
    mapping = {
        "short_term": "Краткосрочные",
        "medium_term": "Среднесрочные",
        "long_term": "Долгосрочные",
        "requires_review": "Требует проверки",
        "Краткосрочные": "Краткосрочные",
        "Среднесрочные": "Среднесрочные",
        "Долгосрочные": "Долгосрочные",
        "Требует проверки": "Требует проверки",
    }
    return mapping.get(str(value), str(value))


def filter_target_sankey_period(
    data: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> pd.DataFrame:
    if "is_target_period" in data.columns:
        target_mask = data["is_target_period"].astype("string").str.lower().isin({"true", "1", "yes"})
        return data.loc[target_mask].copy()
    if "report_period_label" in data.columns:
        target_labels = {str(period["label"]) for period in params.periods if period.get("is_target_period")}
        limitations.append("Для целевого Sankey колонка `is_target_period` отсутствует; период определен по `report_period_label`.")
        return data.loc[data["report_period_label"].astype("string").isin(target_labels)].copy()
    limitations.append("Целевой Sankey пропущен: нет `is_target_period` и `report_period_label`.")
    return data.iloc[0:0].copy()


def build_sankey_flows_for_chain(data: pd.DataFrame, chain: tuple[tuple[str, str], ...]) -> pd.DataFrame:
    total_placement = pd.to_numeric(data["placement_volume"], errors="coerce").sum()
    period_labels = (
        sorted(data["report_period_label"].dropna().astype(str).unique().tolist(), key=period_sort_key)
        if "report_period_label" in data.columns
        else []
    )
    period_color_map = {
        label: hex_to_rgba(color, 0.48)
        for label, color in palette.build_period_color_map(period_labels).items()
    }
    parts: list[pd.DataFrame] = []
    for index in range(len(chain) - 1):
        source_column, source_layer = chain[index]
        target_column, target_layer = chain[index + 1]
        grouped = (
            data.groupby([source_column, target_column], dropna=False)
            .agg(placement_volume=("placement_volume", "sum"), auction_count=("placement_volume", "size"))
            .reset_index()
            .rename(columns={source_column: "source", target_column: "target"})
        )
        grouped["source_layer"] = source_layer
        grouped["target_layer"] = target_layer
        parts.append(grouped)
    flows = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    if flows.empty:
        return flows
    source_totals = flows.groupby(["source_layer", "source"], dropna=False)["placement_volume"].transform("sum")
    flows["share_total"] = flows["placement_volume"] / total_placement if total_placement else pd.NA
    flows["share_source"] = flows["placement_volume"] / source_totals.mask(source_totals == 0)
    flows["placement_volume_bln"] = flows["placement_volume"] / 1000.0
    flows["placement_volume_unit"] = "млн рублей"
    flows["placement_volume_bln_label"] = flows["placement_volume_bln"].map(lambda value: format_ru_number(value, 1))
    flows["share_total_label"] = (flows["share_total"] * 100).map(lambda value: format_ru_number(value, 1))
    flows["share_source_label"] = (flows["share_source"] * 100).map(lambda value: format_ru_number(value, 1))
    flows["period_for_color"] = flows["source"].where(flows["source_layer"] == "Период")
    flows["period_for_color"] = flows["period_for_color"].where(flows["period_for_color"].isin(period_labels), "")
    flows["period_color"] = flows["period_for_color"].map(period_color_map).fillna(hex_to_rgba(QUALITATIVE_COLORS[0], 0.38))
    return flows[
        [
            "source",
            "target",
            "placement_volume",
            "placement_volume_bln",
            "placement_volume_unit",
            "share_total",
            "share_source",
            "auction_count",
            "source_layer",
            "target_layer",
            "period_color",
            "placement_volume_bln_label",
            "share_total_label",
            "share_source_label",
        ]
    ]


def build_sankey_figure_v2(flows: pd.DataFrame, title: str, subtitle: str) -> Any:
    node_names, node_indices, node_labels, node_colors = build_sankey_nodes_v2(flows)
    custom_data = flows[
        [
            "source",
            "target",
            "placement_volume_bln_label",
            "share_total_label",
            "share_source_label",
            "auction_count",
        ]
    ].to_numpy()
    assert go is not None
    figure = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node={
                    "label": node_labels,
                    "color": node_colors,
                    "pad": 28,
                    "thickness": 24,
                    "line": {"color": "rgba(31,41,51,0.40)", "width": 0.8},
                    "hovertemplate": "%{label}<extra></extra>",
                },
                link={
                    "source": flows["source"].map(node_indices).tolist(),
                    "target": flows["target"].map(node_indices).tolist(),
                    "value": flows["placement_volume"].astype(float).tolist(),
                    "color": flows["period_color"].tolist(),
                    "customdata": custom_data,
                    "hovertemplate": (
                        "Источник: %{customdata[0]}<br>"
                        "Получатель: %{customdata[1]}<br>"
                        "Объем размещения по номиналу: %{customdata[2]} млрд руб.<br>"
                        "Доля в общем объеме: %{customdata[3]}%<br>"
                        "Доля внутри исходного узла: %{customdata[4]}%<br>"
                        "Количество размещений: %{customdata[5]}"
                        "<extra></extra>"
                    ),
                },
            )
        ]
    )
    figure.update_layout(
        title_text=title,
        height=920,
        font={"size": 14, "family": "Arial, sans-serif", "color": "#1F2933"},
        margin={"l": 36, "r": 36, "t": 132, "b": 44},
    )
    figure.add_annotation(
        text=subtitle,
        xref="paper",
        yref="paper",
        x=0,
        y=1.08,
        showarrow=False,
        align="left",
        font={"size": 13, "color": "#1F2933"},
    )
    return figure


def build_sankey_nodes_v2(flows: pd.DataFrame) -> tuple[list[str], dict[str, int], list[str], list[str]]:
    node_names = unique_columns(flows["source"].astype(str).tolist() + flows["target"].astype(str).tolist())
    node_indices = {label: index for index, label in enumerate(node_names)}
    incoming = flows.groupby("target")["placement_volume"].sum()
    outgoing = flows.groupby("source")["placement_volume"].sum()
    node_volume = {
        label: max(float(incoming.get(label, 0.0)), float(outgoing.get(label, 0.0)))
        for label in node_names
    }
    total = max(flows["placement_volume"].sum() / max(flows["source_layer"].nunique(), 1), 1.0)
    node_labels = [
        f"{label}<br>{format_ru_number(node_volume[label] / 1000, 1)} млрд руб.<br>{format_ru_number(node_volume[label] / total * 100, 1)}%"
        for label in node_names
    ]
    layer_color_map = DIMENSION_COLOR_MAP
    layer_by_node: dict[str, str] = {}
    for _, row in flows.iterrows():
        layer_by_node[str(row["source"])] = str(row["source_layer"])
        layer_by_node[str(row["target"])] = str(row["target_layer"])
    node_colors = [layer_color_map.get(layer_by_node.get(label, ""), QUALITATIVE_COLORS[1]) for label in node_names]
    return node_names, node_indices, node_labels, node_colors


def sankey_export_columns(flows: pd.DataFrame) -> pd.DataFrame:
    return flows[
        [
            "source",
            "target",
            "source_layer",
            "target_layer",
            "placement_volume",
            "placement_volume_bln",
            "placement_volume_unit",
            "share_total",
            "share_source",
            "auction_count",
        ]
    ].copy()

def hex_to_rgba(hex_color: str, alpha: float) -> str:
    color = hex_color.lstrip("#")
    red = int(color[0:2], 16)
    green = int(color[2:4], 16)
    blue = int(color[4:6], 16)
    return f"rgba({red},{green},{blue},{alpha})"


def weighted_average(values: pd.Series, weights: pd.Series) -> Any:
    valid = values.notna() & weights.notna() & (weights > 0)
    if valid.any():
        return float((values[valid] * weights[valid]).sum() / weights[valid].sum())
    return values.mean(skipna=True)


def missing_columns(df: pd.DataFrame, columns: list[str]) -> list[str]:
    return [column for column in columns if column not in df.columns]


def unique_columns(columns: list[str]) -> list[str]:
    result: list[str] = []
    for column in columns:
        if column not in result:
            result.append(column)
    return result


def markdown_table(df: pd.DataFrame, max_rows: int = 80) -> str:
    shown = df.head(max_rows).copy()
    headers = [str(column) for column in shown.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for _, row in shown.iterrows():
        cells = [markdown_cell(row[column]) for column in shown.columns]
        lines.append("| " + " | ".join(cells) + " |")
    if len(df) > max_rows:
        lines.append("| ... | " + " | ".join("" for _ in headers[1:]) + " |")
    return "\n".join(lines)


def markdown_cell(value: Any) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value).replace("|", r"\|").replace("\n", " ")


def make_result(name: str, figure: Any, data: pd.DataFrame, params: report_params.ReportParams) -> ChartResult:
    suffix = make_suffix(params)
    html_dir = config.chart_html_dir_for_name(name)
    csv_dir = chart_data_dir_for_name(name)
    ensure_directories(html_dir, csv_dir)
    export_data = data.copy()
    if "_placement" in export_data.columns and "placement_volume" not in export_data.columns:
        export_data["placement_volume"] = pd.to_numeric(export_data["_placement"], errors="coerce")
    if "placement_volume" in export_data.columns and "placement_volume_bln" not in export_data.columns:
        export_data["placement_volume_bln"] = pd.to_numeric(export_data["placement_volume"], errors="coerce") / 1000.0
    if "placement_volume" in export_data.columns and "placement_volume_unit" not in export_data.columns:
        export_data["placement_volume_unit"] = "млн рублей"
    return ChartResult(
        name=name,
        figure=figure,
        export_data=export_data,
        html_path=html_dir / f"{name}_{suffix}.html",
        csv_path=csv_dir / f"{name}_{suffix}.csv",
    )


def make_suffix(params: report_params.ReportParams) -> str:
    return make_report_suffix(params)


def chart_data_dir_for_name(name: str) -> Path:
    return chart_data_dir_for_metadata_name(name)


def write_limitations(
    params: report_params.ReportParams,
    limitations: list[str],
    results: list[ChartResult] | None = None,
) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Ограничения построения графиков",
        "",
        f"Дата формирования: `{now}`.",
        "",
        "## Параметры",
        "",
        f"- `report_date`: `{params.report_date.isoformat()}`",
        f"- `retrospective_years`: `{params.retrospective_years}`",
        f"- `period_type`: `{params.period_type}`",
        f"- `aggregation_mode`: `{params.aggregation_mode}`",
        "",
    ]
    if results is not None:
        lines.extend(["## Построенные графики", ""])
        if results:
            for result in results:
                lines.append(f"- `{result.html_path.relative_to(config.ROOT_DIR).as_posix()}`")
        else:
            lines.append("- Графики не построены.")
        lines.append("")

    lines.extend(
        [
            "## Визуальный стандарт",
            "",
            "- Для графиков используется приложенная цветовая система: качественная, последовательная, бинарная и сигнальная палитры.",
            "- Легенды, названия осей и отображаемые названия рядов выводятся на русском языке.",
            "- Для столбчатых, линейных и точечных графиков добавлены подписи данных; для Sankey значения доступны в интерактивной подсказке.",
            "- Во всех графиках с объемом размещения показатель трактуется как объем размещения по номиналу; на визуализациях объемы отображаются в млрд рублей, исходные млн рублей сохраняются в chart data.",
            "- Sankey-графики строятся по `placement_volume`; спрос не используется как ширина потоков.",
            "- Для Sankey точные значения малых категорий доступны в hover и таблицах-основах в `outputs/exports/chart_data/sankey/`.",
            "- ДРПА отображаются в Sankey как формат размещения, но не участвуют в demand-based ratios.",
            "- Классификация сроков для Sankey: краткосрочные - до 5 лет включительно, среднесрочные - свыше 5 и до 10 лет включительно, долгосрочные - более 10 лет.",
            "- Sankey по отчетному периоду фильтруется по `is_target_period == True`; при отсутствии колонки используется целевой `report_period_label`.",
            "- Квадрант риска `risk_quadrant` строится только по целевому отчетному периоду.",
            "- Квадрант риска отчетного года `risk_quadrant_demand_to_placement_by_quarter` строится только по отчетному году; по умолчанию подписываются только ключевые выбросы.",
            "- В графике отчетного года цветовая детализация по кварталам может быть ограничена, если в выборке присутствует только один квартал.",
            "- Ретроспективная версия `risk_quadrant_retrospective` строится по всем выбранным периодам и выделяет периоды цветом без разделения по срокам обращения.",
            "- `demand_to_placement_ratio` не равен `bid_to_cover_ratio`: первый показатель равен `demand_volume / placement_volume`, второй - `demand_volume / supply_volume`.",
            "- ДРПА не должны механически включаться в demand-based ratios, если по ним нет валидного спроса.",
            "- Несостоявшиеся аукционы с `placement_volume = 0` исключаются из графиков, где используется `demand_to_placement_ratio`.",
            "- Для анализа причин неудовлетворения спроса нужна цена отсечения или доходность отсечения; без цены отсечения интерпретация дисконта ограничена.",
            "",
        ]
    )

    lines.extend(["## Ограничения", ""])
    if limitations:
        for item in sorted(set(limitations)):
            lines.append(f"- {item}")
    else:
        lines.append("- Критических ограничений не выявлено.")
    lines.append("")
    utils.write_markdown(config.CHART_BUILD_LIMITATIONS_DOC, "\n".join(lines))


if __name__ == "__main__":
    raise SystemExit(main())
