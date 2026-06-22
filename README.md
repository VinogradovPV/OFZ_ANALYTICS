# OFZ_ANALITICS

Python-first pipeline для аналитики размещений ОФЗ. Проект готовит очищенные datasets, параметризуемый report scope, аналитические таблицы, интерактивные HTML-графики, monthly layer, dashboard-ready exports и executive summary.

Первая модернизация проекта завершена полностью. Текущие блоки `quality_gate.py`, `visual_regression.py`, `run_manifest.py`, `anomaly_tests.py`, `semantic_model_v2`, revenue analytics и revenue charts относятся ко второй модернизации и добавлены поверх уже стабилизированной базы.

Все команды ниже выполняются из корня проекта `OFZ_ANALITICS` через локальный Python:

```powershell
.\.venv\Scripts\python.exe
```

Абсолютные пути к Python в командах не используются.

## Назначение проекта

Проект позволяет:

- анализировать размещения ОФЗ по аукционам и ДРПА;
- сравнивать отчетный период с ретроспективой прошлых лет;
- формировать обязательные аналитические таблицы;
- строить интерактивные визуализации;
- объяснять накопленный итог через monthly layer;
- готовить BI-ready dashboard exports и semantic layer;
- проверять схему, воспроизводимость и качество графиков;
- аккуратно организовывать outputs без удаления исходных данных.

`data/raw/` используется только как источник чтения и не должен изменяться pipeline-скриптами.

## Структура проекта

```text
data/raw/                         исходные Excel/CSV
data/processed/                   очищенные и расчетные datasets
docs/                             проектная документация
logs/                             pipeline.log
outputs/charts/                   HTML-графики
outputs/reports/                  человекочитаемые отчеты
outputs/reports/analytical_tables/ обязательные XLSX-таблицы
outputs/reports/monthly_tables/   monthly XLSX-таблицы
outputs/exports/analytical_csv/   CSV-копии отчетных таблиц
outputs/exports/chart_data/       CSV-основы графиков
outputs/dashboards/               BI-ready exports
outputs/archive/                  архивные outputs
prompts/                          рабочие промпты проекта
scripts/                          Python-скрипты pipeline
```

## Требования к окружению

- Windows и PowerShell как оболочка запуска;
- Python в локальном `.venv`;
- зависимости из `requirements.txt`, если файл присутствует;
- запуск команд из корня проекта.

Проверить Python:

```powershell
.\.venv\Scripts\python.exe --version
```

Python version policy:

- package metadata supports Python `>=3.11,<3.15`;
- current production baseline was actually tested on Python `3.14.5`;
- source syntax was checked as Python 3.11-compatible;
- runtime dependency metadata requires Python `>=3.11` at the strictest point (`pandas`/`numpy`);
- if another Python version from the supported range is used, run `quality_gate.py --fast` before relying on outputs.

Установить зависимости:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Dev/QA dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Dependency check:

```powershell
.\.venv\Scripts\python.exe -m pip check
```

Editable install and CLI entry points:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\ofz-run.exe --help
.\.venv\Scripts\ofz-quality.exe --help
.\.venv\Scripts\ofz-schema.exe --help
.\.venv\Scripts\ofz-clean-outputs.exe --help
.\.venv\Scripts\ofz-build-release-bundle.exe --help
```

Existing script launch commands remain supported. `ofz-clean-outputs` is a safe maintenance entry point for generated `outputs/`: it defaults to dry-run and requires `--confirm DELETE_OUTPUTS` for deletion. `ofz-build-release-bundle` creates an external release bundle under ignored `releases/` and requires `--include-outputs --confirm BUILD_RELEASE_BUNDLE` outside dry-run.

Environment details are documented in [`docs/07_operations/environment.md`](docs/07_operations/environment.md).

Safe outputs cleanup:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --dry-run
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --delete-all --confirm DELETE_OUTPUTS
```

The cleanup command only works inside `outputs/`, preserves `outputs/archive/`, writes cleanup manifests, and recreates the tracked folder skeleton with `.gitkeep`.

Release bundle dry-run:

```powershell
.\.venv\Scripts\ofz-build-release-bundle.exe --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Release bundle creation:

```powershell
.\.venv\Scripts\ofz-build-release-bundle.exe --include-outputs --confirm BUILD_RELEASE_BUNDLE --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

BI release package dry-run:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

BI release package creation:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --include-outputs --confirm BUILD_BI_PACKAGE --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

BI package is an external artifact under ignored `releases/bi/`. It is documented in [`docs/07_operations/bi_release_package.md`](docs/07_operations/bi_release_package.md) and governed by [`docs/02_data_contracts/bi_exports_contract.md`](docs/02_data_contracts/bi_exports_contract.md).

The bundle is written to `releases/ofz_analytics_<report_date>_<period_type>_<aggregation_mode>_retrospective_<N>_<timestamp>/`, which is excluded from Git. The bundle includes generated HTML charts, chart data, dashboard exports, run manifests, QA reports and release manifests.

