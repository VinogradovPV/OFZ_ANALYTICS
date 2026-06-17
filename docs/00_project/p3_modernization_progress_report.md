# P3 modernization progress report

## P3.6 - Интеграция source registry в data audit

Дата: 2026-06-17.

### Статус

- Завершен этап `P3.6 Registry integration with legacy pipeline compatibility`.
- В `scripts/source_acquisition/source_registry.py` добавлены helpers:
  - `validate_source_registry(...)`;
  - `load_active_source_records(...)`;
  - `validate_active_file_hashes(...)`;
  - `summarize_registry_status(...)`.
- `scripts/01_data_audit.py` получил CLI параметры:
  - `--source-registry-mode off|warn|strict`;
  - `--allow-legacy-raw` / `--no-allow-legacy-raw`.
- Default сохранен совместимым: `source-registry-mode=warn`, `allow-legacy-raw=true`.
- `off` не читает registry и сохраняет legacy behavior.
- `warn` читает registry при наличии и пишет warnings/errors в audit report, но legacy raw fallback продолжает работу.
- `strict` требует registry и active controlled files; missing registry, duplicate active rows, missing active file, hash mismatch и size mismatch приводят к non-zero.
- Data audit report теперь включает раздел `Source registry validation` с `source_registry_mode`, `source_registry_status`, `controlled_source_used`, `legacy_raw_fallback_used`, `registry_warnings_count`, `registry_errors_count`.
- Controlled source остается validation-only; Excel input selection и cleaning behavior не менялись.
- Live network calls не добавлялись.

### Изменения

- `scripts/01_data_audit.py`
- `scripts/source_acquisition/source_registry.py`
- `scripts/qa/minfin_data_audit_registry_smoke.py`
- `tests/fixtures/minfin_data_audit_registry_valid.json`
- `tests/fixtures/minfin_data_audit_registry_missing_file.json`
- `tests/fixtures/minfin_data_audit_registry_hash_mismatch.json`
- `tests/fixtures/minfin_data_audit_registry_duplicate_active.json`
- `docs/02_data_contracts/minfin_source_registry_contract.md`
- `docs/07_operations/minfin_source_acquisition.md`
- `docs/06_quality/manual_checks_log.md`
- `docs/00_project/p3_modernization_progress_report.md`

### Проверки

| Проверка | Результат | Примечания |
| --- | --- | --- |
| `py_compile scripts/01_data_audit.py scripts/source_acquisition/source_registry.py` | OK | Data audit CLI и registry helpers компилируются. |
| `py_compile scripts/qa/minfin_data_audit_registry_smoke.py` | OK | Smoke test компилируется. |
| `scripts/qa/minfin_data_audit_registry_smoke.py` | OK | Проверены missing registry warn/strict, valid registry, missing active file, hash mismatch, duplicate active rows, legacy fallback allowed, no live network. |
| `compileall -q scripts` | OK | Все scripts компилируются. |
| `ofz-quality --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` | OK | Fast quality gate не сломан. |
| `scripts/01_data_audit.py --source-registry-mode warn --allow-legacy-raw` | OK | При отсутствующем registry audit продолжил legacy raw fallback и записал warning. |

### Пропущенные проверки

- GitHub Actions runs не проверялись по явной инструкции пользователя.
- Strict run на настоящем raw/registry не запускался как production gate, потому что controlled source migration еще не принято.

### Следующий этап

Следующий этап: `P3.7 Operator reports and acquisition observability`.

## P3.5 - Manual fallback import

Дата: 2026-06-17.

### Статус

- Завершен этап `P3.5 Manual fallback import`.
- Реализован `manual-import` для ручного импорта локального Excel-файла Минфина через canonical option `--manual-file`.
- Импорт через `--download` заблокирован без `--confirm IMPORT_MINFIN_FILE`.
- Валидация manual file проверяет существование файла, `.xlsx`, шаблон имени `INTERNET_Auction_Results_rus_<year>_*.xlsx` и соответствие года `--year`.
- Dry-run manual-import считает `sha256`, размер файла и показывает planned storage role/path без создания raw storage.
- Import использует temp+promote workflow: локальный файл сначала копируется во временный путь, затем валидируется, хэшируется и продвигается.
- Manual import продвигает только `latest`/`versions` по hash-change модели; `final` не перезаписывается и не создается.
- Registry rows для ручного импорта получают `discovery_method=manual-import`, `publication_period=manual-import`; notes содержит `original_local_file=...`.
- Same-hash manual import пишет observation без blind copy и без нового snapshot.
- Smoke test использует только temp XLSX-файлы и удаляет временный каталог после завершения.

