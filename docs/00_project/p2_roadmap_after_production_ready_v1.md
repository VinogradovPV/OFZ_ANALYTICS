# P2 roadmap после production-ready v1

Дата актуализации: 2026-06-08.

Этот документ фиксирует задачи, которые намеренно вынесены за пределы production-ready v1. В рамках v1 эти работы не выполняются физически: не архивируются документы, не переносятся scripts, не запускается массовая декомпозиция и не удаляются archived docs.

## Статус

Статус roadmap: `P2 / post production-ready v1`.

Назначение:

- отделить стабилизацию production-ready v1 от последующих улучшений;
- не смешивать cleanup, decomposition, CI и release automation с уже подтвержденным production-candidate состоянием;
- сохранить контролируемость изменений: каждый пункт P2 должен выполняться отдельным этапом с проверками и отдельным commit.

## Общие правила P2

1. Перед каждым P2-этапом проверять `git status --short`.
2. Не выполнять массовый `git add .` без просмотра staged files.
3. Не менять `data/raw/` вручную.
4. Не коммитить generated outputs.
5. После каждого P2-этапа запускать минимум:

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

6. Для изменений release/CI/visual regression дополнительно обновлять `docs/07_operations/release_checklist.md` и `docs/07_operations/production_runbook.md`.

## 1. Устранить ссылки на docs archive candidates и применить docs archive

Цель: закрыть deferred docs cleanup после production-ready v1.

Что сделать:

- проверить активные ссылки на `archive_candidate` и `merge_candidate` в `README.md`, `docs/**`, `scripts/**`, `pyproject.toml`;
- перенести полезные правила из merge candidates в active docs, если это еще не сделано;
- обновить `docs/00_project/docs_inventory_before_cleanup.md`;
- выполнить `scripts/maintenance/cleanup_docs.py --dry-run`;
- только после проверки dry-run выполнить controlled archive mode;
- создать/обновить `docs/00_project/docs_inventory_after_cleanup.md`.

Запрет: не выполнять `--delete-archived` на этом шаге.

## 2. Устранить ссылки на legacy scripts и применить scripts archive

Цель: закрыть deferred scripts archive decision.

Archive candidates:

- `scripts/cleanup_docs.py`;
- `scripts/migrate_outputs_structure.py`;
- `scripts/reorganize_outputs.py`;
- `scripts/maintenance/migrate_legacy_docs_archive.py`;
- `scripts/maintenance/reorganize_docs.py`.

Что сделать:

- проверить references в `README.md`, `docs/**`, `scripts/**`, `pyproject.toml`, `scripts/run_pipeline.py`, `scripts/quality_gate.py`, `scripts/config.py`;
- удалить или обновить активные ссылки;
- подготовить `scripts/archive/YYYY-MM-DD/README.md`;
- перенести только те scripts, которые больше не имеют активных ссылок;
- сохранить wrapper compatibility, если какой-либо путь еще может использоваться историческими командами;
- выполнить `compileall` и `ofz-quality --fast`.

## 3. Физическая module decomposition

Цель: перейти от planning-only документа к контролируемой модульной структуре.

Основные кандидаты:

- `scripts/06_build_charts.py`;
- `scripts/10_build_monthly_charts.py`;
- `scripts/html_chart_qa.py`;
- `scripts/visual_regression.py`;
- `scripts/quality_gate.py`;
- `scripts/07_dashboard_exports.py`.

Порядок:

1. Сначала выносить pure helper functions.
2. Затем chart family builders.
3. Затем QA check groups.
4. После каждого шага сохранять wrappers для старых entry points.
5. После каждого шага запускать `compileall`, `ofz-quality --fast` и релевантные targeted QA scripts.

## 4. Настроить actual screenshot backend для visual regression

Цель: заменить текущий fallback static HTML / Plotly JSON inspection на полноценную screenshot-проверку.

Что сделать:

- выбрать backend: Kaleido/Playwright/browser-based workflow;
- определить поддержку Windows;
- добавить зависимости в `requirements-dev.txt` или production dependencies, если backend нужен в release gate;
- добавить тестовый screenshot sample;
- обновить `scripts/visual_regression.py`;
- обновить runbook и release checklist.

Критерий готовности: visual regression умеет создавать и сравнивать изображения графиков, а fallback остается резервным режимом.

## 5. CI / GitHub Actions

Цель: проверять production contracts в GitHub до merge/push release.

Минимальный CI:

- checkout;
- setup Python;
- install dependencies;
- `pip install -e .`;
- `pip check`;
- `compileall`;
- `ofz-schema`;
- `ofz-quality --fast`.

Ограничение: generated outputs не должны коммититься CI job. Если CI генерирует артефакты, они должны сохраняться как workflow artifacts.

## 6. Автоматизация release bundle

Цель: одной командой собирать внешний release artifact для конкретного run.

Release bundle должен включать:

- HTML charts;
- chart data CSV;
- dashboard exports;
- run manifests;
- QA reports;
- executive summary;
- data quality summary, если создан;
- release manifest с Git commit, raw hashes, run params и checksums.

Рекомендуемая команда будущего этапа:

```powershell
ofz-build-release-bundle --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## 7. Dockerfile / Windows setup

Цель: упростить воспроизводимый запуск вне текущей машины.

Что сделать:

- описать Windows-first setup;
- добавить проверенный `Dockerfile`, если будет выбран контейнерный сценарий;
- зафиксировать ограничения Excel/raw data handling;
- проверить fonts/locale для русских подписей графиков;
- обновить `docs/07_operations/environment.md`.

## 8. BI-ready release package

Цель: подготовить пакет для BI/аналитических инструментов.

Состав:

- dashboard exports;
- semantic model v2;
- analytical tables;
- chart data CSV;
- data dictionary;
- README для BI-потребителя;
- versioned release manifest.

Требование: BI-ready package должен быть external artifact, а не обычный Git commit generated outputs.

## 9. Pipeline telemetry

Цель: добавить наблюдаемость production-запусков.

Что фиксировать:

- run id;
- stage durations;
- input/output counts;
- warnings/errors;
- generated artifacts count/size;
- cleanup mode;
- quality gate results;
- Git commit;
- raw data hashes.

Результат: telemetry summary должен попадать в run manifest и, при необходимости, в отдельный `outputs/reports/telemetry/` artifact.

## 10. Удалять archived docs только после stable release

Цель: не потерять исторический контекст сразу после первого controlled archive.

Правило:

- после docs archive apply архивированные документы остаются в репозитории;
- `--delete-archived` запрещен до stable release после production-ready v1;
- удаление archived docs допускается только отдельным подтвержденным этапом;
- перед удалением нужен dry-run, manifest и проверка, что release bundle/stable tag уже создан.

## Критерий завершения P2 roadmap

P2 roadmap считается закрытым, когда:

- docs archive references resolved и archive apply выполнен;
- legacy scripts references resolved и archive apply выполнен;
- module decomposition выполнена с wrappers и QA;
- visual regression имеет screenshot backend;
- CI настроен и зеленый;
- release bundle автоматизирован;
- Windows/Docker setup документирован и проверен;
- BI-ready package собирается воспроизводимо;
- pipeline telemetry фиксируется в run manifest;
- archived docs deletion policy выполнена только после stable release.
