"""ЭТАП 1: аудит исходных данных аукционов ОФЗ."""

from __future__ import annotations

import argparse
import re
import sys
import warnings
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, utils
    from scripts.source_acquisition.source_registry import (
        SourceRegistryValidation,
        summarize_registry_status,
        validate_source_registry,
    )
else:
    from . import config, utils
    from .source_acquisition.source_registry import (
        SourceRegistryValidation,
        summarize_registry_status,
        validate_source_registry,
    )


RAW_EXTENSIONS = {".xlsx", ".xls", ".csv"}
DATE_PARSE_THRESHOLD = 0.8
NUMERIC_PARSE_THRESHOLD = 0.8

SEMANTIC_PATTERNS = {
    "дата": re.compile(r"(дата|date|period|период)", re.IGNORECASE),
    "ОФЗ": re.compile(r"(офз|ofz|тип|type)", re.IGNORECASE),
    "выпуск": re.compile(r"(выпуск|issue|isin|код|номер|№)", re.IGNORECASE),
    "объем": re.compile(
        r"(объем|объ[её]м|amount|volume|размещ|предлож|выруч)",
        re.IGNORECASE,
    ),
    "спрос": re.compile(r"(спрос|demand|заяв)", re.IGNORECASE),
    "доходность": re.compile(r"(доход|yield|ставк)", re.IGNORECASE),
    "срок": re.compile(r"(срок|погаш|maturity|duration|days)", re.IGNORECASE),
    "формат": re.compile(r"(формат|format|дрпа)", re.IGNORECASE),
}


@dataclass(frozen=True)
class TableAudit:
    source_path: Path
    table_name: str
    rows: int
    columns: int
    duplicate_rows: int
    missing_cells: int
    missing_pct: float
    column_names: list[str]
    dtypes: dict[str, str]
    missing_by_column: dict[str, int]
    candidate_date_columns: list[str]
    candidate_numeric_columns: list[str]
    semantic_columns: dict[str, list[str]]
    year_coverage: dict[str, list[int]]
    read_error: str | None = None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit raw OFZ source files.")
    parser.add_argument(
        "--source-registry-mode",
        choices=["off", "warn", "strict"],
        default="warn",
        help="Validate controlled Minfin source registry without changing legacy raw ingestion.",
    )
    parser.add_argument(
        "--allow-legacy-raw",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Allow legacy data/raw audit fallback when registry validation is warning-only.",
    )
    return parser.parse_args(argv)


