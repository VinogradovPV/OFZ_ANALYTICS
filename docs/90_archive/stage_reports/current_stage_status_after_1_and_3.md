# Текущий статус проекта после этапов 1 и 3

Дата формирования: `2026-05-18`.

Инвентаризация выполнена без изменения `data/raw/` и без перезаписи существующих outputs. Проверка основана на наличии файлов, размере артефактов, текущих отчетах `docs/` и заголовках processed datasets.

## 1. Подтверждение этапов файлами

| Этап | Статус | Подтверждающие файлы | Комментарий |
|---|---|---|---|
| Этап 1 - Data audit | подтвержден | `scripts/01_data_audit.py`, `docs/data_audit.md`, `logs/pipeline.log` | Скрипт и отчет ненулевые. Последний отчет фиксирует 8 raw Excel-файлов, 8 листов, отсутствие ошибок чтения и логирование. |
| Этап 2 - Data cleaning | частично подтвержден | `scripts/02_data_cleaning.py`, `data/processed/ofz_auctions_clean.csv`, `docs/data_cleaning_report.md` | Артефакты есть: clean dataset содержит 678 строк и 28 колонок. Есть риск несоответствия обновленному правилу `format_assumption_flag`. |
| Этап 3 - Feature engineering | частично подтвержден | `scripts/03_feature_engineering.py`, `data/processed/ofz_auctions_features.csv`, `docs/feature_engineering.md` | Features dataset содержит 678 строк и 61 колонку. Воспроизводимость ограничена отсутствием рабочего orchestration script и отсутствием `maturity_bucket_label`. |

## 2. Существующие outputs

| Каталог / файл | Состояние |
|---|---|
| `data/processed/ofz_auctions_clean.csv` | существует, 212785 байт, 678 строк данных по отчету Этапа 2 |
| `data/processed/ofz_auctions_features.csv` | существует, 512525 байт, 678 строк данных по отчету Этапа 3 |
| `outputs/` | файлов не найдено |
| `outputs/charts/` | пустой каталог или нет файлов |
| `outputs/exports/` | пустой каталог или нет файлов |
| `logs/pipeline.log` | существует, 19865 байт, содержит записи последнего запуска Этапа 1 |

Вывод: расчетные datasets этапов 2-3 существуют, но графики, exports и обязательные табличные отчеты еще не сформированы.

## 3. Существующие scripts

| Скрипт | Состояние |
|---|---|
| `scripts/01_data_audit.py` | существует, ненулевой |
| `scripts/02_data_cleaning.py` | существует, ненулевой |
| `scripts/03_feature_engineering.py` | существует, ненулевой |
| `scripts/config.py` | существует, ненулевой |
| `scripts/utils.py` | существует, ненулевой |
| `scripts/report_params.py` | существует, ненулевой |
| `scripts/period_filter.py` | отсутствует |
| `scripts/run_pipeline.py` | существует, но пустой placeholder |

## 4. Отсутствующие или проблемные файлы

- `scripts/period_filter.py` отсутствует.
- `data/processed/ofz_auctions_report_scope.csv` отсутствует.
- `docs/period_selection_report.md` отсутствует.
- `scripts/run_pipeline.py` пустой и не может считаться рабочим pipeline orchestrator.
- `scripts/08_analytical_tables.py` отсутствует.
- `docs/analytical_tables_report.md` отсутствует.
- `docs/analytical_tables_limitations.md` отсутствует.
- В `outputs/exports/` нет обязательных табличных отчетов.
- В `outputs/charts/` нет графиков.

## 5. Нарушенные зависимости

