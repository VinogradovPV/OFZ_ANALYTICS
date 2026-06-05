# Changelog

Все значимые изменения проекта фиксируются в этом файле. Формат записи: дата, изменение, проверка, результат и ограничения.

## 2026-05-25

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-05-25 | Добавлен `scripts/generate_executive_summary.py` для формирования `outputs/reports/executive_summary_<...>.md` и `docs/executive_summary_report.md` на основе рассчитанных источников. | Ручная: `.\.venv\Scripts\python.exe -m py_compile scripts\generate_executive_summary.py`; запуск с параметрами отчета. | Скрипт создан и подключен к Этапу 10 в `scripts/run_pipeline.py`. | Выводы формируются только при наличии analytical tables, monthly metrics, dashboard exports или chart data; отсутствующие источники документируются как ограничения. |
| 2026-05-25 | README полностью обновлен как русскоязычная инструкция проекта. | Статическая проверка на отсутствие абсолютных путей `C:\`, `Users`, `LLM_CHAT`. | Команды приведены к формату `.\.venv\Scripts\python.exe ...`. | README не заменяет runtime-проверку pipeline. |
| 2026-05-25 | Стабилизирован `yield_boxplot_by_ofz_type` для длинной ретроспективы. | Ручная: пересборка `scripts\06_build_charts.py`; QA через `scripts\html_chart_qa.py`. | Добавлен long-mode `facet_by_ofz_type`; X-периоды не должны схлопываться. | Старые HTML-графики требуют пересборки. |
| 2026-05-25 | Доработаны stacked structure charts. | Ручная: пересборка графиков; QA через `scripts\html_chart_qa.py`. | Добавлены totals над stacked-столбцами, доли сегментов и обновленная палитра сроков. | Малые сегменты могут не иметь внутренних подписей; детали доступны в hover и chart data. |
| 2026-05-25 | Обновлен `scripts/html_chart_qa.py`. | Ручная: `.\.venv\Scripts\python.exe scripts\html_chart_qa.py`. | Добавлены проверки long-mode boxplot, stacked structure charts, volume scale, Sankey subtitle и лимита подписей scatter. | QA статическая и не заменяет визуальную проверку HTML. |

## Ранее выполненные крупные блоки

| Дата | Изменение | Проверка | Результат | Ограничения |
|---|---|---|---|---|
| 2026-05-22 | Внедрены `--aggregation-mode cumulative|point`, cumulative как default и обновленная логика report periods. | Regression/schema validation. | Month/quarter cumulative строятся накопленным итогом; point сохраняет старое поведение. | Требуется не смешивать outputs разных режимов. |
| 2026-05-22 | Добавлен monthly layer и monthly charts. | `scripts\09_monthly_analytics.py`, `scripts\10_build_monthly_charts.py`. | Создается `data/processed/ofz_monthly_metrics.csv` и monthly HTML-графики. | Monthly layer зависит от корректно сформированного report scope. |
| 2026-05-22 | Упорядочена структура `outputs/`. | `scripts\reorganize_outputs.py --dry-run/--apply`. | Отчетные таблицы, chart data и dashboards разведены по папкам. | Архивные outputs не удаляются автоматически. |
| 2026-05-22 | Добавлены dashboard exports и semantic layer. | `scripts\07_dashboard_exports.py`. | Dashboard-ready CSV/JSON сохраняются в `outputs/dashboards/`. | Если report scope пуст, exports не формируются и требуется повторить этап period scope. |
