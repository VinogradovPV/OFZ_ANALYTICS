# Word VBA Launcher Source

This folder contains source artifacts for a future Microsoft Word `.docm` launcher.

Tracked source:

- `OfzLauncher.bas`

Release artifact, not tracked by default:

- `.docm`
- `.dotm`

The `.docm` file must not be committed unless artifact policy is explicitly changed.

## Import into Word

1. Open Microsoft Word.
2. Create or open a trusted macro-enabled document.
3. Press `Alt+F11`.
4. In VBA editor, choose `File -> Import File`.
5. Import `tools/word_launcher/OfzLauncher.bas`.
6. Update `PROJECT_ROOT` in the module if needed.
7. Run `OfzSmokeTest`.

## Safety

The module:

- calls only whitelisted CLI entry points under `.venv\Scripts`;
- validates report date, period type, aggregation mode and retrospective years;
- blocks cleanup delete without `DELETE_OUTPUTS`;
- blocks release bundle creation without `BUILD_RELEASE_BUNDLE`;
- writes logs to `outputs\reports\launcher`;
- does not create GitHub releases;
- does not accept arbitrary shell commands.

## Example calls

Validate environment:

```vb
OfzValidateEnvironment
```

Run schema validation:

```vb
OfzRunAction "schema"
```

Run cleanup dry-run:

```vb
OfzRunAction "cleanup-dry-run"
```

Build release bundle with explicit confirmation:

```vb
OfzRunAction "release-build", "BUILD_RELEASE_BUNDLE"
```

Delete generated outputs with archive and explicit confirmation:

```vb
OfzRunAction "cleanup-delete-all-with-archive", "DELETE_OUTPUTS"
```

## Manual checks

If Word is available, import the `.bas` module and run:

```vb
OfzSmokeTest
```

Generated logs remain ignored artifacts and must not be staged.
