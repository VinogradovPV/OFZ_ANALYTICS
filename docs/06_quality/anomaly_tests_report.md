# Отчет anomaly tests

Метка: `вторая модернизация`.

Дата формирования: `2026-06-16 10:32:03`.

## Источник

- Dataset: `data/processed/ofz_auctions_report_scope.csv`
- Строк: `163`

## Сводка

- OK: `6`
- Warnings: `8`
- Failures: `0`

## Проверки

| Проверка | Статус | Строк | Комментарий |
| --- | --- | ---: | --- |
| `zero_placement` | `ok` | 9 | Нулевое размещение найдено и не ломает demand_to_placement_ratio. |
| `drpa_rows` | `ok` | 35 | ДРПА найдены; demand-based ratios должны учитывать ограничения. |
| `failed_or_no_deal` | `ok` | 9 | Несостоявшиеся аукционы не найдены или не имеют положительного размещения. |
| `missing_yield` | `warning` | 9 | Есть строки без доходности; они должны исключаться из yield-графиков. |
| `zero_yield_suspected` | `ok` | 0 | Около-нулевые доходности не найдены. |
| `bid_to_cover_outliers` | `warning` | 1 | Найдены bid_to_cover_ratio > 5; проверить знаменатель supply_volume. |
| `demand_to_placement_outliers` | `warning` | 1 | Найдены demand_to_placement_ratio > 10; проверить нулевые/малые placement_volume. |
| `zero_supply` | `ok` | 0 | Нулевое предложение не найдено. |
| `zero_demand` | `warning` | 35 | Есть строки с нулевым/отсутствующим спросом; demand ratios должны быть пустыми или ограниченными. |
| `demand_without_placement` | `warning` | 7 | Есть спрос без размещения; вероятно несостоявшийся/ограниченный аукцион. |
| `placement_without_demand` | `warning` | 33 | Есть размещение без спроса; обычно это ДРПА или ограничение источника. |
| `missing_cutoff_price` | `warning` | 7 | У части аукционов отсутствует цена отсечения; discount analysis ограничен. |
| `missing_discount_to_nominal` | `ok` | 0 | Дисконт к номиналу доступен или рассчитывается из цены отсечения. |
| `nominal_revenue_gap_anomaly` | `warning` | 30 | Найдена аномальная разница между номиналом и выручкой > 25%. |

## Диагностические выборки

### `zero_placement`

| auction_date | report_period_label | issue_code | format | _demand | _supply | _placement | _revenue | _yield | _bid_to_cover | _demand_to_placement | _cutoff_price | _discount_to_nominal | source_file | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-02-22 | 2023-M01-M04 | 26240RMFS | Аукцион | 14390.5 | 41004.4 | 0 | 0 |  | 0.35095 |  |  |  | INTERNET_Auction_Results_rus_2023_20231231.xlsx | missing_yield\|failed_or_no_deal |
| 2023-03-22 | 2023-M01-M04 | 52005RMFS | Аукцион | 2852.78 | 343416 | 0 | 0 |  | 0.00830708 |  |  |  | INTERNET_Auction_Results_rus_2023_20231231.xlsx | missing_yield\|failed_or_no_deal |
| 2024-01-17 | 2024-M01-M04 | 52005RMFS | Аукцион | 222.232 | 145267 | 0 | 0 |  | 0.00152982 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2024-03-13 | 2024-M01-M04 | 26219RMFS | Аукцион | 13834 | 10000 | 0 | 0 |  | 1.3834 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2024-04-03 | 2024-M01-M04 | 52005RMFS | Аукцион | 10842.4 | 139615 | 0 | 0 |  | 0.077659 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2025-04-02 | 2025-M01-M04 | 26247RMFS | ДРПА |  | 15902.4 | 0 | 0 |  |  |  |  |  | INTERNET_Auction_Results_rus_2025_20251231.xlsx | missing_demand\|missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct\|demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2025-04-09 | 2025-M01-M04 | 52005RMFS | Аукцион | 3112.64 | 153339 | 0 | 0 |  | 0.020299 |  |  |  | INTERNET_Auction_Results_rus_2025_20251231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2025-04-09 | 2025-M01-M04 | 26221RMFS | ДРПА |  | 36201.4 | 0 | 0 |  |  |  |  |  | INTERNET_Auction_Results_rus_2025_20251231.xlsx | missing_demand\|missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct\|demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2026-02-04 | 2026-M01-M04 | 26251RMFS | Аукцион | 294005 | 80047.5 | 0 | 0 |  | 3.67288 |  |  |  | INTERNET_Auction_Results_rus_2026_20260507.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |

### `drpa_rows`

| auction_date | report_period_label | issue_code | format | _demand | _supply | _placement | _revenue | _yield | _bid_to_cover | _demand_to_placement | _cutoff_price | _discount_to_nominal | source_file | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-01-31 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 35002.7 | 11649.5 | 10195.9 | 12.2 |  |  | 85.9917 | 14.0083 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-02-07 | 2024-M01-M04 | 26244RMFS | ДРПА |  | 16872.6 | 753.883 | 750.889 | 12.23 |  |  | 96.3358 | 3.6642 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-02-14 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 13466.1 | 1045 | 904.533 | 12.44 |  |  | 84.6522 | 15.3478 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-02-21 | 2024-M01-M04 | 26244RMFS | ДРПА |  | 28402.2 | 21699.8 | 21343.7 | 12.55 |  |  | 94.66 | 5.34 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-02-28 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 27296.7 | 4628.08 | 3949.84 | 12.73 |  |  | 83.0631 | 16.9369 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-03-06 | 2024-M01-M04 | 26244RMFS | ДРПА |  | 18125.9 | 510 | 494.305 | 12.92 |  |  | 92.7915 | 7.2085 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-03-13 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 28801 | 500 | 417.579 | 13.15 |  |  | 80.8577 | 19.1423 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-03-27 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 43460.9 | 23273.8 | 19054.8 | 13.55 |  |  | 78.8383 | 21.1617 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-04-03 | 2024-M01-M04 | 26242RMFS | ДРПА |  | 39013.5 | 33913.2 | 29083.5 | 13.34 |  |  | 85.0438 | 14.9562 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-04-10 | 2024-M01-M04 | 26244RMFS | ДРПА |  | 23961.2 | 17475.3 | 15610.4 | 13.74 |  |  | 88.8665 | 11.1335 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |

### `failed_or_no_deal`

| auction_date | report_period_label | issue_code | format | _demand | _supply | _placement | _revenue | _yield | _bid_to_cover | _demand_to_placement | _cutoff_price | _discount_to_nominal | source_file | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-02-22 | 2023-M01-M04 | 26240RMFS | Аукцион | 14390.5 | 41004.4 | 0 | 0 |  | 0.35095 |  |  |  | INTERNET_Auction_Results_rus_2023_20231231.xlsx | missing_yield\|failed_or_no_deal |
| 2023-03-22 | 2023-M01-M04 | 52005RMFS | Аукцион | 2852.78 | 343416 | 0 | 0 |  | 0.00830708 |  |  |  | INTERNET_Auction_Results_rus_2023_20231231.xlsx | missing_yield\|failed_or_no_deal |
| 2024-01-17 | 2024-M01-M04 | 52005RMFS | Аукцион | 222.232 | 145267 | 0 | 0 |  | 0.00152982 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2024-03-13 | 2024-M01-M04 | 26219RMFS | Аукцион | 13834 | 10000 | 0 | 0 |  | 1.3834 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2024-04-03 | 2024-M01-M04 | 52005RMFS | Аукцион | 10842.4 | 139615 | 0 | 0 |  | 0.077659 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2025-04-02 | 2025-M01-M04 | 26247RMFS | ДРПА |  | 15902.4 | 0 | 0 |  |  |  |  |  | INTERNET_Auction_Results_rus_2025_20251231.xlsx | missing_demand\|missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct\|demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2025-04-09 | 2025-M01-M04 | 52005RMFS | Аукцион | 3112.64 | 153339 | 0 | 0 |  | 0.020299 |  |  |  | INTERNET_Auction_Results_rus_2025_20251231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2025-04-09 | 2025-M01-M04 | 26221RMFS | ДРПА |  | 36201.4 | 0 | 0 |  |  |  |  |  | INTERNET_Auction_Results_rus_2025_20251231.xlsx | missing_demand\|missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct\|demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2026-02-04 | 2026-M01-M04 | 26251RMFS | Аукцион | 294005 | 80047.5 | 0 | 0 |  | 3.67288 |  |  |  | INTERNET_Auction_Results_rus_2026_20260507.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |

### `missing_yield`

| auction_date | report_period_label | issue_code | format | _demand | _supply | _placement | _revenue | _yield | _bid_to_cover | _demand_to_placement | _cutoff_price | _discount_to_nominal | source_file | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-02-22 | 2023-M01-M04 | 26240RMFS | Аукцион | 14390.5 | 41004.4 | 0 | 0 |  | 0.35095 |  |  |  | INTERNET_Auction_Results_rus_2023_20231231.xlsx | missing_yield\|failed_or_no_deal |
| 2023-03-22 | 2023-M01-M04 | 52005RMFS | Аукцион | 2852.78 | 343416 | 0 | 0 |  | 0.00830708 |  |  |  | INTERNET_Auction_Results_rus_2023_20231231.xlsx | missing_yield\|failed_or_no_deal |
| 2024-01-17 | 2024-M01-M04 | 52005RMFS | Аукцион | 222.232 | 145267 | 0 | 0 |  | 0.00152982 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2024-03-13 | 2024-M01-M04 | 26219RMFS | Аукцион | 13834 | 10000 | 0 | 0 |  | 1.3834 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2024-04-03 | 2024-M01-M04 | 52005RMFS | Аукцион | 10842.4 | 139615 | 0 | 0 |  | 0.077659 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2025-04-02 | 2025-M01-M04 | 26247RMFS | ДРПА |  | 15902.4 | 0 | 0 |  |  |  |  |  | INTERNET_Auction_Results_rus_2025_20251231.xlsx | missing_demand\|missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct\|demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2025-04-09 | 2025-M01-M04 | 52005RMFS | Аукцион | 3112.64 | 153339 | 0 | 0 |  | 0.020299 |  |  |  | INTERNET_Auction_Results_rus_2025_20251231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2025-04-09 | 2025-M01-M04 | 26221RMFS | ДРПА |  | 36201.4 | 0 | 0 |  |  |  |  |  | INTERNET_Auction_Results_rus_2025_20251231.xlsx | missing_demand\|missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct\|demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2026-02-04 | 2026-M01-M04 | 26251RMFS | Аукцион | 294005 | 80047.5 | 0 | 0 |  | 3.67288 |  |  |  | INTERNET_Auction_Results_rus_2026_20260507.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |

### `bid_to_cover_outliers`

| auction_date | report_period_label | issue_code | format | _demand | _supply | _placement | _revenue | _yield | _bid_to_cover | _demand_to_placement | _cutoff_price | _discount_to_nominal | source_file | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-03-13 | 2024-M01-M04 | 26243RMFS | Аукцион | 86075.1 | 3 | 48969.1 | 40896.9 | 13.15 | 28691.7 | 1.75774 | 80.8495 | 19.1505 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | ok |

### `demand_to_placement_outliers`

