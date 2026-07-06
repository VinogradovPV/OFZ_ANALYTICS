"""Конфигурация проекта для аналитического pipeline ОФЗ.

Все пути строятся от корня проекта. Абсолютные пользовательские пути не
встраиваются в расчетные скрипты, чтобы pipeline оставался переносимым.
"""

from __future__ import annotations

import os
from pathlib import Path


# Канонические директории проекта.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CBR_RAW_DIR = RAW_DATA_DIR / "cbr"
CBR_KEY_RATE_RAW_DIR = CBR_RAW_DIR / "key_rate_inflation"
CBR_KEY_RATE_RAW_LATEST_DIR = CBR_KEY_RATE_RAW_DIR / "latest"
CBR_KEY_RATE_RAW_VERSIONS_DIR = CBR_KEY_RATE_RAW_DIR / "versions"
CBR_KEY_RATE_RAW_REGISTRY_DIR = CBR_KEY_RATE_RAW_DIR / "registry"
CBR_KEY_RATE_RAW_DAILY_CSV = CBR_KEY_RATE_RAW_LATEST_DIR / "cbr_key_rate_daily.csv"
CBR_KEY_RATE_RAW_DAILY_META_JSON = CBR_KEY_RATE_RAW_LATEST_DIR / "cbr_key_rate_daily.meta.json"
CBR_KEY_RATE_RAW_REGISTRY_CSV = CBR_KEY_RATE_RAW_REGISTRY_DIR / "cbr_key_rate_registry.csv"
CBR_KEY_RATE_RAW_REGISTRY_LATEST_JSON = CBR_KEY_RATE_RAW_REGISTRY_DIR / "cbr_key_rate_registry_latest.json"
CBR_KEY_RATE_RAW_XLSX = CBR_KEY_RATE_RAW_DIR / "cbr_key_rate_inflation_2019-01_2026-05.xlsx"
CBR_KEY_RATE_PROCESSED_CSV = PROCESSED_DATA_DIR / "cbr_key_rate_inflation_monthly.csv"
CBR_REFERENCE_DIR = PROCESSED_DATA_DIR / "reference"
CBR_KEY_RATE_DAILY_CSV = CBR_REFERENCE_DIR / "cbr_key_rate_daily.csv"
CBR_KEY_RATE_DAILY_META_JSON = CBR_REFERENCE_DIR / "cbr_key_rate_daily.meta.json"
CBR_KEY_RATE_MONTHLY_CSV = CBR_REFERENCE_DIR / "cbr_key_rate_monthly.csv"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CHARTS_DIR = OUTPUTS_DIR / "charts"
CHARTS_MONTHLY_DIR = CHARTS_DIR / "monthly"
CHARTS_MONTHLY_PLACEMENT_DIR = CHARTS_MONTHLY_DIR / "placement"
CHARTS_MONTHLY_DEMAND_SUPPLY_DIR = CHARTS_MONTHLY_DIR / "demand_supply"
CHARTS_MONTHLY_BID_COVER_DIR = CHARTS_MONTHLY_DIR / "bid_cover"
CHARTS_MONTHLY_YIELD_DIR = CHARTS_MONTHLY_DIR / "yield"
CHARTS_MONTHLY_STRUCTURE_DIR = CHARTS_MONTHLY_DIR / "structure"
CHARTS_MONTHLY_HEATMAP_DIR = CHARTS_MONTHLY_DIR / "heatmap"
CHARTS_RISK_DIR = CHARTS_DIR / "risk"
CHARTS_RISK_TARGET_PERIOD_DIR = CHARTS_RISK_DIR / "target_period"
CHARTS_RISK_RETROSPECTIVE_DIR = CHARTS_RISK_DIR / "retrospective"
CHARTS_RISK_OUTLIERS_DIR = CHARTS_RISK_DIR / "outliers"
CHARTS_RISK_LOGX_DIR = CHARTS_RISK_DIR / "logx"
CHARTS_RISK_FACET_DIR = CHARTS_RISK_DIR / "facet"
CHARTS_SCATTER_DIR = CHARTS_DIR / "scatter"
CHARTS_SCATTER_DISCOUNT_DEMAND_DIR = CHARTS_SCATTER_DIR / "discount_demand"
CHARTS_SCATTER_DISCOUNT_REVENUE_GAP_DIR = CHARTS_SCATTER_DIR / "discount_revenue_gap"
CHARTS_SCATTER_DEMAND_CUTOFF_DIR = CHARTS_SCATTER_DIR / "demand_cutoff"
CHARTS_SCATTER_FORMAT_TERMS_DIR = CHARTS_SCATTER_DIR / "format_terms"
CHARTS_SCATTER_YIELD_DEMAND_DIR = CHARTS_SCATTER_DIR / "yield_demand"
CHARTS_SCATTER_YIELD_DISCOUNT_DIR = CHARTS_SCATTER_DIR / "yield_discount"
CHARTS_YIELD_DIR = CHARTS_DIR / "yield"
CHARTS_YIELD_BOXPLOT_DIR = CHARTS_YIELD_DIR / "boxplot"
CHARTS_YIELD_OFZ_PD_DIR = CHARTS_YIELD_DIR / "ofz_pd"
CHARTS_SANKEY_DIR = CHARTS_DIR / "sankey"
CHARTS_SANKEY_STRUCTURE_DIR = CHARTS_SANKEY_DIR / "structure"
CHARTS_SANKEY_TARGET_PERIOD_DIR = CHARTS_SANKEY_DIR / "target_period"
CHARTS_SANKEY_PERIOD_DIR = CHARTS_SANKEY_DIR / "period"
CHARTS_STRUCTURE_DIR = CHARTS_DIR / "structure"
CHARTS_STRUCTURE_MATURITY_DIR = CHARTS_STRUCTURE_DIR / "maturity"
CHARTS_STRUCTURE_FORMAT_DIR = CHARTS_STRUCTURE_DIR / "format"
CHARTS_STRUCTURE_PLACEMENT_VOLUME_DIR = CHARTS_STRUCTURE_DIR / "placement_volume"
CHARTS_REVENUE_DIR = CHARTS_DIR / "revenue"
CHARTS_REVENUE_PERIOD_DIR = CHARTS_REVENUE_DIR / "period"
CHARTS_REVENUE_MONTHLY_DIR = CHARTS_REVENUE_DIR / "monthly"
CHARTS_REVENUE_GAP_DIR = CHARTS_REVENUE_DIR / "gap"
CHARTS_REVENUE_RATIO_DIR = CHARTS_REVENUE_DIR / "ratio"
CHARTS_REVENUE_BREAKDOWNS_DIR = CHARTS_REVENUE_DIR / "breakdowns"
CHARTS_ARCHIVE_DIR = CHARTS_DIR / "archive"
CHARTS_ARCHIVE_REVIEW_REQUIRED_DIR = CHARTS_ARCHIVE_DIR / "review_required"
REPORTS_DIR = OUTPUTS_DIR / "reports"
REPORTS_ANALYTICAL_TABLES_DIR = REPORTS_DIR / "analytical_tables"
REPORTS_MONTHLY_TABLES_DIR = REPORTS_DIR / "monthly_tables"
EXPORTS_DIR = OUTPUTS_DIR / "exports"
EXPORTS_ANALYTICAL_CSV_DIR = EXPORTS_DIR / "analytical_csv"
EXPORTS_CHART_DATA_DIR = EXPORTS_DIR / "chart_data"
EXPORTS_CHART_DATA_RISK_QUADRANT_DIR = EXPORTS_CHART_DATA_DIR / "risk_quadrant"
EXPORTS_CHART_DATA_SANKEY_DIR = EXPORTS_CHART_DATA_DIR / "sankey"
EXPORTS_CHART_DATA_BOXPLOT_DIR = EXPORTS_CHART_DATA_DIR / "boxplot"
EXPORTS_CHART_DATA_SCATTER_DIR = EXPORTS_CHART_DATA_DIR / "scatter"
EXPORTS_CHART_DATA_MONTHLY_DIR = EXPORTS_CHART_DATA_DIR / "monthly"
EXPORTS_CHART_DATA_STRUCTURE_DIR = EXPORTS_CHART_DATA_DIR / "structure"
EXPORTS_CHART_DATA_REVENUE_DIR = EXPORTS_CHART_DATA_DIR / "revenue"
EXPORTS_CHART_DATA_YIELD_DIR = EXPORTS_CHART_DATA_DIR / "yield"
EXPORTS_TECHNICAL_DIR = EXPORTS_DIR / "technical"
EXPORTS_REVIEW_REQUIRED_DIR = EXPORTS_TECHNICAL_DIR / "review_required"
DASHBOARDS_DIR = OUTPUTS_DIR / "dashboards"
DASHBOARDS_MONTHLY_DIR = DASHBOARDS_DIR / "monthly"
DASHBOARDS_SEMANTIC_LAYER_DIR = DASHBOARDS_DIR / "semantic_layer"
DASHBOARDS_SEMANTIC_MODEL_V2_DIR = DASHBOARDS_DIR / "semantic_model_v2"
ARCHIVE_DIR = OUTPUTS_DIR / "archive"
DOCS_DIR = PROJECT_ROOT / "docs"
DOCS_PROJECT_DIR = DOCS_DIR / "00_project"
DOCS_METHODOLOGY_DIR = DOCS_DIR / "01_methodology"
DOCS_DATA_PIPELINE_DIR = DOCS_DIR / "02_data_pipeline"
DOCS_ANALYTICS_DIR = DOCS_DIR / "03_analytics"
DOCS_VISUALIZATION_DIR = DOCS_DIR / "04_visualization"
DOCS_DASHBOARD_DIR = DOCS_DIR / "05_dashboard"
DOCS_QUALITY_DIR = DOCS_DIR / "06_quality"
DOCS_ARCHIVE_DIR = DOCS_DIR / "90_archive"
DOCS_ARCHIVE_MODERNIZATION_DIR = DOCS_ARCHIVE_DIR / "modernization"
DOCS_ARCHIVE_STAGE_REPORTS_DIR = DOCS_ARCHIVE_DIR / "stage_reports"
DOCS_ARCHIVE_OLD_REPRODUCIBILITY_DIR = DOCS_ARCHIVE_DIR / "old_reproducibility"
DOCS_ARCHIVE_DEPRECATED_DIR = DOCS_ARCHIVE_DIR / "deprecated"
LOGS_DIR = PROJECT_ROOT / "logs"

