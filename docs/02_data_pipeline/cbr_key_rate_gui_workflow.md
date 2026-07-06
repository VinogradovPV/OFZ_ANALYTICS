# GUI workflow ключевой ставки Банка России

Дата актуализации: 2026-07-06.

## Где находится вкладка

В desktop GUI OFZ Analytics workflow ключевой ставки Банка России вынесен на вкладку `Банк России`. Она расположена сразу после вкладки `Исходные данные Минфина` и использует существующий parser:

```text
scripts/reference_data/cbr_key_rate.py
```

Вкладка не создает новый источник данных и не меняет contract хранения. Она является GUI-обвязкой для уже зафиксированной модели:

- raw daily source copy: `data/raw/cbr/key_rate_inflation/latest/cbr_key_rate_daily.csv`;
- raw metadata: `data/raw/cbr/key_rate_inflation/latest/cbr_key_rate_daily.meta.json`;
- raw registry: `data/raw/cbr/key_rate_inflation/registry/cbr_key_rate_registry.csv`;
- raw latest registry JSON: `data/raw/cbr/key_rate_inflation/registry/cbr_key_rate_registry_latest.json`.

## Безопасные действия

Безопасные кнопки ничего не записывают в `data/raw/cbr/key_rate_inflation/`:

- `Проверить сайт Банка России` - live dry-run `--source web --dry-run`;
- `Проверить HTML fixture` - offline dry-run `--source html-file --dry-run`;
- `Проверить XLSX fallback` - аварийная проверка `--source xlsx --dry-run`.

Эти действия можно запускать перед обновлением raw dataset и для диагностики недоступности сайта.

## Обновление raw dataset

Кнопка `Обновить ключевую ставку` запускает web parser без `--dry-run` и требует точного подтверждения:

```text
UPDATE_CBR_KEY_RATE
```

После подтверждения GUI выполняет команду вида:

```powershell
.\.venv\Scripts\python.exe scripts\reference_data\cbr_key_rate.py --source web --from-date 01.01.2019 --to-date 02.07.2026 --download --confirm UPDATE_CBR_KEY_RATE ...
```

Update пишет controlled raw files:

```text
data/raw/cbr/key_rate_inflation/latest/cbr_key_rate_daily.csv
data/raw/cbr/key_rate_inflation/latest/cbr_key_rate_daily.meta.json
data/raw/cbr/key_rate_inflation/registry/cbr_key_rate_registry.csv
data/raw/cbr/key_rate_inflation/registry/cbr_key_rate_registry_latest.json
```

Эти файлы являются generated artifacts и не коммитятся.

## Статус источника

Блок `Статус источника` читает raw latest CSV, raw latest metadata JSON и registry. Если raw latest еще не создан, GUI показывает missing raw dataset и не падает.

Если files существуют, GUI показывает:

- latest date;
- latest value;
- row count;
- parser;
- html_sha256;
- source_url;
- paths до latest/meta/registry.

## График ОФЗ-ПД + ключевая ставка

После обновления raw dataset можно открыть график кнопкой `Открыть график ОФЗ-ПД + ставка`. GUI открывает файл:

```text
outputs/charts/yield/ofz_pd/ofz_pd_yield_key_rate_<suffix>.html
```

Если график еще не создан, сначала запустите pipeline с нужными параметрами report scope.

## Artifact policy

Не коммитятся:

- raw latest CSV/meta и registry;
- generated charts и exports в `outputs/`;
- raw XLSX fallback без отдельного approval.

Default source registry policy не меняется: `source-registry-mode=warn`, `allow-legacy-raw=true`.
