# Production runbook

Дата актуализации: 2026-07-06.

Runbook описывает повторяемый production-запуск OFZ_ANALYTICS после стабилизации Git, artifact policy, CLI entry points и cleanup workflow.

## 1. Клонирование private GitHub repo

Репозиторий:

```powershell
git clone https://github.com/VinogradovPV/OFZ_ANALYTICS.git
cd OFZ_ANALYTICS
```

Ожидаемое состояние:

- repository visibility: private;
- default branch: `main`;
- `data/raw/` входит в Git как source dataset;
- generated outputs не входят в обычную Git-историю.

## 2. Создание и активация `.venv`

```powershell
.\.venv\Scripts\python.exe --version
```

Если `.venv` еще нет:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Все production-команды запускать из корня проекта.

## 3. Установка зависимостей

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .
```

Проверка окружения:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m compileall -q scripts
```

## 4. Проверка CLI

После активации `.venv` доступны короткие команды:

```powershell
ofz-run --help
ofz-interactive --help
ofz-quality --help
ofz-clean-outputs --help
ofz-schema --help
ofz-build-release-bundle --help
```

Если `.venv` не активирована, запускать entry points явно:

```powershell
.\.venv\Scripts\ofz-run.exe --help
.\.venv\Scripts\ofz-interactive.exe --help
.\.venv\Scripts\ofz-quality.exe --help
.\.venv\Scripts\ofz-clean-outputs.exe --help
.\.venv\Scripts\ofz-schema.exe --help
.\.venv\Scripts\ofz-build-release-bundle.exe --help
```

Fallback через Python scripts, если entry point executables недоступны:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --help
.\.venv\Scripts\python.exe scripts\interactive_pipeline.py --help
.\.venv\Scripts\python.exe scripts\quality_gate.py --help
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --help
.\.venv\Scripts\python.exe scripts\schema_validation.py --help
.\.venv\Scripts\python.exe scripts\maintenance\build_release_bundle.py --help
```

## 5. Проверка `data/raw`

`data/raw/` является source dataset проекта и tracked in Git. Pipeline и cleanup-команды не должны менять эти файлы.

Проверить состав:

```powershell
Get-ChildItem data/raw -Recurse -File | Select-Object FullName, Length
git ls-files data/raw
```

Raw hashes фиксируются через raw data registry и run manifest. При production-запуске сверять, что raw-файлы не были заменены случайно.

## 6. Reference datasets Банка России

Перед построением графика `ofz_pd_yield_key_rate` проверьте reference datasets ключевой ставки на вкладке GUI `Банк России`:

1. `Проверить сайт Банка России`.
2. `Обновить ключевую ставку` с confirm token `UPDATE_CBR_KEY_RATE`.
3. `Проверить reference datasets`.

Primary source - `https://cbr.ru/hd_base/KeyRate/`, HTML `table.data` с колонками `Дата` и `Ставка`. Generated files создаются в `data/processed/reference/` и не коммитятся:

```text
data/processed/reference/cbr_key_rate_daily.csv
data/processed/reference/cbr_key_rate_daily.meta.json
data/processed/reference/cbr_key_rate_monthly.csv
```

CLI dry-run для диагностики:

```powershell
.\.venv\Scripts\python.exe scripts\reference_data\cbr_key_rate.py --source web --from-date 01.01.2019 --to-date 02.07.2026 --dry-run
.\.venv\Scripts\python.exe scripts\qa\cbr_reference_status_smoke.py --check-current
```

XLSX fallback является legacy emergency diagnostics. Если metadata указывает на `xlsx_fallback`, отсутствующий `source_file` или legacy path `key_rate_inflation`, обновите key rate с сайта Банка России перед production pipeline.

## 7. Month cumulative pipeline

Базовый production-сценарий:

```powershell
ofz-run --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Fallback:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## 8. Year cumulative pipeline

```powershell
ofz-run --all --report-date 2026-01-01 --retrospective-years 4 --period-type year --aggregation-mode cumulative
```

Fallback:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-01-01 --retrospective-years 4 --period-type year --aggregation-mode cumulative
```

