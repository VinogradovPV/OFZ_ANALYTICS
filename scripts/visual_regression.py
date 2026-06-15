"""Visual regression / fallback inspection для HTML-графиков OFZ_ANALITICS.

Если screenshot backend отсутствует, скрипт выполняет статический анализ HTML и
Plotly payload: trace types, titles, axis titles, annotations, legend,
hovertemplate, total labels и volume-scale policy.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence, cast
from urllib.parse import quote

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, report_params, utils
    from scripts.qa.visual_regression_contracts import (
        STACKED_STRUCTURE_FILENAME_TOKENS,
        VOLUME_FILENAME_TOKENS,
        VisualCheck,
        YIELD_DISCOUNT_CLUSTER_WARN_THRESHOLD,
        YIELD_DISCOUNT_FACET_MAX_LABELS_PER_PANEL,
        YIELD_DISCOUNT_FACET_MAX_LABELS_TOTAL,
        YIELD_DISCOUNT_LABEL_BUFFER,
        YIELD_DISCOUNT_MAIN_MAX_LABELS_TOTAL,
        YIELD_DISCOUNT_OUTLIERS_MAX_LABELS_TOTAL,
    )
else:
    from . import config, report_params, utils
    from .qa.visual_regression_contracts import (
        STACKED_STRUCTURE_FILENAME_TOKENS,
        VOLUME_FILENAME_TOKENS,
        VisualCheck,
        YIELD_DISCOUNT_CLUSTER_WARN_THRESHOLD,
        YIELD_DISCOUNT_FACET_MAX_LABELS_PER_PANEL,
        YIELD_DISCOUNT_FACET_MAX_LABELS_TOTAL,
        YIELD_DISCOUNT_LABEL_BUFFER,
        YIELD_DISCOUNT_MAIN_MAX_LABELS_TOTAL,
        YIELD_DISCOUNT_OUTLIERS_MAX_LABELS_TOTAL,
    )


VISUAL_REGRESSION_REPORT_DOC = config.get_doc_path("visual_regression_report.md")
VISUAL_REGRESSION_REPORTS_DIR = config.REPORTS_DIR / "visual_regression"
VISUAL_REGRESSION_SCREENSHOTS_DIR = VISUAL_REGRESSION_REPORTS_DIR / "screenshots"
VISUAL_REGRESSION_BASELINE_DIR = VISUAL_REGRESSION_REPORTS_DIR / "baseline"
VISUAL_REGRESSION_DIFFS_DIR = VISUAL_REGRESSION_REPORTS_DIR / "diffs"
TECHNICAL_TICK_PATTERN = re.compile(r"(?<![A-Za-zА-Яа-я0-9])(?:1|2|5|8)(?:M|B|k)(?![A-Za-zА-Яа-я0-9])")
CYRILLIC_PATTERN = re.compile(r"[А-Яа-яЁё]")

@dataclass(frozen=True)
class ScreenshotArtifact:
    """Screenshot artifact metadata for report and diff manifest."""

    html_file: str
    screenshot_file: str
    size_bytes: int
    sha256: str
    baseline_status: str
    diff_message: str


def main(argv: Sequence[str] | None = None) -> int:
    """Запустить visual regression или fallback inspection."""
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    args = parse_args(argv)
    config.ensure_output_directories()
    VISUAL_REGRESSION_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    VISUAL_REGRESSION_SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    VISUAL_REGRESSION_DIFFS_DIR.mkdir(parents=True, exist_ok=True)

    html_files = sorted(args.charts_dir.rglob("*.html"))
    html_files = filter_html_files(html_files, args)
    run_id = build_run_id(args)
    backend_status, screenshot_checks, screenshot_artifacts = run_screenshot_backend(html_files, args, run_id)
    checks = [VisualCheck("-", "visual_regression_mode", "ok", backend_status["message"])]
    checks.extend(screenshot_checks)
    checks.extend(inspect_html_files(html_files, args, backend_status))
    write_screenshot_manifest(args, run_id, backend_status, screenshot_artifacts)
    report = render_report(args, backend_status, checks, html_files, screenshot_artifacts)
    utils.write_markdown(VISUAL_REGRESSION_REPORT_DOC, report)

    output_report = VISUAL_REGRESSION_REPORTS_DIR / f"visual_regression_report_{run_id}.md"
    utils.write_markdown(output_report, report)
    logger.info("Visual regression report записан: %s", output_report)

    for check in checks:
        print_console(f"{check.status.upper()} | {check.file} | {check.check} | {check.message}")
    print_console(VISUAL_REGRESSION_REPORT_DOC.relative_to(config.PROJECT_ROOT).as_posix())

    failed = [check for check in checks if check.status == "fail"]
    return 1 if failed else 0


def print_console(value: str) -> None:
    """Безопасно вывести строку в консоль Windows с ограниченной кодировкой."""
    encoding = sys.stdout.encoding or "utf-8"
    safe_value = value.encode(encoding, errors="replace").decode(encoding, errors="replace")
    print(safe_value)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Разобрать параметры visual regression."""
    parser = argparse.ArgumentParser(description="Visual regression / fallback HTML inspection.")
    parser.add_argument("--charts-dir", type=Path, default=config.CHARTS_DIR, help="Папка HTML-графиков.")
    parser.add_argument("--report-date", default=None, help="Отчетная дата для фильтра HTML.")
    parser.add_argument("--retrospective-years", type=int, default=None, help="Ретроспектива для фильтра HTML.")
    parser.add_argument("--period-type", choices=sorted(report_params.ALLOWED_PERIOD_TYPES), default=None, help="Тип периода.")
    parser.add_argument("--aggregation-mode", choices=sorted(report_params.ALLOWED_AGGREGATION_MODES), default=None, help="Режим агрегации.")
    parser.add_argument(
        "--mode",
        choices=("auto", "screenshot", "fallback"),
        default="auto",
        help="Visual regression mode: fallback HTML/Plotly inspection, screenshot backend, or auto fallback.",
    )
    parser.add_argument(
        "--screenshot-backend",
        choices=("auto", "none"),
        default=None,
        help="Backend скриншотов. Сейчас поддержан fallback inspection; none принудительно отключает screenshots.",
    )
    return parser.parse_args(argv)


def detect_screenshot_backend(args: argparse.Namespace) -> dict[str, str]:
    """Определить доступность screenshot backend.

    На текущем этапе второй модернизации backend не навязывается: если он не
    подключен явно будущей реализацией, используется fallback HTML/Plotly анализ.
    """
    if args.screenshot_backend == "none":
        return {"mode": "fallback_static_html", "message": "Screenshot backend отключен параметром."}
    return {
        "mode": "fallback_static_html",
        "message": "Screenshot backend не настроен; выполнен fallback static HTML / Plotly JSON inspection.",
    }


def effective_mode(args: argparse.Namespace) -> str:
    """Return requested visual regression mode with deprecated flag compatibility."""
    if args.screenshot_backend == "none":
        return "fallback"
    return str(args.mode or "auto")


