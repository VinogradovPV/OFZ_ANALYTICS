"""Этап 5: карта KPI для параметризуемой аналитики аукционов ОФЗ."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, utils
else:
    from . import config, utils


GROUP_COLUMNS = [
    "report_period_label",
    "report_year",
    "report_period_type",
    "format",
    "ofz_type",
    "maturity_bucket",
]

REQUIRED_SOURCE_COLUMNS = [
    "report_period_label",
    "report_year",
    "report_period_type",
    "format",
    "ofz_type",
    "maturity_bucket",
]

METRIC_CANDIDATES = {
    "yield": ["yield", "weighted_avg_yield", "weighted_avg_yield_pct"],
    "demand": ["demand_volume", "demand_amount_mln_rub"],
    "supply": ["supply_volume", "offer_amount_mln_rub"],
    "placement": ["placement_volume", "placement_amount_mln_rub"],
}


@dataclass(frozen=True)
class KpiDefinition:
    name: str
    formula: str
    source_fields: str
    applicability: str
    analytical_meaning: str
    management_use: str
    interpretation_limits: str
    table_relevance: str


KPI_DEFINITIONS = [
    KpiDefinition(
        name="Минимальная доходность",
        formula="min(yield)",
        source_fields="yield / weighted_avg_yield / weighted_avg_yield_pct",
        applicability="month, quarter, year",
        analytical_meaning="Нижняя граница стоимости заимствований в выбранном срезе.",
        management_use="Оценка наиболее благоприятных условий размещения.",
        interpretation_limits="Зависит от состава выпусков и наличия доходности в источнике.",
        table_relevance="Таблица доходности по видам ОФЗ.",
    ),
    KpiDefinition(
        name="Средневзвешенная доходность",
        formula="weighted average yield by placement_volume; fallback mean(yield)",
        source_fields="yield, placement_volume",
        applicability="month, quarter, year",
        analytical_meaning="Средняя стоимость размещения с учетом объема.",
        management_use="Мониторинг стоимости заимствований и сравнение с ретроспективой.",
        interpretation_limits="При отсутствии объема размещения используется простое среднее.",
        table_relevance="Таблица доходности по видам ОФЗ.",
    ),
    KpiDefinition(
        name="Максимальная доходность",
        formula="max(yield)",
        source_fields="yield / weighted_avg_yield / weighted_avg_yield_pct",
        applicability="month, quarter, year",
        analytical_meaning="Верхняя граница стоимости заимствований в выбранном срезе.",
        management_use="Идентификация стрессовых размещений.",
        interpretation_limits="Может отражать структуру выпусков, а не только рыночное давление.",
        table_relevance="Таблица доходности по видам ОФЗ.",
    ),
    KpiDefinition(
        name="Совокупный спрос",
        formula="sum(demand_volume)",
        source_fields="demand_volume / demand_amount_mln_rub",
        applicability="month, quarter, year",
        analytical_meaning="Объем заявленного спроса инвесторов.",
        management_use="Оценка глубины спроса на размещения Минфина.",
        interpretation_limits="Не все форматы могут иметь сопоставимые данные спроса.",
        table_relevance="Таблица совокупного спроса и совокупного предложения.",
    ),
    KpiDefinition(
        name="Совокупное предложение",
        formula="sum(supply_volume)",
        source_fields="supply_volume / offer_amount_mln_rub",
        applicability="month, quarter, year",
        analytical_meaning="Объем предложенного к размещению долга.",
        management_use="Оценка интенсивности первичного предложения.",
        interpretation_limits="Требует единообразной нормализации offer amount.",
        table_relevance="Таблица совокупного спроса и совокупного предложения.",
    ),
    KpiDefinition(
        name="Отношение спроса к предложению",
        formula="sum(demand_volume) / sum(supply_volume)",
        source_fields="demand_volume, supply_volume",
        applicability="month, quarter, year",
        analytical_meaning="Интегральный показатель покрытия предложения спросом.",
        management_use="Сигнал баланса спроса и предложения.",
        interpretation_limits="Не рассчитывается при нулевом или отсутствующем предложении.",
        table_relevance="Таблица совокупного спроса и совокупного предложения.",
    ),
    KpiDefinition(
        name="Объем размещения по срокам обращения",
        formula="sum(placement_volume) by maturity_bucket",
        source_fields="placement_volume, maturity_bucket",
        applicability="month, quarter, year",
        analytical_meaning="Структура фактического размещения по сроковым категориям.",
        management_use="Оценка смещения долговой политики по дюрации.",
        interpretation_limits="Зависит от надежности расчета maturity_bucket.",
        table_relevance="Таблица объемов размещения ОФЗ по срокам обращения.",
    ),
    KpiDefinition(
        name="Доля сроковой категории в общем объеме размещения",
        formula="sum(placement_volume by maturity_bucket) / sum(placement_volume by period)",
        source_fields="placement_volume, maturity_bucket, report_period_label",
        applicability="month, quarter, year",
        analytical_meaning="Доля кратко-, средне- и долгосрочных размещений в периоде.",
        management_use="Мониторинг изменения структуры заимствований.",
        interpretation_limits="Не рассчитывается при нулевом общем объеме размещения.",
        table_relevance="Таблица объемов размещения ОФЗ по срокам обращения.",
    ),
]


def main() -> int:
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт Этапа 5: KPI map")

    if not config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.exists():
        report = build_missing_source_report()
        utils.write_markdown(config.KPI_MAP_DOC, report)
        logger.warning("Report scope dataset отсутствует: %s", config.OFZ_AUCTIONS_REPORT_SCOPE_CSV)
        logger.info("KPI map записан с ограничениями: %s", config.KPI_MAP_DOC)
        return 0

    scope = pd.read_csv(config.OFZ_AUCTIONS_REPORT_SCOPE_CSV)
    report = build_kpi_map_report(scope)
    utils.write_markdown(config.KPI_MAP_DOC, report)
    logger.info("KPI map записан: %s", config.KPI_MAP_DOC)
    logger.info("Этап 5 завершен")
    return 0


def build_missing_source_report() -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = base_report_header(now)
    lines.extend(
        [
            "## Статус источника",
            "",
            f"Основной источник отсутствует: `{config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.relative_to(config.ROOT_DIR).as_posix()}`.",
            "",
            "KPI рассчитаны быть не могут. Перед расчетом KPI нужно выполнить Этап 4 `period_filter.py`.",
            "",
        ]
    )
    append_kpi_definitions(lines)
    append_required_grouping(lines)
    append_required_columns(lines)
    return "\n".join(lines)


def build_kpi_map_report(scope: pd.DataFrame) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = base_report_header(now)
    missing_required = [column for column in REQUIRED_SOURCE_COLUMNS if column not in scope.columns]
    metric_columns = resolve_metric_columns(scope)

    lines.extend(
        [
            "## Статус источника",
            "",
            f"- Источник: `{config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.relative_to(config.ROOT_DIR).as_posix()}`",
            f"- Строк: `{len(scope)}`",
            f"- Колонок: `{len(scope.columns)}`",
            f"- Отсутствующие обязательные срезы: `{', '.join(missing_required) if missing_required else '-'}`",
            "",
        ]
    )
    append_resolved_metrics(lines, metric_columns)
    append_kpi_definitions(lines)

    if missing_required:
        lines.extend(
            [
                "## Расчет KPI",
                "",
                "Расчет KPI не выполнен, потому что отсутствуют обязательные колонки группировки.",
                "",
            ]
        )
    else:
        append_calculated_kpis(lines, scope, metric_columns)

    append_required_grouping(lines)
    append_required_columns(lines)
    append_limitations(lines, scope, metric_columns, missing_required)
    return "\n".join(lines)


def base_report_header(now: str) -> list[str]:
    return [
        "# Карта KPI",
        "",
        f"Дата формирования: `{now}`.",
        "",
        "KPI map задает расчетные показатели для параметризуемой аналитики аукционов ОФЗ.",
        "",
    ]


def resolve_metric_columns(df: pd.DataFrame) -> dict[str, str | None]:
    resolved: dict[str, str | None] = {}
    for metric, candidates in METRIC_CANDIDATES.items():
        resolved[metric] = next((column for column in candidates if column in df.columns), None)
    return resolved


def append_resolved_metrics(lines: list[str], metric_columns: dict[str, str | None]) -> None:
    lines.extend(["## Нормализованные поля для KPI", "", "| Метрика | Используемая колонка |", "|---|---|"])
    for metric, column in metric_columns.items():
        lines.append(f"| `{metric}` | `{column or '-'}` |")
    lines.append("")


def append_kpi_definitions(lines: list[str]) -> None:
    lines.extend(
        [
            "## Определения KPI",
            "",
            "| KPI | Формула | Исходные поля | Применимость | Аналитический смысл | Управленческое применение | Ограничения | Табличный отчет |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for item in KPI_DEFINITIONS:
        lines.append(
            "| "
            f"{item.name} | `{item.formula}` | `{item.source_fields}` | {item.applicability} | "
            f"{item.analytical_meaning} | {item.management_use} | {item.interpretation_limits} | "
            f"{item.table_relevance} |"
        )
    lines.append("")


def append_calculated_kpis(
    lines: list[str],
    scope: pd.DataFrame,
    metric_columns: dict[str, str | None],
) -> None:
    working = scope.copy()
    for metric, column in metric_columns.items():
        if column:
            working[f"_{metric}"] = pd.to_numeric(working[column], errors="coerce")
        else:
            working[f"_{metric}"] = pd.NA

    grouped = (
        working.groupby(GROUP_COLUMNS, dropna=False)
        .apply(calculate_group_kpis)
        .reset_index()
    )
    grouped = add_maturity_share(grouped)

    lines.extend(
        [
            "## Расчетная сводка KPI",
            "",
            "Сводка рассчитана в разрезах `report_period_label`, `report_year`, `report_period_type`, `format`, `ofz_type`, `maturity_bucket`.",
            "",
            "| Период | Год | Тип периода | Формат | Тип ОФЗ | Срок | Мин. доходность | Ср. доходность | Макс. доходность | Спрос | Предложение | Спрос / предложение | Размещение | Доля срока | Наблюдений |",
            "|---|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for _, row in grouped.iterrows():
        lines.append(
            "| "
            f"`{row['report_period_label']}` | {row['report_year']} | `{row['report_period_type']}` | "
            f"`{row['format']}` | `{row['ofz_type']}` | `{row['maturity_bucket']}` | "
            f"{fmt(row['min_yield'])} | {fmt(row['weighted_avg_yield_kpi'])} | {fmt(row['max_yield'])} | "
            f"{fmt(row['total_demand'])} | {fmt(row['total_supply'])} | {fmt(row['demand_to_supply_ratio'])} | "
            f"{fmt(row['placement_volume_by_maturity'])} | {fmt(row['placement_volume_share'])} | {int(row['auction_count'])} |"
        )
    lines.append("")


def calculate_group_kpis(group: pd.DataFrame) -> pd.Series:
    total_demand = group["_demand"].sum(min_count=1)
    total_supply = group["_supply"].sum(min_count=1)
    total_placement = group["_placement"].sum(min_count=1)
    weighted_yield = weighted_average(group["_yield"], group["_placement"])
    return pd.Series(
        {
            "min_yield": group["_yield"].min(skipna=True),
            "weighted_avg_yield_kpi": weighted_yield,
            "max_yield": group["_yield"].max(skipna=True),
            "total_demand": total_demand,
            "total_supply": total_supply,
            "demand_to_supply_ratio": safe_scalar_divide(total_demand, total_supply),
            "placement_volume_by_maturity": total_placement,
            "auction_count": int(len(group)),
        }
    )


def add_maturity_share(grouped: pd.DataFrame) -> pd.DataFrame:
    result = grouped.copy()
    denominator = result.groupby(["report_period_label", "report_period_type"], dropna=False)[
        "placement_volume_by_maturity"
    ].transform("sum")
    denominator = denominator.mask(denominator == 0)
    result["placement_volume_share"] = result["placement_volume_by_maturity"] / denominator
    return result


def weighted_average(values: pd.Series, weights: pd.Series) -> Any:
    valid = values.notna() & weights.notna() & (weights > 0)
    if not valid.any():
        return values.mean(skipna=True)
    return float((values[valid] * weights[valid]).sum() / weights[valid].sum())


def safe_scalar_divide(numerator: Any, denominator: Any) -> Any:
    if pd.isna(numerator) or pd.isna(denominator) or denominator == 0:
        return pd.NA
    return float(numerator / denominator)


def append_required_grouping(lines: list[str]) -> None:
    lines.extend(["## Обязательные разрезы", ""])
    for column in GROUP_COLUMNS:
        lines.append(f"- `{column}`")
    lines.append("")


def append_required_columns(lines: list[str]) -> None:
    lines.extend(
        [
            "## Обязательные поля для табличных отчетов",
            "",
            "- `ofz_type`",
            "- `yield` или `weighted_avg_yield`",
            "- `demand_volume`",
            "- `supply_volume`",
            "- `placement_volume`",
            "- `maturity_years`",
            "- `maturity_bucket`",
            "- `maturity_bucket_label`",
            "",
        ]
    )


def append_limitations(
    lines: list[str],
    scope: pd.DataFrame,
    metric_columns: dict[str, str | None],
    missing_required: list[str],
) -> None:
    missing_metrics = [metric for metric, column in metric_columns.items() if column is None]
    lines.extend(["## Ограничения", ""])
    if scope.empty:
        lines.append("- Report scope dataset пуст; KPI не имеют наблюдений для расчета.")
    if missing_required:
        lines.append(f"- Отсутствуют обязательные разрезы: `{', '.join(missing_required)}`.")
    if missing_metrics:
        lines.append(f"- Не найдены нормализованные поля метрик: `{', '.join(missing_metrics)}`.")
    if not scope.empty and not missing_required and not missing_metrics:
        lines.append("- Критических ограничений для расчета обязательных KPI не выявлено.")
    lines.append("")


def fmt(value: Any) -> str:
    if pd.isna(value):
        return "-"
    try:
        return f"{float(value):,.4f}".replace(",", " ")
    except (TypeError, ValueError):
        return str(value)


if __name__ == "__main__":
    raise SystemExit(main())
