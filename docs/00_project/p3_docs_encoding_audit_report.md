# P3.PRE.2 - отчет аудита кодировки документации

Date: 2026-06-16.

## Область проверки

- Checked `README.md`, `CHANGELOG.md`, `docs/**/*.md`, `prompts/**/*.md`, `scripts/**/*.md`, `tools/**/*.md`.
- Excluded `outputs/`, `releases/`, `.venv/`, `.git/`, binary files and raw XLSX inputs.
- Archived docs under `docs/archive/**/*.md`, `docs/90_archive/**/*.md` and `scripts/archive/**/*.md` were checked but not modified.
- Markdown documents checked: 130.

## Сводка

- fixed_utf8: 17
- fixed_utf8_pattern_reference: 1
- no_change: 112

## Документы

| path | encoding_detected | status | mojibake_detected | action | notes |
|---|---|---|---|---|---|
| `CHANGELOG.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/analytical_architecture.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/archive_deletion_policy.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/artifact_policy.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/00_project/dashboard_architecture.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/docs_archive_apply_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/docs_cleanup_apply_decision.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/docs_inventory_after_cleanup.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/00_project/docs_inventory_before_cleanup.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/00_project/final_project_summary.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/00_project/outputs_structure.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/00_project/p2_completion_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/p2_modernization_progress_report.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/00_project/p2_roadmap_after_production_ready_v1.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/00_project/p2_starting_checkpoint.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/p3_docs_encoding_audit_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/p3_modernization_progress_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/p3_scripts_balance_audit_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/production_cleanup_baseline.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/production_readiness_report.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/00_project/project_inventory.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/scripts_archive_decision.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/00_project/scripts_inventory_before_cleanup.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/00_project/scripts_migration_plan.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/00_project/scripts_structure_plan.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/00_project/self_review.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/01_methodology/kpi_map.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/01_methodology/period_selection_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/01_methodology/revenue_kpi_map.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/01_methodology/table_columns_dictionary.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/02_data_contracts/analytical_tables_contract.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/02_data_contracts/bi_exports_contract.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/02_data_contracts/chart_data_contract.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/02_data_contracts/dashboard_exports_contract.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/02_data_contracts/processed_data_contract.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/02_data_contracts/semantic_model_v2.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/02_data_pipeline/data_audit.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/02_data_pipeline/data_cleaning_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/02_data_pipeline/feature_engineering.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/02_data_pipeline/raw_data_registry_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/02_data_pipeline/schema_validation_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/03_analytics/analytical_tables_limitations.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/03_analytics/analytical_tables_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/03_analytics/executive_summary.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/03_analytics/executive_summary_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/03_analytics/monthly_analytics_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/03_analytics/revenue_analytics_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/03_analytics/revenue_charts_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/03_pipeline/module_decomposition_plan.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/04_visualization/chart_build_limitations.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/04_visualization/monthly_visualization_strategy.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/04_visualization/palette_policy.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/04_visualization/visualization_strategy.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/05_dashboard/dashboard_exports_limitations.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/05_dashboard/dashboard_exports_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/05_dashboard/dashboard_semantic_model_v2.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/06_quality/anomaly_tests_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/06_quality/manual_checks_log.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `docs/06_quality/quality_gate_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/06_quality/run_manifest_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/06_quality/visual_regression_backend_decision.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/06_quality/visual_regression_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/07_operations/bi_release_package.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/07_operations/ci_workflow.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/07_operations/docker_plan.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/07_operations/environment.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/07_operations/production_runbook.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/07_operations/release_bundle_plan.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/07_operations/release_checklist.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/07_operations/ui_launcher_contract.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/07_operations/windows_setup.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/07_operations/word_vba_launcher_spec.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/90_archive/deprecated/bid_to_cover_outliers.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/90_archive/old_reproducibility/reproducibility_review_stages_1_3.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/bid_to_cover_outliers.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/bid_to_cover_outliers_20260520_114521.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/bid_to_cover_outliers__legacy_archive.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/boxplot_diagnostics.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/chart_improvement_diagnostics.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/chart_improvement_scope.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/charts_reorganization_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/current_modernization_baseline.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/current_stage_status_after_1_and_3.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/data_audit__before_doc_path_update_20260527_085939.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/data_audit_repro.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/data_audit_repro_20260520_114521.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/data_cleaning_report__before_doc_path_update_20260527_085939.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/data_cleaning_report_repro.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/data_cleaning_report_repro_20260520_114521.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/docs_cleanup_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/docs_reorganization_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/feature_engineering__before_doc_path_update_20260527_085939.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/feature_engineering_repro.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/feature_engineering_repro_20260520_114521.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/format_revenue_discount_chart_diagnostics.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/kpi_map__before_doc_path_update_20260527_085939.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/legacy_docs_archive_migration_dry_run.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/legacy_docs_archive_migration_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/outputs_reorganization_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/outputs_structure_migration_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/parameterized_reporting_plan.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/period_selection_report__before_doc_path_update_20260527_085939.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/python_pipeline_instructions.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/reorganization_initial_audit.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/reproducibility_diff_stages_1_3.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/reproducibility_diff_stages_1_3_20260520_114521.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/reproducibility_review_stages_1_3.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/reproducibility_review_stages_1_3_20260520_114521.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/reproducibility_review_stages_1_3__legacy_archive.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/second_modernization_baseline.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/stage_2_validation_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/stage_3_sync_report.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/archive/2026-06-15/stages_1_3_inventory.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `docs/index.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `prompts/codex_modernization_prompt_v4.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `prompts/codex_period_aggregation_update.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `prompts/codex_second_modernization_prompt.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `prompts/codex_system_prompt.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `prompts/ofz_p2_modernization_step_by_step_v5_cost_aware.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `prompts/ofz_p2_modernization_step_by_step_v6_full.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `prompts/ofz_p2_modernization_system_prompt_v3.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `prompts/ofz_p2_modernization_system_prompt_v4_cost_aware.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `prompts/ofz_p3_modernization_step_by_step.md` | utf-8 | checked | no | fixed_utf8_pattern_reference | Corrupted prose was normalized during P3.PRE.2; remaining pattern hits are the literal audit pattern list. |
| `prompts/ofz_p3_modernization_system_prompt.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `README.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `scripts/archive/2026-06-15/README.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `scripts/README.md` | utf-8 | fixed | no | fixed_utf8 | Normalized during P3.PRE.2; no configured mojibake patterns remain. |
| `tools/windows_launcher/README.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `tools/word_launcher/README.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |
| `tools/word_launcher/word_docm_build_instructions.md` | utf-8 | checked | no | no_change | No configured mojibake patterns found. |

## Верификация

- `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\audit_docs_encoding.py`: OK.
- `.\.venv\Scripts\python.exe scripts\maintenance\audit_docs_encoding.py --report`: OK; generated this report.

## Пропущенные проверки

- `ofz-quality --fast`: skipped because P3.PRE.2 is documentation/encoding only and pipeline behavior was not changed.
- `ofz-quality --full`: skipped because full quality gate is out of scope for the docs encoding audit.