DOC_PATHS: dict[str, Path] = {
    "analytical_architecture.md": DOCS_PROJECT_DIR / "analytical_architecture.md",
    "dashboard_architecture.md": DOCS_PROJECT_DIR / "dashboard_architecture.md",
    "final_project_summary.md": DOCS_PROJECT_DIR / "final_project_summary.md",
    "outputs_structure.md": DOCS_PROJECT_DIR / "outputs_structure.md",
    "project_inventory.md": DOCS_PROJECT_DIR / "project_inventory.md",
    "scripts_migration_plan.md": DOCS_PROJECT_DIR / "scripts_migration_plan.md",
    "scripts_structure_plan.md": DOCS_PROJECT_DIR / "scripts_structure_plan.md",
    "self_review.md": DOCS_PROJECT_DIR / "self_review.md",
    "bid_to_cover_utils.md": DOCS_METHODOLOGY_DIR / "bid_to_cover_utils.md",
    "kpi_map.md": DOCS_METHODOLOGY_DIR / "kpi_map.md",
    "period_selection_report.md": DOCS_METHODOLOGY_DIR / "period_selection_report.md",
    "revenue_kpi_map.md": DOCS_METHODOLOGY_DIR / "revenue_kpi_map.md",
    "table_columns_dictionary.md": DOCS_METHODOLOGY_DIR / "table_columns_dictionary.md",
    "data_audit.md": DOCS_DATA_PIPELINE_DIR / "data_audit.md",
    "data_audit_repro.md": DOCS_DATA_PIPELINE_DIR / "data_audit_repro.md",
    "data_cleaning_report.md": DOCS_DATA_PIPELINE_DIR / "data_cleaning_report.md",
    "data_cleaning_report_repro.md": DOCS_DATA_PIPELINE_DIR / "data_cleaning_report_repro.md",
    "feature_engineering.md": DOCS_DATA_PIPELINE_DIR / "feature_engineering.md",
    "feature_engineering_repro.md": DOCS_DATA_PIPELINE_DIR / "feature_engineering_repro.md",
    "raw_data_registry_report.md": DOCS_DATA_PIPELINE_DIR / "raw_data_registry_report.md",
    "schema_validation_report.md": DOCS_DATA_PIPELINE_DIR / "schema_validation_report.md",
    "analytical_tables_limitations.md": DOCS_ANALYTICS_DIR / "analytical_tables_limitations.md",
    "analytical_tables_report.md": DOCS_ANALYTICS_DIR / "analytical_tables_report.md",
    "executive_summary.md": DOCS_ANALYTICS_DIR / "executive_summary.md",
    "executive_summary_report.md": DOCS_ANALYTICS_DIR / "executive_summary_report.md",
    "monthly_analytics_report.md": DOCS_ANALYTICS_DIR / "monthly_analytics_report.md",
    "revenue_analytics_report.md": DOCS_ANALYTICS_DIR / "revenue_analytics_report.md",
    "revenue_charts_report.md": DOCS_ANALYTICS_DIR / "revenue_charts_report.md",
    "boxplot_diagnostics.md": DOCS_VISUALIZATION_DIR / "boxplot_diagnostics.md",
    "chart_build_limitations.md": DOCS_VISUALIZATION_DIR / "chart_build_limitations.md",
    "line_marker_chart_style.md": DOCS_VISUALIZATION_DIR / "line_marker_chart_style.md",
    "monthly_visualization_strategy.md": DOCS_VISUALIZATION_DIR / "monthly_visualization_strategy.md",
    "palette_policy.md": DOCS_VISUALIZATION_DIR / "palette_policy.md",
    "visualization_strategy.md": DOCS_VISUALIZATION_DIR / "visualization_strategy.md",
    "dashboard_exports_limitations.md": DOCS_DASHBOARD_DIR / "dashboard_exports_limitations.md",
    "dashboard_exports_report.md": DOCS_DASHBOARD_DIR / "dashboard_exports_report.md",
    "dashboard_semantic_model_v2.md": DOCS_DASHBOARD_DIR / "dashboard_semantic_model_v2.md",
    "anomaly_tests_report.md": DOCS_QUALITY_DIR / "anomaly_tests_report.md",
    "charts_reorganization_report.md": DOCS_QUALITY_DIR / "charts_reorganization_report.md",
    "docs_reorganization_report.md": DOCS_QUALITY_DIR / "docs_reorganization_report.md",
    "manual_checks_log.md": DOCS_QUALITY_DIR / "manual_checks_log.md",
    "quality_gate_report.md": DOCS_QUALITY_DIR / "quality_gate_report.md",
    "regression_tests_report.md": DOCS_QUALITY_DIR / "regression_tests_report.md",
    "run_manifest_report.md": DOCS_QUALITY_DIR / "run_manifest_report.md",
    "smoke_tests_report.md": DOCS_QUALITY_DIR / "smoke_tests_report.md",
    "visual_regression_report.md": DOCS_QUALITY_DIR / "visual_regression_report.md",
    "current_modernization_baseline.md": DOCS_ARCHIVE_MODERNIZATION_DIR / "current_modernization_baseline.md",
    "second_modernization_baseline.md": DOCS_ARCHIVE_MODERNIZATION_DIR / "second_modernization_baseline.md",
    "cleanup_report.md": DOCS_ARCHIVE_STAGE_REPORTS_DIR / "cleanup_report.md",
    "docs_cleanup_report.md": DOCS_ARCHIVE_STAGE_REPORTS_DIR / "docs_cleanup_report.md",
    "outputs_reorganization_report.md": DOCS_ARCHIVE_STAGE_REPORTS_DIR / "outputs_reorganization_report.md",
    "outputs_structure_migration_report.md": DOCS_ARCHIVE_STAGE_REPORTS_DIR / "outputs_structure_migration_report.md",
    "reproducibility_review_stages_1_3.md": DOCS_ARCHIVE_OLD_REPRODUCIBILITY_DIR / "reproducibility_review_stages_1_3.md",
    "bid_to_cover_outliers.md": DOCS_ARCHIVE_DEPRECATED_DIR / "bid_to_cover_outliers.md",
    "parameterized_reporting_plan.md": DOCS_ARCHIVE_DEPRECATED_DIR / "parameterized_reporting_plan.md",
    "report_params.md": DOCS_ARCHIVE_DEPRECATED_DIR / "report_params.md",
    "reorganization_initial_audit.md": DOCS_ARCHIVE_DEPRECATED_DIR / "reorganization_initial_audit.md",
    "stages_1_3_inventory.md": DOCS_ARCHIVE_STAGE_REPORTS_DIR / "stages_1_3_inventory.md",
}

