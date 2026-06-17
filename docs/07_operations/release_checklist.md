# Release checklist

## Stable Release Procedure

- [ ] Stable release procedure reviewed: `docs/07_operations/stable_release_procedure.md`.
- [ ] Source acquisition dry-run completed before release decision.
- [ ] Monthly or annual-final update completed if needed.
- [ ] Source registry reviewed after update.
- [ ] Data audit completed with source registry validation.
- [ ] `ofz-quality --fast` completed.
- [ ] Screenshot validation completed outside sandbox or fallback limitation documented.
- [ ] `ofz-quality --full` completed before stable release.
- [ ] Release bundle dry-run reviewed.
- [ ] Release bundle build completed only after dry-run review.
- [ ] Optional BI package dry-run/build completed if BI handoff is in scope.
- [ ] Git tag planned after final commit/push.
- [ ] `gh release create/upload` not run without separate explicit user permission.

Дата актуализации: 2026-06-08.

Использовать перед production release или перед публикацией release bundle.

## Git

- [ ] `git status --short` clean или содержит только ожидаемые release-doc changes.
- [ ] Branch: `main`.
- [ ] `main` synced with `origin/main`.
- [ ] Remote: `https://github.com/VinogradovPV/OFZ_ANALYTICS.git`.
- [ ] Repository visibility: private.
- [ ] Generated outputs not staged.
- [ ] Нет `git add .` без ручного просмотра staged files.

## Environment

- [ ] `.venv` создан.
- [ ] `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` OK.
- [ ] `.\.venv\Scripts\python.exe -m pip install -e .` OK.
- [ ] `.\.venv\Scripts\python.exe -m pip check` OK.
- [ ] `.\.venv\Scripts\python.exe -m compileall -q scripts` OK.

## CLI Help

- [ ] `ofz-run --help` OK after `.venv` activation, or `.\.venv\Scripts\ofz-run.exe --help` OK.
- [ ] `ofz-interactive --help` OK after `.venv` activation, or `.\.venv\Scripts\ofz-interactive.exe --help` OK.
- [ ] `ofz-quality --help` OK after `.venv` activation, or `.\.venv\Scripts\ofz-quality.exe --help` OK.
- [ ] `ofz-clean-outputs --help` OK after `.venv` activation, or `.\.venv\Scripts\ofz-clean-outputs.exe --help` OK.
- [ ] `ofz-schema --help` OK after `.venv` activation, or `.\.venv\Scripts\ofz-schema.exe --help` OK.
- [ ] `ofz-build-release-bundle --help` OK after `.venv` activation, or `.\.venv\Scripts\ofz-build-release-bundle.exe --help` OK.

## UI Launchers

- [ ] CLI remains the main supported production interface.
- [ ] PowerShell GUI launcher smoke OK: `powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1`.
- [ ] PowerShell GUI launcher is treated as the recommended Windows UI MVP, not as a replacement for CLI.
- [ ] Word VBA launcher is optional.
- [ ] `.ps1`, `.bas` and `.frm` files are treated as source artifacts.
- [ ] `.docm` files are treated as release artifacts unless explicitly approved by artifact policy.
- [ ] Launcher logs under `outputs/reports/launcher/` are treated as generated outputs.
- [ ] UI launcher did not skip or replace required quality gate checks.
- [ ] Word launcher source includes `OfzLauncher.bas` and `frmOfzLauncher.frm`.
- [ ] Word `.docm` assembly follows `tools/word_launcher/word_docm_build_instructions.md`.
- [ ] Word `.docm` is saved under `releases/ui_launcher/` or another external release location, not staged in Git.
- [ ] Word launcher blocks `cleanup-delete-all` without `DELETE_OUTPUTS`.
- [ ] Word launcher blocks `release-build` without `BUILD_RELEASE_BUNDLE`.
- [ ] Word launcher command preview contains only whitelisted `ofz-*` CLI entry points.

## Data

- [ ] `data/raw` tracked in Git.
- [ ] Raw files are small and expected.
- [ ] No temporary Excel files: `~$*.xlsx`, `*.tmp`, `*.bak`.
- [ ] Minfin monthly update procedure reviewed: `docs/07_operations/minfin_monthly_update_procedure.md`.
- [ ] For monthly update, `ofz-fetch-minfin --mode monthly --dry-run` was reviewed before any `--download`.
- [ ] For annual-final update, selected title/year/file were reviewed before any final promotion.
- [ ] Changed annual-final hash was not replaced without `REPLACE_MINFIN_FINAL` and manual review.
- [ ] Manual fallback, if used, used `--manual-file` and `IMPORT_MINFIN_FILE`.
- [ ] `data/raw/minfin/ofz_auction_results/versions/` is not staged.
- [ ] `outputs/reports/source_acquisition/` is not staged.
- [ ] Raw data registry updated.
- [ ] Raw hashes captured in registry and/or run manifest.
- [ ] `data/raw` was not modified by pipeline.

