# Run manifest

Метка: `вторая модернизация`.

## Параметры запуска

- `run_id`: `20260604_190842_194415f1`
- `timestamp`: `2026-06-04T19:08:42`
- `report_date`: `2026-01-01`
- `period_type`: `year`
- `aggregation_mode`: `cumulative`
- `retrospective_years`: `4`
- `stages`: `1, 2, 3, 4, 5, 6, 7, 8, 8.1, revenue_analytics, revenue_charts, monthly_analytics, monthly_charts, 9, 9.1, semantic_model_v2, 10, 11, 12`

## Периоды

| Порядок | Период | Начало | Конец | Target |
| ---: | --- | --- | --- | --- |
| 0 | `2021` | `2021-01-01` | `2021-12-31` | `False` |
| 1 | `2022` | `2022-01-01` | `2022-12-31` | `False` |
| 2 | `2023` | `2023-01-01` | `2023-12-31` | `False` |
| 3 | `2024` | `2024-01-01` | `2024-12-31` | `False` |
| 4 | `2025` | `2025-01-01` | `2025-12-31` | `True` |

## Статусы проверок

| Проверка | Статус |
| --- | --- |
| `analytical_csv_exist_for_params` | `ok` |
| `analytical_tables_exist_for_params` | `ok` |
| `chart_data_exist_for_params` | `ok` |
| `charts_exist_for_params` | `ok` |
| `dashboard_exports_exist_for_params` | `ok` |
| `demand_cutoff_explanation_csv_exists` | `ok` |
| `demand_cutoff_explanation_html_exists` | `ok` |
| `monthly_cumulative_placement_csv_exists` | `ok` |
| `monthly_cumulative_placement_html_exists` | `ok` |
| `monthly_demand_supply_csv_exists` | `ok` |
| `monthly_demand_supply_html_exists` | `ok` |
| `monthly_metrics_exists` | `ok` |
| `monthly_placement_by_format_csv_exists` | `ok` |
| `monthly_placement_by_format_html_exists` | `ok` |
| `monthly_placement_by_maturity_csv_exists` | `ok` |
| `monthly_placement_by_maturity_html_exists` | `ok` |
| `monthly_placement_volume_csv_exists` | `ok` |
| `monthly_placement_volume_html_exists` | `ok` |
| `no_direct_files_in_outputs_exports` | `warning` |
| `pipeline_all_run` | `ok` |
| `pipeline_compare` | `not_requested` |
| `pipeline_safe_mode` | `disabled` |
| `raw_data_registry_exists` | `ok` |
| `report_scope_exists` | `ok` |
| `yield_vs_discount_csv_exists` | `ok` |
| `yield_vs_discount_facet_csv_exists` | `ok` |
| `yield_vs_discount_facet_html_exists` | `ok` |
| `yield_vs_discount_html_exists` | `ok` |
| `yield_vs_discount_outliers_csv_exists` | `ok` |
| `yield_vs_discount_outliers_html_exists` | `ok` |

## Outputs

- Файлов: `347`
- Размер, байт: `495283033`

| Область | Файлов | Размер, байт |
| --- | ---: | ---: |
| `outputs/.gitkeep` | 1 | 0 |
| `outputs/archive` | 2 | 4861513 |
| `outputs/charts` | 107 | 483410985 |
| `outputs/dashboards` | 35 | 399730 |
| `outputs/exports` | 141 | 3170241 |
| `outputs/reports` | 60 | 3440564 |
| `outputs/tmp` | 1 | 0 |

## Ключевые графики и CSV-основы