def run_screenshot_backend(
    html_files: Sequence[Path],
    args: argparse.Namespace,
    run_id: str,
) -> tuple[dict[str, str], list[VisualCheck], list[ScreenshotArtifact]]:
    """Run Playwright screenshot backend, fallback, or auto mode."""
    mode = effective_mode(args)
    if mode == "fallback":
        return (
            {
                "mode": "fallback_static_html",
                "message": "visual_regression_mode=fallback; screenshot backend disabled by request.",
            },
            [],
            [],
        )
    if not html_files:
        return (
            {
                "mode": "screenshot_not_run",
                "message": f"visual_regression_mode={mode}; no HTML files available for screenshots.",
            },
            [],
            [],
        )

    try:
        artifacts = capture_playwright_screenshots(html_files, run_id)
    except Exception as exc:
        if mode == "screenshot":
            return (
                {
                    "mode": "screenshot_failed",
                    "message": f"visual_regression_mode=screenshot; screenshot backend failed: {exc}",
                },
                [VisualCheck("-", "screenshot_backend", "fail", f"Playwright screenshot backend failed: {exc}")],
                [],
            )
        return (
            {
                "mode": "auto_fallback_static_html",
                "message": f"visual_regression_mode=auto; screenshot backend unavailable, fallback used: {exc}",
            },
            [VisualCheck("-", "screenshot_backend", "warning", f"Playwright unavailable; fallback used: {exc}")],
            [],
        )

    checks = [
        VisualCheck("-", "screenshot_backend", "ok", f"Playwright screenshots created: {len(artifacts)}."),
        VisualCheck("-", "screenshot_diff_report", "ok", "Screenshot manifest and baseline diff status written."),
    ]
    return (
        {
            "mode": "screenshot_playwright",
            "message": "visual_regression_mode=screenshot_playwright; fallback HTML/Plotly inspection also executed.",
        },
        checks,
        artifacts,
    )


def capture_playwright_screenshots(html_files: Sequence[Path], run_id: str) -> list[ScreenshotArtifact]:
    """Capture stable screenshots for local Plotly HTML files with Playwright."""
    try:
        playwright_sync_api = importlib.import_module("playwright.sync_api")
        playwright_timeout_error = cast(type[BaseException], getattr(playwright_sync_api, "TimeoutError"))
        sync_playwright = getattr(playwright_sync_api, "sync_playwright")
    except Exception as exc:  # pragma: no cover - optional dev dependency.
        raise RuntimeError("Python package 'playwright' is not installed") from exc

    run_dir = VISUAL_REGRESSION_SCREENSHOTS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    artifacts: list[ScreenshotArtifact] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
            for html_path in html_files:
                screenshot_path = run_dir / f"{html_path.stem}.png"
                page.goto(path_to_file_url(html_path), wait_until="networkidle", timeout=45_000)
                page.add_style_tag(
                    content="""
                    .modebar, .modebar-container { display: none !important; }
                    * { cursor: default !important; caret-color: transparent !important; }
                    """
                )
                try:
                    page.wait_for_selector(".plotly-graph-div", timeout=20_000)
                    page.wait_for_function(
                        "() => window.Plotly && document.querySelectorAll('.plotly-graph-div .main-svg').length > 0",
                        timeout=20_000,
                    )
                except playwright_timeout_error:
                    page.wait_for_timeout(2_000)
                page.mouse.move(0, 0)
                page.screenshot(path=str(screenshot_path), full_page=True)
                artifacts.append(build_screenshot_artifact(html_path, screenshot_path))
        finally:
            browser.close()
    return artifacts


def build_screenshot_artifact(html_path: Path, screenshot_path: Path) -> ScreenshotArtifact:
    """Build screenshot metadata and compare checksum with optional baseline file."""
    digest = sha256_file(screenshot_path)
    baseline_path = VISUAL_REGRESSION_BASELINE_DIR / screenshot_path.name
    if baseline_path.exists():
        baseline_digest = sha256_file(baseline_path)
        baseline_status = "match" if baseline_digest == digest else "changed"
        diff_message = "Matches baseline checksum." if baseline_status == "match" else "Checksum differs from baseline."
    else:
        baseline_status = "missing_baseline"
        diff_message = "No baseline screenshot found; current screenshot recorded as generated output."
    return ScreenshotArtifact(
        html_file=html_path.relative_to(config.PROJECT_ROOT).as_posix(),
        screenshot_file=screenshot_path.relative_to(config.PROJECT_ROOT).as_posix(),
        size_bytes=screenshot_path.stat().st_size,
        sha256=digest,
        baseline_status=baseline_status,
        diff_message=diff_message,
    )


def path_to_file_url(path: Path) -> str:
    """Convert local path to a file:// URL accepted by Playwright on Windows."""
    resolved = path.resolve()
    return "file:///" + quote(str(resolved).replace("\\", "/"), safe="/:")


def sha256_file(path: Path) -> str:
    """Calculate SHA256 for generated screenshot or baseline."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def write_screenshot_manifest(
    args: argparse.Namespace,
    run_id: str,
    backend_status: dict[str, str],
    artifacts: Sequence[ScreenshotArtifact],
) -> None:
    """Write screenshot backend manifest and simple diff report as generated outputs."""
    manifest = {
        "run_id": run_id,
        "visual_regression_mode": backend_status["mode"],
        "message": backend_status["message"],
        "report_date": args.report_date,
        "period_type": args.period_type,
        "aggregation_mode": args.aggregation_mode,
        "retrospective_years": args.retrospective_years,
        "artifacts": [artifact.__dict__ for artifact in artifacts],
    }
    manifest_path = VISUAL_REGRESSION_REPORTS_DIR / f"screenshot_manifest_{run_id}.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    diff_path = VISUAL_REGRESSION_DIFFS_DIR / f"screenshot_diff_report_{run_id}.md"
    lines = [
        "# Screenshot visual regression diff report",
        "",
        f"- visual_regression_mode: `{backend_status['mode']}`",
        f"- run_id: `{run_id}`",
        f"- screenshots: `{len(artifacts)}`",
        "",
        "| HTML | Screenshot | Baseline status | Message |",
        "| --- | --- | --- | --- |",
    ]
    for artifact in artifacts:
        lines.append(
            f"| `{artifact.html_file}` | `{artifact.screenshot_file}` | `{artifact.baseline_status}` | {escape_table_text(artifact.diff_message)} |"
        )
    diff_path.write_text("\n".join(lines), encoding="utf-8")


def filter_html_files(html_files: Sequence[Path], args: argparse.Namespace) -> list[Path]:
    """Отфильтровать HTML по параметрам отчета, если они переданы полностью."""
    required = (args.report_date, args.retrospective_years, args.period_type, args.aggregation_mode)
    if not all(value is not None for value in required):
        return list(html_files)
    suffix = f"_{args.period_type}_{args.aggregation_mode}_{args.report_date}_retrospective_{args.retrospective_years}"
    filtered = [path for path in html_files if suffix in path.stem]
    return filtered if filtered else list(html_files)


def inspect_html_files(
    html_files: Sequence[Path],
    args: argparse.Namespace,
    backend_status: dict[str, str],
) -> list[VisualCheck]:
    """Выполнить fallback inspection HTML-файлов."""
    checks: list[VisualCheck] = []
    if not args.charts_dir.exists():
        return [VisualCheck("-", "charts_dir_exists", "fail", f"Папка не найдена: {args.charts_dir}")]
    if not html_files:
        return [VisualCheck("-", "html_files_exist", "fail", "HTML-графики не найдены.")]

    checks.append(VisualCheck("-", "screenshot_backend", "ok", backend_status["message"]))
    checks.append(VisualCheck("-", "html_files_exist", "ok", f"Найдено HTML-файлов: {len(html_files)}."))
    checks.append(check_yield_vs_discount_exists(html_files))

    for path in html_files:
        html = read_text(path)
        payload = extract_plot_payload(html)
        data_segment = extract_newplot_data_segment(payload)
        layout_segment = extract_newplot_layout_segment(payload, data_segment)
        inspection_text = data_segment + "\n" + layout_segment
        traces = extract_trace_types(data_segment)
        checks.extend(
            [
                check_trace_types(path, traces),
                check_title(path, inspection_text),
                check_axis_titles(path, inspection_text),
                check_annotations(path, inspection_text),
                check_legend(path, inspection_text, traces),
                check_hovertemplate(path, inspection_text),
                check_volume_ticks(path, inspection_text),
                check_stacked_total_labels(path, inspection_text),
                check_format_structure_contract(path, inspection_text),
                check_monthly_demand_supply_labels(path, inspection_text),
                check_monthly_placement_volume_labels(path, inspection_text),
                check_monthly_cumulative_placement_labels(path, inspection_text),
                check_monthly_heatmap_total_contract(path, inspection_text, traces),
                check_facet_yaxis_titles(path, inspection_text),
                check_demand_cutoff_contract(path, inspection_text),
                check_yield_vs_discount_contract(path, inspection_text),
                check_format_discount_contract(path, inspection_text),
                check_format_terms_comparison_contract(path, inspection_text),
                check_format_terms_aggregate_scatter_contract(path, inspection_text),
                check_format_terms_scatter_contract(path, inspection_text),
                check_format_terms_delta_contract(path, inspection_text),
            ]
        )
    return checks


def read_text(path: Path) -> str:
    """Прочитать HTML с запасным вариантом кодировки."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def extract_plot_payload(html: str) -> str:
    """Оставить участок с последним Plotly.newPlot."""
    marker = "Plotly.newPlot("
    index = html.rfind(marker)
    return html[index:] if index >= 0 else html


