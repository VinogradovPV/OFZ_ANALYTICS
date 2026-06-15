# scripts/

РџР°РїРєР° `scripts/` СЃРѕРґРµСЂР¶РёС‚ Python-first pipeline РїСЂРѕРµРєС‚Р° OFZ_ANALITICS: РѕС‚ С‡С‚РµРЅРёСЏ Рё РЅРѕСЂРјР°Р»РёР·Р°С†РёРё РёСЃС…РѕРґРЅС‹С… РґР°РЅРЅС‹С… РґРѕ РїРѕСЃС‚СЂРѕРµРЅРёСЏ РіСЂР°С„РёРєРѕРІ, Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёС… С‚Р°Р±Р»РёС†, dashboard-ready exports Рё РїСЂРѕРІРµСЂРѕРє РєР°С‡РµСЃС‚РІР°.

## РџРѕС‡РµРјСѓ СЃРєСЂРёРїС‚С‹ РїРѕРєР° РЅРµ РїРµСЂРµРЅРѕСЃСЏС‚СЃСЏ С„РёР·РёС‡РµСЃРєРё

РћСЃРЅРѕРІРЅС‹Рµ СЃРєСЂРёРїС‚С‹ РѕСЃС‚Р°СЋС‚СЃСЏ РІ РєРѕСЂРЅРµ `scripts/`, С‡С‚РѕР±С‹ РЅРµ Р»РѕРјР°С‚СЊ СЃСѓС‰РµСЃС‚РІСѓСЋС‰РёРµ РєРѕРјР°РЅРґС‹ Р·Р°РїСѓСЃРєР°, РёРјРїРѕСЂС‚С‹, `run_pipeline.py`, README Рё СЂСѓС‡РЅС‹Рµ РїСЂРѕРІРµСЂРєРё. РќР° С‚РµРєСѓС‰РµРј СЌС‚Р°РїРµ РІС‹РїРѕР»РЅРµРЅР° Р»РѕРіРёС‡РµСЃРєР°СЏ РєР»Р°СЃСЃРёС„РёРєР°С†РёСЏ Рё РЅР°РІРµРґРµРЅС‹ РїСЂР°РІРёР»Р° СЂР°Р·РјРµС‰РµРЅРёСЏ outputs/docs, РЅРѕ С„РёР·РёС‡РµСЃРєР°СЏ РјРёРіСЂР°С†РёСЏ Python-РјРѕРґСѓР»РµР№ РЅРµ РїСЂРѕРІРѕРґРёС‚СЃСЏ.

Р•СЃР»Рё РІ Р±СѓРґСѓС‰РµРј РїРѕРЅР°РґРѕР±РёС‚СЃСЏ РїРµСЂРµРЅРѕСЃРёС‚СЊ СЃРєСЂРёРїС‚С‹ РїРѕ РїРѕРґРїР°РїРєР°Рј, СЃРЅР°С‡Р°Р»Р° РЅСѓР¶РµРЅ РѕС‚РґРµР»СЊРЅС‹Р№ РїР»Р°РЅ РјРёРіСЂР°С†РёРё СЃ dry-run, РїСЂРѕРІРµСЂРєРѕР№ РёРјРїРѕСЂС‚РѕРІ Рё РѕР±СЂР°С‚РЅРѕР№ СЃРѕРІРјРµСЃС‚РёРјРѕСЃС‚СЊСЋ CLI.

## Р›РѕРіРёС‡РµСЃРєР°СЏ РєР»Р°СЃСЃРёС„РёРєР°С†РёСЏ

### Pipeline

- `run_pipeline.py` вЂ” РѕСЃРЅРѕРІРЅРѕР№ РѕСЂРєРµСЃС‚СЂР°С‚РѕСЂ СЌС‚Р°РїРѕРІ.
- `interactive_pipeline.py` вЂ” РёРЅС‚РµСЂР°РєС‚РёРІРЅС‹Р№ launcher РґР»СЏ СЂСѓС‡РЅРѕРіРѕ РІС‹Р±РѕСЂР° РїР°СЂР°РјРµС‚СЂРѕРІ.
- `report_params.py` вЂ” СЂР°СЃС‡РµС‚ РѕС‚С‡РµС‚РЅС‹С… РїРµСЂРёРѕРґРѕРІ Рё `aggregation_mode`.
- `period_filter.py` вЂ” С„РѕСЂРјРёСЂРѕРІР°РЅРёРµ `ofz_auctions_report_scope.csv`.

