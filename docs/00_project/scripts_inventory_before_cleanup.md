# Scripts inventory before cleanup

- generated_at: `2026-06-08`
- cleanup mode: `audit only`
- physical moves: `none`
- scope: `scripts/**/*.py`

Р­С‚РѕС‚ РґРѕРєСѓРјРµРЅС‚ С„РёРєСЃРёСЂСѓРµС‚ P1-Р°СѓРґРёС‚ `scripts/` РїРµСЂРµРґ РІРѕР·РјРѕР¶РЅРѕР№ Р±СѓРґСѓС‰РµР№ СЃС‚СЂСѓРєС‚СѓСЂРЅРѕР№ РѕС‡РёСЃС‚РєРѕР№. РќР° СЌС‚РѕРј СЌС‚Р°РїРµ Python-С„Р°Р№Р»С‹ С„РёР·РёС‡РµСЃРєРё РЅРµ РїРµСЂРµРЅРѕСЃСЏС‚СЃСЏ: С‚РµРєСѓС‰РёРµ CLI-РєРѕРјР°РЅРґС‹, imports, `run_pipeline.py`, editable entry points Рё СЂСѓС‡РЅС‹Рµ production-РёРЅСЃС‚СЂСѓРєС†РёРё РґРѕР»Р¶РЅС‹ РѕСЃС‚Р°РІР°С‚СЊСЃСЏ СЃС‚Р°Р±РёР»СЊРЅС‹РјРё.

## Summary

| РљР°С‚РµРіРѕСЂРёСЏ | РљРѕР»РёС‡РµСЃС‚РІРѕ |
|---|---:|
| Р’СЃРµРіРѕ Python-С„Р°Р№Р»РѕРІ | 42 |
| `keep_active` | 32 |
| `refactor_candidate` | 5 |
| `archive_candidate` | 5 |
| `delete_candidate` | 0 |
| `unknown` РґР»СЏ СЂСѓС‡РЅРѕР№ РїСЂРѕРІРµСЂРєРё | 0 |

## No-touch active scripts

Р­С‚Рё С„Р°Р№Р»С‹ РЅРµ РїРµСЂРµРЅРѕСЃРёС‚СЊ Рё РЅРµ Р°СЂС…РёРІРёСЂРѕРІР°С‚СЊ РЅР° production-cleanup СЌС‚Р°РїРµ Р±РµР· РѕС‚РґРµР»СЊРЅРѕРіРѕ migration plan Рё compatibility wrappers.

- `scripts/run_pipeline.py`
- `scripts/interactive_pipeline.py`
- `scripts/report_params.py`
- `scripts/period_filter.py`
- `scripts/config.py`
- `scripts/utils.py`
- `scripts/01_data_audit.py`
- `scripts/02_data_cleaning.py`
- `scripts/03_feature_engineering.py`
- `scripts/04_kpi_map.py`
- `scripts/05_visualization_strategy.py`
- `scripts/06_build_charts.py`
- `scripts/07_dashboard_exports.py`
- `scripts/08_analytical_tables.py`
- `scripts/09_monthly_analytics.py`
- `scripts/10_build_monthly_charts.py`
- `scripts/11_revenue_analytics.py`
- `scripts/12_build_revenue_charts.py`
- `scripts/generate_executive_summary.py`
- `scripts/build_semantic_model_v2.py`
- `scripts/run_manifest.py`
- `scripts/raw_data_registry.py`
- `scripts/quality_gate.py`
- `scripts/schema_validation.py`
- `scripts/html_chart_qa.py`
- `scripts/visual_regression.py`
- `scripts/smoke_tests.py`
- `scripts/regression_tests.py`
- `scripts/anomaly_tests.py`
- `scripts/palette.py`
- `scripts/scatter_chart_policy.py`
- `scripts/__init__.py`

## Refactor candidates

Р­С‚Рё С„Р°Р№Р»С‹ Р°РєС‚РёРІРЅС‹ РёР»Рё РїРѕР»РµР·РЅС‹, РЅРѕ РёС… СЃС‚РѕРёС‚ СЂР°СЃСЃРјРѕС‚СЂРµС‚СЊ РґР»СЏ Р±СѓРґСѓС‰РµР№ РјРѕРґСѓР»СЊРЅРѕР№ РґРµРєРѕРјРїРѕР·РёС†РёРё. РЎРµР№С‡Р°СЃ РЅРµ РїРµСЂРµРЅРѕСЃРёС‚СЊ.

