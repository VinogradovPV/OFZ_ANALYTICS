# Диагностика функций доработки графиков

Дата диагностики: 2026-05-27.

Документ фиксирует текущее состояние функций построения графиков перед точечными доработками блока `monthly`, `facet`, `scatter` и нового квадранта `доходность / дисконт`. Логика графиков на этом шаге не изменялась.

## Проверенные файлы

| Файл | Роль |
|---|---|
| `scripts/10_build_monthly_charts.py` | Помесячные bar/line/facet/heatmap-графики. |
| `scripts/06_build_charts.py` | Основные графики, risk quadrant, demand cutoff, discount vs demand, Sankey, boxplot. |
| `scripts/scatter_chart_policy.py` | Общая политика подписей scatter-графиков и ratio basis. |
| `scripts/palette.py` | Цветовые карты и палитры. |
| `scripts/html_chart_qa.py` | HTML QA по структуре, подписям, scatter policy, volume policy. |
| `scripts/visual_regression.py` | Fallback HTML / Plotly JSON inspection для визуальной регрессии. |

## Карта функций

| График / семейство | Функция | Файл | Текущая логика |
|---|---|---|---|
| `monthly_placement_volume` | `build_monthly_placement_volume_chart` | `scripts/10_build_monthly_charts.py` | Grouped bar, подписи столбцов уже есть через `total_placement_volume_bln_label`. |
| `monthly_cumulative_placement` | `build_monthly_cumulative_placement_chart` | `scripts/10_build_monthly_charts.py` | Line chart, подписи есть у всех точек через `cumulative_placement_volume_bln_label`, но нет политики отбора ключевых точек. |
| `monthly_demand_supply` | `build_monthly_demand_supply_chart` | `scripts/10_build_monthly_charts.py` | Grouped/facet bar, подписи данных отсутствуют: в `px.bar` не задан `text`, нет label columns. |
| `monthly_bid_to_cover` | `build_monthly_bid_to_cover_chart` | `scripts/10_build_monthly_charts.py` | Активная функция переопределена ниже legacy-версии; использует `prepare_monthly_bid_to_cover_labels`, `label_display`, `label_reason`, threshold line y=1. |
| `monthly_weighted_avg_yield` | `build_monthly_weighted_avg_yield_chart` | `scripts/10_build_monthly_charts.py` | Line chart, подписи есть у всех точек, без адаптивного ограничения. |
| `monthly_placement_by_format` | `build_monthly_placement_by_format_chart` | `scripts/10_build_monthly_charts.py` | Stacked bar with `facet_col="Год"`, внутренние подписи сегментов и total labels есть. Вероятен повтор Y-axis title по facet-панелям. |
| `monthly_placement_by_maturity` | `build_monthly_placement_by_maturity_chart` | `scripts/10_build_monthly_charts.py` | Stacked bar with `facet_col="Год"`, внутренние подписи сегментов и total labels есть. Вероятен повтор Y-axis title по facet-панелям. |
| `monthly_heatmap_placement` | `build_monthly_heatmap_placement_chart` | `scripts/10_build_monthly_charts.py` | Heatmap, colorbar подписан в млрд рублей. |
| `risk_quadrant` | `build_risk_quadrant_chart` | `scripts/06_build_charts.py` | Target-period scatter, size=`_placement`, подписи через `scatter_chart_policy.add_scatter_labels`, есть аннотация размера точки. |
| `risk_quadrant_retrospective` | `build_retrospective_risk_quadrant_chart` | `scripts/06_build_charts.py` | Retrospective scatter, size=`_placement`, подписи через policy, есть аннотация размера точки. |
| Risk outliers/log-X/facet | `build_risk_quadrant_retrospective_outliers_chart`, `build_risk_quadrant_retrospective_logx_chart`, `build_risk_quadrant_retrospective_facet_chart` | `scripts/06_build_charts.py` | Используют общий `build_policy_scatter_figure`; подписи и bubble annotation централизованы. |
| `demand_cutoff_explanation` | `build_demand_cutoff_explanation_chart` | `scripts/06_build_charts.py` | Scatter по целевому периоду, size=`_placement`, color=yield. Есть текст про размер точки, но нет bubble-size legend/настройки `sizeref/sizemin/sizemax`, как в `build_policy_scatter_figure`. |
| `discount_vs_demand` | `build_discount_vs_demand_chart` | `scripts/06_build_charts.py` | Dense scatter main clipped, использует `build_policy_scatter_figure`, есть label policy, size annotation и export через `scatter_export_data`. |
| `discount_vs_demand_outliers` | `build_discount_vs_demand_outliers_chart` | `scripts/06_build_charts.py` | Outliers-версия, использует `build_policy_scatter_figure`. |
| `discount_vs_demand_logx` | `build_discount_vs_demand_logx_chart` | `scripts/06_build_charts.py` | Log-X версия, использует `build_policy_scatter_figure`. |
| `yield_vs_demand` | `build_yield_vs_demand_chart` | `scripts/06_build_charts.py` | Scatter, использует `build_policy_scatter_figure`, size=`_placement`. |

