# Production readiness report

Дата обновления: 2026-06-04.

## Статус P0 blocker

Production blocker `schema_validation / volume_bln_units` исправлен.

Baseline показывал падение `quality_gate.py --fast` только из-за отсутствия unit-колонок в двух chart data exports:

- `outputs/exports/chart_data/scatter/format_terms_aggregate_scatter_month_cumulative_2026-05-01_retrospective_4.csv`;
- `outputs/exports/chart_data/structure/format_discount_month_cumulative_2026-05-01_retrospective_4.csv`.

Исправление выполнено в генераторах, а не ручной правкой готовых CSV:

- `format_terms_aggregate_scatter_*` теперь получает `placement_volume_unit`, `revenue_volume_unit`, `nominal_revenue_gap_unit`;
- `format_discount_*` теперь получает `placement_volume_unit`, `revenue_volume_unit`, `nominal_revenue_gap_unit`, `total_nominal_volume_unit`.

## Data contract

Добавлен документ:

- `docs/02_data_contracts/chart_data_contract.md`.

Контракт фиксирует правило: все поля `*_volume_bln` в chart data exports измеряются в млрд рублей, а CSV с объемными показателями должен содержать unit-поля.

## Проверки

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py
.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Результат:

- `py_compile`: OK;
- пересборка `06_build_charts.py`: OK;
- `schema_validation.py`: OK, `Schema validation passed: 16`;
- `quality_gate.py --fast`: OK.

## Ограничения

- Исправление применено к генераторам двух семейств exports и к пересобранному кейсу `month/cumulative/2026-05-01/retrospective_4`.
- Старые CSV других параметров, созданные до исправления, могут требовать пересборки соответствующей командой, если они будут проверяться в production-контуре.
- `data/raw/` не изменялся.

## Artifact policy

Добавлен production artifact policy:

- `docs/00_project/artifact_policy.md`.

Документ разделяет файлы на категории:

- source code;
- configuration;
- stable documentation;
- generated reports;
- chart HTML;
- chart data CSV;
- dashboard exports;
- run manifests;
- logs;
- archive.

Для каждой категории зафиксированы правила git-хранения, пересоздания pipeline, release artifact, локального срока хранения и архивации.

Важно: `.gitignore` не создан и `git init` не выполнялся. Рекомендованный `.gitignore` сохранен только как текст в policy. `outputs/charts/**/*.html` и `outputs/exports/**/*.csv` не исключаются до отдельного решения release policy.
