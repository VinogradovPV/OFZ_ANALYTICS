"""Общие вспомогательные функции для аналитического пайплайна ОФЗ."""

from __future__ import annotations

import logging
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    from . import config
except ImportError:
    import config  # type: ignore


def setup_logging(log_path: Path | None = None, level: int = logging.INFO) -> logging.Logger:
    """Настроить консольное и файловое логирование для скриптов пайплайна."""
    ensure_directories()
    target_log_path = Path(log_path or config.PIPELINE_LOG_PATH)
    target_log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("ofz_analytics")
    logger.setLevel(level)
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()
    logger.propagate = False

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(target_log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)
    logger.addHandler(stream_handler)

    return logger


def ensure_directories() -> None:
    """Создать нужные выходные каталоги проекта, если они отсутствуют."""
    for directory in config.REQUIRED_DIRECTORIES:
        Path(directory).mkdir(parents=True, exist_ok=True)


def read_table_file(path: str | Path, **kwargs: Any) -> pd.DataFrame:
    """Прочитать данные CSV, TSV, Excel или parquet в DataFrame."""
    table_path = Path(path)
    suffix = table_path.suffix.lower()
    suffixes = [item.lower() for item in table_path.suffixes]

    if suffix == ".csv" or suffixes[-2:] in ([".csv", ".gz"], [".csv", ".zip"]):
        return pd.read_csv(table_path, **kwargs)
    if suffix == ".tsv" or suffixes[-2:] in ([".tsv", ".gz"], [".tsv", ".zip"]):
        return pd.read_csv(table_path, sep="\t", **kwargs)
    if suffix in {".xlsx", ".xls", ".xlsm"}:
        return pd.read_excel(table_path, **kwargs)
    if suffix == ".parquet":
        return pd.read_parquet(table_path, **kwargs)

    raise ValueError(f"Unsupported table file extension: {''.join(suffixes)}")


def write_markdown(path: str | Path, content: str) -> Path:
    """Записать Markdown в UTF-8 и вернуть выходной путь."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return output_path


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Вернуть копию со стабильными именами колонок в snake_case."""
    normalized = []
    seen: set[str] = set()

    for column in df.columns:
        name = str(column).strip().lower()
        name = name.replace("\u2116", "number")
        name = re.sub(r"[%]+", " pct ", name)
        name = re.sub(r"[^0-9a-zA-Z\u0430-\u044f\u0410-\u042f]+", "_", name)
        name = re.sub(r"_+", "_", name).strip("_")
        if not name:
            name = "column"
        normalized.append(_unique_column_name(name, seen))

    result = df.copy()
    result.columns = normalized
    return result


def safe_to_numeric(series: pd.Series) -> pd.Series:
    """Преобразовать Series в числа, считая служебные маркеры пропусками."""
    cleaned = (
        series.astype("string")
        .str.strip()
        .str.replace("\u00a0", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace("\u2212", "-", regex=False)
        .str.replace("\u2013", "-", regex=False)
        .str.replace("\u2014", "-", regex=False)
        .str.replace(",", ".", regex=False)
    )
    missing_markers = {"", "-", "****", "-****", "nan", "none", "null", "n/a"}
    cleaned = cleaned.mask(cleaned.str.lower().isin(missing_markers))
    return pd.to_numeric(cleaned, errors="coerce")


def detect_date_columns(df: pd.DataFrame) -> list[str]:
    """Найти вероятные колонки дат по имени и возможности разбора значений."""
    date_columns: list[str] = []
    name_pattern = re.compile(
        r"(date|\u0434\u0430\u0442\u0430|period|\u043f\u0435\u0440\u0438\u043e\u0434)",
        flags=re.IGNORECASE,
    )

    for column in df.columns:
        series = df[column]
        by_name = bool(name_pattern.search(str(column)))

        if pd.api.types.is_datetime64_any_dtype(series):
            date_columns.append(str(column))
            continue

        if pd.api.types.is_numeric_dtype(series):
            if by_name:
                date_columns.append(str(column))
            continue

        non_null = series.dropna()
        if non_null.empty:
            if by_name:
                date_columns.append(str(column))
            continue

        parsed = pd.to_datetime(non_null, errors="coerce", dayfirst=True)
        parse_ratio = float(parsed.notna().mean()) if len(parsed) else 0.0

        if by_name or parse_ratio >= 0.8:
            date_columns.append(str(column))

    return date_columns


def basic_dataframe_profile(df: pd.DataFrame) -> dict[str, Any]:
    """Построить компактный JSON-сериализуемый профиль DataFrame."""
    duplicate_rows = _safe_duplicate_count(df)
    memory_usage_bytes = int(df.memory_usage(deep=True).sum())

    columns: dict[str, dict[str, Any]] = {}
    for column in df.columns:
        series = df[column]
        columns[str(column)] = {
            "dtype": str(series.dtype),
            "non_null": int(series.notna().sum()),
            "missing": int(series.isna().sum()),
            "missing_pct": float(series.isna().mean()) if len(series) else 0.0,
            "unique": _safe_nunique(series),
            "sample_values": [
                _json_safe_value(value)
                for value in series.dropna().head(5).tolist()
            ],
        }

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "duplicate_rows": duplicate_rows,
        "memory_usage_bytes": memory_usage_bytes,
        "date_columns": detect_date_columns(df),
        "columns_profile": columns,
    }