# Алиасы для обратной совместимости со скриптами, которые импортируют старые имена.
ROOT_DIR = PROJECT_ROOT
DATA_RAW_DIR = RAW_DATA_DIR
DATA_PROCESSED_DIR = PROCESSED_DATA_DIR
OUTPUT_REPORTS_DIR = REPORTS_DIR
EXPORTS_TECHNICAL_REVIEW_REQUIRED_DIR = EXPORTS_REVIEW_REQUIRED_DIR
OUTPUTS_ARCHIVE_DIR = ARCHIVE_DIR

PIPELINE_LOG_PATH = LOGS_DIR / "pipeline.log"

# Значения по умолчанию для параметризуемой отчетности.
DEFAULT_REPORT_DATE = None
DEFAULT_RETROSPECTIVE_YEARS = 2
DEFAULT_PERIOD_TYPE = "quarter"

# Исходные файлы, используемые этапами 1-3.
RAW_AUCTION_FILES = {
    2022: RAW_DATA_DIR / "INTERNET_Auction_Results_rus_2022_20221222.xlsx",
    2023: RAW_DATA_DIR / "INTERNET_Auction_Results_rus_2023_20231231.xlsx",
    2024: RAW_DATA_DIR / "INTERNET_Auction_Results_rus_2024_20241231.xlsx",
    2025: RAW_DATA_DIR / "INTERNET_Auction_Results_rus_2025_20251231.xlsx",
    2026: RAW_DATA_DIR / "INTERNET_Auction_Results_rus_2026_20260507.xlsx",
}

