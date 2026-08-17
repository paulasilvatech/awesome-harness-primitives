#!/usr/bin/env python3
"""Validate basic Backstage plugin package structure."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def load_package(package_dir: Path) -> dict:
    package_file = package_dir / "package.json"
    if not package_file.exists():
        raise FileNotFoundError(f"Missing package.json: {package_file}")
    return json.loads(package_file.read_text(encoding="utf-8"))


def has_any(package_dir: Path, candidates: list[str]) -> bool:
    return any((package_dir / candidate).exists() for candidate in candidates)


def run_if_present(package_dir: Path, script_name: str) -> tuple[str, bool, str, bool]:
    package = load_package(package_dir)
    scripts = package.get("scripts", {})
    if script_name not in scripts:
        return script_name, True, "skipped, script missing", False
    result = subprocess.run(["yarn", script_name], cwd=package_dir, text=True, capture_output=True)
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Backstage plugin package")
    parser.add_argument("plugin_dir")
    parser.add_argument("--run", action="store_true", help="Run available yarn lint, tsc, test, and build scripts")
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
        plugin_source = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in package_dir.glob("src/**/*.ts"))
        checks.append(("createBackendPlugin", "createBackendPlugin" in plugin_source, "backend plugins should use the new backend system", True))
    elif kind == "frontend":
        plugin_source = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in package_dir.glob("src/**/*.ts*"))
        checks.append(("frontend plugin API", "createFrontendPlugin" in plugin_source or "createPlugin" in plugin_source, "frontend plugin entry point", True))

    if args.run:
        for script_name in ["lint", "tsc", "test", "build"]:
            checks.append(run_if_present(package_dir, script_name))

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
