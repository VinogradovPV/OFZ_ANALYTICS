# OFZ_ANALYTICS: системный промпт P3 modernization v6
## HTML-aware source acquisition Минфина, полностью на русском

Дата актуализации: 2026-06-17.

## 1. Текущий статус проекта

Фактический статус:

```text
P2 modernization: completed, stable-release-candidate.
P3.PRE.0 Windows GUI launcher UX/runtime fix: completed.
P3.0-pre CI UTF-8 output fix for schema validation: completed.
P3.PRE.1 Scripts balance/problem audit: completed.
P3.PRE.2 Docs mojibake/encoding audit and UTF-8 normalization: completed.
P3.0 Source acquisition design: completed.
Следующий этап: P3.1 Source acquisition skeleton.
```

Не повторяй завершенные этапы без отдельной причины. Не начинай работу “с нуля”.

## 2. Жесткое правило Git/GitHub

Все команды `git` и `gh` выполнять **только outside sandbox** из корня проекта:

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics
```

Запрещено выполнять `git` и `gh` внутри Codex sandbox.

Перед каждым commit outside sandbox:

```powershell
git status --short
git diff --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|outputs/reports/source_acquisition|data/processed|logs|releases|docm|tmp|temp|crdownload|part|data/raw/minfin/ofz_auction_results/versions"
```

После каждого push outside sandbox:

```powershell
gh run list --limit 5
```

Если текущий run упал:

```powershell
gh run view --log
```

Не переходи к следующему этапу, если текущий commit сломал CI и failure не был явно deferred.

## 3. Политика получения данных Минфина

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

503 сайта Минфина считать штатным operational failure mode. При 503 или network failure нельзя менять raw storage.

## 4. HTML-структура страницы Минфина

Пользователь предоставил HTML страницы `Минфин России :: Аукционы`.

Целевая секция:

```text
Название: Таблицы по результатам проведения аукционов
anchor: tablitsy_po_rezultatam_provedeniya_auktsionov
container: ajax-pagination-content-10090-66
pagination id: ajax-pagination-10090-66
page parameter: page_66
document id query parameter: id_66
```

Игнорировать секции:

```text
65 / page_65 - Таблицы планируемых аукционов
38 / page_38 - Информационные сообщения о проведении аукционов
39 / page_39 - Результат аукциона
```

Файлы Excel находятся в:

```text
a.file_item[href]
```

Ссылки относительные, например:

```text
/common/upload/library/2026/06/main/INTERNET_Auction_Results_rus_2026_20260611.xlsx
```

Их нужно резолвить относительно:

```text
https://minfin.gov.ru
```

Пагинация не требует браузера. Использовать:

```text
?page_66=2
?page_66=3
...
```

## 5. Правила выбора кандидатов

Кандидат должен удовлетворять условиям:

```text
section_id == 66
document_title содержит "Результаты проведенных аукционов по размещению государственных ценных бумаг"
document_title содержит "в <year> году"
file_name matches INTERNET_Auction_Results_rus_<year>_*.xlsx
file_extension == .xlsx
```

Для `monthly`:

```text
1. Выбрать документы target year.
2. Предпочитать заголовок с "на DD.MM.YYYY".
3. Если несколько кандидатов, выбрать максимальную as_of_date из заголовка.
4. Если as_of_date не распарсилась, выбрать latest modified_at, затем latest published_at.
5. Annual-final без "на DD.MM.YYYY" не выбирать для monthly, если есть monthly candidate.
```

Для `annual-final`:

```text
1. Выбрать документы target year.
2. Предпочитать заголовок без "на DD.MM.YYYY".
3. Предпочитать публикацию/изменение в январе-феврале year+1, но не требовать это жестко.
4. Не требовать суффикс YYYY1231.
5. При ambiguity блокировать действие или явно выводить список кандидатов.
```

Для `manual-import`:

```text
1. Проверять имя локального файла по INTERNET_Auction_Results_rus_<year>_*.xlsx.
2. Не требовать document_title, потому что локальный файл не имеет HTML-контекста.
3. В registry notes указать ручной источник.
```

## 6. Canonical CLI contract

Entry point:

```toml
ofz-fetch-minfin = "scripts.source_acquisition.minfin_fetch:main"
```

Canonical files:

```text
scripts/source_acquisition/__init__.py
scripts/source_acquisition/minfin_fetch.py
scripts/source_acquisition/source_registry.py
scripts/source_acquisition/minfin_patterns.py
scripts/source_acquisition/path_planning.py
scripts/source_acquisition/minfin_html_parser.py
```

Опции CLI:

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
--source-registry-mode off|warn|strict
--allow-legacy-raw
```

Использовать `--manual-file`, не `--from-file`.

## 7. Запреты

Нельзя:

```text
- скачивать реальные Excel без explicit confirm;
- менять raw Excel files на P3.1;
- создавать raw storage dirs на P3.1;
- коммитить outputs/reports/source_acquisition;
- коммитить data/raw/minfin/ofz_auction_results/versions;
- коммитить temp downloads;
- требовать live network для обычного pipeline;
- ломать legacy data/raw ingestion до отдельного решения.
```

## 8. P3.6 Data audit integration - обязательная детализация

Когда дойдешь до P3.6, интеграция source registry в data audit должна быть постепенной и обратимо-безопасной.

Цель P3.6:

```text
Data audit умеет валидировать controlled Minfin registry, но legacy pipeline остается рабочим.
```

Обязательные режимы:

```text
--source-registry-mode off|warn|strict
--allow-legacy-raw
```

Default:

```text
source-registry-mode=warn
allow-legacy-raw=true
```

Логика:

```text
off:
  registry не проверяется.

warn:
  registry проверяется, но ошибки оформляются как warning, если legacy raw доступен.

strict:
  registry обязателен, ошибки registry/source files должны приводить к fail.
```

Data audit должен проверять:

```text
- registry file exists, если режим warn/strict;
- active rows уникальны по year + storage_role;
- active latest существует для текущего года, если controlled source есть;
- active final существует для закрытого года, если controlled final есть;
- sha256 active file совпадает с registry;
- file_size_bytes совпадает, если поле заполнено;
- HTML provenance поля валидны, если discovery_method=html;
- manual provenance поля валидны, если discovery_method=manual-import;
- legacy raw files продолжают использоваться, если registry отсутствует и allow_legacy_raw=true;
- live network не вызывается внутри data audit.
```

## 9. Финальный ответ Codex после каждого этапа

В каждом финальном ответе Codex обязан указать:

```text
1. Этап.
2. Статус.
3. Что изменено.
4. Какие проверки выполнены.
5. Какие проверки пропущены и почему.
6. Ошибки/warnings.
7. Какие файлы изменены.
8. Commit hash.
9. Push status.
10. GitHub Actions status, если был push.
11. Подтверждение: generated artifacts not staged.
12. Подтверждение: data/raw policy respected.
13. Подтверждение: Git/GitHub commands outside sandbox only.
14. Следующий рекомендуемый этап.
```
