# Диагностика графиков форматов, heatmap, дисконта и выручки

## Дополнение 2026-06-02: уточнение format_terms_comparison

Для графика `format_terms_comparison_*` уточнен контракт панели доходности:

- `metric_code`: `yield_weighted_avg`;
- `metric_name_ru`: `Средневзвешенная доходность размещения, % годовых`;
- `source_column`: `weighted_avg_yield`;
- `aggregation_method`: `weighted_average_by_placement_volume`;
- `weight_field`: `placement_volume`.

Технические facet-префиксы `Метрика=`, `metric_label=` и `Показатель=` удаляются после построения Plotly figure. Общая ось Y с названием `Значение` не используется, так как панели имеют разные единицы измерения.

CSV export `format_terms_comparison_<...>.csv` должен содержать поля `report_year`, `report_period_label`, `format`, `format_available`, `metric_code`, `metric_name_ru`, `metric_unit`, `metric_value`, `placement_count`, `aggregation_method`, `source_column`, `weight_field`, `placement_volume_bln`, `label_value_display`, `label_count_display`, `label_display`, `label_visible`, `data_quality_flag`, `data_quality_display`.

## Дополнение 2026-06-02: format_terms_comparison

График `format_terms_comparison_*` строится в `scripts/06_build_charts.py`. Количество размещений нормализовано в поле `placement_count`; источник для текущей реализации - число строк соответствующей группы `report_period_label × format`, синхронизированное с `auction_count`.

Chart data export содержит `placement_count`, `auction_count`, `label_value_display`, `label_count_display`, `label_count_visible`, `label_display`, `label_visible`, `format_available`. Для отсутствующего формата создаются контрольные строки `format_available=False`, `placement_count=0`, но в HTML такие строки не отрисовываются.

Дата диагностики: `2026-06-01`.

Контекст: диагностика выполнена поверх текущей второй модернизации проекта. `data/raw/` не изменяется. Цель блока - подготовить точечные доработки графиков `format_structure`, `monthly_heatmap_placement`, revenue charts и новых графиков условий размещения по форматам `Аукцион / ДРПА`.

## Проверенные файлы

| Файл | Роль в текущей реализации |
| --- | --- |
| `scripts/06_build_charts.py` | Основные графики report scope: structure, risk/scatter, demand cutoff, discount/yield, Sankey. |
| `scripts/10_build_monthly_charts.py` | Помесячные графики, включая monthly structure и `monthly_heatmap_placement`. |
| `scripts/11_revenue_analytics.py` | Revenue tables: summary, by ofz type, by maturity, by format, monthly. |
| `scripts/12_build_revenue_charts.py` | Revenue charts и chart data exports на основе revenue CSV. |
| `scripts/html_chart_qa.py` | HTML/CSV QA для structure, scatter, revenue, yield/discount и facet-контрактов. |
| `scripts/visual_regression.py` | Fallback static HTML / Plotly JSON inspection. |
| `scripts/palette.py` | Цветовые карты форматов, сроков и структурных графиков. |
| `scripts/config.py` | Маршрутизация HTML-графиков и папок outputs. |

## Найденные функции и outputs

| Семейство графиков | Функция | HTML output | Chart data output |
| --- | --- | --- | --- |
| `format_structure_*` | `build_format_structure_chart` в `scripts/06_build_charts.py` | `outputs/charts/structure/format/` | `outputs/exports/chart_data/structure/` |
| `maturity_structure_*` | `build_maturity_structure_chart` в `scripts/06_build_charts.py` | `outputs/charts/structure/maturity/` | `outputs/exports/chart_data/structure/` |
| `monthly_placement_by_format_*` | `build_monthly_placement_by_format_chart` в `scripts/10_build_monthly_charts.py` | `outputs/charts/monthly/structure/` | `outputs/exports/chart_data/` |
| `monthly_placement_by_maturity_*` | `build_monthly_placement_by_maturity_chart` в `scripts/10_build_monthly_charts.py` | `outputs/charts/monthly/structure/` | `outputs/exports/chart_data/` |
| `monthly_heatmap_placement_*` | `build_monthly_heatmap_placement_chart` в `scripts/10_build_monthly_charts.py` | `outputs/charts/monthly/heatmap/` | `outputs/exports/chart_data/` |
| Revenue charts | `build_revenue_vs_nominal_by_period`, `build_nominal_revenue_gap_by_period`, `build_revenue_to_nominal_ratio`, `build_monthly_revenue_vs_nominal`, `build_monthly_nominal_revenue_gap`, `build_revenue_gap_by_ofz_type`, `build_revenue_gap_by_maturity`, `build_discount_vs_revenue_gap` в `scripts/12_build_revenue_charts.py` | `outputs/charts/revenue/...` и `outputs/charts/scatter/discount_revenue_gap/` | сейчас единая папка `outputs/exports/chart_data/structure/` через `REVENUE_CHART_DATA_DIR` |
| Discount/yield scatter | `build_discount_vs_demand_chart`, `build_discount_vs_demand_outliers_chart`, `build_discount_vs_demand_logx_chart`, `build_yield_vs_discount_chart`, `build_yield_vs_discount_outliers_chart`, `build_yield_vs_discount_facet_chart`, `build_demand_cutoff_explanation_chart` в `scripts/06_build_charts.py` | `outputs/charts/scatter/...` | `outputs/exports/chart_data/risk_quadrant/` или `outputs/exports/chart_data/scatter/` |

