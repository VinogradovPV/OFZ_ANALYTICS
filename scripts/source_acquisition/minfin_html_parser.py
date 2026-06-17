"""HTML-aware parser for Minfin OFZ auction result table documents."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import PurePosixPath
from urllib.parse import parse_qs, urljoin, urlparse

from scripts.source_acquisition.minfin_patterns import (
    AS_OF_DATE_RE,
    BASE_URL,
    FILE_NAME_RE,
    TARGET_CONTAINER_ID,
    TARGET_DOCUMENT_ID_PARAM,
    TARGET_PAGE_PARAM,
    TARGET_PAGINATION_ID,
    TARGET_SECTION_ID,
)
from scripts.source_acquisition.source_registry import SourceDocumentRecord


def _attrs_to_dict(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
    return {key: value or "" for key, value in attrs}


def _class_set(attrs: dict[str, str]) -> set[str]:
    return set(attrs.get("class", "").split())


def _clean_text(value: str) -> str:
    return " ".join(value.split())


@dataclass
class _FileItem:
    href: str
    title: str | None = None
    text_parts: list[str] | None = None

    def text(self) -> str:
        return _clean_text(" ".join(self.text_parts or []))


@dataclass
class _DocumentCard:
    attrs: dict[str, str]
    text_parts: list[str]
    document_title: str | None = None
    document_title_from_attr: bool = False
    document_type: str | None = None
    date_texts: list[str] | None = None
    file_items: list[_FileItem] | None = None
    tags: list[str] | None = None


class _SectionParser(HTMLParser):
    def __init__(self, container_id: str) -> None:
        super().__init__(convert_charrefs=True)
        self.container_id = container_id
        self.in_target = False
        self.target_depth = 0
        self.div_stack: list[dict[str, object]] = []
        self.cards: list[_DocumentCard] = []
        self.current_card: _DocumentCard | None = None
        self.current_file: _FileItem | None = None
        self.capture: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = _attrs_to_dict(attrs)
        classes = _class_set(attr)
        if tag == "div":
            starts_target = attr.get("id") == self.container_id
            if starts_target and not self.in_target:
                self.in_target = True
                self.target_depth = 1
            elif self.in_target:
                self.target_depth += 1
            self.div_stack.append({"attrs": attr, "classes": classes})
            if self.in_target and "document_card" in classes:
                self.current_card = _DocumentCard(
                    attrs=attr,
                    text_parts=[],
                    date_texts=[],
                    file_items=[],
                    tags=[],
                )
            return

        if not self.in_target or self.current_card is None:
            return

        if tag == "a":
            if "file_item" in classes:
                self.current_file = _FileItem(
                    href=attr.get("href", ""),
                    title=attr.get("title") or None,
                    text_parts=[],
                )
                self.capture = "file"
            elif "document_title" in classes:
                self.current_card.document_title = attr.get("title") or None
                self.current_card.document_title_from_attr = bool(attr.get("title"))
                self.capture = "document_title"
            elif "document_type" in classes:
                self.capture = "document_type"
            elif "tag" in classes:
                self.capture = "tag"
        elif tag == "span" and "date" in classes:
            self.capture = "date"

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.current_file is not None:
            assert self.current_card is not None
            self.current_card.file_items = self.current_card.file_items or []
            self.current_card.file_items.append(self.current_file)
            self.current_file = None
            self.capture = None
            return

        if tag == "a" or tag == "span":
            self.capture = None

        if tag == "div":
            if self.current_card is not None and self.div_stack:
                top = self.div_stack[-1]
                if "document_card" in top.get("classes", set()):
                    self.cards.append(self.current_card)
                    self.current_card = None
                    self.capture = None
            if self.div_stack:
                self.div_stack.pop()
            if self.in_target:
                self.target_depth -= 1
                if self.target_depth <= 0:
                    self.in_target = False
                    self.target_depth = 0

    def handle_data(self, data: str) -> None:
        text = _clean_text(data)
        if not text or self.current_card is None:
            return
        if self.current_file is not None:
            self.current_file.text_parts = self.current_file.text_parts or []
            self.current_file.text_parts.append(text)
            return
        if self.capture == "document_title":
            if not self.current_card.document_title_from_attr:
                self.current_card.document_title = _clean_text(
                    " ".join([self.current_card.document_title or "", text])
                )
        elif self.capture == "document_type":
            self.current_card.document_type = text
        elif self.capture == "date":
            self.current_card.date_texts = self.current_card.date_texts or []
            self.current_card.date_texts.append(text)
        elif self.capture == "tag":
            self.current_card.tags = self.current_card.tags or []
            self.current_card.tags.append(text)
        self.current_card.text_parts.append(text)


class _PaginationParser(HTMLParser):
    def __init__(self, pagination_id: str) -> None:
        super().__init__(convert_charrefs=True)
        self.pagination_id = pagination_id
        self.attrs: dict[str, str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = _attrs_to_dict(attrs)
        if attr.get("id") == self.pagination_id:
            self.attrs = attr


def resolve_file_url(base_url: str, href: str) -> str:
    if not href:
        return ""
    return urljoin(base_url or BASE_URL, href)


def parse_as_of_date_from_title(title: str) -> str | None:
    match = AS_OF_DATE_RE.search(title or "")
    if not match:
        return None
    return match.group("date")


def parse_document_dates(card: _DocumentCard) -> tuple[str | None, str | None]:
    published_at = None
    modified_at = None
    for value in card.date_texts or []:
        normalized = _clean_text(value)
        if "Опубликовано:" in normalized:
            published_at = normalized.split("Опубликовано:", 1)[1].strip()
        elif "Изменено:" in normalized:
            modified_at = normalized.split("Изменено:", 1)[1].strip()
    return published_at, modified_at


def _extract_document_id(card: _DocumentCard) -> str | None:
    data_href = card.attrs.get("data-href") or card.attrs.get("href") or ""
    if not data_href:
        return None
    query = parse_qs(urlparse(data_href).query)
    values = query.get(TARGET_DOCUMENT_ID_PARAM)
    return values[0] if values else None


def _record_sort_date(value: str | None) -> datetime:
    if not value:
        return datetime.min
    try:
        return datetime.strptime(value, "%d.%m.%Y")
    except ValueError:
        return datetime.min


def _annual_final_preference(record: SourceDocumentRecord, year: int) -> int:
    next_year = year + 1
    for value in (record.modified_at, record.published_at):
        parsed = _record_sort_date(value)
        if parsed.year == next_year and parsed.month in {1, 2}:
            return 1
    return 0


def parse_minfin_auction_table_documents(
    html: str,
    base_url: str = BASE_URL,
    page_number: int = 1,
) -> list[SourceDocumentRecord]:
    parser = _SectionParser(TARGET_CONTAINER_ID)
    parser.feed(html)
    records: list[SourceDocumentRecord] = []
    for card in parser.cards:
        title = _clean_text(card.document_title or " ".join(card.text_parts))
        published_at, modified_at = parse_document_dates(card)
        document_id = _extract_document_id(card)
        document_page_url = resolve_file_url(base_url, card.attrs.get("data-href", ""))
        for file_item in card.file_items or []:
            absolute_url = resolve_file_url(base_url, file_item.href)
            file_name = PurePosixPath(urlparse(absolute_url).path).name
            extension = PurePosixPath(file_name).suffix.lower().lstrip(".")
            if extension != "xlsx":
                continue
            records.append(
                SourceDocumentRecord(
                    section_id=TARGET_SECTION_ID,
                    page_param=TARGET_PAGE_PARAM,
                    page_number=page_number,
                    document_id=document_id,
                    document_page_url=document_page_url,
                    document_title=title,
                    document_type=card.document_type,
                    published_at=published_at,
                    modified_at=modified_at,
                    tags=tuple(card.tags or []),
                    file_url=file_item.href,
                    absolute_file_url=absolute_url,
                    file_name=file_name,
                    file_title=file_item.title,
                    file_info=file_item.text() or None,
                    file_size_text=file_item.text() or None,
                    file_extension=extension,
                    as_of_date=parse_as_of_date_from_title(title),
                )
            )
    return records


def extract_pagination_info(html: str, section_id: int = TARGET_SECTION_ID) -> dict[str, object]:
    pagination_id = f"ajax-pagination-10090-{section_id}"
    parser = _PaginationParser(pagination_id)
    parser.feed(html)
    attrs = parser.attrs or {}
    page_count_raw = attrs.get("data-page-count")
    try:
        page_count = int(page_count_raw) if page_count_raw else None
    except ValueError:
        page_count = None
    href = attrs.get("href") or ""
    query = parse_qs(urlparse(href).query)
    page_param = f"page_{section_id}"
    next_page_values = query.get(page_param)
    return {
        "section_id": section_id,
        "pagination_id": pagination_id,
        "page_param": page_param,
        "page_count": page_count,
        "next_page": int(next_page_values[0]) if next_page_values else None,
        "container": attrs.get("data-container"),
        "href": href or None,
    }


def filter_candidates(records: list[SourceDocumentRecord], year: int) -> list[SourceDocumentRecord]:
    result: list[SourceDocumentRecord] = []
    year_text = str(year)
    for record in records:
        if record.section_id != TARGET_SECTION_ID:
            continue
        if record.file_extension.lower() != "xlsx":
            continue
        match = FILE_NAME_RE.match(record.file_name)
        if not match or match.group("year") != year_text:
            continue
        if year_text not in record.document_title:
            continue
        result.append(record)
    return result


def select_candidate(
    records: list[SourceDocumentRecord],
    year: int,
    mode: str,
) -> SourceDocumentRecord | None:
    candidates = filter_candidates(records, year)
    if not candidates:
        return None
    if mode == "monthly":
        monthly = [record for record in candidates if record.as_of_date]
        pool = monthly or candidates
        return max(
            pool,
            key=lambda record: (
                _record_sort_date(record.as_of_date),
                _record_sort_date(record.modified_at),
                _record_sort_date(record.published_at),
            ),
        )
    if mode == "annual-final":
        finals = [record for record in candidates if not record.as_of_date]
        pool = finals or candidates
        return max(
            pool,
            key=lambda record: (
                _annual_final_preference(record, year),
                _record_sort_date(record.modified_at),
                _record_sort_date(record.published_at),
            ),
        )
    raise ValueError(f"Unsupported mode: {mode}")


def extract_candidate_links(html: str, year: int, base_url: str = BASE_URL) -> list[SourceDocumentRecord]:
    records = parse_minfin_auction_table_documents(html, base_url=base_url, page_number=1)
    return filter_candidates(records, year)


def filter_minfin_excel_links(
    links: list[SourceDocumentRecord],
    year: int,
) -> list[SourceDocumentRecord]:
    return filter_candidates(links, year)


def select_best_candidate(
    candidates: list[SourceDocumentRecord],
    year: int,
    mode: str = "monthly",
) -> SourceDocumentRecord | None:
    return select_candidate(candidates, year, mode)
