# Dictionary-Driven Localization

Use one current-language UI dictionary instead of duplicating the workflow for
each language.

## Data Model

Persist a stable language code such as `zh-Hans`, `zh-Hant`, `en`, `ja`, or
`zh`. Keep display names separate from stored codes.

Each locale must expose the same keys:

```json
{
  "mainPrompt": "Choose a function",
  "menuCollect": "Inbox",
  "menuSettings": "Settings",
  "settingsLanguage": "Display language",
  "settingsBack": "Back"
}
```

At startup:

1. Read the persisted language code.
2. Initialize `ui` with the default locale dictionary.
3. Replace `ui` when the stored code matches another locale.
4. Read required strings from `ui` with `getvalueforkey`.
5. Store frequently reused values in named variables.

All locale dictionaries must have identical key sets. Treat missing keys as a
build error, not a runtime fallback.

## Dynamic Menus

`choosefrommenu` branch titles are static. Do not duplicate the main workflow
to localize them.

Use this pattern:

```text
ui dictionary
  -> get menuCollect/menuSettings/...
  -> list
  -> choosefromlist
  -> compare the selected value with the same localized variables
  -> route to stable workflow branches
```

Verified action shapes:

```json
{
  "id": "is.workflow.actions.list",
  "params": {
    "UUID": "11111111-1111-1111-1111-111111111111",
    "WFItems": ["Inbox", "Settings"]
  }
}
```

```json
{
  "id": "is.workflow.actions.choosefromlist",
  "params": {
    "UUID": "22222222-2222-2222-2222-222222222222",
    "WFChooseFromListActionPrompt": "Choose a function",
    "WFInput": {
      "Value": {
        "Type": "ActionOutput",
        "OutputUUID": "11111111-1111-1111-1111-111111111111",
        "OutputName": "List"
      },
      "WFSerializationType": "WFTextTokenAttachment"
    }
  }
}
```

Use `scripts/build_localized_menu.py` to validate locale key parity and
generate the dictionary-selection and dynamic-menu action fragment.

```bash
python3 scripts/build_localized_menu.py \
  examples/advanced/localized-review/locales.example.json \
  --default-locale zh-Hans \
  --prompt-key mainPrompt \
  --menu-key menuCollect \
  --menu-key menuReview \
  --menu-key menuSettings \
  --output localized-menu.spec.json
```

The output is a buildable JSON spec. Extend it with conditionals that compare
`selectedMenuItem` against `ui_menuCollect`, `ui_menuReview`, and
`ui_menuSettings`.

## First Run and Settings

- Persist the language code in iCloud Shortcuts storage or the shortcut's
  existing config file.
- If the file is missing, show the language picker before the main menu.
- Provide a settings route that writes the new stable code and exits cleanly.
- Rebuild the `ui` dictionary on the next run.

## Boundaries

- Localize user-visible prompts, menu items, alerts, HTML labels, and status
  messages.
- Do not translate stable internal values such as `Action`, `Schedule`, `Note`,
  JSON keys, route identifiers, or persisted language codes.
- Do not use localized text as long-term stored data when a stable code exists.
