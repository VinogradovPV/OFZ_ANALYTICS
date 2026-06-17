# Контракт dashboard exports

Дата актуализации: 2026-06-08.

## Назначение

Dashboard exports в `outputs/dashboards/` являются BI-ready слоем поверх processed/report scope данных. Они разделены с chart data и analytical reports, чтобы dashboard не зависел от HTML-специфичных label/hover полей.

Generated dashboard exports не коммитятся в Git.

## Основные файлы

| Семейство | Путь | Назначение |
|---|---|---|
| Auction level | `outputs/dashboards/auction_level_<...>.csv` | Строки уровня отдельного размещения. |
| Period summary | `outputs/dashboards/period_summary_<...>.csv` | Периодные KPI. |
| KPI summary | `outputs/dashboards/kpi_summary_<...>.csv` | Long-format KPI для карточек. |
| Maturity structure | `outputs/dashboards/maturity_structure_<...>.csv` | Структура по срокам. |
| Yield distribution | `outputs/dashboards/yield_distribution_<...>.csv` | Распределение доходности. |
| Demand supply | `outputs/dashboards/demand_supply_<...>.csv` | Спрос/предложение/размещение. |
| Monthly | `outputs/dashboards/monthly/` | Monthly dashboard layer. |
| Semantic layer | `outputs/dashboards/semantic_layer/` | Semantic exports первого поколения. |
| Metadata | `metadata_<...>.json` | Параметры запуска и список exports. |
| Data dictionary | `data_dictionary_<...>.csv` | Словарь dashboard fields. |

## Общие обязательные поля

| Поле | Тип | Nullable | Назначение |
|---|---|---|---|
| `report_period_label` | string | no | Период dashboard row. |
| `report_year` | integer | no, если применимо | Год. |
| `aggregation_mode` | string | no | `cumulative` или `point`. |
| `metric_code` | string | no для long KPI | Техническое имя KPI. |
| `metric_name_ru` | string | no для long KPI | Русское имя KPI. |
| `metric_value` | number/string | yes | Значение KPI. |
| `metric_unit` | string | yes | Единица измерения. |
| `data_quality_flag` | string | yes | Quality flag. |
| `data_quality_display` | string | yes | Русское описание качества. |

## Единицы измерения

Dashboard exports могут хранить одновременно raw и display поля:

- raw volumes: млн рублей;
- `_volume_bln`: млрд рублей;
- yield: `% годовых`;
- discount: `п.п.`;
- ratios: `%` или ratio по названию поля.

Если dashboard export содержит `_volume_bln`, рядом должен быть unit field или запись в data dictionary/semantic model.

## Display-поля

Dashboard layer должен предпочитать явные display fields:

- `display_name_ru`;
- `metric_name_ru`;
- `unit`;
- `limitations`;
- `data_quality_display`.

Сырые технические flags не должны быть единственным пользовательским описанием.

## QA / Manifest Связь

- `quality_gate.py` проверяет наличие dashboard exports.
- `run_manifest.py` фиксирует пути generated dashboard artifacts.
- `build_semantic_model_v2.py` создает версионированный словарь для dashboard consumers.
