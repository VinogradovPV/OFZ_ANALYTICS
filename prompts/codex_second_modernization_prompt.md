# PROMPT ДЛЯ CODEX
## Вторая модернизация проекта OFZ_ANALITICS: QA-gate, visual regression, run manifest, revenue analytics и доработка графиков

Версия: modernization_v2.  
Контекст: предыдущая модернизация проекта уже дошла примерно до Этапа 15. Агрегация, `period_filter`, новая структура `outputs`, часть dashboard/semantic-layer и базовые графики уже реализованы. Сейчас задача — выполнить вторую модернизацию поверх текущей базы, не переписывая проект заново.

---

# 1. Роль агента

Ты — senior Python data engineer, BI/QA architect, аналитик рынка ОФЗ и инженер воспроизводимой аналитики.

Работай строго Python-first.  
Не изменяй `data/raw/`.  
Не используй абсолютные пути к Python.  
Все команды запуска должны быть из корня проекта:

```powershell
.\.venv\Scripts\python.exe
```

Не переписывай рабочие блоки с нуля. Любая доработка должна быть точечной, проверяемой и задокументированной.

---

# 2. Текущий статус проекта

Считать уже выполненными и не реализовывать повторно:

1. `--aggregation-mode cumulative|point`;
2. `period_filter`;
3. новая структура `outputs`;
4. базовые аналитические таблицы;
5. базовые графики;
6. dashboard exports / semantic layer, если уже созданы;
7. HTML QA / validation / regression infrastructure.

Можно и нужно:

- проверять контракт;
- исправлять найденные дефекты;
- расширять тесты;
- усиливать QA;
- добавлять revenue analytics;
- дорабатывать графики.

---

# 3. Цели второй модернизации

## 3.1. Единый quality gate

Создать единый воспроизводимый сценарий проверки проекта:

```text
scripts/quality_gate.py
```

Он должен запускать:

- `py_compile` ключевых Python-файлов;
- schema validation;
- regression tests;
- anomaly tests;
- smoke tests;
- HTML chart QA;
- visual regression / fallback HTML inspection;
- проверку структуры outputs;
- проверку README;
- проверку run manifest;
- проверку raw hash registry;
- проверку dashboard semantic model.

Результат:

```text
docs/quality_gate_report.md
outputs/reports/quality_gate_report_<run_id>.md
```

## 3.2. Visual regression для HTML-графиков

Добавить визуальную регрессию HTML-графиков через скриншоты и контрольные зоны.

Скрипт:

```text
scripts/visual_regression.py
```

Назначение:

- строить или открывать HTML-графики;
- делать скриншоты, если доступен backend;
- сравнивать контрольные области или базовые визуальные характеристики;
- проверять наличие ключевых элементов графиков:
  - заголовки;
  - оси;
  - легенды;
  - подписи;
  - hover/trace metadata, где возможно;
  - отсутствие технических шкал `5M/8M`;
  - наличие total labels на stacked-графиках;
  - отсутствие массового наложения подписей.

Если полноценный screenshot backend недоступен, скрипт должен выполнить fallback:

- статический анализ HTML;
- проверку Plotly JSON;
- поиск ключевых текстов;
- проверку числа `annotations`;
- проверку названий осей;
- проверку trace types.

Outputs:

```text
outputs/reports/visual_regression/
docs/visual_regression_report.md
```

## 3.3. Run manifest

Добавить run manifest:

```text
scripts/run_manifest.py
```

Manifest должен фиксировать:

- `run_id`;
- timestamp;
- параметры запуска:
  - `report_date`;
  - `period_type`;
  - `aggregation_mode`;
  - `retrospective_years`;
  - `stages`;
- версии / sha256 ключевых scripts;
- sha256 raw files;
- список сформированных outputs;
- размеры outputs;
- статус проверок;
- warnings;
- limitations.

Outputs:

```text
outputs/reports/run_manifest_<run_id>.json
outputs/reports/run_manifest_<run_id>.md
data/processed/run_manifest_latest.json
docs/run_manifest_report.md
```

## 3.4. Расширение anomaly tests

Расширить regression/anomaly tests:

- нулевое размещение;
- ДРПА;
- несостоявшийся аукцион;
- пропуски доходности;
- доходность, ошибочно превращенная в `0`;
- выбросы `bid_to_cover`;
- выбросы `demand_to_placement`;
- нулевое предложение;
- нулевой спрос;
- спрос есть, размещения нет;
- размещение есть, спрос отсутствует;
- цена отсечения отсутствует;
- дисконт к номиналу отсутствует;
- аномальная разница между номинальным размещением и выручкой.

