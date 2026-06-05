# Структура outputs

Документ фиксирует целевую структуру `outputs/` и проверки, которые должны покрываться smoke tests после нового запуска pipeline.

## Целевая структура

```text
outputs/reports/
outputs/reports/analytical_tables/
outputs/reports/monthly_tables/

outputs/exports/
outputs/exports/analytical_csv/
outputs/exports/chart_data/
outputs/exports/chart_data/risk_quadrant/
outputs/exports/chart_data/sankey/
outputs/exports/chart_data/boxplot/
outputs/exports/chart_data/structure/
outputs/exports/technical/
outputs/exports/technical/review_required/

outputs/dashboards/
outputs/archive/
```

## Назначение папок

| Папка | Назначение |
| --- | --- |
| `outputs/reports/` | Человекочитаемые отчетные таблицы и отчетные файлы. |
| `outputs/reports/analytical_tables/` | XLSX обязательных аналитических таблиц. |
| `outputs/reports/monthly_tables/` | XLSX помесячных отчетных таблиц и monthly layer reports. |
| `outputs/exports/analytical_csv/` | CSV-копии отчетных таблиц. |
| `outputs/exports/chart_data/` | Технические таблицы-основы визуализаций. |
| `outputs/exports/chart_data/risk_quadrant/` | CSV-основы risk quadrant, demand cutoff и ratio-графиков. |
| `outputs/exports/chart_data/sankey/` | CSV-основы Sankey-графиков. |
| `outputs/exports/chart_data/boxplot/` | CSV-основы boxplot-графиков и статистики распределений. |
| `outputs/exports/chart_data/structure/` | CSV-основы структурных визуализаций. |
| `outputs/exports/technical/` | Технические exports, не относящиеся к отчетным таблицам или chart data. |
| `outputs/exports/technical/review_required/` | Файлы, назначение которых требует ручной проверки. |
| `outputs/dashboards/` | BI-ready dashboard exports. |
| `outputs/archive/` | Устаревшие или перенесенные outputs, которые не удаляются автоматически. |

## Smoke checks

Smoke tests, если они будут добавлены в проект, должны проверять наличие:

- `outputs/reports/analytical_tables/`
- `outputs/reports/monthly_tables/`
- `outputs/exports/analytical_csv/`
- `outputs/exports/chart_data/risk_quadrant/`
- `outputs/exports/chart_data/sankey/`
- `outputs/exports/chart_data/boxplot/`
- `outputs/exports/chart_data/structure/`
- `outputs/dashboards/`

После нового запуска pipeline smoke tests также должны проверять, что отчетные `.xlsx` не сохраняются напрямую в корень `outputs/exports/`.

## Правило хранения

Новые генерации должны сохранять файлы сразу в профильную папку. Старые или неоднозначные outputs не удаляются безвозвратно и при необходимости переносятся в `outputs/archive/` или `outputs/exports/technical/review_required/`.

## Актуализация структуры на 2026-05-25

| Тип результата | Целевая папка | Комментарий |
| --- | --- | --- |
| Обязательные XLSX-таблицы | `outputs/reports/analytical_tables/` | Человекочитаемые аналитические таблицы. |
| Помесячные XLSX-таблицы | `outputs/reports/monthly_tables/` | Monthly layer и monthly reports. |
| CSV-копии отчетных таблиц | `outputs/exports/analytical_csv/` | Машиночитаемые версии отчетных таблиц. |
| HTML-графики | `outputs/charts/` | Интерактивные визуализации. |
| Risk/scatter chart data | `outputs/exports/chart_data/risk_quadrant/` | Основы risk quadrant, demand cutoff, scatter/outlier/log/facet версий. |
| Sankey chart data | `outputs/exports/chart_data/sankey/` | Потоки Sankey и таблицы-основы. |
| Boxplot chart data | `outputs/exports/chart_data/boxplot/` | Статистики boxplot, включая long-mode/facet diagnostics. |
| Structure chart data | `outputs/exports/chart_data/structure/` | Stacked structure charts, итоги столбцов и доли сегментов. |
| Dashboard exports | `outputs/dashboards/` | BI-ready datasets, metadata, data dictionary, semantic layer. |
| Executive summary | `outputs/reports/` | Параметризуемое управленческое резюме. |

Новые файлы не должны сохраняться напрямую в корень `outputs/exports/`. Исключение допускается только для архивных/наследованных файлов до миграции; такие файлы должны быть перенесены через `scripts/reorganize_outputs.py` или `scripts/migrate_outputs_structure.py`.

## Проверки структуры

Рекомендуемые команды ручной проверки:

```powershell
.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

```powershell
.\.venv\Scripts\python.exe scripts\smoke_tests.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```
