# OFZ_ANALYTICS: P2 modernization step-by-step v5
## Cost-aware инструкция с сокращением повторяющихся проверок

Дата актуализации: 2026-06-09.

---

## 0. Назначение v5

Эта версия уточняет P2-инструкцию v4 и вводит **cost-aware / credit-aware режим**.

Идея простая: если в рамках одной рабочей сессии уже проверены Git, GitHub CLI, CLI entry points и базовое состояние проекта, то не нужно повторять весь набор проверок после каждого маленького документационного шага. Машины любят повторение, кредиты — нет. Странно, что человечеству понадобилась отдельная инструкция, но вот она.

---

## 1. Текущий статус

Считать актуальным, если `p2_modernization_progress_report.md` и Git не показывают обратное:

```text
P2.0 Starting checkpoint: completed
P2.1 Release bundle automation: completed
P2.2 Pipeline telemetry: completed
Current next stage: P2.3 UI launcher contract
```

Уже реализовано:

```text
ofz-build-release-bundle
release_bundle_plan.md
releases/ ignored
telemetry JSON/MD
run manifest telemetry links
release bundle picks telemetry summary when present
```

Следующий этап:

```text
P2.3 UI launcher contract
```

---

## 2. Что читать в начале сессии

В начале новой рабочей сессии Codex читает:

```text
docs/00_project/p2_modernization_progress_report.md
docs/00_project/p2_starting_checkpoint.md
docs/00_project/production_readiness_report.md
docs/06_quality/manual_checks_log.md
docs/07_operations/release_bundle_plan.md
README.md
```

Если документы отсутствуют или противоречат Git-состоянию — остановиться.

---

## 3. Session preflight: выполнить один раз

В начале сессии:

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics

git status --short --branch
git branch --show-current
git remote -v
git log --oneline -5

gh --version
gh auth status
gh repo view VinogradovPV/OFZ_ANALYTICS

