# Production artifact policy

Р”Р°С‚Р°: 2026-06-04.

Р”РѕРєСѓРјРµРЅС‚ С„РёРєСЃРёСЂСѓРµС‚, РєР°РєРёРµ С„Р°Р№Р»С‹ РїСЂРѕРµРєС‚Р° OFZ_ANALYTICS СЃС‡РёС‚Р°СЋС‚СЃСЏ РёСЃС…РѕРґРЅРёРєР°РјРё, РєР°РєРёРµ СЏРІР»СЏСЋС‚СЃСЏ РІРѕСЃРїСЂРѕРёР·РІРѕРґРёРјС‹РјРё build artifacts, Р° РєР°РєРёРµ РЅСѓР¶РЅРѕ С…СЂР°РЅРёС‚СЊ РєР°Рє release/audit artifacts. РќР° СЌС‚РѕРј СЌС‚Р°РїРµ С„Р°Р№Р»С‹ РЅРµ СѓРґР°Р»СЏСЋС‚СЃСЏ Рё РЅРµ РїРµСЂРµРјРµС‰Р°СЋС‚СЃСЏ.

## РљР°С‚РµРіРѕСЂРёРё Р°СЂС‚РµС„Р°РєС‚РѕРІ

| РљР°С‚РµРіРѕСЂРёСЏ | РџСЂРёРјРµСЂС‹ | РҐСЂР°РЅРёС‚СЊ РІ git | РџРµСЂРµСЃРѕР·РґР°РµС‚СЃСЏ pipeline | Release artifact | Р›РѕРєР°Р»СЊРЅРѕРµ С…СЂР°РЅРµРЅРёРµ | РџСЂР°РІРёР»Рѕ Р°СЂС…РёРІР°С†РёРё |
|---|---|---:|---:|---:|---|---|
| Source code | `scripts/*.py`, `scripts/maintenance/*.py`, `scripts/README.md` | Р”Р° | РќРµС‚ | РќРµС‚ | РџРѕСЃС‚РѕСЏРЅРЅРѕ | РќРµ Р°СЂС…РёРІРёСЂРѕРІР°С‚СЊ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё; СѓСЃС‚Р°СЂРµРІС€РёРµ РІРµСЂСЃРёРё РїРµСЂРµРЅРѕСЃРёС‚СЊ С‚РѕР»СЊРєРѕ С‡РµСЂРµР· РѕС‚РґРµР»СЊРЅС‹Р№ migration/cleanup script. |
| Configuration | `requirements.txt`, future `.gitignore`, РЅР°СЃС‚СЂРѕР№РєРё Р·Р°РїСѓСЃРєР° Р±РµР· СЃРµРєСЂРµС‚РѕРІ | Р”Р° | РќРµС‚ | РќРµС‚ | РџРѕСЃС‚РѕСЏРЅРЅРѕ | РР·РјРµРЅРµРЅРёСЏ С„РёРєСЃРёСЂРѕРІР°С‚СЊ РІ changelog/manual checks; СЃРµРєСЂРµС‚С‹ РЅРµ С…СЂР°РЅРёС‚СЊ РІ СЂРµРїРѕР·РёС‚РѕСЂРёРё. |
| Stable documentation | `README.md`, `docs/index.md`, `docs/00_project/`, `docs/01_methodology/`, `docs/02_data_pipeline/`, `docs/03_analytics/`, `docs/04_visualization/`, `docs/05_dashboard/`, `docs/06_quality/` | Р”Р° | Р§Р°СЃС‚РёС‡РЅРѕ | РќРµС‚ | РџРѕСЃС‚РѕСЏРЅРЅРѕ | РЈСЃС‚Р°СЂРµРІС€РёРµ РґРѕРєСѓРјРµРЅС‚С‹ РїРµСЂРµРЅРѕСЃРёС‚СЊ РІ `docs/90_archive/` С‡РµСЂРµР· maintenance-СЃРєСЂРёРїС‚С‹. |
| Generated reports | `outputs/reports/*.md`, `outputs/reports/*.xlsx`, analytical/monthly/revenue reports | РџРѕ СЂРµС€РµРЅРёСЋ СЂРµР»РёР·Р° | Р”Р° | Р”Р°, РґР»СЏ СѓС‚РІРµСЂР¶РґРµРЅРЅС‹С… Р·Р°РїСѓСЃРєРѕРІ | 30-90 РґРЅРµР№ Р»РѕРєР°Р»СЊРЅРѕ РґР»СЏ СЂР°Р±РѕС‡РёС… Р·Р°РїСѓСЃРєРѕРІ | РџРѕСЃР»Рµ СѓС‚РІРµСЂР¶РґРµРЅРёСЏ СЂРµР»РёР·Р° СЃРѕС…СЂР°РЅСЏС‚СЊ РІ release bundle; СЃС‚Р°СЂС‹Рµ СЂР°Р±РѕС‡РёРµ СЂРµР·СѓР»СЊС‚Р°С‚С‹ РїРµСЂРµРЅРѕСЃРёС‚СЊ РІ `outputs/archive/`. |
| Chart HTML | `outputs/charts/**/*.html` | РџРѕ СЂРµС€РµРЅРёСЋ СЂРµР»РёР·Р°; РЅРµ РёРіРЅРѕСЂРёСЂРѕРІР°С‚СЊ РґРѕ С„РёРЅР°Р»СЊРЅРѕРіРѕ СЂРµС€РµРЅРёСЏ | Р”Р° | Р”Р°, РґР»СЏ СѓС‚РІРµСЂР¶РґРµРЅРЅС‹С… Р·Р°РїСѓСЃРєРѕРІ | 30 РґРЅРµР№ Р»РѕРєР°Р»СЊРЅРѕ РґР»СЏ СЂР°Р±РѕС‡РёС… Р·Р°РїСѓСЃРєРѕРІ; РґРѕР»СЊС€Рµ РґР»СЏ СЂРµР»РёР·РѕРІ | РўСЏР¶РµР»С‹Рµ HTML СЃРєР»Р°РґС‹РІР°С‚СЊ РІ release artifact РёР»Рё Р°СЂС…РёРІРёСЂРѕРІР°С‚СЊ; РЅРµ СѓРґР°Р»СЏС‚СЊ Р±РµР· `--dry-run` Рё `--archive`. |
| Chart data CSV | `outputs/exports/chart_data/**/*.csv` | РџРѕ СЂРµС€РµРЅРёСЋ СЂРµР»РёР·Р°; РЅРµ РёРіРЅРѕСЂРёСЂРѕРІР°С‚СЊ РґРѕ С„РёРЅР°Р»СЊРЅРѕРіРѕ СЂРµС€РµРЅРёСЏ | Р”Р° | Р”Р°, РµСЃР»Рё РЅСѓР¶РµРЅ audit/reproducibility package | 30-90 РґРЅРµР№ Р»РѕРєР°Р»СЊРЅРѕ | РђСЂС…РёРІРёСЂРѕРІР°С‚СЊ РІРјРµСЃС‚Рµ СЃ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РёРјРё HTML, С‡С‚РѕР±С‹ РіСЂР°С„РёРє РјРѕР¶РЅРѕ Р±С‹Р»Рѕ РїСЂРѕРІРµСЂРёС‚СЊ Р±РµР· РїРµСЂРµСЃС‡РµС‚Р°. |
| Dashboard exports | `outputs/dashboards/**/*.csv`, semantic model v2 | РџРѕ СЂРµС€РµРЅРёСЋ СЂРµР»РёР·Р° | Р”Р° | Р”Р° | 30-90 РґРЅРµР№ Р»РѕРєР°Р»СЊРЅРѕ; СЂРµР»РёР·РЅС‹Рµ РІРµСЂСЃРёРё С…СЂР°РЅРёС‚СЊ РґРѕР»СЊС€Рµ | РђСЂС…РёРІРёСЂРѕРІР°С‚СЊ РїРѕ run_id/report_date; РЅРµ СЃРјРµС€РёРІР°С‚СЊ СЂР°Р·РЅС‹Рµ `aggregation_mode`. |
| Run manifests | `outputs/reports/run_manifest_*.json`, `outputs/reports/run_manifest_*.md`, `data/processed/run_manifest_latest.json` | Latest РјРѕР¶РЅРѕ РЅРµ С…СЂР°РЅРёС‚СЊ; СЂРµР»РёР·РЅС‹Рµ manifests С…СЂР°РЅРёС‚СЊ РєР°Рє audit artifact | Р”Р° | Р”Р° | РџРѕСЃС‚РѕСЏРЅРЅРѕ РґР»СЏ СЂРµР»РёР·РѕРІ; 90 РґРЅРµР№ РґР»СЏ СЂР°Р±РѕС‡РёС… Р·Р°РїСѓСЃРєРѕРІ | Р РµР»РёР·РЅС‹Рµ manifests РЅРµ СѓРґР°Р»СЏС‚СЊ; СЂР°Р±РѕС‡РёРµ РїРµСЂРµРЅРѕСЃРёС‚СЊ РІ archive РїРѕСЃР»Рµ СѓСЃС‚Р°СЂРµРІР°РЅРёСЏ. |
| Logs | `logs/*.log`, runtime traces | РќРµС‚ | Р”Р° | РќРµС‚, РєСЂРѕРјРµ РёРЅС†РёРґРµРЅС‚РѕРІ | 14-30 РґРЅРµР№ Р»РѕРєР°Р»СЊРЅРѕ | Р РѕС‚РёСЂРѕРІР°С‚СЊ/Р°СЂС…РёРІРёСЂРѕРІР°С‚СЊ РїСЂРё РёРЅС†РёРґРµРЅС‚Р°С…; РѕР±С‹С‡РЅС‹Рµ logs РјРѕР¶РЅРѕ РёСЃРєР»СЋС‡РёС‚СЊ РёР· git. |
| Archive | `outputs/archive/`, `docs/90_archive/` | Docs archive РјРѕР¶РЅРѕ С…СЂР°РЅРёС‚СЊ; outputs archive РѕР±С‹С‡РЅРѕ РЅРµ С…СЂР°РЅРёС‚СЊ | РќРµС‚ | РўРѕР»СЊРєРѕ РµСЃР»Рё Р°СЂС…РёРІ СЏРІР»СЏРµС‚СЃСЏ С‡Р°СЃС‚СЊСЋ СЂРµР»РёР·Р° | РџРѕ РїРѕР»РёС‚РёРєРµ СЂРµР»РёР·Р° | РЈРґР°Р»РµРЅРёРµ С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ `--dry-run`, Р·Р°С‚РµРј `--archive`, Р·Р°С‚РµРј `--delete-archived` РїСЂРё СЏРІРЅРѕРј СЂР°Р·СЂРµС€РµРЅРёРё. |

