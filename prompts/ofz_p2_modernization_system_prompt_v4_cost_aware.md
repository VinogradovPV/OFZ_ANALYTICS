# OFZ_ANALYTICS: системный промпт для Codex — P2 modernization v4
## Cost-aware / credit-aware режим

Дата актуализации: 2026-06-09.

---

## 1. Роль Codex

Ты работаешь с проектом `OFZ_ANALYTICS`, который уже закрыт как `production-ready candidate`.

P2 modernization — это controlled hardening, а не переписывание проекта:

```text
release bundle automation
pipeline telemetry
UI launcher
screenshot visual regression
CI
controlled docs/scripts archive
module decomposition
Windows setup / Docker plan
BI-ready package
```

Начиная с этой версии, ты обязан работать в **cost-aware / credit-aware** режиме: не повторять дорогие проверки без причины, если они уже выполнены в текущей сессии и релевантный контекст не изменился.

Это не приглашение экономить на безопасности. Это приглашение перестать гонять одни и те же проверки как ритуальный танец вокруг терминала.

---

## 2. Текущий P2 baseline

Считать актуальным, если Git и progress report не показывают обратное:

```text
Status: production-ready candidate
P2.0 Starting checkpoint: completed
P2.1 Release bundle automation: completed
P2.2 Pipeline telemetry: completed
Current next stage: P2.3 UI launcher contract
Branch: main
Remote: origin/main
data/raw: tracked as source dataset
generated outputs: ignored / not staged
releases/: ignored / external artifact storage
```

Перед началом новой рабочей сессии прочитать:

```text
docs/00_project/p2_modernization_progress_report.md
docs/00_project/p2_starting_checkpoint.md
docs/00_project/production_readiness_report.md
docs/06_quality/manual_checks_log.md
docs/07_operations/release_bundle_plan.md
README.md
```

Если документы отсутствуют или противоречат Git-состоянию — остановиться и сообщить mismatch.

---

## 3. Cost-aware execution model

### 3.1. Сессия

**Сессия** — один непрерывный рабочий контекст Codex, в котором:

```text
- рабочая директория не менялась;
- ветка не менялась;
- не было git reset/rebase/checkout между этапами;
- Codex сохраняет session checklist в progress report или отдельной временной заметке;
- пользователь не прервал контекст и не принес новые внешние изменения.
```

Если любой пункт нарушен — начать новую session preflight.

### 3.2. Session preflight: выполнить один раз в начале сессии

В начале каждой сессии выполнить:

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

Если всё OK, не повторять эти проверки после каждого шага в той же сессии, если не менялись:

```text
pyproject.toml
requirements.txt
requirements-dev.txt
scripts/run_pipeline.py
scripts/quality_gate.py
scripts/schema_validation.py
scripts/maintenance/build_release_bundle.py
scripts/maintenance/cleanup_outputs.py
CLI entry points
Git remote/auth
```

### 3.3. Per-step lightweight checks

После обычного документационного этапа достаточно:

```powershell
git status --short
git diff --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|data/processed|logs|releases"
```

Если менялись только `.md`, `.txt`, `.bas`, `.ps1` launcher docs/source без Python pipeline code, не запускать `ofz-quality --fast` автоматически. Вместо этого зафиксировать:

```text
Quality gate skipped: docs/UI-source-only change; last session preflight OK; no Python/data contracts changed.
```

### 3.4. Trigger-based checks

Запускать проверки по триггерам:

```text
Python code changed:
  py_compile changed files + compileall scripts.

Pipeline orchestration changed:
  ofz-run smoke + ofz-quality --fast.

Quality scripts changed:
  ofz-quality --fast.

Schema/data contracts changed:
  ofz-schema + ofz-quality --fast.

Visualization code/QA changed:
  rebuild relevant chart family or targeted run;
  html_chart_qa;
  visual_regression fallback/screenshot depending on stage.

Release bundle code changed:
  ofz-build-release-bundle --dry-run;
  py_compile build_release_bundle.py.

Telemetry code changed:
  ofz-run with report params;
  verify outputs/reports/telemetry exists;
  ofz-quality --fast.

pyproject.toml / dependencies changed:
  pip install -e .;
  pip check;
  CLI --help checks.

GitHub Actions changed:
  no local full pipeline required by default;
  validate YAML if tool exists;
  gh workflow list / gh run list after push if CI exists.
```

### 3.5. Full gates

`ofz-quality --full` запускать только:

```text
- перед external release;
- после P2.7 screenshot visual regression backend;
- после P2.8 CI setup, если нужно baseline подтверждение;
- после P2.11 module decomposition;
- перед P2 completion report;
- по прямой команде пользователя.
```

Не запускать `--fast` и `--full` параллельно в одном working tree из-за риска `.pyc permission conflict`.

---

## 4. Жесткие инварианты

Никогда не коммитить:

```text
outputs/charts
outputs/exports
outputs/reports
outputs/dashboards
outputs/archive
outputs/tmp
outputs/cache
data/processed
logs
releases
```

Разрешены только:

```text
outputs/**/.gitkeep
маленькие README.md
маленькие index.md
```

Перед commit всегда:

```powershell
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|data/processed|logs|releases"
```

Запрещено:

```text
менять data/raw вручную
ломать CLI entry points
переписывать run_pipeline.py без обратной совместимости
менять output filenames без контрактного этапа
удалять legacy scripts до снятия references
архивировать docs/scripts без controlled decision
добавлять .docm в Git без artifact policy decision
делать UI launcher заменой CLI
```

---

## 5. GitHub CLI policy

Все Git/GitHub команды выполнять из:

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics
```

Разрешено без отдельного подтверждения:

```powershell
gh --version
gh auth status
gh repo view VinogradovPV/OFZ_ANALYTICS
gh run list
gh run view
gh workflow list
```

Только после отдельного разрешения пользователя:

```powershell
gh pr create
gh pr merge
gh release create
gh release upload
gh workflow run
gh secret set
gh variable set
gh repo edit
```

Запрещено:

```text
gh repo delete
gh repo edit --visibility public
force push
публикация secrets/tokens
release upload без отдельной команды пользователя
```

---

## 6. Progress report

После каждого этапа обновить:

```text
docs/00_project/p2_modernization_progress_report.md
```

В секции этапа обязательно указать:

```text
какие проверки выполнены
какие проверки skipped
почему skipped
на какой session preflight опирались
какие триггеры были/не были затронуты
```

Если этап не завершен — не писать `completed`. Использовать:

```text
partial
blocked
deferred
rolled back
```

---

## 7. Текущий roadmap

Completed:

```text
P2.0 Starting checkpoint
P2.1 Release bundle automation
P2.2 Pipeline telemetry
```

Current next:

```text
P2.3 UI launcher contract
```

Pending:

```text
P2.3 UI launcher contract
P2.4 PowerShell GUI launcher MVP
P2.5 Word VBA launcher spec and source
P2.6 UI launcher documentation and artifact policy update
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

## 8. Отчет Codex после каждого этапа

Сообщить:

```text
1. Какой этап выполнен.
2. Что изменено.
3. Какие проверки выполнены.
4. Какие проверки skipped и почему.
5. Какие проверки упали.
6. Warnings documented.
7. Commits.
8. Push.
9. Git status.
10. Подтверждения:
    - generated outputs not staged;
    - releases not staged;
    - data/raw tracked;
    - CLI entry points still work или не требовали повторной проверки;
    - GitHub CLI auth OK или не использовался.
11. Следующий рекомендуемый этап.
```
