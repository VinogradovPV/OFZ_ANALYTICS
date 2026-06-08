"""Run manifest второй модернизации для воспроизводимого pipeline ОФЗ.

Manifest фиксирует параметры запуска, контрольные суммы scripts и raw files,
созданные outputs, статусы проверок и ограничения. `data/raw/` только читается.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import config, report_params, utils
else:
    from . import config, report_params, utils


RUN_MANIFEST_REPORT_DOC = config.get_doc_path("run_manifest_report.md")
RUN_MANIFEST_LATEST_JSON = config.PROCESSED_DATA_DIR / "run_manifest_latest.json"

KEY_SCRIPT_NAMES = (
    "run_pipeline.py",
    "report_params.py",
    "period_filter.py",
    "01_data_audit.py",
    "02_data_cleaning.py",
    "03_feature_engineering.py",
    "04_kpi_map.py",
    "05_visualization_strategy.py",
    "06_build_charts.py",
    "07_dashboard_exports.py",
    "08_analytical_tables.py",
    "09_monthly_analytics.py",
    "10_build_monthly_charts.py",
    "generate_executive_summary.py",
    "html_chart_qa.py",
    "schema_validation.py",
    "regression_tests.py",
    "smoke_tests.py",
    "run_manifest.py",
    "raw_data_registry.py",
    "palette.py",
    "scatter_chart_policy.py",
)


@dataclass(frozen=True)
class ManifestPaths:
    """Пути файлов manifest."""

    json_path: Path
    markdown_path: Path
    latest_json_path: Path
    docs_report_path: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Сформировать run manifest из CLI-параметров."""
    logger = utils.setup_logging(config.PIPELINE_LOG_PATH)
    args = parse_args(argv)
    params = build_params(args)
    stages = parse_stages(args.stages)
    check_statuses = parse_check_statuses(args.check_status)
    warnings = list(args.warning or [])
    limitations = list(args.limitation or [])

    paths = write_manifest(
        params=params,
        stages=stages,
        check_statuses=check_statuses,
        warnings=warnings,
        limitations=limitations,
    )
    logger.info("Run manifest сформирован: %s", paths.json_path)
    print(paths.json_path.relative_to(config.PROJECT_ROOT).as_posix())
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Разобрать параметры manifest."""
    parser = argparse.ArgumentParser(description="Сформировать run manifest второй модернизации.")
    parser.add_argument("--report-date", required=True, help="Отчетная дата YYYY-MM-DD.")
    parser.add_argument("--retrospective-years", required=True, type=int, help="Количество лет ретроспективы.")
    parser.add_argument("--period-type", required=True, choices=sorted(report_params.ALLOWED_PERIOD_TYPES), help="Тип периода.")
    parser.add_argument(
        "--aggregation-mode",
        default="cumulative",
        choices=sorted(report_params.ALLOWED_AGGREGATION_MODES),
        help="Режим агрегации периода.",
    )
    parser.add_argument(
        "--stages",
        nargs="*",
        default=[],
        help="Список этапов, включенных в запуск. Можно передавать значения через пробел или запятые.",
    )
    parser.add_argument(
        "--check-status",
        action="append",
        default=[],
        help="Статус проверки в формате name=status. Можно передавать несколько раз.",
    )
    parser.add_argument("--warning", action="append", default=[], help="Предупреждение для manifest.")
    parser.add_argument("--limitation", action="append", default=[], help="Ограничение для manifest.")
    return parser.parse_args(argv)


def build_params(args: argparse.Namespace) -> report_params.ReportParams:
    """Построить проверенные параметры отчета."""
    report_date = date.fromisoformat(args.report_date)
    period_type = report_params.normalize_period_type(args.period_type)
    aggregation_mode = report_params.normalize_aggregation_mode(args.aggregation_mode)
    report_params.validate_period_constraints(report_date, period_type, aggregation_mode)
    report_params.validate_retrospective_years(args.retrospective_years)
    periods = report_params.build_report_periods(
        report_date=report_date,
        retrospective_years=args.retrospective_years,
        period_type=period_type,
        aggregation_mode=aggregation_mode,
    )
    return report_params.ReportParams(
        report_date=report_date,
        retrospective_years=args.retrospective_years,
        period_type=period_type,
        aggregation_mode=aggregation_mode,
        periods=periods,
    )


def write_manifest(
    params: report_params.ReportParams,
    stages: Sequence[str],
    check_statuses: dict[str, str] | None = None,
    warnings: Sequence[str] | None = None,
    limitations: Sequence[str] | None = None,
) -> ManifestPaths:
    """Собрать и записать run manifest."""
    config.ensure_output_directories()
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    run_id = build_run_id(params, timestamp)
    paths = manifest_paths(run_id)

    manifest = build_manifest_data(
        run_id=run_id,
        timestamp=timestamp,
        params=params,
        stages=list(stages),
        check_statuses=check_statuses or {},
        warnings=list(warnings or []),
        limitations=list(limitations or []),
        manifest_paths=paths,
    )

    write_manifest_files(manifest, paths)

    # Повторно собрать outputs, чтобы manifest включал собственные файлы.
    manifest["outputs"] = collect_outputs()
    manifest["docs"] = collect_docs()
    manifest["outputs_summary"] = summarize_outputs(manifest["outputs"])
    write_manifest_files(manifest, paths)
    return paths


def build_manifest_data(
    run_id: str,
    timestamp: str,
    params: report_params.ReportParams,
    stages: list[str],
    check_statuses: dict[str, str],
    warnings: list[str],
    limitations: list[str],
    manifest_paths: ManifestPaths,
) -> dict[str, Any]:
    """Собрать JSON-совместимые данные manifest."""
    artifact_statuses = build_artifact_statuses(params)
    merged_statuses = {**artifact_statuses, **check_statuses}
    script_hashes, script_warnings = collect_script_hashes()
    raw_hashes, raw_warnings = collect_raw_hashes()
    all_warnings = [*warnings, *script_warnings, *raw_warnings]

    return {
        "schema_version": "run_manifest_v2",
        "modernization": "вторая модернизация",
        "run_id": run_id,
        "timestamp": timestamp,
        "report_date": params.report_date.isoformat(),
        "period_type": params.period_type,
        "aggregation_mode": params.aggregation_mode,
        "retrospective_years": params.retrospective_years,
        "stages": stages,
        "periods": serialize_periods(params.periods),
        "script_sha256": script_hashes,
        "raw_files_sha256": raw_hashes,
        "outputs": collect_outputs(),
        "key_chart_outputs": collect_key_chart_outputs(params),
        "docs": collect_docs(),
        "outputs_summary": {},
        "check_statuses": merged_statuses,
        "warnings": all_warnings,
        "limitations": limitations,
        "manifest_files": {
            "json": relative_path(manifest_paths.json_path),
            "markdown": relative_path(manifest_paths.markdown_path),
            "latest_json": relative_path(manifest_paths.latest_json_path),
            "docs_report": relative_path(manifest_paths.docs_report_path),
        },
    }


def build_run_id(params: report_params.ReportParams, timestamp: str) -> str:
    """Сформировать устойчивый run_id из времени и параметров."""
    seed = "|".join(
        [
            timestamp,
            params.report_date.isoformat(),
            params.period_type,
            params.aggregation_mode,
            str(params.retrospective_years),
        ]
    )
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8]
    safe_timestamp = timestamp.replace("-", "").replace(":", "").replace("T", "_")
    return f"{safe_timestamp}_{digest}"


def manifest_paths(run_id: str) -> ManifestPaths:
    """Вернуть целевые пути manifest."""
    return ManifestPaths(
        json_path=config.REPORTS_DIR / f"run_manifest_{run_id}.json",
        markdown_path=config.REPORTS_DIR / f"run_manifest_{run_id}.md",
        latest_json_path=RUN_MANIFEST_LATEST_JSON,
        docs_report_path=RUN_MANIFEST_REPORT_DOC,
    )


def write_manifest_files(manifest: dict[str, Any], paths: ManifestPaths) -> None:
    """Записать JSON, latest JSON и Markdown-представления manifest."""
    for path in (paths.json_path, paths.latest_json_path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    markdown = render_manifest_markdown(manifest)
    utils.write_markdown(paths.markdown_path, markdown)
    utils.write_markdown(paths.docs_report_path, markdown)


def collect_script_hashes() -> tuple[list[dict[str, Any]], list[str]]:
    """Посчитать sha256 ключевых scripts."""
    records: list[dict[str, Any]] = []
    warnings: list[str] = []
    for name in KEY_SCRIPT_NAMES:
        path = config.PROJECT_ROOT / "scripts" / name
        if not path.exists():
            warnings.append(f"Ключевой script отсутствует: scripts/{name}.")
            records.append({"path": f"scripts/{name}", "exists": False, "sha256": None, "size_bytes": None})
            continue
        records.append(file_record(path, with_sha=True))
    return records, warnings


def collect_raw_hashes() -> tuple[list[dict[str, Any]], list[str]]:
    """Посчитать sha256 raw-файлов без изменения data/raw/."""
    warnings: list[str] = []
    if not config.RAW_DATA_DIR.exists():
        return [], [f"Каталог raw files не найден: {relative_path(config.RAW_DATA_DIR)}."]
    raw_files = sorted(
        path for path in config.RAW_DATA_DIR.iterdir() if path.is_file() and path.suffix.lower() in {".xlsx", ".xls", ".csv"}
    )
    if not raw_files:
        warnings.append("В data/raw/ не найдены .xlsx, .xls или .csv файлы.")
    return [file_record(path, with_sha=True) for path in raw_files], warnings


def collect_outputs() -> list[dict[str, Any]]:
    """Собрать список outputs и размеры файлов."""
    if not config.OUTPUTS_DIR.exists():
        return []
    records: list[dict[str, Any]] = []
    for path in sorted(config.OUTPUTS_DIR.rglob("*")):
        if path.is_file():
            records.append(file_record(path, with_sha=False))
    return records


def collect_docs() -> list[dict[str, Any]]:
    """Собрать markdown-документы из новой структуры docs/."""
    if not config.DOCS_DIR.exists():
        return []
    records: list[dict[str, Any]] = []
    for path in sorted(config.DOCS_DIR.rglob("*.md")):
        if path.is_file():
            records.append(file_record(path, with_sha=False))
    return records


def collect_key_chart_outputs(params: report_params.ReportParams) -> list[dict[str, Any]]:
    """Собрать контрольный список новых графиков и CSV-основ второй модернизации."""
    suffix = output_suffix(params)
    specs = [
        ("monthly_placement_volume_html", config.CHARTS_MONTHLY_PLACEMENT_DIR / f"monthly_placement_volume_{suffix}.html"),
        ("monthly_placement_volume_csv", config.EXPORTS_CHART_DATA_DIR / f"monthly_placement_volume_{suffix}.csv"),
        ("monthly_cumulative_placement_html", config.CHARTS_MONTHLY_PLACEMENT_DIR / f"monthly_cumulative_placement_{suffix}.html"),
        ("monthly_cumulative_placement_csv", config.EXPORTS_CHART_DATA_DIR / f"monthly_cumulative_placement_{suffix}.csv"),
        ("monthly_demand_supply_html", config.CHARTS_MONTHLY_DEMAND_SUPPLY_DIR / f"monthly_demand_supply_{suffix}.html"),
        ("monthly_demand_supply_csv", config.EXPORTS_CHART_DATA_DIR / f"monthly_demand_supply_{suffix}.csv"),
        ("monthly_placement_by_format_html", config.CHARTS_MONTHLY_STRUCTURE_DIR / f"monthly_placement_by_format_{suffix}.html"),
        ("monthly_placement_by_format_csv", config.EXPORTS_CHART_DATA_DIR / f"monthly_placement_by_format_{suffix}.csv"),
        ("monthly_placement_by_maturity_html", config.CHARTS_MONTHLY_STRUCTURE_DIR / f"monthly_placement_by_maturity_{suffix}.html"),
        ("monthly_placement_by_maturity_csv", config.EXPORTS_CHART_DATA_DIR / f"monthly_placement_by_maturity_{suffix}.csv"),
        ("demand_cutoff_explanation_html", config.CHARTS_SCATTER_DEMAND_CUTOFF_DIR / f"demand_cutoff_explanation_{suffix}.html"),
        ("demand_cutoff_explanation_csv", config.EXPORTS_CHART_DATA_RISK_QUADRANT_DIR / f"demand_cutoff_explanation_{suffix}.csv"),
        ("yield_vs_discount_html", config.CHARTS_SCATTER_YIELD_DISCOUNT_DIR / f"yield_vs_discount_{suffix}.html"),
        ("yield_vs_discount_csv", config.EXPORTS_CHART_DATA_SCATTER_DIR / f"yield_vs_discount_{suffix}.csv"),
        ("yield_vs_discount_facet_html", config.CHARTS_SCATTER_YIELD_DISCOUNT_DIR / f"yield_vs_discount_facet_{suffix}.html"),
        ("yield_vs_discount_facet_csv", config.EXPORTS_CHART_DATA_SCATTER_DIR / f"yield_vs_discount_facet_{suffix}.csv"),
        ("yield_vs_discount_outliers_html", config.CHARTS_SCATTER_YIELD_DISCOUNT_DIR / f"yield_vs_discount_outliers_{suffix}.html"),
        ("yield_vs_discount_outliers_csv", config.EXPORTS_CHART_DATA_SCATTER_DIR / f"yield_vs_discount_outliers_{suffix}.csv"),
    ]
    return [key_output_record(name, path) for name, path in specs]


def key_output_record(name: str, path: Path) -> dict[str, Any]:
    """Вернуть запись о ключевом output, включая отсутствующие файлы."""
    if path.exists():
        record = file_record(path, with_sha=False)
        record["name"] = name
        return record
    return {
        "name": name,
        "path": relative_path(path),
        "exists": False,
        "size_bytes": 0,
        "modified_at": "",
    }


def file_record(path: Path, with_sha: bool) -> dict[str, Any]:
    """Вернуть компактную запись о файле."""
    stat = path.stat()
    record: dict[str, Any] = {
        "path": relative_path(path),
        "exists": True,
        "size_bytes": int(stat.st_size),
        "modified_at": datetime.fromtimestamp(stat.st_mtime).replace(microsecond=0).isoformat(),
    }
    if with_sha:
        record["sha256"] = sha256_file(path)
    return record


def sha256_file(path: Path) -> str:
    """Посчитать sha256 файла потоковым чтением."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def summarize_outputs(outputs: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Сформировать сводку outputs по верхним папкам."""
    total_size = sum(int(item.get("size_bytes") or 0) for item in outputs)
    by_area: dict[str, dict[str, int]] = {}
    for item in outputs:
        path = str(item.get("path", ""))
        parts = path.split("/")
        area = "/".join(parts[:2]) if len(parts) >= 2 else path
        summary = by_area.setdefault(area, {"files": 0, "size_bytes": 0})
        summary["files"] += 1
        summary["size_bytes"] += int(item.get("size_bytes") or 0)
    return {"files": len(outputs), "size_bytes": total_size, "by_area": by_area}


