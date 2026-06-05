# Baseline audit второй модернизации

Дата проверки: `2026-05-25`.

Документ фиксирует текущее состояние проекта после завершенной первой модернизации и перед началом второй модернизации. Проверка выполнена как короткий контрактный аудит по коду и структуре папок. Рабочие модули не переписывались, `data/raw/` не изменялся.

## Метод проверки

- Проверено наличие ключевых scripts.
- Проверены CLI-контракты и маршрутизация основных этапов по исходному коду.
- Проверена структура `outputs/`.
- Проверено, что новые outputs не лежат файлами напрямую в корне `outputs/exports/`.
- Runtime-запуски и `py_compile` в рамках baseline-аудита не выполнялись.

## Проверка ключевых модулей

| Модуль | Статус | Что подтверждено | Замечания для второй модернизации |
| --- | --- | --- | --- |
| `scripts/run_pipeline.py` | ok | Есть `--stage`, `--stages`, `--all`, `--safe`, `--compare`, `--interactive`, `--report-date`, `--retrospective-years`, `--period-type`, `--aggregation-mode`. В `ALL_STAGES` включены базовые этапы, monthly analytics, monthly charts, dashboard exports, executive summary, self-review и final summary. | Quality gate, run manifest, anomaly tests, visual regression, revenue analytics пока не интегрированы как отдельные этапы второй модернизации. |
| `scripts/06_build_charts.py` | ok | Использует `report_scope`, фильтрует по `period_type` и `aggregation_mode`, сохраняет HTML в `outputs/charts/`, chart data в профильные подпапки `outputs/exports/chart_data/`. Есть volume policy через `placement_volume_bln`, scatter policy, Sankey, risk charts, yield boxplot short/long mode. | Требуются точечные доработки второй модернизации: discount vs demand, отдельный boxplot ОФЗ-ПД, revenue charts. |
| `scripts/10_build_monthly_charts.py` | ok | Использует `data/processed/ofz_monthly_metrics.csv`, принимает `--aggregation-mode`, строит 8 monthly-графиков, переводит объемы в млрд рублей, пишет HTML в `outputs/charts/`. | Monthly bid-to-cover требует доработки подписей и расширения chart data. |
| `scripts/08_analytical_tables.py` | ok | Использует `report_scope`, фильтрует по `aggregation_mode`, пишет XLSX в `outputs/reports/analytical_tables/` или `outputs/reports/monthly_tables/`, CSV в `outputs/exports/analytical_csv/`. Есть сортировка по периоду и сроковым категориям. | Revenue analytical tables пока не добавлены. |
| `scripts/07_dashboard_exports.py` | ok | Создает dashboard exports в `outputs/dashboards/`, monthly dashboard exports в `outputs/dashboards/monthly/`, semantic layer в `outputs/dashboards/semantic_layer/`. Есть словари, metadata и semantic layer первого поколения. | Нужен semantic model v2 в `outputs/dashboards/semantic_model_v2/`. |
| `scripts/html_chart_qa.py` | ok | Есть статическая QA HTML-графиков: русские названия/оси/hover, volume scale, stacked structure charts, Sankey subtitle, risk label limit, scatter versions, yield boxplot mode и long-mode integrity. Поддерживает фильтры `--report-date`, `--retrospective-years`, `--period-type`, `--aggregation-mode`. | Visual regression как отдельный screenshot/fallback-модуль еще отсутствует. |
| `scripts/schema_validation.py` | ok | Проверяет `aggregation_mode`, period dates, interval rules, target period, monthly layer, outputs structure, отсутствие файлов напрямую в `outputs/exports/`, chart data exports, `placement_volume_bln`. | Нужно будет подключить проверки run manifest, semantic model v2 и revenue outputs. |
| `scripts/regression_tests.py` | ok | Проверяет period logic, monthly layer, ДРПА, zero placement, unsatisfied auction, missing/zero yield, bid-to-cover outliers, outputs structure. | Требуется расширение через `scripts/anomaly_tests.py` для дополнительных аномалий второй модернизации. |
| `scripts/smoke_tests.py` | ok | Проверяет `py_compile` ключевых scripts, наличие аналитических таблиц, charts, monthly outputs, dashboard exports, outputs structure, отсутствие XLSX напрямую в `outputs/exports/`. Может опционально запускать pipeline. | Нужно добавить проверки новых артефактов второй модернизации после их появления. |

