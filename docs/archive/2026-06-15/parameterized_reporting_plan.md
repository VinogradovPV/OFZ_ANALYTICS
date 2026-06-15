# План параметризации отчетного pipeline

Дата плана: 2026-05-15

## 1. Цель

Убрать жесткую привязку pipeline к I кварталу 2026 года и перевести запуск итогового расчета на явные параметры:

```powershell
<python_executable> scripts/run_pipeline.py --report-date YYYY-MM-DD --retrospective-years N --period-type month|quarter|year
```

PowerShell остается только терминалом для запуска Python-команд. Логика выбора периода, чтения данных, фильтрации, расчета признаков, KPI, отчетов и графиков должна быть реализована в Python.

## 2. Базовая семантика параметров

`--report-date YYYY-MM-DD`:

- обязательный параметр итогового запуска;
- должен быть валидной датой;
- должен приходиться на первое число месяца;
- трактуется как дата отсечения, не включаемая в анализ;
- отчетный период заканчивается днем перед `report_date`.

Примеры:

- `--report-date 2026-02-01 --period-type month` означает месячный отчет за январь 2026;
- `--report-date 2026-04-01 --period-type quarter` означает квартальный отчет за I квартал 2026;
- `--report-date 2026-01-01 --period-type year` означает годовой отчет за 2025 год.

`--period-type month|quarter|year`:

- `month`: период от первого дня предыдущего месяца до `report_date`, не включая `report_date`;
- `quarter`: период от первого дня квартала, который завершился перед `report_date`, до `report_date`, не включая `report_date`;
- `year`: период от 1 января предыдущего календарного года до `report_date`, не включая `report_date`.

`--retrospective-years N`:

- обязательный положительный integer;
- задает число календарных лет в ретроспективе, включая год текущего отчетного периода;
- для `--report-date 2026-04-01 --period-type quarter --retrospective-years 3` нужно получить Q1 2024, Q1 2025 и Q1 2026;
- для годов отчета `N=3` при `--report-date 2026-01-01` означает 2023, 2024 и 2025 годы.

## 3. Скрипты, которые нужно изменить

### `scripts/run_pipeline.py`

Сейчас файл пустой. Его нужно сделать единой точкой запуска pipeline.

Новые обязанности:

- разобрать CLI-параметры;
- провалидировать `--report-date`, `--retrospective-years`, `--period-type`;
- создать объект контекста отчетности;
- передать контекст во все этапы;
- управлять режимом безопасного воспроизведения этапов 1-3;
- писать лог запуска с параметрами периода;
- возвращать ненулевой код при ошибках валидации или отсутствии данных.

### `scripts/config.py`

Нужно заменить жесткие константы `TARGET_YEARS = (2024, 2025, 2026)` и `TARGET_QUARTER = 1` на конфигурацию, совместимую с параметрами запуска.

Изменения:

- оставить пути и реестр raw-файлов;
- добавить шаблоны имен параметризованных output-файлов;
- добавить константы для legacy production-артефактов этапов 1-3;
- добавить константы для safe/repro-артефактов;
- добавить правила формата размещения до 2024 года.

### `scripts/utils.py`

Нужно расширить общие утилиты.

Новые обязанности:

- парсинг и валидация отчетной даты;
- построение отчетных периодов;
- генерация стабильного slug для периода;
- безопасная запись CSV/Markdown/изображений;
- нормализация отсутствующего столбца `Формат` в данных до 2024 года;
- единый расчет summary-проверок для clean/features/report datasets.

### `scripts/01_data_audit.py`

Сейчас файл пустой. Этап аудита должен остаться максимально независимым от периода, но отчет аудита нужно дополнить проверкой параметризуемости.

Изменения:

- читать все доступные raw-файлы;
- фиксировать, в каких годах есть или нет столбец `Формат`;
- явно документировать правило: до 2024 года все строки считаются `Аукцион`, ДРПА отсутствуют;
- проверять покрытие данных для запрошенного диапазона ретроспективы;
- в safe-режиме писать только `docs/data_audit_repro.md`.

### `scripts/02_data_cleaning.py`

Сейчас файл пустой. Это ключевой скрипт для снятия жесткой привязки к Q1 2024-2026.

Изменения:

- принимать отчетный контекст;
- читать raw-файлы за все годы, нужные для ретроспективы;
- применять фильтр по набору отчетных периодов, а не по `TARGET_QUARTER`;
- для данных до 2024 года создавать `auction_format = "Аукцион"`;
- исключить появление ДРПА до 2024 года как невозможного формата;
- сохранить совместимую схему clean dataset;
- добавить поля, полезные для параметризации: `period_type`, `report_date`, `period_start`, `period_end`, `period_label`, `retrospective_year_index`;
- в safe-режиме не перезаписывать `data/processed/ofz_auctions_clean.csv`.

### `scripts/03_feature_engineering.py`

Сейчас файл пустой. Признаки нужно сделать период-независимыми.

Изменения:

- принимать clean dataset и отчетный контекст;
- заменить признаки с суффиксом `_year_q1` на нейтральные периодные признаки;
- сохранить legacy-совместимость через alias-колонки только при воспроизведении старого Q1-сценария, если это нужно для сравнения;
- считать year-over-year и issue-level изменения относительно такого же месяца/квартала/года предыдущей ретроспективной точки;
- корректно обрабатывать ДРПА, где спрос и bid-to-cover не применимы;
- не ломать существующие флаги outlier и extreme ratios.

### `scripts/04_kpi_map.py`

Сейчас файл пустой. KPI должны строиться по параметризованному features dataset.

Изменения:

- принимать отчетный контекст;
- считать KPI для текущего отчетного периода и для ретроспективы;
- разделять метрики аукционов и ДРПА;
- добавлять сравнение с предыдущим аналогичным периодом;
- обновлять описания KPI так, чтобы они не ссылались на I квартал.

### `scripts/05_visualization_strategy.py`

Сейчас файл пустой. Стратегия визуализаций должна учитывать тип периода.

Изменения:

- генерировать список графиков для month/quarter/year;
- использовать `period_label` вместо захардкоженного `Q1`;
- предусмотреть разные подписи осей и заголовков для месяцев, кварталов и лет;
- отдельно отметить, какие графики должны исключать ДРПА или показывать их отдельной серией.

### `scripts/06_build_charts.py`

Сейчас файл пустой. Построение графиков должно идти от параметризованных данных.

Изменения:

- принимать отчетный контекст и outputs из KPI/strategy;
- писать графики в директории с периодным slug;
- обновлять заголовки, легенды и имена файлов;
- не перезаписывать графики старых запусков без явного режима overwrite.

## 4. Новые scripts, которые нужно создать

### `scripts/reporting_period.py`

Назначение: вся логика отчетных дат и периодов.

Нужные функции:

- `parse_report_date(value: str) -> date`
- `validate_report_date(report_date: date) -> None`
- `validate_period_type(period_type: str) -> None`
- `validate_retrospective_years(value: int) -> None`
- `get_current_period(report_date: date, period_type: str) -> ReportingPeriod`
- `get_retrospective_periods(report_date: date, period_type: str, retrospective_years: int) -> list[ReportingPeriod]`
- `make_period_label(period: ReportingPeriod) -> str`
- `make_period_slug(report_date: date, period_type: str, retrospective_years: int) -> str`

Нужные dataclass:

- `ReportingPeriod`
  - `period_type`
  - `start_date`
  - `end_date`
  - `label`
  - `year`
  - `month`
  - `quarter`
  - `is_current`

- `ReportingContext`
  - `report_date`
  - `period_type`
  - `retrospective_years`
  - `periods`
  - `current_period`
  - `slug`

### `scripts/io_sources.py`

Назначение: Python-слой чтения raw Excel и выбора нужных файлов.

Нужные функции:

- `list_raw_sources() -> dict[int, Path]`
- `select_sources_for_periods(periods: list[ReportingPeriod]) -> dict[int, Path]`
- `read_raw_auction_file(path: Path, source_year: int) -> pd.DataFrame`
- `read_raw_sources_for_context(context: ReportingContext) -> pd.DataFrame`

### `scripts/format_rules.py`

Назначение: централизовать правила формата размещения.

Нужные функции:

- `normalize_auction_format(df: pd.DataFrame) -> pd.DataFrame`
- `has_format_column(df: pd.DataFrame) -> bool`
- `fill_pre_2024_format(df: pd.DataFrame) -> pd.DataFrame`
- `validate_no_pre_2024_drpa(df: pd.DataFrame) -> None`

Правило:

- если `source_year < 2024` и столбца `Формат` нет, `auction_format = "Аукцион"`;
- ДРПА до 2024 года не создаются и не выводятся из косвенных признаков.

