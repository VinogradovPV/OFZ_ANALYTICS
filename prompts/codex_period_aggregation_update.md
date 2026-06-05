# УТОЧНЕНИЕ К СИСТЕМНОМУ ПРОМПТУ CODEX
## Кумулятивная логика отчетных периодов, режимы агрегации и слой помесячной аналитики

Версия: расширенная. Добавлен слой помесячных показателей и обязательные помесячные визуализации.

---

# 1. Суть изменения

В проекте выявлена методологическая ошибка: при формировании месячного отчета по состоянию на `2026-05-01` показатели спроса и предложения были рассчитаны только за апрель 2026 года. Это неверно для режима накопительного отчета.

Для отчетной даты `2026-05-01` месячный отчет должен по умолчанию отражать накопленный итог с начала года:

```text
2026-01-01 — 2026-04-30
```

А ретроспектива должна сравниваться с аналогичными периодами прошлых лет:

```text
2022-01-01 — 2022-04-30
2023-01-01 — 2023-04-30
2024-01-01 — 2024-04-30
2025-01-01 — 2025-04-30
2026-01-01 — 2026-04-30
```

Аналогично квартальный отчет по состоянию на `2026-07-01` должен по умолчанию отражать накопленный итог с начала года по завершенный квартал:

```text
2026-01-01 — 2026-06-30
```

а не только II квартал.

---

# 2. Новый обязательный параметр: aggregation_mode

В проект нужно добавить параметр:

```text
--aggregation-mode cumulative|point
```

Где:

## cumulative

Накопленный итог с начала года до конца отчетного периода.

Это режим по умолчанию.

## point

Точечный отчет только за конкретный завершенный месяц, квартал или год.

---

# 3. Правила расчета периодов

## 3.1 Month + cumulative

Для `period_type = month` и `aggregation_mode = cumulative`:

`report_date` всегда является первым числом месяца.

Отчетный период:
- начало: `1 января отчетного года`;
- конец: последний день месяца, предшествующего `report_date`.

Пример:

```text
report_date = 2026-05-01
period_type = month
aggregation_mode = cumulative
```

Целевой период:

```text
2026-01-01 — 2026-04-30
```

Ретроспектива при `retrospective_years = 4`:

```text
2022-01-01 — 2022-04-30
2023-01-01 — 2023-04-30
2024-01-01 — 2024-04-30
2025-01-01 — 2025-04-30
2026-01-01 — 2026-04-30
```

Для файловых имен можно использовать:

```text
2026_m01_m04
```

---

## 3.2 Month + point

Для `period_type = month` и `aggregation_mode = point`:

Отчетный период:
- только месяц, предшествующий `report_date`.

Пример:

```text
report_date = 2026-05-01
period_type = month
aggregation_mode = point
```

Целевой период:

```text
2026-04-01 — 2026-04-30
```

Метка периода:

```text
2026-04
```

---

## 3.3 Quarter + cumulative

Для `period_type = quarter` и `aggregation_mode = cumulative`:

`report_date` должна быть:
- `01 января`;
- `01 апреля`;
- `01 июля`;
- `01 октября`.

Отчетный период:
- начало: `1 января отчетного года`;
- конец: последний день квартала, предшествующего `report_date`.

Пример:

```text
report_date = 2026-07-01
period_type = quarter
aggregation_mode = cumulative
```

Целевой период:

```text
2026-01-01 — 2026-06-30
```

Метка периода:

```text
2026-Q1-Q2
```

---

## 3.4 Quarter + point

Для `period_type = quarter` и `aggregation_mode = point`:

Отчетный период:
- только завершенный квартал, предшествующий `report_date`.

Пример:

```text
report_date = 2026-07-01
period_type = quarter
aggregation_mode = point
```

Целевой период:

```text
2026-04-01 — 2026-06-30
```

Метка периода:

```text
2026-Q2
```

---

## 3.5 Year

Для `period_type = year`:

`aggregation_mode = cumulative` и `aggregation_mode = point` фактически совпадают, если `report_date = 01 января`.

Пример:

```text
report_date = 2026-01-01
period_type = year
```

Целевой период:

```text
2025-01-01 — 2025-12-31
```

Метка периода:

```text
2025
```

---

# 4. Новый слой аналитики: monthly layer

Так как в проекте появляется корректная логика накопительных периодов, нужно отдельно сформировать слой помесячных показателей.

Назначение monthly layer:
- показывать внутрипериодную динамику;
- объяснять, из каких месяцев сформирован накопленный итог;
- отделять накопленный итог от точечного месячного значения;
- давать основу для помесячных графиков и dashboard.

Создать скрипт:

```text
scripts/09_monthly_analytics.py
```

Источник:

```text
data/processed/ofz_auctions_features.csv
```

или, если отчетные периоды уже сформированы:

```text
data/processed/ofz_auctions_report_scope.csv
```

но предпочтительно использовать features + периоды из `report_params.py`, чтобы monthly layer мог строить месячные ряды внутри выбранного горизонта.

Создать outputs:

```text
data/processed/ofz_monthly_metrics.csv
outputs/exports/monthly_metrics_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.csv
outputs/exports/monthly_metrics_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.xlsx
docs/monthly_analytics_report.md
docs/monthly_visualization_strategy.md
```

---

# 5. Структура monthly layer

`ofz_monthly_metrics.csv` должен содержать строки на уровне:

```text
report_year × month
```

или, если нужен больший детализационный слой:

```text
report_year × month × ofz_type × maturity_bucket × format
```

Минимальные колонки:

```text
report_year
month
month_number
month_label
month_start
month_end
report_period_label
aggregation_mode
is_target_year
auction_count
total_demand
total_supply
total_placement_volume
total_revenue_volume
bid_to_cover_ratio
demand_to_placement_ratio
demand_satisfaction_ratio
yield_weighted_avg
yield_min
yield_median
yield_max
placement_volume_auction
placement_volume_drpa
placement_volume_short_term
placement_volume_medium_term
placement_volume_long_term
ofz_pd_placement_volume
ofz_in_placement_volume
ofz_pk_placement_volume
data_quality_flag
```

Для cumulative-аналитики добавить накопительные поля:

```text
cumulative_demand
cumulative_supply
cumulative_placement_volume
cumulative_revenue_volume
cumulative_bid_to_cover_ratio
cumulative_weighted_avg_yield
cumulative_auction_count
```

Правила:
- месячные показатели считаются за конкретный календарный месяц;
- cumulative-поля считаются с января до текущего месяца включительно;
- для ретроспективы каждый год считается отдельно;
- месяцы после конца целевого отчетного периода не должны попадать в отчетный monthly layer.

---

# 6. Обязательные помесячные визуализации

Добавить блок помесячных визуализаций в `scripts/06_build_charts.py` или вынести в отдельный скрипт:

```text
scripts/10_build_monthly_charts.py
```

Рекомендуется отдельный скрипт, чтобы не превращать `06_build_charts.py` в бездонный шкаф с графиками.

## 6.1 Помесячный объем размещения

Файл:

```text
outputs/charts/monthly_placement_volume_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.html
```

Тип:
- grouped bar или line+markers.

Поля:
- X = месяц;
- Y = monthly total_placement_volume;
- color = report_year;
- optional line = cumulative_placement_volume.

Смысл:
показывает, какие месяцы дали основной вклад в накопленный итог.

## 6.2 Накопленный объем размещения с начала года

Файл:

```text
outputs/charts/monthly_cumulative_placement_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.html
```

Тип:
- line chart.

Поля:
- X = месяц;
- Y = cumulative_placement_volume;
- color = report_year.

Смысл:
сравнивает темп выполнения размещений в отчетном году с ретроспективой.

## 6.3 Помесячный спрос и предложение

Файл:

```text
outputs/charts/monthly_demand_supply_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.html
```

Тип:
- grouped bar или dual line.

Поля:
- X = месяц;
- Y = total_demand и total_supply;
- color/facet = report_year.

Смысл:
показывает, как соотносились рыночный спрос и предложение Минфина внутри года.

## 6.4 Помесячный bid-to-cover

Файл:

```text
outputs/charts/monthly_bid_to_cover_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.html
```

