"""Shared methodology for baseline OFZ yield metrics."""

from __future__ import annotations

import pandas as pd


BASE_YIELD_SCOPE = "ofz_pd_only"
BASE_YIELD_TITLE = "Помесячная средневзвешенная доходность ОФЗ-ПД"
OFZ_PD = "ОФЗ-ПД"
OFZ_PK = "ОФЗ-ПК"
OFZ_IN = "ОФЗ-ИН"


def security_type_series(df: pd.DataFrame) -> pd.Series:
    for column in ("security_type", "ofz_type"):
        if column in df.columns:
            return df[column].astype("string").map(_normalize_security_type)
    return pd.Series(pd.NA, index=df.index, dtype="string")


def _normalize_security_type(value: object) -> object:
    if value is None or value is pd.NA or value is pd.NaT:
        return pd.NA
    if isinstance(value, float) and pd.isna(value):
        return pd.NA
    normalized = str(value).strip().upper()
    if normalized in {OFZ_PD, OFZ_PK, OFZ_IN}:
        return normalized
    try:
        repaired = normalized.encode("cp1251").decode("utf-8").strip().upper()
    except (UnicodeEncodeError, UnicodeDecodeError):
        return normalized
    return repaired


def apply_base_yield_policy(
    df: pd.DataFrame,
    yield_columns: tuple[str, ...],
) -> pd.DataFrame:
    """Mark applicability and null non-comparable yields in analytical data."""
    result = df.copy()
    security_type = security_type_series(result)
    numeric_yields = [
        pd.to_numeric(result[column], errors="coerce")
        for column in yield_columns
        if column in result.columns
    ]
    if numeric_yields:
        has_numeric_yield = pd.concat(numeric_yields, axis=1).notna().any(axis=1)
    else:
        has_numeric_yield = pd.Series(False, index=result.index, dtype="bool")

    is_pd = security_type.eq(OFZ_PD).fillna(False)
    is_pk = security_type.eq(OFZ_PK).fillna(False)
    is_in = security_type.eq(OFZ_IN).fillna(False)
    result["yield_applicable"] = (is_pd & has_numeric_yield).astype(bool)

    reason = pd.Series(pd.NA, index=result.index, dtype="string")
    reason.loc[is_pk] = "ofz_pk_yield_not_applicable"
    reason.loc[is_in] = "ofz_in_separate_yield_scope"
    reason.loc[~is_pd & ~is_pk & ~is_in] = "non_ofz_pd_yield_scope"
    reason.loc[is_pd & ~has_numeric_yield] = "missing_or_non_numeric_yield"
    result["yield_exclusion_reason"] = reason
    result["yield_scope"] = BASE_YIELD_SCOPE

    for column in yield_columns:
        if column in result.columns:
            result[column] = pd.to_numeric(result[column], errors="coerce").where(is_pd)
    return result


def base_yield_cohort_mask(
    df: pd.DataFrame,
    yield_column: str,
    placement_column: str,
) -> pd.Series:
    """Select OFZ-PD rows with numeric yield and positive placement volume."""
    if yield_column not in df.columns or placement_column not in df.columns:
        return pd.Series(False, index=df.index, dtype="bool")
    yields = pd.to_numeric(df[yield_column], errors="coerce")
    placement = pd.to_numeric(df[placement_column], errors="coerce")
    return (
        security_type_series(df).eq(OFZ_PD).fillna(False)
        & yields.notna()
        & placement.notna()
        & placement.gt(0)
    )


def has_mixed_security_types(df: pd.DataFrame) -> bool:
    values = security_type_series(df).dropna()
    return bool(values.nunique() > 1)
