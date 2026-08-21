# Pipeline Migration Assessment

**Read-only pre-flight analysis.** Run this before touching your Fabric workspace. It queries Synapse APIs only, produces a human-readable report, and gives you the information you need to plan scope, estimate effort, and identify blockers before any items are created in Fabric.

---

## When to Run an Assessment

Run the assessment when the user asks questions like:

- "What's involved in migrating my Synapse pipelines to Fabric?"
- "Can you assess my pipelines before we start?"
- "What will and won't migrate automatically?"
- "How complex is my pipeline migration?"
- "What are the blockers?"
- "Give me a migration plan / scope document"

The assessment output is a scoping document the user can share with stakeholders. No Fabric writes occur.

---

## Required Inputs

Ask the user for their **Synapse workspace name only**. Discover everything else automatically.

| Input | Source |
|---|---|
| Synapse workspace name | **Ask the user** — only required input |
| Azure subscription ID | Auto-discover: `az account show --query id -o tsv` |
| Resource group | Auto-discover: `az synapse workspace show --name <ws> --query resourceGroup -o tsv` |

> **Synapse Studio URL shortcut**: If the user provides a URL like `https://web.azuresynapse.net/en/home?workspace=%2Fsubscriptions%2F{subId}%2FresourceGroups%2F{rg}%2Fproviders%2FMicrosoft.Synapse%2Fworkspaces%2F{wsName}`, extract all three values from it automatically — no need to ask anything.

> **Check login first**: Run `az account show` before acquiring tokens. If it fails, ask the user to run `az login`.

---

## Assessment Script

The script is fully read-only. It collects inventory from Synapse, classifies activities, scores complexity, and produces a structured report.

