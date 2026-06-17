# Minfin source acquisition operation design

## P3.6 Registry Validation In Data Audit

Data audit теперь умеет проверять controlled Minfin source registry, но не меняет legacy ingestion.

Default behavior:

```text
source-registry-mode=warn
allow-legacy-raw=true
```

Operational modes:

1. `off`: registry не читается, legacy raw audit идет как раньше.
2. `warn`: registry читается при наличии; validation problems видны в audit report, но legacy raw fallback продолжает работу.
3. `strict`: registry обязателен; missing registry, duplicate active rows, missing active file, hash mismatch и size mismatch блокируют audit.

В audit report добавляется раздел `Source registry validation` с полями:

- `source_registry_mode`
- `source_registry_status`
- `controlled_source_used`
- `legacy_raw_fallback_used`
- `registry_warnings_count`
- `registry_errors_count`

P3.6 не выполняет live network calls и не переключает pipeline на controlled files. Cleaning behavior не меняется.

## P3.5 Manual Fallback Import

Manual fallback используется, когда сайт Минфина недоступен или HTML-верстка изменилась, но оператор получил корректный Excel-файл вручную.

Команды:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode manual-import --manual-file C:\path\INTERNET_Auction_Results_rus_2026_YYYYMMDD.xlsx --dry-run
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode manual-import --manual-file C:\path\INTERNET_Auction_Results_rus_2026_YYYYMMDD.xlsx --download --confirm IMPORT_MINFIN_FILE
```

Правила:

1. `--manual-file` является canonical option для ручного импорта.
2. `--download` в режиме `manual-import` заблокирован без `--confirm IMPORT_MINFIN_FILE`.
3. Файл должен существовать, быть обычным файлом, иметь расширение `.xlsx`, соответствовать шаблону `INTERNET_Auction_Results_rus_<year>_*.xlsx` и году `--year`.
4. Dry-run считает `sha256` и `file_size_bytes`, показывает planned role/path и не создает raw storage.
5. Import использует temp+promote workflow: исходный локальный файл сначала копируется во временный путь, затем продвигается после валидации и hash compare.
6. При новом hash manual import обновляет `latest/` и пишет version snapshot.
7. При неизменном hash manual import пишет observation и не выполняет повторную копию в `latest/`.
8. `final/` не создается и не перезаписывается через `manual-import`; annual-final replacement остается только в `annual-final` workflow.
9. Registry row получает `discovery_method=manual-import`, `publication_period=manual-import`; `notes` содержит `original_local_file=...`.
10. Blind copy запрещен: promote выполняется только после имени/года/расширения/hash validation.

## P3.4 Annual-Final Workflow

Annual-final mode закрывает предыдущий год и пишет только подтвержденный `final` источник.

Команды:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2025 --mode annual-final --dry-run --no-network
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2025 --mode annual-final --download --confirm DOWNLOAD_MINFIN_SOURCE
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2025 --mode annual-final --download --confirm REPLACE_MINFIN_FINAL
```

Правила выбора:

1. Используется только HTML section 66: `id_66`, `page_66`, `ajax-pagination-content-10090-66`.
2. Кандидат должен быть XLSX из `a.file_item`, относительные ссылки резолвятся от `https://minfin.gov.ru`.
3. Заголовок annual-final не должен содержать `на DD.MM.YYYY`.
4. Суффикс `YYYY1231` в имени файла не требуется; валидируется год в имени `INTERNET_Auction_Results_rus_<year>_*.xlsx`.
5. Приоритет имеют документы, опубликованные или измененные в январе-феврале года `year + 1`.

Правила продвижения:

1. Скачивание разрешено только с `--download --confirm DOWNLOAD_MINFIN_SOURCE` или `--download --confirm REPLACE_MINFIN_FINAL`.
2. Файл сначала скачивается во временный путь, затем валидируется, хэшируется и только после этого продвигается.
3. Если `final` отсутствует, файл создается после успешной валидации.
4. Если existing final имеет тот же sha256, замена не выполняется.
5. Если existing final имеет другой sha256, замена блокируется без `REPLACE_MINFIN_FINAL`.
6. Registry row пишется со `storage_role=final`, `publication_period=annual-final` и HTML provenance.
7. Active final row включается только при создании нового final или подтвержденной замене.
8. Partial temp file удаляется после завершения workflow.

