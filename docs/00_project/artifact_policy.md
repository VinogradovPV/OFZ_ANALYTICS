# Production artifact policy

Дата: 2026-06-04.

Документ фиксирует, какие файлы проекта OFZ_ANALYTICS считаются исходниками, какие являются воспроизводимыми build artifacts, а какие нужно хранить как release/audit artifacts. На этом этапе файлы не удаляются и не перемещаются.

## Категории артефактов

| Категория | Примеры | Хранить в git | Пересоздается pipeline | Release artifact | Локальное хранение | Правило архивации |
|---|---|---:|---:|---:|---|---|
| Source code | `scripts/*.py`, `scripts/maintenance/*.py`, `scripts/README.md` | Да | Нет | Нет | Постоянно | Не архивировать автоматически; устаревшие версии переносить только через отдельный migration/cleanup script. |
| Configuration | `requirements.txt`, future `.gitignore`, настройки запуска без секретов | Да | Нет | Нет | Постоянно | Изменения фиксировать в changelog/manual checks; секреты не хранить в репозитории. |
| Stable documentation | `README.md`, `docs/index.md`, `docs/00_project/`, `docs/01_methodology/`, `docs/02_data_pipeline/`, `docs/03_analytics/`, `docs/04_visualization/`, `docs/05_dashboard/`, `docs/06_quality/` | Да | Частично | Нет | Постоянно | Устаревшие документы переносить в `docs/90_archive/` через maintenance-скрипты. |
| Generated reports | `outputs/reports/*.md`, `outputs/reports/*.xlsx`, analytical/monthly/revenue reports | По решению релиза | Да | Да, для утвержденных запусков | 30-90 дней локально для рабочих запусков | После утверждения релиза сохранять в release bundle; старые рабочие результаты переносить в `outputs/archive/`. |
| Chart HTML | `outputs/charts/**/*.html` | По решению релиза; не игнорировать до финального решения | Да | Да, для утвержденных запусков | 30 дней локально для рабочих запусков; дольше для релизов | Тяжелые HTML складывать в release artifact или архивировать; не удалять без `--dry-run` и `--archive`. |
| Chart data CSV | `outputs/exports/chart_data/**/*.csv` | По решению релиза; не игнорировать до финального решения | Да | Да, если нужен audit/reproducibility package | 30-90 дней локально | Архивировать вместе с соответствующими HTML, чтобы график можно было проверить без пересчета. |
| Dashboard exports | `outputs/dashboards/**/*.csv`, semantic model v2 | По решению релиза | Да | Да | 30-90 дней локально; релизные версии хранить дольше | Архивировать по run_id/report_date; не смешивать разные `aggregation_mode`. |
| Run manifests | `outputs/reports/run_manifest_*.json`, `outputs/reports/run_manifest_*.md`, `data/processed/run_manifest_latest.json` | Latest можно не хранить; релизные manifests хранить как audit artifact | Да | Да | Постоянно для релизов; 90 дней для рабочих запусков | Релизные manifests не удалять; рабочие переносить в archive после устаревания. |
| Logs | `logs/*.log`, runtime traces | Нет | Да | Нет, кроме инцидентов | 14-30 дней локально | Ротировать/архивировать при инцидентах; обычные logs можно исключить из git. |
| Archive | `outputs/archive/`, `docs/90_archive/` | Docs archive можно хранить; outputs archive обычно не хранить | Нет | Только если архив является частью релиза | По политике релиза | Удаление только после `--dry-run`, затем `--archive`, затем `--delete-archived` при явном разрешении. |

## Специальные правила outputs

### `outputs/charts/`

`outputs/charts/` содержит тяжелые HTML artifacts. Baseline перед production-cleanup показывал около 97 HTML-файлов и примерно 447 MB в `outputs/charts/`.

Правило:

- HTML-графики считаются build artifacts, потому что пересоздаются pipeline.
- Для рабочих запусков HTML не обязаны храниться в git.
- Для релизного запуска HTML должны сохраняться как release artifact вместе с run manifest и chart data CSV.
- До окончательного решения по релизному процессу не добавлять `outputs/charts/**/*.html` в `.gitignore`.

### `outputs/exports/chart_data/`

`outputs/exports/chart_data/` содержит воспроизводимые CSV-основы графиков.

Правило:

- CSV-основы считаются build artifacts, но важны для аудита графиков.
- Для production release рекомендуется хранить их как release artifact вместе с HTML-графиками.
- Все поля `*_volume_bln` должны сопровождаться unit-полями согласно `docs/02_data_contracts/chart_data_contract.md`.
- До окончательного решения по релизному процессу не добавлять `outputs/exports/**/*.csv` в `.gitignore`.

### `outputs/dashboards/`

`outputs/dashboards/` содержит BI-ready exports, semantic model v2 и словари.

