#!/usr/bin/env python3
"""Focused tests for the Backstage Expert workspace-kit publisher."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("install_workspace_kit.py")
SPEC = importlib.util.spec_from_file_location("backstage_workspace_kit", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
KIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = KIT
SPEC.loader.exec_module(KIT)


class BackstageWorkspaceKitTests(unittest.TestCase):
    def make_target(self) -> tempfile.TemporaryDirectory[str]:
        return tempfile.TemporaryDirectory(dir=Path(__file__).parent)

    def test_profiles_publish_only_retained_prompts(self) -> None:
        expected = (
            "backstage-assess.prompt.md",
            "create-mcp-server.prompt.md",
            "deploy-platform.prompt.md",
            "diagram-architecture.prompt.md",
        )
        self.assertEqual(KIT.PROFILE_FILES["adopter"]["prompts"], expected)
        self.assertEqual(KIT.PROFILE_FILES["core"]["prompts"], expected)

    def test_retired_hook_option_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "no longer bundled"):
            KIT.source_items("adopter", True)

    def test_dry_run_does_not_write(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "adopter", False, {})
            self.assertTrue(plan)
            self.assertTrue(all(entry.status == "create" for entry in plan))
            self.assertFalse((target / ".github").exists())

    def test_apply_is_idempotent_and_tracks_only_created_files(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "core", False, {})
            KIT.apply_install(target, "core", False, {}, plan)
            state = KIT.load_state(target)

            self.assertEqual(state["profile"], "core")
            self.assertTrue(state["managed"])
            second = KIT.build_install_plan(target, "core", False, state)
            self.assertTrue(all(entry.status == "unchanged" for entry in second))

    def test_identical_unmanaged_file_is_not_adopted(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            item = KIT.source_items("core", False)[0]
            destination = KIT.safe_destination(target, item.relative_destination)
            destination.parent.mkdir(parents=True)
            destination.write_bytes(item.source.read_bytes())

            plan = KIT.build_install_plan(target, "core", False, {})
            entry = next(
                entry
                for entry in plan
                if entry.destination == item.relative_destination
            )
            self.assertEqual(entry.status, "unmanaged-identical")
            KIT.apply_install(target, "core", False, {}, plan)
            state = KIT.load_state(target)
            self.assertNotIn(item.relative_destination, state["managed"])

    def test_conflict_blocks_apply(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            item = KIT.source_items("core", False)[0]
            destination = KIT.safe_destination(target, item.relative_destination)
            destination.parent.mkdir(parents=True)
            destination.write_text("user content\n", encoding="utf-8")

            plan = KIT.build_install_plan(target, "core", False, {})
            self.assertIn("conflict", {entry.status for entry in plan})
            with self.assertRaisesRegex(ValueError, "conflicts"):
                KIT.apply_install(target, "core", False, {}, plan)
            self.assertFalse(KIT.state_path(target).exists())

    def test_uninstall_preserves_modified_managed_file(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "core", False, {})
            KIT.apply_install(target, "core", False, {}, plan)
            state = KIT.load_state(target)
            relative = next(iter(state["managed"]))
            destination = KIT.safe_destination(target, relative)
            destination.write_text("user changed this file\n", encoding="utf-8")

            uninstall = KIT.build_uninstall_plan(target, state)
            KIT.apply_uninstall(target, state, uninstall)
            remaining = KIT.load_state(target)
            self.assertTrue(destination.exists())
            self.assertIn(relative, remaining["managed"])

    def test_profile_switch_requires_uninstall(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            state = {
                "version": 1,
                "plugin": "backstage-expert",
                "profile": "core",
                "includeHook": False,
                "managed": {},
            }
            with self.assertRaisesRegex(ValueError, "different profile"):
                KIT.build_install_plan(target, "adopter", False, state)

    def test_state_is_valid_json_and_never_targets_protected_files(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "adopter", False, {})
            KIT.apply_install(target, "adopter", False, {}, plan)
            state = json.loads(KIT.state_path(target).read_text(encoding="utf-8"))
            self.assertEqual(state["version"], 1)
            self.assertNotIn("AGENTS.md", state["managed"])
            self.assertNotIn(".github/copilot-instructions.md", state["managed"])


if __name__ == "__main__":
    unittest.main()
