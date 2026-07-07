"""Bank of Russia key rate web parser.

The daily CSV is intentionally a source-shaped copy with exactly two columns:
``date,value``. Provenance is stored separately in ``*.meta.json``.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import UTC, date, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts import config  # noqa: E402


CBR_KEY_RATE_BASE_URL = "https://cbr.ru/hd_base/KeyRate/"
DEFAULT_FROM_DATE = "01.01.2019"
DEFAULT_USER_AGENT = "OFZ_ANALYTICS/0.1 (+https://github.com/VinogradovPV/OFZ_ANALYTICS)"
DEFAULT_OUTPUT_ROOT = config.CBR_KEY_RATE_RAW_DIR
DEFAULT_DAILY_OUTPUT_CSV = config.CBR_KEY_RATE_RAW_DAILY_CSV
DEFAULT_DAILY_META_JSON = config.CBR_KEY_RATE_RAW_DAILY_META_JSON
DEFAULT_MONTHLY_OUTPUT_CSV = config.CBR_REFERENCE_DIR / "cbr_key_rate_monthly.csv"
DEFAULT_HTML_SNAPSHOT = config.OUTPUTS_DIR / "cache" / "cbr_key_rate_page.html"
CONFIRM_TOKEN = "UPDATE_CBR_KEY_RATE"
LATEST_DAILY_NAME = "cbr_key_rate_daily.csv"
LATEST_META_NAME = "cbr_key_rate_daily.meta.json"
REGISTRY_CSV_NAME = "cbr_key_rate_registry.csv"
REGISTRY_LATEST_JSON_NAME = "cbr_key_rate_registry_latest.json"

TABLE_HEADERS = ("Дата", "Ставка")
XLSX_KEY_RATE_COLUMNS = (
    "Ключевая ставка, % годовых",
    "Ключевая ставка",
    "Ставка",
)
RU_MONTH_ABBR = {
    1: "Янв",
    2: "Фев",
    3: "Мар",
    4: "Апр",
    5: "Май",
    6: "Июн",
    7: "Июл",
    8: "Авг",
    9: "Сен",
    10: "Окт",
    11: "Ноя",
    12: "Дек",
}


@dataclass(frozen=True)
class KeyRateObservation:
    """One key-rate observation from the Bank of Russia source."""

    date: date
    value: float


@dataclass(frozen=True)
class WebFetchResult:
    """Fetched HTML with provenance headers."""

    html: str
    page_last_modified: str | None


@dataclass(frozen=True)
class ParserResult:
    """Parser output and parser source marker."""

    observations: list[KeyRateObservation]
    parser: str


@dataclass(frozen=True)
class LatestAvailable:
    """Latest available key-rate observation detected in the parsed source."""

    date: date
    value: float


@dataclass(frozen=True)
class RawWriteResult:
    """Summary of a controlled raw dataset write."""

    status: str
    sha256: str
    latest_csv: Path
    latest_meta: Path
    version_csv: Path | None
    version_meta: Path | None
    registry_csv: Path
    registry_latest_json: Path


class CbrTableParser(HTMLParser):
    """Extract rows from CBR ``table.data`` elements."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self._inside_table = False
        self._inside_cell = False
        self._current_rows: list[list[str]] = []
        self._current_row: list[str] | None = None
        self._current_cell: list[str] = []
        self._table_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs_map = {key.lower(): value or "" for key, value in attrs}
        if tag == "table":
            if self._inside_table:
                self._table_depth += 1
                return
            classes = set(attrs_map.get("class", "").split())
            if "data" in classes:
                self._inside_table = True
                self._table_depth = 1
                self._current_rows = []
        elif self._inside_table and tag == "tr":
            self._current_row = []
        elif self._inside_table and self._current_row is not None and tag in {"th", "td"}:
            self._inside_cell = True
            self._current_cell = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._inside_table and self._inside_cell and tag in {"th", "td"}:
            cell = normalize_cell_text("".join(self._current_cell))
            if self._current_row is not None:
                self._current_row.append(cell)
            self._inside_cell = False
            self._current_cell = []
        elif self._inside_table and tag == "tr":
            if self._current_row and any(cell.strip() for cell in self._current_row):
                self._current_rows.append(self._current_row)
            self._current_row = None
        elif self._inside_table and tag == "table":
            self._table_depth -= 1
            if self._table_depth <= 0:
                self.tables.append(self._current_rows)
                self._inside_table = False
                self._current_rows = []

    def handle_data(self, data: str) -> None:
        if self._inside_table and self._inside_cell:
            self._current_cell.append(data)