### Изменения

- `scripts/source_acquisition/minfin_fetch.py`
- `scripts/source_acquisition/source_registry.py`
- `scripts/source_acquisition/minfin_patterns.py`
- `scripts/qa/minfin_manual_import_smoke.py`
- `docs/07_operations/minfin_source_acquisition.md`
- `docs/06_quality/manual_checks_log.md`
- `docs/00_project/p3_modernization_progress_report.md`

### Проверки

| Проверка | Результат | Примечания |
| --- | --- | --- |
| `py_compile scripts/source_acquisition/minfin_fetch.py` | OK | CLI manual-import path компилируется. |
| `py_compile scripts/qa/minfin_manual_import_smoke.py` | OK | Smoke test компилируется. |
| `scripts/qa/minfin_manual_import_smoke.py` | OK | Проверены dry-run hash/role, блокировка без confirm, successful import, unchanged observation, year mismatch, invalid extension, отсутствие final overwrite. |
| `compileall -q scripts` | OK | Все scripts компилируются. |

### Пропущенные проверки

- Реальный импорт внешнего пользовательского файла не выполнялся; smoke использует temp XLSX bytes.
- GitHub Actions runs не проверялись по явной инструкции пользователя.

### Следующий этап

Следующий этап: `P3.6 Registry integration with legacy pipeline compatibility`.

## P3.4 - Annual finalization

Дата: 2026-06-17.

### Статус

- Завершен этап `P3.4 Annual finalization`.
- Реализован controlled `annual-final` workflow для закрытия предыдущего года.
- Annual-final candidate выбирается из секции 66 по году, XLSX-ссылке `a.file_item` и отсутствию `на DD.MM.YYYY` в заголовке.
- Суффикс имени файла `YYYY1231` не требуется; поддержан финальный файл вида `INTERNET_Auction_Results_rus_2025_20251230.xlsx`.
- При выборе кандидата annual-final предпочтение отдается публикации/изменению в январе-феврале года `year + 1`, но это не является жестким требованием.
- Если final отсутствует, файл продвигается в `final/` после валидации, расчета sha256 и размера.
- Если existing final имеет тот же hash, замена не выполняется.
- Если existing final имеет другой hash, замена блокируется без `--confirm REPLACE_MINFIN_FINAL`.
- Registry row для annual-final пишется со `storage_role=final` и `publication_period=annual-final`; активной строка становится только при создании/подтвержденной замене.
- Реальное скачивание из Минфина не выполнялось; smoke использует fixture HTML и dummy xlsx bytes во временной директории.
- Настоящий `data/raw` не изменялся.

### Изменения

- `scripts/source_acquisition/minfin_fetch.py`
- `scripts/source_acquisition/minfin_html_parser.py`
- `scripts/source_acquisition/minfin_patterns.py`
- `scripts/source_acquisition/path_planning.py`
- `scripts/qa/minfin_annual_final_smoke.py`
- `docs/07_operations/minfin_source_acquisition.md`
- `docs/06_quality/manual_checks_log.md`
- `docs/00_project/p3_modernization_progress_report.md`

### Проверки

| Проверка | Результат | Примечания |
| --- | --- | --- |
| `py_compile scripts/source_acquisition/minfin_fetch.py scripts/source_acquisition/source_registry.py` | OK | CLI annual-final path и registry layer компилируются. |
| `py_compile scripts/qa/minfin_annual_final_smoke.py` | OK | Smoke test компилируется. |
| `scripts/qa/minfin_annual_final_smoke.py` | OK | Проверены no final, same hash, different hash blocked, replacement with confirm в temp root. |
| `compileall -q scripts` | OK | Все scripts компилируются. |
| `ofz-fetch-minfin --year 2025 --mode annual-final --dry-run --no-network` | OK | Dry-run без сети возвращает план без мутаций. |

### Пропущенные проверки

- Реальный `--download --confirm DOWNLOAD_MINFIN_SOURCE`: пропущен, потому что пользователь не давал отдельного разрешения на live download.
- GitHub Actions runs: не проверялись по явной инструкции пользователя.

### Следующий этап

Следующий этап: `P3.5 Manual import and operator workflow`.

## P3.2 - Registry writer с HTML provenance

Дата: 2026-06-17.

### Статус

