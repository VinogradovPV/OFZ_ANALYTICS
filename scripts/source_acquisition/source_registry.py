"""Registry-facing types for Minfin source acquisition.

P3.1 defines the record shape used by parser and dry-run output. Persistent
CSV/JSON registry writing is intentionally deferred to P3.2.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


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

