---
name: shortcuts-generator
description: Generate, validate, sign, inspect, and unpack macOS/iOS Apple Shortcuts. Use when asked to create shortcuts, automate workflows, build .shortcut files, generate Shortcuts plists, build localized dynamic menus or HTML review interfaces, sign shortcuts with the macOS shortcuts CLI, extract plaintext XML from signed AEA1 .shortcut files, or reverse-engineer Shortcuts workflows. Covers WF*Actions, AppIntents, variable references, control flow, filters, plist structure, signing, extraction, dictionary-driven localization, and show-web-page clipboard interaction.
allowed-tools: Write, Bash
---

# macOS Shortcuts Generator

Create importable Apple Shortcuts by generating plist-backed `.shortcut` files, validating them, and signing them with the macOS `shortcuts` CLI. Inspect existing signed shortcuts by extracting their plaintext workflow plist.

## Start by Classifying the Task

- **Create or edit a shortcut**: Build a JSON spec, generate a `.shortcut` plist with `scripts/build_shortcut.py`, validate it with `scripts/validate_shortcut.py`, then run `shortcuts sign` as a separate command if the user wants an importable file.
- **Inspect or unpack a shortcut**: Use `scripts/extract_shortcut.py` for signed `AEA1` files. Use `plutil -convert xml1` directly only when the input is already a raw plist.
- **Look up action details**: Read only the reference file needed for the feature being built.
- **Debug a failed import**: Validate the plist first, then check signing, variable references, and control-flow grouping.

## Create Workflow

1. Translate the user's request into a short action list.
2. Read the smallest relevant reference files:
   - `references/actions.md` for legacy `is.workflow.actions.*` identifiers and common parameters.
   - `references/appintents.md` for AppIntents, including wrapper-based and direct AppIntent identifiers.
   - `references/parameter-types.md` for complex dictionaries, attachments, quantities, and token strings.
   - `references/variables.md` for `OutputUUID`, `OutputName`, `attachmentsByRange`, and U+FFFC placeholders.
   - `references/control-flow.md` for repeat, if/otherwise, and menu grouping.
   - `references/filters.md` for `WFContentItemFilter` payloads.
   - `references/plist-format.md` for root workflow keys and icon/input/output metadata.
   - `references/examples.md` for complete working patterns.
   - `references/patterns/README.md` for complex shortcut architecture patterns learned from production shortcuts.
   - `references/patterns/localization.md` for dictionary-driven UI strings and dynamic localized menus.
   - `references/patterns/html-interaction.md` for `showwebpage` review UI and clipboard return values.
   - `references/patterns/ai-inbox.md` for capture-first AI classification, repair, review, and multi-app writes.
   - `references/design/linear-review-ui.md` for the reusable Linear-inspired review design.
3. Write a compact JSON spec and generate the shortcut:

```bash
python3 scripts/build_shortcut.py spec.json --output MyShortcut.shortcut
```

4. Validate the generated plist:

```bash
python3 scripts/validate_shortcut.py MyShortcut.shortcut
plutil -lint MyShortcut.shortcut
```

5. Sign the shortcut when it needs to be imported:

```bash
shortcuts sign --mode anyone --input MyShortcut.shortcut --output MyShortcut_signed.shortcut
```

When running from Codex, call `shortcuts sign` as a separate command after validation so sandbox failures can be retried unsandboxed. If a validated plist gets `The file couldn't be opened because it isn't in the correct format` only inside the sandbox, retry the same `shortcuts sign` command with elevated/unsandboxed execution before changing the plist.

`scripts/build_shortcut.py --sign` remains useful from a normal terminal, but the separate signing command is preferred in agent workflows.

## JSON Spec Format

Use `id` for the action identifier and `params` for `WFWorkflowActionParameters`.

```json
{
  "name": "Hello World",
  "actions": [
    {
      "id": "is.workflow.actions.gettext",
      "params": {
        "UUID": "11111111-1111-1111-1111-111111111111",
        "WFTextActionText": "Hello World"
      }
    }
  ]
}
```

Supported optional root fields:

- `client_version`, `client_release`, `minimum_client_version`
- `icon.glyph`, `icon.start_color`, or full `WFWorkflowIcon*` keys
- `input_content_item_classes`, `output_content_item_classes`, `types`
- `import_questions`, `has_output_fallback`
- `quick_action_surfaces`, `has_shortcut_input_variables`, `no_input_behavior`

