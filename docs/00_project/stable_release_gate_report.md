# Stable release gate report

Дата: 2026-06-24.

## Scope

Выполнен `NEXT.4 Stable release/tag gate` после:

- `NEXT.1` screenshot backend validation outside sandbox;
- `NEXT.2` quality-full stable-release precheck;
- `NEXT.3` approved controlled Minfin latest/registry source update.

После отдельного явного разрешения пользователя выполнены `gh release create` и `gh release upload`.

## Preflight

Перед release gate:

- ordinary `git status --short --branch`: clean;
- latest commit on `main`: `a863bbdb108fdfb349e7c07d6ebfd8b654225f97`;
- CI for `Update controlled Minfin source latest registry`: completed success;
- existing remote tags were checked after `v0.1.0` push was rejected as already existing.

## Release bundle dry-run

Команда:

```powershell
.\.venv\Scripts\ofz-build-release-bundle.exe --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Результат:

```text
Release bundle target: releases\ofz_analytics_2026-05-01_month_cumulative_retrospective_4_20260624_165512
html_charts: 50 files
chart_data_csv: 61 files
dashboard_exports: 19 files
run_manifests: 4 files
qa_reports: 17 files
executive_summary: 3 files
data_quality_summary: 3 files
telemetry_summary: 4 files
Dry-run only: no files were written.
```

## Release bundle build

Команда:

```powershell
.\.venv\Scripts\ofz-build-release-bundle.exe --include-outputs --confirm BUILD_RELEASE_BUNDLE --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Результат:

```text
Release bundle created: releases\ofz_analytics_2026-05-01_month_cumulative_retrospective_4_20260624_165519
```

Bundle summary:

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

Release manifest:

- `releases/ofz_analytics_2026-05-01_month_cumulative_retrospective_4_20260624_165519/release_manifest.json`
- package version: `0.1.0`
- git commit hash: `a863bbdb108fdfb349e7c07d6ebfd8b654225f97`
- git branch: `main`
- git dirty flag: `false`
- latest Minfin SHA256 in bundle manifest: `3e748e88be0e5ff26171d6f36916949de83c50c918749e57454aeb1e73e3829b`

Release bundle is an ignored external artifact and is not committed.

## Git tag

Planned stable tag: `v0.1.0`.

Local `git tag -a v0.1.0 -m "Stable release v0.1.0"` created a local annotated tag.

`git push origin v0.1.0` returned:

```text
remote rejected: reference already exists
```

Remote tag inspection confirmed that `v0.1.0` already exists on GitHub and points to the same release commit:

```text
refs/tags/v0.1.0^{} -> a863bbdb108fdfb349e7c07d6ebfd8b654225f97
```

No force push and no tag move were performed.

## GitHub Release

После явного разрешения пользователя опубликован GitHub Release:

- tag: `v0.1.0`
- title: `Stable release v0.1.0`
- URL: `https://github.com/VinogradovPV/OFZ_ANALYTICS/releases/tag/v0.1.0`
- draft: `false`
- prerelease: `false`
- published at: `2026-06-24T14:29:05Z`

Release notes взяты из:

- `releases/ofz_analytics_2026-05-01_month_cumulative_retrospective_4_20260624_165519/release_manifest.md`

Загруженный asset:

- `ofz_analytics_2026-05-01_month_cumulative_retrospective_4_20260624_165519.zip`
- size: `73956359` bytes
- digest: `sha256:faa5f898317c6ec7ea4bb3e15f42ba1de48ff9077e5121330124420b0fb85711`
- asset URL: `https://github.com/VinogradovPV/OFZ_ANALYTICS/releases/download/v0.1.0/ofz_analytics_2026-05-01_month_cumulative_retrospective_4_20260624_165519.zip`

Во время первой попытки `gh release create` был создан неконсистентный draft без asset из-за timeout. Этот draft был удален без удаления или изменения tag `v0.1.0`, после чего release был создан заново и asset загружен отдельной командой.

## Generated artifacts policy

Not staged:

- `releases/`
- `outputs/`
- `data/processed/`
- `logs/`
- source acquisition reports;
- raw version snapshots.

## Decision

NEXT.4 release gate completed:

- release bundle dry-run;
- release bundle build;
- stable tag presence on GitHub;
- GitHub Release create/upload after separate explicit user approval.
