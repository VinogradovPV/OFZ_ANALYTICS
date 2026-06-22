# Журнал ручных проверок

## 2026-06-22 - Новый Python desktop GUI launcher

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-22 | PowerShell/WinForms launcher заменен Python tkinter GUI с девятью вкладками, allowlist runner, Minfin stage 0, typed confirms, live journal и thin wrapper. | `py_compile`; 29-action contract smoke; widget smoke; command runner streaming/parallel-block smoke; editable install; CLI/wrapper help; `compileall`; `pip check`; Minfin offline dry-run; encoding scanner; `quality-fast`. | Все automated GUI checks и quality-fast прошли. Gate приведен в соответствие с generated outputs policy: source-карта остается в docs, `outputs/charts/index.md` не требуется. | Dangerous mutations и live Minfin download не выполнялись; desktop layout требует финального ручного просмотра оператором. Visual regression в managed sandbox использует fallback. |

## 2026-06-22 - UTF-8 / Mojibake quality gate

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-22 | Добавлен строгий UTF-8/mojibake scanner, stage `encoding-mojibake`, интеграция в quality-fast/full и GitHub Actions; исправлены найденные старые фрагменты mojibake. | `py_compile`; первичный и контрольный encoding audit; отдельный `ofz-quality --stage encoding-mojibake`; `compileall`; pipeline; schema; quality-fast; `git diff --check`. | Первичный аудит: 238 файлов, invalid UTF-8 `0`, mojibake-файлов `9`. После remediation: 240 файлов, invalid UTF-8 `0`, mojibake `0`, manual review `0`. Encoding stage OK, pipeline OK, schema 16/16. | Generated/cache/raw Excel исключены из scanner scope. Общий quality-fast имеет один внешний FAIL из-за ранее удаленного `outputs/charts/index.md`; все encoding и расчетные проверки прошли. CI проверяется после push. |

## 2026-06-22 - Регрессия базовых yield metrics ОФЗ-ПД

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-22 | Базовые yield metrics переведены на cohort ОФЗ-ПД; ОФЗ-ПК/ОФЗ-ИН исключены из yield, но сохранены в volume breakdown. | Targeted regression; `compileall`; полный `ofz-run`; `ofz-schema`; `ofz-quality --fast`; HTML QA; visual regression auto; ручная проверка regenerated CSV/HTML за ноябрь 2025. | Ноябрь 2025: weighted `14.873469`, min `14.73`, median `14.75`, max `14.95`; ОФЗ-ПК `1 691 219.3 млн руб.` не влияет на yield. Schema 16/16, regression 15/15, HTML QA OK, visual fallback OK. | `quality-fast` имеет один внешний FAIL: ранее удален `outputs/charts/index.md`. Screenshot backend недоступен в managed sandbox; требуется ручная проверка outside sandbox. |

## 2026-06-17 - Повторная русификация и UTF-8 аудит документации

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-17 | Повторно проверена активная Markdown-документация без архивов; часть английских заголовков и служебных формулировок переведена на русский; документы сохранены как UTF-8. | Python UTF-8 audit для `README.md` и `docs/**/*.md` без `docs/archive/` и `docs/90_archive/`; `rg -n "\?{2,}" README.md docs --glob "*.md" --glob "!docs/90_archive/**" --glob "!docs/archive/**"`; Python mojibake pattern scan. | UTF-8 без BOM подтвержден; поврежденные последовательности вопросительных знаков и контрольные mojibake-паттерны не найдены; архивы не изменялись. | Проверки Python/quality не запускались, потому что менялась только документация. Технические термины, CLI-ключи, пути, поля и stage-названия сохранены как стабильные идентификаторы. |

## 2026-06-03 - format_terms QA contracts

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-03 | Расширены QA и visual regression контракты для `format_terms_aggregate_scatter_*`, `format_terms_scatter_*` и `format_terms_delta_by_format_*`. Detailed scatter получил точное название Y-метрики и source-поля доходности в CSV. | `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py scripts\html_chart_qa.py scripts\visual_regression.py`; `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | HTML QA и visual regression fallback проходят; aggregate scatter проверяется как `период × формат`, detailed scatter - как `color=format`, `symbol=ofz_type`, delta chart - как смысловая оценка дельты. | Screenshot backend не настроен; visual regression выполнен через fallback HTML / Plotly JSON inspection. |

## 2026-06-03 - format_terms_delta_by_format semantic color

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-03 | Цветовая логика `format_terms_delta_by_format_*` переведена с математического знака `ДРПА выше/ниже` на аналитическую оценку `ДРПА хуже/лучше/различие малозначимо`. Добавлены `metric_preference_direction`, `assessment_threshold`, `drpa_condition_assessment`, компактный hover и очищенные facet-заголовки. | `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py scripts\html_chart_qa.py scripts\visual_regression.py`; `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | HTML QA и visual regression fallback проходят; проверено, что отрицательная дельта `выручка / номинал` и положительная дельта дисконта оцениваются как `ДРПА хуже`. | Абсолютная метрика `номинал − выручка` зависит от объема размещения; для относительного сравнения использовать `выручка / номинал`. |

## 2026-06-03 - format_terms_delta_by_format

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-03 | Добавлен diverging small multiples `format_terms_delta_by_format_*`: дельты `ДРПА минус Аукцион` по доходности, дисконту, выручке / номиналу и разнице номинал-выручка. | `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py scripts\html_chart_qa.py`; `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | HTML и CSV созданы; `format_terms_delta_by_format_contract` проходит; CSV содержит рассчитанные дельты только для периодов с двумя форматами. | Дельта не рассчитывается для периодов без одного из форматов; такие строки не рисуются как нули и остаются только в export с `delta_available=False`. |

## 2026-06-02 - format_terms_comparison: уточнение доходности

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-02 | Уточнена панель доходности `format_terms_comparison_*`: название заменено на `Средневзвешенная доходность размещения, % годовых`, удалены технические facet-префиксы и общий Y-title `Значение`, в hover и CSV добавлены `source_column`, `aggregation_method`, `weight_field`. | `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py scripts\html_chart_qa.py scripts\visual_regression.py`; `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-01-01 --retrospective-years 4 --period-type year --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-01-01 --retrospective-years 4 --period-type year --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-01-01 --retrospective-years 4 --period-type year --aggregation-mode cumulative`. | `format_terms_comparison_contract` проходит в HTML QA и visual regression; CSV содержит `weighted_avg_yield`, `weighted_average_by_placement_volume`, `placement_volume` для панели доходности. | Общие HTML QA и visual regression для годового набора все еще фиксируют отдельный старый дефект `monthly_heatmap_placement_year_*`: отсутствует справочная колонка `Итого`; это не связано с `format_terms_comparison`. |

## 2026-06-02 - format_terms_comparison placement_count

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-02 | В `format_terms_comparison_*` добавлены `placement_count`, подписи `n=...`, hover с количеством размещений формата и CSV-строки `format_available=False` для отсутствующих форматов. | `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py scripts\html_chart_qa.py scripts\visual_regression.py`; `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-01-01 --retrospective-years 4 --period-type year --aggregation-mode cumulative`; HTML QA и visual regression fallback. | `format_terms_comparison_contract` прошел в HTML QA и visual regression; CSV содержит `placement_count`, `label_count_display`, `format_available`. | Общий QA по годовому набору все еще падает на старом `monthly_heatmap_placement_year_*`, где отсутствует справочная колонка `Итого`; это отдельный дефект, не связанный с `format_terms_comparison`. |

Дата обновления: `2026-05-25`.

Формат журнала: дата, изменение, проверка, результат и ограничения. Команды выполняются из корня проекта через `.\.venv\Scripts\python.exe`.

## Проверки

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-05-25 | Добавлен `scripts/generate_executive_summary.py`. | `.\.venv\Scripts\python.exe -m py_compile scripts\generate_executive_summary.py`; `.\.venv\Scripts\python.exe scripts\generate_executive_summary.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Ожидается создание `outputs/reports/executive_summary_month_cumulative_2026-05-01_retrospective_4.md` и `docs/executive_summary_report.md`. | Summary не делает выводы без рассчитанных источников; отсутствующие sources фиксируются как ограничения. |
| 2026-05-25 | Обновлен `README.md`. | Ручная проверка текста и команд запуска. | Все команды должны использовать `.\.venv\Scripts\python.exe`; абсолютные пути к Python отсутствуют. | README не подтверждает runtime-работоспособность расчетов. |
| 2026-05-25 | Исправлен long-mode `yield_boxplot_by_ofz_type`. | `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py`; `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-01-01 --retrospective-years 5 --period-type year --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py`. | Ожидается, что периоды `2020`-`2025` отображаются отдельными X-категориями внутри панелей видов ОФЗ. | Старые HTML-файлы остаются неизменными до пересборки графиков. |
| 2026-05-25 | Доработаны stacked structure charts. | `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py`; `.\.venv\Scripts\python.exe -m py_compile scripts\10_build_monthly_charts.py`; пересборка графиков; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py`. | Ожидается наличие totals над stacked-столбцами и корректной оси `Объем размещения по номиналу, млрд рублей`. | Малые сегменты могут не иметь внутренних подписей, но доступны через hover. |
| 2026-05-25 | Обновлен `scripts/html_chart_qa.py`. | `.\.venv\Scripts\python.exe -m py_compile scripts\html_chart_qa.py`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | QA должен проверять HTML текущего отчетного набора и не падать на стандартных отчетных аргументах. | Проверка статическая; итоговый вид графиков требует ручного просмотра HTML. |

## Детальная ручная проверка boxplot доходности

Проверяемый дефект: `yield_boxplot_by_ofz_type_year_cumulative_2026-01-01_retrospective_5.html`.

Проверить после пересборки:

1. В длинной ретроспективе видны отдельные X-категории `2020`, `2021`, `2022`, `2023`, `2024`, `2025`.
2. В каждой панели вида ОФЗ boxplot строится отдельно по каждому периоду.
3. Точки размещений находятся около своего периода, а не в одной вертикальной линии.
4. Подписи `мед` и `n` привязаны к соответствующему boxplot.
5. Ось Y подписана `Доходность, % годовых`.

Команды:

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py
.\.venv\Scripts\python.exe -m py_compile scripts\html_chart_qa.py
.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-01-01 --retrospective-years 5 --period-type year --aggregation-mode cumulative
.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-01-01 --retrospective-years 5 --period-type year --aggregation-mode cumulative
```

