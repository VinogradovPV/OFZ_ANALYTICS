# OFZ_ANALYTICS: пошаговая инструкция P3 modernization v6
## Полностью на русском, с командами для Codex и детальным P3.6

Дата актуализации: 2026-06-17.

---

## 0. Назначение документа

Эта инструкция заменяет v5.

Что исправлено:

```text
1. Документ полностью переведен на русский.
2. Для каждого этапа добавлены готовые команды для Codex.
3. Этап P3.6 детализирован до конкретных действий, CLI-режимов, проверок и критериев завершения.
4. Сохранено жесткое правило: все git/gh команды только outside sandbox.
5. Учтена HTML-структура страницы Минфина:
   section 66, page_66, ajax-pagination-content-10090-66, id_66.
```

---

## 1. Общие правила для всех этапов P3

### 1.1. Рабочая директория

Все команды проекта выполнять из корня:

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics
```

### 1.2. Git/GitHub

Все `git` и `gh` команды выполнять только outside sandbox.

Перед commit:

```powershell
git status --short
git diff --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|outputs/reports/source_acquisition|data/processed|logs|releases|docm|tmp|temp|crdownload|part|data/raw/minfin/ofz_auction_results/versions"
```

После push:

```powershell
gh run list --limit 5
```

Если текущий run упал:

```powershell
gh run view --log
```

### 1.3. Не коммитить

```text
outputs/
releases/
logs/
data/processed/
outputs/reports/source_acquisition/
data/raw/minfin/ofz_auction_results/versions/
temp downloads
*.tmp
*.part
*.crdownload
*.docm
```

### 1.4. Progress report

После каждого этапа обновлять:

```text
docs/00_project/p3_modernization_progress_report.md
```

---

# P3.1 - Skeleton source acquisition с HTML-aware parser

## Цель

Создать CLI `ofz-fetch-minfin`, который умеет строить dry-run план и парсить HTML-фикстуру Минфина без реального скачивания и без изменения raw.

## Создать/изменить файлы

Создать:

```text
scripts/source_acquisition/__init__.py
scripts/source_acquisition/minfin_fetch.py
scripts/source_acquisition/source_registry.py
scripts/source_acquisition/minfin_patterns.py
scripts/source_acquisition/path_planning.py
scripts/source_acquisition/minfin_html_parser.py
tests/fixtures/minfin_auction_page_section_66_sample.html
tests/fixtures/minfin_auction_candidates_expected.json
```

Опционально:

```text
scripts/qa/minfin_source_acquisition_smoke.py
```

Изменить:

```text
pyproject.toml
docs/00_project/p3_modernization_progress_report.md
docs/06_quality/manual_checks_log.md
docs/07_operations/minfin_source_acquisition.md
```

## Требования

Entry point:

```toml
ofz-fetch-minfin = "scripts.source_acquisition.minfin_fetch:main"
```

CLI options:

```text
--year
--mode monthly|annual-final|manual-import
--dry-run
--download
--url
--output-root
--manual-file
--no-network
--timeout-seconds
--retries
--user-agent
--confirm
--max-pages
--html-file
--save-html-snapshot
```

Реализовать функции:

```text
parse_minfin_auction_table_documents(html, base_url, page_number)
extract_pagination_info(html, section_id=66)
resolve_file_url(base_url, href)
parse_document_dates(card)
parse_as_of_date_from_title(title)
filter_candidates(records, year)
select_candidate(records, year, mode)
build_acquisition_plan(...)
```

Парсер должен:

```text
- выбирать только section_id=66;
- игнорировать sections 65/38/39;
- извлекать XLSX только из a.file_item;
- резолвить relative href через https://minfin.gov.ru;
- поддерживать page_66 pagination;
- monthly выбирать заголовок с "на DD.MM.YYYY";
- annual-final не требовать YYYY1231.
```

## Команда для Codex

```text
Выполни P3.1 Source acquisition skeleton с HTML-aware parser.

Не выполняй реальное скачивание.
Не создавай raw storage dirs.
Не меняй data/raw.
Не пиши registry в data/raw.
Не коммить generated outputs.

Создай package scripts/source_acquisition и CLI entry point:
ofz-fetch-minfin = "scripts.source_acquisition.minfin_fetch:main"

