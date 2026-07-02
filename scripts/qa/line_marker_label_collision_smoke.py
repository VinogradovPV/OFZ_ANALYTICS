"""Smoke test for collision-aware line-marker value labels."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.charts.line_marker_style import (  # noqa: E402
    build_collision_safe_value_annotations,
    detect_label_collisions,
    format_key_rate_pct,
)


def main() -> int:
    data = pd.DataFrame(
        [
            {
                "period_month": "2026-02-01",
                "period_label": "Фев-26",
                "ofz_pd_yield_max_pct": 15.25,
                "ofz_pd_yield_min_pct": 14.73,
                "key_rate_month_end_pct": 15.50,
            },
            {
                "period_month": "2026-03-01",
                "period_label": "Мар-26",
                "ofz_pd_yield_max_pct": 14.85,
                "ofz_pd_yield_min_pct": 13.75,
                "key_rate_month_end_pct": 15.00,
            },
            {
                "period_month": "2026-04-01",
                "period_label": "Апр-26",
                "ofz_pd_yield_max_pct": 14.87,
                "ofz_pd_yield_min_pct": 14.18,
                "key_rate_month_end_pct": 14.50,
            },
        ]
    )
    series = [
        ("ofz_pd_yield_max", "ofz_pd_yield_max_pct", "Максимальная доходность ОФЗ-ПД", 2, "top center"),
        ("ofz_pd_yield_min", "ofz_pd_yield_min_pct", "Минимальная доходность ОФЗ-ПД", 2, "bottom center"),
        ("key_rate", "key_rate_month_end_pct", "Ключевая ставка Банка России", 2, "top center"),
    ]

    march = data.loc[data["period_month"].eq("2026-03-01")].iloc[0]
    collisions = detect_label_collisions(
        march,
        ["ofz_pd_yield_max_pct", "ofz_pd_yield_min_pct", "key_rate_month_end_pct"],
        threshold=0.25,
    )
    if collisions.get("ofz_pd_yield_max_pct") != ["key_rate_month_end_pct"]:
        raise AssertionError(f"March 2026 max/key-rate collision not detected: {collisions}")
    if format_key_rate_pct(march["key_rate_month_end_pct"]) != "15.00":
        raise AssertionError("Key rate label must use exactly two decimals.")

    annotations = build_collision_safe_value_annotations(data, series, x_column="period_label")
    march_annotations = [annotation for annotation in annotations if annotation["x"] == "Мар-26"]
    by_name = {annotation["name"]: annotation for annotation in march_annotations}
    max_label = by_name["value_label_ofz_pd_yield_max_1"]
    min_label = by_name["value_label_ofz_pd_yield_min_1"]
    key_rate_label = by_name["value_label_key_rate_1"]
    if max_label["yshift"] == key_rate_label["yshift"]:
        raise AssertionError("March 2026 max/key-rate labels must use different lanes.")
    if key_rate_label["yshift"] <= max_label["yshift"]:
        raise AssertionError("Key rate label must be shifted above the colliding max-yield label.")
    if min_label["yshift"] >= 0:
        raise AssertionError("Minimum yield label must stay below its marker.")
    if key_rate_label["text"] != "15.00":
        raise AssertionError(f"Unexpected key rate label text: {key_rate_label['text']}")
    if not all(annotation.get("bgcolor") == "rgba(255,255,255,0.90)" for annotation in march_annotations):
        raise AssertionError("Value labels must use a white background line guard.")

    try:
        import plotly.graph_objects as go
    except ImportError as exc:  # pragma: no cover - Plotly is a project dependency.
        raise AssertionError("Plotly is required for annotation HTML smoke.") from exc

    fig = go.Figure()
    for annotation in annotations:
        fig.add_annotation(**annotation)
    html = fig.to_html(include_plotlyjs=False)
    if '"annotations"' not in html or "value_label_key_rate_1" not in html:
        raise AssertionError("Value labels must be serialized as Plotly layout annotations.")

    print("Line-marker label collision smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