### `scripts/report_outputs.py`

Назначение: единая генерация путей для параметризованных результатов.

Нужные функции:

- `get_output_paths(context: ReportingContext, mode: str) -> OutputPaths`
- `ensure_output_tree(paths: OutputPaths) -> None`
- `write_run_manifest(context: ReportingContext, paths: OutputPaths, artifacts: list[Path]) -> Path`

Пример директории:

```text
outputs/reports/quarter_2026-04-01_y3/
outputs/charts/quarter_2026-04-01_y3/
data/processed/parameterized/quarter_2026-04-01_y3/
```

### `scripts/07_build_report.py`

Назначение: финальный отчетный слой после KPI и графиков.

Нужные функции:

- `build_markdown_report(context: ReportingContext, kpi: pd.DataFrame, charts: list[Path]) -> str`
- `write_report(context: ReportingContext, content: str) -> Path`

Этот скрипт нужен, если итоговый pipeline должен давать не только datasets и charts, но и человекочитаемый отчет.

## 5. CLI-параметры, которые нужно добавить

Обязательные:

- `--report-date YYYY-MM-DD`
- `--retrospective-years N`
- `--period-type month|quarter|year`

Служебные, рекомендуемые:

- `--stages 1 2 3 4 5 6 7` для частичного запуска;
- `--safe` для запрета перезаписи production-артефактов этапов 1-3;
- `--overwrite` для явной перезаписи параметризованных результатов с тем же slug;
- `--use-existing-stages-1-3` для запуска этапов 4+ от уже существующего `data/processed/ofz_auctions_features.csv`, когда нужен старый Q1 baseline;
- `--output-dir PATH` для альтернативного корня отчетных outputs, если потребуется.

Правила CLI:

- без `--report-date`, `--retrospective-years`, `--period-type` итоговый запуск должен падать с понятной ошибкой;
- `--report-date` не на первое число месяца должен падать с ошибкой;
- `--retrospective-years < 1` должен падать с ошибкой;
- `--period-type` вне `month|quarter|year` должен падать с ошибкой;
- для годового отчета `report_date` должен быть `YYYY-01-01`, иначе период "предыдущий год" будет неоднозначным для пользователя.

## 6. Отчеты и артефакты, которые нужно обновить

### Документация

- `docs/python_pipeline_instructions.md`
  - обновить команды запуска;
  - добавить примеры для месяца, квартала и года;
  - оставить требование использовать явный Python interpreter.

- `docs/data_audit.md` и `docs/data_audit_repro.md`
  - добавить раздел о наличии столбца `Формат` по годам;
  - зафиксировать правило для данных до 2024 года.

- `docs/data_cleaning_report.md` и `docs/data_cleaning_report_repro.md`
  - убрать формулировки "только I квартал 2024-2026" из общей логики;
  - добавить параметры запуска и список периодов ретроспективы.

- `docs/feature_engineering.md` и `docs/feature_engineering_repro.md`
  - переименовать описание Q1-specific признаков в периодные признаки;
  - описать поведение для month/quarter/year.

- `docs/stages_1_3_inventory.md`
  - не переписывать как часть параметризации;
  - при необходимости добавить отдельный appendix или новый diff-документ, чтобы сохранить историческую фиксацию этапа 0.

### Данные

Существующие production-файлы сохранить:

- `data/processed/ofz_auctions_clean.csv`
- `data/processed/ofz_auctions_features.csv`

Новые параметризованные outputs:

- `data/processed/parameterized/<slug>/ofz_auctions_clean.csv`
- `data/processed/parameterized/<slug>/ofz_auctions_features.csv`
- `data/processed/parameterized/<slug>/kpi.csv`
- `data/processed/parameterized/<slug>/run_manifest.json`

### Графики и финальные отчеты

Новые outputs:

- `outputs/charts/<slug>/...`
- `outputs/reports/<slug>/report.md`
- опционально `outputs/exports/<slug>/...`

В заголовках и подписях не должно быть жесткого `Q1 2026`; все должно строиться из `ReportingContext`.

## 7. Риски совместимости

1. Существующие признаки с именами `placement_share_in_year_q1`, `demand_share_in_year_q1`, `issue_placement_share_in_year_q1`, `issue_demand_share_in_year_q1` завязаны на Q1. Их нужно заменить на нейтральные имена, например `placement_share_in_period_year`, но это может сломать будущие этапы 4-6, если они ожидают старые колонки.

