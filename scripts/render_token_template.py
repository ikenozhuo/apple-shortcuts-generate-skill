#!/usr/bin/env python3
"""Render template placeholders into a Shortcuts WFTextTokenString value."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


PLACEHOLDER_RE = re.compile(r"\{\{([A-Za-z][A-Za-z0-9_.-]*)\}\}")
OBJECT_REPLACEMENT_CHARACTER = "\ufffc"


def load_bindings(path: Path) -> dict[str, dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("bindings JSON must be an object")
    for name, binding in value.items():
        if not isinstance(binding, dict):
            raise ValueError(f"binding {name!r} must be an object")
        if not isinstance(binding.get("Type"), str):
            raise ValueError(f"binding {name!r} must contain a string Type")
    return value


def render_template(
    template: str, bindings: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    parts: list[str] = []
    attachments: dict[str, dict[str, Any]] = {}
    used: set[str] = set()
    source_position = 0
    output_position = 0

    for match in PLACEHOLDER_RE.finditer(template):
        literal = template[source_position : match.start()]
        parts.append(literal)
        output_position += len(literal)

        name = match.group(1)
        if name not in bindings:
            raise ValueError(f"template binding {name!r} is missing")
        parts.append(OBJECT_REPLACEMENT_CHARACTER)
        attachments[f"{{{output_position}, 1}}"] = bindings[name]
        used.add(name)
        output_position += 1
        source_position = match.end()

    tail = template[source_position:]
    parts.append(tail)

    unused = sorted(set(bindings) - used)
    if unused:
        raise ValueError(f"unused bindings: {', '.join(unused)}")

    return {
        "Value": {
            "string": "".join(parts),
            "attachmentsByRange": attachments,
        },
        "WFSerializationType": "WFTextTokenString",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Replace {{name}} placeholders with U+FFFC and emit a "
            "WFTextTokenString JSON object with calculated attachmentsByRange."
        )
    )
    parser.add_argument("template", type=Path)
    parser.add_argument("bindings", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        template = args.template.read_text(encoding="utf-8")
        bindings = load_bindings(args.bindings)
        result = render_template(template, bindings)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"error: {error}") from error

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

