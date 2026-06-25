#!/usr/bin/env python3
"""Validate PatX user skill import package content using only the Python standard library."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "patx-user-skill-import-v1"
MAX_SKILL_KEY = 128
MAX_NAME = 100
MAX_TEXT = 20000
MAX_SKILLS = 100
MAX_ITEMS_PER_SKILL = 200
MAX_TREE_DEPTH = 2
MAX_TAGS = 20
MAX_TAG = 30


class ValidationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def require_object(value: Any, path: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{path} must be an object")
    return value


def require_array(value: Any, path: str) -> list[Any]:
    require(isinstance(value, list), f"{path} must be an array")
    return value


def require_text(value: Any, path: str, max_length: int, *, allow_empty: bool = False) -> str:
    require(isinstance(value, str), f"{path} must be a string")
    if allow_empty:
        require(len(value) <= max_length, f"{path} exceeds max length {max_length}")
    else:
        require(value.strip() != "", f"{path} is required")
        require(len(value) <= max_length, f"{path} exceeds max length {max_length}")
    return value


def reject_extra_keys(obj: dict[str, Any], allowed: set[str], path: str) -> None:
    extra = sorted(set(obj) - allowed)
    require(not extra, f"{path} has unsupported fields: {', '.join(extra)}")


def validate_item_shape(item: Any, path: str) -> dict[str, Any]:
    item_obj = require_object(item, path)
    allowed = {"node_key", "parent_node_key", "item_type", "name", "content", "order"}
    reject_extra_keys(item_obj, allowed, path)
    for key in allowed:
        require(key in item_obj, f"{path}.{key} is required")

    require_text(item_obj["node_key"], f"{path}.node_key", MAX_SKILL_KEY)
    parent = item_obj["parent_node_key"]
    require(parent is None or isinstance(parent, str), f"{path}.parent_node_key must be string or null")
    if isinstance(parent, str):
        require(parent.strip() != "", f"{path}.parent_node_key cannot be empty")
        require(len(parent) <= MAX_SKILL_KEY, f"{path}.parent_node_key exceeds max length {MAX_SKILL_KEY}")

    require(item_obj["item_type"] in {"folder", "content"}, f"{path}.item_type must be folder or content")
    require_text(item_obj["name"], f"{path}.name", MAX_NAME)
    content = item_obj["content"]
    require(content is None or isinstance(content, str), f"{path}.content must be string or null")
    if isinstance(content, str):
        require(len(content) <= MAX_TEXT, f"{path}.content exceeds max length {MAX_TEXT}")
    require(isinstance(item_obj["order"], int) and not isinstance(item_obj["order"], bool), f"{path}.order must be an integer")
    require(item_obj["order"] >= 0, f"{path}.order must be >= 0")
    return item_obj


def validate_skill(skill: Any, index: int) -> tuple[str, str]:
    path = f"skills[{index}]"
    skill_obj = require_object(skill, path)
    allowed = {"skill_key", "name", "description", "tags", "readme_content", "items"}
    reject_extra_keys(skill_obj, allowed, path)
    for key in allowed:
        require(key in skill_obj, f"{path}.{key} is required")

    skill_key = require_text(skill_obj["skill_key"], f"{path}.skill_key", MAX_SKILL_KEY)
    name = require_text(skill_obj["name"], f"{path}.name", MAX_NAME)
    require_text(skill_obj["description"], f"{path}.description", MAX_TEXT)
    require_text(skill_obj["readme_content"], f"{path}.readme_content", MAX_TEXT)

    tags = require_array(skill_obj["tags"], f"{path}.tags")
    require(len(tags) <= MAX_TAGS, f"{path}.tags exceeds max items {MAX_TAGS}")
    for tag_index, tag in enumerate(tags):
        require_text(tag, f"{path}.tags[{tag_index}]", MAX_TAG)

    items = require_array(skill_obj["items"], f"{path}.items")
    require(items, f"{path}.items must not be empty")
    require(
        len(items) <= MAX_ITEMS_PER_SKILL,
        f"{path}.items exceeds max items {MAX_ITEMS_PER_SKILL}",
    )

    item_objs = [validate_item_shape(item, f"{path}.items[{item_index}]") for item_index, item in enumerate(items)]
    node_keys: set[str] = set()
    item_by_key: dict[str, dict[str, Any]] = {}
    content_count = 0

    for item_obj in item_objs:
        node_key = item_obj["node_key"]
        require(node_key not in node_keys, f"{path}.items has duplicate node_key: {node_key}")
        node_keys.add(node_key)
        item_by_key[node_key] = item_obj
        if item_obj["item_type"] == "content":
            content_count += 1
            require(isinstance(item_obj["content"], str) and item_obj["content"].strip() != "", f"{path}.items[{node_key}].content is required for content item")

    require(content_count > 0, f"{path}.items must include at least one content node")

    for item_obj in item_objs:
        node_key = item_obj["node_key"]
        parent_key = item_obj["parent_node_key"]

        if item_obj["item_type"] == "folder":
            require(
                parent_key is None,
                f"{path}.items[{node_key}] is a folder and must be top-level",
            )
            continue

        if parent_key is None:
            continue

        parent = item_by_key.get(parent_key)
        require(parent is not None, f"{path}.items[{node_key}].parent_node_key does not exist: {parent_key}")
        require(parent["item_type"] == "folder", f"{path}.items[{node_key}].parent_node_key must point to a folder: {parent_key}")
        require(
            parent["parent_node_key"] is None,
            f"{path}.items[{node_key}].parent_node_key must point to a top-level folder: {parent_key}",
        )

    return skill_key, name


def validate(data: Any) -> None:
    root = require_object(data, "root")
    reject_extra_keys(root, {"schema_version", "skills"}, "root")
    require(root.get("schema_version") == SCHEMA_VERSION, "root.schema_version must be patx-user-skill-import-v1")
    skills = require_array(root.get("skills"), "root.skills")
    require(skills, "root.skills must not be empty")
    require(len(skills) <= MAX_SKILLS, f"root.skills exceeds max items {MAX_SKILLS}")

    skill_keys: set[str] = set()
    names: set[str] = set()
    for index, skill in enumerate(skills):
        skill_key, name = validate_skill(skill, index)
        require(skill_key not in skill_keys, f"root.skills has duplicate skill_key: {skill_key}")
        require(name not in names, f"root.skills has duplicate name: {name}")
        skill_keys.add(skill_key)
        names.add(name)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("INVALID: usage: validate_import_json.py <patx-path>")
        return 2

    try:
        with Path(argv[1]).open("r", encoding="utf-8-sig") as handle:
            data = json.load(handle)
        validate(data)
    except Exception as exc:  # noqa: BLE001 - concise CLI diagnostics
        print(f"INVALID: {exc}")
        return 1

    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