Добавь parser для HTML Минфина:
- target section id_66/page_66/ajax-pagination-content-10090-66;
- ignore sections 65/38/39;
- extract a.file_item XLSX links;
- resolve relative URLs;
- parse published_at/modified_at/as_of_date;
- select monthly and annual-final candidates.

Добавь --html-file dry-run mode и offline fixture.
Обнови progress report и manual_checks_log.
```

## Проверки

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\source_acquisition\minfin_fetch.py scripts\source_acquisition\minfin_html_parser.py scripts\source_acquisition\source_registry.py
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\ofz-fetch-minfin.exe --help
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --dry-run --no-network
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2025 --mode annual-final --dry-run --no-network
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --dry-run --html-file tests\fixtures\minfin_auction_page_section_66_sample.html
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2025 --mode annual-final --dry-run --html-file tests\fixtures\minfin_auction_page_section_66_sample.html
```

Если создан smoke:

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_source_acquisition_smoke.py
.\.venv\Scripts\python.exe scripts\qa\minfin_source_acquisition_smoke.py
```

## Commit

```powershell
git add scripts/source_acquisition tests/fixtures/minfin_auction_page_section_66_sample.html tests/fixtures/minfin_auction_candidates_expected.json scripts/qa/minfin_source_acquisition_smoke.py pyproject.toml docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md docs/07_operations/minfin_source_acquisition.md
git commit -m "Add HTML-aware Minfin source acquisition skeleton"
git push
```

Добавлять только реально измененные файлы.

## Критерии завершения

```text
- ofz-fetch-minfin --help работает.
- no-network dry-run работает.
- --html-file dry-run выбирает monthly/annual-final кандидатов.
- raw не изменен.
- generated artifacts не staged.
```

---

# P3.2 - Registry writer с HTML provenance

## Цель

Реализовать слой registry CSV/JSON и hash metadata без реального скачивания и без записи в настоящий raw storage.

## Создать/изменить файлы

Изменить:

```text
scripts/source_acquisition/source_registry.py
docs/02_data_contracts/minfin_source_registry_contract.md
docs/00_project/p3_modernization_progress_report.md
docs/06_quality/manual_checks_log.md
```

Создать:

```text
scripts/qa/minfin_source_registry_smoke.py
tests/fixtures/minfin_registry_sample.json
```

## Требования

Реализовать:

```text
RegistryRecord
RegistryStatus
compute_sha256(path)
get_file_size(path)
load_registry_csv(path)
load_registry_json(path)
write_registry_csv(path, records)
write_registry_json(path, records)
append_registry_record(path, record)
find_active_record(records, year, storage_role)
detect_hash_change(previous_record, candidate_sha256)
mark_superseded(records, superseded_sha256)
validate_registry_record(record)
```

Поля registry:

```text
source_name
source_url
page_title
link_text
file_name
year
publication_period
downloaded_at
source_last_modified
http_etag
http_last_modified
file_size_bytes
sha256
storage_role
is_active_for_pipeline
supersedes_sha256
change_detected
notes
section_id
page_param
page_number
document_id
document_page_url
document_title
published_at
modified_at
as_of_date
file_url
absolute_file_url
file_title
file_info
file_size_text
discovery_method
pagination_page_count
```

Storage roles:

```text
latest
version_snapshot
final
manual_candidate
observation
```

## Команда для Codex

```text
Выполни P3.2 Registry writer.

Не скачивай файлы.
Не пиши registry в настоящий data/raw/minfin.
Используй только temp fixtures.

Реализуй RegistryRecord и CSV/JSON read-write layer.
Добавь HTML provenance поля.
Добавь smoke test, который создает temp files, считает sha256, пишет CSV/JSON, читает обратно, проверяет unchanged/changed hash и active row selection.
Обнови контракт registry, progress report и manual_checks_log.
```

## Проверки

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\source_acquisition\source_registry.py
.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_source_registry_smoke.py
.\.venv\Scripts\python.exe scripts\qa\minfin_source_registry_smoke.py
.\.venv\Scripts\python.exe -m compileall -q scripts
```

## Commit

