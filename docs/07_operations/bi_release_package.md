# BI release package

Дата актуализации: 2026-06-16.

BI release package - внешний артефакт для передачи результатов OFZ_ANALYTICS в BI-инструменты. Пакет собирается из уже созданных `outputs/` и не коммитится в Git.

## Назначение

BI package нужен, когда потребителю нужны не HTML-графики, а воспроизводимый набор CSV, словарей и manifest-файлов:

- dashboard exports;
- semantic model v2;
- analytical tables CSV;
- monthly metrics CSV;
- revenue analytics CSV;
- chart data CSV;
- data dictionary;
- KPI dictionary;
- period dimension;
- OFZ type dimension;
- placement format dimension.

## Команды

Dry-run:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Build:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --include-outputs --confirm BUILD_BI_PACKAGE --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Путь пакета

```text
releases/bi/ofz_analytics_bi_<report_date>_<period_type>_<aggregation_mode>_r<N>_<timestamp>/
```

`releases/` исключен из Git. BI package хранится как external artifact или передается потребителю отдельно.

## Состав

Пакет содержит:

- исходные CSV из `outputs/dashboards/`;
- `outputs/dashboards/semantic_model_v2/`;
- scoped CSV из `outputs/exports/analytical_csv/`;
- scoped chart data CSV из `outputs/exports/chart_data/`;
- generated BI dimensions в `dimensions/`;
- `README.md` для BI-потребителя;
- `bi_manifest.json`;
- `bi_manifest.md`.

## Правила безопасности

- Скрипт не создает пустые CSV вместо отсутствующих required datasets.
- В build mode отсутствие required datasets завершает команду с non-zero exit code.
- В dry-run mode скрипт только показывает, что будет включено и чего не хватает.
- Build mode требует `--include-outputs --confirm BUILD_BI_PACKAGE`.
- Generated BI package не должен попадать в Git.

## Manifest

`bi_manifest.json` фиксирует:

- имя и версию пакета;
- Git commit, branch и dirty flag;
- параметры отчета;
- timestamp генерации;
- Python version;
- CLI command;
- raw data file hashes;
- included files;
- generated helper tables;
- SHA256 checksums;
- missing required items.

## Ограничения

BI package не запускает pipeline и не пересоздает `outputs/`. Если required CSV отсутствуют, сначала нужно выполнить соответствующий pipeline run и quality checks.

