"""Inventory-first cleanup workflow for project documentation.

The script never deletes files in dry-run mode. Archive mode moves only
documents classified as archive/delete candidates into docs/archive/YYYY-MM-DD/.
Permanent deletion is limited to files already archived by a previous manifest.
"""

from __future__ import annotations

import argparse
import csv
import shutil
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = PROJECT_ROOT / "docs"
OUTPUTS_REPORTS_CLEANUP_DIR = PROJECT_ROOT / "outputs" / "reports" / "cleanup"
BEFORE_INVENTORY_PATH = DOCS_DIR / "00_project" / "docs_inventory_before_cleanup.md"
AFTER_INVENTORY_PATH = DOCS_DIR / "00_project" / "docs_inventory_after_cleanup.md"
ARCHIVE_ROOT = DOCS_DIR / "archive"

ACTIVE_EXACT_PATHS = {
    "docs/index.md",
    "docs/00_project/analytical_architecture.md",
    "docs/00_project/artifact_policy.md",
    "docs/00_project/dashboard_architecture.md",
    "docs/00_project/final_project_summary.md",
    "docs/00_project/outputs_structure.md",
    "docs/00_project/production_cleanup_baseline.md",
    "docs/00_project/production_readiness_report.md",
    "docs/00_project/project_inventory.md",
    "docs/00_project/docs_cleanup_apply_decision.md",
    "docs/00_project/docs_inventory_before_cleanup.md",
    "docs/00_project/docs_inventory_after_cleanup.md",
    "docs/00_project/scripts_inventory_before_cleanup.md",
    "docs/00_project/scripts_migration_plan.md",
    "docs/00_project/scripts_structure_plan.md",
    "docs/00_project/self_review.md",
    "docs/01_methodology/kpi_map.md",
    "docs/01_methodology/period_selection_report.md",
    "docs/01_methodology/revenue_kpi_map.md",
    "docs/01_methodology/table_columns_dictionary.md",
    "docs/02_data_contracts/chart_data_contract.md",
    "docs/02_data_contracts/processed_data_contract.md",
    "docs/02_data_contracts/analytical_tables_contract.md",
    "docs/02_data_contracts/dashboard_exports_contract.md",
    "docs/02_data_contracts/semantic_model_v2.md",
    "docs/02_data_pipeline/data_audit.md",
    "docs/02_data_pipeline/data_cleaning_report.md",
    "docs/02_data_pipeline/feature_engineering.md",
    "docs/02_data_pipeline/raw_data_registry_report.md",
    "docs/02_data_pipeline/schema_validation_report.md",
    "docs/03_analytics/analytical_tables_limitations.md",
    "docs/03_analytics/analytical_tables_report.md",
    "docs/03_analytics/executive_summary.md",
    "docs/03_analytics/executive_summary_report.md",
    "docs/03_analytics/monthly_analytics_report.md",
    "docs/03_analytics/revenue_analytics_report.md",
    "docs/03_analytics/revenue_charts_report.md",
    "docs/04_visualization/chart_build_limitations.md",
    "docs/04_visualization/monthly_visualization_strategy.md",
    "docs/04_visualization/palette_policy.md",
    "docs/04_visualization/visualization_strategy.md",
    "docs/05_dashboard/dashboard_exports_limitations.md",
    "docs/05_dashboard/dashboard_exports_report.md",
    "docs/05_dashboard/dashboard_semantic_model_v2.md",
    "docs/06_quality/anomaly_tests_report.md",
    "docs/06_quality/manual_checks_log.md",
    "docs/06_quality/quality_gate_report.md",
    "docs/06_quality/run_manifest_report.md",
    "docs/06_quality/visual_regression_report.md",
    "docs/07_operations/environment.md",
    "docs/07_operations/production_runbook.md",
    "docs/07_operations/release_checklist.md",
    "docs/03_pipeline/module_decomposition_plan.md",
}

ACTIVE_NAME_HINTS = {
    "release_checklist.md",
    "module_decomposition_plan.md",
    "quality_gate_report.md",
    "manual_checks_log.md",
    "production_runbook.md",
    "environment.md",
}

