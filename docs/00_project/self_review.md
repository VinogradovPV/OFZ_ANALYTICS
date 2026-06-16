# Self-review проекта

Дата формирования: `2026-05-19`.

Первая модернизация проекта завершена полностью. Текущий self-review дополнен проверками второй модернизации: quality gate, visual regression/fallback inspection, anomaly tests, run manifest, semantic model v2, revenue analytics и revenue charts. Уже стабилизированные блоки первой модернизации не переписывались повторно.

Проверка выполнена как статический self-review структуры проекта, кода, документации и созданных артефактов. Python-скрипты в ходе проверки не запускались.

## Итоговый статус

| Область | Статус | Основание | Остаточный риск |
| --- | --- | --- | --- |
| Python-first pipeline | ok | Основные этапы реализованы Python-скриптами в `scripts/`; `run_pipeline.py` оркестрирует этапы. | Runtime должен подтверждаться ручным запуском проектного Python. |
| Pylance-friendly код | partial | В новых/ключевых скриптах используются `pathlib`, type hints, явные функции и проверки колонок. | Нужна IDE-проверка Pylance после последних правок. |
| Русификация | ok | Документация, логи, названия этапов, подписи графиков и hover-тексты преимущественно на русском языке. | Технические имена колонок сохраняются как контрактные поля datasets. |
| CLI `--stages 1 2 3` | ok | `scripts/run_pipeline.py` использует `nargs="+"` и поддерживает пример `--stages 1 2 3`. | Нужна ручная runtime-проверка. |
| `run_pipeline.py --all` | ok | `ALL_STAGES` включает `1, 2, 3, 4, 5, 6, 7, 8, 8.1, 9, 9.1, 10`. | Полный запуск зависит от наличия report scope и доступности XLSX-файлов. |
| `data/raw/` | ok | Workflow не требует изменения исходных файлов; скрипты читают raw/processed данные и пишут в `data/processed`, `docs`, `outputs`, `logs`. | В self-review не выполнялась проверка хэшей raw-файлов. |

## Pipeline Рё CLI

| Проверка | Статус | Комментарий |
| --- | --- | --- |
| Есть `scripts/run_pipeline.py` | ok | Оркестратор существует. |
| Есть параметры `--stage`, `--stages`, `--all` | ok | Поддержаны одиночный, множественный и полный запуск. |
| Есть параметры отчета `--report-date`, `--retrospective-years`, `--period-type` | ok | Передаются в параметризуемые этапы. |
| Есть `--safe`, `--compare` | ok | Поддержка safe/repro логики для ранних этапов сохранена. |
| Stage 4 создается до downstream-этапов | ok | Этапы, которым нужен report scope, отмечены как зависящие от `data/processed/ofz_auctions_report_scope.csv`. |
| Stage 8.1 запускает обязательные таблицы | ok | `scripts/08_analytical_tables.py` включен в workflow. |
| Stage 9.1 запускает dashboard exports | ok | `scripts/07_dashboard_exports.py` включен в `--all`. |

## Данные и признаки

| Проверка | Статус | Комментарий |
| --- | --- | --- |
| Источник Этапа 3 - cleaned dataset | ok | Feature engineering опирается на очищенный dataset. |
| Актуальная классификация сроков | ok | `short_term`: до 5 лет включительно; `medium_term`: свыше 5 и до 10 лет включительно; `long_term`: более 10 лет. |
| `maturity_years` | ok | Рассчитывается на основе срока до погашения. |
| `maturity_bucket` и `maturity_bucket_label` | ok | Используются в таблицах, графиках и dashboard exports. |
| Zero placement | ok | Ratio-показатели с размещением в знаменателе не должны рассчитываться при нулевом размещении; ограничение отражается в методологии. |
| `format` сохранен | ok | Формат размещения используется в cleaning, charts, dashboard exports. |
| `data_quality_flag` | ok | Используется для ограничений и фильтрации в аналитике. |

## Показатели спроса и покрытия

| Показатель | Формула | Статус | Комментарий |
| --- | --- | --- | --- |
| `demand_satisfaction_ratio` | `placement_volume / demand_volume` | ok | Коэффициент удовлетворения спроса; если есть исходное поле, оно сохраняется как приоритетное. |
| `demand_to_placement_ratio` | `demand_volume / placement_volume` | ok | Кратность спроса к фактическому размещению; не называется bid-to-cover. |
| `bid_to_cover_ratio` | `demand_volume / supply_volume` | ok | Классическое покрытие предложения спросом. |
| `ratio_basis` | текстовое описание расчетной базы | ok | Фиксирует методологию и проблемные знаменатели. |
| ДРПА в demand-based ratios | ok | Документировано ограничение: ДРПА без валидного спроса не должны механически включаться. |

