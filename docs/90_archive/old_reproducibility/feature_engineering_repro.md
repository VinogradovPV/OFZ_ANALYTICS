# Отчет feature engineering

Дата формирования: 2026-05-18 10:33:36

## Краткий вывод

Источник: `data/processed/ofz_auctions_clean_repro.csv`.
Строк во входном dataset: 678.
Строк в features dataset: 678.
Колонок во входном dataset: 28.
Колонок в features dataset: 64.
Добавлено признаков: 36.

## Добавленные признаки

| Признак | Пропусков |
|---|---:|
| `auction_year` | 0 |
| `auction_quarter` | 0 |
| `auction_month` | 0 |
| `is_q1` | 0 |
| `placement_volume` | 1 |
| `demand_volume` | 79 |
| `supply_volume` | 0 |
| `weighted_avg_yield` | 106 |
| `yield` | 106 |
| `bid_to_cover_ratio` | 114 |
| `placement_to_offer_ratio` | 1 |
| `demand_to_offer_ratio` | 79 |
| `maturity_years` | 0 |
| `maturity_bucket` | 0 |
| `maturity_bucket_label` | 0 |
| `ofz_type` | 0 |
| `issue_year_weighted_avg_yield` | 55 |
| `yield_yoy_change` | 367 |
| `demand_pressure_indicator` | 0 |
| `yield_zscore_in_year` | 106 |
| `yield_pressure_indicator` | 0 |
| `auction_efficiency_score` | 178 |
| `issue_year_placement_mln_rub` | 0 |
| `issue_year_demand_mln_rub` | 0 |
| `year_total_placement_mln_rub` | 0 |
| `year_total_demand_mln_rub` | 0 |
| `issue_placement_share_in_year` | 0 |
| `issue_demand_share_in_year` | 0 |
| `year_placement_hhi_by_issue` | 0 |
| `year_demand_hhi_by_issue` | 0 |
| `year_yield_volatility_std` | 0 |
| `issue_yield_volatility_std` | 77 |
| `placement_deviation_from_average` | 1 |
| `demand_deviation_from_average` | 79 |
| `yield_deviation_from_average` | 106 |
| `feature_processing_timestamp` | 0 |

## Skipped / requires_review

Пропущенных блоков признаков нет.

## Проверка обязательных признаков

| Признак | Статус | Пропусков | Назначение |
|---|---|---:|---|
| `bid_to_cover_ratio` | ok | 114 | bid-to-cover для аналитики спроса |
| `placement_volume` | ok | 1 | объем размещения |
| `demand_volume` | ok | 79 | объем спроса |
| `supply_volume` | ok | 0 | объем предложения |
| `yield` | ok | 106 | основной alias доходности для табличных отчетов |
| `weighted_avg_yield` | ok | 106 | средневзвешенная доходность |
| `maturity_years` | ok | 0 | срок обращения в годах |
| `maturity_bucket` | ok | 0 | категория срока обращения |
| `maturity_bucket_label` | ok | 0 | человекочитаемая категория срока обращения |
| `ofz_type` | ok | 0 | тип ОФЗ |
| `auction_year` | ok | 0 | год аукциона |
| `auction_quarter` | ok | 0 | квартал аукциона |
| `auction_month` | ok | 0 | месяц аукциона |
| `demand_pressure_indicator` | ok | 0 | индикатор давления спроса |
| `yield_pressure_indicator` | ok | 0 | индикатор давления доходности |
| `auction_efficiency_score` | ok | 178 | интегральный показатель эффективности аукциона |

## Правило классификации сроков обращения

- `short_term`: краткосрочные ОФЗ, срок обращения до 5 лет.
- `medium_term`: среднесрочные ОФЗ, срок обращения от 5 до 10 лет включительно.
- `long_term`: долгосрочные ОФЗ, срок обращения свыше 10 лет.
- `requires_review`: срок обращения невозможно надежно определить.

## Контроль качества

- Полных дубликатов: 0.
- Годы: 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026.
- Распределение `maturity_bucket`:
  - `long_term`: 348
  - `medium_term`: 262
  - `short_term`: 68
- Распределение `maturity_bucket_label`:
  - `Долгосрочные (свыше 10 лет)`: 348
  - `Среднесрочные (5-10 лет)`: 262
  - `Краткосрочные (до 5 лет)`: 68
- Распределение `demand_pressure_indicator`:
  - `moderate`: 326
  - `high`: 238
  - `not_applicable`: 114
- Распределение `yield_pressure_indicator`:
  - `normal`: 471
  - `not_applicable`: 106
  - `low`: 71
  - `high`: 30

## Выходные артефакты

- `data/processed/ofz_auctions_features_repro.csv`
- `docs/feature_engineering_repro.md`
- `logs/pipeline.log`
