"""Offline smoke checks for P3.6 Minfin registry validation in data audit."""

from __future__ import annotations

import shutil
from datetime import UTC, datetime
from pathlib import Path

from scripts.source_acquisition.source_registry import (
    RegistryRecord,
    compute_sha256,
    validate_source_registry,
    write_registry_json,
)


ROOT = Path(__file__).resolve().parents[2]


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _controlled_latest_path(root: Path, year: int) -> Path:
    return (
        root
        / "data"
        / "raw"
        / "minfin"
        / "ofz_auction_results"
        / "latest"
        / f"INTERNET_Auction_Results_rus_{year}_latest.xlsx"
    )


def _registry_path(root: Path, name: str = "registry.json") -> Path:
    return root / "data" / "raw" / "minfin" / "ofz_auction_results" / "registry" / name


def _record(*, year: int, sha256: str, size: int, active: bool = True) -> RegistryRecord:
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
        file_size_bytes=size,
        sha256=sha256,
        storage_role="latest",
        is_active_for_pipeline=active,
        supersedes_sha256=None,
        change_detected=True,
        notes="smoke controlled source",
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


def main() -> int:
    smoke_root = ROOT / "minfin_data_audit_registry_smoke_tmp"
    if smoke_root.exists():
        shutil.rmtree(smoke_root)
    smoke_root.mkdir()

    try:
        missing = _registry_path(smoke_root, "missing.json")
        warn_missing = validate_source_registry(
            missing,
            project_root=smoke_root,
            mode="warn",
            expected_years=[2026],
            allow_legacy_raw=True,
            legacy_raw_available=True,
        )
        _assert(warn_missing.ok, "missing registry in warn mode should not fail with legacy fallback")
        _assert(warn_missing.legacy_raw_fallback_used, "warn missing registry should use legacy fallback")
        _assert(warn_missing.warnings, "warn missing registry should emit warning")

        strict_missing = validate_source_registry(
            missing,
            project_root=smoke_root,
            mode="strict",
            expected_years=[2026],
            allow_legacy_raw=True,
            legacy_raw_available=True,
        )
        _assert(not strict_missing.ok, "missing registry in strict mode should fail")
        _assert(strict_missing.errors, "strict missing registry should emit error")
        _assert(not strict_missing.legacy_raw_fallback_used, "strict mode must not use legacy fallback")

        latest = _controlled_latest_path(smoke_root, 2026)
        latest.parent.mkdir(parents=True, exist_ok=True)
        latest.write_bytes(b"valid controlled bytes")
        valid_record = _record(year=2026, sha256=compute_sha256(latest), size=latest.stat().st_size)
        valid_registry = _registry_path(smoke_root, "valid.json")
        write_registry_json(valid_registry, [valid_record])
        valid = validate_source_registry(
            valid_registry,
            project_root=smoke_root,
            mode="strict",
            expected_years=[2026],
            allow_legacy_raw=False,
            legacy_raw_available=False,
        )
        _assert(valid.ok, "valid registry should pass strict validation")
        _assert(valid.active_records_count == 1, "valid registry should expose one active row")

        latest.unlink()
        missing_file = validate_source_registry(
            valid_registry,
            project_root=smoke_root,
            mode="strict",
            expected_years=[2026],
            allow_legacy_raw=False,
            legacy_raw_available=False,
        )
        _assert(not missing_file.ok, "missing active file should fail strict validation")
        _assert(any("missing" in error for error in missing_file.errors), "missing active file should be reported")

        latest.write_bytes(b"changed controlled bytes")
        hash_mismatch = validate_source_registry(
            valid_registry,
            project_root=smoke_root,
            mode="strict",
            expected_years=[2026],
            allow_legacy_raw=False,
            legacy_raw_available=False,
        )
        _assert(not hash_mismatch.ok, "hash mismatch should fail strict validation")
        _assert(any("hash mismatch" in error for error in hash_mismatch.errors), "hash mismatch should be reported")

        latest.write_bytes(b"valid controlled bytes")
        duplicate_registry = _registry_path(smoke_root, "duplicate.json")
        write_registry_json(duplicate_registry, [valid_record, valid_record])
        duplicate = validate_source_registry(
            duplicate_registry,
            project_root=smoke_root,
            mode="strict",
            expected_years=[2026],
            allow_legacy_raw=False,
            legacy_raw_available=False,
        )
        _assert(not duplicate.ok, "duplicate active rows should fail strict validation")
        _assert(any("duplicate active rows" in error for error in duplicate.errors), "duplicate active rows reported")

        latest.write_bytes(b"warn mode mismatch bytes")
        warn_hash_mismatch = validate_source_registry(
            valid_registry,
            project_root=smoke_root,
            mode="warn",
            expected_years=[2026],
            allow_legacy_raw=True,
            legacy_raw_available=True,
        )
        _assert(warn_hash_mismatch.ok, "warn mode should continue when legacy fallback is allowed")
        _assert(warn_hash_mismatch.legacy_raw_fallback_used, "legacy fallback should be visible in warn mode")
    finally:
        if smoke_root.exists():
            shutil.rmtree(smoke_root)

    print("P3.6 Minfin data audit registry smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
