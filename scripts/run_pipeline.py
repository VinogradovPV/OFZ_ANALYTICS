"""Оркестратор воспроизводимого pipeline аналитики аукционов ОФЗ.

Скрипт запускает только проектные Python-скрипты. Каталог `data/raw/`
используется только как источник чтения и не изменяется этим оркестратором.
"""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, report_params, run_manifest, utils
else:
    from . import config, report_params, run_manifest, utils


REPORT_SCOPE_STAGES = {"5", "8", "8.1", "revenue_analytics", "revenue_charts", "9.1", "monthly_analytics", "monthly_charts"}
SAFE_REPRO_STAGES = {"1", "2", "3"}


@dataclass(frozen=True)
class StageSpec:
    code: str
    name: str
    script: Path | None
    needs_report_params: bool = False
    needs_report_scope: bool = False
    implemented: bool = True
    optional_in_all: bool = False
    output_docs: tuple[Path, ...] = ()


STAGE_SPECS: dict[str, StageSpec] = {
    "1": StageSpec("1", "Этап 1: аудит исходных данных", config.ROOT_DIR / "scripts" / "01_data_audit.py"),
    "2": StageSpec("2", "Этап 2: очистка данных", config.ROOT_DIR / "scripts" / "02_data_cleaning.py"),
    "3": StageSpec("3", "Этап 3: построение признаков", config.ROOT_DIR / "scripts" / "03_feature_engineering.py"),
    "4": StageSpec(
        "4",
        "Этап 4: параметризуемый контур отчета",
        config.ROOT_DIR / "scripts" / "period_filter.py",
        needs_report_params=True,
    ),
    "5": StageSpec(
        "5",
        "Этап 5: карта KPI",
        config.ROOT_DIR / "scripts" / "04_kpi_map.py",
        needs_report_scope=True,
    ),
    "6": StageSpec(
        "6",
        "Этап 6: аналитическая архитектура",
        None,
        output_docs=(config.get_doc_path("analytical_architecture.md"),),
    ),
    "7": StageSpec("7", "Этап 7: стратегия визуализаций", config.ROOT_DIR / "scripts" / "05_visualization_strategy.py"),
    "8": StageSpec(
        "8",
        "Этап 8: построение графиков",
        config.ROOT_DIR / "scripts" / "06_build_charts.py",
        needs_report_params=True,
        needs_report_scope=True,
    ),
    "8.1": StageSpec(
        "8.1",
        "Этап 8.1: обязательные аналитические таблицы",
        config.ROOT_DIR / "scripts" / "08_analytical_tables.py",
        needs_report_params=True,
        needs_report_scope=True,
    ),
    "revenue_analytics": StageSpec(
        "revenue_analytics",
        "Вторая модернизация: revenue analytics",
        config.ROOT_DIR / "scripts" / "11_revenue_analytics.py",
        needs_report_params=True,
        needs_report_scope=True,
        output_docs=(config.get_doc_path("revenue_analytics_report.md"),),
    ),
    "revenue_charts": StageSpec(
        "revenue_charts",
        "Вторая модернизация: revenue charts",
        config.ROOT_DIR / "scripts" / "12_build_revenue_charts.py",
        needs_report_params=True,
        needs_report_scope=True,
        output_docs=(config.get_doc_path("revenue_charts_report.md"),),
    ),
    "monthly_analytics": StageSpec(
        "monthly_analytics",
        "Monthly layer: помесячная аналитика",
        config.ROOT_DIR / "scripts" / "09_monthly_analytics.py",
        needs_report_params=True,
        needs_report_scope=True,
        optional_in_all=True,
    ),
    "monthly_charts": StageSpec(
        "monthly_charts",
        "Monthly layer: помесячные визуализации",
        config.ROOT_DIR / "scripts" / "10_build_monthly_charts.py",
        needs_report_params=True,
        needs_report_scope=True,
        optional_in_all=True,
    ),
    "9": StageSpec(
        "9",
        "Этап 9: архитектура dashboard",
        None,
        output_docs=(config.get_doc_path("dashboard_architecture.md"),),
    ),
    "9.1": StageSpec(
        "9.1",
        "Этап 9.1: dashboard exports",
        config.ROOT_DIR / "scripts" / "07_dashboard_exports.py",
        needs_report_params=True,
        needs_report_scope=True,
    ),
    "semantic_model_v2": StageSpec(
        "semantic_model_v2",
        "Вторая модернизация: semantic model v2",
        config.ROOT_DIR / "scripts" / "build_semantic_model_v2.py",
        output_docs=(config.get_doc_path("dashboard_semantic_model_v2.md"),),
    ),
    "run_manifest": StageSpec(
        "run_manifest",
        "Вторая модернизация: run manifest",
        None,
        needs_report_params=True,
        output_docs=(config.get_doc_path("run_manifest_report.md"), config.DATA_PROCESSED_DIR / "run_manifest_latest.json"),
    ),
    "quality_gate": StageSpec(
        "quality_gate",
        "Вторая модернизация: quality gate",
        config.ROOT_DIR / "scripts" / "quality_gate.py",
        needs_report_params=True,
        output_docs=(config.get_doc_path("quality_gate_report.md"),),
    ),
    "anomaly_tests": StageSpec(
        "anomaly_tests",
        "Вторая модернизация: anomaly tests",
        config.ROOT_DIR / "scripts" / "anomaly_tests.py",
        output_docs=(config.get_doc_path("anomaly_tests_report.md"),),
    ),
    "10": StageSpec(
        "10",
        "Этап 10: executive summary",
        config.ROOT_DIR / "scripts" / "generate_executive_summary.py",
        needs_report_params=True,
        output_docs=(config.get_doc_path("executive_summary_report.md"),),
    ),
    "11": StageSpec(
        "11",
        "Этап 11: self-review",
        None,
        output_docs=(config.get_doc_path("self_review.md"),),
    ),
    "12": StageSpec(
        "12",
        "Этап 12: финальный обзор проекта",
        None,
        output_docs=(config.get_doc_path("final_project_summary.md"),),
    ),
}