- Завершен P3.2 Registry writer.
- Реализованы `RegistryRecord` и `RegistryStatus`.
- Реализован CSV/JSON read-write layer для source registry.
- Добавлены hash metadata helpers: `compute_sha256(path)` и `get_file_size(path)`.
- Добавлены helpers для append, active row selection, hash changed/unchanged, superseded records и validation.
- Поддержаны HTML provenance поля: `section_id`, `page_param`, `page_number`, `document_id`, `document_page_url`, `document_title`, `published_at`, `modified_at`, `as_of_date`, `file_url`, `absolute_file_url`, `file_title`, `file_info`, `file_size_text`, `discovery_method`, `pagination_page_count`.
- Настоящий `data/raw/minfin/ofz_auction_results/` не создавался и не изменялся.
- Реальное скачивание не выполнялось.

### Изменения

- `scripts/source_acquisition/source_registry.py`
- `scripts/qa/minfin_source_registry_smoke.py`
- `tests/fixtures/minfin_registry_sample.json`
- `docs/02_data_contracts/minfin_source_registry_contract.md`
- `docs/06_quality/manual_checks_log.md`
- `docs/00_project/p3_modernization_progress_report.md`

### Проверки

| Проверка | Результат | Примечания |
| --- | --- | --- |
| `py_compile scripts/source_acquisition/source_registry.py` | OK | Registry writer компилируется. |
| `py_compile scripts/qa/minfin_source_registry_smoke.py` | OK | Smoke test компилируется. |
| `scripts/qa/minfin_source_registry_smoke.py` | OK | Проверены temp file hash/size, CSV/JSON roundtrip, append, active row selection, unchanged/changed hash, superseded active row. |
| `compileall -q scripts` | OK | Все scripts компилируются. |

### Пропущенные проверки

- `ofz-quality --fast`: пропущен, потому что P3.2 добавляет isolated registry writer и smoke без изменения pipeline behavior.
- `ofz-quality --full`: пропущен, потому что full quality gate не входит в scope registry writer stage.

### Следующий этап

Следующий этап: `P3.3 Monthly acquisition implementation`.

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

Next stage was superseded by CI blocker remediation: GitHub Actions `quality-fast` failed in schema validation on Windows stdout encoding.

## P3.0-pre - CI UTF-8 output fix for schema validation

Date: 2026-06-16.

### Status

- Completed before `P3.PRE.1` and `P3.PRE.2`; GitHub Actions `quality-fast` passed after the workflow update.
- Root cause: Windows runner/Python stdout used a non-UTF-8 encoding while schema validation printed Cyrillic diagnostics, raising `UnicodeEncodeError`.
- P3 source acquisition was not changed.
- `data/raw` was not changed.

### Changes

- Workflow `.github/workflows/quality.yml` sets `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`.
- Workflow PowerShell steps that run Python or installed CLI entry points call `chcp 65001`.
- Workflow runs `ofz-run` before schema validation and quality gate so CI validates generated artifacts created from source inputs rather than relying on ignored outputs being present in Git.
- Added UTF-8 stdout/stderr handling with `errors="replace"` for CLI entry points that print Cyrillic diagnostics.
- Fixed stale dashboard smoke check to search organized dashboard exports recursively under `outputs/dashboards/`.
- Documented the CI console encoding contract in `docs/07_operations/ci_workflow.md`.

### Checks

| Check | Result | Notes |
| --- | --- | --- |
| `py_compile` changed CLI files | OK | `schema_validation.py`, `quality_gate.py`, `run_pipeline.py`, `smoke_tests.py`, `console_encoding.py`. |
| `ofz-schema` normal encoding | OK | 16 schema checks passed. |
| `ofz-schema` with `PYTHONIOENCODING=cp1252` | OK | No `UnicodeEncodeError`; 16 schema checks passed. |
| `compileall -q scripts` | OK | No compile errors. |
| `ofz-quality --fast` | OK | Fast gate passed after recursive dashboard smoke check fix. |
| GitHub Actions run `27620284328` | Failed after encoding fix | UTF-8 output worked; new failure was missing generated `data/processed` and outputs in CI checkout before schema validation. |
| GitHub Actions run `27623278589` | OK | Workflow with `ofz-run` pre-step completed successfully. |

### Next stage

Next stage after successful CI: `P3.PRE.1 Scripts balance/problem audit`.

## P3.PRE.1 - Scripts balance/problem audit

Date: 2026-06-16.

### Status

- Completed pre-P3 scripts balance/problem audit before `P3.PRE.2` and before P3.0 source acquisition.
- P3 source acquisition was not started; `scripts/source_acquisition/` does not exist yet.
- Pipeline behavior was not changed.
- Generated outputs, release artifacts, logs, `data/processed` and `.docm` files were not staged.

