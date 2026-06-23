"""Единый quality gate второй модернизации OFZ_ANALITICS.

Скрипт запускает доступные проверки проекта и формирует единый отчет. Если
опциональная проверка еще не реализована, quality gate фиксирует warning и
продолжает остальные проверки.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import py_compile
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Callable, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, console_encoding, report_params, utils
else:
    from . import config, console_encoding, report_params, utils


QUALITY_GATE_REPORT_DOC = config.get_doc_path("quality_gate_report.md")

KEY_SCRIPTS = (
    "run_pipeline.py",
    "report_params.py",
    "period_filter.py",
    "01_data_audit.py",
    "02_data_cleaning.py",
    "03_feature_engineering.py",
    "04_kpi_map.py",
    "05_visualization_strategy.py",
    "06_build_charts.py",
    "07_dashboard_exports.py",
    "08_analytical_tables.py",
    "09_monthly_analytics.py",
    "10_build_monthly_charts.py",
    "generate_executive_summary.py",
    "html_chart_qa.py",
    "visual_regression.py",
    "schema_validation.py",
    "regression_tests.py",
    "smoke_tests.py",
    "run_manifest.py",
    "raw_data_registry.py",
    "palette.py",
    "scatter_chart_policy.py",
)


def subprocess_utf8_env() -> dict[str, str]:
    """Return environment forcing UTF-8 for nested Python quality scripts."""
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


@dataclass(frozen=True)
class GateResult:
    """Результат одной проверки quality gate."""

    name: str
    status: str
    message: str
    command: str = ""


@dataclass(frozen=True)
class GateContext:
    """Параметры запуска quality gate."""

    mode: str
    report_date: date
    retrospective_years: int
    period_type: str
    aggregation_mode: str
    run_id: str


def main(argv: Sequence[str] | None = None) -> int:
    """Запустить quality gate и записать отчеты."""
    console_encoding.configure_utf8_stdio()
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    args = parse_args(argv)
    context = build_context(args)
    logger.info("Старт quality gate: mode=%s run_id=%s", context.mode, context.run_id)

    config.ensure_output_directories()
    results = run_checks(context)
    paths = write_reports(context, results)

    for result in results:
        print(f"{result.status.upper()} | {result.name} | {result.message}")
    print(paths["docs_report"].relative_to(config.PROJECT_ROOT).as_posix())

    failed = [result for result in results if result.status == "fail"]
    return 1 if failed else 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Разобрать CLI-параметры quality gate."""
    parser = argparse.ArgumentParser(description="Единый quality gate проекта OFZ_ANALITICS.")
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--fast", action="store_true", help="Быстрые проверки без тяжелых сценариев.")
    mode_group.add_argument("--full", action="store_true", help="Полный набор доступных проверок.")
    mode_group.add_argument(
        "--stage",
        choices=["encoding-mojibake"],
        help="Запустить отдельный quality stage.",
    )
    parser.add_argument("--report-date", default="2026-05-01", help="Отчетная дата YYYY-MM-DD.")
    parser.add_argument("--retrospective-years", type=int, default=4, help="Количество лет ретроспективы.")
    parser.add_argument("--period-type", choices=sorted(report_params.ALLOWED_PERIOD_TYPES), default="month", help="Тип периода.")
    parser.add_argument(
        "--aggregation-mode",
        choices=sorted(report_params.ALLOWED_AGGREGATION_MODES),
        default="cumulative",
        help="Режим агрегации.",
    )
    return parser.parse_args(argv)


def build_context(args: argparse.Namespace) -> GateContext:
    """Проверить параметры отчета и создать контекст quality gate."""
    report_date = date.fromisoformat(args.report_date)
    period_type = report_params.normalize_period_type(args.period_type)
    aggregation_mode = report_params.normalize_aggregation_mode(args.aggregation_mode)
    report_params.validate_report_date(report_date)
    report_params.validate_period_constraints(report_date, period_type, aggregation_mode)
    report_params.validate_retrospective_years(args.retrospective_years)
    mode = args.stage or ("full" if args.full else "fast")
    run_id = build_run_id(mode, report_date, period_type, aggregation_mode, args.retrospective_years)
    return GateContext(
        mode=mode,
        report_date=report_date,
        retrospective_years=args.retrospective_years,
        period_type=period_type,
        aggregation_mode=aggregation_mode,
        run_id=run_id,
    )


