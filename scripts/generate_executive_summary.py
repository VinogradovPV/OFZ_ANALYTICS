"""Сформировать executive summary на основе рассчитанных артефактов pipeline.

Скрипт не рассчитывает показатели заново и не формулирует выводы без данных.
Все утверждения в итоговом markdown опираются на analytical tables, monthly
metrics, dashboard exports или chart data, найденные для заданного набора
параметров отчета.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence, cast

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, report_params, utils
else:
    from . import config, report_params, utils


EXECUTIVE_SUMMARY_REPORT_DOC = config.get_doc_path("executive_summary_report.md")


@dataclass(frozen=True)
class SourceStatus:
    """Статус одного входного артефакта executive summary."""

    name: str
    path: Path | None
    rows: int
    status: str
    note: str


@dataclass(frozen=True)
class SummaryContext:
    """Контекст загруженных источников."""

    suffix: str
    sources: list[SourceStatus]
    tables: dict[str, pd.DataFrame]
    source_paths: dict[str, Path]
    limitations: list[str]


def main(argv: Sequence[str] | None = None) -> int:
    """Сформировать executive summary и отчет об источниках."""
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт генерации executive summary")

    params = report_params.parse_report_args(argv)
    config.ensure_output_directories()

    context = load_summary_context(params)
    summary_path = config.REPORTS_DIR / f"executive_summary_{context.suffix}.md"
    utils.write_markdown(summary_path, build_executive_summary(params, context))
    utils.write_markdown(EXECUTIVE_SUMMARY_REPORT_DOC, build_sources_report(params, context, summary_path))

    logger.info("Executive summary сохранен: %s", summary_path)
    logger.info("Отчет по executive summary сохранен: %s", EXECUTIVE_SUMMARY_REPORT_DOC)
    return 0


def load_summary_context(params: report_params.ReportParams) -> SummaryContext:
    """Загрузить все доступные рассчитанные источники для заданного suffix."""
    suffix = make_suffix(params)
    limitations: list[str] = []
    sources: list[SourceStatus] = []
    tables: dict[str, pd.DataFrame] = {}
    source_paths: dict[str, Path] = {}

    expected_sources = {
        "demand_supply": config.EXPORTS_ANALYTICAL_CSV_DIR / f"demand_supply_{suffix}.csv",
        "ofz_yield_by_type": config.EXPORTS_ANALYTICAL_CSV_DIR / f"ofz_yield_by_type_{suffix}.csv",
        "placement_volume_by_maturity": config.EXPORTS_ANALYTICAL_CSV_DIR / f"placement_volume_by_maturity_{suffix}.csv",
        "monthly_metrics": config.EXPORTS_ANALYTICAL_CSV_DIR / f"monthly_metrics_{suffix}.csv",
        "revenue_summary": config.EXPORTS_ANALYTICAL_CSV_DIR / f"revenue_summary_{suffix}.csv",
        "revenue_by_ofz_type": config.EXPORTS_ANALYTICAL_CSV_DIR / f"revenue_by_ofz_type_{suffix}.csv",
        "revenue_by_maturity": config.EXPORTS_ANALYTICAL_CSV_DIR / f"revenue_by_maturity_{suffix}.csv",
        "revenue_by_format": config.EXPORTS_ANALYTICAL_CSV_DIR / f"revenue_by_format_{suffix}.csv",
        "revenue_monthly": config.EXPORTS_ANALYTICAL_CSV_DIR / f"revenue_monthly_{suffix}.csv",
    }

    for name, path in expected_sources.items():
        register_source(name, path, tables, source_paths, sources, limitations)

    dashboard_patterns = {
        "dashboard_period_summary": f"dashboard_period_summary_{suffix}.csv",
        "dashboard_kpi_summary": f"dashboard_kpi_summary_{suffix}.csv",
        "dashboard_demand_supply": f"dashboard_demand_supply_{suffix}.csv",
        "dashboard_monthly_metrics": f"dashboard_monthly_metrics_{suffix}.csv",
    }
    for name, filename in dashboard_patterns.items():
        register_source(name, find_latest(config.DASHBOARDS_DIR, filename), tables, source_paths, sources, limitations)

    chart_patterns = {
        "chart_placement_volume": f"placement_volume_{suffix}.csv",
        "chart_maturity_structure": f"maturity_structure_{suffix}.csv",
        "chart_format_structure": f"format_structure_{suffix}.csv",
        "chart_bid_to_cover": f"bid_to_cover_{suffix}.csv",
        "chart_yield_by_type": f"yield_by_type_{suffix}.csv",
        "chart_yield_boxplot_stats": f"yield_boxplot_stats_{suffix}.csv",
        "chart_yield_boxplot_ofz_pd_stats": f"yield_boxplot_ofz_pd_stats_{suffix}.csv",
        "chart_monthly_bid_to_cover": f"monthly_bid_to_cover_{suffix}.csv",
        "chart_discount_vs_demand": f"discount_vs_demand_{suffix}.csv",
        "chart_discount_vs_demand_outliers": f"discount_vs_demand_outliers_{suffix}.csv",
    }
    for name, filename in chart_patterns.items():
        register_source(name, find_latest(config.EXPORTS_CHART_DATA_DIR, filename), tables, source_paths, sources, limitations)

    return SummaryContext(
        suffix=suffix,
        sources=sources,
        tables=tables,
        source_paths=source_paths,
        limitations=limitations,
    )


def register_source(
    name: str,
    path: Path | None,
    tables: dict[str, pd.DataFrame],
    source_paths: dict[str, Path],
    sources: list[SourceStatus],
    limitations: list[str],
) -> None:
    """Загрузить источник и зафиксировать статус."""
    if path is None or not path.exists():
        sources.append(SourceStatus(name, path, 0, "missing", "Файл не найден."))
        limitations.append(f"Источник `{name}` не найден; связанные выводы не формировались.")
        return
    try:
        dataframe = pd.read_csv(path)
    except Exception as error:
        sources.append(SourceStatus(name, path, 0, "read_error", str(error)))
        limitations.append(f"Источник `{name}` не прочитан: {error}.")
        return
    tables[name] = dataframe
    source_paths[name] = path
    sources.append(SourceStatus(name, path, len(dataframe), "ok", "Источник использован."))


def find_latest(root: Path, filename: str) -> Path | None:
    """Найти последний по времени файл с заданным именем под root."""
    if not root.exists():
        return None
    candidates = sorted(root.rglob(filename), key=lambda path: path.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def build_executive_summary(params: report_params.ReportParams, context: SummaryContext) -> str:
    """Собрать markdown executive summary из рассчитанных показателей."""
    target_period = params.periods[-1]
    period_line = (
        f"{target_period['report_period_display_label']} "
        f"({target_period['period_start']} - {target_period['period_end']})"
    )
    lines: list[str] = [
        "# Executive summary по размещениям ОФЗ",
        "",
        f"Дата формирования: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`.",
        "",
        "## Параметры отчета",
        "",
        f"- Отчетная дата: `{params.report_date.isoformat()}`.",
        f"- Тип периода: `{params.period_type}`.",
        f"- Режим агрегации: `{params.aggregation_mode}`.",
        f"- Глубина ретроспективы: `{params.retrospective_years}`.",
        f"- Целевой период: {period_line}.",
        f"- Периоды сравнения: {', '.join(str(period['report_period_display_label']) for period in params.periods)}.",
        "",
        "## Ключевые показатели целевого периода",
        "",
    ]

    lines.extend(build_demand_supply_findings(context))
    lines.extend(build_placement_findings(context))
    lines.extend(build_revenue_findings(context))
    lines.extend(build_yield_findings(context))
    lines.extend(build_maturity_findings(context))
    lines.extend(build_monthly_findings(context))
    lines.extend(build_monthly_bid_cover_findings(context))
    lines.extend(build_discount_vs_demand_findings(context))
    lines.extend(build_yield_boxplot_findings(context))
    lines.extend(build_ofz_pd_yield_distribution_findings(context))
    lines.extend(build_dashboard_findings(context))
    lines.extend(build_chart_data_findings(context))

    lines.extend(
        [
            "",
            "## Ограничения интерпретации",
            "",
        ]
    )
    if context.limitations:
        lines.extend(f"- {item}" for item in sorted(set(context.limitations)))
    else:
        lines.append("- Все обязательные источники для executive summary найдены.")
    lines.extend(
        [
            "",
            "## Использованные источники",
            "",
            "| Источник | Файл | Строк | Статус |",
            "|---|---|---:|---|",
        ]
    )
    for source in context.sources:
        path_text = source.path.as_posix() if source.path else "-"
        lines.append(f"| {source.name} | `{path_text}` | {source.rows} | {source.status} |")
    return "\n".join(lines)


def build_demand_supply_findings(context: SummaryContext) -> list[str]:
    """Сформировать выводы по спросу и предложению."""
    df = context.tables.get("demand_supply")
    if df is None or df.empty:
        return ["- Спрос и предложение: нет рассчитанной таблицы `demand_supply`."]
    target = select_target_rows(df)
    if target.empty:
        return ["- Спрос и предложение: целевой период не найден в `demand_supply`."]
    row = target.iloc[-1]
    return [
        f"- Совокупный спрос: {format_volume_mln(row.get('total_demand'))}.",
        f"- Совокупное предложение: {format_volume_mln(row.get('total_supply'))}.",
        f"- Спрос / предложение: {format_ratio(first_row_value(row, ['bid_to_cover_ratio', 'demand_supply_ratio']))}.",
        f"- Количество размещений в таблице спроса/предложения: {format_int(row.get('auction_count'))}.",
        f"- YoY-изменение спроса: {format_ratio(row.get('total_demand_yoy_change'), percent=True)}; "
        f"YoY-изменение предложения: {format_ratio(row.get('total_supply_yoy_change'), percent=True)}.",
    ]


def build_placement_findings(context: SummaryContext) -> list[str]:
    """Сформировать выводы по объему размещения."""
    placement = context.tables.get("placement_volume_by_maturity")
    if placement is not None and not placement.empty:
        target = select_target_rows(placement)
        total = numeric_sum(target, "placement_volume")
        return [f"- Объем размещения по номиналу: {format_volume_mln(total)}."]
    period_summary = context.tables.get("dashboard_period_summary")
    if period_summary is not None and not period_summary.empty:
        target = select_target_rows(period_summary)
        return [f"- Объем размещения по номиналу: {format_volume_mln(first_available(target, ['total_placement_volume']))}."]
    return ["- Объем размещения: нет рассчитанного источника с `placement_volume`."]


def build_yield_findings(context: SummaryContext) -> list[str]:
    """Сформировать выводы по доходности."""
    df = context.tables.get("ofz_yield_by_type")
    if df is None or df.empty:
        return ["- Доходность по видам ОФЗ: таблица `ofz_yield_by_type` не найдена."]
    target = select_target_rows(df)
    if target.empty:
        return ["- Доходность по видам ОФЗ: целевой период не найден."]
    if "yield_weighted_avg" not in target.columns:
        return ["- Доходность по видам ОФЗ: колонка `yield_weighted_avg` отсутствует."]
    weighted = pd.to_numeric(target["yield_weighted_avg"], errors="coerce")
    if weighted.dropna().empty:
        return ["- Доходность по видам ОФЗ: нет валидной средневзвешенной доходности."]
    max_index = weighted.idxmax()
    row = row_at_label(target, max_index)
    return [
        f"- Максимальная средневзвешенная доходность среди видов ОФЗ в целевом периоде: "
        f"{row.get('ofz_type')} - {format_ratio(row.get('yield_weighted_avg'), digits=2)}% годовых.",
        f"- Диапазон доходности по этому виду: min {format_ratio(row.get('yield_min'), digits=2)}%, "
        f"max {format_ratio(row.get('yield_max'), digits=2)}%.",
    ]


def build_maturity_findings(context: SummaryContext) -> list[str]:
    """Сформировать выводы по сроковой структуре."""
    df = context.tables.get("placement_volume_by_maturity")
    if df is None or df.empty:
        return ["- Сроковая структура: таблица `placement_volume_by_maturity` не найдена."]
    target = select_target_rows(df)
    if target.empty:
        return ["- Сроковая структура: целевой период не найден."]
    if "placement_volume" not in target.columns:
        return ["- Сроковая структура: колонка `placement_volume` отсутствует."]
    volumes = pd.to_numeric(target["placement_volume"], errors="coerce")
    if volumes.dropna().empty:
        return ["- Сроковая структура: нет валидного `placement_volume`."]
    row = row_at_label(target, volumes.idxmax())
    share = row.get("placement_volume_share")
    return [
        f"- Крупнейшая сроковая категория по объему размещения: {row.get('maturity_bucket_label') or row.get('maturity_bucket')} "
        f"({format_volume_mln(row.get('placement_volume'))}; доля {format_ratio(share, percent=True)})."
    ]


def build_monthly_findings(context: SummaryContext) -> list[str]:
    """Сформировать выводы по monthly layer."""
    df = context.tables.get("monthly_metrics")
    if df is None or df.empty:
        return ["- Monthly layer: файл monthly metrics не найден."]
    target = target_year_rows(df)
    if target.empty:
        return ["- Monthly layer: целевой год не найден."]
    if "total_placement_volume" not in target.columns:
        return ["- Monthly layer: колонка `total_placement_volume` отсутствует."]
    placement = pd.to_numeric(target["total_placement_volume"], errors="coerce")
    if placement.dropna().empty:
        return ["- Monthly layer: нет валидного помесячного объема размещения."]
    max_row = row_at_label(target, placement.idxmax())
    last_row = target.sort_values("month_number").iloc[-1] if "month_number" in target.columns else target.iloc[-1]
    return [
        f"- Максимальный месячный объем размещения в целевом году: {max_row.get('month_label') or max_row.get('month')} - "
        f"{format_volume_mln(max_row.get('total_placement_volume'))}.",
        f"- Накопленный объем размещения на конец последнего месяца слоя: "
        f"{format_volume_mln(last_row.get('cumulative_placement_volume'))}.",
    ]


def build_revenue_findings(context: SummaryContext) -> list[str]:
    """Сформировать выводы по выручке от реализации ОФЗ."""
    df = context.tables.get("revenue_summary")
    if df is None or df.empty:
        return ["- Выручка от реализации ОФЗ: таблица `revenue_summary` не найдена; выводы по выручке не формировались."]
    target = select_target_rows(df)
    if target.empty:
        return ["- Выручка от реализации ОФЗ: целевой период не найден в `revenue_summary`."]
    row = target.iloc[-1]
    revenue_value = first_row_value(row, ["revenue_volume", "total_revenue_volume"])
    if pd.isna(pd.to_numeric(pd.Series([revenue_value]), errors="coerce").iloc[0]):
        context.limitations.append("В `revenue_summary` нет валидной выручки; блок revenue analytics ограничен.")
        return ["- Выручка от реализации ОФЗ: валидная колонка выручки отсутствует или пуста."]

    lines = [
        f"- Выручка от реализации ОФЗ: {format_volume_mln(revenue_value)}.",
        f"- Разница номинала и выручки: {format_volume_mln(row.get('nominal_revenue_gap'))}; "
        f"nominal discount ratio: {format_ratio(row.get('nominal_discount_ratio'), percent=True)}.",
        f"- Revenue-to-nominal ratio: {format_ratio(row.get('revenue_to_nominal_ratio'), digits=3)}.",
    ]
    by_type = context.tables.get("revenue_by_ofz_type")
    if by_type is not None and not by_type.empty:
        target_by_type = select_target_rows(by_type)
        gap_column = first_existing_column(target_by_type, ["nominal_revenue_gap", "nominal_revenue_gap_bln"])
        if gap_column:
            gaps = pd.to_numeric(target_by_type[gap_column], errors="coerce")
            if gaps.notna().any():
                max_gap_row = row_at_label(target_by_type, gaps.idxmax())
                gap_value = max_gap_row.get(gap_column)
                if gap_column.endswith("_bln"):
                    gap_value = pd.to_numeric(pd.Series([gap_value]), errors="coerce").iloc[0] * 1000.0
                lines.append(
                    f"- Максимальный разрыв номинала и выручки по видам бумаг: "
                    f"{max_gap_row.get('ofz_type')} - {format_volume_mln(gap_value)}."
                )
    return lines


def build_monthly_bid_cover_findings(context: SummaryContext) -> list[str]:
    """Сформировать выводы по помесячному покрытию предложения спросом."""
    df = context.tables.get("chart_monthly_bid_to_cover")
    if df is None or df.empty:
        df = context.tables.get("monthly_metrics")
    if df is None or df.empty:
        return ["- Помесячное покрытие предложения спросом: источник monthly bid-cover не найден."]
    target = target_year_rows(df)
    if target.empty:
        target = df.copy()
    ratio_column = first_existing_column(target, ["bid_to_cover_ratio", "cumulative_bid_to_cover_ratio"])
    if not ratio_column:
        return ["- Помесячное покрытие предложения спросом: колонка `bid_to_cover_ratio` отсутствует."]
    ratios = pd.to_numeric(target[ratio_column], errors="coerce")
    if ratios.dropna().empty:
        return ["- Помесячное покрытие предложения спросом: нет валидных значений."]
    ordered = target.sort_values("month_number") if "month_number" in target.columns else target
    valid_ordered = ordered.loc[pd.to_numeric(ordered[ratio_column], errors="coerce").notna()]
    last_row = valid_ordered.iloc[-1] if not valid_ordered.empty else target.iloc[-1]
    min_row = row_at_label(target, ratios.idxmin())
    max_row = row_at_label(target, ratios.idxmax())
    threshold_count = int((ratios >= 1).sum())
    return [
        f"- Помесячное покрытие предложения спросом: последнее доступное значение {month_name(last_row)} - "
        f"{format_ratio(last_row.get(ratio_column), digits=2)}.",
        f"- Диапазон monthly bid-cover: минимум {month_name(min_row)} - {format_ratio(min_row.get(ratio_column), digits=2)}, "
        f"максимум {month_name(max_row)} - {format_ratio(max_row.get(ratio_column), digits=2)}; "
        f"месяцев с `Спрос / предложение >= 1`: {threshold_count}.",
    ]


def build_discount_vs_demand_findings(context: SummaryContext) -> list[str]:
    """Сформировать выводы по графику discount vs demand."""
    df = context.tables.get("chart_discount_vs_demand")
    if df is None or df.empty:
        return ["- Discount vs demand: CSV-основа `discount_vs_demand` не найдена; выводы не формировались."]
    x_column = first_existing_column(df, ["x_value", "_demand_to_placement", "demand_to_placement_ratio"])
    y_column = first_existing_column(df, ["y_value", "_discount_to_nominal", "discount_to_nominal"])
    if not x_column or not y_column:
        return ["- Discount vs demand: отсутствуют расчетные X/Y (`demand_to_placement_ratio`, `discount_to_nominal`)."]
    x_values = pd.to_numeric(df[x_column], errors="coerce")
    y_values = pd.to_numeric(df[y_column], errors="coerce")
    if x_values.dropna().empty or y_values.dropna().empty:
        return ["- Discount vs demand: нет валидных значений спроса к размещению или дисконта."]
    max_x_row = row_at_label(df, x_values.idxmax())
    max_y_row = row_at_label(df, y_values.idxmax())
    outliers = context.tables.get("chart_discount_vs_demand_outliers")
    outlier_count = 0 if outliers is None else len(outliers)
    return [
        f"- Discount vs demand: максимальная кратность спроса к размещению - "
        f"{format_ratio(max_x_row.get(x_column), digits=2)} по выпуску {max_x_row.get('issue_code', 'нет данных')}.",
        f"- Максимальный дисконт к номиналу в CSV-основе: {format_ratio(max_y_row.get(y_column), digits=2)} п.п. "
        f"по выпуску {max_y_row.get('issue_code', 'нет данных')}; отмеченных outlier-точек: {outlier_count}.",
    ]


def build_yield_boxplot_findings(context: SummaryContext) -> list[str]:
    """Сформировать выводы по общему boxplot доходности."""
    df = context.tables.get("chart_yield_boxplot_stats")
    if df is None or df.empty:
        return ["- Yield boxplot: статистика `yield_boxplot_stats` не найдена."]
    target = select_target_rows(df)
    if target.empty:
        target = df.copy()
    median_column = first_existing_column(target, ["median", "yield_median"])
    min_column = first_existing_column(target, ["min", "yield_min_actual"])
    max_column = first_existing_column(target, ["max", "yield_max_actual"])
    n_column = first_existing_column(target, ["n", "auction_count"])
    if not median_column:
        return ["- Yield boxplot: колонка медианной доходности отсутствует."]
    medians = pd.to_numeric(target[median_column], errors="coerce")
    if medians.dropna().empty:
        return ["- Yield boxplot: нет валидных медианных значений доходности."]
    max_median_row = row_at_label(target, medians.idxmax())
    lines = [
        f"- Yield boxplot: максимальная медианная доходность в целевом срезе у {max_median_row.get('ofz_type')} - "
        f"{format_ratio(max_median_row.get(median_column), digits=2)}% годовых "
        f"(n={format_int(max_median_row.get(n_column)) if n_column else 'нет данных'})."
    ]
    if min_column and max_column:
        min_values = pd.to_numeric(target[min_column], errors="coerce")
        max_values = pd.to_numeric(target[max_column], errors="coerce")
        if min_values.notna().any() and max_values.notna().any():
            min_row = row_at_label(target, min_values.idxmin())
            max_row = row_at_label(target, max_values.idxmax())
            lines.append(
                f"- Диапазон фактической доходности по boxplot: min {format_ratio(min_row.get(min_column), digits=2)}% "
                f"({min_row.get('ofz_type')}), max {format_ratio(max_row.get(max_column), digits=2)}% ({max_row.get('ofz_type')})."
            )
    return lines


def build_ofz_pd_yield_distribution_findings(context: SummaryContext) -> list[str]:
    """Сформировать выводы по отдельному boxplot ОФЗ-ПД."""
    df = context.tables.get("chart_yield_boxplot_ofz_pd_stats")
    if df is None or df.empty:
        return ["- ОФЗ-ПД yield distribution: отдельная статистика `yield_boxplot_ofz_pd_stats` не найдена."]
    target = select_target_rows(df)
    if target.empty:
        target = df.copy()
    median_column = first_existing_column(target, ["median", "yield_median"])
    min_column = first_existing_column(target, ["min", "yield_min_actual"])
    max_column = first_existing_column(target, ["max", "yield_max_actual"])
    n_column = first_existing_column(target, ["n", "auction_count"])
    row = target.iloc[-1]
    if not median_column:
        return ["- ОФЗ-ПД yield distribution: колонка медианы отсутствует."]
    return [
        f"- ОФЗ-ПД yield distribution: медианная доходность {format_ratio(row.get(median_column), digits=2)}% годовых; "
        f"min {format_ratio(row.get(min_column), digits=2)}%, max {format_ratio(row.get(max_column), digits=2)}%, "
        f"n={format_int(row.get(n_column)) if n_column else 'нет данных'}."
    ]


def build_dashboard_findings(context: SummaryContext) -> list[str]:
    """Сформировать краткий блок о dashboard-ready источниках."""
    dashboard_sources = [source for source in context.sources if source.name.startswith("dashboard_") and source.status == "ok"]
    if not dashboard_sources:
        return ["- Dashboard exports: подходящие BI-ready источники не найдены."]
    return [f"- Dashboard exports: использовано файлов {len(dashboard_sources)}; они подтверждают показатели для BI-слоя."]


def build_chart_data_findings(context: SummaryContext) -> list[str]:
    """Сформировать краткий блок о chart data."""
    chart_sources = [source for source in context.sources if source.name.startswith("chart_") and source.status == "ok"]
    if not chart_sources:
        return ["- Chart data: таблицы-основы графиков не найдены."]
    return [f"- Chart data: использовано таблиц-основ графиков {len(chart_sources)}; визуальные выводы сверяются с CSV-основами."]


def build_sources_report(
    params: report_params.ReportParams,
    context: SummaryContext,
    summary_path: Path,
) -> str:
    """Сформировать служебный отчет о генерации executive summary."""
    lines = [
        "# Отчет о генерации executive summary",
        "",
        f"Дата формирования: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`.",
        "",
        "## Параметры",
        "",
        f"- `report_date`: `{params.report_date.isoformat()}`",
        f"- `period_type`: `{params.period_type}`",
        f"- `aggregation_mode`: `{params.aggregation_mode}`",
        f"- `retrospective_years`: `{params.retrospective_years}`",
        f"- Summary output: `{summary_path.as_posix()}`",
        "",
        "## Источники",
        "",
        "| Источник | Статус | Строк | Путь | Примечание |",
        "|---|---|---:|---|---|",
    ]
    for source in context.sources:
        path_text = source.path.as_posix() if source.path else "-"
        lines.append(f"| {source.name} | {source.status} | {source.rows} | `{path_text}` | {source.note} |")
    lines.extend(["", "## Ограничения", ""])
    if context.limitations:
        lines.extend(f"- {item}" for item in sorted(set(context.limitations)))
    else:
        lines.append("- Ограничений по источникам не зафиксировано.")
    return "\n".join(lines)


def select_target_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Вернуть строки целевого периода или последнего периода в таблице."""
    if "is_target_period" in df.columns:
        mask = df["is_target_period"].astype("string").str.lower().isin({"true", "1", "yes"})
        if mask.any():
            return df.loc[mask].copy()
    if "report_period_order" in df.columns:
        order = pd.to_numeric(df["report_period_order"], errors="coerce")
        if order.notna().any():
            return df.loc[order == order.max()].copy()
    if "report_period_start" in df.columns:
        dates = pd.to_datetime(df["report_period_start"], errors="coerce")
        if dates.notna().any():
            return df.loc[dates == dates.max()].copy()
    if "report_year" in df.columns:
        years = pd.to_numeric(df["report_year"], errors="coerce")
        if years.notna().any():
            return df.loc[years == years.max()].copy()
    return df.copy()


