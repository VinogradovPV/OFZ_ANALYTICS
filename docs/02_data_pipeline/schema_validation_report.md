# Отчет schema validation

Документ описывает проверки, которые выполняет `scripts/schema_validation.py`.

## Проверяемая периодная логика

- `--aggregation-mode` задает режим агрегации отчетного периода.
- Допустимые значения: `cumulative` и `point`.
- Значение по умолчанию: `cumulative`.
- `month + cumulative`: `report_date=2026-05-01` означает интервал `2026-01-01` - `2026-04-30`.
- `month + point`: `report_date=2026-05-01` означает только апрель 2026, то есть `2026-04-01` - `2026-04-30`.
- `quarter + cumulative`: `report_date=2026-07-01` означает интервал `2026-01-01` - `2026-06-30`.
- `quarter + point`: `report_date=2026-07-01` означает только II квартал 2026, то есть `2026-04-01` - `2026-06-30`.
- `year`: `report_date=2026-01-01` означает завершенный год перед отчетной датой, то есть `2025-01-01` - `2025-12-31`.
- Ретроспектива сравнивает аналогичные интервалы прошлых лет.
- Outputs для `cumulative` и `point` не должны смешиваться: `aggregation_mode` включается в имена файлов и metadata.

## Проверки report scope

- `aggregation_mode` существует и принимает только `cumulative|point`.
- `report_period_start` и `report_period_end` заполнены и распознаются как даты.
- Для `month+cumulative` и `quarter+cumulative` период начинается 1 января.
- Для `month+point` период охватывает один месяц.
- Для `quarter+point` период охватывает один квартал.
- Количество периодов равно `retrospective_years + 1`.
- Есть ровно один целевой период `is_target_period == True`.

## Проверки monthly layer

- `data/processed/ofz_monthly_metrics.csv` существует после запуска `scripts/09_monthly_analytics.py`.
- `month_number` находится в диапазоне 1-12.
- Для `month+cumulative+2026-05-01` в целевом году нет месяца 5 и далее.
- `cumulative_placement_volume` не меньше `total_placement_volume` в соответствующем месяце.
- `cumulative_placement_volume` монотонно не убывает внутри каждого года, если месячный объем размещения неотрицателен.

## Команда проверки

```powershell
& "C:\Users\Rockaudit\LLM_CHAT\ofz_analytics\.venv\Scripts\python.exe" "C:\Users\Rockaudit\LLM_CHAT\ofz_analytics\scripts\schema_validation.py" --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## 2026-06-04 - volume_bln_units

`schema_validation.py` проверяет, что chart data exports с объемными показателями содержат:

- поля `*_volume_bln` в млрд рублей;
- unit-поля, завершающиеся на `_unit`.

Для новых chart data exports с объемами обязательны unit-поля, например:

- `placement_volume_unit = "млрд рублей"`;
- `revenue_volume_unit = "млрд рублей"`;
- `nominal_revenue_gap_unit = "млрд рублей"`;
- `total_nominal_volume_unit = "млрд рублей"`.

Актуальная команда проверки из корня проекта:

```powershell
.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Результат после исправления production blocker:

```text
OK | volume_bln_units | ok
Schema validation passed: 16
```