## Проверка структуры outputs

| Папка | Статус | Комментарий |
| --- | --- | --- |
| `outputs/charts/` | ok | Найдено HTML-графиков: `29`. |
| `outputs/reports/` | ok | Корневая папка отчетов существует. |
| `outputs/reports/analytical_tables/` | ok | Найдено файлов: `6`. |
| `outputs/reports/monthly_tables/` | ok | Папка существует. |
| `outputs/exports/analytical_csv/` | ok | Найдено файлов: `20`. |
| `outputs/exports/chart_data/` | ok | Найдено файлов во вложенных папках: `135`. |
| `outputs/exports/chart_data/risk_quadrant/` | ok | Папка существует. |
| `outputs/exports/chart_data/sankey/` | ok | Папка существует. |
| `outputs/exports/chart_data/boxplot/` | ok | Папка существует. |
| `outputs/exports/chart_data/structure/` | ok | Папка существует. |
| `outputs/exports/technical/` | ok | Папка существует. |
| `outputs/exports/technical/review_required/` | ok | Папка существует. |
| `outputs/dashboards/` | ok | Найдено файлов во вложенных папках: `67`. |
| `outputs/dashboards/monthly/` | ok | Папка существует. |
| `outputs/dashboards/semantic_layer/` | ok | Папка существует. |
| `outputs/archive/` | ok | Папка существует. |

В корне `outputs/exports/` файлов не найдено. Контракт новой структуры outputs соблюден на момент baseline-аудита.

## Что считать уже выполненным и не переписывать

- `--aggregation-mode cumulative|point`.
- `report_params.py` и периодная логика.
- `period_filter.py` и формирование `ofz_auctions_report_scope.csv`.
- Новая структура `outputs/`.
- Базовые аналитические таблицы.
- Базовые графики, monthly layer и monthly charts.
- Dashboard exports и semantic layer первого поколения.
- HTML QA, schema validation, regression tests и smoke tests первого поколения.

## Что является задачами второй модернизации

| Блок | Текущий статус | Нужно добавить |
| --- | --- | --- |
| Единый quality gate | отсутствует как отдельный скрипт | `scripts/quality_gate.py`, `docs/quality_gate_report.md`, отчет в `outputs/reports/`. |
| Visual regression | отсутствует как отдельный скрипт | `scripts/visual_regression.py` с fallback HTML inspection. |
| Run manifest | отсутствует как отдельный скрипт | `scripts/run_manifest.py`, JSON/MD manifest, latest manifest в `data/processed/`. |
| Anomaly tests | частично покрыто regression tests | `scripts/anomaly_tests.py` и отдельный отчет. |
| Semantic model v2 | есть semantic layer v1 | Версионированный semantic model v2 в `outputs/dashboards/semantic_model_v2/`. |
| Revenue analytics | частично поля встречаются в monthly/dashboard коде | Полный слой таблиц, графиков, KPI и документации по выручке. |
| Графики второй модернизации | базовые графики есть | Monthly bid-cover labels, discount vs demand, yield boxplot, отдельный boxplot ОФЗ-ПД. |

## Риски и ограничения baseline

- Baseline-аудит не подтверждает runtime-успех последнего полного запуска pipeline.
- Старые outputs могут не отражать будущие исправления до повторной генерации.
- `html_chart_qa.py` остается статическим HTML-анализом и не заменяет полноценную визуальную регрессию.
- Revenue analytics нужно начинать с проверки надежного mapping для `revenue_volume`; данные нельзя выдумывать.
- Вторую модернизацию нужно маркировать в новых отчетах и changelog как `вторая модернизация`.

## Рекомендуемые команды ручной проверки

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\run_pipeline.py
```

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py
```

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\10_build_monthly_charts.py
```

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\08_analytical_tables.py
```

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\07_dashboard_exports.py
```

```powershell
.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

```powershell
.\.venv\Scripts\python.exe scripts\regression_tests.py
```

```powershell
.\.venv\Scripts\python.exe scripts\smoke_tests.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

```powershell
.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

