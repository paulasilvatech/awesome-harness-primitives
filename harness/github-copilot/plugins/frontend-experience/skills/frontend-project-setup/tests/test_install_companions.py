from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "install_companions.py"
SPEC = importlib.util.spec_from_file_location("install_companions", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def create_workspace(root: Path) -> None:
    (root / "package.json").write_text(
        json.dumps(
            {
                "dependencies": {"react": "19.0.0"},
                "scripts": {"test": "vitest", "build": "vite build"},
            }
        ),
        encoding="utf-8",
    )
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "public").mkdir()


class CompanionInstallerTests(unittest.TestCase):
    def test_plan_is_a_no_write_operation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            create_workspace(workspace)
            result = MODULE.main(
                ["--workspace", str(workspace), "--action", "plan", "--json"]
            )
            self.assertEqual(0, result)
            self.assertFalse((workspace / ".github").exists())
            self.assertFalse((workspace / ".vscode").exists())

    def test_apply_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            create_workspace(workspace)
            result = MODULE.main(
                [
                    "--workspace",
                    str(workspace),
                    "--action",
                    "apply",
                    "--approve",
                    "--json",
                ]
            )
            self.assertEqual(0, result)
            metadata = workspace / MODULE.METADATA_REL
            self.assertTrue(metadata.is_file())
            _, actions, _ = MODULE.build_install_plan(
                workspace, include_mcp=False, force=False
            )
            changed = [
                item for item in actions if item.action in {"create", "update", "conflict"}
            ]
            self.assertEqual([], changed)

    def test_conflict_performs_no_partial_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            create_workspace(workspace)
            conflict = (
                workspace / ".github" / "prompts" / "frontend-design.prompt.md"
            )
            conflict.parent.mkdir(parents=True)
            conflict.write_text("team-owned\n", encoding="utf-8")
            untouched = (
                workspace
                / ".github"
                / "instructions"
                / "frontend-experience.instructions.md"
            )
            result = MODULE.main(
                [
                    "--workspace",
                    str(workspace),
                    "--action",
                    "apply",
                    "--approve",
                    "--json",
                ]
            )
            self.assertEqual(2, result)
            self.assertEqual("team-owned\n", conflict.read_text(encoding="utf-8"))
            self.assertFalse(untouched.exists())
            self.assertFalse((workspace / MODULE.METADATA_REL).exists())

    def test_force_is_explicit_and_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            create_workspace(workspace)
            conflict = (
                workspace / ".github" / "prompts" / "frontend-design.prompt.md"
            )
            conflict.parent.mkdir(parents=True)
            conflict.write_text("team-owned\n", encoding="utf-8")
            result = MODULE.main(
                [
                    "--workspace",
                    str(workspace),
                    "--action",
                    "apply",
                    "--approve",
                    "--force",
                    "--json",
                ]
            )
            self.assertEqual(0, result)
            self.assertIn("# /frontend-design", conflict.read_text(encoding="utf-8"))

    def test_uninstall_preserves_modified_owned_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            create_workspace(workspace)
            self.assertEqual(
                0,
                MODULE.main(
                    [
                        "--workspace",
                        str(workspace),
                        "--action",
                        "apply",
                        "--approve",
                        "--json",
                    ]
                ),
            )
            modified = (
                workspace / ".github" / "prompts" / "frontend-design.prompt.md"
            )
            modified.write_text(
                modified.read_text(encoding="utf-8") + "\nTeam change.\n",
                encoding="utf-8",
            )
            removable = (
                workspace
                / ".github"
                / "instructions"
                / "frontend-experience.instructions.md"
            )
            self.assertEqual(
                0,
                MODULE.main(
                    [
                        "--workspace",
                        str(workspace),
                        "--action",
                        "uninstall",
                        "--approve",
                        "--json",
                    ]
                ),
            )
            self.assertTrue(modified.is_file())
            self.assertIn("Team change.", modified.read_text(encoding="utf-8"))
            self.assertFalse(removable.exists())
            self.assertFalse((workspace / MODULE.METADATA_REL).exists())

    def test_mcp_merge_and_uninstall_preserve_other_servers(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            create_workspace(workspace)
            mcp = workspace / MODULE.MCP_REL
            mcp.parent.mkdir()
            mcp.write_text(
                json.dumps(
                    {
                        "servers": {
                            "existing": {
                                "type": "stdio",
                                "command": "example",
                                "args": [],
                            }
                        },
                        "inputs": [{"id": "example", "type": "promptString"}],
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(
                0,
                MODULE.main(
                    [
                        "--workspace",
                        str(workspace),
                        "--action",
                        "apply",
                        "--approve",
                        "--include-vscode-mcp",
                        "--json",
                    ]
                ),
            )
            installed = json.loads(mcp.read_text(encoding="utf-8"))
            self.assertIn("existing", installed["servers"])
            self.assertIn("playwright", installed["servers"])
            self.assertEqual(
                0,
                MODULE.main(
                    [
                        "--workspace",
                        str(workspace),
                        "--action",
                        "uninstall",
                        "--approve",
                        "--json",
                    ]
                ),
            )
            preserved = json.loads(mcp.read_text(encoding="utf-8"))
            self.assertEqual(["existing"], list(preserved["servers"]))
            self.assertEqual([{"id": "example", "type": "promptString"}], preserved["inputs"])

    def test_rejects_path_traversal_and_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            workspace = Path(temp)
            create_workspace(workspace)
            with self.assertRaises(ValueError):
                MODULE.safe_target(workspace, Path("../outside"))

            github = workspace / ".github"
            os.symlink(outside, github)
            with self.assertRaises(ValueError):
                MODULE.build_install_plan(
                    workspace, include_mcp=False, force=False
                )
            self.assertEqual([], list(Path(outside).iterdir()))

    def test_discoverability_requires_public_route_evidence_or_override(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            (workspace / "package.json").write_text(
                json.dumps(
                    {
                        "dependencies": {
                            "expo": "53.0.20",
                            "react": "19.0.0",
                            "react-native": "0.79.5",
                        }
                    }
                ),
                encoding="utf-8",
            )
            (workspace / "app").mkdir()
            context, actions, _ = MODULE.build_install_plan(
                workspace,
                include_mcp=False,
                force=False,
            )
            self.assertFalse(context["discoverability_selected"])
            skipped = {
                item.path for item in actions if item.action == "skipped"
            }
            self.assertTrue(
                {
                    ".github/instructions/frontend-discoverability.instructions.md",
                    ".github/prompts/frontend-assets.prompt.md",
                }
                <= skipped
            )

            forced_context, forced_actions, _ = MODULE.build_install_plan(
                workspace,
                include_mcp=False,
                force=False,
                discoverability="include",
            )
            self.assertTrue(forced_context["discoverability_selected"])
            selected = {
                item.path
                for item in forced_actions
                if item.action in {"create", "update", "unchanged"}
            }
            self.assertIn(
                ".github/instructions/frontend-discoverability.instructions.md",
                selected,
            )
            self.assertIn(".github/prompts/frontend-assets.prompt.md", selected)

    def test_interrupted_apply_rolls_back_prior_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            create_workspace(workspace)
            _, actions, metadata = MODULE.build_install_plan(
                workspace, include_mcp=False, force=False
            )
            calls = 0

            def flaky_writer(path: Path, content: bytes) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("simulated interruption")
                MODULE.atomic_write(path, content)

            with self.assertRaises(OSError):
                MODULE.apply_install(
                    workspace, actions, metadata, writer=flaky_writer
                )
            for action in actions:
                if action.action in {"create", "update"}:
                    self.assertFalse((workspace / action.path).exists())
            self.assertFalse((workspace / MODULE.METADATA_REL).exists())


if __name__ == "__main__":
    unittest.main()