ALL_STAGES = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "8.1",
    "revenue_analytics",
    "revenue_charts",
    "monthly_analytics",
    "monthly_charts",
    "9",
    "9.1",
    "semantic_model_v2",
    "10",
    "11",
    "12",
]


@dataclass(frozen=True)
class PipelineArgs:
    stages: list[str]
    all_requested: bool
    safe: bool
    compare: bool
    interactive: bool
    report_date: str | None
    retrospective_years: int | None
    period_type: str | None
    aggregation_mode: str
    params: report_params.ReportParams | None


def main(argv: Sequence[str] | None = None) -> int:
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    try:
        args = parse_args(argv)
        logger.info(
            "Старт run_pipeline: stages=%s safe=%s compare=%s interactive=%s "
            "report_date=%s retrospective_years=%s period_type=%s aggregation_mode=%s",
            args.stages,
            args.safe,
            args.compare,
            args.interactive,
            args.report_date,
            args.retrospective_years,
            args.period_type,
            args.aggregation_mode,
        )
        config.ensure_output_directories()
        verify_raw_directory_is_read_only_source()
        ensure_stage_scripts(args.stages)
        ensure_report_scope_prerequisites(args)

        for stage in args.stages:
            run_stage(stage, args=args, logger=logger)
            validate_stage_output(stage, logger)

        if args.compare or args.safe:
            run_compare(logger=logger)

        write_reproducibility_review(args)
        if args.all_requested:
            write_run_manifest(args, logger)
        logger.info("run_pipeline завершен")
        return 0
    except Exception as exc:
        logger.exception("Pipeline остановлен: %s", exc)
        print(f"Ошибка pipeline: {exc}", file=sys.stderr)
        return 1


