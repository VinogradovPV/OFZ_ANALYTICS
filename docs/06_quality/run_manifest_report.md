# Run manifest

Метка: `вторая модернизация`.

## Параметры запуска

- `run_id`: `20260609_110853_c779f602`
- `timestamp`: `2026-06-09T11:08:53`
- `report_date`: `2026-05-01`
- `period_type`: `month`
- `aggregation_mode`: `cumulative`
- `retrospective_years`: `4`
- `stages`: `1, 2, 3, 4, 5, 6, 7, 8, 8.1, revenue_analytics, revenue_charts, monthly_analytics, monthly_charts, 9, 9.1, semantic_model_v2, 10, 11, 12`

## Периоды

| Порядок | Период | Начало | Конец | Target |
| ---: | --- | --- | --- | --- |
| 0 | `2022-M01-M04` | `2022-01-01` | `2022-04-30` | `False` |
| 1 | `2023-M01-M04` | `2023-01-01` | `2023-04-30` | `False` |
| 2 | `2024-M01-M04` | `2024-01-01` | `2024-04-30` | `False` |
| 3 | `2025-M01-M04` | `2025-01-01` | `2025-04-30` | `False` |
| 4 | `2026-M01-M04` | `2026-01-01` | `2026-04-30` | `True` |

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

- Файлов: `399`
- Размер, байт: `498595333`

| Область | Файлов | Размер, байт |
| --- | ---: | ---: |
| `outputs/.gitkeep` | 1 | 0 |
| `outputs/archive` | 2 | 4861513 |
| `outputs/charts` | 107 | 483410985 |
| `outputs/dashboards` | 35 | 399730 |
| `outputs/exports` | 141 | 3170333 |
| `outputs/reports` | 112 | 6752772 |
| `outputs/tmp` | 1 | 0 |

## Ключевые графики и CSV-основы

| Артефакт | Путь | Статус | Размер, байт |
| --- | --- | --- | ---: |
| `monthly_placement_volume_html` | `outputs/charts/monthly/placement/monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html` | `exists` | 4861474 |
| `monthly_placement_volume_csv` | `outputs/exports/chart_data/monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.csv` | `exists` | 6254 |
| `monthly_cumulative_placement_html` | `outputs/charts/monthly/placement/monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.html` | `exists` | 4862493 |
| `monthly_cumulative_placement_csv` | `outputs/exports/chart_data/monthly_cumulative_placement_month_cumulative_2026-05-01_retrospective_4.csv` | `exists` | 4987 |
| `monthly_demand_supply_html` | `outputs/charts/monthly/demand_supply/monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.html` | `exists` | 4873543 |
| `monthly_demand_supply_csv` | `outputs/exports/chart_data/monthly_demand_supply_month_cumulative_2026-05-01_retrospective_4.csv` | `exists` | 11151 |
| `monthly_placement_by_format_html` | `outputs/charts/monthly/structure/monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.html` | `exists` | 4872872 |
| `monthly_placement_by_format_csv` | `outputs/exports/chart_data/monthly_placement_by_format_month_cumulative_2026-05-01_retrospective_4.csv` | `exists` | 11935 |
| `monthly_placement_by_maturity_html` | `outputs/charts/monthly/structure/monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.html` | `exists` | 4882412 |
| `monthly_placement_by_maturity_csv` | `outputs/exports/chart_data/monthly_placement_by_maturity_month_cumulative_2026-05-01_retrospective_4.csv` | `exists` | 19190 |
| `demand_cutoff_explanation_html` | `outputs/charts/scatter/demand_cutoff/demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.html` | `exists` | 4869184 |
| `demand_cutoff_explanation_csv` | `outputs/exports/chart_data/risk_quadrant/demand_cutoff_explanation_month_cumulative_2026-05-01_retrospective_4.csv` | `exists` | 12541 |
| `yield_vs_discount_html` | `outputs/charts/scatter/yield_discount/yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.html` | `exists` | 4927814 |
| `yield_vs_discount_csv` | `outputs/exports/chart_data/scatter/yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.csv` | `exists` | 91657 |
| `yield_vs_discount_facet_html` | `outputs/charts/scatter/yield_discount/yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html` | `exists` | 4930632 |
| `yield_vs_discount_facet_csv` | `outputs/exports/chart_data/scatter/yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.csv` | `exists` | 93387 |
| `yield_vs_discount_outliers_html` | `outputs/charts/scatter/yield_discount/yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html` | `exists` | 4886420 |
| `yield_vs_discount_outliers_csv` | `outputs/exports/chart_data/scatter/yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.csv` | `exists` | 32264 |

## Контрольные суммы

- Ключевых scripts: `22`
- Raw files: `8`

## Warnings

- Нет.

## Limitations

- Manifest формируется после успешного `--all` и фиксирует существующие outputs на момент записи.
- Статусы внешних QA-проверок отражают наличие артефактов; отдельные runtime QA-скрипты запускаются через quality gate или вручную.

## Cleanup pre-flight

- `status`: `not_requested`
- `mode`: `not_interactive`
- `returncode`: ``

## Pipeline telemetry

- `status`: `written`
- `json`: `outputs/reports/telemetry/telemetry_20260609_080836_53742514.json`
- `markdown`: `outputs/reports/telemetry/telemetry_20260609_080836_53742514.md`

## Файлы manifest

- `json`: `outputs/reports/run_manifest_20260609_110853_c779f602.json`
- `markdown`: `outputs/reports/run_manifest_20260609_110853_c779f602.md`
- `latest_json`: `data/processed/run_manifest_latest.json`
- `docs_report`: `docs/06_quality/run_manifest_report.md`
