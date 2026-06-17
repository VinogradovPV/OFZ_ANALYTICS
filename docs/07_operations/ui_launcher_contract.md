# Контракт UI launcher

Дата создания: 2026-06-11.

## Назначение

UI launcher - это пользовательская оболочка над существующими CLI entry points проекта OFZ_ANALYTICS. Он не заменяет pipeline, не импортирует внутренние Python-функции и не реализует собственную бизнес-логику расчетов.

Основное правило: UI вызывает только поддержанные CLI-команды с валидированными аргументами.

## Поддерживаемый CLI

UI launcher может вызывать только эти команды:

- `ofz-run`;
- `ofz-interactive`;
- `ofz-quality`;
- `ofz-clean-outputs`;
- `ofz-schema`;
- `ofz-build-release-bundle`.

Fallback через `.venv\Scripts\*.exe` допустим, если `.venv` не активирована, но набор команд остается тем же.

## Поддерживаемые параметры

UI launcher поддерживает только явные параметры:

- `project_root`;
- `report_date`;
- `retrospective_years`;
- `period_type`;
- `aggregation_mode`;
- `cleanup_mode`;
- `run_schema_validation`;
- `run_quality_gate_fast`;
- `run_quality_gate_full`, optional/manual;
- `build_release_bundle`;
- `open_outputs_folder`;
- `open_release_bundle_folder`.

Произвольная строка shell-команды не является допустимым параметром.

## Правила валидации

Перед запуском CLI UI launcher обязан проверить:

- `project_root` exists;
- `git status` works from `project_root`;
- `pyproject.toml` exists;
- `.venv` exists;
- `data/raw` exists;
- `report_date` format is `YYYY-MM-DD`;
- `report_date` is first day of month;
- `retrospective_years` is integer `1..10`;
- `period_type` in `month`, `quarter`, `year`;
- `aggregation_mode` in `cumulative`, `point`;
- `cleanup_mode` is in the cleanup whitelist.

Если валидация не проходит, UI launcher не должен запускать pipeline.

## Режимы cleanup

Разрешенные `cleanup_mode` значения:

- `keep`;
- `dry-run`;
- `archive-all`;
- `delete-all-with-archive`;
- `delete-all-without-archive` only if explicitly supported by `cleanup_outputs.py`.

Удаление outputs требует явного подтверждения:

```text
DELETE_OUTPUTS
```

UI launcher не удаляет файлы напрямую. Он вызывает `ofz-clean-outputs` или fallback-скрипт `scripts/maintenance/cleanup_outputs.py`.

## Release bundle behavior

UI launcher использует `docs/07_operations/release_bundle_plan.md` как контракт поведения release bundle.

Создание release bundle с копированием generated outputs требует:

```text
--include-outputs --confirm BUILD_RELEASE_BUNDLE
```

Без этого UI launcher может запускать только dry-run release bundle.

## Логирование

Каждый запуск UI launcher пишет log:

```text
outputs/reports/launcher/launcher_run_<timestamp>.log
```

Log является generated artifact и не коммитится.

Минимальный состав log:

- timestamp;
- selected parameters;
- command preview;
- working directory;
- stdout;
- stderr;
- exit code;
- path to run manifest, if created;
- path to telemetry summary, if created;
- path to release bundle, if created.

## Требования к UI-отображению

UI launcher должен показывать пользователю:

- command preview;
- working directory;
- stdout/stderr;
- exit code;
- path to run manifest;
- path to telemetry summary;
- path to release bundle, if created.

## Запрещенное поведение

UI launcher не должен:

- менять `data/raw`;
- принимать arbitrary shell command;
- коммитить `outputs`;
- создавать GitHub release без отдельной команды пользователя;
- запускать `ofz-quality --fast` и `ofz-quality --full` параллельно;
- выполнять `git push`, `gh release create`, `gh release upload` или публикацию артефактов без отдельного явного этапа.

## Политика Word VBA launcher

Для будущего Word VBA launcher:

- `.bas` / `.frm` source можно коммитить как source artifacts;
- `.docm` является release artifact, не source artifact;
- `.docm` не коммитится без отдельного artifact policy decision;
- macro security должна быть документирована;
- VBA launcher также вызывает только whitelist CLI.

## Политика PowerShell GUI launcher

PowerShell GUI launcher является recommended first UI implementation для Windows.

Правила:

- text source tracked in Git;
- UI вызывает только supported CLI;
- process arguments passed safely;
- unsafe shell string concatenation запрещена;
- delete cleanup blocked without `DELETE_OUTPUTS`;
- release bundle creation blocked without `BUILD_RELEASE_BUNDLE`;
- launcher logs пишутся в `outputs/reports/launcher/`.

## Уровень проверки

P2.3 является Level 0 / docs-only этапом, если меняется только этот контракт, progress report и manual checks log.

Для P2.3 не требуется:

- `compileall`;
- `ofz-quality --fast`;
- `ofz-quality --full`.

Достаточные проверки:

- `git status --short`;
- `git diff --name-only`;
- staged generated artifacts check;
- `Select-String` по ключевым токенам контракта.
