"""Регрессионные тесты методологии отчетных периодов.

Скрипт не требует pytest и запускается обычным проектным Python. Он проверяет
границы `cumulative` и `point` периодов, количество ретроспективных периодов и
помесячный слой, объясняющий накопленный итог.
"""

from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Callable

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, report_params
else:
    from . import config, report_params


@dataclass(frozen=True)
class TestResult:
    """Результат одного регрессионного теста."""

    name: str
    passed: bool
    message: str


def main() -> int:
    """Запустить все регрессионные тесты и вернуть код завершения."""
    tests: list[Callable[[], None]] = [
        test_month_cumulative_period,
        test_month_point_period,
        test_quarter_cumulative_period,
        test_quarter_point_period,
        test_year_period,
        test_retrospective_period_count,
        test_monthly_layer_cumulative_months_and_april_cumulative,
        test_monthly_layer_point_april_only,
        test_drpa_excluded_from_demand_ratios,
        test_zero_placement_ratio_handling,
        test_unsatisfied_auction_ratios,
        test_zero_or_missing_yield_handling,
        test_bid_to_cover_outlier_detection,
        test_outputs_structure_contract,
    ]

    results: list[TestResult] = []
    for test in tests:
        try:
            test()
        except AssertionError as exc:
            results.append(TestResult(test.__name__, False, str(exc)))
        except Exception as exc:  # pragma: no cover - нужен явный текст для ручного запуска.
            results.append(TestResult(test.__name__, False, f"Неожиданная ошибка: {exc}"))
        else:
            results.append(TestResult(test.__name__, True, "ok"))

    for result in results:
        status = "OK" if result.passed else "FAIL"
        print(f"{status} | {result.name} | {result.message}")

    failed = [result for result in results if not result.passed]
    if failed:
        print(f"Regression tests failed: {len(failed)}")
        return 1
    print(f"Regression tests passed: {len(results)}")
    return 0


def target_period(
    report_date: date,
    period_type: str,
    aggregation_mode: str,
    retrospective_years: int = 0,
) -> dict[str, Any]:
    """Вернуть целевой период из построенного горизонта."""
    periods = report_params.build_report_periods(
        report_date=report_date,
        retrospective_years=retrospective_years,
        period_type=period_type,
        aggregation_mode=aggregation_mode,
    )
    targets = [period for period in periods if bool(period["is_target_period"])]
    assert len(targets) == 1, f"Ожидался один целевой период, получено {len(targets)}."
    return targets[0]


def assert_bounds(period: dict[str, Any], expected_start: date, expected_end: date) -> None:
    """Проверить начало и конец периода."""
    actual_start = period["period_start"]
    actual_end = period["period_end"]
    assert actual_start == expected_start, f"period_start: ожидалось {expected_start}, получено {actual_start}."
    assert actual_end == expected_end, f"period_end: ожидалось {expected_end}, получено {actual_end}."


def test_month_cumulative_period() -> None:
    period = target_period(date(2026, 5, 1), "month", "cumulative")
    assert_bounds(period, date(2026, 1, 1), date(2026, 4, 30))


def test_month_point_period() -> None:
    period = target_period(date(2026, 5, 1), "month", "point")
    assert_bounds(period, date(2026, 4, 1), date(2026, 4, 30))


def test_quarter_cumulative_period() -> None:
    period = target_period(date(2026, 7, 1), "quarter", "cumulative")
    assert_bounds(period, date(2026, 1, 1), date(2026, 6, 30))


def test_quarter_point_period() -> None:
    period = target_period(date(2026, 7, 1), "quarter", "point")
    assert_bounds(period, date(2026, 4, 1), date(2026, 6, 30))


def test_year_period() -> None:
    period = target_period(date(2026, 1, 1), "year", "cumulative")
    assert_bounds(period, date(2025, 1, 1), date(2025, 12, 31))


def test_retrospective_period_count() -> None:
    periods = report_params.build_report_periods(
        report_date=date(2026, 5, 1),
        retrospective_years=4,
        period_type="month",
        aggregation_mode="cumulative",
    )
    assert len(periods) == 5, f"retrospective_years=4 должен давать 5 периодов, получено {len(periods)}."
    assert bool(periods[-1]["is_target_period"]), "Последний период должен быть целевым."


