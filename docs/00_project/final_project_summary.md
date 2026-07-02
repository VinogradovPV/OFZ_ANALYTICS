# Финальный обзор проекта

Дата формирования: `2026-05-19`.

Первая модернизация проекта завершена полностью. Текущие дополнительные артефакты, проверки качества, semantic model v2, revenue analytics и связанные визуализации относятся ко второй модернизации и выполняются поверх уже стабилизированной базы без повторного внедрения периодной агрегации, `period_filter` и структуры `outputs`.

Проект реализует воспроизводимый Python-first pipeline аналитики размещений ОФЗ: от аудита исходных файлов и очистки данных до параметризуемого report scope, KPI, обязательных табличных отчетов, интерактивных графиков, dashboard-ready exports и executive summary.

## Workflow проекта

| Этап | Назначение | Основные артефакты |
| --- | --- | --- |
| Этап 1 | Аудит исходных данных | `scripts/01_data_audit.py`, `docs/data_audit.md` |
| Этап 2 | Очистка данных | `scripts/02_data_cleaning.py`, `data/processed/ofz_auctions_clean.csv`, `docs/data_cleaning_report.md` |
| Этап 3 | Feature engineering | `scripts/03_feature_engineering.py`, `data/processed/ofz_auctions_features.csv`, `docs/feature_engineering.md` |
| Этап 4 | Параметризуемый report scope | `scripts/period_filter.py`, `data/processed/ofz_auctions_report_scope.csv`, `docs/period_selection_report.md` |
| Этап 5 | KPI map | `scripts/04_kpi_map.py`, `docs/kpi_map.md` |
| Этап 6 | Analytical architecture | `docs/analytical_architecture.md` |
| Этап 7 | Visualization strategy | `scripts/05_visualization_strategy.py`, `docs/visualization_strategy.md` |
| Этап 8 | Chart implementation | `scripts/06_build_charts.py`, `outputs/charts/`, `outputs/exports/chart_data/`, `docs/chart_build_limitations.md` |
| Этап 8.1 | Обязательные аналитические таблицы | `scripts/08_analytical_tables.py`, XLSX в `outputs/reports/analytical_tables/` или `outputs/reports/monthly_tables/`, CSV в `outputs/exports/analytical_csv/` |
| Этап 9 | Dashboard architecture | `docs/dashboard_architecture.md` |
| Этап 9.1 | Dashboard exports | `scripts/07_dashboard_exports.py`, `outputs/dashboards/`, `docs/dashboard_exports_report.md` |
| Этап 10 | Executive summary | `docs/executive_summary.md` |
| Этап 11 | Self-review | `docs/self_review.md` |
| Этап 12 | Final project summary | `docs/final_project_summary.md` |

Аналитические таблицы `ofz_yield_by_type` и `placement_volume_by_maturity` упорядочены по отчетному периоду как основной оси сравнения: внутри периода строки сортируются соответственно по виду ОФЗ и методологическому порядку сроковых категорий.

Графики объема размещения приведены к единому докладному стандарту: показатель трактуется как объем размещения ОФЗ по номиналу, на визуализациях отображается в млрд рублей, а исходные значения в млн рублей сохраняются в таблицах-основах графиков.

## Созданные скрипты

- `scripts/01_data_audit.py`
- `scripts/02_data_cleaning.py`
- `scripts/03_feature_engineering.py`
- `scripts/04_kpi_map.py`
- `scripts/05_visualization_strategy.py`
- `scripts/06_build_charts.py`
- `scripts/07_dashboard_exports.py`
- `scripts/08_analytical_tables.py`
- `scripts/archive/2026-06-15/cleanup_docs.py`
- `scripts/compare_outputs.py`
- `scripts/config.py`
- `scripts/interactive_pipeline.py`
- `scripts/period_filter.py`
- `scripts/report_params.py`
- `scripts/run_pipeline.py`
- `scripts/utils.py`
- `scripts/__init__.py`

## Созданные документы

Активные документы в корне `docs/`:

- `docs/analytical_architecture.md`
- `docs/analytical_tables_limitations.md`
- `docs/analytical_tables_report.md`
- `docs/chart_build_limitations.md`
- `docs/dashboard_architecture.md`
- `docs/dashboard_exports_limitations.md`
- `docs/dashboard_exports_report.md`
- `docs/data_audit.md`
- `docs/data_cleaning_report.md`
- `docs/docs_cleanup_report.md`
- `docs/executive_summary.md`
- `docs/feature_engineering.md`
- `docs/final_project_summary.md`
- `docs/kpi_map.md`
- `docs/period_selection_report.md`
- `docs/project_inventory.md`
- `docs/self_review.md`
- `docs/visualization_strategy.md`

Промежуточные repro/status/sync/validation-документы перенесены в `docs/archive/` и не удалялись безвозвратно.

## Наборы данных

Исходные файлы в `data/raw/`:

- `INTERNET_Auction_Results_rus_2019_20191218.xlsx`
- `INTERNET_Auction_Results_rus_2020_20201223.xlsx`
- `INTERNET_Auction_Results_rus_2021_20211223.xlsx`
- `INTERNET_Auction_Results_rus_2022_20221222.xlsx`
- `INTERNET_Auction_Results_rus_2023_20231231.xlsx`
- `INTERNET_Auction_Results_rus_2024_20241231.xlsx`
- `INTERNET_Auction_Results_rus_2025_20251231.xlsx`
- `INTERNET_Auction_Results_rus_2026_20260507.xlsx`

Рабочие datasets в `data/processed/`:

- `ofz_auctions_clean.csv`
- `ofz_auctions_clean_repro.csv`
- `ofz_auctions_features.csv`
- `ofz_auctions_features_repro.csv`
- `ofz_auctions_report_scope.csv`

## Графики

Созданные HTML-графики в `outputs/charts/`:

- `placement_volume_quarter_2026-04-01_retrospective_2.html`
- `demand_supply_quarter_2026-04-01_retrospective_2.html`
- `bid_to_cover_quarter_2026-04-01_retrospective_2.html`
- `yield_by_type_quarter_2026-04-01_retrospective_2.html`
- `maturity_structure_quarter_2026-04-01_retrospective_2.html`
- `format_structure_quarter_2026-04-01_retrospective_2.html`
- `risk_quadrant_quarter_2026-04-01_retrospective_2.html`
- `risk_quadrant_retrospective_quarter_2026-04-01_retrospective_2.html`
- `risk_quadrant_demand_to_placement_by_quarter_quarter_2026-04-01_retrospective_2.html`
- `yield_boxplot_by_ofz_type_quarter_2026-04-01_retrospective_2.html`
- `demand_cutoff_explanation_quarter_2026-04-01_retrospective_2.html`
- `sankey_structure_quarter_2026-04-01_retrospective_2.html`
- `sankey_period_maturity_type_format_quarter_2026-04-01_retrospective_2.html`
- `sankey_period_format_type_maturity_quarter_2026-04-01_retrospective_2.html`
- `sankey_period_format_maturity_type_quarter_2026-04-01_retrospective_2.html`
- `sankey_target_period_quarter_2026-04-01_retrospective_2.html`

## Экспорты

Созданные аналитические CSV и chart-support exports:

- `bid_to_cover_quarter_2026-04-01_retrospective_2.csv`
- `demand_cutoff_explanation_quarter_2026-04-01_retrospective_2.csv`
- `demand_supply_quarter_2026-04-01_retrospective_2.csv`
- `demand_supply_quarter_2026-04-01_retrospective_2.xlsx`
- `format_structure_quarter_2026-04-01_retrospective_2.csv`
- `maturity_structure_quarter_2026-04-01_retrospective_2.csv`
- `ofz_yield_by_type_quarter_2026-04-01_retrospective_2.csv`
- `ofz_yield_by_type_quarter_2026-04-01_retrospective_2.xlsx`
- `placement_volume_by_maturity_quarter_2026-04-01_retrospective_2.csv`
- `placement_volume_by_maturity_quarter_2026-04-01_retrospective_2.xlsx`
- `placement_volume_quarter_2026-04-01_retrospective_2.csv`
- `risk_quadrant_demand_to_placement_by_quarter_quarter_2026-04-01_retrospective_2.csv`
- `risk_quadrant_quarter_2026-04-01_retrospective_2.csv`
- `risk_quadrant_retrospective_quarter_2026-04-01_retrospective_2.csv`
- `sankey_structure_flow_quarter_2026-04-01_retrospective_2.csv`
- `sankey_structure_quarter_2026-04-01_retrospective_2.csv`
- `sankey_period_maturity_type_format_quarter_2026-04-01_retrospective_2.csv`
- `sankey_period_format_type_maturity_quarter_2026-04-01_retrospective_2.csv`
- `sankey_period_format_maturity_type_quarter_2026-04-01_retrospective_2.csv`
- `sankey_target_period_structure_quarter_2026-04-01_retrospective_2.csv`
- `yield_boxplot_by_ofz_type_quarter_2026-04-01_retrospective_2.csv`
- `yield_by_type_quarter_2026-04-01_retrospective_2.csv`