```python
import requests
import shutil
import subprocess
import os
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

# Per-request HTTP timeout as (connect_seconds, read_seconds). Matches the
# pattern in pipeline-orchestrator.md / validation-testing.md so a transient
# network stall can never hang a read-only assessment run indefinitely.
# Override via env without editing code.
HTTP_TIMEOUT = (
    float(os.environ.get("FABRIC_HTTP_CONNECT_TIMEOUT", 10)),
    float(os.environ.get("FABRIC_HTTP_READ_TIMEOUT", 60)),
)

# ── Platform detection ────────────────────────────────────────────────────────
# Use az.cmd on Windows when present so this runs on Windows/macOS/Linux
# without modification — same approach as pipeline-orchestrator.md.
_AZ = "az.cmd" if shutil.which("az.cmd") else "az"

# ── Activity classification ────────────────────────────────────────────────────

# Activities that drop in cleanly with no required edits — pure
# control-flow / utility activities whose JSON shape is identical
# between Synapse and Fabric.
COMPATIBLE_ACTIVITIES = {
    "ForEach", "IfCondition", "Switch", "Until",        # containers — recurse
    "Wait", "Fail", "SetVariable", "AppendVariable",
    "Filter", "WebActivity", "Script",
}

# Activities that exist in Fabric under the same type but still need targeted
# edits during migration — surfaced separately so the assessment report shows
# the required action items instead of marking them silently 'compatible'.
COMPATIBLE_WITH_CHANGES = {
    "Copy":              "Phase 3 -- dataset inlining + linkedService -> connection mapping (Fabric has no Dataset item type; inputs/outputs collapse into activity `typeProperties` with a sibling `linkedService` reference)",
    "Lookup":            "Phase 3 -- dataset inlining + linkedService -> connection mapping (same dataset-removal pattern as Copy)",
    "GetMetadata":       "Phase 3 -- dataset inlining + linkedService -> connection mapping (same dataset-removal pattern as Copy)",
    "Delete":            "Phase 3 -- dataset inlining + linkedService -> connection mapping (same dataset-removal pattern as Copy)",
    "ExecutePipeline":   "Add `workspaceId` (Fabric requires it even for same-workspace children) and replace `referenceName` with the Fabric DataPipeline item GUID",
    "SparkJobDefinition": "Replace the SJD `referenceName` with the Fabric SJD item GUID and add `workspaceId`",
}

REWRITE_ACTIVITIES = {
    "SynapseNotebook": "TridentNotebook — property changes + GUID lookup required",
    "Validation": "GetMetadata + IfCondition — split into 2 activities",
    "AzureFunctionActivity": "WebActivity — use function URL + x-functions-key header",
    "HDInsightSpark": "TridentNotebook or SparkJobDefinition — significant rewrite",
    "AzureMLBatchExecution": "WebActivity — rewrite as REST call to ML endpoint",
    "AzureMLUpdateResource": "WebActivity — rewrite as REST call",
}

PARKED_ACTIVITIES = {
    "ExecuteSSISPackage": "No Fabric equivalent — use ADF + WebActivity as workaround",
    "DatabricksNotebook": "No native equivalent — use WebActivity → Databricks REST API",
    "DatabricksSparkJar": "No native equivalent — use WebActivity → Databricks REST API",
    "DatabricksSparkPython": "No native equivalent — use WebActivity → Databricks REST API",
    "AzureBatch": "No Fabric equivalent — rehost on Azure Container Apps or Functions",
    "Custom": "No Fabric equivalent — evaluate Azure Container Apps or Functions",
    "MapReduce": "Rewrite in PySpark on Fabric Notebook / SJD",
    "Pig": "Rewrite in PySpark on Fabric Notebook / SJD",
    "Hive": "Rewrite as Spark SQL on Fabric Notebook / SJD",
}

CONTAINER_ACTIVITIES = {
    "ForEach": ["activities"],
    "IfCondition": ["ifTrueActivities", "ifFalseActivities"],
    # Switch is NOT listed here — its cases list contains case objects, not activities.
    # Switch recursion is handled entirely by the dedicated block in walk_activities.
    "Until": ["activities"],
}

SHIR_REQUIRED_CONNECTOR_TYPES = {
    "FileServer", "Ftp", "Sftp", "MongoDb", "MongoDbAtlas",
    "Oracle", "SapBW", "SapCloudForCustomer", "SapEcc", "SapHana",
    "SapOpenHub", "SapTable", "Teradata",
}

# ── Data model ─────────────────────────────────────────────────────────────────

@dataclass
class ActivityRecord:
    name: str
    activity_type: str
    classification: str   # "compatible" | "compatible_with_changes" | "rewrite" | "parked"
    note: str = ""

@dataclass
class PipelineAssessment:
    pipeline_name: str
    total_activities: int = 0
    compatible_count: int = 0                # Drop-in compatible (zero edits)
    compatible_with_changes_count: int = 0   # Compatible activity type, BUT requires edits
                                             # (dataset inlining, connection GUID swap,
                                             # workspaceId injection, notebook GUID
                                             # remap, etc.). Surfaced as its own bucket
                                             # so executive rollups don't conflate
                                             # zero-action with "needs work but the
                                             # activity type itself doesn't change".
    rewrite_count: int = 0                   # Activity type itself must change
    parked_count: int = 0                    # Not supported -- block migration
    activity_records: list[ActivityRecord] = field(default_factory=list)
    unique_activity_types: set = field(default_factory=set)
    notebook_refs: list[str] = field(default_factory=list)     # Synapse notebook names referenced
    linked_service_refs: set = field(default_factory=set)      # linked service names used
    child_pipeline_refs: list[str] = field(default_factory=list)  # pipelines called via ExecutePipeline
    complexity_score: int = 0    # 0=low, 1=medium, 2=high, 3=critical
    complexity_label: str = ""
    blockers: list[str] = field(default_factory=list)
    friction: list[str] = field(default_factory=list)

    def score_complexity(self):
        """Compute complexity score from activity mix and counts."""
        score = 0
        if self.parked_count > 0:
            score += 3
        if self.rewrite_count >= 3:
            score += 2
        elif self.rewrite_count >= 1:
            score += 1
        # compatible_with_changes is genuine edit work (dataset inlining,
        # connection remap, GUID swaps). Counted toward complexity so
        # 'rewrite_count == 0' pipelines that still have hundreds of Copy
        # activities don't roll up as zero-effort.
        if self.compatible_with_changes_count >= 5:
            score += 1
        if self.total_activities > 20:
            score += 1
        if len(self.child_pipeline_refs) > 0:
            score += 1

        self.complexity_score = min(score, 3)
        self.complexity_label = ["🟢 Low", "🟡 Medium", "🟠 High", "🔴 Critical"][self.complexity_score]


# ── Synapse API helpers ────────────────────────────────────────────────────────

def paginate_synapse(url: str, token: str) -> list:
    """Collect all items from a paginated Synapse data-plane list endpoint."""
    headers = {"Authorization": f"Bearer {token}"}
    items = []
    while url:
        r = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        items.extend(data.get("value", []))
        url = data.get("nextLink")
    return items


def get_global_parameters(sub_id: str, rg: str, ws_name: str, arm_token: str) -> dict:
    """Fetch Synapse workspace global parameters via ARM."""
    url = (
        f"https://management.azure.com/subscriptions/{sub_id}/resourceGroups/{rg}"
        f"/providers/Microsoft.Synapse/workspaces/{ws_name}?api-version=2021-06-01"
    )
    r = requests.get(url, headers={"Authorization": f"Bearer {arm_token}"},
                     timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return r.json().get("properties", {}).get("globalParameters", {})


# ── Activity analysis ──────────────────────────────────────────────────────────

def classify_activity(activity_type: str) -> tuple[str, str]:
    """Return (classification, note) for an activity type.

    Returns one of:
      - "parked"                   -- not supported in Fabric; blocks migration
      - "rewrite"                  -- activity type itself must change
                                     (e.g., SynapseNotebook -> TridentNotebook,
                                     Validation -> GetMetadata + IfCondition)
      - "compatible_with_changes"  -- activity type unchanged, BUT requires
                                     targeted edits (dataset inlining,
                                     connection remap, GUID swap, workspaceId
                                     injection). Distinct from "compatible"
                                     so executive rollups (which interpret
                                     rewrite_count == 0 as "clean migration")
                                     don't silently downgrade real work.
      - "compatible"               -- drop-in; zero edits beyond the standard
                                     workspace/dependency remap the migration
                                     orchestrator performs.
    """
    if activity_type in PARKED_ACTIVITIES:
        return "parked", PARKED_ACTIVITIES[activity_type]
    elif activity_type in REWRITE_ACTIVITIES:
        return "rewrite", REWRITE_ACTIVITIES[activity_type]
    elif activity_type in COMPATIBLE_WITH_CHANGES:
        return "compatible_with_changes", COMPATIBLE_WITH_CHANGES[activity_type]
    elif activity_type in COMPATIBLE_ACTIVITIES:
        return "compatible", ""
    else:
        return "rewrite", "Unknown activity type — manual review required"


def walk_activities(activities: list, pipeline_assessment: PipelineAssessment):
    """Recursively walk all activities in a pipeline (including containers)."""
    for activity in activities:
        atype = activity.get("type", "Unknown")
        classification, note = classify_activity(atype)
        pipeline_assessment.unique_activity_types.add(atype)
        pipeline_assessment.total_activities += 1

        record = ActivityRecord(
            name=activity.get("name", ""),
            activity_type=atype,
            classification=classification,
            note=note
        )
        pipeline_assessment.activity_records.append(record)

        if classification == "compatible":
            pipeline_assessment.compatible_count += 1
        elif classification == "compatible_with_changes":
            pipeline_assessment.compatible_with_changes_count += 1
        elif classification == "rewrite":
            pipeline_assessment.rewrite_count += 1
        elif classification == "parked":
            pipeline_assessment.parked_count += 1
            pipeline_assessment.blockers.append(
                f"`{activity.get('name', '<unnamed>')}` ({atype}): {note}"
            )

        tp = activity.get("typeProperties", {})

        # Collect notebook references
        if atype == "SynapseNotebook":
            ref = tp.get("notebook", {}).get("referenceName") or tp.get("notebook", {}).get("name")
            if ref and ref not in pipeline_assessment.notebook_refs:
                pipeline_assessment.notebook_refs.append(ref)

        # Collect ExecutePipeline child references
        if atype == "ExecutePipeline":
            child = tp.get("pipeline", {}).get("referenceName")
            if child and child not in pipeline_assessment.child_pipeline_refs:
                pipeline_assessment.child_pipeline_refs.append(child)

        # Recurse into containers
        for key in CONTAINER_ACTIVITIES.get(atype, []):
            inner = tp.get(key, [])
            if isinstance(inner, list):
                walk_activities(inner, pipeline_assessment)

        # Handle Switch — cases is a list of {value, activities} objects, not activities
        if atype == "Switch":
            for case in tp.get("cases", []):
                walk_activities(case.get("activities", []), pipeline_assessment)
            walk_activities(tp.get("defaultActivities", []), pipeline_assessment)


def collect_linked_service_refs(activity: dict, refs: set):
    """Recursively collect all linkedServiceName references in an activity tree."""
    def _scan(obj):
        if isinstance(obj, dict):
            ls = obj.get("linkedServiceName", {})
            if isinstance(ls, dict) and ls.get("referenceName"):
                refs.add(ls["referenceName"])
            elif isinstance(ls, str) and ls:
                refs.add(ls)
            for v in obj.values():
                _scan(v)
        elif isinstance(obj, list):
            for item in obj:
                _scan(item)

    _scan(activity)


# ── Main assessment function ───────────────────────────────────────────────────

def run_pipeline_assessment(
    synapse_workspace_name: str,
    subscription_id: str,
    resource_group: str,
    synapse_token: str,
    arm_token: str,
) -> dict:
    """
    Collect full inventory from Synapse and produce structured assessment data.
    READ-ONLY — no Fabric API calls, no writes.

    Returns a dict with keys:
        workspace_name, pipelines, linked_services, datasets,
        global_parameters, assessments, dependency_graph,
        ls_classifications
    """
    dp_base = f"https://{synapse_workspace_name}.dev.azuresynapse.net"

    print(f"Collecting inventory from Synapse workspace: {synapse_workspace_name}")

    # ── Inventory collection ───────────────────────────────────────────────────
    pipelines = paginate_synapse(f"{dp_base}/pipelines?api-version=2020-12-01", synapse_token)
    print(f"  Pipelines: {len(pipelines)}")

    linked_services = paginate_synapse(f"{dp_base}/linkedservices?api-version=2020-12-01", synapse_token)
    print(f"  Linked services: {len(linked_services)}")

    datasets = paginate_synapse(f"{dp_base}/datasets?api-version=2020-12-01", synapse_token)
    print(f"  Datasets: {len(datasets)}")

    global_params = get_global_parameters(subscription_id, resource_group, synapse_workspace_name, arm_token)
    print(f"  Global parameters: {len(global_params)}")

    # ── Classify linked services ────────────────────────────────────────────────
    ls_classifications = {}
    for ls in linked_services:
        ls_type = ls.get("properties", {}).get("type", "Unknown")
        requires_shir = ls_type in SHIR_REQUIRED_CONNECTOR_TYPES or (
            ls.get("properties", {}).get("connectVia", {}).get("type") == "IntegrationRuntimeReference"
            and ls.get("properties", {}).get("connectVia", {}).get("referenceName", "") != "AutoResolveIntegrationRuntime"
        )
        ls_classifications[ls["name"]] = {
            "type": ls_type,
            "requires_shir": requires_shir,
            "ir_name": ls.get("properties", {}).get("connectVia", {}).get("referenceName", "AutoResolveIntegrationRuntime")
        }

    # ── Per-pipeline analysis ──────────────────────────────────────────────────
    assessments: dict[str, PipelineAssessment] = {}
    dependency_graph: dict[str, list[str]] = defaultdict(list)

    for pl in pipelines:
        pl_name = pl["name"]
        # The /pipelines list endpoint returns stubs without properties.activities.
        # Fetch the full definition so walk_activities sees the real activity tree.
        r = requests.get(
            f"{dp_base}/pipelines/{pl_name}?api-version=2020-12-01",
            headers={"Authorization": f"Bearer {synapse_token}"},
            timeout=HTTP_TIMEOUT,
        )
        r.raise_for_status()
        pl_detail = r.json()
        pl_props = pl_detail.get("properties", {})
        activities = pl_props.get("activities", [])

        assessment = PipelineAssessment(pipeline_name=pl_name)
        walk_activities(activities, assessment)

        # Collect all linked service refs across the whole pipeline
        for activity in activities:
            collect_linked_service_refs(activity, assessment.linked_service_refs)

        # Check for SHIR-backed linked services used by this pipeline
        for ls_name in assessment.linked_service_refs:
            ls_info = ls_classifications.get(ls_name, {})
            if ls_info.get("requires_shir"):
                assessment.friction.append(
                    f"Linked service `{ls_name}` ({ls_info.get('type')}) uses SHIR "
                    f"`{ls_info.get('ir_name')}` — requires on-premises data gateway in Fabric"
                )

        # Notebook pre-migration friction
        if assessment.notebook_refs:
            assessment.friction.append(
                f"Notebook activities reference {len(assessment.notebook_refs)} Synapse notebook(s) "
                f"that must be migrated to Fabric first: {', '.join(f'`{n}`' for n in assessment.notebook_refs)}"
            )

        # Pipeline dependencies
        for child in assessment.child_pipeline_refs:
            dependency_graph[pl_name].append(child)

        assessment.score_complexity()
        assessments[pl_name] = assessment

    return {
        "workspace_name": synapse_workspace_name,
        "pipelines": pipelines,
        "linked_services": linked_services,
        "datasets": datasets,
        "global_parameters": global_params,
        "assessments": assessments,
        "dependency_graph": dict(dependency_graph),
        "ls_classifications": ls_classifications,
    }
```