Pipeline telemetry:

```powershell
.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Each full pipeline run writes telemetry summaries to `outputs/reports/telemetry/telemetry_<run_id>.json` and `.md`. Telemetry records stage durations, artifact counts and sizes, cleanup mode, quality/schema status, Git commit/dirty flag and raw data hashes. These generated telemetry files are not committed and are included in release bundles when present.

Windows UI launcher MVP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Gui
```

The default launcher action is a safe smoke check. The GUI mode calls only approved CLI entry points, validates report parameters, writes logs to `outputs/reports/launcher/`, blocks delete cleanup without `DELETE_OUTPUTS`, and blocks release bundle creation without `BUILD_RELEASE_BUNDLE`. The GUI includes project root, report date, retrospective years, period type, aggregation mode, action, cleanup mode, release/cleanup confirmations, command preview and output/status fields.

Русскоязычная UX-инструкция по полям, сценариям, Preview, run-pipeline и логам: [`tools/windows_launcher/README.md`](tools/windows_launcher/README.md).

UI launchers do not replace the CLI or quality gate. The supported production interface remains the CLI (`ofz-run`, `ofz-quality`, `ofz-schema`, `ofz-clean-outputs`, `ofz-build-release-bundle`). The PowerShell launcher is the recommended Windows UI MVP for operators who need a guided local launcher.

Word VBA launcher source:

```text
tools/word_launcher/OfzLauncher.bas
tools/word_launcher/README.md
docs/07_operations/word_vba_launcher_spec.md
```

The `.bas` source can be committed. A future `.docm` file is a release artifact, not a source artifact, and must not be committed without a separate artifact policy decision. The VBA launcher calls only whitelisted CLI entry points and applies the same `DELETE_OUTPUTS` and `BUILD_RELEASE_BUNDLE` confirmation gates.

Word VBA is optional. Text source files (`.bas`, `.frm`) are source artifacts; `.docm` packages are release artifacts unless explicitly approved by artifact policy. Launcher logs under `outputs/reports/launcher/` are generated outputs and are excluded from Git. Release bundles remain external artifacts under ignored `releases/`.

Interactive cleanup pre-flight:

```powershell
.\.venv\Scripts\python.exe scripts\interactive_pipeline.py
```

Before running the selected pipeline command, the interactive launcher checks whether generated `outputs/` artifacts already exist. If they do, it offers to keep outputs, run cleanup dry-run, archive and clean outputs, clean without archive after explicit `DELETE_OUTPUTS_NO_ARCHIVE`, or cancel the run. The launcher never deletes files directly: it calls `scripts/maintenance/cleanup_outputs.py` and stops the pipeline if cleanup fails. The selected cleanup status is recorded in the run manifest for full interactive runs.

Интерактивная активация `.venv`, если нужна:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Параметры запуска

Основные параметры:

- `--report-date` — отчетная дата, всегда первое число месяца;
- `--period-type` — `month`, `quarter` или `year`;
- `--retrospective-years` — число лет ретроспективы;
- `--aggregation-mode` — `cumulative` или `point`;
- `--stage` — запуск одного этапа;
- `--stages` — запуск нескольких этапов;
- `--all` — полный запуск;
- `--safe` — safe reproduction mode для ранних этапов;
- `--compare` — сравнение outputs, если применимо;
- `--interactive` — интерактивный режим оркестратора.

### cumulative Рё point

`cumulative` используется по умолчанию.

- `month + cumulative + report_date=2026-05-01` означает январь-апрель 2026.
- `month + point + report_date=2026-05-01` означает только апрель 2026.
- `quarter + cumulative + report_date=2026-07-01` означает январь-июнь 2026.
- `quarter + point + report_date=2026-07-01` означает только II квартал 2026.
- `year + report_date=2026-01-01` означает завершенный 2025 год.

Ретроспектива сравнивает аналогичные интервалы прошлых лет. Outputs `cumulative` и `point` не смешиваются: режим агрегации входит в имена файлов.

## Быстрый запуск

Интерактивный launcher:

```powershell
.\.venv\Scripts\python.exe scripts\interactive_pipeline.py
```

Интерактивный launcher спрашивает `report_date`, `period_type`, `aggregation_mode`, `retrospective_years`, режим запуска и подтверждение перед выполнением. Доступные режимы:

Если в `outputs/` уже есть generated artifacts, launcher перед запуском показывает cleanup pre-flight menu. Default-действие: оставить outputs как есть. Архивация и очистка выполняются только через `scripts/maintenance/cleanup_outputs.py`; очистка без архива требует ввода `DELETE_OUTPUTS_NO_ARCHIVE`.

- `all` — полный pipeline;
- `stages` — ручной список stage numbers / stage names;
- `validate` — формирование report scope;
- `charts` — report scope и основные графики;
- `tables` — report scope и аналитические таблицы;
- `monthly` — monthly layer и помесячные графики;
- `dashboard` — dashboard exports и semantic model v2;
- `revenue` — таблицы и графики выручки;
- `quality` — quality gate в fast-режиме;
- `anomaly` — anomaly tests;
- `manifest` — run manifest;
- `semantic` — semantic model v2.

