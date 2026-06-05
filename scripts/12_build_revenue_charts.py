"""Этап 11: графики по выручке от реализации ОФЗ.

Графики строятся по outputs Этапа 10 (`scripts/11_revenue_analytics.py`).
Все суммы на визуализациях отображаются в млрд рублей.
"""

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
    from scripts import config, palette, report_params, utils
else:
    from . import config, palette, report_params, utils


REVENUE_CHARTS_REPORT_DOC = config.get_doc_path("revenue_charts_report.md")
REVENUE_CHART_DATA_DIR = config.EXPORTS_CHART_DATA_REVENUE_DIR
QUALITATIVE_COLORS = palette.QUALITATIVE_PALETTE
MATURITY_COLORS = palette.MATURITY_COLOR_MAP
MATURITY_ORDER = palette.MATURITY_CATEGORY_ORDER


@dataclass(frozen=True)
class RevenueChartResult:
    """Результат построения одного revenue-графика."""

    name: str
    figure: Any
    html_path: Path
    csv_path: Path
    dataframe: pd.DataFrame


RevenueChartBuilder = Callable[[dict[str, pd.DataFrame], report_params.ReportParams, list[str]], RevenueChartResult | None]


def main(argv: Sequence[str] | None = None) -> int:
    """Построить revenue charts и сохранить chart data exports."""
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт Этапа 11: revenue charts")
    params = report_params.parse_report_args(argv)
    config.ensure_output_directories()
    REVENUE_CHART_DATA_DIR.mkdir(parents=True, exist_ok=True)
    limitations: list[str] = []

    if not plotly_available():
        limitations.append("Plotly недоступен; revenue-графики не построены.")
        utils.write_markdown(REVENUE_CHARTS_REPORT_DOC, build_report(params, [], limitations))
        return 0

    tables = read_revenue_tables(params)
    prepared = {name: prepare_revenue_table(table) for name, table in tables.items()}

    results: list[RevenueChartResult] = []
    for builder in chart_builders():
        result = builder(prepared, params, limitations)
        if result is None:
            continue
        result.figure.write_html(result.html_path)
        result.dataframe.to_csv(result.csv_path, index=False, encoding="utf-8-sig")
        results.append(result)
        logger.info("Revenue chart сохранен: %s", result.html_path)
        logger.info("Revenue chart data сохранены: %s", result.csv_path)

    utils.write_markdown(REVENUE_CHARTS_REPORT_DOC, build_report(params, results, limitations))
    logger.info("Revenue charts построены: %s", len(results))
    return 0


def plotly_available() -> bool:
    """Проверить доступность Plotly."""
    return px is not None and go is not None


def read_revenue_tables(params: report_params.ReportParams) -> dict[str, pd.DataFrame]:
    """Прочитать CSV-таблицы Этапа 10."""
    suffix = make_output_suffix(params)
    paths = {
        "summary": config.EXPORTS_ANALYTICAL_CSV_DIR / f"revenue_summary_{suffix}.csv",
        "monthly": config.EXPORTS_ANALYTICAL_CSV_DIR / f"revenue_monthly_{suffix}.csv",
        "by_ofz_type": config.EXPORTS_ANALYTICAL_CSV_DIR / f"revenue_by_ofz_type_{suffix}.csv",
        "by_maturity": config.EXPORTS_ANALYTICAL_CSV_DIR / f"revenue_by_maturity_{suffix}.csv",
        "by_format": config.EXPORTS_ANALYTICAL_CSV_DIR / f"revenue_by_format_{suffix}.csv",
    }
    missing = [path for path in paths.values() if not path.exists()]
    if missing:
        details = ", ".join(path.relative_to(config.PROJECT_ROOT).as_posix() for path in missing)
        raise FileNotFoundError(
            "Не найдены revenue CSV-таблицы Этапа 10: "
            f"{details}. Сначала выполните scripts/11_revenue_analytics.py с теми же параметрами."
        )
    return {name: pd.read_csv(path) for name, path in paths.items()}