## Детальная ручная проверка stacked structure charts

Проверить после пересборки:

1. В `maturity_structure` и `format_structure` над stacked-столбцами с двумя и более сегментами есть итоговая сумма.
2. В monthly stacked charts totals отображаются по каждому месяцу и году.
3. Ось Y: `Объем размещения по номиналу, млрд рублей`.
4. Hover содержит значение сегмента, долю в столбце, итог столбца и долю в общей сумме.
5. В сроковой структуре цвета различимы: долгосрочные - пурпурный, среднесрочные - бирюзовый, краткосрочные - терракотовый, требует проверки - серый.

Команды:

```powershell
.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\python.exe scripts\10_build_monthly_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```
| 2026-05-27 | Исправлены подписи `monthly_placement_volume`. | `.\.venv\Scripts\python.exe -m py_compile scripts\10_build_monthly_charts.py`; `.\.venv\Scripts\python.exe -m py_compile scripts\html_chart_qa.py`; `.\.venv\Scripts\python.exe scripts\10_build_monthly_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Ожидается, что `label_display` соответствует `placement_volume_bln`, hover и подписи используют одну метрику, а нулевые месяцы не подписываются. | Старые HTML до пересборки могут содержать прежние подписи. |

| 2026-05-27 | Доработано семейство `yield_vs_discount`: цвет по году, facet-оси без дублей, человекочитаемый hover. | `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py`; `.\.venv\Scripts\python.exe -m py_compile scripts\html_chart_qa.py`; `.\.venv\Scripts\python.exe -m py_compile scripts\visual_regression.py`; `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Ожидается: main/outliers окрашены по `report_year`, legend title = `Год`, facet имеет общие X/Y подписи и человекочитаемые панели. | Старые HTML до пересборки могут сохранять прежнюю группировку по срокам обращения. |
| 2026-05-28 | Дополнительно закреплен порядок facet-панелей `yield_vs_discount` и убрано размножение подписей медианных линий в facet. | `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py`; `.\.venv\Scripts\python.exe -m py_compile scripts\html_chart_qa.py`; `.\.venv\Scripts\python.exe -m py_compile scripts\visual_regression.py`; `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | В текущей сессии автоматический запуск заблокирован: `.venv` ссылается на отсутствующий `Python314`. | Проверить вручную после восстановления локального виртуального окружения. |
| 2026-05-28 | Исправлен QA-fail `yield_vs_discount_contract`: facet-заголовки больше не должны содержать `Период=`, а медианные линии не должны выводить подписи `None`. | `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Ожидается: `yield_vs_discount_facet_*.html` проходит проверку facet-осей и заголовков панелей. | Старый HTML продолжит падать до пересборки графиков. |
| 2026-05-28 | Исправлена видимость подписей facet-графика `yield_vs_discount`: общие подписи X/Y возвращены в видимую область, подписи медианных линий вынесены под заголовок. | `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; визуально открыть `outputs/charts/scatter/yield_discount/yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html`. | Ожидается: видны подписи `Дисконт к номиналу, п.п.`, `Доходность, % годовых`, а также пояснения к общей медиане дисконта и доходности. | Старый HTML нужно пересобрать. |
| 2026-05-28 | Подписи медианных линий `yield_vs_discount_facet` перенесены с верхней области графика непосредственно к линиям медианы. | `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; визуально открыть `outputs/charts/scatter/yield_discount/yield_vs_discount_facet_month_cumulative_2026-05-01_retrospective_4.html`. | Ожидается: подпись `Общая медиана дисконта` находится рядом с вертикальной линией, `Общая медиана доходности` — рядом с горизонтальной линией. | Старый HTML нужно пересобрать. |
| 2026-05-28 | Для `yield_vs_discount_facet` введена отдельная политика подписей и периодные медианы. | `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Ожидается: не более 3 подписей на панель и 15 на график; подзаголовок сообщает, что пунктирные линии — медианы периода; CSV содержит `label_visible`, `median_scope`, `is_incomplete_period`. | Для 2022 в текущем наборе пригодных строк доступны только январь-февраль. |
| 2026-06-01 | Для всего семейства `yield_vs_discount` введена единая label policy с приоритетами `data_quality_flag → top_yield → top_discount → top_placement → outlier → target_period` и дистанцией между подписями. | `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; проверить CSV `yield_vs_discount*.csv`. | Ожидается: main <= 25 видимых подписей, outliers <= 30, facet <= 15 и <= 3 на панель; скрытые кандидаты сохраняют `label_display` и `label_reason`, но имеют `label_visible=False`. | Старые HTML/CSV нужно пересобрать. |
| 2026-05-28 | Уточнен CSV-контракт семейства `yield_vs_discount`: обязательные поля `label_visible`, `median_discount`, `median_yield`, `median_scope`, `is_incomplete_period` добавляются во все exports. | `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; открыть CSV в `outputs/exports/chart_data/scatter/`. | Ожидается: `label_visible` boolean во всех трех CSV `yield_vs_discount*`; main/outliers имеют `median_scope=global`, facet имеет `median_scope=period`. | Старые CSV нужно пересобрать. |
| 2026-06-01 | Подписи медианных линий `yield_vs_discount` разделены по осям: `мед. дисконт` для вертикальной линии и `мед. доходность` для горизонтальной линии; в facet текст с линий убран, методология оставлена в subtitle. | `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; визуально открыть три графика `yield_vs_discount*`. | Ожидается: main/outliers не используют одинаковую подпись `Общая медиана`; facet показывает пунктирные медианы периода без текстового конфликта в панелях. | Старые HTML/CSV нужно пересобрать. |
| 2026-06-01 | Для `yield_vs_discount` добавлено пояснение размера точки: объем размещения по номиналу и ориентиры `50 / 250 / 500 млрд руб.`. | `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; визуально открыть `outputs/charts/scatter/yield_discount/yield_vs_discount*_month_cumulative_2026-05-01_retrospective_4.html`. | Ожидается: subtitle содержит `Размер точки — объем размещения по номиналу`, аннотация размера содержит ориентиры, hover содержит точный объем в млрд рублей. | Старые HTML нужно пересобрать. |
| 2026-06-01 | Основной `yield_vs_discount` приведен к контракту: цвет = год, размер = `placement_volume_bln`, подписи только при `label_visible=True`, лимит <= 25. | `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; проверить `yield_vs_discount_month_cumulative_2026-05-01_retrospective_4.csv`. | Ожидается: `median_scope=global`, видимых подписей не больше 25, легенда `Год`, оси `Дисконт к номиналу, п.п.` и `Доходность, % годовых`. | Старые HTML/CSV нужно пересобрать. |
| 2026-06-01 | `yield_vs_discount_outliers` получил аналитический subtitle вместо технического `scatter label policy`: отбор объяснен через экстремальные значения дисконта, доходности или объема размещения. | `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; открыть `outputs/charts/scatter/yield_discount/yield_vs_discount_outliers_month_cumulative_2026-05-01_retrospective_4.html`. | Ожидается: title `Квадрант риска: дисконт к номиналу и доходность — выбросы`, легенда `Год`, сроковая категория в hover, видимых подписей <= 30. | Старые HTML/CSV нужно пересобрать. |
| 2026-06-01 | Для `yield_vs_discount_facet` уточнен флаг неполного периода: `incomplete_period_reason` теперь человекочитаемый, например `доступны данные только за янв–фев`. | `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; проверить `yield_vs_discount_facet_*.csv`. | Ожидается: для панели 2022 `is_incomplete_period=True`, причина `доступны данные только за янв–фев`; лимиты подписей 3 на панель и 15 всего соблюдены. | Старые CSV нужно пересобрать. |
| 2026-06-01 | Hover семейства `yield_vs_discount` приведен к русскому аналитическому виду: технические причины и флаги переводятся в `высокая доходность`, `высокий дисконт`, `крупное размещение`, `нет данных о спросе`, `требуется проверка спроса`. | `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `Select-String -Path outputs\charts\scatter\yield_discount\yield_vs_discount*_month_cumulative_2026-05-01_retrospective_4.html -Pattern "top_y_value|top_discount|missing_demand\|source_markers"`. | Ожидается: в hover HTML нет сырых технических токенов; русские display-формулировки присутствуют. | Старые HTML нужно пересобрать. |
| 2026-06-01 | HTML QA расширен для `yield_vs_discount`: проверяются CSV-поля `label_visible` и `median_scope`, boolean-значения `label_visible`, лимиты видимых подписей, `color=report_year`, легенда `Год`, пояснение размера точки и медианных линий. | `.\.venv\Scripts\python.exe -m py_compile scripts\html_chart_qa.py`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Пройдено: `yield_vs_discount_contract` проверил 3 файла текущего набора без FAIL. | Проверка CSV ограничивается тем отчетным набором, который выбран аргументами QA; stale exports других параметров проверяются при запуске QA для соответствующего набора. |
| 2026-06-01 | Visual regression fallback расширен для `yield_vs_discount`: проверяет количество подписей на facet/main/outliers, скопление подписей в одной панели, subtitle про медианы и размер точки, legend title `Год`; поиск HTML стал рекурсивным по новой структуре `outputs/charts/`. | `.\.venv\Scripts\python.exe -m py_compile scripts\visual_regression.py`; `.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Пройдено: fallback inspection нашел 43 HTML, контракты `yield_vs_discount` подтверждены для 3 файлов. | В консольном выводе Windows символы вне cp1251 заменяются безопасно; Markdown-отчет сохраняется в UTF-8. |
| 2026-06-01 | Документация `yield_vs_discount` обновлена: назначение main/facet/outliers, `label_visible`, медианные линии, размер точки, outliers и неполные периоды описаны в README и docs. | Проверить разделы `docs/04_visualization/visualization_strategy.md`, `docs/04_visualization/chart_build_limitations.md`, `docs/04_visualization/chart_improvement_diagnostics.md`, `README.md`. | Ожидается: методология семейства графиков описана без противоречий с CSV-контрактом и QA. | Документация описывает текущий контракт; старые HTML/CSV других параметров требуют пересборки для полного соответствия. |
| 2026-06-01 | HTML QA расширен для доработанных monthly/facet/scatter-графиков: `monthly_demand_supply`, `monthly_cumulative_placement`, facet Y-title policy, `demand_cutoff_explanation` и обязательный `yield_vs_discount`. | `.\.venv\Scripts\python.exe -m py_compile scripts\html_chart_qa.py`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Ожидается: QA проверяет подписи данных, оси, hover, bubble-size policy, лимиты подписей и наличие chart data exports. | Автоматический запуск в текущей сессии не выполнен из-за ограничения среды; команды нужно выполнить вручную. |
| 2026-06-01 | Visual regression расширен для `monthly_demand_supply`, `monthly_cumulative_placement`, facet Y-title policy, `demand_cutoff_explanation` и обязательного `yield_vs_discount` с reference lines. | `.\.venv\Scripts\python.exe -m py_compile scripts\visual_regression.py`; `.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Ожидается: fallback inspection проверяет подписи данных, отсутствие дублей Y-title, bubble-size explanation и наличие `yield_vs_discount`. | Автоматический запуск в текущей сессии заблокирован sandbox `spawn setup refresh`; команды нужно выполнить вручную. |
| 2026-06-01 | Обновлена документация по доработкам графиков: monthly labels, единый Y-title для facet, bubble-size/fixed-size fallback, `yield_vs_discount` и его ограничения. | Проверить `docs/04_visualization/*.md`, `docs/06_quality/visual_regression_report.md`, `docs/00_project/final_project_summary.md`, `README.md`. | Ожидается: правила визуализации и QA описаны согласованно с текущими скриптами. | Документация не заменяет ручной просмотр HTML после пересборки графиков. |
## 2026-06-01 - format_discount composite stabilization

- Изменение: `format_discount_*` перестроен как stacked bar по форматам, где высота сегмента равна номинальному объему размещения, а дисконт выводится подписью сегмента.
- Проверка: пересборка `scripts/06_build_charts.py` для `2026-05-01`, `month`, `cumulative`, `retrospective_years=4`.
- Проверка: `py_compile` для `scripts/06_build_charts.py`, `scripts/html_chart_qa.py`, `scripts/visual_regression.py`.
- Проверка: `scripts/html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`.
- Результат: `format_discount_contract` прошел; CSV содержит `segment_label_visible`, `discount_label_visible`, `total_label_display`, `data_quality_display`.
- Ограничение: финальное визуальное расстояние между верхним сегментом и total label желательно контролировать вручную при очень малой доле ДРПА.
## 2026-06-02 - format_discount mini-indicator stabilization

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-02 | Доработан `format_discount_*`: добавлены координаты сегментов, annotation mini-indicator дисконта и `total_label_y`; подпись ДРПА привязана к собственному сегменту. | `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py scripts\html_chart_qa.py scripts\visual_regression.py`; `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Пройдено: `format_discount_contract` подтвержден HTML QA и visual regression fallback; CSV содержит `segment_base_y`, `segment_top_y`, `segment_mid_y`, `discount_bar_norm`, `total_label_y`. | Мини-индикатор дисконта является относительной визуальной подсказкой внутри текущего графика; точные значения следует читать в hover и CSV. |
## 2026-06-02 - format_discount component decomposition

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-02 | `format_discount_*` перестроен как разложение номинала на `revenue` и `discount_gap` внутри каждого форматного сегмента. | `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py scripts\html_chart_qa.py scripts\visual_regression.py`; пересборка month/year; HTML QA month/year; visual regression fallback для month. | CSV export содержит `component_type`, `nominal_volume_bln`, `revenue_volume_bln`, `discount_gap_bln`, `component_volume_bln`; проверка `revenue + discount_gap = nominal` прошла. | Визуальная читаемость очень малых дисконтных разрывов остается предметом ручной проверки; точные значения доступны в hover и CSV. |
# 2026-06-02 - format_nominal_revenue_gap

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-02 | Добавлен `format_nominal_revenue_gap`: grouped bar денежной разницы номинала и выручки по форматам размещения. | `.\.venv\Scripts\python.exe -m py_compile scripts\config.py scripts\12_build_revenue_charts.py scripts\html_chart_qa.py`; запуск `scripts\12_build_revenue_charts.py` для month/year; HTML QA для month/year. | График создан в `outputs/charts/revenue/gap/`, CSV export создан в `outputs/exports/chart_data/revenue/`, `revenue_charts_contract` проверяет 9 revenue-графиков. | График опирается на готовую таблицу `revenue_by_format`; при отсутствии выручки значения не выдумываются и должны быть отмечены через `data_quality_flag`. |
# 2026-06-02 - monthly_heatmap_placement total column

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-02 | В `monthly_heatmap_placement_*` добавлена колонка `Итого`, равная сумме месяцев выбранного отчетного горизонта по каждому году. | `.\.venv\Scripts\python.exe -m py_compile scripts\10_build_monthly_charts.py scripts\html_chart_qa.py`; `.\.venv\Scripts\python.exe scripts\10_build_monthly_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | QA `monthly_heatmap_placement_contract` прошел; CSV содержит `is_total_column=True`, `total_placement_volume_bln`, `label_display`, сумма месяцев равна итогу. | Итоговая колонка использует общую шкалу цвета, поэтому при больших итогах месячные ячейки могут быть менее контрастными. |

# 2026-06-02 - monthly heatmap neutral total column

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-02 | `monthly_heatmap_placement_*` total column was moved out of the main color scale and rendered as a neutral informational overlay. | `.\.venv\Scripts\python.exe -m py_compile scripts\10_build_monthly_charts.py scripts\html_chart_qa.py scripts\visual_regression.py`; `.\.venv\Scripts\python.exe scripts\10_build_monthly_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Passed: py_compile, monthly rebuild, HTML QA and fallback visual regression. CSV has `color_scale_included=True` for monthly cells and `False` for `Итого`. | `monthly_heatmap_revenue_*` was not found in the current generated chart set; the same contract is documented for future analogous heatmaps. |
## 2026-06-02 - format_terms_scatter

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-02 | Добавлен scatter-график `format_terms_scatter_*`: X = дисконт к номиналу, Y = доходность, цвет = формат размещения, размер точки = объем размещения по номиналу. | `.\.venv\Scripts\python.exe -m py_compile scripts\config.py scripts\06_build_charts.py scripts\html_chart_qa.py`; `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-01-01 --retrospective-years 4 --period-type year --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-01-01 --retrospective-years 4 --period-type year --aggregation-mode cumulative`. | HTML и CSV созданы; `format_terms_scatter_contract` в HTML QA проходит; в CSV 25 видимых подписей при лимите 25. | Общий HTML QA годового набора все еще фиксирует отдельный старый дефект `monthly_heatmap_placement_year_*`: отсутствует справочная колонка `Итого`; это не связано с `format_terms_scatter`. |
## 2026-06-04 - documentation update for format/revenue/discount charts

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-04 | Документация обновлена для `format_structure`, `format_discount`, `format_nominal_revenue_gap`, `monthly_heatmap_revenue`, `format_terms_comparison` и `format_terms_scatter`. | Проверить актуальные разделы в `docs/04_visualization/`, `docs/03_analytics/revenue_analytics_report.md`, `docs/01_methodology/revenue_kpi_map.md`, `docs/00_project/final_project_summary.md` и `README.md`. | Зафиксированы правила подписей сегментов, total labels, ограничения по отсутствующим discount/revenue data и назначение новых графиков по форматам. | Документация описывает текущий контракт; старые HTML/CSV других параметров требуют пересборки, чтобы полностью соответствовать новым правилам. |

## 2026-06-04 - production blocker volume_bln_units

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-04 | Fixed `schema_validation / volume_bln_units` blocker by adding unit fields in `format_discount_*` and `format_terms_aggregate_scatter_*` chart data generators. | `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py`; `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Passed: schema validation reports `volume_bln_units | ok`; quality gate fast completed successfully. | Existing chart data exports for other parameter combinations should be rebuilt when they enter the production validation scope. |

## 2026-06-04 - production artifact policy

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-04 | Added `docs/00_project/artifact_policy.md` with git/release/archive policy for source code, documentation, reports, chart HTML, chart data CSV, dashboard exports, run manifests, logs and archive. | Manual review of policy content; no cleanup command executed. | Policy created; no files deleted, moved, ignored or archived. | `.gitignore` is documented as recommended only and was not created; final git policy for heavy outputs remains a release-process decision. |

## 2026-06-04 - `.gitignore` created

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-04 | Created project-root `.gitignore` after artifact policy confirmation. | Manual content check. | `.gitignore` ignores local environment/cache/log/archive folders and does not ignore `outputs/charts/**/*.html` or `outputs/exports/**/*.csv`. | `git init` was not executed. Final git policy for HTML/CSV release artifacts remains a release-process decision. |

## 2026-06-04 - first commit artifact strategy

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-04 | Fixed first commit strategy in `docs/00_project/artifact_policy.md`: generated outputs are excluded from ordinary Git history. | Reviewed large-file audit: no individual files above 50 MB, but `outputs/charts/` is about 447 MB by baseline. | First commit scope is source/config/docs/scripts/contracts; generated outputs should be release bundle/external/local archive artifacts. | `.gitignore` still needs to be updated in the next step to enforce this strategy before `git add`. |

## 2026-06-04 - `data/raw` first commit decision

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-04 | Confirmed `data/raw` as source dataset for the first Git commit. | `Get-ChildItem data/raw -Recurse -File`; `git check-ignore -v data/raw`; `git check-ignore -v data/raw/*`; temporary-file scan for `~$*.xlsx`, `*.tmp`, `*.bak`. | `data/raw` is not ignored; 8 raw Excel files found, about 0.02-0.03 MB each; no temporary Excel/cache files found; user confirmed no confidential data by manual review. | Pipeline must not modify `data/raw`; raw file hashes should be tracked in raw data registry / run manifest. |

## 2026-06-04 - final `data/raw` Git check

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-04 | Reconfirmed that `data/raw` is committed as the project source dataset. | `git check-ignore -v data/raw`; `git check-ignore -v data/raw/*`; `Get-ChildItem data/raw -Recurse -File`; scan for `~$*.xlsx`, `*.tmp`, `*.bak`. | `data/raw` is not ignored; files are small, up to about 0.03 MB; no heavy files found; no temporary Excel/cache files found; generated outputs are excluded from Git. | User confirmed raw data is acceptable for repository storage; pipeline must not modify `data/raw` in place. |

## 2026-06-05 - repeated secret scan before first commit

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-05 | Repeated pre-commit secret scan for source/config/docs/script candidates. | `Get-ChildItem -Recurse -File -Include *.py,*.md,*.txt,*.json,*.yaml,*.yml,*.toml,*.ini,*.cfg | Select-String -Pattern "password|secret|token|api_key|apikey|private_key|credentials"`; scoped follow-up excluding `.venv`, `.git`, `outputs`, `logs` and `__pycache__`; manual review of matched lines. | No real secrets found. Matches in source candidates are non-secret code tokens such as variable names/constants in chart QA and parser code. `.env` / `*.env` are ignored by `.gitignore`. | Pattern-based scan is heuristic; binary files and raw Excel content were not text-scanned in this step. User has already confirmed `data/raw` is acceptable for repository storage. |

## 2026-06-05 - first commit staging scope

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-05 | Prepared first commit staging scope after `git add .`; excluded `data/processed` from the source commit. | `git diff --cached --name-only`; generated-output filters for `outputs/charts`, `outputs/exports`, `outputs/reports`, `outputs/dashboards`, `outputs/archive`, `outputs/tmp`; `git check-ignore -v data/processed/ofz_auctions_clean.csv`. | `data/raw` is staged; `data/processed` was removed from the index and added to `.gitignore`; generated outputs are not staged except `.gitkeep` files and navigation `index.md`. | `data/processed` can be recreated by pipeline; release-specific processed outputs should be stored in release bundles or external artifacts when audit retention is required. |

## 2026-06-05 - first push to GitHub

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-05 | Pushed the initial source commit to the private GitHub repository `OFZ_ANALYTICS`. | `git remote -v`; `git branch -vv`; `git status --short --branch`; `git log --oneline --decorate -1`. | Remote is `https://github.com/VinogradovPV/OFZ_ANALYTICS.git`; branch `main` tracks `origin/main`; initial commit `4fa6d61fa67281c20d5d7a878cd2191e953507bc` is present locally and remotely; working tree was clean after push. | Repository visibility is recorded as private by project policy; generated outputs are not committed and should be distributed through release bundles or external artifacts when needed. |

## 2026-06-05 - schema validation production stabilization

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-05 | Stabilized `schema_validation / volume_bln_units` production check and aligned `outputs/exports` root validation with the Git skeleton policy. | `schema_validation.py` contract review; `format_discount_*` and `format_terms_aggregate_scatter_*` generator review; `py_compile`; chart rebuild; schema validation; regression tests; quality gate fast. | Unit fields are generated by `scripts/06_build_charts.py`; `.gitkeep`, `README.md` and `index.md` are allowed as skeleton/navigation files in `outputs/exports`, while generated exports remain restricted to subdirectories. `schema_validation.py` passed 16 checks and `regression_tests.py` passed 14 checks after the skeleton whitelist update. | Existing generated outputs are not committed; any stale local CSV/HTML should be regenerated by pipeline commands before validation. |

## 2026-06-05 - baseline quality gate after schema fix

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-05 | Ran baseline production checks after the `schema_validation / volume_bln_units` fix. | `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Passed: `compileall`, schema validation 16/16, quality gate fast OK. Production blocker is resolved. | Generated outputs remain excluded from Git and should be regenerated by pipeline when validating a fresh run. Local Git push can require network access outside the sandbox. |

## 2026-06-05 - dependency stabilization

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-05 | Stabilized runtime/dev dependency contract and documented Windows PowerShell environment setup. | Reviewed imports in `scripts/`; reviewed installed `.venv` package versions; `.\.venv\Scripts\python.exe -m pip check`; `.\.venv\Scripts\python.exe -m compileall -q scripts`. | Runtime dependencies are bounded by major version in `requirements.txt`; `requirements-dev.txt` installs the runtime stack for project-local QA scripts; environment setup documented in `docs/07_operations/environment.md`. | Lockfile deferred to next release; screenshot backend for visual regression remains fallback-only unless added in a later controlled step. |

## 2026-06-05 - project metadata and CLI entry points

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-05 | Added `pyproject.toml` with project metadata and editable-install entry points for existing `main()` modules. | `.\.venv\Scripts\python.exe -m pip install -e .`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-quality.exe --help`; `.\.venv\Scripts\ofz-schema.exe --help`. | Passed: editable install built `ofz-analytics==0.1.0`, `compileall` passed, `ofz-quality --help` and `ofz-schema --help` returned CLI help. | `ofz-clean-outputs` is deferred because `scripts/maintenance/cleanup_outputs.py` does not exist yet; Ruff/Black/pytest/mypy are not enabled in the current production QA contract. |

## 2026-06-05 - production artifact policy update

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-05 | Strengthened `docs/00_project/artifact_policy.md` after Git initialization and first pushes. | Policy review against current repository state: `data/raw` tracked, generated outputs ignored, outputs skeleton tracked via `.gitkeep`/`index.md`. | Added explicit source/generated artifact rules, Git tracking policy, release bundle policy, clean outputs protocol, run manifest retention, `outputs/archive` policy, generated-output commit prohibition and skeleton exception. | `scripts/maintenance/cleanup_outputs.py` is referenced as the approved future cleanup interface but is not implemented yet. |

## 2026-06-05 - safe outputs cleanup command

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-05 | Added `scripts/maintenance/cleanup_outputs.py` with dry-run, archive and confirmed delete modes. | `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\cleanup_outputs.py`; `.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --dry-run`; `.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --delete-all`. | Passed: dry-run found 6 top-level working output candidates, about 468.2 MB, and wrote cleanup manifests under `outputs/reports/cleanup/` without archiving or deleting files. `--delete-all` without `--confirm DELETE_OUTPUTS` failed before deletion with an explicit safety message. Cleanup is limited to `outputs/`, preserves `outputs/archive/`, writes manifests and recreates `.gitkeep` skeleton after deletion. | Cleanup reports/manifests under `outputs/` are generated artifacts and are not committed. |

## 2026-06-05 - Python version policy

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-05 | Relaxed `pyproject.toml` Python metadata from `>=3.14,<3.15` to `>=3.11,<3.15`. | `.\.venv\Scripts\python.exe --version`; dependency metadata review for `pandas`, `numpy`, `openpyxl`, `plotly`, `kaleido`; Python 3.11 syntax parse check for `scripts/**/*.py`; `.\.venv\Scripts\python.exe -m pip install -e .`; `.\.venv\Scripts\python.exe -m pip check`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `ofz-run --help`; `ofz-interactive --help`; `ofz-quality --help`; `ofz-schema --help`; `ofz-clean-outputs --help`. | Passed on current `.venv`: Python 3.14.5, editable install succeeded, `pip check` passed, `compileall` passed, entry point help commands returned successfully. Dependency metadata requires Python `>=3.11` at the strictest point; no strict Python 3.14-only syntax was found. | Python 3.11-3.13 are allowed by metadata but not fully runtime-certified in this local stage; run `quality_gate.py --fast` before trusting outputs on those versions. `ofz-interactive --help` required a small help-mode fix because the interactive launcher previously entered input mode for `--help`. |

## 2026-06-08 - interactive cleanup pre-flight

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-08 | Added cleanup pre-flight to `scripts/interactive_pipeline.py` and translated `docs/07_operations/production_runbook.md` to Russian. | `.\.venv\Scripts\python.exe -m py_compile scripts\interactive_pipeline.py scripts\run_pipeline.py scripts\run_manifest.py scripts\smoke_tests.py`; `.\.venv\Scripts\python.exe scripts\smoke_tests.py`. | Interactive launcher now checks generated `outputs/` before pipeline start and can keep outputs, run dry-run, archive and clean, clean without archive after `DELETE_OUTPUTS_NO_ARCHIVE`, or cancel. Cleanup is delegated to `scripts/maintenance/cleanup_outputs.py`; run manifest records cleanup status/mode/return code for full interactive runs. | Manual interactive path should still be checked by running `.\.venv\Scripts\python.exe scripts\interactive_pipeline.py` in a console before a production run that actually cleans outputs. |

## 2026-06-08 - documentation cleanup inventory workflow

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-08 | Added `scripts/maintenance/cleanup_docs.py` with inventory-first documentation cleanup workflow and created `docs/00_project/docs_inventory_before_cleanup.md`. | `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\cleanup_docs.py`; `.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --dry-run`. | Passed: dry-run classified 83 markdown documents without moving or deleting files: 44 `keep_active`, 4 `merge_candidate`, 35 `archive_candidate`, 0 `delete_candidate`. Cleanup manifest was generated under `outputs/reports/cleanup/` as a generated artifact. | No archive/delete action was executed in this pass. `docs_inventory_after_cleanup.md` is created only after a future `--archive` run. |

## 2026-06-08 - scripts inventory before cleanup

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-08 | Created `docs/00_project/scripts_inventory_before_cleanup.md` for P1 scripts audit without physical file moves. | `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Passed: compileall completed; quality gate fast completed successfully with schema validation 16/16, regression tests 14, smoke tests 9, HTML QA and visual regression fallback OK. Inventory classified 42 Python files: 32 `keep_active`, 5 `refactor_candidate`, 5 `archive_candidate`, 0 `delete_candidate`, 0 unknown. | No Python files were moved or archived. Refactor/archive candidates require a separate migration/archive stage with compatibility checks. |