# Основные документы pipeline.
DATA_AUDIT_MAIN_DOC = DOC_PATHS["data_audit.md"]
DATA_CLEANING_REPORT_MAIN_DOC = DOC_PATHS["data_cleaning_report.md"]
FEATURE_ENGINEERING_MAIN_DOC = DOC_PATHS["feature_engineering.md"]
STAGES_1_3_INVENTORY_DOC = DOC_PATHS["stages_1_3_inventory.md"]
PARAMETERIZED_REPORTING_PLAN_PATH = DOC_PATHS["parameterized_reporting_plan.md"]
REPORT_PARAMS_DOC_PATH = DOC_PATHS["report_params.md"]
PERIOD_SELECTION_REPORT_PATH = DOC_PATHS["period_selection_report.md"]
KPI_MAP_DOC = DOC_PATHS["kpi_map.md"]
ANALYTICAL_TABLES_REPORT_DOC = DOC_PATHS["analytical_tables_report.md"]
ANALYTICAL_TABLES_LIMITATIONS_DOC = DOC_PATHS["analytical_tables_limitations.md"]
CHART_BUILD_LIMITATIONS_DOC = DOC_PATHS["chart_build_limitations.md"]

# Основные datasets.
OFZ_AUCTIONS_CLEAN_MAIN_CSV = PROCESSED_DATA_DIR / "ofz_auctions_clean.csv"
OFZ_AUCTIONS_FEATURES_MAIN_CSV = PROCESSED_DATA_DIR / "ofz_auctions_features.csv"
OFZ_AUCTIONS_REPORT_SCOPE_CSV = PROCESSED_DATA_DIR / "ofz_auctions_report_scope.csv"
FILTERED_REPORT_DATA_PATH = PROCESSED_DATA_DIR / "filtered_report_data.csv"