## РЎРїРµС†РёР°Р»СЊРЅС‹Рµ РїСЂР°РІРёР»Р° outputs

### `outputs/charts/`

`outputs/charts/` СЃРѕРґРµСЂР¶РёС‚ С‚СЏР¶РµР»С‹Рµ HTML artifacts. Baseline РїРµСЂРµРґ production-cleanup РїРѕРєР°Р·С‹РІР°Р» РѕРєРѕР»Рѕ 97 HTML-С„Р°Р№Р»РѕРІ Рё РїСЂРёРјРµСЂРЅРѕ 447 MB РІ `outputs/charts/`.

РџСЂР°РІРёР»Рѕ:

- HTML-РіСЂР°С„РёРєРё СЃС‡РёС‚Р°СЋС‚СЃСЏ build artifacts, РїРѕС‚РѕРјСѓ С‡С‚Рѕ РїРµСЂРµСЃРѕР·РґР°СЋС‚СЃСЏ pipeline.
- Р”Р»СЏ СЂР°Р±РѕС‡РёС… Р·Р°РїСѓСЃРєРѕРІ HTML РЅРµ РѕР±СЏР·Р°РЅС‹ С…СЂР°РЅРёС‚СЊСЃСЏ РІ git.
- Р”Р»СЏ СЂРµР»РёР·РЅРѕРіРѕ Р·Р°РїСѓСЃРєР° HTML РґРѕР»Р¶РЅС‹ СЃРѕС…СЂР°РЅСЏС‚СЊСЃСЏ РєР°Рє release artifact РІРјРµСЃС‚Рµ СЃ run manifest Рё chart data CSV.
- Р”Рѕ РѕРєРѕРЅС‡Р°С‚РµР»СЊРЅРѕРіРѕ СЂРµС€РµРЅРёСЏ РїРѕ СЂРµР»РёР·РЅРѕРјСѓ РїСЂРѕС†РµСЃСЃСѓ РЅРµ РґРѕР±Р°РІР»СЏС‚СЊ `outputs/charts/**/*.html` РІ `.gitignore`.

