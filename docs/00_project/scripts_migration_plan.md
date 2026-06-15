# Scripts Migration Plan

Р”РѕРєСѓРјРµРЅС‚ РѕРїРёСЃС‹РІР°РµС‚ РІРѕР·РјРѕР¶РЅСѓСЋ Р±СѓРґСѓС‰СѓСЋ С„РёР·РёС‡РµСЃРєСѓСЋ СЂРµРѕСЂРіР°РЅРёР·Р°С†РёСЋ `scripts/`. РќР° С‚РµРєСѓС‰РµРј СЌС‚Р°РїРµ РїРµСЂРµРЅРѕСЃ РѕСЃРЅРѕРІРЅС‹С… Python-СЃРєСЂРёРїС‚РѕРІ РЅРµ РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ. РџСЂРѕРµРєС‚ СЃРѕС…СЂР°РЅСЏРµС‚ РґРµР№СЃС‚РІСѓСЋС‰РёРµ РєРѕРјР°РЅРґС‹ Р·Р°РїСѓСЃРєР° РёР· РєРѕСЂРЅСЏ С‡РµСЂРµР· `.\.venv\Scripts\python.exe`.

## Р¦РµР»РµРІР°СЏ СЃС‚СЂСѓРєС‚СѓСЂР°

```text
scripts/
  pipeline/
  stages/
  qa/
  metadata/
  utils/
  maintenance/
```

## РџСЂРµРґР»Р°РіР°РµРјРѕРµ СЂР°СЃРїСЂРµРґРµР»РµРЅРёРµ

### `scripts/pipeline/`

- `run_pipeline.py`
- `interactive_pipeline.py`
- `report_params.py`
- `period_filter.py`

### `scripts/stages/`

- `01_data_audit.py`
- `02_data_cleaning.py`
- `03_feature_engineering.py`
- `04_kpi_map.py`
- `05_visualization_strategy.py`
- `06_build_charts.py`
- `07_dashboard_exports.py`
- `08_analytical_tables.py`
- `09_monthly_analytics.py`
- `10_build_monthly_charts.py`
- `11_revenue_analytics.py`
- `12_build_revenue_charts.py`
- `generate_executive_summary.py`
- `build_semantic_model_v2.py`

### `scripts/qa/`

- `quality_gate.py`
- `schema_validation.py`
- `regression_tests.py`
- `smoke_tests.py`
- `html_chart_qa.py`
- `visual_regression.py`
- `anomaly_tests.py`

### `scripts/metadata/`

- `run_manifest.py`
- `raw_data_registry.py`

### `scripts/utils/`

- `config.py`
- `utils.py`
- `palette.py`
- `scatter_chart_policy.py`
- `compare_outputs.py`

### `scripts/maintenance/`

- `archive/2026-06-15/cleanup_docs.py`
- `archive/2026-06-15/reorganize_outputs.py`
- `archive/2026-06-15/migrate_outputs_structure.py`
- `archive/2026-06-15/reorganize_docs.py`
- `maintenance/reorganize_charts.py`
- `archive/2026-06-15/migrate_legacy_docs_archive.py`

## РЈСЃР»РѕРІРёСЏ Р±СѓРґСѓС‰РµРіРѕ РїРµСЂРµРЅРѕСЃР°

Р¤РёР·РёС‡РµСЃРєРёР№ РїРµСЂРµРЅРѕСЃ РґРѕРїСѓСЃС‚РёРј С‚РѕР»СЊРєРѕ РѕС‚РґРµР»СЊРЅС‹Рј СЌС‚Р°РїРѕРј СЃ dry-run Рё РїСЂРѕРІРµСЂРєРѕР№ РѕР±СЂР°С‚РЅРѕР№ СЃРѕРІРјРµСЃС‚РёРјРѕСЃС‚Рё. РќРµР»СЊР·СЏ РѕРґРЅРѕРІСЂРµРјРµРЅРЅРѕ РїРµСЂРµРЅРѕСЃРёС‚СЊ СЃРєСЂРёРїС‚С‹ Рё РјРµРЅСЏС‚СЊ РјРµС‚РѕРґРѕР»РѕРіРёСЋ СЂР°СЃС‡РµС‚РѕРІ.

РњРёРЅРёРјР°Р»СЊРЅС‹Рµ СѓСЃР»РѕРІРёСЏ:

- СЃРѕС…СЂР°РЅРёС‚СЊ СЃСѓС‰РµСЃС‚РІСѓСЋС‰РёРµ CLI-РєРѕРјР°РЅРґС‹;
- РѕР±РЅРѕРІРёС‚СЊ РёРјРїРѕСЂС‚С‹ Р±РµР· РёР·РјРµРЅРµРЅРёСЏ РїРѕРІРµРґРµРЅРёСЏ;
- РґРѕР±Р°РІРёС‚СЊ wrapper-С„Р°Р№Р»С‹ РЅР° СЃС‚Р°СЂС‹С… РїСѓС‚СЏС…;
- РїСЂРѕРІРµСЂРёС‚СЊ `py_compile`;
- РїСЂРѕРІРµСЂРёС‚СЊ `run_pipeline.py --all`;
- РїСЂРѕРІРµСЂРёС‚СЊ `quality_gate.py`;
- РѕР±РЅРѕРІРёС‚СЊ README Рё `scripts/README.md`;
- РЅРµ РёР·РјРµРЅСЏС‚СЊ `data/raw/`.

## Wrapper Compatibility

РџРѕСЃР»Рµ РїРµСЂРµРЅРѕСЃР° СЃС‚Р°СЂС‹Рµ РїСѓС‚Рё РґРѕР»Р¶РЅС‹ РѕСЃС‚Р°РІР°С‚СЊСЃСЏ СЂР°Р±РѕС‡РёРјРё С‡РµСЂРµР· С‚РѕРЅРєРёРµ wrappers. РџСЂРёРјРµСЂ wrapper РґР»СЏ `scripts/run_pipeline.py`:

```python
from scripts.pipeline.run_pipeline import main

if __name__ == "__main__":
    main()
```

Wrapper РЅРµ РґРѕР»Р¶РµРЅ СЃРѕРґРµСЂР¶Р°С‚СЊ Р±РёР·РЅРµСЃ-Р»РѕРіРёРєСѓ. Р•РіРѕ Р·Р°РґР°С‡Р° вЂ” СЃРѕС…СЂР°РЅРёС‚СЊ СЃС‚Р°СЂСѓСЋ С‚РѕС‡РєСѓ РІС…РѕРґР° РґР»СЏ РїРѕР»СЊР·РѕРІР°С‚РµР»РµР№, РґРѕРєСѓРјРµРЅС‚Р°С†РёРё Рё Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРёС… РїСЂРѕРІРµСЂРѕРє.

## Р РµРєРѕРјРµРЅРґСѓРµРјС‹Р№ РїРѕСЂСЏРґРѕРє РјРёРіСЂР°С†РёРё

1. РЎРѕР·РґР°С‚СЊ С†РµР»РµРІС‹Рµ РїРѕРґРїР°РїРєРё Рё `__init__.py`.
2. РџРµСЂРµРЅРµСЃС‚Рё РѕРґРёРЅ РЅРµР±РѕР»СЊС€РѕР№ QA-СЃРєСЂРёРїС‚ РІ С‚РµСЃС‚РѕРІРѕРј СЂРµР¶РёРјРµ.
3. Р”РѕР±Р°РІРёС‚СЊ wrapper РЅР° СЃС‚Р°СЂРѕРј РїСѓС‚Рё.
4. РџСЂРѕРІРµСЂРёС‚СЊ РїСЂСЏРјРѕР№ Р·Р°РїСѓСЃРє СЃС‚Р°СЂРѕРіРѕ РїСѓС‚Рё Рё РЅРѕРІРѕРіРѕ РїСѓС‚Рё.
5. РџРѕРІС‚РѕСЂРёС‚СЊ РґР»СЏ РѕСЃС‚Р°Р»СЊРЅС‹С… РіСЂСѓРїРї.
6. РћР±РЅРѕРІРёС‚СЊ `run_pipeline.py`, README, `scripts/README.md` Рё quality checks.
7. РЈРґР°Р»СЏС‚СЊ wrappers С‚РѕР»СЊРєРѕ РїРѕСЃР»Рµ РѕС‚РґРµР»СЊРЅРѕРіРѕ СЂРµС€РµРЅРёСЏ Рё Р·Р°РІРµСЂС€РµРЅРЅРѕРіРѕ РїРµСЂРёРѕРґР° РѕР±СЂР°С‚РЅРѕР№ СЃРѕРІРјРµСЃС‚РёРјРѕСЃС‚Рё.

