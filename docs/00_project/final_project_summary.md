# Р¤РёРЅР°Р»СЊРЅС‹Р№ РѕР±Р·РѕСЂ РїСЂРѕРµРєС‚Р°

Р”Р°С‚Р° С„РѕСЂРјРёСЂРѕРІР°РЅРёСЏ: `2026-05-19`.

РџРµСЂРІР°СЏ РјРѕРґРµСЂРЅРёР·Р°С†РёСЏ РїСЂРѕРµРєС‚Р° Р·Р°РІРµСЂС€РµРЅР° РїРѕР»РЅРѕСЃС‚СЊСЋ. РўРµРєСѓС‰РёРµ РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅС‹Рµ Р°СЂС‚РµС„Р°РєС‚С‹, РїСЂРѕРІРµСЂРєРё РєР°С‡РµСЃС‚РІР°, semantic model v2, revenue analytics Рё СЃРІСЏР·Р°РЅРЅС‹Рµ РІРёР·СѓР°Р»РёР·Р°С†РёРё РѕС‚РЅРѕСЃСЏС‚СЃСЏ РєРѕ РІС‚РѕСЂРѕР№ РјРѕРґРµСЂРЅРёР·Р°С†РёРё Рё РІС‹РїРѕР»РЅСЏСЋС‚СЃСЏ РїРѕРІРµСЂС… СѓР¶Рµ СЃС‚Р°Р±РёР»РёР·РёСЂРѕРІР°РЅРЅРѕР№ Р±Р°Р·С‹ Р±РµР· РїРѕРІС‚РѕСЂРЅРѕРіРѕ РІРЅРµРґСЂРµРЅРёСЏ РїРµСЂРёРѕРґРЅРѕР№ Р°РіСЂРµРіР°С†РёРё, `period_filter` Рё СЃС‚СЂСѓРєС‚СѓСЂС‹ `outputs`.

РџСЂРѕРµРєС‚ СЂРµР°Р»РёР·СѓРµС‚ РІРѕСЃРїСЂРѕРёР·РІРѕРґРёРјС‹Р№ Python-first pipeline Р°РЅР°Р»РёС‚РёРєРё СЂР°Р·РјРµС‰РµРЅРёР№ РћР¤Р—: РѕС‚ Р°СѓРґРёС‚Р° РёСЃС…РѕРґРЅС‹С… С„Р°Р№Р»РѕРІ Рё РѕС‡РёСЃС‚РєРё РґР°РЅРЅС‹С… РґРѕ РїР°СЂР°РјРµС‚СЂРёР·СѓРµРјРѕРіРѕ report scope, KPI, РѕР±СЏР·Р°С‚РµР»СЊРЅС‹С… С‚Р°Р±Р»РёС‡РЅС‹С… РѕС‚С‡РµС‚РѕРІ, РёРЅС‚РµСЂР°РєС‚РёРІРЅС‹С… РіСЂР°С„РёРєРѕРІ, dashboard-ready exports Рё executive summary.

## Workflow РїСЂРѕРµРєС‚Р°

| Р­С‚Р°Рї | РќР°Р·РЅР°С‡РµРЅРёРµ | РћСЃРЅРѕРІРЅС‹Рµ Р°СЂС‚РµС„Р°РєС‚С‹ |
| --- | --- | --- |
| Р­С‚Р°Рї 1 | РђСѓРґРёС‚ РёСЃС…РѕРґРЅС‹С… РґР°РЅРЅС‹С… | `scripts/01_data_audit.py`, `docs/data_audit.md` |
| Р­С‚Р°Рї 2 | РћС‡РёСЃС‚РєР° РґР°РЅРЅС‹С… | `scripts/02_data_cleaning.py`, `data/processed/ofz_auctions_clean.csv`, `docs/data_cleaning_report.md` |
| Р­С‚Р°Рї 3 | Feature engineering | `scripts/03_feature_engineering.py`, `data/processed/ofz_auctions_features.csv`, `docs/feature_engineering.md` |
| Р­С‚Р°Рї 4 | РџР°СЂР°РјРµС‚СЂРёР·СѓРµРјС‹Р№ report scope | `scripts/period_filter.py`, `data/processed/ofz_auctions_report_scope.csv`, `docs/period_selection_report.md` |
| Р­С‚Р°Рї 5 | KPI map | `scripts/04_kpi_map.py`, `docs/kpi_map.md` |
| Р­С‚Р°Рї 6 | Analytical architecture | `docs/analytical_architecture.md` |
| Р­С‚Р°Рї 7 | Visualization strategy | `scripts/05_visualization_strategy.py`, `docs/visualization_strategy.md` |
| Р­С‚Р°Рї 8 | Chart implementation | `scripts/06_build_charts.py`, `outputs/charts/`, `outputs/exports/chart_data/`, `docs/chart_build_limitations.md` |
| Р­С‚Р°Рї 8.1 | РћР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёРµ С‚Р°Р±Р»РёС†С‹ | `scripts/08_analytical_tables.py`, XLSX РІ `outputs/reports/analytical_tables/` РёР»Рё `outputs/reports/monthly_tables/`, CSV РІ `outputs/exports/analytical_csv/` |
| Р­С‚Р°Рї 9 | Dashboard architecture | `docs/dashboard_architecture.md` |
| Р­С‚Р°Рї 9.1 | Dashboard exports | `scripts/07_dashboard_exports.py`, `outputs/dashboards/`, `docs/dashboard_exports_report.md` |
| Р­С‚Р°Рї 10 | Executive summary | `docs/executive_summary.md` |
| Р­С‚Р°Рї 11 | Self-review | `docs/self_review.md` |
| Р­С‚Р°Рї 12 | Final project summary | `docs/final_project_summary.md` |

РђРЅР°Р»РёС‚РёС‡РµСЃРєРёРµ С‚Р°Р±Р»РёС†С‹ `ofz_yield_by_type` Рё `placement_volume_by_maturity` СѓРїРѕСЂСЏРґРѕС‡РµРЅС‹ РїРѕ РѕС‚С‡РµС‚РЅРѕРјСѓ РїРµСЂРёРѕРґСѓ РєР°Рє РѕСЃРЅРѕРІРЅРѕР№ РѕСЃРё СЃСЂР°РІРЅРµРЅРёСЏ: РІРЅСѓС‚СЂРё РїРµСЂРёРѕРґР° СЃС‚СЂРѕРєРё СЃРѕСЂС‚РёСЂСѓСЋС‚СЃСЏ СЃРѕРѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕ РїРѕ РІРёРґСѓ РћР¤Р— Рё РјРµС‚РѕРґРѕР»РѕРіРёС‡РµСЃРєРѕРјСѓ РїРѕСЂСЏРґРєСѓ СЃСЂРѕРєРѕРІС‹С… РєР°С‚РµРіРѕСЂРёР№.

Р“СЂР°С„РёРєРё РѕР±СЉРµРјР° СЂР°Р·РјРµС‰РµРЅРёСЏ РїСЂРёРІРµРґРµРЅС‹ Рє РµРґРёРЅРѕРјСѓ РґРѕРєР»Р°РґРЅРѕРјСѓ СЃС‚Р°РЅРґР°СЂС‚Сѓ: РїРѕРєР°Р·Р°С‚РµР»СЊ С‚СЂР°РєС‚СѓРµС‚СЃСЏ РєР°Рє РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РћР¤Р— РїРѕ РЅРѕРјРёРЅР°Р»Сѓ, РЅР° РІРёР·СѓР°Р»РёР·Р°С†РёСЏС… РѕС‚РѕР±СЂР°Р¶Р°РµС‚СЃСЏ РІ РјР»СЂРґ СЂСѓР±Р»РµР№, Р° РёСЃС…РѕРґРЅС‹Рµ Р·РЅР°С‡РµРЅРёСЏ РІ РјР»РЅ СЂСѓР±Р»РµР№ СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РІ С‚Р°Р±Р»РёС†Р°С…-РѕСЃРЅРѕРІР°С… РіСЂР°С„РёРєРѕРІ.

