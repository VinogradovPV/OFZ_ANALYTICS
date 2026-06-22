# Revenue charts: графики выручки от реализации ОФЗ

Дата формирования: `2026-06-22 15:11:08`.

## Параметры

- `report_date`: `2026-05-01`
- `period_type`: `month`
- `aggregation_mode`: `cumulative`
- `retrospective_years`: `4`

## Созданные графики

- `revenue_vs_nominal_by_period`: `outputs/charts/revenue/period/revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.html`
  - chart data: `outputs/exports/chart_data/revenue/revenue_vs_nominal_by_period_month_cumulative_2026-05-01_retrospective_4.csv`
- `nominal_revenue_gap_by_period`: `outputs/charts/revenue/gap/nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.html`
  - chart data: `outputs/exports/chart_data/revenue/nominal_revenue_gap_by_period_month_cumulative_2026-05-01_retrospective_4.csv`
- `revenue_to_nominal_ratio`: `outputs/charts/revenue/ratio/revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.html`
  - chart data: `outputs/exports/chart_data/revenue/revenue_to_nominal_ratio_month_cumulative_2026-05-01_retrospective_4.csv`
- `monthly_revenue_vs_nominal`: `outputs/charts/revenue/monthly/monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.html`
  - chart data: `outputs/exports/chart_data/revenue/monthly_revenue_vs_nominal_month_cumulative_2026-05-01_retrospective_4.csv`
- `monthly_nominal_revenue_gap`: `outputs/charts/revenue/monthly/monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html`
  - chart data: `outputs/exports/chart_data/revenue/monthly_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.csv`
- `revenue_gap_by_ofz_type`: `outputs/charts/revenue/breakdowns/revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html`
  - chart data: `outputs/exports/chart_data/revenue/revenue_gap_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.csv`
- `revenue_gap_by_maturity`: `outputs/charts/revenue/breakdowns/revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.html`
  - chart data: `outputs/exports/chart_data/revenue/revenue_gap_by_maturity_month_cumulative_2026-05-01_retrospective_4.csv`
- `format_nominal_revenue_gap`: `outputs/charts/revenue/gap/format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html`
  - chart data: `outputs/exports/chart_data/revenue/format_nominal_revenue_gap_month_cumulative_2026-05-01_retrospective_4.csv`
- `discount_vs_revenue_gap`: `outputs/charts/scatter/discount_revenue_gap/discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.html`
  - chart data: `outputs/exports/chart_data/revenue/discount_vs_revenue_gap_month_cumulative_2026-05-01_retrospective_4.csv`

## Методика

- Все суммы на графиках отображаются в млрд рублей.
- `placement_volume_bln = placement_volume / 1000`.
- `revenue_volume_bln = revenue_volume / 1000`.
- `nominal_revenue_gap_bln = (placement_volume - revenue_volume) / 1000`.
- `discount_vs_revenue_gap` использует `nominal_discount_ratio`, то есть дисконт выручки к номиналу.

## Ограничения

- Существенные ограничения не выявлены.
