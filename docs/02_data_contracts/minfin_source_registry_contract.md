# Minfin source registry contract

## P3.6 Data Audit Integration Contract

Дата: 2026-06-17.

Data audit поддерживает validation-only интеграцию controlled Minfin registry без переключения legacy pipeline на controlled source.

CLI параметры `scripts/01_data_audit.py`:

```powershell
.\.venv\Scripts\python.exe scripts\01_data_audit.py --source-registry-mode off
.\.venv\Scripts\python.exe scripts\01_data_audit.py --source-registry-mode warn --allow-legacy-raw
.\.venv\Scripts\python.exe scripts\01_data_audit.py --source-registry-mode strict
```

Default:

```text
source-registry-mode=warn
allow-legacy-raw=true
```

Режимы:

- `off`: registry не читается; legacy `data/raw` audit работает как раньше.
- `warn`: registry читается, если существует; ошибки registry пишутся как warnings/errors в audit report, но при доступном legacy raw pipeline продолжает работу.
- `strict`: registry обязателен; missing registry, duplicate active rows, missing active file и hash/size mismatch возвращают fail; legacy fallback не используется.

Validation helpers:

- `validate_source_registry(...)`
- `load_active_source_records(...)`
- `validate_active_file_hashes(...)`
- `summarize_registry_status(...)`

Data audit report обязан явно показывать:

- `source_registry_mode`
- `source_registry_status`
- `controlled_source_used`
- `legacy_raw_fallback_used`
- `registry_warnings_count`
- `registry_errors_count`

P3.6 не меняет cleaning behavior и не переключает Excel input selection на controlled source. Controlled source remains validation-only until a separate migration decision.

Дополнительные validation rules:

- Registry schema должна соответствовать `RegistryRecord`.
- Для одного `year + storage_role` не допускаются duplicate active rows.
- Active `latest` для текущего года проверяется при включенном controlled registry.
- Active file path для `latest`/`final` должен существовать в controlled storage layout.
- Active file `sha256` должен совпадать с registry.
- `file_size_bytes` должен совпадать, если поле заполнено.
- `discovery_method=html` требует `section_id`, `page_param`, `document_title`, а также `document_id` или `document_page_url`, `file_url` или `absolute_file_url`.
- `discovery_method=manual-import` должен содержать `notes` с `original_local_file=...`.
- Validation не выполняет live network calls.

Дата актуализации: 2026-06-16.

## Назначение

Этот контракт описывает будущий реестр controlled acquisition для исходных Excel-таблиц Минфина с результатами аукционов ОФЗ.

P3.0 является design-only этапом: downloader code, CLI entry point и изменения pipeline на этом шаге не создаются.

## Source

Основной источник:

```text
https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/#tablitsy_po_rezultatam_provedeniya_auktsionov
```

Fallback URL without anchor:

```text
https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction
```

Ожидаемый раздел страницы:

```text
Результаты проведенных аукционов по размещению государственных ценных бумаг в...
```

Ожидаемый шаблон файлов:

```text
INTERNET_Auction_Results_rus_<year>_....xlsx
```

## Acquisition Policy

Обязательная политика P3:

```text
Variant C - hybrid latest + final + version snapshots on hash change
```

Смысл политики:

- `latest/` хранит текущую активную копию файла по году для pipeline.
- `final/` хранит annual-final copy после январской фиксации прошедшего года.
- `versions/` хранит version snapshots только когда новый hash отличается от уже известного.
- `registry/` хранит machine-readable audit trail acquisition-решений.

## Storage Structure

```text
data/raw/minfin/ofz_auction_results/
  latest/
  versions/
  final/
  registry/
```

Recommended future file layout:

```text
data/raw/minfin/ofz_auction_results/latest/
  INTERNET_Auction_Results_rus_2026_latest.xlsx

data/raw/minfin/ofz_auction_results/final/
  INTERNET_Auction_Results_rus_2025_final.xlsx

data/raw/minfin/ofz_auction_results/versions/
  2026/
    INTERNET_Auction_Results_rus_2026_20260616_<sha12>.xlsx

data/raw/minfin/ofz_auction_results/registry/
  minfin_ofz_auction_sources.csv
  minfin_ofz_auction_sources_latest.json
```

## Git And Artifact Policy

Tracked by default:

- `data/raw/minfin/ofz_auction_results/latest/`
- `data/raw/minfin/ofz_auction_results/final/`
- `data/raw/minfin/ofz_auction_results/registry/`

External or ignored by default:

- `data/raw/minfin/ofz_auction_results/versions/`

If `versions/` snapshots must be committed later, that requires a separate artifact policy decision before staging.

## Registry Fields

