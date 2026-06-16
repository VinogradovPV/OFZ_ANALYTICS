"""Build an external BI-ready package for OFZ_ANALYTICS generated exports."""

from __future__ import annotations

import argparse
import csv
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

CONFIRM_TOKEN = "BUILD_BI_PACKAGE"
PACKAGE_NAME = "ofz-analytics-bi"
DEFAULT_OUTPUT_DIR = Path("releases") / "bi"
SKIP_NAMES = {".gitkeep"}


@dataclass(frozen=True)
class FileEntry:
    """Source file included in the BI package."""

    category: str
    source_path: Path
    package_path: Path
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class GeneratedTable:
    """Generated BI helper table."""

    category: str
    package_path: Path
    rows: list[dict[str, str]]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an external BI package with dashboard exports, semantic model and BI dimensions."
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
        help="Copy generated exports into the BI package. Required outside dry-run.",
    )
    parser.add_argument("--confirm", default="", help=f"Required outside dry-run: {CONFIRM_TOKEN}")
    return parser.parse_args(argv)


def package_name(args: argparse.Namespace, timestamp: str) -> str:
    return (
        f"ofz_analytics_bi_{args.report_date}_{args.period_type}_{args.aggregation_mode}"
        f"_r{args.retrospective_years}_{timestamp}"
    )


def scope_suffix(args: argparse.Namespace) -> str:
    return f"_{args.period_type}_{args.aggregation_mode}_{args.report_date}_retrospective_{args.retrospective_years}"


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


def iter_files(root: Path, suffixes: tuple[str, ...] | None = None) -> list[Path]:
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


def scoped_csv_files(root: Path, args: argparse.Namespace, prefixes: tuple[str, ...] | None = None) -> list[Path]:
    suffix = scope_suffix(args)
    files = [path for path in iter_files(root, suffixes=(".csv",)) if suffix in path.stem]
    if prefixes is None:
        return files
    return [path for path in files if path.name.startswith(prefixes)]


def entry(project_root: Path, category: str, source_path: Path, package_root: str) -> FileEntry:
    package_path = Path(package_root) / source_path.relative_to(project_root)
    return FileEntry(
        category=category,
        source_path=source_path,
        package_path=package_path,
        size_bytes=source_path.stat().st_size,
        sha256=sha256_file(source_path),
    )


def entries(project_root: Path, category: str, files: Iterable[Path], package_root: str) -> list[FileEntry]:
    return [entry(project_root, category, path, package_root) for path in files]


def collect_categories(project_root: Path, args: argparse.Namespace) -> dict[str, list[FileEntry]]:
    outputs = project_root / "outputs"
    dashboards = outputs / "dashboards"
    analytical_csv = outputs / "exports" / "analytical_csv"
    chart_data = outputs / "exports" / "chart_data"

    semantic_model_files = iter_files(dashboards / "semantic_model_v2", suffixes=(".csv", ".json"))
    dashboard_files = scoped_csv_files(dashboards, args)
    chart_data_files = scoped_csv_files(chart_data, args)
    analytical_files = scoped_csv_files(analytical_csv, args)
    monthly_metrics_files = scoped_csv_files(analytical_csv, args, prefixes=("monthly_metrics_",))
    revenue_files = scoped_csv_files(analytical_csv, args, prefixes=("revenue_",))

    data_dictionary_files = [
        path
        for path in [
            dashboards / "semantic_model_v2" / "field_dictionary.csv",
            *scoped_csv_files(dashboards, args, prefixes=("dashboard_data_dictionary_", "dashboard_monthly_data_dictionary_")),
        ]
        if path.exists()
    ]
    kpi_dictionary_files = [
        path
        for path in [
            dashboards / "semantic_model_v2" / "kpi_dictionary.csv",
            *scoped_csv_files(dashboards, args, prefixes=("dashboard_kpi_summary_",)),
        ]
        if path.exists()
    ]

    return {
        "dashboard_exports": entries(project_root, "dashboard_exports", dashboard_files, "source"),
        "semantic_model_v2": entries(project_root, "semantic_model_v2", semantic_model_files, "source"),
        "analytical_tables_csv": entries(project_root, "analytical_tables_csv", analytical_files, "source"),
        "monthly_metrics_csv": entries(project_root, "monthly_metrics_csv", monthly_metrics_files, "source"),
        "revenue_analytics_csv": entries(project_root, "revenue_analytics_csv", revenue_files, "source"),
        "chart_data_csv": entries(project_root, "chart_data_csv", chart_data_files, "source"),
        "data_dictionary": entries(project_root, "data_dictionary", data_dictionary_files, "source"),
        "kpi_dictionary": entries(project_root, "kpi_dictionary", kpi_dictionary_files, "source"),
    }


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def first_existing(paths: Iterable[Path]) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def dashboard_auction_level_path(project_root: Path, args: argparse.Namespace) -> Path | None:
    dashboards = project_root / "outputs" / "dashboards"
    suffix = scope_suffix(args)
    return first_existing(
        [
            dashboards / "monthly" / f"dashboard_auction_level{suffix}.csv",
            dashboards / f"dashboard_auction_level{suffix}.csv",
        ]
    )