- `scripts/06_build_charts.py` - РѕС‡РµРЅСЊ РєСЂСѓРїРЅС‹Р№ CLI/stage script; РєР°РЅРґРёРґР°С‚ РЅР° СЂР°Р·Р±РёРµРЅРёРµ РЅР° chart family modules.
- `scripts/html_chart_qa.py` - РєСЂСѓРїРЅС‹Р№ QA script; РєР°РЅРґРёРґР°С‚ РЅР° СЂР°Р·РґРµР»РµРЅРёРµ РєРѕРЅС‚СЂР°РєС‚РѕРІ РїРѕ СЃРµРјРµР№СЃС‚РІР°Рј РіСЂР°С„РёРєРѕРІ.
- `scripts/visual_regression.py` - РєСЂСѓРїРЅС‹Р№ fallback QA script; РєР°РЅРґРёРґР°С‚ РЅР° СЂР°Р·РґРµР»РµРЅРёРµ Plotly JSON checks Рё screenshot backend.
- `scripts/10_build_monthly_charts.py` - РєСЂСѓРїРЅС‹Р№ monthly chart builder; РєР°РЅРґРёРґР°С‚ РЅР° СЂР°Р·РґРµР»РµРЅРёРµ bar/line/heatmap/facet logic.
- `scripts/07_dashboard_exports.py` - РєСЂСѓРїРЅС‹Р№ dashboard exporter; РєР°РЅРґРёРґР°С‚ РЅР° РІС‹РґРµР»РµРЅРёРµ semantic/export helpers.

## Archive candidates

Р­С‚Рё С„Р°Р№Р»С‹ РѕС‚РЅРѕСЃСЏС‚СЃСЏ Рє legacy/reorganization maintenance Рё РЅРµ РґРѕР»Р¶РЅС‹ РІС‹Р·С‹РІР°С‚СЊСЃСЏ production pipeline. РђСЂС…РёРІРёСЂРѕРІР°РЅРёРµ РґРѕРїСѓСЃС‚РёРјРѕ С‚РѕР»СЊРєРѕ РѕС‚РґРµР»СЊРЅС‹Рј СЌС‚Р°РїРѕРј РїРѕСЃР»Рµ РїСЂРѕРІРµСЂРєРё СЃСЃС‹Р»РѕРє РІ README/docs.

- `scripts/archive/2026-06-15/cleanup_docs.py` - legacy cleanup script РґР»СЏ СЃС‚Р°СЂРѕР№ СЃС‚СЂСѓРєС‚СѓСЂС‹ docs; Р·Р°РјРµРЅРµРЅ production workflow `scripts/maintenance/cleanup_docs.py`.
- `scripts/archive/2026-06-15/migrate_outputs_structure.py` - РѕРґРЅРѕСЂР°Р·РѕРІР°СЏ migration utility СЃС‚Р°СЂРѕР№ СЃС‚СЂСѓРєС‚СѓСЂС‹ outputs.
- `scripts/archive/2026-06-15/reorganize_outputs.py` - legacy reorganization utility РґР»СЏ outputs/exports.
- `scripts/archive/2026-06-15/migrate_legacy_docs_archive.py` - РѕРґРЅРѕСЂР°Р·РѕРІС‹Р№ РїРµСЂРµРЅРѕСЃ СЃС‚Р°СЂРѕРіРѕ docs/archive.
- `scripts/archive/2026-06-15/reorganize_docs.py` - reorganization utility РїСЂРµРґС‹РґСѓС‰РµРіРѕ СЌС‚Р°РїР°; РјРѕР¶РµС‚ РѕСЃС‚Р°РІР°С‚СЊСЃСЏ РєР°Рє historical maintenance РґРѕ С„РёРЅР°Р»СЊРЅРѕРіРѕ archive decision.

## Unknown scripts for manual review

РќРµС‚. Р’СЃРµ Python-С„Р°Р№Р»С‹ РєР»Р°СЃСЃРёС„РёС†РёСЂРѕРІР°РЅС‹ РєР°Рє active, refactor candidate РёР»Рё archive candidate.

## Inventory