def normalize_cell_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def build_cbr_key_rate_url(from_date: str, to_date: str) -> str:
    """Build a CBR KeyRate URL with DD.MM.YYYY query parameters."""
    parse_cbr_query_date(from_date)
    parse_cbr_query_date(to_date)
    query = urlencode(
        {
            "UniDbQuery.Posted": "True",
            "UniDbQuery.From": from_date,
            "UniDbQuery.To": to_date,
        }
    )
    return f"{CBR_KEY_RATE_BASE_URL}?{query}"


def default_to_date() -> str:
    """Return the local operator date in CBR query format."""
    return date.today().strftime("%d.%m.%Y")


def parse_cbr_query_date(value: str) -> date:
    return datetime.strptime(value, "%d.%m.%Y").date()


def parse_source_date(value: object) -> date:
    text = normalize_cell_text(str(value))
    for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    month_match = re.fullmatch(r"(?P<month>\d{1,2})\.(?P<year>\d{4})", text)
    if not month_match and "." in text:
        month_part, year_part = text.split(".", 1)
        if len(year_part) == 3 and year_part.startswith("20"):
            text = f"{month_part}.{year_part}0"
            month_match = re.fullmatch(r"(?P<month>\d{1,2})\.(?P<year>\d{4})", text)
    if month_match:
        return date(int(month_match.group("year")), int(month_match.group("month")), 1)
    raise ValueError(f"Invalid CBR key rate date: {text!r}")


def parse_rate_value(value: object) -> float:
    text = normalize_cell_text(str(value)).replace(" ", "").replace(",", ".")
    parsed = float(text)
    if parsed < 0 or parsed > 50:
        raise ValueError(f"CBR key rate value is outside 0..50 range: {parsed}")
    return parsed


def fetch_web_page(url: str, timeout_seconds: int, retries: int, user_agent: str) -> WebFetchResult:
    """Fetch CBR HTML and return decoded text plus Last-Modified if present."""
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            request = Request(url, headers={"User-Agent": user_agent})
            with urlopen(request, timeout=timeout_seconds) as response:
                body = response.read()
                return WebFetchResult(
                    html=decode_response(body, response.headers.get("Content-Type")),
                    page_last_modified=response.headers.get("Last-Modified"),
                )
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(min(2**attempt, 5))
    raise RuntimeError(f"failed to fetch CBR key rate page {url}: {last_error}") from last_error


def decode_response(body: bytes, content_type: str | None) -> str:
    charset = None
    if content_type:
        for part in content_type.split(";"):
            part = part.strip()
            if part.lower().startswith("charset="):
                charset = part.split("=", 1)[1].strip()
                break
    for encoding in (charset, "utf-8", "cp1251"):
        if not encoding:
            continue
        try:
            return body.decode(encoding)
        except UnicodeDecodeError:
            continue
    return body.decode("utf-8", errors="replace")


def parse_cbr_key_rate_html(html: str) -> ParserResult:
    """Parse CBR key rate HTML using table.data with Highcharts fallback/cross-check."""
    table_observations = parse_table_data(html)
    chart_observations = parse_highcharts_data(html)

    if table_observations:
        if chart_observations:
            cross_check_observations(table_observations, chart_observations)
        return ParserResult(table_observations, "html_table")
    if chart_observations:
        return ParserResult(chart_observations, "highcharts_fallback")
    raise ValueError("CBR key rate HTML contains neither valid table.data nor Highcharts data.")


