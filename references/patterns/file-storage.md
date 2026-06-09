# File Storage Pattern

Complex shortcuts need persistent state. Use either file-per-setting storage or one dictionary/JSON config file.

## Option A: File Per Setting

Use this when users may inspect, replace, or recover individual values.

Example layout:

```text
ShortcutName/
  mode.txt
  privacy.txt
  model.txt
  name.txt
  version.txt
  artifacts/
```

Best for:

- Simple toggles.
- One setting changed at a time.
- Human-readable support instructions.
- Partial reset or migration.

Tradeoff: many file actions and more existence checks.

## Option B: Config JSON

Use this when settings are related and should migrate together.

Example shape:

```json
{
  "version": "1.0.0",
  "mode": "text",
  "privacy": true,
  "model": "default",
  "features": {
    "artifacts": true
  }
}
```

Best for:

- Versioned migrations.
- Nested state.
- Many settings loaded at once.
- Dictionary-driven routing.

Tradeoff: harder for users to repair manually.

## Storage Rules

- Define the folder name before writing actions.
- Write defaults before first read.
- Keep version data near config data.
- For secrets, use import questions, user-provided files, or user entry flows; do not place real secrets in templates.
- For artifacts, keep generated files separate from settings.
