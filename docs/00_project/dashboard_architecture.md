# Архитектура dashboard

Дата формирования: `2026-05-19`.

Dashboard предназначен для параметризуемого управленческого анализа аукционов ОФЗ. Единый источник данных для интерактивного слоя:

```text
data/processed/ofz_auctions_report_scope.csv
```

Report scope должен формироваться после feature engineering через параметры `report_date`, `period_type` и `retrospective_years`. Dashboard не должен обращаться напрямую к `data/raw/`.

## Цель dashboard

Dashboard должен давать быстрый ответ на четыре управленческих вопроса:

- как изменились объемы размещения, спроса и предложения в отчетном периоде и ретроспективе;
- какие виды ОФЗ, форматы и сроки обращения формируют структуру размещения;
- насколько устойчив спрос и покрытие предложения спросом;
- где возникают риск-сигналы по доходности, спросу, дисконту, нулевому размещению и качеству данных.

## Обязательные фильтры

| Фильтр | Тип | Назначение | Источник |
|---|---|---|---|
| `report_date` | date picker | Выбор отчетной даты; дата должна быть первым числом месяца. | CLI / report params |
| `period_type` | selector | Переключение месячного, квартального или годового отчета. | CLI / report params |
| `retrospective_years` | numeric input | Количество сопоставимых ретроспективных периодов. | CLI / report params |
| `format` | multi-select | Фильтр по формату размещения: Аукцион, ДРПА и другие значения. | `format` |
| `ofz_type` | multi-select | Фильтр по виду ОФЗ. | `ofz_type` |
| `maturity_bucket` | multi-select | Фильтр по сроковой категории. | `maturity_bucket` |

Фильтры `report_date`, `period_type` и `retrospective_years` должны пересобирать report scope. Фильтры `format`, `ofz_type` и `maturity_bucket` применяются внутри уже сформированного scope.

## Layout

Рекомендуемая структура первого экрана:

1. Панель параметров отчета и фильтров.
2. Executive summary zone.
3. KPI layer.
4. Risk-monitoring zone.
5. Основные аналитические блоки с вкладками.
6. Analytical tables block.
7. Export zone.

Первый экран должен быть рабочим dashboard, а не landing page: фильтры, KPI и риск-сигналы должны быть видны сразу.

## Executive Summary Zone

| Элемент | Содержание |
|---|---|
| Цель | Сжато объяснить состояние размещений за отчетный период и ретроспективу. |
| Основные показатели | Объем размещения, совокупный спрос, совокупное предложение, спрос / предложение, спрос / размещение, средневзвешенная доходность, количество размещений. |
| Текстовые выводы | 3-5 кратких тезисов: что изменилось, где риск, какие сегменты доминируют. |
| Risk badges | Высокая доходность, слабый спрос, нулевое размещение, неполные данные, высокий дисконт. |
| Drill-down | Клик по тезису ведет к соответствующему блоку: спрос, доходность, сроки, формат или risk zone. |

## KPI Layer

KPI layer должен быть плотным и сканируемым. Карточки KPI не должны заменять графики, а должны давать быстрый вход в аналитику.

| KPI | Формула | Drill-down |
|---|---|---|
| Объем размещения | `sum(placement_volume)` | Структура размещений и сроки |
| Совокупный спрос | `sum(demand_volume)` | Demand analytics |
| Совокупное предложение | `sum(supply_volume)` | Supply analytics |
| Спрос / предложение | `sum(demand_volume) / sum(supply_volume)` | Demand/supply analytics |
| Спрос / размещение | `sum(demand_volume) / sum(placement_volume)` или строковый анализ на графиках риска | Risk-monitoring zone |
| Средневзвешенная доходность | weighted average by `placement_volume` | Yield analytics |
| Количество размещений | count rows after filters | Auction performance |
| Доля ДРПА | `placement_volume` ДРПА / общий `placement_volume` | Format analytics |

## Auction Performance Block

| Компонент | Назначение |
|---|---|
| Динамика количества размещений | Показать активность по периодам. |
| Объем размещения по периодам | Показать масштаб заимствований и YoY-изменения. |
| Рейтинг выпусков | Найти крупнейшие и наиболее эффективные размещения. |
| Таблица detail | `auction_date`, `issue_code`, `ofz_type`, `format`, `placement_volume`, `weighted_avg_yield`, `maturity_bucket`. |

Drill-down: период -> выпуск -> карточка выпуска с ценой отсечения, доходностью, спросом, предложением, размещением и сроком.

## Demand Analytics Block

