#!/usr/bin/env python3
"""Focused tests for the Open Horizons workspace-kit publisher."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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

    def test_mid_commit_failure_rolls_back_files_and_state(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            original_state = {
                "version": 1,
                "package": KIT.PACKAGE_NAME,
                "profile": "aeg",
                "managed": {},
            }
            state_content = (
                json.dumps(original_state, indent=2, sort_keys=True) + "\n"
            ).encode("utf-8")
            KIT.atomic_write(KIT.state_path(target), state_content)
            plan = KIT.build_install_plan(target, "aeg", original_state)
            original_install = KIT.install_staged_file
            calls = 0

            def fail_second_install(staged: Path, destination: Path) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected commit failure")
                original_install(staged, destination)

            with mock.patch.object(
                KIT,
                "install_staged_file",
                side_effect=fail_second_install,
            ):
                with self.assertRaisesRegex(RuntimeError, "rolled back"):
                    KIT.apply_install(target, "aeg", original_state, plan)

            for entry in plan:
                if entry.status == "create":
                    destination = KIT.safe_destination(
                        target,
                        entry.destination,
                    )
                    self.assertFalse(
                        destination.exists()
                    )
            current_state = KIT.state_path(target).read_bytes()
            self.assertEqual(current_state, state_content)

    def test_upgrade_archives_unchanged_retired_destination(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "aeg", {})
            KIT.apply_install(target, "aeg", {}, plan)
            state = KIT.load_state(target)
            relative = (
                ".github/skills/backstage-authentication/SKILL.md"
            )
            destination = KIT.safe_destination(target, relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            content = b"legacy managed skill\n"
            destination.write_bytes(content)
            state["managed"][relative] = KIT.digest_bytes(content)
            KIT.atomic_write(
                KIT.state_path(target),
                (
                    json.dumps(state, indent=2, sort_keys=True) + "\n"
                ).encode("utf-8"),
            )

            upgrade = KIT.build_install_plan(target, "aeg", state)
            retired = next(
                entry for entry in upgrade
                if entry.destination == relative
            )
            self.assertEqual(retired.status, "retired-archive")
            KIT.apply_install(target, "aeg", state, upgrade)

            self.assertFalse(destination.exists())
            self.assertTrue(KIT.backup_path(target, relative).exists())
            self.assertNotIn(relative, KIT.load_state(target)["managed"])

    def test_upgrade_preserves_modified_retired_destination(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "aeg", {})
            KIT.apply_install(target, "aeg", {}, plan)
            state = KIT.load_state(target)
            relative = (
                ".github/skills/backstage-authentication/SKILL.md"
            )
            destination = KIT.safe_destination(target, relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text("user-modified skill\n", encoding="utf-8")
            state["managed"][relative] = KIT.digest_bytes(
                b"original managed skill\n"
            )
            KIT.atomic_write(
                KIT.state_path(target),
                (
                    json.dumps(state, indent=2, sort_keys=True) + "\n"
                ).encode("utf-8"),
            )

            upgrade = KIT.build_install_plan(target, "aeg", state)
            retired = next(
                entry for entry in upgrade
                if entry.destination == relative
            )
            self.assertEqual(
                retired.status,
                "retired-modified-preserve",
            )
            KIT.apply_install(target, "aeg", state, upgrade)

            self.assertTrue(destination.exists())
            self.assertIn(relative, KIT.load_state(target)["managed"])

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

    def test_automation_omits_target_specific_validation(self) -> None:
        destinations = {
            item.relative_destination
            for item in KIT.source_items("automation")
        }
        self.assertNotIn(
            ".github/workflows/validate-agents.yml",
            destinations,
        )

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