def extract_newplot_data_segment(payload: str) -> str:
    """Извлечь фактический data-array из Plotly.newPlot."""
    start = payload.find("[")
    if start < 0:
        return payload
    return extract_balanced_segment(payload, start, "[", "]")


def extract_newplot_layout_segment(payload: str, data_segment: str) -> str:
    """Извлечь layout-object из Plotly.newPlot без обращения к встроенной библиотеке."""
    data_start = payload.find(data_segment)
    search_from = data_start + len(data_segment) if data_start >= 0 else 0
    start = payload.find("{", search_from)
    if start < 0:
        return ""
    return extract_balanced_segment(payload, start, "{", "}")


def extract_balanced_segment(text: str, start: int, open_char: str, close_char: str) -> str:
    """Извлечь сбалансированный JSON-подобный фрагмент с учетом строк."""
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
            continue
        if char == open_char:
            depth += 1
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return text[start:]


def extract_trace_types(payload: str) -> list[str]:
    """Извлечь типы traces из Plotly payload."""
    return re.findall(r'"type"\s*:\s*"([^"]+)"', payload)


def check_trace_types(path: Path, traces: Sequence[str]) -> VisualCheck:
    """Проверить наличие traces."""
    if not traces:
        return VisualCheck(path.name, "trace_types", "fail", "Trace types не найдены.")
    return VisualCheck(path.name, "trace_types", "ok", ", ".join(sorted(set(traces))))


def check_title(path: Path, html: str) -> VisualCheck:
    """Проверить наличие русскоязычного title."""
    title = extract_title(html)
    if not title:
        return VisualCheck(path.name, "title", "warning", "Title не распознан статически.")
    if not CYRILLIC_PATTERN.search(title):
        return VisualCheck(path.name, "title", "fail", f"Title без кириллицы: {title}")
    return VisualCheck(path.name, "title", "ok", title)


