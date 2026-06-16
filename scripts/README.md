# scripts/

Папка `scripts/` содержит Python-first pipeline проекта OFZ_ANALITICS: от чтения и нормализации исходных данных до построения графиков, аналитических таблиц, dashboard-ready exports и проверок качества.

## Почему скрипты пока не переносятся физически

Основные скрипты остаются в корне `scripts/`, чтобы не ломать существующие команды запуска, импорты, `run_pipeline.py`, README и ручные проверки. На текущем этапе выполнена логическая классификация и наведены правила размещения outputs/docs, но физическая миграция Python-модулей не проводится.

Если в будущем понадобится переносить скрипты по подпапкам, сначала нужен отдельный план миграции с dry-run, проверкой импортов и обратной совместимостью CLI.

## Логическая классификация

### Pipeline

- `run_pipeline.py` — основной оркестратор этапов.
- `interactive_pipeline.py` — интерактивный launcher для ручного выбора параметров.
- `report_params.py` — расчет отчетных периодов и `aggregation_mode`.
- `period_filter.py` — формирование `ofz_auctions_report_scope.csv`.

### Stages

- `01_data_audit.py` — аудит исходных файлов.
- `02_data_cleaning.py` — очистка данных.
- `03_feature_engineering.py` — расчет признаков и KPI-полей.
- `04_kpi_map.py` — карта KPI.
- `05_visualization_strategy.py` — методология визуализаций.
- `06_build_charts.py` — основные HTML-графики.
- `07_dashboard_exports.py` — dashboard-ready exports.
- `08_analytical_tables.py` — обязательные аналитические таблицы.
- `09_monthly_analytics.py` — monthly layer.
- `10_build_monthly_charts.py` — помесячные графики.
- `11_revenue_analytics.py` — аналитика выручки.
- `12_build_revenue_charts.py` — графики по выручке.
- `generate_executive_summary.py` — параметризуемое executive summary.
- `build_semantic_model_v2.py` — semantic model v2.

### QA

- `quality_gate.py` — единый quality gate.
- `schema_validation.py` — проверка схемы и контрактов данных.
- `regression_tests.py` — регрессионные тесты периодной логики и edge cases.
- `smoke_tests.py` — smoke tests pipeline outputs.
- `html_chart_qa.py` — QA HTML-графиков.
- `visual_regression.py` — visual regression или fallback HTML/Plotly inspection.
- `anomaly_tests.py` — проверки аномалий данных.

### Metadata

- `run_manifest.py` — run manifest.
- `raw_data_registry.py` — registry исходных файлов без изменения `data/raw/`.

### Utils

- `config.py` — централизованные пути и routing helper-функции.
- `utils.py` — общие функции чтения/записи, логирования и нормализации.
- `palette.py` — цветовые палитры.
- `scatter_chart_policy.py` — политика подписей scatter-графиков.
- `compare_outputs.py` — сравнение outputs.

### Maintenance

- `maintenance/cleanup_outputs.py` - production-safe cleanup generated outputs.
- `maintenance/cleanup_docs.py` - inventory-first docs cleanup workflow.
- `maintenance/build_release_bundle.py` - external release bundle builder.
- `maintenance/reorganize_charts.py` - HTML charts reorganization helper.
- `archive/2026-06-15/` - legacy maintenance scripts kept for audit only; do not use for production runs.

## Основные entry points

Полный запуск:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Интерактивный запуск:

```powershell
.\.venv\Scripts\python.exe scripts\interactive_pipeline.py
```

Quality gate:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Visual regression / fallback HTML inspection:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Run manifest:

```powershell
.\.venv\Scripts\python.exe scripts\run_manifest.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --stages all
```

## Правила для markdown-документов

Новые `.md`-документы нельзя сохранять напрямую в корень `docs/`. Единственное исключение: `docs/index.md`.

Используйте централизованный helper:

```python
from scripts import config

target_path = config.get_doc_path("quality_gate_report.md")
```

Документы должны попадать в тематические папки:

- `docs/00_project/`;
- `docs/01_methodology/`;
- `docs/02_data_pipeline/`;
- `docs/03_analytics/`;
- `docs/04_visualization/`;
- `docs/05_dashboard/`;
- `docs/06_quality/`;
- `docs/90_archive/`.

## Правила для HTML-графиков

Новые HTML-графики нельзя сохранять напрямую в корень `outputs/charts/`.

Используйте:

```python
html_dir = config.chart_html_dir_for_name(chart_name)
```

Индекс графиков поддерживается в `outputs/charts/index.md`.