.\.venv\Scripts\ofz-run.exe --help
.\.venv\Scripts\ofz-interactive.exe --help
.\.venv\Scripts\ofz-quality.exe --help
.\.venv\Scripts\ofz-clean-outputs.exe --help
.\.venv\Scripts\ofz-schema.exe --help
.\.venv\Scripts\ofz-build-release-bundle.exe --help
```

Если preflight OK, записать в progress report:

```text
Session preflight: OK
Дата/время:
Проверены:
- Git branch/remote/status
- GitHub CLI auth/repo access
- CLI entry points
```

В этой же сессии не повторять preflight, если не менялись:

```text
pyproject.toml
requirements*.txt
CLI entry points
Git remote/auth
run_pipeline.py
quality_gate.py
schema_validation.py
cleanup_outputs.py
build_release_bundle.py
```

---

## 4. Когда session preflight нужно повторить

Повторить preflight, если:

```text
- Codex перешел в новую сессию;
- пользователь сообщил, что были внешние изменения;
- был git checkout / reset / rebase / pull с изменениями;
- изменился pyproject.toml;
- изменились requirements.txt или requirements-dev.txt;
- изменились CLI entry points;
- изменился Git remote;
- gh auth status начал падать;
- working tree стал dirty не из-за текущего этапа.
```

---

## 5. Проверки по уровням

### 5.1. Level 0 — docs-only / prompt-only / policy-only

Применять, если менялись только:

```text
.md
.txt
prompt files
policy docs
README sections
manual_checks_log.md
p2 progress report
```

Проверки:

```powershell
git status --short
git diff --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|data/processed|logs|releases"
```

Не запускать:

```text
compileall
ofz-quality --fast
ofz-quality --full
ofz-run
pip install -e
```

В progress report написать:

```text
Skipped compileall/quality gate: docs-only change; session preflight OK; no Python/data/CLI contracts changed.
```

### 5.2. Level 1 — UI source only

Применять, если менялись:

```text
tools/windows_launcher/*.ps1
tools/word_launcher/*.bas
tools/word_launcher/*.frm
docs for UI launcher
```

Проверки:

```powershell
git status --short
git diff --name-only
```

Для PowerShell launcher:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1
```

Для VBA:

```text
ручная проверка импорта .bas/.frm в Word, если Word доступен;
иначе syntax/source review и documented limitation.
```

Не запускать `ofz-quality --fast`, если Python pipeline не менялся.

### 5.3. Level 2 — Python utility changed, no pipeline behavior

Применять, если менялся отдельный Python utility без влияния на pipeline outputs.

Проверки:

```powershell
.\.venv\Scripts\python.exe -m py_compile <changed_python_files>
.\.venv\Scripts\python.exe -m compileall -q scripts
```

`ofz-quality --fast` можно пропустить, если utility не участвует в pipeline/QA/CLI.

### 5.4. Level 3 — pipeline / QA / schema / release / telemetry changed

Запускать targeted checks:

Release bundle:

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\build_release_bundle.py
.\.venv\Scripts\ofz-build-release-bundle.exe --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Telemetry:

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\pipeline\telemetry.py scripts\run_pipeline.py scripts\run_manifest.py
.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
Get-ChildItem outputs/reports/telemetry -Recurse -File
```

Quality gate code:

```powershell
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Schema/data contracts:

```powershell
.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

### 5.5. Level 4 — package/dependencies/CLI changed

Проверки:

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

### 5.6. Level 5 — full gate

Запускать только:

```text
- перед external release;
- перед GitHub Release;
- после P2.7 screenshot visual regression backend;
- после P2.11 module decomposition;
- перед P2.15 completion report;
- по прямой команде пользователя.
```

Команда:

```powershell
.\.venv\Scripts\ofz-quality.exe --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

---

## 6. GitHub CLI cost-aware policy

Не повторять `gh auth status` и `gh repo view` после каждого шага, если session preflight OK и не было Git/GitHub изменений.

Для docs-only/UI-only этапов достаточно:

```powershell
git status --short --branch
```

Использовать `gh` только при необходимости:

```text
CI inspection
GitHub release planning
remote access troubleshooting
pull/push validation
```

Не использовать `gh` ради галочки. Галочки хороши в чеклистах, не в расходе кредитов.

---

## 7. Generated artifacts policy

Перед каждым commit всегда проверять staged files:

```powershell
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|data/processed|logs|releases"
```

Это не пропускать даже в cost-aware режиме. Дешево, быстро, спасает от больших глупостей.

Если generated artifacts staged:

```powershell
git reset HEAD outputs/charts outputs/exports outputs/reports outputs/dashboards outputs/archive outputs/tmp outputs/cache data/processed logs releases
git add outputs/**/.gitkeep
git add outputs/charts/index.md
```

---

# P2.3. UI launcher contract — cost-aware версия

## Цель

Создать только контракт UI launcher.

## Проверочный уровень

```text
Level 0 / docs-only
```

Если меняется только `docs/07_operations/ui_launcher_contract.md`, progress report и manual log, то:

```text
compileall не нужен;
ofz-quality --fast не нужен;
gh auth повторять не нужно, если session preflight OK.
```

## Команда для Codex

```text
Выполни P2.3 UI launcher contract в cost-aware режиме.

Перед началом:
1. Если это новая сессия — выполнить session preflight.
2. Если session preflight уже выполнен и зафиксирован в progress report, не повторять gh/CLI help проверки.
3. Прочитать docs/00_project/p2_modernization_progress_report.md.
4. Подтвердить, что P2.2 completed.
5. Подтвердить, что следующий этап — P2.3.

Создать:
docs/07_operations/ui_launcher_contract.md

Документ должен зафиксировать:

1. UI launcher вызывает только CLI, не внутренние Python функции.

2. Supported CLI:
   - ofz-run;
   - ofz-interactive;
   - ofz-quality;
   - ofz-clean-outputs;
   - ofz-schema;
   - ofz-build-release-bundle.

3. UI launcher поддерживает параметры:
   - project_root;
   - report_date;
   - retrospective_years;
   - period_type;
   - aggregation_mode;
   - cleanup_mode;
   - run_schema_validation;
   - run_quality_gate_fast;
   - run_quality_gate_full, optional/manual;
   - build_release_bundle;
   - open_outputs_folder;
   - open_release_bundle_folder.

