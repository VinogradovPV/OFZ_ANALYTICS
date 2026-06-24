# POSTP3.5 - Отчет по оптимизации pipeline и data audit

Дата: 2026-06-24.

## Цель этапа

POSTP3.5 проверяет производительность и операционные узкие места pipeline после P3 без изменения финансовой методологии, схемы outputs и правил расчета метрик.

Этап выполнен как assessment-first. Код не менялся: найденные улучшения требуют отдельного небольшого этапа с regression checks, потому что затрагивают orchestration, telemetry или кэширование generated artifacts.

## Проверенный baseline

Команда baseline pipeline:

```powershell
.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Результат: OK.

Свежая telemetry:

- telemetry file: `outputs/reports/telemetry/telemetry_20260624_075557_3344c61e.json`;
- status: `ok`;
- duration_seconds: `12.445`;
- report date: `2026-05-01`;
- retrospective years: `4`;
- period type: `month`;
- aggregation mode: `cumulative`.

Input row/file counts из telemetry:

| Dataset | Count |
|---|---:|
| `raw_files` | 14 |
| `ofz_auctions_clean` | 678 |
| `ofz_auctions_features` | 678 |
| `ofz_auctions_report_scope` | 163 |
| `ofz_monthly_metrics` | 20 |

Важно: `raw_files=14` в telemetry сейчас означает все файлы под `data/raw`, а не только Excel-файлы, реально участвующие в pipeline. Этап 1 фактически нашел 8 raw Excel-файлов. После P3 controlled source acquisition это различие стало существенным: `latest/`, `registry/` и `versions/` не должны смешиваться с числом pipeline input XLSX.

Generated output counts из telemetry:

| Area | Count |
|---|---:|
| `charts` | 100 |
| `exports` | 122 |
| `reports` | 44 |
| `dashboards` | 34 |
| `archive` | 1351 |

Telemetry также зафиксировала:

- generated_artifacts_count: `1651`;
- artifacts_total_size_bytes: `2221054885`.

Важно: `outputs/archive` входит в общий счетчик generated artifacts. Это полезно для release bundle inventory, но шумит при оценке текущего pipeline run: старые cleanup snapshots доминируют над freshly generated outputs.

## Самые медленные стадии

По свежему run:

| Stage | Duration, sec | Комментарий |
|---|---:|---|
| `8` - построение графиков | 4.0 | Самый дорогой этап; строит 32 HTML-графика и CSV-экспорты. |
| `1` - аудит исходных данных | 1.0 | Повторно читает raw Excel-файлы. |
| `2` - очистка данных | 1.0 | Повторно читает те же raw Excel-файлы, что и data audit. |
| `4` - report scope | 1.0 | Читает features CSV и формирует scoped dataset. |
| `8.1` - аналитические таблицы | 1.0 | Читает report scope и пишет CSV/XLSX. |
| `revenue_charts` | 1.0 | Пишет HTML/CSV revenue charts. |
| `monthly_analytics` | 1.0 | Читает scope/features, пишет monthly metrics CSV/XLSX. |
| `monthly_charts` | 1.0 | Пишет 9 monthly HTML/CSV artifacts. |
| `semantic_model_v2` | 1.0 | Пишет semantic model CSV/JSON. |

Остальные стадии по текущей telemetry укладываются в `0.0` секунд из-за секундной точности stage telemetry. Общая длительность считается точнее, но per-stage durations округлены фактически до секунд.

## Повторные чтения данных

Статический аудит чтений показал:

- `scripts/01_data_audit.py` читает raw Excel/CSV для audit.
- `scripts/02_data_cleaning.py` повторно читает raw Excel/CSV для очистки.
- `scripts/03_feature_engineering.py` читает `data/processed/ofz_auctions_clean.csv`.
- `scripts/period_filter.py` читает `data/processed/ofz_auctions_features.csv`.
- Downstream stages многократно читают `data/processed/ofz_auctions_report_scope.csv`:
  - `scripts/04_kpi_map.py`;
  - `scripts/06_build_charts.py`;
  - `scripts/07_dashboard_exports.py`;
  - `scripts/08_analytical_tables.py`;
  - `scripts/09_monthly_analytics.py`;
  - `scripts/11_revenue_analytics.py`;
  - `scripts/12_build_revenue_charts.py`;
  - `scripts/anomaly_tests.py`;
  - `scripts/schema_validation.py`.
- `scripts/10_build_monthly_charts.py` читает `ofz_monthly_metrics.csv`, а также использует report scope/features для части проверок и графиков.

Для текущего объема данных это не является performance blocker. Риск появится при росте raw history, monthly detail, BI exports или visual QA surface.

## Повторная генерация artifacts

Pipeline сейчас намеренно перегенерирует named outputs при каждом run:

- HTML charts;
- chart data CSV;
- analytical tables CSV/XLSX;
- dashboard CSV/JSON;
- executive summary;
- run manifest;
- telemetry.

Это безопасно для воспроизводимости, но не оптимально:

- при неизменных inputs и одинаковых report params графики и CSV пересоздаются;
- outputs counts включают несколько report dates, поэтому `charts=100` означает накопленную рабочую папку, а не только текущий run;
- telemetry artifact inventory обходит весь `outputs`, включая `outputs/archive`, что может становиться дорогим и шумным.

## Возможность safe cache / manifest-based skip

Safe skip возможен, но не должен внедряться вслепую.

Минимальный безопасный дизайн:

1. Для каждого stage считать fingerprint:
   - stage code;
   - script path + sha256;
   - report params;
   - input file paths, sizes, mtimes и sha256 для ключевых datasets;
   - schema version соответствующего stage.
2. Писать stage manifest под `outputs/reports/run_manifests/` или отдельный `outputs/reports/stage_cache/`.
3. Разрешать skip только для deterministic generated artifacts.
4. Никогда не skip:
   - source acquisition;
   - data audit registry validation;
   - quality gate;
   - encoding/mojibake checks;
   - release bundle build;
   - dangerous actions.
5. По умолчанию оставить current behavior; включать skip отдельным explicit flag, например `--allow-stage-skip`, после regression.

До внедрения такого механизма нельзя просто проверять наличие output-файла и пропускать stage: это может скрыть изменение методологии, schema или source data.

## Low-risk optimization candidates

Кандидаты на отдельные маленькие этапы:

1. **Уточнить telemetry raw counts.**
   - Разделить `raw_files_total_under_data_raw`, `pipeline_input_excel_files`, `source_registry_files`, `source_versions_files`.
   - Не менять pipeline behavior.
   - Проверки: telemetry unit/smoke + `ofz-run`.

2. **Исключить `outputs/archive` из current-run artifact summary или вынести отдельно.**
   - Оставить archive inventory для release/cleanup.
   - В telemetry добавить `current_outputs_file_counts` без archive и `archive_file_count` отдельно.
   - Проверки: telemetry report smoke + release bundle dry-run.

3. **Повысить точность stage durations.**
   - Сейчас per-stage durations фактически секундные, что затрудняет поиск узких мест.
   - Ввести perf-counter based duration без изменения публичного смысла stage status.
   - Проверки: telemetry JSON shape/backward compatibility.

4. **Сделать read audit report для repeated CSV/Excel reads.**
   - Отдельная read-only QA команда может считать частоту чтения ключевых datasets за run.
   - Это безопаснее, чем сразу внедрять cache.

5. **Подготовить manifest-based skip RFC.**
   - Начать с charts stage 8 и monthly charts, потому что это самые дорогие deterministic generated stages.
   - Skip должен быть opt-in.

## Что не менялось

- Финансовая методология не менялась.
- Yield metrics scope `ОФЗ-ПД only` не менялся.
- Outputs schema не менялась.
- Source registry mode/default не менялись.
- Raw storage не мутировался этим этапом вручную.
- Release bundle и BI package не строились.
- Generated outputs, `data/processed`, telemetry и run manifests, созданные проверками, не предназначены для commit.

## Выполненные проверки

```powershell
.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Результат: все три проверки прошли успешно.

