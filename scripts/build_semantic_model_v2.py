"""Построить dashboard semantic model v2 для второй модернизации."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, utils
else:
    from . import config, utils


SEMANTIC_VERSION = "2.0.0"
SEMANTIC_MODEL_V2_DIR = config.DASHBOARDS_SEMANTIC_MODEL_V2_DIR
FIELD_DICTIONARY_PATH = SEMANTIC_MODEL_V2_DIR / "field_dictionary.csv"
KPI_DICTIONARY_PATH = SEMANTIC_MODEL_V2_DIR / "kpi_dictionary.csv"
MEASURES_PATH = SEMANTIC_MODEL_V2_DIR / "measures.csv"
MODEL_MANIFEST_PATH = SEMANTIC_MODEL_V2_DIR / "model_manifest.json"
DOC_PATH = config.get_doc_path("dashboard_semantic_model_v2.md")


@dataclass(frozen=True)
class SemanticEntry:
    """Строка semantic dictionary."""

    technical_name: str
    display_name_ru: str
    unit: str
    data_type: str
    calculation_rule: str
    source_table: str
    source_column: str
    limitations: str
    applicable_period_types: str = "month, quarter, year"
    applicable_aggregation_modes: str = "cumulative, point"


def main() -> int:
    """Сформировать semantic model v2."""
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт построения dashboard semantic model v2")
    paths = build_semantic_model_v2()
    logger.info("Semantic model v2 создан: %s", paths)
    return 0


def build_semantic_model_v2() -> dict[str, Path]:
    """Собрать и записать semantic model v2."""
    SEMANTIC_MODEL_V2_DIR.mkdir(parents=True, exist_ok=True)
    field_dictionary = build_field_dictionary()
    kpi_dictionary = build_kpi_dictionary()
    measures = build_measures(kpi_dictionary)
    manifest = build_manifest(field_dictionary, kpi_dictionary, measures)

    field_dictionary.to_csv(FIELD_DICTIONARY_PATH, index=False, encoding="utf-8-sig")
    kpi_dictionary.to_csv(KPI_DICTIONARY_PATH, index=False, encoding="utf-8-sig")
    measures.to_csv(MEASURES_PATH, index=False, encoding="utf-8-sig")
    MODEL_MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    utils.write_markdown(DOC_PATH, build_doc(field_dictionary, kpi_dictionary, measures, manifest))
    return {
        "field_dictionary": FIELD_DICTIONARY_PATH,
        "kpi_dictionary": KPI_DICTIONARY_PATH,
        "measures": MEASURES_PATH,
        "model_manifest": MODEL_MANIFEST_PATH,
        "docs": DOC_PATH,
    }


def build_field_dictionary() -> pd.DataFrame:
    """Сформировать словарь полей semantic model v2."""
    entries = [
        SemanticEntry("auction_date", "Дата размещения", "date", "date", "исходное поле", "dashboard_auction_level", "auction_date", ""),
        SemanticEntry("report_period_label", "Отчетный период", "label", "text", "этап period_filter", "all dashboard datasets", "report_period_label", ""),
        SemanticEntry("report_period_start", "Начало отчетного периода", "date", "date", "этап period_filter", "report_scope", "report_period_start", ""),
        SemanticEntry("report_period_end", "Конец отчетного периода", "date", "date", "этап period_filter", "report_scope", "report_period_end", ""),
        SemanticEntry("report_year", "Отчетный год", "year", "integer", "год отчетного периода", "all dashboard datasets", "report_year", ""),
        SemanticEntry("report_period_type", "Тип периода", "period type", "text", "CLI parameter", "all dashboard datasets", "report_period_type", ""),
        SemanticEntry("aggregation_mode", "Режим агрегации", "mode", "text", "CLI parameter", "all dashboard datasets", "aggregation_mode", "cumulative и point не смешиваются в одном output"),
        SemanticEntry("is_target_period", "Целевой отчетный период", "boolean", "boolean", "этап period_filter", "report_scope", "is_target_period", ""),
        SemanticEntry("issue_code", "Код выпуска", "text", "text", "исходное поле", "dashboard_auction_level", "issue_code", ""),
        SemanticEntry("ofz_type", "Вид ОФЗ", "category", "text", "нормализация security_type", "dashboard_auction_level", "ofz_type", "Поддерживает ОФЗ-ПД, ОФЗ-ИН, ОФЗ-ПК и прочие виды при наличии данных"),
        SemanticEntry("format", "Формат размещения", "category", "text", "нормализация столбца Формат", "dashboard_auction_level", "format", "ДРПА не включать в demand-based ratios без флага ограничения"),
        SemanticEntry("maturity_bucket", "Сроковая категория", "category", "text", "классификация срока обращения", "dashboard_auction_level", "maturity_bucket", "short_term <= 5 лет; medium_term > 5 и <= 10; long_term > 10"),
        SemanticEntry("maturity_bucket_label", "Сроковая категория, подпись", "category", "text", "маппинг maturity_bucket", "dashboard_auction_level", "maturity_bucket_label", ""),
        SemanticEntry("maturity_years", "Срок до погашения", "лет", "number", "days_to_maturity / 365.25", "dashboard_auction_level", "maturity_years", "Пусто, если срок нельзя определить"),
        SemanticEntry("demand_volume", "Спрос", "млн рублей", "number", "нормализованный совокупный спрос", "dashboard_auction_level", "demand_volume", "Может отсутствовать для ДРПА"),
        SemanticEntry("supply_volume", "Предложение", "млн рублей", "number", "нормализованный объем предложения", "dashboard_auction_level", "supply_volume", "Не заменять фактическим размещением"),
        SemanticEntry("placement_volume", "Объем размещения по номиналу", "млн рублей", "number", "нормализованный объем размещения по номиналу", "dashboard_auction_level", "placement_volume", "На графиках отображается в млрд рублей"),
        SemanticEntry("placement_volume_bln", "Объем размещения по номиналу", "млрд рублей", "number", "placement_volume / 1000", "chart_data", "placement_volume_bln", "Только отображаемая величина для графиков"),
        SemanticEntry("revenue_volume", "Выручка от реализации ОФЗ", "млн рублей", "number", "proceeds_mln_rub или revenue source mapping", "dashboard_auction_level", "revenue_volume", "Может отсутствовать или требовать проверки source mapping"),
        SemanticEntry("weighted_avg_yield", "Средневзвешенная доходность", "% годовых", "number", "нормализованная доходность", "dashboard_auction_level", "weighted_avg_yield", "Строки без доходности исключаются из yield analytics"),
        SemanticEntry("cutoff_yield", "Доходность отсечения", "% годовых", "number", "нормализованная доходность отсечения", "dashboard_auction_level", "cutoff_yield", "Может отсутствовать"),
        SemanticEntry("cutoff_price", "Цена отсечения", "% от номинала", "number", "нормализованная цена отсечения", "dashboard_auction_level", "cutoff_price", "Без цены отсечения discount analysis ограничен"),
        SemanticEntry("discount_to_nominal", "Дисконт к номиналу", "п.п.", "number", "100 - cutoff_price", "dashboard_auction_level", "discount_to_nominal", "Рассчитывается только при наличии cutoff_price"),
        SemanticEntry("bid_to_cover_ratio", "Спрос / предложение", "ratio", "number", "demand_volume / supply_volume", "dashboard_auction_level", "bid_to_cover_ratio", "Не равно demand_to_placement_ratio"),
        SemanticEntry("demand_to_placement_ratio", "Спрос / объем размещения", "ratio", "number", "demand_volume / placement_volume", "dashboard_auction_level", "demand_to_placement_ratio", "Не называть bid-to-cover"),
        SemanticEntry("demand_satisfaction_ratio", "Коэффициент удовлетворения спроса", "ratio", "number", "placement_volume / demand_volume", "dashboard_auction_level", "demand_satisfaction_ratio", "Пусто при нулевом или отсутствующем спросе"),
        SemanticEntry("data_quality_flag", "Флаг качества данных", "flag", "text", "сводный флаг pipeline", "all dashboard datasets", "data_quality_flag", "Использовать для фильтров и предупреждений"),
    ]
    return entries_to_dataframe(entries, dictionary_type="field")


def build_kpi_dictionary() -> pd.DataFrame:
    """Сформировать KPI dictionary semantic model v2."""
    entries = [
        SemanticEntry("total_demand", "Совокупный спрос", "млн рублей", "number", "sum(demand_volume)", "dashboard_period_summary", "demand_volume", "ДРПА интерпретировать с учетом data_quality_flag"),
        SemanticEntry("total_supply", "Совокупное предложение", "млн рублей", "number", "sum(supply_volume)", "dashboard_period_summary", "supply_volume", "Не заменять объемом размещения"),
        SemanticEntry("total_placement_volume", "Объем размещения по номиналу", "млн рублей", "number", "sum(placement_volume)", "dashboard_period_summary", "placement_volume", "Для визуализаций использовать млрд рублей"),
        SemanticEntry("total_revenue_volume", "Выручка от реализации ОФЗ", "млн рублей", "number", "sum(revenue_volume)", "dashboard_period_summary", "revenue_volume", "Пусто или ограничено при отсутствии source mapping"),
        SemanticEntry("bid_to_cover_ratio", "Спрос / предложение", "ratio", "number", "sum(demand_volume) / sum(supply_volume)", "dashboard_period_summary", "demand_volume, supply_volume", "Пусто при нулевом предложении"),
        SemanticEntry("demand_to_placement_ratio", "Спрос / объем размещения", "ratio", "number", "sum(demand_volume) / sum(placement_volume)", "dashboard_period_summary", "demand_volume, placement_volume", "Не является bid-to-cover"),
        SemanticEntry("demand_satisfaction_ratio", "Коэффициент удовлетворения спроса", "ratio", "number", "sum(placement_volume) / sum(demand_volume)", "dashboard_demand_supply", "placement_volume, demand_volume", "Пусто при нулевом спросе"),
        SemanticEntry("weighted_avg_yield_by_placement", "Средневзвешенная доходность", "% годовых", "number", "sum(weighted_avg_yield * placement_volume) / sum(placement_volume)", "dashboard_period_summary", "weighted_avg_yield, placement_volume", "Fallback к среднему должен быть явно помечен"),
        SemanticEntry("yield_min", "Минимальная доходность", "% годовых", "number", "min(weighted_avg_yield)", "dashboard_yield_distribution", "weighted_avg_yield", "Строки без доходности исключаются"),
        SemanticEntry("yield_median", "Медианная доходность", "% годовых", "number", "median(weighted_avg_yield)", "dashboard_yield_distribution", "weighted_avg_yield", "Ограничено при малом n"),
        SemanticEntry("yield_max", "Максимальная доходность", "% годовых", "number", "max(weighted_avg_yield)", "dashboard_yield_distribution", "weighted_avg_yield", "Может отражать выброс"),
        SemanticEntry("placement_volume_share", "Доля сроковой категории", "доля", "number", "placement_volume / total_placement_volume by period", "dashboard_maturity_structure", "placement_volume", "Пусто при нулевом общем объеме"),
        SemanticEntry("nominal_revenue_gap", "Разница номинал - выручка", "млн рублей", "number", "placement_volume - revenue_volume", "revenue analytics", "placement_volume, revenue_volume", "Будет использоваться revenue analytics второй модернизации"),
        SemanticEntry("revenue_to_nominal_ratio", "Выручка / номинал", "ratio", "number", "revenue_volume / placement_volume", "revenue analytics", "revenue_volume, placement_volume", "Пусто при нулевом размещении"),
        SemanticEntry("nominal_discount_ratio", "Дисконт выручки к номиналу", "ratio", "number", "(placement_volume - revenue_volume) / placement_volume", "revenue analytics", "placement_volume, revenue_volume", "Требует надежной выручки"),
    ]
    return entries_to_dataframe(entries, dictionary_type="kpi")


def build_measures(kpi_dictionary: pd.DataFrame) -> pd.DataFrame:
    """Сформировать measures table на основе KPI dictionary."""
    measures = kpi_dictionary.copy()
    measures["measure_name"] = measures["technical_name"]
    measures["aggregation"] = measures["calculation_rule"].map(default_aggregation)
    measures["recommended_visuals"] = measures["technical_name"].map(recommended_visuals)
    return measures[
        [
            "semantic_version",
            "measure_name",
            "technical_name",
            "display_name_ru",
            "unit",
            "data_type",
            "aggregation",
            "calculation_rule",
            "source_table",
            "source_column",
            "limitations",
            "applicable_period_types",
            "applicable_aggregation_modes",
            "recommended_visuals",
        ]
    ]


def entries_to_dataframe(entries: Sequence[SemanticEntry], dictionary_type: str) -> pd.DataFrame:
    """Преобразовать semantic entries в DataFrame единого формата."""
    rows = []
    for entry in entries:
        rows.append(
            {
                "semantic_version": SEMANTIC_VERSION,
                "dictionary_type": dictionary_type,
                "technical_name": entry.technical_name,
                "display_name_ru": entry.display_name_ru,
                "unit": entry.unit,
                "data_type": entry.data_type,
                "calculation_rule": entry.calculation_rule,
                "source_table": entry.source_table,
                "source_column": entry.source_column,
                "limitations": entry.limitations,
                "applicable_period_types": entry.applicable_period_types,
                "applicable_aggregation_modes": entry.applicable_aggregation_modes,
            }
        )
    return pd.DataFrame(rows)


def default_aggregation(rule: str) -> str:
    """Определить рекомендуемую агрегацию меры."""
    normalized = rule.lower()
    if normalized.startswith("sum"):
        return "sum"
    if normalized.startswith("min"):
        return "min"
    if normalized.startswith("max"):
        return "max"
    if "median" in normalized:
        return "median"
    if "/" in normalized or "weighted" in normalized:
        return "calculated"
    return "none"


def recommended_visuals(technical_name: str) -> str:
    """Рекомендовать типы визуализаций для меры."""
    if "yield" in technical_name:
        return "line, boxplot, scatter"
    if "ratio" in technical_name or "bid_to_cover" in technical_name:
        return "line, scatter, KPI card"
    if "revenue" in technical_name:
        return "bar, line, scatter"
    if "placement" in technical_name or "demand" in technical_name or "supply" in technical_name:
        return "bar, stacked bar, line, Sankey"
    return "table, KPI card"


def build_manifest(field_dictionary: pd.DataFrame, kpi_dictionary: pd.DataFrame, measures: pd.DataFrame) -> dict[str, Any]:
    """Сформировать manifest semantic model v2."""
    now = datetime.now().replace(microsecond=0).isoformat()
    return {
        "semantic_version": SEMANTIC_VERSION,
        "modernization": "вторая модернизация",
        "generated_at": now,
        "model_dir": SEMANTIC_MODEL_V2_DIR.relative_to(config.PROJECT_ROOT).as_posix(),
        "files": {
            "field_dictionary": FIELD_DICTIONARY_PATH.relative_to(config.PROJECT_ROOT).as_posix(),
            "kpi_dictionary": KPI_DICTIONARY_PATH.relative_to(config.PROJECT_ROOT).as_posix(),
            "measures": MEASURES_PATH.relative_to(config.PROJECT_ROOT).as_posix(),
            "model_manifest": MODEL_MANIFEST_PATH.relative_to(config.PROJECT_ROOT).as_posix(),
        },
        "row_counts": {
            "field_dictionary": int(len(field_dictionary)),
            "kpi_dictionary": int(len(kpi_dictionary)),
            "measures": int(len(measures)),
        },
        "compatibility_notes": [
            "Совместимо с dashboard exports первого поколения.",
            "cumulative и point не смешиваются в одном output.",
            "Revenue measures являются частью второй модернизации и зависят от надежного source mapping выручки.",
        ],
        "required_columns": [
            "semantic_version",
            "technical_name",
            "display_name_ru",
            "unit",
            "data_type",
            "calculation_rule",
            "source_table",
            "source_column",
            "limitations",
            "applicable_period_types",
            "applicable_aggregation_modes",
        ],
    }


def build_doc(
    field_dictionary: pd.DataFrame,
    kpi_dictionary: pd.DataFrame,
    measures: pd.DataFrame,
    manifest: dict[str, Any],
) -> str:
    """Сформировать документацию semantic model v2."""
    lines = [
        "# Dashboard semantic model v2",
        "",
        "Метка: `вторая модернизация`.",
        "",
        f"- Semantic version: `{SEMANTIC_VERSION}`",
        f"- Generated at: `{manifest['generated_at']}`",
        f"- Model dir: `{manifest['model_dir']}`",
        "",
        "## Outputs",
        "",
        f"- `{FIELD_DICTIONARY_PATH.relative_to(config.PROJECT_ROOT).as_posix()}`",
        f"- `{KPI_DICTIONARY_PATH.relative_to(config.PROJECT_ROOT).as_posix()}`",
        f"- `{MEASURES_PATH.relative_to(config.PROJECT_ROOT).as_posix()}`",
        f"- `{MODEL_MANIFEST_PATH.relative_to(config.PROJECT_ROOT).as_posix()}`",
        "",
        "## Состав",
        "",
        f"- Field dictionary rows: `{len(field_dictionary)}`",
        f"- KPI dictionary rows: `{len(kpi_dictionary)}`",
        f"- Measures rows: `{len(measures)}`",
        "",
        "## Обязательные поля словарей",
        "",
        "- `semantic_version`",
        "- `technical_name`",
        "- `display_name_ru`",
        "- `unit`",
        "- `data_type`",
        "- `calculation_rule`",
        "- `source_table`",
        "- `source_column`",
        "- `limitations`",
        "- `applicable_period_types`",
        "- `applicable_aggregation_modes`",
        "",
        "## Совместимость",
        "",
        "- Semantic model v2 не заменяет dashboard exports первого поколения, а добавляет версионированный слой описаний.",
        "- `cumulative` и `point` должны использоваться как разные режимы и не смешиваться в одном output.",
        "- Revenue KPI включены как словарные элементы второй модернизации; полноценные revenue outputs формируются отдельным этапом.",
        "",
        "## Ограничения",
        "",
        "- Если источник выручки отсутствует или ненадежен, revenue measures должны оставаться ограниченными.",
        "- ДРПА не должны механически включаться в demand-based ratios без проверки валидности спроса.",
        "- Нулевые размещения, нулевое предложение и пропуски доходности должны учитываться через `data_quality_flag`.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
