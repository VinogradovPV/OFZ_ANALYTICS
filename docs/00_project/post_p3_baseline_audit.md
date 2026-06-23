# POSTP3.0 Baseline and contradiction audit

Дата: 2026-06-23.

Статус: audit-only. Код, raw storage, generated outputs, release bundles и GUI runtime state не изменялись.

## Прочитанные источники

- `prompts/ofz_post_p3_optimization_system_prompt.md`
- `prompts/ofz_post_p3_optimization_step_by_step.md`
- `README.md`
- `docs/00_project/p3_modernization_progress_report.md`
- `docs/06_quality/manual_checks_log.md`
- `docs/07_operations/gui_launcher.md`
- `docs/07_operations/minfin_source_acquisition.md`
- `docs/07_operations/minfin_monthly_update_procedure.md`
- `docs/07_operations/release_checklist.md`
- `docs/07_operations/stable_release_procedure.md`
- `docs/02_data_contracts/minfin_source_registry_contract.md`
- `docs/00_project/outputs_structure.md`
- `pyproject.toml`
- `.github/workflows/quality.yml`
- `.gitignore`

## Текущее состояние репозитория и CI

- Branch: `main`.
- Последние commits перед audit: `4bca5d6`, `85b39e4`, `83edba3`, `3e8be2c`, `a4bc06c`.
- Последние пять GitHub Actions runs до POSTP3.0 были успешными.
- До audit в рабочей копии уже были local changes и untracked generated artifacts: raw/latest/registry changes, `data/raw/minfin/ofz_auction_results/versions/`, `outputs/`, untracked prompt files и часть generated/report docs. Эти изменения не относятся к POSTP3.0 и не должны попасть в commit.
- Локальная папка `.ofz_launcher` существует и должна оставаться вне Git.
- POSTP3.0 UTF-8 scanner завершился с FAIL из-за существующего untracked prompt `prompts/ofz_gui_launcher_user_friendly_status_and_navigation_fix_ru.md`, где найден `U+FFFD`.

## Что реально завершено в P3

1. Source acquisition Минфина:
   - создан `ofz-fetch-minfin`;
   - реализован HTML-aware parser для section `id_66`, pagination `page_66`, container `ajax-pagination-content-10090-66`;
   - sections `65`, `38`, `39` игнорируются;
   - XLSX извлекаются из `a.file_item`;
   - relative URLs резолвятся от `https://minfin.gov.ru`;
   - monthly candidate выбирается по title с `на DD.MM.YYYY`;
   - annual-final не требует суффикс `YYYY1231`;
   - реализованы monthly download workflow, annual-final workflow и manual-import workflow с confirm tokens.

2. Source registry:
   - реализованы CSV/JSON writer/reader, SHA-256/file size helpers, active row selection, superseded rows и validation;
   - добавлены HTML provenance поля;
   - data audit получил `--source-registry-mode off|warn|strict` и `--allow-legacy-raw`;
   - default остается совместимым: `warn + allow-legacy-raw`;
   - controlled source пока validation-only и не заменяет legacy Excel input selection.

3. QA fixtures/tests:
   - добавлены offline fixtures для parser, pagination, wrong sections, hash changed/unchanged, annual-final и manual-import failure modes;
   - тесты не обращаются к live site и не меняют настоящий `data/raw`.

4. Операционная документация:
   - создана monthly/final update procedure;
   - stable release procedure обновлена с source acquisition dry-run/update, registry review, data audit, quality gates, screenshot validation, release bundle и GitHub release только по отдельному разрешению.

5. UTF-8 / Mojibake policy:
   - создан `scripts/qa/check_text_encoding.py`;
   - stage `encoding-mojibake` встроен в `ofz-quality` и GitHub Actions;
   - invalid UTF-8 и mojibake считаются release blockers.

6. Yield metrics:
   - базовые yield metrics переведены на scope `ОФЗ-ПД` only;
   - ОФЗ-ПК и ОФЗ-ИН не попадают в numerator/denominator доходности и min/median/max;
   - ОФЗ-ПК сохранен в volume breakdown;
   - ожидаемая regression-точка за ноябрь 2025: weighted около `14.873469`, min `14.73`, median `14.75`, max `14.95`.

