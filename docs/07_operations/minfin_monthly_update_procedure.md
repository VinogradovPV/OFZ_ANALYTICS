# Операционная инструкция: ежемесячное обновление данных Минфина

## NEXT.7 - strict registry migration note

Дата актуализации: 2026-06-25.

Ежемесячный workflow пока остается в совместимом режиме `warn + allow-legacy-raw`. Проверка `strict --no-allow-legacy-raw` проходит на уровне `scripts/01_data_audit.py`, но `ofz-run.exe` еще не поддерживает передачу этих параметров в полный pipeline.

До отдельного approval оператор не должен включать strict mode как default, отключать legacy fallback по умолчанию, обходить `ofz-fetch-minfin` ручным копированием XLSX в raw или коммитить файлы из `data/raw/minfin/ofz_auction_results/versions/`.

Подробный план перехода: `docs/00_project/source_registry_strict_migration_plan.md`.

Дата актуализации: 2026-06-17.

Документ описывает ручной операторский порядок обновления источников Минфина для ОФЗ: ежемесячный `monthly` update, январское закрытие `annual-final`, обработку изменившегося final hash и ручной fallback import. Автоматическое скачивание по расписанию не включается.

## 1. Основные правила

Все команды выполнять из корня проекта:

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics
```

Использовать локальные CLI entry points:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --help
.\.venv\Scripts\ofz-quality.exe --help
```

`ofz-fetch-minfin` работает с целевой секцией страницы Минфина:

- anchor: `tablitsy_po_rezultatam_provedeniya_auktsionov`;
- section/document ids: `id_66`;
- pagination parameter: `page_66`;
- content container: `ajax-pagination-content-10090-66`;
- pagination id: `ajax-pagination-10090-66`;
- file links: только `a.file_item`;
- relative links resolve against `https://minfin.gov.ru`.

Parser должен игнорировать другие секции страницы, включая `65`, `38` и `39`.

## 2. Как понять, что выбран правильный XLSX

Для monthly:

1. В dry-run выбранный файл должен иметь имя вида `INTERNET_Auction_Results_rus_YYYY_YYYYMMDD.xlsx`.
2. Год в имени файла должен совпадать с `--year`.
3. Заголовок документа должен содержать `на DD.MM.YYYY`.
4. Если найдено несколько monthly-кандидатов, выбирается максимальная `as_of_date`.
5. `absolute_file_url` должен указывать на `https://minfin.gov.ru/...xlsx`.

Для annual-final:

1. Год в имени файла должен совпадать с `--year`.
2. Заголовок обычно не содержит `на DD.MM.YYYY`.
3. Суффикс имени файла не обязан быть `YYYY1231`; например, `INTERNET_Auction_Results_rus_2025_20251230.xlsx` допустим.
4. Предпочтительны документы, опубликованные или измененные в январе-феврале года `year + 1`.
5. При сомнении сначала остановиться на dry-run и не запускать replace.

## 3. Ежемесячное обновление

Пример для текущего года `YYYY`.

Сначала dry-run:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode monthly --dry-run
```

Dry-run выполняет live discovery страницы Минфина, но не скачивает XLSX и не меняет `raw`. Для offline проверки parser можно использовать `--html-file`; для безопасной проверки без сети - `--no-network`.

Проверить в JSON-выводе:

- `selected_candidate.file_name`;
- `selected_candidate.as_of_date`;
- `selected_candidate.absolute_file_url`;
- planned paths для `latest`, `registry`, `versions`;
- warnings.

Если выбран правильный XLSX, выполнить controlled download:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode monthly --download --confirm DOWNLOAD_MINFIN_SOURCE
```

После скачивания выполнить fast quality gate для отчетного месяца. Дата отчета всегда первое число месяца:

```powershell
.\.venv\Scripts\ofz-quality.exe --fast --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Если hash не изменился, workflow не должен создавать новый snapshot в `versions/`; registry получит observation. Если hash изменился, обновляется `latest/`, пишется version snapshot и registry row.

## 4. Январское annual-final закрытие

В январе закрывается предыдущий год. Если сейчас год `YYYY`, закрываем `YYYY-1`.

Сначала dry-run:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY-1 --mode annual-final --dry-run
```

Проверить:

- selected candidate относится к предыдущему году;
- заголовок без monthly-фразы `на DD.MM.YYYY`;
- файл `.xlsx`;
- год в имени файла соответствует `YYYY-1`;
- отсутствие требования `YYYY1231` соблюдается.

