"""ЭТАП 2: очистка исходных данных аукционов ОФЗ."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, utils
else:
    from . import config, utils


RAW_EXTENSIONS = {".xlsx", ".xls", ".csv"}
FORMAT_REVIEW_START = pd.Timestamp("2024-01-01")

STANDARD_COLUMNS = [
    "source_file",
    "source_sheet",
    "source_row",
    "source_year",
    "quarter",
    "period",
    "auction_date",
    "format",
    "format_assumption_flag",
    "auction_format",
    "issue_code",
    "security_type",
    "maturity_date",
    "days_to_maturity",
    "offer_amount_mln_rub",
    "cutoff_price_pct",
    "weighted_avg_price_pct",
    "cutoff_yield_pct",
    "weighted_avg_yield_pct",
    "demand_amount_mln_rub",
    "placement_amount_mln_rub",
    "proceeds_mln_rub",
    "demand_satisfaction_ratio",
    "demand_available",
    "yield_available",
    "failed_or_no_deal",
    "marker_fields",
    "data_quality_flag",
    "processing_timestamp",
]

NUMERIC_COLUMNS = [
    "days_to_maturity",
    "offer_amount_mln_rub",
    "cutoff_price_pct",
    "weighted_avg_price_pct",
    "cutoff_yield_pct",
    "weighted_avg_yield_pct",
    "demand_amount_mln_rub",
    "placement_amount_mln_rub",
    "proceeds_mln_rub",
    "demand_satisfaction_ratio",
]


@dataclass(frozen=True)
class RawTable:
    path: Path
    sheet_name: str | int
    header_row_index: int | None
    data: pd.DataFrame


def main() -> None:
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт этапа 2: очистка данных")

    raw_files = list_raw_files(config.DATA_RAW_DIR)
    logger.info("Найдено raw-файлов для очистки: %s", len(raw_files))

    tables = read_raw_tables(raw_files, logger)
    cleaned_parts: list[pd.DataFrame] = []
    for table in tables:
        cleaned = clean_table(table)
        logger.info(
            "Очищено строк: %s из %s / %s",
            len(cleaned),
            table.path.name,
            table.sheet_name,
        )
        if not cleaned.empty:
            cleaned_parts.append(cleaned)

    if cleaned_parts:
        result = pd.concat(cleaned_parts, ignore_index=True)
    else:
        result = pd.DataFrame(columns=STANDARD_COLUMNS)

    before_dedup = len(result)
    result = result.drop_duplicates().reset_index(drop=True)
    removed_duplicates = before_dedup - len(result)
    result = result.reindex(columns=STANDARD_COLUMNS)

    config.DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    result.to_csv(config.OFZ_AUCTIONS_CLEAN_CSV, index=False, encoding="utf-8")

    report = build_report(
        raw_files=raw_files,
        tables=tables,
        cleaned=result,
        rows_before_dedup=before_dedup,
        removed_duplicates=removed_duplicates,
    )
    utils.write_markdown(config.DATA_CLEANING_REPORT_DOC, report)

    logger.info("Clean dataset записан: %s", config.OFZ_AUCTIONS_CLEAN_CSV)
    logger.info("Отчет очистки записан: %s", config.DATA_CLEANING_REPORT_DOC)
    logger.info("Этап 2 завершен")


def list_raw_files(raw_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in raw_dir.iterdir()
        if path.is_file() and path.suffix.lower() in RAW_EXTENSIONS
    )


def read_raw_tables(raw_files: list[Path], logger: Any) -> list[RawTable]:
    tables: list[RawTable] = []
    for path in raw_files:
        suffix = path.suffix.lower()
        try:
            if suffix in {".xlsx", ".xls"}:
                tables.extend(read_excel_tables(path))
            elif suffix == ".csv":
                tables.append(read_csv_table(path))
        except Exception:
            logger.exception("Не удалось прочитать raw-файл: %s", path)
    return tables


def read_excel_tables(path: Path) -> list[RawTable]:
    excel_file = pd.ExcelFile(path)
    tables: list[RawTable] = []
    for sheet_name in excel_file.sheet_names:
        raw = pd.read_excel(path, sheet_name=sheet_name, header=None)
        header_row_index = detect_header_row(raw)
        data = normalize_table(raw, header_row_index)
        tables.append(RawTable(path, sheet_name, header_row_index, data))
    return tables


def read_csv_table(path: Path) -> RawTable:
    try:
        data = pd.read_csv(path)
    except UnicodeDecodeError:
        data = pd.read_csv(path, encoding="cp1251")

    data = data.copy()
    data.columns = make_unique_column_names(str(column).strip() for column in data.columns)
    data["source_row"] = range(2, len(data) + 2)
    return RawTable(path, "CSV", 0, data)


def detect_header_row(raw: pd.DataFrame) -> int | None:
    best_index: int | None = None
    best_score = 0
    header_patterns = [
        r"дата",
        r"код\s+выпуска",
        r"тип\s+бумаги",
        r"объем|объ[её]м",
        r"спрос",
        r"доход",
        r"погаш",
        r"формат",
    ]

    for index, row in raw.head(25).iterrows():
        values = " ".join(str(value).strip() for value in row.dropna().tolist())
        if not values:
            continue

        score = sum(
            1 for pattern in header_patterns if re.search(pattern, values, re.IGNORECASE)
        )
        if score > best_score:
            best_index = int(str(index))
            best_score = score

    return best_index if best_score >= 3 else None


def normalize_table(raw: pd.DataFrame, header_row_index: int | None) -> pd.DataFrame:
    if raw.empty:
        return raw.copy()

    if header_row_index is None:
        data = raw.copy()
        data.columns = [f"column_{index + 1}" for index in range(len(data.columns))]
        data["source_row"] = range(1, len(data) + 1)
        return data.dropna(how="all").reset_index(drop=True)

    header_values = raw.iloc[header_row_index].tolist()
    columns = [
        make_column_name(value, index)
        for index, value in enumerate(header_values)
    ]

    data = raw.iloc[header_row_index + 1 :].copy()
    data.columns = make_unique_column_names(columns)
    data["source_row"] = range(header_row_index + 2, header_row_index + 2 + len(data))
    return data.dropna(how="all").reset_index(drop=True)


def make_column_name(value: Any, index: int) -> str:
    if pd.isna(value):
        return f"column_{index + 1}"

    name = re.sub(r"\s+", " ", str(value).strip())
    return name if name else f"column_{index + 1}"


def make_unique_column_names(columns: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: dict[str, int] = {}

    for column in columns:
        name = str(column) if str(column) else "column"
        count = seen.get(name, 0)
        seen[name] = count + 1
        result.append(f"{name}_{count + 1}" if count else name)

    return result


def clean_table(table: RawTable) -> pd.DataFrame:
    df = table.data.copy()
    if df.empty:
        return pd.DataFrame(columns=STANDARD_COLUMNS)

    raw_filtered = remove_service_rows(df)
    df = normalize_missing_markers(raw_filtered)
    column_map = build_column_map(df.columns)
    rows = pd.DataFrame(index=df.index)
    rows["source_file"] = table.path.name
    rows["source_sheet"] = table.sheet_name
    rows["source_row"] = get_series(df, "source_row")

    rows["auction_date"] = parse_date(get_source_column(df, column_map, "auction_date"))
    rows["maturity_date"] = parse_date(get_source_column(df, column_map, "maturity_date"))
    rows["issue_code"] = clean_string(get_source_column(df, column_map, "issue_code"))
    rows["security_type"] = clean_string(get_source_column(df, column_map, "security_type"))

    for target in NUMERIC_COLUMNS:
        if target == "demand_satisfaction_ratio":
            source = get_source_column(df, column_map, target)
        else:
            source = get_source_column(df, column_map, target)
        rows[target] = utils.safe_to_numeric(source)

    raw_format = clean_string(get_source_column(df, column_map, "format"))
    rows["format"], rows["format_assumption_flag"] = normalize_format(
        raw_format,
        rows["auction_date"],
        has_format_column=column_map.get("format") is not None,
    )
    rows["auction_format"] = rows["format"]

    rows["source_year"] = rows["auction_date"].dt.year.astype("Int64")
    rows["quarter"] = rows["auction_date"].dt.quarter.astype("Int64")
    rows["period"] = "Q" + rows["quarter"].astype("string") + "-" + rows["source_year"].astype("string")

    rows["demand_available"] = rows["demand_amount_mln_rub"].notna()
    rows["yield_available"] = (
        rows["cutoff_yield_pct"].notna() | rows["weighted_avg_yield_pct"].notna()
    )
    rows["failed_or_no_deal"] = detect_failed_or_no_deal(rows)
    rows["marker_fields"] = build_marker_fields(raw_filtered, column_map)
    rows["data_quality_flag"] = build_data_quality_flag(rows)
    rows["processing_timestamp"] = datetime.now().isoformat(timespec="seconds")

    rows = rows[is_relevant_auction_row(rows)].copy()
    rows["auction_date"] = rows["auction_date"].dt.strftime("%Y-%m-%d")
    rows["maturity_date"] = rows["maturity_date"].dt.strftime("%Y-%m-%d")
    rows = rows.where(pd.notna(rows), None)
    return rows.reindex(columns=STANDARD_COLUMNS)


def normalize_missing_markers(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    missing_markers = {"", "-", "—", "–", "−", "****", "-****", "nan", "none", "null", "n/a"}
    for column in result.columns:
        if pd.api.types.is_object_dtype(result[column]) or pd.api.types.is_string_dtype(result[column]):
            values = result[column].astype("string").str.strip()
            result[column] = result[column].mask(values.str.lower().isin(missing_markers), pd.NA)
    return result


def remove_service_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    result = df.copy()
    source_row = result["source_row"] if "source_row" in result.columns else pd.Series(pd.NA, index=result.index)
    text = result.drop(columns=["source_row"], errors="ignore").apply(
        lambda row: " ".join(str(value).strip().lower() for value in row.dropna().tolist()),
        axis=1,
    )
    non_empty_cells = result.drop(columns=["source_row"], errors="ignore").notna().sum(axis=1)
    service_mask = (
        text.str.fullmatch(r"\d+(\s+\d+)*", na=False)
        | text.str.contains(r"единиц[аы]? измерения|млн\.?\s*руб|процент|%|дн(?:ей|я)", regex=True, na=False)
        | text.str.contains(r"^итого\b|\bитого\b|^всего\b|\bвсего\b", regex=True, na=False)
        | text.str.contains(r"^\*|^\d+\)|примечани|сноск|расчет", regex=True, na=False)
        | (non_empty_cells <= 1)
    )
    cleaned = result.loc[~service_mask].copy()
    if "source_row" in cleaned.columns:
        cleaned["source_row"] = source_row.loc[cleaned.index]
    return cleaned


def build_column_map(columns: Iterable[str]) -> dict[str, str | None]:
    names = list(columns)
    return {
        "auction_date": find_column(names, [r"^дата$", r"дата аукциона"]),
        "format": find_column(names, [r"формат"]),
        "issue_code": find_column(names, [r"код\s+выпуска", r"выпуск"]),
        "security_type": find_column(names, [r"тип\s+бумаги", r"офз"]),
        "maturity_date": find_column(names, [r"дата погашения", r"погаш"]),
        "days_to_maturity": find_column(names, [r"дней до погашения", r"срок"]),
        "offer_amount_mln_rub": find_column(names, [r"объем предложения", r"объ[её]м предложения"]),
        "cutoff_price_pct": find_column(names, [r"цена отсечения"]),
        "weighted_avg_price_pct": find_column(names, [r"цена средневзвешенная"]),
        "cutoff_yield_pct": find_column(names, [r"доходность по цене отсечения"]),
        "weighted_avg_yield_pct": find_column(names, [r"доходность по средневзве"]),
        "demand_amount_mln_rub": find_column(names, [r"совокупный объем спроса", r"спрос"]),
        "placement_amount_mln_rub": find_column(names, [r"объем размещения"]),
        "proceeds_mln_rub": find_column(names, [r"объем выручки", r"выруч"]),
        "demand_satisfaction_ratio": find_column(names, [r"коэффициент удовлетворения"]),
    }


def find_column(columns: list[str], patterns: list[str]) -> str | None:
    for pattern in patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        for column in columns:
            if regex.search(str(column)):
                return str(column)
    return None


def get_source_column(df: pd.DataFrame, column_map: dict[str, str | None], key: str) -> pd.Series:
    column = column_map.get(key)
    if column is None or column not in df.columns:
        return pd.Series([pd.NA] * len(df), index=df.index, dtype="object")
    return df[column]


def get_series(df: pd.DataFrame, column: str) -> pd.Series:
    if column in df.columns:
        return df[column]
    return pd.Series([pd.NA] * len(df), index=df.index, dtype="object")


def parse_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce", dayfirst=True)


def clean_string(series: pd.Series) -> pd.Series:
    result = (
        series.astype("string")
        .str.strip()
        .replace("", pd.NA)
        .replace("-", pd.NA)
        .replace("—", pd.NA)
        .replace("–", pd.NA)
        .replace("nan", pd.NA)
        .replace("None", pd.NA)
    )
    return result


def normalize_format(
    raw_format: pd.Series,
    auction_date: pd.Series,
    has_format_column: bool,
) -> tuple[pd.Series, pd.Series]:
    result = raw_format.astype("string").str.strip()
    result = result.replace("", pd.NA).replace("nan", pd.NA).replace("None", pd.NA)
    flag = pd.Series(["explicit"] * len(result), index=result.index, dtype="object")

    if not has_format_column:
        result = pd.Series(["Аукцион"] * len(result), index=result.index, dtype="string")
        flag[:] = "assumed_missing_column_auction"
        return result, flag

    missing = result.isna()
    before_2024 = auction_date < FORMAT_REVIEW_START
    result = result.mask(missing & before_2024, "Аукцион")
    flag = flag.mask(missing & before_2024, "assumed_pre_2024_auction")
    flag = flag.mask(missing & ~before_2024, "requires_review")
    flag = flag.mask(~missing, "explicit")
    return result, flag


def detect_failed_or_no_deal(rows: pd.DataFrame) -> pd.Series:
    placement_missing_or_zero = rows["placement_amount_mln_rub"].fillna(0) <= 0
    price_missing = rows["cutoff_price_pct"].isna() & rows["weighted_avg_price_pct"].isna()
    return placement_missing_or_zero | price_missing


def build_data_quality_flag(rows: pd.DataFrame) -> pd.Series:
    flags: list[str] = []
    for _, row in rows.iterrows():
        row_flags: list[str] = []
        if pd.isna(row.get("auction_date")):
            row_flags.append("missing_auction_date")
        if pd.isna(row.get("issue_code")):
            row_flags.append("missing_issue_code")
        if pd.isna(row.get("format")) or row.get("format_assumption_flag") == "requires_review":
            row_flags.append("format_requires_review")
        if not bool(row.get("demand_available", False)):
            row_flags.append("missing_demand")
        if not bool(row.get("yield_available", False)):
            row_flags.append("missing_yield")
        if bool(row.get("failed_or_no_deal", False)):
            row_flags.append("failed_or_no_deal")
        marker_fields = str(row.get("marker_fields") or "").strip()
        if marker_fields:
            row_flags.append(f"source_markers:{marker_fields}")
        flags.append("|".join(row_flags) if row_flags else "ok")
    return pd.Series(flags, index=rows.index, dtype="object")


def build_marker_fields(df: pd.DataFrame, column_map: dict[str, str | None]) -> pd.Series:
    marker_columns = [
        target
        for target, column in column_map.items()
        if column is not None and target in NUMERIC_COLUMNS
    ]
    result: list[str] = []
    markers = {"-", "-****", "****", "—"}

    for index in df.index:
        fields: list[str] = []
        for target in marker_columns:
            column = column_map[target]
            value = df.at[index, column] if column in df.columns else pd.NA
            if str(value).strip() in markers:
                fields.append(target)
        result.append("|".join(fields) if fields else "")

    return pd.Series(result, index=df.index, dtype="object")


def is_relevant_auction_row(rows: pd.DataFrame) -> pd.Series:
    has_date = rows["auction_date"].notna()
    plausible_date = rows["auction_date"].dt.year.between(1990, 2100)
    has_issue = rows["issue_code"].astype("string").str.contains(
        r"\d{5}RMFS", case=False, na=False
    )
    has_security = rows["security_type"].astype("string").str.contains(
        "ОФЗ", case=False, na=False
    )
    not_total = ~rows["issue_code"].astype("string").str.contains(
        "итого|total", case=False, na=False
    )
    return has_date & plausible_date & has_issue & has_security & not_total


def build_report(
    raw_files: list[Path],
    tables: list[RawTable],
    cleaned: pd.DataFrame,
    rows_before_dedup: int,
    removed_duplicates: int,
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = [
        "# Отчет об очистке данных",
        "",
        f"Дата формирования: {now}",
        "",
        "## Краткий вывод",
        "",
        f"Прочитано raw-файлов: {len(raw_files)}.",
        f"Прочитано таблиц/листов: {len(tables)}.",
        f"Строк до удаления полных дубликатов: {rows_before_dedup}.",
        f"Строк после удаления полных дубликатов: {len(cleaned)}.",
        f"Удалено полных дубликатов: {removed_duplicates}.",
        "",
        "Исходные данные в `data/raw/` не изменялись.",
        "",
    ]

    append_sources_section(lines, raw_files, tables)
    append_schema_section(lines, cleaned)
    append_format_section(lines, cleaned)
    append_quality_section(lines, cleaned)
    append_outputs_section(lines)
    return "\n".join(lines)


def append_sources_section(lines: list[str], raw_files: list[Path], tables: list[RawTable]) -> None:
    lines.extend(["## Источники", "", "| Файл | Размер, байт | Таблиц/листов |", "|---|---:|---:|"])
    table_counts = pd.Series([table.path.name for table in tables]).value_counts().to_dict()
    for path in raw_files:
        size = f"{path.stat().st_size:,}".replace(",", " ")
        lines.append(f"| `{path.name}` | {size} | {table_counts.get(path.name, 0)} |")
    lines.append("")


def append_schema_section(lines: list[str], cleaned: pd.DataFrame) -> None:
    lines.extend(["## Нормализованная схема", "", "| Колонка | Тип pandas | Пропусков |", "|---|---|---:|"])
    for column in cleaned.columns:
        missing = int(cleaned[column].isna().sum())
        lines.append(f"| `{column}` | `{cleaned[column].dtype}` | {missing} |")
    lines.append("")


def append_format_section(lines: list[str], cleaned: pd.DataFrame) -> None:
    lines.extend(["## Правило по столбцу `Формат`", ""])
    lines.extend(
        [
            "- Если столбец `Формат` присутствует и значение заполнено, `format_assumption_flag = \"explicit\"`.",
            "- Если столбец `Формат` отсутствует, `format = \"Аукцион\"`, `format_assumption_flag = \"assumed_missing_column_auction\"`.",
            "- Если `format` пустой и дата ранее `2024-01-01`, `format = \"Аукцион\"`, `format_assumption_flag = \"assumed_pre_2024_auction\"`.",
            "- Если `format` пустой начиная с `2024-01-01`, `format_assumption_flag = \"requires_review\"`.",
            "- Допустимые значения флага: `explicit`, `assumed_missing_column_auction`, `assumed_pre_2024_auction`, `requires_review`.",
            "",
        ]
    )

    if cleaned.empty:
        lines.append("Clean dataset пуст.")
        lines.append("")
        return

    lines.extend(["### Распределение `format`", "", "| format | Строк |", "|---|---:|"])
    for value, count in cleaned["format"].value_counts(dropna=False).items():
        lines.append(f"| `{value}` | {count} |")
    lines.append("")

    lines.extend(
        [
            "### Распределение `format_assumption_flag`",
            "",
            "| format_assumption_flag | Строк |",
            "|---|---:|",
        ]
    )
    for value, count in cleaned["format_assumption_flag"].value_counts(dropna=False).items():
        lines.append(f"| `{value}` | {count} |")
    lines.append("")


def append_quality_section(lines: list[str], cleaned: pd.DataFrame) -> None:
    lines.extend(["## Контроль качества", ""])
    if cleaned.empty:
        lines.append("- Clean dataset пуст.")
        lines.append("")
        return

    lines.append(f"- Годы в `auction_date`: {format_values(cleaned['source_year'].dropna().unique())}.")
    lines.append(f"- Кварталы: {format_values(cleaned['quarter'].dropna().unique())}.")
    lines.append(f"- Полных дубликатов после очистки: {int(cleaned.duplicated().sum())}.")
    lines.append(f"- Строк `requires_review`: {int((cleaned['format_assumption_flag'] == 'requires_review').sum())}.")
    if "data_quality_flag" in cleaned.columns:
        lines.append("- Распределение `data_quality_flag`:")
        for value, count in cleaned["data_quality_flag"].value_counts(dropna=False).items():
            lines.append(f"  - `{value}`: {count}")
    lines.append("")

    normalized_columns = {
        "доходность": ["cutoff_yield_pct", "weighted_avg_yield_pct"],
        "спрос": ["demand_amount_mln_rub", "demand_satisfaction_ratio", "demand_available"],
        "предложение": ["offer_amount_mln_rub"],
        "объем размещения": ["placement_amount_mln_rub", "proceeds_mln_rub"],
        "срок обращения": ["maturity_date", "days_to_maturity"],
    }
    lines.extend(
        [
            "## Нормализованные аналитические колонки",
            "",
            "| Направление | Колонки | Статус |",
            "|---|---|---|",
        ]
    )
    for domain, columns in normalized_columns.items():
        present = [column for column in columns if column in cleaned.columns]
        missing = [column for column in columns if column not in cleaned.columns]
        status = "ok" if not missing else f"missing: {', '.join(missing)}"
        formatted = ", ".join(f"`{column}`" for column in present) if present else "-"
        lines.append(f"| {domain} | {formatted} | {status} |")
    lines.append("")


def append_outputs_section(lines: list[str]) -> None:
    lines.extend(
        [
            "## Выходные артефакты",
            "",
            f"- `{config.OFZ_AUCTIONS_CLEAN_CSV.relative_to(config.ROOT_DIR).as_posix()}`",
            f"- `{config.DATA_CLEANING_REPORT_DOC.relative_to(config.ROOT_DIR).as_posix()}`",
            f"- `{config.PIPELINE_LOG_PATH.relative_to(config.ROOT_DIR).as_posix()}`",
            "",
        ]
    )


def format_values(values: Any) -> str:
    normalized = sorted(str(value) for value in values)
    return ", ".join(f"`{value}`" for value in normalized) if normalized else "-"


if __name__ == "__main__":
    main()
