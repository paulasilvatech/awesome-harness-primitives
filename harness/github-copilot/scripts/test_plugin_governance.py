#!/usr/bin/env python3
"""Focused tests for deterministic plugin classification."""

from __future__ import annotations

import unittest
from datetime import date

from _plugin_governance import classify

AS_OF = date(2026, 8, 24)
UPSTREAM = {
    "componentSource": "plugin",
    "upstreamRepository": "https://github.com/github/awesome-copilot",
    "upstreamCommit": "318066d2213b510e89b500ed0d53506c54093ddc",
}


class LifecycleTests(unittest.TestCase):
    def test_stable_version_is_active(self) -> None:
        result = classify(
            version="1.0.2",
            source_config={"componentSource": "library"},
            as_of=AS_OF,
        )
        self.assertEqual(result.lifecycle, "active")

    def test_pre_release_major_is_incubating(self) -> None:
        result = classify(
            version="0.1.2",
            source_config={"componentSource": "library"},
            as_of=AS_OF,
        )
        self.assertEqual(result.lifecycle, "incubating")

    def test_explicit_override_wins(self) -> None:
        result = classify(
            version="1.0.2",
            source_config={
                "componentSource": "library",
                "governance": {
                    "lifecycle": "deprecated",
                    "evidence": "docs/HARNESS-VALIDATION.md#upstream-archived",
                },
            },
            as_of=AS_OF,
        )
        self.assertEqual(result.lifecycle, "deprecated")


class AssuranceTests(unittest.TestCase):
    def test_static_when_no_runtime_surface(self) -> None:
        result = classify(
            version="1.0.2",
            source_config={"componentSource": "library"},
            as_of=AS_OF,
        )
        self.assertEqual(result.assurance, "static-validated")

    def test_runtime_surface_without_probe_requires_runtime(self) -> None:
        for surface in ("mcp_servers", "hooks", "extensions"):
            with self.subTest(surface=surface):
                result = classify(
                    version="1.0.2",
                    source_config={"componentSource": "plugin"},
                    as_of=AS_OF,
                    **{surface: 1},
                )
                self.assertEqual(result.assurance, "runtime-required")

    def test_recent_probe_is_verified(self) -> None:
        result = classify(
            version="1.0.2",
            source_config={
                "componentSource": "plugin",
                "governance": {
                    "lastRuntimeProbe": "2026-08-22",
                    "evidence": "docs/HARNESS-VALIDATION.md#flat-layout",
                },
            },
            hooks=1,
            as_of=AS_OF,
        )
        self.assertEqual(result.assurance, "runtime-verified")
        self.assertEqual(result.last_runtime_probe, "2026-08-22")

    def test_probe_expires_after_freshness_window(self) -> None:
        governance = {
            "lastRuntimeProbe": "2026-08-22",
            "evidence": "docs/HARNESS-VALIDATION.md#flat-layout",
        }
        source_config = {"componentSource": "plugin", "governance": governance}
        boundary = classify(
            version="1.0.2",
            source_config=source_config,
            hooks=1,
            as_of=date(2026, 11, 20),
        )
        self.assertEqual(boundary.assurance, "runtime-verified")
        expired = classify(
            version="1.0.2",
            source_config=source_config,
            hooks=1,
            as_of=date(2026, 11, 21),
        )
        self.assertEqual(expired.assurance, "runtime-stale")

    def test_malformed_probe_does_not_claim_verification(self) -> None:
        result = classify(
            version="1.0.2",
            source_config={
                "componentSource": "plugin",
                "governance": {"lastRuntimeProbe": "not-a-date"},
            },
            mcp_servers=2,
            as_of=AS_OF,
        )
        self.assertEqual(result.assurance, "runtime-required")


class ProvenanceTests(unittest.TestCase):
    def test_pinned_upstream_is_mirror(self) -> None:
        result = classify(
            version="1.0.4",
            source_config=UPSTREAM,
            extensions=1,
            as_of=AS_OF,
        )
        self.assertEqual(result.provenance, "upstream-mirror")

    def test_repository_owned_without_upstream(self) -> None:
        result = classify(
            version="1.0.4",
            source_config={"componentSource": "library"},
            as_of=AS_OF,
        )
        self.assertEqual(result.provenance, "repository")

    def test_partial_upstream_metadata_is_not_mirror(self) -> None:
        result = classify(
            version="1.0.4",
            source_config={
                "componentSource": "plugin",
                "upstreamRepository": "https://github.com/github/awesome-copilot",
            },
            as_of=AS_OF,
        )
        self.assertEqual(result.provenance, "repository")


if __name__ == "__main__":
    unittest.main()
