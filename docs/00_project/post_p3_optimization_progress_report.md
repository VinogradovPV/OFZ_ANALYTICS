# Post-P3 optimization progress report

## POSTP3.1 - Resolve quality-gate inconsistencies

Дата: 2026-06-23.

### Статус

- Устранены активные противоречия вокруг `outputs/charts/index.md`.
- Актуальная policy: source-карта структуры generated outputs находится в `docs/00_project/outputs_structure.md`.
- Generated `outputs/charts/index.md` не является обязательным source artifact и не требуется quality gate.
- Исправлен локальный UTF-8 blocker в untracked prompt: в `prompts/ofz_gui_launcher_user_friendly_status_and_navigation_fix_ru.md` фактические replacement characters заменены на текстовое описание `U+FFFD`; prompt остается вне staged scope, потому что файл не отслеживается Git.
- Исторические записи о прежнем blocker оставлены как historical context, но новый статус зафиксирован в P3/Post-P3 progress и manual checks log.

### Изменения

- `README.md`
- `docs/index.md`
- `scripts/README.md`
- `docs/00_project/production_readiness_report.md`
- `docs/00_project/p3_modernization_progress_report.md`
- `docs/06_quality/manual_checks_log.md`
- `docs/00_project/post_p3_optimization_progress_report.md`
- Локально нормализован untracked `prompts/ofz_gui_launcher_user_friendly_status_and_navigation_fix_ru.md`; файл не добавляется в commit.

### Проверки

- `rg -n "outputs/charts/index.md|charts/index.md|index.md" README.md docs scripts .github pyproject.toml` - OK: активные ссылки переведены на `docs/00_project/outputs_structure.md`; оставшиеся упоминания являются historical context или прямым statement "не требуется".
- `.\.venv\Scripts\python.exe -m py_compile scripts\quality_gate.py` - OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts` - OK.
- `.\.venv\Scripts\python.exe scripts\qa\check_text_encoding.py` - OK.
- `.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` - OK: regenerated current generated outputs for quality-fast.
- `.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` - OK, 16/16.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative` - OK.
- `git diff --check` - OK.

Дополнительный runtime fix:

- `scripts/quality_gate.py` теперь запускает вложенные Python checks с `PYTHONUTF8=1` и `PYTHONIOENCODING=utf-8`, чтобы `quality_gate_report.md` не загрязнялся mojibake из stdout/stderr child scripts.

### Пропущенные проверки и почему

- Live Minfin download, delete outputs, release build и BI build не выполняются: POSTP3.1 исправляет quality/docs policy и не должен мутировать raw/release/generated artifacts.
- Screenshot backend остается fallback в managed sandbox; Playwright screenshot outside sandbox переносится на release-candidate/manual validation.

### Риски

- В рабочей копии до этапа уже были unrelated raw/output/report changes и untracked prompts; они не относятся к POSTP3.1 commit и не должны staged.

### Следующий этап

Следующий рекомендуемый этап: `POSTP3.2 GUI real workflow validation and polish`.

## POSTP3.0 - Baseline and contradiction audit

Дата: 2026-06-23.

### Статус

- Принят к исполнению Post-P3 stabilization and optimization.
- Выполнен только audit-only этап `POSTP3.0 Baseline and contradiction audit`.
- Создан baseline audit: `docs/00_project/post_p3_baseline_audit.md`.
- Код, raw storage, generated outputs, release bundles и GUI runtime state не изменялись.
- Git/GitHub команды выполнялись outside sandbox из корня проекта.

### Изменения

- `docs/00_project/post_p3_optimization_progress_report.md`
- `docs/00_project/post_p3_baseline_audit.md`

### Проверки

- `git status --short --branch`
- `git log --oneline -5`
- `gh run list --limit 5`
- `rg` по активным docs/scripts на `outputs/charts/index.md`, `charts/index.md`, `outputs_structure` и related quality-gate references.
- `Test-Path outputs/charts/index.md`
- `Test-Path docs/00_project/outputs_structure.md`
- `Test-Path .ofz_launcher`

Итог предварительного аудита:

- последние GitHub Actions runs до этапа были green;
- `outputs/charts/index.md` в рабочем дереве отсутствует;
- `docs/00_project/outputs_structure.md` существует;
- `.ofz_launcher` существует локально и должен оставаться вне Git;
- текущий `scripts/quality_gate.py` проверяет `docs/00_project/outputs_structure.md`, а не требует generated `outputs/charts/index.md`;
- активные документы все еще содержат устаревшие ссылки на `outputs/charts/index.md`.

Финальные проверки этапа выполняются после создания audit-документов:

- `.\.venv\Scripts\python.exe scripts\qa\check_text_encoding.py` - FAIL: найден `U+FFFD` в существующем untracked prompt `prompts/ofz_gui_launcher_user_friendly_status_and_navigation_fix_ru.md`.
- `git diff --check` - OK.
- `git diff --name-only` - OK: показал ранее существующие tracked local changes; новые untracked audit docs в этот вывод не входят до staging.

### Пропущенные проверки и почему

- `compileall`, `py_compile`, `ofz-run`, `ofz-schema`, `ofz-quality --fast/full`, GUI smoke и source acquisition smoke не запускались: этап documentation/audit-only, Python-код не менялся.
- Live Minfin download, manual import, annual-final replacement, delete outputs, release bundle build и BI build не выполнялись: это dangerous actions и они не входят в POSTP3.0.
- Screenshot validation outside sandbox не выполнялась: POSTP3.0 только фиксирует, что эта ручная проверка остается release-candidate blocker.

### Риски

- Рабочее дерево до POSTP3.0 уже содержало локальные raw/registry/generated/output изменения и untracked prompt files; они не относятся к этому audit commit и не должны попадать в stage.
- В активной документации есть устаревшие ссылки на generated `outputs/charts/index.md`, хотя текущий quality gate уже использует source-карту `docs/00_project/outputs_structure.md`.
- UTF-8 scanner сейчас блокируется существующим untracked prompt `prompts/ofz_gui_launcher_user_friendly_status_and_navigation_fix_ru.md` с replacement character `U+FFFD`; это нужно устранить отдельным scope или исключить файл из активного scanner scope осознанным решением.
- Source registry пока находится в совместимом режиме `warn + allow-legacy-raw`; strict migration не завершен.
- GUI automated smoke пройден ранее, но ручная UX/layout validation outside sandbox остается отдельным шагом.

### Git status

- Перед этапом branch: `main...origin/main`.
- В рабочей копии уже были unrelated local changes/generated artifacts; audit stage не изменяет и не коммитит их.

### Commit

- Планируемый commit: `Audit post-P3 optimization baseline`.

### Push

- Планируется после успешной staged artifact guard проверки.

### GitHub Actions

- До этапа последние пять runs были успешными.
- После push нужно повторно проверить `gh run list --limit 5`; если новый run упадет, просмотреть `gh run view --log`.

### Следующий этап

Следующий рекомендуемый этап: `POSTP3.1 Resolve quality-gate inconsistencies` - привести README/docs/scripts references к единой policy, где source-карта структуры находится в `docs/00_project/outputs_structure.md`, а generated `outputs/charts/index.md` не является обязательным source artifact.