Полный месячный отчет накопленным итогом:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Полный месячный отчет за один месяц:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode point
```

Полный квартальный отчет:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-04-01 --retrospective-years 2 --period-type quarter --aggregation-mode cumulative
```

Полный годовой отчет:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-01-01 --retrospective-years 5 --period-type year --aggregation-mode cumulative
```

Запуск этапов 1-3:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --stages 1 2 3 --report-date 2026-04-01 --retrospective-years 2 --period-type quarter --aggregation-mode cumulative
```

## Порядок полного pipeline

При `--all` оркестратор запускает:

1. `scripts\01_data_audit.py` — аудит исходных данных.
2. `scripts\02_data_cleaning.py` — очистка данных.
3. `scripts\03_feature_engineering.py` — расчет признаков.
4. `scripts\period_filter.py` — report scope dataset.
5. `scripts\04_kpi_map.py` — карта KPI.
6. `scripts\05_visualization_strategy.py` — стратегия визуализаций.
7. `scripts\06_build_charts.py` — HTML-графики.
8. `scripts\08_analytical_tables.py` — обязательные аналитические таблицы.
9. `scripts\11_revenue_analytics.py` — таблицы выручки от реализации ОФЗ.
10. `scripts\12_build_revenue_charts.py` — графики выручки от реализации ОФЗ.
11. Документ dashboard architecture.
12. `scripts\07_dashboard_exports.py` — dashboard exports.
13. `scripts\build_semantic_model_v2.py` — semantic model v2 для dashboard.
14. `scripts\generate_executive_summary.py` — executive summary.
15. Self-review.
16. Final project summary.
17. Run manifest — автоматически после успешного `--all`.

Monthly layer и monthly charts доступны как отдельные этапы и входят в `--all`, если соответствующие скрипты присутствуют.

Дополнительные stage names / stage numbers второй модернизации:

| Номер | Stage name | Скрипт / действие | Как запускается |
|---|---|---|---|
| 13.1 | `run_manifest` | запись run manifest | отдельно через `--stage run_manifest`, после `--all` создается автоматически |
| 13.2 | `quality_gate` | `scripts\quality_gate.py` | отдельно через `--stage quality_gate`; из pipeline используется fast mode |
| 13.3 | `anomaly_tests` | `scripts\anomaly_tests.py` | отдельно через `--stage anomaly_tests` |
| 13.4 | `revenue_analytics` | `scripts\11_revenue_analytics.py` | входит в `--all`, можно запускать отдельно |
| 13.5 | `revenue_charts` | `scripts\12_build_revenue_charts.py` | входит в `--all`, можно запускать отдельно |
| 13.6 | `semantic_model_v2` | `scripts\build_semantic_model_v2.py` | входит в `--all`, можно запускать отдельно |

## Отдельные скрипты

Аудит исходных данных:

```powershell
.\.venv\Scripts\python.exe scripts\01_data_audit.py
```

Очистка:

```powershell
.\.venv\Scripts\python.exe scripts\02_data_cleaning.py
```

Feature engineering:

```powershell
.\.venv\Scripts\python.exe scripts\03_feature_engineering.py
```

Р’С‹Р±РѕСЂ report scope:

```powershell
.\.venv\Scripts\python.exe scripts\period_filter.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

KPI map:

```powershell
.\.venv\Scripts\python.exe scripts\04_kpi_map.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Графики:

```powershell
.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Аналитические таблицы:

```powershell
.\.venv\Scripts\python.exe scripts\08_analytical_tables.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Monthly analytics:

```powershell
.\.venv\Scripts\python.exe scripts\09_monthly_analytics.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Monthly charts:

```powershell
.\.venv\Scripts\python.exe scripts\10_build_monthly_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Revenue analytics:

```powershell
.\.venv\Scripts\python.exe scripts\11_revenue_analytics.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Revenue charts:

```powershell
.\.venv\Scripts\python.exe scripts\12_build_revenue_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Dashboard exports:

```powershell
.\.venv\Scripts\python.exe scripts\07_dashboard_exports.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Semantic model v2:

```powershell
.\.venv\Scripts\python.exe scripts\build_semantic_model_v2.py
```

Executive summary:

```powershell
.\.venv\Scripts\python.exe scripts\generate_executive_summary.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Raw data registry:

```powershell
.\.venv\Scripts\python.exe scripts\raw_data_registry.py
```

Run manifest через pipeline:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --stage run_manifest --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Quality gate через pipeline в fast-режиме:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --stage quality_gate --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Quality gate напрямую в full-режиме:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Visual regression / fallback HTML inspection:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Visual regression modes after P2.7:

```powershell
# Contract/static inspection only
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode fallback --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative

# Try Playwright screenshots, then fallback if unavailable
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode auto --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative

# Require screenshot backend
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode screenshot --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Playwright screenshot backend is a dev/QA dependency. Install it when screenshot mode is needed:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

In the Codex managed sandbox browser subprocesses can be blocked by Windows pipe permissions. If `--mode auto` records a sandbox warning, run `--mode screenshot` from the project PowerShell session. A local smoke file such as `playwright_smoke.png` is a generated artifact and must not be committed.

Anomaly tests:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --stage anomaly_tests
```

Anomaly tests напрямую:

```powershell
.\.venv\Scripts\python.exe scripts\anomaly_tests.py
```

Semantic model v2 через pipeline:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --stage semantic_model_v2
```

Run manifest напрямую:

```powershell
.\.venv\Scripts\python.exe scripts\run_manifest.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --stages all
```

## Выходные файлы

Основные результаты:

- `data/processed/ofz_auctions_clean.csv`;
- `data/processed/ofz_auctions_features.csv`;
- `data/processed/ofz_auctions_report_scope.csv`;
- `data/processed/ofz_monthly_metrics.csv`;
- `outputs/charts/**/*.html`;
- `outputs/reports/analytical_tables/*.xlsx`;
- `outputs/reports/monthly_tables/*.xlsx`;
- `outputs/reports/executive_summary_<...>.md`;
- `outputs/reports/run_manifest_<run_id>.json`;
- `outputs/reports/run_manifest_<run_id>.md`;
- `outputs/reports/quality_gate_report_<run_id>.md`;
- `outputs/reports/visual_regression/**/*.md`;
- `outputs/exports/analytical_csv/*.csv`;
- `outputs/exports/chart_data/**/*.csv`;
- `outputs/dashboards/**/*.csv`;
- `outputs/dashboards/**/*.json`;
- `outputs/dashboards/semantic_layer/*`;
- `outputs/dashboards/semantic_model_v2/*`.

Отчетные `.xlsx` не должны сохраняться напрямую в корень `outputs/exports/`.

Revenue outputs:

- `outputs/reports/analytical_tables/revenue_summary_<...>.xlsx`;
- `outputs/exports/analytical_csv/revenue_summary_<...>.csv`;
- `outputs/exports/analytical_csv/revenue_by_ofz_type_<...>.csv`;
- `outputs/exports/analytical_csv/revenue_by_maturity_<...>.csv`;
- `outputs/exports/analytical_csv/revenue_by_format_<...>.csv`;
- `outputs/exports/analytical_csv/revenue_monthly_<...>.csv`;
- `outputs/exports/chart_data/structure/revenue_*_<...>.csv`;
- `outputs/charts/revenue/**/*.html`;
- `outputs/charts/scatter/discount_revenue_gap/discount_vs_revenue_gap_<...>.html`.

## Визуализации

Ключевые графики:

- объем размещения ОФЗ по номиналу;
- спрос и предложение;
- покрытие предложения спросом;
- доходность по видам ОФЗ;
- структура по срокам;
- структура по форматам;
- risk quadrant;
- ретроспективный risk quadrant;
- boxplot доходности по видам ОФЗ;
- график отсечения спроса;
- Sankey-графики структуры размещений;
- monthly charts.
- revenue charts по выручке от реализации.

Для графиков с объемом размещения используется единый стандарт: объем размещения по номиналу, млрд рублей.

Revenue-графики также используют млрд рублей и строятся по таблицам Этапа 10:

- `revenue_vs_nominal_by_period`;
- `nominal_revenue_gap_by_period`;
- `revenue_to_nominal_ratio`;
- `monthly_revenue_vs_nominal`;
- `monthly_nominal_revenue_gap`;
- `revenue_gap_by_ofz_type`;
- `revenue_gap_by_maturity`;
- `discount_vs_revenue_gap`.

## Dashboard exports

### Базовая методология доходности

Базовые yield-графики, monthly metrics и dashboard summaries используют только сопоставимый cohort ОФЗ-ПД: числовая доходность и положительный объем размещения. Аукционы и ДРПА ОФЗ-ПД включаются; ОФЗ-ПК учитывается только в объемах и имеет `yield_exclusion_reason=ofz_pk_yield_not_applicable`; ОФЗ-ИН не смешивается с номинальной доходностью ОФЗ-ПД. Missing/non-applicable yield остается null, а exports содержат `yield_scope=ofz_pd_only` и `mixed_security_types`.

Dashboard-ready файлы сохраняются в `outputs/dashboards/`.

Основные datasets:

- `dashboard_auction_level_<...>.csv`;
- `dashboard_period_summary_<...>.csv`;
- `dashboard_kpi_summary_<...>.csv`;
- `dashboard_maturity_structure_<...>.csv`;
- `dashboard_yield_distribution_<...>.csv`;
- `dashboard_demand_supply_<...>.csv`;
- `dashboard_metadata_<...>.json`;
- `dashboard_data_dictionary_<...>.csv`;
- `dashboard_monthly_metrics_<...>.csv`;
- `dashboard_monthly_data_dictionary_<...>.csv`;
- semantic layer первого поколения в `outputs/dashboards/semantic_layer/`;
- semantic model v2 РІ `outputs/dashboards/semantic_model_v2/`.

Semantic model v2 включает:

- `field_dictionary.csv`;
- `kpi_dictionary.csv`;
- `measures.csv`;
- `model_manifest.json`.

## Проверки качества

Компиляция ключевых скриптов:

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\run_pipeline.py
.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py
.\.venv\Scripts\python.exe -m py_compile scripts\08_analytical_tables.py
.\.venv\Scripts\python.exe -m py_compile scripts\generate_executive_summary.py
```