## 1. Где задается порог скрытия подписей данных

### Report-level structure charts

В `scripts/06_build_charts.py` общий helper `add_stacked_structure_metrics` рассчитывает:

- `column_total`;
- `segment_share_in_column`;
- `segment_share_total`;
- текст сегмента `Подпись`;
- hover-поля объема и долей.

Текущий порог видимости подписи сегмента:

```python
float(row["segment_share_in_column"]) >= 0.08
```

Именно этот порог влияет на `format_structure_*` и `maturity_structure_*`. Для задачи по `format_structure` его нужно снизить или параметризовать отдельно, чтобы малые, но управленчески важные сегменты `ДРПА` чаще получали подписи.

### Monthly stacked/facet charts

В `scripts/10_build_monthly_charts.py` helper `add_monthly_stacked_metrics` задает аналогичную политику:

```python
segment_share_in_column >= 0.08
```

Он влияет на `monthly_placement_by_format_*` и `monthly_placement_by_maturity_*`.

## 2. Где рассчитываются total labels

### Report-level totals

В `scripts/06_build_charts.py` helper `add_stacked_total_labels` добавляет итог над stacked-столбцом, если в столбце два и более сегмента:

- группировка по X-периоду;
- проверка количества сегментов через `nunique`;
- подпись `Итого подпись`;
- вывод через `go.Scatter(mode="text")`.

Используется в structure charts, включая `format_structure`.

### Monthly totals

В `scripts/10_build_monthly_charts.py` helper `add_monthly_stacked_total_labels` добавляет итог над stacked/facet-столбцами:

- группировка по `Год` и `Месяц`;
- проверка количества положительных сегментов;
- подпись `Итого подпись`;
- вывод в соответствующую facet-панель через `row=1, col=index`.

Это место релевантно для `monthly_placement_by_format` и `monthly_placement_by_maturity`.

### Heatmap totals

Для `monthly_heatmap_placement` отдельной подписи итогового размещения поверх heatmap на момент диагностики не выделено как общий helper. Доработку нужно вносить в `build_monthly_heatmap_placement_chart`: добавить отображаемое поле итога по году/периоду или итоговую annotation/side label, а также сохранить соответствующие поля в CSV-основу.

## 3. Какие поля доступны для дисконта

### В report scope / `scripts/06_build_charts.py`

При подготовке данных `prepare_data` формирует:

- `_cutoff_price` из `cutoff_price`;
- `_discount_to_nominal` из `discount_to_nominal`;
- fallback: если `discount_to_nominal` пустой, но есть `_cutoff_price`, тогда `_discount_to_nominal = 100 - _cutoff_price`;
- `_cutoff_yield`;
- `_weighted_avg_yield`;
- `_demand_to_placement`;
- `_bid_to_cover`.

Фактические поля, доступные для графиков условий размещения:

| Поле | Назначение |
| --- | --- |
| `discount_to_nominal` | Исходный дисконт к номиналу, если есть в processed/report scope. |
| `_discount_to_nominal` | Нормализованное рабочее поле для графиков; может быть рассчитано как `100 - cutoff_price`. |
| `cutoff_price` / `_cutoff_price` | Цена отсечения, источник fallback-дисконта. |
| `weighted_avg_yield` / `_weighted_avg_yield` | Доходность для сравнения условий размещения. |
| `cutoff_yield` / `_cutoff_yield` | Доходность отсечения, если доступна. |
| `demand_to_placement_ratio` / `_demand_to_placement` | Спрос / объем размещения. |
| `bid_to_cover_ratio` / `_bid_to_cover` | Спрос / предложение. |
| `format` | Формат размещения: `Аукцион`, `ДРПА`, requires review. |

