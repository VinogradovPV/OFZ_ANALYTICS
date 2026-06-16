# OFZ_ANALYTICS: P2 modernization step-by-step v6
## Полная инструкция P2.7-P2.15 + launcher gap close-out + Git outside-sandbox policy

Дата актуализации: 2026-06-11.

---

## 0. Назначение v6

Эта версия заменяет v5 как актуальная рабочая инструкция для Codex.

Исправления v6:

1. Добавлена полная детализация этапов `P2.7-P2.15`.
2. Учтено, что `P2.0-P2.6` уже выполнены.
3. Добавлен промежуточный этап `P2.6.1 Launcher hardening close-out`, потому что текущий PowerShell GUI launcher слишком минималистичный.
4. Добавлен этап `P2.6.2 Word VBA docm assembly`, потому что после `P2.5` создан `.bas` source/spec, но не создан рабочий `.docm` с UserForm.
5. Зафиксировано, что Git/GitHub команды должны выполняться **вне sandbox**, точечно и с явным запросом.
6. Сохранен cost-aware режим: не гонять дорогие проверки без триггера.

---

## 1. Текущий статус P2

Перед началом следующего этапа Codex должен прочитать:

```text
docs/00_project/p2_modernization_progress_report.md
docs/00_project/p2_starting_checkpoint.md
docs/00_project/production_readiness_report.md
docs/06_quality/manual_checks_log.md
docs/07_operations/release_bundle_plan.md
docs/07_operations/release_checklist.md
README.md
```

Текущий статус по progress report:

```text
P2.0 Starting checkpoint: completed
P2.1 Release bundle automation: completed
P2.2 Pipeline telemetry: completed
Cost-aware rules accepted / session preflight: completed
P2.3 UI launcher contract: completed
P2.4 PowerShell GUI launcher MVP: completed
P2.5 Word VBA launcher spec and source: completed
P2.6 UI launcher documentation and artifact policy update: completed
```

Вывод:

```text
1. Следующий этап НЕ должен быть сразу P2.7.
2. Перед P2.7 нужно закрыть launcher gaps:
   - P2.6.1: доработать PowerShell GUI launcher, потому что текущий интерфейс не дает выбрать все параметры запуска.
   - P2.6.2: собрать Word .docm launcher с импортом .bas и UserForm.
3. Только после P2.6.1 и P2.6.2 переходить к P2.7 Screenshot visual regression backend.
```

---

## 2. Git / GitHub outside-sandbox policy

### 2.1. Правило

Git/gh команды считать outside-sandbox operations.

Codex не должен пытаться делать Git/GitHub проверки внутри sandbox, если уже известно, что там нет доступа к реальному `.git`, network или credentials.

### 2.2. Рабочая директория

Все Git/GitHub команды выполнять из корня проекта:

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics
```

Если `git remote -v` запущен вне репозитория и падает:

```text
fatal: not a git repository (or any of the parent directories): .git
```

это не ошибка GitHub CLI, а неверная рабочая директория.

### 2.3. Outside-sandbox preflight

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics

git status --short --branch
git branch --show-current
git remote -v
git log --oneline -5

gh --version
gh auth status
gh repo view VinogradovPV/OFZ_ANALYTICS
```

### 2.4. Outside-sandbox commit/push block

Перед commit:

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics

git status --short
git diff --name-only
git diff --cached --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|data/processed|logs|releases"
```

Если generated artifacts попали в staged:

```powershell
git reset HEAD outputs/charts outputs/exports outputs/reports outputs/dashboards outputs/archive outputs/tmp outputs/cache data/processed logs releases
git add outputs/**/.gitkeep
git add outputs/charts/index.md
```

Commit/push:

```powershell
git add <только нужные source/docs/scripts files>
git commit -m "<message>"
git push
git status --short --branch
```

### 2.5. Запреты

Требуют отдельной команды пользователя:

```text
gh pr create
gh pr merge
gh release create
gh release upload
gh workflow run
gh secret set
gh variable set
gh repo edit
```

Запрещено всегда:

```text
gh repo delete
gh repo edit --visibility public
force push
commit generated outputs
commit releases/
commit .docm без explicit artifact policy approval
```

---

## 3. Cost-aware проверочные уровни

### Level 0 — docs-only

Если менялись только `.md`, `.txt`, prompt/policy docs, README sections, progress report или manual checks:

```powershell
git status --short
git diff --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|data/processed|logs|releases"
```

Не запускать `compileall`, `ofz-quality --fast`, `ofz-quality --full`.

### Level 1 — UI source only

Если менялись `.ps1`, `.bas`, `.frm`, launcher docs:

```text
PowerShell launcher smoke
VBA source review/import check
staged generated artifacts check
```

`ofz-quality --fast` не нужен, если Python pipeline не менялся.

### Level 2 — Python utility changed

```powershell
.\.venv\Scripts\python.exe -m py_compile <changed_python_files>
.\.venv\Scripts\python.exe -m compileall -q scripts
```

### Level 3 — pipeline / QA / schema / release / telemetry changed

Targeted checks + `ofz-quality --fast`, если затронут production path.

### Level 4 — package / dependencies / CLI changed

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\ofz-run.exe --help
.\.venv\Scripts\ofz-interactive.exe --help
.\.venv\Scripts\ofz-quality.exe --help
.\.venv\Scripts\ofz-clean-outputs.exe --help
.\.venv\Scripts\ofz-schema.exe --help
.\.venv\Scripts\ofz-build-release-bundle.exe --help
```

### Level 5 — full gate

Запускать только перед external release, после P2.7 backend stabilization, после P2.11 module decomposition, перед P2.15 completion report или по прямой команде пользователя.

---

# P2.6.1 — PowerShell GUI launcher hardening close-out

## Статус

Новый обязательный промежуточный этап перед P2.7.

## Проверочный уровень

```text
Level 1 / UI source only
```

## Цель

Довести PowerShell GUI launcher до реального parameterized launcher.

По текущему скриншоту GUI содержит только `Report date` и `Action`, поэтому не позволяет выбирать:

```text
retrospective_years
period_type
aggregation_mode
project_root
cleanup mode
release bundle creation confirm
quality full/manual mode
open outputs/release folders
```

## Требования к GUI

GUI должен содержать:

```text
Project root
Report date
Retrospective years
Period type
Aggregation mode
Action
Cleanup mode
Run schema validation
Run quality gate fast
Run quality gate full, manual only
Build release bundle
Open outputs folder after run
Open release folder after bundle
Confirm DELETE_OUTPUTS
Confirm BUILD_RELEASE_BUNDLE
Command preview
Output/status area
```

### Defaults

```text
ProjectRoot = C:\Users\Rockaudit\LLM_CHAT\ofz_analytics
ReportDate = 2026-05-01
RetrospectiveYears = 4
PeriodType = month
AggregationMode = cumulative
Action = validate-environment
```

### Action dropdown

```text
validate-environment
run-pipeline
schema
quality-fast
quality-full
cleanup-dry-run
cleanup-archive-all
cleanup-delete-all
release-dry-run
release-build
open-outputs
open-releases
```

## Запрещено

```text
Не принимать arbitrary shell command.
Не вызывать внутренние Python functions.
Не менять data/raw.
Не создавать GitHub release.
Не запускать fast/full quality gate параллельно.
Не выполнять delete без DELETE_OUTPUTS.
Не выполнять release-build без BUILD_RELEASE_BUNDLE.
```

## Команда для Codex

```text
Выполни P2.6.1 PowerShell GUI launcher hardening close-out.

Перед началом:
1. Прочитай docs/00_project/p2_modernization_progress_report.md.
2. Подтверди, что P2.6 completed.
3. Подтверди, что текущий PowerShell GUI launcher не дает выбрать retrospective_years, period_type, aggregation_mode и другие параметры.
4. Не переходи к P2.7 до закрытия launcher gap.
5. Git/gh команды выполняй outside-sandbox, только точечно.

Измени:
- tools/windows_launcher/ofz_launcher.ps1
- tools/windows_launcher/README.md
- README.md, если нужно
- docs/06_quality/manual_checks_log.md, если выполнялись ручные проверки
- docs/00_project/p2_modernization_progress_report.md

Сделай GUI parameterized:
- project_root
- report_date
- retrospective_years
- period_type
- aggregation_mode
- action
- cleanup confirm
- release confirm
- command preview
- launcher log display/path

Сохрани CLI-only policy:
- только approved entry points;
- no arbitrary shell command.
```