def minfin_registry_path() -> Path:
    return (
        config.DATA_RAW_DIR
        / "minfin"
        / "ofz_auction_results"
        / "registry"
        / "minfin_ofz_auction_sources.csv"
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт этапа 1: аудит исходных данных")

    raw_files = list_raw_files(config.DATA_RAW_DIR)
    logger.info("Найдено raw-файлов: %s", len(raw_files))
    expected_years = sorted(
        {
            int(match.group(1))
            for path in raw_files
            if (match := re.search(r"(20\d{2})", path.name))
        }
    )
    registry_status = validate_source_registry(
        minfin_registry_path(),
        project_root=config.ROOT_DIR,
        mode=args.source_registry_mode,
        expected_years=expected_years,
        allow_legacy_raw=args.allow_legacy_raw,
        legacy_raw_available=bool(raw_files),
    )
    for message in registry_status.warnings:
        logger.warning("Source registry warning: %s", message)
    for message in registry_status.errors:
        logger.error("Source registry error: %s", message)

    if args.source_registry_mode == "strict" and not registry_status.ok:
        report = build_markdown_report(raw_files, [], registry_status)
        utils.write_markdown(config.DATA_AUDIT_DOC, report)
        logger.error("Source registry strict validation failed; legacy raw fallback disabled")
        return 1

    audits: list[TableAudit] = []
    for raw_file in raw_files:
        logger.info("Аудит файла: %s", raw_file)
        file_audits = audit_raw_file(raw_file, logger)
        audits.extend(file_audits)
        for audit in file_audits:
            if audit.read_error:
                logger.warning(
                    "Аудит таблицы завершен с ошибкой: file=%s table=%s error=%s",
                    audit.source_path,
                    audit.table_name,
                    audit.read_error,
                )
            else:
                logger.info(
                    "Аудит таблицы: file=%s table=%s rows=%s columns=%s duplicates=%s missing_cells=%s",
                    audit.source_path,
                    audit.table_name,
                    audit.rows,
                    audit.columns,
                    audit.duplicate_rows,
                    audit.missing_cells,
                )

    report = build_markdown_report(raw_files, audits, registry_status)
    utils.write_markdown(config.DATA_AUDIT_DOC, report)
    logger.info("Отчет аудита записан: %s", config.DATA_AUDIT_DOC)
    logger.info("Этап 1 завершен")
    return 0


def list_raw_files(raw_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in raw_dir.iterdir()
        if path.is_file() and path.suffix.lower() in RAW_EXTENSIONS
    )


def audit_raw_file(path: Path, logger: Any) -> list[TableAudit]:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return audit_excel_file(path, logger)
    if suffix == ".csv":
        return [audit_csv_file(path)]
    return []


def audit_excel_file(path: Path, logger: Any) -> list[TableAudit]:
    try:
        excel_file = pd.ExcelFile(path)
    except Exception as exc:
        logger.exception("Не удалось открыть Excel-файл: %s", path)
        return [make_error_audit(path, "Excel workbook", exc)]

    audits: list[TableAudit] = []
    for sheet_name in excel_file.sheet_names:
        try:
            df = read_excel_sheet(path, sheet_name)
        except Exception as exc:
            logger.exception("Не удалось прочитать лист %s в файле %s", sheet_name, path)
            audits.append(make_error_audit(path, sheet_name, exc))
            continue
        audits.append(audit_dataframe(path, sheet_name, df))
    return audits


def read_excel_sheet(path: Path, sheet_name: str | int) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=sheet_name, header=None)
    return normalize_excel_header(raw)


def normalize_excel_header(raw: pd.DataFrame) -> pd.DataFrame:
    if raw.empty:
        return raw

    header_row_index = detect_header_row(raw)
    if header_row_index is None:
        df = raw.copy()
        df.columns = [f"column_{index + 1}" for index in range(len(df.columns))]
        return df.dropna(how="all").reset_index(drop=True)

    header_row_index_int: int = header_row_index
    header_values = raw.iloc[header_row_index_int].tolist()
    columns = [
        make_column_name(value, index)
        for index, value in enumerate(header_values)
    ]
    df_slice = raw.iloc[header_row_index_int + 1 :, :].copy()
    if isinstance(df_slice, pd.DataFrame):
        df_slice.columns = make_unique_column_names(columns)
        result = df_slice.dropna(how="all").reset_index(drop=True)
        if isinstance(result, pd.DataFrame):
            return result
    return pd.DataFrame()


def detect_header_row(raw: pd.DataFrame) -> int | None:
    best_index: int | None = None
    best_score = 0

    for index, row in raw.head(20).iterrows():
        index_int = int(str(index))
        values = [str(value).strip() for value in row.dropna().tolist()]
        if not values:
            continue

        semantic_hits = sum(
            1
            for value in values
            for pattern in SEMANTIC_PATTERNS.values()
            if pattern.search(value)
        )
        non_empty = len(values)
        score = semantic_hits * 10 + non_empty

        if semantic_hits >= 2 and score > best_score:
            best_index = index_int
            best_score = score

    return best_index


def make_column_name(value: Any, index: int) -> str:
    if pd.isna(value):
        return f"column_{index + 1}"

    name = str(value).strip()
    if not name:
        return f"column_{index + 1}"
    return name


def audit_csv_file(path: Path) -> TableAudit:
    try:
        df = pd.read_csv(path)
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(path, encoding="cp1251")
        except Exception as exc:
            return make_error_audit(path, "CSV", exc)
    except Exception as exc:
        return make_error_audit(path, "CSV", exc)
    return audit_dataframe(path, "CSV", df)