def extract_title(html: str) -> str:
    """Извлечь title из layout или HTML."""
    object_titles = re.findall(r'"title"\s*:\s*\{\s*"text"\s*:\s*"(?P<title>[^"]+)"', html, flags=re.IGNORECASE | re.DOTALL)
    if object_titles:
        return clean_json_text(object_titles[-1])
    string_titles = re.findall(r'"title"\s*:\s*"(?P<title>[^"]+)"', html, flags=re.IGNORECASE | re.DOTALL)
    if string_titles:
        return clean_json_text(string_titles[-1])
    html_titles = re.findall(r"<title>(?P<title>.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if html_titles:
        return clean_json_text(html_titles[-1])
    return ""


def check_axis_titles(path: Path, html: str) -> VisualCheck:
    """Проверить подписи осей или эквивалентные измерения."""
    axis_tokens = ("Период", "Год", "Месяц", "Доходность", "Объем", "Спрос", "Предложение", "Вид ОФЗ")
    if any(token in html for token in axis_tokens):
        return VisualCheck(path.name, "axis_titles", "ok", "Русские подписи осей/измерений найдены.")
    return VisualCheck(path.name, "axis_titles", "fail", "Русские подписи осей/измерений не найдены.")


def check_annotations(path: Path, html: str) -> VisualCheck:
    """Проверить annotations как подписи, thresholds или subtitles."""
    count = html.count('"annotations"')
    text_count = len(re.findall(r'"text"\s*:', html))
    if count or text_count:
        return VisualCheck(path.name, "annotations", "ok", f"Найдены annotation/text entries: {text_count}.")
    return VisualCheck(path.name, "annotations", "warning", "Annotations/text entries не найдены.")


def check_legend(path: Path, html: str, traces: Sequence[str]) -> VisualCheck:
    """Проверить наличие легенды или допустимость ее отсутствия."""
    if len(set(traces)) <= 1 and len(traces) <= 1:
        return VisualCheck(path.name, "legend", "ok", "Один trace; легенда не обязательна.")
    if '"showlegend":false' in html.replace(" ", "").lower():
        return VisualCheck(path.name, "legend", "ok", "Легенда отключена явно; статический fallback считает это допустимым.")
    if "legend" in html.lower() or '"name"' in html:
        return VisualCheck(path.name, "legend", "ok", "Legend/name metadata найдено.")
    return VisualCheck(path.name, "legend", "warning", "Legend metadata не найдено.")


def check_hovertemplate(path: Path, html: str) -> VisualCheck:
    """Проверить наличие hovertemplate."""
    if "hovertemplate" not in html:
        return VisualCheck(path.name, "hovertemplate", "fail", "hovertemplate отсутствует.")
    if not any(token in html for token in ("Период", "Дата", "Спрос", "Объем", "Доходность", "Размещение")):
        return VisualCheck(path.name, "hovertemplate", "warning", "hovertemplate найден, но русские подписи не подтверждены.")
    return VisualCheck(path.name, "hovertemplate", "ok", "hovertemplate найден.")


def check_volume_ticks(path: Path, html: str) -> VisualCheck:
    """Проверить volume charts на отсутствие 5M/8M и наличие млрд рублей."""
    if not is_volume_chart_file(path):
        return VisualCheck(path.name, "volume_scale", "ok", "Не volume-график.")
    if TECHNICAL_TICK_PATTERN.search(html):
        return VisualCheck(path.name, "volume_scale", "fail", "Найден технический tick suffix M/B/k.")
    normalized = html.lower()
    if path.stem.startswith("monthly_heatmap_revenue"):
        if "РІС‹СЂСѓС‡Рє" not in normalized and "выручк" not in normalized:
            return VisualCheck(path.name, "volume_scale", "fail", "Нет явного указания выручки от реализации.")
        if "РјР»СЂРґ" not in normalized and "млрд" not in normalized:
            return VisualCheck(path.name, "volume_scale", "warning", "Не найдено указание млрд рублей.")
        return VisualCheck(path.name, "volume_scale", "ok", "Revenue volume policy подтверждена.")
    if "объем размещения по номиналу" not in normalized and "объему размещения по номиналу" not in normalized:
        return VisualCheck(path.name, "volume_scale", "fail", "Нет явного указания объема размещения по номиналу.")
    if "млрд" not in normalized:
        return VisualCheck(path.name, "volume_scale", "warning", "Не найдено указание млрд рублей.")
    return VisualCheck(path.name, "volume_scale", "ok", "Volume policy подтверждена.")


def is_volume_chart_file(path: Path) -> bool:
    """Определить графики, где volume является отображаемой метрикой, а не частью ratio-названия."""
    stem = path.stem
    ratio_or_scatter_tokens = (
        "risk_quadrant",
        "demand_cutoff",
        "discount_vs_demand",
        "yield_vs_demand",
        "bid_to_cover",
    )
    if any(token in stem for token in ratio_or_scatter_tokens):
        return False
    return any(token in stem for token in VOLUME_FILENAME_TOKENS)


def check_stacked_total_labels(path: Path, html: str) -> VisualCheck:
    """Проверить total labels на stacked structure charts."""
    if not any(token in path.stem for token in STACKED_STRUCTURE_FILENAME_TOKENS):
        return VisualCheck(path.name, "stacked_total_labels", "ok", "Не stacked structure chart.")
    if "Итого" in html or "итого" in html.lower():
        return VisualCheck(path.name, "stacked_total_labels", "ok", "Total labels найдены.")
    return VisualCheck(path.name, "stacked_total_labels", "fail", "Не найдены total labels для stacked chart.")


def check_format_structure_contract(path: Path, html: str) -> VisualCheck:
    """Fallback-проверка подписей сегментов и итогов на format_structure."""
    if not path.stem.startswith("format_structure"):
        return VisualCheck(path.name, "format_structure_contract", "ok", "Не format_structure.")

    text = clean_json_text(html)
    normalized = text.lower()
    if "объем размещения по номиналу, млрд рублей" not in normalized:
        return VisualCheck(path.name, "format_structure_contract", "fail", "Ось Y не подтверждает номинальный объем в млрд рублей.")
    if "итого" not in normalized:
        return VisualCheck(path.name, "format_structure_contract", "fail", "Не найдены total labels.")

    text_values = [value for value in extract_string_array_values(html, "text") if value.strip()]
    numeric_labels = [value for value in text_values if re.search(r"\d", value)]
    if not numeric_labels:
        return VisualCheck(path.name, "format_structure_contract", "fail", "Не найдены числовые подписи сегментов.")

    csv_path = config.EXPORTS_CHART_DATA_STRUCTURE_DIR / f"{path.stem}.csv"
    if not csv_path.exists():
        return VisualCheck(path.name, "format_structure_contract", "warning", "CSV export не найден; проверен только HTML.")
    try:
        import csv

        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as error:
        return VisualCheck(path.name, "format_structure_contract", "warning", f"CSV недоступен: {error}")
    if not rows:
        return VisualCheck(path.name, "format_structure_contract", "fail", "CSV export пуст.")

    required_columns = {"label_display", "label_visible"}
    if required_columns.difference(rows[0].keys()):
        return VisualCheck(path.name, "format_structure_contract", "fail", "CSV не содержит label_display/label_visible.")
    has_total_field = "total_placement_volume_bln" in rows[0] or "column_total" in rows[0]
    if not has_total_field:
        return VisualCheck(path.name, "format_structure_contract", "fail", "CSV не содержит поле итога столбца.")
    visible_rows = [
        row
        for row in rows
        if str(row.get("label_visible", "")).strip().lower() in {"true", "1", "yes"}
        and row.get("label_display", "").strip()
    ]
    if not visible_rows:
        return VisualCheck(path.name, "format_structure_contract", "fail", "В CSV нет видимых подписей сегментов.")

    return VisualCheck(path.name, "format_structure_contract", "ok", "Подписи сегментов и total labels format_structure подтверждены.")


def check_monthly_demand_supply_labels(path: Path, html: str) -> VisualCheck:
    """Проверить подписи данных и hover/ось на monthly_demand_supply."""
    if not path.stem.startswith("monthly_demand_supply"):
        return VisualCheck(path.name, "monthly_demand_supply_labels", "ok", "Не monthly_demand_supply.")
    normalized = html.replace("\\/", "/").replace("\\u002f", "/").replace("\\u002F", "/")
    if "Объем, млрд рублей" not in normalized:
        return VisualCheck(path.name, "monthly_demand_supply_labels", "fail", "Некорректная ось Y.")
    if "Спрос" not in normalized or "Предложение" not in normalized or "hovertemplate" not in normalized:
        return VisualCheck(path.name, "monthly_demand_supply_labels", "fail", "Hover не подтверждает спрос и предложение.")
    text_values = [value for value in extract_string_array_values(html, "text") if value.strip()]
    if not text_values:
        return VisualCheck(path.name, "monthly_demand_supply_labels", "fail", "Подписи данных не найдены.")
    return VisualCheck(path.name, "monthly_demand_supply_labels", "ok", "Подписи спроса/предложения найдены.")


def check_monthly_placement_volume_labels(path: Path, html: str) -> VisualCheck:
    """Проверить наличие и вариативность подписей monthly_placement_volume."""
    if not path.stem.startswith("monthly_placement_volume"):
        return VisualCheck(path.name, "monthly_placement_volume_labels", "ok", "Не monthly_placement_volume.")
    normalized = html.replace("\\/", "/").replace("\\u002f", "/").replace("\\u002F", "/")
    if "Объем размещения по номиналу, млрд рублей" not in normalized:
        return VisualCheck(path.name, "monthly_placement_volume_labels", "fail", "Некорректная ось Y.")
    if '"text"' not in html:
        return VisualCheck(path.name, "monthly_placement_volume_labels", "fail", "Подписи данных не найдены.")
    text_values = extract_string_array_values(html, "text")
    y_values = extract_numeric_array_values(html, "y")
    non_empty_text = [value for value in text_values if value]
    distinct_y = {round(value, 6) for value in y_values}
    if len(distinct_y) > 1 and len(set(non_empty_text)) <= 1:
        return VisualCheck(
            path.name,
            "monthly_placement_volume_labels",
            "fail",
            "Подписи выглядят константными при разных Y; возможна рассинхронизация text и y.",
        )
    return VisualCheck(path.name, "monthly_placement_volume_labels", "ok", "Подписи monthly_placement_volume найдены.")


def check_monthly_cumulative_placement_labels(path: Path, html: str) -> VisualCheck:
    """Проверить подписи ключевых точек на monthly_cumulative_placement."""
    if not path.stem.startswith("monthly_cumulative_placement"):
        return VisualCheck(path.name, "monthly_cumulative_placement_labels", "ok", "Не monthly_cumulative_placement.")
    normalized = html.replace("\\/", "/").replace("\\u002f", "/").replace("\\u002F", "/")
    if "Накопленный объем размещения по номиналу, млрд рублей" not in normalized:
        return VisualCheck(path.name, "monthly_cumulative_placement_labels", "fail", "Некорректная ось Y.")
    text_values = [value for value in extract_string_array_values(html, "text") if value.strip()]
    if not text_values:
        return VisualCheck(path.name, "monthly_cumulative_placement_labels", "fail", "Подписи ключевых точек не найдены.")
    return VisualCheck(path.name, "monthly_cumulative_placement_labels", "ok", "Подписи ключевых точек найдены.")


def check_monthly_heatmap_total_contract(path: Path, html: str, traces: Sequence[str]) -> VisualCheck:
    """Check that heatmap totals are drawn as a neutral informational overlay."""
    if not path.stem.startswith(("monthly_heatmap_placement", "monthly_heatmap_revenue")):
        return VisualCheck(path.name, "monthly_heatmap_total_contract", "ok", "Не monthly heatmap.")

    normalized = clean_json_text(html)
    if "Цветовая шкала применяется только к месячным значениям" not in normalized:
        return VisualCheck(path.name, "monthly_heatmap_total_contract", "fail", "Нет subtitle о справочной итоговой колонке.")
    if "Итого" not in normalized:
        return VisualCheck(path.name, "monthly_heatmap_total_contract", "fail", "Колонка Итого не найдена.")
    if traces.count("heatmap") < 2:
        return VisualCheck(path.name, "monthly_heatmap_total_contract", "fail", "Итого не вынесено в отдельный heatmap overlay.")
    lowered = normalized.lower()
    if "f3f4f6" not in lowered:
        return VisualCheck(path.name, "monthly_heatmap_total_contract", "fail", "Нет нейтрального фона итоговой колонки.")
    if "9ca3af" not in lowered and '"shapes"' not in lowered:
        return VisualCheck(path.name, "monthly_heatmap_total_contract", "warning", "Визуальный разделитель перед Итого не распознан статически.")
    return VisualCheck(path.name, "monthly_heatmap_total_contract", "ok", "Итого вынесено в нейтральный overlay вне основной шкалы.")


def check_facet_yaxis_titles(path: Path, html: str) -> VisualCheck:
    """Проверить, что facet-графики не повторяют Y-title в каждой панели."""
    facet_tokens = (
        "monthly_demand_supply",
        "monthly_placement_by_format",
        "monthly_placement_by_maturity",
        "monthly_revenue_vs_nominal",
        "yield_vs_discount_facet",
    )
    if not any(path.stem.startswith(token) for token in facet_tokens):
        return VisualCheck(path.name, "facet_yaxis_titles", "ok", "Не facet-график.")
    axis_titles = re.findall(r'"(?:xaxis|yaxis)\d*"\s*:\s*\{[^{}]*"title"\s*:\s*\{[^{}]*"text"\s*:\s*"([^"]*)"', html)
    y_titles = [clean_json_text(title) for title in axis_titles if "Доходность" in title or "Объем" in title or "Объ" in title]
    counts: dict[str, int] = {}
    for title in y_titles:
        counts[title] = counts.get(title, 0) + 1
    repeated = [f"{title}={count}" for title, count in counts.items() if title and count > 1]
    if repeated:
        return VisualCheck(path.name, "facet_yaxis_titles", "fail", "Повторяются Y-title: " + ", ".join(repeated))
    return VisualCheck(path.name, "facet_yaxis_titles", "ok", "Повторяющиеся Y-title не найдены.")


def check_demand_cutoff_contract(path: Path, html: str) -> VisualCheck:
    """Проверить bubble-size explanation и лимит подписей demand_cutoff_explanation."""
    if not path.stem.startswith("demand_cutoff_explanation"):
        return VisualCheck(path.name, "demand_cutoff_contract", "ok", "Не demand_cutoff_explanation.")
    text = clean_json_text(html)
    normalized = text.lower()
    has_fixed_fallback = "фиксированный размер" in normalized or "fixed-size" in normalized
    if "размер точки = объем размещения по номиналу" not in normalized and not has_fixed_fallback:
        return VisualCheck(path.name, "demand_cutoff_contract", "fail", "Нет пояснения размера точки или fixed-size fallback.")
    label_count = max_text_label_count_from_payload(html)
    if label_count is not None and label_count > 35:
        return VisualCheck(path.name, "demand_cutoff_contract", "fail", f"Слишком много подписей: {label_count}.")
    return VisualCheck(path.name, "demand_cutoff_contract", "ok", "Bubble-size policy и лимит подписей подтверждены.")


def check_yield_vs_discount_exists(html_files: Sequence[Path]) -> VisualCheck:
    """Проверить наличие нового семейства yield_vs_discount."""
    files = [path.name for path in html_files if path.stem.startswith("yield_vs_discount")]
    if not files:
        return VisualCheck("-", "yield_vs_discount_exists", "fail", "yield_vs_discount HTML не найден.")
    return VisualCheck("-", "yield_vs_discount_exists", "ok", f"Найдено yield_vs_discount HTML: {len(files)}.")


def check_format_discount_contract(path: Path, html: str) -> VisualCheck:
    """Fallback-проверка графика средневзвешенного дисконта по форматам."""
    if not path.stem.startswith("format_discount"):
        return VisualCheck(path.name, "format_discount_contract", "ok", "Не format_discount.")
    text = clean_json_text(html)
    normalized = text.lower()
    traces = parse_plot_data_traces(html)
    bar_traces = [trace for trace in traces if str(trace.get("type", "")).lower() == "bar"]
    if not bar_traces:
        return VisualCheck(path.name, "format_discount_contract", "fail", "Не найдены bar traces.")
    if "средневзвешенный дисконт к номиналу, п.п." not in normalized:
        return VisualCheck(path.name, "format_discount_contract", "fail", "Ось/заголовок не подтверждает дисконт в п.п.")
    if "y = средневзвешенный дисконт к номиналу, п.п." not in normalized:
        return VisualCheck(path.name, "format_discount_contract", "fail", "Subtitle не объясняет, что Y — средневзвешенный дисконт.")
    if "формат" not in normalized:
        return VisualCheck(path.name, "format_discount_contract", "fail", "Не подтвержден цветовой слой по формату.")
    text_values = [value for value in extract_string_array_values(html, "text") if value.strip()]
    if not any(re.search(r"\d", value) for value in text_values):
        return VisualCheck(path.name, "format_discount_contract", "fail", "Не найдены подписи значений дисконта.")
    required_hover_tokens = [
        "объем размещения по номиналу, млрд рублей",
        "минимальный дисконт",
        "максимальный дисконт",
        "качество данных",
    ]
    for token in required_hover_tokens:
        if token not in normalized:
            return VisualCheck(path.name, "format_discount_contract", "fail", f"Hover не содержит поле: {token}.")
    if "data_quality_flag:" in normalized:
        return VisualCheck(path.name, "format_discount_contract", "fail", "Hover содержит сырой data_quality_flag.")

    csv_path = config.EXPORTS_CHART_DATA_STRUCTURE_DIR / f"{path.stem}.csv"
    if not csv_path.exists():
        return VisualCheck(path.name, "format_discount_contract", "fail", "CSV export не найден.")
    try:
        import csv

        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as error:
        return VisualCheck(path.name, "format_discount_contract", "fail", f"CSV недоступен: {error}")
    if not rows:
        return VisualCheck(path.name, "format_discount_contract", "fail", "CSV export пуст.")
    required_columns = {
        "weighted_avg_discount_to_nominal",
        "placement_volume_bln",
        "label_visible",
        "data_quality_flag",
    }
    missing = required_columns.difference(rows[0].keys())
    if missing:
        return VisualCheck(path.name, "format_discount_contract", "fail", "CSV contract неполный: " + ", ".join(sorted(missing)))

    return VisualCheck(path.name, "format_discount_contract", "ok", "Discount-axis contract format_discount подтвержден.")


def check_format_terms_comparison_contract(path: Path, html: str) -> VisualCheck:
    """Fallback-проверка n labels и отсутствующих форматов в format_terms_comparison."""
    if not path.stem.startswith("format_terms_comparison"):
        return VisualCheck(path.name, "format_terms_comparison_contract", "ok", "Не format_terms_comparison.")
    text = clean_json_text(html)
    if "n — количество размещений" not in text and "n - количество размещений" not in text:
        return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Нет пояснения n в subtitle.")
    if "средневзвешенно по объему размещения по номиналу" not in text.lower():
        return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Subtitle не содержит метод агрегации.")
    if "Метрика=" in text or "metric_label=" in text or "Показатель=" in text:
        return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Facet title содержит технический префикс.")
    if "Доходность, % годовых" in text:
        return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Панель доходности названа слишком общо.")
    if "Средневзвешенная доходность размещения, % годовых" not in text:
        return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Нет точного названия доходности.")
    if '"text":"Значение"' in text or '"text": "Значение"' in text:
        return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Общий Y-title равен `Значение`.")
    if "Количество размещений формата" not in text:
        return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Hover не содержит количество размещений формата.")
    if "Исходное поле" not in text or "Метод агрегации" not in text or "Поле веса" not in text:
        return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Hover не содержит методологические поля.")
    if "data_quality_flag:" in text.lower():
        return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Hover содержит сырой data_quality_flag.")
    if "n=" not in text:
        return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Нет n в текстовых подписях.")
    csv_path = config.EXPORTS_CHART_DATA_STRUCTURE_DIR / f"{path.stem}.csv"
    if not csv_path.exists():
        return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "CSV export не найден.")
    try:
        import csv

        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as error:
        return VisualCheck(path.name, "format_terms_comparison_contract", "fail", f"CSV недоступен: {error}")
    if not rows:
        return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "CSV пуст.")
    required_metrics = {
        "yield_weighted_avg",
        "weighted_avg_discount_to_nominal",
        "revenue_to_nominal_pct",
        "nominal_revenue_gap_bln",
    }
    metric_codes = {row.get("metric_code", "") for row in rows}
    missing_metrics = required_metrics.difference(metric_codes)
    if missing_metrics:
        return VisualCheck(
            path.name,
            "format_terms_comparison_contract",
            "fail",
            "Не найдены обязательные метрики: " + ", ".join(sorted(missing_metrics)),
        )
    for row in rows:
        available = str(row.get("format_available", "")).strip().lower() in {"true", "1", "yes"}
        try:
            placement_count = int(float(row.get("placement_count") or 0))
        except ValueError:
            return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "placement_count не число.")
        if available and placement_count <= 0:
            return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "format_available=True при placement_count<=0.")
        if not available and placement_count != 0:
            return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "format_available=False при placement_count!=0.")
        if not available and row.get("label_display", "").strip():
            return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Для отсутствующего формата задана подпись.")
        if available and not row.get("source_column", "").strip():
            return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Нет source_column для доступной метрики.")
        if available and not row.get("aggregation_method", "").strip():
            return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Нет aggregation_method для доступной метрики.")
        if row.get("metric_code", "") == "yield_weighted_avg":
            if row.get("metric_name_ru", "") != "Средневзвешенная доходность размещения, % годовых":
                return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Нет точного metric_name_ru для доходности.")
            if row.get("source_column", "") != "weighted_avg_yield":
                return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Неверный source_column доходности.")
            if row.get("aggregation_method", "") != "weighted_average_by_placement_volume":
                return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Неверный aggregation_method доходности.")
            if row.get("weight_field", "") != "placement_volume":
                return VisualCheck(path.name, "format_terms_comparison_contract", "fail", "Неверный weight_field доходности.")
    return VisualCheck(path.name, "format_terms_comparison_contract", "ok", "n labels и CSV contract подтверждены.")


