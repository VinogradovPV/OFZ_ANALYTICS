"""Build an external release bundle for generated OFZ_ANALYTICS artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

CONFIRM_TOKEN = "BUILD_RELEASE_BUNDLE"
PACKAGE_NAME = "ofz-analytics"
DEFAULT_OUTPUT_DIR = Path("releases")
SKIP_NAMES = {".gitkeep"}


@dataclass(frozen=True)
class FileEntry:
    category: str
    source_path: Path
    relative_path: Path
    size_bytes: int
    sha256: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build an external release bundle with HTML charts, chart data, "
            "dashboards, manifests and QA reports. Dry-run does not write files."
        )
    )
    parser.add_argument("--report-date", required=True)
    parser.add_argument("--retrospective-years", required=True, type=int)
    parser.add_argument("--period-type", required=True, choices=["month", "quarter", "year"])
    parser.add_argument("--aggregation-mode", required=True, choices=["cumulative", "point"])
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--include-outputs",
        action="store_true",
        help="Copy generated outputs into the bundle. Required outside dry-run.",
    )
    parser.add_argument(
        "--confirm",
        default="",
        help=f"Required outside dry-run: {CONFIRM_TOKEN}",
    )
    return parser.parse_args(argv)


def run_git(args: list[str], project_root: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_files(root: Path, suffixes: tuple[str, ...] | None = None) -> Iterable[Path]:
    if not root.exists():
        return []
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.name in SKIP_NAMES:
            continue
        if suffixes and path.suffix.lower() not in suffixes:
            continue
        files.append(path)
    return sorted(files)


def matching_files(root: Path, patterns: list[str]) -> list[Path]:
    files: list[Path] = []
    for pattern in patterns:
        files.extend(path for path in root.glob(pattern) if path.is_file() and path.name not in SKIP_NAMES)
    return sorted(set(files))


def file_entries(project_root: Path, category: str, paths: Iterable[Path]) -> list[FileEntry]:
    entries: list[FileEntry] = []
    for source_path in paths:
        relative_path = source_path.relative_to(project_root)
        entries.append(
            FileEntry(
                category=category,
                source_path=source_path,
                relative_path=relative_path,
                size_bytes=source_path.stat().st_size,
                sha256=sha256_file(source_path),
            )
        )
    return entries


def collect_files(project_root: Path) -> dict[str, list[FileEntry]]:
    outputs = project_root / "outputs"
    docs = project_root / "docs"

    categories = {
        "html_charts": file_entries(
            project_root,
            "html_charts",
            iter_files(outputs / "charts", suffixes=(".html", ".md")),
        ),
        "chart_data_csv": file_entries(
            project_root,
            "chart_data_csv",
            iter_files(outputs / "exports", suffixes=(".csv", ".json", ".xlsx")),
        ),
        "dashboard_exports": file_entries(
            project_root,
            "dashboard_exports",
            iter_files(outputs / "dashboards"),
        ),
        "run_manifests": file_entries(
            project_root,
            "run_manifests",
            matching_files(outputs / "reports", ["run_manifest_*.json", "run_manifest_*.md", "run_manifests/*"]),
        ),
        "qa_reports": file_entries(
            project_root,
            "qa_reports",
            [
                *matching_files(outputs / "reports", ["quality_gate_report_*", "visual_regression/*"]),
                *matching_files(docs / "06_quality", ["*.md"]),
            ],
        ),
        "executive_summary": file_entries(
            project_root,
            "executive_summary",
            [
                *matching_files(outputs / "reports", ["executive_summary_*", "executive_summary/*"]),
                *matching_files(docs / "03_analytics", ["executive_summary*.md"]),
            ],
        ),
        "data_quality_summary": file_entries(
            project_root,
            "data_quality_summary",
            [
                *matching_files(outputs / "reports", ["data_quality/*"]),
                *matching_files(docs / "02_data_pipeline", ["*quality*.md", "*data*.md"]),
            ],
        ),
        "telemetry_summary": file_entries(
            project_root,
            "telemetry_summary",
            matching_files(outputs / "reports", ["telemetry/*", "*telemetry*"]),
        ),
    }
    return categories


def raw_file_hashes(project_root: Path) -> list[dict[str, str | int]]:
    raw_root = project_root / "data" / "raw"
    rows: list[dict[str, str | int]] = []
    for path in iter_files(raw_root):
        rows.append(
            {
                "path": str(path.relative_to(project_root)).replace("\\", "/"),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return rows


def read_project_version(project_root: Path) -> str:
    pyproject = project_root / "pyproject.toml"
    if not pyproject.exists():
        return "unknown"
    for line in pyproject.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("version"):
            return stripped.split("=", 1)[1].strip().strip('"')
    return "unknown"


def summarize_quality(project_root: Path) -> dict[str, str]:
    quality_report = project_root / "docs" / "06_quality" / "quality_gate_report.md"
    schema_report = project_root / "docs" / "06_quality" / "schema_validation_report.md"
    visual_report = project_root / "docs" / "06_quality" / "visual_regression_report.md"

    def status_from_file(path: Path) -> str:
        if not path.exists():
            return "report_missing"
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        if "fail" in text or "failed" in text:
            return "review_required"
        if "ok" in text or "passed" in text:
            return "ok"
        return "report_exists"

    visual_mode = "report_missing"
    if visual_report.exists():
        text = visual_report.read_text(encoding="utf-8", errors="replace").lower()
        visual_mode = "fallback_static_html_or_plotly_json" if "fallback" in text else "report_exists"

    return {
        "quality_gate_status": status_from_file(quality_report),
        "schema_validation_status": status_from_file(schema_report),
        "visual_regression_mode": visual_mode,
    }


def warning_summary(project_root: Path) -> list[str]:
    candidates = [
        project_root / "docs" / "06_quality" / "manual_checks_log.md",
        project_root / "docs" / "06_quality" / "anomaly_tests_report.md",
        project_root / "docs" / "06_quality" / "visual_regression_report.md",
    ]
    warnings: list[str] = []
    for path in candidates:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if "warning" in line.lower() or "предупреж" in line.lower():
                warnings.append(f"{path.relative_to(project_root)}: {line.strip()[:300]}")
    return warnings[:50]


def bundle_name(args: argparse.Namespace, timestamp: str) -> str:
    return (
        f"ofz_analytics_{args.report_date}_{args.period_type}_{args.aggregation_mode}"
        f"_retrospective_{args.retrospective_years}_{timestamp}"
    )


def build_manifest(
    project_root: Path,
    args: argparse.Namespace,
    categories: dict[str, list[FileEntry]],
    timestamp: str,
    bundle_dir: Path,
    missing_required: list[str],
) -> dict[str, object]:
    git_status = run_git(["status", "--short"], project_root)
    included = [
        {
            "category": entry.category,
            "path": str(entry.relative_path).replace("\\", "/"),
            "size_bytes": entry.size_bytes,
            "sha256": entry.sha256,
        }
        for entries in categories.values()
        for entry in entries
    ]
    manifest: dict[str, object] = {
        "package_name": PACKAGE_NAME,
        "package_version": read_project_version(project_root),
        "git_commit_hash": run_git(["rev-parse", "HEAD"], project_root) or "unknown",
        "git_branch": run_git(["branch", "--show-current"], project_root) or "unknown",
        "git_dirty_flag": bool(git_status),
        "git_status_short": git_status,
        "report_date": args.report_date,
        "period_type": args.period_type,
        "aggregation_mode": args.aggregation_mode,
        "retrospective_years": args.retrospective_years,
        "generated_timestamp": timestamp,
        "python_version": platform.python_version(),
        "cli_command": " ".join(sys.argv),
        "bundle_dir": str(bundle_dir),
        "raw_data_file_hashes": raw_file_hashes(project_root),
        "included_files": included,
        "included_file_count": len(included),
        "included_total_size_bytes": sum(entry["size_bytes"] for entry in included),
        "missing_required_categories": missing_required,
        "warning_summary": warning_summary(project_root),
        **summarize_quality(project_root),
    }
    return manifest


def manifest_markdown(manifest: dict[str, object]) -> str:
    lines = [
        "# OFZ_ANALYTICS release manifest",
        "",
        f"- Package: `{manifest['package_name']}`",
        f"- Version: `{manifest['package_version']}`",
        f"- Git commit: `{manifest['git_commit_hash']}`",
        f"- Branch: `{manifest['git_branch']}`",
        f"- Dirty flag: `{manifest['git_dirty_flag']}`",
        f"- Report date: `{manifest['report_date']}`",
        f"- Period type: `{manifest['period_type']}`",
        f"- Aggregation mode: `{manifest['aggregation_mode']}`",
        f"- Retrospective years: `{manifest['retrospective_years']}`",
        f"- Generated timestamp: `{manifest['generated_timestamp']}`",
        f"- Python version: `{manifest['python_version']}`",
        f"- Quality gate status: `{manifest['quality_gate_status']}`",
        f"- Schema validation status: `{manifest['schema_validation_status']}`",
        f"- Visual regression mode: `{manifest['visual_regression_mode']}`",
        f"- Included files: `{manifest['included_file_count']}`",
        f"- Included total size bytes: `{manifest['included_total_size_bytes']}`",
        "",
        "## Missing required categories",
        "",
    ]
    missing = manifest.get("missing_required_categories") or []
    if missing:
        lines.extend(f"- `{item}`" for item in missing)
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    warnings = manifest.get("warning_summary") or []
    if warnings:
        lines.extend(f"- {item}" for item in warnings)
    else:
        lines.append("- none")
    lines.extend(["", "## Included files", ""])
    for entry in manifest.get("included_files", []):
        if isinstance(entry, dict):
            lines.append(
                f"- `{entry['path']}` ({entry['category']}, {entry['size_bytes']} bytes, sha256 `{entry['sha256']}`)"
            )
    return "\n".join(lines) + "\n"


def copy_entries(bundle_dir: Path, entries: Iterable[FileEntry]) -> None:
    for entry in entries:
        target = bundle_dir / entry.relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(entry.source_path, target)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    project_root = Path.cwd()
    output_dir = Path(args.output_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bundle_dir = output_dir / bundle_name(args, timestamp)

    categories = collect_files(project_root)
    required_categories = [
        "html_charts",
        "chart_data_csv",
        "dashboard_exports",
        "run_manifests",
        "qa_reports",
        "executive_summary",
    ]
    missing_required = [name for name in required_categories if not categories.get(name)]
    manifest = build_manifest(project_root, args, categories, timestamp, bundle_dir, missing_required)

    print(f"Release bundle target: {bundle_dir}")
    for name, entries in categories.items():
        print(f"{name}: {len(entries)} files")
    if missing_required:
        print("Missing required categories: " + ", ".join(missing_required))

    if args.dry_run:
        print("Dry-run only: no files were written.")
        return 0

    if not args.include_outputs:
        print("Release mode requires --include-outputs.", file=sys.stderr)
        return 2
    if args.confirm != CONFIRM_TOKEN:
        print(f"Release mode requires --confirm {CONFIRM_TOKEN}.", file=sys.stderr)
        return 2
    if missing_required:
        print("Release bundle was not created because required outputs are missing.", file=sys.stderr)
        return 2

    bundle_dir.mkdir(parents=True, exist_ok=False)
    for entries in categories.values():
        copy_entries(bundle_dir, entries)
    (bundle_dir / "release_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (bundle_dir / "release_manifest.md").write_text(manifest_markdown(manifest), encoding="utf-8")
    print(f"Release bundle created: {bundle_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
