# P2 roadmap РїРѕСЃР»Рµ production-ready v1

Р”Р°С‚Р° Р°РєС‚СѓР°Р»РёР·Р°С†РёРё: 2026-06-08.

Р­С‚РѕС‚ РґРѕРєСѓРјРµРЅС‚ С„РёРєСЃРёСЂСѓРµС‚ Р·Р°РґР°С‡Рё, РєРѕС‚РѕСЂС‹Рµ РЅР°РјРµСЂРµРЅРЅРѕ РІС‹РЅРµСЃРµРЅС‹ Р·Р° РїСЂРµРґРµР»С‹ production-ready v1. Р’ СЂР°РјРєР°С… v1 СЌС‚Рё СЂР°Р±РѕС‚С‹ РЅРµ РІС‹РїРѕР»РЅСЏСЋС‚СЃСЏ С„РёР·РёС‡РµСЃРєРё: РЅРµ Р°СЂС…РёРІРёСЂСѓСЋС‚СЃСЏ РґРѕРєСѓРјРµРЅС‚С‹, РЅРµ РїРµСЂРµРЅРѕСЃСЏС‚СЃСЏ scripts, РЅРµ Р·Р°РїСѓСЃРєР°РµС‚СЃСЏ РјР°СЃСЃРѕРІР°СЏ РґРµРєРѕРјРїРѕР·РёС†РёСЏ Рё РЅРµ СѓРґР°Р»СЏСЋС‚СЃСЏ archived docs.

## РЎС‚Р°С‚СѓСЃ

РЎС‚Р°С‚СѓСЃ roadmap: `P2 / post production-ready v1`.

РќР°Р·РЅР°С‡РµРЅРёРµ:

- РѕС‚РґРµР»РёС‚СЊ СЃС‚Р°Р±РёР»РёР·Р°С†РёСЋ production-ready v1 РѕС‚ РїРѕСЃР»РµРґСѓСЋС‰РёС… СѓР»СѓС‡С€РµРЅРёР№;
- РЅРµ СЃРјРµС€РёРІР°С‚СЊ cleanup, decomposition, CI Рё release automation СЃ СѓР¶Рµ РїРѕРґС‚РІРµСЂР¶РґРµРЅРЅС‹Рј production-candidate СЃРѕСЃС‚РѕСЏРЅРёРµРј;
- СЃРѕС…СЂР°РЅРёС‚СЊ РєРѕРЅС‚СЂРѕР»РёСЂСѓРµРјРѕСЃС‚СЊ РёР·РјРµРЅРµРЅРёР№: РєР°Р¶РґС‹Р№ РїСѓРЅРєС‚ P2 РґРѕР»Р¶РµРЅ РІС‹РїРѕР»РЅСЏС‚СЊСЃСЏ РѕС‚РґРµР»СЊРЅС‹Рј СЌС‚Р°РїРѕРј СЃ РїСЂРѕРІРµСЂРєР°РјРё Рё РѕС‚РґРµР»СЊРЅС‹Рј commit.

## РћР±С‰РёРµ РїСЂР°РІРёР»Р° P2

1. РџРµСЂРµРґ РєР°Р¶РґС‹Рј P2-СЌС‚Р°РїРѕРј РїСЂРѕРІРµСЂСЏС‚СЊ `git status --short`.
2. РќРµ РІС‹РїРѕР»РЅСЏС‚СЊ РјР°СЃСЃРѕРІС‹Р№ `git add .` Р±РµР· РїСЂРѕСЃРјРѕС‚СЂР° staged files.
3. РќРµ РјРµРЅСЏС‚СЊ `data/raw/` РІСЂСѓС‡РЅСѓСЋ.
4. РќРµ РєРѕРјРјРёС‚РёС‚СЊ generated outputs.
5. РџРѕСЃР»Рµ РєР°Р¶РґРѕРіРѕ P2-СЌС‚Р°РїР° Р·Р°РїСѓСЃРєР°С‚СЊ РјРёРЅРёРјСѓРј:

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

