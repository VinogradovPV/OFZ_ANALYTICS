# P3.PRE.1 scripts balance/problem audit report

Date: 2026-06-16.

## Scope

- Checked `scripts/`, `scripts/archive/`, `scripts/charts/`, `scripts/qa/`, `scripts/maintenance/`, `scripts/pipeline/`.
- `scripts/source_acquisition/` does not exist yet; P3.0 source acquisition was not started.
- Python files scanned: 58 total, 53 active, 5 archived.

## Method

- Static scan for stale archive references, TODO/FIXME/XXX, hardcoded absolute paths, `shell=True`, subprocess usage, potential `data/raw` mutation, missing `main()`, and wrapper/module balance.
- No pipeline behavior was changed.
- No source acquisition files were created.

## Summary

- medium: 5
- info: 8

## Issues

| issue_id | file | severity | category | description | recommended_action | fixed_now | notes |
|---|---|---|---|---|---|---|---|
| P3PRE1-001 | `scripts/06_build_charts.py` | medium | wrapper_module_balance | Chart family skeletons exist under `scripts/charts/`, but the main chart builder remains intentionally monolithic after P2.11. Current size: 7161 lines. | Defer to P3.MOD: extract one family/check group per commit with targeted chart/QA validation. | no | No behavior change in P3.PRE.1; large decomposition is intentionally out of scope. |
| P3PRE1-002 | `scripts/10_build_monthly_charts.py` | medium | wrapper_module_balance | Monthly chart skeleton exists under `scripts/charts/monthly.py`, but builders remain in the root script. Current size: 1886 lines. | Defer to P3.MOD: extract one family/check group per commit with targeted chart/QA validation. | no | No behavior change in P3.PRE.1; large decomposition is intentionally out of scope. |
| P3PRE1-003 | `scripts/12_build_revenue_charts.py` | medium | wrapper_module_balance | Revenue chart skeleton exists under `scripts/charts/revenue.py`, but builders remain in the root script. Current size: 711 lines. | Defer to P3.MOD: extract one family/check group per commit with targeted chart/QA validation. | no | No behavior change in P3.PRE.1; large decomposition is intentionally out of scope. |
| P3PRE1-004 | `scripts/html_chart_qa.py` | medium | wrapper_module_balance | QA contract constants were extracted, but check functions remain in the monolithic QA script. Current size: 2264 lines. | Defer to P3.MOD: extract one family/check group per commit with targeted chart/QA validation. | no | No behavior change in P3.PRE.1; large decomposition is intentionally out of scope. |
| P3PRE1-005 | `scripts/visual_regression.py` | medium | wrapper_module_balance | Visual regression contract constants were extracted, but check functions remain in the monolithic QA script. Current size: 1405 lines. | Defer to P3.MOD: extract one family/check group per commit with targeted chart/QA validation. | no | No behavior change in P3.PRE.1; large decomposition is intentionally out of scope. |
| P3PRE1-006 | `scripts/interactive_pipeline.py` | info | subprocess_review | Uses `subprocess` without detected `shell=True`. | Keep argument-list invocation and explicit cwd/check handling; review if command surface expands. | n/a | No unsafe shell=True found by static scan. |
| P3PRE1-007 | `scripts/maintenance/build_bi_package.py` | info | subprocess_review | Uses `subprocess` without detected `shell=True`. | Keep argument-list invocation and explicit cwd/check handling; review if command surface expands. | n/a | No unsafe shell=True found by static scan. |
| P3PRE1-008 | `scripts/maintenance/build_release_bundle.py` | info | subprocess_review | Uses `subprocess` without detected `shell=True`. | Keep argument-list invocation and explicit cwd/check handling; review if command surface expands. | n/a | No unsafe shell=True found by static scan. |
| P3PRE1-009 | `scripts/pipeline/telemetry.py` | info | subprocess_review | Uses `subprocess` without detected `shell=True`. | Keep argument-list invocation and explicit cwd/check handling; review if command surface expands. | n/a | No unsafe shell=True found by static scan. |
| P3PRE1-010 | `scripts/quality_gate.py` | info | subprocess_review | Uses `subprocess` without detected `shell=True`. | Keep argument-list invocation and explicit cwd/check handling; review if command surface expands. | n/a | No unsafe shell=True found by static scan. |
| P3PRE1-011 | `scripts/run_pipeline.py` | info | subprocess_review | Uses `subprocess` without detected `shell=True`. | Keep argument-list invocation and explicit cwd/check handling; review if command surface expands. | n/a | No unsafe shell=True found by static scan. |
| P3PRE1-012 | `scripts/smoke_tests.py` | info | subprocess_review | Uses `subprocess` without detected `shell=True`. | Keep argument-list invocation and explicit cwd/check handling; review if command surface expands. | n/a | No unsafe shell=True found by static scan. |
| P3PRE1-013 | `scripts/visual_regression.py` | info | subprocess_review | Uses `subprocess` without detected `shell=True`. | Keep argument-list invocation and explicit cwd/check handling; review if command surface expands. | n/a | No unsafe shell=True found by static scan. |

## Checks Performed

- `shell=True`: none found.
- Active imports/references to `scripts.archive`: none found in active Python files.
- Hardcoded absolute user paths: none found in Python scripts.
- TODO/FIXME/XXX markers: none found in Python scripts.
- CLI-like scripts missing `main()`: none found.
- Potential direct `data/raw` mutation: none found.
- Archived scripts are retained under `scripts/archive/2026-06-15/` for audit only.
- Subprocess usage exists in active scripts, but static scan found no `shell=True`; keep command lists and explicit cwd/check handling.

## Recommended P3.MOD Items

1. Continue controlled chart decomposition after P3.PRE audits: extract one chart family/check group per commit from `06_build_charts.py`, `10_build_monthly_charts.py`, `12_build_revenue_charts.py`, `html_chart_qa.py`, and `visual_regression.py`.
2. Keep archived scripts as audit-only until post-stable archive deletion policy allows deletion.
3. Re-run this audit after P3 source acquisition scripts are added.

## Verification

- `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\audit_scripts_balance.py`: OK.
- `.\.venv\Scripts\python.exe scripts\maintenance\audit_scripts_balance.py --report`: OK; generated this report.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.

## Skipped Checks

- `ofz-quality --fast`: skipped because P3.PRE.1 changed only an audit helper and documentation, with no pipeline behavior change.
- `ofz-quality --full`: skipped because full quality gate is out of scope for the audit helper/report step.
