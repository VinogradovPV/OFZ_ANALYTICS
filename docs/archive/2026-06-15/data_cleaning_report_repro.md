# Отчет об очистке данных

Дата формирования: 2026-05-18 10:33:36

## Краткий вывод

Прочитано raw-файлов: 8.
Прочитано таблиц/листов: 8.
Строк до удаления полных дубликатов: 678.
Строк после удаления полных дубликатов: 678.
Удалено полных дубликатов: 0.

Исходные данные в `data/raw/` не изменялись.

## Источники

| Файл | Размер, байт | Таблиц/листов |
|---|---:|---:|
| `INTERNET_Auction_Results_rus_2019_20191218.xlsx` | 23 528 | 1 |
| `INTERNET_Auction_Results_rus_2020_20201223.xlsx` | 23 517 | 1 |
| `INTERNET_Auction_Results_rus_2021_20211223.xlsx` | 22 945 | 1 |
| `INTERNET_Auction_Results_rus_2022_20221222.xlsx` | 16 563 | 1 |
| `INTERNET_Auction_Results_rus_2023_20231231.xlsx` | 24 162 | 1 |
| `INTERNET_Auction_Results_rus_2024_20241231.xlsx` | 25 414 | 1 |
| `INTERNET_Auction_Results_rus_2025_20251231.xlsx` | 30 160 | 1 |
| `INTERNET_Auction_Results_rus_2026_20260507.xlsx` | 18 426 | 1 |

## Нормализованная схема

| Колонка | Тип pandas | Пропусков |
|---|---|---:|
| `source_file` | `str` | 0 |
| `source_sheet` | `str` | 0 |
| `source_row` | `int64` | 0 |
| `source_year` | `Int64` | 0 |
| `quarter` | `Int64` | 0 |
| `period` | `string` | 0 |
| `auction_date` | `str` | 0 |
| `format` | `string` | 0 |
| `format_assumption_flag` | `object` | 0 |
| `auction_format` | `string` | 0 |
| `issue_code` | `string` | 0 |
| `security_type` | `string` | 0 |
| `maturity_date` | `str` | 0 |
| `days_to_maturity` | `Int64` | 0 |
| `offer_amount_mln_rub` | `Float64` | 0 |
| `cutoff_price_pct` | `Float64` | 42 |
| `weighted_avg_price_pct` | `Float64` | 42 |
| `cutoff_yield_pct` | `Float64` | 106 |
| `weighted_avg_yield_pct` | `Float64` | 106 |
| `demand_amount_mln_rub` | `Float64` | 79 |
| `placement_amount_mln_rub` | `Float64` | 1 |
| `proceeds_mln_rub` | `Float64` | 1 |
| `demand_satisfaction_ratio` | `Float64` | 79 |
| `demand_available` | `bool` | 0 |
| `yield_available` | `bool` | 0 |
| `failed_or_no_deal` | `boolean` | 0 |
| `marker_fields` | `object` | 0 |
| `processing_timestamp` | `str` | 0 |

## Правило по столбцу `Формат`

- Если столбец `Формат` присутствует и значение заполнено, `format_assumption_flag = "explicit"`.
- Если столбец `Формат` отсутствует, `format = "Аукцион"`, `format_assumption_flag = "assumed_missing_column_auction"`.
- Если `format` пустой и дата ранее `2024-01-01`, `format = "Аукцион"`, `format_assumption_flag = "assumed_pre_2024_auction"`.
- Если `format` пустой начиная с `2024-01-01`, `format_assumption_flag = "requires_review"`.
- Допустимые значения флага: `explicit`, `assumed_missing_column_auction`, `assumed_pre_2024_auction`, `requires_review`.

### Распределение `format`

| format | Строк |
|---|---:|
| `Аукцион` | 600 |
| `ДРПА` | 78 |

### Распределение `format_assumption_flag`

| format_assumption_flag | Строк |
|---|---:|
| `assumed_missing_column_auction` | 386 |
| `explicit` | 292 |

## Контроль качества

- Годы в `auction_date`: `2019`, `2020`, `2021`, `2022`, `2023`, `2024`, `2025`, `2026`.
- Кварталы: `1`, `2`, `3`, `4`.
- Полных дубликатов после очистки: 0.
- Строк `requires_review`: 0.

## Нормализованные аналитические колонки

| Направление | Колонки | Статус |
|---|---|---|
| доходность | `cutoff_yield_pct`, `weighted_avg_yield_pct` | ok |
| спрос | `demand_amount_mln_rub`, `demand_satisfaction_ratio`, `demand_available` | ok |
| предложение | `offer_amount_mln_rub` | ok |
| объем размещения | `placement_amount_mln_rub`, `proceeds_mln_rub` | ok |
| срок обращения | `maturity_date`, `days_to_maturity` | ok |

## Выходные артефакты

- `data/processed/ofz_auctions_clean_repro.csv`
- `docs/data_cleaning_report_repro.md`
- `logs/pipeline.log`
