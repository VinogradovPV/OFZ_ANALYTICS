# POSTP3.6 - План декомпозиции chart/QA модулей

Дата: 2026-06-24.

## Цель

Подготовить безопасную декомпозицию крупных chart/QA scripts без одновременного изменения финансовой методологии, визуального смысла графиков и quality-gate contract.

На этом этапе код не меняется. Документ фиксирует текущую структуру, зависимости, риски и порядок миграции.

## Текущие крупные модули

| Файл | Размер | Top-level functions | Classes | Роль |
|---|---:|---:|---:|---|
| `scripts/06_build_charts.py` | ~346 KB / 7162 строк | 175 | 1 | Stage 8: основные Plotly-графики, export CSV, limitations report. |
| `scripts/10_build_monthly_charts.py` | ~87 KB / 1890 строк | 54 | 1 | Stage monthly charts: monthly metrics charts, heatmaps, monthly chart CSV. |
| `scripts/html_chart_qa.py` | ~115 KB / 2269 строк | 63 | 0 | Static HTML/chart-data QA для quality-fast. |
| `scripts/visual_regression.py` | ~77 KB / 1406 строк | 57 | 2 | Visual regression fallback + optional screenshot backend. |

Уже существует пакет `scripts/charts/`:

- `scripts/charts/common.py` содержит реально используемые formatting helpers;
- `scripts/charts/boxplot.py`, `monthly.py`, `revenue.py`, `scatter.py`, `structure.py` пока являются почти пустыми заготовками.

Вывод: декомпозицию лучше вести через развитие существующего `scripts/charts/`, а не через создание параллельного пакета.

## Семейства графиков

### `scripts/06_build_charts.py`

Основные группы функций:

- common orchestration and IO: `main`, `read_report_scope`, `filter_scope`, `prepare_scope`, `make_result`, `make_suffix`, `chart_data_dir_for_name`, `write_limitations`;
- shared formatting/layout: volume conversions, hover labels, axis helpers, data quality display;
- structure charts: placement volume, maturity structure, format structure, format discount, format terms comparison/delta;
- risk charts: demand/supply, bid-to-cover, risk quadrant, retrospective risk quadrant, demand-to-placement risk;
- scatter charts: demand/cutoff, yield/demand, discount/demand, yield/discount, format terms scatter;
- yield charts: yield by type, OFZ-PD yield scope charts, yield/discount charts;
- boxplot charts: yield boxplot by OFZ type, OFZ-PD boxplot, stats exports, annotations, hover traces;
- sankey charts: structure sankey, period/maturity/type/format chains, target-period sankey;
- technical helpers: weighted averages, missing columns, markdown table rendering.

AST family counts:

| Family token | Functions |
|---|---:|
| `yield` | 46 |
| `format` | 33 |
| `boxplot` | 22 |
| `scatter` | 18 |
| `sankey` | 15 |
| `risk` | 11 |
| `hover` | 15 |

### `scripts/10_build_monthly_charts.py`

Основные группы:

- monthly orchestration and IO;
- monthly placement/cumulative placement;
- monthly demand/supply and bid-to-cover;
- monthly OFZ-PD weighted yield chart;
- monthly structure by format/maturity;
- monthly placement and revenue heatmaps;
- monthly labels, hover and export helpers.

AST family counts:

| Family token | Functions |
|---|---:|
| `monthly` | 26 |
| `heatmap` | 8 |
| `revenue` | 7 |
| `hover` | 5 |
| `format` | 4 |

### `scripts/html_chart_qa.py`

Основные группы:

- CLI and file filtering;
- Plotly payload extraction;
- common static checks: titles, axes, hovertemplate, volume scale;
- monthly chart contracts;
- format/structure contracts;
- yield/discount contracts;
- boxplot/sankey/scatter contracts;
- CSV companion contract checks;
- report rendering.

AST family counts:

| Family token | Functions |
|---|---:|
| `check` | 36 |
| `contract` | 20 |
| `format` | 11 |
| `yield` | 7 |
| `monthly` | 7 |
| `boxplot` | 5 |

### `scripts/visual_regression.py`

Основные группы:

- CLI and mode selection;
- screenshot backend detection;
- Playwright capture;
- Chromium CLI fallback;
- screenshot manifest/diff report;
- static HTML fallback checks;
- chart-specific visual contracts;
- report rendering.

AST family counts:

| Family token | Functions |
|---|---:|
| `check` | 22 |
| `contract` | 9 |
| `screenshot` | 7 |
| `format` | 6 |
| `monthly` | 4 |

