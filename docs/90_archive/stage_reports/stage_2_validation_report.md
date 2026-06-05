# Проверка Этапа 2 - Data cleaning

Дата проверки: `2026-05-18`.

Проверка выполнена без изменения `data/raw/` и без перезаписи существующих файлов в `outputs/`.

## Проверенные артефакты

| Артефакт | Статус | Комментарий |
|---|---|---|
| `scripts/02_data_cleaning.py` | существует, обновлен | Скрипт ненулевой. В ходе проверки обновлена логика `format_assumption_flag` под актуальный system prompt. |
| `data/processed/ofz_auctions_clean.csv` | существует | Текущая версия содержит 678 строк и 28 колонок, но была сформирована до обновления логики `format_assumption_flag`. |
| `docs/data_cleaning_report.md` | существует | Текущая версия отражает предыдущий запуск Этапа 2 и должна быть регенерирована после ручного запуска обновленного скрипта. |
| `logs/pipeline.log` | существует | Логирование pipeline настроено через `logs/pipeline.log`. |

## Соответствие требованиям обновленного system prompt

| Требование | Статус | Комментарий |
|---|---|---|
| Читать raw-файлы из `data/raw/` | реализовано | Скрипт читает `.xlsx`, `.xls`, `.csv` из `data/raw/`. |
| Не изменять `data/raw/` | реализовано | Скрипт только читает raw-источники. |
| Объединять релевантные таблицы | реализовано | Таблицы из raw-файлов объединяются через `pd.concat`. |
| Нормализовать названия и схему колонок | реализовано | Выходная схема фиксируется через `STANDARD_COLUMNS`. |
| Парсить даты | реализовано | `auction_date` и `maturity_date` создаются через `parse_date`. |
| Парсить числовые колонки | реализовано | Числовые поля проходят через `utils.safe_to_numeric`. |
| Удалять полные дубликаты | реализовано | Используется `drop_duplicates()`. |
| Добавлять service columns | реализовано | Есть `source_file`, `source_sheet`, `source_row`, `processing_timestamp`. |
| Создавать `format` | реализовано | Колонка входит в `STANDARD_COLUMNS`. |
| Создавать `format_assumption_flag` | реализовано | Колонка входит в `STANDARD_COLUMNS`; логика флагов обновлена. |
| Нормализовать / определить колонки доходности | реализовано | `cutoff_yield_pct`, `weighted_avg_yield_pct`. |
| Нормализовать / определить колонки спроса | реализовано | `demand_amount_mln_rub`, `demand_satisfaction_ratio`, `demand_available`. |
| Нормализовать / определить предложение | реализовано | `offer_amount_mln_rub`. |
| Нормализовать / определить объем размещения | реализовано | `placement_amount_mln_rub`, `proceeds_mln_rub`. |
| Нормализовать / определить срок обращения | реализовано | `maturity_date`, `days_to_maturity`. |
| Документировать трансформации | частично реализовано | `docs/data_cleaning_report.md` есть, но требуется регенерация после обновления скрипта. |

## Правило по столбцу `Формат`

В текущем `data/processed/ofz_auctions_clean.csv` найдены старые значения:

- `missing_column_assumed_auction`;
- `source`.

Они не соответствуют допустимым значениям из обновленного system prompt:

- `explicit`;
- `assumed_missing_column_auction`;
- `assumed_pre_2024_auction`;
- `requires_review`.

В `scripts/02_data_cleaning.py` логика исправлена:

- если источник содержит явный формат, ставится `explicit`;
- если колонка `Формат` отсутствует, ставится `assumed_missing_column_auction`;
- если колонка есть, но значение пустое до `2024-01-01`, ставится `assumed_pre_2024_auction`;
- если колонка есть, но значение пустое с `2024-01-01`, ставится `requires_review`.

## Вывод по статусу Этапа 2

Этап 2 нельзя считать полностью актуальным по текущим generated artifacts, потому что `ofz_auctions_clean.csv` и `data_cleaning_report.md` были созданы до исправления `format_assumption_flag`.

Этап 2 можно считать восстановленным на уровне кода: `scripts/02_data_cleaning.py` обновлен под актуальные требования. Для финального подтверждения нужно вручную выполнить компиляцию и запуск проектным Python, потому что Codex sandbox не смог запустить `.venv`.

## Ограничение sandbox / manual check

Попытка runtime-проверки из Codex завершилась ошибкой запуска интерпретатора:

```text
did not find executable at 'C:\Users\Rockaudit\AppData\Local\Programs\Python\Python314\python.exe'
```

Это не считается поломкой `.venv`: ранее ручные запуски проектного Python выполнялись успешно.

## Команды ручной проверки

Проверка компиляции:

```powershell
& "C:\Users\Rockaudit\LLM_CHAT\ofz_analytics\.venv\Scripts\python.exe" -m py_compile "C:\Users\Rockaudit\LLM_CHAT\ofz_analytics\scripts\02_data_cleaning.py"
```

Ожидаемый результат: команда завершится без вывода.

Регенерация Этапа 2:

```powershell
& "C:\Users\Rockaudit\LLM_CHAT\ofz_analytics\.venv\Scripts\python.exe" "C:\Users\Rockaudit\LLM_CHAT\ofz_analytics\scripts\02_data_cleaning.py"
```

Ожидаемый результат:

- будет обновлен `data/processed/ofz_auctions_clean.csv`;
- будет обновлен `docs/data_cleaning_report.md`;
- в `logs/pipeline.log` появятся записи запуска Этапа 2;
- в распределении `format_assumption_flag` должны использоваться только допустимые значения: `explicit`, `assumed_missing_column_auction`, `assumed_pre_2024_auction`, `requires_review`.

После ручного запуска нужно повторно проверить `docs/data_cleaning_report.md` и `data/processed/ofz_auctions_clean.csv`.