Правило:

- Dashboard exports считаются release artifacts, если запуск утвержден как отчетный.
- Для рабочих прогонов они пересоздаются pipeline и могут архивироваться по run_id/report_date.
- Semantic model v2 и data dictionaries должны храниться вместе с релизным dashboard package.

### `outputs/reports/run_manifests/`

Текущая структура проекта сохраняет run manifests в `outputs/reports/` и latest manifest в `data/processed/run_manifest_latest.json`. Логическая production-категория: `outputs/reports/run_manifests/`.

Правило:

- Run manifest является audit trail.
- Релизный manifest хранить как release artifact.
- `run_manifest_latest.json` является рабочим указателем и может пересоздаваться.
- При будущей реорганизации допустимо выделить физическую папку `outputs/reports/run_manifests/`, но только через отдельный dry-run/apply maintenance-блок.

## Release bundle

Минимальный production release bundle должен включать:

- run manifest (`json` и `md`);
- параметры запуска (`report_date`, `period_type`, `aggregation_mode`, `retrospective_years`);
- analytical/monthly/revenue reports;
- dashboard exports и semantic model v2;
- HTML-графики;
- chart data CSV;
- quality gate report;
- visual regression report или fallback inspection report;
- schema validation report;
- anomaly/regression/smoke test reports, если они запускались.

## Рекомендуемый `.gitignore`

`.gitignore` в проекте на момент создания policy отсутствует. Ниже приведен рекомендуемый шаблон. Не выполнять `git init` и не создавать `.gitignore` без отдельного подтверждения.

```gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
logs/
*.log

# Optional depending on artifact_policy.md
outputs/archive/
outputs/tmp/
outputs/cache/
```

## Production cleanup addendum

Этот раздел уточняет правила полной очистки `outputs/` перед production-перегенерацией.

### Working, release, archive and audit outputs

| Состояние | Что это | Git policy | Cleanup policy |
|---|---|---|---|
| Working outputs | Текущие результаты локальных прогонов pipeline в `outputs/`. | Обычно не коммитить без решения release process. | Можно очищать перед production-перегенерацией только через `scripts/maintenance/cleanup_outputs.py`. |
| Release artifacts | Утвержденный набор отчетов, графиков, CSV и dashboard exports для конкретного запуска. | По решению релиза; может храниться вне git как release package. | Не удалять обычным cleanup без отдельного решения. |
| Archive outputs | Перенесенные старые или рабочие результаты в `outputs/archive/`. | Обычно не хранить в git. | Удаление только после отдельного dry-run/archive/delete протокола. |
| Audit artifacts | Run manifest, quality gate, schema validation, visual regression, executive summary и data quality summary. | Релизные версии хранить как audit trail. | Релизные audit artifacts не удалять; disposable latest-файлы можно пересоздавать. |

### Clean outputs before production run

Перед production-перегенерацией outputs допускается полностью очищать generated artifacts, но только по явному протоколу.

Разрешенный инструмент:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --dry-run
```

Порядок действий:

1. Выполнить `--dry-run` и проверить отчет.
2. Если текущие результаты могут понадобиться для аудита, сначала создать archive bundle:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all
```

3. Только после проверки archive policy выполнить удаление:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --delete-all --confirm DELETE_OUTPUTS
```

4. После очистки обязательно выполнить production-перегенерацию:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

5. После pipeline обязательно выполнить quality gate:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Предупреждение: полная очистка outputs удаляет все generated artifacts, кроме сохраненного archive. Запускать только после dry-run и проверки archive policy.

### Archive bundle before cleanup

Перед полной очисткой outputs, если результаты могут понадобиться для аудита, нужно создать release/work archive bundle.

Минимальный состав archive bundle:

- run manifest `json` и `md`;
- quality gate report;
- schema validation report;
- HTML charts;
- chart data CSV;
- dashboard exports;
- executive summary;
- data quality summary, если есть.

Archive bundle должен быть связан с параметрами запуска: `report_date`, `period_type`, `aggregation_mode`, `retrospective_years`, `run_id`.

### Run manifest retention

Run manifest является audit trail.

Правила:

- релизные manifests не удалять;
- `run_manifest_latest.json` можно пересоздавать;
- если outputs очищаются, текущий manifest должен быть либо заархивирован, либо явно признан disposable в cleanup report;
- для release bundle manifest является обязательным файлом.

### `outputs/archive/`

`outputs/archive/` обычно не хранится в git, потому что содержит тяжелые и устаревающие generated artifacts.

Исключение: release archive может храниться как внешний release artifact, если он нужен для аудита или передачи результата.

`cleanup_outputs.py` не должен удалять archive, созданный в том же запуске. Это защищает сценарий `--archive-all` -> проверка -> последующая очистка working outputs.

Важно: не добавлять `outputs/charts/**/*.html` и `outputs/exports/**/*.csv` в `.gitignore`, пока artifact policy и release process явно не решат, что эти артефакты не коммитятся.

## Cleanup gates

Перед очисткой артефактов обязательно:

1. Выполнить cleanup script в режиме `--dry-run`.
2. Проверить отчет dry-run.
3. Выполнить `--archive`, если перенос согласован.
4. Выполнить `--delete-archived` только после отдельного явного разрешения.
5. После крупного блока запустить:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## 2026-06-04 - `.gitignore` created

`.gitignore` created in the project root after artifact policy confirmation.

Current ignore rules:

```gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
logs/
*.log

