"""Shared visual regression contract constants and result types."""

from __future__ import annotations

from dataclasses import dataclass

VOLUME_FILENAME_TOKENS = (
    "placement",
    "volume",
    "sankey",
    "maturity_structure",
    "format_structure",
    "monthly_heatmap",
)

STACKED_STRUCTURE_FILENAME_TOKENS = (
    "maturity_structure",
    "format_structure",
    "monthly_placement_by_maturity",
    "monthly_placement_by_format",
)

YIELD_DISCOUNT_FACET_MAX_LABELS_PER_PANEL = 3
YIELD_DISCOUNT_FACET_MAX_LABELS_TOTAL = 15
YIELD_DISCOUNT_MAIN_MAX_LABELS_TOTAL = 25
YIELD_DISCOUNT_OUTLIERS_MAX_LABELS_TOTAL = 30
YIELD_DISCOUNT_LABEL_BUFFER = 5
YIELD_DISCOUNT_CLUSTER_WARN_THRESHOLD = 8


@dataclass(frozen=True)
class VisualCheck:
    """Result of one visual regression check."""

    file: str
    check: str
    status: str
    message: str