def prepare_revenue_table(df: pd.DataFrame) -> pd.DataFrame:
    """Подготовить русские подписи, млрд рублей и поля hover."""
    result = df.copy()
    for column in [
        "placement_volume",
        "placement_volume_bln",
        "revenue_volume",
        "revenue_volume_bln",
        "nominal_revenue_gap",
        "nominal_revenue_gap_bln",
        "revenue_to_nominal_ratio",
        "nominal_discount_ratio",
        "auction_count",
        "month_number",
    ]:
        if column in result.columns:
            result[column] = pd.to_numeric(result[column], errors="coerce")

    if "placement_volume_bln" not in result.columns and "placement_volume" in result.columns:
        result["placement_volume_bln"] = result["placement_volume"] / 1000.0
    if "revenue_volume_bln" not in result.columns and "revenue_volume" in result.columns:
        result["revenue_volume_bln"] = result["revenue_volume"] / 1000.0
    if "nominal_revenue_gap_bln" not in result.columns and "nominal_revenue_gap" in result.columns:
        result["nominal_revenue_gap_bln"] = result["nominal_revenue_gap"] / 1000.0

    result["Период"] = result["report_period_label"].astype("string") if "report_period_label" in result.columns else ""
    result["Год"] = result["report_year"].astype("string") if "report_year" in result.columns else ""
    if "month_number" in result.columns:
        result["Месяц"] = result["month_number"].map(month_label_short)
    result["Размещение, млрд руб."] = result.get("placement_volume_bln", pd.Series(index=result.index)).map(lambda value: format_ru_number(value, 1))
    result["Выручка, млрд руб."] = result.get("revenue_volume_bln", pd.Series(index=result.index)).map(lambda value: format_ru_number(value, 1))
    result["Разница, млрд руб."] = result.get("nominal_revenue_gap_bln", pd.Series(index=result.index)).map(lambda value: format_ru_number(value, 1))
    result["Выручка / номинал"] = result.get("revenue_to_nominal_ratio", pd.Series(index=result.index)).map(lambda value: format_ru_number(value, 3))
    result["Дисконт, %"] = (result.get("nominal_discount_ratio", pd.Series(index=result.index)) * 100).map(lambda value: format_ru_number(value, 2))
    result["data_quality_flag"] = result["data_quality_flag"].fillna("").astype(str) if "data_quality_flag" in result.columns else ""
    return result


def chart_builders() -> list[RevenueChartBuilder]:
    """Вернуть список revenue chart builders."""
    return [
        build_revenue_vs_nominal_by_period,
        build_nominal_revenue_gap_by_period,
        build_revenue_to_nominal_ratio,
        build_monthly_revenue_vs_nominal,
        build_monthly_nominal_revenue_gap,
        build_revenue_gap_by_ofz_type,
        build_revenue_gap_by_maturity,
        build_format_nominal_revenue_gap,
        build_discount_vs_revenue_gap,
    ]


def build_revenue_vs_nominal_by_period(
    tables: dict[str, pd.DataFrame],
    params: report_params.ReportParams,
    limitations: list[str],
) -> RevenueChartResult | None:
    data = tables["summary"].copy()
    long_data = data.melt(
        id_vars=["report_period_label", "Период", "auction_count", "data_quality_flag"],
        value_vars=["placement_volume_bln", "revenue_volume_bln"],
        var_name="metric",
        value_name="value_bln",
    )
    long_data["Показатель"] = long_data["metric"].map(
        {
            "placement_volume_bln": "Объем размещения по номиналу",
            "revenue_volume_bln": "Выручка от реализации",
        }
    )
    long_data["Значение"] = long_data["value_bln"].map(lambda value: format_ru_number(value, 1))
    fig = px.bar(
        long_data,
        x="Период",
        y="value_bln",
        color="Показатель",
        barmode="group",
        text="Значение",
        color_discrete_sequence=[QUALITATIVE_COLORS[0], QUALITATIVE_COLORS[1]],
        title="Номинальное размещение и выручка от реализации ОФЗ",
        custom_data=["Период", "Показатель", "Значение", "auction_count", "data_quality_flag"],
    )
    fig.update_traces(hovertemplate=revenue_metric_hover_template())
    apply_volume_axis_layout(fig, "Объем, млрд рублей")
    return make_result("revenue_vs_nominal_by_period", fig, params, add_chart_units(long_data))


