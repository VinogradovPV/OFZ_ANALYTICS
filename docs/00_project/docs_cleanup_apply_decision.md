# Docs Cleanup Apply Decision

Дата: 2026-06-08.

## Решение

Физическое архивирование документации по Этапу 11.1 отложено.

Статус: `deferred_until_references_are_resolved`.

## Причины

Dry-run `scripts/maintenance/cleanup_docs.py --dry-run` после consolidation data contracts показал, что архивирование пока нельзя выполнять вслепую:

- часть `archive_candidate` все еще имеет активные ссылки в `scripts/config.py`, `scripts/quality_gate.py`, maintenance-скриптах и `docs/index.md`;
- `docs_reorganization_report.md` и `charts_reorganization_report.md` используются quality gate как evidence-файлы структуры docs/charts;
- `legacy_docs_archive_migration_*` еще упоминаются в `docs/index.md` и maintenance workflow;
- merge diagnostics уже частично перенесены в active contracts/visualization docs, но ссылки на них еще остаются в документации и журнале проверок;
- новый dry-run после Этапа 11 выявил дополнительные active docs, которые требовали обновления классификатора `cleanup_docs.py`.

## Проверка merge candidates

Полезные правила из visualization diagnostics перенесены в:

- `docs/02_data_contracts/chart_data_contract.md`;
- `docs/04_visualization/chart_build_limitations.md`;
- `docs/04_visualization/visualization_strategy.md`;
- `docs/06_quality/manual_checks_log.md`.

Следующие документы считаются кандидатами `ready_for_archive_after_merge`, но физически не архивируются до удаления/обновления активных ссылок:

- `docs/04_visualization/chart_improvement_diagnostics.md`;
- `docs/04_visualization/format_revenue_discount_chart_diagnostics.md`;
- `docs/04_visualization/chart_improvement_scope.md`;
- `docs/04_visualization/boxplot_diagnostics.md`.

## Следующий безопасный шаг

Перед archive apply нужно отдельным controlled step:

1. Убрать ссылки на archive candidates из `docs/index.md`, если они больше не являются active docs.
2. Обновить `quality_gate.py`, если evidence-файлы `docs_reorganization_report.md` и `charts_reorganization_report.md` должны переехать в архив.
3. Обновить `scripts/config.py` и maintenance reports paths, если reports больше не должны считаться active.
4. Запустить:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --dry-run
```

5. Выполнять `--archive` только если dry-run не содержит active references для архивируемых документов.

## Запреты

- Не выполнять `--delete-archived` до production-ready v1.
- Не архивировать merge candidates, пока ссылки не сняты.
- Не коммитить generated manifests из `outputs/reports/cleanup/`.
