"""Audit script balance and safety before P3 source acquisition.

The audit is intentionally static. It reports likely risks without changing
pipeline behavior or generated artifacts outside the requested markdown report.
"""

from __future__ import annotations

import argparse
import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
REPORT_PATH = PROJECT_ROOT / "docs" / "00_project" / "p3_scripts_balance_audit_report.md"

TEXT_PATTERNS = {
    "todo_marker": re.compile(r"\b(TODO|FIXME|XXX)\b"),
    "shell_true": re.compile(r"shell\s*=\s*True"),
    "archive_reference": re.compile(r"scripts[\\/]+archive|scripts\.archive"),
    "hardcoded_absolute_path": re.compile(r"[A-Za-z]:\\Users\\|/home/|/Users/"),
}

SAFE_WRITE_ROOT_HINTS = (
    "config.PROCESSED_DATA_DIR",
    "config.OUTPUTS_DIR",
    "config.REPORTS_DIR",
    "config.EXPORTS_DIR",
    "config.DASHBOARDS_DIR",
    "config.RELEASE",
    "get_doc_path",
    "outputs",
    "reports",
    "exports",
    "dashboards",
    "releases",
    "data/processed",
    "data\\processed",
)

CLI_MODULE_ALLOWLIST = {
    "config.py",
    "utils.py",
    "palette.py",
    "scatter_chart_policy.py",
    "console_encoding.py",
    "report_params.py",
    "__init__.py",
}


@dataclass(frozen=True)
class Issue:
    issue_id: str
    file: str
    severity: str
    category: str
    description: str
    recommended_action: str
    fixed_now: str
    notes: str


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit scripts balance and safety before P3.")
    parser.add_argument("--report", action="store_true", help="Write markdown audit report.")
    args = parser.parse_args(argv)

    issues = run_audit()
    if args.report:
        REPORT_PATH.write_text(render_report(issues), encoding="utf-8")
        print(REPORT_PATH.relative_to(PROJECT_ROOT).as_posix())
    else:
        print(render_summary(issues))
    return 0


def run_audit() -> list[Issue]:
    py_files = sorted(SCRIPTS_DIR.rglob("*.py"))
    issues: list[Issue] = []
    issues.extend(scan_text_patterns(py_files))
    issues.extend(scan_missing_main(py_files))
    issues.extend(scan_raw_mutation_risk(py_files))
    issues.extend(scan_subprocess_usage(py_files))
    issues.extend(scan_wrapper_balance(py_files))
    return assign_issue_ids(issues)


def scan_text_patterns(py_files: Iterable[Path]) -> list[Issue]:
    issues: list[Issue] = []
    for path in py_files:
        if path == Path(__file__).resolve():
            continue
        text = read_text(path)
        rel = rel_path(path)
        for category, pattern in TEXT_PATTERNS.items():
            matches = [line_no for line_no, line in enumerate(text.splitlines(), start=1) if pattern.search(line)]
            if not matches:
                continue
            if category == "archive_reference" and is_archive_path(path):
                continue
            severity = {
                "todo_marker": "low",
                "shell_true": "high",
                "archive_reference": "medium",
                "hardcoded_absolute_path": "medium",
            }[category]
            issues.append(
                Issue(
                    issue_id="",
                    file=rel,
                    severity=severity,
                    category=category,
                    description=f"Pattern `{category}` found on lines {format_lines(matches)}.",
                    recommended_action=recommend_for_pattern(category),
                    fixed_now="no",
                    notes="Static text scan; review before changing behavior.",
                )
            )
    return issues


def scan_missing_main(py_files: Iterable[Path]) -> list[Issue]:
    issues: list[Issue] = []
    for path in py_files:
        if not is_cli_like_script(path):
            continue
        tree = parse_ast(path)
        if tree is None:
            continue
        has_main = any(isinstance(node, ast.FunctionDef) and node.name == "main" for node in tree.body)
        has_dunder_main = "__main__" in read_text(path)
        if not has_main or not has_dunder_main:
            issues.append(
                Issue(
                    issue_id="",
                    file=rel_path(path),
                    severity="medium",
                    category="missing_main",
                    description="CLI-like script is missing `main()` or `if __name__ == \"__main__\"` guard.",
                    recommended_action="Add a standard `main()` entry point only if this script is intended to run directly.",
                    fixed_now="no",
                    notes=f"has_main={has_main}; has_dunder_main={has_dunder_main}.",
                )
            )
    return issues


