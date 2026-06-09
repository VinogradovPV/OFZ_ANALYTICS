# OFZ_ANALYTICS: системный промпт для Codex — P2 modernization v3

Дата актуализации: 2026-06-09.

## 1. Роль

Ты работаешь с проектом `OFZ_ANALYTICS`, который закрыт как `production-ready candidate`. P2 — это не переписывание проекта, а controlled hardening: release bundle, telemetry, UI launcher, screenshot visual regression, CI, controlled archive, module decomposition, Windows setup, BI package.

Работай маленькими этапами: один этап — проверки — commit — push — отчет. Не устраивай “давайте заодно перепишем половину проекта”, человечество и так настрадалось.

## 2. Текущий P2 baseline

Считать актуальным, если Git не показывает обратное:

```text
Status: production-ready candidate
Branch: main
Remote: origin/main
data/raw: tracked as source dataset
generated outputs: not tracked / not staged
outputs: tracked only as skeleton/index
quality_gate --fast: OK
quality_gate --full: OK
```

P2 уже стартовал:

```text
P2.0 Starting checkpoint выполнен.
Создан docs/00_project/p2_starting_checkpoint.md.
Создан docs/00_project/p2_modernization_progress_report.md.
Следующий рекомендуемый этап: P2.1 Release bundle automation.
```

Перед каждым этапом читать:

```text
docs/00_project/p2_modernization_progress_report.md
docs/00_project/p2_starting_checkpoint.md
docs/00_project/production_readiness_report.md
docs/06_quality/manual_checks_log.md
```

Если документы отсутствуют или противоречат Git-состоянию — остановиться и сообщить расхождение.

## 3. CLI entry points

Основные CLI:

```toml
[project.scripts]
ofz-run = "scripts.run_pipeline:main"
ofz-interactive = "scripts.interactive_pipeline:main"
ofz-quality = "scripts.quality_gate:main"
ofz-clean-outputs = "scripts.maintenance.cleanup_outputs:main"
ofz-schema = "scripts.schema_validation:main"
```

Проверка через `.venv`:

```powershell
.\.venv\Scripts\ofz-run.exe --help
.\.venv\Scripts\ofz-interactive.exe --help
.\.venv\Scripts\ofz-quality.exe --help
.\.venv\Scripts\ofz-clean-outputs.exe --help
.\.venv\Scripts\ofz-schema.exe --help
```

Fallback через Python-файлы сохранять в docs.

## 4. Обязательный progress-report контур

После каждого P2-этапа обновлять:

```text
docs/00_project/p2_modernization_progress_report.md
```

Формат секции:

```markdown
## P2.X - <Название этапа>

Дата: YYYY-MM-DD.

### 1. Какой P2-этап выполнен
### 2. Что изменено
### 3. Какие проверки прошли
### 4. Какие проверки упали
### 5. Какие warnings documented
### 6. Какие commits созданы
### 7. Был ли push
### 8. Текущий git status
### 9. Подтверждения
- generated outputs not staged:
- data/raw tracked:
- CLI entry points still work:
### 10. Следующий рекомендуемый P2-этап
```

Если этап не завершен, не писать completed. Использовать `blocked`, `partial`, `deferred` или `rolled back`.

## 5. Жесткие инварианты

Нельзя коммитить:

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

Разрешены только skeleton/index/readme исключения.

Перед commit:

```powershell
git status --short
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|data/processed|logs|releases"
```

Если generated outputs staged:

```powershell
git reset HEAD outputs/charts outputs/exports outputs/reports outputs/dashboards outputs/archive outputs/tmp outputs/cache data/processed logs releases
git add outputs/**/.gitkeep
git add outputs/charts/index.md
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

## 6. Проверки после каждого этапа

Минимум:

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Для package/CLI этапов:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\ofz-run.exe --help
.\.venv\Scripts\ofz-interactive.exe --help
.\.venv\Scripts\ofz-quality.exe --help
.\.venv\Scripts\ofz-clean-outputs.exe --help
.\.venv\Scripts\ofz-schema.exe --help
```

Не запускать fast/full quality gate параллельно в одном working tree из-за возможного `.pyc` permission conflict.

## 7. Текущий порядок P2

После выполненного P2.0:

```text
P2.1 Release bundle automation
P2.2 Pipeline telemetry
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

## 8. UI launcher rules

UI launcher — только оболочка над CLI.

Word/VBA:

```text
.bas/.frm source в Git
.docm как release artifact, не source
макросы: Trusted Location / signing / macro policy
только whitelist CLI
DELETE_OUTPUTS required для delete cleanup
лог в outputs/reports/launcher/
```

PowerShell GUI:

```text
текстовый source artifact
валидирует параметры
не принимает arbitrary commands
запускает процессы безопасно, без string-concat shell execution
```

## 9. Отчет после каждого этапа

В ответе Codex должен указать:

```text
этап, изменения, проверки, failures, warnings, commits, push, git status,
generated outputs not staged, data/raw tracked, CLI still works,
следующий рекомендуемый этап.
```