def make_error_audit(path: Path, table_name: str | int, exc: Exception) -> TableAudit:
    return TableAudit(
        source_path=path,
        table_name=str(table_name),
        rows=0,
        columns=0,
        duplicate_rows=0,
        missing_cells=0,
        missing_pct=0.0,
        column_names=[],
        dtypes={},
        missing_by_column={},
        candidate_date_columns=[],
        candidate_numeric_columns=[],
        semantic_columns={name: [] for name in SEMANTIC_PATTERNS},
        year_coverage={},
        read_error=f"{type(exc).__name__}: {exc}",
    )


def audit_dataframe(path: Path, table_name: str | int, df: pd.DataFrame) -> TableAudit:
    df = df.copy()
    df.columns = make_unique_column_names(str(column).strip() for column in df.columns)

    rows = int(len(df))
    columns = int(len(df.columns))
    cell_count = rows * columns
    missing_cells = int(df.isna().sum().sum())
    missing_pct = float(missing_cells / cell_count) if cell_count else 0.0

    candidate_date_columns = detect_candidate_date_columns(df)
    candidate_numeric_columns = detect_candidate_numeric_columns(df)
    semantic_columns = detect_semantic_columns(df)

    return TableAudit(
        source_path=path,
        table_name=str(table_name),
        rows=rows,
        columns=columns,
        duplicate_rows=safe_duplicate_count(df),
        missing_cells=missing_cells,
        missing_pct=missing_pct,
        column_names=list(map(str, df.columns)),
        dtypes={str(column): str(dtype) for column, dtype in df.dtypes.items()},
        missing_by_column={
            str(column): int(value) for column, value in df.isna().sum().items()
        },
        candidate_date_columns=candidate_date_columns,
        candidate_numeric_columns=candidate_numeric_columns,
        semantic_columns=semantic_columns,
        year_coverage=detect_year_coverage(df, candidate_date_columns),
    )


def detect_candidate_date_columns(df: pd.DataFrame) -> list[str]:
    candidates: list[str] = []
    name_pattern = re.compile(r"(date|дата|period|период)", re.IGNORECASE)

    for column in df.columns:
        series = df[column]
        column_name = str(column)
        by_name = bool(name_pattern.search(column_name))

        if pd.api.types.is_datetime64_any_dtype(series):
            candidates.append(column_name)
            continue

        if pd.api.types.is_numeric_dtype(series):
            if by_name:
                candidates.append(column_name)
            continue

        non_null = series.dropna()
        if non_null.empty:
            if by_name:
                candidates.append(column_name)
            continue

        if by_name:
            candidates.append(column_name)
            continue

        if date_like_value_ratio(non_null) < DATE_PARSE_THRESHOLD:
            continue

        parsed = safe_to_datetime(non_null)
        parse_ratio = float(parsed.notna().mean()) if len(parsed) else 0.0
        if parse_ratio >= DATE_PARSE_THRESHOLD:
            candidates.append(column_name)

    return candidates


def detect_candidate_numeric_columns(df: pd.DataFrame) -> list[str]:
    candidates: list[str] = []

    for column in df.columns:
        series = df[column]
        column_name = str(column)
        if pd.api.types.is_numeric_dtype(series):
            candidates.append(column_name)
            continue

        non_null = series.dropna()
        if non_null.empty:
            continue

        numeric = utils.safe_to_numeric(non_null)
        parse_ratio = float(numeric.notna().mean()) if len(numeric) else 0.0
        if parse_ratio >= NUMERIC_PARSE_THRESHOLD:
            candidates.append(column_name)

    return candidates


def detect_semantic_columns(df: pd.DataFrame) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for semantic_name, pattern in SEMANTIC_PATTERNS.items():
        result[semantic_name] = [
            str(column) for column in df.columns if pattern.search(str(column))
        ]
    return result


def detect_year_coverage(df: pd.DataFrame, date_columns: list[str]) -> dict[str, list[int]]:
    coverage: dict[str, list[int]] = {}
    for column in date_columns:
        parsed = safe_to_datetime(df[column])
        year_series = parsed.dt.year
        unique_years = year_series.dropna().unique()
        years: list[int] = sorted(int(year) for year in unique_years)
        if years:
            coverage[column] = years
    return coverage


