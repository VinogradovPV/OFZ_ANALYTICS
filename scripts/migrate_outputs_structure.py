"""Безопасная миграция существующих outputs в упорядоченную структуру.

Скрипт не удаляет файлы безвозвратно и не трогает `data/raw/`.
Существующие артефакты переносятся в новые целевые папки или в архив
для ручной проверки, если назначение файла неоднозначно.
"""

from __future__ import annotations

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


REPORT_PATH = config.get_doc_path("outputs_structure_migration_report.md")


@dataclass(frozen=True)
class MigrationDecision:
    source: Path
    target: Path
    decision: str
    reason: str


TARGET_DIRECTORIES = (
    config.OUTPUT_REPORTS_DIR,
    config.REPORTS_ANALYTICAL_TABLES_DIR,
    config.REPORTS_MONTHLY_TABLES_DIR,
    config.EXPORTS_DIR,
    config.EXPORTS_ANALYTICAL_CSV_DIR,
    config.EXPORTS_CHART_DATA_DIR,
    config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR,
    config.EXPORTS_CHART_DATA_SANKEY_DIR,
    config.EXPORTS_CHART_DATA_BOXPLOT_DIR,
    config.EXPORTS_CHART_DATA_STRUCTURE_DIR,
    config.EXPORTS_TECHNICAL_DIR,
    config.EXPORTS_TECHNICAL_REVIEW_REQUIRED_DIR,
    config.DASHBOARDS_DIR,
    config.OUTPUTS_ARCHIVE_DIR,
    config.OUTPUTS_ARCHIVE_DIR / "review_required",
)


ANALYTICAL_TABLE_PREFIXES = (
    "ofz_yield_by_type_",
    "demand_supply_",
    "placement_volume_by_maturity_",
)
RISK_PREFIXES = (
    "risk_quadrant",
    "demand_cutoff",
    "bid_to_cover",
)
SANKEY_PREFIXES = ("sankey",)
BOXPLOT_PREFIXES = ("yield_boxplot",)
STRUCTURE_PREFIXES = (
    "placement_volume_",
    "yield_by_type_",
    "demand_supply_",
    "format_structure_",
    "maturity_structure_",
)
MONTHLY_PREFIXES = (
    "monthly_",
    "ofz_monthly_",
    "dashboard_monthly_",
)


def main(argv: Sequence[str] | None = None) -> int:
    """Выполнить миграцию outputs без удаления файлов."""
    _ = argv
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт миграции структуры outputs")

    for directory in TARGET_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)

    decisions = build_migration_plan()
    moved: list[MigrationDecision] = []
    for decision in decisions:
        if decision.decision == "keep":
            continue
        target = unique_target_path(decision.target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(decision.source), str(target))
        moved.append(
            MigrationDecision(
                source=decision.source,
                target=target,
                decision=decision.decision,
                reason=decision.reason,
            )
        )
        logger.info("Перенесен output: %s -> %s", decision.source, target)

    utils.write_markdown(REPORT_PATH, build_report(decisions, moved))
    logger.info("Отчет миграции outputs записан: %s", REPORT_PATH)
    logger.info("Миграция структуры outputs завершена")
    return 0


def build_migration_plan() -> list[MigrationDecision]:
    """Сформировать план переноса файлов из старой структуры."""
    decisions: list[MigrationDecision] = []
    if not config.OUTPUTS_DIR.exists():
        return decisions

    for path in sorted(config.OUTPUTS_DIR.rglob("*")):
        if not path.is_file():
            continue
        if path == REPORT_PATH:
            continue
        if is_inside_new_structure(path):
            decisions.append(
                MigrationDecision(path, path, "keep", "Файл уже находится в целевой структуре.")
            )
            continue
        decisions.append(classify_file(path))
    return decisions


def is_inside_new_structure(path: Path) -> bool:
    """Проверить, что файл уже лежит в одной из целевых папок."""
    target_roots = (
        config.OUTPUT_REPORTS_DIR,
        config.EXPORTS_ANALYTICAL_CSV_DIR,
        config.EXPORTS_CHART_DATA_DIR,
        config.EXPORTS_TECHNICAL_DIR,
        config.DASHBOARDS_DIR,
        config.OUTPUTS_ARCHIVE_DIR,
    )
    return any(is_relative_to(path, root) for root in target_roots)


