"""Проверка исходных текстовых файлов на UTF-8 и признаки mojibake."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Sequence


TEXT_EXTENSIONS = {
    ".bat",
    ".cfg",
    ".csv",
    ".ini",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".spec",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
    ".html",
    ".css",
    ".js",
    ".sql",
    ".rst",
}

EXCLUDED_DIR_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tmp",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "releases",
    "outputs",
    "logs",
    "venv",
}

EXCLUDED_RELATIVE_DIRS = {("data", "processed")}
GENERATED_TEMP_DIR_PREFIXES = (".minfin_registry_smoke_", "minfin_registry_smoke_")

# Строки намеренно хранятся через escape-последовательности: сам QA-скрипт не
# должен срабатывать на собственный список запрещенных маркеров.
MOJIBAKE_MARKERS = tuple(
    value.encode("ascii").decode("unicode_escape")
    for value in (
        r"\u00d0",
        r"\u00d1",
        r"\u0420\u045f",
        r"\u0420\u0408",
        r"\u0420\u0452",
        r"\u0420\u00b5",
        r"\u0420\u0455",
        r"\u0420\u00b0",
        r"\u0420\u0451",
        r"\u0420\u0459",
        r"\u0420\u045a",
        r"\u0420\u045b",
        r"\u2568",
        r"\u2564",
        r"\ufffd",
        r"\u00e2",
        r"\u00c2",
        r"\u00e2\u20ac\u2122",
        r"\u00e2\u20ac\u0153",
        r"\u00e2\u20ac",
        r"\u00e2\u20ac\u201c",
        r"\u00e2\u20ac\u201d",
    )
)

SELF_ALLOWLIST = {Path("scripts/qa/check_text_encoding.py")}
WORK_INSTRUCTION_ALLOWLIST = {
    Path("prompts/ofz_cbr_keyrate_web_parser_gui_utf8_instruction_v3(1).md"),
}
FIXTURE_ALLOWLIST_PARTS = {"encoding_fixtures", "mojibake_fixtures"}
MAX_PRINTED_PROBLEMS = 200


@dataclass(frozen=True)
class EncodingProblem:
    """Одна проблема кодировки или mojibake."""

    path: str
    category: str
    detail: str


@dataclass(frozen=True)
class AuditSummary:
    """Сводка одного запуска проверки."""

    root: str
    checked_files: int
    excluded_directories: int
    invalid_utf8_files: int
    mojibake_files: int
    allowed_marker_files: int
    fixed_files: int
    problems: int


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Проверка UTF-8 и mojibake в исходных текстовых файлах.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--json-report", type=Path)
    parser.add_argument("--markdown-report", type=Path)
    parser.add_argument("--commit", default="unknown", help="Commit/base commit для audit report.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--fix-safe", action="store_true", help="Исправить только однозначные случаи.")
    mode.add_argument("--no-fix", action="store_true", help="Только проверка (режим по умолчанию).")
    return parser.parse_args(argv)


def is_excluded_directory(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if path.name in EXCLUDED_DIR_NAMES:
        return True
    if path.name.startswith(GENERATED_TEMP_DIR_PREFIXES):
        return True
    parts = tuple(relative.parts)
    return any(parts[: len(prefix)] == prefix for prefix in EXCLUDED_RELATIVE_DIRS)


def iter_text_files(root: Path) -> tuple[list[Path], int]:
    files: list[Path] = []
    excluded_count = 0
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in sorted(directory.iterdir(), key=lambda item: item.name.lower(), reverse=True):
            if path.is_dir():
                if is_excluded_directory(path, root):
                    excluded_count += 1
                else:
                    pending.append(path)
            elif path.suffix.lower() in TEXT_EXTENSIONS:
                files.append(path)
    return sorted(files, key=lambda path: path.relative_to(root).as_posix().lower()), excluded_count


def marker_label(marker: str) -> str:
    return " ".join(f"U+{ord(char):04X}" for char in marker)


def is_marker_allowed(relative: Path) -> bool:
    normalized = Path(relative.as_posix())
    return (
        normalized in SELF_ALLOWLIST
        or normalized in WORK_INSTRUCTION_ALLOWLIST
        or bool(FIXTURE_ALLOWLIST_PARTS.intersection(relative.parts))
    )


def find_markers(text: str) -> list[str]:
    return [marker for marker in MOJIBAKE_MARKERS if marker in text]


def safe_repair(path: Path, raw: bytes, text: str | None) -> str | None:
    """Вернуть однозначно исправленный текст или None."""
    if text is None:
        try:
            candidate = raw.decode("cp1251")
        except UnicodeDecodeError:
            return None
        return candidate if not find_markers(candidate) else None

    before = len(find_markers(text))
    if before == 0:
        return None
    try:
        candidate = text.encode("cp1251").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return None
    return candidate if len(find_markers(candidate)) < before else None


def audit(root: Path, fix_safe: bool = False) -> tuple[AuditSummary, list[EncodingProblem]]:
    root = root.resolve()
    files, excluded_count = iter_text_files(root)
    problems: list[EncodingProblem] = []
    invalid_paths: set[Path] = set()
    mojibake_paths: set[Path] = set()
    allowed_paths: set[Path] = set()
    fixed_paths: set[Path] = set()

    for path in files:
        relative = path.relative_to(root)
        raw = path.read_bytes()
        try:
            text: str | None = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            text = None
            invalid_paths.add(relative)
            if fix_safe:
                repaired = safe_repair(path, raw, None)
                if repaired is not None:
                    path.write_text(repaired, encoding="utf-8", newline="")
                    fixed_paths.add(relative)
                    text = repaired
                    invalid_paths.discard(relative)
            if text is None:
                problems.append(EncodingProblem(relative.as_posix(), "invalid_utf8", str(exc)))
                continue

        markers = find_markers(text)
        if not markers:
            continue
        if is_marker_allowed(relative):
            allowed_paths.add(relative)
            continue
        if fix_safe:
            repaired = safe_repair(path, raw, text)
            if repaired is not None:
                path.write_text(repaired, encoding="utf-8", newline="")
                fixed_paths.add(relative)
                markers = find_markers(repaired)
        if markers:
            mojibake_paths.add(relative)
            labels = ", ".join(marker_label(marker) for marker in markers)
            problems.append(EncodingProblem(relative.as_posix(), "mojibake_detected", labels))

    summary = AuditSummary(
        root=str(root),
        checked_files=len(files),
        excluded_directories=excluded_count,
        invalid_utf8_files=len(invalid_paths),
        mojibake_files=len(mojibake_paths),
        allowed_marker_files=len(allowed_paths),
        fixed_files=len(fixed_paths),
        problems=len(problems),
    )
    return summary, problems


def render_markdown(summary: AuditSummary, problems: Iterable[EncodingProblem], commit: str) -> str:
    problem_list = list(problems)
    lines = [
        "# Аудит UTF-8 и mojibake",
        "",
        f"- Дата: `{date.today().isoformat()}`",
        f"- Commit/base commit: `{commit}` (Git не вызывается из QA-скрипта).",
        f"- Корень проверки: `{summary.root}`",
        "- Scope: source, tests, docs, configs и другие поддерживаемые текстовые файлы проекта.",
        "- Расширения: " + ", ".join(f"`{value}`" for value in sorted(TEXT_EXTENSIONS)),
        "- Исключенные каталоги: " + ", ".join(f"`{value}`" for value in sorted(EXCLUDED_DIR_NAMES)),
        "- Дополнительные исключения: `data/processed`, весь `outputs` (включая reports/charts/exports/dashboards/archive/tmp/cache).",
        "",
        "## Итог",
        "",
        f"- Проверено файлов: `{summary.checked_files}`",
        f"- Исключено каталогов: `{summary.excluded_directories}`",
        f"- Invalid UTF-8: `{summary.invalid_utf8_files}`",
        f"- Файлы с mojibake: `{summary.mojibake_files}`",
        f"- Allowlisted marker contexts: `{summary.allowed_marker_files}`",
        f"- Безопасно исправлено в этом запуске: `{summary.fixed_files}`",
        f"- Статус: `{'BLOCKED' if summary.problems else 'PASSED'}`",
        "",
        "## Найденные проблемы и действия",
        "",
    ]
    if problem_list:
        lines.extend(["| Файл | Классификация | Действие |", "| --- | --- | --- |"])
        for problem in problem_list:
            action = "Требуется исправление или ручная проверка"
            lines.append(f"| `{problem.path}` | `{problem.category}` ({problem.detail}) | {action} |")
    else:
        lines.append("Invalid UTF-8 и запрещенные mojibake-маркеры не обнаружены.")
    lines.extend(
        [
            "",
            "## Manual review",
            "",
            "Неоднозначные случаи автоматически не исправляются. При чистом результате открытых пунктов нет.",
            "",
            "## Политика",
            "",
            "- Все source/docs/config/scripts хранятся в UTF-8.",
            "- Generated artifacts, caches, virtual environments и raw Excel не проверяются.",
            "- Mojibake допускается только в allowlisted тестовых контекстах.",
            "- Invalid UTF-8 или mojibake блокирует quality gate и release.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_reports(
    summary: AuditSummary,
    problems: Sequence[EncodingProblem],
    json_report: Path | None,
    markdown_report: Path | None,
    commit: str,
) -> None:
    if json_report:
        json_report.parent.mkdir(parents=True, exist_ok=True)
        payload = {"commit": commit, "summary": asdict(summary), "problems": [asdict(problem) for problem in problems]}
        json_report.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    if markdown_report:
        markdown_report.parent.mkdir(parents=True, exist_ok=True)
        markdown_report.write_text(render_markdown(summary, problems, commit), encoding="utf-8", newline="")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    summary, problems = audit(args.root, fix_safe=args.fix_safe)
    write_reports(summary, problems, args.json_report, args.markdown_report, args.commit)
    for problem in problems[:MAX_PRINTED_PROBLEMS]:
        print(f"{problem.path}: {problem.category}: {problem.detail}")
    if len(problems) > MAX_PRINTED_PROBLEMS:
        print(f"... показано {MAX_PRINTED_PROBLEMS} из {len(problems)} проблем")
    print(
        "UTF-8/mojibake summary: "
        f"checked={summary.checked_files}, invalid_utf8={summary.invalid_utf8_files}, "
        f"mojibake={summary.mojibake_files}, allowed={summary.allowed_marker_files}, "
        f"fixed={summary.fixed_files}, problems={summary.problems}"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
