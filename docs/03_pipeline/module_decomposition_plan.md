# Module decomposition plan

Р”Р°С‚Р° Р°РєС‚СѓР°Р»РёР·Р°С†РёРё: 2026-06-08.

Р”РѕРєСѓРјРµРЅС‚ С„РёРєСЃРёСЂСѓРµС‚ P1-РїР»Р°РЅ Р±СѓРґСѓС‰РµР№ РґРµРєРѕРјРїРѕР·РёС†РёРё РєСЂСѓРїРЅС‹С… scripts. РќР° СЌС‚РѕРј СЌС‚Р°РїРµ С„РёР·РёС‡РµСЃРєРёР№ РїРµСЂРµРЅРѕСЃ С„Р°Р№Р»РѕРІ РЅРµ РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ. Р’СЃРµ СЃСѓС‰РµСЃС‚РІСѓСЋС‰РёРµ РєРѕРјР°РЅРґС‹ Р·Р°РїСѓСЃРєР°, imports, entry points Рё `run_pipeline.py` РѕСЃС‚Р°СЋС‚СЃСЏ Р±РµР· РёР·РјРµРЅРµРЅРёР№.

## РћР±С‰РёРµ РїСЂР°РІРёР»Р°

1. РЎРЅР°С‡Р°Р»Р° РІС‹РЅРѕСЃРёС‚СЊ pure helper functions Р±РµР· РїРѕР±РѕС‡РЅС‹С… СЌС„С„РµРєС‚РѕРІ.
2. Р—Р°С‚РµРј РІС‹РЅРѕСЃРёС‚СЊ chart family builders Рё export helpers.
3. Р—Р°С‚РµРј РІС‹РЅРѕСЃРёС‚СЊ QA check groups.
4. РџРѕСЃР»Рµ РєР°Р¶РґРѕРіРѕ РїРµСЂРµРЅРѕСЃР° СЃРѕС…СЂР°РЅСЏС‚СЊ wrapper compatibility РґР»СЏ СЃС‚Р°СЂРѕРіРѕ РїСѓС‚Рё.
5. РџРѕСЃР»Рµ РєР°Р¶РґРѕРіРѕ С€Р°РіР° Р·Р°РїСѓСЃРєР°С‚СЊ:

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

6. РќРµ РјРµРЅСЏС‚СЊ `data/raw/`.
7. РќРµ РјРµРЅСЏС‚СЊ generated outputs РІСЂСѓС‡РЅСѓСЋ.
8. РќРµ РІС‹РїРѕР»РЅСЏС‚СЊ РјР°СЃСЃРѕРІСѓСЋ РјРёРіСЂР°С†РёСЋ РЅРµСЃРєРѕР»СЊРєРёС… РјРѕРЅРѕР»РёС‚РѕРІ РІ РѕРґРЅРѕРј commit.

## Target Structure

РџСЂРµРґР»Р°РіР°РµРјР°СЏ Р±СѓРґСѓС‰Р°СЏ СЃС‚СЂСѓРєС‚СѓСЂР°:

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

Р¤РёР·РёС‡РµСЃРєРёР№ РїРµСЂРµРЅРѕСЃ РґРѕРїСѓСЃС‚РёРј С‚РѕР»СЊРєРѕ СЃ wrapper-С„Р°Р№Р»Р°РјРё РЅР° СЃС‚Р°СЂС‹С… РїСѓС‚СЏС…, РЅР°РїСЂРёРјРµСЂ:

```python
from scripts.pipeline.run_pipeline import main

if __name__ == "__main__":
    main()
```

## 1. `scripts/06_build_charts.py`

РўРµРєСѓС‰Р°СЏ СЂРѕР»СЊ: РѕСЃРЅРѕРІРЅРѕР№ builder HTML-РіСЂР°С„РёРєРѕРІ target/retrospective/risk/scatter/structure/yield/format terms, Р° С‚Р°РєР¶Рµ chart data exports РґР»СЏ РјРЅРѕРіРёС… СЃРµРјРµР№СЃС‚РІ.