### В revenue analytics

В `scripts/11_revenue_analytics.py` рассчитывается `nominal_discount_ratio`:

```text
nominal_discount_ratio = nominal_revenue_gap / placement_volume
```

Это не то же самое, что `discount_to_nominal` по цене отсечения. Для новых графиков нужно явно различать:

- `discount_to_nominal` / `_discount_to_nominal`: рыночный/ценовой дисконт к номиналу;
- `nominal_discount_ratio`: дисконт выручки относительно номинала, рассчитанный через `placement_volume - revenue_volume`.

## 4. Какие поля доступны для выручки

### Источник revenue

В `scripts/11_revenue_analytics.py` список кандидатов источника:

- `revenue_volume`;
- `proceeds_volume`;
- `placement_revenue`;
- `placement_revenue_mln_rub`;
- `revenue_amount_mln_rub`;
- `proceeds_mln_rub`;
- `объем выручки`;
- `выручка от реализации`;
- `выручка`.

После подготовки доступны агрегированные поля:

| Поле | Назначение |
| --- | --- |
| `placement_volume` | Номинальный объем размещения, млн рублей. |
| `placement_volume_bln` | Номинальный объем размещения, млрд рублей. |
| `revenue_volume` | Выручка от реализации, млн рублей. |
| `revenue_volume_bln` | Выручка от реализации, млрд рублей. |
| `nominal_revenue_gap` | Номинал минус выручка, млн рублей. |
| `nominal_revenue_gap_bln` | Номинал минус выручка, млрд рублей. |
| `revenue_to_nominal_ratio` | Выручка / номинал. |
| `nominal_discount_ratio` | `(номинал - выручка) / номинал`. |
| `auction_count` | Количество размещений. |
| `data_quality_flag` | Ограничения качества данных. |

### Срезы revenue

`build_revenue_tables` уже создает:

- `summary`;
- `by_ofz_type`;
- `by_maturity`;
- `by_format`;
- `monthly`.

Срез `by_format` является базой для новых графиков различий условий размещения между `Аукцион` и `ДРПА` по выручке, номиналу, разнице и ratios. Для графиков, где нужен `discount_to_nominal` и `weighted_avg_yield`, может потребоваться использовать исходный `ofz_auctions_report_scope.csv`, потому что revenue CSV `by_format` сейчас не хранит ценовой `discount_to_nominal` и доходность.

## 5. Где нужно добавить новые chart data exports

| Новый/дорабатываемый график | Предпочтительный источник | Рекомендуемая папка CSV |
| --- | --- | --- |
| `format_discount_by_format_*` или аналогичный график дисконта по форматам | `data/processed/ofz_auctions_report_scope.csv`, поля `_discount_to_nominal`, `format`, `_placement` | `outputs/exports/chart_data/scatter/` или новая тематическая папка при добавлении в `config.py` |
| `format_yield_by_format_*` | report scope, поля `_weighted_avg_yield`, `format`, `_placement` | `outputs/exports/chart_data/scatter/` или `structure/` в зависимости от типа графика |
| `format_placement_revenue_conditions_*` | revenue `by_format` и/или report scope | `outputs/exports/chart_data/structure/` для bar/structure, `scatter/` для scatter |
| `monthly_heatmap_revenue_*` | revenue `monthly` или `ofz_monthly_metrics.total_revenue_volume` | `outputs/exports/chart_data/` или отдельная `chart_data/structure/` при унификации |
| Доработанный `monthly_heatmap_placement_*` | `data/processed/ofz_monthly_metrics.csv` | текущий `outputs/exports/chart_data/`, добавить поля итогов |

Текущая маршрутизация:

- `scripts/06_build_charts.py`: `chart_data_dir_for_name` отправляет `yield_vs_discount*` в `outputs/exports/chart_data/scatter/`, `discount_vs_demand*` и `demand_cutoff*` - в `risk_quadrant/`, все прочее по умолчанию - в `structure/`.
- `scripts/10_build_monthly_charts.py`: все monthly chart data сейчас сохраняются напрямую в `outputs/exports/chart_data/`.
- `scripts/12_build_revenue_charts.py`: все revenue chart data сохраняются через `REVENUE_CHART_DATA_DIR = config.EXPORTS_CHART_DATA_STRUCTURE_DIR`.

