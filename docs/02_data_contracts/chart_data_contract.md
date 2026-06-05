# Контракт chart data exports

Дата актуализации: 2026-06-04.

## Назначение

Chart data exports в `outputs/exports/chart_data/` фиксируют табличные основы HTML-графиков. Эти CSV нужны для проверки визуализаций, воспроизводимости показателей и BI/QA-аудита.

## Единицы измерения объемов

Все поля с суффиксом `_volume_bln` должны измеряться в млрд рублей.

Обязательное правило для chart data exports с объемными показателями:

- если CSV содержит `placement_volume_bln`, рядом должно быть unit-поле;
- если CSV содержит `revenue_volume_bln`, рядом должно быть unit-поле;
- если CSV содержит `nominal_revenue_gap_bln`, рядом должно быть unit-поле;
- если CSV содержит `total_nominal_volume_bln`, рядом должно быть unit-поле.

Рекомендуемые имена unit-полей:

| Поле показателя | Unit-поле | Значение |
|---|---|---|
| `placement_volume_bln` | `placement_volume_unit` | `млрд рублей` |
| `revenue_volume_bln` | `revenue_volume_unit` | `млрд рублей` |
| `nominal_revenue_gap_bln` | `nominal_revenue_gap_unit` | `млрд рублей` |
| `total_nominal_volume_bln` | `total_nominal_volume_unit` | `млрд рублей` |

`schema_validation.py` проверяет наличие unit-колонок для chart data exports с объемами. Отсутствие таких колонок считается production blocker, потому что без них нельзя однозначно отличить исходные млн рублей от отображаемых млрд рублей.

## Применение

Правило применяется ко всем новым chart data exports независимо от:

- `period_type`: `month`, `quarter`, `year`;
- `aggregation_mode`: `cumulative`, `point`;
- `report_date`;
- `retrospective_years`.

Для графиков `format_terms_aggregate_scatter_*` и `format_discount_*` unit-поля добавляются генератором `scripts/06_build_charts.py`, а не ручной правкой готовых CSV.