## Проверки

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Gui
```

Ручные проверки GUI:

```text
1. GUI открывается.
2. Можно выбрать retrospective_years.
3. Можно выбрать period_type.
4. Можно выбрать aggregation_mode.
5. Можно выбрать project_root.
6. validate-environment проходит.
7. bad report_date блокируется.
8. release-build блокируется без BUILD_RELEASE_BUNDLE.
9. cleanup-delete-all блокируется без DELETE_OUTPUTS.
10. release-dry-run строит корректную команду.
11. quality-fast строит команду с выбранными параметрами.
12. launcher log создается в outputs/reports/launcher/.
```

## Commit

```powershell
git add tools/windows_launcher/ofz_launcher.ps1 tools/windows_launcher/README.md README.md docs/06_quality/manual_checks_log.md docs/00_project/p2_modernization_progress_report.md
git commit -m "Enhance Windows UI launcher parameters"
git push
```

Если README/manual log не менялись — не добавлять.

---

# P2.6.2 — Word VBA docm assembly and UserForm

## Статус

Новый обязательный промежуточный этап перед P2.7.

## Цель

После `P2.5` есть `.bas` source/spec, но нужен рабочий Word launcher:

```text
Word .docm document
VBA module imported from .bas
UserForm with controls
local/release artifact packaging
```

## Artifact policy

```text
.bas/.frm/.cls source files можно коммитить.
.docm по умолчанию release artifact.
.docm не коммитить в Git без отдельного explicit artifact policy approval.
```

Рекомендуемое место для локальной сборки:

```text
releases/ui_launcher/ofz_launcher_word_<timestamp>.docm
```

`releases/` не коммитить.

## UserForm controls

UserForm name:

```text
frmOfzLauncher
```

Controls:

```text
txtProjectRoot
btnBrowseProjectRoot
btnValidateProject
txtReportDate
cmbRetrospectiveYears
cmbPeriodType
cmbAggregationMode
cmbAction
chkRunSchema
chkRunQualityFast
chkRunQualityFull
chkBuildReleaseBundle
chkOpenOutputs
chkOpenReleases
txtDeleteConfirm
txtReleaseConfirm
txtCommandPreview
txtLogOutput
btnPreviewCommand
btnRun
btnOpenOutputs
btnOpenReleases
btnClose
```

## VBA procedures

`OfzLauncher.bas` должен иметь:

```vb
Sub OFZ_ShowLauncher()
Sub OFZ_RunPipeline()
Sub OFZ_RunSchemaValidation()
Sub OFZ_RunQualityGateFast()
Sub OFZ_RunQualityGateFull()
Sub OFZ_CleanupDryRun()
Sub OFZ_CleanupArchiveAll()
Sub OFZ_CleanupDeleteAll()
Sub OFZ_ReleaseBundleDryRun()
Sub OFZ_ReleaseBundleBuild()
Sub OFZ_OpenOutputsFolder()
Sub OFZ_OpenReleasesFolder()

Function OFZ_ValidateProjectRoot(projectRoot As String) As Boolean
Function OFZ_ValidateReportDate(reportDate As String) As Boolean
Function OFZ_ValidateRetrospectiveYears(value As String) As Boolean
Function OFZ_BuildCommand(...) As String
Function OFZ_RunCommand(commandLine As String, workingDirectory As String) As Long
Function OFZ_LogPath(projectRoot As String) As String
```

## Security

Документация должна указать:

```text
макросы могут быть заблокированы
использовать Trusted Location
не рассылать .docm без контроля
желательно code signing
Word launcher не принимает произвольные команды
Word launcher вызывает только whitelist CLI
DELETE_OUTPUTS required для удаления
BUILD_RELEASE_BUNDLE required для release bundle
```

## Команда для Codex

```text
Выполни P2.6.2 Word VBA docm assembly and UserForm.

Перед началом:
1. Прочитай p2_modernization_progress_report.md.
2. Убедись, что P2.5 completed и P2.6 completed.
3. Убедись, что P2.6.1 completed или явно deferred пользователем.
4. Не переходи к P2.7 до закрытия Word VBA launcher gap.
5. Git/gh команды выполняй outside-sandbox, только точечно.

Задачи:

1. Обновить tools/word_launcher/OfzLauncher.bas:
   - добавить процедуры для всех supported actions;
   - добавить validation functions;
   - добавить command preview/build logic;
   - добавить logging;
   - добавить safe process execution.

