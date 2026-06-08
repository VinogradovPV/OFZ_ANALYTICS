# Отчет о готовности к production

Дата актуализации: 2026-06-08.

## 1. Исполнительный статус

Статус проекта: `production-ready candidate`.

Проект готов к повторяемому production-запуску в текущем локальном и Git-контуре при соблюдении production runbook и release checklist. Статус обозначен как `production-ready candidate`, а не окончательный `production-ready` без оговорок, потому что остаются документированные предупреждения по данным, visual regression работает через fallback без screenshot backend, а физическая очистка legacy docs/scripts отложена до P2.

## 2. Статус Git

- URL репозитория: `https://github.com/VinogradovPV/OFZ_ANALYTICS.git`.
- Видимость: private.
- Основная ветка: `main`.
- Последний проверенный commit до обновления этого отчета: `2ac420b Record final production quality gate`.
- Состояние working tree до обновления этого отчета: clean.
- Политика generated outputs проверена: generated HTML/CSV/reports/dashboard exports не tracked в Git.

## 3. Стратегия артефактов

Source artifacts в Git:

- source code;
- config;
- docs;
- scripts;
- data contracts;
- prompts;
- `data/raw`;
- skeleton-файлы outputs (`.gitkeep`, допустимые легкие `index.md` / `README.md`).

`data/raw` tracked в Git как source dataset проекта, потому что исходные Excel-файлы небольшие и нужны для воспроизводимости.

Generated outputs не входят в обычную Git-историю:

- `outputs/charts/**`;
- `outputs/exports/**`;
- `outputs/reports/**`;
- `outputs/dashboards/**`;
- `outputs/archive/**`;
- `outputs/tmp/**`;
- `outputs/cache/**`.

Политика release bundle:

- generated outputs конкретного отчетного запуска сохраняются как release bundle, external artifact или будущий GitHub Release asset;
- release bundle должен включать HTML charts, chart data CSV, dashboard exports, run manifests, QA reports и summaries;
- generated outputs не должны коммититься как обычная source history.

## 4. Статус Python и package

- `pyproject.toml`: существует.
- Имя package: `ofz-analytics`.
- Версия: `0.1.0`.
- Поддерживаемый диапазон Python: `>=3.11,<3.15`.
- Проверенная версия Python: `Python 3.14.5`.

CLI entry points:

- `ofz-run`;
- `ofz-interactive`;
- `ofz-quality`;
- `ofz-clean-outputs`;
- `ofz-schema`.

Примечание: короткие команды `ofz-*` требуют активированной `.venv` или PATH, содержащего `.venv\Scripts`. Прямые проверки через `.\.venv\Scripts\ofz-*.exe` прошли.

## 5. Статус очистки docs

Инвентаризация docs:

- `keep_active`: 51;
- `archive_candidate`: 35;
- `merge_candidate`: 4;
- `delete_candidate`: 0.

Контрольные документы:

- `docs/00_project/docs_inventory_before_cleanup.md`;
- `docs/00_project/docs_cleanup_apply_decision.md`.

Решение:

- физическое архивирование docs отложено;
- для части archive/merge candidates остаются нерешенные ссылки;
- `--delete-archived` запрещен до production-ready v1;
- archive apply требует отдельного controlled stage после устранения ссылок.

## 6. Статус очистки scripts

Инвентаризация scripts:

- `keep_active`: 32;
- `refactor_candidate`: 5;
- `archive_candidate`: 5;
- `delete_candidate`: 0;
- `unknown`: 0.

Контрольные документы:

- `docs/00_project/scripts_inventory_before_cleanup.md`;
- `docs/00_project/scripts_archive_decision.md`.

Пять archive candidates:

- `scripts/cleanup_docs.py`;
- `scripts/migrate_outputs_structure.py`;
- `scripts/reorganize_outputs.py`;
- `scripts/maintenance/migrate_legacy_docs_archive.py`;
- `scripts/maintenance/reorganize_docs.py`.

Решение:

- рекомендация для всех пяти: `keep_legacy_until_p2`;
- физическое архивирование отложено;
- scripts не переносились и не удалялись;
- будущий physical archive требует cleanup ссылок, явного подтверждения, `compileall` и `ofz-quality --fast`.

## 7. Статус module decomposition

План существует:

- `docs/03_pipeline/module_decomposition_plan.md`.

Статус:

- только планирование;
- в production-ready v1 физические переносы не выполняются;
- декомпозиция является P2-only;
- для будущих переносов обязательна wrapper compatibility.

Основные кандидаты:

- `scripts/06_build_charts.py`;
- `scripts/10_build_monthly_charts.py`;
- `scripts/html_chart_qa.py`;
- `scripts/visual_regression.py`;
- `scripts/quality_gate.py`;
- `scripts/07_dashboard_exports.py`.

## 8. Статус data contracts

Активные data contracts:

- `docs/02_data_contracts/processed_data_contract.md`;
- `docs/02_data_contracts/analytical_tables_contract.md`;
- `docs/02_data_contracts/chart_data_contract.md`;
- `docs/02_data_contracts/dashboard_exports_contract.md`;
- `docs/02_data_contracts/semantic_model_v2.md`.

Ключевые правила contracts:

- поля `*_volume_bln` требуют unit-поля со значением `млрд рублей`;
- revenue fields включают `revenue_volume_bln`, `nominal_revenue_gap_bln`, `revenue_to_nominal_ratio`;
- yield fields различают обычную доходность и средневзвешенную доходность размещения;
- discount fields фиксируют source column, fallback formula и unit `п.п.`;
- label fields и quality fields документированы для chart data exports.

