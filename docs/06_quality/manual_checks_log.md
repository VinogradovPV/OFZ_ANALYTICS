# Журнал ручных проверок

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
| 2026-06-08 | Deferred physical archive of five legacy script archive candidates. | Reference scan across `README.md`, `docs/**`, `scripts/**`, `pyproject.toml`, `run_pipeline.py`, `quality_gate.py`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`. | References still exist for `scripts/cleanup_docs.py`, `scripts/migrate_outputs_structure.py`, `scripts/reorganize_outputs.py`, `scripts/maintenance/migrate_legacy_docs_archive.py` and `scripts/maintenance/reorganize_docs.py`, so no files were moved. Variant A selected: keep files in place and defer physical archive to P2. | No entry points changed. Module decomposition plan was not changed. Physical archive requires a later reference cleanup and explicit approval. |
## 2026-06-08 - legacy scripts archive decision follow-up

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-08 | Aligned the archive decision artifact with the production cleanup naming convention: `docs/00_project/scripts_archive_decision.md`. | Documentation review against `scripts_inventory_before_cleanup.md` and `production_readiness_report.md`. | The decision is recorded in the required file name, with per-script reference status, production risk and recommendation. `scripts_inventory_before_cleanup.md` and `production_readiness_report.md` were updated. | Physical archive remains deferred to P2. No Python files were moved or deleted. |
## 2026-06-08 - production runbook and release checklist

| Date | Change | Check | Result | Limitations |
|---|---|---|---|---|
| 2026-06-08 | Updated production operations documentation after docs cleanup and scripts archive decisions. | `git status --short`; `.\.venv\Scripts\python.exe -m compileall -q scripts`; `.\.venv\Scripts\python.exe -m pip check`; `.\.venv\Scripts\ofz-run.exe --help`; `.\.venv\Scripts\ofz-interactive.exe --help`; `.\.venv\Scripts\ofz-quality.exe --help`; `.\.venv\Scripts\ofz-clean-outputs.exe --help`; `.\.venv\Scripts\ofz-schema.exe --help`. | Added `docs/07_operations/production_runbook.md` and `docs/07_operations/release_checklist.md` aligned with current CLI entry points, generated-output Git policy, cleanup workflow, release bundle policy and deferred docs/scripts archive decisions. Short `ofz-*` commands require activated `.venv`; direct `.venv\Scripts\ofz-*.exe` checks passed. | This is documentation-only. Full release still requires a separate `ofz-quality --full` run and release bundle preparation. |