РџСЂРёС‡РёРЅС‹ РґРµРєРѕРјРїРѕР·РёС†РёРё:
- СЃР°РјС‹Р№ РєСЂСѓРїРЅС‹Р№ С„Р°Р№Р» РїСЂРѕРµРєС‚Р°;
- СЃРјРµС€РёРІР°РµС‚ РїРѕРґРіРѕС‚РѕРІРєСѓ РґР°РЅРЅС‹С…, chart policy, Plotly layout, exports Рё РґРѕРєСѓРјРµРЅС‚Р°С†РёСЋ;
- РІС‹СЃРѕРєР°СЏ СЃС‚РѕРёРјРѕСЃС‚СЊ review РїСЂРё С‚РѕС‡РµС‡РЅС‹С… РёР·РјРµРЅРµРЅРёСЏС… РіСЂР°С„РёРєРѕРІ;
- СЂРёСЃРє СЂРµРіСЂРµСЃСЃРёРё РїСЂРё РґРѕСЂР°Р±РѕС‚РєРµ РѕРґРЅРѕРіРѕ СЃРµРјРµР№СЃС‚РІР° РіСЂР°С„РёРєРѕРІ.

Р РёСЃРєРё:
- СЂР°Р·СЂС‹РІ РёРјРµРЅ РІС‹С…РѕРґРЅС‹С… HTML/CSV;
- РЅР°СЂСѓС€РµРЅРёРµ routing С‡РµСЂРµР· `config.chart_html_dir_for_name`;
- РїРѕС‚РµСЂСЏ hover/export РїРѕР»РµР№;
- СЂР°СЃС…РѕР¶РґРµРЅРёРµ СЃ `html_chart_qa.py` Рё `visual_regression.py`.

Р—Р°РІРёСЃРёРјРѕСЃС‚Рё:
- `config.py`;
- `palette.py`;
- `report_params.py`;
- `scatter_chart_policy.py`;
- `utils.py`;
- `period_filter.py` output: `data/processed/ofz_auctions_report_scope.csv`;
- QA: `html_chart_qa.py`, `visual_regression.py`, `schema_validation.py`.

РџСЂРµРґР»Р°РіР°РµРјР°СЏ target structure:

```text
scripts/charts/core.py
scripts/charts/risk.py
scripts/charts/scatter.py
scripts/charts/yield_charts.py
scripts/charts/structure.py
scripts/charts/format_terms.py
```

РџРѕСЂСЏРґРѕРє Р±РµР·РѕРїР°СЃРЅРѕРіРѕ РїРµСЂРµРЅРѕСЃР°:
1. Р’С‹РЅРµСЃС‚Рё pure helpers С„РѕСЂРјР°С‚РёСЂРѕРІР°РЅРёСЏ С‡РёСЃРµР», РїРѕРґРїРёСЃРµР№, hover Рё subtitle.
2. Р’С‹РЅРµСЃС‚Рё chart data export helpers.
3. Р’С‹РЅРµСЃС‚Рё СЃРµРјРµР№СЃС‚РІРѕ `yield_vs_discount`.
4. Р’С‹РЅРµСЃС‚Рё `format_terms_*`.
5. Р’С‹РЅРµСЃС‚Рё risk/scatter charts.
6. Р’С‹РЅРµСЃС‚Рё structure charts.
7. РћСЃС‚Р°РІРёС‚СЊ `scripts/06_build_charts.py` wrapper/CLI orchestrator РґРѕ РїРѕР»РЅРѕР№ СЃС‚Р°Р±РёР»РёР·Р°С†РёРё.

РўРµСЃС‚С‹ РїРѕСЃР»Рµ РєР°Р¶РґРѕРіРѕ С€Р°РіР°:
- `compileall`;
- `scripts/06_build_charts.py` РґР»СЏ baseline РїР°СЂР°РјРµС‚СЂРѕРІ;
- `schema_validation.py`;
- `html_chart_qa.py`;
- `visual_regression.py`;
- `quality_gate.py --fast`.

