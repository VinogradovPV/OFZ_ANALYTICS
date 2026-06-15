"""Shared HTML chart QA contract constants and result types."""

from __future__ import annotations

from dataclasses import dataclass

try:
    from scripts.scatter_chart_policy import MAX_SCATTER_LABELS
except Exception:  # pragma: no cover - fallback for isolated QA runs.
    MAX_SCATTER_LABELS = 30

MAX_YIELD_DISCOUNT_FACET_LABELS_PER_FACET = 3
MAX_YIELD_DISCOUNT_FACET_LABELS_TOTAL = 15
MAX_YIELD_DISCOUNT_MAIN_LABELS_TOTAL = 25
MAX_YIELD_DISCOUNT_OUTLIERS_LABELS_TOTAL = 30

RUSSIAN_AXIS_TOKENS = (
    "Период",
    "Год",
    "Месяц",
    "Доходность",
    "Объем",
    "Объём",
    "Спрос",
    "Предложение",
    "Размещение",
    "Вид ОФЗ",
    "Формат",
)

TECHNICAL_COLUMN_TOKENS = (
    "auction_date",
    "report_period_label",
    "report_period_start",
    "report_period_end",
    "issue_code",
    "ofz_type",
    "format_assumption_flag",
    "demand_volume",
    "supply_volume",
    "placement_volume",
    "weighted_avg_yield",
    "cutoff_yield",
    "cutoff_price",
    "weighted_avg_price",
    "maturity_bucket",
    "ratio_basis",
)

VOLUME_FILENAME_TOKENS = (
    "placement",
    "volume",
    "sankey",
    "maturity_structure",
    "format_structure",
    "monthly_heatmap",
)

SCATTER_FILENAME_TOKENS = (
    "risk_quadrant",
    "demand_cutoff",
    "yield_vs_demand",
    "discount_vs_demand",
    "discount_vs_revenue_gap",
    "format_terms_scatter",
    "format_terms_aggregate_scatter",
)

DISCOUNT_VS_DEMAND_FILENAME_TOKENS = (
    "discount_vs_demand",
)

REVENUE_CHART_PREFIXES = (
    "revenue_vs_nominal_by_period",
    "nominal_revenue_gap_by_period",
    "revenue_to_nominal_ratio",
    "monthly_revenue_vs_nominal",
    "monthly_nominal_revenue_gap",
    "revenue_gap_by_ofz_type",
    "revenue_gap_by_maturity",
    "format_nominal_revenue_gap",
    "discount_vs_revenue_gap",
)

STACKED_STRUCTURE_FILENAME_TOKENS = (
    "maturity_structure",
    "format_structure",
    "monthly_placement_by_maturity",
    "monthly_placement_by_format",
)

FORBIDDEN_ADJACENT_STRUCTURE_COLORS = ("#2EA3D8", "#E6D957")
SCATTER_LABEL_BUFFER = 5


@dataclass(frozen=True)
class QaResult:
    """Result of one HTML chart QA check."""

    name: str
    passed: bool
    message: str
