# Docs Archive Apply Report

Дата: 2026-06-15.

## Статус

P2.9 Controlled docs archive apply выполнен.

Физическое архивирование применено только к документам, которые после повторной проверки не входят в активный production contract. Удаление архивированных документов не выполнялось.

## Что сделано

- Выполнен повторный dry-run `scripts/maintenance/cleanup_docs.py --dry-run`.
- Проверены активные ссылки из `README.md`, `docs/**`, `scripts/**` и `pyproject.toml`.
- Полезные правила из merge diagnostics ранее перенесены в активные data contracts и visualization docs.
- `cleanup_docs.py` обновлен так, чтобы P2 operation docs оставались `keep_active`, а устаревшие diagnostics и legacy stage reports классифицировались как `archive_candidate`.
- Активная карта документации `docs/index.md` больше не перечисляет legacy diagnostics как active documents.
- `quality_gate.py` больше не требует архивные reorganization reports как active quality documents.
- Выполнен archive mode без `--delete-archived`.

## Результат archive mode

- Архивная папка: `docs/archive/2026-06-15/`.
- Архивировано документов: 39.
- Active docs после cleanup: 61.
- Создан after-inventory: `docs/00_project/docs_inventory_after_cleanup.md`.
- Generated cleanup manifest создан в `outputs/reports/cleanup/` и не коммитится.

## Удаление

Удаление архивированных документов не выполнялось. `--delete-archived` остается запрещенным до отдельного production-ready/stable release решения.

## Проверки

- `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\cleanup_docs.py scripts\quality_gate.py`: OK.
- `.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --dry-run`: OK.
- `.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --archive`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.

Quality gate warning: screenshot backend unavailable in current environment, visual regression used fallback mode. This is the expected P2.7/P2.8 state until Playwright browser binaries are installed.

## Ограничения

- В архивных документах и legacy maintenance scripts могут оставаться исторические ссылки на старые пути. Они не считаются active production references.
- Scripts archive остается отдельным этапом P2.10.
- Generated outputs и cleanup manifests не входят в Git.
