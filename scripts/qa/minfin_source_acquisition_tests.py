"""Offline QA tests for Minfin source acquisition parser and workflows."""

from __future__ import annotations

import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

from scripts.source_acquisition.http_client import HttpClientError
from scripts.source_acquisition.minfin_fetch import (
    build_acquisition_plan,
    run_annual_final_download,
    run_manual_import,
    run_monthly_download,
)
from scripts.source_acquisition.minfin_html_parser import (
    extract_pagination_info,
    filter_candidates,
    parse_minfin_auction_table_documents,
    select_candidate,
)
from scripts.source_acquisition.source_registry import (
    RegistryRecord,
    compute_sha256,
    detect_hash_change,
    find_active_record,
    load_registry_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "fixtures"
BASE_URL = "https://minfin.gov.ru"


def _assert(condition: object, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _load_text(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def _empty_page() -> str:
    return '<div id="ajax-pagination-content-10090-66"></div>'


def _registry_record(year: int, sha256: str) -> RegistryRecord:
    return RegistryRecord(
        source_name="minfin_ofz_auction_results",
        source_url="https://minfin.gov.ru/example.xlsx",
        page_title="Minfin auction page",
        link_text=f"INTERNET_Auction_Results_rus_{year}_latest.xlsx",
        file_name=f"INTERNET_Auction_Results_rus_{year}_latest.xlsx",
        year=year,
        publication_period="monthly",
        downloaded_at=datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        source_last_modified=None,
        http_etag=None,
        http_last_modified=None,
        file_size_bytes=1,
        sha256=sha256,
        storage_role="latest",
        is_active_for_pipeline=True,
        supersedes_sha256=None,
        change_detected=True,
        notes="source acquisition QA fixture",
        section_id=66,
        page_param="page_66",
        page_number=1,
        document_id="6601",
        document_page_url=None,
        document_title=f"Auction results {year}",
        published_at="15.06.2026",
        modified_at="15.06.2026",
        as_of_date="11.06.2026",
        file_url="/common/upload/example.xlsx",
        absolute_file_url="https://minfin.gov.ru/common/upload/example.xlsx",
        file_title=f"INTERNET_Auction_Results_rus_{year}_latest.xlsx",
        file_info="xlsx",
        file_size_text="xlsx",
        discovery_method="html",
        pagination_page_count=1,
    )


def test_parser_and_selection() -> None:
    html = _load_text("minfin_auction_page_section_66_sample.html")
    page2 = _load_text("minfin_auction_page_66_page2_sample.html")
    wrong_sections = _load_text("minfin_wrong_sections_sample.html")
    expected = json.loads((FIXTURES / "minfin_auction_candidates_expected.json").read_text(encoding="utf-8"))

    records = parse_minfin_auction_table_documents(html, BASE_URL, page_number=1)
    page2_records = parse_minfin_auction_table_documents(page2, BASE_URL, page_number=2)
    wrong_records = parse_minfin_auction_table_documents(wrong_sections, BASE_URL, page_number=1)
    all_records = records + page2_records

    _assert(records, "section 66 parser should extract records")
    _assert({record.section_id for record in records} == {66}, "only section 66 should be selected")
    _assert(wrong_records == [], "sections 65/38/39 should be ignored")
    _assert(all(record.page_param == "page_66" for record in all_records), "page_66 should be preserved")
    _assert(any(record.page_number == 2 for record in page2_records), "page 2 records should preserve page_number")

    pagination = extract_pagination_info(html)
    _assert(pagination["page_param"] == expected["pagination"]["page_param"], "page_66 should be parsed")
    _assert(pagination["page_count"] == expected["pagination"]["page_count"], "data-page-count should be parsed")
    _assert(pagination["container"] == expected["pagination"]["container"], "pagination container should be parsed")

    monthly = select_candidate(all_records, 2026, "monthly")
    annual = select_candidate(all_records, 2025, "annual-final")
    assert monthly is not None, "monthly candidate should be selected"
    _assert(monthly.file_name == expected["monthly"]["file_name"], "current-year monthly candidate mismatch")
    _assert(monthly.as_of_date == expected["monthly"]["as_of_date"], "monthly as_of_date should be parsed")
    _assert(monthly.absolute_file_url == expected["monthly"]["absolute_file_url"], "relative XLSX URL should resolve")
    assert annual is not None, "annual-final candidate should be selected"
    _assert(annual.file_name == expected["annual_final"]["file_name"], "annual-final candidate mismatch")
    _assert("20251230" in annual.file_name, "annual-final must not require YYYY1231")
    _assert(annual.as_of_date is None, "annual-final should not have monthly as_of_date")

    year_2026 = filter_candidates(all_records, 2026)
    names_2026 = {record.file_name for record in year_2026}
    _assert("INTERNET_Auction_Results_rus_2024_20241230.xlsx" not in names_2026, "wrong year ignored")
    _assert(all(not name.endswith(".pdf") for name in names_2026), "non-xlsx ignored")
    _assert("" not in names_2026, "malformed links ignored")


def test_hash_changed_unchanged() -> None:
    changed_case = json.loads((FIXTURES / "minfin_hash_changed_case.json").read_text(encoding="utf-8"))
    unchanged_case = json.loads((FIXTURES / "minfin_hash_unchanged_case.json").read_text(encoding="utf-8"))
    changed_path = ROOT / "minfin_hash_changed_tmp"
    unchanged_path = ROOT / "minfin_hash_unchanged_tmp"
    try:
        changed_path.write_bytes(changed_case["candidate_bytes"].encode("utf-8"))
        changed_sha = compute_sha256(changed_path)
        previous = _registry_record(2026, changed_case["previous_sha256"])
        _assert(
            detect_hash_change(previous, changed_sha) is changed_case["expected_change_detected"],
            "changed hash should be detected",
        )

        unchanged_path.write_bytes(unchanged_case["candidate_bytes"].encode("utf-8"))
        unchanged_sha = compute_sha256(unchanged_path)
        previous_same = _registry_record(2026, unchanged_sha)
        _assert(
            detect_hash_change(previous_same, unchanged_sha) is unchanged_case["expected_change_detected"],
            "unchanged hash should not be detected as change",
        )
    finally:
        for path in (changed_path, unchanged_path):
            if path.exists():
                path.unlink()


def test_workflow_failure_modes() -> None:
    smoke_root = ROOT / "minfin_source_acquisition_tests_tmp"
    if smoke_root.exists():
        shutil.rmtree(smoke_root)
    smoke_root.mkdir()
    html = _load_text("minfin_auction_page_section_66_sample.html")

    def fake_fetcher(url: str, timeout_seconds: int, retries: int, user_agent: str) -> str:
        if "page_66=" in url:
            return _empty_page()
        return html

    payload = {"bytes": b"annual final v1"}

    def fake_downloader(url: str, temp_path: str | Path, timeout_seconds: int, retries: int, user_agent: str) -> Path:
        target = Path(temp_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload["bytes"])
        return target

    try:
        failure_root = smoke_root / "network_failure"

        def failing_fetcher(url: str, timeout_seconds: int, retries: int, user_agent: str) -> str:
            raise HttpClientError("simulated 503")

        try:
            run_monthly_download(
                year=2026,
                source_url="https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/",
                output_root=str(failure_root),
                timeout_seconds=1,
                retries=0,
                user_agent="qa",
                max_pages=4,
                page_fetcher=failing_fetcher,
                file_downloader=fake_downloader,
            )
            raise AssertionError("simulated 503 should fail")
        except HttpClientError:
            pass
        _assert(not (failure_root / "data").exists(), "503/timeout failure must not mutate raw")

        first = run_annual_final_download(
            year=2025,
            source_url="https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/",
            output_root=str(smoke_root),
            timeout_seconds=1,
            retries=0,
            user_agent="qa",
            max_pages=4,
            replace_final=False,
            page_fetcher=fake_fetcher,
            file_downloader=fake_downloader,
        )
        _assert(Path(first["final_path"]).exists(), "annual-final initial promote should create temp final")
        payload["bytes"] = b"annual final v2"
        try:
            run_annual_final_download(
                year=2025,
                source_url="https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/",
                output_root=str(smoke_root),
                timeout_seconds=1,
                retries=0,
                user_agent="qa",
                max_pages=4,
                replace_final=False,
                page_fetcher=fake_fetcher,
                file_downloader=fake_downloader,
            )
            raise AssertionError("annual-final changed hash should require replace confirm")
        except RuntimeError as exc:
            _assert("REPLACE_MINFIN_FINAL" in str(exc), "annual-final replacement should mention confirm")

        wrong_year = smoke_root / "INTERNET_Auction_Results_rus_2025_20251230.xlsx"
        wrong_year.write_bytes(b"manual wrong year")
        try:
            run_manual_import(year=2026, manual_file=wrong_year, output_root=str(smoke_root))
            raise AssertionError("manual-file year mismatch should be rejected")
        except ValueError as exc:
            _assert("does not match --year" in str(exc), "manual mismatch error should explain year")

        dry_root = smoke_root / "dry_run"
        plan, records, pagination = build_acquisition_plan(
            year=2026,
            mode="monthly",
            dry_run=True,
            download_requested=False,
            output_root=str(dry_root),
            html=html,
            no_network=True,
        )
        _assert(plan.selected_candidate is not None, "dry-run should select candidate from fixture")
        _assert(records, "dry-run should expose fixture records")
        _assert(pagination is not None, "dry-run should parse pagination")
        _assert(not (dry_root / "data").exists(), "dry-run must not mutate raw")
        _assert(not (dry_root / "outputs").exists(), "dry-run must not write outputs")

        registry = load_registry_csv(smoke_root / "data" / "raw" / "minfin" / "ofz_auction_results" / "registry" / "minfin_ofz_auction_sources.csv")
        active_final = find_active_record(registry, 2025, "final")
        assert active_final is not None, "annual-final workflow should leave active final in temp registry"
    finally:
        if smoke_root.exists():
            shutil.rmtree(smoke_root)


def main() -> int:
    test_parser_and_selection()
    test_hash_changed_unchanged()
    test_workflow_failure_modes()
    print("P3.7 Minfin source acquisition QA tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
