# Migration Report

Post-migration report generator for the `pipeline-migration` skill. Produces a markdown summary of all migrated pipelines with Fabric portal links, activity counts, parked activity blockers, and validation status.

---

## Fabric Portal URL Patterns

| Item | URL Pattern |
|---|---|
| DataPipeline | `https://app.fabric.microsoft.com/groups/{workspaceId}/datapipelines/{itemId}` |
| Notebook | `https://app.fabric.microsoft.com/groups/{workspaceId}/synapsenotebooks/{itemId}` |
| Variable Library | `https://app.fabric.microsoft.com/groups/{workspaceId}/variablelibraries/{itemId}` |
| Workspace | `https://app.fabric.microsoft.com/groups/{workspaceId}` |

---

## Report Generator Script

```python
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

PARKED_ACTIVITY_TYPES = {
    "DatabricksNotebook",
    "DatabricksSparkJar",
    "DatabricksSparkPython",
    "ExecuteSSISPackage",
    "AzureBatch",
    "Custom",
    "MapReduce",
    "Pig",
    "Hive",
}

MIGRATED_ACTIVITY_TYPES = {
    "SynapseNotebook": "TridentNotebook",
    "Validation": "GetMetadata+IfCondition",
    "AzureFunctionActivity": "WebActivity",
    "HDInsightSpark": "TridentNotebook or SparkJobDefinition",
    "AzureMLBatchExecution": "WebActivity",
    "AzureMLUpdateResource": "WebActivity",
}


@dataclass
class PipelineMigrationRecord:
    synapse_name: str
    fabric_pipeline_id: Optional[str] = None
    fabric_workspace_id: Optional[str] = None
    source_activity_types: list[str] = field(default_factory=list)
    migrated_activities: list[dict] = field(default_factory=list)   # {from_type, to_type} — see analyze_synapse_pipeline()
    parked_activities: list[dict] = field(default_factory=list)     # {type, reason}        — see analyze_synapse_pipeline()
    validation_passed: Optional[bool] = None
    validation_run_status: Optional[str] = None
    # Migration errors (Phase 4/5) — drive the "❌ Migration errors" summary count.
    errors: list[str] = field(default_factory=list)
    # Validation errors (Phase 6) — kept separate so a validation failure does NOT
    # get miscounted as a migration error in the summary. `validation_passed=False`
    # already drives the "❌ Validation failed" row class; this list carries the
    # human-readable details for the "Validation Errors" section of the report.
    validation_errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def fabric_url(self) -> Optional[str]:
        if self.fabric_pipeline_id and self.fabric_workspace_id:
            return (f"https://app.fabric.microsoft.com/groups/{self.fabric_workspace_id}"
                    f"/datapipelines/{self.fabric_pipeline_id}")
        return None

    @property
    def status_emoji(self) -> str:
        # Order matters: hard errors and explicit validation failure outrank
        # parked-only state, which in turn outranks 'passed'. `validation_passed
        # is False` (explicit failure) must NOT be conflated with None (not yet
        # validated) — `not self.validation_passed` is true for both and would
        # mislabel a failed pipeline as ⏳.
        if self.errors or self.validation_passed is False:
            return "❌"
        if self.parked_activities:
            return "⚠️"
        if self.validation_passed:
            return "✅"
        return "⏳"


def collect_activity_types(activities: list, result: set = None) -> set:
    """Recursively collect all activity types from a pipeline's activity tree."""
    if result is None:
        result = set()
    if not isinstance(activities, list):
        return result
    for activity in activities:
        if not isinstance(activity, dict):
            continue
        # Use a non-null fallback so the set never contains None
        # (which would later break sorted()).
        result.add(activity.get("type") or "Unknown")
        tp = activity.get("typeProperties") or {}
        if not isinstance(tp, dict):
            continue
        for key in ("activities", "ifTrueActivities", "ifFalseActivities", "defaultActivities"):
            inner = tp.get(key)
            if isinstance(inner, list):
                collect_activity_types(inner, result)
        for case in tp.get("cases", []) or []:
            if isinstance(case, dict):
                collect_activity_types(case.get("activities", []), result)
    return result


