"""Safe cleanup helper for generated files under outputs/.

The script defaults to dry-run. Destructive cleanup requires
`--delete-all --confirm DELETE_OUTPUTS` and never touches paths outside
the project `outputs/` directory.
"""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
ARCHIVE_DIR = OUTPUTS_DIR / "archive"
CLEANUP_REPORTS_DIR = OUTPUTS_DIR / "reports" / "cleanup"
CONFIRM_TOKEN = "DELETE_OUTPUTS"

SKELETON_DIRS = [
    OUTPUTS_DIR,
    OUTPUTS_DIR / "charts",
    OUTPUTS_DIR / "exports",
    OUTPUTS_DIR / "reports",
    OUTPUTS_DIR / "dashboards",
    OUTPUTS_DIR / "archive",
    OUTPUTS_DIR / "tmp",
    OUTPUTS_DIR / "charts" / "monthly",
    OUTPUTS_DIR / "charts" / "scatter",
    OUTPUTS_DIR / "charts" / "structure",
    OUTPUTS_DIR / "charts" / "revenue",
    OUTPUTS_DIR / "charts" / "sankey",
    OUTPUTS_DIR / "charts" / "risk",
    OUTPUTS_DIR / "exports" / "chart_data",
    OUTPUTS_DIR / "exports" / "analytical_tables",
    OUTPUTS_DIR / "exports" / "dashboard",
    OUTPUTS_DIR / "reports" / "quality",
    OUTPUTS_DIR / "reports" / "run_manifests",
    OUTPUTS_DIR / "reports" / "cleanup",
    OUTPUTS_DIR / "reports" / "executive_summary",
    OUTPUTS_DIR / "reports" / "data_quality",
]


@dataclass(frozen=True)
class CleanupCandidate:
    path: Path
    relative_path: str
    kind: str
    size_bytes: int


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Safely archive and/or clean generated files under outputs/.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build a cleanup report without archiving or deleting files. Default mode.",
    )
    parser.add_argument(
        "--archive-all",
        action="store_true",
        help="Archive current working outputs into outputs/archive/cleanup_<run_id>/.",
    )
    parser.add_argument(
        "--delete-all",
        action="store_true",
        help="Delete generated working outputs after explicit confirmation.",
    )
    parser.add_argument(
        "--confirm",
        default="",
        help=f"Required token for --delete-all: {CONFIRM_TOKEN}.",
    )
    return parser.parse_args(argv)


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def ensure_inside_outputs(path: Path) -> Path:
    resolved = path.resolve()
    outputs_resolved = OUTPUTS_DIR.resolve()
    if resolved != outputs_resolved and not is_relative_to(resolved, outputs_resolved):
        raise RuntimeError(f"Refusing to touch path outside outputs/: {path}")
    return resolved


def ensure_skeleton() -> None:
    for directory in SKELETON_DIRS:
        ensure_inside_outputs(directory)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / ".gitkeep").touch(exist_ok=True)


def top_level_working_entries() -> list[Path]:
    if not OUTPUTS_DIR.exists():
        return []
    entries: list[Path] = []
    for child in OUTPUTS_DIR.iterdir():
        ensure_inside_outputs(child)
        if child.resolve() == ARCHIVE_DIR.resolve():
            continue
        entries.append(child)
    return sorted(entries, key=lambda p: p.as_posix())


def collect_candidates() -> list[CleanupCandidate]:
    candidates: list[CleanupCandidate] = []
    for entry in top_level_working_entries():
        if entry.is_dir():
            files = list(entry.rglob("*"))
            size = sum(path.stat().st_size for path in files if path.is_file())
            kind = "directory"
        else:
            size = entry.stat().st_size
            kind = "file"
        candidates.append(
            CleanupCandidate(
                path=entry,
                relative_path=entry.relative_to(PROJECT_ROOT).as_posix(),
                kind=kind,
                size_bytes=size,
            )
        )
    return candidates