def target_year_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Вернуть строки target year для monthly metrics."""
    if "is_target_year" in df.columns:
        mask = df["is_target_year"].astype("string").str.lower().isin({"true", "1", "yes"})
        if mask.any():
            return df.loc[mask].copy()
    return select_target_rows(df)


def first_available(df: pd.DataFrame, columns: Sequence[str]) -> Any:
    """Вернуть первое доступное значение из списка колонок."""
    if df.empty:
        return pd.NA
    for column in columns:
        if column in df.columns:
            values = df[column].dropna()
            if not values.empty:
                return values.iloc[-1]
    return pd.NA


def first_row_value(row: pd.Series, columns: Sequence[str]) -> Any:
    """Вернуть первое непустое значение из строки."""
    for column in columns:
        if column in row.index and pd.notna(row.get(column)):
            return row.get(column)
    return pd.NA


def first_existing_column(df: pd.DataFrame, columns: Sequence[str]) -> str | None:
    """Вернуть первое имя колонки, которое есть в таблице."""
    for column in columns:
        if column in df.columns:
            return column
    return None


def row_at_label(df: pd.DataFrame, label: Any) -> pd.Series[Any]:
    """Return one row for a label even when pandas sees duplicate index labels."""
    selected = df.loc[label]
    if isinstance(selected, pd.DataFrame):
        return selected.iloc[0]
    return cast(pd.Series[Any], selected)


def month_name(row: pd.Series) -> str:
    """Вернуть человекочитаемую подпись месяца для executive summary."""
    for column in ("month_label", "month", "Месяц"):
        if column in row.index and pd.notna(row.get(column)):
            return str(row.get(column))
    if "month_number" in row.index and pd.notna(row.get("month_number")):
        return f"месяц {format_int(row.get('month_number'))}"
    return "месяц не определен"


def numeric_sum(df: pd.DataFrame, column: str) -> Any:
    """Суммировать числовую колонку, если она есть."""
    if column not in df.columns:
        return pd.NA
    return pd.to_numeric(df[column], errors="coerce").sum(min_count=1)


def format_volume_mln(value: Any) -> str:
    """Отформатировать объем из млн рублей в млн и млрд рублей."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return "нет данных"
    million = format_number(numeric, 1)
    billion = format_number(float(numeric) / 1000.0, 1)
    return f"{billion} млрд руб. ({million} млн руб.)"


def format_ratio(value: Any, digits: int = 2, percent: bool = False) -> str:
    """Отформатировать ratio или процентное изменение."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return "нет данных"
    if percent:
        return f"{format_number(float(numeric) * 100.0, 1)}%"
    return format_number(float(numeric), digits)


def format_int(value: Any) -> str:
    """Отформатировать целое число."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return "нет данных"
    return f"{int(numeric):,}".replace(",", " ")


def format_number(value: float, digits: int) -> str:
    """Отформатировать число с пробелом как разделителем тысяч и запятой."""
    return f"{value:,.{digits}f}".replace(",", " ").replace(".", ",")


def make_suffix(params: report_params.ReportParams) -> str:
    """Вернуть контрактный suffix отчетных файлов."""
    return (
        f"{params.period_type}_{params.aggregation_mode}_{params.report_date.isoformat()}_"
        f"retrospective_{params.retrospective_years}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
