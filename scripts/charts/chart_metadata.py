"""Chart artifact metadata helpers shared by chart builders."""

from __future__ import annotations

from pathlib import Path

from scripts import config, report_params


def make_report_suffix(params: report_params.ReportParams) -> str:
    """Build the stable report suffix used in chart artifact names."""
    return (
        f"{params.period_type}_{params.aggregation_mode}_{params.report_date.isoformat()}_"
        f"retrospective_{params.retrospective_years}"
    )


def chart_data_dir_for_name(name: str) -> Path:
    """Return the target CSV-export directory for a chart name."""
    if (
        name.startswith("risk_quadrant")
        or name.startswith("demand_cutoff")
        or name.startswith("bid_to_cover")
        or name.startswith("discount_vs_demand")
        or name.startswith("yield_vs_demand")
    ):
        return config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR
    if (
        name.startswith("yield_vs_discount")
        or name.startswith("format_terms_scatter")
        or name.startswith("format_terms_aggregate_scatter")
    ):
        return config.EXPORTS_CHART_DATA_SCATTER_DIR
    if name.startswith("sankey"):
        return config.EXPORTS_CHART_DATA_SANKEY_DIR
    if name.startswith("yield_boxplot"):
        return config.EXPORTS_CHART_DATA_BOXPLOT_DIR
    if name == "ofz_pd_yield_key_rate":
        return config.EXPORTS_CHART_DATA_YIELD_DIR
    return config.EXPORTS_CHART_DATA_STRUCTURE_DIR