6. Р”Р»СЏ РёР·РјРµРЅРµРЅРёР№ release/CI/visual regression РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅРѕ РѕР±РЅРѕРІР»СЏС‚СЊ `docs/07_operations/release_checklist.md` Рё `docs/07_operations/production_runbook.md`.

## 1. РЈСЃС‚СЂР°РЅРёС‚СЊ СЃСЃС‹Р»РєРё РЅР° docs archive candidates Рё РїСЂРёРјРµРЅРёС‚СЊ docs archive

Р¦РµР»СЊ: Р·Р°РєСЂС‹С‚СЊ deferred docs cleanup РїРѕСЃР»Рµ production-ready v1.

Р§С‚Рѕ СЃРґРµР»Р°С‚СЊ:

- РїСЂРѕРІРµСЂРёС‚СЊ Р°РєС‚РёРІРЅС‹Рµ СЃСЃС‹Р»РєРё РЅР° `archive_candidate` Рё `merge_candidate` РІ `README.md`, `docs/**`, `scripts/**`, `pyproject.toml`;
- РїРµСЂРµРЅРµСЃС‚Рё РїРѕР»РµР·РЅС‹Рµ РїСЂР°РІРёР»Р° РёР· merge candidates РІ active docs, РµСЃР»Рё СЌС‚Рѕ РµС‰Рµ РЅРµ СЃРґРµР»Р°РЅРѕ;
- РѕР±РЅРѕРІРёС‚СЊ `docs/00_project/docs_inventory_before_cleanup.md`;
- РІС‹РїРѕР»РЅРёС‚СЊ `scripts/maintenance/cleanup_docs.py --dry-run`;
- С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ РїСЂРѕРІРµСЂРєРё dry-run РІС‹РїРѕР»РЅРёС‚СЊ controlled archive mode;
- СЃРѕР·РґР°С‚СЊ/РѕР±РЅРѕРІРёС‚СЊ `docs/00_project/docs_inventory_after_cleanup.md`.

Р—Р°РїСЂРµС‚: РЅРµ РІС‹РїРѕР»РЅСЏС‚СЊ `--delete-archived` РЅР° СЌС‚РѕРј С€Р°РіРµ.

## 2. РЈСЃС‚СЂР°РЅРёС‚СЊ СЃСЃС‹Р»РєРё РЅР° legacy scripts Рё РїСЂРёРјРµРЅРёС‚СЊ scripts archive

Р¦РµР»СЊ: Р·Р°РєСЂС‹С‚СЊ deferred scripts archive decision.

Archive candidates:

- `scripts/archive/2026-06-15/cleanup_docs.py`;
- `scripts/archive/2026-06-15/migrate_outputs_structure.py`;
- `scripts/archive/2026-06-15/reorganize_outputs.py`;
- `scripts/archive/2026-06-15/migrate_legacy_docs_archive.py`;
- `scripts/archive/2026-06-15/reorganize_docs.py`.

Р§С‚Рѕ СЃРґРµР»Р°С‚СЊ:

- РїСЂРѕРІРµСЂРёС‚СЊ references РІ `README.md`, `docs/**`, `scripts/**`, `pyproject.toml`, `scripts/run_pipeline.py`, `scripts/quality_gate.py`, `scripts/config.py`;
- СѓРґР°Р»РёС‚СЊ РёР»Рё РѕР±РЅРѕРІРёС‚СЊ Р°РєС‚РёРІРЅС‹Рµ СЃСЃС‹Р»РєРё;
- РїРѕРґРіРѕС‚РѕРІРёС‚СЊ `scripts/archive/YYYY-MM-DD/README.md`;
- РїРµСЂРµРЅРµСЃС‚Рё С‚РѕР»СЊРєРѕ С‚Рµ scripts, РєРѕС‚РѕСЂС‹Рµ Р±РѕР»СЊС€Рµ РЅРµ РёРјРµСЋС‚ Р°РєС‚РёРІРЅС‹С… СЃСЃС‹Р»РѕРє;
- СЃРѕС…СЂР°РЅРёС‚СЊ wrapper compatibility, РµСЃР»Рё РєР°РєРѕР№-Р»РёР±Рѕ РїСѓС‚СЊ РµС‰Рµ РјРѕР¶РµС‚ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊСЃСЏ РёСЃС‚РѕСЂРёС‡РµСЃРєРёРјРё РєРѕРјР°РЅРґР°РјРё;
- РІС‹РїРѕР»РЅРёС‚СЊ `compileall` Рё `ofz-quality --fast`.

