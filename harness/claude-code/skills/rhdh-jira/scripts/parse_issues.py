#!/usr/bin/env python3
"""Flatten, enrich, and filter acli Jira JSON output.

Core problem: acli search --json returns only basic fields. Custom fields
(team, story points, size, sprint) are rejected by --fields. This script
bridges the gap by enriching search results via acli view, then flattening
deeply nested JSON into clean output.

Usage:
  # Flatten piped JSON (no enrichment - works with whatever fields are present)
  acli jira workitem search --jql "project = RHIDP" --json | python parse_issues.py

  # Enrich piped search results with full custom fields (calls acli view per issue)
  acli jira workitem search --jql "project = RHIDP" --limit 20 --json | python parse_issues.py --enrich

  # Flatten a single issue
  acli jira workitem view RHIDP-123 --fields "*all" --json | python parse_issues.py

  # Select specific fields
  acli jira workitem search --jql "..." --json | python parse_issues.py --enrich -s key,summary,team,story_points

  # Filter by team (the #1 use case - team is not JQL-filterable)
  acli jira workitem search --jql "..." --json | python parse_issues.py --enrich -f team="RHDH Install"

  # CSV export
  acli jira workitem search --jql "..." --json | python parse_issues.py -s key,summary,status --csv
"""

import argparse
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Field extractors: map friendly names → extraction logic
# ---------------------------------------------------------------------------


def _f(issue, field, default=None):
    """Get field from issue.fields or top-level."""
    return issue.get("fields", {}).get(field, issue.get(field, default))


def _name(issue, field):
    """Get .name from a nested object field."""
    val = _f(issue, field)
    if isinstance(val, dict):
        return val.get("name", val.get("displayName", val.get("value", "")))
    return val if val is not None else ""


def _sprint_name(issue):
    """Extract active/future sprint name from sprint array."""
    sprints = _f(issue, "customfield_10020", [])
    if not sprints:
        return ""
    for state in ("active", "future"):
        for s in sprints:
            if isinstance(s, dict) and s.get("state") == state:
                return s.get("name", "")
    if isinstance(sprints[-1], dict):
        return sprints[-1].get("name", "")
    return ""


def _list_names(issue, field):
    """Join .name values from a list of objects."""
    items = _f(issue, field, [])
    return ", ".join(i.get("name", "") for i in items if isinstance(i, dict)) if items else ""


def _adf_to_text(issue):
    """Extract plain text from ADF description."""
    desc = _f(issue, "description")
    if desc is None:
        return ""
    if isinstance(desc, str):
        return desc
    if isinstance(desc, dict):
        parts = []
        _walk_adf(desc, parts)
        return " ".join(parts).strip()
    return str(desc)


def _walk_adf(node, parts):
    if isinstance(node, dict):
        if node.get("type") == "text":
            text = node.get("text", "")
            if text:
                parts.append(text)
        for child in node.get("content", []):
            _walk_adf(child, parts)
    elif isinstance(node, list):
        for child in node:
            _walk_adf(child, parts)


FIELDS = {
    # Core
    "key": lambda i: i.get("key", ""),
    "summary": lambda i: _f(i, "summary", ""),
    "status": lambda i: _name(i, "status"),
    "assignee": lambda i: _name(i, "assignee"),
    "assignee_email": lambda i: (
        _f(i, "assignee", {}).get("emailAddress", "") if isinstance(_f(i, "assignee"), dict) else ""
    ),
    "reporter": lambda i: _name(i, "reporter"),
    "issuetype": lambda i: _name(i, "issuetype"),
    "priority": lambda i: _name(i, "priority"),
    "project": lambda i: (
        _f(i, "project", {}).get("key", "")
        if isinstance(_f(i, "project"), dict)
        else str(_f(i, "project", ""))
    ),
    "created": lambda i: _f(i, "created", ""),
    "updated": lambda i: _f(i, "updated", ""),
    # Custom
    "team": lambda i: _name(i, "customfield_10001"),
    "story_points": lambda i: _f(i, "customfield_10028"),
    "size": lambda i: _name(i, "customfield_10795"),
    "sprint": _sprint_name,
    "parent": lambda i: (
        _f(i, "parent", {}).get("key", "") if isinstance(_f(i, "parent"), dict) else ""
    ),
    "rn_type": lambda i: _name(i, "customfield_10785"),
    "fix_versions": lambda i: _list_names(i, "fixVersions"),
    "components": lambda i: _list_names(i, "components"),
    "labels": lambda i: ", ".join(_f(i, "labels", [])),
    "description": _adf_to_text,
    "security": lambda i: _name(i, "security"),
    "feature_status": lambda i: _name(i, "customfield_10807"),
    "link_count": lambda i: len(_f(i, "issuelinks", [])),
}

