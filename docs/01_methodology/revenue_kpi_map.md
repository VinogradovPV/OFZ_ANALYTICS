# Revenue KPI map

Документ фиксирует показатели revenue analytics второй модернизации проекта OFZ_ANALITICS.

## Источник

- Основной dataset: `data/processed/ofz_auctions_report_scope.csv`.
- Табличный слой: `scripts/11_revenue_analytics.py`.
- Графический слой: `scripts/12_build_revenue_charts.py`.
- Приоритетная колонка выручки: `revenue_volume`.
- Для текущего processed-контура фактический источник выручки: `proceeds_mln_rub`.

Если надежная колонка выручки отсутствует, скрипт не подставляет синтетические значения: revenue KPI остаются пустыми или получают `data_quality_flag`.

## KPI

| KPI | Формула | Единица | Назначение | Ограничения |
| --- | --- | --- | --- | --- |
| `placement_volume` | сумма нормализованного объема размещения по номиналу | млн рублей | База сравнения для выручки и дисконта | Не заменять выручкой или предложением |
| `placement_volume_bln` | `placement_volume / 1000` | млрд рублей | Докладное отображение объема размещения | Только display-поле |
| `revenue_volume` | сумма выручки от реализации | млн рублей | Денежный результат размещения | Зависит от наличия надежной source-колонки |
| `revenue_volume_bln` | `revenue_volume / 1000` | млрд рублей | Докладное отображение выручки | Только display-поле |
| `nominal_revenue_gap` | `placement_volume - revenue_volume` | млн рублей | Абсолютный разрыв между номиналом и выручкой | Интерпретация зависит от цен размещения и структуры выпусков |
| `nominal_revenue_gap_bln` | `nominal_revenue_gap / 1000` | млрд рублей | Докладное отображение разрыва | Только display-поле |
| `revenue_to_nominal_ratio` | `revenue_volume / placement_volume` | ratio | Доля номинального размещения, покрытая выручкой | Пусто при нулевом или отсутствующем размещении |
| `nominal_discount_ratio` | `nominal_revenue_gap / placement_volume` | ratio | Относительный дисконт выручки к номиналу | Не равен аукционному `discount_to_nominal = 100 - cutoff_price` |

## Таблицы

- `revenue_summary_<...>.csv/.xlsx`: периодный итог.
- `revenue_by_ofz_type_<...>.csv`: срез по видам ОФЗ.
- `revenue_by_maturity_<...>.csv`: срез по сроковым категориям.
- `revenue_by_format_<...>.csv`: срез по формату размещения.
- `revenue_monthly_<...>.csv`: помесячный срез внутри выбранного горизонта.

## Графики

- `revenue_vs_nominal_by_period_<...>.html`: номинальное размещение и выручка по периодам.
- `nominal_revenue_gap_by_period_<...>.html`: разница номинал минус выручка.
- `revenue_to_nominal_ratio_<...>.html`: отношение выручки к номиналу.
- `monthly_revenue_vs_nominal_<...>.html`: помесячное сравнение номинала и выручки.
- `monthly_nominal_revenue_gap_<...>.html`: помесячная разница номинал минус выручка.
- `revenue_gap_by_ofz_type_<...>.html`: разница по видам ОФЗ.
- `revenue_gap_by_maturity_<...>.html`: разница по срокам обращения.
- `discount_vs_revenue_gap_<...>.html`: связь относительного дисконта выручки и абсолютного разрыва.

## Ограничения

- `revenue_volume` не рассчитывается из `placement_volume`, `supply_volume` или `demand_volume`.
- Если выручка отсутствует полностью, revenue analytics документирует ограничение и не выдумывает данные.
- Если выручка заполнена частично, группы получают `data_quality_flag = revenue_partial`.
- `nominal_discount_ratio` является revenue-показателем и не заменяет ценовой дисконт по цене отсечения.
- Все `_bln`-поля используются для отчетного отображения; исходный расчетный масштаб остается в млн рублей.
## Связанные визуализации и KPI

Для графиков форматов используются следующие KPI:

| KPI | Использование в графиках | Единица | Ограничение |
| --- | --- | --- | --- |
| `placement_volume_bln` | `format_structure`, `format_terms_scatter`, bubble size, hover | млрд рублей | Отображает номинал, не выручку |
| `revenue_volume_bln` | `monthly_heatmap_revenue`, `format_nominal_revenue_gap`, `format_terms_comparison` | млрд рублей | Не рассчитывается синтетически при отсутствии источника |
| `nominal_revenue_gap_bln` | `format_nominal_revenue_gap`, `format_terms_comparison`, `format_terms_scatter` | млрд рублей | Зависит от полноты `revenue_volume` |
| `revenue_to_nominal_ratio` | `format_terms_comparison`, hover revenue-графиков | % или ratio | Пусто при нулевом или отсутствующем номинале |
| `weighted_avg_discount_to_nominal` | `format_discount`, `format_terms_comparison`, scatter по условиям | п.п. | Не подставляется, если отсутствует надежный дисконт |

`format_discount_*` использует средневзвешенный дисконт к номиналу, а не денежный разрыв. Денежный эффект дисконта показывается отдельным KPI `nominal_revenue_gap_bln`. Поэтому графики `format_discount_*` и `format_nominal_revenue_gap_*` дополняют друг друга и не являются взаимозаменяемыми.
