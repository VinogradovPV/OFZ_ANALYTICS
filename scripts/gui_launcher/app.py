"""Полноценный desktop GUI launcher OFZ_ANALYTICS на tkinter."""

from __future__ import annotations

import argparse
import json
import sys
import tkinter as tk
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from typing import Callable

from . import actions
from .actions import ActionPlan, ActionRegistry
from .command_runner import CommandRunner, RunResult, format_plan
from .help_text import HELP_TEXT
from .state import GuiState
from .widgets import add_action_row, add_info_block, add_intro, add_labeled_combo, add_labeled_entry, make_scrolled_text


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

MINFIN_BASIC_CONTROL_LABELS = (
    "Текущий год",
    "Год финального закрытия",
    "Проверить сайт Минфина",
    "Обновить данные текущего года",
    "Проверить закрытие предыдущего года",
    "Закрыть предыдущий год",
    "Проверить registry",
    "Открыть registry",
    "Открыть отчеты source acquisition",
)

MINFIN_ADVANCED_CONTROL_LABELS = (
    "Manual XLSX",
    "URL override",
    "HTML fixture",
    "No network",
    "Max pages",
    "Replace changed final",
)

STAGE_ZERO_LABEL_TO_MODE = {
    "Не выполнять": "off",
    "Только dry-run": "dry-run",
    "Download с подтверждением": "download",
}
STAGE_ZERO_MODE_TO_LABEL = {value: key for key, value in STAGE_ZERO_LABEL_TO_MODE.items()}
PREVIEW_PLACEHOLDER = "Выберите действие на вкладке. Здесь появятся технические детали и команда запуска."
NO_RESULT_POPUP_TEXT = "Папка результатов еще не создана. Сначала выполните действие."