### `outputs/exports/chart_data/`

`outputs/exports/chart_data/` СЃРѕРґРµСЂР¶РёС‚ РІРѕСЃРїСЂРѕРёР·РІРѕРґРёРјС‹Рµ CSV-РѕСЃРЅРѕРІС‹ РіСЂР°С„РёРєРѕРІ.

РџСЂР°РІРёР»Рѕ:

- CSV-РѕСЃРЅРѕРІС‹ СЃС‡РёС‚Р°СЋС‚СЃСЏ build artifacts, РЅРѕ РІР°Р¶РЅС‹ РґР»СЏ Р°СѓРґРёС‚Р° РіСЂР°С„РёРєРѕРІ.
- Р”Р»СЏ production release СЂРµРєРѕРјРµРЅРґСѓРµС‚СЃСЏ С…СЂР°РЅРёС‚СЊ РёС… РєР°Рє release artifact РІРјРµСЃС‚Рµ СЃ HTML-РіСЂР°С„РёРєР°РјРё.
- Р’СЃРµ РїРѕР»СЏ `*_volume_bln` РґРѕР»Р¶РЅС‹ СЃРѕРїСЂРѕРІРѕР¶РґР°С‚СЊСЃСЏ unit-РїРѕР»СЏРјРё СЃРѕРіР»Р°СЃРЅРѕ `docs/02_data_contracts/chart_data_contract.md`.
- Р”Рѕ РѕРєРѕРЅС‡Р°С‚РµР»СЊРЅРѕРіРѕ СЂРµС€РµРЅРёСЏ РїРѕ СЂРµР»РёР·РЅРѕРјСѓ РїСЂРѕС†РµСЃСЃСѓ РЅРµ РґРѕР±Р°РІР»СЏС‚СЊ `outputs/exports/**/*.csv` РІ `.gitignore`.

### `outputs/dashboards/`

`outputs/dashboards/` СЃРѕРґРµСЂР¶РёС‚ BI-ready exports, semantic model v2 Рё СЃР»РѕРІР°СЂРё.

РџСЂР°РІРёР»Рѕ:

- Dashboard exports СЃС‡РёС‚Р°СЋС‚СЃСЏ release artifacts, РµСЃР»Рё Р·Р°РїСѓСЃРє СѓС‚РІРµСЂР¶РґРµРЅ РєР°Рє РѕС‚С‡РµС‚РЅС‹Р№.
- Р”Р»СЏ СЂР°Р±РѕС‡РёС… РїСЂРѕРіРѕРЅРѕРІ РѕРЅРё РїРµСЂРµСЃРѕР·РґР°СЋС‚СЃСЏ pipeline Рё РјРѕРіСѓС‚ Р°СЂС…РёРІРёСЂРѕРІР°С‚СЊСЃСЏ РїРѕ run_id/report_date.
- Semantic model v2 Рё data dictionaries РґРѕР»Р¶РЅС‹ С…СЂР°РЅРёС‚СЊСЃСЏ РІРјРµСЃС‚Рµ СЃ СЂРµР»РёР·РЅС‹Рј dashboard package.

### `outputs/reports/run_manifests/`

РўРµРєСѓС‰Р°СЏ СЃС‚СЂСѓРєС‚СѓСЂР° РїСЂРѕРµРєС‚Р° СЃРѕС…СЂР°РЅСЏРµС‚ run manifests РІ `outputs/reports/` Рё latest manifest РІ `data/processed/run_manifest_latest.json`. Р›РѕРіРёС‡РµСЃРєР°СЏ production-РєР°С‚РµРіРѕСЂРёСЏ: `outputs/reports/run_manifests/`.

