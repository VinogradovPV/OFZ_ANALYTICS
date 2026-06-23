# Post-P3 optimization progress report

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
