"""Shared constants and patterns for Minfin OFZ source acquisition."""

from __future__ import annotations

import re


BASE_URL = "https://minfin.gov.ru"
DEFAULT_SOURCE_URL = (
    "https://minfin.gov.ru/ru/perfomance/public_debt/internal/operations/ofz/"
    "auction/#tablitsy_po_rezultatam_provedeniya_auktsionov"
)

TARGET_SECTION_ID = 66
TARGET_ANCHOR = "tablitsy_po_rezultatam_provedeniya_auktsionov"
TARGET_CONTAINER_ID = "ajax-pagination-content-10090-66"
TARGET_PAGINATION_ID = "ajax-pagination-10090-66"
TARGET_PAGE_PARAM = "page_66"
TARGET_DOCUMENT_ID_PARAM = "id_66"
IGNORED_SECTION_IDS = {65, 38, 39}

DEFAULT_MAX_PAGES = 20
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_RETRIES = 2
DEFAULT_USER_AGENT = "OFZ_ANALYTICS source acquisition"
DOWNLOAD_CONFIRM_TOKEN = "DOWNLOAD_MINFIN_SOURCE"
REPLACE_FINAL_CONFIRM_TOKEN = "REPLACE_MINFIN_FINAL"

FILE_NAME_RE = re.compile(
    r"^INTERNET_Auction_Results_rus_(?P<year>\d{4})_(?P<suffix>[^/\\]+)\.xlsx$",
    re.IGNORECASE,
)
AS_OF_DATE_RE = re.compile(r"\b(?:на|РЅР°)\s+(?P<date>\d{2}\.\d{2}\.\d{4})\b", re.IGNORECASE)