def backup_file(path: str | Path) -> Path | None:
    """Создать резервную копию с меткой времени рядом с существующим файлом."""
    source = Path(path)
    if not source.exists():
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = source.with_name(f"{source.stem}.backup_{timestamp}{source.suffix}")
    shutil.copy2(source, backup_path)
    return backup_path


def compare_dataframes(df_old: pd.DataFrame, df_new: pd.DataFrame) -> dict[str, Any]:
    """Сравнить два DataFrame и вернуть компактную сводку различий."""
    old = df_old.copy()
    new = df_new.copy()

    old_columns = list(map(str, old.columns))
    new_columns = list(map(str, new.columns))
    old.columns = old_columns
    new.columns = new_columns
    common_columns = [column for column in old_columns if column in new_columns]

    old_common = old[common_columns].reset_index(drop=True) if common_columns else pd.DataFrame()
    new_common = new[common_columns].reset_index(drop=True) if common_columns else pd.DataFrame()

    same_shape = old.shape == new.shape
    same_columns = old_columns == new_columns
    same_values = False
    changed_cells = None

    if same_shape and same_columns:
        old_for_compare = _comparison_safe_dataframe(old.reset_index(drop=True))
        new_for_compare = _comparison_safe_dataframe(new.reset_index(drop=True))
        comparison = old_for_compare.compare(new_for_compare, keep_shape=False)
        same_values = comparison.empty
        changed_cells = int(comparison.size / 2)

    old_hash_counts = _row_hash_counts(old_common) if common_columns else pd.Series(dtype="int64")
    new_hash_counts = _row_hash_counts(new_common) if common_columns else pd.Series(dtype="int64")
    old_only_rows = old_hash_counts.subtract(new_hash_counts, fill_value=0).clip(lower=0)
    new_only_rows = new_hash_counts.subtract(old_hash_counts, fill_value=0).clip(lower=0)

    return {
        "old_shape": tuple(map(int, old.shape)),
        "new_shape": tuple(map(int, new.shape)),
        "same_shape": bool(same_shape),
        "same_columns": bool(same_columns),
        "same_values": bool(same_values),
        "columns_added": [column for column in new_columns if column not in old_columns],
        "columns_removed": [column for column in old_columns if column not in new_columns],
        "common_columns": common_columns,
        "changed_cells": changed_cells,
        "rows_only_in_old": int(old_only_rows.sum()),
        "rows_only_in_new": int(new_only_rows.sum()),
        "old_duplicate_rows": _safe_duplicate_count(old),
        "new_duplicate_rows": _safe_duplicate_count(new),
    }


def _unique_column_name(name: str, seen: set[str]) -> str:
    candidate = name
    suffix = 2
    while candidate in seen:
        candidate = f"{name}_{suffix}"
        suffix += 1
    seen.add(candidate)
    return candidate


def _safe_duplicate_count(df: pd.DataFrame) -> int:
    try:
        return int(df.duplicated().sum())
    except TypeError:
        comparable = df.map(_comparison_safe_value)
        return int(comparable.duplicated().sum())


def _safe_nunique(series: pd.Series) -> int:
    try:
        return int(series.nunique(dropna=True))
    except TypeError:
        comparable = series.dropna().map(_comparison_safe_value)
        return int(comparable.nunique(dropna=True))


def _row_hash_counts(df: pd.DataFrame) -> pd.Series:
    try:
        row_hashes = pd.util.hash_pandas_object(df, index=False).astype("uint64")
    except TypeError:
        comparable = df.map(_comparison_safe_value)
        row_hashes = pd.util.hash_pandas_object(comparable, index=False).astype("uint64")
    return row_hashes.value_counts()


def _comparison_safe_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df.map(_comparison_safe_value)


def _comparison_safe_value(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return tuple(_comparison_safe_value(item) for item in value.tolist())
    if isinstance(value, list):
        return tuple(_comparison_safe_value(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_comparison_safe_value(item) for item in value)
    if isinstance(value, set):
        return tuple(
            sorted((_comparison_safe_value(item) for item in value), key=repr)
        )
    if isinstance(value, dict):
        return tuple(
            sorted((str(key), _comparison_safe_value(item)) for key, item in value.items())
        )
    return value


def _json_safe_value(value: Any) -> Any:
    """Преобразовать скаляры и контейнеры pandas/numpy в JSON-безопасные объекты."""
    if isinstance(value, np.ndarray):
        return [_json_safe_value(item) for item in value.tolist()]
    if isinstance(value, list):
        return [_json_safe_value(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe_value(item) for item in value]
    if isinstance(value, set):
        return [_json_safe_value(item) for item in sorted(value, key=repr)]
    if isinstance(value, dict):
        return {str(key): _json_safe_value(item) for key, item in value.items()}
    missing = pd.isna(value)
    if isinstance(missing, (bool, np.bool_)) and missing:
        return None
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    return value
