#!/usr/bin/env python3
"""Focused tests for the Open Horizons workspace-kit publisher."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("install_workspace_kit.py")
SPEC = importlib.util.spec_from_file_location(
    "open_horizons_workspace_kit",
    SCRIPT,
)
assert SPEC is not None and SPEC.loader is not None
KIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = KIT
SPEC.loader.exec_module(KIT)


class OpenHorizonsWorkspaceKitTests(unittest.TestCase):
    def make_target(self) -> tempfile.TemporaryDirectory[str]:
        return tempfile.TemporaryDirectory(dir=Path(__file__).parent)

    def test_aeg_profile_has_named_assets_without_mcp_endpoint(self) -> None:
        destinations = {
            item.relative_destination for item in KIT.source_items("aeg")
        }
        expected = {
            ".github/agents/open-horizons-aeg-concierge.agent.md",
            (
                ".github/skills/open-horizons-backstage-aeg-feature/"
                "SKILL.md"
            ),
            ".github/prompts/open-horizons-aeg-start.prompt.md",
            ".github/hooks/open-horizons-safety.json",
        }
        self.assertTrue(expected.issubset(destinations))
        self.assertNotIn(".github/mcp.json", destinations)

    def test_dry_run_does_not_write(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "aeg", {})
            self.assertTrue(plan)
            self.assertTrue(all(entry.status == "create" for entry in plan))
            self.assertFalse((target / ".github").exists())

    def test_apply_is_idempotent(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "aeg", {})
            KIT.apply_install(target, "aeg", {}, plan)
            state = KIT.load_state(target)
            second = KIT.build_install_plan(target, "aeg", state)
            self.assertTrue(
                all(entry.status == "unchanged" for entry in second)
            )

    def test_conflict_blocks_all_writes(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            item = KIT.source_items("aeg")[0]
            destination = KIT.safe_destination(
                target,
                item.relative_destination,
            )
            destination.parent.mkdir(parents=True)
            destination.write_text("user content\n", encoding="utf-8")
            plan = KIT.build_install_plan(target, "aeg", {})
            with self.assertRaisesRegex(ValueError, "conflicts"):
                KIT.apply_install(target, "aeg", {}, plan)
            self.assertFalse(KIT.state_path(target).exists())

    def test_uninstall_archives_unchanged_managed_file(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "aeg", {})
            KIT.apply_install(target, "aeg", {}, plan)
            state = KIT.load_state(target)
            relative = next(iter(state["managed"]))
            destination = KIT.safe_destination(target, relative)
            uninstall = KIT.build_uninstall_plan(target, state)
            KIT.apply_uninstall(target, state, uninstall)
            archive = KIT.backup_path(target, relative)
            self.assertFalse(destination.exists())
            self.assertTrue(archive.exists())

    def test_uninstall_preserves_modified_managed_file(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "aeg", {})
            KIT.apply_install(target, "aeg", {}, plan)
            state = KIT.load_state(target)
            relative = next(iter(state["managed"]))
            destination = KIT.safe_destination(target, relative)
            destination.write_text(
                "user changed this file\n",
                encoding="utf-8",
            )
            uninstall = KIT.build_uninstall_plan(target, state)
            KIT.apply_uninstall(target, state, uninstall)
            remaining = KIT.load_state(target)
            self.assertTrue(destination.exists())
            self.assertIn(relative, remaining["managed"])

    def test_profile_switch_requires_uninstall(self) -> None:
        state = {
            "version": 1,
            "package": "example",
            "profile": "aeg",
            "managed": {},
        }
        with self.assertRaisesRegex(ValueError, "different profile"):
            KIT.ensure_compatible_state(state, "core")

    def test_workspace_mcp_template_matches_package_manifest(self) -> None:
        KIT.validate_workspace_mcp_template()

    def test_state_is_valid_json(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "aeg", {})
            KIT.apply_install(target, "aeg", {}, plan)
            state = json.loads(
                KIT.state_path(target).read_text(encoding="utf-8")
            )
            self.assertEqual(state["package"], KIT.PACKAGE_NAME)
            self.assertEqual(state["profile"], "aeg")


if __name__ == "__main__":
    unittest.main()