## Обязательные таблицы

| Таблица | Файл | Статус | Проверка |
| --- | --- | --- | --- |
| Доходность по видам ОФЗ | `outputs/exports/ofz_yield_by_type_quarter_2026-04-01_retrospective_2.csv` | ok | Включает `placement_volume`, min/weighted avg/max yield и YoY-изменения. |
| Спрос и предложение | `outputs/exports/demand_supply_quarter_2026-04-01_retrospective_2.csv` | ok | Использует совокупный спрос и совокупное предложение. |
| Размещение по срокам обращения | `outputs/exports/placement_volume_by_maturity_quarter_2026-04-01_retrospective_2.csv` | ok | Использует `maturity_bucket` и доли в размещении. |
| XLSX-экспорт таблиц | `outputs/exports/*.xlsx` | ok | Есть XLSX для обязательных табличных отчетов; в коде предусмотрен fallback при `PermissionError`. |
| Документация таблиц | `docs/analytical_tables_report.md`, `docs/analytical_tables_limitations.md` | ok | Отчет и ограничения присутствуют. |

## Обязательные графики

| График | Файл | Статус | Комментарий |
| --- | --- | --- | --- |
| Объем размещения | `outputs/charts/placement_volume_quarter_2026-04-01_retrospective_2.html` | ok | Есть подписи данных. |
| Спрос и предложение | `outputs/charts/demand_supply_quarter_2026-04-01_retrospective_2.html` | ok | Русские подписи и легенда. |
| Покрытие предложения спросом | `outputs/charts/bid_to_cover_quarter_2026-04-01_retrospective_2.html` | ok | Методология: совокупный спрос / совокупное предложение. |
| Доходность по видам ОФЗ | `outputs/charts/yield_by_type_quarter_2026-04-01_retrospective_2.html` | ok | По видам бумаг. |
| Структура по срокам | `outputs/charts/maturity_structure_quarter_2026-04-01_retrospective_2.html` | ok | Использует актуальные buckets. |
| Форматы размещения | `outputs/charts/format_structure_quarter_2026-04-01_retrospective_2.html` | ok | Учитывает `format`. |
| Квадрант риска | `outputs/charts/risk_quadrant_quarter_2026-04-01_retrospective_2.html` | ok | Подписи и методология demand-to-placement уточнены. |
| Ретроспективный квадрант риска | `outputs/charts/risk_quadrant_retrospective_quarter_2026-04-01_retrospective_2.html` | ok | По умолчанию подписываются ключевые выбросы. |
| Квадрант риска отчетного года | `outputs/charts/risk_quadrant_demand_to_placement_by_quarter_quarter_2026-04-01_retrospective_2.html` | ok | Цвет по кварталам размещения; ограничение одного квартала документировано. |
| Boxplot доходности | `outputs/charts/yield_boxplot_by_ofz_type_quarter_2026-04-01_retrospective_2.html` | ok | Подписываются ключевые статистики boxplot. |
| Отсечение спроса | `outputs/charts/demand_cutoff_explanation_quarter_2026-04-01_retrospective_2.html` | ok | Только целевой отчетный период; X = спрос / размещение. |
| Sankey structure | `outputs/charts/sankey_structure_quarter_2026-04-01_retrospective_2.html` | ok | Ширина потоков соответствует `placement_volume`. |

## Подписи, hover и palette policy

| Проверка | Статус | Комментарий |
| --- | --- | --- |
| Подписи данных на базовых графиках | ok | Столбчатые, линейные и точечные графики используют подписи значений. |
| Подписи выбросов | ok | Risk/cutoff-графики подписывают ключевые наблюдения, а не все точки. |
| Boxplot-статистики | ok | Для групп показываются min/median/max/n; для малых `n` документированы ограничения. |
| Русский hover | ok | Ключевые hover-template используют русские названия показателей. |
| Контрастные цвета | ok | В `scripts/06_build_charts.py` заданы качественные, последовательные и контрастные последовательные палитры. |
| Легенды на русском | ok | Легенды и colorbar подписываются на русском, где график имеет легенду/colorbar. |

