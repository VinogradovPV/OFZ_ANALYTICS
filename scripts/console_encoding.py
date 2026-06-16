"""Console encoding helpers for Windows CI and local CLI entry points."""

from __future__ import annotations

import sys


def configure_utf8_stdio() -> None:
    """Prefer UTF-8 console output and replace unencodable characters."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