## 2026-06-08 - module decomposition plan

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-08 | Added `docs/03_pipeline/module_decomposition_plan.md` for future decomposition of large scripts. | Documentation review against `scripts_inventory_before_cleanup.md`, `run_pipeline.py`, `quality_gate.py` and current CLI entry points. | Plan covers `06_build_charts.py`, `10_build_monthly_charts.py`, `html_chart_qa.py`, `visual_regression.py`, `quality_gate.py` and `07_dashboard_exports.py`; no files were moved. | The plan is not an implementation. Each future decomposition step must keep wrapper compatibility and run `compileall` plus `quality_gate.py --fast`. |

## 2026-06-08 - checkpoint before data contracts consolidation

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-08 | Recorded checkpoint after production cleanup stages 8-10 and before data contracts consolidation. | `git status --short`; `git ls-files outputs`; `git ls-files docs/00_project/docs_inventory_before_cleanup.md docs/00_project/scripts_inventory_before_cleanup.md docs/03_pipeline/module_decomposition_plan.md docs/06_quality/manual_checks_log.md`; top-level `scripts/` listing; `Test-Path docs/00_project/docs_inventory_after_cleanup.md`. | Working tree was clean before this log update; tracked `outputs/` contained only `.gitkeep` files and `outputs/charts/index.md`; inventories and module decomposition plan are tracked. No physical script refactor/decomposition was performed. `docs_inventory_after_cleanup.md` is absent, so docs archive apply has not been run in this checkpoint. | Data contracts were intentionally not changed. Physical refactor/decomposition is deferred to P2. Docs archive apply remains a separate controlled step with after-inventory generation. |

