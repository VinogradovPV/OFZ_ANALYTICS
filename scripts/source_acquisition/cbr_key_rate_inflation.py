"""Manual CBR key rate and inflation source parser."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = (
    "Дата",
    "Ключевая ставка, % годовых",
    "Инфляция, % г/г",
    "Цель по инфляции",
)
ORIGINAL_CBR_FILE_NAME = "Инфляция и ключевая ставка Банка России_F01_01_2019_T02_07_2026.xlsx"
MONTH_RE = re.compile(r"^(?P<month>\d{1,2})\.(?P<year>\d{4})$")
RU_MONTH_ABBR = {
    1: "Янв",
    2: "Фев",
    3: "Мар",
    4: "Апр",
    5: "Май",
    6: "Июн",
    7: "Июл",
    8: "Авг",
    9: "Сен",
    10: "Окт",
    11: "Ноя",
    12: "Дек",
}


def read_cbr_key_rate_workbook(path: Path) -> pd.DataFrame:
    """Read the first sheet from the manual CBR workbook."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"CBR key rate workbook not found: {source}")
    return pd.read_excel(source, sheet_name=0)


def normalize_cbr_key_rate_table(df: pd.DataFrame, source_file: Path) -> pd.DataFrame:
    """Normalize CBR monthly key rate and inflation data to a stable CSV contract."""
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"CBR workbook is missing required columns: {', '.join(missing)}")

    result = df.loc[:, list(REQUIRED_COLUMNS)].copy()
    result["month"] = result["Дата"].map(parse_cbr_month)
    for column in REQUIRED_COLUMNS[1:]:
        result[column] = pd.to_numeric(result[column], errors="coerce")

    result = result.rename(
        columns={
            "Ключевая ставка, % годовых": "key_rate_pct",
            "Инфляция, % г/г": "inflation_yoy_pct",
            "Цель по инфляции": "inflation_target_pct",
        }
    )
    result = result.dropna(subset=["month"]).copy()
    result["month"] = pd.to_datetime(result["month"])
    if result["month"].duplicated().any():
        duplicates = sorted(result.loc[result["month"].duplicated(), "month"].dt.strftime("%Y-%m").unique())
        raise ValueError(f"CBR workbook contains duplicate months: {', '.join(duplicates)}")

    numeric_columns = ["key_rate_pct", "inflation_yoy_pct", "inflation_target_pct"]
    if result[numeric_columns].isna().any().any():
        raise ValueError("CBR workbook contains non-numeric key rate or inflation values.")

    result = result.sort_values("month").reset_index(drop=True)
    min_month = result["month"].min().strftime("%Y-%m")
    max_month = result["month"].max().strftime("%Y-%m")
    source = Path(source_file)
    source_original_name = ORIGINAL_CBR_FILE_NAME if source.name.startswith("cbr_key_rate_inflation_") else source.name
    loaded_at = datetime.now(UTC).replace(microsecond=0).isoformat()

    result["month_label"] = result["month"].map(format_ru_month_label)
    result["month"] = result["month"].dt.strftime("%Y-%m-01")
    result["source_file"] = source.as_posix()
    result["source_original_name"] = source_original_name
    result["source_loaded_at"] = loaded_at
    result["source_min_month"] = min_month
    result["source_max_month"] = max_month

    return result[
        [
            "month",
            "month_label",
            "key_rate_pct",
            "inflation_yoy_pct",
            "inflation_target_pct",
            "source_file",
            "source_original_name",
            "source_loaded_at",
            "source_min_month",
            "source_max_month",
        ]
    ]


def write_cbr_key_rate_processed(input_path: Path, output_path: Path) -> Path:
    """Parse the manual workbook and write a reproducible processed monthly CSV."""
    normalized = normalize_cbr_key_rate_table(read_cbr_key_rate_workbook(input_path), input_path)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    normalized.to_csv(target, index=False, encoding="utf-8")
    return target


def parse_cbr_month(value: object) -> str:
    """Parse M.YYYY/MM.YYYY month text as the first day of month."""
    text = str(value).strip()
    match = MONTH_RE.match(text)
    if not match and "." in text:
        month_part, year_part = text.split(".", 1)
        if len(year_part) == 3 and year_part.startswith("20"):
            text = f"{month_part}.{year_part}0"
            match = MONTH_RE.match(text)
    if not match:
        raise ValueError(f"Invalid CBR month value: {text!r}")
    month = int(match.group("month"))
    year = int(match.group("year"))
    if month < 1 or month > 12:
        raise ValueError(f"Invalid CBR month number: {text!r}")
    return f"{year:04d}-{month:02d}-01"


def format_ru_month_label(value: object) -> str:
    timestamp = pd.to_datetime(value, errors="coerce")
    if pd.isna(timestamp):
        return ""
    return f"{RU_MONTH_ABBR[int(timestamp.month)]}-{str(int(timestamp.year))[-2:]}"