## 3. Р¤РёР·РёС‡РµСЃРєР°СЏ module decomposition

Р¦РµР»СЊ: РїРµСЂРµР№С‚Рё РѕС‚ planning-only РґРѕРєСѓРјРµРЅС‚Р° Рє РєРѕРЅС‚СЂРѕР»РёСЂСѓРµРјРѕР№ РјРѕРґСѓР»СЊРЅРѕР№ СЃС‚СЂСѓРєС‚СѓСЂРµ.

РћСЃРЅРѕРІРЅС‹Рµ РєР°РЅРґРёРґР°С‚С‹:

- `scripts/06_build_charts.py`;
- `scripts/10_build_monthly_charts.py`;
- `scripts/html_chart_qa.py`;
- `scripts/visual_regression.py`;
- `scripts/quality_gate.py`;
- `scripts/07_dashboard_exports.py`.

РџРѕСЂСЏРґРѕРє:

1. РЎРЅР°С‡Р°Р»Р° РІС‹РЅРѕСЃРёС‚СЊ pure helper functions.
2. Р—Р°С‚РµРј chart family builders.
3. Р—Р°С‚РµРј QA check groups.
4. РџРѕСЃР»Рµ РєР°Р¶РґРѕРіРѕ С€Р°РіР° СЃРѕС…СЂР°РЅСЏС‚СЊ wrappers РґР»СЏ СЃС‚Р°СЂС‹С… entry points.
5. РџРѕСЃР»Рµ РєР°Р¶РґРѕРіРѕ С€Р°РіР° Р·Р°РїСѓСЃРєР°С‚СЊ `compileall`, `ofz-quality --fast` Рё СЂРµР»РµРІР°РЅС‚РЅС‹Рµ targeted QA scripts.

## 4. РќР°СЃС‚СЂРѕРёС‚СЊ actual screenshot backend РґР»СЏ visual regression

Р¦РµР»СЊ: Р·Р°РјРµРЅРёС‚СЊ С‚РµРєСѓС‰РёР№ fallback static HTML / Plotly JSON inspection РЅР° РїРѕР»РЅРѕС†РµРЅРЅСѓСЋ screenshot-РїСЂРѕРІРµСЂРєСѓ.

Р§С‚Рѕ СЃРґРµР»Р°С‚СЊ:

- РІС‹Р±СЂР°С‚СЊ backend: Kaleido/Playwright/browser-based workflow;
- РѕРїСЂРµРґРµР»РёС‚СЊ РїРѕРґРґРµСЂР¶РєСѓ Windows;
- РґРѕР±Р°РІРёС‚СЊ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё РІ `requirements-dev.txt` РёР»Рё production dependencies, РµСЃР»Рё backend РЅСѓР¶РµРЅ РІ release gate;
- РґРѕР±Р°РІРёС‚СЊ С‚РµСЃС‚РѕРІС‹Р№ screenshot sample;
- РѕР±РЅРѕРІРёС‚СЊ `scripts/visual_regression.py`;
- РѕР±РЅРѕРІРёС‚СЊ runbook Рё release checklist.

РљСЂРёС‚РµСЂРёР№ РіРѕС‚РѕРІРЅРѕСЃС‚Рё: visual regression СѓРјРµРµС‚ СЃРѕР·РґР°РІР°С‚СЊ Рё СЃСЂР°РІРЅРёРІР°С‚СЊ РёР·РѕР±СЂР°Р¶РµРЅРёСЏ РіСЂР°С„РёРєРѕРІ, Р° fallback РѕСЃС‚Р°РµС‚СЃСЏ СЂРµР·РµСЂРІРЅС‹Рј СЂРµР¶РёРјРѕРј.

## 5. CI / GitHub Actions

Р¦РµР»СЊ: РїСЂРѕРІРµСЂСЏС‚СЊ production contracts РІ GitHub РґРѕ merge/push release.

