# Production runbook

Дата актуализации: 2026-06-08.

Этот runbook описывает безопасный production workflow для OFZ_ANALYTICS после стабилизации Git, artifact policy, cleanup-команды и интерактивного launcher.

## Предварительные условия

- Работать из корня проекта.
- Все Python-команды запускать через локальное окружение:

```powershell
.\.venv\Scripts\python.exe
```

- `data/raw/` является source dataset проекта и не изменяется cleanup-командами.
- Generated outputs не коммитятся в Git.
- Перед production-запуском проверить состояние репозитория:

```powershell
git status --short --branch
git log --oneline --decorate -5
```

## Проверка окружения

После изменения зависимостей или Python-окружения выполнить:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m compileall -q scripts
```

Поддерживаемый диапазон Python указан в `pyproject.toml`. Текущий локальный baseline проверен на Python 3.14.5; при запуске на другой версии из поддерживаемого диапазона сначала выполнить fast quality gate.

## Безопасная очистка outputs

Cleanup выполняется только через `scripts/maintenance/cleanup_outputs.py`. Скрипт работает только внутри `outputs/`, сохраняет `outputs/archive/`, пишет cleanup manifest и пересоздает skeleton с `.gitkeep`.

Dry-run без удаления:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --dry-run
```

Архивировать текущие working outputs:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all
```

Удалить working outputs только после явного подтверждения:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --delete-all --confirm DELETE_OUTPUTS
```

Архивировать и удалить одним контролируемым запуском:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all --delete-all --confirm DELETE_OUTPUTS
```

Гарантии cleanup:

- пути вне `outputs/` не затрагиваются;
- `outputs/archive/` сохраняется при удалении working outputs;
- manifest создается до удаления;
- skeleton outputs пересоздается после удаления;
- `.gitkeep` восстанавливаются;
- cleanup reports и manifests в `outputs/` являются generated artifacts и не коммитятся.

## Интерактивный cleanup pre-flight

Интерактивный launcher запускается так:

```powershell
.\.venv\Scripts\python.exe scripts\interactive_pipeline.py
```

Перед стартом выбранной pipeline-команды launcher проверяет, есть ли generated files в `outputs/`. Если working outputs присутствуют, показывается меню:

1. Оставить outputs как есть.
2. Показать dry-run очистки.
3. Архивировать outputs и очистить.
4. Очистить outputs без архива.
5. Отменить запуск.

Действие по умолчанию: оставить outputs как есть.

Launcher не удаляет файлы напрямую. Он делегирует cleanup скрипту `scripts/maintenance/cleanup_outputs.py`.

Вариант 3 выполняет:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all --delete-all --confirm DELETE_OUTPUTS
```

Вариант 4 требует ввести `DELETE_OUTPUTS_NO_ARCHIVE` в интерактивном launcher, после чего launcher вызывает подтвержденное удаление через cleanup-скрипт. Если cleanup завершается с ошибкой, pipeline не запускается.

Для полного интерактивного запуска cleanup status, mode и return code фиксируются в run manifest.

## Production regeneration

Полный pipeline:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Fast quality gate после production-запуска:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

При необходимости отдельно проверить schema validation:

```powershell
.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Run manifest

После полного `--all` pipeline формирует run manifest. Manifest фиксирует:

- параметры запуска;
- periods;
- sha256 ключевых scripts;
- sha256 raw files;
- outputs summary;
- key chart outputs;
- check statuses;
- cleanup pre-flight status, если запуск шел через interactive launcher.

Latest manifest может пересоздаваться. Релизные manifests должны сохраняться как audit artifacts или входить в release bundle.

## Git safety

Перед commit:

```powershell
git status --short
git diff --cached --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|data/processed|logs"
```

В обычный commit должны попадать только:

- source code;
- config;
- docs;
- scripts;
- data contracts;
- prompts;
- `data/raw`;
- skeleton files outputs (`.gitkeep`, допустимые `README.md` / `index.md`).

Generated outputs должны храниться как release bundle, external artifact или local archive, но не как обычная Git-история.

## Ограничения

- `data/raw/` не очищается и не модифицируется maintenance-командами.
- Полная очистка outputs удаляет generated artifacts, кроме сохраненного archive. Запускать ее следует только после dry-run и проверки archive policy.
- Если production run нужен для аудита, перед очисткой outputs нужно создать archive/release bundle.
- На Python 3.11-3.13 metadata допускает запуск, но локальный production baseline пока подтвержден на Python 3.14.5; перед использованием результатов обязателен quality gate.
