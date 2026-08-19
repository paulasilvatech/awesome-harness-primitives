# Global Parameters → Variable Library

Synapse Analytics global parameters are workspace-level key-value settings accessible by all pipelines via `@pipeline().globalParameters.<name>`. Fabric replaces this concept with the **Variable Library** item type — a workspace-level collection of typed variables with optional environment-specific value sets.

---

## Concept Mapping

| Synapse | Fabric |
|---|---|
| Global parameters (workspace-level setting) | Variable Library (workspace item, type `VariableLibrary`) |
| `@pipeline().globalParameters.<name>` expression | `@pipeline().libraryVariables.<name>` expression |
| Single set of values (no environments) | Value Sets — one per environment (default + dev/test/prod overrides) |
| Types: `String`, `Int`, `Float`, `Bool`, `Array`, `Object` (capitalized in ARM response) | Types: `String`, `Integer`, `Number`, `Boolean` (no array/object — workaround: JSON string) |

---

## Type Mapping

> Synapse global parameter `type` values are **capitalized** in the ARM response (`String`, `Int`, `Bool`, `Array`, etc.) — match the casing in the [ARM API example below](#getting-synapse-global-parameters-via-arm-api). The conversion script's `TYPE_MAP` keys use this canonical capitalized form.

| Synapse Type (ARM) | Fabric Variable Library Type | Notes |
|---|---|---|
| `String` | `String` | Direct |
| `Int` | `Integer` | Direct |
| `Float` / `Double` | `Number` | Direct |
| `Bool` | `Boolean` | Direct |
| `Array` | `String` | Serialize as JSON string: `'["a","b","c"]'` |
| `Object` | `String` | Serialize as JSON string: `'{"key":"value"}'` |

> Downstream code that reads an `Array`/`Object` global parameter must `json.loads()` the string value. If the pipeline used `@pipeline().globalParameters.myArray[0]`, this expression must change — see [pipeline-gotchas.md § PG9](pipeline-gotchas.md).

---

## Getting Synapse Global Parameters via ARM API

Global parameters are stored at the ARM resource level, not the Synapse data-plane API. Use the ARM token:

```bash
ARM_TOKEN="<arm-management-token>"
SUBSCRIPTION_ID="<subscription-id>"
RESOURCE_GROUP="<resource-group>"
SYNAPSE_WORKSPACE="<synapse-workspace-name>"

az rest --method GET \
  --headers "Authorization=Bearer ${ARM_TOKEN}" \
  --url "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.Synapse/workspaces/${SYNAPSE_WORKSPACE}?api-version=2021-06-01" \
  --query "properties.globalParameters" -o json
```

**Example response:**
```json
{
  "environmentName": {
    "type": "String",
    "value": "production"
  },
  "maxBatchSize": {
    "type": "Int",
    "value": 500
  },
  "enableDebugLogging": {
    "type": "Bool",
    "value": false
  },
  "storageAccountName": {
    "type": "String",
    "value": "mystorage"
  },
  "allowedRegions": {
    "type": "Array",
    "value": ["eastus", "westus2"]
  }
}
```

---

## Fabric Variable Library Structure

A Variable Library item consists of three definition parts:

### 1. `variables.json` — Variable declarations

```json
{
  "schema": "https://developer.microsoft.com/json-schemas/fabric/item/variablelibrary/definitionFiles/variables/1.0.0/schema.json#",
  "variables": [
    {
      "name": "environmentName",
      "type": "String",
      "defaultValue": "production"
    },
    {
      "name": "maxBatchSize",
      "type": "Integer",
      "defaultValue": 500
    },
    {
      "name": "enableDebugLogging",
      "type": "Boolean",
      "defaultValue": false
    },
    {
      "name": "storageAccountName",
      "type": "String",
      "defaultValue": "mystorage"
    },
    {
      "name": "allowedRegions",
      "type": "String",
      "defaultValue": "[\"eastus\",\"westus2\"]",
      "description": "Serialized JSON array — use json() expression to parse"
    }
  ]
}
```

### 2. `settings.json` — Value set ordering

```json
{
  "schema": "https://developer.microsoft.com/json-schemas/fabric/item/variablelibrary/definitionFiles/settings/1.0.0/schema.json#",
  "valueSetsOrder": ["default", "dev", "test", "prod"]
}
```

### 3. `valueSets/default.json` — Default values (mirrors `variables.json` defaults)

```json
{
  "schema": "https://developer.microsoft.com/json-schemas/fabric/item/variablelibrary/definitionFiles/valueSets/1.0.0/schema.json#",
  "name": "default",
  "values": [
    { "name": "environmentName", "value": "production" },
    { "name": "maxBatchSize", "value": 500 },
    { "name": "enableDebugLogging", "value": false },
    { "name": "storageAccountName", "value": "mystorage" },
    { "name": "allowedRegions", "value": "[\"eastus\",\"westus2\"]" }
  ]
}
```

---

## Creating the Variable Library via REST API

```python
import os
import requests, json, base64, copy

FABRIC_TOKEN = "<fabric-token>"
FABRIC_WORKSPACE_ID = "<workspace-id>"
VARIABLE_LIBRARY_NAME = "GlobalParameters"
headers = {
    "Authorization": f"Bearer {FABRIC_TOKEN}",
    "Content-Type": "application/json"
}

# Per-request HTTP timeout (connect, read). Mirrors pipeline-orchestrator.md
# so long-running Variable Library creation / LRO polling never hangs
# indefinitely on a transient network stall.
_HTTP_TIMEOUT = (
    float(os.environ.get("FABRIC_HTTP_CONNECT_TIMEOUT", 10)),
    float(os.environ.get("FABRIC_HTTP_READ_TIMEOUT", 60)),
)


def b64(obj: dict) -> str:
    return base64.b64encode(json.dumps(obj).encode()).decode()


def convert_synapse_global_params(synapse_params: dict) -> dict:
    """
    Convert Synapse global parameters to Fabric Variable Library variables.json content.
    
    Returns:
        variables.json content dict
    """
    # Fabric Variable Library supports Boolean, Datetime, Guid, Integer,
    # Number, and String as data types, BUT "Number types aren't supported
    # in pipelines" (per the Variable library integration limitations doc:
    # learn.microsoft.com/fabric/data-factory/variable-library-integration-with-data-pipelines#known-limitations).
    # Because this skill consumes globals via @pipeline().libraryVariables.*,
    # any variable typed Number is silently unusable -- so Synapse Float and
    # Double must map to String here (with the numeric value serialized as
    # its string form by Fabric's runtime cast). Integer stays Integer.
    # Datetime and Guid surface as String inside pipelines per the same doc.
    TYPE_MAP = {
        "String": "String",
        "Int": "Integer",
        "Float": "String",   # Number unsupported in pipelines; preserve as String
        "Double": "String",  # Number unsupported in pipelines; preserve as String
        "Bool": "Boolean",
        "Array": "String",   # Serialize as JSON string
        "Object": "String",  # Serialize as JSON string
    }

    variables = []
    for name, param in synapse_params.items():
        synapse_type = param.get("type", "String")
        fabric_type = TYPE_MAP.get(synapse_type, "String")
        value = param.get("value")

        # Serialize array/object to JSON string
        if synapse_type in ("Array", "Object"):
            value = json.dumps(value)

        entry = {
            "name": name,
            "type": fabric_type,
            "defaultValue": value
        }
        if synapse_type in ("Array", "Object"):
            entry["description"] = f"Serialized JSON {synapse_type.lower()} — use json() to parse"

        variables.append(entry)

    return {
        "schema": "https://developer.microsoft.com/json-schemas/fabric/item/variablelibrary/definitionFiles/variables/1.0.0/schema.json#",
        "variables": variables
    }


def build_value_set(name: str, variables_def: dict) -> dict:
    """Build a value set from variables definition (copies default values)."""
    return {
        "schema": "https://developer.microsoft.com/json-schemas/fabric/item/variablelibrary/definitionFiles/valueSets/1.0.0/schema.json#",
        "name": name,
        "values": [
            {"name": v["name"], "value": v.get("defaultValue")}
            for v in variables_def["variables"]
        ]
    }


def create_variable_library(
    synapse_params: dict,
    workspace_id: str,
    library_name: str,
    additional_value_sets: list[str] = None
) -> str:
    """
    Create a Fabric Variable Library from Synapse global parameters.
    
    Args:
        synapse_params: Dict from Synapse ARM API `properties.globalParameters`
        workspace_id: Fabric workspace GUID
        library_name: Display name for the Variable Library item
        additional_value_sets: Optional list of extra value set names (e.g. ["dev","test","prod"])
    
    Returns:
        Created item ID (GUID)
    """
    variables_def = convert_synapse_global_params(synapse_params)
    value_set_names = ["default"] + (additional_value_sets or [])

    settings_content = {
        "schema": "https://developer.microsoft.com/json-schemas/fabric/item/variablelibrary/definitionFiles/settings/1.0.0/schema.json#",
        "valueSetsOrder": value_set_names
    }

    definition_parts = [
        {
            "path": "variables.json",
            "payload": b64(variables_def),
            "payloadType": "InlineBase64"
        },
        {
            "path": "settings.json",
            "payload": b64(settings_content),
            "payloadType": "InlineBase64"
        }
    ]

    for vs_name in value_set_names:
        value_set = build_value_set(vs_name, variables_def)
        definition_parts.append({
            "path": f"valueSets/{vs_name}.json",
            "payload": b64(value_set),
            "payloadType": "InlineBase64"
        })

    payload = {
        "displayName": library_name,
        "type": "VariableLibrary",
        "definition": {
            "format": "VariableLibrary",
            "parts": definition_parts
        }
    }

    r = requests.post(
        f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items",
        headers=headers,
        json=payload,
        timeout=_HTTP_TIMEOUT,
    )

    if r.status_code in (200, 201):
        # Fabric item creation typically returns 201 Created for synchronous success;
        # 200 OK is also accepted for endpoint variations. Some endpoints return an
        # empty or non-JSON body and provide the created item identity via the
        # Location header instead — handle that defensively rather than blindly
        # calling r.json()["id"], which would raise on empty/non-JSON bodies.
        item_id = None
        if r.content:
            try:
                item_id = r.json().get("id")
            except ValueError:
                item_id = None
        if not item_id:
            location = r.headers.get("Location") or r.headers.get("Content-Location")
            if location:
                if location.startswith("/"):
                    location = f"https://api.fabric.microsoft.com{location}"
                fetched = requests.get(location, headers=headers, timeout=_HTTP_TIMEOUT)
                fetched.raise_for_status()
                item_id = fetched.json().get("id")
        if not item_id:
            raise RuntimeError(
                f"Variable Library creation returned {r.status_code} but no item "
                f"id was found in the body or a Location header. "
                f"Headers: {dict(r.headers)}"
            )
    elif r.status_code == 202:
        # Fabric may return 202 + LRO headers for item creation
        op_url = r.headers.get("Location") or r.headers.get("Operation-Location")
        operation_id = r.headers.get("x-ms-operation-id")
        if not op_url and operation_id:
            op_url = f"https://api.fabric.microsoft.com/v1/operations/{operation_id}"
        if not op_url:
            raise RuntimeError("202 response with no LRO URL header")
        # Resolve relative LRO URLs (e.g. "/v1/operations/...") against the
        # Fabric base so requests.get() receives a valid absolute URL,
        # matching the normalization used in pipeline-orchestrator.md.
        if op_url.startswith("/"):
            op_url = f"https://api.fabric.microsoft.com{op_url}"
        import time
        # Configurable polling cadence — slow tenants/capacities can exceed
        # a fixed 30 * 2 s = 60 s budget. Env-var names match the orchestrator
        # so a single set of overrides applies to every LRO in this skill.
        max_polls = int(os.environ.get("FABRIC_LRO_MAX_POLLS", 150))
        base_poll_interval = float(os.environ.get("FABRIC_LRO_POLL_INTERVAL", 2))
        for _ in range(max_polls):
            # Honor Retry-After when the service supplies a polling cadence;
            # fall back to base_poll_interval otherwise.
            retry_after = r.headers.get("Retry-After")
            sleep_s = float(retry_after) if retry_after else base_poll_interval
            time.sleep(sleep_s)
            poll = requests.get(op_url, headers=headers, timeout=_HTTP_TIMEOUT)
            poll.raise_for_status()
            state = poll.json()
            # Refresh r for the next iteration's Retry-After read
            r = poll
            if state.get("status") == "Succeeded":
                # Different Fabric LRO endpoints return the new item ID in different
                # places — prefer createdItemId, fall back to result.id, then to
                # fetching resourceLocation. This avoids KeyError on endpoint variants.
                item_id = (
                    state.get("createdItemId")
                    or state.get("result", {}).get("id")
                )
                if not item_id:
                    resource_loc = state.get("resourceLocation") or poll.headers.get("Location")
                    if resource_loc:
                        if resource_loc.startswith("/"):
                            resource_loc = f"https://api.fabric.microsoft.com{resource_loc}"
                        created = requests.get(resource_loc, headers=headers, timeout=_HTTP_TIMEOUT)
                        created.raise_for_status()
                        item_id = created.json().get("id")
                if not item_id:
                    raise RuntimeError(
                        f"Variable Library LRO succeeded but no item ID was returned. "
                        f"Operation payload: {state}"
                    )
                break
            if state.get("status") in ("Failed", "Cancelled"):
                raise RuntimeError(f"Variable Library creation failed: {state}")
        else:
            raise TimeoutError(
                f"Variable Library creation LRO timed out after {max_polls} polls "
                f"(base interval {base_poll_interval}s). Increase "
                f"FABRIC_LRO_MAX_POLLS or FABRIC_LRO_POLL_INTERVAL for "
                f"slow tenants/capacities."
            )
    else:
        r.raise_for_status()

    print(f"✅ Variable Library '{library_name}' created: {item_id}")
    return item_id
```

---

## Connecting the Variable Library to a Pipeline

After creating the Variable Library, add the `libraryVariables` block to each pipeline definition:

```json
{
  "properties": {
    "activities": [...],
    "parameters": {...},
    "variables": {...},
    "libraryVariables": {
      "libraryId": "<variable-library-item-id>",
      "workspaceId": "<fabric-workspace-id>"
    }
  }
}
```

Add this to all pipelines that previously used `@pipeline().globalParameters.*`:

```python
def attach_variable_library(
    pipeline_def: dict,
    library_id: str,
    workspace_id: str
) -> dict:
    """Add libraryVariables reference to a pipeline definition."""
    import copy
    pipeline_def = copy.deepcopy(pipeline_def)
    pipeline_def.setdefault("properties", {})["libraryVariables"] = {
        "libraryId": library_id,
        "workspaceId": workspace_id
    }
    return pipeline_def
```

---

## Expression Rewrite

After creating the Variable Library and attaching it to pipelines, replace all expression references:

| Before (Synapse) | After (Fabric) |
|---|---|
| `@pipeline().globalParameters.environmentName` | `@pipeline().libraryVariables.environmentName` |
| `@pipeline().globalParameters.maxBatchSize` | `@pipeline().libraryVariables.maxBatchSize` |

This replacement is included in the bulk transformation in `notebook-activity-migration.md` and `pipeline-orchestrator.md`. Use an object-walk that rewrites only ADF expression strings (string values starting with `@`) — a blind `replace()` on the serialized JSON would also mutate unrelated literal text such as descriptions, annotations, or embedded code snippets that happen to contain `@pipeline().globalParameters.` in prose form.

> **Keep in sync** with the equivalent helpers in `notebook-activity-migration.md` (`_rewrite_expressions` inside `transform_pipeline_notebook_activities`) and `pipeline-orchestrator.md` (`_rewrite_expressions` inside the per-pipeline migration loop). Editing the rewrite rules in one place without updating the others will cause the three docs to drift.

```python
def rewrite_global_parameters(node):
    if isinstance(node, dict):
        # Only rewrite within the canonical ADF/Fabric expression dict shape
        # ({"value": "@...", "type": "Expression"}) — never bare strings, so
        # description/annotation text or embedded code samples that contain
        # "pipeline().globalParameters." in prose aren't mutated.
        if (
            node.get("type") == "Expression"
            and isinstance(node.get("value"), str)
            and node["value"].startswith("@")
        ):
            return {
                **node,
                # Match the bare `pipeline().globalParameters.` substring so
                # both `@pipeline().globalParameters.x` AND nested forms
                # like `@concat('env=', pipeline().globalParameters.env)`
                # get rewritten. The outer startswith("@") guard above
                # still scopes this strictly to expression-shaped dicts.
                "value": node["value"].replace(
                    "pipeline().globalParameters.",
                    "pipeline().libraryVariables.",
                ),
            }
        return {k: rewrite_global_parameters(v) for k, v in node.items()}
    if isinstance(node, list):
        return [rewrite_global_parameters(v) for v in node]
    return node

pipeline_def = rewrite_global_parameters(pipeline_def)
```

---

## Value Sets for Environment Promotion

Use value sets to maintain dev/test/prod environment-specific overrides without duplicating Variable Library items:

### Create a `prod` value set with different values

```python
prod_value_set = {
    "schema": "https://developer.microsoft.com/json-schemas/fabric/item/variablelibrary/definitionFiles/valueSets/1.0.0/schema.json#",
    "name": "prod",
    "values": [
        {"name": "environmentName", "value": "production"},
        {"name": "maxBatchSize", "value": 5000},       # Higher batch size in prod
        {"name": "enableDebugLogging", "value": False},
        {"name": "storageAccountName", "value": "prodstorageaccount"},
        {"name": "allowedRegions", "value": "[\"eastus\",\"westeurope\"]"}
    ]
}
```

When a pipeline runs, it uses the active value set selected at workspace or pipeline scope.
