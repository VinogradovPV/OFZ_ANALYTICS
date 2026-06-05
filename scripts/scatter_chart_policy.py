"""Единая политика подписей и ratio basis для scatter-графиков."""

from __future__ import annotations

from typing import Any

import pandas as pd


MAX_SCATTER_LABELS = 30

RATIO_BASIS = {
    "_demand_to_placement": {
        "basis": "demand_volume / placement_volume",
        "axis": "Спрос / объем размещения",
        "hover": "Спрос / размещение",
    },
    "demand_to_placement_ratio": {
        "basis": "demand_volume / placement_volume",
        "axis": "Спрос / объем размещения",
        "hover": "Спрос / размещение",
    },
    "_bid_to_cover": {
        "basis": "demand_volume / supply_volume",
        "axis": "Спрос / предложение",
        "hover": "Спрос / предложение",
    },
    "bid_to_cover_ratio": {
        "basis": "demand_volume / supply_volume",
        "axis": "Спрос / предложение",
        "hover": "Спрос / предложение",
    },
}


def ratio_basis_for(column: str) -> str:
    """Вернуть формулу ratio для hover/export."""
    return RATIO_BASIS.get(column, {}).get("basis", column)


def ratio_axis_title(column: str, fallback: str = "") -> str:
    """Вернуть русскую подпись оси ratio."""
    return RATIO_BASIS.get(column, {}).get("axis", fallback or column)


def add_scatter_labels(
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    *,
    placement_column: str = "_placement",
    yield_column: str | None = None,
    label_column: str = "issue_code",
    max_labels: int = MAX_SCATTER_LABELS,
) -> pd.DataFrame:
    """Подписать только ключевые наблюдения и сохранить причины подписи.

    Подписи выбираются по правилам: выбросы X/Y, около-нулевая доходность, top
    placement, top X/Y, целевой период и флаги качества данных. Hover остается
    основным источником детализации.
    """
    result = data.copy()
    result["scatter_label_reason"] = ""
    result["scatter_label"] = ""

    reasons: dict[Any, set[str]] = {}

    def add_reason(indexes: list[Any], reason: str) -> None:
        for index in indexes:
            if index in result.index:
                reasons.setdefault(index, set()).add(reason)

    x_values = pd.to_numeric(result[x_column], errors="coerce") if x_column in result.columns else pd.Series(dtype=float)
    y_values = pd.to_numeric(result[y_column], errors="coerce") if y_column in result.columns else pd.Series(dtype=float)

    add_reason(outlier_indexes(x_values), "x_outlier")
    add_reason(outlier_indexes(y_values), "yield_outlier")
    add_reason(top_indexes(result, placement_column, 8), "top placement_volume")
    add_reason(top_indexes(result, x_column, 8), "top x_value")
    add_reason(top_indexes(result, y_column, 8), "top y_value")

    effective_yield_column = yield_column or y_column
    if effective_yield_column in result.columns:
        yield_values = pd.to_numeric(result[effective_yield_column], errors="coerce")
        add_reason(yield_values.loc[yield_values.abs() <= 0.01].index.tolist(), "zero_yield_check")

    if "is_target_period" in result.columns:
        target_mask = result["is_target_period"].astype("string").str.lower().isin({"true", "1", "yes"})
        add_reason(result.loc[target_mask].index.tolist(), "target_period")

    if "data_quality_flag" in result.columns:
        quality = result["data_quality_flag"].fillna("").astype(str).str.strip()
        flagged = quality.loc[quality.ne("") & quality.str.lower().ne("ok")]
        add_reason(flagged.index.tolist(), "data_quality_flag")

    selected = sorted(
        reasons,
        key=lambda index: (
            -len(reasons[index]),
            -safe_float(x_values.get(index)),
            -safe_float(y_values.get(index)),
        ),
    )[:max_labels]

    for index in selected:
        label = str(result.at[index, label_column]) if label_column in result.columns else ""
        if not label or label.lower() == "nan":
            label = str(index)
        result.at[index, "scatter_label"] = label
        result.at[index, "scatter_label_reason"] = "; ".join(sorted(reasons[index]))

    result["scatter_textposition"] = dynamic_text_positions(result, x_column, y_column)
    return result


def outlier_indexes(values: pd.Series) -> list[Any]:
    """Вернуть индексы IQR-выбросов; если их нет, вернуть пустой список."""
    numeric = pd.to_numeric(values, errors="coerce").dropna()
    if numeric.empty:
        return []
    q1 = numeric.quantile(0.25)
    q3 = numeric.quantile(0.75)
    iqr = q3 - q1
    if pd.isna(iqr) or float(iqr) == 0:
        return []
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return numeric.loc[(numeric < lower) | (numeric > upper)].index.tolist()


def top_indexes(data: pd.DataFrame, column: str, n: int) -> list[Any]:
    """Вернуть индексы крупнейших значений колонки."""
    if column not in data.columns:
        return []
    return pd.to_numeric(data[column], errors="coerce").nlargest(n).index.tolist()


def dynamic_text_positions(data: pd.DataFrame, x_column: str, y_column: str) -> pd.Series:
    """Разнести подписи по квадрантам относительно медиан X/Y."""
    x_values = pd.to_numeric(data[x_column], errors="coerce") if x_column in data.columns else pd.Series(index=data.index)
    y_values = pd.to_numeric(data[y_column], errors="coerce") if y_column in data.columns else pd.Series(index=data.index)
    x_median = x_values.median()
    y_median = y_values.median()
    result = pd.Series("bottom right", index=data.index, dtype="string")
    high_x = x_values >= x_median
    high_y = y_values >= y_median
    result.loc[high_x & high_y] = "top left"
    result.loc[~high_x & high_y] = "top right"
    result.loc[high_x & ~high_y] = "bottom left"
    return result


def outlier_subset(data: pd.DataFrame) -> pd.DataFrame:
    """Вернуть только подписанные/проблемные точки для outliers-версии."""
    if "scatter_label_reason" not in data.columns:
        return data.iloc[0:0].copy()
    return data.loc[data["scatter_label_reason"].fillna("").astype(str).str.strip().ne("")].copy()


def safe_float(value: Any) -> float:
    """Преобразовать значение в число для сортировки, NaN считать минимальным."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return float("-inf")
    return float(numeric)