7. Desktop GUI:
   - добавлен Python tkinter entry point `ofz-gui`;
   - реализованы девять вкладок: обзор, Минфин, pipeline, quality, reports, release, maintenance, журнал и справка;
   - command runner использует allowlist, `shell=False`, background thread, UTF-8 logs, stop и запрет параллельных запусков;
   - dangerous actions защищены typed confirm;
   - GUI logs перенесены в `.ofz_launcher/logs/`;
   - PowerShell wrapper стал thin launcher.

## Какие проверки прошли

По stage reports и manual checks log подтверждены:

- `py_compile` и `compileall` для source acquisition, data audit integration, GUI и related smoke scripts;
- `pip install -e .` и `pip check` на GUI/quality этапах;
- `ofz-fetch-minfin --help`, no-network dry-run и offline `--html-file` dry-run;
- monthly, annual-final, manual-import, registry writer, parser QA и data audit registry smoke tests;
- `ofz-quality --fast` после P3.6 registry integration;
- UTF-8/mojibake scanner и отдельный encoding quality stage;
- full pipeline/schema/html QA/visual fallback при исправлении yield metrics;
- GUI smoke: `gui_launcher_smoke.py`, `gui_command_runner_smoke.py`, `ofz-gui --smoke`, `ofz-gui --smoke-ui`;
- GitHub Actions latest runs до POSTP3.0: green.

## Какие проверки были пропущены или требуют подтверждения

- Live Minfin download не выполнялся в исходных P3 stages без отдельного разрешения; текущее локальное изменение raw/registry требует отдельного operator decision и не входит в audit.
- `REPLACE_MINFIN_FINAL`, `IMPORT_MINFIN_FILE`, `BUILD_RELEASE_BUNDLE`, `BUILD_BI_PACKAGE`, `DELETE_OUTPUTS` как production/dangerous действия не подтверждены как release-ready workflows.
- `ofz-quality --full` после всех GUI/cleanup/yield/docs изменений не зафиксирован как финальный release gate.
- Screenshot backend outside sandbox не подтвержден; visual regression в managed sandbox мог использовать fallback.
- GUI automated smoke прошел, но финальная ручная UX/layout validation в интерактивном окне остается незакрытой.
- Strict source-registry mode на production registry не принят как default migration gate.
- Release bundle dry-run/build и BI package build после всех P3 изменений не подтверждены как выполненные для release-candidate.

## Dangerous actions, которые не выполнялись в POSTP3.0

- Live Minfin download.
- Annual-final replacement.
- Manual import external XLSX.
- Delete outputs.
- Release bundle build.
- BI package build.
- Git tag.
- `gh release create` / `gh release upload`.

## Противоречия и устаревшие записи

### `outputs/charts/index.md`

Актуальное состояние:

- `outputs/charts/index.md` отсутствует в рабочем дереве.
- `docs/00_project/outputs_structure.md` существует.
- `scripts/quality_gate.py` в `check_charts_structure` требует `docs/00_project/outputs_structure.md` и ключевые generated categories under `outputs/charts/`; generated `outputs/charts/index.md` не является required source artifact.
- `docs/00_project/p3_modernization_progress_report.md` и свежие GUI/manual logs фиксируют, что quality gate больше не требует generated `outputs/charts/index.md`.

Оставшиеся устаревшие references:

- `README.md` все еще пишет, что карта графиков находится в `outputs/charts/index.md`.
- `README.md` также допускает lightweight navigation files such as `outputs/charts/index.md` как часть skeleton policy.
- `docs/index.md` содержит ссылку на `../outputs/charts/index.md`.
- `scripts/README.md` упоминает индекс графиков в `outputs/charts/index.md`.
- Исторические entries в `docs/06_quality/manual_checks_log.md` и `docs/00_project/p3_modernization_progress_report.md` все еще содержат старый blocker wording про удаленный `outputs/charts/index.md`.

