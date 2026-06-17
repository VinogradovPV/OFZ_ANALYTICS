# Контракт аналитических таблиц

Дата актуализации: 2026-06-08.

## Назначение

Analytical tables в `outputs/reports/analytical_tables/`, `outputs/reports/monthly_tables/` и CSV exports в `outputs/exports/analytical_csv/` дают табличные результаты для аудита, Excel-потребления и сверки с визуализациями.

Generated analytical outputs не коммитятся в Git; они пересоздаются pipeline и сохраняются как release artifacts при необходимости.

## Основные семейства

| Семейство | Путь | Назначение |
|---|---|---|
| Analytical summary | `outputs/reports/analytical_tables/*.xlsx` | Основные периодные таблицы. |
| Analytical CSV | `outputs/exports/analytical_csv/*.csv` | Машиночитаемые версии таблиц. |
| Monthly tables | `outputs/reports/monthly_tables/*.xlsx` | Помесячный аналитический слой. |
| Revenue summary | `revenue_summary_<...>.xlsx/.csv` | Аналитика выручки и разницы номинал-выручка. |

## Обязательные поля revenue summary

| Поле | Тип | Unit | Nullable |
|---|---|---|---|
| `report_period_label` | string | n/a | no |
| `report_period_start` | date | n/a | no |
| `report_period_end` | date | n/a | no |
| `report_year` | integer | n/a | no |
| `aggregation_mode` | string | n/a | no |
| `placement_volume` | number | млн рублей | yes |
| `placement_volume_bln` | number | млрд рублей | yes |
| `revenue_volume` | number | млн рублей | yes |
| `revenue_volume_bln` | number | млрд рублей | yes |
| `nominal_revenue_gap` | number | млн рублей | yes |
| `nominal_revenue_gap_bln` | number | млрд рублей | yes |
| `revenue_to_nominal_ratio` | number | % | yes |
| `nominal_discount_ratio` | number | % | yes |
| `auction_count` | integer | count | no |
| `data_quality_flag` | string | n/a | yes |

## Дополнительные срезы

Допустимые срезы:

- `by_ofz_type`;
- `by_maturity`;
- `by_format`;
- `monthly`.

Для срезов обязательны соответствующие dimension fields: `ofz_type`, `maturity_bucket_label`, `format`, `month`/`month_order`.

## Политика nullable-полей

- Revenue fields nullable, если source-поле выручки отсутствует или неполно.
- Ratio fields nullable при нулевом/отсутствующем знаменателе.
- Missing revenue не заменяется нулем.
- `data_quality_flag` обязателен для строк с отсутствующей/неполной выручкой или аномальной разницей номинал-выручка.

## QA / Schema Связь

- `quality_gate.py --fast` проверяет наличие аналитических таблиц.
- `schema_validation.py` проверяет базовую структуру report scope и outputs.
- `anomaly_tests.py` фиксирует revenue gap anomalies.
- `revenue_analytics_report.md` документирует ограничения revenue data.