2. Создать UserForm source, если возможно:
   - tools/word_launcher/frmOfzLauncher.frm
   - controls по списку выше.

3. Если полноценный .frm/.frx экспорт невозможен автоматически:
   - создать tools/word_launcher/word_docm_build_instructions.md
   - описать создание UserForm вручную в Word VBA editor.

4. Создать локальный .docm artifact, если среда поддерживает Word automation:
   - не коммитить .docm;
   - положить в releases/ui_launcher/;
   - записать путь в progress report.

5. Если Word automation недоступен:
   - не имитировать создание .docm;
   - записать status: docm assembly deferred/manual;
   - source/spec должны быть готовы для ручной сборки.
```

## Проверки

Если Word доступен:

```text
1. Import .bas into Word.
2. Import .frm/.frx or manually create UserForm.
3. Save as .docm under releases/ui_launcher/.
4. Open .docm from Trusted Location.
5. OFZ_ShowLauncher opens UserForm.
6. Validate project root works.
7. bad report_date blocked.
8. release-build blocked without BUILD_RELEASE_BUNDLE.
9. cleanup-delete blocked without DELETE_OUTPUTS.
10. command preview matches approved CLI.
```

Обязательные Git checks:

```text
.docm not staged
releases/ not staged
generated outputs not staged
```

## Commit

```powershell
git add tools/word_launcher/OfzLauncher.bas tools/word_launcher/README.md tools/word_launcher/word_docm_build_instructions.md docs/07_operations/word_vba_launcher_spec.md docs/07_operations/release_checklist.md docs/00_project/artifact_policy.md docs/06_quality/manual_checks_log.md docs/00_project/p2_modernization_progress_report.md
git commit -m "Prepare Word VBA launcher document assembly"
git push
```

Если `.frm` source добавлен и policy разрешает:

```powershell
git add tools/word_launcher/frmOfzLauncher.frm
```

Не добавлять:

```text
*.docm
releases/
outputs/reports/launcher/
```

---

# P2.7 — Screenshot visual regression backend

## Проверочный уровень

```text
Level 3 initially
Level 5 after backend stabilization
```

## Цель

Заменить или дополнить fallback static HTML / Plotly JSON visual regression полноценным screenshot backend.

Fallback оставить как резервный режим.

## Backend candidates

Проанализировать:

```text
Playwright
Kaleido
Selenium/browser-based
Existing Plotly JSON fallback
```

Рекомендуемое решение для HTML/Plotly:

```text
Playwright screenshot backend
```

## Deliverables

```text
scripts/visual_regression.py
docs/06_quality/visual_regression_backend_decision.md
requirements-dev.txt, если нужна новая dev dependency
docs/07_operations/release_checklist.md
README.md
```

## Requirements

`visual_regression.py` должен поддерживать:

```text
--mode fallback
--mode screenshot
--mode auto
```

Auto mode:

```text
1. Пытается screenshot backend.
2. Если backend недоступен, fallback.
3. Ясно пишет visual_regression_mode в report.
```

Screenshot backend должен:

```text
открывать локальные HTML
использовать стабильный viewport
ждать загрузки Plotly
скрывать toolbar/modebar
отключать hover/cursor effects
сохранять screenshots как generated outputs
не коммитить screenshots
создавать diff report
```

## Commands for Codex

```text
Выполни P2.7 Screenshot visual regression backend.

Перед началом:
1. Убедись, что P2.6.1 и P2.6.2 completed/deferred by user decision.
2. Прочитай manual_checks_log: текущий visual regression использует fallback.
3. Git/gh команды выполняй outside-sandbox.
4. Не удаляй fallback mode.

Задачи:
1. Создать backend decision doc.
2. Добавить screenshot backend в visual_regression.py.
3. Сохранить fallback.
4. Добавить режим --mode auto/screenshot/fallback.
5. Добавить отчет с visual_regression_mode.
6. Обновить quality gate, если он вызывает visual_regression.
7. Обновить README/release_checklist.
8. Не коммитить generated screenshots.
```

## Проверки

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\visual_regression.py

.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --mode fallback

.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --mode auto
```

Если screenshot dependencies установлены:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --mode screenshot
```

После стабилизации:

```powershell
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Full gate после стабилизации:

```powershell
.\.venv\Scripts\ofz-quality.exe --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Commit

```powershell
git add scripts/visual_regression.py requirements-dev.txt README.md docs/06_quality docs/07_operations/release_checklist.md docs/00_project/p2_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Add screenshot visual regression backend"
git push
```

---

# P2.8 — CI / GitHub Actions

## Проверочный уровень

```text
Level 2 locally
GitHub-side validation via gh run list/view
```

## Цель

Добавить CI, чтобы production checks запускались в GitHub Actions.

## Deliverables

```text
.github/workflows/quality.yml
docs/07_operations/ci_workflow.md
```

## Workflow requirements

Triggers:

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

Job `quality-fast`:

```text
checkout
setup-python
pip install -r requirements.txt
pip install -r requirements-dev.txt, if needed
pip install -e .
pip check
compileall
ofz-schema
ofz-quality --fast
upload QA reports as workflow artifacts
```

Important:

```text
Do not commit generated outputs.
Do not run fast/full in parallel in same working tree.
Do not cache outputs.
Use pip cache only.
```

Optional manual job:

```text
quality-full via workflow_dispatch only
```

## GitHub CLI

Outside-sandbox only:

```powershell
gh workflow list
gh run list
gh run view <run-id> --log
```

Do not run workflow manually unless user approves:

```powershell
gh workflow run quality.yml
```

## Local checks

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Commit

```powershell
git add .github/workflows/quality.yml docs/07_operations/ci_workflow.md README.md docs/07_operations/release_checklist.md docs/00_project/p2_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Add GitHub Actions quality workflow"
git push
```

---

# P2.9 — Controlled docs archive apply

## Проверочный уровень

```text
Level 0 if docs-only
Level 2 if cleanup_docs.py changes
```

## Цель

Закрыть deferred docs cleanup: снять references, объединить merge candidates, затем выполнить controlled archive.

## Inputs

```text
docs/00_project/docs_inventory_before_cleanup.md
docs/00_project/docs_cleanup_apply_decision.md
scripts/maintenance/cleanup_docs.py
```

## Задачи

```text
1. Проверить archive_candidate и merge_candidate.
2. Проверить references в README/docs/scripts/pyproject.
3. Для merge_candidate перенести полезное в active docs.
4. Для archive_candidate снять активные ссылки.
5. Запустить cleanup_docs.py --dry-run.
6. Если dry-run безопасен, выполнить archive mode.
7. Не выполнять --delete-archived.
8. Создать docs_archive_apply_report.
```

## Commands

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --dry-run
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --archive
```

Если менялся Python:

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\cleanup_docs.py
.\.venv\Scripts\python.exe -m compileall -q scripts
```

## Required docs

```text
docs/00_project/docs_inventory_after_cleanup.md
docs/00_project/docs_archive_apply_report.md
docs/00_project/p2_modernization_progress_report.md
docs/06_quality/manual_checks_log.md
```

## Commit

```powershell
git add docs scripts/maintenance/cleanup_docs.py
git commit -m "Apply controlled documentation archive"
git push
```

---

# P2.10 — Controlled legacy scripts archive apply

## Проверочный уровень

```text
Level 2/3
```

## Цель

Закрыть deferred legacy scripts archive.

## Inputs

```text
docs/00_project/scripts_inventory_before_cleanup.md
docs/00_project/scripts_archive_decision.md
```

Known legacy candidates:

```text
scripts/cleanup_docs.py
scripts/migrate_outputs_structure.py
scripts/reorganize_outputs.py
scripts/maintenance/migrate_legacy_docs_archive.py
scripts/maintenance/reorganize_docs.py
```

## Задачи

```text
1. Проверить references в README/docs/scripts/pyproject.
2. Снять active references.
3. Если безопасно, переместить scripts в scripts/archive/YYYY-MM-DD/.
4. Добавить README.md в archive folder.
5. Не удалять файлы.
6. Если references снять нельзя — обновить deferred decision.
```

## Проверки

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-run.exe --help
.\.venv\Scripts\ofz-quality.exe --help
.\.venv\Scripts\ofz-clean-outputs.exe --help
.\.venv\Scripts\ofz-schema.exe --help
```

Если scripts moved:

```powershell
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Commit

```powershell
git add scripts docs
git commit -m "Apply controlled legacy scripts archive"
git push
```

Если deferred:

```powershell
git add docs/00_project/scripts_archive_decision.md docs/00_project/p2_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Update deferred legacy scripts archive decision"
git push
```

---

# P2.11 — Controlled module decomposition

## Проверочный уровень

```text
Level 3 per small extraction
Level 5 after major decomposition
```

## Цель

Разделить монолиты без изменения behavior.

## Candidates

```text
scripts/06_build_charts.py
scripts/10_build_monthly_charts.py
scripts/html_chart_qa.py
scripts/visual_regression.py
scripts/quality_gate.py
scripts/07_dashboard_exports.py
```

## Rules

```text
1. No output filename changes.
2. No CLI behavior changes.
3. No chart contract changes without QA update.
4. No schema contract changes without schema_validation update.
5. Wrappers stay stable.
6. Extract pure helpers first.
7. One module/family per commit.
```

## Suggested sequence

### P2.11.1 Chart common helpers

Create:

```text
scripts/charts/common.py
scripts/charts/__init__.py
```

Move only pure helpers:

```text
format labels
unit formatting
period labels
color palette access
safe annotation helpers
```

### P2.11.2 Chart family modules

Create:

```text
scripts/charts/structure.py
scripts/charts/scatter.py
scripts/charts/monthly.py
scripts/charts/revenue.py
scripts/charts/boxplot.py
```

Keep:

```text
scripts/06_build_charts.py as wrapper/orchestrator
scripts/10_build_monthly_charts.py as wrapper/orchestrator until later
```

### P2.11.3 QA modules

Create:

```text
scripts/qa/html_chart_contracts.py
scripts/qa/visual_regression_contracts.py
```

## Checks after each extraction

```powershell
.\.venv\Scripts\python.exe -m py_compile <changed files>
.\.venv\Scripts\python.exe -m compileall -q scripts
```

Targeted chart build:

```powershell
.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

QA:

```powershell
.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Full gate after final decomposition:

```powershell
.\.venv\Scripts\ofz-quality.exe --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Commit pattern

```powershell
git add scripts docs/00_project/p2_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Extract chart common helpers"
git push
```

---

# P2.12 — Windows setup / Docker plan

## Проверочный уровень

```text
Level 1/2
```

## Цель

Сделать воспроизводимый setup вне текущей машины.

## Deliverables

```text
tools/setup/setup_windows.ps1
docs/07_operations/windows_setup.md
docs/07_operations/docker_plan.md
```

Optional after decision:

```text
Dockerfile
.dockerignore
```

## setup_windows.ps1 requirements

```text
1. Проверить PowerShell version.
2. Проверить Python version.
3. Создать .venv, если нет.
4. Установить requirements.txt.
5. Установить requirements-dev.txt, если нужен QA.
6. pip install -e .
7. pip check.
8. CLI help checks.
9. compileall.
10. optional smoke ofz-quality --fast only with flag.
11. Не трогать outputs без явного флага.
```

## Docker plan requirements

```text
Windows-first remains primary.
Docker is optional.
Russian fonts/locale requirements.
Browser dependencies for screenshot regression.
Raw data mount strategy.
Generated outputs mount strategy.
Release bundle output path.
```

## Checks

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/setup/setup_windows.ps1 -DryRun
```

If safe:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/setup/setup_windows.ps1
```

## Commit

```powershell
git add tools/setup docs/07_operations README.md docs/00_project/p2_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Add Windows setup workflow"
git push
```

---

# P2.13 — BI-ready release package

## Проверочный уровень

```text
Level 3
```

## Цель

Создать воспроизводимый BI package как external artifact.

## Deliverables

```text
scripts/maintenance/build_bi_package.py
docs/07_operations/bi_release_package.md
docs/02_data_contracts/bi_exports_contract.md
```

## Package location

```text
releases/bi/ofz_analytics_bi_<report_date>_<period_type>_<aggregation_mode>_r<N>_<timestamp>/
```

`releases/` ignored.

## Required BI contents

```text
dashboard exports
semantic model v2
analytical tables CSV
monthly metrics CSV
revenue analytics CSV
chart data CSV
data dictionary
KPI dictionary
period dimension
OFZ type dimension
placement format dimension
README for BI consumer
bi_manifest.json
bi_manifest.md
```

## Commands

