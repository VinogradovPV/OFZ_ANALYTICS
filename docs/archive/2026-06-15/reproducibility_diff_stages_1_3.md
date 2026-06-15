# Reproducibility diff report for stages 1-3

Generated at: `2026-05-18 10:33:36`.

This report compares existing main outputs with safe reproduction outputs. Known volatile timestamp fields are ignored for value-level CSV comparison.

| Output | Kind | Main exists | Repro exists | Status | Details |
|---|---|---:|---:|---|---|
| Stage 1 data audit doc | `markdown` | True | True | match | Normalized text matches. |
| Stage 2 clean dataset | `csv` | True | True | match | main_shape=(678, 27); repro_shape=(678, 27); same_columns=True; changed_cells=0; rows_only_in_main=0; rows_only_in_repro=0 |
| Stage 2 cleaning report | `markdown` | True | True | diff | main_lines=104; repro_lines=104 |
| Stage 3 features dataset | `csv` | True | True | match | main_shape=(678, 62); repro_shape=(678, 62); same_columns=True; changed_cells=0; rows_only_in_main=0; rows_only_in_repro=0 |
| Stage 3 feature report | `markdown` | True | True | diff | main_lines=113; repro_lines=113 |

## Details

### Stage 2 cleaning report

- Main: `docs/data_cleaning_report.md`
- Repro: `docs/data_cleaning_report_repro.md`
- main_lines=104; repro_lines=104

### Stage 3 feature report

- Main: `docs/feature_engineering.md`
- Repro: `docs/feature_engineering_repro.md`
- main_lines=113; repro_lines=113
