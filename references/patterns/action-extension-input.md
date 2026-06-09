# Action Extension Input Pattern

Use this pattern when the shortcut should work from Share Sheet, Search, Siri, or direct app launch.

## Root Metadata

Set accepted input types in the JSON spec:

```json
{
  "types": ["ActionExtension", "WFWorkflowTypeShowInSearch"],
  "input_content_item_classes": [
    "WFStringContentItem",
    "WFURLContentItem",
    "WFImageContentItem",
    "WFGenericFileContentItem",
    "WFPDFContentItem",
    "WFSafariWebPageContentItem"
  ],
  "has_shortcut_input_variables": true,
  "no_input_behavior": {
    "Name": "Ask For Text"
  }
}
```

The exact `no_input_behavior` payload varies by Shortcuts version. When uncertain, inspect an exported shortcut that already has the desired no-input setting.

## Input Strategy

1. Reference Extension Input for Share Sheet data.
2. If no input exists, ask the user, read clipboard, or show a mode menu.
3. Normalize input into one variable.
4. Route by type or selected mode.

## Variable Reference

Use `Type: "ExtensionInput"` in token attachments when referring to Shortcut Input. For general variable/token syntax, read `../variables.md`.

## Anti-Patterns

- Assuming the shortcut always starts with text.
- Ignoring files or images after declaring them as accepted inputs.
- Asking for input before checking whether Share Sheet input already exists.
