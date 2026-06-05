# Обзор запуска pipeline

Дата формирования: `2026-06-04 19:08:42`.

## Параметры запуска

- Этапы: `1, 2, 3, 4, 5, 6, 7, 8, 8.1, revenue_analytics, revenue_charts, monthly_analytics, monthly_charts, 9, 9.1, semantic_model_v2, 10, 11, 12`
- Safe mode: `False`
- Compare: `False`
- Interactive: `False`
- report_date: `2026-01-01`
- retrospective_years: `4`
- period_type: `year`
- aggregation_mode: `cumulative`

## Контракт данных

- `data/raw/` используется только как источник чтения.
- После feature engineering параметризуемый report scope формируется этапом 4.
- KPI, графики, аналитические таблицы, dashboard и executive summary должны использовать `data/processed/ofz_auctions_report_scope.csv`.
- Параметр `aggregation_mode` прокидывается во все параметризуемые downstream-скрипты.

## Safe mode

- Для этапов 1-3 переменная `OFZ_SAFE_REPRO=1` включает запись `_repro` артефактов.
- Downstream-этапы работают с основным report scope dataset и не получают safe-флаг автоматически.

## Отчет различий

- `docs/90_archive/old_reproducibility/reproducibility_diff_stages_1_3.md`
