"""Очистка папки docs с переносом промежуточных документов в архив.

Скрипт не удаляет файлы безвозвратно и не изменяет data/raw/.
Все устаревшие документы переносятся только в docs/archive/.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import config


DOCS_DIR = config.DOCS_DIR
ARCHIVE_DIR = config.DOCS_ARCHIVE_DEPRECATED_DIR
LOG_PATH = config.LOGS_DIR / "pipeline.log"

KEEP_FILES = {
    "analytical_architecture.md",
    "analytical_tables_report.md",
    "analytical_tables_limitations.md",
    "chart_build_limitations.md",
    "dashboard_architecture.md",
    "dashboard_exports_report.md",
    "dashboard_exports_limitations.md",
    "data_audit.md",
    "data_cleaning_report.md",
    "executive_summary.md",
    "feature_engineering.md",
    "final_project_summary.md",
    "kpi_map.md",
    "period_selection_report.md",
    "project_inventory.md",
    "self_review.md",
    "visualization_strategy.md",
    "docs_cleanup_report.md",
}

ARCHIVE_FILES = {
    "bid_to_cover_outliers.md",
    "current_stage_status_after_1_and_3.md",
    "data_audit_repro.md",
    "data_cleaning_report_repro.md",
    "feature_engineering_repro.md",
    "parameterized_reporting_plan.md",
    "python_pipeline_instructions.md",
    "reproducibility_diff_stages_1_3.md",
    "reproducibility_review_stages_1_3.md",
    "stage_2_validation_report.md",
    "stage_3_sync_report.md",
    "stages_1_3_inventory.md",
    "table_columns_dictionary.md",
}

ARCHIVE_PATTERNS = (
    "_repro",
    "repro",
    "sync",
    "validation",
    "status",
    "current_stage",
    "stages_1_3",
    "reproducibility",
)

REVIEW_REQUIRED_FILES: set[str] = set()


@dataclass(frozen=True)
class CleanupDecision:
    """Решение по одному документу в docs/."""

    file_name: str
    decision: str
    reason: str
    destination: str
    note: str


def main() -> int:
    """Выполнить безопасную очистку docs/ и сформировать отчеты."""

    setup_logging()
    logging.info("Старт очистки docs/")

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    decisions = classify_documents()
    move_archived_documents(decisions)
    write_cleanup_report(decisions)
    write_project_inventory(decisions)
    update_final_project_summary(decisions)

    logging.info("Очистка docs/ завершена")
    return 0


def setup_logging() -> None:
    """Настроить запись действий в общий pipeline log."""

    config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def classify_documents() -> list[CleanupDecision]:
    """Классифицировать документы перед переносом."""

    decisions: list[CleanupDecision] = []
    for path in sorted(DOCS_DIR.glob("*.md")):
        name = path.name
        if name in KEEP_FILES:
            decisions.append(
                CleanupDecision(
                    name,
                    "keep",
                    "Актуальный проектный документ.",
                    "-",
                    "Оставлен в корне docs/.",
                )
            )
            continue

        if name in REVIEW_REQUIRED_FILES:
            decisions.append(
                CleanupDecision(
                    name,
                    "review_required",
                    "Файл требует ручной проверки перед архивированием.",
                    "-",
                    "Не перемещался автоматически.",
                )
            )
            continue

        if name in ARCHIVE_FILES or matches_archive_pattern(name):
            decisions.append(
                CleanupDecision(
                    name,
                    "archive",
                    "Промежуточный, repro, sync, status, validation или устаревший инвентаризационный документ.",
                    str(ARCHIVE_DIR / name),
                    "Переносится в docs/archive/ без удаления.",
                )
            )
            continue

        decisions.append(
            CleanupDecision(
                name,
                "review_required",
                "Файл не входит в целевую структуру и не совпал с архивными правилами.",
                "-",
                "Оставлен в корне docs/ до ручного решения.",
            )
        )
    return decisions


def matches_archive_pattern(file_name: str) -> bool:
    """Проверить имя файла на архивные признаки."""

    lower_name = file_name.lower()
    return any(pattern in lower_name for pattern in ARCHIVE_PATTERNS)


def move_archived_documents(decisions: list[CleanupDecision]) -> None:
    """Перенести архивные документы в docs/archive/ без перезаписи."""

    for decision in decisions:
        if decision.decision != "archive":
            continue

        source = DOCS_DIR / decision.file_name
        if not source.exists():
            continue

        destination = unique_archive_path(ARCHIVE_DIR / decision.file_name)
        logging.info("Архивирование документа: %s -> %s", source, destination)
        source.replace(destination)


def unique_archive_path(path: Path) -> Path:
    """Вернуть свободный путь в архиве, не перезаписывая существующий файл."""

    if not path.exists():
        return path

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return path.with_name(f"{path.stem}_{timestamp}{path.suffix}")


def write_cleanup_report(decisions: list[CleanupDecision]) -> None:
    """Создать отчет о классификации и переносе документов."""

    lines = [
        "# Отчет об очистке docs/",
        "",
        f"Дата формирования: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`.",
        "",
        "Файлы не удалялись безвозвратно. Промежуточные документы перенесены в `docs/archive/`.",
        "",
        "## Решения по документам",
        "",
        "| Файл | Решение | Причина | Куда перемещен | Примечание |",
        "| --- | --- | --- | --- | --- |",
    ]

    for decision in decisions:
        destination = decision.destination
        if decision.decision == "archive":
            destination = f"docs/archive/{decision.file_name}"
        lines.append(
            "| "
            + " | ".join(
                [
                    decision.file_name,
                    decision.decision,
                    decision.reason,
                    destination,
                    decision.note,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Итоговая структура корня docs/",
            "",
        ]
    )
    for path in sorted(DOCS_DIR.glob("*.md")):
        lines.append(f"- `{path.name}`")

    lines.extend(
        [
            "",
            "## Архив",
            "",
            f"Папка архива: `docs/archive/`.",
            "",
        ]
    )
    for path in sorted(ARCHIVE_DIR.glob("*.md")):
        lines.append(f"- `docs/archive/{path.name}`")

    config.get_doc_path("docs_cleanup_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_project_inventory(decisions: list[CleanupDecision]) -> None:
    """Обновить project_inventory.md с актуальной структурой docs/."""

    root_docs = sorted(path.name for path in DOCS_DIR.glob("*.md"))
    archive_docs = sorted(path.name for path in ARCHIVE_DIR.glob("*.md"))
    archived_now = [decision.file_name for decision in decisions if decision.decision == "archive"]
    review_required = [decision.file_name for decision in decisions if decision.decision == "review_required"]

    lines = [
        "# Инвентаризация проекта",
        "",
        f"Дата обновления: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`.",
        "",
        "Инвентаризация обновлена после безопасной очистки `docs/`. `data/raw/` не изменялся.",
        "",
        "## Актуальная структура docs/",
        "",
        "| Файл | Статус | Назначение |",
        "| --- | --- | --- |",
    ]
    for name in root_docs:
        status = "keep"
        purpose = "Актуальный проектный документ."
        if name == "docs_cleanup_report.md":
            purpose = "Отчет о классификации и переносе промежуточных документов."
        lines.append(f"| docs/{name} | {status} | {purpose} |")

    lines.extend(
        [
            "",
            "## Архивированные документы",
            "",
        ]
    )
    if archive_docs:
        for name in archive_docs:
            marker = "archived_now" if name in archived_now else "archived"
            lines.append(f"- `docs/archive/{name}` ({marker})")
    else:
        lines.append("- Архивных документов нет.")

    lines.extend(
        [
            "",
            "## Документы, требующие ручной проверки",
            "",
        ]
    )
    if review_required:
        for name in review_required:
            lines.append(f"- `docs/{name}`")
    else:
        lines.append("- Нет.")

    lines.extend(
        [
            "",
            "## Ограничения",
            "",
            "- Очистка не удаляет документы безвозвратно.",
            "- `docs/archive/` не удаляется автоматически.",
            "- Runtime-проверки pipeline выполняются отдельными командами проектного Python.",
        ]
    )

    config.get_doc_path("project_inventory.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_final_project_summary(decisions: list[CleanupDecision]) -> None:
    """Добавить в финальный обзор раздел о наведении порядка в docs/."""

    path = config.get_doc_path("final_project_summary.md")
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")
    marker = "## Структура документации"
    archived_count = sum(1 for decision in decisions if decision.decision == "archive")
    section = (
        f"{marker}\n\n"
        "Корень `docs/` оставлен для актуальных проектных документов pipeline. "
        f"Промежуточные, repro, sync, status и validation-документы перенесены в `docs/archive/` ({archived_count} файлов). "
        "`docs/archive/` не удаляется автоматически и может быть проверен вручную перед окончательным удалением.\n"
    )

    if marker in text:
        prefix = text.split(marker, 1)[0].rstrip()
        text = prefix + "\n\n" + section
    else:
        text = text.rstrip() + "\n\n" + section

    path.write_text(text.rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
