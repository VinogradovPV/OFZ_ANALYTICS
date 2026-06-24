# NEXT.5 Telemetry hardening plan

Дата: 2026-06-24.

## Цель

Уточнить telemetry после release `v0.1.0`, чтобы оператор видел раздельные счетчики:

- active raw;
- raw versions;
- current generated outputs;
- archive outputs;
- tmp/cache outputs;
- точные duration по stage.

Этап не меняет финансовую методологию, output paths, chart semantics, source acquisition policy и release policy.

## Текущие telemetry fields

`scripts/pipeline/telemetry.py` сейчас пишет:

- `schema_version`;
- `run_id`;
- `status`;
- `started_at`;
- `finished_at`;
- `duration_seconds`;
- `stage_durations`;
- `input_row_counts`;
- `output_file_counts`;
- `generated_artifacts_count`;
- `artifacts_total_size` / `artifacts_total_size_bytes`;
- `warnings_count` / `errors_count`;
- `cleanup_mode`;
- `quality_gate_results`;
- `schema_validation_results`;
- `git_commit`;
- `git_dirty_flag`;
- `raw_data_hashes`;
- report parameters and requested stages.

## Неоднозначные counters

- `input_row_counts.raw_files` считает все файлы под `data/raw`, а не только pipeline input Excel/CSV.
- `raw_data_hashes` собирает все файлы под `data/raw`, включая controlled Minfin registry/latest/final/versions.
- `generated_artifacts_count` считает весь `outputs`, включая `outputs/archive`, `outputs/tmp` и `outputs/cache`.
- `output_file_counts.archive` есть отдельно, но общий `generated_artifacts_count` остается смешанным.
- `stage_durations.duration_seconds` считается через ISO timestamps с секундной точностью, поэтому короткие stages могут выглядеть как `0.0`.

## Counters to split

Добавить совместимые top-level fields, не удаляя старые поля:

- `raw_active_files_count`;
- `raw_versions_files_count`;
- `generated_current_files_count`;
- `generated_archive_files_count`;
- `generated_tmp_cache_files_count`.

Также добавить подробные словари:

- `raw_file_scope_counts`;
- `generated_file_scope_counts`.

## Duration fields

В каждой записи `stage_durations` добавить:

- `stage_duration_seconds_precise`.

Старое поле `duration_seconds` сохранить для обратной совместимости, но считать его на основе `perf_counter`, а не по ISO timestamps.

## Source files to change

- `scripts/pipeline/telemetry.py`
- `scripts/qa/telemetry_summary_smoke.py` (новый smoke)

Документация:

- `docs/00_project/telemetry_hardening_plan.md`
- `docs/00_project/post_p3_pipeline_optimization_report.md`
- `docs/07_operations/production_runbook.md`
- `docs/06_quality/manual_checks_log.md`
- `README.md`, если потребуется уточнить описание telemetry.

## Smoke/tests

Нужен offline/current telemetry smoke:

- найти свежий telemetry JSON;
- проверить чтение JSON;
- проверить наличие новых fields;
- проверить, что `raw_active_files_count` не включает versions;
- проверить, что `generated_current_files_count` не включает archive/tmp/cache;
- проверить, что duration fields являются числами `>= 0`.

## Not changed

- Расчетные данные, yield/revenue/volume methodology.
- Output paths и имена generated artifacts.
- Chart/table semantics и labels.
- Source acquisition behavior, registry policy и Minfin download/import rules.
- Release bundle logic и GitHub Release assets.

## Baseline before code changes

Будет выполнен baseline run:

```powershell
.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

После baseline run сюда добавляются наблюдения по свежему `outputs/reports/telemetry/telemetry_*.json`.

Baseline telemetry:

- file: `outputs/reports/telemetry/telemetry_20260624_145510_d76e190c.json`;
- `duration_seconds`: `11.528`;
- `generated_artifacts_count`: `209`;
- `artifacts_total_size_bytes`: `249050537`;
- `input_row_counts.raw_files`: `14`;
- `raw_data_hashes`: `14`;
- `output_file_counts`: `charts=50`, `exports=61`, `reports=78`, `dashboards=19`, `archive=1`;
- sample stage durations show second-level rounding: stage `3` and stage `5` have `duration_seconds=0.0`.

Baseline observation:

- Stage 1 runtime log says `Найдено raw-файлов: 8`, while telemetry `raw_files=14`; telemetry counts all files under `data/raw`, including controlled source acquisition files, not only pipeline input workbooks.
- `generated_artifacts_count=209` is useful as total inventory, but it mixes current outputs and archive outputs.
- Per-stage duration precision is insufficient for short stages.

## Implementation result

Added compatible telemetry fields:

- `raw_file_scope_counts`;
- `generated_file_scope_counts`;
- `raw_active_files_count`;
- `raw_versions_files_count`;
- `generated_current_files_count`;
- `generated_archive_files_count`;
- `generated_tmp_cache_files_count`;
- `stage_duration_seconds_precise` inside each `stage_durations` row.

Existing fields are preserved:

- `input_row_counts.raw_files`;
- `generated_artifacts_count`;
- `artifacts_total_size` / `artifacts_total_size_bytes`;
- `stage_durations[].duration_seconds`;
- `raw_data_hashes`.

Post-change telemetry:

- file: `outputs/reports/telemetry/telemetry_20260624_151147_e980bc2b.json`;
- `duration_seconds`: `11.384`;
- `raw_file_scope_counts`: `active=10`, `versions=2`, `registry=2`, `latest=1`, `final=1`, `other=8`, `total=14`;
- `generated_file_scope_counts`: `current=212`, `archive=1`, `tmp_cache=0`;
- `generated_artifacts_count`: `213`;
- stages: `19`;
- slowest stage: `8` / `Этап 8: построение графиков`, `stage_duration_seconds_precise=3.315637`.

Smoke note:

`scripts/qa/telemetry_summary_smoke.py` compares raw scopes exactly. For generated current outputs it allows the filesystem current count to be greater than telemetry, because telemetry is written before the run manifest files are appended. Archive and tmp/cache counts are checked strictly.
