"""Общие tkinter helpers для GUI launcher."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


def add_labeled_entry(
    parent,
    row: int,
    label: str,
    variable: tk.Variable,
    width: int = 24,
    column: int = 0,
) -> ttk.Entry:
    ttk.Label(parent, text=label).grid(row=row, column=column, sticky="w", padx=5, pady=4)
    entry = ttk.Entry(parent, textvariable=variable, width=width)
    entry.grid(row=row, column=column + 1, sticky="ew", padx=5, pady=4)
    return entry


def add_labeled_combo(
    parent,
    row: int,
    label: str,
    variable: tk.Variable,
    values: tuple[str, ...],
    width: int = 22,
    column: int = 0,
) -> ttk.Combobox:
    ttk.Label(parent, text=label).grid(row=row, column=column, sticky="w", padx=5, pady=4)
    combo = ttk.Combobox(parent, textvariable=variable, values=values, state="readonly", width=width)
    combo.grid(row=row, column=column + 1, sticky="ew", padx=5, pady=4)
    return combo


def add_intro(parent, text: str) -> ttk.Label:
    label = ttk.Label(parent, text=text, wraplength=1080, justify="left")
    label.pack(fill="x", padx=10, pady=(10, 6))
    return label


def add_action_row(parent, title: str, description: str, command) -> ttk.Button:
    row = ttk.Frame(parent)
    row.pack(fill="x", padx=10, pady=3)
    row.columnconfigure(1, weight=1)
    button = ttk.Button(row, text=title, command=command, width=31)
    button.grid(row=0, column=0, sticky="w", padx=(0, 10))
    ttk.Label(row, text=description, wraplength=760, justify="left").grid(row=0, column=1, sticky="w")
    return button


def make_scrolled_text(parent, **kwargs) -> tk.Text:
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=8, pady=8)
    text = tk.Text(frame, wrap="word", **kwargs)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
    text.configure(yscrollcommand=scrollbar.set)
    text.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return text