Rollback:
- РІРµСЂРЅСѓС‚СЊ РёРјРїРѕСЂС‚ РІ `06_build_charts.py` Рє РїСЂРµРґС‹РґСѓС‰РµР№ Р»РѕРєР°Р»СЊРЅРѕР№ С„СѓРЅРєС†РёРё;
- РЅРµ СѓРґР°Р»СЏС‚СЊ РёСЃС…РѕРґРЅС‹Р№ helper РґРѕ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РґРІСѓС… РїРѕСЃР»РµРґРѕРІР°С‚РµР»СЊРЅС‹С… quality gate;
- РµСЃР»Рё РёР·РјРµРЅРёР»РёСЃСЊ РёРјРµРЅР° outputs РёР»Рё CSV-СЃС…РµРјР°, РѕС‚РєР°С‚РёС‚СЊ commit С†РµР»РёРєРѕРј.

## 2. `scripts/10_build_monthly_charts.py`

РўРµРєСѓС‰Р°СЏ СЂРѕР»СЊ: monthly placement, demand/supply, bid-cover, yield, structure Рё heatmap charts.

РџСЂРёС‡РёРЅС‹ РґРµРєРѕРјРїРѕР·РёС†РёРё:
- РЅРµСЃРєРѕР»СЊРєРѕ РЅРµР·Р°РІРёСЃРёРјС‹С… chart families РІ РѕРґРЅРѕРј С„Р°Р№Р»Рµ;
- СЂР°Р·РЅС‹Рµ РїРѕР»РёС‚РёРєРё РїРѕРґРїРёСЃРµР№ РґР»СЏ bar/line/facet/heatmap;
- РІС‹СЃРѕРєРёРµ СЂРёСЃРєРё РІРёР·СѓР°Р»СЊРЅС‹С… СЂРµРіСЂРµСЃСЃРёР№ РїСЂРё Р»РѕРєР°Р»СЊРЅРѕР№ РїСЂР°РІРєРµ.

Р РёСЃРєРё:
- РїРѕРІС‚РѕСЂРЅРѕРµ РїРѕСЏРІР»РµРЅРёРµ РґСѓР±Р»РµР№ Y-axis РІ facet;
- РЅР°СЂСѓС€РµРЅРёРµ label policy monthly bar/line charts;
- РїРѕРїР°РґР°РЅРёРµ `РС‚РѕРіРѕ` РІ color scale heatmap;
- СЂР°СЃСЃРёРЅС…СЂРѕРЅРёР·Р°С†РёСЏ chart data exports.

Р—Р°РІРёСЃРёРјРѕСЃС‚Рё:
- monthly metrics: `data/processed/ofz_monthly_metrics.csv`;
- `config.py`, `palette.py`, `report_params.py`, `utils.py`;
- QA: monthly checks РІ `html_chart_qa.py` Рё `visual_regression.py`.

РџСЂРµРґР»Р°РіР°РµРјР°СЏ target structure:

```text
scripts/charts/monthly/placement.py
scripts/charts/monthly/demand_supply.py
scripts/charts/monthly/bid_cover.py
scripts/charts/monthly/yield.py
scripts/charts/monthly/structure.py
scripts/charts/monthly/heatmap.py
```

РџРѕСЂСЏРґРѕРє Р±РµР·РѕРїР°СЃРЅРѕРіРѕ РїРµСЂРµРЅРѕСЃР°:
1. Р’С‹РЅРµСЃС‚Рё РѕР±С‰РёРµ monthly helpers: month labels, period labels, formatting.
2. Р’С‹РЅРµСЃС‚Рё placement bar/line charts.
3. Р’С‹РЅРµСЃС‚Рё demand/supply and bid-cover charts.
4. Р’С‹РЅРµСЃС‚Рё facet structure charts.
5. Р’С‹РЅРµСЃС‚Рё heatmap logic РІРјРµСЃС‚Рµ СЃ neutral total column policy.
6. РћСЃС‚Р°РІРёС‚СЊ `10_build_monthly_charts.py` РєР°Рє CLI wrapper.

