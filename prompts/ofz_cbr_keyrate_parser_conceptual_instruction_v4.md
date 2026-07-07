# OFZ_ANALYTICS: уточненная инструкция Codex по ключевой ставке ЦБ, GUI и UTF-8 — v4

Дата: 2026-07-02
Проект: `OFZ_ANALYTICS`
Рабочая директория:

```powershell
C:\Users\Rockaudit\LLM_CHAT\ofz_analytics
```

## 0. Главные уточнения

Эта версия заменяет предыдущую инструкцию. Из scope удаляется все, что связано с инфляцией.

Codex должен реализовать **только ключевую ставку Банка России**:

```text
IN SCOPE:
- ключевая ставка Банка России;
- HTML-таблица `table.data` страницы CBR KeyRate;
- daily source copy в форме сайта: дата / значение;
- monthly derived view для графика: значение на последний доступный день месяца;
- график ОФЗ-ПД + ключевая ставка;
- исправление labels / boxplot / GUI wrappers / UTF-8.

OUT OF SCOPE:
- инфляция;
- цель по инфляции;
- любые поля inflation_yoy / inflation_target;
- XLSX как основной источник;
- месячные max/min/avg ключевой ставки.
```

Фундаментальное правило данных:

```text
Выгруженная информация хранится в строгом соответствии с формой на сайте Банка России:
date,value
```

То есть daily файл — это не аналитическая таблица, а нормализованная копия данных сайта. Аналитическое правило применяется только при построении графика: для каждого месяца брать ключевую ставку на последний доступный день этого месяца.

---

## 1. Проверенные факты по HTML странице Банка России

Из предоставленного HTML страницы `https://cbr.ru/hd_base/KeyRate/?UniDbQuery.Posted=True&UniDbQuery.From=01.01.2019&UniDbQuery.To=02.07.2026`:

```text
1. Форма использует параметры:
   - UniDbQuery.Posted=True
   - UniDbQuery.From=01.01.2019
   - UniDbQuery.To=02.07.2026

2. Datepicker указывает доступный диапазон:
   - data-min-date="17.09.2013"
   - data-max-date="02.07.2026"

3. Preferred source — HTML-таблица:
   <table class="data">
     <th>Дата</th>
     <th>Ставка</th>

4. Таблица идет от новых дат к старым:
   02.07.2026, 01.07.2026, 30.06.2026, ...

5. Числа используют русскую десятичную запятую:
   14,25

6. На странице есть Highcharts settings:
   - xAxis.categories содержит даты;
   - series[0].data содержит значения;
   - series[0].name = "Значение ключевой ставки".

7. Highcharts не должен быть primary source. Его можно использовать только как fallback/cross-check.
```

---

## 2. Базовые правила выполнения

### 2.1. Рабочая директория

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics
```

### 2.2. Git только outside sandbox

Все `git` команды выполнять только outside sandbox.

### 2.3. GitHub Actions не проверять

Не выполнять:

```powershell
gh run list --limit 5
gh run view --log
```

В финальном ответе не писать `GitHub Actions status`.

### 2.4. Preflight

```powershell
git status --short --branch
git log --oneline -10
git ls-files -v | Select-String '^S '
Get-Content .git\info\exclude
```

### 2.5. Не использовать

```powershell
git add .
```

### 2.6. Artifact guard

```powershell
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|outputs/reports/source_acquisition|data/processed|logs|releases|docm|tmp|temp|crdownload|part|data/raw/minfin/ofz_auction_results/versions|.ofz_launcher"
```

Если вывод не пустой — снять запрещенные файлы из staging.

---

## 3. Этап A — UTF-8 правило Windows / PowerShell

### Цель

Внедрить правило UTF-8 по образцу проекта Expense_Splitter.

### Требования

Добавить в документацию и wrappers:

```powershell
chcp 65001 | Out-Null
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
```

Проверить subprocess runner:

```text
scripts/gui_launcher/command_runner.py
scripts/reference_data/cbr_key_rate.py
```

Subprocess env должен содержать:

```text
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
```

Чтение stdout/stderr:

```python
encoding="utf-8"
errors="replace"
```

### Проверка

```powershell
.\.venv\Scripts\python.exe scripts\qa\check_text_encoding.py
```

---

## 4. Этап B — починить запуск GUI из корня проекта

### Проблема

Команда:

```powershell
ofz-gui.exe
```

из корня проекта не работает, если `.venv\Scripts` не находится в `PATH`.

### Решение

Добавить root wrappers:

```text
run-gui.ps1
ofz-gui.cmd
```

`run-gui.ps1` должен:

```text
- включать UTF-8 bootstrap;
- искать `.venv\Scripts\ofz-gui.exe`;
- если entry point отсутствует, подсказать:
  .\.venv\Scripts\python.exe -m pip install -e .
