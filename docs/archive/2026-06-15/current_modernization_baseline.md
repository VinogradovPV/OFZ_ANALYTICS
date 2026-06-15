# Baseline модернизации проекта

Дата проверки: `2026-05-22`.

Проверка выполнена как аудит текущего контракта уже реализованных блоков. `data/raw/` не изменялся. Блоки aggregation-mode, `report_params.py`, `period_filter.py` и структура `outputs/` не переписывались.

## Итог

| Блок | Статус | Вывод |
|---|---|---|
| `aggregation-mode` в `run_pipeline.py` | confirmed | CLI принимает `--aggregation-mode`, допустимые значения берутся из `report_params.ALLOWED_AGGREGATION_MODES`, default = `cumulative`. |
| `report_params.py` | confirmed | `ReportParams` содержит `aggregation_mode`; периоды строятся из `report_date`, `retrospective_years`, `period_type`, `aggregation_mode`. |
| `period_filter.py` | confirmed | Использует `report_params.parse_report_args()`, фильтрует по интервалам и добавляет периодные колонки в report scope. |
| Структура `outputs/` | confirmed | Основные целевые папки существуют. |
| Запрет новых файлов напрямую в `outputs/exports/` | confirmed | Код генераторов использует новую структуру; найденные legacy-файлы перенесены в целевые папки. |

## 1. aggregation-mode в run_pipeline.py

| Требование | Статус | Наблюдение |
|---|---|---|
| `run_pipeline.py` принимает `--aggregation-mode` | confirmed | Аргумент объявлен в `parse_args()`. |
| Допустимые значения `cumulative` и `point` | confirmed | `choices=sorted(report_params.ALLOWED_AGGREGATION_MODES)`, где разрешены `cumulative`, `point`. |
| `cumulative` является default | confirmed | В `run_pipeline.py` default установлен как `cumulative`. |
| Параметр прокидывается downstream-этапам | confirmed | `build_report_args()` добавляет `--aggregation-mode` в команды этапов с периодной логикой. |

## 2. report_params.py

| Требование | Статус | Наблюдение |
|---|---|---|
| `ReportParams` содержит `aggregation_mode` | confirmed | Поле присутствует в dataclass. |
| Допустимые значения `cumulative`, `point` | confirmed | `ALLOWED_AGGREGATION_MODES = {"cumulative", "point"}`. |
| Default `cumulative` | confirmed | Default задан в `parse_report_args()`, `build_report_periods()` и `get_period_bounds()`. |
| `month + cumulative` | confirmed | `end_date = report_date - 1 day`, `start_date = 1 января года end_date`. |
| `month + point` | confirmed | `start_date = 1 число месяца end_date`, `end_date = report_date - 1 day`. |
| `quarter + cumulative` | confirmed | `start_date = 1 января года end_date`, `end_date = report_date - 1 day`. |
| `quarter + point` | confirmed | `start_date` рассчитывается как начало завершенного квартала перед `report_date`. |
| `year` | confirmed | `report_date` должен быть 1 января; период строится как завершенный предыдущий год. |
| Периоды идут от старого к новому | confirmed | `build_report_periods()` использует `range(retrospective_years, -1, -1)`. |
| Количество периодов = `retrospective_years + 1` | confirmed | Есть явная проверка длины списка периодов. |

Контрольные ожидаемые интервалы по текущей логике:

| Сценарий | Ожидаемый target period | Статус по коду |
|---|---|---|
| `month + cumulative + 2026-05-01` | `2026-01-01` - `2026-04-30` | confirmed |
| `month + point + 2026-05-01` | `2026-04-01` - `2026-04-30` | confirmed |
| `quarter + cumulative + 2026-07-01` | `2026-01-01` - `2026-06-30` | confirmed |
| `quarter + point + 2026-07-01` | `2026-04-01` - `2026-06-30` | confirmed |
| `year + 2026-01-01` | `2025-01-01` - `2025-12-31` | confirmed |

## 3. period_filter.py

| Требование | Статус | Наблюдение |
|---|---|---|
| Принимает `--aggregation-mode` | confirmed | Использует `report_params.parse_report_args()`, где аргумент уже описан. |
| Фильтрует по интервалам | confirmed | Используется `between(start_date, end_date, inclusive="both")`. |
| Формирует `report_period_start` | confirmed | Колонка добавляется в `period_df`. |
| Формирует `report_period_end` | confirmed | Колонка добавляется в `period_df`. |
| Формирует `report_period_label` | confirmed | Колонка добавляется в `period_df`. |
| Формирует `report_period_display_label` | confirmed | Колонка добавляется в `period_df`. |
| Формирует `report_period_file_label` | confirmed | Колонка добавляется в `period_df`. |
| Формирует `report_period_order` | confirmed | Колонка добавляется в `period_df`. |
| Формирует `aggregation_mode` | confirmed | Колонка добавляется в `period_df`. |
| Формирует `is_target_period` | confirmed | Колонка добавляется в `period_df`. |
| Пишет `data/processed/ofz_auctions_report_scope.csv` | confirmed | Output path используется через `config.OFZ_AUCTIONS_REPORT_SCOPE_CSV`. |

## 4. Структура outputs

| Папка | Статус |
|---|---|
| `outputs/reports/analytical_tables/` | exists |
| `outputs/reports/monthly_tables/` | exists |
| `outputs/exports/analytical_csv/` | exists |
| `outputs/exports/chart_data/` | exists |
| `outputs/exports/chart_data/risk_quadrant/` | exists |
| `outputs/exports/chart_data/sankey/` | exists |
| `outputs/exports/chart_data/boxplot/` | exists |
| `outputs/exports/chart_data/structure/` | exists |
| `outputs/dashboards/` | exists |
| `outputs/archive/` | exists |

Дополнительно обнаружены уже созданные подпапки:

- `outputs/dashboards/monthly/`
- `outputs/dashboards/semantic_layer/`
- `outputs/exports/technical/`
- `outputs/exports/technical/review_required/`
- `outputs/archive/review_required/`

## 5. Прямое сохранение в outputs/exports

Контракт: новые файлы не должны сохраняться напрямую в корень `outputs/exports/`; они должны попадать в целевые подпапки:

- `outputs/exports/analytical_csv/`
- `outputs/exports/chart_data/...`
- `outputs/exports/technical/...`
- `outputs/reports/...` для XLSX-отчетов.

Проверка кода генераторов не выявила активного сохранения новых отчетных таблиц или chart data напрямую в `outputs/exports/`. В ходе baseline-проверки были найдены legacy-артефакты в корне `outputs/exports/`; они перенесены в целевые папки новой структуры:

| Файл | Статус | Комментарий |
|---|---|---|
| `outputs/exports/monthly_metrics_year_cumulative_2026-01-01_retrospective_6.csv` | moved | Перенесен в `outputs/exports/analytical_csv/monthly_metrics_year_cumulative_2026-01-01_retrospective_6.csv`. |
| `outputs/exports/monthly_metrics_year_cumulative_2026-01-01_retrospective_6.xlsx` | moved | Перенесен в `outputs/reports/monthly_tables/monthly_metrics_year_cumulative_2026-01-01_retrospective_6.xlsx`. |

Текущее состояние: в корне `outputs/exports/` файлов не осталось.

## Вывод

Базовый контракт модернизации по `aggregation-mode`, `report_params.py`, `period_filter.py` и структуре `outputs/` подтвержден. Повторно внедрять эти блоки не требуется.

Ранее найденное эксплуатационное замечание по legacy-файлам в корне `outputs/exports/` устранено переносом файлов в новую структуру outputs.
