# Контракт источника ключевой ставки Банка России

Дата актуализации: 2026-07-02.

## Назначение

Этот контракт фиксирует источник, parser policy и monthly normalization для ключевой ставки Банка России в OFZ Analytics. Контракт нужен для последующей реализации web parser и для графика `ofz_pd_yield_key_rate`.

Текущая реализация pipeline может временно использовать ручной XLSX fallback. После внедрения web parser primary source должен соответствовать этому документу.

## Primary source

Основной источник:

```text
https://cbr.ru/hd_base/KeyRate/
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

Parser должен сохранять фактический `source_url` в output metadata.

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

## Daily output

Daily output содержит одно наблюдение на дату изменения ключевой ставки.

Обязательные поля:

| Поле | Тип | Nullable | Правило |
|---|---|---:|---|
| `key_rate_date` | date | no | Дата наблюдения, ISO `YYYY-MM-DD`. |
| `key_rate_pct` | number | no | Значение ключевой ставки, проценты годовых. |
| `source_parser` | string | no | `html_table`, `highcharts_fallback` или `xlsx_fallback`. |
| `source_url` | string | yes | URL страницы ЦБ для web/html source. |
| `source_retrieved_at` | datetime | yes | UTC-время получения источника. |
| `source_page_last_modified` | string | yes | HTTP Last-Modified, если доступен. |
| `source_html_sha256` | string | yes | SHA256 HTML-снимка, если source web/html. |
| `source_row_count` | integer | no | Количество строк source parser. |

Daily CSV является generated artifact и не коммитится.

## Monthly normalization

Для помесячного графика и chart data используется правило:

```text
last_available_observation_in_month
```

То есть для каждого месяца выбирается последняя доступная дата наблюдения в этом месяце и ставка на эту дату.

Запрещено использовать:

- максимум месяца;
- минимум месяца;
- среднее месяца;
- первое значение месяца;
- интерполяцию пропусков.

Если отчетная дата попадает внутрь месяца и в источнике есть только часть месяца, строка помечается как partial.

## Monthly output

Обязательные поля monthly output:

| Поле | Тип | Nullable | Правило |
|---|---|---:|---|
| `period_month` | date | no | Первый день месяца, ISO `YYYY-MM-01`. |
| `period_label` | string | no | Русская подпись месяца, например `Июн-26`. |
| `key_rate_month_end_pct` | number | no | Ставка на последний доступный день месяца. |
| `key_rate_date` | date | no | Фактическая дата выбранного daily observation. |
| `key_rate_source_rule` | string | no | Всегда `last_available_observation_in_month`. |
| `key_rate_month_is_partial` | boolean | no | `true`, если месяц неполный относительно requested `to-date`. |
| `source_url` | string | yes | URL страницы ЦБ или HTML source. |
| `source_retrieved_at` | datetime | yes | UTC-время получения source. |
| `source_page_last_modified` | string | yes | HTTP Last-Modified, если доступен. |
| `source_html_sha256` | string | yes | SHA256 HTML-снимка, если source web/html. |
| `source_row_count` | integer | no | Количество строк source parser. |

Monthly CSV является generated artifact и не коммитится.

## Chart integration

График `ofz_pd_yield_key_rate` должен использовать monthly key rate field:

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

XLSX допускается только как fallback/manual source до завершения web parser или при недоступности сайта Банка России.

Ожидаемые колонки:

```text
Дата
Ключевая ставка, % годовых
Инфляция, % г/г
Цель по инфляции
```

Output должен помечать такой источник:

```text
source_parser=xlsx_fallback
```

Raw XLSX не добавляется в Git без отдельного approval.

## QA expectations

Fixture-based parser smoke должен проверять:

- URL builder для `cbr.ru/hd_base/KeyRate/`;
- parser `table.data`;
- headers `Дата` и `Ставка`;
- десятичную запятую;
- сортировку по возрастанию;
- Highcharts fallback/cross-check;
- monthly rule `last_available_observation_in_month`;
- partial month flag;
- dry-run без записи CSV;
- понятную ошибку для пустой или malformed таблицы.

Live web dry-run допускается как отдельная проверка. Если сайт ЦБ недоступен, это фиксируется как ограничение live-проверки, но не блокирует fixture-based smoke.