## Dashboard architecture Рё exports

| Проверка | Статус | Основание |
| --- | --- | --- |
| `docs/dashboard_architecture.md` | ok | Документ присутствует в корне `docs/`. |
| `scripts/07_dashboard_exports.py` | ok | Скрипт присутствует. |
| Auction-level export | ok | `outputs/dashboards/dashboard_auction_level_quarter_2026-04-01_retrospective_2.csv`. |
| Period summary export | ok | `outputs/dashboards/dashboard_period_summary_quarter_2026-04-01_retrospective_2.csv`. |
| KPI summary export | ok | `outputs/dashboards/dashboard_kpi_summary_quarter_2026-04-01_retrospective_2.csv`. |
| Maturity structure export | ok | `outputs/dashboards/dashboard_maturity_structure_quarter_2026-04-01_retrospective_2.csv`. |
| Yield distribution export | ok | `outputs/dashboards/dashboard_yield_distribution_quarter_2026-04-01_retrospective_2.csv`. |
| Demand/supply export | ok | `outputs/dashboards/dashboard_demand_supply_quarter_2026-04-01_retrospective_2.csv`. |
| Metadata JSON | ok | `outputs/dashboards/dashboard_metadata_quarter_2026-04-01_retrospective_2.json`. |
| Data dictionary | ok | `outputs/dashboards/dashboard_data_dictionary_quarter_2026-04-01_retrospective_2.csv`. |
| Dashboard exports documentation | ok | `docs/dashboard_exports_report.md`, `docs/dashboard_exports_limitations.md`. |

## Документация ограничений

| Документ | Статус | Что покрывает |
| --- | --- | --- |
| `docs/chart_build_limitations.md` | ok | Ограничения графиков, demand ratios, ДРПА, нулевого размещения, cutoff price, подписей. |
| `docs/analytical_tables_limitations.md` | ok | Ограничения обязательных таблиц, взвешивания доходности и доступности полей. |
| `docs/dashboard_exports_limitations.md` | ok | Ограничения dashboard-ready datasets. |
| `docs/kpi_map.md` | ok | Формулы KPI, включая различие `bid_to_cover_ratio`, `demand_to_placement_ratio`, `demand_satisfaction_ratio`. |
| `docs/visualization_strategy.md` | ok | Описание визуализаций и их управленческого смысла. |
| `docs/final_project_summary.md` | ok | Финальная структура workflow и dashboard exports. |

## Проверки, которые нужно выполнять вручную

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\run_pipeline.py
```

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\03_feature_engineering.py
```

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py
```

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\07_dashboard_exports.py
```

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\08_analytical_tables.py
```

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --stages 1 2 3 --safe
```

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Р’С‹РІРѕРґ

Проект можно считать методологически собранным для воспроизводимого Python-first pipeline: ранние этапы формируют cleaned/features/report scope, downstream-этапы используют report scope, обязательные таблицы и графики созданы, dashboard exports реализованы, ограничения документированы. Основной остаточный риск - необходимость регулярной ручной runtime-проверки проектным Python после правок кода и перед использованием результатов в отчетности.

## Проверка структуры outputs

- `scripts/config.py` содержит целевые директории `outputs/reports/`, `outputs/exports/analytical_csv/`, `outputs/exports/chart_data/`, `outputs/dashboards/` и `outputs/archive/`.
- `scripts/archive/2026-06-15/migrate_outputs_structure.py` подготовлен для безопасной миграции существующих файлов без удаления.
- `scripts/06_build_charts.py` сохраняет CSV-основы графиков в `outputs/exports/chart_data/`.
- `scripts/08_analytical_tables.py` сохраняет XLSX отчетных таблиц в `outputs/reports/analytical_tables/`, а CSV-копии в `outputs/exports/analytical_csv/`.
- `scripts/07_dashboard_exports.py` использует `outputs/dashboards/`.
- Документация структуры outputs находится в `docs/outputs_structure.md`.

## Outputs smoke checklist