Обязательные табличные отчеты:

- `ofz_yield_by_type_<period_type>_<report_date>_retrospective_<N>.csv/.xlsx`
- `demand_supply_<period_type>_<report_date>_retrospective_<N>.csv/.xlsx`
- `placement_volume_by_maturity_<period_type>_<report_date>_retrospective_<N>.csv/.xlsx`

## Dashboard exports

Созданные dashboard-ready files в `outputs/dashboards/`:

- `dashboard_auction_level_quarter_2026-04-01_retrospective_2.csv`
- `dashboard_period_summary_quarter_2026-04-01_retrospective_2.csv`
- `dashboard_kpi_summary_quarter_2026-04-01_retrospective_2.csv`
- `dashboard_maturity_structure_quarter_2026-04-01_retrospective_2.csv`
- `dashboard_yield_distribution_quarter_2026-04-01_retrospective_2.csv`
- `dashboard_demand_supply_quarter_2026-04-01_retrospective_2.csv`
- `dashboard_metadata_quarter_2026-04-01_retrospective_2.json`
- `dashboard_data_dictionary_quarter_2026-04-01_retrospective_2.csv`

Эти файлы предназначены для BI/dashboard-слоя: detail fact table, периодные KPI, KPI cards, maturity structure, yield distribution, demand/supply views, metadata и data dictionary.

## Команды запуска

Все команды выполняются из корня проекта локальным Python из `.venv`:

```powershell
.\.venv\Scripts\python.exe --version
```

Месячный отчет:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Квартальный отчет:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-07-01 --retrospective-years 4 --period-type quarter --aggregation-mode cumulative
```

Годовой отчет:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-01-01 --retrospective-years 5 --period-type year --aggregation-mode cumulative
```

Запуск только Этапов 1-3:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --stages 1 2 3 --safe
```

Запуск dashboard exports отдельно:

```powershell
.\.venv\Scripts\python.exe scripts\07_dashboard_exports.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Ключевые методологические правила

- `report-date` должен быть первым днем месяца.
- Для `period-type=quarter` допустимы только 1 января, 1 апреля, 1 июля, 1 октября.
- Для `period-type=year` допустимо только 1 января.
- Количество периодов сравнения равно `retrospective-years + 1`.
- `data/raw/` не изменяется pipeline.
- `format` сохраняется как отдельный признак и используется в отчетах, графиках и dashboard exports.
- Сроки классифицируются так: краткосрочные - до 5 лет включительно; среднесрочные - свыше 5 и до 10 лет включительно; долгосрочные - более 10 лет.
- `bid_to_cover_ratio = demand_volume / supply_volume`.
- `demand_to_placement_ratio = demand_volume / placement_volume`.
- `demand_satisfaction_ratio = placement_volume / demand_volume`.
- `demand_to_placement_ratio` не называется bid-to-cover.

## Известные ограничения

- Runtime-проверки должны выполняться вручную проектным Python, если sandbox не запускает `.venv`.
- ДРПА не должны механически включаться в demand-based ratios без проверки валидности спроса.
- Несостоявшиеся аукционы и строки с `placement_volume = 0` исключаются из ratio-графиков, где размещение стоит в знаменателе.
- Для анализа причин неудовлетворения спроса нужна `cutoff_price` или `cutoff_yield`; без них интерпретация дисконта ограничена.
- Неполные периоды, включая текущий год или квартал, требуют явной интерпретации в отчетах.
- XLSX-экспорт может быть заблокирован открытым файлом; для обязательных таблиц предусмотрен fallback с уникальным именем.
- Pylance-friendly статус требует регулярной проверки в IDE после изменений.
- Интерактивные HTML-графики требуют браузерной проверки читаемости подписей, легенд и colorbar.
- Промежуточные документы сохранены в `docs/archive/`; архив не удаляется автоматически.