```powershell
git add scripts/source_acquisition/source_registry.py scripts/qa/minfin_source_registry_smoke.py tests/fixtures/minfin_registry_sample.json docs/02_data_contracts/minfin_source_registry_contract.md docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Add Minfin source registry writer"
git push
```

## Критерии завершения

```text
- CSV/JSON roundtrip работает.
- Hash changed/unchanged работает.
- Active row selection работает.
- HTML provenance поля поддержаны.
- Настоящий raw storage не изменен.
```

---

# P3.3 - Monthly acquisition implementation

## Цель

Реализовать controlled monthly download для текущего года с подтверждением.

## Создать/изменить файлы

Изменить:

```text
scripts/source_acquisition/minfin_fetch.py
scripts/source_acquisition/http_client.py
scripts/source_acquisition/minfin_html_parser.py
scripts/source_acquisition/minfin_patterns.py
scripts/source_acquisition/path_planning.py
scripts/source_acquisition/source_registry.py
docs/07_operations/minfin_source_acquisition.md
docs/00_project/p3_modernization_progress_report.md
docs/06_quality/manual_checks_log.md
```

Создать:

```text
scripts/qa/minfin_monthly_acquisition_smoke.py
```

## Требования

Реализовать:

```text
fetch_page(url, timeout_seconds, retries, user_agent)
download_file(url, temp_path, timeout_seconds, retries, user_agent)
extract_candidate_links(html, year)
filter_minfin_excel_links(links, year)
select_best_candidate(candidates, year, mode=monthly)
```

Monthly workflow:

```text
1. Fetch base page.
2. Parse section 66.
3. Read page_66 pagination count.
4. Fetch page_66=2..N.
5. Extract XLSX candidates only from section 66.
6. Select monthly candidate by max as_of_date.
7. Download selected absolute_file_url to temp path.
8. Validate .xlsx extension and filename year.
9. Compute sha256 and size.
10. Compare with current latest hash.
11. If unchanged: no version snapshot.
12. If changed: write versions/<year>/ snapshot and latest.
13. Update registry.
14. Write report to outputs/reports/source_acquisition/.
```

Real download requires:

```text
--download --confirm DOWNLOAD_MINFIN_SOURCE
```

Without confirm:

```text
exit non-zero
no mutation
```

## Команда для Codex

```text
Выполни P3.3 Monthly acquisition implementation.

Реализуй live monthly acquisition, но реальный download запускай только если пользователь отдельно разрешил.
Без confirm DOWNLOAD_MINFIN_SOURCE download должен блокироваться.

Используй section 66/page_66 pagination.
Скачивай только selected absolute_file_url.
Сначала temp download, потом validation, hash compare, затем promote.
Не оставляй partial files.
versions/ не коммитить.
outputs/reports/source_acquisition не коммитить.

Добавь offline smoke test с temp HTML/dummy xlsx bytes.
```

## Проверки

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\source_acquisition\minfin_fetch.py scripts\source_acquisition\http_client.py scripts\source_acquisition\source_registry.py
.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_monthly_acquisition_smoke.py
.\.venv\Scripts\python.exe scripts\qa\minfin_monthly_acquisition_smoke.py
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --dry-run --no-network
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --download
```

Последняя команда должна безопасно заблокироваться без confirm.

Реальный download только после отдельного разрешения:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --download --confirm DOWNLOAD_MINFIN_SOURCE
```

## Commit

```powershell
git add scripts/source_acquisition scripts/qa/minfin_monthly_acquisition_smoke.py docs/07_operations/minfin_source_acquisition.md docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Implement controlled Minfin monthly acquisition"
git push
```

## Критерии завершения

```text
- Monthly workflow покрыт offline smoke.
- Download blocked без confirm.
- Live 503/network failure не мутирует raw.
- Registry update реализован.
```

---

# P3.4 - Annual finalization

## Цель

Реализовать annual-final mode для январского закрытия предыдущего года.

## Создать/изменить файлы

Изменить:

```text
scripts/source_acquisition/minfin_fetch.py
scripts/source_acquisition/source_registry.py
scripts/source_acquisition/path_planning.py
scripts/source_acquisition/minfin_html_parser.py
docs/07_operations/minfin_source_acquisition.md
docs/00_project/p3_modernization_progress_report.md
docs/06_quality/manual_checks_log.md
```

