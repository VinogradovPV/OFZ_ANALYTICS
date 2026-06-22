"""Allowlisted actions and command plans for the GUI launcher."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from .state import GuiState


class UnknownActionError(ValueError):
    """Запрошен action вне allowlist."""


class ConfirmationRequiredError(ValueError):
    """Typed confirm отсутствует или не совпадает."""


@dataclass(frozen=True)
class CommandStep:
    label: str
    args: tuple[str, ...]


@dataclass(frozen=True)
class ActionPlan:
    action_id: str
    description: str
    steps: tuple[CommandStep, ...]
    required_confirm: str = ""
    result_paths: tuple[Path, ...] = ()

    @property
    def dangerous(self) -> bool:
        return bool(self.required_confirm)


@dataclass(frozen=True)
class ActionDefinition:
    action_id: str
    description: str
    builder: Callable[[GuiState], Iterable[CommandStep]]
    required_confirm: str = ""
    result_paths: Callable[[GuiState], Iterable[Path]] = lambda _state: ()


def executable(state: GuiState, name: str) -> str:
    return str(state.venv_scripts / name)


def python_step(state: GuiState, label: str, relative_script: str, *args: str) -> CommandStep:
    return CommandStep(label, (str(state.python_executable), relative_script, *args))


def cli_step(state: GuiState, label: str, cli: str, *args: str) -> CommandStep:
    return CommandStep(label, (executable(state, cli), *args))


def minfin_optional_args(state: GuiState) -> list[str]:
    args = ["--max-pages", str(state.max_pages)]
    if state.minfin_url.strip():
        args.extend(["--url", state.minfin_url.strip()])
    if state.html_file.strip():
        args.extend(["--html-file", state.html_file.strip()])
    return args


def minfin_step(
    state: GuiState,
    label: str,
    year: int,
    mode: str,
    operation: str,
    confirm: str = "",
    no_network: bool = False,
) -> CommandStep:
    args = ["--year", str(year), "--mode", mode, operation]
    args.extend(minfin_optional_args(state))
    if no_network or state.no_network:
        args.append("--no-network")
    if mode == "manual-import" and state.manual_file.strip():
        args.extend(["--manual-file", state.manual_file.strip()])
    if confirm:
        args.extend(["--confirm", confirm])
    return cli_step(state, label, "ofz-fetch-minfin.exe", *args)


def pipeline_step(state: GuiState) -> CommandStep:
    return cli_step(state, "Pipeline", "ofz-run.exe", *state.common_report_args())


def schema_step(state: GuiState) -> CommandStep:
    return cli_step(state, "Schema validation", "ofz-schema.exe", *state.common_report_args())


def pipeline_steps(state: GuiState, include_stage_zero: bool) -> list[CommandStep]:
    steps: list[CommandStep] = []
    if include_stage_zero and state.stage_zero_mode == "dry-run":
        steps.append(minfin_step(state, "Этап 0: Минфин dry-run", state.minfin_year, "monthly", "--dry-run"))
    elif include_stage_zero and state.stage_zero_mode == "download":
        steps.append(
            minfin_step(
                state,
                "Этап 0: Минфин download",
                state.minfin_year,
                "monthly",
                "--download",
                "DOWNLOAD_MINFIN_SOURCE",
            )
        )
    if state.run_schema_before_pipeline:
        steps.append(schema_step(state))
    steps.append(pipeline_step(state))
    return steps


def registry() -> dict[str, ActionDefinition]:
    """Вернуть полный allowlist GUI actions."""
    return {
        "check-environment": ActionDefinition(
            "check-environment",
            "Проверить Python и установленные зависимости.",
            lambda state: (
                CommandStep("Python version", (str(state.python_executable), "--version")),
                CommandStep("Pip check", (str(state.python_executable), "-m", "pip", "check")),
            ),
        ),
        "git-status": ActionDefinition(
            "git-status",
            "Показать fixed read-only Git status.",
            lambda _state: (CommandStep("Git status", ("git", "status", "--short", "--branch")),),
        ),
        "artifact-guard": ActionDefinition(
            "artifact-guard",
            "Проверить staged paths по artifact policy.",
            lambda state: (
                python_step(state, "Artifact guard", "scripts/qa/gui_artifact_guard.py"),
            ),
        ),
        "minfin-monthly-offline": ActionDefinition(
            "minfin-monthly-offline",
            "Monthly dry-run без сети; raw не изменяется.",
            lambda state: (minfin_step(state, "Monthly offline dry-run", state.minfin_year, "monthly", "--dry-run", no_network=True),),
            result_paths=lambda state: (state.project_root / "data/raw/minfin/ofz_auction_results/registry",),
        ),
        "minfin-monthly-live": ActionDefinition(
            "minfin-monthly-live",
            "Live discovery Минфина без скачивания.",
            lambda state: (minfin_step(state, "Monthly live dry-run", state.minfin_year, "monthly", "--dry-run"),),
        ),
        "minfin-monthly-download": ActionDefinition(
            "minfin-monthly-download",
            "Скачать выбранный monthly XLSX в controlled raw storage.",
            lambda state: (minfin_step(state, "Monthly download", state.minfin_year, "monthly", "--download", "DOWNLOAD_MINFIN_SOURCE"),),
            "DOWNLOAD_MINFIN_SOURCE",
        ),
        "minfin-annual-dry": ActionDefinition(
            "minfin-annual-dry",
            "Проверить annual-final candidate без скачивания.",
            lambda state: (minfin_step(state, "Annual-final dry-run", state.final_year, "annual-final", "--dry-run"),),
        ),
        "minfin-annual-download": ActionDefinition(
            "minfin-annual-download",
            "Создать annual final после controlled download.",
            lambda state: (minfin_step(state, "Annual-final download", state.final_year, "annual-final", "--download", "DOWNLOAD_MINFIN_SOURCE"),),
            "DOWNLOAD_MINFIN_SOURCE",
        ),
        "minfin-final-replace": ActionDefinition(
            "minfin-final-replace",
            "Заменить changed annual final после ручной проверки.",
            lambda state: (minfin_step(state, "Replace annual final", state.final_year, "annual-final", "--download", "REPLACE_MINFIN_FINAL"),),
            "REPLACE_MINFIN_FINAL",
        ),
        "minfin-manual-dry": ActionDefinition(
            "minfin-manual-dry",
            "Проверить локальный XLSX без импорта.",
            lambda state: (minfin_step(state, "Manual import dry-run", state.minfin_year, "manual-import", "--dry-run"),),
        ),
        "minfin-manual-import": ActionDefinition(
            "minfin-manual-import",
            "Импортировать проверенный локальный XLSX.",
            lambda state: (minfin_step(state, "Manual import", state.minfin_year, "manual-import", "--download", "IMPORT_MINFIN_FILE"),),
            "IMPORT_MINFIN_FILE",
        ),
        "pipeline": ActionDefinition(
            "pipeline",
            "Запустить основной pipeline.",
            lambda state: pipeline_steps(state, False),
            result_paths=lambda state: (state.project_root / "outputs",),
        ),
        "pipeline-stage-zero": ActionDefinition(
            "pipeline-stage-zero",
            "Последовательно выполнить Минфин stage 0, optional schema и pipeline.",
            lambda state: pipeline_steps(state, True),
            result_paths=lambda state: (state.project_root / "outputs",),
        ),
        "schema": ActionDefinition("schema", "Проверить схемы generated artifacts.", lambda state: (schema_step(state),)),
        "quality-fast": ActionDefinition(
            "quality-fast",
            "Запустить быстрый quality gate.",
            lambda state: (cli_step(state, "Quality fast", "ofz-quality.exe", "--fast", *state.common_report_args()),),
        ),
        "quality-full": ActionDefinition(
            "quality-full",
            "Запустить полный длительный quality gate.",
            lambda state: (cli_step(state, "Quality full", "ofz-quality.exe", "--full", *state.common_report_args()),),
        ),
        "encoding-mojibake": ActionDefinition(
            "encoding-mojibake",
            "Проверить UTF-8 и mojibake.",
            lambda state: (cli_step(state, "UTF-8 / Mojibake", "ofz-quality.exe", "--stage", "encoding-mojibake", *state.common_report_args()),),
        ),
        "source-acquisition-tests": ActionDefinition(
            "source-acquisition-tests",
            "Запустить offline parser/source acquisition tests.",
            lambda state: (python_step(state, "Source acquisition tests", "scripts/qa/minfin_source_acquisition_tests.py"),),
        ),
        "registry-smoke": ActionDefinition(
            "registry-smoke",
            "Запустить registry CSV/JSON smoke.",
            lambda state: (python_step(state, "Registry smoke", "scripts/qa/minfin_source_registry_smoke.py"),),
        ),
        "data-audit-registry-smoke": ActionDefinition(
            "data-audit-registry-smoke",
            "Запустить data audit registry smoke.",
            lambda state: (python_step(state, "Data audit registry smoke", "scripts/qa/minfin_data_audit_registry_smoke.py"),),
        ),
        "html-chart-qa": ActionDefinition(
            "html-chart-qa",
            "Проверить HTML chart contracts.",
            lambda state: (python_step(state, "HTML chart QA", "scripts/html_chart_qa.py", *state.common_report_args()),),
        ),
        "visual-auto": ActionDefinition(
            "visual-auto",
            "Visual regression auto с fallback.",
            lambda state: (python_step(state, "Visual regression auto", "scripts/visual_regression.py", "--mode", "auto", *state.common_report_args()),),
        ),
        "visual-screenshot": ActionDefinition(
            "visual-screenshot",
            "Visual regression с обязательным screenshot backend.",
            lambda state: (python_step(state, "Visual regression screenshot", "scripts/visual_regression.py", "--mode", "screenshot", *state.common_report_args()),),
        ),
        "release-dry": ActionDefinition(
            "release-dry",
            "Построить план release bundle без записи.",
            lambda state: (cli_step(state, "Release bundle dry-run", "ofz-build-release-bundle.exe", "--dry-run", *state.common_report_args()),),
        ),
        "release-build": ActionDefinition(
            "release-build",
            "Собрать внешний release bundle.",
            lambda state: (cli_step(state, "Build release bundle", "ofz-build-release-bundle.exe", "--include-outputs", "--confirm", "BUILD_RELEASE_BUNDLE", *state.common_report_args()),),
            "BUILD_RELEASE_BUNDLE",
            lambda state: (state.project_root / "releases",),
        ),
        "bi-dry": ActionDefinition(
            "bi-dry",
            "Построить план BI package без записи.",
            lambda state: (python_step(state, "BI package dry-run", "scripts/maintenance/build_bi_package.py", "--dry-run", *state.common_report_args()),),
        ),
        "bi-build": ActionDefinition(
            "bi-build",
            "Собрать внешний BI package.",
            lambda state: (python_step(state, "Build BI package", "scripts/maintenance/build_bi_package.py", "--include-outputs", "--confirm", "BUILD_BI_PACKAGE", *state.common_report_args()),),
            "BUILD_BI_PACKAGE",
            lambda state: (state.project_root / "releases" / "bi",),
        ),
        "cleanup-keep": ActionDefinition(
            "cleanup-keep",
            "Показать cleanup plan без удаления.",
            lambda state: (cli_step(state, "Cleanup dry-run", "ofz-clean-outputs.exe", "--dry-run"),),
        ),
        "cleanup-delete": ActionDefinition(
            "cleanup-delete",
            "Архивировать и удалить generated outputs.",
            lambda state: (cli_step(state, "Cleanup delete", "ofz-clean-outputs.exe", "--archive-all", "--delete-all", "--confirm", "DELETE_OUTPUTS"),),
            "DELETE_OUTPUTS",
        ),
    }


class ActionRegistry:
    """Единственная публичная точка построения command plans."""

    def __init__(self) -> None:
        self._definitions = registry()

    def action_ids(self) -> tuple[str, ...]:
        return tuple(self._definitions)

    def definition(self, action_id: str) -> ActionDefinition:
        try:
            return self._definitions[action_id]
        except KeyError as exc:
            raise UnknownActionError(f"Action не входит в allowlist: {action_id}") from exc

    def build(
        self,
        action_id: str,
        state: GuiState,
        confirm: str = "",
        validate_confirmation: bool = True,
    ) -> ActionPlan:
        state.validate()
        definition = self.definition(action_id)
        if action_id.startswith("minfin-manual-") and not state.manual_file.strip():
            raise ValueError("Для manual-import выберите --manual-file.")
        required_confirm = definition.required_confirm
        if action_id == "pipeline-stage-zero" and state.stage_zero_mode == "download":
            required_confirm = "DOWNLOAD_MINFIN_SOURCE"
        if validate_confirmation and required_confirm and confirm != required_confirm:
            raise ConfirmationRequiredError(
                f"Действие заблокировано. Введите exact token: {required_confirm}"
            )
        steps = tuple(definition.builder(state))
        if not steps or any(not step.args for step in steps):
            raise ValueError(f"Action {action_id} не сформировал команду.")
        return ActionPlan(
            action_id=action_id,
            description=definition.description,
            steps=steps,
            required_confirm=required_confirm,
            result_paths=tuple(definition.result_paths(state)),
        )


def open_path(path: Path) -> None:
    """Открыть существующий файл/каталог штатным приложением Windows."""
    target = path.resolve()
    if not target.exists():
        raise FileNotFoundError(f"Путь отсутствует: {target}. Сначала запустите pipeline.")
    os.startfile(target)  # type: ignore[attr-defined]
