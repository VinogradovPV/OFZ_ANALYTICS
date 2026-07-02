"""Smoke checks for chart artifact metadata helpers."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import config, report_params  # noqa: E402
from scripts.charts.chart_metadata import chart_data_dir_for_name, make_report_suffix  # noqa: E402


def main() -> int:
    params = report_params.ReportParams(
        report_date=date(2026, 5, 1),
        retrospective_years=4,
        period_type="month",
        aggregation_mode="cumulative",
        periods=[],
    )
    assert make_report_suffix(params) == "month_cumulative_2026-05-01_retrospective_4"

    expected = {
        "risk_quadrant": config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR,
        "demand_cutoff_explanation": config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR,
        "bid_to_cover": config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR,
        "discount_vs_demand": config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR,
        "yield_vs_demand": config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR,
        "yield_vs_discount": config.EXPORTS_CHART_DATA_SCATTER_DIR,
        "yield_vs_discount_facet": config.EXPORTS_CHART_DATA_SCATTER_DIR,
        "format_terms_scatter": config.EXPORTS_CHART_DATA_SCATTER_DIR,
        "format_terms_aggregate_scatter": config.EXPORTS_CHART_DATA_SCATTER_DIR,
        "sankey_structure": config.EXPORTS_CHART_DATA_SANKEY_DIR,
        "yield_boxplot_by_ofz_type": config.EXPORTS_CHART_DATA_BOXPLOT_DIR,
        "format_structure": config.EXPORTS_CHART_DATA_STRUCTURE_DIR,
    }
    for name, directory in expected.items():
        actual = chart_data_dir_for_name(name)
        assert actual == directory, f"{name}: {actual} != {directory}"

    print("Chart metadata smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
