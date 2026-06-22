# Аудит радикальной переработки GUI launcher

Дата: 2026-06-22.

## Текущее состояние

Текущий `tools/windows_launcher/ofz_launcher.ps1` совмещает поиск окружения, валидацию параметров, построение команд, выполнение CLI и WinForms UI. Интерфейс представляет длинную форму с техническими переключателями и частично остается command preview. В нем нет сценарных вкладок Минфина, pipeline stage 0, targeted QA, отчетов, release/BI, журнала и встроенной справки.

PowerShell-код синхронно выполняет процессы и собирает stdout/stderr через временные файлы. Это затрудняет live streaming, отмену длительной операции и безопасное расширение allowlist.

## Паттерны Expense_Splitter

- Python `tkinter` является основным desktop UI.
- `ttk.Notebook` разделяет пользовательские сценарии.
- Состояние вынесено в отдельный `GuiState`.
- Actions отделены от layout.
- Ошибки отображаются пользователю, а status bar показывает результат.
- PowerShell wrapper только находит и запускает GUI entry point.

## Целевые actions OFZ_ANALYTICS

- Source acquisition Минфина: monthly, annual-final и manual-import.
- Pipeline, schema и optional stage 0 Минфина.
- Quality fast/full, encoding, source-registry smoke, HTML QA и visual regression.
- Открытие ключевых charts, exports, reports, telemetry и run manifest.
- Release bundle и BI package в dry-run/build режимах.
- Cleanup, artifact guard, Git status и открытие рабочих каталогов.

## Dangerous actions

| Действие | Typed confirm |
| --- | --- |
| Monthly/annual-final download | `DOWNLOAD_MINFIN_SOURCE` |
| Замена changed final | `REPLACE_MINFIN_FINAL` |
| Manual import | `IMPORT_MINFIN_FILE` |
| Release bundle build | `BUILD_RELEASE_BUNDLE` |
| BI package build | `BUILD_BI_PACKAGE` |
| Delete outputs | `DELETE_OUTPUTS` |

## Artifact policy

Нельзя коммитить `outputs/`, `releases/`, `logs/`, `data/processed/`, source acquisition reports и `data/raw/minfin/ofz_auction_results/versions/`. Launcher logs являются generated artifacts.

## Архитектура

- Entry point: `ofz-gui = "scripts.gui_launcher.app:main"`.
- Пакет: `scripts/gui_launcher/` с `app.py`, `state.py`, `command_runner.py`, `actions.py`, `widgets.py`, `help_text.py`.
- Runner принимает только заранее зарегистрированные action IDs, запускает аргументы списком с `shell=False`, стримит объединенный вывод и запрещает параллельные процессы.
- PowerShell становится совместимым thin wrapper для `.venv\Scripts\ofz-gui.exe` или `dist\ofz-gui.exe`.

## Этапы

1. Каркас, state и entry point.
2. Allowlist actions и streaming runner.
3. Вкладка Минфина.
4. Pipeline со stage 0.
5. Quality checks.
6. Reports/charts.
7. Release и обслуживание.
8. Журнал и русская справка.
9. Thin wrapper и operator docs.
10. Automated smoke и ручной checklist.
