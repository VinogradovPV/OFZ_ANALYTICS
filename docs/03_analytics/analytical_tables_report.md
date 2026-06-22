# Аналитические табличные отчеты

Дата формирования: `2026-06-22 15:11:06`.

## Параметры

- `report_date`: `2026-05-01`
- `retrospective_years`: `4`
- `period_type`: `month`
- `aggregation_mode`: `cumulative`

## Правила сортировки аналитических таблиц

- `ofz_yield_by_type` сортируется прежде всего по отчетному периоду, затем по виду ОФЗ.
- `placement_volume_by_maturity` сортируется прежде всего по отчетному периоду, затем по сроковой категории.
- Если доступен `report_period_start`, он используется как основной надежный ключ периода; иначе используется `report_period_order`.
- Внутри периода сроковые категории идут в порядке: краткосрочные -> среднесрочные -> долгосрочные -> requires_review.
- Такая сортировка нужна, чтобы отчетный период и ретроспектива читались как последовательность сравнения, а не как блоки по категориям.

## Таблица доходности по видам ОФЗ

- CSV: `outputs/exports/analytical_csv/ofz_yield_by_type_month_cumulative_2026-05-01_retrospective_4.csv`
- XLSX: `outputs/reports/monthly_tables/ofz_yield_by_type_month_cumulative_2026-05-01_retrospective_4.xlsx`

| report_period_label | report_year | report_period_type | aggregation_mode | report_period_order | report_period_start | ofz_type | placement_volume | yield_min | yield_weighted_avg | yield_max | yield_min_yoy_change | yield_weighted_avg_yoy_change | yield_max_yoy_change | auction_count | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022-M01-M04 | 2022 | month | cumulative | 0 | 2022-01-01 | ОФЗ-ПД | 111915 | 8.94 | 9.45711 | 9.59 |  |  |  | 3 | ok |
| 2023-M01-M04 | 2023 | month | cumulative | 1 | 2023-01-01 | ОФЗ-ПД | 835877 | 9.8 | 10.4697 | 10.84 | 0.86 | 1.01259 | 1.25 | 26 | ok |
| 2024-M01-M04 | 2024 | month | cumulative | 2 | 2024-01-01 | ОФЗ-ПД | 1.13867e+06 | 11.87 | 12.9259 | 13.8 | 2.07 | 2.45621 | 2.96 | 33 | ok |
| 2025-M01-M04 | 2025 | month | cumulative | 3 | 2025-01-01 | ОФЗ-ПД | 1.74544e+06 | 14.47 | 16.1527 | 17.49 | 2.6 | 3.22682 | 3.69 | 42 | ok |
| 2026-M01-M04 | 2026 | month | cumulative | 4 | 2026-01-01 | ОФЗ-ПД | 2.47772e+06 | 13.75 | 14.6938 | 15.32 | -0.72 | -1.45896 | -2.17 | 41 | ok |

## Таблица совокупного спроса и совокупного предложения

- CSV: `outputs/exports/analytical_csv/demand_supply_month_cumulative_2026-05-01_retrospective_4.csv`
- XLSX: `outputs/reports/monthly_tables/demand_supply_month_cumulative_2026-05-01_retrospective_4.xlsx`

| report_period_label | report_year | report_period_type | aggregation_mode | report_period_start | report_period_end | total_demand | total_supply | total_demand_yoy_change | total_supply_yoy_change | bid_to_cover_ratio | bid_to_cover_ratio_yoy_change | demand_supply_ratio | demand_supply_ratio_yoy_change | auction_count | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022-M01-M04 | 2022 | month | cumulative | 2022-01-01 | 2022-04-30 | 252099 | 1.2082e+06 |  |  | 0.208656 |  | 0.208656 |  | 5 | ok |
| 2023-M01-M04 | 2023 | month | cumulative | 2023-01-01 | 2023-04-30 | 1.90724e+06 | 9.30988e+06 | 1.65515e+06 | 8.10167e+06 | 0.204862 | -0.00379339 | 0.204862 | -0.00379339 | 34 | ok |
| 2024-M01-M04 | 2024 | month | cumulative | 2024-01-01 | 2024-04-30 | 1.73564e+06 | 5.22732e+06 | -171606 | -4.08256e+06 | 0.332032 | 0.12717 | 0.332032 | 0.12717 | 37 | ok |
| 2025-M01-M04 | 2025 | month | cumulative | 2025-01-01 | 2025-04-30 | 2.85448e+06 | 8.56045e+06 | 1.11884e+06 | 3.33314e+06 | 0.333449 | 0.00141696 | 0.333449 | 0.00141696 | 45 | ok |
| 2026-M01-M04 | 2026 | month | cumulative | 2026-01-01 | 2026-04-30 | 3.94459e+06 | 1.29817e+07 | 1.09012e+06 | 4.42126e+06 | 0.303858 | -0.0295915 | 0.303858 | -0.0295915 | 42 | ok |

