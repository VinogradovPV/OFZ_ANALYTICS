# NEXT.13 - BI package handoff

Дата проверки: 2026-07-02

## Цель

Проверить, что workflow подготовки BI package после релиза v0.1.0 и strict registry plumbing понятен оператору и безопасен для dry-run режима.

Реальная сборка BI package не выполнялась, потому что она требует отдельного approval и может создать release/handoff artifacts.

## Preflight

Перед проверкой выполнен preflight из корня проекта:

```powershell
git status --short --branch
git log --oneline -5
```

Наблюдения:

- рабочая ветка: `main`;
- HEAD после NEXT.12: `d9b67ab Document monthly operation rehearsal after strict plumbing`;
- tracked-изменений перед NEXT.13 не было;
- в working tree оставались только локальные untracked prompt-файлы.

## Entry point

Проверка entry point:

- `.\.venv\Scripts\ofz-build-bi-package.exe` отсутствует;
- fallback script `scripts\maintenance\build_bi_package.py` существует и доступен.

Поэтому NEXT.13 выполнен через fallback-команду:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --help
```

Help подтвердил обязательные параметры report scope и безопасную модель запуска:

- `--dry-run` проверяет план без записи файлов;
- реальная сборка требует `--include-outputs`;
- реальная сборка также требует `--confirm BUILD_BI_PACKAGE`.

## Dry-run

Выполнена команда:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Результат: OK.

Dry-run target:

```text
releases\bi\ofz_analytics_bi_2026-05-01_month_cumulative_r4_20260702_081514
```

Проверенный состав пакета:

| Группа | Количество |
|---|---:|
| dashboard_exports | 13 files |
| semantic_model_v2 | 4 files |
| analytical_tables_csv | 9 files |
| monthly_metrics_csv | 1 file |
| revenue_analytics_csv | 5 files |
| chart_data_csv | 52 files |
| data_dictionary | 3 files |
| kpi_dictionary | 2 files |
| ofz_type_dimension | 2 rows |
| placement_format_dimension | 2 rows |
| period_dimension | 20 rows |
| bi_readme | 0 rows |

Команда завершилась сообщением:

```text
Dry-run only: no files were written.
```

## Решение по handoff

BI package workflow готов для операторского handoff на уровне dry-run проверки:

- состав пакета резолвится;
- semantic model v2 и dashboard exports находятся;
- analytical/monthly/revenue CSV находятся;
- chart data и dictionaries находятся;
- BI dimensions строятся;
- release directory в dry-run не создается;
- реальная сборка защищена явным confirm token.

## Что не выполнялось

Не выполнялись:

- `--include-outputs`;
- `--confirm BUILD_BI_PACKAGE`;
- создание release/handoff artifact;
- загрузка или публикация release asset;
- `git tag`;
- raw/source update;
- изменение source registry default.

Default source registry policy не менялась и остается:

```text
source-registry-mode=warn
allow-legacy-raw=true
```

## Следующий шаг только после approval

Если нужен фактический BI handoff artifact, оператор должен отдельно approve реальную сборку:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --include-outputs --confirm BUILD_BI_PACKAGE --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Созданные BI artifacts должны оставаться вне Git staging.
