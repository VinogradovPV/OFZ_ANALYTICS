"""Reference style helpers for line charts with markers."""

from __future__ import annotations

from typing import Any

import pandas as pd


REFERENCE_LINE_MARKER_COLORS = {
    "ofz_pd_yield_max": "#FF5D50",
    "ofz_pd_yield_min": "#00CE7E",
    "key_rate": "#BB88EF",
}
REFERENCE_TITLE_COLOR = "#001648"
REFERENCE_FONT_FAMILY = "Golos Text, Arial, sans-serif"
REFERENCE_LINE_WIDTH = 2.25
REFERENCE_MARKER_SIZE = 7
REFERENCE_MARKER_LINE_WIDTH = 1.5
REFERENCE_MARKER_FILL = "white"
REFERENCE_LEGEND_POSITION = "bottom"
REFERENCE_X_TICK_ANGLE = -45


def apply_reference_line_marker_layout(
    fig: Any,
    title: str | None = None,
    show_yaxis_labels: bool = False,
) -> None:
    """Apply the reference slide layout to a Plotly line+markers figure."""
    layout: dict[str, Any] = {
        "template": "plotly_white",
        "font": {"family": REFERENCE_FONT_FAMILY, "color": "#1F2933"},
        "legend": {
            "orientation": "h",
            "yanchor": "top",
            "y": -0.25,
            "xanchor": "center",
            "x": 0.5,
        },
        "legend_title_text": "",
        "separators": ", ",
        "margin": {"l": 56, "r": 32, "t": 90, "b": 110},
        "hovermode": "x unified",
    }
    if title is not None:
        layout["title"] = {
            "text": title,
            "font": {"family": REFERENCE_FONT_FAMILY, "color": REFERENCE_TITLE_COLOR, "size": 20},
            "x": 0,
            "xanchor": "left",
        }
    fig.update_layout(**layout)
    fig.update_xaxes(tickangle=REFERENCE_X_TICK_ANGLE, showgrid=False)
    fig.update_yaxes(showticklabels=show_yaxis_labels, gridcolor="#E6EAF0", zeroline=False)


def apply_reference_line_marker_trace(trace: Any, color: str, text_position: str | None = None) -> None:
    """Style one line+markers Plotly trace according to the reference slide."""
    update: dict[str, Any] = {
        "mode": "lines+markers+text" if getattr(trace, "text", None) is not None else "lines+markers",
        "line": {"color": color, "width": REFERENCE_LINE_WIDTH, "shape": "linear"},
        "marker": {
            "color": REFERENCE_MARKER_FILL,
            "size": REFERENCE_MARKER_SIZE,
            "line": {"color": color, "width": REFERENCE_MARKER_LINE_WIDTH},
        },
        "textfont": {"color": color, "family": REFERENCE_FONT_FAMILY, "size": 11},
    }
    if text_position:
        update["textposition"] = text_position
    trace.update(**update)


def format_reference_percent_label(value: object, decimals: int = 1) -> str:
    """Format a percent-like chart label for the reference line+marker style."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return ""
    return f"{float(numeric):.{decimals}f}"