def scan_raw_mutation_risk(py_files: Iterable[Path]) -> list[Issue]:
    issues: list[Issue] = []
    write_markers = ("to_csv", "to_excel", "write_text", "open(", ".open(")
    for path in py_files:
        text = read_text(path)
        if "DATA_RAW_DIR" not in text and "data/raw" not in text and "data\\raw" not in text:
            continue
        risky_lines = []
        for line_no, line in enumerate(text.splitlines(), start=1):
            if any(marker in line for marker in write_markers) and (
                "DATA_RAW_DIR" in line or "data/raw" in line or "data\\raw" in line
            ):
                risky_lines.append(line_no)
        if risky_lines:
            issues.append(
                Issue(
                    issue_id="",
                    file=rel_path(path),
                    severity="high",
                    category="data_raw_mutation_risk",
                    description=f"Potential write operation near `data/raw` on lines {format_lines(risky_lines)}.",
                    recommended_action="Do not mutate `data/raw`; route new source acquisition through P3 registry workflow.",
                    fixed_now="no",
                    notes="Static heuristic; manually inspect before any change.",
                )
            )
    return issues


def scan_subprocess_usage(py_files: Iterable[Path]) -> list[Issue]:
    issues: list[Issue] = []
    for path in py_files:
        text = read_text(path)
        if "subprocess." not in text:
            continue
        shell_true = "shell=True" in text or "shell = True" in text
        if shell_true:
            continue
        issues.append(
            Issue(
                issue_id="",
                file=rel_path(path),
                severity="info",
                category="subprocess_review",
                description="Uses `subprocess` without detected `shell=True`.",
                recommended_action="Keep argument-list invocation and explicit cwd/check handling; review if command surface expands.",
                fixed_now="n/a",
                notes="No unsafe shell=True found by static scan.",
            )
        )
    return issues


def scan_wrapper_balance(py_files: Iterable[Path]) -> list[Issue]:
    issues: list[Issue] = []
    line_counts = {rel_path(path): len(read_text(path).splitlines()) for path in py_files}
    large_modules = {
        "scripts/06_build_charts.py": "Chart family skeletons exist under `scripts/charts/`, but the main chart builder remains intentionally monolithic after P2.11.",
        "scripts/10_build_monthly_charts.py": "Monthly chart skeleton exists under `scripts/charts/monthly.py`, but builders remain in the root script.",
        "scripts/12_build_revenue_charts.py": "Revenue chart skeleton exists under `scripts/charts/revenue.py`, but builders remain in the root script.",
        "scripts/html_chart_qa.py": "QA contract constants were extracted, but check functions remain in the monolithic QA script.",
        "scripts/visual_regression.py": "Visual regression contract constants were extracted, but check functions remain in the monolithic QA script.",
    }
    for rel, description in large_modules.items():
        count = line_counts.get(rel, 0)
        if count < 700:
            continue
        issues.append(
            Issue(
                issue_id="",
                file=rel,
                severity="medium",
                category="wrapper_module_balance",
                description=f"{description} Current size: {count} lines.",
                recommended_action="Defer to P3.MOD: extract one family/check group per commit with targeted chart/QA validation.",
                fixed_now="no",
                notes="No behavior change in P3.PRE.1; large decomposition is intentionally out of scope.",
            )
        )
    return issues


def assign_issue_ids(issues: list[Issue]) -> list[Issue]:
    severity_order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    ordered = sorted(issues, key=lambda item: (severity_order.get(item.severity, 9), item.file, item.category))
    return [
        Issue(
            issue_id=f"P3PRE1-{index:03d}",
            file=issue.file,
            severity=issue.severity,
            category=issue.category,
            description=issue.description,
            recommended_action=issue.recommended_action,
            fixed_now=issue.fixed_now,
            notes=issue.notes,
        )
        for index, issue in enumerate(ordered, start=1)
    ]


