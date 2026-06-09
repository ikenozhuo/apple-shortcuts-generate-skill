#!/usr/bin/env python3
"""Validate common Apple Shortcuts plist structure mistakes."""

from __future__ import annotations

import argparse
import plistlib
import re
import sys
from pathlib import Path
from typing import Any


UUID_RE = re.compile(
    r"^[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}$"
)
RANGE_RE = re.compile(r"^\{(\d+),\s*(\d+)\}$")
OBJECT_REPLACEMENT_CHARACTER = "\ufffc"
CONTROL_FLOW_IDENTIFIERS = {
    "is.workflow.actions.repeat.count",
    "is.workflow.actions.repeat.each",
    "is.workflow.actions.conditional",
    "is.workflow.actions.choosefrommenu",
}


def load_plist(path: Path) -> Any:
    with path.open("rb") as handle:
        prefix = handle.read(4)
        handle.seek(0)
        if prefix == b"AEA1":
            raise ValueError(
                "file is an AEA1 signed shortcut; extract plaintext first"
            )
        return plistlib.load(handle)


def walk_values(value: Any, path: str):
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key), child, f"{path}.{key}"
            yield from walk_values(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield str(index), child, f"{path}[{index}]"
            yield from walk_values(child, f"{path}[{index}]")


def walk_nodes(value: Any, path: str):
    yield value, path
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk_nodes(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_nodes(child, f"{path}[{index}]")


def validate_uuid_fields(params: dict[str, Any], action_index: int) -> list[str]:
    errors = []
    for key, value, path in walk_values(params, f"actions[{action_index}].params"):
        if key in {"UUID", "OutputUUID", "GroupingIdentifier"}:
            if not isinstance(value, str) or not UUID_RE.match(value):
                errors.append(f"{path} must be an uppercase UUID")
    return errors


def validate_token_strings(params: dict[str, Any], action_index: int) -> list[str]:
    errors = []
    root_path = f"actions[{action_index}].params"
    for value, path in walk_nodes(params, root_path):
        if not isinstance(value, dict):
            continue
        if value.get("WFSerializationType") != "WFTextTokenString":
            continue

        state = value.get("Value")
        if not isinstance(state, dict):
            errors.append(f"{path}.Value must be a dictionary")
            continue
        string = state.get("string")
        if not isinstance(string, str):
            errors.append(f"{path}.Value.string must be a string")
            continue
        attachments = state.get("attachmentsByRange", {})
        if not isinstance(attachments, dict):
            errors.append(f"{path}.Value.attachmentsByRange must be a dictionary")
            continue

        covered_positions: set[int] = set()
        for range_key, attachment in attachments.items():
            match = RANGE_RE.match(str(range_key))
            if not match:
                errors.append(
                    f"{path}.Value.attachmentsByRange[{range_key!r}] "
                    "must use '{start, length}'"
                )
                continue
            start, length = (int(part) for part in match.groups())
            if length != 1:
                errors.append(
                    f"{path}.Value.attachmentsByRange[{range_key!r}] "
                    "must have length 1"
                )
                continue
            if start >= len(string):
                errors.append(
                    f"{path}.Value.attachmentsByRange[{range_key!r}] "
                    f"starts outside a {len(string)} character string"
                )
                continue
            if string[start] != OBJECT_REPLACEMENT_CHARACTER:
                errors.append(
                    f"{path}.Value.attachmentsByRange[{range_key!r}] "
                    "does not point to U+FFFC"
                )
            if start in covered_positions:
                errors.append(
                    f"{path}.Value.attachmentsByRange has duplicate position {start}"
                )
            covered_positions.add(start)
            if not isinstance(attachment, dict):
                errors.append(
                    f"{path}.Value.attachmentsByRange[{range_key!r}] "
                    "must contain a dictionary attachment"
                )

        placeholder_positions = {
            index
            for index, character in enumerate(string)
            if character == OBJECT_REPLACEMENT_CHARACTER
        }
        missing = sorted(placeholder_positions - covered_positions)
        if missing:
            errors.append(
                f"{path}.Value.attachmentsByRange is missing U+FFFC "
                f"positions {missing}"
            )
        extra = sorted(covered_positions - placeholder_positions)
        if extra:
            errors.append(
                f"{path}.Value.attachmentsByRange contains non-token "
                f"positions {extra}"
            )
    return errors


def validate_action_parameters(
    identifier: str, params: dict[str, Any], action_index: int
) -> list[str]:
    errors = []
    if identifier == "is.workflow.actions.list":
        if not isinstance(params.get("WFItems"), list):
            errors.append(f"actions[{action_index}].params.WFItems must be a list")
    elif identifier == "is.workflow.actions.choosefromlist":
        if not isinstance(params.get("WFInput"), dict):
            errors.append(
                f"actions[{action_index}].params.WFInput is required for choosefromlist"
            )
    elif identifier == "is.workflow.actions.showwebpage":
        if not isinstance(params.get("WFURL"), dict):
            errors.append(
                f"actions[{action_index}].params.WFURL is required for showwebpage"
            )
    elif identifier == "is.workflow.actions.setclipboard":
        if not isinstance(params.get("WFInput"), dict):
            errors.append(
                f"actions[{action_index}].params.WFInput is required for setclipboard"
            )
    return errors


def validate_action(
    action: Any, action_index: int, control_groups: dict[str, list[tuple[int, int]]]
) -> list[str]:
    errors = []
    if not isinstance(action, dict):
        return [f"actions[{action_index}] must be a dictionary"]

    identifier = action.get("WFWorkflowActionIdentifier")
    params = action.get("WFWorkflowActionParameters")
    if not isinstance(identifier, str) or not identifier:
        errors.append(
            f"actions[{action_index}].WFWorkflowActionIdentifier must be a string"
        )
    if not isinstance(params, dict):
        errors.append(
            f"actions[{action_index}].WFWorkflowActionParameters must be a dictionary"
        )
        return errors

    errors.extend(validate_uuid_fields(params, action_index))
    errors.extend(validate_token_strings(params, action_index))
    if isinstance(identifier, str):
        errors.extend(validate_action_parameters(identifier, params, action_index))

    if "WFControlFlowMode" in params and type(
        params["WFControlFlowMode"]
    ) is not int:
        errors.append(f"actions[{action_index}].WFControlFlowMode must be an integer")

    if identifier == "is.workflow.actions.deletephotos" and "WFInput" in params:
        errors.append(
            "actions[{0}] deletephotos uses 'photos', not 'WFInput'".format(
                action_index
            )
        )

    if identifier in CONTROL_FLOW_IDENTIFIERS:
        grouping_identifier = params.get("GroupingIdentifier")
        mode = params.get("WFControlFlowMode")
        if not isinstance(grouping_identifier, str):
            errors.append(
                f"actions[{action_index}].GroupingIdentifier is required for control flow"
            )
        elif isinstance(mode, int):
            control_groups.setdefault(grouping_identifier, []).append(
                (action_index, mode)
            )
        if mode not in {0, 1, 2}:
            errors.append(
                f"actions[{action_index}].WFControlFlowMode must be 0, 1, or 2"
            )

    return errors


def validate_control_groups(
    control_groups: dict[str, list[tuple[int, int]]]
) -> list[str]:
    errors = []
    for grouping_identifier, entries in control_groups.items():
        modes = [mode for _, mode in entries]
        positions = [index for index, _ in entries]
        if modes.count(0) != 1:
            errors.append(
                f"GroupingIdentifier {grouping_identifier} must have exactly one start mode"
            )
        if modes.count(2) != 1:
            errors.append(
                f"GroupingIdentifier {grouping_identifier} must have exactly one end mode"
            )
        if 0 in modes and 2 in modes:
            start_index = entries[modes.index(0)][0]
            end_index = entries[modes.index(2)][0]
            if start_index >= end_index:
                errors.append(
                    f"GroupingIdentifier {grouping_identifier} end must come after start"
                )
            for action_index, mode in entries:
                if mode == 1 and not (start_index < action_index < end_index):
                    errors.append(
                        f"GroupingIdentifier {grouping_identifier} middle mode at actions[{action_index}] must be inside the block"
                    )
        if positions != sorted(positions):
            errors.append(
                f"GroupingIdentifier {grouping_identifier} entries are out of action order"
            )
    return errors


def validate_workflow(workflow: Any) -> list[str]:
    errors = []
    if not isinstance(workflow, dict):
        return ["root plist must be a dictionary"]

    actions = workflow.get("WFWorkflowActions")
    if not isinstance(actions, list):
        errors.append("WFWorkflowActions must be an array")
        actions = []

    for key in (
        "WFWorkflowClientVersion",
        "WFWorkflowMinimumClientVersion",
        "WFWorkflowMinimumClientVersionString",
        "WFWorkflowIcon",
    ):
        if key not in workflow:
            errors.append(f"{key} is required")

    control_groups: dict[str, list[tuple[int, int]]] = {}
    for index, action in enumerate(actions):
        errors.extend(validate_action(action, index, control_groups))
    errors.extend(validate_control_groups(control_groups))
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate common Apple Shortcuts plist mistakes."
    )
    parser.add_argument("shortcut", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        workflow = load_plist(args.shortcut)
        errors = validate_workflow(workflow)
    except (OSError, ValueError, plistlib.InvalidFileException) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"{args.shortcut} looks valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
