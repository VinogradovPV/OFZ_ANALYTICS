"""Style helpers for line charts with markers."""

from __future__ import annotations

from itertools import combinations
from typing import Any, Mapping, Sequence

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
    """Apply the line-marker style policy to a Plotly line+markers figure."""
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


def apply_line_marker_layout(
    fig: Any,
    title: str | None = None,
    show_yaxis_labels: bool = False,
) -> None:
    """Compatibility alias for the shared line-marker layout helper."""
    apply_reference_line_marker_layout(fig, title=title, show_yaxis_labels=show_yaxis_labels)


def apply_reference_line_marker_trace(trace: Any, color: str, text_position: str | None = None) -> None:
    """Style one line+markers Plotly trace according to the line-marker policy."""
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


def add_line_marker_trace(trace: Any, color: str, text_position: str | None = None) -> None:
    """Compatibility alias for the shared line-marker trace helper."""
    apply_reference_line_marker_trace(trace, color=color, text_position=text_position)


def format_reference_percent_label(value: object, decimals: int = 1) -> str:
    """Format a percent-like chart label for the reference line+marker style."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return ""
    return f"{float(numeric):.{decimals}f}"


def format_key_rate_pct(value: object) -> str:
    """Format Bank of Russia key rate labels with exactly two decimals."""
    return format_reference_percent_label(value, decimals=2)


def detect_label_collisions(
    row: Mapping[str, object] | pd.Series,
    value_columns: Sequence[str],
    threshold: float,
) -> dict[str, list[str]]:
    """Return columns whose values are too close for same-point labels."""
    numeric_values: dict[str, float] = {}
    for column in value_columns:
        value = pd.to_numeric(pd.Series([row.get(column)]), errors="coerce").iloc[0]
        if pd.notna(value):
            numeric_values[column] = float(value)

    collisions: dict[str, list[str]] = {column: [] for column in numeric_values}
    for left, right in combinations(numeric_values, 2):
        if abs(numeric_values[left] - numeric_values[right]) <= threshold:
            collisions[left].append(right)
            collisions[right].append(left)
    return {column: peers for column, peers in collisions.items() if peers}


def build_collision_safe_value_annotations(
    data: pd.DataFrame,
    series: Sequence[tuple[str, str, str, int, str]],
    *,
    x_column: str,
    max_dense_points: int = 24,
    collision_threshold: float | None = None,
) -> list[dict[str, Any]]:
    """Build value-label annotations with lane shifts for close line values."""
    y_columns = [value_column for _, value_column, _, _, _ in series]
    threshold = collision_threshold
    if threshold is None:
        threshold = _collision_threshold(data, y_columns)

    annotations: list[dict[str, Any]] = []
    for row_index, row in data.reset_index(drop=True).iterrows():
        collisions = detect_label_collisions(row, y_columns, threshold)
        previous_same_lane: dict[int, list[str]] = {1: [], -1: []}
        for series_key, value_column, _name, decimals, text_position in series:
            values = pd.to_numeric(data[value_column], errors="coerce")
            if row_index not in _visible_label_indexes(values, max_dense_points=max_dense_points):
                continue
            value = pd.to_numeric(pd.Series([row.get(value_column)]), errors="coerce").iloc[0]
            if pd.isna(value):
                continue
            text = format_key_rate_pct(value) if series_key == "key_rate" else format_reference_percent_label(value, decimals)
            if not text:
                continue

            direction = _label_direction(text_position)
            collided_peers = set(collisions.get(value_column, []))
            lane_index = sum(1 for peer in previous_same_lane[direction] if peer in collided_peers)
            previous_same_lane[direction].append(value_column)
            yshift = _label_base_shift(series_key, text_position) + direction * 14 * lane_index
            if collided_peers:
                yshift += direction * 4

            color = REFERENCE_LINE_MARKER_COLORS.get(series_key, "#1F2933")
            annotations.append(
                {
                    "x": row[x_column],
                    "y": float(value),
                    "text": text,
                    "showarrow": False,
                    "xanchor": "center",
                    "yanchor": "bottom" if direction > 0 else "top",
                    "yshift": yshift,
                    "font": {"color": color, "size": 11, "family": REFERENCE_FONT_FAMILY},
                    "bgcolor": "rgba(255,255,255,0.90)",
                    "bordercolor": "rgba(255,255,255,0.90)",
                    "borderpad": 1,
                    "name": f"value_label_{series_key}_{row_index}",
                }
            )
    return annotations


def _collision_threshold(data: pd.DataFrame, y_columns: Sequence[str]) -> float:
    values = pd.to_numeric(data[list(y_columns)].stack(), errors="coerce").dropna()
    if values.empty:
        return 0.25
    y_span = float(values.max() - values.min())
    return max(0.25, y_span * 0.025)


def _visible_label_indexes(values: pd.Series, max_dense_points: int) -> set[int]:
    if len(values) <= max_dense_points:
        return set(range(len(values)))
    valid = values.dropna()
    if valid.empty:
        return set()
    return {0, len(values) - 1, int(valid.idxmin()), int(valid.idxmax())}


def _label_direction(text_position: str) -> int:
    return -1 if text_position.startswith("bottom") else 1


def _label_base_shift(series_key: str, text_position: str) -> int:
    if series_key == "key_rate":
        return 30
    if _label_direction(text_position) < 0:
        return -20
    return 18
