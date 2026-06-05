# Dashboard exports report

Дата формирования: `2026-06-04 19:08:42`.

## Параметры

- `report_date`: `2026-01-01`
- `period_type`: `year`
- `aggregation_mode`: `cumulative`
- `retrospective_years`: `4`
- Периоды: `2021, 2022, 2023, 2024, 2025`
- Целевой период: `2025`
- Источник: `data/processed/ofz_auctions_report_scope.csv`
- Строк в source scope после фильтрации: `461`

## Структура сохранения

- Dashboard-ready файлы сохраняются только в `outputs/dashboards/`.
- Monthly dashboard exports сохраняются в `outputs/dashboards/monthly/`.
- Semantic layer, если он формируется как dashboard export, сохраняется в `outputs/dashboards/semantic_layer/`.
- Dashboard exports не переносятся в `outputs/reports/` и не смешиваются с `outputs/exports/chart_data/`.

## Созданные exports

| Dataset | Файл | Строк | Назначение |
|---|---|---:|---|
| `auction_level` | `outputs/dashboards/dashboard_auction_level_year_cumulative_2026-01-01_retrospective_4.csv` | 461 | Строки уровня отдельного размещения / аукциона. |
| `period_summary` | `outputs/dashboards/dashboard_period_summary_year_cumulative_2026-01-01_retrospective_4.csv` | 5 | Периодная сводка спроса, предложения, размещения и доходности. |
| `kpi_summary` | `outputs/dashboards/dashboard_kpi_summary_year_cumulative_2026-01-01_retrospective_4.csv` | 75 | KPI в long-format для карточек dashboard. |
| `maturity_structure` | `outputs/dashboards/dashboard_maturity_structure_year_cumulative_2026-01-01_retrospective_4.csv` | 13 | Структура размещения по срокам обращения. |
| `yield_distribution` | `outputs/dashboards/dashboard_yield_distribution_year_cumulative_2026-01-01_retrospective_4.csv` | 11 | Распределение доходности по периодам и видам ОФЗ. |
| `demand_supply` | `outputs/dashboards/dashboard_demand_supply_year_cumulative_2026-01-01_retrospective_4.csv` | 7 | Спрос и предложение по периодам и форматам. |
| `metadata` | `outputs/dashboards/dashboard_metadata_year_cumulative_2026-01-01_retrospective_4.json` | 1 | JSON metadata по dashboard exports. |
| `data_dictionary` | `outputs/dashboards/dashboard_data_dictionary_year_cumulative_2026-01-01_retrospective_4.csv` | 16 | Словарь данных dashboard exports. |
| `semantic_layer_fields` | `outputs/dashboards/semantic_layer/dashboard_semantic_layer_fields_year_cumulative_2026-01-01_retrospective_4.csv` | 53 | Каталог полей semantic layer: русские названия, technical names, units и правила расчета. |
| `semantic_layer_metrics` | `outputs/dashboards/semantic_layer/dashboard_semantic_layer_metrics_year_cumulative_2026-01-01_retrospective_4.csv` | 10 | Каталог управленческих метрик semantic layer с формулами и ограничениями. |
| `semantic_layer_dimensions` | `outputs/dashboards/semantic_layer/dashboard_semantic_layer_dimensions_year_cumulative_2026-01-01_retrospective_4.csv` | 8 | Каталог измерений, рекомендуемых фильтров и default sorting для dashboard. |
| `semantic_layer_relationships` | `outputs/dashboards/semantic_layer/dashboard_semantic_layer_relationships_year_cumulative_2026-01-01_retrospective_4.csv` | 6 | Контракт связей между dashboard-ready таблицами. |
| `semantic_layer_manifest` | `outputs/dashboards/semantic_layer/dashboard_semantic_layer_manifest_year_cumulative_2026-01-01_retrospective_4.json` | 1 | JSON manifest semantic layer с параметрами отчета и списком semantic exports. |
| `monthly_metrics` | `outputs/dashboards/monthly/dashboard_monthly_metrics_year_cumulative_2026-01-01_retrospective_4.csv` | 60 | BI-ready помесячные показатели для объяснения накопленного итога. |
| `monthly_data_dictionary` | `outputs/dashboards/monthly/dashboard_monthly_data_dictionary_year_cumulative_2026-01-01_retrospective_4.csv` | 37 | Словарь данных помесячного dashboard layer. |

## Ключевые KPI

- Совокупный спрос: `12 622 493.9` млн руб.
- Совокупное предложение: `28 343 508.3` млн руб.
- Объем размещения: `8 047 086.6` млн руб.
- Bid-to-cover: `0.445`.
- Спрос / размещение: `1.569`.
- Средневзвешенная доходность: `12.08`%.

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