РџСЂР°РІРёР»Рѕ:

- Run manifest СЏРІР»СЏРµС‚СЃСЏ audit trail.
- Р РµР»РёР·РЅС‹Р№ manifest С…СЂР°РЅРёС‚СЊ РєР°Рє release artifact.
- `run_manifest_latest.json` СЏРІР»СЏРµС‚СЃСЏ СЂР°Р±РѕС‡РёРј СѓРєР°Р·Р°С‚РµР»РµРј Рё РјРѕР¶РµС‚ РїРµСЂРµСЃРѕР·РґР°РІР°С‚СЊСЃСЏ.
- РџСЂРё Р±СѓРґСѓС‰РµР№ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё РґРѕРїСѓСЃС‚РёРјРѕ РІС‹РґРµР»РёС‚СЊ С„РёР·РёС‡РµСЃРєСѓСЋ РїР°РїРєСѓ `outputs/reports/run_manifests/`, РЅРѕ С‚РѕР»СЊРєРѕ С‡РµСЂРµР· РѕС‚РґРµР»СЊРЅС‹Р№ dry-run/apply maintenance-Р±Р»РѕРє.

## Release bundle

РњРёРЅРёРјР°Р»СЊРЅС‹Р№ production release bundle РґРѕР»Р¶РµРЅ РІРєР»СЋС‡Р°С‚СЊ:

- run manifest (`json` Рё `md`);
- РїР°СЂР°РјРµС‚СЂС‹ Р·Р°РїСѓСЃРєР° (`report_date`, `period_type`, `aggregation_mode`, `retrospective_years`);
- analytical/monthly/revenue reports;
- dashboard exports Рё semantic model v2;
- HTML-РіСЂР°С„РёРєРё;
- chart data CSV;
- quality gate report;
- visual regression report РёР»Рё fallback inspection report;
- schema validation report;
- anomaly/regression/smoke test reports, РµСЃР»Рё РѕРЅРё Р·Р°РїСѓСЃРєР°Р»РёСЃСЊ.

## Р РµРєРѕРјРµРЅРґСѓРµРјС‹Р№ `.gitignore`

`.gitignore` РІ РїСЂРѕРµРєС‚Рµ РЅР° РјРѕРјРµРЅС‚ СЃРѕР·РґР°РЅРёСЏ policy РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚. РќРёР¶Рµ РїСЂРёРІРµРґРµРЅ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ С€Р°Р±Р»РѕРЅ. РќРµ РІС‹РїРѕР»РЅСЏС‚СЊ `git init` Рё РЅРµ СЃРѕР·РґР°РІР°С‚СЊ `.gitignore` Р±РµР· РѕС‚РґРµР»СЊРЅРѕРіРѕ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ.

```gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
logs/
*.log

# Optional depending on artifact_policy.md
outputs/archive/
outputs/tmp/
outputs/cache/
```

## Production cleanup addendum

Р­С‚РѕС‚ СЂР°Р·РґРµР» СѓС‚РѕС‡РЅСЏРµС‚ РїСЂР°РІРёР»Р° РїРѕР»РЅРѕР№ РѕС‡РёСЃС‚РєРё `outputs/` РїРµСЂРµРґ production-РїРµСЂРµРіРµРЅРµСЂР°С†РёРµР№.

### Working, release, archive and audit outputs

| РЎРѕСЃС‚РѕСЏРЅРёРµ | Р§С‚Рѕ СЌС‚Рѕ | Git policy | Cleanup policy |
|---|---|---|---|
| Working outputs | РўРµРєСѓС‰РёРµ СЂРµР·СѓР»СЊС‚Р°С‚С‹ Р»РѕРєР°Р»СЊРЅС‹С… РїСЂРѕРіРѕРЅРѕРІ pipeline РІ `outputs/`. | РћР±С‹С‡РЅРѕ РЅРµ РєРѕРјРјРёС‚РёС‚СЊ Р±РµР· СЂРµС€РµРЅРёСЏ release process. | РњРѕР¶РЅРѕ РѕС‡РёС‰Р°С‚СЊ РїРµСЂРµРґ production-РїРµСЂРµРіРµРЅРµСЂР°С†РёРµР№ С‚РѕР»СЊРєРѕ С‡РµСЂРµР· `scripts/maintenance/cleanup_outputs.py`. |
| Release artifacts | РЈС‚РІРµСЂР¶РґРµРЅРЅС‹Р№ РЅР°Р±РѕСЂ РѕС‚С‡РµС‚РѕРІ, РіСЂР°С„РёРєРѕРІ, CSV Рё dashboard exports РґР»СЏ РєРѕРЅРєСЂРµС‚РЅРѕРіРѕ Р·Р°РїСѓСЃРєР°. | РџРѕ СЂРµС€РµРЅРёСЋ СЂРµР»РёР·Р°; РјРѕР¶РµС‚ С…СЂР°РЅРёС‚СЊСЃСЏ РІРЅРµ git РєР°Рє release package. | РќРµ СѓРґР°Р»СЏС‚СЊ РѕР±С‹С‡РЅС‹Рј cleanup Р±РµР· РѕС‚РґРµР»СЊРЅРѕРіРѕ СЂРµС€РµРЅРёСЏ. |
| Archive outputs | РџРµСЂРµРЅРµСЃРµРЅРЅС‹Рµ СЃС‚Р°СЂС‹Рµ РёР»Рё СЂР°Р±РѕС‡РёРµ СЂРµР·СѓР»СЊС‚Р°С‚С‹ РІ `outputs/archive/`. | РћР±С‹С‡РЅРѕ РЅРµ С…СЂР°РЅРёС‚СЊ РІ git. | РЈРґР°Р»РµРЅРёРµ С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ РѕС‚РґРµР»СЊРЅРѕРіРѕ dry-run/archive/delete РїСЂРѕС‚РѕРєРѕР»Р°. |
| Audit artifacts | Run manifest, quality gate, schema validation, visual regression, executive summary Рё data quality summary. | Р РµР»РёР·РЅС‹Рµ РІРµСЂСЃРёРё С…СЂР°РЅРёС‚СЊ РєР°Рє audit trail. | Р РµР»РёР·РЅС‹Рµ audit artifacts РЅРµ СѓРґР°Р»СЏС‚СЊ; disposable latest-С„Р°Р№Р»С‹ РјРѕР¶РЅРѕ РїРµСЂРµСЃРѕР·РґР°РІР°С‚СЊ. |