### Stages

- `01_data_audit.py` вЂ” Р°СѓРґРёС‚ РёСЃС…РѕРґРЅС‹С… С„Р°Р№Р»РѕРІ.
- `02_data_cleaning.py` вЂ” РѕС‡РёСЃС‚РєР° РґР°РЅРЅС‹С….
- `03_feature_engineering.py` вЂ” СЂР°СЃС‡РµС‚ РїСЂРёР·РЅР°РєРѕРІ Рё KPI-РїРѕР»РµР№.
- `04_kpi_map.py` вЂ” РєР°СЂС‚Р° KPI.
- `05_visualization_strategy.py` вЂ” РјРµС‚РѕРґРѕР»РѕРіРёСЏ РІРёР·СѓР°Р»РёР·Р°С†РёР№.
- `06_build_charts.py` вЂ” РѕСЃРЅРѕРІРЅС‹Рµ HTML-РіСЂР°С„РёРєРё.
- `07_dashboard_exports.py` вЂ” dashboard-ready exports.
- `08_analytical_tables.py` вЂ” РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёРµ С‚Р°Р±Р»РёС†С‹.
- `09_monthly_analytics.py` вЂ” monthly layer.
- `10_build_monthly_charts.py` вЂ” РїРѕРјРµСЃСЏС‡РЅС‹Рµ РіСЂР°С„РёРєРё.
- `11_revenue_analytics.py` вЂ” Р°РЅР°Р»РёС‚РёРєР° РІС‹СЂСѓС‡РєРё.
- `12_build_revenue_charts.py` вЂ” РіСЂР°С„РёРєРё РїРѕ РІС‹СЂСѓС‡РєРµ.
- `generate_executive_summary.py` вЂ” РїР°СЂР°РјРµС‚СЂРёР·СѓРµРјРѕРµ executive summary.
- `build_semantic_model_v2.py` вЂ” semantic model v2.

### QA

- `quality_gate.py` вЂ” РµРґРёРЅС‹Р№ quality gate.
- `schema_validation.py` вЂ” РїСЂРѕРІРµСЂРєР° СЃС…РµРјС‹ Рё РєРѕРЅС‚СЂР°РєС‚РѕРІ РґР°РЅРЅС‹С….
- `regression_tests.py` вЂ” СЂРµРіСЂРµСЃСЃРёРѕРЅРЅС‹Рµ С‚РµСЃС‚С‹ РїРµСЂРёРѕРґРЅРѕР№ Р»РѕРіРёРєРё Рё edge cases.
- `smoke_tests.py` вЂ” smoke tests pipeline outputs.
- `html_chart_qa.py` вЂ” QA HTML-РіСЂР°С„РёРєРѕРІ.
- `visual_regression.py` вЂ” visual regression РёР»Рё fallback HTML/Plotly inspection.
- `anomaly_tests.py` вЂ” РїСЂРѕРІРµСЂРєРё Р°РЅРѕРјР°Р»РёР№ РґР°РЅРЅС‹С….

### Metadata

- `run_manifest.py` вЂ” run manifest.
- `raw_data_registry.py` вЂ” registry РёСЃС…РѕРґРЅС‹С… С„Р°Р№Р»РѕРІ Р±РµР· РёР·РјРµРЅРµРЅРёСЏ `data/raw/`.

### Utils