## 1. Где не хватает подписей данных

| Место | Диагноз | Что потребуется обновить |
|---|---|---|
| `monthly_demand_supply` | В `px.bar` не задан `text`, в `long_df` нет готовой подписи значения. Hover есть, но на столбцах значений нет. | Добавить форматированную колонку подписи для спроса/предложения в млрд рублей и `text=...`; для малых столбцов можно использовать `uniformtext_mode="hide"` или threshold. |
| `monthly_cumulative_placement` | Подписи есть у всех точек. Для длинного ряда это может перегружать график; для текущей задачи нужны осмысленные подписи ключевых точек. | Добавить label policy для line charts: последняя точка года, максимум/минимум, отчетный год, ключевые изменения. |
| `monthly_weighted_avg_yield` | Подписи есть у всех точек, без отбора. | Аналогичная line-label policy, если график считается аналогичным line chart. |
| `monthly_placement_by_format` | Внутренние подписи сегментов и total labels есть. Малые сегменты скрываются через `uniformtext_mode="hide"`, детализация есть в hover. | Проверить читаемость после удаления повторных Y-axis titles. |
| `monthly_placement_by_maturity` | Внутренние подписи сегментов и total labels есть. | Проверить читаемость после удаления повторных Y-axis titles. |
| `demand_cutoff_explanation` | Подписи точек формируются через `scatter_chart_policy`, но размер окружности не имеет полноценной визуальной легенды. | Добавить bubble-size annotation/legend по аналогии с `build_policy_scatter_figure`; желательно обновить `sizeref/sizemin/sizemax`. |

## 2. Где повторяется подпись оси Y

| Место | Причина | Диагноз |
|---|---|---|
| `monthly_placement_by_format` | `facet_col="Год"` и общий `apply_monthly_volume_axis()` вызывают `figure.update_yaxes(title_text=...)` для всех Y-осей. | Нужно оставить title только у первой/левой Y-оси, остальные очистить. |
| `monthly_placement_by_maturity` | Аналогично: `facet_col="Год"` плюс общий `update_yaxes`. | Нужен helper для facet Y-axis titles. |
| Потенциально другие facet charts | `risk_quadrant_retrospective_facet` использует `build_policy_scatter_figure` с `facet_column`; там `fig.update_yaxes(title_text=y_title)` может размножать title по панелям. | Для текущего шага основной ручной дефект указан на monthly facet, но helper стоит сделать переиспользуемым. |

## 3. Где используется bubble size

| График | Size column | Где задано | Комментарий |
|---|---|---|---|
| `risk_quadrant` | `_placement` | `px.scatter(..., size="_placement")` | Есть текстовая аннотация размера точки, но настройка размера менее централизована, чем в policy builder. |
| `risk_quadrant_retrospective` | `_placement` | `px.scatter(..., size="_placement")` | Есть аннотация размера точки. |
| `risk_quadrant_demand_to_placement_by_quarter` | `_placement` | `px.scatter(..., size="_placement")` | Есть аннотация размера пузыря. |
| `yield_vs_demand` | `_placement` | Через `build_policy_scatter_figure` | Есть централизованный `sizeref`, `sizemin`, opacity и bubble annotation. |
| `discount_vs_demand` | `_placement` | Через `build_policy_scatter_figure` | Есть централизованный `sizeref`, `sizemin`, opacity и bubble annotation. |
| `discount_vs_demand_outliers` | `_placement` | Через `build_policy_scatter_figure` | Есть централизованный bubble policy. |
| `discount_vs_demand_logx` | `_placement` | Через `build_policy_scatter_figure` | Есть централизованный bubble policy. |
| `demand_cutoff_explanation` | `_placement` | `px.scatter(..., size=size_column)` | Размер используется, но без централизованной настройки marker size и без bubble-size legend. |