def parse_table_data(html: str) -> list[KeyRateObservation] | None:
    parser = CbrTableParser()
    parser.feed(html)
    if len(parser.tables) > 1:
        raise ValueError(f"Expected exactly one table.data, found {len(parser.tables)}.")
    if not parser.tables:
        return None

    rows = parser.tables[0]
    if not rows:
        raise ValueError("CBR table.data is empty.")
    headers = tuple(rows[0][:2])
    if headers != TABLE_HEADERS:
        raise ValueError(f"Unexpected CBR table.data headers: {headers!r}.")

    observations = [
        KeyRateObservation(parse_source_date(row[0]), parse_rate_value(row[1]))
        for row in rows[1:]
        if len(row) >= 2 and row[0] and row[1]
    ]
    return validate_observations(observations)


def parse_highcharts_data(html: str) -> list[KeyRateObservation] | None:
    categories_match = re.search(
        r"(?:xAxis\s*:\s*\{[^{}]*?categories|xAxis\.categories)\s*[:=]\s*(\[[^\]]*\])",
        html,
        flags=re.DOTALL,
    )
    data_match = re.search(
        r"(?:series\s*:\s*\[\s*\{[^{}]*?data|series\s*\[\s*0\s*\]\.data)\s*[:=]\s*(\[[^\]]*\])",
        html,
        flags=re.DOTALL,
    )
    if not categories_match or not data_match:
        return None

    categories = parse_js_array(categories_match.group(1))
    values = parse_js_array(data_match.group(1))
    if len(categories) != len(values):
        raise ValueError("Highcharts categories/data arrays have different lengths.")
    observations = [
        KeyRateObservation(parse_source_date(category), parse_rate_value(value))
        for category, value in zip(categories, values, strict=True)
    ]
    return validate_observations(observations)


def parse_js_array(value: str) -> list[Any]:
    cleaned = re.sub(r",\s*]", "]", value.strip())
    try:
        parsed = ast.literal_eval(cleaned)
    except (SyntaxError, ValueError) as exc:
        raise ValueError("Failed to parse Highcharts array.") from exc
    if not isinstance(parsed, list):
        raise ValueError("Highcharts value is not an array.")
    return parsed


def validate_observations(observations: list[KeyRateObservation]) -> list[KeyRateObservation]:
    if not observations:
        raise ValueError("CBR key rate observations are empty.")
    dates = [observation.date for observation in observations]
    duplicates = sorted({item.isoformat() for item in dates if dates.count(item) > 1})
    if duplicates:
        raise ValueError(f"CBR key rate observations contain duplicate dates: {', '.join(duplicates)}")
    return sorted(observations, key=lambda item: item.date)


def latest_available(observations: list[KeyRateObservation]) -> LatestAvailable:
    if not observations:
        raise ValueError("CBR key rate observations are empty.")
    latest = max(observations, key=lambda item: item.date)
    return LatestAvailable(latest.date, latest.value)


def check_mode_for_to_date(to_date: date, today: date | None = None) -> str:
    today = today or date.today()
    if to_date < today:
        return "historical_range"
    return "freshness"


def cross_check_observations(
    table_observations: list[KeyRateObservation],
    chart_observations: list[KeyRateObservation],
) -> None:
    if len(table_observations) != len(chart_observations):
        raise ValueError(
            "CBR table.data and Highcharts row counts differ: "
            f"{len(table_observations)} != {len(chart_observations)}."
        )
    table_by_date = {item.date: item.value for item in table_observations}
    chart_by_date = {item.date: item.value for item in chart_observations}
    if min(table_by_date) != min(chart_by_date) or max(table_by_date) != max(chart_by_date):
        raise ValueError("CBR table.data and Highcharts boundary dates differ.")
    for item_date, table_value in table_by_date.items():
        chart_value = chart_by_date.get(item_date)
        if chart_value is None or abs(table_value - chart_value) > 0.000001:
            raise ValueError(f"CBR table.data and Highcharts values differ for {item_date.isoformat()}.")