## РЎРѕР·РґР°РЅРЅС‹Рµ scripts

- `scripts/01_data_audit.py`
- `scripts/02_data_cleaning.py`
- `scripts/03_feature_engineering.py`
- `scripts/04_kpi_map.py`
- `scripts/05_visualization_strategy.py`
- `scripts/06_build_charts.py`
- `scripts/07_dashboard_exports.py`
- `scripts/08_analytical_tables.py`
- `scripts/archive/2026-06-15/cleanup_docs.py`
- `scripts/compare_outputs.py`
- `scripts/config.py`
- `scripts/interactive_pipeline.py`
- `scripts/period_filter.py`
- `scripts/report_params.py`
- `scripts/run_pipeline.py`
- `scripts/utils.py`
- `scripts/__init__.py`

## РЎРѕР·РґР°РЅРЅС‹Рµ docs

РђРєС‚РёРІРЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ РІ РєРѕСЂРЅРµ `docs/`:

- `docs/analytical_architecture.md`
- `docs/analytical_tables_limitations.md`
- `docs/analytical_tables_report.md`
- `docs/chart_build_limitations.md`
- `docs/dashboard_architecture.md`
- `docs/dashboard_exports_limitations.md`
- `docs/dashboard_exports_report.md`
- `docs/data_audit.md`
- `docs/data_cleaning_report.md`
- `docs/docs_cleanup_report.md`
- `docs/executive_summary.md`
- `docs/feature_engineering.md`
- `docs/final_project_summary.md`
- `docs/kpi_map.md`
- `docs/period_selection_report.md`
- `docs/project_inventory.md`
- `docs/self_review.md`
- `docs/visualization_strategy.md`

РџСЂРѕРјРµР¶СѓС‚РѕС‡РЅС‹Рµ repro/status/sync/validation-РґРѕРєСѓРјРµРЅС‚С‹ РїРµСЂРµРЅРµСЃРµРЅС‹ РІ `docs/archive/` Рё РЅРµ СѓРґР°Р»СЏР»РёСЃСЊ Р±РµР·РІРѕР·РІСЂР°С‚РЅРѕ.

## Datasets

РСЃС…РѕРґРЅС‹Рµ С„Р°Р№Р»С‹ РІ `data/raw/`:

- `INTERNET_Auction_Results_rus_2019_20191218.xlsx`
- `INTERNET_Auction_Results_rus_2020_20201223.xlsx`
- `INTERNET_Auction_Results_rus_2021_20211223.xlsx`
- `INTERNET_Auction_Results_rus_2022_20221222.xlsx`
- `INTERNET_Auction_Results_rus_2023_20231231.xlsx`
- `INTERNET_Auction_Results_rus_2024_20241231.xlsx`
- `INTERNET_Auction_Results_rus_2025_20251231.xlsx`
- `INTERNET_Auction_Results_rus_2026_20260507.xlsx`

Р Р°Р±РѕС‡РёРµ datasets РІ `data/processed/`:

- `ofz_auctions_clean.csv`
- `ofz_auctions_clean_repro.csv`
- `ofz_auctions_features.csv`
- `ofz_auctions_features_repro.csv`
- `ofz_auctions_report_scope.csv`

## Charts

РЎРѕР·РґР°РЅРЅС‹Рµ HTML-РіСЂР°С„РёРєРё РІ `outputs/charts/`:

- `placement_volume_quarter_2026-04-01_retrospective_2.html`
- `demand_supply_quarter_2026-04-01_retrospective_2.html`
- `bid_to_cover_quarter_2026-04-01_retrospective_2.html`
- `yield_by_type_quarter_2026-04-01_retrospective_2.html`
- `maturity_structure_quarter_2026-04-01_retrospective_2.html`
- `format_structure_quarter_2026-04-01_retrospective_2.html`
- `risk_quadrant_quarter_2026-04-01_retrospective_2.html`
- `risk_quadrant_retrospective_quarter_2026-04-01_retrospective_2.html`
- `risk_quadrant_demand_to_placement_by_quarter_quarter_2026-04-01_retrospective_2.html`
- `yield_boxplot_by_ofz_type_quarter_2026-04-01_retrospective_2.html`
- `demand_cutoff_explanation_quarter_2026-04-01_retrospective_2.html`
- `sankey_structure_quarter_2026-04-01_retrospective_2.html`
- `sankey_period_maturity_type_format_quarter_2026-04-01_retrospective_2.html`
- `sankey_period_format_type_maturity_quarter_2026-04-01_retrospective_2.html`
- `sankey_period_format_maturity_type_quarter_2026-04-01_retrospective_2.html`
- `sankey_target_period_quarter_2026-04-01_retrospective_2.html`

## Exports

РЎРѕР·РґР°РЅРЅС‹Рµ Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёРµ CSV Рё chart-support exports:

- `bid_to_cover_quarter_2026-04-01_retrospective_2.csv`
- `demand_cutoff_explanation_quarter_2026-04-01_retrospective_2.csv`
- `demand_supply_quarter_2026-04-01_retrospective_2.csv`
- `demand_supply_quarter_2026-04-01_retrospective_2.xlsx`
- `format_structure_quarter_2026-04-01_retrospective_2.csv`
- `maturity_structure_quarter_2026-04-01_retrospective_2.csv`
- `ofz_yield_by_type_quarter_2026-04-01_retrospective_2.csv`
- `ofz_yield_by_type_quarter_2026-04-01_retrospective_2.xlsx`
- `placement_volume_by_maturity_quarter_2026-04-01_retrospective_2.csv`
- `placement_volume_by_maturity_quarter_2026-04-01_retrospective_2.xlsx`
- `placement_volume_quarter_2026-04-01_retrospective_2.csv`
- `risk_quadrant_demand_to_placement_by_quarter_quarter_2026-04-01_retrospective_2.csv`
- `risk_quadrant_quarter_2026-04-01_retrospective_2.csv`
- `risk_quadrant_retrospective_quarter_2026-04-01_retrospective_2.csv`
- `sankey_structure_flow_quarter_2026-04-01_retrospective_2.csv`
- `sankey_structure_quarter_2026-04-01_retrospective_2.csv`
- `sankey_period_maturity_type_format_quarter_2026-04-01_retrospective_2.csv`
- `sankey_period_format_type_maturity_quarter_2026-04-01_retrospective_2.csv`
- `sankey_period_format_maturity_type_quarter_2026-04-01_retrospective_2.csv`
- `sankey_target_period_structure_quarter_2026-04-01_retrospective_2.csv`
- `yield_boxplot_by_ofz_type_quarter_2026-04-01_retrospective_2.csv`
- `yield_by_type_quarter_2026-04-01_retrospective_2.csv`

РћР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ С‚Р°Р±Р»РёС‡РЅС‹Рµ РѕС‚С‡РµС‚С‹:

- `ofz_yield_by_type_<period_type>_<report_date>_retrospective_<N>.csv/.xlsx`
- `demand_supply_<period_type>_<report_date>_retrospective_<N>.csv/.xlsx`
- `placement_volume_by_maturity_<period_type>_<report_date>_retrospective_<N>.csv/.xlsx`

## Dashboard exports

РЎРѕР·РґР°РЅРЅС‹Рµ dashboard-ready files РІ `outputs/dashboards/`:

- `dashboard_auction_level_quarter_2026-04-01_retrospective_2.csv`
- `dashboard_period_summary_quarter_2026-04-01_retrospective_2.csv`
- `dashboard_kpi_summary_quarter_2026-04-01_retrospective_2.csv`
- `dashboard_maturity_structure_quarter_2026-04-01_retrospective_2.csv`
- `dashboard_yield_distribution_quarter_2026-04-01_retrospective_2.csv`
- `dashboard_demand_supply_quarter_2026-04-01_retrospective_2.csv`
- `dashboard_metadata_quarter_2026-04-01_retrospective_2.json`
- `dashboard_data_dictionary_quarter_2026-04-01_retrospective_2.csv`

Р­С‚Рё С„Р°Р№Р»С‹ РїСЂРµРґРЅР°Р·РЅР°С‡РµРЅС‹ РґР»СЏ BI/dashboard-СЃР»РѕСЏ: detail fact table, РїРµСЂРёРѕРґРЅС‹Рµ KPI, KPI cards, maturity structure, yield distribution, demand/supply views, metadata Рё data dictionary.

## РљРѕРјР°РЅРґС‹ Р·Р°РїСѓСЃРєР°

Р’СЃРµ РєРѕРјР°РЅРґС‹ РІС‹РїРѕР»РЅСЏСЋС‚СЃСЏ РёР· РєРѕСЂРЅСЏ РїСЂРѕРµРєС‚Р° Р»РѕРєР°Р»СЊРЅС‹Рј Python РёР· `.venv`:

```powershell
.\.venv\Scripts\python.exe --version
```

РњРµСЃСЏС‡РЅС‹Р№ РѕС‚С‡РµС‚:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

РљРІР°СЂС‚Р°Р»СЊРЅС‹Р№ РѕС‚С‡РµС‚:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-07-01 --retrospective-years 4 --period-type quarter --aggregation-mode cumulative
```

Р“РѕРґРѕРІРѕР№ РѕС‚С‡РµС‚:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-01-01 --retrospective-years 5 --period-type year --aggregation-mode cumulative
```

Р—Р°РїСѓСЃРє С‚РѕР»СЊРєРѕ Р­С‚Р°РїРѕРІ 1-3:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --stages 1 2 3 --safe
```

Р—Р°РїСѓСЃРє dashboard exports РѕС‚РґРµР»СЊРЅРѕ:

```powershell
.\.venv\Scripts\python.exe scripts\07_dashboard_exports.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## РљР»СЋС‡РµРІС‹Рµ РјРµС‚РѕРґРѕР»РѕРіРёС‡РµСЃРєРёРµ РїСЂР°РІРёР»Р°

- `report-date` РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ РїРµСЂРІС‹Рј РґРЅРµРј РјРµСЃСЏС†Р°.
- Р”Р»СЏ `period-type=quarter` РґРѕРїСѓСЃС‚РёРјС‹ С‚РѕР»СЊРєРѕ 1 СЏРЅРІР°СЂСЏ, 1 Р°РїСЂРµР»СЏ, 1 РёСЋР»СЏ, 1 РѕРєС‚СЏР±СЂСЏ.
- Р”Р»СЏ `period-type=year` РґРѕРїСѓСЃС‚РёРјРѕ С‚РѕР»СЊРєРѕ 1 СЏРЅРІР°СЂСЏ.
- РљРѕР»РёС‡РµСЃС‚РІРѕ РїРµСЂРёРѕРґРѕРІ СЃСЂР°РІРЅРµРЅРёСЏ СЂР°РІРЅРѕ `retrospective-years + 1`.
- `data/raw/` РЅРµ РёР·РјРµРЅСЏРµС‚СЃСЏ pipeline.
- `format` СЃРѕС…СЂР°РЅСЏРµС‚СЃСЏ РєР°Рє РѕС‚РґРµР»СЊРЅС‹Р№ РїСЂРёР·РЅР°Рє Рё РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ РІ РѕС‚С‡РµС‚Р°С…, РіСЂР°С„РёРєР°С… Рё dashboard exports.
- РЎСЂРѕРєРё РєР»Р°СЃСЃРёС„РёС†РёСЂСѓСЋС‚СЃСЏ С‚Р°Рє: РєСЂР°С‚РєРѕСЃСЂРѕС‡РЅС‹Рµ - РґРѕ 5 Р»РµС‚ РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ; СЃСЂРµРґРЅРµСЃСЂРѕС‡РЅС‹Рµ - СЃРІС‹С€Рµ 5 Рё РґРѕ 10 Р»РµС‚ РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ; РґРѕР»РіРѕСЃСЂРѕС‡РЅС‹Рµ - Р±РѕР»РµРµ 10 Р»РµС‚.
- `bid_to_cover_ratio = demand_volume / supply_volume`.
- `demand_to_placement_ratio = demand_volume / placement_volume`.
- `demand_satisfaction_ratio = placement_volume / demand_volume`.
- `demand_to_placement_ratio` РЅРµ РЅР°Р·С‹РІР°РµС‚СЃСЏ bid-to-cover.

## РР·РІРµСЃС‚РЅС‹Рµ РѕРіСЂР°РЅРёС‡РµРЅРёСЏ

- Runtime-РїСЂРѕРІРµСЂРєРё РґРѕР»Р¶РЅС‹ РІС‹РїРѕР»РЅСЏС‚СЊСЃСЏ РІСЂСѓС‡РЅСѓСЋ РїСЂРѕРµРєС‚РЅС‹Рј Python, РµСЃР»Рё sandbox РЅРµ Р·Р°РїСѓСЃРєР°РµС‚ `.venv`.
- Р”Р РџРђ РЅРµ РґРѕР»Р¶РЅС‹ РјРµС…Р°РЅРёС‡РµСЃРєРё РІРєР»СЋС‡Р°С‚СЊСЃСЏ РІ demand-based ratios Р±РµР· РїСЂРѕРІРµСЂРєРё РІР°Р»РёРґРЅРѕСЃС‚Рё СЃРїСЂРѕСЃР°.
- РќРµСЃРѕСЃС‚РѕСЏРІС€РёРµСЃСЏ Р°СѓРєС†РёРѕРЅС‹ Рё СЃС‚СЂРѕРєРё СЃ `placement_volume = 0` РёСЃРєР»СЋС‡Р°СЋС‚СЃСЏ РёР· ratio-РіСЂР°С„РёРєРѕРІ, РіРґРµ СЂР°Р·РјРµС‰РµРЅРёРµ СЃС‚РѕРёС‚ РІ Р·РЅР°РјРµРЅР°С‚РµР»Рµ.
- Р”Р»СЏ Р°РЅР°Р»РёР·Р° РїСЂРёС‡РёРЅ РЅРµСѓРґРѕРІР»РµС‚РІРѕСЂРµРЅРёСЏ СЃРїСЂРѕСЃР° РЅСѓР¶РЅР° `cutoff_price` РёР»Рё `cutoff_yield`; Р±РµР· РЅРёС… РёРЅС‚РµСЂРїСЂРµС‚Р°С†РёСЏ РґРёСЃРєРѕРЅС‚Р° РѕРіСЂР°РЅРёС‡РµРЅР°.
- РќРµРїРѕР»РЅС‹Рµ РїРµСЂРёРѕРґС‹, РІРєР»СЋС‡Р°СЏ С‚РµРєСѓС‰РёР№ РіРѕРґ РёР»Рё РєРІР°СЂС‚Р°Р», С‚СЂРµР±СѓСЋС‚ СЏРІРЅРѕР№ РёРЅС‚РµСЂРїСЂРµС‚Р°С†РёРё РІ РѕС‚С‡РµС‚Р°С….
- XLSX-СЌРєСЃРїРѕСЂС‚ РјРѕР¶РµС‚ Р±С‹С‚СЊ Р·Р°Р±Р»РѕРєРёСЂРѕРІР°РЅ РѕС‚РєСЂС‹С‚С‹Рј С„Р°Р№Р»РѕРј; РґР»СЏ РѕР±СЏР·Р°С‚РµР»СЊРЅС‹С… С‚Р°Р±Р»РёС† РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅ fallback СЃ СѓРЅРёРєР°Р»СЊРЅС‹Рј РёРјРµРЅРµРј.
- Pylance-friendly СЃС‚Р°С‚СѓСЃ С‚СЂРµР±СѓРµС‚ СЂРµРіСѓР»СЏСЂРЅРѕР№ РїСЂРѕРІРµСЂРєРё РІ IDE РїРѕСЃР»Рµ РёР·РјРµРЅРµРЅРёР№.
- РРЅС‚РµСЂР°РєС‚РёРІРЅС‹Рµ HTML-РіСЂР°С„РёРєРё С‚СЂРµР±СѓСЋС‚ Р±СЂР°СѓР·РµСЂРЅРѕР№ РїСЂРѕРІРµСЂРєРё С‡РёС‚Р°РµРјРѕСЃС‚Рё РїРѕРґРїРёСЃРµР№, Р»РµРіРµРЅРґ Рё colorbar.
- РџСЂРѕРјРµР¶СѓС‚РѕС‡РЅС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹ СЃРѕС…СЂР°РЅРµРЅС‹ РІ `docs/archive/`; Р°СЂС…РёРІ РЅРµ СѓРґР°Р»СЏРµС‚СЃСЏ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё.