### Clean outputs before production run

РџРµСЂРµРґ production-РїРµСЂРµРіРµРЅРµСЂР°С†РёРµР№ outputs РґРѕРїСѓСЃРєР°РµС‚СЃСЏ РїРѕР»РЅРѕСЃС‚СЊСЋ РѕС‡РёС‰Р°С‚СЊ generated artifacts, РЅРѕ С‚РѕР»СЊРєРѕ РїРѕ СЏРІРЅРѕРјСѓ РїСЂРѕС‚РѕРєРѕР»Сѓ.

Р Р°Р·СЂРµС€РµРЅРЅС‹Р№ РёРЅСЃС‚СЂСѓРјРµРЅС‚:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --dry-run
```

РџРѕСЂСЏРґРѕРє РґРµР№СЃС‚РІРёР№:

1. Р’С‹РїРѕР»РЅРёС‚СЊ `--dry-run` Рё РїСЂРѕРІРµСЂРёС‚СЊ РѕС‚С‡РµС‚.
2. Р•СЃР»Рё С‚РµРєСѓС‰РёРµ СЂРµР·СѓР»СЊС‚Р°С‚С‹ РјРѕРіСѓС‚ РїРѕРЅР°РґРѕР±РёС‚СЊСЃСЏ РґР»СЏ Р°СѓРґРёС‚Р°, СЃРЅР°С‡Р°Р»Р° СЃРѕР·РґР°С‚СЊ archive bundle:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all
```

