#!/usr/bin/env python3
"""Generate a dictionary-driven localized Shortcuts menu spec."""

from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path
from typing import Any


NAMESPACE = uuid.UUID("687BF302-80F5-4E61-92B3-0A92CCDB9226")
OBJECT_REPLACEMENT_CHARACTER = "\ufffc"


def stable_uuid(seed: str) -> str:
    return str(uuid.uuid5(NAMESPACE, seed)).upper()


def output_attachment(action_uuid: str, output_name: str) -> dict[str, Any]:
    return {
        "Value": {
            "Type": "ActionOutput",
            "OutputUUID": action_uuid,
            "OutputName": output_name,
        },
        "WFSerializationType": "WFTextTokenAttachment",
    }


def variable_attachment(name: str) -> dict[str, Any]:
    return {
        "Value": {"Type": "Variable", "VariableName": name},
        "WFSerializationType": "WFTextTokenAttachment",
    }


def variable_token(name: str) -> dict[str, Any]:
    return {
        "Value": {
            "string": OBJECT_REPLACEMENT_CHARACTER,
            "attachmentsByRange": {
                "{0, 1}": {"Type": "Variable", "VariableName": name}
            },
        },
        "WFSerializationType": "WFTextTokenString",
    }


def dictionary_items(values: dict[str, str]) -> dict[str, Any]:
    items = []
    for key, value in values.items():
        items.append(
            {
                "WFItemType": 0,
                "WFKey": {
                    "Value": {"string": key},
                    "WFSerializationType": "WFTextTokenString",
                },
                "WFValue": {
                    "Value": {"string": value},
                    "WFSerializationType": "WFTextTokenString",
                },
            }
        )
    return {
        "Value": {"WFDictionaryFieldValueItems": items},
        "WFSerializationType": "WFDictionaryFieldValue",
    }


def action(identifier: str, params: dict[str, Any]) -> dict[str, Any]:
    return {"id": identifier, "params": params}


def dictionary_actions(
    locale: str, values: dict[str, str], seed_prefix: str
) -> list[dict[str, Any]]:
    dictionary_uuid = stable_uuid(f"{seed_prefix}:dictionary:{locale}")
    return [
        action(
            "is.workflow.actions.dictionary",
            {
                "UUID": dictionary_uuid,
                "WFItems": dictionary_items(values),
            },
        ),
        action(
            "is.workflow.actions.setvariable",
            {
                "WFInput": output_attachment(dictionary_uuid, "Dictionary"),
                "WFVariableName": "ui",
            },
        ),
    ]


def validate_locales(
    locales: Any, default_locale: str, required_keys: list[str]
) -> dict[str, dict[str, str]]:
    if not isinstance(locales, dict) or not locales:
        raise ValueError("locales JSON must be a non-empty object")
    if default_locale not in locales:
        raise ValueError(f"default locale {default_locale!r} is missing")

    normalized: dict[str, dict[str, str]] = {}
    canonical_keys: set[str] | None = None
    for locale, values in locales.items():
        if not isinstance(locale, str) or not isinstance(values, dict):
            raise ValueError("each locale must map to an object")
        if not all(isinstance(key, str) and isinstance(value, str) for key, value in values.items()):
            raise ValueError(f"locale {locale!r} keys and values must be strings")
        keys = set(values)
        if canonical_keys is None:
            canonical_keys = keys
        elif keys != canonical_keys:
            missing = sorted(canonical_keys - keys)
            extra = sorted(keys - canonical_keys)
            raise ValueError(
                f"locale {locale!r} key mismatch; missing={missing}, extra={extra}"
            )
        normalized[locale] = values

    missing_required = sorted(set(required_keys) - set(normalized[default_locale]))
    if missing_required:
        raise ValueError(
            f"default locale is missing required keys: {', '.join(missing_required)}"
        )
    return normalized