РњРёРЅРёРјР°Р»СЊРЅС‹Р№ CI:

- checkout;
- setup Python;
- install dependencies;
- `pip install -e .`;
- `pip check`;
- `compileall`;
- `ofz-schema`;
- `ofz-quality --fast`.

РћРіСЂР°РЅРёС‡РµРЅРёРµ: generated outputs РЅРµ РґРѕР»Р¶РЅС‹ РєРѕРјРјРёС‚РёС‚СЊСЃСЏ CI job. Р•СЃР»Рё CI РіРµРЅРµСЂРёСЂСѓРµС‚ Р°СЂС‚РµС„Р°РєС‚С‹, РѕРЅРё РґРѕР»Р¶РЅС‹ СЃРѕС…СЂР°РЅСЏС‚СЊСЃСЏ РєР°Рє workflow artifacts.

## 6. РђРІС‚РѕРјР°С‚РёР·Р°С†РёСЏ release bundle

Р¦РµР»СЊ: РѕРґРЅРѕР№ РєРѕРјР°РЅРґРѕР№ СЃРѕР±РёСЂР°С‚СЊ РІРЅРµС€РЅРёР№ release artifact РґР»СЏ РєРѕРЅРєСЂРµС‚РЅРѕРіРѕ run.

Release bundle РґРѕР»Р¶РµРЅ РІРєР»СЋС‡Р°С‚СЊ:

- HTML charts;
- chart data CSV;
- dashboard exports;
- run manifests;
- QA reports;
- executive summary;
- data quality summary, РµСЃР»Рё СЃРѕР·РґР°РЅ;
- release manifest СЃ Git commit, raw hashes, run params Рё checksums.

Р РµРєРѕРјРµРЅРґСѓРµРјР°СЏ РєРѕРјР°РЅРґР° Р±СѓРґСѓС‰РµРіРѕ СЌС‚Р°РїР°:

```powershell
ofz-build-release-bundle --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## 7. Dockerfile / Windows setup

Р¦РµР»СЊ: СѓРїСЂРѕСЃС‚РёС‚СЊ РІРѕСЃРїСЂРѕРёР·РІРѕРґРёРјС‹Р№ Р·Р°РїСѓСЃРє РІРЅРµ С‚РµРєСѓС‰РµР№ РјР°С€РёРЅС‹.

Р§С‚Рѕ СЃРґРµР»Р°С‚СЊ:

- РѕРїРёСЃР°С‚СЊ Windows-first setup;
- РґРѕР±Р°РІРёС‚СЊ РїСЂРѕРІРµСЂРµРЅРЅС‹Р№ `Dockerfile`, РµСЃР»Рё Р±СѓРґРµС‚ РІС‹Р±СЂР°РЅ РєРѕРЅС‚РµР№РЅРµСЂРЅС‹Р№ СЃС†РµРЅР°СЂРёР№;
- Р·Р°С„РёРєСЃРёСЂРѕРІР°С‚СЊ РѕРіСЂР°РЅРёС‡РµРЅРёСЏ Excel/raw data handling;
- РїСЂРѕРІРµСЂРёС‚СЊ fonts/locale РґР»СЏ СЂСѓСЃСЃРєРёС… РїРѕРґРїРёСЃРµР№ РіСЂР°С„РёРєРѕРІ;
- РѕР±РЅРѕРІРёС‚СЊ `docs/07_operations/environment.md`.

## 8. BI-ready release package

Р¦РµР»СЊ: РїРѕРґРіРѕС‚РѕРІРёС‚СЊ РїР°РєРµС‚ РґР»СЏ BI/Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёС… РёРЅСЃС‚СЂСѓРјРµРЅС‚РѕРІ.

РЎРѕСЃС‚Р°РІ:

- dashboard exports;
- semantic model v2;
- analytical tables;
- chart data CSV;
- data dictionary;
- README РґР»СЏ BI-РїРѕС‚СЂРµР±РёС‚РµР»СЏ;
- versioned release manifest.

РўСЂРµР±РѕРІР°РЅРёРµ: BI-ready package РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ external artifact, Р° РЅРµ РѕР±С‹С‡РЅС‹Р№ Git commit generated outputs.

## 9. Pipeline telemetry

Р¦РµР»СЊ: РґРѕР±Р°РІРёС‚СЊ РЅР°Р±Р»СЋРґР°РµРјРѕСЃС‚СЊ production-Р·Р°РїСѓСЃРєРѕРІ.

Р§С‚Рѕ С„РёРєСЃРёСЂРѕРІР°С‚СЊ:

- run id;
- stage durations;
- input/output counts;
- warnings/errors;
- generated artifacts count/size;
- cleanup mode;
- quality gate results;
- Git commit;
- raw data hashes.

Р РµР·СѓР»СЊС‚Р°С‚: telemetry summary РґРѕР»Р¶РµРЅ РїРѕРїР°РґР°С‚СЊ РІ run manifest Рё, РїСЂРё РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё, РІ РѕС‚РґРµР»СЊРЅС‹Р№ `outputs/reports/telemetry/` artifact.

## 10. РЈРґР°Р»СЏС‚СЊ archived docs С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ stable release

Р¦РµР»СЊ: РЅРµ РїРѕС‚РµСЂСЏС‚СЊ РёСЃС‚РѕСЂРёС‡РµСЃРєРёР№ РєРѕРЅС‚РµРєСЃС‚ СЃСЂР°Р·Сѓ РїРѕСЃР»Рµ РїРµСЂРІРѕРіРѕ controlled archive.

РџСЂР°РІРёР»Рѕ:

- РїРѕСЃР»Рµ docs archive apply Р°СЂС…РёРІРёСЂРѕРІР°РЅРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ РѕСЃС‚Р°СЋС‚СЃСЏ РІ СЂРµРїРѕР·РёС‚РѕСЂРёРё;
- `--delete-archived` Р·Р°РїСЂРµС‰РµРЅ РґРѕ stable release РїРѕСЃР»Рµ production-ready v1;
- СѓРґР°Р»РµРЅРёРµ archived docs РґРѕРїСѓСЃРєР°РµС‚СЃСЏ С‚РѕР»СЊРєРѕ РѕС‚РґРµР»СЊРЅС‹Рј РїРѕРґС‚РІРµСЂР¶РґРµРЅРЅС‹Рј СЌС‚Р°РїРѕРј;
- РїРµСЂРµРґ СѓРґР°Р»РµРЅРёРµРј РЅСѓР¶РµРЅ dry-run, manifest Рё РїСЂРѕРІРµСЂРєР°, С‡С‚Рѕ release bundle/stable tag СѓР¶Рµ СЃРѕР·РґР°РЅ.

## РљСЂРёС‚РµСЂРёР№ Р·Р°РІРµСЂС€РµРЅРёСЏ P2 roadmap

P2 roadmap СЃС‡РёС‚Р°РµС‚СЃСЏ Р·Р°РєСЂС‹С‚С‹Рј, РєРѕРіРґР°:

- docs archive references resolved Рё archive apply РІС‹РїРѕР»РЅРµРЅ;
- legacy scripts references resolved Рё archive apply РІС‹РїРѕР»РЅРµРЅ;
- module decomposition РІС‹РїРѕР»РЅРµРЅР° СЃ wrappers Рё QA;
- visual regression РёРјРµРµС‚ screenshot backend;
- CI РЅР°СЃС‚СЂРѕРµРЅ Рё Р·РµР»РµРЅС‹Р№;
- release bundle Р°РІС‚РѕРјР°С‚РёР·РёСЂРѕРІР°РЅ;
- Windows/Docker setup РґРѕРєСѓРјРµРЅС‚РёСЂРѕРІР°РЅ Рё РїСЂРѕРІРµСЂРµРЅ;
- BI-ready package СЃРѕР±РёСЂР°РµС‚СЃСЏ РІРѕСЃРїСЂРѕРёР·РІРѕРґРёРјРѕ;
- pipeline telemetry С„РёРєСЃРёСЂСѓРµС‚СЃСЏ РІ run manifest;
- archived docs deletion policy РІС‹РїРѕР»РЅРµРЅР° С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ stable release.

