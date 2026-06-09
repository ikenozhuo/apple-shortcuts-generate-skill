# Update Check Pattern

Use update checks for shortcuts that are shared outside a private machine. Add this only after the shortcut works locally.

## Flow

1. Read local version from config storage.
2. Download remote metadata.
3. Compare version strings or build numbers.
4. If current, continue silently or show a small result.
5. If update exists, show a menu:
   - Install update
   - View release notes
   - Ignore this version
   - Continue current version
6. Save ignored version when the user chooses to ignore.

## Remote Metadata Shape

Keep the remote response small:

```json
{
  "version": "1.2.0",
  "build": 12,
  "download_url": "https://example.com/Shortcut.shortcut",
  "notes": "Short release note text."
}
```

## Implementation Notes

- Store `version.txt` or `config.version`.
- Do not block the main task if the update endpoint is temporarily unavailable.
- Do not download and run arbitrary content silently.
- Keep update URLs and release notes outside generated examples unless the user supplies them.

## Anti-Patterns

- Checking for updates before local config exists.
- Treating a failed update check as a failed shortcut run.
- Combining update install with unrelated setup steps.
