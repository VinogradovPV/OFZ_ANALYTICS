# Dashboard exports report

Дата формирования: `2026-06-16 11:32:33`.

## Параметры

- `report_date`: `2026-05-01`
- `period_type`: `month`
- `aggregation_mode`: `cumulative`
- `retrospective_years`: `4`
- Периоды: `2022-M01-M04, 2023-M01-M04, 2024-M01-M04, 2025-M01-M04, 2026-M01-M04`
- Целевой период: `2026-M01-M04`
- Источник: `data/processed/ofz_auctions_report_scope.csv`
- Строк в source scope после фильтрации: `163`

## Структура сохранения

- Dashboard-ready файлы сохраняются только в `outputs/dashboards/`.
- Monthly dashboard exports сохраняются в `outputs/dashboards/monthly/`.
- Semantic layer, если он формируется как dashboard export, сохраняется в `outputs/dashboards/semantic_layer/`.
- Dashboard exports не переносятся в `outputs/reports/` и не смешиваются с `outputs/exports/chart_data/`.

## Созданные exports

| Dataset | Файл | Строк | Назначение |
|---|---|---:|---|
| `auction_level` | `outputs/dashboards/monthly/dashboard_auction_level_month_cumulative_2026-05-01_retrospective_4.csv` | 163 | Строки уровня отдельного размещения / аукциона. |
| `period_summary` | `outputs/dashboards/monthly/dashboard_period_summary_month_cumulative_2026-05-01_retrospective_4.csv` | 5 | Периодная сводка спроса, предложения, размещения и доходности. |
| `kpi_summary` | `outputs/dashboards/monthly/dashboard_kpi_summary_month_cumulative_2026-05-01_retrospective_4.csv` | 75 | KPI в long-format для карточек dashboard. |
| `maturity_structure` | `outputs/dashboards/monthly/dashboard_maturity_structure_month_cumulative_2026-05-01_retrospective_4.csv` | 13 | Структура размещения по срокам обращения. |
| `yield_distribution` | `outputs/dashboards/monthly/dashboard_yield_distribution_month_cumulative_2026-05-01_retrospective_4.csv` | 8 | Распределение доходности по периодам и видам ОФЗ. |
| `demand_supply` | `outputs/dashboards/monthly/dashboard_demand_supply_month_cumulative_2026-05-01_retrospective_4.csv` | 8 | Спрос и предложение по периодам и форматам. |
| `metadata` | `outputs/dashboards/monthly/dashboard_metadata_month_cumulative_2026-05-01_retrospective_4.json` | 1 | JSON metadata по dashboard exports. |
| `data_dictionary` | `outputs/dashboards/monthly/dashboard_data_dictionary_month_cumulative_2026-05-01_retrospective_4.csv` | 16 | Словарь данных dashboard exports. |
| `semantic_layer_fields` | `outputs/dashboards/semantic_layer/dashboard_semantic_layer_fields_month_cumulative_2026-05-01_retrospective_4.csv` | 53 | Каталог полей semantic layer: русские названия, technical names, units и правила расчета. |
| `semantic_layer_metrics` | `outputs/dashboards/semantic_layer/dashboard_semantic_layer_metrics_month_cumulative_2026-05-01_retrospective_4.csv` | 10 | Каталог управленческих метрик semantic layer с формулами и ограничениями. |
| `semantic_layer_dimensions` | `outputs/dashboards/semantic_layer/dashboard_semantic_layer_dimensions_month_cumulative_2026-05-01_retrospective_4.csv` | 8 | Каталог измерений, рекомендуемых фильтров и default sorting для dashboard. |
| `semantic_layer_relationships` | `outputs/dashboards/semantic_layer/dashboard_semantic_layer_relationships_month_cumulative_2026-05-01_retrospective_4.csv` | 6 | Контракт связей между dashboard-ready таблицами. |
| `semantic_layer_manifest` | `outputs/dashboards/semantic_layer/dashboard_semantic_layer_manifest_month_cumulative_2026-05-01_retrospective_4.json` | 1 | JSON manifest semantic layer с параметрами отчета и списком semantic exports. |
| `monthly_metrics` | `outputs/dashboards/monthly/dashboard_monthly_metrics_month_cumulative_2026-05-01_retrospective_4.csv` | 20 | BI-ready помесячные показатели для объяснения накопленного итога. |
| `monthly_data_dictionary` | `outputs/dashboards/monthly/dashboard_monthly_data_dictionary_month_cumulative_2026-05-01_retrospective_4.csv` | 37 | Словарь данных помесячного dashboard layer. |

## Ключевые KPI

- Совокупный спрос: `3 944 592.0` млн руб.
- Совокупное предложение: `12 981 710.8` млн руб.
- Объем размещения: `2 477 715.9` млн руб.
- Bid-to-cover: `0.304`.
- Спрос / размещение: `1.592`.
- Средневзвешенная доходность: `14.69`%.

## Использование в BI/dashboard

- `dashboard_auction_level` использовать как detail fact table.
- `dashboard_period_summary` использовать для временных KPI и trend charts.
- `dashboard_kpi_summary` использовать для KPI cards в long-format.
- `dashboard_maturity_structure` использовать для структуры сроков.
- `dashboard_yield_distribution` использовать для boxplot и yield analytics.
- `dashboard_demand_supply` использовать для demand/supply views с учетом формата.
- `dashboard_monthly_metrics` использовать для помесячных dashboard views и объяснения накопленного итога.
- `dashboard_monthly_data_dictionary` использовать как словарь полей помесячного слоя.
- `dashboard_metadata` использовать для отображения параметров отчета и методологии.
- `dashboard_data_dictionary` использовать как технический слой описания полей.