Создать:

```text
scripts/qa/minfin_annual_final_smoke.py
```

## Требования

Annual-final workflow:

```text
1. Discover/download prior-year file.
2. Select title without "на DD.MM.YYYY".
3. Do not require suffix YYYY1231.
4. Prefer publication/modified date in January-February of year+1.
5. Validate filename year.
6. Compute candidate hash.
7. Compare with existing final.
8. If no final exists: create final after validation.
9. If same hash: no replacement.
10. If different hash: block and require manual review.
11. Registry row storage_role=final.
12. Mark final active only after approval.
```

Confirm tokens:

```text
--download --confirm DOWNLOAD_MINFIN_SOURCE
--download --confirm REPLACE_MINFIN_FINAL
```

## Команда для Codex

```text
Выполни P3.4 Annual finalization.

Не требуй YYYY1231 в имени annual-final файла.
Выбирай final candidate по title/year и отсутствию "на DD.MM.YYYY".
Если existing final hash differs, блокируй replacement без REPLACE_MINFIN_FINAL.
Добавь smoke test для no final, same hash, different hash blocked, replacement with confirm in temp dir.
```

## Проверки

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\source_acquisition\minfin_fetch.py scripts\source_acquisition\source_registry.py
.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_annual_final_smoke.py
.\.venv\Scripts\python.exe scripts\qa\minfin_annual_final_smoke.py
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2025 --mode annual-final --dry-run --no-network
```

## Commit

```powershell
git add scripts/source_acquisition scripts/qa/minfin_annual_final_smoke.py docs/07_operations/minfin_source_acquisition.md docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Implement Minfin annual finalization workflow"
git push
```

## Критерии завершения

```text
- Annual-final работает в temp smoke.
- Changed final hash блокируется.
- REPLACE_MINFIN_FINAL нужен для замены.
```

---

# P3.5 - Manual fallback import

## Цель

Реализовать ручной импорт Excel, если сайт Минфина недоступен или изменилась верстка.

## Создать/изменить файлы

Изменить:

```text
scripts/source_acquisition/minfin_fetch.py
scripts/source_acquisition/source_registry.py
docs/07_operations/minfin_source_acquisition.md
docs/00_project/p3_modernization_progress_report.md
docs/06_quality/manual_checks_log.md
```

Создать:

```text
scripts/qa/minfin_manual_import_smoke.py
```

## Требования

Команды:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode manual-import --manual-file C:\path\INTERNET_Auction_Results_rus_2026_YYYYMMDD.xlsx --dry-run
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode manual-import --manual-file C:\path\INTERNET_Auction_Results_rus_2026_YYYYMMDD.xlsx --download --confirm IMPORT_MINFIN_FILE
```

Правила:

```text
- validate file exists;
- validate .xlsx;
- validate filename pattern;
- validate filename year equals --year;
- compute sha256;
- dry-run shows planned role/path/hash;
- import uses temp+promote workflow;
- registry discovery_method=manual-import;
- notes includes original local file path;
- no final overwrite outside annual-final rules;
- no blind copy.
```

## Команда для Codex

```text
Выполни P3.5 Manual fallback import.

Используй canonical option --manual-file.
Импорт должен быть заблокирован без --confirm IMPORT_MINFIN_FILE.
Проверяй extension, filename pattern и year.
Не перезаписывай final через manual-import.
Добавь smoke test с temp xlsx-файлами.
```

