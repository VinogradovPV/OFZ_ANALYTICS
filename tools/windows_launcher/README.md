# Windows GUI launcher для OFZ Analytics

`ofz_launcher.ps1` - это безопасная PowerShell-оболочка над утвержденными CLI-командами проекта OFZ Analytics. Launcher не принимает произвольные shell-команды, не запускает внутренние Python-функции напрямую и не меняет `data/raw`.

## Как открыть GUI

Из корня проекта:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Gui
```

Автозакрытие только для smoke-проверок:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Gui -AutoCloseGuiForCheck
```

Обычный smoke без GUI:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1
```

## Поля GUI

| Поле | Что означает |
|---|---|
| Project root | Корень проекта `OFZ_ANALYTICS`; все CLI-команды запускаются из него. |
| Report date | Отчетная дата в формате `YYYY-MM-DD`; должна быть первым днем месяца. |
| Retrospective years | Количество лет ретроспективы, допустимый диапазон `1..10`. |
| Period type | Тип периода: `month`, `quarter` или `year`. |
| Aggregation | Режим агрегации: `cumulative` или `point`. |
| Action | Одна выбранная whitelisted-команда launcher. |
| Cleanup mode | Быстрый выбор cleanup-действия: keep, dry-run, archive-all или delete-all-with-archive. |
| Checkboxes | Подсказки для schema/quality/release/open actions; команды не объединяются автоматически. |
| Confirm DELETE_OUTPUTS | Обязательный токен для `cleanup-delete-all`. |
| Confirm BUILD_RELEASE_BUNDLE | Обязательный токен для `release-build`. |
| Command preview | Точная CLI-команда или пояснение для локального validate-действия. |
| Output/status | Краткий результат, exit code и путь к полному launcher log. |

## Типовые сценарии

### A. Проверить окружение

В GUI выберите `Action = validate-environment` и нажмите `Validate` или `Run selected`.

CLI-вариант:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Action validate-environment
```

Проверяются локальные пути и entry points: project root, `pyproject.toml`, `.venv\Scripts`, `data\raw`, `ofz-run.exe`, `ofz-schema.exe`, `ofz-quality.exe`, `ofz-clean-outputs.exe`, `ofz-build-release-bundle.exe`. Pipeline при этом не запускается.

### B. Запустить pipeline

Выберите `Action = run-pipeline`.

Команда строится как production default CLI:

```powershell
.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Launcher не передает ручной список stages для обычного `run-pipeline`.

### C. Запустить schema validation

Выберите `Action = schema`.

### D. Запустить quality-fast

Выберите `Action = quality-fast`. `quality-full` является ручным действием и запускается только при явном выборе `Action = quality-full`.

### E. Сделать cleanup dry-run

Выберите `Action = cleanup-dry-run` или `Cleanup mode = dry-run`. Токен `DELETE_OUTPUTS` не нужен.

### F. Сделать release bundle dry-run

Выберите `Action = release-dry-run`. Токен `BUILD_RELEASE_BUNDLE` не нужен.

### G. Создать release bundle

Выберите `Action = release-build`, заполните `Confirm BUILD_RELEASE_BUNDLE` значением:

```text
BUILD_RELEASE_BUNDLE
```

Без этого токена создание release bundle блокируется.

## Таблица actions

| Action | Что запускает | Нужен токен |
|---|---|---|
| `validate-environment` | Локальные проверки окружения, без CLI process. | Нет |
| `run-pipeline` | `ofz-run.exe` с report parameters. | Нет |
| `schema` | `ofz-schema.exe` с report parameters. | Нет |
| `quality-fast` | `ofz-quality.exe --fast` с report parameters. | Нет |
| `quality-full` | `ofz-quality.exe --full` с report parameters. | Нет, но запуск ручной |
| `cleanup-dry-run` | `ofz-clean-outputs.exe --dry-run`. | Нет |
| `cleanup-archive-all` | `ofz-clean-outputs.exe --archive-all`. | Нет |
| `cleanup-delete-all` | `ofz-clean-outputs.exe --archive-all --delete-all --confirm DELETE_OUTPUTS`. | `DELETE_OUTPUTS` |
| `release-dry-run` | `ofz-build-release-bundle.exe --dry-run` с report parameters. | Нет |
| `release-build` | `ofz-build-release-bundle.exe --include-outputs --confirm BUILD_RELEASE_BUNDLE` с report parameters. | `BUILD_RELEASE_BUNDLE` |
| `open-outputs` | Открывает папку `outputs`. | Нет |
| `open-releases` | Открывает папку `releases`, если она существует. | Нет |

## Что нельзя делать

- Нельзя коммитить generated launcher logs из `outputs/reports/launcher/`.
- Нельзя коммитить `releases/`.
- Нельзя использовать launcher для произвольных shell-команд.
- Нельзя обходить токены `DELETE_OUTPUTS` и `BUILD_RELEASE_BUNDLE`.
- Нельзя запускать `quality-fast` и `quality-full` параллельно.
- Нельзя менять `data/raw` через launcher.

## Где лежат логи

Launcher пишет логи в:

```text
outputs/reports/launcher/launcher_run_<timestamp>.log
```

Также рядом могут создаваться `stdout_<timestamp>.txt` и `stderr_<timestamp>.txt`. Это generated artifacts; они не входят в Git.

## Если упал run-pipeline

1. Посмотрите `Exit code` в Output/status.
2. Откройте файл из строки `Log: ...`.
3. Проверьте последние строки `STDERR` и `STDOUT`.
4. Убедитесь, что `Command preview` не содержит `--stages` для обычного `run-pipeline`.
5. Проверьте окружение через `validate-environment`.

## Если упал Preview

1. Нажмите `Preview` еще раз после выбора action.
2. Проверьте, что Project root указывает на корень проекта.
3. Запустите CLI preview без GUI:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Action run-pipeline -PreviewOnly
```

Если Preview показывает ошибку свойства или control, это bug launcher source и его нужно исправлять до P3.
