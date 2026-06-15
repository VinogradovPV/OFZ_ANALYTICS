# РћС‚С‡РµС‚ Рѕ РіРѕС‚РѕРІРЅРѕСЃС‚Рё Рє production

Р”Р°С‚Р° Р°РєС‚СѓР°Р»РёР·Р°С†РёРё: 2026-06-08.

## 1. РСЃРїРѕР»РЅРёС‚РµР»СЊРЅС‹Р№ СЃС‚Р°С‚СѓСЃ

РЎС‚Р°С‚СѓСЃ РїСЂРѕРµРєС‚Р°: `production-ready candidate`.

РџСЂРѕРµРєС‚ РіРѕС‚РѕРІ Рє РїРѕРІС‚РѕСЂСЏРµРјРѕРјСѓ production-Р·Р°РїСѓСЃРєСѓ РІ С‚РµРєСѓС‰РµРј Р»РѕРєР°Р»СЊРЅРѕРј Рё Git-РєРѕРЅС‚СѓСЂРµ РїСЂРё СЃРѕР±Р»СЋРґРµРЅРёРё production runbook Рё release checklist. РЎС‚Р°С‚СѓСЃ РѕР±РѕР·РЅР°С‡РµРЅ РєР°Рє `production-ready candidate`, Р° РЅРµ РѕРєРѕРЅС‡Р°С‚РµР»СЊРЅС‹Р№ `production-ready` Р±РµР· РѕРіРѕРІРѕСЂРѕРє, РїРѕС‚РѕРјСѓ С‡С‚Рѕ РѕСЃС‚Р°СЋС‚СЃСЏ РґРѕРєСѓРјРµРЅС‚РёСЂРѕРІР°РЅРЅС‹Рµ РїСЂРµРґСѓРїСЂРµР¶РґРµРЅРёСЏ РїРѕ РґР°РЅРЅС‹Рј, visual regression СЂР°Р±РѕС‚Р°РµС‚ С‡РµСЂРµР· fallback Р±РµР· screenshot backend, Р° С„РёР·РёС‡РµСЃРєР°СЏ РѕС‡РёСЃС‚РєР° legacy docs/scripts РѕС‚Р»РѕР¶РµРЅР° РґРѕ P2.

## 2. РЎС‚Р°С‚СѓСЃ Git

- URL СЂРµРїРѕР·РёС‚РѕСЂРёСЏ: `https://github.com/VinogradovPV/OFZ_ANALYTICS.git`.
- Р’РёРґРёРјРѕСЃС‚СЊ: private.
- РћСЃРЅРѕРІРЅР°СЏ РІРµС‚РєР°: `main`.
- РџРѕСЃР»РµРґРЅРёР№ РїСЂРѕРІРµСЂРµРЅРЅС‹Р№ commit РґРѕ РѕР±РЅРѕРІР»РµРЅРёСЏ СЌС‚РѕРіРѕ РѕС‚С‡РµС‚Р°: `2ac420b Record final production quality gate`.
- РЎРѕСЃС‚РѕСЏРЅРёРµ working tree РґРѕ РѕР±РЅРѕРІР»РµРЅРёСЏ СЌС‚РѕРіРѕ РѕС‚С‡РµС‚Р°: clean.
- РџРѕР»РёС‚РёРєР° generated outputs РїСЂРѕРІРµСЂРµРЅР°: generated HTML/CSV/reports/dashboard exports РЅРµ tracked РІ Git.

## 3. РЎС‚СЂР°С‚РµРіРёСЏ Р°СЂС‚РµС„Р°РєС‚РѕРІ

Source artifacts РІ Git:

- source code;
- config;
- docs;
- scripts;
- data contracts;
- prompts;
- `data/raw`;
- skeleton-С„Р°Р№Р»С‹ outputs (`.gitkeep`, РґРѕРїСѓСЃС‚РёРјС‹Рµ Р»РµРіРєРёРµ `index.md` / `README.md`).