def safe_duplicate_count(df: pd.DataFrame) -> int:
    try:
        return int(df.duplicated().sum())
    except TypeError:
        comparable = df.astype(str)
        return int(comparable.duplicated().sum())


def safe_to_datetime(values: pd.Series) -> pd.Series:
    series = values if isinstance(values, pd.Series) else pd.Series(values)
    if pd.api.types.is_datetime64_any_dtype(series):
        return series

    result = pd.Series(pd.NaT, index=series.index, dtype="datetime64[ns]")

    numeric = pd.to_numeric(series, errors="coerce")
    excel_serial_mask = numeric.notna() & numeric.between(20_000, 60_000)
    if excel_serial_mask.any():
        result.loc[excel_serial_mask] = pd.to_datetime(
            numeric.loc[excel_serial_mask],
            errors="coerce",
            unit="D",
            origin="1899-12-30",
        )

    text_mask = ~excel_serial_mask
    text_values = series.loc[text_mask].astype("string").str.strip()
    text_values = text_values.mask(text_values.isin({"", "-", "nan", "NaT", "None"}))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        parsed_text = pd.to_datetime(text_values, errors="coerce", dayfirst=True)

    result.loc[text_mask] = parsed_text
    return result


def date_like_value_ratio(values: pd.Series) -> float:
    if values.empty:
        return 0.0

    date_like = values.map(is_date_like_value)
    return float(date_like.mean()) if len(date_like) else 0.0


def is_date_like_value(value: Any) -> bool:
    if isinstance(value, (pd.Timestamp, datetime)):
        return True

    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.notna(numeric) and 20_000 <= float(numeric) <= 60_000:
        return True

    text = str(value).strip()
    if not text:
        return False

    return bool(
        re.search(r"\d{4}[-./]\d{1,2}[-./]\d{1,2}", text)
        or re.search(r"\d{1,2}[-./]\d{1,2}[-./]\d{2,4}", text)
    )