## Проверки

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\source_acquisition\minfin_fetch.py
.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_manual_import_smoke.py
.\.venv\Scripts\python.exe scripts\qa\minfin_manual_import_smoke.py
.\.venv\Scripts\python.exe -m compileall -q scripts
```

## Commit

```powershell
git add scripts/source_acquisition scripts/qa/minfin_manual_import_smoke.py docs/07_operations/minfin_source_acquisition.md docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Add Minfin manual fallback import"
git push
```

## Критерии завершения

```text
- Manual import dry-run работает.
- Import без confirm блокируется.
- Year mismatch rejected.
- Invalid extension rejected.
- No blind copy.
```

---

# P3.6 - Интеграция source registry в data audit

## Цель

Интегрировать controlled Minfin registry в `01_data_audit.py` без поломки существующего legacy pipeline.

Это критический этап. Нельзя просто “подключить registry и надеяться”, потому что человечество уже пробовало надеяться на данные. Получилось Excel.

## Создать/изменить файлы

Изменить:

```text
scripts/01_data_audit.py
scripts/source_acquisition/source_registry.py
docs/02_data_contracts/minfin_source_registry_contract.md
docs/07_operations/minfin_source_acquisition.md
docs/00_project/p3_modernization_progress_report.md
docs/06_quality/manual_checks_log.md
```

Создать:

```text
scripts/qa/minfin_data_audit_registry_smoke.py
tests/fixtures/minfin_data_audit_registry_valid.json
tests/fixtures/minfin_data_audit_registry_missing_file.json
tests/fixtures/minfin_data_audit_registry_hash_mismatch.json
tests/fixtures/minfin_data_audit_registry_duplicate_active.json
```

## Требования к CLI

Добавить в data audit и/или общий pipeline параметры:

```text
--source-registry-mode off|warn|strict
--allow-legacy-raw
```

Default:

```text
--source-registry-mode warn
--allow-legacy-raw true
```

Если параметры добавляются в `ofz-run` или quality gate, они должны быть совместимы с текущими default-запусками.

## Режимы работы

### off

```text
- Registry не читается.
- Legacy data/raw используется как раньше.
- Никаких новых failures.
```

### warn

```text
- Registry читается, если существует.
- Ошибки registry пишутся как warnings.
- Если controlled source некорректен, но legacy raw доступен, pipeline продолжает работу.
- Warning должен быть явно виден в data audit report/manual log.
```

### strict

```text
- Registry обязателен.
- Active controlled files обязательны.
- Hash mismatch = fail.
- Missing active file = fail.
- Duplicate active rows = fail.
- Legacy fallback не используется, если registry должен быть strict.
```

## Что проверять в registry

Data audit должен валидировать:

```text
1. Registry file exists, если mode warn/strict.
2. Registry file schema соответствует контракту.
3. Нет дубликатов active rows для одного year + storage_role.
4. Для current year есть active latest, если controlled source включен.
5. Для закрытых лет есть active final, если controlled final существует.
6. Active file path существует.
7. sha256 active file совпадает с registry.
8. file_size_bytes совпадает, если поле заполнено.
9. storage_role входит в allowed list.
10. discovery_method входит в html/manual-import/observation.
11. Для discovery_method=html заполнены:
    - section_id;
    - page_param;
    - document_id или document_page_url;
    - document_title;
    - file_url или absolute_file_url.
12. Для discovery_method=manual-import заполнены notes и file_name.
13. Registry не требует live network.
```

## Поведение с legacy raw

Legacy raw должен продолжать работать:

```text
- если registry отсутствует и mode=warn;
- если registry есть, но controlled source еще не полностью migrated;
- если allow_legacy_raw=true.
```

В отчете data audit нужно явно писать:

```text
source_registry_mode
source_registry_status
controlled_source_used
legacy_raw_fallback_used
registry_warnings_count
registry_errors_count
```

## Встраивание в pipeline

Порядок реализации:

```text
1. Добавить helper в source_registry.py:
   validate_source_registry(...)
   load_active_source_records(...)
   validate_active_file_hashes(...)
   summarize_registry_status(...)

2. Подключить helper в 01_data_audit.py в начале audit.

3. Добавить warnings/errors в существующий audit report.

4. Не менять cleaning/feature engineering.

5. Не менять реальные Excel input selection без отдельного controlled migration.
```

## Команда для Codex

```text
Выполни P3.6 Интеграция source registry в data audit.

Цель:
Data audit должен уметь проверять controlled Minfin registry, но legacy pipeline должен продолжать работать.

Добавь режимы:
--source-registry-mode off|warn|strict
--allow-legacy-raw

Default:
source-registry-mode=warn
allow-legacy-raw=true

Реализуй registry validation helper в scripts/source_acquisition/source_registry.py:
- validate_source_registry
- load_active_source_records
- validate_active_file_hashes
- summarize_registry_status

