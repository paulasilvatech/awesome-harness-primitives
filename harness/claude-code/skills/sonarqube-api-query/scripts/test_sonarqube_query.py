#!/usr/bin/env python3
"""Synthetic tests for the read-only SonarQube API helper."""

from __future__ import annotations

import io
import json
import unittest
import urllib.error

from sonarqube_query import (
    Endpoint,
    HttpResult,
    QueryError,
    QuerySpec,
    build_parser,
    build_spec,
    capabilities,
    execute_spec,
    http_get,
    normalize_base_url,
    parse_webservices,
)


def endpoint(path: str, parameters: set[str], deprecated: str | None = None) -> Endpoint:
    return Endpoint(
        path=path,
        parameters=frozenset(parameters),
        deprecated_since=deprecated,
        since=None,
        is_post=False,
    )


class FakeResponse:
    def __init__(
        self,
        payload: object,
        *,
        status: int = 200,
        headers: dict[str, str] | None = None,
    ):
        self.status = status
        self.headers = headers or {"Content-Type": "application/json"}
        self._body = json.dumps(payload).encode("utf-8")

    def read(self) -> bytes:
        return self._body

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        return False


class SonarQubeQueryTests(unittest.TestCase):
    def test_base_url_preserves_context_path_and_rejects_credentials(self):
        self.assertEqual(
            normalize_base_url("https://example.test/sonarqube/"),
            "https://example.test/sonarqube",
        )
        with self.assertRaisesRegex(QueryError, "must not contain credentials"):
            normalize_base_url("https://user:secret@example.test")
        with self.assertRaisesRegex(QueryError, "query string"):
            normalize_base_url("https://example.test?token=secret")

    def test_webservice_discovery_captures_parameters_and_deprecation(self):
        endpoints = parse_webservices(
            {
                "webServices": [
                    {
                        "path": "api/issues",
                        "actions": [
                            {
                                "key": "search",
                                "deprecatedSince": "2026.4",
                                "params": [{"key": "components"}, {"key": "p"}],
                            }
                        ],
                    }
                ]
            }
        )
        discovered = endpoints["/api/issues/search"]
        self.assertEqual(discovered.parameters, frozenset({"components", "p"}))
        self.assertEqual(discovered.deprecated_since, "2026.4")
        self.assertFalse(discovered.is_post)

    def test_issue_query_selects_server_project_parameter(self):
        parser = build_parser()
        args = parser.parse_args(
            [
                "--base-url",
                "https://example.test",
                "issues",
                "--project-key",
                "acme:payments",
                "--resolved",
                "false",
            ]
        )
        spec = build_spec(
            args,
            {
                "/api/issues/search": endpoint(
                    "/api/issues/search",
                    {
                        "components",
                        "resolved",
                        "severities",
                        "statuses",
                        "types",
                        "rules",
                        "branch",
                        "pullRequest",
                        "p",
                        "ps",
                    },
                )
            },
        )
        self.assertEqual(spec.parameters["components"], "acme:payments")
        self.assertNotIn("componentKeys", spec.parameters)
        self.assertEqual(spec.parameters["resolved"], "false")

    def test_project_search_uses_component_search_and_project_qualifier(self):
        parser = build_parser()
        args = parser.parse_args(
            [
                "--base-url",
                "https://example.test",
                "projects",
                "--query",
                "payments",
            ]
        )
        spec = build_spec(
            args,
            {
                "/api/components/search": endpoint(
                    "/api/components/search",
                    {"q", "qualifiers", "p", "ps"},
                )
            },
        )
        self.assertEqual(spec.endpoint.path, "/api/components/search")
        self.assertEqual(spec.parameters["qualifiers"], "TRK")
        self.assertEqual(spec.parameters["q"], "payments")

    def test_issue_query_selects_cloud_parameter_and_organization(self):
        parser = build_parser()
        args = parser.parse_args(
            [
                "--base-url",
                "https://sonarcloud.io",
                "--organization",
                "acme",
                "issues",
                "--project-key",
                "payments",
            ]
        )
        spec = build_spec(
            args,
            {
                "/api/issues/search": endpoint(
                    "/api/issues/search",
                    {
                        "componentKeys",
                        "organization",
                        "resolved",
                        "severities",
                        "statuses",
                        "types",
                        "rules",
                        "branch",
                        "pullRequest",
                        "p",
                        "ps",
                    },
                )
            },
        )
        self.assertEqual(spec.parameters["componentKeys"], "payments")
        self.assertEqual(spec.parameters["organization"], "acme")

    def test_unsupported_branch_scope_fails_instead_of_being_dropped(self):
        parser = build_parser()
        args = parser.parse_args(
            [
                "--base-url",
                "https://sonarcloud.io",
                "hotspots",
                "--project-key",
                "payments",
                "--branch",
                "main",
            ]
        )
        with self.assertRaisesRegex(QueryError, "does not expose branch"):
            build_spec(
                args,
                {
                    "/api/hotspots/search": endpoint(
                        "/api/hotspots/search",
                        {"projectKey", "status", "resolution", "p", "ps"},
                    )
                },
            )

    def test_http_get_uses_bearer_header_without_putting_token_in_url(self):
        captured = {}

        def opener(request, timeout):
            captured["request"] = request
            captured["timeout"] = timeout
            return FakeResponse(
                {"status": "UP"},
                headers={
                    "Content-Type": "application/json",
                    "SonarQube-Authentication-Token-Expiration": "2026-12-01",
                },
            )

        result = http_get(
            "https://example.test/sonarqube",
            "/api/system/status",
            {},
            "top-secret",
            12,
            opener=opener,
        )
        request = captured["request"]
        self.assertEqual(request.get_header("Authorization"), "Bearer top-secret")
        self.assertNotIn("top-secret", request.full_url)
        self.assertEqual(captured["timeout"], 12)
        self.assertEqual(result.payload, {"status": "UP"})
        self.assertEqual(
            result.headers["sonarqube-authentication-token-expiration"],
            "2026-12-01",
        )

    def test_http_429_surfaces_retry_after(self):
        def opener(request, timeout):
            raise urllib.error.HTTPError(
                request.full_url,
                429,
                "Too Many Requests",
                {
                    "Content-Type": "application/json",
                    "Retry-After": "60",
                },
                io.BytesIO(b'{"errors":[{"msg":"rate limit"}]}'),
            )

        with self.assertRaisesRegex(QueryError, "Retry-After: 60"):
            http_get(
                "https://sonarcloud.io",
                "/api/projects/search",
                {},
                None,
                30,
                opener=opener,
            )

    def test_all_pages_combines_results(self):
        calls = []

        def getter(base_url, path, parameters, token, timeout):
            calls.append(dict(parameters))
            page = int(parameters["p"])
            issues = [{"key": "one"}, {"key": "two"}] if page == 1 else [{"key": "three"}]
            return HttpResult(
                200,
                {"content-type": "application/json"},
                {
                    "paging": {"pageIndex": page, "pageSize": 2, "total": 3},
                    "issues": issues,
                },
            )

        spec = QuerySpec(
            endpoint("/api/issues/search", {"p", "ps"}),
            {"p": "1", "ps": "2"},
            "issues",
        )
        result = execute_spec(
            spec,
            "https://example.test",
            None,
            30,
            all_pages=True,
            max_pages=3,
            getter=getter,
        )
        self.assertEqual(
            [item["key"] for item in result.http.payload["issues"]],
            ["one", "two", "three"],
        )
        self.assertEqual(result.pages_fetched, 2)
        self.assertFalse(result.truncated)
        self.assertEqual([call["p"] for call in calls], ["1", "2"])

    def test_all_pages_reports_truncation_at_bound(self):
        def getter(base_url, path, parameters, token, timeout):
            return HttpResult(
                200,
                {},
                {
                    "paging": {"pageIndex": 1, "pageSize": 1, "total": 5},
                    "metrics": [{"key": "coverage"}],
                },
            )

        spec = QuerySpec(
            endpoint("/api/metrics/search", {"p", "ps"}),
            {"p": "1", "ps": "1"},
            "metrics",
        )
        result = execute_spec(
            spec,
            "https://example.test",
            None,
            30,
            all_pages=True,
            max_pages=1,
            getter=getter,
        )
        self.assertTrue(result.truncated)
        self.assertTrue(result.http.payload["paging"]["truncated"])

    def test_all_pages_supports_top_level_legacy_pagination(self):
        calls = []

        def getter(base_url, path, parameters, token, timeout):
            calls.append(dict(parameters))
            page = int(parameters["p"])
            return HttpResult(
                200,
                {},
                {
                    "p": page,
                    "ps": 1,
                    "total": 2,
                    "metrics": [{"key": f"metric-{page}"}],
                },
            )

        spec = QuerySpec(
            endpoint("/api/metrics/search", {"p", "ps"}),
            {"p": "1", "ps": "1"},
            "metrics",
        )
        result = execute_spec(
            spec,
            "https://example.test",
            None,
            30,
            all_pages=True,
            max_pages=2,
            getter=getter,
        )
        self.assertEqual(
            [item["key"] for item in result.http.payload["metrics"]],
            ["metric-1", "metric-2"],
        )
        self.assertEqual([call["p"] for call in calls], ["1", "2"])
        self.assertFalse(result.truncated)

    def test_all_pages_removes_overlapping_items(self):
        def getter(base_url, path, parameters, token, timeout):
            page = int(parameters["p"])
            metrics = (
                [{"key": "one"}, {"key": "two"}]
                if page == 1
                else [{"key": "two"}, {"key": "three"}]
            )
            return HttpResult(
                200,
                {},
                {"p": page, "ps": 2, "total": 4, "metrics": metrics},
            )

        spec = QuerySpec(
            endpoint("/api/metrics/search", {"p", "ps"}),
            {"p": "1", "ps": "2"},
            "metrics",
        )
        result = execute_spec(
            spec,
            "https://example.test",
            None,
            30,
            all_pages=True,
            max_pages=2,
            getter=getter,
        )
        self.assertEqual(
            [item["key"] for item in result.http.payload["metrics"]],
            ["one", "two", "three"],
        )
        self.assertEqual(result.duplicates_removed, 1)
        self.assertFalse(result.stalled)

    def test_capabilities_preserve_live_deprecation_metadata(self):
        rows = capabilities(
            {
                "/api/qualitygates/project_status": endpoint(
                    "/api/qualitygates/project_status",
                    {"projectKey"},
                    deprecated="16 September, 2025",
                )
            }
        )
        quality_gate = next(
            row for row in rows if row["command"] == "quality-gate"
        )
        self.assertTrue(quality_gate["available"])
        self.assertEqual(
            quality_gate["deprecatedSince"],
            "16 September, 2025",
        )


if __name__ == "__main__":
    unittest.main()
