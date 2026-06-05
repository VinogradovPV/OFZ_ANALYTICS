"""Сравнение основных и безопасно воспроизведенных outputs этапов 1-3."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Sequence

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, utils
else:
    from . import config, utils


TIMESTAMP_PATTERNS = [
    re.compile(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?"),
    re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"),
]


@dataclass(frozen=True)
class OutputPair:
    label: str
    main_path: Path
    repro_path: Path
    kind: str


OUTPUT_PAIRS = (
    OutputPair("Этап 1: отчет аудита данных", config.DATA_AUDIT_MAIN_DOC, config.DATA_AUDIT_REPRO_DOC, "markdown"),
    OutputPair(
        "Этап 2: очищенный dataset",
        config.OFZ_AUCTIONS_CLEAN_MAIN_CSV,
        config.OFZ_AUCTIONS_CLEAN_REPRO_CSV,
        "csv",
    ),
    OutputPair(
        "Этап 2: отчет очистки данных",
        config.DATA_CLEANING_REPORT_MAIN_DOC,
        config.DATA_CLEANING_REPORT_REPRO_DOC,
        "markdown",
    ),
    OutputPair(
        "Этап 3: dataset признаков",
        config.OFZ_AUCTIONS_FEATURES_MAIN_CSV,
        config.OFZ_AUCTIONS_FEATURES_REPRO_CSV,
        "csv",
    ),
    OutputPair(
        "Этап 3: отчет построения признаков",
        config.FEATURE_ENGINEERING_MAIN_DOC,
        config.FEATURE_ENGINEERING_REPRO_DOC,
        "markdown",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Сравнить outputs этапов 1-3 проекта ОФЗ.")
    parser.add_argument(
        "--output",
        default=str(config.REPRO_DIFF_STAGES_1_3_DOC),
        help="Путь к Markdown-отчету различий.",
    )
    args = parser.parse_args(argv)

    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт сравнения outputs этапов 1-3")

    report = build_diff_report(OUTPUT_PAIRS)
    output_path = Path(args.output)
    utils.write_markdown(output_path, report)
    logger.info("Diff report записан: %s", output_path)
    return 0


def build_diff_report(pairs: Sequence[OutputPair]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Отчет различий воспроизводимости этапов 1-3",
        "",
        f"Дата формирования: `{now}`.",
        "",
        "Отчет сравнивает основные outputs с outputs безопасного воспроизведения. "
        "Из CSV-сравнения исключаются заведомо изменчивые timestamp-поля.",
        "",
        "| Output | Тип | Основной существует | Repro существует | Статус | Детали |",
        "|---|---|---:|---:|---|---|",
    ]

    detailed_sections: list[str] = []
    for pair in pairs:
        status, details, detail_section = compare_pair(pair)
        lines.append(
            "| "
            f"{pair.label} | `{pair.kind}` | {pair.main_path.exists()} | "
            f"{pair.repro_path.exists()} | {status} | {details} |"
        )
        if detail_section:
            detailed_sections.append(detail_section)

    if detailed_sections:
        lines.extend(["", "## Детали", ""])
        lines.extend(detailed_sections)

    lines.append("")
    return "\n".join(lines)


def compare_pair(pair: OutputPair) -> tuple[str, str, str]:
    if not pair.main_path.exists() and not pair.repro_path.exists():
        return "missing", "Оба файла отсутствуют.", ""
    if not pair.main_path.exists():
        return "missing_main", f"Основной файл отсутствует: `{rel(pair.main_path)}`.", ""
    if not pair.repro_path.exists():
        return "missing_repro", f"Repro-файл отсутствует: `{rel(pair.repro_path)}`.", ""

    if pair.kind == "csv":
        return compare_csv_pair(pair)
    return compare_text_pair(pair)


def compare_csv_pair(pair: OutputPair) -> tuple[str, str, str]:
    try:
        main_df = pd.read_csv(pair.main_path)
        repro_df = pd.read_csv(pair.repro_path)
    except Exception as exc:  # noqa: BLE001 - ошибка сравнения должна попасть в отчет.
        return "error", f"{type(exc).__name__}: {exc}", ""

    normalized_main = normalize_for_compare(main_df)
    normalized_repro = normalize_for_compare(repro_df)
    comparison = utils.compare_dataframes(normalized_main, normalized_repro)

    status = "match" if comparison["same_shape"] and comparison["same_columns"] and comparison["same_values"] else "diff"
    details = (
        f"main_shape={comparison['old_shape']}; repro_shape={comparison['new_shape']}; "
        f"same_columns={comparison['same_columns']}; changed_cells={comparison['changed_cells']}; "
        f"rows_only_in_main={comparison['rows_only_in_old']}; rows_only_in_repro={comparison['rows_only_in_new']}"
    )
    detail_section = make_detail_section(pair, comparison)
    return status, details, detail_section


def compare_text_pair(pair: OutputPair) -> tuple[str, str, str]:
    main_text = normalize_text(pair.main_path.read_text(encoding="utf-8"))
    repro_text = normalize_text(pair.repro_path.read_text(encoding="utf-8"))
    if main_text == repro_text:
        return "match", "Нормализованный текст совпадает.", ""

    main_lines = main_text.splitlines()
    repro_lines = repro_text.splitlines()
    details = f"main_lines={len(main_lines)}; repro_lines={len(repro_lines)}"
    section = [
        f"### {pair.label}",
        "",
        f"- Основной файл: `{rel(pair.main_path)}`",
        f"- Repro-файл: `{rel(pair.repro_path)}`",
        f"- {details}",
        "",
    ]
    return "diff", details, "\n".join(section)


def normalize_for_compare(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    volatile_columns = [
        column
        for column in result.columns
        if "timestamp" in str(column).lower() or str(column).lower().endswith("_at")
    ]
    if volatile_columns:
        result = result.drop(columns=volatile_columns)
    return result


def normalize_text(text: str) -> str:
    normalized = text
    for pattern in TIMESTAMP_PATTERNS:
        normalized = pattern.sub("<timestamp>", normalized)
    return normalized.strip()


def make_detail_section(pair: OutputPair, comparison: dict[str, object]) -> str:
    if comparison["same_shape"] and comparison["same_columns"] and comparison["same_values"]:
        return ""
    lines = [
        f"### {pair.label}",
        "",
        f"- Основной файл: `{rel(pair.main_path)}`",
        f"- Repro-файл: `{rel(pair.repro_path)}`",
        f"- Old shape: `{comparison['old_shape']}`",
        f"- New shape: `{comparison['new_shape']}`",
        f"- Same columns: `{comparison['same_columns']}`",
        f"- Same values: `{comparison['same_values']}`",
        f"- Changed cells: `{comparison['changed_cells']}`",
        f"- Columns added: `{comparison['columns_added']}`",
        f"- Columns removed: `{comparison['columns_removed']}`",
        "",
    ]
    return "\n".join(lines)


def rel(path: Path) -> str:
    try:
        return path.relative_to(config.ROOT_DIR).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