`data/raw` tracked РІ Git РєР°Рє source dataset РїСЂРѕРµРєС‚Р°, РїРѕС‚РѕРјСѓ С‡С‚Рѕ РёСЃС…РѕРґРЅС‹Рµ Excel-С„Р°Р№Р»С‹ РЅРµР±РѕР»СЊС€РёРµ Рё РЅСѓР¶РЅС‹ РґР»СЏ РІРѕСЃРїСЂРѕРёР·РІРѕРґРёРјРѕСЃС‚Рё.

Generated outputs РЅРµ РІС…РѕРґСЏС‚ РІ РѕР±С‹С‡РЅСѓСЋ Git-РёСЃС‚РѕСЂРёСЋ:

- `outputs/charts/**`;
- `outputs/exports/**`;
- `outputs/reports/**`;
- `outputs/dashboards/**`;
- `outputs/archive/**`;
- `outputs/tmp/**`;
- `outputs/cache/**`.

РџРѕР»РёС‚РёРєР° release bundle:

- generated outputs РєРѕРЅРєСЂРµС‚РЅРѕРіРѕ РѕС‚С‡РµС‚РЅРѕРіРѕ Р·Р°РїСѓСЃРєР° СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РєР°Рє release bundle, external artifact РёР»Рё Р±СѓРґСѓС‰РёР№ GitHub Release asset;
- release bundle РґРѕР»Р¶РµРЅ РІРєР»СЋС‡Р°С‚СЊ HTML charts, chart data CSV, dashboard exports, run manifests, QA reports Рё summaries;
- generated outputs РЅРµ РґРѕР»Р¶РЅС‹ РєРѕРјРјРёС‚РёС‚СЊСЃСЏ РєР°Рє РѕР±С‹С‡РЅР°СЏ source history.

## 4. РЎС‚Р°С‚СѓСЃ Python Рё package

- `pyproject.toml`: СЃСѓС‰РµСЃС‚РІСѓРµС‚.
- РРјСЏ package: `ofz-analytics`.
- Р’РµСЂСЃРёСЏ: `0.1.0`.
- РџРѕРґРґРµСЂР¶РёРІР°РµРјС‹Р№ РґРёР°РїР°Р·РѕРЅ Python: `>=3.11,<3.15`.
- РџСЂРѕРІРµСЂРµРЅРЅР°СЏ РІРµСЂСЃРёСЏ Python: `Python 3.14.5`.

CLI entry points:

- `ofz-run`;
- `ofz-interactive`;
- `ofz-quality`;
- `ofz-clean-outputs`;
- `ofz-schema`.

РџСЂРёРјРµС‡Р°РЅРёРµ: РєРѕСЂРѕС‚РєРёРµ РєРѕРјР°РЅРґС‹ `ofz-*` С‚СЂРµР±СѓСЋС‚ Р°РєС‚РёРІРёСЂРѕРІР°РЅРЅРѕР№ `.venv` РёР»Рё PATH, СЃРѕРґРµСЂР¶Р°С‰РµРіРѕ `.venv\Scripts`. РџСЂСЏРјС‹Рµ РїСЂРѕРІРµСЂРєРё С‡РµСЂРµР· `.\.venv\Scripts\ofz-*.exe` РїСЂРѕС€Р»Рё.

## 5. РЎС‚Р°С‚СѓСЃ РѕС‡РёСЃС‚РєРё docs

РРЅРІРµРЅС‚Р°СЂРёР·Р°С†РёСЏ docs:

- `keep_active`: 51;
- `archive_candidate`: 35;
- `merge_candidate`: 4;
- `delete_candidate`: 0.

РљРѕРЅС‚СЂРѕР»СЊРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹:

- `docs/00_project/docs_inventory_before_cleanup.md`;
- `docs/00_project/docs_cleanup_apply_decision.md`.

Р РµС€РµРЅРёРµ:

- С„РёР·РёС‡РµСЃРєРѕРµ Р°СЂС…РёРІРёСЂРѕРІР°РЅРёРµ docs РѕС‚Р»РѕР¶РµРЅРѕ;
- РґР»СЏ С‡Р°СЃС‚Рё archive/merge candidates РѕСЃС‚Р°СЋС‚СЃСЏ РЅРµСЂРµС€РµРЅРЅС‹Рµ СЃСЃС‹Р»РєРё;
- `--delete-archived` Р·Р°РїСЂРµС‰РµРЅ РґРѕ production-ready v1;
- archive apply С‚СЂРµР±СѓРµС‚ РѕС‚РґРµР»СЊРЅРѕРіРѕ controlled stage РїРѕСЃР»Рµ СѓСЃС‚СЂР°РЅРµРЅРёСЏ СЃСЃС‹Р»РѕРє.

## 6. РЎС‚Р°С‚СѓСЃ РѕС‡РёСЃС‚РєРё scripts

РРЅРІРµРЅС‚Р°СЂРёР·Р°С†РёСЏ scripts:

- `keep_active`: 32;
- `refactor_candidate`: 5;
- `archive_candidate`: 5;
- `delete_candidate`: 0;
- `unknown`: 0.

РљРѕРЅС‚СЂРѕР»СЊРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹:

- `docs/00_project/scripts_inventory_before_cleanup.md`;
- `docs/00_project/scripts_archive_decision.md`.

РџСЏС‚СЊ archive candidates:

- `scripts/archive/2026-06-15/cleanup_docs.py`;
- `scripts/archive/2026-06-15/migrate_outputs_structure.py`;
- `scripts/archive/2026-06-15/reorganize_outputs.py`;
- `scripts/archive/2026-06-15/migrate_legacy_docs_archive.py`;
- `scripts/archive/2026-06-15/reorganize_docs.py`.

Р РµС€РµРЅРёРµ:

- legacy scripts archive applied in P2.10;
- physical archive completed to `scripts/archive/2026-06-15/`;
- no scripts were deleted;
- validation requires `compileall`, CLI help checks and `ofz-quality --fast`.

## 7. РЎС‚Р°С‚СѓСЃ module decomposition

РџР»Р°РЅ СЃСѓС‰РµСЃС‚РІСѓРµС‚:

- `docs/03_pipeline/module_decomposition_plan.md`.

РЎС‚Р°С‚СѓСЃ:

- С‚РѕР»СЊРєРѕ РїР»Р°РЅРёСЂРѕРІР°РЅРёРµ;
- РІ production-ready v1 С„РёР·РёС‡РµСЃРєРёРµ РїРµСЂРµРЅРѕСЃС‹ РЅРµ РІС‹РїРѕР»РЅСЏСЋС‚СЃСЏ;
- РґРµРєРѕРјРїРѕР·РёС†РёСЏ СЏРІР»СЏРµС‚СЃСЏ P2-only;
- РґР»СЏ Р±СѓРґСѓС‰РёС… РїРµСЂРµРЅРѕСЃРѕРІ РѕР±СЏР·Р°С‚РµР»СЊРЅР° wrapper compatibility.

РћСЃРЅРѕРІРЅС‹Рµ РєР°РЅРґРёРґР°С‚С‹:

- `scripts/06_build_charts.py`;
- `scripts/10_build_monthly_charts.py`;
- `scripts/html_chart_qa.py`;
- `scripts/visual_regression.py`;
- `scripts/quality_gate.py`;
- `scripts/07_dashboard_exports.py`.

## 8. РЎС‚Р°С‚СѓСЃ data contracts

РђРєС‚РёРІРЅС‹Рµ data contracts:

- `docs/02_data_contracts/processed_data_contract.md`;
- `docs/02_data_contracts/analytical_tables_contract.md`;
- `docs/02_data_contracts/chart_data_contract.md`;
- `docs/02_data_contracts/dashboard_exports_contract.md`;
- `docs/02_data_contracts/semantic_model_v2.md`.