## QA и visual regression

`scripts/html_chart_qa.py` уже проверяет:

- stacked structure charts (`maturity_structure`, `format_structure`, `monthly_placement_by_maturity`, `monthly_placement_by_format`);
- volume scale без `M/B/k`;
- `discount_vs_demand`;
- `demand_cutoff_explanation`;
- `yield_vs_discount`;
- revenue charts.

Для нового блока нужно добавить проверки:

- сниженный/параметризованный порог подписей `format_structure`;
- наличие итоговой подписи в heatmap размещения;
- наличие heatmap по выручке;
- наличие новых графиков условий размещения по форматам;
- наличие CSV-основ с `format`, `discount_to_nominal`, `weighted_avg_yield`, `placement_volume_bln`, `revenue_volume_bln`, `nominal_revenue_gap_bln`, `demand_to_placement_ratio` там, где показатель применим.

`scripts/visual_regression.py` уже выполняет fallback inspection HTML/Plotly JSON. Для нового блока нужно добавить статические проверки:

- `format_structure`: больше подписей данных у малых сегментов или наличие `label_visible/label_reason` в CSV;
- `monthly_heatmap_placement`: есть итоговая подпись или annotation;
- `monthly_heatmap_revenue`: график существует, colorbar в млрд рублей;
- новые discount/revenue/format charts: оси и hover русифицированы, размер/единицы размещения указаны.

## Маршрутизация и палитра

`scripts/config.py` уже содержит:

- `CHARTS_STRUCTURE_FORMAT_DIR` для `format_structure`;
- `CHARTS_MONTHLY_HEATMAP_DIR` для `monthly_heatmap_placement`;
- `CHARTS_REVENUE_*` для revenue charts;
- `CHARTS_SCATTER_DISCOUNT_REVENUE_GAP_DIR`, `CHARTS_SCATTER_DISCOUNT_DEMAND_DIR`, `CHARTS_SCATTER_DEMAND_CUTOFF_DIR`, `CHARTS_SCATTER_YIELD_DISCOUNT_DIR`.

Для новых графиков по условиям размещения между `Аукцион / ДРПА` возможны два варианта:

1. Использовать существующие папки `outputs/charts/scatter/...` и `outputs/charts/revenue/...`.
2. Добавить отдельную папку, например `outputs/charts/scatter/format_conditions/`, если семейство графиков станет отдельным блоком.

`scripts/palette.py` уже содержит:

- `FORMAT_COLOR_MAP`: `Аукцион`, `ДРПА`, `Требует проверки`;
- `BINARY_PALETTE` на основе `FORMAT_COLOR_MAP`;
- `STRUCTURE_PALETTE` без проблемного соседства синего и желтого.

Для новых графиков сравнения `Аукцион / ДРПА` рекомендуется использовать `FORMAT_COLOR_MAP`, чтобы формат размещения был стабилен во всех визуализациях.

## Вывод для следующего шага

1. Для `format_structure` надо снизить порог подписи сегментов с `8%` до более низкого значения или сделать отдельный параметр для форматов.
2. Для heatmap размещения нужно добавить итоговую подпись/annotation и поля в CSV.
3. Heatmap выручки можно строить из `ofz_monthly_metrics.total_revenue_volume` или из revenue monthly CSV; предпочтительно использовать уже рассчитанный monthly/revenue layer, не пересчитывая периодную фильтрацию.
4. Новые графики различий условий `Аукцион / ДРПА` должны различать ценовой `discount_to_nominal` и revenue-based `nominal_discount_ratio`.
5. Новые chart data exports нужны для каждого нового графика, с явными единицами, format, data quality и исходными metric columns.
## Update: format_discount composite contract

`format_discount_*` доработан как composite stacked bar:

- `placement_volume_bln` остается единственной метрикой высоты сегмента;
- `weighted_avg_discount_to_nominal` отображается подписью сегмента, а не отдельным столбцом;
- текущий горизонтальный маркер дисконта убран из основного отображения, чтобы не создавать ложное впечатление второй оси;
- подписи разделены на `segment_label_*`, `discount_label_*` и `total_label_*`;
- `data_quality_flag` остается в CSV для аудита, но hover использует человекочитаемый `data_quality_display`;
- CSV export: `outputs/exports/chart_data/structure/format_discount_<...>.csv`.

