# Обзор запуска pipeline

Дата формирования: `2026-05-20 11:41:30`.

## Параметры запуска

- Этапы: `1, 2, 3, 4, 5, 6, 7, 8, 8.1, 9, 9.1, 10, 11, 12`
- Safe mode: `False`
- Compare: `False`
- report_date: `2026-04-01`
- retrospective_years: `5`
- period_type: `quarter`

## Контракт данных

- `data/raw/` используется только как источник чтения.
- После feature engineering параметризуемый report scope формируется этапом 4.
- KPI, графики, аналитические таблицы, dashboard и executive summary должны использовать `data/processed/ofz_auctions_report_scope.csv`.
- При `--all` запускается этап 8.1 и формируются обязательные аналитические таблицы.

## Safe mode

- Для этапов 1-3 переменная `OFZ_SAFE_REPRO=1` включает запись `_repro` артефактов.
- Downstream-этапы работают с основным report scope dataset и не получают safe-флаг автоматически.

## Отчет различий

- `docs/reproducibility_diff_stages_1_3.md`