Schema validation:

```powershell
.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Regression tests:

```powershell
.\.venv\Scripts\python.exe scripts\regression_tests.py
```

Smoke tests:

```powershell
.\.venv\Scripts\python.exe scripts\smoke_tests.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

HTML chart QA:

```powershell
.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Visual regression / fallback HTML inspection:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Anomaly tests:

```powershell
.\.venv\Scripts\python.exe scripts\anomaly_tests.py
```

Run manifest:

```powershell
.\.venv\Scripts\python.exe scripts\run_manifest.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --stages all
```

Quality gate:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Quality gate объединяет `py_compile`, `schema_validation.py`, `regression_tests.py`, `anomaly_tests.py`, `smoke_tests.py`, `html_chart_qa.py`, `visual_regression.py`, проверки README, outputs structure, run manifest и dashboard semantic model. Если часть проверок недоступна, результат фиксируется как warning, а остальные проверки продолжаются.

## Упорядочивание outputs

Dry-run:

```powershell
.\.venv\Scripts\ofz-clean-outputs.exe --dry-run
```

Production delete/archive modes описаны в `docs/07_operations/production_runbook.md`; destructive cleanup требует explicit confirmation token.

Legacy migration reports are archive/audit documents and are not part of the active production contract.

## Методологические правила

Формат размещения:

- `format` сохраняется как отдельная колонка;
- `format_assumption_flag` фиксирует уверенность классификации;
- ДРПА не должны механически включаться в demand-based ratios без ограничения.

Сроки обращения:

- `short_term` — до 5 лет включительно;
- `medium_term` — свыше 5 и до 10 лет включительно;
- `long_term` — более 10 лет;
- `requires_review` — срок нельзя надежно определить.

Показатели спроса и покрытия:

- `demand_satisfaction_ratio = placement_volume / demand_volume`;
- `demand_to_placement_ratio = demand_volume / placement_volume`;
- `bid_to_cover_ratio = demand_volume / supply_volume`.

`demand_to_placement_ratio` нельзя называть классическим bid-to-cover.

Показатели выручки:

- `placement_volume` — объем размещения по номиналу, млн рублей;
- `revenue_volume` — выручка от реализации, млн рублей; текущий source mapping использует `proceeds_mln_rub`, если канонический `revenue_volume` отсутствует;
- `nominal_revenue_gap = placement_volume - revenue_volume`;
- `revenue_to_nominal_ratio = revenue_volume / placement_volume`;
- `nominal_discount_ratio = nominal_revenue_gap / placement_volume`.

Если выручка отсутствует или заполнена неполно, проект не выдумывает значения: ограничение фиксируется через `data_quality_flag`, `docs/03_analytics/revenue_analytics_report.md` и `docs/01_methodology/revenue_kpi_map.md`.

Revenue analytics строится только при наличии надежной колонки выручки или сопоставимого source mapping. Если доступен только номинальный объем размещения, таблицы и графики выручки не должны подменять выручку номиналом.

`nominal_revenue_gap`, `revenue_to_nominal_ratio` и `nominal_discount_ratio` интерпретируются только в пределах строк с валидными `placement_volume` и `revenue_volume`.

## Частые проблемы

`run_pipeline.py` требует `--stage`, `--stages` или `--all`.

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Если report scope пуст, сначала выполните этап 4:

```powershell
.\.venv\Scripts\python.exe scripts\period_filter.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Если Excel-файл открыт, запись XLSX может завершиться `PermissionError`. Закройте файл или используйте fallback-файл, который создают скрипты.

Если `html_chart_qa.py` сообщает о старых графиках, пересоберите графики перед QA:

```powershell
.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Если outputs перепутаны после старых запусков, сначала выполните dry-run реорганизации:

```powershell
.\.venv\Scripts\ofz-clean-outputs.exe --dry-run
```

## Ограничения

- Инвентаризация файлов не заменяет runtime-проверку расчетов.
- Executive summary не формирует выводы без рассчитанных источников.
- При отсутствии `cutoff_price` анализ дисконта к номиналу ограничен.
- Группы boxplot с `n=1` не интерпретируются как распределение.
- Около-нулевые доходности ОФЗ-ПК требуют проверки качества данных.
- Неполные периоды должны документироваться в отчетах.
- Outputs режимов `cumulative` и `point` не должны смешиваться.
- `data/raw/` не изменяется pipeline-скриптами.

## Документация

Ключевые документы:

- `docs/00_project/project_inventory.md`;
- `docs/02_data_pipeline/data_audit.md`;
- `docs/02_data_pipeline/data_cleaning_report.md`;
- `docs/02_data_pipeline/feature_engineering.md`;
- `docs/01_methodology/period_selection_report.md`;
- `docs/01_methodology/kpi_map.md`;
- `docs/00_project/analytical_architecture.md`;
- `docs/04_visualization/visualization_strategy.md`;
- `docs/04_visualization/chart_build_limitations.md`;
- `docs/03_analytics/analytical_tables_report.md`;
- `docs/03_analytics/analytical_tables_limitations.md`;
- `docs/03_analytics/monthly_analytics_report.md`;
- `docs/04_visualization/monthly_visualization_strategy.md`;
- `docs/00_project/dashboard_architecture.md`;
- `docs/05_dashboard/dashboard_exports_report.md`;
- `docs/05_dashboard/dashboard_exports_limitations.md`;
- `docs/03_analytics/executive_summary_report.md`;
- `docs/06_quality/run_manifest_report.md`;
- `docs/06_quality/quality_gate_report.md`;
- `docs/06_quality/visual_regression_report.md`;
- `docs/06_quality/anomaly_tests_report.md`;
- `docs/05_dashboard/dashboard_semantic_model_v2.md`;
- `docs/03_analytics/revenue_analytics_report.md`;
- `docs/01_methodology/revenue_kpi_map.md`;
- `docs/02_data_pipeline/schema_validation_report.md`;
- `docs/00_project/self_review.md`;
- `docs/00_project/final_project_summary.md`;

## Структура документации, скриптов и графиков

Документация организована тематически. Главная карта находится в [`docs/index.md`](docs/index.md).

- [`docs/00_project/`](docs/00_project/) — проектная документация, архитектура, summary, планы структуры scripts.
- [`docs/01_methodology/`](docs/01_methodology/) — методология, KPI, правила периодов, revenue KPI.
- [`docs/02_data_pipeline/`](docs/02_data_pipeline/) — аудит, очистка, feature engineering, schema validation.
- [`docs/03_analytics/`](docs/03_analytics/) — аналитические таблицы, monthly analytics, revenue analytics, executive summary.
- [`docs/04_visualization/`](docs/04_visualization/) — стратегия визуализаций, ограничения графиков, palette policy.
- [`docs/05_dashboard/`](docs/05_dashboard/) — dashboard exports и semantic model.
- [`docs/06_quality/`](docs/06_quality/) — quality gate, visual regression, anomaly tests, manual checks, run manifest.
- [`docs/90_archive/`](docs/90_archive/) — архив промежуточных и устаревших документов.

Скрипты пока физически остаются в корне `scripts/`, но логически классифицированы. См.:

- [`scripts/README.md`](scripts/README.md);
- [`docs/00_project/scripts_structure_plan.md`](docs/00_project/scripts_structure_plan.md);
- [`docs/00_project/scripts_migration_plan.md`](docs/00_project/scripts_migration_plan.md).

HTML-графики организованы по тематическим подпапкам. Карта графиков находится в [`outputs/charts/index.md`](outputs/charts/index.md).

- [`outputs/charts/monthly/`](outputs/charts/monthly/) — помесячные графики.
- [`outputs/charts/monthly/heatmap/`](outputs/charts/monthly/heatmap/) — heatmap размещения и выручки, включая `monthly_heatmap_placement_*` и `monthly_heatmap_revenue_*`.
- [`outputs/charts/risk/`](outputs/charts/risk/) — risk quadrant и его версии.
- [`outputs/charts/scatter/`](outputs/charts/scatter/) — scatter-графики.
- [`outputs/charts/scatter/yield_discount/`](outputs/charts/scatter/yield_discount/) — семейство `yield_vs_discount`: main, facet и outliers.
- [`outputs/charts/scatter/format_terms/`](outputs/charts/scatter/format_terms/) — графики условий размещения по форматам: `format_terms_scatter_*` и `format_terms_aggregate_scatter_*`.
- [`outputs/charts/yield/`](outputs/charts/yield/) — yield boxplots.
- [`outputs/charts/sankey/`](outputs/charts/sankey/) — Sankey-графики.
- [`outputs/charts/structure/`](outputs/charts/structure/) — структурные графики.
- [`outputs/charts/structure/format/`](outputs/charts/structure/format/) — структура и условия по форматам: `format_structure_*`, `format_discount_*`, `format_terms_comparison_*`, `format_terms_delta_by_format_*`.
- [`outputs/charts/revenue/`](outputs/charts/revenue/) — revenue analytics.
- [`outputs/charts/revenue/gap/`](outputs/charts/revenue/gap/) — графики разницы номинал-выручка, включая `format_nominal_revenue_gap_*`.

### График `yield_vs_discount`

Семейство `yield_vs_discount` находится в `outputs/charts/scatter/yield_discount/` и показывает связь дисконта к номиналу и доходности. В основных версиях цвет соответствует году (`report_year`), размер точки соответствует объему размещения по номиналу, а сроковая категория доступна в hover. CSV-основы сохраняются в `outputs/exports/chart_data/scatter/`.

В семействе создаются три версии:

- `yield_vs_discount_<...>.html` — основной график по всем пригодным наблюдениям.
- `yield_vs_discount_facet_<...>.html` — сравнение по периодам/годам в отдельных панелях.
- `yield_vs_discount_outliers_<...>.html` — фокус на экстремальных точках по дисконту, доходности или объему размещения.

Подписи точек управляются полем `label_visible` в CSV export. Если `label_visible=True`, подпись выводится на график. Если `False`, наблюдение остается в hover и CSV, но подпись скрывается из-за лимита, плотности или отсутствия аналитической причины. Для main-графика лимит — 25 подписей, для outliers — 30, для facet — 15 всего и не более 3 на панель.

Медианные линии имеют разную методологию. В main/outliers они считаются по всей выборке графика (`median_scope=global`) и подписываются как `мед. дисконт` и `мед. доходность`. В facet-графике медианы считаются внутри каждой панели (`median_scope=period`), а пояснение вынесено в subtitle: пунктирные линии — медианы периода.

Размер точки означает объем размещения по номиналу. На графике есть пояснение размера и ориентиры `50 / 250 / 500 млрд руб.`, точное значение доступно в hover. Если период неполный после фильтрации валидных строк, CSV содержит `is_incomplete_period=True` и человекочитаемую причину, например `доступны данные только за янв–фев`.

Интерпретация квадрантов:

- высокий дисконт / высокая доходность — зона повышенной стоимости привлечения и ценового дисконта;
- высокий дисконт / низкая доходность — ценовой дисконт при умеренной доходности;
- низкий дисконт / высокая доходность — высокая доходность без выраженного ценового дисконта;
- низкий дисконт / низкая доходность — относительно спокойная зона.

Если размер точки плохо читается или перекрывает наблюдения, график может использовать fixed-size fallback. В этом случае размер маркера не интерпретируется как объем, но объем размещения по номиналу остается в hover и CSV.

### Правила читаемости графиков

- Monthly bar charts показывают подписи только для читаемых столбцов; малые значения остаются в hover.
- Monthly line charts подписывают ключевые точки: последние значения, максимумы, отчетный год и резкие изменения.
- Facet-графики должны иметь один общий Y-axis title; повторение подписи Y в каждой панели считается дефектом.
- Scatter-графики с bubble-size обязаны объяснять, что означает размер точки, либо явно использовать fixed-size fallback.
### Маршрутизация новых графиков условий и выручки

Новые HTML-графики сохраняются сразу в тематические подпапки `outputs/charts/`; при миграции старых файлов те же правила применяет `scripts/maintenance/reorganize_charts.py`.

- `format_discount_*` -> `outputs/charts/structure/format/`.
- `format_terms_comparison_*` -> `outputs/charts/structure/format/`.
- `format_terms_delta_by_format_*` -> `outputs/charts/structure/format/`.
- `format_nominal_revenue_gap_*` -> `outputs/charts/revenue/gap/`.
- `monthly_heatmap_revenue_*` -> `outputs/charts/monthly/heatmap/`.
- `format_terms_scatter_*` Рё `format_terms_aggregate_scatter_*` -> `outputs/charts/scatter/format_terms/`.
## Графики по форматам, дисконту и выручке

В актуальной структуре графики по форматам размещения находятся в тематических папках `outputs/charts/structure/format/`, `outputs/charts/revenue/gap/`, `outputs/charts/monthly/heatmap/` и `outputs/charts/scatter/format_terms/`.

Ключевые графики:

- `format_structure_<...>.html` - stacked bar структуры размещения по форматам `Аукцион` / `ДРПА`. Высота сегмента равна объему размещения по номиналу в млрд рублей. Над столбцами с двумя и более сегментами выводится итоговая сумма, а подписи сегментов управляются полем `label_visible`.
- `format_discount_<...>.html` - средневзвешенный дисконт к номиналу по форматам. Ось Y: `Средневзвешенный дисконт к номиналу, п.п.`. Номинальный объем, выручка, min/max дисконт и качество данных доступны в hover и CSV.
- `format_nominal_revenue_gap_<...>.html` - денежная разница между номинальным размещением и выручкой по форматам: `nominal_revenue_gap_bln = placement_volume_bln - revenue_volume_bln`.
- `monthly_heatmap_revenue_<...>.html` - heatmap помесячной выручки с колонкой `Итого`. Итоговая колонка справочная и не участвует в основной цветовой шкале.
- `format_terms_comparison_<...>.html` - small multiples для сравнения форматов по доходности, дисконту, выручке / номиналу и разнице номинал минус выручка. `n` означает количество размещений соответствующего формата в периоде.
- `format_terms_scatter_<...>.html` - scatter отдельных размещений: цвет = формат, форма = вид ОФЗ, размер = объем размещения по номиналу.

Ограничения:

- если выручка отсутствует, проект не подставляет синтетические значения из номинала или спроса;
- если дисконт отсутствует и его нельзя надежно получить из цены отсечения, строка исключается из расчета дисконта или помечается через `data_quality_flag`;
- показатели по ДРПА при малом `n` нужно интерпретировать осторожно.

## Dataset data/raw и политика Git

`data/raw/` contains the baseline source dataset for the project. These raw Excel files are intentionally included in the repository because the current files are small and are required to reproduce the pipeline from source data.

For the first Git commit, `data/raw/` is committed as the source dataset. Generated outputs are not committed to normal Git history and are recreated by the pipeline or preserved separately as release artifacts.

Generated outputs are not part of the normal Git history:

- `outputs/charts/`;
- `outputs/exports/`;
- `outputs/reports/`;
- `outputs/dashboards/`.

For a specific reporting run, generated outputs should be preserved as a release bundle or external artifact together with the run manifest and quality reports.

## Version Control

- Repository: GitHub / `OFZ_ANALYTICS`
- Remote: `https://github.com/VinogradovPV/OFZ_ANALYTICS.git`
- Default branch: `main`
- Visibility: private
- Initial commit: `4fa6d61fa67281c20d5d7a878cd2191e953507bc`
- Initial commit message: `Initial source dataset and OFZ analytics pipeline`

