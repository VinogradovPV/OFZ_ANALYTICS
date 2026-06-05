"""Интерактивный launcher для запуска pipeline OFZ_ANALITICS.

Скрипт не выполняет расчеты самостоятельно. Он помогает выбрать параметры,
показывает интерпретацию отчетного периода, печатает итоговую команду и
запускает `scripts/run_pipeline.py` через локальный Python проекта.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import report_params, run_pipeline
else:
    from . import report_params, run_pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WINDOWS_LOCAL_PYTHON_COMMAND = r".\.venv\Scripts\python.exe"
POSIX_LOCAL_PYTHON_COMMAND = "./.venv/bin/python"


@dataclass(frozen=True)
class LauncherChoice:
    """Проверенные параметры интерактивного запуска."""

    report_date: date
    period_type: str
    aggregation_mode: str
    retrospective_years: int
    run_mode: str
    stages: list[str]
    periods: list[dict[str, Any]]


RUN_MODES: dict[str, str] = {
    "all": "полный pipeline",
    "stages": "ручной список этапов",
    "validate": "формирование report scope",
    "charts": "report scope и основные графики",
    "tables": "report scope и аналитические таблицы",
    "monthly": "monthly layer и помесячные графики",
    "dashboard": "dashboard exports и semantic model v2",
    "revenue": "таблицы, графики выручки и графики дисконта по форматам",
    "quality": "quality gate в fast-режиме",
    "anomaly": "anomaly tests",
    "manifest": "run manifest",
    "semantic": "semantic model v2",
}

MODE_COMMANDS: dict[str, list[str]] = {
    "validate": ["--stage", "4"],
    "charts": ["--stages", "4", "8"],
    "tables": ["--stages", "4", "8.1"],
    "monthly": ["--stages", "4", "monthly_analytics", "monthly_charts"],
    "dashboard": ["--stages", "4", "9.1", "semantic_model_v2"],
    "revenue": ["--stages", "4", "8", "revenue_analytics", "revenue_charts"],
    "quality": ["--stage", "quality_gate"],
    "anomaly": ["--stage", "anomaly_tests"],
    "manifest": ["--stage", "run_manifest"],
    "semantic": ["--stage", "semantic_model_v2"],
}

STAGE_HINTS: tuple[str, ...] = (
    "1  - аудит исходных данных",
    "2  - очистка данных",
    "3  - feature engineering",
    "4  - report scope",
    "5  - KPI map",
    "8  - графики",
    "8.1 - аналитические таблицы",
    "9.1 - dashboard exports",
    "13.1 / run_manifest",
    "13.2 / quality_gate",
    "13.3 / anomaly_tests",
    "13.4 / revenue_analytics",
    "13.5 / revenue_charts",
    "13.6 / semantic_model_v2",
    "monthly_analytics, monthly_charts",
)


def main(argv: Sequence[str] | None = None) -> int:
    """Запустить интерактивный выбор параметров и выбранную команду."""
    args = list(sys.argv[1:] if argv is None else argv)
    if any(arg in {"-h", "--help"} for arg in args):
        print_help()
        return 0
    if args:
        print("interactive_pipeline.py не принимает позиционные аргументы.")
        print("Запустите его без параметров и выберите режим в диалоге.")
        return 2

    print("OFZ_ANALITICS: интерактивный запуск pipeline")
    print(r"Команды выполняются из корня проекта через .\.venv\Scripts\python.exe.")
    print("")

    choice = ask_launcher_choice()
    show_periods(choice)
    command = build_command(choice)
    print("")
    print("Итоговая команда:")
    print(format_command(command))
    print("")

    if not ask_confirmation("Запустить команду?"):
        print("Запуск отменен. Команду можно выполнить вручную из корня проекта.")
        return 0

    completed = subprocess.run(command, cwd=PROJECT_ROOT, check=False)
    return int(completed.returncode)


def print_help() -> None:
    """Print non-interactive CLI help for console entry point checks."""
    print("usage: ofz-interactive [-h]")
    print("")
    print("Interactive launcher for OFZ_ANALITICS pipeline.")
    print("")
    print("options:")
    print("  -h, --help  show this help message and exit")
    print("")
    print("Run without arguments from the project root:")
    print(r"  .\.venv\Scripts\python.exe scripts\interactive_pipeline.py")


def ask_launcher_choice() -> LauncherChoice:
    """Запросить параметры отчета и режим запуска."""
    while True:
        report_date = ask_date("report_date (YYYY-MM-DD, первый день месяца)")
        period_type = ask_choice("period_type", ["month", "quarter", "year"], default="month")
        aggregation_mode = ask_choice("aggregation_mode", ["cumulative", "point"], default="cumulative")
        retrospective_years = ask_non_negative_int("retrospective_years", default=4)
        try:
            periods = report_params.build_report_periods(
                report_date=report_date,
                retrospective_years=retrospective_years,
                period_type=period_type,
                aggregation_mode=aggregation_mode,
            )
        except ValueError as exc:
            print(f"Ошибка параметров: {exc}")
            print("Введите параметры заново.")
            print("")
            continue
        break

    run_mode = ask_choice("режим запуска", list(RUN_MODES), default="all", descriptions=RUN_MODES)
    stages: list[str] = []
    if run_mode == "stages":
        stages = ask_stages()

    return LauncherChoice(
        report_date=report_date,
        period_type=period_type,
        aggregation_mode=aggregation_mode,
        retrospective_years=retrospective_years,
        run_mode=run_mode,
        stages=stages,
        periods=periods,
    )


def ask_date(prompt: str) -> date:
    """Запросить и проверить отчетную дату."""
    while True:
        raw = input(f"{prompt}: ").strip()
        try:
            value = date.fromisoformat(raw)
            report_params.validate_report_date(value)
        except ValueError as exc:
            print(f"Некорректная дата: {exc}")
            continue
        return value


def ask_choice(
    prompt: str,
    choices: list[str],
    default: str,
    descriptions: dict[str, str] | None = None,
) -> str:
    """Запросить значение из фиксированного списка."""
    joined = "/".join(choices)
    while True:
        if descriptions:
            print("")
            for key in choices:
                print(f"- {key}: {descriptions[key]}")
        raw = input(f"{prompt} [{joined}], default={default}: ").strip().lower()
        value = raw or default
        if value in choices:
            return value
        print(f"Допустимые значения: {', '.join(choices)}.")


def ask_non_negative_int(prompt: str, default: int) -> int:
    """Запросить неотрицательное целое число."""
    while True:
        raw = input(f"{prompt}, default={default}: ").strip()
        if not raw:
            return default
        try:
            value = int(raw)
            report_params.validate_retrospective_years(value)
        except ValueError as exc:
            print(f"Некорректное значение: {exc}")
            continue
        return value


def ask_stages() -> list[str]:
    """Запросить список этапов для `run_pipeline.py --stages`."""
    print("")
    print("Доступные подсказки по этапам:")
    for hint in STAGE_HINTS:
        print(f"- {hint}")

    while True:
        raw = input("Этапы через пробел или запятую, например `1 2 3 4 8`: ").strip()
        stages = [item.strip() for chunk in raw.split(",") for item in chunk.split() if item.strip()]
        if not stages:
            print("Нужно указать хотя бы один этап.")
            continue
        invalid = validate_stage_names(stages)
        if invalid:
            print(f"Неподдерживаемые этапы: {', '.join(invalid)}.")
            continue
        return stages


def validate_stage_names(stages: list[str]) -> list[str]:
    """Проверить stage aliases через контракт run_pipeline."""
    invalid: list[str] = []
    for stage in stages:
        try:
            run_pipeline.normalize_stage(stage)
        except ValueError:
            invalid.append(stage)
    return invalid


def show_periods(choice: LauncherChoice) -> None:
    """Показать пользователю интерпретацию периода до запуска."""
    target_period = next((period for period in choice.periods if bool(period["is_target_period"])), None)
    print("")
    print("Проверенные параметры:")
    print(f"- report_date: {choice.report_date.isoformat()}")
    print(f"- period_type: {choice.period_type}")
    print(f"- aggregation_mode: {choice.aggregation_mode}")
    print(f"- retrospective_years: {choice.retrospective_years}")
    print(f"- режим запуска: {choice.run_mode} ({RUN_MODES[choice.run_mode]})")

    if target_period is not None:
        print("")
        print("Интерпретация целевого отчетного периода:")
        print(
            "- "
            f"{target_period['report_period_display_label']}: "
            f"{target_period['period_start']} -> {target_period['period_end']}"
        )

    print("")
    print("Периоды сравнения:")
    for period in choice.periods:
        target_mark = " (целевой)" if bool(period["is_target_period"]) else ""
        print(
            "- "
            f"{period['report_period_label']}: "
            f"{period['period_start']} -> {period['period_end']}"
            f"{target_mark}"
        )


def build_command(choice: LauncherChoice) -> list[str]:
    """Собрать команду запуска через локальный Python проекта."""
    command = [local_python_command(), "scripts/run_pipeline.py"]
    if choice.run_mode == "all":
        command.append("--all")
    elif choice.run_mode == "stages":
        command.extend(["--stages", *choice.stages])
    else:
        command.extend(MODE_COMMANDS[choice.run_mode])

    command.extend(report_cli_args(choice))
    return command


def report_cli_args(choice: LauncherChoice) -> list[str]:
    """Вернуть CLI-параметры отчета."""
    return [
        "--report-date",
        choice.report_date.isoformat(),
        "--retrospective-years",
        str(choice.retrospective_years),
        "--period-type",
        choice.period_type,
        "--aggregation-mode",
        choice.aggregation_mode,
    ]


def local_python_command() -> str:
    """Вернуть относительный путь к Python внутри локального `.venv`."""
    if (PROJECT_ROOT / ".venv" / "Scripts" / "python.exe").exists():
        return WINDOWS_LOCAL_PYTHON_COMMAND
    if (PROJECT_ROOT / ".venv" / "bin" / "python").exists():
        return POSIX_LOCAL_PYTHON_COMMAND
    return WINDOWS_LOCAL_PYTHON_COMMAND


def ask_confirmation(prompt: str) -> bool:
    """Запросить подтверждение запуска."""
    answer = input(f"{prompt} [y/N]: ").strip().lower()
    return answer in {"y", "yes", "д", "да"}


def format_command(command: Sequence[str]) -> str:
    """Показать команду в виде, пригодном для PowerShell."""
    return " ".join(quote_arg(item) for item in command)


def quote_arg(value: str) -> str:
    """Заключить аргумент в кавычки только при необходимости."""
    if any(char.isspace() for char in value):
        return f'"{value}"'
    return value


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