1. Этап 4 не может быть выполнен без `scripts/period_filter.py`.
2. `data/processed/ofz_auctions_report_scope.csv` отсутствует, поэтому KPI, визуализации, dashboard, executive summary и обязательные табличные отчеты не имеют параметризованного входного dataset.
3. `run_pipeline.py` пустой, поэтому этапы 1-3 пока не связаны в воспроизводимый общий запуск.
4. `scripts/config.py` содержит путь `FILTERED_REPORT_DATA_PATH = data/processed/filtered_report_data.csv`, тогда как обновленный workflow требует `data/processed/ofz_auctions_report_scope.csv`.
5. Обновленный промпт требует `maturity_bucket_label`, но в заголовке `ofz_auctions_features.csv` найден `maturity_bucket` без `maturity_bucket_label`.
6. Обновленный промпт задает допустимые значения `format_assumption_flag`: `explicit`, `assumed_missing_column_auction`, `assumed_pre_2024_auction`, `requires_review`. Текущий clean dataset и отчет Этапа 2 используют значения `missing_column_assumed_auction` и `source`, что требует нормализации.

## 6. Можно ли считать Этап 2 выполненным

Этап 2 можно считать выполненным по факту существования базовых артефактов: есть рабочий скрипт, clean dataset, отчет очистки, service columns, нормализованные поля, правило `Формат` и логирование.

Но по обновленному промпту Этап 2 требует ревизии перед дальнейшей параметризацией:

- привести `format_assumption_flag` к допустимым значениям из системного промпта;
- явно проверить, что правило до 2024 года разделяет случаи `assumed_missing_column_auction` и `assumed_pre_2024_auction`, если это применимо;
- убедиться, что нормализованы или определены candidate columns для доходности, спроса, предложения, объема размещения и срока обращения;
- при повторном запуске не перезаписывать существующие outputs вне safe/repro режима.

Итог: `completed with compatibility gaps`.

## 7. Можно ли считать Этап 3 воспроизводимым

Этап 3 подтвержден файлами и содержательным отчетом: features dataset построен из `ofz_auctions_clean.csv`, добавлено 33 признака, есть `maturity_bucket`, `ofz_type`, KPI-like признаки спроса, доходности, эффективности, концентрации и волатильности.

Полностью воспроизводимым Этап 3 пока считать нельзя, потому что:

- `run_pipeline.py` пустой;
- нет safe reproduction / compare механизма для проверки повторного результата;
- нет параметризованного report scope;
- отсутствует `maturity_bucket_label`, требуемый обновленным промптом;
- текущие категории `maturity_bucket` (`short`, `medium`, `long`, `ultra_long`) не совпадают с обновленными категориями `less_than_1_year`, `short_term`, `medium_term`, `long_term`, `requires_review`.

Итог: `artifact-confirmed, not fully reproducible under updated prompt`.

## 8. Действия перед переходом к параметризуемой отчетности

1. Актуализировать Этап 2 под обновленное правило `format_assumption_flag`.
2. Актуализировать Этап 3 под единую классификацию сроков обращения и добавить `maturity_bucket_label`.
3. Зафиксировать выбранную шкалу maturity buckets в документации, особенно из-за расхождения формулировок в обновленном промпте.
4. Создать `scripts/period_filter.py`.
5. Сформировать `data/processed/ofz_auctions_report_scope.csv`.
6. Сформировать `docs/period_selection_report.md`.
7. Обновить `scripts/config.py`, чтобы основной report scope путь был согласован с workflow.
8. Реализовать непустой `scripts/run_pipeline.py` с поддержкой `--stage`, `--stages`, `--all`, `--safe`, `--compare`, `--report-date`, `--retrospective-years`, `--period-type`.
9. После Этапа 4 переходить к KPI, обязательным табличным отчетам, визуализациям и dashboard/export слоям.

## 9. Ограничения проверки

- `data/raw/` не изменялся.
- Существующие outputs не перезаписывались.
- В текущей среде Codex ранее не мог запускать проектный Python из-за sandbox, но ручные проверки пользователя через `.venv` успешны. Это не считается поломкой `.venv`.
- Git-репозиторий ранее не определялся, поэтому статус отслеживается файловой инвентаризацией, а не `git status`.