def build_artifact_statuses(params: report_params.ReportParams) -> dict[str, str]:
    """Проверить наличие ключевых артефактов без запуска расчетов."""
    suffix = output_suffix(params)
    checks = {
        "report_scope_exists": config.OFZ_AUCTIONS_REPORT_SCOPE_CSV.exists(),
        "charts_exist_for_params": any(config.CHARTS_DIR.rglob(f"*_{suffix}.html")) if config.CHARTS_DIR.exists() else False,
        "analytical_tables_exist_for_params": any(config.REPORTS_ANALYTICAL_TABLES_DIR.glob(f"*_{suffix}.xlsx"))
        if config.REPORTS_ANALYTICAL_TABLES_DIR.exists()
        else False,
        "analytical_csv_exist_for_params": any(config.EXPORTS_ANALYTICAL_CSV_DIR.glob(f"*_{suffix}.csv"))
        if config.EXPORTS_ANALYTICAL_CSV_DIR.exists()
        else False,
        "chart_data_exist_for_params": any(config.EXPORTS_CHART_DATA_DIR.rglob(f"*_{suffix}.csv"))
        if config.EXPORTS_CHART_DATA_DIR.exists()
        else False,
        "dashboard_exports_exist_for_params": any(config.DASHBOARDS_DIR.rglob(f"*_{suffix}.*")) if config.DASHBOARDS_DIR.exists() else False,
        "monthly_metrics_exists": (config.PROCESSED_DATA_DIR / "ofz_monthly_metrics.csv").exists(),
        "raw_data_registry_exists": (config.PROCESSED_DATA_DIR / "raw_data_registry.csv").exists(),
        "no_direct_files_in_outputs_exports": not any(path.is_file() for path in config.EXPORTS_DIR.glob("*")) if config.EXPORTS_DIR.exists() else False,
    }
    for record in collect_key_chart_outputs(params):
        checks[f"{record['name']}_exists"] = bool(record.get("exists"))
    return {name: "ok" if passed else "warning" for name, passed in checks.items()}