Git artifact strategy:

- the first commit includes source code, configuration, documentation, scripts, prompts, data contracts and `data/raw`;
- generated outputs are excluded from ordinary Git history;
- `outputs/charts/`, `outputs/exports/`, `outputs/reports/` and `outputs/dashboards/` are regenerated by the pipeline;
- release outputs should be stored as a release bundle, external artifact or GitHub Release asset when that release process is configured;
- the empty outputs folder skeleton is kept in Git via `.gitkeep` and lightweight navigation files such as `outputs/charts/index.md`.

Data strategy:

- `data/raw` is committed as the project source dataset;
- raw file hashes are tracked by raw data registry and/or run manifest;
- generated data such as `data/processed` is not committed and is recreated by pipeline stages.
## Production operations

Production-запуск описан в:

- `docs/07_operations/production_runbook.md` — пошаговый runbook для clone, `.venv`, CLI, pipeline, cleanup outputs, QA, release bundle и Git workflow.
- `docs/07_operations/stable_release_procedure.md` — stable release procedure с source acquisition dry-run/update, registry review, quality gates, release bundle, tag и правилом `gh release` только по отдельному разрешению.
- `docs/07_operations/release_checklist.md` — контрольный checklist перед production release.
- `docs/07_operations/minfin_monthly_update_procedure.md` — русскоязычная инструкция для ежемесячного обновления источника Минфина, январского annual-final и manual fallback.
- `docs/07_operations/windows_setup.md` — reproducible Windows setup workflow for a new machine.
- `docs/07_operations/docker_plan.md` — optional Docker plan; Windows-first remains the primary supported path.

