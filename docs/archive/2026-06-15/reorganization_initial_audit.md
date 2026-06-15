# Первичный аудит перед реорганизацией docs, scripts и outputs/charts

Дата аудита: 2026-05-26.

Цель: зафиксировать текущее состояние проекта после второй модернизации перед созданием maintenance-скриптов для реорганизации. На этом шаге файлы не переносились и не удалялись.

## Проверенные папки

| Папка | Состояние | Комментарий |
|---|---|---|
| `docs/` | 43 markdown-файла в корне и папка `docs/archive/` | В корне смешаны эксплуатационная документация, отчеты QA, отчеты миграций, baseline-документы и диагностические артефакты. |
| `scripts/` | 36 Python-файлов | Основные pipeline-скрипты остаются в корне `scripts/`; физически переносить их на этом этапе нельзя. |
| `outputs/charts/` | 40 HTML-графиков, суммарно около 195 МБ | В одной папке лежат все семейства графиков: основные, monthly, Sankey, risk/scatter, revenue и yield boxplot. |

## 1. Типы документов в docs

### Эксплуатационная документация проекта

Эти документы нужны для дальнейшего использования pipeline и должны оставаться доступными в корне `docs/` либо в понятной постоянной структуре:

- `analytical_architecture.md`
- `analytical_tables_report.md`
- `analytical_tables_limitations.md`
- `chart_build_limitations.md`
- `dashboard_architecture.md`
- `dashboard_exports_report.md`
- `dashboard_exports_limitations.md`
- `dashboard_semantic_model_v2.md`
- `data_audit.md`
- `data_cleaning_report.md`
- `executive_summary.md`
- `executive_summary_report.md`
- `feature_engineering.md`
- `final_project_summary.md`
- `kpi_map.md`
- `monthly_analytics_report.md`
- `monthly_visualization_strategy.md`
- `outputs_structure.md`
- `period_selection_report.md`
- `project_inventory.md`
- `revenue_analytics_report.md`
- `revenue_charts_report.md`
- `revenue_kpi_map.md`
- `self_review.md`
- `visualization_strategy.md`

### QA, проверки и контроль воспроизводимости

Эти документы актуальны как следы качества, но часть из них может быть перенесена в отдельный раздел `docs/quality/` или архивирована после подтверждения:

- `anomaly_tests_report.md`
- `boxplot_diagnostics.md`
- `manual_checks_log.md`
- `quality_gate_report.md`
- `raw_data_registry_report.md`
- `run_manifest_report.md`
- `schema_validation_report.md`
- `visual_regression_report.md`

### Baseline и modernization status

Эти документы полезны для истории модернизаций, но не обязательно должны лежать в корне `docs/` постоянно:

- `current_modernization_baseline.md`
- `second_modernization_baseline.md`

### Миграции, cleanup и промежуточные отчеты

Эти файлы явно похожи на кандидатов для архива или отдельной maintenance-папки:

- `docs_cleanup_report.md`
- `outputs_reorganization_report.md`
- `outputs_structure_migration_report.md`
- `reproducibility_review_stages_1_3.md`

### Диагностические точечные отчеты

Кандидаты на архивирование после проверки, что информация уже отражена в основных документах:

- `bid_to_cover_outliers.md`

## 2. Типы скриптов в scripts

### Основные этапы pipeline

Нумерованные скрипты формируют ядро проекта. На этом этапе их физически переносить нельзя:

- `01_data_audit.py`
- `02_data_cleaning.py`
- `03_feature_engineering.py`
- `04_kpi_map.py`
- `05_visualization_strategy.py`
- `06_build_charts.py`
- `07_dashboard_exports.py`
- `08_analytical_tables.py`
- `09_monthly_analytics.py`
- `10_build_monthly_charts.py`
- `11_revenue_analytics.py`
- `12_build_revenue_charts.py`

### Оркестрация и пользовательский запуск

- `run_pipeline.py`
- `interactive_pipeline.py`

### Параметры, конфигурация и общие модули

- `config.py`
- `report_params.py`
- `utils.py`
- `palette.py`
- `scatter_chart_policy.py`
- `__init__.py`

### Проверки качества и регрессии

- `schema_validation.py`
- `regression_tests.py`
- `smoke_tests.py`
- `html_chart_qa.py`
- `visual_regression.py`
- `quality_gate.py`
- `anomaly_tests.py`

### Dashboard, semantic layer и executive reporting

- `build_semantic_model_v2.py`
- `generate_executive_summary.py`

### Maintenance и служебные операции

- `cleanup_docs.py`
- `compare_outputs.py`
- `migrate_outputs_structure.py`
- `raw_data_registry.py`
- `reorganize_outputs.py`
- `run_manifest.py`

Вывод: `scripts/` уже содержит логически разные классы скриптов, но физический перенос основных Python-скриптов сейчас запрещен. На следующем шаге можно создать документацию или manifest-карту скриптов, а не переносить сами файлы.

## 3. Семейства HTML-графиков в outputs/charts

В `outputs/charts/` обнаружены следующие семейства графиков:

| Семейство | Количество | Назначение |
|---|---:|---|
| `placement_volume` | 1 | Объем размещения ОФЗ по номиналу. |
| `demand_supply` | 1 | Спрос и предложение. |
| `bid_to_cover` | 1 | Покрытие предложения спросом. |
| `yield_by_type` | 1 | Доходность по видам ОФЗ. |
| `yield_boxplot_by_ofz_type` | 1 | Boxplot доходности по видам ОФЗ. |
| `yield_boxplot_ofz_pd` | 1 | Отдельный boxplot по ОФЗ-ПД. |
| `yield_vs_demand` | 1 | Scatter доходности и спроса. |
| `demand_cutoff_explanation` | 1 | Отсечение спроса через кратность спроса, дисконт и доходность. |
| `discount_vs_demand` | 3 | Основная, log-X и outliers версии dense scatter. |
| `risk_quadrant` | 6 | Основной, ретроспективный, facet/log/outliers и квартальная детализация. |
| `format_structure` | 1 | Структура размещений по форматам. |
| `maturity_structure` | 1 | Структура размещений по срокам. |
| `sankey` | 5 | Sankey-структуры по периодам, видам, срокам и форматам. |
| `monthly_*` | 10 | Помесячные графики, включая размещение, накопленный итог, спрос/предложение, bid-cover, доходность, структуры, heatmap и revenue. |
| `revenue_*`, `nominal_revenue_*`, `discount_vs_revenue_gap` | 8 | Графики аналитики выручки и разницы номинала/выручки. |

Текущая папка содержит только актуальный набор для параметров `month`, `cumulative`, `2026-05-01`, `retrospective_4`. Старые HTML-графики в этой папке по результатам просмотра не обнаружены.

## 4. Файлы, явно требующие архивирования или ручной проверки

### Кандидаты на архивирование

Эти документы выглядят промежуточными или относящимися к предыдущим cleanup/migration шагам:

| Файл | Причина | Предварительное решение |
|---|---|---|
| `docs_cleanup_report.md` | Отчет предыдущей уборки `docs/`. | `archive_candidate` |
| `outputs_reorganization_report.md` | Отчет предыдущей реорганизации outputs. | `archive_candidate` |
| `outputs_structure_migration_report.md` | Большой отчет миграции структуры outputs. | `archive_candidate` |
| `reproducibility_review_stages_1_3.md` | Старый отчет воспроизводимости ранних этапов. | `archive_candidate` |
| `bid_to_cover_outliers.md` | Точечный диагностический отчет; вероятно уже покрыт QA/anomaly docs. | `review_required` |

### Требуют ручной проверки перед архивированием

| Файл | Почему не архивировать автоматически |
|---|---|
| `current_modernization_baseline.md` | Может быть нужен как baseline первой модернизации. |
| `second_modernization_baseline.md` | Нужен как baseline второй модернизации. |
| `manual_checks_log.md` | Журнал ручных проверок может быть эксплуатационно важен. |
| `quality_gate_report.md` | Последний quality gate может понадобиться в корне до создания `docs/quality/`. |
| `visual_regression_report.md` | Важный QA-отчет второй модернизации. |
| `anomaly_tests_report.md` | Важный QA-отчет второй модернизации. |
| `boxplot_diagnostics.md` | Специализированная диагностика boxplot; можно переносить только после проверки актуальности. |

### Scripts

Файлы в `scripts/` на этом шаге не переносить. Возможные кандидаты на логическую группировку в будущем:

- maintenance: `cleanup_docs.py`, `migrate_outputs_structure.py`, `reorganize_outputs.py`, `compare_outputs.py`;
- QA: `schema_validation.py`, `regression_tests.py`, `smoke_tests.py`, `html_chart_qa.py`, `visual_regression.py`, `quality_gate.py`, `anomaly_tests.py`;
- orchestration: `run_pipeline.py`, `interactive_pipeline.py`, `run_manifest.py`.

Физический перенос может сломать импорты, CLI и `run_pipeline.py`, поэтому сейчас допустима только инвентаризация и создание будущих dry-run maintenance-скриптов.

### Charts

В `outputs/charts/` явных устаревших HTML-файлов не выявлено. Однако папка смешивает разные семейства графиков. Возможная будущая структура для dry-run:

- `outputs/charts/core/`
- `outputs/charts/risk/`
- `outputs/charts/sankey/`
- `outputs/charts/monthly/`
- `outputs/charts/revenue/`
- `outputs/charts/yield/`
- `outputs/charts/structure/`
- `outputs/charts/archive/`

На текущем шаге перенос HTML-графиков не выполнялся.

## Итог

1. `docs/` требует аккуратной реорганизации: отдельно эксплуатационные документы, QA-отчеты, baseline-документы, migration/cleanup history.
2. `scripts/` трогать физически нельзя; нужна только карта назначений и, возможно, будущая документация по группам скриптов.
3. `outputs/charts/` содержит актуальные графики, но без разделения по семействам.
4. Следующий безопасный шаг: создать maintenance-скрипты с `--dry-run` для `docs` и `outputs/charts`, которые сформируют подробные отчеты переноса без фактического перемещения.