3. РўРѕР»СЊРєРѕ РїРѕСЃР»Рµ РїСЂРѕРІРµСЂРєРё archive policy РІС‹РїРѕР»РЅРёС‚СЊ СѓРґР°Р»РµРЅРёРµ:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --delete-all --confirm DELETE_OUTPUTS
```

4. РџРѕСЃР»Рµ РѕС‡РёСЃС‚РєРё РѕР±СЏР·Р°С‚РµР»СЊРЅРѕ РІС‹РїРѕР»РЅРёС‚СЊ production-РїРµСЂРµРіРµРЅРµСЂР°С†РёСЋ:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

5. РџРѕСЃР»Рµ pipeline РѕР±СЏР·Р°С‚РµР»СЊРЅРѕ РІС‹РїРѕР»РЅРёС‚СЊ quality gate:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

РџСЂРµРґСѓРїСЂРµР¶РґРµРЅРёРµ: РїРѕР»РЅР°СЏ РѕС‡РёСЃС‚РєР° outputs СѓРґР°Р»СЏРµС‚ РІСЃРµ generated artifacts, РєСЂРѕРјРµ СЃРѕС…СЂР°РЅРµРЅРЅРѕРіРѕ archive. Р—Р°РїСѓСЃРєР°С‚СЊ С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ dry-run Рё РїСЂРѕРІРµСЂРєРё archive policy.

### Archive bundle before cleanup

РџРµСЂРµРґ РїРѕР»РЅРѕР№ РѕС‡РёСЃС‚РєРѕР№ outputs, РµСЃР»Рё СЂРµР·СѓР»СЊС‚Р°С‚С‹ РјРѕРіСѓС‚ РїРѕРЅР°РґРѕР±РёС‚СЊСЃСЏ РґР»СЏ Р°СѓРґРёС‚Р°, РЅСѓР¶РЅРѕ СЃРѕР·РґР°С‚СЊ release/work archive bundle.

РњРёРЅРёРјР°Р»СЊРЅС‹Р№ СЃРѕСЃС‚Р°РІ archive bundle:

- run manifest `json` Рё `md`;
- quality gate report;
- schema validation report;
- HTML charts;
- chart data CSV;
- dashboard exports;
- executive summary;
- data quality summary, РµСЃР»Рё РµСЃС‚СЊ.

Archive bundle РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ СЃРІСЏР·Р°РЅ СЃ РїР°СЂР°РјРµС‚СЂР°РјРё Р·Р°РїСѓСЃРєР°: `report_date`, `period_type`, `aggregation_mode`, `retrospective_years`, `run_id`.

### Run manifest retention

Run manifest СЏРІР»СЏРµС‚СЃСЏ audit trail.

РџСЂР°РІРёР»Р°:

- СЂРµР»РёР·РЅС‹Рµ manifests РЅРµ СѓРґР°Р»СЏС‚СЊ;
- `run_manifest_latest.json` РјРѕР¶РЅРѕ РїРµСЂРµСЃРѕР·РґР°РІР°С‚СЊ;
- РµСЃР»Рё outputs РѕС‡РёС‰Р°СЋС‚СЃСЏ, С‚РµРєСѓС‰РёР№ manifest РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ Р»РёР±Рѕ Р·Р°Р°СЂС…РёРІРёСЂРѕРІР°РЅ, Р»РёР±Рѕ СЏРІРЅРѕ РїСЂРёР·РЅР°РЅ disposable РІ cleanup report;
- РґР»СЏ release bundle manifest СЏРІР»СЏРµС‚СЃСЏ РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рј С„Р°Р№Р»РѕРј.

### `outputs/archive/`

`outputs/archive/` РѕР±С‹С‡РЅРѕ РЅРµ С…СЂР°РЅРёС‚СЃСЏ РІ git, РїРѕС‚РѕРјСѓ С‡С‚Рѕ СЃРѕРґРµСЂР¶РёС‚ С‚СЏР¶РµР»С‹Рµ Рё СѓСЃС‚Р°СЂРµРІР°СЋС‰РёРµ generated artifacts.

РСЃРєР»СЋС‡РµРЅРёРµ: release archive РјРѕР¶РµС‚ С…СЂР°РЅРёС‚СЊСЃСЏ РєР°Рє РІРЅРµС€РЅРёР№ release artifact, РµСЃР»Рё РѕРЅ РЅСѓР¶РµРЅ РґР»СЏ Р°СѓРґРёС‚Р° РёР»Рё РїРµСЂРµРґР°С‡Рё СЂРµР·СѓР»СЊС‚Р°С‚Р°.

`cleanup_outputs.py` РЅРµ РґРѕР»Р¶РµРЅ СѓРґР°Р»СЏС‚СЊ archive, СЃРѕР·РґР°РЅРЅС‹Р№ РІ С‚РѕРј Р¶Рµ Р·Р°РїСѓСЃРєРµ. Р­С‚Рѕ Р·Р°С‰РёС‰Р°РµС‚ СЃС†РµРЅР°СЂРёР№ `--archive-all` -> РїСЂРѕРІРµСЂРєР° -> РїРѕСЃР»РµРґСѓСЋС‰Р°СЏ РѕС‡РёСЃС‚РєР° working outputs.

Р’Р°Р¶РЅРѕ: РЅРµ РґРѕР±Р°РІР»СЏС‚СЊ `outputs/charts/**/*.html` Рё `outputs/exports/**/*.csv` РІ `.gitignore`, РїРѕРєР° artifact policy Рё release process СЏРІРЅРѕ РЅРµ СЂРµС€Р°С‚, С‡С‚Рѕ СЌС‚Рё Р°СЂС‚РµС„Р°РєС‚С‹ РЅРµ РєРѕРјРјРёС‚СЏС‚СЃСЏ.

## Cleanup gates

РџРµСЂРµРґ РѕС‡РёСЃС‚РєРѕР№ Р°СЂС‚РµС„Р°РєС‚РѕРІ РѕР±СЏР·Р°С‚РµР»СЊРЅРѕ:

1. Р’С‹РїРѕР»РЅРёС‚СЊ cleanup script РІ СЂРµР¶РёРјРµ `--dry-run`.
2. РџСЂРѕРІРµСЂРёС‚СЊ РѕС‚С‡РµС‚ dry-run.
3. Р’С‹РїРѕР»РЅРёС‚СЊ `--archive`, РµСЃР»Рё РїРµСЂРµРЅРѕСЃ СЃРѕРіР»Р°СЃРѕРІР°РЅ.
4. Р’С‹РїРѕР»РЅРёС‚СЊ `--delete-archived` С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ РѕС‚РґРµР»СЊРЅРѕРіРѕ СЏРІРЅРѕРіРѕ СЂР°Р·СЂРµС€РµРЅРёСЏ.
5. РџРѕСЃР»Рµ РєСЂСѓРїРЅРѕРіРѕ Р±Р»РѕРєР° Р·Р°РїСѓСЃС‚РёС‚СЊ:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## 2026-06-04 - `.gitignore` created

`.gitignore` created in the project root after artifact policy confirmation.

Current ignore rules:

```gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
logs/
*.log

