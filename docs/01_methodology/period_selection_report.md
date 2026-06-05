# Отчет выбора периодов

Дата формирования: `2026-06-05 12:07:04`.

## Параметры отчета

- `report_date`: `2026-05-01`
- `retrospective_years`: `4`
- `period_type`: `month`
- `aggregation_mode`: `cumulative`
- Количество периодов: `5`

## Методология

- Фильтрация выполняется по включительному интервалу: `auction_date >= report_period_start` и `auction_date <= report_period_end`.
- `cumulative` строит накопленный период с начала года до конца завершенного месяца или квартала.
- `point` сохраняет старое поведение: только конкретный завершенный месяц или квартал.

## Источник

- Dataset: `data/processed/ofz_auctions_features.csv`
- Строк в источнике: `678`
- Основная дата аукциона: `auction_date`

## Выбранные периоды

| Порядок | Период | Отображение | File label | Начало | Конец | Агрегация | Целевой | Строк | Статус |
|---:|---|---|---|---|---|---|---:|---:|---|
| 0 | `2022-M01-M04` | `2022: 01.01 - 04.30` | `2022_m01_m04` | `2022-01-01` | `2022-04-30` | `cumulative` | False | 5 | ok |
| 1 | `2023-M01-M04` | `2023: 01.01 - 04.30` | `2023_m01_m04` | `2023-01-01` | `2023-04-30` | `cumulative` | False | 34 | ok |
| 2 | `2024-M01-M04` | `2024: 01.01 - 04.30` | `2024_m01_m04` | `2024-01-01` | `2024-04-30` | `cumulative` | False | 37 | ok |
| 3 | `2025-M01-M04` | `2025: 01.01 - 04.30` | `2025_m01_m04` | `2025-01-01` | `2025-04-30` | `cumulative` | False | 45 | ok |
| 4 | `2026-M01-M04` | `2026: 01.01 - 04.30` | `2026_m01_m04` | `2026-01-01` | `2026-04-30` | `cumulative` | True | 42 | ok |

## Результат фильтрации

- Строк в report scope: `163`
- Пустых периодов: `0`
- Output: `data/processed/ofz_auctions_report_scope.csv`

## Добавленные колонки

- `aggregation_mode`
- `report_period_start`
- `report_period_end`
- `report_period_label`
- `report_period_display_label`
- `report_period_file_label`
- `report_period_order`
- `report_year`
- `report_period_type`
- `is_target_period`
