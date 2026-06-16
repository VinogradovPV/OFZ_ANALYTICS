"""Smoke tests готовности OFZ_ANALITICS pipeline.

По умолчанию скрипт выполняет быстрые проверки артефактов и компиляции. Полный
запуск pipeline включается явно через `--run-pipeline`, чтобы smoke tests не
перезаписывали outputs неожиданно.
"""

from __future__ import annotations

import argparse
import py_compile
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Callable, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, report_params
else:
    from . import config, report_params


KEY_SCRIPTS = [
    "run_pipeline.py",
    "report_params.py",
    "period_filter.py",
    "03_feature_engineering.py",
    "06_build_charts.py",
    "07_dashboard_exports.py",
    "08_analytical_tables.py",
    "09_monthly_analytics.py",
    "10_build_monthly_charts.py",
    "interactive_pipeline.py",
    "maintenance/cleanup_outputs.py",
    "schema_validation.py",
    "regression_tests.py",
    "raw_data_registry.py",
]


@dataclass(frozen=True)
class SmokeResult:
    """Результат одной smoke-проверки."""

    name: str
    passed: bool
    message: str


def main(argv: Sequence[str] | None = None) -> int:
    """Запустить smoke tests."""
    args = parse_args(argv)
    report_date = date.fromisoformat(args.report_date)
    report_params.validate_retrospective_years(args.retrospective_years)
    retrospective_years = args.retrospective_years
    period_type = report_params.normalize_period_type(args.period_type)
    aggregation_mode = report_params.normalize_aggregation_mode(args.aggregation_mode)
    report_params.validate_report_date(report_date)
    report_params.validate_period_constraints(report_date, period_type, aggregation_mode)
    params = report_params.ReportParams(
        report_date=report_date,
        retrospective_years=retrospective_years,
        period_type=period_type,
        aggregation_mode=aggregation_mode,
        periods=report_params.build_report_periods(
            report_date=report_date,
            retrospective_years=retrospective_years,
            period_type=period_type,
            aggregation_mode=aggregation_mode,
        ),
    )

    checks: list[tuple[str, Callable[[], None]]] = [
        ("py_compile_key_scripts", validate_py_compile_key_scripts),
        ("pipeline_command_contract", lambda: validate_pipeline_command_contract(args)),
        ("interactive_cleanup_contract", validate_interactive_cleanup_contract),
        ("analytical_tables_exist", validate_analytical_tables_exist),
        ("charts_exist", validate_charts_exist),
        ("monthly_outputs_exist", validate_monthly_outputs_exist),
        ("dashboard_exports_exist", validate_dashboard_exports_exist),
        ("outputs_structure", validate_outputs_structure),
        ("no_xlsx_directly_in_outputs_exports", validate_no_xlsx_directly_in_outputs_exports),
    ]
    if args.run_pipeline:
        checks.insert(2, ("pipeline_runtime", lambda: run_pipeline(params)))

    results: list[SmokeResult] = []
    for name, check in checks:
        try:
            check()
        except AssertionError as exc:
            results.append(SmokeResult(name, False, str(exc)))
        except Exception as exc:  # pragma: no cover - нужен текст диагностики при ручном запуске.
            results.append(SmokeResult(name, False, f"Неожиданная ошибка: {exc}"))
        else:
            results.append(SmokeResult(name, True, "ok"))

    for result in results:
        status = "OK" if result.passed else "FAIL"
        print(f"{status} | {result.name} | {result.message}")

    failed = [result for result in results if not result.passed]
    if failed:
        print(f"Smoke tests failed: {len(failed)}")
        return 1
    print(f"Smoke tests passed: {len(results)}")
    return 0


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    """Разобрать параметры smoke tests."""
    parser = argparse.ArgumentParser(description="Smoke tests OFZ_ANALITICS.")
    parser.add_argument("--report-date", default="2026-05-01")
    parser.add_argument("--retrospective-years", type=int, default=4)
    parser.add_argument("--period-type", choices=["month", "quarter", "year"], default="month")
    parser.add_argument("--aggregation-mode", choices=["cumulative", "point"], default="cumulative")
    parser.add_argument(
        "--run-pipeline",
        action="store_true",
        help="Фактически запустить scripts/run_pipeline.py --all перед проверкой outputs.",
    )
    return parser.parse_args(argv)


def validate_py_compile_key_scripts() -> None:
    """Проверить компиляцию ключевых Python-скриптов."""
    errors: list[str] = []
    for script_name in KEY_SCRIPTS:
        path = config.PROJECT_ROOT / "scripts" / script_name
        if not path.exists():
            errors.append(f"{script_name}: файл отсутствует")
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"{script_name}: {exc.msg}")
    assert not errors, "; ".join(errors)


def validate_pipeline_command_contract(args: argparse.Namespace) -> None:
    """Проверить, что команда полного pipeline может быть сформирована."""
    command = pipeline_command(
        report_date=args.report_date,
        retrospective_years=args.retrospective_years,
        period_type=args.period_type,
        aggregation_mode=args.aggregation_mode,
    )
    assert command[0].endswith("python.exe") or command[0] == sys.executable, "Команда должна запускаться проектным Python."
    assert "scripts/run_pipeline.py" in command, "Команда должна запускать scripts/run_pipeline.py."
    assert "--all" in command, "Команда полного pipeline должна содержать --all."