QA-контракт проверяет наличие `placement_volume_bln`, `weighted_avg_discount_to_nominal`, `segment_label_visible`, `discount_label_visible`, `total_label_display`, `data_quality_display`, отсутствие отдельного bar trace для дисконта и наличие total labels.
## Update 2026-06-02: format_discount mini-indicator and segment geometry

- `format_discount_*` stores segment geometry fields: `segment_base_y`, `segment_top_y`, `segment_mid_y`, `segment_height`.
- Discount magnitude is encoded by an annotation mini-indicator/badge using `discount_bar_norm` and `discount_bar_visible`; it is not a separate bar trace and does not use a second Y-axis.
- DRPA labels are tied to their own segment coordinates and must not fall inside the auction segment.
- Total labels use `total_label_y`, which is above `total_placement_volume_bln`.
- HTML QA and visual regression fallback check CSV geometry, the mini-indicator/badge contract, nominal-volume Y-axis wording and absence of raw `data_quality_flag` in hover.
## Итоговая реализация format_discount

Предыдущая идея с мини-индикатором дисконта заменена на компонентное разложение номинала. Новый график `format_discount_*` показывает внутри каждого форматного сегмента две денежные части: выручку и дисконтный разрыв.

Проверочный контракт:

- `component_type` принимает значения `revenue` и `discount_gap`;
- `component_volume_bln` используется как высота stacked-компонента;
- `nominal_volume_bln = revenue_volume_bln + discount_gap_bln`;
- ось Y подписана как `Объем размещения по номиналу, млрд рублей`;
- дисконт в п.п. доступен в hover и CSV как `weighted_avg_discount_pp`, но не является отдельным bar trace;
- hover использует человекочитаемый `data_quality_display`.

Chart data export сохраняется в `outputs/exports/chart_data/structure/format_discount_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.csv`.
## Дополнение 2026-06-02: format_terms_scatter

Добавлен scatter-график `format_terms_scatter_*` для сравнения условий отдельных размещений по форматам `Аукцион` и `ДРПА`.

- X: `discount_to_nominal`, дисконт к номиналу, п.п.
- Y: `weighted_avg_yield`, доходность, % годовых.
- Цвет: `format`.
- Размер точки: `placement_volume_bln`.
- Подписи: максимум 25 точек по policy `top_discount`, `top_yield`, `top_nominal_revenue_gap`, `top_placement`, `data_quality_flag`.
- Export: `outputs/exports/chart_data/scatter/format_terms_scatter_<...>.csv`.

График строится только по строкам с валидными дисконтом, доходностью и положительным объемом размещения. Выручка и разница номинал-выручка добавляются в hover и export, если фактическое поле выручки найдено в processed/report scope данных.
# Доработка format_terms_delta_by_format

`format_terms_delta_by_format_*` сохраняет расчет `delta = ДРПА − Аукцион`, но интерпретация вынесена в отдельные поля export. Для каждой метрики задается `metric_preference_direction`: `lower_is_better` для доходности, дисконта и `номинал − выручка`; `higher_is_better` для `выручка / номинал`.

Порог малозначимой разницы (`assessment_threshold`) равен `0.10 п.п.` для относительных метрик и `10 млрд рублей` для абсолютной разницы `номинал − выручка`. На графике цвет показывает `drpa_condition_assessment_ru`, а не простой знак дельты.

Hover сделан компактным: показывает значения ДРПА и Аукцион, дельту, оценку, количество размещений, объемы по форматам, метод агрегации и короткое описание качества данных. Полный список флагов качества остается в CSV export.

## QA-контракты format_terms

HTML QA и visual regression теперь проверяют три уровня `format_terms`:

- `format_terms_aggregate_scatter_*`: одна строка CSV соответствует `report_period_label × format`, цветовой слой - формат, размер точки - `placement_volume_bln`, есть `placement_count` и методологические поля доходности/дисконта.
- `format_terms_scatter_*`: цвет - формат, symbol - вид ОФЗ, смешанная категория `format + ofz_type` не используется как основной цвет, есть `label_visible`, есть пояснение размера точки, hover не содержит сырой `data_quality_flag`.
- `format_terms_delta_by_format_*`: есть `delta_drpa_minus_auction`, фиктивные дельты не создаются, subtitle объясняет знак дельты и цветовую оценку.

Название доходности в scatter-графиках раскрывает используемую методологию: `Средневзвешенная доходность размещения, % годовых`, а CSV хранит `source_column_yield`, `aggregation_method_yield` и `weight_field_yield`.