def parse_args(argv: Sequence[str] | None = None) -> PipelineArgs:
    parser = argparse.ArgumentParser(description="Запуск этапов pipeline аналитики ОФЗ.")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--stage", help="Один этап, например: --stage 3.")
    selector.add_argument(
        "--stages",
        nargs="+",
        help="Несколько этапов, например: --stages 1 2 3 или --stages 1,2,3.",
    )
    selector.add_argument("--all", action="store_true", help="Запустить все реализованные этапы.")
    parser.add_argument("--safe", action="store_true", help="Для этапов 1-3 писать *_repro outputs.")
    parser.add_argument("--compare", action="store_true", help="Сравнить основные outputs и *_repro outputs этапов 1-3.")
    parser.add_argument("--interactive", action="store_true", help="Зарезервированный флаг; расчеты pipeline не меняет.")
    parser.add_argument("--report-date", help="Отчетная дата YYYY-MM-DD.")
    parser.add_argument("--retrospective-years", type=int, help="Количество лет ретроспективы.")
    parser.add_argument("--period-type", help="Тип периода: month, quarter или year.")
    parser.add_argument(
        "--aggregation-mode",
        default="cumulative",
        choices=sorted(report_params.ALLOWED_AGGREGATION_MODES),
        help="Режим агрегации: cumulative или point. По умолчанию cumulative.",
    )

    ns = parser.parse_args(argv)
    requested = select_stages(ns)
    stages = expand_dependent_stages(requested)
    explicit_requested = [] if ns.all else requested
    stages = drop_optional_missing_stages(stages, explicit_requested)
    params = validate_report_args(
        stages,
        report_date=ns.report_date,
        retrospective_years=ns.retrospective_years,
        period_type=ns.period_type,
        aggregation_mode=ns.aggregation_mode,
    )

    return PipelineArgs(
        stages=stages,
        all_requested=bool(ns.all),
        safe=bool(ns.safe),
        compare=bool(ns.compare),
        interactive=bool(ns.interactive),
        report_date=ns.report_date,
        retrospective_years=ns.retrospective_years,
        period_type=ns.period_type,
        aggregation_mode=str(ns.aggregation_mode),
        params=params,
    )


def select_stages(ns: argparse.Namespace) -> list[str]:
    if ns.all:
        return list(ALL_STAGES)
    if ns.stage:
        return [normalize_stage(ns.stage)]

    items: list[str] = []
    for item in ns.stages or []:
        items.extend(part.strip() for part in str(item).split(",") if part.strip())
    return [normalize_stage(item) for item in items]


def normalize_stage(stage: str) -> str:
    normalized = str(stage).strip().lower().replace("stage", "").replace("этап", "").strip()
    if normalized in {"04.1", "4.1", "4_1", "4-1"}:
        normalized = "4"
    elif normalized in {"08.1", "8_1", "8-1"}:
        normalized = "8.1"
    elif normalized in {"revenue", "revenue_analytics", "11_revenue_analytics"}:
        normalized = "revenue_analytics"
    elif normalized in {"revenue_charts", "12_build_revenue_charts"}:
        normalized = "revenue_charts"
    elif normalized in {"09.1", "9_1", "9-1"}:
        normalized = "9.1"
    elif normalized in {"monthly", "monthly-analytics", "monthly_analytics", "9.2"}:
        normalized = "monthly_analytics"
    elif normalized in {"monthly-charts", "monthly_charts", "10_build_monthly_charts", "9.3"}:
        normalized = "monthly_charts"
    elif normalized in {"13.1", "run-manifest", "run_manifest", "manifest"}:
        normalized = "run_manifest"
    elif normalized in {"13.2", "quality-gate", "quality_gate", "qa", "gate"}:
        normalized = "quality_gate"
    elif normalized in {"13.3", "anomaly", "anomaly-tests", "anomaly_tests"}:
        normalized = "anomaly_tests"
    elif normalized in {"13.4"}:
        normalized = "revenue_analytics"
    elif normalized in {"13.5"}:
        normalized = "revenue_charts"
    elif normalized in {"13.6", "semantic", "semantic-model-v2", "semantic_model_v2", "build_semantic_model_v2"}:
        normalized = "semantic_model_v2"
    elif normalized.isdigit():
        normalized = str(int(normalized))

    if normalized not in STAGE_SPECS:
        allowed = ", ".join(sorted(STAGE_SPECS, key=stage_sort_key))
        raise ValueError(f"Неподдерживаемый этап {stage!r}. Доступные этапы: {allowed}.")
    return normalized


def expand_dependent_stages(stages: Sequence[str]) -> list[str]:
    expanded: list[str] = []
    requested = sorted(dict.fromkeys(stages), key=stage_sort_key)
    needs_scope = any(stage in REPORT_SCOPE_STAGES for stage in requested)

    for stage in requested:
        if stage == "3" and needs_scope and "4" not in requested:
            expanded.append(stage)
            expanded.append("4")
            continue
        if stage in REPORT_SCOPE_STAGES and "3" in requested and "4" not in expanded and "4" not in requested:
            expanded.append("4")
        expanded.append(stage)

    deduplicated: list[str] = []
    for stage in expanded:
        if stage not in deduplicated:
            deduplicated.append(stage)
    return deduplicated