def test_monthly_layer_cumulative_months_and_april_cumulative() -> None:
    monthly_analytics = importlib.import_module("scripts.09_monthly_analytics")
    params = report_params.ReportParams(
        report_date=date(2026, 5, 1),
        retrospective_years=0,
        period_type="month",
        aggregation_mode="cumulative",
        periods=report_params.build_report_periods(
            report_date=date(2026, 5, 1),
            retrospective_years=0,
            period_type="month",
            aggregation_mode="cumulative",
        ),
    )
    source = sample_monthly_source()

    metrics, _limitations = monthly_analytics.build_monthly_metrics(source, params)
    months = sorted(pd.to_numeric(metrics["month_number"], errors="coerce").dropna().astype(int).tolist())
    assert months == [1, 2, 3, 4], f"month cumulative должен содержать месяцы 1-4, получено {months}."
    assert 5 not in months, "Месяц 5 не должен попадать в report_date=2026-05-01."

    april = metrics.loc[pd.to_numeric(metrics["month_number"], errors="coerce") == 4]
    assert len(april) == 1, f"Ожидалась одна строка апреля, получено {len(april)}."
    monthly_sum = pd.to_numeric(metrics["total_placement_volume"], errors="coerce").sum()
    april_cumulative = float(april.iloc[0]["cumulative_placement_volume"])
    assert april_cumulative == monthly_sum, (
        "cumulative_placement_volume за апрель должен равняться сумме monthly "
        f"total_placement_volume за январь-апрель: ожидалось {monthly_sum}, получено {april_cumulative}."
    )


def test_monthly_layer_point_april_only() -> None:
    monthly_analytics = importlib.import_module("scripts.09_monthly_analytics")
    params = report_params.ReportParams(
        report_date=date(2026, 5, 1),
        retrospective_years=0,
        period_type="month",
        aggregation_mode="point",
        periods=report_params.build_report_periods(
            report_date=date(2026, 5, 1),
            retrospective_years=0,
            period_type="month",
            aggregation_mode="point",
        ),
    )
    source = sample_monthly_source()
    metrics, _limitations = monthly_analytics.build_monthly_metrics(source, params)
    months = sorted(pd.to_numeric(metrics["month_number"], errors="coerce").dropna().astype(int).tolist())
    assert months == [4], f"month point должен содержать только апрель, получено {months}."


def test_drpa_excluded_from_demand_ratios() -> None:
    monthly_analytics = importlib.import_module("scripts.09_monthly_analytics")
    rows = pd.DataFrame(
        {
            "auction_date": ["2026-04-10", "2026-04-11"],
            "placement_volume": [100.0, 50.0],
            "demand_volume": [200.0, pd.NA],
            "supply_volume": [150.0, pd.NA],
            "weighted_avg_yield": [12.0, 12.5],
            "format": ["Аукцион", "ДРПА"],
            "maturity_bucket": ["short_term", "short_term"],
            "ofz_type": ["ОФЗ-ПД", "ОФЗ-ПД"],
        }
    )
    params = report_params.ReportParams(
        report_date=date(2026, 5, 1),
        retrospective_years=0,
        period_type="month",
        aggregation_mode="point",
        periods=report_params.build_report_periods(date(2026, 5, 1), 0, "month", "point"),
    )
    metrics, _limitations = monthly_analytics.build_monthly_metrics(rows, params)
    april = metrics.iloc[0]
    assert float(april["placement_volume_drpa"]) == 50.0, "ДРПА должен попадать в объем ДРПА."
    assert float(april["total_demand"]) == 200.0, "ДРПА без спроса не должен добавлять спрос."
    assert float(april["bid_to_cover_ratio"]) == 200.0 / 150.0, "bid-to-cover должен считаться по demand/supply."


def test_zero_placement_ratio_handling() -> None:
    feature_engineering = importlib.import_module("scripts.03_feature_engineering")
    df = pd.DataFrame(
        {
            "placement_amount_mln_rub": [0.0],
            "demand_amount_mln_rub": [100.0],
            "offer_amount_mln_rub": [200.0],
        }
    )
    context = feature_engineering.FeatureContext()
    result = df.copy()
    feature_engineering.add_demand_ratios(result, context)
    assert pd.isna(result.loc[0, "demand_to_placement_ratio"]), "При нулевом размещении demand_to_placement_ratio должен быть NaN."
    assert "missing_or_zero_placement" in str(result.loc[0, "ratio_basis"]), "ratio_basis должен фиксировать нулевое размещение."


