# Production Readiness Report

Дата актуализации: 2026-06-08.

## 1. Executive Status

Статус проекта: `production-ready candidate`.

Проект готов к повторяемому production-запуску в текущем локальном и Git-контуре при соблюдении runbook и release checklist. Статус обозначен как production-ready candidate, а не окончательный production-ready без оговорок, потому что остаются документированные data warnings, visual regression работает через fallback без screenshot backend, а физическая очистка legacy docs/scripts отложена до P2.

## 2. Git Status

- Repository URL: `https://github.com/VinogradovPV/OFZ_ANALYTICS.git`.
- Visibility: private.
- Default branch: `main`.
- Last verified commit before this report update: `2ac420b Record final production quality gate`.
- Working tree status before this report update: clean.
- Generated outputs policy verified: generated HTML/CSV/reports/dashboard exports are not tracked.

## 3. Artifact Strategy

Source artifacts in Git:

- source code;
- config;
- docs;
- scripts;
- data contracts;
- prompts;
- `data/raw`;
- outputs skeleton files (`.gitkeep`, allowed lightweight `index.md` / `README.md`).

`data/raw` is tracked in Git as the source dataset because the raw Excel files are small and required for reproducibility.

Generated outputs are outside ordinary Git history:

- `outputs/charts/**`;
- `outputs/exports/**`;
- `outputs/reports/**`;
- `outputs/dashboards/**`;
- `outputs/archive/**`;
- `outputs/tmp/**`;
- `outputs/cache/**`.

Release bundle policy:

- generated outputs for a specific reporting run are stored as a release bundle, external artifact or future GitHub Release asset;
- release bundle should include HTML charts, chart data CSV, dashboard exports, run manifests, QA reports and summaries;
- generated outputs should not be committed as normal source history.

## 4. Python And Package Status

- `pyproject.toml`: exists.
- Package name: `ofz-analytics`.
- Version: `0.1.0`.
- Supported Python range: `>=3.11,<3.15`.
- Tested Python version: `Python 3.14.5`.

CLI entry points:

- `ofz-run`;
- `ofz-interactive`;
- `ofz-quality`;
- `ofz-clean-outputs`;
- `ofz-schema`.

Note: short `ofz-*` commands require activated `.venv` or PATH containing `.venv\Scripts`. Direct executable checks through `.\.venv\Scripts\ofz-*.exe` passed.

## 5. Docs Cleanup Status

Docs inventory:

- `keep_active`: 51;
- `archive_candidate`: 35;
- `merge_candidate`: 4;
- `delete_candidate`: 0.

Control documents:

- `docs/00_project/docs_inventory_before_cleanup.md`;
- `docs/00_project/docs_cleanup_apply_decision.md`.

Decision:

- physical docs archive is deferred;
- unresolved references still exist for part of archive/merge candidates;
- no `--delete-archived` before production-ready v1;
- archive apply requires a separate controlled stage after references are resolved.

## 6. Scripts Cleanup Status

Scripts inventory:

- `keep_active`: 32;
- `refactor_candidate`: 5;
- `archive_candidate`: 5;
- `delete_candidate`: 0;
- `unknown`: 0.

Control documents:

- `docs/00_project/scripts_inventory_before_cleanup.md`;
- `docs/00_project/scripts_archive_decision.md`.

Five archive candidates:

- `scripts/cleanup_docs.py`;
- `scripts/migrate_outputs_structure.py`;
- `scripts/reorganize_outputs.py`;
- `scripts/maintenance/migrate_legacy_docs_archive.py`;
- `scripts/maintenance/reorganize_docs.py`.

Decision:

- recommendation for all five: `keep_legacy_until_p2`;
- physical archive deferred;
- no moved/deleted scripts;
- future physical archive requires reference cleanup, explicit approval, `compileall` and `ofz-quality --fast`.

## 7. Module Decomposition Status

Plan exists:

- `docs/03_pipeline/module_decomposition_plan.md`.

Status:

- planning-only;
- no physical moves in production-ready v1;
- decomposition is P2-only;
- wrapper compatibility is mandatory for future moves.

Primary candidates:

- `scripts/06_build_charts.py`;
- `scripts/10_build_monthly_charts.py`;
- `scripts/html_chart_qa.py`;
- `scripts/visual_regression.py`;
- `scripts/quality_gate.py`;
- `scripts/07_dashboard_exports.py`.

## 8. Data Contracts Status

Active data contracts:

- `docs/02_data_contracts/processed_data_contract.md`;
- `docs/02_data_contracts/analytical_tables_contract.md`;
- `docs/02_data_contracts/chart_data_contract.md`;
- `docs/02_data_contracts/dashboard_exports_contract.md`;
- `docs/02_data_contracts/semantic_model_v2.md`.

Contract highlights:

- `*_volume_bln` fields require unit fields with value `млрд рублей`;
- revenue fields include `revenue_volume_bln`, `nominal_revenue_gap_bln`, `revenue_to_nominal_ratio`;
- yield fields distinguish generic yield from weighted average placement yield;
- discount fields define source column, fallback formula and unit `п.п.`;
- label and quality fields are documented for chart data exports.