def read_xlsx_key_rate(input_file: Path) -> ParserResult:
    """Read emergency XLSX fallback and ignore non-key-rate columns."""
    source = Path(input_file)
    if not source.exists():
        raise FileNotFoundError(f"CBR key rate XLSX not found: {source}")
    df = pd.read_excel(source, sheet_name=0)
    if "Дата" not in df.columns:
        raise ValueError("CBR XLSX is missing required column: Дата")
    key_rate_column = next((column for column in XLSX_KEY_RATE_COLUMNS if column in df.columns), None)
    if key_rate_column is None:
        raise ValueError("CBR XLSX is missing key rate column.")
    observations = [
        KeyRateObservation(parse_source_date(row["Дата"]), parse_rate_value(row[key_rate_column]))
        for _, row in df.loc[:, ["Дата", key_rate_column]].dropna(how="any").iterrows()
    ]
    return ParserResult(validate_observations(observations), "xlsx_fallback")


def make_daily_frame(observations: list[KeyRateObservation]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": [item.date.isoformat() for item in observations],
            "value": [item.value for item in observations],
        },
        columns=["date", "value"],
    )


def make_monthly_frame(observations: list[KeyRateObservation], to_date: date) -> pd.DataFrame:
    daily = make_daily_frame(observations)
    daily["date"] = pd.to_datetime(daily["date"])
    daily["period_month"] = daily["date"].dt.to_period("M").dt.to_timestamp()
    monthly = daily.sort_values("date").groupby("period_month", as_index=False).tail(1).copy()
    monthly["period_label"] = monthly["period_month"].map(format_ru_month_label)
    monthly["key_rate_month_end_pct"] = monthly["value"].astype(float)
    monthly["key_rate_date"] = monthly["date"].dt.strftime("%Y-%m-%d")
    monthly["key_rate_source_rule"] = "last_available_observation_in_month"
    monthly["month_end"] = monthly["period_month"] + pd.offsets.MonthEnd(0)
    requested_to = pd.Timestamp(to_date)
    monthly["key_rate_month_is_partial"] = monthly["month_end"] > requested_to
    monthly["period_month"] = monthly["period_month"].dt.strftime("%Y-%m-01")
    return monthly[
        [
            "period_month",
            "period_label",
            "key_rate_month_end_pct",
            "key_rate_date",
            "key_rate_source_rule",
            "key_rate_month_is_partial",
        ]
    ].reset_index(drop=True)


def format_ru_month_label(value: object) -> str:
    value_text = "" if value is None else str(value)
    timestamp = pd.to_datetime(value_text, errors="coerce")
    if pd.isna(timestamp):
        return ""
    return f"{RU_MONTH_ABBR[int(timestamp.month)]}-{str(int(timestamp.year))[-2:]}"


def source_type_for_result(source: str, parser: str) -> str:
    if source == "web" and parser == "html_table":
        return "web_table_data"
    if source == "web" and parser == "highcharts_fallback":
        return "web_highcharts_fallback"
    if source == "html-file":
        return "html_fixture"
    if source == "xlsx":
        return "xlsx_fallback"
    return source


def source_rule_for_result(source_type: str, parser: str) -> str:
    if source_type == "web_table_data" and parser == "html_table":
        return "exact_daily_site_rows"
    if parser == "highcharts_fallback":
        return "highcharts_fallback_rows"
    if source_type == "xlsx_fallback":
        return "xlsx_fallback_rows"
    if source_type == "html_fixture":
        return "fixture_daily_rows"
    return "daily_rows"


