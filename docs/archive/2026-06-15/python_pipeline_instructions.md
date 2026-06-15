# Python Pipeline Instructions

Date: 2026-05-15

## Python executable policy

Основной Python-интерпретатор проекта:

```powershell
C:\Users\Rockaudit\LLM_CHAT\ofz_analytics\.venv\Scripts\python.exe
```

Если Codex или терминал запускаются не из корня проекта, запрещено использовать относительный путь:

```powershell
.venv\Scripts\python.exe
```

Вместо этого использовать абсолютный путь:

```powershell
& "C:\Users\Rockaudit\LLM_CHAT\ofz_analytics\.venv\Scripts\python.exe" -m py_compile "C:\Users\Rockaudit\LLM_CHAT\ofz_analytics\scripts\report_params.py"
```

Перед запуском pipeline проверять рабочую директорию:

```powershell
Get-Location
```

Корень проекта:

```powershell
C:\Users\Rockaudit\LLM_CHAT\ofz_analytics
```

## Interpreter selection

Do not assume that `python`, `py`, or `python3` are available in `PATH`.
The runtime environment may have a different `PATH` from the user's regular
PowerShell session.

Before running checks, choose an explicit Python executable:

1. Use the full path to `python.exe` if it is known.
2. Use `.venv\Scripts\python.exe` only when the current working directory is
   the project root, the project virtual environment exists, and the executable
   starts successfully.

If `python` is unavailable in `PATH`, do not replace Python checks with
PowerShell-only logic. Fix or select the interpreter path first, then run the
Python command through that executable.

Use `<python_executable>` as a placeholder for the selected interpreter path.

## Compilation checks

Run script compilation checks with:

```powershell
<python_executable> -m py_compile <script.py>
```

Examples:

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\run_pipeline.py
C:\Path\To\Python\python.exe -m py_compile scripts\run_pipeline.py
```

## Pipeline run

Run stages 1, 2, and 3 in safe mode with:

```powershell
<python_executable> scripts/run_pipeline.py --stages 1 2 3 --safe
```

Examples:

```powershell
.\.venv\Scripts\python.exe scripts/run_pipeline.py --stages 1 2 3 --safe
C:\Path\To\Python\python.exe scripts/run_pipeline.py --stages 1 2 3 --safe
```

## Current runtime note

In this Codex runtime, `Get-Command python` and `where.exe python` may return no
result even when Python works in a normal user PowerShell session. In that case,
prefer an explicit interpreter path and verify it with:

```powershell
<python_executable> --version
```