outputs/archive/
outputs/tmp/
outputs/cache/
```

Not ignored by design:

- `outputs/charts/**/*.html`;
- `outputs/exports/**/*.csv`.

These HTML and CSV artifacts remain outside `.gitignore` until the release process explicitly decides that they should not be committed.

## 2026-06-04 - first commit strategy

Decision: generated outputs are not included in the first Git commit.

The first commit should include source/configuration/documentation/contracts:

- source code: `scripts/**/*.py`;
- maintenance scripts: `scripts/maintenance/**/*.py`;
- project documentation: `README.md`, `CHANGELOG.md`, `docs/**/*.md`;
- configuration and dependency files: `.gitignore`, `requirements.txt`;
- data contracts and methodology docs.

Generated outputs are not committed to ordinary Git history:

- `outputs/charts/**/*.html`;
- `outputs/exports/**/*.csv`;
- `outputs/reports/**`;
- `outputs/dashboards/**`.

Generated processed data is also excluded from the ordinary source commit:

- `data/processed/**`.

Rationale:

- no single generated file above 50 MB was found before the first commit;
- however `outputs/charts/` is a heavy generated zone, approximately 447 MB by baseline;
- committing generated HTML/CSV/report/dashboard outputs into normal Git history would make the repository heavy and noisy;
- production artifacts should be distributed as release bundles or external artifacts.

Generated outputs should be preserved as one of:

- release bundle;
- external artifact;
- archived local artifact;
- GitHub Release asset, if this process is configured later.

Reproducibility should rely on:

- run manifest;
- raw file hashes;
- data contracts;
- scripts;
- `requirements.txt`;
- quality reports;
- schema validation reports;
- visual regression / HTML QA reports.

If a specific reporting run must be preserved completely, package its outputs into a release bundle instead of committing files individually into Git history.

Exceptions:

- empty output folder structure may be preserved via `.gitkeep`;
- small `README.md` or `index.md` files inside `outputs/` may be committed when they are useful as navigation or documentation.

This decision can be revisited later, but only through a separate release-process decision.

## 2026-06-04 - `data/raw` source dataset policy

`data/raw` is treated as a source dataset of the project and is committed to Git when both conditions hold:

- files are small enough for normal Git history;
- files do not contain confidential data.

For the first commit, `data/raw` was checked manually:

- no heavy files were found;
- listed Excel files are about 0.02-0.03 MB each;
- no temporary Excel/cache files were found by patterns `~$*.xlsx`, `*.tmp`, `*.bak`;
- the user confirmed that no confidential data was detected by manual review.

Raw file hashes are tracked through raw data registry and run manifest. Pipeline scripts must not modify `data/raw` in place.

## 2026-06-04 - Git policy for `data/raw`

`data/raw` is committed to Git as the source dataset of the project.

Decision rationale:

- raw files are small, approximately up to 0.03 MB each;
- no heavy raw files were found;
- `data/raw` is required for reproducible pipeline execution from source data;
- data was approved by the user as acceptable for repository storage.

`data/raw` must not be added to `.gitignore`. Raw file hashes are fixed in the raw data registry and/or run manifest. Generated outputs remain excluded from normal Git history and are recreated by the pipeline or preserved as release artifacts.

## 2026-06-05 - Git policy for `data/processed`

`data/processed` is treated as reproducible working output of the pipeline, not as the source dataset.

Decision:

- `data/raw` is committed as source data;
- `data/processed/**` is excluded from the first source commit via `.gitignore`;
- processed CSV/JSON files should be recreated by pipeline stages or preserved in release bundles when a run must be audited;
- latest runtime files such as `data/processed/run_manifest_latest.json` are working artifacts and can be regenerated.

## 2026-06-05 - GitHub repository and post-push artifact strategy

Version control state after the first push:

- Repository: GitHub / `OFZ_ANALYTICS`;
- Remote: `https://github.com/VinogradovPV/OFZ_ANALYTICS.git`;
- Default branch: `main`;
- Visibility: private;
- Initial commit: `4fa6d61fa67281c20d5d7a878cd2191e953507bc`;
- Initial commit message: `Initial source dataset and OFZ analytics pipeline`.

The first commit includes:

- source code and scripts;
- configuration files and dependency contract;
- stable project documentation and data contracts;
- prompt source assets;
- `data/raw` source dataset;
- `.gitkeep` files and lightweight navigation files for the `outputs/` skeleton.

The first commit excludes generated artifacts:

- generated HTML charts;
- generated chart data CSV exports;
- generated reports;
- dashboard exports;
- local archives, cache and temporary outputs;
- `data/processed` working data.

Generated outputs are recreated by the pipeline. When a specific reporting run must be preserved for audit or delivery, outputs should be packed into a release bundle or stored as an external artifact. The repository keeps reproducibility through source scripts, data contracts, `requirements.txt`, raw file hashes, raw data registry, run manifests and quality reports.

## 2026-06-05 - production Git artifact policy

This section supersedes earlier draft notes that said HTML/CSV outputs should not be ignored until the release process is decided. The release process decision has now been made for the production-ready baseline.

### Source artifacts

Source artifacts are tracked in Git:

- `scripts/**/*.py`;
- `scripts/**/*.md`;
- `docs/**/*.md`;
- `README.md`;
- `CHANGELOG.md`;
- `prompts/**`;
- `.gitignore`;
- `requirements.txt`;
- `requirements-dev.txt`;
- `pyproject.toml`;
- data contracts and methodology documentation;
- `data/raw/**`.

`data/raw` is committed as the project source dataset because the files are small, required for reproducibility and approved for repository storage. Pipeline scripts must not modify `data/raw` in place.

### Generated artifacts

Generated artifacts are not tracked in ordinary Git history:

- `outputs/charts/**/*.html`;
- `outputs/exports/**/*.csv`;
- `outputs/reports/**`;
- `outputs/dashboards/**`;
- `outputs/archive/**`;
- `outputs/tmp/**`;
- `outputs/cache/**`;
- `data/processed/**`;
- `logs/**`.

Generated artifacts are recreated by the pipeline, archived locally when needed, or packaged as external release artifacts.

### Git tracking policy

The Git repository stores source/config/docs/scripts/contracts/prompts and the small source dataset in `data/raw`.

The repository must not commit generated outputs. Before every commit, check staged files:

```powershell
git diff --cached --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|data/processed|logs"
```

If generated outputs are staged, remove them from the index without deleting local files:

```powershell
git rm --cached -r outputs/charts outputs/exports outputs/reports outputs/dashboards outputs/archive outputs/tmp data/processed
```

### Outputs skeleton exception

The empty/structural `outputs/` skeleton may be tracked:

- `outputs/**/.gitkeep`;
- small `outputs/**/README.md`;
- small `outputs/**/index.md`.

This exception exists only for navigation and folder discoverability. It does not allow committing generated HTML, CSV, XLSX, JSON or report artifacts from `outputs/`.

### Release bundle policy

If a reporting run must be preserved, create an external release bundle instead of committing outputs individually.

Minimum release bundle contents:

- run manifest `json` and `md`;
- quality gate report;
- schema validation report;
- HTML charts;
- chart data CSV;
- dashboard exports and semantic model;
- executive summary;
- analytical/monthly/revenue reports;
- visual regression or fallback HTML inspection report;
- anomaly/regression/smoke test reports when they were part of the run;
- data quality summary when available.

The release bundle must record `report_date`, `period_type`, `aggregation_mode`, `retrospective_years`, `run_id`, commit hash and raw file hashes.

### Clean outputs before production run

Before production regeneration, working outputs may be cleaned only through a maintenance script with an explicit safety flow.

Allowed protocol:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --dry-run
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --delete-all --confirm DELETE_OUTPUTS
```

Rules:

- start with `--dry-run`;
- archive first if current outputs may be needed for audit;
- delete only after archive policy is checked;
- after cleanup, run the pipeline and quality gate;
- never delete `data/raw`;
- never commit generated outputs after regeneration.

Warning: full outputs cleanup deletes generated artifacts except the preserved archive. Run it only after dry-run and archive-policy review.

### Run manifest policy

Run manifest is the audit trail of a production run.

Rules:

- release manifests are not deleted;
- `run_manifest_latest.json` is a working pointer and may be regenerated;
- if outputs are cleaned, the current manifest must be archived or explicitly marked disposable in the cleanup report;
- release bundles must include the run manifest and raw file hashes.

### `outputs/archive/` policy

`outputs/archive/` is normally not tracked in Git.

Allowed storage:

- local archive for short-term retention;
- external release artifact;
- GitHub Release asset, if the release process later enables it.

`cleanup_outputs.py` must not delete an archive created in the same cleanup run.

### Commit prohibition

Generated outputs are prohibited from ordinary commits. The only allowed tracked files under `outputs/` are skeleton/navigation files described above.
