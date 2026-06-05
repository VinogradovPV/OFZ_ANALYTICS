# Инвентаризация этапов 1-3

Дата формирования: `2026-05-15 18:26:13`.

Отчет создан, потому что обнаружены артефакты ранних этапов pipeline.

## Статус этапов 1-3

| Этап | Статус | Найдено | Не хватает | Комментарий |
| --- | --- | --- | --- | --- |
| Этап 1 - Data audit | completed | scripts/01_data_audit.py<br>docs/data_audit.md | - | Выполнен, если есть скрипт аудита и документированный отчет. |
| Этап 2 - Data cleaning | completed | scripts/02_data_cleaning.py<br>data/processed/ofz_auctions_clean.csv<br>docs/data_cleaning_report.md | - | Выполнен, если есть скрипт, очищенный dataset и отчет очистки. |
| Этап 3 - Feature engineering | completed | scripts/03_feature_engineering.py<br>data/processed/ofz_auctions_features.csv<br>docs/feature_engineering.md | - | Выполнен, если есть скрипт, feature dataset и документация. |
| Этап 10 - Executive summary | missing | - | docs/executive_summary.md | Выполнен, если создан параметризуемый executive summary. |
| Этап 11 - Self-review | missing | - | docs/self_review.md | Выполнен, если создан self-review проекта. |
| Этап 12 - Final project summary | missing | - | docs/final_project_summary.md | Выполнен, если создан финальный обзор проекта. |

## Данные этапов 1-3

| Файл | Тип | Описание |
| --- | --- | --- |
| data/processed/ofz_auctions_clean.csv | csv | 678 data rows; 28 columns; columns: source_file, source_sheet, source_row, source_year, quarter, period, auction_date, format, format_assumption_flag, auction_format, issue_code, security_type, ... |
| data/processed/ofz_auctions_features.csv | csv | 678 data rows; 61 columns; columns: source_file, source_sheet, source_row, source_year, quarter, period, auction_date, format, format_assumption_flag, auction_format, issue_code, security_type, ... |

## Документация этапов 1-3

| Документ | Размер, байт | Изменен |
| --- | --- | --- |
| docs/data_audit.md | 26643 | 2026-05-15 15:52:16 |
| docs/data_cleaning_report.md | 3455 | 2026-05-15 17:24:10 |
| docs/feature_engineering.md | 2399 | 2026-05-15 17:39:45 |
| docs/stages_1_3_inventory.md | 2415 | 2026-05-15 18:21:09 |

## Вывод

Этап считается выполненным только при наличии скрипта, основного output и документации. Если статус `partial`, нужна доработка воспроизводимости или документации.