def build_nominal_revenue_gap_by_period(
    tables: dict[str, pd.DataFrame],
    params: report_params.ReportParams,
    limitations: list[str],
) -> RevenueChartResult | None:
    data = tables["summary"].copy()
    data["Подпись"] = data["nominal_revenue_gap_bln"].map(lambda value: format_ru_number(value, 1))
    fig = px.bar(
        data,
        x="Период",
        y="nominal_revenue_gap_bln",
        text="Подпись",
        color_discrete_sequence=[QUALITATIVE_COLORS[3]],
        title="Разница между номиналом и выручкой от реализации",
        custom_data=["Период", "Разница, млрд руб.", "Размещение, млрд руб.", "Выручка, млрд руб.", "auction_count", "data_quality_flag"],
    )
    fig.update_traces(hovertemplate=revenue_gap_hover_template())
    apply_volume_axis_layout(fig, "Номинал минус выручка, млрд рублей")
    return make_result("nominal_revenue_gap_by_period", fig, params, add_chart_units(data))


def build_revenue_to_nominal_ratio(
    tables: dict[str, pd.DataFrame],
    params: report_params.ReportParams,
    limitations: list[str],
) -> RevenueChartResult | None:
    data = tables["summary"].copy()
    data["ratio_pct"] = data["revenue_to_nominal_ratio"] * 100
    data["Подпись"] = data["ratio_pct"].map(lambda value: format_ru_number(value, 1))
    fig = px.line(
        data,
        x="Период",
        y="ratio_pct",
        markers=True,
        text="Подпись",
        title="Выручка от реализации к номинальному объему размещения",
        custom_data=["Период", "Подпись", "Размещение, млрд руб.", "Выручка, млрд руб.", "auction_count", "data_quality_flag"],
    )
    fig.update_traces(line={"color": QUALITATIVE_COLORS[1]}, textposition="top center", hovertemplate=revenue_ratio_hover_template())
    fig.update_yaxes(title="Выручка / номинал, %", ticksuffix="", separatethousands=True, showexponent="none")
    apply_common_layout(fig)
    return make_result("revenue_to_nominal_ratio", fig, params, add_chart_units(data))


def build_monthly_revenue_vs_nominal(
    tables: dict[str, pd.DataFrame],
    params: report_params.ReportParams,
    limitations: list[str],
) -> RevenueChartResult | None:
    data = tables["monthly"].copy()
    long_data = data.melt(
        id_vars=["report_year", "month_number", "Месяц", "Период", "auction_count", "data_quality_flag"],
        value_vars=["placement_volume_bln", "revenue_volume_bln"],
        var_name="metric",
        value_name="value_bln",
    )
    long_data["Показатель"] = long_data["metric"].map(
        {
            "placement_volume_bln": "Объем размещения по номиналу",
            "revenue_volume_bln": "Выручка от реализации",
        }
    )
    long_data["Значение"] = long_data["value_bln"].map(lambda value: format_ru_number(value, 1))
    fig = px.bar(
        long_data,
        x="Месяц",
        y="value_bln",
        color="Показатель",
        facet_col="report_year",
        barmode="group",
        text="Значение",
        color_discrete_sequence=[QUALITATIVE_COLORS[0], QUALITATIVE_COLORS[1]],
        title="Помесячное размещение и выручка от реализации ОФЗ",
        custom_data=["Период", "Месяц", "Показатель", "Значение", "auction_count", "data_quality_flag"],
    )
    fig.update_traces(hovertemplate=monthly_revenue_metric_hover_template())
    apply_volume_axis_layout(fig, "Объем, млрд рублей")
    keep_single_yaxis_title(fig, "Объем, млрд рублей")
    return make_result("monthly_revenue_vs_nominal", fig, params, add_chart_units(long_data))