## Целевая структура модулей

Предлагаемая структура без изменения entry points:

```text
scripts/charts/
  __init__.py
  common.py
  io.py
  layout.py
  registry.py
  structure.py
  risk.py
  scatter.py
  yield_charts.py
  boxplot.py
  sankey.py
  monthly.py
  monthly_heatmaps.py
  exports.py
  limitations.py

scripts/qa/chart_contracts/
  __init__.py
  common.py
  html_payload.py
  monthly.py
  structure.py
  format_terms.py
  yield_discount.py
  boxplot.py
  sankey.py
  screenshot_backend.py
  visual_static.py
  reports.py
```

Entry points должны остаться совместимыми:

- `scripts/06_build_charts.py` остается thin wrapper для stage 8;
- `scripts/10_build_monthly_charts.py` остается thin wrapper для monthly chart stage;
- `scripts/html_chart_qa.py` остается CLI wrapper для quality gate;
- `scripts/visual_regression.py` остается CLI wrapper для quality gate и screenshot mode.

## Зависимости

Ключевые shared dependencies:

- `scripts/config.py` - пути outputs/docs/data;
- `scripts/report_params.py` - report date/period/aggregation contract;
- `scripts/palette.py` - цвета и порядок категорий;
- `scripts/scatter_chart_policy.py` - лимиты подписей scatter;
- `scripts/yield_policy.py` - OFZ-PD yield scope/title policy;
- `scripts/charts/common.py` - форматирование чисел и hover labels;
- `scripts/qa/html_chart_contracts.py` - текущие QA constants and `QaResult`;
- Plotly and pandas.

Декомпозиция не должна переносить business rules в QA-only modules. QA modules должны проверять контракты, а не определять расчетную методологию.

## Риски

1. **Изменение методологии под видом рефакторинга.**
   - Особенно опасны yield, OFZ-PD scope, OFZ-PK/OFZ-IN exclusion, discount calculations и DRPA handling.
   - Миграция должна быть механической: сначала move-only, затем отдельные behavior changes только отдельными задачами.

2. **Смена filenames/output paths.**
   - Quality gate, README, release bundle и BI package зависят от стабильных paths.
   - `make_result`, suffix generation и `chart_data_dir_for_name` нужно переносить первыми и покрыть smoke.

3. **Разрыв CSV companion contracts.**
   - HTML QA активно проверяет CSV exports рядом с графиками.
   - При переносе chart family нужно проверять HTML + CSV вместе.

4. **Слабая визуальная regression без screenshot backend.**
   - Static fallback полезен, но не ловит все layout regressions.
   - После декомпозиции крупных families нужен outside-sandbox screenshot check.

5. **Циклические imports.**
   - `config`, `report_params`, `palette`, `charts.common` должны быть нижним слоем.
   - Family modules не должны импортировать wrappers.

6. **Слишком большой PR/commit.**
   - Нельзя переносить все 7000 строк сразу.
   - Каждый family move должен иметь отдельный commit и targeted regression.

## Порядок миграции

### Этап 1 - shared foundation

Цель: вынести только общие модели/IO без изменения графиков.

Кандидаты:

- `ChartResult`;
- `ChartBuilder`;
- `make_suffix` / monthly suffix equivalent;
- `make_result`;
- `chart_data_dir_for_name`;
- common output directory preparation;
- shared limitation report helpers.

Проверки:

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py scripts\10_build_monthly_charts.py
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

### Этап 2 - structure and format charts

Цель: перенести сравнительно независимые structure/format functions в `scripts/charts/structure.py`.

Включить:

- placement volume;
- maturity structure;
- format structure;
- format discount;
- format terms comparison/delta.

Regression:

- `format_structure_contract`;
- `format_discount_contract`;
- `format_terms_comparison_contract`;
- `format_terms_delta_by_format_contract`;
- `outputs_structure`;
- `html_chart_qa.py`.

### Этап 3 - risk and scatter charts

Цель: перенести risk/scatter functions в `scripts/charts/risk.py` и `scripts/charts/scatter.py`.

Включить:

- demand/supply;
- bid-to-cover;
- risk quadrant and retrospective variants;
- demand cutoff;
- yield/demand;
- discount/demand;
- yield/discount;
- format terms scatter.

Regression:

- `yield_vs_discount_contract`;
- scatter label limits;
- risk quadrant contracts;
- `html_chart_qa.py`;
- `visual_regression.py --mode auto`.

### Этап 4 - yield and boxplot