Дата актуализации: 2026-06-16.

## Status

Design-only P3.0 document. No downloader code is implemented in this step.

Prerequisites completed:

- `P3.PRE.1 Scripts balance/problem audit`
- `P3.PRE.2 Docs mojibake/encoding audit and UTF-8 normalization`

## Policy

The required acquisition policy is:

```text
Variant C - hybrid latest + final + version snapshots on hash change
```

This policy balances operational simplicity and auditability:

- `latest/` gives pipeline a stable current input.
- `final/` freezes prior-year annual sources after January review.
- `versions/` preserves only meaningful hash changes.
- `registry/` records every decision and source identity.

## Source

Minfin OFZ auction page:

```text
https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/#tablitsy_po_rezultatam_provedeniya_auktsionov
```

Fallback page URL without anchor:

```text
https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction
```

Expected source section:

```text
Результаты проведенных аукционов по размещению государственных ценных бумаг в...
```

Expected file pattern:

```text
INTERNET_Auction_Results_rus_<year>_....xlsx
```

Note: during P3.0 design review on 2026-06-16, both the anchored URL and the same page URL without anchor returned `503 Service Unavailable`. The future tool must treat this as a normal operational failure mode, not as a reason to mutate local source files.

## Monthly Lifecycle

Monthly mode is used for the current year while Minfin continues to update the year file.

Future command:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --dry-run
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --download
```

Monthly lifecycle:

1. Discover the source page and candidate Excel link for the requested year.
2. Validate filename pattern and year.
3. In `--dry-run`, report planned target paths, previous hash, candidate hash if available, and whether a change would be detected.
4. In `--download`, download into a temporary file outside final target paths.
5. Compute `sha256` and `file_size_bytes`.
6. If hash equals the current active `latest` hash, update registry observation metadata only when useful; do not create a new version snapshot.
7. If hash differs, write a version snapshot under `versions/<year>/`, update `latest/`, and add a registry row with `change_detected=true`.
8. Mark the new `latest` row as `is_active_for_pipeline=true`.
9. Leave `final/` unchanged.

## January Annual-Final Lifecycle

Annual-final mode is used after the prior year is considered complete, typically in January.

Future command:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2025 --mode annual-final --download
```

Annual-final lifecycle:

1. Discover and download the prior-year file.
2. Compute hash and compare to current `latest` and existing `final`.
3. If a final copy already exists with the same hash, record no file change.
4. If no final exists, write `final/INTERNET_Auction_Results_rus_<year>_final.xlsx`.
5. If final exists with a different hash, require manual review before replacing it.
6. Add or update registry rows with `storage_role=final`.
7. Mark the final row as `is_active_for_pipeline=true` for that year after approval.
8. Keep versions snapshots external/ignored unless artifact policy changes.

## Storage Structure

```text
data/raw/minfin/ofz_auction_results/
  latest/
  versions/
  final/
  registry/
```

Tracked by default:

- `latest/`
- `final/`
- `registry/`

External or ignored by default:

- `versions/`

The future implementation must create parent directories only when running an explicit download/import command. Design docs do not create raw storage directories.

## Future CLI Contract

Planned entry point:

```text
ofz-fetch-minfin = scripts.source_acquisition.minfin_fetch:main
```

Planned commands:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --dry-run
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --download
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2025 --mode annual-final --download
```

Required behavior:

- `--dry-run` never writes raw files.
- `--download` writes only through the controlled storage policy.
- `--mode monthly` targets `latest/` plus optional `versions/` snapshot on hash change.
- `--mode annual-final` targets `final/` and requires stricter replacement rules.
- Commands must be idempotent for unchanged hashes.

## Failure Behavior

If the Minfin site or file endpoint is unavailable:

- fail closed;
- do not modify `latest/`, `final/`, `registry/`, or `versions/`;
- do not leave partial files in tracked paths;
- return a non-zero code for `--download`;
- for `--dry-run`, return a clear warning and no planned mutation;
- include source URL, year, mode, HTTP status or network exception and next action.

If parsing the page fails:

- do not guess file URLs;
- report discovered links, if any;
- require manual fallback or parser update.

If hash changes unexpectedly for a final year:

- store as manual candidate or version snapshot only when explicitly allowed;
- do not replace `final/` automatically;
- require operator review.

## Manual Fallback Import

Manual fallback is allowed when the Minfin site is temporarily unavailable or the page markup changes.

Planned future command shape:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --manual-file C:\path\INTERNET_Auction_Results_rus_2026_YYYYMMDD.xlsx --dry-run
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --manual-file C:\path\INTERNET_Auction_Results_rus_2026_YYYYMMDD.xlsx --download
```

