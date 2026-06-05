# Упорядочивание outputs/exports

Дата формирования: `2026-05-21 12:56:08`.

Режим: `apply`.

Скрипт работает только с файлами из корня `outputs/exports`, не удаляет файлы и не перезаписывает существующие артефакты молча.

| Исходный файл | Новый путь | Категория | Действие | Примечание |
| --- | --- | --- | --- | --- |
| - | - | - | no_files | В корне `outputs/exports` нет файлов для переноса. |

## Smoke checks для структуры outputs

`scripts/smoke_tests.py` и `scripts/schema_validation.py` на момент проверки отсутствуют, поэтому кодовые проверки в них не обновлялись.

После появления smoke tests они должны проверять наличие:

- `outputs/reports/analytical_tables/`
- `outputs/reports/monthly_tables/`
- `outputs/exports/analytical_csv/`
- `outputs/exports/chart_data/risk_quadrant/`
- `outputs/exports/chart_data/sankey/`
- `outputs/exports/chart_data/boxplot/`
- `outputs/exports/chart_data/structure/`
- `outputs/dashboards/`

Отдельная проверка после нового запуска pipeline: отчетные `.xlsx` не должны попадать напрямую в корень `outputs/exports/`.