| Компонент | Назначение |
|---|---|
| Совокупный спрос по периодам | Динамика емкости рынка. |
| Спрос по видам ОФЗ | Какие типы бумаг концентрируют спрос. |
| Спрос по срокам обращения | Где инвесторы готовы принимать duration. |
| Спрос / размещение | Показать превышение спроса над фактическим размещением. |

Методологическое правило: `demand_to_placement_ratio = demand_volume / placement_volume` не должен называться bid-to-cover.

## Supply Analytics Block

| Компонент | Назначение |
|---|---|
| Объем предложения по периодам | Оценка заявленного объема Минфина. |
| Предложение по видам ОФЗ | Структура размещаемых инструментов. |
| Предложение по срокам | Duration profile предложения. |
| Предложение vs размещение | Насколько предложение было реализовано рынком. |

Предложение должно использовать `supply_volume`, если поле доступно. Не заменять предложение объемом размещения.

## Demand/Supply Analytics Block

| Компонент | Назначение |
|---|---|
| Покрытие предложения спросом | `sum(demand_volume) / sum(supply_volume)` по периодам. |
| Demand-supply table | Обязательная таблица спроса и предложения. |
| Аномалии покрытия | Отдельные строки с высоким `bid_to_cover_ratio`. |
| Сравнение форматов | Аукцион и ДРПА показываются отдельно, если спрос применим. |

Для периодного bid-to-cover использовать агрегированный расчет, а не среднее строковых ratios.

## Yield Analytics Block

| Компонент | Назначение |
|---|---|
| Доходность по видам ОФЗ | Минимальная, средневзвешенная и максимальная доходность. |
| Boxplot доходности | Распределение доходности по `ofz_type` и периодам. |
| Динамика доходности | Сравнение отчетного периода и ретроспективы. |
| Доходность vs спрос | Риск-квадранты по спросу и стоимости размещения. |

Средневзвешенная доходность должна использовать `placement_volume` как вес. Если вес недоступен, dashboard должен показывать data quality warning.

## Format Analytics Block

| Компонент | Назначение |
|---|---|
| Доля форматов | Структура размещения по `format`. |
| ДРПА vs аукционы | Сравнение роли форматов в объеме размещения. |
| Формат и доходность | Проверка различий стоимости размещения по форматам. |
| Формат и сроки | Какие сроки чаще размещаются через разные форматы. |

Формат должен учитывать методологию: до 2024 года отсутствие столбца `Формат` трактуется как `Аукцион` с соответствующим флагом предположения.

## Maturity Structure Block

| Компонент | Назначение |
|---|---|
| Размещение по срокам | Обязательная таблица и stacked bar по `maturity_bucket`. |
| Доли сроковых категорий | `placement_volume_share` по периодам. |
| Sankey structure | Период -> вид бумаги -> срок -> формат. |
| Сроки и доходность | Проверка премии за duration. |

Классификация сроков:

- `short_term`: до 5 лет включительно;
- `medium_term`: свыше 5 и до 10 лет включительно;
- `long_term`: более 10 лет;
- `requires_review`: срок нельзя определить.

## Analytical Tables Block

Dashboard должен включать доступ к трем обязательным таблицам:

| Таблица | Файл | Назначение |
|---|---|---|
| Доходность по видам ОФЗ | `ofz_yield_by_type_<period_type>_<report_date>_retrospective_<N>.csv/.xlsx` | Доходность и объем размещения по `ofz_type`. |
| Спрос и предложение | `demand_supply_<period_type>_<report_date>_retrospective_<N>.csv/.xlsx` | Совокупный спрос, предложение и их ratio. |
| Размещение по срокам | `placement_volume_by_maturity_<period_type>_<report_date>_retrospective_<N>.csv/.xlsx` | Объем и доля размещений по сроковым категориям. |

Табличный блок должен поддерживать:

- просмотр markdown/table preview;
- сортировку;
- фильтрацию по тем же фильтрам dashboard;
- экспорт CSV/XLSX;
- показ `data_quality_flag`.

## Risk-Monitoring Zone

| Риск | Индикатор | Визуализация |
|---|---|---|
| Слабый спрос | `bid_to_cover_ratio < 1` или падение спроса | Покрытие предложения спросом |
| Дорогой спрос | высокий `demand_to_placement_ratio` и высокая доходность | Квадрант риска |
| Ценовое отсечение | высокий спрос к размещению и высокий дисконт | Отсечение спроса |
| Нулевое размещение | `placement_volume = 0` | Data quality / detail table |
| Неполные данные | `data_quality_flag`, missing yield/supply/demand | Data quality table |
| Концентрация | высокая доля одного выпуска, типа или срока | Concentration / Sankey |

