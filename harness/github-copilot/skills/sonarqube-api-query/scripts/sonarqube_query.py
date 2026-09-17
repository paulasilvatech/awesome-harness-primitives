#!/usr/bin/env python3
"""Query a bounded set of read-only SonarQube Web API v1 endpoints."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Any, Callable

DEFAULT_TIMEOUT = 30
DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 500
DEFAULT_MAX_PAGES = 10
USER_AGENT = "copilot-primitives-sonarqube-api-query/1.0"

ENV_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
PROJECT_KEY_RE = re.compile(r"^[A-Za-z0-9_.:-]+$")
IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9_.:-]+$")
CSV_RE = re.compile(r"^[A-Za-z0-9_.:-]+(?:,[A-Za-z0-9_.:-]+)*$")

COMMAND_ENDPOINTS = {
    "server-status": "/api/system/status",
    "server-version": "/api/server/version",
    "projects": "/api/components/search",
    "project": "/api/components/show",
    "branches": "/api/project_branches/list",
    "pull-requests": "/api/project_pull_requests/list",
    "quality-gate": "/api/qualitygates/project_status",
    "quality-gate-definition": "/api/qualitygates/get_by_project",
    "quality-gates": "/api/qualitygates/list",
    "measures": "/api/measures/component",
    "issues": "/api/issues/search",
    "hotspots": "/api/hotspots/search",
    "hotspot": "/api/hotspots/show",
    "analyses": "/api/project_analyses/search",
    "quality-profiles": "/api/qualityprofiles/search",
    "rule": "/api/rules/show",
    "metrics": "/api/metrics/search",
}


class QueryError(Exception):
    """Raised for actionable query failures."""


@dataclass(frozen=True)
class Endpoint:
    path: str
    parameters: frozenset[str]
    deprecated_since: str | None
    since: str | None
    is_post: bool


@dataclass(frozen=True)
class HttpResult:
    status: int
    headers: dict[str, str]
    payload: Any


@dataclass(frozen=True)
class QuerySpec:
    endpoint: Endpoint
    parameters: dict[str, str]
    collection_key: str | None = None


@dataclass(frozen=True)
class ExecutionResult:
    http: HttpResult
    pages_fetched: int = 1
    truncated: bool = False
    duplicates_removed: int = 0
    stalled: bool = False


HttpGetter = Callable[[str, str, dict[str, str], str | None, int], HttpResult]


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed


def page_size(value: str) -> int:
    parsed = positive_int(value)
    if parsed > MAX_PAGE_SIZE:
        raise argparse.ArgumentTypeError(f"must not exceed {MAX_PAGE_SIZE}")
    return parsed


def normalize_base_url(value: str | None) -> str:
    if not value or not value.strip():
        raise QueryError("SonarQube base URL is required via --base-url or SONARQUBE_URL")
    parsed = urllib.parse.urlsplit(value.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise QueryError("base URL must use http:// or https:// and include a host")
    if parsed.username or parsed.password:
        raise QueryError("base URL must not contain credentials")
    if parsed.query or parsed.fragment:
        raise QueryError("base URL must not contain a query string or fragment")
    path = parsed.path.rstrip("/")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))


def validate_env_name(value: str) -> str:
    if not ENV_NAME_RE.fullmatch(value):
        raise QueryError(f"invalid environment variable name: {value!r}")
    return value


def validate_project_key(value: str) -> str:
    if not PROJECT_KEY_RE.fullmatch(value):
        raise QueryError(
            "project key must contain only letters, digits, underscore, hyphen, dot, or colon"
        )
    return value


def validate_identifier(value: str, label: str) -> str:
    if not IDENTIFIER_RE.fullmatch(value):
        raise QueryError(
            f"{label} must contain only letters, digits, underscore, hyphen, dot, or colon"
        )
    return value


def validate_csv(value: str, label: str) -> str:
    if not CSV_RE.fullmatch(value):
        raise QueryError(f"{label} must be a comma-separated list of identifiers")
    return value


def validate_text(value: str, label: str, *, maximum: int = 500) -> str:
    stripped = value.strip()
    if not stripped:
        raise QueryError(f"{label} must not be empty")
    if len(stripped) > maximum:
        raise QueryError(f"{label} must not exceed {maximum} characters")
    if any(ord(character) < 32 or ord(character) == 127 for character in stripped):
        raise QueryError(f"{label} must not contain control characters")
    return stripped


def validate_date(value: str, label: str) -> str:
    try:
        date.fromisoformat(value)
    except ValueError as error:
        raise QueryError(f"{label} must use YYYY-MM-DD format") from error
    return value


def request_url(base_url: str, endpoint: str, parameters: dict[str, str]) -> str:
    if not endpoint.startswith("/api/") or ".." in endpoint.split("/"):
        raise QueryError(f"refusing unsupported endpoint path: {endpoint}")
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    if parameters:
        url = f"{url}?{urllib.parse.urlencode(parameters)}"
    return url


def parse_payload(body: bytes, content_type: str) -> Any:
    if not body:
        return None
    text = body.decode("utf-8", errors="replace")
    if "json" in content_type.lower() or text.lstrip().startswith(("{", "[")):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
    return text


def error_detail(payload: Any) -> str:
    if isinstance(payload, dict):
        errors = payload.get("errors")
        if isinstance(errors, list):
            messages = [
                item.get("msg")
                for item in errors
                if isinstance(item, dict) and isinstance(item.get("msg"), str)
            ]
            if messages:
                return "; ".join(messages)
        message = payload.get("message")
        if isinstance(message, str):
            return message
    if isinstance(payload, str):
        return payload.strip()[:1000]
    return ""


def http_get(
    base_url: str,
    endpoint: str,
    parameters: dict[str, str],
    token: str | None,
    timeout: int,
    opener: Callable[..., Any] = urllib.request.urlopen,
) -> HttpResult:
    headers = {
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    if token:
        if "\r" in token or "\n" in token:
            raise QueryError("token environment variable contains invalid newline characters")
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        request_url(base_url, endpoint, parameters),
        headers=headers,
        method="GET",
    )
    try:
        with opener(request, timeout=timeout) as response:
            response_headers = {
                key.lower(): value for key, value in response.headers.items()
            }
            payload = parse_payload(
                response.read(),
                response_headers.get("content-type", ""),
            )
            return HttpResult(
                status=getattr(response, "status", 200),
                headers=response_headers,
                payload=payload,
            )
    except urllib.error.HTTPError as error:
        response_headers = {
            key.lower(): value for key, value in error.headers.items()
        } if error.headers else {}
        try:
            error_body = error.read(8192)
        finally:
            error.close()
        payload = parse_payload(error_body, response_headers.get("content-type", ""))
        detail = error_detail(payload)
        message = f"HTTP {error.code} from {endpoint}"
        if detail:
            message = f"{message}: {detail}"
        retry_after = response_headers.get("retry-after")
        if error.code == 429 and retry_after:
            message = f"{message} (Retry-After: {retry_after})"
        raise QueryError(message) from error
    except urllib.error.URLError as error:
        raise QueryError(f"cannot reach SonarQube at {base_url}: {error.reason}") from error
    except TimeoutError as error:
        raise QueryError(f"SonarQube request timed out after {timeout} seconds") from error


def parse_webservices(payload: Any) -> dict[str, Endpoint]:
    if not isinstance(payload, dict) or not isinstance(payload.get("webServices"), list):
        raise QueryError("/api/webservices/list returned an unexpected response")
    endpoints: dict[str, Endpoint] = {}
    for service in payload["webServices"]:
        if not isinstance(service, dict) or not isinstance(service.get("path"), str):
            continue
        service_path = service["path"].strip("/")
        actions = service.get("actions")
        if not isinstance(actions, list):
            continue
        for action in actions:
            if not isinstance(action, dict) or not isinstance(action.get("key"), str):
                continue
            path = f"/{service_path}/{action['key']}"
            raw_parameters = action.get("params")
            parameters = frozenset(
                parameter["key"]
                for parameter in raw_parameters
                if isinstance(parameter, dict) and isinstance(parameter.get("key"), str)
            ) if isinstance(raw_parameters, list) else frozenset()
            endpoints[path] = Endpoint(
                path=path,
                parameters=parameters,
                deprecated_since=(
                    str(action["deprecatedSince"])
                    if action.get("deprecatedSince") is not None
                    else None
                ),
                since=str(action["since"]) if action.get("since") is not None else None,
                is_post=bool(action.get("post")),
            )
    return endpoints


def discover_endpoints(
    base_url: str,
    token: str | None,
    timeout: int,
    getter: HttpGetter = http_get,
) -> tuple[dict[str, Endpoint], HttpResult]:
    result = getter(base_url, "/api/webservices/list", {}, token, timeout)
    return parse_webservices(result.payload), result


def require_endpoint(endpoints: dict[str, Endpoint], path: str) -> Endpoint:
    endpoint = endpoints.get(path)
    if endpoint is None:
        raise QueryError(
            f"the selected SonarQube instance does not expose read endpoint {path}; "
            "run capabilities and consult the instance API documentation"
        )
    if endpoint.is_post:
        raise QueryError(f"refusing {path} because the instance reports it as POST")
    return endpoint


def add_supported(
    endpoint: Endpoint,
    parameters: dict[str, str],
    key: str,
    value: str | None,
    label: str,
) -> None:
    if value is None:
        return
    if key not in endpoint.parameters:
        raise QueryError(f"{endpoint.path} does not expose {label} parameter {key}")
    parameters[key] = value


def add_organization(
    endpoint: Endpoint,
    parameters: dict[str, str],
    organization: str | None,
) -> None:
    if organization and "organization" in endpoint.parameters:
        parameters["organization"] = validate_identifier(organization, "organization")


def select_parameter(endpoint: Endpoint, candidates: tuple[str, ...], label: str) -> str:
    for candidate in candidates:
        if candidate in endpoint.parameters:
            return candidate
    raise QueryError(
        f"{endpoint.path} does not expose a supported {label} parameter "
        f"({', '.join(candidates)})"
    )


def add_scope(
    endpoint: Endpoint,
    parameters: dict[str, str],
    branch: str | None,
    pull_request: str | None,
) -> None:
    add_supported(
        endpoint,
        parameters,
        "branch",
        validate_text(branch, "branch", maximum=255) if branch else None,
        "branch",
    )
    add_supported(
        endpoint,
        parameters,
        "pullRequest",
        validate_identifier(pull_request, "pull request") if pull_request else None,
        "pull request",
    )


def add_pagination(
    endpoint: Endpoint,
    parameters: dict[str, str],
    page: int,
    size: int,
) -> None:
    if "p" not in endpoint.parameters or "ps" not in endpoint.parameters:
        raise QueryError(f"{endpoint.path} does not expose standard pagination")
    parameters["p"] = str(page)
    parameters["ps"] = str(size)


def build_spec(args: argparse.Namespace, endpoints: dict[str, Endpoint]) -> QuerySpec:
    path = COMMAND_ENDPOINTS.get(args.command)
    if path is None:
        raise QueryError(f"unsupported command: {args.command}")
    endpoint = require_endpoint(endpoints, path)
    parameters: dict[str, str] = {}
    collection_key: str | None = None

    if args.command == "projects":
        add_supported(
            endpoint,
            parameters,
            "q",
            validate_text(args.query, "query") if args.query else None,
            "search",
        )
        if "qualifiers" in endpoint.parameters:
            parameters["qualifiers"] = "TRK"
        add_organization(endpoint, parameters, args.organization)
        add_pagination(endpoint, parameters, args.page, args.page_size)
        collection_key = "components"
    elif args.command == "project":
        parameters["component"] = validate_project_key(args.project_key)
        add_scope(endpoint, parameters, args.branch, args.pull_request)
    elif args.command in {"branches", "pull-requests"}:
        parameters["project"] = validate_project_key(args.project_key)
        collection_key = "branches" if args.command == "branches" else "pullRequests"
    elif args.command == "quality-gate":
        parameters["projectKey"] = validate_project_key(args.project_key)
        add_scope(endpoint, parameters, args.branch, args.pull_request)
    elif args.command == "quality-gate-definition":
        parameters["project"] = validate_project_key(args.project_key)
        add_organization(endpoint, parameters, args.organization)
    elif args.command == "quality-gates":
        add_organization(endpoint, parameters, args.organization)
        collection_key = "qualitygates"
    elif args.command == "measures":
        parameters["component"] = validate_project_key(args.project_key)
        parameters["metricKeys"] = validate_csv(args.metrics, "metrics")
        add_scope(endpoint, parameters, args.branch, args.pull_request)
    elif args.command == "issues":
        project_parameter = select_parameter(
            endpoint,
            ("componentKeys", "components"),
            "project",
        )
        parameters[project_parameter] = validate_project_key(args.project_key)
        add_organization(endpoint, parameters, args.organization)
        add_scope(endpoint, parameters, args.branch, args.pull_request)
        add_supported(
            endpoint,
            parameters,
            "resolved",
            args.resolved,
            "resolved",
        )
        for key, value, label in (
            ("severities", args.severities, "severities"),
            ("statuses", args.statuses, "statuses"),
            ("types", args.types, "types"),
            ("rules", args.rules, "rules"),
        ):
            add_supported(
                endpoint,
                parameters,
                key,
                validate_csv(value, label) if value else None,
                label,
            )
        add_pagination(endpoint, parameters, args.page, args.page_size)
        collection_key = "issues"
    elif args.command == "hotspots":
        project_parameter = select_parameter(
            endpoint,
            ("projectKey", "project"),
            "project",
        )
        parameters[project_parameter] = validate_project_key(args.project_key)
        add_scope(endpoint, parameters, args.branch, args.pull_request)
        add_supported(
            endpoint,
            parameters,
            "status",
            validate_identifier(args.status, "status") if args.status else None,
            "status",
        )
        add_supported(
            endpoint,
            parameters,
            "resolution",
            validate_identifier(args.resolution, "resolution")
            if args.resolution
            else None,
            "resolution",
        )
        add_pagination(endpoint, parameters, args.page, args.page_size)
        collection_key = "hotspots"
    elif args.command == "hotspot":
        parameters["hotspot"] = validate_identifier(args.hotspot_key, "hotspot key")
    elif args.command == "analyses":
        parameters["project"] = validate_project_key(args.project_key)
        add_supported(
            endpoint,
            parameters,
            "branch",
            validate_text(args.branch, "branch", maximum=255)
            if args.branch
            else None,
            "branch",
        )
        add_supported(
            endpoint,
            parameters,
            "from",
            validate_date(args.from_date, "from date") if args.from_date else None,
            "from date",
        )
        add_supported(
            endpoint,
            parameters,
            "to",
            validate_date(args.to_date, "to date") if args.to_date else None,
            "to date",
        )
        add_pagination(endpoint, parameters, args.page, args.page_size)
        collection_key = "analyses"
    elif args.command == "quality-profiles":
        add_supported(
            endpoint,
            parameters,
            "project",
            validate_project_key(args.project_key) if args.project_key else None,
            "project",
        )
        add_supported(
            endpoint,
            parameters,
            "language",
            validate_identifier(args.language, "language") if args.language else None,
            "language",
        )
        add_organization(endpoint, parameters, args.organization)
        collection_key = "profiles"
    elif args.command == "rule":
        parameters["key"] = validate_identifier(args.rule_key, "rule key")
        add_organization(endpoint, parameters, args.organization)
    elif args.command == "metrics":
        add_pagination(endpoint, parameters, args.page, args.page_size)
        collection_key = "metrics"
    elif args.command not in {"server-status", "server-version"}:
        raise QueryError(f"command is not implemented: {args.command}")

    return QuerySpec(
        endpoint=endpoint,
        parameters=parameters,
        collection_key=collection_key,
    )


def paging_total(payload: dict[str, Any]) -> int | None:
    paging = payload.get("paging")
    if isinstance(paging, dict):
        total = paging.get("total")
        if isinstance(total, int):
            return total
    total = payload.get("total")
    return total if isinstance(total, int) else None


def item_identity(item: Any) -> str:
    if isinstance(item, dict):
        for field in ("key", "id", "uuid"):
            value = item.get(field)
            if isinstance(value, (str, int, float, bool)):
                return f"{field}:{value}"
    return json.dumps(item, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def execute_spec(
    spec: QuerySpec,
    base_url: str,
    token: str | None,
    timeout: int,
    *,
    all_pages: bool = False,
    max_pages: int = DEFAULT_MAX_PAGES,
    getter: HttpGetter = http_get,
) -> ExecutionResult:
    first = getter(base_url, spec.endpoint.path, dict(spec.parameters), token, timeout)
    if not all_pages:
        return ExecutionResult(first)
    if spec.collection_key is None:
        raise QueryError(f"{spec.endpoint.path} is not a paginated collection command")
    if not isinstance(first.payload, dict):
        raise QueryError(f"{spec.endpoint.path} returned a non-object response")
    first_items = first.payload.get(spec.collection_key)
    if not isinstance(first_items, list):
        raise QueryError(
            f"{spec.endpoint.path} did not return collection {spec.collection_key!r}"
        )

    combined_items: list[Any] = []
    seen_items: set[str] = set()
    duplicates_removed = 0
    for item in first_items:
        identity = item_identity(item)
        if identity in seen_items:
            duplicates_removed += 1
            continue
        seen_items.add(identity)
        combined_items.append(item)
    combined_payload = dict(first.payload)
    total = paging_total(first.payload)
    current_page = int(spec.parameters.get("p", "1"))
    page_size_value = int(spec.parameters.get("ps", str(DEFAULT_PAGE_SIZE)))
    pages_fetched = 1
    truncated = False
    stalled = False

    while total is not None and current_page * page_size_value < total:
        if pages_fetched >= max_pages:
            truncated = True
            break
        current_page += 1
        parameters = dict(spec.parameters)
        parameters["p"] = str(current_page)
        result = getter(base_url, spec.endpoint.path, parameters, token, timeout)
        if not isinstance(result.payload, dict):
            raise QueryError(f"{spec.endpoint.path} returned a non-object response")
        items = result.payload.get(spec.collection_key)
        if not isinstance(items, list):
            raise QueryError(
                f"{spec.endpoint.path} did not return collection {spec.collection_key!r}"
            )
        added = 0
        for item in items:
            identity = item_identity(item)
            if identity in seen_items:
                duplicates_removed += 1
                continue
            seen_items.add(identity)
            combined_items.append(item)
            added += 1
        pages_fetched += 1
        if not items:
            break
        if added == 0:
            truncated = True
            stalled = True
            break

    combined_payload[spec.collection_key] = combined_items
    combined_payload["paging"] = {
        "pageIndex": int(spec.parameters.get("p", "1")),
        "pageSize": page_size_value,
        "total": total,
        "pagesFetched": pages_fetched,
        "truncated": truncated,
        "duplicatesRemoved": duplicates_removed,
        "stalled": stalled,
    }
    return ExecutionResult(
        http=HttpResult(first.status, first.headers, combined_payload),
        pages_fetched=pages_fetched,
        truncated=truncated,
        duplicates_removed=duplicates_removed,
        stalled=stalled,
    )


def capabilities(
    endpoints: dict[str, Endpoint],
) -> list[dict[str, Any]]:
    result = []
    for command, path in sorted(COMMAND_ENDPOINTS.items()):
        endpoint = endpoints.get(path)
        result.append(
            {
                "command": command,
                "endpoint": path,
                "available": endpoint is not None and not endpoint.is_post,
                "method": "POST" if endpoint and endpoint.is_post else "GET",
                "deprecatedSince": endpoint.deprecated_since if endpoint else None,
                "since": endpoint.since if endpoint else None,
                "parameters": sorted(endpoint.parameters) if endpoint else [],
            }
        )
    return result


def token_expiration(headers: dict[str, str]) -> str | None:
    return headers.get("sonarqube-authentication-token-expiration")


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def query_envelope(
    args: argparse.Namespace,
    base_url: str,
    token: str | None,
    spec: QuerySpec,
    execution: ExecutionResult,
) -> dict[str, Any]:
    warnings: list[str] = []
    if spec.endpoint.deprecated_since:
        warnings.append(
            f"{spec.endpoint.path} reports deprecatedSince={spec.endpoint.deprecated_since}; "
            "prefer a documented v2 or native-tool replacement when available"
        )
    if execution.truncated:
        warnings.append(
            f"pagination stopped after {execution.pages_fetched} page(s); result is truncated"
        )
    if execution.duplicates_removed:
        warnings.append(
            f"removed {execution.duplicates_removed} duplicate item(s) returned across pages"
        )
    if execution.stalled:
        warnings.append("pagination stopped because a page produced no new items")
    return {
        "command": args.command,
        "baseUrl": base_url,
        "retrievedAt": utc_now(),
        "authentication": "bearer" if token else "anonymous",
        "endpoint": spec.endpoint.path,
        "parameters": spec.parameters,
        "httpStatus": execution.http.status,
        "pagesFetched": execution.pages_fetched,
        "truncated": execution.truncated,
        "duplicatesRemoved": execution.duplicates_removed,
        "stalled": execution.stalled,
        "deprecatedSince": spec.endpoint.deprecated_since,
        "tokenExpiration": token_expiration(execution.http.headers),
        "warnings": warnings,
        "result": execution.http.payload,
    }


def add_scope_arguments(parser: argparse.ArgumentParser) -> None:
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--branch")
    scope.add_argument("--pull-request")


def add_pagination_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--page", type=positive_int, default=1)
    parser.add_argument("--page-size", type=page_size, default=DEFAULT_PAGE_SIZE)
    parser.add_argument("--all-pages", action="store_true")
    parser.add_argument("--max-pages", type=positive_int, default=DEFAULT_MAX_PAGES)


def add_project_key(parser: argparse.ArgumentParser, *, required: bool = True) -> None:
    parser.add_argument("--project-key", required=required)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Query supported read-only SonarQube Web API v1 endpoints. "
            "Connection options must precede the subcommand."
        )
    )
    parser.add_argument("--base-url", default=os.environ.get("SONARQUBE_URL"))
    parser.add_argument("--token-env", default="SONARQUBE_TOKEN")
    parser.add_argument("--anonymous", action="store_true")
    parser.add_argument(
        "--organization",
        default=os.environ.get("SONARQUBE_ORGANIZATION"),
    )
    parser.add_argument("--timeout", type=positive_int, default=DEFAULT_TIMEOUT)

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("capabilities", help="Show supported live endpoints")
    subparsers.add_parser("server-status", help="Get server status")
    subparsers.add_parser("server-version", help="Get server version")

    projects = subparsers.add_parser("projects", help="Search accessible projects")
    projects.add_argument("--query")
    add_pagination_arguments(projects)

    project = subparsers.add_parser("project", help="Get one project component")
    add_project_key(project)
    add_scope_arguments(project)

    branches = subparsers.add_parser("branches", help="List analyzed branches")
    add_project_key(branches)

    pull_requests = subparsers.add_parser(
        "pull-requests",
        help="List analyzed pull requests",
    )
    add_project_key(pull_requests)

    quality_gate = subparsers.add_parser(
        "quality-gate",
        help="Get project quality-gate status",
    )
    add_project_key(quality_gate)
    add_scope_arguments(quality_gate)

    quality_gate_definition = subparsers.add_parser(
        "quality-gate-definition",
        help="Get the quality gate assigned to a project",
    )
    add_project_key(quality_gate_definition)

    subparsers.add_parser("quality-gates", help="List visible quality gates")

    measures = subparsers.add_parser("measures", help="Get project measures")
    add_project_key(measures)
    measures.add_argument("--metrics", required=True)
    add_scope_arguments(measures)

    issues = subparsers.add_parser("issues", help="Search project issues")
    add_project_key(issues)
    add_scope_arguments(issues)
    issues.add_argument("--resolved", choices=("true", "false"))
    issues.add_argument("--severities")
    issues.add_argument("--statuses")
    issues.add_argument("--types")
    issues.add_argument("--rules")
    add_pagination_arguments(issues)

    hotspots = subparsers.add_parser("hotspots", help="Search security hotspots")
    add_project_key(hotspots)
    add_scope_arguments(hotspots)
    hotspots.add_argument("--status")
    hotspots.add_argument("--resolution")
    add_pagination_arguments(hotspots)

    hotspot = subparsers.add_parser("hotspot", help="Get one security hotspot")
    hotspot.add_argument("--hotspot-key", required=True)

    analyses = subparsers.add_parser("analyses", help="Search project analyses")
    add_project_key(analyses)
    analyses.add_argument("--branch")
    analyses.add_argument("--from-date")
    analyses.add_argument("--to-date")
    add_pagination_arguments(analyses)

    quality_profiles = subparsers.add_parser(
        "quality-profiles",
        help="List quality profiles",
    )
    add_project_key(quality_profiles, required=False)
    quality_profiles.add_argument("--language")

    rule = subparsers.add_parser("rule", help="Get one rule")
    rule.add_argument("--rule-key", required=True)

    metrics = subparsers.add_parser("metrics", help="List metric definitions")
    add_pagination_arguments(metrics)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        base_url = normalize_base_url(args.base_url)
        token_environment = validate_env_name(args.token_env)
        token = None if args.anonymous else os.environ.get(token_environment)
        endpoints, discovery = discover_endpoints(
            base_url,
            token,
            args.timeout,
        )
        if args.command == "capabilities":
            output = {
                "command": "capabilities",
                "baseUrl": base_url,
                "retrievedAt": utc_now(),
                "authentication": "bearer" if token else "anonymous",
                "httpStatus": discovery.status,
                "tokenExpiration": token_expiration(discovery.headers),
                "endpoints": capabilities(endpoints),
            }
        else:
            spec = build_spec(args, endpoints)
            all_pages = bool(getattr(args, "all_pages", False))
            max_pages = int(getattr(args, "max_pages", DEFAULT_MAX_PAGES))
            execution = execute_spec(
                spec,
                base_url,
                token,
                args.timeout,
                all_pages=all_pages,
                max_pages=max_pages,
            )
            output = query_envelope(args, base_url, token, spec, execution)
        json.dump(output, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    except QueryError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    except BrokenPipeError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