### Changes

- Added `scripts/maintenance/audit_scripts_balance.py` as a static audit helper for P3.PRE.1.
- Created `docs/00_project/p3_scripts_balance_audit_report.md`.
- Updated `docs/06_quality/manual_checks_log.md`.

### Findings

- No `shell=True` was found.
- No active imports/references to `scripts.archive` were found in active Python files.
- No hardcoded absolute user paths were found in Python scripts.
- No TODO/FIXME/XXX markers were found in Python scripts.
- No CLI-like active scripts missing `main()` were found.
- No potential direct `data/raw` mutation was found.
- Deferred medium P3.MOD items remain for controlled decomposition of chart/QA monoliths: `scripts/06_build_charts.py`, `scripts/10_build_monthly_charts.py`, `scripts/12_build_revenue_charts.py`, `scripts/html_chart_qa.py`, and `scripts/visual_regression.py`.
- Subprocess usage exists in several active scripts, but static scan found no `shell=True`; keep argument-list invocation and explicit cwd/check handling.

### Checks

| Check | Result | Notes |
| --- | --- | --- |
| `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\audit_scripts_balance.py` | OK | Audit helper compiles. |
| `.\.venv\Scripts\python.exe scripts\maintenance\audit_scripts_balance.py --report` | OK | Generated `docs/00_project/p3_scripts_balance_audit_report.md`. |
| `.\.venv\Scripts\python.exe -m compileall -q scripts` | OK | No compile errors. |

### Skipped checks

- `ofz-quality --fast`: skipped because P3.PRE.1 changed only an audit helper and documentation, with no pipeline behavior change.
- `ofz-quality --full`: skipped because full quality gate is out of scope for the audit helper/report step.

### Next stage

Next stage: `P3.PRE.2 Docs mojibake/encoding audit and UTF-8 normalization`.

## P3.PRE.2 - Docs mojibake/encoding audit and UTF-8 normalization

Date: 2026-06-16.

### Status

- Completed pre-P3 documentation encoding audit before P3.0 source acquisition.
- P3 source acquisition was not started.
- Active Markdown documentation was checked and normalized to UTF-8 where obvious mojibake was mechanically recoverable.
- Archived docs were checked by scope rules but left unchanged when historical.
- Generated outputs, release artifacts, logs, `data/processed`, raw XLSX inputs and `.docm` files were not changed or staged.

### Changes

- Added `scripts/maintenance/audit_docs_encoding.py`.
- Created `docs/00_project/p3_docs_encoding_audit_report.md` with one row per checked Markdown document.
- Normalized mojibake in active documentation, including `README.md`, selected `docs/00_project/*.md`, `docs/03_pipeline/module_decomposition_plan.md`, `docs/06_quality/manual_checks_log.md`, `docs/index.md`, and `prompts/ofz_p3_modernization_step_by_step.md`.
- Kept the literal mojibake pattern list in `prompts/ofz_p3_modernization_step_by_step.md` as intentional audit instruction text.

### Results

- Markdown documents checked: 128.
- Documents normalized to UTF-8: 16.
- Documents normalized with intentional pattern-reference text remaining: 1.
- Documents with no configured mojibake patterns: 111.
- `manual_review_required`: 0.

### Checks

| Check | Result | Notes |
| --- | --- | --- |
| `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\audit_docs_encoding.py` | OK | Audit helper compiles. |
| `.\.venv\Scripts\python.exe scripts\maintenance\audit_docs_encoding.py --report` | OK | Generated `docs/00_project/p3_docs_encoding_audit_report.md`. |
| `git diff --name-only` | OK | Reviewed changed source/docs/helper files. |
| `git diff --name-only | Select-String "outputs|releases|logs|data/processed"` | OK | No generated outputs/release/log/processed data paths in diff. |

### Skipped checks

- `compileall`: skipped because only docs and a targeted audit helper changed; `py_compile` covered the helper.
- `ofz-quality --fast`: skipped because P3.PRE.2 is documentation/encoding only and pipeline behavior was not changed.
- `ofz-quality --full`: skipped because full quality gate is out of scope for the docs encoding audit.

### Next stage

Next stage after P3.PRE.2 commit/push: `P3.0 Source acquisition design`.

## P3.PRE.2 addendum - scripts README encoding normalization

Date: 2026-06-16.

### Status

- Completed follow-up fix for mojibake found by manual review in `scripts/README.md`.
- Root cause: initial P3.PRE.2 scope covered `README.md`, `CHANGELOG.md`, `docs/**/*.md`, `prompts/**/*.md`, and `tools/**/*.md`; `scripts/**/*.md` was not included.
- P3 source acquisition was not started.