| Артефакт | Путь | Статус | Размер, байт |
| --- | --- | --- | ---: |
| `monthly_placement_volume_html` | `outputs/charts/monthly/placement/monthly_placement_volume_year_cumulative_2026-01-01_retrospective_4.html` | `exists` | 4865022 |
| `monthly_placement_volume_csv` | `outputs/exports/chart_data/monthly_placement_volume_year_cumulative_2026-01-01_retrospective_4.csv` | `exists` | 16765 |
| `monthly_cumulative_placement_html` | `outputs/charts/monthly/placement/monthly_cumulative_placement_year_cumulative_2026-01-01_retrospective_4.html` | `exists` | 4867228 |
| `monthly_cumulative_placement_csv` | `outputs/exports/chart_data/monthly_cumulative_placement_year_cumulative_2026-01-01_retrospective_4.csv` | `exists` | 12797 |
| `monthly_demand_supply_html` | `outputs/charts/monthly/demand_supply/monthly_demand_supply_year_cumulative_2026-01-01_retrospective_4.html` | `exists` | 4885487 |
| `monthly_demand_supply_csv` | `outputs/exports/chart_data/monthly_demand_supply_year_cumulative_2026-01-01_retrospective_4.csv` | `exists` | 30280 |
| `monthly_placement_by_format_html` | `outputs/charts/monthly/structure/monthly_placement_by_format_year_cumulative_2026-01-01_retrospective_4.html` | `exists` | 4883554 |
| `monthly_placement_by_format_csv` | `outputs/exports/chart_data/monthly_placement_by_format_year_cumulative_2026-01-01_retrospective_4.csv` | `exists` | 31008 |
| `monthly_placement_by_maturity_html` | `outputs/charts/monthly/structure/monthly_placement_by_maturity_year_cumulative_2026-01-01_retrospective_4.html` | `exists` | 4900791 |
| `monthly_placement_by_maturity_csv` | `outputs/exports/chart_data/monthly_placement_by_maturity_year_cumulative_2026-01-01_retrospective_4.csv` | `exists` | 52044 |
| `demand_cutoff_explanation_html` | `outputs/charts/scatter/demand_cutoff/demand_cutoff_explanation_year_cumulative_2026-01-01_retrospective_4.html` | `exists` | 4886895 |
| `demand_cutoff_explanation_csv` | `outputs/exports/chart_data/risk_quadrant/demand_cutoff_explanation_year_cumulative_2026-01-01_retrospective_4.csv` | `exists` | 32000 |
| `yield_vs_discount_html` | `outputs/charts/scatter/yield_discount/yield_vs_discount_year_cumulative_2026-01-01_retrospective_4.html` | `exists` | 5018081 |
| `yield_vs_discount_csv` | `outputs/exports/chart_data/scatter/yield_vs_discount_year_cumulative_2026-01-01_retrospective_4.csv` | `exists` | 222185 |
| `yield_vs_discount_facet_html` | `outputs/charts/scatter/yield_discount/yield_vs_discount_facet_year_cumulative_2026-01-01_retrospective_4.html` | `exists` | 5021271 |
| `yield_vs_discount_facet_csv` | `outputs/exports/chart_data/scatter/yield_vs_discount_facet_year_cumulative_2026-01-01_retrospective_4.csv` | `exists` | 223479 |
| `yield_vs_discount_outliers_html` | `outputs/charts/scatter/yield_discount/yield_vs_discount_outliers_year_cumulative_2026-01-01_retrospective_4.html` | `exists` | 4889287 |
| `yield_vs_discount_outliers_csv` | `outputs/exports/chart_data/scatter/yield_vs_discount_outliers_year_cumulative_2026-01-01_retrospective_4.csv` | `exists` | 46700 |

## Контрольные суммы

- Ключевых scripts: `22`
- Raw files: `8`

## Warnings

- Нет.

## Limitations

- Manifest формируется после успешного `--all` и фиксирует существующие outputs на момент записи.
- Статусы внешних QA-проверок отражают наличие артефактов; отдельные runtime QA-скрипты запускаются через quality gate или вручную.

## Файлы manifest

- `json`: `outputs/reports/run_manifest_20260604_190842_194415f1.json`
- `markdown`: `outputs/reports/run_manifest_20260604_190842_194415f1.md`
- `latest_json`: `data/processed/run_manifest_latest.json`
- `docs_report`: `docs/06_quality/run_manifest_report.md`
