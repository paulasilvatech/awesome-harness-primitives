# COMMON-CLI.md — CLI Implementation Patterns for Microsoft Fabric

> **Purpose**: This document translates every REST specification in
> `COMMON-CORE.md` into concrete, copy-pasteable CLI
> invocations using **the lowest-footprint tooling available** in the target
> agent environments (GitHub Copilot CLI, Claude Code / Cowork).
>
> **Assumed tools**: `az` (Azure CLI ≥ 2.55), `curl`, standard POSIX shell
> (`bash`), and `jq`.  These are pre-installed or trivially available in most
> development environments. No Python, no Node, no PowerShell modules, no SDKs.

---

## Tool Selection Rationale

| Tool | Role | Why |
|---|---|---|
| `az login` | Authenticate to Entra ID | Pre-installed on most dev machines; handles MFA, device-code, and SPN flows transparently. |
| `az account get-access-token` | Obtain bearer tokens for specific audiences | Supports `--resource` for arbitrary audiences (Fabric API, Storage, Database). |
| `az rest` | Invoke Fabric REST API calls | Auto-attaches bearer tokens, supports `--resource` for non-ARM endpoints. **This is the primary tool.** |
| `curl` | Invoke OneLake DFS / Blob APIs, TDS-adjacent calls, or any endpoint `az rest` doesn't cover | Universal, zero-dependency. |
| `jq` | Parse JSON responses | Standard in all modern shells. |

> **Key insight — `az rest` for Fabric**: Because `api.fabric.microsoft.com`
> is **not** a built-in Azure cloud endpoint, you must always pass
> `--resource https://api.fabric.microsoft.com` so that `az rest` acquires
> a token with the correct audience.  Without `--resource`, `az rest` will
> try to derive the audience from the URL and fail.

---

## Skill Attribution Header — `x-ms-fabric-skill` (Required on Every Fabric API Call)

> **Requirement**: **Every** call you make to the Fabric REST API
> (`https://api.fabric.microsoft.com/...`) — whether via `az rest` or `curl` —
> **MUST** include the HTTP header **`x-ms-fabric-skill`** whose value is the
> **name of the skill making the call**.

**Where the skill name comes from** — use the `name` field from the calling
skill's `SKILL.md` YAML frontmatter (the value on the `name:` line, which is
also the skill's directory name). For example, a skill whose `SKILL.md` begins
with:

```yaml
---
name: activator-authoring-cli
description: >
  ...
---
```

must send `x-ms-fabric-skill: activator-authoring-cli` on every Fabric API call.
Use the value **verbatim** — do not translate, abbreviate, prettify, or add a
version suffix.

**Why**: the Fabric backend reads this header at the public-API gateway to
attribute traffic to the originating skill. The value
is a non-sensitive skill identifier only — never place user data, tokens, or
PII in it.

**Scope**: send it on control-plane calls to `api.fabric.microsoft.com` only.
It is **not** needed for OneLake (`storage.azure.com`), SQL/TDS
(`database.windows.net`), or Kusto calls, which do not traverse the Fabric API
gateway.

**How** — set the skill name once at the top of your shell session, then pass
it on each request. `$SKILL_NAME` is **not** predefined by the environment: in a
one-off command that lacks the assignment below, substitute your skill's literal
`name:` value, or the shell expands it to an empty string and the call goes out
unattributed.

```bash
# Take this literally from your SKILL.md `name:` field:
SKILL_NAME="activator-authoring-cli"

# az rest — add it via --headers (repeat/extend as needed):
az rest \
  --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces" \
  --headers "x-ms-fabric-skill=$SKILL_NAME"

# curl to the Fabric API — add it via -H:
curl -s \
  -H "Authorization: Bearer $FABRIC_TOKEN" \
  -H "x-ms-fabric-skill: $SKILL_NAME" \
  "https://api.fabric.microsoft.com/v1/workspaces"
```

A missing or empty header never changes API behavior or results — the call
still succeeds, it is simply not attributed. So never abort, retry, or fail a
request over it. Sending it is nonetheless **mandatory**: put it on every
Fabric API call, without exception, so the skill's usage and health stay visible.

---

## Finding Workspaces and Items in Fabric

Most of your work will depend on finding items (artifacts) in Fabric.

Simple algorithm:

1. If workspace AND item are specified:
   1. If workspace is specified by name, find the workspace ID (follow instructions in section Resolve Workspace Properties by Name)
   2. If item is specified by name, use the workspace ID and *then* find the item properties within the workspace (follow instructions in section Resolve Item Properties by Name)