# Безопасные артефакты воспроизведения. Они не перезаписывают основные результаты.
DATA_AUDIT_REPRO_DOC = DOC_PATHS["data_audit_repro.md"]
DATA_CLEANING_REPORT_REPRO_DOC = DOC_PATHS["data_cleaning_report_repro.md"]
FEATURE_ENGINEERING_REPRO_DOC = DOC_PATHS["feature_engineering_repro.md"]
REPRO_DIFF_STAGES_1_3_DOC = DOCS_ARCHIVE_OLD_REPRODUCIBILITY_DIR / "reproducibility_diff_stages_1_3.md"

OFZ_AUCTIONS_CLEAN_REPRO_CSV = PROCESSED_DATA_DIR / "ofz_auctions_clean_repro.csv"
OFZ_AUCTIONS_FEATURES_REPRO_CSV = PROCESSED_DATA_DIR / "ofz_auctions_features_repro.csv"
FILTERED_REPORT_DATA_REPRO_PATH = PROCESSED_DATA_DIR / "filtered_report_data_repro.csv"

SAFE_REPRO_MODE = os.environ.get("OFZ_SAFE_REPRO", "").strip().lower() in {
    "1",
    "true",
    "yes",
}

DATA_AUDIT_DOC = DATA_AUDIT_REPRO_DOC if SAFE_REPRO_MODE else DATA_AUDIT_MAIN_DOC
DATA_CLEANING_REPORT_DOC = (
    DATA_CLEANING_REPORT_REPRO_DOC if SAFE_REPRO_MODE else DATA_CLEANING_REPORT_MAIN_DOC
)
FEATURE_ENGINEERING_DOC = (
    FEATURE_ENGINEERING_REPRO_DOC if SAFE_REPRO_MODE else FEATURE_ENGINEERING_MAIN_DOC
)
OFZ_AUCTIONS_CLEAN_CSV = (
    OFZ_AUCTIONS_CLEAN_REPRO_CSV if SAFE_REPRO_MODE else OFZ_AUCTIONS_CLEAN_MAIN_CSV
)
OFZ_AUCTIONS_FEATURES_CSV = (
    OFZ_AUCTIONS_FEATURES_REPRO_CSV if SAFE_REPRO_MODE else OFZ_AUCTIONS_FEATURES_MAIN_CSV
)

