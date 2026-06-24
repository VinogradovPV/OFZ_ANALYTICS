"""Smoke checks for hardened pipeline telemetry scope counters."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import config  # noqa: E402


REQUIRED_TOP_LEVEL_FIELDS = {
    "raw_file_scope_counts",
    "generated_file_scope_counts",
    "raw_active_files_count",
    "raw_versions_files_count",
    "generated_current_files_count",
    "generated_archive_files_count",
    "generated_tmp_cache_files_count",
    "stage_durations",
}


def main() -> int:
    telemetry_path = latest_telemetry_json()
    data = json.loads(telemetry_path.read_text(encoding="utf-8"))

    missing = sorted(REQUIRED_TOP_LEVEL_FIELDS - set(data))
    assert not missing, f"missing telemetry fields: {missing}"

    raw_counts = data["raw_file_scope_counts"]
    generated_counts = data["generated_file_scope_counts"]
    assert data["raw_active_files_count"] == raw_counts["active"]
    assert data["raw_versions_files_count"] == raw_counts["versions"]
    assert data["generated_current_files_count"] == generated_counts["current"]
    assert data["generated_archive_files_count"] == generated_counts["archive"]
    assert data["generated_tmp_cache_files_count"] == generated_counts["tmp_cache"]

    expected_raw = count_raw_scopes()
    assert raw_counts == expected_raw, f"raw scope mismatch: telemetry={raw_counts}, expected={expected_raw}"
    assert raw_counts["active"] + raw_counts["versions"] + raw_counts["registry"] == raw_counts["total"]

    expected_generated = count_generated_scopes()
    assert generated_counts["archive"] == expected_generated["archive"], (
        f"archive scope mismatch: telemetry={generated_counts}, expected={expected_generated}"
    )
    assert generated_counts["tmp_cache"] == expected_generated["tmp_cache"], (
        f"tmp/cache scope mismatch: telemetry={generated_counts}, expected={expected_generated}"
    )
    assert expected_generated["current"] >= generated_counts["current"], (
        f"current output count cannot shrink after telemetry write: telemetry={generated_counts}, "
        f"filesystem={expected_generated}"
    )
    assert sum(generated_counts.values()) == data["generated_artifacts_count"]

    stages = data.get("stage_durations") or []
    assert stages, "stage_durations must not be empty"
    for stage in stages:
        duration = stage.get("duration_seconds")
        precise = stage.get("stage_duration_seconds_precise")
        assert_number(duration, f"duration_seconds for {stage.get('code')}")
        assert_number(precise, f"stage_duration_seconds_precise for {stage.get('code')}")
        assert precise >= 0
        assert duration >= 0

    print(f"Telemetry smoke OK: {telemetry_path.relative_to(PROJECT_ROOT).as_posix()}")
    print(f"raw_file_scope_counts={raw_counts}")
    print(f"generated_file_scope_counts={generated_counts}")
    return 0


def latest_telemetry_json() -> Path:
    telemetry_dir = config.REPORTS_DIR / "telemetry"
    candidates = sorted(telemetry_dir.glob("telemetry_*.json"), key=lambda path: path.stat().st_mtime)
    if not candidates:
        raise AssertionError(f"No telemetry JSON files found under {telemetry_dir}")
    return candidates[-1]


def count_raw_scopes() -> dict[str, int]:
    counts = {
        "active": 0,
        "versions": 0,
        "registry": 0,
        "latest": 0,
        "final": 0,
        "other": 0,
        "total": 0,
    }
    if not config.RAW_DATA_DIR.exists():
        return counts

    for path in sorted(item for item in config.RAW_DATA_DIR.rglob("*") if item.is_file() and item.name != ".gitkeep"):
        parts = path.relative_to(config.RAW_DATA_DIR).parts
        counts["total"] += 1
        if "versions" in parts:
            counts["versions"] += 1
        elif "registry" in parts:
            counts["registry"] += 1
        else:
            counts["active"] += 1
            if "latest" in parts:
                counts["latest"] += 1
            elif "final" in parts:
                counts["final"] += 1
            else:
                counts["other"] += 1
    return counts


def count_generated_scopes() -> dict[str, int]:
    counts = {"current": 0, "archive": 0, "tmp_cache": 0}
    if not config.OUTPUTS_DIR.exists():
        return counts

    for path in sorted(item for item in config.OUTPUTS_DIR.rglob("*") if item.is_file() and item.name != ".gitkeep"):
        rel = path.relative_to(config.PROJECT_ROOT).as_posix()
        if rel.startswith("outputs/archive/"):
            counts["archive"] += 1
        elif rel.startswith(("outputs/tmp/", "outputs/cache/")):
            counts["tmp_cache"] += 1
        else:
            counts["current"] += 1
    return counts


def assert_number(value: Any, label: str) -> None:
    assert isinstance(value, (int, float)), f"{label} must be numeric, got {type(value).__name__}"


if __name__ == "__main__":
    raise SystemExit(main())
