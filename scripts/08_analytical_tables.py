"""Этап 8.1: обязательные аналитические табличные отчеты."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, report_params, utils
else:
    from . import config, report_params, utils


@dataclass(frozen=True)
class TableResult:
    name: str
    dataframe: pd.DataFrame
    csv_path: Path
    xlsx_path: Path


def main(argv: Sequence[str] | None = None) -> int:
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт Этапа 8.1: аналитические таблицы")

    params = report_params.parse_report_args(argv)
    scope = read_report_scope()
    scope = filter_scope_by_params(scope, params)

    limitations: list[str] = []
    prepared = prepare_columns(scope, limitations)
    append_context_limitations(prepared, params, limitations)
    table_results = build_tables(prepared, params, limitations)

    reports_dir = report_tables_dir(params)
    reports_dir.mkdir(parents=True, exist_ok=True)
    config.EXPORTS_ANALYTICAL_CSV_DIR.mkdir(parents=True, exist_ok=True)
    for result in table_results:
        result.dataframe.to_csv(result.csv_path, index=False, encoding="utf-8")
        saved_xlsx_path = write_xlsx_with_fallback(result, limitations)
        logger.info("Таблица сохранена: %s; %s", result.csv_path, saved_xlsx_path)

    report = build_report(params, table_results, limitations)
    utils.write_markdown(config.ANALYTICAL_TABLES_REPORT_DOC, report)
    utils.write_markdown(
        config.ANALYTICAL_TABLES_LIMITATIONS_DOC,
        build_limitations_report(params, limitations),
    )
    logger.info("Отчет аналитических таблиц записан: %s", config.ANALYTICAL_TABLES_REPORT_DOC)
    logger.info("Ограничения аналитических таблиц записаны: %s", config.ANALYTICAL_TABLES_LIMITATIONS_DOC)
    logger.info("Этап 8.1 завершен")
    return 0


def read_report_scope() -> pd.DataFrame:
    if not config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.exists():
        raise FileNotFoundError(
            f"Report scope dataset не найден: {config.OFZ_AUCTIONS_REPORT_SCOPE_CSV}. "
            "Сначала выполните Этап 4."
        )
    return pd.read_csv(config.OFZ_AUCTIONS_REPORT_SCOPE_CSV)


def filter_scope_by_params(
    scope: pd.DataFrame,
    params: report_params.ReportParams,
) -> pd.DataFrame:
    required = {"report_period_label", "report_period_type", "aggregation_mode"}
    missing = required.difference(scope.columns)
    if missing:
        raise ValueError(f"В report scope отсутствуют колонки: {', '.join(sorted(missing))}.")

    labels = {str(period["label"]) for period in params.periods}
    mask = (
        scope["report_period_label"].astype("string").isin(labels)
        & (scope["report_period_type"].astype("string") == params.period_type)
        & (scope["aggregation_mode"].astype("string") == params.aggregation_mode)
    )
    return scope.loc[mask].copy()


def prepare_columns(scope: pd.DataFrame, limitations: list[str]) -> pd.DataFrame:
    df = scope.copy()
    required_base = [
        "report_period_label",
        "report_year",
        "report_period_type",
        "aggregation_mode",
        "report_period_start",
        "report_period_end",
        "ofz_type",
        "maturity_bucket",
    ]
    missing_base = [column for column in required_base if column not in df.columns]
    if missing_base:
        raise ValueError(f"Не хватает обязательных колонок report scope: {', '.join(missing_base)}.")

    df["_yield"] = resolve_numeric(df, ["yield", "weighted_avg_yield", "weighted_avg_yield_pct"], "доходность", limitations)
    df["_placement"] = resolve_numeric(df, ["placement_volume", "placement_amount_mln_rub"], "объем размещения", limitations)
    df["_demand"] = resolve_numeric(df, ["demand_volume", "demand_amount_mln_rub"], "спрос", limitations)
    df["_supply"] = resolve_numeric(df, ["supply_volume", "offer_amount_mln_rub"], "предложение", limitations)
    df["_days_to_maturity"] = resolve_numeric(df, ["days_to_maturity"], "срок до погашения в днях", limitations)
    df = add_period_order_columns(df)

    if "maturity_bucket_label" not in df.columns:
        limitations.append("Колонка `maturity_bucket_label` отсутствовала и была восстановлена по `maturity_bucket`.")
        df["maturity_bucket_label"] = df["maturity_bucket"].map(maturity_label_map()).astype("string")

    if "_days_to_maturity" in df.columns and df["_days_to_maturity"].notna().any():
        recalculated_bucket = classify_maturity_bucket_from_days(df["_days_to_maturity"])
        df["maturity_bucket"] = recalculated_bucket
        df["maturity_bucket_label"] = df["maturity_bucket"].map(maturity_label_map()).astype("string")
        limitations.append("Таблица сроков обращения классифицирует сроки по `days_to_maturity`.")
    elif {"auction_date", "maturity_date"}.issubset(df.columns):
        recalculated_bucket = classify_maturity_bucket_from_dates(df["auction_date"], df["maturity_date"])
        df["maturity_bucket"] = recalculated_bucket
        df["maturity_bucket_label"] = df["maturity_bucket"].map(maturity_label_map()).astype("string")
        limitations.append("`days_to_maturity` недоступен; таблица сроков использует календарный расчет по датам.")
    elif "maturity_years" in df.columns:
        years = pd.to_numeric(df["maturity_years"], errors="coerce")
        recalculated_bucket = classify_maturity_bucket_from_years(years)
        if recalculated_bucket.notna().any():
            df["maturity_bucket"] = recalculated_bucket
            df["maturity_bucket_label"] = df["maturity_bucket"].map(maturity_label_map()).astype("string")
    else:
        limitations.append("Колонка `maturity_years` отсутствует; используется существующий `maturity_bucket` без пересчета.")

    df["maturity_bucket_order"] = df["maturity_bucket"].map(maturity_order_map()).fillna(99).astype("Int64")
    return df


def add_period_order_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Добавить служебный порядок периода, если report scope его не содержит."""
    result = df.copy()
    if "report_period_order" in result.columns:
        result["report_period_order"] = pd.to_numeric(result["report_period_order"], errors="coerce").astype("Int64")
        return result

    if "report_period_start" in result.columns:
        period_starts = pd.to_datetime(result["report_period_start"], errors="coerce")
        ordered = sorted(pd.Timestamp(value) for value in period_starts.dropna().unique())
        order_lookup = {value: index + 1 for index, value in enumerate(ordered)}
        result["report_period_order"] = period_starts.map(
            lambda value: order_lookup.get(pd.Timestamp(value), pd.NA) if pd.notna(value) else pd.NA
        ).astype("Int64")
        return result

    period_keys = (
        result[["report_year", "report_period_label"]]
        .drop_duplicates()
        .sort_values(["report_year", "report_period_label"])
        .reset_index(drop=True)
    )
    period_keys["report_period_order"] = period_keys.index + 1
    result = result.merge(period_keys, on=["report_year", "report_period_label"], how="left")
    result["report_period_order"] = pd.to_numeric(result["report_period_order"], errors="coerce").astype("Int64")
    return result