4. UI launcher валидирует:
   - project_root exists;
   - git status works;
   - pyproject.toml exists;
   - .venv exists;
   - data/raw exists;
   - report_date format YYYY-MM-DD;
   - report_date is first day of month;
   - retrospective_years integer 1..10;
   - period_type in month/quarter/year;
   - aggregation_mode in cumulative/point;
   - cleanup_mode whitelist.

5. Cleanup modes:
   - keep;
   - dry-run;
   - archive-all;
   - delete-all-with-archive;
   - delete-all-without-archive only if explicitly supported by cleanup_outputs.py.

6. Delete cleanup requires:
   DELETE_OUTPUTS

7. Release bundle creation requires:
   --include-outputs --confirm BUILD_RELEASE_BUNDLE

8. UI launcher пишет log:
   outputs/reports/launcher/launcher_run_<timestamp>.log

9. UI launcher показывает:
   - command preview;
   - working directory;
   - stdout/stderr;
   - exit code;
   - path to run manifest;
   - path to telemetry summary;
   - path to release bundle, if created.

10. UI launcher не должен:
   - менять data/raw;
   - принимать arbitrary shell command;
   - коммитить outputs;
   - создавать GitHub release без отдельной команды;
   - запускать fast и full quality gate параллельно.

11. UI launcher использует release_bundle_plan.md как контракт для bundle behavior.

12. Word VBA launcher:
   - .bas/.frm source можно коммитить;
   - .docm является release artifact, не source artifact;
   - macro security documented.

13. PowerShell GUI launcher:
   - recommended first UI implementation;
   - text source tracked in Git;
   - process arguments passed safely, not through unsafe shell string concatenation.

Обновить:
- docs/00_project/p2_modernization_progress_report.md;
- docs/06_quality/manual_checks_log.md, если были ручные проверки.

Не создавать PowerShell GUI.
Не создавать Word VBA.
P2.3 — только contract.

Проверки:
- git status --short;
- git diff --name-only;
- staged generated artifacts check;
- Select-String по ui_launcher_contract.md на ключевые токены.

Не запускать compileall/ofz-quality, если Python code не менялся.
```

## Проверка документа

```powershell
Select-String -Path docs\07_operations\ui_launcher_contract.md -Pattern "ofz-build-release-bundle|BUILD_RELEASE_BUNDLE|DELETE_OUTPUTS|release_bundle_plan|telemetry|docm|PowerShell"
```

## Commit

```powershell
git add docs/07_operations/ui_launcher_contract.md docs/00_project/p2_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Document UI launcher contract"
git push
```

Если `manual_checks_log.md` не менялся — не добавлять.

---

# P2.4. PowerShell GUI launcher MVP — cost-aware версия

## Проверочный уровень

```text
Level 1 / UI source only
```

Если меняется только `.ps1`, README и docs:

```text
ofz-quality --fast не нужен;
compileall не нужен;
нужен запуск/ручной smoke самого launcher.
```

## Команда для Codex

```text
Выполни P2.4 PowerShell GUI launcher MVP в cost-aware режиме.

Перед началом:
1. Убедись по progress report, что P2.3 completed.
2. Если session preflight уже OK, не повторяй gh/CLI help.
3. Git status должен быть clean или содержать только ожидаемые изменения текущего этапа.

Создать:
tools/windows_launcher/ofz_launcher.ps1
tools/windows_launcher/README.md

Launcher должен:
- вызывать только CLI;
- валидировать параметры;
- показывать stdout/stderr;
- сохранять logs;
- блокировать bad date;
- блокировать delete без DELETE_OUTPUTS;
- блокировать bundle creation без BUILD_RELEASE_BUNDLE;
- не выполнять arbitrary command input;
- не создавать GitHub release.
```

## Проверки

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1
```

Ручная проверка:

```text
Validate environment OK.
Bad date blocked.
Dry-run cleanup does not delete.
Quality gate fast starts only when user selects it.
Release bundle dry-run starts.
Release bundle creation blocked without BUILD_RELEASE_BUNDLE.
Delete mode blocked without DELETE_OUTPUTS.
Launcher log created.
```

## Commit

```powershell
git add tools/windows_launcher README.md docs/00_project/p2_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Add Windows UI launcher MVP"
git push
```