РљР»СЋС‡РµРІС‹Рµ РїСЂР°РІРёР»Р° contracts:

- РїРѕР»СЏ `*_volume_bln` С‚СЂРµР±СѓСЋС‚ unit-РїРѕР»СЏ СЃРѕ Р·РЅР°С‡РµРЅРёРµРј `РјР»СЂРґ СЂСѓР±Р»РµР№`;
- revenue fields РІРєР»СЋС‡Р°СЋС‚ `revenue_volume_bln`, `nominal_revenue_gap_bln`, `revenue_to_nominal_ratio`;
- yield fields СЂР°Р·Р»РёС‡Р°СЋС‚ РѕР±С‹С‡РЅСѓСЋ РґРѕС…РѕРґРЅРѕСЃС‚СЊ Рё СЃСЂРµРґРЅРµРІР·РІРµС€РµРЅРЅСѓСЋ РґРѕС…РѕРґРЅРѕСЃС‚СЊ СЂР°Р·РјРµС‰РµРЅРёСЏ;
- discount fields С„РёРєСЃРёСЂСѓСЋС‚ source column, fallback formula Рё unit `Рї.Рї.`;
- label fields Рё quality fields РґРѕРєСѓРјРµРЅС‚РёСЂРѕРІР°РЅС‹ РґР»СЏ chart data exports.

## 9. РЎС‚Р°С‚СѓСЃ quality gate

Р¤РёРЅР°Р»СЊРЅС‹Р№ production quality gate РІС‹РїРѕР»РЅРµРЅ РґР»СЏ РїР°СЂР°РјРµС‚СЂРѕРІ:

