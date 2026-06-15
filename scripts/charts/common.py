"""Common pure helpers for chart builders."""

from __future__ import annotations

from typing import Any

import pandas as pd


def format_number_text(series: pd.Series, digits: int = 1) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    return numeric.map(lambda value: "" if pd.isna(value) else f"{value:,.{digits}f}".replace(",", " "))


def format_hover_number(value: Any, digits: int = 2) -> str:
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return ""
    return f"{float(numeric):,.{digits}f}".replace(",", " ")


def format_bln(value: Any, suffix: bool = True) -> str:
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return ""
    text = f"{float(numeric):,.1f}".replace(",", " ").replace(".", ",")
    return f"{text} \u043c\u043b\u0440\u0434 \u0440\u0443\u0431." if suffix else text


def format_percent_label(value: Any) -> str:
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return ""
    return f"{float(numeric) * 100:,.1f}".replace(",", " ").replace(".", ",")


def format_metric_value(value: Any, digits: int = 1) -> str:
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return ""
    return f"{float(numeric):,.{digits}f}".replace(",", " ").replace(".", ",")


def format_signed_metric_value(value: Any, digits: int = 1) -> str:
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return ""
    if abs(float(numeric)) < 10 ** (-digits):
        return f"{0:,.{digits}f}".replace(",", " ").replace(".", ",")
    sign = "+" if float(numeric) > 0 else ""
    return f"{sign}{float(numeric):,.{digits}f}".replace(",", " ").replace(".", ",")


def format_ru_number(value: Any, digits: int = 1) -> str:
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return ""
    return f"{float(numeric):,.{digits}f}".replace(",", " ").replace(".", ",")
