#!/usr/bin/env python3
"""Validate SIFAP REQ-NNN declarations and source_legacy evidence."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REQ_PATTERN = re.compile(
    r"^(?:#{1,6}\s+|[-*]\s+(?:\*\*)?)?(REQ-\d{3})\b"
)
LINE_ANCHOR_PATTERN = re.compile(r"#L\d+(?:-L\d+)?$")
PLACEHOLDER_PATTERN = re.compile(
    r"<[^>]+>|\b(?:TODO|TBD|PLACEHOLDER)\b",
    re.IGNORECASE,
)
ALLOWED_PREFIXES = (
    "01-archaeology/legacy-sifap/natural-programs/",
    "01-archaeology/legacy-sifap/adabas-ddms/",
)
ALLOWED_EXTENSIONS = {
    ".NSP", ".NSN", ".NSS", ".NSA", ".NSL", ".NSC", ".NSM", ".jcl",
    ".NSD", ".ddm", ".txt",
}


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    message: str


def markdown_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix.lower() == ".md" else []
    if target.is_dir():
        return sorted(target.rglob("*.md"))
    return []


def source_value(
    lines: list[str], declaration_index: int
) -> tuple[int, str] | None:
    stop = min(len(lines), declaration_index + 21)
    for index in range(declaration_index + 1, stop):
        candidate = lines[index].strip()
        if candidate.startswith(("- ", "* ")):
            candidate = candidate[2:].lstrip()
        if not candidate.startswith("source_legacy:"):
            continue
        value = candidate.removeprefix("source_legacy:").strip()
        if value:
            return index, value.strip('"').strip("'")
    return None


def validate_source(
    root: Path, path: Path, line: int, value: str
) -> list[Finding]:
    if value.startswith("[GREENFIELD]"):
        justification = value.removeprefix("[GREENFIELD]").strip()
        if not justification or PLACEHOLDER_PATTERN.search(justification):
            return [
                Finding(
                    path,
                    line,
                    "[GREENFIELD] requires a concrete non-placeholder "
                    "justification",
                )
            ]
        return []

    if PLACEHOLDER_PATTERN.search(value):
        return [Finding(path, line, "source_legacy contains a placeholder")]

    source_path = LINE_ANCHOR_PATTERN.sub("", value)
    if not source_path.startswith(ALLOWED_PREFIXES):
        return [
            Finding(
                path,
                line,
                "source_legacy is outside the approved SIFAP legacy "
                "directories",
            )
        ]

    extension = Path(source_path).suffix
    if extension not in ALLOWED_EXTENSIONS:
        message = (
            "source_legacy extension is not allowed: "
            f"{extension or '<none>'}"
        )
        return [Finding(path, line, message)]

    candidate = (root / source_path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return [
            Finding(path, line, "source_legacy escapes the repository root")
        ]
    if not candidate.is_file():
        message = f"source_legacy file does not exist: {source_path}"
        return [Finding(path, line, message)]
    return []


def validate_file(
    root: Path,
    path: Path,
    seen: dict[str, tuple[Path, int]],
) -> list[Finding]:
    lines = path.read_text(encoding="utf-8").splitlines()
    findings: list[Finding] = []
    for index, text in enumerate(lines):
        match = REQ_PATTERN.match(text.strip())
        if not match:
            continue
        req_id = match.group(1)
        if req_id in seen:
            first_path, first_line = seen[req_id]
            message = (
                f"duplicate {req_id}; first declared at "
                f"{first_path}:{first_line}"
            )
            findings.append(Finding(path, index + 1, message))
        else:
            seen[req_id] = (path, index + 1)

        source = source_value(lines, index)
        if source is None:
            message = f"{req_id} has no source_legacy within 20 lines"
            findings.append(Finding(path, index + 1, message))
            continue
        source_index, value = source
        findings.extend(validate_source(root, path, source_index + 1, value))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        required=True,
        help="target repository root",
    )
    parser.add_argument(
        "--path",
        type=Path,
        help="spec file or directory; defaults to <root>/specs",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"repository root does not exist: {root}")
    target = args.path or (root / "specs")
    if not target.is_absolute():
        target = root / target
    files = markdown_files(target.resolve())
    if not files:
        print(
            f"No Markdown specifications found under {target}",
            file=sys.stderr,
        )
        return 2

    seen: dict[str, tuple[Path, int]] = {}
    findings: list[Finding] = []
    for path in files:
        findings.extend(validate_file(root, path, seen))

    if findings:
        for finding in findings:
            try:
                display = finding.path.resolve().relative_to(root)
            except ValueError:
                display = finding.path
            print(f"{display}:{finding.line}: {finding.message}")
        return 1

    print(f"OK: {len(seen)} requirements across {len(files)} Markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
