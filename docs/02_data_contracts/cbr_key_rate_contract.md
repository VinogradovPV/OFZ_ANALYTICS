# Контракт источника ключевой ставки Банка России

Дата актуализации: 2026-07-02.

## Назначение

Этот контракт фиксирует модель хранения, источник и правила нормализации ключевой ставки Банка России в OFZ Analytics. Контракт используется parser-ом `scripts/reference_data/cbr_key_rate.py` и графиком `ofz_pd_yield_key_rate`.

В scope входит только ключевая ставка Банка России. Инфляция, цель по инфляции и любые поля `inflation_yoy` / `inflation_target` не входят в этот контракт.

Текущий pipeline может временно использовать ручной XLSX fallback, но целевая модель хранения web parser должна соответствовать этому документу.

## Primary source

Основной источник:

```text
https://cbr.ru/hd_base/KeyRate/
```

Параметризованный URL:

```text
https://cbr.ru/hd_base/KeyRate/?UniDbQuery.Posted=True&UniDbQuery.From=<DD.MM.YYYY>&UniDbQuery.To=<DD.MM.YYYY>
```

Параметры запроса:

| Параметр | Обязательность | Формат | Назначение |
|---|---:|---|---|
| `UniDbQuery.Posted` | да | `True` | Фильтр опубликованных наблюдений. |
| `UniDbQuery.From` | да | `DD.MM.YYYY` | Начальная дата периода. |
| `UniDbQuery.To` | да | `DD.MM.YYYY` | Конечная дата периода. |

Пример URL:

```text
https://cbr.ru/hd_base/KeyRate/?UniDbQuery.Posted=True&UniDbQuery.From=01.01.2019&UniDbQuery.To=02.07.2026
```

Фактический `source_url` не записывается в daily CSV. Если provenance нужен, он хранится только в отдельном metadata-файле.

## Preferred HTML source

Preferred source внутри страницы Банка России:

```html
<table class="data">
  <tr>
    <th>Дата</th>
    <th>Ставка</th>
  </tr>
  ...
</table>
```

Parser обязан:

1. Найти ровно одну таблицу `table.data`.
2. Проверить headers после нормализации: `Дата`, `Ставка`.
3. Прочитать строки таблицы.
4. Отбросить пустые строки.
5. Конвертировать дату из `DD.MM.YYYY`.
6. Конвертировать ставку: убрать пробелы и NBSP, заменить десятичную запятую на точку, привести к `float`.
7. Отсортировать наблюдения по дате по возрастанию.
8. Проверить отсутствие дублей по дате.
9. Проверить, что строк больше нуля.
10. Проверить диапазон ставки `0..50`.

Если `table.data` найдена и валидна, она является primary parser source.

## Highcharts fallback и cross-check

На странице может присутствовать JS-конфигурация Highcharts:

```text
settings.xAxis.categories = [...]
settings.series[0].data = [...]
settings.series[0].name = "Значение ключевой ставки"
```

Highcharts policy:

1. Не использовать Highcharts как primary source, если доступна валидная `table.data`.
2. Использовать Highcharts как fallback, если `table.data` отсутствует или невалидна.
3. Использовать Highcharts как cross-check, если `table.data` найдена.
4. Не парсить весь `settings` object как строгий JSON.
5. Извлекать только массивы `categories` и `data`.

Cross-check должен сравнить:

- количество наблюдений;
- граничные даты;
- значения ставок по совпадающим датам.

При расхождении таблицы и Highcharts parser должен завершаться понятной ошибкой или фиксировать blocker warning в QA, а не молча выбирать один источник.

## Daily source copy

Daily source copy является нормализованной копией формы сайта Банка России, а не аналитической таблицей.

Путь:

```text
data/processed/reference/cbr_key_rate_daily.csv
```

CSV должен содержать строго две колонки и только их:

```text
date,value
```

Обязательные поля:

| Поле | Тип | Nullable | Правило |
|---|---|---:|---|
| `date` | date | no | Дата наблюдения, ISO `YYYY-MM-DD`. |
| `value` | number | no | Значение ключевой ставки, проценты годовых. |

Daily CSV не должен содержать:

- `inflation`;
- `inflation_yoy`;
- `inflation_target`;
- `key_rate_max_pct`;
- `key_rate_min_pct`;
- `key_rate_avg_pct`;
- `source_url`;
- `retrieved_at`.

Файл `data/processed/reference/cbr_key_rate_daily.csv` является generated artifact и не коммитится.

## Daily metadata

Если нужно сохранить provenance, он хранится отдельно:

```text
data/processed/reference/cbr_key_rate_daily.meta.json
```

Разрешенные поля metadata:

| Поле | Тип | Nullable | Правило |
|---|---|---:|---|
| `source_url` | string | no | Фактический URL страницы Банка России с параметрами периода. |
| `from_date` | date | no | Начало requested period, ISO `YYYY-MM-DD`. |
| `to_date` | date | no | Конец requested period, ISO `YYYY-MM-DD`. |
| `retrieved_at` | datetime | no | UTC-время получения источника. |
| `page_last_modified` | string | yes | HTTP Last-Modified, если доступен. |
| `html_sha256` | string | yes | SHA256 HTML-снимка, если source web/html. |
| `row_count` | integer | no | Количество строк в daily CSV. |
| `parser` | string | no | `html_table` или `highcharts_fallback`. |

Metadata JSON является generated artifact и не коммитится.

## Monthly derived view

Monthly derived view строится только из daily source copy и используется для графика.

Путь:

```text
data/processed/reference/cbr_key_rate_monthly.csv
```

Правило выбора значения:

```text
last_available_observation_in_month
```

То есть для каждого месяца выбирается последняя доступная дата наблюдения внутри месяца и значение `value` на эту дату.

Запрещено использовать:

- максимум месяца;
- минимум месяца;
- среднее месяца;
- первое значение месяца;
- интерполяцию пропусков.

Обязательные поля monthly output:

| Поле | Тип | Nullable | Правило |
|---|---|---:|---|
| `period_month` | date | no | Первый день месяца, ISO `YYYY-MM-01`. |
| `period_label` | string | no | Русская подпись месяца, например `Июн-26`. |
| `key_rate_month_end_pct` | number | no | Ставка на последний доступный день месяца. |
| `key_rate_date` | date | no | Фактическая дата выбранного daily observation. |
| `key_rate_source_rule` | string | no | Всегда `last_available_observation_in_month`. |
| `key_rate_month_is_partial` | boolean | no | `true`, если месяц неполный относительно requested `to_date`. |

Monthly CSV не должен содержать provenance-поля `source_url`, `retrieved_at`, `page_last_modified`, `html_sha256` и `row_count`. Эти сведения остаются в daily metadata.

Файл `data/processed/reference/cbr_key_rate_monthly.csv` является generated artifact и не коммитится.

## Chart integration

График `ofz_pd_yield_key_rate` должен использовать monthly field:

```text
key_rate_month_end_pct
```

Допустимый временный compatibility alias:

```text
key_rate_pct = key_rate_month_end_pct
```

Chart-facing export должен содержать:

```text
period_month
period_label
ofz_pd_yield_min_pct
ofz_pd_yield_max_pct
key_rate_month_end_pct
key_rate_date
key_rate_source_rule
key_rate_month_is_partial
```

Hover/note графика должны явно сообщать:

```text
Ключевая ставка Банка России указана на последний доступный день месяца.
```

Для неполного месяца:

```text
Месяц неполный: значение на <key_rate_date>.
```

## Fallback XLSX

XLSX допускается только как временный manual fallback до завершения web parser или при недоступности сайта Банка России.

Fallback не меняет целевую модель хранения:

- daily source copy остается `date,value`;
- monthly derived view строится по `last_available_observation_in_month`;
- inflation-поля не входят в контракт key rate;
- raw XLSX не добавляется в Git без отдельного approval.

## QA expectations

Fixture-based parser smoke должен проверять:

- fixture `scripts/qa/fixtures/cbr/key_rate_page_2019_2026.html`;
- smoke runner `scripts/qa/cbr_key_rate_parser_smoke.py`;
- URL builder для `cbr.ru/hd_base/KeyRate/`;
- parser `table.data`;
- headers `Дата` и `Ставка`;
- десятичную запятую;
- сортировку по возрастанию;
- daily CSV ровно с колонками `date,value`;
- отсутствие в daily CSV колонок `inflation`, `inflation_yoy`, `inflation_target`, `source_url`, `retrieved_at`;
- metadata JSON только с разрешенными provenance-полями;
- Highcharts fallback/cross-check;
- monthly rule `last_available_observation_in_month`;
- отсутствие monthly max/min/avg/first aggregations;
- partial month flag;
- dry-run без записи CSV;
- понятную ошибку для пустой или malformed таблицы.

Live web dry-run допускается как отдельная проверка. Если сайт Банка России недоступен, это фиксируется как ограничение live-проверки, но не блокирует fixture-based smoke.
