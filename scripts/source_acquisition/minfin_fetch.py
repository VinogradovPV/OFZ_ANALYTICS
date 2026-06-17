"""CLI skeleton for Minfin OFZ source acquisition dry-runs."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from scripts.source_acquisition.http_client import HttpClientError, download_file, fetch_page
from scripts.source_acquisition.minfin_html_parser import (
    extract_pagination_info,
    filter_candidates,
    parse_minfin_auction_table_documents,
    select_candidate,
)
from scripts.source_acquisition.minfin_patterns import (
    BASE_URL,
    DOWNLOAD_CONFIRM_TOKEN,
    DEFAULT_MAX_PAGES,
    DEFAULT_RETRIES,
    DEFAULT_SOURCE_URL,
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_USER_AGENT,
    FILE_NAME_RE,
    TARGET_PAGE_PARAM,
)
from scripts.source_acquisition.path_planning import build_storage_paths, build_version_snapshot_path
from scripts.source_acquisition.source_registry import (
    AcquisitionPlan,
    RegistryRecord,
    SourceDocumentRecord,
    compute_sha256,
    detect_hash_change,
    find_active_record,
    get_file_size,
    load_registry_csv,
    mark_superseded,
    write_registry_csv,
    write_registry_json,
)


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


def _page_url(base_url: str, page_number: int) -> str:
    split = urlsplit(base_url)
    query = dict(parse_qsl(split.query, keep_blank_values=True))
    query[TARGET_PAGE_PARAM] = str(page_number)
    return urlunsplit((split.scheme, split.netloc, split.path, urlencode(query), ""))


def _base_page_url(source_url: str) -> str:
    split = urlsplit(source_url)
    return urlunsplit((split.scheme, split.netloc, split.path, split.query, ""))


def _discover_records(
    *,
    source_url: str,
    year: int,
    timeout_seconds: int,
    retries: int,
    user_agent: str,
    max_pages: int,
    page_fetcher=fetch_page,
) -> tuple[list[SourceDocumentRecord], dict[str, object] | None]:
    base_url = _base_page_url(source_url)
    first_html = page_fetcher(base_url, timeout_seconds, retries, user_agent)
    pagination = extract_pagination_info(first_html)
    records = parse_minfin_auction_table_documents(first_html, BASE_URL, page_number=1)
    page_count = pagination.get("page_count")
    if isinstance(page_count, int) and page_count > 1:
        last_page = min(page_count, max_pages)
    else:
        last_page = 1
    for page_number in range(2, last_page + 1):
        page_html = page_fetcher(_page_url(base_url, page_number), timeout_seconds, retries, user_agent)
        records.extend(parse_minfin_auction_table_documents(page_html, BASE_URL, page_number=page_number))
    candidates = filter_candidates(records, year)
    deduped: dict[tuple[str | None, str], SourceDocumentRecord] = {}
    for record in candidates:
        deduped[(record.document_id, record.file_url)] = record
    return list(deduped.values()), pagination


def _validate_monthly_candidate(candidate: SourceDocumentRecord, year: int) -> None:
    if candidate.file_extension.lower() != "xlsx":
        raise ValueError("selected candidate is not an xlsx file")
    match = FILE_NAME_RE.match(candidate.file_name)
    if not match or match.group("year") != str(year):
        raise ValueError(f"selected candidate filename does not match year {year}: {candidate.file_name}")


def _registry_record(
    *,
    candidate: SourceDocumentRecord,
    year: int,
    file_size_bytes: int,
    sha256: str,
    storage_role: str,
    is_active_for_pipeline: bool,
    supersedes_sha256: str | None,
    change_detected: bool,
    pagination_page_count: int | None,
    notes: str,
) -> RegistryRecord:
    return RegistryRecord(
        source_name="minfin_ofz_auction_results",
        source_url=candidate.absolute_file_url,
        page_title="Минфин России :: Аукционы",
        link_text=candidate.file_title or candidate.file_name,
        file_name=candidate.file_name,
        year=year,
        publication_period="monthly",
        downloaded_at=datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        source_last_modified=candidate.modified_at,
        http_etag=None,
        http_last_modified=None,
        file_size_bytes=file_size_bytes,
        sha256=sha256,
        storage_role=storage_role,
        is_active_for_pipeline=is_active_for_pipeline,
        supersedes_sha256=supersedes_sha256,
        change_detected=change_detected,
        notes=notes,
        section_id=candidate.section_id,
        page_param=candidate.page_param,
        page_number=candidate.page_number,
        document_id=candidate.document_id,
        document_page_url=candidate.document_page_url,
        document_title=candidate.document_title,
        published_at=candidate.published_at,
        modified_at=candidate.modified_at,
        as_of_date=candidate.as_of_date,
        file_url=candidate.file_url,
        absolute_file_url=candidate.absolute_file_url,
        file_title=candidate.file_title,
        file_info=candidate.file_info,
        file_size_text=candidate.file_size_text,
        discovery_method=candidate.discovery_method,
        pagination_page_count=pagination_page_count,
    )


def _write_report(path: str | Path, payload: dict[str, object]) -> None:
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def _promote_monthly_download(
    *,
    candidate: SourceDocumentRecord,
    downloaded_path: Path,
    output_root: str,
    year: int,
    pagination: dict[str, object] | None,
) -> dict[str, object]:
    _validate_monthly_candidate(candidate, year)
    paths = build_storage_paths(output_root, year).to_dict()
    candidate_sha = compute_sha256(downloaded_path)
    candidate_size = get_file_size(downloaded_path)
    registry_path = Path(paths["registry_csv_path"])
    records = load_registry_csv(registry_path)
    previous = find_active_record(records, year, "latest")
    changed = detect_hash_change(previous, candidate_sha)

    if changed:
        version_path = build_version_snapshot_path(output_root, year, candidate.file_name, candidate_sha)
        latest_path = Path(paths["latest_path"])
        version_path.parent.mkdir(parents=True, exist_ok=True)
        latest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(downloaded_path, version_path)
        shutil.copy2(downloaded_path, latest_path)
        records = mark_superseded(records, previous.sha256) if previous else records
        new_record = _registry_record(
            candidate=candidate,
            year=year,
            file_size_bytes=candidate_size,
            sha256=candidate_sha,
            storage_role="latest",
            is_active_for_pipeline=True,
            supersedes_sha256=previous.sha256 if previous else None,
            change_detected=True,
            pagination_page_count=pagination.get("page_count") if pagination else None,
            notes=f"monthly download promoted; version_snapshot={version_path}",
        )
        records.append(new_record)
        version_snapshot = str(version_path)
    else:
        new_record = _registry_record(
            candidate=candidate,
            year=year,
            file_size_bytes=candidate_size,
            sha256=candidate_sha,
            storage_role="observation",
            is_active_for_pipeline=False,
            supersedes_sha256=None,
            change_detected=False,
            pagination_page_count=pagination.get("page_count") if pagination else None,
            notes="monthly download observed unchanged; no version snapshot created",
        )
        records.append(new_record)
        version_snapshot = None

    write_registry_csv(registry_path, records)
    write_registry_json(paths["registry_json_path"], records)
    payload = {
        "year": year,
        "mode": "monthly",
        "selected_candidate": candidate.to_dict(),
        "sha256": candidate_sha,
        "file_size_bytes": candidate_size,
        "change_detected": changed,
        "latest_path": paths["latest_path"] if changed else None,
        "version_snapshot_path": version_snapshot,
        "registry_csv_path": paths["registry_csv_path"],
        "registry_json_path": paths["registry_json_path"],
    }
    _write_report(paths["report_path"], payload)
    return payload


def run_monthly_download(
    *,
    year: int,
    source_url: str,
    output_root: str,
    timeout_seconds: int,
    retries: int,
    user_agent: str,
    max_pages: int,
    page_fetcher=fetch_page,
    file_downloader=download_file,
) -> dict[str, object]:
    candidates, pagination = _discover_records(
        source_url=source_url,
        year=year,
        timeout_seconds=timeout_seconds,
        retries=retries,
        user_agent=user_agent,
        max_pages=max_pages,
        page_fetcher=page_fetcher,
    )
    selected = select_candidate(candidates, year, "monthly")
    if selected is None:
        raise RuntimeError(f"no monthly candidate found for {year}")
    _validate_monthly_candidate(selected, year)
    paths = build_storage_paths(output_root, year).to_dict()
    temp_path = Path(paths["temp_download_path"])
    try:
        downloaded = file_downloader(
            selected.absolute_file_url,
            temp_path,
            timeout_seconds,
            retries,
            user_agent,
        )
        return _promote_monthly_download(
            candidate=selected,
            downloaded_path=Path(downloaded),
            output_root=output_root,
            year=year,
            pagination=pagination,
        )
    finally:
        if temp_path.exists():
            temp_path.unlink()


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
        warnings.append("Download requires --confirm DOWNLOAD_MINFIN_SOURCE and is not part of dry-run planning.")

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
        if args.confirm != DOWNLOAD_CONFIRM_TOKEN:
            print("ERROR: --download requires --confirm DOWNLOAD_MINFIN_SOURCE.", file=sys.stderr)
            return 2
        if args.mode != "monthly":
            print("ERROR: P3.3 implements --download only for --mode monthly.", file=sys.stderr)
            return 2
        try:
            payload = run_monthly_download(
                year=args.year,
                source_url=args.url,
                output_root=args.output_root,
                timeout_seconds=args.timeout_seconds,
                retries=args.retries,
                user_agent=args.user_agent,
                max_pages=args.max_pages,
            )
        except (HttpClientError, RuntimeError, ValueError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if not args.dry_run:
        print("ERROR: use --dry-run or --download.", file=sys.stderr)
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