def check_format_terms_aggregate_scatter_contract(path: Path, html: str) -> VisualCheck:
    """Fallback-проверка основного агрегированного scatter по форматам."""
    if not path.stem.startswith("format_terms_aggregate_scatter"):
        return VisualCheck(path.name, "format_terms_aggregate_scatter_contract", "ok", "Не format_terms_aggregate_scatter.")
    text = clean_json_text(html)
    required = [
        "Средние условия размещения по форматам",
        "Одна точка",
        "формат размещения в периоде",
        "размер точки",
        "Формат",
        "Количество размещений формата",
        "Средневзвешенная доходность размещения",
    ]
    for token in required:
        if token not in text:
            return VisualCheck(path.name, "format_terms_aggregate_scatter_contract", "fail", f"Нет текста: {token}")
    if "data_quality_flag:" in text.lower():
        return VisualCheck(path.name, "format_terms_aggregate_scatter_contract", "fail", "Hover содержит сырой data_quality_flag.")
    csv_path = config.EXPORTS_CHART_DATA_SCATTER_DIR / f"{path.stem}.csv"
    if not csv_path.exists():
        return VisualCheck(path.name, "format_terms_aggregate_scatter_contract", "fail", "CSV export не найден.")
    try:
        import csv

        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as error:
        return VisualCheck(path.name, "format_terms_aggregate_scatter_contract", "fail", f"CSV недоступен: {error}")
    keys = [(row.get("report_period_label", ""), row.get("format", "")) for row in rows]
    if len(keys) != len(set(keys)):
        return VisualCheck(path.name, "format_terms_aggregate_scatter_contract", "fail", "CSV содержит дубли period × format.")
    required_columns = {
        "placement_count",
        "source_column_yield",
        "aggregation_method_yield",
        "weight_field_yield",
        "source_column_discount",
        "aggregation_method_discount",
        "weight_field_discount",
    }
    if rows and required_columns.difference(rows[0].keys()):
        return VisualCheck(path.name, "format_terms_aggregate_scatter_contract", "fail", "CSV contract неполный.")
    return VisualCheck(path.name, "format_terms_aggregate_scatter_contract", "ok", "Aggregate scatter contract подтвержден.")


