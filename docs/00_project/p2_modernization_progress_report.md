# Отчет о прогрессе модернизации P2

Дата создания: 2026-06-09.

Этот документ является сводным информационным отчетом по этапам P2 modernization. После каждого P2-этапа сюда добавляется краткий итог: выполненный этап, изменения, проверки, warnings, commits, push, Git status и следующий рекомендуемый этап.

## P2.0 - Starting checkpoint

Дата: 2026-06-09.

### 1. Какой P2-этап выполнен

Выполнен `P2.0 Starting checkpoint`.

### 2. Что изменено

Создан baseline перед началом P2:

- проанализирован `prompts/ofz_p2_modernization_system_prompt_v3.md`;
- подтвержден production-ready candidate baseline;
- зафиксирован P2 execution protocol;
- зафиксирован уточненный порядок P2.0-P2.15;
- создан документ `docs/00_project/p2_starting_checkpoint.md`;
- создан этот сводный progress report.

### 3. Какие проверки прошли

- `git status --short --branch`: branch `main`, remote synced with `origin/main` before P2 docs changes.
- `git branch --show-current`: `main`.
- `git remote -v`: `origin https://github.com/VinogradovPV/OFZ_ANALYTICS.git`.
- `git log --oneline -5`: latest history reviewed.
- `git ls-files data/raw`: 8 raw Excel files tracked.
- `git ls-files outputs`: only skeleton/index files tracked.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\ofz-quality.exe --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- CLI help through `.venv\Scripts\ofz-*.exe`: OK.

### 4. Какие проверки упали

Падений проверок не было.

### 5. Какие warnings documented

- `anomaly_tests` содержит документированные data warnings.
- `visual_regression` пока использует fallback static HTML / Plotly JSON inspection.
- `prompts/ofz_p2_modernization_system_prompt_v3.md` включается как актуальный source prompt asset; старая версия prompt удаляется из активного набора.

### 6. Какие commits созданы

Commit message: `Record P2 starting checkpoint`.

### 7. Р‘С‹Р» Р»Рё push

Push выполняется в `origin/main` после commit P2.0.

### 8. Текущий git status

На момент подготовки P2.0 ожидаемые изменения:

- новый P2 checkpoint doc;
- новый P2 progress report;
- QA reports, обновленные baseline quality gate;
- untracked P2 system prompt, который включается в commit как source prompt asset.

### 9. Подтверждения

- generated outputs not staged: должно быть проверено перед commit;
- `data/raw` tracked: подтверждено;
- CLI entry points still work: подтверждено.

### 10. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.1 Release bundle automation`.

## P2.1 - Release bundle automation

Дата: 2026-06-09.

### 1. Какой P2-этап выполнен

Выполнен `P2.1 Release bundle automation`.

### 2. Что изменено

- создан `scripts/maintenance/build_release_bundle.py`;
- добавлен CLI entry point `ofz-build-release-bundle`;
- добавлено правило `.gitignore` для `releases/`;
- создан `docs/07_operations/release_bundle_plan.md`;
- обновлены README, production runbook и release checklist;
- release bundle создается как внешний artifact и не попадает в Git.

### 3. Какие проверки прошли

- `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\build_release_bundle.py`: OK.
- `.\.venv\Scripts\python.exe scripts\maintenance\build_release_bundle.py --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\python.exe -m pip install -e .`: OK after approved retry.
- `.\.venv\Scripts\ofz-build-release-bundle.exe --help`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.

### 4. Какие проверки упали

Production-проверки не упали. Первый запуск `pip install -e .` внутри sandbox получил permission denied на `%TEMP%`; повтор с разрешением прошел.

### 5. Какие warnings documented

- `telemetry_summary` остается optional до этапа `P2.2 Pipeline telemetry`;
- реальный release bundle не создается без `--include-outputs --confirm BUILD_RELEASE_BUNDLE`;
- generated outputs и `releases/` не коммитятся.

### 6. Какие commits созданы

Commit message: `Add release bundle automation`.

### 7. Р‘С‹Р» Р»Рё push

Push выполняется после commit P2.1.

### 8. Текущий git status

Фиксируется после commit/push P2.1.

### 9. Подтверждения

- generated outputs not staged: проверить перед commit;
- `data/raw` tracked: подтверждено через `git ls-files data/raw`;
- CLI entry points still work: `ofz-build-release-bundle --help` OK, остальные entry points не менялись.

### 10. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.2 Pipeline telemetry`.

## P2.2 - Pipeline telemetry

Дата: 2026-06-09.

### 1. Какой P2-этап выполнен

Выполнен `P2.2 Pipeline telemetry`.

### 2. Что изменено

- создан модуль `scripts/pipeline/telemetry.py`;
- добавлен package marker `scripts/pipeline/__init__.py`;
- `ofz-run` теперь пишет telemetry JSON/MD для полного pipeline run;
- run manifest включает ссылки на telemetry summary;
- release bundle подхватывает telemetry summary через существующую категорию `telemetry_summary`;
- команда `ofz-run` без `--all/--stage/--stages`, но с report params, запускает полный pipeline как production default.

### 3. Какие проверки прошли

Проверки фиксируются после выполнения P2.2 validation commands.

### 4. Какие проверки упали

Падения фиксируются после выполнения P2.2 validation commands.

### 5. Какие warnings documented

- telemetry outputs являются generated artifacts и не коммитятся;
- telemetry summary не заменяет QA scripts, а фиксирует runtime/audit metadata.

### 6. Какие commits созданы