Manual import rules:

- validate extension `.xlsx`;
- validate filename year;
- compute `sha256`;
- write registry row with `publication_period=manual-import` until reviewed;
- preserve original filename in `notes`;
- never overwrite `final/` without explicit annual-final review.

## Integration With Existing Pipeline

Future integration sequence:

```text
ofz-fetch-minfin
  -> data/raw/minfin/ofz_auction_results/registry/
  -> raw_data_registry.py
  -> 01_data_audit.py
  -> 02_data_cleaning.py
```

The existing pipeline should not directly scrape Minfin. It should consume controlled raw files selected by registry state.

P3 implementation should add integration gradually:

1. Add source acquisition package and dry-run parser.
2. Add registry writer without changing existing cleaning behavior.
3. Add compatibility path or migration from current `data/raw/INTERNET_Auction_Results_rus_*.xlsx`.
4. Add targeted tests for dry-run, unchanged hash, changed hash, manual import, and site unavailable.
5. Only then connect production runbook to `ofz-fetch-minfin`.

## P3.1 Skeleton Implementation

Дата обновления: 2026-06-17.

P3.1 добавляет только skeleton source acquisition и offline HTML-aware parser. Реальное скачивание, запись registry в `data/raw`, создание `data/raw/minfin/ofz_auction_results/` и изменение raw Excel файлов на этом этапе запрещены.

CLI entry point:

```text
ofz-fetch-minfin = scripts.source_acquisition.minfin_fetch:main
```

Поддерживаемые dry-run опции P3.1:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --dry-run --no-network
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --dry-run --html-file tests\fixtures\minfin_auction_page_section_66_sample.html
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2025 --mode annual-final --dry-run --html-file tests\fixtures\minfin_auction_page_section_66_sample.html
```

Parser contract:

- target section: `id_66`, `page_66`, `ajax-pagination-content-10090-66`;
- ignored sections: `65`, `38`, `39`;
- file links are read only from `a.file_item`;
- relative file URLs are resolved against `https://minfin.gov.ru`;
- pagination metadata is read from `ajax-pagination-10090-66`;
- monthly selection prefers title with `на DD.MM.YYYY`;
- annual-final selection does not require file suffix `YYYY1231`.

P3.1 deliberately blocks `--download` and `--save-html-snapshot`. Live network discovery is not implemented in this stage; `--no-network` dry-run returns a non-mutating plan with warning when no local `--html-file` is supplied.

## P3.3 Monthly Acquisition Implementation

Дата обновления: 2026-06-17.

P3.3 реализует controlled monthly acquisition workflow для текущего года. Реальный download разрешен только при явном подтверждении:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --download --confirm DOWNLOAD_MINFIN_SOURCE
```

Без confirm команда должна завершаться с ошибкой до network/raw mutation:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --download
```

Monthly workflow:

1. Fetch base page.
2. Parse target section 66.
3. Read `page_66` pagination count.
4. Fetch `page_66=2..N`.
5. Extract XLSX candidates only from section 66.
6. Select monthly candidate by max `as_of_date`.
7. Download selected `absolute_file_url` to temp path under ignored `outputs/tmp/source_acquisition/`.
8. Validate `.xlsx` extension and filename year.
9. Compute SHA-256 and file size.
10. Compare with current active `latest` hash from registry.
11. If unchanged, append an `observation` registry row and create no version snapshot.
12. If changed, write `versions/<year>/` snapshot, update `latest/`, and append active `latest` registry row.
13. Write CSV/JSON registry.
14. Write source acquisition report under ignored `outputs/reports/source_acquisition/`.

Failure behavior:

- Page fetch or network failure must not mutate raw storage.
- Failed file download must not leave partial downloaded files.
- `versions/` and `outputs/reports/source_acquisition/` remain generated/external artifacts and must not be staged by default.
