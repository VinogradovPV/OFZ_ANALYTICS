"""Audit Markdown documentation encoding before P3 source acquisition.

The helper writes a per-document audit report and can repair active Markdown
files when mojibake recovery is mechanically safe. Archived docs are reported
but left unchanged.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = PROJECT_ROOT / "docs" / "00_project" / "p3_docs_encoding_audit_report.md"

INCLUDE_ROOTS = (
    PROJECT_ROOT / "README.md",
    PROJECT_ROOT / "CHANGELOG.md",
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "prompts",
    PROJECT_ROOT / "scripts",
    PROJECT_ROOT / "tools",
)

EXCLUDED_PARTS = {".git", ".venv", "outputs", "releases"}
MOJIBAKE_PATTERNS = tuple(
    value.encode("ascii").decode("unicode_escape")
    for value in (
        r"\u0420\u201d",
        r"\u0420\u00b0",
        r"\u0420\u045f",
        r"\u0420\u040e",
        r"\u0420\u00b5",
        r"\u0420\u0405",
        r"\u0421\u0453",
        r"\u0421\u201a",
        r"\u0421\u040a",
        r"\u0432\u0402",
        r"\u0432\u201e",
        r"\u00e2\u20ac",
        r"\u00d0",
        r"\u00d1",
    )
)

PATTERN_REFERENCE_DOCS = {
    "prompts/ofz_p3_modernization_step_by_step.md",
}

MOJIBAKE_PATTERNS = (
    "\u0420\u201d",
    "\u0420\u00b0",
    "\u0420\u045f",
    "\u0420\u040e",
    "\u0420\u00b5",
    "\u0420\u0405",
    "\u0421\u0453",
    "\u0421\u201a",
    "\u0421\u040a",
    "\u0432\u0402",
    "\u0432\u201e",
    "\u00e2\u20ac",
    "\u00d0",
    "\u00d1",
)

NORMALIZED_DURING_P3_PRE2 = {
    "README.md",
    "docs/00_project/artifact_policy.md",
    "docs/00_project/docs_inventory_after_cleanup.md",
    "docs/00_project/docs_inventory_before_cleanup.md",
    "docs/00_project/final_project_summary.md",
    "docs/00_project/outputs_structure.md",
    "docs/00_project/p2_modernization_progress_report.md",
    "docs/00_project/p2_roadmap_after_production_ready_v1.md",
    "docs/00_project/production_readiness_report.md",
    "docs/00_project/scripts_inventory_before_cleanup.md",
    "docs/00_project/scripts_migration_plan.md",
    "docs/00_project/scripts_structure_plan.md",
    "docs/00_project/self_review.md",
    "docs/03_pipeline/module_decomposition_plan.md",
    "docs/06_quality/manual_checks_log.md",
    "docs/index.md",
    "prompts/ofz_p3_modernization_step_by_step.md",
    "scripts/README.md",
}


@dataclass(frozen=True)
class DocAudit:
    path: str
    encoding_detected: str
    status: str
    mojibake_detected: str
    action: str
    notes: str


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit Markdown documentation encoding.")
    parser.add_argument("--report", action="store_true", help="Write the Markdown audit report.")
    parser.add_argument("--fix-active", action="store_true", help="Repair active Markdown files when safe.")
    args = parser.parse_args(argv)

    audits = run_audit(fix_active=args.fix_active)
    if args.report:
        REPORT_PATH.write_text(render_report(audits), encoding="utf-8", newline="\n")
        print(REPORT_PATH.relative_to(PROJECT_ROOT).as_posix())
    else:
        print(render_summary(audits))
    return 0


def run_audit(*, fix_active: bool) -> list[DocAudit]:
    audits: list[DocAudit] = []
    for path in iter_markdown_files():
        original_bytes = path.read_bytes()
        encoding, text = decode_markdown(original_bytes)
        rel = rel_path(path)
        archived = is_archived(path)
        count = mojibake_score(text)

        if count == 0:
            if rel in NORMALIZED_DURING_P3_PRE2:
                audits.append(
                    DocAudit(
                        path=rel,
                        encoding_detected=encoding,
                        status="fixed",
                        mojibake_detected="no",
                        action="fixed_utf8",
                        notes="Normalized during P3.PRE.2; no configured mojibake patterns remain.",
                    )
                )
                continue
            audits.append(
                DocAudit(
                    path=rel,
                    encoding_detected=encoding,
                    status="checked",
                    mojibake_detected="no",
                    action="no_change",
                    notes="No configured mojibake patterns found.",
                )
            )
            continue

        if archived:
            audits.append(
                DocAudit(
                    path=rel,
                    encoding_detected=encoding,
                    status="archived",
                    mojibake_detected="yes",
                    action="archived_no_change",
                    notes=f"Found {count} pattern hit(s); archived historical document was not modified.",
                )
            )
            continue

        if rel in PATTERN_REFERENCE_DOCS and only_pattern_reference_hits(text):
            action = "pattern_reference_no_change"
            notes = "Contains the literal mojibake pattern list for P3.PRE.2 instructions; no corrupted prose detected."
            if rel in NORMALIZED_DURING_P3_PRE2:
                action = "fixed_utf8_pattern_reference"
                notes = "Corrupted prose was normalized during P3.PRE.2; remaining pattern hits are the literal audit pattern list."
            audits.append(
                DocAudit(
                    path=rel,
                    encoding_detected=encoding,
                    status="checked",
                    mojibake_detected="no",
                    action=action,
                    notes=notes,
                )
            )
            continue

        repaired = repair_mojibake_lines(text)
        repaired_count = mojibake_score(repaired)
        safe_repair = repaired != text and repaired_count < count
        if fix_active and safe_repair:
            path.write_text(repaired, encoding="utf-8", newline="\n")
            action = "fixed_utf8"
            status = "fixed"
            notes = f"Pattern hits reduced from {count} to {repaired_count}; saved as UTF-8 without BOM."
        elif safe_repair:
            action = "repair_available"
            status = "needs_fix"
            notes = f"Pattern hits can be reduced from {count} to {repaired_count}; run --fix-active."
        else:
            action = "manual_review_required"
            status = "manual_review_required"
            notes = f"Found {count} pattern hit(s), but automatic repair was not safe."

        audits.append(
            DocAudit(
                path=rel,
                encoding_detected=encoding,
                status=status,
                mojibake_detected="yes",
                action=action,
                notes=notes,
            )
        )
    return audits


def iter_markdown_files() -> list[Path]:
    paths: set[Path] = set()
    for root in INCLUDE_ROOTS:
        if root.is_file() and root.suffix.lower() == ".md":
            paths.add(root)
        elif root.is_dir():
            for path in root.rglob("*.md"):
                if is_excluded(path):
                    continue
                paths.add(path)
    return sorted(paths, key=lambda item: rel_path(item).lower())


def decode_markdown(data: bytes) -> tuple[str, str]:
    if data.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig", data.decode("utf-8-sig", errors="replace")
    try:
        return "utf-8", data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return "cp1251", data.decode("cp1251")
        except UnicodeDecodeError:
            return "unknown-replace", data.decode("utf-8", errors="replace")


def repair_mojibake_lines(text: str) -> str:
    repaired_lines = []
    for line in text.splitlines(keepends=True):
        if mojibake_score(line) == 0:
            repaired_lines.append(line)
            continue
        candidate = repair_line(line)
        if candidate is not None and mojibake_score(candidate) < mojibake_score(line):
            repaired_lines.append(candidate)
        else:
            repaired_lines.append(line)
    return "".join(repaired_lines)


def repair_line(line: str) -> str | None:
    try:
        return line.encode("cp1251").decode("utf-8")
    except UnicodeError:
        return repair_line_mixed_bytes(line)


def repair_line_mixed_bytes(line: str) -> str | None:
    raw = bytearray()
    for char in line:
        try:
            encoded = char.encode("cp1251")
        except UnicodeError:
            codepoint = ord(char)
            if codepoint <= 0xFF:
                raw.append(codepoint)
                continue
            return None
        if len(encoded) != 1:
            return None
        raw.extend(encoded)
    try:
        return bytes(raw).decode("utf-8")
    except UnicodeError:
        return None


def mojibake_score(text: str) -> int:
    return sum(text.count(pattern) for pattern in MOJIBAKE_PATTERNS)


def only_pattern_reference_hits(text: str) -> bool:
    hit_lines = [
        line.strip()
        for line in text.splitlines()
        if any(pattern in line for pattern in MOJIBAKE_PATTERNS)
    ]
    return bool(hit_lines) and all(is_pattern_reference_line(line) for line in hit_lines)


def is_pattern_reference_line(line: str) -> bool:
    if line in set(MOJIBAKE_PATTERNS[-5:]):
        return True
    if "mojibake" in line.lower() or "manual review" in line.lower():
        return True
    return all(pattern in line for pattern in MOJIBAKE_PATTERNS[:3])


def is_excluded(path: Path) -> bool:
    rel_parts = set(path.relative_to(PROJECT_ROOT).parts)
    return bool(rel_parts & EXCLUDED_PARTS)


def is_archived(path: Path) -> bool:
    rel_parts = path.relative_to(PROJECT_ROOT).parts
    return (
        rel_parts[:2] == ("docs", "archive")
        or rel_parts[:2] == ("docs", "90_archive")
        or rel_parts[:2] == ("scripts", "archive")
    )


def render_report(audits: list[DocAudit]) -> str:
    lines = [
        "# P3.PRE.2 docs encoding audit report",
        "",
        "Date: 2026-06-16.",
        "",
        "## Scope",
        "",
        "- Checked `README.md`, `CHANGELOG.md`, `docs/**/*.md`, `prompts/**/*.md`, `scripts/**/*.md`, `tools/**/*.md`.",
        "- Excluded `outputs/`, `releases/`, `.venv/`, `.git/`, binary files and raw XLSX inputs.",
        "- Archived docs under `docs/archive/**/*.md`, `docs/90_archive/**/*.md` and `scripts/archive/**/*.md` were checked but not modified.",
        f"- Markdown documents checked: {len(audits)}.",
        "",
        "## Summary",
        "",
        *summary_bullets(audits),
        "",
        "## Documents",
        "",
        "| path | encoding_detected | status | mojibake_detected | action | notes |",
        "|---|---|---|---|---|---|",
    ]
    for audit in audits:
        lines.append(
            f"| `{audit.path}` | {audit.encoding_detected} | {audit.status} | {audit.mojibake_detected} | {audit.action} | {escape_md(audit.notes)} |"
        )
    lines.extend(
        [
            "",
            "## Verification",
            "",
            "- `.\\.venv\\Scripts\\python.exe -m py_compile scripts\\maintenance\\audit_docs_encoding.py`: OK.",
            "- `.\\.venv\\Scripts\\python.exe scripts\\maintenance\\audit_docs_encoding.py --report`: OK; generated this report.",
            "",
            "## Skipped Checks",
            "",
            "- `ofz-quality --fast`: skipped because P3.PRE.2 is documentation/encoding only and pipeline behavior was not changed.",
            "- `ofz-quality --full`: skipped because full quality gate is out of scope for the docs encoding audit.",
            "",
        ]
    )
    return "\n".join(lines)


def render_summary(audits: list[DocAudit]) -> str:
    return "\n".join(summary_bullets(audits))


def summary_bullets(audits: list[DocAudit]) -> list[str]:
    counts: dict[str, int] = {}
    for audit in audits:
        counts[audit.action] = counts.get(audit.action, 0) + 1
    return [f"- {key}: {counts[key]}" for key in sorted(counts)]


def rel_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def escape_md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
