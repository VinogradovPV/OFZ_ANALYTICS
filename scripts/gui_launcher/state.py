"""Состояние и валидация desktop GUI launcher."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


ALLOWED_PERIOD_TYPES = {"month", "quarter", "year"}
ALLOWED_AGGREGATION_MODES = {"cumulative", "point"}
ALLOWED_REGISTRY_MODES = {"off", "warn", "strict"}
ALLOWED_STAGE_ZERO_MODES = {"off", "dry-run", "download"}


def default_report_date() -> str:
    today = date.today()
    return today.replace(day=1).isoformat()


@dataclass
class GuiState:
    """Параметры, общие для GUI actions."""

    project_root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2])
    report_date: str = field(default_factory=default_report_date)
    retrospective_years: int = 4
    period_type: str = "month"
    aggregation_mode: str = "cumulative"
    source_registry_mode: str = "warn"
    allow_legacy_raw: bool = True
    minfin_year: int = field(default_factory=lambda: date.today().year)
    final_year: int = field(default_factory=lambda: date.today().year - 1)
    minfin_mode: str = "monthly"
    minfin_url: str = ""
    max_pages: int = 10
    no_network: bool = False
    html_file: str = ""
    manual_file: str = ""
    stage_zero_mode: str = "dry-run"
    run_schema_before_pipeline: bool = False
    open_outputs_after_run: bool = False

    def validate(self) -> None:
        root = self.project_root.resolve()
        if not (root / "pyproject.toml").is_file():
            raise ValueError(f"Не найден pyproject.toml в project root: {root}")
        parsed_date = date.fromisoformat(self.report_date)
        if parsed_date.day != 1:
            raise ValueError("Report date должна быть первым днем месяца.")
        if not 1 <= int(self.retrospective_years) <= 10:
            raise ValueError("Retrospective years должен быть в диапазоне 1..10.")
        if self.period_type not in ALLOWED_PERIOD_TYPES:
            raise ValueError(f"Недопустимый period type: {self.period_type}")
        if self.aggregation_mode not in ALLOWED_AGGREGATION_MODES:
            raise ValueError(f"Недопустимый aggregation mode: {self.aggregation_mode}")
        if self.source_registry_mode not in ALLOWED_REGISTRY_MODES:
            raise ValueError(f"Недопустимый source registry mode: {self.source_registry_mode}")
        if self.stage_zero_mode not in ALLOWED_STAGE_ZERO_MODES:
            raise ValueError(f"Недопустимый stage zero mode: {self.stage_zero_mode}")
        if not 2000 <= int(self.minfin_year) <= 2100:
            raise ValueError("Year должен быть в диапазоне 2000..2100.")
        if not 2000 <= int(self.final_year) <= 2100:
            raise ValueError("Final year должен быть в диапазоне 2000..2100.")
        if not 1 <= int(self.max_pages) <= 100:
            raise ValueError("Max pages должен быть в диапазоне 1..100.")

    @property
    def venv_scripts(self) -> Path:
        return self.project_root / ".venv" / "Scripts"

    @property
    def python_executable(self) -> Path:
        return self.venv_scripts / "python.exe"

    @property
    def launcher_log_dir(self) -> Path:
        return self.project_root / "outputs" / "reports" / "launcher"

    @property
    def output_suffix(self) -> str:
        return (
            f"{self.period_type}_{self.aggregation_mode}_{self.report_date}_"
            f"retrospective_{self.retrospective_years}"
        )

    def common_report_args(self) -> list[str]:
        return [
            "--report-date",
            self.report_date,
            "--retrospective-years",
            str(self.retrospective_years),
            "--period-type",
            self.period_type,
            "--aggregation-mode",
            self.aggregation_mode,
        ]