REQUIRED_DIRECTORIES = (
    RAW_DATA_DIR,
    CBR_RAW_DIR,
    CBR_KEY_RATE_RAW_DIR,
    CBR_KEY_RATE_RAW_LATEST_DIR,
    CBR_KEY_RATE_RAW_VERSIONS_DIR,
    CBR_KEY_RATE_RAW_REGISTRY_DIR,
    PROCESSED_DATA_DIR,
    DOCS_DIR,
    DOCS_PROJECT_DIR,
    DOCS_METHODOLOGY_DIR,
    DOCS_DATA_PIPELINE_DIR,
    DOCS_ANALYTICS_DIR,
    DOCS_VISUALIZATION_DIR,
    DOCS_DASHBOARD_DIR,
    DOCS_QUALITY_DIR,
    DOCS_ARCHIVE_DIR,
    DOCS_ARCHIVE_MODERNIZATION_DIR,
    DOCS_ARCHIVE_STAGE_REPORTS_DIR,
    DOCS_ARCHIVE_OLD_REPRODUCIBILITY_DIR,
    DOCS_ARCHIVE_DEPRECATED_DIR,
    OUTPUTS_DIR,
    CHARTS_DIR,
    CHARTS_MONTHLY_DIR,
    CHARTS_MONTHLY_PLACEMENT_DIR,
    CHARTS_MONTHLY_DEMAND_SUPPLY_DIR,
    CHARTS_MONTHLY_BID_COVER_DIR,
    CHARTS_MONTHLY_YIELD_DIR,
    CHARTS_MONTHLY_STRUCTURE_DIR,
    CHARTS_MONTHLY_HEATMAP_DIR,
    CHARTS_RISK_DIR,
    CHARTS_RISK_TARGET_PERIOD_DIR,
    CHARTS_RISK_RETROSPECTIVE_DIR,
    CHARTS_RISK_OUTLIERS_DIR,
    CHARTS_RISK_LOGX_DIR,
    CHARTS_RISK_FACET_DIR,
    CHARTS_SCATTER_DIR,
    CHARTS_SCATTER_DISCOUNT_DEMAND_DIR,
    CHARTS_SCATTER_DISCOUNT_REVENUE_GAP_DIR,
    CHARTS_SCATTER_DEMAND_CUTOFF_DIR,
    CHARTS_SCATTER_FORMAT_TERMS_DIR,
    CHARTS_SCATTER_YIELD_DEMAND_DIR,
    CHARTS_SCATTER_YIELD_DISCOUNT_DIR,
    CHARTS_YIELD_DIR,
    CHARTS_YIELD_BOXPLOT_DIR,
    CHARTS_YIELD_OFZ_PD_DIR,
    CHARTS_SANKEY_DIR,
    CHARTS_SANKEY_STRUCTURE_DIR,
    CHARTS_SANKEY_TARGET_PERIOD_DIR,
    CHARTS_SANKEY_PERIOD_DIR,
    CHARTS_STRUCTURE_DIR,
    CHARTS_STRUCTURE_MATURITY_DIR,
    CHARTS_STRUCTURE_FORMAT_DIR,
    CHARTS_STRUCTURE_PLACEMENT_VOLUME_DIR,
    CHARTS_REVENUE_DIR,
    CHARTS_REVENUE_PERIOD_DIR,
    CHARTS_REVENUE_MONTHLY_DIR,
    CHARTS_REVENUE_GAP_DIR,
    CHARTS_REVENUE_RATIO_DIR,
    CHARTS_REVENUE_BREAKDOWNS_DIR,
    CHARTS_ARCHIVE_DIR,
    CHARTS_ARCHIVE_REVIEW_REQUIRED_DIR,
    REPORTS_DIR,
    REPORTS_ANALYTICAL_TABLES_DIR,
    REPORTS_MONTHLY_TABLES_DIR,
    EXPORTS_DIR,
    EXPORTS_ANALYTICAL_CSV_DIR,
    EXPORTS_CHART_DATA_DIR,
    EXPORTS_CHART_DATA_RISK_QUADRANT_DIR,
    EXPORTS_CHART_DATA_SANKEY_DIR,
    EXPORTS_CHART_DATA_BOXPLOT_DIR,
    EXPORTS_CHART_DATA_SCATTER_DIR,
    EXPORTS_CHART_DATA_MONTHLY_DIR,
    EXPORTS_CHART_DATA_STRUCTURE_DIR,
    EXPORTS_CHART_DATA_REVENUE_DIR,
    EXPORTS_CHART_DATA_YIELD_DIR,
    EXPORTS_TECHNICAL_DIR,
    EXPORTS_REVIEW_REQUIRED_DIR,
    DASHBOARDS_DIR,
    DASHBOARDS_MONTHLY_DIR,
    DASHBOARDS_SEMANTIC_LAYER_DIR,
    DASHBOARDS_SEMANTIC_MODEL_V2_DIR,
    ARCHIVE_DIR,
    LOGS_DIR,
)

