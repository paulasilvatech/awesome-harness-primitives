#!/usr/bin/env python3
"""Validate a GitHub Copilot Agent Skill folder.

This validator checks the portable Agent Skills structure used by VS Code,
GitHub Copilot CLI, and GitHub Copilot cloud agent, plus the local repository
conventions for skills under .github/skills/.
"""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path
from typing import Any

REQUIRED = ("name", "description")
SUPPORTED_KEYS = {
    "name",
    "description",
    "argument-hint",
    "compatibility",
    "license",
    "user-invocable",
    "disable-model-invocation",
    "allowed-tools",
    "metadata",
    "tags",
}
FORBIDDEN_KEYS = {"context"}
SANDBOX_PATTERNS = (
    "/home/" + "cl" + "aude",
    "/mnt/" + "skills",
    "/mnt/" + "user-data",
)
NAME_RE = re.compile(r"^(?!.*--)[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
WHEN_RE = re.compile(
    r"\b(use when|use this skill when|when (?:the )?(?:user|users|asked|working|you)|for when|invoke when|trigger)\b", re.I)
REF_RE = re.compile(r"\]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def warn(warnings: list[str], message: str) -> None:
    warnings.append(message)


def parse_frontmatter(text: str, errors: list[str]) -> dict[str, Any]:
    if not text.startswith("---\n"):
        fail(errors, "SKILL.md must start with YAML frontmatter on line 1")
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        fail(errors, "SKILL.md frontmatter is not closed")
        return {}
    try:
        return parse_simple_yaml(text[4:end])
    except ValueError as exc:
        fail(errors, f"SKILL.md frontmatter is invalid: {exc}")
        return {}


def parse_simple_yaml(raw: str) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent != 0:
            raise ValueError(f"unexpected indented line: {line.strip()}")
        if ":" not in line:
            raise ValueError(f"cannot parse line: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError("empty key")
        if value in {"|", ">", "|-", ">-"}:
            fields[key], i = parse_block_scalar(lines, i + 1, indent, value)
            continue
        if value == "":
            fields[key], i = parse_nested(lines, i + 1, indent)
            continue
        fields[key] = parse_scalar(value)
        i += 1
    return fields


def parse_block_scalar(lines: list[str], i: int, parent_indent: int, marker: str) -> tuple[str, int]:
    style = marker[0]
    strip_final_newline = marker.endswith("-")
    block: list[str] = []
    content_indent: int | None = None
    while i < len(lines):
        line = lines[i]
        if line.strip():
            indent = len(line) - len(line.lstrip(" "))
            if indent <= parent_indent:
                break
            if content_indent is None:
                content_indent = indent
            block.append(line[min(content_indent, len(line)):])
        else:
            block.append("")
        i += 1
    if style == ">":
        text = fold_block(block)
    else:
        text = "\n".join(block)
    if not strip_final_newline:
        text += "\n"
    return text, i


def fold_block(block: list[str]) -> str:
    paragraphs: list[str] = []
    current: list[str] = []
    for line in block:
        if line == "":
            if current:
                paragraphs.append(" ".join(part.strip() for part in current))
                current = []
            paragraphs.append("")
        else:
            current.append(line)
    if current:
        paragraphs.append(" ".join(part.strip() for part in current))
    return "\n".join(paragraphs)


def parse_nested(lines: list[str], i: int, parent_indent: int) -> tuple[Any, int]:
    items: list[Any] | None = None
    mapping: dict[str, Any] = {}
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent <= parent_indent:
            break
        stripped = line.strip()
        if stripped.startswith("- "):
            if items is None:
                items = []
            items.append(parse_scalar(stripped[2:].strip()))
        elif ":" in stripped:
            key, value = stripped.split(":", 1)
            mapping[key.strip()] = parse_scalar(
                value.strip()) if value.strip() else {}
        else:
            raise ValueError(f"cannot parse nested line: {line}")
        i += 1
    return (items if items is not None else mapping), i


def parse_scalar(value: str) -> Any:
    value = value.split(" #", 1)[0].strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "Null", "~"}:
        return None
    if value.startswith("[") and value.endswith("]"):
        try:
            return ast.literal_eval(value)
        except Exception:
            inner = value[1:-1].strip()
            return [] if not inner else [parse_scalar(part.strip()) for part in inner.split(",")]
    if value.startswith("{") and value.endswith("}"):
        try:
            return ast.literal_eval(value)
        except Exception:
            return value
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        try:
            return ast.literal_eval(value)
        except Exception:
            return value[1:-1]
    return value


def local_refs(text: str) -> list[str]:
    refs = []
    for match in REF_RE.finditer(strip_code_fences(text)):
        ref = match.group(1).strip()
        if ref.startswith(("http://", "https://", "#", "mailto:")):
            continue
        refs.append(ref.split("#", 1)[0])
    return refs


def strip_code_fences(text: str) -> str:
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)[0]
            if fence is None:
                fence = token
                continue
            if fence == token:
                fence = None
                continue
        if fence is None:
            kept.append(line)
    return "\n".join(kept)


def validate_skill(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not path.is_dir():
        return [f"skill path is not a directory: {path}"], warnings
    skill_md = path / "SKILL.md"
    if not skill_md.is_file():
        return [f"missing SKILL.md in {path}"], warnings
    text = skill_md.read_text(encoding="utf-8")
    fields = parse_frontmatter(text, errors)
    validate_frontmatter(path.name, fields, errors)
    validate_copy_rules(text, errors, warnings)
    validate_line_count(text, errors, warnings)
    validate_references(path, text, errors)
    validate_scripts(path, errors)
    return errors, warnings


def validate_frontmatter(folder_name: str, fields: dict[str, Any], errors: list[str]) -> None:
    for key in REQUIRED:
        if key not in fields:
            fail(errors, f"missing required frontmatter key: {key}")
    name = fields.get("name", "")
    if name and not isinstance(name, str):
        fail(errors, "name must be a string")
        name = ""
    if name and name != folder_name:
        fail(errors, f"name '{name}' does not match folder '{folder_name}'")
    if name and (not (1 <= len(name) <= 64) or not NAME_RE.match(name)):
        fail(
            errors, f"name '{name}' is not lowercase hyphenated Agent Skills format")
    description = fields.get("description", "")
    if description and not isinstance(description, str):
        fail(errors, "description must be a string")
        description = ""
    if description and len(description) > 1024:
        fail(
            errors, f"description is {len(description)} characters, maximum is 1024")
    if description and not WHEN_RE.search(description):
        fail(errors, "description must state when to use the skill")
    if "allowed-tools" in fields and not valid_string_or_string_list(fields["allowed-tools"]):
        fail(errors, "allowed-tools must be a string or list of strings")
    compatibility = fields.get("compatibility")
    if compatibility is not None:
        if not isinstance(compatibility, str) or not compatibility.strip():
            fail(errors, "compatibility must be a non-empty string")
        elif len(compatibility) > 500:
            fail(
                errors, f"compatibility is {len(compatibility)} characters, maximum is 500")
    if "metadata" in fields and not isinstance(fields["metadata"], dict):
        fail(errors, "metadata must be a map")
    if "tags" in fields and not valid_string_or_string_list(fields["tags"]):
        fail(errors, "tags must be a string or list of strings")
    for key in ("user-invocable", "disable-model-invocation"):
        if key in fields and not isinstance(fields[key], bool):
            fail(errors, f"{key} must be boolean")
    for key in fields:
        if key in FORBIDDEN_KEYS:
            fail(errors, f"unsupported frontmatter key: {key}")
        elif key not in SUPPORTED_KEYS:
            fail(errors, f"unknown frontmatter key: {key}")


def valid_string_or_string_list(value: Any) -> bool:
    return isinstance(value, str) or (isinstance(value, list) and all(isinstance(item, str) for item in value))


def validate_copy_rules(text: str, errors: list[str], warnings: list[str]) -> None:
    for pattern in SANDBOX_PATTERNS:
        if pattern in text:
            fail(errors, f"sandbox path leak found: {pattern}")
    if re.search(r"(?<!GitHub )\bCopilot\b", text) and "GitHub Copilot" not in text:
        warn(warnings, "bare 'Copilot' found without 'GitHub Copilot'")


def validate_line_count(text: str, errors: list[str], warnings: list[str]) -> None:
    lines = len(text.splitlines())
    if lines > 500:
        fail(errors, f"SKILL.md is {lines} lines, maximum is 500")
    elif lines > 200:
        warn(
            warnings, f"SKILL.md is {lines} lines; consider moving detail into bundled resources")


def validate_references(path: Path, text: str, errors: list[str]) -> None:
    for ref in local_refs(text):
        target = (path / ref).resolve()
        try:
            target.relative_to(path.resolve())
        except ValueError:
            fail(errors, f"local reference escapes skill folder: {ref}")
            continue
        if not target.exists():
            fail(errors, f"dangling local reference: {ref}")


def validate_scripts(path: Path, errors: list[str]) -> None:
    scripts_dir = path / "scripts"
    if not scripts_dir.is_dir():
        return
    for script in scripts_dir.glob("*.py"):
        source = script.read_text(encoding="utf-8")
        try:
            compile(source, str(script), "exec")
        except SyntaxError as exc:
            fail(
                errors, f"script does not compile: {script.relative_to(path)} ({exc})")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a GitHub Copilot Agent Skill folder")
    parser.add_argument("skill", help="Path to the skill folder")
    args = parser.parse_args()
    errors, warnings = validate_skill(Path(args.skill))
    if errors:
        print(f"FAIL {args.skill}")
        for error in errors:
            print(f"  - {error}")
        return 1
    for warning in warnings:
        print(f"WARN {args.skill}: {warning}")
    print(f"OK {args.skill}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