def check_format_terms_scatter_contract(path: Path, html: str) -> VisualCheck:
    """Fallback-проверка detailed scatter по форматам."""
    if not path.stem.startswith("format_terms_scatter"):
        return VisualCheck(path.name, "format_terms_scatter_contract", "ok", "Не format_terms_scatter.")
    text = clean_json_text(html)
    required = [
        "Условия размещения ОФЗ по форматам",
        "Цвет",
        "формат",
        "форма",
        "вид ОФЗ",
        "размер",
        "объем размещения по номиналу",
        "Средневзвешенная доходность размещения",
    ]
    lower_text = text.lower()
    for token in required:
        if token.lower() not in lower_text:
            return VisualCheck(path.name, "format_terms_scatter_contract", "fail", f"Нет текста: {token}")
    if "цвет — формат" not in lower_text and "цвет - формат" not in lower_text:
        return VisualCheck(path.name, "format_terms_scatter_contract", "fail", "Subtitle не подтверждает color = format.")
    if "format + ofz_type" in text or "format_ofz_type" in text or "format_ofz" in text:
        return VisualCheck(path.name, "format_terms_scatter_contract", "fail", "Найдена смешанная категория format+ofz_type.")
    if "data_quality_flag:" in text.lower():
        return VisualCheck(path.name, "format_terms_scatter_contract", "fail", "Hover содержит сырой data_quality_flag.")
    label_count = max_text_label_count_from_payload(html)
    if label_count is not None and label_count > 25 + 5:
        return VisualCheck(path.name, "format_terms_scatter_contract", "fail", "Слишком много подписей точек.")
    csv_path = config.EXPORTS_CHART_DATA_SCATTER_DIR / f"{path.stem}.csv"
    if not csv_path.exists():
        return VisualCheck(path.name, "format_terms_scatter_contract", "fail", "CSV export не найден.")
    try:
        import csv

        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as error:
        return VisualCheck(path.name, "format_terms_scatter_contract", "fail", f"CSV недоступен: {error}")
    if not rows:
        return VisualCheck(path.name, "format_terms_scatter_contract", "fail", "CSV export пуст.")
    required_columns = {"format", "ofz_type", "label_visible", "placement_volume_bln"}
    missing = required_columns.difference(rows[0].keys())
    if missing:
        return VisualCheck(path.name, "format_terms_scatter_contract", "fail", "CSV contract неполный: " + ", ".join(sorted(missing)))
    return VisualCheck(path.name, "format_terms_scatter_contract", "ok", "Detailed scatter contract подтвержден.")


