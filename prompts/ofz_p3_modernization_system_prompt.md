# OFZ_ANALYTICS: P3 modernization system prompt
## Source acquisition, pre-P3 audit, UTF-8 normalization, token-aware execution

Дата актуализации: 2026-06-16.

## 1. Роль Codex

Ты работаешь с проектом `OFZ_ANALYTICS`.

Текущий подтвержденный статус после P2:

```text
P2 modernization completed.
Project status: stable-release-candidate.
Production-ready candidate preserved.
Generated outputs and release artifacts are outside normal Git history.
Final close-out checks passed.
```

P3 не должен ломать P2. P3 должен добавить управляемый контур получения исходных данных Минфина и перед этим закрыть технические долги:

```text
P3.PRE.1 scripts balance/problem audit
P3.PRE.2 docs mojibake/encoding audit and UTF-8 normalization
P3.0 source acquisition design
P3.1 Minfin downloader MVP
P3.2 source registry and revision report
P3.3 data audit integration
P3.4 parser QA fixtures/tests
P3.5 operator schedule / monthly-final procedure
```

Работай маленькими этапами: один этап, targeted checks, progress report, commit, push.

## 2. Источники статуса

Перед началом P3 прочитай:

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

Если документы отсутствуют или противоречат Git-состоянию, остановись и зафиксируй mismatch.

## 3. Обязательный P3 progress report

Создать и далее вести:

```text
docs/00_project/p3_modernization_progress_report.md
```

После каждого P3-этапа добавлять секцию:

```markdown
## P3.X - <Название этапа>

Дата: YYYY-MM-DD.

### 1. Статус этапа
completed / partial / blocked / deferred / rolled back

### 2. Что изменено
### 3. Какие проверки выполнены
### 4. Какие проверки skipped и почему
### 5. Какие проверки упали
### 6. Warnings documented
### 7. Какие файлы изменены
### 8. Какие commits созданы
### 9. Был ли push
### 10. Текущий git status
### 11. Подтверждения
- generated outputs not staged:
- releases not staged:
- data/raw policy respected:
- CLI entry points still work or not required:
- GitHub CLI auth OK or not used:
- encoding policy respected:
- token/cost-aware mode respected:
### 12. Следующий рекомендуемый этап
```

Если этап не завершен, нельзя писать `completed`.

## 4. Документ по каждому аудируемому документу

Для P3.PRE.2 обязательно создать отдельный отчет:

```text
docs/00_project/p3_docs_encoding_audit_report.md
```

В нем по каждому проверенному документу должна быть строка:

```text
path
encoding_detected
status
mojibake_detected
action
notes
```

Где `action`:

```text
no_change
converted_to_utf8
manual_review_required
skipped_binary_or_generated
archived_no_change
```

Не исправлять документы вслепую. Если есть риск смысловой порчи, пометить `manual_review_required`.

## 5. Отчет по аудиту скриптов

Для P3.PRE.1 обязательно создать:

```text
docs/00_project/p3_scripts_balance_audit_report.md
```

Проверять:

```text
- чрезмерно большие скрипты;
- дублирование функций;
- archived scripts, которые всё еще импортируются;
- TODO/FIXME/XXX;
- hardcoded absolute paths;
- unsafe shell execution;
- subprocess shell=True;
- direct generated outputs writes outside policy;
- data/raw mutation outside source-acquisition/data-cleaning policy;
- missing main() in CLI-like scripts;
- encoding declaration issues;
- dependency drift;
- suspicious dead wrappers;
- typos in stage names / CLI references;
- balance проблем: когда часть логики уже вынесена в module skeleton, но wrapper всё еще содержит основную бизнес-логику.
```

По каждому найденному issue указать:

```text
issue_id
file
severity: low / medium / high / blocker
category
description
recommended_action
fixed_now: yes/no
commit
notes
```

## 6. Token-aware / cost-aware политика

Работай в режиме экономии токенов и проверок.

### 6.1. Session preflight один раз

В начале сессии:

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics

git status --short --branch
git branch --show-current
git remote -v
git log --oneline -10

gh --version
gh auth status
gh repo view VinogradovPV/OFZ_ANALYTICS

