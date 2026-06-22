"""Безопасный background runner для allowlisted GUI command plans."""

from __future__ import annotations

import subprocess
import threading
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

from .actions import ActionPlan, CommandStep


OutputCallback = Callable[[str], None]
CompletionCallback = Callable[["RunResult"], None]


@dataclass(frozen=True)
class RunResult:
    action_id: str
    exit_code: int
    log_path: Path
    last_command: str
    stopped: bool = False


def format_command(args: tuple[str, ...]) -> str:
    return subprocess.list2cmdline(list(args))


def format_plan(plan: ActionPlan) -> str:
    return "\n".join(f"{index}. {format_command(step.args)}" for index, step in enumerate(plan.steps, 1))


class CommandRunner:
    """Выполняет только готовый ActionPlan, никогда не принимает shell-строку."""

    def __init__(self, project_root: Path, log_dir: Path) -> None:
        self.project_root = project_root.resolve()
        self.log_dir = log_dir.resolve()
        self._lock = threading.Lock()
        self._process: subprocess.Popen[str] | None = None
        self._thread: threading.Thread | None = None
        self._stop_requested = False

    @property
    def is_running(self) -> bool:
        with self._lock:
            return self._thread is not None and self._thread.is_alive()

    def start(
        self,
        plan: ActionPlan,
        on_output: OutputCallback,
        on_complete: CompletionCallback,
    ) -> Path:
        with self._lock:
            if self._thread is not None and self._thread.is_alive():
                raise RuntimeError("Другая команда уже выполняется.")
            self._stop_requested = False
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            log_path = self.log_dir / f"gui_run_{timestamp}.log"
            self._thread = threading.Thread(
                target=self._run,
                args=(plan, log_path, on_output, on_complete),
                daemon=True,
            )
            self._thread.start()
        return log_path

    def _run(
        self,
        plan: ActionPlan,
        log_path: Path,
        on_output: OutputCallback,
        on_complete: CompletionCallback,
    ) -> None:
        exit_code = 0
        last_command = ""
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            minfin_unavailable = False
            with log_path.open("w", encoding="utf-8", newline="") as log_file:
                self._emit(log_file, on_output, f"Action: {plan.action_id}\n{plan.description}\n")
                for index, step in enumerate(plan.steps, 1):
                    if self._stop_requested:
                        exit_code = 130
                        break
                    last_command = format_command(step.args)
                    self._emit(log_file, on_output, f"\n[{index}/{len(plan.steps)}] {step.label}\n$ {last_command}\n")
                    exit_code, saw_503 = self._run_step(step, log_file, on_output)
                    minfin_unavailable = minfin_unavailable or saw_503
                    self._emit(log_file, on_output, f"Exit code: {exit_code}\n")
                    if exit_code != 0:
                        self._emit(log_file, on_output, "Последовательность остановлена: предыдущий этап завершился с ошибкой.\n")
                        break
                if minfin_unavailable:
                    self._emit(log_file, on_output, "Сайт Минфина временно недоступен; raw не изменен.\n")
        except Exception as exc:  # Ошибка runner должна вернуться в GUI, а не потеряться в thread.
            exit_code = 1
            on_output(f"Runner error: {exc}\n")
        result = RunResult(plan.action_id, exit_code, log_path, last_command, self._stop_requested)
        on_complete(result)

    def _run_step(self, step: CommandStep, log_file, on_output: OutputCallback) -> tuple[int, bool]:
        process = subprocess.Popen(
            list(step.args),
            cwd=self.project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
        )
        with self._lock:
            self._process = process
        saw_503 = False
        assert process.stdout is not None
        for line in process.stdout:
            saw_503 = saw_503 or "503" in line
            self._emit(log_file, on_output, line)
        exit_code = process.wait()
        with self._lock:
            self._process = None
        return exit_code, saw_503

    @staticmethod
    def _emit(log_file, on_output: OutputCallback, text: str) -> None:
        log_file.write(text)
        log_file.flush()
        on_output(text)

    def stop(self) -> bool:
        with self._lock:
            process = self._process
            if process is None or process.poll() is not None:
                return False
            self._stop_requested = True
            process.terminate()
            return True
