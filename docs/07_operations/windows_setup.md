# Windows setup

Дата: 2026-06-16.

Этот документ описывает воспроизводимую установку OFZ_ANALYTICS на новой Windows-машине. Windows + PowerShell остается основным production-сценарием проекта.

## Цель

Setup должен:

- проверить PowerShell и Python;
- создать `.venv`, если его еще нет;
- установить runtime dependencies;
- при необходимости установить dev/QA dependencies;
- выполнить `pip install -e .`;
- проверить `pip check`;
- проверить CLI entry points;
- выполнить `compileall`;
- запускать `ofz-quality --fast` только по явному флагу;
- не трогать `outputs/` без отдельной команды cleanup.

## Требования

- Windows PowerShell 5.1+ или PowerShell 7+.
- Python из поддержанного диапазона проекта: `>=3.11,<3.15`.
- Для точного воспроизведения локального baseline рекомендуется Python `3.14.x`.
- Git уже должен быть установлен, если машина будет работать с репозиторием.

## Быстрый dry-run

Из корня проекта:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/setup/setup_windows.ps1 -DryRun
```

Dry-run не создает `.venv`, не устанавливает зависимости и не меняет outputs. Он показывает команды, которые будут выполнены.

## Базовая установка

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/setup/setup_windows.ps1
```

Скрипт:

1. Проверяет `pyproject.toml`, `requirements.txt`, `data/raw`.
2. Создает `.venv` через `py -3.14 -m venv .venv`, если `.venv` отсутствует.
3. Устанавливает runtime dependencies из `requirements.txt`.
4. Выполняет `pip install -e .`.
5. Выполняет `pip check`.
6. Проверяет CLI help для:
   - `ofz-run`;
   - `ofz-interactive`;
   - `ofz-quality`;
   - `ofz-clean-outputs`;
   - `ofz-schema`;
   - `ofz-build-release-bundle`.
7. Выполняет `python -m compileall -q scripts`.

## Dev / QA setup

Если нужны screenshot visual regression и dev/QA зависимости:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/setup/setup_windows.ps1 -IncludeDev
.\.venv\Scripts\python.exe -m playwright install chromium
```

Playwright/Chromium нужны только для screenshot mode. Fallback visual regression работает без браузера.

## Optional fast quality gate

Fast quality gate не запускается по умолчанию. Для полной smoke-проверки setup:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/setup/setup_windows.ps1 -IncludeDev -RunFastQuality
```

Параметры отчета можно переопределить:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/setup/setup_windows.ps1 `
  -RunFastQuality `
  -ReportDate 2026-05-01 `
  -RetrospectiveYears 4 `
  -PeriodType month `
  -AggregationMode cumulative
```

## Что setup не делает

Скрипт не должен:

- менять `data/raw`;
- очищать `outputs`;
- создавать release bundle;
- запускать full quality gate;
- выполнять Git commit/push;
- устанавливать глобальные Python packages вне `.venv`.

Для очистки outputs используется отдельная команда:

```powershell
.\.venv\Scripts\ofz-clean-outputs.exe --dry-run
```

## Troubleshooting

Если `py -3.14` недоступен, установите Python из поддержанного диапазона и повторите setup с нужной версией:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/setup/setup_windows.ps1 -PythonVersion 3.12
```

Если `pip install -e .` прошел, но CLI не найдены, проверьте:

```powershell
.\.venv\Scripts\python.exe -m pip show ofz-analytics
Get-ChildItem .\.venv\Scripts\ofz-*.exe
```

Если screenshot backend недоступен:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

Если `ofz-quality --fast` падает, не правьте generated CSV/HTML вручную. Исправляйте source/generator/contracts и повторяйте targeted checks.
