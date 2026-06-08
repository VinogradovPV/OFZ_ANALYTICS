# Scripts Legacy Archive Decision

Дата: 2026-06-08.

## Решение

Физическое архивирование legacy scripts отложено до P2.

Статус: `physical_archive_deferred_to_P2`.

## Проверенные кандидаты

| Скрипт | Решение | Причина |
|---|---|---|
| `scripts/cleanup_docs.py` | оставить на месте | Есть ссылки в `scripts/README.md`, project docs, migration plans and inventory. |
| `scripts/migrate_outputs_structure.py` | оставить на месте | Есть ссылки в `docs/00_project/outputs_structure.md`, `final_project_summary.md`, scripts plans and inventory. |
| `scripts/reorganize_outputs.py` | оставить на месте | Есть ссылки в `README.md`, `outputs_structure.md`, scripts plans and inventory. |
| `scripts/maintenance/migrate_legacy_docs_archive.py` | оставить на месте | Есть ссылки в `scripts/README.md`, scripts plans and inventory. |
| `scripts/maintenance/reorganize_docs.py` | оставить на месте | Есть ссылки в `scripts/README.md`, scripts plans and inventory. |

## Reference scan scope

Проверены ссылки в:

- `README.md`;
- `docs/**`;
- `scripts/**`;
- `pyproject.toml`;
- `scripts/run_pipeline.py`;
- `scripts/quality_gate.py`.

## Обоснование

До production-ready v1 предпочтителен консервативный вариант A:

- не удалять;
- не переносить;
- не ломать исторические команды и документацию;
- зафиксировать статус legacy/archive candidates;
- перенести физически только в P2 после отдельного reference cleanup и совместимых wrappers/README updates.

## Запреты до P2

- Не удалять файлы без отдельного подтверждения.
- Не переносить в `scripts/archive/` без обновления ссылок и повторного `compileall` + `ofz-quality --fast`.
- Не менять entry points.
- Не менять module decomposition plan в рамках этого решения.

## P2 follow-up

Перед физическим архивированием:

1. Убрать или обновить ссылки в README/docs/scripts plans.
2. Проверить, что scripts не вызываются из `run_pipeline.py`, `quality_gate.py` и `pyproject.toml`.
3. Создать `scripts/archive/YYYY-MM-DD/README.md`, если будет выбран физический перенос.
4. Выполнить:

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```