.\.venv\Scripts\ofz-run.exe --help
.\.venv\Scripts\ofz-quality.exe --help
.\.venv\Scripts\ofz-schema.exe --help
.\.venv\Scripts\ofz-build-release-bundle.exe --help
```

Не повторять эти проверки в той же сессии, если не менялись:

```text
pyproject.toml
requirements*.txt
CLI entry points
Git remote/auth
pipeline/quality/schema/release scripts
```

### 6.2. Не перечитывать большие документы полностью без причины

Для больших отчетов:

```text
1. Сначала использовать поиск по нужным секциям.
2. Читать только релевантные фрагменты.
3. Не переписывать целиком long progress reports.
4. Для итогового статуса использовать p2_completion_report.md как source of truth, если он согласуется с Git.
```

### 6.3. Проверки по уровням

Docs-only:

```text
git diff / staged generated artifacts check
без compileall / quality gate
```

Python utility changed:

```text
py_compile changed files
compileall scripts, если затронуты imports
```

Pipeline/source acquisition changed:

```text
targeted tests
dry-run
quality-fast только если затронут production path
```

Final/stable release:

```text
full gate только по явной необходимости
```

## 7. Git / GitHub outside-sandbox policy

Git/GitHub команды выполнять только из корня проекта:

```powershell
cd C:\Users\Rockaudit\LLM_CHAT\ofz_analytics
```

Если sandbox не видит `.git` или credentials, выполнять Git/GitHub outside-sandbox точечно.

Разрешено без отдельного подтверждения:

```powershell
gh --version
gh auth status
gh repo view VinogradovPV/OFZ_ANALYTICS
gh run list
gh run view
gh workflow list
```

Требует отдельного разрешения:

```powershell
gh pr create
gh pr merge
gh release create
gh release upload
gh workflow run
gh secret set
gh variable set
gh repo edit
```

Запрещено:

```text
gh repo delete
gh repo edit --visibility public
force push
commit generated outputs
commit releases
commit browser binaries
commit .docm without explicit policy approval
```

## 8. P3 source acquisition policy: Variant C

Для Минфина выбран **Variant C: hybrid latest + final + version snapshots on hash change**.

Это обязательное решение P3.

### 8.1. Источник

Страница:

```text
https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/auction/#tablitsy_po_rezultatam_provedeniya_auktsionov
```

Паттерн заголовков:

```text
Результаты проведенных аукционов по размещению государственных ценных бумаг в...
```

Паттерн файлов:

```text
INTERNET_Auction_Results_rus_<year>_....xlsx
```

### 8.2. Business lifecycle

Минфин публикует данные ежемесячно.

Каждый месяц:

```text
- скачать актуальный файл текущего года;
- сравнить hash с предыдущим latest;
- если hash изменился, сохранить version snapshot;
- заменить latest текущего года;
- обновить registry.
```

В январе следующего года:

```text
- скачать итоговый/обновленный файл за предыдущий год;
- сравнить hash;
- сохранить final snapshot;
- заменить/обновить final-файл предыдущего года;
- обновить registry;
- пометить год как annual_final/closed.
```

### 8.3. Storage structure

```text
data/raw/minfin/ofz_auction_results/
  latest/
    INTERNET_Auction_Results_rus_2026_latest.xlsx

  versions/
    2026/
      INTERNET_Auction_Results_rus_2026_downloaded_2026-06-16_sha256_<short>.xlsx

  final/
    INTERNET_Auction_Results_rus_2025_final_downloaded_2026-01-xx_sha256_<short>.xlsx

  registry/
    minfin_auction_files_registry.csv
    minfin_auction_files_registry.json
```

### 8.4. Git/artifact policy

Рекомендуемая политика:

```text
Tracked in Git:
- latest/
- final/
- registry/

Ignored or external artifact by default:
- versions/
```

Причина: pipeline воспроизводим по active latest/final и registry, но snapshot history не раздувает Git. Если позже решено коммитить versions, нужен отдельный artifact policy decision.

Guardrails:

```text
- no individual raw file > 50 MB;
- warn if total raw/minfin versions > 200 MB;
- no generated outputs committed;
- no downloaded temp files committed;
- registry must record hashes for every active/snapshot/final file.
```

## 9. P3 этапы

Актуальный порядок:

```text
P3.PRE.1 Scripts balance/problem audit
P3.PRE.2 Docs mojibake/encoding audit and UTF-8 normalization
P3.0 Source acquisition design
P3.1 Minfin downloader MVP
P3.2 Source registry and revision report
P3.3 Data audit integration
P3.4 Parser QA fixtures/tests
P3.5 Operator schedule / monthly-final procedure
P3.REL.1 Stable release procedure update
```

Не начинать `P3.0` до закрытия `P3.PRE.1` и `P3.PRE.2`, если пользователь не дал отдельное разрешение.

## 10. Инварианты P3

Запрещено:

```text
- менять data/raw вручную вне P3 source acquisition scripts;
- скачивать и заменять raw files без dry-run и registry update;
- удалять старые raw files без registry history;
- silently overwrite current-year latest without hash comparison;
- silently replace annual final without registry entry;
- коммитить outputs/reports/source_acquisition;
- коммитить temp downloads;
- ломать существующий data audit;
- делать network access обязательным для обычного ofz-run;
- падать всем pipeline из-за недоступности сайта Минфина, если fetch не был явно requested.
```

## 11. Финальный отчет Codex после каждого этапа

Каждый ответ Codex должен содержать:

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
