# Контракт processed data

Дата актуализации: 2026-06-08.

## Назначение

Processed datasets в `data/processed/` являются воспроизводимыми промежуточными слоями pipeline. Они не являются raw source, но задают основной контракт для analytics, charts, dashboard exports, schema validation и run manifest.

`data/raw/` коммитится как source dataset. `data/processed/` пересоздается pipeline и не должен редактироваться вручную.

## Основные файлы

| Файл | Назначение |
|---|---|
| `data/processed/ofz_auctions_clean.csv` | Очищенные строки размещений/аукционов после нормализации raw Excel. |
| `data/processed/ofz_auctions_features.csv` | Feature layer с расчетными KPI, классификациями и quality flags. |
| `data/processed/ofz_auctions_report_scope.csv` | Параметризованный report scope для выбранных period/report settings. |
| `data/processed/ofz_monthly_metrics.csv` | Monthly layer для помесячных графиков и dashboard exports. |

## Обязательные группы колонок

| Группа | Колонки | Типы | Nullable policy |
|---|---|---|---|
| Идентификация | `auction_date`, `issue_code`, `ofz_type`, `format` | date/string/string/string | `auction_date` и `issue_code` обязательны для строк размещений; `format` должен быть нормализован. |
| Источник | `source_file`, `source_sheet`, `source_year`, `processing_timestamp` | string/string/integer/datetime-string | Обязательны в clean/features слоях. |
| Период | `report_period_label`, `report_period_type`, `report_year`, `aggregation_mode`, `is_target_period` | string/string/integer/string/bool | Обязательны в report scope. |
| Объемы | `placement_volume`, `demand_volume`, `supply_volume`, `revenue_volume` | number | Исходные объемы хранятся в млн рублей; revenue может быть nullable. |
| Доходность | `weighted_avg_yield` или source yield column | number | Nullable; строки без доходности исключаются из yield-графиков. |
| Цена/дисконт | `cutoff_price`, `discount_to_nominal` | number | Nullable; discount может рассчитываться только при валидной цене отсечения. |
| Ratios | `bid_to_cover_ratio`, `demand_to_placement_ratio`, `revenue_to_nominal_ratio` | number | Nullable при нулевых/отсутствующих знаменателях. |
| Качество | `data_quality_flag`, `data_quality_display`, `source_markers` | string | Nullable, но recommended для rows с ограничениями. |

## Единицы измерения

| Поле | Unit |
|---|---|
| `placement_volume` | млн рублей |
| `demand_volume` | млн рублей |
| `supply_volume` | млн рублей |
| `revenue_volume` | млн рублей |
| `weighted_avg_yield` | % годовых |
| `cutoff_price` | % от номинала |
| `discount_to_nominal` | п.п. |
| `bid_to_cover_ratio` | ratio |
| `demand_to_placement_ratio` | ratio |
| `revenue_to_nominal_ratio` | % |

Display-поля в млрд рублей создаются на export/chart layers и должны иметь unit contract из `chart_data_contract.md`.

## Допустимые категории

| Поле | Категории |
|---|---|
| `aggregation_mode` | `cumulative`, `point` |
| `report_period_type` / CLI `period_type` | `month`, `quarter`, `year` |
| `format` | `Аукцион`, `ДРПА`, `requires_review`/ограниченные значения только с quality flag |
| `ofz_type` | Нормализованные типы ОФЗ из raw/source layer |
| `maturity_bucket_label` | Краткосрочные, среднесрочные, долгосрочные или project-local equivalents |

## QA / Schema Связь

- `scripts/schema_validation.py` проверяет report scope, periods, monthly layer и outputs structure.
- `scripts/anomaly_tests.py` проверяет нулевые размещения, пропуски доходности, выбросы спроса/покрытия, missing cutoff/discount/revenue anomalies.
- `scripts/regression_tests.py` контролирует воспроизводимость ключевых расчетов.
- `scripts/run_manifest.py` фиксирует параметры запуска и raw/processed metadata.