```powershell
--report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Р РµР·СѓР»СЊС‚Р°С‚С‹:

- `pip install -e .`: OK РїРѕСЃР»Рµ escalated rerun, РїРѕС‚РѕРјСѓ С‡С‚Рѕ sandboxed pip РЅРµ СЃРјРѕРі Р·Р°РїРёСЃР°С‚СЊ РІРѕ `%TEMP%`;
- `pip check`: OK;
- `compileall`: OK;
- `schema_validation`: OK, 16/16;
- `smoke_tests`: OK, 9 checks;
- `regression_tests`: OK, 14 checks;
- `anomaly_tests`: completed with documented data warnings;
- `html_chart_qa`: OK;
- `visual_regression`: OK С‡РµСЂРµР· fallback static HTML / Plotly JSON inspection;
- `quality_gate --fast`: OK;
- `quality_gate --full`: OK.

РџСЂРёРјРµС‡Р°РЅРёРµ: РїРµСЂРІС‹Р№ РїР°СЂР°Р»Р»РµР»СЊРЅС‹Р№ Р·Р°РїСѓСЃРє fast/full gate РІС‹Р·РІР°Р» РІСЂРµРјРµРЅРЅС‹Р№ `.pyc` permission conflict РІ `scripts/__pycache__`. РџРѕСЃР»РµРґРѕРІР°С‚РµР»СЊРЅС‹Р№ rerun РїСЂРѕС€РµР».

## 10. РСЃРїСЂР°РІР»РµРЅРЅС‹Рµ blockers

РСЃРїСЂР°РІР»РµРЅРЅС‹Рµ blockers:

- production blocker `schema_validation / volume_bln_units` РёСЃРїСЂР°РІР»РµРЅ РІ generators Рё data contracts;
- generated outputs РёСЃРєР»СЋС‡РµРЅС‹ РёР· Git СЃ СЃРѕС…СЂР°РЅРµРЅРёРµРј skeleton;
- СЃС‚СЂР°С‚РµРіРёСЏ `data/raw` Р·Р°С„РёРєСЃРёСЂРѕРІР°РЅР° Рё РґРѕРєСѓРјРµРЅС‚РёСЂРѕРІР°РЅР°;
- `.gitignore` Рё Git artifact strategy РІРЅРµРґСЂРµРЅС‹;
- CLI entry points РґРѕР±Р°РІР»РµРЅС‹ Рё РїСЂРѕРІРµСЂРµРЅС‹;
- cleanup outputs workflow РґРѕР±Р°РІР»РµРЅ С‡РµСЂРµР· `ofz-clean-outputs`;
- production runbook Рё release checklist СЃРѕР·РґР°РЅС‹.

## 11. РћСЃС‚Р°РІС€РёРµСЃСЏ warnings

РћСЃС‚Р°РІС€РёРµСЃСЏ warnings СЏРІР»СЏСЋС‚СЃСЏ РїСЂРµРґСѓРїСЂРµР¶РґРµРЅРёСЏРјРё РїРѕ РґР°РЅРЅС‹Рј/РѕРїРµСЂР°С†РёСЏРј, Р° РЅРµ execution failures:

- anomaly tests С„РёРєСЃРёСЂСѓСЋС‚ СЃС‚СЂРѕРєРё Р±РµР· yield Рё demand/supply edge cases;
- bid-to-cover Рё demand-to-placement outliers С‚СЂРµР±СѓСЋС‚ Р°РЅР°Р»РёС‚РёС‡РµСЃРєРѕР№ РїСЂРѕРІРµСЂРєРё;
- СЃС‚СЂРѕРєРё Р±РµР· cutoff price РѕРіСЂР°РЅРёС‡РёРІР°СЋС‚ discount analysis;
- nominal/revenue gap anomalies РІС‹С€Рµ threshold С‚СЂРµР±СѓСЋС‚ РёРЅС‚РµСЂРїСЂРµС‚Р°С†РёРё;
- screenshot backend РЅРµ РЅР°СЃС‚СЂРѕРµРЅ, РїРѕСЌС‚РѕРјСѓ visual regression РёСЃРїРѕР»СЊР·СѓРµС‚ fallback static HTML / Plotly JSON;
- physical cleanup docs/scripts РѕС‚Р»РѕР¶РµРЅ РґРѕ СѓСЃС‚СЂР°РЅРµРЅРёСЏ СЃСЃС‹Р»РѕРє;
- Python 3.11-3.13 СЂР°Р·СЂРµС€РµРЅС‹ metadata, РЅРѕ С‚РµРєСѓС‰Р°СЏ Р»РѕРєР°Р»СЊРЅР°СЏ runtime-СЃРµСЂС‚РёС„РёРєР°С†РёСЏ РІС‹РїРѕР»РЅРµРЅР° РЅР° Python 3.14.5.

## 12. РС‚РѕРіРѕРІР°СЏ СЃС‚СЂСѓРєС‚СѓСЂР°

Docs:

- `docs/00_project/` вЂ” project governance, inventories, readiness, artifact policy;
- `docs/01_methodology/` вЂ” methodology Рё KPI maps;
- `docs/02_data_contracts/` вЂ” active data contracts;
- `docs/02_data_pipeline/` вЂ” data pipeline documentation;
- `docs/03_analytics/` Рё `docs/03_pipeline/` вЂ” analytics Рё pipeline planning;
- `docs/04_visualization/` вЂ” visualization rules Рё limitations;
- `docs/05_dashboard/` вЂ” dashboard docs;
- `docs/06_quality/` вЂ” QA reports Рё manual checks;
- `docs/07_operations/` вЂ” environment, runbook, release checklist;
- `docs/90_archive/` вЂ” historical documentation.

Scripts:

- active stage scripts РѕСЃС‚Р°СЋС‚СЃСЏ РІ `scripts/`;
- production maintenance scripts РЅР°С…РѕРґСЏС‚СЃСЏ РІ `scripts/maintenance/`;
- physical script archive РёР»Рё decomposition РІ v1 РЅРµ РІС‹РїРѕР»РЅСЏСЋС‚СЃСЏ.

Outputs:

- generated outputs РЅР°С…РѕРґСЏС‚СЃСЏ РІ `outputs/`;
- Git tracks С‚РѕР»СЊРєРѕ skeleton `.gitkeep` files Рё `outputs/charts/index.md`;
- generated HTML/CSV/reports/dashboard exports СЏРІР»СЏСЋС‚СЃСЏ release artifacts, Р° РЅРµ source commits.

## 13. РљРѕРјР°РЅРґР° РїРѕР»РЅРѕР№ РѕС‡РёСЃС‚РєРё outputs

Dry-run:

```powershell
ofz-clean-outputs --dry-run
```

РђСЂС…РёРІРёСЂРѕРІР°С‚СЊ Рё СѓРґР°Р»РёС‚СЊ:

```powershell
ofz-clean-outputs --archive-all --delete-all --confirm DELETE_OUTPUTS
```

Fallback:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all --delete-all --confirm DELETE_OUTPUTS
```

