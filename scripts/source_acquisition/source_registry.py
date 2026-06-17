"""Registry-facing types and read/write helpers for Minfin source acquisition."""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any


REGISTRY_FIELDS = [
    "source_name",
    "source_url",
    "page_title",
    "link_text",
    "file_name",
    "year",
    "publication_period",
    "downloaded_at",
    "source_last_modified",
    "http_etag",
    "http_last_modified",
    "file_size_bytes",
    "sha256",
    "storage_role",
    "is_active_for_pipeline",
    "supersedes_sha256",
    "change_detected",
    "notes",
    "section_id",
    "page_param",
    "page_number",
    "document_id",
    "document_page_url",
    "document_title",
    "published_at",
    "modified_at",
    "as_of_date",
    "file_url",
    "absolute_file_url",
    "file_title",
    "file_info",
    "file_size_text",
    "discovery_method",
    "pagination_page_count",
]

STORAGE_ROLES = {"latest", "version_snapshot", "final", "manual_candidate", "observation"}
PUBLICATION_PERIODS = {"monthly", "annual-final", "manual-import", "unknown"}
DISCOVERY_METHODS = {"html", "manual-import", "observation"}


@dataclass(frozen=True)
class SourceDocumentRecord:
    section_id: int
    page_param: str
    page_number: int
    document_id: str | None
    document_page_url: str | None
    document_title: str
    document_type: str | None
    published_at: str | None
    modified_at: str | None
    tags: tuple[str, ...]
    file_url: str
    absolute_file_url: str
    file_name: str
    file_title: str | None
    file_info: str | None
    file_size_text: str | None
    file_extension: str
    as_of_date: str | None
    discovery_method: str = "html"

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["tags"] = list(self.tags)
        return result


@dataclass(frozen=True)
class AcquisitionPlan:
    year: int
    mode: str
    dry_run: bool
    download_requested: bool
    source_url: str
    selected_candidate: dict[str, object] | None
    candidate_count: int
    warnings: tuple[str, ...]
    planned_paths: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["warnings"] = list(self.warnings)
        return result


@dataclass(frozen=True)
class RegistryRecord:
    source_name: str
    source_url: str
    page_title: str
    link_text: str
    file_name: str
    year: int
    publication_period: str
    downloaded_at: str
    source_last_modified: str | None
    http_etag: str | None
    http_last_modified: str | None
    file_size_bytes: int
    sha256: str
    storage_role: str
    is_active_for_pipeline: bool
    supersedes_sha256: str | None
    change_detected: bool
    notes: str | None
    section_id: int | None
    page_param: str | None
    page_number: int | None
    document_id: str | None
    document_page_url: str | None
    document_title: str | None
    published_at: str | None
    modified_at: str | None
    as_of_date: str | None
    file_url: str | None
    absolute_file_url: str | None
    file_title: str | None
    file_info: str | None
    file_size_text: str | None
    discovery_method: str
    pagination_page_count: int | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RegistryStatus:
    ok: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    record_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["errors"] = list(self.errors)
        result["warnings"] = list(self.warnings)
        return result


def _parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def _parse_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _normalize_record_dict(row: dict[str, Any]) -> dict[str, Any]:
    normalized = {field: row.get(field) for field in REGISTRY_FIELDS}
    normalized["year"] = int(normalized["year"])
    normalized["file_size_bytes"] = int(normalized["file_size_bytes"])
    normalized["is_active_for_pipeline"] = _parse_bool(normalized["is_active_for_pipeline"])
    normalized["change_detected"] = _parse_bool(normalized["change_detected"])
    normalized["section_id"] = _parse_int(normalized["section_id"])
    normalized["page_number"] = _parse_int(normalized["page_number"])
    normalized["pagination_page_count"] = _parse_int(normalized["pagination_page_count"])
    for field in REGISTRY_FIELDS:
        if normalized[field] == "":
            normalized[field] = None
    return normalized


def _record_from_dict(row: dict[str, Any]) -> RegistryRecord:
    return RegistryRecord(**_normalize_record_dict(row))


def _csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def compute_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def get_file_size(path: str | Path) -> int:
    return Path(path).stat().st_size


def load_registry_csv(path: str | Path) -> list[RegistryRecord]:
    registry_path = Path(path)
    if not registry_path.exists():
        return []
    with registry_path.open("r", encoding="utf-8", newline="") as handle:
        return [_record_from_dict(row) for row in csv.DictReader(handle)]


def load_registry_json(path: str | Path) -> list[RegistryRecord]:
    registry_path = Path(path)
    if not registry_path.exists():
        return []
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    rows = payload.get("records", payload) if isinstance(payload, dict) else payload
    return [_record_from_dict(row) for row in rows]


def write_registry_csv(path: str | Path, records: list[RegistryRecord]) -> None:
    registry_path = Path(path)
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with registry_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REGISTRY_FIELDS)
        writer.writeheader()
        for record in records:
            writer.writerow({field: _csv_value(record.to_dict().get(field)) for field in REGISTRY_FIELDS})


def write_registry_json(path: str | Path, records: list[RegistryRecord]) -> None:
    registry_path = Path(path)
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"records": [record.to_dict() for record in records]}
    registry_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def append_registry_record(path: str | Path, record: RegistryRecord) -> list[RegistryRecord]:
    registry_path = Path(path)
    records = load_registry_csv(registry_path)
    records.append(record)
    write_registry_csv(registry_path, records)
    return records


def find_active_record(
    records: list[RegistryRecord],
    year: int,
    storage_role: str,
) -> RegistryRecord | None:
    for record in records:
        if record.year == year and record.storage_role == storage_role and record.is_active_for_pipeline:
            return record
    return None


def detect_hash_change(previous_record: RegistryRecord | None, candidate_sha256: str) -> bool:
    if previous_record is None:
        return True
    return previous_record.sha256 != candidate_sha256


def mark_superseded(records: list[RegistryRecord], superseded_sha256: str) -> list[RegistryRecord]:
    updated: list[RegistryRecord] = []
    for record in records:
        if record.sha256 == superseded_sha256 and record.is_active_for_pipeline:
            updated.append(replace(record, is_active_for_pipeline=False, notes="superseded"))
        else:
            updated.append(record)
    return updated


def validate_registry_record(record: RegistryRecord) -> RegistryStatus:
    errors: list[str] = []
    warnings: list[str] = []
    if record.storage_role not in STORAGE_ROLES:
        errors.append(f"invalid storage_role: {record.storage_role}")
    if record.publication_period not in PUBLICATION_PERIODS:
        errors.append(f"invalid publication_period: {record.publication_period}")
    if record.discovery_method not in DISCOVERY_METHODS:
        errors.append(f"invalid discovery_method: {record.discovery_method}")
    if len(record.sha256) != 64:
        errors.append("sha256 must be a 64-character hex digest")
    if record.file_size_bytes < 0:
        errors.append("file_size_bytes must be non-negative")
    if record.discovery_method == "html":
        for field in ("section_id", "page_param", "document_title", "absolute_file_url"):
            if getattr(record, field) in (None, ""):
                errors.append(f"html discovery requires {field}")
    if record.discovery_method == "manual-import" and not record.notes:
        warnings.append("manual-import should include notes with original local file context")
    return RegistryStatus(ok=not errors, errors=tuple(errors), warnings=tuple(warnings), record_count=1)
