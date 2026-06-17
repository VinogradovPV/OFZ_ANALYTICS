"""Offline smoke checks for the P3.1 Minfin source acquisition skeleton."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.source_acquisition.minfin_fetch import build_acquisition_plan
from scripts.source_acquisition.minfin_html_parser import (
    extract_pagination_info,
    parse_minfin_auction_table_documents,
    select_candidate,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "fixtures" / "minfin_auction_page_section_66_sample.html"
EXPECTED = ROOT / "tests" / "fixtures" / "minfin_auction_candidates_expected.json"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    html = FIXTURE.read_text(encoding="utf-8")
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    records = parse_minfin_auction_table_documents(html, page_number=1)
    _assert(records, "expected records from section 66 fixture")
    _assert({record.section_id for record in records} == {66}, "only section 66 should be parsed")
    _assert(all(record.file_extension == "xlsx" for record in records), "non-xlsx files should be ignored")
    _assert(
        all("20260620" not in record.file_name and "20260621" not in record.file_name for record in records),
        "sections 38/39 must be ignored",
    )

    pagination = extract_pagination_info(html)
    _assert(pagination["page_param"] == expected["pagination"]["page_param"], "page_66 must be parsed")
    _assert(pagination["page_count"] == expected["pagination"]["page_count"], "page count must be parsed")
    _assert(pagination["container"] == expected["pagination"]["container"], "container must be parsed")

    monthly = select_candidate(records, 2026, "monthly")
    _assert(monthly is not None, "monthly candidate expected")
    _assert(monthly.file_name == expected["monthly"]["file_name"], "latest monthly candidate mismatch")
    _assert(monthly.as_of_date == expected["monthly"]["as_of_date"], "monthly as_of_date mismatch")
    _assert(
        monthly.absolute_file_url == expected["monthly"]["absolute_file_url"],
        "relative monthly URL should be resolved",
    )

    annual = select_candidate(records, 2025, "annual-final")
    _assert(annual is not None, "annual-final candidate expected")
    _assert(annual.file_name == expected["annual_final"]["file_name"], "annual-final candidate mismatch")
    _assert(annual.as_of_date is None, "annual-final should prefer title without as_of_date")

    plan, plan_records, _ = build_acquisition_plan(
        year=2026,
        mode="monthly",
        dry_run=True,
        download_requested=False,
        html=html,
        no_network=True,
    )
    _assert(plan.selected_candidate is not None, "dry-run plan should select candidate")
    _assert(plan.candidate_count == len(plan_records), "candidate count should match parsed records")
    _assert("latest_path" in plan.planned_paths, "planned paths should include latest_path")

    print("P3.1 Minfin source acquisition smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