def candidate_file_rows(candidates: Sequence[CleanupCandidate]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for candidate in candidates:
        if candidate.path.is_file():
            rows.append(
                {
                    "path": candidate.relative_path,
                    "kind": "file",
                    "size_bytes": candidate.size_bytes,
                }
            )
            continue
        for path in sorted(candidate.path.rglob("*"), key=lambda item: item.as_posix()):
            if not path.is_file():
                continue
            rows.append(
                {
                    "path": path.relative_to(PROJECT_ROOT).as_posix(),
                    "kind": "file",
                    "size_bytes": path.stat().st_size,
                }
            )
    return rows


def build_manifest(
    *,
    run_id: str,
    mode: str,
    candidates: Sequence[CleanupCandidate],
    archive_root: Path | None,
    deleted: bool,
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "project_root": PROJECT_ROOT.as_posix(),
        "outputs_dir": OUTPUTS_DIR.relative_to(PROJECT_ROOT).as_posix(),
        "mode": mode,
        "archive_root": (
            archive_root.relative_to(PROJECT_ROOT).as_posix() if archive_root else None
        ),
        "delete_confirmed": deleted,
        "skeleton_recreated": deleted,
        "archive_policy": "outputs/archive is preserved; archives are not deleted by --delete-all.",
        "candidates_count": len(candidates),
        "candidates_size_bytes": sum(item.size_bytes for item in candidates),
        "candidates": [
            {
                "path": item.relative_path,
                "kind": item.kind,
                "size_bytes": item.size_bytes,
            }
            for item in candidates
        ],
        "files": candidate_file_rows(candidates),
    }


def format_bytes(size: int) -> str:
    value = float(size)
    for unit in ["bytes", "KB", "MB", "GB"]:
        if value < 1024 or unit == "GB":
            if unit == "bytes":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{size} bytes"


def manifest_markdown(manifest: dict[str, object]) -> str:
    candidates = manifest["candidates"]
    assert isinstance(candidates, list)
    lines = [
        "# Outputs cleanup manifest",
        "",
        f"- run_id: `{manifest['run_id']}`",
        f"- timestamp: `{manifest['timestamp']}`",
        f"- mode: `{manifest['mode']}`",
        f"- archive_root: `{manifest['archive_root']}`",
        f"- delete_confirmed: `{manifest['delete_confirmed']}`",
        f"- candidates_count: `{manifest['candidates_count']}`",
        f"- candidates_size: `{format_bytes(int(manifest['candidates_size_bytes']))}`",
        "",
        "| Path | Kind | Size |",
        "|---|---|---:|",
    ]
    for item in candidates:
        assert isinstance(item, dict)
        lines.append(
            f"| `{item['path']}` | {item['kind']} | {format_bytes(int(item['size_bytes']))} |"
        )
    return "\n".join(lines) + "\n"


def write_manifest(manifest: dict[str, object], directory: Path) -> tuple[Path, Path]:
    ensure_inside_outputs(directory)
    directory.mkdir(parents=True, exist_ok=True)
    run_id = str(manifest["run_id"])
    json_path = directory / f"cleanup_manifest_{run_id}.json"
    md_path = directory / f"cleanup_manifest_{run_id}.md"
    json_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    md_path.write_text(manifest_markdown(manifest), encoding="utf-8")
    return json_path, md_path


def archive_outputs(run_id: str, candidates: Sequence[CleanupCandidate]) -> Path:
    archive_root = ARCHIVE_DIR / f"cleanup_{run_id}"
    ensure_inside_outputs(archive_root)
    snapshot_root = archive_root / "outputs_snapshot"
    snapshot_root.mkdir(parents=True, exist_ok=False)
    for candidate in candidates:
        target = snapshot_root / candidate.path.name
        ensure_inside_outputs(target)
        if candidate.path.is_dir():
            shutil.copytree(candidate.path, target, dirs_exist_ok=False)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(candidate.path, target)
    return archive_root


def delete_working_outputs(candidates: Sequence[CleanupCandidate]) -> None:
    for candidate in candidates:
        ensure_inside_outputs(candidate.path)
        if candidate.path.resolve() == ARCHIVE_DIR.resolve():
            raise RuntimeError("Refusing to delete outputs/archive.")
        if candidate.path.is_dir():
            shutil.rmtree(candidate.path)
        elif candidate.path.exists():
            candidate.path.unlink()
    ensure_skeleton()


def mode_name(args: argparse.Namespace) -> str:
    if args.archive_all and args.delete_all:
        return "archive-all-delete-all"
    if args.archive_all:
        return "archive-all"
    if args.delete_all:
        return "delete-all"
    return "dry-run"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.dry_run and not args.archive_all and not args.delete_all:
        args.dry_run = True
    if args.delete_all and args.confirm != CONFIRM_TOKEN:
        raise SystemExit(
            f"ERROR: --delete-all requires --confirm {CONFIRM_TOKEN}. Nothing was deleted."
        )

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    ensure_inside_outputs(OUTPUTS_DIR)
    candidates = collect_candidates()
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode = mode_name(args)

    archive_root: Path | None = None
    if args.archive_all:
        archive_root = archive_outputs(run_id, candidates)

    if args.delete_all:
        manifest_dir = archive_root if archive_root is not None else ARCHIVE_DIR / f"cleanup_{run_id}"
        pre_delete_manifest = build_manifest(
            run_id=run_id,
            mode=f"{mode}-pre-delete",
            candidates=candidates,
            archive_root=archive_root if archive_root is not None else manifest_dir,
            deleted=False,
        )
        write_manifest(pre_delete_manifest, manifest_dir)
        delete_working_outputs(candidates)
        post_candidates = collect_candidates()
        post_delete_manifest = build_manifest(
            run_id=run_id,
            mode=f"{mode}-post-delete",
            candidates=post_candidates,
            archive_root=archive_root if archive_root is not None else manifest_dir,
            deleted=True,
        )
        json_path, md_path = write_manifest(post_delete_manifest, manifest_dir)
    else:
        report_dir = archive_root if archive_root is not None else CLEANUP_REPORTS_DIR
        manifest = build_manifest(
            run_id=run_id,
            mode=mode,
            candidates=candidates,
            archive_root=archive_root,
            deleted=False,
        )
        json_path, md_path = write_manifest(manifest, report_dir)

    print(f"mode={mode}")
    print(f"candidates={len(candidates)}")
    print(f"size={format_bytes(sum(item.size_bytes for item in candidates))}")
    print(f"manifest_json={json_path.relative_to(PROJECT_ROOT)}")
    print(f"manifest_md={md_path.relative_to(PROJECT_ROOT)}")
    if args.dry_run and not args.archive_all and not args.delete_all:
        print("dry_run=True; no files archived or deleted.")
    if args.delete_all:
        print("delete_confirmed=True; working outputs removed and skeleton recreated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
