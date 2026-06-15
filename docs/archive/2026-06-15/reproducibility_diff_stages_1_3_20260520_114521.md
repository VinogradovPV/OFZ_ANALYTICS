# Отчет различий воспроизводимости этапов 1-3

Дата формирования: `2026-05-20 09:10:03`.

Отчет сравнивает основные outputs с outputs безопасного воспроизведения. Из CSV-сравнения исключаются заведомо изменчивые timestamp-поля.

| Output | Тип | Основной существует | Repro существует | Статус | Детали |
|---|---|---:|---:|---|---|
| Этап 1: отчет аудита данных | `markdown` | True | True | match | Нормализованный текст совпадает. |
| Этап 2: очищенный dataset | `csv` | True | True | diff | main_shape=(678, 27); repro_shape=(678, 28); same_columns=False; changed_cells=None; rows_only_in_main=0; rows_only_in_repro=0 |
| Этап 2: отчет очистки данных | `markdown` | True | True | diff | main_lines=104; repro_lines=113 |
| Этап 3: dataset признаков | `csv` | True | True | diff | main_shape=(678, 62); repro_shape=(678, 70); same_columns=False; changed_cells=None; rows_only_in_main=629; rows_only_in_repro=629 |
| Этап 3: отчет построения признаков | `markdown` | True | True | diff | main_lines=113; repro_lines=137 |

## Детали

### Этап 2: очищенный dataset

- Основной файл: `data/processed/ofz_auctions_clean.csv`
- Repro-файл: `data/processed/ofz_auctions_clean_repro.csv`
- Old shape: `(678, 27)`
- New shape: `(678, 28)`
- Same columns: `False`
- Same values: `False`
- Changed cells: `None`
- Columns added: `['data_quality_flag']`
- Columns removed: `[]`

### Этап 2: отчет очистки данных

- Основной файл: `docs/data_cleaning_report.md`
- Repro-файл: `docs/data_cleaning_report_repro.md`
- main_lines=104; repro_lines=113

### Этап 3: dataset признаков

- Основной файл: `data/processed/ofz_auctions_features.csv`
- Repro-файл: `data/processed/ofz_auctions_features_repro.csv`
- Old shape: `(678, 62)`
- New shape: `(678, 70)`
- Same columns: `False`
- Same values: `False`
- Changed cells: `None`
- Columns added: `['data_quality_flag', 'cutoff_price', 'weighted_avg_price', 'cutoff_yield', 'discount_to_nominal', 'cutoff_yield_spread', 'demand_to_placement_ratio', 'ratio_basis']`
- Columns removed: `[]`

### Этап 3: отчет построения признаков

- Основной файл: `docs/feature_engineering.md`
- Repro-файл: `docs/feature_engineering_repro.md`
- main_lines=113; repro_lines=137