def analyze_synapse_pipeline(pipeline_def: dict) -> dict:
    """Analyze a Synapse pipeline definition and return activity summary."""
    activities = pipeline_def.get("properties", {}).get("activities", [])
    all_types = collect_activity_types(activities)
    
    migrated = []
    parked = []
    
    for activity_type in all_types:
        if activity_type in PARKED_ACTIVITY_TYPES:
            parked.append({
                "type": activity_type,
                "reason": "No Fabric equivalent — see pipeline-gotchas.md"
            })
        elif activity_type in MIGRATED_ACTIVITY_TYPES:
            migrated.append({
                "from_type": activity_type,
                "to_type": MIGRATED_ACTIVITY_TYPES[activity_type]
            })
    
    return {
        "all_activity_types": sorted(all_types),
        "migrated_activities": migrated,
        "parked_activities": parked
    }


def generate_markdown_report(
    records: list[PipelineMigrationRecord],
    fabric_workspace_id: str,
    variable_library_id: Optional[str],
    synapse_workspace_name: str,
    migration_date: Optional[str] = None
) -> str:
    if migration_date is None:
        migration_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    
    total = len(records)
    # Disjoint categories — each record falls into exactly one bucket so the
    # counts always sum to total and "Not yet validated" cannot go negative.
    # Distinguish validation_passed=False (explicitly failed) from None (pending)
    # so failed pipelines don't inflate the "Not yet validated" bucket and don't
    # disappear into ⏳ on the per-row display.
    failed = sum(1 for r in records if r.errors)
    validation_failed = sum(
        1 for r in records
        if not r.errors and r.validation_passed is False
    )
    passed_with_parked = sum(
        1 for r in records
        if not r.errors and r.validation_passed is True and r.parked_activities
    )
    passed_clean = sum(
        1 for r in records
        if not r.errors and r.validation_passed is True and not r.parked_activities
    )
    warned = sum(
        1 for r in records
        if not r.errors and r.validation_passed is None and r.parked_activities
    )
    not_validated = total - failed - validation_failed - passed_with_parked - passed_clean - warned
    
    workspace_url = f"https://app.fabric.microsoft.com/groups/{fabric_workspace_id}"
    
    lines = [
        f"# Pipeline Migration Report",
        f"",
        f"**Source**: Synapse workspace `{synapse_workspace_name}`  ",
        f"**Target**: [Fabric Workspace]({workspace_url})  ",
        f"**Generated**: {migration_date}",
        f"",
        f"## Summary",
        f"",
        f"| Stat | Count |",
        f"|---|---|",
        f"| Total pipelines | {total} |",
        f"| ✅ Migrated & validated (clean) | {passed_clean} |",
        f"| ⚠️  Validated with parked activities | {passed_with_parked} |",
        f"| ⚠️  Migrated with parked activities (not yet validated) | {warned} |",
        f"| ❌ Migration errors | {failed} |",
        f"| ❌ Validation failed | {validation_failed} |",
        f"| ⏳ Not yet validated | {not_validated} |",
        f"",
    ]
    
    if variable_library_id:
        vl_url = f"https://app.fabric.microsoft.com/groups/{fabric_workspace_id}/variablelibraries/{variable_library_id}"
        lines += [
            f"## Variable Library",
            f"",
            f"Global parameters migrated to: [{variable_library_id}]({vl_url})",
            f"",
            f"> Expression change: `@pipeline().globalParameters.*` → `@pipeline().libraryVariables.*`",
            f"",
        ]
    
    lines += [
        f"## Pipeline Migration Details",
        f"",
        f"| # | Pipeline | Status | Fabric Link | Migrated Activities | Parked | Validation |",
        f"|---|---|---|---|---|---|---|",
    ]
    
    for i, record in enumerate(records, 1):
        fabric_link = f"[Open]({record.fabric_url})" if record.fabric_url else "Not deployed"
        migrated_str = ", ".join(f"`{m['from_type']}→{m['to_type']}`" for m in record.migrated_activities) or "—"
        parked_str = ", ".join(f"`{p['type']}`" for p in record.parked_activities) or "—"
        # Validation column reflects ONLY validation state (passed / failed / pending).
        # Parked-activity presence is shown in its own column above and must not
        # mask the true validation state — a pipeline with parked types but not
        # yet validated should still read ⏳, not ⚠️.
        # validation_passed is tri-state: True (✅), False (❌ — explicit fail),
        # None (⏳ — not yet validated). `record.errors` (migration-time error)
        # also forces ❌ since you can't trust validation of a broken pipeline.
        if record.validation_passed is True:
            validation_str = "✅"
        elif record.errors or record.validation_passed is False:
            validation_str = "❌"
        else:
            validation_str = "⏳"
        lines.append(
            f"| {i} | `{record.synapse_name}` | {record.status_emoji} | {fabric_link} "
            f"| {migrated_str} | {parked_str} | {validation_str} |"
        )
    
    # Parked activities section
    parked_records = [r for r in records if r.parked_activities]
    if parked_records:
        lines += [
            f"",
            f"## Parked Activities — Action Required",
            f"",
            f"These activity types have no Fabric equivalent and were not migrated. "
            f"See [pipeline-gotchas.md](../resources/pipeline-gotchas.md) for remediation options.",
            f"",
        ]
        for record in parked_records:
            lines.append(f"### `{record.synapse_name}`")
            lines.append(f"")
            for p in record.parked_activities:
                lines.append(f"- **`{p['type']}`** — {p['reason']}")
            lines.append(f"")
    
    # Error section
    error_records = [r for r in records if r.errors]
    if error_records:
        lines += [
            f"## Migration Errors",
            f"",
        ]
        for record in error_records:
            lines.append(f"### `{record.synapse_name}`")
            lines.append(f"")
            for e in record.errors:
                lines.append(f"- {e}")
            lines.append(f"")

    # Validation error section — kept separate from migration errors so they
    # show up in the report without being miscounted as migration failures.
    val_error_records = [r for r in records if r.validation_errors and not r.errors]
    if val_error_records:
        lines += [
            f"## Validation Errors",
            f"",
            f"These pipelines were migrated successfully but failed one or more "
            f"validation checks (V1/V2/V3/V4). See "
            f"[validation-testing.md](../resources/validation-testing.md).",
            f"",
        ]
        for record in val_error_records:
            lines.append(f"### `{record.synapse_name}`")
            lines.append(f"")
            for e in record.validation_errors:
                lines.append(f"- {e}")
            lines.append(f"")
    
    # Notes section
    note_records = [r for r in records if r.notes]
    if note_records:
        lines += [
            f"## Notes",
            f"",
        ]
        for record in note_records:
            if record.notes:
                lines.append(f"### `{record.synapse_name}`")
                for note in record.notes:
                    lines.append(f"- {note}")
                lines.append(f"")
    
    lines += [
        f"---",
        f"",
        f"*Generated by the `pipeline-migration` skill.*",
        f"*Refer to the skill documentation for resolution of ⚠️ and ❌ items.*",
    ]
    
    return "\n".join(lines)


