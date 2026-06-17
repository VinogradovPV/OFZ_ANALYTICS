# План декомпозиции модулей

Дата актуализации: 2026-06-08.

Документ фиксирует P1-план будущей декомпозиции крупных scripts. На этом этапе физический перенос файлов не выполняется. Все существующие команды запуска, imports, entry points и `run_pipeline.py` остаются без изменений.

## Общие правила

1. Сначала выносить pure helper functions без побочных эффектов.
2. Затем выносить chart family builders и export helpers.
3. Затем выносить QA check groups.
4. После каждого переноса сохранять wrapper compatibility для старого пути.
5. После каждого шага запускать:

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

6. Не менять `data/raw/`.
7. Не менять generated outputs вручную.
8. Не выполнять массовую миграцию нескольких монолитов в одном commit.

## Целевая структура

Предлагаемая будущая структура:

```text
scripts/
  pipeline/
    run_pipeline.py
    interactive_pipeline.py
  stages/
    data_audit.py
    data_cleaning.py
    feature_engineering.py
    analytical_tables.py
    dashboard_exports.py
    revenue_analytics.py
  charts/
    core.py
    risk.py
    scatter.py
    yield_charts.py
    structure.py
    revenue.py
    monthly/
      placement.py
      demand_supply.py
      bid_cover.py
      heatmap.py
      structure.py
  qa/
    quality_gate.py
    schema_validation.py
    html/
      monthly_checks.py
      scatter_checks.py
      yield_checks.py
      revenue_checks.py
    visual/
      plotly_json_checks.py
      screenshot_backend.py
  metadata/
    run_manifest.py
    raw_data_registry.py
    semantic_model_v2.py
  utils/
    config.py
    paths.py
    markdown.py
    palette.py
    scatter_policy.py
  maintenance/
    cleanup_outputs.py
    cleanup_docs.py
```

Физический перенос допустим только с wrapper-файлами на старых путях, например:

```python
from scripts.pipeline.run_pipeline import main

if __name__ == "__main__":
    main()
```

## 1. `scripts/06_build_charts.py`

Текущая роль: основной builder HTML-графиков target/retrospective/risk/scatter/structure/yield/format terms, а также chart data exports для многих семейств.

Причины декомпозиции:
- самый крупный файл проекта;
- смешивает подготовку данных, chart policy, Plotly layout, exports и документацию;
- высокая стоимость review при точечных изменениях графиков;
- риск регрессии при доработке одного семейства графиков.

Риски:
- разрыв имен выходных HTML/CSV;
- нарушение routing через `config.chart_html_dir_for_name`;
- потеря hover/export полей;
- расхождение с `html_chart_qa.py` и `visual_regression.py`.

Зависимости:
- `config.py`;
- `palette.py`;
- `report_params.py`;
- `scatter_chart_policy.py`;
- `utils.py`;
- `period_filter.py` output: `data/processed/ofz_auctions_report_scope.csv`;
- QA: `html_chart_qa.py`, `visual_regression.py`, `schema_validation.py`.

Предлагаемая target structure:

```text
scripts/charts/core.py
scripts/charts/risk.py
scripts/charts/scatter.py
scripts/charts/yield_charts.py
scripts/charts/structure.py
scripts/charts/format_terms.py
```

Порядок безопасного переноса:
1. Вынести pure helpers форматирования чисел, подписей, hover и subtitle.
2. Вынести chart data export helpers.
3. Вынести семейство `yield_vs_discount`.
4. Вынести `format_terms_*`.
5. Вынести risk/scatter charts.
6. Вынести structure charts.
7. Оставить `scripts/06_build_charts.py` wrapper/CLI orchestrator до полной стабилизации.

Тесты после каждого шага:
- `compileall`;
- `scripts/06_build_charts.py` для baseline параметров;
- `schema_validation.py`;
- `html_chart_qa.py`;
- `visual_regression.py`;
- `quality_gate.py --fast`.

Rollback:
- вернуть импорт в `06_build_charts.py` к предыдущей локальной функции;
- не удалять исходный helper до прохождения двух последовательных quality gate;
- если изменились имена outputs или CSV-схема, откатить commit целиком.