| Path | Size bytes | РќР°Р·РЅР°С‡РµРЅРёРµ | РўРёРї | Run pipeline | Quality gate | Imported by scripts | main() | argparse | Status | Reason |
|---|---:|---|---|---|---|---|---|---|---|---|
| `scripts/__init__.py` | 113 | Package marker РґР»СЏ editable install Рё imports `scripts.*`. | library | no | no | yes | no | no | `keep_active` | РќСѓР¶РµРЅ РґР»СЏ package layout Рё entry points. |
| `scripts/01_data_audit.py` | 24035 | Р­С‚Р°Рї 1: Р°СѓРґРёС‚ РёСЃС…РѕРґРЅС‹С… Excel/CSV. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ stage script, РІС…РѕРґРёС‚ РІ `run_pipeline.py` Рё `quality_gate.py`. |
| `scripts/02_data_cleaning.py` | 24381 | Р­С‚Р°Рї 2: РѕС‡РёСЃС‚РєР° РёСЃС…РѕРґРЅС‹С… РґР°РЅРЅС‹С…. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ stage script, РІС…РѕРґРёС‚ РІ `run_pipeline.py` Рё `quality_gate.py`. |
| `scripts/03_feature_engineering.py` | 28534 | Р­С‚Р°Рї 3: СЂР°СЃС‡РµС‚ РїСЂРёР·РЅР°РєРѕРІ Рё KPI-РїРѕР»РµР№. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ stage script, РІС…РѕРґРёС‚ РІ `run_pipeline.py` Рё `quality_gate.py`. |
| `scripts/04_kpi_map.py` | 17679 | Р­С‚Р°Рї 5: РєР°СЂС‚Р° KPI Рё РјРµС‚РѕРґРѕР»РѕРіРёС‡РµСЃРєРёР№ РґРѕРєСѓРјРµРЅС‚. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ stage script, РІС…РѕРґРёС‚ РІ `run_pipeline.py` Рё `quality_gate.py`. |
| `scripts/05_visualization_strategy.py` | 20365 | Р­С‚Р°Рї 7: СЃС‚СЂР°С‚РµРіРёСЏ РІРёР·СѓР°Р»РёР·Р°С†РёР№. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ stage script, РІС…РѕРґРёС‚ РІ `run_pipeline.py` Рё `quality_gate.py`. |
| `scripts/06_build_charts.py` | 339363 | РћСЃРЅРѕРІРЅС‹Рµ HTML-РіСЂР°С„РёРєРё, risk/scatter/structure/format terms. | CLI entry | yes | py_compile | yes | yes | no | `refactor_candidate` | РђРєС‚РёРІРЅС‹Р№ stage script, РЅРѕ СЃР°РјС‹Р№ РєСЂСѓРїРЅС‹Р№ С„Р°Р№Р»; Р±СѓРґСѓС‰Р°СЏ РґРµРєРѕРјРїРѕР·РёС†РёСЏ Р¶РµР»Р°С‚РµР»СЊРЅР° Р±РµР· С„РёР·РёС‡РµСЃРєРѕРіРѕ РїРµСЂРµРЅРѕСЃР° СЃРµР№С‡Р°СЃ. |
| `scripts/07_dashboard_exports.py` | 70630 | Dashboard-ready exports Рё СЃРІСЏР·Р°РЅРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹. | CLI entry | yes | py_compile | yes | yes | no | `refactor_candidate` | РђРєС‚РёРІРЅС‹Р№ stage script; СЂР°Р·РјРµСЂ Рё semantic/export mix РґРµР»Р°СЋС‚ РµРіРѕ РєР°РЅРґРёРґР°С‚РѕРј РЅР° РґРµРєРѕРјРїРѕР·РёС†РёСЋ. |
| `scripts/08_analytical_tables.py` | 32701 | РћР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёРµ С‚Р°Р±Р»РёС†С‹ Рё CSV. | CLI entry | yes | no | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ stage script, РІС‹Р·С‹РІР°РµС‚СЃСЏ pipeline. |
| `scripts/09_monthly_analytics.py` | 29397 | Monthly metrics layer. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ monthly stage script. |
| `scripts/10_build_monthly_charts.py` | 87172 | Monthly HTML-РіСЂР°С„РёРєРё, facet/heatmap/monthly chart data. | CLI entry | yes | py_compile | yes | yes | no | `refactor_candidate` | РђРєС‚РёРІРЅС‹Р№ monthly stage script; СЂР°Р·РјРµСЂ Рё СЂР°Р·РЅС‹Рµ chart families С‚СЂРµР±СѓСЋС‚ Р±СѓРґСѓС‰РµР№ РјРѕРґСѓР»СЊРЅРѕР№ РґРµРєРѕРјРїРѕР·РёС†РёРё. |
| `scripts/11_revenue_analytics.py` | 18592 | Revenue analytics tables. | CLI entry | yes | no | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ revenue stage script. |
| `scripts/12_build_revenue_charts.py` | 32785 | Revenue charts. | CLI entry | yes | no | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ revenue chart stage script. |
| `scripts/anomaly_tests.py` | 19269 | РџСЂРѕРІРµСЂРєРё Р°РЅРѕРјР°Р»РёР№ РґР°РЅРЅС‹С…. | quality | yes | optional/runtime | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ QA script, РІС‹Р·С‹РІР°РµС‚СЃСЏ pipeline stage Рё quality gate РїСЂРё РЅР°Р»РёС‡РёРё. |
| `scripts/build_semantic_model_v2.py` | 21512 | Dashboard semantic model v2. | CLI entry | yes | no | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ stage script РґР»СЏ semantic model v2. |
| `scripts/archive/2026-06-15/cleanup_docs.py` | 12243 | Legacy cleanup docs РґР»СЏ СЃС‚Р°СЂРѕР№ РєРѕСЂРЅРµРІРѕР№ СЃС‚СЂСѓРєС‚СѓСЂС‹ docs. | maintenance | no | no | no | yes | no | `archive_candidate` | Р—Р°РјРµРЅРµРЅ `scripts/maintenance/cleanup_docs.py`; РЅРµ Р·Р°РїСѓСЃРєР°С‚СЊ РІ production cleanup Р±РµР· РѕС‚РґРµР»СЊРЅРѕРіРѕ СЂРµС€РµРЅРёСЏ. |
| `scripts/compare_outputs.py` | 7752 | РЎСЂР°РІРЅРµРЅРёРµ main/repro outputs РґР»СЏ safe/compare СЂРµР¶РёРјР°. | quality | yes | no | yes | yes | yes | `keep_active` | РСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ `run_pipeline.py` РїСЂРё `--safe`/`--compare`. |
| `scripts/config.py` | 22450 | Р¦РµРЅС‚СЂР°Р»РёР·РѕРІР°РЅРЅС‹Рµ РїСѓС‚Рё, docs routing, chart routing. | library | no | import | yes | no | no | `keep_active` | Р‘Р°Р·РѕРІР°СЏ library РґР»СЏ Р±РѕР»СЊС€РёРЅСЃС‚РІР° scripts; no-touch. |
| `scripts/generate_executive_summary.py` | 34298 | Executive summary РїРѕ СЂР°СЃС‡РµС‚РЅС‹Рј РїРѕРєР°Р·Р°С‚РµР»СЏРј. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ stage script, РІС…РѕРґРёС‚ РІ `run_pipeline.py` Рё `quality_gate.py`. |
| `scripts/html_chart_qa.py` | 113969 | HTML/Plotly QA РєРѕРЅС‚СЂР°РєС‚ РіСЂР°С„РёРєРѕРІ. | quality | no | runtime | yes | yes | yes | `refactor_candidate` | РђРєС‚РёРІРЅС‹Р№ QA script, РІС‹Р·С‹РІР°РµС‚СЃСЏ quality gate; РєСЂСѓРїРЅС‹Р№ С„Р°Р№Р» РґР»СЏ Р±СѓРґСѓС‰РµРіРѕ СЂР°Р·Р±РёРµРЅРёСЏ РїРѕ РєРѕРЅС‚СЂР°РєС‚Р°Рј. |
| `scripts/interactive_pipeline.py` | 16519 | РРЅС‚РµСЂР°РєС‚РёРІРЅС‹Р№ launcher СЃ cleanup pre-flight. | CLI entry | no | no | entry point | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ CLI entry point `ofz-interactive`; no-touch. |
| `scripts/maintenance/__init__.py` | 83 | Package marker РґР»СЏ maintenance entry points. | library | no | no | yes | no | no | `keep_active` | РќСѓР¶РµРЅ РґР»СЏ `scripts.maintenance.*` imports Рё entry points. |
| `scripts/maintenance/cleanup_docs.py` | 18528 | Inventory-first docs cleanup workflow. | maintenance | no | no | no | yes | yes | `keep_active` | РќРѕРІС‹Р№ production maintenance script; dry-run/archive/delete-archived modes. |
| `scripts/maintenance/cleanup_outputs.py` | 11917 | Safe outputs cleanup. | maintenance | no | entry/help | yes | yes | yes | `keep_active` | РђРєС‚РёРІРЅС‹Р№ maintenance CLI, РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ interactive launcher Рё entry point `ofz-clean-outputs`. |
| `scripts/archive/2026-06-15/migrate_legacy_docs_archive.py` | 8578 | РњРёРіСЂР°С†РёСЏ СЃС‚Р°СЂРѕРіРѕ docs/archive РІ РЅРѕРІСѓСЋ СЃС‚СЂСѓРєС‚СѓСЂСѓ. | maintenance | no | no | no | yes | yes | `archive_candidate` | РћРґРЅРѕСЂР°Р·РѕРІР°СЏ legacy migration utility; РѕСЃС‚Р°РІРёС‚СЊ РґРѕ РѕС‚РґРµР»СЊРЅРѕРіРѕ archive decision. |
| `scripts/maintenance/reorganize_charts.py` | 16627 | Dry-run/apply СЂРµРѕСЂРіР°РЅРёР·Р°С†РёСЏ HTML charts. | maintenance | no | no | no | yes | yes | `keep_active` | РџРѕР»РµР·РЅС‹Р№ maintenance script РґР»СЏ chart routing cleanup; РѕСЃС‚Р°РІР»РµРЅ Р°РєС‚РёРІРЅС‹Рј. |
| `scripts/archive/2026-06-15/reorganize_docs.py` | 12059 | Dry-run/apply СЂРµРѕСЂРіР°РЅРёР·Р°С†РёСЏ markdown docs. | maintenance | no | no | no | yes | yes | `archive_candidate` | РСЃС‚РѕСЂРёС‡РµСЃРєРёР№ reorganization utility; РЅРѕРІС‹Р№ production cleanup workflow С‚РµРїРµСЂСЊ РІ `maintenance/cleanup_docs.py`. |
| `scripts/archive/2026-06-15/migrate_outputs_structure.py` | 10185 | Legacy migration СЃС‚СЂСѓРєС‚СѓСЂС‹ outputs. | maintenance | no | no | no | yes | no | `archive_candidate` | РћРґРЅРѕСЂР°Р·РѕРІС‹Р№ migration script; production pipeline РЅРµ РІС‹Р·С‹РІР°РµС‚. |
| `scripts/palette.py` | 3508 | Р¦РІРµС‚РѕРІС‹Рµ РїР°Р»РёС‚СЂС‹ Рё semantic colors. | library | no | py_compile | yes | no | no | `keep_active` | РђРєС‚РёРІРЅР°СЏ library РґР»СЏ chart builders Рё QA; РІС…РѕРґРёС‚ РІ `quality_gate.py` key scripts. |
| `scripts/period_filter.py` | 9650 | Report scope dataset РїРѕ РїР°СЂР°РјРµС‚СЂР°Рј РїРµСЂРёРѕРґР°. | CLI entry | yes | py_compile | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ stage script, РІС…РѕРґРёС‚ РІ `run_pipeline.py` Рё `quality_gate.py`. |
| `scripts/quality_gate.py` | 26751 | Р•РґРёРЅС‹Р№ fast/full quality gate. | quality | yes | entry | yes | yes | yes | `keep_active` | РђРєС‚РёРІРЅС‹Р№ QA entry point, С‚Р°РєР¶Рµ pipeline stage. |
| `scripts/raw_data_registry.py` | 7878 | Raw data registry Рё hashes Р±РµР· РёР·РјРµРЅРµРЅРёСЏ `data/raw`. | CLI entry | no | py_compile | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ metadata/QA helper, РІС…РѕРґРёС‚ РІ key scripts quality gate. |
| `scripts/regression_tests.py` | 14573 | Regression tests РґР»СЏ РїРµСЂРёРѕРґРЅРѕР№ Р»РѕРіРёРєРё Рё edge cases. | quality | no | runtime | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ QA script, РІС‹Р·С‹РІР°РµС‚СЃСЏ quality gate. |
| `scripts/archive/2026-06-15/reorganize_outputs.py` | 12354 | Legacy reorganization outputs/exports. | maintenance | no | no | no | yes | yes | `archive_candidate` | РСЃС‚РѕСЂРёС‡РµСЃРєРёР№ utility РїРѕСЃР»Рµ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё outputs; РЅРµ production path. |
| `scripts/report_params.py` | 14134 | РџР°СЂР°РјРµС‚СЂС‹ РѕС‚С‡РµС‚РЅС‹С… РїРµСЂРёРѕРґРѕРІ Рё CLI parser helpers. | library | no | py_compile | yes | no | yes | `keep_active` | Р¦РµРЅС‚СЂР°Р»СЊРЅР°СЏ library РґР»СЏ pipeline, QA Рё chart scripts. |
| `scripts/run_manifest.py` | 25454 | Run manifest JSON/MD/latest. | CLI entry | yes | py_compile | yes | yes | yes | `keep_active` | РђРєС‚РёРІРЅС‹Р№ metadata stage Рё entry point. |
| `scripts/run_pipeline.py` | 27605 | РћСЃРЅРѕРІРЅРѕР№ РѕСЂРєРµСЃС‚СЂР°С‚РѕСЂ pipeline. | CLI entry | entry | py_compile | entry point | yes | yes | `keep_active` | Р“Р»Р°РІРЅС‹Р№ production entry point; no-touch. |
| `scripts/scatter_chart_policy.py` | 6866 | Scatter label policy Рё constants. | library | no | py_compile | yes | no | no | `keep_active` | РђРєС‚РёРІРЅР°СЏ library РґР»СЏ scatter charts Рё QA. |
| `scripts/schema_validation.py` | 20357 | Schema validation Рё chart data contracts. | quality | no | runtime/entry | yes | yes | no | `keep_active` | РђРєС‚РёРІРЅС‹Р№ QA entry point `ofz-schema`, РІС‹Р·С‹РІР°РµС‚СЃСЏ quality gate. |
| `scripts/smoke_tests.py` | 11825 | Smoke tests РґР»СЏ pipeline artifacts Рё contracts. | quality | no | runtime | yes | yes | yes | `keep_active` | РђРєС‚РёРІРЅС‹Р№ QA script, РІС‹Р·С‹РІР°РµС‚СЃСЏ quality gate. |
| `scripts/utils.py` | 12306 | РћР±С‰РёРµ utilities: markdown, logging, formatting, filesystem helpers. | library | no | import | yes | no | no | `keep_active` | Р‘Р°Р·РѕРІР°СЏ shared library; no-touch. |
| `scripts/visual_regression.py` | 58785 | Visual regression / fallback Plotly JSON inspection. | quality | no | runtime | yes | yes | yes | `refactor_candidate` | РђРєС‚РёРІРЅС‹Р№ QA script, РІС‹Р·С‹РІР°РµС‚СЃСЏ quality gate; РєР°РЅРґРёРґР°С‚ РЅР° СЂР°Р·Р±РёРµРЅРёРµ backend/check modules. |

