# Desktop GUI launcher OFZ Analytics

Дата актуализации: 2026-06-22.

## Установка и запуск

Из корня проекта:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\ofz-gui.exe
```

Совместимый wrapper:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1
```

Wrapper содержит только поиск project root/entry point, UTF-8 setup и запуск GUI. Основная логика находится в `scripts/gui_launcher/`.

## Вкладки

1. `Обзор`: общие report parameters, environment check и read-only Git status.
2. `Исходные данные Минфина`: monthly, annual-final, manual-import, fixtures и registry/report folders.
3. `Pipeline`: обычный запуск, optional schema и Минфин stage 0.
4. `Проверки качества`: encoding, schema, quality fast/full, targeted source QA, HTML QA и visual regression.
5. `Отчеты и графики`: generated folders, monthly metrics и yield ОФЗ-ПД quick links.
6. `Release и пакеты`: release bundle и BI package dry-run/build.
7. `Обслуживание`: artifact guard, Git status, cleanup и рабочие каталоги.
8. `Журнал`: live output, exit code, log path, stop/copy/open actions.
9. `Справка`: русское объяснение workflow и параметров.

Выбранное действие показывает command preview в общей нижней панели. Кнопка `Выполнить` запускает команду; копировать ее в консоль не требуется.

## Безопасность

- Команды строятся только из allowlisted action IDs.
- `subprocess.Popen` получает список аргументов и `shell=False`.
- Одновременно выполняется только одна sequence.
- При non-zero exit code последующие шаги не запускаются.
- Произвольной shell-команды в интерфейсе нет.

Typed confirm tokens:

| Действие | Token |
| --- | --- |
| Monthly/annual-final download | `DOWNLOAD_MINFIN_SOURCE` |
| Changed final replacement | `REPLACE_MINFIN_FINAL` |
| Manual import | `IMPORT_MINFIN_FILE` |
| Release bundle build | `BUILD_RELEASE_BUNDLE` |
| BI package build | `BUILD_BI_PACKAGE` |
| Delete outputs | `DELETE_OUTPUTS` |

## Минфин и stage 0

Сначала выполнить dry-run. При HTTP 503 GUI пишет: `Сайт Минфина временно недоступен; raw не изменен.`

Pipeline stage 0 поддерживает `off`, `dry-run` и подтвержденный `download`. Если stage 0 завершился с ошибкой, pipeline не запускается.

## Logs и artifacts

Launcher пишет объединенный stdout/stderr в:

```text
outputs/reports/launcher/gui_run_<timestamp>.log
```

Не коммитить `outputs/`, `releases/`, `logs/`, `data/processed/`, source acquisition reports и `data/raw/minfin/ofz_auction_results/versions/`.

## Диагностика

Headless smoke:

```powershell
.\.venv\Scripts\ofz-gui.exe --smoke
.\.venv\Scripts\ofz-gui.exe --smoke-ui
.\.venv\Scripts\python.exe scripts\qa\gui_launcher_smoke.py
.\.venv\Scripts\python.exe scripts\qa\gui_command_runner_smoke.py
```

При ошибке открыть вкладку `Журнал`, проверить exit code, последнюю команду и полный log-файл.