def check_format_terms_delta_contract(path: Path, html: str) -> VisualCheck:
    """Fallback-проверка смысловой легенды и facet-title для format_terms_delta_by_format."""
    if not path.stem.startswith("format_terms_delta_by_format"):
        return VisualCheck(path.name, "format_terms_delta_by_format_contract", "ok", "Не format_terms_delta_by_format.")
    text = clean_json_text(html)
    required = [
        "Разница условий размещения: ДРПА минус Аукцион",
        "Δ = ДРПА − Аукцион",
        "цвет показывает аналитическую оценку",
        "ДРПА хуже",
        "ДРПА лучше",
        "Различие малозначимо",
    ]
    for token in required:
        if token not in text:
            return VisualCheck(path.name, "format_terms_delta_by_format_contract", "fail", f"Нет текста: {token}")
    if "Показатель=" in text or "metric_name_ru=" in text:
        return VisualCheck(path.name, "format_terms_delta_by_format_contract", "fail", "Facet title содержит технический префикс.")
    if "ДРПА выше" in text or "ДРПА ниже" in text:
        return VisualCheck(path.name, "format_terms_delta_by_format_contract", "fail", "Осталась старая математическая легенда выше/ниже.")
    if "data_quality_flag:" in text.lower():
        return VisualCheck(path.name, "format_terms_delta_by_format_contract", "fail", "Hover содержит сырой data_quality_flag.")
    if "line" not in text.lower() and "shape" not in text.lower():
        return VisualCheck(path.name, "format_terms_delta_by_format_contract", "warning", "Нулевая линия не подтверждена по JSON.")
    return VisualCheck(path.name, "format_terms_delta_by_format_contract", "ok", "Смысловая легенда и facet-title подтверждены.")


def check_yield_vs_discount_contract(path: Path, html: str) -> VisualCheck:
    """Fallback-проверка Plotly JSON для семейства yield_vs_discount."""
    if not path.stem.startswith("yield_vs_discount"):
        return VisualCheck(path.name, "yield_vs_discount_contract", "ok", "Не yield_vs_discount.")
    text = clean_json_text(html)
    labels_by_trace = yield_discount_text_labels_by_trace(html)
    total_labels = sum(len(labels) for labels in labels_by_trace)
    if "Дисконт к номиналу, п.п." not in text or "Доходность, % годовых" not in text:
        return VisualCheck(path.name, "yield_vs_discount_contract", "fail", "Не подтверждены оси X/Y.")
    if "Год" not in text:
        return VisualCheck(path.name, "yield_vs_discount_contract", "fail", "Не найден legend title `Год`.")
    if "Размер пузыря" not in text and "Размер точки" not in text:
        return VisualCheck(path.name, "yield_vs_discount_contract", "fail", "Нет пояснения размера точки.")
    if "мед. дисконт" not in text and "мед. доходность" not in text and "Пунктирные линии — медианы периода" not in text:
        return VisualCheck(path.name, "yield_vs_discount_contract", "fail", "Reference lines медиан не подтверждены.")
    if path.stem.startswith("yield_vs_discount_facet"):
        if "yield_vs_discount_facet=" in text or "Период=" in text:
            return VisualCheck(path.name, "yield_vs_discount_contract", "fail", "Facet-заголовки панелей не человекочитаемые.")
        if "Пунктирные линии — медианы периода; размер точки — объем размещения по номиналу" not in text:
            return VisualCheck(path.name, "yield_vs_discount_contract", "fail", "Нет подзаголовка про медианы периода и размер точки.")
        if text.count("Общая медиана") > 0 or text.count("медиана периода") > 1:
            return VisualCheck(path.name, "yield_vs_discount_contract", "fail", "В facet дублируются длинные подписи медиан.")
        if total_labels > YIELD_DISCOUNT_FACET_MAX_LABELS_TOTAL + YIELD_DISCOUNT_LABEL_BUFFER:
            return VisualCheck(path.name, "yield_vs_discount_contract", "fail", f"В facet слишком много подписей: {total_labels}.")
        max_trace_labels = max((len(labels) for labels in labels_by_trace), default=0)
        if max_trace_labels > YIELD_DISCOUNT_FACET_MAX_LABELS_PER_PANEL + YIELD_DISCOUNT_LABEL_BUFFER:
            return VisualCheck(
                path.name,
                "yield_vs_discount_contract",
                "fail",
                f"В одной facet-панели/trace слишком много подписей: {max_trace_labels}.",
            )
        if max_trace_labels > YIELD_DISCOUNT_CLUSTER_WARN_THRESHOLD:
            return VisualCheck(path.name, "yield_vs_discount_contract", "warning", "Возможен плотный кластер подписей в одной панели.")
        axis_titles = re.findall(r'"(?:xaxis|yaxis)\d*"\s*:\s*\{[^{}]*"title"\s*:\s*\{[^{}]*"text"\s*:\s*"([^"]*)"', text)
        if axis_titles.count("Доходность, % годовых") > 1 or axis_titles.count("Дисконт к номиналу, п.п.") > 1:
            return VisualCheck(path.name, "yield_vs_discount_contract", "fail", "В facet повторяются подписи осей.")
    else:
        max_allowed = (
            YIELD_DISCOUNT_OUTLIERS_MAX_LABELS_TOTAL
            if path.stem.startswith("yield_vs_discount_outliers")
            else YIELD_DISCOUNT_MAIN_MAX_LABELS_TOTAL
        )
        if total_labels > max_allowed + YIELD_DISCOUNT_LABEL_BUFFER:
            return VisualCheck(path.name, "yield_vs_discount_contract", "fail", f"Слишком много подписей: {total_labels}.")
        if "мед. дисконт" not in text or "мед. доходность" not in text:
            return VisualCheck(path.name, "yield_vs_discount_contract", "fail", "Медианные линии не подписаны раздельно.")
    return VisualCheck(path.name, "yield_vs_discount_contract", "ok", "Контракт yield_vs_discount подтвержден.")