OUTPUT_DIRECTORIES = (
    OUTPUTS_DIR,
    CHARTS_DIR,
    CHARTS_MONTHLY_DIR,
    CHARTS_MONTHLY_PLACEMENT_DIR,
    CHARTS_MONTHLY_DEMAND_SUPPLY_DIR,
    CHARTS_MONTHLY_BID_COVER_DIR,
    CHARTS_MONTHLY_YIELD_DIR,
    CHARTS_MONTHLY_STRUCTURE_DIR,
    CHARTS_MONTHLY_HEATMAP_DIR,
    CHARTS_RISK_DIR,
    CHARTS_RISK_TARGET_PERIOD_DIR,
    CHARTS_RISK_RETROSPECTIVE_DIR,
    CHARTS_RISK_OUTLIERS_DIR,
    CHARTS_RISK_LOGX_DIR,
    CHARTS_RISK_FACET_DIR,
    CHARTS_SCATTER_DIR,
    CHARTS_SCATTER_DISCOUNT_DEMAND_DIR,
    CHARTS_SCATTER_DISCOUNT_REVENUE_GAP_DIR,
    CHARTS_SCATTER_DEMAND_CUTOFF_DIR,
    CHARTS_SCATTER_FORMAT_TERMS_DIR,
    CHARTS_SCATTER_YIELD_DEMAND_DIR,
    CHARTS_SCATTER_YIELD_DISCOUNT_DIR,
    CHARTS_YIELD_DIR,
    CHARTS_YIELD_BOXPLOT_DIR,
    CHARTS_YIELD_OFZ_PD_DIR,
    CHARTS_SANKEY_DIR,
    CHARTS_SANKEY_STRUCTURE_DIR,
    CHARTS_SANKEY_TARGET_PERIOD_DIR,
    CHARTS_SANKEY_PERIOD_DIR,
    CHARTS_STRUCTURE_DIR,
    CHARTS_STRUCTURE_MATURITY_DIR,
    CHARTS_STRUCTURE_FORMAT_DIR,
    CHARTS_STRUCTURE_PLACEMENT_VOLUME_DIR,
    CHARTS_REVENUE_DIR,
    CHARTS_REVENUE_PERIOD_DIR,
    CHARTS_REVENUE_MONTHLY_DIR,
    CHARTS_REVENUE_GAP_DIR,
    CHARTS_REVENUE_RATIO_DIR,
    CHARTS_REVENUE_BREAKDOWNS_DIR,
    CHARTS_ARCHIVE_DIR,
    CHARTS_ARCHIVE_REVIEW_REQUIRED_DIR,
    REPORTS_DIR,
    REPORTS_ANALYTICAL_TABLES_DIR,
    REPORTS_MONTHLY_TABLES_DIR,
    EXPORTS_DIR,
    EXPORTS_ANALYTICAL_CSV_DIR,
    EXPORTS_CHART_DATA_DIR,
    EXPORTS_CHART_DATA_RISK_QUADRANT_DIR,
    EXPORTS_CHART_DATA_SANKEY_DIR,
    EXPORTS_CHART_DATA_BOXPLOT_DIR,
    EXPORTS_CHART_DATA_SCATTER_DIR,
    EXPORTS_CHART_DATA_MONTHLY_DIR,
    EXPORTS_CHART_DATA_STRUCTURE_DIR,
    EXPORTS_CHART_DATA_REVENUE_DIR,
    EXPORTS_CHART_DATA_YIELD_DIR,
    EXPORTS_TECHNICAL_DIR,
    EXPORTS_REVIEW_REQUIRED_DIR,
    DASHBOARDS_DIR,
    DASHBOARDS_MONTHLY_DIR,
    DASHBOARDS_SEMANTIC_LAYER_DIR,
    DASHBOARDS_SEMANTIC_MODEL_V2_DIR,
    ARCHIVE_DIR,
)

TARGET_YEARS = (2024, 2025, 2026)
TARGET_QUARTER = 1


def get_doc_path(doc_name: str) -> Path:
    """Вернуть тематический путь документа по имени файла.

    Неизвестные stage-отчеты отправляются в архив этапов, остальные неизвестные
    markdown-документы - в deprecated, чтобы корень docs/ оставался чистым.
    """
    name = Path(doc_name).name
    if name in DOC_PATHS:
        return DOC_PATHS[name]
    lower_name = name.lower()
    if lower_name.startswith("stage_") and lower_name.endswith("_report.md"):
        return DOCS_ARCHIVE_STAGE_REPORTS_DIR / name
    if "repro" in lower_name or "reproducibility" in lower_name:
        return DOCS_ARCHIVE_OLD_REPRODUCIBILITY_DIR / name
    if "modernization" in lower_name:
        return DOCS_ARCHIVE_MODERNIZATION_DIR / name
    if "cleanup" in lower_name or "migration" in lower_name or "reorganization" in lower_name:
        return DOCS_ARCHIVE_STAGE_REPORTS_DIR / name
    return DOCS_ARCHIVE_DEPRECATED_DIR / name