- `config.py` вЂ” С†РµРЅС‚СЂР°Р»РёР·РѕРІР°РЅРЅС‹Рµ РїСѓС‚Рё Рё routing helper-С„СѓРЅРєС†РёРё.
- `utils.py` вЂ” РѕР±С‰РёРµ С„СѓРЅРєС†РёРё С‡С‚РµРЅРёСЏ/Р·Р°РїРёСЃРё, Р»РѕРіРёСЂРѕРІР°РЅРёСЏ Рё РЅРѕСЂРјР°Р»РёР·Р°С†РёРё.
- `palette.py` вЂ” С†РІРµС‚РѕРІС‹Рµ РїР°Р»РёС‚СЂС‹.
- `scatter_chart_policy.py` вЂ” РїРѕР»РёС‚РёРєР° РїРѕРґРїРёСЃРµР№ scatter-РіСЂР°С„РёРєРѕРІ.
- `compare_outputs.py` вЂ” СЃСЂР°РІРЅРµРЅРёРµ outputs.

### Maintenance

- `maintenance/cleanup_outputs.py` - production-safe cleanup generated outputs.
- `maintenance/cleanup_docs.py` - inventory-first docs cleanup workflow.
- `maintenance/build_release_bundle.py` - external release bundle builder.
- `maintenance/reorganize_charts.py` - HTML charts reorganization helper.
- `archive/2026-06-15/` - legacy maintenance scripts kept for audit only; do not use for production runs.

## РћСЃРЅРѕРІРЅС‹Рµ entry points

РџРѕР»РЅС‹Р№ Р·Р°РїСѓСЃРє:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

РРЅС‚РµСЂР°РєС‚РёРІРЅС‹Р№ Р·Р°РїСѓСЃРє:

```powershell
.\.venv\Scripts\python.exe scripts\interactive_pipeline.py
```

Quality gate:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Visual regression / fallback HTML inspection:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Run manifest:

```powershell
.\.venv\Scripts\python.exe scripts\run_manifest.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --stages all
```

## РџСЂР°РІРёР»Р° РґР»СЏ markdown-РґРѕРєСѓРјРµРЅС‚РѕРІ

РќРѕРІС‹Рµ `.md`-РґРѕРєСѓРјРµРЅС‚С‹ РЅРµР»СЊР·СЏ СЃРѕС…СЂР°РЅСЏС‚СЊ РЅР°РїСЂСЏРјСѓСЋ РІ РєРѕСЂРµРЅСЊ `docs/`. Р•РґРёРЅСЃС‚РІРµРЅРЅРѕРµ РёСЃРєР»СЋС‡РµРЅРёРµ: `docs/index.md`.

РСЃРїРѕР»СЊР·СѓР№С‚Рµ С†РµРЅС‚СЂР°Р»РёР·РѕРІР°РЅРЅС‹Р№ helper:

```python
from scripts import config

target_path = config.get_doc_path("quality_gate_report.md")
```

Р”РѕРєСѓРјРµРЅС‚С‹ РґРѕР»Р¶РЅС‹ РїРѕРїР°РґР°С‚СЊ РІ С‚РµРјР°С‚РёС‡РµСЃРєРёРµ РїР°РїРєРё:

- `docs/00_project/`;
- `docs/01_methodology/`;
- `docs/02_data_pipeline/`;
- `docs/03_analytics/`;
- `docs/04_visualization/`;
- `docs/05_dashboard/`;
- `docs/06_quality/`;
- `docs/90_archive/`.

## РџСЂР°РІРёР»Р° РґР»СЏ HTML-РіСЂР°С„РёРєРѕРІ

РќРѕРІС‹Рµ HTML-РіСЂР°С„РёРєРё РЅРµР»СЊР·СЏ СЃРѕС…СЂР°РЅСЏС‚СЊ РЅР°РїСЂСЏРјСѓСЋ РІ РєРѕСЂРµРЅСЊ `outputs/charts/`.

РСЃРїРѕР»СЊР·СѓР№С‚Рµ:

```python
html_dir = config.chart_html_dir_for_name(chart_name)
```

РРЅРґРµРєСЃ РіСЂР°С„РёРєРѕРІ РїРѕРґРґРµСЂР¶РёРІР°РµС‚СЃСЏ РІ `outputs/charts/index.md`.