| auction_date | report_period_label | issue_code | format | _demand | _supply | _placement | _revenue | _yield | _bid_to_cover | _demand_to_placement | _cutoff_price | _discount_to_nominal | source_file | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-01-25 | 2023-M01-M04 | 26242RMFS | Аукцион | 65425.6 | 500000 | 6495.81 | 6289.18 | 9.9 | 0.130851 | 10.072 | 96.6411 | 3.3589 | INTERNET_Auction_Results_rus_2023_20231231.xlsx | ok |

### `zero_demand`

| auction_date | report_period_label | issue_code | format | _demand | _supply | _placement | _revenue | _yield | _bid_to_cover | _demand_to_placement | _cutoff_price | _discount_to_nominal | source_file | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-01-31 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 35002.7 | 11649.5 | 10195.9 | 12.2 |  |  | 85.9917 | 14.0083 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-02-07 | 2024-M01-M04 | 26244RMFS | ДРПА |  | 16872.6 | 753.883 | 750.889 | 12.23 |  |  | 96.3358 | 3.6642 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-02-14 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 13466.1 | 1045 | 904.533 | 12.44 |  |  | 84.6522 | 15.3478 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-02-21 | 2024-M01-M04 | 26244RMFS | ДРПА |  | 28402.2 | 21699.8 | 21343.7 | 12.55 |  |  | 94.66 | 5.34 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-02-28 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 27296.7 | 4628.08 | 3949.84 | 12.73 |  |  | 83.0631 | 16.9369 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-03-06 | 2024-M01-M04 | 26244RMFS | ДРПА |  | 18125.9 | 510 | 494.305 | 12.92 |  |  | 92.7915 | 7.2085 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-03-13 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 28801 | 500 | 417.579 | 13.15 |  |  | 80.8577 | 19.1423 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-03-27 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 43460.9 | 23273.8 | 19054.8 | 13.55 |  |  | 78.8383 | 21.1617 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-04-03 | 2024-M01-M04 | 26242RMFS | ДРПА |  | 39013.5 | 33913.2 | 29083.5 | 13.34 |  |  | 85.0438 | 14.9562 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-04-10 | 2024-M01-M04 | 26244RMFS | ДРПА |  | 23961.2 | 17475.3 | 15610.4 | 13.74 |  |  | 88.8665 | 11.1335 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |

### `demand_without_placement`

| auction_date | report_period_label | issue_code | format | _demand | _supply | _placement | _revenue | _yield | _bid_to_cover | _demand_to_placement | _cutoff_price | _discount_to_nominal | source_file | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-02-22 | 2023-M01-M04 | 26240RMFS | Аукцион | 14390.5 | 41004.4 | 0 | 0 |  | 0.35095 |  |  |  | INTERNET_Auction_Results_rus_2023_20231231.xlsx | missing_yield\|failed_or_no_deal |
| 2023-03-22 | 2023-M01-M04 | 52005RMFS | Аукцион | 2852.78 | 343416 | 0 | 0 |  | 0.00830708 |  |  |  | INTERNET_Auction_Results_rus_2023_20231231.xlsx | missing_yield\|failed_or_no_deal |
| 2024-01-17 | 2024-M01-M04 | 52005RMFS | Аукцион | 222.232 | 145267 | 0 | 0 |  | 0.00152982 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2024-03-13 | 2024-M01-M04 | 26219RMFS | Аукцион | 13834 | 10000 | 0 | 0 |  | 1.3834 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2024-04-03 | 2024-M01-M04 | 52005RMFS | Аукцион | 10842.4 | 139615 | 0 | 0 |  | 0.077659 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2025-04-09 | 2025-M01-M04 | 52005RMFS | Аукцион | 3112.64 | 153339 | 0 | 0 |  | 0.020299 |  |  |  | INTERNET_Auction_Results_rus_2025_20251231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2026-02-04 | 2026-M01-M04 | 26251RMFS | Аукцион | 294005 | 80047.5 | 0 | 0 |  | 3.67288 |  |  |  | INTERNET_Auction_Results_rus_2026_20260507.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |

### `placement_without_demand`