### Changes

- Extended `scripts/maintenance/audit_docs_encoding.py` scope to include `scripts/**/*.md`.
- Normalized active `scripts/README.md` to UTF-8 without BOM.
- `scripts/archive/2026-06-15/README.md` was checked and left unchanged because no configured mojibake patterns were found.
- Regenerated `docs/00_project/p3_docs_encoding_audit_report.md`.

### Checks

| Check | Result | Notes |
| --- | --- | --- |
| `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\audit_docs_encoding.py` | OK | Audit helper compiles. |
| `.\.venv\Scripts\python.exe scripts\maintenance\audit_docs_encoding.py --fix-active --report` | OK | Normalized `scripts/README.md` and regenerated report. |
| Unicode-level verification | OK | `scripts/README.md` has 0 configured mojibake pattern hits. |

### Skipped checks

- `compileall`: skipped because only docs and a targeted audit helper changed; `py_compile` covered the helper.
- `ofz-quality --fast`: skipped because this was documentation/encoding only and pipeline behavior was not changed.
- `ofz-quality --full`: skipped because full quality gate is out of scope for the docs encoding follow-up.

### Next stage

Next stage after this addendum commit/push: `P3.0 Source acquisition design`.

## P3.0 - Source acquisition design

Date: 2026-06-16.

### Status

- Completed design-only P3.0 step after P3.PRE.1 and P3.PRE.2.
- P3.PRE.1 status: completed.
- P3.PRE.2 status: completed, including scripts README encoding addendum.
- No downloader code was written.
- No raw files, generated outputs, release artifacts, logs, `data/processed`, or `.docm` files were changed.

### Policy

Accepted and documented required source acquisition policy:

```text
Variant C - hybrid latest + final + version snapshots on hash change
```

### Changes

- Created `docs/02_data_contracts/minfin_source_registry_contract.md`.
- Created `docs/07_operations/minfin_source_acquisition.md`.
- Created `docs/00_project/p3_source_data_roadmap.md`.
- Documented monthly lifecycle, January annual-final lifecycle, storage structure, Git/artifact policy, registry fields, future CLI, integration path, failure behavior, and manual fallback import.

### Source Review

- Minfin source URL: `https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/#tablitsy_po_rezultatam_provedeniya_auktsionov`.
- Fallback URL without anchor checked by user request: `https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction`.
- During P3.0 design review, both source URL variants returned `503 Service Unavailable`; the design documents explicitly treat site unavailability as a normal failure mode that must not mutate local raw storage.

### Checks

| Check | Result | Notes |
| --- | --- | --- |
| `git diff --name-only` | OK | Reviewed docs-only change set. |
| staged generated artifacts filter | OK | No generated outputs/release/log/processed data paths should be staged. |

### Skipped checks

- `py_compile`: skipped because no Python code was changed in P3.0.
- `compileall`: skipped because no Python code was changed in P3.0.
- `ofz-quality --fast`: skipped because this is a docs-only design step.
- `ofz-quality --full`: skipped because full quality gate is out of scope for source acquisition design.

### Next stage

Next stage: `P3.1 Source acquisition skeleton` or the next user-approved P3 implementation step.

## P3.1-pre - P3 prompt/instruction v5 accepted

Date: 2026-06-17.

### Status

- P3 prompt/instruction v5 accepted from `prompts/ofz_p3_modernization_system_prompt_v5.md` and `prompts/ofz_p3_modernization_step_by_step_v5.md`.
- Current status confirmed: P2 modernization is `stable-release-candidate`; P3.PRE.0, P3.0-pre CI UTF-8 fix, P3.PRE.1, P3.PRE.2 and P3.0 Source acquisition design are completed.
- Minfin supplied HTML structure is incorporated into the P3 working rules.
- Target source section confirmed as section/document id `66`, page parameter `page_66`, container `ajax-pagination-content-10090-66`, pagination id `ajax-pagination-10090-66`, anchor `tablitsy_po_rezultatam_provedeniya_auktsionov`, and file links `a.file_item`.
- P3.1 now requires an HTML-aware parser skeleton for local/offline parsing and candidate selection.
- Parser must ignore non-target sections `65`, `38` and `39`; support pagination through `?page_66=N`; resolve relative file URLs against `https://minfin.gov.ru`; use title `на DD.MM.YYYY` for monthly selection; and tolerate annual-final files whose suffix is not `YYYY1231`.
- Canonical entry point remains `ofz-fetch-minfin = "scripts.source_acquisition.minfin_fetch:main"`.
- Canonical manual fallback option remains `--manual-file`.
- P3.1 remains a skeleton/offline dry-run stage: no production download, no raw Excel mutation, and no raw storage directory or `.gitkeep` creation.
- Git/GitHub outside-sandbox-only rule accepted and preserved for all `git` and `gh` commands.
- Next stage: `P3.1 Source acquisition skeleton` with HTML-aware parser.