def build_spec(
    locales: dict[str, dict[str, str]],
    default_locale: str,
    language_variable: str,
    prompt_key: str,
    menu_keys: list[str],
    name: str,
) -> dict[str, Any]:
    seed_prefix = f"{name}:{language_variable}:{prompt_key}:{','.join(menu_keys)}"
    actions: list[dict[str, Any]] = []
    actions.extend(
        dictionary_actions(default_locale, locales[default_locale], seed_prefix)
    )

    for locale, values in locales.items():
        if locale == default_locale:
            continue
        grouping_identifier = stable_uuid(f"{seed_prefix}:locale-if:{locale}")
        actions.append(
            action(
                "is.workflow.actions.conditional",
                {
                    "UUID": stable_uuid(f"{seed_prefix}:locale-if-start:{locale}"),
                    "GroupingIdentifier": grouping_identifier,
                    "WFCondition": 99,
                    "WFControlFlowMode": 0,
                    "WFConditionalActionString": locale,
                    "WFInput": {
                        "Type": "Variable",
                        "Variable": variable_attachment(language_variable),
                    },
                },
            )
        )
        actions.extend(dictionary_actions(locale, values, seed_prefix))
        actions.append(
            action(
                "is.workflow.actions.conditional",
                {
                    "UUID": stable_uuid(f"{seed_prefix}:locale-if-end:{locale}"),
                    "GroupingIdentifier": grouping_identifier,
                    "WFControlFlowMode": 2,
                },
            )
        )

    for key in [prompt_key, *menu_keys]:
        get_uuid = stable_uuid(f"{seed_prefix}:get:{key}")
        actions.append(
            action(
                "is.workflow.actions.getvalueforkey",
                {
                    "UUID": get_uuid,
                    "CustomOutputName": key,
                    "WFDictionaryKey": key,
                    "WFInput": variable_attachment("ui"),
                },
            )
        )
        actions.append(
            action(
                "is.workflow.actions.setvariable",
                {
                    "WFInput": output_attachment(get_uuid, key),
                    "WFVariableName": f"ui_{key}",
                },
            )
        )

    list_uuid = stable_uuid(f"{seed_prefix}:menu-list")
    actions.append(
        action(
            "is.workflow.actions.list",
            {
                "UUID": list_uuid,
                "WFItems": [variable_token(f"ui_{key}") for key in menu_keys],
            },
        )
    )
    choose_uuid = stable_uuid(f"{seed_prefix}:choose")
    actions.append(
        action(
            "is.workflow.actions.choosefromlist",
            {
                "UUID": choose_uuid,
                "WFChooseFromListActionPrompt": variable_token(
                    f"ui_{prompt_key}"
                ),
                "WFInput": output_attachment(list_uuid, "List"),
            },
        )
    )
    actions.append(
        action(
            "is.workflow.actions.setvariable",
            {
                "WFInput": output_attachment(choose_uuid, "Chosen Item"),
                "WFVariableName": "selectedMenuItem",
            },
        )
    )

    return {
        "name": name,
        "actions": actions,
        "localization": {
            "default_locale": default_locale,
            "language_variable": language_variable,
            "prompt_key": prompt_key,
            "menu_keys": menu_keys,
            "selected_variable": "selectedMenuItem",
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate locale dictionaries and generate a compact JSON spec "
            "for a dictionary-driven dynamic Shortcuts menu."
        )
    )
    parser.add_argument("locales", type=Path)
    parser.add_argument("--default-locale", required=True)
    parser.add_argument("--language-variable", default="displayLanguage")
    parser.add_argument("--prompt-key", required=True)
    parser.add_argument("--menu-key", action="append", required=True)
    parser.add_argument("--name", default="Localized Menu")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        source = json.loads(args.locales.read_text(encoding="utf-8"))
        required_keys = [args.prompt_key, *args.menu_key]
        locales = validate_locales(source, args.default_locale, required_keys)
        spec = build_spec(
            locales,
            args.default_locale,
            args.language_variable,
            args.prompt_key,
            args.menu_key,
            args.name,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"error: {error}") from error

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