def save_report(
    records: list[PipelineMigrationRecord],
    fabric_workspace_id: str,
    variable_library_id: Optional[str],
    synapse_workspace_name: str,
    output_path: str = "pipeline-migration-report.md"
):
    """Generate and save the migration report to disk."""
    report = generate_markdown_report(
        records, fabric_workspace_id, variable_library_id, synapse_workspace_name
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"✅ Migration report saved: {output_path}")
    return output_path
```

---

## How to Build Records from the Migration Run

The `PipelineMigrationRecord` objects are built incrementally during the migration process in `pipeline-orchestrator.md`. Here is the pattern for assembling records:

```python
# After Phase 1 inventory
# NOTE: synapse_pipelines must be full pipeline definitions (each item must contain
# properties.activities). The Synapse list endpoint (GET /pipelines) returns stubs
# without activity details — fetch each pipeline individually via
# GET /pipelines/{pipelineName} before passing it here.
records = {}
for pipeline in synapse_pipelines:
    analysis = analyze_synapse_pipeline(pipeline)  # pass full object; function reads ["properties"]["activities"]
    records[pipeline["name"]] = PipelineMigrationRecord(
        synapse_name=pipeline["name"],
        source_activity_types=analysis["all_activity_types"],
        migrated_activities=analysis["migrated_activities"],
        parked_activities=analysis["parked_activities"]
    )

