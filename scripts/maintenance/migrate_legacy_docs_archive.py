"""Миграция старой папки docs/archive в новую структуру docs/90_archive.

По умолчанию скрипт работает в режиме dry-run. Фактический перенос файлов
выполняется только при явном параметре --apply. Файлы не удаляются и не
перезаписываются молча.
"""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = PROJECT_ROOT / "docs"
LEGACY_ARCHIVE_DIR = DOCS_DIR / "archive"
REPORT_PATH = DOCS_DIR / "06_quality" / "legacy_docs_archive_migration_report.md"


@dataclass(frozen=True)
class MigrationPlan:
    """Одна строка плана миграции старого docs/archive."""

    source: Path
    target: Path
    category: str
    action: str
    status: str
    note: str


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    apply_changes = bool(args.apply)

    ensure_target_directories()
    plans = build_plan()
    if apply_changes:
        plans = apply_plan(plans)
    write_report(plans, apply_changes)

    print(REPORT_PATH.relative_to(PROJECT_ROOT).as_posix())
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Разобрать режим запуска."""
    parser = argparse.ArgumentParser(description="Миграция старой docs/archive в новую docs/90_archive.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Сформировать отчет без переноса файлов.")
    mode.add_argument("--apply", action="store_true", help="Выполнить перенос файлов.")
    args = parser.parse_args(argv)
    if not args.apply:
        args.dry_run = True
    return args


def ensure_target_directories() -> None:
    """Создать целевые папки."""
    for directory in (
        DOCS_DIR / "01_methodology",
        DOCS_DIR / "06_quality",
        DOCS_DIR / "90_archive" / "deprecated",
        DOCS_DIR / "90_archive" / "stage_reports",
        DOCS_DIR / "90_archive" / "old_reproducibility",
    ):
        directory.mkdir(parents=True, exist_ok=True)


def build_plan() -> list[MigrationPlan]:
    """Построить план миграции файлов из старого архива."""
    if not LEGACY_ARCHIVE_DIR.exists():
        return []

    plans: list[MigrationPlan] = []
    for source in sorted(LEGACY_ARCHIVE_DIR.glob("*.md")):
        target_dir, category, action, note = classify_legacy_file(source.name)
        target = safe_target_path(target_dir / source.name)
        plans.append(
            MigrationPlan(
                source=source,
                target=target,
                category=category,
                action=action,
                status="planned",
                note=note,
            )
        )
    return plans


def classify_legacy_file(filename: str) -> tuple[Path, str, str, str]:
    """Определить целевую папку старого архивного документа."""
    lower_name = filename.lower()
    if filename == "table_columns_dictionary.md":
        return (
            DOCS_DIR / "01_methodology",
            "methodology",
            "restore",
            "Возврат словаря колонок из старого архива в методологическую документацию.",
        )
    if "repro" in lower_name or "reproducibility" in lower_name:
        return (
            DOCS_DIR / "90_archive" / "old_reproducibility",
            "archive/old_reproducibility",
            "move",
            "Старый reproducibility/repro-документ.",
        )
    if lower_name.startswith("stage_") or "stage" in lower_name or "sync" in lower_name or "status" in lower_name:
        return (
            DOCS_DIR / "90_archive" / "stage_reports",
            "archive/stage_reports",
            "move",
            "Старый stage/status/sync/inventory отчет.",
        )
    return (
        DOCS_DIR / "90_archive" / "deprecated",
        "archive/deprecated",
        "move",
        "Старый диагностический или deprecated-документ.",
    )


def apply_plan(plans: list[MigrationPlan]) -> list[MigrationPlan]:
    """Выполнить переносы без удаления и молчаливой перезаписи."""
    applied: list[MigrationPlan] = []
    for plan in plans:
        if not plan.source.exists():
            applied.append(
                MigrationPlan(
                    source=plan.source,
                    target=plan.target,
                    category=plan.category,
                    action=plan.action,
                    status="missing_source",
                    note="Исходный файл отсутствует; перенос пропущен.",
                )
            )
            continue
        target = safe_target_path(plan.target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(plan.source), str(target))
        applied.append(
            MigrationPlan(
                source=plan.source,
                target=target,
                category=plan.category,
                action=plan.action,
                status="moved",
                note=plan.note,
            )
        )
    return applied


def safe_target_path(target: Path) -> Path:
    """Добавить безопасный суффикс, если целевой файл уже существует."""
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    legacy_target = target.with_name(f"{stem}__legacy_archive{suffix}")
    if not legacy_target.exists():
        return legacy_target
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate = target.with_name(f"{stem}__legacy_archive_{timestamp}{suffix}")
    counter = 1
    while candidate.exists():
        candidate = target.with_name(f"{stem}__legacy_archive_{timestamp}_{counter}{suffix}")
        counter += 1
    return candidate


def write_report(plans: list[MigrationPlan], apply_changes: bool) -> None:
    """Записать отчет по миграции старого архива."""
    mode = "apply" if apply_changes else "dry-run"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Миграция старой docs/archive",
        "",
        f"Дата формирования: `{now}`.",
        f"Режим: `{mode}`.",
        "",
        "Файлы не удаляются. При конфликте имени используется безопасный суффикс.",
        "",
        "| Исходный путь | Новый путь | Категория | Действие | Статус | Примечание |",
        "|---|---|---|---|---|---|",
    ]
    for plan in plans:
        lines.append(
            "| "
            f"`{relative(plan.source)}` | "
            f"`{relative(plan.target)}` | "
            f"{plan.category} | "
            f"{plan.action} | "
            f"{plan.status} | "
            f"{escape_table(plan.note)} |"
        )
    lines.extend(
        [
            "",
            "## Сводка",
            "",
            f"- Всего файлов в плане: `{len(plans)}`.",
            f"- Возвратов в актуальную документацию: `{sum(1 for plan in plans if plan.action == 'restore')}`.",
            f"- Переносов в архив: `{sum(1 for plan in plans if plan.action == 'move')}`.",
            f"- Фактически перемещено: `{sum(1 for plan in plans if plan.status == 'moved')}`.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def relative(path: Path) -> str:
    """Вернуть путь относительно корня проекта."""
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def escape_table(value: str) -> str:
    """Экранировать markdown-таблицу."""
    return value.replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