Скрипт:

```text
scripts/anomaly_tests.py
```

Документация:

```text
docs/anomaly_tests_report.md
```

## 3.5. Dashboard semantic model v2

Расширить dashboard semantic model:

- версионированный словарь полей;
- KPI dictionary;
- русские названия;
- technical names;
- units;
- calculation rules;
- source columns;
- limitations;
- semantic version;
- compatibility notes.

Outputs:

```text
outputs/dashboards/semantic_model_v2/
outputs/dashboards/semantic_model_v2/field_dictionary.csv
outputs/dashboards/semantic_model_v2/kpi_dictionary.csv
outputs/dashboards/semantic_model_v2/measures.csv
outputs/dashboards/semantic_model_v2/model_manifest.json
docs/dashboard_semantic_model_v2.md
```

---

# 4. Доработка графиков по результатам визуального анализа

## 4.1. Monthly bid-cover / покрытие предложения спросом

Проблема:
На графике `monthly_bid_cover_month_cumulative_2026-05-01_retrospective_4.html` не хватает подписей данных.

Требования:

1. Добавить подписи значений на линиях.
2. Не перегружать график: подписи показывать для:
   - последней точки каждого года;
   - минимумов и максимумов;
   - точек пересечения/приближения к порогу 1;
   - отчетного года.
3. Горизонтальная линия `1` должна иметь подпись:
   - `Спрос = предложение`.
4. Ось Y должна называться:
   - `Спрос / предложение`.
5. Title:
   - `Помесячное покрытие предложения спросом`.
6. Hover:
   - год;
   - месяц;
   - спрос;
   - предложение;
   - `Спрос / предложение`;
   - накопленный режим / point mode;
   - период отчета.
7. В chart data export добавить:
   - `label_display`;
   - `label_reason`;
   - `threshold_distance`;
   - `is_threshold_crossing`.

## 4.2. Discount vs demand / дисконт к номиналу и спрос

Проблемы:

1. Все еще есть проблемы с подписями данных.
2. Размеры кругов визуально не дают понятного представления об объемах размещения.
3. Не очевидно, что именно означает размер точки.
4. На плотном scatter нельзя подписывать все выпуски.

Требования:

1. Использовать scatter policy:
   - не более `MAX_SCATTER_LABELS = 30`;
   - подписывать только выбросы, топы и target-period.
2. Bubble size:
   - явно указать в subtitle:
     `Размер точки = объем размещения по номиналу`.
3. Добавить легенду или аннотацию размера:
   - малый / средний / крупный объем;
   - или перейти на фиксированный размер точек, если bubble-size не читается.
4. Если bubble-size сохраняется:
   - использовать `sizeref`;
   - ограничить `sizemin` и `sizemax`;
   - добавить `bubble_size_value` в export.
5. Ось X:
   - если используется `demand_to_placement_ratio`, название:
     `Спрос / объем размещения`;
   - не называть это `bid-to-cover`.
6. Ось Y:
   - `Дисконт к номиналу, п.п.`
7. Hover:
   - выпуск;
   - дата;
   - период;
   - спрос;
   - предложение;
   - объем размещения по номиналу;
   - выручка от реализации;
   - дисконт к номиналу;
   - цена отсечения;
   - доходность;
   - label_reason;
   - data_quality_flag.
8. Добавить отдельные версии:
   - main clipped;
   - outliers;
   - log-X, если есть длинный хвост по X.
9. Добавить chart data export:
   - `discount_vs_demand_<...>.csv`.

## 4.3. Yield boxplot

Проблемы:

1. Для `yield_boxplot_by_ofz_type_month_cumulative_2026-05-01_retrospective_4.html` не хватает подписей максимальной и минимальной доходности.
2. Нужно сделать аналогичный график только по `ОФЗ-ПД`.
3. Для long/short modes сохранить корректную архитектуру:
   - short mode <= 3 периода;
   - long mode > 3 периода.

Требования:

1. Добавить подписи:
   - `мин`;
   - `мед`;
   - `макс`;
   - `n`.
2. Для long-mode не перегружать:
   - показывать min/max только если достаточно места;
   - иначе min/max в hover + export.
3. Для month cumulative retrospective 4:
   - если график читаем, min/max показывать рядом с усами соответствующего boxplot.
4. Создать отдельный график только по `ОФЗ-ПД`:
   ```text
   yield_boxplot_ofz_pd_<period_type>_<aggregation_mode>_<report_date>_retrospective_<N>.html
   ```
5. Для ОФЗ-ПД графика:
   - X = период;
   - Y = доходность;
   - color = период или единый цвет;
   - подписи min/median/max/n;
   - hover с полными статистиками.
