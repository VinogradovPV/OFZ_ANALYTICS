# Legacy maintenance scripts archive

Date: 2026-06-15.

This folder contains legacy maintenance utilities moved during `P2.10 Controlled legacy scripts archive apply`.

Archived scripts:

- `cleanup_docs.py`
- `migrate_outputs_structure.py`
- `reorganize_outputs.py`
- `migrate_legacy_docs_archive.py`
- `reorganize_docs.py`

These files are kept for audit and historical reproducibility only. They are not production entry points and should not be used for new production runs.

Current replacements:

- outputs cleanup: `ofz-clean-outputs` / `scripts/maintenance/cleanup_outputs.py`
- docs cleanup: `scripts/maintenance/cleanup_docs.py`
- release bundle: `ofz-build-release-bundle` / `scripts/maintenance/build_release_bundle.py`

No files were deleted in this stage.
