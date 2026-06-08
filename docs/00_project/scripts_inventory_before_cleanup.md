# Scripts inventory before cleanup

- generated_at: `2026-06-08`
- cleanup mode: `audit only`
- physical moves: `none`
- scope: `scripts/**/*.py`

Этот документ фиксирует P1-аудит `scripts/` перед возможной будущей структурной очисткой. На этом этапе Python-файлы физически не переносятся: текущие CLI-команды, imports, `run_pipeline.py`, editable entry points и ручные production-инструкции должны оставаться стабильными.

## Summary

| Категория | Количество |
|---|---:|
| Всего Python-файлов | 42 |
| `keep_active` | 32 |
| `refactor_candidate` | 5 |
| `archive_candidate` | 5 |
| `delete_candidate` | 0 |
| `unknown` для ручной проверки | 0 |

## No-touch active scripts

Эти файлы не переносить и не архивировать на production-cleanup этапе без отдельного migration plan и compatibility wrappers.

- `scripts/run_pipeline.py`
- `scripts/interactive_pipeline.py`
- `scripts/report_params.py`
- `scripts/period_filter.py`
- `scripts/config.py`
- `scripts/utils.py`
- `scripts/01_data_audit.py`
- `scripts/02_data_cleaning.py`
- `scripts/03_feature_engineering.py`
- `scripts/04_kpi_map.py`
- `scripts/05_visualization_strategy.py`
- `scripts/06_build_charts.py`
- `scripts/07_dashboard_exports.py`
- `scripts/08_analytical_tables.py`
- `scripts/09_monthly_analytics.py`
- `scripts/10_build_monthly_charts.py`
- `scripts/11_revenue_analytics.py`
- `scripts/12_build_revenue_charts.py`
- `scripts/generate_executive_summary.py`
- `scripts/build_semantic_model_v2.py`
- `scripts/run_manifest.py`
- `scripts/raw_data_registry.py`
- `scripts/quality_gate.py`
- `scripts/schema_validation.py`
- `scripts/html_chart_qa.py`
- `scripts/visual_regression.py`
- `scripts/smoke_tests.py`
- `scripts/regression_tests.py`
- `scripts/anomaly_tests.py`
- `scripts/palette.py`
- `scripts/scatter_chart_policy.py`
- `scripts/__init__.py`

## Refactor candidates

Эти файлы активны или полезны, но их стоит рассмотреть для будущей модульной декомпозиции. Сейчас не переносить.

- `scripts/06_build_charts.py` - очень крупный CLI/stage script; кандидат на разбиение на chart family modules.
- `scripts/html_chart_qa.py` - крупный QA script; кандидат на разделение контрактов по семействам графиков.
- `scripts/visual_regression.py` - крупный fallback QA script; кандидат на разделение Plotly JSON checks и screenshot backend.
- `scripts/10_build_monthly_charts.py` - крупный monthly chart builder; кандидат на разделение bar/line/heatmap/facet logic.
- `scripts/07_dashboard_exports.py` - крупный dashboard exporter; кандидат на выделение semantic/export helpers.

## Archive candidates

Эти файлы относятся к legacy/reorganization maintenance и не должны вызываться production pipeline. Архивирование допустимо только отдельным этапом после проверки ссылок в README/docs.

- `scripts/cleanup_docs.py` - legacy cleanup script для старой структуры docs; заменен production workflow `scripts/maintenance/cleanup_docs.py`.
- `scripts/migrate_outputs_structure.py` - одноразовая migration utility старой структуры outputs.
- `scripts/reorganize_outputs.py` - legacy reorganization utility для outputs/exports.
- `scripts/maintenance/migrate_legacy_docs_archive.py` - одноразовый перенос старого docs/archive.
- `scripts/maintenance/reorganize_docs.py` - reorganization utility предыдущего этапа; может оставаться как historical maintenance до финального archive decision.

## Unknown scripts for manual review

Нет. Все Python-файлы классифицированы как active, refactor candidate или archive candidate.

## Inventory