### Scope

- No code changes.
- No raw data, processed data, generated outputs, release artifacts, logs or source acquisition storage directories changed.
- Token/cost-aware mode preserved: targeted reads, no broad quality gate, no production network/download action.

### Checks

| Check | Result | Notes |
| --- | --- | --- |
| source-of-truth document review | OK | Reviewed P3 progress, source roadmap, Minfin source registry contract, Minfin acquisition operations, manual checks log, `pyproject.toml`, and `.gitignore`. |
| v5 prompt/instruction review | OK | Reviewed the v5 system prompt and step-by-step prompt from `prompts/`. |
| `git status --short --branch` | OK outside sandbox | Real Git state checked from project root outside sandbox. |
| `git log --oneline -5` | OK outside sandbox | Recent history checked from project root outside sandbox. |
| session preflight | OK outside sandbox | Confirmed branch, remote, `gh` version/auth, and GitHub repo view. |

### Skipped checks

- `compileall`: skipped because this is an instruction acceptance/docs-only stage with no Python code changes.
- `ofz-quality --fast`: skipped because no pipeline behavior changed.
- `ofz-quality --full`: skipped because full quality is out of scope for this instruction acceptance step.

## P3.1-pre - P3 prompt/instruction v6 accepted

Дата: 2026-06-17.

### Статус

- Приняты актуальные инструкции P3 v6 из `prompts/ofz_p3_modernization_system_prompt_v6.md` и `prompts/ofz_p3_modernization_step_by_step_v6_ru.md`.
- Подтвержден текущий статус проекта: P2 modernization завершена как `stable-release-candidate`; P3.PRE.0, P3.0-pre CI UTF-8 fix, P3.PRE.1, P3.PRE.2 и P3.0 Source acquisition design завершены.
- Русскоязычная пошаговая инструкция v6 принята как актуальная замена v5.
- Приняты отдельные команды Codex для этапов P3.1-P3.8.
- Принят детализированный план P3.6: `source-registry-mode off|warn|strict`, `allow-legacy-raw`, registry validation, legacy fallback, smoke tests и `ofz-quality --fast`; P3.6 не должна ломать legacy pipeline и не должна требовать live network в data audit.
- HTML-aware parser logic для Минфина сохраняется: целевая секция `id_66` / `page_66` / `ajax-pagination-content-10090-66`, игнорирование секций `65`, `38`, `39`, поддержка pagination через `?page_66=N`, резолв относительных ссылок, monthly title с `на DD.MM.YYYY`, annual-final без требования суффикса `YYYY1231`.
- Canonical entry point остается `ofz-fetch-minfin = "scripts.source_acquisition.minfin_fetch:main"`.
- Canonical manual option остается `--manual-file`.
- P3.1 остается следующим этапом и включает HTML-aware parser skeleton.
- P3.1 не выполняет production download, не меняет `data/raw`, не создает raw storage dirs или `.gitkeep`, и не пишет registry в raw storage.
- Правило Git/GitHub outside-sandbox-only принято и сохраняется для всех команд `git` и `gh`.
- Следующий этап: `P3.1 Source acquisition skeleton` с HTML-aware parser.

### Объем изменений

- Изменена только документация progress report.
- Код, raw data, processed data, generated outputs, release artifacts, logs и source acquisition storage directories не изменялись.
- Token/cost-aware mode сохранен: использованы targeted reads, без широкого quality gate, без production download и без сетевого source acquisition.

### Проверки

| Проверка | Результат | Примечания |
| --- | --- | --- |
| Обзор source-of-truth документов | OK | Перечитаны P3 progress report, source roadmap, Minfin source registry contract, Minfin source acquisition operations, manual checks log, `pyproject.toml`, `.gitignore`. |
| Обзор v6 prompt/instruction | OK | Прочитаны v6 system prompt и русская step-by-step инструкция из `prompts/`. |
| `git status --short --branch` | OK outside sandbox | Реальный Git status проверен из корня проекта outside sandbox. |
| `git log --oneline -5` | OK outside sandbox | Последняя история коммитов проверена из корня проекта outside sandbox. |
| Session preflight | OK outside sandbox | Проверены branch, remote, `gh --version`, `gh auth status`, `gh repo view VinogradovPV/OFZ_ANALYTICS`. |