2. If workspace is *not specified*: use the **Catalog Search API** (`POST /v1/catalog/search`). You can search by name, description, or workspace name. You can also filter by type (e.g., `"filter": "Type eq 'Lakehouse'"`) with or without a search string. The response includes both the item `id` and `hierarchy.workspace.id` - no second call needed

> **Disambiguation**: If Catalog Search returns multiple matches, present the results to the user (showing display name, type, and workspace name) and ask them to confirm which item they mean.

*Don't try to be creative about the APIs, use them exactly as specified — they have implementation limitations.*

### Resolve Workspace Properties

**Prefer direct ID lookup whenever a workspace UUID is available** (from a prior create response, earlier list result already in context, or explicit user input): call `GET /v1/workspaces/$WS_ID`. Permission-checked direct lookup with no listing or filtering concerns.

**Resolve by name (only when an ID is not available).** The Fabric REST API has no "get workspace by name" endpoint, so list+filter is the only path. The Workspace object exposes `displayName`, not `name` (see [List Workspaces reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/list-workspaces)) — queries on `name` (filter `value[?name==...]` or projection `value[].{name:name,...}`) return empty / nulls and are easily misread as "workspace not found":

```bash
WS_NAME="Marketing"
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces" \
  --query "value[?displayName=='$WS_NAME'] | [0].id" \
  --output tsv
```

Once you have the ID, switch to direct ID lookup for any subsequent calls in the same task.

> **Caution**: This only searches the first page. For tenants with many
> workspaces, pagination may be needed (see Pagination Pattern section below).

### Resolve Item Properties by Name

#### When the workspace is known
Use list-and-filter for an exact match (see also COMMON-CORE.md Resolve Item Properties by Name):

```bash
ITEM_NAME="SalesLakehouse"
ITEM_TYPE="Lakehouse"
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items?type=$ITEM_TYPE" \
  --query "value[?displayName=='$ITEM_NAME'] | [0].id" \
  --output tsv
```

> **Caution**: This only searches the first page. For tenants with many
> items, pagination may be needed (see Pagination Pattern section below).

#### When the workspace is *not* known
Use the Catalog Search API (see also COMMON-CORE.md Catalog Search):

```bash
cat > /tmp/body.json << 'EOF'
{"search": "SalesLakehouse", "filter": "Type eq 'Lakehouse'", "pageSize": 30}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

* The response includes `id`, `type`, `displayName`, `description`, and `hierarchy.workspace` (with `id` and `displayName`) for each match.
* Newly created items can take up to 24 hours to appear in Catalog Search results.
* See [Catalog Search API reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/catalog/search) for supported filter types.

---

## Authentication Recipes

All recipes below correspond to COMMON-CORE.md Authentication & Token Acquisition section. See COMMON-CORE.md for detailed prerequisites, Entra app registration requirements, and permission models.

```bash
# Interactive login (opens browser)
az login

# Fabric tenant with no Azure subscription:
az login --allow-no-subscriptions --tenant <tenantId>

# Headless / SSH / no-browser (device code):
az login --use-device-code --tenant <tenantId>

# Service Principal (client secret) — for CI/CD:
az login --service-principal --username <appId> --password <clientSecret> --tenant <tenantId>

# Service Principal (certificate) — preferred, no secret to rotate:
az login --service-principal --username <appId> --certificate /path/to/cert.pem --tenant <tenantId>

# Managed Identity (system-assigned):
az login --identity

# Managed Identity (user-assigned):
az login --identity --username <clientId>
```

> **`--allow-no-subscriptions`**: Many Fabric users lack an Azure subscription. Without this flag, `az login` reports "No subscriptions found" and subsequent commands may fail.

### Environment Detection and API Configuration

**All Fabric skills use environment-aware API configuration** (see COMMON-CORE.md Environment Detection Pattern for centralized pattern):

```bash
# Standard API Configuration - implemented per COMMON-CORE.md Environment Detection Pattern
FABRIC_API_BASE="https://api.fabric.microsoft.com"
FABRIC_RESOURCE_SCOPE="https://api.fabric.microsoft.com"

# API Versions (centrally managed)
FABRIC_API_VERSION="v1"
LIVY_API_VERSION="2023-12-01"

