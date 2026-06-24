# Post-P3 next work plan after cleanup

Дата: 2026-06-24.

## Назначение

Документ фиксирует baseline после Post-P3 cleanup и скрытое локальное состояние, которое не видно в обычном `git status`.

Важно: `skip-worktree` и `.git/info/exclude` являются локальной Git-метаданной. Они не коммитятся и не являются approval для raw/source update.

## Текущий git status

Команды выполнены outside sandbox из корня проекта.

```text
## main...origin/main
M  docs/00_project/post_p3_worktree_cleanup_report.md
```

`docs/00_project/post_p3_worktree_cleanup_report.md` еще содержит follow-up CLEAN.1-CLEAN.5 update и должен быть закоммичен вместе с этим планом.

## Последние коммиты

- `4bdac2f Clean post-P3 working tree state`
- `dc4176d Document post-P3 release candidate gate`
- `d28641c Plan chart and QA module decomposition`
- `7abf48e Assess post-P3 pipeline optimization opportunities`
- `f92c799 Harden Minfin live dry-run acquisition`

## Skip-worktree paths

### Controlled raw/registry files

Эти файлы физически остаются в рабочем каталоге, но скрыты из обычного `git status`:

- `data/raw/minfin/ofz_auction_results/latest/INTERNET_Auction_Results_rus_2026_latest.xlsx`
- `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources.csv`
- `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources_latest.json`

Перед любым source update commit нельзя забыть:

1. Снять `skip-worktree` с этих путей.
2. Проверить hash, registry CSV/JSON и соответствие controlled source acquisition workflow.
3. Отдельно получить operator approval на source update.
4. Не stage `data/raw/minfin/ofz_auction_results/versions/` без отдельного решения.

### Generated/report docs hidden from status

Эти tracked docs отражают локальные pipeline/QA report updates и скрыты через `skip-worktree`:

- `docs/01_methodology/kpi_map.md`
- `docs/01_methodology/period_selection_report.md`
- `docs/02_data_pipeline/data_audit.md`
- `docs/02_data_pipeline/data_cleaning_report.md`
- `docs/02_data_pipeline/feature_engineering.md`
- `docs/03_analytics/analytical_tables_limitations.md`
- `docs/03_analytics/analytical_tables_report.md`
- `docs/03_analytics/executive_summary_report.md`
- `docs/03_analytics/monthly_analytics_report.md`
- `docs/03_analytics/revenue_analytics_report.md`
- `docs/03_analytics/revenue_charts_report.md`
- `docs/04_visualization/chart_build_limitations.md`
- `docs/04_visualization/monthly_visualization_strategy.md`
- `docs/04_visualization/visualization_strategy.md`
- `docs/05_dashboard/dashboard_exports_limitations.md`
- `docs/05_dashboard/dashboard_exports_report.md`
- `docs/05_dashboard/dashboard_semantic_model_v2.md`
- `docs/06_quality/quality_gate_report.md`
- `docs/06_quality/run_manifest_report.md`
- `docs/06_quality/visual_regression_report.md`
- `docs/90_archive/deprecated/bid_to_cover_outliers.md`
- `docs/90_archive/old_reproducibility/reproducibility_review_stages_1_3.md`

Перед docs/report refresh commit нужно снять `skip-worktree` только с релевантных файлов и отдельно решить, являются ли эти report docs expected generated documentation update или локальным шумом.

## Local exclude paths

`.git/info/exclude` содержит локальные untracked leftovers, оставленные физически, но скрытые из обычного status:

- `data/raw/minfin/ofz_auction_results/versions/2026/INTERNET_Auction_Results_rus_2026_20260618_3e748e88be0e.xlsx`
- `post_p3_ignored_files_before_cleanup.txt`
- `post_p3_modified_files_before_cleanup.txt`
- `post_p3_untracked_files_before_cleanup.txt`
- `post_p3_worktree_status_before_cleanup.txt`
- `prompts/ofz_gui_launcher_user_friendly_status_and_navigation_fix_ru.md`
- `prompts/ofz_gui_launcher_ux_improvement_instruction_ru.md`
- `prompts/ofz_post_p3_optimization_step_by_step.md`
- `prompts/ofz_post_p3_optimization_system_prompt.md`
- `prompts/ofz_post_p3_worktree_cleanup_and_next_work_instruction.md`
- `prompts/ofz_post_p3_next_work_after_cleanup_instruction.md`