---

## Recommended Migration Order

After scoring, determine migration order by sorting pipelines such that:

1. **No parked blockers** — migrate these first
2. **Lowest dependency depth** — leaf pipelines (not called by any other) can be validated in isolation
3. **Most used by other pipelines** — shared/utility pipelines should migrate early so dependents can be validated

```python
def recommended_order(assessments: dict, dependency_graph: dict) -> list[str]:
    """
    Return pipeline names in recommended migration order.
    Priority: no-blocker < medium < high < critical, 
    then by how many other pipelines depend on this one (descending).
    """
    # Count how many pipelines call each pipeline
    reverse_deps: dict[str, int] = defaultdict(int)
    for caller, callees in dependency_graph.items():
        for callee in callees:
            reverse_deps[callee] += 1

    def sort_key(name: str):
        a = assessments[name]
        return (a.complexity_score, -reverse_deps.get(name, 0))

    return sorted(assessments.keys(), key=sort_key)
```

---

## Report Generation

```python
def generate_assessment_report(data: dict, output_path: Optional[str] = None) -> str:
    ws = data["workspace_name"]
    assessments: dict[str, PipelineAssessment] = data["assessments"]
    dep_graph: dict = data["dependency_graph"]
    ls_classifications: dict = data["ls_classifications"]
    global_params: dict = data["global_parameters"]
    datasets: list = data["datasets"]
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    total = len(assessments)
    parked_pipelines = [a for a in assessments.values() if a.parked_count > 0]
    rewrite_pipelines = [a for a in assessments.values() if a.rewrite_count > 0 and a.parked_count == 0]
    # "Compatible-with-changes only" = no rewrite activity types and no
    # blockers, BUT at least one activity needs targeted edits (dataset
    # inlining, connection remap, GUID swap). These were previously
    # bucketed as "clean" -- which silently downgraded pipelines that
    # may have hundreds of Copy/Lookup activities each carrying real
    # connection/GUID work.
    cwc_pipelines = [a for a in assessments.values()
                     if a.parked_count == 0 and a.rewrite_count == 0
                     and a.compatible_with_changes_count > 0]
    clean_pipelines = [a for a in assessments.values()
                       if a.rewrite_count == 0 and a.parked_count == 0
                       and a.compatible_with_changes_count == 0]
    shir_pipelines = [a for a in assessments.values() if a.friction and any("SHIR" in f or "gateway" in f for f in a.friction)]

    all_parked_types: set = set()
    all_notebook_refs: set = set()
    for a in assessments.values():
        for rec in a.activity_records:
            if rec.classification == "parked":
                all_parked_types.add(rec.activity_type)
        all_notebook_refs.update(a.notebook_refs)

    order = recommended_order(assessments, dep_graph)

    lines = [
        f"# Synapse Pipeline Migration Assessment",
        f"",
        f"**Workspace**: `{ws}`  ",
        f"**Generated**: {generated}",
        f"",
        f"---",
        f"",
        f"## Executive Summary",
        f"",
        f"| Category | Count |",
        f"|---|---|",
        f"| Total pipelines | {total} |",
        f"| 🟢 Migrate cleanly (no rewrites, no edits) | {len(clean_pipelines)} |",
        f"| 🟢🟡 Compatible activities only, but require edits (dataset inlining / connection remap / GUID swap) | {len(cwc_pipelines)} |",
        f"| 🟡 Require rewrites (notebook/validation activity changes) | {len(rewrite_pipelines)} |",
        f"| 🔴 Have blockers (parked activity types) | {len(parked_pipelines)} |",
        f"| ⚠️  Use SHIR (require on-premises data gateway) | {len(shir_pipelines)} |",
        f"| Linked services to migrate as connections | {len(data['linked_services'])} |",
        f"| Datasets to inline into activities | {len(datasets)} |",
        f"| Global parameters to move to Variable Library | {len(global_params)} |",
        f"| Synapse notebooks referenced (must migrate first) | {len(all_notebook_refs)} |",
        f"",
    ]

    # Blockers section
    if parked_pipelines:
        lines += [
            f"## 🔴 Blockers — Parked Activity Types",
            f"",
            f"The following activity types have **no direct Fabric equivalent**. "
            f"Each must be manually addressed before or after migration. "
            f"See [pipeline-gotchas.md](../resources/pipeline-gotchas.md) for workaround options.",
            f"",
        ]
        for a in parked_pipelines:
            lines.append(f"### `{a.pipeline_name}`")
            lines.append(f"")
            for blocker in a.blockers:
                lines.append(f"- {blocker}")
            lines.append(f"")

    # SHIR / gateway section
    if shir_pipelines:
        lines += [
            f"## ⚠️  On-Premises Connectivity — Data Gateway Required",
            f"",
            f"These pipelines use linked services backed by a Self-Hosted Integration Runtime (SHIR). "
            f"In Fabric, SHIR is replaced by the **on-premises data gateway**. "
            f"The gateway must be installed and registered before these pipelines can run.",
            f"",
        ]
        for a in shir_pipelines:
            shir_frictions = [f for f in a.friction if "SHIR" in f or "gateway" in f]
            lines.append(f"### `{a.pipeline_name}`")
            for f in shir_frictions:
                lines.append(f"- {f}")
            lines.append(f"")

    # Notebook pre-migration requirements
    if all_notebook_refs:
        lines += [
            f"## 📓 Notebooks — Must Migrate Before Pipelines",
            f"",
            f"The following Synapse notebooks are referenced by `SynapseNotebook` activities. "
            f"They must be migrated to Fabric **before** pipeline migration begins, "
            f"because Fabric `TridentNotebook` activities require a Fabric notebook **GUID**, not a name.",
            f"",
        ]
        for nb in sorted(all_notebook_refs):
            lines.append(f"- `{nb}`")
        lines += [
            f"",
            f"> Use the **synapse-migration** skill to migrate these notebooks first.",
            f"",
        ]

    # Per-pipeline breakdown
    lines += [
        f"## Pipeline-by-Pipeline Analysis",
        f"",
        f"| Pipeline | Complexity | Activities | Rewrites | Blockers | Notes |",
        f"|---|---|---|---|---|---|",
    ]
    for name in order:
        a = assessments[name]
        rewrite_types = sorted({r.activity_type for r in a.activity_records if r.classification == "rewrite"})
        parked_types = sorted({r.activity_type for r in a.activity_records if r.classification == "parked"})
        rewrite_str = ", ".join(f"`{t}`" for t in rewrite_types) if rewrite_types else "—"
        parked_str = ", ".join(f"`{t}`" for t in parked_types) if parked_types else "—"
        notes_parts = []
        if a.notebook_refs:
            notes_parts.append(f"{len(a.notebook_refs)} notebook(s)")
        if a.child_pipeline_refs:
            notes_parts.append(f"calls {len(a.child_pipeline_refs)} pipeline(s)")
        if any("gateway" in f for f in a.friction):
            notes_parts.append("SHIR/gateway")
        notes = "; ".join(notes_parts) if notes_parts else "—"
        lines.append(
            f"| `{name}` | {a.complexity_label} | {a.total_activities} "
            f"| {rewrite_str} | {parked_str} | {notes} |"
        )

    # Pipeline dependency graph
    if dep_graph:
        lines += [
            f"",
            f"## Pipeline Dependencies",
            f"",
            f"These pipelines call other pipelines via `ExecutePipeline` activities. "
            f"Migrate dependencies before callers to enable isolated validation.",
            f"",
            f"| Pipeline | Calls |",
            f"|---|---|",
        ]
        for caller, callees in sorted(dep_graph.items()):
            lines.append(f"| `{caller}` | {', '.join(f'`{c}`' for c in callees)} |")

    # Linked service summary
    shir_ls = {k: v for k, v in ls_classifications.items() if v.get("requires_shir")}
    lines += [
        f"",
        f"## Linked Services → Connections",
        f"",
        f"| Linked Service | Type | SHIR? | IR Name |",
        f"|---|---|---|---|",
    ]
    for ls_name, info in sorted(ls_classifications.items()):
        shir_flag = "⚠️ Yes" if info.get("requires_shir") else "No"
        lines.append(f"| `{ls_name}` | `{info['type']}` | {shir_flag} | `{info['ir_name']}` |")

    # Global parameters
    if global_params:
        lines += [
            f"",
            f"## Global Parameters → Variable Library",
            f"",
            f"All {len(global_params)} global parameter(s) will be migrated to a single "
            f"**Variable Library** item in Fabric.",
            f"Expressions using `@pipeline().globalParameters.<name>` must be "
            f"updated to `@pipeline().libraryVariables.<name>` in all pipeline JSON.",
            f"",
            f"| Parameter Name | Type | Has Array/Object Value |",
            f"|---|---|---|",
        ]
        for pname, pdef in sorted(global_params.items()):
            ptype = pdef.get("type", "string")
            is_complex = "⚠️ Yes — serialized to JSON string" if ptype in ("array", "object") else "No"
            lines.append(f"| `{pname}` | `{ptype}` | {is_complex} |")

    # Recommended migration order
    lines += [
        f"",
        f"## Recommended Migration Order",
        f"",
        f"Migrate in the order below to minimize dependency failures during validation.",
        f"",
    ]
    for i, name in enumerate(order, 1):
        a = assessments[name]
        lines.append(f"{i}. `{name}` — {a.complexity_label}")

    # Pre-migration checklist
    lines += [
        f"",
        f"## Pre-Migration Checklist",
        f"",
        f"Complete these before running the pipeline migration:",
        f"",
        f"- [ ] Fabric workspace created and capacity assigned",
        f"- [ ] Azure tokens acquired (Synapse data-plane, ARM, Fabric)",
    ]
    if all_notebook_refs:
        lines.append(f"- [ ] **Synapse notebooks migrated to Fabric** ({len(all_notebook_refs)} notebook(s) — use synapse-migration skill)")
    if global_params:
        lines.append(f"- [ ] Variable Library plan reviewed ({len(global_params)} global parameter(s))")
    if shir_ls:
        lines.append(f"- [ ] On-premises data gateway installed and registered ({len(shir_ls)} SHIR-backed linked service(s))")
    if parked_pipelines:
        lines.append(f"- [ ] Blocker resolution plan agreed for parked activities (see 🔴 section above)")
    lines += [
        f"- [ ] Fabric Connections created for all linked services ({len(ls_classifications)} linked service(s))",
        f"",
        f"---",
        f"",
        f"*Generated by the `pipeline-migration` skill — assessment mode.*",
        f"*No Fabric items were created. Re-run the assessment after resolving blockers.*",
    ]

    report = "\n".join(lines)
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ Assessment report saved: {output_path}")
    return report


# ── Entry point — Copilot runs this inline, no saved script required ──────────
#
# Copilot workflow:
#   1. Ask user: "What is the name of your Synapse workspace?"
#   2. Run the auto-discovery block below to find subscription and resource group
#   3. Execute this whole file inline via the terminal
#   4. Print the report in the chat — no file write needed (pass output_path to also save)

if __name__ == "__main__":
    import sys

    SYNAPSE_WS = "<workspace-name>"   # ← Copilot fills this in from user answer

    def _az(*args) -> str:
        # _AZ is set at module load — picks "az.cmd" on Windows, "az" elsewhere.
        return subprocess.run([_AZ, *args], capture_output=True, text=True, check=True).stdout.strip()

    # Auto-discover — no need to ask the user for these
    SUBSCRIPTION   = _az("account", "show", "--query", "id", "-o", "tsv")
    RESOURCE_GROUP = _az("synapse", "workspace", "show",
                          "--name", SYNAPSE_WS, "--query", "resourceGroup", "-o", "tsv")
    if not RESOURCE_GROUP:
        # Fallback if the synapse CLI extension is not installed
        RESOURCE_GROUP = _az("resource", "list",
                              "--resource-type", "Microsoft.Synapse/workspaces",
                              "--query", f"[?name=='{SYNAPSE_WS}'].resourceGroup | [0]",
                              "-o", "tsv")

    def get_token(audience: str) -> str:
        return _az("account", "get-access-token", "--resource", audience,
                   "--query", "accessToken", "-o", "tsv")

    synapse_token = get_token("https://dev.azuresynapse.net")
    arm_token     = get_token("https://management.azure.com")

    data = run_pipeline_assessment(
        synapse_workspace_name=SYNAPSE_WS,
        subscription_id=SUBSCRIPTION,
        resource_group=RESOURCE_GROUP,
        synapse_token=synapse_token,
        arm_token=arm_token,
    )

    # Print the full report — Copilot presents this in the chat
    # To also save to disk: generate_assessment_report(data, output_path=f"pipeline-assessment-{SYNAPSE_WS}.md")
    print(generate_assessment_report(data))
```