def drop_optional_missing_stages(stages: Sequence[str], requested: Sequence[str]) -> list[str]:
    """Не ломать `--all`, если будущие monthly-скрипты еще не созданы."""
    requested_set = set(requested)
    result: list[str] = []
    for stage in stages:
        spec = STAGE_SPECS[stage]
        if spec.optional_in_all and stage not in requested_set:
            if spec.script is None or not spec.script.exists() or spec.script.stat().st_size == 0:
                continue
        result.append(stage)
    return result


def validate_report_args(
    stages: Sequence[str],
    report_date: str | None,
    retrospective_years: int | None,
    period_type: str | None,
    aggregation_mode: str,
) -> report_params.ReportParams | None:
    needs_params = any(STAGE_SPECS[stage].needs_report_params for stage in stages)
    provided = [report_date is not None, retrospective_years is not None, period_type is not None]
    report_params.validate_aggregation_mode(aggregation_mode)

    if needs_params and not all(provided):
        raise ValueError(
            "Для параметризуемых этапов обязательны параметры "
            "--report-date, --retrospective-years, --period-type и --aggregation-mode."
        )
    if any(provided) and not all(provided):
        raise ValueError("--report-date, --retrospective-years и --period-type должны передаваться вместе.")
    if not all(provided):
        return None

    return report_params.parse_report_args(
        [
            "--report-date",
            str(report_date),
            "--retrospective-years",
            str(retrospective_years),
            "--period-type",
            str(period_type),
            "--aggregation-mode",
            str(aggregation_mode),
        ]
    )


def verify_raw_directory_is_read_only_source() -> None:
    if not config.DATA_RAW_DIR.exists():
        raise FileNotFoundError(f"Каталог исходных данных не найден: {config.DATA_RAW_DIR}")
    if not config.DATA_RAW_DIR.is_dir():
        raise NotADirectoryError(f"Путь data/raw не является каталогом: {config.DATA_RAW_DIR}")


def ensure_stage_scripts(stages: Sequence[str]) -> None:
    missing: list[str] = []
    empty: list[str] = []
    not_implemented: list[str] = []

    for stage in stages:
        spec = STAGE_SPECS[stage]
        if not spec.implemented:
            not_implemented.append(f"{stage}: {spec.name}")
            continue
        if spec.script is None:
            continue
        if not spec.script.exists():
            missing.append(f"{stage}: {spec.script}")
        elif spec.script.stat().st_size == 0:
            empty.append(f"{stage}: {spec.script}")

    if not_implemented:
        raise NotImplementedError("Запрошены этапы без реализованного скрипта: " + "; ".join(not_implemented))
    if missing:
        raise FileNotFoundError("Отсутствуют скрипты этапов: " + "; ".join(missing))
    if empty:
        raise RuntimeError("Скрипты этапов пустые и не могут быть запущены: " + "; ".join(empty))


def ensure_report_scope_prerequisites(args: PipelineArgs) -> None:
    if not any(STAGE_SPECS[stage].needs_report_scope for stage in args.stages):
        return
    if "4" in args.stages:
        return
    if not config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.exists():
        raise FileNotFoundError(
            f"Report scope dataset не найден: {config.OFZ_AUCTIONS_REPORT_SCOPE_CSV}. "
            "Сначала выполните этап 4 или запустите pipeline с этапом 3, чтобы оркестратор добавил этап 4 автоматически."
        )


def run_stage(stage: str, args: PipelineArgs, logger: logging.Logger) -> None:
    spec = STAGE_SPECS[stage]
    if stage == "run_manifest":
        write_run_manifest(args, logger)
        return
    if spec.script is None:
        validate_doc_only_stage(stage, spec)
        logger.info("Документационный этап подтвержден без запуска скрипта: %s", spec.name)
        return

    env = os.environ.copy()
    if args.safe and stage in SAFE_REPRO_STAGES:
        env["OFZ_SAFE_REPRO"] = "1"

    command = [sys.executable, str(spec.script)]
    if stage == "quality_gate":
        command.append("--fast")
    if spec.needs_report_params:
        command.extend(report_cli_args(args))

    logger.info("Запуск: %s", spec.name)
    logger.info("Команда этапа %s: %s", stage, command)

    result = subprocess.run(
        command,
        cwd=config.ROOT_DIR,
        env=env,
        check=False,
        text=True,
        capture_output=True,
    )

    if result.stdout.strip():
        logger.info("stdout этапа %s: %s", stage, result.stdout.strip())
    if result.stderr.strip():
        logger.warning("stderr этапа %s: %s", stage, result.stderr.strip())
    if result.returncode != 0:
        raise RuntimeError(f"{spec.name} завершился с кодом {result.returncode}. Подробности см. в logs/pipeline.log.")


