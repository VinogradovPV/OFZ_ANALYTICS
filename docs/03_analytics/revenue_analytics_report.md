# Revenue analytics: выручка от реализации ОФЗ

Дата формирования: `2026-06-04 19:08:38`.

## Параметры

- `report_date`: `2026-01-01`
- `period_type`: `year`
- `aggregation_mode`: `cumulative`
- `retrospective_years`: `4`

## Источник

- Dataset: `data/processed/ofz_auctions_report_scope.csv`
- Колонка выручки: `proceeds_mln_rub`
- Строк в расчетном scope: `461`

## Outputs

- XLSX workbook: `outputs/reports/analytical_tables/revenue_summary_year_cumulative_2026-01-01_retrospective_4.xlsx`
- CSV: `outputs/exports/analytical_csv/revenue_summary_year_cumulative_2026-01-01_retrospective_4.csv`
- CSV: `outputs/exports/analytical_csv/revenue_by_ofz_type_year_cumulative_2026-01-01_retrospective_4.csv`
- CSV: `outputs/exports/analytical_csv/revenue_by_maturity_year_cumulative_2026-01-01_retrospective_4.csv`
- CSV: `outputs/exports/analytical_csv/revenue_by_format_year_cumulative_2026-01-01_retrospective_4.csv`
- CSV: `outputs/exports/analytical_csv/revenue_monthly_year_cumulative_2026-01-01_retrospective_4.csv`

## Срезы

- `summary`: 5 строк.
- `by_ofz_type`: 14 строк.
- `by_maturity`: 13 строк.
- `by_format`: 7 строк.
- `monthly`: 54 строк.

## Основная таблица `revenue_summary`

| report_period_label | report_period_start | report_period_end | report_year | aggregation_mode | placement_volume | placement_volume_bln | revenue_volume | revenue_volume_bln | nominal_revenue_gap | nominal_revenue_gap_bln | revenue_to_nominal_ratio | nominal_discount_ratio | auction_count | data_quality_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021 | 2021-01-01 | 2021-12-31 | 2021 | cumulative | 2636364.9247 | 2636.3649 | 2528760.4187 | 2528.7604 | 107604.506 | 107.6045 | 0.9592 | 0.0408 | 83 | revenue_partial; zero_or_negative_placement_present |
| 2022 | 2022-01-01 | 2022-12-31 | 2022 | cumulative | 3281258.8937 | 3281.2589 | 3130555.8953 | 3130.5559 | 150702.9984 | 150.703 | 0.9541 | 0.0459 | 37 | ok; zero_or_negative_placement_present |
| 2023 | 2023-01-01 | 2023-12-31 | 2023 | cumulative | 2845599.7653 | 2845.5998 | 2624741.9076 | 2624.7419 | 220857.8576 | 220.8579 | 0.9224 | 0.0776 | 95 | ok; zero_or_negative_placement_present |
| 2024 | 2024-01-01 | 2024-12-31 | 2024 | cumulative | 4376614.1568 | 4376.6142 | 4007481.0881 | 4007.4811 | 369133.0688 | 369.1331 | 0.9157 | 0.0843 | 104 | ok; zero_or_negative_placement_present |
| 2025 | 2025-01-01 | 2025-12-31 | 2025 | cumulative | 8047086.647 | 8047.0866 | 6983192.786 | 6983.1928 | 1063893.861 | 1063.8939 | 0.8678 | 0.1322 | 142 | ok; zero_or_negative_placement_present |

## Методика

- `placement_volume` — сумма объема размещения по номиналу, млн рублей.
- `revenue_volume` — сумма выручки от реализации, млн рублей.
- `nominal_revenue_gap = placement_volume - revenue_volume`.
- `revenue_to_nominal_ratio = revenue_volume / placement_volume`.
- `nominal_discount_ratio = nominal_revenue_gap / placement_volume`.
- Значения `_bln` являются отображением в млрд рублей и не изменяют исходные млн рублей.

## Ограничения

- Выручка от реализации нормализована из колонки `proceeds_mln_rub`.
