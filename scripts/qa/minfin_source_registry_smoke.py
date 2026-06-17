"""Offline smoke checks for the P3.2 Minfin source registry writer."""

from __future__ import annotations

import json
import shutil
from dataclasses import replace
from pathlib import Path

from scripts.source_acquisition.source_registry import (
    RegistryRecord,
    append_registry_record,
    compute_sha256,
    detect_hash_change,
    find_active_record,
    get_file_size,
    load_registry_csv,
    load_registry_json,
    mark_superseded,
    validate_registry_record,
    write_registry_csv,
    write_registry_json,
)


ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "tests" / "fixtures" / "minfin_registry_sample.json"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _load_sample_record() -> RegistryRecord:
    payload = json.loads(SAMPLE.read_text(encoding="utf-8"))
    row = payload["records"][0]
    return RegistryRecord(**row)


def main() -> int:
    tmp = ROOT / "minfin_registry_smoke_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    try:
        candidate = tmp / "INTERNET_Auction_Results_rus_2026_20260611.xlsx"
        candidate.write_bytes(b"fixture-v1")
        changed = tmp / "INTERNET_Auction_Results_rus_2026_20260612.xlsx"
        changed.write_bytes(b"fixture-v2")

        sha = compute_sha256(candidate)
        changed_sha = compute_sha256(changed)
        size = get_file_size(candidate)

        record = replace(_load_sample_record(), sha256=sha, file_size_bytes=size)
        status = validate_registry_record(record)
        _assert(status.ok, f"sample record should validate: {status.errors}")

        csv_path = tmp / "registry" / "minfin_ofz_auction_sources.csv"
        json_path = tmp / "registry" / "minfin_ofz_auction_sources_latest.json"
        write_registry_csv(csv_path, [record])
        write_registry_json(json_path, [record])

        csv_records = load_registry_csv(csv_path)
        json_records = load_registry_json(json_path)
        _assert(csv_records == [record], "CSV roundtrip mismatch")
        _assert(json_records == [record], "JSON roundtrip mismatch")

        appended = append_registry_record(csv_path, replace(record, storage_role="observation", is_active_for_pipeline=False))
        _assert(len(appended) == 2, "append should return two records")
        _assert(len(load_registry_csv(csv_path)) == 2, "append should persist second record")

        active = find_active_record(appended, 2026, "latest")
        _assert(active == record, "active latest record should be selected")
        _assert(not detect_hash_change(active, sha), "same sha should be unchanged")
        _assert(detect_hash_change(active, changed_sha), "different sha should be changed")

        superseded = mark_superseded(appended, sha)
        superseded_active = find_active_record(superseded, 2026, "latest")
        _assert(superseded_active is None, "superseded active latest should be inactive")
    finally:
        if tmp.exists():
            shutil.rmtree(tmp)

    print("P3.2 Minfin source registry smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
