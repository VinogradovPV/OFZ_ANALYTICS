# Ограничения построения графиков

Дата формирования: `2026-06-04 19:08:37`.

## Параметры

- `report_date`: `2026-01-01`
- `retrospective_years`: `4`
- `period_type`: `year`
- `aggregation_mode`: `cumulative`

## Построенные графики

- `outputs/charts/structure/placement_volume/placement_volume_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/risk/target_period/demand_supply_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/risk/target_period/bid_to_cover_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/yield/yield_by_type_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/structure/maturity/maturity_structure_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/structure/format/format_structure_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/structure/format/format_discount_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/structure/format/format_terms_comparison_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/structure/format/format_terms_delta_by_format_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/risk/target_period/risk_quadrant_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/risk/retrospective/risk_quadrant_retrospective_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/yield/boxplot/yield_boxplot_by_ofz_type_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/yield/ofz_pd/yield_boxplot_ofz_pd_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/scatter/demand_cutoff/demand_cutoff_explanation_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/scatter/yield_demand/yield_vs_demand_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/scatter/discount_demand/discount_vs_demand_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/scatter/discount_demand/discount_vs_demand_outliers_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/scatter/discount_demand/discount_vs_demand_logx_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/scatter/yield_discount/yield_vs_discount_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/scatter/yield_discount/yield_vs_discount_outliers_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/scatter/yield_discount/yield_vs_discount_facet_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/scatter/format_terms/format_terms_aggregate_scatter_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/scatter/format_terms/format_terms_scatter_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/risk/outliers/risk_quadrant_retrospective_outliers_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/risk/logx/risk_quadrant_retrospective_logx_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/risk/facet/risk_quadrant_retrospective_facet_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/sankey/structure/sankey_structure_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/sankey/period/sankey_period_maturity_type_format_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/sankey/period/sankey_period_format_type_maturity_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/sankey/period/sankey_period_format_maturity_type_year_cumulative_2026-01-01_retrospective_4.html`
- `outputs/charts/sankey/target_period/sankey_target_period_year_cumulative_2026-01-01_retrospective_4.html`

## Визуальный стандарт

- Для графиков используется приложенная цветовая система: качественная, последовательная, бинарная и сигнальная палитры.
- Легенды, названия осей и отображаемые названия рядов выводятся на русском языке.
- Для столбчатых, линейных и точечных графиков добавлены подписи данных; для Sankey значения доступны в интерактивной подсказке.
- Во всех графиках с объемом размещения показатель трактуется как объем размещения по номиналу; на визуализациях объемы отображаются в млрд рублей, исходные млн рублей сохраняются в chart data.
- Sankey-графики строятся по `placement_volume`; спрос не используется как ширина потоков.
- Для Sankey точные значения малых категорий доступны в hover и таблицах-основах в `outputs/exports/chart_data/sankey/`.
- ДРПА отображаются в Sankey как формат размещения, но не участвуют в demand-based ratios.
- Классификация сроков для Sankey: краткосрочные - до 5 лет включительно, среднесрочные - свыше 5 и до 10 лет включительно, долгосрочные - более 10 лет.
- Sankey по отчетному периоду фильтруется по `is_target_period == True`; при отсутствии колонки используется целевой `report_period_label`.
- Квадрант риска `risk_quadrant` строится только по целевому отчетному периоду.
- Квадрант риска отчетного года `risk_quadrant_demand_to_placement_by_quarter` строится только по отчетному году; по умолчанию подписываются только ключевые выбросы.
- В графике отчетного года цветовая детализация по кварталам может быть ограничена, если в выборке присутствует только один квартал.
- Ретроспективная версия `risk_quadrant_retrospective` строится по всем выбранным периодам и выделяет периоды цветом без разделения по срокам обращения.
- `demand_to_placement_ratio` не равен `bid_to_cover_ratio`: первый показатель равен `demand_volume / placement_volume`, второй - `demand_volume / supply_volume`.
- ДРПА не должны механически включаться в demand-based ratios, если по ним нет валидного спроса.
- Несостоявшиеся аукционы с `placement_volume = 0` исключаются из графиков, где используется `demand_to_placement_ratio`.
- Для анализа причин неудовлетворения спроса нужна цена отсечения или доходность отсечения; без цены отсечения интерпретация дисконта ограничена.

## Ограничения

- Boxplot доходности автоматически переключен в facet mode, потому что выбрано больше трех периодов; на графике показаны компактные подписи медианы и n, а полные статистики доступны в hover и export.
- Boxplot доходности включает разные форматы размещения; формат доступен в tooltip и может влиять на интерпретацию.
- Boxplot доходности содержит группы с `n<3`; распределение статистически ограничено.
- Boxplot доходности содержит группы с `n=1`; такие коробки не интерпретируются как распределение.
- Sankey `sankey_period_format_maturity_type` использует `placement_volume` как value потоков; малые категории не удаляются и могут быть визуально тонкими.
- Sankey `sankey_period_format_type_maturity` использует `placement_volume` как value потоков; малые категории не удаляются и могут быть визуально тонкими.
- Sankey `sankey_period_maturity_type_format` использует `placement_volume` как value потоков; малые категории не удаляются и могут быть визуально тонкими.
- Sankey `sankey_structure` использует `placement_volume` как value потоков; малые категории не удаляются и могут быть визуально тонкими.
- Sankey `sankey_target_period` использует `placement_volume` как value потоков; малые категории не удаляются и могут быть визуально тонкими.
- В boxplot доходности обнаружены ОФЗ-ПК с доходностью около нуля; строки не удаляются автоматически, но помечаются `near_zero_yield_requires_review` и требуют сверки с исходной колонкой доходности.
- График `demand_cutoff_explanation` строится только по целевому отчетному периоду, только по аукционам с валидным спросом и положительным размещением; ретроспективные периоды не включаются.
- График `format_terms_aggregate_scatter` агрегирует строки до уровня report_period_label × format; доходность и дисконт считаются средневзвешенно по placement_volume.
- График `format_terms_delta_by_format` рассчитывает дельты только для периодов, где есть оба формата; отсутствующие пары не рисуются как нулевые значения.
- График `format_terms_scatter` показывает отдельные размещения; подписи ограничены MAX_LABELS_TOTAL=25, остальные детали доступны в hover и CSV.
- График `yield_vs_discount` строится только по строкам с валидными `discount_to_nominal`, доходностью и положительным объемом размещения; дисконт не восстанавливается из цены отсечения.
- График отсечения спроса использует `discount_to_nominal = 100 - cutoff_price`.
- График покрытия предложения спросом рассчитывает периодный bid-to-cover как `sum(demand_volume) / sum(supply_volume)`, а не как среднее строковых ratios.
- Для `discount_vs_demand` используется scatter label policy: подписываются только выбросы, top placement_volume, top X/Y, target period и data_quality_flag; максимум подписей ограничен.
- Из графика отсечения спроса исключены неаукционные строки: 47; анализ строится только по аукционам.
- Из расчета bid-to-cover исключено строк: 67 (неаукционные форматы, отсутствующий спрос/предложение, нулевое предложение или requires_review).
- Квадрант риска отчетного года пропущен: нет строк с доходностью, спросом и положительным размещением.
- На ретроспективном квадранте риска по умолчанию подписываются только ключевые выбросы, чтобы избежать наложения подписей. Все остальные значения доступны через hover.
- Создан отдельный boxplot ОФЗ-ПД: X = период, Y = доходность; на графике показаны min, median, max и n.