## 14. Cleanup mode РІ interactive launcher

Interactive launcher:

```powershell
ofz-interactive
```

РџРµСЂРµРґ Р·Р°РїСѓСЃРєРѕРј pipeline РѕРЅ РїСЂРѕРІРµСЂСЏРµС‚ generated outputs Рё РїСЂРµРґР»Р°РіР°РµС‚:

1. РѕСЃС‚Р°РІРёС‚СЊ outputs РєР°Рє РµСЃС‚СЊ;
2. РїРѕРєР°Р·Р°С‚СЊ cleanup dry-run;
3. Р°СЂС…РёРІРёСЂРѕРІР°С‚СЊ outputs Рё РѕС‡РёСЃС‚РёС‚СЊ;
4. РѕС‡РёСЃС‚РёС‚СЊ outputs Р±РµР· Р°СЂС…РёРІР° РїРѕСЃР»Рµ СЏРІРЅРѕРіРѕ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ;
5. РѕС‚РјРµРЅРёС‚СЊ Р·Р°РїСѓСЃРє.

Launcher РґРµР»РµРіРёСЂСѓРµС‚ СѓРґР°Р»РµРЅРёРµ `scripts/maintenance/cleanup_outputs.py`; РЅР°РїСЂСЏРјСѓСЋ С„Р°Р№Р»С‹ РѕРЅ РЅРµ СѓРґР°Р»СЏРµС‚.

## 15. Release checklist

Release checklist СЃСѓС‰РµСЃС‚РІСѓРµС‚:

- `docs/07_operations/release_checklist.md`.

РћРЅ РїРѕРєСЂС‹РІР°РµС‚ Git state, environment, CLI help, `data/raw`, pipeline runs, QA, outputs/release bundle, docs/scripts cleanup decisions Рё final staged-file checks.

## 16. РћСЃС‚Р°РІС€РёРµСЃСЏ СЂРёСЃРєРё

РћСЃС‚Р°РІС€РёРµСЃСЏ production risks:

- visual regression РїРѕРєР° РЅРµ screenshot-based;
- generated outputs Р±РѕР»СЊС€РёРµ Рё С‚СЂРµР±СѓСЋС‚ РґРёСЃС†РёРїР»РёРЅС‹ external release bundle;
- docs archive candidates РІСЃРµ РµС‰Рµ РёРјРµСЋС‚ СЃСЃС‹Р»РєРё, РїРѕСЌС‚РѕРјСѓ cleanup С„РёР·РёС‡РµСЃРєРё РЅРµ РїСЂРёРјРµРЅРµРЅ;
- legacy scripts РѕСЃС‚Р°СЋС‚СЃСЏ РЅР° РјРµСЃС‚Рµ РґРѕ P2;
- chart builders Рё QA scripts СЏРІР»СЏСЋС‚СЃСЏ РєСЂСѓРїРЅС‹РјРё monoliths Рё С‚СЂРµР±СѓСЋС‚ controlled decomposition РїРѕР·Р¶Рµ;
- data warnings С‚СЂРµР±СѓСЋС‚ Р°РЅР°Р»РёС‚РёС‡РµСЃРєРѕР№ РїСЂРѕРІРµСЂРєРё РїРµСЂРµРґ high-stakes external publication;
- release bundle process РґРѕРєСѓРјРµРЅС‚РёСЂРѕРІР°РЅ, РЅРѕ РїРѕРєР° РЅРµ Р°РІС‚РѕРјР°С‚РёР·РёСЂРѕРІР°РЅ РѕРґРЅРѕР№ РєРѕРјР°РЅРґРѕР№.

