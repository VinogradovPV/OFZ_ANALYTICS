"""Реестр исходных файлов data/raw без изменения исходных данных."""

from __future__ import annotations

import hashlib
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


RAW_DATA_REGISTRY_CSV = config.PROCESSED_DATA_DIR / "raw_data_registry.csv"
RAW_DATA_REGISTRY_REPORT = config.get_doc_path("raw_data_registry_report.md")
REGISTRY_EXTENSIONS = {".xlsx", ".xls", ".xlsm", ".csv"}


@dataclass(frozen=True)
class RawFileRecord:
    """Метаданные одного исходного файла."""

    filename: str
    path: str
    size: int
    modified_time: str
    sha256: str
    source_note: str
    registry_timestamp: str


def main(argv: Sequence[str] | None = None) -> int:
    """Сформировать реестр исходных файлов и отчет."""
    _ = argv
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт формирования реестра исходных файлов data/raw")

    config.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.DOCS_DIR.mkdir(parents=True, exist_ok=True)

    records = build_registry()
    registry = pd.DataFrame([record.__dict__ for record in records])
    registry.to_csv(RAW_DATA_REGISTRY_CSV, index=False, encoding="utf-8-sig")
    utils.write_markdown(RAW_DATA_REGISTRY_REPORT, build_report(registry))

    logger.info("Реестр исходных файлов сохранен: %s", RAW_DATA_REGISTRY_CSV)
    logger.info("Отчет реестра исходных файлов сохранен: %s", RAW_DATA_REGISTRY_REPORT)
    logger.info("Формирование реестра исходных файлов завершено; data/raw не изменялся")
    return 0


def build_registry() -> list[RawFileRecord]:
    """Прочитать метаданные raw-файлов без изменения `data/raw/`."""
    registry_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    records: list[RawFileRecord] = []
    for path in raw_files():
        stat = path.stat()
        records.append(
            RawFileRecord(
                filename=path.name,
                path=relative_project_path(path),
                size=int(stat.st_size),
                modified_time=datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                sha256=sha256_file(path),
                source_note=source_note_for_file(path),
                registry_timestamp=registry_timestamp,
            )
        )
    return records


def raw_files() -> list[Path]:
    """Вернуть поддерживаемые raw-файлы в стабильном порядке."""
    if not config.RAW_DATA_DIR.exists():
        return []
    return sorted(
        path
        for path in config.RAW_DATA_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in REGISTRY_EXTENSIONS
    )


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Посчитать SHA-256 файла потоково, не загружая файл целиком в память."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_note_for_file(path: Path) -> str:
    """Сформировать краткое примечание об источнике файла."""
    if path.name.startswith("INTERNET_Auction_Results"):
        return "Исходный файл результатов размещений ОФЗ из data/raw; реестр фиксирует файл без изменения."
    return "Исходный файл из data/raw; происхождение требует ручного описания при необходимости."


def relative_project_path(path: Path) -> str:
    """Вернуть путь относительно корня проекта, если возможно."""
    try:
        return path.relative_to(config.PROJECT_ROOT).as_posix()
    except ValueError:
        return str(path)


def build_report(registry: pd.DataFrame) -> str:
    """Сформировать Markdown-отчет по реестру исходных файлов."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_size = int(registry["size"].sum()) if "size" in registry.columns and not registry.empty else 0
    lines = [
        "# Реестр исходных данных",
        "",
        f"Дата формирования: `{now}`.",
        "",
        "Скрипт выполняет только чтение `data/raw/` и запись артефактов в `data/processed/` и `docs/`. "
        "`data/raw/` не изменяется.",
        "",
        "## Выходные файлы",
        "",
        f"- `{relative_project_path(RAW_DATA_REGISTRY_CSV)}`",
        f"- `{relative_project_path(RAW_DATA_REGISTRY_REPORT)}`",
        "",
        "## Сводка",
        "",
        f"- Файлов в реестре: `{len(registry)}`",
        f"- Совокупный размер, байт: `{total_size}`",
        "",
        "## Файлы",
        "",
    ]
    if registry.empty:
        lines.append("Поддерживаемые raw-файлы не найдены.")
    else:
        preview = registry[
            [
                "filename",
                "path",
                "size",
                "modified_time",
                "sha256",
                "source_note",
                "registry_timestamp",
            ]
        ].copy()
        lines.append(markdown_table(preview))
    lines.extend(
        [
            "",
            "## Поля реестра",
            "",
            "- `filename` — имя файла.",
            "- `path` — путь относительно корня проекта.",
            "- `size` — размер файла в байтах.",
            "- `modified_time` — время последнего изменения файла по filesystem metadata.",
            "- `sha256` — контрольная сумма SHA-256.",
            "- `source_note` — краткое примечание об источнике.",
            "- `registry_timestamp` — время фиксации записи в реестре.",
        ]
    )
    return "\n".join(lines)


def markdown_table(df: pd.DataFrame) -> str:
    """Преобразовать DataFrame в Markdown-таблицу."""
    if df.empty:
        return ""
    columns = [str(column) for column in df.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for _, row in df.iterrows():
        values = [escape_markdown_cell(row[column]) for column in df.columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def escape_markdown_cell(value: object) -> str:
    """Экранировать значение ячейки Markdown-таблицы."""
    if pd.isna(value):
        return ""
    return str(value).replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