Цель: отдельно перенести yield/boxplot modules, потому что они связаны с последним критическим defect по ОФЗ-ПД.

Включить:

- `yield_by_type`;
- OFZ-PD yield chart helpers;
- boxplot by OFZ type;
- OFZ-PD boxplot;
- stats exports and annotations.

Regression:

```powershell
.\.venv\Scripts\python.exe scripts\qa\ofz_pd_yield_metrics_regression.py
.\.venv\Scripts\ofz-run.exe --report-date 2026-01-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-schema.exe --report-date 2026-01-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-01-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Manual spot check:

- November 2025 `yield_weighted_avg` remains around `14.87`;
- `yield_min` remains around `14.73`;
- title/tooltip says `ОФЗ-ПД`.

### Этап 5 - sankey

Цель: перенести sankey chain builders в `scripts/charts/sankey.py`.

Regression:

- Sankey HTML exists;
- Sankey CSV exports exist;
- hover and volume labels remain in млрд рублей;
- no filename/path changes.

### Этап 6 - monthly charts

Цель: перенести monthly chart families в `scripts/charts/monthly.py` и `scripts/charts/monthly_heatmaps.py`.

Включить:

- monthly placement;
- cumulative placement;
- demand/supply;
- bid-to-cover;
- monthly OFZ-PD yield;
- structure by format/maturity;
- placement/revenue heatmaps.

Regression:

- monthly chart contract checks;
- monthly heatmap total column checks;
- monthly metrics schema;
- `ofz-quality --fast`.

### Этап 7 - HTML QA contracts

Цель: после стабилизации chart modules разнести `html_chart_qa.py` на small contract modules.

Порядок:

1. `html_payload.py` - Plotly extraction/read helpers.
2. `common.py` - common checks and `QaResult` reuse.
3. `monthly.py` - monthly contracts.
4. `structure.py` / `format_terms.py`.
5. `yield_discount.py`.
6. `boxplot.py` / `sankey.py`.
7. wrapper keeps CLI and report rendering.

Regression:

```powershell
.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

### Этап 8 - visual regression decomposition

Цель: отделить screenshot backend от static visual checks.

Кандидаты:

- `screenshot_backend.py`: Playwright/Chromium detection and capture;
- `visual_static.py`: fallback static checks;
- `reports.py`: screenshot manifest/diff/report rendering.

Regression:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode auto --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Outside sandbox manual:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode screenshot --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Regression matrix per family

| Family | Required checks |
|---|---|
| Shared chart foundation | `py_compile`, `compileall`, `ofz-run`, `ofz-schema`, `ofz-quality --fast` |
| Structure/format | HTML QA format/structure contracts, schema, quality-fast |
| Risk/scatter | HTML QA scatter/risk contracts, visual regression auto |
| Yield/boxplot | OFZ-PD yield regression, January 2026 pipeline/schema/quality-fast, manual November 2025 spot check |
| Sankey | HTML exists, CSV exists, volume units, quality-fast |
| Monthly | monthly schema, monthly chart contracts, heatmap contracts, quality-fast |
| HTML QA modules | direct `html_chart_qa.py`, quality-fast |
| Visual regression modules | `visual_regression.py --mode auto`, outside-sandbox screenshot when available |

## Запреты на время декомпозиции

- Не менять financial methodology вместе с move-only refactor.
- Не менять OFZ-PD yield scope.
- Не менять filenames, suffixes и output directories без отдельной schema/docs migration.
- Не менять quality gate semantics вместе с переносом функций.
- Не удалять old wrappers до завершения migration.
- Не коммитить generated outputs, screenshots, logs, `.ofz_launcher`, `outputs/`, `releases/`, `data/processed`, `versions/`.

## Definition of Done для каждого move-only этапа

1. Entry point остается тем же.
2. Количество и имена generated charts/CSV не меняются или изменение явно documented.
3. `ofz-run` проходит на baseline params.
4. `ofz-schema` проходит.
5. `ofz-quality --fast` проходит.
6. Для yield family дополнительно проходит OFZ-PD regression.
7. Staged scope содержит только source/docs/tests, без generated artifacts.

## Рекомендация

Начать не с переноса chart families, а с маленького foundation этапа:

- вынести `ChartResult`, suffix/path helpers и result writer;
- добавить targeted smoke на expected chart output paths;
- сохранить wrappers untouched для CLI compatibility.

После foundation двигаться по одному семейству графиков за commit. Самый рискованный блок `yield/boxplot` лучше переносить после structure/risk, когда migration pattern уже проверен.