Minfin source acquisition uses the CLI entry point:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --help
```

Monthly download requires `--confirm DOWNLOAD_MINFIN_SOURCE`, annual final replacement requires `--confirm REPLACE_MINFIN_FINAL`, and manual fallback requires `--confirm IMPORT_MINFIN_FILE`. Generated acquisition reports under `outputs/reports/source_acquisition/` and version snapshots under `data/raw/minfin/ofz_auction_results/versions/` are not committed.

Windows setup dry-run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/setup/setup_windows.ps1 -DryRun
```

Актуальные CLI entry points:

```powershell
ofz-run --help
ofz-interactive --help
ofz-quality --help
ofz-clean-outputs --help
ofz-schema --help
```

Если `.venv` не активирована, используйте явные executables из `.venv\Scripts`, например `.\.venv\Scripts\ofz-quality.exe --help`.

Generated outputs не входят в обычную Git-историю. Для конкретного отчетного запуска они сохраняются как release bundle / external artifact.

## CI / GitHub Actions

GitHub Actions workflow `.github/workflows/quality.yml` запускает `quality-fast` на `push`/`pull_request` в `main` и вручную через `workflow_dispatch`.

CI выполняет `pip install`, editable install, `pip check`, `compileall`, `ofz-schema` и `ofz-quality --fast`. Manual `quality-full` job доступен только через `workflow_dispatch` и зависит от `quality-fast`, чтобы fast/full не выполнялись параллельно в одном workflow.

QA reports сохраняются как GitHub Actions artifacts. Generated outputs и `releases/` не коммитятся. Подробный контракт: [`docs/07_operations/ci_workflow.md`](docs/07_operations/ci_workflow.md).

## Ограничения

Ограничения production-запуска, визуализаций и release artifacts описаны в `docs/07_operations/release_checklist.md`, `docs/07_operations/production_runbook.md` и `docs/04_visualization/chart_build_limitations.md`.