TAB_INFO = {
    "Обзор": (
        "Задает общие параметры проекта.",
        "Перед запуском pipeline, проверок качества и release bundle.",
        "Выберите папку проекта, дату отчета и параметры расчета, затем нажмите \"Проверить окружение\".",
        "Проверка окружения и Git-статуса ничего не меняет.",
    ),
    "Исходные данные Минфина": (
        "Получает и проверяет исходные XLSX-файлы Минфина.",
        "Перед pipeline, если нужно обновить текущий год или закрыть прошлый год.",
        "Сначала нажмите \"Проверить сайт Минфина\", затем при необходимости \"Обновить текущий год\".",
        "Dry-run ничего не меняет; download меняет controlled raw storage и требует подтверждения.",
    ),
    "Pipeline": (
        "Запускает основной расчетный pipeline.",
        "После проверки или обновления исходных данных Минфина.",
        "Выберите, нужно ли перед расчетом проверять или обновлять данные Минфина, затем нажмите \"Запустить pipeline\".",
        "Создает generated outputs в outputs/. Raw меняется только при download этапа 0.",
    ),
    "Проверки качества": (
        "Запускает проверки качества проекта.",
        "После изменений кода, данных, документации или перед release.",
        "Для обычной проверки выполните UTF-8/Mojibake, Schema validation и Quality fast.",
        "Проверки могут создавать отчеты в outputs/, но не меняют исходные данные.",
    ),
    "Отчеты и графики": (
        "Открывает сформированные отчеты, таблицы и графики.",
        "После успешного запуска pipeline.",
        "Нажмите нужную кнопку для открытия папки или ключевого артефакта.",
        "Ничего не меняет; открывает generated outputs, которые не коммитятся.",
    ),
    "Release и пакеты": (
        "Готовит release bundle и BI package.",
        "Перед публикацией результата или передачей артефактов.",
        "Сначала выполните dry-run, проверьте план, затем при необходимости выполните build.",
        "Build создает файлы в releases/. Эта папка не коммитится.",
    ),
    "Обслуживание": (
        "Диагностика, проверка staged artifacts и обслуживание generated outputs.",
        "Перед commit, после pipeline или при очистке локальных результатов.",
        "Безопасные проверки можно запускать сразу; удаление outputs требует подтверждения.",
        "Git status и artifact guard ничего не меняют; удаление outputs удаляет generated artifacts.",
    ),
    "Журнал": (
        "Показывает журнал выполнения команд GUI.",
        "Во время и после запуска действий.",
        "Выберите действие на любой вкладке; вывод появится здесь автоматически.",
        "Ничего не меняет; позволяет остановить выполняющуюся команду.",
    ),
    "Справка": (
        "Объясняет основной workflow проекта и правила безопасной работы.",
        "Когда нужно вспомнить порядок действий, смысл параметров или правила артефактов.",
        "Читайте разделы справки или вернитесь к нужной вкладке.",
        "Ничего не меняет.",
    ),
}


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
        self.open_results_button: ttk.Button | None = None

        self.root.title("OFZ Analytics")
        self.root.geometry("1280x860")
        self.root.minsize(1060, 720)
        self.status_var = tk.StringVar(value="Готово")
        self.last_command_var = tk.StringVar(value="Команда еще не выполнялась")
        self.exit_code_var = tk.StringVar(value="Exit code: -")
        self.log_path_var = tk.StringVar(value="Log: -")
        self.run_status_var = tk.StringVar(value="Статус выполнения: ожидание")
        self.user_summary_var = tk.StringVar(value="Итог операции: выберите действие и запустите его.")
        self.run_started_var = tk.StringVar(value="Время старта: -")
        self.run_finished_var = tk.StringVar(value="Время завершения: -")
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
        self.minfin_advanced_var = tk.BooleanVar(value=False)
        self.manual_import_var = tk.BooleanVar(value=False)
        self.stage_zero_var = tk.StringVar(value=STAGE_ZERO_MODE_TO_LABEL.get(self.state.stage_zero_mode, "Не выполнять"))
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
            self.minfin_advanced_var,
            self.manual_import_var,
        ):
            variable.trace_add("write", lambda *_args: self._refresh_button_states())
        self.minfin_status_var = tk.StringVar(value="Registry status: еще не проверялся")
        self.minfin_candidate_var = tk.StringVar(value="Последний selected candidate: -")
        self.minfin_dates_var = tk.StringVar(value="Публикация / изменение: -")
        self.minfin_file_var = tk.StringVar(value="XLSX: -")
        self.minfin_hash_var = tk.StringVar(value="SHA256: -")
        self.minfin_paths_var = tk.StringVar(value="latest/final/registry: -")

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
        add_info_block(tab, *TAB_INFO["Обзор"])
        form = ttk.LabelFrame(tab, text="Общие параметры")
        form.pack(fill="x", padx=10, pady=6)
        form.columnconfigure(1, weight=1)
        add_labeled_entry(form, 0, "Папка проекта", self.project_root_var, 72)
        ttk.Button(form, text="Выбрать папку", command=self._choose_project_root).grid(row=0, column=2, padx=5, pady=4)
        add_labeled_entry(form, 1, "Дата отчета", self.report_date_var)
        add_labeled_entry(form, 1, "Лет ретроспективы", self.years_var, 8, column=2)
        add_labeled_combo(form, 2, "Период", self.period_type_var, ("month", "quarter", "year"))
        add_labeled_combo(form, 2, "Режим агрегации", self.aggregation_var, ("cumulative", "point"), column=2)
        add_labeled_combo(form, 3, "Режим проверки registry", self.registry_mode_var, ("off", "warn", "strict"))
        ttk.Checkbutton(form, text="Разрешить legacy-данные", variable=self.allow_legacy_var).grid(row=3, column=2, columnspan=2, sticky="w", padx=5)
        status_frame = ttk.LabelFrame(tab, text="Статус окружения")
        status_frame.pack(fill="x", padx=10, pady=6)
        for text in (
            "Последняя проверка: смотрите вкладку Журнал после запуска.",
            "Последний Git-статус: доступен через кнопку ниже.",
            "Последний pipeline: смотрите exit code и log path во вкладке Журнал.",
            "Последний quality-fast: смотрите exit code и log path во вкладке Журнал.",
        ):
            ttk.Label(status_frame, text=text, wraplength=980, justify="left").pack(anchor="w", padx=8, pady=2)
        actions_frame = ttk.LabelFrame(tab, text="Стартовые действия")
        actions_frame.pack(fill="x", padx=10, pady=6)
        self._action_row(actions_frame, "Проверить окружение", "Проверяет Python и зависимости; ничего не меняет.", "check-environment")
        self._action_row(actions_frame, "Проверить Git-статус", "Показывает read-only Git status.", "git-status")
        ttk.Button(actions_frame, text="Открыть инструкцию проекта", command=lambda: self._open_path(self.state.project_root / "README.md")).pack(anchor="w", padx=10, pady=4)
        ttk.Button(actions_frame, text="Перейти к Pipeline", command=lambda: self._select_tab("Pipeline")).pack(anchor="w", padx=10, pady=4)

    def _build_minfin_tab(self) -> None:
        tab = self._new_tab("Исходные данные Минфина")
        add_info_block(tab, *TAB_INFO["Исходные данные Минфина"])

        status_frame = ttk.LabelFrame(tab, text="Статус источника")
        status_frame.pack(fill="x", padx=10, pady=6)
        status_frame.columnconfigure(1, weight=1)
        add_labeled_entry(status_frame, 0, "Текущий год", self.minfin_year_var, 10)
        add_labeled_entry(status_frame, 0, "Год финального закрытия", self.final_year_var, 10, column=2)
        for row, variable in enumerate(
            (
                self.minfin_status_var,
                self.minfin_candidate_var,
                self.minfin_dates_var,
                self.minfin_file_var,
                self.minfin_hash_var,
                self.minfin_paths_var,
            ),
            start=1,
        ):
            ttk.Label(status_frame, textvariable=variable, wraplength=1060, justify="left").grid(
                row=row, column=0, columnspan=4, sticky="w", padx=5, pady=2
            )
        ttk.Button(status_frame, text="Обновить статус", command=self._refresh_minfin_status).grid(
            row=7, column=0, sticky="w", padx=5, pady=5
        )
        self._refresh_minfin_status(show_errors=False)

        actions_frame = ttk.LabelFrame(tab, text="Основные действия")
        actions_frame.pack(fill="x", padx=10, pady=6)
        self._action_row(actions_frame, "Проверить сайт Минфина", "Dry-run: сайт проверяется, raw не изменяется.", "minfin-monthly-live")
        self._action_row(
            actions_frame,
            "Обновить текущий год",
            "Сначала показываются технические детали; запуск требует DOWNLOAD_MINFIN_SOURCE.",
            "minfin-monthly-download",
            self.minfin_confirm_var,
        )
        self._action_row(actions_frame, "Проверить закрытие предыдущего года", "Annual-final dry-run без изменения raw.", "minfin-annual-dry")
        self._action_row(
            actions_frame,
            "Закрыть предыдущий год",
            "Создать/подтвердить final-файл; запуск требует DOWNLOAD_MINFIN_SOURCE.",
            "minfin-annual-download",
            self.minfin_confirm_var,
        )
        self._action_row(actions_frame, "Проверить registry", "Проверить registry и связку data audit.", "data-audit-registry-smoke")

        toolbar = ttk.Frame(tab)
        toolbar.pack(fill="x", padx=10, pady=4)
        ttk.Button(toolbar, text="Открыть registry", command=lambda: self._open_path(self.state.project_root / "data/raw/minfin/ofz_auction_results/registry")).pack(side="left")
        ttk.Button(toolbar, text="Открыть отчеты source acquisition", command=lambda: self._open_path(self.state.project_root / "outputs/reports/source_acquisition")).pack(side="left", padx=6)

        manual_toggle = ttk.Checkbutton(
            tab,
            text="Показать аварийный ручной импорт",
            variable=self.manual_import_var,
            command=self._set_minfin_advanced_visibility,
        )
        manual_toggle.pack(anchor="w", padx=12, pady=(8, 0))
        self.manual_import_frame = ttk.LabelFrame(tab, text="Аварийный ручной импорт")
        self.manual_import_frame.columnconfigure(1, weight=1)
        add_labeled_entry(self.manual_import_frame, 0, "Manual XLSX", self.manual_file_var, 68)
        ttk.Button(self.manual_import_frame, text="Выбрать XLSX", command=self._choose_manual).grid(row=0, column=2, padx=5)
        manual_actions = ttk.Frame(self.manual_import_frame)
        manual_actions.grid(row=1, column=0, columnspan=3, sticky="ew", padx=0, pady=4)
        self._action_row(manual_actions, "Проверить выбранный XLSX", "Проверка файла без импорта.", "minfin-manual-dry", condition=self._manual_file_selected)
        self._action_row(
            manual_actions,
            "Импортировать XLSX",
            "Аварийный импорт требует IMPORT_MINFIN_FILE.",
            "minfin-manual-import",
            self.minfin_confirm_var,
            self._manual_file_selected,
        )

        advanced_toggle = ttk.Checkbutton(
            tab,
            text="Показать расширенную диагностику парсера",
            variable=self.minfin_advanced_var,
            command=self._set_minfin_advanced_visibility,
        )
        advanced_toggle.pack(anchor="w", padx=12, pady=(8, 0))
        self.minfin_advanced_frame = ttk.LabelFrame(tab, text="Диагностика парсера")
        self.minfin_advanced_frame.columnconfigure(1, weight=1)
        add_labeled_entry(self.minfin_advanced_frame, 0, "URL override", self.minfin_url_var, 68)
        add_labeled_entry(self.minfin_advanced_frame, 1, "HTML fixture", self.html_file_var, 68)
        ttk.Button(self.minfin_advanced_frame, text="Выбрать HTML", command=self._choose_html).grid(row=1, column=2, padx=5)
        add_labeled_entry(self.minfin_advanced_frame, 2, "Max pages", self.max_pages_var, 10)
        ttk.Checkbutton(self.minfin_advanced_frame, text="No network", variable=self.no_network_var).grid(row=2, column=2, sticky="w", padx=5)
        advanced_actions = ttk.Frame(self.minfin_advanced_frame)
        advanced_actions.grid(row=3, column=0, columnspan=3, sticky="ew", padx=0, pady=4)
        self._action_row(advanced_actions, "Parser dry-run с fixture", "Offline plan; можно использовать HTML fixture.", "minfin-monthly-offline")
        self._action_row(
            advanced_actions,
            "Replace changed final",
            "Аварийная замена final после ручной проверки; требует REPLACE_MINFIN_FINAL.",
            "minfin-final-replace",
            self.minfin_confirm_var,
        )
        self._set_minfin_advanced_visibility()

    def _build_pipeline_tab(self) -> None:
        tab = self._new_tab("Pipeline")
        add_info_block(tab, *TAB_INFO["Pipeline"])
        options = ttk.LabelFrame(tab, text="Pipeline workflow")
        options.pack(fill="x", padx=10, pady=6)
        ttk.Label(options, text="Перед запуском pipeline:").pack(anchor="w", padx=8, pady=(6, 2))
        stage_zero_descriptions = {
            "Не выполнять": "pipeline запустится на уже имеющихся данных.",
            "Только dry-run": "сайт Минфина будет проверен, но raw-данные не изменятся.",
            "Download с подтверждением": "GUI скачает актуальный файл после ввода DOWNLOAD_MINFIN_SOURCE.",
        }
        for text, description in stage_zero_descriptions.items():
            row = ttk.Frame(options)
            row.pack(fill="x", padx=18, pady=2)
            ttk.Radiobutton(row, text=text, variable=self.stage_zero_var, value=text).pack(side="left")
            ttk.Label(row, text=f"- {description}", wraplength=820, justify="left").pack(side="left", padx=8)
        ttk.Checkbutton(options, text="Запустить schema validation перед pipeline", variable=self.schema_before_var).pack(anchor="w", padx=8, pady=(8, 2))
        ttk.Checkbutton(options, text="Открыть outputs после успешного запуска", variable=self.open_outputs_var).pack(anchor="w", padx=8, pady=2)
        actions_frame = ttk.LabelFrame(tab, text="Запуск")
        actions_frame.pack(fill="x", padx=10, pady=6)
        self._action_row(
            actions_frame,
            "Запустить pipeline",
            "Учитывает выбранный этап 0. При ошибке stage 0/schema pipeline не запускается.",
            "pipeline-stage-zero",
            self.pipeline_confirm_var,
        )

    def _build_quality_tab(self) -> None:
        tab = self._new_tab("Проверки качества")
        add_info_block(tab, *TAB_INFO["Проверки качества"])
        order = ttk.LabelFrame(tab, text="Рекомендуемый порядок")
        order.pack(fill="x", padx=10, pady=6)
        ttk.Label(
            order,
            text="1. UTF-8 / Mojibake -> 2. Schema validation -> 3. Быстрая проверка качества -> "
            "4. Полная проверка перед release -> 5. Visual regression после изменений графиков.",
            wraplength=1080,
            justify="left",
        ).pack(anchor="w", padx=8, pady=6)
        groups = (
            (
                "Базовые проверки",
                (
                    ("UTF-8 / Mojibake", "Проверяет кодировки и mojibake.", "encoding-mojibake"),
                    ("Schema validation", "Проверяет схемы generated artifacts.", "schema"),
                    ("Быстрая проверка качества", "Обычный быстрый quality gate.", "quality-fast"),
                ),
            ),
            (
                "Расширенные проверки",
                (
                    ("Полная проверка качества", "Длительная pre-release проверка.", "quality-full"),
                    ("HTML chart QA", "Проверяет HTML contracts и подписи.", "html-chart-qa"),
                    ("Visual regression auto", "Screenshot при доступности, иначе fallback.", "visual-auto"),
                    ("Visual regression screenshot", "Требует работающий browser backend.", "visual-screenshot"),
                ),
            ),
            (
                "Проверки source acquisition",
                (
                    ("Source acquisition tests", "Offline parser, selection и failure modes.", "source-acquisition-tests"),
                    ("Registry smoke", "CSV/JSON registry roundtrip и hash.", "registry-smoke"),
                    ("Data audit registry smoke", "off/warn/strict и legacy fallback.", "data-audit-registry-smoke"),
                ),
            ),
        )
        for group_title, rows in groups:
            frame = ttk.LabelFrame(tab, text=group_title)
            frame.pack(fill="x", padx=10, pady=6)
            for title, description, action_id in rows:
                self._action_row(frame, title, description, action_id)

    def _build_reports_tab(self) -> None:
        tab = self._new_tab("Отчеты и графики")
        add_info_block(tab, *TAB_INFO["Отчеты и графики"])
        add_intro(
            tab,
            "После исправления методологии доходности проверьте, что доходность ОФЗ-ПД не смешивается с ОФЗ-ПК. "
            "В проблемном кейсе ноябрь 2025 не должен падать к 3.16%.",
        )
        groups = (
            (
                "Основные результаты",
                (
                    ("Открыть графики", lambda: self._open_path(self.state.project_root / "outputs/charts")),
                    ("Открыть exports", lambda: self._open_path(self.state.project_root / "outputs/exports")),
                    ("Открыть reports", lambda: self._open_path(self.state.project_root / "outputs/reports")),
                ),
            ),
            (
                "Ключевые ручные проверки",
                (
                    ("Monthly metrics XLSX", self._open_monthly_metrics),
                    ("Доходность ОФЗ-ПД", self._open_weighted_yield),
                    ("Yield min/median/max", self._open_weighted_yield),
                    ("Revenue charts", lambda: self._open_path(self.state.project_root / "outputs/charts/revenue")),
                ),
            ),
            (
                "Диагностика",
                (
                    ("Telemetry reports", lambda: self._open_path(self.state.project_root / "outputs/reports/telemetry")),
                    ("Run manifest", self._open_run_manifest),
                ),
            ),
        )
        for group_title, buttons in groups:
            frame = ttk.LabelFrame(tab, text=group_title)
            frame.pack(fill="x", padx=10, pady=6)
            for index, (title, command) in enumerate(buttons):
                ttk.Button(frame, text=title, command=command, width=30).grid(row=0, column=index, padx=8, pady=8, sticky="ew")
                frame.columnconfigure(index, weight=1)

    def _build_release_tab(self) -> None:
        tab = self._new_tab("Release и пакеты")
        add_info_block(tab, *TAB_INFO["Release и пакеты"])
        release_frame = ttk.LabelFrame(tab, text="Release bundle")
        release_frame.pack(fill="x", padx=10, pady=6)
        self._action_row(release_frame, "Проверить план release bundle", "Dry-run без записи в releases/.", "release-dry")
        self._action_row(release_frame, "Собрать release bundle", "Создает ignored releases/; требует BUILD_RELEASE_BUNDLE.", "release-build", self.release_confirm_var)
        bi_frame = ttk.LabelFrame(tab, text="BI package")
        bi_frame.pack(fill="x", padx=10, pady=6)
        self._action_row(bi_frame, "Проверить план BI package", "Dry-run без записи.", "bi-dry")
        self._action_row(bi_frame, "Собрать BI package", "Создает ignored releases/bi/; требует BUILD_BI_PACKAGE.", "bi-build", self.release_confirm_var)
        ttk.Button(tab, text="Открыть releases", command=lambda: self._open_path(self.state.project_root / "releases")).pack(anchor="w", padx=12, pady=8)

    def _build_maintenance_tab(self) -> None:
        tab = self._new_tab("Обслуживание")
        add_info_block(tab, *TAB_INFO["Обслуживание"])
        diagnostics = ttk.LabelFrame(tab, text="Безопасная диагностика")
        diagnostics.pack(fill="x", padx=10, pady=6)
        self._action_row(diagnostics, "Git status", "Read-only diagnostic.", "git-status")
        self._action_row(diagnostics, "Artifact guard", "Проверить staged generated paths.", "artifact-guard")
        folders = ttk.LabelFrame(tab, text="Открыть папки")
        folders.pack(fill="x", padx=10, pady=6)
        for title, relative in (
            ("Папка проекта", "."),
            ("data/raw", "data/raw"),
            ("outputs", "outputs"),
            ("logs", "logs"),
        ):
            ttk.Button(folders, text=f"Открыть {title}", command=lambda value=relative: self._open_path(self.state.project_root / value)).pack(side="left", padx=4)
        cleanup = ttk.LabelFrame(tab, text="Очистка")
        cleanup.pack(fill="x", padx=10, pady=6)
        self._action_row(cleanup, "Cleanup dry-run", "Показать план без удаления.", "cleanup-keep")
        self._action_row(cleanup, "Удалить outputs", "Удаляет generated artifacts; требует DELETE_OUTPUTS.", "cleanup-delete", self.maintenance_confirm_var)

    def _build_log_tab(self) -> None:
        tab = self._new_tab("Журнал")
        add_info_block(tab, *TAB_INFO["Журнал"])
        header = ttk.Frame(tab)
        header.pack(fill="x", padx=8, pady=6)
        ttk.Label(header, textvariable=self.run_status_var).pack(anchor="w")
        ttk.Label(header, textvariable=self.user_summary_var, wraplength=1080, justify="left").pack(anchor="w")
        ttk.Label(header, textvariable=self.run_started_var).pack(anchor="w")
        ttk.Label(header, textvariable=self.run_finished_var).pack(anchor="w")
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
        add_info_block(tab, *TAB_INFO["Справка"])
        text = make_scrolled_text(tab, height=30)
        text.insert("1.0", HELP_TEXT)
        text.configure(state="disabled")

    def _build_command_bar(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Технические детали выбранного действия")
        frame.pack(fill="x", padx=8, pady=4)
        self.preview_text = tk.Text(frame, height=5, wrap="word")
        self.preview_text.pack(side="left", fill="both", expand=True, padx=6, pady=5)
        self.preview_text.configure(state="disabled")
        buttons = ttk.Frame(frame)
        buttons.pack(side="right", padx=6)
        self.execute_button = ttk.Button(buttons, text="Повторить выбранное действие", command=self._execute_selected, state="disabled")
        self.execute_button.pack(fill="x", pady=2)
        ttk.Button(buttons, text="Копировать команду", command=self._copy_preview).pack(fill="x", pady=2)
        self.open_results_button = ttk.Button(buttons, text="Открыть результаты", command=self._open_result_path, state="disabled")
        self.open_results_button.pack(fill="x", pady=2)
        ttk.Button(buttons, text="Открыть log-файл", command=self._open_last_log).pack(fill="x", pady=2)
        ttk.Button(buttons, text="Открыть папку logs", command=lambda: self._open_path(self.state.launcher_log_dir)).pack(fill="x", pady=2)
        self._set_preview(PREVIEW_PLACEHOLDER)

    def _action_row(
        self,
        parent,
        title: str,
        description: str,
        action_id: str,
        confirm_var: tk.StringVar | None = None,
        condition: Callable[[], bool] | None = None,
    ) -> ttk.Button:
        button = add_action_row(parent, title, description, lambda: self._run_action_from_row(action_id, confirm_var))
        self.button_gates.append(ButtonGate(button, action_id, confirm_var, condition))
        return button

    def _run_action_from_row(self, action_id: str, confirm_var: tk.StringVar | None = None) -> None:
        self._prepare_action(action_id, confirm_var)
        if self.selected_action_id == action_id:
            self._execute_selected()

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
        self.state.stage_zero_mode = STAGE_ZERO_LABEL_TO_MODE.get(self.stage_zero_var.get(), self.stage_zero_var.get())
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
        self._set_preview(self._format_preview_details(plan))
        self.execute_button.configure(state="normal" if not self.runner.is_running else "disabled")
        self._refresh_result_button(plan)
        self.user_summary_var.set(f"Итог операции: действие подготовлено. {plan.description}")
        self.status_var.set(f"Подготовлено: {action_id}")

    def _execute_selected(self) -> None:
        if not self.selected_action_id:
            messagebox.showwarning("Действие", "Сначала подготовьте действие.", parent=self.root)
            return
        try:
            self._sync_state()
            preview_plan = self.registry.build(self.selected_action_id, self.state, validate_confirmation=False)
            confirm = self.selected_confirm_var.get() if self.selected_confirm_var is not None else ""
            if preview_plan.required_confirm and confirm != preview_plan.required_confirm:
                confirm = self._ask_confirm_token(preview_plan)
                if not confirm:
                    self.status_var.set("Операция отменена: token не введен")
                    return
                if self.selected_confirm_var is not None:
                    self.selected_confirm_var.set(confirm)
            plan = self.registry.build(self.selected_action_id, self.state, confirm=confirm)
            self.runner = CommandRunner(self.state.project_root, self.state.launcher_log_dir)
            self.execute_button.configure(state="disabled")
            self.status_var.set(f"Выполняется: {plan.action_id}")
            started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.run_status_var.set("Статус выполнения: выполняется")
            self.user_summary_var.set(f"Итог операции: выполняется {plan.description}")
            self.run_started_var.set(f"Время старта: {started}")
            self.run_finished_var.set("Время завершения: -")
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
        self.run_finished_var.set(f"Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.exit_code_var.set(f"Технический код завершения: {result.exit_code}")
        self.log_path_var.set(f"Log: {result.log_path}")
        self.last_command_var.set(f"Последняя команда: {result.last_command}")
        plan = self.selected_plan
        self.user_summary_var.set(self._build_user_summary(result, plan))
        if result.stopped:
            self.run_status_var.set("Статус выполнения: остановлено")
            self.status_var.set("Остановлено пользователем")
        elif result.exit_code == 0:
            self.run_status_var.set("Статус выполнения: успешно завершено")
            self.status_var.set("Успешно завершено")
            if result.action_id in {"pipeline", "pipeline-stage-zero"} and self.open_outputs_var.get():
                self._open_path(self.state.project_root / "outputs")
        else:
            self.run_status_var.set("Статус выполнения: завершено с ошибкой")
            self.status_var.set("Завершено с ошибкой")
        self.execute_button.configure(state="normal" if self.selected_action_id else "disabled")
        if plan is not None:
            self._refresh_result_button(plan)
        self._refresh_button_states()

    def _append_log(self, text: str) -> None:
        self.log_text.insert("end", text)
        self.log_text.see("end")

    def _set_preview(self, text: str) -> None:
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", text)
        self.preview_text.configure(state="disabled")

    def _format_preview_details(self, plan: ActionPlan) -> str:
        mutation = self._mutation_description(plan)
        confirm = plan.required_confirm or "не требуется"
        result_paths = ", ".join(str(path) for path in plan.result_paths) if plan.result_paths else "смотрите журнал выполнения"
        return (
            f"Что будет выполнено: {plan.description}\n"
            f"Команда:\n{format_plan(plan)}\n"
            f"Изменяет ли файлы: {mutation}\n"
            f"Confirm: {confirm}\n"
            f"Log: {self.state.launcher_log_dir}\\gui_run_<timestamp>.log\n"
            f"Ожидаемый результат: {result_paths}\n"
            "Основной запуск выполняется кнопкой на вкладке; нижняя кнопка повторяет выбранное действие."
        )

    def _mutation_description(self, plan: ActionPlan) -> str:
        mutating_actions = {
            "minfin-monthly-download": "да, controlled raw storage Минфина",
            "minfin-annual-download": "да, controlled raw storage Минфина",
            "minfin-final-replace": "да, annual-final в controlled raw storage",
            "minfin-manual-import": "да, controlled raw storage Минфина",
            "pipeline": "да, generated outputs в outputs/",
            "pipeline-stage-zero": "да, generated outputs; raw только если выбран download этапа 0",
            "release-build": "да, releases/",
            "bi-build": "да, releases/bi/",
            "cleanup-delete": "да, удаляет generated outputs",
        }
        return mutating_actions.get(plan.action_id, "нет, только проверка или открытие информации")

    def _refresh_result_button(self, plan: ActionPlan | None = None) -> None:
        if self.open_results_button is None:
            return
        active_plan = plan or self.selected_plan
        if active_plan is None or not active_plan.has_results:
            self.open_results_button.configure(state="disabled")
            return
        self.open_results_button.configure(state="normal" if not self.runner.is_running else "disabled")

    def _build_user_summary(self, result: RunResult, plan: ActionPlan | None) -> str:
        if plan is None:
            return "Итог операции: технический результат получен. Подробности доступны в журнале."
        if result.stopped:
            return "Остановлено пользователем. Подробности доступны в журнале."
        if result.saw_503:
            return "Сайт Минфина временно недоступен; raw не изменен. Повторите проверку позже или используйте ручной импорт."
        if result.exit_code != 0:
            return f"Завершено с ошибкой. {plan.user_failure_hint}"
        summary = self._success_summary_for_action(plan, result.output_tail)
        if result.saw_replacement_char:
            summary += "\nВ техническом журнале есть нечитаемые символы; проверьте UTF-8 настройки."
        return summary

    def _success_summary_for_action(self, plan: ActionPlan, output_tail: str) -> str:
        if plan.action_id == "git-status":
            dirty_hint = ""
            if any(line.startswith((" M ", "?? ", "A ", "D ")) for line in output_tail.splitlines()):
                dirty_hint = "\nЕсть локальные изменения. Проверьте список в журнале."
            return "Git-статус получен. Это read-only проверка." + dirty_hint
        if plan.action_id in {"minfin-monthly-live", "minfin-monthly-offline", "minfin-annual-dry", "minfin-manual-dry"}:
            return self._minfin_dry_run_summary(plan, output_tail)
        if plan.action_id in {"minfin-monthly-download", "minfin-annual-download", "minfin-final-replace", "minfin-manual-import"}:
            return self._minfin_download_summary(plan)
        if plan.action_id == "pipeline-stage-zero" and "Этап 0" in output_tail and "Exit code: 1" in output_tail:
            return "Этап 0 Минфина завершился ошибкой. Pipeline не запускался."
        return plan.user_success_message or "Успешно завершено. Подробности доступны в журнале."

    def _minfin_dry_run_summary(self, plan: ActionPlan, output_tail: str) -> str:
        candidate = self._extract_minfin_candidate_from_output(output_tail)
        raw_line = "Raw-данные не изменялись."
        if "Live network discovery is not implemented in P3.1 skeleton" in output_tail:
            return (
                "Live-поиск еще не реализован в текущей версии. "
                "Используйте HTML fixture/manual import или завершите реализацию source acquisition.\n"
                f"{raw_line}"
            )
        if candidate:
            lines = [
                "Проверка сайта Минфина завершена успешно.",
                f"Найден файл: {candidate.get('file_name', '-')}",
            ]
            published = candidate.get("published_at") or candidate.get("modified_at") or candidate.get("as_of_date")
            if published:
                lines.append(f"Дата публикации/изменения: {published}")
            lines.extend((raw_line, "Следующий шаг: при необходимости нажмите \"Обновить текущий год\"."))
            return "\n".join(lines)
        return (
            "Проверка завершена, но файл не найден.\n"
            f"{raw_line}\n"
            "Проверьте сайт Минфина или используйте ручной импорт."
        )

    def _minfin_download_summary(self, plan: ActionPlan) -> str:
        self._refresh_minfin_status(show_errors=False)
        registry_path = self.state.project_root / "data/raw/minfin/ofz_auction_results/registry"
        if plan.action_id == "minfin-monthly-download":
            return (
                "Обновление данных Минфина завершено успешно.\n"
                "Файл скачан и зарегистрирован.\n"
                f"Registry: {registry_path}\n"
                "Следующий шаг: запустите pipeline."
            )
        if plan.action_id == "minfin-manual-import":
            return f"Ручной импорт XLSX завершен успешно.\nRegistry: {registry_path}\nСледующий шаг: запустите pipeline."
        return f"{plan.user_success_message}\nRegistry: {registry_path}"

    def _extract_minfin_candidate_from_output(self, output_tail: str) -> dict:
        try:
            start = output_tail.find("{")
            end = output_tail.rfind("}")
            if start == -1 or end == -1 or end <= start:
                return {}
            payload = json.loads(output_tail[start : end + 1])
            candidate = payload.get("selected_candidate") or payload.get("selected_record") or {}
            if isinstance(candidate, dict):
                return candidate
        except Exception:
            return {}
        return {}

    def _refresh_button_states(self) -> None:
        for gate in self.button_gates:
            enabled = True
            if gate.condition is not None:
                enabled = enabled and gate.condition()
            gate.button.configure(state="normal" if enabled and not self.runner.is_running else "disabled")
        if hasattr(self, "manual_import_frame"):
            self._set_minfin_advanced_visibility()
        self._refresh_result_button()

    def _manual_file_selected(self) -> bool:
        return bool(self.manual_file_var.get().strip())

    def _pipeline_stage_zero_ready(self) -> bool:
        mode = STAGE_ZERO_LABEL_TO_MODE.get(self.stage_zero_var.get(), self.stage_zero_var.get())
        return mode != "download" or self.pipeline_confirm_var.get() == "DOWNLOAD_MINFIN_SOURCE"

    def _ask_confirm_token(self, plan: ActionPlan) -> str:
        messages = {
            "DOWNLOAD_MINFIN_SOURCE": (
                "Операция изменит controlled raw storage Минфина. "
                "Перед запуском убедитесь, что command preview выбран правильно."
            ),
            "REPLACE_MINFIN_FINAL": (
                "Операция заменяет annual-final файл после changed hash. "
                "Запускайте ее только после ручной проверки."
            ),
            "IMPORT_MINFIN_FILE": (
                "Операция импортирует локальный XLSX в controlled raw storage. "
                "Проверьте год, имя файла и источник."
            ),
            "BUILD_RELEASE_BUNDLE": "Операция создаст внешний release bundle в ignored releases/.",
            "BUILD_BI_PACKAGE": "Операция создаст внешний BI package в ignored releases/bi/.",
            "DELETE_OUTPUTS": "Операция удалит generated outputs после архивации/cleanup workflow.",
        }
        token = plan.required_confirm
        prompt = (
            f"{messages.get(token, 'Операция требует явного подтверждения.')}\n\n"
            f"Будет выполнено:\n{format_plan(plan)}\n\n"
            f"Для подтверждения введите:\n{token}"
        )
        answer = simpledialog.askstring("Подтверждение действия", prompt, parent=self.root)
        return answer.strip() if answer else ""

    def _set_minfin_advanced_visibility(self) -> None:
        if not hasattr(self, "manual_import_frame") or not hasattr(self, "minfin_advanced_frame"):
            return
        if self.manual_import_var.get():
            self.manual_import_frame.pack(fill="x", padx=10, pady=6)
        else:
            self.manual_import_frame.pack_forget()
        if self.minfin_advanced_var.get():
            self.minfin_advanced_frame.pack(fill="x", padx=10, pady=6)
        else:
            self.minfin_advanced_frame.pack_forget()

    def _refresh_minfin_status(self, show_errors: bool = True) -> None:
        try:
            self._sync_state()
            registry_root = self.state.project_root / "data/raw/minfin/ofz_auction_results"
            latest_json = registry_root / "registry/minfin_ofz_auction_sources_latest.json"
            latest_path = registry_root / "latest" / f"INTERNET_Auction_Results_rus_{self.state.minfin_year}_latest.xlsx"
            final_path = registry_root / "final" / f"INTERNET_Auction_Results_rus_{self.state.final_year}_final.xlsx"
            if not latest_json.exists():
                self.minfin_status_var.set("Registry status: latest JSON отсутствует")
                self.minfin_candidate_var.set("Последний selected candidate: -")
                self.minfin_dates_var.set("Публикация / изменение: -")
                self.minfin_file_var.set("XLSX: -")
                self.minfin_hash_var.set("SHA256: -")
            else:
                payload = json.loads(latest_json.read_text(encoding="utf-8"))
                records = payload.get("records", [])
                record = self._select_minfin_status_record(records)
                if record:
                    self.minfin_status_var.set(
                        f"Registry status: active {record.get('storage_role', '-')} для {record.get('year', '-')}"
                    )
                    self.minfin_candidate_var.set(f"Последний selected candidate: {record.get('document_title') or record.get('file_title') or '-'}")
                    self.minfin_dates_var.set(
                        f"Публикация / изменение: {record.get('published_at') or '-'} / {record.get('modified_at') or '-'}"
                    )
                    self.minfin_file_var.set(f"XLSX: {record.get('file_name') or '-'}")
                    sha256 = str(record.get("sha256") or "")
                    self.minfin_hash_var.set(f"SHA256: {sha256[:12] if sha256 else '-'}")
                else:
                    self.minfin_status_var.set("Registry status: active latest/final для выбранных лет не найден")
                    self.minfin_candidate_var.set("Последний selected candidate: -")
                    self.minfin_dates_var.set("Публикация / изменение: -")
                    self.minfin_file_var.set("XLSX: -")
                    self.minfin_hash_var.set("SHA256: -")
            self.minfin_paths_var.set(f"latest: {latest_path} | final: {final_path} | registry: {latest_json.parent}")
        except Exception as exc:
            self.minfin_status_var.set("Registry status: не удалось прочитать")
            if show_errors:
                self._show_error(exc)

    def _select_minfin_status_record(self, records: list[dict]) -> dict | None:
        preferred = (
            (self.state.minfin_year, "latest"),
            (self.state.final_year, "final"),
        )
        for year, role in preferred:
            for record in records:
                if record.get("year") == year and record.get("storage_role") == role and record.get("is_active_for_pipeline"):
                    return record
        return records[0] if records else None

    def _choose_project_root(self) -> None:
        selected = filedialog.askdirectory(initialdir=self.project_root_var.get(), parent=self.root)
        if selected:
            self.project_root_var.set(selected)

    def _select_tab(self, title: str) -> None:
        for index, tab_id in enumerate(self.notebook.tabs()):
            if self.notebook.tab(tab_id, "text") == title:
                self.notebook.select(index)
                return

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
        if not self.selected_plan or not self.selected_plan.has_results:
            return
        existing = next((path for path in self.selected_plan.result_paths if path.exists()), self.selected_plan.result_paths[0])
        if not existing.exists():
            messagebox.showinfo("Результаты", NO_RESULT_POPUP_TEXT, parent=self.root)
            return
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
