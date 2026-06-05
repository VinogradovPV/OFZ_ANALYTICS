"""Параметры отчета и построение отчетных периодов.

Модуль не содержит hardcode под конкретный месяц, квартал или год:
периоды строятся только из `report_date`, `retrospective_years`,
`period_type` и `aggregation_mode`.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, Literal, Sequence


PeriodType = Literal["month", "quarter", "year"]
AggregationMode = Literal["cumulative", "point"]

ALLOWED_PERIOD_TYPES: set[str] = {"month", "quarter", "year"}
ALLOWED_AGGREGATION_MODES: set[str] = {"cumulative", "point"}
QUARTER_REPORT_MONTHS = {1, 4, 7, 10}


@dataclass(frozen=True)
class ReportParams:
    """Проверенные параметры отчета и периоды сравнения."""

    report_date: date
    retrospective_years: int
    period_type: str
    aggregation_mode: str
    periods: list[dict[str, Any]]


def parse_report_args(argv: Sequence[str] | None = None) -> ReportParams:
    """Разобрать CLI-аргументы отчета и вернуть проверенные параметры."""
    parser = argparse.ArgumentParser(
        description="Запуск аналитики ОФЗ для параметризуемого отчетного периода."
    )
    parser.add_argument(
        "--report-date",
        required=True,
        help="Отчетная дата в формате YYYY-MM-DD. Должна быть первым днем месяца.",
    )
    parser.add_argument(
        "--retrospective-years",
        required=True,
        type=int,
        help="Количество лет ретроспективы перед целевым периодом.",
    )
    parser.add_argument(
        "--period-type",
        required=True,
        help="Тип отчетного периода: month, quarter или year.",
    )
    parser.add_argument(
        "--aggregation-mode",
        default="cumulative",
        choices=sorted(ALLOWED_AGGREGATION_MODES),
        help="Режим агрегации периода: cumulative или point. По умолчанию cumulative.",
    )

    args = parser.parse_args(argv)

    try:
        report_date = date.fromisoformat(args.report_date)
    except ValueError:
        parser.error("--report-date должен быть корректной датой в формате YYYY-MM-DD.")

    period_type = normalize_period_type(args.period_type)
    aggregation_mode = normalize_aggregation_mode(args.aggregation_mode)

    try:
        validate_report_date(report_date)
        validate_period_type(period_type)
        validate_aggregation_mode(aggregation_mode)
        validate_period_constraints(report_date, period_type, aggregation_mode)
        validate_retrospective_years(args.retrospective_years)
        periods = build_report_periods(
            report_date=report_date,
            retrospective_years=args.retrospective_years,
            period_type=period_type,
            aggregation_mode=aggregation_mode,
        )
    except ValueError as exc:
        parser.error(str(exc))

    return ReportParams(
        report_date=report_date,
        retrospective_years=args.retrospective_years,
        period_type=period_type,
        aggregation_mode=aggregation_mode,
        periods=periods,
    )


def validate_report_date(report_date: date) -> None:
    """Проверить, что report_date приходится на первый день месяца."""
    if report_date.day != 1:
        raise ValueError(
            f"report_date должен быть первым днем месяца; получено {report_date.isoformat()}."
        )


def normalize_period_type(period_type: str) -> PeriodType:
    """Нормализовать и проверить пользовательский тип периода."""
    normalized = str(period_type).strip().lower()
    validate_period_type(normalized)
    return normalized  # type: ignore[return-value]


def validate_period_type(period_type: str) -> None:
    """Проверить поддерживаемый тип отчетного периода."""
    if period_type not in ALLOWED_PERIOD_TYPES:
        allowed = ", ".join(sorted(ALLOWED_PERIOD_TYPES))
        raise ValueError(f"period_type должен быть одним из: {allowed}; получено {period_type!r}.")


def normalize_aggregation_mode(aggregation_mode: str) -> AggregationMode:
    """Нормализовать и проверить режим агрегации отчетного периода."""
    normalized = str(aggregation_mode).strip().lower()
    validate_aggregation_mode(normalized)
    return normalized  # type: ignore[return-value]


def validate_aggregation_mode(aggregation_mode: str) -> None:
    """Проверить поддерживаемый режим агрегации."""
    if aggregation_mode not in ALLOWED_AGGREGATION_MODES:
        allowed = ", ".join(sorted(ALLOWED_AGGREGATION_MODES))
        raise ValueError(
            f"aggregation_mode должен быть одним из: {allowed}; получено {aggregation_mode!r}."
        )


def validate_period_constraints(
    report_date: date,
    period_type: str,
    aggregation_mode: str = "cumulative",
) -> None:
    """Проверить календарные ограничения для выбранного типа периода."""
    period_type = normalize_period_type(period_type)
    aggregation_mode = normalize_aggregation_mode(aggregation_mode)
    validate_report_date(report_date)

    if period_type == "month":
        return

    if period_type == "quarter" and report_date.month not in QUARTER_REPORT_MONTHS:
        raise ValueError(
            "Для quarter report_date должен быть 1 января, 1 апреля, 1 июля "
            f"или 1 октября; получено {report_date.isoformat()}."
        )

    if period_type == "year" and report_date.month != 1:
        raise ValueError(
            f"Для year report_date должен быть 1 января; получено {report_date.isoformat()}."
        )


def build_report_periods(
    report_date: date,
    retrospective_years: int,
    period_type: str,
    aggregation_mode: str = "cumulative",
) -> list[dict[str, Any]]:
    """Построить ретроспективные и целевой периоды от старого к новому."""
    period_type = normalize_period_type(period_type)
    aggregation_mode = normalize_aggregation_mode(aggregation_mode)
    validate_period_constraints(report_date, period_type, aggregation_mode)
    validate_retrospective_years(retrospective_years)

    periods: list[dict[str, Any]] = []
    shifts = range(retrospective_years, -1, -1)
    for report_period_order, year_shift in enumerate(shifts):
        bounds = get_period_bounds(
            report_date=report_date,
            period_type=period_type,
            aggregation_mode=aggregation_mode,
            year_shift=year_shift,
        )
        start_date = bounds["period_start"]
        end_date = bounds["period_end"]
        period = {
            "period_start": start_date,
            "period_end": end_date,
            "report_period_label": bounds["report_period_label"],
            "report_period_display_label": bounds["report_period_display_label"],
            "report_period_file_label": bounds["report_period_file_label"],
            "report_year": start_date.year,
            "report_period_order": report_period_order,
            "aggregation_mode": aggregation_mode,
            "is_target_period": year_shift == 0,
            # Alias-поля оставлены для существующих downstream-скриптов.
            "period_type": period_type,
            "year_shift": year_shift,
            "start_date": start_date,
            "end_date": end_date,
            "label": bounds["report_period_label"],
        }
        periods.append(period)

    if len(periods) != retrospective_years + 1:
        raise RuntimeError("Внутренняя ошибка: построено неверное количество отчетных периодов.")
    return periods


def get_period_bounds(
    report_date: date,
    period_type: str,
    aggregation_mode: str = "cumulative",
    year_shift: int = 0,
) -> dict[str, Any]:
    """Вернуть границы и метки выбранного отчетного периода."""
    period_type = normalize_period_type(period_type)
    aggregation_mode = normalize_aggregation_mode(aggregation_mode)
    validate_period_constraints(report_date, period_type, aggregation_mode)
    if year_shift < 0:
        raise ValueError(f"year_shift должен быть неотрицательным; получено {year_shift}.")

    shifted_report_date = date(report_date.year - year_shift, report_date.month, 1)
    end_date = shifted_report_date - timedelta(days=1)

    if period_type == "month":
        if aggregation_mode == "cumulative":
            start_date = date(end_date.year, 1, 1)
        else:
            start_date = date(end_date.year, end_date.month, 1)
    elif period_type == "quarter":
        if aggregation_mode == "cumulative":
            start_date = date(end_date.year, 1, 1)
        else:
            start_month = shifted_report_date.month - 3
            start_year = shifted_report_date.year
            if start_month <= 0:
                start_month += 12
                start_year -= 1
            start_date = date(start_year, start_month, 1)
    elif period_type == "year":
        start_date = date(end_date.year, 1, 1)
    else:
        validate_period_type(period_type)
        raise ValueError(f"Неподдерживаемый period_type: {period_type!r}.")

    label = make_period_label(start_date, end_date, period_type, aggregation_mode)
    display_label = make_period_display_label(start_date, end_date, period_type, aggregation_mode)
    file_label = make_period_file_label(start_date, end_date, period_type, aggregation_mode)

    return {
        "period_start": start_date,
        "period_end": end_date,
        "report_period_label": label,
        "period_label": label,
        "report_period_display_label": display_label,
        "period_display_label": display_label,
        "report_period_file_label": file_label,
        "period_file_label": file_label,
    }


def validate_retrospective_years(retrospective_years: int) -> None:
    """Проверить количество лет ретроспективы."""
    if isinstance(retrospective_years, bool) or not isinstance(retrospective_years, int):
        raise ValueError(
            "retrospective_years должен быть целым числом больше или равным нулю; "
            f"получено {retrospective_years!r}."
        )
    if retrospective_years < 0:
        raise ValueError(
            "retrospective_years должен быть нулем или положительным целым числом; "
            f"получено {retrospective_years}."
        )


def make_period_label(
    start_date: date,
    end_date: date,
    period_type: str,
    aggregation_mode: str,
) -> str:
    """Сформировать техническую метку периода для таблиц и группировок."""
    if period_type == "month":
        if aggregation_mode == "cumulative":
            return f"{start_date.year}-M{start_date.month:02d}-M{end_date.month:02d}"
        return start_date.strftime("%Y-%m")
    if period_type == "quarter":
        start_quarter = quarter_number(start_date)
        end_quarter = quarter_number(end_date)
        if aggregation_mode == "cumulative":
            return f"{start_date.year}-Q{start_quarter}-Q{end_quarter}"
        return f"{start_date.year}-Q{start_quarter}"
    if period_type == "year":
        return str(start_date.year)
    return f"{start_date.isoformat()}_{end_date.isoformat()}"


def make_period_display_label(
    start_date: date,
    end_date: date,
    period_type: str,
    aggregation_mode: str,
) -> str:
    """Сформировать человекочитаемую метку периода."""
    if period_type == "month" and aggregation_mode == "cumulative":
        return f"{start_date.year}: {start_date:%m}.{start_date:%d} - {end_date:%m}.{end_date:%d}"
    if period_type == "quarter" and aggregation_mode == "cumulative":
        return f"{start_date.year}: Q{quarter_number(start_date)}-Q{quarter_number(end_date)}"
    return make_period_label(start_date, end_date, period_type, aggregation_mode)


def make_period_file_label(
    start_date: date,
    end_date: date,
    period_type: str,
    aggregation_mode: str,
) -> str:
    """Сформировать безопасную метку периода для имен файлов."""
    if period_type == "month":
        if aggregation_mode == "cumulative":
            return f"{start_date.year}_m{start_date.month:02d}_m{end_date.month:02d}"
        return start_date.strftime("%Y_m%m")
    if period_type == "quarter":
        start_quarter = quarter_number(start_date)
        end_quarter = quarter_number(end_date)
        if aggregation_mode == "cumulative":
            return f"{start_date.year}_q{start_quarter}_q{end_quarter}"
        return f"{start_date.year}_q{start_quarter}"
    if period_type == "year":
        return str(start_date.year)
    return f"{start_date.isoformat()}_{end_date.isoformat()}".replace("-", "_")


def quarter_number(value: date) -> int:
    """Вернуть номер квартала для календарной даты."""
    return ((value.month - 1) // 3) + 1


def _make_period_label(start_date: date, end_date: date, period_type: str) -> str:
    """Backward-compatible wrapper for old callers."""
    return make_period_label(start_date, end_date, period_type, "point")