### Пропущенные проверки

- `compileall`: пропущен, потому что это instruction acceptance/docs-only stage без изменений Python-кода.
- `ofz-quality --fast`: пропущен, потому что поведение pipeline не менялось.
- `ofz-quality --full`: пропущен, потому что full quality gate не входит в scope этого acceptance stage.
## P3.1 - Skeleton source acquisition с HTML-aware parser

Дата: 2026-06-17.

### Статус

- Завершен P3.1 Source acquisition skeleton.
- Создан package `scripts/source_acquisition`.
- Добавлен CLI entry point `ofz-fetch-minfin = "scripts.source_acquisition.minfin_fetch:main"`.
- Добавлен offline HTML-aware parser для страницы Минфина: target section `id_66` / `page_66` / `ajax-pagination-content-10090-66`, ignored sections `65`, `38`, `39`, file links из `a.file_item`, relative URL resolve через `https://minfin.gov.ru`, pagination metadata из `ajax-pagination-10090-66`.
- Добавлен dry-run режим `--html-file`, выбирающий monthly и annual-final кандидатов из fixture.
- Monthly selection выбирает заголовок с `на DD.MM.YYYY`; annual-final selection не требует суффикс `YYYY1231`.
- `--download` намеренно заблокирован на P3.1; production download не выполнялся.
- Raw storage dirs и `.gitkeep` для `data/raw/minfin/ofz_auction_results/` не создавались.
- `data/raw` не изменялся, registry в `data/raw` не писался.

### Изменения

- `scripts/source_acquisition/__init__.py`
- `scripts/source_acquisition/minfin_fetch.py`
- `scripts/source_acquisition/source_registry.py`
- `scripts/source_acquisition/minfin_patterns.py`
- `scripts/source_acquisition/path_planning.py`
- `scripts/source_acquisition/minfin_html_parser.py`
- `scripts/qa/minfin_source_acquisition_smoke.py`
- `tests/fixtures/minfin_auction_page_section_66_sample.html`
- `tests/fixtures/minfin_auction_candidates_expected.json`
- `pyproject.toml`
- `docs/07_operations/minfin_source_acquisition.md`
- `docs/06_quality/manual_checks_log.md`
- `docs/00_project/p3_modernization_progress_report.md`

### Проверки

| Проверка | Результат | Примечания |
| --- | --- | --- |
| `py_compile` source acquisition files | OK | Проверены `minfin_fetch.py`, `minfin_html_parser.py`, `source_registry.py`. |
| `compileall -q scripts` | OK | Все scripts компилируются. |
| `pip install -e .` | OK | Entry point `ofz-fetch-minfin` установлен. |
| `ofz-fetch-minfin --help` | OK | CLI help работает. |
| `ofz-fetch-minfin --year 2026 --mode monthly --dry-run --no-network` | OK | Возвращает non-mutating dry-run plan с warning о пропущенном discovery. |
| `ofz-fetch-minfin --year 2025 --mode annual-final --dry-run --no-network` | OK | Возвращает non-mutating dry-run plan с warning о пропущенном discovery. |
| `ofz-fetch-minfin --year 2026 --mode monthly --dry-run --html-file ...` | OK | Выбран monthly candidate `INTERNET_Auction_Results_rus_2026_20260611.xlsx`. |
| `ofz-fetch-minfin --year 2025 --mode annual-final --dry-run --html-file ...` | OK | Выбран annual-final candidate `INTERNET_Auction_Results_rus_2025_20251230.xlsx`, без требования `YYYY1231`. |
| `scripts/qa/minfin_source_acquisition_smoke.py` | OK | Offline smoke проверяет section 66, ignored sections, pagination, URL resolve, monthly/annual-final selection. |

### Пропущенные проверки

- `ofz-quality --fast`: пропущен, потому что P3.1 добавляет isolated source acquisition skeleton и offline smoke, без изменения pipeline behavior.
- `ofz-quality --full`: пропущен, потому что full quality gate не входит в scope skeleton stage.

### Следующий этап

Следующий этап: `P3.2 Registry writer с HTML provenance`.
## P3.2 - Registry writer с HTML provenance

Дата: 2026-06-17.

### Статус

