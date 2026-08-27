#!/usr/bin/env python3
"""Validate the bundled AEG OpenAPI operation and identity boundaries."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

CONTRACT = Path(__file__).resolve().parents[1] / "assets/openapi-aeg.json"
EXPECTED_OPERATIONS = {
    "aeg_start_run": True,
    "aeg_list_runs": False,
    "aeg_get_run": False,
    "aeg_get_gate_package": False,
    "aeg_decide_gate": True,
    "aeg_get_traceability": False,
    "aeg_get_metrics": False,
    "aeg_propose_profile": True,
}
FORBIDDEN_REQUEST_FIELDS = {
    "initiated_by",
    "decided_by",
    "proposed_by",
    "actor_id",
    "roles",
    "tenant_id",
}


def operation_map(document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    operations: dict[str, dict[str, Any]] = {}
    for path_item in document.get("paths", {}).values():
        if not isinstance(path_item, dict):
            continue
        for operation in path_item.values():
            if not isinstance(operation, dict):
                continue
            operation_id = operation.get("operationId")
            if isinstance(operation_id, str):
                operations[operation_id] = operation
    return operations


def collect_property_names(value: Any) -> set[str]:
    names: set[str] = set()
    if isinstance(value, dict):
        properties = value.get("properties")
        if isinstance(properties, dict):
            names.update(str(name) for name in properties)
        for nested in value.values():
            names.update(collect_property_names(nested))
    elif isinstance(value, list):
        for nested in value:
            names.update(collect_property_names(nested))
    return names


def validate(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("openapi") != "3.0.3":
        errors.append("openapi must be 3.0.3")
    if document.get("security") != [{"bearerAuth": []}]:
        errors.append("root bearerAuth security is required")

    operations = operation_map(document)
    if set(operations) != set(EXPECTED_OPERATIONS):
        errors.append(
            "operation IDs differ: expected "
            f"{sorted(EXPECTED_OPERATIONS)}, got {sorted(operations)}"
        )
    for operation_id, mutating in EXPECTED_OPERATIONS.items():
        operation = operations.get(operation_id, {})
        if operation.get("x-open-horizons-mutating") is not mutating:
            errors.append(
                f"{operation_id} has incorrect mutation classification"
            )

    components = document.get("components", {})
    schema_names = collect_property_names(components.get("schemas", {}))
    forbidden = sorted(schema_names & FORBIDDEN_REQUEST_FIELDS)
    if forbidden:
        errors.append(
            f"model-controlled actor fields are forbidden: {forbidden}"
        )

    request_schemas = components.get("schemas", {})
    start = request_schemas.get("StartRunRequest", {})
    worker = start.get("properties", {}).get("worker_engine", {})
    if worker.get("default") != "inherit":
        errors.append("worker_engine must default to inherit")
    proposal = request_schemas.get("ProposeProfileRequest", {})
    evidence = proposal.get("properties", {}).get("evidence_runs", {})
    if evidence.get("minItems") != 2:
        errors.append("profile proposals require at least two evidence runs")
    return errors


def main() -> int:
    try:
        document = json.loads(CONTRACT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"AEG contract validation failed: {exc}", file=sys.stderr)
        return 2
    errors = validate(document)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(EXPECTED_OPERATIONS)} AEG operations validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
