# Scripts Structure Plan

Документ фиксирует текущую логическую структуру папки `scripts/` после второй модернизации проекта OFZ_ANALITICS. Физический перенос основных скриптов сейчас не выполняется: действующие CLI-команды, импорты и `run_pipeline.py` сохраняют обратную совместимость.

## Pipeline

- `run_pipeline.py` — основной оркестратор этапов pipeline.
- `interactive_pipeline.py` — интерактивный launcher для выбора параметров запуска.
- `report_params.py` — расчет отчетных периодов, ретроспективы и `aggregation_mode`.
- `period_filter.py` — формирование `data/processed/ofz_auctions_report_scope.csv`.

## Stages

- `01_data_audit.py` — аудит исходных файлов.
- `02_data_cleaning.py` — очистка и нормализация данных.
- `03_feature_engineering.py` — расчет признаков, сроковых категорий и ratio-показателей.
- `04_kpi_map.py` — карта KPI.
- `05_visualization_strategy.py` — методология визуализаций.
- `06_build_charts.py` — основные HTML-графики.
- `07_dashboard_exports.py` — dashboard-ready exports.
- `08_analytical_tables.py` — обязательные аналитические таблицы.
- `09_monthly_analytics.py` — monthly layer.
- `10_build_monthly_charts.py` — помесячные визуализации.
- `11_revenue_analytics.py` — аналитика выручки.
- `12_build_revenue_charts.py` — графики по выручке.
- `generate_executive_summary.py` — параметризуемое executive summary.
- `build_semantic_model_v2.py` — semantic model v2.

## QA

- `quality_gate.py` — единый quality gate.
- `schema_validation.py` — проверка схемы и контрактов данных.
- `regression_tests.py` — регрессионные тесты периодной логики и edge cases.
- `smoke_tests.py` — smoke tests ключевых outputs.
- `html_chart_qa.py` — QA HTML-графиков.
- `visual_regression.py` — visual regression или fallback HTML/Plotly inspection.
- `anomaly_tests.py` — проверки аномалий данных.

## Metadata

- `run_manifest.py` — run manifest.
- `raw_data_registry.py` — registry исходных файлов без изменения `data/raw/`.

## Utils

- `config.py` — централизованные пути, `get_doc_path()` и `chart_html_dir_for_name()`.
- `utils.py` — общие функции чтения, записи, логирования и нормализации.
- `palette.py` — цветовые палитры.
- `scatter_chart_policy.py` — политика подписей scatter-графиков.
- `compare_outputs.py` — сравнение outputs.
- `__init__.py` — пакетная инициализация `scripts`.

## Maintenance

- `archive/2026-06-15/cleanup_docs.py` — legacy-очистка docs.
- `archive/2026-06-15/reorganize_outputs.py` — реорганизация outputs/exports.
- `archive/2026-06-15/migrate_outputs_structure.py` — миграция структуры outputs.
- `archive/2026-06-15/reorganize_docs.py` — безопасная реорганизация docs.
- `maintenance/reorganize_charts.py` — безопасная реорганизация HTML-графиков.
- `archive/2026-06-15/migrate_legacy_docs_archive.py` — перенос старого `docs/archive/`.
- `maintenance/__init__.py` — пакетная инициализация maintenance.