def yield_discount_text_labels_by_trace(html: str) -> list[list[str]]:
    """Извлечь видимые подписи точек `yield_vs_discount` по traces."""
    traces = parse_plot_data_traces(html)
    labels_by_trace: list[list[str]] = []
    ignored = {
        "мед. дисконт",
        "мед. доходность",
        "высокий дисконт / высокая доходность",
        "высокий дисконт / низкая доходность",
        "низкий дисконт / высокая доходность",
        "низкий дисконт / низкая доходность",
    }
    for trace in traces:
        raw_text = trace.get("text")
        if not isinstance(raw_text, list):
            continue
        labels = [str(value).strip() for value in raw_text if str(value or "").strip()]
        point_labels = [label for label in labels if label not in ignored and "медиан" not in label.lower()]
        if point_labels:
            labels_by_trace.append(point_labels)
    return labels_by_trace


def max_text_label_count_from_payload(html: str) -> int | None:
    """Оценить максимальное число непустых подписей в одном массиве Plotly `text`."""
    counts: list[int] = []
    for match in re.finditer(r'"text"\s*:\s*(\[[^\]]*\])', html):
        try:
            parsed = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, list):
            counts.append(sum(1 for value in parsed if str(value or "").strip()))
    return max(counts) if counts else None


def parse_plot_data_traces(html: str) -> list[dict[str, Any]]:
    """Распарсить data-array Plotly из fallback payload."""
    start = html.find("[")
    if start < 0:
        return []
    segment = extract_balanced_segment(html, start, "[", "]")
    try:
        parsed = json.loads(segment)
    except json.JSONDecodeError:
        return []
    if not isinstance(parsed, list):
        return []
    return [item for item in parsed if isinstance(item, dict)]


def extract_string_array_values(html: str, key: str) -> list[str]:
    """Извлечь строковые значения из JSON-массивов Plotly по ключу."""
    values: list[str] = []
    for match in re.finditer(rf'"{re.escape(key)}"\s*:\s*(\[[^\]]*\])', html):
        try:
            parsed = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, list):
            values.extend(str(item) for item in parsed if item is not None)
    return values


def extract_numeric_array_values(html: str, key: str) -> list[float]:
    """Извлечь числовые значения из JSON-массивов Plotly по ключу."""
    values: list[float] = []
    for match in re.finditer(rf'"{re.escape(key)}"\s*:\s*(\[[^\]]*\])', html):
        try:
            parsed = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        if not isinstance(parsed, list):
            continue
        for item in parsed:
            try:
                values.append(float(item))
            except (TypeError, ValueError):
                continue
    return values


def clean_json_text(value: str) -> str:
    """Очистить JSON/HTML текст."""
    try:
        return json.loads(f'"{value}"')
    except json.JSONDecodeError:
        return re.sub(r"<[^>]+>", "", value).strip()


def build_run_id(args: argparse.Namespace) -> str:
    """Сформировать run_id отчета visual regression."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    parts = ["visual_regression", timestamp]
    if args.period_type and args.aggregation_mode and args.report_date and args.retrospective_years is not None:
        parts.extend([args.period_type, args.aggregation_mode, args.report_date, f"r{args.retrospective_years}"])
    return "_".join(parts)


def render_report(
    args: argparse.Namespace,
    backend_status: dict[str, str],
    checks: Sequence[VisualCheck],
    html_files: Sequence[Path],
    screenshot_artifacts: Sequence[ScreenshotArtifact],
) -> str:
    """Сформировать Markdown-отчет visual regression."""
    counts = {
        "ok": sum(check.status == "ok" for check in checks),
        "warning": sum(check.status == "warning" for check in checks),
        "fail": sum(check.status == "fail" for check in checks),
    }
    lines = [
        "# Visual regression report",
        "",
        "Метка: `вторая модернизация`.",
        "",
        "## Режим",
        "",
        f"- Screenshot/backend mode: `{backend_status['mode']}`",
        f"- Комментарий: {backend_status['message']}",
        f"- HTML-файлов в проверке: `{len(html_files)}`",
        f"- `report_date`: `{args.report_date}`",
        f"- `period_type`: `{args.period_type}`",
        f"- `aggregation_mode`: `{args.aggregation_mode}`",
        f"- `retrospective_years`: `{args.retrospective_years}`",
        "",
        "## Сводка",
        "",
        f"- OK: `{counts['ok']}`",
        f"- Warnings: `{counts['warning']}`",
        f"- Failures: `{counts['fail']}`",
        "",
        "## Проверки",
        "",
        "| Файл | Проверка | Статус | Сообщение |",
        "| --- | --- | --- | --- |",
    ]
    for check in checks:
        lines.append(
            f"| `{check.file}` | `{check.check}` | `{check.status}` | {escape_table_text(check.message)} |"
        )
    lines.extend(
        [
            "",
            "## Screenshots",
            "",
            f"Папка для скриншотов: `{VISUAL_REGRESSION_SCREENSHOTS_DIR.relative_to(config.PROJECT_ROOT).as_posix()}`.",
            "Если screenshot backend недоступен, папка создается, но изображения не формируются.",
            "",
            "## Ограничения",
            "",
            "- Fallback static HTML inspection проверяет структуру Plotly/HTML, но не заменяет визуальный просмотр графика.",
            "- Проверка наложения подписей без screenshot backend является эвристической.",
            "- Полноценное сравнение контрольных зон будет доступно после подключения screenshot backend.",
        ]
    )
    lines.extend(
        [
            "",
            "## Screenshot artifacts",
            "",
            f"- Screenshot artifacts count: `{len(screenshot_artifacts)}`",
            f"- Screenshot manifest directory: `{VISUAL_REGRESSION_REPORTS_DIR.relative_to(config.PROJECT_ROOT).as_posix()}`",
            f"- Diff report directory: `{VISUAL_REGRESSION_DIFFS_DIR.relative_to(config.PROJECT_ROOT).as_posix()}`",
            "",
            "| HTML | Screenshot | Baseline status | SHA256 |",
            "| --- | --- | --- | --- |",
        ]
    )
    for artifact in screenshot_artifacts:
        lines.append(
            f"| `{artifact.html_file}` | `{artifact.screenshot_file}` | `{artifact.baseline_status}` | `{artifact.sha256}` |"
        )
    lines.extend(
        [
            "",
            "Screenshot PNG, manifest and diff report files are generated outputs and must not be committed.",
            "If baseline screenshots are absent, the diff report records `missing_baseline` instead of failing the run.",
        ]
    )
    return "\n".join(lines)


def escape_table_text(value: str) -> str:
    """Экранировать Markdown table text."""
    return value.replace("|", "\\|").replace("\n", "<br>")


if __name__ == "__main__":
    raise SystemExit(main())