## 4. Где отсутствует или недостаточно пояснен размер точки

| Место | Диагноз |
|---|---|
| `demand_cutoff_explanation` | Есть подзаголовок с текстом `Размер точки = объем размещения по номиналу`, но нет отдельной bubble-size annotation `малый / средний / крупный объем`, нет явной настройки `sizemode/sizeref/sizemin`. Именно этот график требует доработки. |
| `risk_quadrant` и `risk_quadrant_retrospective` | Пояснение есть, но они построены напрямую через `px.scatter`, а не через `build_policy_scatter_figure`; при будущей унификации можно перенести настройку marker size в общий helper. |
| `build_policy_scatter_figure` | Размер объяснен через аннотацию и настроен через `sizemode="area"`, `sizeref`, `sizemin=6`, `size_max=42`. Это целевой стандарт для dense scatter. |

## 5. Chart data exports, которые нужно обновить

| Export | Текущая папка | Что добавить / проверить |
|---|---|---|
| `monthly_demand_supply_<...>.csv` | `outputs/exports/chart_data/structure/` через `make_result` monthly-модуля | Добавить `label_display` или аналогичную колонку для подписей спроса/предложения; проверить единицы млрд рублей. |
| `monthly_cumulative_placement_<...>.csv` | `outputs/exports/chart_data/structure/` | Добавить `label_display`, `label_reason` для line-label policy. |
| `monthly_weighted_avg_yield_<...>.csv` | `outputs/exports/chart_data/structure/` | Если будет применяться line-label policy, добавить `label_display`, `label_reason`. |
| `monthly_placement_by_format_<...>.csv` | `outputs/exports/chart_data/structure/` | Уже содержит stacked metrics, но нужно проверить наличие `column_total`; при необходимости сохранить `label_display`/`segment_label_display`. |
| `monthly_placement_by_maturity_<...>.csv` | `outputs/exports/chart_data/structure/` | Аналогично: проверить `column_total`, доли сегментов и единицы. |
| `demand_cutoff_explanation_<...>.csv` | `outputs/exports/chart_data/risk_quadrant/` | Добавить/проверить `label_display`, `label_reason`, `placement_volume_bln`, поля bubble policy (`bubble_size_bucket` или аналог, если будет добавлен). |
| `discount_vs_demand_<...>.csv` | `outputs/exports/chart_data/risk_quadrant/` | Уже формируется через `scatter_export_data`; проверить, что `label_display`, `label_reason`, `x_value`, `y_value`, `placement_volume_bln` сохраняются. |
| `discount_vs_demand_outliers_<...>.csv` | `outputs/exports/chart_data/risk_quadrant/` | Аналогично основному export. |
| `discount_vs_demand_logx_<...>.csv` | `outputs/exports/chart_data/risk_quadrant/` | Аналогично основному export. |
| Новый квадрант `yield_discount_quadrant_<...>.csv` | Предпочтительно `outputs/exports/chart_data/risk_quadrant/` или `scatter/` при расширении структуры | Нужны `discount_to_nominal`, yield column, placement volume, label policy fields, target-period flag, data quality fields. |

## Дополнительные наблюдения