## 2026-06-08 - data contracts consolidation

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-08 | Consolidated active data contracts for processed data, analytical tables, chart data, dashboard exports and semantic model v2. | Contract review against `scripts/schema_validation.py`, `scripts/html_chart_qa.py`, `scripts/visual_regression.py`, chart/revenue/dashboard generators and current documentation; `.\.venv\Scripts\python.exe -m py_compile scripts\html_chart_qa.py scripts\visual_regression.py scripts\schema_validation.py`; `.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Added active contracts in `docs/02_data_contracts/`; synchronized visualization docs with unit, revenue, yield, discount, label and quality-field policies; updated `schema_validation.py` to validate unit fields for `_volume_bln` display columns while preserving legacy raw-volume unit fields. Passed: py_compile, schema validation 16/16, quality gate fast OK. Diagnostics `chart_improvement_diagnostics.md` and `format_revenue_discount_chart_diagnostics.md` are ready for a later controlled archive follow-up. | Generated outputs were not edited or committed. Physical script decomposition remains deferred. Diagnostics are not deleted in this stage; archive apply requires a separate cleanup step. |

## 2026-06-08 - docs cleanup apply decision

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-08 | Deferred physical docs archive apply after inventory review. | Reference scan across `README.md`, `docs/**`, `scripts/**`, `pyproject.toml`; `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\cleanup_docs.py`; `.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --dry-run`. | Dry-run completed with 90 documents: 51 `keep_active`, 35 `archive_candidate`, 4 `merge_candidate`. New data contracts, scripts inventory and module decomposition plan are classified as active. Archive apply is deferred because several archive candidates still have active references in `quality_gate.py`, `config.py`, maintenance scripts or `docs/index.md`; merge diagnostics are marked ready for future archive after references are removed. | No documents were archived or deleted. Generated cleanup manifests under `outputs/reports/cleanup/` are not committed. `--delete-archived` remains prohibited before production-ready v1. |

## 2026-06-08 - legacy scripts archive decision

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-08 | Deferred physical archive of five legacy script archive candidates. | Reference scan across `README.md`, `docs/**`, `scripts/**`, `pyproject.toml`, `run_pipeline.py`, `quality_gate.py`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | References still exist for `scripts/archive/2026-06-15/cleanup_docs.py`, `scripts/archive/2026-06-15/migrate_outputs_structure.py`, `scripts/archive/2026-06-15/reorganize_outputs.py`, `scripts/archive/2026-06-15/migrate_legacy_docs_archive.py` and `scripts/archive/2026-06-15/reorganize_docs.py`, so no files were moved. Variant A selected: keep files in place and defer physical archive to P2. | No entry points changed. Module decomposition plan was not changed. Physical archive requires a later reference cleanup and explicit approval. |
## 2026-06-08 - legacy scripts archive decision follow-up

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-08 | Aligned the archive decision artifact with the production cleanup naming convention: `docs/00_project/scripts_archive_decision.md`. | Documentation review against `scripts_inventory_before_cleanup.md` and `production_readiness_report.md`. | The decision is recorded in the required file name, with per-script reference status, production risk and recommendation. `scripts_inventory_before_cleanup.md` and `production_readiness_report.md` were updated. | Physical archive remains deferred to P2. No Python files were moved or deleted. |
## 2026-06-08 - production runbook and release checklist

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-08 | Updated production operations documentation after docs cleanup and scripts archive decisions. | `git status --short`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\python.exe -m pip check`; `.\.venv\Scripts\ofz-run.exe --help`; `.\.venv\Scripts\ofz-interactive.exe --help`; `.\.venv\Scripts\ofz-quality.exe --help`; `.\.venv\Scripts\ofz-clean-outputs.exe --help`; `.\.venv\Scripts\ofz-schema.exe --help`. | Added `docs/07_operations/production_runbook.md` and `docs/07_operations/release_checklist.md` aligned with current CLI entry points, generated-output Git policy, cleanup workflow, release bundle policy and deferred docs/scripts archive decisions. Short `ofz-*` commands require activated `.venv`; direct `.venv\Scripts\ofz-*.exe` checks passed. | This is documentation-only. Full release still requires a separate `ofz-quality --full` run and release bundle preparation. |
## 2026-06-08 - final production quality gate

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-08 | Completed final production-candidate quality gate after production runbook and release checklist. | `.\.venv\Scripts\python.exe -m pip install -e .`; `.\.venv\Scripts\python.exe -m pip check`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; smoke, regression, anomaly, HTML QA, visual regression, `ofz-quality --full`, `ofz-quality --fast`; `git ls-files outputs`; `git ls-files data/raw`. | Passed: editable install, pip check, compileall, schema validation 16/16, smoke 9, regression 14, HTML QA, visual regression fallback, quality gate full and fast. `data/raw` is tracked; `outputs` tracks only skeleton/index files. | Anomaly tests completed with expected data warnings. Screenshot backend is not configured, so visual regression used static HTML / Plotly JSON fallback. Initial parallel fast/full quality-gate run caused a transient `.pyc` permission conflict; sequential rerun passed. |
## 2026-06-09 - P2 starting checkpoint

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-09 | Started P2 modernization with a formal baseline checkpoint and execution protocol. | `git status --short --branch`; `git branch --show-current`; `git remote -v`; `git log --oneline -5`; `git ls-files data/raw`; `git ls-files outputs`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\ofz-quality.exe --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.venv\Scripts\ofz-*.exe --help`. | Baseline confirmed: branch `main`, remote `origin/main`, `data/raw` tracked, generated outputs not tracked except skeleton/index, fast/full quality gates OK, CLI entry points OK. Created `p2_starting_checkpoint.md` and `p2_modernization_progress_report.md`. | `anomaly_tests` warnings remain documented data warnings. Visual regression remains fallback-only until P2 screenshot backend. |
## 2026-06-09 - P2 system prompt v3

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-09 | Replaced the initial P2 modernization system prompt with `prompts/ofz_p2_modernization_system_prompt_v3.md`. | Reference scan for old/new prompt filenames; Git status review. | Old prompt filename references were updated in P2 checkpoint/progress docs. The old prompt file was removed from the active source prompt set; v3 is tracked as the current source prompt asset. | Documentation/source-prompt change only. No pipeline code or generated outputs changed. |

## 2026-06-11 - P2.6.2 Word VBA docm assembly source

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-11 | Prepared Word VBA launcher assembly source: refreshed `OfzLauncher.bas`, added `frmOfzLauncher.frm`, and added manual `.docm` build instructions. | Level 1 source checks: required `OFZ_*` procedures/functions scanned in `.bas`; required UserForm controls scanned in `.frm`; `.docm`/`releases` staging checks planned before commit. | Source is ready for manual Word import. The module builds only whitelisted CLI commands, blocks delete without `DELETE_OUTPUTS`, blocks release build without `BUILD_RELEASE_BUNDLE`, and logs to `outputs/reports/launcher`. | Word automation was not executed in this environment. `.docm` assembly status is `deferred/manual`; the release artifact must be built in Word under `releases/ui_launcher/` and must not be committed. |

## 2026-06-11 - P2.7 screenshot visual regression backend

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-11 | Added Playwright screenshot backend to `scripts/visual_regression.py` with `--mode fallback`, `--mode screenshot` and `--mode auto`; kept existing static HTML / Plotly JSON fallback. | `.\.venv\Scripts\python.exe -m py_compile scripts\visual_regression.py`; visual regression `--mode fallback`; visual regression `--mode auto`; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; Pylance missing-import review. | Passed: py_compile, fallback mode, auto mode and quality gate fast. Screenshot backend opens local HTML, hides Plotly modebar, saves screenshots/manifests/diff reports as generated outputs and writes `visual_regression_mode` to reports. Direct `playwright.sync_api` imports were replaced with dynamic `importlib.import_module` so Playwright remains optional and Pylance does not flag it as a required runtime import. | Playwright is not installed in the current `.venv`, so `--mode auto` records a warning and uses fallback. To enable screenshot mode, install dev dependencies and Chromium via `python -m playwright install chromium`. Missing baseline screenshots are recorded as `missing_baseline`, not as failures during P2.7 stabilization. |
| 2026-06-16 | Stabilized screenshot backend after local Playwright/Chromium installation. | User PowerShell smoke: `.\.venv\Scripts\python.exe -m playwright --version` returned `1.60.0`; `sync_playwright` headless Chromium smoke created `playwright_smoke.png`; Codex sandbox checks: `py_compile`, visual regression `--mode fallback`, visual regression `--mode auto`. | Passed: py_compile, fallback mode and auto mode in Codex sandbox. Code now records `screenshot_backend`, uses stable Playwright launch flags, skips browser subprocess attempts in Codex managed sandbox, and keeps optional Chromium CLI fallback behind `OFZ_VISUAL_REGRESSION_CHROMIUM_CLI_FALLBACK=1`. | Direct full `--mode screenshot` should be run from the project PowerShell session because Codex sandbox blocks browser subprocess pipes. `playwright_smoke.png` and screenshot outputs are generated artifacts and must not be committed. |

## 2026-06-09 - P2.1 release bundle automation

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-09 | Added external release bundle automation through `scripts/maintenance/build_release_bundle.py` and entry point `ofz-build-release-bundle`. | `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\build_release_bundle.py`; release bundle dry-run for month/cumulative 2026-05-01 r4; `.\.venv\Scripts\python.exe -m pip install -e .`; `.\.venv\Scripts\ofz-build-release-bundle.exe --help`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Passed: py_compile, dry-run, editable install after escalated retry, CLI help, compileall and quality gate fast. Dry-run found 100 chart files, 137 export files, 34 dashboard files, 12 run manifest files, 66 QA report files, 4 executive summary files and 3 data quality summary files. Bundle writes to ignored `releases/` and requires `--include-outputs --confirm BUILD_RELEASE_BUNDLE` outside dry-run. | `telemetry_summary` is optional until P2.2 Pipeline telemetry. Actual release bundle creation was not executed in this stage. Initial `pip install -e .` failed inside sandbox on `%TEMP%` permissions and passed after approved retry. |

## 2026-06-09 - P2.2 pipeline telemetry

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-09 | Added pipeline telemetry reporting through `scripts/pipeline/telemetry.py` and integrated telemetry links into run manifest. | Planned checks: `py_compile`, full `ofz-run`, `ofz-quality --fast`, telemetry file listing and generated-output staging filter. | Telemetry writes JSON/Markdown to `outputs/reports/telemetry/`, records stage durations, row/file counts, artifact count/size, cleanup mode, QA/schema status, Git commit/dirty flag and raw data hashes. | Telemetry outputs are generated artifacts and are not committed. P2.2 does not add external telemetry dashboards; that remains a later optional extension. |
| 2026-06-09 | Completed P2.2 validation after fixing the executive summary runtime cast issue. | `.\.venv\Scripts\python.exe -m py_compile scripts\generate_executive_summary.py scripts\pipeline\telemetry.py scripts\run_pipeline.py scripts\run_manifest.py scripts\maintenance\build_release_bundle.py`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; telemetry file listing. | Passed: py_compile, compileall, full `ofz-run`, quality gate fast. Latest telemetry files: `outputs/reports/telemetry/telemetry_20260609_080836_53742514.json` and `.md`. Latest run manifest contains telemetry links. | Initial `ofz-run` failed before the final run because `pd.Series[Any]` was used as a runtime `cast` target in `generate_executive_summary.py`; fixed by using non-subscripted `pd.Series` in the runtime cast. Generated telemetry and pipeline outputs remain uncommitted artifacts. |
| 2026-06-09 | Closed P2.2 telemetry validation after final `ofz-quality --fast`. | `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; telemetry JSON inspection; run manifest telemetry link inspection. | Passed: compileall and quality gate fast. Telemetry JSON contains 19 `stage_durations`, generated artifact count/size, quality/schema status, Git commit/dirty flag and raw data hashes. Run manifest points to telemetry JSON/MD. | Telemetry was produced while P2.2 code/docs were still uncommitted, so `git_dirty_flag=True` is expected for this validation run. Telemetry files under `outputs/reports/telemetry/` are generated artifacts and are not committed. |

## 2026-06-11 - P2.3 UI launcher contract

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-11 | Created `docs/07_operations/ui_launcher_contract.md` as the contract for future UI launchers. | Level 0 checks: `git status --short`; `git diff --name-only`; staged generated artifacts filter; `Select-String` for `ofz-build-release-bundle`, `BUILD_RELEASE_BUNDLE`, `DELETE_OUTPUTS`, `release_bundle_plan`, `telemetry`, `docm`, `PowerShell`. | Contract covers CLI-only execution, supported CLI entry points, parameter validation, cleanup safety, release bundle confirmation, launcher logs, prohibited behavior, Word VBA policy and PowerShell GUI policy. | No PowerShell GUI or Word VBA source was created in this stage. `compileall` and quality gates were skipped because this was docs-only and session preflight was already OK. |

## 2026-06-11 - P2.4 PowerShell GUI launcher MVP

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-11 | Added `tools/windows_launcher/ofz_launcher.ps1` and `tools/windows_launcher/README.md` as the Windows UI launcher MVP. | Level 1 checks: `git status --short --branch`; `powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1`; staged generated artifacts filter; `git diff --name-only`. | Launcher smoke passed: environment validation OK, bad date blocked, delete cleanup blocked without `DELETE_OUTPUTS`, release bundle creation blocked without `BUILD_RELEASE_BUNDLE`, cleanup dry-run ran, release bundle dry-run ran, launcher log was created under `outputs/reports/launcher/`. | `compileall` and quality gates were skipped because this was UI source/docs only. Generated launcher logs remain ignored artifacts. P2 prompt v4/v5 files remain untracked until a separate source-prompt decision. |

## 2026-06-11 - P2.5 Word VBA launcher spec and source

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-11 | Added Word VBA launcher source and specification: `docs/07_operations/word_vba_launcher_spec.md`, `tools/word_launcher/README.md`, `tools/word_launcher/OfzLauncher.bas`. | Level 1 checks: `git status --short --branch`; reference/status review; `Select-String` for `ofz-build-release-bundle`, `BUILD_RELEASE_BUNDLE`, `DELETE_OUTPUTS`, `.docm`, `macro security`, `arbitrary`; staged generated artifacts filter. | Source contract is documented: `.bas` can be committed, `.docm` is a release artifact, VBA calls only whitelisted CLI, delete and bundle actions require confirmation tokens, macro security is documented. | Word import smoke is manual-only and was not executed automatically. `compileall` and quality gates were skipped because no Python code changed. P2 prompt v4/v5 files remain untracked until a separate source-prompt decision. |

## 2026-06-11 - P2.6 UI launcher documentation and artifact policy

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-11 | Updated UI launcher documentation and artifact policy in README, production runbook, release checklist, artifact policy and P2 progress report. | Level 0 checks: docs diff review; staged generated artifacts filter; `Select-String` for CLI primary interface, PowerShell GUI, Word VBA, `.ps1`, `.bas`, `.frm`, `.docm`, launcher logs, release bundle and quality gate. | Documentation now states that CLI remains the primary interface, PowerShell GUI is the recommended Windows UI MVP, Word VBA is optional, launcher source files are source artifacts, `.docm` is a release artifact, launcher logs are generated outputs, release bundles stay external, and UI launchers do not replace quality gate. | `compileall` and quality gates were skipped because this was docs-only. P2.5 Word VBA tool source must be committed separately if not included in the active stage. |

## 2026-06-11 - P2.6.1 PowerShell GUI launcher hardening

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-11 | Hardened `tools/windows_launcher/ofz_launcher.ps1` from a minimal smoke GUI into a parameterized Windows launcher. | Level 1 checks: PowerShell parse check; `powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1`; `powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Gui -AutoCloseGuiForCheck`; staged generated artifacts filter. | Passed: default smoke validates environment, blocks bad report date, blocks delete without `DELETE_OUTPUTS`, blocks release-build without `BUILD_RELEASE_BUNDLE`, runs cleanup dry-run and release bundle dry-run. GUI opens without runtime error in auto-close check and no longer auto-closes in normal `-Gui` mode. GUI includes project root, report date, retrospective years, period type, aggregation mode, action, cleanup mode, confirm fields, command preview, output/status and log path. | `compileall` and quality gates skipped because only PowerShell UI source/docs changed. Full manual GUI verification should be done by launching `-Gui`, selecting fields and pressing `Validate`. Generated launcher logs and cleanup dry-run manifests remain ignored artifacts. |

## 2026-06-11 - P2.8 CI / GitHub Actions

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-11 | Added GitHub Actions workflow `.github/workflows/quality.yml` and documented CI contract in `docs/07_operations/ci_workflow.md`. | `.\.venv\Scripts\python.exe -m pip check`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; staged generated artifacts filter; GitHub-side `gh workflow list` / `gh run list` planned after push. | Passed: pip check, compileall, schema validation 16/16 and quality gate fast. Workflow has `quality-fast` for push/PR/manual and `quality-full` manual-only via `workflow_dispatch`. | CI uploads QA reports as workflow artifacts and must not commit generated outputs. Local fast gate recorded the expected visual regression warning: Playwright/screenshot backend unavailable, fallback mode used. |

## 2026-06-15 - P2.9 Controlled docs archive apply

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-15 | Applied controlled documentation archive after inventory review. | `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\cleanup_docs.py scripts\quality_gate.py`; `.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --dry-run`; `.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --archive`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Archived 39 legacy documentation files to `docs/archive/2026-06-15/`; after-inventory created with 61 `keep_active` documents and 39 archived candidates. `--delete-archived` was not used. | Cleanup manifests under `outputs/reports/cleanup/` are generated artifacts and are not committed. Legacy scripts archive is still deferred to P2.10. |

## 2026-06-15 - P2.10 Controlled legacy scripts archive apply

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-15 | Applied controlled legacy scripts archive. | Reference scan across `README.md`, `docs/**`, `scripts/**`, `pyproject.toml`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; CLI help checks; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | Five legacy maintenance scripts moved to `scripts/archive/2026-06-15/`; no files deleted; no entry points changed. | Archived scripts are audit artifacts only. Current production maintenance uses `ofz-clean-outputs`, `scripts/maintenance/cleanup_outputs.py`, `scripts/maintenance/cleanup_docs.py` and release bundle tooling. |

## 2026-06-15 - P2.11.1 chart common helpers

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-15 | Extracted pure chart formatting helpers from `scripts/06_build_charts.py` into `scripts/charts/common.py`; added `scripts/charts/__init__.py`. | `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py scripts\charts\common.py scripts\charts\__init__.py`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; targeted chart build; HTML QA; visual regression; `ofz-quality --fast`. | Passed: py_compile, compileall, `06_build_charts.py`, `html_chart_qa.py`, `visual_regression.py`, and quality gate fast. CLI behavior, output filenames, chart contracts and schema contracts were unchanged. | Visual regression used the existing fallback mode because screenshot backend was unavailable in the current environment. Generated outputs remain ignored and were not staged. |

## 2026-06-15 - P2.11.2 chart family module skeleton

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-15 | Added behavior-neutral chart family modules under `scripts/charts/`: `structure`, `scatter`, `monthly`, `revenue`, `boxplot`; added `CHART_FAMILY_MODULES` in `scripts/charts/__init__.py`. | `.\.venv\Scripts\python.exe -m py_compile scripts\charts\__init__.py scripts\charts\structure.py scripts\charts\scatter.py scripts\charts\monthly.py scripts\charts\revenue.py scripts\charts\boxplot.py`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `ofz-quality --fast`. | Passed: py_compile, compileall and quality gate fast. No chart builders were moved in this step, so CLI behavior and output contracts remain unchanged. | This is a skeleton step only. Actual builder extraction remains incremental and must be done one family/helper group per commit. |

## 2026-06-15 - P2.11.3 QA contract modules

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-15 | Added `scripts/qa/html_chart_contracts.py` and `scripts/qa/visual_regression_contracts.py`; moved QA contract constants plus `QaResult`/`VisualCheck` out of the monolithic QA scripts. | `py_compile` for changed QA files; `compileall -q scripts`; targeted `06_build_charts.py`; `html_chart_qa.py`; `visual_regression.py`; `ofz-quality --fast`. | Passed: py_compile, compileall, targeted chart build, HTML QA, visual regression and quality gate fast. CLI behavior and QA outcomes remain unchanged. | Check functions remain in the current scripts. Further QA decomposition should move one small check group per commit. Visual regression used fallback because screenshot backend was unavailable in the current environment. |

## 2026-06-16 - P2.12 Windows setup / Docker plan

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-16 | Added reproducible Windows setup workflow and Docker plan. | `powershell -NoProfile -ExecutionPolicy Bypass -File tools/setup/setup_windows.ps1 -DryRun`; generated artifact staging filter before commit. | Dry-run passed. `tools/setup/setup_windows.ps1` supports `.venv` creation, runtime/dev dependency install, editable install, `pip check`, CLI help checks, `compileall`, and optional fast quality gate via `-RunFastQuality`. `docker_plan.md` documents Docker as optional while Windows-first remains primary. | Actual setup was not run on the current already-configured machine because it would mutate `.venv`; run it on a clean/new machine. Setup script does not touch `outputs/`; Dockerfile/.dockerignore are deferred to a future explicit decision. |

## 2026-06-16 - P2.13 BI-ready release package

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-16 | Added BI-ready release package workflow. | `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\build_bi_package.py`; dry-run for month cumulative 2026-05-01 scope; generated artifact staging filter before commit. | OK. Dry-run found required source exports and generated BI dimension previews without writing files. | BI package is an ignored external artifact under `releases/bi/`; build mode is not run unless `--include-outputs --confirm BUILD_BI_PACKAGE` is provided. |

## 2026-06-16 - P2.15 final close-out

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-16 | Final P2 close-out checks. | `pip install -e .`; `pip check`; `compileall`; `ofz-schema`; `ofz-quality --fast`; `ofz-quality --full`; release bundle dry-run. | OK. Fast/full quality gates passed and release bundle dry-run wrote no files. | First `pip install -e .` attempt in sandbox failed on Windows temp permission; outside-sandbox rerun passed. Visual regression used fallback in Codex managed sandbox. Anomaly tests reported domain data-quality warnings. |

## 2026-06-16 - P3.PRE.0 Windows GUI launcher UX and runtime fix

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-16 | Fixed Windows launcher preview/runtime behavior and updated Russian UX documentation. | PowerShell parse check; launcher smoke; GUI auto-close smoke; `-Action validate-environment`; `-Action release-dry-run`; safe-fail checks for `release-build` without `BUILD_RELEASE_BUNDLE` and `cleanup-delete-all` without `DELETE_OUTPUTS`; `-Action run-pipeline -PreviewOnly`. | OK. Preview no longer reads a missing `.Preview` property under `Set-StrictMode`; validate-environment reports explicit OK/FAIL local file checks without starting a pipeline process; `run-pipeline` preview uses `.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` and does not include `--stages`; release dry-run works without `BUILD_RELEASE_BUNDLE`; destructive release/delete actions are blocked without tokens; launcher logs now use unique names. | Real `run-pipeline` was not executed through the launcher because preview-only verified command construction and full execution may generate outputs. `compileall`, `ofz-quality --fast` and `ofz-quality --full` were skipped because Python pipeline code did not change. Generated launcher logs and cleanup dry-run manifests remain generated artifacts and must not be committed. |

## 2026-06-16 - CI UTF-8 schema validation fix

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-16 | Fixed GitHub Actions `quality-fast` failure caused by Windows runner stdout encoding during schema validation. Also fixed follow-up CI blockers surfaced after schema validation could print UTF-8 diagnostics. | `.\.venv\Scripts\python.exe -m py_compile scripts\schema_validation.py scripts\quality_gate.py scripts\run_pipeline.py scripts\smoke_tests.py scripts\console_encoding.py`; `.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `PYTHONIOENCODING=cp1252` schema run; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; GitHub Actions runs `27620284328` and `27623278589`. | Local checks OK. UTF-8 fix sets workflow `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`, runs `chcp 65001` before Python/CLI steps, and configures UTF-8 stdout/stderr with replacement in CLI entry points that print Cyrillic diagnostics. The cp1252 schema simulation no longer raises `UnicodeEncodeError`. Run `27620284328` confirmed UTF-8 output worked, then failed because CI checkout did not contain generated `data/processed` and outputs. Workflow now runs `ofz-run` before schema/quality. `smoke_tests.py` searches dashboard exports recursively under `outputs/dashboards/`, matching the P2 organized dashboard structure. Run `27623278589` completed successfully. | Generated outputs/release artifacts were not staged. |

## 2026-06-16 - P3.PRE.1 scripts balance/problem audit

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-16 | Created P3.PRE.1 scripts balance/problem audit helper and report. | `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\audit_scripts_balance.py`; `.\.venv\Scripts\python.exe scripts\maintenance\audit_scripts_balance.py --report`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; generated artifact staging filter before commit. | OK. Audit report created at `docs/00_project/p3_scripts_balance_audit_report.md`. No `shell=True`, active `scripts.archive` dependency, hardcoded absolute user path, TODO/FIXME/XXX marker, active CLI-like missing `main()`, or direct `data/raw` mutation was found. Deferred P3.MOD items remain for controlled chart/QA monolith decomposition. | `ofz-quality --fast` and `ofz-quality --full` were skipped because this step changed only an audit helper and documentation, with no pipeline behavior change. P3.0 source acquisition was not started. |

## 2026-06-16 - P3.PRE.2 docs encoding audit and normalization

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-16 | Audited Markdown documentation for mojibake/encoding problems and normalized active docs to UTF-8. | `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\audit_docs_encoding.py`; `.\.venv\Scripts\python.exe scripts\maintenance\audit_docs_encoding.py --report`; `git diff --name-only`; `git diff --name-only \| Select-String "outputs\|releases\|logs\|data/processed"`. | OK. Audit report created at `docs/00_project/p3_docs_encoding_audit_report.md` with one row per checked document. Checked 128 Markdown documents: 16 normalized to UTF-8, 1 normalized while retaining intentional mojibake pattern-reference text, 111 unchanged, 0 manual-review items. README legacy mojibake was normalized. | `compileall`, `ofz-quality --fast` and `ofz-quality --full` were skipped because this stage was documentation/encoding only with no pipeline behavior change. Archived docs were checked but not rewritten as historical records unless active scope required normalization. P3.0 source acquisition was not started. |

## 2026-06-16 - P3.PRE.2 scripts README encoding addendum

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-16 | Added `scripts/**/*.md` to the docs encoding audit scope and normalized `scripts/README.md`. | `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\audit_docs_encoding.py`; `.\.venv\Scripts\python.exe scripts\maintenance\audit_docs_encoding.py --fix-active --report`; Unicode-level pattern verification for `scripts/README.md`. | OK. `scripts/README.md` now has 0 configured mojibake pattern hits. The regenerated audit report checks 130 Markdown documents: 17 normalized to UTF-8, 1 normalized while retaining intentional pattern-reference text, 112 unchanged. | `compileall`, `ofz-quality --fast` and `ofz-quality --full` were skipped because this was documentation/encoding only with no pipeline behavior change. P3.0 source acquisition was not started. |

## 2026-06-16 - P3.0 Minfin source acquisition design

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-16 | Designed controlled Minfin OFZ auction source acquisition workflow using Variant C: hybrid latest + final + version snapshots on hash change. | `git diff --name-only`; staged generated artifacts filter before commit. | OK. Created `docs/02_data_contracts/minfin_source_registry_contract.md`, `docs/07_operations/minfin_source_acquisition.md`, and `docs/00_project/p3_source_data_roadmap.md`. Documented monthly lifecycle, January annual-final lifecycle, storage structure, Git/artifact policy, registry fields, future CLI, integration path, failure behavior, and manual fallback import. | Design-only step. Downloader code, raw storage directories, raw Excel files and pipeline behavior were not changed. Both Minfin URL variants checked during design review returned `503 Service Unavailable`, so failure behavior was documented but no acquisition was attempted. `py_compile`, `compileall`, `ofz-quality --fast` and `ofz-quality --full` were skipped because no Python code changed. |

## 2026-06-17 - P3.1 Skeleton source acquisition с HTML-aware parser

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-17 | Добавлен skeleton `ofz-fetch-minfin` и offline HTML-aware parser для секции Минфина `id_66` / `page_66` / `ajax-pagination-content-10090-66`. | `.\.venv\Scripts\python.exe -m py_compile scripts\source_acquisition\minfin_fetch.py scripts\source_acquisition\minfin_html_parser.py scripts\source_acquisition\source_registry.py`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\python.exe -m pip install -e .`; `.\.venv\Scripts\ofz-fetch-minfin.exe --help`; no-network dry-runs; `--html-file` monthly/annual-final dry-runs; `scripts\qa\minfin_source_acquisition_smoke.py`. | OK. CLI help работает; `--no-network` dry-run не мутирует raw; `--html-file` выбирает monthly candidate за 2026 и annual-final candidate за 2025; parser игнорирует sections 65/38/39, читает только `a.file_item`, резолвит relative URLs и не требует `YYYY1231` для annual-final. | Реальное скачивание заблокировано на P3.1; raw storage dirs, `.gitkeep`, registry в `data/raw`, `data/raw` и generated outputs не создавались и не изменялись. `ofz-quality --fast/full` пропущены, потому что pipeline behavior не менялся. |
## 2026-06-17 - P3.2 Registry writer с HTML provenance

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-17 | Реализован offline registry writer для controlled Minfin source acquisition: `RegistryRecord`, CSV/JSON roundtrip, SHA-256/file size helpers, active row selection, changed/unchanged hash detection, superseded active row и validation. | `.\.venv\Scripts\python.exe -m py_compile scripts\source_acquisition\source_registry.py`; `.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_source_registry_smoke.py`; `.\.venv\Scripts\python.exe scripts\qa\minfin_source_registry_smoke.py`; `.\.venv\Scripts\python.exe -m compileall -q scripts`. | OK. Smoke test пишет только во временную директорию, проверяет CSV/JSON read-write, hash changed/unchanged, active row selection и validation failure. | Реальное скачивание не выполнялось; registry в настоящий `data/raw/minfin/ofz_auction_results/` не писался; raw storage и generated outputs не изменялись. `ofz-quality --fast/full` пропущены, потому что pipeline behavior не менялся. |
## 2026-06-17 - P3.2 Registry writer с HTML provenance

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-17 | Добавлен registry writer layer для Minfin source acquisition: `RegistryRecord`, `RegistryStatus`, CSV/JSON read-write, append, SHA-256, file size, active row selection, hash changed/unchanged, superseded marker и record validation. | `.\.venv\Scripts\python.exe -m py_compile scripts\source_acquisition\source_registry.py`; `.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_source_registry_smoke.py`; `.\.venv\Scripts\python.exe scripts\qa\minfin_source_registry_smoke.py`; `.\.venv\Scripts\python.exe -m compileall -q scripts`. | OK. Smoke test создает temporary files, считает sha256/size, пишет CSV и JSON registry, читает обратно, проверяет append, active latest selection, unchanged/changed hash и снятие active flag у superseded record. HTML provenance поля поддержаны. | Реальное скачивание не выполнялось; registry не писался в настоящий `data/raw/minfin`; настоящий raw storage не создавался и не изменялся. `ofz-quality --fast/full` пропущены, потому что pipeline behavior не менялся. |
## 2026-06-17 - P3.3 Monthly acquisition implementation

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-17 | Реализован controlled monthly acquisition workflow для `ofz-fetch-minfin`: HTTP fetch/download helpers, section 66 pagination, monthly candidate selection, temp download, validation, hash compare, latest/version promotion, registry update and source acquisition report. | `.\.venv\Scripts\python.exe -m py_compile scripts\source_acquisition\minfin_fetch.py scripts\source_acquisition\http_client.py scripts\source_acquisition\source_registry.py`; `.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_monthly_acquisition_smoke.py`; `.\.venv\Scripts\python.exe scripts\qa\minfin_monthly_acquisition_smoke.py`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --dry-run --no-network`; `.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --download`. | OK. Offline smoke покрывает changed/unchanged hash, latest/version promotion, registry update, report write и simulated network failure without raw mutation. `--download` без `DOWNLOAD_MINFIN_SOURCE` безопасно блокируется до network/raw mutation. | Реальный download не запускался, потому что для него нужно отдельное разрешение пользователя. `versions/` и `outputs/reports/source_acquisition/` являются generated/external outputs и не должны коммититься. `ofz-quality --fast/full` пропущены, потому что pipeline behavior не менялся. |
## 2026-06-17 - P3.REL.1 Stable release procedure update

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-17 | Создана stable release procedure с source acquisition dry-run/update, registry review, data audit, quality-fast/full, screenshot validation outside sandbox, release bundle, optional BI package, git tag и запретом `gh release create/upload` без отдельного разрешения. | `git diff --name-only`. | OK: этап docs-only, изменены release procedure/checklist, README и stage reports. | `compileall` и `ofz-quality` не запускались, потому что Python-код не менялся. GitHub Actions runs не проверяются по инструкции пользователя. |

## 2026-06-17 - P3.8 Operator procedure

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-17 | Создана русскоязычная процедура monthly update, annual-final, changed final hash и manual fallback для Minfin source acquisition. Обновлены source acquisition doc, release checklist и README. | `git diff --name-only`. | OK: этап docs-only, изменены только операционные документы и stage reports. | `compileall` и `ofz-quality` не запускались, потому что Python-код не менялся. GitHub Actions runs не проверяются по инструкции пользователя. |

## 2026-06-17 - P3.7 Parser QA fixtures/tests

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-17 | Добавлены offline QA fixtures/tests для Minfin parser, pagination, selection, hash, annual-final, manual-import и failure modes. | `.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_source_acquisition_tests.py`; `.\.venv\Scripts\python.exe scripts\qa\minfin_source_acquisition_tests.py`; `.\.venv\Scripts\python.exe -m compileall -q scripts`. | OK: wrong sections ignored, pagination tested, annual-final non-YYYY1231 tested, simulated 503 не мутирует raw, dry-run не пишет raw/output paths. | Live site не используется; тесты работают только на fixtures/temp roots. GitHub Actions runs не проверяются по инструкции пользователя. |

## 2026-06-17 - P3.6 Registry integration with data audit

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-17 | Data audit получил validation-only интеграцию Minfin source registry: `--source-registry-mode off\|warn\|strict`, `--allow-legacy-raw`, registry helpers, strict failures для missing registry/file/hash/duplicates. | `.\.venv\Scripts\python.exe -m py_compile scripts\01_data_audit.py scripts\source_acquisition\source_registry.py`; `.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_data_audit_registry_smoke.py`; `.\.venv\Scripts\python.exe scripts\qa\minfin_data_audit_registry_smoke.py`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`; `.\.venv\Scripts\python.exe scripts\01_data_audit.py --source-registry-mode warn --allow-legacy-raw`. | OK: smoke покрыл missing registry warn/strict, valid registry, missing active file, hash mismatch, duplicate active rows, legacy fallback allowed; fast quality gate прошел; data audit warn продолжил legacy raw fallback. | Generated audit/quality outputs не коммитятся. Strict на настоящем production registry не запускался как migration gate; GitHub Actions runs не проверяются по инструкции пользователя. |