2. Данные 2022-2023 не имеют столбца `Формат`. Если правило "до 2024 все Аукцион" применить не в одном месте, возможны расхождения между cleaning, KPI и отчетами.

3. В старом Q1 production dataset есть только 2024-2026. При ретроспективе, которая требует 2022-2023, нельзя использовать старый features-файл как источник истины; нужно читать raw Excel и строить новый parameterized dataset.

4. ДРПА до 2024 года отсутствуют. Метрики, где формат используется как категория, должны показывать нули или отсутствие категории осознанно, а не считать это пропуском данных.

5. Годовой отчет за 2025 при `--report-date 2026-01-01` будет требовать полный 2025 год. Нужно проверять полноту raw-файла и явно предупреждать, если источник обрывается раньше конца периода.

6. Текущий raw-файл 2026 содержит данные до 2026-05-06. Для отчетов после этой даты нужна проверка, что период полностью покрыт источниками.

7. Старые docs из этапов 1-3 имеют историческую ценность. Их нельзя автоматически переписать при обычном параметризованном запуске.

8. Имена output-файлов без slug приведут к перезаписи результатов разных запусков. Все новые результаты должны быть разнесены по периодным директориям.

## 8. Как сохранить уже выполненные результаты этапов 1-3

1. Считать текущие файлы этапов 1-3 production baseline:

- `docs/data_audit.md`
- `docs/data_cleaning_report.md`
- `docs/feature_engineering.md`
- `data/processed/ofz_auctions_clean.csv`
- `data/processed/ofz_auctions_features.csv`

2. Не перезаписывать эти файлы в параметризованном pipeline по умолчанию.

3. Для воспроизведения старого состояния использовать только `_repro`-артефакты:

- `docs/data_audit_repro.md`
- `docs/data_cleaning_report_repro.md`
- `docs/feature_engineering_repro.md`
- `data/processed/ofz_auctions_clean_repro.csv`
- `data/processed/ofz_auctions_features_repro.csv`
- `docs/reproducibility_diff_stages_1_3.md`

4. Для новых параметризованных запусков писать результаты в отдельные директории со slug:

```text
data/processed/parameterized/<slug>/
outputs/charts/<slug>/
outputs/reports/<slug>/
logs/<slug>.log
```

5. Для сценария, эквивалентного старому Q1 dataset, использовать:

```powershell
<python_executable> scripts/run_pipeline.py --report-date 2026-04-01 --period-type quarter --retrospective-years 3 --safe
```

6. После реализации сравнить новый parameterized Q1-результат со старым production baseline через отдельный diff-report, не перезаписывая старые файлы.

## 9. Рекомендуемая последовательность реализации

1. Создать `scripts/reporting_period.py` и покрыть его проверками для month/quarter/year.
2. Создать `scripts/report_outputs.py`, чтобы сразу исключить случайную перезапись старых результатов.
3. Обновить `scripts/run_pipeline.py` и CLI-валидацию.
4. Создать `scripts/io_sources.py` и `scripts/format_rules.py`.
5. Реализовать параметризованный `scripts/02_data_cleaning.py`.
6. Реализовать период-независимый `scripts/03_feature_engineering.py`.
7. Добавить safe reproduction для этапов 1-3 и diff с текущими production-файлами.
8. Реализовать `scripts/04_kpi_map.py`, `scripts/05_visualization_strategy.py`, `scripts/06_build_charts.py`.
9. Создать `scripts/07_build_report.py`, если нужен итоговый Markdown-отчет.
10. Обновить документацию запуска и примеры команд.

## 10. Критерии готовности

- Pipeline запускается через Python с обязательными параметрами `--report-date`, `--retrospective-years`, `--period-type`.
- Невалидная отчетная дата, например `2026-04-02`, отклоняется.
- Поддерживаются month, quarter и year.
- Сценарий `2026-04-01 / quarter / 3` воспроизводит текущую бизнес-рамку Q1 2024-2026 без перезаписи production-файлов.
- Данные до 2024 года получают `auction_format = "Аукцион"`.
- ДРПА до 2024 года не появляются в результатах.
- Все новые результаты пишутся в параметризованные директории.
- PowerShell не содержит pipeline-логики и используется только для запуска Python-команд.