Commit message: `Add pipeline telemetry reporting`.

### 7. Р‘С‹Р» Р»Рё push

Push выполняется после commit P2.2.

### 8. Текущий git status

Фиксируется после commit/push P2.2.

### 9. Подтверждения

- generated outputs not staged: проверить перед commit;
- `data/raw` tracked: проверить перед commit;
- CLI entry points still work: проверить через `ofz-run` и `ofz-quality`.

### 10. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.3 UI launcher contract`.

## P2.2 - Pipeline telemetry validation close-out

Дата: 2026-06-09.

### Итог

`P2.2 Pipeline telemetry` завершен. `ofz-run` пишет runtime telemetry в `outputs/reports/telemetry/`, run manifest содержит ссылки на telemetry JSON/MD, а release bundle automation подхватывает telemetry summary при наличии.

### Фактические проверки

- `.\.venv\Scripts\python.exe -m py_compile scripts\generate_executive_summary.py scripts\pipeline\telemetry.py scripts\run_pipeline.py scripts\run_manifest.py`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `Get-ChildItem outputs/reports/telemetry -Recurse -File`: telemetry JSON/MD files created.

### Зафиксированные telemetry fields

- `run_id`, `started_at`, `finished_at`, `duration_seconds`;
- `stage_durations`;
- `input_row_counts`;
- `output_file_counts`;
- `generated_artifacts_count`, `artifacts_total_size_bytes`;
- `warnings_count`, `errors_count`;
- `cleanup_mode`;
- `quality_gate_results`, `schema_validation_results`;
- `git_commit`, `git_dirty_flag`;
- `raw_data_hashes`.

### Warnings documented

- Telemetry outputs are generated artifacts and are not committed.
- During validation an existing runtime cast issue in `generate_executive_summary.py` was fixed: runtime `cast(pd.Series[Any], ...)` was replaced with non-subscripted `pd.Series`.
- The latest telemetry run was executed with a dirty working tree because P2.2 source changes were intentionally uncommitted during validation.

### Следующий рекомендуемый P2-этап

`P2.3 UI launcher contract`.

### 11. P2.2 validation update

- `py_compile`: OK.
- `compileall`: OK.
- `ofz-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `ofz-quality --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- Latest telemetry summary: `outputs/reports/telemetry/telemetry_20260609_080836_53742514.json` and `.md`.
- Latest run manifest contains telemetry links.
- Initial P2.2 validation run found and fixed a runtime cast issue in `scripts/generate_executive_summary.py`: `pd.Series[Any]` was replaced with runtime-safe `pd.Series` inside `cast`.
- Generated outputs and telemetry reports remain ignored and must not be staged.

## Cost-aware rules accepted / session preflight

Дата: 2026-06-11.

Приняты актуальные рабочие правила:

- `prompts/ofz_p2_modernization_system_prompt_v4_cost_aware.md`;
- `prompts/ofz_p2_modernization_step_by_step_v5_cost_aware.md`.

Текущий статус P2 подтвержден:

- `P2.0 Starting checkpoint`: completed;
- `P2.1 Release bundle automation`: completed;
- `P2.2 Pipeline telemetry`: completed;
- следующий этап: `P2.3 UI launcher contract`.

Session preflight выполнен один раз для текущей рабочей сессии:

- `git status --short --branch`: branch `main`, remote `origin/main`, untracked только новые prompt-инструкции v4/v5;
- `git branch --show-current`: `main`;
- `git remote -v`: `origin https://github.com/VinogradovPV/OFZ_ANALYTICS.git`;
- `git log --oneline -5`: latest commit `1b07100 Add pipeline telemetry reporting`;
- `gh --version`: OK;
- `gh auth status`: OK after approved outside-sandbox check;
- `gh repo view VinogradovPV/OFZ_ANALYTICS`: OK after approved outside-sandbox check;
- CLI help OK: `ofz-run`, `ofz-interactive`, `ofz-quality`, `ofz-clean-outputs`, `ofz-schema`, `ofz-build-release-bundle`.

Cost-aware / credit-aware режим принят:

- session preflight выполняется один раз в начале рабочей сессии;
- docs-only этапы используют Level 0 checks;
- UI source only этапы используют Level 1 checks;
- Python/pipeline/schema/release/telemetry изменения запускают targeted checks;
- full quality gate запускается только по явным триггерам или перед release/final close-out;
- generated outputs и `releases/` никогда не staged/committed.

Следующий этап `P2.3 UI launcher contract` является Level 0 / docs-only, если будет меняться только контрактная документация.

## P2.3 - UI launcher contract

Дата: 2026-06-11.

### 1. Какой P2-этап выполнен

Выполнен `P2.3 UI launcher contract`.

### 2. Что изменено

Создан документ `docs/07_operations/ui_launcher_contract.md`.

Контракт фиксирует:

- UI launcher вызывает только CLI, а не внутренние Python-функции;
- supported CLI: `ofz-run`, `ofz-interactive`, `ofz-quality`, `ofz-clean-outputs`, `ofz-schema`, `ofz-build-release-bundle`;
- валидируемые параметры запуска;
- cleanup modes и обязательный `DELETE_OUTPUTS` для удаления;
- release bundle creation только с `--include-outputs --confirm BUILD_RELEASE_BUNDLE`;
- launcher logs РІ `outputs/reports/launcher/`;
- запрет arbitrary shell command, изменения `data/raw`, commit generated outputs и параллельного fast/full quality gate;
- Word VBA launcher policy: `.bas/.frm` source, `.docm` release artifact;
- PowerShell GUI launcher policy: recommended first UI implementation, safe process arguments.

