# Release checklist

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
- [ ] `.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` OK.
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