def classify_file(path: Path) -> MigrationDecision:
    """Классифицировать существующий файл outputs."""
    name = path.name
    lower_name = name.lower()

    if is_relative_to(path, config.CHARTS_DIR):
        return MigrationDecision(path, path, "keep", "HTML-графики остаются в outputs/charts/.")

    if is_relative_to(path, config.DASHBOARDS_DIR):
        return MigrationDecision(path, path, "keep", "Dashboard exports уже находятся в outputs/dashboards/.")

    if not is_relative_to(path, config.EXPORTS_DIR):
        target = config.OUTPUTS_ARCHIVE_DIR / "review_required" / name
        return MigrationDecision(path, target, "archive_review", "Файл вне ожидаемых подпапок outputs.")

    if lower_name.endswith(".xlsx") and lower_name.startswith(ANALYTICAL_TABLE_PREFIXES):
        target = config.REPORTS_ANALYTICAL_TABLES_DIR / name
        return MigrationDecision(path, target, "move", "XLSX обязательной аналитической таблицы.")

    if lower_name.endswith(".csv") and lower_name.startswith(ANALYTICAL_TABLE_PREFIXES):
        xlsx_peer = path.with_suffix(".xlsx")
        if xlsx_peer.exists():
            target = config.EXPORTS_ANALYTICAL_CSV_DIR / name
            return MigrationDecision(path, target, "move", "CSV-копия обязательной аналитической таблицы.")

    if lower_name.startswith(MONTHLY_PREFIXES):
        target = config.REPORTS_MONTHLY_TABLES_DIR / name
        return MigrationDecision(path, target, "move", "Помесячная таблица или monthly layer output.")

    if lower_name.startswith(SANKEY_PREFIXES):
        target = config.EXPORTS_CHART_DATA_SANKEY_DIR / name
        return MigrationDecision(path, target, "move", "Таблица-основа Sankey-графика.")

    if lower_name.startswith(BOXPLOT_PREFIXES):
        target = config.EXPORTS_CHART_DATA_BOXPLOT_DIR / name
        return MigrationDecision(path, target, "move", "Таблица-основа boxplot-графика.")

    if lower_name.startswith(RISK_PREFIXES):
        target = config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR / name
        return MigrationDecision(path, target, "move", "Таблица-основа риск-графика.")

    if lower_name.startswith(STRUCTURE_PREFIXES):
        target = config.EXPORTS_CHART_DATA_STRUCTURE_DIR / name
        return MigrationDecision(path, target, "move", "Таблица-основа структурной визуализации.")

    target = config.EXPORTS_TECHNICAL_REVIEW_REQUIRED_DIR / name
    return MigrationDecision(path, target, "review_required", "Назначение файла не определено автоматически.")


def unique_target_path(path: Path) -> Path:
    """Вернуть свободный путь, не перезаписывая существующие файлы."""
    if not path.exists():
        return path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate = path.with_name(f"{path.stem}_{timestamp}{path.suffix}")
    counter = 1
    while candidate.exists():
        candidate = path.with_name(f"{path.stem}_{timestamp}_{counter}{path.suffix}")
        counter += 1
    return candidate


def is_relative_to(path: Path, root: Path) -> bool:
    """Совместимая проверка принадлежности пути корню."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def build_report(
    decisions: Sequence[MigrationDecision],
    moved: Sequence[MigrationDecision],
) -> str:
    """Сформировать отчет о плане и фактическом переносе outputs."""
    lines = [
        "# Миграция структуры outputs",
        "",
        f"Дата формирования: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`.",
        "",
        "Скрипт не удаляет файлы безвозвратно и не изменяет `data/raw/`.",
        "",
        "## Целевая структура",
        "",
    ]
    for directory in TARGET_DIRECTORIES:
        rel = directory.relative_to(config.ROOT_DIR).as_posix()
        lines.append(f"- `{rel}/`")

    lines.extend(
        [
            "",
            "## Решения по файлам",
            "",
            "| Файл | Решение | Причина | Целевой путь |",
            "|---|---|---|---|",
        ]
    )
    moved_by_source = {item.source: item for item in moved}
    for decision in decisions:
        actual = moved_by_source.get(decision.source, decision)
        source = decision.source.relative_to(config.ROOT_DIR).as_posix()
        target = actual.target.relative_to(config.ROOT_DIR).as_posix()
        lines.append(f"| `{source}` | `{decision.decision}` | {decision.reason} | `{target}` |")

    if moved:
        lines.extend(["", "## Перенесенные файлы", ""])
        for item in moved:
            source = item.source.relative_to(config.ROOT_DIR).as_posix()
            target = item.target.relative_to(config.ROOT_DIR).as_posix()
            lines.append(f"- `{source}` -> `{target}`")
    else:
        lines.extend(["", "## Перенесенные файлы", "", "- Файлы для переноса не найдены."])

    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