Если final отсутствует или hash совпадает с ожидаемым, выполнить:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY-1 --mode annual-final --download --confirm DOWNLOAD_MINFIN_SOURCE
```

Annual-final пишет `storage_role=final` в registry. `final` становится активным только после успешного controlled workflow.

## 5. Что делать при changed final hash

Если annual-final обнаружил, что существующий final имеет другой hash, обычный confirm должен заблокировать замену. Это нормальное защитное поведение.

Порядок действий:

1. Не повторять команду вслепую.
2. Сравнить `selected_candidate`, `existing_final_sha256`, новый `sha256`, `published_at`, `modified_at`, `document_title`.
3. Убедиться, что файл действительно является финальным файлом года, а не monthly update.
4. Зафиксировать причину ручной замены в рабочем журнале или commit message.
5. Только после ручной проверки выполнить:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY-1 --mode annual-final --download --confirm REPLACE_MINFIN_FINAL
```

`REPLACE_MINFIN_FINAL` не использовать для обычного monthly update.

## 6. Manual fallback, если сайт недоступен или изменилась верстка

Manual fallback используется, если:

- Минфин возвращает `503 Service Unavailable`;
- сеть недоступна;
- parser перестал находить section 66 из-за изменения HTML;
- оператор вручную скачал корректный XLSX.

Dry-run manual import:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode manual-import --manual-file C:\path\INTERNET_Auction_Results_rus_YYYY_YYYYMMDD.xlsx --dry-run
```

Проверить:

- файл существует;
- расширение `.xlsx`;
- имя соответствует `INTERNET_Auction_Results_rus_YYYY_YYYYMMDD.xlsx`;
- год в имени совпадает с `--year`;
- dry-run показывает `sha256`, `file_size_bytes`, planned role/path;
- `final_path` не планируется.

Импорт после проверки:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode manual-import --manual-file C:\path\INTERNET_Auction_Results_rus_YYYY_YYYYMMDD.xlsx --download --confirm IMPORT_MINFIN_FILE
```

Manual import не должен перезаписывать `final/`; annual-final replacement выполняется только через `annual-final` workflow.

## 7. Что делать при 503

Если Минфин вернул `503`:

1. Не создавать и не править raw-файлы вручную в controlled storage.
2. Повторить dry-run позже.
3. Если обновление срочное, скачать XLSX вручную с сайта/официального источника и использовать `manual-import`.
4. Не коммитить partial downloads, `.part`, `.crdownload`, temp files.
5. В progress/manual log указать, что live site был недоступен и использован manual fallback или обновление отложено.

`503` не является причиной для guessed URL или ручной записи registry без файла.

## 8. Commit policy

Можно коммитить:

- `data/raw/minfin/ofz_auction_results/latest/`, если monthly/manual import действительно обновил active latest;
- `data/raw/minfin/ofz_auction_results/final/`, если annual-final действительно создан или подтвержденно заменен;
- `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources.csv`;
- `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources_latest.json`;
- документацию, source code и QA fixtures.

Нельзя коммитить:

- `data/raw/minfin/ofz_auction_results/versions/`;
- `outputs/reports/source_acquisition/`;
- `outputs/tmp/`;
- `outputs/charts/`, `outputs/exports/`, `outputs/dashboards/`, `outputs/archive/`;
- `data/processed/`;
- `logs/`;
- `releases/`;
- `*.tmp`, `*.part`, `*.crdownload`;
- Office macro packages `.docm` без отдельного artifact policy decision.

Перед commit обязательно проверить staged paths:

```powershell
git status --short
git diff --cached --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|outputs/reports/source_acquisition|data/processed|logs|releases|docm|tmp|temp|crdownload|part|data/raw/minfin/ofz_auction_results/versions"
```

Если filter что-то вывел, остановиться и убрать generated artifact из stage.

## 9. Windows Task Scheduler: только reminder

Допустим только reminder-only план:

- создать напоминание раз в месяц открыть эту инструкцию и выполнить dry-run вручную;
- создать отдельное январское напоминание для annual-final dry-run;
- не запускать `--download` автоматически;
- не хранить confirm tokens в scheduler;
- не запускать `REPLACE_MINFIN_FINAL` по расписанию.

Смысл scheduler здесь - напомнить оператору, а не выполнять download.

## 10. Минимальный monthly checklist

1. `git status --short` проверен.
2. Выполнен monthly dry-run.
3. Проверен выбранный XLSX.
4. Выполнен download только с `DOWNLOAD_MINFIN_SOURCE`.
5. Выполнен `ofz-quality --fast`.
6. Проверены staged paths.
7. В commit не попали `versions/` и `outputs/reports/source_acquisition/`.

## 11. Минимальный annual-final checklist

1. Выполнен annual-final dry-run для `YYYY-1`.
2. Проверено, что заголовок без `на DD.MM.YYYY`.
3. Проверено, что файл `.xlsx` и год в имени правильный.
4. Если hash совпал или final отсутствует, использован `DOWNLOAD_MINFIN_SOURCE`.
5. Если hash отличается, выполнена ручная проверка и только затем `REPLACE_MINFIN_FINAL`.
6. Проверены registry rows и staged paths.
