"""Static smoke for project-root GUI wrappers."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WRAPPERS = (
    ROOT / "run-gui.ps1",
    ROOT / "ofz-gui.cmd",
)
FORBIDDEN_ABSOLUTE_FRAGMENTS = (
    "C:\\Users\\",
    "C:/Users/",
    "\\LLM_CHAT\\",
)


def assert_contains(text: str, token: str, path: Path) -> None:
    if token not in text:
        raise AssertionError(f"{path.name}: missing {token!r}")


def main() -> int:
    for path in WRAPPERS:
        if not path.exists():
            raise AssertionError(f"missing wrapper: {path}")
        text = path.read_text(encoding="utf-8")
        assert_contains(text, "PYTHONUTF8", path)
        assert_contains(text, "PYTHONIOENCODING", path)
        assert_contains(text, ".venv\\Scripts\\ofz-gui.exe", path)
        if any(fragment in text for fragment in FORBIDDEN_ABSOLUTE_FRAGMENTS):
            raise AssertionError(f"{path.name}: contains absolute user path")

    ps1 = WRAPPERS[0].read_text(encoding="utf-8")
    assert_contains(ps1, "chcp 65001 | Out-Null", WRAPPERS[0])
    assert_contains(ps1, "[Console]::OutputEncoding", WRAPPERS[0])
    assert_contains(ps1, "$OutputEncoding", WRAPPERS[0])

    cmd = WRAPPERS[1].read_text(encoding="utf-8")
    assert_contains(cmd, "chcp 65001 > nul", WRAPPERS[1])

    print("GUI launcher wrapper smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
