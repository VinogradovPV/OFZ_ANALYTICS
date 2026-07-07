"""Offline smoke checks for P3.4 annual-final Minfin acquisition workflow."""

from __future__ import annotations

import shutil
from pathlib import Path

from scripts.source_acquisition.minfin_fetch import run_annual_final_download
from scripts.source_acquisition.source_registry import compute_sha256, load_registry_csv


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "fixtures" / "minfin_auction_page_section_66_sample.html"


def _assert(condition: object, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _empty_page() -> str:
    return '<div id="ajax-pagination-content-10090-66"></div>'


def main() -> int:
    smoke_root = ROOT / "minfin_annual_final_smoke_tmp"
    if smoke_root.exists():
        shutil.rmtree(smoke_root)
    smoke_root.mkdir()
    html = FIXTURE.read_text(encoding="utf-8")
    payload = {"bytes": b"annual final v1"}

    def fake_fetcher(url: str, timeout_seconds: int, retries: int, user_agent: str) -> str:
        if "page_66=" in url:
            return _empty_page()
        return html

    def fake_downloader(url: str, temp_path: str | Path, timeout_seconds: int, retries: int, user_agent: str) -> Path:
        target = Path(temp_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload["bytes"])
        return target

    try:
        first = run_annual_final_download(
            year=2025,
            source_url="https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/",
            output_root=str(smoke_root),
            timeout_seconds=1,
            retries=0,
            user_agent="smoke",
            max_pages=4,
            replace_final=False,
            page_fetcher=fake_fetcher,
            file_downloader=fake_downloader,
        )
        final_path = Path(first["final_path"])
        registry_path = Path(first["registry_csv_path"])
        _assert(final_path.exists(), "first annual-final run should create final file")
        _assert(registry_path.exists(), "first annual-final run should create registry")
        _assert(first["change_detected"] is True, "first annual-final run should detect new final")
        _assert(first["replacement_performed"] is False, "first annual-final run should not be replacement")
        _assert("20251230" in first["selected_candidate"]["file_name"], "final candidate must not require YYYY1231")
        _assert(first["selected_candidate"]["as_of_date"] is None, "annual final title must not have as_of_date")

        records = load_registry_csv(registry_path)
        _assert(records[-1].storage_role == "final", "annual-final registry row should use final role")
        _assert(records[-1].is_active_for_pipeline, "new annual final should be active after approval")

        same = run_annual_final_download(
            year=2025,
            source_url="https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/",
            output_root=str(smoke_root),
            timeout_seconds=1,
            retries=0,
            user_agent="smoke",
            max_pages=4,
            replace_final=False,
            page_fetcher=fake_fetcher,
            file_downloader=fake_downloader,
        )
        _assert(same["change_detected"] is False, "same final hash should be unchanged")
        _assert(same["final_path"] is None, "unchanged final should not be rewritten")

        original_hash = compute_sha256(final_path)
        payload["bytes"] = b"annual final v2"
        try:
            run_annual_final_download(
                year=2025,
                source_url="https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/",
                output_root=str(smoke_root),
                timeout_seconds=1,
                retries=0,
                user_agent="smoke",
                max_pages=4,
                replace_final=False,
                page_fetcher=fake_fetcher,
                file_downloader=fake_downloader,
            )
            raise AssertionError("changed final hash should be blocked without replacement confirmation")
        except RuntimeError as exc:
            _assert("REPLACE_MINFIN_FINAL" in str(exc), "blocked replacement should mention confirm token")
        _assert(compute_sha256(final_path) == original_hash, "blocked replacement must not mutate final file")

        replaced = run_annual_final_download(
            year=2025,
            source_url="https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/",
            output_root=str(smoke_root),
            timeout_seconds=1,
            retries=0,
            user_agent="smoke",
            max_pages=4,
            replace_final=True,
            page_fetcher=fake_fetcher,
            file_downloader=fake_downloader,
        )
        _assert(replaced["change_detected"] is True, "replacement should detect changed hash")
        _assert(replaced["replacement_performed"] is True, "replacement should be reported")
        _assert(compute_sha256(final_path) == replaced["sha256"], "replacement should update final file")

        records = load_registry_csv(registry_path)
        active_finals = [record for record in records if record.storage_role == "final" and record.is_active_for_pipeline]
        _assert(active_finals[-1].sha256 == replaced["sha256"], "new final row should be active")
    finally:
        if smoke_root.exists():
            shutil.rmtree(smoke_root)

    print("P3.4 Minfin annual-final smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
