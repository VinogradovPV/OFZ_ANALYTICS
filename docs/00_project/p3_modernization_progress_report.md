# P3 modernization progress report

## P3.0-pre - P3 rules accepted and session preflight

Date: 2026-06-16.

### Status

- P3 prompt/instructions accepted from `prompts/ofz_p3_modernization_system_prompt.md` and `prompts/ofz_p3_modernization_step_by_step.md`.
- P2 status confirmed from `docs/00_project/p2_completion_report.md`: `stable-release-candidate`.
- P3 does not start with source acquisition code. `P3.PRE.1 Scripts balance/problem audit` and `P3.PRE.2 Docs mojibake/encoding audit and UTF-8 normalization` are mandatory before `P3.0 Source acquisition design`.
- Minfin source acquisition policy accepted as mandatory Variant C: hybrid latest + final + version snapshots on hash change.
- P3 progress tracking will use `docs/00_project/p3_modernization_progress_report.md`.
- `P3.PRE.1` must maintain `docs/00_project/p3_scripts_balance_audit_report.md`.
- `P3.PRE.2` must maintain `docs/00_project/p3_docs_encoding_audit_report.md` with an entry for every checked document.
- Token/cost-aware mode accepted: targeted reads/searches, no large rereads without cause, no full quality gate without trigger, docs-only stages do not require compileall/quality, session preflight once per session, skipped checks documented after each stage.
- Git/GitHub outside-sandbox policy accepted for subsequent work: run Git/`gh` commands from the project root outside sandbox, check staged generated artifacts before commit, and do not perform PR/release/workflow/secret/repo-edit operations without a separate explicit user command.

### Session preflight results

Repository state:

| Check | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | OK outside sandbox | Real Git state checked from project root outside sandbox. Final state after the P3 rules commits: clean on `main...origin/main`. Earlier sandbox status output is considered non-authoritative under the accepted Git/GitHub outside-sandbox policy. |
| `git branch --show-current` | OK | `main`. |
| `git remote -v` | OK | `origin` fetch/push: `https://github.com/VinogradovPV/OFZ_ANALYTICS.git`. |
| `git log --oneline -10` | OK outside sandbox | Latest commit before this step in the real repo: `9dffa96 rerun pipeline`; recent history also included `75e0e9b rerun pipeline`, `3a018bb Add P2 completion report`, `d8cc7ed Document archive deletion policy`, `a9ad498 Add BI release package workflow`. |

GitHub CLI:

| Check | Result | Notes |
| --- | --- | --- |
| `gh --version` | OK | `gh version 2.93.0 (2026-05-27)`. |
| `gh auth status` | OK outside sandbox | Sandbox run reported invalid keyring token; required outside-sandbox rerun succeeded for `VinogradovPV`, HTTPS protocol, scopes `gist`, `read:org`, `repo`, `workflow`. |
| `gh repo view VinogradovPV/OFZ_ANALYTICS` | OK outside sandbox | Sandbox run failed on proxy connection to `127.0.0.1:9`; required outside-sandbox rerun succeeded and identified the repo as private `VinogradovPV/OFZ_ANALYTICS`. |

CLI entry points:

| Check | Result | Notes |
| --- | --- | --- |
| `.\.venv\Scripts\ofz-run.exe --help` | OK | Help rendered. |
| `.\.venv\Scripts\ofz-quality.exe --help` | OK | Help rendered. |
| `.\.venv\Scripts\ofz-schema.exe --help` | OK | Help rendered. |
| `.\.venv\Scripts\ofz-build-release-bundle.exe --help` | OK | Help rendered. |

### Skipped checks

- `compileall`: skipped because this step changed only documentation.
- `ofz-quality --fast`: skipped because this step changed only documentation and no quality gate was requested.
- `ofz-quality --full`: skipped because this step changed only documentation and full quality is explicitly out of scope for the P3 rules acceptance step.

### Next stage

Next stage was superseded by the pre-P3 blocker fix requested by the user: `P3.PRE.0 Windows GUI launcher UX and runtime fix`.

## P3.PRE.0 - Windows GUI launcher UX and runtime fix

Date: 2026-06-16.

### Status

- Completed pre-P3 bugfix stage before `P3.PRE.1` and `P3.PRE.2`.
- P3 source acquisition was not changed.
- `data/raw` was not changed.
- Generated launcher logs, cleanup manifests and release artifacts are not source artifacts and must not be committed.

### Changes

- Fixed `tools/windows_launcher/ofz_launcher.ps1` command preview under `Set-StrictMode` by checking the hashtable key before reading `Preview`.
- Changed `run-pipeline` action to build the production default CLI command without a manual stages list: `.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`.
- Added `-PreviewOnly` for safe command construction checks without running the pipeline.
- Changed `validate-environment` to explicit local OK/FAIL checks for project root, `pyproject.toml`, `.venv\Scripts`, `data\raw` and required CLI entry points.
- Improved CLI failure logging with exit code, full log path and last meaningful stdout/stderr line.
- Made launcher log/stdout/stderr file names unique beyond seconds to avoid collisions during fast repeated checks.
- Replaced `tools/windows_launcher/README.md` with a Russian UX guide and added a short link from `README.md`.
- Updated `docs/06_quality/manual_checks_log.md`.

### Checks

| Check | Result | Notes |
| --- | --- | --- |
| PowerShell parse check | OK | Scriptblock parse passed. |
| Launcher smoke | OK | Environment validation, bad date block, token blocks, cleanup dry-run and release dry-run passed. |
| GUI auto-close smoke | OK | `-Gui -AutoCloseGuiForCheck` opened and closed without runtime error. |
| `-Action validate-environment` | OK | Printed explicit OK checks and stated that no pipeline process started. |
| `-Action release-dry-run` | OK | Dry-run completed and wrote no release bundle. |
| `-Action release-build` without token | Expected fail | Blocked without `BUILD_RELEASE_BUNDLE`. |
| `-Action cleanup-delete-all` without token | Expected fail | Blocked without `DELETE_OUTPUTS`. |
| `-Action run-pipeline -PreviewOnly` | OK | Preview command contains `ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` and does not contain `--stages`. |

### Skipped checks

- Real `run-pipeline` through launcher: skipped because preview-only verified command construction and a real run can generate outputs.
- `compileall`: skipped because Python pipeline code did not change.
- `ofz-quality --fast`: skipped because Python pipeline code did not change and this is a PowerShell/docs bugfix.
- `ofz-quality --full`: skipped because Python pipeline code did not change and full quality was not triggered.

### Next stage

Next stage: `P3.PRE.1 Scripts balance/problem audit`.
