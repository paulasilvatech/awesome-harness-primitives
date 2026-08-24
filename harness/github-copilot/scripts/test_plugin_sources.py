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


class GovernanceMetadataTests(unittest.TestCase):
    def manifest(self, governance: object) -> dict:
        return {
            "version": SOURCE_LAYOUT_VERSION,
            "plugins": {
                "example": {
                    "componentSource": "plugin",
                    "governance": governance,
                }
            },
        }

    def test_accepts_dated_probe_with_evidence(self) -> None:
        validate_source_manifest(
            self.manifest(
                {
                    "lifecycle": "active",
                    "lastRuntimeProbe": "2026-08-22",
                    "evidence": "docs/HARNESS-VALIDATION.md#flat-layout",
                }
            )
        )

    def test_rejects_unknown_governance_key(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported governance keys"):
            validate_source_manifest(self.manifest({"tier": "gold"}))

    def test_rejects_derived_lifecycle_override(self) -> None:
        with self.assertRaisesRegex(ValueError, "active or deprecated"):
            validate_source_manifest(
                self.manifest({"lifecycle": "incubating"}))

    def test_rejects_malformed_probe_date(self) -> None:
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            validate_source_manifest(
                self.manifest(
                    {
                        "lastRuntimeProbe": "22-08-2026",
                        "evidence": "docs/HARNESS-VALIDATION.md",
                    }
                )
            )

    def test_rejects_probe_without_evidence(self) -> None:
        with self.assertRaisesRegex(ValueError, "requires evidence"):
            validate_source_manifest(
                self.manifest({"lastRuntimeProbe": "2026-08-22"})
            )

    def test_rejects_deprecated_without_evidence(self) -> None:
        with self.assertRaisesRegex(ValueError, "requires evidence"):
            validate_source_manifest(
                self.manifest({"lifecycle": "deprecated"}))

    def test_rejects_non_object_governance(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be an object"):
            validate_source_manifest(self.manifest("active"))


if __name__ == "__main__":
    unittest.main()
