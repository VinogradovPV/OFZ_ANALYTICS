# OFZ_ANALYTICS: P3 modernization step-by-step
## Pre-P3 audits + Minfin source acquisition Variant C

Дата актуализации: 2026-06-16.

## 0. Назначение инструкции

Эта инструкция описывает порядок P3 после закрытия P2.

P2 завершен как `stable-release-candidate`: release bundle, telemetry, UI launchers, screenshot visual regression backend with fallback, CI, archive flow, module scaffolding, Windows setup, Docker plan и BI package workflow реализованы.

P3 должен добавить управляемый контур получения исходных данных Минфина, но сначала нужно убрать два вида технического мусора:

```text
1. Возможные balance/problems в scripts после P2-декомпозиции.
2. Mojibake/encoding проблемы в документации.
```

## 1. Общие правила

### 1.1. Корень проекта

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics
```

### 1.2. Прочитать перед стартом

```text
docs/00_project/p2_completion_report.md
docs/00_project/p2_modernization_progress_report.md
docs/06_quality/manual_checks_log.md
docs/07_operations/release_bundle_plan.md
docs/07_operations/release_checklist.md
README.md
pyproject.toml
.gitignore
```

### 1.3. Создать P3 progress report

Создать:

```text
docs/00_project/p3_modernization_progress_report.md
```

Вести его после каждого этапа.

### 1.4. Cost-aware mode

Не запускать дорогие проверки без триггера.

Docs-only:

```text
только git diff/status + staged generated artifacts check
```

Python changes:

```text
py_compile + targeted checks
```

Pipeline/source acquisition changes:

```text
dry-run + targeted tests
```

Full gate:

```text
только перед stable release или по отдельной команде
```

### 1.5. Generated artifacts policy

Не коммитить:

```text
outputs/
releases/
logs/
data/processed/
temp downloads
browser binaries
.docm artifacts
```

Перед каждым commit:

```powershell
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|outputs/reports/source_acquisition|data/processed|logs|releases|docm|tmp|temp"
```

# P3.PRE.1 — Scripts balance/problem audit

## Цель

Проверить, не появились ли после P2 проблемы в скриптах:

```text
- перекос между wrappers и вынесенными module skeletons;
- дублирование logic;
- stale imports;
- archived scripts, которые всё еще где-то используются;
- hardcoded paths;
- unsafe subprocess;
- shell=True;
- direct writes outside artifact policy;
- TODO/FIXME/XXX;
- dead wrappers;
- missing main();
- импорт из archive;
- неактуальные CLI references.
```

## Проверочный уровень

```text
Level 2 if scripts/audit script created or changed
Level 0 if only manual report
```

## Задачи

1. Создать отчет:

```text
docs/00_project/p3_scripts_balance_audit_report.md
```

2. При необходимости создать audit helper:

```text
scripts/maintenance/audit_scripts_balance.py
```

3. Проверить:

```text
scripts/
scripts/archive/
scripts/charts/
scripts/qa/
scripts/maintenance/
scripts/source_acquisition/, если уже существует
```

4. В отчете фиксировать issues:

```text
issue_id
file
severity
category
description
recommended_action
fixed_now
notes
```

5. Если найдены safe fixes:

```text
- удалить stale imports;
- исправить очевидные CLI references;
- исправить hardcoded project path only if safe;
- не делать крупную декомпозицию.
```

6. Если найдены non-trivial issues:

```text
- не чинить массово;
- пометить deferred;
- создать recommended P3.MOD item.
```

## Команда для Codex

```text
Выполни P3.PRE.1 Scripts balance/problem audit.

Не начинай P3.0 source acquisition до завершения этого этапа.

Создай docs/00_project/p3_scripts_balance_audit_report.md.

Проверь scripts на:
- stale imports;
- archived scripts references;
- TODO/FIXME/XXX;
- hardcoded absolute paths;
- unsafe subprocess/shell=True;
- generated outputs writes outside policy;
- data/raw mutation outside policy;
- missing main() in CLI-like scripts;
- duplicated helpers after P2 module scaffolding;
- wrappers that should remain wrappers but still contain too much logic;
- references to old scripts moved to scripts/archive.

Если нужно, создай scripts/maintenance/audit_scripts_balance.py.
Если создаешь Python helper, выполни py_compile и compileall.
Не делай крупную декомпозицию.
Не меняй pipeline behavior.
```

## Проверки

Если создан/изменен Python helper:

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\audit_scripts_balance.py
.\.venv\Scripts\python.exe scripts\maintenance\audit_scripts_balance.py --report
.\.venv\Scripts\python.exe -m compileall -q scripts
```