## Рекомендуемые следующие улучшения

- Добавить automated smoke tests для `py_compile`, `--stages 1 2 3`, `period_filter`, charts, analytical tables и dashboard exports.
- Ввести schema validation для `ofz_auctions_clean.csv`, `ofz_auctions_features.csv` и `ofz_auctions_report_scope.csv`.
- Добавить контроль хэшей исходных файлов `data/raw/` и журнал версий raw-источников.
- Сформировать regression tests для спорных методологических кейсов: ДРПА, нулевое размещение, несостоявшийся аукцион, неполный период, выбросы bid-to-cover.
- Добавить HTML rendering QA для ключевых графиков: подписи, hover, легенды, colorbar, читаемость Sankey.
- Создать BI-ready semantic layer поверх dashboard exports: единые меры, русские названия, типы данных и форматирование.
- Добавить конфигурационный файл для palette policy, чтобы цвета были единообразны во всех графиках.
- Реализовать автоматическую генерацию executive summary на основе новых dashboard exports и обязательных таблиц.
- Добавить отдельный changelog проекта и журнал ручных проверок.

## Структура документации

Корень `docs/` оставлен для актуальных проектных документов pipeline. Промежуточные, repro, sync, status и validation-документы перенесены в `docs/archive/` (6 файлов). `docs/archive/` не удаляется автоматически и может быть проверен вручную перед окончательным удалением.

## Структура outputs

Актуальная целевая структура outputs описана в `docs/outputs_structure.md`.

- HTML-графики сохраняются в `outputs/charts/`.
- XLSX обязательных аналитических таблиц сохраняются в `outputs/reports/analytical_tables/`.
- CSV-копии обязательных аналитических таблиц сохраняются в `outputs/exports/analytical_csv/`.
- CSV-основы графиков сохраняются в `outputs/exports/chart_data/` с разбиением на `risk_quadrant/`, `sankey/`, `boxplot/` и `structure/`.
- Dashboard-ready exports сохраняются в `outputs/dashboards/`.
- Monthly dashboard exports сохраняются в `outputs/dashboards/monthly/`.
- Semantic layer для dashboard, если он формируется, сохраняется в `outputs/dashboards/semantic_layer/`.
- Dashboard exports не относятся к `outputs/reports/` и не смешиваются с `outputs/exports/chart_data/`.
- Неоднозначные и архивные outputs не удаляются автоматически; для них предусмотрены `outputs/exports/technical/review_required/` и `outputs/archive/`.

Безопасная миграция существующих outputs выполняется командой:

```powershell
.\.venv\Scripts\ofz-clean-outputs.exe --dry-run
```

## Smoke-проверки outputs

`scripts/smoke_tests.py` и `scripts/schema_validation.py` присутствуют и должны использоваться как регулярные проверки после регенерации outputs.

Smoke tests должны проверять наличие:

- `outputs/reports/analytical_tables/`
- `outputs/reports/monthly_tables/`
- `outputs/exports/analytical_csv/`
- `outputs/exports/chart_data/risk_quadrant/`
- `outputs/exports/chart_data/sankey/`
- `outputs/exports/chart_data/boxplot/`
- `outputs/exports/chart_data/structure/`
- `outputs/dashboards/`

После нового запуска pipeline нужно отдельно проверять, что отчетные `.xlsx` не сохраняются напрямую в корень `outputs/exports/`.

Рекомендуемые команды:

```powershell
.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

```powershell
.\.venv\Scripts\python.exe scripts\smoke_tests.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```
## Обновленная периодная методология

- Pipeline поддерживает параметр `--aggregation-mode`.
- Допустимые значения: `cumulative` и `point`.
- `cumulative` является default.
- `month + cumulative`: `report_date=2026-05-01` означает январь-апрель 2026.
- `month + point`: `report_date=2026-05-01` означает только апрель 2026.
- `quarter + cumulative`: `report_date=2026-07-01` означает январь-июнь 2026.
- `quarter + point`: `report_date=2026-07-01` означает только II квартал 2026.
- `year`: `report_date=2026-01-01` означает завершенный 2025 год.
- Ретроспектива сравнивает аналогичные интервалы прошлых лет.
- Outputs для `cumulative` и `point` не должны смешиваться; `aggregation_mode` включается в имена файлов.

## Monthly layer и помесячные визуализации

- `scripts/09_monthly_analytics.py` формирует `data/processed/ofz_monthly_metrics.csv`.
- Monthly layer объясняет состав накопленного итога: месячные показатели считаются за конкретный месяц, cumulative-поля - с января до текущего месяца включительно.
- `scripts/10_build_monthly_charts.py` строит помесячные визуализации:
  - помесячный объем размещения;
  - накопленный объем размещения;
  - помесячный спрос и предложение;
  - помесячный bid-to-cover;
  - помесячную средневзвешенную доходность;
  - структуру по форматам;
  - структуру по срокам;
  - heatmap месяц x год.
- Управленческий смысл monthly layer - показать, какие месяцы и факторы сформировали итоговый cumulative-результат.

## Стабилизация boxplot доходности

- График `yield_boxplot_by_ofz_type` разделяет короткую и длинную ретроспективу: до трех периодов используется grouped mode, при большем числе периодов используется `facet_by_ofz_type`.
- Для длинной ретроспективы каждая панель соответствует виду ОФЗ, а ось X показывает периоды в хронологическом порядке.
- Экспорт статистик boxplot сохраняется в `outputs/exports/chart_data/boxplot/` и содержит `report_period_start`, `report_period_display_label`, `report_period_order`, `ofz_type`, `n`, `min`, `q1`, `median`, `q3`, `max`, `lower_fence`, `upper_fence`, `has_outliers`, `outliers_count`.

- Отдельный график `yield_boxplot_ofz_pd` для короткого horizon использует fallback `jittered strip + summary ticks`, чтобы точки ОФЗ-ПД не схлопывались в одну вертикальную линию.

## Stacked structure charts

- Структурные stacked-графики по срокам, форматам и monthly-разрезам показывают итоговую сумму над столбцом при наличии двух и более сегментов.
- В chart data exports добавляются `column_total`, `segment_share_in_column` и `segment_share_total`, поэтому итог столбца можно восстановить из CSV.
- Для сроковой структуры используется порядок сегментов: долгосрочные, среднесрочные, краткосрочные, требует проверки.

## Актуализация финального состояния на 2026-05-25

- Реализован интерактивный и пакетный Python-first workflow: `scripts/run_pipeline.py` остается основным оркестратором, `scripts/interactive_pipeline.py` используется для ручного выбора параметров.
- Периодная агрегация `cumulative` / `point` уже реализована ранее и в этой актуализации не переписывалась.
- `scripts/generate_executive_summary.py` формирует управленческое резюме только на основании рассчитанных таблиц, monthly metrics, dashboard exports и chart data.
- Все новые отчетные артефакты должны сохраняться в профильные папки: XLSX в `outputs/reports/`, CSV отчетов в `outputs/exports/analytical_csv/`, основы графиков в `outputs/exports/chart_data/`, dashboard exports в `outputs/dashboards/`.
- Графики с объемами размещения приведены к единому стандарту: объем размещения по номиналу, млрд рублей.
- Для boxplot доходности используется адаптивная компоновка: grouped mode для короткой ретроспективы и facet mode по видам ОФЗ для длинной ретроспективы.
- Для stacked structure charts добавлены итоги столбцов, доли сегментов и контроль палитры.
- Для monthly bar/line charts добавлены выборочные подписи данных: столбцы подписываются при достаточной читаемости, line charts подписывают ключевые точки. Малые/перегруженные значения остаются в hover и CSV.
- Facet-графики приведены к правилу одного общего Y-axis title.
- Scatter-графики с bubble-size должны явно объяснять размер точки; если bubble-size не читается, используется fixed-size fallback, а объем размещения остается в hover.
- Добавлено семейство `yield_vs_discount`: main, facet и outliers для анализа связки `дисконт к номиналу` x `доходность`; размер точки - объем размещения по номиналу, reference lines - медианы дисконта и доходности.

## Рекомендуемые улучшения

- Добавить единый `quality_gate.py`, который последовательно запускает `py_compile`, `schema_validation.py`, `regression_tests.py`, `smoke_tests.py` и `html_chart_qa.py`.
- Ввести versioned run manifest: параметры запуска, список входных файлов, sha256 источников, список созданных outputs и статус проверок.
- Добавить визуальную регрессионную проверку HTML-графиков через скриншоты для контроля наложения подписей и легенд.
- Расширить semantic layer: формализовать бизнес-словарь показателей, единицы измерения и связи dashboard datasets.
- Добавить lineage до уровня строки: raw file / sheet / row -> cleaned row -> feature row -> report scope -> chart/table output.

## Вторая модернизация: revenue analytics

- Добавлен скрипт `scripts/11_revenue_analytics.py`.
- Скрипт формирует `revenue_summary_<...>.xlsx` в `outputs/reports/analytical_tables/` и CSV-версии в `outputs/exports/analytical_csv/`.
- Основной source mapping выручки: `revenue_volume = proceeds_mln_rub`, если каноническая колонка `revenue_volume` отсутствует.
- Рассчитываются `nominal_revenue_gap`, `revenue_to_nominal_ratio`, `nominal_discount_ratio`, а также срезы по виду ОФЗ, сроковой категории, формату и месяцам.
- Этап доступен в pipeline как `--stage revenue_analytics`; при `--all` запускается после обязательных аналитических таблиц.
- Добавлен скрипт `scripts/12_build_revenue_charts.py`.
- Revenue charts сохраняются в `outputs/charts/`, а CSV-основы - в `outputs/exports/chart_data/structure/`.
- Создаются графики `revenue_vs_nominal_by_period`, `nominal_revenue_gap_by_period`, `revenue_to_nominal_ratio`, `monthly_revenue_vs_nominal`, `monthly_nominal_revenue_gap`, `revenue_gap_by_ofz_type`, `revenue_gap_by_maturity`, `discount_vs_revenue_gap`.
- Этап доступен в pipeline как `--stage revenue_charts`; при `--all` запускается после `revenue_analytics`.
- Добавлен документ `docs/revenue_kpi_map.md` с формулами `placement_volume`, `revenue_volume`, `nominal_revenue_gap`, `revenue_to_nominal_ratio` и `nominal_discount_ratio`.
- Методическое ограничение: если выручка отсутствует или неполна, проект не выдумывает значения и фиксирует ограничение через `data_quality_flag`.
# Update 2026-06-02: format_nominal_revenue_gap

- Добавлен график `format_nominal_revenue_gap_<...>.html`: grouped bar по форматам размещения, где Y = `nominal_revenue_gap_bln`.
- HTML сохраняется в `outputs/charts/revenue/gap/`.
- CSV-основа сохраняется в `outputs/exports/chart_data/revenue/`.
- Revenue chart data exports теперь маршрутизируются в `outputs/exports/chart_data/revenue/`.
# Update 2026-06-04: format, discount and revenue visualization contracts

- `format_structure_*` описан как stacked bar по форматам размещения: сегменты показывают `placement_volume_bln`, total label выводится над столбцом, а `label_visible` управляет видимостью подписей сегментов.
- `format_discount_*` актуализирован как grouped bar средневзвешенного дисконта к номиналу по форматам; ось Y = `Средневзвешенный дисконт к номиналу, п.п.`.
- `format_nominal_revenue_gap_*` показывает денежную разницу `placement_volume_bln - revenue_volume_bln` по форматам размещения.
- `monthly_heatmap_revenue_*` добавлен в описание monthly heatmap: колонка `Итого` является справочной и не участвует в основной цветовой шкале.
- `format_terms_comparison_*` сравнивает форматы по доходности, дисконту, `revenue_to_nominal_ratio` и `nominal_revenue_gap_bln`; в hover и подписях используется `placement_count`.
- `format_terms_scatter_*` показывает отдельные размещения: цвет = формат, форма = вид ОФЗ, размер = объем размещения по номиналу.
- Ограничения по отсутствующим `discount_to_nominal` и `revenue_volume` закреплены: значения не выдумываются, строки получают `data_quality_flag`, а неполные графики/элементы должны интерпретироваться с учетом качества данных.
