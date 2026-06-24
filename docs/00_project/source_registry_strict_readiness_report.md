# Source registry strict-readiness report

Дата: 2026-06-24.

Статус: assessment-only. Live network, Minfin download, manual import, raw mutation и release actions не выполнялись.

## Цель

Оценить, готов ли controlled Minfin source registry к строгому режиму проверки (`--source-registry-mode strict`) без поломки legacy pipeline compatibility.

## Проверенный registry

Registry files:

- `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources.csv`
- `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources_latest.json`

Controlled storage:

- `data/raw/minfin/ofz_auction_results/latest/INTERNET_Auction_Results_rus_2026_latest.xlsx`
- `data/raw/minfin/ofz_auction_results/final/INTERNET_Auction_Results_rus_2025_final.xlsx`
- `data/raw/minfin/ofz_auction_results/versions/2026/`

## Фактический registry status

- Registry rows: `4`.
- Active rows: `2`.
- Active `final`: year `2025`, storage_role `final`, file exists, size matches, SHA-256 matches.
- Active `latest`: year `2026`, storage_role `latest`, file exists, size matches, SHA-256 matches.
- Superseded row: `2026 latest` for `2026-06-11`, inactive.
- Observation row: `2026 monthly` for unchanged `2026-06-18`, inactive.
- Duplicate active rows: not found.
- Missing active files: not found.
- Hash mismatch: not found.
- Size mismatch: not found.

Validation helper results:

| Mode | Result | Legacy fallback | Errors | Warnings |
| --- | --- | ---: | ---: | ---: |
| `off` | OK | yes | 0 | 1 (`source registry validation disabled`) |
| `warn` | OK | yes | 0 | 0 |
| `strict` | OK | no | 0 | 0 |

Data audit mode checks:

- `scripts/01_data_audit.py --source-registry-mode off` - OK.
- `scripts/01_data_audit.py --source-registry-mode warn --allow-legacy-raw` - OK.
- `scripts/01_data_audit.py --source-registry-mode strict` - OK.

## Checks

- `.\.venv\Scripts\python.exe scripts\qa\minfin_data_audit_registry_smoke.py` - OK.
- `.\.venv\Scripts\python.exe scripts\qa\minfin_source_acquisition_tests.py` - OK.
- direct registry validation helper check for `off|warn|strict` - OK.
- active file hash/size verification - OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts` - OK.

## Можно ли переводить default с `warn` на `strict`

Не сейчас.

Причины:

1. P3.6 intentionally left controlled source integration as validation-only. Cleaning/pipeline input selection still uses legacy raw files.
2. Default `warn + allow-legacy-raw` is still the compatibility contract in active docs and CLI behavior.
3. Working tree currently contains local raw/latest/registry modifications and an untracked new version snapshot. These files need an explicit operator decision before strict-by-default can become release policy.
4. `versions/` policy is inconsistent with repository history: current Post-P3 policy says `versions/` is not committed, but one older `versions/2026/...20260611...xlsx` is already tracked. This needs a separate artifact-policy decision; do not add more versions snapshots by default.

## Что мешает strict-by-default release-candidate

- Decide whether the current modified controlled files should be committed:
  - `data/raw/minfin/ofz_auction_results/latest/INTERNET_Auction_Results_rus_2026_latest.xlsx`
  - `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources.csv`
  - `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources_latest.json`
- Decide what to do with the untracked snapshot:
  - `data/raw/minfin/ofz_auction_results/versions/2026/INTERNET_Auction_Results_rus_2026_20260618_3e748e88be0e.xlsx`
- Resolve the existing tracked `versions/2026/...20260611...xlsx` versus the current "versions are not committed" policy.
- Decide whether data audit strict mode should become a release gate only, or a default local mode.
- Document whether legacy root raw files remain canonical pipeline inputs until a separate controlled-source ingestion migration.

## Что можно коммитить после operator review

If the 2026 monthly source update is accepted:

- `data/raw/minfin/ofz_auction_results/latest/INTERNET_Auction_Results_rus_2026_latest.xlsx`
- `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources.csv`
- `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources_latest.json`

Only commit these after reviewing the live acquisition report/registry diff and confirming the update is intended.

## Что нельзя коммитить по текущей policy

- `data/raw/minfin/ofz_auction_results/versions/2026/INTERNET_Auction_Results_rus_2026_20260618_3e748e88be0e.xlsx`
- `outputs/reports/source_acquisition/`
- `outputs/charts/`
- `outputs/exports/`
- `outputs/reports/`
- `outputs/dashboards/`
- `outputs/archive/`
- `data/processed/`
- `.ofz_launcher/`
- `logs/`
- `releases/`

## Рекомендация

- Keep default as `source-registry-mode=warn` and `allow-legacy-raw=true` for now.
- Use `strict` as a pre-release validation check while controlled source migration remains validation-only.
- Do not stage `versions/` snapshots until artifact policy is explicitly reconciled with the already tracked old snapshot.
- Treat POSTP3.4/POSTP3.7 as the right places to decide whether current controlled raw/registry changes should become part of the next release-candidate.
