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
CBR_FORBIDDEN_DAILY_COLUMNS = {"inflation", "inflation_yoy", "inflation_target"}
CBR_RAW_ROOT_RELATIVE = Path("data/raw/cbr/key_rate_inflation")
CBR_LATEST_DAILY_RELATIVE = CBR_RAW_ROOT_RELATIVE / "latest/cbr_key_rate_daily.csv"
CBR_LATEST_META_RELATIVE = CBR_RAW_ROOT_RELATIVE / "latest/cbr_key_rate_daily.meta.json"
CBR_REGISTRY_CSV_RELATIVE = CBR_RAW_ROOT_RELATIVE / "registry/cbr_key_rate_registry.csv"
CBR_REGISTRY_LATEST_JSON_RELATIVE = CBR_RAW_ROOT_RELATIVE / "registry/cbr_key_rate_registry_latest.json"
CBR_LEGACY_REFERENCE_RELATIVE = Path("data/processed/reference")


def default_report_date() -> str:
    today = date.today()
    return today.replace(day=1).isoformat()


def parse_cbr_gui_date(value: str, field_name: str) -> date:
    try:
        return datetime.strptime(value.strip(), "%d.%m.%Y").date()
    except ValueError as exc:
        raise ValueError(f"{field_name} должна быть в формате DD.MM.YYYY.") from exc


@dataclass(frozen=True)
class CbrRawStatus:
    """User-facing status for the raw Bank of Russia key-rate dataset."""

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
    latest_path: Path | None = None
    meta_path: Path | None = None
    registry_path: Path | None = None
    registry_latest_path: Path | None = None

    @property
    def paths_label(self) -> str:
        if not (self.latest_path and self.meta_path and self.registry_path):
            return "-"
        return f"latest: {self.latest_path} | meta: {self.meta_path} | registry: {self.registry_path}"


CbrReferenceStatus = CbrRawStatus


