# Revenue analytics: выручка от реализации ОФЗ

Дата формирования: `2026-06-22 15:11:06`.

## Параметры

- `report_date`: `2026-05-01`
- `period_type`: `month`
- `aggregation_mode`: `cumulative`
- `retrospective_years`: `4`

## Источник

- Dataset: `data/processed/ofz_auctions_report_scope.csv`
- Колонка выручки: `proceeds_mln_rub`
- Строк в расчетном scope: `163`

## Outputs

- XLSX workbook: `outputs/reports/analytical_tables/revenue_summary_month_cumulative_2026-05-01_retrospective_4.xlsx`
- CSV: `outputs/exports/analytical_csv/revenue_summary_month_cumulative_2026-05-01_retrospective_4.csv`
- CSV: `outputs/exports/analytical_csv/revenue_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.csv`
- CSV: `outputs/exports/analytical_csv/revenue_by_maturity_month_cumulative_2026-05-01_retrospective_4.csv`
- CSV: `outputs/exports/analytical_csv/revenue_by_format_month_cumulative_2026-05-01_retrospective_4.csv`
- CSV: `outputs/exports/analytical_csv/revenue_monthly_month_cumulative_2026-05-01_retrospective_4.csv`

## Срезы

- `summary`: 5 строк.
- `by_ofz_type`: 9 строк.
- `by_maturity`: 13 строк.
- `by_format`: 8 строк.
- `monthly`: 18 строк.

## Основная таблица `revenue_summary`

| report_period_label | report_period_start | report_period_end | report_year | aggregation_mode | placement_volume | placement_volume_bln | revenue_volume | revenue_volume_bln | nominal_revenue_gap | nominal_revenue_gap_bln | revenue_to_nominal_ratio | nominal_discount_ratio | auction_count | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022-M01-M04 | 2022-01-01 | 2022-04-30 | 2022 | cumulative | 128079.33 | 128.0793 | 114898.8907 | 114.8989 | 13180.4393 | 13.1804 | 0.8971 | 0.1029 | 5 | ok |
| 2023-M01-M04 | 2023-01-01 | 2023-04-30 | 2023 | cumulative | 965462.1515 | 965.4622 | 857660.0763 | 857.6601 | 107802.0752 | 107.8021 | 0.8883 | 0.1117 | 34 | ok; zero_or_negative_placement_present |
| 2024-M01-M04 | 2024-01-01 | 2024-04-30 | 2024 | cumulative | 1147609.6578 | 1147.6097 | 1033852.2148 | 1033.8522 | 113757.443 | 113.7574 | 0.9009 | 0.0991 | 37 | ok; zero_or_negative_placement_present |
| 2025-M01-M04 | 2025-01-01 | 2025-04-30 | 2025 | cumulative | 1745442.217 | 1745.4422 | 1373723.6101 | 1373.7236 | 371718.6069 | 371.7186 | 0.787 | 0.213 | 45 | ok; zero_or_negative_placement_present |
| 2026-M01-M04 | 2026-01-01 | 2026-04-30 | 2026 | cumulative | 2477715.934 | 2477.7159 | 2210455.1374 | 2210.4551 | 267260.7966 | 267.2608 | 0.8921 | 0.1079 | 42 | ok; zero_or_negative_placement_present |

## Методика

- `placement_volume` — сумма объема размещения по номиналу, млн рублей.
- `revenue_volume` — сумма выручки от реализации, млн рублей.
- `nominal_revenue_gap = placement_volume - revenue_volume`.
- `revenue_to_nominal_ratio = revenue_volume / placement_volume`.
- `nominal_discount_ratio = nominal_revenue_gap / placement_volume`.
- Значения `_bln` являются отображением в млрд рублей и не изменяют исходные млн рублей.

## Ограничения

- Выручка от реализации нормализована из колонки `proceeds_mln_rub`.
