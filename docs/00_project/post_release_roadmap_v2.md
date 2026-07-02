# Post-release roadmap v2

Дата: 2026-07-02

## 1. Текущий статус релиза

Проект находится после stable release `v0.1.0` и серии post-release hardening шагов.

Уже выполнено:

- telemetry hardening;
- первая и вторая малые итерации Chart/QA decomposition;
- source registry strict migration plan;
- strict CLI plumbing для `ofz-run`;
- strict/no-legacy full pipeline precheck;
- approval request для возможного strict default switch;
- raw versions policy cleanup по варианту B;
- monthly operation rehearsal после strict plumbing;
- BI package handoff dry-run.

Текущий production-compatible default source registry policy остается:

```text
source-registry-mode=warn
allow-legacy-raw=true
```

Strict-by-default не включен и не должен включаться без отдельного явного approval.

## 2. Что завершено после релиза

### Source registry

- `ofz-run` принимает `--source-registry-mode off|warn|strict`.
- `ofz-run` принимает `--allow-legacy-raw` и `--no-allow-legacy-raw`.
- Stage 1 `scripts/01_data_audit.py` получает registry flags из pipeline.
- GUI command builder передает выбранный registry mode и legacy checkbox state в pipeline command.
- Strict/no-legacy full pipeline precheck прошел успешно.
- Default policy намеренно не менялась.

### Raw versions

- Принят и применен вариант B: historical tracked Minfin version snapshot снят из Git tracking через `git rm --cached`.
- Физический файл оставлен локально.
- `data/raw/minfin/ofz_auction_results/versions/` добавлен в `.gitignore`.
- Future version snapshots остаются local/external artifacts и не должны попадать в staging.

### Monthly operations

- Monthly rehearsal выполнен без raw mutation.
- Minfin monthly dry-run безопасно завершился без download/import.
- Pipeline `warn + allow-legacy-raw` прошел.
- Pipeline `strict + no-allow-legacy-raw` прошел как явный контрольный режим.
- `ofz-quality --fast` прошел.
- GUI smoke checks прошли; manual GUI rehearsal остается операторским действием.

### BI handoff

- Entry point `ofz-build-bi-package.exe` отсутствует.
- Fallback `scripts/maintenance/build_bi_package.py` доступен.
- BI package dry-run прошел и подтвердил состав пакета.
- Реальная BI-сборка не выполнялась, потому что требует отдельного approval и confirm token.

### Chart/QA decomposition

- `scripts/charts/export_utils.py` вынес общие helper-функции записи HTML/CSV artifacts.
- `scripts/charts/chart_metadata.py` вынес suffix/routing helpers для chart artifacts.
- `scripts/06_build_charts.py` сохранил wrapper compatibility.
- Методология, output paths, filenames, chart semantics и yield/boxplot scope не менялись.

## 3. Оставшиеся blockers

На текущем этапе нет blocker для обычного совместимого pipeline режима `warn + allow-legacy-raw`.

Остаются controlled decisions:

- strict default switch: только после отдельного approval;
- real BI package build: только после отдельного approval;
- live Minfin download/import/replacement: только после отдельного approval;
- release bundle/tag/release asset operations: только после отдельного approval;
- дальнейшая физическая декомпозиция chart/QA монолитов: только малыми behavior-neutral шагами.

Технические ограничения:

- visual regression в managed Codex среде использует fallback, потому что screenshot backend недоступен;
- интерактивные GUI проверки остаются manual operator checks;
- generated outputs, telemetry, run manifests, logs, releases, `data/processed`, raw versions и `.ofz_launcher` не коммитятся.

## 4. Strict registry roadmap

Текущий статус: strict-ready для явных precheck запусков, но не strict-by-default.

Следующие варианты:

1. Оставить default как есть.
   - Рекомендуемый безопасный режим для обычной эксплуатации.
   - Явные strict/no-legacy команды доступны для precheck и monthly rehearsal.

2. Подготовить manual GUI strict/no-legacy rehearsal.
   - Проверить registry mode labels.
   - Проверить pipeline command preview.
   - Проверить запуск pipeline strict/no-legacy через GUI.
   - Проверить понятность journal/result messages.

