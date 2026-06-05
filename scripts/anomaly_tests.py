"""Диагностические anomaly tests второй модернизации OFZ_ANALITICS.

Скрипт читает `data/processed/ofz_auctions_report_scope.csv`, проверяет
методологические аномалии и записывает подробный отчет. `data/raw/` не меняется.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Sequence, cast

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, utils
else:
    from . import config, utils


ANOMALY_TESTS_REPORT_DOC = config.get_doc_path("anomaly_tests_report.md")


@dataclass(frozen=True)
class AnomalyResult:
    """Результат одной anomaly-проверки."""

    name: str
    status: str
    rows: int
    message: str
    sample: pd.DataFrame


AnomalyCheck = Callable[[pd.DataFrame], AnomalyResult]


def main() -> int:
    """Запустить anomaly tests и вернуть код завершения."""
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт anomaly tests второй модернизации")

    scope = read_report_scope()
    prepared = prepare_scope(scope)
    results = run_checks(prepared)

    utils.write_markdown(ANOMALY_TESTS_REPORT_DOC, build_report(results, prepared))
    for result in results:
        print(f"{result.status.upper()} | {result.name} | rows={result.rows} | {result.message}")

    failed = [result for result in results if result.status == "fail"]
    if failed:
        print(f"Anomaly tests failed: {len(failed)}")
        return 1
    print(f"Anomaly tests completed: {len(results)} checks")
    return 0


def read_report_scope() -> pd.DataFrame:
    """Прочитать report scope."""
    if not config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.exists():
        raise FileNotFoundError(
            f"Не найден {config.OFZ_AUCTIONS_REPORT_SCOPE_CSV}. Сначала выполните period_filter.py."
        )
    return pd.read_csv(config.OFZ_AUCTIONS_REPORT_SCOPE_CSV)


def prepare_scope(scope: pd.DataFrame) -> pd.DataFrame:
    """Подготовить стабильные служебные числовые поля."""
    df = scope.copy()
    numeric_map = {
        "_placement": ["placement_volume", "placement_amount_mln_rub"],
        "_demand": ["demand_volume", "demand_amount_mln_rub"],
        "_supply": ["supply_volume", "offer_amount_mln_rub"],
        "_yield": ["yield", "weighted_avg_yield", "weighted_avg_yield_pct"],
        "_cutoff_price": ["cutoff_price", "cutoff_price_pct"],
        "_discount_to_nominal": ["discount_to_nominal"],
        "_revenue": ["revenue_volume", "proceeds_mln_rub", "revenue_amount_mln_rub", "placement_revenue_mln_rub"],
        "_bid_to_cover": ["bid_to_cover_ratio"],
        "_demand_to_placement": ["demand_to_placement_ratio"],
    }
    for target, candidates in numeric_map.items():
        df[target] = first_numeric(df, candidates)
    if df["_bid_to_cover"].isna().all():
        df["_bid_to_cover"] = safe_divide(df["_demand"], df["_supply"])
    if df["_demand_to_placement"].isna().all():
        df["_demand_to_placement"] = safe_divide(df["_demand"], df["_placement"])
    if df["_discount_to_nominal"].isna().all() and df["_cutoff_price"].notna().any():
        df["_discount_to_nominal"] = 100 - df["_cutoff_price"]
    for column in ("format", "data_quality_flag", "failed_or_no_deal", "issue_code", "auction_date", "report_period_label", "source_file"):
        if column not in df.columns:
            df[column] = ""
    return df


def first_numeric(df: pd.DataFrame, candidates: Sequence[str]) -> pd.Series:
    """Вернуть первую доступную числовую колонку или пустую Series."""
    for column in candidates:
        if column in df.columns:
            return pd.to_numeric(df[column], errors="coerce")
    return pd.Series(pd.NA, index=df.index, dtype="Float64")


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Безопасное деление с NaN при нулевом знаменателе."""
    denominator_numeric = pd.to_numeric(denominator, errors="coerce")
    numerator_numeric = pd.to_numeric(numerator, errors="coerce")
    return numerator_numeric / denominator_numeric.mask(denominator_numeric == 0)


