# Инвентаризация проекта

Дата обновления: `2026-05-20 11:45:21`.

Инвентаризация обновлена после безопасной очистки `docs/`. `data/raw/` не изменялся.

## Актуальная структура docs/

| Файл | Статус | Назначение |
| --- | --- | --- |
| docs/analytical_architecture.md | keep | Актуальный проектный документ. |
| docs/analytical_tables_limitations.md | keep | Актуальный проектный документ. |
| docs/analytical_tables_report.md | keep | Актуальный проектный документ. |
| docs/chart_build_limitations.md | keep | Актуальный проектный документ. |
| docs/dashboard_architecture.md | keep | Актуальный проектный документ. |
| docs/dashboard_exports_limitations.md | keep | Актуальный проектный документ. |
| docs/dashboard_exports_report.md | keep | Актуальный проектный документ. |
| docs/data_audit.md | keep | Актуальный проектный документ. |
| docs/data_cleaning_report.md | keep | Актуальный проектный документ. |
| docs/docs_cleanup_report.md | keep | Отчет о классификации и переносе промежуточных документов. |
| docs/executive_summary.md | keep | Актуальный проектный документ. |
| docs/feature_engineering.md | keep | Актуальный проектный документ. |
| docs/final_project_summary.md | keep | Актуальный проектный документ. |
| docs/kpi_map.md | keep | Актуальный проектный документ. |
| docs/period_selection_report.md | keep | Актуальный проектный документ. |
| docs/project_inventory.md | keep | Актуальный проектный документ. |
| docs/self_review.md | keep | Актуальный проектный документ. |
| docs/visualization_strategy.md | keep | Актуальный проектный документ. |

## Архивированные документы

- `docs/archive/bid_to_cover_outliers.md` (archived_now)
- `docs/archive/bid_to_cover_outliers_20260520_114521.md` (archived)
- `docs/archive/current_stage_status_after_1_and_3.md` (archived)
- `docs/archive/data_audit_repro.md` (archived_now)
- `docs/archive/data_audit_repro_20260520_114521.md` (archived)
- `docs/archive/data_cleaning_report_repro.md` (archived_now)
- `docs/archive/data_cleaning_report_repro_20260520_114521.md` (archived)
- `docs/archive/feature_engineering_repro.md` (archived_now)
- `docs/archive/feature_engineering_repro_20260520_114521.md` (archived)
- `docs/archive/parameterized_reporting_plan.md` (archived)
- `docs/archive/python_pipeline_instructions.md` (archived)
- `docs/archive/reproducibility_diff_stages_1_3.md` (archived_now)
- `docs/archive/reproducibility_diff_stages_1_3_20260520_114521.md` (archived)
- `docs/archive/reproducibility_review_stages_1_3.md` (archived_now)
- `docs/archive/reproducibility_review_stages_1_3_20260520_114521.md` (archived)
- `docs/archive/stage_2_validation_report.md` (archived)
- `docs/archive/stage_3_sync_report.md` (archived)
- `docs/archive/stages_1_3_inventory.md` (archived)
- `docs/archive/table_columns_dictionary.md` (archived)

## Документы, требующие ручной проверки

- Нет.

## Ограничения

- Очистка не удаляет документы безвозвратно.
- `docs/archive/` не удаляется автоматически.
- Runtime-проверки pipeline выполняются отдельными командами проектного Python.

## 2026-06-04 - production blocker volume_bln_units

| Object | Status | Purpose |
|---|---|---|
| `docs/02_data_contracts/chart_data_contract.md` | added | Contract for unit fields in chart data exports with volume metrics. |
| `scripts/06_build_charts.py` | updated | Generators `format_discount_*` and `format_terms_aggregate_scatter_*` now add unit fields for `*_volume_bln`. |

Checks:

- `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py` - OK.
- `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` - OK.
- `.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` - OK.
- `.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` - OK.

## 2026-06-04 - production artifact policy

| Object | Status | Purpose |
|---|---|---|
| `docs/00_project/artifact_policy.md` | added | Production policy for source files, generated artifacts, release artifacts, logs and archive retention. |

Notes:

- No files were deleted or moved.
- `.gitignore` was not created; the recommended template is documented in `artifact_policy.md`.
- `outputs/charts/**/*.html` and `outputs/exports/**/*.csv` are not ignored until the release process explicitly decides their git policy.