Подключи validation в scripts/01_data_audit.py.
Не делай live network calls.
Не меняй cleaning behavior.
Не ломай текущий ofz-quality --fast.

Добавь smoke test:
scripts/qa/minfin_data_audit_registry_smoke.py

Тест должен покрывать:
- missing registry in warn mode;
- missing registry in strict mode;
- valid registry;
- missing active file;
- hash mismatch;
- duplicate active rows;
- legacy fallback allowed;
- no live network.

Обнови docs/02_data_contracts/minfin_source_registry_contract.md,
docs/07_operations/minfin_source_acquisition.md,
docs/00_project/p3_modernization_progress_report.md,
docs/06_quality/manual_checks_log.md.
```

## Проверки

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\01_data_audit.py scripts\source_acquisition\source_registry.py
.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_data_audit_registry_smoke.py
.\.venv\Scripts\python.exe scripts\qa\minfin_data_audit_registry_smoke.py
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Если добавлены CLI options в `ofz-run`, проверить:

```powershell
.\.venv\Scripts\ofz-run.exe --help
```

Если добавлены CLI options в `ofz-quality`, проверить:

```powershell
.\.venv\Scripts\ofz-quality.exe --help
```

## Запрещено

```text
- требовать live network в data audit;
- ломать legacy raw ingestion;
- делать strict default;
- менять cleaning behavior;
- автоматически переключать pipeline на controlled source без отдельного migration decision;
- коммитить generated audit outputs.
```

## Commit

```powershell
git add scripts/01_data_audit.py scripts/source_acquisition/source_registry.py scripts/qa/minfin_data_audit_registry_smoke.py tests/fixtures/minfin_data_audit_registry_valid.json tests/fixtures/minfin_data_audit_registry_missing_file.json tests/fixtures/minfin_data_audit_registry_hash_mismatch.json tests/fixtures/minfin_data_audit_registry_duplicate_active.json docs/02_data_contracts/minfin_source_registry_contract.md docs/07_operations/minfin_source_acquisition.md docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Integrate Minfin source registry into data audit"
git push
```

## Критерии завершения

```text
- source-registry-mode off/warn/strict реализован.
- warn mode не ломает текущий pipeline.
- strict mode валит ошибочные registry cases.
- legacy fallback работает.
- ofz-quality --fast проходит.
- Нет live network calls в data audit.
```

---

# P3.7 - Parser QA fixtures/tests

## Цель

Добавить полноценные offline QA fixtures/tests для parser, selection, hash, annual-final, manual-import и failure modes.

## Создать файлы

```text
tests/fixtures/minfin_auction_page_section_66_sample.html
tests/fixtures/minfin_auction_page_66_page2_sample.html
tests/fixtures/minfin_auction_candidates_expected.json
tests/fixtures/minfin_wrong_sections_sample.html
tests/fixtures/minfin_hash_changed_case.json
tests/fixtures/minfin_hash_unchanged_case.json
scripts/qa/minfin_source_acquisition_tests.py
```

## Команда для Codex

```text
Выполни P3.7 Parser QA fixtures/tests.

Создай offline fixtures и test runner.
Тесты не должны обращаться к live site и не должны менять data/raw.

Покрой:
- section 66 selected;
- sections 65/38/39 ignored;
- page_66 parsed;
- data-page-count parsed;
- relative XLSX URL resolved;
- current-year monthly selected;
- annual-final selected;
- annual final not requiring YYYY1231;
- non-xlsx ignored;
- wrong year ignored;
- malformed links ignored;
- 503/timeout simulated;
- hash changed/unchanged;
- annual-final changed hash requires confirm;
- manual-file year mismatch rejected;
- dry-run does not mutate raw.
```

## Проверки

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_source_acquisition_tests.py
.\.venv\Scripts\python.exe scripts\qa\minfin_source_acquisition_tests.py
.\.venv\Scripts\python.exe -m compileall -q scripts
```

## Commit

```powershell
git add tests/fixtures scripts/qa/minfin_source_acquisition_tests.py docs/06_quality/manual_checks_log.md docs/00_project/p3_modernization_progress_report.md
git commit -m "Add Minfin source acquisition QA fixtures"
git push
```

## Критерии завершения