## 9. Статус quality gate

Финальный production quality gate выполнен для параметров:

```powershell
--report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Результаты:

- `pip install -e .`: OK после escalated rerun, потому что sandboxed pip не смог записать во `%TEMP%`;
- `pip check`: OK;
- `compileall`: OK;
- `schema_validation`: OK, 16/16;
- `smoke_tests`: OK, 9 checks;
- `regression_tests`: OK, 14 checks;
- `anomaly_tests`: completed with documented data warnings;
- `html_chart_qa`: OK;
- `visual_regression`: OK через fallback static HTML / Plotly JSON inspection;
- `quality_gate --fast`: OK;
- `quality_gate --full`: OK.

Примечание: первый параллельный запуск fast/full gate вызвал временный `.pyc` permission conflict в `scripts/__pycache__`. Последовательный rerun прошел.

## 10. Исправленные blockers

Исправленные blockers:

- production blocker `schema_validation / volume_bln_units` исправлен в generators и data contracts;
- generated outputs исключены из Git с сохранением skeleton;
- стратегия `data/raw` зафиксирована и документирована;
- `.gitignore` и Git artifact strategy внедрены;
- CLI entry points добавлены и проверены;
- cleanup outputs workflow добавлен через `ofz-clean-outputs`;
- production runbook и release checklist созданы.

## 11. Оставшиеся warnings

Оставшиеся warnings являются предупреждениями по данным/операциям, а не execution failures:

- anomaly tests фиксируют строки без yield и demand/supply edge cases;
- bid-to-cover и demand-to-placement outliers требуют аналитической проверки;
- строки без cutoff price ограничивают discount analysis;
- nominal/revenue gap anomalies выше threshold требуют интерпретации;
- screenshot backend не настроен, поэтому visual regression использует fallback static HTML / Plotly JSON;
- physical cleanup docs/scripts отложен до устранения ссылок;
- Python 3.11-3.13 разрешены metadata, но текущая локальная runtime-сертификация выполнена на Python 3.14.5.

## 12. Итоговая структура

Docs:

- `docs/00_project/` — project governance, inventories, readiness, artifact policy;
- `docs/01_methodology/` — methodology и KPI maps;
- `docs/02_data_contracts/` — active data contracts;
- `docs/02_data_pipeline/` — data pipeline documentation;
- `docs/03_analytics/` и `docs/03_pipeline/` — analytics и pipeline planning;
- `docs/04_visualization/` — visualization rules и limitations;
- `docs/05_dashboard/` — dashboard docs;
- `docs/06_quality/` — QA reports и manual checks;
- `docs/07_operations/` — environment, runbook, release checklist;
- `docs/90_archive/` — historical documentation.

Scripts:

- active stage scripts остаются в `scripts/`;
- production maintenance scripts находятся в `scripts/maintenance/`;
- physical script archive или decomposition в v1 не выполняются.

Outputs:

- generated outputs находятся в `outputs/`;
- Git tracks только skeleton `.gitkeep` files и `outputs/charts/index.md`;
- generated HTML/CSV/reports/dashboard exports являются release artifacts, а не source commits.

## 13. Команда полной очистки outputs

Dry-run:

```powershell
ofz-clean-outputs --dry-run
```

Архивировать и удалить:

```powershell
ofz-clean-outputs --archive-all --delete-all --confirm DELETE_OUTPUTS
```

Fallback:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all --delete-all --confirm DELETE_OUTPUTS
```

## 14. Cleanup mode в interactive launcher

Interactive launcher:

```powershell
ofz-interactive
```

Перед запуском pipeline он проверяет generated outputs и предлагает:

1. оставить outputs как есть;
2. показать cleanup dry-run;
3. архивировать outputs и очистить;
4. очистить outputs без архива после явного подтверждения;
5. отменить запуск.

Launcher делегирует удаление `scripts/maintenance/cleanup_outputs.py`; напрямую файлы он не удаляет.

## 15. Release checklist

Release checklist существует:

- `docs/07_operations/release_checklist.md`.

Он покрывает Git state, environment, CLI help, `data/raw`, pipeline runs, QA, outputs/release bundle, docs/scripts cleanup decisions и final staged-file checks.

## 16. Оставшиеся риски

Оставшиеся production risks:

- visual regression пока не screenshot-based;
- generated outputs большие и требуют дисциплины external release bundle;
- docs archive candidates все еще имеют ссылки, поэтому cleanup физически не применен;
- legacy scripts остаются на месте до P2;
- chart builders и QA scripts являются крупными monoliths и требуют controlled decomposition позже;
- data warnings требуют аналитической проверки перед high-stakes external publication;
- release bundle process документирован, но пока не автоматизирован одной командой.

## 17. Рекомендации следующего релиза

Рекомендуемые P2-задачи:

Детальный P2 roadmap после production-ready v1 вынесен в отдельный документ:

- `docs/00_project/p2_roadmap_after_production_ready_v1.md`.

1. Добавить screenshot backend для visual regression.
2. Автоматизировать release bundle creation.
3. Устранить ссылки на docs archive candidates и выполнить controlled docs archive apply.
4. Устранить ссылки на legacy scripts и физически архивировать safe candidates.
5. Начать module decomposition только с extraction pure helper functions.
6. Добавить CI workflow для install, compileall, schema и fast quality gate.
7. Сертифицировать runtime на Python 3.11/3.12/3.13 или сузить metadata до реально проверенных версий.
8. Добавить release manifest, связывающий Git commit, raw hashes, run manifest и checksum release bundle.