def run_checks(context: GateContext) -> list[GateResult]:
    """Выполнить набор проверок quality gate."""
    if context.mode == "encoding-mojibake":
        return [check_encoding_mojibake(context)]

    checks: list[tuple[str, Callable[[GateContext], GateResult]]] = [
        ("encoding-mojibake", check_encoding_mojibake),
        ("py_compile_key_scripts", check_py_compile_key_scripts),
        ("schema_validation", lambda ctx: run_required_script(ctx, "schema_validation.py", report_args(ctx))),
        ("regression_tests", lambda ctx: run_required_script(ctx, "regression_tests.py", [])),
        ("smoke_tests", lambda ctx: run_required_script(ctx, "smoke_tests.py", report_args(ctx))),
        ("html_chart_qa", lambda ctx: run_required_script(ctx, "html_chart_qa.py", report_args(ctx))),
        ("visual_regression", lambda ctx: run_required_script(ctx, "visual_regression.py", report_args(ctx))),
        ("readme_contract", check_readme_contract),
        ("outputs_structure", check_outputs_structure),
        ("docs_structure", check_docs_structure),
        ("charts_structure", check_charts_structure),
        ("yield_vs_discount_outputs", check_yield_vs_discount_outputs),
        ("scripts_structure", check_scripts_structure),
        ("run_manifest", check_run_manifest),
        ("dashboard_semantic_model", check_dashboard_semantic_model),
    ]
    if context.mode == "full":
        checks.insert(3, ("anomaly_tests", lambda ctx: run_optional_script(ctx, "anomaly_tests.py", [])))

    results: list[GateResult] = []
    for _name, check in checks:
        try:
            results.append(check(context))
        except Exception as exc:  # pragma: no cover - нужен полный отчет при ручном запуске.
            results.append(GateResult(getattr(check, "__name__", "unknown_check"), "fail", f"Неожиданная ошибка: {exc}"))
    return results


def check_encoding_mojibake(_context: GateContext) -> GateResult:
    """Проверить исходные текстовые файлы на UTF-8 и mojibake."""
    relative_path = Path("scripts/qa/check_text_encoding.py")
    script_path = config.PROJECT_ROOT / relative_path
    command = [sys.executable, str(script_path)]
    command_text = ".\\.venv\\Scripts\\python.exe scripts\\qa\\check_text_encoding.py"
    if not script_path.exists():
        return GateResult("encoding-mojibake", "fail", f"Обязательный скрипт отсутствует: {relative_path}", command_text)
    result = subprocess.run(
        command,
        cwd=config.PROJECT_ROOT,
        env=subprocess_utf8_env(),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    output = compact_output(result.stdout, result.stderr)
    status = "ok" if result.returncode == 0 else "fail"
    return GateResult("encoding-mojibake", status, output or f"Код завершения: {result.returncode}", command_text)


def check_py_compile_key_scripts(_context: GateContext) -> GateResult:
    """Проверить py_compile ключевых scripts."""
    errors: list[str] = []
    missing: list[str] = []
    for script_name in KEY_SCRIPTS:
        path = config.PROJECT_ROOT / "scripts" / script_name
        if not path.exists():
            missing.append(script_name)
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"{script_name}: {exc.msg}")
    if errors:
        return GateResult("py_compile_key_scripts", "fail", "; ".join(errors))
    if missing:
        return GateResult("py_compile_key_scripts", "warning", "Отсутствуют scripts: " + ", ".join(missing))
    return GateResult("py_compile_key_scripts", "ok", f"Проверено scripts: {len(KEY_SCRIPTS)}.")


