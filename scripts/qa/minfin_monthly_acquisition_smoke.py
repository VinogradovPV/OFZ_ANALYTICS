"""Offline smoke checks for P3.3 monthly Minfin acquisition workflow."""

from __future__ import annotations

import shutil
from pathlib import Path

from scripts.source_acquisition.http_client import HttpClientError
from scripts.source_acquisition.minfin_fetch import run_monthly_download
from scripts.source_acquisition.source_registry import load_registry_csv


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "fixtures" / "minfin_auction_page_section_66_sample.html"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _empty_page() -> str:
    return '<div id="ajax-pagination-content-10090-66"></div>'


def main() -> int:
    smoke_root = ROOT / "minfin_monthly_smoke_tmp"
    if smoke_root.exists():
        shutil.rmtree(smoke_root)
    smoke_root.mkdir()
    html = FIXTURE.read_text(encoding="utf-8")

    def fake_fetcher(url: str, timeout_seconds: int, retries: int, user_agent: str) -> str:
        if "page_66=" in url:
            return _empty_page()
        return html

    def fake_downloader(url: str, temp_path: str | Path, timeout_seconds: int, retries: int, user_agent: str) -> Path:
        target = Path(temp_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"dummy xlsx bytes v1")
        return target

    try:
        result = run_monthly_download(
            year=2026,
            source_url="https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/",
            output_root=str(smoke_root),
            timeout_seconds=1,
            retries=0,
            user_agent="smoke",
            max_pages=4,
            page_fetcher=fake_fetcher,
            file_downloader=fake_downloader,
        )
        latest = Path(result["latest_path"])
        version = Path(result["version_snapshot_path"])
        registry = Path(result["registry_csv_path"])
        report = smoke_root / "outputs" / "reports" / "source_acquisition" / "minfin_monthly_2026.json"
        _assert(latest.exists(), "latest file should be promoted")
        _assert(version.exists(), "version snapshot should be created on first changed hash")
        _assert(registry.exists(), "registry CSV should be written")
        _assert(report.exists(), "source acquisition report should be written")
        _assert(result["change_detected"] is True, "first acquisition should be a change")

        records = load_registry_csv(registry)
        _assert(len(records) == 1, "first run should write one registry row")
        _assert(records[0].storage_role == "latest", "first row should be latest")
        _assert(records[0].is_active_for_pipeline, "latest row should be active")

        second = run_monthly_download(
            year=2026,
            source_url="https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/",
            output_root=str(smoke_root),
            timeout_seconds=1,
            retries=0,
            user_agent="smoke",
            max_pages=4,
            page_fetcher=fake_fetcher,
            file_downloader=fake_downloader,
        )
        _assert(second["change_detected"] is False, "second identical acquisition should be unchanged")
        _assert(second["version_snapshot_path"] is None, "unchanged hash should not create a version snapshot")
        records = load_registry_csv(registry)
        _assert(len(records) == 2, "unchanged observation should append registry row")
        _assert(records[-1].storage_role == "observation", "unchanged row should be observation")
        _assert(len(list(version.parent.glob("*.xlsx"))) == 1, "unchanged run should not add snapshots")

        failure_root = smoke_root / "failure_case"

        def failing_fetcher(url: str, timeout_seconds: int, retries: int, user_agent: str) -> str:
            raise HttpClientError("simulated 503")

        try:
            run_monthly_download(
                year=2026,
                source_url="https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/",
                output_root=str(failure_root),
                timeout_seconds=1,
                retries=0,
                user_agent="smoke",
                max_pages=4,
                page_fetcher=failing_fetcher,
                file_downloader=fake_downloader,
            )
            raise AssertionError("simulated fetch failure should raise")
        except HttpClientError:
            pass
        _assert(not (failure_root / "data").exists(), "fetch failure must not mutate raw storage")
    finally:
        if smoke_root.exists():
            shutil.rmtree(smoke_root)

    print("P3.3 Minfin monthly acquisition smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
