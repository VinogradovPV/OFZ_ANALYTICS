# Аналитические табличные отчеты

Дата формирования: `2026-06-04 19:08:37`.

## Параметры

- `report_date`: `2026-01-01`
- `retrospective_years`: `4`
- `period_type`: `year`
- `aggregation_mode`: `cumulative`

## Правила сортировки аналитических таблиц

- `ofz_yield_by_type` сортируется прежде всего по отчетному периоду, затем по виду ОФЗ.
- `placement_volume_by_maturity` сортируется прежде всего по отчетному периоду, затем по сроковой категории.
- Если доступен `report_period_start`, он используется как основной надежный ключ периода; иначе используется `report_period_order`.
- Внутри периода сроковые категории идут в порядке: краткосрочные -> среднесрочные -> долгосрочные -> requires_review.
- Такая сортировка нужна, чтобы отчетный период и ретроспектива читались как последовательность сравнения, а не как блоки по категориям.

## Таблица доходности по видам ОФЗ

- CSV: `outputs/exports/analytical_csv/ofz_yield_by_type_year_cumulative_2026-01-01_retrospective_4.csv`
- XLSX: `outputs/reports/analytical_tables/ofz_yield_by_type_year_cumulative_2026-01-01_retrospective_4.xlsx`

| report_period_label | report_year | report_period_type | aggregation_mode | report_period_order | report_period_start | ofz_type | placement_volume | yield_min | yield_weighted_avg | yield_max | yield_min_yoy_change | yield_weighted_avg_yoy_change | yield_max_yoy_change | auction_count | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021 | 2021 | year | cumulative | 0 | 2021-01-01 | ОФЗ-ИН | 139402 | 2.39 | 2.68114 | 3.09 |  |  |  | 13 | ok |
| 2021 | 2021 | year | cumulative | 0 | 2021-01-01 | ОФЗ-ПД | 2.49696e+06 | 5.55 | 7.17975 | 8.71 |  |  |  | 67 | ok |
| 2022 | 2022 | year | cumulative | 1 | 2022-01-01 | ОФЗ-ИН | 155529 | 3.09 | 3.30522 | 3.35 | 0.7 | 0.62408 | 0.26 | 10 | ok |
| 2022 | 2022 | year | cumulative | 1 | 2022-01-01 | ОФЗ-ПД | 625730 | 8.94 | 10.026 | 10.62 | 3.39 | 2.84628 | 1.91 | 15 | ok |
| 2023 | 2023 | year | cumulative | 2 | 2023-01-01 | ОФЗ-ИН | 316335 | 3.06 | 3.2615 | 4.22 | -0.03 | -0.043712 | 0.87 | 16 | ok |
| 2023 | 2023 | year | cumulative | 2 | 2023-01-01 | ОФЗ-ПД | 1.70132e+06 | 9.8 | 10.9817 | 12.5 | 0.86 | 0.955671 | 1.88 | 61 | ok |
| 2024 | 2024 | year | cumulative | 3 | 2024-01-01 | ОФЗ-ИН | 8943.83 | 5.17 | 5.17 | 5.17 | 2.11 | 1.9085 | 0.95 | 1 | ok |
| 2024 | 2024 | year | cumulative | 3 | 2024-01-01 | ОФЗ-ПД | 1.79662e+06 | 11.87 | 14.1195 | 18.42 | 2.07 | 3.13779 | 5.92 | 66 | ok |
| 2024 | 2024 | year | cumulative | 3 | 2024-01-01 | ОФЗ-ПК | 27716.7 | 0 | 0 | 0 |  |  |  | 1 | ok |
| 2025 | 2025 | year | cumulative | 4 | 2025-01-01 | ОФЗ-ПД | 6.35587e+06 | 13.51 | 15.2912 | 17.49 | 1.64 | 1.1717 | -0.93 | 135 | ok |
| 2025 | 2025 | year | cumulative | 4 | 2025-01-01 | ОФЗ-ПК | 1.69122e+06 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | ok |

## Таблица совокупного спроса и совокупного предложения

- CSV: `outputs/exports/analytical_csv/demand_supply_year_cumulative_2026-01-01_retrospective_4.csv`
- XLSX: `outputs/reports/analytical_tables/demand_supply_year_cumulative_2026-01-01_retrospective_4.xlsx`

| report_period_label | report_year | report_period_type | aggregation_mode | report_period_start | report_period_end | total_demand | total_supply | total_demand_yoy_change | total_supply_yoy_change | bid_to_cover_ratio | bid_to_cover_ratio_yoy_change | demand_supply_ratio | demand_supply_ratio_yoy_change | auction_count | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021 | 2021 | year | cumulative | 2021-01-01 | 2021-12-31 | 4.74442e+06 | 1.29816e+07 |  |  | 0.365473 |  | 0.365473 |  | 83 | ok |
| 2022 | 2022 | year | cumulative | 2022-01-01 | 2022-12-31 | 6.60459e+06 | 9.77621e+06 | 1.86018e+06 | -3.20536e+06 | 0.675578 | 0.310105 | 0.675578 | 0.310105 | 37 | ok |
| 2023 | 2023 | year | cumulative | 2023-01-01 | 2023-12-31 | 6.03043e+06 | 2.83754e+07 | -574160 | 1.85992e+07 | 0.212523 | -0.463055 | 0.212523 | -0.463055 | 95 | ok |
| 2024 | 2024 | year | cumulative | 2024-01-01 | 2024-12-31 | 9.93345e+06 | 3.29047e+07 | 3.90302e+06 | 4.52922e+06 | 0.301886 | 0.089363 | 0.301886 | 0.089363 | 104 | ok |
| 2025 | 2025 | year | cumulative | 2025-01-01 | 2025-12-31 | 1.26225e+07 | 2.83435e+07 | 2.68904e+06 | -4.56116e+06 | 0.44534 | 0.143454 | 0.44534 | 0.143454 | 142 | ok |

