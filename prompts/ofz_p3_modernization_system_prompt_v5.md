# OFZ_ANALYTICS: P3 modernization system prompt v5
## Minfin HTML-aware source acquisition

Дата актуализации: 2026-06-16.

## 1. Текущий статус проекта

Фактический статус:

```text
P2 modernization: completed, stable-release-candidate.
P3.PRE.0 Windows GUI launcher UX/runtime fix: completed.
P3.0-pre CI UTF-8 output fix for schema validation: completed.
P3.PRE.1 Scripts balance/problem audit: completed.
P3.PRE.2 Docs mojibake/encoding audit and UTF-8 normalization: completed.
P3.0 Source acquisition design: completed.
Next stage: P3.1 Source acquisition skeleton.
```

Не повторять завершенные этапы без отдельной причины.

## 2. Жесткое правило Git/GitHub

Все `git` и `gh` команды выполнять **только outside sandbox** из корня проекта:

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics
```

Запрещено выполнять `git` и `gh` внутри Codex sandbox.

## 3. Source acquisition policy

Обязательная политика:

```text
Variant C - hybrid latest + final + version snapshots on hash change
```

Источник:

```text
https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/#tablitsy_po_rezultatam_provedeniya_auktsionov
```

Fallback URL:

```text
https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction
```

503 сайта Минфина считается штатным operational failure mode. При 503/network failure нельзя мутировать raw storage.

## 4. Новые сведения из фактического HTML страницы Минфина

Пользователь предоставил HTML страницы Минфина `Минфин России :: Аукционы`.

### 4.1. Структура секций

На странице есть anchor navigation:

```html
<a href="#tablitsy_planiruemykh_auktsionov">Таблицы планируемых аукционов</a>
<a href="#informatsionnye_soobshcheniya_o_provedenii_auktsionov">Информационные сообщения о проведении аукционов</a>
<a href="#rezultat_auktsiona">Результат аукциона</a>
<a href="#tablitsy_po_rezultatam_provedeniya_auktsionov">Таблицы по результатам проведения аукционов</a>
```

Целевая секция для source acquisition:

```text
Таблицы по результатам проведения аукционов
anchor name="tablitsy_po_rezultatam_provedeniya_auktsionov"
document_group_name="Таблицы по результатам проведения аукционов"
container id="ajax-pagination-content-10090-66"
pagination id="ajax-pagination-10090-66"
page parameter="page_66"
data-page-count="4" in supplied HTML
list_found_count="19"
```

Не путать с другими секциями:

```text
id 65 / page_65 - Таблицы планируемых аукционов
id 38 / page_38 - Информационные сообщения о проведении аукционов
id 39 / page_39 - Результат аукциона
id 66 / page_66 - Таблицы по результатам проведения аукционов
```

### 4.2. Document card structure

Каждый документ в целевой секции представлен как:

```html
<div class="document_card inner_link" data-href="...id_66=...">
  <div class="document_info">
    <div class="date_list">
      <span class="date">Опубликовано: DD.MM.YYYY</span>
      <span class="date">Изменено: DD.MM.YYYY</span>
    </div>
  </div>
  <a class="document_type">Документ</a>
  <a class="document_title" title="...">...</a>
  <div class="files_list">
    <a class="file_item" href="/common/upload/library/YYYY/MM/main/INTERNET_Auction_Results_rus_YYYY_YYYYMMDD.xlsx">
      <span class="file_info">xlsx, NN.NN kb</span>
    </a>
  </div>
</div>
```

Parser должен извлекать:

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

### 4.3. Pagination

В HTML целевой секции есть ajax pagination:

```html
<a id="ajax-pagination-10090-66"
   href="?page_66=2"
   data-page-count="4"
   data-container="#ajax-pagination-content-10090-66">
