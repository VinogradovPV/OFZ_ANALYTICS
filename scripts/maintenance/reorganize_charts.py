"""Безопасная реорганизация HTML-графиков в outputs/charts/.

Скрипт по умолчанию работает в режиме dry-run: строит план переноса,
формирует отчет и индекс графиков, но не перемещает HTML-файлы. Фактический
перенос выполняется только при явном параметре --apply.
"""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts"
REPORT_PATH = PROJECT_ROOT / "docs" / "06_quality" / "charts_reorganization_report.md"
INDEX_PATH = CHARTS_DIR / "index.md"


CATEGORY_DIRS: dict[str, Path] = {
    "monthly_placement": CHARTS_DIR / "monthly" / "placement",
    "monthly_demand_supply": CHARTS_DIR / "monthly" / "demand_supply",
    "monthly_bid_cover": CHARTS_DIR / "monthly" / "bid_cover",
    "monthly_yield": CHARTS_DIR / "monthly" / "yield",
    "monthly_structure": CHARTS_DIR / "monthly" / "structure",
    "monthly_heatmap": CHARTS_DIR / "monthly" / "heatmap",
    "risk_target_period": CHARTS_DIR / "risk" / "target_period",
    "risk_retrospective": CHARTS_DIR / "risk" / "retrospective",
    "risk_outliers": CHARTS_DIR / "risk" / "outliers",
    "risk_logx": CHARTS_DIR / "risk" / "logx",
    "risk_facet": CHARTS_DIR / "risk" / "facet",
    "scatter_discount_demand": CHARTS_DIR / "scatter" / "discount_demand",
    "scatter_discount_revenue_gap": CHARTS_DIR / "scatter" / "discount_revenue_gap",
    "scatter_demand_cutoff": CHARTS_DIR / "scatter" / "demand_cutoff",
    "scatter_format_terms": CHARTS_DIR / "scatter" / "format_terms",
    "scatter_yield_demand": CHARTS_DIR / "scatter" / "yield_demand",
    "scatter_yield_discount": CHARTS_DIR / "scatter" / "yield_discount",
    "yield_boxplot": CHARTS_DIR / "yield" / "boxplot",
    "yield_ofz_pd": CHARTS_DIR / "yield" / "ofz_pd",
    "yield_other": CHARTS_DIR / "yield",
    "sankey_structure": CHARTS_DIR / "sankey" / "structure",
    "sankey_target_period": CHARTS_DIR / "sankey" / "target_period",
    "sankey_period": CHARTS_DIR / "sankey" / "period",
    "structure_maturity": CHARTS_DIR / "structure" / "maturity",
    "structure_format": CHARTS_DIR / "structure" / "format",
    "structure_placement_volume": CHARTS_DIR / "structure" / "placement_volume",
    "revenue_period": CHARTS_DIR / "revenue" / "period",
    "revenue_monthly": CHARTS_DIR / "revenue" / "monthly",
    "revenue_gap": CHARTS_DIR / "revenue" / "gap",
    "revenue_ratio": CHARTS_DIR / "revenue" / "ratio",
    "revenue_breakdowns": CHARTS_DIR / "revenue" / "breakdowns",
    "archive_review_required": CHARTS_DIR / "archive" / "review_required",
}


DISPLAY_CATEGORY: dict[str, str] = {
    "monthly_placement": "monthly/placement",
    "monthly_demand_supply": "monthly/demand_supply",
    "monthly_bid_cover": "monthly/bid_cover",
    "monthly_yield": "monthly/yield",
    "monthly_structure": "monthly/structure",
    "monthly_heatmap": "monthly/heatmap",
    "risk_target_period": "risk/target_period",
    "risk_retrospective": "risk/retrospective",
    "risk_outliers": "risk/outliers",
    "risk_logx": "risk/logx",
    "risk_facet": "risk/facet",
    "scatter_discount_demand": "scatter/discount_demand",
    "scatter_discount_revenue_gap": "scatter/discount_revenue_gap",
    "scatter_demand_cutoff": "scatter/demand_cutoff",
    "scatter_format_terms": "scatter/format_terms",
    "scatter_yield_demand": "scatter/yield_demand",
    "scatter_yield_discount": "scatter/yield_discount",
    "yield_boxplot": "yield/boxplot",
    "yield_ofz_pd": "yield/ofz_pd",
    "yield_other": "yield",
    "sankey_structure": "sankey/structure",
    "sankey_target_period": "sankey/target_period",
    "sankey_period": "sankey/period",
    "structure_maturity": "structure/maturity",
    "structure_format": "structure/format",
    "structure_placement_volume": "structure/placement_volume",
    "revenue_period": "revenue/period",
    "revenue_monthly": "revenue/monthly",
    "revenue_gap": "revenue/gap",
    "revenue_ratio": "revenue/ratio",
    "revenue_breakdowns": "revenue/breakdowns",
    "archive_review_required": "review_required",
}


