# Linear-Inspired Review UI

Use this design for dense Shortcut review pages, not for marketing pages.

## Tokens

| Role | Value |
| --- | --- |
| Canvas | `#010102` |
| Surface 1 | `#0f1011` |
| Surface 2 | `#141516` |
| Surface 3 | `#18191a` |
| Hairline | `#23252a` |
| Strong hairline | `#34343a` |
| Primary | `#5e6ad2` |
| Primary hover | `#828fff` |
| Ink | `#f7f8f8` |
| Muted ink | `#d0d6e0` |
| Subtle ink | `#8a8f98` |
| Success | `#27a644` |

## Rules

- Use a near-black canvas and charcoal surface ladder.
- Use one lavender primary accent for focus and the accept action.
- Use 1px hairline borders instead of heavy shadows.
- Keep controls compact: 8px button radius, 12-16px panel radius.
- Use system fonts and `letter-spacing: 0` for reliable Shortcuts rendering.
- Keep the page scannable: eyebrow, title, compact badges, field panels,
  sticky actions.
- Use category color only as a restrained semantic stripe or badge.

## Category Accents

- Action: lavender-blue, `#5e6ad2`
- Schedule: muted amber, `#d2995e`
- Note: muted green, `#66a98f`

Layout and button behavior remain identical across categories.

## Localization

Use a page-local translation dictionary keyed by the same persisted language
code used by the Shortcut. Pass the language code into the HTML as a Shortcut
token. Do not duplicate the page per language.

The reusable source template is
`assets/templates/linear-review.html`.

