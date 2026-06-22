# Dashboard semantic model v2

Метка: `вторая модернизация`.

- Semantic version: `2.0.0`
- Generated at: `2026-06-22T15:11:11`
- Model dir: `outputs/dashboards/semantic_model_v2`

## Outputs

- `outputs/dashboards/semantic_model_v2/field_dictionary.csv`
- `outputs/dashboards/semantic_model_v2/kpi_dictionary.csv`
- `outputs/dashboards/semantic_model_v2/measures.csv`
- `outputs/dashboards/semantic_model_v2/model_manifest.json`

## Состав

- Field dictionary rows: `27`
- KPI dictionary rows: `15`
- Measures rows: `15`

## Обязательные поля словарей

- `semantic_version`
- `technical_name`
- `display_name_ru`
- `unit`
- `data_type`
- `calculation_rule`
- `source_table`
- `source_column`
- `limitations`
- `applicable_period_types`
- `applicable_aggregation_modes`

## Совместимость

- Semantic model v2 не заменяет dashboard exports первого поколения, а добавляет версионированный слой описаний.
- `cumulative` и `point` должны использоваться как разные режимы и не смешиваться в одном output.
- Revenue KPI включены как словарные элементы второй модернизации; полноценные revenue outputs формируются отдельным этапом.

## Ограничения

- Если источник выручки отсутствует или ненадежен, revenue measures должны оставаться ограниченными.
- ДРПА не должны механически включаться в demand-based ratios без проверки валидности спроса.
- Нулевые размещения, нулевое предложение и пропуски доходности должны учитываться через `data_quality_flag`.
