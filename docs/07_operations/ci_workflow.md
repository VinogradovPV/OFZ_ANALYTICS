# CI workflow

Дата актуализации: 2026-06-11.

CI для OFZ_ANALYTICS настроен через GitHub Actions workflow:

- `.github/workflows/quality.yml`
- repository: `https://github.com/VinogradovPV/OFZ_ANALYTICS`
- default branch: `main`

## Назначение

Workflow запускает production-oriented проверки без коммита generated outputs. CI проверяет, что проект устанавливается из source, проходит dependency check, компиляцию Python scripts, schema validation и fast quality gate.

Generated outputs, release bundles и screenshots остаются внешними/generated artifacts и не должны попадать в Git.

## Triggers

Workflow запускается на:

- `push` в `main`;
- `pull_request` в `main`;
- `workflow_dispatch`.

Ручной запуск `workflow_dispatch` нужен для операторской проверки и для optional full quality job. Команда `gh workflow run quality.yml` не выполняется автоматически и требует отдельного подтверждения пользователя.

## Jobs

### quality-fast

`quality-fast` запускается на `windows-latest` для всех triggers.

Шаги:

1. `actions/checkout`.
2. `actions/setup-python` с Python `3.12`.
3. `pip install -r requirements.txt`.
4. `pip install -r requirements-dev.txt`, если файл существует.
5. `pip install -e .`.
6. `python -m pip check`.
7. `python -m compileall -q scripts`.
8. `ofz-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`.
9. `ofz-schema --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`.
10. `ofz-quality --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`.
11. Upload QA reports as workflow artifacts.

### quality-full

`quality-full` запускается только для `workflow_dispatch`.

Job зависит от `quality-fast`, чтобы fast/full не выполнялись параллельно в одном CI workflow. Full gate нужен для release validation, но не для каждого push.

## Python version

CI использует Python `3.12`, потому что проект поддерживает диапазон `>=3.11,<3.15`, а hosted runner для Python 3.14 может быть недоступен или нестабилен. Локальная production-проверка может выполняться на другой версии из поддержанного диапазона, но перед release нужно пройти `ofz-quality --fast` или `ofz-quality --full`.

## Console encoding

Windows runners can expose a non-UTF-8 stdout/stderr encoding. Schema validation and quality gate messages can contain Cyrillic text, so the workflow sets:

```yaml
PYTHONUTF8: "1"
PYTHONIOENCODING: "utf-8"
```

PowerShell steps that run Python or installed CLI entry points also call `chcp 65001` before those commands. CLI entry points that print Cyrillic diagnostics configure stdout/stderr to UTF-8 with replacement for unencodable characters.

Schema validation and quality gates require generated `data/processed` and `outputs` artifacts. CI therefore runs `ofz-run` before schema validation instead of relying on generated files being present in Git.

## Dependency cache

Workflow использует только pip cache через `actions/setup-python`.

Запрещено кешировать:

- `outputs/`;
- `releases/`;
- screenshots;
- generated chart data;
- dashboard exports.

## Workflow artifacts

CI загружает QA reports как GitHub Actions artifacts:

- `docs/06_quality/*.md`;
- `docs/02_data_pipeline/schema_validation_report.md`;
- `outputs/reports/quality/**`;
- `outputs/reports/run_manifests/**`;
- `outputs/reports/visual_regression/**`;
- `outputs/reports/telemetry/**`.

Эти artifacts не являются Git-tracked source. Они используются как external audit trail для конкретного CI run.

## Visual regression mode

`ofz-quality --fast` использует текущий production contract. Если screenshot backend недоступен на runner, visual regression может перейти в fallback/static inspection mode и явно записать это в report. Browser binaries для Playwright не устанавливаются в P2.8, чтобы не утяжелять baseline CI. Полная стабилизация screenshot backend в CI может быть добавлена отдельным этапом.

## Generated outputs policy

CI не должен коммитить generated outputs. Workflow содержит informational guard:

```powershell
git status --short -- outputs/charts outputs/exports outputs/reports outputs/dashboards outputs/archive outputs/tmp outputs/cache data/processed logs releases
git ls-files outputs releases data/processed logs
```

Если в будущем появится workflow, который создает release bundle, он должен публиковать bundle как workflow artifact или GitHub Release asset только после отдельного release-process approval.

## GitHub CLI inspection

Разрешенные команды просмотра:

```powershell
gh workflow list
gh run list
gh run view <run-id> --log
```

Не запускать без отдельного подтверждения пользователя:

```powershell
gh workflow run quality.yml
```

Не выполнять из CI или локально без отдельной команды:

- `gh release create`;
- `gh release upload`;
- `gh repo edit`;
- `gh secret set`;
- `gh variable set`.

## Local parity checks

Перед коммитом workflow локально выполняются:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

После push можно проверить GitHub-side состояние:

```powershell
gh workflow list
gh run list --limit 5
gh run view <run-id> --log
```