def validate_interactive_cleanup_contract() -> None:
    """Проверить, что interactive launcher использует безопасный cleanup pre-flight."""
    launcher = config.PROJECT_ROOT / "scripts" / "interactive_pipeline.py"
    cleanup = config.PROJECT_ROOT / "scripts" / "maintenance" / "cleanup_outputs.py"
    assert launcher.exists(), "Не найден scripts/interactive_pipeline.py."
    assert cleanup.exists(), "Не найден scripts/maintenance/cleanup_outputs.py."
    text = launcher.read_text(encoding="utf-8")
    required = [
        "run_cleanup_preflight",
        "scripts/maintenance/cleanup_outputs.py",
        "DELETE_OUTPUTS_NO_ARCHIVE",
        "OFZ_INTERACTIVE_CLEANUP_STATUS",
    ]
    missing = [item for item in required if item not in text]
    assert not missing, "В interactive launcher отсутствуют cleanup-маркеры: " + ", ".join(missing)


def run_pipeline(params: report_params.ReportParams) -> None:
    """Запустить полный pipeline для smoke-проверки."""
    command = pipeline_command(
        report_date=params.report_date.isoformat(),
        retrospective_years=params.retrospective_years,
        period_type=params.period_type,
        aggregation_mode=params.aggregation_mode,
    )
    completed = subprocess.run(command, cwd=config.PROJECT_ROOT, check=False)
    assert completed.returncode == 0, f"Pipeline завершился с кодом {completed.returncode}."


def pipeline_command(
    report_date: str,
    retrospective_years: int,
    period_type: str,
    aggregation_mode: str,
) -> list[str]:
    """Сформировать команду полного запуска pipeline без абсолютного пути в документации."""
    return [
        str(config.PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"),
        "scripts/run_pipeline.py",
        "--all",
        "--report-date",
        report_date,
        "--retrospective-years",
        str(retrospective_years),
        "--period-type",
        period_type,
        "--aggregation-mode",
        aggregation_mode,
    ]


def validate_analytical_tables_exist() -> None:
    """Проверить наличие аналитических таблиц."""
    xlsx_files = list(config.REPORTS_ANALYTICAL_TABLES_DIR.glob("*.xlsx")) if config.REPORTS_ANALYTICAL_TABLES_DIR.exists() else []
    csv_files = list(config.EXPORTS_ANALYTICAL_CSV_DIR.glob("*.csv")) if config.EXPORTS_ANALYTICAL_CSV_DIR.exists() else []
    assert xlsx_files, "Не найдены XLSX аналитические таблицы в outputs/reports/analytical_tables/."
    assert csv_files, "Не найдены CSV аналитические таблицы в outputs/exports/analytical_csv/."


def validate_charts_exist() -> None:
    """Проверить наличие HTML-графиков."""
    charts = list(config.CHARTS_DIR.rglob("*.html")) if config.CHARTS_DIR.exists() else []
    assert charts, "Не найдены HTML-графики в outputs/charts/."


def validate_monthly_outputs_exist() -> None:
    """Проверить наличие monthly outputs."""
    processed = config.PROCESSED_DATA_DIR / "ofz_monthly_metrics.csv"
    monthly_reports = list(config.REPORTS_MONTHLY_TABLES_DIR.glob("monthly_metrics_*.xlsx")) if config.REPORTS_MONTHLY_TABLES_DIR.exists() else []
    monthly_csv = list(config.EXPORTS_ANALYTICAL_CSV_DIR.glob("monthly_metrics_*.csv")) if config.EXPORTS_ANALYTICAL_CSV_DIR.exists() else []
    monthly_charts = list(config.CHARTS_DIR.rglob("monthly_*.html")) if config.CHARTS_DIR.exists() else []
    assert processed.exists(), "Не найден data/processed/ofz_monthly_metrics.csv."
    assert monthly_reports, "Не найдены monthly XLSX reports в outputs/reports/monthly_tables/."
    assert monthly_csv, "Не найдены monthly CSV exports в outputs/exports/analytical_csv/."
    assert monthly_charts, "Не найдены monthly charts в outputs/charts/."


def validate_dashboard_exports_exist() -> None:
    """Проверить наличие dashboard exports."""
    dashboard_files = list(config.DASHBOARDS_DIR.rglob("dashboard_*")) if config.DASHBOARDS_DIR.exists() else []
    assert dashboard_files, "Не найдены dashboard exports в outputs/dashboards/."


def validate_outputs_structure() -> None:
    """Проверить новую структуру outputs."""
    required = [
        config.REPORTS_ANALYTICAL_TABLES_DIR,
        config.REPORTS_MONTHLY_TABLES_DIR,
        config.EXPORTS_ANALYTICAL_CSV_DIR,
        config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR,
        config.EXPORTS_CHART_DATA_SANKEY_DIR,
        config.EXPORTS_CHART_DATA_BOXPLOT_DIR,
        config.EXPORTS_CHART_DATA_STRUCTURE_DIR,
        config.DASHBOARDS_DIR,
    ]
    missing = [path.relative_to(config.PROJECT_ROOT).as_posix() for path in required if not path.exists()]
    assert not missing, f"Отсутствуют директории outputs: {', '.join(missing)}."


def validate_no_xlsx_directly_in_outputs_exports() -> None:
    """Проверить отсутствие XLSX напрямую в outputs/exports/."""
    if not config.EXPORTS_DIR.exists():
        return
    xlsx_files = sorted(path.name for path in config.EXPORTS_DIR.glob("*.xlsx"))
    assert not xlsx_files, f"XLSX не должны лежать напрямую в outputs/exports/: {', '.join(xlsx_files)}."


if __name__ == "__main__":
    raise SystemExit(main())