РўРµСЃС‚С‹:
- `compileall`;
- `scripts/09_monthly_analytics.py`;
- `scripts/10_build_monthly_charts.py`;
- `html_chart_qa.py`;
- `visual_regression.py`;
- `quality_gate.py --fast`.

Rollback:
- РµСЃР»Рё РјРµСЃСЏС‡РЅС‹Рµ HTML/CSV РѕС‚Р»РёС‡Р°СЋС‚СЃСЏ РїРѕ РёРјРµРЅР°Рј РёР»Рё РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рј РєРѕР»РѕРЅРєР°Рј, РѕС‚РєР°С‚РёС‚СЊ РїРµСЂРµРЅРѕСЃ РєРѕРЅРєСЂРµС‚РЅРѕРіРѕ СЃРµРјРµР№СЃС‚РІР°;
- РµСЃР»Рё visual regression Р»РѕРІРёС‚ label/axis regression, РІРµСЂРЅСѓС‚СЊ builder РІ РјРѕРЅРѕР»РёС‚ РґРѕ РїРѕРІС‚РѕСЂРЅРѕР№ РёР·РѕР»СЏС†РёРё.

## 3. `scripts/html_chart_qa.py`

РўРµРєСѓС‰Р°СЏ СЂРѕР»СЊ: РµРґРёРЅС‹Р№ QA-РєРѕРЅС‚СЂР°РєС‚ HTML-РіСЂР°С„РёРєРѕРІ Рё chart data exports.

РџСЂРёС‡РёРЅС‹ РґРµРєРѕРјРїРѕР·РёС†РёРё:
- РјРЅРѕРіРѕ РЅРµР·Р°РІРёСЃРёРјС‹С… check groups;
- РѕРґРёРЅ Р±РѕР»СЊС€РѕР№ С„Р°Р№Р» Р·Р°С‚СЂСѓРґРЅСЏРµС‚ РїРѕРґРґРµСЂР¶РєСѓ contract tests;
- СЂР°СЃС‚РµС‚ РІРјРµСЃС‚Рµ СЃ РєР°Р¶РґС‹Рј РЅРѕРІС‹Рј СЃРµРјРµР№СЃС‚РІРѕРј РіСЂР°С„РёРєРѕРІ.

Р РёСЃРєРё:
- РїРѕС‚РµСЂСЏ coverage РѕС‚РґРµР»СЊРЅС‹С… chart families;
- СЂР°Р·РЅР°СЏ С‚СЂР°РєС‚РѕРІРєР° Р»РёРјРёС‚РѕРІ РїРѕРґРїРёСЃРµР№;
- РЅРµСЃРѕРІРјРµСЃС‚РёРјРѕСЃС‚СЊ СЃ `quality_gate.py`.

Р—Р°РІРёСЃРёРјРѕСЃС‚Рё:
- `config.py`;
- `scatter_chart_policy.py`;
- generated HTML/CSV outputs;
- `quality_gate.py`.

РџСЂРµРґР»Р°РіР°РµРјР°СЏ target structure:

```text
scripts/qa/html/core.py
scripts/qa/html/monthly_checks.py
scripts/qa/html/scatter_checks.py
scripts/qa/html/yield_checks.py
scripts/qa/html/revenue_checks.py
scripts/qa/html/structure_checks.py
```

РџРѕСЂСЏРґРѕРє Р±РµР·РѕРїР°СЃРЅРѕРіРѕ РїРµСЂРµРЅРѕСЃР°:
1. Р’С‹РЅРµСЃС‚Рё file discovery Рё Plotly JSON extraction.
2. Р’С‹РЅРµСЃС‚Рё monthly checks.
3. Р’С‹РЅРµСЃС‚Рё scatter/yield checks.
4. Р’С‹РЅРµСЃС‚Рё revenue/structure checks.
5. РћСЃС‚Р°РІРёС‚СЊ `html_chart_qa.py` CLI wrapper СЃ РїСЂРµР¶РЅРёРјРё Р°СЂРіСѓРјРµРЅС‚Р°РјРё.

