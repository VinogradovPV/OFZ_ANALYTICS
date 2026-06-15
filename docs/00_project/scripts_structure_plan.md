# Scripts Structure Plan

Р”РѕРєСѓРјРµРЅС‚ С„РёРєСЃРёСЂСѓРµС‚ С‚РµРєСѓС‰СѓСЋ Р»РѕРіРёС‡РµСЃРєСѓСЋ СЃС‚СЂСѓРєС‚СѓСЂСѓ РїР°РїРєРё `scripts/` РїРѕСЃР»Рµ РІС‚РѕСЂРѕР№ РјРѕРґРµСЂРЅРёР·Р°С†РёРё РїСЂРѕРµРєС‚Р° OFZ_ANALITICS. Р¤РёР·РёС‡РµСЃРєРёР№ РїРµСЂРµРЅРѕСЃ РѕСЃРЅРѕРІРЅС‹С… СЃРєСЂРёРїС‚РѕРІ СЃРµР№С‡Р°СЃ РЅРµ РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ: РґРµР№СЃС‚РІСѓСЋС‰РёРµ CLI-РєРѕРјР°РЅРґС‹, РёРјРїРѕСЂС‚С‹ Рё `run_pipeline.py` СЃРѕС…СЂР°РЅСЏСЋС‚ РѕР±СЂР°С‚РЅСѓСЋ СЃРѕРІРјРµСЃС‚РёРјРѕСЃС‚СЊ.

## Pipeline

- `run_pipeline.py` вЂ” РѕСЃРЅРѕРІРЅРѕР№ РѕСЂРєРµСЃС‚СЂР°С‚РѕСЂ СЌС‚Р°РїРѕРІ pipeline.
- `interactive_pipeline.py` вЂ” РёРЅС‚РµСЂР°РєС‚РёРІРЅС‹Р№ launcher РґР»СЏ РІС‹Р±РѕСЂР° РїР°СЂР°РјРµС‚СЂРѕРІ Р·Р°РїСѓСЃРєР°.
- `report_params.py` вЂ” СЂР°СЃС‡РµС‚ РѕС‚С‡РµС‚РЅС‹С… РїРµСЂРёРѕРґРѕРІ, СЂРµС‚СЂРѕСЃРїРµРєС‚РёРІС‹ Рё `aggregation_mode`.
- `period_filter.py` вЂ” С„РѕСЂРјРёСЂРѕРІР°РЅРёРµ `data/processed/ofz_auctions_report_scope.csv`.

## Stages

- `01_data_audit.py` вЂ” Р°СѓРґРёС‚ РёСЃС…РѕРґРЅС‹С… С„Р°Р№Р»РѕРІ.
- `02_data_cleaning.py` вЂ” РѕС‡РёСЃС‚РєР° Рё РЅРѕСЂРјР°Р»РёР·Р°С†РёСЏ РґР°РЅРЅС‹С….
- `03_feature_engineering.py` вЂ” СЂР°СЃС‡РµС‚ РїСЂРёР·РЅР°РєРѕРІ, СЃСЂРѕРєРѕРІС‹С… РєР°С‚РµРіРѕСЂРёР№ Рё ratio-РїРѕРєР°Р·Р°С‚РµР»РµР№.
- `04_kpi_map.py` вЂ” РєР°СЂС‚Р° KPI.
- `05_visualization_strategy.py` вЂ” РјРµС‚РѕРґРѕР»РѕРіРёСЏ РІРёР·СѓР°Р»РёР·Р°С†РёР№.
- `06_build_charts.py` вЂ” РѕСЃРЅРѕРІРЅС‹Рµ HTML-РіСЂР°С„РёРєРё.
- `07_dashboard_exports.py` вЂ” dashboard-ready exports.
- `08_analytical_tables.py` вЂ” РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёРµ С‚Р°Р±Р»РёС†С‹.
- `09_monthly_analytics.py` вЂ” monthly layer.
- `10_build_monthly_charts.py` вЂ” РїРѕРјРµСЃСЏС‡РЅС‹Рµ РІРёР·СѓР°Р»РёР·Р°С†РёРё.
- `11_revenue_analytics.py` вЂ” Р°РЅР°Р»РёС‚РёРєР° РІС‹СЂСѓС‡РєРё.
- `12_build_revenue_charts.py` вЂ” РіСЂР°С„РёРєРё РїРѕ РІС‹СЂСѓС‡РєРµ.
- `generate_executive_summary.py` вЂ” РїР°СЂР°РјРµС‚СЂРёР·СѓРµРјРѕРµ executive summary.
- `build_semantic_model_v2.py` вЂ” semantic model v2.