Вывод: текущий code gate уже соответствует новой policy, но активная документация содержит stale references. Это не чинится в POSTP3.0, а становится первым предметом POSTP3.1.

### GUI logs

- Активные GUI docs описывают `.ofz_launcher/logs/`.
- `release_checklist.md` еще содержит пункт про launcher logs under `outputs/reports/launcher/` как generated outputs. Это допустимо как legacy mention, но требует уточнения: новые Python GUI logs живут в `.ofz_launcher/logs/`, а старые launcher reports в `outputs/reports/launcher/` остаются generated.

### Source registry strict mode

- Контракт и P3.6 отчеты честно фиксируют default `warn + allow-legacy-raw`.
- Release/stable docs уже описывают strict pre-release gate, но migration на strict default еще не выполнена.
- Это не blocker для локальной совместимости, но blocker для статуса "strict registry-ready release-candidate".

## Что блокирует release-candidate

1. Нечистое рабочее дерево: есть local raw/registry/generated/output changes и untracked files, которые нужно классифицировать отдельно.
2. UTF-8/mojibake scanner падает на существующем untracked prompt с `U+FFFD`.
3. Активные docs содержат stale references на `outputs/charts/index.md`, хотя quality gate уже не должен требовать этот generated artifact.
4. Не подтвержден final `quality-full` после всех поздних GUI/cleanup/yield/docs изменений.
5. Не подтверждена screenshot validation outside sandbox.
6. GUI требует ручной UX/layout validation в интерактивном окне.
7. Source registry strict migration не завершен; default остается legacy-compatible.
8. Release bundle dry-run/build и optional BI package не подтверждены для финального release-candidate.
9. Dangerous workflows должны быть проверены через dry-run/confirm policy без попадания generated artifacts в Git.

## Generated artifacts и ignored dirs вне Git

Должны оставаться вне Git:

- `outputs/charts/`
- `outputs/exports/`
- `outputs/reports/`
- `outputs/dashboards/`
- `outputs/archive/`
- `outputs/tmp/`
- `outputs/cache/`
- `outputs/reports/source_acquisition/`
- `data/processed/`
- `logs/`
- `.ofz_launcher/`
- `releases/`
- `data/raw/minfin/ofz_auction_results/versions/`
- `*.docm`
- `*.tmp`
- `*.part`
- `*.crdownload`
- virtualenv/cache folders such as `.venv/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`.

Tracked controlled source paths remain a separate policy decision:

- `data/raw/minfin/ofz_auction_results/latest/`
- `data/raw/minfin/ofz_auction_results/final/`
- `data/raw/minfin/ofz_auction_results/registry/`

Они допустимы к commit только после controlled workflow review; `versions/` не коммитится.

## Нужные следующие этапы POSTP3

1. `POSTP3.1 Resolve quality-gate inconsistencies`:
   - сначала устранить текущий UTF-8 scanner FAIL в untracked prompt или принять явное решение о scope scanner;
   - убрать/обновить active references на `outputs/charts/index.md`;
   - подтвердить `ofz-quality --fast` на текущей policy.

2. `POSTP3.2 GUI real workflow validation and polish`:
   - выполнить интерактивный GUI smoke outside sandbox;
   - проверить layout, status summaries, cleanup dry-run/delete confirm и logs.

3. `POSTP3.3 Source registry strict-readiness`:
   - проверить production registry/latest/final rows;
   - подготовить решение, когда можно переходить от `warn` к `strict`.

4. `POSTP3.4 Minfin live acquisition hardening`:
   - проверить live dry-run, 503 handling и manual fallback;
   - не выполнять download без отдельного разрешения.

5. `POSTP3.5 Pipeline/data audit optimization`:
   - оценить telemetry, повторные чтения и safe skip/cache opportunities без изменения методологии.

6. `POSTP3.6 Chart/QA monolith decomposition planning`:
   - спланировать декомпозицию chart/QA scripts без одновременного изменения методологии.

7. `POSTP3.7 Release-candidate gate`:
   - выполнить финальный install/pip check/compileall/encoding/pipeline/schema/quality-fast/release dry-run;
   - зафиксировать screenshot/manual GUI/yield spot checks.