def append_context_limitations(
    scope: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> None:
    if "format" in scope.columns:
        drpa_rows = int(scope["format"].astype("string").str.contains("ДРПА", case=False, na=False).sum())
        if drpa_rows:
            limitations.append(
                f"В report scope есть строки ДРПА: {drpa_rows}; при наличии `demand_volume` они включаются в таблицу спроса и предложения."
            )
    if "failed_or_no_deal" in scope.columns:
        failed_rows = int(scope["failed_or_no_deal"].astype("string").str.lower().isin({"true", "1", "yes"}).sum())
        if failed_rows:
            limitations.append(
                f"В report scope есть несостоявшиеся или нулевые размещения: {failed_rows}; ratio с размещением может быть пустым."
            )

    if params.period_type == "quarter" and params.report_date.month == 7:
        target_period = next((period for period in params.periods if period.get("is_target_period")), None)
        if target_period is not None and params.report_date <= datetime.now().date():
            limitations.append(
                "Целевой период соответствует II кварталу; если исходные данные обновлены не на конец квартала, "
                "сравнение может отражать неполный II квартал."
            )


def resolve_numeric(
    df: pd.DataFrame,
    candidates: list[str],
    metric_name: str,
    limitations: list[str],
) -> pd.Series:
    for column in candidates:
        if column in df.columns:
            return pd.to_numeric(df[column], errors="coerce")
    limitations.append(f"Не удалось надежно определить поле `{metric_name}`; связанные KPI будут пустыми.")
    return pd.Series(pd.NA, index=df.index, dtype="Float64")


def classify_maturity_bucket_from_years(maturity_years: pd.Series) -> pd.Series:
    result = pd.Series("requires_review", index=maturity_years.index, dtype="object")
    result.loc[maturity_years.notna() & (maturity_years <= 5)] = "short_term"
    result.loc[maturity_years.notna() & (maturity_years > 5) & (maturity_years <= 10)] = "medium_term"
    result.loc[maturity_years.notna() & (maturity_years > 10)] = "long_term"
    return result.astype("string")


def classify_maturity_bucket_from_days(days_to_maturity: pd.Series) -> pd.Series:
    years = pd.to_numeric(days_to_maturity, errors="coerce") / 365.25
    return classify_maturity_bucket_from_years(years)


def classify_maturity_bucket_from_dates(
    auction_date: pd.Series,
    maturity_date: pd.Series,
) -> pd.Series:
    years = calendar_maturity_years(auction_date, maturity_date)
    return classify_maturity_bucket_from_years(years)


def calendar_maturity_years(auction_date: pd.Series, maturity_date: pd.Series) -> pd.Series:
    auction = pd.to_datetime(auction_date, errors="coerce")
    maturity = pd.to_datetime(maturity_date, errors="coerce")
    result = pd.Series(pd.NA, index=auction.index, dtype="Float64")
    valid = auction.notna() & maturity.notna()
    full_years = maturity.dt.year - auction.dt.year
    before_anniversary = (
        (maturity.dt.month < auction.dt.month)
        | ((maturity.dt.month == auction.dt.month) & (maturity.dt.day < auction.dt.day))
    )
    full_years = full_years.where(~before_anniversary, full_years - 1)
    result.loc[valid] = full_years.loc[valid].astype("Float64")
    return result


def maturity_label_map() -> dict[str, str]:
    return {
        "short_term": "Краткосрочные (до 5 лет включительно)",
        "medium_term": "Среднесрочные (свыше 5 до 10 лет включительно)",
        "long_term": "Долгосрочные (более 10 лет)",
        "requires_review": "Требует проверки",
    }


def maturity_order_map() -> dict[str, int]:
    """Методологический порядок сроковых категорий внутри отчетного периода."""
    return {
        "short_term": 1,
        "medium_term": 2,
        "long_term": 3,
        "requires_review": 99,
    }


def build_tables(
    scope: pd.DataFrame,
    params: report_params.ReportParams,
    limitations: list[str],
) -> list[TableResult]:
    suffix = make_output_suffix(params)
    xlsx_dir = report_tables_dir(params)
    yield_table = build_yield_by_type_table(scope, limitations)
    demand_supply_table = build_demand_supply_table(scope, limitations)
    maturity_table = build_placement_by_maturity_table(scope)

    return [
        TableResult(
            "Таблица доходности по видам ОФЗ",
            yield_table,
            config.EXPORTS_ANALYTICAL_CSV_DIR / f"ofz_yield_by_type_{suffix}.csv",
            xlsx_dir / f"ofz_yield_by_type_{suffix}.xlsx",
        ),
        TableResult(
            "Таблица совокупного спроса и совокупного предложения",
            demand_supply_table,
            config.EXPORTS_ANALYTICAL_CSV_DIR / f"demand_supply_{suffix}.csv",
            xlsx_dir / f"demand_supply_{suffix}.xlsx",
        ),
        TableResult(
            "Таблица объемов размещения ОФЗ по срокам обращения",
            maturity_table,
            config.EXPORTS_ANALYTICAL_CSV_DIR / f"placement_volume_by_maturity_{suffix}.csv",
            xlsx_dir / f"placement_volume_by_maturity_{suffix}.xlsx",
        ),
    ]


def report_tables_dir(params: report_params.ReportParams) -> Path:
    """Вернуть папку для XLSX-версий отчетных таблиц."""
    if params.period_type == "month":
        return config.REPORTS_MONTHLY_TABLES_DIR
    return config.REPORTS_ANALYTICAL_TABLES_DIR


def write_xlsx_with_fallback(result: TableResult, limitations: list[str]) -> Path:
    try:
        result.dataframe.to_excel(result.xlsx_path, index=False)
        return result.xlsx_path
    except PermissionError:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fallback_path = result.xlsx_path.with_name(
            f"{result.xlsx_path.stem}_{timestamp}{result.xlsx_path.suffix}"
        )
        result.dataframe.to_excel(fallback_path, index=False)
        limitations.append(
            "Основной XLSX-файл был заблокирован и не перезаписан: "
            f"`{result.xlsx_path.relative_to(config.ROOT_DIR).as_posix()}`. "
            f"Сохранена альтернативная версия: `{fallback_path.relative_to(config.ROOT_DIR).as_posix()}`."
        )
        return fallback_path


def build_yield_by_type_table(scope: pd.DataFrame, limitations: list[str]) -> pd.DataFrame:
    source_rows = len(scope)
    scope = scope.loc[scope["_yield"].notna()].copy()
    excluded_rows = source_rows - len(scope)
    if excluded_rows:
        limitations.append(
            f"Таблица доходности исключила строки без доходности: {excluded_rows}."
        )
    rows: list[dict[str, Any]] = []
    output_columns = [
        "report_period_label",
        "report_year",
        "report_period_type",
        "aggregation_mode",
        "report_period_order",
        "report_period_start",
        "ofz_type",
        "placement_volume",
        "yield_min",
        "yield_weighted_avg",
        "yield_max",
        "yield_min_yoy_change",
        "yield_weighted_avg_yoy_change",
        "yield_max_yoy_change",
        "auction_count",
        "data_quality_flag",
    ]
    group_columns = ["report_period_label", "report_year", "report_period_type", "aggregation_mode", "ofz_type"]
    for keys, group in scope.groupby(group_columns, dropna=False):
        period_label, report_year, period_type, aggregation_mode, ofz_type = keys
        weighted_yield, flag = weighted_average_with_flag(group["_yield"], group["_placement"])
        placement_volume = group["_placement"].sum(min_count=1)
        if pd.isna(placement_volume):
            limitations.append(
                f"{period_label} / {ofz_type}: `placement_volume` отсутствует; объем размещения в таблице доходности пуст."
            )
        if flag != "ok":
            limitations.append(
                f"{period_label} / {ofz_type}: средневзвешенная доходность рассчитана с ограничением `{flag}`."
            )
        rows.append(
            {
                "report_period_label": period_label,
                "report_year": report_year,
                "report_period_type": period_type,
                "aggregation_mode": aggregation_mode,
                "report_period_order": first_group_value(group, "report_period_order"),
                "report_period_start": first_group_value(group, "report_period_start"),
                "ofz_type": ofz_type,
                "placement_volume": placement_volume,
                "yield_min": group["_yield"].min(skipna=True),
                "yield_weighted_avg": weighted_yield,
                "yield_max": group["_yield"].max(skipna=True),
                "auction_count": int(len(group)),
                "data_quality_flag": flag,
            }
        )
    if not rows:
        return pd.DataFrame(columns=output_columns)
    result = pd.DataFrame(rows)
    result = add_yoy_columns(
        result,
        key_columns=["ofz_type"],
        value_columns=["yield_min", "yield_weighted_avg", "yield_max"],
    )
    result = sort_table_by_period_then_category(result, ["ofz_type"])
    return result[output_columns]


def build_demand_supply_table(scope: pd.DataFrame, limitations: list[str]) -> pd.DataFrame:
    group_columns = [
        "report_period_label",
        "report_year",
        "report_period_type",
        "aggregation_mode",
        "report_period_start",
        "report_period_end",
    ]
    rows: list[dict[str, Any]] = []
    output_columns = [
        "report_period_label",
        "report_year",
        "report_period_type",
        "aggregation_mode",
        "report_period_start",
        "report_period_end",
        "total_demand",
        "total_supply",
        "total_demand_yoy_change",
        "total_supply_yoy_change",
        "bid_to_cover_ratio",
        "bid_to_cover_ratio_yoy_change",
        "demand_supply_ratio",
        "demand_supply_ratio_yoy_change",
        "auction_count",
        "data_quality_flag",
    ]
    for keys, group in scope.groupby(group_columns, dropna=False):
        period_label, report_year, period_type, aggregation_mode, period_start, period_end = keys
        total_demand = group["_demand"].sum(min_count=1)
        total_supply = group["_supply"].sum(min_count=1)
        bid_to_cover_ratio = safe_divide_scalar(total_demand, total_supply)
        rows.append(
            {
                "report_period_label": period_label,
                "report_year": report_year,
                "report_period_type": period_type,
                "aggregation_mode": aggregation_mode,
                "report_period_start": period_start,
                "report_period_end": period_end,
                "total_demand": total_demand,
                "total_supply": total_supply,
                "bid_to_cover_ratio": bid_to_cover_ratio,
                "demand_supply_ratio": bid_to_cover_ratio,
                "auction_count": int(len(group)),
                "data_quality_flag": demand_supply_flag(total_demand, total_supply),
            }
        )
    if not rows:
        return pd.DataFrame(columns=output_columns)
    result = pd.DataFrame(rows)
    result = add_yoy_columns(
        result,
        key_columns=[],
        value_columns=["total_demand", "total_supply", "bid_to_cover_ratio", "demand_supply_ratio"],
    )
    limitations.append(
        "Таблица спроса и предложения использует `demand_volume` из столбца "
        "`Совокупный объем спроса по номиналу` и `supply_volume` из столбца `Объем предложения`; "
        "суммируются и аукционы, и ДРПА при наличии значений."
    )
    limitations.append(
        "Таблица спроса и предложения группирует данные по `report_period_start` и `report_period_end`; "
        "для cumulative-режима суммируется весь накопленный интервал report scope."
    )
    return result[output_columns]


def build_placement_by_maturity_table(scope: pd.DataFrame) -> pd.DataFrame:
    group_columns = [
        "report_period_label",
        "report_year",
        "report_period_type",
        "aggregation_mode",
        "maturity_bucket",
        "maturity_bucket_label",
    ]
    rows: list[dict[str, Any]] = []
    output_columns = [
        "report_period_label",
        "report_year",
        "report_period_type",
        "aggregation_mode",
        "report_period_order",
        "report_period_start",
        "maturity_bucket",
        "maturity_bucket_order",
        "maturity_bucket_label",
        "placement_volume",
        "placement_volume_yoy_change",
        "placement_volume_share",
        "placement_volume_share_yoy_change",
        "auction_count",
        "data_quality_flag",
    ]
    for keys, group in scope.groupby(group_columns, dropna=False):
        period_label, report_year, period_type, aggregation_mode, bucket, bucket_label = keys
        placement_volume = group["_placement"].sum(min_count=1)
        rows.append(
            {
                "report_period_label": period_label,
                "report_year": report_year,
                "report_period_type": period_type,
                "aggregation_mode": aggregation_mode,
                "report_period_order": first_group_value(group, "report_period_order"),
                "report_period_start": first_group_value(group, "report_period_start"),
                "maturity_bucket": bucket,
                "maturity_bucket_order": first_group_value(group, "maturity_bucket_order"),
                "maturity_bucket_label": bucket_label,
                "placement_volume": placement_volume,
                "auction_count": int(len(group)),
                "data_quality_flag": "requires_review" if bucket == "requires_review" else "ok",
            }
        )
    if not rows:
        return pd.DataFrame(columns=output_columns)
    result = pd.DataFrame(rows)
    denominator = result.groupby(["report_period_label", "report_period_type", "aggregation_mode"], dropna=False)[
        "placement_volume"
    ].transform("sum")
    result["placement_volume_share"] = result["placement_volume"] / denominator.mask(denominator == 0)
    result = add_yoy_columns(
        result,
        key_columns=["maturity_bucket"],
        value_columns=["placement_volume", "placement_volume_share"],
    )
    result = sort_table_by_period_then_category(result, ["maturity_bucket_order", "maturity_bucket_label"])
    return result[output_columns]


def weighted_average_with_flag(values: pd.Series, weights: pd.Series) -> tuple[Any, str]:
    valid = values.notna() & weights.notna() & (weights > 0)
    if valid.any():
        return float((values[valid] * weights[valid]).sum() / weights[valid].sum()), "ok"
    if values.notna().any():
        return float(values.mean(skipna=True)), "simple_mean_used_no_placement_volume"
    return pd.NA, "requires_review_no_yield"


def demand_supply_flag(total_demand: Any, total_supply: Any) -> str:
    if pd.isna(total_demand) or pd.isna(total_supply):
        return "requires_review_missing_demand_or_supply"
    if total_supply == 0:
        return "requires_review_zero_supply"
    return "ok"


def safe_divide_scalar(numerator: Any, denominator: Any) -> Any:
    if pd.isna(numerator) or pd.isna(denominator) or denominator == 0:
        return pd.NA
    return float(numerator / denominator)


def first_group_value(group: pd.DataFrame, column: str) -> Any:
    """Вернуть первое непустое значение группы для служебных ключей сортировки."""
    if column not in group.columns:
        return pd.NA
    values = group[column].dropna()
    if values.empty:
        return pd.NA
    return values.iloc[0]


def period_sort_columns(table: pd.DataFrame) -> list[str]:
    """Вернуть надежные колонки сортировки периода от общего режима к дате периода."""
    columns: list[str] = []
    if "aggregation_mode" in table.columns:
        columns.append("aggregation_mode")
    if "report_period_start" in table.columns and table["report_period_start"].notna().any():
        columns.append("report_period_start")
    elif "report_period_order" in table.columns and table["report_period_order"].notna().any():
        columns.append("report_period_order")
    else:
        for column in ["report_year", "report_period_label"]:
            if column in table.columns:
                columns.append(column)
    for column in ["report_year", "report_period_label"]:
        if column in table.columns and column not in columns:
            columns.append(column)
    return columns


def sort_table_by_period_then_category(table: pd.DataFrame, category_columns: list[str]) -> pd.DataFrame:
    """Отсортировать пользовательский вывод: сначала период, затем аналитическая категория."""
    sort_columns = period_sort_columns(table) + [column for column in category_columns if column in table.columns]
    if not sort_columns:
        return table.reset_index(drop=True)
    return table.sort_values(sort_columns, kind="mergesort").reset_index(drop=True)


def add_yoy_columns(
    table: pd.DataFrame,
    key_columns: list[str],
    value_columns: list[str],
) -> pd.DataFrame:
    result = table.copy()
    sort_columns = key_columns + [column for column in period_sort_columns(result) if column not in key_columns]
    if "report_period_type" in result.columns and "report_period_type" not in sort_columns:
        sort_columns.insert(len(key_columns), "report_period_type")
    result = result.sort_values(sort_columns).reset_index(drop=True)
    group_columns = key_columns + ["report_period_type", "aggregation_mode"]
    for column in value_columns:
        yoy_column = f"{column}_yoy_change"
        if group_columns:
            result[yoy_column] = result[column] - result.groupby(group_columns, dropna=False)[column].shift(1)
        else:
            result[yoy_column] = result[column] - result.groupby(["report_period_type", "aggregation_mode"], dropna=False)[column].shift(1)
    return result


def make_output_suffix(params: report_params.ReportParams) -> str:
    return (
        f"{params.period_type}_{params.aggregation_mode}_{params.report_date.isoformat()}_"
        f"retrospective_{params.retrospective_years}"
    )


def build_report(
    params: report_params.ReportParams,
    results: list[TableResult],
    limitations: list[str],
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Аналитические табличные отчеты",
        "",
        f"Дата формирования: `{now}`.",
        "",
        "## Параметры",
        "",
        f"- `report_date`: `{params.report_date.isoformat()}`",
        f"- `retrospective_years`: `{params.retrospective_years}`",
        f"- `period_type`: `{params.period_type}`",
        f"- `aggregation_mode`: `{params.aggregation_mode}`",
        "",
        "## Правила сортировки аналитических таблиц",
        "",
        "- `ofz_yield_by_type` сортируется прежде всего по отчетному периоду, затем по виду ОФЗ.",
        "- `placement_volume_by_maturity` сортируется прежде всего по отчетному периоду, затем по сроковой категории.",
        "- Если доступен `report_period_start`, он используется как основной надежный ключ периода; иначе используется `report_period_order`.",
        "- Внутри периода сроковые категории идут в порядке: краткосрочные -> среднесрочные -> долгосрочные -> requires_review.",
        "- Такая сортировка нужна, чтобы отчетный период и ретроспектива читались как последовательность сравнения, а не как блоки по категориям.",
        "",
    ]
    for result in results:
        lines.extend(
            [
                f"## {result.name}",
                "",
                f"- CSV: `{result.csv_path.relative_to(config.ROOT_DIR).as_posix()}`",
                f"- XLSX: `{result.xlsx_path.relative_to(config.ROOT_DIR).as_posix()}`",
                "",
            ]
        )
        if result.dataframe.empty:
            lines.append("Таблица пуста.")
        else:
            lines.append(markdown_table(result.dataframe))
        lines.append("")

    lines.extend(["## Ограничения", ""])
    if limitations:
        for item in sorted(set(limitations)):
            lines.append(f"- {item}")
    else:
        lines.append("- Критических ограничений не выявлено.")
    lines.append("")
    return "\n".join(lines)


def markdown_table(df: pd.DataFrame, max_rows: int = 80) -> str:
    shown = df.head(max_rows).copy()
    headers = [str(column) for column in shown.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for _, row in shown.iterrows():
        cells = [markdown_cell(row[column]) for column in shown.columns]
        lines.append("| " + " | ".join(cells) + " |")
    if len(df) > max_rows:
        lines.append(f"| ... | " + " | ".join("" for _ in headers[1:]) + " |")
    return "\n".join(lines)


def markdown_cell(value: Any) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value).replace("|", r"\|").replace("\n", " ")


def build_limitations_report(
    params: report_params.ReportParams,
    limitations: list[str],
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Ограничения аналитических табличных отчетов",
        "",
        f"Дата формирования: `{now}`.",
        "",
        f"Параметры: `{params.period_type}`, `{params.aggregation_mode}`, `{params.report_date.isoformat()}`, ретроспектива `{params.retrospective_years}`.",
        "",
        "## Методические ограничения",
        "",
        "- Таблица спроса и предложения использует спрос из `Совокупный объем спроса по номиналу` и предложение из `Объем предложения`.",
        "- В таблице спроса и предложения суммируются и аукционы, и ДРПА при наличии значений спроса и предложения.",
        "- Несостоявшиеся аукционы и строки с нулевым размещением сохраняются в данных, но ratio с размещением может быть пустым.",
        "- Для II квартала нужно проверять полноту периода: если источник обновлен до окончания квартала, сравнение отражает неполный II квартал.",
        "",
        "## Ограничения запуска",
        "",
    ]
    if limitations:
        for item in sorted(set(limitations)):
            lines.append(f"- {item}")
    else:
        lines.append("- Критических ограничений не выявлено.")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