Если только docs:

```powershell
git diff --name-only
```

Перед commit:

```powershell
git diff --cached --name-only | Select-String "outputs|releases|logs|data/processed"
```

## Commit

```powershell
git add docs/00_project/p3_scripts_balance_audit_report.md docs/00_project/p3_modernization_progress_report.md scripts/maintenance/audit_scripts_balance.py docs/06_quality/manual_checks_log.md
git commit -m "Audit scripts before P3 source acquisition"
git push
```

Если `audit_scripts_balance.py` или manual log не менялись — не добавлять.

# P3.PRE.2 — Docs mojibake/encoding audit and UTF-8 normalization

## Цель

Найти и исправить mojibake/encoding проблемы в документах и привести активную документацию к UTF-8.

P2 completion report фиксирует, что README содержит legacy mixed encoding/mojibake в старых секциях. Это нужно закрыть до P3.

## Проверочный уровень

```text
Level 0 if only docs
Level 2 if created encoding audit helper
```

## Scope

Проверять:

```text
README.md
CHANGELOG.md
docs/**/*.md
prompts/**/*.md
tools/**/*.md
```

Не проверять/не менять:

```text
outputs/
releases/
.venv/
.git/
data/raw/*.xlsx
binary files
```

Archived docs:

```text
docs/archive/**/*.md
```

Проверять, но не обязательно исправлять, если они исторические. Для archive можно ставить:

```text
archived_no_change
```

## Mojibake patterns

Искать признаки:

```text
Р”
Р°
Рџ
РЎ
Рµ
РЅ
СЃ
С‚
СЊ
вЂ
в„
â€
Ð
Ñ
```

Осторожно: не каждый символ `Ð` или `Ñ` обязательно ошибка. Если сомневаешься — manual review.

## Задачи

1. Создать:

```text
docs/00_project/p3_docs_encoding_audit_report.md
```

2. При необходимости создать:

```text
scripts/maintenance/audit_docs_encoding.py
```

3. В отчете по каждому документу фиксировать:

```text
path
encoding_detected
status
mojibake_detected
action
notes
```

4. Для активных документов с явным mojibake:

```text
- восстановить текст, если возможно;
- сохранить UTF-8 without BOM;
- не менять смысл;
- не переписывать весь документ стилистически.
```

5. Если восстановление невозможно:

```text
manual_review_required
```

6. Не исправлять generated reports в outputs.

## Команда для Codex

```text
Выполни P3.PRE.2 Docs mojibake/encoding audit and UTF-8 normalization.

Не начинай P3.0 source acquisition до завершения этого этапа.

Создай docs/00_project/p3_docs_encoding_audit_report.md.

Проверь:
- README.md
- CHANGELOG.md
- docs/**/*.md
- prompts/**/*.md
- tools/**/*.md

Исключи:
- outputs/
- releases/
- .venv/
- .git/
- data/raw/*.xlsx
- binary files

Найди mojibake patterns:
Р”, Р°, Рџ, РЎ, Рµ, РЅ, СЃ, С‚, СЊ, вЂ, â€, Ð, Ñ.

Для каждого документа запиши:
path, encoding_detected, mojibake_detected, action, notes.

Активные документы с очевидным mojibake приведи к UTF-8.
Архивные документы можно помечать archived_no_change.
Если восстановление текста рискованно — manual_review_required.

Не запускай full quality gate.
```

## Проверки

Если создан Python helper:

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\audit_docs_encoding.py
.\.venv\Scripts\python.exe scripts\maintenance\audit_docs_encoding.py --report
```

Docs-only check:

```powershell
git diff --name-only
```

Проверить, что не затронуты generated outputs:

```powershell
git diff --name-only | Select-String "outputs|releases|logs|data/processed"
```

## Commit

```powershell
git add README.md CHANGELOG.md docs prompts tools scripts/maintenance/audit_docs_encoding.py docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Normalize documentation encoding before P3"
git push
```

Добавлять только реально измененные файлы. Не использовать `git add .`.

# P3.0 — Source acquisition design

## Статус

Начинать только после P3.PRE.1 и P3.PRE.2.

## Цель

Спроектировать controlled acquisition исходных Excel-таблиц Минфина перед data audit.

## Выбранная политика

Обязательно использовать Variant C:

```text
hybrid latest + final + version snapshots on hash change
```

## Источник

```text
https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/#tablitsy_po_rezultatam_provedeniya_auktsionov
```

Заголовки:

```text
Результаты проведенных аукционов по размещению государственных ценных бумаг в...
```

Файлы:

```text
INTERNET_Auction_Results_rus_<year>_....xlsx
```

## Storage structure

```text
data/raw/minfin/ofz_auction_results/
  latest/
  versions/
  final/
  registry/