## Р РµРєРѕРјРµРЅРґСѓРµРјС‹Рµ СЃР»РµРґСѓСЋС‰РёРµ СѓР»СѓС‡С€РµРЅРёСЏ

- Р”РѕР±Р°РІРёС‚СЊ automated smoke tests РґР»СЏ `py_compile`, `--stages 1 2 3`, `period_filter`, charts, analytical tables Рё dashboard exports.
- Р’РІРµСЃС‚Рё schema validation РґР»СЏ `ofz_auctions_clean.csv`, `ofz_auctions_features.csv` Рё `ofz_auctions_report_scope.csv`.
- Р”РѕР±Р°РІРёС‚СЊ РєРѕРЅС‚СЂРѕР»СЊ С…СЌС€РµР№ РёСЃС…РѕРґРЅС‹С… С„Р°Р№Р»РѕРІ `data/raw/` Рё Р¶СѓСЂРЅР°Р» РІРµСЂСЃРёР№ raw-РёСЃС‚РѕС‡РЅРёРєРѕРІ.
- РЎС„РѕСЂРјРёСЂРѕРІР°С‚СЊ regression tests РґР»СЏ СЃРїРѕСЂРЅС‹С… РјРµС‚РѕРґРѕР»РѕРіРёС‡РµСЃРєРёС… РєРµР№СЃРѕРІ: Р”Р РџРђ, РЅСѓР»РµРІРѕРµ СЂР°Р·РјРµС‰РµРЅРёРµ, РЅРµСЃРѕСЃС‚РѕСЏРІС€РёР№СЃСЏ Р°СѓРєС†РёРѕРЅ, РЅРµРїРѕР»РЅС‹Р№ РїРµСЂРёРѕРґ, РІС‹Р±СЂРѕСЃС‹ bid-to-cover.
- Р”РѕР±Р°РІРёС‚СЊ HTML rendering QA РґР»СЏ РєР»СЋС‡РµРІС‹С… РіСЂР°С„РёРєРѕРІ: РїРѕРґРїРёСЃРё, hover, Р»РµРіРµРЅРґС‹, colorbar, С‡РёС‚Р°РµРјРѕСЃС‚СЊ Sankey.
- РЎРѕР·РґР°С‚СЊ BI-ready semantic layer РїРѕРІРµСЂС… dashboard exports: РµРґРёРЅС‹Рµ РјРµСЂС‹, СЂСѓСЃСЃРєРёРµ РЅР°Р·РІР°РЅРёСЏ, С‚РёРїС‹ РґР°РЅРЅС‹С… Рё С„РѕСЂРјР°С‚РёСЂРѕРІР°РЅРёРµ.
- Р”РѕР±Р°РІРёС‚СЊ РєРѕРЅС„РёРіСѓСЂР°С†РёРѕРЅРЅС‹Р№ С„Р°Р№Р» РґР»СЏ palette policy, С‡С‚РѕР±С‹ С†РІРµС‚Р° Р±С‹Р»Рё РµРґРёРЅРѕРѕР±СЂР°Р·РЅС‹ РІРѕ РІСЃРµС… РіСЂР°С„РёРєР°С….
- Р РµР°Р»РёР·РѕРІР°С‚СЊ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєСѓСЋ РіРµРЅРµСЂР°С†РёСЋ executive summary РЅР° РѕСЃРЅРѕРІРµ РЅРѕРІС‹С… dashboard exports Рё РѕР±СЏР·Р°С‚РµР»СЊРЅС‹С… С‚Р°Р±Р»РёС†.
- Р”РѕР±Р°РІРёС‚СЊ РѕС‚РґРµР»СЊРЅС‹Р№ changelog РїСЂРѕРµРєС‚Р° Рё Р¶СѓСЂРЅР°Р» СЂСѓС‡РЅС‹С… РїСЂРѕРІРµСЂРѕРє.

## РЎС‚СЂСѓРєС‚СѓСЂР° РґРѕРєСѓРјРµРЅС‚Р°С†РёРё

РљРѕСЂРµРЅСЊ `docs/` РѕСЃС‚Р°РІР»РµРЅ РґР»СЏ Р°РєС‚СѓР°Р»СЊРЅС‹С… РїСЂРѕРµРєС‚РЅС‹С… РґРѕРєСѓРјРµРЅС‚РѕРІ pipeline. РџСЂРѕРјРµР¶СѓС‚РѕС‡РЅС‹Рµ, repro, sync, status Рё validation-РґРѕРєСѓРјРµРЅС‚С‹ РїРµСЂРµРЅРµСЃРµРЅС‹ РІ `docs/archive/` (6 С„Р°Р№Р»РѕРІ). `docs/archive/` РЅРµ СѓРґР°Р»СЏРµС‚СЃСЏ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё Рё РјРѕР¶РµС‚ Р±С‹С‚СЊ РїСЂРѕРІРµСЂРµРЅ РІСЂСѓС‡РЅСѓСЋ РїРµСЂРµРґ РѕРєРѕРЅС‡Р°С‚РµР»СЊРЅС‹Рј СѓРґР°Р»РµРЅРёРµРј.

## РЎС‚СЂСѓРєС‚СѓСЂР° outputs

РђРєС‚СѓР°Р»СЊРЅР°СЏ С†РµР»РµРІР°СЏ СЃС‚СЂСѓРєС‚СѓСЂР° outputs РѕРїРёСЃР°РЅР° РІ `docs/outputs_structure.md`.

