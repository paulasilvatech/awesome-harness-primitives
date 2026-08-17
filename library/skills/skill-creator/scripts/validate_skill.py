#!/usr/bin/env python3
"""Validate a GitHub Copilot Agent Skill folder.

This validator checks the portable Agent Skills structure used by VS Code,
GitHub Copilot CLI, and GitHub Copilot cloud agent, plus the local repository
conventions for skills under .github/skills/.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED = ("name", "description")
SUPPORTED_KEYS = {
    "name",
    "description",
    "argument-hint",
    "license",
    "user-invocable",
    "disable-model-invocation",
    "context",
}
FORBIDDEN_KEYS = {"allowed-tools"}
SANDBOX_PATTERNS = (
    "/home/" + "cl" + "aude",
    "/mnt/" + "skills",
    "/mnt/" + "user-data",
)
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
REF_RE = re.compile(r"\]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(text: str, errors: list[str]) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail(errors, "SKILL.md must start with YAML frontmatter on line 1")
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        fail(errors, "SKILL.md frontmatter is not closed")
        return {}
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith("  "):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def local_refs(text: str) -> list[str]:
    refs = []
    for match in REF_RE.finditer(text):
        ref = match.group(1).strip()
        if ref.startswith(("http://", "https://", "#", "mailto:")):
            continue
        refs.append(ref.split("#", 1)[0])
    return refs


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_dir():
        return [f"skill path is not a directory: {path}"]
    skill_md = path / "SKILL.md"
    if not skill_md.is_file():
        return [f"missing SKILL.md in {path}"]
    text = skill_md.read_text(encoding="utf-8")
    fields = parse_frontmatter(text, errors)
    validate_frontmatter(path.name, fields, errors)
    validate_copy_rules(text, errors)
    validate_references(path, text, errors)
    validate_scripts(path, errors)
    return errors


def validate_frontmatter(folder_name: str, fields: dict[str, str], errors: list[str]) -> None:
    for key in REQUIRED:
        if key not in fields:
            fail(errors, f"missing required frontmatter key: {key}")
    name = fields.get("name", "")
    if name and name != folder_name:
        fail(errors, f"name '{name}' does not match folder '{folder_name}'")
    if name and not NAME_RE.match(name):
        fail(errors, f"name '{name}' is not lowercase hyphenated Agent Skills format")
    description = fields.get("description", "")
    if description and len(description) > 1024:
        fail(errors, f"description is {len(description)} characters, maximum is 1024")
    for key in fields:
        if key in FORBIDDEN_KEYS:
            fail(errors, f"unsupported frontmatter key: {key}")
        elif key not in SUPPORTED_KEYS:
            fail(errors, f"unknown frontmatter key: {key}")


def validate_copy_rules(text: str, errors: list[str]) -> None:
    for pattern in SANDBOX_PATTERNS:
        if pattern in text:
            fail(errors, f"sandbox path leak found: {pattern}")
    if "\u2014" in text:
        fail(errors, "em dash found in SKILL.md")
    if re.search(r"(?<!GitHub )\bCopilot\b", text) and "GitHub Copilot" not in text:
        fail(errors, "bare 'Copilot' found without 'GitHub Copilot'")


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
            fail(errors, f"script does not compile: {script.relative_to(path)} ({exc})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a GitHub Copilot Agent Skill folder")
    parser.add_argument("skill", help="Path to the skill folder")
    args = parser.parse_args()
    errors = validate_skill(Path(args.skill))
    if errors:
        print(f"FAIL {args.skill}")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"OK {args.skill}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