def build_metadata(
    *,
    source_url: str,
    source_type: str,
    source_file: str | None = None,
    from_date: date,
    to_date: date,
    retrieved_at: datetime,
    page_last_modified: str | None,
    html: str | None,
    row_count: int,
    parser: str,
    latest_available_date: date | None = None,
    latest_available_value: float | None = None,
    source_rule: str | None = None,
    sha256: str | None = None,
) -> dict[str, Any]:
    return {
        "source_url": source_url,
        "source_type": source_type,
        "source_file": source_file,
        "from_date": from_date.isoformat(),
        "to_date": to_date.isoformat(),
        "requested_to_date": to_date.isoformat(),
        "latest_available_date": latest_available_date.isoformat() if latest_available_date else None,
        "latest_available_value": latest_available_value,
        "retrieved_at": retrieved_at.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "page_last_modified": page_last_modified,
        "html_sha256": hashlib.sha256(html.encode("utf-8")).hexdigest() if html is not None else None,
        "row_count": row_count,
        "parser": parser,
        "source_rule": source_rule or source_rule_for_result(source_type, parser),
        "sha256": sha256,
        "source_parser": parser,
    }


def write_outputs(
    *,
    daily: pd.DataFrame,
    monthly: pd.DataFrame,
    metadata: dict[str, Any],
    daily_output_csv: Path,
    daily_meta_json: Path,
    monthly_output_csv: Path,
) -> None:
    daily_output_csv.parent.mkdir(parents=True, exist_ok=True)
    monthly_output_csv.parent.mkdir(parents=True, exist_ok=True)
    daily_meta_json.parent.mkdir(parents=True, exist_ok=True)
    daily.to_csv(daily_output_csv, index=False, encoding="utf-8")
    daily_meta_json.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    monthly.to_csv(monthly_output_csv, index=False, encoding="utf-8")


def daily_csv_bytes(daily: pd.DataFrame) -> bytes:
    if list(daily.columns) != ["date", "value"]:
        raise ValueError("CBR key rate daily CSV must contain exactly date,value columns.")
    return daily.to_csv(index=False, lineterminator="\n").encode("utf-8")


def raw_paths(output_root: Path) -> dict[str, Path]:
    root = Path(output_root)
    return {
        "latest_dir": root / "latest",
        "versions_dir": root / "versions",
        "registry_dir": root / "registry",
        "latest_csv": root / "latest" / LATEST_DAILY_NAME,
        "latest_meta": root / "latest" / LATEST_META_NAME,
        "registry_csv": root / "registry" / REGISTRY_CSV_NAME,
        "registry_latest_json": root / "registry" / REGISTRY_LATEST_JSON_NAME,
    }