---

# P2.5. Word VBA launcher spec and source — cost-aware версия

## Проверочный уровень

```text
Level 1 / UI source only
```

Если меняются только `.bas`, `.frm`, README и docs:

```text
ofz-quality --fast не нужен;
compileall не нужен;
нужна ручная проверка импорта VBA, если Word доступен.
```

## Команда для Codex

```text
Выполни P2.5 Word VBA launcher spec and source в cost-aware режиме.

Создать:
docs/07_operations/word_vba_launcher_spec.md
tools/word_launcher/README.md
tools/word_launcher/OfzLauncher.bas

Если нужен UserForm:
tools/word_launcher/OfzLauncherForm.frm

Правила:
- .bas/.frm source можно коммитить;
- .docm считать release artifact;
- .docm не коммитить без отдельного artifact policy decision;
- VBA запускает только whitelist CLI;
- delete cleanup требует DELETE_OUTPUTS;
- release bundle creation требует BUILD_RELEASE_BUNDLE;
- macro security documented.
```

## Commit

```powershell
git add docs/07_operations/word_vba_launcher_spec.md tools/word_launcher README.md docs/00_project/p2_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Add Word VBA launcher specification"
git push
```

---

# P2.6. UI launcher documentation and artifact policy update

## Проверочный уровень

```text
Level 0 / docs-only
```

## Команда для Codex

```text
Выполни P2.6 UI launcher documentation and artifact policy update.

Обновить:
- README.md;
- docs/07_operations/production_runbook.md;
- docs/07_operations/release_checklist.md;
- docs/00_project/artifact_policy.md;
- docs/00_project/p2_modernization_progress_report.md.

Зафиксировать:
1. CLI остается главным supported interface.
2. PowerShell GUI launcher — recommended Windows UI MVP.
3. Word VBA launcher — optional launcher.
4. .ps1/.bas/.frm are source artifacts.
5. .docm is release artifact unless explicitly approved.
6. Launcher logs are generated outputs.
7. Release bundle remains external artifact.
8. UI launcher не заменяет quality gate.

Проверки:
- docs diff;
- staged generated artifacts check;
- no compileall / no quality gate unless Python changed.
```

## Commit

```powershell
git add README.md docs
git commit -m "Document UI launcher usage and artifact policy"
git push
```

---

# P2.7-P2.15: проверочные уровни

```text
P2.7 Screenshot visual regression backend:
  Level 3/5 depending on backend.
  Required: targeted visual_regression + quality fast.
  Full gate after backend stabilizes.

P2.8 CI / GitHub Actions:
  Level 0/2 locally.
  Validate YAML if possible.
  After push use gh run list/view if workflow runs.

P2.9 Controlled docs archive apply:
  Level 0 until archive script changes.
  If cleanup_docs.py changes: Level 2.
  If physical archive: references check mandatory.

P2.10 Controlled legacy scripts archive apply:
  Level 2/3.
  compileall mandatory.
  quality fast recommended after moving scripts.

P2.11 Controlled module decomposition:
  Level 3/5.
  compileall + targeted tests + quality fast mandatory.
  full gate after major decomposition.

P2.12 Windows setup / Docker plan:
  Level 1/2.
  setup script smoke required.

P2.13 BI-ready release package:
  Level 3.
  dry-run build_bi_package mandatory.
  quality fast if pipeline/export contracts changed.

P2.14 Archive deletion policy:
  Level 0 docs-only.

P2.15 P2 completion report:
  Level 5 full gate before final report.
```

---

## 8. Отчет Codex после каждого этапа

После каждого этапа Codex должен сообщить:

```text
1. Этап.
2. Что изменено.
3. Проверочный уровень.
4. Какие проверки выполнены.
5. Какие проверки skipped и почему.
6. Какие проверки упали.
7. Warnings documented.
8. Commits.
9. Push.
10. Git status.
11. Подтверждения:
    - generated outputs not staged;
    - releases not staged;
    - data/raw tracked;
    - CLI entry points still work или не требовали повторной проверки;
    - GitHub CLI auth OK или не использовался.
12. Следующий рекомендуемый этап.
```