@dataclass(frozen=True)
class ChartPlan:
    """Одна строка плана реорганизации HTML-графика."""

    source: Path
    target: Path
    category: str
    action: str
    status: str
    note: str


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    apply_changes = bool(args.apply)

    ensure_directories()
    plans = build_plan()
    if apply_changes:
        plans = apply_plan(plans)
    write_report(plans, apply_changes)
    write_index(plans, apply_changes)

    print(REPORT_PATH.relative_to(PROJECT_ROOT).as_posix())
    print(INDEX_PATH.relative_to(PROJECT_ROOT).as_posix())
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Разобрать режим запуска."""
    parser = argparse.ArgumentParser(description="Безопасная реорганизация HTML-графиков outputs/charts/.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Сформировать план без переноса файлов.")
    mode.add_argument("--apply", action="store_true", help="Выполнить перенос файлов.")
    args = parser.parse_args(argv)
    if not args.apply:
        args.dry_run = True
    return args


def ensure_directories() -> None:
    """Создать целевые папки и папку отчета."""
    for directory in set(CATEGORY_DIRS.values()):
        directory.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)


def build_plan() -> list[ChartPlan]:
    """Сформировать план переноса HTML из корня outputs/charts/."""
    plans: list[ChartPlan] = []
    for source in sorted(CHARTS_DIR.glob("*.html")):
        category_key = classify_chart(source.name)
        target_dir = CATEGORY_DIRS[category_key]
        target = safe_target_path(target_dir / source.name)
        plans.append(
            ChartPlan(
                source=source,
                target=target,
                category=DISPLAY_CATEGORY[category_key],
                action="move",
                status="planned",
                note=category_note(category_key),
            )
        )
    return plans


def classify_chart(filename: str) -> str:
    """Определить целевую категорию HTML-графика по имени файла."""
    name = filename.lower()
    if name.startswith("monthly_placement_volume") or name.startswith("monthly_cumulative_placement"):
        return "monthly_placement"
    if name.startswith("monthly_demand_supply"):
        return "monthly_demand_supply"
    if name.startswith("monthly_bid_cover") or name.startswith("monthly_bid_to_cover"):
        return "monthly_bid_cover"
    if name.startswith("monthly_weighted_avg_yield"):
        return "monthly_yield"
    if name.startswith("monthly_placement_by_format") or name.startswith("monthly_placement_by_maturity"):
        return "monthly_structure"
    if name.startswith("monthly_heatmap"):
        return "monthly_heatmap"
    if name.startswith("risk_quadrant_retrospective_outliers"):
        return "risk_outliers"
    if name.startswith("risk_quadrant_retrospective_logx"):
        return "risk_logx"
    if name.startswith("risk_quadrant_retrospective_facet"):
        return "risk_facet"
    if name.startswith("risk_quadrant_retrospective"):
        return "risk_retrospective"
    if name.startswith("risk_quadrant"):
        return "risk_target_period"
    if name.startswith("bid_to_cover"):
        return "risk_target_period"
    if name.startswith("demand_supply"):
        return "risk_target_period"

    if name.startswith("discount_vs_revenue_gap"):
        return "scatter_discount_revenue_gap"
    if name.startswith("discount_vs_demand"):
        return "scatter_discount_demand"
    if name.startswith("demand_cutoff_explanation"):
        return "scatter_demand_cutoff"
    if name.startswith("format_terms_scatter") or name.startswith("format_terms_aggregate_scatter"):
        return "scatter_format_terms"
    if name.startswith("yield_vs_demand"):
        return "scatter_yield_demand"
    if name.startswith("yield_vs_discount"):
        return "scatter_yield_discount"

    if name.startswith("yield_boxplot_ofz_pd"):
        return "yield_ofz_pd"
    if name.startswith("yield_boxplot"):
        return "yield_boxplot"
    if name.startswith("yield_"):
        return "yield_other"

    if name.startswith("sankey_target_period"):
        return "sankey_target_period"
    if name.startswith("sankey_period"):
        return "sankey_period"
    if name.startswith("sankey"):
        return "sankey_structure"

    if name.startswith("maturity_structure"):
        return "structure_maturity"
    if name.startswith("format_structure") or name.startswith("format_discount") or name.startswith("format_terms_comparison") or name.startswith("format_terms_delta_by_format"):
        return "structure_format"
    if name.startswith("placement_volume"):
        return "structure_placement_volume"

    if name.startswith("format_nominal_revenue_gap"):
        return "revenue_gap"
    if name.startswith("revenue_vs_nominal") or name.startswith("nominal_revenue_gap_by_period"):
        if name.startswith("revenue_vs_nominal_by_period"):
            return "revenue_period"
        return "revenue_gap"
    if name.startswith("monthly_revenue_vs_nominal") or name.startswith("monthly_nominal_revenue_gap"):
        return "revenue_monthly"
    if name.startswith("revenue_to_nominal_ratio"):
        return "revenue_ratio"
    if name.startswith("revenue_gap_by_"):
        return "revenue_breakdowns"

    return "archive_review_required"


def apply_plan(plans: list[ChartPlan]) -> list[ChartPlan]:
    """Выполнить переносы без удаления и молчаливой перезаписи."""
    applied: list[ChartPlan] = []
    for plan in plans:
        if not plan.source.exists():
            applied.append(
                ChartPlan(
                    source=plan.source,
                    target=plan.target,
                    category=plan.category,
                    action=plan.action,
                    status="missing_source",
                    note="Исходный файл отсутствует; перенос пропущен.",
                )
            )
            continue
        target = safe_target_path(plan.target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(plan.source), str(target))
        applied.append(
            ChartPlan(
                source=plan.source,
                target=target,
                category=plan.category,
                action=plan.action,
                status="moved",
                note=plan.note,
            )
        )
    return applied


def safe_target_path(target: Path) -> Path:
    """Вернуть безопасный целевой путь, добавляя суффикс при конфликте."""
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate = target.with_name(f"{stem}__moved_{timestamp}{suffix}")
    counter = 1
    while candidate.exists():
        candidate = target.with_name(f"{stem}__moved_{timestamp}_{counter}{suffix}")
        counter += 1
    return candidate


def category_note(category_key: str) -> str:
    """Пояснить решение классификации."""
    if category_key == "archive_review_required":
        return "Имя графика не попало в явные правила; требуется ручная проверка."
    if category_key == "scatter_yield_discount":
        return "Графики yield_vs_discount_* маршрутизируются в `scatter/yield_discount`."
    if category_key == "scatter_format_terms":
        return "Графики format_terms_scatter_* и format_terms_aggregate_scatter_* маршрутизируются в `scatter/format_terms`."
    if category_key == "structure_format":
        return "Графики format_structure_*, format_discount_* и format_terms_comparison_* маршрутизируются в `structure/format`."
    if category_key == "revenue_gap":
        return "Графики разницы номинал-выручка, включая format_nominal_revenue_gap_*, маршрутизируются в `revenue/gap`."
    return f"График отнесен к категории `{DISPLAY_CATEGORY[category_key]}`."


def write_report(plans: list[ChartPlan], apply_changes: bool) -> None:
    """Записать отчет о dry-run/apply."""
    mode = "apply" if apply_changes else "dry-run"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Отчет о реорганизации outputs/charts",
        "",
        f"Дата формирования: `{now}`.",
        f"Режим: `{mode}`.",
        "",
        "Файлы не удаляются. При конфликте имени используется безопасный суффикс.",
        "",
        "| Исходный путь | Новый путь | Категория | Действие | Статус | Примечание |",
        "|---|---|---|---|---|---|",
    ]
    for plan in plans:
        lines.append(
            "| "
            f"`{relative(plan.source)}` | "
            f"`{relative(plan.target)}` | "
            f"{plan.category} | "
            f"{plan.action} | "
            f"{plan.status} | "
            f"{escape_table(plan.note)} |"
        )
    lines.extend(
        [
            "",
            "## Сводка",
            "",
            f"- Всего HTML-файлов в плане: `{len(plans)}`.",
            f"- Запланировано переносов: `{sum(1 for plan in plans if plan.action == 'move')}`.",
            f"- Требуют ручной проверки: `{sum(1 for plan in plans if plan.category == 'review_required')}`.",
            f"- Фактически перемещено: `{sum(1 for plan in plans if plan.status == 'moved')}`.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_index(plans: list[ChartPlan], apply_changes: bool) -> None:
    """Сформировать индекс HTML-графиков по тематическим папкам."""
    mode = "apply" if apply_changes else "dry-run"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Индекс HTML-графиков",
        "",
        f"Дата формирования: `{now}`.",
        f"Режим последней реорганизации: `{mode}`.",
        "",
    ]
    grouped: dict[str, list[ChartPlan]] = {}
    for plan in plans:
        grouped.setdefault(plan.category, []).append(plan)
    for category in sorted(grouped):
        lines.extend([f"## {category}", ""])
        for plan in sorted(grouped[category], key=lambda item: item.target.name):
            link_target = plan.target if apply_changes and plan.status == "moved" else plan.source
            lines.append(f"- [{link_target.name}]({relative_to_charts(link_target)})")
        lines.append("")
    INDEX_PATH.write_text("\n".join(lines), encoding="utf-8")


def relative(path: Path) -> str:
    """Вернуть путь относительно корня проекта."""
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def relative_to_charts(path: Path) -> str:
    """Вернуть ссылку относительно outputs/charts/index.md."""
    try:
        return path.relative_to(CHARTS_DIR).as_posix()
    except ValueError:
        return path.as_posix()


def escape_table(value: str) -> str:
    """Экранировать markdown-таблицу."""
    return value.replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
