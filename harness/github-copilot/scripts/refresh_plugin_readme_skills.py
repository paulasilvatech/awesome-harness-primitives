#!/usr/bin/env python3
"""Refresh the skill table in a plugin README from canonical skill sources.

Rewrites only the rows of the existing skill/command table so the README lists
every skill the plugin actually distributes. Other sections are left untouched.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from _layout import HARNESS_ROOT
except ModuleNotFoundError:  # pragma: no cover
    from ._layout import HARNESS_ROOT

SOURCES = HARNESS_ROOT / "manifests" / "plugin-sources.json"
SKILLS = HARNESS_ROOT / "skills"
PLUGINS = HARNESS_ROOT / "plugins"


def description(skill: str) -> str:
    text = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
    body = text.split("---", 2)[1]
    match = re.search(r"^description:\s*(.*)$", body, re.M)
    if not match:
        return ""
    value = match.group(1).strip()
    if value in {">-", ">", "|", "|-"}:
        lines = body.split("description:", 1)[1].splitlines()[1:]
        collected = []
        for line in lines:
            if line.strip() and not line.startswith(" "):
                break
            collected.append(line.strip())
        value = " ".join(part for part in collected if part)
    value = value.strip().strip('"').strip("'")
    # keep the capability half; the trigger half stays in SKILL.md
    value = re.split(r"\.\s+Use (?:this skill |it )?when", value)[0]
    return value.rstrip(".") + "."


def rows(plugin: str, label: str) -> list[str]:
    config = json.loads(SOURCES.read_text(encoding="utf-8"))["plugins"][plugin]
    refs = list(config.get("skills", [])) + \
        list(config.get("sharedSkills", []))
    names = sorted({Path(ref.rstrip("/")).name for ref in refs})
    if label == "command":
        return [f"| `/{plugin}:{n}` | {description(n)} |" for n in names]
    return [f"| `{n}` | {description(n)} |" for n in names]


def refresh(plugin: str) -> bool:
    readme = PLUGINS / plugin / "README.md"
    lines = readme.read_text(encoding="utf-8").splitlines()
    start = next((i for i, l in enumerate(lines)
                  if l.startswith(("|---", "|-------"))), None)
    if start is None:
        raise SystemExit(f"{plugin}: no table found in README")
    header = lines[start - 1]
    label = "command" if "Command" in header else "skill"
    end = start + 1
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    updated = lines[:start + 1] + rows(plugin, label) + lines[end:]
    text = "\n".join(updated) + "\n"
    if text != readme.read_text(encoding="utf-8"):
        readme.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugins", nargs="+")
    args = parser.parse_args()
    for plugin in args.plugins:
        changed = refresh(plugin)
        print(f"{'updated' if changed else 'unchanged'} {plugin}/README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