def report_cli_args(args: PipelineArgs) -> list[str]:
    if args.report_date is None or args.retrospective_years is None or args.period_type is None:
        raise RuntimeError("Внутренняя ошибка: параметры отчета не были проверены до запуска параметризуемого этапа.")
    return [
        "--report-date",
        str(args.report_date),
        "--retrospective-years",
        str(args.retrospective_years),
        "--period-type",
        str(args.period_type),
        "--aggregation-mode",
        str(args.aggregation_mode),
    ]


def validate_stage_output(stage: str, logger: logging.Logger) -> None:
    checks: dict[str, list[Path]] = {
        "1": [config.DATA_AUDIT_DOC],
        "2": [config.OFZ_AUCTIONS_CLEAN_CSV, config.DATA_CLEANING_REPORT_DOC],
        "3": [config.OFZ_AUCTIONS_FEATURES_CSV, config.FEATURE_ENGINEERING_DOC],
        "4": [config.OFZ_AUCTIONS_REPORT_SCOPE_CSV, config.PERIOD_SELECTION_REPORT_PATH],
        "5": [config.KPI_MAP_DOC],
        "6": [config.get_doc_path("analytical_architecture.md")],
        "8": [config.CHART_BUILD_LIMITATIONS_DOC],
        "8.1": [config.ANALYTICAL_TABLES_REPORT_DOC, config.ANALYTICAL_TABLES_LIMITATIONS_DOC],
        "9": [config.get_doc_path("dashboard_architecture.md")],
        "9.1": [config.get_doc_path("dashboard_exports_report.md"), config.get_doc_path("dashboard_exports_limitations.md")],
        "10": [config.get_doc_path("executive_summary_report.md")],
        "11": [config.get_doc_path("self_review.md")],
        "12": [config.get_doc_path("final_project_summary.md")],
        "monthly_analytics": [config.DATA_PROCESSED_DIR / "ofz_monthly_metrics.csv", config.get_doc_path("monthly_analytics_report.md")],
        "monthly_charts": [config.get_doc_path("monthly_visualization_strategy.md")],
    }
    if STAGE_SPECS[stage].output_docs:
        checks[stage] = list(STAGE_SPECS[stage].output_docs)
    expected = checks.get(stage, [])
    missing = [path for path in expected if not path.exists()]
    if missing:
        details = ", ".join(str(path) for path in missing)
        raise RuntimeError(f"После этапа {stage} не найдены ожидаемые артефакты: {details}")
    if expected:
        logger.info("Проверены артефакты этапа %s: %s", stage, [str(path) for path in expected])


def validate_doc_only_stage(stage: str, spec: StageSpec) -> None:
    if not spec.output_docs:
        raise RuntimeError(f"Для документационного этапа {stage} не заданы ожидаемые артефакты.")
    missing = [path for path in spec.output_docs if not path.exists() or path.stat().st_size == 0]
    if missing:
        details = ", ".join(str(path) for path in missing)
        raise FileNotFoundError(f"{spec.name} не подтвержден: отсутствуют или пустые документы: {details}")