## Таблица объемов размещения ОФЗ по срокам обращения

- CSV: `outputs/exports/analytical_csv/placement_volume_by_maturity_month_cumulative_2026-05-01_retrospective_4.csv`
- XLSX: `outputs/reports/monthly_tables/placement_volume_by_maturity_month_cumulative_2026-05-01_retrospective_4.xlsx`

| report_period_label | report_year | report_period_type | aggregation_mode | report_period_order | report_period_start | maturity_bucket | maturity_bucket_order | maturity_bucket_label | placement_volume | placement_volume_yoy_change | placement_volume_share | placement_volume_share_yoy_change | auction_count | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022-M01-M04 | 2022 | month | cumulative | 0 | 2022-01-01 | medium_term | 2 | Среднесрочные (свыше 5 до 10 лет включительно) | 91258 |  | 0.712512 |  | 2 | ok |
| 2022-M01-M04 | 2022 | month | cumulative | 0 | 2022-01-01 | long_term | 3 | Долгосрочные (более 10 лет) | 36821.3 |  | 0.287488 |  | 3 | ok |
| 2023-M01-M04 | 2023 | month | cumulative | 1 | 2023-01-01 | medium_term | 2 | Среднесрочные (свыше 5 до 10 лет включительно) | 559147 | 467890 | 0.57915 | -0.133361 | 18 | ok |
| 2023-M01-M04 | 2023 | month | cumulative | 1 | 2023-01-01 | long_term | 3 | Долгосрочные (более 10 лет) | 406315 | 369493 | 0.42085 | 0.133361 | 16 | ok |
| 2024-M01-M04 | 2024 | month | cumulative | 2 | 2024-01-01 | short_term | 1 | Краткосрочные (до 5 лет включительно) | 54472.8 |  | 0.0474663 |  | 9 | ok |
| 2024-M01-M04 | 2024 | month | cumulative | 2 | 2024-01-01 | medium_term | 2 | Среднесрочные (свыше 5 до 10 лет включительно) | 332067 | -227081 | 0.289355 | -0.289795 | 9 | ok |
| 2024-M01-M04 | 2024 | month | cumulative | 2 | 2024-01-01 | long_term | 3 | Долгосрочные (более 10 лет) | 761070 | 354756 | 0.663179 | 0.242329 | 19 | ok |
| 2025-M01-M04 | 2025 | month | cumulative | 3 | 2025-01-01 | short_term | 1 | Краткосрочные (до 5 лет включительно) | 50000 | -4472.76 | 0.028646 | -0.0188202 | 1 | ok |
| 2025-M01-M04 | 2025 | month | cumulative | 3 | 2025-01-01 | medium_term | 2 | Среднесрочные (свыше 5 до 10 лет включительно) | 140239 | -191828 | 0.0803456 | -0.209009 | 11 | ok |
| 2025-M01-M04 | 2025 | month | cumulative | 3 | 2025-01-01 | long_term | 3 | Долгосрочные (более 10 лет) | 1.5552e+06 | 794133 | 0.891008 | 0.22783 | 33 | ok |
| 2026-M01-M04 | 2026 | month | cumulative | 4 | 2026-01-01 | short_term | 1 | Краткосрочные (до 5 лет включительно) | 72917.9 | 22917.9 | 0.0294295 | 0.000783463 | 3 | ok |
| 2026-M01-M04 | 2026 | month | cumulative | 4 | 2026-01-01 | medium_term | 2 | Среднесрочные (свыше 5 до 10 лет включительно) | 1.0587e+06 | 918463 | 0.42729 | 0.346944 | 15 | ok |
| 2026-M01-M04 | 2026 | month | cumulative | 4 | 2026-01-01 | long_term | 3 | Долгосрочные (более 10 лет) | 1.3461e+06 | -209108 | 0.543281 | -0.347727 | 24 | ok |

## Ограничения

- В report scope есть несостоявшиеся или нулевые размещения: 9; ratio с размещением может быть пустым.
- В report scope есть строки ДРПА: 35; при наличии `demand_volume` они включаются в таблицу спроса и предложения.
- Таблица доходности исключила строки без доходности: 18.
- Таблица спроса и предложения группирует данные по `report_period_start` и `report_period_end`; для cumulative-режима суммируется весь накопленный интервал report scope.
- Таблица спроса и предложения использует `demand_volume` из столбца `Совокупный объем спроса по номиналу` и `supply_volume` из столбца `Объем предложения`; суммируются и аукционы, и ДРПА при наличии значений.
- Таблица сроков обращения классифицирует сроки по `days_to_maturity`.