def test_unsatisfied_auction_ratios() -> None:
    feature_engineering = importlib.import_module("scripts.03_feature_engineering")
    df = pd.DataFrame(
        {
            "placement_amount_mln_rub": [80.0],
            "demand_amount_mln_rub": [200.0],
            "offer_amount_mln_rub": [100.0],
        }
    )
    context = feature_engineering.FeatureContext()
    result = df.copy()
    feature_engineering.add_demand_ratios(result, context)
    assert as_float(result.loc[0, "demand_satisfaction_ratio"]) == 0.4, "Удовлетворение спроса должно быть placement/demand."
    assert as_float(result.loc[0, "demand_to_placement_ratio"]) == 2.5, "Спрос/размещение должен быть demand/placement."
    assert as_float(result.loc[0, "bid_to_cover_ratio"]) == 2.0, "Bid-to-cover должен быть demand/supply."


def test_zero_or_missing_yield_handling() -> None:
    build_charts = importlib.import_module("scripts.06_build_charts")
    data = pd.DataFrame(
        {
            "ofz_type": ["ОФЗ-ПК", "ОФЗ-ПК"],
            "_yield": [0.0, pd.NA],
            "data_quality_flag": ["requires_review", ""],
        }
    )
    limitations: list[str] = []
    result = build_charts.mark_near_zero_floating_rate_yields(data, limitations)
    assert pd.isna(result.loc[0, "_yield"]), "Около-нулевая доходность ОФЗ-ПК с requires_review должна исключаться из boxplot."
    assert limitations, "Ограничение по zero/missing yield должно документироваться."


def test_bid_to_cover_outlier_detection() -> None:
    build_charts = importlib.import_module("scripts.06_build_charts")
    data = pd.DataFrame(
        {
            "_demand": [600.0, 100.0],
            "_supply": [100.0, 100.0],
            "_placement": [50.0, 80.0],
            "format": ["Аукцион", "Аукцион"],
            "data_quality_flag": ["ok", "ok"],
        }
    )
    limitations: list[str] = []
    eligible = build_charts.filter_bid_to_cover_rows(data, limitations)
    outliers = eligible.loc[pd.to_numeric(eligible["_bid_to_cover"], errors="coerce") > 5]
    assert len(outliers) == 1, f"Ожидался один выброс bid-to-cover > 5, получено {len(outliers)}."


def test_outputs_structure_contract() -> None:
    required_directories = [
        config.REPORTS_ANALYTICAL_TABLES_DIR,
        config.REPORTS_MONTHLY_TABLES_DIR,
        config.EXPORTS_ANALYTICAL_CSV_DIR,
        config.EXPORTS_CHART_DATA_DIR,
        config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR,
        config.EXPORTS_CHART_DATA_SANKEY_DIR,
        config.EXPORTS_CHART_DATA_BOXPLOT_DIR,
        config.EXPORTS_CHART_DATA_STRUCTURE_DIR,
        config.DASHBOARDS_DIR,
    ]
    missing = [path.relative_to(config.PROJECT_ROOT).as_posix() for path in required_directories if not path.exists()]
    assert not missing, f"Отсутствуют директории outputs: {', '.join(missing)}."

    allowed_skeleton_files = {".gitkeep", "README.md", "index.md"}
    direct_exports = (
        [
            path.name
            for path in config.EXPORTS_DIR.iterdir()
            if path.is_file() and path.name not in allowed_skeleton_files
        ]
        if config.EXPORTS_DIR.exists()
        else []
    )
    assert not direct_exports, f"Файлы не должны лежать напрямую в outputs/exports: {', '.join(direct_exports)}."


def sample_monthly_source() -> pd.DataFrame:
    """Вернуть минимальный источник для тестов monthly layer."""
    return pd.DataFrame(
        {
            "auction_date": [
                "2026-01-10",
                "2026-02-10",
                "2026-03-10",
                "2026-04-10",
                "2026-05-10",
            ],
            "placement_volume": [10.0, 20.0, 30.0, 40.0, 500.0],
            "demand_volume": [15.0, 25.0, 35.0, 45.0, 600.0],
            "supply_volume": [12.0, 22.0, 32.0, 42.0, 550.0],
            "weighted_avg_yield": [10.0, 11.0, 12.0, 13.0, 99.0],
            "format": ["Аукцион", "Аукцион", "Аукцион", "Аукцион", "Аукцион"],
            "maturity_bucket": ["short_term", "short_term", "medium_term", "long_term", "long_term"],
            "ofz_type": ["ОФЗ-ПД", "ОФЗ-ПД", "ОФЗ-ПД", "ОФЗ-ПД", "ОФЗ-ПД"],
        }
    )


def as_float(value: Any) -> float:
    """Convert pandas scalar-like values to float for assertions."""
    return float(value)


if __name__ == "__main__":
    raise SystemExit(main())