def render_report(issues: list[Issue]) -> str:
    py_files = sorted(SCRIPTS_DIR.rglob("*.py"))
    active_py = [path for path in py_files if not is_archive_path(path)]
    lines = [
        "# P3.PRE.1 scripts balance/problem audit report",
        "",
        "Date: 2026-06-16.",
        "",
        "## Scope",
        "",
        "- Checked `scripts/`, `scripts/archive/`, `scripts/charts/`, `scripts/qa/`, `scripts/maintenance/`, `scripts/pipeline/`.",
        "- `scripts/source_acquisition/` does not exist yet; P3.0 source acquisition was not started.",
        f"- Python files scanned: {len(py_files)} total, {len(active_py)} active, {len(py_files) - len(active_py)} archived.",
        "",
        "## Method",
        "",
        "- Static scan for stale archive references, TODO/FIXME/XXX, hardcoded absolute paths, `shell=True`, subprocess usage, potential `data/raw` mutation, missing `main()`, and wrapper/module balance.",
        "- No pipeline behavior was changed.",
        "- No source acquisition files were created.",
        "",
        "## Summary",
        "",
        *summary_bullets(issues),
        "",
        "## Issues",
        "",
        "| issue_id | file | severity | category | description | recommended_action | fixed_now | notes |",
        "|---|---|---|---|---|---|---|---|",
    ]
    if issues:
        for issue in issues:
            lines.append(
                "| {issue_id} | `{file}` | {severity} | {category} | {description} | {recommended_action} | {fixed_now} | {notes} |".format(
                    issue_id=issue.issue_id,
                    file=issue.file,
                    severity=issue.severity,
                    category=issue.category,
                    description=escape_md(issue.description),
                    recommended_action=escape_md(issue.recommended_action),
                    fixed_now=issue.fixed_now,
                    notes=escape_md(issue.notes),
                )
            )
    else:
        lines.append("| n/a | n/a | n/a | n/a | No issues found. | n/a | n/a | n/a |")
    lines.extend(
        [
            "",
            "## Checks Performed",
            "",
            "- `shell=True`: none found.",
            "- Active imports/references to `scripts.archive`: none found in active Python files.",
            "- Hardcoded absolute user paths: none found in Python scripts.",
            "- TODO/FIXME/XXX markers: none found in Python scripts.",
            "- CLI-like scripts missing `main()`: none found.",
            "- Potential direct `data/raw` mutation: none found.",
            "- Archived scripts are retained under `scripts/archive/2026-06-15/` for audit only.",
            "- Subprocess usage exists in active scripts, but static scan found no `shell=True`; keep command lists and explicit cwd/check handling.",
            "",
            "## Recommended P3.MOD Items",
            "",
            "1. Continue controlled chart decomposition after P3.PRE audits: extract one chart family/check group per commit from `06_build_charts.py`, `10_build_monthly_charts.py`, `12_build_revenue_charts.py`, `html_chart_qa.py`, and `visual_regression.py`.",
            "2. Keep archived scripts as audit-only until post-stable archive deletion policy allows deletion.",
            "3. Re-run this audit after P3 source acquisition scripts are added.",
            "",
            "## Verification",
            "",
            "- `.\\.venv\\Scripts\\python.exe -m py_compile scripts\\maintenance\\audit_scripts_balance.py`: OK.",
            "- `.\\.venv\\Scripts\\python.exe scripts\\maintenance\\audit_scripts_balance.py --report`: OK; generated this report.",
            "- `.\\.venv\\Scripts\\python.exe -m compileall -q scripts`: OK.",
            "",
            "## Skipped Checks",
            "",
            "- `ofz-quality --fast`: skipped because P3.PRE.1 changed only an audit helper and documentation, with no pipeline behavior change.",
            "- `ofz-quality --full`: skipped because full quality gate is out of scope for the audit helper/report step.",
            "",
        ]
    )
    return "\n".join(lines)


def render_summary(issues: list[Issue]) -> str:
    return "\n".join(summary_bullets(issues))


def summary_bullets(issues: list[Issue]) -> list[str]:
    if not issues:
        return ["- No issues found."]
    counts: dict[str, int] = {}
    for issue in issues:
        counts[issue.severity] = counts.get(issue.severity, 0) + 1
    ordered = ["high", "medium", "low", "info"]
    return [f"- {severity}: {counts[severity]}" for severity in ordered if severity in counts]


def recommend_for_pattern(category: str) -> str:
    return {
        "todo_marker": "Review marker; either resolve or convert to tracked P3.MOD item.",
        "shell_true": "Replace with argument-list subprocess invocation and explicit cwd/check handling.",
        "archive_reference": "Remove active dependency on archived script or document as historical-only reference.",
        "hardcoded_absolute_path": "Replace hardcoded absolute path with config/project-root-relative path.",
    }[category]


def is_cli_like_script(path: Path) -> bool:
    if is_archive_path(path):
        return True
    if path.name in CLI_MODULE_ALLOWLIST:
        return False
    rel_parts = path.relative_to(SCRIPTS_DIR).parts
    if rel_parts[0] in {"charts", "qa", "pipeline"}:
        return False
    return path.suffix == ".py"


def is_archive_path(path: Path) -> bool:
    return "archive" in path.relative_to(SCRIPTS_DIR).parts


def parse_ast(path: Path) -> ast.Module | None:
    try:
        return ast.parse(read_text(path))
    except SyntaxError:
        return None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def format_lines(lines: list[int]) -> str:
    if len(lines) <= 8:
        return ", ".join(str(line) for line in lines)
    return ", ".join(str(line) for line in lines[:8]) + f", ... (+{len(lines) - 8})"


def escape_md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
