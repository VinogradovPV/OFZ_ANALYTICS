"""Состояние и валидация desktop GUI launcher."""

from __future__ import annotations

import csv
import json
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
DEFAULT_CBR_XLSX_FILE = "data/raw/cbr/key_rate/key_rate_fallback.xlsx"
CBR_PREFERRED_SOURCE_URL = "https://cbr.ru/hd_base/KeyRate/"
CBR_DAILY_COLUMNS = ("date", "value")
CBR_MONTHLY_COLUMNS = (
    "period_month",
    "period_label",
    "key_rate_month_end_pct",
    "key_rate_date",
    "key_rate_source_rule",
    "key_rate_month_is_partial",
)
CBR_FORBIDDEN_DAILY_COLUMNS = {"inflation", "inflation_yoy", "inflation_target"}
CBR_LEGACY_SOURCE_MARKER = "data/raw/cbr/key_rate_inflation"


def default_report_date() -> str:
    today = date.today()
    return today.replace(day=1).isoformat()


def parse_cbr_gui_date(value: str, field_name: str) -> date:
    try:
        return datetime.strptime(value.strip(), "%d.%m.%Y").date()
    except ValueError as exc:
        raise ValueError(f"{field_name} должна быть в формате DD.MM.YYYY.") from exc


@dataclass(frozen=True)
class CbrReferenceStatus:
    """User-facing status for generated Bank of Russia key-rate datasets."""

    status: str
    severity: str
    next_step: str
    latest_date: str = "-"
    latest_value: str = "-"
    daily_rows: int = 0
    source_label: str = "-"
    retrieved_at: str = "-"
    checks: tuple[str, ...] = ()
    parser: str = "-"
    source_url: str = "-"
    source_file: str = "-"
    html_sha256: str = "-"
    daily_path: Path | None = None
    monthly_path: Path | None = None
    meta_path: Path | None = None

    @property
    def paths_label(self) -> str:
        if not (self.daily_path and self.monthly_path and self.meta_path):
            return "-"
        return f"daily: {self.daily_path} | monthly: {self.monthly_path} | meta: {self.meta_path}"


