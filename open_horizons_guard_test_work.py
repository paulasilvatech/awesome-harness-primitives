#!/usr/bin/env python3
"""Focused tests for Open Horizons AEG and config hook policy."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("guard.py")
SPEC = importlib.util.spec_from_file_location(
    "open_horizons_safety_guard",
    SCRIPT,
)
assert SPEC is not None and SPEC.loader is not None
GUARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GUARD)


class OpenHorizonsSafetyTests(unittest.TestCase):
    def test_read_only_aeg_tool_requires_no_decision(self) -> None:
        result = GUARD.additional_decision(
            "preMcpToolCall",
            "open-horizons-aeg/aeg_get_run",
            "run_id run-123",
        )
        self.assertIsNone(result)

    def test_mutating_aeg_tool_requires_approval(self) -> None:
        result = GUARD.additional_decision(
            "preMcpToolCall",
            "open-horizons-aeg/aeg_decide_gate",
            "run_id run-123 decision approve",
        )
        self.assertEqual(result[0], "ask")
        self.assertNotIn("run-123", result[1])

    def test_literal_secret_in_app_config_is_denied(self) -> None:
        result = GUARD.additional_decision(
            "preToolUse",
            "edit",
            "backstage/app-config.local.yaml token: abcdefghijklmnop",
        )
        self.assertEqual(result[0], "deny")
        self.assertNotIn("abcdefghijklmnop", result[1])

    def test_environment_reference_is_allowed(self) -> None:
        result = GUARD.additional_decision(
            "preToolUse",
            "edit",
            "backstage/app-config.local.yaml token: ${AEG_API_TOKEN}",
        )
        self.assertIsNone(result)

    def test_protected_portal_path_requires_approval(self) -> None:
        result = GUARD.additional_decision(
            "preToolUse",
            "write",
            "packages/backend/src/plugins/auth.ts",
        )
        self.assertEqual(result[0], "ask")


if __name__ == "__main__":
    unittest.main()