For advanced parameters, put the exact plist-shaped dictionaries in `params`; the builder preserves nested dictionaries, arrays, booleans, numbers, and U+FFFC token strings.

## Core Shortcut Rules

- Every action dictionary needs `WFWorkflowActionIdentifier` and `WFWorkflowActionParameters`; the JSON builder creates these from `id` and `params`.
- Actions that will be referenced later need an uppercase UUID.
- Variable references use `OutputUUID`, `OutputName`, and `Type` inside `attachmentsByRange`.
- Text token strings use the object replacement character U+FFFC at the same positions named by range keys such as `{0, 1}`.
- Generate long HTML/text token strings with `scripts/render_token_template.py`; do not hand-maintain offsets after editing the source.
- `WFControlFlowMode` must be an integer: `0` start, `1` middle, `2` end.
- Every repeat, conditional, or menu group needs matching actions with the same `GroupingIdentifier`.
- `is.workflow.actions.deletephotos` uses the `photos` parameter, not `WFInput`.
- For localized menus, keep stable language codes and internal route values. Build visible menu items from one current-language dictionary and route `choosefromlist` results against the same localized variables.
- Save raw user input before AI or network work. Stop downstream writes after unrecoverable parsing errors.

## Inspect or Extract Existing Shortcuts

Modern signed shortcuts often begin with `AEA1`; `plutil` cannot read them directly. Extract plaintext XML with:

```bash
python3 scripts/extract_shortcut.py Input.shortcut --output Input_plaintext.plist
```

Use `--keep-workdir debug-dir` when debugging certificate, AEA, or Apple Archive steps. If extraction fails, read `references/extraction.md` for the manual workflow and troubleshooting table.

After editing plaintext XML, convert it back to an accepted shortcut format and re-sign it for import:

```bash
shortcuts sign --mode anyone --input edited.shortcut --output edited_signed.shortcut
```

## Script Reference

- `scripts/build_shortcut.py`: Convert JSON spec to XML or binary plist `.shortcut`; optionally sign.
- `scripts/build_localized_menu.py`: Validate locale key parity and generate a dictionary-driven dynamic menu JSON spec.
- `scripts/render_token_template.py`: Replace named template placeholders with U+FFFC and calculate `attachmentsByRange`.
- `scripts/validate_shortcut.py`: Check root structure, action dictionaries, uppercase UUID fields, token ranges, dynamic menu inputs, control-flow closure, integer modes, and common parameter mistakes.
- `scripts/extract_shortcut.py`: Extract signed AEA1 `.shortcut` files to readable XML plist using macOS archive/signing tools.

## Complex Shortcut Patterns

When a shortcut is more than a short linear automation, use the pattern docs before writing actions:

- `references/patterns/config-shortcut.md`: Separate settings/control-panel shortcut.
- `references/patterns/main-runtime.md`: Runtime shortcut that reads config, handles inputs, and routes work.
- `references/patterns/file-storage.md`: File-per-setting and JSON/dictionary persistence.
- `references/patterns/update-check.md`: Version check and update prompt flow.
- `references/patterns/import-export-reset.md`: Backup, import, export, and reset flows.
- `references/patterns/action-extension-input.md`: Share Sheet and no-input fallback design.
- `references/patterns/localization.md`: Locale dictionaries, first-run language choice, and dynamic menus.
- `references/patterns/html-interaction.md`: HTML review pages that return a decision through the clipboard.
- `references/patterns/ai-inbox.md`: Durable AI capture, repair, review, write, and reporting flow.

For a minimal buildable suite skeleton, start with `examples/advanced/config-and-runtime/`.
For localized menu and HTML token inputs, start with `examples/advanced/localized-review/`.

## Validation Expectations

For generated shortcuts, run `scripts/validate_shortcut.py` and `plutil -lint` before signing. If the local machine has the `shortcuts` CLI and the user wants an importable file, sign the generated shortcut, confirm the output starts with `AEA1`, extract it again, and validate the extracted plaintext before reporting the signed output path.

```bash
python3 scripts/validate_shortcut.py MyShortcut.shortcut
plutil -lint MyShortcut.shortcut
shortcuts sign --mode anyone --input MyShortcut.shortcut --output MyShortcut_signed.shortcut
xxd -l 4 MyShortcut_signed.shortcut
python3 scripts/extract_shortcut.py MyShortcut_signed.shortcut --output MyShortcut_signed_plaintext.plist
python3 scripts/validate_shortcut.py MyShortcut_signed_plaintext.plist
```
