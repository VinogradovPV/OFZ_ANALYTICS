# Environment Setup

Дата актуализации: 2026-06-05.

## Supported Python

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
