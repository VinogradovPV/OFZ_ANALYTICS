"""Smoke tests for the Bank of Russia raw key rate status reader."""

from __future__ import annotations

import csv
import json
import shutil
import sys
import uuid
from datetime import UTC, date, datetime
from pathlib import Path

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.gui_launcher.state import check_cbr_raw_status  # noqa: E402
from scripts.reference_data.cbr_key_rate import (  # noqa: E402
    KeyRateObservation,
    build_cbr_key_rate_url,
    build_metadata,
    make_daily_frame,
    parse_cbr_key_rate_html,
    write_raw_outputs,
)


ROOT = Path(__file__).resolve().parents[2]
TEMP_ROOT = ROOT / "outputs" / "tmp"
FIXTURE_PATH = ROOT / "scripts" / "qa" / "fixtures" / "cbr" / "key_rate_page_2019_2026.html"


def assert_equal(actual: object, expected: object, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def assert_true(condition: object, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def make_project_root() -> tuple[Path, Path]:
    root = TEMP_ROOT / f"cbr_raw_status_smoke_{uuid.uuid4().hex}"
    raw_root = root / "data/raw/cbr/key_rate_inflation"
    raw_root.mkdir(parents=True, exist_ok=True)
    return root, raw_root


def fixture_daily() -> tuple[pd.DataFrame, str]:
    html = FIXTURE_PATH.read_text(encoding="utf-8")
    result = parse_cbr_key_rate_html(html)
    daily = make_daily_frame(result.observations)
    return daily, html


def write_web_raw(raw_root: Path, latest_date: date = date(2026, 7, 2)) -> None:
    _daily, html = fixture_daily()
    observations = [
        KeyRateObservation(date(2026, 7, 1), 14.25),
        KeyRateObservation(latest_date, 14.25),
    ]
    daily = make_daily_frame(sorted(observations, key=lambda item: item.date))
    metadata = build_metadata(
        source_url=build_cbr_key_rate_url("01.01.2019", latest_date.strftime("%d.%m.%Y")),
        source_type="web_table_data",
        source_file=None,
        from_date=date(2019, 1, 1),
        to_date=latest_date,
        retrieved_at=datetime(2026, 7, 3, tzinfo=UTC),
        page_last_modified=None,
        html=html,
        row_count=len(daily),
        parser="html_table",
        latest_available_date=latest_date,
        latest_available_value=14.25,
        source_rule="exact_daily_site_rows",
    )
    write_raw_outputs(daily=daily, metadata=metadata, output_root=raw_root)


def check_missing_raw() -> None:
    root, raw_root = make_project_root()
    try:
        legacy = root / "data/processed/reference"
        legacy.mkdir(parents=True, exist_ok=True)
        (legacy / "cbr_key_rate_daily.csv").write_text("date,value\n2026-07-02,14.25\n", encoding="utf-8")
        status = check_cbr_raw_status(root, raw_root=raw_root)
        assert_equal(status.severity, "missing", "Missing raw latest must not be hidden by processed/reference")
        assert_true("Raw dataset" in status.status, "Missing status should mention raw dataset")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def check_requires_update_when_site_is_newer() -> None:
    root, raw_root = make_project_root()
    try:
        write_web_raw(raw_root)
        status = check_cbr_raw_status(
            root,
            raw_root=raw_root,
            site_latest_date="2026-07-06",
            site_latest_value="14.25",
            site_checked_at="2026-07-06T12:00:00",
            requested_to_date="2026-07-06",
            today=date(2026, 7, 6),
        )
        assert_equal(status.severity, "requires_update", "Site-newer status severity mismatch")
        assert_equal(status.latest_date, "2026-07-02", "Latest date mismatch")
        assert_equal(status.latest_value, "14.25%", "Latest value mismatch")
        assert_equal(status.site_latest_date, "2026-07-06", "Site latest date mismatch")
        assert_equal(status.site_latest_value, "14.25%", "Site latest value mismatch")
        assert_equal(status.daily_rows, 2, "Daily row count mismatch")
        assert_equal(status.parser, "html_table", "Parser mismatch")
        assert_true("требуется обновление" in status.status, "Status should require update")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def check_current_when_site_matches() -> None:
    root, raw_root = make_project_root()
    try:
        write_web_raw(raw_root, latest_date=date(2026, 7, 6))
        status = check_cbr_raw_status(
            root,
            raw_root=raw_root,
            site_latest_date="2026-07-06",
            site_latest_value="14.25",
            site_checked_at="2026-07-06T12:00:00",
            requested_to_date="2026-07-06",
            today=date(2026, 7, 6),
        )
        assert_equal(status.severity, "ok", "Matching site/local status severity mismatch")
        assert_true("локальные данные совпадают" in status.status, "Current status wording mismatch")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def check_site_unavailable_warning() -> None:
    root, raw_root = make_project_root()
    try:
        write_web_raw(raw_root)
        status = check_cbr_raw_status(
            root,
            raw_root=raw_root,
            site_error="timeout",
            requested_to_date="2026-07-06",
            today=date(2026, 7, 6),
        )
        assert_equal(status.severity, "warning", "Site unavailable should be warning")
        assert_true("не проверен" in status.status, "Site unavailable wording mismatch")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def check_historical_range_status() -> None:
    root, raw_root = make_project_root()
    try:
        write_web_raw(raw_root)
        status = check_cbr_raw_status(
            root,
            raw_root=raw_root,
            site_latest_date="2026-07-06",
            site_latest_value="14.25",
            site_checked_at="2026-07-06T12:00:00",
            requested_to_date="2026-07-02",
            today=date(2026, 7, 6),
        )
        assert_equal(status.severity, "historical", "Historical To date status mismatch")
        assert_true("историческая проверка" in status.status, "Historical status wording mismatch")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def check_missing_meta_warning() -> None:
    root, raw_root = make_project_root()
    try:
        write_web_raw(raw_root)
        (raw_root / "latest/cbr_key_rate_daily.meta.json").unlink()
        status = check_cbr_raw_status(root, raw_root=raw_root)
        assert_equal(status.severity, "warning", "Missing meta should be a warning")
        assert_true("meta JSON отсутствует" in status.status, "Missing meta status mismatch")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def check_xlsx_fallback_warning() -> None:
    root, raw_root = make_project_root()
    try:
        daily, _html = fixture_daily()
        metadata = build_metadata(
            source_url="",
            source_type="xlsx_fallback",
            source_file="data/raw/cbr/key_rate_inflation/deleted.xlsx",
            from_date=date(2019, 1, 1),
            to_date=date(2026, 7, 2),
            retrieved_at=datetime(2026, 7, 3, tzinfo=UTC),
            page_last_modified=None,
            html=None,
            row_count=len(daily),
            parser="xlsx_fallback",
            source_rule="xlsx_fallback_rows",
        )
        write_raw_outputs(daily=daily, metadata=metadata, output_root=raw_root)
        status = check_cbr_raw_status(root, raw_root=raw_root)
        assert_equal(status.severity, "warning", "XLSX fallback should be warning")
        assert_true("XLSX fallback" in status.status, "XLSX fallback status mismatch")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def check_forbidden_columns_error() -> None:
    root, raw_root = make_project_root()
    try:
        latest = raw_root / "latest"
        latest.mkdir(parents=True, exist_ok=True)
        with (latest / "cbr_key_rate_daily.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["date", "value", "inflation"])
            writer.writeheader()
            writer.writerow({"date": "2026-07-02", "value": "14.25", "inflation": "0"})
        status = check_cbr_raw_status(root, raw_root=raw_root)
        assert_equal(status.severity, "error", "Forbidden inflation column should be error")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def check_current_project() -> None:
    status = check_cbr_raw_status(ROOT)
    payload = {
        "status": status.status,
        "severity": status.severity,
        "latest_date": status.latest_date,
        "latest_value": status.latest_value,
        "daily_rows": status.daily_rows,
        "source_label": status.source_label,
        "next_step": status.next_step,
        "paths": status.paths_label,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if status.severity not in {"ok", "warning", "historical", "requires_update"}:
        raise SystemExit(1)


def main(argv: list[str] | None = None) -> int:
    if argv and "--check-current" in argv:
        check_current_project()
        return 0
    check_missing_raw()
    check_requires_update_when_site_is_newer()
    check_current_when_site_matches()
    check_site_unavailable_warning()
    check_historical_range_status()
    check_missing_meta_warning()
    check_xlsx_fallback_warning()
    check_forbidden_columns_error()
    print("CBR raw status smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
