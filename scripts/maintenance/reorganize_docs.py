"""Безопасная реорганизация markdown-документов в docs/.

Скрипт по умолчанию работает в режиме dry-run: строит план переноса и
формирует отчет, но не перемещает документы. Фактический перенос выполняется
только при явном параметре --apply.
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
REPORT_PATH = DOCS_DIR / "06_quality" / "docs_reorganization_report.md"


CATEGORY_DIRS: dict[str, Path] = {
    "project": DOCS_DIR / "00_project",
    "methodology": DOCS_DIR / "01_methodology",
    "data_pipeline": DOCS_DIR / "02_data_pipeline",
    "analytics": DOCS_DIR / "03_analytics",
    "visualization": DOCS_DIR / "04_visualization",
    "dashboard": DOCS_DIR / "05_dashboard",
    "quality": DOCS_DIR / "06_quality",
    "archive_modernization": DOCS_DIR / "90_archive" / "modernization",
    "archive_stage_reports": DOCS_DIR / "90_archive" / "stage_reports",
    "archive_old_reproducibility": DOCS_DIR / "90_archive" / "old_reproducibility",
    "archive_deprecated": DOCS_DIR / "90_archive" / "deprecated",
    "review_required": DOCS_DIR / "90_archive" / "deprecated",
}


FILE_CATEGORY_RULES: dict[str, str] = {
    # Project.
    "final_project_summary.md": "project",
    "self_review.md": "project",
    "project_inventory.md": "project",
    "outputs_structure.md": "project",
    "analytical_architecture.md": "project",
    "dashboard_architecture.md": "project",
    # Methodology.
    "kpi_map.md": "methodology",
    "bid_to_cover_utils.md": "methodology",
    "period_selection_report.md": "methodology",
    "revenue_kpi_map.md": "methodology",
    "table_columns_dictionary.md": "methodology",
    # Data pipeline.
    "data_audit.md": "data_pipeline",
    "data_cleaning_report.md": "data_pipeline",
    "data_cleaning_report_repro.md": "data_pipeline",
    "feature_engineering.md": "data_pipeline",
    "feature_engineering_repro.md": "data_pipeline",
    "raw_data_registry_report.md": "data_pipeline",
    "schema_validation_report.md": "data_pipeline",
    # Analytics.
    "analytical_tables_limitations.md": "analytics",
    "analytical_tables_report.md": "analytics",
    "executive_summary.md": "analytics",
    "executive_summary_report.md": "analytics",
    "monthly_analytics_report.md": "analytics",
    "revenue_analytics_report.md": "analytics",
    "revenue_charts_report.md": "analytics",
    # Visualization.
    "chart_build_limitations.md": "visualization",
    "boxplot_diagnostics.md": "visualization",
    "monthly_visualization_strategy.md": "visualization",
    "palette_policy.md": "visualization",
    "visualization_strategy.md": "visualization",
    # Dashboard.
    "dashboard_exports_limitations.md": "dashboard",
    "dashboard_exports_report.md": "dashboard",
    "dashboard_semantic_model_v2.md": "dashboard",
    # Quality.
    "anomaly_tests_report.md": "quality",
    "manual_checks_log.md": "quality",
    "quality_gate_report.md": "quality",
    "regression_tests_report.md": "quality",
    "run_manifest_report.md": "quality",
    "smoke_tests_report.md": "quality",
    "visual_regression_report.md": "quality",
    # Archive.
    "current_modernization_baseline.md": "archive_modernization",
    "second_modernization_baseline.md": "archive_modernization",
    "docs_cleanup_report.md": "archive_stage_reports",
    "cleanup_report.md": "archive_stage_reports",
    "outputs_reorganization_report.md": "archive_stage_reports",
    "outputs_structure_migration_report.md": "archive_stage_reports",
    "reproducibility_review_stages_1_3.md": "archive_old_reproducibility",
    "bid_to_cover_outliers.md": "archive_deprecated",
}


DISPLAY_CATEGORY: dict[str, str] = {
    "archive_modernization": "archive",
    "archive_stage_reports": "archive",
    "archive_old_reproducibility": "archive",
    "archive_deprecated": "archive",
}


@dataclass(frozen=True)
class MovePlan:
    """Одна строка плана реорганизации документа."""

    source: Path
    target: Path
    category: str
    action: str
    status: str
    note: str


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    apply_changes = bool(args.apply)

    ensure_directories()
    plans = build_plan()
    if apply_changes:
        plans = apply_plan(plans)
    write_report(plans, apply_changes)

    print(REPORT_PATH.relative_to(PROJECT_ROOT).as_posix())
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Разобрать параметры запуска."""
    parser = argparse.ArgumentParser(description="Безопасная реорганизация markdown-документов docs/.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Сформировать план без переноса файлов.")
    mode.add_argument("--apply", action="store_true", help="Выполнить перенос файлов по плану.")
    args = parser.parse_args(argv)
    if not args.apply:
        args.dry_run = True
    return args


