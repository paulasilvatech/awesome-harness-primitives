#!/usr/bin/env python3
"""Check one HTTP image's metadata and declared ports against a hosting target.

Consumes saved image-inspection JSON; no engine, network, or Azure calls.
Exit 0 means platform-consistent only, 1 means incompatible, 2 means invalid input.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from dotnet_common import InputError, framework_family, read_json

TARGETS = ("appservice-windows", "appservice-linux", "aca")
VERIFIED_ON = "2026-09-15"
WINDOWS_BASE_BUILDS = {"17763": "ltsc2019", "20348": "ltsc2022"}
SOURCES = {
    "appservice-windows": "https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container",
    "appservice-linux": "https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container",
    "aca": "https://learn.microsoft.com/en-us/azure/container-apps/containers",
}


def port(value: str) -> int:
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("port must be an integer") from error
    if not 1 <= number <= 65535:
        raise argparse.ArgumentTypeError("port must be between 1 and 65535")
    return number


def image_metadata(document: object) -> tuple[str, str, str]:
    if isinstance(document, list):
        if len(document) != 1:
            raise InputError("provide exactly one inspected image, not a manifest index or multiple images")
        document = document[0]
    if not isinstance(document, dict):
        raise InputError("image inspection must be an object or a one-object array")
    image_os = document.get("Os")
    architecture = document.get("Architecture")
    if not isinstance(image_os, str) or image_os not in {"windows", "linux"}:
        raise InputError("image inspection requires Os equal to windows or linux")
    if not isinstance(architecture, str) or not re.fullmatch(r"[a-z0-9_]+", architecture):
        raise InputError("image inspection requires an Architecture string")
    os_version = document.get("OsVersion", "")
    if not isinstance(os_version, str):
        raise InputError("OsVersion must be a string")
    if image_os == "windows" and not re.fullmatch(r"10\.0\.\d+\.\d+", os_version):
        raise InputError("Windows inspection requires an actual OsVersion such as 10.0.20348.0")
    return image_os, architecture, os_version


def validate(
    document: object, target: str, framework: str, listen_port: int, target_port: int
) -> dict[str, object]:
    if target not in TARGETS:
        raise InputError("unknown target")
    if framework_family(framework) == "unknown":
        raise InputError("framework must be one literal, recognized application TFM")
    if any(type(value) is not int or not 1 <= value <= 65535 for value in (listen_port, target_port)):
        raise InputError("ports must be integers between 1 and 65535")
    image_os, architecture, os_version = image_metadata(document)
    problems: list[str] = []
    expected_os = "windows" if target == "appservice-windows" else "linux"
    if image_os != expected_os:
        problems.append(f"{target} requires a {expected_os} image")
    if architecture != "amd64":
        problems.append("this verified hosting profile requires amd64; reverify before choosing another architecture")
    family = framework_family(framework)
    if family == "net-standard":
        problems.append(".NET Standard is a library target, not a deployable application")
    if expected_os == "linux" and (family == "net-framework" or "-" in framework):
        problems.append("Linux requires a modern .NET/.NET Core application without a platform-specific TFM")
    if expected_os == "windows" and "-" in framework and not framework.split("-", 1)[1].startswith("windows"):
        problems.append("the platform-qualified TFM does not target Windows")
    if target == "appservice-windows" and image_os == "windows":
        build = os_version.split(".")[2]
        if build == "26100":
            problems.append("Windows Server 2025 base images are not supported by the verified App Service policy")
        elif build not in WINDOWS_BASE_BUILDS:
            problems.append("Windows base is outside the verified LTSC 2019/2022 set; reverify official support")
        if framework == "net481" and build == "17763":
            problems.append("the verified .NET Framework 4.8.1 image uses LTSC 2022, not LTSC 2019")
    if listen_port != target_port:
        problems.append("declared listening port and configured platform target port differ")
    return {
        "schema_version": 1,
        "status": "incompatible" if problems else "platform-consistent",
        "target": target,
        "framework": framework,
        "image": {"os": image_os, "architecture": architecture, "os_version": os_version},
        "ports": {"declared_listener": listen_port, "configured_target": target_port},
        "policy": {"verified_on": VERIFIED_ON, "source": SOURCES[target]},
        "problems": problems,
        "unchecked": [
            "Freshness of service policy, regional/SKU availability and quota.",
            "Actual image runtime contents, .NET/OS support lifecycle and Windows host compatibility.",
            "Actual listening address/port, health probes, startup and application behavior.",
            "Sidecar/worker/job topology, identity, registry pull, network and state.",
            "Image provenance/digest, vulnerabilities, deployment authorization and rollback.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image-inspect", required=True, type=Path, help="saved inspection JSON for exactly one image")
    parser.add_argument("--target", required=True, choices=TARGETS)
    parser.add_argument("--framework", required=True, help="selected entry project's literal TFM, such as net481 or net10.0")
    parser.add_argument("--listen-port", required=True, type=port, help="declared application listening port")
    parser.add_argument("--target-port", required=True, type=port, help="configured container target port, not public HTTPS port")
    args = parser.parse_args(argv)
    try:
        result = validate(read_json(args.image_inspect), args.target, args.framework, args.listen_port, args.target_port)
    except (InputError, OSError) as error:
        message = error.strerror if isinstance(error, OSError) else str(error)
        print(f"Target validation error: {message}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "platform-consistent" else 1


if __name__ == "__main__":
    raise SystemExit(main())