outputs/archive/
outputs/tmp/
outputs/cache/
```

Not ignored by design:

- `outputs/charts/**/*.html`;
- `outputs/exports/**/*.csv`.

These HTML and CSV artifacts remain outside `.gitignore` until the release process explicitly decides that they should not be committed.

## 2026-06-04 - first commit strategy

Decision: generated outputs are not included in the first Git commit.

The first commit should include source/configuration/documentation/contracts:

- source code: `scripts/**/*.py`;
- maintenance scripts: `scripts/maintenance/**/*.py`;
- project documentation: `README.md`, `CHANGELOG.md`, `docs/**/*.md`;
- configuration and dependency files: `.gitignore`, `requirements.txt`;
- data contracts and methodology docs.

Generated outputs are not committed to ordinary Git history:

- `outputs/charts/**/*.html`;
- `outputs/exports/**/*.csv`;
- `outputs/reports/**`;
- `outputs/dashboards/**`.

Generated processed data is also excluded from the ordinary source commit:

- `data/processed/**`.

Rationale:

- no single generated file above 50 MB was found before the first commit;
- however `outputs/charts/` is a heavy generated zone, approximately 447 MB by baseline;
- committing generated HTML/CSV/report/dashboard outputs into normal Git history would make the repository heavy and noisy;
- production artifacts should be distributed as release bundles or external artifacts.

Generated outputs should be preserved as one of:

- release bundle;
- external artifact;
- archived local artifact;
- GitHub Release asset, if this process is configured later.

Reproducibility should rely on:

- run manifest;
- raw file hashes;
- data contracts;
- scripts;
- `requirements.txt`;
- quality reports;
- schema validation reports;
- visual regression / HTML QA reports.

If a specific reporting run must be preserved completely, package its outputs into a release bundle instead of committing files individually into Git history.

Exceptions:

- empty output folder structure may be preserved via `.gitkeep`;
- small `README.md` or `index.md` files inside `outputs/` may be committed when they are useful as navigation or documentation.

This decision can be revisited later, but only through a separate release-process decision.

## 2026-06-04 - `data/raw` source dataset policy

`data/raw` is treated as a source dataset of the project and is committed to Git when both conditions hold:

- files are small enough for normal Git history;
- files do not contain confidential data.

For the first commit, `data/raw` was checked manually:

- no heavy files were found;
- listed Excel files are about 0.02-0.03 MB each;
- no temporary Excel/cache files were found by patterns `~$*.xlsx`, `*.tmp`, `*.bak`;
- the user confirmed that no confidential data was detected by manual review.

Raw file hashes are tracked through raw data registry and run manifest. Pipeline scripts must not modify `data/raw` in place.

## 2026-06-04 - Git policy for `data/raw`

`data/raw` is committed to Git as the source dataset of the project.

Decision rationale:

- raw files are small, approximately up to 0.03 MB each;
- no heavy raw files were found;
- `data/raw` is required for reproducible pipeline execution from source data;
- data was approved by the user as acceptable for repository storage.

`data/raw` must not be added to `.gitignore`. Raw file hashes are fixed in the raw data registry and/or run manifest. Generated outputs remain excluded from normal Git history and are recreated by the pipeline or preserved as release artifacts.

## 2026-06-05 - Git policy for `data/processed`

`data/processed` is treated as reproducible working output of the pipeline, not as the source dataset.

Decision:

- `data/raw` is committed as source data;
- `data/processed/**` is excluded from the first source commit via `.gitignore`;
- processed CSV/JSON files should be recreated by pipeline stages or preserved in release bundles when a run must be audited;
- latest runtime files such as `data/processed/run_manifest_latest.json` are working artifacts and can be regenerated.

## 2026-06-05 - GitHub repository and post-push artifact strategy

Version control state after the first push:

- Repository: GitHub / `OFZ_ANALYTICS`;
- Remote: `https://github.com/VinogradovPV/OFZ_ANALYTICS.git`;
- Default branch: `main`;
- Visibility: private;
- Initial commit: `4fa6d61fa67281c20d5d7a878cd2191e953507bc`;
- Initial commit message: `Initial source dataset and OFZ analytics pipeline`.

The first commit includes:

- source code and scripts;
- configuration files and dependency contract;
- stable project documentation and data contracts;
- prompt source assets;
- `data/raw` source dataset;
- `.gitkeep` files and lightweight navigation files for the `outputs/` skeleton.

The first commit excludes generated artifacts:

- generated HTML charts;
- generated chart data CSV exports;
- generated reports;
- dashboard exports;
- local archives, cache and temporary outputs;
- `data/processed` working data.

Generated outputs are recreated by the pipeline. When a specific reporting run must be preserved for audit or delivery, outputs should be packed into a release bundle or stored as an external artifact. The repository keeps reproducibility through source scripts, data contracts, `requirements.txt`, raw file hashes, raw data registry, run manifests and quality reports.

## 2026-06-05 - production Git artifact policy

This section supersedes earlier draft notes that said HTML/CSV outputs should not be ignored until the release process is decided. The release process decision has now been made for the production-ready baseline.

### Source artifacts

Source artifacts are tracked in Git:

- `scripts/**/*.py`;
- `scripts/**/*.md`;
- `docs/**/*.md`;
- `README.md`;
- `CHANGELOG.md`;
- `prompts/**`;
- `.gitignore`;
- `requirements.txt`;
- `requirements-dev.txt`;
- `pyproject.toml`;
- data contracts and methodology documentation;
- `data/raw/**`.

`data/raw` is committed as the project source dataset because the files are small, required for reproducibility and approved for repository storage. Pipeline scripts must not modify `data/raw` in place.

### Generated artifacts

Generated artifacts are not tracked in ordinary Git history:

- `outputs/charts/**/*.html`;
- `outputs/exports/**/*.csv`;
- `outputs/reports/**`;
- `outputs/dashboards/**`;
- `outputs/archive/**`;
- `outputs/tmp/**`;
- `outputs/cache/**`;
- `data/processed/**`;
- `logs/**`.

Generated artifacts are recreated by the pipeline, archived locally when needed, or packaged as external release artifacts.

### Git tracking policy

The Git repository stores source/config/docs/scripts/contracts/prompts and the small source dataset in `data/raw`.

The repository must not commit generated outputs. Before every commit, check staged files:

```powershell
git diff --cached --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|data/processed|logs"
```

If generated outputs are staged, remove them from the index without deleting local files:

```powershell
git rm --cached -r outputs/charts outputs/exports outputs/reports outputs/dashboards outputs/archive outputs/tmp data/processed
```

### Outputs skeleton exception

The empty/structural `outputs/` skeleton may be tracked:

- `outputs/**/.gitkeep`;
- small `outputs/**/README.md`;
- small `outputs/**/index.md`.

This exception exists only for navigation and folder discoverability. It does not allow committing generated HTML, CSV, XLSX, JSON or report artifacts from `outputs/`.

### Release bundle policy

If a reporting run must be preserved, create an external release bundle instead of committing outputs individually.

Minimum release bundle contents:

- run manifest `json` and `md`;
- quality gate report;
- schema validation report;
- HTML charts;
- chart data CSV;
- dashboard exports and semantic model;
- executive summary;
- analytical/monthly/revenue reports;
- visual regression or fallback HTML inspection report;
- anomaly/regression/smoke test reports when they were part of the run;
- data quality summary when available.

The release bundle must record `report_date`, `period_type`, `aggregation_mode`, `retrospective_years`, `run_id`, commit hash and raw file hashes.

### Clean outputs before production run

Before production regeneration, working outputs may be cleaned only through a maintenance script with an explicit safety flow.

Allowed protocol:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --dry-run
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --delete-all --confirm DELETE_OUTPUTS
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all --delete-all --confirm DELETE_OUTPUTS
```

