# UTF-8 для Windows PowerShell

Дата актуализации: 2026-07-02.

Этот документ фиксирует обязательное правило UTF-8 для локальной работы с OFZ Analytics в Windows PowerShell. Правило применяется к CLI, GUI, source acquisition, CBR/Minfin parser flows, QA и release-проверкам.

## Политика

1. Все текстовые файлы проекта хранятся в UTF-8.
2. CLI/subprocess output читается как UTF-8 с безопасной заменой нечитаемых символов.
3. Перед запуском project commands в PowerShell нужно включить UTF-8 bootstrap.
4. Mojibake-маркеры считаются blocker/release проблемой.
5. Generated/local artifacts не коммитятся.

## PowerShell bootstrap

Выполняйте этот блок в новой PowerShell-сессии перед запуском команд проекта:

```powershell
chcp 65001 | Out-Null
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
```

После этого запускайте команды из корня проекта:

```powershell
.\.venv\Scripts\python.exe scripts\qa\check_text_encoding.py
.\.venv\Scripts\ofz-quality.exe --stage encoding-mojibake
.\.venv\Scripts\ofz-run.exe --help
```

## Subprocess policy

GUI command runner и другие subprocess runners должны передавать в дочерний процесс:

```text
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
```

Stdout/stderr должны читаться как:

```python
encoding="utf-8"
errors="replace"
```

Если в пользовательском выводе появляются признаки `U+FFFD`, `U+00D0`, `U+00D1`, `U+2568`, `U+2564`, это не считается нормальным результатом. Пользовательский итог должен показать понятное предупреждение, а полный raw output должен оставаться в техническом UTF-8 журнале.

## Проверка кодировок

Основная проверка:

```powershell
.\.venv\Scripts\python.exe scripts\qa\check_text_encoding.py
```

Scanner проверяет source/docs/config/scripts и исключает:

- `.venv/`;
- `outputs/`;
- `data/processed/`;
- `logs/`;
- `releases/`;
- `.ofz_launcher/`;
- временные/generated каталоги.

Mojibake markers:

```text
U+00D0
U+00D1
U+FFFD
U+2568
U+2564
```

Найденные invalid UTF-8 или mojibake-маркеры блокируют quality gate и release.