# After Phase 5 deployment — add Fabric IDs
for pipeline_name, fabric_item in deployed_pipelines.items():
    if pipeline_name in records:
        records[pipeline_name].fabric_pipeline_id = fabric_item["id"]
        records[pipeline_name].fabric_workspace_id = FABRIC_WORKSPACE_ID

# After Phase 6 validation
for pipeline_name, validation_result in validation_results.items():
    if pipeline_name in records:
        records[pipeline_name].validation_passed = validation_result.passed()
        records[pipeline_name].validation_run_status = validation_result.v2_run_status
        # Keep validation failures out of `errors` — `errors` drives the
        # "Migration errors" count in the summary table. A pipeline that
        # migrated cleanly but failed validation should appear as
        # "Validation failed" (driven by validation_passed=False), not as a
        # migration failure.
        records[pipeline_name].validation_errors.extend(validation_result.errors)

# Generate final report
save_report(
    records=list(records.values()),
    fabric_workspace_id=FABRIC_WORKSPACE_ID,
    variable_library_id=VARIABLE_LIBRARY_ID,
    synapse_workspace_name=SYNAPSE_WORKSPACE_NAME,
    output_path="pipeline-migration-report.md"
)
```

---

## Example Report Output

```markdown
# Pipeline Migration Report

**Source**: Synapse workspace `mysynapse`  
**Target**: [Fabric Workspace](https://app.fabric.microsoft.com/groups/dddd-...)  
**Generated**: 2024-09-15 14:30 UTC

## Summary

| Stat | Count |
|---|---|
| Total pipelines | 8 |
| ✅ Migrated & validated | 5 |
| ⚠️  Migrated with parked activities | 2 |
| ❌ Migration errors | 1 |

## Variable Library

Global parameters migrated to: [aaaa-...](https://app.fabric.microsoft.com/groups/.../variablelibraries/aaaa-...)

> Expression change: `@pipeline().globalParameters.*` → `@pipeline().libraryVariables.*`

## Pipeline Migration Details

| # | Pipeline | Status | Fabric Link | Migrated Activities | Parked | Validation |
|---|---|---|---|---|---|---|
| 1 | `IngestSalesPipeline` | ✅ | [Open](...) | `SynapseNotebook→TridentNotebook` | — | ✅ |
| 2 | `DatabricksTransform` | ⚠️ | [Open](...) | — | `DatabricksNotebook` | ⚠️ Parked |
| 3 | `SSISPackageRunner` | ⚠️ | [Open](...) | — | `ExecuteSSISPackage` | ⚠️ Parked |
| 4 | `CopyOrders` | ✅ | [Open](...) | — | — | ✅ |
| 5 | `ValidateAndLoad` | ✅ | [Open](...) | `Validation→GetMetadata+IfCondition` | — | ✅ |

## Parked Activities — Action Required

### `DatabricksTransform`

- **`DatabricksNotebook`** — No Fabric equivalent — see pipeline-gotchas.md

### `SSISPackageRunner`

- **`ExecuteSSISPackage`** — No Fabric equivalent — see pipeline-gotchas.md
```
