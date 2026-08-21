#!/usr/bin/env python3
"""Validate Backstage plugin structure and optional package-local checks."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


def load_package(package_dir: Path) -> dict:
    package_file = package_dir / "package.json"
    if not package_file.exists():
        raise FileNotFoundError(f"Missing package.json: {package_file}")
    return json.loads(package_file.read_text(encoding="utf-8"))


def has_any(package_dir: Path, candidates: list[str]) -> bool:
    return any((package_dir / candidate).exists() for candidate in candidates)


def run_if_present(
    package_dir: Path, package: dict, script_name: str
) -> tuple[str, bool, str, bool]:
    scripts = package.get("scripts", {})
    if script_name not in scripts:
        return script_name, True, "not run: package script is missing", False
    if shutil.which("yarn") is None:
        return script_name, False, "yarn is required for --run", True
    result = subprocess.run(
        ["yarn", script_name],
        cwd=package_dir,
        text=True,
        capture_output=True,
        check=False,
    )
    return script_name, result.returncode == 0, (result.stdout + result.stderr).strip()[-1200:], True


def detect_kind(package_dir: Path, package: dict) -> str:
    name = package.get("name", "")
    if name.endswith("-backend"):
        return "backend"
    if name.endswith("-node"):
        return "node"
    if name.endswith("-common"):
        return "common"
    if has_any(package_dir, ["src/plugin.ts", "src/plugin.tsx"]):
        return "frontend"
    return "unknown"


def source_text(package_dir: Path) -> str:
    sources: list[str] = []
    for suffix in ("*.ts", "*.tsx"):
        for path in sorted(package_dir.glob(f"src/**/{suffix}")):
            sources.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(sources)


def frontend_mode_check(mode: str, plugin_source: str) -> tuple[str, bool, str, bool]:
    has_new = "createFrontendPlugin" in plugin_source
    has_legacy = re.search(r"\bcreatePlugin\s*\(", plugin_source) is not None
    expected = {
        "new": has_new,
        "legacy": has_legacy,
        "dual": has_new and has_legacy,
    }
    detail = (
        f"mode={mode}; createFrontendPlugin={has_new}; "
        f"legacy createPlugin={has_legacy}"
    )
    return "frontend mode", expected[mode], detail, True


def is_backstage_core_root(package_dir: Path) -> bool:
    return all(
        path.exists()
        for path in (
            package_dir / ".changeset",
            package_dir / "packages/frontend-plugin-api",
            package_dir / "packages/backend-plugin-api",
            package_dir / "yarn.lock",
        )
    )


def run_pack(package_dir: Path) -> tuple[str, bool, str, bool]:
    if shutil.which("npm") is None:
        return "npm pack --dry-run", False, "npm is required for --pack", True
    result = subprocess.run(
        ["npm", "pack", "--dry-run"],
        cwd=package_dir,
        text=True,
        capture_output=True,
        check=False,
    )
    return (
        "npm pack --dry-run",
        result.returncode == 0,
        (result.stdout + result.stderr).strip()[-1200:],
        True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Backstage plugin package")
    parser.add_argument("plugin_dir")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["new", "legacy", "dual"],
        help="Explicit frontend compatibility mode.",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run available package-local yarn lint, tsc, test, and build scripts.",
    )
    parser.add_argument(
        "--pack",
        action="store_true",
        help="Run npm pack --dry-run after structural validation.",
    )
    args = parser.parse_args()

    package_dir = Path(args.plugin_dir).resolve()
    package = load_package(package_dir)
    kind = detect_kind(package_dir, package)
    checks: list[tuple[str, bool, str, bool]] = []

    checks.append(("package.json", True, "present", True))
    checks.append(("README.md", (package_dir / "README.md").exists(), "required for maintainability", True))
    checks.append(("src", (package_dir / "src").is_dir(), "source directory", True))
    checks.append(("catalog-info.yaml", (package_dir / "catalog-info.yaml").exists(), "recommended for cataloged packages", False))

    if kind == "backend":
        plugin_source = source_text(package_dir)
        checks.append(("createBackendPlugin", "createBackendPlugin" in plugin_source, "backend plugins should use the new backend system", True))
    elif kind == "frontend":
        checks.append(frontend_mode_check(args.mode, source_text(package_dir)))

    if (args.run or args.pack) and is_backstage_core_root(package_dir):
        checks.append(
            (
                "core root safety",
                False,
                "select a plugin package directory; root builds and package publication checks are not routine Backstage core validation",
                True,
            )
        )
    elif args.run:
        for script_name in ["lint", "tsc", "test", "build"]:
            checks.append(run_if_present(package_dir, package, script_name))
    if args.pack and not is_backstage_core_root(package_dir):
        checks.append(run_pack(package_dir))

    failed = False
    print(f"Backstage plugin validation: {package_dir}")
    print(f"Detected kind: {kind}")
    for name, ok, detail, required in checks:
        if ok:
            status = "PASS"
        elif required:
            status = "FAIL"
        else:
            status = "WARN"
        print(f"{status:4} {name}: {detail}")
        failed = failed or (required and not ok)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