## 17. Р РµРєРѕРјРµРЅРґР°С†РёРё СЃР»РµРґСѓСЋС‰РµРіРѕ СЂРµР»РёР·Р°

Р РµРєРѕРјРµРЅРґСѓРµРјС‹Рµ P2-Р·Р°РґР°С‡Рё:

Р”РµС‚Р°Р»СЊРЅС‹Р№ P2 roadmap РїРѕСЃР»Рµ production-ready v1 РІС‹РЅРµСЃРµРЅ РІ РѕС‚РґРµР»СЊРЅС‹Р№ РґРѕРєСѓРјРµРЅС‚:

- `docs/00_project/p2_roadmap_after_production_ready_v1.md`.

1. Р”РѕР±Р°РІРёС‚СЊ screenshot backend РґР»СЏ visual regression.
2. РђРІС‚РѕРјР°С‚РёР·РёСЂРѕРІР°С‚СЊ release bundle creation.
3. РЈСЃС‚СЂР°РЅРёС‚СЊ СЃСЃС‹Р»РєРё РЅР° docs archive candidates Рё РІС‹РїРѕР»РЅРёС‚СЊ controlled docs archive apply.
4. РЈСЃС‚СЂР°РЅРёС‚СЊ СЃСЃС‹Р»РєРё РЅР° legacy scripts Рё С„РёР·РёС‡РµСЃРєРё Р°СЂС…РёРІРёСЂРѕРІР°С‚СЊ safe candidates.
5. РќР°С‡Р°С‚СЊ module decomposition С‚РѕР»СЊРєРѕ СЃ extraction pure helper functions.
6. Р”РѕР±Р°РІРёС‚СЊ CI workflow РґР»СЏ install, compileall, schema Рё fast quality gate.
7. РЎРµСЂС‚РёС„РёС†РёСЂРѕРІР°С‚СЊ runtime РЅР° Python 3.11/3.12/3.13 РёР»Рё СЃСѓР·РёС‚СЊ metadata РґРѕ СЂРµР°Р»СЊРЅРѕ РїСЂРѕРІРµСЂРµРЅРЅС‹С… РІРµСЂСЃРёР№.
8. Р”РѕР±Р°РІРёС‚СЊ release manifest, СЃРІСЏР·С‹РІР°СЋС‰РёР№ Git commit, raw hashes, run manifest Рё checksum release bundle.
## P2.1 update: release bundle automation

Р”Р°С‚Р°: 2026-06-09.

Release bundle creation Р°РІС‚РѕРјР°С‚РёР·РёСЂРѕРІР°РЅ С‡РµСЂРµР· `scripts/maintenance/build_release_bundle.py` Рё CLI entry point `ofz-build-release-bundle`.

РќРѕРІС‹Р№ release bundle СЃРѕР·РґР°РµС‚СЃСЏ РІРЅРµ Git РІ `releases/` Рё РІРєР»СЋС‡Р°РµС‚ generated outputs С‚РѕР»СЊРєРѕ РїСЂРё СЏРІРЅРѕРј Р·Р°РїСѓСЃРєРµ:

```powershell
ofz-build-release-bundle --include-outputs --confirm BUILD_RELEASE_BUNDLE --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

РЎР»РµРґСѓСЋС‰РёР№ production-readiness С€Р°Рі P2: РґРѕР±Р°РІРёС‚СЊ pipeline telemetry Рё РІРєР»СЋС‡РёС‚СЊ telemetry summary РІ release bundle.