def output_suffix(params: report_params.ReportParams) -> str:
    """Сформировать suffix outputs."""
    return (
        f"{params.period_type}_{params.aggregation_mode}_{params.report_date.isoformat()}_"
        f"retrospective_{params.retrospective_years}"
    )


def serialize_periods(periods: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Сериализовать периоды в JSON-friendly вид."""
    result: list[dict[str, Any]] = []
    for period in periods:
        result.append(
            {
                "report_period_label": str(period.get("report_period_label") or period.get("label")),
                "report_period_display_label": str(period.get("report_period_display_label", "")),
                "report_period_file_label": str(period.get("report_period_file_label", "")),
                "period_start": iso_or_none(period.get("period_start") or period.get("start_date")),
                "period_end": iso_or_none(period.get("period_end") or period.get("end_date")),
                "report_year": optional_int(period.get("report_year")),
                "report_period_order": optional_int(period.get("report_period_order")),
                "aggregation_mode": str(period.get("aggregation_mode", "")),
                "is_target_period": bool(period.get("is_target_period", False)),
            }
        )
    return result


def iso_or_none(value: Any) -> str | None:
    """Вернуть isoformat, если объект похож на дату."""
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        return str(value.isoformat())
    return str(value)


def optional_int(value: Any) -> int | None:
    """Convert value to int unless it is missing."""
    if value is None:
        return None
    return int(value)


def parse_stages(values: Sequence[str]) -> list[str]:
    """Разобрать список этапов из CLI."""
    stages: list[str] = []
    for value in values:
        stages.extend(part.strip() for part in str(value).split(",") if part.strip())
    return stages


def parse_check_statuses(values: Sequence[str]) -> dict[str, str]:
    """Разобрать статусы проверок формата name=status."""
    statuses: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            statuses[str(value)] = "provided"
            continue
        name, status = value.split("=", 1)
        statuses[name.strip()] = status.strip()
    return statuses


def relative_path(path: Path) -> str:
    """Вернуть путь относительно корня проекта, если возможно."""
    try:
        return path.relative_to(config.PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def render_manifest_markdown(manifest: dict[str, Any]) -> str:
    """Сформировать Markdown-представление manifest."""
    outputs_summary = manifest.get("outputs_summary", {})
    by_area = outputs_summary.get("by_area", {})
    lines = [
        "# Run manifest",
        "",
        "Метка: `вторая модернизация`.",
        "",
        "## Параметры запуска",
        "",
        f"- `run_id`: `{manifest['run_id']}`",
        f"- `timestamp`: `{manifest['timestamp']}`",
        f"- `report_date`: `{manifest['report_date']}`",
        f"- `period_type`: `{manifest['period_type']}`",
        f"- `aggregation_mode`: `{manifest['aggregation_mode']}`",
        f"- `retrospective_years`: `{manifest['retrospective_years']}`",
        f"- `stages`: `{', '.join(manifest.get('stages') or [])}`",
        "",
        "## Периоды",
        "",
        "| Порядок | Период | Начало | Конец | Target |",
        "| ---: | --- | --- | --- | --- |",
    ]
    for period in manifest.get("periods", []):
        lines.append(
            "| {order} | `{label}` | `{start}` | `{end}` | `{target}` |".format(
                order=period.get("report_period_order"),
                label=period.get("report_period_label"),
                start=period.get("period_start"),
                end=period.get("period_end"),
                target=period.get("is_target_period"),
            )
        )

    lines.extend(
        [
            "",
            "## Статусы проверок",
            "",
            "| Проверка | Статус |",
            "| --- | --- |",
        ]
    )
    for name, status in sorted((manifest.get("check_statuses") or {}).items()):
        lines.append(f"| `{name}` | `{status}` |")

    lines.extend(
        [
            "",
            "## Outputs",
            "",
            f"- Файлов: `{outputs_summary.get('files', 0)}`",
            f"- Размер, байт: `{outputs_summary.get('size_bytes', 0)}`",
            "",
            "| Область | Файлов | Размер, байт |",
            "| --- | ---: | ---: |",
        ]
    )
    for area, summary in sorted(by_area.items()):
        lines.append(f"| `{area}` | {summary.get('files', 0)} | {summary.get('size_bytes', 0)} |")

    lines.extend(
        [
            "",
            "## Ключевые графики и CSV-основы",
            "",
            "| Артефакт | Путь | Статус | Размер, байт |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for item in manifest.get("key_chart_outputs", []):
        status = "exists" if item.get("exists") else "missing"
        lines.append(
            "| `{name}` | `{path}` | `{status}` | {size} |".format(
                name=item.get("name", ""),
                path=item.get("path", ""),
                status=status,
                size=item.get("size_bytes", 0),
            )
        )

    lines.extend(
        [
            "",
            "## Контрольные суммы",
            "",
            f"- Ключевых scripts: `{len(manifest.get('script_sha256') or [])}`",
            f"- Raw files: `{len(manifest.get('raw_files_sha256') or [])}`",
            "",
            "## Warnings",
            "",
        ]
    )
    warnings = manifest.get("warnings") or []
    lines.extend([f"- {item}" for item in warnings] if warnings else ["- Нет."])

    lines.extend(["", "## Limitations", ""])
    limitations = manifest.get("limitations") or []
    lines.extend([f"- {item}" for item in limitations] if limitations else ["- Нет."])

    lines.extend(
        [
            "",
            "## Файлы manifest",
            "",
        ]
    )
    for key, value in (manifest.get("manifest_files") or {}).items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