def ensure_directories() -> None:
    """Создать целевые папки и папку отчета."""
    for directory in set(CATEGORY_DIRS.values()):
        directory.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)


def build_plan() -> list[MovePlan]:
    """Сформировать план переноса markdown-файлов из корня docs/."""
    plans: list[MovePlan] = []
    for source in sorted(DOCS_DIR.glob("*.md")):
        category_key = classify_document(source.name)
        target_dir = CATEGORY_DIRS[category_key]
        target = safe_target_path(target_dir / source.name)
        display_category = DISPLAY_CATEGORY.get(category_key, category_key)
        note = category_note(category_key, source)
        status = "planned"
        action = "move"
        if source.resolve() == target.resolve():
            action = "keep"
            status = "already_in_place"
            note = "Файл уже находится в целевой папке."
        plans.append(
            MovePlan(
                source=source,
                target=target,
                category=display_category,
                action=action,
                status=status,
                note=note,
            )
        )
    return plans


def classify_document(filename: str) -> str:
    """Определить категорию документа по явным правилам и архивным паттернам."""
    if filename in FILE_CATEGORY_RULES:
        return FILE_CATEGORY_RULES[filename]
    lower_name = filename.lower()
    if lower_name.startswith("stage_") and lower_name.endswith("_report.md"):
        return "archive_stage_reports"
    archive_markers = (
        "modernization",
        "repro",
        "reproducibility",
        "current_stage",
        "stages_",
        "sync",
        "validation",
        "status",
        "cleanup",
    )
    if any(marker in lower_name for marker in archive_markers):
        if "repro" in lower_name or "reproducibility" in lower_name:
            return "archive_old_reproducibility"
        if "modernization" in lower_name:
            return "archive_modernization"
        return "archive_stage_reports"
    return "review_required"


def apply_plan(plans: list[MovePlan]) -> list[MovePlan]:
    """Выполнить перенос по плану без удаления и молчаливой перезаписи."""
    applied: list[MovePlan] = []
    for plan in plans:
        if plan.action == "keep":
            applied.append(plan)
            continue
        target = safe_target_path(plan.target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(plan.source), str(target))
        applied.append(
            MovePlan(
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
    """Вернуть безопасный путь, добавляя суффикс при конфликте имени."""
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate = target.with_name(f"{stem}__moved_{timestamp}{suffix}")
    counter = 1
    while candidate.exists():
        candidate = target.with_name(f"{stem}__moved_{timestamp}_{counter}{suffix}")
        counter += 1
    return candidate


def category_note(category_key: str, source: Path) -> str:
    """Сформировать пояснение к решению классификации."""
    if category_key == "review_required":
        return "Файл не попал в явные правила классификации; требуется ручная проверка."
    if category_key.startswith("archive_"):
        return "Промежуточный, исторический или диагностический документ; переносится в архивную зону."
    return f"Документ отнесен к тематической категории `{DISPLAY_CATEGORY.get(category_key, category_key)}`."


def write_report(plans: list[MovePlan], apply_changes: bool) -> None:
    """Записать markdown-отчет по dry-run/apply."""
    mode = "apply" if apply_changes else "dry-run"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Отчет о реорганизации docs",
        "",
        f"Дата формирования: `{now}`.",
        f"Режим: `{mode}`.",
        "",
        "Файлы не удаляются безвозвратно. При конфликте имени целевой файл получает безопасный суффикс.",
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
            f"- Запланировано переносов: `{sum(1 for plan in plans if plan.action == 'move')}`.",
            f"- Требуют ручной проверки: `{sum(1 for plan in plans if plan.category == 'review_required')}`.",
            f"- Архивных кандидатов: `{sum(1 for plan in plans if plan.category == 'archive')}`.",
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
    """Экранировать символы, которые ломают markdown-таблицу."""
    return value.replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
