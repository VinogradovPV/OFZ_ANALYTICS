"""Построение параметризованного report scope на основе признаков ОФЗ."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Sequence

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, report_params, utils
else:
    from . import config, report_params, utils


@dataclass(frozen=True)
class PeriodSelectionSummary:
    label: str
    display_label: str
    file_label: str
    start_date: pd.Timestamp
    end_date: pd.Timestamp
    aggregation_mode: str
    report_period_order: int
    rows: int
    is_target_period: bool


def main(argv: Sequence[str] | None = None) -> int:
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт Этапа 4: параметризованный контур отчета")

    params = report_params.parse_report_args(argv)
    features = read_features()
    date_column = detect_auction_date_column(features)
    logger.info("Основная дата аукциона: %s", date_column)

    scoped, summaries = build_report_scope(features, params, date_column)
    config.DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    scoped.to_csv(config.OFZ_AUCTIONS_REPORT_SCOPE_CSV, index=False, encoding="utf-8")

    report = build_period_selection_report(params, date_column, features, scoped, summaries)
    utils.write_markdown(config.PERIOD_SELECTION_REPORT_PATH, report)

    logger.info("Report scope dataset записан: %s", config.OFZ_AUCTIONS_REPORT_SCOPE_CSV)
    logger.info("Отчет выбора периодов записан: %s", config.PERIOD_SELECTION_REPORT_PATH)
    logger.info("Этап 4 завершен")
    return 0


def read_features() -> pd.DataFrame:
    if not config.OFZ_AUCTIONS_FEATURES_CSV.exists():
        raise FileNotFoundError(f"Features dataset не найден: {config.OFZ_AUCTIONS_FEATURES_CSV}")
    return pd.read_csv(config.OFZ_AUCTIONS_FEATURES_CSV)


def detect_auction_date_column(df: pd.DataFrame) -> str:
    candidates = ["auction_date", "date", "Дата", "Дата аукциона"]
    for column in candidates:
        if column in df.columns:
            parsed = pd.to_datetime(df[column], errors="coerce")
            if parsed.notna().any():
                return column
    raise ValueError("Не удалось надежно определить колонку даты аукциона.")


def build_report_scope(
    features: pd.DataFrame,
    params: report_params.ReportParams,
    date_column: str,
) -> tuple[pd.DataFrame, list[PeriodSelectionSummary]]:
    df = features.copy()
    df["_auction_date_for_filter"] = pd.to_datetime(df[date_column], errors="coerce")

    scoped_parts: list[pd.DataFrame] = []
    summaries: list[PeriodSelectionSummary] = []

    for period in params.periods:
        start_date = pd.Timestamp(period["period_start"])
        end_date = pd.Timestamp(period["period_end"])
        mask = df["_auction_date_for_filter"].between(start_date, end_date, inclusive="both")
        period_df = df.loc[mask].copy()

        period_df["aggregation_mode"] = str(period["aggregation_mode"])
        period_df["report_period_start"] = start_date.date().isoformat()
        period_df["report_period_end"] = end_date.date().isoformat()
        period_df["report_period_label"] = str(period["report_period_label"])
        period_df["report_period_display_label"] = str(period["report_period_display_label"])
        period_df["report_period_file_label"] = str(period["report_period_file_label"])
        period_df["report_period_order"] = int(period["report_period_order"])
        period_df["report_year"] = int(period["report_year"])
        period_df["report_period_type"] = str(period["period_type"])
        period_df["is_target_period"] = bool(period["is_target_period"])

        summaries.append(
            PeriodSelectionSummary(
                label=str(period["report_period_label"]),
                display_label=str(period["report_period_display_label"]),
                file_label=str(period["report_period_file_label"]),
                start_date=start_date,
                end_date=end_date,
                aggregation_mode=str(period["aggregation_mode"]),
                report_period_order=int(period["report_period_order"]),
                rows=int(len(period_df)),
                is_target_period=bool(period["is_target_period"]),
            )
        )
        if not period_df.empty:
            scoped_parts.append(period_df)

    if scoped_parts:
        scoped = pd.concat(scoped_parts, ignore_index=True)
    else:
        scoped = make_empty_scope(features, params)

    if "_auction_date_for_filter" in scoped.columns:
        scoped = scoped.drop(columns=["_auction_date_for_filter"])
    return scoped, summaries


def make_empty_scope(
    features: pd.DataFrame,
    params: report_params.ReportParams,
) -> pd.DataFrame:
    columns = list(features.columns)
    for column in [
        "aggregation_mode",
        "report_period_start",
        "report_period_end",
        "report_period_label",
        "report_period_display_label",
        "report_period_file_label",
        "report_period_order",
        "report_year",
        "report_period_type",
        "is_target_period",
    ]:
        if column not in columns:
            columns.append(column)
    empty = pd.DataFrame(columns=columns)
    if params.periods:
        first_period = params.periods[-1]
        empty.attrs["target_period_label"] = first_period["report_period_label"]
    return empty


def build_period_selection_report(
    params: report_params.ReportParams,
    date_column: str,
    features: pd.DataFrame,
    scoped: pd.DataFrame,
    summaries: list[PeriodSelectionSummary],
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Отчет выбора периодов",
        "",
        f"Дата формирования: `{now}`.",
        "",
        "## Параметры отчета",
        "",
        f"- `report_date`: `{params.report_date.isoformat()}`",
        f"- `retrospective_years`: `{params.retrospective_years}`",
        f"- `period_type`: `{params.period_type}`",
        f"- `aggregation_mode`: `{params.aggregation_mode}`",
        f"- Количество периодов: `{len(params.periods)}`",
        "",
        "## Методология",
        "",
        "- Фильтрация выполняется по включительному интервалу: `auction_date >= report_period_start` и `auction_date <= report_period_end`.",
        "- `cumulative` строит накопленный период с начала года до конца завершенного месяца или квартала.",
        "- `point` сохраняет старое поведение: только конкретный завершенный месяц или квартал.",
        "",
        "## Источник",
        "",
        f"- Dataset: `{config.OFZ_AUCTIONS_FEATURES_CSV.relative_to(config.ROOT_DIR).as_posix()}`",
        f"- Строк в источнике: `{len(features)}`",
        f"- Основная дата аукциона: `{date_column}`",
        "",
        "## Выбранные периоды",
        "",
        "| Порядок | Период | Отображение | File label | Начало | Конец | Агрегация | Целевой | Строк | Статус |",
        "|---:|---|---|---|---|---|---|---:|---:|---|",
    ]
    for summary in summaries:
        status = "empty" if summary.rows == 0 else "ok"
        lines.append(
            "| "
            f"{summary.report_period_order} | `{summary.label}` | `{summary.display_label}` | "
            f"`{summary.file_label}` | `{summary.start_date.date().isoformat()}` | "
            f"`{summary.end_date.date().isoformat()}` | `{summary.aggregation_mode}` | "
            f"{summary.is_target_period} | {summary.rows} | {status} |"
        )

    empty_periods = [summary for summary in summaries if summary.rows == 0]
    lines.extend(
        [
            "",
            "## Результат фильтрации",
            "",
            f"- Строк в report scope: `{len(scoped)}`",
            f"- Пустых периодов: `{len(empty_periods)}`",
            f"- Output: `{config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.relative_to(config.ROOT_DIR).as_posix()}`",
            "",
        ]
    )

    if empty_periods:
        lines.extend(["## Пустые периоды", ""])
        for summary in empty_periods:
            lines.append(
                f"- `{summary.label}` (`{summary.start_date.date().isoformat()}` - "
                f"`{summary.end_date.date().isoformat()}`): нет строк в features dataset."
            )
        lines.append("")

    lines.extend(
        [
            "## Добавленные колонки",
            "",
            "- `aggregation_mode`",
            "- `report_period_start`",
            "- `report_period_end`",
            "- `report_period_label`",
            "- `report_period_display_label`",
            "- `report_period_file_label`",
            "- `report_period_order`",
            "- `report_year`",
            "- `report_period_type`",
            "- `is_target_period`",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
