"""Low-risk export helpers shared by chart builders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def ensure_directories(*directories: Path) -> None:
    """Create output directories without changing path selection policy."""
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def write_chart_artifacts(
    figure: Any,
    dataframe: pd.DataFrame,
    html_path: Path,
    csv_path: Path,
    *,
    csv_encoding: str,
) -> None:
    """Write one chart HTML file and its CSV export."""
    html_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    figure.write_html(html_path)
    dataframe.to_csv(csv_path, index=False, encoding=csv_encoding)