| auction_date | report_period_label | issue_code | format | _demand | _supply | _placement | _revenue | _yield | _bid_to_cover | _demand_to_placement | _cutoff_price | _discount_to_nominal | source_file | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-01-31 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 35002.7 | 11649.5 | 10195.9 | 12.2 |  |  | 85.9917 | 14.0083 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-02-07 | 2024-M01-M04 | 26244RMFS | ДРПА |  | 16872.6 | 753.883 | 750.889 | 12.23 |  |  | 96.3358 | 3.6642 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-02-14 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 13466.1 | 1045 | 904.533 | 12.44 |  |  | 84.6522 | 15.3478 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-02-21 | 2024-M01-M04 | 26244RMFS | ДРПА |  | 28402.2 | 21699.8 | 21343.7 | 12.55 |  |  | 94.66 | 5.34 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-02-28 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 27296.7 | 4628.08 | 3949.84 | 12.73 |  |  | 83.0631 | 16.9369 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-03-06 | 2024-M01-M04 | 26244RMFS | ДРПА |  | 18125.9 | 510 | 494.305 | 12.92 |  |  | 92.7915 | 7.2085 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-03-13 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 28801 | 500 | 417.579 | 13.15 |  |  | 80.8577 | 19.1423 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-03-27 | 2024-M01-M04 | 26243RMFS | ДРПА |  | 43460.9 | 23273.8 | 19054.8 | 13.55 |  |  | 78.8383 | 21.1617 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-04-03 | 2024-M01-M04 | 26242RMFS | ДРПА |  | 39013.5 | 33913.2 | 29083.5 | 13.34 |  |  | 85.0438 | 14.9562 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2024-04-10 | 2024-M01-M04 | 26244RMFS | ДРПА |  | 23961.2 | 17475.3 | 15610.4 | 13.74 |  |  | 88.8665 | 11.1335 | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |

### `missing_cutoff_price`

| auction_date | report_period_label | issue_code | format | _demand | _supply | _placement | _revenue | _yield | _bid_to_cover | _demand_to_placement | _cutoff_price | _discount_to_nominal | source_file | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-02-22 | 2023-M01-M04 | 26240RMFS | Аукцион | 14390.5 | 41004.4 | 0 | 0 |  | 0.35095 |  |  |  | INTERNET_Auction_Results_rus_2023_20231231.xlsx | missing_yield\|failed_or_no_deal |
| 2023-03-22 | 2023-M01-M04 | 52005RMFS | Аукцион | 2852.78 | 343416 | 0 | 0 |  | 0.00830708 |  |  |  | INTERNET_Auction_Results_rus_2023_20231231.xlsx | missing_yield\|failed_or_no_deal |
| 2024-01-17 | 2024-M01-M04 | 52005RMFS | Аукцион | 222.232 | 145267 | 0 | 0 |  | 0.00152982 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2024-03-13 | 2024-M01-M04 | 26219RMFS | Аукцион | 13834 | 10000 | 0 | 0 |  | 1.3834 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2024-04-03 | 2024-M01-M04 | 52005RMFS | Аукцион | 10842.4 | 139615 | 0 | 0 |  | 0.077659 |  |  |  | INTERNET_Auction_Results_rus_2024_20241231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2025-04-09 | 2025-M01-M04 | 52005RMFS | Аукцион | 3112.64 | 153339 | 0 | 0 |  | 0.020299 |  |  |  | INTERNET_Auction_Results_rus_2025_20251231.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |
| 2026-02-04 | 2026-M01-M04 | 26251RMFS | Аукцион | 294005 | 80047.5 | 0 | 0 |  | 3.67288 |  |  |  | INTERNET_Auction_Results_rus_2026_20260507.xlsx | missing_yield\|failed_or_no_deal\|source_markers:cutoff_price_pct\|weighted_avg_price_pct\|cutoff_yield_pct\|weighted_avg_yield_pct |