def run_checks(df: pd.DataFrame) -> list[AnomalyResult]:
    """Запустить все anomaly checks."""
    checks: list[AnomalyCheck] = [
        check_zero_placement,
        check_drpa_rows,
        check_failed_or_no_deal,
        check_missing_yield,
        check_zero_yield_suspected,
        check_bid_to_cover_outliers,
        check_demand_to_placement_outliers,
        check_zero_supply,
        check_zero_demand,
        check_demand_without_placement,
        check_placement_without_demand,
        check_missing_cutoff_price,
        check_missing_discount_to_nominal,
        check_nominal_revenue_gap_anomaly,
    ]
    results: list[AnomalyResult] = []
    for check in checks:
        try:
            results.append(check(df))
        except Exception as exc:  # pragma: no cover - отчет должен показать причину.
            results.append(AnomalyResult(check.__name__, "fail", 0, f"Неожиданная ошибка: {exc}", pd.DataFrame()))
    return results


def check_zero_placement(df: pd.DataFrame) -> AnomalyResult:
    rows = df.loc[df["_placement"].fillna(0) == 0]
    invalid_ratio = rows.loc[rows["_demand_to_placement"].notna()]
    if not invalid_ratio.empty:
        return result("zero_placement", "fail", invalid_ratio, "При нулевом размещении demand_to_placement_ratio должен быть пустым.")
    return result("zero_placement", "ok", rows, "Нулевое размещение найдено и не ломает demand_to_placement_ratio." if len(rows) else "Нулевое размещение не найдено.")


def check_drpa_rows(df: pd.DataFrame) -> AnomalyResult:
    rows = df.loc[df["format"].astype("string").str.contains("ДРПА", case=False, na=False)]
    demand_rows = rows.loc[rows["_demand"].notna() & (rows["_demand"] > 0)]
    status = "warning" if not demand_rows.empty else "ok"
    message = "ДРПА со спросом требуют ручной интерпретации." if status == "warning" else "ДРПА найдены; demand-based ratios должны учитывать ограничения." if len(rows) else "ДРПА не найдены."
    return result("drpa_rows", status, demand_rows if not demand_rows.empty else rows, message)


def check_failed_or_no_deal(df: pd.DataFrame) -> AnomalyResult:
    flag = df["failed_or_no_deal"].astype("string").str.lower().isin({"true", "1", "yes", "да"})
    rows = df.loc[flag | df["data_quality_flag"].astype("string").str.contains("failed|no_deal|несостоя", case=False, regex=True, na=False)]
    suspicious = rows.loc[rows["_placement"].fillna(0) > 0]
    if not suspicious.empty:
        return result("failed_or_no_deal", "warning", suspicious, "Есть несостоявшиеся/failed строки с положительным размещением.")
    return result("failed_or_no_deal", "ok", rows, "Несостоявшиеся аукционы не найдены или не имеют положительного размещения.")


def check_missing_yield(df: pd.DataFrame) -> AnomalyResult:
    rows = df.loc[df["_yield"].isna()]
    status = "warning" if not rows.empty else "ok"
    return result("missing_yield", status, rows, "Есть строки без доходности; они должны исключаться из yield-графиков." if status == "warning" else "Пропуски доходности не найдены.")


def check_zero_yield_suspected(df: pd.DataFrame) -> AnomalyResult:
    rows = df.loc[df["_yield"].notna() & (df["_yield"].abs() < 0.000001)]
    suspicious = rows.loc[
        rows["data_quality_flag"].astype("string").str.contains("missing|requires_review|invalid|zero", case=False, regex=True, na=False)
        | rows["format"].astype("string").str.len().ge(0)
    ]
    status = "warning" if not suspicious.empty else "ok"
    return result("zero_yield_suspected", status, suspicious, "Найдены около-нулевые доходности; проверить, не заменен ли пропуск на 0." if status == "warning" else "Около-нулевые доходности не найдены.")


def check_bid_to_cover_outliers(df: pd.DataFrame) -> AnomalyResult:
    rows = df.loc[df["_bid_to_cover"].notna() & (df["_bid_to_cover"] > 5)]
    status = "warning" if not rows.empty else "ok"
    return result("bid_to_cover_outliers", status, rows, "Найдены bid_to_cover_ratio > 5; проверить знаменатель supply_volume." if status == "warning" else "Выбросы bid_to_cover_ratio > 5 не найдены.")


