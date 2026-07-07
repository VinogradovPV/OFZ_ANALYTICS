"""Smoke tests for the Bank of Russia key rate parser fixture."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import uuid
from datetime import UTC, date, datetime
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.reference_data.cbr_key_rate import (  # noqa: E402
    CbrTableParser,
    TABLE_HEADERS,
    build_metadata,
    build_cbr_key_rate_url,
    check_mode_for_to_date,
    default_to_date,
    latest_available,
    make_daily_frame,
    make_monthly_frame,
    parse_cbr_key_rate_html,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = ROOT / "scripts" / "qa" / "fixtures" / "cbr" / "key_rate_page_2019_2026.html"


def assert_equal(actual: object, expected: object, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def assert_true(condition: object, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_fixture() -> str:
    if not FIXTURE_PATH.exists():
        raise AssertionError(f"CBR key rate fixture not found: {FIXTURE_PATH}")
    return FIXTURE_PATH.read_text(encoding="utf-8")


def check_url_builder() -> None:
    expected = (
        "https://cbr.ru/hd_base/KeyRate/"
        "?UniDbQuery.Posted=True&UniDbQuery.From=01.01.2019&UniDbQuery.To=02.07.2026"
    )
    assert_equal(build_cbr_key_rate_url("01.01.2019", "02.07.2026"), expected, "Unexpected CBR URL")


def check_fixture_shape(html: str) -> None:
    for token in ("UniDbQuery.Posted", "UniDbQuery.From", "UniDbQuery.To", "table class=\"data\"", "categories", "data"):
        assert_true(token in html, f"Fixture is missing token: {token}")

    table_parser = CbrTableParser()
    table_parser.feed(html)
    assert_equal(len(table_parser.tables), 1, "Expected exactly one table.data")
    assert_equal(tuple(table_parser.tables[0][0][:2]), TABLE_HEADERS, "Unexpected table headers")


def check_parser_contract(html: str) -> None:
    result = parse_cbr_key_rate_html(html)
    assert_equal(result.parser, "html_table", "Expected table parser with Highcharts cross-check")
    observations = result.observations
    assert_equal(len(observations), 8, "Unexpected observation count")

    dates = [item.date for item in observations]
    assert_equal(dates, sorted(dates), "Observations are not sorted ascending")
    assert_equal(dates[0], date(2019, 1, 2), "Unexpected first observation")
    assert_equal(dates[-1], date(2026, 7, 2), "Unexpected last observation")

    values_by_date = {item.date: item.value for item in observations}
    assert_equal(values_by_date[date(2026, 7, 2)], 14.25, "Decimal comma was not parsed as 14.25")
    latest = latest_available(observations)
    assert_equal(latest.date, date(2026, 7, 2), "Latest available date must be max(date)")
    assert_equal(latest.value, 14.25, "Latest available value mismatch")

    daily = make_daily_frame(observations)
    assert_equal(list(daily.columns), ["date", "value"], "Daily columns must be exactly date,value")
    forbidden_daily_columns = {"inflation", "inflation_yoy", "inflation_target", "source_url", "retrieved_at"}
    assert_true(not forbidden_daily_columns.intersection(daily.columns), "Daily output contains forbidden columns")

    monthly = make_monthly_frame(observations, date(2026, 7, 2))
    monthly_by_period = {row["period_month"]: row for _, row in monthly.iterrows()}

    march = monthly_by_period["2026-03-01"]
    assert_equal(march["key_rate_date"], "2026-03-31", "March 2026 key rate date mismatch")
    assert_equal(float(march["key_rate_month_end_pct"]), 15.0, "March 2026 key rate mismatch")

    june = monthly_by_period["2026-06-01"]
    assert_equal(june["key_rate_date"], "2026-06-30", "June 2026 key rate date mismatch")
    assert_equal(float(june["key_rate_month_end_pct"]), 14.25, "June 2026 key rate mismatch")

    july = monthly_by_period["2026-07-01"]
    assert_equal(july["key_rate_date"], "2026-07-02", "July 2026 key rate date mismatch")
    assert_true(bool(july["key_rate_month_is_partial"]), "July 2026 must be marked as partial")
    assert_equal(july["key_rate_source_rule"], "last_available_observation_in_month", "Monthly source rule mismatch")

    metadata = build_metadata(
        source_url=build_cbr_key_rate_url("01.01.2019", "02.07.2026"),
        source_type="web_table_data",
        source_file=None,
        from_date=date(2019, 1, 1),
        to_date=date(2026, 7, 2),
        retrieved_at=datetime(2026, 7, 3, tzinfo=UTC),
        page_last_modified=None,
        html=html,
        row_count=len(daily),
        parser=result.parser,
        latest_available_date=latest.date,
        latest_available_value=latest.value,
        source_rule="exact_daily_site_rows",
    )
    assert_equal(metadata["source_type"], "web_table_data", "Metadata source_type mismatch")
    assert_equal(metadata["source_file"], None, "Metadata source_file mismatch")
    assert_equal(metadata["source_parser"], "html_table", "Metadata source_parser mismatch")
    assert_equal(metadata["requested_to_date"], "2026-07-02", "Metadata requested_to_date mismatch")
    assert_equal(metadata["latest_available_date"], "2026-07-02", "Metadata latest_available_date mismatch")
    assert_equal(metadata["latest_available_value"], 14.25, "Metadata latest_available_value mismatch")
    assert_equal(metadata["source_rule"], "exact_daily_site_rows", "Metadata source_rule mismatch")
    assert_true(bool(metadata["html_sha256"]), "Metadata html_sha256 is empty")


def check_latest_available_from_table_data() -> None:
    html = f"""
    <html><body>
      <table class="data">
        <tr><th>{TABLE_HEADERS[0]}</th><th>{TABLE_HEADERS[1]}</th></tr>
        <tr><td>02.07.2026</td><td>14,25</td></tr>
        <tr><td>06.07.2026</td><td>14,25</td></tr>
        <tr><td>03.07.2026</td><td>14,25</td></tr>
      </table>
    </body></html>
    """
    result = parse_cbr_key_rate_html(html)
    dates = [item.date for item in result.observations]
    assert_equal(dates, sorted(dates), "Parser must sort table rows ascending")
    latest = latest_available(result.observations)
    assert_equal(latest.date, date(2026, 7, 6), "Parser did not detect max table.data date")
    assert_equal(latest.value, 14.25, "Latest available value must come from max(date) row")


def check_dynamic_to_date_and_modes() -> None:
    assert_equal(default_to_date(), date.today().strftime("%d.%m.%Y"), "Default CBR To date must be today")
    assert_equal(check_mode_for_to_date(date(2026, 7, 2), date(2026, 7, 6)), "historical_range", "Historical mode mismatch")
    assert_equal(check_mode_for_to_date(date(2026, 7, 6), date(2026, 7, 6)), "freshness", "Freshness mode mismatch")


def check_dry_run_does_not_write() -> None:
    temp_root = ROOT / "outputs" / "tmp" / f"cbr_key_rate_parser_smoke_{uuid.uuid4().hex}"
    daily_csv = temp_root / "cbr_key_rate_daily.csv"
    meta_json = temp_root / "cbr_key_rate_daily.meta.json"
    monthly_csv = temp_root / "cbr_key_rate_monthly.csv"

    command = [
        sys.executable,
        str(ROOT / "scripts" / "reference_data" / "cbr_key_rate.py"),
        "--source",
        "html-file",
        "--html-file",
        str(FIXTURE_PATH),
        "--daily-output-csv",
        str(daily_csv),
        "--daily-meta-json",
        str(meta_json),
        "--monthly-output-csv",
        str(monthly_csv),
        "--dry-run",
    ]
    completed = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert_true("dry_run=True" in completed.stdout, "Dry-run output did not confirm dry_run=True")
    for path in (daily_csv, meta_json, monthly_csv):
        assert_true(not path.exists(), f"Dry-run unexpectedly wrote {path}")
    assert_true(not temp_root.exists(), f"Dry-run unexpectedly created output directory {temp_root}")


def check_download_writes_raw_storage() -> None:
    temp_root = ROOT / "outputs" / "tmp" / f"cbr_key_rate_parser_download_{uuid.uuid4().hex}"
    output_root = temp_root / "raw"
    command = [
        sys.executable,
        str(ROOT / "scripts" / "reference_data" / "cbr_key_rate.py"),
        "--source",
        "html-file",
        "--html-file",
        str(FIXTURE_PATH),
        "--output-root",
        str(output_root),
        "--download",
        "--confirm",
        "UPDATE_CBR_KEY_RATE",
    ]
    try:
        first = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert_true("write_status=changed" in first.stdout, "Download output did not confirm update")
        latest_csv = output_root / "latest" / "cbr_key_rate_daily.csv"
        latest_meta = output_root / "latest" / "cbr_key_rate_daily.meta.json"
        registry_csv = output_root / "registry" / "cbr_key_rate_registry.csv"
        registry_json = output_root / "registry" / "cbr_key_rate_registry_latest.json"
        versions = sorted((output_root / "versions").glob("cbr_key_rate_daily_*.csv"))
        for path in (latest_csv, latest_meta, registry_csv, registry_json):
            assert_true(path.exists(), f"Download did not write {path}")
        assert_equal(len(versions), 1, "First download should write one version snapshot")
        assert_equal(latest_csv.read_text(encoding="utf-8").splitlines()[0], "date,value", "Latest CSV header mismatch")
        meta = json.loads(latest_meta.read_text(encoding="utf-8"))
        assert_equal(meta["source_type"], "html_fixture", "HTML fixture source_type mismatch")
        assert_equal(meta["parser"], "html_table", "Parser metadata mismatch")
        assert_equal(meta["latest_available_date"], "2026-07-02", "Latest available metadata mismatch")
        assert_equal(meta["latest_available_value"], 14.25, "Latest available value metadata mismatch")
        assert_true(bool(meta["sha256"]), "Metadata sha256 is empty")

        second = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert_true("write_status=unchanged" in second.stdout, "Second download should be unchanged")
        versions_after_second = sorted((output_root / "versions").glob("cbr_key_rate_daily_*.csv"))
        assert_equal(len(versions_after_second), 1, "Unchanged download should not add a version snapshot")
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def main() -> int:
    html = load_fixture()
    check_url_builder()
    check_fixture_shape(html)
    check_parser_contract(html)
    check_latest_available_from_table_data()
    check_dynamic_to_date_and_modes()
    check_dry_run_does_not_write()
    check_download_writes_raw_storage()
    print("CBR key rate parser smoke passed: fixture rows=8, monthly rule=last_available_observation_in_month")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