```

## Git policy

Tracked:

```text
latest/
final/
registry/
```

External/ignored by default:

```text
versions/
```

Если versions решено коммитить, нужен отдельный artifact policy decision.

## Design docs to create

```text
docs/02_data_contracts/minfin_source_registry_contract.md
docs/07_operations/minfin_source_acquisition.md
docs/00_project/p3_source_data_roadmap.md
```

## Registry fields

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
```

## Future CLI

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --dry-run
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --download
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2025 --mode annual-final --download
```

## Command for Codex

```text
Выполни P3.0 Source acquisition design.

Перед началом подтверди, что P3.PRE.1 и P3.PRE.2 completed или явно deferred пользователем.

Не пиши downloader code на этом этапе.

Создай:
- docs/02_data_contracts/minfin_source_registry_contract.md
- docs/07_operations/minfin_source_acquisition.md
- docs/00_project/p3_source_data_roadmap.md

Зафиксируй Variant C:
hybrid latest + final + version snapshots on hash change.

Опиши:
- monthly lifecycle;
- January annual-final lifecycle;
- storage structure;
- Git/artifact policy;
- registry fields;
- future CLI;
- future integration source acquisition -> raw registry -> data audit -> cleaning;
- failure behavior when Minfin site unavailable;
- manual fallback URL/file import.
```

## Checks

Docs-only:

```powershell
git diff --name-only
staged generated artifacts check
```

## Commit

```powershell
git add docs/02_data_contracts/minfin_source_registry_contract.md docs/07_operations/minfin_source_acquisition.md docs/00_project/p3_source_data_roadmap.md docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Design Minfin source acquisition workflow"
git push
```

# P3.1 — Minfin downloader MVP

## Цель

Создать downloader dry-run/download MVP без интеграции в основной pipeline.

## Files

```text
scripts/source_acquisition/__init__.py
scripts/source_acquisition/minfin_auction_tables.py
scripts/source_acquisition/source_registry.py
```

Добавить CLI entry point:

```toml
ofz-fetch-minfin = "scripts.source_acquisition.minfin_auction_tables:main"
```

## Requirements

Downloader должен:

```text
- иметь --dry-run;
- иметь --download;
- принимать --year;
- принимать --mode monthly|annual-final;
- принимать --url override;
- принимать --output-root;
- иметь retry/timeout/user-agent;
- корректно обрабатывать 503/network errors;
- находить Excel links по title/file pattern;
- не заменять latest без hash compare;
- сохранять version snapshot только при hash change;
- обновлять registry;
- писать source acquisition report в outputs/reports/source_acquisition/.
```

## Safety

```text
Default = dry-run.
Download requires --download.
No pipeline integration yet.
No generated reports committed.
No temp files committed.
Network failure is not pipeline failure unless command explicitly requested download.
```

## Checks

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\source_acquisition\minfin_auction_tables.py scripts\source_acquisition\source_registry.py
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\python.exe scripts\source_acquisition\minfin_auction_tables.py --year 2026 --mode monthly --dry-run
```

