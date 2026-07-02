"""Состояние и валидация desktop GUI launcher."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path


ALLOWED_PERIOD_TYPES = {"month", "quarter", "year"}
ALLOWED_AGGREGATION_MODES = {"cumulative", "point"}
ALLOWED_REGISTRY_MODES = {"off", "warn", "strict"}
ALLOWED_STAGE_ZERO_MODES = {"off", "dry-run", "download"}
DEFAULT_CBR_FROM_DATE = "01.01.2019"
DEFAULT_CBR_TO_DATE = "02.07.2026"
DEFAULT_CBR_HTML_FIXTURE = "scripts/qa/fixtures/cbr/key_rate_page_2019_2026.html"
DEFAULT_CBR_XLSX_FILE = "data/raw/cbr/key_rate_inflation/cbr_key_rate_inflation_2019-01_2026-05.xlsx"


def default_report_date() -> str:
    today = date.today()
    return today.replace(day=1).isoformat()


def parse_cbr_gui_date(value: str, field_name: str) -> date:
    try:
        return datetime.strptime(value.strip(), "%d.%m.%Y").date()
    except ValueError as exc:
        raise ValueError(f"{field_name} должна быть в формате DD.MM.YYYY.") from exc


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
    cbr_from_date: str = DEFAULT_CBR_FROM_DATE
    cbr_to_date: str = DEFAULT_CBR_TO_DATE
    cbr_url: str = ""
    cbr_html_file: str = DEFAULT_CBR_HTML_FIXTURE
    cbr_xlsx_file: str = DEFAULT_CBR_XLSX_FILE
    cbr_timeout_seconds: int = 30
    cbr_retries: int = 2
    cbr_save_html_snapshot: bool = False
    cbr_no_network: bool = False

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
        cbr_from = parse_cbr_gui_date(self.cbr_from_date, "CBR from date")
        cbr_to = parse_cbr_gui_date(self.cbr_to_date, "CBR to date")
        if cbr_from > cbr_to:
            raise ValueError("CBR from date должна быть меньше или равна CBR to date.")
        if not 1 <= int(self.cbr_timeout_seconds) <= 120:
            raise ValueError("CBR timeout seconds должен быть в диапазоне 1..120.")
        if not 0 <= int(self.cbr_retries) <= 10:
            raise ValueError("CBR retries должен быть в диапазоне 0..10.")
        if self.cbr_no_network and not (self.cbr_html_file.strip() or self.cbr_xlsx_file.strip()):
            raise ValueError("Для CBR no network укажите HTML fixture или XLSX fallback.")

    @property
    def venv_scripts(self) -> Path:
        return self.project_root / ".venv" / "Scripts"

    @property
    def python_executable(self) -> Path:
        return self.venv_scripts / "python.exe"

    @property
    def launcher_log_dir(self) -> Path:
        return self.project_root / ".ofz_launcher" / "logs"

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

    def pipeline_registry_args(self) -> list[str]:
        legacy_flag = "--allow-legacy-raw" if self.allow_legacy_raw else "--no-allow-legacy-raw"
        return ["--source-registry-mode", self.source_registry_mode, legacy_flag]