```text
- Tests работают offline.
- Wrong sections ignored.
- Pagination tested.
- Annual-final non-YYYY1231 tested.
- No raw mutation.
```

---

# P3.8 - Операционная инструкция monthly/final update

## Цель

Создать русскоязычную операционную инструкцию по ежемесячному обновлению данных Минфина и январскому annual-final.

## Создать/изменить файлы

Создать:

```text
docs/07_operations/minfin_monthly_update_procedure.md
```

Изменить:

```text
docs/07_operations/minfin_source_acquisition.md
docs/07_operations/release_checklist.md
README.md
docs/00_project/p3_modernization_progress_report.md
docs/06_quality/manual_checks_log.md
```

## Что документировать

Monthly:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode monthly --dry-run
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode monthly --download --confirm DOWNLOAD_MINFIN_SOURCE
.\.venv\Scripts\ofz-quality.exe --fast --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

January annual-final:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY-1 --mode annual-final --dry-run
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY-1 --mode annual-final --download --confirm DOWNLOAD_MINFIN_SOURCE
```

Changed final hash:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY-1 --mode annual-final --download --confirm REPLACE_MINFIN_FINAL
```

Manual fallback:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode manual-import --manual-file C:\path\INTERNET_Auction_Results_rus_YYYY_YYYYMMDD.xlsx --dry-run
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode manual-import --manual-file C:\path\INTERNET_Auction_Results_rus_YYYY_YYYYMMDD.xlsx --download --confirm IMPORT_MINFIN_FILE
```

Также описать:

```text
- target section id_66/page_66;
- как понять, что выбран правильный XLSX;
- что делать при 503;
- что делать при changed final hash;
- что можно коммитить;
- что нельзя коммитить;
- что versions/ не коммитится;
- что outputs/reports/source_acquisition не коммитится;
- Windows Task Scheduler plan как reminder only, без авто-download.
```

## Команда для Codex

```text
Выполни P3.8 Operator procedure.

Создай русскоязычную инструкцию minfin_monthly_update_procedure.md.
Опиши monthly, annual-final, changed final hash и manual fallback.
Укажи HTML-структуру Минфина: section id_66, page_66, title patterns.
Опиши commit policy и запрет на versions/outputs.
Не реализуй автоматический scheduler, только план/reminder.
```

## Проверки

Docs-only:

```powershell
git diff --name-only
```

Compileall/quality не запускать, если Python не менялся.

## Commit

```powershell
git add docs/07_operations/minfin_monthly_update_procedure.md docs/07_operations/minfin_source_acquisition.md docs/07_operations/release_checklist.md README.md docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Document Minfin monthly update procedure"
git push
```

## Критерии завершения

```text
- Оператор может выполнить monthly update по документу.
- Annual-final описан.
- Manual fallback описан.
- Commit policy понятна.
- 503 handling описан.
```

---

# P3.REL.1 - Stable release procedure update

## Цель

Обновить release procedure с учетом source acquisition.

## Команда для Codex

```text
Выполни P3.REL.1 Stable release procedure update.

Обнови stable release procedure так, чтобы она включала:
1. source acquisition dry-run;
2. monthly/annual-final update при необходимости;
3. registry review;
4. data audit;
5. quality-fast;
6. screenshot validation outside sandbox;
7. quality-full;
8. release bundle dry-run;
9. release bundle build;
10. optional BI package;
11. git tag;
12. gh release create/upload только по явному разрешению пользователя.
```

## Проверки

Docs-only, если код не менялся:

```powershell
git diff --name-only
```

## Commit

```powershell
git add docs/07_operations/stable_release_procedure.md docs/07_operations/release_checklist.md README.md docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Update stable release procedure for source acquisition"
git push
```

---

## Финальный ответ Codex после каждого этапа

```text
1. Этап.
2. Статус.
3. Что изменено.
4. Какие проверки выполнены.
5. Какие проверки пропущены и почему.
6. Ошибки/warnings.
7. Измененные файлы.
8. Commit hash.
9. Push status.
10. GitHub Actions status, если был push.
11. Generated artifacts not staged.
12. Data/raw policy respected.
13. Git/GitHub commands outside sandbox only.
14. Следующий рекомендуемый этап.
```