## 9. Interactive pipeline

```powershell
ofz-interactive
```

Fallback:

```powershell
.\.venv\Scripts\python.exe scripts\interactive_pipeline.py
```

Interactive launcher перед запуском проверяет generated outputs. Если outputs не пустые, он предлагает оставить outputs, выполнить dry-run cleanup, архивировать и очистить, очистить без архива или отменить запуск. Launcher не удаляет файлы напрямую: cleanup делегируется `scripts/maintenance/cleanup_outputs.py`.

## 10. Очистка outputs

Dry-run:

```powershell
ofz-clean-outputs --dry-run
```

Архивировать текущие working outputs:

```powershell
ofz-clean-outputs --archive-all
```

Архивировать и очистить:

```powershell
ofz-clean-outputs --archive-all --delete-all --confirm DELETE_OUTPUTS
```

Fallback:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --dry-run
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all --delete-all --confirm DELETE_OUTPUTS
```

Полная очистка outputs удаляет generated artifacts, кроме сохраненного archive. Запускать только после dry-run и проверки archive policy.

## 11. Quality gate

Schema validation:

```powershell
ofz-schema --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Fast quality gate:

```powershell
ofz-quality --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Full quality gate для release:

```powershell
ofz-quality --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Fallback:

```powershell
.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## 12. Если `schema_validation` failed

1. Не править generated CSV вручную.
2. Открыть `docs/02_data_contracts/` и `scripts/schema_validation.py`.
3. Найти семейство export, которое нарушило contract.
4. Исправить generator, а не готовый файл.
5. Пересобрать соответствующий stage.
6. Повторить `ofz-schema` и `ofz-quality --fast`.

Особое правило: поля `*_volume_bln` должны иметь unit-поля со значением `млрд рублей`.

## 13. Если `quality_gate` failed

1. Прочитать `docs/06_quality/quality_gate_report.md`.
2. Разделить ошибку на data/schema/chart/visual/docs/scripts.
3. Запустить конкретный failing script отдельно.
4. Исправить source/generator/contract.
5. Не коммитить generated outputs.
6. Повторить `ofz-quality --fast`.

## 14. Если `visual_regression` failed

1. Проверить, это screenshot backend или fallback Plotly JSON inspection.
2. Открыть failing HTML chart локально.
3. Проверить подписи осей, legends, annotations, label density, hover и reference lines.
4. Исправить chart generator.
5. Пересобрать графики и повторить `ofz-quality --fast`.

## 15. Если Excel заблокирован

1. Закрыть Excel/LibreOffice/preview pane.
2. Убедиться, что нет временных файлов `~$*.xlsx`.
3. Не менять `data/raw/` вручную.
4. Повторить stage после снятия блокировки.

## 16. Процедура обновления raw data

1. Добавить новый raw-файл в `data/raw/`.
2. Проверить размер и отсутствие временных файлов.
3. Запустить raw data registry / data audit stage.
4. Проверить raw hashes в registry и run manifest.
5. Запустить pipeline и quality gate.
6. Коммитить raw source dataset только если данные не конфиденциальны и нужны для воспроизводимости.

## 17. Run manifest

Искать в:

- `outputs/reports/run_manifests/`;
- latest manifest, если он создан pipeline.

Manifest должен содержать:

- report params;
- commit hash;
- raw file hashes;
- key scripts hashes;
- outputs summary;
- QA statuses;
- cleanup fields: status, mode, return code, если запуск шел через interactive launcher.
- telemetry summary links: JSON and Markdown paths under `outputs/reports/telemetry/`.

Latest manifest может пересоздаваться. Release manifests сохранять как audit artifacts или включать в release bundle.

Telemetry summary создается автоматически при full pipeline run:

```powershell
ofz-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Файлы:

- `outputs/reports/telemetry/telemetry_<run_id>.json`;
- `outputs/reports/telemetry/telemetry_<run_id>.md`.

Telemetry outputs являются generated artifacts и не коммитятся.

Telemetry counters after NEXT.5:

- `raw_active_files_count` - active raw/source files excluding `registry/` and `versions/`;
- `raw_versions_files_count` - files under controlled raw `versions/`;
- `raw_file_scope_counts.registry` - source registry CSV/JSON files;
- `generated_current_files_count` - current generated outputs, excluding `outputs/archive`, `outputs/tmp` and `outputs/cache`;
- `generated_archive_files_count` - files under `outputs/archive`;
- `generated_tmp_cache_files_count` - files under `outputs/tmp` and `outputs/cache`;
- `stage_duration_seconds_precise` - per-stage duration from `perf_counter`.

Old broad counters such as `generated_artifacts_count` and `input_row_counts.raw_files` remain for backward compatibility, but operator performance review should prefer the scoped counters above.

## 18. Релизный пакет

Generated outputs не коммитятся. Для аудита конкретного запуска собрать release bundle / external artifact:

- HTML charts;
- chart data CSV;
- dashboard exports;
- run manifests;
- quality gate report;
- schema validation report;
- visual regression report;
- executive summary;
- data quality summary, если создан.

### 17.1 Автоматизация релизного пакета

Dry-run:

```powershell
ofz-build-release-bundle --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Release bundle creation:

```powershell
ofz-build-release-bundle --include-outputs --confirm BUILD_RELEASE_BUNDLE --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Fallback:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_release_bundle.py --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Bundle creates `release_manifest.json` and `release_manifest.md` under ignored `releases/`. Manifest records Git commit, branch, dirty flag, raw file hashes, included file checksums, QA/schema status, visual regression mode and warning summary.

## 18.2 Использование UI launcher

CLI remains the main supported production interface. UI launchers are convenience wrappers and must call only approved CLI entry points:

- `ofz-run`;
- `ofz-interactive`;
- `ofz-quality`;
- `ofz-clean-outputs`;
- `ofz-schema`;
- `ofz-build-release-bundle`.

PowerShell GUI launcher is the recommended Windows UI MVP:

```powershell
.\run-gui.ps1
.\ofz-gui.cmd
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1
```

Bare `ofz-gui.exe` works only when `.venv\Scripts` is in `PATH`, for example after `.venv` activation.

Word VBA launcher is optional. Use it only as a controlled launcher source and import it into a trusted document manually when needed:

- `.bas` and `.frm` are source artifacts and may be tracked in Git;
- `.docm` is a release artifact unless explicitly approved by artifact policy;
- macro security and trusted location setup must be checked manually.

Safety gates are the same for all UI launchers:

- delete cleanup requires `DELETE_OUTPUTS`;
- release bundle creation requires `BUILD_RELEASE_BUNDLE`;
- arbitrary shell commands are not accepted;
- release bundle remains an external artifact under ignored `releases/`.

Launcher logs are generated outputs:

```text
outputs/reports/launcher/launcher_run_<timestamp>.log
```

UI launchers do not replace quality gate. Before release, run the checklist QA commands directly through CLI or through an explicitly selected launcher action. Do not run fast and full quality gates in parallel.

## 19. Статус docs cleanup

Физическое архивирование docs отложено.

Решение:

- `docs/00_project/docs_cleanup_apply_decision.md`;
- archive only after references are resolved;
- `--delete-archived` запрещен до production-ready v1.

## 20. Статус scripts archive

Физическое архивирование legacy scripts отложено.

Решение:

- `docs/00_project/scripts_archive_decision.md`;
- 5 archive candidates kept until P2;
- no physical moves before production-ready v1.

## 21. Статус module decomposition

План существует:

- `docs/03_pipeline/module_decomposition_plan.md`.

Физическая декомпозиция является P2-only. До P2 не переносить основные scripts и не ломать wrapper compatibility.

## 22. Git workflow

Перед каждым этапом:

```powershell
git status --short
git branch --show-current
git remote -v
git log --oneline -5
```

Перед commit:

```powershell
git status --short
git diff --name-only
git diff --cached --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|data/processed|logs"
```

Правила:

- не делать `git add .` без просмотра статуса;
- generated outputs не staged;
- коммитить source/config/docs/scripts/contracts/prompts/data/raw;
- push только в `origin/main`, если stage завершен и проверки прошли.
