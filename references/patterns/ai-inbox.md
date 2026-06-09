# Resilient AI Inbox

Use this architecture for shortcuts that capture raw input, ask an AI to
classify it, let the user review the result, and write to multiple apps.

## Order of Operations

```text
capture input
  -> save raw record
  -> capture optional media
  -> call AI
  -> parse strict output
  -> repair once if parsing fails
  -> show summary or per-item review
  -> write accepted items
  -> append processing report to the raw record
```

Saving the raw record before network work is mandatory. API failures, malformed
JSON, cancellation, and partial writes must not lose the original input.

## AI Contract

- Request a strict JSON array.
- Keep internal enum values stable: `Action`, `Schedule`, `Note`.
- Do not ask the model for display-only summaries when the shortcut can build
  them locally.
- Use a shared source identifier when one input produces multiple records.
- Keep secrets in import questions or user-managed configuration.

## Parse and Repair

1. Parse the first response.
2. If it is wrapped in a Markdown fence, remove only the fence.
3. If parsing still fails, make one repair request that asks only for valid
   JSON matching the original contract.
4. If the repair fails, append the error and raw response to the raw record,
   then stop before writing downstream items.

Do not loop repair requests indefinitely.

## Review

Offer:

- Accept all
- Review individually
- Cancel

For individual review, use `references/patterns/html-interaction.md`. Category
pages should emphasize different fields:

| Type | Review focus |
| --- | --- |
| Action | Executable next action, reminder date, destination list |
| Schedule | Start, end, all-day state, event title |
| Note | Captured content, title, archive destination |

## Writes and Reporting

Count accepted, skipped, and failed items independently. A downstream failure
must not erase successful writes.

Append to the raw record:

- Original AI JSON
- Accepted count
- Skipped count
- Failed count and reasons
- Final state: processed, partially processed, or pending

Entity names, folders, calendars, AI providers, prompts, and storage paths are
project configuration. Keep them out of the reusable pattern.

