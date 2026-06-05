# Dry-run миграции старой docs/archive

Дата формирования: 2026-05-26.

Режим: `dry-run`.

Назначение: проверить план переноса старой папки `docs/archive/` в новую архивную структуру `docs/90_archive/` и вернуть `table_columns_dictionary.md` в методологическую документацию.

Файлы не переносились и не удалялись. При конфликтах имен в плане указан безопасный суффикс.

## План миграции

| Исходный путь | Новый путь | Категория | Действие | Статус | Примечание |
|---|---|---|---|---|---|
| `docs/archive/bid_to_cover_outliers.md` | `docs/90_archive/deprecated/bid_to_cover_outliers__legacy_archive.md` | archive/deprecated | move | planned | В целевой папке уже есть `bid_to_cover_outliers.md`; нужен безопасный суффикс. |
| `docs/archive/bid_to_cover_outliers_20260520_114521.md` | `docs/90_archive/deprecated/bid_to_cover_outliers_20260520_114521.md` | archive/deprecated | move | planned | Старый диагностический отчет по выбросам bid-to-cover. |
| `docs/archive/current_stage_status_after_1_and_3.md` | `docs/90_archive/stage_reports/current_stage_status_after_1_and_3.md` | archive/stage_reports | move | planned | Старый статус ранних этапов. |
| `docs/archive/data_audit_repro.md` | `docs/90_archive/old_reproducibility/data_audit_repro.md` | archive/old_reproducibility | move | planned | Старый repro-документ, не актуальная эксплуатационная версия. |
| `docs/archive/data_audit_repro_20260520_114521.md` | `docs/90_archive/old_reproducibility/data_audit_repro_20260520_114521.md` | archive/old_reproducibility | move | planned | Историческая копия repro-документа. |
| `docs/archive/data_cleaning_report_repro.md` | `docs/90_archive/old_reproducibility/data_cleaning_report_repro.md` | archive/old_reproducibility | move | planned | Старый repro-документ, не актуальная эксплуатационная версия. |
| `docs/archive/data_cleaning_report_repro_20260520_114521.md` | `docs/90_archive/old_reproducibility/data_cleaning_report_repro_20260520_114521.md` | archive/old_reproducibility | move | planned | Историческая копия repro-документа. |
| `docs/archive/feature_engineering_repro.md` | `docs/90_archive/old_reproducibility/feature_engineering_repro.md` | archive/old_reproducibility | move | planned | Старый repro-документ, не актуальная эксплуатационная версия. |
| `docs/archive/feature_engineering_repro_20260520_114521.md` | `docs/90_archive/old_reproducibility/feature_engineering_repro_20260520_114521.md` | archive/old_reproducibility | move | planned | Историческая копия repro-документа. |
| `docs/archive/parameterized_reporting_plan.md` | `docs/90_archive/deprecated/parameterized_reporting_plan.md` | archive/deprecated | move | planned | Старый план параметризованной отчетности; текущая логика описана в актуальных docs. |
| `docs/archive/python_pipeline_instructions.md` | `docs/90_archive/deprecated/python_pipeline_instructions.md` | archive/deprecated | move | planned | Старые инструкции запуска; актуальные команды должны жить в README и проектных docs. |
| `docs/archive/reproducibility_diff_stages_1_3.md` | `docs/90_archive/old_reproducibility/reproducibility_diff_stages_1_3.md` | archive/old_reproducibility | move | planned | Старый diff ранних этапов. |
| `docs/archive/reproducibility_diff_stages_1_3_20260520_114521.md` | `docs/90_archive/old_reproducibility/reproducibility_diff_stages_1_3_20260520_114521.md` | archive/old_reproducibility | move | planned | Историческая копия diff ранних этапов. |
| `docs/archive/reproducibility_review_stages_1_3.md` | `docs/90_archive/old_reproducibility/reproducibility_review_stages_1_3__legacy_archive.md` | archive/old_reproducibility | move | planned | В целевой папке уже есть `reproducibility_review_stages_1_3.md`; нужен безопасный суффикс. |
| `docs/archive/reproducibility_review_stages_1_3_20260520_114521.md` | `docs/90_archive/old_reproducibility/reproducibility_review_stages_1_3_20260520_114521.md` | archive/old_reproducibility | move | planned | Историческая копия review ранних этапов. |
| `docs/archive/stage_2_validation_report.md` | `docs/90_archive/stage_reports/stage_2_validation_report.md` | archive/stage_reports | move | planned | Старый отчет валидации этапа 2. |
| `docs/archive/stage_3_sync_report.md` | `docs/90_archive/stage_reports/stage_3_sync_report.md` | archive/stage_reports | move | planned | Старый sync-отчет этапа 3. |
| `docs/archive/stages_1_3_inventory.md` | `docs/90_archive/stage_reports/stages_1_3_inventory.md` | archive/stage_reports | move | planned | Старый inventory ранних этапов. |
| `docs/archive/table_columns_dictionary.md` | `docs/01_methodology/table_columns_dictionary.md` | methodology | restore | planned | Вернуть из старого архива в методологическую документацию. |

## Сводка

- Всего файлов в старом `docs/archive/`: `19`.
- Планируемый возврат в актуальные docs: `1`.
- Планируемые переносы в `docs/90_archive/deprecated/`: `4`.
- Планируемые переносы в `docs/90_archive/stage_reports/`: `4`.
- Планируемые переносы в `docs/90_archive/old_reproducibility/`: `10`.
- Планируемые переносы в `docs/90_archive/modernization/`: `0`.
- Файлы не удаляются.
- `docs/archive/` после apply можно будет оставить пустой до отдельного решения об удалении папки.

## Проверка неоднозначностей

- `table_columns_dictionary.md` не является устаревшим архивным документом по текущим правилам; его целевое место: `docs/01_methodology/`.
- `data_audit_repro.md`, `data_cleaning_report_repro.md`, `feature_engineering_repro.md` не возвращаются в `docs/02_data_pipeline/`, потому что это старые repro-версии. Актуальные эксплуатационные версии уже лежат в `docs/02_data_pipeline/`.
- Дубликаты `bid_to_cover_outliers.md` и `reproducibility_review_stages_1_3.md` требуют безопасных суффиксов, чтобы не перезаписать уже перенесенные файлы.
