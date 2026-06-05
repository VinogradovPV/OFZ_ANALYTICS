"""Проверка схемы report scope и monthly layer для параметризуемой отчетности."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Callable, Sequence

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, report_params
else:
    from . import config, report_params


ALLOWED_AGGREGATION_MODES = {"cumulative", "point"}
MONTHLY_METRICS_CSV = config.PROCESSED_DATA_DIR / "ofz_monthly_metrics.csv"


@dataclass(frozen=True)
class ValidationResult:
    """Результат одной проверки схемы."""

    name: str
    passed: bool
    message: str


def main(argv: Sequence[str] | None = None) -> int:
    """Запустить проверки схемы для report scope и monthly layer."""
    params = report_params.parse_report_args(argv)
    results: list[ValidationResult] = []

    scope = filter_report_scope_by_params(read_csv_if_exists(config.OFZ_AUCTIONS_REPORT_SCOPE_CSV), params)
    monthly = read_csv_if_exists(MONTHLY_METRICS_CSV)

    checks: list[tuple[str, Callable[[], None]]] = [
        ("report_scope_exists", lambda: validate_report_scope_exists(scope)),
        ("report_scope_columns", lambda: validate_report_scope_columns(scope)),
        ("aggregation_mode_values", lambda: validate_aggregation_mode_values(scope)),
        ("report_period_dates_filled", lambda: validate_report_period_dates_filled(scope)),
        ("period_interval_rules", lambda: validate_period_interval_rules(scope, params)),
        ("period_count", lambda: validate_period_count(scope, params)),
        ("single_target_period", lambda: validate_single_target_period(scope)),
        ("monthly_layer_exists", lambda: validate_monthly_layer_exists(monthly)),
        ("monthly_layer_schema", lambda: validate_monthly_layer_schema(monthly)),
        ("monthly_target_months", lambda: validate_monthly_target_months(monthly, params)),
        ("monthly_cumulative_vs_monthly", lambda: validate_monthly_cumulative_vs_monthly(monthly)),
        ("monthly_cumulative_monotonic", lambda: validate_monthly_cumulative_monotonic(monthly)),
        ("outputs_structure", validate_outputs_structure),
        ("no_direct_outputs_exports", validate_no_direct_outputs_exports),
        ("chart_data_exports", lambda: validate_chart_data_exports(params)),
        ("volume_bln_units", lambda: validate_volume_bln_units(params)),
    ]

    for name, check in checks:
        try:
            check()
        except AssertionError as exc:
            results.append(ValidationResult(name, False, str(exc)))
        except Exception as exc:  # pragma: no cover - нужен диагностический текст для ручного запуска.
            results.append(ValidationResult(name, False, f"Неожиданная ошибка: {exc}"))
        else:
            results.append(ValidationResult(name, True, "ok"))

    for result in results:
        status = "OK" if result.passed else "FAIL"
        print(f"{status} | {result.name} | {result.message}")

    failed = [result for result in results if not result.passed]
    if failed:
        print(f"Schema validation failed: {len(failed)}")
        return 1
    print(f"Schema validation passed: {len(results)}")
    return 0


def read_csv_if_exists(path: Path) -> pd.DataFrame | None:
    """Прочитать CSV, если он существует."""
    if not path.exists():
        return None
    return pd.read_csv(path)


def filter_report_scope_by_params(
    scope: pd.DataFrame | None,
    params: report_params.ReportParams,
) -> pd.DataFrame | None:
    """Оставить в report scope только строки текущего отчетного горизонта."""
    if scope is None:
        return None
    required = {"report_period_label", "report_period_type", "aggregation_mode"}
    if not required.issubset(scope.columns):
        return scope
    labels = {str(period["report_period_label"]) for period in params.periods}
    mask = (
        scope["report_period_label"].astype("string").isin(labels)
        & (scope["report_period_type"].astype("string") == params.period_type)
        & (scope["aggregation_mode"].astype("string") == params.aggregation_mode)
    )
    return scope.loc[mask].copy()


def validate_report_scope_exists(scope: pd.DataFrame | None) -> None:
    assert scope is not None, f"Не найден report scope: {config.OFZ_AUCTIONS_REPORT_SCOPE_CSV}."


def validate_report_scope_columns(scope: pd.DataFrame | None) -> None:
    df = require_dataframe(scope, "report scope")
    required = {
        "aggregation_mode",
        "report_period_start",
        "report_period_end",
        "report_period_label",
        "report_period_type",
        "is_target_period",
    }
    missing = required.difference(df.columns)
    assert not missing, f"В report scope отсутствуют колонки: {', '.join(sorted(missing))}."


def validate_aggregation_mode_values(scope: pd.DataFrame | None) -> None:
    df = require_dataframe(scope, "report scope")
    values = set(df["aggregation_mode"].dropna().astype(str).str.lower())
    invalid = values.difference(ALLOWED_AGGREGATION_MODES)
    assert not invalid, f"`aggregation_mode` содержит недопустимые значения: {', '.join(sorted(invalid))}."


def validate_report_period_dates_filled(scope: pd.DataFrame | None) -> None:
    df = require_dataframe(scope, "report scope")
    for column in ["report_period_start", "report_period_end"]:
        missing_count = int(df[column].isna().sum())
        empty_count = int((df[column].astype("string").str.len() == 0).sum())
        assert missing_count == 0 and empty_count == 0, f"`{column}` содержит пустые значения."
        parsed = pd.to_datetime(df[column], errors="coerce")
        invalid_count = int(parsed.isna().sum())
        assert invalid_count == 0, f"`{column}` содержит нераспознанные даты: {invalid_count}."


def validate_period_interval_rules(
    scope: pd.DataFrame | None,
    params: report_params.ReportParams,
) -> None:
    df = unique_period_rows(require_dataframe(scope, "report scope"))
    starts = pd.to_datetime(df["report_period_start"], errors="coerce")
    ends = pd.to_datetime(df["report_period_end"], errors="coerce")

    if params.period_type == "month" and params.aggregation_mode == "cumulative":
        invalid = df.loc[starts.dt.month.ne(1) | starts.dt.day.ne(1)]
        assert invalid.empty, "Для month+cumulative все периоды должны начинаться 1 января."

    if params.period_type == "quarter" and params.aggregation_mode == "cumulative":
        invalid = df.loc[starts.dt.month.ne(1) | starts.dt.day.ne(1)]
        assert invalid.empty, "Для quarter+cumulative все периоды должны начинаться 1 января."

    if params.period_type == "month" and params.aggregation_mode == "point":
        invalid = df.loc[(starts.dt.year != ends.dt.year) | (starts.dt.month != ends.dt.month) | starts.dt.day.ne(1)]
        assert invalid.empty, "Для month+point каждый период должен охватывать ровно один месяц."

    if params.period_type == "quarter" and params.aggregation_mode == "point":
        invalid_rows: list[str] = []
        for _, row in df.iterrows():
            start = pd.Timestamp(row["report_period_start"]).date()
            end = pd.Timestamp(row["report_period_end"]).date()
            if not is_one_quarter(start, end):
                invalid_rows.append(str(row["report_period_label"]))
        assert not invalid_rows, f"Для quarter+point найдены периоды не на один квартал: {', '.join(invalid_rows)}."


def validate_period_count(
    scope: pd.DataFrame | None,
    params: report_params.ReportParams,
) -> None:
    df = unique_period_rows(require_dataframe(scope, "report scope"))
    actual = int(len(df))
    expected = params.retrospective_years + 1
    expected_labels = [str(period["report_period_label"]) for period in params.periods]
    actual_labels = set(df["report_period_label"].dropna().astype(str))
    missing_labels = [label for label in expected_labels if label not in actual_labels]
    detail = f" Отсутствующие периоды: {', '.join(missing_labels)}." if missing_labels else ""
    assert actual == expected, (
        f"Количество периодов должно быть {expected}, получено {actual}.{detail} "
        "Вероятно, `data/processed/ofz_auctions_report_scope.csv` сформирован для другого "
        "`retrospective_years`; перезапустите `scripts/period_filter.py` с текущими параметрами."
    )


def validate_single_target_period(scope: pd.DataFrame | None) -> None:
    df = require_dataframe(scope, "report scope")
    targets = df.loc[to_bool(df["is_target_period"])]
    target_periods = set(targets["report_period_label"].dropna().astype(str))
    assert len(target_periods) == 1, f"Должен быть ровно один целевой период, получено {len(target_periods)}."


def validate_monthly_layer_exists(monthly: pd.DataFrame | None) -> None:
    assert monthly is not None, f"Не найден monthly layer: {MONTHLY_METRICS_CSV}."


def validate_monthly_layer_schema(monthly: pd.DataFrame | None) -> None:
    df = require_dataframe(monthly, "monthly layer")
    required = {
        "report_year",
        "month_number",
        "report_period_label",
        "aggregation_mode",
        "total_placement_volume",
        "cumulative_placement_volume",
    }
    missing = required.difference(df.columns)
    assert not missing, f"В monthly layer отсутствуют колонки: {', '.join(sorted(missing))}."

    month_number = pd.to_numeric(df["month_number"], errors="coerce")
    invalid = df.loc[month_number.isna() | month_number.lt(1) | month_number.gt(12)]
    assert invalid.empty, "`month_number` должен быть в диапазоне 1-12."


def validate_monthly_target_months(
    monthly: pd.DataFrame | None,
    params: report_params.ReportParams,
) -> None:
    df = filter_monthly_by_params(require_dataframe(monthly, "monthly layer"), params)
    if not (params.period_type == "month" and params.aggregation_mode == "cumulative" and params.report_date == date(2026, 5, 1)):
        return

    target_year = params.report_date.year
    target = df.loc[pd.to_numeric(df["report_year"], errors="coerce") == target_year]
    months = set(pd.to_numeric(target["month_number"], errors="coerce").dropna().astype(int).tolist())
    forbidden = sorted(month for month in months if month >= 5)
    assert not forbidden, f"Для month+cumulative+2026-05-01 в целевом году не должно быть месяцев 5+, найдено: {forbidden}."


def validate_monthly_cumulative_vs_monthly(monthly: pd.DataFrame | None) -> None:
    df = require_dataframe(monthly, "monthly layer")
    monthly_value = pd.to_numeric(df["total_placement_volume"], errors="coerce").fillna(0)
    cumulative_value = pd.to_numeric(df["cumulative_placement_volume"], errors="coerce").fillna(0)
    invalid = df.loc[cumulative_value < monthly_value]
    assert invalid.empty, "`cumulative_placement_volume` не должен быть меньше месячного `total_placement_volume`."


def validate_monthly_cumulative_monotonic(monthly: pd.DataFrame | None) -> None:
    df = require_dataframe(monthly, "monthly layer").copy()
    df["month_number_numeric"] = pd.to_numeric(df["month_number"], errors="coerce")
    df["placement_numeric"] = pd.to_numeric(df["total_placement_volume"], errors="coerce").fillna(0)
    df["cumulative_numeric"] = pd.to_numeric(df["cumulative_placement_volume"], errors="coerce")
    group_columns = ["report_period_label", "report_year", "aggregation_mode"]

    invalid_groups: list[str] = []
    for keys, part in df.sort_values("month_number_numeric").groupby(group_columns, dropna=False):
        if (part["placement_numeric"] < 0).any():
            continue
        cumulative = part["cumulative_numeric"].dropna()
        if cumulative.empty:
            continue
        if (cumulative.diff().dropna() < 0).any():
            invalid_groups.append(" / ".join(str(item) for item in keys))
    assert not invalid_groups, (
        "`cumulative_placement_volume` должен монотонно не убывать внутри каждого года "
        f"при неотрицательном размещении. Нарушения: {', '.join(invalid_groups)}."
    )


def validate_outputs_structure() -> None:
    """Проверить наличие новой структуры outputs."""
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
    assert not missing, f"Отсутствуют директории новой структуры outputs: {', '.join(missing)}."


def validate_no_direct_outputs_exports() -> None:
    """Проверить, что файлы не сохраняются напрямую в корень outputs/exports."""
    if not config.EXPORTS_DIR.exists():
        return
    direct_files = sorted(path.name for path in config.EXPORTS_DIR.iterdir() if path.is_file())
    assert not direct_files, (
        "В корне outputs/exports не должно быть файлов; используйте подкаталоги analytical_csv/chart_data/technical. "
        f"Найдены: {', '.join(direct_files)}."
    )


def validate_chart_data_exports(params: report_params.ReportParams) -> None:
    """Проверить наличие chart data exports и их размещение вне корня outputs/exports."""
    chart_data_dir = config.EXPORTS_CHART_DATA_DIR
    assert chart_data_dir.exists(), f"Не найден каталог chart data exports: {chart_data_dir}."
    csv_files = chart_data_files_for_params(params)
    assert csv_files, (
        f"В {chart_data_dir.relative_to(config.PROJECT_ROOT).as_posix()} нет CSV-основ графиков "
        f"для текущего suffix `{make_output_suffix(params)}`."
    )
    direct_root_files = [path.name for path in chart_data_dir.glob("*.xlsx")]
    assert not direct_root_files, f"В chart_data не должно быть XLSX-файлов: {', '.join(direct_root_files)}."


def validate_volume_bln_units(params: report_params.ReportParams) -> None:
    """Проверить, что chart data с объемами содержит млрд-колонки и единицы измерения."""
    csv_files = chart_data_files_for_params(params)
    volume_files = [path for path in csv_files if file_has_volume_signal(path)]
    assert volume_files, "Не найдены chart data exports с volume-полями для проверки `*_bln`."

    missing_bln: list[str] = []
    missing_unit: list[str] = []
    invalid_bln: list[str] = []
    for path in volume_files:
        try:
            sample = pd.read_csv(path, nrows=50)
        except Exception:
            continue
        volume_columns = [column for column in sample.columns if "placement_volume" in column and not column.endswith("_label")]
        if any(column.endswith("_bln") for column in volume_columns):
            bln_columns = [column for column in volume_columns if column.endswith("_bln")]
            for column in bln_columns:
                numeric = pd.to_numeric(sample[column], errors="coerce")
                if numeric.notna().any() and numeric.max(skipna=True) > 100_000:
                    invalid_bln.append(path.relative_to(config.PROJECT_ROOT).as_posix())
                    break
        else:
            missing_bln.append(path.relative_to(config.PROJECT_ROOT).as_posix())

        unit_columns = [column for column in sample.columns if column.endswith("_unit") or column == "placement_volume_unit"]
        if not unit_columns:
            missing_unit.append(path.relative_to(config.PROJECT_ROOT).as_posix())

    assert not missing_bln, f"В chart data с объемами отсутствует `placement_volume_bln`: {', '.join(missing_bln[:10])}."
    assert not missing_unit, f"В chart data с объемами отсутствует колонка единиц измерения: {', '.join(missing_unit[:10])}."
    assert not invalid_bln, f"`*_bln` выглядит как исходные млн рублей, а не млрд: {', '.join(invalid_bln[:10])}."


def require_dataframe(df: pd.DataFrame | None, name: str) -> pd.DataFrame:
    assert df is not None, f"{name} не найден."
    return df


def unique_period_rows(scope: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "report_period_label",
        "report_period_type",
        "aggregation_mode",
        "report_period_start",
        "report_period_end",
        "is_target_period",
    ]
    return scope[columns].drop_duplicates().reset_index(drop=True)


def to_bool(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False).astype(bool)
    return series.astype("string").str.lower().isin({"true", "1", "yes", "да"})


def is_one_quarter(start: date, end: date) -> bool:
    quarter_start_months = {1, 4, 7, 10}
    if start.day != 1 or start.month not in quarter_start_months:
        return False
    expected_end_month = start.month + 2
    if expected_end_month > 12:
        return False
    next_month = expected_end_month + 1
    next_year = start.year
    if next_month == 13:
        next_month = 1
        next_year += 1
    expected_end = pd.Timestamp(date(next_year, next_month, 1)) - pd.Timedelta(days=1)
    return end == expected_end.date()


def filter_monthly_by_params(
    monthly: pd.DataFrame,
    params: report_params.ReportParams,
) -> pd.DataFrame:
    labels = {str(period["report_period_label"]) for period in params.periods}
    years = {int(period["report_year"]) for period in params.periods}
    report_year = pd.to_numeric(monthly["report_year"], errors="coerce").astype("Int64")
    mask = (
        monthly["report_period_label"].astype("string").isin(labels)
        & (monthly["aggregation_mode"].astype("string") == params.aggregation_mode)
        & report_year.isin(years)
    )
    return monthly.loc[mask].copy()


def file_has_volume_signal(path: Path) -> bool:
    """Быстро определить, содержит ли CSV поля объема размещения."""
    try:
        columns = pd.read_csv(path, nrows=0).columns
    except Exception:
        return False
    return any("placement_volume" in column for column in columns)


def chart_data_files_for_params(params: report_params.ReportParams) -> list[Path]:
    """Вернуть CSV-основы графиков только для текущего набора параметров."""
    if not config.EXPORTS_CHART_DATA_DIR.exists():
        return []
    suffix = make_output_suffix(params)
    return sorted(config.EXPORTS_CHART_DATA_DIR.rglob(f"*_{suffix}.csv"))


def make_output_suffix(params: report_params.ReportParams) -> str:
    """Сформировать suffix outputs так же, как в графических скриптах."""
    return (
        f"{params.period_type}_{params.aggregation_mode}_{params.report_date.isoformat()}_"
        f"retrospective_{params.retrospective_years}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
