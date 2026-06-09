# Shortcuts Generator — Programmatic Apple Shortcuts Builder

[![macOS](https://img.shields.io/badge/macOS-≥14.0-blue?logo=apple)](https://support.apple.com/shortcuts)
[![Python](https://img.shields.io/badge/Python-≥3.10-blue?logo=python)](https://python.org)

**A code-driven toolkit to create, validate, sign, inspect, and unpack macOS/iOS Apple Shortcuts.**

Stop dragging blocks around. Describe your automation as JSON, generate a `.shortcut` file, sign it with the macOS `shortcuts` CLI, and import it directly to your device.

---

## Table of Contents

- [Why This Tool?](#why-this-tool)
- [Quick Start](#quick-start)
- [Workflow Overview](#workflow-overview)
- [Script Reference](#script-reference)
- [Reference Docs](#reference-docs)
- [JSON Spec Format](#json-spec-format-1)
- [Advanced Patterns](#advanced-patterns)
- [FAQ](#faq)

---

## Why This Tool?

| Scenario | Manual Shortcuts.app | Shortcuts Generator |
|----------|---------------------|---------------------|
| Complex workflows | Drag & configure, error-prone | JSON description, version-controlled |
| Batch / repetitive creation | One at a time | Scripted bulk generation |
| Team collaboration | Can't diff | `.shortcut` is diffable |
| Validation | Must run to find out | Static validation catches issues early |
| AI generation | ❌ Can't generate directly | JSON spec → signed file in one step |

---

## Quick Start

### Prerequisites

- macOS 14.0+ (requires the `shortcuts` CLI)
- Python 3.10+

### Setup

```bash
git clone https://github.com/drewocarr/generate-shortcuts-skill.git
cd generate-shortcuts-skill
```

All dependencies are Python stdlib — no `pip install` or virtual environment needed.

### Minimal Example

Create a shortcut that says "Hello World":

**spec.json**
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

```bash
# 1. Generate the .shortcut file
python3 scripts/build_shortcut.py spec.json --output Hello.shortcut

# 2. Validate
python3 scripts/validate_shortcut.py Hello.shortcut
plutil -lint Hello.shortcut

# 3. Sign (produces an importable file)
shortcuts sign --mode anyone --input Hello.shortcut --output Hello_signed.shortcut
```

Double-click `Hello_signed.shortcut` to import.

---

## Workflow Overview

```
User request → JSON Spec → build_shortcut.py → .shortcut plist
                              ↓
                         validate_shortcut.py ←─── Issues? Back to JSON
                              ↓
                         plutil -lint
                              ↓
                         shortcuts sign → xxx_signed.shortcut → Import into Shortcuts.app
```

Reverse direction for existing signed files:

```
Signed .shortcut → extract_shortcut.py → Plaintext XML plist → Edit → Re-sign
```

---

## Script Reference

| Script | Purpose | Key Features |
|--------|---------|-------------|
| `scripts/build_shortcut.py` | JSON spec → `.shortcut` plist | XML / binary plist, optional inline signing |
| `scripts/validate_shortcut.py` | Static plist validation | 20+ rules: UUID format, variable refs, control flow closure, param structure |
| `scripts/extract_shortcut.py` | Unpack signed `.shortcut` | Handles AEA1 format, extracts plaintext XML |
| `scripts/render_token_template.py` | Render text token templates | Auto-calculates U+FFFC placeholder offsets |
| `scripts/build_localized_menu.py` | Generate multi-language menu specs | Locale key parity validation, stable UUIDs |
| `scripts/link_skill.sh` | Shell helper | Quick-link tool |

### build_shortcut.py

Compiles a JSON spec into the standard Apple Shortcuts plist format (.shortcut).

```bash
# Basic usage
python3 scripts/build_shortcut.py spec.json --output MyShortcut.shortcut

# Generate and sign in one pass
python3 scripts/build_shortcut.py spec.json --output MyShortcut.shortcut --sign

# Specify minimum client version
python3 scripts/build_shortcut.py spec.json --output MyShortcut.shortcut \
  --client-version 3000.0.0
```

### validate_shortcut.py

Checks for common structural errors including:

- ✅ Every action has `WFWorkflowActionIdentifier` and `WFWorkflowActionParameters`
- ✅ UUIDs are uppercase format
- ✅ Variable references (`attachmentsByRange`) point to existing action UUIDs
- ✅ Control flow (Repeat / If / Menu) pairs are closed, `WFControlFlowMode` is integer
- ✅ U+FFFC token string offsets match
- ✅ `choosefromlist` multi-language menu inputs are correct
- ✅ Common parameter typos

```bash
python3 scripts/validate_shortcut.py MyShortcut.shortcut
```

### extract_shortcut.py

Modern Apple Shortcuts use AEA1 (Apple Encryption Archive 1) signing, which `plutil` can't read directly. This script unpacks and restores plaintext XML.

```bash
python3 scripts/extract_shortcut.py Input.shortcut --output Input_plaintext.plist

# Debug mode: keep intermediate files
python3 scripts/extract_shortcut.py Input.shortcut --output Input_plaintext.plist \
  --keep-workdir debug-dir
```

### render_token_template.py

Processes text templates containing variable placeholders. Converts `{{variable_name}}` to U+FFFC placeholder characters and auto-calculates `attachmentsByRange` offset arrays.

```bash
python3 scripts/render_token_template.py template.json
```

### build_localized_menu.py

Generates stable JSON specs for multi-language menus. Ensures the same logical option maps to the same internal UUID across languages.

```bash
python3 scripts/build_localized_menu.py spec.json --locales zh,en,ja --output menu_spec.json
```

---

## Reference Docs

The `references/` directory contains detailed reverse-engineered documentation of Apple Shortcuts internals:

| File | Content |
|------|---------|
| `actions.md` | `is.workflow.actions.*` identifiers and common parameters |
| `appintents.md` | AppIntents (wrapper and direct identifiers) |
| `parameter-types.md` | Complex dictionaries, attachments, Quantity, Token strings |
| `variables.md` | `OutputUUID`, `OutputName`, `attachmentsByRange`, U+FFFC |
| `control-flow.md` | Repeat, If/Otherwise, Menu grouping |
| `filters.md` | `WFContentItemFilter` payloads |
| `plist-format.md` | Root workflow keys, icon/input/output metadata |
| `examples.md` | Complete working patterns |
| `extraction.md` | Manual extraction and troubleshooting |
| `design/linear-review-ui.md` | Linear-style HTML review UI design |
| `patterns/` | Advanced architecture patterns (see below) |

### Advanced Patterns

`references/patterns/` covers production-grade Shortcut architecture:

- **config-shortcut.md** — Separate settings / control panel shortcut
- **main-runtime.md** — Runtime shortcut that reads config, handles inputs, routes work
- **file-storage.md** — File-per-setting and JSON/dictionary persistence
- **update-check.md** — Version check and update prompt flow
- **import-export-reset.md** — Backup, import, export, reset
- **action-extension-input.md** — Share Sheet and no-input fallback design
- **localization.md** — Locale dictionaries, first-run language choice, dynamic menus
- **html-interaction.md** — HTML review pages returning decisions through the clipboard
- **ai-inbox.md** — Durable AI capture, repair, review, write, and reporting flow

Each pattern doc includes complete JSON spec structure and design rationale.

---

## JSON Spec Format

### Basic Structure

```json
{
  "name": "Shortcut Name",
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

### Optional Root Fields

```json
{
  "client_version": "2700.0.4",
  "client_release": "2700.0.4",
  "minimum_client_version": "2700",
  "icon": {
    "glyph": "ShortcutGlyphTypeApple",
    "start_color": "3679C8FF"
  },
  "input_content_item_classes": ["WFContentItem"],
  "output_content_item_classes": ["WFContentItem"],
  "import_questions": [],
  "quick_action_surfaces": [],
  "has_output_fallback": false,
  "has_shortcut_input_variables": false,
  "no_input_behavior": false
}
```

### Core Rules

1. **Every action needs `id` (→ `WFWorkflowActionIdentifier`) and `params` (→ `WFWorkflowActionParameters`)**
2. **Referenced action UUIDs must be uppercase**, e.g. `11111111-1111-1111-1111-111111111111`
3. **Variable references** use `OutputUUID`, `OutputName`, `Type` inside `attachmentsByRange`
4. **Token strings** use the U+FFFC object replacement character paired with `{offset, length}` range keys
5. **Control flow mode** `WFControlFlowMode` is integer: `0`=start, `1`=middle, `2`=end
6. **Grouping** (Repeat / If / Menu) requires matching `GroupingIdentifier`

---

## Advanced Patterns

### Multi-language Dynamic Menus

Combine `build_localized_menu.py` + `references/patterns/localization.md` to generate:

- Same logical option → same UUID across languages
- Runtime displays the user's preferred language
- `choosefromlist` results match through consistent route values

See `examples/advanced/localized-review/` for a complete walkthrough.

### HTML Review UI

Embed an HTML page via the `showwebpage` action; user actions return decisions through the clipboard. Design doc at `references/design/linear-review-ui.md`, template at `assets/templates/linear-review.html`.

### AI Inbox Workflow

`references/patterns/ai-inbox.md` describes a production-grade "capture-first, classify-later" Shortcut architecture:

1. **Capture** — Share Sheet / shortcut trigger / alarm
2. **AI Classification** — Identify type, extract key info
3. **Repair** — Graceful degradation on parse failures
4. **Review** — HTML review interface
5. **Write** — Multi-app writes (Notes, Reminders, Files…)
6. **Report** — Summarize results

### Config + Runtime Separation

A two-shortcut architecture (Config + Runtime) for a settings system:

- `examples/advanced/config-and-runtime/` provides a minimal buildable skeleton
- Config shortcut manages all user settings
- Runtime shortcut reads config, handles input, routes execution

---

## FAQ

### My generated .shortcut won't import?

```bash
# 1. Check plist structure
plutil -lint MyShortcut.shortcut

# 2. Run full validation
python3 scripts/validate_shortcut.py MyShortcut.shortcut

# 3. Confirm it's signed
head -c 4 MyShortcut.shortcut   # should output AEA1

# 4. Extract and inspect
python3 scripts/extract_shortcut.py MyShortcut.shortcut --output debug.plist
```

### `plutil -lint` passes but import still fails with a format error?

Some sandbox / runtime environments restrict the `shortcuts` CLI. Use separate signing:

```bash
shortcuts sign --mode anyone --input MyShortcut.shortcut --output MyShortcut_signed.shortcut
```

If it fails inside the sandbox, re-run the same sign command outside — no plist changes needed.

### Where do I find action IDs and parameters?

Check `references/actions.md` (legacy `is.workflow.actions.*`) and `references/appintents.md` (AppIntents). For complex parameter types, see `references/parameter-types.md`.

### How do I inspect or annotate an existing shortcut?

Use `extract_shortcut.py` to unpack the signed file to plaintext XML. Edit with any text editor, then re-sign.

---

## Project Structure

```
├── SKILL.md                    # Skill entry point (for Reasonix / Codex Agent)
├── scripts/
│   ├── build_shortcut.py       # JSON → .shortcut compiler
│   ├── build_localized_menu.py # Multi-language menu generator
│   ├── render_token_template.py# Token template renderer
│   ├── validate_shortcut.py    # Structure validator
│   ├── extract_shortcut.py     # Signed file extractor
│   └── link_skill.sh           # Shell helper
├── references/
│   ├── actions.md, appintents.md, parameter-types.md ...
│   ├── patterns/               # Advanced architecture patterns
│   └── design/                 # UI design docs
├── assets/templates/           # HTML / UI templates
├── examples/advanced/          # Buildable complete examples
│   ├── config-and-runtime/
│   └── localized-review/
└── agents/
    └── openai.yaml             # AI Agent configuration
```

---

## License

MIT