def build_monthly_nominal_revenue_gap(
    tables: dict[str, pd.DataFrame],
    params: report_params.ReportParams,
    limitations: list[str],
) -> RevenueChartResult | None:
    data = tables["monthly"].copy()
    data["Подпись"] = data["nominal_revenue_gap_bln"].map(lambda value: format_ru_number(value, 1))
    fig = px.bar(
        data,
        x="Месяц",
        y="nominal_revenue_gap_bln",
        color="Год",
        text="Подпись",
        color_discrete_map=palette.build_period_color_map(sorted(data["Год"].dropna().astype(str).unique().tolist())),
        title="Помесячная разница между номиналом и выручкой",
        custom_data=["Период", "Месяц", "Разница, млрд руб.", "Размещение, млрд руб.", "Выручка, млрд руб.", "auction_count", "data_quality_flag"],
    )
    fig.update_traces(hovertemplate=monthly_revenue_gap_hover_template())
    apply_volume_axis_layout(fig, "Номинал минус выручка, млрд рублей")
    return make_result("monthly_nominal_revenue_gap", fig, params, add_chart_units(data))


def build_revenue_gap_by_ofz_type(
    tables: dict[str, pd.DataFrame],
    params: report_params.ReportParams,
    limitations: list[str],
) -> RevenueChartResult | None:
    data = tables["by_ofz_type"].copy()
    data["Подпись"] = data["nominal_revenue_gap_bln"].map(lambda value: format_ru_number(value, 1))
    fig = px.bar(
        data,
        x="Период",
        y="nominal_revenue_gap_bln",
        color="ofz_type",
        text="Подпись",
        color_discrete_sequence=QUALITATIVE_COLORS,
        title="Разница номинал - выручка по видам ОФЗ",
        custom_data=["Период", "ofz_type", "Разница, млрд руб.", "Размещение, млрд руб.", "Выручка, млрд руб.", "auction_count", "data_quality_flag"],
    )
    fig.update_traces(hovertemplate=category_gap_hover_template("Вид ОФЗ"))
    fig.update_layout(legend_title_text="Вид ОФЗ")
    apply_volume_axis_layout(fig, "Номинал минус выручка, млрд рублей")
    return make_result("revenue_gap_by_ofz_type", fig, params, add_chart_units(data))


def build_revenue_gap_by_maturity(
    tables: dict[str, pd.DataFrame],
    params: report_params.ReportParams,
    limitations: list[str],
) -> RevenueChartResult | None:
    data = tables["by_maturity"].copy()
    data["maturity_bucket_label"] = data["maturity_bucket_label"].fillna("Требует проверки").astype(str)
    data["Подпись"] = data["nominal_revenue_gap_bln"].map(lambda value: format_ru_number(value, 1))
    fig = px.bar(
        data,
        x="Период",
        y="nominal_revenue_gap_bln",
        color="maturity_bucket_label",
        text="Подпись",
        category_orders={"maturity_bucket_label": MATURITY_ORDER},
        color_discrete_map=MATURITY_COLORS,
        title="Разница номинал - выручка по срокам обращения",
        custom_data=["Период", "maturity_bucket_label", "Разница, млрд руб.", "Размещение, млрд руб.", "Выручка, млрд руб.", "auction_count", "data_quality_flag"],
    )
    fig.update_traces(hovertemplate=category_gap_hover_template("Сроковая категория"))
    fig.update_layout(legend_title_text="Сроковая категория")
    apply_volume_axis_layout(fig, "Номинал минус выручка, млрд рублей")
    return make_result("revenue_gap_by_maturity", fig, params, add_chart_units(data))


