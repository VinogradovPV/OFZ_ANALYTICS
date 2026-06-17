# Minfin source acquisition operation design

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