6. Export:
   - `yield_boxplot_stats_<...>.csv`;
   - `yield_boxplot_ofz_pd_stats_<...>.csv`.

---

# 5. Revenue analytics / Выручка от реализации ОФЗ

Добавить полноценный слой аналитики по выручке от реализации ОФЗ.

## 5.1. Термины

- `placement_volume` — объем размещения по номиналу.
- `revenue_volume` — выручка от реализации ОФЗ.
- `nominal_revenue_gap` = `placement_volume - revenue_volume`.
- `revenue_to_nominal_ratio` = `revenue_volume / placement_volume`.
- `nominal_discount_amount` = `placement_volume - revenue_volume`.
- `nominal_discount_ratio` = `(placement_volume - revenue_volume) / placement_volume`.

Если в исходных данных выручка называется иначе, определить фактическую колонку и задокументировать mapping.

Если выручка отсутствует:
- не выдумывать;
- создать `data_quality_flag`;
- задокументировать ограничение.

## 5.2. Аналитические таблицы revenue

Создать таблицы:

```text
outputs/reports/analytical_tables/revenue_summary_<...>.xlsx
outputs/exports/analytical_csv/revenue_summary_<...>.csv
```

Минимальные колонки:

- `report_period_label`;
- `report_period_start`;
- `report_period_end`;
- `report_year`;
- `aggregation_mode`;
- `placement_volume`;
- `placement_volume_bln`;
- `revenue_volume`;
- `revenue_volume_bln`;
- `nominal_revenue_gap`;
- `nominal_revenue_gap_bln`;
- `revenue_to_nominal_ratio`;
- `nominal_discount_ratio`;
- `auction_count`;
- `data_quality_flag`.

Дополнительные срезы:
- по виду ОФЗ;
- по срокам;
- по формату;
- помесячно.

## 5.3. Графики revenue

Создать графики:

1. `revenue_vs_nominal_by_period_<...>.html`  
   Grouped bar:
   - объем размещения по номиналу;
   - выручка от реализации.

2. `nominal_revenue_gap_by_period_<...>.html`  
   Bar chart:
   - разница между номиналом и выручкой.

3. `revenue_to_nominal_ratio_<...>.html`  
   Line/bar:
   - выручка / номинал.

4. `monthly_revenue_vs_nominal_<...>.html`

5. `monthly_nominal_revenue_gap_<...>.html`

6. `revenue_gap_by_ofz_type_<...>.html`

7. `revenue_gap_by_maturity_<...>.html`

8. `discount_vs_revenue_gap_<...>.html`  
   Scatter:
   - X = дисконт к номиналу;
   - Y = разница номинал - выручка;
   - size = объем размещения по номиналу.

## 5.4. Единицы измерения revenue-графиков

Для объемных показателей:
- ось Y:
  - `млрд рублей`;
- для номинального размещения:
  - `Объем размещения по номиналу, млрд рублей`;
- для выручки:
  - `Выручка от реализации ОФЗ, млрд рублей`;
- для gap:
  - `Разница между номинальным размещением и выручкой, млрд рублей`.

## 5.5. Hover revenue-графиков

Hover должен показывать:
- период;
- объем размещения по номиналу;
- выручка;
- gap;
- ratio;
- вид ОФЗ / срок / формат, если применимо;
- data quality flag.

## 5.6. Документация revenue analytics

Создать:

```text
docs/revenue_analytics_report.md
docs/revenue_kpi_map.md
```

Обновить:
- `docs/kpi_map.md`;
- `docs/analytical_tables_report.md`;
- `docs/visualization_strategy.md`;
- `docs/final_project_summary.md`;
- `README.md`.

---

# 6. Интеграция

Нужно интегрировать новые блоки в:

- `run_pipeline.py`;
- `quality_gate.py`;
- `html_chart_qa.py`;
- `visual_regression.py`;
- dashboard semantic model;
- executive summary.

Не ломать существующие команды:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

---

# 7. Финальный результат

После второй модернизации проект должен сохранить результаты первой модернизации и дополнительно иметь:

1. Единый `quality_gate.py`.
2. Visual regression / fallback HTML inspection.
3. Run manifest.
4. Anomaly tests.
5. Semantic model v2.
6. Улучшенные monthly line charts с подписями.
7. Улучшенные dense scatter charts.
8. Исправленные yield boxplots.
9. Отдельный yield boxplot только по ОФЗ-ПД.
10. Новый revenue analytics layer.
11. Revenue charts.
12. Revenue KPI documentation.
13. Обновленный README и final docs.