```

Важно:

```text
Не нужен browser click для pagination.
Можно запрашивать обычные HTML pages:
base_url?page_66=2
base_url?page_66=3
base_url?page_66=4
```

Алгоритм discovery:

```text
1. Fetch base page.
2. Locate target section container `#ajax-pagination-content-10090-66`.
3. Read pagination data-page-count for page_66.
4. Parse page 1.
5. Fetch pages 2..page_count using `?page_66=N`.
6. Extract contents of `#ajax-pagination-content-10090-66`.
7. Deduplicate documents by document_id + file_url.
```

Fallback if `data-page-count` missing:

```text
Try pages until no new target document cards are returned, with max_pages guard.
Default max_pages guard for section 66: 20.
```

### 4.4. Candidate examples from supplied HTML

Current-year latest example:

```text
title: Результаты проведенных аукционов по размещению государственных ценных бумаг в 2026 году на 11.06.2026
published_at: 15.06.2026
modified_at: 15.06.2026
file_url: /common/upload/library/2026/06/main/INTERNET_Auction_Results_rus_2026_20260611.xlsx
file_info: xlsx, 19.58 kb
```

Annual-final examples:

```text
2025: INTERNET_Auction_Results_rus_2025_20251231.xlsx, published 16.01.2026
2024: INTERNET_Auction_Results_rus_2024_20241231.xlsx, published 13.01.2025
2023: INTERNET_Auction_Results_rus_2023_20231231.xlsx, published 19.01.2024
2022: INTERNET_Auction_Results_rus_2022_20221222.xlsx, published 20.01.2023
2021: INTERNET_Auction_Results_rus_2021_20211223.xlsx, published 11.02.2022
```

Important inference:

```text
Annual-final file date is not always YYYY1231.
Do not assume December 31.
Use title/year + file pattern + publication date + modified date.
```

### 4.5. Candidate selection rules

For target year `Y`, candidates must satisfy:

```text
- located in section id_66 / page_66 / "Таблицы по результатам проведения аукционов";
- document_title contains "Результаты проведенных аукционов по размещению государственных ценных бумаг";
- document_title contains "в Y году";
- file_url ends with .xlsx;
- file_name matches INTERNET_Auction_Results_rus_Y_*.xlsx;
```

For `mode=monthly`:

```text
- select target year Y;
- prefer documents whose title contains "на DD.MM.YYYY";
- if several monthly documents exist for Y, choose latest as_of_date from title;
- if as_of_date cannot be parsed, choose latest modified_at, then latest published_at;
- annual final title without "на" should not be selected for monthly if a "на DD.MM.YYYY" candidate exists.
```

For `mode=annual-final`:

```text
- select target year Y;
- prefer title without "на DD.MM.YYYY";
- prefer publication in January/February of Y+1, but do not require it;
- if several final candidates exist, choose latest modified_at/published_at and flag ambiguity;
- do not require file suffix Y1231.
```

### 4.6. URL handling

`file_url` values are relative:

```text
/common/upload/library/2026/06/main/INTERNET_Auction_Results_rus_2026_20260611.xlsx
```

Downloader must resolve them against:

```text
https://minfin.gov.ru
```

## 5. Canonical CLI contract

Entry point:

```toml
ofz-fetch-minfin = "scripts.source_acquisition.minfin_fetch:main"
```

Canonical files:

```text
scripts/source_acquisition/__init__.py
scripts/source_acquisition/minfin_fetch.py
scripts/source_acquisition/source_registry.py
```

Optional helpers:

```text
scripts/source_acquisition/minfin_patterns.py
scripts/source_acquisition/path_planning.py
scripts/source_acquisition/http_client.py
scripts/source_acquisition/minfin_html_parser.py
```

Canonical options:

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
--save-html-snapshot
--html-file
```

## 6. P3.1 requirements updated by HTML analysis

P3.1 must include parser skeleton or parser helper that can parse local supplied HTML fixture.

Allowed in P3.1:

```text
- implement parse_minfin_auction_table_documents(html, base_url, page_number);
- implement extract_pagination_info(html, section_id=66);
- implement select_candidate(records, year, mode);
- implement --html-file for local dry-run testing;
- add offline fixture based on supplied HTML trimmed to target section.
```

Still forbidden in P3.1:

```text
- real download;
- raw Excel mutation;
- raw storage dir creation;
- registry write to raw storage;
```

## 7. Registry fields updated by HTML analysis

Add fields to registry/planned record contracts:

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

## 8. P3.7 fixtures updated by HTML analysis

Fixtures must include target-section realistic HTML:

```text
tests/fixtures/minfin_auction_page_section_66_sample.html
tests/fixtures/minfin_auction_page_66_page2_sample.html
tests/fixtures/minfin_auction_candidates_expected.json
```

Tests must verify:

```text
- section 66 selected, not sections 65/38/39;
- pagination page_66 parsed;
- data-page-count parsed;
- relative file_url resolved;
- current-year monthly candidate selected;
- annual-final candidate selected even if file suffix is not YYYY1231;
- non-xlsx docs ignored;
- wrong sections ignored even if they contain "аукцион".
```

## 9. Final response format for Codex

Every Codex final response must include:

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