def build_format_nominal_revenue_gap(
    tables: dict[str, pd.DataFrame],
    params: report_params.ReportParams,
    limitations: list[str],
) -> RevenueChartResult | None:
    """Построить grouped bar разницы номинала и выручки по форматам размещения."""
    data = tables["by_format"].copy()
    required = {
        "report_period_label",
        "format",
        "placement_volume_bln",
        "revenue_volume_bln",
        "nominal_revenue_gap_bln",
    }
    missing = sorted(required - set(data.columns))
    if missing:
        limitations.append(
            "`format_nominal_revenue_gap` пропущен: нет колонок "
            + ", ".join(missing)
            + "."
        )
        return None
    data = data.dropna(subset=["nominal_revenue_gap_bln", "format"]).copy()
    if data.empty:
        limitations.append("`format_nominal_revenue_gap` пропущен: нет валидной разницы номинал-выручка по форматам.")
        return None

    data["format"] = data["format"].fillna("Требует проверки").astype(str)
    data["Подпись"] = data["nominal_revenue_gap_bln"].map(lambda value: format_ru_number(value, 1))
    data["revenue_to_nominal_pct"] = data["revenue_to_nominal_ratio"] * 100 if "revenue_to_nominal_ratio" in data.columns else pd.NA
    data["Выручка / номинал, %"] = data["revenue_to_nominal_pct"].map(lambda value: format_ru_number(value, 1))
    data["label_visible"] = data["nominal_revenue_gap_bln"].notna()
    data["label_reason"] = data["nominal_revenue_gap_bln"].map(
        lambda value: "real_zero" if pd.notna(value) and abs(float(value)) < 0.05 else "value"
    )

    fig = px.bar(
        data,
        x="Период",
        y="nominal_revenue_gap_bln",
        color="format",
        barmode="group",
        text="Подпись",
        color_discrete_map=palette.FORMAT_COLOR_MAP,
        title="Разница между номинальным размещением и выручкой по форматам",
        labels={
            "format": "Формат",
            "nominal_revenue_gap_bln": "Номинал минус выручка, млрд рублей",
            "Период": "Период",
        },
        custom_data=[
            "Период",
            "format",
            "Размещение, млрд руб.",
            "Выручка, млрд руб.",
            "Разница, млрд руб.",
            "Выручка / номинал, %",
            "auction_count",
            "data_quality_flag",
        ],
    )
    fig.update_traces(
        hovertemplate=(
            "Период: %{customdata[0]}<br>"
            "Формат: %{customdata[1]}<br>"
            "Размещение по номиналу: %{customdata[2]} млрд руб.<br>"
            "Выручка от реализации: %{customdata[3]} млрд руб.<br>"
            "Номинал минус выручка: %{customdata[4]} млрд руб.<br>"
            "Выручка / номинал: %{customdata[5]}%<br>"
            "Количество размещений: %{customdata[6]}<br>"
            "Флаг качества данных: %{customdata[7]}<extra></extra>"
        )
    )
    fig.update_layout(legend_title_text="Формат")
    apply_volume_axis_layout(fig, "Номинал минус выручка, млрд рублей")
    export = add_chart_units(data)
    export["revenue_to_nominal_pct_unit"] = "%"
    return make_result("format_nominal_revenue_gap", fig, params, export)


def build_discount_vs_revenue_gap(
    tables: dict[str, pd.DataFrame],
    params: report_params.ReportParams,
    limitations: list[str],
) -> RevenueChartResult | None:
    data = tables["by_ofz_type"].copy()
    data = data.dropna(subset=["nominal_discount_ratio", "nominal_revenue_gap_bln", "placement_volume_bln"]).copy()
    if data.empty:
        limitations.append("Scatter `discount_vs_revenue_gap` пропущен: нет валидного дисконта выручки или разницы номинал-выручка.")
        return None
    data["nominal_discount_pct"] = data["nominal_discount_ratio"] * 100
    data["Дисконт, %"] = data["nominal_discount_pct"].map(lambda value: format_ru_number(value, 2))
    fig = px.scatter(
        data,
        x="nominal_discount_pct",
        y="nominal_revenue_gap_bln",
        size="placement_volume_bln",
        color="ofz_type",
        size_max=42,
        color_discrete_sequence=QUALITATIVE_COLORS,
        title="Дисконт выручки и разница между номиналом и выручкой",
        labels={
            "ofz_type": "Вид ОФЗ",
            "nominal_discount_pct": "Дисконт к номиналу, %",
            "nominal_revenue_gap_bln": "Номинал минус выручка, млрд рублей",
            "placement_volume_bln": "Объем размещения по номиналу, млрд рублей",
        },
        custom_data=[
            "Период",
            "ofz_type",
            "Дисконт, %",
            "Разница, млрд руб.",
            "Размещение, млрд руб.",
            "Выручка, млрд руб.",
            "auction_count",
            "data_quality_flag",
        ],
    )
    fig.update_traces(
        hovertemplate=(
            "Период: %{customdata[0]}<br>"
            "Вид ОФЗ: %{customdata[1]}<br>"
            "Дисконт к номиналу: %{customdata[2]}%<br>"
            "Номинал минус выручка: %{customdata[3]} млрд руб.<br>"
            "Объем размещения по номиналу: %{customdata[4]} млрд руб.<br>"
            "Выручка от реализации: %{customdata[5]} млрд руб.<br>"
            "Количество размещений: %{customdata[6]}<br>"
            "Флаг качества данных: %{customdata[7]}<extra></extra>"
        )
    )
    fig.add_annotation(
        text="Размер точки = объем размещения по номиналу",
        xref="paper",
        yref="paper",
        x=0,
        y=1.10,
        showarrow=False,
        align="left",
        font={"size": 12, "color": "#1F2933"},
    )
    fig.update_xaxes(title="Дисконт к номиналу, %", ticksuffix="", separatethousands=True, showexponent="none")
    fig.update_yaxes(title="Номинал минус выручка, млрд рублей", ticksuffix="", separatethousands=True, showexponent="none")
    fig.update_layout(legend_title_text="Вид ОФЗ")
    apply_common_layout(fig)
    return make_result("discount_vs_revenue_gap", fig, params, add_chart_units(data))