## 2. `scripts/10_build_monthly_charts.py`

Текущая роль: monthly placement, demand/supply, bid-cover, yield, structure и heatmap charts.

Причины декомпозиции:
- несколько независимых chart families в одном файле;
- разные политики подписей для bar/line/facet/heatmap;
- высокие риски визуальных регрессий при локальной правке.

Риски:
- повторное появление дублей Y-axis в facet;
- нарушение label policy monthly bar/line charts;
- попадание `Итого` в color scale heatmap;
- рассинхронизация chart data exports.

Зависимости:
- monthly metrics: `data/processed/ofz_monthly_metrics.csv`;
- `config.py`, `palette.py`, `report_params.py`, `utils.py`;
- QA: monthly checks РІ `html_chart_qa.py` Рё `visual_regression.py`.

Предлагаемая target structure:

```text
scripts/charts/monthly/placement.py
scripts/charts/monthly/demand_supply.py
scripts/charts/monthly/bid_cover.py
scripts/charts/monthly/yield.py
scripts/charts/monthly/structure.py
scripts/charts/monthly/heatmap.py
```

Порядок безопасного переноса:
1. Вынести общие monthly helpers: month labels, period labels, formatting.
2. Вынести placement bar/line charts.
3. Вынести demand/supply and bid-cover charts.
4. Вынести facet structure charts.
5. Вынести heatmap logic вместе с neutral total column policy.
6. Оставить `10_build_monthly_charts.py` как CLI wrapper.

Тесты:
- `compileall`;
- `scripts/09_monthly_analytics.py`;
- `scripts/10_build_monthly_charts.py`;
- `html_chart_qa.py`;
- `visual_regression.py`;
- `quality_gate.py --fast`.

Rollback:
- если месячные HTML/CSV отличаются по именам или обязательным колонкам, откатить перенос конкретного семейства;
- если visual regression ловит label/axis regression, вернуть builder в монолит до повторной изоляции.

## 3. `scripts/html_chart_qa.py`

Текущая роль: единый QA-контракт HTML-графиков и chart data exports.

Причины декомпозиции:
- много независимых check groups;
- один большой файл затрудняет поддержку contract tests;
- растет вместе с каждым новым семейством графиков.

Риски:
- потеря coverage отдельных chart families;
- разная трактовка лимитов подписей;
- несовместимость с `quality_gate.py`.

Зависимости:
- `config.py`;
- `scatter_chart_policy.py`;
- generated HTML/CSV outputs;
- `quality_gate.py`.

Предлагаемая target structure:

```text
scripts/qa/html/core.py
scripts/qa/html/monthly_checks.py
scripts/qa/html/scatter_checks.py
scripts/qa/html/yield_checks.py
scripts/qa/html/revenue_checks.py
scripts/qa/html/structure_checks.py
```

Порядок безопасного переноса:
1. Вынести file discovery и Plotly JSON extraction.
2. Вынести monthly checks.
3. Вынести scatter/yield checks.
4. Вынести revenue/structure checks.
5. Оставить `html_chart_qa.py` CLI wrapper с прежними аргументами.

Тесты:
- `compileall`;
- `scripts/html_chart_qa.py`;
- `quality_gate.py --fast`;
- manual diff РїРѕ `docs/06_quality/quality_gate_report.md`.

Rollback:
- если количество проверок или статус меняется без причины, откатить конкретный group extraction;
- wrapper должен оставаться единственной точкой запуска до полного перехода.

## 4. `scripts/visual_regression.py`

Текущая роль: visual regression или fallback static HTML / Plotly JSON inspection.

Причины декомпозиции:
- смешивает screenshot backend, fallback parser и семейные проверки;
- большой файл, высокая когнитивная нагрузка;
- future screenshot backend проще подключать отдельно.

Риски:
- пропуск fallback checks при отсутствии screenshot backend;
- ложные visual warnings;
- несовместимость с quality gate.

