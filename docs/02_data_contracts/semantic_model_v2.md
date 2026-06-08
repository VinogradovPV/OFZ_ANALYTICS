# Semantic Model V2 Contract

Дата актуализации: 2026-06-08.

## Назначение

Semantic model v2 описывает поля, KPI и меры dashboard/analytics слоев в стабильной форме. Это контракт для BI, документации и downstream-потребителей.

## Пути

| Файл | Путь |
|---|---|
| Field dictionary | `outputs/dashboards/semantic_model_v2/field_dictionary.csv` |
| KPI dictionary | `outputs/dashboards/semantic_model_v2/kpi_dictionary.csv` |
| Measures | `outputs/dashboards/semantic_model_v2/measures.csv` |
| Manifest | `outputs/dashboards/semantic_model_v2/model_manifest.json` |
| Документация | `docs/05_dashboard/dashboard_semantic_model_v2.md` |

Generated semantic model CSV/JSON не коммитятся в Git; документация коммитится.

## Обязательные колонки словарей

| Поле | Тип | Nullable | Назначение |
|---|---|---|---|
| `semantic_version` | string | no | Версия semantic model. |
| `technical_name` | string | no | Техническое имя поля/KPI. |
| `display_name_ru` | string | no | Русское пользовательское имя. |
| `unit` | string | yes | Единица измерения. |
| `data_type` | string | no | `number`, `string`, `date`, `boolean`. |
| `calculation_rule` | string | yes | Формула или метод расчета. |
| `source_table` | string | no | Таблица-источник. |
| `source_column` | string | yes | Колонка-источник. |
| `limitations` | string | yes | Ограничения использования. |
| `applicable_period_types` | string | no | `month`, `quarter`, `year`, `all`. |
| `applicable_aggregation_modes` | string | no | `cumulative`, `point`, `all`. |

## Measures Contract

`measures.csv` расширяет KPI dictionary и должен содержать:

- `measure_name`;
- `aggregation`;
- `recommended_visuals`;
- все поля из KPI dictionary, если применимо.

## Units and Display Names

| Semantic field | Display | Unit |
|---|---|---|
| `placement_volume_bln` | Объем размещения по номиналу | млрд рублей |
| `revenue_volume_bln` | Выручка от реализации | млрд рублей |
| `nominal_revenue_gap_bln` | Номинал минус выручка | млрд рублей |
| `weighted_avg_yield` | Средневзвешенная доходность размещения | % годовых |
| `discount_to_nominal` | Дисконт к номиналу | п.п. |
| `revenue_to_nominal_ratio` | Выручка / номинал | % |

## Quality Fields

Semantic model должен включать или описывать:

- `data_quality_flag`;
- `data_quality_display`;
- `limitations`;
- nullable policy для revenue/discount/yield.

## QA Связь

- `quality_gate.py` проверяет наличие semantic model v2 artifacts.
- `build_semantic_model_v2.py` является генератором contract artifacts.
- `docs/05_dashboard/dashboard_semantic_model_v2.md` должен соответствовать этому contract.