Тип:
- line chart.

Поля:
- X = месяц;
- Y = total_demand / total_supply;
- color = report_year.

Смысл:
выявляет месяцы с ухудшением или усилением покрытия предложения спросом.

Важно:
не путать с `demand_to_placement_ratio`.

## 6.5 Помесячная средневзвешенная доходность

Файл:

```text
outputs/charts/monthly_weighted_avg_yield_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.html
```

Тип:
- line chart или boxplot по месяцам.

Поля:
- X = месяц;
- Y = weighted average yield by placement volume;
- color = report_year.

Смысл:
показывает изменение стоимости заимствований внутри года.

## 6.6 Помесячная структура по форматам

Файл:

```text
outputs/charts/monthly_placement_by_format_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.html
```

Тип:
- stacked bar.

Поля:
- X = месяц;
- Y = placement_volume;
- color = format;
- facet или dropdown = report_year.

Смысл:
показывает, в какие месяцы использовались ДРПА и какой вклад они дали.

## 6.7 Помесячная структура по срокам обращения

Файл:

```text
outputs/charts/monthly_placement_by_maturity_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.html
```

Тип:
- stacked bar.

Поля:
- X = месяц;
- Y = placement_volume;
- color = maturity_bucket_label;
- facet/dropdown = report_year.

Смысл:
показывает, в какие месяцы размещались кратко-, средне- и долгосрочные бумаги.

## 6.8 Помесячный вклад месяцев в YoY-изменение

Файл:

```text
outputs/charts/monthly_yoy_contribution_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.html
```

Тип:
- waterfall или bar chart.

Поля:
- X = месяц;
- Y = monthly placement current year - same month previous year.

Смысл:
показывает, какие месяцы объясняют прирост или снижение накопленного объема размещения.

## 6.9 Heatmap месяц × год

Файл:

```text
outputs/charts/monthly_heatmap_placement_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.html
```

Тип:
- heatmap.

Поля:
- X = месяц;
- Y = report_year;
- color = total_placement_volume или bid_to_cover_ratio.

Смысл:
быстро выявляет сезонность, аномальные месяцы и структурные сдвиги.

---

# 7. Dashboard exports для monthly layer

Добавить:

```text
outputs/dashboards/dashboard_monthly_metrics_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.csv
outputs/dashboards/dashboard_monthly_data_dictionary_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.csv
```

Эти файлы должны быть BI-ready и содержать:
- monthly metrics;
- cumulative metrics;
- русские описания колонок;
- единицы измерения;
- ограничения.

---

# 8. Обратная совместимость

Если `--aggregation-mode` не передан, использовать:

```text
aggregation_mode = cumulative
```

Для точечного отчета пользователь должен явно указать:

```text
--aggregation-mode point
```

---

# 9. Изменения в ReportParams

`ReportParams` должен включать:

```python
aggregation_mode: str
```

Допустимые значения:

```text
cumulative
point
```

`parse_report_args()` должен читать:

```text
--aggregation-mode
```

с default:

```text
cumulative
```

---

# 10. Изменения в build_report_periods и get_period_bounds

Функции должны учитывать `aggregation_mode`.

`get_period_bounds(report_date, period_type, aggregation_mode, year_shift=0)` должен возвращать:
- `start_date`;
- `end_date`;
- `period_label`;
- `period_display_label`;
- `period_file_label`.

`build_report_periods(report_date, retrospective_years, period_type, aggregation_mode)` должен возвращать список периодов для целевого года и ретроспективных лет.

Количество периодов:

```text
retrospective_years + 1
```

Периоды должны быть упорядочены от старого к новому.

---

# 11. Изменения в period_filter.py

`period_filter.py` должен:
- принимать `--aggregation-mode`;
- использовать `ReportParams.aggregation_mode`;
- фильтровать строки по `auction_date >= period_start` и `auction_date <= period_end`;
- добавлять в `ofz_auctions_report_scope.csv` колонки:
  - `aggregation_mode`;
  - `report_period_start`;
  - `report_period_end`;
  - `report_period_label`;
  - `report_period_display_label`;
  - `report_period_file_label`;
  - `report_period_order`;
  - `is_target_period`.