# Derived URLs
FABRIC_API_URL="$FABRIC_API_BASE/$FABRIC_API_VERSION"
LIVY_API_PATH="livyapi/versions/$LIVY_API_VERSION"
```

### Token Acquisition for Specific Audiences

After login, acquire tokens targeting the correct audience (COMMON-CORE.md Token Audiences / Scopes per Workload). Template:

```bash
az account get-access-token --resource <AUDIENCE> --query accessToken --output tsv
```

| Audience | Use For |
|---|---|
| `https://api.fabric.microsoft.com` | Fabric REST API |
| `https://storage.azure.com` | OneLake (DFS/Blob) and OneLake Table APIs |
| `https://database.windows.net` | SQL / TDS (Warehouse, SQL Endpoint, SQL Database) |
| `https://analysis.windows.net/powerbi/api` | Power BI / XMLA |

> **Note**: `az account get-access-token --resource` uses the v1.0 token endpoint internally. The double-slash gotcha for `database.windows.net` (COMMON-CORE.md) does **not** apply here — `az` handles it correctly.

### Token-in-Variable Pattern

For `curl` calls, capture tokens once and reuse:

```bash
FABRIC_TOKEN=$(az account get-access-token --resource https://api.fabric.microsoft.com --query accessToken --output tsv)
STORAGE_TOKEN=$(az account get-access-token --resource https://storage.azure.com --query accessToken --output tsv)
SQL_TOKEN=$(az account get-access-token --resource https://database.windows.net --query accessToken --output tsv)
```

> **Token lifetime**: Entra tokens typically expire after 60–90 minutes. For long-running scripts, check `--query expiresOn` and re-acquire before expiry.

### Validate a Token (Debugging)

```bash
TOKEN=$(az account get-access-token --resource https://api.fabric.microsoft.com --query accessToken --output tsv)
echo "$TOKEN" | cut -d'.' -f2 | base64 -d 2>/dev/null | jq .
```

Check key claims: `aud` (must match target resource), `exp` (Unix timestamp), `oid` (principal object ID), `tid` (tenant ID).

---

## Fabric Control-Plane API via `az rest`