## Pipeline

- [ ] Month cumulative pipeline OK:

```powershell
ofz-run --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

- [ ] Year cumulative pipeline OK, if release includes year outputs:

```powershell
ofz-run --all --report-date 2026-01-01 --retrospective-years 4 --period-type year --aggregation-mode cumulative
```

- [ ] Executive summary created.
- [ ] Run manifest created.

## QA

- [ ] `ofz-schema --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` OK.
- [ ] `.\.venv\Scripts\python.exe scripts\smoke_tests.py` OK.
- [ ] `.\.venv\Scripts\python.exe scripts\regression_tests.py` OK.
- [ ] `.\.venv\Scripts\python.exe scripts\anomaly_tests.py` OK or warnings documented.
- [ ] `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` OK.
- [ ] `.\.venv\Scripts\python.exe scripts\visual_regression.py --mode fallback --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` OK.
- [ ] `.\.venv\Scripts\python.exe scripts\visual_regression.py --mode auto --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` OK.
- [ ] If Playwright browser is installed, `.\.venv\Scripts\python.exe scripts\visual_regression.py --mode screenshot --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` OK.
- [ ] Screenshot mode was run from the project PowerShell session, not from Codex sandbox, if browser subprocesses are blocked.
- [ ] Screenshot artifacts under `outputs/reports/visual_regression/` are treated as generated outputs and are not staged.
- [ ] `ofz-quality --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` OK.
- [ ] `ofz-quality --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` OK for release.

## Outputs And Artifacts

- [ ] Outputs cleaned or archive policy followed.
- [ ] If cleanup needed, `ofz-clean-outputs --dry-run` was reviewed.
- [ ] If audit history needed, `ofz-clean-outputs --archive-all` was run before delete.
- [ ] `ofz-build-release-bundle --dry-run --report-date <date> --retrospective-years <N> --period-type <period> --aggregation-mode <mode>` was reviewed.
- [ ] If release bundle is needed, `ofz-build-release-bundle --include-outputs --confirm BUILD_RELEASE_BUNDLE ...` was run.
- [ ] Release bundle includes HTML charts.
- [ ] Release bundle includes chart data CSV.
- [ ] Release bundle includes dashboard exports.
- [ ] Release bundle includes run manifests.
- [ ] Release bundle includes QA reports.
- [ ] Release bundle includes summaries.
- [ ] Generated outputs are not committed to Git.
- [ ] Release bundle remains an external artifact under ignored `releases/`.

## Documentation And Cleanup Decisions

- [ ] Docs inventory updated.
- [ ] Docs archive deferred decision documented in `docs/00_project/docs_cleanup_apply_decision.md`.
- [ ] No docs physical archive before references are resolved.
- [ ] No `--delete-archived` before production-ready v1.
- [ ] Scripts inventory updated.
- [ ] Scripts archive deferred decision documented in `docs/00_project/scripts_archive_decision.md`.
- [ ] 5 legacy scripts kept until P2.
- [ ] Module decomposition deferred to P2 and documented in `docs/03_pipeline/module_decomposition_plan.md`.

## Final Git Check

```powershell
git status --short
git diff --cached --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|data/processed|logs"
```

- [ ] Generated outputs not staged.
- [ ] Commit contains only intended source/docs/config changes.
- [ ] Commit pushed to `origin/main`.

## CI / GitHub Actions release checks

- [ ] `.github/workflows/quality.yml` exists.
- [ ] `quality-fast` runs on `push` and `pull_request` to `main`.
- [ ] `quality-fast` installs runtime/dev dependencies, editable package, runs `pip check`, `compileall`, `ofz-schema` and `ofz-quality --fast`.
- [ ] `quality-full` is manual-only via `workflow_dispatch` and depends on `quality-fast`.
- [ ] Workflow uses pip cache only and does not cache `outputs/` or `releases/`.
- [ ] Workflow uploads QA reports as GitHub Actions artifacts.
- [ ] Generated outputs and release bundles are not committed by CI.
- [ ] GitHub-side workflow state reviewed with `gh workflow list` and `gh run list`.
- [ ] If a CI run failed, `gh run view <run-id> --log` was reviewed and the failure was documented.