## Notes

- `run_pipeline.py` РІС‹Р·С‹РІР°РµС‚ stage scripts С‡РµСЂРµР· `STAGE_SPECS`; С„РёР·РёС‡РµСЃРєРёР№ РїРµСЂРµРЅРѕСЃ active scripts СЃРµР№С‡Р°СЃ Р·Р°РїСЂРµС‰РµРЅ.
- `quality_gate.py` РёСЃРїРѕР»СЊР·СѓРµС‚ `KEY_SCRIPTS` РґР»СЏ py_compile Рё Р·Р°РїСѓСЃРєР°РµС‚ runtime QA scripts (`schema_validation.py`, `regression_tests.py`, `smoke_tests.py`, `html_chart_qa.py`, `visual_regression.py`, `anomaly_tests.py` РїСЂРё РЅР°Р»РёС‡РёРё).
- `scripts/maintenance/cleanup_docs.py` is the current production-safe workflow. Archived legacy cleanup script is stored at `scripts/archive/2026-06-15/cleanup_docs.py` for audit only.
- `delete_candidate` РЅР°РјРµСЂРµРЅРЅРѕ РЅРµ РІС‹СЃС‚Р°РІР»СЏР»СЃСЏ: РЅР° P1-Р°СѓРґРёС‚Рµ РґРѕСЃС‚Р°С‚РѕС‡РЅРѕ inventory Рё Р±СѓРґСѓС‰РµРіРѕ archive plan.
## 2026-06-08 Archive Decision Update

Physical archive for all five `archive_candidate` scripts was applied in P2.10 to `scripts/archive/2026-06-15/`.

Decision document: `docs/00_project/scripts_archive_decision.md`.

Summary:

- all five candidates were moved to `scripts/archive/2026-06-15/`;
- no Python files were deleted;
- recommendation for each candidate is now `archived`;
- P2.10 validation requires `compileall`, CLI help checks and `ofz-quality --fast`.


