# Environment Setup

Дата актуализации: 2026-06-05.

## Supported Python

Package metadata supports Python `>=3.11,<3.15`.

Actually tested production baseline:

```powershell
.\.venv\Scripts\python.exe --version
```

Result on 2026-06-05: `Python 3.14.5`.

Compatibility checks completed in this stage:

- project source files under `scripts/` parse with Python 3.11 syntax rules when read as UTF-8 with optional BOM;
- installed runtime dependency metadata requires Python `>=3.11` at the strictest point (`pandas` and `numpy`);
- `pip install -e .`, `pip check`, `compileall` and CLI entry point help were rerun on the current Python 3.14.5 `.venv`.

Policy:

- use Python `3.14.x` to reproduce the current local production baseline exactly;
- Python `3.11`, `3.12` and `3.13` are allowed by package metadata, but must be validated with `quality_gate.py --fast` before relying on generated outputs;
- do not mix dependencies from system Python and `.venv`;
- run all project commands from the project root through `.\.venv\Scripts\python.exe`.

Production baseline проверен на Python `3.14.5` в локальном Windows PowerShell окружении.

Рекомендуемая политика:

- использовать Python `3.14.x` для воспроизведения текущего production baseline;
- не смешивать зависимости из системного Python и `.venv`;
- все команды запускать из корня проекта через `.\.venv\Scripts\python.exe`.

## Create `.venv`

```powershell
py -3.14 -m venv .venv
```

Если launcher `py` недоступен, используйте установленный Python 3.14, но не фиксируйте абсолютный путь к Python в документации проекта.

## Activate `.venv`

```powershell
.\.venv\Scripts\Activate.ps1
```

Активация удобна для интерактивной работы, но проектные команды в README используют явный локальный Python:

```powershell
.\.venv\Scripts\python.exe
```

## Runtime Dependencies

Установка runtime-зависимостей:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Runtime dependencies:

| Package | Role |
|---|---|
| `pandas` | Табличная обработка, CSV/XLSX чтение и запись. |
| `numpy` | Численные операции и расчет признаков. |
| `openpyxl` | Чтение и запись Excel-файлов. |
| `plotly` | HTML-графики. |
| `kaleido` | Plotly static export backend, optional для будущих image/screenshot workflows. |

`matplotlib` не входит в runtime baseline, потому что текущие production scripts не импортируют его напрямую.

## Dev / QA Dependencies

Установка dev/QA окружения:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Текущий `requirements-dev.txt` подключает runtime stack. Отдельные dev-зависимости не требуются:

- `pytest` не используется; regression/smoke/anomaly tests запускаются как project scripts;
- linters/formatters не зафиксированы в production baseline;
- screenshot backend для visual regression пока не включен, используется fallback HTML / Plotly JSON inspection.

## Dependency Check

```powershell
.\.venv\Scripts\python.exe -m pip check
```

Ожидаемый результат:

```text
No broken requirements found.
```

## Editable Install And CLI Entry Points

Project metadata is defined in `pyproject.toml`. Existing script-based commands remain the compatibility contract:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --help
```

Editable install:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

Console entry points after editable install:

```powershell
.\.venv\Scripts\ofz-run.exe --help
.\.venv\Scripts\ofz-interactive.exe
.\.venv\Scripts\ofz-quality.exe --help
.\.venv\Scripts\ofz-schema.exe --help
.\.venv\Scripts\ofz-clean-outputs.exe --help
.\.venv\Scripts\ofz-build-release-bundle.exe --help
```

Implemented entry points:

| Command | Module |
|---|---|
| `ofz-run` | `scripts.run_pipeline:main` |
| `ofz-interactive` | `scripts.interactive_pipeline:main` |
| `ofz-quality` | `scripts.quality_gate:main` |
| `ofz-schema` | `scripts.schema_validation:main` |
| `ofz-clean-outputs` | `scripts.maintenance.cleanup_outputs:main` |
| `ofz-build-release-bundle` | `scripts.maintenance.build_release_bundle:main` |

Safe outputs cleanup:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --dry-run
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --delete-all --confirm DELETE_OUTPUTS
```

Deletion is impossible without the exact confirm token. The command only touches paths inside `outputs/`, preserves `outputs/archive/`, writes cleanup manifests and recreates the skeleton with `.gitkeep`.

Ruff, Black, pytest and mypy are not enabled in this release because they are not part of the current production QA contract. The active QA stack is script-based: schema validation, regression tests, smoke tests, HTML chart QA, visual regression fallback and quality gate.

## Minimal Smoke Run

Минимальная проверка после установки окружения:

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\python.exe scripts\smoke_tests.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Для полного production baseline используйте:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Lockfile Policy

Lockfile deferred to next release.

Текущий production contract ограничивает major versions в `requirements.txt`, но не фиксирует полный transitive dependency lock. Перед внешним release bundle можно добавить lockfile отдельным контролируемым этапом.