DEFAULT_SELECT = ["key", "issuetype", "status", "assignee", "priority", "summary"]
ENRICHED_SELECT = [
    "key",
    "issuetype",
    "status",
    "assignee",
    "team",
    "story_points",
    "sprint",
    "summary",
]


# ---------------------------------------------------------------------------
# Enrichment: fetch full fields via acli view
# ---------------------------------------------------------------------------


def find_acli():
    """Find acli on PATH or common locations."""
    path = shutil.which("acli")
    if path:
        return path
    if sys.platform == "win32":
        candidate = Path.home() / ".path" / "acli.exe"
        if candidate.exists():
            return str(candidate)
    return None


def enrich(issues, acli_path):
    """Fetch full field data for each issue via acli view."""
    enriched = []
    total = len(issues)
    for idx, issue in enumerate(issues, 1):
        key = issue.get("key", "")
        if not key:
            continue
        print(f"\r  Enriching {idx}/{total}: {key}...", end="", file=sys.stderr)
        try:
            result = subprocess.run(
                [acli_path, "jira", "workitem", "view", key, "--fields", "*all", "--json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=15,
            )
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                enriched.append(data[0] if isinstance(data, list) else data)
            else:
                enriched.append(issue)
                print(" [failed]", file=sys.stderr)
        except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
            enriched.append(issue)
    print(file=sys.stderr)  # newline after progress
    return enriched


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------


def apply_filters(issues, filters):
    """Filter issues by field=value pairs. Case-insensitive matching."""
    for filt in filters:
        if "=" not in filt:
            print(f"Warning: invalid filter '{filt}', use field=value", file=sys.stderr)
            continue
        field, value = filt.split("=", 1)
        field, value = field.strip(), value.strip().strip('"').strip("'").lower()
        extractor = FIELDS.get(field)
        if extractor:
            issues = [i for i in issues if str(extractor(i)).lower() == value]
        else:
            issues = [i for i in issues if str(_f(i, field, "")).lower() == value]
    return issues


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def flatten(issue, fields):
    """Extract fields into a flat dict."""
    row = {}
    for f in fields:
        ext = FIELDS.get(f)
        val = ext(issue) if ext else _f(issue, f, "")
        row[f] = val if val is not None else ""
    return row


def out_table(rows, fields):
    if not rows:
        print("No issues found.")
        return
    widths = {}
    for f in fields:
        col_vals = [str(r.get(f, "")) for r in rows]
        widths[f] = min(max(len(f), max((len(v) for v in col_vals), default=0)), 60)
    print(" | ".join(f.ljust(widths[f]) for f in fields))
    print("-+-".join("-" * widths[f] for f in fields))
    for row in rows:
        print(" | ".join(str(row.get(f, ""))[: widths[f]].ljust(widths[f]) for f in fields))


def out_csv(rows, fields):
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Flatten, enrich, and filter acli Jira JSON output.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Fields: " + ", ".join(sorted(FIELDS.keys())),
    )
    parser.add_argument(
        "--enrich",
        action="store_true",
        help="Fetch full custom fields via acli view per issue (slower, but gets team/points/sprint)",
    )
    parser.add_argument(
        "-s",
        "--select",
        help="Comma-separated fields to output (default changes based on --enrich)",
    )
    parser.add_argument(
        "-f",
        "--filter",
        action="append",
        default=[],
        help='Filter by field=value, e.g. -f team="RHDH Install". Repeatable.',
    )
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--csv", action="store_true", help="CSV output")
    parser.add_argument(
        "--list-fields",
        action="store_true",
        help="List available field names",
    )
    args = parser.parse_args()

    if args.list_fields:
        for name in sorted(FIELDS.keys()):
            print(f"  {name}")
        sys.exit(0)

    if sys.stdin.isatty():
        print("Error: pipe JSON from acli to stdin.", file=sys.stderr)
        print(
            '  acli jira workitem search --jql "..." --json | python parse_issues.py',
            file=sys.stderr,
        )
        sys.exit(2)

    issues = json.load(sys.stdin)
    if not isinstance(issues, list):
        issues = [issues]

    if args.enrich:
        acli_path = find_acli()
        if not acli_path:
            print("Error: acli not found (required for --enrich)", file=sys.stderr)
            sys.exit(2)
        issues = enrich(issues, acli_path)

    if args.filter:
        issues = apply_filters(issues, args.filter)

    fields = (
        [f.strip() for f in args.select.split(",")]
        if args.select
        else ENRICHED_SELECT
        if args.enrich
        else DEFAULT_SELECT
    )

    rows = [flatten(issue, fields) for issue in issues]

    if args.json:
        json.dump(rows, sys.stdout, indent=2, default=str)
        print()
    elif args.csv:
        out_csv(rows, fields)
    elif sys.stdout.isatty():
        out_table(rows, fields)
    else:
        json.dump(rows, sys.stdout, indent=2, default=str)
        print()


if __name__ == "__main__":
    main()