def monthly_metrics_path(project_root: Path, args: argparse.Namespace) -> Path | None:
    analytical = project_root / "outputs" / "exports" / "analytical_csv"
    return analytical / f"monthly_metrics{scope_suffix(args)}.csv"


def generated_tables(project_root: Path, args: argparse.Namespace) -> tuple[list[GeneratedTable], list[str]]:
    missing: list[str] = []
    auction_path = dashboard_auction_level_path(project_root, args)
    monthly_path = monthly_metrics_path(project_root, args)
    tables: list[GeneratedTable] = []

    if auction_path is None:
        missing.extend(["ofz_type_dimension_source", "placement_format_dimension_source"])
    else:
        auction_rows = read_csv_rows(auction_path)
        tables.append(
            GeneratedTable(
                category="ofz_type_dimension",
                package_path=Path("dimensions") / "ofz_type_dimension.csv",
                rows=build_ofz_type_dimension(auction_rows),
            )
        )
        tables.append(
            GeneratedTable(
                category="placement_format_dimension",
                package_path=Path("dimensions") / "placement_format_dimension.csv",
                rows=build_placement_format_dimension(auction_rows),
            )
        )

    if monthly_path is None or not monthly_path.exists():
        missing.append("period_dimension_source")
    else:
        tables.append(
            GeneratedTable(
                category="period_dimension",
                package_path=Path("dimensions") / "period_dimension.csv",
                rows=build_period_dimension(read_csv_rows(monthly_path), args),
            )
        )

    tables.append(
        GeneratedTable(
            category="bi_readme",
            package_path=Path("README.md"),
            rows=[],
        )
    )
    return tables, missing


def unique_sorted(values: Iterable[str]) -> list[str]:
    return sorted({str(value).strip() for value in values if str(value).strip()})


