"""Контрактный smoke нового OFZ GUI launcher."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.gui_launcher.actions import (
    ActionRegistry,
    ConfirmationRequiredError,
    UnknownActionError,
)
from scripts.gui_launcher.app import TAB_TITLES
from scripts.gui_launcher.help_text import HELP_TEXT
from scripts.gui_launcher.state import GuiState


def expect_error(error_type, callback, message: str) -> None:
    try:
        callback()
    except error_type:
        return
    raise AssertionError(message)


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    state = GuiState(project_root=root)
    state.validate()
    registry = ActionRegistry()

    required_actions = {
        "minfin-monthly-offline",
        "minfin-monthly-download",
        "pipeline-stage-zero",
        "quality-fast",
        "release-build",
        "cleanup-delete",
    }
    assert required_actions.issubset(registry.action_ids())
    assert TAB_TITLES == (
        "Обзор",
        "Исходные данные Минфина",
        "Pipeline",
        "Проверки качества",
        "Отчеты и графики",
        "Release и пакеты",
        "Обслуживание",
        "Журнал",
        "Справка",
    )

    monthly = registry.build("minfin-monthly-offline", state)
    assert "--no-network" in monthly.steps[0].args
    expect_error(
        ConfirmationRequiredError,
        lambda: registry.build("minfin-monthly-download", state),
        "monthly download was not blocked",
    )
    registry.build("minfin-monthly-download", state, confirm="DOWNLOAD_MINFIN_SOURCE")

    state.stage_zero_mode = "download"
    expect_error(
        ConfirmationRequiredError,
        lambda: registry.build("pipeline-stage-zero", state),
        "stage zero download was not blocked",
    )
    stage_zero = registry.build("pipeline-stage-zero", state, confirm="DOWNLOAD_MINFIN_SOURCE")
    assert len(stage_zero.steps) == 2
    assert "ofz-fetch-minfin.exe" in stage_zero.steps[0].args[0]
    assert "ofz-run.exe" in stage_zero.steps[-1].args[0]

    expect_error(
        ValueError,
        lambda: registry.build("minfin-manual-dry", state),
        "manual import without file was not blocked",
    )
    expect_error(
        UnknownActionError,
        lambda: registry.build("arbitrary-shell-command", state),
        "unknown action was accepted",
    )
    state.manual_file = str(root / "tests/fixtures/manual_smoke_placeholder.xlsx")
    for action_id in registry.action_ids():
        plan = registry.build(action_id, state, validate_confirmation=False)
        assert plan.steps, f"empty plan: {action_id}"
        assert all(step.args for step in plan.steps), f"empty command: {action_id}"
    assert "Минфин -> source registry -> pipeline" in HELP_TEXT
    assert HELP_TEXT.strip()
    print(f"GUI launcher smoke passed. Actions: {len(registry.action_ids())}; tabs: {len(TAB_TITLES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