## 2026-06-17 - P3.5 Manual fallback import

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-17 | Реализован `manual-import` для Минфина: canonical `--manual-file`, блокировка без `IMPORT_MINFIN_FILE`, валидация `.xlsx`/шаблона/года, temp+promote workflow, registry `discovery_method=manual-import`, запрет записи `final`. | `.\.venv\Scripts\python.exe -m py_compile scripts\source_acquisition\minfin_fetch.py`; `.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_manual_import_smoke.py`; `.\.venv\Scripts\python.exe scripts\qa\minfin_manual_import_smoke.py`; `.\.venv\Scripts\python.exe -m compileall -q scripts`. | OK: smoke проверяет manual dry-run hash/role, блокировку import без confirm, successful import, unchanged observation, year mismatch rejected, invalid extension rejected, отсутствие final overwrite. | Реальный внешний операторский файл не импортировался; smoke использует temp XLSX bytes. GitHub Actions runs не проверяются по инструкции пользователя. |

## 2026-06-17 - P3.4 Annual finalization

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-06-17 | Реализован `annual-final` workflow для Минфина: выбор final candidate без требования `YYYY1231`, блокировка changed final hash без `REPLACE_MINFIN_FINAL`, registry row `storage_role=final`. | `.\.venv\Scripts\python.exe -m py_compile scripts\source_acquisition\minfin_fetch.py scripts\source_acquisition\source_registry.py`; `.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_annual_final_smoke.py`; `.\.venv\Scripts\python.exe scripts\qa\minfin_annual_final_smoke.py`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-fetch-minfin.exe --year 2025 --mode annual-final --dry-run --no-network`. | OK: temp smoke проверяет no final, same hash, different hash blocked и replacement with confirm; dry-run без сети не мутирует raw. | Реальный live download не выполнялся без отдельного разрешения пользователя; GitHub Actions runs не проверяются по инструкции пользователя. |
