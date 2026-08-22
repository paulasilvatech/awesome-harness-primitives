#!/usr/bin/env python3
"""Focused tests for flat plugin source metadata."""

from __future__ import annotations

import unittest

from _plugin_sources import SOURCE_LAYOUT_VERSION, validate_source_manifest


class PluginSourceManifestTests(unittest.TestCase):
    def test_accepts_flat_source_metadata(self) -> None:
        validate_source_manifest(
            {
                "version": SOURCE_LAYOUT_VERSION,
                "plugins": {
                    "example": {
                        "componentSource": "plugin",
                        "extensionSources": ["./extensions/example"],
                    }
                },
            }
        )

    def test_rejects_removed_layout_version_key(self) -> None:
        with self.assertRaisesRegex(ValueError, "layoutVersion"):
            validate_source_manifest(
                {
                    "version": SOURCE_LAYOUT_VERSION,
                    "plugins": {
                        "example": {
                            "componentSource": "plugin",
                            "layoutVersion": 1,
                        }
                    },
                }
            )


if __name__ == "__main__":
    unittest.main()