| Field | Required | Type | Description |
|---|---:|---|---|
| `source_name` | yes | string | Stable source id, expected `minfin_ofz_auction_results`. |
| `source_url` | yes | string | Page URL or direct file URL used for acquisition. |
| `page_title` | yes | string | Page title or source page section title observed during discovery. |
| `link_text` | yes | string | Exact link text for the Excel file when available. |
| `file_name` | yes | string | Stored file name. |
| `year` | yes | integer | Auction results year inferred from filename/link. |
| `publication_period` | yes | string | `monthly`, `annual-final`, `manual-import`, or `unknown`. |
| `downloaded_at` | yes | datetime string | UTC timestamp when acquisition/import happened. |
| `source_last_modified` | no | datetime string | Last modified date parsed from page metadata if available. |
| `http_etag` | no | string | HTTP ETag header from the file response if available. |
| `http_last_modified` | no | datetime string | HTTP Last-Modified header from the file response if available. |
| `file_size_bytes` | yes | integer | Size of stored file in bytes. |
| `sha256` | yes | string | SHA-256 hash of stored file bytes. |
| `storage_role` | yes | string | `latest`, `version`, `final`, or `manual_candidate`. |
| `is_active_for_pipeline` | yes | boolean | Whether this row is the pipeline-selected source for its year. |
| `supersedes_sha256` | no | string | Previous SHA-256 superseded by this acquisition, when applicable. |
| `change_detected` | yes | boolean | True when downloaded/imported content differs from prior active hash. |
| `notes` | no | string | Human-readable notes, failures, manual import reason, or review decision. |

## Registry Invariants

- Exactly one `latest` row per active year should have `is_active_for_pipeline=true`, unless the year is intentionally excluded.
- A `final` row for a year supersedes `latest` for production runs after annual-final approval.
- `sha256` is the identity of file content; filename alone is not sufficient.
- `change_detected=false` must not create a new `versions/` snapshot.
- `versions/` rows must be reproducible from `sha256`, `source_url`, `downloaded_at`, and `file_size_bytes`.
- Manual imports must use `publication_period=manual-import` until reviewed and promoted.

## Integration Contract

Future flow:

```text
source acquisition
  -> source registry
  -> raw data registry
  -> data audit
  -> cleaning
```

The existing raw data registry should continue to treat `data/raw/` as source input and must not mutate raw files. The future acquisition step is the only controlled writer for `data/raw/minfin/ofz_auction_results/`.

## Failure Contract

If the Minfin site is unavailable, the future acquisition tool must:

- fail closed for `--download`;
- keep existing tracked `latest/`, `final/`, and `registry/` files unchanged;
- write no partial Excel file into tracked raw storage;
- return a non-zero exit code unless explicitly running `--dry-run`;
- emit a clear operator message with source URL, target year, mode and failure reason;
- suggest manual fallback import.

If only HTTP metadata is missing but file bytes download successfully, the acquisition may continue with blank `http_etag` / `http_last_modified` and a note.

## P3.2 Registry Writer Contract

Дата обновления: 2026-06-17.

P3.2 реализует registry writer layer без реального скачивания и без записи в настоящий `data/raw/minfin/ofz_auction_results/`. Проверки используют только temporary fixtures.

Поддерживаемые форматы:

- CSV registry с полным набором полей;
- JSON registry в форме `{ "records": [...] }`;
- append одного registry record в CSV;
- roundtrip чтение/запись CSV и JSON.

Storage roles:

```text
latest
version_snapshot
final
manual_candidate
observation
```

P3.2 registry fields:

```text
source_name
source_url
page_title
link_text
file_name
year
publication_period
downloaded_at
source_last_modified
http_etag
http_last_modified
file_size_bytes
sha256
storage_role
is_active_for_pipeline
supersedes_sha256
change_detected
notes
section_id
page_param
page_number
document_id
document_page_url
document_title
published_at
modified_at
as_of_date
file_url
absolute_file_url
file_title
file_info
file_size_text
discovery_method
pagination_page_count
```

Validation rules implemented in P3.2:

- `storage_role` must be one of the supported storage roles;
- `publication_period` must be `monthly`, `annual-final`, `manual-import`, or `unknown`;
- `discovery_method` must be `html`, `manual-import`, or `observation`;
- `sha256` must be a 64-character digest string;
- `file_size_bytes` must be non-negative;
- `discovery_method=html` requires HTML provenance fields such as `section_id`, `page_param`, `document_title`, and `absolute_file_url`;
- `manual-import` should include human-readable `notes`.

## P3.2 Registry Writer Contract Update

Дата обновления: 2026-06-17.

P3.2 добавляет offline registry writer layer без скачивания и без записи в настоящий `data/raw/minfin/ofz_auction_results/`.

Реализованные helper-функции:

- `RegistryRecord`;
- `RegistryStatus`;
- `compute_sha256(path)`;
- `get_file_size(path)`;
- `load_registry_csv(path)`;
- `load_registry_json(path)`;
- `write_registry_csv(path, records)`;
- `write_registry_json(path, records)`;
- `append_registry_record(path, record)`;
- `find_active_record(records, year, storage_role)`;
- `detect_hash_change(previous_record, candidate_sha256)`;
- `mark_superseded(records, superseded_sha256)`;
- `validate_registry_record(record)`.

P3.2 поддерживает HTML provenance поля:

- `section_id`;
- `page_param`;
- `page_number`;
- `document_id`;
- `document_page_url`;
- `document_title`;
- `published_at`;
- `modified_at`;
- `as_of_date`;
- `file_url`;
- `absolute_file_url`;
- `file_title`;
- `file_info`;
- `file_size_text`;
- `discovery_method`;
- `pagination_page_count`.

Допустимые `storage_role`:

- `latest`;
- `version_snapshot`;
- `final`;
- `manual_candidate`;
- `observation`.

P3.2 smoke test пишет CSV/JSON только во временную директорию и проверяет roundtrip, hash changed/unchanged, active row selection, superseded active row и validation failure. Настоящий raw storage не изменяется.