---

# 12. Изменения в таблицах, графиках и dashboard exports

Все downstream-скрипты должны принимать и прокидывать:

```text
--aggregation-mode
```

Обновить:
- `scripts/06_build_charts.py`;
- `scripts/07_dashboard_exports.py`;
- `scripts/08_analytical_tables.py`;
- `scripts/09_monthly_analytics.py`;
- `scripts/10_build_monthly_charts.py`;
- `scripts/schema_validation.py`;
- `scripts/smoke_tests.py`;
- `scripts/generate_executive_summary.py`;
- `scripts/run_pipeline.py`.

Файловые имена outputs должны включать режим агрегации, чтобы не смешивать cumulative и point:

```text
demand_supply_month_cumulative_2026-05-01_retrospective_4.xlsx
monthly_metrics_month_cumulative_2026-05-01_retrospective_4.csv
monthly_placement_volume_month_cumulative_2026-05-01_retrospective_4.html
```

---

# 13. Изменения в аналитических таблицах

Таблица спроса и предложения должна рассчитывать показатели по выбранному периоду из `ofz_auctions_report_scope.csv`.

Для `month + cumulative + report_date=2026-05-01` строка `2026` должна включать январь–апрель 2026 года, а не только апрель.

Проверять:
- `total_demand = sum(demand_volume)` за весь период;
- `total_supply = sum(supply_volume)` за весь период;
- `bid_to_cover_ratio = total_demand / total_supply`;
- `total_demand_yoy_change` сравнивается с аналогичным накопленным периодом предыдущего года;
- `total_supply_yoy_change` сравнивается с аналогичным накопленным периодом предыдущего года.

---

# 14. Schema validation

`schema_validation.py` должен проверять:
- наличие `aggregation_mode`;
- допустимость значений `cumulative|point`;
- корректность `report_period_start` и `report_period_end`;
- для `month + cumulative` отчетный период начинается 1 января;
- для `quarter + cumulative` отчетный период начинается 1 января;
- для `point` отчетный период соответствует одному месяцу или одному кварталу;
- наличие и корректность `data/processed/ofz_monthly_metrics.csv`, если monthly layer уже сформирован.

---

# 15. Regression tests

Добавить regression tests:

1. `month + cumulative + report_date=2026-05-01`
   - период: `2026-01-01 — 2026-04-30`.

2. `month + point + report_date=2026-05-01`
   - период: `2026-04-01 — 2026-04-30`.

3. `quarter + cumulative + report_date=2026-07-01`
   - период: `2026-01-01 — 2026-06-30`.

4. `quarter + point + report_date=2026-07-01`
   - период: `2026-04-01 — 2026-06-30`.

5. `year + cumulative + report_date=2026-01-01`
   - период: `2025-01-01 — 2025-12-31`.

6. monthly layer:
   - для `month + cumulative + 2026-05-01` monthly layer содержит месяцы январь, февраль, март, апрель;
   - май и последующие месяцы не включены;
   - cumulative_placement_volume за апрель равен сумме monthly total_placement_volume за январь–апрель.

---

# 16. Документация

Обновить:
- `docs/kpi_map.md`;
- `docs/period_selection_report.md`;
- `docs/analytical_tables_report.md`;
- `docs/dashboard_exports_report.md`;
- `docs/schema_validation_report.md`;
- `docs/monthly_analytics_report.md`;
- `docs/monthly_visualization_strategy.md`;
- `docs/final_project_summary.md`;
- `docs/self_review.md`.

Документировать:
- что `cumulative` является режимом по умолчанию;
- как строятся месячные накопительные отчеты;
- как строятся квартальные накопительные отчеты;
- чем отличается `point`;
- что ретроспектива сравнивает аналогичные интервалы прошлых лет;
- какие помесячные показатели и визуализации создаются;
- что monthly layer объясняет состав накопительного итога.

---

# 17. Stop condition

Если невозможно определить дату аукциона или корректно построить период:
- остановиться;
- не строить таблицы и графики молча;
- сообщить пользователю, какие поля отсутствуют или некорректны.