## 9. Quality Gate Status

Final production quality gate was executed for:

```powershell
--report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Results:

- `pip install -e .`: OK after escalated rerun because sandboxed pip could not write to `%TEMP%`;
- `pip check`: OK;
- `compileall`: OK;
- `schema_validation`: OK, 16/16;
- `smoke_tests`: OK, 9 checks;
- `regression_tests`: OK, 14 checks;
- `anomaly_tests`: completed with documented data warnings;
- `html_chart_qa`: OK;
- `visual_regression`: OK via fallback static HTML / Plotly JSON inspection;
- `quality_gate --fast`: OK;
- `quality_gate --full`: OK.

Note: a first parallel fast/full gate run caused a transient `.pyc` permission conflict in `scripts/__pycache__`. Sequential rerun passed.

## 10. Fixed Blockers

Fixed blockers:

- `schema_validation / volume_bln_units` production blocker fixed in generators and data contracts;
- generated outputs excluded from Git with skeleton preserved;
- `data/raw` strategy fixed and documented;
- `.gitignore` and Git artifact strategy implemented;
- CLI entry points added and verified;
- cleanup outputs workflow added through `ofz-clean-outputs`;
- production runbook and release checklist created.

## 11. Remaining Warnings

Remaining warnings are data/operations warnings, not blocking execution failures:

- anomaly tests report missing yield rows and demand/supply edge cases;
- bid-to-cover and demand-to-placement outliers require analytical review;
- rows with missing cutoff price limit discount analysis;
- nominal/revenue gap anomalies above threshold require interpretation;
- screenshot backend is not configured, so visual regression uses static HTML / Plotly JSON fallback;
- docs/scripts physical cleanup remains deferred until references are resolved;
- Python 3.11-3.13 are allowed by metadata but current local runtime certification was performed on Python 3.14.5.

## 12. Final Structure

Docs:

- `docs/00_project/` — project governance, inventories, readiness, artifact policy;
- `docs/01_methodology/` — methodology and KPI maps;
- `docs/02_data_contracts/` — active data contracts;
- `docs/02_data_pipeline/` — data pipeline documentation;
- `docs/03_analytics/` and `docs/03_pipeline/` — analytics and pipeline planning;
- `docs/04_visualization/` — visualization rules and limitations;
- `docs/05_dashboard/` — dashboard docs;
- `docs/06_quality/` — QA reports and manual checks;
- `docs/07_operations/` — environment, runbook, release checklist;
- `docs/90_archive/` — historical documentation.

Scripts:

- active stage scripts remain in `scripts/`;
- production maintenance scripts are under `scripts/maintenance/`;
- no physical script archive or decomposition in v1.

Outputs:

- generated outputs under `outputs/`;
- Git tracks only skeleton `.gitkeep` files and `outputs/charts/index.md`;
- generated HTML/CSV/reports/dashboard exports are release artifacts, not source commits.

## 13. Full Outputs Cleanup Command

Dry-run:

```powershell
ofz-clean-outputs --dry-run
```

Archive and delete:

```powershell
ofz-clean-outputs --archive-all --delete-all --confirm DELETE_OUTPUTS
```

Fallback:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all --delete-all --confirm DELETE_OUTPUTS
```

## 14. Interactive Launcher Cleanup Mode

Interactive launcher:

```powershell
ofz-interactive
```

Before pipeline start it checks generated outputs and offers:

1. keep outputs as-is;
2. show cleanup dry-run;
3. archive outputs and clean;
4. clean outputs without archive after explicit confirmation;
5. cancel run.

Launcher delegates deletion to `scripts/maintenance/cleanup_outputs.py`; it does not delete files directly.

## 15. Release Checklist

Release checklist exists:

- `docs/07_operations/release_checklist.md`.

It covers Git state, environment, CLI help, data/raw, pipeline runs, QA, outputs/release bundle, docs/scripts cleanup decisions and final staged-file checks.

## 16. Remaining Risks

Production risks that remain:

- visual regression is not screenshot-based yet;
- generated outputs are large and require external release bundle discipline;
- docs archive candidates still have references, so cleanup is not physically applied;
- legacy scripts remain in place until P2;
- chart builders and QA scripts are large monoliths and need controlled decomposition later;
- data warnings require analytical review before high-stakes external publication;
- release bundle process is documented but not yet automated as a single command.

## 17. Next Release Recommendations

Recommended P2 work:

1. Add screenshot backend for visual regression.
2. Automate release bundle creation.
3. Resolve docs archive references and run controlled docs archive apply.
4. Resolve legacy script references and physically archive safe candidates.
5. Start module decomposition with helper extraction only.
6. Add CI workflow for install, compileall, schema, fast quality gate.
7. Certify runtime on Python 3.11/3.12/3.13 or narrow metadata to tested versions.
8. Add a release manifest tying Git commit, raw hashes, run manifest and release bundle checksum.
