# Стратегия помесячных визуализаций

Дата формирования: `2026-06-22 15:11:10`.

## Параметры

- `report_date`: `2026-05-01`
- `retrospective_years`: `4`
- `period_type`: `month`
- `aggregation_mode`: `cumulative`

## Назначение

Помесячные графики объясняют, из каких месяцев складывается накопленный итог отчетного периода. Объем размещения трактуется как объем размещения по номиналу: исходные данные считаются в млн руб., а на графиках отображаются в млрд руб.

## Графики

| График | Тип | Что показывает | Управленческий смысл |
|---|---|---|---|
| Помесячный объем размещения по номиналу | grouped bar | `total_placement_volume` по месяцам и годам, млрд руб. | Показывает, какие месяцы дали основной вклад в размещение. |
| Накопленный объем размещения по номиналу | line | `cumulative_placement_volume`, млрд руб. | Сравнивает траекторию накопления размещений между годами. |
| Помесячный спрос и предложение | grouped/facet bar | `total_demand` и `total_supply` | Показывает баланс рыночного спроса и объема предложения по месяцам. |
| Помесячный bid-to-cover | line | `bid_to_cover_ratio = total_demand / total_supply` | Показывает месяцы с дефицитом или избытком спроса относительно предложения. |
| Помесячная средневзвешенная доходность ОФЗ-ПД | line | `yield_weighted_avg`, `yield_scope=ofz_pd_only` | Показывает изменение стоимости фиксированных заимствований без ОФЗ-ПК и ОФЗ-ИН. |
| Структура объема размещения по номиналу по форматам | stacked bar | аукционы и ДРПА, млрд руб. | Разделяет рыночные размещения и ДРПА. |
| Структура объема размещения по номиналу по срокам | stacked bar | кратко-, средне- и долгосрочные размещения, млрд руб. | Показывает сдвиги в сроковой структуре размещений. |
| Heatmap месяц × год | heatmap | `total_placement_volume`, млрд руб. | Быстро выделяет месяцы и годы с максимальной активностью. |

## Созданные файлы

- HTML: `outputs/charts/monthly/placement/monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html`
- CSV-основа: `outputs/exports/chart_data/monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.csv`
- HTML: `outputs/charts/monthly/placement/monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html`
- CSV-основа: `outputs/exports/chart_data/monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.csv`
- HTML: `outputs/charts/monthly/demand_supply/monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html`
- CSV-основа: `outputs/exports/chart_data/monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.csv`
- HTML: `outputs/charts/monthly/bid_cover/monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html`
- CSV-основа: `outputs/exports/chart_data/monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.csv`
- HTML: `outputs/charts/monthly/yield/monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.html`
- CSV-основа: `outputs/exports/chart_data/monthly_weighted_avg_yield_month_cumulative_2026-05-01_retrospective_4.csv`
- HTML: `outputs/charts/monthly/structure/monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html`
- CSV-основа: `outputs/exports/chart_data/monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.csv`
- HTML: `outputs/charts/monthly/structure/monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html`
- CSV-основа: `outputs/exports/chart_data/monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.csv`
- HTML: `outputs/charts/monthly/heatmap/monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.html`
- CSV-основа: `outputs/exports/chart_data/monthly_heatmap_placement_month_cumulative_2026-05-01_retrospective_4.csv`
- HTML: `outputs/charts/monthly/heatmap/monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.html`
- CSV-основа: `outputs/exports/chart_data/monthly/monthly_heatmap_revenue_month_cumulative_2026-05-01_retrospective_4.csv`

## Ограничения

- Heatmap выручки использует fallback-источник `ofz_auctions_report_scope.proceeds_mln_rub`.

## Вторая модернизация: подписи monthly bid-cover

- График `monthly_bid_to_cover` называется `Помесячное покрытие предложения спросом`.
- Ось Y подписана как `Спрос / предложение`.
- Горизонтальная линия `y = 1` подписана `Спрос = предложение`.
- Подписи выводятся выборочно: последняя точка каждого года, минимум, максимум, точки около порога 1 и точки отчетного года.
- Максимальное число подписей на графике: `30`.
- Полная детализация доступна в hover и CSV-основе графика.
- CSV-основа содержит `label_display`, `label_reason`, `threshold_distance`, `is_threshold_crossing`.
