# Strict pipeline precheck report

Date: 2026-07-01.

## 1. Scope

NEXT.9 validates that the canonical full pipeline can run with strict source registry validation and legacy raw fallback disabled.

This report does not switch defaults. Production default remains:

```text
source-registry-mode=warn
allow-legacy-raw=true
```

## 2. Preconditions

- NEXT.8 was completed and pushed in commit `83da318`.
- `ofz-run` supports `--source-registry-mode off|warn|strict`, `--allow-legacy-raw` and `--no-allow-legacy-raw`.
- Working tree before NEXT.9 contained only untracked prompt files outside staging scope.
- Strict-by-default has not been approved.

## 3. Commands

```powershell
git status --short --branch
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\python.exe scripts\qa\check_text_encoding.py
.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --source-registry-mode strict --no-allow-legacy-raw
.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-quality.exe --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## 4. Results

| Check | Result |
|---|---|
| `pip install -e .` | OK |
| `pip check` | OK, no broken requirements |
| `compileall -q scripts` | OK |
| `check_text_encoding.py` | OK, checked 282 files, 0 invalid UTF-8, 0 mojibake |
| Full `ofz-run` strict/no-legacy | OK |
| `ofz-schema` | OK, 16 schema checks passed |
| `ofz-quality --fast` | OK |
| `ofz-quality --full` | OK |

The strict full pipeline run wrote run manifest `run_manifest_20260701_171622_de0245bd.json` and telemetry `telemetry_20260701_141610_202c7783.json` under generated output folders.

## 5. Registry Validation Status

Stage 1 ran with:

```text
--source-registry-mode strict --no-allow-legacy-raw
```

Fresh `docs/02_data_pipeline/data_audit.md` recorded:

```text
source_registry_mode=strict
source_registry_status=ok
registry_warnings_count=0
registry_errors_count=0
registry_exists=True
records_count=5
active_records_count=2
```

## 6. Legacy Fallback Used

No.

Fresh data audit recorded:

```text
legacy_raw_fallback_used=False
controlled_source_used=False
```

`controlled_source_used=False` is expected for the current validation-only integration: strict registry validation gates the run, while downstream ingestion behavior is not switched by NEXT.9.

## 7. Warnings

- `ofz-quality --full` reported existing analytical warnings from anomaly tests, such as missing yield rows and demand/placement edge cases; the quality gate completed with exit code 0.
- Visual regression used the documented fallback because the browser screenshot backend is unavailable in the managed Codex environment; this did not fail the gate.
- Strict-by-default remains unapproved.

## 8. Generated Artifacts Not Staged

The precheck regenerated outputs, processed datasets, telemetry, run manifests, quality reports and logs. These are generated artifacts and must not be staged.

The NEXT.9 staging scope is documentation only:

```text
docs/00_project/strict_pipeline_precheck_report.md
docs/00_project/source_registry_strict_migration_plan.md
docs/00_project/post_p3_optimization_progress_report.md
docs/06_quality/manual_checks_log.md
```

## 9. Decision

Strict-ready for full pipeline precheck: yes.

The canonical full pipeline, schema validation, quality-fast and quality-full all passed with strict/no-legacy registry flags.

## 10. Recommendation

Keep default as `warn + allow-legacy-raw` until a separate approval request is prepared and approved.

Recommended next step: NEXT.10 strict default approval request.