---

## Assessment Output — Example

```markdown
# Synapse Pipeline Migration Assessment

**Workspace**: `mysynapse`
**Generated**: 2024-09-15 09:00 UTC

---

## Executive Summary

| Category | Count |
|---|---|
| Total pipelines | 12 |
| 🟢 Migrate cleanly | 5 |
| 🟡 Require rewrites | 5 |
| 🔴 Have blockers | 2 |
| ⚠️  Use SHIR | 1 |
| Linked services to migrate as connections | 8 |
| Datasets to inline | 14 |
| Global parameters to move to Variable Library | 6 |
| Synapse notebooks referenced | 4 |

## 🔴 Blockers — Parked Activity Types

### `DatabricksTransformPipeline`
- `RunDatabricks` (DatabricksNotebook): No native equivalent — use WebActivity → Databricks REST API

## 📓 Notebooks — Must Migrate Before Pipelines
- `etl_sales_notebook`
- `ingest_orders_notebook`

> Use the **synapse-migration** skill to migrate these notebooks first.

## Pipeline-by-Pipeline Analysis

| Pipeline | Complexity | Activities | Rewrites | Blockers | Notes |
|---|---|---|---|---|---|
| `CopyOrdersPipeline` | 🟢 Low | 3 | — | — | — |
| `IngestSalesPipeline` | 🟡 Medium | 8 | `SynapseNotebook` | — | 2 notebook(s) |
| `DatabricksTransformPipeline` | 🔴 Critical | 5 | — | `DatabricksNotebook` | — |
```

---

## How Assessment Feeds into Migration

After reviewing the assessment report:

1. **Resolve blockers** — address parked activities per [pipeline-gotchas.md](pipeline-gotchas.md)
2. **Migrate notebooks first** — use the **synapse-migration** skill for the notebooks listed in the assessment
3. **Install data gateway** — if SHIR-backed linked services are flagged
4. **Run migration in recommended order** — use [pipeline-orchestrator.md](pipeline-orchestrator.md)
5. **Use assessment counts to pre-size effort** — activities to rewrite, datasets to inline, linked services to create as connections

The `PipelineAssessment` objects produced by `run_pipeline_assessment()` can also be passed directly to the migration scripts in `pipeline-orchestrator.md` — they contain pre-classified activity lists that avoid re-scanning during migration.