def revenue_metric_hover_template() -> str:
    return (
        "Период: %{customdata[0]}<br>"
        "Показатель: %{customdata[1]}<br>"
        "Значение: %{customdata[2]} млрд руб.<br>"
        "Количество размещений: %{customdata[3]}<br>"
        "Флаг качества данных: %{customdata[4]}<extra></extra>"
    )


def monthly_revenue_metric_hover_template() -> str:
    return (
        "Период: %{customdata[0]}<br>"
        "Месяц: %{customdata[1]}<br>"
        "Показатель: %{customdata[2]}<br>"
        "Значение: %{customdata[3]} млрд руб.<br>"
        "Количество размещений: %{customdata[4]}<br>"
        "Флаг качества данных: %{customdata[5]}<extra></extra>"
    )


def revenue_gap_hover_template() -> str:
    return (
        "Период: %{customdata[0]}<br>"
        "Номинал минус выручка: %{customdata[1]} млрд руб.<br>"
        "Объем размещения по номиналу: %{customdata[2]} млрд руб.<br>"
        "Выручка от реализации: %{customdata[3]} млрд руб.<br>"
        "Количество размещений: %{customdata[4]}<br>"
        "Флаг качества данных: %{customdata[5]}<extra></extra>"
    )


def monthly_revenue_gap_hover_template() -> str:
    return (
        "Период: %{customdata[0]}<br>"
        "Месяц: %{customdata[1]}<br>"
        "Номинал минус выручка: %{customdata[2]} млрд руб.<br>"
        "Объем размещения по номиналу: %{customdata[3]} млрд руб.<br>"
        "Выручка от реализации: %{customdata[4]} млрд руб.<br>"
        "Количество размещений: %{customdata[5]}<br>"
        "Флаг качества данных: %{customdata[6]}<extra></extra>"
    )


def revenue_ratio_hover_template() -> str:
    return (
        "Период: %{customdata[0]}<br>"
        "Выручка / номинал: %{customdata[1]}%<br>"
        "Объем размещения по номиналу: %{customdata[2]} млрд руб.<br>"
        "Выручка от реализации: %{customdata[3]} млрд руб.<br>"
        "Количество размещений: %{customdata[4]}<br>"
        "Флаг качества данных: %{customdata[5]}<extra></extra>"
    )


def category_gap_hover_template(category_name: str) -> str:
    return (
        "Период: %{customdata[0]}<br>"
        f"{category_name}: %{{customdata[1]}}<br>"
        "Номинал минус выручка: %{customdata[2]} млрд руб.<br>"
        "Объем размещения по номиналу: %{customdata[3]} млрд руб.<br>"
        "Выручка от реализации: %{customdata[4]} млрд руб.<br>"
        "Количество размещений: %{customdata[5]}<br>"
        "Флаг качества данных: %{customdata[6]}<extra></extra>"
    )


