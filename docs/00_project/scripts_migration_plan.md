# Scripts Migration Plan

Документ описывает возможную будущую физическую реорганизацию `scripts/`. На текущем этапе перенос основных Python-скриптов не выполняется. Проект сохраняет действующие команды запуска из корня через `.\.venv\Scripts\python.exe`.

## Целевая структура

```text
scripts/
  pipeline/
  stages/
  qa/
  metadata/
  utils/
  maintenance/
```

## Предлагаемое распределение

### `scripts/pipeline/`

- `run_pipeline.py`
- `interactive_pipeline.py`
- `report_params.py`
- `period_filter.py`

### `scripts/stages/`

- `01_data_audit.py`
- `02_data_cleaning.py`
- `03_feature_engineering.py`
- `04_kpi_map.py`
- `05_visualization_strategy.py`
- `06_build_charts.py`
- `07_dashboard_exports.py`
- `08_analytical_tables.py`
- `09_monthly_analytics.py`
- `10_build_monthly_charts.py`
- `11_revenue_analytics.py`
- `12_build_revenue_charts.py`
- `generate_executive_summary.py`
- `build_semantic_model_v2.py`

### `scripts/qa/`

- `quality_gate.py`
- `schema_validation.py`
- `regression_tests.py`
- `smoke_tests.py`
- `html_chart_qa.py`
- `visual_regression.py`
- `anomaly_tests.py`

### `scripts/metadata/`

- `run_manifest.py`
- `raw_data_registry.py`

### `scripts/utils/`

- `config.py`
- `utils.py`
- `palette.py`
- `scatter_chart_policy.py`
- `compare_outputs.py`

### `scripts/maintenance/`

- `cleanup_docs.py`
- `reorganize_outputs.py`
- `migrate_outputs_structure.py`
- `maintenance/reorganize_docs.py`
- `maintenance/reorganize_charts.py`
- `maintenance/migrate_legacy_docs_archive.py`

## Условия будущего переноса

Физический перенос допустим только отдельным этапом с dry-run и проверкой обратной совместимости. Нельзя одновременно переносить скрипты и менять методологию расчетов.

Минимальные условия:

- сохранить существующие CLI-команды;
- обновить импорты без изменения поведения;
- добавить wrapper-файлы на старых путях;
- проверить `py_compile`;
- проверить `run_pipeline.py --all`;
- проверить `quality_gate.py`;
- обновить README и `scripts/README.md`;
- не изменять `data/raw/`.

## Wrapper Compatibility

После переноса старые пути должны оставаться рабочими через тонкие wrappers. Пример wrapper для `scripts/run_pipeline.py`:

```python
from scripts.pipeline.run_pipeline import main

if __name__ == "__main__":
    main()
```

Wrapper не должен содержать бизнес-логику. Его задача — сохранить старую точку входа для пользователей, документации и автоматических проверок.

## Рекомендуемый порядок миграции

1. Создать целевые подпапки и `__init__.py`.
2. Перенести один небольшой QA-скрипт в тестовом режиме.
3. Добавить wrapper на старом пути.
4. Проверить прямой запуск старого пути и нового пути.
5. Повторить для остальных групп.
6. Обновить `run_pipeline.py`, README, `scripts/README.md` и quality checks.
7. Удалять wrappers только после отдельного решения и завершенного периода обратной совместимости.