If package changed:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\ofz-fetch-minfin.exe --help
```

Do not run real download unless user approves.

## Commit

```powershell
git add scripts/source_acquisition pyproject.toml docs README.md docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Add Minfin auction table downloader MVP"
git push
```

# P3.2 — Source registry and revision report

## Цель

Довести registry/revision reporting до production-ready.

## Outputs

Generated, not committed:

```text
outputs/reports/source_acquisition/minfin_source_revision_report_<timestamp>.md
outputs/reports/source_acquisition/minfin_source_revision_report_<timestamp>.json
```

Tracked, if policy allows:

```text
data/raw/minfin/ofz_auction_results/registry/minfin_auction_files_registry.csv
data/raw/minfin/ofz_auction_results/registry/minfin_auction_files_registry.json
```

## Requirements

Registry должен позволять ответить:

```text
- какой файл активен для pipeline;
- какой hash у active latest/final;
- когда файл скачан;
- какой snapshot superseded;
- изменился ли hash;
- является ли год annual_final;
- какие years покрыты;
- какие скачивания failed/skipped.
```

## Checks

```powershell
.\.venv\Scripts\python.exe scripts\source_acquisition\minfin_auction_tables.py --year 2026 --mode monthly --dry-run
.\.venv\Scripts\python.exe scripts\source_acquisition\minfin_auction_tables.py --year 2025 --mode annual-final --dry-run
```

## Commit

```powershell
git add scripts/source_acquisition docs data/raw/minfin/ofz_auction_results/registry docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Add Minfin source registry and revision reporting"
git push
```

Do not add `versions/` unless policy changed.

# P3.3 — Integrate source registry into data audit

## Цель

`01_data_audit.py` должен проверять source registry до анализа данных.

## Requirements

Data audit должен проверять:

```text
- active raw file exists;
- active raw file sha256 matches registry;
- expected years coverage;
- current year has latest;
- closed years have final where expected;
- no mixed old/new file ambiguity;
- registry status is clear.
```

If registry missing:

```text
warn or fail depending on strict mode
```

Add CLI option if needed:

```text
--strict-source-registry
--allow-missing-source-registry
```

Default behavior should not break legacy runs until migration completed.

## Checks

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\01_data_audit.py
.\.venv\Scripts\python.exe scripts\01_data_audit.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Commit

```powershell
git add scripts docs docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Integrate Minfin source registry into data audit"
git push
```

# P3.4 — Parser QA fixtures/tests

## Цель

Проверить source parser без зависимости от живого сайта Минфина.

## Fixtures

```text
tests/fixtures/minfin_auction_page_sample.html
tests/fixtures/minfin_auction_links_sample.json
tests/fixtures/minfin_registry_sample.json
```

If no tests framework exists, create lightweight script:

```text
scripts/qa/minfin_source_acquisition_tests.py
```

## Test cases

```text
- finds title pattern;
- finds INTERNET_Auction_Results_rus_<year> files;
- selects target year;
- handles several matching links;
- handles no matching links;
- handles 503;
- detects hash unchanged;
- detects hash changed;
- marks annual-final correctly.
```

## Checks

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\qa\minfin_source_acquisition_tests.py
.\.venv\Scripts\python.exe scripts\qa\minfin_source_acquisition_tests.py
```

## Commit

```powershell
git add tests/fixtures scripts/qa docs docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md
git commit -m "Add Minfin source acquisition QA fixtures"
git push
```

# P3.5 — Operator schedule / monthly-final procedure

## Цель

Описать эксплуатационный процесс.

## Docs

```text
docs/07_operations/minfin_monthly_update_procedure.md
```

## Procedure

Monthly:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode monthly --dry-run
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY --mode monthly --download
.\.venv\Scripts\ofz-quality.exe --fast --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

January annual-final:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY-1 --mode annual-final --dry-run
.\.venv\Scripts\ofz-fetch-minfin.exe --year YYYY-1 --mode annual-final --download
```

Manual fallback:

```text
download XLSX manually
place into temp/import folder
run ofz-fetch-minfin --from-file <path> --year YYYY --mode monthly
```

## Optional scheduling

Document only:

```text
Windows Task Scheduler plan
GitHub Actions manual workflow plan
```

Do not implement automatic scheduled download without separate approval.

## Commit

```powershell
git add docs/07_operations/minfin_monthly_update_procedure.md docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md README.md
git commit -m "Document Minfin monthly update procedure"
git push
```

# P3.REL.1 — Stable release procedure update

## Цель

Обновить release procedure с учетом source acquisition.

## Docs

```text
docs/07_operations/stable_release_procedure.md
```

Include:

```text
1. source acquisition dry-run;
2. monthly or annual-final source update;
3. registry audit;
4. data audit;
5. quality-fast;
6. screenshot validation outside sandbox;
7. quality-full;
8. release bundle build;
9. optional BI package;
10. tag;
11. gh release create/upload only by explicit approval.
```

## Commit

```powershell
git add docs/07_operations/stable_release_procedure.md docs/00_project/p3_modernization_progress_report.md docs/06_quality/manual_checks_log.md README.md
git commit -m "Document stable release procedure with source acquisition"
git push
```

## Финальный отчет Codex после каждого этапа

Формат:

```text
1. Этап.
2. Статус.
3. Что изменено.
4. Проверочный уровень.
5. Проверки выполнены.
6. Проверки skipped и почему.
7. Warnings.
8. Commits.
9. Push.
10. Git status.
11. Подтверждения:
    - generated outputs not staged;
    - releases not staged;
    - data/raw policy respected;
    - UTF-8 policy respected;
    - token/cost-aware mode respected.
12. Следующий рекомендуемый этап.
```