def ensure_output_directories() -> None:
    """Создать директории для outputs, не считая существующие папки ошибкой."""
    for directory in OUTPUT_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


def chart_html_dir_for_name(name: str) -> Path:
    """Вернуть тематическую папку для HTML-графика по его техническому имени."""
    if name in {"monthly_placement_volume", "monthly_cumulative_placement"}:
        return CHARTS_MONTHLY_PLACEMENT_DIR
    if name == "monthly_demand_supply":
        return CHARTS_MONTHLY_DEMAND_SUPPLY_DIR
    if name in {"monthly_bid_cover", "monthly_bid_to_cover"}:
        return CHARTS_MONTHLY_BID_COVER_DIR
    if name == "monthly_weighted_avg_yield":
        return CHARTS_MONTHLY_YIELD_DIR
    if name in {"monthly_placement_by_format", "monthly_placement_by_maturity"}:
        return CHARTS_MONTHLY_STRUCTURE_DIR
    if name in {"monthly_heatmap_placement", "monthly_heatmap_revenue"}:
        return CHARTS_MONTHLY_HEATMAP_DIR
    if name in {"monthly_revenue_vs_nominal", "monthly_nominal_revenue_gap"}:
        return CHARTS_REVENUE_MONTHLY_DIR
    if name == "risk_quadrant_retrospective_outliers":
        return CHARTS_RISK_OUTLIERS_DIR
    if name == "risk_quadrant_retrospective_logx":
        return CHARTS_RISK_LOGX_DIR
    if name == "risk_quadrant_retrospective_facet":
        return CHARTS_RISK_FACET_DIR
    if name == "risk_quadrant_retrospective":
        return CHARTS_RISK_RETROSPECTIVE_DIR
    if name.startswith("risk_quadrant") or name in {"bid_to_cover", "demand_supply"}:
        return CHARTS_RISK_TARGET_PERIOD_DIR
    if name.startswith("discount_vs_demand"):
        return CHARTS_SCATTER_DISCOUNT_DEMAND_DIR
    if name == "discount_vs_revenue_gap":
        return CHARTS_SCATTER_DISCOUNT_REVENUE_GAP_DIR
    if name == "demand_cutoff_explanation":
        return CHARTS_SCATTER_DEMAND_CUTOFF_DIR
    if name in {"format_terms_scatter", "format_terms_aggregate_scatter"}:
        return CHARTS_SCATTER_FORMAT_TERMS_DIR
    if name == "yield_vs_demand":
        return CHARTS_SCATTER_YIELD_DEMAND_DIR
    if name.startswith("yield_vs_discount"):
        return CHARTS_SCATTER_YIELD_DISCOUNT_DIR
    if name == "yield_boxplot_by_ofz_type":
        return CHARTS_YIELD_BOXPLOT_DIR
    if name == "yield_boxplot_ofz_pd":
        return CHARTS_YIELD_OFZ_PD_DIR
    if name == "ofz_pd_yield_key_rate":
        return CHARTS_YIELD_OFZ_PD_DIR
    if name.startswith("yield_"):
        return CHARTS_YIELD_DIR
    if name == "sankey_target_period":
        return CHARTS_SANKEY_TARGET_PERIOD_DIR
    if name.startswith("sankey_period"):
        return CHARTS_SANKEY_PERIOD_DIR
    if name.startswith("sankey"):
        return CHARTS_SANKEY_STRUCTURE_DIR
    if name == "maturity_structure":
        return CHARTS_STRUCTURE_MATURITY_DIR
    if name in {"format_structure", "format_discount", "format_terms_comparison", "format_terms_delta_by_format"}:
        return CHARTS_STRUCTURE_FORMAT_DIR
    if name == "placement_volume":
        return CHARTS_STRUCTURE_PLACEMENT_VOLUME_DIR
    if name == "revenue_vs_nominal_by_period":
        return CHARTS_REVENUE_PERIOD_DIR
    if name in {"nominal_revenue_gap_by_period", "format_nominal_revenue_gap"}:
        return CHARTS_REVENUE_GAP_DIR
    if name == "revenue_to_nominal_ratio":
        return CHARTS_REVENUE_RATIO_DIR
    if name in {"revenue_gap_by_maturity", "revenue_gap_by_ofz_type"}:
        return CHARTS_REVENUE_BREAKDOWNS_DIR
    return CHARTS_ARCHIVE_REVIEW_REQUIRED_DIR
