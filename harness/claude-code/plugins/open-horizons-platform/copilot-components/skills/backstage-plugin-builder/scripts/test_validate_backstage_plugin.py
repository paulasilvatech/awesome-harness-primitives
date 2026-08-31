#!/usr/bin/env python3
"""Focused tests for validate_backstage_plugin.py."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("validate_backstage_plugin.py")
SPEC = importlib.util.spec_from_file_location("validate_backstage_plugin", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BackstagePluginValidationTests(unittest.TestCase):
    def test_frontend_modes_are_explicit(self) -> None:
        new_source = "export const plugin = createFrontendPlugin({ pluginId: 'demo' });"
        legacy_source = "export const plugin = createPlugin({ id: 'demo' });"
        dual_source = f"{new_source}\n{legacy_source}"

        self.assertTrue(MODULE.frontend_mode_check("new", new_source)[1])
        self.assertTrue(MODULE.frontend_mode_check("legacy", legacy_source)[1])
        self.assertTrue(MODULE.frontend_mode_check("dual", dual_source)[1])
        self.assertFalse(MODULE.frontend_mode_check("dual", new_source)[1])

    def test_backstage_core_root_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / ".changeset").mkdir()
            (root / "packages/frontend-plugin-api").mkdir(parents=True)
            (root / "packages/backend-plugin-api").mkdir(parents=True)
            (root / "yarn.lock").write_text("", encoding="utf-8")

            self.assertTrue(MODULE.is_backstage_core_root(root))

    def test_kind_detection_prefers_frontend_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "src").mkdir()
            (root / "src/plugin.ts").write_text("", encoding="utf-8")
            package = {"name": "@example/backstage-plugin-demo"}
            (root / "package.json").write_text(json.dumps(package), encoding="utf-8")

            self.assertEqual(MODULE.detect_kind(root, package), "frontend")


if __name__ == "__main__":
    unittest.main()