РўРµСЃС‚С‹:
- `compileall`;
- `scripts/html_chart_qa.py`;
- `quality_gate.py --fast`;
- manual diff РїРѕ `docs/06_quality/quality_gate_report.md`.

Rollback:
- РµСЃР»Рё РєРѕР»РёС‡РµСЃС‚РІРѕ РїСЂРѕРІРµСЂРѕРє РёР»Рё СЃС‚Р°С‚СѓСЃ РјРµРЅСЏРµС‚СЃСЏ Р±РµР· РїСЂРёС‡РёРЅС‹, РѕС‚РєР°С‚РёС‚СЊ РєРѕРЅРєСЂРµС‚РЅС‹Р№ group extraction;
- wrapper РґРѕР»Р¶РµРЅ РѕСЃС‚Р°РІР°С‚СЊСЃСЏ РµРґРёРЅСЃС‚РІРµРЅРЅРѕР№ С‚РѕС‡РєРѕР№ Р·Р°РїСѓСЃРєР° РґРѕ РїРѕР»РЅРѕРіРѕ РїРµСЂРµС…РѕРґР°.

## 4. `scripts/visual_regression.py`

РўРµРєСѓС‰Р°СЏ СЂРѕР»СЊ: visual regression РёР»Рё fallback static HTML / Plotly JSON inspection.

РџСЂРёС‡РёРЅС‹ РґРµРєРѕРјРїРѕР·РёС†РёРё:
- СЃРјРµС€РёРІР°РµС‚ screenshot backend, fallback parser Рё СЃРµРјРµР№РЅС‹Рµ РїСЂРѕРІРµСЂРєРё;
- Р±РѕР»СЊС€РѕР№ С„Р°Р№Р», РІС‹СЃРѕРєР°СЏ РєРѕРіРЅРёС‚РёРІРЅР°СЏ РЅР°РіСЂСѓР·РєР°;
- future screenshot backend РїСЂРѕС‰Рµ РїРѕРґРєР»СЋС‡Р°С‚СЊ РѕС‚РґРµР»СЊРЅРѕ.

Р РёСЃРєРё:
- РїСЂРѕРїСѓСЃРє fallback checks РїСЂРё РѕС‚СЃСѓС‚СЃС‚РІРёРё screenshot backend;
- Р»РѕР¶РЅС‹Рµ visual warnings;
- РЅРµСЃРѕРІРјРµСЃС‚РёРјРѕСЃС‚СЊ СЃ quality gate.

Р—Р°РІРёСЃРёРјРѕСЃС‚Рё:
- generated HTML outputs;
- `config.py`, `report_params.py`, `utils.py`;
- `quality_gate.py`.

РџСЂРµРґР»Р°РіР°РµРјР°СЏ target structure:

```text
scripts/qa/visual/core.py
scripts/qa/visual/plotly_json_checks.py
scripts/qa/visual/screenshot_backend.py
scripts/qa/visual/monthly_checks.py
scripts/qa/visual/scatter_checks.py
```

РџРѕСЂСЏРґРѕРє Р±РµР·РѕРїР°СЃРЅРѕРіРѕ РїРµСЂРµРЅРѕСЃР°:
1. Р’С‹РЅРµСЃС‚Рё HTML discovery Рё Plotly JSON extraction.
2. Р’С‹РЅРµСЃС‚Рё fallback checks.
3. Р’С‹РЅРµСЃС‚Рё screenshot backend interface Р±РµР· РІРєР»СЋС‡РµРЅРёСЏ РЅРѕРІРѕРіРѕ backend РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ.
4. РћСЃС‚Р°РІРёС‚СЊ `visual_regression.py` CLI wrapper.

РўРµСЃС‚С‹:
- `compileall`;
- `scripts/visual_regression.py`;
- `quality_gate.py --fast`.

Rollback:
- РµСЃР»Рё fallback РїРµСЂРµСЃС‚Р°Р» СЂР°Р±РѕС‚Р°С‚СЊ Р±РµР· screenshot backend, РѕС‚РєР°С‚РёС‚СЊ РїРµСЂРµРЅРѕСЃ backend boundary;
- Р»СЋР±С‹Рµ РёР·РјРµРЅРµРЅРёСЏ РєРѕР»РёС‡РµСЃС‚РІР° HTML files/checks С‚СЂРµР±СѓСЋС‚ review.

