# Minfin source update decision report

Дата: 2026-06-24.

## Решение

Выполнен `NEXT.3 Operator decision по raw/latest/registry`.

Пользователь выбрал вариант A: approve source update.

Approved scope:

- `data/raw/minfin/ofz_auction_results/latest/INTERNET_Auction_Results_rus_2026_latest.xlsx`
- `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources.csv`
- `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources_latest.json`

Not approved / not staged:

- `data/raw/minfin/ofz_auction_results/versions/`
- `outputs/reports/source_acquisition/`
- generated outputs, processed data, logs, release artifacts.

## Проверка controlled files

Скрытые через `skip-worktree` файлы были раскрыты для review:

```powershell
git update-index --no-skip-worktree -- data/raw/minfin/ofz_auction_results/latest/INTERNET_Auction_Results_rus_2026_latest.xlsx
git update-index --no-skip-worktree -- data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources.csv
git update-index --no-skip-worktree -- data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources_latest.json
```

Фактический status controlled raw scope:

```text
 M data/raw/minfin/ofz_auction_results/latest/INTERNET_Auction_Results_rus_2026_latest.xlsx
 M data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources.csv
 M data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources_latest.json
```

## Latest XLSX

Approved latest file:

```text
INTERNET_Auction_Results_rus_2026_latest.xlsx
```

File metadata:

| Field | Value |
|---|---|
| SHA256 | `3e748e88be0e5ff26171d6f36916949de83c50c918749e57454aeb1e73e3829b` |
| Size bytes | `20131` |
| Last write time | `2026-06-23 10:59:21` local time |
| Source candidate | `INTERNET_Auction_Results_rus_2026_20260618.xlsx` |
| As-of date | `18.06.2026` |
| Published/modified | `19.06.2026` |

## Registry decision

Registry update changes:

- previous 2026 latest `INTERNET_Auction_Results_rus_2026_20260611.xlsx` is marked inactive and superseded;
- new 2026 latest `INTERNET_Auction_Results_rus_2026_20260618.xlsx` is active for pipeline;
- 2025 annual-final remains active as `final`;
- additional observation rows for unchanged 2026 latest checks remain inactive.

Programmatic registry check:

```text
latest_sha256 3e748e88be0e5ff26171d6f36916949de83c50c918749e57454aeb1e73e3829b
latest_size 20131
active_count 2
2025 final INTERNET_Auction_Results_rus_2025_20251231.xlsx cc4d89b113fca89cf12363c8a249b3902c7800a6cbef6e3d9729774fdc96f5b8
2026 latest INTERNET_Auction_Results_rus_2026_20260618.xlsx 3e748e88be0e5ff26171d6f36916949de83c50c918749e57454aeb1e73e3829b
```

## Remaining local state

The raw version snapshot remains physically present and excluded from ordinary status through local `.git/info/exclude`:

```text
data/raw/minfin/ofz_auction_results/versions/2026/INTERNET_Auction_Results_rus_2026_20260618_3e748e88be0e.xlsx
```

This is intentional. It is not staged and remains outside the approved commit scope.

## Checks

- `git status --short data/raw/minfin/ofz_auction_results` - reviewed.
- `git diff -- registry/minfin_ofz_auction_sources.csv` - reviewed.
- `git diff -- registry/minfin_ofz_auction_sources_latest.json` - reviewed.
- `Get-FileHash ... -Algorithm SHA256` - reviewed.
- Programmatic registry active-row/hash check - OK.

## Next step

After this operator decision, the next recommended stage is `NEXT.4 Stable release/tag gate`, but only after explicit user approval for release build, tag and GitHub release actions.
