"""CLI skeleton for Minfin OFZ source acquisition dry-runs."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
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
    IMPORT_CONFIRM_TOKEN,
    REPLACE_FINAL_CONFIRM_TOKEN,
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
    parser.add_argument("--download", action="store_true", help="Perform controlled acquisition/import with confirm token.")
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


def _validate_candidate_file(candidate: SourceDocumentRecord, year: int) -> None:
    if candidate.file_extension.lower() != "xlsx":
        raise ValueError("selected candidate is not an xlsx file")
    match = FILE_NAME_RE.match(candidate.file_name)
    if not match or match.group("year") != str(year):
        raise ValueError(f"selected candidate filename does not match year {year}: {candidate.file_name}")


def _validate_monthly_candidate(candidate: SourceDocumentRecord, year: int) -> None:
    _validate_candidate_file(candidate, year)


def _validate_annual_final_candidate(candidate: SourceDocumentRecord, year: int) -> None:
    _validate_candidate_file(candidate, year)
    if candidate.as_of_date:
        raise ValueError("selected annual-final candidate has a monthly as-of date in the title")


def _validate_manual_file(path: str | Path, year: int) -> Path:
    manual_path = Path(path)
    if not manual_path.exists():
        raise FileNotFoundError(f"manual file does not exist: {manual_path}")
    if not manual_path.is_file():
        raise ValueError(f"manual file is not a file: {manual_path}")
    if manual_path.suffix.lower() != ".xlsx":
        raise ValueError(f"manual file must be .xlsx: {manual_path}")
    match = FILE_NAME_RE.match(manual_path.name)
    if not match:
        raise ValueError(f"manual file name does not match Minfin pattern: {manual_path.name}")
    if match.group("year") != str(year):
        raise ValueError(f"manual file year does not match --year {year}: {manual_path.name}")
    return manual_path


def _manual_candidate(path: str | Path, year: int) -> SourceDocumentRecord:
    manual_path = _validate_manual_file(path, year).resolve()
    return SourceDocumentRecord(
        section_id=None,
        page_param=None,
        page_number=None,
        document_id=None,
        document_page_url=None,
        document_title=f"Manual Minfin OFZ auction results import for {year}",
        document_type="manual-import",
        published_at=None,
        modified_at=None,
        tags=(),
        file_url=str(manual_path),
        absolute_file_url=str(manual_path),
        file_name=manual_path.name,
        file_title=manual_path.name,
        file_info=None,
        file_size_text=None,
        file_extension=manual_path.suffix.lower().lstrip("."),
        as_of_date=None,
        discovery_method="manual-import",
    )


def _pagination_page_count(pagination: dict[str, object] | None) -> int | None:
    if not pagination:
        return None
    value = pagination.get("page_count")
    if value is None:
        return None
    return int(value)


def _registry_record(
    *,
    candidate: SourceDocumentRecord,
    year: int,
    publication_period: str,
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
        publication_period=publication_period,
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


def _write_report(path: str | Path, payload: dict[str, Any]) -> None:
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
) -> dict[str, Any]:
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
            publication_period="monthly",
            file_size_bytes=candidate_size,
            sha256=candidate_sha,
            storage_role="latest",
            is_active_for_pipeline=True,
            supersedes_sha256=previous.sha256 if previous else None,
            change_detected=True,
            pagination_page_count=_pagination_page_count(pagination),
            notes=f"monthly download promoted; version_snapshot={version_path}",
        )
        records.append(new_record)
        version_snapshot = str(version_path)
    else:
        new_record = _registry_record(
            candidate=candidate,
            year=year,
            publication_period="monthly",
            file_size_bytes=candidate_size,
            sha256=candidate_sha,
            storage_role="observation",
            is_active_for_pipeline=False,
            supersedes_sha256=None,
            change_detected=False,
            pagination_page_count=_pagination_page_count(pagination),
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


def _promote_annual_final_download(
    *,
    candidate: SourceDocumentRecord,
    downloaded_path: Path,
    output_root: str,
    year: int,
    pagination: dict[str, object] | None,
    replace_final: bool,
) -> dict[str, Any]:
    _validate_annual_final_candidate(candidate, year)
    paths = build_storage_paths(output_root, year).to_dict()
    final_path = Path(paths["final_path"])
    candidate_sha = compute_sha256(downloaded_path)
    candidate_size = get_file_size(downloaded_path)
    registry_path = Path(paths["registry_csv_path"])
    records = load_registry_csv(registry_path)
    previous = find_active_record(records, year, "final")
    existing_final_sha = compute_sha256(final_path) if final_path.exists() else None
    existing_sha = existing_final_sha or (previous.sha256 if previous else None)
    changed = existing_sha != candidate_sha if existing_sha else True

    if existing_sha and changed and not replace_final:
        raise RuntimeError(
            "existing annual final hash differs; manual review required with "
            "--confirm REPLACE_MINFIN_FINAL"
        )

    promoted = False
    replaced = False
    if not existing_sha:
        final_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(downloaded_path, final_path)
        promoted = True
    elif not changed:
        promoted = False
    else:
        final_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(downloaded_path, final_path)
        records = mark_superseded(records, previous.sha256) if previous else records
        promoted = True
        replaced = True

    active = promoted or replaced
    new_record = _registry_record(
        candidate=candidate,
        year=year,
        publication_period="annual-final",
        file_size_bytes=candidate_size,
        sha256=candidate_sha,
        storage_role="final",
        is_active_for_pipeline=active,
        supersedes_sha256=existing_sha if replaced else None,
        change_detected=changed,
        pagination_page_count=_pagination_page_count(pagination),
        notes=(
            "annual final promoted"
            if promoted and not replaced
            else "annual final replaced after manual confirmation"
            if replaced
            else "annual final observed unchanged; no replacement"
        ),
    )
    records.append(new_record)
    write_registry_csv(registry_path, records)
    write_registry_json(paths["registry_json_path"], records)
    payload = {
        "year": year,
        "mode": "annual-final",
        "selected_candidate": candidate.to_dict(),
        "sha256": candidate_sha,
        "file_size_bytes": candidate_size,
        "change_detected": changed,
        "final_path": paths["final_path"] if active else None,
        "existing_final_sha256": existing_sha,
        "replacement_performed": replaced,
        "registry_csv_path": paths["registry_csv_path"],
        "registry_json_path": paths["registry_json_path"],
    }
    _write_report(paths["annual_final_report_path"], payload)
    return payload


def _promote_manual_import(
    *,
    candidate: SourceDocumentRecord,
    imported_path: Path,
    original_path: Path,
    output_root: str,
    year: int,
) -> dict[str, Any]:
    _validate_candidate_file(candidate, year)
    paths = build_storage_paths(output_root, year).to_dict()
    candidate_sha = compute_sha256(imported_path)
    candidate_size = get_file_size(imported_path)
    registry_path = Path(paths["registry_csv_path"])
    records = load_registry_csv(registry_path)
    previous = find_active_record(records, year, "latest")
    changed = detect_hash_change(previous, candidate_sha)

    if changed:
        version_path = build_version_snapshot_path(output_root, year, candidate.file_name, candidate_sha)
        latest_path = Path(paths["latest_path"])
        version_path.parent.mkdir(parents=True, exist_ok=True)
        latest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(imported_path, version_path)
        shutil.copy2(imported_path, latest_path)
        records = mark_superseded(records, previous.sha256) if previous else records
        new_record = _registry_record(
            candidate=candidate,
            year=year,
            publication_period="manual-import",
            file_size_bytes=candidate_size,
            sha256=candidate_sha,
            storage_role="latest",
            is_active_for_pipeline=True,
            supersedes_sha256=previous.sha256 if previous else None,
            change_detected=True,
            pagination_page_count=None,
            notes=f"manual import promoted; original_local_file={original_path}; version_snapshot={version_path}",
        )
        records.append(new_record)
        version_snapshot = str(version_path)
    else:
        new_record = _registry_record(
            candidate=candidate,
            year=year,
            publication_period="manual-import",
            file_size_bytes=candidate_size,
            sha256=candidate_sha,
            storage_role="observation",
            is_active_for_pipeline=False,
            supersedes_sha256=None,
            change_detected=False,
            pagination_page_count=None,
            notes=f"manual import observed unchanged; original_local_file={original_path}; no copy promoted",
        )
        records.append(new_record)
        version_snapshot = None

    write_registry_csv(registry_path, records)
    write_registry_json(paths["registry_json_path"], records)
    payload = {
        "year": year,
        "mode": "manual-import",
        "selected_candidate": candidate.to_dict(),
        "sha256": candidate_sha,
        "file_size_bytes": candidate_size,
        "change_detected": changed,
        "planned_storage_role": "latest" if changed else "observation",
        "latest_path": paths["latest_path"] if changed else None,
        "version_snapshot_path": version_snapshot,
        "final_path": None,
        "registry_csv_path": paths["registry_csv_path"],
        "registry_json_path": paths["registry_json_path"],
        "original_local_file": str(original_path),
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
) -> dict[str, Any]:
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


def run_annual_final_download(
    *,
    year: int,
    source_url: str,
    output_root: str,
    timeout_seconds: int,
    retries: int,
    user_agent: str,
    max_pages: int,
    replace_final: bool = False,
    page_fetcher=fetch_page,
    file_downloader=download_file,
) -> dict[str, Any]:
    candidates, pagination = _discover_records(
        source_url=source_url,
        year=year,
        timeout_seconds=timeout_seconds,
        retries=retries,
        user_agent=user_agent,
        max_pages=max_pages,
        page_fetcher=page_fetcher,
    )
    selected = select_candidate(candidates, year, "annual-final")
    if selected is None:
        raise RuntimeError(f"no annual-final candidate found for {year}")
    _validate_annual_final_candidate(selected, year)
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
        return _promote_annual_final_download(
            candidate=selected,
            downloaded_path=Path(downloaded),
            output_root=output_root,
            year=year,
            pagination=pagination,
            replace_final=replace_final,
        )
    finally:
        if temp_path.exists():
            temp_path.unlink()


def run_manual_import(
    *,
    year: int,
    manual_file: str | Path,
    output_root: str,
) -> dict[str, Any]:
    original_path = _validate_manual_file(manual_file, year).resolve()
    candidate = _manual_candidate(original_path, year)
    paths = build_storage_paths(output_root, year).to_dict()
    temp_path = Path(paths["temp_download_path"])
    try:
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original_path, temp_path)
        return _promote_manual_import(
            candidate=candidate,
            imported_path=temp_path,
            original_path=original_path,
            output_root=output_root,
            year=year,
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
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    retries: int = DEFAULT_RETRIES,
    user_agent: str = DEFAULT_USER_AGENT,
    max_pages: int = DEFAULT_MAX_PAGES,
    page_fetcher=fetch_page,
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
        else:
            manual_path = _validate_manual_file(manual_file, year).resolve()
            candidate = _manual_candidate(manual_path, year)
            paths = build_storage_paths(output_root, year).to_dict()
            candidate_sha = compute_sha256(manual_path)
            candidate_size = get_file_size(manual_path)
            previous = find_active_record(load_registry_csv(paths["registry_csv_path"]), year, "latest")
            changed = detect_hash_change(previous, candidate_sha)
            selected = {
                **candidate.to_dict(),
                "sha256": candidate_sha,
                "file_size_bytes": candidate_size,
                "planned_storage_role": "latest" if changed else "observation",
                "planned_target_path": paths["latest_path"] if changed else None,
                "planned_version_snapshot_dir": paths["version_snapshot_dir"] if changed else None,
                "final_path": None,
                "original_local_file": str(manual_path),
            }
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
            try:
                records, pagination = _discover_records(
                    source_url=source_url,
                    year=year,
                    timeout_seconds=timeout_seconds,
                    retries=retries,
                    user_agent=user_agent,
                    max_pages=max_pages,
                    page_fetcher=page_fetcher,
                )
                selected_record = select_candidate(records, year, mode)
                selected = selected_record.to_dict() if selected_record else None
                if selected is None:
                    warnings.append("No matching candidate found during live discovery.")
            except HttpClientError as exc:
                warnings.append(f"Live discovery failed; raw unchanged: {exc}")

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
        try:
            if args.mode == "monthly":
                if args.confirm != DOWNLOAD_CONFIRM_TOKEN:
                    print("ERROR: --download requires --confirm DOWNLOAD_MINFIN_SOURCE.", file=sys.stderr)
                    return 2
                payload = run_monthly_download(
                    year=args.year,
                    source_url=args.url,
                    output_root=args.output_root,
                    timeout_seconds=args.timeout_seconds,
                    retries=args.retries,
                    user_agent=args.user_agent,
                    max_pages=args.max_pages,
                )
            elif args.mode == "annual-final":
                if args.confirm not in {DOWNLOAD_CONFIRM_TOKEN, REPLACE_FINAL_CONFIRM_TOKEN}:
                    print(
                        "ERROR: --download requires --confirm DOWNLOAD_MINFIN_SOURCE "
                        "or --confirm REPLACE_MINFIN_FINAL.",
                        file=sys.stderr,
                    )
                    return 2
                payload = run_annual_final_download(
                    year=args.year,
                    source_url=args.url,
                    output_root=args.output_root,
                    timeout_seconds=args.timeout_seconds,
                    retries=args.retries,
                    user_agent=args.user_agent,
                    max_pages=args.max_pages,
                    replace_final=args.confirm == REPLACE_FINAL_CONFIRM_TOKEN,
                )
            elif args.mode == "manual-import":
                if args.confirm != IMPORT_CONFIRM_TOKEN:
                    print("ERROR: --download requires --confirm IMPORT_MINFIN_FILE.", file=sys.stderr)
                    return 2
                if not args.manual_file:
                    print("ERROR: --manual-file is required for manual-import.", file=sys.stderr)
                    return 2
                payload = run_manual_import(
                    year=args.year,
                    manual_file=args.manual_file,
                    output_root=args.output_root,
                )
            else:
                print("ERROR: unsupported --mode for --download.", file=sys.stderr)
                return 2
        except (FileNotFoundError, HttpClientError, RuntimeError, ValueError) as exc:
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
    try:
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
            timeout_seconds=args.timeout_seconds,
            retries=args.retries,
            user_agent=args.user_agent,
            max_pages=args.max_pages,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    payload = {
        "plan": plan.to_dict(),
        "pagination": pagination,
        "records": _records_to_dicts(records),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
