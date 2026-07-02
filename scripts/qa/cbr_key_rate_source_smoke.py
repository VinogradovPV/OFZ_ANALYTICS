"""Smoke test for the manual CBR key rate and inflation source."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts import config  # noqa: E402
from scripts.source_acquisition.cbr_key_rate_inflation import (  # noqa: E402
    REQUIRED_COLUMNS,
    normalize_cbr_key_rate_table,
    read_cbr_key_rate_workbook,
    write_cbr_key_rate_processed,
)


def main() -> int:
    raw_path = config.CBR_KEY_RATE_RAW_XLSX
    if not raw_path.exists():
        raise AssertionError(f"CBR raw XLSX not found: {raw_path}")

    workbook = read_cbr_key_rate_workbook(raw_path)
    missing = [column for column in REQUIRED_COLUMNS if column not in workbook.columns]
    if missing:
        raise AssertionError(f"Missing required CBR columns: {', '.join(missing)}")

    normalized = normalize_cbr_key_rate_table(workbook, raw_path)
    if normalized.empty:
        raise AssertionError("Normalized CBR dataset is empty.")
    if normalized["month"].duplicated().any():
        raise AssertionError("Normalized CBR dataset contains duplicate months.")
    if normalized["month"].min() != "2019-01-01":
        raise AssertionError(f"Unexpected min month: {normalized['month'].min()}")
    if normalized["month"].max() != "2026-05-01":
        raise AssertionError(f"Unexpected max month: {normalized['month'].max()}")
    if not pd.api.types.is_numeric_dtype(normalized["key_rate_pct"]):
        raise AssertionError("key_rate_pct is not numeric.")
    if float(normalized["key_rate_pct"].max()) != 21.0:
        raise AssertionError("Expected max key rate 21.0 was not found.")

    output_path = write_cbr_key_rate_processed(raw_path, config.CBR_KEY_RATE_PROCESSED_CSV)
    if not output_path.exists():
        raise AssertionError(f"Processed CBR CSV was not written: {output_path}")

    print(
        "CBR key rate source smoke passed: "
        f"rows={len(normalized)}, min={normalized['month'].min()}, max={normalized['month'].max()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