- `scripts/smoke_tests.py` присутствует и должен проверять компиляцию ключевых scripts, запуск pipeline, наличие отчетных таблиц, charts, monthly outputs, dashboard exports и структуру outputs.
- `scripts/schema_validation.py` присутствует и должен проверять `aggregation_mode`, интервалы `report_period_start` / `report_period_end`, единственный target period, monthly layer, chart data exports, единицы `volume_bln` и отсутствие новых отчетных файлов напрямую в корне `outputs/exports/`.
- Smoke tests должны проверять наличие `outputs/reports/analytical_tables/`, `outputs/reports/monthly_tables/`, `outputs/exports/analytical_csv/`, `outputs/exports/chart_data/risk_quadrant/`, `outputs/exports/chart_data/sankey/`, `outputs/exports/chart_data/boxplot/`, `outputs/exports/chart_data/structure/`, `outputs/dashboards/`.
- После нового запуска pipeline нужно проверять, что отчетные `.xlsx` не попадают напрямую в корень `outputs/exports/`.

Рекомендуемые команды:

```powershell
.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

```powershell
.\.venv\Scripts\python.exe scripts\smoke_tests.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

```powershell
.\.venv\Scripts\python.exe scripts\html_chart_qa.py
```

## Проверка `aggregation_mode` и monthly layer

- Проверено требование поддержки `--aggregation-mode`.
- Допустимые значения: `cumulative` и `point`; default: `cumulative`.
- `month + cumulative + report_date=2026-05-01` должен означать январь-апрель 2026.
- `month + point + report_date=2026-05-01` должен означать только апрель 2026.
- `quarter + cumulative + report_date=2026-07-01` должен означать январь-июнь 2026.
- `quarter + point + report_date=2026-07-01` должен означать только II квартал 2026.
- `year` должен работать как завершенный год перед `report_date`.
- Ретроспектива должна сравнивать аналогичные интервалы прошлых лет.
- Outputs `cumulative` и `point` не должны смешиваться.
- Monthly layer должен объяснять состав накопленного итога.
- Перечень помесячных визуализаций должен включать объем размещения, накопленный объем, спрос/предложение, bid-to-cover, средневзвешенную доходность, структуру по форматам, структуру по срокам и heatmap месяц x год.

## Актуализация self-review на 2026-05-25

### Что не переписывалось

- Уже выполненная периодная агрегация `cumulative` / `point` не переписывалась.
- `period_filter.py` и структура папок `outputs/` не пересобирались заново; изменения в документации фиксируют текущий контракт и оставшиеся проверки.
- `data/raw/` не должен изменяться ни одним этапом pipeline.

### Какие проверки проведены или предусмотрены

- Проведена документальная сверка контрактов: `aggregation_mode`, period scope, новая структура outputs, dashboard exports, monthly layer, визуальные ограничения и KPI-формулы.
- Зафиксированы ручные команды для `py_compile` ключевых скриптов.
- Зафиксированы команды для `schema_validation.py`, `smoke_tests.py`, `regression_tests.py` и `html_chart_qa.py`.
- В документации отражены проверки HTML-графиков: русские подписи, отсутствие технического формата `M/B/k` на volume-графиках, Sankey subtitle, лимит подписей scatter-графиков, режимы boxplot.
- Для stacked structure charts документированы итоги столбцов, доли сегментов и новая палитра сроковых категорий.

### Оставшиеся ограничения

- Runtime-статус зависит от последнего ручного запуска проектным Python; документация не заменяет фактический запуск проверок.
- Старые HTML/CSV/XLSX outputs могут сохранять прежнюю методологию до повторной генерации pipeline.
- Некоторые проверки качества являются эвристическими: HTML QA не заменяет визуальный просмотр графиков в браузере.
- ДРПА остаются ограничением для demand-based ratios, если в источнике отсутствует валидный спрос.
- Для объяснения неудовлетворенного спроса нужен `cutoff_price` или `cutoff_yield`; без этих полей интерпретация ограничена.
- Нулевые или около-нулевые доходности требуют ручной проверки источника и `data_quality_flag`.

### Предложения по совершенствованию

- Собрать единый `quality_gate.py`, который будет запускать все проверки одним воспроизводимым сценарием.
- Добавить визуальную регрессию HTML-графиков через скриншоты и сравнение контрольных зон.
- Ввести run manifest с параметрами запуска, версиями scripts, sha256 raw files и списком outputs.
- Расширить тесты на аномалии: нулевое размещение, ДРПА, несостоявшиеся аукционы, пропуски доходности, выбросы bid-to-cover.
- Подготовить dashboard semantic model с версионированным словарем полей и KPI.