def check_cbr_raw_status(project_root: Path, raw_root: Path | None = None) -> CbrRawStatus:
    """Validate the controlled raw CBR key-rate dataset and registry."""
    root = project_root.resolve()
    raw_root = raw_root or root / CBR_RAW_ROOT_RELATIVE
    latest_path = raw_root / "latest/cbr_key_rate_daily.csv"
    meta_path = raw_root / "latest/cbr_key_rate_daily.meta.json"
    registry_path = raw_root / "registry/cbr_key_rate_registry.csv"
    registry_latest_path = raw_root / "registry/cbr_key_rate_registry_latest.json"
    legacy_reference_root = root / CBR_LEGACY_REFERENCE_RELATIVE
    common_paths = {
        "latest_path": latest_path,
        "meta_path": meta_path,
        "registry_path": registry_path,
        "registry_latest_path": registry_latest_path,
    }
    checks = [
        f"raw latest CSV exists: {'yes' if latest_path.exists() else 'no'}",
        f"meta exists: {'yes' if meta_path.exists() else 'no'}",
        f"registry CSV exists: {'yes' if registry_path.exists() else 'no'}",
        f"registry latest JSON exists: {'yes' if registry_latest_path.exists() else 'no'}",
        f"legacy processed/reference ignored: {'yes' if legacy_reference_root.exists() else 'no'}",
    ]
    if not latest_path.exists():
        return CbrRawStatus(
            status="Raw dataset ключевой ставки не найден",
            severity="missing",
            next_step=(
                "Нажмите 'Проверить сайт Банка России', затем "
                "'Обновить ключевую ставку'."
            ),
            checks=tuple(checks + ["production source: missing raw latest"]),
            **common_paths,
        )

    try:
        with latest_path.open("r", encoding="utf-8", newline="") as handle:
            daily_reader = csv.DictReader(handle)
            daily_columns = tuple(daily_reader.fieldnames or ())
            daily_rows = list(daily_reader)
    except Exception as exc:
        return CbrRawStatus(
            status=f"Raw latest CSV не читается: {exc}",
            severity="error",
            next_step="Обновите raw dataset ключевой ставки с сайта Банка России.",
            checks=tuple(checks + ["production source: unreadable raw latest"]),
            **common_paths,
        )

    if set(daily_columns).intersection(CBR_FORBIDDEN_DAILY_COLUMNS):
        return CbrRawStatus(
            status="Raw latest CSV содержит устаревшие inflation columns",
            severity="error",
            next_step="Обновите raw dataset: daily CSV должен содержать только date,value.",
            daily_rows=len(daily_rows),
            checks=tuple(checks + ["daily columns: invalid"]),
            **common_paths,
        )
    if daily_columns != CBR_DAILY_COLUMNS:
        return CbrRawStatus(
            status="Raw latest CSV не соответствует contract",
            severity="error",
            next_step="Обновите raw dataset: daily CSV должен содержать строго date,value.",
            daily_rows=len(daily_rows),
            checks=tuple(checks + [f"daily columns: {','.join(daily_columns) or '-'}"]),
            **common_paths,
        )

    latest = max(daily_rows, key=lambda row: row.get("date", "")) if daily_rows else {}
    latest_value = "-"
    if latest.get("value"):
        latest_value = f"{float(latest['value']):.2f}%"

    if not meta_path.exists():
        return CbrRawStatus(
            status="Raw latest CSV есть, но meta JSON отсутствует",
            severity="warning",
            next_step="Повторите update ключевой ставки: он восстановит meta без смены CSV, если данные не изменились.",
            latest_date=latest.get("date", "-"),
            latest_value=latest_value,
            daily_rows=len(daily_rows),
            checks=tuple(checks + ["meta consistency: missing"]),
            source_label="raw latest без meta",
            **common_paths,
        )

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return CbrRawStatus(
            status=f"Meta JSON не читается: {exc}",
            severity="error",
            next_step="Обновите raw dataset ключевой ставки с сайта Банка России.",
            daily_rows=len(daily_rows),
            checks=tuple(checks + ["meta consistency: unreadable"]),
            **common_paths,
        )

    raw_sha256 = _sha256_file(latest_path)
    meta_sha256 = str(meta.get("sha256") or "")
    parser = str(meta.get("parser") or meta.get("source_parser") or "-")
    source_type = str(meta.get("source_type") or "")
    source_url = str(meta.get("source_url") or "-")
    source_file = str(meta.get("source_file") or "-")
    retrieved_at = str(meta.get("retrieved_at") or "-")
    html_sha256 = str(meta.get("html_sha256") or "-")

    if meta_sha256 and meta_sha256 != raw_sha256:
        return CbrRawStatus(
            status="Raw latest CSV и meta JSON имеют разные sha256",
            severity="error",
            next_step="Повторите update ключевой ставки с сайта Банка России.",
            latest_date=latest.get("date", "-"),
            latest_value=latest_value,
            daily_rows=len(daily_rows),
            source_label=source_type or "-",
            retrieved_at=retrieved_at,
            checks=tuple(checks + [f"meta sha256: {meta_sha256[:12]}", f"raw sha256: {raw_sha256[:12]}"]),
            parser=parser,
            source_url=source_url,
            source_file=source_file,
            html_sha256=html_sha256,
            **common_paths,
        )

    registry_warning = _registry_warning(registry_path, registry_latest_path, raw_sha256)
    if source_type == "xlsx_fallback" or parser == "xlsx_fallback":
        source_exists = source_file not in {"", "-"} and _source_file_exists(root, source_file)
        source_note = "source file exists" if source_exists else "source file missing"
        return CbrRawStatus(
            status=f"Raw dataset построен из XLSX fallback ({source_note})",
            severity="warning",
            next_step="Обновите ключевую ставку с сайта Банка России, чтобы получить web_table_data.",
            latest_date=latest.get("date", "-"),
            latest_value=latest_value,
            daily_rows=len(daily_rows),
            source_label="XLSX fallback legacy",
            retrieved_at=retrieved_at,
            checks=tuple(checks + [f"source fallback: {source_note}"]),
            parser=parser,
            source_url=source_url,
            source_file=source_file,
            html_sha256=html_sha256,
            **common_paths,
        )

    if registry_warning:
        return CbrRawStatus(
            status=f"Raw dataset есть, но registry требует внимания: {registry_warning}",
            severity="warning",
            next_step="Повторите update ключевой ставки, чтобы синхронизировать registry.",
            latest_date=latest.get("date", "-"),
            latest_value=latest_value,
            daily_rows=len(daily_rows),
            source_label=_source_label(source_type, parser),
            retrieved_at=retrieved_at,
            checks=tuple(checks + [registry_warning]),
            parser=parser,
            source_url=source_url,
            source_file=source_file,
            html_sha256=html_sha256,
            **common_paths,
        )

    if source_type == "web_table_data" and parser == "html_table" and source_url.startswith(CBR_PREFERRED_SOURCE_URL):
        return CbrRawStatus(
            status="Исходные данные Банка России доступны",
            severity="ok",
            next_step="Можно строить график ОФЗ-ПД + ключевая ставка.",
            latest_date=latest.get("date", "-"),
            latest_value=latest_value,
            daily_rows=len(daily_rows),
            source_label="сайт Банка России table.data",
            retrieved_at=retrieved_at,
            checks=tuple(checks + ["production source: raw web_table_data"]),
            parser=parser,
            source_url=source_url,
            source_file=source_file,
            html_sha256=html_sha256,
            **common_paths,
        )

    return CbrRawStatus(
        status="Raw dataset требует проверки provenance",
        severity="warning",
        next_step="Обновите ключевую ставку с сайта Банка России.",
        latest_date=latest.get("date", "-"),
        latest_value=latest_value,
        daily_rows=len(daily_rows),
        source_label=_source_label(source_type, parser),
        retrieved_at=retrieved_at,
        checks=tuple(checks + ["production source: unexpected provenance"]),
        parser=parser,
        source_url=source_url,
        source_file=source_file,
        html_sha256=html_sha256,
        **common_paths,
    )


def check_cbr_reference_status(project_root: Path, reference_root: Path | None = None) -> CbrRawStatus:
    """Compatibility wrapper; production status is raw CBR storage."""
    return check_cbr_raw_status(project_root, raw_root=reference_root)


def _sha256_file(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_file_exists(root: Path, value: str) -> bool:
    path = Path(value)
    return path.exists() if path.is_absolute() else (root / path).exists()


def _source_label(source_type: str, parser: str) -> str:
    if source_type == "web_table_data" and parser == "html_table":
        return "сайт Банка России table.data"
    if source_type == "web_highcharts_fallback":
        return "сайт Банка России Highcharts fallback"
    if source_type == "html_fixture":
        return "HTML fixture"
    if source_type == "xlsx_fallback":
        return "XLSX fallback legacy"
    return source_type or parser or "-"


def _registry_warning(registry_path: Path, registry_latest_path: Path, sha256: str) -> str:
    if not registry_path.exists():
        return "registry CSV missing"
    if not registry_latest_path.exists():
        return "registry latest JSON missing"
    try:
        payload = json.loads(registry_latest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return f"registry latest JSON unreadable: {exc}"
    record = payload.get("record") if isinstance(payload, dict) else None
    if not isinstance(record, dict):
        return "registry latest JSON has no record"
    registry_sha = str(record.get("sha256") or "")
    if registry_sha != sha256:
        return "registry sha256 mismatch"
    if not bool(record.get("is_active", False)):
        return "registry active flag missing"
    return ""


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
