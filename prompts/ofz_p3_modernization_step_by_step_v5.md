# OFZ_ANALYTICS: P3 modernization step-by-step v5
## HTML-aware Minfin acquisition implementation plan

Дата актуализации: 2026-06-16.

## 0. Что изменилось в v5

Пользователь предоставил HTML страницы Минфина `Минфин России :: Аукционы`.

Из HTML получены важные технические детали:

```text
- целевая секция имеет anchor `tablitsy_po_rezultatam_provedeniya_auktsionov`;
- целевая секция имеет container id `ajax-pagination-content-10090-66`;
- pagination id `ajax-pagination-10090-66`;
- page parameter `page_66`;
- document ids: `id_66`;
- file links: `a.file_item`;
- current-year monthly title contains `на DD.MM.YYYY`;
- annual-final title usually does not contain `на DD.MM.YYYY`;
- annual-final file suffix is not always YYYY1231;
- href values are relative and must be resolved against `https://minfin.gov.ru`.
```

## 1. HTML parser rules

### 1.1. Target section only

Parser must target only:

```text
section_id=66
anchor=tablitsy_po_rezultatam_provedeniya_auktsionov
container=#ajax-pagination-content-10090-66
pagination=#ajax-pagination-10090-66
page_param=page_66
document id query param=id_66
document_group_name=Таблицы по результатам проведения аукционов
```

Ignore sections:

```text
65 planned auctions
38 auction announcements
39 auction result documents
```

### 1.2. Document extraction

For each `div.document_card` inside target container, extract:

```text
section_id
page_param
page_number
document_id
document_page_url
document_title
document_type
published_at
modified_at
tags
file_url
absolute_file_url
file_name
file_title
file_info
file_size_text
file_extension
```

### 1.3. Candidate filter

Candidate must satisfy:

```text
document_title contains "Результаты проведенных аукционов по размещению государственных ценных бумаг"
document_title contains "в <year> году"
file_name matches INTERNET_Auction_Results_rus_<year>_*.xlsx
file extension is .xlsx
section_id == 66
```

### 1.4. Pagination

Use `data-page-count` from `#ajax-pagination-10090-66`.

Fetch pages:

```text
base URL
base URL?page_66=2
base URL?page_66=3
...
base URL?page_66=N
```

Do not require browser/JS click. The JS simply calls `$.get(url)` and appends contents.

Fallback if page count missing:

```text
crawl page_66 incrementally until no new target documents or max_pages reached.
Default max_pages=20.
```

### 1.5. Selection logic

Monthly mode:

```text
1. Filter target year.
2. Prefer title containing `на DD.MM.YYYY`.
3. Choose max as_of_date from title.
4. If no as_of_date, choose latest modified_at, then published_at.
```

Annual-final mode:

```text
1. Filter target year.
2. Prefer title without `на DD.MM.YYYY`.
3. Prefer documents published/modified in January-February of year+1, but do not require.
4. Do not assume file suffix YYYY1231.
5. If ambiguous, block or warn with candidate list.
```

## 2. P3.1 - Source acquisition skeleton with HTML parser skeleton

## Цель

Создать CLI skeleton `ofz-fetch-minfin` plus offline HTML parser skeleton.

## Файлы

Создать:

```text
scripts/source_acquisition/__init__.py
scripts/source_acquisition/minfin_fetch.py
scripts/source_acquisition/source_registry.py
scripts/source_acquisition/minfin_patterns.py
scripts/source_acquisition/path_planning.py
scripts/source_acquisition/minfin_html_parser.py
```

Создать fixture:

```text
tests/fixtures/minfin_auction_page_section_66_sample.html
tests/fixtures/minfin_auction_candidates_expected.json
```

Допустимо создать smoke:

```text
scripts/qa/minfin_source_acquisition_smoke.py
```

Обновить:

```text
pyproject.toml
docs/00_project/p3_modernization_progress_report.md
docs/06_quality/manual_checks_log.md
docs/07_operations/minfin_source_acquisition.md
```

## Entry point

```toml
ofz-fetch-minfin = "scripts.source_acquisition.minfin_fetch:main"
```

## CLI options

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

## Implement in P3.1

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

P3.1 must not perform real download or raw mutation.

## Required commands

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

If smoke exists:

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

Add only actually changed files.

## 3. P3.2 - Registry writer with HTML provenance

P3.2 remains registry writer stage, but registry records must include HTML provenance fields when available:

```text
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

Required checks:

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\source_acquisition\source_registry.py
.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_source_registry_smoke.py
.\.venv\Scripts\python.exe scripts\qa\minfin_source_registry_smoke.py
.\.venv\Scripts\python.exe -m compileall -q scripts
```

## 4. P3.3 - Monthly acquisition with section 66 pagination

P3.3 monthly implementation must:

```text
1. Fetch base page.
2. Parse target section 66.
3. Read page_66 pagination count.
4. Fetch page_66=2..N.
5. Extract candidate XLSX files only from section 66.
6. Select monthly candidate for target year.
7. Download selected absolute_file_url to temp.
8. Validate filename/year/extension.
9. Hash compare.
10. Promote latest and version snapshot only if changed.
11. Update registry with HTML provenance.
```

Real download requires:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --download --confirm DOWNLOAD_MINFIN_SOURCE
```

Blocked without confirm.

## 5. P3.4 - Annual finalization with non-YYYY1231 tolerance

Annual-final must:

```text
- select title without `на DD.MM.YYYY`;
- not require file suffix YYYY1231;
- use year in title and filename pattern;
- prefer January-February publication of Y+1;
- block ambiguous candidates.
```

Changed final replacement requires:

```text
--confirm REPLACE_MINFIN_FINAL
```

## 6. P3.5 - Manual fallback import

Manual import uses:

```text
--manual-file
```

It does not have HTML provenance. Registry must set:

```text
discovery_method=manual-import
document_title=null
document_id=null
file_url=null or local path in notes
notes includes original local file path and operator action
```

## 7. P3.6 - Pipeline integration

Data audit must validate registry fields including HTML provenance if controlled source is used, but must not require live network.

## 8. P3.7 - Parser QA fixtures/tests expanded

Create:

```text
tests/fixtures/minfin_auction_page_section_66_sample.html
tests/fixtures/minfin_auction_page_66_page2_sample.html
tests/fixtures/minfin_auction_candidates_expected.json
tests/fixtures/minfin_wrong_sections_sample.html
```

Test:

```text
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
- ambiguity warning.
```

## 9. P3.8 - Operator procedure update

Operator procedure must mention actual Minfin HTML structure:

```text
- target section name;
- section id 66;
- pagination page_66;
- current-year monthly title contains "на DD.MM.YYYY";
- annual-final title usually has no "на DD.MM.YYYY";
- annual-final file suffix may be not YYYY1231;
- if parser fails, use manual-import.
```

## 10. Final response format

Codex must report:

```text
1. Stage.
2. Status.
3. What changed.
4. Checks run.
5. Checks skipped and why.
6. Failures/warnings.
7. Files changed.
8. Commit hash.
9. Push status.
10. GitHub Actions status if push occurred.
11. Generated artifacts not staged.
12. Data/raw policy respected.
13. Git/GitHub commands outside sandbox only.
14. Next recommended stage.
```