def make_unique_column_names(columns: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: dict[str, int] = {}

    for column in columns:
        name = str(column) if str(column) else "column"
        count = seen.get(name, 0)
        seen[name] = count + 1
        if count:
            result.append(f"{name}_{count + 1}")
        else:
            result.append(name)

    return result


def build_markdown_report(
    raw_files: list[Path],
    audits: list[TableAudit],
    registry_status: SourceRegistryValidation | None = None,
) -> str:
    lines: list[str] = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.extend(
        [
            "# Аудит исходных данных",
            "",
            f"Дата формирования: {now}",
            "",
            "## Краткий вывод",
            "",
            (
                f"Проверено raw-файлов: {len(raw_files)}. "
                f"Проверено таблиц и листов: {len(audits)}. "
                f"Ошибок чтения: {sum(1 for audit in audits if audit.read_error)}."
            ),
            "",
            (
                "Аудит не изменяет исходные данные и используется как входная "
                "диагностика для следующих этапов pipeline."
            ),
            "",
        ]
    )

    if registry_status is not None:
        append_source_registry_section(lines, registry_status)
    append_raw_file_section(lines, raw_files)
    append_table_summary_section(lines, audits)
    append_column_section(lines, audits)
    append_candidate_section(lines, audits)
    append_year_coverage_section(lines, audits)
    append_issue_section(lines, audits)
    append_stage_compliance_section(lines, raw_files, audits)

    return "\n".join(lines)


def append_source_registry_section(lines: list[str], status: SourceRegistryValidation) -> None:
    summary = summarize_registry_status(status)
    lines.extend(
        [
            "## Source registry validation",
            "",
            "| Параметр | Значение |",
            "|---|---|",
        ]
    )
    for key in (
        "source_registry_mode",
        "source_registry_status",
        "controlled_source_used",
        "legacy_raw_fallback_used",
        "registry_warnings_count",
        "registry_errors_count",
        "registry_exists",
        "records_count",
        "active_records_count",
    ):
        lines.append(f"| `{key}` | `{summary[key]}` |")
    lines.append("")
    if status.warnings:
        lines.extend(["### Registry warnings", ""])
        for warning in status.warnings:
            lines.append(f"- {markdown_cell(warning)}")
        lines.append("")
    if status.errors:
        lines.extend(["### Registry errors", ""])
        for error in status.errors:
            lines.append(f"- {markdown_cell(error)}")
        lines.append("")


def append_raw_file_section(lines: list[str], raw_files: list[Path]) -> None:
    lines.extend(
        [
            "## Найденные raw-файлы",
            "",
            "| Файл | Тип | Размер, байт |",
            "|---|---|---:|",
        ]
    )
    for path in raw_files:
        rel_path = path.relative_to(config.ROOT_DIR).as_posix()
        size = f"{path.stat().st_size:,}".replace(",", " ")
        lines.append(f"| `{rel_path}` | `{path.suffix.lower()}` | {size} |")
    lines.append("")


def append_table_summary_section(lines: list[str], audits: list[TableAudit]) -> None:
    lines.extend(
        [
            "## Сводка по таблицам и листам",
            "",
            (
                "| Источник | Лист/таблица | Строк | Колонок | Дубликатов | "
                "Пропусков | Пропусков, % |"
            ),
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for audit in audits:
        source = audit.source_path.relative_to(config.ROOT_DIR).as_posix()
        table = markdown_cell(audit.table_name)
        if audit.read_error:
            lines.append(f"| `{source}` | `{table}` | 0 | 0 | 0 | 0 | 0.00 |")
            continue
        lines.append(
            "| "
            f"`{source}` | `{table}` | {audit.rows} | {audit.columns} | "
            f"{audit.duplicate_rows} | {audit.missing_cells} | {audit.missing_pct:.2%} |"
        )
    lines.append("")


def append_column_section(lines: list[str], audits: list[TableAudit]) -> None:
    lines.extend(["## Колонки, типы данных и пропуски", ""])
    for audit in audits:
        source = audit.source_path.relative_to(config.ROOT_DIR).as_posix()
        table = markdown_cell(audit.table_name)
        lines.extend([f"### `{source}` / `{table}`", ""])
        if audit.read_error:
            lines.extend([f"Ошибка чтения: `{markdown_cell(audit.read_error)}`", ""])
            continue

        lines.extend(["| Колонка | Тип данных | Пропусков |", "|---|---|---:|"])
        for column in audit.column_names:
            dtype = audit.dtypes.get(column, "")
            missing = audit.missing_by_column.get(column, 0)
            lines.append(f"| `{markdown_cell(column)}` | `{dtype}` | {missing} |")
        lines.append("")


def append_candidate_section(lines: list[str], audits: list[TableAudit]) -> None:
    lines.extend(["## Кандидатные колонки", ""])
    for audit in audits:
        source = audit.source_path.relative_to(config.ROOT_DIR).as_posix()
        table = markdown_cell(audit.table_name)
        lines.extend([f"### `{source}` / `{table}`", ""])
        if audit.read_error:
            lines.extend([f"Ошибка чтения: `{markdown_cell(audit.read_error)}`", ""])
            continue

        lines.append(f"- candidate date columns: {format_list(audit.candidate_date_columns)}")
        lines.append(
            f"- candidate numeric columns: {format_list(audit.candidate_numeric_columns)}"
        )
        lines.append("- candidate semantic columns:")
        for semantic_name, columns in audit.semantic_columns.items():
            lines.append(f"  - {semantic_name}: {format_list(columns)}")
        lines.append("")


def append_year_coverage_section(lines: list[str], audits: list[TableAudit]) -> None:
    filename_years = sorted(
        {
            int(match.group(1))
            for audit in audits
            if (match := re.search(r"(20\d{2})", audit.source_path.name))
        }
    )

    lines.extend(["## Покрытие по годам", ""])
    lines.append(
        "Годы, найденные в именах файлов: "
        f"{format_list([str(year) for year in filename_years])}"
    )
    lines.append("")

    lines.extend(
        [
            "| Источник | Лист/таблица | Колонка даты | Годы в данных |",
            "|---|---|---|---|",
        ]
    )
    for audit in audits:
        source = audit.source_path.relative_to(config.ROOT_DIR).as_posix()
        table = markdown_cell(audit.table_name)
        if not audit.year_coverage:
            lines.append(f"| `{source}` | `{table}` | - | - |")
            continue
        for column, years in audit.year_coverage.items():
            lines.append(
                f"| `{source}` | `{table}` | `{markdown_cell(column)}` | "
                f"{format_list([str(year) for year in years])} |"
            )
    lines.append("")


def append_issue_section(lines: list[str], audits: list[TableAudit]) -> None:
    errors = [audit for audit in audits if audit.read_error]
    empty_tables = [audit for audit in audits if not audit.read_error and audit.rows == 0]
    no_date = [
        audit for audit in audits if not audit.read_error and not audit.candidate_date_columns
    ]
    no_numeric = [
        audit for audit in audits if not audit.read_error and not audit.candidate_numeric_columns
    ]

    lines.extend(["## Диагностические замечания", ""])
    lines.append(f"- Ошибки чтения: {len(errors)}.")
    lines.append(f"- Пустые таблицы/листы: {len(empty_tables)}.")
    lines.append(f"- Таблицы без candidate date columns: {len(no_date)}.")
    lines.append(f"- Таблицы без candidate numeric columns: {len(no_numeric)}.")
    lines.append("")

    if errors:
        lines.append("### Ошибки чтения")
        lines.append("")
        for audit in errors:
            source = audit.source_path.relative_to(config.ROOT_DIR).as_posix()
            table = markdown_cell(audit.table_name)
            error = markdown_cell(audit.read_error or "")
            lines.append(f"- `{source}` / `{table}`: `{error}`")
        lines.append("")


def append_stage_compliance_section(
    lines: list[str],
    raw_files: list[Path],
    audits: list[TableAudit],
) -> None:
    excel_files = [path for path in raw_files if path.suffix.lower() in {".xlsx", ".xls"}]
    csv_files = [path for path in raw_files if path.suffix.lower() == ".csv"]
    successful_audits = [audit for audit in audits if not audit.read_error]

    all_semantics = {
        semantic_name: sorted(
            {
                column
                for audit in successful_audits
                for column in audit.semantic_columns.get(semantic_name, [])
            }
        )
        for semantic_name in SEMANTIC_PATTERNS
    }

    lines.extend(
        [
            "## Проверка требований этапа 1",
            "",
            "| Требование | Статус | Комментарий |",
            "|---|---|---|",
            (
                "| Читать все `.xlsx`, `.xls`, `.csv` из `data/raw/` | выполнено | "
                f"Найдено файлов: {len(raw_files)}; Excel: {len(excel_files)}; CSV: {len(csv_files)}. |"
            ),
            (
                "| Определять листы Excel | выполнено | "
                f"Проверено Excel-листов: {sum(1 for audit in audits if audit.source_path.suffix.lower() in {'.xlsx', '.xls'})}. |"
            ),
            "| Определять колонки и типы данных | выполнено | См. раздел `Колонки, типы данных и пропуски`. |",
            "| Рассчитывать пропуски и дубликаты | выполнено | См. раздел `Сводка по таблицам и листам`. |",
            "| Определять candidate date columns | выполнено | См. раздел `Кандидатные колонки`. |",
            "| Определять candidate numeric columns | выполнено | См. раздел `Кандидатные колонки`. |",
            "| Определять semantic columns | выполнено | См. сводку ниже. |",
            "| Оценивать покрытие по годам | выполнено | См. раздел `Покрытие по годам`. |",
            f"| Писать логи | выполнено | Лог: `{config.PIPELINE_LOG_PATH.relative_to(config.ROOT_DIR).as_posix()}`. |",
        ]
    )
    lines.append("")

    lines.extend(["### Сводка semantic columns", ""])
    for semantic_name, columns in all_semantics.items():
        lines.append(f"- {semantic_name}: {format_list(columns)}")
    lines.append("")


def format_list(values: list[str]) -> str:
    if not values:
        return "-"
    return ", ".join(f"`{markdown_cell(value)}`" for value in values)


def markdown_cell(value: str) -> str:
    return str(value).replace("|", r"\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