def apply_volume_axis_layout(fig: Any, yaxis_title: str) -> None:
    """Применить единый стандарт оси для млрд рублей без технических суффиксов."""
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_yaxes(title=yaxis_title, ticksuffix="", separatethousands=True, showexponent="none")
    apply_common_layout(fig)


def keep_single_yaxis_title(fig: Any, yaxis_title: str) -> None:
    """Оставить подпись Y только на первой facet-панели."""
    for axis_name in fig.layout:
        if not str(axis_name).startswith("yaxis"):
            continue
        axis = getattr(fig.layout, str(axis_name))
        axis.update(title_text=yaxis_title if str(axis_name) == "yaxis" else "")


def apply_common_layout(fig: Any) -> None:
    """Единый тихий стиль revenue-графиков."""
    fig.update_layout(
        template="plotly_white",
        font={"family": "Arial", "size": 12, "color": "#1F2933"},
        margin={"l": 72, "r": 48, "t": 110, "b": 80},
        hoverlabel={"font_size": 12},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    )


def add_chart_units(df: pd.DataFrame) -> pd.DataFrame:
    """Добавить единицы измерения в chart data export."""
    result = df.copy()
    for column in list(result.columns):
        if column.endswith("_bln") or column == "value_bln":
            result[f"{column}_unit"] = "млрд рублей"
        elif "volume" in column or "revenue" in column or "gap" in column:
            if not column.endswith("_label") and not column.endswith("_unit"):
                result[f"{column}_unit"] = "млн рублей"
    return result


def make_result(
    name: str,
    figure: Any,
    params: report_params.ReportParams,
    dataframe: pd.DataFrame,
) -> RevenueChartResult:
    """Сформировать объект результата с путями HTML и CSV."""
    suffix = make_output_suffix(params)
    html_dir = config.chart_html_dir_for_name(name)
    html_dir.mkdir(parents=True, exist_ok=True)
    return RevenueChartResult(
        name=name,
        figure=figure,
        html_path=html_dir / f"{name}_{suffix}.html",
        csv_path=REVENUE_CHART_DATA_DIR / f"{name}_{suffix}.csv",
        dataframe=dataframe,
    )


def make_output_suffix(params: report_params.ReportParams) -> str:
    """Вернуть суффикс с aggregation_mode."""
    return (
        f"{params.period_type}_{params.aggregation_mode}_{params.report_date.isoformat()}_"
        f"retrospective_{params.retrospective_years}"
    )


def month_label_short(value: Any) -> str:
    """Вернуть короткую русскую подпись месяца."""
    labels = {
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
    try:
        return labels.get(int(value), "")
    except (TypeError, ValueError):
        return ""


def format_ru_number(value: Any, digits: int = 1) -> str:
    """Отформатировать число с пробелом тысяч и десятичной запятой."""
    if pd.isna(value):
        return ""
    text = f"{float(value):,.{digits}f}"
    return text.replace(",", " ").replace(".", ",")


def build_report(
    params: report_params.ReportParams,
    results: list[RevenueChartResult],
    limitations: list[str],
) -> str:
    """Сформировать markdown-отчет по revenue charts."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Revenue charts: графики выручки от реализации ОФЗ",
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
        "## Созданные графики",
        "",
    ]
    if results:
        for result in results:
            lines.append(f"- `{result.name}`: `{result.html_path.relative_to(config.PROJECT_ROOT).as_posix()}`")
            lines.append(f"  - chart data: `{result.csv_path.relative_to(config.PROJECT_ROOT).as_posix()}`")
    else:
        lines.append("- Графики не построены.")
    lines.extend(
        [
            "",
            "## Методика",
            "",
            "- Все суммы на графиках отображаются в млрд рублей.",
            "- `placement_volume_bln = placement_volume / 1000`.",
            "- `revenue_volume_bln = revenue_volume / 1000`.",
            "- `nominal_revenue_gap_bln = (placement_volume - revenue_volume) / 1000`.",
            "- `discount_vs_revenue_gap` использует `nominal_discount_ratio`, то есть дисконт выручки к номиналу.",
            "",
            "## Ограничения",
            "",
        ]
    )
    if limitations:
        lines.extend(f"- {item}" for item in limitations)
    else:
        lines.append("- Существенные ограничения не выявлены.")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
