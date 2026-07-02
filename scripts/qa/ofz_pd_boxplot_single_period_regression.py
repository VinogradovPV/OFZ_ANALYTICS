"""Regression smoke for OFZ-PD single-period boxplot fallback."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts import config  # noqa: E402


REPORT_DATE = "2026-01-01"
RETROSPECTIVE_YEARS = "1"
PERIOD_TYPE = "year"
AGGREGATION_MODE = "cumulative"
SUFFIX = "year_cumulative_2026-01-01_retrospective_1"


def main() -> int:
    period_filter_command = [
        sys.executable,
        "scripts/period_filter.py",
        "--report-date",
        REPORT_DATE,
        "--retrospective-years",
        RETROSPECTIVE_YEARS,
        "--period-type",
        PERIOD_TYPE,
        "--aggregation-mode",
        AGGREGATION_MODE,
    ]
    subprocess.run(period_filter_command, cwd=config.PROJECT_ROOT, check=True)

    chart_command = [
        sys.executable,
        "scripts/06_build_charts.py",
        "--report-date",
        REPORT_DATE,
        "--retrospective-years",
        RETROSPECTIVE_YEARS,
        "--period-type",
        PERIOD_TYPE,
        "--aggregation-mode",
        AGGREGATION_MODE,
    ]
    subprocess.run(chart_command, cwd=config.PROJECT_ROOT, check=True)

    html_path = config.CHARTS_DIR / "yield" / "ofz_pd" / f"yield_boxplot_ofz_pd_{SUFFIX}.html"
    stats_path = config.EXPORTS_CHART_DATA_BOXPLOT_DIR / f"yield_boxplot_ofz_pd_stats_{SUFFIX}.csv"
    if not html_path.exists():
        raise AssertionError(f"Single-period OFZ-PD HTML was not generated: {html_path}")
    if not stats_path.exists():
        raise AssertionError(f"Single-period OFZ-PD stats CSV was not generated: {stats_path}")

    html = html_path.read_text(encoding="utf-8")
    compact = "".join(html.split())
    required_tokens = [
        "single_period_strip_points",
        "single_period_stats_hover",
        "single_period_strip_box",
        "single_period_jitter",
        "single_period_min_tick",
        "single_period_median_tick",
        "single_period_max_tick",
        "Один период",
        "мин:",
        "мед:",
        "макс:",
        "n=",
    ]
    missing = [token for token in required_tokens if token not in html]
    if missing:
        raise AssertionError(f"Single-period fallback tokens missing in HTML: {', '.join(missing)}")
    if '"opacity":0.55' not in compact:
        raise AssertionError("Strip points must use marker opacity 0.55.")
    if '"range":[-0.72,1.72]' not in compact:
        raise AssertionError("Single-period x-axis range must be expanded for the short year horizon.")
    if '"type":"box"' in compact:
        raise AssertionError("Single-period fallback must not rely on a collapsed box trace.")

    with stats_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 2:
        raise AssertionError(f"Expected two stats rows for retrospective_1 year horizon, got {len(rows)}.")
    modes = {row.get("chart_mode") for row in rows}
    if modes != {"ofz_pd_single_period_strip_box"}:
        raise AssertionError(f"Unexpected chart_mode values: {sorted(str(mode) for mode in modes)}")
    for row in rows:
        if int(float(row.get("auction_count") or 0)) < 2:
            raise AssertionError("Single-period regression expects at least two OFZ-PD observations per period.")
        for column in ["yield_min_actual", "yield_median", "yield_max_actual"]:
            if not str(row.get(column, "")).strip():
                raise AssertionError(f"Stats export is missing {column}.")

    print("OFZ-PD single-period boxplot regression passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