Эти excludes не должны скрывать future source changes. Если какой-либо prompt должен стать частью проекта, его нужно вынести из `.git/info/exclude`, проверить содержание и stage точечно.

## Source update caveat

Текущее состояние raw/source update не approved.

Clean ordinary status не означает, что raw/latest/registry уже подтверждены. Перед любым коммитом raw/source update нужно явно вернуться к controlled raw paths, снять локальную маскировку и провести review.

## Выбранный следующий этап

Рекомендуемый следующий этап: `NEXT.1 Screenshot backend validation outside sandbox`.

Причина: POSTP3.7 release-candidate gate прошел автоматизированные проверки, но screenshot backend был заблокирован в Codex managed environment. Перед stable release нужно выполнить validation из обычного project PowerShell или оформить явный waiver.

Команда для NEXT.1:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode screenshot --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## NEXT.1 result - Screenshot backend validation outside sandbox

Дата: 2026-06-24.

Пользователь вручную выполнил команду из обычного project PowerShell:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode screenshot --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Результат зафиксирован в `docs/06_quality/visual_regression_report.md`.

Фактический результат:

- screenshot backend отработал outside sandbox;
- сформировано `50` screenshot artifacts;
- screenshot run id/path содержит `visual_regression_20260624_160024_month_cumulative_2026-05-01_r4`;
- baseline screenshots отсутствуют, поэтому diff report фиксирует `missing_baseline`, а не failure;
- generated screenshot PNG, manifest и diff report files остаются generated outputs и не должны коммититься.

NEXT.1 считается закрытым как backend validation. Перед stable release остается операторский visual review/waiver по содержанию скриншотов и решение по baseline policy.

Следующий рекомендуемый этап: `NEXT.2 quality-full stable-release precheck`.

## NEXT.2 result - Quality-full stable-release precheck

Дата: 2026-06-24.

Выполнен stable-release precheck без release build/tag/GitHub release:

- editable install - OK;
- `pip check` - OK;
- `compileall` - OK;
- UTF-8/mojibake scanner - OK;
- pipeline for `2026-05-01 / month / cumulative / retrospective 4` - OK;
- schema validation - OK, `16` checks;
- `ofz-quality --fast` - OK;
- `ofz-quality --full` - OK;
- release bundle dry-run - OK, dry-run only.

Подробности зафиксированы в `docs/00_project/stable_release_precheck_report.md`.

`ofz-quality --full` содержит expected anomaly warnings, но gate завершился успешно. Release bundle dry-run показал target `releases\ofz_analytics_2026-05-01_month_cumulative_retrospective_4_20260624_163039` и не записывал release files.

NEXT.2 считается закрытым.

Следующий рекомендуемый этап: `NEXT.3 Operator decision по raw/latest/registry`.

## NEXT.3 result - Operator decision по raw/latest/registry

Дата: 2026-06-24.

Пользователь выбрал `Вариант A — approve source update`.

Approved controlled paths:

- `data/raw/minfin/ofz_auction_results/latest/INTERNET_Auction_Results_rus_2026_latest.xlsx`
- `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources.csv`
- `data/raw/minfin/ofz_auction_results/registry/minfin_ofz_auction_sources_latest.json`

Not staged:

- `data/raw/minfin/ofz_auction_results/versions/`
- `outputs/reports/source_acquisition/`
- generated outputs, processed data, logs and release artifacts.

Validated source state:

- new 2026 latest candidate: `INTERNET_Auction_Results_rus_2026_20260618.xlsx`;
- as-of date: `18.06.2026`;
- latest SHA256: `3e748e88be0e5ff26171d6f36916949de83c50c918749e57454aeb1e73e3829b`;
- latest size: `20131` bytes;
- active registry rows: `2025 final` and `2026 latest`.

Details are recorded in `docs/00_project/minfin_source_update_decision_report.md`.

NEXT.3 is complete.

Next recommended stage: `NEXT.4 Stable release/tag gate`, only after explicit user approval for release build, tag and GitHub release actions.

## Запреты до отдельного approval

Не выполнять без отдельного явного разрешения пользователя:

- stable release;
- git tag;
- GitHub release create/upload;
- release bundle build;
- BI package build;
- live Minfin download/import/replacement;
- destructive cleanup;
- commit raw/source update.

## Проверки NEXT.0

- `.\.venv\Scripts\python.exe scripts\qa\check_text_encoding.py`
- `git diff --check`

Artifact guard должен оставаться пустым для staged scope.
