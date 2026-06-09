# Import, Export, and Reset Pattern

Production shortcuts need user-controlled recovery paths.

## Export

Export should package settings and user artifacts without exposing sensitive values unexpectedly.

Typical flow:

1. Locate the data folder.
2. Let the user choose what to export when data may be sensitive.
3. Create an archive.
4. Share, save, or preview the archive.

## Import

Import should avoid overwriting existing data without a confirmation.

Typical flow:

1. Pick a file.
2. Validate the file type or expected folder contents.
3. Confirm overwrite or merge.
4. Restore files.
5. Show a short success/failure result.

## Reset

Reset must be explicit.

Typical flow:

1. Show a warning menu or alert.
2. Offer cancel as a first-class branch.
3. Delete only the shortcut's own data folder or known files.
4. Recreate defaults after deletion if the shortcut expects them.

## Anti-Patterns

- Resetting broad folders like Shortcuts root or iCloud Drive root.
- Exporting tokens or private files without warning.
- Importing untrusted remote data silently.