All calls in this section correspond to COMMON-CORE.md Core Control-Plane REST APIs.
The `--resource` parameter ensures `az rest` acquires the correct Fabric token.
Every call must also carry the `--headers "x-ms-fabric-skill=$SKILL_NAME"` skill-attribution
header, where `$SKILL_NAME` is your `SKILL.md` `name:` value — assign it first, or inline
the literal name — see [§ Skill Attribution Header](#skill-attribution-header--x-ms-fabric-skill-required-on-every-fabric-api-call).

### Common Operations Reference

All operations use the `az rest` template from the Quick Reference section. Key endpoints:

| Operation | Method | URL Path | Notes |
|---|---|---|---|
| Catalog Search | POST | `/v1/catalog/search` | Body: `search`, `filter`, `pageSize`. Returns items with workspace context. |
| List Workspaces | GET | `/v1/workspaces` | Add `?roles=Admin` to filter by role |
| Get Workspace by ID | GET | `/v1/workspaces/$WS_ID` | |
| List Items | GET | `/v1/workspaces/$WS_ID/items` | Add `?type=Lakehouse` to filter |
| Get Item by ID | GET | `/v1/workspaces/$WS_ID/items/$ITEM_ID` | |
| List Items by Type | GET | `/v1/workspaces/$WS_ID/{type}s` | Returns richer `properties` (connection strings, etc.) |
| Get Item by Type + ID | GET | `/v1/workspaces/$WS_ID/{type}s/$ITEM_ID` | Returns richer `properties` |
| Create Workspace | POST | `/v1/workspaces` | Body: `displayName`, `description`, `capacityId` |
| Workspace Role Assignment | POST | `/v1/workspaces/$WS_ID/roleAssignments` | Body: `principal` (id, type), `role` |
| Provision Workspace Identity | POST | `/v1/workspaces/$WS_ID/provisionIdentity` | |
| List Capacities | GET | `/v1/capacities` | |

Where `{type}` is one of: `lakehouse`, `warehouse`, `sqlDatabase`, `notebook`, etc.

**Example — List workspaces as table**:
```bash
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces" \
  --query "value[].{name:displayName, id:id}" \
  --output table
```

**Example — List type-specific items with properties**:
```bash
# Lakehouses — returns sqlEndpointProperties, oneLakeTablesPath, etc.
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/lakehouses"
```

### Resolve Workspace Properties by Name

See the canonical code in the Finding Workspaces and Items in Fabric section above.

### Resolve Item Properties by Name

See the canonical code in the Finding Workspaces and Items in Fabric section above.

### Item CRUD Operations

**Create** (generic — works for any item type):
```bash
cat > /tmp/body.json << 'EOF'
{"displayName": "MyItem", "type": "Lakehouse", "description": "Optional description"}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items" \
  --body @/tmp/body.json
```

Common item types: `Lakehouse`, `Warehouse`, `Notebook`, `DataPipeline`, `SemanticModel`.

**Create with inline definition** (e.g., notebook with content):
```bash
# Base64-encode your .ipynb file, then:
ENCODED_CONTENT=$(base64 -w 0 < ./notebook.ipynb)
cat > /tmp/body.json << EOF
{
  "displayName": "MyNotebook",
  "type": "Notebook",
  "definition": {
    "format": "ipynb",
    "parts": [{
      "path": "notebook-content.ipynb",
      "payload": "$ENCODED_CONTENT",
      "payloadType": "InlineBase64"
    }]
  }
}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items" \
  --body @/tmp/body.json
```

> See ITEM-DEFINITIONS-CORE.md for per-item-type `format`, `path`, and content structure.

**Get definition** (retrieve content from existing item):
```bash
# getDefinition is a POST (not GET); empty body required or 411 error
RESPONSE=$(az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$ITEM_ID/getDefinition?format=ipynb" \
  --body '{}' \
  --output json 2>/dev/null)
```

> The `?format=` parameter is item-type-specific (e.g. `ipynb` for Notebook, `TMDL` for SemanticModel). Omit for item types with a single default format. See ITEM-DEFINITIONS-CORE.md for per-item-type parts and content structure.

**Update definition** (deploy content to existing item):
```bash
cat > /tmp/body.json << EOF
{
  "definition": {
    "format": "ipynb",
    "parts": [{
      "path": "notebook-content.ipynb",
      "payload": "$ENCODED_CONTENT",
      "payloadType": "InlineBase64"
    }]
  }
}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$ITEM_ID/updateDefinition" \
  --body @/tmp/body.json
```

**Update metadata**:
```bash
cat > /tmp/body.json << 'EOF'
{"displayName": "Updated Name", "description": "Updated description"}
EOF
az rest --method patch \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$ITEM_ID" \
  --body @/tmp/body.json
```

**Delete**:
```bash
az rest --method delete \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$ITEM_ID"
```

**Extract created item ID**:
```bash
cat > /tmp/body.json << 'EOF'
{"displayName": "DataLakehouse", "type": "Lakehouse"}
EOF
ITEM_ID=$(az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items" \
  --body @/tmp/body.json \
  --query "id" --output tsv)
```

### Pagination Pattern

Corresponds to COMMON-CORE.md Core Control-Plane REST APIs § Pagination.

The Fabric API uses continuation tokens for paged results. `az rest` combined
with a simple bash loop handles this:

```bash
# Generic paginated fetcher
fetch_all_pages() {
  local URL="$1"
  local RESOURCE="https://api.fabric.microsoft.com"
  local ALL_ITEMS="[]"
  local NEXT_URL="$URL"

  while [ -n "$NEXT_URL" ]; do
    RESPONSE=$(az rest --method get \
      --resource "$RESOURCE" \
      --url "$NEXT_URL" \
      --output json 2>/dev/null)

    PAGE_ITEMS=$(echo "$RESPONSE" | jq -c '.value // []')
    ALL_ITEMS=$(echo "$ALL_ITEMS $PAGE_ITEMS" | jq -sc 'add')

    NEXT_URL=$(echo "$RESPONSE" | jq -r '.continuationUri // empty')
  done

  echo "$ALL_ITEMS"
}

# Usage:
ALL_WORKSPACES=$(fetch_all_pages "https://api.fabric.microsoft.com/v1/workspaces")
echo "$ALL_WORKSPACES" | jq '.[].displayName'
```

### Long-Running Operations (LRO) Pattern

Corresponds to COMMON-CORE.md Core Control-Plane REST APIs § Long-Running Operations (LRO).

When an API returns `202 Accepted`, poll the `Location` header URL until a terminal state. Use this reusable helper:

```bash
# Usage: fabric_lro POST "https://api.fabric.microsoft.com/v1/..." '{"body":"..."}'
fabric_lro() {
  local METHOD="$1" URL="$2" BODY="$3"
  # Skill attribution: set SKILL_NAME to your SKILL.md `name:` value before calling.
  # If unset, the call is simply unattributed — never fail a request over a missing header.
  local TOKEN=$(az account get-access-token \
    --resource https://api.fabric.microsoft.com \
    --query accessToken --output tsv)

  local CURL_ARGS=(-si -X "$METHOD" "$URL" \
    -H "Authorization: Bearer $TOKEN" \
    -H "x-ms-fabric-skill: $SKILL_NAME" \
    -H "Content-Type: application/json")
  [ -n "$BODY" ] && CURL_ARGS+=(-d "$BODY")

  local RESPONSE=$(curl "${CURL_ARGS[@]}")
  local HTTP_STATUS=$(echo "$RESPONSE" | head -1 | awk '{print $2}')

  # If not 202, return the body directly (synchronous response)
  if [ "$HTTP_STATUS" != "202" ]; then
    echo "$RESPONSE" | sed '1,/^\r$/d'
    return 0
  fi

  local OP_URL=$(echo "$RESPONSE" | grep -i '^location:' | tr -d '\r' | awk '{print $2}')
  local RETRY=$(echo "$RESPONSE" | grep -i '^retry-after:' | tr -d '\r' | awk '{print $2}')
  RETRY=${RETRY:-5}

  echo "LRO started, polling $OP_URL every ${RETRY}s..." >&2
  while true; do
    sleep "$RETRY"
    local STATUS_JSON=$(curl -s "$OP_URL" \
      -H "Authorization: Bearer $TOKEN" \
      -H "x-ms-fabric-skill: $SKILL_NAME")
    local STATUS=$(echo "$STATUS_JSON" | jq -r '.status')
    echo "  status: $STATUS" >&2
    case "$STATUS" in
      Succeeded) echo "$STATUS_JSON"; return 0 ;;
      Failed)    echo "$STATUS_JSON"; return 1 ;;
    esac
  done
}
```

---

## OneLake Data Access via `curl`

Corresponds to COMMON-CORE.md OneLake Data Access.

OneLake uses ADLS Gen2-compatible REST APIs. `az rest` is **not suitable**
here because the audience is `https://storage.azure.com`, not the Fabric API.
Use `curl` with a Storage-audience token.

> **All OneLake curl calls require** `-H "x-ms-version: 2021-06-08"`.

```bash
STORAGE_TOKEN=$(az account get-access-token --resource https://storage.azure.com --query accessToken --output tsv)
ONELAKE="https://onelake.dfs.fabric.microsoft.com"
AUTH=(-H "Authorization: Bearer $STORAGE_TOKEN" -H "x-ms-version: 2021-06-08")

WS_NAME="<workspaceGuid>"
LH_NAME="SalesLakehouse.Lakehouse"
```

### List Files in a Lakehouse

```bash
# Top-level listing
curl -s "$ONELAKE/$WS_NAME/$LH_NAME?resource=filesystem&recursive=false" "${AUTH[@]}" | jq .

# Subdirectory listing
curl -s "$ONELAKE/$WS_NAME/$LH_NAME?resource=filesystem&recursive=true&directory=Tables" "${AUTH[@]}" | jq .
```

### Read a File

```bash
curl -s "$ONELAKE/$WS_NAME/$LH_NAME/Files/raw/data.csv" "${AUTH[@]}"
```

### Upload a File

OneLake upload is a three-step process: create → append → flush.

```bash
FILE_PATH="Files/uploads/data.csv"
LOCAL_FILE="./data.csv"
FILE_SIZE=$(wc -c < "$LOCAL_FILE" | tr -d ' ')

# Step 1: Create empty file resource
curl -s -X PUT "$ONELAKE/$WS_NAME/$LH_NAME/$FILE_PATH?resource=file" "${AUTH[@]}" -H "Content-Length: 0"

# Step 2: Append data
curl -s -X PATCH "$ONELAKE/$WS_NAME/$LH_NAME/$FILE_PATH?action=append&position=0" "${AUTH[@]}" \
  -H "Content-Length: $FILE_SIZE" --data-binary @"$LOCAL_FILE"

# Step 3: Flush (finalize)
curl -s -X PATCH "$ONELAKE/$WS_NAME/$LH_NAME/$FILE_PATH?action=flush&position=$FILE_SIZE" "${AUTH[@]}" \
  -H "Content-Length: 0"
```

### Delete a File

```bash
curl -s -X DELETE "$ONELAKE/$WS_NAME/$LH_NAME/$FILE_PATH" "${AUTH[@]}"
```

### Create a Directory

```bash
curl -s -X PUT "$ONELAKE/$WS_NAME/$LH_NAME/Files/new_folder?resource=directory" "${AUTH[@]}" -H "Content-Length: 0"
```

---

## SQL / TDS Data-Plane Access

Corresponds to COMMON-CORE.md SQL / TDS Data-Plane Access.

TDS is a binary protocol — it cannot be invoked via `curl`. The
lowest-footprint CLI tool is **`sqlcmd`** (Go version), which is a standalone
binary with built-in Entra ID authentication.

### Tool: sqlcmd (Go)

- **Install**: `winget install sqlcmd` (Windows), `brew install sqlcmd` (macOS),
  or download from https://aka.ms/go-sqlcmd
- **Zero-config auth**: Uses `az login` context automatically via `-G` flag
- **Standalone**: Single binary, no ODBC driver required

### Connect with Interactive Entra Auth

```bash
# Uses the az login identity automatically
sqlcmd -S <server>.datawarehouse.fabric.microsoft.com -d "<DatabaseName>" -G

# Example: connect to a Warehouse
sqlcmd -S abc123.datawarehouse.fabric.microsoft.com -d "SalesWarehouse" -G
```

### Run a Query Non-Interactively

```bash
sqlcmd -S <server>.datawarehouse.fabric.microsoft.com \
  -d "<DatabaseName>" -G \
  -Q "SELECT TOP 10 * FROM dbo.SalesFactTable"
```

### Run a SQL Script File

```bash
sqlcmd -S <server>.datawarehouse.fabric.microsoft.com \
  -d "<DatabaseName>" -G \
  -i ./my_query.sql
```

### Output to CSV

```bash
sqlcmd -S <server>.datawarehouse.fabric.microsoft.com \
  -d "<DatabaseName>" -G \
  -Q "SELECT * FROM dbo.SalesFactTable" \
  -s "," -W -h -1 > output.csv
```

### Service Principal Authentication

```bash
# First, login as SPN
az login --service-principal -u <appId> -p <secret> --tenant <tenantId>

# Then sqlcmd picks up the SPN context via -G
sqlcmd -S <server>.datawarehouse.fabric.microsoft.com \
  -d "<DatabaseName>" -G \
  -Q "SELECT @@VERSION"
```

### Discovering Connection Parameters via REST

Before connecting via `sqlcmd`, discover the server FQDN and database name
from the Fabric REST API:

```bash
# For a Warehouse:
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/warehouses/$ITEM_ID" \
  --query "properties.{server:connectionString, database:displayName}" \
  --output table

# For a Lakehouse SQL Endpoint:
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/lakehouses/$ITEM_ID" \
  --query "properties.sqlEndpointProperties.{server:connectionString, status:provisioningStatus}"

# For a SQL Database:
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/sqlDatabases/$ITEM_ID" \
  --query "properties.{server:serverFqdn, database:databaseName}"
```

---

## Job Execution

Corresponds to COMMON-CORE.md Job Execution.

### Run a Notebook

```bash
NOTEBOOK_ID="<notebookId>"
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$NOTEBOOK_ID/jobs/instances?jobType=RunNotebook"
```

> **Critical**: Use `jobType=RunNotebook`, NOT `DefaultJob`.
> `DefaultJob` silently fails for most item types.

### Run a Pipeline

```bash
PIPELINE_ID="<pipelineId>"
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$PIPELINE_ID/jobs/instances?jobType=Pipeline"
```

### Refresh a Semantic Model

```bash
MODEL_ID="<semanticModelId>"
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$MODEL_ID/jobs/instances?jobType=Refresh"
```

### Check Job Status

The POST above returns `202 Accepted` with a `Location` header. Use the LRO
pattern from Long-Running Operations (LRO) Pattern section, or:

```bash
JOB_INSTANCE_ID="<jobInstanceId>"
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$NOTEBOOK_ID/jobs/instances/$JOB_INSTANCE_ID"
```

### Cancel a Running Job

```bash
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$NOTEBOOK_ID/jobs/instances/$JOB_INSTANCE_ID/cancel"
```

### Job Scheduling

URL pattern: `POST /v1/workspaces/$WS_ID/items/$ITEM_ID/jobs/{jobType}/schedules`

```bash
cat > /tmp/body.json << 'EOF'
{
  "enabled": true,
  "configuration": {
    "startDateTime": "2026-01-01T06:00:00.000Z",
    "endDateTime": "2027-01-01T06:00:00.000Z",
    "type": "Daily",
    "interval": 1,
    "localTimeZoneId": "UTC",
    "times": ["06:00"]
  }
}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$ITEM_ID/jobs/Pipeline/schedules" \
  --body @/tmp/body.json
```

**Required fields**: `enabled`, `configuration.startDateTime`, `configuration.endDateTime`, `configuration.type`

> **Gotchas**: URL path is `/jobs/{jobType}/schedules` — NOT `/jobs/instances/schedules`. `endDateTime` is required — omitting it returns 400. `type` values: `Daily`, `Weekly`, `Monthly`; `Weekly` also requires `weekDays` array.

**List / Delete schedules**:
```bash
# List
az rest --method get --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$ITEM_ID/jobs/Pipeline/schedules"
# Delete
az rest --method delete --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$ITEM_ID/jobs/Pipeline/schedules/$SCHEDULE_ID"
```

---

## OneLake Shortcuts

Corresponds to COMMON-CORE.md OneLake Shortcuts.

### Create a Shortcut

```bash
cat > /tmp/body.json << 'EOF'
{
  "path": "Tables/external_data",
  "name": "my_shortcut",
  "target": {
    "oneLake": {
      "workspaceId": "<sourceWorkspaceId>",
      "itemId": "<sourceItemId>",
      "path": "Tables/source_table"
    }
  }
}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$LH_ID/shortcuts" \
  --body @/tmp/body.json
```

### List Shortcuts

```bash
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$LH_ID/shortcuts"
```

### Delete a Shortcut

```bash
SHORTCUT_NAME="my_shortcut"
SHORTCUT_PATH="Tables/external_data"
az rest --method delete \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$LH_ID/shortcuts/$SHORTCUT_NAME?path=$SHORTCUT_PATH"
```

---

## Capacity Management

Corresponds to COMMON-CORE.md Capacity Management.

### List Capacities

```bash
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/capacities" \
  --query "value[].{name:displayName, id:id, sku:sku, region:region}" \
  --output table
```

### Assign Workspace to Capacity

```bash
cat > /tmp/body.json << 'EOF'
{"capacityId": "<capacityId>"}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/assignToCapacity" \
  --body @/tmp/body.json
```

---

## Composite Recipes

These recipes combine multiple calls into common real-world workflows.
They use the helpers and patterns defined above (workspace resolution, token acquisition, `fabric_lro`).

### End-to-End: Find Workspace → List Lakehouses → Read OneLake File

```bash
#!/usr/bin/env bash
set -euo pipefail

WS_NAME="Marketing"
LH_NAME="SalesLakehouse"
FILE_PATH="Files/raw/latest_export.csv"

# Step 1: Resolve workspace ID (see Finding Workspaces and Items)
WS_ID=$(az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces" \
  --query "value[?displayName=='$WS_NAME'] | [0].id" \
  --output tsv)

# Step 2: Resolve lakehouse ID
LH_ID=$(az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/lakehouses" \
  --query "value[?displayName=='$LH_NAME'] | [0].id" \
  --output tsv)

# Step 3: Read file from OneLake (Storage token, not Fabric token)
STORAGE_TOKEN=$(az account get-access-token --resource https://storage.azure.com --query accessToken --output tsv)
curl -s "https://onelake.dfs.fabric.microsoft.com/$WS_ID/$LH_NAME.Lakehouse/$FILE_PATH" \
  -H "Authorization: Bearer $STORAGE_TOKEN" -H "x-ms-version: 2021-06-08"
```

### End-to-End: Discover SQL Endpoint → Query via sqlcmd

```bash
#!/usr/bin/env bash
set -euo pipefail

WS_ID="<workspaceId>"
LH_NAME="SalesLakehouse"

# Step 1: Resolve lakehouse and get SQL endpoint info
LH_ID=$(az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/lakehouses" \
  --query "value[?displayName=='$LH_NAME'] | [0].id" \
  --output tsv)

SQL_INFO=$(az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/lakehouses/$LH_ID" \
  --query "properties.sqlEndpointProperties" --output json)

SERVER=$(echo "$SQL_INFO" | jq -r '.connectionString')
STATUS=$(echo "$SQL_INFO" | jq -r '.provisioningStatus')

# Step 2: Query (if endpoint is ready)
if [ "$STATUS" = "Success" ]; then
  sqlcmd -S "$SERVER" -d "$LH_NAME" -G \
    -Q "SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES"
else
  echo "SQL endpoint not ready yet: $STATUS"
fi
```

### Run Notebook and Wait for Completion

Uses the `fabric_lro` helper from the Long-Running Operations (LRO) Pattern section:

```bash
#!/usr/bin/env bash
set -euo pipefail

WS_ID="<workspaceId>"
NOTEBOOK_ID="<notebookId>"

# fabric_lro handles the 202 → poll → terminal-state cycle
RESULT=$(fabric_lro POST \
  "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$NOTEBOOK_ID/jobs/instances?jobType=RunNotebook")

echo "$RESULT" | jq .
```

---

## Gotchas & Troubleshooting (CLI-Specific)

Extends COMMON-CORE.md Gotchas, Best Practices & Troubleshooting with CLI-specific issues.

| Symptom | Cause | Fix |
|---|---|---|
| `az rest` returns `"Can't derive appropriate Azure AD resource from --url"` | Fabric URL is not a built-in Azure endpoint | Always add `--resource "https://api.fabric.microsoft.com"` |
| `az account get-access-token` returns `"AADSTS500011: resource not found"` | Wrong resource URI string | Verify exact string from Environment Detection and API Configuration — no trailing slash variations |
| `401 Unauthorized` on OneLake `curl` call | Using Fabric API token instead of Storage token | Use `--resource https://storage.azure.com` for OneLake |
| `401` with message "Audience validation failed" | Token audience mismatch | Decode the JWT (Validate a Token), compare `aud` with COMMON-CORE.md Token Audiences / Scopes per Workload |
| `az login` says "No subscriptions found" | Fabric-only tenant without Azure subscription | Use `az login --allow-no-subscriptions --tenant <tenantId>` |
| `sqlcmd` connection timeout | Port 1433 blocked outbound, or wrong server FQDN | Verify FQDN from REST API (Discovering Connection Parameters via REST); check firewall rules |
| `sqlcmd` auth error with `-G` | `az login` session expired or wrong tenant | Re-run `az login`; verify `az account show` shows correct tenant |
| `az rest` truncates large JSON bodies | Shell escaping issue with `--body` | Write body to a file and use `--body @body.json` |
| Pagination returns incomplete results | Only first page fetched | Implement the pagination loop from Pagination Pattern section |
| LRO poll returns stale token | Token expired during long operation | Re-acquire token in the poll loop |
| `jq` "Cannot iterate over null" | API returned error instead of expected shape | Check `az rest` stderr; add `--output json` and inspect raw response |
| Complex JSON with special characters | Shell escaping breaks JSON | Write body to file: `cat > /tmp/body.json << 'EOF' ... EOF` then use `--body @/tmp/body.json` |
| KQL pipe `\|` breaks PowerShell inline `--body` | PowerShell interprets `\|` as pipeline operator | **Always write KQL body to temp file**: PowerShell: `@{db="X";csl="T \| count"} \| ConvertTo-Json -Compress \| Out-File $env:TEMP\kql_body.json` then `--body "@$env:TEMP\kql_body.json"` |
| JMESPath query with single quotes in names | Standard quoting doesn't work | Use backtick escaping: `--query "value[?displayName==\`Alice's Workspace\`]"` |
| Unsure which tenant/identity is active | Multiple `az login` sessions | Run `az account show --output table` to check current identity and tenant |

---

## Quick Reference

### `az rest` Template

Every Fabric REST API call follows this pattern:

```bash
# For requests with a JSON body, write it to a temp file first:
cat > /tmp/body.json << 'EOF'
{"key": "value"}
EOF

az rest \
  --method {get|post|put|patch|delete} \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/{path}" \
  --headers "x-ms-fabric-skill=$SKILL_NAME" \
  [--body @/tmp/body.json] \
  [--query "jmesPathExpression"] \
  [--output {json|table|tsv}]
```

**Never omit `--resource`** for Fabric API calls. This is the single most
common mistake and produces a cryptic "Can't derive appropriate Azure AD
resource" error.

**Always include `--headers "x-ms-fabric-skill=$SKILL_NAME"`** on Fabric API
calls, where `$SKILL_NAME` is the `name:` value from your `SKILL.md` frontmatter
— assign it (`SKILL_NAME="<your-skill-name>"`) before the call, or inline the
literal name; an unset variable expands to empty and loses the attribution
(see [§ Skill Attribution Header](#skill-attribution-header--x-ms-fabric-skill-required-on-every-fabric-api-call)). It enables per-skill health and usage telemetry.

### Token Audience ↔ CLI Tool Matrix

| Access Target | Audience for `--resource` | Primary CLI Tool |
|---|---|---|
| Fabric REST API | `https://api.fabric.microsoft.com` | `az rest` |
| OneLake (DFS/Blob) | `https://storage.azure.com` | `curl` |
| SQL / TDS | `https://database.windows.net` | `sqlcmd -G` |
| Power BI / XMLA | `https://analysis.windows.net/powerbi/api` | `curl` or dedicated tools |
| KQL / Kusto | `https://kusto.kusto.windows.net` (or per-cluster URI) | `curl` |
| Azure Resource Manager | `https://management.azure.com` | `az rest` (native) |