def check_demand_to_placement_outliers(df: pd.DataFrame) -> AnomalyResult:
    rows = df.loc[df["_demand_to_placement"].notna() & (df["_demand_to_placement"] > 10)]
    status = "warning" if not rows.empty else "ok"
    return result("demand_to_placement_outliers", status, rows, "Найдены demand_to_placement_ratio > 10; проверить нулевые/малые placement_volume." if status == "warning" else "Выбросы demand_to_placement_ratio > 10 не найдены.")


def check_zero_supply(df: pd.DataFrame) -> AnomalyResult:
    rows = df.loc[df["_supply"].fillna(0) == 0]
    invalid_ratio = rows.loc[rows["_bid_to_cover"].notna()]
    if not invalid_ratio.empty:
        return result("zero_supply", "fail", invalid_ratio, "При нулевом предложении bid_to_cover_ratio должен быть пустым.")
    return result("zero_supply", "ok", rows, "Нулевое предложение найдено и не ломает bid_to_cover_ratio." if len(rows) else "Нулевое предложение не найдено.")


def check_zero_demand(df: pd.DataFrame) -> AnomalyResult:
    rows = df.loc[df["_demand"].fillna(0) == 0]
    status = "warning" if not rows.empty else "ok"
    return result("zero_demand", status, rows, "Есть строки с нулевым/отсутствующим спросом; demand ratios должны быть пустыми или ограниченными." if status == "warning" else "Нулевой спрос не найден.")


def check_demand_without_placement(df: pd.DataFrame) -> AnomalyResult:
    rows = df.loc[(df["_demand"].fillna(0) > 0) & (df["_placement"].fillna(0) == 0)]
    invalid_ratio = rows.loc[rows["_demand_to_placement"].notna()]
    if not invalid_ratio.empty:
        return result("demand_without_placement", "fail", invalid_ratio, "Есть спрос без размещения, но demand_to_placement_ratio не пустой.")
    return result("demand_without_placement", "warning" if len(rows) else "ok", rows, "Есть спрос без размещения; вероятно несостоявшийся/ограниченный аукцион." if len(rows) else "Спрос без размещения не найден.")


def check_placement_without_demand(df: pd.DataFrame) -> AnomalyResult:
    rows = df.loc[(df["_placement"].fillna(0) > 0) & (df["_demand"].isna() | (df["_demand"] == 0))]
    status = "warning" if not rows.empty else "ok"
    return result("placement_without_demand", status, rows, "Есть размещение без спроса; обычно это ДРПА или ограничение источника." if status == "warning" else "Размещение без спроса не найдено.")


def check_missing_cutoff_price(df: pd.DataFrame) -> AnomalyResult:
    auction_rows = df.loc[df["format"].astype("string").str.contains("Аукцион", case=False, na=False)]
    rows = auction_rows.loc[auction_rows["_cutoff_price"].isna()]
    status = "warning" if not rows.empty else "ok"
    return result("missing_cutoff_price", status, rows, "У части аукционов отсутствует цена отсечения; discount analysis ограничен." if status == "warning" else "Цена отсечения заполнена для аукционов.")


def check_missing_discount_to_nominal(df: pd.DataFrame) -> AnomalyResult:
    rows = df.loc[df["_cutoff_price"].notna() & df["_discount_to_nominal"].isna()]
    status = "warning" if not rows.empty else "ok"
    return result("missing_discount_to_nominal", status, rows, "Есть цена отсечения, но нет discount_to_nominal." if status == "warning" else "Дисконт к номиналу доступен или рассчитывается из цены отсечения.")


def check_nominal_revenue_gap_anomaly(df: pd.DataFrame) -> AnomalyResult:
    available = df.loc[df["_placement"].notna() & df["_revenue"].notna() & (df["_placement"] > 0)]
    if available.empty:
        return result("nominal_revenue_gap_anomaly", "warning", available, "Выручка недоступна; revenue anomaly tests ограничены.")
    gap_ratio = (available["_placement"] - available["_revenue"]) / available["_placement"]
    rows = available.loc[gap_ratio.abs() > 0.25].copy()
    if not rows.empty:
        rows["nominal_revenue_gap_ratio"] = gap_ratio.loc[rows.index]
    status = "warning" if not rows.empty else "ok"
    return result("nominal_revenue_gap_anomaly", status, rows, "Найдена аномальная разница между номиналом и выручкой > 25%." if status == "warning" else "Аномальная разница номинал/выручка > 25% не найдена.")