### `nominal_revenue_gap_anomaly`

| auction_date | report_period_label | issue_code | format | _demand | _supply | _placement | _revenue | _yield | _bid_to_cover | _demand_to_placement | _cutoff_price | _discount_to_nominal | source_file | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-02-15 | 2023-M01-M04 | 26238RMFS | Аукцион | 84768.6 | 262228 | 41238.9 | 30710.1 | 10.69 | 0.323262 | 2.05555 | 73.023 | 26.977 | INTERNET_Auction_Results_rus_2023_20231231.xlsx | ok |
| 2023-03-01 | 2023-M01-M04 | 26238RMFS | Аукцион | 43094.1 | 220990 | 30406.4 | 22602.2 | 10.76 | 0.195005 | 1.41727 | 72.56 | 27.44 | INTERNET_Auction_Results_rus_2023_20231231.xlsx | ok |
| 2023-03-15 | 2023-M01-M04 | 26238RMFS | Аукцион | 48252.3 | 190583 | 35873.3 | 26791.7 | 10.76 | 0.253183 | 1.34508 | 72.639 | 27.361 | INTERNET_Auction_Results_rus_2023_20231231.xlsx | ok |
| 2023-03-29 | 2023-M01-M04 | 26238RMFS | Аукцион | 44777.7 | 154710 | 28877.4 | 21636.6 | 10.76 | 0.28943 | 1.55062 | 72.6004 | 27.3996 | INTERNET_Auction_Results_rus_2023_20231231.xlsx | ok |
| 2025-01-29 | 2025-M01-M04 | 26235RMFS | Аукцион | 36286.8 | 50000 | 17606 | 11128.4 | 16.81 | 0.725736 | 2.06105 | 61.0084 | 38.9916 | INTERNET_Auction_Results_rus_2025_20251231.xlsx | ok |
| 2025-01-29 | 2025-M01-M04 | 26238RMFS | Аукцион | 73562.7 | 50000 | 50000 | 25947.5 | 16.02 | 1.47125 | 1.47125 | 50.61 | 49.39 | INTERNET_Auction_Results_rus_2025_20251231.xlsx | ok |
| 2025-01-29 | 2025-M01-M04 | 26235RMFS | ДРПА |  | 12144.9 | 5594.75 | 3536.33 | 16.81 |  |  | 61.042 | 38.958 | INTERNET_Auction_Results_rus_2025_20251231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2025-02-05 | 2025-M01-M04 | 26228RMFS | Аукцион | 29661.4 | 50000 | 12677.1 | 9093.86 | 17.41 | 0.593227 | 2.33977 | 69.35 | 30.65 | INTERNET_Auction_Results_rus_2025_20251231.xlsx | ok |
| 2025-02-05 | 2025-M01-M04 | 26228RMFS | ДРПА |  | 14205.2 | 7205.15 | 5168.59 | 17.41 |  |  | 69.3657 | 30.6343 | INTERNET_Auction_Results_rus_2025_20251231.xlsx | missing_demand\|source_markers:demand_amount_mln_rub\|demand_satisfaction_ratio |
| 2025-02-12 | 2025-M01-M04 | 26233RMFS | Аукцион | 153915 | 50000 | 50000 | 25045.5 | 16.89 | 3.07829 | 3.0783 | 49.82 | 50.18 | INTERNET_Auction_Results_rus_2025_20251231.xlsx | ok |

## Интерпретация

- `ok` означает, что критичного нарушения по проверке не выявлено.
- `warning` означает наличие наблюдений, требующих методологической или ручной проверки.
- `fail` означает нарушение расчетного контракта, которое может искажать downstream-таблицы или графики.

## Ограничения

- Проверка не изменяет `data/raw/` и processed datasets.
- Revenue checks ограничены, если в данных нет надежной колонки выручки.
- Наличие warning не всегда означает ошибку данных; часть предупреждений фиксирует ожидаемые ограничения источника.
