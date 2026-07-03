from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

from scripts.reference_data.cbr_key_rate import make_daily_frame, make_monthly_frame, parse_cbr_key_rate_html


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "scripts" / "qa" / "fixtures" / "cbr" / "key_rate_page_2019_2026.html"


def test_parser_fixture_daily_and_monthly_contract() -> None:
    html = FIXTURE_PATH.read_text(encoding="utf-8")
    result = parse_cbr_key_rate_html(html)

    assert result.parser == "html_table"
    assert len(result.observations) == 8

    daily = make_daily_frame(result.observations)
    assert list(daily.columns) == ["date", "value"]
    assert {"inflation", "inflation_yoy", "inflation_target", "source_url", "retrieved_at"}.isdisjoint(
        daily.columns
    )

    monthly = make_monthly_frame(result.observations, date(2026, 7, 2))
    monthly_by_period = {row["period_month"]: row for _, row in monthly.iterrows()}

    assert monthly_by_period["2026-03-01"]["key_rate_date"] == "2026-03-31"
    assert float(monthly_by_period["2026-03-01"]["key_rate_month_end_pct"]) == 15.0
    assert monthly_by_period["2026-06-01"]["key_rate_date"] == "2026-06-30"
    assert float(monthly_by_period["2026-06-01"]["key_rate_month_end_pct"]) == 14.25
    assert monthly_by_period["2026-07-01"]["key_rate_date"] == "2026-07-02"
    assert monthly_by_period["2026-07-01"]["key_rate_source_rule"] == "last_available_observation_in_month"
    assert bool(monthly_by_period["2026-07-01"]["key_rate_month_is_partial"])


def test_html_file_dry_run_does_not_write(tmp_path: Path) -> None:
    daily_csv = tmp_path / "cbr_key_rate_daily.csv"
    meta_json = tmp_path / "cbr_key_rate_daily.meta.json"
    monthly_csv = tmp_path / "cbr_key_rate_monthly.csv"

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
    completed = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8")

    assert "dry_run=True" in completed.stdout
    assert not daily_csv.exists()
    assert not meta_json.exists()
    assert not monthly_csv.exists()
