# Config Shortcut Pattern

A Config shortcut is a control panel for a larger shortcut system. It should be runnable by itself and safe to rerun.

## Responsibilities

- Create the data folder.
- Initialize default settings.
- Let the user change settings through menus.
- Export, import, reset, and inspect data.
- Launch the Runtime shortcut after setup when useful.

## Menu Shape

Use `is.workflow.actions.choosefrommenu` as the top-level router:

| Menu Item | Typical Branch |
| --- | --- |
| Initialize | Create folder and write defaults |
| Settings | Nested menu for toggles and choices |
| Export Data | Zip or share the data folder |
| Import Data | Pick a file and restore settings |
| Reset Data | Confirm, then delete or overwrite data |
| Start | Run the Runtime shortcut |

For exact control-flow plist structure, read `../control-flow.md`.

## Implementation Notes

- Use one stable `GroupingIdentifier` per menu block.
- Keep menu case titles exactly equal to `WFMenuItems`.
- Store defaults in files or a config dictionary before the Runtime shortcut needs them.
- Make destructive actions explicit with a confirmation alert or menu branch.
- Prefer `runworkflow` for handoff to the Runtime shortcut instead of duplicating runtime logic.

## Anti-Patterns

- Mixing setup screens into the Runtime shortcut's normal fast path.
- Hiding reset or export flows inside unrelated menus.
- Writing settings only to variables; variables disappear after the run.
- Hardcoding user secrets into generated examples.