Rules:

- start with `--dry-run`;
- archive first if current outputs may be needed for audit;
- delete only after archive policy is checked;
- after cleanup, run the pipeline and quality gate;
- never delete `data/raw`;
- never commit generated outputs after regeneration.
- cleanup reports and manifests under `outputs/` are generated artifacts and are not committed.

Warning: full outputs cleanup deletes generated artifacts except the preserved archive. Run it only after dry-run and archive-policy review.

### Run manifest policy

Run manifest is the audit trail of a production run.

Rules:

- release manifests are not deleted;
- `run_manifest_latest.json` is a working pointer and may be regenerated;
- if outputs are cleaned, the current manifest must be archived or explicitly marked disposable in the cleanup report;
- release bundles must include the run manifest and raw file hashes.

### `outputs/archive/` policy

`outputs/archive/` is normally not tracked in Git.

Allowed storage:

- local archive for short-term retention;
- external release artifact;
- GitHub Release asset, if the release process later enables it.

`cleanup_outputs.py` must not delete an archive created in the same cleanup run.

The implemented cleanup command also preserves existing `outputs/archive/` during `--delete-all`. Removing old archives requires a separate, explicit archive-retention step and is not part of this command.

### Commit prohibition

Generated outputs are prohibited from ordinary commits. The only allowed tracked files under `outputs/` are skeleton/navigation files described above.
## P2.1 release bundle automation note

Р”Р°С‚Р°: 2026-06-09.

External release bundles are created under `releases/` by `ofz-build-release-bundle` / `scripts/maintenance/build_release_bundle.py`. The `releases/` directory is ignored by Git. A real bundle requires `--include-outputs --confirm BUILD_RELEASE_BUNDLE`; dry-run reports planned contents and missing categories without writing files.

## P2.6 UI launcher artifact policy

Р”Р°С‚Р°: 2026-06-11.

CLI remains the main supported production interface. UI launchers are controlled wrappers around approved CLI entry points and do not replace `ofz-quality`, `ofz-schema`, release checklist or manual release approval.

### Source artifacts

The following UI launcher files are source artifacts and may be tracked in Git:

- PowerShell launcher source: `tools/windows_launcher/*.ps1`;
- Word VBA source modules: `tools/word_launcher/*.bas`;
- Word VBA form source: `tools/word_launcher/*.frm`;
- launcher documentation under `docs/07_operations/`.

PowerShell GUI launcher is the recommended Windows UI MVP. Word VBA launcher is optional.

### Generated and release artifacts

The following files are not ordinary source artifacts:

- launcher logs: `outputs/reports/launcher/*.log`;
- Word macro-enabled documents: `*.docm`;
- release bundles under `releases/`.

Policy:

- launcher logs are generated outputs and must not be committed;
- `.docm` is a release artifact unless explicitly approved by a separate artifact policy decision;
- release bundle remains an external artifact and must not be committed to ordinary Git history;
- delete cleanup from any UI launcher requires `DELETE_OUTPUTS`;
- release bundle creation from any UI launcher requires `BUILD_RELEASE_BUNDLE`;
- UI launchers must not create GitHub releases without a separate explicit release command and policy;
- UI launchers must not accept arbitrary shell command input;
- UI launchers may start quality checks only by explicit user selection and must not run fast/full quality gates in parallel.

## P2.6.2 Word DOCM Assembly Policy

Дата: 2026-06-11.

Word launcher source files are tracked source artifacts:

- `tools/word_launcher/OfzLauncher.bas`;
- `tools/word_launcher/frmOfzLauncher.frm`;
- `tools/word_launcher/word_docm_build_instructions.md`.

Word macro-enabled documents are release artifacts:

- `*.docm`;
- `*.dotm`;
- `releases/ui_launcher/ofz_launcher_word_<timestamp>.docm`.

Rules:

- `.docm` is not committed to ordinary Git history without a separate explicit artifact policy approval;
- `releases/` remains ignored and external;
- Word launcher logs under `outputs/reports/launcher/` remain generated outputs;
- Word launcher source must call only whitelisted CLI entry points;
- delete cleanup requires `DELETE_OUTPUTS`;
- release bundle creation requires `BUILD_RELEASE_BUNDLE`;
- macro security must be handled through Trusted Location and, for broad use, code signing.
