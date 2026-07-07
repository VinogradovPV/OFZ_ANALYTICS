"""Offline smoke checks for P3.5 manual Minfin import workflow."""

from __future__ import annotations

import shutil
from pathlib import Path

from scripts.source_acquisition.minfin_fetch import build_acquisition_plan, main, run_manual_import
from scripts.source_acquisition.source_registry import compute_sha256, load_registry_csv


ROOT = Path(__file__).resolve().parents[2]


def _assert(condition: object, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main_smoke() -> int:
    smoke_root = ROOT / "minfin_manual_import_smoke_tmp"
    if smoke_root.exists():
        shutil.rmtree(smoke_root)
    smoke_root.mkdir()

    valid_file = smoke_root / "INTERNET_Auction_Results_rus_2026_20260630.xlsx"
    year_mismatch = smoke_root / "INTERNET_Auction_Results_rus_2025_20251230.xlsx"
    invalid_extension = smoke_root / "INTERNET_Auction_Results_rus_2026_20260630.csv"
    valid_file.write_bytes(b"manual xlsx bytes v1")
    year_mismatch.write_bytes(b"manual xlsx bytes mismatch")
    invalid_extension.write_bytes(b"not xlsx")

    try:
        plan, records, pagination = build_acquisition_plan(
            year=2026,
            mode="manual-import",
            dry_run=True,
            download_requested=False,
            output_root=str(smoke_root),
            manual_file=str(valid_file),
            no_network=True,
        )
        selected = plan.selected_candidate or {}
        _assert(records == [], "manual dry-run should not create HTML records")
        _assert(pagination is None, "manual dry-run should not parse pagination")
        _assert(selected.get("sha256") == compute_sha256(valid_file), "manual dry-run should compute sha256")
        _assert(selected.get("planned_storage_role") == "latest", "new manual file should plan latest role")
        _assert(selected.get("final_path") is None, "manual dry-run must not plan final overwrite")
        _assert(not (smoke_root / "data").exists(), "manual dry-run must not create raw storage")

        blocked = main(
            [
                "--year",
                "2026",
                "--mode",
                "manual-import",
                "--manual-file",
                str(valid_file),
                "--download",
            ]
        )
        _assert(blocked == 2, "manual import without confirm should be blocked")
        _assert(not (smoke_root / "data").exists(), "blocked manual import must not mutate raw storage")

        imported = run_manual_import(year=2026, manual_file=valid_file, output_root=str(smoke_root))
        latest = Path(imported["latest_path"])
        version = Path(imported["version_snapshot_path"])
        final_path = smoke_root / "data" / "raw" / "minfin" / "ofz_auction_results" / "final"
        registry = Path(imported["registry_csv_path"])
        _assert(latest.exists(), "manual import should promote latest")
        _assert(version.exists(), "manual import should write version snapshot on changed hash")
        _assert(not final_path.exists(), "manual import must not write final storage")

        rows = load_registry_csv(registry)
        _assert(rows[-1].discovery_method == "manual-import", "registry discovery_method should be manual-import")
        _assert(rows[-1].storage_role == "latest", "changed manual import should become active latest")
        _assert(rows[-1].is_active_for_pipeline, "changed manual latest should be active")
        _assert("original_local_file=" in (rows[-1].notes or ""), "manual import notes should include source path")

        unchanged = run_manual_import(year=2026, manual_file=valid_file, output_root=str(smoke_root))
        _assert(unchanged["change_detected"] is False, "same manual file should be unchanged")
        _assert(unchanged["planned_storage_role"] == "observation", "same hash should become observation")
        _assert(unchanged["latest_path"] is None, "unchanged manual import should not rewrite latest")

        try:
            run_manual_import(year=2026, manual_file=year_mismatch, output_root=str(smoke_root))
            raise AssertionError("year mismatch should be rejected")
        except ValueError as exc:
            _assert("does not match --year" in str(exc), "year mismatch should explain --year")

        try:
            run_manual_import(year=2026, manual_file=invalid_extension, output_root=str(smoke_root))
            raise AssertionError("invalid extension should be rejected")
        except ValueError as exc:
            _assert("must be .xlsx" in str(exc), "invalid extension should explain .xlsx requirement")
    finally:
        if smoke_root.exists():
            shutil.rmtree(smoke_root)

    print("P3.5 Minfin manual import smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main_smoke())
