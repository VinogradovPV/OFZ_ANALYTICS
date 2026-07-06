"""Smoke tests for Bank of Russia reference dataset status validation."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.gui_launcher.state import check_cbr_reference_status  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
TEMP_ROOT = ROOT / "outputs" / "tmp"
DAILY_COLUMNS = ("date", "value")
MONTHLY_COLUMNS = (
    "period_month",
    "period_label",
    "key_rate_month_end_pct",
    "key_rate_date",
    "key_rate_source_rule",
    "key_rate_month_is_partial",
)


def write_reference(
    root: Path,
    *,
    reference_root: Path,
    daily_columns: tuple[str, ...] = DAILY_COLUMNS,
    monthly_columns: tuple[str, ...] = MONTHLY_COLUMNS,
    meta: dict | None = None,
) -> None:
    reference_root.mkdir(parents=True, exist_ok=True)
    daily_path = reference_root / "cbr_key_rate_daily.csv"
    monthly_path = reference_root / "cbr_key_rate_monthly.csv"
    meta_path = reference_root / "cbr_key_rate_daily.meta.json"

    daily_row = {
        "date": "2026-07-02",
        "value": "14.25",
        "inflation": "9.0",
    }
    with daily_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(daily_columns), extrasaction="ignore")
        writer.writeheader()
        writer.writerow(daily_row)

    monthly_row = {
        "period_month": "2026-07-01",
        "period_label": "Июл-26",
        "key_rate_month_end_pct": "14.25",
        "key_rate_date": "2026-07-02",
        "key_rate_source_rule": "last_available_observation_in_month",
        "key_rate_month_is_partial": "True",
    }
    with monthly_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(monthly_columns), extrasaction="ignore")
        writer.writeheader()
        writer.writerow(monthly_row)

    payload = meta or {
        "source_url": "https://cbr.ru/hd_base/KeyRate/?UniDbQuery.Posted=True",
        "source_type": "web",
        "source_file": None,
        "retrieved_at": "2026-07-03T00:00:00Z",
        "row_count": 1,
        "parser": "html_table",
        "source_parser": "html_table",
    }
    meta_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def assert_status(root: Path, reference_root: Path, severity: str, text: str) -> None:
    status = check_cbr_reference_status(root, reference_root=reference_root)
    if status.severity != severity:
        raise AssertionError(f"Expected severity {severity!r}, got {status.severity!r}: {status.status}")
    if text not in status.status:
        raise AssertionError(f"Expected status containing {text!r}, got {status.status!r}")


def run_temp_status_smoke() -> None:
    TEMP_ROOT.mkdir(parents=True, exist_ok=True)
    root = TEMP_ROOT / "cbr_reference_status_smoke"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    reference_root = root / "reference"
    try:
        assert_status(root, reference_root, "missing", "не найдены")

        write_reference(root, reference_root=reference_root)
        assert_status(root, reference_root, "ok", "доступны")

        source_file = root / "raw/cbr/key_rate/key_rate_fallback.xlsx"
        source_file.parent.mkdir(parents=True, exist_ok=True)
        source_file.write_text("placeholder", encoding="utf-8")
        write_reference(
            root,
            reference_root=reference_root,
            meta={
                "source_url": "",
                "source_type": "xlsx_fallback",
                "source_file": "raw/cbr/key_rate/key_rate_fallback.xlsx",
                "retrieved_at": "2026-07-03T00:00:00Z",
                "row_count": 1,
                "parser": "xlsx_fallback",
                "source_parser": "xlsx_fallback",
            },
        )
        assert_status(root, reference_root, "warning", "XLSX fallback")

        source_file.unlink()
        assert_status(root, reference_root, "warning", "исходный XLSX fallback удален")

        write_reference(root, reference_root=reference_root, daily_columns=("date", "value", "inflation"))
        assert_status(root, reference_root, "error", "inflation columns")

        write_reference(
            root,
            reference_root=reference_root,
            monthly_columns=tuple(column for column in MONTHLY_COLUMNS if column != "key_rate_month_end_pct"),
        )
        assert_status(root, reference_root, "error", "Monthly dataset")

        write_reference(
            root,
            reference_root=reference_root,
            meta={
                "source_url": "",
                "source_type": "xlsx_fallback",
                "source_file": "data/raw/cbr/key_rate_inflation/cbr_key_rate_inflation_2019-01_2026-05.xlsx",
                "retrieved_at": "2026-07-03T00:00:00Z",
                "row_count": 1,
                "parser": "xlsx_fallback",
                "source_parser": "xlsx_fallback",
            },
        )
        assert_status(root, reference_root, "warning", "исходный XLSX fallback удален")

        write_reference(
            root,
            reference_root=reference_root,
            meta={
                "source_url": "data/raw/cbr/key_rate_inflation/cbr_key_rate_inflation_2019-01_2026-05.xlsx",
                "source_type": "web",
                "source_file": None,
                "retrieved_at": "2026-07-03T00:00:00Z",
                "row_count": 1,
                "parser": "html_table",
                "source_parser": "html_table",
            },
        )
        assert_status(root, reference_root, "warning", "Legacy source path")
    finally:
        if root.exists():
            shutil.rmtree(root)


def check_current(root: Path) -> int:
    status = check_cbr_reference_status(root)
    print(f"status={status.status}")
    print(f"severity={status.severity}")
    print(f"latest_date={status.latest_date}")
    print(f"latest_value={status.latest_value}")
    print(f"source={status.source_label}")
    print(f"next_step={status.next_step}")
    for check in status.checks:
        print(f"check: {check}")
    return 1 if status.severity == "error" else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Smoke CBR reference status validation.")
    parser.add_argument("--check-current", action="store_true", help="Validate current project reference datasets.")
    parser.add_argument("--project-root", type=Path, default=ROOT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.check_current:
        return check_current(args.project_root.resolve())
    run_temp_status_smoke()
    print("CBR reference status smoke passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
