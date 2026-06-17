"""Small urllib-based HTTP helpers for Minfin source acquisition."""

from __future__ import annotations

import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class HttpClientError(RuntimeError):
    """Raised when page or file acquisition fails after retries."""


def _request(url: str, user_agent: str) -> Request:
    return Request(url, headers={"User-Agent": user_agent})


def _decode_response(body: bytes, content_type: str | None) -> str:
    charset = None
    if content_type:
        for part in content_type.split(";"):
            part = part.strip()
            if part.lower().startswith("charset="):
                charset = part.split("=", 1)[1].strip()
                break
    for encoding in [charset, "utf-8", "cp1251"]:
        if not encoding:
            continue
        try:
            return body.decode(encoding)
        except UnicodeDecodeError:
            continue
    return body.decode("utf-8", errors="replace")


def fetch_page(url: str, timeout_seconds: int, retries: int, user_agent: str) -> str:
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urlopen(_request(url, user_agent), timeout=timeout_seconds) as response:
                body = response.read()
                return _decode_response(body, response.headers.get("Content-Type"))
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(min(2**attempt, 5))
    raise HttpClientError(f"failed to fetch page {url}: {last_error}") from last_error


def download_file(url: str, temp_path: str | Path, timeout_seconds: int, retries: int, user_agent: str) -> Path:
    target = Path(temp_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urlopen(_request(url, user_agent), timeout=timeout_seconds) as response:
                with target.open("wb") as handle:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        handle.write(chunk)
            return target
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if target.exists():
                target.unlink()
            if attempt < retries:
                time.sleep(min(2**attempt, 5))
    raise HttpClientError(f"failed to download file {url}: {last_error}") from last_error