- передавать аргументы в GUI.
```

`ofz-gui.cmd` должен делать то же для cmd.exe.

### Документация

В README и `docs/07_operations/gui_launcher.md` явно написать:

```text
Из корня проекта используйте:
  .\run-gui.ps1
  .\ofz-gui.cmd
  .\.venv\Scripts\ofz-gui.exe

Голая команда `ofz-gui.exe` работает только после активации venv или если `.venv\Scripts` добавлен в PATH.
```

### Smoke

Создать:

```text
scripts/qa/gui_launcher_wrapper_smoke.py
```

Проверить:

```text
1. run-gui.ps1 существует.
2. ofz-gui.cmd существует.
3. Оба содержат PYTHONUTF8 и PYTHONIOENCODING.
4. Оба ссылаются на .venv\Scripts\ofz-gui.exe.
5. Нет абсолютного user path.
```

---

## 5. Этап C — удалить reference-график / reference-слайд

### Цель

Удалить PPTX/PNG/reference-график, на основании которого проектировался стиль. В проекте остается только текстовая visual policy.

### Найти

```powershell
git ls-files | Select-String "Слайд доходность|reference.*key.*rate|ofz.*key.*rate.*reference|pptx|ppt"
Get-ChildItem -Recurse -File | Where-Object {
  $_.Name -match "Слайд доходность|reference.*key.*rate|ofz.*key.*rate.*reference|pptx|ppt"
} | Select-Object FullName
```

### Удалить

Tracked:

```powershell
git rm <path>
```

Untracked:

```powershell
Remove-Item <path>
```

### Оставить

```text
docs/04_visualization/line_marker_chart_style.md
```

---

## 6. Этап D — уточненный результат этапа 4: модель хранения key rate

### 6.1. Цель

Этап 4 должен дать строгую модель данных:

```text
1. daily source copy = точная форма сайта Банка России;
2. monthly derived view = только для графика.
```

### 6.2. Основной URL

```text
https://cbr.ru/hd_base/KeyRate/?UniDbQuery.Posted=True&UniDbQuery.From=<DD.MM.YYYY>&UniDbQuery.To=<DD.MM.YYYY>
```

### 6.3. Preferred parser source

Primary source:

```html
<table class="data">
  <th>Дата</th>
  <th>Ставка</th>
