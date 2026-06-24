# Stable release precheck report

Дата: 2026-06-24.

## Scope

Выполнен `NEXT.2 quality-full stable-release precheck`.

Цель: проверить проект на уровне stable release без release build, git tag, GitHub release, live Minfin download/import/replacement и без commit raw/source update.

Параметры проверки:

```powershell
--report-date 2026-05-01
--retrospective-years 4
--period-type month
--aggregation-mode cumulative
```

## Preconditions

- `NEXT.0` выполнен: post-cleanup baseline и скрытое локальное состояние задокументированы.
- `NEXT.1` выполнен: screenshot backend outside sandbox был вручную проверен пользователем и дал `50` screenshot artifacts.
- Ordinary `git status` перед NEXT.2 был clean.
- Controlled raw/latest/registry update не approved и остается вне текущего commit scope.

## Commands and results

| Command | Result |
|---|---|
| `.\.venv\Scripts\python.exe -m pip install -e .` | OK |
| `.\.venv\Scripts\python.exe -m pip check` | OK, broken requirements not found |
| `.\.venv\Scripts\python.exe -m compileall -q scripts` | OK |
| `.\.venv\Scripts\python.exe scripts\qa\check_text_encoding.py` | OK, checked=271, problems=0 |
| `.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` | OK |
| `.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` | OK, 16 schema checks |
| `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` | OK |
| `.\.venv\Scripts\ofz-quality.exe --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` | OK |
| `.\.venv\Scripts\ofz-build-release-bundle.exe --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` | OK, dry-run only |

## Quality-full notes

`ofz-quality --full` passed. It includes expected anomaly warnings that do not fail the gate:

- missing yield rows: `18`;
- bid-to-cover outliers: `1`;
- demand-to-placement outliers: `1`;
- zero/absent demand rows: `35`;
- demand without placement rows: `7`;
- placement without demand rows: `33`;
- missing cutoff price rows: `7`.

These warnings are data-quality observations and should remain visible for operator review. They did not block the stable-release precheck.

`visual_regression.py` inside quality gate used the auto/fallback path in Codex context. This is acceptable for NEXT.2 because `NEXT.1` already validated screenshot backend outside sandbox and recorded the manual screenshot run in `docs/06_quality/visual_regression_report.md`.

## Generated artifacts

The precheck regenerated local outputs and reports. Notable generated artifacts:

- pipeline telemetry: `outputs/reports/telemetry/telemetry_20260624_132831_c38d46bf.json`;
- run manifest: `outputs/reports/run_manifest_20260624_162843_31810cc4.json`;
- quality-fast run id: `quality_gate_fast_month_cumulative_2026-05-01_r4_20260624_162944`;
- quality-full run id: `quality_gate_full_month_cumulative_2026-05-01_r4_20260624_163010`.

Release bundle dry-run target:

```text
releases\ofz_analytics_2026-05-01_month_cumulative_retrospective_4_20260624_163039
```

Dry-run summary:

| Category | Files |
|---|---:|
| HTML charts | 50 |
| chart data CSV | 61 |
| dashboard exports | 19 |
| run manifests | 4 |
| QA reports | 17 |
| executive summary | 3 |
| data quality summary | 3 |
| telemetry summary | 4 |

Dry-run did not write release files.

## Not performed

The following actions were intentionally not performed:

- stable release;
- git tag;
- GitHub release create/upload;
- release bundle build with `--include-outputs`;
- BI package build;
- live Minfin download/import/replacement;
- commit raw/source update.

## Decision

`NEXT.2 quality-full stable-release precheck` passed.

Remaining before stable release:

1. `NEXT.3` operator decision for hidden controlled raw/latest/registry state.
2. Explicit user approval for stable release gate, release build, tag and GitHub release.
3. Operator review/waiver for screenshot baselines, because current screenshot report records `missing_baseline` for the newly generated screenshots.
