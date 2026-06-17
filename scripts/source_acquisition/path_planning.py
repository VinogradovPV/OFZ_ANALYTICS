"""Dry-run path planning for controlled Minfin storage.

P3.1 deliberately returns planned paths only; it does not create raw storage
directories and does not write registry files.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass(frozen=True)
class PlannedStoragePaths:
    output_root: str
    latest_path: str
    final_path: str
    registry_csv_path: str
    registry_json_path: str
    version_snapshot_dir: str
    temp_download_path: str
    report_path: str
    annual_final_report_path: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def build_storage_paths(output_root: str | Path, year: int) -> PlannedStoragePaths:
    root = Path(output_root)
    base = root / "data" / "raw" / "minfin" / "ofz_auction_results"
    return PlannedStoragePaths(
        output_root=str(root),
        latest_path=str(base / "latest" / f"INTERNET_Auction_Results_rus_{year}_latest.xlsx"),
        final_path=str(base / "final" / f"INTERNET_Auction_Results_rus_{year}_final.xlsx"),
        registry_csv_path=str(base / "registry" / "minfin_ofz_auction_sources.csv"),
        registry_json_path=str(base / "registry" / "minfin_ofz_auction_sources_latest.json"),
        version_snapshot_dir=str(base / "versions" / str(year)),
        temp_download_path=str(root / "outputs" / "tmp" / "source_acquisition" / f"minfin_{year}.download"),
        report_path=str(root / "outputs" / "reports" / "source_acquisition" / f"minfin_monthly_{year}.json"),
        annual_final_report_path=str(
            root / "outputs" / "reports" / "source_acquisition" / f"minfin_annual_final_{year}.json"
        ),
    )


def build_version_snapshot_path(output_root: str | Path, year: int, file_name: str, sha256: str) -> Path:
    root = Path(output_root)
    stem = Path(file_name).stem
    suffix = Path(file_name).suffix
    return (
        root
        / "data"
        / "raw"
        / "minfin"
        / "ofz_auction_results"
        / "versions"
        / str(year)
        / f"{stem}_{sha256[:12]}{suffix}"
    )
