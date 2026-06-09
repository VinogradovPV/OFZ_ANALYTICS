"""Pipeline telemetry writer for OFZ_ANALYTICS production runs."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any, Sequence

from scripts import config

TELEMETRY_DIR = config.REPORTS_DIR / "telemetry"


@dataclass
class StageTelemetry:
    """Runtime telemetry for one pipeline stage."""

    code: str
    name: str
    started_at: str
    finished_at: str = ""
    duration_seconds: float = 0.0
    status: str = "running"
    returncode: int | None = None
    error: str = ""


@dataclass
class PipelineTelemetry:
    """In-memory telemetry accumulator."""

    run_id: str
    started_at: str
    report_date: str | None
    period_type: str | None
    aggregation_mode: str
    retrospective_years: int | None
    stages_requested: list[str]
    cleanup_mode: str
    git_commit: str
    git_dirty_flag: bool
    _start_perf: float = field(default_factory=perf_counter)
    stage_durations: list[StageTelemetry] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class TelemetryPaths:
    """Written telemetry paths."""

    json_path: Path
    markdown_path: Path


def start_pipeline_telemetry(args: Any) -> PipelineTelemetry:
    """Create a telemetry accumulator from run_pipeline args."""
    started_at = utc_now()
    run_id = build_run_id(started_at, args)
    git_status = git_output(["status", "--short"])
    cleanup_mode = ",".join(
        item
        for item in [
            env_value("OFZ_INTERACTIVE_CLEANUP_STATUS"),
            env_value("OFZ_INTERACTIVE_CLEANUP_MODE"),
        ]
        if item
    )
    return PipelineTelemetry(
        run_id=run_id,
        started_at=started_at,
        report_date=args.report_date,
        period_type=args.period_type,
        aggregation_mode=args.aggregation_mode,
        retrospective_years=args.retrospective_years,
        stages_requested=list(args.stages),
        cleanup_mode=cleanup_mode or "not_requested",
        git_commit=git_output(["rev-parse", "HEAD"]) or "unknown",
        git_dirty_flag=bool(git_status),
    )


def start_stage(run: PipelineTelemetry, code: str, name: str) -> StageTelemetry:
    """Start stage timer."""
    stage = StageTelemetry(code=code, name=name, started_at=utc_now())
    run.stage_durations.append(stage)
    return stage


def finish_stage(stage: StageTelemetry, status: str, error: str = "", returncode: int | None = None) -> None:
    """Finish stage timer."""
    stage.finished_at = utc_now()
    stage.status = status
    stage.error = error
    stage.returncode = returncode
    start = datetime.fromisoformat(stage.started_at.replace("Z", "+00:00"))
    finish = datetime.fromisoformat(stage.finished_at.replace("Z", "+00:00"))
    stage.duration_seconds = round((finish - start).total_seconds(), 3)


def write_pipeline_telemetry(
    run: PipelineTelemetry,
    status: str,
    quality_gate_results: dict[str, str] | None = None,
    schema_validation_results: dict[str, str] | None = None,
    extra_warnings: Sequence[str] | None = None,
    extra_errors: Sequence[str] | None = None,
) -> TelemetryPaths:
    """Write telemetry JSON and Markdown under outputs/reports/telemetry."""
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
    finished_at = utc_now()
    if extra_warnings:
        run.warnings.extend(str(item) for item in extra_warnings)
    if extra_errors:
        run.errors.extend(str(item) for item in extra_errors)

    artifacts = collect_artifacts(config.OUTPUTS_DIR)
    data = {
        "schema_version": "pipeline_telemetry_v1",
        "run_id": run.run_id,
        "status": status,
        "started_at": run.started_at,
        "finished_at": finished_at,
        "duration_seconds": round(perf_counter() - run._start_perf, 3),
        "stage_durations": [stage.__dict__ for stage in run.stage_durations],
        "input_row_counts": input_row_counts(),
        "output_file_counts": output_file_counts(),
        "generated_artifacts_count": len(artifacts),
        "artifacts_total_size": sum(int(item["size_bytes"]) for item in artifacts),
        "artifacts_total_size_bytes": sum(int(item["size_bytes"]) for item in artifacts),
        "warnings_count": len(run.warnings),
        "errors_count": len(run.errors),
        "warnings": run.warnings,
        "errors": run.errors,
        "cleanup_mode": run.cleanup_mode,
        "quality_gate_results": quality_gate_results or infer_quality_gate_results(),
        "schema_validation_results": schema_validation_results or infer_schema_validation_results(),
        "git_commit": run.git_commit,
        "git_dirty_flag": run.git_dirty_flag,
        "raw_data_hashes": raw_data_hashes(),
        "report_date": run.report_date,
        "period_type": run.period_type,
        "aggregation_mode": run.aggregation_mode,
        "retrospective_years": run.retrospective_years,
        "stages_requested": run.stages_requested,
    }

    json_path = TELEMETRY_DIR / f"telemetry_{run.run_id}.json"
    md_path = TELEMETRY_DIR / f"telemetry_{run.run_id}.md"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(data), encoding="utf-8")
    return TelemetryPaths(json_path=json_path, markdown_path=md_path)


def collect_artifacts(root: Path) -> list[dict[str, Any]]:
    """Collect generated artifact metadata under outputs."""
    if not root.exists():
        return []
    artifacts: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != ".gitkeep":
            artifacts.append(
                {
                    "path": relative_path(path),
                    "size_bytes": path.stat().st_size,
                    "modified_at": datetime.fromtimestamp(path.stat().st_mtime).replace(microsecond=0).isoformat(),
                }
            )
    return artifacts


def output_file_counts() -> dict[str, int]:
    """Count output files by top-level generated area."""
    areas = {
        "charts": config.CHARTS_DIR,
        "exports": config.EXPORTS_DIR,
        "reports": config.REPORTS_DIR,
        "dashboards": config.DASHBOARDS_DIR,
        "archive": config.ARCHIVE_DIR,
    }
    return {name: count_files(path) for name, path in areas.items()}


def input_row_counts() -> dict[str, int | None]:
    """Count rows for common input/processed CSV files when available."""
    candidates = {
        "raw_files": config.RAW_DATA_DIR,
        "ofz_auctions_clean": config.PROCESSED_DATA_DIR / "ofz_auctions_clean.csv",
        "ofz_auctions_features": config.PROCESSED_DATA_DIR / "ofz_auctions_features.csv",
        "ofz_auctions_report_scope": config.OFZ_AUCTIONS_REPORT_SCOPE_CSV,
        "ofz_monthly_metrics": config.PROCESSED_DATA_DIR / "ofz_monthly_metrics.csv",
    }
    rows: dict[str, int | None] = {}
    for name, path in candidates.items():
        if path.is_dir():
            rows[name] = count_files(path)
        elif path.exists():
            rows[name] = count_csv_rows(path)
        else:
            rows[name] = None
    return rows


def count_csv_rows(path: Path) -> int:
    """Count CSV rows excluding header."""
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream)
        count = sum(1 for _row in reader)
    return max(0, count - 1)


def count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file() and item.name != ".gitkeep")


def raw_data_hashes() -> list[dict[str, Any]]:
    """Return raw data SHA256 hashes."""
    records: list[dict[str, Any]] = []
    if not config.RAW_DATA_DIR.exists():
        return records
    for path in sorted(item for item in config.RAW_DATA_DIR.rglob("*") if item.is_file()):
        records.append({"path": relative_path(path), "size_bytes": path.stat().st_size, "sha256": sha256_file(path)})
    return records


def infer_quality_gate_results() -> dict[str, str]:
    report = config.DOCS_QUALITY_DIR / "quality_gate_report.md"
    return {"latest_report": status_from_report(report)}


def infer_schema_validation_results() -> dict[str, str]:
    report = config.DOCS_DATA_PIPELINE_DIR / "schema_validation_report.md"
    return {"latest_report": status_from_report(report)}


def status_from_report(path: Path) -> str:
    if not path.exists():
        return "report_missing"
    text = path.read_text(encoding="utf-8", errors="replace").lower()
    if "fail" in text or "failed" in text:
        return "review_required"
    if "ok" in text or "passed" in text:
        return "ok"
    return "report_exists"


def render_markdown(data: dict[str, Any]) -> str:
    """Render telemetry summary markdown."""
    lines = [
        "# Pipeline telemetry",
        "",
        f"- `run_id`: `{data['run_id']}`",
        f"- `status`: `{data['status']}`",
        f"- `started_at`: `{data['started_at']}`",
        f"- `finished_at`: `{data['finished_at']}`",
        f"- `duration_seconds`: `{data['duration_seconds']}`",
        f"- `git_commit`: `{data['git_commit']}`",
        f"- `git_dirty_flag`: `{data['git_dirty_flag']}`",
        f"- `cleanup_mode`: `{data['cleanup_mode']}`",
        f"- `generated_artifacts_count`: `{data['generated_artifacts_count']}`",
        f"- `artifacts_total_size_bytes`: `{data['artifacts_total_size_bytes']}`",
        f"- `warnings_count`: `{data['warnings_count']}`",
        f"- `errors_count`: `{data['errors_count']}`",
        "",
        "## Stage durations",
        "",
        "| Stage | Status | Duration, sec |",
        "| --- | --- | ---: |",
    ]
    for stage in data.get("stage_durations", []):
        lines.append(f"| `{stage['code']}` {stage['name']} | `{stage['status']}` | {stage['duration_seconds']} |")

    lines.extend(["", "## Output file counts", "", "| Area | Files |", "| --- | ---: |"])
    for area, count in sorted((data.get("output_file_counts") or {}).items()):
        lines.append(f"| `{area}` | {count} |")

    lines.extend(["", "## Input row counts", "", "| Dataset | Rows/files |", "| --- | ---: |"])
    for name, count in sorted((data.get("input_row_counts") or {}).items()):
        lines.append(f"| `{name}` | {'' if count is None else count} |")

    lines.extend(["", "## Warnings", ""])
    warnings = data.get("warnings") or []
    lines.extend([f"- {item}" for item in warnings] if warnings else ["- none"])
    lines.extend(["", "## Errors", ""])
    errors = data.get("errors") or []
    lines.extend([f"- {item}" for item in errors] if errors else ["- none"])
    return "\n".join(lines) + "\n"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_run_id(started_at: str, args: Any) -> str:
    seed = "|".join(
        [
            started_at,
            str(args.report_date),
            str(args.period_type),
            str(args.aggregation_mode),
            str(args.retrospective_years),
            ",".join(args.stages),
        ]
    )
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8]
    safe_timestamp = started_at.replace("-", "").replace(":", "").replace("Z", "").replace("T", "_")
    return f"{safe_timestamp}_{digest}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def git_output(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=config.PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def env_value(name: str) -> str:
    import os

    return os.environ.get(name, "").strip()


def relative_path(path: Path) -> str:
    try:
        return path.relative_to(config.PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    """Small CLI for inspecting the latest telemetry directory."""
    print(TELEMETRY_DIR.relative_to(config.PROJECT_ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