## 5. `scripts/quality_gate.py`

РўРµРєСѓС‰Р°СЏ СЂРѕР»СЊ: РµРґРёРЅР°СЏ С‚РѕС‡РєР° production QA, Р·Р°РїСѓСЃРєР°СЋС‰Р°СЏ py_compile, schema, regression, anomaly, smoke, HTML QA, visual regression, docs/charts/run manifest checks.

РџСЂРёС‡РёРЅС‹ РґРµРєРѕРјРїРѕР·РёС†РёРё:
- СЃРѕРґРµСЂР¶РёС‚ orchestration Рё РєРѕРЅРєСЂРµС‚РЅС‹Рµ РїСЂРѕРІРµСЂРєРё РІ РѕРґРЅРѕРј С„Р°Р№Р»Рµ;
- СЃРїРёСЃРѕРє РїСЂРѕРІРµСЂРѕРє Р±СѓРґРµС‚ СЂР°СЃС‚Рё;
- РѕС‚РґРµР»СЊРЅС‹Рµ checks Р»СѓС‡С€Рµ С‚РµСЃС‚РёСЂРѕРІР°С‚СЊ РЅРµР·Р°РІРёСЃРёРјРѕ.

Р РёСЃРєРё:
- РїРѕС‚РµСЂСЏ fail/warning semantics;
- РЅРµРїСЂР°РІРёР»СЊРЅС‹Р№ СЂРµР¶РёРј `--fast`/`--full`;
- РёР·РјРµРЅРµРЅРёРµ С„РѕСЂРјР°С‚Р° report.

Р—Р°РІРёСЃРёРјРѕСЃС‚Рё:
- РІСЃРµ QA scripts;
- `config.py`, `report_params.py`, `utils.py`;
- docs report paths.

РџСЂРµРґР»Р°РіР°РµРјР°СЏ target structure:

```text
scripts/qa/gate/core.py
scripts/qa/gate/script_checks.py
scripts/qa/gate/docs_checks.py
scripts/qa/gate/outputs_checks.py
scripts/qa/gate/dashboard_checks.py
```

РџРѕСЂСЏРґРѕРє Р±РµР·РѕРїР°СЃРЅРѕРіРѕ РїРµСЂРµРЅРѕСЃР°:
1. Р’С‹РЅРµСЃС‚Рё pure check functions Р±РµР· РёР·РјРµРЅРµРЅРёСЏ result model.
2. Р’С‹РЅРµСЃС‚Рё report rendering.
3. Р’С‹РЅРµСЃС‚Рё command runner helpers.
4. РћСЃС‚Р°РІРёС‚СЊ `quality_gate.py` CLI wrapper.

РўРµСЃС‚С‹:
- `compileall`;
- `ofz-quality --help`;
- `ofz-quality --fast ...`;
- fallback `scripts/quality_gate.py --fast ...`.

Rollback:
- РµСЃР»Рё `quality_gate_report.md` РјРµРЅСЏРµС‚ С„РѕСЂРјР°С‚ Р±РµР· РїР»Р°РЅРѕРІРѕРіРѕ РёР·РјРµРЅРµРЅРёСЏ, РѕС‚РєР°С‚РёС‚СЊ;
- РµСЃР»Рё СЃС‚Р°С‚СѓСЃ `warning/fail` РјРµРЅСЏРµС‚СЃСЏ Р±РµР· РёР·РјРµРЅРµРЅРёСЏ РґР°РЅРЅС‹С…, РѕС‚РєР°С‚РёС‚СЊ check extraction.

## 6. `scripts/07_dashboard_exports.py`

РўРµРєСѓС‰Р°СЏ СЂРѕР»СЊ: dashboard exports, supporting dictionaries, semantic/dashboard-ready datasets.