PowerShell GUI и Word VBA source в P2.3 не создавались.

### 3. Проверочный уровень

Level 0 / docs-only.

### 4. Какие проверки выполнены

- `git status --short --branch`;
- `git diff --name-only`;
- staged generated artifacts check;
- `Select-String` по `docs/07_operations/ui_launcher_contract.md` на ключевые токены.

### 5. Какие проверки skipped и почему

- `compileall`: skipped, Python-код не менялся.
- `ofz-quality --fast`: skipped, Python/pipeline/schema/release/telemetry код не менялся.
- `ofz-quality --full`: skipped, нет release/final close-out trigger.
- `gh auth status` / CLI help: skipped повторно, session preflight уже выполнен и зафиксирован 2026-06-11.

### 6. Warnings documented

- `prompts/ofz_p2_modernization_system_prompt_v4_cost_aware.md` и `prompts/ofz_p2_modernization_step_by_step_v5_cost_aware.md` остаются untracked source prompt files до отдельного решения о commit.
- UI launcher log under `outputs/reports/launcher/` является generated artifact и не коммитится.

### 7. Commit

Commit message: `Document UI launcher contract`.

### 8. Push

Push выполняется после commit P2.3.

### 9. Git status

Фиксируется после commit/push P2.3.

### 10. Подтверждения

- generated outputs not staged: проверить перед commit;
- releases not staged: проверить перед commit;
- `data/raw` tracked: ранее подтверждено, не менялось;
- CLI entry points still work: не требовали повторной проверки по cost-aware rules, session preflight OK.

### 11. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.4 PowerShell GUI launcher MVP`.

## P2.4 - PowerShell GUI launcher MVP

Дата: 2026-06-11.

### 1. Какой P2-этап выполнен

Выполнен `P2.4 PowerShell GUI launcher MVP`.

### 2. Что изменено

Созданы:

- `tools/windows_launcher/ofz_launcher.ps1`;
- `tools/windows_launcher/README.md`.

Обновлены:

- `README.md`;
- `docs/06_quality/manual_checks_log.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

Launcher реализован как безопасная оболочка над CLI:

- вызывает только whitelisted CLI entry points;
- валидирует `project_root`, `.venv`, `pyproject.toml`, `data/raw`, `report_date`, `retrospective_years`, `period_type`, `aggregation_mode` и action;
- по умолчанию выполняет безопасный smoke-check, а GUI открывает только по `-Gui`;
- пишет логи в `outputs/reports/launcher/`;
- блокирует delete cleanup без `DELETE_OUTPUTS`;
- блокирует release bundle creation без `BUILD_RELEASE_BUNDLE`;
- не принимает arbitrary shell command input;
- не создает GitHub release.

### 3. Проверочный уровень

Level 1 / UI source only.

### 4. Какие проверки выполнены

- `git status --short --branch`;
- `powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1`;
- staged generated artifacts check;
- `git diff --name-only`;
- launcher smoke подтвердил environment validation, bad-date block, delete confirmation block, bundle confirmation block, cleanup dry-run, release bundle dry-run и создание launcher log.

### 5. Какие проверки skipped и почему

- `compileall`: skipped, Python-код не менялся.
- `ofz-quality --fast`: skipped, pipeline/schema/release/telemetry Python-код не менялся.
- `ofz-quality --full`: skipped, нет release/final close-out trigger.
- `gh auth status` и CLI help preflight: skipped повторно, session preflight уже выполнен и зафиксирован.

### 6. Warnings documented

- Smoke launcher создает generated log under `outputs/reports/launcher/`; этот файл игнорируется Git.
- `prompts/ofz_p2_modernization_system_prompt_v4_cost_aware.md` и `prompts/ofz_p2_modernization_step_by_step_v5_cost_aware.md` остаются untracked source prompt files до отдельного решения.

### 7. Commit

Commit message: `Add Windows UI launcher MVP`.

### 8. Push

Push выполняется после commit P2.4.

### 9. Git status

Фиксируется после commit/push P2.4.

### 10. Подтверждения

- generated outputs not staged: проверить перед commit;
- releases not staged: проверить перед commit;
- `data/raw` tracked: ранее подтверждено, не менялось;
- CLI entry points still work: session preflight OK; launcher вызывает entry points через `.venv\Scripts`.

### 11. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.5 Word VBA launcher spec and source`.

## P2.5 - Word VBA launcher spec and source

Дата: 2026-06-11.

### 1. Какой P2-этап выполнен

Выполнен `P2.5 Word VBA launcher spec and source`.

### 2. Что изменено

Созданы:

- `docs/07_operations/word_vba_launcher_spec.md`;
- `tools/word_launcher/README.md`;
- `tools/word_launcher/OfzLauncher.bas`.

Обновлены:

- `README.md`;
- `docs/06_quality/manual_checks_log.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

Word VBA launcher source фиксирует:

- `.bas` source можно коммитить;
- `.docm` является release artifact и не коммитится без отдельного artifact policy decision;
- VBA вызывает только whitelisted CLI under `.venv\Scripts`;
- delete cleanup требует `DELETE_OUTPUTS`;
- release bundle creation требует `BUILD_RELEASE_BUNDLE`;
- macro security documented;
- arbitrary shell command input и GitHub Release creation запрещены.

### 3. Проверочный уровень

Level 1 / UI source only.

### 4. Какие проверки выполнены

- `git status --short --branch`;
- reference/status review после P2.4;
- `Select-String` по `tools/word_launcher/OfzLauncher.bas`, `tools/word_launcher/README.md`, `docs/07_operations/word_vba_launcher_spec.md` на ключевые safety-токены;
- staged generated artifacts check.

### 5. Какие проверки skipped и почему

- `compileall`: skipped, Python-код не менялся.
- `ofz-quality --fast`: skipped, pipeline/schema/release/telemetry Python-код не менялся.
- `ofz-quality --full`: skipped, нет release/final close-out trigger.
- Word import smoke: manual-only; автоматический Word UI запуск не выполнялся в этом этапе.

### 6. Warnings documented

- `.docm` не создан и не коммитится.
- Перед использованием Word launcher нужно импортировать `OfzLauncher.bas` в trusted `.docm` и выполнить ручной smoke `OfzSmokeTest`.
- `prompts/ofz_p2_modernization_system_prompt_v4_cost_aware.md` и `prompts/ofz_p2_modernization_step_by_step_v5_cost_aware.md` остаются untracked source prompt files до отдельного решения.

### 7. Commit

Commit message: `Add Word VBA launcher specification`.

### 8. Push

Push выполняется после commit P2.5.

### 9. Git status

Фиксируется после commit/push P2.5.

### 10. Подтверждения

- generated outputs not staged: проверить перед commit;
- releases not staged: проверить перед commit;
- `data/raw` tracked: ранее подтверждено, не менялось;
- CLI entry points still work: session preflight OK; VBA source вызывает только whitelisted CLI paths.

### 11. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.6 UI launcher documentation and artifact policy update`.

## P2.6 - UI launcher documentation and artifact policy update

Дата: 2026-06-11.

### 1. Какой P2-этап выполнен

Выполнен `P2.6 UI launcher documentation and artifact policy update`.

### 2. Что изменено

Обновлены:

- `README.md`;
- `docs/07_operations/production_runbook.md`;
- `docs/07_operations/release_checklist.md`;
- `docs/00_project/artifact_policy.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

Зафиксировано:

- CLI остается главным supported production interface;
- PowerShell GUI launcher является recommended Windows UI MVP;
- Word VBA launcher является optional launcher;
- `.ps1`, `.bas`, `.frm` являются source artifacts;
- `.docm` является release artifact unless explicitly approved;
- launcher logs under `outputs/reports/launcher/` являются generated outputs;
- release bundle остается external artifact under ignored `releases/`;
- UI launcher не заменяет quality gate.

### 3. Проверочный уровень

Level 0 / docs-only.

### 4. Какие проверки выполнены

- `git status --short --branch`;
- docs diff review;
- staged generated artifacts check.

### 5. Какие проверки skipped и почему

- `compileall`: skipped, Python-код не менялся.
- `ofz-quality --fast`: skipped, Python/pipeline/schema/release/telemetry код не менялся.
- `ofz-quality --full`: skipped, нет release/final close-out trigger.

### 6. Warnings documented

- В рабочем дереве уже были незакоммиченные P2.5 source/docs изменения до начала P2.6; P2.6 не выполнял физические cleanup/decomposition действия.
- `tools/word_launcher/` и prompt v4/v5 файлы остаются вне P2.6, если не будут отдельно staged.

### 7. Commit

Commit message: `Document UI launcher usage and artifact policy`.

### 8. Push

Push выполняется после commit P2.6.

### 9. Git status

Фиксируется после commit/push P2.6.

### 10. Подтверждения

- generated outputs not staged: проверить перед commit;
- releases not staged: проверить перед commit;
- `data/raw` tracked: ранее подтверждено, не менялось;
- CLI entry points still work: session preflight OK, Python-код не менялся.

### 11. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.7 Screenshot visual regression backend`.
## P2.6.1 - PowerShell GUI launcher hardening close-out

Дата: 2026-06-11.

### 1. Какой P2-этап выполнен

Выполнен обязательный промежуточный этап `P2.6.1 PowerShell GUI launcher hardening close-out`.

### 2. Исходный gap

После P2.4 PowerShell GUI launcher был функциональным smoke-wrapper, но GUI содержал только `Report date` и `Action`. Этого было недостаточно для production-like ручного запуска, потому что нельзя было выбирать:

- `project_root`;
- `retrospective_years`;
- `period_type`;
- `aggregation_mode`;
- cleanup mode;
- release/delete confirmation tokens;
- open outputs/release folders;
- command preview.

Также GUI закрывался автоматически через таймер, что было допустимо для проверки, но неверно для ручной работы.

### 3. Что изменено

Обновлены:

- `tools/windows_launcher/ofz_launcher.ps1`;
- `tools/windows_launcher/README.md`;
- `README.md`;
- `docs/06_quality/manual_checks_log.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

GUI теперь содержит:

- project root;
- report date;
- retrospective years;
- period type;
- aggregation mode;
- action;
- cleanup mode;
- schema/quality/release options;
- `DELETE_OUTPUTS` confirmation;
- `BUILD_RELEASE_BUNDLE` confirmation;
- command preview;
- output/status area;
- launcher log path.

### 4. Safety policy

Сохранено:

- только approved CLI entry points;
- no arbitrary shell command;
- no internal Python function calls;
- no `data/raw` changes;
- no GitHub Release creation;
- no fast/full quality gate parallel run;
- delete cleanup blocked without `DELETE_OUTPUTS`;
- release-build blocked without `BUILD_RELEASE_BUNDLE`.

### 5. Проверочный уровень

Level 1 / UI source only.

### 6. Какие проверки выполнены

- PowerShell parse check for `tools/windows_launcher/ofz_launcher.ps1`: OK;
- `powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1`: OK;
- `powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Gui -AutoCloseGuiForCheck`: OK;
- smoke подтвердил environment validation, bad date block, delete confirmation block, release confirmation block, cleanup dry-run, release bundle dry-run и launcher log creation.

### 7. Какие проверки skipped и почему

- `compileall`: skipped, Python-код не менялся.
- `ofz-quality --fast`: skipped, UI source only.
- `ofz-quality --full`: skipped, нет release/final close-out trigger.
- Ручной interactive GUI smoke пользователем остается желательным: открыть `-Gui`, проверить поля и нажать `Validate`.

### 8. Warnings documented

- `tools/word_launcher/` и prompt v4/v5/v6 файлы остаются вне этого этапа, если отдельно не staged.
- Запуск smoke создает generated logs under `outputs/reports/launcher/` и cleanup dry-run manifests under `outputs/reports/cleanup/`; они игнорируются Git.

### 9. Commit

Commit message: `Enhance Windows UI launcher parameters`.

### 10. Push

Push выполняется после commit P2.6.1.

### 11. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап после закрытия launcher gap: `P2.7 Screenshot visual regression backend`.

## P2.6.2 - Word VBA docm assembly and UserForm

Дата: 2026-06-11.

### 1. Какой P2-этап выполнен

Выполнен обязательный промежуточный этап `P2.6.2 Word VBA docm assembly and UserForm`.

### 2. Что изменено

Обновлены и добавлены:

- `tools/word_launcher/OfzLauncher.bas`;
- `tools/word_launcher/frmOfzLauncher.frm`;
- `tools/word_launcher/word_docm_build_instructions.md`;
- `tools/word_launcher/README.md`;
- `docs/07_operations/word_vba_launcher_spec.md`;
- `docs/07_operations/release_checklist.md`;
- `docs/00_project/artifact_policy.md`;
- `docs/06_quality/manual_checks_log.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

`OfzLauncher.bas` теперь содержит required `OFZ_*` procedures/functions, validation, command preview/build logic, safe CLI-only process execution and launcher logging.

`frmOfzLauncher.frm` содержит source UserForm `frmOfzLauncher` с required controls for project root, report params, action, confirmation tokens, command preview, log output and action buttons.

### 3. Artifact status

- `.bas` / `.frm` / build instructions are source artifacts.
- `.docm` is a release artifact.
- Recommended `.docm` path: `releases/ui_launcher/ofz_launcher_word_<timestamp>.docm`.
- `.docm` and `releases/` must not be committed.

### 4. Проверочный уровень

Level 1 / UI source only.

### 5. Какие проверки выполнены

- required `OFZ_*` procedure/function scan in `OfzLauncher.bas`;
- required UserForm control scan in `frmOfzLauncher.frm`;
- `.docm` / `releases/` not staged check before commit;
- generated outputs not staged check before commit.

### 6. Какие проверки skipped и почему

- Word automation/manual import: skipped in this environment; `.docm` assembly is `deferred/manual`.
- `compileall`: skipped, Python-код не менялся.
- `ofz-quality --fast`: skipped, UI source/docs only.
- `ofz-quality --full`: skipped, нет release/final close-out trigger.

### 7. Warnings documented

- `.docm` must be assembled manually in Word or by a controlled Word automation step on an operator workstation.
- Macros can be blocked; use Trusted Location and consider code signing.
- Word launcher does not accept arbitrary shell commands and calls only whitelisted CLI.
- Delete cleanup requires `DELETE_OUTPUTS`.
- Release bundle creation requires `BUILD_RELEASE_BUNDLE`.

### 8. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап после закрытия Word launcher gap: `P2.7 Screenshot visual regression backend`.

## P2.7 - Screenshot visual regression backend

Дата: 2026-06-11.

### 1. Какой P2-этап выполнен

Выполнен `P2.7 Screenshot visual regression backend`.

### 2. Что изменено

Обновлены:

- `scripts/visual_regression.py`;
- `requirements-dev.txt`;
- `pyproject.toml`;
- `README.md`;
- `docs/06_quality/visual_regression_backend_decision.md`;
- `docs/07_operations/release_checklist.md`;
- `docs/06_quality/manual_checks_log.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

### 3. Backend decision

Основное решение: Playwright screenshot backend для локальных HTML/Plotly charts.

Fallback static HTML / Plotly JSON inspection сохранен как резервный и контрактный режим.

Поддержанные режимы:

- `--mode fallback`;
- `--mode screenshot`;
- `--mode auto`.

`auto` сначала пытается использовать Playwright, а если backend или browser binaries недоступны, явно фиксирует warning и переходит в fallback.

### 4. Generated artifacts

Screenshot backend пишет generated outputs:

- `outputs/reports/visual_regression/screenshots/<run_id>/*.png`;
- `outputs/reports/visual_regression/screenshot_manifest_*.json`;
- `outputs/reports/visual_regression/diffs/screenshot_diff_report_*.md`.

Эти файлы не коммитятся.

### 5. Проверочный уровень

Level 3 initially. Level 5 only after backend stabilization and explicit full-gate trigger.

### 6. Какие проверки выполнены

- `.\.venv\Scripts\python.exe -m py_compile scripts\visual_regression.py`: OK.
- `.\.venv\Scripts\python.exe scripts\visual_regression.py --mode fallback --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\python.exe scripts\visual_regression.py --mode auto --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK, with documented Playwright-unavailable warning and fallback.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- Pylance missing-import issue for `playwright.sync_api`: fixed by replacing direct optional imports with dynamic `importlib.import_module`.

### 7. Какие warnings documented

- Playwright is not installed in the current `.venv`; `--mode auto` uses fallback and records a warning.
- Screenshot mode requires `requirements-dev.txt` plus `python -m playwright install chromium`.
- Screenshot PNG/manifest/diff outputs are generated artifacts and must not be committed.
- Missing baseline screenshots are recorded as `missing_baseline`, not as a failure during backend stabilization.

### 7.1. Screenshot backend follow-up after manual Playwright installation

Дата: 2026-06-16.

Пользователь вручную подтвердил локальную установку Playwright/Chromium в проектной PowerShell-сессии:

- `.\.venv\Scripts\python.exe -m playwright --version`: OK, Playwright `1.60.0`;
- smoke script with `sync_playwright`, headless Chromium and `page.screenshot(path='playwright_smoke.png')`: OK.

Код `scripts/visual_regression.py` обновлен:

- Playwright launch uses stable headless flags and `domcontentloaded` instead of `networkidle` for standalone Plotly HTML;
- reports now include `screenshot_backend`;
- Codex managed sandbox is detected and `--mode auto` uses fallback with a documented warning instead of emitting noisy subprocess tracebacks;
- optional direct Chromium CLI fallback exists only behind `OFZ_VISUAL_REGRESSION_CHROMIUM_CLI_FALLBACK=1`.

Проверки в Codex sandbox:

- `.\.venv\Scripts\python.exe -m py_compile scripts\visual_regression.py scripts\qa\visual_regression_contracts.py`: OK;
- `.\.venv\Scripts\python.exe scripts\visual_regression.py --mode fallback --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK;
- `.\.venv\Scripts\python.exe scripts\visual_regression.py --mode auto --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK, fallback warning expected in Codex sandbox.

Direct `--mode screenshot` must be validated from the project PowerShell session, where the user already confirmed Playwright smoke execution. `playwright_smoke.png` is a generated local artifact and must not be committed.

### 8. Следующий рекомендуемый P2-этап

После завершения P2.7 и стабилизации проверок: `P2.8 CI / GitHub Actions`.

## P2.8 - CI / GitHub Actions

Дата: 2026-06-11.

### 1. Какой P2-этап выполнен

Выполнен `P2.8 CI / GitHub Actions`.

### 2. Что изменено

Добавлены и обновлены:

- `.github/workflows/quality.yml`;
- `docs/07_operations/ci_workflow.md`;
- `README.md`;
- `docs/07_operations/release_checklist.md`;
- `docs/06_quality/manual_checks_log.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

### 3. CI contract

Workflow запускает `quality-fast` на `push`/`pull_request` в `main` и через `workflow_dispatch`.

`quality-fast` выполняет checkout, setup Python, install runtime/dev dependencies, editable install, `pip check`, `compileall`, `ofz-schema` и `ofz-quality --fast`.

`quality-full` доступен только вручную через `workflow_dispatch`, зависит от `quality-fast` и не запускается параллельно с fast job.

### 4. Artifact policy

CI не коммитит generated outputs. QA reports сохраняются как GitHub Actions artifacts. Кешируется только pip cache; `outputs/` и `releases/` не кешируются.

### 5. Проверочный уровень

Level 2 locally. GitHub-side validation через `gh workflow list` / `gh run list` после push.

### 6. Какие проверки выполнены

- `.\.venv\Scripts\python.exe -m pip check`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK, 16/16 checks passed.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- staged generated artifacts check: OK before commit.
- GitHub-side `gh workflow list` / `gh run list`: planned after push.

### 7. Warnings documented

Screenshot backend browser binaries are not installed in CI during P2.8. Local fast gate completed with expected warning: screenshot backend unavailable and visual regression used fallback/static inspection mode.

### 8. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.9 Controlled docs archive apply`.

## P2.9 - Controlled docs archive apply

Дата: 2026-06-15.

### 1. Какой P2-этап выполнен

Выполнен `P2.9 Controlled docs archive apply`.

### 2. Что изменено

Обновлены и созданы:

- `scripts/maintenance/cleanup_docs.py`;
- `scripts/quality_gate.py`;
- `docs/index.md`;
- `docs/00_project/docs_inventory_before_cleanup.md`;
- `docs/00_project/docs_inventory_after_cleanup.md`;
- `docs/00_project/docs_archive_apply_report.md`;
- `docs/archive/2026-06-15/`;
- `README.md`.

### 3. Результат cleanup

После повторного dry-run активные P2 operation docs сохранены как `keep_active`, а legacy diagnostics/stage/reproducibility reports переведены в controlled archive.

Итог archive mode:

- `keep_active`: 61 documents;
- `archive_candidate`: 39 documents;
- archive folder: `docs/archive/2026-06-15/`;
- `--delete-archived`: not executed.

### 4. Что не делалось

- Generated cleanup manifests under `outputs/reports/cleanup/` are not committed.
- No archived docs were deleted.
- No scripts were moved or deleted.
- P2.10 legacy scripts archive remains a separate controlled stage.

### 5. Проверки

- `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\cleanup_docs.py scripts\quality_gate.py`: OK.
- `.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --dry-run`: OK.
- `.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --archive`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.

### 6. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.10 Controlled legacy scripts archive apply`.

## P2.10 - Controlled legacy scripts archive apply

Дата: 2026-06-15.

### 1. Какой P2-этап выполнен

Выполнен `P2.10 Controlled legacy scripts archive apply`.

### 2. Что изменено

Пять legacy maintenance scripts перенесены в `scripts/archive/2026-06-15/`:

- `cleanup_docs.py`;
- `migrate_outputs_structure.py`;
- `reorganize_outputs.py`;
- `migrate_legacy_docs_archive.py`;
- `reorganize_docs.py`.

Добавлен `scripts/archive/2026-06-15/README.md`.

Обновлены active docs so old scripts are no longer presented as production commands:

- `README.md`;
- `scripts/README.md`;
- `docs/00_project/scripts_archive_decision.md`;
- `docs/00_project/scripts_inventory_before_cleanup.md`;
- `docs/00_project/scripts_structure_plan.md`;
- `docs/00_project/scripts_migration_plan.md`;
- `docs/00_project/outputs_structure.md`;
- `docs/00_project/production_readiness_report.md`;
- `docs/00_project/final_project_summary.md`;
- `docs/03_pipeline/module_decomposition_plan.md`.

### 3. Что не делалось

- No files were deleted.
- No production entry points were changed.
- Generated outputs were not staged.
- Physical module decomposition remains P2-only.

### 4. Проверки

- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- CLI help checks for `ofz-run`, `ofz-quality`, `ofz-clean-outputs`, `ofz-schema`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.

### 5. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.11 Controlled module decomposition`.

## P2.11.1 - Chart common helpers

Дата: 2026-06-15.

### 1. Какой P2-этап выполнен

Выполнен первый малый шаг `P2.11 Controlled module decomposition`: `P2.11.1 Chart common helpers`.

### 2. Что изменено

Создан пакет `scripts/charts/`:

- `scripts/charts/__init__.py`;
- `scripts/charts/common.py`.

Из `scripts/06_build_charts.py` вынесены только pure formatting helpers:

- `format_number_text`;
- `format_hover_number`;
- `format_bln`;
- `format_percent_label`;
- `format_metric_value`;
- `format_signed_metric_value`;
- `format_ru_number`.

`scripts/06_build_charts.py` остается стабильным wrapper/orchestrator. CLI behavior, output filenames, chart contracts and schema contracts were not changed.

### 3. Что не делалось

- No chart family builders were moved.
- No QA modules were extracted.
- No output filename changes.
- No generated outputs were staged.
- Physical module decomposition remains incremental: one small extraction per commit.

### 4. Проверки

- `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py scripts\charts\common.py scripts\charts\__init__.py`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.

### 5. Warnings documented

Visual regression in `auto` mode recorded the known warning that the screenshot backend was unavailable in the current environment and fallback static inspection was used.

### 6. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.11.2 Chart family modules`, but only as another small extraction with the same no-behavior-change rule.

## P2.11.2 - Chart family module skeleton

Дата: 2026-06-15.

### 1. Какой P2-этап выполнен

Выполнен второй малый шаг `P2.11 Controlled module decomposition`: создан behavior-neutral skeleton для chart-family modules.

### 2. Что изменено

Добавлены family modules:

- `scripts/charts/structure.py`;
- `scripts/charts/scatter.py`;
- `scripts/charts/monthly.py`;
- `scripts/charts/revenue.py`;
- `scripts/charts/boxplot.py`.

В `scripts/charts/__init__.py` добавлен список `CHART_FAMILY_MODULES`.

### 3. Что не делалось

- Chart builders не переносились из `scripts/06_build_charts.py`.
- Monthly builders не переносились из `scripts/10_build_monthly_charts.py`.
- Output filenames, CLI behavior, chart contracts and schema contracts were not changed.
- Generated outputs were not staged.

### 4. Проверки

- `.\.venv\Scripts\python.exe -m py_compile scripts\charts\__init__.py scripts\charts\structure.py scripts\charts\scatter.py scripts\charts\monthly.py scripts\charts\revenue.py scripts\charts\boxplot.py`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.

### 5. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: первый реальный перенос одной небольшой chart family или pure-helper группы в созданные modules.

## P2.11.3 - QA contract modules

Дата: 2026-06-15.

### 1. Какой P2-этап выполнен

Выполнен третий малый шаг `P2.11 Controlled module decomposition`: созданы QA contract modules для HTML QA и visual regression.

### 2. Что изменено

Создан пакет `scripts/qa/`:

- `scripts/qa/__init__.py`;
- `scripts/qa/html_chart_contracts.py`;
- `scripts/qa/visual_regression_contracts.py`.

Из `scripts/html_chart_qa.py` вынесены contract constants и `QaResult`.

Из `scripts/visual_regression.py` вынесены visual contract constants и `VisualCheck`.

### 3. Что не делалось

- Check functions не переносились.
- CLI behavior не менялся.
- Chart data/schema contracts не менялись.
- Generated outputs were not staged.

### 4. Проверки

- `.\.venv\Scripts\python.exe -m py_compile scripts\html_chart_qa.py scripts\visual_regression.py scripts\qa\__init__.py scripts\qa\html_chart_contracts.py scripts\qa\visual_regression_contracts.py`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.

### 5. Warnings documented

Visual regression in `auto` mode recorded the known warning that the screenshot backend was unavailable in the current environment and fallback static inspection was used.

### 6. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: продолжить P2.11 small extractions by moving one small QA check group or one chart helper group per commit.

## P2.12 - Windows setup / Docker plan

Дата: 2026-06-16.

### 1. Какой P2-этап выполнен

Выполнен `P2.12 Windows setup / Docker plan`.

### 2. Что изменено

Добавлены:

- `tools/setup/setup_windows.ps1`;
- `docs/07_operations/windows_setup.md`;
- `docs/07_operations/docker_plan.md`.

Обновлены:

- `README.md`;
- `docs/06_quality/manual_checks_log.md`.

### 3. Windows setup workflow

`setup_windows.ps1` поддерживает:

- проверку PowerShell version;
- создание `.venv`, если она отсутствует;
- установку `requirements.txt`;
- опциональную установку `requirements-dev.txt` через `-IncludeDev`;
- `pip install -e .`;
- `pip check`;
- CLI help checks для `ofz-*`;
- `compileall`;
- optional fast quality gate только через `-RunFastQuality`.

Скрипт не трогает `outputs/` и не запускает cleanup без отдельной команды.

### 4. Docker plan

Docker зафиксирован как optional path. Windows-first остается основным production setup.

Docker plan описывает:

- UTF-8 locale и русские шрифты;
- browser dependencies для screenshot visual regression;
- read-only mount strategy для `data/raw`;
- mount strategy для generated `outputs`;
- release bundle path через external `releases/`;
- риски различий rendering/fonts/file permissions.

### 5. Проверки

Выполненные проверки P2.12:

- `powershell -NoProfile -ExecutionPolicy Bypass -File tools/setup/setup_windows.ps1 -DryRun`: OK.
- Actual setup command not run on the current machine because `.venv` already exists and a real setup run would mutate the local environment; it is intended for a clean/new machine.
- generated outputs staging filter before commit.

### 6. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.13 BI-ready release package` или продолжение `P2.11` small module decomposition только отдельным малым commit.

## P2.13 - BI-ready release package

Дата: 2026-06-16.

### 1. Какой P2-этап выполнен

Выполнен `P2.13 BI-ready release package`.

### 2. Что изменено

Добавлены:

- `scripts/maintenance/build_bi_package.py`;
- `docs/07_operations/bi_release_package.md`;
- `docs/02_data_contracts/bi_exports_contract.md`.

Обновлены:

- `README.md`;
- `docs/06_quality/manual_checks_log.md`.

### 3. Поведение BI package

BI package собирается как external artifact в:

```text
releases/bi/ofz_analytics_bi_<report_date>_<period_type>_<aggregation_mode>_r<N>_<timestamp>/
```

Build mode требует `--include-outputs --confirm BUILD_BI_PACKAGE`. Если required datasets отсутствуют, build mode завершается с non-zero exit code и не заменяет отсутствующие данные пустыми файлами.

### 4. Состав

Скрипт включает dashboard exports, semantic model v2, analytical CSV, monthly metrics, revenue analytics CSV, chart data CSV, data/KPI dictionaries и generated BI dimensions: period, OFZ type и placement format.

### 5. Проверки

Выполненные проверки P2.13:

- `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\build_bi_package.py`: OK.
- `.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- dry-run found 13 dashboard exports, 4 semantic model files, 9 analytical CSV files, 1 monthly metrics CSV, 5 revenue analytics CSV files, 60 chart data CSV files, 3 data dictionary files and 2 KPI dictionary files.
- generated helper dimensions: 20 period rows, 2 OFZ type rows, 2 placement format rows.
- generated outputs and `releases/` staging filter before commit.

### 6. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.14 Archive deletion policy`.

## P2.14 - Archive deletion policy

Дата: 2026-06-16.

### 1. Какой P2-этап выполнен

Выполнен `P2.14 Archive deletion policy`.

### 2. Что изменено

Добавлен документ:

- `docs/00_project/archive_deletion_policy.md`.

### 3. Зафиксированные правила

- Archived docs/scripts не удаляются в production-ready candidate.
- Физическое удаление разрешено только после stable release.
- Перед удалением нужны release tag, release bundle, references check и archive manifest.
- `--delete-archived` запрещен без explicit approval пользователя.
- Удаление должно выполняться отдельным commit.

### 4. Проверки

P2.14 является Level 0 / docs-only этапом:

- `git status --short --branch`: checked before edits.
- generated artifacts staging filter before commit.
- `compileall` and quality gates skipped because Python code was not changed.

### 5. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.15 P2 completion report`.

## P2.15 - P2 completion report

Дата: 2026-06-16.

### 1. Какой P2-этап выполнен

Выполнен `P2.15 P2 completion report`.

### 2. Что изменено

Добавлен документ:

- `docs/00_project/p2_completion_report.md`.

Обновлены final QA reports:

- `docs/06_quality/quality_gate_report.md`;
- `docs/06_quality/anomaly_tests_report.md`.

### 3. Финальные проверки

- `.\.venv\Scripts\python.exe -m pip install -e .`: OK after outside-sandbox rerun; initial sandbox attempt failed on Windows temp permission.
- `.\.venv\Scripts\python.exe -m pip check`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK, 16 checks passed.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\ofz-quality.exe --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\ofz-build-release-bundle.exe --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.

### 4. Warnings documented

- Visual regression used fallback in Codex managed sandbox because screenshot backend is intentionally skipped there; run from normal project PowerShell to exercise local Playwright/Chromium.
- Anomaly tests reported data-quality warnings for known domain cases such as missing yield, demand outliers, zero/missing demand and missing cutoff price.

### 5. Recommendation

P2 close-out recommendation: `stable-release-candidate`.
