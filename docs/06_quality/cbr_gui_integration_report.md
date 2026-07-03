# Отчет по интеграции CBR key rate workflow в GUI

Дата проверки: 2026-07-03.

## Что добавлено

- В `GuiState` добавлены отдельные CBR-поля: период запроса, URL override, HTML fixture, XLSX fallback, timeout, retries, save HTML snapshot и no-network режим.
- В `ActionRegistry` добавлены allowlisted actions:
  - `cbr-key-rate-web-dry`;
  - `cbr-key-rate-web-update`;
  - `cbr-key-rate-html-fixture`;
  - `cbr-key-rate-xlsx-fallback`.
- В desktop GUI добавлена вкладка `Банк России` сразу после `Исходные данные Минфина`.
- Вкладка `Банк России` сделана прокручиваемой, чтобы нижние кнопки не обрезались при стандартной высоте окна.
- Добавлен status reader для `data/processed/reference/cbr_key_rate_daily.csv`, `data/processed/reference/cbr_key_rate_monthly.csv` и `data/processed/reference/cbr_key_rate_daily.meta.json`.
- Добавлены pytest-тесты parser contract и GUI action builder.
- Добавлена документация workflow: `docs/02_data_pipeline/cbr_key_rate_gui_workflow.md`.

## Выполненные проверки

```powershell
.\.venv\Scripts\python.exe -m compileall scripts
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe scripts\qa\gui_launcher_smoke.py
.\.venv\Scripts\python.exe -m scripts.gui_launcher.app --smoke-ui
.\.venv\Scripts\python.exe scripts\qa\cbr_key_rate_parser_smoke.py
.\.venv\Scripts\python.exe scripts\reference_data\cbr_key_rate.py --source html-file --html-file scripts\qa\fixtures\cbr\key_rate_page_2019_2026.html --dry-run
.\.venv\Scripts\ofz-run.exe --report-date 2026-07-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --source-registry-mode warn --allow-legacy-raw
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-07-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Результат: проверки прошли успешно. Visual regression внутри fast quality gate использовал fallback, потому что screenshot backend недоступен в managed-среде.

## Generated files не коммитились

Не коммитились generated artifacts:

- `data/processed/reference/cbr_key_rate_daily.csv`;
- `data/processed/reference/cbr_key_rate_daily.meta.json`;
- `data/processed/reference/cbr_key_rate_monthly.csv`;
- `data/processed/`;
- `outputs/charts/`;
- `outputs/exports/`;
- `outputs/dashboards/`;
- `outputs/reports/`;
- `.ofz_launcher/`;
- raw XLSX fallback.

## Что осталось следующим этапом

- При необходимости выполнить live web dry-run CBR из обычного PowerShell окружения оператора.
- После подтвержденного live dry-run выполнить update через GUI с token `UPDATE_CBR_KEY_RATE`.
- Затем запустить pipeline и визуально проверить график `ofz_pd_yield_key_rate_<suffix>.html`.

Default source registry policy не менялась: `source-registry-mode=warn`, `allow-legacy-raw=true`.
