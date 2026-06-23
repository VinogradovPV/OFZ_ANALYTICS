"""Read-only guard for generated paths accidentally staged in Git."""

from __future__ import annotations

import subprocess
from pathlib import Path


FORBIDDEN_PARTS = (
    "outputs/charts",
    "outputs/exports",
    "outputs/reports",
    "outputs/dashboards",
    "outputs/archive",
    "outputs/tmp",
    "outputs/cache",
    "data/processed",
    "logs",
    ".ofz_launcher",
    "releases",
    "docm",
    "crdownload",
    "data/raw/minfin/ofz_auction_results/versions",
)


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        shell=False,
        check=False,
    )
    if result.returncode != 0:
        print(result.stderr.strip() or "Не удалось получить staged paths.")
        return result.returncode
    staged = [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]
    forbidden = [path for path in staged if any(part in path.lower() for part in FORBIDDEN_PARTS)]
    if forbidden:
        print("BLOCKED: generated/release paths staged:")
        for path in forbidden:
            print(f"- {path}")
        return 1
    print(f"Artifact guard passed. Staged files checked: {len(staged)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
