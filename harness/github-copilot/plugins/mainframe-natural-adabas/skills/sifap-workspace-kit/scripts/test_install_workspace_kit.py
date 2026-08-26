#!/usr/bin/env python3
"""Focused tests for the SIFAP workspace-kit publisher."""

from __future__ import annotations

import importlib.util
import json
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).with_name("install_workspace_kit.py")
SPEC = importlib.util.spec_from_file_location(
    "sifap_workspace_kit",
    SCRIPT,
)
assert SPEC is not None
assert SPEC.loader is not None
KIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = KIT
SPEC.loader.exec_module(KIT)


class SifapWorkspaceKitTests(unittest.TestCase):
    def make_target(self) -> tempfile.TemporaryDirectory[str]:
        return tempfile.TemporaryDirectory()

    def test_core_profile_has_context_without_stage_prompts(self) -> None:
        destinations = {
            item.relative_destination for item in KIT.source_items("core")
        }
        expected = {
            ".github/copilot-instructions.md",
            ".github/agents/sifap-archaeologist.agent.md",
            (
                ".github/skills/sifap-modernization-context/"
                "SKILL.md"
            ),
            (
                ".github/instructions/"
                "sifap-requirements.instructions.md"
            ),
        }
        self.assertTrue(expected.issubset(destinations))
        self.assertFalse(
            any(path.startswith(".github/prompts/") for path in destinations)
        )

    def test_dry_run_does_not_write(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "core", {})
            self.assertTrue(plan)
            self.assertTrue(all(entry.status == "create" for entry in plan))
            self.assertFalse((target / ".github").exists())

    def test_apply_is_idempotent(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "core", {})
            KIT.apply_install(target, "core", {}, plan)
            state = KIT.load_state(target)
            second = KIT.build_install_plan(target, "core", state)
            self.assertTrue(
                all(entry.status == "unchanged" for entry in second)
            )

    def test_conflict_blocks_all_writes(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            item = KIT.source_items("core")[0]
            destination = KIT.safe_destination(
                target,
                item.relative_destination,
            )
            destination.parent.mkdir(parents=True)
            destination.write_text("user content\n", encoding="utf-8")
            plan = KIT.build_install_plan(target, "core", {})
            with self.assertRaisesRegex(ValueError, "conflicts"):
                KIT.apply_install(target, "core", {}, plan)
            self.assertFalse(KIT.state_path(target).exists())

    def test_mid_commit_failure_rolls_back_files_and_state(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            original_state = {
                "version": 1,
                "package": KIT.PACKAGE_NAME,
                "profile": "core",
                "managed": {},
            }
            state_content = (
                json.dumps(original_state, indent=2, sort_keys=True) + "\n"
            ).encode("utf-8")
            KIT.atomic_write(KIT.state_path(target), state_content)
            plan = KIT.build_install_plan(target, "core", original_state)
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
                    KIT.apply_install(target, "core", original_state, plan)

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
            self.assertEqual(state_content, current_state)

    def test_upgrade_archives_unchanged_retired_destination(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "core", {})
            KIT.apply_install(target, "core", {}, plan)
            state = KIT.load_state(target)
            relative = ".github/skills/sifap-retired/SKILL.md"
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

            upgrade = KIT.build_install_plan(target, "core", state)
            retired = next(
                entry for entry in upgrade
                if entry.destination == relative
            )
            self.assertEqual("retired-archive", retired.status)
            KIT.apply_install(target, "core", state, upgrade)

            self.assertFalse(destination.exists())
            self.assertTrue(KIT.backup_path(target, relative).exists())
            self.assertNotIn(relative, KIT.load_state(target)["managed"])

    def test_upgrade_preserves_modified_retired_destination(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "core", {})
            KIT.apply_install(target, "core", {}, plan)
            state = KIT.load_state(target)
            relative = ".github/skills/sifap-retired/SKILL.md"
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

            upgrade = KIT.build_install_plan(target, "core", state)
            retired = next(
                entry for entry in upgrade
                if entry.destination == relative
            )
            self.assertEqual(
                "retired-modified-preserve",
                retired.status,
            )
            KIT.apply_install(target, "core", state, upgrade)

            self.assertTrue(destination.exists())
            self.assertIn(relative, KIT.load_state(target)["managed"])

    def test_cli_blocks_retired_backup_conflict_in_dry_run(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = [
                KIT.PlanEntry(
                    None,
                    ".github/skills/retired/SKILL.md",
                    "retired-backup-conflict",
                    "hash",
                )
            ]
            with (
                mock.patch.object(KIT, "validate_package_root"),
                mock.patch.object(KIT, "load_state", return_value={}),
                mock.patch.object(
                    KIT,
                    "build_install_plan",
                    return_value=plan,
                ),
                mock.patch.object(KIT, "print_report"),
            ):
                result = KIT.main(
                    [
                        "--target",
                        str(target),
                        "--profile",
                        "core",
                        "--allow-non-git",
                    ]
                )
            self.assertEqual(2, result)

    def test_cli_reports_transaction_failure_without_traceback(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            stderr = io.StringIO()
            with (
                mock.patch.object(KIT, "validate_package_root"),
                mock.patch.object(KIT, "load_state", return_value={}),
                mock.patch.object(
                    KIT,
                    "build_install_plan",
                    return_value=[],
                ),
                mock.patch.object(
                    KIT,
                    "apply_install",
                    side_effect=RuntimeError("transaction failed"),
                ),
                mock.patch("sys.stderr", stderr),
            ):
                result = KIT.main(
                    [
                        "--target",
                        str(target),
                        "--profile",
                        "core",
                        "--allow-non-git",
                        "--apply",
                    ]
                )
            self.assertEqual(2, result)
            self.assertIn("workspace-kit error", stderr.getvalue())
            self.assertIn("transaction failed", stderr.getvalue())

    def test_uninstall_archives_unchanged_managed_file(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "core", {})
            KIT.apply_install(target, "core", {}, plan)
            state = KIT.load_state(target)
            relative = next(iter(state["managed"]))
            destination = KIT.safe_destination(target, relative)
            uninstall = KIT.build_uninstall_plan(target, state)
            KIT.apply_uninstall(target, state, uninstall)
            archive = KIT.backup_path(target, relative)
            self.assertFalse(destination.exists())
            self.assertTrue(archive.exists())

    def test_mid_uninstall_failure_restores_files_and_state(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "core", {})
            KIT.apply_install(target, "core", {}, plan)
            state = KIT.load_state(target)
            state_content = KIT.state_path(target).read_bytes()
            uninstall = KIT.build_uninstall_plan(target, state)
            archived_entries = [
                entry for entry in uninstall if entry.status == "archive"
            ]
            self.assertGreaterEqual(len(archived_entries), 2)
            original_contents = {
                entry.destination: KIT.safe_destination(
                    target,
                    entry.destination,
                ).read_bytes()
                for entry in archived_entries
            }
            original_archive = KIT.archive_managed_file
            calls = 0

            def fail_second_archive(source: Path, destination: Path) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected uninstall failure")
                original_archive(source, destination)

            with mock.patch.object(
                KIT,
                "archive_managed_file",
                side_effect=fail_second_archive,
            ):
                with self.assertRaisesRegex(RuntimeError, "rolled back"):
                    KIT.apply_uninstall(target, state, uninstall)

            for entry in archived_entries:
                destination = KIT.safe_destination(
                    target,
                    entry.destination,
                )
                self.assertTrue(destination.exists())
                self.assertEqual(
                    original_contents[entry.destination],
                    destination.read_bytes(),
                )
                self.assertFalse(
                    KIT.backup_path(target, entry.destination).exists()
                )
            current_state = KIT.state_path(target).read_bytes()
            self.assertEqual(state_content, current_state)

    def test_partial_uninstall_state_failure_restores_everything(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "core", {})
            KIT.apply_install(target, "core", {}, plan)
            state = KIT.load_state(target)
            preserved_relative = next(iter(state["managed"]))
            preserved = KIT.safe_destination(target, preserved_relative)
            preserved.write_text("user modified\n", encoding="utf-8")
            state_content = KIT.state_path(target).read_bytes()
            uninstall = KIT.build_uninstall_plan(target, state)
            archived_entries = [
                entry for entry in uninstall if entry.status == "archive"
            ]
            original_contents = {
                entry.destination: KIT.safe_destination(
                    target,
                    entry.destination,
                ).read_bytes()
                for entry in archived_entries
            }
            original_install = KIT.install_staged_file

            def fail_state_install(staged: Path, destination: Path) -> None:
                if destination == KIT.state_path(target):
                    raise OSError("injected state commit failure")
                original_install(staged, destination)

            with mock.patch.object(
                KIT,
                "install_staged_file",
                side_effect=fail_state_install,
            ):
                with self.assertRaisesRegex(RuntimeError, "rolled back"):
                    KIT.apply_uninstall(target, state, uninstall)

            self.assertTrue(preserved.exists())
            for entry in archived_entries:
                destination = KIT.safe_destination(
                    target,
                    entry.destination,
                )
                self.assertTrue(destination.exists())
                self.assertEqual(
                    original_contents[entry.destination],
                    destination.read_bytes(),
                )
                self.assertFalse(
                    KIT.backup_path(target, entry.destination).exists()
                )
            current_state = KIT.state_path(target).read_bytes()
            self.assertEqual(state_content, current_state)

    def test_uninstall_preserves_modified_managed_file(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "core", {})
            KIT.apply_install(target, "core", {}, plan)
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
            "profile": "core",
            "managed": {},
        }
        with self.assertRaisesRegex(ValueError, "different profile"):
            KIT.ensure_compatible_state(state, "workshop")

    def test_automation_contains_only_traceability_assets(self) -> None:
        destinations = {
            item.relative_destination
            for item in KIT.source_items("automation")
        }
        self.assertEqual(
            {
                ".github/scripts/validate_sifap_traceability.py",
                ".github/workflows/sifap-traceability.yml",
            },
            destinations,
        )

    def test_state_is_valid_json(self) -> None:
        with self.make_target() as temp_dir:
            target = Path(temp_dir)
            plan = KIT.build_install_plan(target, "core", {})
            KIT.apply_install(target, "core", {}, plan)
            state = json.loads(
                KIT.state_path(target).read_text(encoding="utf-8")
            )
            self.assertEqual(KIT.PACKAGE_NAME, state["package"])
            self.assertEqual("core", state["profile"])


if __name__ == "__main__":
    unittest.main()
