"""Этап 9.3: помесячные визуализации для объяснения накопленного итога."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Sequence

import pandas as pd

px: Any = None
go: Any = None
try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    pass

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, palette, report_params, utils, yield_policy
else:
    from . import config, palette, report_params, utils, yield_policy


MONTHLY_METRICS_CSV = config.PROCESSED_DATA_DIR / "ofz_monthly_metrics.csv"
MONTHLY_VISUALIZATION_STRATEGY_DOC = config.get_doc_path("monthly_visualization_strategy.md")
REVENUE_ANALYTICS_REPORT_DOC = config.get_doc_path("revenue_analytics_report.md")

QUALITATIVE_COLORS = palette.QUALITATIVE_PALETTE
SEQUENTIAL_COLORS = palette.SEQUENTIAL_PALETTE
FORMAT_COLORS = palette.FORMAT_COLOR_MAP
MATURITY_COLORS = palette.MATURITY_COLOR_MAP
MATURITY_CATEGORY_ORDER = palette.MATURITY_CATEGORY_ORDER
STRUCTURE_COLORS = palette.STRUCTURE_PALETTE
MAX_MONTHLY_LINE_LABELS = 30
MONTH_LABELS = {
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


@dataclass(frozen=True)
class ChartResult:
    """Результат построения одного monthly-графика."""

    name: str
    figure: Any
    html_path: Path
    csv_path: Path
    dataframe: pd.DataFrame


MonthlyChartBuilder = Callable[[pd.DataFrame, report_params.ReportParams, list[str]], ChartResult | None]


def main(argv: Sequence[str] | None = None) -> int:
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт Этапа 9.3: помесячные графики")

    params = report_params.parse_report_args(argv)
    config.ensure_output_directories()
    limitations: list[str] = []

    if not plotly_available():
        limitations.append("Библиотека Plotly недоступна; помесячные графики не построены.")
        utils.write_markdown(MONTHLY_VISUALIZATION_STRATEGY_DOC, build_strategy_doc(params, [], limitations))
        logger.warning("Plotly недоступен, Этап 9.3 завершен с ограничениями")
        return 0

    metrics = read_monthly_metrics()
    metrics = filter_monthly_metrics(metrics, params)
    if metrics.empty:
        limitations.append("Monthly metrics пуст после фильтрации по параметрам отчета; графики не построены.")
        utils.write_markdown(MONTHLY_VISUALIZATION_STRATEGY_DOC, build_strategy_doc(params, [], limitations))
        logger.warning("Monthly metrics пуст, Этап 9.3 завершен с ограничениями")
        return 0

    prepared = prepare_metrics(metrics)
    config.CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    config.EXPORTS_CHART_DATA_DIR.mkdir(parents=True, exist_ok=True)

    results: list[ChartResult] = []
    for builder in chart_builders():
        result = builder(prepared, params, limitations)
        if result is None:
            continue
        result.figure.write_html(result.html_path)
        result.dataframe.to_csv(result.csv_path, index=False, encoding="utf-8-sig")
        results.append(result)
        logger.info("Помесячный график сохранен: %s", result.html_path)
        logger.info("Данные помесячного графика сохранены: %s", result.csv_path)

    utils.write_markdown(MONTHLY_VISUALIZATION_STRATEGY_DOC, build_strategy_doc(params, results, limitations))
    logger.info("Построено помесячных графиков: %s", len(results))
    logger.info("Этап 9.3 завершен")
    return 0


def plotly_available() -> bool:
    return px is not None and go is not None


def read_monthly_metrics() -> pd.DataFrame:
    if not MONTHLY_METRICS_CSV.exists():
        raise FileNotFoundError(
            f"Monthly metrics dataset не найден: {MONTHLY_METRICS_CSV}. "
            "Сначала выполните scripts/09_monthly_analytics.py."
        )
    return pd.read_csv(MONTHLY_METRICS_CSV)


def filter_monthly_metrics(
    metrics: pd.DataFrame,
    params: report_params.ReportParams,
) -> pd.DataFrame:
    """Оставить только месяцы выбранного отчетного горизонта."""
    required = {"report_period_label", "aggregation_mode", "report_year"}
    missing = required.difference(metrics.columns)
    if missing:
        raise ValueError(f"В monthly metrics отсутствуют обязательные колонки: {', '.join(sorted(missing))}.")

    labels = {str(period["report_period_label"]) for period in params.periods}
    years = {int(period["report_year"]) for period in params.periods}
    mask = (
        metrics["report_period_label"].astype("string").isin(labels)
        & (metrics["aggregation_mode"].astype("string") == params.aggregation_mode)
        & metrics["report_year"].astype("Int64").isin(years)
    )
    return metrics.loc[mask].copy()


def prepare_metrics(metrics: pd.DataFrame) -> pd.DataFrame:
    """Подготовить поля для визуализаций и русских hover."""
    df = metrics.copy()
    df["report_year"] = pd.to_numeric(df["report_year"], errors="coerce").astype("Int64").astype("string")
    df["month_number"] = pd.to_numeric(df["month_number"], errors="coerce").astype("Int64")
    df["Месяц"] = df["month_number"].map(MONTH_LABELS).fillna(df["month_label"].astype("string"))
    df["Год"] = df["report_year"].astype("string")
    df["Период"] = df["report_period_label"].astype("string")

    for column in numeric_columns():
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    volume_columns = [
        "total_demand",
        "total_supply",
        "total_placement_volume",
        "total_revenue_volume",
        "cumulative_demand",
        "cumulative_supply",
        "cumulative_placement_volume",
    "cumulative_revenue_volume",
        "placement_volume_auction",
        "placement_volume_drpa",
        "placement_volume_short_term",
        "placement_volume_medium_term",
        "placement_volume_long_term",
    ]
    for column in volume_columns:
        if column in df.columns:
            df[f"{column}_bln"] = df[column] / 1000.0
            df[f"{column}_unit"] = "млн рублей"
            df[f"{column}_bln_unit"] = "млрд рублей"
            df[f"{column}_bln_label"] = df[f"{column}_bln"].map(lambda value: format_ru_number(value, 1))
            df[f"{column}_mln_label"] = df[column].map(lambda value: format_ru_number(value, 1))
    return df.sort_values(["month_number", "Год"]).reset_index(drop=True)


def numeric_columns() -> list[str]:
    return [
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
        "cumulative_demand",
        "cumulative_supply",
        "cumulative_placement_volume",
        "cumulative_revenue_volume",
        "cumulative_bid_to_cover_ratio",
        "cumulative_weighted_avg_yield",
        "cumulative_auction_count",
        "ofz_pd_placement_volume",
        "ofz_in_placement_volume",
        "ofz_pk_placement_volume",
    ]


def chart_builders() -> list[MonthlyChartBuilder]:
    return [
        build_monthly_placement_volume_chart,
        build_monthly_cumulative_placement_chart,
        build_monthly_demand_supply_chart,
        build_monthly_bid_to_cover_chart,
        build_monthly_weighted_avg_yield_chart,
        build_monthly_placement_by_format_chart,
        build_monthly_placement_by_maturity_chart,
        build_monthly_heatmap_placement_chart,
        build_monthly_heatmap_revenue_chart,
    ]


def build_monthly_placement_volume_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    if "total_placement_volume_bln" not in df.columns:
        limitations.append("График помесячного объема размещения пропущен: нет `total_placement_volume`.")
        return None
    plot_df = prepare_monthly_placement_volume_labels(df)
    figure = px.bar(
        plot_df,
        x="Месяц",
        y="total_placement_volume_bln",
        color="Год",
        barmode="group",
        title="Помесячный объем размещения ОФЗ по номиналу",
        text="label_display",
        color_discrete_sequence=QUALITATIVE_COLORS,
        category_orders=category_orders(plot_df),
        labels={
            "total_placement_volume_bln": "Объем размещения по номиналу, млрд рублей",
            "Месяц": "Месяц",
            "Год": "Год",
        },
        custom_data=[
            "Период",
            "Год",
            "Месяц",
            "hover_value_bln",
            "hover_value_mln",
            "auction_count",
            "data_quality_flag",
            "hover_note",
        ],
    )
    figure.update_traces(
        textposition="outside",
        textfont={"size": 10},
        hovertemplate=(
            "Период: %{customdata[0]}<br>"
            "Год: %{customdata[1]}<br>"
            "Месяц: %{customdata[2]}<br>"
            "Объем размещения по номиналу: %{customdata[3]} млрд руб.<br>"
            "Объем размещения по номиналу: %{customdata[4]} млн руб.<br>"
            "%{customdata[7]}<br>"
            "Количество размещений: %{customdata[5]}<br>"
            "Качество данных: %{customdata[6]}<extra></extra>"
        ),
        cliponaxis=False,
    )
    figure.add_annotation(
        text="Показаны месячные значения за месяцы, входящие в отчетный период; объем в млрд рублей",
        xref="paper",
        yref="paper",
        x=0,
        y=1.08,
        showarrow=False,
        align="left",
        font={"size": 12, "color": "#1F2933"},
    )
    apply_common_layout(figure, "Год")
    apply_monthly_volume_axis(figure, "Объем размещения по номиналу, млрд рублей")
    export_data = chart_export_data(
        plot_df,
        [
            "month_order",
            "placement_volume",
            "placement_volume_bln",
            "total_placement_volume",
            "total_placement_volume_unit",
            "total_placement_volume_bln",
            "total_placement_volume_bln_unit",
            "label_display",
            "label_visible",
            "hover_value_bln",
            "hover_value_mln",
            "hover_note",
            "auction_count",
        ],
    )
    return make_result("monthly_placement_volume", figure, params, export_data)


def build_monthly_cumulative_placement_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    if "cumulative_placement_volume_bln" not in df.columns:
        limitations.append("График накопленного размещения пропущен: нет `cumulative_placement_volume`.")
        return None
    plot_df = prepare_monthly_cumulative_placement_labels(df)
    figure = px.line(
        plot_df,
        x="Месяц",
        y="cumulative_placement_volume_bln",
        color="Год",
        markers=True,
        text="label_display",
        title="Накопленный объем размещения ОФЗ по номиналу",
        color_discrete_sequence=QUALITATIVE_COLORS,
        category_orders=category_orders(plot_df),
        labels={"cumulative_placement_volume_bln": "Накопленный объем размещения по номиналу, млрд рублей", "Месяц": "Месяц"},
        custom_data=[
            "Год",
            "Месяц",
            "cumulative_placement_volume_bln_label",
            "cumulative_placement_volume_mln_label",
            "monthly_delta_bln_label",
            "aggregation_mode",
            "Период",
            "label_reason",
            "data_quality_flag",
        ],
    )
    figure.update_traces(
        textposition="top center",
        textfont={"size": 10},
        hovertemplate=(
            "Год: %{customdata[0]}<br>"
            "Месяц: %{customdata[1]}<br>"
            "Накопленный объем по номиналу: %{customdata[2]} млрд руб.<br>"
            "Накопленный объем по номиналу: %{customdata[3]} млн руб.<br>"
            "Прирост за месяц: %{customdata[4]} млрд руб.<br>"
            "Режим агрегации: %{customdata[5]}<br>"
            "Период отчета: %{customdata[6]}<br>"
            "Причина подписи: %{customdata[7]}<br>"
            "Качество данных: %{customdata[8]}<extra></extra>"
        ),
    )
    apply_common_layout(figure, "Год")
    apply_monthly_volume_axis(figure, "Накопленный объем размещения по номиналу, млрд рублей")
    export_data = chart_export_data(
        plot_df,
        [
            "cumulative_placement_volume",
            "cumulative_placement_volume_unit",
            "cumulative_placement_volume_bln",
            "cumulative_placement_volume_bln_unit",
            "monthly_delta_bln",
            "label_display",
            "label_reason",
            "cumulative_auction_count",
        ],
    )
    return make_result("monthly_cumulative_placement", figure, params, export_data)


def build_monthly_demand_supply_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = {"total_demand_bln", "total_supply_bln"}
    if not required.issubset(df.columns):
        limitations.append("График помесячного спроса и предложения пропущен: нет спроса или предложения.")
        return None
    long_df = df.melt(
        id_vars=monthly_melt_id_vars(df),
        value_vars=["total_demand_bln", "total_supply_bln"],
        var_name="metric_code",
        value_name="value_bln",
    )
    long_df["Показатель"] = long_df["metric_code"].map(
        {"total_demand_bln": "Спрос", "total_supply_bln": "Предложение"}
    )
    long_df["value_mln"] = pd.to_numeric(long_df["value_bln"], errors="coerce") * 1000.0
    max_value = pd.to_numeric(long_df["value_bln"], errors="coerce").max()
    label_threshold = float(max_value) * 0.03 if pd.notna(max_value) and float(max_value) > 0 else 0.0
    values = pd.to_numeric(long_df["value_bln"], errors="coerce")
    long_df["label_visible"] = values.ge(label_threshold) & values.gt(0)
    long_df["label_display"] = values.map(lambda value: format_ru_number(value, 1))
    long_df.loc[~long_df["label_visible"], "label_display"] = ""
    long_df["label_reason"] = long_df["label_visible"].map(
        {True: "value_above_visual_threshold", False: "small_value_hover_only"}
    )
    long_df["value_bln_label"] = values.map(lambda value: format_ru_number(value, 1))
    long_df["value_mln_label"] = long_df["value_mln"].map(lambda value: format_ru_number(value, 1))
    long_df["period_type"] = params.period_type
    figure = px.bar(
        long_df,
        x="Месяц",
        y="value_bln",
        color="Показатель",
        facet_col="Год",
        barmode="group",
        title="Помесячный спрос и предложение",
        text="label_display",
        color_discrete_sequence=palette.BINARY_PALETTE,
        category_orders=category_orders(df),
        labels={
            "value_bln": "Объем, млрд рублей",
            "Месяц": "Месяц",
            "Показатель": "Показатель",
        },
        custom_data=[
            "Год",
            "Период",
            "Показатель",
            "value_bln_label",
            "value_mln_label",
            "period_type",
            "aggregation_mode",
            "auction_count",
            "data_quality_flag",
            "label_reason",
        ],
    )
    figure.update_traces(
        textposition="outside",
        textfont={"size": 10},
        cliponaxis=False,
        hovertemplate=(
            "Год: %{customdata[0]}<br>"
            "Месяц: %{x}<br>"
            "Период: %{customdata[1]}<br>"
            "Показатель: %{customdata[2]}<br>"
            "Значение: %{customdata[3]} млрд руб.<br>"
            "Значение: %{customdata[4]} млн руб.<br>"
            "Тип периода: %{customdata[5]}<br>"
            "Режим агрегации: %{customdata[6]}<br>"
            "Размещений: %{customdata[7]}<br>"
            "Качество данных: %{customdata[8]}<br>"
            "Причина подписи: %{customdata[9]}<extra></extra>"
        )
    )
    figure.for_each_annotation(lambda annotation: annotation.update(text=annotation.text.replace("Год=", "Год: ")))
    apply_common_layout(figure, "Показатель")
    figure.update_yaxes(title_text="Объем, млрд рублей")
    keep_single_yaxis_title(figure, "Объем, млрд рублей")
    long_df["Единица измерения"] = "млрд рублей"
    return make_result("monthly_demand_supply", figure, params, long_df)


def _build_monthly_bid_to_cover_chart_legacy(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    if "bid_to_cover_ratio" not in df.columns:
        limitations.append("График помесячного bid-to-cover пропущен: нет `bid_to_cover_ratio`.")
        return None
    figure = px.line(
        df,
        x="Месяц",
        y="bid_to_cover_ratio",
        color="Год",
        markers=True,
        title="Помесячное покрытие предложения спросом",
        color_discrete_sequence=QUALITATIVE_COLORS,
        category_orders=category_orders(df),
        labels={"bid_to_cover_ratio": "Спрос / предложение", "Месяц": "Месяц"},
        custom_data=monthly_custom_data(df),
    )
    figure.update_traces(
        text=df["bid_to_cover_ratio"].map(lambda value: format_ru_number(value, 2)),
        textposition="top center",
        hovertemplate=base_ratio_hover("Спрос / предложение", "%{y:.2f}"),
    )
    figure.add_hline(
        y=1,
        line_dash="dash",
        line_color=palette.STATUS_PALETTE["риск"],
        annotation_text="Спрос = предложение",
    )
    apply_common_layout(figure, "Год")
    export_data = chart_export_data(df, ["bid_to_cover_ratio", "total_demand", "total_supply"])
    return make_result("monthly_bid_to_cover", figure, params, export_data)


def build_monthly_weighted_avg_yield_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    if "yield_weighted_avg" not in df.columns:
        limitations.append("График помесячной доходности пропущен: нет `yield_weighted_avg`.")
        return None
    figure = px.line(
        df,
        x="Месяц",
        y="yield_weighted_avg",
        color="Год",
        markers=True,
        title=yield_policy.BASE_YIELD_TITLE,
        color_discrete_sequence=QUALITATIVE_COLORS,
        category_orders=category_orders(df),
        labels={"yield_weighted_avg": "Средневзвешенная доходность ОФЗ-ПД, % годовых", "Месяц": "Месяц"},
        custom_data=monthly_custom_data(df),
    )
    figure.update_traces(
        text=df["yield_weighted_avg"].map(lambda value: format_ru_number(value, 2)),
        textposition="top center",
        hovertemplate=base_ratio_hover("Средневзвешенная доходность ОФЗ-ПД", "%{y:.2f}%"),
    )
    apply_common_layout(figure, "Год")
    export_data = chart_export_data(
        df,
        ["yield_weighted_avg", "yield_min", "yield_median", "yield_max", "total_placement_volume_bln"],
    )
    return make_result("monthly_weighted_avg_yield", figure, params, export_data)


def build_monthly_placement_by_format_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = {"placement_volume_auction_bln", "placement_volume_drpa_bln"}
    if not required.issubset(df.columns):
        limitations.append("График структуры по форматам пропущен: нет разбивки `placement_volume_auction/drpa`.")
        return None
    long_df = df.melt(
        id_vars=monthly_melt_id_vars(df),
        value_vars=["placement_volume_auction_bln", "placement_volume_drpa_bln"],
        var_name="Формат",
        value_name="Объем размещения по номиналу, млрд рублей",
    )
    long_df["Формат"] = long_df["Формат"].map(
        {"placement_volume_auction_bln": "Аукционы", "placement_volume_drpa_bln": "ДРПА"}
    )
    long_df = add_monthly_stacked_metrics(long_df, "Формат")
    figure = px.bar(
        long_df,
        x="Месяц",
        y="Объем размещения по номиналу, млрд рублей",
        color="Формат",
        text="Подпись",
        facet_col="Год",
        barmode="stack",
        title="Помесячная структура объема размещения по номиналу по форматам",
        color_discrete_map=FORMAT_COLORS,
        color_discrete_sequence=STRUCTURE_COLORS,
        category_orders=category_orders(df),
        custom_data=[
            "Год",
            "Месяц",
            "Сегмент",
            "Объем сегмента, млрд рублей",
            "Итого по столбцу",
            "Доля в столбце, %",
            "Доля в общей сумме, %",
            "auction_count",
            "data_quality_flag",
            "label_reason",
        ],
    )
    figure.update_traces(textposition="inside", hovertemplate=stacked_hover("Формат"))
    add_monthly_stacked_total_labels(figure, long_df)
    figure.for_each_annotation(lambda annotation: annotation.update(text=annotation.text.replace("Год=", "Год: ")))
    apply_common_layout(figure, "Формат")
    apply_monthly_volume_axis(figure, "Объем размещения по номиналу, млрд рублей")
    keep_single_yaxis_title(figure, "Объем размещения по номиналу, млрд рублей")
    long_df["Единица измерения"] = "млрд рублей"
    return make_result("monthly_placement_by_format", figure, params, long_df)


def build_monthly_placement_by_maturity_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    required = {
        "placement_volume_short_term_bln",
        "placement_volume_medium_term_bln",
        "placement_volume_long_term_bln",
    }
    if not required.issubset(df.columns):
        limitations.append("График структуры по срокам пропущен: нет разбивки по maturity bucket.")
        return None
    long_df = df.melt(
        id_vars=monthly_melt_id_vars(df),
        value_vars=sorted(required),
        var_name="Сроковая категория",
        value_name="Объем размещения по номиналу, млрд рублей",
    )
    long_df["Сроковая категория"] = long_df["Сроковая категория"].map(
        {
            "placement_volume_short_term_bln": "Краткосрочные",
            "placement_volume_medium_term_bln": "Среднесрочные",
            "placement_volume_long_term_bln": "Долгосрочные",
        }
    )
    long_df = add_monthly_stacked_metrics(long_df, "Сроковая категория")
    figure = px.bar(
        long_df,
        x="Месяц",
        y="Объем размещения по номиналу, млрд рублей",
        color="Сроковая категория",
        text="Подпись",
        facet_col="Год",
        barmode="stack",
        title="Помесячная структура объема размещения по номиналу по срокам обращения",
        color_discrete_map=MATURITY_COLORS,
        color_discrete_sequence=STRUCTURE_COLORS,
        category_orders=category_orders(df) | {"Сроковая категория": MATURITY_CATEGORY_ORDER},
        custom_data=[
            "Год",
            "Месяц",
            "Сегмент",
            "Объем сегмента, млрд рублей",
            "Итого по столбцу",
            "Доля в столбце, %",
            "Доля в общей сумме, %",
            "auction_count",
            "data_quality_flag",
            "label_reason",
        ],
    )
    figure.update_traces(textposition="inside", hovertemplate=stacked_hover("Сроковая категория"))
    add_monthly_stacked_total_labels(figure, long_df)
    figure.for_each_annotation(lambda annotation: annotation.update(text=annotation.text.replace("Год=", "Год: ")))
    apply_common_layout(figure, "Сроковая категория")
    apply_monthly_volume_axis(figure, "Объем размещения по номиналу, млрд рублей")
    keep_single_yaxis_title(figure, "Объем размещения по номиналу, млрд рублей")
    long_df["Единица измерения"] = "млрд рублей"
    return make_result("monthly_placement_by_maturity", figure, params, long_df)


def build_monthly_heatmap_placement_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    if "total_placement_volume_bln" not in df.columns:
        limitations.append("Heatmap размещения пропущен: нет `total_placement_volume`.")
        return None
    heatmap_data = build_monthly_heatmap_placement_data(df)
    if heatmap_data.empty:
        limitations.append("Heatmap размещения пропущен: нет валидных месячных объемов размещения.")
        return None
    years = sorted(heatmap_data["Год"].dropna().astype(str).unique().tolist())
    month_order = [MONTH_LABELS[number] for number in sorted(df["month_number"].dropna().astype(int).unique().tolist())]
    month_positions = list(range(len(month_order)))
    total_position = len(month_order) + 0.35
    z_matrix = (
        heatmap_data.loc[heatmap_data["color_scale_included"].astype(bool)]
        .pivot_table(index="Год", columns="Месяц", values="placement_volume_bln", aggfunc="sum", observed=False)
        .reindex(index=years, columns=month_order)
    )
    text_matrix = (
        heatmap_data.loc[heatmap_data["color_scale_included"].astype(bool)]
        .pivot_table(index="Год", columns="Месяц", values="label_display", aggfunc="first", observed=False)
        .reindex(index=years, columns=month_order)
    )
    custom_matrices = [
        heatmap_data.loc[heatmap_data["color_scale_included"].astype(bool)]
        .pivot_table(index="Год", columns="Месяц", values=column, aggfunc="first", observed=False)
        .reindex(index=years, columns=month_order)
        for column in [
            "month_hover",
            "placement_volume_display",
            "auction_count",
            "period_summing_label",
        ]
    ]
    customdata = [
        [
            [matrix.iloc[row_index, column_index] for matrix in custom_matrices]
            for column_index in range(len(month_order))
        ]
        for row_index in range(len(years))
    ]
    total_data = heatmap_data.loc[heatmap_data["is_total_column"].astype(bool)].copy()
    total_data = total_data.set_index("Год").reindex(years).reset_index()
    total_z = [[1.0] for _ in years]
    total_text = [[value] for value in total_data["label_display"].fillna("").astype(str).tolist()]
    total_customdata = [
        [
            [
                str(row.get("period_summing_label", "")),
                str(row.get("placement_volume_display", "")),
                row.get("auction_count", ""),
            ]
        ]
        for _, row in total_data.iterrows()
    ]
    monthly_zmax = pd.to_numeric(
        heatmap_data.loc[heatmap_data["color_scale_included"].astype(bool), "placement_volume_bln"],
        errors="coerce",
    ).max()
    assert go is not None
    figure = go.Figure(
        data=go.Heatmap(
            z=z_matrix.to_numpy(),
            x=month_positions,
            y=years,
            text=text_matrix.fillna("").to_numpy(),
            texttemplate="%{text}",
            textfont={"size": 11},
            customdata=customdata,
            colorscale=SEQUENTIAL_COLORS,
            zmin=0,
            zmax=float(monthly_zmax) if pd.notna(monthly_zmax) and float(monthly_zmax) > 0 else None,
            colorbar={
                "title": "Объем размещения по номиналу, млрд рублей",
                "tickformat": ",.0f",
                "exponentformat": "none",
                "showexponent": "none",
            },
            hovertemplate=(
                "Год: %{y}<br>"
                "%{customdata[0]}<br>"
                "Объем размещения по номиналу: %{customdata[1]} млрд руб.<br>"
                "Количество размещений: %{customdata[2]}<extra></extra>"
            ),
            name="Месячные значения",
        )
    )
    figure.add_trace(
        go.Heatmap(
            z=total_z,
            x=[total_position],
            y=years,
            text=total_text,
            texttemplate="%{text}",
            textfont={"size": 11, "color": "#111827"},
            customdata=total_customdata,
            colorscale=[[0, "#F3F4F6"], [1, "#F3F4F6"]],
            showscale=False,
            hovertemplate=(
                "Год: %{y}<br>"
                "Показатель: Итого за период<br>"
                "Период суммирования: %{customdata[0]}<br>"
                "Итоговый объем размещения по номиналу: %{customdata[1]} млрд руб.<br>"
                "Количество размещений: %{customdata[2]}<extra></extra>"
            ),
            name="Итого",
        )
    )
    figure.update_layout(
        title=(
            "Heatmap объема размещения по номиналу: месяц × год"
            "<br><sup>Цветовая шкала применяется только к месячным значениям; колонка «Итого» показана справочно</sup>"
        )
    )
    figure.update_xaxes(
        title="Месяц",
        tickmode="array",
        tickvals=month_positions + [total_position],
        ticktext=month_order + ["Итого"],
    )
    figure.update_yaxes(title="Год")
    figure.add_vline(
        x=len(month_order) - 0.5,
        line_width=1,
        line_color="#9CA3AF",
        line_dash="solid",
    )
    apply_common_layout(figure, "")
    export_data = add_volume_unit_columns(heatmap_data)
    return make_result("monthly_heatmap_placement", figure, params, export_data)


def build_monthly_heatmap_placement_data(df: pd.DataFrame) -> pd.DataFrame:
    """Подготовить long-format данные heatmap с отдельной колонкой `Итого`."""
    base_columns = [
        "report_year",
        "month",
        "month_number",
        "month_label",
        "report_period_label",
        "aggregation_mode",
        "Месяц",
        "Год",
        "total_placement_volume",
        "total_placement_volume_bln",
        "auction_count",
    ]
    existing = [column for column in base_columns if column in df.columns]
    monthly = df.loc[:, existing].copy()
    monthly["month_order"] = pd.to_numeric(monthly["month_number"], errors="coerce")
    monthly["placement_volume_bln"] = pd.to_numeric(monthly["total_placement_volume_bln"], errors="coerce")
    monthly["is_total_column"] = False
    monthly["total_placement_volume_bln"] = monthly.groupby("Год", dropna=False)["placement_volume_bln"].transform("sum")
    monthly["label_display"] = monthly["placement_volume_bln"].map(lambda value: format_ru_number(value, 1))
    monthly["placement_volume_display"] = monthly["placement_volume_bln"].map(lambda value: format_ru_number(value, 1))
    monthly["period_summing_label"] = ""
    monthly["month_hover"] = "Месяц: " + monthly["Месяц"].astype(str)
    monthly["color_scale_included"] = True

    total = (
        monthly.groupby(["Год", "report_year", "report_period_label", "aggregation_mode"], dropna=False)
        .agg(
            placement_volume_bln=("placement_volume_bln", "sum"),
            total_placement_volume_bln=("placement_volume_bln", "sum"),
            auction_count=("auction_count", "sum"),
            month_order_min=("month_order", "min"),
            month_order_max=("month_order", "max"),
        )
        .reset_index()
    )
    total["month"] = "Итого"
    total["month_number"] = 99
    total["month_label"] = "Итого"
    total["Месяц"] = "Итого"
    total["month_order"] = 99
    total["is_total_column"] = True
    total["color_scale_included"] = False
    total["label_display"] = total["placement_volume_bln"].map(lambda value: format_ru_number(value, 1))
    total["placement_volume_display"] = total["placement_volume_bln"].map(lambda value: format_ru_number(value, 1))
    total["period_summing_label"] = total.apply(
        lambda row: heatmap_total_period_label(row.get("month_order_min"), row.get("month_order_max")),
        axis=1,
    )
    total["month_hover"] = "Итого за период: " + total["period_summing_label"].astype(str)
    total = total.drop(columns=["month_order_min", "month_order_max"])
    result = pd.concat([monthly, total], ignore_index=True)
    result = result.sort_values(["Год", "month_order"]).reset_index(drop=True)
    return result


def heatmap_total_period_label(start_month: Any, end_month: Any) -> str:
    """Вернуть подпись периода суммирования для итоговой колонки heatmap."""
    try:
        start = int(start_month)
        end = int(end_month)
    except (TypeError, ValueError):
        return "выбранные месяцы"
    start_label = MONTH_LABELS.get(start, str(start))
    end_label = MONTH_LABELS.get(end, str(end))
    if start == end:
        return start_label
    return f"{start_label}-{end_label}"


def build_monthly_heatmap_revenue_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Построить heatmap помесячной выручки с нейтральной итоговой колонкой."""
    heatmap_data = build_monthly_heatmap_revenue_data(df, params, limitations)
    if heatmap_data.empty:
        limitations.append("Heatmap выручки пропущен: нет валидных данных выручки.")
        write_revenue_heatmap_warning(
            "Heatmap выручки не построен: в monthly layer и report scope нет валидной выручки для выбранного отчета."
        )
        return None

    years = sorted(heatmap_data["Год"].dropna().astype(str).unique().tolist())
    month_order = [
        MONTH_LABELS[number]
        for number in sorted(
            heatmap_data.loc[~heatmap_data["is_total_column"].map(is_truthy), "month_order"]
            .dropna()
            .astype(int)
            .unique()
            .tolist()
        )
    ]
    month_positions = list(range(len(month_order)))
    total_position = len(month_order) + 0.35
    monthly_rows = heatmap_data.loc[heatmap_data["color_scale_included"].map(is_truthy)]
    z_matrix = (
        monthly_rows.pivot_table(index="Год", columns="Месяц", values="revenue_volume_bln", aggfunc="sum", observed=False)
        .reindex(index=years, columns=month_order)
    )
    text_matrix = (
        monthly_rows.pivot_table(index="Год", columns="Месяц", values="label_display", aggfunc="first", observed=False)
        .reindex(index=years, columns=month_order)
    )
    custom_matrices = [
        monthly_rows.pivot_table(index="Год", columns="Месяц", values=column, aggfunc="first", observed=False)
        .reindex(index=years, columns=month_order)
        for column in [
            "month_hover",
            "revenue_display",
            "placement_display",
            "gap_display",
            "revenue_to_nominal_ratio_display",
            "auction_count",
            "data_quality_flag",
        ]
    ]
    customdata = [
        [
            [matrix.iloc[row_index, column_index] for matrix in custom_matrices]
            for column_index in range(len(month_order))
        ]
        for row_index in range(len(years))
    ]
    total_data = heatmap_data.loc[heatmap_data["is_total_column"].map(is_truthy)].copy()
    total_data = total_data.set_index("Год").reindex(years).reset_index()
    total_text = [[value] for value in total_data["label_display"].fillna("").astype(str).tolist()]
    total_customdata = [
        [
            [
                str(row.get("period_summing_label", "")),
                str(row.get("revenue_display", "")),
                str(row.get("placement_display", "")),
                str(row.get("gap_display", "")),
                str(row.get("revenue_to_nominal_ratio_display", "")),
                row.get("auction_count", ""),
                str(row.get("data_quality_flag", "")),
            ]
        ]
        for _, row in total_data.iterrows()
    ]
    monthly_zmax = pd.to_numeric(monthly_rows["revenue_volume_bln"], errors="coerce").max()

    assert go is not None
    figure = go.Figure(
        data=go.Heatmap(
            z=z_matrix.to_numpy(),
            x=month_positions,
            y=years,
            text=text_matrix.fillna("").to_numpy(),
            texttemplate="%{text}",
            textfont={"size": 11},
            customdata=customdata,
            colorscale=SEQUENTIAL_COLORS,
            zmin=0,
            zmax=float(monthly_zmax) if pd.notna(monthly_zmax) and float(monthly_zmax) > 0 else None,
            colorbar={
                "title": "Выручка от реализации, млрд рублей",
                "tickformat": ",.0f",
                "exponentformat": "none",
                "showexponent": "none",
            },
            hovertemplate=(
                "Год: %{y}<br>"
                "%{customdata[0]}<br>"
                "Выручка: %{customdata[1]} млрд руб.<br>"
                "Размещение по номиналу: %{customdata[2]} млрд руб.<br>"
                "Номинал минус выручка: %{customdata[3]} млрд руб.<br>"
                "Выручка / номинал: %{customdata[4]}%<br>"
                "Количество размещений: %{customdata[5]}<br>"
                "Качество данных: %{customdata[6]}<extra></extra>"
            ),
            name="Месячные значения",
        )
    )
    figure.add_trace(
        go.Heatmap(
            z=[[1.0] for _ in years],
            x=[total_position],
            y=years,
            text=total_text,
            texttemplate="%{text}",
            textfont={"size": 11, "color": "#111827"},
            customdata=total_customdata,
            colorscale=[[0, "#F3F4F6"], [1, "#F3F4F6"]],
            showscale=False,
            hovertemplate=(
                "Год: %{y}<br>"
                "Показатель: Итого за период<br>"
                "Период суммирования: %{customdata[0]}<br>"
                "Итоговая выручка: %{customdata[1]} млрд руб.<br>"
                "Размещение по номиналу: %{customdata[2]} млрд руб.<br>"
                "Номинал минус выручка: %{customdata[3]} млрд руб.<br>"
                "Выручка / номинал: %{customdata[4]}%<br>"
                "Количество размещений: %{customdata[5]}<br>"
                "Качество данных: %{customdata[6]}<extra></extra>"
            ),
            name="Итого",
        )
    )
    figure.update_layout(
        title=(
            "Помесячная выручка от реализации ОФЗ"
            "<br><sup>Цветовая шкала применяется только к месячным значениям; колонка «Итого» показана справочно</sup>"
        )
    )
    figure.update_xaxes(
        title="Месяц",
        tickmode="array",
        tickvals=month_positions + [total_position],
        ticktext=month_order + ["Итого"],
    )
    figure.update_yaxes(title="Год")
    figure.add_vline(x=len(month_order) - 0.5, line_width=1, line_color="#9CA3AF", line_dash="solid")
    apply_common_layout(figure, "")
    export_data = add_volume_unit_columns(heatmap_data)
    return make_result(
        "monthly_heatmap_revenue",
        figure,
        params,
        export_data,
        csv_dir=config.EXPORTS_CHART_DATA_MONTHLY_DIR,
    )