MERGE_CANDIDATE_NAMES = {
    "boxplot_diagnostics.md",
    "chart_improvement_diagnostics.md",
    "chart_improvement_scope.md",
    "format_revenue_discount_chart_diagnostics.md",
}

ARCHIVE_CANDIDATE_NAMES = {
    "charts_reorganization_report.md",
    "docs_reorganization_report.md",
    "legacy_docs_archive_migration_dry_run.md",
    "legacy_docs_archive_migration_report.md",
}

ARCHIVE_DIR_MARKERS = (
    "docs/90_archive/",
    "docs/archive/",
)

ARCHIVE_NAME_MARKERS = (
    "modernization",
    "stage_",
    "_stage_",
    "cleanup_report",
    "reorganization",
    "migration",
    "repro",
    "legacy",
    "deprecated",
    "baseline",
    "__before_doc_path_update",
)


@dataclass(frozen=True)
class DocInventoryRow:
    path: str
    title: str
    purpose: str
    actuality: str
    production_related: str
    status: str
    reason: str
    archive_target: str


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory-first docs cleanup workflow.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Write inventory and manifest without moving files.")
    mode.add_argument("--archive", action="store_true", help="Archive documents marked as archive/delete candidates.")
    mode.add_argument(
        "--delete-archived",
        action="store_true",
        help="Delete files already archived in docs/archive/ according to the manifest.",
    )
    parser.add_argument(
        "--manifest",
        default="",
        help="Manifest CSV path. Default: outputs/reports/cleanup/docs_cleanup_manifest_<timestamp>.csv.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    mode = selected_mode(args)
    manifest_path = resolve_manifest_path(args.manifest)
    rows = build_inventory_rows(include_planned_before_inventory=True)

    write_inventory(BEFORE_INVENTORY_PATH, rows, mode=mode)
    actions = execute_mode(mode, rows, manifest_path)
    write_manifest(manifest_path, rows, actions, mode)

    if mode == "archive":
        after_rows = build_inventory_rows(include_planned_before_inventory=True)
        write_inventory(AFTER_INVENTORY_PATH, after_rows, mode=mode)

    print(f"mode={mode}")
    print(f"documents={len(rows)}")
    print(f"manifest={manifest_path.relative_to(PROJECT_ROOT).as_posix()}")
    print(f"before_inventory={BEFORE_INVENTORY_PATH.relative_to(PROJECT_ROOT).as_posix()}")
    if mode == "archive":
        print(f"after_inventory={AFTER_INVENTORY_PATH.relative_to(PROJECT_ROOT).as_posix()}")
    return 0


def selected_mode(args: argparse.Namespace) -> str:
    if args.archive:
        return "archive"
    if args.delete_archived:
        return "delete-archived"
    return "dry-run"


def resolve_manifest_path(raw_path: str) -> Path:
    if raw_path:
        path = Path(raw_path)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return OUTPUTS_REPORTS_CLEANUP_DIR / f"docs_cleanup_manifest_{timestamp}.csv"


def build_inventory_rows(*, include_planned_before_inventory: bool) -> list[DocInventoryRow]:
    paths = sorted(path for path in DOCS_DIR.rglob("*.md") if path.is_file())
    if include_planned_before_inventory and BEFORE_INVENTORY_PATH not in paths:
        paths.append(BEFORE_INVENTORY_PATH)
    rows = [classify_document(path) for path in sorted(paths)]
    return rows


def classify_document(path: Path) -> DocInventoryRow:
    rel_path = relative_path(path)
    title = extract_title(path)
    name = path.name
    lower = rel_path.lower()

    if rel_path == relative_path(BEFORE_INVENTORY_PATH) or rel_path == relative_path(AFTER_INVENTORY_PATH):
        return row(
            path=rel_path,
            title=title or "Docs cleanup inventory",
            purpose="Inventory-first отчет о состоянии документации перед/после cleanup.",
            actuality="актуальный production-control документ",
            production_related="yes",
            status="keep_active",
            reason="Инвентаризация является обязательным входом для cleanup workflow.",
        )

    if rel_path in ACTIVE_EXACT_PATHS or name in ACTIVE_NAME_HINTS:
        return row(
            path=rel_path,
            title=title,
            purpose=purpose_for_path(rel_path),
            actuality="актуален для production run или project governance",
            production_related="yes",
            status="keep_active",
            reason="Документ входит в активный production/documentation contract.",
        )

    if name in MERGE_CANDIDATE_NAMES:
        return row(
            path=rel_path,
            title=title,
            purpose=purpose_for_path(rel_path),
            actuality="частично актуален; содержит диагностический контекст",
            production_related="indirect",
            status="merge_candidate",
            reason="Диагностический документ может быть объединен с visualization strategy или limitations.",
        )

    if name in ARCHIVE_CANDIDATE_NAMES or lower.startswith(ARCHIVE_DIR_MARKERS) or has_archive_marker(lower):
        return row(
            path=rel_path,
            title=title,
            purpose=purpose_for_path(rel_path),
            actuality="исторический или промежуточный документ",
            production_related="no",
            status="archive_candidate",
            reason="Похоже на modernization/stage/repro/migration/cleanup history, не основной production contract.",
            archive_target=archive_target_for(path),
        )

    return row(
        path=rel_path,
        title=title,
        purpose=purpose_for_path(rel_path),
        actuality="нужна ручная сверка актуальности",
        production_related="indirect",
        status="merge_candidate",
        reason="Не попал в явные active/archive правила; перед переносом требуется ручная проверка.",
    )


def row(
    *,
    path: str,
    title: str,
    purpose: str,
    actuality: str,
    production_related: str,
    status: str,
    reason: str,
    archive_target: str = "",
) -> DocInventoryRow:
    return DocInventoryRow(
        path=path,
        title=title or Path(path).stem.replace("_", " "),
        purpose=purpose,
        actuality=actuality,
        production_related=production_related,
        status=status,
        reason=reason,
        archive_target=archive_target,
    )


def extract_title(path: Path) -> str:
    if not path.exists():
        return path.stem.replace("_", " ")
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip()
            if stripped:
                return stripped[:120]
    except OSError:
        return path.stem.replace("_", " ")
    return path.stem.replace("_", " ")


def purpose_for_path(rel_path: str) -> str:
    if rel_path == "docs/index.md":
        return "Главная карта документации проекта."
    if "/00_project/" in rel_path:
        return "Проектная, governance или production-readiness документация."
    if "/01_methodology/" in rel_path:
        return "Методология KPI, периодов и аналитических показателей."
    if "/02_data_contracts/" in rel_path:
        return "Data contract для воспроизводимых artifacts."
    if "/02_data_pipeline/" in rel_path:
        return "Документация data pipeline и проверок данных."
    if "/03_analytics/" in rel_path:
        return "Аналитические отчеты, таблицы и executive outputs."
    if "/04_visualization/" in rel_path:
        return "Стратегия, ограничения и диагностика визуализаций."
    if "/05_dashboard/" in rel_path:
        return "Dashboard exports и semantic model."
    if "/06_quality/" in rel_path:
        return "QA, reproducibility и manual checks."
    if "/07_operations/" in rel_path:
        return "Операционная документация production-запуска."
    if "/90_archive/" in rel_path or "/archive/" in rel_path:
        return "Исторический, промежуточный или архивный документ."
    return "Документ требует ручной классификации."


def has_archive_marker(lower_rel_path: str) -> bool:
    name = Path(lower_rel_path).name
    return any(marker in name for marker in ARCHIVE_NAME_MARKERS)


def archive_target_for(path: Path) -> str:
    archive_dir = ARCHIVE_ROOT / date.today().isoformat()
    return relative_path(archive_dir / path.name)


def execute_mode(mode: str, rows: Sequence[DocInventoryRow], manifest_path: Path) -> dict[str, str]:
    if mode == "dry-run":
        return {item.path: "planned" if item.status in {"archive_candidate", "delete_candidate"} else "none" for item in rows}
    if mode == "archive":
        return archive_candidates(rows)
    if mode == "delete-archived":
        return delete_archived_from_manifest(manifest_path)
    raise ValueError(f"Unsupported cleanup mode: {mode}")


def archive_candidates(rows: Sequence[DocInventoryRow]) -> dict[str, str]:
    actions: dict[str, str] = {}
    archive_dir = ARCHIVE_ROOT / date.today().isoformat()
    archive_dir.mkdir(parents=True, exist_ok=True)
    for item in rows:
        if item.status not in {"archive_candidate", "delete_candidate"}:
            actions[item.path] = "kept"
            continue
        source = PROJECT_ROOT / item.path
        if not source.exists():
            actions[item.path] = "missing"
            continue
        target = unique_path(archive_dir / source.name)
        assert_inside_docs(target)
        shutil.move(str(source), str(target))
        actions[item.path] = f"archived:{relative_path(target)}"
    return actions


def delete_archived_from_manifest(manifest_path: Path) -> dict[str, str]:
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest for --delete-archived not found: {manifest_path}")
    actions: dict[str, str] = {}
    with manifest_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for record in reader:
            action = record.get("action", "")
            target = record.get("archive_target", "")
            original = record.get("path", "")
            if not action.startswith("archived:") and not target:
                actions[original] = "skipped"
                continue
            archived_path = PROJECT_ROOT / (target or action.removeprefix("archived:"))
            assert_inside_docs_archive(archived_path)
            if archived_path.exists() and archived_path.is_file():
                archived_path.unlink()
                actions[original] = "deleted_archived"
            else:
                actions[original] = "missing_archived"
    return actions


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return path.with_name(f"{path.stem}_{timestamp}{path.suffix}")


def assert_inside_docs(path: Path) -> None:
    resolved = path.resolve()
    docs_resolved = DOCS_DIR.resolve()
    if resolved != docs_resolved and docs_resolved not in resolved.parents:
        raise RuntimeError(f"Refusing to touch path outside docs/: {path}")


def assert_inside_docs_archive(path: Path) -> None:
    resolved = path.resolve()
    archive_resolved = ARCHIVE_ROOT.resolve()
    if archive_resolved not in resolved.parents:
        raise RuntimeError(f"Refusing to delete path outside docs/archive/: {path}")


def write_inventory(path: Path, rows: Sequence[DocInventoryRow], *, mode: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for item in rows:
        counts[item.status] = counts.get(item.status, 0) + 1
    lines = [
        "# Docs inventory before cleanup" if path == BEFORE_INVENTORY_PATH else "# Docs inventory after cleanup",
        "",
        f"- generated_at: `{datetime.now().isoformat(timespec='seconds')}`",
        f"- mode: `{mode}`",
        f"- documents: `{len(rows)}`",
        "",
        "## Summary",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in sorted(counts.items()):
        lines.append(f"| `{status}` | {count} |")
    lines.extend(
        [
            "",
            "## Inventory",
            "",
            "| Path | Title | Назначение | Актуальность | Production run | Status | Reason |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for item in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item.path}`",
                    sanitize_md_cell(item.title),
                    sanitize_md_cell(item.purpose),
                    sanitize_md_cell(item.actuality),
                    item.production_related,
                    f"`{item.status}`",
                    sanitize_md_cell(item.reason),
                ]
            )
            + " |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    manifest_path: Path,
    rows: Sequence[DocInventoryRow],
    actions: dict[str, str],
    mode: str,
) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "mode",
                "path",
                "title",
                "status",
                "production_related",
                "archive_target",
                "action",
                "reason",
            ],
        )
        writer.writeheader()
        for item in rows:
            writer.writerow(
                {
                    "mode": mode,
                    "path": item.path,
                    "title": item.title,
                    "status": item.status,
                    "production_related": item.production_related,
                    "archive_target": item.archive_target,
                    "action": actions.get(item.path, ""),
                    "reason": item.reason,
                }
            )


def sanitize_md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def relative_path(path: Path) -> str:
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
