# GUI workflow ключевой ставки Банка России

Дата актуализации: 2026-07-03.

## Где находится вкладка

В desktop GUI OFZ Analytics workflow ключевой ставки Банка России вынесен на вкладку `Банк России`. Она расположена сразу после вкладки `Исходные данные Минфина` и использует существующий parser:

```text
scripts/reference_data/cbr_key_rate.py
```

Вкладка не создает новый источник данных и не меняет contract хранения. Она является GUI-обвязкой для уже зафиксированной модели:

- daily source copy: `data/processed/reference/cbr_key_rate_daily.csv`;
- metadata: `data/processed/reference/cbr_key_rate_daily.meta.json`;
- monthly derived view: `data/processed/reference/cbr_key_rate_monthly.csv`.

## Безопасные действия

Безопасные кнопки ничего не записывают в `data/processed/reference/`:

- `Проверить сайт Банка России` - live dry-run `--source web --dry-run`;
- `Проверить HTML fixture` - offline dry-run `--source html-file --dry-run`;
- `Проверить XLSX fallback` - аварийная проверка `--source xlsx --dry-run`.

Эти действия можно запускать перед обновлением reference datasets и для диагностики недоступности сайта.

## Обновление reference datasets

Кнопка `Обновить ключевую ставку` запускает web parser без `--dry-run` и требует точного подтверждения:

```text
UPDATE_CBR_KEY_RATE
```

После подтверждения GUI выполняет команду вида:

```powershell
.\.venv\Scripts\python.exe scripts\reference_data\cbr_key_rate.py --source web --from-date 01.01.2019 --to-date 02.07.2026 ...
```

Update пишет generated files:

```text
data/processed/reference/cbr_key_rate_daily.csv
data/processed/reference/cbr_key_rate_daily.meta.json
data/processed/reference/cbr_key_rate_monthly.csv
```

Эти файлы являются generated artifacts и не коммитятся.

## Статус источника

Блок `Статус источника` читает daily CSV, monthly CSV и metadata JSON. Если files еще не созданы, GUI показывает `Reference datasets еще не созданы` и не падает.

Если files существуют, GUI показывает:

- latest date;
- latest value;
- row count;
- parser;
- html_sha256;
- source_url;
- paths до daily/monthly/meta.

## График ОФЗ-ПД + ключевая ставка

После обновления reference datasets можно открыть график кнопкой `Открыть график ОФЗ-ПД + ставка`. GUI открывает файл:

```text
outputs/charts/yield/ofz_pd/ofz_pd_yield_key_rate_<suffix>.html
```

Если график еще не создан, сначала запустите pipeline с нужными параметрами report scope.

## Artifact policy

Не коммитятся:

- `data/processed/reference/cbr_key_rate_daily.csv`;
- `data/processed/reference/cbr_key_rate_daily.meta.json`;
- `data/processed/reference/cbr_key_rate_monthly.csv`;
- generated charts и exports в `outputs/`;
- raw XLSX fallback без отдельного approval.

Default source registry policy не меняется: `source-registry-mode=warn`, `allow-legacy-raw=true`.
