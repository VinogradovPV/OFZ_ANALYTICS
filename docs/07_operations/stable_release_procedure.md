# Процедура stable release

Дата актуализации: 2026-06-17.

Эта процедура описывает стабильный release flow с учетом P3 source acquisition. Все команды выполняются из корня проекта:

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics
```

GitHub release (`gh release create/upload`) выполняется только после отдельного явного разрешения пользователя. Эта процедура не дает такого разрешения сама по себе.

## 1. Preflight

Проверить рабочее дерево:

```powershell
git status --short --branch
```

Перед релизом допустимы только осознанные source/docs/config/data changes. Generated outputs не должны быть staged.

Проверить CLI:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --help
.\.venv\Scripts\ofz-quality.exe --help
.\.venv\Scripts\ofz-build-release-bundle.exe --help
```

## 2. Source acquisition dry-run

Для текущего года выполнить dry-run:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode monthly --dry-run
```

Проверить:

- выбранный XLSX относится к section `id_66`;
- pagination использует `page_66`;
- URL файла резолвится от `https://minfin.gov.ru`;
- filename соответствует `INTERNET_Auction_Results_rus_YYYY_*.xlsx`;
- monthly title содержит `на DD.MM.YYYY`;
- warnings отсутствуют или понятны.

Если релиз январский и нужно закрыть предыдущий год:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY-1 --mode annual-final --dry-run
```

Annual-final title обычно не содержит `на DD.MM.YYYY`, а имя файла не обязано заканчиваться на `YYYY1231`.

## 3. Monthly/annual-final update, если нужно

Если dry-run показывает новый monthly source и обновление нужно включить в релиз:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode monthly --download --confirm DOWNLOAD_MINFIN_SOURCE
```

Если нужно создать annual-final для предыдущего года:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY-1 --mode annual-final --download --confirm DOWNLOAD_MINFIN_SOURCE
```

Если existing final hash отличается, остановиться и выполнить ручную проверку. Замена final допустима только после review:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY-1 --mode annual-final --download --confirm REPLACE_MINFIN_FINAL
```

Manual fallback допускается только для корректного локального XLSX:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode manual-import --manual-file C:\path\INTERNET_Auction_Results_rus_YYYY_YYYYMMDD.xlsx --dry-run
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode manual-import --manual-file C:\path\INTERNET_Auction_Results_rus_YYYY_YYYYMMDD.xlsx --download --confirm IMPORT_MINFIN_FILE
```

`versions/` и `outputs/reports/source_acquisition/` не коммитятся.

## 4. Registry review

Проверить controlled registry:

```text
data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources.csv
data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources_latest.json
```

Проверить:

- active row для актуального `latest`;
- active row для `final`, если выполнялся annual-final;
- `sha256`;
- `file_size_bytes`;
- `storage_role`;
- `is_active_for_pipeline`;
- `discovery_method`;
- HTML provenance или manual import notes.

Если registry отсутствует или еще не полностью migrated, data audit в default `warn` mode должен явно показать legacy fallback.

## 5. Data audit

Запустить data audit с registry validation:

```powershell
.\.venv\Scripts\python.exe scripts\01_data_audit.py --source-registry-mode warn --allow-legacy-raw
```

Проверить в `docs/02_data_pipeline/data_audit.md` раздел `Source registry validation`:

- `source_registry_mode`;
- `source_registry_status`;
- `controlled_source_used`;
- `legacy_raw_fallback_used`;
- `registry_warnings_count`;
- `registry_errors_count`.

Для strict pre-release gate, когда controlled source migration уже считается обязательной:

```powershell
.\.venv\Scripts\python.exe scripts\01_data_audit.py --source-registry-mode strict
```

Strict mode не должен использовать legacy fallback.

## 6. Quality-fast

Выполнить fast quality gate:

```powershell
.\.venv\Scripts\ofz-quality.exe --fast --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Все `FAIL` должны быть исправлены или релиз остановлен.

## 7. Screenshot validation outside sandbox

Screenshot validation выполнять из обычной проектной PowerShell-сессии outside sandbox, если браузерный backend доступен:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode screenshot --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Если screenshot backend недоступен, выполнить fallback/auto и явно записать ограничение:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode auto --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Screenshot artifacts under `outputs/reports/visual_regression/` are generated outputs and are not committed.

## 8. Quality-full

Перед stable release выполнить full gate:

```powershell
.\.venv\Scripts\ofz-quality.exe --full --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Full gate может быть дольше fast gate. Релиз не продолжается при `FAIL`.

## 9. Release bundle dry-run

Сначала dry-run:

```powershell
.\.venv\Scripts\ofz-build-release-bundle.exe --dry-run --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Проверить список planned artifacts и отсутствие неожиданных missing items.

## 10. Release bundle build

После dry-run:

```powershell
.\.venv\Scripts\ofz-build-release-bundle.exe --include-outputs --confirm BUILD_RELEASE_BUNDLE --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Release bundle создается под ignored `releases/` и не коммитится.

## 11. Опциональный BI-пакет

Если релиз включает BI handoff, сначала dry-run:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --dry-run --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Затем build:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --include-outputs --confirm BUILD_BI_PACKAGE --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

BI package также является external artifact и не коммитится.

## 12. Финальная git-проверка

Проверить staged files:

```powershell
git status --short
git diff --cached --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|outputs/reports/source_acquisition|data/processed|logs|releases|docm|tmp|temp|crdownload|part|data/raw/minfin/ofz_auction_results/versions"
```

Если filter что-то вывел, убрать generated artifact из stage.

Допустимые source acquisition paths после controlled update:

- `data/raw/minfin/ofz_auction_results/latest/`;
- `data/raw/minfin/ofz_auction_results/final/`;
- `data/raw/minfin/ofz_auction_results/registry/`.

Недопустимые paths:

- `data/raw/minfin/ofz_auction_results/versions/`;
- `outputs/reports/source_acquisition/`;
- `outputs/tmp/`;
- `releases/`;
- generated chart/export/dashboard/report outputs.

## 13. Git tag

После успешного commit/push stable release можно создать tag:

```powershell
git tag -a vX.Y.Z -m "Stable release vX.Y.Z"
git push origin vX.Y.Z
```

Tag создавать только после финальной проверки release contents.

## 14. GitHub release только по отдельному разрешению

`gh release create`, `gh release upload`, изменение release assets и публикация GitHub Release выполняются только после отдельного явного разрешения пользователя.

Команды ниже являются примером, а не разрешением:

```powershell
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file RELEASE_NOTES.md
gh release upload vX.Y.Z releases\...\*
```

Если такого разрешения нет, остановиться после tag/push или после локального release bundle.