</table>
```

### 6.4. Daily source copy

Файл:

```text
data/processed/reference/cbr_key_rate_daily.csv
```

Колонки строго:

```text
date
value
```

Семантика:

```text
date  = дата с сайта Банка России, ISO YYYY-MM-DD
value = значение ключевой ставки с сайта Банка России
```

Запрещено добавлять в daily CSV:

```text
inflation
inflation_yoy
inflation_target
key_rate_max_pct
key_rate_min_pct
key_rate_avg_pct
source_url
retrieved_at
```

Если нужна provenance, хранить отдельно:

```text
data/processed/reference/cbr_key_rate_daily.meta.json
```

Допустимые поля metadata:

```text
source_url
from_date
to_date
retrieved_at
page_last_modified
html_sha256
row_count
parser
```

`data/processed/reference/` не коммитить.

### 6.5. Monthly derived view для графика

Файл:

```text
data/processed/reference/cbr_key_rate_monthly.csv
```

Колонки:

```text
period_month
period_label
key_rate_month_end_pct
key_rate_date
key_rate_source_rule
key_rate_month_is_partial
```

Правило:

```text
Для каждого месяца взять последнюю доступную дату месяца из daily data и значение `value` на эту дату.
```

Запрещено:

```text
max(value)
min(value)
avg(value)
first(value)
```

`key_rate_source_rule`:

```text
last_available_observation_in_month
```

### 6.6. Data contract

Создать/обновить:

```text
docs/02_data_contracts/cbr_key_rate_contract.md
```

Обязательные формулировки:

```text
- Scope: only Bank of Russia key rate.
- Out of scope: inflation and inflation target.
- Daily storage: exact site-form data `date,value`.
- Monthly chart value: last available observation in month.
- Preferred source: `table.data`.
- Highcharts: fallback/cross-check only.
- Processed CSV not committed.
```

---

## 7. Этап E — web parser ключевой ставки

### Parser file

```text
scripts/reference_data/cbr_key_rate.py
```

### CLI

```text
--source web|html-file|xlsx
--from-date DD.MM.YYYY
--to-date DD.MM.YYYY
--url
--html-file
--input-file
--daily-output-csv
--daily-meta-json
--monthly-output-csv
--dry-run
--timeout-seconds
--retries
--user-agent
--save-html-snapshot
```

Defaults:

```text
--source web
--from-date 01.01.2019
--to-date 02.07.2026
--daily-output-csv data/processed/reference/cbr_key_rate_daily.csv
--daily-meta-json data/processed/reference/cbr_key_rate_daily.meta.json
--monthly-output-csv data/processed/reference/cbr_key_rate_monthly.csv
```

### Table parser

```text
1. Select exactly one `table.data`.
2. Validate headers: Дата, Ставка.
3. Parse date as `%d.%m.%Y`.
4. Parse value: replace comma with dot.
5. Sort ascending.
6. Validate no duplicate dates.
7. Validate value range 0..50.
8. Write daily rows as exactly `date,value`.
```

### Highcharts fallback/cross-check

```text
1. Extract only `categories` and first `data` array.
2. Do not parse full JS settings as JSON.
3. Use as fallback if table missing.
4. Use as cross-check if table exists.
```

### XLSX fallback

`--source xlsx` остается emergency fallback только для ключевой ставки.

Accepted columns:

```text
Дата
Ключевая ставка, % годовых
```

Игнорировать, если встречаются:

```text
Инфляция, % г/г
Цель по инфляции
```

В output их не включать.

---

## 8. Этап F — QA parser fixtures

### Fixture

```text
scripts/qa/fixtures/cbr/key_rate_page_2019_2026.html
```

Можно использовать full HTML или минимальный fixture, но он должен сохранять:

```text
- form date filters;
- table.data;
- Highcharts categories/data sample.
```

### Smoke

```text
scripts/qa/cbr_key_rate_parser_smoke.py
```

Проверки:

```text
1. URL builder produces expected CBR URL.
2. table.data parses successfully.
3. headers are Дата / Ставка.
4. decimal comma parses correctly.
5. daily output columns are exactly date,value.
6. daily output contains no inflation columns.
7. output sorted ascending.
8. Highcharts cross-check works.
9. monthly aggregation selects last available observation in month.
10. March 2026: key_rate_date=2026-03-31, key_rate_month_end_pct=15.00.
11. June 2026: key_rate_date=2026-06-30, key_rate_month_end_pct=14.25.
12. July 2026 partial: key_rate_date=2026-07-02, key_rate_month_is_partial=true.
13. dry-run does not write CSV.
```

---

## 9. Этап G — график ОФЗ-ПД + ключевая ставка

### Field policy

Не использовать:

```text
key_rate_max_pct
```

Использовать:

```text
key_rate_month_end_pct
```

### Chart export columns

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

### Chart note

```text
Ключевая ставка Банка России указана на последний доступный день месяца.
```

### Формат значений ключевой ставки

На графике и в hover:

```text
2 знака после запятой
```

Примеры:

```text
21.00
15.50
15.00
14.25
```

Не допускать:

```text
21.0
15.5
15.0
14.3
```

CSV остается numeric.

---

## 10. Этап H — исправить перекрытие labels

Использовать collision-aware annotations, а не только `trace.textposition`.

Helper:

```text
scripts/charts/line_marker_style.py
```

Функции:

```text
add_line_marker_trace(...)
apply_line_marker_layout(...)
build_collision_safe_value_annotations(...)
detect_label_collisions(...)
format_key_rate_pct(...)
```

Правило collision:

```text
threshold = max(0.25 п.п., 2.5% диапазона Y)
```

Smoke:

```text
scripts/qa/line_marker_label_collision_smoke.py
```

Проверить:

```text
- March 2026 labels have different offsets/lanes;
- key rate labels use 2 decimals;
- HTML uses annotations for value labels.
```

---

## 11. Этап I — исправить OFZ-PD single-period boxplot

График:

```text
yield_boxplot_ofz_pd_year_cumulative_2026-01-01_retrospective_1
```

Проблема:

```text
схлопнут в вертикальную линию, single-period layout не читается.
```

Сделать single-period fallback:

```text
- jittered strip + box или strip + min/median/max ticks;
- marker opacity 0.45-0.60;
- jitter >= 0.45;
- explicit box width;
- expanded x-axis range;
- summary annotations near category, not right edge.
```

Regression:

```text
scripts/qa/ofz_pd_boxplot_single_period_regression.py
```

---

## 12. Проверки

### UTF-8 / wrappers

```powershell
.\.venv\Scripts\python.exe scripts\qa\check_text_encoding.py
.\.venv\Scripts\python.exe scripts\qa\gui_launcher_wrapper_smoke.py
```

### Parser

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\reference_data\cbr_key_rate.py scripts\qa\cbr_key_rate_parser_smoke.py
.\.venv\Scripts\python.exe scripts\reference_data\cbr_key_rate.py --source html-file --html-file scripts\qa\fixtures\cbr\key_rate_page_2019_2026.html --dry-run
.\.venv\Scripts\python.exe scripts\qa\cbr_key_rate_parser_smoke.py
```