def result(name: str, status: str, rows: pd.DataFrame, message: str) -> AnomalyResult:
    """Сформировать результат с компактным sample."""
    return AnomalyResult(name, status, int(len(rows)), message, sample_rows(rows))


def sample_rows(rows: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    """Оставить диагностические колонки sample."""
    if rows.empty:
        return pd.DataFrame()
    columns = [
        "auction_date",
        "report_period_label",
        "issue_code",
        "format",
        "_demand",
        "_supply",
        "_placement",
        "_revenue",
        "_yield",
        "_bid_to_cover",
        "_demand_to_placement",
        "_cutoff_price",
        "_discount_to_nominal",
        "source_file",
        "data_quality_flag",
    ]
    existing = [column for column in columns if column in rows.columns]
    return rows.loc[:, existing].head(limit).copy()


def build_report(results: Sequence[AnomalyResult], df: pd.DataFrame) -> str:
    """Сформировать Markdown-отчет anomaly tests."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    counts = {
        "ok": sum(item.status == "ok" for item in results),
        "warning": sum(item.status == "warning" for item in results),
        "fail": sum(item.status == "fail" for item in results),
    }
    lines = [
        "# Anomaly tests report",
        "",
        "Метка: `вторая модернизация`.",
        "",
        f"Дата формирования: `{now}`.",
        "",
        "## Источник",
        "",
        f"- Dataset: `{config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.relative_to(config.PROJECT_ROOT).as_posix()}`",
        f"- Строк: `{len(df)}`",
        "",
        "## Сводка",
        "",
        f"- OK: `{counts['ok']}`",
        f"- Warnings: `{counts['warning']}`",
        f"- Failures: `{counts['fail']}`",
        "",
        "## Проверки",
        "",
        "| Проверка | Статус | Строк | Комментарий |",
        "| --- | --- | ---: | --- |",
    ]
    for item in results:
        lines.append(f"| `{item.name}` | `{item.status}` | {item.rows} | {item.message} |")

    lines.extend(["", "## Диагностические выборки", ""])
    for item in results:
        if item.sample.empty:
            continue
        lines.extend(
            [
                f"### `{item.name}`",
                "",
                dataframe_to_markdown(item.sample),
                "",
            ]
        )

    lines.extend(
        [
            "## Интерпретация",
            "",
            "- `ok` означает, что критичного нарушения по проверке не выявлено.",
            "- `warning` означает наличие наблюдений, требующих методологической или ручной проверки.",
            "- `fail` означает нарушение расчетного контракта, которое может искажать downstream-таблицы или графики.",
            "",
            "## Ограничения",
            "",
            "- Проверка не изменяет `data/raw/` и processed datasets.",
            "- Revenue checks ограничены, если в данных нет надежной колонки выручки.",
            "- Наличие warning не всегда означает ошибку данных; часть предупреждений фиксирует ожидаемые ограничения источника.",
        ]
    )
    return "\n".join(lines)


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Сформировать Markdown-таблицу без зависимости от `tabulate`."""
    if df.empty:
        return "_Нет строк для отображения._"
    columns = [str(column) for column in df.columns]
    lines = [
        "| " + " | ".join(escape_markdown_cell(column) for column in columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for _, row in df.iterrows():
        values = [format_cell(row[column]) for column in df.columns]
        lines.append("| " + " | ".join(escape_markdown_cell(value) for value in values) + " |")
    return "\n".join(lines)


def format_cell(value: object) -> str:
    """Отформатировать значение для Markdown-таблицы."""
    if is_missing_cell(value):
        return ""
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def is_missing_cell(value: object) -> bool:
    """Return True for scalar missing values used in Markdown cells."""
    try:
        missing = pd.isna(cast(Any, value))
    except (TypeError, ValueError):
        return False
    try:
        return bool(missing)
    except ValueError:
        return False


def escape_markdown_cell(value: object) -> str:
    """Экранировать значение ячейки Markdown-таблицы."""
    return str(value).replace("|", "\\|").replace("\n", "<br>")


if __name__ == "__main__":
    raise SystemExit(main())