| Path | Size bytes | Назначение | Тип | Run pipeline | Quality gate | Imported by scripts | main() | argparse | Status | Reason |
|---|---:|---|---|---|---|---|---|---|---|---|
| `scripts/__init__.py` | 113 | Package marker для editable install и imports `scripts.*`. | library | no | no | yes | no | no | `keep_active` | Нужен для package layout и entry points. |
| `scripts/01_data_audit.py` | 24035 | Этап 1: аудит исходных Excel/CSV. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | Активный stage script, входит в `run_pipeline.py` и `quality_gate.py`. |
| `scripts/02_data_cleaning.py` | 24381 | Этап 2: очистка исходных данных. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | Активный stage script, входит в `run_pipeline.py` и `quality_gate.py`. |
| `scripts/03_feature_engineering.py` | 28534 | Этап 3: расчет признаков и KPI-полей. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | Активный stage script, входит в `run_pipeline.py` и `quality_gate.py`. |
| `scripts/04_kpi_map.py` | 17679 | Этап 5: карта KPI и методологический документ. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | Активный stage script, входит в `run_pipeline.py` и `quality_gate.py`. |
| `scripts/05_visualization_strategy.py` | 20365 | Этап 7: стратегия визуализаций. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | Активный stage script, входит в `run_pipeline.py` и `quality_gate.py`. |
| `scripts/06_build_charts.py` | 339363 | Основные HTML-графики, risk/scatter/structure/format terms. | CLI entry | yes | py_compile | yes | yes | no | `refactor_candidate` | Активный stage script, но самый крупный файл; будущая декомпозиция желательна без физического переноса сейчас. |
| `scripts/07_dashboard_exports.py` | 70630 | Dashboard-ready exports и связанные документы. | CLI entry | yes | py_compile | yes | yes | no | `refactor_candidate` | Активный stage script; размер и semantic/export mix делают его кандидатом на декомпозицию. |
| `scripts/08_analytical_tables.py` | 32701 | Обязательные аналитические таблицы и CSV. | CLI entry | yes | no | yes | yes | no | `keep_active` | Активный stage script, вызывается pipeline. |
| `scripts/09_monthly_analytics.py` | 29397 | Monthly metrics layer. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | Активный monthly stage script. |
| `scripts/10_build_monthly_charts.py` | 87172 | Monthly HTML-графики, facet/heatmap/monthly chart data. | CLI entry | yes | py_compile | yes | yes | no | `refactor_candidate` | Активный monthly stage script; размер и разные chart families требуют будущей модульной декомпозиции. |
| `scripts/11_revenue_analytics.py` | 18592 | Revenue analytics tables. | CLI entry | yes | no | yes | yes | no | `keep_active` | Активный revenue stage script. |
| `scripts/12_build_revenue_charts.py` | 32785 | Revenue charts. | CLI entry | yes | no | yes | yes | no | `keep_active` | Активный revenue chart stage script. |
| `scripts/anomaly_tests.py` | 19269 | Проверки аномалий данных. | quality | yes | optional/runtime | yes | yes | no | `keep_active` | Активный QA script, вызывается pipeline stage и quality gate при наличии. |
| `scripts/build_semantic_model_v2.py` | 21512 | Dashboard semantic model v2. | CLI entry | yes | no | yes | yes | no | `keep_active` | Активный stage script для semantic model v2. |
| `scripts/cleanup_docs.py` | 12243 | Legacy cleanup docs для старой корневой структуры docs. | maintenance | no | no | no | yes | no | `archive_candidate` | Заменен `scripts/maintenance/cleanup_docs.py`; не запускать в production cleanup без отдельного решения. |
| `scripts/compare_outputs.py` | 7752 | Сравнение main/repro outputs для safe/compare режима. | quality | yes | no | yes | yes | yes | `keep_active` | Используется `run_pipeline.py` при `--safe`/`--compare`. |
| `scripts/config.py` | 22450 | Централизованные пути, docs routing, chart routing. | library | no | import | yes | no | no | `keep_active` | Базовая library для большинства scripts; no-touch. |
| `scripts/generate_executive_summary.py` | 34298 | Executive summary по расчетным показателям. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | Активный stage script, входит в `run_pipeline.py` и `quality_gate.py`. |
| `scripts/html_chart_qa.py` | 113969 | HTML/Plotly QA контракт графиков. | quality | no | runtime | yes | yes | yes | `refactor_candidate` | Активный QA script, вызывается quality gate; крупный файл для будущего разбиения по контрактам. |
| `scripts/interactive_pipeline.py` | 16519 | Интерактивный launcher с cleanup pre-flight. | CLI entry | no | no | entry point | yes | no | `keep_active` | Активный CLI entry point `ofz-interactive`; no-touch. |
| `scripts/maintenance/__init__.py` | 83 | Package marker для maintenance entry points. | library | no | no | yes | no | no | `keep_active` | Нужен для `scripts.maintenance.*` imports и entry points. |
| `scripts/maintenance/cleanup_docs.py` | 18528 | Inventory-first docs cleanup workflow. | maintenance | no | no | no | yes | yes | `keep_active` | Новый production maintenance script; dry-run/archive/delete-archived modes. |
| `scripts/maintenance/cleanup_outputs.py` | 11917 | Safe outputs cleanup. | maintenance | no | entry/help | yes | yes | yes | `keep_active` | Активный maintenance CLI, используется interactive launcher и entry point `ofz-clean-outputs`. |
| `scripts/maintenance/migrate_legacy_docs_archive.py` | 8578 | Миграция старого docs/archive в новую структуру. | maintenance | no | no | no | yes | yes | `archive_candidate` | Одноразовая legacy migration utility; оставить до отдельного archive decision. |
| `scripts/maintenance/reorganize_charts.py` | 16627 | Dry-run/apply реорганизация HTML charts. | maintenance | no | no | no | yes | yes | `keep_active` | Полезный maintenance script для chart routing cleanup; оставлен активным. |
| `scripts/maintenance/reorganize_docs.py` | 12059 | Dry-run/apply реорганизация markdown docs. | maintenance | no | no | no | yes | yes | `archive_candidate` | Исторический reorganization utility; новый production cleanup workflow теперь в `maintenance/cleanup_docs.py`. |
| `scripts/migrate_outputs_structure.py` | 10185 | Legacy migration структуры outputs. | maintenance | no | no | no | yes | no | `archive_candidate` | Одноразовый migration script; production pipeline не вызывает. |
| `scripts/palette.py` | 3508 | Цветовые палитры и semantic colors. | library | no | py_compile | yes | no | no | `keep_active` | Активная library для chart builders и QA; входит в `quality_gate.py` key scripts. |
| `scripts/period_filter.py` | 9650 | Report scope dataset по параметрам периода. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | Активный stage script, входит в `run_pipeline.py` и `quality_gate.py`. |
| `scripts/quality_gate.py` | 26751 | Единый fast/full quality gate. | quality | yes | entry | yes | yes | yes | `keep_active` | Активный QA entry point, также pipeline stage. |
| `scripts/raw_data_registry.py` | 7878 | Raw data registry и hashes без изменения `data/raw`. | CLI entry | no | py_compile | yes | yes | no | `keep_active` | Активный metadata/QA helper, входит в key scripts quality gate. |
| `scripts/regression_tests.py` | 14573 | Regression tests для периодной логики и edge cases. | quality | no | runtime | yes | yes | no | `keep_active` | Активный QA script, вызывается quality gate. |
| `scripts/reorganize_outputs.py` | 12354 | Legacy reorganization outputs/exports. | maintenance | no | no | no | yes | yes | `archive_candidate` | Исторический utility после реорганизации outputs; не production path. |
| `scripts/report_params.py` | 14134 | Параметры отчетных периодов и CLI parser helpers. | library | no | py_compile | yes | no | yes | `keep_active` | Центральная library для pipeline, QA и chart scripts. |
| `scripts/run_manifest.py` | 25454 | Run manifest JSON/MD/latest. | CLI entry | yes | py_compile | yes | yes | yes | `keep_active` | Активный metadata stage и entry point. |
| `scripts/run_pipeline.py` | 27605 | Основной оркестратор pipeline. | CLI entry | entry | py_compile | entry point | yes | yes | `keep_active` | Главный production entry point; no-touch. |
| `scripts/scatter_chart_policy.py` | 6866 | Scatter label policy и constants. | library | no | py_compile | yes | no | no | `keep_active` | Активная library для scatter charts и QA. |
| `scripts/schema_validation.py` | 20357 | Schema validation и chart data contracts. | quality | no | runtime/entry | yes | yes | no | `keep_active` | Активный QA entry point `ofz-schema`, вызывается quality gate. |
| `scripts/smoke_tests.py` | 11825 | Smoke tests для pipeline artifacts и contracts. | quality | no | runtime | yes | yes | yes | `keep_active` | Активный QA script, вызывается quality gate. |
| `scripts/utils.py` | 12306 | Общие utilities: markdown, logging, formatting, filesystem helpers. | library | no | import | yes | no | no | `keep_active` | Базовая shared library; no-touch. |
| `scripts/visual_regression.py` | 58785 | Visual regression / fallback Plotly JSON inspection. | quality | no | runtime | yes | yes | yes | `refactor_candidate` | Активный QA script, вызывается quality gate; кандидат на разбиение backend/check modules. |

## Notes

- `run_pipeline.py` вызывает stage scripts через `STAGE_SPECS`; физический перенос active scripts сейчас запрещен.
- `quality_gate.py` использует `KEY_SCRIPTS` для py_compile и запускает runtime QA scripts (`schema_validation.py`, `regression_tests.py`, `smoke_tests.py`, `html_chart_qa.py`, `visual_regression.py`, `anomaly_tests.py` при наличии).
- `scripts/maintenance/cleanup_docs.py` создан как новый production-safe workflow. Старый `scripts/cleanup_docs.py` остается только archive candidate до отдельного решения.
- `delete_candidate` намеренно не выставлялся: на P1-аудите достаточно inventory и будущего archive plan.
