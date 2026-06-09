#!/usr/bin/env python3
"""Build an Apple Shortcuts .shortcut plist from a compact JSON spec."""

from __future__ import annotations

import argparse
import json
import plistlib
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_CLIENT_VERSION = "2700.0.4"
DEFAULT_MINIMUM_CLIENT_VERSION = 900
DEFAULT_ICON = {
    "WFWorkflowIconGlyphNumber": 59511,
    "WFWorkflowIconStartColor": 4282601983,
}


def load_spec(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        spec = json.load(handle)
    if not isinstance(spec, dict):
        raise ValueError("spec root must be a JSON object")
    return spec


def normalize_action(action: dict[str, Any], index: int) -> dict[str, Any]:
    if not isinstance(action, dict):
        raise ValueError(f"actions[{index}] must be an object")

    if "WFWorkflowActionIdentifier" in action:
        identifier = action["WFWorkflowActionIdentifier"]
        params = action.get("WFWorkflowActionParameters", {})
    else:
        identifier = action.get("id") or action.get("identifier")
        params = action.get("params", {})

    if not isinstance(identifier, str) or not identifier:
        raise ValueError(f"actions[{index}] must include a non-empty id")
    if not isinstance(params, dict):
        raise ValueError(f"actions[{index}].params must be an object")

    return {
        "WFWorkflowActionIdentifier": identifier,
        "WFWorkflowActionParameters": params,
    }


def build_workflow(spec: dict[str, Any]) -> dict[str, Any]:
    actions = spec.get("actions")
    if not isinstance(actions, list):
        raise ValueError("spec must include actions as an array")

    icon = dict(DEFAULT_ICON)
    if "icon" in spec:
        if not isinstance(spec["icon"], dict):
            raise ValueError("icon must be an object")
        if "glyph" in spec["icon"]:
            icon["WFWorkflowIconGlyphNumber"] = spec["icon"]["glyph"]
        if "start_color" in spec["icon"]:
            icon["WFWorkflowIconStartColor"] = spec["icon"]["start_color"]
        icon.update(
            {
                key: value
                for key, value in spec["icon"].items()
                if key.startswith("WFWorkflowIcon")
            }
        )

    minimum_version = spec.get(
        "minimum_client_version", DEFAULT_MINIMUM_CLIENT_VERSION
    )

    workflow: dict[str, Any] = {
        "WFWorkflowActions": [
            normalize_action(action, index) for index, action in enumerate(actions)
        ],
        "WFWorkflowClientVersion": spec.get(
            "client_version", DEFAULT_CLIENT_VERSION
        ),
        "WFWorkflowHasOutputFallback": bool(
            spec.get("has_output_fallback", False)
        ),
        "WFWorkflowIcon": icon,
        "WFWorkflowImportQuestions": spec.get("import_questions", []),
        "WFWorkflowMinimumClientVersion": minimum_version,
        "WFWorkflowMinimumClientVersionString": str(minimum_version),
        "WFWorkflowName": spec.get("name", "Untitled Shortcut"),
        "WFWorkflowOutputContentItemClasses": spec.get(
            "output_content_item_classes", []
        ),
        "WFWorkflowTypes": spec.get("types", []),
    }

    optional_key_map = {
        "client_release": "WFWorkflowClientRelease",
        "input_content_item_classes": "WFWorkflowInputContentItemClasses",
        "quick_action_surfaces": "WFQuickActionSurfaces",
        "has_shortcut_input_variables": "WFWorkflowHasShortcutInputVariables",
        "no_input_behavior": "WFWorkflowNoInputBehavior",
    }
    for spec_key, plist_key in optional_key_map.items():
        if spec_key in spec:
            workflow[plist_key] = spec[spec_key]

    return workflow


def write_plist(workflow: dict[str, Any], output: Path, binary: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fmt = plistlib.FMT_BINARY if binary else plistlib.FMT_XML
    with output.open("wb") as handle:
        plistlib.dump(workflow, handle, fmt=fmt, sort_keys=False)


def sign_shortcut(input_path: Path, output_path: Path, mode: str) -> None:
    result = subprocess.run(
        [
            "shortcuts",
            "sign",
            "--mode",
            mode,
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        hint = (
            "If this runs inside Codex or another sandbox, retry `shortcuts sign` "
            "as a separate unsandboxed command after validating the plist."
        )
        raise RuntimeError(f"shortcuts sign failed: {detail}\n{hint}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an Apple Shortcuts .shortcut file from JSON."
    )
    parser.add_argument("spec", type=Path, help="Path to the JSON shortcut spec")
    parser.add_argument("--output", "-o", type=Path, required=True)
    parser.add_argument(
        "--binary",
        action="store_true",
        help="Write binary plist instead of XML plist",
    )
    parser.add_argument(
        "--sign",
        action="store_true",
        help="Sign the generated shortcut with the macOS shortcuts CLI",
    )
    parser.add_argument(
        "--mode",
        choices=("anyone", "people-who-know-me"),
        default="anyone",
        help="Signing mode used with --sign",
    )
    parser.add_argument(
        "--signed-output",
        type=Path,
        help="Signed shortcut output path. Defaults to <output stem>_signed.shortcut",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        workflow = build_workflow(load_spec(args.spec))
        write_plist(workflow, args.output, args.binary)
        print(f"Wrote {args.output}")

        if args.sign:
            signed_output = args.signed_output
            if signed_output is None:
                signed_output = args.output.with_name(
                    f"{args.output.stem}_signed{args.output.suffix}"
                )
            sign_shortcut(args.output, signed_output, args.mode)
            print(f"Signed {signed_output}")
    except (OSError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
