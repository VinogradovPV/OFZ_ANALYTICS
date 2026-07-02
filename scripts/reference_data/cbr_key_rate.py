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
DEFAULT_TO_DATE = "02.07.2026"
DEFAULT_USER_AGENT = "OFZ_ANALYTICS/0.1 (+https://github.com/VinogradovPV/OFZ_ANALYTICS)"
DEFAULT_DAILY_OUTPUT_CSV = config.PROCESSED_DATA_DIR / "reference" / "cbr_key_rate_daily.csv"
DEFAULT_DAILY_META_JSON = config.PROCESSED_DATA_DIR / "reference" / "cbr_key_rate_daily.meta.json"
DEFAULT_MONTHLY_OUTPUT_CSV = config.PROCESSED_DATA_DIR / "reference" / "cbr_key_rate_monthly.csv"
DEFAULT_HTML_SNAPSHOT = config.OUTPUTS_DIR / "cache" / "cbr_key_rate_page.html"

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
    timestamp = pd.to_datetime(value, errors="coerce")
    if pd.isna(timestamp):
        return ""
    return f"{RU_MONTH_ABBR[int(timestamp.month)]}-{str(int(timestamp.year))[-2:]}"


def build_metadata(
    *,
    source_url: str,
    from_date: date,
    to_date: date,
    retrieved_at: datetime,
    page_last_modified: str | None,
    html: str | None,
    row_count: int,
    parser: str,
) -> dict[str, Any]:
    return {
        "source_url": source_url,
        "from_date": from_date.isoformat(),
        "to_date": to_date.isoformat(),
        "retrieved_at": retrieved_at.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "page_last_modified": page_last_modified,
        "html_sha256": hashlib.sha256(html.encode("utf-8")).hexdigest() if html is not None else None,
        "row_count": row_count,
        "parser": parser,
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


def run(args: argparse.Namespace) -> int:
    from_date = parse_cbr_query_date(args.from_date)
    to_date = parse_cbr_query_date(args.to_date)
    if from_date > to_date:
        raise ValueError("--from-date must be less than or equal to --to-date.")

    source_url = args.url or build_cbr_key_rate_url(args.from_date, args.to_date)
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
        html = Path(args.html_file).read_text(encoding="utf-8")
        result = parse_cbr_key_rate_html(html)
    elif args.source == "xlsx":
        if args.input_file is None:
            raise ValueError("--input-file is required when --source xlsx.")
        result = read_xlsx_key_rate(Path(args.input_file))
    else:
        raise ValueError(f"Unsupported CBR source: {args.source}")

    daily = make_daily_frame(result.observations)
    monthly = make_monthly_frame(result.observations, to_date)
    metadata = build_metadata(
        source_url=source_url,
        from_date=from_date,
        to_date=to_date,
        retrieved_at=retrieved_at,
        page_last_modified=page_last_modified,
        html=html,
        row_count=len(daily),
        parser=result.parser,
    )

    if args.save_html_snapshot and html is not None and not args.dry_run:
        snapshot_path = Path(args.save_html_snapshot)
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot_path.write_text(html, encoding="utf-8")

    if not args.dry_run:
        write_outputs(
            daily=daily,
            monthly=monthly,
            metadata=metadata,
            daily_output_csv=Path(args.daily_output_csv),
            daily_meta_json=Path(args.daily_meta_json),
            monthly_output_csv=Path(args.monthly_output_csv),
        )

    print(
        "CBR key rate parser completed: "
        f"source={args.source}, parser={result.parser}, rows={len(daily)}, "
        f"from={daily['date'].min()}, to={daily['date'].max()}, dry_run={args.dry_run}"
    )
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch and normalize Bank of Russia key rate data.")
    parser.add_argument("--source", choices=["web", "html-file", "xlsx"], default="web")
    parser.add_argument("--from-date", default=DEFAULT_FROM_DATE, help="Start date in DD.MM.YYYY format.")
    parser.add_argument("--to-date", default=DEFAULT_TO_DATE, help="End date in DD.MM.YYYY format.")
    parser.add_argument("--url", help="Override the CBR KeyRate URL.")
    parser.add_argument("--html-file", type=Path, help="Parse a saved CBR KeyRate HTML page.")
    parser.add_argument("--input-file", type=Path, help="Emergency XLSX fallback file.")
    parser.add_argument("--daily-output-csv", type=Path, default=DEFAULT_DAILY_OUTPUT_CSV)
    parser.add_argument("--daily-meta-json", type=Path, default=DEFAULT_DAILY_META_JSON)
    parser.add_argument("--monthly-output-csv", type=Path, default=DEFAULT_MONTHLY_OUTPUT_CSV)
    parser.add_argument("--dry-run", action="store_true", help="Parse and validate without writing outputs.")
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