def build_ofz_type_dimension(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    values = unique_sorted(row.get("ofz_type", "") for row in rows)
    return [{"ofz_type": value, "display_name_ru": value} for value in values]


def build_placement_format_dimension(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    values = unique_sorted(row.get("format", "") for row in rows)
    return [{"format": value, "display_name_ru": value} for value in values]


def build_period_dimension(rows: list[dict[str, str]], args: argparse.Namespace) -> list[dict[str, str]]:
    seen: dict[str, dict[str, str]] = {}
    for row in rows:
        label = row.get("report_period_label", "").strip()
        if not label:
            continue
        key = "|".join([str(row.get("report_year", "")), str(row.get("month", "")), label])
        seen[key] = {
            "report_year": row.get("report_year", ""),
            "month": row.get("month", ""),
            "month_number": row.get("month_number", ""),
            "month_label": row.get("month_label", ""),
            "month_start": row.get("month_start", ""),
            "month_end": row.get("month_end", ""),
            "report_period_label": label,
            "period_type": args.period_type,
            "aggregation_mode": args.aggregation_mode,
            "is_target_year": row.get("is_target_year", ""),
        }
    return [seen[key] for key in sorted(seen)]


def raw_file_hashes(project_root: Path) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    raw_root = project_root / "data" / "raw"
    for path in iter_files(raw_root):
        rows.append(
            {
                "path": path.relative_to(project_root).as_posix(),
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


def required_missing(
    categories: dict[str, list[FileEntry]],
    generated: list[GeneratedTable],
    generated_missing: list[str],
) -> list[str]:
    required_categories = [
        "dashboard_exports",
        "semantic_model_v2",
        "analytical_tables_csv",
        "monthly_metrics_csv",
        "revenue_analytics_csv",
        "chart_data_csv",
        "data_dictionary",
        "kpi_dictionary",
    ]
    missing = [name for name in required_categories if not categories.get(name)]
    generated_categories = {table.category for table in generated}
    for required in ("period_dimension", "ofz_type_dimension", "placement_format_dimension"):
        if required not in generated_categories:
            missing.append(required)
    missing.extend(generated_missing)
    return sorted(set(missing))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bi_readme(args: argparse.Namespace, manifest: dict[str, object]) -> str:
    return "\n".join(
        [
            "# OFZ_ANALYTICS BI package",
            "",
            "This package is an external generated artifact for BI consumers.",
            "",
            f"- Report date: `{args.report_date}`",
            f"- Period type: `{args.period_type}`",
            f"- Aggregation mode: `{args.aggregation_mode}`",
            f"- Retrospective years: `{args.retrospective_years}`",
            f"- Git commit: `{manifest['git_commit_hash']}`",
            "",
            "## Contents",
            "",
            "- `source/outputs/dashboards/`: dashboard-ready CSV/JSON exports.",
            "- `source/outputs/dashboards/semantic_model_v2/`: semantic model v2 dictionaries and measures.",
            "- `source/outputs/exports/analytical_csv/`: analytical, monthly and revenue CSV exports.",
            "- `source/outputs/exports/chart_data/`: chart data CSV exports.",
            "- `dimensions/`: BI helper dimensions generated from dashboard exports.",
            "- `bi_manifest.json` and `bi_manifest.md`: audit manifest with hashes.",
            "",
            "Generated BI package files are not committed to Git.",
            "",
        ]
    )


def build_manifest(
    project_root: Path,
    args: argparse.Namespace,
    categories: dict[str, list[FileEntry]],
    generated: list[GeneratedTable],
    timestamp: str,
    package_dir: Path,
    missing: list[str],
) -> dict[str, object]:
    git_status = run_git(["status", "--short"], project_root)
    included_files = [
        {
            "category": entry.category,
            "path": entry.package_path.as_posix(),
            "source_path": entry.source_path.relative_to(project_root).as_posix(),
            "size_bytes": entry.size_bytes,
            "sha256": entry.sha256,
        }
        for entries_list in categories.values()
        for entry in entries_list
    ]
    generated_files = [
        {
            "category": table.category,
            "path": table.package_path.as_posix(),
            "row_count": len(table.rows),
        }
        for table in generated
    ]
    return {
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
        "package_dir": str(package_dir),
        "raw_data_file_hashes": raw_file_hashes(project_root),
        "included_files": included_files,
        "generated_files": generated_files,
        "included_file_count": len(included_files),
        "included_total_size_bytes": sum(int(entry["size_bytes"]) for entry in included_files),
        "missing_required_items": missing,
    }


def manifest_markdown(manifest: dict[str, object]) -> str:
    missing_raw = manifest.get("missing_required_items")
    missing = [str(item) for item in missing_raw] if isinstance(missing_raw, list) else []
    included_raw = manifest.get("included_files")
    included = included_raw if isinstance(included_raw, list) else []
    generated_raw = manifest.get("generated_files")
    generated = generated_raw if isinstance(generated_raw, list) else []
    lines = [
        "# OFZ_ANALYTICS BI manifest",
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
        f"- Included source files: `{manifest['included_file_count']}`",
        f"- Included total size bytes: `{manifest['included_total_size_bytes']}`",
        "",
        "## Missing required items",
        "",
    ]
    lines.extend(f"- `{item}`" for item in missing) if missing else lines.append("- none")
    lines.extend(["", "## Generated BI tables", ""])
    for item in generated:
        if isinstance(item, dict):
            lines.append(f"- `{item['path']}` ({item['category']}, rows: `{item['row_count']}`)")
    lines.extend(["", "## Included source files", ""])
    for item in included:
        if isinstance(item, dict):
            lines.append(
                f"- `{item['path']}` ({item['category']}, source `{item['source_path']}`, sha256 `{item['sha256']}`)"
            )
    return "\n".join(lines) + "\n"


def copy_entries(package_dir: Path, entries_iter: Iterable[FileEntry]) -> None:
    for item in entries_iter:
        target = package_dir / item.package_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item.source_path, target)


def write_generated_tables(package_dir: Path, generated: list[GeneratedTable], manifest: dict[str, object], args: argparse.Namespace) -> None:
    for table in generated:
        target = package_dir / table.package_path
        if table.category == "bi_readme":
            target.write_text(bi_readme(args, manifest), encoding="utf-8")
        else:
            write_csv(target, table.rows)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    project_root = Path.cwd()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_dir = Path(args.output_dir) / package_name(args, timestamp)

    categories = collect_categories(project_root, args)
    generated, generated_missing = generated_tables(project_root, args)
    missing = required_missing(categories, generated, generated_missing)
    manifest = build_manifest(project_root, args, categories, generated, timestamp, package_dir, missing)

    print(f"BI package target: {package_dir}")
    for name, items in categories.items():
        print(f"{name}: {len(items)} files")
    for table in generated:
        print(f"{table.category}: {len(table.rows)} rows")
    if missing:
        print("Missing required items: " + ", ".join(missing))

    if args.dry_run:
        print("Dry-run only: no files were written.")
        return 0

    if not args.include_outputs:
        print("Build mode requires --include-outputs.", file=sys.stderr)
        return 2
    if args.confirm != CONFIRM_TOKEN:
        print(f"Build mode requires --confirm {CONFIRM_TOKEN}.", file=sys.stderr)
        return 2
    if missing:
        print("BI package was not created because required outputs are missing.", file=sys.stderr)
        return 2

    package_dir.mkdir(parents=True, exist_ok=False)
    for entries_list in categories.values():
        copy_entries(package_dir, entries_list)
    write_generated_tables(package_dir, generated, manifest, args)
    (package_dir / "bi_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (package_dir / "bi_manifest.md").write_text(manifest_markdown(manifest), encoding="utf-8")
    print(f"BI package created: {package_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
