"""Контрактный smoke нового OFZ GUI launcher."""

from __future__ import annotations

import sys
import inspect
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.gui_launcher.actions import (
    ActionRegistry,
    ConfirmationRequiredError,
    UnknownActionError,
)
from scripts.gui_launcher.app import (
    MINFIN_ADVANCED_CONTROL_LABELS,
    MINFIN_BASIC_CONTROL_LABELS,
    NO_RESULT_POPUP_TEXT,
    PREVIEW_PLACEHOLDER,
    REGISTRY_MODE_LABEL_TO_VALUE,
    REGISTRY_MODE_VALUE_TO_LABEL,
    STAGE_ZERO_LABEL_TO_MODE,
    TAB_INFO,
    TAB_TITLES,
    OfzAnalyticsGui,
)
from scripts.gui_launcher.help_text import HELP_TEXT
from scripts.gui_launcher.state import GuiState
from scripts.gui_launcher.command_runner import RunResult


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
    assert set(TAB_INFO) == set(TAB_TITLES)
    for title, rows in TAB_INFO.items():
        assert len(rows) == 4, f"description block is incomplete: {title}"
        assert all(row.strip() for row in rows), f"description block has empty row: {title}"
    assert "Не выполнять" in STAGE_ZERO_LABEL_TO_MODE
    assert "Только dry-run" in STAGE_ZERO_LABEL_TO_MODE
    assert "Download с подтверждением" in STAGE_ZERO_LABEL_TO_MODE
    assert STAGE_ZERO_LABEL_TO_MODE["Только dry-run"] == "dry-run"
    assert REGISTRY_MODE_LABEL_TO_VALUE["Проверять и предупреждать"] == "warn"
    assert REGISTRY_MODE_VALUE_TO_LABEL[state.source_registry_mode] == "Проверять и предупреждать"
    assert state.launcher_log_dir == root / ".ofz_launcher" / "logs"
    assert "Выберите действие на вкладке" in PREVIEW_PLACEHOLDER
    basic_controls = set(MINFIN_BASIC_CONTROL_LABELS)
    advanced_controls = set(MINFIN_ADVANCED_CONTROL_LABELS)
    assert "Проверить сайт Минфина" in basic_controls
    assert "Обновить данные текущего года" in basic_controls
    assert "Закрыть предыдущий год" in basic_controls
    assert "URL override" not in basic_controls
    assert "HTML fixture" not in basic_controls
    assert "No network" not in basic_controls
    assert "Max pages" not in basic_controls
    assert "Manual XLSX" in advanced_controls
    assert "URL override" in advanced_controls
    assert "HTML fixture" in advanced_controls
    assert "No network" in advanced_controls
    assert "Max pages" in advanced_controls
    assert "Replace changed final" in advanced_controls

    monthly = registry.build("minfin-monthly-offline", state)
    assert "--no-network" in monthly.steps[0].args
    assert not registry.build("check-environment", state).has_results
    assert not registry.build("git-status", state).has_results
    assert not monthly.has_results
    live = registry.build("minfin-monthly-live", state)
    assert "--dry-run" in live.steps[0].args
    assert "--no-network" not in live.steps[0].args
    assert not live.has_results
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
    assert stage_zero.has_results
    assert len(stage_zero.steps) == 2
    assert "ofz-fetch-minfin.exe" in stage_zero.steps[0].args[0]
    assert "ofz-run.exe" in stage_zero.steps[-1].args[0]
    state.stage_zero_mode = "dry-run"
    stage_zero_dry = registry.build("pipeline-stage-zero", state)
    assert "--dry-run" in stage_zero_dry.steps[0].args
    assert "--download" not in stage_zero_dry.steps[0].args

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
    assert registry.build("release-build", state, validate_confirmation=False).has_results
    assert registry.build("bi-build", state, validate_confirmation=False).has_results
    assert registry.build("quality-fast", state).user_success_message
    assert registry.build("encoding-mojibake", state).user_failure_hint
    assert "Папка результатов еще не создана" in NO_RESULT_POPUP_TEXT
    assert "Для action не задана отдельная папка результатов" != NO_RESULT_POPUP_TEXT
    confirm_source = inspect.getsource(OfzAnalyticsGui._ask_confirm_token)
    assert confirm_source.index("token = plan.required_confirm") < confirm_source.index('if token == "DELETE_OUTPUTS"')
    success = RunResult("smoke", 0, root / "smoke.log", "cmd")
    failed = RunResult("smoke", 1, root / "smoke.log", "cmd")
    assert success.exit_code == 0
    assert failed.exit_code != 0
    assert "Минфин -> source registry -> pipeline" in HELP_TEXT
    assert HELP_TEXT.strip()
    print(f"GUI launcher smoke passed. Actions: {len(registry.action_ids())}; tabs: {len(TAB_TITLES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
