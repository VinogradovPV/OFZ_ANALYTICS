# Стартовый checkpoint P2

Дата: 2026-06-09.

## Назначение

Документ фиксирует исходное состояние перед началом P2 modernization после production-ready candidate v11.

P2 начинается только после подтверждения baseline, Git-состояния, artifact policy, CLI entry points и quality gate.

## Анализ P2 system prompt

Источник:

- `prompts/ofz_p2_modernization_system_prompt_v3.md`.

Ключевые правила prompt:

- P2 не является переписыванием проекта с нуля;
- каждый P2-этап выполняется отдельно;
- generated outputs не коммитятся;
- `data/raw` не меняется вручную;
- текущие CLI entry points сохраняются;
- `quality_gate --fast` и `quality_gate --full` не запускать параллельно из-за возможного `.pyc` permission conflict;
- UI launcher должен быть оболочкой над CLI, а не отдельной реализацией pipeline;
- docs/scripts archive выполняются только после reference cleanup;
- module decomposition выполняется controlled extraction с wrapper compatibility.

## Подтвержденное исходное состояние

| Проверка | Статус |
|---|---|
| Project status | `production-ready candidate` |
| Branch | `main` |
| Remote | `origin/main` |
| Git status before P2 | clean, затем после запуска baseline изменились только QA reports и P2 docs |
| Repository visibility | private |
| `data/raw` | tracked as source dataset |
| Generated outputs | not tracked; `outputs` tracked only as skeleton/index |
| `quality_gate --fast` | OK |
| `quality_gate --full` | OK |

## Предварительная проверка Git

Выполнено:

```powershell
git status --short --branch
git branch --show-current
git remote -v
git log --oneline -5
```

Результат:

- branch: `main`;
- remote: `origin https://github.com/VinogradovPV/OFZ_ANALYTICS.git`;
- latest commits included `b549ba5 Add P2 roadmap after production-ready v1`;
- prompt file was present as untracked source prompt asset before this checkpoint commit.

## CLI entry points

Актуальные entry points из `pyproject.toml`:

```toml
[project.scripts]
ofz-run = "scripts.run_pipeline:main"
ofz-interactive = "scripts.interactive_pipeline:main"
ofz-quality = "scripts.quality_gate:main"
ofz-clean-outputs = "scripts.maintenance.cleanup_outputs:main"
ofz-schema = "scripts.schema_validation:main"
```

Проверены:

```powershell
.\.venv\Scripts\ofz-run.exe --help
.\.venv\Scripts\ofz-interactive.exe --help
.\.venv\Scripts\ofz-quality.exe --help
.\.venv\Scripts\ofz-clean-outputs.exe --help
.\.venv\Scripts\ofz-schema.exe --help
```

Результат: OK.

## Базовая линия качества

Выполнено последовательно:

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-quality.exe --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Результат:

- `compileall`: OK;
- `quality_gate --fast`: OK;
- `quality_gate --full`: OK;
- anomaly warnings remain documented data warnings, not execution failures;
- visual regression continues to use fallback static HTML / Plotly JSON inspection until P2 screenshot backend.

## P2 execution protocol

Каждый P2-этап выполнять по схеме:

1. Pre-check Git.
2. Выполнить только один P2-этап.
3. Запустить минимальные проверки.
4. Проверить, что generated outputs не staged.
5. Обновить docs/manual checks log.
6. Сделать отдельный commit.
7. Push в `origin/main`.
8. Подготовить короткий отчет.

Pre-check:

```powershell
git status --short
git branch --show-current
git remote -v
git log --oneline -5
```

Generated outputs check:

```powershell
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|outputs/cache|data/processed|logs|releases"
```

Минимальные проверки:

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Уточненный порядок P2

Рекомендуемый порядок:

| Этап | Название |
|---|---|
| P2.0 | Starting checkpoint |
| P2.1 | Release bundle automation |
| P2.2 | Pipeline telemetry |
| P2.3 | UI launcher contract |
| P2.4 | PowerShell GUI launcher MVP |
| P2.5 | Word VBA launcher spec and source |
| P2.6 | UI launcher documentation and artifact policy update |
| P2.7 | Screenshot visual regression backend |
| P2.8 | CI / GitHub Actions |
| P2.9 | Controlled docs archive apply |
| P2.10 | Controlled legacy scripts archive apply |
| P2.11 | Controlled module decomposition |
| P2.12 | Windows setup / Docker plan |
| P2.13 | BI-ready release package |
| P2.14 | Archive deletion policy |
| P2.15 | P2 completion report |

## P2 reporting rule

Финальный отчет после каждого P2-этапа должен содержать:

1. Какой P2-этап выполнен.
2. Что изменено.
3. Какие проверки прошли.
4. Какие проверки упали.
5. Какие warnings documented.
6. Какие commits созданы.
7. Был ли push.
8. Текущий git status.
9. Подтверждение:
   - generated outputs not staged;
   - `data/raw` tracked;
   - CLI entry points still work.
10. Следующий рекомендуемый P2-этап.

Сводный отчет по каждому P2-этапу ведется в:

- `docs/00_project/p2_modernization_progress_report.md`.
