"""Focused tests for the IssueOps dispatcher."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

MODULE_PATH = Path(__file__).with_name("dispatcher.py")
SPEC = importlib.util.spec_from_file_location(
    "issue_ops_dispatcher", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
dispatcher = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = dispatcher
SPEC.loader.exec_module(dispatcher)


class ParseCommentTests(unittest.TestCase):
    def test_parses_only_first_line(self) -> None:
        self.assertEqual(
            dispatcher.parse_comment("/check-agents\nignored"), "/check-agents"
        )
        self.assertIsNone(dispatcher.parse_comment("context\n/check-agents"))
        self.assertIsNone(dispatcher.parse_comment(" /check-agents"))

    def test_malformed_quoting_fails_without_execution(self) -> None:
        with mock.patch.object(dispatcher.subprocess, "run") as run:
            result = dispatcher.execute_command('/check-agents "')

        self.assertEqual(result.exit_code, 2)
        run.assert_not_called()

    def test_shell_syntax_is_rejected_as_an_argument(self) -> None:
        with mock.patch.object(dispatcher.subprocess, "run") as run:
            result = dispatcher.execute_command("/check-agents; touch owned")

        self.assertEqual(result.exit_code, 2)
        run.assert_not_called()


class CommandTests(unittest.TestCase):
    def test_help_is_supported_without_subprocess(self) -> None:
        with mock.patch.object(dispatcher.subprocess, "run") as run:
            result = dispatcher.execute_command("/help")

        self.assertEqual(result.exit_code, 0)
        self.assertIn("/check-agents", result.output)
        run.assert_not_called()

    def test_unsupported_cloud_commands_fail_clearly(self) -> None:
        for command in ("/onboard", "/validate"):
            with self.subTest(command=command):
                result = dispatcher.execute_command(command)
                self.assertEqual(result.exit_code, 2)
                self.assertIn("Unsupported command", result.summary)

    def test_check_agents_uses_fixed_argv_and_propagates_status(self) -> None:
        completed = subprocess.CompletedProcess(
            args=[], returncode=7, stdout="validation failed\n", stderr=""
        )
        # AGENT_VALIDATOR only resolves to a real file in the published layout.
        with mock.patch.object(dispatcher, "AGENT_VALIDATOR", MODULE_PATH), \
                mock.patch.object(
                    dispatcher.subprocess, "run", return_value=completed
        ) as run:
            result = dispatcher.execute_command("/check-agents")

        self.assertEqual(result.exit_code, 7)
        self.assertIn("exit code 7", result.summary)
        run.assert_called_once_with(
            [
                dispatcher.sys.executable,
                str(MODULE_PATH),
                "--strict",
            ],
            cwd=dispatcher.REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )

    def test_missing_validator_fails_without_execution(self) -> None:
        missing = MODULE_PATH.with_name("does-not-exist.py")
        with mock.patch.object(dispatcher, "AGENT_VALIDATOR", missing), \
                mock.patch.object(dispatcher.subprocess, "run") as run:
            result = dispatcher.execute_command("/check-agents")

        self.assertEqual(result.exit_code, 2)
        self.assertIn("unavailable", result.summary)
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
