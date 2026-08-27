#!/usr/bin/env python3
"""Focused tests for validate_skill.py frontmatter rules."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("validate_skill.py")
SPEC = importlib.util.spec_from_file_location("validate_skill", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

BODY = """
# Demo skill

## When to invoke

- "run the demo"

## Output template

Report the result.

## Quality gate

- [ ] The result was verified.
"""


def build_skill(root: Path, name: str, frontmatter: str) -> Path:
    skill_dir = root / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\n{frontmatter}\n---\n{BODY}", encoding="utf-8")
    return skill_dir


class CompatibilityFieldTests(unittest.TestCase):
    def test_accepts_portable_compatibility_field(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = build_skill(
                Path(temp_dir),
                "demo-skill",
                "name: demo-skill\n"
                "description: Demo capability. Use when the user runs the demo.\n"
                "compatibility: Requires Python 3.11+ and network access",
            )
            errors, _ = MODULE.validate_skill(skill)
            self.assertEqual(errors, [])

    def test_rejects_compatibility_over_500_characters(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = build_skill(
                Path(temp_dir),
                "demo-skill",
                "name: demo-skill\n"
                "description: Demo capability. Use when the user runs the demo.\n"
                f"compatibility: {'a' * 501}",
            )
            errors, _ = MODULE.validate_skill(skill)
            self.assertTrue(
                any("compatibility is 501 characters" in e for e in errors),
                errors,
            )

    def test_rejects_unknown_frontmatter_key(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = build_skill(
                Path(temp_dir),
                "demo-skill",
                "name: demo-skill\n"
                "description: Demo capability. Use when the user runs the demo.\n"
                "version: 1.0.0",
            )
            errors, _ = MODULE.validate_skill(skill)
            self.assertIn("unknown frontmatter key: version", errors)


class DiscoveryMetadataTests(unittest.TestCase):
    def test_requires_when_language_in_description(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = build_skill(
                Path(temp_dir),
                "demo-skill",
                "name: demo-skill\ndescription: Demo capability.",
            )
            errors, _ = MODULE.validate_skill(skill)
            self.assertIn(
                "description must state when to use the skill", errors)

    def test_requires_name_to_match_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = build_skill(
                Path(temp_dir),
                "demo-skill",
                "name: other-skill\n"
                "description: Demo capability. Use when the user runs the demo.",
            )
            errors, _ = MODULE.validate_skill(skill)
            self.assertTrue(
                any("does not match folder" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
