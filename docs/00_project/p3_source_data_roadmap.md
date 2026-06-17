# P3 roadmap source data

Дата актуализации: 2026-06-16.

## Status

P3.0 Source acquisition design is allowed because:

- P3.PRE.1 scripts balance/problem audit is completed.
- P3.PRE.2 docs encoding audit and UTF-8 normalization is completed.

This step creates design documentation only. Downloader code is intentionally deferred.

## Цель

Design controlled acquisition of Minfin OFZ auction Excel source files before data audit.

Required policy:

```text
Variant C - hybrid latest + final + version snapshots on hash change
```

## Результаты

Created in P3.0:

- `docs/02_data_contracts/minfin_source_registry_contract.md`
- `docs/07_operations/minfin_source_acquisition.md`
- `docs/00_project/p3_source_data_roadmap.md`

## Источник

Source page:

```text
https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/#tablitsy_po_rezultatam_provedeniya_auktsionov
```

Fallback page URL without anchor:

```text
https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction
```

Expected section:

```text
Результаты проведенных аукционов по размещению государственных ценных бумаг в...
```

Expected files:

```text
INTERNET_Auction_Results_rus_<year>_....xlsx
```

## Целевое хранилище

```text
data/raw/minfin/ofz_auction_results/
  latest/
  versions/
  final/
  registry/
```

Git policy:

- Track `latest/`, `final/`, and `registry/`.
- Keep `versions/` external/ignored by default.
- Commit `versions/` only after a separate artifact policy decision.

## Roadmap

### P3.0 - Design

Status: current step.

Scope:

- document registry contract;
- document operation lifecycle;
- document storage and Git policy;
- document failure and manual fallback behavior;
- do not write downloader code.

Checks:

- docs-only diff review;
- staged generated artifacts check;
- no compileall or quality gate unless code changes beyond docs/helper scope.

### P3.1 - Source Acquisition Skeleton

Planned scope:

- create `scripts/source_acquisition/` package;
- add parser/discovery interfaces with no production download by default;
- add CLI skeleton for `ofz-fetch-minfin`;
- add dry-run output schema;
- add unit-level tests or smoke checks for argument parsing and path planning.

No raw file mutation unless an explicit download/import command is implemented and tested.

### P3.2 - Registry Writer

Planned scope:

- implement registry CSV/JSON writer;
- implement SHA-256 and file metadata capture;
- add idempotency behavior for unchanged hash;
- add controlled storage role calculation: `latest`, `version`, `final`, `manual_candidate`.

### P3.3 - Monthly Acquisition

Planned scope:

- implement page discovery and monthly download;
- write temporary files first;
- promote to `latest/` only after hash and filename validation;
- create `versions/` snapshot only on hash change;
- keep `versions/` external/ignored unless policy changes.

Future CLI:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --dry-run
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --download
```

### P3.4 - Annual Finalization

Planned scope:

- implement annual-final mode;
- promote prior-year reviewed file to `final/`;
- prevent automatic replacement of an existing final file with a different hash;
- document January operator checklist.

Future CLI:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2025 --mode annual-final --download
```

### P3.5 - Manual Fallback Import

Planned scope:

- support manual file path import;
- validate file naming and year;
- write `manual-import` registry rows;
- require review before final promotion.

### P3.6 - Pipeline Integration

Planned flow:

```text
source acquisition
  -> raw source registry
  -> raw data registry
  -> data audit
  -> cleaning
```

Integration should be incremental:

1. Existing `data/raw/INTERNET_Auction_Results_rus_*.xlsx` continues to work.
2. New controlled Minfin storage is introduced side by side.
3. Raw registry learns to report both legacy and controlled source locations.
4. Data audit consumes controlled active files after compatibility checks pass.
5. Cleaning remains behavior-stable until source selection is fully validated.

## Принципы обработки ошибок

If Minfin site is unavailable:

- do not mutate raw storage;
- do not update registry as successful acquisition;
- report failure with URL/year/mode;
- allow manual fallback import.

If file content changes:

- compare by SHA-256;
- preserve snapshot only on hash change;
- never replace annual final automatically.

If page markup changes:

- fail parser with clear diagnostics;
- do not guess link selection;
- require parser update or manual import.

## Открытые решения для следующих P3-этапов

- Exact registry file format: CSV only, JSON latest, or both.
- Whether `versions/` remains fully external or selected snapshots become tracked release/audit artifacts.
- Whether current legacy raw files are migrated, copied, or retained as compatibility fixtures.
- Whether future CI runs source acquisition in dry-run only or uses committed raw fixtures.
