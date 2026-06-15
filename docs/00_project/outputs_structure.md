# РЎС‚СЂСѓРєС‚СѓСЂР° outputs

Р”РѕРєСѓРјРµРЅС‚ С„РёРєСЃРёСЂСѓРµС‚ С†РµР»РµРІСѓСЋ СЃС‚СЂСѓРєС‚СѓСЂСѓ `outputs/` Рё РїСЂРѕРІРµСЂРєРё, РєРѕС‚РѕСЂС‹Рµ РґРѕР»Р¶РЅС‹ РїРѕРєСЂС‹РІР°С‚СЊСЃСЏ smoke tests РїРѕСЃР»Рµ РЅРѕРІРѕРіРѕ Р·Р°РїСѓСЃРєР° pipeline.

## Р¦РµР»РµРІР°СЏ СЃС‚СЂСѓРєС‚СѓСЂР°

```text
outputs/reports/
outputs/reports/analytical_tables/
outputs/reports/monthly_tables/

outputs/exports/
outputs/exports/analytical_csv/
outputs/exports/chart_data/
outputs/exports/chart_data/risk_quadrant/
outputs/exports/chart_data/sankey/
outputs/exports/chart_data/boxplot/
outputs/exports/chart_data/structure/
outputs/exports/technical/
outputs/exports/technical/review_required/

outputs/dashboards/
outputs/archive/
```

## РќР°Р·РЅР°С‡РµРЅРёРµ РїР°РїРѕРє

| РџР°РїРєР° | РќР°Р·РЅР°С‡РµРЅРёРµ |
| --- | --- |
| `outputs/reports/` | Р§РµР»РѕРІРµРєРѕС‡РёС‚Р°РµРјС‹Рµ РѕС‚С‡РµС‚РЅС‹Рµ С‚Р°Р±Р»РёС†С‹ Рё РѕС‚С‡РµС‚РЅС‹Рµ С„Р°Р№Р»С‹. |
| `outputs/reports/analytical_tables/` | XLSX РѕР±СЏР·Р°С‚РµР»СЊРЅС‹С… Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёС… С‚Р°Р±Р»РёС†. |
| `outputs/reports/monthly_tables/` | XLSX РїРѕРјРµСЃСЏС‡РЅС‹С… РѕС‚С‡РµС‚РЅС‹С… С‚Р°Р±Р»РёС† Рё monthly layer reports. |
| `outputs/exports/analytical_csv/` | CSV-РєРѕРїРёРё РѕС‚С‡РµС‚РЅС‹С… С‚Р°Р±Р»РёС†. |
| `outputs/exports/chart_data/` | РўРµС…РЅРёС‡РµСЃРєРёРµ С‚Р°Р±Р»РёС†С‹-РѕСЃРЅРѕРІС‹ РІРёР·СѓР°Р»РёР·Р°С†РёР№. |
| `outputs/exports/chart_data/risk_quadrant/` | CSV-РѕСЃРЅРѕРІС‹ risk quadrant, demand cutoff Рё ratio-РіСЂР°С„РёРєРѕРІ. |
| `outputs/exports/chart_data/sankey/` | CSV-РѕСЃРЅРѕРІС‹ Sankey-РіСЂР°С„РёРєРѕРІ. |
| `outputs/exports/chart_data/boxplot/` | CSV-РѕСЃРЅРѕРІС‹ boxplot-РіСЂР°С„РёРєРѕРІ Рё СЃС‚Р°С‚РёСЃС‚РёРєРё СЂР°СЃРїСЂРµРґРµР»РµРЅРёР№. |
| `outputs/exports/chart_data/structure/` | CSV-РѕСЃРЅРѕРІС‹ СЃС‚СЂСѓРєС‚СѓСЂРЅС‹С… РІРёР·СѓР°Р»РёР·Р°С†РёР№. |
| `outputs/exports/technical/` | РўРµС…РЅРёС‡РµСЃРєРёРµ exports, РЅРµ РѕС‚РЅРѕСЃСЏС‰РёРµСЃСЏ Рє РѕС‚С‡РµС‚РЅС‹Рј С‚Р°Р±Р»РёС†Р°Рј РёР»Рё chart data. |
| `outputs/exports/technical/review_required/` | Р¤Р°Р№Р»С‹, РЅР°Р·РЅР°С‡РµРЅРёРµ РєРѕС‚РѕСЂС‹С… С‚СЂРµР±СѓРµС‚ СЂСѓС‡РЅРѕР№ РїСЂРѕРІРµСЂРєРё. |
| `outputs/dashboards/` | BI-ready dashboard exports. |
| `outputs/archive/` | РЈСЃС‚Р°СЂРµРІС€РёРµ РёР»Рё РїРµСЂРµРЅРµСЃРµРЅРЅС‹Рµ outputs, РєРѕС‚РѕСЂС‹Рµ РЅРµ СѓРґР°Р»СЏСЋС‚СЃСЏ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё. |

## Smoke checks

Smoke tests, РµСЃР»Рё РѕРЅРё Р±СѓРґСѓС‚ РґРѕР±Р°РІР»РµРЅС‹ РІ РїСЂРѕРµРєС‚, РґРѕР»Р¶РЅС‹ РїСЂРѕРІРµСЂСЏС‚СЊ РЅР°Р»РёС‡РёРµ:

- `outputs/reports/analytical_tables/`
- `outputs/reports/monthly_tables/`
- `outputs/exports/analytical_csv/`
- `outputs/exports/chart_data/risk_quadrant/`
- `outputs/exports/chart_data/sankey/`
- `outputs/exports/chart_data/boxplot/`
- `outputs/exports/chart_data/structure/`
- `outputs/dashboards/`

РџРѕСЃР»Рµ РЅРѕРІРѕРіРѕ Р·Р°РїСѓСЃРєР° pipeline smoke tests С‚Р°РєР¶Рµ РґРѕР»Р¶РЅС‹ РїСЂРѕРІРµСЂСЏС‚СЊ, С‡С‚Рѕ РѕС‚С‡РµС‚РЅС‹Рµ `.xlsx` РЅРµ СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РЅР°РїСЂСЏРјСѓСЋ РІ РєРѕСЂРµРЅСЊ `outputs/exports/`.

## РџСЂР°РІРёР»Рѕ С…СЂР°РЅРµРЅРёСЏ

РќРѕРІС‹Рµ РіРµРЅРµСЂР°С†РёРё РґРѕР»Р¶РЅС‹ СЃРѕС…СЂР°РЅСЏС‚СЊ С„Р°Р№Р»С‹ СЃСЂР°Р·Сѓ РІ РїСЂРѕС„РёР»СЊРЅСѓСЋ РїР°РїРєСѓ. РЎС‚Р°СЂС‹Рµ РёР»Рё РЅРµРѕРґРЅРѕР·РЅР°С‡РЅС‹Рµ outputs РЅРµ СѓРґР°Р»СЏСЋС‚СЃСЏ Р±РµР·РІРѕР·РІСЂР°С‚РЅРѕ Рё РїСЂРё РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё РїРµСЂРµРЅРѕСЃСЏС‚СЃСЏ РІ `outputs/archive/` РёР»Рё `outputs/exports/technical/review_required/`.

## РђРєС‚СѓР°Р»РёР·Р°С†РёСЏ СЃС‚СЂСѓРєС‚СѓСЂС‹ РЅР° 2026-05-25

| РўРёРї СЂРµР·СѓР»СЊС‚Р°С‚Р° | Р¦РµР»РµРІР°СЏ РїР°РїРєР° | РљРѕРјРјРµРЅС‚Р°СЂРёР№ |
| --- | --- | --- |
| РћР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ XLSX-С‚Р°Р±Р»РёС†С‹ | `outputs/reports/analytical_tables/` | Р§РµР»РѕРІРµРєРѕС‡РёС‚Р°РµРјС‹Рµ Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёРµ С‚Р°Р±Р»РёС†С‹. |
| РџРѕРјРµСЃСЏС‡РЅС‹Рµ XLSX-С‚Р°Р±Р»РёС†С‹ | `outputs/reports/monthly_tables/` | Monthly layer Рё monthly reports. |
| CSV-РєРѕРїРёРё РѕС‚С‡РµС‚РЅС‹С… С‚Р°Р±Р»РёС† | `outputs/exports/analytical_csv/` | РњР°С€РёРЅРѕС‡РёС‚Р°РµРјС‹Рµ РІРµСЂСЃРёРё РѕС‚С‡РµС‚РЅС‹С… С‚Р°Р±Р»РёС†. |
| HTML-РіСЂР°С„РёРєРё | `outputs/charts/` | РРЅС‚РµСЂР°РєС‚РёРІРЅС‹Рµ РІРёР·СѓР°Р»РёР·Р°С†РёРё. |
| Risk/scatter chart data | `outputs/exports/chart_data/risk_quadrant/` | РћСЃРЅРѕРІС‹ risk quadrant, demand cutoff, scatter/outlier/log/facet РІРµСЂСЃРёР№. |
| Sankey chart data | `outputs/exports/chart_data/sankey/` | РџРѕС‚РѕРєРё Sankey Рё С‚Р°Р±Р»РёС†С‹-РѕСЃРЅРѕРІС‹. |
| Boxplot chart data | `outputs/exports/chart_data/boxplot/` | РЎС‚Р°С‚РёСЃС‚РёРєРё boxplot, РІРєР»СЋС‡Р°СЏ long-mode/facet diagnostics. |
| Structure chart data | `outputs/exports/chart_data/structure/` | Stacked structure charts, РёС‚РѕРіРё СЃС‚РѕР»Р±С†РѕРІ Рё РґРѕР»Рё СЃРµРіРјРµРЅС‚РѕРІ. |
| Dashboard exports | `outputs/dashboards/` | BI-ready datasets, metadata, data dictionary, semantic layer. |
| Executive summary | `outputs/reports/` | РџР°СЂР°РјРµС‚СЂРёР·СѓРµРјРѕРµ СѓРїСЂР°РІР»РµРЅС‡РµСЃРєРѕРµ СЂРµР·СЋРјРµ. |

Новые файлы не должны сохраняться напрямую в корень `outputs/exports/`. Production cleanup выполняется через `ofz-clean-outputs` / `scripts/maintenance/cleanup_outputs.py`; legacy migration helpers хранятся в `scripts/archive/2026-06-15/` только для audit trail.

## РџСЂРѕРІРµСЂРєРё СЃС‚СЂСѓРєС‚СѓСЂС‹

Р РµРєРѕРјРµРЅРґСѓРµРјС‹Рµ РєРѕРјР°РЅРґС‹ СЂСѓС‡РЅРѕР№ РїСЂРѕРІРµСЂРєРё:

```powershell
.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

```powershell
.\.venv\Scripts\python.exe scripts\smoke_tests.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```