def check_cbr_reference_status(project_root: Path, reference_root: Path | None = None) -> CbrReferenceStatus:
    """Validate generated CBR reference datasets and their provenance."""
    root = project_root.resolve()
    reference_root = reference_root or root / "data/processed/reference"
    daily_path = reference_root / "cbr_key_rate_daily.csv"
    monthly_path = reference_root / "cbr_key_rate_monthly.csv"
    meta_path = reference_root / "cbr_key_rate_daily.meta.json"
    common_paths = {
        "daily_path": daily_path,
        "monthly_path": monthly_path,
        "meta_path": meta_path,
    }
    checks = [
        f"daily CSV exists: {'yes' if daily_path.exists() else 'no'}",
        f"monthly CSV exists: {'yes' if monthly_path.exists() else 'no'}",
        f"meta exists: {'yes' if meta_path.exists() else 'no'}",
    ]
    if not daily_path.exists() or not monthly_path.exists() or not meta_path.exists():
        return CbrReferenceStatus(
            status="Reference datasets не найдены",
            severity="missing",
            next_step=(
                "Нажмите 'Проверить сайт Банка России', затем "
                "'Обновить ключевую ставку'."
            ),
            checks=tuple(checks + ["source still valid: no"]),
            **common_paths,
        )

    try:
        with daily_path.open("r", encoding="utf-8", newline="") as handle:
            daily_reader = csv.DictReader(handle)
            daily_columns = tuple(daily_reader.fieldnames or ())
            daily_rows = list(daily_reader)
    except Exception as exc:
        return CbrReferenceStatus(
            status=f"Daily dataset не читается: {exc}",
            severity="error",
            next_step="Пересоздайте reference datasets с сайта Банка России.",
            checks=tuple(checks + ["source still valid: unknown"]),
            **common_paths,
        )

    if set(daily_columns).intersection(CBR_FORBIDDEN_DAILY_COLUMNS):
        return CbrReferenceStatus(
            status="Daily dataset содержит устаревшие inflation columns",
            severity="error",
            next_step="Пересоздайте reference datasets: daily CSV должен содержать только date,value.",
            daily_rows=len(daily_rows),
            checks=tuple(checks + ["daily columns: invalid", "source still valid: unknown"]),
            **common_paths,
        )
    if daily_columns != CBR_DAILY_COLUMNS:
        return CbrReferenceStatus(
            status="Daily dataset не соответствует contract",
            severity="error",
            next_step="Пересоздайте reference datasets: daily CSV должен содержать строго date,value.",
            daily_rows=len(daily_rows),
            checks=tuple(checks + [f"daily columns: {','.join(daily_columns) or '-'}", "source still valid: unknown"]),
            **common_paths,
        )

    try:
        with monthly_path.open("r", encoding="utf-8", newline="") as handle:
            monthly_reader = csv.DictReader(handle)
            monthly_columns = tuple(monthly_reader.fieldnames or ())
    except Exception as exc:
        return CbrReferenceStatus(
            status=f"Monthly dataset не читается: {exc}",
            severity="error",
            next_step="Пересоздайте monthly reference dataset с сайта Банка России.",
            daily_rows=len(daily_rows),
            checks=tuple(checks + ["monthly columns: unreadable", "source still valid: unknown"]),
            **common_paths,
        )
    missing_monthly = [column for column in CBR_MONTHLY_COLUMNS if column not in monthly_columns]
    if missing_monthly:
        return CbrReferenceStatus(
            status="Monthly dataset не соответствует contract",
            severity="error",
            next_step="Пересоздайте monthly reference dataset с сайта Банка России.",
            daily_rows=len(daily_rows),
            checks=tuple(checks + [f"monthly missing: {', '.join(missing_monthly)}", "source still valid: unknown"]),
            **common_paths,
        )

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return CbrReferenceStatus(
            status=f"Meta JSON не читается: {exc}",
            severity="error",
            next_step="Пересоздайте metadata с сайта Банка России.",
            daily_rows=len(daily_rows),
            checks=tuple(checks + ["source still valid: unknown"]),
            **common_paths,
        )

    latest = max(daily_rows, key=lambda row: row.get("date", "")) if daily_rows else {}
    latest_value = "-"
    if latest.get("value"):
        latest_value = f"{float(latest['value']):.2f}%"
    parser = str(meta.get("source_parser") or meta.get("parser") or "-")
    source_type = str(meta.get("source_type") or "")
    source_url = str(meta.get("source_url") or "-")
    source_file = str(meta.get("source_file") or "-")
    retrieved_at = str(meta.get("retrieved_at") or "-")
    html_sha256 = str(meta.get("html_sha256") or "-")
    legacy_source = _contains_legacy_cbr_path(source_url) or _contains_legacy_cbr_path(source_file)

    if parser == "xlsx_fallback" or source_type == "xlsx_fallback":
        source_exists = source_file != "-" and (root / source_file).exists()
        if source_file != "-" and Path(source_file).is_absolute():
            source_exists = Path(source_file).exists()
        if source_exists:
            status = "Reference datasets построены из XLSX fallback"
            next_step = "Предпочтительно обновить с сайта Банка России."
            source_valid = "yes"
        else:
            status = "Reference datasets есть, но исходный XLSX fallback удален"
            next_step = "Рекомендуется обновить ключевую ставку с сайта Банка России."
            source_valid = "no"
        if legacy_source:
            status = (
                "Legacy source path: key_rate_inflation. Инфляция вне scope. "
                "Рекомендуется обновить web source."
            ) if source_exists else status
        return CbrReferenceStatus(
            status=status,
            severity="warning",
            next_step=next_step,
            latest_date=latest.get("date", "-"),
            latest_value=latest_value,
            daily_rows=len(daily_rows),
            source_label="XLSX fallback legacy",
            retrieved_at=retrieved_at,
            checks=tuple(checks + [f"source still valid: {source_valid}"]),
            parser=parser,
            source_url=source_url,
            source_file=source_file,
            html_sha256=html_sha256,
            **common_paths,
        )

    if legacy_source:
        return CbrReferenceStatus(
            status=(
                "Legacy source path: key_rate_inflation. Инфляция вне scope. "
                "Рекомендуется обновить web source."
            ),
            severity="warning",
            next_step="Обновите ключевую ставку с сайта Банка России.",
            latest_date=latest.get("date", "-"),
            latest_value=latest_value,
            daily_rows=len(daily_rows),
            source_label="legacy source path",
            retrieved_at=retrieved_at,
            checks=tuple(checks + ["source still valid: no"]),
            parser=parser,
            source_url=source_url,
            source_file=source_file,
            html_sha256=html_sha256,
            **common_paths,
        )

    if parser in {"html_table", "highcharts_fallback"} or source_type == "web":
        source_ok = source_url.startswith(CBR_PREFERRED_SOURCE_URL)
        source_label = "сайт Банка России table.data" if parser == "html_table" else "сайт Банка России Highcharts fallback"
        if source_type == "html_fixture":
            source_ok = source_file != "-" and (root / source_file).exists()
            source_label = "HTML fixture"
        if not source_ok:
            return CbrReferenceStatus(
                status="Reference datasets требуют обновления source provenance",
                severity="warning",
                next_step="Обновите ключевую ставку с сайта Банка России.",
                latest_date=latest.get("date", "-"),
                latest_value=latest_value,
                daily_rows=len(daily_rows),
                source_label=source_label,
                retrieved_at=retrieved_at,
                checks=tuple(checks + ["source still valid: no"]),
                parser=parser,
                source_url=source_url,
                source_file=source_file,
                html_sha256=html_sha256,
                **common_paths,
            )
        return CbrReferenceStatus(
            status="Reference datasets доступны",
            severity="ok",
            next_step="Можно строить график ОФЗ-ПД + ключевая ставка.",
            latest_date=latest.get("date", "-"),
            latest_value=latest_value,
            daily_rows=len(daily_rows),
            source_label=source_label,
            retrieved_at=retrieved_at,
            checks=tuple(checks + ["source still valid: yes"]),
            parser=parser,
            source_url=source_url,
            source_file=source_file,
            html_sha256=html_sha256,
            **common_paths,
        )

    return CbrReferenceStatus(
        status="Reference datasets требуют проверки provenance",
        severity="warning",
        next_step="Обновите ключевую ставку с сайта Банка России.",
        latest_date=latest.get("date", "-"),
        latest_value=latest_value,
        daily_rows=len(daily_rows),
        source_label="-",
        retrieved_at=retrieved_at,
        checks=tuple(checks + ["source still valid: unknown"]),
        parser=parser,
        source_url=source_url,
        source_file=source_file,
        html_sha256=html_sha256,
        **common_paths,
    )


def _contains_legacy_cbr_path(value: str) -> bool:
    return CBR_LEGACY_SOURCE_MARKER in value.replace("\\", "/")


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