Risk zone должна показывать только интерпретируемые сигналы. Если данные не позволяют рассчитать показатель, показывается ограничение, а не искусственное значение.

## Drill-Down Logic

| Уровень | Действие | Результат |
|---|---|---|
| Период | Клик по `report_period_label` | Фильтрация всех блоков до выбранного периода. |
| Вид ОФЗ | Клик по `ofz_type` | Переход к доходности, структуре и спросу по виду бумаги. |
| Срок | Клик по `maturity_bucket` | Показ выпусков выбранной сроковой категории. |
| Формат | Клик по `format` | Сравнение аукционов и ДРПА. |
| Выпуск | Клик по `issue_code` | Detail card выпуска. |
| Риск-сигнал | Клик по badge | Открытие строк, формирующих сигнал. |

Detail card выпуска должна содержать: `auction_date`, `issue_code`, `ofz_type`, `format`, `demand_volume`, `supply_volume`, `placement_volume`, `demand_to_placement_ratio`, `bid_to_cover_ratio`, `weighted_avg_yield`, `cutoff_price`, `discount_to_nominal`, `maturity_years`, `maturity_bucket`, `data_quality_flag`.

## Export Logic

| Export | Содержание |
|---|---|
| CSV | Текущая отфильтрованная таблица dashboard. |
| XLSX | Обязательные табличные отчеты и detail sheets. |
| HTML | Интерактивные графики из `outputs/charts/`. |
| PNG/SVG | Статичные версии ключевых графиков, если доступен backend экспорта. |
| Markdown | Executive summary и ограничения расчетов. |

Имена экспортов должны включать:

- `period_type`;
- `report_date`;
- `retrospective_years`;
- при необходимости имя блока или таблицы.

Пример:

```text
outputs/exports/dashboard_summary_quarter_2026-04-01_retrospective_2.xlsx
```

## Dashboard Exports Stage

Технический экспорт для dashboard/BI выполняется отдельным этапом `9.1`:

```text
scripts/07_dashboard_exports.py
```

Скрипт должен запускаться после формирования `data/processed/ofz_auctions_report_scope.csv`, построения графиков и обязательных аналитических таблиц. Результаты сохраняются в:

```text
outputs/dashboards/
```

Обязательные dashboard-ready datasets:

| Dataset | Назначение |
|---|---|
| `dashboard_auction_level_<...>.csv` | Детальный fact table уровня размещения/аукциона. |
| `dashboard_period_summary_<...>.csv` | Периодная сводка KPI и ratios. |
| `dashboard_kpi_summary_<...>.csv` | Long-format KPI для карточек dashboard. |
| `dashboard_maturity_structure_<...>.csv` | Структура размещения по срокам обращения. |
| `dashboard_yield_distribution_<...>.csv` | Распределение доходности по видам ОФЗ и периодам. |
| `dashboard_demand_supply_<...>.csv` | Спрос и предложение по периодам и форматам. |
| `dashboard_metadata_<...>.json` | Метаданные запуска, периоды и методология. |
| `dashboard_data_dictionary_<...>.csv` | Словарь данных для BI-слоя. |

Dashboard architecture является концептуальным слоем, а `scripts/07_dashboard_exports.py` - воспроизводимым техническим слоем передачи данных в dashboard/BI.

## Data Quality And Limitations

Dashboard должен явно показывать ограничения:

- report scope отсутствует: dashboard не строится, требуется выполнить этап 4;
- пустой отчетный период: показывается empty state и ссылка на `docs/period_selection_report.md`;
- отсутствует `placement_volume`: нельзя считать веса доходности и структуру размещения;
- отсутствует `supply_volume`: нельзя корректно считать bid-to-cover;
- отсутствует `cutoff_price`: ограничен анализ дисконта и отсечения спроса;
- `format_assumption_flag` не `explicit`: требуется аккуратная интерпретация формата;
- `maturity_bucket = requires_review`: сроковая аналитика ограничена.

## Зависимости от pipeline

| Dashboard слой | Минимальный этап pipeline |
|---|---|
| KPI и фильтры | Этап 4: report scope |
| KPI definitions | Этап 5: KPI map |
| Архитектура dashboard | Этап 9 |
| Графики | Этап 8 |
| Таблицы | Этап 8.1 |
| Executive summary | Этап 10 |

Перед публикацией dashboard должны быть доступны:

- `data/processed/ofz_auctions_report_scope.csv`;
- `docs/kpi_map.md`;
- `docs/visualization_strategy.md`;
- `docs/chart_build_limitations.md`;
- `docs/analytical_tables_report.md`;
- `docs/analytical_tables_limitations.md`.