Зависимости:
- generated HTML outputs;
- `config.py`, `report_params.py`, `utils.py`;
- `quality_gate.py`.

Предлагаемая target structure:

```text
scripts/qa/visual/core.py
scripts/qa/visual/plotly_json_checks.py
scripts/qa/visual/screenshot_backend.py
scripts/qa/visual/monthly_checks.py
scripts/qa/visual/scatter_checks.py
```

Порядок безопасного переноса:
1. Вынести HTML discovery и Plotly JSON extraction.
2. Вынести fallback checks.
3. Вынести screenshot backend interface без включения нового backend по умолчанию.
4. Оставить `visual_regression.py` CLI wrapper.

Тесты:
- `compileall`;
- `scripts/visual_regression.py`;
- `quality_gate.py --fast`.

Rollback:
- если fallback перестал работать без screenshot backend, откатить перенос backend boundary;
- любые изменения количества HTML files/checks требуют review.

## 5. `scripts/quality_gate.py`

Текущая роль: единая точка production QA, запускающая py_compile, schema, regression, anomaly, smoke, HTML QA, visual regression, docs/charts/run manifest checks.

Причины декомпозиции:
- содержит orchestration и конкретные проверки в одном файле;
- список проверок будет расти;
- отдельные checks лучше тестировать независимо.

Риски:
- потеря fail/warning semantics;
- неправильный режим `--fast`/`--full`;
- изменение формата report.

Зависимости:
- все QA scripts;
- `config.py`, `report_params.py`, `utils.py`;
- docs report paths.

Предлагаемая target structure:

```text
scripts/qa/gate/core.py
scripts/qa/gate/script_checks.py
scripts/qa/gate/docs_checks.py
scripts/qa/gate/outputs_checks.py
scripts/qa/gate/dashboard_checks.py
```

Порядок безопасного переноса:
1. Вынести pure check functions без изменения result model.
2. Вынести report rendering.
3. Вынести command runner helpers.
4. Оставить `quality_gate.py` CLI wrapper.

Тесты:
- `compileall`;
- `ofz-quality --help`;
- `ofz-quality --fast ...`;
- fallback `scripts/quality_gate.py --fast ...`.

Rollback:
- если `quality_gate_report.md` меняет формат без планового изменения, откатить;
- если статус `warning/fail` меняется без изменения данных, откатить check extraction.

## 6. `scripts/07_dashboard_exports.py`

Текущая роль: dashboard exports, supporting dictionaries, semantic/dashboard-ready datasets.

Причины декомпозиции:
- смешивает export logic, transformations и documentation;
- пересекается по смыслу с semantic model v2;
- future dashboard changes проще развивать в отдельных modules.

Риски:
- изменение dashboard file names/schema;
- расхождение с `dashboard_semantic_model_v2`;
- нарушение BI contract.

Зависимости:
- report scope dataset;
- `config.py`, `report_params.py`, `utils.py`;
- `build_semantic_model_v2.py`;
- quality gate dashboard semantic checks.

Предлагаемая target structure:

```text
scripts/stages/dashboard_exports.py
scripts/dashboard/export_tables.py
scripts/dashboard/semantic_helpers.py
scripts/dashboard/documentation.py
```

Порядок безопасного переноса:
1. Вынести pure field mapping helpers.
2. Вынести table export helpers.
3. Вынести documentation rendering.
4. Оставить старый `07_dashboard_exports.py` wrapper.

Тесты:
- `compileall`;
- `scripts/07_dashboard_exports.py`;
- `scripts/build_semantic_model_v2.py`;
- `quality_gate.py --fast`.

Rollback:
- если dashboard exports изменили схему/имена без ожидаемого contract update, откатить перенос;
- semantic model v2 должен оставаться валидным после каждого шага.

## Критерии релиза

Декомпозицию считать готовой только если:

- старые команды из README продолжают работать;
- entry points из `pyproject.toml` продолжают работать;
- `compileall` проходит;
- `quality_gate.py --fast` проходит;
- generated output names не меняются без отдельного documented contract update;
- `scripts_inventory_before_cleanup.md` обновлен после фактической миграции.

