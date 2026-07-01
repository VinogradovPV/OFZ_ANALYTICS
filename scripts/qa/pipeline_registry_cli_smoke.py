"""Smoke test for source registry flags in the canonical pipeline CLI."""

from __future__ import annotations

import contextlib
import io
import logging
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts import run_pipeline


ROOT = Path(__file__).resolve().parents[2]
OFZ_RUN = ROOT / ".venv" / "Scripts" / "ofz-run.exe"


def assert_contains(text: str, needle: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {needle!r}")


def run_help() -> str:
    result = subprocess.run(
        [str(OFZ_RUN), "--help"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)
    return result.stdout


def parse_invalid_mode_is_rejected() -> None:
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr):
        try:
            run_pipeline.parse_args(["--source-registry-mode", "invalid"])
        except SystemExit as exc:
            if exc.code != 2:
                raise AssertionError(f"Unexpected argparse exit code: {exc.code}") from exc
            return
    raise AssertionError("Invalid source registry mode was accepted")


def capture_stage_one_command(argv: list[str]) -> list[str]:
    args = run_pipeline.parse_args(["--stage", "1", *argv])
    captured: list[str] = []
    original_run = run_pipeline.subprocess.run

    def fake_run(command, **_kwargs):  # type: ignore[no-untyped-def]
        captured.extend(str(part) for part in command)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    run_pipeline.subprocess.run = fake_run  # type: ignore[assignment]
    try:
        run_pipeline.run_stage("1", args=args, logger=logging.getLogger("pipeline-registry-cli-smoke"))
    finally:
        run_pipeline.subprocess.run = original_run  # type: ignore[assignment]
    if not captured:
        raise AssertionError("Stage 1 command was not captured")
    return captured


def assert_stage_one_flags(command: list[str], mode: str, legacy_flag: str) -> None:
    assert_contains(" ".join(command), "01_data_audit.py")
    try:
        mode_index = command.index("--source-registry-mode")
    except ValueError as exc:
        raise AssertionError("Stage 1 command lacks --source-registry-mode") from exc
    if command[mode_index + 1] != mode:
        raise AssertionError(f"Unexpected registry mode: {command[mode_index + 1]!r}")
    if legacy_flag not in command:
        raise AssertionError(f"Stage 1 command lacks {legacy_flag}")


def main() -> int:
    help_text = run_help()
    assert_contains(help_text, "--source-registry-mode")
    assert_contains(help_text, "--allow-legacy-raw")
    assert_contains(help_text, "--no-allow-legacy-raw")

    default_args = run_pipeline.parse_args(["--stage", "1"])
    if default_args.source_registry_mode != "warn":
        raise AssertionError("Default source registry mode changed")
    if default_args.allow_legacy_raw is not True:
        raise AssertionError("Default legacy raw fallback changed")
    assert_stage_one_flags(capture_stage_one_command([]), "warn", "--allow-legacy-raw")
    assert_stage_one_flags(
        capture_stage_one_command(["--source-registry-mode", "strict", "--no-allow-legacy-raw"]),
        "strict",
        "--no-allow-legacy-raw",
    )
    parse_invalid_mode_is_rejected()
    print("Pipeline registry CLI smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