def build_monthly_heatmap_revenue_data(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> pd.DataFrame:
    """Подготовить данные heatmap выручки из monthly layer или report scope fallback."""
    if "total_revenue_volume_bln" in df.columns and pd.to_numeric(df["total_revenue_volume_bln"], errors="coerce").notna().any():
        monthly = build_monthly_heatmap_revenue_data_from_metrics(df)
        source_note = "monthly_metrics.total_revenue_volume"
    else:
        monthly = build_monthly_heatmap_revenue_data_from_scope(params, limitations)
        source_note = str(monthly["revenue_source"].dropna().iloc[0]) if "revenue_source" in monthly.columns and monthly["revenue_source"].notna().any() else "ofz_auctions_report_scope.proceeds_mln_rub"

    if monthly.empty:
        return monthly
    monthly["revenue_source"] = source_note
    monthly["color_scale_included"] = True
    monthly["is_total_column"] = False
    monthly["label_display"] = monthly["revenue_volume_bln"].map(lambda value: format_ru_number(value, 1))
    monthly["revenue_display"] = monthly["revenue_volume_bln"].map(lambda value: format_ru_number(value, 1))
    monthly["placement_display"] = monthly["placement_volume_bln"].map(lambda value: format_ru_number(value, 1))
    monthly["nominal_revenue_gap_bln"] = monthly["placement_volume_bln"] - monthly["revenue_volume_bln"]
    monthly["gap_display"] = monthly["nominal_revenue_gap_bln"].map(lambda value: format_ru_number(value, 1))
    monthly["revenue_to_nominal_ratio"] = monthly["revenue_volume_bln"] / monthly["placement_volume_bln"]
    monthly.loc[monthly["placement_volume_bln"].isna() | (monthly["placement_volume_bln"] == 0), "revenue_to_nominal_ratio"] = pd.NA
    monthly["revenue_to_nominal_ratio_display"] = (monthly["revenue_to_nominal_ratio"] * 100).map(
        lambda value: format_ru_number(value, 1)
    )
    monthly["month_hover"] = "Месяц: " + monthly["Месяц"].astype(str)
    monthly["total_revenue_volume_bln"] = monthly.groupby("Год", dropna=False)["revenue_volume_bln"].transform("sum")

    total = (
        monthly.groupby(["Год", "report_year", "report_period_label", "aggregation_mode"], dropna=False)
        .agg(
            revenue_volume_bln=("revenue_volume_bln", "sum"),
            placement_volume_bln=("placement_volume_bln", "sum"),
            nominal_revenue_gap_bln=("nominal_revenue_gap_bln", "sum"),
            total_revenue_volume_bln=("revenue_volume_bln", "sum"),
            auction_count=("auction_count", "sum"),
            month_order_min=("month_order", "min"),
            month_order_max=("month_order", "max"),
            data_quality_flag=("data_quality_flag", combine_quality_flags),
            revenue_source=("revenue_source", "first"),
        )
        .reset_index()
    )
    total["month"] = "Итого"
    total["month_number"] = 99
    total["month_label"] = "Итого"
    total["Месяц"] = "Итого"
    total["month_order"] = 99
    total["is_total_column"] = True
    total["color_scale_included"] = False
    total["label_display"] = total["revenue_volume_bln"].map(lambda value: format_ru_number(value, 1))
    total["revenue_display"] = total["revenue_volume_bln"].map(lambda value: format_ru_number(value, 1))
    total["placement_display"] = total["placement_volume_bln"].map(lambda value: format_ru_number(value, 1))
    total["gap_display"] = total["nominal_revenue_gap_bln"].map(lambda value: format_ru_number(value, 1))
    total["revenue_to_nominal_ratio"] = total["revenue_volume_bln"] / total["placement_volume_bln"]
    total.loc[total["placement_volume_bln"].isna() | (total["placement_volume_bln"] == 0), "revenue_to_nominal_ratio"] = pd.NA
    total["revenue_to_nominal_ratio_display"] = (total["revenue_to_nominal_ratio"] * 100).map(
        lambda value: format_ru_number(value, 1)
    )
    total["period_summing_label"] = total.apply(
        lambda row: heatmap_total_period_label(row.get("month_order_min"), row.get("month_order_max")),
        axis=1,
    )
    total["month_hover"] = "Итого за период: " + total["period_summing_label"].astype(str)
    total = total.drop(columns=["month_order_min", "month_order_max"])
    monthly["period_summing_label"] = ""
    result = pd.concat([monthly, total], ignore_index=True)
    return result.sort_values(["Год", "month_order"]).reset_index(drop=True)


def build_monthly_heatmap_revenue_data_from_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Взять выручку из готового monthly metrics layer."""
    placement_volume = (
        df["total_placement_volume_bln"]
        if "total_placement_volume_bln" in df.columns
        else pd.Series(pd.NA, index=df.index)
    )
    auction_count = (
        df["auction_count"]
        if "auction_count" in df.columns
        else pd.Series(0, index=df.index)
    )
    data_quality_flag = (
        df["data_quality_flag"]
        if "data_quality_flag" in df.columns
        else pd.Series("", index=df.index)
    )
    result = pd.DataFrame(
        {
            "report_year": df["report_year"],
            "month": df["month"],
            "month_number": df["month_number"],
            "month_label": df["month_label"],
            "report_period_label": df["report_period_label"],
            "aggregation_mode": df["aggregation_mode"],
            "Месяц": df["Месяц"],
            "Год": df["Год"],
            "month_order": pd.to_numeric(df["month_number"], errors="coerce"),
            "revenue_volume_bln": pd.to_numeric(df["total_revenue_volume_bln"], errors="coerce"),
            "placement_volume_bln": pd.to_numeric(placement_volume, errors="coerce"),
            "auction_count": pd.to_numeric(auction_count, errors="coerce").fillna(0),
            "data_quality_flag": data_quality_flag.fillna("").astype(str),
        }
    )
    return result.dropna(subset=["revenue_volume_bln"])


def build_monthly_heatmap_revenue_data_from_scope(
    params: report_params.ReportParams,
    limitations: list[str],
) -> pd.DataFrame:
    """Fallback: агрегировать выручку из report scope по `proceeds_mln_rub`."""
    if not config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.exists():
        limitations.append("Heatmap выручки пропущен: нет report scope для fallback-агрегации.")
        return pd.DataFrame()
    scope = pd.read_csv(config.OFZ_AUCTIONS_REPORT_SCOPE_CSV)
    revenue_col = detect_revenue_column(scope)
    if revenue_col is None:
        limitations.append("Heatmap выручки пропущен: в report scope нет колонки выручки.")
        write_revenue_heatmap_warning("Heatmap выручки не построен: не найдена колонка выручки в report scope.")
        return pd.DataFrame()
    required = {"report_period_label", "aggregation_mode", "report_year", "auction_date"}
    missing = required.difference(scope.columns)
    if missing:
        limitations.append(f"Heatmap выручки пропущен: в report scope нет колонок {', '.join(sorted(missing))}.")
        return pd.DataFrame()
    labels = {str(period["report_period_label"]) for period in params.periods}
    years = {int(period["report_year"]) for period in params.periods}
    source_note = f"ofz_auctions_report_scope.{revenue_col}"
    data = scope.loc[
        scope["report_period_label"].astype("string").isin(labels)
        & (scope["aggregation_mode"].astype("string") == params.aggregation_mode)
        & pd.to_numeric(scope["report_year"], errors="coerce").astype("Int64").isin(years)
    ].copy()
    if data.empty:
        data = build_revenue_scope_from_features(params, limitations)
        if data.empty:
            limitations.append("Heatmap выручки пропущен: report scope/features пусты после фильтрации.")
            return pd.DataFrame()
        revenue_col = detect_revenue_column(data)
        if revenue_col is None:
            limitations.append("Heatmap выручки пропущен: в features fallback нет колонки выручки.")
            return pd.DataFrame()
        source_note = f"ofz_auctions_features.{revenue_col}"
    data["_auction_date"] = pd.to_datetime(data["auction_date"], errors="coerce")
    data["month_order"] = data["_auction_date"].dt.month
    data = data.dropna(subset=["month_order"])
    data["month_order"] = data["month_order"].astype(int)
    data["revenue_volume"] = pd.to_numeric(data[revenue_col], errors="coerce")
    placement_volume = (
        data["placement_volume"]
        if "placement_volume" in data.columns
        else pd.Series(pd.NA, index=data.index)
    )
    data["placement_volume"] = pd.to_numeric(placement_volume, errors="coerce")
    data = data.dropna(subset=["revenue_volume"])
    if data.empty:
        limitations.append(f"Heatmap выручки пропущен: колонка `{revenue_col}` не содержит валидных значений.")
        write_revenue_heatmap_warning(f"Heatmap выручки не построен: `{revenue_col}` пуст для выбранного отчета.")
        return pd.DataFrame()
    grouped = (
        data.groupby(["report_year", "report_period_label", "aggregation_mode", "month_order"], dropna=False)
        .agg(
            revenue_volume=("revenue_volume", "sum"),
            placement_volume=("placement_volume", "sum"),
            auction_count=("auction_date", "count"),
            data_quality_flag=("data_quality_flag", combine_quality_flags)
            if "data_quality_flag" in data.columns
            else ("auction_date", lambda _: ""),
        )
        .reset_index()
    )
    grouped["report_year"] = grouped["report_year"].astype(int).astype(str)
    grouped["month"] = grouped["report_year"] + "-" + grouped["month_order"].astype(int).astype(str).str.zfill(2)
    grouped["month_number"] = grouped["month_order"]
    grouped["month_label"] = grouped["month_order"].map(MONTH_LABELS)
    grouped["Месяц"] = grouped["month_order"].map(MONTH_LABELS)
    grouped["Год"] = grouped["report_year"]
    grouped["revenue_volume_bln"] = grouped["revenue_volume"] / 1000.0
    grouped["placement_volume_bln"] = grouped["placement_volume"] / 1000.0
    grouped["revenue_source"] = source_note
    limitations.append(f"Heatmap выручки использует fallback-источник `{source_note}`.")
    return grouped


def build_revenue_scope_from_features(params: report_params.ReportParams, limitations: list[str]) -> pd.DataFrame:
    """Сформировать временный report scope для выручки из features, если текущий scope для другого отчета."""
    features_path = config.PROCESSED_DATA_DIR / "ofz_auctions_features.csv"
    if not features_path.exists():
        limitations.append("Heatmap выручки: features fallback недоступен, файл не найден.")
        return pd.DataFrame()
    features = pd.read_csv(features_path)
    if "auction_date" not in features.columns:
        limitations.append("Heatmap выручки: в features fallback нет auction_date.")
        return pd.DataFrame()
    features["_auction_date"] = pd.to_datetime(features["auction_date"], errors="coerce")
    chunks: list[pd.DataFrame] = []
    for period in params.periods:
        start = pd.to_datetime(period["period_start"])
        end = pd.to_datetime(period["period_end"])
        period_data = features.loc[
            (features["_auction_date"] >= start)
            & (features["_auction_date"] <= end)
        ].copy()
        if period_data.empty:
            continue
        period_data["report_period_label"] = period["report_period_label"]
        period_data["report_period_display_label"] = period.get("report_period_display_label", period["report_period_label"])
        period_data["report_year"] = period["report_year"]
        period_data["aggregation_mode"] = params.aggregation_mode
        period_data["report_period_type"] = params.period_type
        chunks.append(period_data)
    if not chunks:
        return pd.DataFrame()
    limitations.append("Heatmap выручки использует features fallback, потому что текущий report scope не соответствует параметрам отчета.")
    return pd.concat(chunks, ignore_index=True)


def detect_revenue_column(df: pd.DataFrame) -> str | None:
    """Найти фактическую колонку выручки в processed/report scope данных."""
    candidates = (
        "revenue_volume",
        "proceeds_volume",
        "placement_revenue",
        "placement_revenue_mln_rub",
        "revenue_amount_mln_rub",
        "proceeds_mln_rub",
    )
    lookup = {str(column).strip().lower(): str(column) for column in df.columns}
    for candidate in candidates:
        if candidate in lookup:
            return lookup[candidate]
    return None


def combine_quality_flags(values: pd.Series) -> str:
    """Собрать человекочитаемый список flags без дублей."""
    flags: list[str] = []
    for value in values.fillna("").astype(str):
        for part in value.replace("|", ";").split(";"):
            text = part.strip()
            if text and text not in flags:
                flags.append(text)
    return "; ".join(flags) if flags else "ok"


def write_revenue_heatmap_warning(message: str) -> None:
    """Добавить warning в revenue analytics report, если heatmap выручки нельзя построить."""
    existing = REVENUE_ANALYTICS_REPORT_DOC.read_text(encoding="utf-8") if REVENUE_ANALYTICS_REPORT_DOC.exists() else ""
    if message in existing:
        return
    addition = f"\n\n## Warning: monthly_heatmap_revenue\n\n- {message}\n"
    utils.write_markdown(REVENUE_ANALYTICS_REPORT_DOC, existing + addition if existing else addition.lstrip())


def monthly_custom_data(df: pd.DataFrame) -> list[str]:
    columns = ["Период", "Год", "auction_count", "data_quality_flag"]
    return [column for column in columns if column in df.columns]


def monthly_melt_id_vars(df: pd.DataFrame) -> list[str]:
    """Вернуть периодные поля, которые нужно сохранить в CSV-основах long-format графиков."""
    columns = [
        "report_year",
        "month",
        "month_number",
        "month_label",
        "month_start",
        "month_end",
        "report_period_label",
        "aggregation_mode",
        "is_target_year",
        "Месяц",
        "Год",
        "Период",
        "auction_count",
        "data_quality_flag",
    ]
    return [column for column in columns if column in df.columns]


def category_orders(df: pd.DataFrame) -> dict[str, list[str]]:
    months = [MONTH_LABELS[number] for number in sorted(df["month_number"].dropna().astype(int).unique().tolist())]
    years = sorted(df["Год"].dropna().astype(str).unique().tolist())
    return {"Месяц": months, "Год": years}


def base_volume_hover(metric_label: str, value_template: str) -> str:
    return (
        "Период: %{customdata[0]}<br>"
        "Год: %{customdata[1]}<br>"
        "Месяц: %{x}<br>"
        f"{metric_label}: {value_template}<br>"
        "Размещений: %{customdata[2]}<br>"
        "Качество данных: %{customdata[3]}<extra></extra>"
    )


def base_placement_hover(metric_label: str) -> str:
    return (
        "Период: %{customdata[0]}<br>"
        "Год: %{customdata[1]}<br>"
        "Месяц: %{x}<br>"
        f"{metric_label}: %{{customdata[4]}} млрд руб.<br>"
        f"{metric_label}, млн рублей: %{{customdata[5]}}<br>"
        "Размещений: %{customdata[2]}<br>"
        "Качество данных: %{customdata[3]}<extra></extra>"
    )


def base_ratio_hover(metric_label: str, value_template: str) -> str:
    return (
        "Период: %{customdata[0]}<br>"
        "Год: %{customdata[1]}<br>"
        "Месяц: %{x}<br>"
        f"{metric_label}: {value_template}<br>"
        "Размещений: %{customdata[2]}<br>"
        "Качество данных: %{customdata[3]}<extra></extra>"
    )


def add_monthly_stacked_metrics(data: pd.DataFrame, category_column: str) -> pd.DataFrame:
    """Добавить totals и доли для помесячных stacked-графиков."""
    result = data.copy()
    value_column = "Объем размещения по номиналу, млрд рублей"
    values = pd.to_numeric(result[value_column], errors="coerce")
    result["column_total"] = result.groupby(["Год", "Месяц"])[value_column].transform("sum")
    grand_total = pd.to_numeric(result[value_column], errors="coerce").sum()
    result["segment_share_in_column"] = result[value_column] / result["column_total"]
    result["segment_share_total"] = result[value_column] / grand_total if grand_total else pd.NA
    result["label_visible"] = (
        values.gt(0)
        & pd.to_numeric(result["segment_share_in_column"], errors="coerce").ge(0.08)
    )
    result["Подпись"] = values.map(format_bln_short)
    result.loc[~result["label_visible"], "Подпись"] = ""
    result["label_reason"] = result["label_visible"].map(
        {True: "segment_share_above_8_percent", False: "small_segment_hover_only"}
    )
    result["Объем сегмента, млрд рублей"] = values.map(format_bln_short)
    result["Доля в столбце, %"] = result["segment_share_in_column"].map(format_percent_label)
    result["Доля в общей сумме, %"] = result["segment_share_total"].map(format_percent_label)
    result["Итого по столбцу"] = result["column_total"].map(format_bln_short)
    result["Сегмент"] = result[category_column].astype("string")
    return result


def add_monthly_stacked_total_labels(figure: Any, data: pd.DataFrame) -> None:
    """Добавить итоговые суммы над помесячными stacked-столбцами."""
    assert go is not None
    value_column = "Объем размещения по номиналу, млрд рублей"
    positive_segments = data.loc[pd.to_numeric(data[value_column], errors="coerce").fillna(0) > 0]
    segment_counts = positive_segments.groupby(["Год", "Месяц"])["Сегмент"].nunique()
    totals = data[["Год", "Месяц", "column_total"]].drop_duplicates().copy()
    totals = totals.loc[
        totals.apply(lambda row: int(segment_counts.get((row["Год"], row["Месяц"]), 0)) >= 2, axis=1)
    ]
    if totals.empty:
        return
    totals["Итого подпись"] = totals["column_total"].map(format_bln_short)
    years = sorted(totals["Год"].dropna().astype(str).unique().tolist())
    for index, year in enumerate(years, start=1):
        part = totals.loc[totals["Год"].astype(str) == year]
        if part.empty:
            continue
        figure.add_trace(
            go.Scatter(
                x=part["Месяц"],
                y=part["column_total"],
                text=part["Итого подпись"],
                mode="text",
                textposition="top center",
                textfont={"size": 10, "color": "#1F2933"},
                hoverinfo="skip",
                showlegend=False,
                name="Итого",
            ),
            row=1,
            col=index,
        )


def format_bln_short(value: Any) -> str:
    """Отформатировать млрд рублей без суффикса для подписей на графике."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return ""
    return f"{float(numeric):,.1f}".replace(",", " ").replace(".", ",")


def format_percent_label(value: Any) -> str:
    """Отформатировать долю как проценты с одним знаком."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return ""
    return f"{float(numeric) * 100:,.1f}".replace(",", " ").replace(".", ",")


def stacked_hover(category_label: str) -> str:
    return (
        "Год: %{customdata[0]}<br>"
        "Месяц: %{customdata[1]}<br>"
        f"{category_label}: %{{customdata[2]}}<br>"
        "Объем сегмента: %{customdata[3]} млрд руб.<br>"
        "Общий объем столбца: %{customdata[4]} млрд руб.<br>"
        "Доля сегмента в столбце, %: %{customdata[5]}<br>"
        "Доля сегмента в общей сумме, %: %{customdata[6]}<br>"
        "Размещений: %{customdata[7]}<br>"
        "Качество данных: %{customdata[8]}<br>"
        "Причина подписи: %{customdata[9]}<extra></extra>"
    )


def apply_common_layout(figure: Any, legend_title: str) -> None:
    figure.update_layout(
        template="plotly_white",
        font={"family": "Arial, sans-serif", "color": "#1F2933"},
        colorway=QUALITATIVE_COLORS,
        legend_title_text=legend_title,
        separators=", ",
        margin={"l": 72, "r": 36, "t": 92, "b": 64},
        hoverlabel={"font_size": 12, "font_family": "Arial, sans-serif"},
        uniformtext_minsize=9,
        uniformtext_mode="hide",
    )
    figure.update_yaxes(tickformat=",.1f", separatethousands=True, exponentformat="none", showexponent="none")


def apply_monthly_volume_axis(figure: Any, title: str) -> None:
    figure.update_yaxes(
        title_text=title,
        tickformat=",.0f",
        separatethousands=True,
        exponentformat="none",
        showexponent="none",
    )


def keep_single_yaxis_title(figure: Any, title: str) -> None:
    """Оставить подпись Y только на первой панели facet-графика."""
    for axis_name in figure.layout:
        if not str(axis_name).startswith("yaxis"):
            continue
        axis = getattr(figure.layout, str(axis_name))
        axis.update(title_text=title if str(axis_name) == "yaxis" else "")


def chart_export_data(df: pd.DataFrame, value_columns: Sequence[str]) -> pd.DataFrame:
    """Сформировать компактную CSV-основу графика с периодными ключами и выбранными метриками."""
    base_columns = [
        "report_year",
        "month",
        "month_number",
        "month_label",
        "month_start",
        "month_end",
        "report_period_label",
        "aggregation_mode",
        "is_target_year",
        "Период",
        "Год",
        "Месяц",
        "data_quality_flag",
        "yield_scope",
        "yield_observation_count",
        "mixed_security_types",
    ]
    columns = list(dict.fromkeys(base_columns + list(value_columns)))
    existing_columns = [column for column in columns if column in df.columns]
    result = df.loc[:, existing_columns].copy()
    return add_volume_unit_columns(result)


def add_volume_unit_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Добавить единицы измерения к volume-полям chart data."""
    result = df.copy()
    for column in list(result.columns):
        if "volume" not in str(column):
            continue
        if str(column).endswith("_label") or str(column).endswith("_unit"):
            continue
        unit_column = f"{column}_unit"
        if unit_column in result.columns:
            continue
        result[unit_column] = "млрд рублей" if str(column).endswith("_bln") else "млн рублей"
    return result


def make_result(
    name: str,
    figure: Any,
    params: report_params.ReportParams,
    dataframe: pd.DataFrame,
    csv_dir: Path | None = None,
) -> ChartResult:
    suffix = make_output_suffix(params)
    html_dir = config.chart_html_dir_for_name(name)
    html_dir.mkdir(parents=True, exist_ok=True)
    export_dir = csv_dir or config.EXPORTS_CHART_DATA_DIR
    export_dir.mkdir(parents=True, exist_ok=True)
    return ChartResult(
        name=name,
        figure=figure,
        html_path=html_dir / f"{name}_{suffix}.html",
        csv_path=export_dir / f"{name}_{suffix}.csv",
        dataframe=dataframe,
    )


def make_output_suffix(params: report_params.ReportParams) -> str:
    return (
        f"{params.period_type}_{params.aggregation_mode}_{params.report_date.isoformat()}_"
        f"retrospective_{params.retrospective_years}"
    )


def format_ru_number(value: Any, digits: int = 1) -> str:
    if pd.isna(value):
        return ""
    text = f"{float(value):,.{digits}f}"
    return text.replace(",", " ").replace(".", ",")


def _build_strategy_doc_base(
    params: report_params.ReportParams,
    results: list[ChartResult],
    limitations: list[str],
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Стратегия помесячных визуализаций",
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
        "## Назначение",
        "",
        "Помесячные графики объясняют, из каких месяцев складывается накопленный итог отчетного периода. "
        "Объем размещения трактуется как объем размещения по номиналу: исходные данные считаются в млн руб., "
        "а на графиках отображаются в млрд руб.",
        "",
        "## Графики",
        "",
        "| График | Тип | Что показывает | Управленческий смысл |",
        "|---|---|---|---|",
        "| Помесячный объем размещения по номиналу | grouped bar | `total_placement_volume` по месяцам и годам, млрд руб. | Показывает, какие месяцы дали основной вклад в размещение. |",
        "| Накопленный объем размещения по номиналу | line | `cumulative_placement_volume`, млрд руб. | Сравнивает траекторию накопления размещений между годами. |",
        "| Помесячный спрос и предложение | grouped/facet bar | `total_demand` и `total_supply` | Показывает баланс рыночного спроса и объема предложения по месяцам. |",
        "| Помесячный bid-to-cover | line | `bid_to_cover_ratio = total_demand / total_supply` | Показывает месяцы с дефицитом или избытком спроса относительно предложения. |",
        "| Помесячная средневзвешенная доходность ОФЗ-ПД | line | `yield_weighted_avg`, `yield_scope=ofz_pd_only` | Показывает изменение стоимости фиксированных заимствований без ОФЗ-ПК и ОФЗ-ИН. |",
        "| Структура объема размещения по номиналу по форматам | stacked bar | аукционы и ДРПА, млрд руб. | Разделяет рыночные размещения и ДРПА. |",
        "| Структура объема размещения по номиналу по срокам | stacked bar | кратко-, средне- и долгосрочные размещения, млрд руб. | Показывает сдвиги в сроковой структуре размещений. |",
        "| Heatmap месяц × год | heatmap | `total_placement_volume`, млрд руб. | Быстро выделяет месяцы и годы с максимальной активностью. |",
        "",
        "## Созданные файлы",
        "",
    ]
    if results:
        for result in results:
            lines.append(f"- HTML: `{result.html_path.relative_to(config.PROJECT_ROOT).as_posix()}`")
            lines.append(f"- CSV-основа: `{result.csv_path.relative_to(config.PROJECT_ROOT).as_posix()}`")
    else:
        lines.append("- Графики не построены.")

    lines.extend(["", "## Ограничения", ""])
    if limitations:
        for limitation in limitations:
            lines.append(f"- {limitation}")
    else:
        lines.append("- Существенных ограничений не выявлено.")
    return "\n".join(lines)


def numeric_column_or_empty(df: pd.DataFrame, column: str) -> pd.Series:
    """Вернуть числовую колонку или пустой ряд с индексом исходной таблицы."""
    if column in df.columns:
        return pd.to_numeric(df[column], errors="coerce")
    return pd.Series(pd.NA, index=df.index, dtype="Float64")


def prepare_monthly_placement_volume_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Подготовить подписи, hover и export для помесячного объема размещения."""
    result = df.copy()
    result["placement_volume"] = numeric_column_or_empty(result, "total_placement_volume")
    result["placement_volume_bln"] = numeric_column_or_empty(result, "total_placement_volume_bln")
    result["month_order"] = numeric_column_or_empty(result, "month_number")
    result["label_visible"] = result["placement_volume_bln"].gt(0)
    result["label_display"] = result["placement_volume_bln"].map(lambda value: format_ru_number(value, 1))
    result.loc[~result["label_visible"], "label_display"] = ""
    result["hover_value_bln"] = result["placement_volume_bln"].map(lambda value: format_ru_number(value, 1))
    result["hover_value_mln"] = result["placement_volume"].map(lambda value: format_ru_number(value, 1))
    result["hover_note"] = result["placement_volume_bln"].map(
        lambda value: "Размещения не было" if pd.notna(value) and float(value) == 0 else ""
    )
    return result


def prepare_monthly_cumulative_placement_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Подготовить выборочные подписи для графика накопленного размещения."""
    result = df.copy()
    result["cumulative_placement_volume_bln"] = numeric_column_or_empty(result, "cumulative_placement_volume_bln")
    if "cumulative_placement_volume_mln_label" not in result.columns:
        cumulative_mln = numeric_column_or_empty(result, "cumulative_placement_volume")
        result["cumulative_placement_volume_mln_label"] = cumulative_mln.map(lambda value: format_ru_number(value, 1))
    if "cumulative_placement_volume_bln_label" not in result.columns:
        result["cumulative_placement_volume_bln_label"] = result["cumulative_placement_volume_bln"].map(
            lambda value: format_ru_number(value, 1)
        )
    if "total_placement_volume_bln" in result.columns:
        result["monthly_delta_bln"] = numeric_column_or_empty(result, "total_placement_volume_bln")
    else:
        result = result.sort_values(["Год", "month_number"]).copy()
        result["monthly_delta_bln"] = (
            result.groupby("Год", dropna=False)["cumulative_placement_volume_bln"].diff()
        )
        first_by_year = result.groupby("Год", dropna=False)["cumulative_placement_volume_bln"].transform("first")
        result["monthly_delta_bln"] = result["monthly_delta_bln"].fillna(first_by_year)
    result["monthly_delta_bln_label"] = result["monthly_delta_bln"].map(lambda value: format_ru_number(value, 1))
    result["label_reason"] = ""
    result["label_display"] = ""

    label_parts_by_index: dict[Any, list[str]] = {index: [] for index in result.index}
    label_priority_by_index: dict[Any, int] = {index: 999 for index in result.index}

    sorted_result = result.sort_values(["Год", "month_number"])
    for _, group in sorted_result.groupby("Год", dropna=False):
        valid = group.dropna(subset=["cumulative_placement_volume_bln"])
        if valid.empty:
            continue
        add_monthly_label_reason(label_parts_by_index, label_priority_by_index, valid.index[-1], "последняя точка года", 5)
        add_monthly_label_reason(
            label_parts_by_index,
            label_priority_by_index,
            valid["cumulative_placement_volume_bln"].idxmax(),
            "максимум года",
            15,
        )

    if "is_target_year" in result.columns:
        target_mask = result["is_target_year"].map(is_truthy)
        for index in result.loc[target_mask].dropna(subset=["cumulative_placement_volume_bln"]).index:
            add_monthly_label_reason(label_parts_by_index, label_priority_by_index, index, "отчетный год", 10)

    deltas = pd.to_numeric(result["monthly_delta_bln"], errors="coerce").dropna()
    positive_deltas = deltas.loc[deltas > 0]
    if len(positive_deltas) >= 4:
        q1 = positive_deltas.quantile(0.25)
        q3 = positive_deltas.quantile(0.75)
        iqr = q3 - q1
        threshold = q3 + 1.5 * iqr if pd.notna(iqr) and float(iqr) > 0 else positive_deltas.quantile(0.90)
        for index in positive_deltas.loc[positive_deltas >= threshold].index:
            add_monthly_label_reason(label_parts_by_index, label_priority_by_index, index, "резкий месячный прирост", 20)

    selected_indexes = [index for index, parts in label_parts_by_index.items() if parts]
    if len(selected_indexes) > MAX_MONTHLY_LINE_LABELS:
        selected = result.loc[selected_indexes].copy()
        selected["_label_priority"] = selected.index.map(lambda index: label_priority_by_index.get(index, 999))
        selected["_monthly_delta_abs"] = pd.to_numeric(selected["monthly_delta_bln"], errors="coerce").abs()
        selected = selected.sort_values(
            ["_label_priority", "_monthly_delta_abs", "month_number"],
            ascending=[True, False, True],
        ).head(MAX_MONTHLY_LINE_LABELS)
        allowed = set(selected.index)
        for index in selected_indexes:
            if index not in allowed:
                label_parts_by_index[index] = []

    result["label_reason"] = [
        "; ".join(dict.fromkeys(label_parts_by_index.get(index, []))) for index in result.index
    ]
    result["label_display"] = result.apply(
        lambda row: format_ru_number(row["cumulative_placement_volume_bln"], 1) if row["label_reason"] else "",
        axis=1,
    )
    return result


def prepare_monthly_bid_to_cover_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Подготовить управляемые подписи для графика покрытия предложения спросом."""
    result = df.copy()
    result["bid_to_cover_ratio"] = numeric_column_or_empty(result, "bid_to_cover_ratio")
    result["total_demand"] = numeric_column_or_empty(result, "total_demand")
    result["total_supply"] = numeric_column_or_empty(result, "total_supply")
    result["threshold_distance"] = (result["bid_to_cover_ratio"] - 1.0).abs()
    result["is_threshold_crossing"] = False
    result["label_reason"] = ""
    result["label_display"] = ""
    label_parts_by_index: dict[Any, list[str]] = {index: [] for index in result.index}
    label_priority_by_index: dict[Any, int] = {index: 999 for index in result.index}

    for _, group in result.sort_values(["Год", "month_number"]).groupby("Год", dropna=False):
        valid = group.dropna(subset=["bid_to_cover_ratio"])
        if valid.empty:
            continue
        add_monthly_label_reason(label_parts_by_index, label_priority_by_index, valid.index[-1], "последняя точка года", 10)
        add_monthly_label_reason(label_parts_by_index, label_priority_by_index, valid["bid_to_cover_ratio"].idxmin(), "минимум", 20)
        add_monthly_label_reason(label_parts_by_index, label_priority_by_index, valid["bid_to_cover_ratio"].idxmax(), "максимум", 20)

        close_to_threshold = valid.loc[valid["threshold_distance"] <= 0.10].sort_values("threshold_distance").head(3)
        for index in close_to_threshold.index:
            add_monthly_label_reason(label_parts_by_index, label_priority_by_index, index, "около порога 1", 30)
            result.loc[index, "is_threshold_crossing"] = True

        previous_value: float | None = None
        for index, row in valid.iterrows():
            current = row["bid_to_cover_ratio"]
            if previous_value is not None and (previous_value - 1.0) * (float(current) - 1.0) <= 0:
                add_monthly_label_reason(label_parts_by_index, label_priority_by_index, index, "пересечение порога 1", 25)
                result.loc[index, "is_threshold_crossing"] = True
            previous_value = float(current)

    if "is_target_year" in result.columns:
        target_mask = result["is_target_year"].map(is_truthy)
        for index in result.loc[target_mask].dropna(subset=["bid_to_cover_ratio"]).index:
            add_monthly_label_reason(label_parts_by_index, label_priority_by_index, index, "отчетный год", 40)

    selected_indexes = [index for index, parts in label_parts_by_index.items() if parts]
    if len(selected_indexes) > MAX_MONTHLY_LINE_LABELS:
        selected = result.loc[selected_indexes].copy()
        selected["_label_priority"] = selected.index.map(lambda index: label_priority_by_index.get(index, 999))
        selected = selected.sort_values(["_label_priority", "threshold_distance", "month_number"]).head(MAX_MONTHLY_LINE_LABELS)
        allowed = set(selected.index)
        for index in selected_indexes:
            if index not in allowed:
                label_parts_by_index[index] = []

    result["label_reason"] = [
        "; ".join(dict.fromkeys(label_parts_by_index.get(index, []))) for index in result.index
    ]
    result["label_display"] = result.apply(
        lambda row: format_ru_number(row["bid_to_cover_ratio"], 2) if row["label_reason"] else "",
        axis=1,
    )
    return result


def add_monthly_label_reason(
    label_parts_by_index: dict[Any, list[str]],
    label_priority_by_index: dict[Any, int],
    index: Any,
    reason: str,
    priority: int,
) -> None:
    """Добавить причину подписи к точке без дублирования одинаковых причин."""
    if index not in label_parts_by_index:
        return
    parts = label_parts_by_index[index]
    if reason not in parts:
        parts.append(reason)
    current_priority = label_priority_by_index.get(index, 999)
    if priority < current_priority:
        label_priority_by_index[index] = priority


def is_truthy(value: Any) -> bool:
    """Нормализовать булево значение из CSV."""
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    return text in {"1", "true", "yes", "да", "истина"}


def monthly_bid_to_cover_hover() -> str:
    """Русифицированный hover для помесячного покрытия предложения спросом."""
    return (
        "Год: %{customdata[0]}<br>"
        "Месяц: %{customdata[1]}<br>"
        "Спрос: %{customdata[2]:,.1f} млн руб.<br>"
        "Предложение: %{customdata[3]:,.1f} млн руб.<br>"
        "Спрос / предложение: %{customdata[4]:.2f}<br>"
        "Режим агрегации: %{customdata[5]}<br>"
        "Период отчета: %{customdata[6]}<br>"
        "Причина подписи: %{customdata[7]}<br>"
        "Расстояние до порога 1: %{customdata[8]:.2f}<br>"
        "Качество данных: %{customdata[9]}<extra></extra>"
    )


def build_monthly_bid_to_cover_chart(
    df: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> ChartResult | None:
    """Построить помесячное покрытие предложения спросом с выборочными подписями."""
    if "bid_to_cover_ratio" not in df.columns:
        limitations.append("График помесячного покрытия предложения спросом пропущен: нет `bid_to_cover_ratio`.")
        return None
    plot_df = prepare_monthly_bid_to_cover_labels(df)
    figure = px.line(
        plot_df,
        x="Месяц",
        y="bid_to_cover_ratio",
        color="Год",
        markers=True,
        text="label_display",
        title="Помесячное покрытие предложения спросом",
        color_discrete_sequence=QUALITATIVE_COLORS,
        category_orders=category_orders(plot_df),
        labels={"bid_to_cover_ratio": "Спрос / предложение", "Месяц": "Месяц"},
        custom_data=[
            "Год",
            "Месяц",
            "total_demand",
            "total_supply",
            "bid_to_cover_ratio",
            "aggregation_mode",
            "report_period_label",
            "label_reason",
            "threshold_distance",
            "data_quality_flag",
        ],
    )
    figure.update_traces(
        textposition="top center",
        textfont={"size": 10},
        hovertemplate=monthly_bid_to_cover_hover(),
    )
    figure.add_hline(
        y=1,
        line_dash="dash",
        line_color=palette.STATUS_PALETTE["риск"],
        annotation_text="Спрос = предложение",
        annotation_position="top left",
    )
    apply_common_layout(figure, "Год")
    figure.update_yaxes(title_text="Спрос / предложение")
    export_data = chart_export_data(
        plot_df,
        [
            "bid_to_cover_ratio",
            "total_demand",
            "total_supply",
            "label_display",
            "label_reason",
            "threshold_distance",
            "is_threshold_crossing",
        ],
    )
    return make_result("monthly_bid_to_cover", figure, params, export_data)


BASE_MONTHLY_STRATEGY_DOC_BUILDER = _build_strategy_doc_base


def build_strategy_doc(
    params: report_params.ReportParams,
    results: list[ChartResult],
    limitations: list[str],
) -> str:
    """Сформировать документацию с описанием новой политики подписей monthly bid-cover."""
    base = BASE_MONTHLY_STRATEGY_DOC_BUILDER(params, results, limitations)
    extra = [
        "",
        "## Вторая модернизация: подписи monthly bid-cover",
        "",
        "- График `monthly_bid_to_cover` называется `Помесячное покрытие предложения спросом`.",
        "- Ось Y подписана как `Спрос / предложение`.",
        "- Горизонтальная линия `y = 1` подписана `Спрос = предложение`.",
        "- Подписи выводятся выборочно: последняя точка каждого года, минимум, максимум, точки около порога 1 и точки отчетного года.",
        f"- Максимальное число подписей на графике: `{MAX_MONTHLY_LINE_LABELS}`.",
        "- Полная детализация доступна в hover и CSV-основе графика.",
        "- CSV-основа содержит `label_display`, `label_reason`, `threshold_distance`, `is_threshold_crossing`.",
    ]
    return base + "\n" + "\n".join(extra)


if __name__ == "__main__":
    raise SystemExit(main())

