"""Статическая QA-проверка HTML-графиков.

Скрипт проверяет уже построенные файлы из ``outputs/charts`` без запуска
браузера. Цель проверки - быстро поймать методологические и презентационные
регрессии: англоязычные подписи, технические имена колонок в видимых заголовках,
техническую шкалу объемов, отсутствие Sankey-подзаголовков и перегрузку
подписей на risk/scatter-графиках.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Iterable, Sequence


if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import config  # noqa: E402

from scripts.qa.html_chart_contracts import (  # noqa: E402
    DISCOUNT_VS_DEMAND_FILENAME_TOKENS,
    FORBIDDEN_ADJACENT_STRUCTURE_COLORS,
    MAX_SCATTER_LABELS,
    MAX_YIELD_DISCOUNT_FACET_LABELS_PER_FACET,
    MAX_YIELD_DISCOUNT_FACET_LABELS_TOTAL,
    MAX_YIELD_DISCOUNT_MAIN_LABELS_TOTAL,
    MAX_YIELD_DISCOUNT_OUTLIERS_LABELS_TOTAL,
    QaResult,
    REVENUE_CHART_PREFIXES,
    RUSSIAN_AXIS_TOKENS,
    SCATTER_FILENAME_TOKENS,
    SCATTER_LABEL_BUFFER,
    STACKED_STRUCTURE_FILENAME_TOKENS,
    TECHNICAL_COLUMN_TOKENS,
    VOLUME_FILENAME_TOKENS,
)

TECHNICAL_TICK_PATTERN = re.compile(r"(?<![A-Za-zА-Яа-я0-9])(?:1|2|5|8)(?:M|B|k)(?![A-Za-zА-Яа-я0-9])")
CYRILLIC_PATTERN = re.compile(r"[А-Яа-яЁё]")
TITLE_PATTERN = re.compile(r'"title"\s*:\s*\{\s*"text"\s*:\s*"(?P<text>[^"]*)"', re.IGNORECASE)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Разобрать параметры запуска HTML QA."""
    parser = argparse.ArgumentParser(description="QA-проверка HTML-графиков OFZ_ANALITICS.")
    parser.add_argument(
        "--charts-dir",
        type=Path,
        default=config.CHARTS_DIR,
        help="Папка с HTML-графиками. По умолчанию outputs/charts.",
    )
    parser.add_argument(
        "--max-risk-labels",
        type=int,
        default=MAX_SCATTER_LABELS,
        help="Максимальное число видимых подписей на risk/scatter-графике.",
    )
    parser.add_argument(
        "--report-date",
        default=None,
        help="Отчетная дата. Используется как необязательный фильтр HTML-файлов.",
    )
    parser.add_argument(
        "--retrospective-years",
        type=int,
        default=None,
        help="Глубина ретроспективы. Используется как необязательный фильтр HTML-файлов.",
    )
    parser.add_argument(
        "--period-type",
        choices=("month", "quarter", "year"),
        default=None,
        help="Тип периода. Используется как необязательный фильтр HTML-файлов.",
    )
    parser.add_argument(
        "--aggregation-mode",
        choices=("cumulative", "point"),
        default=None,
        help="Режим агрегации. Используется как необязательный фильтр HTML-файлов.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Выполнить QA-проверки и вернуть код завершения."""
    args = parse_args(argv)
    charts_dir = args.charts_dir
    html_files = sorted(charts_dir.rglob("*.html"))
    html_files = filter_html_files_by_report_args(html_files, args)
    html_by_file = {path: read_text(path) for path in html_files}
    plot_by_file = {path: extract_plot_payload(html) for path, html in html_by_file.items()}

    results = [
        check_charts_exist(html_files, charts_dir),
        check_russian_titles(html_by_file),
        check_russian_axes(html_by_file),
        check_hovertemplates(html_by_file),
        check_monthly_bid_cover_contract(html_by_file),
        check_monthly_demand_supply_contract(html_by_file),
        check_monthly_placement_volume_contract(html_by_file),
        check_monthly_cumulative_placement_contract(html_by_file),
        check_monthly_heatmap_placement_contract(html_by_file),
        check_monthly_heatmap_revenue_contract(html_by_file),
        check_facet_yaxis_title_policy(plot_by_file),
        check_volume_scale(plot_by_file),
        check_stacked_structure_charts(plot_by_file),
        check_format_structure_contract(html_by_file),
        check_format_discount_contract(html_by_file),
        check_format_nominal_revenue_gap_contract(html_by_file),
        check_format_terms_comparison_contract(html_by_file),
        check_format_terms_delta_contract(html_by_file),
        check_sankey_subtitle(plot_by_file),
        check_risk_label_limit(plot_by_file, max_labels=args.max_risk_labels),
        check_demand_cutoff_contract(plot_by_file, max_labels=args.max_risk_labels),
        check_discount_vs_demand_contract(plot_by_file, max_labels=args.max_risk_labels),
        check_yield_vs_discount_contract(plot_by_file, max_labels=args.max_risk_labels),
        check_format_terms_aggregate_scatter_contract(plot_by_file),
        check_format_terms_scatter_contract(plot_by_file),
        check_required_scatter_versions(html_files),
        check_yield_boxplot_mode(html_by_file),
        check_yield_boxplot_long_mode_integrity(plot_by_file),
        check_yield_boxplot_min_max_contract(html_by_file),
        check_yield_boxplot_ofz_pd_exists(html_files),
        check_ofz_pd_yield_key_rate_contract(html_by_file),
        check_revenue_charts_contract(plot_by_file),
        check_visible_technical_names(html_by_file),
    ]

    for result in results:
        status = "OK" if result.passed else "FAIL"
        print(f"{status} | {result.name} | {result.message}")

    failed = [result for result in results if not result.passed]
    return 0 if not failed else 1


def read_text(path: Path) -> str:
    """Прочитать HTML как UTF-8 с запасным вариантом для старых файлов."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def filter_html_files_by_report_args(html_files: Sequence[Path], args: argparse.Namespace) -> list[Path]:
    """Ограничить QA конкретным отчетным набором, если переданы параметры отчета."""
    required = (args.report_date, args.retrospective_years, args.period_type, args.aggregation_mode)
    if not all(value is not None for value in required):
        return list(html_files)
    suffix = f"_{args.period_type}_{args.aggregation_mode}_{args.report_date}_retrospective_{args.retrospective_years}"
    filtered = [path for path in html_files if suffix in path.stem]
    return filtered if filtered else list(html_files)


def extract_plot_payload(html: str) -> str:
    """Оставить только участок с конкретным Plotly.newPlot, исключая встроенную библиотеку Plotly."""
    marker = "Plotly.newPlot("
    index = html.rfind(marker)
    if index < 0:
        return html
    return html[index:]


def check_charts_exist(html_files: Sequence[Path], charts_dir: Path) -> QaResult:
    """Проверить, что папка графиков существует и содержит HTML."""
    if not charts_dir.exists():
        return QaResult("charts_dir_exists", False, f"Папка не найдена: {charts_dir}")
    if not html_files:
        return QaResult("html_charts_exist", False, f"В папке нет HTML-графиков: {charts_dir}")
    return QaResult("html_charts_exist", True, f"Найдено HTML-графиков: {len(html_files)}.")


def check_russian_titles(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить наличие русскоязычных названий в HTML-графиках."""
    failed = [
        path.name
        for path, html in html_by_file.items()
        if not CYRILLIC_PATTERN.search(extract_title_text(html) or html)
    ]
    if failed:
        return QaResult(
            "russian_titles",
            False,
            "Нет кириллицы в названии или HTML: " + short_list(failed),
        )
    return QaResult("russian_titles", True, "В графиках найдены русскоязычные названия.")


def check_russian_axes(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить, что в HTML есть русские подписи осей или измерений."""
    failed = [
        path.name
        for path, html in html_by_file.items()
        if not any(token in html for token in RUSSIAN_AXIS_TOKENS)
    ]
    if failed:
        return QaResult("russian_axes", False, "Не найдены русские оси/измерения: " + short_list(failed))
    return QaResult("russian_axes", True, "Русские подписи осей/измерений присутствуют.")


def check_hovertemplates(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить наличие hovertemplate и русификацию hover."""
    failed_missing = [path.name for path, html in html_by_file.items() if "hovertemplate" not in html]
    failed_russian = [
        path.name
        for path, html in html_by_file.items()
        if "hovertemplate" in html and not hover_has_russian_text(html)
    ]
    if failed_missing or failed_russian:
        parts = []
        if failed_missing:
            parts.append("нет hovertemplate: " + short_list(failed_missing))
        if failed_russian:
            parts.append("hover без русских подписей: " + short_list(failed_russian))
        return QaResult("hovertemplate", False, "; ".join(parts))
    return QaResult("hovertemplate", True, "Hovertemplate найден и содержит русские подписи.")


def check_monthly_bid_cover_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить подписи и CSV-контракт графика помесячного покрытия предложения спросом."""
    files = {path: html for path, html in html_by_file.items() if path.stem.startswith("monthly_bid_to_cover")}
    if not files:
        return QaResult("monthly_bid_cover_contract", True, "monthly_bid_to_cover не найден в текущем наборе HTML; проверка пропущена.")

    failed_html: list[str] = []
    failed_csv: list[str] = []
    required_csv_columns = {"label_display", "label_reason", "threshold_distance", "is_threshold_crossing"}
    for path, html in files.items():
        normalized_html = html.replace("\\/", "/").replace("\\u002f", "/").replace("\\u002F", "/")
        if (
            "Помесячное покрытие предложения спросом" not in normalized_html
            or "Спрос / предложение" not in normalized_html
            or "Спрос = предложение" not in normalized_html
            or "Режим агрегации" not in normalized_html
            or "Период отчета" not in normalized_html
        ):
            failed_html.append(path.name)
        csv_path = config.EXPORTS_CHART_DATA_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed_csv.append(f"{path.name}: нет CSV-основы")
            continue
        with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
            header = next(csv.reader(file), [])
        missing = sorted(required_csv_columns.difference(header))
        if missing:
            failed_csv.append(f"{csv_path.name}: нет {', '.join(missing)}")

    if failed_html or failed_csv:
        parts = []
        if failed_html:
            parts.append("HTML без обязательных подписей: " + short_list(failed_html))
        if failed_csv:
            parts.append("CSV-контракт нарушен: " + short_list(failed_csv))
        return QaResult("monthly_bid_cover_contract", False, "; ".join(parts))
    return QaResult("monthly_bid_cover_contract", True, f"monthly_bid_to_cover проверен: {len(files)} файлов.")


def check_monthly_placement_volume_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить, что подписи monthly_placement_volume рассчитаны из той же метрики, что и Y."""
    files = {path: html for path, html in html_by_file.items() if path.stem.startswith("monthly_placement_volume")}
    if not files:
        return QaResult("monthly_placement_volume_contract", True, "monthly_placement_volume не найден в текущем наборе HTML; проверка пропущена.")

    failed_html: list[str] = []
    failed_csv: list[str] = []
    required_columns = {
        "report_year",
        "month",
        "month_order",
        "placement_volume",
        "placement_volume_bln",
        "label_display",
        "label_visible",
        "hover_value_bln",
        "data_quality_flag",
    }
    for path, html in files.items():
        normalized = html.replace("\\/", "/").replace("\\u002f", "/").replace("\\u002F", "/")
        if (
            "Помесячный объем размещения ОФЗ по номиналу" not in normalized
            or "Объем размещения по номиналу, млрд рублей" not in normalized
            or "Показаны месячные значения" not in normalized
            or "hovertemplate" not in normalized
        ):
            failed_html.append(path.name)

        csv_path = config.EXPORTS_CHART_DATA_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed_csv.append(f"{path.name}: нет CSV-основы")
            continue
        with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        if not rows:
            failed_csv.append(f"{csv_path.name}: пустой CSV")
            continue
        missing = sorted(required_columns.difference(rows[0].keys()))
        if missing:
            failed_csv.append(f"{csv_path.name}: нет {', '.join(missing)}")
            continue
        for row_number, row in enumerate(rows, start=2):
            value = parse_float(row.get("placement_volume_bln", ""))
            if value is None:
                continue
            expected_label = format_qa_number(value, 1) if value > 0 else ""
            actual_label = str(row.get("label_display", ""))
            if actual_label != expected_label:
                failed_csv.append(
                    f"{csv_path.name}: строка {row_number} label_display={actual_label!r}, ожидалось {expected_label!r}"
                )
                break
            expected_hover = format_qa_number(value, 1)
            actual_hover = str(row.get("hover_value_bln", ""))
            if actual_hover != expected_hover:
                failed_csv.append(
                    f"{csv_path.name}: строка {row_number} hover_value_bln={actual_hover!r}, ожидалось {expected_hover!r}"
                )
                break

    if failed_html or failed_csv:
        parts = []
        if failed_html:
            parts.append("HTML-контракт нарушен: " + short_list(failed_html))
        if failed_csv:
            parts.append("CSV labels не соответствуют placement_volume_bln: " + short_list(failed_csv))
        return QaResult("monthly_placement_volume_contract", False, "; ".join(parts))
    return QaResult(
        "monthly_placement_volume_contract",
        True,
        f"monthly_placement_volume проверен: {len(files)} файлов; label_display соответствует placement_volume_bln.",
    )


def check_monthly_demand_supply_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить grouped/facet bar chart помесячного спроса и предложения."""
    files = {path: html for path, html in html_by_file.items() if path.stem.startswith("monthly_demand_supply")}
    if not files:
        return QaResult("monthly_demand_supply_contract", True, "monthly_demand_supply не найден; проверка пропущена.")

    failed_html: list[str] = []
    failed_csv: list[str] = []
    required_columns = {"value_bln", "label_display", "label_visible", "label_reason"}
    for path, html in files.items():
        normalized = unescape_json_text(html)
        has_labels = bool([value for value in extract_text_array_values(normalized) if str(value).strip()])
        hover_ok = "Спрос" in normalized and "Предложение" in normalized and "hovertemplate" in normalized
        if "Объем, млрд рублей" not in normalized or not hover_ok:
            failed_html.append(f"{path.name}: ось/hover")

        csv_path = config.EXPORTS_CHART_DATA_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed_csv.append(f"{path.name}: нет CSV-основы")
            continue
        with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        if not rows:
            failed_csv.append(f"{csv_path.name}: пустой CSV")
            continue
        missing = sorted(required_columns.difference(rows[0].keys()))
        if missing:
            failed_csv.append(f"{csv_path.name}: нет {', '.join(missing)}")
        csv_has_labels = any(str(row.get("label_display", "")).strip() for row in rows)
        if not has_labels and not csv_has_labels:
            failed_csv.append(f"{csv_path.name}: нет label_display и HTML-подписей")

    if failed_html or failed_csv:
        parts = []
        if failed_html:
            parts.append("HTML-контракт нарушен: " + short_list(failed_html))
        if failed_csv:
            parts.append("CSV labels неполные: " + short_list(failed_csv))
        return QaResult("monthly_demand_supply_contract", False, "; ".join(parts))
    return QaResult("monthly_demand_supply_contract", True, f"monthly_demand_supply проверен: {len(files)} файлов.")


def check_monthly_cumulative_placement_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить line chart накопленного объема размещения."""
    files = {path: html for path, html in html_by_file.items() if path.stem.startswith("monthly_cumulative_placement")}
    if not files:
        return QaResult("monthly_cumulative_placement_contract", True, "monthly_cumulative_placement не найден; проверка пропущена.")

    failed_html: list[str] = []
    failed_csv: list[str] = []
    required_columns = {
        "cumulative_placement_volume_bln",
        "monthly_delta_bln",
        "label_display",
        "label_reason",
    }
    for path, html in files.items():
        normalized = unescape_json_text(html)
        labels = [value for value in extract_text_array_values(normalized) if str(value).strip()]
        if "Накопленный объем размещения по номиналу, млрд рублей" not in normalized:
            failed_html.append(f"{path.name}: ось Y")
        if not labels:
            failed_html.append(f"{path.name}: нет подписей ключевых точек")

        csv_path = config.EXPORTS_CHART_DATA_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed_csv.append(f"{path.name}: нет CSV-основы")
            continue
        with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
            header = set(next(csv.reader(file), []))
        missing = sorted(required_columns.difference(header))
        if missing:
            failed_csv.append(f"{csv_path.name}: нет {', '.join(missing)}")

    if failed_html or failed_csv:
        parts = []
        if failed_html:
            parts.append("HTML-контракт нарушен: " + short_list(failed_html))
        if failed_csv:
            parts.append("CSV-контракт нарушен: " + short_list(failed_csv))
        return QaResult("monthly_cumulative_placement_contract", False, "; ".join(parts))
    return QaResult(
        "monthly_cumulative_placement_contract",
        True,
        f"monthly_cumulative_placement проверен: {len(files)} файлов.",
    )


def _legacy_check_monthly_heatmap_placement_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить heatmap размещения: колонка Итого и CSV-контракт."""
    files = {path: html for path, html in html_by_file.items() if path.stem.startswith("monthly_heatmap_placement")}
    if not files:
        return QaResult("monthly_heatmap_placement_contract", True, "monthly_heatmap_placement не найден; проверка пропущена.")

    required_columns = {
        "report_year",
        "month",
        "month_order",
        "placement_volume_bln",
        "is_total_column",
        "total_placement_volume_bln",
        "label_display",
    }
    failed: list[str] = []
    for path, html in files.items():
        normalized = unescape_json_text(html)
        if "Итого" not in normalized:
            failed.append(f"{path.name}: нет колонки Итого в HTML")
        csv_path = config.EXPORTS_CHART_DATA_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed.append(f"{path.name}: нет CSV-основы")
            continue
        rows = read_csv_rows(csv_path)
        if not rows:
            failed.append(f"{csv_path.name}: пустой CSV")
            continue
        missing = sorted(required_columns.difference(rows[0].keys()))
        if missing:
            failed.append(f"{csv_path.name}: нет {', '.join(missing)}")
            continue
        totals_by_year: dict[str, float] = {}
        months_by_year: dict[str, float] = {}
        for row in rows:
            year = str(row.get("report_year", "")).strip()
            value = parse_float(row.get("placement_volume_bln", ""))
            if value is None:
                continue
            is_total = str(row.get("is_total_column", "")).strip().lower() in {"true", "1", "yes"}
            if is_total:
                totals_by_year[year] = totals_by_year.get(year, 0.0) + value
            else:
                months_by_year[year] = months_by_year.get(year, 0.0) + value
        for year, total_value in totals_by_year.items():
            month_sum = months_by_year.get(year, 0.0)
            if abs(total_value - month_sum) > 0.05:
                failed.append(f"{csv_path.name}: итог {year} не равен сумме месяцев")
        if not totals_by_year:
            failed.append(f"{csv_path.name}: нет строк is_total_column=True")

    if failed:
        return QaResult("monthly_heatmap_placement_contract", False, short_list(failed))
    return QaResult("monthly_heatmap_placement_contract", True, f"monthly_heatmap_placement проверен: {len(files)} файлов.")


def check_volume_scale(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить стандарт отображения объемов: млрд рублей и без 5M/8M."""
    volume_files = {
        path: html
        for path, html in html_by_file.items()
        if any(token in path.stem for token in VOLUME_FILENAME_TOKENS)
    }
    failed_unit: list[str] = []
    failed_ticks: list[str] = []
    for path, html in volume_files.items():
        normalized = html.replace("\\/", "/").replace("\\u002f", "/").replace("\\u002F", "/").lower()
        if path.stem.startswith("monthly_heatmap_revenue"):
            if "РІС‹СЂСѓС‡Рє" not in normalized and "выручк" not in normalized:
                failed_unit.append(path.name)
            if TECHNICAL_TICK_PATTERN.search(html):
                failed_ticks.append(path.name)
            continue
        if (
            "объем размещения по номиналу" not in normalized
            and "объему размещения по номиналу" not in normalized
        ):
            failed_unit.append(path.name)
        if TECHNICAL_TICK_PATTERN.search(html):
            failed_ticks.append(path.name)

    if failed_unit or failed_ticks:
        parts = []
        if failed_unit:
            parts.append("нет явного указания номинального объема: " + short_list(failed_unit))
        if failed_ticks:
            parts.append("найден технический tick suffix M/B/k: " + short_list(failed_ticks))
        return QaResult("volume_scale_bln", False, "; ".join(parts))
    return QaResult(
        "volume_scale_bln",
        True,
        f"Проверены volume-графики: {len(volume_files)}; формат M/B/k не найден.",
    )


def check_facet_yaxis_title_policy(plot_by_file: dict[Path, str]) -> QaResult:
    """Проверить, что facet-графики не повторяют Y-title в каждой панели."""
    facet_tokens = (
        "monthly_demand_supply",
        "monthly_placement_by_format",
        "monthly_placement_by_maturity",
        "monthly_revenue_vs_nominal",
        "yield_vs_discount_facet",
    )
    facet_files = {
        path: html for path, html in plot_by_file.items() if any(path.stem.startswith(token) for token in facet_tokens)
    }
    failed: list[str] = []
    for path, html in facet_files.items():
        axis_titles = extract_axis_title_texts(html)
        y_titles = [title for title in axis_titles if "Доходность" in title or "Объем" in title or "Объ" in title]
        counts: dict[str, int] = {}
        for title in y_titles:
            counts[title] = counts.get(title, 0) + 1
        repeated = [f"{title}={count}" for title, count in counts.items() if title and count > 1]
        if repeated:
            failed.append(f"{path.name}: {short_list(repeated)}")
    if failed:
        return QaResult("facet_yaxis_title_policy", False, "Y-title повторяется в facet: " + short_list(failed))
    return QaResult("facet_yaxis_title_policy", True, f"Facet Y-title policy проверена: {len(facet_files)} файлов.")


def check_stacked_structure_charts(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить stacked structure charts: totals, ось Y и цветовые ограничения."""
    structure_files = {
        path: html
        for path, html in html_by_file.items()
        if any(token in path.stem for token in STACKED_STRUCTURE_FILENAME_TOKENS)
    }
    failed_total: list[str] = []
    failed_axis: list[str] = []
    failed_palette: list[str] = []
    for path, html in structure_files.items():
        normalized = html.replace("\\/", "/").replace("\\u002f", "/").replace("\\u002F", "/").lower()
        if "итого" not in normalized:
            failed_total.append(path.name)
        if "объем размещения по номиналу, млрд рублей" not in normalized:
            failed_axis.append(path.name)
        if has_forbidden_adjacent_structure_colors(html):
            failed_palette.append(path.name)

    if failed_total or failed_axis or failed_palette:
        parts = []
        if failed_total:
            parts.append("нет top total label: " + short_list(failed_total))
        if failed_axis:
            parts.append("некорректная ось Y объема: " + short_list(failed_axis))
        if failed_palette:
            parts.append("найдены соседние синий/желтый структурные цвета: " + short_list(failed_palette))
        return QaResult("stacked_structure_charts", False, "; ".join(parts))
    return QaResult(
        "stacked_structure_charts",
        True,
        f"Stacked structure charts проверены: {len(structure_files)} файлов.",
    )


def has_forbidden_adjacent_structure_colors(html: str) -> bool:
    """Проверить соседство запрещенной пары только среди цветов bar-traces."""
    colors = extract_bar_trace_colors(html)
    if len(colors) < 2:
        return False
    forbidden = {color.lower() for color in FORBIDDEN_ADJACENT_STRUCTURE_COLORS}
    for left, right in zip(colors, colors[1:]):
        pair = {left.lower(), right.lower()}
        if forbidden.issubset(pair):
            return True
    return False


def extract_bar_trace_colors(html: str) -> list[str]:
    """Извлечь цвета фактических bar-traces без учета layout.colorway и библиотеки Plotly."""
    colors: list[str] = []
    for match in re.finditer(r'\{[^{}]*"type"\s*:\s*"bar"[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', html):
        trace_text = match.group(0)
        color_match = re.search(r'"marker"\s*:\s*\{[^{}]*"color"\s*:\s*"(?P<color>#[0-9A-Fa-f]{6})"', trace_text)
        if color_match:
            colors.append(color_match.group("color"))
    if colors:
        return colors
    # Запасной вариант для minified Plotly JSON: берем только цвета marker.color рядом с bar trace.
    for match in re.finditer(r'"marker"\s*:\s*\{[^{}]*"color"\s*:\s*"(?P<color>#[0-9A-Fa-f]{6})"[^{}]*\}[^{}]*"type"\s*:\s*"bar"', html):
        colors.append(match.group("color"))
    return colors


def check_format_structure_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить контракт графиков структуры размещения по форматам."""
    files = {path: html for path, html in html_by_file.items() if path.name.startswith("format_structure")}
    if not files:
        return QaResult("format_structure_contract", False, "format_structure HTML не найден.")

    required_columns = {
        "report_period_label",
        "report_year",
        "format",
        "placement_volume_bln",
        "column_total",
        "segment_share_in_column",
        "label_visible",
        "label_reason",
        "label_position",
        "label_display",
        "total_placement_volume_bln",
        "format_share_pct",
    }
    min_segment_label_share = 0.015
    min_segment_label_value_bln = 20.0
    failed_html: list[str] = []
    failed_csv: list[str] = []

    for path, html in files.items():
        text = unescape_json_text(html)
        if "Объем размещения по номиналу, млрд рублей" not in text:
            failed_html.append(f"{path.name}: неверная Y-ось")
        if "Итого" not in text:
            failed_html.append(f"{path.name}: нет total labels")

        csv_path = config.EXPORTS_CHART_DATA_STRUCTURE_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed_csv.append(f"{csv_path.name}: файл не найден")
            continue
        rows = read_csv_rows(csv_path)
        if not rows:
            failed_csv.append(f"{csv_path.name}: пустой CSV")
            continue
        missing = sorted(required_columns.difference(rows[0].keys()))
        if missing:
            failed_csv.append(f"{csv_path.name}: нет {', '.join(missing)}")
            continue

        if not any(str(row.get("column_total", "")).strip() for row in rows):
            failed_csv.append(f"{csv_path.name}: нет column_total для восстановления totals")

        for row in rows:
            label_visible_text = str(row.get("label_visible", "")).strip().lower()
            if label_visible_text not in {"true", "false", "1", "0"}:
                failed_csv.append(f"{csv_path.name}: label_visible не boolean")
                break
            placement_bln = parse_float(row.get("placement_volume_bln"))
            share = parse_float(row.get("segment_share_in_column"))
            format_name = str(row.get("format", "")).lower()
            should_be_visible = (
                (share is not None and share >= min_segment_label_share)
                or (placement_bln is not None and placement_bln >= min_segment_label_value_bln)
                or "дрпа" in format_name
            )
            if should_be_visible and not parse_bool(label_visible_text):
                failed_csv.append(
                    f"{csv_path.name}: читаемый сегмент скрыт "
                    f"({row.get('report_period_label', '')}, {row.get('format', '')})"
                )
                break

    if failed_html or failed_csv:
        parts: list[str] = []
        if failed_html:
            parts.append("HTML contract: " + short_list(failed_html))
        if failed_csv:
            parts.append("CSV contract: " + short_list(failed_csv))
        return QaResult("format_structure_contract", False, "; ".join(parts))
    return QaResult("format_structure_contract", True, f"format_structure проверен: {len(files)} файлов.")


def check_sankey_subtitle(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить подзаголовок Sankey о ширине потоков."""
    sankey_files = {path: html for path, html in html_by_file.items() if path.name.startswith("sankey")}
    failed = [
        path.name
        for path, html in sankey_files.items()
        if not has_sankey_width_subtitle(html)
    ]
    if failed:
        return QaResult("sankey_subtitle", False, "Нет обязательного Sankey-подзаголовка: " + short_list(failed))
    return QaResult("sankey_subtitle", True, f"Sankey-подзаголовок проверен: {len(sankey_files)} файлов.")


def has_sankey_width_subtitle(html: str) -> bool:
    """Проверить смысловой Sankey-подзаголовок о ширине потока и номинальном объеме."""
    normalized = html.lower()
    return (
        "ширина потока" in normalized
        and "объем размещения по номиналу" in normalized
    )


def check_risk_label_limit(html_by_file: dict[Path, str], max_labels: int) -> QaResult:
    """Проверить, что risk/scatter-графики не подписывают все точки массово."""
    scatter_files = {
        path: html
        for path, html in html_by_file.items()
        if any(token in path.stem for token in SCATTER_FILENAME_TOKENS)
    }
    failed: list[str] = []
    not_measured: list[str] = []
    allowed_labels = max_labels + SCATTER_LABEL_BUFFER
    for path, html in scatter_files.items():
        label_count = max_text_label_count(html)
        if label_count is None:
            not_measured.append(path.name)
            continue
        if label_count > allowed_labels:
            failed.append(f"{path.name} ({label_count})")

    if failed:
        return QaResult(
            "risk_scatter_label_limit",
            False,
            f"Больше {allowed_labels} подписей (MAX_SCATTER_LABELS + запас): " + short_list(failed),
        )
    note = f"Проверены risk/scatter-графики: {len(scatter_files)}."
    if not_measured:
        note += " Для части файлов число подписей не удалось измерить статически: " + short_list(not_measured)
    return QaResult("risk_scatter_label_limit", True, note)


def check_discount_vs_demand_contract(html_by_file: dict[Path, str], max_labels: int) -> QaResult:
    """Проверить методологию и подписи dense scatter `discount_vs_demand`."""
    files = {
        path: html
        for path, html in html_by_file.items()
        if any(token in path.stem for token in DISCOUNT_VS_DEMAND_FILENAME_TOKENS)
    }
    if not files:
        return QaResult("discount_vs_demand_contract", True, "discount_vs_demand не найден в текущем наборе HTML; проверка пропущена.")

    failed_axes: list[str] = []
    failed_size_explanation: list[str] = []
    failed_labels: list[str] = []
    failed_csv: list[str] = []
    allowed_labels = max_labels + SCATTER_LABEL_BUFFER
    required_csv_columns = {"label_display", "label_reason"}

    for path, html in files.items():
        normalized = html.replace("\\/", "/").replace("\\u002f", "/").replace("\\u002F", "/").lower()
        if "спрос / объем размещения" not in normalized or "дисконт к номиналу" not in normalized:
            failed_axes.append(path.name)
        if (
            "размер точки = объем размещения по номиналу" not in normalized
            and "фиксированный размер" not in normalized
            and "размер пузыря" not in normalized
        ):
            failed_size_explanation.append(path.name)
        label_count = max_text_label_count(html)
        if label_count is not None and label_count > allowed_labels:
            failed_labels.append(f"{path.name} ({label_count})")

        csv_path = config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR / f"{path.stem}.csv"
        if csv_path.exists():
            with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
                header = set(next(csv.reader(file), []))
            missing = sorted(required_csv_columns.difference(header))
            if missing:
                failed_csv.append(f"{csv_path.name}: нет {', '.join(missing)}")

    if failed_axes or failed_size_explanation or failed_labels or failed_csv:
        parts = []
        if failed_axes:
            parts.append("не подтверждены оси X/Y: " + short_list(failed_axes))
        if failed_size_explanation:
            parts.append("нет пояснения размера точки или fixed-size fallback: " + short_list(failed_size_explanation))
        if failed_labels:
            parts.append("перегрузка подписей: " + short_list(failed_labels))
        if failed_csv:
            parts.append("CSV label policy неполный: " + short_list(failed_csv))
        return QaResult("discount_vs_demand_contract", False, "; ".join(parts))

    return QaResult(
        "discount_vs_demand_contract",
        True,
        f"discount_vs_demand проверен: {len(files)} файлов; label policy и size explanation подтверждены.",
    )


def check_demand_cutoff_contract(html_by_file: dict[Path, str], max_labels: int) -> QaResult:
    """Проверить bubble-size и label policy графика отсечения спроса."""
    files = {path: html for path, html in html_by_file.items() if path.stem.startswith("demand_cutoff_explanation")}
    if not files:
        return QaResult("demand_cutoff_contract", True, "demand_cutoff_explanation не найден; проверка пропущена.")

    failed_size: list[str] = []
    failed_labels: list[str] = []
    failed_csv: list[str] = []
    allowed_labels = max_labels + SCATTER_LABEL_BUFFER
    required_csv_columns = {"bubble_size_value", "placement_volume_bln", "label_display", "label_reason"}
    for path, html in files.items():
        normalized = unescape_json_text(html).lower()
        has_fixed_fallback = "фиксированный размер" in normalized or "fixed-size" in normalized
        if "размер точки = объем размещения по номиналу" not in normalized and not has_fixed_fallback:
            failed_size.append(path.name)
        label_count = max_text_label_count(html)
        if label_count is not None and label_count > allowed_labels:
            failed_labels.append(f"{path.name} ({label_count})")
        csv_path = config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed_csv.append(f"{path.name}: нет CSV-основы")
            continue
        with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
            header = set(next(csv.reader(file), []))
        missing = sorted(required_csv_columns.difference(header))
        if missing:
            failed_csv.append(f"{csv_path.name}: нет {', '.join(missing)}")

    if failed_size or failed_labels or failed_csv:
        parts = []
        if failed_size:
            parts.append("нет пояснения размера точки/fallback: " + short_list(failed_size))
        if failed_labels:
            parts.append("перегрузка подписей: " + short_list(failed_labels))
        if failed_csv:
            parts.append("CSV-контракт нарушен: " + short_list(failed_csv))
        return QaResult("demand_cutoff_contract", False, "; ".join(parts))
    return QaResult("demand_cutoff_contract", True, f"demand_cutoff_explanation проверен: {len(files)} файлов.")


def check_yield_vs_discount_contract(plot_by_file: dict[Path, str], max_labels: int) -> QaResult:
    """Проверить контракт семейства `yield_vs_discount` после перехода на группировку по годам."""
    files = {path: html for path, html in plot_by_file.items() if path.name.startswith("yield_vs_discount")}
    if not files:
        return QaResult("yield_vs_discount_contract", False, "yield_vs_discount HTML не найден в текущем наборе.")

    failed_legend: list[str] = []
    failed_maturity_color: list[str] = []
    failed_facet_axes: list[str] = []
    failed_facet_policy: list[str] = []
    failed_labels: list[str] = []
    failed_csv: list[str] = []
    failed_size_explanation: list[str] = []
    failed_median_explanation: list[str] = []
    failed_csv_label_visible: list[str] = []
    failed_csv_label_limits: list[str] = []
    failed_csv_color: list[str] = []
    required_csv_columns = {
        "report_year",
        "report_period_label",
        "report_period_display_label",
        "auction_date",
        "issue_code",
        "ofz_type",
        "format",
        "maturity_bucket_label",
        "discount_to_nominal",
        "weighted_avg_yield",
        "placement_volume",
        "placement_volume_bln",
        "demand_volume",
        "supply_volume",
        "demand_to_placement_ratio",
        "bid_to_cover_ratio",
        "x_value",
        "y_value",
        "yield_vs_discount_color",
        "bubble_size_value",
        "label_display",
        "label_visible",
        "label_reason",
        "period_month_start",
        "period_month_end",
        "is_incomplete_period",
        "incomplete_period_reason",
        "median_discount",
        "median_yield",
        "median_discount_period",
        "median_yield_period",
        "median_scope",
        "data_quality_flag",
        "data_quality_display",
        "label_reason_display",
    }
    expected_csv_files = {config.EXPORTS_CHART_DATA_SCATTER_DIR / f"{path.stem}.csv" for path in files}

    for path, html in files.items():
        text = unescape_json_text(html)
        is_facet = path.name.startswith("yield_vs_discount_facet")
        is_outliers = path.name.startswith("yield_vs_discount_outliers")
        if "Дисконт к номиналу, п.п." not in text or "Доходность, % годовых" not in text:
            failed_facet_axes.append(path.name)
        if (
            "мед. дисконт" not in text
            and "мед. доходность" not in text
            and "Пунктирные линии — медианы периода" not in text
        ):
            failed_median_explanation.append(path.name)
        if not is_facet:
            if "Год" not in text:
                failed_legend.append(path.name)
            if "Сроковая категория / вид ОФЗ" in text:
                failed_maturity_color.append(path.name)
            if "Размер точки" not in text or "объем размещения по номиналу" not in text:
                failed_size_explanation.append(path.name)
            if "мед. дисконт" not in text or "мед. доходность" not in text:
                failed_median_explanation.append(path.name)
        else:
            axis_titles = extract_axis_title_texts(text)
            if axis_titles.count("Доходность, % годовых") > 1 or axis_titles.count("Дисконт к номиналу, п.п.") > 1:
                failed_facet_axes.append(path.name)
            if "yield_vs_discount_facet=" in text or "Период=" in text:
                failed_facet_axes.append(path.name)
            if "Пунктирные линии — медианы периода; размер точки — объем размещения по номиналу" not in text:
                failed_facet_policy.append(f"{path.name}: нет пояснения медиан/размера")
            if text.count("Общая медиана") > 0 or text.count("медиана периода") > 1:
                failed_facet_policy.append(f"{path.name}: дублируются длинные подписи медиан")
            if "Размер точки" not in text or "объем размещения по номиналу" not in text:
                failed_size_explanation.append(path.name)

        label_count = max_text_label_count(html)
        if is_facet:
            if label_count is not None and label_count > MAX_YIELD_DISCOUNT_FACET_LABELS_TOTAL + SCATTER_LABEL_BUFFER:
                failed_labels.append(f"{path.name} ({label_count})")
        elif is_outliers and label_count is not None and label_count > MAX_YIELD_DISCOUNT_OUTLIERS_LABELS_TOTAL + SCATTER_LABEL_BUFFER:
            failed_labels.append(f"{path.name} ({label_count})")
        elif label_count is not None and label_count > MAX_YIELD_DISCOUNT_MAIN_LABELS_TOTAL + SCATTER_LABEL_BUFFER:
            failed_labels.append(f"{path.name} ({label_count})")

    for csv_path in sorted(expected_csv_files):
        csv_name = csv_path.name
        if not csv_path.exists():
            failed_csv.append(f"{csv_name}: файл не найден")
            continue
        with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            header = set(reader.fieldnames or [])
            rows = list(reader)
        missing = sorted(required_csv_columns.difference(header))
        if missing:
            failed_csv.append(f"{csv_name}: нет {', '.join(missing)}")
            continue

        label_values = [str(row.get("label_visible", "")).strip().lower() for row in rows]
        invalid_label_values = sorted({value for value in label_values if value not in {"true", "false", "1", "0"}})
        if invalid_label_values:
            failed_csv_label_visible.append(f"{csv_name}: некорректные значения {short_list(invalid_label_values)}")
        visible_rows = [row for row, value in zip(rows, label_values) if value in {"true", "1"}]

        is_csv_facet = csv_name.startswith("yield_vs_discount_facet")
        is_csv_outliers = csv_name.startswith("yield_vs_discount_outliers")
        if is_csv_facet:
            if len(visible_rows) > MAX_YIELD_DISCOUNT_FACET_LABELS_TOTAL + SCATTER_LABEL_BUFFER:
                failed_csv_label_limits.append(
                    f"{csv_name}: видимых подписей {len(visible_rows)} > {MAX_YIELD_DISCOUNT_FACET_LABELS_TOTAL}+{SCATTER_LABEL_BUFFER}"
                )
            per_panel: dict[str, int] = {}
            for row in visible_rows:
                key = row.get("report_period_display_label") or row.get("report_period_label") or row.get("report_year", "")
                per_panel[key] = per_panel.get(key, 0) + 1
            overloaded = [
                f"{key}={count}"
                for key, count in per_panel.items()
                if count > MAX_YIELD_DISCOUNT_FACET_LABELS_PER_FACET
            ]
            if overloaded:
                failed_csv_label_limits.append(f"{csv_name}: подписей на панель больше лимита: {short_list(overloaded)}")
            median_scopes = {row.get("median_scope", "") for row in rows}
            if "period" not in median_scopes:
                failed_facet_policy.append(f"{csv_name}: median_scope не period")
        elif is_csv_outliers:
            if len(visible_rows) > MAX_YIELD_DISCOUNT_OUTLIERS_LABELS_TOTAL + SCATTER_LABEL_BUFFER:
                failed_csv_label_limits.append(
                    f"{csv_name}: видимых подписей {len(visible_rows)} > {MAX_YIELD_DISCOUNT_OUTLIERS_LABELS_TOTAL}+{SCATTER_LABEL_BUFFER}"
                )
            failed_csv_color.extend(yield_vs_discount_color_failures(csv_name, rows))
            median_scopes = {row.get("median_scope", "") for row in rows}
            if "global" not in median_scopes:
                failed_median_explanation.append(f"{csv_name}: median_scope не global")
        else:
            if len(visible_rows) > MAX_YIELD_DISCOUNT_MAIN_LABELS_TOTAL + SCATTER_LABEL_BUFFER:
                failed_csv_label_limits.append(
                    f"{csv_name}: видимых подписей {len(visible_rows)} > {MAX_YIELD_DISCOUNT_MAIN_LABELS_TOTAL}+{SCATTER_LABEL_BUFFER}"
                )
            failed_csv_color.extend(yield_vs_discount_color_failures(csv_name, rows))
            median_scopes = {row.get("median_scope", "") for row in rows}
            if "global" not in median_scopes:
                failed_median_explanation.append(f"{csv_name}: median_scope не global")

    if (
        failed_legend
        or failed_maturity_color
        or failed_facet_axes
        or failed_facet_policy
        or failed_labels
        or failed_size_explanation
        or failed_median_explanation
        or failed_csv
        or failed_csv_label_visible
        or failed_csv_label_limits
        or failed_csv_color
    ):
        parts: list[str] = []
        if failed_legend:
            parts.append("main/outliers без легенды `Год`: " + short_list(failed_legend))
        if failed_maturity_color:
            parts.append("сроковая категория выглядит как главное цветовое измерение: " + short_list(failed_maturity_color))
        if failed_facet_axes:
            parts.append("facet-оси или заголовки панелей некорректны: " + short_list(failed_facet_axes))
        if failed_facet_policy:
            parts.append("facet-policy некорректна: " + short_list(failed_facet_policy))
        if failed_labels:
            parts.append("перегрузка подписей: " + short_list(failed_labels))
        if failed_size_explanation:
            parts.append("нет пояснения размера точки: " + short_list(failed_size_explanation))
        if failed_median_explanation:
            parts.append("медианные линии/median_scope некорректны: " + short_list(failed_median_explanation))
        if failed_csv:
            parts.append("CSV export неполный: " + short_list(failed_csv))
        if failed_csv_label_visible:
            parts.append("CSV label_visible не boolean/0/1: " + short_list(failed_csv_label_visible))
        if failed_csv_label_limits:
            parts.append("CSV превышает лимит видимых подписей: " + short_list(failed_csv_label_limits))
        if failed_csv_color:
            parts.append("CSV main/outliers не подтверждает color=report_year: " + short_list(failed_csv_color))
        return QaResult("yield_vs_discount_contract", False, "; ".join(parts))

    return QaResult("yield_vs_discount_contract", True, f"yield_vs_discount проверен: {len(files)} файлов.")


def yield_vs_discount_color_failures(csv_name: str, rows: Sequence[dict[str, str]]) -> list[str]:
    """Проверить, что main/outliers CSV подтверждает цветовое измерение `report_year`."""
    mismatches: list[str] = []
    for row in rows:
        report_year = str(row.get("report_year", "")).strip()
        color_value = str(row.get("yield_vs_discount_color", "")).strip()
        if report_year and color_value and report_year != color_value:
            issue_code = str(row.get("issue_code", "")).strip()
            mismatches.append(f"{issue_code or 'строка'}: {color_value}!={report_year}")
        elif report_year and not color_value:
            issue_code = str(row.get("issue_code", "")).strip()
            mismatches.append(f"{issue_code or 'строка'}: пустой color")
        if len(mismatches) >= 3:
            break
    if mismatches:
        return [f"{csv_name}: {short_list(mismatches)}"]
    return []


def check_format_terms_aggregate_scatter_contract(plot_by_file: dict[Path, str]) -> QaResult:
    """Проверить основной агрегированный scatter условий размещения по форматам."""
    files = {path: html for path, html in plot_by_file.items() if path.name.startswith("format_terms_aggregate_scatter")}
    if not files:
        return QaResult("format_terms_aggregate_scatter_contract", False, "format_terms_aggregate_scatter HTML не найден.")
    failed_html: list[str] = []
    failed_labels: list[str] = []
    failed_csv: list[str] = []
    required_csv_columns = {
        "report_period_label",
        "report_year",
        "format",
        "weighted_avg_discount_to_nominal",
        "weighted_avg_yield",
        "placement_volume_bln",
        "revenue_volume_bln",
        "nominal_revenue_gap_bln",
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
    }
    required_text = [
        "Средние условия размещения по форматам",
        "Одна точка",
        "формат размещения в периоде",
        "размер точки",
        "Средневзвешенный дисконт к номиналу, п.п.",
        "Средневзвешенная доходность размещения, % годовых",
        "мед. дисконт",
        "мед. доходность",
        "Формат",
    ]
    for path, html in files.items():
        text = unescape_json_text(html)
        if not all(token in text for token in required_text):
            failed_html.append(path.name)
        label_count = max_text_label_count(html)
        if label_count is not None and label_count > 25 + SCATTER_LABEL_BUFFER:
            failed_labels.append(f"{path.name} ({label_count})")
        csv_path = config.EXPORTS_CHART_DATA_SCATTER_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed_csv.append(f"{csv_path.name}: файл не найден")
            continue
        rows = read_csv_rows(csv_path)
        header = set(rows[0].keys()) if rows else set()
        missing = sorted(required_csv_columns.difference(header))
        if missing:
            failed_csv.append(f"{csv_path.name}: нет {', '.join(missing)}")
            continue
        period_format_keys = [
            (str(row.get("report_period_label", "")).strip(), str(row.get("format", "")).strip())
            for row in rows
        ]
        if len(period_format_keys) != len(set(period_format_keys)):
            failed_csv.append(f"{csv_path.name}: есть дубли period × format")
        if not all(period and format_name for period, format_name in period_format_keys):
            failed_csv.append(f"{csv_path.name}: пустой period или format")
        for column in [
            "placement_count",
            "placement_volume_bln",
            "source_column_yield",
            "aggregation_method_yield",
            "weight_field_yield",
            "source_column_discount",
            "aggregation_method_discount",
            "weight_field_discount",
        ]:
            if not all(str(row.get(column, "")).strip() for row in rows):
                failed_csv.append(f"{csv_path.name}: {column} пустой")
        invalid_label_values = sorted(
            {
                str(row.get("label_visible", "")).strip().lower()
                for row in rows
                if str(row.get("label_visible", "")).strip().lower() not in {"true", "false", "1", "0"}
            }
        )
        if invalid_label_values:
            failed_csv.append(f"{csv_path.name}: label_visible не boolean/0/1")
        if not any(str(row.get("aggregation_method_yield", "")).strip() for row in rows):
            failed_csv.append(f"{csv_path.name}: нет метода агрегации доходности")
        if not any(str(row.get("aggregation_method_discount", "")).strip() for row in rows):
            failed_csv.append(f"{csv_path.name}: нет метода агрегации дисконта")
    if failed_html or failed_labels or failed_csv:
        parts = []
        if failed_html:
            parts.append("HTML contract: " + short_list(failed_html))
        if failed_labels:
            parts.append("перегрузка подписей: " + short_list(failed_labels))
        if failed_csv:
            parts.append("CSV contract: " + short_list(failed_csv))
        return QaResult("format_terms_aggregate_scatter_contract", False, "; ".join(parts))
    return QaResult("format_terms_aggregate_scatter_contract", True, f"format_terms_aggregate_scatter проверен: {len(files)} файлов.")


def check_format_terms_scatter_contract(plot_by_file: dict[Path, str]) -> QaResult:
    """Проверить новый scatter-график условий размещения по форматам."""
    files = {path: html for path, html in plot_by_file.items() if path.name.startswith("format_terms_scatter")}
    if not files:
        return QaResult("format_terms_scatter_contract", False, "format_terms_scatter HTML не найден.")
    failed_html: list[str] = []
    failed_labels: list[str] = []
    failed_csv: list[str] = []
    required_csv_columns = {
        "report_year",
        "report_period_label",
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
        "demand_to_placement_ratio",
        "x_value",
        "y_value",
        "bubble_size_value",
        "label_display",
        "label_visible",
        "label_reason",
        "label_reason_display",
        "data_quality_flag",
        "data_quality_display",
    }
    for path, html in files.items():
        text = unescape_json_text(html)
        required_text = [
            "Условия размещения ОФЗ по форматам",
            "Дисконт к номиналу, п.п.",
            "Средневзвешенная доходность размещения, % годовых",
            "Цвет",
            "форма",
            "вид ОФЗ",
            "Размер",
            "объем размещения по номиналу",
            "Формат",
        ]
        if not all(token in text for token in required_text):
            failed_html.append(path.name)
        if "format + ofz_type" in text or "format_ofz_type" in text or "format_ofz" in text:
            failed_html.append(f"{path.name}: найдена смешанная категория format+ofz_type")
        if "data_quality_flag:" in text.lower():
            failed_html.append(f"{path.name}: сырой data_quality_flag в hover")
        label_count = max_text_label_count(html)
        if label_count is not None and label_count > 25 + SCATTER_LABEL_BUFFER:
            failed_labels.append(f"{path.name} ({label_count})")
        csv_path = config.EXPORTS_CHART_DATA_SCATTER_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed_csv.append(f"{csv_path.name}: файл не найден")
            continue
        rows = read_csv_rows(csv_path)
        header = set(rows[0].keys()) if rows else set()
        missing = sorted(required_csv_columns.difference(header))
        if missing:
            failed_csv.append(f"{csv_path.name}: нет {', '.join(missing)}")
            continue
        invalid_label_values = sorted(
            {
                str(row.get("label_visible", "")).strip().lower()
                for row in rows
                if str(row.get("label_visible", "")).strip().lower() not in {"true", "false", "1", "0"}
            }
        )
        if invalid_label_values:
            failed_csv.append(f"{csv_path.name}: label_visible не boolean/0/1")
        for column in ["format", "ofz_type", "source_column_yield", "aggregation_method_yield"]:
            if not all(str(row.get(column, "")).strip() for row in rows):
                failed_csv.append(f"{csv_path.name}: {column} пустой")
        if any(str(row.get("yield_metric_name_ru", "")).strip() == "Доходность, % годовых" for row in rows):
            failed_csv.append(f"{csv_path.name}: generic yield_metric_name_ru")
        visible_count = sum(
            1 for row in rows if str(row.get("label_visible", "")).strip().lower() in {"true", "1"}
        )
        if visible_count > 25 + SCATTER_LABEL_BUFFER:
            failed_csv.append(f"{csv_path.name}: видимых подписей {visible_count} > 25+{SCATTER_LABEL_BUFFER}")
    if failed_html or failed_labels or failed_csv:
        parts = []
        if failed_html:
            parts.append("HTML contract: " + short_list(failed_html))
        if failed_labels:
            parts.append("перегрузка подписей: " + short_list(failed_labels))
        if failed_csv:
            parts.append("CSV contract: " + short_list(failed_csv))
        return QaResult("format_terms_scatter_contract", False, "; ".join(parts))
    return QaResult("format_terms_scatter_contract", True, f"format_terms_scatter проверен: {len(files)} файлов.")


def check_required_scatter_versions(html_files: Sequence[Path]) -> QaResult:
    """Проверить наличие outlier/log/facet-версий risk-quadrant."""
    names = [path.name for path in html_files]
    required_tokens = (
        "risk_quadrant_retrospective_outliers_",
        "risk_quadrant_retrospective_logx_",
        "risk_quadrant_retrospective_facet_",
        "discount_vs_demand_outliers_",
        "discount_vs_demand_logx_",
        "yield_vs_discount_outliers_",
        "yield_vs_discount_facet_",
    )
    missing = [token for token in required_tokens if not any(token in name for name in names)]
    if missing:
        return QaResult("risk_scatter_versions", False, "Не найдены версии: " + ", ".join(missing))
    return QaResult("risk_scatter_versions", True, "Outlier/log-X/facet версии risk/scatter найдены.")


def check_yield_boxplot_mode(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить адаптивный режим boxplot доходности."""
    boxplot_files = {
        path: html for path, html in html_by_file.items() if path.name.startswith("yield_boxplot_by_ofz_type")
    }
    if not boxplot_files:
        return QaResult("yield_boxplot_mode", False, "Не найдены yield_boxplot_by_ofz_type HTML.")

    failed_title: list[str] = []
    failed_long_mode: list[str] = []
    for path, html in boxplot_files.items():
        valid_titles = (
            "Распределение доходности ОФЗ по видам бумаг",
            "Распределение доходности ОФЗ-ПД",
        )
        if not any(title in html for title in valid_titles):
            failed_title.append(path.name)
        retrospective = retrospective_years_from_name(path.name)
        if retrospective is not None and retrospective > 2:
            has_period_axis = "Период" in html
            has_facet_hint = "панел" in html.lower() or "facet" in html.lower() or "компакт" in html.lower()
            if not has_period_axis or not has_facet_hint:
                failed_long_mode.append(path.name)

    if failed_title or failed_long_mode:
        parts = []
        if failed_title:
            parts.append("нет корректного названия: " + short_list(failed_title))
        if failed_long_mode:
            parts.append("не подтвержден facet/compact mode для длинной ретроспективы: " + short_list(failed_long_mode))
        return QaResult("yield_boxplot_mode", False, "; ".join(parts))
    return QaResult("yield_boxplot_mode", True, f"Проверены boxplot-графики: {len(boxplot_files)}.")


def check_yield_boxplot_long_mode_integrity(plot_by_file: dict[Path, str]) -> QaResult:
    """Проверить, что длинный boxplot не схлопывает периоды в одну X-категорию."""
    long_files = {
        path: html
        for path, html in plot_by_file.items()
        if path.name.startswith("yield_boxplot_by_ofz_type")
        and (retrospective_years_from_name(path.name) or 0) > 2
    }
    if not long_files:
        return QaResult("yield_boxplot_long_mode_integrity", True, "Длинные boxplot-файлы не найдены.")

    failed_box: list[str] = []
    failed_x: list[str] = []
    failed_labels: list[str] = []
    failed_axis: list[str] = []
    for path, html in long_files.items():
        if '"type":"box"' not in html and '"type": "box"' not in html:
            failed_box.append(path.name)
        x_values = extract_plot_x_categories(html)
        expected_min = min((retrospective_years_from_name(path.name) or 0) + 1, 4)
        if len(x_values) < expected_min:
            failed_x.append(f"{path.name} ({len(x_values)} X-категорий)")
        if "Доходность, % годовых" not in html:
            failed_axis.append(path.name)
        median_labels = count_plot_label_token(html, "мед:")
        n_labels = count_plot_label_token(html, "n=")
        if median_labels == 0 or n_labels == 0:
            failed_labels.append(path.name)

    if failed_box or failed_x or failed_labels or failed_axis:
        parts = []
        if failed_box:
            parts.append("нет box traces: " + short_list(failed_box))
        if failed_x:
            parts.append("периоды X схлопнуты или не распознаны: " + short_list(failed_x))
        if failed_labels:
            parts.append("нет компактных median/n подписей: " + short_list(failed_labels))
        if failed_axis:
            parts.append("ось Y не равна `Доходность, % годовых`: " + short_list(failed_axis))
        return QaResult("yield_boxplot_long_mode_integrity", False, "; ".join(parts))
    return QaResult(
        "yield_boxplot_long_mode_integrity",
        True,
        f"Длинный boxplot проверен: {len(long_files)} файлов; X-периоды не схлопнуты.",
    )


def check_yield_boxplot_min_max_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить, что min/max есть на графике или в статистическом export."""
    boxplot_files = {
        path: html
        for path, html in html_by_file.items()
        if path.name.startswith("yield_boxplot_by_ofz_type") or path.name.startswith("yield_boxplot_ofz_pd")
    }
    if not boxplot_files:
        return QaResult("yield_boxplot_min_max_contract", True, "Boxplot-графики не найдены в текущем QA-наборе.")

    failed: list[str] = []
    for path, html in boxplot_files.items():
        has_visible_min_max = "мин:" in html and "макс:" in html
        stats_path = yield_boxplot_stats_path_for_html(path)
        has_export_min_max = stats_export_has_any_column_set(
            stats_path,
            ({"yield_min_actual", "yield_max_actual"}, {"min", "max"}),
        )
        if not has_visible_min_max and not has_export_min_max:
            failed.append(path.name)
    if failed:
        return QaResult(
            "yield_boxplot_min_max_contract",
            False,
            "Нет min/max ни в HTML-подписях, ни в stats export: " + short_list(failed),
        )
    return QaResult(
        "yield_boxplot_min_max_contract",
        True,
        f"Контракт min/max для yield boxplot проверен: {len(boxplot_files)} файлов.",
    )


def check_yield_boxplot_ofz_pd_exists(html_files: Sequence[Path]) -> QaResult:
    """Проверить наличие отдельного boxplot только по ОФЗ-ПД."""
    matched = [path.name for path in html_files if path.name.startswith("yield_boxplot_ofz_pd")]
    if not matched:
        return QaResult("yield_boxplot_ofz_pd_exists", False, "Не найден отдельный график yield_boxplot_ofz_pd.")
    return QaResult("yield_boxplot_ofz_pd_exists", True, "Отдельный boxplot ОФЗ-ПД найден: " + short_list(matched, limit=3))


def check_ofz_pd_yield_key_rate_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить контракт нового графика ОФЗ-ПД + ключевая ставка."""
    files = {path: html for path, html in html_by_file.items() if path.name.startswith("ofz_pd_yield_key_rate_")}
    if not files:
        return QaResult("ofz_pd_yield_key_rate_contract", True, "График OFZ-PD + key rate не найден в текущем наборе.")

    required_series = [
        "Максимальная доходность ОФЗ-ПД",
        "Минимальная доходность ОФЗ-ПД",
        "Ключевая ставка Банка России",
    ]
    required_colors = ["#FF5D50", "#00CE7E", "#BB88EF"]
    required_columns = {
        "month",
        "month_label",
        "ofz_pd_yield_max",
        "ofz_pd_yield_min",
        "key_rate_pct",
        "inflation_yoy_pct",
        "inflation_target_pct",
        "key_rate_available",
        "yield_scope",
        "source_cbr_file",
    }
    failed: list[str] = []
    for path, html in files.items():
        normalized = unescape_json_text(html)
        compact = normalized.replace(" ", "")
        for token in ["ОФЗ-ПД", "ключевой ставки Банка России"]:
            if token not in normalized:
                failed.append(f"{path.name}: в title не найден `{token}`")
        for series in required_series:
            if series not in normalized:
                failed.append(f"{path.name}: нет серии `{series}`")
        for color in required_colors:
            if color.lower() not in normalized.lower():
                failed.append(f"{path.name}: нет цвета {color}")
        if '"size":7' not in compact:
            failed.append(f"{path.name}: не подтвержден marker size 7")
        if '"width":1.5' not in compact:
            failed.append(f"{path.name}: не подтверждена marker outline width 1.5")

        csv_path = config.EXPORTS_CHART_DATA_YIELD_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed.append(f"{path.name}: не найден CSV {csv_path.name}")
            continue
        rows = read_csv_rows(csv_path)
        if not rows:
            failed.append(f"{csv_path.name}: пустой CSV")
            continue
        missing = sorted(required_columns.difference(rows[0].keys()))
        if missing:
            failed.append(f"{csv_path.name}: нет колонок {', '.join(missing)}")
        scopes = {str(row.get("yield_scope", "")).strip() for row in rows}
        if scopes != {"ofz_pd_only"}:
            failed.append(f"{csv_path.name}: unexpected yield_scope {sorted(scopes)}")
        if not any(str(row.get("key_rate_pct", "")).strip() for row in rows):
            failed.append(f"{csv_path.name}: key_rate_pct пуст")

    if failed:
        return QaResult("ofz_pd_yield_key_rate_contract", False, short_list(failed, limit=8))
    return QaResult("ofz_pd_yield_key_rate_contract", True, f"OFZ-PD + key rate проверен: {len(files)} файлов.")


def check_revenue_charts_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить наличие и презентационный контракт revenue charts второй модернизации."""
    matched = {
        prefix: [
            path
            for path in html_by_file
            if path.name.startswith(prefix)
        ]
        for prefix in REVENUE_CHART_PREFIXES
    }
    missing = [prefix for prefix, paths in matched.items() if not paths]
    failed_units: list[str] = []
    failed_hover: list[str] = []
    failed_discount_scatter: list[str] = []

    for paths in matched.values():
        for path in paths:
            html = html_by_file[path]
            normalized = html.lower()
            if "млрд руб" not in normalized and "млрд рублей" not in normalized:
                failed_units.append(path.name)
            if "флаг качества данных" not in normalized:
                failed_hover.append(path.name)
            if path.name.startswith("discount_vs_revenue_gap"):
                if "размер точки = объем размещения по номиналу" not in normalized or "вид офз" not in normalized:
                    failed_discount_scatter.append(path.name)

    if missing or failed_units or failed_hover or failed_discount_scatter:
        parts = []
        if missing:
            parts.append("не найдены revenue charts: " + short_list(missing))
        if failed_units:
            parts.append("нет млрд рублей в revenue chart: " + short_list(failed_units))
        if failed_hover:
            parts.append("нет флага качества данных в hover: " + short_list(failed_hover))
        if failed_discount_scatter:
            parts.append("неполный scatter contract revenue gap: " + short_list(failed_discount_scatter))
        return QaResult("revenue_charts_contract", False, "; ".join(parts))

    count = sum(len(paths) for paths in matched.values())
    return QaResult("revenue_charts_contract", True, f"Revenue charts проверены: {count} файлов.")


def check_format_nominal_revenue_gap_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить график разницы номинал-выручка по форматам."""
    files = {path: html for path, html in html_by_file.items() if path.name.startswith("format_nominal_revenue_gap")}
    if not files:
        return QaResult("format_nominal_revenue_gap_contract", False, "format_nominal_revenue_gap HTML не найден.")

    required_columns = {
        "report_period_label",
        "report_year",
        "format",
        "placement_volume_bln",
        "revenue_volume_bln",
        "nominal_revenue_gap_bln",
        "revenue_to_nominal_ratio",
        "auction_count",
        "data_quality_flag",
        "label_visible",
        "label_reason",
    }
    failed_html: list[str] = []
    failed_csv: list[str] = []

    for path, html in files.items():
        text = unescape_json_text(html)
        if "Разница между номинальным размещением и выручкой по форматам" not in text:
            failed_html.append(f"{path.name}: нет title")
        if "Номинал минус выручка, млрд рублей" not in text:
            failed_html.append(f"{path.name}: неверная Y-ось")

        csv_path = config.EXPORTS_CHART_DATA_REVENUE_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed_csv.append(f"{csv_path.name}: файл не найден")
            continue
        rows = read_csv_rows(csv_path)
        if not rows:
            failed_csv.append(f"{csv_path.name}: пустой CSV")
            continue
        missing = sorted(required_columns.difference(rows[0].keys()))
        if missing:
            failed_csv.append(f"{csv_path.name}: нет {', '.join(missing)}")

    if failed_html or failed_csv:
        parts: list[str] = []
        if failed_html:
            parts.append("HTML contract: " + short_list(failed_html))
        if failed_csv:
            parts.append("CSV contract: " + short_list(failed_csv))
        return QaResult("format_nominal_revenue_gap_contract", False, "; ".join(parts))
    return QaResult(
        "format_nominal_revenue_gap_contract",
        True,
        f"format_nominal_revenue_gap проверен: {len(files)} файлов.",
    )


def legacy_check_format_discount_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить composite-график номинала и дисконта по форматам."""
    files = {path: html for path, html in html_by_file.items() if path.name.startswith("format_discount")}
    if not files:
        return QaResult("format_discount_contract", False, "format_discount HTML не найден.")
    required_csv_columns = {
        "report_period_label",
        "report_year",
        "format",
        "component_type",
        "nominal_volume_bln",
        "revenue_volume_bln",
        "discount_gap_bln",
        "component_volume_bln",
        "weighted_avg_discount_pp",
        "min_discount_pp",
        "max_discount_pp",
        "format_share_pct",
        "total_nominal_volume_bln",
        "total_revenue_volume_bln",
        "total_discount_gap_bln",
        "auction_count",
        "discount_calc_method",
        "label_display",
        "label_visible",
        "total_label_display",
        "data_quality_flag",
        "data_quality_display",
    }
    failed_html: list[str] = []
    failed_csv: list[str] = []
    for path, html in files.items():
        text = unescape_json_text(html)
        normalized = text.lower()
        if "Номинал размещения, выручка и дисконтный разрыв по форматам" not in text:
            failed_html.append(f"{path.name}: нет title")
        if "внутри сегмента выделены выручка и дисконтный разрыв" not in normalized:
            failed_html.append(f"{path.name}: нет объяснения разложения номинала")
        if "Объем размещения по номиналу, млрд рублей" not in text:
            failed_html.append(f"{path.name}: Y-ось не про номинал")
        if re.search(r'"name"\s*:\s*"[^"]*п\.п\.[^"]*"[^{}]*"type"\s*:\s*"bar"', text):
            failed_html.append(f"{path.name}: возможен отдельный bar для дисконта в п.п.")
        if "Средневзвешенный дисконт к номиналу" not in text or "Дисконтный разрыв" not in text:
            failed_html.append(f"{path.name}: hover не подтверждает дисконтный разрыв и дисконт в п.п.")
        if "data_quality_flag:" in normalized:
            failed_html.append(f"{path.name}: hover содержит сырой data_quality_flag")
        if "Итого" not in text:
            failed_html.append(f"{path.name}: нет total labels")
        csv_path = config.EXPORTS_CHART_DATA_STRUCTURE_DIR / f"{path.stem}.csv"
        if not stats_export_has_columns(csv_path, required_csv_columns):
            failed_csv.append(csv_path.name)
        else:
            component_error = check_format_discount_csv_components(csv_path)
            if component_error:
                failed_csv.append(f"{csv_path.name}: {component_error}")

    if failed_html or failed_csv:
        parts = []
        if failed_html:
            parts.append("HTML contract: " + short_list(failed_html))
        if failed_csv:
            parts.append("CSV contract: " + short_list(failed_csv))
        return QaResult("format_discount_contract", False, "; ".join(parts))
    return QaResult("format_discount_contract", True, f"format_discount проверен: {len(files)} файлов.")


def check_format_discount_csv_components(path: Path) -> str:
    """Проверить компонентный CSV export format_discount."""
    try:
        rows = read_csv_rows(path)
    except OSError:
        return "CSV недоступен"
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        component_type = row.get("component_type", "")
        if component_type not in {"revenue", "discount_gap"}:
            return "component_type вне допустимых значений"
        if row.get("label_visible", "").strip().lower() not in {"true", "false", "1", "0"}:
            return "label_visible не boolean"
        if component_type == "discount_gap":
            try:
                gap_value = float(row.get("discount_gap_bln") or 0)
                component_value = float(row.get("component_volume_bln") or 0)
            except ValueError:
                return "некорректный discount_gap_bln"
            if gap_value < -0.000001 or component_value < -0.000001:
                return "discount_gap_bln отрицательный"
        grouped.setdefault((row.get("report_period_label", ""), row.get("format", "")), []).append(row)
    if not any(row.get("component_type") == "revenue" for row in rows):
        return "нет компонента revenue"
    if not any(row.get("component_type") == "discount_gap" for row in rows):
        return "нет компонента discount_gap"
    for key, group_rows in grouped.items():
        component_types = {item.get("component_type") for item in group_rows}
        if "revenue" not in component_types:
            return f"{key}: нет revenue"
        try:
            first = group_rows[0]
            revenue = float(first.get("revenue_volume_bln") or 0)
            gap = float(first.get("discount_gap_bln") or 0)
            nominal = float(first.get("nominal_volume_bln") or 0)
            total = float(first.get("total_nominal_volume_bln") or 0)
        except ValueError:
            return "некорректные числовые компоненты"
        if gap < -0.000001:
            return f"{key}: discount_gap_bln отрицательный"
        if abs((revenue + gap) - nominal) > 0.05:
            return f"{key}: revenue + discount_gap != nominal"
        if total <= 0:
            return f"{key}: total_nominal_volume_bln не положительный"
    return ""


def check_format_discount_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить график средневзвешенного дисконта по форматам."""
    files = {path: html for path, html in html_by_file.items() if path.name.startswith("format_discount")}
    if not files:
        return QaResult("format_discount_contract", False, "format_discount HTML не найден.")

    required_csv_columns = {
        "report_period_label",
        "report_year",
        "format",
        "weighted_avg_discount_to_nominal",
        "min_discount_to_nominal",
        "max_discount_to_nominal",
        "auction_count",
        "discount_calc_method",
        "label_display",
        "label_visible",
        "data_quality_flag",
    }
    failed_html: list[str] = []
    failed_csv: list[str] = []

    for path, html in files.items():
        text = unescape_json_text(html)
        normalized = text.lower()
        axis_titles = extract_axis_title_texts(text)
        if "Средневзвешенный дисконт к номиналу, п.п." not in axis_titles:
            failed_html.append(f"{path.name}: Y-ось не равна средневзвешенному дисконту")
        if "дисконт к номиналу" not in normalized:
            failed_html.append(f"{path.name}: нет аналитического названия дисконта")
        if "data_quality_flag:" in normalized:
            failed_html.append(f"{path.name}: hover содержит сырой data_quality_flag")

        csv_path = config.EXPORTS_CHART_DATA_STRUCTURE_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed_csv.append(f"{csv_path.name}: файл не найден")
            continue
        rows = read_csv_rows(csv_path)
        if not rows:
            failed_csv.append(f"{csv_path.name}: пустой CSV")
            continue
        missing = sorted(required_csv_columns.difference(rows[0].keys()))
        if missing:
            failed_csv.append(f"{csv_path.name}: нет {', '.join(missing)}")
            continue

        invalid_label_values = sorted(
            {
                str(row.get("label_visible", "")).strip().lower()
                for row in rows
                if str(row.get("label_visible", "")).strip().lower() not in {"true", "false", "1", "0"}
            }
        )
        if invalid_label_values:
            failed_csv.append(f"{csv_path.name}: label_visible не boolean")

        missing_discount_without_flag = [
            row.get("report_period_label", "")
            for row in rows
            if not str(row.get("weighted_avg_discount_to_nominal", "")).strip()
            and not str(row.get("data_quality_flag", "")).strip()
        ]
        if missing_discount_without_flag:
            failed_csv.append(f"{csv_path.name}: отсутствующий discount без data_quality_flag")

    if failed_html or failed_csv:
        parts: list[str] = []
        if failed_html:
            parts.append("HTML contract: " + short_list(failed_html))
        if failed_csv:
            parts.append("CSV contract: " + short_list(failed_csv))
        return QaResult("format_discount_contract", False, "; ".join(parts))
    return QaResult("format_discount_contract", True, f"format_discount проверен: {len(files)} файлов.")


def check_format_terms_comparison_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить контракт small multiples сравнения условий размещения по форматам."""
    files = {path: html for path, html in html_by_file.items() if path.name.startswith("format_terms_comparison")}
    if not files:
        return QaResult("format_terms_comparison_contract", False, "format_terms_comparison HTML не найден.")
    required_columns = {
        "report_period_label",
        "report_year",
        "format",
        "format_available",
        "metric_code",
        "metric_name_ru",
        "metric_name",
        "metric_label",
        "metric_value",
        "metric_unit",
        "source_column",
        "aggregation_method",
        "weight_field",
        "placement_count",
        "auction_count",
        "label_value_display",
        "label_count_display",
        "label_count_visible",
        "label_display",
        "label_visible",
        "format_available",
        "placement_volume_bln",
        "data_quality_flag",
    }
    html_errors: list[str] = []
    csv_errors: list[str] = []
    for path, html in files.items():
        text = unescape_json_text(html)
        if "n — количество размещений" not in text and "n - количество размещений" not in text:
            html_errors.append(f"{path.name}: нет пояснения n в subtitle")
        if "средневзвешенно по объему размещения по номиналу" not in text.lower():
            html_errors.append(f"{path.name}: subtitle не содержит метод агрегации доходности/дисконта")
        if "Метрика=" in text or "metric_label=" in text or "Показатель=" in text:
            html_errors.append(f"{path.name}: facet title содержит технический префикс")
        if "Доходность, % годовых" in text:
            html_errors.append(f"{path.name}: панель доходности названа слишком общо")
        if "Средневзвешенная доходность размещения, % годовых" not in text:
            html_errors.append(f"{path.name}: нет точного названия панели доходности")
        if '"text":"Значение"' in text or '"text": "Значение"' in text:
            html_errors.append(f"{path.name}: общий Y-title равен `Значение`")
        if "Количество размещений формата" not in text:
            html_errors.append(f"{path.name}: hover не содержит количество размещений формата")
        if "Исходное поле" not in text or "Метод агрегации" not in text or "Поле веса" not in text:
            html_errors.append(f"{path.name}: hover не содержит методологические поля")
        if "data_quality_flag:" in text.lower():
            html_errors.append(f"{path.name}: hover содержит сырой data_quality_flag")
        if "n=" not in text:
            html_errors.append(f"{path.name}: на графике нет подписей n")
        csv_path = config.EXPORTS_CHART_DATA_STRUCTURE_DIR / f"{path.stem}.csv"
        if not stats_export_has_columns(csv_path, required_columns):
            csv_errors.append(f"{csv_path.name}: неполный набор колонок")
            continue
        contract_error = check_format_terms_comparison_csv(csv_path, text)
        if contract_error:
            csv_errors.append(f"{csv_path.name}: {contract_error}")
    if html_errors or csv_errors:
        parts: list[str] = []
        if html_errors:
            parts.append("HTML contract: " + short_list(html_errors))
        if csv_errors:
            parts.append("CSV contract: " + short_list(csv_errors))
        return QaResult("format_terms_comparison_contract", False, "; ".join(parts))
    return QaResult("format_terms_comparison_contract", True, f"format_terms_comparison проверен: {len(files)} файлов.")


def check_format_terms_delta_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить график дельт ДРПА минус Аукцион."""
    files = {path: html for path, html in html_by_file.items() if path.name.startswith("format_terms_delta_by_format")}
    if not files:
        return QaResult("format_terms_delta_by_format_contract", False, "format_terms_delta_by_format HTML не найден.")
    required_csv_columns = {
        "report_period_label",
        "metric_code",
        "metric_name_ru",
        "metric_unit",
        "auction_value",
        "drpa_value",
        "delta_drpa_minus_auction",
        "metric_preference_direction",
        "assessment_threshold",
        "drpa_condition_assessment",
        "drpa_condition_assessment_ru",
        "auction_placement_count",
        "drpa_placement_count",
        "auction_placement_volume_bln",
        "drpa_placement_volume_bln",
        "aggregation_method",
        "source_column",
        "weight_field",
        "label_display",
        "label_visible",
        "data_quality_flag",
        "data_quality_display_short",
        "data_quality_display_full",
    }
    failed_html: list[str] = []
    failed_csv: list[str] = []
    for path, html in files.items():
        text = unescape_json_text(html)
        required_text = [
            "Разница условий размещения: ДРПА минус Аукцион",
            "Δ = ДРПА − Аукцион",
            "цвет показывает аналитическую оценку",
            "ДРПА хуже",
            "ДРПА лучше",
            "Различие малозначимо",
            "Разница доходности",
            "Разница дисконта к номиналу",
            "Разница номинал",
        ]
        revenue_to_nominal_present = (
            "Разница выручки / номинала" in text
            or "Разница выручки \\u002f номинала" in html
            or "Разница выручки \\u002f номинала" in text
        )
        if not all(token in text for token in required_text) or not revenue_to_nominal_present:
            failed_html.append(path.name)
        if "Показатель=" in text or "metric_name_ru=" in text:
            failed_html.append(f"{path.name}: технический facet-prefix")
        if "ДРПА выше" in text or "ДРПА ниже" in text:
            failed_html.append(f"{path.name}: старая легенда выше/ниже")
        if "data_quality_flag:" in text.lower():
            failed_html.append(f"{path.name}: сырой data_quality_flag в hover")
        csv_path = config.EXPORTS_CHART_DATA_STRUCTURE_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed_csv.append(f"{csv_path.name}: файл не найден")
            continue
        rows = read_csv_rows(csv_path)
        header = set(rows[0].keys()) if rows else set()
        missing = sorted(required_csv_columns.difference(header))
        if missing:
            failed_csv.append(f"{csv_path.name}: нет {', '.join(missing)}")
            continue
        unavailable_with_delta = [
            row.get("report_period_label", "")
            for row in rows
            if str(row.get("delta_available", "")).strip().lower() in {"false", "0"}
            and str(row.get("delta_drpa_minus_auction", "")).strip() not in {"", "nan", "NaN", "<NA>"}
        ]
        if unavailable_with_delta:
            failed_csv.append(f"{csv_path.name}: фиктивная дельта при delta_available=False")
        for row in rows:
            metric_code = row.get("metric_code", "")
            delta_text = str(row.get("delta_drpa_minus_auction", "")).strip()
            if not delta_text or delta_text in {"nan", "NaN", "<NA>"}:
                continue
            try:
                delta = float(delta_text)
            except ValueError:
                continue
            assessment = row.get("drpa_condition_assessment_ru", "")
            if metric_code == "delta_revenue_to_nominal_pp" and delta < -0.10 and assessment != "ДРПА хуже":
                failed_csv.append(f"{csv_path.name}: revenue_to_nominal negative delta должна быть `ДРПА хуже`")
            if metric_code == "delta_discount_pp" and delta > 0.10 and assessment != "ДРПА хуже":
                failed_csv.append(f"{csv_path.name}: discount positive delta должна быть `ДРПА хуже`")
    if failed_html or failed_csv:
        parts = []
        if failed_html:
            parts.append("HTML contract: " + short_list(failed_html))
        if failed_csv:
            parts.append("CSV contract: " + short_list(failed_csv))
        return QaResult("format_terms_delta_by_format_contract", False, "; ".join(parts))
    return QaResult("format_terms_delta_by_format_contract", True, f"format_terms_delta_by_format проверен: {len(files)} файлов.")


def check_format_terms_comparison_csv(path: Path, html_text: str) -> str:
    """Проверить placement_count и format_available в CSV format_terms_comparison."""
    try:
        rows = read_csv_rows(path)
    except OSError:
        return "CSV недоступен"
    if not rows:
        return "CSV пуст"
    required_metric_codes = {
        "yield_weighted_avg",
        "weighted_avg_discount_to_nominal",
        "revenue_to_nominal_pct",
        "nominal_revenue_gap_bln",
    }
    metric_codes = {row.get("metric_code", "") for row in rows}
    missing_metric_codes = sorted(required_metric_codes.difference(metric_codes))
    if missing_metric_codes:
        return "нет обязательных метрик: " + ", ".join(missing_metric_codes)
    visible_count_values: set[int] = set()
    for row in rows:
        available = parse_bool(row.get("format_available", ""))
        label_visible = parse_bool(row.get("label_visible", ""))
        count_visible = parse_bool(row.get("label_count_visible", ""))
        try:
            placement_count = int(float(row.get("placement_count") or 0))
        except ValueError:
            return "placement_count не число"
        if available and placement_count <= 0:
            return "format_available=True при placement_count <= 0"
        if not available and placement_count != 0:
            return "format_available=False при placement_count != 0"
        if available and label_visible and not row.get("label_value_display", "").strip():
            return "нет label_value_display для видимой подписи"
        if available and not row.get("source_column", "").strip():
            return "нет source_column для доступной метрики"
        if available and not row.get("aggregation_method", "").strip():
            return "нет aggregation_method для доступной метрики"
        if row.get("metric_code", "") == "yield_weighted_avg":
            if row.get("metric_name_ru", "") != "Средневзвешенная доходность размещения, % годовых":
                return "нет точного metric_name_ru для доходности"
            if row.get("source_column", "") != "weighted_avg_yield":
                return "доходность использует неверный source_column"
            if row.get("aggregation_method", "") != "weighted_average_by_placement_volume":
                return "доходность использует неверный aggregation_method"
            if row.get("weight_field", "") != "placement_volume":
                return "доходность использует неверный weight_field"
        if available and count_visible:
            expected = f"n={placement_count}"
            if row.get("label_count_display", "").strip() != expected:
                return "label_count_display не соответствует placement_count"
            if expected not in row.get("label_display", ""):
                return "label_display не содержит n"
            visible_count_values.add(placement_count)
    for value in visible_count_values:
        if f"n={value}" not in html_text:
            return f"HTML не содержит n={value} из CSV"
    return ""


def parse_bool(value: str) -> bool:
    """Интерпретировать boolean из CSV."""
    return str(value).strip().lower() in {"true", "1", "yes"}


def yield_boxplot_stats_path_for_html(path: Path) -> Path:
    """Получить ожидаемый путь stats export для yield boxplot HTML."""
    stem = path.stem
    if stem.startswith("yield_boxplot_by_ofz_type_"):
        suffix = stem.removeprefix("yield_boxplot_by_ofz_type_")
        return config.EXPORTS_CHART_DATA_BOXPLOT_DIR / f"yield_boxplot_stats_{suffix}.csv"
    if stem.startswith("yield_boxplot_ofz_pd_"):
        suffix = stem.removeprefix("yield_boxplot_ofz_pd_")
        return config.EXPORTS_CHART_DATA_BOXPLOT_DIR / f"yield_boxplot_ofz_pd_stats_{suffix}.csv"
    return config.EXPORTS_CHART_DATA_BOXPLOT_DIR / f"{stem}.csv"


def stats_export_has_columns(path: Path, required_columns: set[str]) -> bool:
    """Проверить наличие обязательных колонок в CSV export без зависимости от pandas."""
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            header = set(next(csv.reader(file), []))
    except OSError:
        return False
    return required_columns.issubset(header)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Прочитать CSV как список словарей для контрактных QA-проверок."""
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def stats_export_has_any_column_set(path: Path, column_sets: Sequence[set[str]]) -> bool:
    """Проверить, что CSV содержит хотя бы один допустимый набор колонок."""
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            header = set(next(csv.reader(file), []))
    except OSError:
        return False
    return any(required.issubset(header) for required in column_sets)


def check_visible_technical_names(html_by_file: dict[Path, str]) -> QaResult:
    """Проверить отсутствие технических имен колонок в видимых заголовках и осях."""
    failed: list[str] = []
    for path, html in html_by_file.items():
        visible_titles = extract_title_like_texts(html)
        bad_titles = [
            text
            for text in visible_titles
            if any(token in text for token in TECHNICAL_COLUMN_TOKENS)
        ]
        if bad_titles:
            failed.append(f"{path.name}: {short_list(bad_titles, limit=2)}")
    if failed:
        return QaResult(
            "no_technical_visible_names",
            False,
            "Технические имена найдены в видимых заголовках/осях: " + short_list(failed),
        )
    return QaResult(
        "no_technical_visible_names",
        True,
        "Технические имена колонок не найдены в видимых title/axis-подписях.",
    )


def extract_title_text(html: str) -> str:
    """Извлечь первый Plotly title text."""
    match = TITLE_PATTERN.search(html)
    return unescape_json_text(match.group("text")) if match else ""


def extract_title_like_texts(html: str) -> list[str]:
    """Извлечь тексты, которые обычно используются как видимые заголовки и подписи осей."""
    texts: list[str] = []
    for match in TITLE_PATTERN.finditer(html):
        texts.append(unescape_json_text(match.group("text")))
    axis_title_pattern = re.compile(r'"(?:xaxis|yaxis|coloraxis)[^"]*"\s*:\s*\{[^{}]*"title"\s*:\s*\{[^{}]*"text"\s*:\s*"([^"]*)"', re.IGNORECASE)
    for match in axis_title_pattern.finditer(html):
        texts.append(unescape_json_text(match.group(1)))
    return texts


def extract_axis_title_texts(html: str) -> list[str]:
    """Извлечь только подписи осей из Plotly layout."""
    texts: list[str] = []
    axis_title_pattern = re.compile(r'"(?:xaxis|yaxis)\d*"\s*:\s*\{[^{}]*"title"\s*:\s*\{[^{}]*"text"\s*:\s*"([^"]*)"', re.IGNORECASE)
    for match in axis_title_pattern.finditer(html):
        texts.append(unescape_json_text(match.group(1)))
    return texts


def hover_has_russian_text(html: str) -> bool:
    """Проверить, что hovertemplate содержит кириллицу."""
    for match in re.finditer(r'"hovertemplate"\s*:\s*"(?P<hover>[^"]*)"', html):
        if CYRILLIC_PATTERN.search(unescape_json_text(match.group("hover"))):
            return True
    return False


def max_text_label_count(html: str) -> int | None:
    """Оценить максимальное число непустых подписей в массиве Plotly text."""
    counts: list[int] = []
    for match in re.finditer(r'"text"\s*:\s*(\[[^\]]*\])', html):
        raw_array = match.group(1)
        try:
            values = json.loads(raw_array)
        except json.JSONDecodeError:
            continue
        if isinstance(values, list) and values and all(
            isinstance(value, (str, int, float, type(None))) for value in values
        ):
            non_empty = sum(1 for value in values if str(value or "").strip())
            counts.append(non_empty)
    if not counts:
        return None
    return max(counts)


def extract_text_array_values(html: str) -> list[str]:
    """Извлечь все строковые значения из массивов Plotly `text`."""
    values: list[str] = []
    for match in re.finditer(r'"text"\s*:\s*(\[[^\]]*\])', html):
        raw_array = match.group(1)
        try:
            parsed = json.loads(raw_array)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, list):
            values.extend(str(value or "").strip() for value in parsed)
    return values


def extract_plot_x_categories(html: str) -> set[str]:
    """Извлечь строковые X-категории из массивов Plotly."""
    categories: set[str] = set()
    for match in re.finditer(r'"x"\s*:\s*(\[[^\]]*\])', html):
        try:
            values = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        if not isinstance(values, list):
            continue
        for value in values:
            if isinstance(value, (str, int)):
                text = str(value).strip()
                if re.search(r"20\d{2}", text) and len(text) <= 40:
                    categories.add(text)
    return categories


def count_plot_label_token(html: str, token: str) -> int:
    """Посчитать в Plotly payload видимые подписи с указанным токеном."""
    count = 0
    for match in re.finditer(r'"text"\s*:\s*(?:"([^"]*)"|(\[[^\]]*\]))', html):
        single_value = match.group(1)
        raw_array = match.group(2)
        if single_value is not None:
            if token in unescape_json_text(single_value):
                count += 1
            continue
        if raw_array is None:
            continue
        try:
            values = json.loads(raw_array)
        except json.JSONDecodeError:
            continue
        if isinstance(values, list):
            count += sum(1 for value in values if token in str(value))
    return count


def retrospective_years_from_name(filename: str) -> int | None:
    """Получить N из суффикса retrospective_N."""
    match = re.search(r"retrospective_(\d+)", filename)
    return int(match.group(1)) if match else None


def unescape_json_text(value: str) -> str:
    """Декодировать JSON-escaped текст из HTML."""
    try:
        return json.loads(f'"{value}"')
    except json.JSONDecodeError:
        return value


def short_list(values: Iterable[str], limit: int = 8) -> str:
    """Сократить длинный список для консольного отчета."""
    items = list(values)
    if len(items) <= limit:
        return ", ".join(items)
    return ", ".join(items[:limit]) + f", ... (+{len(items) - limit})"


def parse_float(value: object) -> float | None:
    """Преобразовать число из CSV, включая русскую десятичную запятую."""
    text = str(value).strip().replace(" ", "").replace(",", ".")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def format_qa_number(value: float, digits: int = 1) -> str:
    """Формат QA-значения в том же виде, что и подписи графиков."""
    return f"{float(value):,.{digits}f}".replace(",", " ").replace(".", ",")


def check_monthly_heatmap_placement_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Check that the heatmap total column is informational and outside the color scale."""
    files = {path: html for path, html in html_by_file.items() if path.stem.startswith("monthly_heatmap_placement")}
    if not files:
        return QaResult("monthly_heatmap_placement_contract", True, "monthly_heatmap_placement не найден; проверка пропущена.")

    required_columns = {
        "report_year",
        "month",
        "month_order",
        "placement_volume_bln",
        "is_total_column",
        "total_placement_volume_bln",
        "color_scale_included",
        "label_display",
    }
    failed: list[str] = []
    for path, html in files.items():
        normalized = unescape_json_text(html)
        if "Итого" not in normalized:
            failed.append(f"{path.name}: нет колонки Итого в HTML")
        if "Цветовая шкала применяется только к месячным значениям" not in normalized:
            failed.append(f"{path.name}: нет пояснения, что колонка Итого показана справочно")
        if "f3f4f6" not in normalized.lower():
            failed.append(f"{path.name}: нет нейтрального фона итоговой колонки")
        csv_path = config.EXPORTS_CHART_DATA_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed.append(f"{path.name}: нет CSV-основы")
            continue
        rows = read_csv_rows(csv_path)
        if not rows:
            failed.append(f"{csv_path.name}: пустой CSV")
            continue
        missing = sorted(required_columns.difference(rows[0].keys()))
        if missing:
            failed.append(f"{csv_path.name}: нет {', '.join(missing)}")
            continue
        totals_by_year: dict[str, float] = {}
        months_by_year: dict[str, float] = {}
        for row in rows:
            year = str(row.get("report_year", "")).strip()
            value = parse_float(row.get("placement_volume_bln", ""))
            if value is None:
                continue
            is_total = str(row.get("is_total_column", "")).strip().lower() in {"true", "1", "yes"}
            color_scale_included = str(row.get("color_scale_included", "")).strip().lower() in {
                "true",
                "1",
                "yes",
            }
            if is_total:
                if color_scale_included:
                    failed.append(f"{csv_path.name}: итоговая строка {year} участвует в color scale")
                totals_by_year[year] = totals_by_year.get(year, 0.0) + value
            else:
                if not color_scale_included:
                    failed.append(f"{csv_path.name}: месячная строка {year} исключена из color scale")
                months_by_year[year] = months_by_year.get(year, 0.0) + value
        for year, total_value in totals_by_year.items():
            month_sum = months_by_year.get(year, 0.0)
            if abs(total_value - month_sum) > 0.05:
                failed.append(f"{csv_path.name}: итог {year} не равен сумме месяцев")
        if not totals_by_year:
            failed.append(f"{csv_path.name}: нет строк is_total_column=True")

    if failed:
        return QaResult("monthly_heatmap_placement_contract", False, short_list(failed))
    return QaResult("monthly_heatmap_placement_contract", True, f"monthly_heatmap_placement проверен: {len(files)} файлов.")


def check_monthly_heatmap_revenue_contract(html_by_file: dict[Path, str]) -> QaResult:
    """Check the monthly revenue heatmap and its chart-data export."""
    files = {path: html for path, html in html_by_file.items() if path.stem.startswith("monthly_heatmap_revenue")}
    if not files:
        return QaResult("monthly_heatmap_revenue_contract", True, "monthly_heatmap_revenue не найден; проверка пропущена.")

    required_columns = {
        "report_year",
        "month",
        "month_order",
        "revenue_volume_bln",
        "placement_volume_bln",
        "nominal_revenue_gap_bln",
        "revenue_to_nominal_ratio",
        "auction_count",
        "data_quality_flag",
        "is_total_column",
        "total_revenue_volume_bln",
        "color_scale_included",
        "label_display",
    }
    failed: list[str] = []
    for path, html in files.items():
        normalized = unescape_json_text(html)
        if "Помесячная выручка от реализации ОФЗ" not in normalized:
            failed.append(f"{path.name}: некорректный title")
        if "Итого" not in normalized:
            failed.append(f"{path.name}: нет колонки Итого")
        if "Цветовая шкала применяется только к месячным значениям" not in normalized:
            failed.append(f"{path.name}: нет пояснения справочной итоговой колонки")
        csv_path = config.EXPORTS_CHART_DATA_MONTHLY_DIR / f"{path.stem}.csv"
        if not csv_path.exists():
            failed.append(f"{path.name}: нет CSV-основы в chart_data/monthly")
            continue
        rows = read_csv_rows(csv_path)
        if not rows:
            failed.append(f"{csv_path.name}: пустой CSV")
            continue
        missing = sorted(required_columns.difference(rows[0].keys()))
        if missing:
            failed.append(f"{csv_path.name}: нет {', '.join(missing)}")
            continue
        if not any(str(row.get("is_total_column", "")).lower() in {"true", "1", "yes"} for row in rows):
            failed.append(f"{csv_path.name}: нет is_total_column=True")
        if any(
            str(row.get("is_total_column", "")).lower() in {"true", "1", "yes"}
            and str(row.get("color_scale_included", "")).lower() in {"true", "1", "yes"}
            for row in rows
        ):
            failed.append(f"{csv_path.name}: итоговая колонка участвует в color scale")

    if failed:
        return QaResult("monthly_heatmap_revenue_contract", False, short_list(failed))
    return QaResult("monthly_heatmap_revenue_contract", True, f"monthly_heatmap_revenue проверен: {len(files)} файлов.")


if __name__ == "__main__":
    raise SystemExit(main())
