# Production Cleanup Baseline

Дата фиксации: `2026-06-04`.

Этап: `0 - baseline перед production-cleanup`.

Команды выполнялись из корня проекта через локальное окружение:

```powershell
.\.venv\Scripts\python.exe
```

На этом этапе файлы не удалялись и не перемещались.

## Верхний уровень проекта

| Объект | Тип | Размер |
| --- | --- | --- |
| `.venv/` | директория | - |
| `.vscode/` | директория | - |
| `data/` | директория | - |
| `docs/` | директория | - |
| `logs/` | директория | - |
| `outputs/` | директория | - |
| `prompts/` | директория | - |
| `scripts/` | директория | - |
| `CHANGELOG.md` | файл | 4 353 bytes |
| `README.md` | файл | 38 061 bytes |
| `requirements.txt` | файл | 80 bytes |

## Количество файлов

| Папка | Количество файлов |
| --- | ---: |
| `scripts/` | 82 |
| `docs/` | 76 |
| `outputs/charts/` | 97 |
| `outputs/exports/` | 134 |
| `outputs/reports/` | 42 на момент первого замера; 44 после запуска baseline quality/visual reports |

## Крупнейшие файлы scripts

| Файл | Размер, bytes |
| --- | ---: |
| `scripts/06_build_charts.py` | 338 831 |
| `scripts/html_chart_qa.py` | 113 969 |
| `scripts/10_build_monthly_charts.py` | 86 634 |
| `scripts/07_dashboard_exports.py` | 70 630 |
| `scripts/visual_regression.py` | 58 785 |
| `scripts/generate_executive_summary.py` | 33 885 |
| `scripts/12_build_revenue_charts.py` | 32 785 |
| `scripts/08_analytical_tables.py` | 32 701 |
| `scripts/09_monthly_analytics.py` | 29 397 |
| `scripts/03_feature_engineering.py` | 28 534 |
| `scripts/run_pipeline.py` | 26 841 |
| `scripts/quality_gate.py` | 26 562 |

## Крупнейшие папки outputs

| Папка | Файлов | Размер, MB |
| --- | ---: | ---: |
| `outputs/charts/` | 97 | 447.09 |
| `outputs/archive/` | 1 | 4.64 |
| `outputs/exports/` | 134 | 2.89 |
| `outputs/reports/` | 44 | 2.52 |
| `outputs/dashboards/` | 34 | 0.38 |

## Baseline status: quality gate

Команда:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Статус: `FAIL`.

Причина: падает `schema_validation.py`, проверка `volume_bln_units`.

Деталь:

```text
В chart data с объемами отсутствует колонка единиц измерения:
outputs/exports/chart_data/scatter/format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.csv
outputs/exports/chart_data/structure/format_discount_month_cumulative_2026-05-01_retrospective_4.csv
```

Прочие проверки внутри `quality_gate --fast` прошли:

- `py_compile_key_scripts`: OK;
- `regression_tests.py`: OK, 14 проверок;
- `smoke_tests.py`: OK, 8 проверок;
- `html_chart_qa.py`: OK;
- `visual_regression.py`: OK через fallback static HTML / Plotly JSON inspection;
- `readme_contract`: OK;
- `outputs_structure`: OK;
- `docs_structure`: OK;
- `charts_structure`: OK;
- `yield_vs_discount_outputs`: OK;
- `scripts_structure`: OK;
- `run_manifest`: OK;
- `dashboard_semantic_model`: OK.

Последний отчет quality gate:

`outputs/reports/quality_gate_report_quality_gate_fast_month_cumulative_2026-05-01_r4_20260604_135654.md`

## Baseline status: schema validation

Команда:

```powershell
.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Статус: `FAIL`.

Единственный failing check:

```text
FAIL | volume_bln_units | В chart data с объемами отсутствует колонка единиц измерения:
outputs/exports/chart_data/scatter/format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.csv,
outputs/exports/chart_data/structure/format_discount_month_cumulative_2026-05-01_retrospective_4.csv.
```

Остальные schema checks: `OK`.

## Baseline status: compileall

Команда:

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
```

Статус: `OK`.

## Baseline status: pip check

Команда:

```powershell
.\.venv\Scripts\python.exe -m pip check
```

Статус: `OK`.

Результат:

```text
No broken requirements found.
```

## Baseline observations

- Главный production blocker подтвержден: `quality_gate --fast` красный только из-за `schema_validation.py`.
- Исправление должно быть точечным: добавить недостающую колонку единиц измерения в chart data exports для `format_terms_aggregate_scatter` и `format_discount`, а затем пересобрать соответствующие outputs.
- `outputs/charts/` является крупнейшей зоной проекта: около 447 MB. Любая будущая очистка HTML должна выполняться только через dry-run и архивирование.
- Крупнейший модуль проекта - `scripts/06_build_charts.py`; для production сопровождения его желательно декомпозировать после снятия текущего blocker.
- На этапе 0 `data/raw/` не изменялась.