## QA

- `quality_gate.py` вЂ” РµРґРёРЅС‹Р№ quality gate.
- `schema_validation.py` вЂ” РїСЂРѕРІРµСЂРєР° СЃС…РµРјС‹ Рё РєРѕРЅС‚СЂР°РєС‚РѕРІ РґР°РЅРЅС‹С….
- `regression_tests.py` вЂ” СЂРµРіСЂРµСЃСЃРёРѕРЅРЅС‹Рµ С‚РµСЃС‚С‹ РїРµСЂРёРѕРґРЅРѕР№ Р»РѕРіРёРєРё Рё edge cases.
- `smoke_tests.py` вЂ” smoke tests РєР»СЋС‡РµРІС‹С… outputs.
- `html_chart_qa.py` вЂ” QA HTML-РіСЂР°С„РёРєРѕРІ.
- `visual_regression.py` вЂ” visual regression РёР»Рё fallback HTML/Plotly inspection.
- `anomaly_tests.py` вЂ” РїСЂРѕРІРµСЂРєРё Р°РЅРѕРјР°Р»РёР№ РґР°РЅРЅС‹С….

## Metadata

- `run_manifest.py` вЂ” run manifest.
- `raw_data_registry.py` вЂ” registry РёСЃС…РѕРґРЅС‹С… С„Р°Р№Р»РѕРІ Р±РµР· РёР·РјРµРЅРµРЅРёСЏ `data/raw/`.

## Utils

- `config.py` вЂ” С†РµРЅС‚СЂР°Р»РёР·РѕРІР°РЅРЅС‹Рµ РїСѓС‚Рё, `get_doc_path()` Рё `chart_html_dir_for_name()`.
- `utils.py` вЂ” РѕР±С‰РёРµ С„СѓРЅРєС†РёРё С‡С‚РµРЅРёСЏ, Р·Р°РїРёСЃРё, Р»РѕРіРёСЂРѕРІР°РЅРёСЏ Рё РЅРѕСЂРјР°Р»РёР·Р°С†РёРё.
- `palette.py` вЂ” С†РІРµС‚РѕРІС‹Рµ РїР°Р»РёС‚СЂС‹.
- `scatter_chart_policy.py` вЂ” РїРѕР»РёС‚РёРєР° РїРѕРґРїРёСЃРµР№ scatter-РіСЂР°С„РёРєРѕРІ.
- `compare_outputs.py` вЂ” СЃСЂР°РІРЅРµРЅРёРµ outputs.
- `__init__.py` вЂ” РїР°РєРµС‚РЅР°СЏ РёРЅРёС†РёР°Р»РёР·Р°С†РёСЏ `scripts`.

## Maintenance

- `archive/2026-06-15/cleanup_docs.py` вЂ” legacy-РѕС‡РёСЃС‚РєР° docs.
- `archive/2026-06-15/reorganize_outputs.py` вЂ” СЂРµРѕСЂРіР°РЅРёР·Р°С†РёСЏ outputs/exports.
- `archive/2026-06-15/migrate_outputs_structure.py` вЂ” РјРёРіСЂР°С†РёСЏ СЃС‚СЂСѓРєС‚СѓСЂС‹ outputs.
- `archive/2026-06-15/reorganize_docs.py` вЂ” Р±РµР·РѕРїР°СЃРЅР°СЏ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёСЏ docs.
- `maintenance/reorganize_charts.py` вЂ” Р±РµР·РѕРїР°СЃРЅР°СЏ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёСЏ HTML-РіСЂР°С„РёРєРѕРІ.
- `archive/2026-06-15/migrate_legacy_docs_archive.py` вЂ” РїРµСЂРµРЅРѕСЃ СЃС‚Р°СЂРѕРіРѕ `docs/archive/`.
- `maintenance/__init__.py` вЂ” РїР°РєРµС‚РЅР°СЏ РёРЅРёС†РёР°Р»РёР·Р°С†РёСЏ maintenance.

