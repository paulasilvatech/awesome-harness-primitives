#!/usr/bin/env python3
"""Print a bounded, read-only .NET inventory as JSON, never configuration values.

Exit 0: selected text scan complete (not migration readiness).
Exit 1: incomplete scan, unresolved targets/references, or no project files.
Exit 2: invalid input, malformed build XML, or a filesystem failure.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from dotnet_common import InputError, framework_family, read_text

PROJECT_SUFFIXES = {".csproj", ".vbproj", ".fsproj"}
SOURCE_SUFFIXES = {".cs", ".vb", ".fs", ".aspx", ".ascx", ".asax", ".asmx", ".ashx", ".svc"}
WEB_FORMS_SUFFIXES = {".aspx", ".ascx", ".master"}
EXCLUDED_DIRS = {
    ".git", ".vs", ".idea", ".venv", "venv", "node_modules", "packages",
    "bin", "obj", "__pycache__", "testresults", ".nuget",
}
CONFIG_NAMES = {"web.config", "app.config", "packages.config", "global.json", "nuget.config"}
SIGNALS = {
    "system-web": r"\bSystem\.Web\b|<system\.web(?:>|\s)",
    "wcf-review": r"\bSystem\.ServiceModel\b|<system\.serviceModel(?:>|\s)",
    "remoting": r"\bSystem\.Runtime\.Remoting\b|\bAppDomain\.CreateDomain\b",
    "workflow-foundation": r"\bSystem\.Activities\b|\bSystem\.Workflow\b",
    "com-interop": r"\bComImport\b|<COMReference\b|\bSystem\.EnterpriseServices\b",
    "native-interop": r"\b(?:DllImport|LibraryImport|Declare\s+(?:Auto\s+|Ansi\s+|Unicode\s+)?Function)\b",
    "registry": r"\bMicrosoft\.Win32\b|\bRegistry(?:Key)?\.",
    "drawing-review": r"\bSystem\.Drawing\b",
    "windows-identity": r"\bWindowsIdentity\b|\bWindowsImpersonationContext\b|mode\s*=\s*[\"']Windows[\"']",
    "windows-desktop": r"<Use(?:WPF|WindowsForms)>\s*true\s*</|System\.Windows\.Forms",
    "windows-target": r"\bnet\d+(?:\.\d+)?-windows|\bwin(?:7|8|10|11)?-(?:x64|x86|arm64)\b",
    "localdb": r"\(localdb\)",
    "windows-path-review": r"[A-Za-z]:\\|\\\\[A-Za-z0-9_.-]+\\",
}
COMPILED_SIGNALS = {name: re.compile(pattern, re.IGNORECASE) for name, pattern in SIGNALS.items()}


def local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def parse_xml(text: str, relative_path: str) -> ET.Element:
    if re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", text, re.IGNORECASE):
        raise InputError(f"{relative_path}: XML declarations with DTD/entities are not accepted")
    try:
        return ET.fromstring(text)
    except ET.ParseError as error:
        raise InputError(f"{relative_path}: invalid XML (source content omitted)") from error


def declared_frameworks(document: ET.Element) -> tuple[list[str], bool]:
    frameworks: set[str] = set()
    unresolved = False
    for element in document.iter():
        name = local_name(element)
        if name not in {"TargetFramework", "TargetFrameworks", "TargetFrameworkVersion"}:
            continue
        for value in (element.text or "").split(";"):
            value = value.strip().lower()
            if name == "TargetFrameworkVersion" and re.fullmatch(r"v[1-4](?:\.\d+){1,2}", value):
                value = "net" + value[1:].replace(".", "")
            if framework_family(value) == "unknown":
                unresolved = True
            else:
                frameworks.add(value)
    return sorted(frameworks), unresolved


def project_inventory(
    path: Path, root: Path, document: ET.Element, warnings: list[dict[str, str]]
) -> dict[str, object]:
    relative = path.relative_to(root).as_posix()
    frameworks, unresolved = declared_frameworks(document)
    if not frameworks or unresolved:
        warnings.append({"path": relative, "reason": "effective target requires MSBuild evaluation"})
    references: set[str] = set()
    packages: set[str] = set()
    for element in document.iter():
        name = local_name(element)
        if name == "PackageReference":
            package = element.get("Include") or element.get("Update") or ""
            if re.fullmatch(r"[A-Za-z0-9_.-]+", package):
                packages.add(package)
        if name != "ProjectReference":
            continue
        include = (element.get("Include") or "").replace("\\", "/")
        if not include or "$(" in include or "@(" in include or "*" in include or re.match(r"^[A-Za-z]:", include):
            warnings.append({"path": relative, "reason": "unresolved or absolute Windows project reference"})
            continue
        candidate = path.parent / include
        resolved = candidate.resolve()
        if candidate.is_symlink() or not resolved.is_relative_to(root):
            warnings.append({"path": relative, "reason": "linked or external project reference was not followed"})
            continue
        references.add(resolved.relative_to(root).as_posix())
        if not resolved.is_file():
            warnings.append({"path": relative, "reason": "project reference does not exist"})
    return {
        "path": relative,
        "sdk_style": bool(document.get("Sdk")) or any(local_name(item) == "Sdk" for item in document),
        "declared_frameworks": frameworks,
        "framework_families": sorted({framework_family(tfm) for tfm in frameworks}),
        "contains_conditions": any("Condition" in item.attrib for item in document.iter()),
        "explicit_imports": sum(local_name(item) == "Import" for item in document.iter()),
        "requires_msbuild_evaluation": True,
        "package_references": sorted(packages),
        "project_references": sorted(references),
    }


def selected_file(path: Path) -> bool:
    name = path.name.lower()
    return (
        path.suffix.lower() in PROJECT_SUFFIXES | SOURCE_SUFFIXES | WEB_FORMS_SUFFIXES | {".props", ".targets"}
        or name in CONFIG_NAMES
        or name.startswith("dockerfile")
        or name.endswith(".dockerfile")
    )


def fail_walk(error: OSError) -> None:
    raise InputError(f"cannot traverse input directory: {error.strerror}") from error


def inventory(root: Path, max_bytes: int = 1024 * 1024, exclude_dirs: tuple[str, ...] = ()) -> dict[str, object]:
    root = root.resolve()
    if not root.is_dir():
        raise InputError("root must be an existing directory")
    if max_bytes < 1:
        raise InputError("max-file-bytes must be positive")
    for name in exclude_dirs:
        if not name or "/" in name or "\\" in name or name in {".", ".."}:
            raise InputError("exclude-dir must be a directory basename")
    exclusions = EXCLUDED_DIRS | {name.lower() for name in exclude_dirs}
    projects: list[dict[str, object]] = []
    signals: list[dict[str, object]] = []
    warnings: list[dict[str, str]] = []
    shared_build: list[dict[str, object]] = []
    package_configs: list[dict[str, object]] = []
    solutions: list[str] = []
    configuration_files: list[str] = []
    container_files: list[str] = []
    scanned_files = 0
    for folder, directories, files in os.walk(root, topdown=True, followlinks=False, onerror=fail_walk):
        parent = Path(folder)
        kept: list[str] = []
        for name in sorted(directories):
            candidate = parent / name
            if name.lower() in exclusions:
                continue
            if candidate.is_symlink() or not candidate.resolve().is_relative_to(root):
                warnings.append({"path": candidate.relative_to(root).as_posix(), "reason": "linked directory was not followed"})
            else:
                kept.append(name)
        directories[:] = kept
        for name in sorted(files):
            path = parent / name
            relative = path.relative_to(root).as_posix()
            suffix = path.suffix.lower()
            if suffix not in {".sln", ".slnx"} and not selected_file(path):
                continue
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                warnings.append({"path": relative, "reason": "linked file was not read"})
                continue
            if suffix in {".sln", ".slnx"}:
                solutions.append(relative)
                continue
            try:
                text = read_text(path, max_bytes)
            except InputError as error:
                warnings.append({"path": relative, "reason": str(error)})
                continue
            scanned_files += 1
            lowered = name.lower()
            if suffix in PROJECT_SUFFIXES:
                projects.append(project_inventory(path, root, parse_xml(text, relative), warnings))
            elif suffix in {".props", ".targets"}:
                document = parse_xml(text, relative)
                frameworks, unresolved = declared_frameworks(document)
                shared_build.append({
                    "path": relative, "declared_frameworks": frameworks,
                    "has_unresolved_targets": unresolved, "evaluated": False,
                })
            elif lowered == "packages.config":
                document = parse_xml(text, relative)
                packages = sorted({
                    item.get("id", "") for item in document.iter()
                    if local_name(item) == "package" and re.fullmatch(r"[A-Za-z0-9_.-]+", item.get("id", ""))
                })
                package_configs.append({"path": relative, "package_ids": packages})
            if lowered in CONFIG_NAMES:
                configuration_files.append(relative)
            if lowered.startswith("dockerfile") or lowered.endswith(".dockerfile"):
                container_files.append(relative)
            if suffix in WEB_FORMS_SUFFIXES:
                signals.append({"path": relative, "line": 1, "signal": "web-forms", "confidence": "heuristic"})
            for signal, pattern in COMPILED_SIGNALS.items():
                match = pattern.search(text)
                if match:
                    signals.append({
                        "path": relative, "line": text.count("\n", 0, match.start()) + 1,
                        "signal": signal, "confidence": "heuristic",
                    })
    if not projects:
        warnings.append({"path": ".", "reason": "no project files found; Web Site or other layouts require manual assessment"})
    return {
        "schema_version": 1,
        "status": "inventory-incomplete" if warnings else "inventory-complete",
        "root": str(root),
        "solutions": solutions,
        "projects": projects,
        "shared_build_files": shared_build,
        "package_configs": package_configs,
        "configuration_files": configuration_files,
        "container_files": container_files,
        "signals": signals,
        "coverage": {
            "scanned_files": scanned_files,
            "excluded_directory_names": sorted(exclusions),
            "warnings": warnings,
        },
        "limitations": [
            "Literal declarations only; MSBuild properties, imports and conditions are not evaluated.",
            "Package versions, transitive/native dependencies and source reachability are not resolved.",
            "Only selected file types are scanned; .gitignore is not interpreted.",
            "Signals can match comments and are not confirmed blockers.",
            "No build, runtime, hosting, support-lifecycle or deployment readiness is certified.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="application root to inspect; never modified")
    parser.add_argument("--max-file-bytes", type=int, default=1024 * 1024, help="maximum bytes per selected text file")
    parser.add_argument("--exclude-dir", action="append", default=[], help="additional directory basename to exclude")
    args = parser.parse_args(argv)
    try:
        report = inventory(args.root, args.max_file_bytes, tuple(args.exclude_dir))
    except (InputError, OSError) as error:
        message = error.strerror if isinstance(error, OSError) else str(error)
        print(f"Inventory error: {message}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "inventory-complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
