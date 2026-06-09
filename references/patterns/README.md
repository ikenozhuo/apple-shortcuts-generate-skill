# Complex Shortcut Patterns

Use these pattern notes when building shortcuts that behave like small apps rather than single-purpose macros.

## When to Read

- Need settings, account state, model choices, privacy toggles, or persistent data: read `config-shortcut.md` and `file-storage.md`.
- Need a main shortcut that can run from the app, Siri, Search, or Share Sheet: read `main-runtime.md` and `action-extension-input.md`.
- Need user-managed data export, import, reset, or backup: read `import-export-reset.md`.
- Need distributed shortcuts with versions or install/update prompts: read `update-check.md`.
- Need localized prompts or menus: read `localization.md`.
- Need a rich review page that returns a decision: read `html-interaction.md`.
- Need capture-first AI classification and multi-app writes: read `ai-inbox.md`.

## Architecture Rule

Split complex systems into shortcuts with clear roles:

| Shortcut | Responsibility |
| --- | --- |
| Config | Setup, settings, import/export, reset, diagnostics |
| Runtime | Accept input, load config, run the main task, return output |
| Helpers | Optional focused subflows called with `runworkflow` |

Keep sensitive values in user-managed storage or import questions. Do not hardcode tokens in examples or generated docs.

## Build Order

1. Define the data folder and config keys.
2. Draft the menu tree.
3. Generate the Config shortcut.
4. Generate the Runtime shortcut.
5. Add import/export/reset flows.
6. Add update checks only after the local workflow is stable.

See `../../examples/advanced/config-and-runtime/` for a minimal JSON spec suite.
