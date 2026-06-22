# Контракт chart data

Дата актуализации: 2026-06-08.

## Назначение

Chart data exports в `outputs/exports/chart_data/` фиксируют табличную основу HTML-графиков. Эти CSV нужны для воспроизводимости визуализаций, HTML QA, visual regression fallback и аудита подписей/hover/единиц измерения.

Generated CSV не коммитятся в обычную Git-историю. Они пересоздаются pipeline и могут сохраняться как release bundle.

## Пути

| Семейство | Путь |
|---|---|
| Monthly charts | `outputs/exports/chart_data/monthly/` или legacy root `outputs/exports/chart_data/monthly_*` |
| Risk quadrant | `outputs/exports/chart_data/risk_quadrant/` |
| Scatter | `outputs/exports/chart_data/scatter/` |
| Structure | `outputs/exports/chart_data/structure/` |
| Revenue | `outputs/exports/chart_data/revenue/` |
| Sankey | `outputs/exports/chart_data/sankey/` |
| Boxplot | `outputs/exports/chart_data/boxplot/` |

Generated exports не должны сохраняться напрямую в `outputs/exports/`.

## Общие обязательные поля

| Поле | Тип | Nullable | Назначение |
|---|---|---|---|
| `report_period_label` | string | no | Техническая метка отчетного периода. |
| `report_year` | integer | no, если применимо | Год периода или размещения. |
| `aggregation_mode` | string | no | `cumulative` или `point`. |
| `data_quality_flag` | string | yes | Машиночитаемый флаг качества данных. |
| `data_quality_display` | string | yes | Человекочитаемое описание качества данных. |

Допустимые `aggregation_mode`: `cumulative`, `point`.

## Поля объема

Все display-поля с суффиксом `_volume_bln` измеряются в млрд рублей. Для каждого такого поля требуется unit-поле.

| Поле значения | Unit field | Обязательное значение |
|---|---|---|
| `placement_volume_bln` | `placement_volume_bln_unit` или `placement_volume_unit` | `млрд рублей` |
| `revenue_volume_bln` | `revenue_volume_bln_unit` или `revenue_volume_unit` | `млрд рублей` |
| `nominal_revenue_gap_bln` | `nominal_revenue_gap_bln_unit` или `nominal_revenue_gap_unit` | `млрд рублей` |
| `total_nominal_volume_bln` | `total_nominal_volume_bln_unit` или `total_nominal_volume_unit` | `млрд рублей` |
| `total_revenue_volume_bln` | `total_revenue_volume_bln_unit` или `revenue_volume_unit` | `млрд рублей` |
| `nominal_volume_bln` | `nominal_volume_bln_unit` или `placement_volume_unit` | `млрд рублей` |
| `discount_gap_bln` | `discount_gap_bln_unit` или `nominal_revenue_gap_unit` | `млрд рублей` |
| `component_volume_bln` | `component_volume_bln_unit` или `placement_volume_unit` | `млрд рублей` |

Если рядом хранится исходное поле в млн рублей (`placement_volume`, `revenue_volume`), для него допустим отдельный unit `млн рублей`. Для display-поля `_bln` unit должен оставаться `млрд рублей`.

Стандартная подпись оси для номинального объема:

`Объем размещения по номиналу, млрд рублей`

Проверка: `scripts/schema_validation.py::validate_volume_bln_units`.

## Поля выручки

| Поле | Тип | Unit | Nullable | Правило |
|---|---|---|---|---|
| `revenue_volume_bln` | number | `млрд рублей` | yes | Выручка от реализации ОФЗ. |
| `nominal_revenue_gap_bln` | number | `млрд рублей` | yes | `placement_volume_bln - revenue_volume_bln`. |
| `revenue_to_nominal_ratio` | number | `%` | yes | `revenue_volume / placement_volume * 100`. |
| `nominal_discount_ratio` | number | `%` | yes | Денежный дисконт к номиналу. |

Если source-поле выручки отсутствует или неполно, export обязан сохранять `data_quality_flag` / `data_quality_display`, а график не должен выдумывать значения.

## Поля доходности

Базовые yield chart data используют `yield_scope=ofz_pd_only`. Заголовки, оси и hover должны явно указывать ОФЗ-ПД. `yield_observation_count` содержит число строк ОФЗ-ПД с числовой доходностью и положительным размещением, а `mixed_security_types` предупреждает, что объем месяца включает другие типы бумаг. ОФЗ-ПК и ОФЗ-ИН не участвуют в числителе, знаменателе, min/median/max и cumulative yield.