## NEXT.5 telemetry hardening result

Дата: 2026-06-24.

Кандидаты 1-3 из этого отчета реализованы отдельным small-scope этапом NEXT.5 без изменения методологии, output paths, chart semantics и source acquisition policy.

Добавлено в telemetry:

- `raw_file_scope_counts`;
- `generated_file_scope_counts`;
- `raw_active_files_count`;
- `raw_versions_files_count`;
- `generated_current_files_count`;
- `generated_archive_files_count`;
- `generated_tmp_cache_files_count`;
- `stage_duration_seconds_precise` для каждой stage row.

Свежая telemetry после hardening:

- file: `outputs/reports/telemetry/telemetry_20260624_151147_e980bc2b.json`;
- `raw_file_scope_counts`: `active=10`, `versions=2`, `registry=2`, `latest=1`, `final=1`, `other=8`, `total=14`;
- `generated_file_scope_counts`: `current=212`, `archive=1`, `tmp_cache=0`;
- slowest stage: `8` / построение графиков, `3.315637` sec precise duration.

Проверки: `py_compile`, `compileall`, full `ofz-run`, `telemetry_summary_smoke.py`, `ofz-schema`, `ofz-quality --fast`.

Осталось на будущие этапы: read audit для repeated CSV/Excel reads и opt-in manifest-based skip RFC. Cache/skip не внедрялся.

## Рекомендация

Не внедрять cache/skip в POSTP3.5. Следующий безопасный шаг - отдельный маленький этап telemetry hardening:

- разделить current-run outputs и archive inventory;
- уточнить raw file counters;
- повысить точность stage duration;
- добавить smoke test на telemetry JSON/Markdown.

После этого можно проектировать opt-in manifest-based skip для chart stages.
