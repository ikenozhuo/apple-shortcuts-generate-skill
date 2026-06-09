# HTML Interaction Through Show Web Page

Use `showwebpage` when a Shortcut needs richer review UI than alerts, menus, or
Quick Look can provide.

## Action Pipeline

```text
gettext HTML with token attachments
  -> setitemname to review.html
  -> setclipboard to a sentinel value
  -> showwebpage
  -> getclipboard
  -> route from the returned protocol value
```

The `showwebpage` input should reference the renamed HTML item:

```json
{
  "id": "is.workflow.actions.showwebpage",
  "params": {
    "UUID": "33333333-3333-3333-3333-333333333333",
    "WFURL": {
      "Value": {
        "string": "￼",
        "attachmentsByRange": {
          "{0, 1}": {
            "Type": "ActionOutput",
            "OutputUUID": "22222222-2222-2222-2222-222222222222",
            "OutputName": "Renamed Item"
          }
        }
      },
      "WFSerializationType": "WFTextTokenString"
    }
  }
}
```

## Clipboard Protocol

Use a namespaced protocol rather than arbitrary display text:

```text
review:unset
review:accept
review:skip
```

Before opening the page, write the sentinel. JavaScript writes the selected
value:

```js
async function choose(value) {
  const result = `review:${value}`;
  try {
    await navigator.clipboard.writeText(result);
  } catch {
    const area = document.createElement("textarea");
    area.value = result;
    document.body.appendChild(area);
    area.select();
    document.execCommand("copy");
    area.remove();
  }
}
```

The user normally must tap Done to return from the Shortcuts web view. State
this inside the page.

## Token Safety

Shortcut variables embedded in HTML are U+FFFC characters with matching
`attachmentsByRange` entries. Hand-calculated offsets break whenever HTML
changes.

Use:

```bash
python3 scripts/render_token_template.py \
  assets/templates/linear-review.html \
  bindings.json \
  --output review-token.json
```

The script replaces `{{bindingName}}` placeholders with U+FFFC and calculates
all ranges. Run `validate_shortcut.py` after inserting the result.

## Security

- Escape or tokenize user data; do not concatenate untrusted text into
  executable JavaScript.
- Keep secrets out of HTML.
- Treat clipboard contents as untrusted and accept only known protocol values.
- Use a sentinel so closing the page without choosing cannot be mistaken for
  acceptance.