Dry-run:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Build:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --include-outputs --confirm BUILD_BI_PACKAGE --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Safety

```text
No generated BI package committed.
No missing required datasets silently replaced with empty files.
Non-zero exit in build mode if required exports missing.
```

## Checks

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\build_bi_package.py
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

If pipeline/export contracts changed:

```powershell
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Commit

```powershell
git add scripts/maintenance/build_bi_package.py docs README.md docs/00_project/p2_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Add BI release package workflow"
git push
```

---

# P2.14 — Archive deletion policy

## Проверочный уровень

```text
Level 0 / docs-only
```

## Цель

Описать, когда archived docs/scripts можно удалять физически.

## Deliverable

```text
docs/00_project/archive_deletion_policy.md
```

## Rules

```text
1. Archived docs/scripts не удалять в production-ready candidate.
2. Удаление разрешено только после stable release.
3. Перед удалением нужен release tag.
4. Перед удалением нужен release bundle.
5. Перед удалением нужен references check.
6. Перед удалением нужен archive manifest.
7. Удаление отдельным commit.
8. Никакого --delete-archived без explicit approval.
```

## Commit

```powershell
git add docs/00_project/archive_deletion_policy.md docs/00_project/p2_modernization_progress_report.md
git commit -m "Document archive deletion policy"
git push
```

---

# P2.15 — P2 completion report

## Проверочный уровень

```text
Level 5 / final close-out
```

## Deliverable

```text
docs/00_project/p2_completion_report.md
```

## Required structure

```text
1. Executive summary.
2. Completed P2 stages.
3. Deferred P2 stages and reasons.
4. Release bundle status.
5. Telemetry status.
6. UI launcher status:
   - PowerShell GUI
   - Word VBA source
   - Word docm artifact
7. Screenshot visual regression status.
8. CI status.
9. Docs/scripts archive status.
10. Module decomposition status.
11. Windows setup / Docker status.
12. BI package status.
13. GitHub CLI / release readiness status.
14. Remaining risks.
15. Recommendation:
    - production-ready candidate remains
    - stable-release-candidate
    - needs-more-hardening
```

## Final checks

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m compileall -q scripts

.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative

.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative

.\.venv\Scripts\ofz-quality.exe --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative

.\.venv\Scripts\ofz-build-release-bundle.exe --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Optional real release bundle:

```powershell
.\.venv\Scripts\ofz-build-release-bundle.exe --include-outputs --confirm BUILD_RELEASE_BUNDLE --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Do not commit bundle.

## Git final check

Outside-sandbox:

```powershell
git status --short --branch
git diff --cached --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|data/processed|logs|releases"
```

## Commit

```powershell
git add docs/00_project/p2_completion_report.md docs/00_project/p2_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Add P2 completion report"
git push
```

---

## 4. Обновленный порядок выполнения после v6

```text
Completed:
P2.0 Starting checkpoint
P2.1 Release bundle automation
P2.2 Pipeline telemetry
P2.3 UI launcher contract
P2.4 PowerShell GUI launcher MVP
P2.5 Word VBA launcher spec and source
P2.6 UI launcher documentation and artifact policy update

New required close-out before P2.7:
P2.6.1 PowerShell GUI launcher hardening close-out
P2.6.2 Word VBA docm assembly and UserForm

Then:
P2.7 Screenshot visual regression backend
P2.8 CI / GitHub Actions
P2.9 Controlled docs archive apply
P2.10 Controlled legacy scripts archive apply
P2.11 Controlled module decomposition
P2.12 Windows setup / Docker plan
P2.13 BI-ready release package
P2.14 Archive deletion policy
P2.15 P2 completion report
```

---

## 5. Финальный отчет Codex после каждого этапа

Codex должен сообщить:

```text
1. Этап.
2. Статус: completed / partial / blocked / deferred / rolled back.
3. Что изменено.
4. Проверочный уровень.
5. Какие проверки выполнены.
6. Какие проверки skipped и почему.
7. Какие проверки упали.
8. Warnings documented.
9. Commits.
10. Push.
11. Git status.
12. Подтверждения:
    - generated outputs not staged;
    - releases not staged;
    - data/raw tracked;
    - CLI entry points still work or not required by level;
    - GitHub CLI auth OK or not used;
    - .docm not committed unless explicitly approved.
13. Следующий рекомендуемый этап.
```