| Поле | Тип | Unit | Назначение |
|---|---|---|---|
| `weighted_avg_yield` | number | `% годовых` | Средневзвешенная доходность размещения. |
| `yield_value` | number | `% годовых` | Значение доходности на уровне строки/точки. |
| `source_column_yield` | string | n/a | Исходная колонка доходности. |
| `aggregation_method_yield` | string | n/a | Метод агрегации. |
| `weight_field_yield` | string | n/a | Поле веса, обычно `placement_volume`. |

В title/axis/hover нужно различать:

- `Доходность, % годовых` для неагрегированных точек;
- `Средневзвешенная доходность размещения, % годовых` для агрегированных периодов/форматов.

## Поля дисконта

| Поле | Тип | Unit | Nullable | Правило |
|---|---|---|---|---|
| `discount_to_nominal` | number | `п.п.` | yes | Дисконт к номиналу. |
| `weighted_avg_discount_to_nominal` | number | `п.п.` | yes | Средневзвешенный дисконт. |
| `source_column_discount` | string | n/a | yes | Основной источник дисконта. |
| `aggregation_method_discount` | string | n/a | yes | Метод агрегации. |
| `weight_field_discount` | string | n/a | yes | Поле веса. |
| `discount_calc_method` | string | n/a | yes | Метод расчета или причина отсутствия. |

Основной source: `discount_to_nominal`.

Fallback допускается только если `cutoff_price` выражен в процентах от номинала:

`discount_to_nominal = 100 - cutoff_price`

Display name: `Дисконт к номиналу, п.п.`

Если источник/цена отсутствуют, значение не восстанавливается искусственно; используется quality flag.

## Политика подписей

| Поле | Тип | Nullable | Назначение |
|---|---|---|---|
| `label_display` | string | yes | Текст подписи на графике или в export. |
| `label_visible` | boolean/string boolean | no для label-enabled charts | Реально ли подпись показана. |
| `label_reason` | string | yes | Машиночитаемая причина подписи. |
| `label_reason_display` | string | yes | Русское описание причины подписи. |
| `label_count_display` | string | yes | `n=...` для графиков с количеством размещений. |
| `label_count_visible` | boolean/string boolean | yes | Показывается ли count-label. |
| `segment_label_visible` | boolean/string boolean | yes | Видимость подписи сегмента stacked bar. |
| `discount_label_visible` | boolean/string boolean | yes | Видимость подписи дисконта. |
| `total_label_display` | string | yes | Подпись итога stacked/heatmap/bar. |
| `total_label_y` | number | yes | Y-position итоговой подписи. |

`label_visible=True` означает, что подпись реально выводится в HTML. Скрытые подписи остаются в CSV/hover для аудита.

## Поля качества

| Поле | Тип | Nullable | Назначение |
|---|---|---|---|
| `data_quality_flag` | string | yes | Технический флаг качества. |
| `data_quality_display` | string | yes | Русское описание качества. |
| `is_incomplete_period` | boolean/string boolean | yes | Период неполный по доступным данным. |
| `incomplete_period_reason` | string | yes | Причина неполноты периода. |
| `source_markers` | string | yes | Технические маркеры источника. |
| `demand_cutoff_explanation` | string | yes | Пояснение cutoff/demand logic, если применимо. |

Hover не должен показывать сырые технические значения вместо русских display fields.

## QA / Schema Связь

| Проверка | Что контролирует |
|---|---|
| `schema_validation.py` | Наличие chart data, `*_bln` units, структура outputs. |
| `html_chart_qa.py` | Оси, hover, label limits, bubble-size explanation, chart-specific CSV contracts. |
| `visual_regression.py` | Fallback Plotly JSON/HTML inspection: labels, legends, totals, median/reference lines. |

## Диагностическое follow-up

Полезные правила из `docs/04_visualization/chart_improvement_diagnostics.md` и `docs/04_visualization/format_revenue_discount_chart_diagnostics.md` перенесены в активные data/visualization contracts. Эти diagnostics не удаляются в Этапе 11 и должны быть помечены как `ready_for_archive` в отдельном controlled docs cleanup follow-up.
