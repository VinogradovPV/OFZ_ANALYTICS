# Миграция структуры outputs

Дата формирования: `2026-05-21 10:17:43`.

Скрипт не удаляет файлы безвозвратно и не изменяет `data/raw/`.

## Целевая структура

- `outputs/reports/`
- `outputs/reports/analytical_tables/`
- `outputs/reports/monthly_tables/`
- `outputs/exports/`
- `outputs/exports/analytical_csv/`
- `outputs/exports/chart_data/`
- `outputs/exports/chart_data/risk_quadrant/`
- `outputs/exports/chart_data/sankey/`
- `outputs/exports/chart_data/boxplot/`
- `outputs/exports/chart_data/structure/`
- `outputs/exports/technical/`
- `outputs/exports/technical/review_required/`
- `outputs/dashboards/`
- `outputs/archive/`
- `outputs/archive/review_required/`

## Решения по файлам

| Файл | Решение | Причина | Целевой путь |
|---|---|---|---|
| `outputs/charts/bid_to_cover_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/bid_to_cover_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/bid_to_cover_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/bid_to_cover_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/demand_cutoff_explanation_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/demand_cutoff_explanation_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/demand_cutoff_explanation_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/demand_cutoff_explanation_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/demand_supply_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/demand_supply_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/demand_supply_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/demand_supply_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/format_structure_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/format_structure_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/format_structure_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/format_structure_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/maturity_structure_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/maturity_structure_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/maturity_structure_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/maturity_structure_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/placement_volume_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/placement_volume_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/placement_volume_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/placement_volume_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/risk_quadrant_demand_to_placement_by_quarter_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/risk_quadrant_demand_to_placement_by_quarter_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/risk_quadrant_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/risk_quadrant_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/risk_quadrant_retrospective_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/risk_quadrant_retrospective_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/risk_quadrant_retrospective_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/risk_quadrant_retrospective_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/risk_quadrant_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/risk_quadrant_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/sankey_period_format_maturity_type_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/sankey_period_format_maturity_type_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/sankey_period_format_maturity_type_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/sankey_period_format_maturity_type_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/sankey_period_format_type_maturity_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/sankey_period_format_type_maturity_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/sankey_period_format_type_maturity_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/sankey_period_format_type_maturity_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/sankey_period_maturity_type_format_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/sankey_period_maturity_type_format_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/sankey_period_maturity_type_format_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/sankey_period_maturity_type_format_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/sankey_structure_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/sankey_structure_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/sankey_structure_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/sankey_structure_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/sankey_target_period_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/sankey_target_period_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/sankey_target_period_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/sankey_target_period_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/yield_boxplot_by_ofz_type_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/yield_boxplot_by_ofz_type_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/yield_boxplot_by_ofz_type_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/yield_boxplot_by_ofz_type_year_2026-01-01_retrospective_5.html` |
| `outputs/charts/yield_by_type_month_2026-05-01_retrospective_4.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/yield_by_type_month_2026-05-01_retrospective_4.html` |
| `outputs/charts/yield_by_type_year_2026-01-01_retrospective_5.html` | `keep` | HTML-графики остаются в outputs/charts/. | `outputs/charts/yield_by_type_year_2026-01-01_retrospective_5.html` |
| `outputs/dashboards/dashboard_auction_level_month_2026-05-01_retrospective_4.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_auction_level_month_2026-05-01_retrospective_4.csv` |
| `outputs/dashboards/dashboard_auction_level_year_2026-01-01_retrospective_5.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_auction_level_year_2026-01-01_retrospective_5.csv` |
| `outputs/dashboards/dashboard_data_dictionary_month_2026-05-01_retrospective_4.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_data_dictionary_month_2026-05-01_retrospective_4.csv` |
| `outputs/dashboards/dashboard_data_dictionary_year_2026-01-01_retrospective_5.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_data_dictionary_year_2026-01-01_retrospective_5.csv` |
| `outputs/dashboards/dashboard_demand_supply_month_2026-05-01_retrospective_4.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_demand_supply_month_2026-05-01_retrospective_4.csv` |
| `outputs/dashboards/dashboard_demand_supply_year_2026-01-01_retrospective_5.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_demand_supply_year_2026-01-01_retrospective_5.csv` |
| `outputs/dashboards/dashboard_kpi_summary_month_2026-05-01_retrospective_4.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_kpi_summary_month_2026-05-01_retrospective_4.csv` |
| `outputs/dashboards/dashboard_kpi_summary_year_2026-01-01_retrospective_5.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_kpi_summary_year_2026-01-01_retrospective_5.csv` |
| `outputs/dashboards/dashboard_maturity_structure_month_2026-05-01_retrospective_4.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_maturity_structure_month_2026-05-01_retrospective_4.csv` |
| `outputs/dashboards/dashboard_maturity_structure_year_2026-01-01_retrospective_5.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_maturity_structure_year_2026-01-01_retrospective_5.csv` |
| `outputs/dashboards/dashboard_metadata_month_2026-05-01_retrospective_4.json` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_metadata_month_2026-05-01_retrospective_4.json` |
| `outputs/dashboards/dashboard_metadata_year_2026-01-01_retrospective_5.json` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_metadata_year_2026-01-01_retrospective_5.json` |
| `outputs/dashboards/dashboard_period_summary_month_2026-05-01_retrospective_4.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_period_summary_month_2026-05-01_retrospective_4.csv` |
| `outputs/dashboards/dashboard_period_summary_year_2026-01-01_retrospective_5.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_period_summary_year_2026-01-01_retrospective_5.csv` |
| `outputs/dashboards/dashboard_yield_distribution_month_2026-05-01_retrospective_4.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_yield_distribution_month_2026-05-01_retrospective_4.csv` |
| `outputs/dashboards/dashboard_yield_distribution_year_2026-01-01_retrospective_5.csv` | `keep` | Файл уже находится в целевой структуре. | `outputs/dashboards/dashboard_yield_distribution_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/bid_to_cover_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа риск-графика. | `outputs/exports/chart_data/risk_quadrant/bid_to_cover_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/bid_to_cover_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа риск-графика. | `outputs/exports/chart_data/risk_quadrant/bid_to_cover_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/demand_cutoff_explanation_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа риск-графика. | `outputs/exports/chart_data/risk_quadrant/demand_cutoff_explanation_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/demand_cutoff_explanation_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа риск-графика. | `outputs/exports/chart_data/risk_quadrant/demand_cutoff_explanation_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/demand_supply_month_2026-05-01_retrospective_4.csv` | `move` | CSV-копия обязательной аналитической таблицы. | `outputs/exports/analytical_csv/demand_supply_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/demand_supply_month_2026-05-01_retrospective_4.xlsx` | `move` | XLSX обязательной аналитической таблицы. | `outputs/reports/analytical_tables/demand_supply_month_2026-05-01_retrospective_4.xlsx` |
| `outputs/exports/demand_supply_year_2026-01-01_retrospective_5.csv` | `move` | CSV-копия обязательной аналитической таблицы. | `outputs/exports/analytical_csv/demand_supply_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/demand_supply_year_2026-01-01_retrospective_5.xlsx` | `move` | XLSX обязательной аналитической таблицы. | `outputs/reports/analytical_tables/demand_supply_year_2026-01-01_retrospective_5.xlsx` |
| `outputs/exports/format_structure_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа структурной визуализации. | `outputs/exports/chart_data/structure/format_structure_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/format_structure_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа структурной визуализации. | `outputs/exports/chart_data/structure/format_structure_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/maturity_structure_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа структурной визуализации. | `outputs/exports/chart_data/structure/maturity_structure_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/maturity_structure_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа структурной визуализации. | `outputs/exports/chart_data/structure/maturity_structure_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/ofz_yield_by_type_month_2026-05-01_retrospective_4.csv` | `move` | CSV-копия обязательной аналитической таблицы. | `outputs/exports/analytical_csv/ofz_yield_by_type_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/ofz_yield_by_type_month_2026-05-01_retrospective_4.xlsx` | `move` | XLSX обязательной аналитической таблицы. | `outputs/reports/analytical_tables/ofz_yield_by_type_month_2026-05-01_retrospective_4.xlsx` |
| `outputs/exports/ofz_yield_by_type_year_2026-01-01_retrospective_5.csv` | `move` | CSV-копия обязательной аналитической таблицы. | `outputs/exports/analytical_csv/ofz_yield_by_type_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/ofz_yield_by_type_year_2026-01-01_retrospective_5.xlsx` | `move` | XLSX обязательной аналитической таблицы. | `outputs/reports/analytical_tables/ofz_yield_by_type_year_2026-01-01_retrospective_5.xlsx` |
| `outputs/exports/placement_volume_by_maturity_month_2026-05-01_retrospective_4.csv` | `move` | CSV-копия обязательной аналитической таблицы. | `outputs/exports/analytical_csv/placement_volume_by_maturity_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/placement_volume_by_maturity_month_2026-05-01_retrospective_4.xlsx` | `move` | XLSX обязательной аналитической таблицы. | `outputs/reports/analytical_tables/placement_volume_by_maturity_month_2026-05-01_retrospective_4.xlsx` |
| `outputs/exports/placement_volume_by_maturity_year_2026-01-01_retrospective_5.csv` | `move` | CSV-копия обязательной аналитической таблицы. | `outputs/exports/analytical_csv/placement_volume_by_maturity_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/placement_volume_by_maturity_year_2026-01-01_retrospective_5.xlsx` | `move` | XLSX обязательной аналитической таблицы. | `outputs/reports/analytical_tables/placement_volume_by_maturity_year_2026-01-01_retrospective_5.xlsx` |
| `outputs/exports/placement_volume_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа структурной визуализации. | `outputs/exports/chart_data/structure/placement_volume_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/placement_volume_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа структурной визуализации. | `outputs/exports/chart_data/structure/placement_volume_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/risk_quadrant_demand_to_placement_by_quarter_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа риск-графика. | `outputs/exports/chart_data/risk_quadrant/risk_quadrant_demand_to_placement_by_quarter_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/risk_quadrant_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа риск-графика. | `outputs/exports/chart_data/risk_quadrant/risk_quadrant_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/risk_quadrant_retrospective_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа риск-графика. | `outputs/exports/chart_data/risk_quadrant/risk_quadrant_retrospective_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/risk_quadrant_retrospective_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа риск-графика. | `outputs/exports/chart_data/risk_quadrant/risk_quadrant_retrospective_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/risk_quadrant_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа риск-графика. | `outputs/exports/chart_data/risk_quadrant/risk_quadrant_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/sankey_period_format_maturity_type_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа Sankey-графика. | `outputs/exports/chart_data/sankey/sankey_period_format_maturity_type_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/sankey_period_format_maturity_type_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа Sankey-графика. | `outputs/exports/chart_data/sankey/sankey_period_format_maturity_type_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/sankey_period_format_type_maturity_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа Sankey-графика. | `outputs/exports/chart_data/sankey/sankey_period_format_type_maturity_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/sankey_period_format_type_maturity_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа Sankey-графика. | `outputs/exports/chart_data/sankey/sankey_period_format_type_maturity_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/sankey_period_maturity_type_format_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа Sankey-графика. | `outputs/exports/chart_data/sankey/sankey_period_maturity_type_format_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/sankey_period_maturity_type_format_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа Sankey-графика. | `outputs/exports/chart_data/sankey/sankey_period_maturity_type_format_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/sankey_structure_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа Sankey-графика. | `outputs/exports/chart_data/sankey/sankey_structure_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/sankey_structure_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа Sankey-графика. | `outputs/exports/chart_data/sankey/sankey_structure_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/sankey_target_period_structure_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа Sankey-графика. | `outputs/exports/chart_data/sankey/sankey_target_period_structure_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/sankey_target_period_structure_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа Sankey-графика. | `outputs/exports/chart_data/sankey/sankey_target_period_structure_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/yield_boxplot_by_ofz_type_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа boxplot-графика. | `outputs/exports/chart_data/boxplot/yield_boxplot_by_ofz_type_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/yield_boxplot_by_ofz_type_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа boxplot-графика. | `outputs/exports/chart_data/boxplot/yield_boxplot_by_ofz_type_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/yield_boxplot_stats_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа boxplot-графика. | `outputs/exports/chart_data/boxplot/yield_boxplot_stats_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/yield_boxplot_stats_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа boxplot-графика. | `outputs/exports/chart_data/boxplot/yield_boxplot_stats_year_2026-01-01_retrospective_5.csv` |
| `outputs/exports/yield_by_type_month_2026-05-01_retrospective_4.csv` | `move` | Таблица-основа структурной визуализации. | `outputs/exports/chart_data/structure/yield_by_type_month_2026-05-01_retrospective_4.csv` |
| `outputs/exports/yield_by_type_year_2026-01-01_retrospective_5.csv` | `move` | Таблица-основа структурной визуализации. | `outputs/exports/chart_data/structure/yield_by_type_year_2026-01-01_retrospective_5.csv` |

## Перенесенные файлы

- `outputs/exports/bid_to_cover_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/risk_quadrant/bid_to_cover_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/bid_to_cover_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/risk_quadrant/bid_to_cover_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/demand_cutoff_explanation_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/risk_quadrant/demand_cutoff_explanation_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/demand_cutoff_explanation_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/risk_quadrant/demand_cutoff_explanation_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/demand_supply_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/analytical_csv/demand_supply_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/demand_supply_month_2026-05-01_retrospective_4.xlsx` -> `outputs/reports/analytical_tables/demand_supply_month_2026-05-01_retrospective_4.xlsx`
- `outputs/exports/demand_supply_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/analytical_csv/demand_supply_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/demand_supply_year_2026-01-01_retrospective_5.xlsx` -> `outputs/reports/analytical_tables/demand_supply_year_2026-01-01_retrospective_5.xlsx`
- `outputs/exports/format_structure_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/structure/format_structure_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/format_structure_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/structure/format_structure_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/maturity_structure_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/structure/maturity_structure_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/maturity_structure_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/structure/maturity_structure_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/ofz_yield_by_type_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/analytical_csv/ofz_yield_by_type_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/ofz_yield_by_type_month_2026-05-01_retrospective_4.xlsx` -> `outputs/reports/analytical_tables/ofz_yield_by_type_month_2026-05-01_retrospective_4.xlsx`
- `outputs/exports/ofz_yield_by_type_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/analytical_csv/ofz_yield_by_type_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/ofz_yield_by_type_year_2026-01-01_retrospective_5.xlsx` -> `outputs/reports/analytical_tables/ofz_yield_by_type_year_2026-01-01_retrospective_5.xlsx`
- `outputs/exports/placement_volume_by_maturity_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/analytical_csv/placement_volume_by_maturity_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/placement_volume_by_maturity_month_2026-05-01_retrospective_4.xlsx` -> `outputs/reports/analytical_tables/placement_volume_by_maturity_month_2026-05-01_retrospective_4.xlsx`
- `outputs/exports/placement_volume_by_maturity_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/analytical_csv/placement_volume_by_maturity_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/placement_volume_by_maturity_year_2026-01-01_retrospective_5.xlsx` -> `outputs/reports/analytical_tables/placement_volume_by_maturity_year_2026-01-01_retrospective_5.xlsx`
- `outputs/exports/placement_volume_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/structure/placement_volume_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/placement_volume_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/structure/placement_volume_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/risk_quadrant_demand_to_placement_by_quarter_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/risk_quadrant/risk_quadrant_demand_to_placement_by_quarter_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/risk_quadrant_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/risk_quadrant/risk_quadrant_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/risk_quadrant_retrospective_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/risk_quadrant/risk_quadrant_retrospective_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/risk_quadrant_retrospective_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/risk_quadrant/risk_quadrant_retrospective_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/risk_quadrant_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/risk_quadrant/risk_quadrant_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/sankey_period_format_maturity_type_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/sankey/sankey_period_format_maturity_type_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/sankey_period_format_maturity_type_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/sankey/sankey_period_format_maturity_type_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/sankey_period_format_type_maturity_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/sankey/sankey_period_format_type_maturity_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/sankey_period_format_type_maturity_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/sankey/sankey_period_format_type_maturity_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/sankey_period_maturity_type_format_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/sankey/sankey_period_maturity_type_format_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/sankey_period_maturity_type_format_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/sankey/sankey_period_maturity_type_format_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/sankey_structure_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/sankey/sankey_structure_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/sankey_structure_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/sankey/sankey_structure_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/sankey_target_period_structure_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/sankey/sankey_target_period_structure_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/sankey_target_period_structure_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/sankey/sankey_target_period_structure_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/yield_boxplot_by_ofz_type_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/boxplot/yield_boxplot_by_ofz_type_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/yield_boxplot_by_ofz_type_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/boxplot/yield_boxplot_by_ofz_type_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/yield_boxplot_stats_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/boxplot/yield_boxplot_stats_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/yield_boxplot_stats_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/boxplot/yield_boxplot_stats_year_2026-01-01_retrospective_5.csv`
- `outputs/exports/yield_by_type_month_2026-05-01_retrospective_4.csv` -> `outputs/exports/chart_data/structure/yield_by_type_month_2026-05-01_retrospective_4.csv`
- `outputs/exports/yield_by_type_year_2026-01-01_retrospective_5.csv` -> `outputs/exports/chart_data/structure/yield_by_type_year_2026-01-01_retrospective_5.csv`
