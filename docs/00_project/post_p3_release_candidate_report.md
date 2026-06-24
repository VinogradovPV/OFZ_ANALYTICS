# POSTP3.7 - Release-candidate gate

Дата: 2026-06-24.

## Статус

POSTP3.7 выполнен как release-candidate gate для текущего состояния после P3/Post-P3.

Автоматизированный gate прошел: install, dependency check, compileall, UTF-8/mojibake scanner, pipeline, schema, quality-fast, release bundle dry-run, GUI smoke, Minfin dry-run и OFZ-PD yield regression завершились успешно.

Stable release/tag/GitHub release пока не выполнялись. Перед stable release остаются два осознанных operator decision:

1. Запустить screenshot backend из обычного project PowerShell, потому что Codex managed environment блокирует browser screenshot backend.
2. Разобрать локальные raw/generated изменения в рабочем дереве: что является operator-approved source update, а что остается generated/local и не staging scope.

## Проверенные параметры

```powershell
--report-date 2026-05-01
--retrospective-years 4
--period-type month
--aggregation-mode cumulative
```

## Выполненные проверки

| Проверка | Результат |
|---|---|
| `.\.venv\Scripts\python.exe -m pip install -e .` | OK |
| `.\.venv\Scripts\python.exe -m pip check` | OK, broken requirements нет |
| `.\.venv\Scripts\python.exe -m compileall -q scripts` | OK |
| `.\.venv\Scripts\python.exe scripts\qa\check_text_encoding.py` | OK, checked=262, problems=0 |
| `.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` | OK |
| `.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` | OK, 16 checks |
| `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` | OK |
| `.\.venv\Scripts\ofz-build-release-bundle.exe --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` | OK, dry-run only |
| `.\.venv\Scripts\ofz-gui.exe --smoke` | OK, 29 actions |
| `.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --dry-run --timeout-seconds 20 --retries 1` | OK, selected `INTERNET_Auction_Results_rus_2026_20260618.xlsx`; raw unchanged |
| `.\.venv\Scripts\python.exe scripts\qa\ofz_pd_yield_metrics_regression.py` | OK |
| `.\.venv\Scripts\python.exe scripts\visual_regression.py --mode screenshot --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` | FAIL only for screenshot backend availability in Codex managed environment; static checks still ran |

## Pipeline artifacts observed

Fresh run wrote generated telemetry and run manifest:

- telemetry: `outputs/reports/telemetry/telemetry_20260624_082444_3cdd899a.json`;
- run manifest: `outputs/reports/run_manifest_20260624_112457_ab56d871.json`.

These are generated outputs and are not committed.

Release bundle dry-run target:

```text
releases\ofz_analytics_2026-05-01_month_cumulative_retrospective_4_20260624_112517
```

Dry-run summary:

| Category | Files |
|---|---:|
| HTML charts | 100 |
| chart data CSV | 122 |
| dashboard exports | 34 |
| run manifests | 8 |
| QA reports | 26 |
| executive summary | 4 |
| data quality summary | 3 |
| telemetry summary | 8 |

Dry-run did not write release files.

## Yield scope spot check

`scripts\qa\ofz_pd_yield_metrics_regression.py` passed.

For the current RC run (`2026-05-01`, cumulative month), `data/processed/ofz_monthly_metrics.csv` contains only the report-scope months through `2026-M01-M04`; November 2025 is not in the current RC scope. The known November 2025 regression is covered by the dedicated OFZ-PD yield regression and prior manual log:

- `yield_weighted_avg` around `14.87`;
- `yield_min` around `14.73`;
- `yield_max` around `14.95`;
- OFZ-PK placement volume remains in volume breakdown and is excluded from yield numerator/denominator.

Current RC monthly metrics preserve:

- `yield_scope=ofz_pd_only`;
- OFZ-PD yield labels in generated yield charts;
- OFZ-PK/OFZ-IN exclusion from base yield denominator.

## Minfin source acquisition gate

Live dry-run completed without raw mutation.

Selected monthly candidate:

```text
INTERNET_Auction_Results_rus_2026_20260618.xlsx
```

Confirmed parser/provenance fields:

- section id: `66`;
- pagination param: `page_66`;
- page count: `4`;
- absolute file URL resolved under `https://minfin.gov.ru`;
- `as_of_date`: `18.06.2026`;
- `published_at` / `modified_at`: `19.06.2026`.

No live download, manual import, final replacement or raw promotion was executed.

## Screenshot backend status

`visual_regression --mode screenshot` could not complete browser screenshots from the Codex managed environment:

```text
browser screenshot backend skipped in Codex managed sandbox; run the same command from project PowerShell to use Playwright
```

Static visual checks still executed and quality-fast passed via auto fallback. This is acceptable as documented limitation for the gate, but stable release should include a manual outside-Codex screenshot run:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode screenshot --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Git / artifact status

Before POSTP3.7 the working tree already contained local raw/generated/report changes from prior pipeline/source-acquisition activity. POSTP3.7 did not stage them.

Must remain outside the release-candidate commit unless separately reviewed:

- `outputs/`;
- `outputs/reports/visual_regression/`;
- `outputs/reports/source_acquisition/`;
- `data/processed/`;
- `logs/`;
- `releases/`;
- `.ofz_launcher/`;
- `data/raw/minfin/ofz_auction_results/versions/`;
- local raw/latest/registry updates unless operator explicitly approves them as source update.

## Dangerous actions not performed

- Live Minfin download with `DOWNLOAD_MINFIN_SOURCE`;
- annual-final replacement with `REPLACE_MINFIN_FINAL`;
- manual import with `IMPORT_MINFIN_FILE`;
- delete outputs with `DELETE_OUTPUTS`;
- release bundle build with `BUILD_RELEASE_BUNDLE`;
- BI package build with `BUILD_BI_PACKAGE`;
- git tag;
- `gh release create` / upload.

## Release-candidate decision

Automated release-candidate gate: **passed**.

Stable release/tag decision: **deferred** until:

1. screenshot backend is run from normal project PowerShell or explicitly waived;
2. local raw/generated working tree state is reviewed;
3. `quality-full` is run if the target is stable release rather than release-candidate readiness;
4. user explicitly authorizes tag/release actions.

## Recommended next step

Run the screenshot command from normal Windows PowerShell, then decide whether to:

- proceed to stable release/tag gate;
- perform telemetry hardening from POSTP3.5;
- start the chart foundation refactor from POSTP3.6.
