# Reproducibility review for stages 1-3

Generated at: `2026-05-18 10:33:37`.

Run mode: `safe reproduction mode`.
Stages requested: `1, 2, 3`.
Compare requested: `True`.

## Safe mode behavior

- Stage 1 writes `docs/data_audit_repro.md` when `--safe` is used.
- Stage 2 writes `data/processed/ofz_auctions_clean_repro.csv` and `docs/data_cleaning_report_repro.md` when `--safe` is used.
- Stage 3 reads `ofz_auctions_clean_repro.csv` and writes `data/processed/ofz_auctions_features_repro.csv` plus `docs/feature_engineering_repro.md` when `--safe` is used.
- Main outputs are not overwritten in safe mode.

## Diff report

- `docs/reproducibility_diff_stages_1_3.md`

## Parameter arguments

- `report_date`: `None`
- `retrospective_years`: `None`
- `period_type`: `None`