def run_compare(logger: logging.Logger) -> None:
    script = config.ROOT_DIR / "scripts" / "compare_outputs.py"
    if not script.exists() or script.stat().st_size == 0:
        raise FileNotFoundError(f"Скрипт сравнения outputs не найден или пустой: {script}")

    command = [sys.executable, str(script)]
    logger.info("Запуск сравнения outputs этапов 1-3: %s", command)
    result = subprocess.run(
        command,
        cwd=config.ROOT_DIR,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.stdout.strip():
        logger.info("stdout compare_outputs: %s", result.stdout.strip())
    if result.stderr.strip():
        logger.warning("stderr compare_outputs: %s", result.stderr.strip())
    if result.returncode != 0:
        raise RuntimeError(f"compare_outputs завершился с кодом {result.returncode}.")


def write_reproducibility_review(args: PipelineArgs) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Обзор запуска pipeline",
        "",
        f"Дата формирования: `{now}`.",
        "",
        "## Параметры запуска",
        "",
        f"- Этапы: `{', '.join(args.stages)}`",
        f"- Safe mode: `{args.safe}`",
        f"- Compare: `{args.compare}`",
        f"- Interactive: `{args.interactive}`",
        f"- report_date: `{args.report_date}`",
        f"- retrospective_years: `{args.retrospective_years}`",
        f"- period_type: `{args.period_type}`",
        f"- aggregation_mode: `{args.aggregation_mode}`",
        "",
        "## Контракт данных",
        "",
        "- `data/raw/` используется только как источник чтения.",
        "- После feature engineering параметризуемый report scope формируется этапом 4.",
        "- KPI, графики, аналитические таблицы, dashboard и executive summary должны использовать `data/processed/ofz_auctions_report_scope.csv`.",
        "- Параметр `aggregation_mode` прокидывается во все параметризуемые downstream-скрипты.",
        "",
        "## Safe mode",
        "",
        "- Для этапов 1-3 переменная `OFZ_SAFE_REPRO=1` включает запись `_repro` артефактов.",
        "- Downstream-этапы работают с основным report scope dataset и не получают safe-флаг автоматически.",
        "",
        "## Отчет различий",
        "",
        f"- `{config.REPRO_DIFF_STAGES_1_3_DOC.relative_to(config.ROOT_DIR).as_posix()}`",
        "",
    ]
    utils.write_markdown(config.get_doc_path("reproducibility_review_stages_1_3.md"), "\n".join(lines))


def write_run_manifest(args: PipelineArgs, logger: logging.Logger) -> None:
    """Сформировать run manifest после успешного полного запуска pipeline."""
    if args.params is None:
        logger.warning("Run manifest не сформирован: параметры отчета отсутствуют.")
        return
    paths = run_manifest.write_manifest(
        params=args.params,
        stages=args.stages,
        check_statuses={
            "pipeline_all_run": "ok" if args.all_requested else "not_requested",
            "pipeline_compare": "ok" if args.compare else "not_requested",
            "pipeline_safe_mode": "enabled" if args.safe else "disabled",
        },
        warnings=[],
        limitations=[
            "Manifest формируется после успешного `--all` и фиксирует существующие outputs на момент записи.",
            "Статусы внешних QA-проверок отражают наличие артефактов; отдельные runtime QA-скрипты запускаются через quality gate или вручную.",
        ],
        cleanup=cleanup_manifest_fields(),
    )
    logger.info("Run manifest записан: %s", paths.json_path)


def cleanup_manifest_fields() -> dict[str, str]:
    """Return cleanup pre-flight fields supplied by interactive launcher."""
    status = os.environ.get("OFZ_INTERACTIVE_CLEANUP_STATUS", "").strip()
    mode = os.environ.get("OFZ_INTERACTIVE_CLEANUP_MODE", "").strip()
    returncode = os.environ.get("OFZ_INTERACTIVE_CLEANUP_RETURNCODE", "").strip()
    if not status and not mode and not returncode:
        return {
            "source": "run_pipeline",
            "status": "not_requested",
            "mode": "not_interactive",
            "returncode": "",
        }
    return {
        "source": "interactive_pipeline",
        "status": status,
        "mode": mode,
        "returncode": returncode,
    }


def stage_sort_key(stage: str) -> tuple[int, int]:
    if stage == "run_manifest":
        return 13, 1
    if stage == "quality_gate":
        return 13, 2
    if stage == "anomaly_tests":
        return 13, 3
    if stage == "revenue_analytics":
        return 8, 2
    if stage == "revenue_charts":
        return 8, 3
    if stage == "semantic_model_v2":
        return 9, 2
    if stage == "monthly_analytics":
        return 8, 4
    if stage == "monthly_charts":
        return 8, 5
    if "." in stage:
        left, right = stage.split(".", 1)
        return int(left), int(right)
    return int(stage), 0


if __name__ == "__main__":
    raise SystemExit(main())
