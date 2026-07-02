"""Smoke test for the reference line+marker style contract."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.charts import line_marker_style  # noqa: E402


def main() -> int:
    expected_colors = {
        "ofz_pd_yield_max": "#FF5D50",
        "ofz_pd_yield_min": "#00CE7E",
        "key_rate": "#BB88EF",
    }
    if line_marker_style.REFERENCE_LINE_MARKER_COLORS != expected_colors:
        raise AssertionError("Reference line marker colors changed.")
    if line_marker_style.REFERENCE_LINE_WIDTH != 2.25:
        raise AssertionError("Reference line width changed.")
    if line_marker_style.REFERENCE_MARKER_SIZE != 7:
        raise AssertionError("Reference marker size changed.")
    if line_marker_style.REFERENCE_MARKER_LINE_WIDTH != 1.5:
        raise AssertionError("Reference marker outline width changed.")
    if line_marker_style.REFERENCE_MARKER_FILL.lower() != "white":
        raise AssertionError("Reference marker fill changed.")

    chart_source = Path("scripts/06_build_charts.py").read_text(encoding="utf-8")
    required_tokens = [
        "build_ofz_pd_yield_key_rate_chart",
        "apply_reference_line_marker_layout",
        "apply_reference_line_marker_trace",
        "REFERENCE_LINE_MARKER_COLORS",
        "ofz_pd_yield_key_rate",
    ]
    missing = [token for token in required_tokens if token not in chart_source]
    if missing:
        raise AssertionError(f"Chart builder does not use reference style tokens: {', '.join(missing)}")

    print("Line+marker reference style smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
