# Отчет выбора периодов

Дата формирования: `2026-06-04 19:08:32`.

## Параметры отчета

- `report_date`: `2026-01-01`
- `retrospective_years`: `4`
- `period_type`: `year`
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
| 0 | `2021` | `2021` | `2021` | `2021-01-01` | `2021-12-31` | `cumulative` | False | 83 | ok |
| 1 | `2022` | `2022` | `2022` | `2022-01-01` | `2022-12-31` | `cumulative` | False | 37 | ok |
| 2 | `2023` | `2023` | `2023` | `2023-01-01` | `2023-12-31` | `cumulative` | False | 95 | ok |
| 3 | `2024` | `2024` | `2024` | `2024-01-01` | `2024-12-31` | `cumulative` | False | 104 | ok |
| 4 | `2025` | `2025` | `2025` | `2025-01-01` | `2025-12-31` | `cumulative` | True | 142 | ok |

## Результат фильтрации

- Строк в report scope: `461`
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