def run_required_script(context: GateContext, script_name: str, args: Sequence[str]) -> GateResult:
    """Запустить обязательный проверочный скрипт."""
    script_path = config.PROJECT_ROOT / "scripts" / script_name
    command = [sys.executable, str(script_path), *args]
    command_text = command_for_report(script_name, args)
    if not script_path.exists():
        return GateResult(script_name, "fail", f"Обязательный скрипт отсутствует: scripts/{script_name}", command_text)
    result = subprocess.run(
        command,
        cwd=config.PROJECT_ROOT,
        env=subprocess_utf8_env(),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    output = compact_output(result.stdout, result.stderr)
    status = "ok" if result.returncode == 0 else "fail"
    message = output or f"Код завершения: {result.returncode}"
    return GateResult(script_name, status, message, command_text)


def run_optional_script(context: GateContext, script_name: str, args: Sequence[str]) -> GateResult:
    """Запустить опциональный проверочный скрипт или вернуть warning."""
    script_path = config.PROJECT_ROOT / "scripts" / script_name
    command_text = command_for_report(script_name, args)
    if not script_path.exists():
        return GateResult(script_name, "warning", f"Опциональный скрипт отсутствует: scripts/{script_name}", command_text)
    return run_required_script(context, script_name, args)


def check_readme_contract(_context: GateContext) -> GateResult:
    """Проверить базовый контракт README."""
    path = config.PROJECT_ROOT / "README.md"
    if not path.exists():
        return GateResult("readme_contract", "fail", "README.md отсутствует.")
    text = path.read_text(encoding="utf-8", errors="replace")
    issues: list[str] = []
    if ".\\.venv\\Scripts\\python.exe" not in text:
        issues.append("нет команд через .\\.venv\\Scripts\\python.exe")
    absolute_path_pattern = "C:" + "\\\\" + "Users" + "\\\\" + "|" + "LLM" + "_CHAT" + "\\\\"
    if re.search(absolute_path_pattern, text, flags=re.IGNORECASE):
        issues.append("найден абсолютный пользовательский путь")
    required_terms = [
        ("aggregation-mode",),
        ("cumulative",),
        ("point",),
        ("outputs",),
        ("quality", "качест"),
        ("ограничения",),
    ]
    text_lower = text.lower()
    missing_terms = ["/".join(term_group) for term_group in required_terms if not any(term.lower() in text_lower for term in term_group)]
    if missing_terms:
        issues.append("не найдены термины: " + ", ".join(missing_terms))
    if issues:
        return GateResult("readme_contract", "fail", "; ".join(issues))
    return GateResult("readme_contract", "ok", "README содержит локальные команды и ключевые разделы.")


def check_outputs_structure(_context: GateContext) -> GateResult:
    """Проверить целевую структуру outputs."""
    required_dirs = [
        config.REPORTS_ANALYTICAL_TABLES_DIR,
        config.REPORTS_MONTHLY_TABLES_DIR,
        config.EXPORTS_ANALYTICAL_CSV_DIR,
        config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR,
        config.EXPORTS_CHART_DATA_SANKEY_DIR,
        config.EXPORTS_CHART_DATA_BOXPLOT_DIR,
        config.EXPORTS_CHART_DATA_SCATTER_DIR,
        config.EXPORTS_CHART_DATA_STRUCTURE_DIR,
        config.DASHBOARDS_DIR,
    ]
    missing = [path.relative_to(config.PROJECT_ROOT).as_posix() for path in required_dirs if not path.exists()]
    allowed_skeleton_files = {".gitkeep", "README.md", "index.md"}
    direct_files = (
        [
            path.name
            for path in config.EXPORTS_DIR.glob("*")
            if path.is_file() and path.name not in allowed_skeleton_files
        ]
        if config.EXPORTS_DIR.exists()
        else []
    )
    if missing or direct_files:
        parts = []
        if missing:
            parts.append("нет папок: " + ", ".join(missing))
        if direct_files:
            parts.append("файлы напрямую в outputs/exports: " + ", ".join(direct_files))
        return GateResult("outputs_structure", "fail", "; ".join(parts))
    return GateResult("outputs_structure", "ok", "Структура outputs соответствует контракту.")


def check_docs_structure(_context: GateContext) -> GateResult:
    """Проверить тематическую структуру docs/ и ключевые карты реорганизации."""
    required_dirs = [
        config.DOCS_PROJECT_DIR,
        config.DOCS_METHODOLOGY_DIR,
        config.DOCS_DATA_PIPELINE_DIR,
        config.DOCS_ANALYTICS_DIR,
        config.DOCS_VISUALIZATION_DIR,
        config.DOCS_DASHBOARD_DIR,
        config.DOCS_QUALITY_DIR,
        config.DOCS_ARCHIVE_DIR,
    ]
    required_files = [
        config.DOCS_DIR / "index.md",
        config.DOCS_PROJECT_DIR / "docs_inventory_before_cleanup.md",
        config.DOCS_PROJECT_DIR / "docs_cleanup_apply_decision.md",
        config.get_doc_path("scripts_structure_plan.md"),
        config.get_doc_path("scripts_migration_plan.md"),
    ]
    missing_dirs = [path.relative_to(config.PROJECT_ROOT).as_posix() for path in required_dirs if not path.exists()]
    missing_files = [path.relative_to(config.PROJECT_ROOT).as_posix() for path in required_files if not path.exists()]
    root_md = sorted(path.name for path in config.DOCS_DIR.glob("*.md") if path.name != "index.md")
    if missing_dirs or missing_files or root_md:
        parts: list[str] = []
        if missing_dirs:
            parts.append("нет папок: " + ", ".join(missing_dirs))
        if missing_files:
            parts.append("нет файлов: " + ", ".join(missing_files))
        if root_md:
            parts.append("markdown в корне docs/: " + ", ".join(root_md))
        return GateResult("docs_structure", "fail", "; ".join(parts))
    return GateResult("docs_structure", "ok", "Корень docs/ чистый; индекс, отчеты реорганизации и планы scripts найдены.")


def check_charts_structure(_context: GateContext) -> GateResult:
    """Проверить тематическую структуру outputs/charts/."""
    required_dirs = [
        config.CHARTS_MONTHLY_DIR,
        config.CHARTS_RISK_DIR,
        config.CHARTS_SCATTER_DIR,
        config.CHARTS_SCATTER_YIELD_DISCOUNT_DIR,
        config.CHARTS_YIELD_DIR,
        config.CHARTS_SANKEY_DIR,
        config.CHARTS_STRUCTURE_DIR,
        config.CHARTS_REVENUE_DIR,
    ]
    required_files = [
        config.DOCS_PROJECT_DIR / "outputs_structure.md",
    ]
    missing_dirs = [path.relative_to(config.PROJECT_ROOT).as_posix() for path in required_dirs if not path.exists()]
    missing_files = [path.relative_to(config.PROJECT_ROOT).as_posix() for path in required_files if not path.exists()]
    root_html = sorted(
        path.name
        for path in config.CHARTS_DIR.glob("*.html")
        if not path.name.startswith(("_", "."))
    )
    if missing_dirs or missing_files or root_html:
        parts: list[str] = []
        if missing_dirs:
            parts.append("нет папок: " + ", ".join(missing_dirs))
        if missing_files:
            parts.append("нет файлов: " + ", ".join(missing_files))
        if root_html:
            parts.append("HTML в корне outputs/charts/: " + ", ".join(root_html))
        return GateResult("charts_structure", "fail", "; ".join(parts))
    return GateResult(
        "charts_structure",
        "ok",
        "Ключевые generated-категории outputs/charts/ и source-карта docs/00_project/outputs_structure.md найдены; HTML в корне нет.",
    )


def check_yield_vs_discount_outputs(context: GateContext) -> GateResult:
    """Проверить наличие yield_vs_discount HTML и chart data для текущего запуска."""
    suffix = output_suffix(context)
    required_files = [
        config.CHARTS_SCATTER_YIELD_DISCOUNT_DIR / f"yield_vs_discount_{suffix}.html",
        config.CHARTS_SCATTER_YIELD_DISCOUNT_DIR / f"yield_vs_discount_facet_{suffix}.html",
        config.CHARTS_SCATTER_YIELD_DISCOUNT_DIR / f"yield_vs_discount_outliers_{suffix}.html",
        config.EXPORTS_CHART_DATA_SCATTER_DIR / f"yield_vs_discount_{suffix}.csv",
        config.EXPORTS_CHART_DATA_SCATTER_DIR / f"yield_vs_discount_facet_{suffix}.csv",
        config.EXPORTS_CHART_DATA_SCATTER_DIR / f"yield_vs_discount_outliers_{suffix}.csv",
    ]
    missing = [path.relative_to(config.PROJECT_ROOT).as_posix() for path in required_files if not path.exists()]
    if missing:
        return GateResult("yield_vs_discount_outputs", "fail", "нет файлов: " + ", ".join(missing))
    return GateResult(
        "yield_vs_discount_outputs",
        "ok",
        "Найдены yield_vs_discount main/facet/outliers и CSV-основы.",
    )


def check_scripts_structure(_context: GateContext) -> GateResult:
    """Проверить наличие документации по структуре scripts/."""
    required_files = [
        config.PROJECT_ROOT / "scripts" / "README.md",
        config.get_doc_path("scripts_structure_plan.md"),
        config.get_doc_path("scripts_migration_plan.md"),
    ]
    missing = [path.relative_to(config.PROJECT_ROOT).as_posix() for path in required_files if not path.exists()]
    if missing:
        return GateResult("scripts_structure", "fail", "нет файлов: " + ", ".join(missing))
    return GateResult("scripts_structure", "ok", "scripts/README.md и планы структуры scripts найдены.")


def check_run_manifest(_context: GateContext) -> GateResult:
    """Проверить наличие run manifest."""
    script_path = config.PROJECT_ROOT / "scripts" / "run_manifest.py"
    latest_path = config.PROCESSED_DATA_DIR / "run_manifest_latest.json"
    report_path = config.get_doc_path("run_manifest_report.md")
    issues: list[str] = []
    if not script_path.exists():
        issues.append("scripts/run_manifest.py отсутствует")
    if not report_path.exists():
        issues.append(f"{report_path.relative_to(config.PROJECT_ROOT).as_posix()} отсутствует")
    if not latest_path.exists():
        issues.append("latest manifest еще не создан")
    if issues:
        return GateResult("run_manifest", "warning", "; ".join(issues))
    try:
        data = json.loads(latest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return GateResult("run_manifest", "fail", f"run_manifest_latest.json не является JSON: {exc}")
    required = {"run_id", "timestamp", "report_date", "period_type", "aggregation_mode", "outputs"}
    missing = required.difference(data)
    if missing:
        return GateResult("run_manifest", "fail", "В manifest отсутствуют поля: " + ", ".join(sorted(missing)))
    return GateResult("run_manifest", "ok", f"Latest manifest найден: {data.get('run_id')}.")


def check_dashboard_semantic_model(_context: GateContext) -> GateResult:
    """Проверить dashboard semantic model первого поколения и готовность к v2."""
    v1_dir = config.DASHBOARDS_SEMANTIC_LAYER_DIR
    v2_dir = config.DASHBOARDS_DIR / "semantic_model_v2"
    if v2_dir.exists():
        required = ["field_dictionary.csv", "kpi_dictionary.csv", "measures.csv", "model_manifest.json"]
        missing = [name for name in required if not (v2_dir / name).exists()]
        if missing:
            return GateResult("dashboard_semantic_model", "warning", "Semantic model v2 неполный: " + ", ".join(missing))
        required_columns = {
            "semantic_version",
            "technical_name",
            "display_name_ru",
            "unit",
            "data_type",
            "calculation_rule",
            "source_table",
            "source_column",
            "limitations",
            "applicable_period_types",
            "applicable_aggregation_modes",
        }
        column_warnings = []
        for csv_name in ("field_dictionary.csv", "kpi_dictionary.csv", "measures.csv"):
            with (v2_dir / csv_name).open("r", encoding="utf-8-sig", newline="") as file:
                reader = csv.reader(file)
                header = next(reader, [])
            missing_columns = sorted(required_columns.difference(header))
            if missing_columns:
                column_warnings.append(f"{csv_name}: " + ", ".join(missing_columns))
        try:
            manifest = json.loads((v2_dir / "model_manifest.json").read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return GateResult("dashboard_semantic_model", "warning", f"Semantic model v2 manifest невалиден: {exc}")
        if column_warnings:
            return GateResult(
                "dashboard_semantic_model",
                "warning",
                "Semantic model v2 не прошел контроль колонок: " + "; ".join(column_warnings),
            )
        version = manifest.get("semantic_version", "unknown")
        return GateResult("dashboard_semantic_model", "ok", f"Semantic model v2 найден: version={version}.")
    if v1_dir.exists() and any(v1_dir.glob("*")):
        return GateResult(
            "dashboard_semantic_model",
            "warning",
            "Найден semantic layer первого поколения; semantic model v2 еще не создан.",
        )
    return GateResult("dashboard_semantic_model", "warning", "Dashboard semantic model не найден.")


def report_args(context: GateContext) -> list[str]:
    """CLI-аргументы отчетного периода для downstream-проверок."""
    return [
        "--report-date",
        context.report_date.isoformat(),
        "--retrospective-years",
        str(context.retrospective_years),
        "--period-type",
        context.period_type,
        "--aggregation-mode",
        context.aggregation_mode,
    ]


def output_suffix(context: GateContext) -> str:
    """Сформировать suffix outputs для проверки артефактов конкретного запуска."""
    return (
        f"{context.period_type}_{context.aggregation_mode}_{context.report_date.isoformat()}_"
        f"retrospective_{context.retrospective_years}"
    )


def command_for_report(script_name: str, args: Sequence[str]) -> str:
    """Сформировать переносимую команду для отчета."""
    return " ".join([".\\.venv\\Scripts\\python.exe", f"scripts\\{script_name}", *args])


def compact_output(stdout: str, stderr: str, limit: int = 1200) -> str:
    """Сжать stdout/stderr для Markdown-отчета."""
    text = "\n".join(part.strip() for part in (stdout, stderr) if part and part.strip())
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        return text[:limit].rstrip() + " ..."
    return text


def build_run_id(mode: str, report_date: date, period_type: str, aggregation_mode: str, retrospective_years: int) -> str:
    """Сформировать run_id для отчета quality gate."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"quality_gate_{mode}_{period_type}_{aggregation_mode}_{report_date.isoformat()}_r{retrospective_years}_{timestamp}"


def write_reports(context: GateContext, results: Sequence[GateResult]) -> dict[str, Path]:
    """Записать docs и outputs reports."""
    markdown = render_report(context, results)
    docs_path = utils.write_markdown(QUALITY_GATE_REPORT_DOC, markdown)
    output_path = config.REPORTS_DIR / f"quality_gate_report_{context.run_id}.md"
    utils.write_markdown(output_path, markdown)
    return {"docs_report": docs_path, "output_report": output_path}


def render_report(context: GateContext, results: Sequence[GateResult]) -> str:
    """Сформировать Markdown-отчет quality gate."""
    counts = {
        "ok": sum(result.status == "ok" for result in results),
        "warning": sum(result.status == "warning" for result in results),
        "fail": sum(result.status == "fail" for result in results),
    }
    lines = [
        "# Quality gate report",
        "",
        "Метка: `вторая модернизация`.",
        "",
        "## Параметры",
        "",
        f"- `run_id`: `{context.run_id}`",
        f"- `mode`: `{context.mode}`",
        f"- `report_date`: `{context.report_date.isoformat()}`",
        f"- `period_type`: `{context.period_type}`",
        f"- `aggregation_mode`: `{context.aggregation_mode}`",
        f"- `retrospective_years`: `{context.retrospective_years}`",
        "",
        "## Сводка",
        "",
        f"- OK: `{counts['ok']}`",
        f"- Warnings: `{counts['warning']}`",
        f"- Failures: `{counts['fail']}`",
        "",
        "## Проверки",
        "",
        "| Проверка | Статус | Сообщение | Команда |",
        "| --- | --- | --- | --- |",
    ]
    for result in results:
        lines.append(
            "| `{name}` | `{status}` | {message} | {command} |".format(
                name=result.name,
                status=result.status,
                message=escape_table_text(result.message),
                command=f"`{result.command}`" if result.command else "-",
            )
        )
    lines.extend(
        [
            "",
            "## Интерпретация",
            "",
            "- `ok` означает успешную проверку.",
            "- `warning` означает, что блок отсутствует, еще не создан или требует ручной проверки, но остальные проверки можно продолжать.",
            "- `fail` означает дефект контракта или неуспешное завершение обязательной проверки.",
            "",
            "## Ограничения",
            "",
            "- Quality gate не изменяет `data/raw/`.",
            "- `html_chart_qa.py` и `visual_regression.py` запускаются в режимах `fast` и `full`.",
            "- Проверка отсутствия повторяющихся facet-осей выполняется через `html_chart_qa.py`.",
            "- В режиме `full` дополнительно запускается опциональный `anomaly_tests.py`, если он уже создан.",
        ]
    )
    return "\n".join(lines)


def escape_table_text(value: str) -> str:
    """Экранировать текст для Markdown-таблицы."""
    return value.replace("|", "\\|").replace("\n", "<br>")


if __name__ == "__main__":
    raise SystemExit(main())

