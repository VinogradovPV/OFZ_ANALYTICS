"""Разложить существующие файлы из `outputs/exports` по новой структуре.

Скрипт работает только с файлами из корня `outputs/exports`, не удаляет файлы
и не перезаписывает существующие артефакты молча. По умолчанию используется
режим `--dry-run`: формируется отчет без переноса файлов.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, utils
else:
    from . import config, utils


REPORT_PATH = config.get_doc_path("outputs_reorganization_report.md")


@dataclass(frozen=True)
class ReorganizationItem:
    """Одна строка плана переноса output-файла."""

    source: Path
    target: Path
    category: str
    action: str
    note: str
    copy_target: Path | None = None


@dataclass(frozen=True)
class Classification:
    """Результат классификации файла."""

    category: str
    target_dir: Path
    note: str
    copy_dir: Path | None = None


REPORT_XLSX_PREFIXES = (
    "demand_supply_",
    "ofz_yield_by_type_",
    "placement_volume_by_maturity_",
    "format_structure_",
    "maturity_structure_",
)
ANALYTICAL_CSV_PREFIXES = (
    "demand_supply_",
    "ofz_yield_by_type_",
    "placement_volume_by_maturity_",
    "format_structure_",
    "maturity_structure_",
    "monthly_metrics_",
    "placement_volume_",
)
RISK_QUADRANT_PREFIXES = (
    "risk_quadrant_",
    "risk_quadrant_retrospective_",
    "risk_quadrant_demand_to_placement_",
)
SANKEY_PREFIXES = (
    "sankey_",
    "sankey_structure_",
    "sankey_target_period_structure_",
    "sankey_period_",
)
BOXPLOT_PREFIXES = (
    "yield_boxplot_stats_",
    "yield_boxplot_by_ofz_type_",
)
STRUCTURE_CHART_PREFIXES = (
    "placement_by_format_",
    "placement_by_maturity_",
    "format_structure_",
    "maturity_structure_",
)
MONTHLY_MARKERS = ("_month_", "monthly")
TECHNICAL_MARKERS = (
    "debug",
    "validation",
    "repro",
    "intermediate",
    "temp",
    "dictionary",
    "stats",
)


def main(argv: Sequence[str] | None = None) -> int:
    """Сформировать план или выполнить перенос файлов из `outputs/exports`."""
    args = parse_args(argv)
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    apply_changes = bool(args.apply)
    logger.info("Старт упорядочивания outputs/exports: apply=%s", apply_changes)

    config.ensure_output_directories()
    items = build_plan()
    executed = execute_plan(items) if apply_changes else mark_dry_run(items)
    utils.write_markdown(REPORT_PATH, build_report(executed, apply_changes))

    logger.info("Отчет упорядочивания outputs записан: %s", REPORT_PATH)
    logger.info("Упорядочивание outputs/exports завершено")
    return 0


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    """Разобрать режим запуска. Без режима используется dry-run."""
    parser = argparse.ArgumentParser(
        description="Разложить файлы outputs/exports по новой структуре."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Только сформировать отчет без переноса файлов. Режим по умолчанию.",
    )
    mode.add_argument(
        "--apply",
        action="store_true",
        help="Выполнить перенос файлов согласно плану.",
    )
    args = parser.parse_args(argv)
    if not args.apply:
        args.dry_run = True
    return args


def build_plan() -> list[ReorganizationItem]:
    """Построить план переноса только для файлов из корня `outputs/exports`."""
    if not config.EXPORTS_DIR.exists():
        return []

    items: list[ReorganizationItem] = []
    for source in sorted(config.EXPORTS_DIR.iterdir()):
        if not source.is_file():
            continue
        classification = classify_source(source)
        target = unique_target_path(classification.target_dir / source.name)
        copy_target = (
            unique_target_path(classification.copy_dir / source.name)
            if classification.copy_dir is not None
            else None
        )
        action = "move" if source.resolve() != target.resolve() else "keep"
        items.append(
            ReorganizationItem(
                source=source,
                target=target,
                category=classification.category,
                action=action,
                note=classification.note,
                copy_target=copy_target,
            )
        )
    return items


def classify_source(source: Path) -> Classification:
    """Классифицировать файл по имени, расширению и назначению."""
    lower_name = source.name.lower()
    suffix = source.suffix.lower()

    if suffix == ".xlsx" and lower_name.startswith(REPORT_XLSX_PREFIXES):
        if has_monthly_marker(lower_name):
            return Classification(
                "monthly_table_xlsx",
                config.REPORTS_MONTHLY_TABLES_DIR,
                "Excel-файл помесячной отчетной таблицы.",
            )
        return Classification(
            "analytical_table_xlsx",
            config.REPORTS_ANALYTICAL_TABLES_DIR,
            "Excel-файл обязательной аналитической таблицы.",
        )

    if suffix == ".csv" and lower_name.startswith(STRUCTURE_CHART_PREFIXES):
        copy_dir = config.EXPORTS_ANALYTICAL_CSV_DIR if lower_name.startswith(ANALYTICAL_CSV_PREFIXES) else None
        copy_note = " Дополнительно сохраняется копия в analytical_csv." if copy_dir else ""
        return Classification(
            "chart_data_structure",
            config.EXPORTS_CHART_DATA_STRUCTURE_DIR,
            "Таблица-основа структурной визуализации." + copy_note,
            copy_dir,
        )

    if suffix == ".csv" and lower_name.startswith(ANALYTICAL_CSV_PREFIXES):
        return Classification(
            "analytical_csv",
            config.EXPORTS_ANALYTICAL_CSV_DIR,
            "CSV-копия аналитической отчетной таблицы.",
        )

    if lower_name.startswith(RISK_QUADRANT_PREFIXES):
        return Classification(
            "chart_data_risk_quadrant",
            config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR,
            "Таблица-основа risk quadrant / demand-to-placement графика.",
        )

    if lower_name.startswith(SANKEY_PREFIXES):
        return Classification(
            "chart_data_sankey",
            config.EXPORTS_CHART_DATA_SANKEY_DIR,
            "Таблица-основа Sankey-графика.",
        )

    if lower_name.startswith(BOXPLOT_PREFIXES):
        return Classification(
            "chart_data_boxplot",
            config.EXPORTS_CHART_DATA_BOXPLOT_DIR,
            "Таблица-основа boxplot-графика.",
        )

    if has_technical_marker(lower_name):
        return Classification(
            "technical",
            config.EXPORTS_TECHNICAL_DIR,
            "Технический файл по маркеру debug/validation/repro/intermediate/temp/dictionary/stats.",
        )

    return Classification(
        "review_required",
        config.EXPORTS_REVIEW_REQUIRED_DIR,
        "Файл не подходит ни под одно правило и требует ручной проверки.",
    )


def execute_plan(items: Sequence[ReorganizationItem]) -> list[ReorganizationItem]:
    """Перенести файлы согласно плану, не перезаписывая существующие."""
    executed: list[ReorganizationItem] = []
    for item in items:
        if item.copy_target is not None:
            item.copy_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(item.source), str(item.copy_target))
        if item.action == "keep":
            executed.append(item)
            continue
        item.target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(item.source), str(item.target))
        executed.append(
            ReorganizationItem(
                source=item.source,
                target=item.target,
                category=item.category,
                action="moved",
                note=item.note,
                copy_target=item.copy_target,
            )
        )
    return executed


def mark_dry_run(items: Sequence[ReorganizationItem]) -> list[ReorganizationItem]:
    """Пометить план как dry-run без переноса файлов."""
    result: list[ReorganizationItem] = []
    for item in items:
        action = "dry_run_keep" if item.action == "keep" else "dry_run_move"
        result.append(
            ReorganizationItem(
                source=item.source,
                target=item.target,
                category=item.category,
                action=action,
                note=item.note,
                copy_target=item.copy_target,
            )
        )
    return result


def has_monthly_marker(name: str) -> bool:
    """Проверить, относится ли имя к помесячному отчету."""
    return any(marker in name for marker in MONTHLY_MARKERS)


def has_technical_marker(name: str) -> bool:
    """Проверить наличие технического маркера в имени файла."""
    return any(marker in name for marker in TECHNICAL_MARKERS)


def unique_target_path(path: Path) -> Path:
    """Вернуть безопасный целевой путь без молчаливой перезаписи."""
    if not path.exists():
        return path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate = path.with_name(f"{path.stem}_{timestamp}{path.suffix}")
    counter = 1
    while candidate.exists():
        candidate = path.with_name(f"{path.stem}_{timestamp}_{counter}{path.suffix}")
        counter += 1
    return candidate


def build_report(items: Sequence[ReorganizationItem], apply_changes: bool) -> str:
    """Сформировать markdown-отчет о плане или выполненном переносе."""
    mode = "apply" if apply_changes else "dry-run"
    lines = [
        "# Упорядочивание outputs/exports",
        "",
        f"Дата формирования: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`.",
        "",
        f"Режим: `{mode}`.",
        "",
        "Скрипт работает только с файлами из корня `outputs/exports`, не удаляет файлы и не перезаписывает существующие артефакты молча.",
        "",
        "| Исходный файл | Новый путь | Категория | Действие | Примечание |",
        "| --- | --- | --- | --- | --- |",
    ]
    if not items:
        lines.append("| - | - | - | no_files | В корне `outputs/exports` нет файлов для переноса. |")
        return "\n".join(lines)

    for item in items:
        source = item.source.relative_to(config.PROJECT_ROOT).as_posix()
        target = item.target.relative_to(config.PROJECT_ROOT).as_posix()
        note = item.note
        if item.copy_target is not None:
            copy_target = item.copy_target.relative_to(config.PROJECT_ROOT).as_posix()
            note = f"{note} Копия: `{copy_target}`."
        lines.append(
            f"| `{source}` | `{target}` | `{item.category}` | `{item.action}` | {note} |"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