### Live web dry-run

```powershell
.\.venv\Scripts\python.exe scripts\reference_data\cbr_key_rate.py --source web --from-date 01.01.2019 --to-date 02.07.2026 --dry-run
```

Если сайт ЦБ недоступен, зафиксировать failure, но fixture smoke остается обязательным.

### Chart / pipeline

```powershell
.\.venv\Scripts\python.exe scripts\reference_data\cbr_key_rate.py --source web --from-date 01.01.2019 --to-date 02.07.2026

.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --source-registry-mode warn --allow-legacy-raw

.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-01-01 --retrospective-years 1 --period-type year --aggregation-mode cumulative

.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative

.\.venv\Scripts\python.exe scripts\qa\line_marker_label_collision_smoke.py
.\.venv\Scripts\python.exe scripts\qa\ofz_pd_boxplot_single_period_regression.py
.\.venv\Scripts\python.exe scripts\qa\ofz_pd_yield_metrics_regression.py

.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

### Compile

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
```

---

## 13. Документация

Обновить:

```text
docs/02_data_contracts/cbr_key_rate_contract.md
docs/04_visualization/line_marker_chart_style.md
docs/04_visualization/visualization_strategy.md
docs/07_operations/windows_utf8_powershell_setup.md
docs/07_operations/gui_launcher.md
docs/00_project/post_release_roadmap_v2.md
docs/00_project/post_p3_optimization_progress_report.md
docs/06_quality/manual_checks_log.md
docs/07_operations/production_runbook.md
README.md
```

Обязательно указать:

```text
1. Парсится только ключевая ставка.
2. Инфляция вне scope.
3. Daily CBR key rate storage = date,value.
4. Monthly chart value = last available observation in month.
5. Key rate labels use 2 decimals.
6. GUI wrappers added.
7. UTF-8 setup required.
```

---

## 14. Staging

Allowed scope:

```powershell
git add run-gui.ps1
git add ofz-gui.cmd
git add scripts/reference_data/cbr_key_rate.py
git add scripts/reference_data/__init__.py
git add scripts/charts/line_marker_style.py
git add scripts/charts/chart_metadata.py
git add scripts/06_build_charts.py
git add scripts/10_build_monthly_charts.py
git add scripts/html_chart_qa.py
git add scripts/visual_regression.py
git add scripts/qa/gui_launcher_wrapper_smoke.py
git add scripts/qa/cbr_key_rate_parser_smoke.py
git add scripts/qa/line_marker_label_collision_smoke.py
git add scripts/qa/ofz_pd_boxplot_single_period_regression.py
git add scripts/qa/fixtures/cbr/key_rate_page_2019_2026.html
git add docs/02_data_contracts/cbr_key_rate_contract.md
git add docs/04_visualization/line_marker_chart_style.md
git add docs/04_visualization/visualization_strategy.md
git add docs/07_operations/windows_utf8_powershell_setup.md
git add docs/07_operations/gui_launcher.md
git add docs/00_project/post_release_roadmap_v2.md
git add docs/00_project/post_p3_optimization_progress_report.md
git add docs/06_quality/manual_checks_log.md
git add docs/07_operations/production_runbook.md
git add README.md
```

Если reference PPTX/PNG удален:

```powershell
git add -u
git diff --cached --name-only
```

Не stage:

```text
data/processed/reference/*.csv
data/processed/reference/*.json
outputs/
logs/
releases/
.ofz_launcher/
raw HTML snapshots outside test fixtures
```

Raw CBR XLSX только после отдельного approval.

---

## 15. Commit strategy

Рекомендуемый split:

```powershell
git commit -m "Add Windows GUI launch wrappers and UTF-8 setup"
git commit -m "Remove key rate reference chart artifact"
git commit -m "Add CBR key rate HTML table parser"
git commit -m "Integrate month-end key rate chart data"
git commit -m "Fix line marker labels and OFZ-PD boxplot"
```

Compact:

```powershell
git commit -m "Integrate CBR key rate parser and fix GUI/chart UX"
```

После commit:

```powershell
git push
git status --short --branch
git log --oneline -5
```

GitHub Actions не проверять.

---

## 16. Финальный ответ Codex

Codex должен ответить:

```text
1. Как исправлен запуск GUI.
2. Какие wrappers добавлены.
3. Как применено UTF-8 правило.
4. Удален ли reference PPTX/PNG.
5. Подтверждение: парсится только ключевая ставка, инфляция out of scope.
6. Какой parser source используется primary: table.data.
7. Как хранится daily data: date,value.
8. Как monthly key rate выбирает последний доступный день месяца.
9. Как исправлен формат ключевой ставки до 2 знаков.
10. Как исправлено перекрытие labels.
11. Как исправлен single-period OFZ-PD boxplot.
12. Какие checks выполнены.
13. Что не коммитилось: generated outputs, processed CSV/JSON, logs, releases.
14. Commit hash.
15. Push status.
```

## 17. Критерии готовности

```text
1. GUI запускается через .\run-gui.ps1 и .\ofz-gui.cmd.
2. UTF-8 setup documented and used.
3. Reference PPTX/PNG удален.
4. Parser читает только ключевую ставку из table.data.
5. Daily output строго date,value.
6. Inflation отсутствует в parser outputs/docs/tests.
7. Monthly key rate = last available observation in month.
8. Key-rate labels show 2 decimals.
9. March 2026 labels do not overlap.
10. Single-period OFZ-PD boxplot readable.
11. Fixture-based parser smoke does not require internet.
12. Generated artifacts not staged.