3. Только после явного approval переключить default.
   - Изменить defaults в `scripts/run_pipeline.py`.
   - Изменить GUI defaults.
   - Обновить operator docs и release checklist.
   - Повторить full local gate.

Rollback должен возвращать:

```text
source-registry-mode=warn
allow-legacy-raw=true
```

## 5. GUI roadmap

Ближайшие безопасные задачи:

- выполнить ручной strict/no-legacy GUI rehearsal;
- проверить, что warning/default labels не подталкивают к strict-by-default без approval;
- улучшить summary messages для Minfin dry-run при сетевой недоступности;
- проверить command preview для BI dry-run и real build guarded mode;
- сохранить `.ofz_launcher` как local runtime state вне Git.

Не делать в рамках GUI roadmap без отдельного approval:

- destructive cleanup;
- real raw import/download/replacement;
- release build;
- BI build;
- switch defaults to strict/no-legacy.

## 6. Chart/QA decomposition roadmap

Правило: один малый extraction на commit.

Уже сделано:

- `scripts/charts/export_utils.py`;
- `scripts/charts/chart_metadata.py`;
- `scripts/qa/html_chart_contracts.py`;
- `scripts/qa/visual_regression_contracts.py`.

Следующие кандидаты:

- `scripts/charts/label_policy.py` только после contract snapshot по title/tooltip/yield scope;
- `scripts/qa/chart_contract_helpers.py` для HTML QA helper-функций;
- небольшой блок visual regression backend/manifest helpers после отдельного smoke.

Не начинать пока:

- yield/boxplot methodology changes;
- scatter label policy semantic changes;
- output path/name changes;
- массовый перенос chart families.

## 7. BI handoff

Текущий статус: dry-run validated.

Следующий шаг только после approval:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --include-outputs --confirm BUILD_BI_PACKAGE --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

BI artifacts должны оставаться вне Git staging.

Перед реальной сборкой желательно:

- выполнить свежий `ofz-run` на целевом report scope;
- выполнить `ofz-quality --fast`;
- проверить, что `releases/bi/` не попадает в staging;
- зафиксировать handoff artifact location в отдельном operator note.

## 8. Monthly operations

Рекомендуемый monthly workflow до strict default approval:

1. Minfin monthly dry-run:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --dry-run --timeout-seconds 20 --retries 1
```

2. Pipeline в текущем compatible default режиме:

```powershell
.\.venv\Scripts\ofz-run.exe --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --source-registry-mode warn --allow-legacy-raw
```

3. Quality-fast:

```powershell
.\.venv\Scripts\ofz-quality.exe --fast --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

4. Optional strict precheck:

```powershell
.\.venv\Scripts\ofz-run.exe --report-date YYYY-MM-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --source-registry-mode strict --no-allow-legacy-raw
```

Raw/source mutation выполняется только через controlled source acquisition workflows и только после отдельного approval.

## 9. Optional installer/Docker

Эти направления остаются optional и не являются blocker для текущего post-release состояния:

- Windows installer;
- Docker/devcontainer;
- packaged GUI launcher;
- packaged BI handoff runner.

Перед началом любого packaging шага нужно отдельно зафиксировать:

- целевую аудиторию;
- supported OS/runtime;
- список включаемых и исключаемых artifacts;
- release/build approval gate;
- artifact guard для `releases/`, logs, outputs и local runtime directories.

## 10. Deferred ideas

Отложено:

- strict-by-default implementation без approval;
- real BI package build без approval;
- live Minfin update без approval;
- release bundle/tag/release asset operations без approval;
- крупная физическая декомпозиция chart/QA modules;
- методологические изменения yield/discount/boxplot;
- автоматическая интерактивная GUI проверка в Codex managed session;
- перенос historical generated reports из skip-worktree состояния.

## 11. Ближайший рекомендуемый NEXT

После NEXT.15 безопасные следующие варианты:

1. `NEXT.16 - GUI manual strict/no-legacy rehearsal report`.
2. `NEXT.17 - BI package real build approval request`.
3. `NEXT.18 - Chart/QA decomposition iteration 3`.
4. `NEXT.19 - Monthly operation procedure cleanup`.

Рекомендуемый следующий шаг: GUI manual strict/no-legacy rehearsal report, потому что он закрывает последний практический gap перед возможным решением по strict default switch.