- Завершен P3.2 Registry writer.
- Реализованы `RegistryRecord` и `RegistryStatus`.
- Добавлены CSV/JSON read-write helpers.
- Добавлены hash/file metadata helpers: `compute_sha256` и `get_file_size`.
- Добавлены helpers для active row selection, changed/unchanged hash detection, superseded active row и validation.
- HTML provenance поля поддержаны в registry record contract.
- Smoke test пишет registry только во временную директорию, не в настоящий `data/raw/minfin/ofz_auction_results/`.
- Реальное скачивание не выполнялось; raw storage не изменялся.

### Изменения

- `scripts/source_acquisition/source_registry.py`
- `scripts/qa/minfin_source_registry_smoke.py`
- `tests/fixtures/minfin_registry_sample.json`
- `docs/02_data_contracts/minfin_source_registry_contract.md`
- `docs/06_quality/manual_checks_log.md`
- `docs/00_project/p3_modernization_progress_report.md`

### Проверки

| Проверка | Результат | Примечания |
| --- | --- | --- |
| `py_compile scripts\source_acquisition\source_registry.py` | OK | Registry writer компилируется. |
| `py_compile scripts\qa\minfin_source_registry_smoke.py` | OK | Smoke test компилируется. |
| `scripts\qa\minfin_source_registry_smoke.py` | OK | Проверены CSV/JSON roundtrip, hash changed/unchanged, active row selection, supersede и validation failure во временной директории. |
| `compileall -q scripts` | OK | Все scripts компилируются. |

### Пропущенные проверки

- `ofz-quality --fast`: пропущен, потому что P3.2 добавляет isolated registry writer и offline smoke, без изменения pipeline behavior.
- `ofz-quality --full`: пропущен, потому что full quality gate не входит в scope registry writer stage.

### Следующий этап

Следующий этап: `P3.3 Monthly acquisition implementation`.
## P3.3 - Monthly acquisition implementation

Дата: 2026-06-17.

### Статус

- Завершена реализация P3.3 Monthly acquisition implementation.
- Добавлен HTTP client на `urllib`: `fetch_page` и `download_file`.
- Реализован controlled monthly workflow: fetch base page, parse section 66, read `page_66` pagination, fetch subsequent pages, select monthly candidate by max `as_of_date`, temp download, validation, SHA-256/file size, hash compare, promote latest/version, registry update and source acquisition report.
- Реальный download требует `--download --confirm DOWNLOAD_MINFIN_SOURCE`.
- `--download` без confirm блокируется до network/raw mutation и возвращает non-zero exit.
- Offline smoke покрывает changed hash, unchanged hash, registry update, latest/version promotion, report write и simulated network failure without raw mutation.
- Реальный download не запускался.

### Изменения

- `scripts/source_acquisition/minfin_fetch.py`
- `scripts/source_acquisition/http_client.py`
- `scripts/source_acquisition/minfin_html_parser.py`
- `scripts/source_acquisition/minfin_patterns.py`
- `scripts/source_acquisition/path_planning.py`
- `scripts/source_acquisition/source_registry.py`
- `scripts/qa/minfin_monthly_acquisition_smoke.py`
- `docs/07_operations/minfin_source_acquisition.md`
- `docs/06_quality/manual_checks_log.md`
- `docs/00_project/p3_modernization_progress_report.md`

### Проверки

| Проверка | Результат | Примечания |
| --- | --- | --- |
| `py_compile minfin_fetch.py http_client.py source_registry.py` | OK | Monthly acquisition modules compile. |
| `py_compile minfin_monthly_acquisition_smoke.py` | OK | Smoke compiles. |
| `minfin_monthly_acquisition_smoke.py` | OK | Offline smoke checks monthly workflow with dummy XLSX bytes and no live network. |
| `compileall -q scripts` | OK | Все scripts компилируются. |
| `ofz-fetch-minfin --year 2026 --mode monthly --dry-run --no-network` | OK | Non-mutating dry-run plan returned. |
| `ofz-fetch-minfin --year 2026 --mode monthly --download` | OK expected block | Command blocked without `DOWNLOAD_MINFIN_SOURCE` before mutation. |

### Пропущенные проверки

- Real download with `--confirm DOWNLOAD_MINFIN_SOURCE`: пропущен, потому что пользователь не давал отдельного разрешения на реальное скачивание.
- `ofz-quality --fast`: пропущен, потому что P3.3 isolated source acquisition workflow не меняет pipeline behavior.
- `ofz-quality --full`: пропущен, потому что full quality gate не входит в scope monthly acquisition implementation stage.

### Следующий этап

Следующий этап: `P3.4 Annual finalization`.