- HTML-РіСЂР°С„РёРєРё СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РІ `outputs/charts/`.
- XLSX РѕР±СЏР·Р°С‚РµР»СЊРЅС‹С… Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёС… С‚Р°Р±Р»РёС† СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РІ `outputs/reports/analytical_tables/`.
- CSV-РєРѕРїРёРё РѕР±СЏР·Р°С‚РµР»СЊРЅС‹С… Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёС… С‚Р°Р±Р»РёС† СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РІ `outputs/exports/analytical_csv/`.
- CSV-РѕСЃРЅРѕРІС‹ РіСЂР°С„РёРєРѕРІ СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РІ `outputs/exports/chart_data/` СЃ СЂР°Р·Р±РёРµРЅРёРµРј РЅР° `risk_quadrant/`, `sankey/`, `boxplot/` Рё `structure/`.
- Dashboard-ready exports СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РІ `outputs/dashboards/`.
- Monthly dashboard exports СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РІ `outputs/dashboards/monthly/`.
- Semantic layer РґР»СЏ dashboard, РµСЃР»Рё РѕРЅ С„РѕСЂРјРёСЂСѓРµС‚СЃСЏ, СЃРѕС…СЂР°РЅСЏРµС‚СЃСЏ РІ `outputs/dashboards/semantic_layer/`.
- Dashboard exports РЅРµ РѕС‚РЅРѕСЃСЏС‚СЃСЏ Рє `outputs/reports/` Рё РЅРµ СЃРјРµС€РёРІР°СЋС‚СЃСЏ СЃ `outputs/exports/chart_data/`.
- РќРµРѕРґРЅРѕР·РЅР°С‡РЅС‹Рµ Рё Р°СЂС…РёРІРЅС‹Рµ outputs РЅРµ СѓРґР°Р»СЏСЋС‚СЃСЏ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё; РґР»СЏ РЅРёС… РїСЂРµРґСѓСЃРјРѕС‚СЂРµРЅС‹ `outputs/exports/technical/review_required/` Рё `outputs/archive/`.

Р‘РµР·РѕРїР°СЃРЅР°СЏ РјРёРіСЂР°С†РёСЏ СЃСѓС‰РµСЃС‚РІСѓСЋС‰РёС… outputs РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ РєРѕРјР°РЅРґРѕР№:

```powershell
.\.venv\Scripts\ofz-clean-outputs.exe --dry-run
```

## Outputs smoke checks

`scripts/smoke_tests.py` Рё `scripts/schema_validation.py` РїСЂРёСЃСѓС‚СЃС‚РІСѓСЋС‚ Рё РґРѕР»Р¶РЅС‹ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊСЃСЏ РєР°Рє СЂРµРіСѓР»СЏСЂРЅС‹Рµ РїСЂРѕРІРµСЂРєРё РїРѕСЃР»Рµ СЂРµРіРµРЅРµСЂР°С†РёРё outputs.

Smoke tests РґРѕР»Р¶РЅС‹ РїСЂРѕРІРµСЂСЏС‚СЊ РЅР°Р»РёС‡РёРµ:

- `outputs/reports/analytical_tables/`
- `outputs/reports/monthly_tables/`
- `outputs/exports/analytical_csv/`
- `outputs/exports/chart_data/risk_quadrant/`
- `outputs/exports/chart_data/sankey/`
- `outputs/exports/chart_data/boxplot/`
- `outputs/exports/chart_data/structure/`
- `outputs/dashboards/`

РџРѕСЃР»Рµ РЅРѕРІРѕРіРѕ Р·Р°РїСѓСЃРєР° pipeline РЅСѓР¶РЅРѕ РѕС‚РґРµР»СЊРЅРѕ РїСЂРѕРІРµСЂСЏС‚СЊ, С‡С‚Рѕ РѕС‚С‡РµС‚РЅС‹Рµ `.xlsx` РЅРµ СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РЅР°РїСЂСЏРјСѓСЋ РІ РєРѕСЂРµРЅСЊ `outputs/exports/`.

Р РµРєРѕРјРµРЅРґСѓРµРјС‹Рµ РєРѕРјР°РЅРґС‹:

```powershell
.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

```powershell
.\.venv\Scripts\python.exe scripts\smoke_tests.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```
## РћР±РЅРѕРІР»РµРЅРЅР°СЏ РїРµСЂРёРѕРґРЅР°СЏ РјРµС‚РѕРґРѕР»РѕРіРёСЏ

- Pipeline РїРѕРґРґРµСЂР¶РёРІР°РµС‚ РїР°СЂР°РјРµС‚СЂ `--aggregation-mode`.
- Р”РѕРїСѓСЃС‚РёРјС‹Рµ Р·РЅР°С‡РµРЅРёСЏ: `cumulative` Рё `point`.
- `cumulative` СЏРІР»СЏРµС‚СЃСЏ default.
- `month + cumulative`: `report_date=2026-05-01` РѕР·РЅР°С‡Р°РµС‚ СЏРЅРІР°СЂСЊ-Р°РїСЂРµР»СЊ 2026.
- `month + point`: `report_date=2026-05-01` РѕР·РЅР°С‡Р°РµС‚ С‚РѕР»СЊРєРѕ Р°РїСЂРµР»СЊ 2026.
- `quarter + cumulative`: `report_date=2026-07-01` РѕР·РЅР°С‡Р°РµС‚ СЏРЅРІР°СЂСЊ-РёСЋРЅСЊ 2026.
- `quarter + point`: `report_date=2026-07-01` РѕР·РЅР°С‡Р°РµС‚ С‚РѕР»СЊРєРѕ II РєРІР°СЂС‚Р°Р» 2026.
- `year`: `report_date=2026-01-01` РѕР·РЅР°С‡Р°РµС‚ Р·Р°РІРµСЂС€РµРЅРЅС‹Р№ 2025 РіРѕРґ.
- Р РµС‚СЂРѕСЃРїРµРєС‚РёРІР° СЃСЂР°РІРЅРёРІР°РµС‚ Р°РЅР°Р»РѕРіРёС‡РЅС‹Рµ РёРЅС‚РµСЂРІР°Р»С‹ РїСЂРѕС€Р»С‹С… Р»РµС‚.
- Outputs РґР»СЏ `cumulative` Рё `point` РЅРµ РґРѕР»Р¶РЅС‹ СЃРјРµС€РёРІР°С‚СЊСЃСЏ; `aggregation_mode` РІРєР»СЋС‡Р°РµС‚СЃСЏ РІ РёРјРµРЅР° С„Р°Р№Р»РѕРІ.

## Monthly layer Рё РїРѕРјРµСЃСЏС‡РЅС‹Рµ РІРёР·СѓР°Р»РёР·Р°С†РёРё

- `scripts/09_monthly_analytics.py` С„РѕСЂРјРёСЂСѓРµС‚ `data/processed/ofz_monthly_metrics.csv`.
- Monthly layer РѕР±СЉСЏСЃРЅСЏРµС‚ СЃРѕСЃС‚Р°РІ РЅР°РєРѕРїР»РµРЅРЅРѕРіРѕ РёС‚РѕРіР°: РјРµСЃСЏС‡РЅС‹Рµ РїРѕРєР°Р·Р°С‚РµР»Рё СЃС‡РёС‚Р°СЋС‚СЃСЏ Р·Р° РєРѕРЅРєСЂРµС‚РЅС‹Р№ РјРµСЃСЏС†, cumulative-РїРѕР»СЏ - СЃ СЏРЅРІР°СЂСЏ РґРѕ С‚РµРєСѓС‰РµРіРѕ РјРµСЃСЏС†Р° РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ.
- `scripts/10_build_monthly_charts.py` СЃС‚СЂРѕРёС‚ РїРѕРјРµСЃСЏС‡РЅС‹Рµ РІРёР·СѓР°Р»РёР·Р°С†РёРё:
  - РїРѕРјРµСЃСЏС‡РЅС‹Р№ РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ;
  - РЅР°РєРѕРїР»РµРЅРЅС‹Р№ РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ;
  - РїРѕРјРµСЃСЏС‡РЅС‹Р№ СЃРїСЂРѕСЃ Рё РїСЂРµРґР»РѕР¶РµРЅРёРµ;
  - РїРѕРјРµСЃСЏС‡РЅС‹Р№ bid-to-cover;
  - РїРѕРјРµСЃСЏС‡РЅСѓСЋ СЃСЂРµРґРЅРµРІР·РІРµС€РµРЅРЅСѓСЋ РґРѕС…РѕРґРЅРѕСЃС‚СЊ;
  - СЃС‚СЂСѓРєС‚СѓСЂСѓ РїРѕ С„РѕСЂРјР°С‚Р°Рј;
  - СЃС‚СЂСѓРєС‚СѓСЂСѓ РїРѕ СЃСЂРѕРєР°Рј;
  - heatmap РјРµСЃСЏС† x РіРѕРґ.
- РЈРїСЂР°РІР»РµРЅС‡РµСЃРєРёР№ СЃРјС‹СЃР» monthly layer - РїРѕРєР°Р·Р°С‚СЊ, РєР°РєРёРµ РјРµСЃСЏС†С‹ Рё С„Р°РєС‚РѕСЂС‹ СЃС„РѕСЂРјРёСЂРѕРІР°Р»Рё РёС‚РѕРіРѕРІС‹Р№ cumulative-СЂРµР·СѓР»СЊС‚Р°С‚.

## РЎС‚Р°Р±РёР»РёР·Р°С†РёСЏ boxplot РґРѕС…РѕРґРЅРѕСЃС‚Рё

- Р“СЂР°С„РёРє `yield_boxplot_by_ofz_type` СЂР°Р·РґРµР»СЏРµС‚ РєРѕСЂРѕС‚РєСѓСЋ Рё РґР»РёРЅРЅСѓСЋ СЂРµС‚СЂРѕСЃРїРµРєС‚РёРІСѓ: РґРѕ С‚СЂРµС… РїРµСЂРёРѕРґРѕРІ РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ grouped mode, РїСЂРё Р±РѕР»СЊС€РµРј С‡РёСЃР»Рµ РїРµСЂРёРѕРґРѕРІ РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ `facet_by_ofz_type`.
- Р”Р»СЏ РґР»РёРЅРЅРѕР№ СЂРµС‚СЂРѕСЃРїРµРєС‚РёРІС‹ РєР°Р¶РґР°СЏ РїР°РЅРµР»СЊ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓРµС‚ РІРёРґСѓ РћР¤Р—, Р° РѕСЃСЊ X РїРѕРєР°Р·С‹РІР°РµС‚ РїРµСЂРёРѕРґС‹ РІ С…СЂРѕРЅРѕР»РѕРіРёС‡РµСЃРєРѕРј РїРѕСЂСЏРґРєРµ.
- Р­РєСЃРїРѕСЂС‚ СЃС‚Р°С‚РёСЃС‚РёРє boxplot СЃРѕС…СЂР°РЅСЏРµС‚СЃСЏ РІ `outputs/exports/chart_data/boxplot/` Рё СЃРѕРґРµСЂР¶РёС‚ `report_period_start`, `report_period_display_label`, `report_period_order`, `ofz_type`, `n`, `min`, `q1`, `median`, `q3`, `max`, `lower_fence`, `upper_fence`, `has_outliers`, `outliers_count`.

## Stacked structure charts

- РЎС‚СЂСѓРєС‚СѓСЂРЅС‹Рµ stacked-РіСЂР°С„РёРєРё РїРѕ СЃСЂРѕРєР°Рј, С„РѕСЂРјР°С‚Р°Рј Рё monthly-СЂР°Р·СЂРµР·Р°Рј РїРѕРєР°Р·С‹РІР°СЋС‚ РёС‚РѕРіРѕРІСѓСЋ СЃСѓРјРјСѓ РЅР°Рґ СЃС‚РѕР»Р±С†РѕРј РїСЂРё РЅР°Р»РёС‡РёРё РґРІСѓС… Рё Р±РѕР»РµРµ СЃРµРіРјРµРЅС‚РѕРІ.
- Р’ chart data exports РґРѕР±Р°РІР»СЏСЋС‚СЃСЏ `column_total`, `segment_share_in_column` Рё `segment_share_total`, РїРѕСЌС‚РѕРјСѓ РёС‚РѕРі СЃС‚РѕР»Р±С†Р° РјРѕР¶РЅРѕ РІРѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ РёР· CSV.
- Р”Р»СЏ СЃСЂРѕРєРѕРІРѕР№ СЃС‚СЂСѓРєС‚СѓСЂС‹ РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ РїРѕСЂСЏРґРѕРє СЃРµРіРјРµРЅС‚РѕРІ: РґРѕР»РіРѕСЃСЂРѕС‡РЅС‹Рµ, СЃСЂРµРґРЅРµСЃСЂРѕС‡РЅС‹Рµ, РєСЂР°С‚РєРѕСЃСЂРѕС‡РЅС‹Рµ, С‚СЂРµР±СѓРµС‚ РїСЂРѕРІРµСЂРєРё.

## РђРєС‚СѓР°Р»РёР·Р°С†РёСЏ С„РёРЅР°Р»СЊРЅРѕРіРѕ СЃРѕСЃС‚РѕСЏРЅРёСЏ РЅР° 2026-05-25

- Р РµР°Р»РёР·РѕРІР°РЅ РёРЅС‚РµСЂР°РєС‚РёРІРЅС‹Р№ Рё РїР°РєРµС‚РЅС‹Р№ Python-first workflow: `scripts/run_pipeline.py` РѕСЃС‚Р°РµС‚СЃСЏ РѕСЃРЅРѕРІРЅС‹Рј РѕСЂРєРµСЃС‚СЂР°С‚РѕСЂРѕРј, `scripts/interactive_pipeline.py` РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ РґР»СЏ СЂСѓС‡РЅРѕРіРѕ РІС‹Р±РѕСЂР° РїР°СЂР°РјРµС‚СЂРѕРІ.
- РџРµСЂРёРѕРґРЅР°СЏ Р°РіСЂРµРіР°С†РёСЏ `cumulative` / `point` СѓР¶Рµ СЂРµР°Р»РёР·РѕРІР°РЅР° СЂР°РЅРµРµ Рё РІ СЌС‚РѕР№ Р°РєС‚СѓР°Р»РёР·Р°С†РёРё РЅРµ РїРµСЂРµРїРёСЃС‹РІР°Р»Р°СЃСЊ.
- `scripts/generate_executive_summary.py` С„РѕСЂРјРёСЂСѓРµС‚ СѓРїСЂР°РІР»РµРЅС‡РµСЃРєРѕРµ СЂРµР·СЋРјРµ С‚РѕР»СЊРєРѕ РЅР° РѕСЃРЅРѕРІР°РЅРёРё СЂР°СЃСЃС‡РёС‚Р°РЅРЅС‹С… С‚Р°Р±Р»РёС†, monthly metrics, dashboard exports Рё chart data.
- Р’СЃРµ РЅРѕРІС‹Рµ РѕС‚С‡РµС‚РЅС‹Рµ Р°СЂС‚РµС„Р°РєС‚С‹ РґРѕР»Р¶РЅС‹ СЃРѕС…СЂР°РЅСЏС‚СЊСЃСЏ РІ РїСЂРѕС„РёР»СЊРЅС‹Рµ РїР°РїРєРё: XLSX РІ `outputs/reports/`, CSV РѕС‚С‡РµС‚РѕРІ РІ `outputs/exports/analytical_csv/`, РѕСЃРЅРѕРІС‹ РіСЂР°С„РёРєРѕРІ РІ `outputs/exports/chart_data/`, dashboard exports РІ `outputs/dashboards/`.
- Р“СЂР°С„РёРєРё СЃ РѕР±СЉРµРјР°РјРё СЂР°Р·РјРµС‰РµРЅРёСЏ РїСЂРёРІРµРґРµРЅС‹ Рє РµРґРёРЅРѕРјСѓ СЃС‚Р°РЅРґР°СЂС‚Сѓ: РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РїРѕ РЅРѕРјРёРЅР°Р»Сѓ, РјР»СЂРґ СЂСѓР±Р»РµР№.
- Р”Р»СЏ boxplot РґРѕС…РѕРґРЅРѕСЃС‚Рё РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ Р°РґР°РїС‚РёРІРЅР°СЏ РєРѕРјРїРѕРЅРѕРІРєР°: grouped mode РґР»СЏ РєРѕСЂРѕС‚РєРѕР№ СЂРµС‚СЂРѕСЃРїРµРєС‚РёРІС‹ Рё facet mode РїРѕ РІРёРґР°Рј РћР¤Р— РґР»СЏ РґР»РёРЅРЅРѕР№ СЂРµС‚СЂРѕСЃРїРµРєС‚РёРІС‹.
- Р”Р»СЏ stacked structure charts РґРѕР±Р°РІР»РµРЅС‹ РёС‚РѕРіРё СЃС‚РѕР»Р±С†РѕРІ, РґРѕР»Рё СЃРµРіРјРµРЅС‚РѕРІ Рё РєРѕРЅС‚СЂРѕР»СЊ РїР°Р»РёС‚СЂС‹.
- Р”Р»СЏ monthly bar/line charts РґРѕР±Р°РІР»РµРЅС‹ РІС‹Р±РѕСЂРѕС‡РЅС‹Рµ РїРѕРґРїРёСЃРё РґР°РЅРЅС‹С…: СЃС‚РѕР»Р±С†С‹ РїРѕРґРїРёСЃС‹РІР°СЋС‚СЃСЏ РїСЂРё РґРѕСЃС‚Р°С‚РѕС‡РЅРѕР№ С‡РёС‚Р°РµРјРѕСЃС‚Рё, line charts РїРѕРґРїРёСЃС‹РІР°СЋС‚ РєР»СЋС‡РµРІС‹Рµ С‚РѕС‡РєРё. РњР°Р»С‹Рµ/РїРµСЂРµРіСЂСѓР¶РµРЅРЅС‹Рµ Р·РЅР°С‡РµРЅРёСЏ РѕСЃС‚Р°СЋС‚СЃСЏ РІ hover Рё CSV.
- Facet-РіСЂР°С„РёРєРё РїСЂРёРІРµРґРµРЅС‹ Рє РїСЂР°РІРёР»Сѓ РѕРґРЅРѕРіРѕ РѕР±С‰РµРіРѕ Y-axis title.
- Scatter-РіСЂР°С„РёРєРё СЃ bubble-size РґРѕР»Р¶РЅС‹ СЏРІРЅРѕ РѕР±СЉСЏСЃРЅСЏС‚СЊ СЂР°Р·РјРµСЂ С‚РѕС‡РєРё; РµСЃР»Рё bubble-size РЅРµ С‡РёС‚Р°РµС‚СЃСЏ, РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ fixed-size fallback, Р° РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РѕСЃС‚Р°РµС‚СЃСЏ РІ hover.
- Р”РѕР±Р°РІР»РµРЅРѕ СЃРµРјРµР№СЃС‚РІРѕ `yield_vs_discount`: main, facet Рё outliers РґР»СЏ Р°РЅР°Р»РёР·Р° СЃРІСЏР·РєРё `РґРёСЃРєРѕРЅС‚ Рє РЅРѕРјРёРЅР°Р»Сѓ` x `РґРѕС…РѕРґРЅРѕСЃС‚СЊ`; СЂР°Р·РјРµСЂ С‚РѕС‡РєРё - РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РїРѕ РЅРѕРјРёРЅР°Р»Сѓ, reference lines - РјРµРґРёР°РЅС‹ РґРёСЃРєРѕРЅС‚Р° Рё РґРѕС…РѕРґРЅРѕСЃС‚Рё.

## Р РµРєРѕРјРµРЅРґСѓРµРјС‹Рµ СѓР»СѓС‡С€РµРЅРёСЏ

- Р”РѕР±Р°РІРёС‚СЊ РµРґРёРЅС‹Р№ `quality_gate.py`, РєРѕС‚РѕСЂС‹Р№ РїРѕСЃР»РµРґРѕРІР°С‚РµР»СЊРЅРѕ Р·Р°РїСѓСЃРєР°РµС‚ `py_compile`, `schema_validation.py`, `regression_tests.py`, `smoke_tests.py` Рё `html_chart_qa.py`.
- Р’РІРµСЃС‚Рё versioned run manifest: РїР°СЂР°РјРµС‚СЂС‹ Р·Р°РїСѓСЃРєР°, СЃРїРёСЃРѕРє РІС…РѕРґРЅС‹С… С„Р°Р№Р»РѕРІ, sha256 РёСЃС‚РѕС‡РЅРёРєРѕРІ, СЃРїРёСЃРѕРє СЃРѕР·РґР°РЅРЅС‹С… outputs Рё СЃС‚Р°С‚СѓСЃ РїСЂРѕРІРµСЂРѕРє.
- Р”РѕР±Р°РІРёС‚СЊ РІРёР·СѓР°Р»СЊРЅСѓСЋ СЂРµРіСЂРµСЃСЃРёРѕРЅРЅСѓСЋ РїСЂРѕРІРµСЂРєСѓ HTML-РіСЂР°С„РёРєРѕРІ С‡РµСЂРµР· СЃРєСЂРёРЅС€РѕС‚С‹ РґР»СЏ РєРѕРЅС‚СЂРѕР»СЏ РЅР°Р»РѕР¶РµРЅРёСЏ РїРѕРґРїРёСЃРµР№ Рё Р»РµРіРµРЅРґ.
- Р Р°СЃС€РёСЂРёС‚СЊ semantic layer: С„РѕСЂРјР°Р»РёР·РѕРІР°С‚СЊ Р±РёР·РЅРµСЃ-СЃР»РѕРІР°СЂСЊ РїРѕРєР°Р·Р°С‚РµР»РµР№, РµРґРёРЅРёС†С‹ РёР·РјРµСЂРµРЅРёСЏ Рё СЃРІСЏР·Рё dashboard datasets.
- Р”РѕР±Р°РІРёС‚СЊ lineage РґРѕ СѓСЂРѕРІРЅСЏ СЃС‚СЂРѕРєРё: raw file / sheet / row -> cleaned row -> feature row -> report scope -> chart/table output.

## Р’С‚РѕСЂР°СЏ РјРѕРґРµСЂРЅРёР·Р°С†РёСЏ: revenue analytics

- Р”РѕР±Р°РІР»РµРЅ СЃРєСЂРёРїС‚ `scripts/11_revenue_analytics.py`.
- РЎРєСЂРёРїС‚ С„РѕСЂРјРёСЂСѓРµС‚ `revenue_summary_<...>.xlsx` РІ `outputs/reports/analytical_tables/` Рё CSV-РІРµСЂСЃРёРё РІ `outputs/exports/analytical_csv/`.
- РћСЃРЅРѕРІРЅРѕР№ source mapping РІС‹СЂСѓС‡РєРё: `revenue_volume = proceeds_mln_rub`, РµСЃР»Рё РєР°РЅРѕРЅРёС‡РµСЃРєР°СЏ РєРѕР»РѕРЅРєР° `revenue_volume` РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚.
- Р Р°СЃСЃС‡РёС‚С‹РІР°СЋС‚СЃСЏ `nominal_revenue_gap`, `revenue_to_nominal_ratio`, `nominal_discount_ratio`, Р° С‚Р°РєР¶Рµ СЃСЂРµР·С‹ РїРѕ РІРёРґСѓ РћР¤Р—, СЃСЂРѕРєРѕРІРѕР№ РєР°С‚РµРіРѕСЂРёРё, С„РѕСЂРјР°С‚Сѓ Рё РјРµСЃСЏС†Р°Рј.
- Р­С‚Р°Рї РґРѕСЃС‚СѓРїРµРЅ РІ pipeline РєР°Рє `--stage revenue_analytics`; РїСЂРё `--all` Р·Р°РїСѓСЃРєР°РµС‚СЃСЏ РїРѕСЃР»Рµ РѕР±СЏР·Р°С‚РµР»СЊРЅС‹С… Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёС… С‚Р°Р±Р»РёС†.
- Р”РѕР±Р°РІР»РµРЅ СЃРєСЂРёРїС‚ `scripts/12_build_revenue_charts.py`.
- Revenue charts СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РІ `outputs/charts/`, Р° CSV-РѕСЃРЅРѕРІС‹ - РІ `outputs/exports/chart_data/structure/`.
- РЎРѕР·РґР°СЋС‚СЃСЏ РіСЂР°С„РёРєРё `revenue_vs_nominal_by_period`, `nominal_revenue_gap_by_period`, `revenue_to_nominal_ratio`, `monthly_revenue_vs_nominal`, `monthly_nominal_revenue_gap`, `revenue_gap_by_ofz_type`, `revenue_gap_by_maturity`, `discount_vs_revenue_gap`.
- Р­С‚Р°Рї РґРѕСЃС‚СѓРїРµРЅ РІ pipeline РєР°Рє `--stage revenue_charts`; РїСЂРё `--all` Р·Р°РїСѓСЃРєР°РµС‚СЃСЏ РїРѕСЃР»Рµ `revenue_analytics`.
- Р”РѕР±Р°РІР»РµРЅ РґРѕРєСѓРјРµРЅС‚ `docs/revenue_kpi_map.md` СЃ С„РѕСЂРјСѓР»Р°РјРё `placement_volume`, `revenue_volume`, `nominal_revenue_gap`, `revenue_to_nominal_ratio` Рё `nominal_discount_ratio`.
- РњРµС‚РѕРґРёС‡РµСЃРєРѕРµ РѕРіСЂР°РЅРёС‡РµРЅРёРµ: РµСЃР»Рё РІС‹СЂСѓС‡РєР° РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚ РёР»Рё РЅРµРїРѕР»РЅР°, РїСЂРѕРµРєС‚ РЅРµ РІС‹РґСѓРјС‹РІР°РµС‚ Р·РЅР°С‡РµРЅРёСЏ Рё С„РёРєСЃРёСЂСѓРµС‚ РѕРіСЂР°РЅРёС‡РµРЅРёРµ С‡РµСЂРµР· `data_quality_flag`.
# Update 2026-06-02: format_nominal_revenue_gap

- Р”РѕР±Р°РІР»РµРЅ РіСЂР°С„РёРє `format_nominal_revenue_gap_<...>.html`: grouped bar РїРѕ С„РѕСЂРјР°С‚Р°Рј СЂР°Р·РјРµС‰РµРЅРёСЏ, РіРґРµ Y = `nominal_revenue_gap_bln`.
- HTML СЃРѕС…СЂР°РЅСЏРµС‚СЃСЏ РІ `outputs/charts/revenue/gap/`.
- CSV-РѕСЃРЅРѕРІР° СЃРѕС…СЂР°РЅСЏРµС‚СЃСЏ РІ `outputs/exports/chart_data/revenue/`.
- Revenue chart data exports С‚РµРїРµСЂСЊ РјР°СЂС€СЂСѓС‚РёР·РёСЂСѓСЋС‚СЃСЏ РІ `outputs/exports/chart_data/revenue/`.
# Update 2026-06-04: format, discount and revenue visualization contracts

- `format_structure_*` РѕРїРёСЃР°РЅ РєР°Рє stacked bar РїРѕ С„РѕСЂРјР°С‚Р°Рј СЂР°Р·РјРµС‰РµРЅРёСЏ: СЃРµРіРјРµРЅС‚С‹ РїРѕРєР°Р·С‹РІР°СЋС‚ `placement_volume_bln`, total label РІС‹РІРѕРґРёС‚СЃСЏ РЅР°Рґ СЃС‚РѕР»Р±С†РѕРј, Р° `label_visible` СѓРїСЂР°РІР»СЏРµС‚ РІРёРґРёРјРѕСЃС‚СЊСЋ РїРѕРґРїРёСЃРµР№ СЃРµРіРјРµРЅС‚РѕРІ.
- `format_discount_*` Р°РєС‚СѓР°Р»РёР·РёСЂРѕРІР°РЅ РєР°Рє grouped bar СЃСЂРµРґРЅРµРІР·РІРµС€РµРЅРЅРѕРіРѕ РґРёСЃРєРѕРЅС‚Р° Рє РЅРѕРјРёРЅР°Р»Сѓ РїРѕ С„РѕСЂРјР°С‚Р°Рј; РѕСЃСЊ Y = `РЎСЂРµРґРЅРµРІР·РІРµС€РµРЅРЅС‹Р№ РґРёСЃРєРѕРЅС‚ Рє РЅРѕРјРёРЅР°Р»Сѓ, Рї.Рї.`.
- `format_nominal_revenue_gap_*` РїРѕРєР°Р·С‹РІР°РµС‚ РґРµРЅРµР¶РЅСѓСЋ СЂР°Р·РЅРёС†Сѓ `placement_volume_bln - revenue_volume_bln` РїРѕ С„РѕСЂРјР°С‚Р°Рј СЂР°Р·РјРµС‰РµРЅРёСЏ.
- `monthly_heatmap_revenue_*` РґРѕР±Р°РІР»РµРЅ РІ РѕРїРёСЃР°РЅРёРµ monthly heatmap: РєРѕР»РѕРЅРєР° `РС‚РѕРіРѕ` СЏРІР»СЏРµС‚СЃСЏ СЃРїСЂР°РІРѕС‡РЅРѕР№ Рё РЅРµ СѓС‡Р°СЃС‚РІСѓРµС‚ РІ РѕСЃРЅРѕРІРЅРѕР№ С†РІРµС‚РѕРІРѕР№ С€РєР°Р»Рµ.
- `format_terms_comparison_*` СЃСЂР°РІРЅРёРІР°РµС‚ С„РѕСЂРјР°С‚С‹ РїРѕ РґРѕС…РѕРґРЅРѕСЃС‚Рё, РґРёСЃРєРѕРЅС‚Сѓ, `revenue_to_nominal_ratio` Рё `nominal_revenue_gap_bln`; РІ hover Рё РїРѕРґРїРёСЃСЏС… РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ `placement_count`.
- `format_terms_scatter_*` РїРѕРєР°Р·С‹РІР°РµС‚ РѕС‚РґРµР»СЊРЅС‹Рµ СЂР°Р·РјРµС‰РµРЅРёСЏ: С†РІРµС‚ = С„РѕСЂРјР°С‚, С„РѕСЂРјР° = РІРёРґ РћР¤Р—, СЂР°Р·РјРµСЂ = РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РїРѕ РЅРѕРјРёРЅР°Р»Сѓ.
- РћРіСЂР°РЅРёС‡РµРЅРёСЏ РїРѕ РѕС‚СЃСѓС‚СЃС‚РІСѓСЋС‰РёРј `discount_to_nominal` Рё `revenue_volume` Р·Р°РєСЂРµРїР»РµРЅС‹: Р·РЅР°С‡РµРЅРёСЏ РЅРµ РІС‹РґСѓРјС‹РІР°СЋС‚СЃСЏ, СЃС‚СЂРѕРєРё РїРѕР»СѓС‡Р°СЋС‚ `data_quality_flag`, Р° РЅРµРїРѕР»РЅС‹Рµ РіСЂР°С„РёРєРё/СЌР»РµРјРµРЅС‚С‹ РґРѕР»Р¶РЅС‹ РёРЅС‚РµСЂРїСЂРµС‚РёСЂРѕРІР°С‚СЊСЃСЏ СЃ СѓС‡РµС‚РѕРј РєР°С‡РµСЃС‚РІР° РґР°РЅРЅС‹С….

