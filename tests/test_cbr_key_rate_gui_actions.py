from __future__ import annotations

import importlib
from pathlib import Path

import pytest

from scripts.gui_launcher.actions import ActionRegistry, ConfirmationRequiredError
from scripts.gui_launcher.state import GuiState


ROOT = Path(__file__).resolve().parents[1]


def test_cbr_gui_actions_build_expected_commands() -> None:
    state = GuiState(project_root=ROOT)
    registry = ActionRegistry()

    web_dry = registry.build("cbr-key-rate-web-dry", state)
    web_dry_args = web_dry.steps[0].args
    assert web_dry_args[:3] == (str(state.python_executable), "scripts/reference_data/cbr_key_rate.py", "--source")
    assert "web" in web_dry_args
    assert "--dry-run" in web_dry_args
    assert "--from-date" in web_dry_args
    assert "--to-date" in web_dry_args

    html_fixture = registry.build("cbr-key-rate-html-fixture", state)
    html_args = html_fixture.steps[0].args
    assert "--source" in html_args
    assert html_args[html_args.index("--source") + 1] == "html-file"
    assert "--html-file" in html_args
    assert "--dry-run" in html_args

    xlsx_fallback = registry.build("cbr-key-rate-xlsx-fallback", state)
    xlsx_args = xlsx_fallback.steps[0].args
    assert "--source" in xlsx_args
    assert xlsx_args[xlsx_args.index("--source") + 1] == "xlsx"
    assert "--input-file" in xlsx_args
    assert "--dry-run" in xlsx_args


def test_cbr_web_update_requires_confirmation_and_has_reference_results() -> None:
    state = GuiState(project_root=ROOT)
    registry = ActionRegistry()

    with pytest.raises(ConfirmationRequiredError):
        registry.build("cbr-key-rate-web-update", state)

    plan = registry.build("cbr-key-rate-web-update", state, confirm="UPDATE_CBR_KEY_RATE")
    args = plan.steps[0].args
    assert plan.required_confirm == "UPDATE_CBR_KEY_RATE"
    assert "--dry-run" not in args
    assert plan.result_paths == (
        ROOT / "data/processed/reference/cbr_key_rate_daily.csv",
        ROOT / "data/processed/reference/cbr_key_rate_monthly.csv",
        ROOT / "data/processed/reference/cbr_key_rate_daily.meta.json",
    )


def test_importing_gui_app_does_not_start_network() -> None:
    module = importlib.import_module("scripts.gui_launcher.app")
    assert module.TAB_TITLES[2] == "Банк России"
    assert "Банк России" in module.TAB_INFO