- В `scripts/10_build_monthly_charts.py` присутствует legacy-функция `_build_monthly_bid_to_cover_chart_legacy` и активная `build_monthly_bid_to_cover_chart` ниже по файлу. `chart_builders()` ссылается на имя функции и при вызове использует актуальное позднее определение.
- В `scripts/06_build_charts.py` есть legacy-вариант `_build_discount_vs_demand_chart_legacy`, но активные функции `build_discount_vs_demand_chart`, `build_discount_vs_demand_outliers_chart`, `build_discount_vs_demand_logx_chart` используют новую scatter policy.
- `scripts/scatter_chart_policy.py` содержит рабочую логику `MAX_SCATTER_LABELS = 30`, выбор outliers/top values/target period/data_quality_flag, но файл отображается в PowerShell с mojibake. Логика при этом читается как UTF-8 в Python.
- `scripts/html_chart_qa.py` уже проверяет recursive HTML (`rglob`), monthly bid-cover contract, dense scatter contract, risk/scatter label limit, boxplot и revenue charts. Для нового этапа нужно будет добавить проверки monthly grouped bar labels, facet Y-title policy и нового квадранта discount/yield.
- `scripts/visual_regression.py` сейчас использует `args.charts_dir.glob("*.html")`, то есть смотрит только корень `outputs/charts`. После реорганизации графиков это потенциальный дефект fallback visual regression: нужно перейти на recursive `rglob("*.html")`.

## Рекомендуемый порядок дальнейших правок

1. Добавить общий helper для line/bar labels в `scripts/10_build_monthly_charts.py`.
2. Исправить facet Y-axis title policy для `monthly_placement_by_format` и `monthly_placement_by_maturity`.
3. Унифицировать bubble-size policy для `demand_cutoff_explanation` с `build_policy_scatter_figure`.
4. Добавить новый квадрант `discount_to_nominal` × yield с chart data export и QA-check.
5. Обновить `html_chart_qa.py` и `visual_regression.py` под новые проверки и рекурсивную структуру графиков.

## Уточнение диагностики `yield_vs_discount`

- Семейство состоит из main/facet/outliers: main используется для общей карты риска, facet - для сопоставления периодов, outliers - для быстрой проверки экстремальных точек.
- Main/outliers-графики должны группироваться цветом по `report_year`; сроковая категория остается в hover.
- Facet-график использует человекочитаемые панели вида `2022: янв–апр`, общие шкалы X/Y и одну общую подпись каждой оси.
- Для facet-графика дополнительно проверяется порядок панелей по `report_period_order` и отсутствие размноженных подписей медианных линий.
- CSV export должен включать `report_year`, `discount_to_nominal`, `weighted_avg_yield`, `placement_volume_bln`, `label_visible`, `median_scope`, `data_quality_display` и `label_reason_display`.
- QA расширен проверками: цвет по году, легенда "Год", отсутствие повторяющихся axis title в facet и наличие chart data export.
- Новая facet-policy для `yield_vs_discount_facet`: максимум 3 видимые подписи на панель и 15 на весь график; видимость фиксируется в `label_visible`.
- Для main/outliers действует `median_scope=global`; подписи линий разделены на `мед. дисконт` и `мед. доходность`. Для facet действует `median_scope=period`, а методология медианных линий вынесена в subtitle, чтобы не перегружать панели.
- Размер точки = объем размещения по номиналу; на графиках есть subtitle/annotation с ориентирами `50 / 250 / 500 млрд руб.`, точное значение остается в hover.
- Outliers-график отбирает экстремумы по дисконту, доходности или объему размещения; причина подписи сохраняется в `label_reason` и переводится в `label_reason_display`.
- Для панели 2022 в текущем наборе пригодных строк доступны только январь-февраль, поэтому заголовок `2022: янв–фев` считается особенностью данных, а не ошибкой оси. В export добавляется `is_incomplete_period`.

## Диагностика подписей и facet-осей

- `monthly_demand_supply` должен иметь подписи на столбцах спроса и предложения либо `label_display` в CSV-основе; ось Y - `Объем, млрд рублей`.
- `monthly_cumulative_placement` должен иметь подписи ключевых точек; ось Y - `Накопленный объем размещения по номиналу, млрд рублей`.
- Facet-графики (`monthly_placement_by_format`, `monthly_placement_by_maturity`, `yield_vs_discount_facet` и аналогичные) должны иметь один общий Y-axis title без повторения в каждой панели.
- `demand_cutoff_explanation` и другие scatter-графики с bubble-size должны иметь пояснение размера точки. Если используется fixed-size fallback, объем размещения остается в hover.
- `yield_vs_discount` должен иметь reference lines по медианному дисконту и медианной доходности; для facet используется пояснение в subtitle, что пунктирные линии - медианы периода.
