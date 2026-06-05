"""ЭТАП 3: построение признаков для аналитики аукционов ОФЗ."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, utils
else:
    from . import config, utils


FeatureBuilder = Callable[[pd.DataFrame, "FeatureContext"], None]


@dataclass
class FeatureContext:
    added_features: list[str] = field(default_factory=list)
    skipped_features: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add(self, *features: str) -> None:
        for feature in features:
            if feature not in self.added_features:
                self.added_features.append(feature)

    def skip(self, feature_group: str, reason: str) -> None:
        self.skipped_features.append({"feature_group": feature_group, "reason": reason})

    def warn(self, message: str) -> None:
        self.warnings.append(message)


FEATURE_BUILDERS: list[tuple[str, FeatureBuilder, list[str]]] = [
    (
        "calendar_features",
        lambda df, context: add_calendar_features(df, context),
        ["auction_date"],
    ),
    (
        "volume_aliases",
        lambda df, context: add_volume_aliases(df, context),
        ["placement_amount_mln_rub", "demand_amount_mln_rub", "offer_amount_mln_rub"],
    ),
    (
        "weighted_avg_yield",
        lambda df, context: add_weighted_avg_yield(df, context),
        ["weighted_avg_yield_pct"],
    ),
    (
        "price_and_cutoff_aliases",
        lambda df, context: add_price_and_cutoff_aliases(df, context),
        ["cutoff_price_pct", "weighted_avg_price_pct", "cutoff_yield_pct"],
    ),
    (
        "demand_ratios",
        lambda df, context: add_demand_ratios(df, context),
        ["demand_amount_mln_rub", "placement_amount_mln_rub", "offer_amount_mln_rub"],
    ),
    (
        "offer_ratios",
        lambda df, context: add_offer_ratios(df, context),
        ["offer_amount_mln_rub", "placement_amount_mln_rub", "demand_amount_mln_rub"],
    ),
    (
        "maturity_bucket",
        lambda df, context: add_maturity_features(df, context),
        ["days_to_maturity"],
    ),
    (
        "ofz_type",
        lambda df, context: add_ofz_type(df, context),
        ["security_type"],
    ),
    (
        "yield_yoy_change",
        lambda df, context: add_yield_yoy_change(df, context),
        ["issue_code", "auction_year", "weighted_avg_yield"],
    ),
    (
        "pressure_indicators",
        lambda df, context: add_pressure_indicators(df, context),
        ["bid_to_cover_ratio", "weighted_avg_yield", "auction_year"],
    ),
    (
        "auction_efficiency_score",
        lambda df, context: add_auction_efficiency_score(df, context),
        ["placement_to_offer_ratio", "demand_to_offer_ratio", "weighted_avg_yield"],
    ),
    (
        "concentration_indicators",
        lambda df, context: add_concentration_indicators(df, context),
        ["auction_year", "issue_code", "placement_amount_mln_rub", "demand_amount_mln_rub"],
    ),
    (
        "volatility_indicators",
        lambda df, context: add_volatility_indicators(df, context),
        ["auction_year", "issue_code", "weighted_avg_yield"],
    ),
    (
        "deviation_from_average",
        lambda df, context: add_deviation_from_average(df, context),
        ["auction_year", "placement_amount_mln_rub", "demand_amount_mln_rub", "weighted_avg_yield"],
    ),
]


def main() -> None:
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    logger.info("Старт этапа 3: построение признаков")

    if not config.OFZ_AUCTIONS_CLEAN_CSV.exists():
        raise FileNotFoundError(f"Clean dataset не найден: {config.OFZ_AUCTIONS_CLEAN_CSV}")

    clean = pd.read_csv(config.OFZ_AUCTIONS_CLEAN_CSV)
    context = FeatureContext()
    features = build_features(clean, context, logger)

    config.DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    features.to_csv(config.OFZ_AUCTIONS_FEATURES_CSV, index=False, encoding="utf-8")

    report = build_report(clean, features, context)
    utils.write_markdown(config.FEATURE_ENGINEERING_DOC, report)

    logger.info("Features dataset записан: %s", config.OFZ_AUCTIONS_FEATURES_CSV)
    logger.info("Отчет построения признаков записан: %s", config.FEATURE_ENGINEERING_DOC)
    logger.info("Этап 3 завершен")


def build_features(clean: pd.DataFrame, context: FeatureContext, logger: Any) -> pd.DataFrame:
    df = clean.copy()
    normalize_base_types(df)

    for feature_group, builder, required_columns in FEATURE_BUILDERS:
        missing = [column for column in required_columns if column not in df.columns]
        if missing:
            reason = f"Отсутствуют колонки: {', '.join(missing)}"
            context.skip(feature_group, reason)
            logger.warning("Пропущен блок признаков %s: %s", feature_group, reason)
            continue

        try:
            builder(df, context)
        except Exception as exc:
            reason = f"{type(exc).__name__}: {exc}"
            context.skip(feature_group, reason)
            logger.warning("Блок признаков требует проверки %s: %s", feature_group, reason)

    df["feature_processing_timestamp"] = datetime.now().isoformat(timespec="seconds")
    context.add("feature_processing_timestamp")
    return df


def normalize_base_types(df: pd.DataFrame) -> None:
    for column in ["auction_date", "maturity_date"]:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    numeric_columns = [
        "source_year",
        "quarter",
        "days_to_maturity",
        "offer_amount_mln_rub",
        "cutoff_price_pct",
        "weighted_avg_price_pct",
        "cutoff_yield_pct",
        "weighted_avg_yield_pct",
        "demand_amount_mln_rub",
        "placement_amount_mln_rub",
        "proceeds_mln_rub",
        "demand_satisfaction_ratio",
    ]
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")


def add_calendar_features(df: pd.DataFrame, context: FeatureContext) -> None:
    df["auction_year"] = df["auction_date"].dt.year.astype("Int64")
    df["auction_quarter"] = df["auction_date"].dt.quarter.astype("Int64")
    df["auction_month"] = df["auction_date"].dt.month.astype("Int64")
    df["is_q1"] = df["auction_quarter"] == 1
    context.add("auction_year", "auction_quarter", "auction_month", "is_q1")


def add_volume_aliases(df: pd.DataFrame, context: FeatureContext) -> None:
    df["placement_volume"] = df["placement_amount_mln_rub"]
    df["demand_volume"] = df["demand_amount_mln_rub"]
    df["supply_volume"] = df["offer_amount_mln_rub"]
    context.add("placement_volume", "demand_volume", "supply_volume")


def add_weighted_avg_yield(df: pd.DataFrame, context: FeatureContext) -> None:
    df["weighted_avg_yield"] = df["weighted_avg_yield_pct"]
    df["yield"] = df["weighted_avg_yield"]
    context.add("weighted_avg_yield", "yield")


def add_price_and_cutoff_aliases(df: pd.DataFrame, context: FeatureContext) -> None:
    df["cutoff_price"] = df["cutoff_price_pct"]
    df["weighted_avg_price"] = df["weighted_avg_price_pct"]
    df["cutoff_yield"] = df["cutoff_yield_pct"]
    df["discount_to_nominal"] = 100 - df["cutoff_price"]
    df["cutoff_yield_spread"] = df["cutoff_yield"] - df["weighted_avg_yield"]
    context.add(
        "cutoff_price",
        "weighted_avg_price",
        "cutoff_yield",
        "discount_to_nominal",
        "cutoff_yield_spread",
    )


def add_demand_ratios(df: pd.DataFrame, context: FeatureContext) -> None:
    df["bid_to_cover_ratio"] = safe_divide(df["demand_amount_mln_rub"], df["offer_amount_mln_rub"])
    df["demand_to_placement_ratio"] = safe_divide(
        df["demand_amount_mln_rub"],
        df["placement_amount_mln_rub"],
    )

    if "demand_satisfaction_ratio" in df.columns:
        source_ratio = pd.to_numeric(df["demand_satisfaction_ratio"], errors="coerce")
    else:
        source_ratio = pd.Series(np.nan, index=df.index, dtype="float64")
    calculated_satisfaction = safe_divide(
        df["placement_amount_mln_rub"],
        df["demand_amount_mln_rub"],
    )
    df["demand_satisfaction_ratio"] = source_ratio.combine_first(calculated_satisfaction)

    ratio_basis = pd.Series(
        "bid_to_cover=demand/supply; demand_to_placement=demand/placement",
        index=df.index,
        dtype="string",
    )
    ratio_basis = append_ratio_basis(
        ratio_basis,
        df["offer_amount_mln_rub"].isna() | (df["offer_amount_mln_rub"] <= 0),
        "; missing_or_zero_supply",
    )
    ratio_basis = append_ratio_basis(
        ratio_basis,
        df["placement_amount_mln_rub"].isna() | (df["placement_amount_mln_rub"] <= 0),
        "; missing_or_zero_placement",
    )
    ratio_basis = append_ratio_basis(
        ratio_basis,
        df["demand_amount_mln_rub"].isna() | (df["demand_amount_mln_rub"] <= 0),
        "; missing_or_zero_demand",
    )
    ratio_basis = append_ratio_basis(
        ratio_basis,
        source_ratio.notna(),
        "; demand_satisfaction=source",
    )
    ratio_basis = append_ratio_basis(
        ratio_basis,
        source_ratio.isna() & calculated_satisfaction.notna(),
        "; demand_satisfaction=placement/demand",
    )
    df["ratio_basis"] = ratio_basis
    context.add(
        "bid_to_cover_ratio",
        "demand_to_placement_ratio",
        "demand_satisfaction_ratio",
        "ratio_basis",
    )


def append_ratio_basis(
    basis: pd.Series,
    mask: pd.Series,
    note: str,
) -> pd.Series:
    result = basis.copy()
    normalized_mask = mask.fillna(False).astype(bool)
    selected = result.loc[normalized_mask].astype("string")
    result.loc[normalized_mask] = selected.map(lambda value: f"{value}{note}")
    return result


def add_offer_ratios(df: pd.DataFrame, context: FeatureContext) -> None:
    df["placement_to_offer_ratio"] = safe_divide(
        df["placement_amount_mln_rub"],
        df["offer_amount_mln_rub"],
    )
    df["demand_to_offer_ratio"] = safe_divide(
        df["demand_amount_mln_rub"],
        df["offer_amount_mln_rub"],
    )
    context.add("placement_to_offer_ratio", "demand_to_offer_ratio")


def add_maturity_features(df: pd.DataFrame, context: FeatureContext) -> None:
    df["maturity_years"] = df["days_to_maturity"] / 365.25
    df["maturity_bucket"] = classify_maturity_bucket(df)
    df["maturity_bucket_label"] = df["maturity_bucket"].map(
        {
            "short_term": "Краткосрочные (до 5 лет включительно)",
            "medium_term": "Среднесрочные (свыше 5 до 10 лет включительно)",
            "long_term": "Долгосрочные (свыше 10 лет)",
            "requires_review": "Требует проверки",
        }
    ).astype("string")
    context.add("maturity_years", "maturity_bucket", "maturity_bucket_label")


def classify_maturity_bucket(df: pd.DataFrame) -> pd.Series:
    result = pd.Series("requires_review", index=df.index, dtype="object")
    if {"auction_date", "maturity_date"}.issubset(df.columns):
        years = calendar_maturity_years(df["auction_date"], df["maturity_date"])
    else:
        years = pd.to_numeric(df["maturity_years"], errors="coerce")

    result.loc[years.notna() & (years <= 5)] = "short_term"
    result.loc[years.notna() & (years > 5) & (years <= 10)] = "medium_term"
    result.loc[years.notna() & (years > 10)] = "long_term"
    return result.astype("string")


def calendar_maturity_years(auction_date: pd.Series, maturity_date: pd.Series) -> pd.Series:
    auction = pd.to_datetime(auction_date, errors="coerce")
    maturity = pd.to_datetime(maturity_date, errors="coerce")
    result = pd.Series(pd.NA, index=auction.index, dtype="Float64")
    valid = auction.notna() & maturity.notna()
    full_years = maturity.dt.year - auction.dt.year
    before_anniversary = (
        (maturity.dt.month < auction.dt.month)
        | ((maturity.dt.month == auction.dt.month) & (maturity.dt.day < auction.dt.day))
    )
    full_years = full_years.where(~before_anniversary, full_years - 1)
    result.loc[valid] = full_years.loc[valid].astype("Float64")
    return result


def add_ofz_type(df: pd.DataFrame, context: FeatureContext) -> None:
    df["ofz_type"] = df["security_type"].astype("string")
    context.add("ofz_type")


def add_yield_yoy_change(df: pd.DataFrame, context: FeatureContext) -> None:
    yearly_issue_yield = (
        df.groupby(["issue_code", "auction_year"], dropna=False)["weighted_avg_yield"]
        .mean()
        .rename("issue_year_weighted_avg_yield")
        .reset_index()
        .sort_values(["issue_code", "auction_year"])
    )
    yearly_issue_yield["previous_year_yield"] = yearly_issue_yield.groupby("issue_code")[
        "issue_year_weighted_avg_yield"
    ].shift(1)
    yearly_issue_yield["yield_yoy_change"] = (
        yearly_issue_yield["issue_year_weighted_avg_yield"]
        - yearly_issue_yield["previous_year_yield"]
    )

    df.merge(
        yearly_issue_yield[
            [
                "issue_code",
                "auction_year",
                "issue_year_weighted_avg_yield",
                "yield_yoy_change",
            ]
        ],
        on=["issue_code", "auction_year"],
        how="left",
    )
    merged = df.merge(
        yearly_issue_yield[
            [
                "issue_code",
                "auction_year",
                "issue_year_weighted_avg_yield",
                "yield_yoy_change",
            ]
        ],
        on=["issue_code", "auction_year"],
        how="left",
    )
    df["issue_year_weighted_avg_yield"] = merged["issue_year_weighted_avg_yield"].to_numpy()
    df["yield_yoy_change"] = merged["yield_yoy_change"].to_numpy()
    context.add("issue_year_weighted_avg_yield", "yield_yoy_change")


def add_pressure_indicators(df: pd.DataFrame, context: FeatureContext) -> None:
    df["demand_pressure_indicator"] = pd.Series("not_applicable", index=df.index, dtype="object")
    df.loc[df["bid_to_cover_ratio"] < 1, "demand_pressure_indicator"] = "weak"
    df.loc[
        df["bid_to_cover_ratio"].between(1, 2, inclusive="left"),
        "demand_pressure_indicator",
    ] = "moderate"
    df.loc[df["bid_to_cover_ratio"] >= 2, "demand_pressure_indicator"] = "high"
    df.loc[df["bid_to_cover_ratio"].isna(), "demand_pressure_indicator"] = "not_applicable"

    year_mean = df.groupby("auction_year")["weighted_avg_yield"].transform("mean")
    year_std = df.groupby("auction_year")["weighted_avg_yield"].transform("std")
    df["yield_zscore_in_year"] = safe_divide(df["weighted_avg_yield"] - year_mean, year_std)
    df["yield_pressure_indicator"] = "normal"
    df.loc[df["yield_zscore_in_year"] > 1, "yield_pressure_indicator"] = "high"
    df.loc[df["yield_zscore_in_year"] < -1, "yield_pressure_indicator"] = "low"
    df.loc[df["yield_zscore_in_year"].isna(), "yield_pressure_indicator"] = "not_applicable"

    context.add(
        "demand_pressure_indicator",
        "yield_zscore_in_year",
        "yield_pressure_indicator",
    )


def add_auction_efficiency_score(df: pd.DataFrame, context: FeatureContext) -> None:
    placement_component = df["placement_to_offer_ratio"].clip(lower=0, upper=1)
    demand_component = df["demand_to_offer_ratio"].clip(lower=0, upper=2) / 2
    yield_component = 1 - percentile_rank(df["weighted_avg_yield"])
    df["auction_efficiency_score"] = (
        placement_component * 0.45 + demand_component * 0.35 + yield_component * 0.20
    )
    context.add("auction_efficiency_score")


def add_concentration_indicators(df: pd.DataFrame, context: FeatureContext) -> None:
    issue_year = (
        df.groupby(["auction_year", "issue_code"], dropna=False)
        .agg(
            issue_year_placement_mln_rub=("placement_amount_mln_rub", "sum"),
            issue_year_demand_mln_rub=("demand_amount_mln_rub", "sum"),
        )
        .reset_index()
    )
    issue_year["year_total_placement_mln_rub"] = issue_year.groupby("auction_year")[
        "issue_year_placement_mln_rub"
    ].transform("sum")
    issue_year["year_total_demand_mln_rub"] = issue_year.groupby("auction_year")[
        "issue_year_demand_mln_rub"
    ].transform("sum")
    issue_year["issue_placement_share_in_year"] = safe_divide(
        issue_year["issue_year_placement_mln_rub"],
        issue_year["year_total_placement_mln_rub"],
    )
    issue_year["issue_demand_share_in_year"] = safe_divide(
        issue_year["issue_year_demand_mln_rub"],
        issue_year["year_total_demand_mln_rub"],
    )
    issue_year["year_placement_hhi_by_issue"] = issue_year.groupby("auction_year")[
        "issue_placement_share_in_year"
    ].transform(lambda values: float((values.fillna(0) ** 2).sum()))
    issue_year["year_demand_hhi_by_issue"] = issue_year.groupby("auction_year")[
        "issue_demand_share_in_year"
    ].transform(lambda values: float((values.fillna(0) ** 2).sum()))

    columns = [
        "auction_year",
        "issue_code",
        "issue_year_placement_mln_rub",
        "issue_year_demand_mln_rub",
        "year_total_placement_mln_rub",
        "year_total_demand_mln_rub",
        "issue_placement_share_in_year",
        "issue_demand_share_in_year",
        "year_placement_hhi_by_issue",
        "year_demand_hhi_by_issue",
    ]
    merged = df.merge(issue_year[columns], on=["auction_year", "issue_code"], how="left")
    for column in columns[2:]:
        df[column] = merged[column].to_numpy()
    context.add(*columns[2:])


def add_volatility_indicators(df: pd.DataFrame, context: FeatureContext) -> None:
    df["year_yield_volatility_std"] = df.groupby("auction_year")["weighted_avg_yield"].transform(
        "std"
    )
    df["issue_yield_volatility_std"] = df.groupby("issue_code")["weighted_avg_yield"].transform(
        "std"
    )
    context.add("year_yield_volatility_std", "issue_yield_volatility_std")


def add_deviation_from_average(df: pd.DataFrame, context: FeatureContext) -> None:
    year_avg_placement = df.groupby("auction_year")["placement_amount_mln_rub"].transform("mean")
    year_avg_demand = df.groupby("auction_year")["demand_amount_mln_rub"].transform("mean")
    year_avg_yield = df.groupby("auction_year")["weighted_avg_yield"].transform("mean")

    df["placement_deviation_from_average"] = df["placement_amount_mln_rub"] - year_avg_placement
    df["demand_deviation_from_average"] = df["demand_amount_mln_rub"] - year_avg_demand
    df["yield_deviation_from_average"] = df["weighted_avg_yield"] - year_avg_yield
    context.add(
        "placement_deviation_from_average",
        "demand_deviation_from_average",
        "yield_deviation_from_average",
    )


def safe_divide(numerator: Any, denominator: Any) -> pd.Series:
    numerator_series = pd.Series(numerator)
    denominator_series = pd.Series(denominator).replace({0: np.nan})
    return numerator_series / denominator_series


def percentile_rank(series: pd.Series) -> pd.Series:
    return series.rank(pct=True)


def build_report(clean: pd.DataFrame, features: pd.DataFrame, context: FeatureContext) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    added_columns = [column for column in features.columns if column not in clean.columns]

    lines: list[str] = [
        "# Отчет построения признаков",
        "",
        f"Дата формирования: {now}",
        "",
        "## Краткий вывод",
        "",
        f"Источник: `{config.OFZ_AUCTIONS_CLEAN_CSV.relative_to(config.ROOT_DIR).as_posix()}`.",
        f"Строк во входном dataset: {len(clean)}.",
        f"Строк в features dataset: {len(features)}.",
        f"Колонок во входном dataset: {len(clean.columns)}.",
        f"Колонок в features dataset: {len(features.columns)}.",
        f"Добавлено признаков: {len(added_columns)}.",
        "",
    ]

    append_added_features_section(lines, added_columns, features)
    append_skipped_section(lines, context)
    append_required_features_section(lines, features)
    append_quality_section(lines, features)
    append_outputs_section(lines)
    return "\n".join(lines)


def append_added_features_section(
    lines: list[str],
    added_columns: list[str],
    features: pd.DataFrame,
) -> None:
    lines.extend(["## Добавленные признаки", "", "| Признак | Пропусков |", "|---|---:|"])
    for column in added_columns:
        lines.append(f"| `{column}` | {int(features[column].isna().sum())} |")
    lines.append("")


def append_skipped_section(lines: list[str], context: FeatureContext) -> None:
    lines.extend(["## Пропущено / requires_review", ""])
    if not context.skipped_features and not context.warnings:
        lines.append("Пропущенных блоков признаков нет.")
        lines.append("")
        return

    if context.skipped_features:
        lines.extend(["| Блок признаков | Причина |", "|---|---|"])
        for item in context.skipped_features:
            lines.append(f"| `{item['feature_group']}` | {item['reason']} |")
        lines.append("")

    if context.warnings:
        lines.append("### Предупреждения")
        lines.append("")
        for message in context.warnings:
            lines.append(f"- {message}")
        lines.append("")


def append_required_features_section(lines: list[str], features: pd.DataFrame) -> None:
    required_features = [
        ("bid_to_cover_ratio", "bid-to-cover для аналитики спроса"),
        ("demand_to_placement_ratio", "отношение спроса к размещению"),
        ("demand_satisfaction_ratio", "коэффициент удовлетворения спроса"),
        ("ratio_basis", "методическая база расчета ratio-показателей"),
        ("cutoff_price", "цена отсечения"),
        ("weighted_avg_price", "средневзвешенная цена"),
        ("cutoff_yield", "доходность по цене отсечения"),
        ("discount_to_nominal", "дисконт к номиналу"),
        ("cutoff_yield_spread", "спред доходности отсечения к средневзвешенной доходности"),
        ("placement_volume", "объем размещения"),
        ("demand_volume", "объем спроса"),
        ("supply_volume", "объем предложения"),
        ("yield", "основной alias доходности для табличных отчетов"),
        ("weighted_avg_yield", "средневзвешенная доходность"),
        ("maturity_years", "срок обращения в годах"),
        ("maturity_bucket", "категория срока обращения"),
        ("maturity_bucket_label", "человекочитаемая категория срока обращения"),
        ("ofz_type", "тип ОФЗ"),
        ("auction_year", "год аукциона"),
        ("auction_quarter", "квартал аукциона"),
        ("auction_month", "месяц аукциона"),
        ("demand_pressure_indicator", "индикатор давления спроса"),
        ("yield_pressure_indicator", "индикатор давления доходности"),
        ("auction_efficiency_score", "интегральный показатель эффективности аукциона"),
    ]

    lines.extend(
        [
            "## Проверка обязательных признаков",
            "",
            "| Признак | Статус | Пропусков | Назначение |",
            "|---|---|---:|---|",
        ]
    )
    for feature, purpose in required_features:
        if feature in features.columns:
            status = "ok"
            missing = int(features[feature].isna().sum())
        else:
            status = "missing"
            missing = len(features)
        lines.append(f"| `{feature}` | {status} | {missing} | {purpose} |")
    lines.append("")

    lines.extend(
        [
            "## Правило классификации сроков обращения",
            "",
            "- `short_term`: краткосрочные ОФЗ, срок обращения до 5 лет.",
            "- `medium_term`: среднесрочные ОФЗ, срок обращения от 5 до 10 лет включительно.",
            "- `long_term`: долгосрочные ОФЗ, срок обращения свыше 10 лет.",
            "- `requires_review`: срок обращения невозможно надежно определить.",
            "- `maturity_years` рассчитывается по `days_to_maturity / 365.25`; пограничная классификация bucket при наличии дат уточняется календарной логикой.",
            "",
            "## Методика ratio-показателей",
            "",
            "- `bid_to_cover_ratio`: спрос / предложение. Это показатель покрытия предложенного объема спросом.",
            "- `demand_to_placement_ratio`: спрос / фактическое размещение. Этот показатель не называется bid-to-cover.",
            "- `demand_satisfaction_ratio`: исходный коэффициент удовлетворения спроса, если он есть; иначе размещение / спрос.",
            "- При нулевом или отсутствующем размещении `demand_to_placement_ratio` остается пустым, а `ratio_basis` фиксирует `missing_or_zero_placement`.",
            "",
        ]
    )


def append_quality_section(lines: list[str], features: pd.DataFrame) -> None:
    lines.extend(["## Контроль качества", ""])
    lines.append(f"- Полных дубликатов: {int(features.duplicated().sum())}.")

    if "auction_year" in features.columns:
        years = sorted(str(year) for year in features["auction_year"].dropna().unique())
        lines.append(f"- Годы: {', '.join(years) if years else '-'}.")

    if "maturity_bucket" in features.columns:
        lines.append("- Распределение `maturity_bucket`:")
        for value, count in features["maturity_bucket"].value_counts(dropna=False).items():
            lines.append(f"  - `{value}`: {count}")

    if "maturity_bucket_label" in features.columns:
        lines.append("- Распределение `maturity_bucket_label`:")
        for value, count in features["maturity_bucket_label"].value_counts(dropna=False).items():
            lines.append(f"  - `{value}`: {count}")

    if "demand_pressure_indicator" in features.columns:
        lines.append("- Распределение `demand_pressure_indicator`:")
        for value, count in features["demand_pressure_indicator"].value_counts(dropna=False).items():
            lines.append(f"  - `{value}`: {count}")

    if "yield_pressure_indicator" in features.columns:
        lines.append("- Распределение `yield_pressure_indicator`:")
        for value, count in features["yield_pressure_indicator"].value_counts(dropna=False).items():
            lines.append(f"  - `{value}`: {count}")
    lines.append("")


def append_outputs_section(lines: list[str]) -> None:
    lines.extend(
        [
            "## Выходные артефакты",
            "",
            f"- `{config.OFZ_AUCTIONS_FEATURES_CSV.relative_to(config.ROOT_DIR).as_posix()}`",
            f"- `{config.FEATURE_ENGINEERING_DOC.relative_to(config.ROOT_DIR).as_posix()}`",
            f"- `{config.PIPELINE_LOG_PATH.relative_to(config.ROOT_DIR).as_posix()}`",
            "",
        ]
    )


if __name__ == "__main__":
    main()