РџСЂРёС‡РёРЅС‹ РґРµРєРѕРјРїРѕР·РёС†РёРё:
- СЃРјРµС€РёРІР°РµС‚ export logic, transformations Рё documentation;
- РїРµСЂРµСЃРµРєР°РµС‚СЃСЏ РїРѕ СЃРјС‹СЃР»Сѓ СЃ semantic model v2;
- future dashboard changes РїСЂРѕС‰Рµ СЂР°Р·РІРёРІР°С‚СЊ РІ РѕС‚РґРµР»СЊРЅС‹С… modules.

Р РёСЃРєРё:
- РёР·РјРµРЅРµРЅРёРµ dashboard file names/schema;
- СЂР°СЃС…РѕР¶РґРµРЅРёРµ СЃ `dashboard_semantic_model_v2`;
- РЅР°СЂСѓС€РµРЅРёРµ BI contract.

Р—Р°РІРёСЃРёРјРѕСЃС‚Рё:
- report scope dataset;
- `config.py`, `report_params.py`, `utils.py`;
- `build_semantic_model_v2.py`;
- quality gate dashboard semantic checks.

РџСЂРµРґР»Р°РіР°РµРјР°СЏ target structure:

```text
scripts/stages/dashboard_exports.py
scripts/dashboard/export_tables.py
scripts/dashboard/semantic_helpers.py
scripts/dashboard/documentation.py
```

РџРѕСЂСЏРґРѕРє Р±РµР·РѕРїР°СЃРЅРѕРіРѕ РїРµСЂРµРЅРѕСЃР°:
1. Р’С‹РЅРµСЃС‚Рё pure field mapping helpers.
2. Р’С‹РЅРµСЃС‚Рё table export helpers.
3. Р’С‹РЅРµСЃС‚Рё documentation rendering.
4. РћСЃС‚Р°РІРёС‚СЊ СЃС‚Р°СЂС‹Р№ `07_dashboard_exports.py` wrapper.

РўРµСЃС‚С‹:
- `compileall`;
- `scripts/07_dashboard_exports.py`;
- `scripts/build_semantic_model_v2.py`;
- `quality_gate.py --fast`.

Rollback:
- РµСЃР»Рё dashboard exports РёР·РјРµРЅРёР»Рё СЃС…РµРјСѓ/РёРјРµРЅР° Р±РµР· РѕР¶РёРґР°РµРјРѕРіРѕ contract update, РѕС‚РєР°С‚РёС‚СЊ РїРµСЂРµРЅРѕСЃ;
- semantic model v2 РґРѕР»Р¶РµРЅ РѕСЃС‚Р°РІР°С‚СЊСЃСЏ РІР°Р»РёРґРЅС‹Рј РїРѕСЃР»Рµ РєР°Р¶РґРѕРіРѕ С€Р°РіР°.

## Release Criteria

Р”РµРєРѕРјРїРѕР·РёС†РёСЋ СЃС‡РёС‚Р°С‚СЊ РіРѕС‚РѕРІРѕР№ С‚РѕР»СЊРєРѕ РµСЃР»Рё:

- СЃС‚Р°СЂС‹Рµ РєРѕРјР°РЅРґС‹ РёР· README РїСЂРѕРґРѕР»Р¶Р°СЋС‚ СЂР°Р±РѕС‚Р°С‚СЊ;
- entry points РёР· `pyproject.toml` РїСЂРѕРґРѕР»Р¶Р°СЋС‚ СЂР°Р±РѕС‚Р°С‚СЊ;
- `compileall` РїСЂРѕС…РѕРґРёС‚;
- `quality_gate.py --fast` РїСЂРѕС…РѕРґРёС‚;
- generated output names РЅРµ РјРµРЅСЏСЋС‚СЃСЏ Р±РµР· РѕС‚РґРµР»СЊРЅРѕРіРѕ documented contract update;
- `scripts_inventory_before_cleanup.md` РѕР±РЅРѕРІР»РµРЅ РїРѕСЃР»Рµ С„Р°РєС‚РёС‡РµСЃРєРѕР№ РјРёРіСЂР°С†РёРё.

