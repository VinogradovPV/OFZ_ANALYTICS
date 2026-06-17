"""CLI skeleton for Minfin OFZ source acquisition dry-runs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scripts.source_acquisition.minfin_html_parser import (
    extract_pagination_info,
    parse_minfin_auction_table_documents,
    select_candidate,
)
from scripts.source_acquisition.minfin_patterns import (
    BASE_URL,
    DEFAULT_MAX_PAGES,
    DEFAULT_RETRIES,
    DEFAULT_SOURCE_URL,
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_USER_AGENT,
)
from scripts.source_acquisition.path_planning import build_storage_paths
from scripts.source_acquisition.source_registry import AcquisitionPlan, SourceDocumentRecord


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a dry-run plan for Minfin OFZ auction result source acquisition."
    )
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--mode", choices=["monthly", "annual-final", "manual-import"], required=True)
    parser.add_argument("--dry-run", action="store_true", help="Build a plan without mutating raw storage.")
    parser.add_argument("--download", action="store_true", help="Reserved for later P3 stages.")
    parser.add_argument("--url", default=DEFAULT_SOURCE_URL)
    parser.add_argument("--output-root", default=".")
    parser.add_argument("--manual-file")
    parser.add_argument("--no-network", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    parser.add_argument("--confirm")
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--html-file")
    parser.add_argument("--save-html-snapshot")
    return parser


def _load_html(path: str | None) -> str | None:
    if not path:
        return None
    return Path(path).read_text(encoding="utf-8")


def _records_to_dicts(records: list[SourceDocumentRecord]) -> list[dict[str, object]]:
    return [record.to_dict() for record in records]


def build_acquisition_plan(
    *,
    year: int,
    mode: str,
    dry_run: bool,
    download_requested: bool,
    source_url: str = DEFAULT_SOURCE_URL,
    output_root: str = ".",
    html: str | None = None,
    manual_file: str | None = None,
    no_network: bool = False,
) -> tuple[AcquisitionPlan, list[SourceDocumentRecord], dict[str, object] | None]:
    warnings: list[str] = []
    records: list[SourceDocumentRecord] = []
    pagination: dict[str, object] | None = None

    if download_requested:
        warnings.append("P3.1 skeleton blocks --download; production download is deferred.")

    if mode == "manual-import":
        if not manual_file:
            warnings.append("--manual-file is required for manual-import mode.")
        selected = None
    elif html:
        records = parse_minfin_auction_table_documents(html, BASE_URL, page_number=1)
        pagination = extract_pagination_info(html)
        selected_record = select_candidate(records, year, mode)
        selected = selected_record.to_dict() if selected_record else None
        if selected is None:
            warnings.append("No matching candidate found in local HTML fixture.")
    else:
        selected = None
        if no_network:
            warnings.append("No HTML file supplied and --no-network is set; discovery skipped.")
        else:
            warnings.append("Live network discovery is not implemented in P3.1 skeleton.")

    paths = build_storage_paths(output_root, year).to_dict()
    plan = AcquisitionPlan(
        year=year,
        mode=mode,
        dry_run=dry_run,
        download_requested=download_requested,
        source_url=source_url,
        selected_candidate=selected,
        candidate_count=len(records),
        warnings=tuple(warnings),
        planned_paths=paths,
    )
    return plan, records, pagination


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.download:
        print("ERROR: --download is blocked in P3.1 skeleton.", file=sys.stderr)
        return 2
    if not args.dry_run:
        print("ERROR: P3.1 supports --dry-run only.", file=sys.stderr)
        return 2
    if args.save_html_snapshot:
        print("ERROR: --save-html-snapshot is reserved for later P3 stages.", file=sys.stderr)
        return 2

    html = _load_html(args.html_file)
    plan, records, pagination = build_acquisition_plan(
        year=args.year,
        mode=args.mode,
        dry_run=args.dry_run,
        download_requested=args.download,
        source_url=args.url,
        output_root=args.output_root,
        html=html,
        manual_file=args.manual_file,
        no_network=args.no_network,
    )
    payload = {
        "plan": plan.to_dict(),
        "pagination": pagination,
        "records": _records_to_dicts(records),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

