# Quality gate report

Метка: `вторая модернизация`.

## Параметры

- `run_id`: `quality_gate_fast_month_cumulative_2026-05-01_r4_20260611_182130`
- `mode`: `fast`
- `report_date`: `2026-05-01`
- `period_type`: `month`
- `aggregation_mode`: `cumulative`
- `retrospective_years`: `4`

## Сводка

- OK: `14`
- Warnings: `0`
- Failures: `0`

## Проверки

| Проверка | Статус | Сообщение | Команда |
| --- | --- | --- | --- |
| `py_compile_key_scripts` | `ok` | Проверено scripts: 23. | - |
| `schema_validation.py` | `ok` | OK \| report_scope_exists \| ok OK \| report_scope_columns \| ok OK \| aggregation_mode_values \| ok OK \| report_period_dates_filled \| ok OK \| period_interval_rules \| ok OK \| period_count \| ok OK \| single_target_period \| ok OK \| monthly_layer_exists \| ok OK \| monthly_layer_schema \| ok OK \| monthly_target_months \| ok OK \| monthly_cumulative_vs_monthly \| ok OK \| monthly_cumulative_monotonic \| ok OK \| outputs_structure \| ok OK \| no_direct_outputs_exports \| ok OK \| chart_data_exports \| ok OK \| volume_bln_units \| ok Schema validation passed: 16 | `.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` |
| `regression_tests.py` | `ok` | OK \| test_month_cumulative_period \| ok OK \| test_month_point_period \| ok OK \| test_quarter_cumulative_period \| ok OK \| test_quarter_point_period \| ok OK \| test_year_period \| ok OK \| test_retrospective_period_count \| ok OK \| test_monthly_layer_cumulative_months_and_april_cumulative \| ok OK \| test_monthly_layer_point_april_only \| ok OK \| test_drpa_excluded_from_demand_ratios \| ok OK \| test_zero_placement_ratio_handling \| ok OK \| test_unsatisfied_auction_ratios \| ok OK \| test_zero_or_missing_yield_handling \| ok OK \| test_bid_to_cover_outlier_detection \| ok OK \| test_outputs_structure_contract \| ok Regression tests passed: 14 | `.\.venv\Scripts\python.exe scripts\regression_tests.py` |
| `smoke_tests.py` | `ok` | OK \| py_compile_key_scripts \| ok OK \| pipeline_command_contract \| ok OK \| interactive_cleanup_contract \| ok OK \| analytical_tables_exist \| ok OK \| charts_exist \| ok OK \| monthly_outputs_exist \| ok OK \| dashboard_exports_exist \| ok OK \| outputs_structure \| ok OK \| no_xlsx_directly_in_outputs_exports \| ok Smoke tests passed: 9 | `.\.venv\Scripts\python.exe scripts\smoke_tests.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` |
| `html_chart_qa.py` | `ok` | OK \| html_charts_exist \| Найдено HTML-графиков: 50. OK \| russian_titles \| В графиках найдены русскоязычные названия. OK \| russian_axes \| Русские подписи осей/измерений присутствуют. OK \| hovertemplate \| Hovertemplate найден и содержит русские подписи. OK \| monthly_bid_cover_contract \| monthly_bid_to_cover проверен: 1 файлов. OK \| monthly_demand_supply_contract \| monthly_demand_supply проверен: 1 файлов. OK \| monthly_placement_volume_contract \| monthly_placement_volume проверен: 1 файлов; label_display соответствует placement_volume_bln. OK \| monthly_cumulative_placement_contract \| monthly_cumulative_placement проверен: 1 файлов. OK \| monthly_heatmap_placement_contract \| monthly_heatmap_placement проверен: 1 файлов. OK \| monthly_heatmap_revenue_contract \| monthly_heatmap_revenue проверен: 1 файлов. OK \| facet_yaxis_title_policy \| Facet Y-title policy проверена: 5 файлов. OK \| volume_scale_bln \| Проверены volume-графики: 15; формат M/B/k не найден. OK \| stacked_structure_charts \| Stacked structure charts проверены: 4 файлов. OK \| format_structure_contract \| format_structure проверен: 1 файлов. OK \| format_discount_contract \| format_discount проверен: 1 файлов. OK \| format_nominal_rev ... | `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` |
| `visual_regression.py` | `ok` | OK \| - \| visual_regression_mode \| visual_regression_mode=auto; screenshot backend unavailable, fallback used: Python package 'playwright' is not installed WARNING \| - \| screenshot_backend \| Playwright unavailable; fallback used: Python package 'playwright' is not installed OK \| - \| screenshot_backend \| visual_regression_mode=auto; screenshot backend unavailable, fallback used: Python package 'playwright' is not installed OK \| - \| html_files_exist \| Найдено HTML-файлов: 50. OK \| - \| yield_vs_discount_exists \| Найдено yield_vs_discount HTML: 3. OK \| monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html \| trace_types \| scatter OK \| monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html \| title \| Помесячное покрытие предложения спросом OK \| monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html \| axis_titles \| Русские подписи осей/измерений найдены. OK \| monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html \| annotations \| Найдены annotation/text entries: 10. OK \| monthly_bid_to_cover_month_cumulative_2026-05-01_retrospective_4.html \| legend \| Legend/name metadata найдено. OK \| monthly_bid_to_cover_month_cumulative_2026-05-0 ... | `.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` |
| `readme_contract` | `ok` | README содержит локальные команды и ключевые разделы. | - |
| `outputs_structure` | `ok` | Структура outputs соответствует контракту. | - |
| `docs_structure` | `ok` | Корень docs/ чистый; индекс, отчеты реорганизации и планы scripts найдены. | - |
| `charts_structure` | `ok` | Карта графиков и ключевые категории outputs/charts/ найдены; HTML в корне нет. | - |
| `yield_vs_discount_outputs` | `ok` | Найдены yield_vs_discount main/facet/outliers и CSV-основы. | - |
| `scripts_structure` | `ok` | scripts/README.md и планы структуры scripts найдены. | - |
| `run_manifest` | `ok` | Latest manifest найден: 20260609_110853_c779f602. | - |
| `dashboard_semantic_model` | `ok` | Semantic model v2 найден: version=2.0.0. | - |

## Интерпретация

- `ok` означает успешную проверку.
- `warning` означает, что блок отсутствует, еще не создан или требует ручной проверки, но остальные проверки можно продолжать.
- `fail` означает дефект контракта или неуспешное завершение обязательной проверки.

## Ограничения

- Quality gate не изменяет `data/raw/`.
- `html_chart_qa.py` и `visual_regression.py` запускаются в режимах `fast` и `full`.
- Проверка отсутствия повторяющихся facet-осей выполняется через `html_chart_qa.py`.
- В режиме `full` дополнительно запускается опциональный `anomaly_tests.py`, если он уже создан.
