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

На каждой вкладке есть верхний блок `Назначение / Когда использовать / Как запускать / Что изменяет`. Он нужен, чтобы оператор понимал сценарий без внешней инструкции.

1. `Обзор`: папка проекта, дата отчета, параметры расчета, статус окружения, environment check и read-only Git status.
2. `Исходные данные Минфина`: простой сценарий проверки сайта, monthly update, annual-final, registry review и отдельные advanced-блоки для manual import/debug.
3. `Pipeline`: один основной запуск pipeline и понятный выбор этапа 0 Минфина через radio buttons.
4. `Проверки качества`: базовые, расширенные и source acquisition проверки, сгруппированные по назначению.
5. `Отчеты и графики`: основные результаты, ключевые ручные проверки и диагностические артефакты.
6. `Release и пакеты`: отдельные карточки release bundle и BI package.
7. `Обслуживание`: безопасная диагностика, открытие папок и отдельная зона очистки outputs.
8. `Журнал`: live output, время старта/завершения, exit code, log path, stop/copy/open actions.
9. `Справка`: русское объяснение workflow, параметров, confirm tokens и artifact policy.

Кнопки на вкладках запускают выбранные действия напрямую. Нижняя панель показывает технические детали: что будет выполнено, команда, изменяет ли action файлы, нужен ли confirm, log path и ожидаемый результат. Нижняя кнопка `Повторить выбранное действие` нужна только для повторного запуска уже выбранного action; копировать команду в консоль не требуется.

GUI разделяет пользовательский итог и технический журнал:

- `Итог операции` показывает понятный результат: успешно, ошибка, остановлено, что изменилось и следующий шаг.
- `Журнал` содержит stdout/stderr, JSON, команды и технический код завершения.
- Exit code показывается как `Технический код завершения`, но не является главным сообщением для оператора.

Кнопка `Открыть результаты` активна только для actions с реальной папкой результатов, например pipeline, release bundle или BI package. Для диагностик вроде проверки окружения, Git status, UTF-8/Mojibake или registry smoke доступны log controls: открыть log-файл, открыть папку logs и скопировать журнал.

## Безопасность

- Команды строятся только из allowlisted action IDs.
- `subprocess.Popen` получает список аргументов и `shell=False`.
- Subprocess получает `PYTHONUTF8=1` и `PYTHONIOENCODING=utf-8`, stdout/stderr читаются как UTF-8 с `errors="replace"`.
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

Основной сценарий вкладки Минфина:

1. `Проверить сайт Минфина` - live dry-run без изменения `raw`.
2. `Обновить данные текущего года` - monthly download после modal confirm `DOWNLOAD_MINFIN_SOURCE`.
3. `Проверить закрытие предыдущего года` - annual-final dry-run.
4. `Закрыть предыдущий год` - annual-final download после modal confirm `DOWNLOAD_MINFIN_SOURCE`.
5. `Проверить registry` - smoke-проверка registry/data audit.
6. `Открыть registry` и `Открыть отчеты source acquisition` - быстрые ссылки на рабочие папки.

Поля `URL override`, `HTML fixture`, `No network`, `Max pages` и аварийная кнопка `Replace changed final` скрыты в блоке `Показать расширенную диагностику парсера`. Ручной импорт XLSX скрыт в блоке `Показать аварийный ручной импорт` и используется только при недоступности сайта Минфина или изменении верстки.

Сначала выполните проверку сайта. При HTTP 503 GUI пишет: `Сайт Минфина временно недоступен; raw не изменен.`

После dry-run GUI показывает человекочитаемый итог: найденный XLSX, дату публикации/изменения, что raw не менялся, и следующий шаг. Технический JSON остается в журнале.

Pipeline stage 0 показывает radio buttons:

- `Не выполнять`;
- `Только dry-run`;
- `Download с подтверждением`.

Если stage 0 или optional schema validation завершились с ошибкой, pipeline не запускается.

## Проверки качества

Вкладка качества сгруппирована:

- `Базовые проверки`: UTF-8/Mojibake, Schema validation, Быстрая проверка качества.
- `Расширенные проверки`: Полная проверка качества, HTML chart QA, Visual regression.
- `Проверки source acquisition`: parser/source tests, registry smoke, data audit registry smoke.

Рекомендуемый порядок: UTF-8/Mojibake -> Schema validation -> Quality fast -> Quality full перед release -> Visual regression после изменений графиков.

## Отчеты, release и обслуживание

Вкладка отчетов разделяет основные результаты, ключевые ручные проверки и диагностику. После исправления методологии доходности вручную проверяйте, что базовые yield artifacts показывают доходность ОФЗ-ПД и не смешивают ее с ОФЗ-ПК.

Release build и BI build запускаются только после dry-run и modal confirm. Cleanup delete визуально отделен от безопасной диагностики и требует `DELETE_OUTPUTS`.

## Logs и artifacts

Python GUI launcher пишет объединенный stdout/stderr в runtime-папку вне `outputs/`:

```text
.ofz_launcher/logs/gui_run_<timestamp>.log
```

Эта папка не является generated analytical outputs. Cleanup outputs не трогает `.ofz_launcher/logs/`, поэтому активный GUI log не блокирует удаление `outputs/`. Generated reports остаются в `outputs/reports/`.

Не коммитить `outputs/`, `releases/`, `logs/`, `.ofz_launcher/`, `data/processed/`, source acquisition reports и `data/raw/minfin/ofz_auction_results/versions/`.

## Режим проверки registry

В интерфейсе режимы registry показываются пользовательскими названиями:

- `Не проверять registry` -> internal `off`;
- `Проверять и предупреждать` -> internal `warn`;
- `Требовать корректный registry` -> internal `strict`.

В CLI и command builder всегда передается internal value `off|warn|strict`. Рекомендуемый режим для обычной работы: `Проверять и предупреждать`. Строгий режим включайте после полного перехода на controlled source registry.

Начиная с NEXT.8 pipeline action реально добавляет эти параметры в `ofz-run.exe`: выбранный режим превращается в `--source-registry-mode <off|warn|strict>`, а checkbox `Разрешить legacy-данные` превращается в `--allow-legacy-raw` или `--no-allow-legacy-raw`. Default GUI state остается `warn + allow-legacy-raw`; strict-by-default не включен.

## Cleanup outputs

`Cleanup dry-run` только строит план очистки и ничего не удаляет. `Удалить outputs` требует `DELETE_OUTPUTS`, удаляет generated outputs и не меняет raw-данные. GUI logs сохраняются в `.ofz_launcher/logs/`.

Если cleanup сообщает PermissionError, вероятно, один из HTML/XLSX/report-файлов открыт браузером, Excel или другой программой. Закройте открытые отчеты/графики и повторите cleanup; технические подробности останутся в журнале.

## Диагностика

Headless smoke:

```powershell
.\.venv\Scripts\ofz-gui.exe --smoke
.\.venv\Scripts\ofz-gui.exe --smoke-ui
.\.venv\Scripts\python.exe scripts\qa\gui_launcher_smoke.py
.\.venv\Scripts\python.exe scripts\qa\gui_command_runner_smoke.py
```

При ошибке открыть вкладку `Журнал`, проверить exit code, последнюю команду и полный log-файл.
