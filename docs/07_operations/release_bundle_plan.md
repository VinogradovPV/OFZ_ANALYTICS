# Release bundle plan

Дата актуализации: 2026-06-09.

## Назначение

Release bundle - внешний пакет артефактов конкретного отчетного запуска OFZ_ANALYTICS. Он нужен потому, что generated outputs не входят в обычную Git-историю: HTML-графики, chart data CSV, dashboard exports и отчеты качества хранятся как release/external artifacts.

## Команда

Dry-run:

```powershell
.\.venv\Scripts\ofz-build-release-bundle.exe --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Создание bundle:

```powershell
.\.venv\Scripts\ofz-build-release-bundle.exe --include-outputs --confirm BUILD_RELEASE_BUNDLE --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Fallback через Python:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_release_bundle.py --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Путь пакета

По умолчанию пакет создается в:

```text
releases/ofz_analytics_<report_date>_<period_type>_<aggregation_mode>_retrospective_<N>_<timestamp>/
```

`releases/` исключен из Git. Пакет можно передавать как внешний artifact, GitHub Release asset или локальный audit bundle.

## Состав

Bundle включает:

- HTML charts из `outputs/charts/`;
- chart data CSV/JSON/XLSX из `outputs/exports/`;
- dashboard exports из `outputs/dashboards/`;
- run manifests из `outputs/reports/`;
- QA reports из `outputs/reports/` и `docs/06_quality/`;
- executive summary из `outputs/reports/` и `docs/03_analytics/`;
- data quality summary, если создан;
- telemetry summary, если создан;
- `release_manifest.json`;
- `release_manifest.md`.

## Release manifest

Manifest фиксирует:

- package name и version;
- Git commit hash;
- branch;
- dirty flag;
- параметры отчета: `report_date`, `period_type`, `aggregation_mode`, `retrospective_years`;
- timestamp генерации;
- Python version;
- CLI command;
- raw data file hashes;
- список включенных файлов;
- размеры файлов;
- SHA256 checksums;
- quality gate status;
- schema validation status;
- visual regression mode;
- warning summary.

## Missing outputs policy

Если required outputs отсутствуют:

- dry-run выводит список missing categories и завершается без записи файлов;
- release mode завершается non-zero;
- скрипт не создает фиктивные файлы и не подменяет отсутствующие outputs пустыми заглушками.

Required categories:

- `html_charts`;
- `chart_data_csv`;
- `dashboard_exports`;
- `run_manifests`;
- `qa_reports`;
- `executive_summary`.

Optional categories:

- `data_quality_summary`;
- `telemetry_summary`.

## Safety policy

Реальное создание bundle требует оба флага:

```powershell
--include-outputs --confirm BUILD_RELEASE_BUNDLE
```

Это защищает от случайного копирования тяжелых generated outputs. Перед release bundle рекомендуется выполнить:

```powershell
ofz-quality --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Для внешнего release дополнительно выполнить full quality gate.
