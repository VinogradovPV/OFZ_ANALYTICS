"""Offline smoke для background command runner GUI."""

from __future__ import annotations

import sys
import threading
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.gui_launcher.actions import ActionPlan, CommandStep
from scripts.gui_launcher.command_runner import CommandRunner, RunResult


def main() -> int:
    root = Path.cwd()
    output: list[str] = []
    completed: list[RunResult] = []
    event = threading.Event()
    plan = ActionPlan(
        "runner-smoke",
        "Test-only fixed command plan.",
        (
            CommandStep(
                "Runner smoke",
                (
                    sys.executable,
                    "-c",
                    "import os, time; print('runner smoke'); print(os.environ.get('PYTHONUTF8')); print(os.environ.get('PYTHONIOENCODING')); time.sleep(0.2)",
                ),
            ),
        ),
    )
    log_dir = root / ".ofz_launcher" / "logs"
    runner = CommandRunner(root, log_dir)

    def complete(result: RunResult) -> None:
        completed.append(result)
        event.set()

    log_path = runner.start(plan, output.append, complete)
    try:
        runner.start(plan, output.append, complete)
    except RuntimeError:
        pass
    else:
        raise AssertionError("parallel command was not blocked")
    if not event.wait(10):
        raise AssertionError("runner did not complete")
    assert completed[0].exit_code == 0, "".join(output)
    output_text = "".join(output)
    assert "runner smoke" in output_text
    assert "utf-8" in output_text
    assert completed[0].output_tail
    assert not completed[0].saw_replacement_char
    assert log_path.read_text(encoding="utf-8").find("runner smoke") >= 0
    assert log_path.is_relative_to(log_dir)
    try:
        log_path.unlink()
    except OSError:
        pass
    print("GUI command runner smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