def relative_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(config.PROJECT_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def write_raw_outputs(
    *,
    daily: pd.DataFrame,
    metadata: dict[str, Any],
    output_root: Path,
) -> RawWriteResult:
    paths = raw_paths(output_root)
    csv_bytes = daily_csv_bytes(daily)
    sha256 = hashlib.sha256(csv_bytes).hexdigest()
    existing_sha256 = hashlib.sha256(paths["latest_csv"].read_bytes()).hexdigest() if paths["latest_csv"].exists() else ""
    content_changed = existing_sha256 != sha256

    metadata = dict(metadata)
    metadata["sha256"] = sha256
    metadata["row_count"] = int(len(daily))

    from_label = str(metadata["from_date"])
    to_label = str(metadata["to_date"])
    version_csv = paths["versions_dir"] / f"cbr_key_rate_daily_{from_label}_{to_label}_{sha256[:12]}.csv"
    version_meta = paths["versions_dir"] / f"cbr_key_rate_daily_{from_label}_{to_label}_{sha256[:12]}.meta.json"

    for directory_key in ("latest_dir", "versions_dir", "registry_dir"):
        paths[directory_key].mkdir(parents=True, exist_ok=True)

    status = "changed"
    if content_changed:
        paths["latest_csv"].write_bytes(csv_bytes)
        paths["latest_meta"].write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        version_csv.write_bytes(csv_bytes)
        version_meta.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    elif not paths["latest_meta"].exists():
        status = "metadata_repaired"
        paths["latest_meta"].write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        version_csv = None
        version_meta = None
    else:
        status = "unchanged"
        version_csv = None
        version_meta = None

    write_registry(
        daily=daily,
        metadata=metadata,
        sha256=sha256,
        status=status,
        latest_csv=paths["latest_csv"],
        version_csv=version_csv,
        registry_csv=paths["registry_csv"],
        registry_latest_json=paths["registry_latest_json"],
    )
    return RawWriteResult(
        status=status,
        sha256=sha256,
        latest_csv=paths["latest_csv"],
        latest_meta=paths["latest_meta"],
        version_csv=version_csv,
        version_meta=version_meta,
        registry_csv=paths["registry_csv"],
        registry_latest_json=paths["registry_latest_json"],
    )


def write_registry(
    *,
    daily: pd.DataFrame,
    metadata: dict[str, Any],
    sha256: str,
    status: str,
    latest_csv: Path,
    version_csv: Path | None,
    registry_csv: Path,
    registry_latest_json: Path,
) -> None:
    latest_row = daily.sort_values("date").iloc[-1]
    version_path_value = relative_path(version_csv) if version_csv else existing_registry_version_path(registry_csv, sha256)
    record = {
        "source_name": "cbr_key_rate_daily",
        "source_type": metadata.get("source_type"),
        "from_date": metadata.get("from_date"),
        "to_date": metadata.get("to_date"),
        "latest_date": str(latest_row["date"]),
        "latest_value": float(latest_row["value"]),
        "row_count": int(len(daily)),
        "sha256": sha256,
        "latest_path": relative_path(latest_csv),
        "version_path": version_path_value,
        "retrieved_at": metadata.get("retrieved_at"),
        "source_url": metadata.get("source_url"),
        "parser": metadata.get("parser"),
        "is_active": True,
        "status": status,
    }
    if registry_csv.exists():
        existing = pd.read_csv(registry_csv)
        existing["is_active"] = False
        registry = pd.concat([existing, pd.DataFrame([record])], ignore_index=True)
    else:
        registry = pd.DataFrame([record])
    registry.to_csv(registry_csv, index=False, encoding="utf-8", lineterminator="\n")
    registry_latest_json.write_text(
        json.dumps({"record": record, "metadata": metadata}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def existing_registry_version_path(registry_csv: Path, sha256: str) -> str:
    if not registry_csv.exists():
        return ""
    try:
        registry = pd.read_csv(registry_csv)
    except Exception:
        return ""
    if not {"sha256", "version_path"}.issubset(registry.columns):
        return ""
    matches = registry.loc[
        (registry["sha256"].astype(str) == sha256)
        & registry["version_path"].fillna("").astype(str).ne("")
    ]
    if matches.empty:
        return ""
    return str(matches.iloc[-1]["version_path"])


def run(args: argparse.Namespace) -> int:
    from_date = parse_cbr_query_date(args.from_date)
    to_date = parse_cbr_query_date(args.to_date)
    if from_date > to_date:
        raise ValueError("--from-date must be less than or equal to --to-date.")

    source_url = args.url or build_cbr_key_rate_url(args.from_date, args.to_date)
    source_type = "web"
    source_file: str | None = None
    retrieved_at = datetime.now(UTC)
    page_last_modified = None
    html: str | None = None

    if args.source == "web":
        fetched = fetch_web_page(source_url, args.timeout_seconds, args.retries, args.user_agent)
        html = fetched.html
        page_last_modified = fetched.page_last_modified
        result = parse_cbr_key_rate_html(html)
    elif args.source == "html-file":
        if args.html_file is None:
            raise ValueError("--html-file is required when --source html-file.")
        source_type = "html_fixture"
        source_file = Path(args.html_file).as_posix()
        html = Path(args.html_file).read_text(encoding="utf-8")
        result = parse_cbr_key_rate_html(html)
    elif args.source == "xlsx":
        if args.input_file is None:
            raise ValueError("--input-file is required when --source xlsx.")
        source_type = "xlsx_fallback"
        source_file = Path(args.input_file).as_posix()
        source_url = ""
        result = read_xlsx_key_rate(Path(args.input_file))
    else:
        raise ValueError(f"Unsupported CBR source: {args.source}")

    daily = make_daily_frame(result.observations)
    latest_on_site = latest_available(result.observations)
    check_mode = check_mode_for_to_date(to_date)
    source_type = source_type_for_result(args.source, result.parser)
    source_rule = source_rule_for_result(source_type, result.parser)
    metadata = build_metadata(
        source_url=source_url,
        source_type=source_type,
        source_file=source_file,
        from_date=from_date,
        to_date=to_date,
        retrieved_at=retrieved_at,
        page_last_modified=page_last_modified,
        html=html,
        row_count=len(daily),
        parser=result.parser,
        latest_available_date=latest_on_site.date,
        latest_available_value=latest_on_site.value,
        source_rule=source_rule,
    )

    if args.dry_run and args.download:
        raise ValueError("--dry-run cannot be combined with --download.")
    if args.download and args.confirm != CONFIRM_TOKEN:
        raise ValueError(f"--download requires --confirm {CONFIRM_TOKEN}.")

    if args.save_html_snapshot and html is not None and args.download:
        snapshot_path = Path(args.save_html_snapshot)
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot_path.write_text(html, encoding="utf-8")

    write_result: RawWriteResult | None = None
    if args.download:
        write_result = write_raw_outputs(
            daily=daily,
            metadata=metadata,
            output_root=Path(args.output_root),
        )

    print(
        "CBR key rate parser completed: "
        f"source={args.source}, source_type={source_type}, parser={result.parser}, rows={len(daily)}, "
        f"from={daily['date'].min()}, to={daily['date'].max()}, "
        f"requested_from_date={from_date.isoformat()}, requested_to_date={to_date.isoformat()}, "
        f"latest_available_date={latest_on_site.date.isoformat()}, "
        f"latest_available_value={latest_on_site.value:.2f}, check_mode={check_mode}, "
        f"dry_run={not args.download}"
    )
    if write_result is not None:
        status_label = (
            "Данные Банка России не изменились"
            if write_result.status == "unchanged"
            else "Данные Банка России обновлены"
        )
        print(
            f"{status_label}: write_status={write_result.status}, sha256={write_result.sha256}, "
            f"latest_csv={write_result.latest_csv}, latest_meta={write_result.latest_meta}, "
            f"version_csv={write_result.version_csv or '-'}, registry={write_result.registry_csv}"
        )
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch and normalize Bank of Russia key rate data.")
    parser.add_argument("--source", choices=["web", "html-file", "xlsx"], default="web")
    parser.add_argument("--from-date", default=DEFAULT_FROM_DATE, help="Start date in DD.MM.YYYY format.")
    parser.add_argument("--to-date", default=default_to_date(), help="End date in DD.MM.YYYY format; default is today.")
    parser.add_argument("--url", help="Override the CBR KeyRate URL.")
    parser.add_argument("--html-file", type=Path, help="Parse a saved CBR KeyRate HTML page.")
    parser.add_argument("--input-file", type=Path, help="Emergency XLSX fallback file.")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT, help="Raw CBR key rate output root.")
    parser.add_argument("--daily-output-csv", type=Path, default=DEFAULT_DAILY_OUTPUT_CSV, help=argparse.SUPPRESS)
    parser.add_argument("--daily-meta-json", type=Path, default=DEFAULT_DAILY_META_JSON, help=argparse.SUPPRESS)
    parser.add_argument("--monthly-output-csv", type=Path, default=DEFAULT_MONTHLY_OUTPUT_CSV, help=argparse.SUPPRESS)
    parser.add_argument("--dry-run", action="store_true", help="Parse and validate without writing outputs.")
    parser.add_argument("--download", action="store_true", help="Write controlled raw latest/version/registry outputs.")
    parser.add_argument("--confirm", default="", help=f"Required confirmation token for --download: {CONFIRM_TOKEN}.")
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    parser.add_argument(
        "--save-html-snapshot",
        nargs="?",
        const=DEFAULT_HTML_SNAPSHOT,
        type=Path,
        help="Save fetched HTML to the optional path; ignored in dry-run.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
