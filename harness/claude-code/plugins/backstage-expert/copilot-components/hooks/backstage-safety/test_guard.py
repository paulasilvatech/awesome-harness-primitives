#!/usr/bin/env python3
"""Focused tests for the Backstage safety hook."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("guard.py")
SPEC = importlib.util.spec_from_file_location("backstage_safety_guard", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
GUARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GUARD)


class BackstageSafetyTests(unittest.TestCase):
    def test_safe_command_is_allowed(self) -> None:
        reason = GUARD.risk_reason("bash", "yarn test plugins/catalog", core_root=True)
        self.assertIsNone(reason)

    def test_exact_core_tsc_is_allowed(self) -> None:
        reason = GUARD.risk_reason("bash", "yarn tsc", core_root=True)
        self.assertIsNone(reason)

    def test_core_tsc_arguments_require_approval(self) -> None:
        reason = GUARD.risk_reason("bash", "yarn tsc --skipLibCheck", core_root=True)
        self.assertIn("unsupported arguments", reason)

    def test_core_build_requires_approval_but_api_reports_do_not(self) -> None:
        self.assertIsNotNone(
            GUARD.risk_reason("bash", "yarn build", core_root=True)
        )
        self.assertIsNone(
            GUARD.risk_reason("bash", "yarn build:api-reports", core_root=True)
        )

    def test_create_app_requires_approval(self) -> None:
        reason = GUARD.risk_reason(
            "execute",
            "npx @backstage/create-app@latest",
            core_root=False,
        )
        self.assertIn("creating", reason)

    def test_techdocs_publish_requires_approval(self) -> None:
        reason = GUARD.risk_reason(
            "bash",
            "npx @techdocs/cli publish --publisher-type googleGcs",
            core_root=False,
        )
        self.assertIn("TechDocs", reason)

    def test_backstage_json_edit_requires_approval(self) -> None:
        reason = GUARD.risk_reason(
            "edit",
            'backstage.json {"version": "1.54.0"}',
            core_root=False,
        )
        self.assertIn("version", reason)

    def test_core_detection_requires_identity_and_layout(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp_dir:
            root = Path(temp_dir)
            (root / ".changeset").mkdir()
            (root / "packages/frontend-plugin-api").mkdir(parents=True)
            (root / "packages/backend-plugin-api").mkdir(parents=True)
            (root / "package.json").write_text(
                json.dumps(
                    {
                        "repository": {
                            "url": "https://github.com/backstage/backstage"
                        }
                    }
                ),
                encoding="utf-8",
            )
            self.assertTrue(GUARD.is_backstage_core(root))


if __name__ == "__main__":
    unittest.main()
