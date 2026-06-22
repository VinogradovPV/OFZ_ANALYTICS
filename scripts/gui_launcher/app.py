"""Полноценный desktop GUI launcher OFZ_ANALYTICS на tkinter."""

from __future__ import annotations

import argparse
import sys
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Callable

from . import actions
from .actions import ActionPlan, ActionRegistry
from .command_runner import CommandRunner, RunResult, format_plan
from .help_text import HELP_TEXT
from .state import GuiState
from .widgets import add_action_row, add_intro, add_labeled_combo, add_labeled_entry, make_scrolled_text


TAB_TITLES = (
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


@dataclass
class ButtonGate:
    button: ttk.Button
    action_id: str
    confirm_var: tk.StringVar | None = None
    condition: Callable[[], bool] | None = None


class OfzAnalyticsGui:
    """Основное окно с пользовательскими сценариями OFZ_ANALYTICS."""

    def __init__(self, root: tk.Tk, state: GuiState) -> None:
        self.root = root
        self.state = state
        self.registry = ActionRegistry()
        self.runner = CommandRunner(state.project_root, state.launcher_log_dir)
        self.selected_action_id = ""
        self.selected_confirm_var: tk.StringVar | None = None
        self.selected_plan: ActionPlan | None = None
        self.button_gates: list[ButtonGate] = []
        self.last_log_path: Path | None = None
        self.last_exit_code: int | None = None

        self.root.title("OFZ Analytics")
        self.root.geometry("1280x860")
        self.root.minsize(1060, 720)
        self.status_var = tk.StringVar(value="Готово")
        self.last_command_var = tk.StringVar(value="Команда еще не выполнялась")
        self.exit_code_var = tk.StringVar(value="Exit code: -")
        self.log_path_var = tk.StringVar(value="Log: -")
        self._create_variables()
        self._configure_style()
        self._build()
        self._refresh_button_states()

    def _create_variables(self) -> None:
        self.project_root_var = tk.StringVar(value=str(self.state.project_root))
        self.report_date_var = tk.StringVar(value=self.state.report_date)
        self.years_var = tk.StringVar(value=str(self.state.retrospective_years))
        self.period_type_var = tk.StringVar(value=self.state.period_type)
        self.aggregation_var = tk.StringVar(value=self.state.aggregation_mode)
        self.registry_mode_var = tk.StringVar(value=self.state.source_registry_mode)
        self.allow_legacy_var = tk.BooleanVar(value=self.state.allow_legacy_raw)
        self.minfin_year_var = tk.StringVar(value=str(self.state.minfin_year))
        self.final_year_var = tk.StringVar(value=str(self.state.final_year))
        self.minfin_mode_var = tk.StringVar(value=self.state.minfin_mode)
        self.minfin_url_var = tk.StringVar(value=self.state.minfin_url)
        self.max_pages_var = tk.StringVar(value=str(self.state.max_pages))
        self.no_network_var = tk.BooleanVar(value=self.state.no_network)
        self.html_file_var = tk.StringVar(value=self.state.html_file)
        self.manual_file_var = tk.StringVar(value=self.state.manual_file)
        self.minfin_confirm_var = tk.StringVar()
        self.stage_zero_var = tk.StringVar(value=self.state.stage_zero_mode)
        self.schema_before_var = tk.BooleanVar(value=self.state.run_schema_before_pipeline)
        self.open_outputs_var = tk.BooleanVar(value=self.state.open_outputs_after_run)
        self.pipeline_confirm_var = tk.StringVar()
        self.release_confirm_var = tk.StringVar()
        self.maintenance_confirm_var = tk.StringVar()
        for variable in (
            self.minfin_confirm_var,
            self.manual_file_var,
            self.pipeline_confirm_var,
            self.release_confirm_var,
            self.maintenance_confirm_var,
            self.stage_zero_var,
        ):
            variable.trace_add("write", lambda *_args: self._refresh_button_states())

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure("Status.TLabel", padding=(8, 5))

    def _build(self) -> None:
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=(8, 4))
        self._build_overview_tab()
        self._build_minfin_tab()
        self._build_pipeline_tab()
        self._build_quality_tab()
        self._build_reports_tab()
        self._build_release_tab()
        self._build_maintenance_tab()
        self._build_log_tab()
        self._build_help_tab()
        self._build_command_bar()
        ttk.Label(self.root, textvariable=self.status_var, style="Status.TLabel", anchor="w").pack(fill="x")

    def _new_tab(self, title: str) -> ttk.Frame:
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=title)
        return tab

    def _build_overview_tab(self) -> None:
        tab = self._new_tab("Обзор")
        add_intro(tab, "Здесь задаются общие параметры запуска. Они используются в pipeline, quality checks, chart QA и release bundle.")
        form = ttk.LabelFrame(tab, text="Общие параметры")
        form.pack(fill="x", padx=10, pady=6)
        form.columnconfigure(1, weight=1)
        add_labeled_entry(form, 0, "Project root", self.project_root_var, 72)
        ttk.Button(form, text="Выбрать папку", command=self._choose_project_root).grid(row=0, column=2, padx=5, pady=4)
        add_labeled_entry(form, 1, "Report date", self.report_date_var)
        add_labeled_entry(form, 1, "Retrospective years", self.years_var, 8, column=2)
        add_labeled_combo(form, 2, "Period type", self.period_type_var, ("month", "quarter", "year"))
        add_labeled_combo(form, 2, "Aggregation mode", self.aggregation_var, ("cumulative", "point"), column=2)
        add_labeled_combo(form, 3, "Source registry mode", self.registry_mode_var, ("off", "warn", "strict"))
        ttk.Checkbutton(form, text="Allow legacy raw", variable=self.allow_legacy_var).grid(row=3, column=2, columnspan=2, sticky="w", padx=5)
        actions_frame = ttk.LabelFrame(tab, text="Диагностика")
        actions_frame.pack(fill="x", padx=10, pady=6)
        self._action_row(actions_frame, "Проверить окружение", "Python version и pip check.", "check-environment")
        self._action_row(actions_frame, "Проверить Git статус", "Fixed read-only git status, без destructive actions.", "git-status")

    def _build_minfin_tab(self) -> None:
        tab = self._new_tab("Исходные данные Минфина")
        add_intro(tab, "Эта вкладка получает исходные XLSX Минфина. Dry-run безопасен. Download меняет controlled raw storage. versions/ не коммитится.")
        form = ttk.LabelFrame(tab, text="Параметры source acquisition")
        form.pack(fill="x", padx=10, pady=6)
        form.columnconfigure(1, weight=1)
        add_labeled_entry(form, 0, "Year", self.minfin_year_var, 10)
        add_labeled_entry(form, 0, "Final year", self.final_year_var, 10, column=2)
        add_labeled_combo(form, 1, "Mode", self.minfin_mode_var, ("monthly", "annual-final", "manual-import"))
        add_labeled_entry(form, 1, "Max pages", self.max_pages_var, 10, column=2)
        add_labeled_entry(form, 2, "URL override", self.minfin_url_var, 68)
        ttk.Checkbutton(form, text="No network", variable=self.no_network_var).grid(row=2, column=2, sticky="w", padx=5)
        add_labeled_entry(form, 3, "HTML fixture", self.html_file_var, 68)
        ttk.Button(form, text="Выбрать HTML", command=self._choose_html).grid(row=3, column=2, padx=5)
        add_labeled_entry(form, 4, "Manual XLSX", self.manual_file_var, 68)
        ttk.Button(form, text="Выбрать XLSX", command=self._choose_manual).grid(row=4, column=2, padx=5)
        add_labeled_entry(form, 5, "Typed confirm", self.minfin_confirm_var, 32)
        actions_frame = ttk.LabelFrame(tab, text="Действия")
        actions_frame.pack(fill="both", expand=True, padx=10, pady=6)
        self._action_row(actions_frame, "Monthly dry-run без сети", "Offline plan; можно использовать HTML fixture.", "minfin-monthly-offline")
        self._action_row(actions_frame, "Monthly live dry-run", "Получить кандидатов с сайта без download.", "minfin-monthly-live")
        self._action_row(actions_frame, "Monthly download", "Требует DOWNLOAD_MINFIN_SOURCE.", "minfin-monthly-download", self.minfin_confirm_var)
        self._action_row(actions_frame, "Annual-final dry-run", "Проверить final candidate предыдущего года.", "minfin-annual-dry")
        self._action_row(actions_frame, "Annual-final download", "Требует DOWNLOAD_MINFIN_SOURCE.", "minfin-annual-download", self.minfin_confirm_var)
        self._action_row(actions_frame, "Replace changed final", "Требует REPLACE_MINFIN_FINAL после review.", "minfin-final-replace", self.minfin_confirm_var)
        self._action_row(actions_frame, "Manual import dry-run", "Проверить выбранный XLSX.", "minfin-manual-dry", condition=self._manual_file_selected)
        self._action_row(actions_frame, "Manual import", "Требует XLSX и IMPORT_MINFIN_FILE.", "minfin-manual-import", self.minfin_confirm_var, self._manual_file_selected)
        toolbar = ttk.Frame(tab)
        toolbar.pack(fill="x", padx=10, pady=4)
        ttk.Button(toolbar, text="Открыть registry", command=lambda: self._open_path(self.state.project_root / "data/raw/minfin/ofz_auction_results/registry")).pack(side="left")
        ttk.Button(toolbar, text="Открыть source reports", command=lambda: self._open_path(self.state.project_root / "outputs/reports/source_acquisition")).pack(side="left", padx=6)

    def _build_pipeline_tab(self) -> None:
        tab = self._new_tab("Pipeline")
        add_intro(tab, "Pipeline выполняется напрямую из GUI. Stage 0 по умолчанию является dry-run; download требует explicit confirm.")
        options = ttk.LabelFrame(tab, text="Pipeline workflow")
        options.pack(fill="x", padx=10, pady=6)
        add_labeled_combo(options, 0, "Этап 0 Минфина", self.stage_zero_var, ("off", "dry-run", "download"))
        ttk.Checkbutton(options, text="Run schema before pipeline", variable=self.schema_before_var).grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=4)
        ttk.Checkbutton(options, text="Open outputs after run", variable=self.open_outputs_var).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=4)
        add_labeled_entry(options, 3, "Stage 0 typed confirm", self.pipeline_confirm_var, 32)
        actions_frame = ttk.LabelFrame(tab, text="Запуск")
        actions_frame.pack(fill="x", padx=10, pady=6)
        self._action_row(actions_frame, "Запустить pipeline", "Без source acquisition stage 0.", "pipeline")
        self._action_row(
            actions_frame,
            "Запустить pipeline с этапом 0",
            "При non-zero stage 0/schema дальнейшие команды не запускаются.",
            "pipeline-stage-zero",
            self.pipeline_confirm_var,
            self._pipeline_stage_zero_ready,
        )

    def _build_quality_tab(self) -> None:
        tab = self._new_tab("Проверки качества")
        add_intro(tab, "Проверки выполняются последовательно: одновременно может работать только одна команда. Quality full является длительной pre-release проверкой.")
        actions_frame = ttk.LabelFrame(tab, text="Quality и targeted QA")
        actions_frame.pack(fill="both", expand=True, padx=10, pady=6)
        rows = (
            ("UTF-8 / Mojibake", "Strict encoding quality stage.", "encoding-mojibake"),
            ("Schema validation", "Проверить generated schemas.", "schema"),
            ("Quality fast", "Обычный быстрый gate.", "quality-fast"),
            ("Quality full", "Длительная полная проверка.", "quality-full"),
            ("Source acquisition tests", "Offline parser, selection и failure modes.", "source-acquisition-tests"),
            ("Registry smoke", "CSV/JSON registry roundtrip и hash.", "registry-smoke"),
            ("Data audit registry smoke", "off/warn/strict и legacy fallback.", "data-audit-registry-smoke"),
            ("HTML chart QA", "HTML contracts и подписи.", "html-chart-qa"),
            ("Visual regression auto", "Screenshot при доступности, иначе fallback.", "visual-auto"),
            ("Visual regression screenshot", "Требует работающий browser backend.", "visual-screenshot"),
        )
        for title, description, action_id in rows:
            self._action_row(actions_frame, title, description, action_id)

    def _build_reports_tab(self) -> None:
        tab = self._new_tab("Отчеты и графики")
        add_intro(tab, "Generated outputs не коммитятся. Quick links позволяют вручную проверить исправленные yield artifacts ОФЗ-ПД.")
        frame = ttk.LabelFrame(tab, text="Открыть результаты")
        frame.pack(fill="x", padx=10, pady=6)
        buttons = (
            ("Открыть charts", lambda: self._open_path(self.state.project_root / "outputs/charts")),
            ("Открыть exports", lambda: self._open_path(self.state.project_root / "outputs/exports")),
            ("Открыть reports", lambda: self._open_path(self.state.project_root / "outputs/reports")),
            ("Monthly metrics XLSX", self._open_monthly_metrics),
            ("Weighted yield ОФЗ-ПД", self._open_weighted_yield),
            ("Yield min/median/max", self._open_weighted_yield),
            ("Revenue charts", lambda: self._open_path(self.state.project_root / "outputs/charts/revenue")),
            ("Telemetry reports", lambda: self._open_path(self.state.project_root / "outputs/reports/telemetry")),
            ("Run manifest", self._open_run_manifest),
        )
        for index, (title, command) in enumerate(buttons):
            ttk.Button(frame, text=title, command=command, width=30).grid(row=index // 3, column=index % 3, padx=8, pady=8, sticky="ew")
        for column in range(3):
            frame.columnconfigure(column, weight=1)

    def _build_release_tab(self) -> None:
        tab = self._new_tab("Release и пакеты")
        add_intro(tab, "Сначала используйте dry-run. Build пишет во внешний ignored releases/ и требует typed confirm.")
        form = ttk.LabelFrame(tab, text="Подтверждение")
        form.pack(fill="x", padx=10, pady=6)
        add_labeled_entry(form, 0, "Typed confirm", self.release_confirm_var, 32)
        actions_frame = ttk.LabelFrame(tab, text="Release actions")
        actions_frame.pack(fill="x", padx=10, pady=6)
        self._action_row(actions_frame, "Release bundle dry-run", "Проверить план bundle без записи.", "release-dry")
        self._action_row(actions_frame, "Build release bundle", "Требует BUILD_RELEASE_BUNDLE.", "release-build", self.release_confirm_var)
        self._action_row(actions_frame, "BI package dry-run", "Проверить BI handoff plan.", "bi-dry")
        self._action_row(actions_frame, "Build BI package", "Требует BUILD_BI_PACKAGE.", "bi-build", self.release_confirm_var)
        ttk.Button(tab, text="Открыть releases", command=lambda: self._open_path(self.state.project_root / "releases")).pack(anchor="w", padx=12, pady=8)

    def _build_maintenance_tab(self) -> None:
        tab = self._new_tab("Обслуживание")
        add_intro(tab, "Диагностика и cleanup. Artifact guard и Git status являются fixed read-only actions; произвольной shell-команды нет.")
        form = ttk.LabelFrame(tab, text="Подтверждение удаления")
        form.pack(fill="x", padx=10, pady=6)
        add_labeled_entry(form, 0, "Typed confirm", self.maintenance_confirm_var, 32)
        actions_frame = ttk.LabelFrame(tab, text="Actions")
        actions_frame.pack(fill="x", padx=10, pady=6)
        self._action_row(actions_frame, "Git status", "Read-only diagnostic.", "git-status")
        self._action_row(actions_frame, "Artifact guard", "Проверить staged generated paths.", "artifact-guard")
        self._action_row(actions_frame, "Cleanup keep / dry-run", "Показать план без удаления.", "cleanup-keep")
        self._action_row(actions_frame, "Cleanup delete outputs", "Архивирование и удаление; требует DELETE_OUTPUTS.", "cleanup-delete", self.maintenance_confirm_var)
        folders = ttk.Frame(tab)
        folders.pack(fill="x", padx=10, pady=8)
        for title, relative in (
            ("Project root", "."),
            ("data/raw", "data/raw"),
            ("outputs", "outputs"),
            ("logs", "logs"),
        ):
            ttk.Button(folders, text=f"Открыть {title}", command=lambda value=relative: self._open_path(self.state.project_root / value)).pack(side="left", padx=4)

    def _build_log_tab(self) -> None:
        tab = self._new_tab("Журнал")
        header = ttk.Frame(tab)
        header.pack(fill="x", padx=8, pady=6)
        ttk.Label(header, textvariable=self.last_command_var).pack(anchor="w")
        ttk.Label(header, textvariable=self.exit_code_var).pack(anchor="w")
        ttk.Label(header, textvariable=self.log_path_var).pack(anchor="w")
        self.log_text = make_scrolled_text(tab, height=24)
        toolbar = ttk.Frame(tab)
        toolbar.pack(fill="x", padx=8, pady=6)
        ttk.Button(toolbar, text="Остановить", command=self._stop_command).pack(side="left")
        ttk.Button(toolbar, text="Очистить журнал", command=lambda: self.log_text.delete("1.0", "end")).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Копировать журнал", command=self._copy_log).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Открыть log-файл", command=self._open_last_log).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Открыть папку logs", command=lambda: self._open_path(self.state.launcher_log_dir)).pack(side="left", padx=5)

    def _build_help_tab(self) -> None:
        tab = self._new_tab("Справка")
        text = make_scrolled_text(tab, height=30)
        text.insert("1.0", HELP_TEXT)
        text.configure(state="disabled")

    def _build_command_bar(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Выбранное действие и command preview")
        frame.pack(fill="x", padx=8, pady=4)
        self.preview_text = tk.Text(frame, height=3, wrap="word")
        self.preview_text.pack(side="left", fill="both", expand=True, padx=6, pady=5)
        self.preview_text.configure(state="disabled")
        buttons = ttk.Frame(frame)
        buttons.pack(side="right", padx=6)
        self.execute_button = ttk.Button(buttons, text="Выполнить", command=self._execute_selected, state="disabled")
        self.execute_button.pack(fill="x", pady=2)
        ttk.Button(buttons, text="Копировать команду", command=self._copy_preview).pack(fill="x", pady=2)
        ttk.Button(buttons, text="Открыть результаты", command=self._open_result_path).pack(fill="x", pady=2)

    def _action_row(
        self,
        parent,
        title: str,
        description: str,
        action_id: str,
        confirm_var: tk.StringVar | None = None,
        condition: Callable[[], bool] | None = None,
    ) -> ttk.Button:
        button = add_action_row(parent, title, description, lambda: self._prepare_action(action_id, confirm_var))
        self.button_gates.append(ButtonGate(button, action_id, confirm_var, condition))
        return button

    def _sync_state(self) -> None:
        self.state.project_root = Path(self.project_root_var.get()).expanduser().resolve()
        self.state.report_date = self.report_date_var.get().strip()
        self.state.retrospective_years = int(self.years_var.get())
        self.state.period_type = self.period_type_var.get()
        self.state.aggregation_mode = self.aggregation_var.get()
        self.state.source_registry_mode = self.registry_mode_var.get()
        self.state.allow_legacy_raw = self.allow_legacy_var.get()
        self.state.minfin_year = int(self.minfin_year_var.get())
        self.state.final_year = int(self.final_year_var.get())
        self.state.minfin_mode = self.minfin_mode_var.get()
        self.state.minfin_url = self.minfin_url_var.get()
        self.state.max_pages = int(self.max_pages_var.get())
        self.state.no_network = self.no_network_var.get()
        self.state.html_file = self.html_file_var.get()
        self.state.manual_file = self.manual_file_var.get()
        self.state.stage_zero_mode = self.stage_zero_var.get()
        self.state.run_schema_before_pipeline = self.schema_before_var.get()
        self.state.open_outputs_after_run = self.open_outputs_var.get()
        self.state.validate()

    def _prepare_action(self, action_id: str, confirm_var: tk.StringVar | None = None) -> None:
        try:
            self._sync_state()
            plan = self.registry.build(action_id, self.state, validate_confirmation=False)
        except Exception as exc:
            self._show_error(exc)
            return
        self.selected_action_id = action_id
        self.selected_confirm_var = confirm_var
        self.selected_plan = plan
        self._set_preview(f"{plan.description}\n{format_plan(plan)}")
        self.execute_button.configure(state="normal" if not self.runner.is_running else "disabled")
        self.status_var.set(f"Подготовлено: {action_id}")

    def _execute_selected(self) -> None:
        if not self.selected_action_id:
            messagebox.showwarning("Действие", "Сначала подготовьте действие.", parent=self.root)
            return
        try:
            self._sync_state()
            confirm = self.selected_confirm_var.get() if self.selected_confirm_var is not None else ""
            plan = self.registry.build(self.selected_action_id, self.state, confirm=confirm)
            self.runner = CommandRunner(self.state.project_root, self.state.launcher_log_dir)
            self.execute_button.configure(state="disabled")
            self.status_var.set(f"Выполняется: {plan.action_id}")
            self.notebook.select(self.log_text.master.master)
            log_path = self.runner.start(plan, self._runner_output, self._runner_complete)
            self._refresh_button_states()
            self.last_log_path = log_path
            self.log_path_var.set(f"Log: {log_path}")
            self.last_command_var.set(f"Action: {plan.action_id}")
            self._append_log(f"\n=== {plan.action_id} ===\n")
        except Exception as exc:
            self.execute_button.configure(state="normal")
            self._show_error(exc)

    def _runner_output(self, text: str) -> None:
        self.root.after(0, self._append_log, text)

    def _runner_complete(self, result: RunResult) -> None:
        self.root.after(0, self._finish_run, result)

    def _finish_run(self, result: RunResult) -> None:
        self.last_exit_code = result.exit_code
        self.last_log_path = result.log_path
        self.exit_code_var.set(f"Exit code: {result.exit_code}")
        self.log_path_var.set(f"Log: {result.log_path}")
        self.last_command_var.set(f"Последняя команда: {result.last_command}")
        if result.stopped:
            self.status_var.set("Команда остановлена")
        elif result.exit_code == 0:
            self.status_var.set(f"Успешно: {result.action_id}")
            if result.action_id in {"pipeline", "pipeline-stage-zero"} and self.open_outputs_var.get():
                self._open_path(self.state.project_root / "outputs")
        else:
            self.status_var.set(f"Ошибка: {result.action_id}, exit code {result.exit_code}")
        self.execute_button.configure(state="normal" if self.selected_action_id else "disabled")
        self._refresh_button_states()

    def _append_log(self, text: str) -> None:
        self.log_text.insert("end", text)
        self.log_text.see("end")

    def _set_preview(self, text: str) -> None:
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", text)
        self.preview_text.configure(state="disabled")

    def _refresh_button_states(self) -> None:
        for gate in self.button_gates:
            definition = self.registry.definition(gate.action_id)
            enabled = True
            if definition.required_confirm:
                enabled = gate.confirm_var is not None and gate.confirm_var.get() == definition.required_confirm
            if gate.condition is not None:
                enabled = enabled and gate.condition()
            gate.button.configure(state="normal" if enabled and not self.runner.is_running else "disabled")

    def _manual_file_selected(self) -> bool:
        return bool(self.manual_file_var.get().strip())

    def _pipeline_stage_zero_ready(self) -> bool:
        mode = self.stage_zero_var.get()
        return mode != "download" or self.pipeline_confirm_var.get() == "DOWNLOAD_MINFIN_SOURCE"

    def _choose_project_root(self) -> None:
        selected = filedialog.askdirectory(initialdir=self.project_root_var.get(), parent=self.root)
        if selected:
            self.project_root_var.set(selected)

    def _choose_html(self) -> None:
        selected = filedialog.askopenfilename(filetypes=[("HTML", "*.html"), ("Все файлы", "*.*")], parent=self.root)
        if selected:
            self.html_file_var.set(selected)

    def _choose_manual(self) -> None:
        selected = filedialog.askopenfilename(filetypes=[("Excel XLSX", "*.xlsx")], parent=self.root)
        if selected:
            self.manual_file_var.set(selected)

    def _open_path(self, path: Path) -> None:
        try:
            actions.open_path(path)
            self.status_var.set(f"Открыто: {path}")
        except Exception as exc:
            self._show_error(exc)

    def _open_monthly_metrics(self) -> None:
        self._sync_state()
        self._open_path(self.state.project_root / "outputs/reports/monthly_tables" / f"monthly_metrics_{self.state.output_suffix}.xlsx")

    def _open_weighted_yield(self) -> None:
        self._sync_state()
        self._open_path(self.state.project_root / "outputs/charts/monthly/yield" / f"monthly_weighted_avg_yield_{self.state.output_suffix}.html")

    def _open_run_manifest(self) -> None:
        candidates = sorted((self.state.project_root / "outputs/reports").glob("run_manifest_*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
        if not candidates:
            latest = self.state.project_root / "data/processed/run_manifest_latest.json"
            self._open_path(latest)
            return
        self._open_path(candidates[0])

    def _open_result_path(self) -> None:
        if not self.selected_plan or not self.selected_plan.result_paths:
            messagebox.showinfo("Результаты", "Для action не задана отдельная папка результатов.", parent=self.root)
            return
        existing = next((path for path in self.selected_plan.result_paths if path.exists()), self.selected_plan.result_paths[0])
        self._open_path(existing)

    def _copy_preview(self) -> None:
        text = self.preview_text.get("1.0", "end").strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set("Command preview скопирован")

    def _copy_log(self) -> None:
        self.root.clipboard_clear()
        self.root.clipboard_append(self.log_text.get("1.0", "end").strip())
        self.status_var.set("Журнал скопирован")

    def _open_last_log(self) -> None:
        if self.last_log_path is None:
            messagebox.showinfo("Журнал", "Log-файл еще не создан.", parent=self.root)
            return
        self._open_path(self.last_log_path)

    def _stop_command(self) -> None:
        if self.runner.stop():
            self.status_var.set("Остановка команды запрошена")
        else:
            self.status_var.set("Активной команды нет")

    def _show_error(self, error: Exception) -> None:
        self.status_var.set("Ошибка")
        messagebox.showerror("OFZ Analytics", str(error), parent=self.root)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Desktop GUI launcher OFZ_ANALYTICS.")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--smoke", action="store_true", help="Проверить state/actions без открытия окна.")
    parser.add_argument("--smoke-ui", action="store_true", help="Создать widgets и закрыть тестовое окно.")
    return parser


def run_smoke(project_root: Path) -> int:
    state = GuiState(project_root=project_root.resolve())
    state.validate()
    action_registry = ActionRegistry()
    for action_id in ("check-environment", "minfin-monthly-offline", "pipeline-stage-zero", "quality-fast", "release-dry"):
        action_registry.build(action_id, state, validate_confirmation=False)
    if not HELP_TEXT.strip():
        raise RuntimeError("Встроенная справка пуста.")
    if len(TAB_TITLES) != 9:
        raise RuntimeError("Нарушен контракт вкладок GUI.")
    print(f"OFZ GUI smoke passed. Actions: {len(action_registry.action_ids())}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.smoke:
        return run_smoke(args.project_root)
    state = GuiState(project_root=args.project_root.resolve())
    state.validate()
    root = tk.Tk()
    OfzAnalyticsGui(root, state)
    if args.smoke_ui:
        root.withdraw()
        root.update_idletasks()
        root.destroy()
        print("OFZ GUI widget smoke passed")
        return 0
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