## Таблица объемов размещения ОФЗ по срокам обращения

- CSV: `outputs/exports/analytical_csv/placement_volume_by_maturity_year_cumulative_2026-01-01_retrospective_4.csv`
- XLSX: `outputs/reports/analytical_tables/placement_volume_by_maturity_year_cumulative_2026-01-01_retrospective_4.xlsx`

| report_period_label | report_year | report_period_type | aggregation_mode | report_period_order | report_period_start | maturity_bucket | maturity_bucket_order | maturity_bucket_label | placement_volume | placement_volume_yoy_change | placement_volume_share | placement_volume_share_yoy_change | auction_count | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021 | 2021 | year | cumulative | 0 | 2021-01-01 | short_term | 1 | Краткосрочные (до 5 лет включительно) | 204533 |  | 0.0775814 |  | 6 | ok |
| 2021 | 2021 | year | cumulative | 0 | 2021-01-01 | medium_term | 2 | Среднесрочные (свыше 5 до 10 лет включительно) | 1.65569e+06 |  | 0.628022 |  | 42 | ok |
| 2021 | 2021 | year | cumulative | 0 | 2021-01-01 | long_term | 3 | Долгосрочные (более 10 лет) | 776138 |  | 0.294397 |  | 35 | ok |
| 2022 | 2022 | year | cumulative | 1 | 2022-01-01 | medium_term | 2 | Среднесрочные (свыше 5 до 10 лет включительно) | 1.06042e+06 | -595278 | 0.323173 | -0.304848 | 26 | ok |
| 2022 | 2022 | year | cumulative | 1 | 2022-01-01 | long_term | 3 | Долгосрочные (более 10 лет) | 2.22084e+06 | 1.44471e+06 | 0.676827 | 0.38243 | 11 | ok |
| 2023 | 2023 | year | cumulative | 2 | 2023-01-01 | medium_term | 2 | Среднесрочные (свыше 5 до 10 лет включительно) | 1.02909e+06 | -31324.4 | 0.361643 | 0.0384696 | 42 | ok |
| 2023 | 2023 | year | cumulative | 2 | 2023-01-01 | long_term | 3 | Долгосрочные (более 10 лет) | 1.81651e+06 | -404335 | 0.638357 | -0.0384696 | 53 | ok |
| 2024 | 2024 | year | cumulative | 3 | 2024-01-01 | short_term | 1 | Краткосрочные (до 5 лет включительно) | 129178 | -75354.5 | 0.0295156 | -0.0480658 | 12 | ok |
| 2024 | 2024 | year | cumulative | 3 | 2024-01-01 | medium_term | 2 | Среднесрочные (свыше 5 до 10 лет включительно) | 435376 | -593715 | 0.0994777 | -0.262165 | 13 | ok |
| 2024 | 2024 | year | cumulative | 3 | 2024-01-01 | long_term | 3 | Долгосрочные (более 10 лет) | 3.81206e+06 | 1.99555e+06 | 0.871007 | 0.23265 | 79 | ok |
| 2025 | 2025 | year | cumulative | 4 | 2025-01-01 | short_term | 1 | Краткосрочные (до 5 лет включительно) | 600070 | 470892 | 0.0745699 | 0.0450543 | 10 | ok |
| 2025 | 2025 | year | cumulative | 4 | 2025-01-01 | medium_term | 2 | Среднесрочные (свыше 5 до 10 лет включительно) | 1.37489e+06 | 939512 | 0.170855 | 0.0713776 | 37 | ok |
| 2025 | 2025 | year | cumulative | 4 | 2025-01-01 | long_term | 3 | Долгосрочные (более 10 лет) | 6.07213e+06 | 2.26007e+06 | 0.754575 | -0.116432 | 95 | ok |

## Ограничения

- В report scope есть несостоявшиеся или нулевые размещения: 36; ratio с размещением может быть пустым.
- В report scope есть строки ДРПА: 66; при наличии `demand_volume` они включаются в таблицу спроса и предложения.
- Таблица доходности исключила строки без доходности: 74.
- Таблица спроса и предложения группирует данные по `report_period_start` и `report_period_end`; для cumulative-режима суммируется весь накопленный интервал report scope.
- Таблица спроса и предложения использует `demand_volume` из столбца `Совокупный объем спроса по номиналу` и `supply_volume` из столбца `Объем предложения`; суммируются и аукционы, и ДРПА при наличии значений.
- Таблица сроков обращения классифицирует сроки по `days_to_maturity`.
