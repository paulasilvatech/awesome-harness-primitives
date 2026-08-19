<!-- Mode reference for the `eventhouse-cli` skill. Loaded on demand from `skills/eventhouse-cli/SKILL.md` when the request matches the `authoring` mode. -->

> **PRE-MUTATION REQUIREMENTS GATE (mandatory)**
> Before any mutation, confirm the request identifies the target KQL database
> and the intended table, schema, ingestion, policy, function, or materialized
> view change. If the request is generic, such as "set up my Eventhouse", ask a
> clarifying question and stop before mutation. Do not infer a schema or apply
> management commands from unrelated workspace items.

# eventhouse-cli authoring mode — Eventhouse Authoring and Management via CLI

## Table of Contents

| Task | Reference | Notes |
|---|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | **Mandatory** — *READ link first* [needed for workspace/item ID resolution] |
| Fabric Topology & Key Concepts | [COMMON-CORE.md § Fabric Topology & Key Concepts](../../../common/COMMON-CORE.md#fabric-topology--key-concepts) | Hierarchy, Finding Things in Fabric |
| Environment URLs | [COMMON-CORE.md § Environment URLs](../../../common/COMMON-CORE.md#environment-urls) | KQL Cluster URI, KQL Ingestion URI |
| Authentication & Token Acquisition | [COMMON-CORE.md § Authentication & Token Acquisition](../../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401; KQL audience: `kusto.kusto.windows.net` |
| Core Control-Plane REST APIs | [COMMON-CORE.md § Core Control-Plane REST APIs](../../../common/COMMON-CORE.md#core-control-plane-rest-apis) | List Workspaces, List Items, Item Creation |
| Pagination | [COMMON-CORE.md § Pagination](../../../common/COMMON-CORE.md#pagination) | |
| Long-Running Operations (LRO) | [COMMON-CORE.md § Long-Running Operations (LRO)](../../../common/COMMON-CORE.md#long-running-operations-lro) | |
| Rate Limiting & Throttling | [COMMON-CORE.md § Rate Limiting & Throttling](../../../common/COMMON-CORE.md#rate-limiting--throttling) | |
| OneLake Data Access | [COMMON-CORE.md § OneLake Data Access](../../../common/COMMON-CORE.md#onelake-data-access) | Requires `storage.azure.com` token, not Fabric token |
| Job Execution | [COMMON-CORE.md § Job Execution](../../../common/COMMON-CORE.md#job-execution) | |
| Capacity Management | [COMMON-CORE.md § Capacity Management](../../../common/COMMON-CORE.md#capacity-management) | |
| Gotchas & Troubleshooting | [COMMON-CORE.md § Gotchas & Troubleshooting](../../../common/COMMON-CORE.md#gotchas--troubleshooting) | |
| Best Practices | [COMMON-CORE.md § Best Practices](../../../common/COMMON-CORE.md#best-practices) | |
| Tool Selection Rationale | [COMMON-CLI.md § Tool Selection Rationale](../../../common/COMMON-CLI.md#tool-selection-rationale) | |
| Authentication Recipes | [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) | `az login` flows and token acquisition |
| Fabric Control-Plane API via `az rest` | [COMMON-CLI.md § Fabric Control-Plane API via az rest](../../../common/COMMON-CLI.md#fabric-control-plane-api-via-az-rest) | **Always pass `--resource https://api.fabric.microsoft.com`** or `az rest` fails |
| Pagination Pattern | [COMMON-CLI.md § Pagination Pattern](../../../common/COMMON-CLI.md#pagination-pattern) | |
| Long-Running Operations (LRO) Pattern | [COMMON-CLI.md § Long-Running Operations (LRO) Pattern](../../../common/COMMON-CLI.md#long-running-operations-lro-pattern) | |
| OneLake Data Access via `curl` | [COMMON-CLI.md § OneLake Data Access via curl](../../../common/COMMON-CLI.md#onelake-data-access-via-curl) | Use `curl` not `az rest` (different token audience) |
| SQL / TDS Data-Plane Access | [COMMON-CLI.md § SQL / TDS Data-Plane Access](../../../common/COMMON-CLI.md#sql--tds-data-plane-access) | `sqlcmd` (Go) — not for KQL, but useful for cross-workload |
| Job Execution (CLI) | [COMMON-CLI.md § Job Execution](../../../common/COMMON-CLI.md#job-execution) | |
| OneLake Shortcuts | [COMMON-CLI.md § OneLake Shortcuts](../../../common/COMMON-CLI.md#onelake-shortcuts) | |
| Capacity Management (CLI) | [COMMON-CLI.md § Capacity Management](../../../common/COMMON-CLI.md#capacity-management) | |
| Composite Recipes | [COMMON-CLI.md § Composite Recipes](../../../common/COMMON-CLI.md#composite-recipes) | |
| Gotchas & Troubleshooting (CLI-Specific) | [COMMON-CLI.md § Gotchas & Troubleshooting (CLI-Specific)](../../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping, token expiry |
| Quick Reference: `az rest` Template | [COMMON-CLI.md § Quick Reference: az rest Template](../../../common/COMMON-CLI.md#quick-reference-az-rest-template) | |
| Quick Reference: Token Audience / CLI Tool Matrix | [COMMON-CLI.md § Quick Reference: Token Audience ↔ CLI Tool Matrix](../../../common/COMMON-CLI.md#quick-reference-token-audience--cli-tool-matrix) | Which `--resource` + tool for each service |
| Authoring Capability Matrix | [EVENTHOUSE-AUTHORING-CORE.md § Authoring Capability Matrix](../../../common/EVENTHOUSE-AUTHORING-CORE.md#authoring-capability-matrix) | **Read first** — KQL Database vs Shortcut (read-only); connection requires Admin/Ingestor role |
| Table Management and Schema Evolution | [EVENTHOUSE-AUTHORING-CORE.md § Table Management and Schema Evolution](../../../common/EVENTHOUSE-AUTHORING-CORE.md#table-management-and-schema-evolution) | Create Table, Create-Merge (idempotent), Alter / Rename / Drop, Schema Evolution (Rename, Swap/Blue-Green) |
| Ingestion and Data Mappings | [EVENTHOUSE-AUTHORING-CORE.md § Ingestion and Data Mappings](../../../common/EVENTHOUSE-AUTHORING-CORE.md#ingestion-and-data-mappings) | Inline, Set-or-Append/Replace, From Storage, Streaming, Data Mappings (CSV, JSON) |
| Policies | [EVENTHOUSE-AUTHORING-CORE.md § Policies](../../../common/EVENTHOUSE-AUTHORING-CORE.md#policies) | Retention, Caching, Partitioning, Merge |
| Materialized Views | [EVENTHOUSE-AUTHORING-CORE.md § Materialized Views](../../../common/EVENTHOUSE-AUTHORING-CORE.md#materialized-views) | Create, Alter, Lifecycle, Supported aggregations |
| Stored Functions and Update Policies | [EVENTHOUSE-AUTHORING-CORE.md § Stored Functions and Update Policies](../../../common/EVENTHOUSE-AUTHORING-CORE.md#stored-functions-and-update-policies) | Stored Functions, Update Policies (auto-transform on ingestion) |
| External Tables | [EVENTHOUSE-AUTHORING-CORE.md § External Tables](../../../common/EVENTHOUSE-AUTHORING-CORE.md#external-tables) | OneLake / ADLS External Table, Query External Table |
| Permission Model | [EVENTHOUSE-AUTHORING-CORE.md § Permission Model](../../../common/EVENTHOUSE-AUTHORING-CORE.md#permission-model) | Database Roles, Grant Permissions |
| Authoring Gotchas and Troubleshooting | [EVENTHOUSE-AUTHORING-CORE.md § Authoring Gotchas and Troubleshooting Reference](../../../common/EVENTHOUSE-AUTHORING-CORE.md#authoring-gotchas-and-troubleshooting-reference) | 10 numbered issues with cause + fix |
| Bash Templates | [authoring-script-templates.md § Bash Templates](authoring/authoring-script-templates.md#bash-templates) | Create Table + Ingest, Schema Deployment, Export Schema, Set Retention/Caching |
| PowerShell Templates | [authoring-script-templates.md § PowerShell Templates](authoring/authoring-script-templates.md#powershell-templates) | Create Table + Ingest, Schema Deployment |
| Tool Stack | [SKILL.md § Tool Stack](#tool-stack) | |
| Connection | [SKILL.md § Connection](#connection) | |
| Authoring Scope | [SKILL.md § Authoring Scope](#authoring-scope) | |
| Execute KQL Command | [SKILL.md § Execute KQL Command](#execute-kql-command) | **`az rest` pattern** — write JSON body, then execute |
| Table Management via CLI | [SKILL.md § Table Management via CLI](#table-management-via-cli) | Create Table, Add Column, Drop Table |
| Data Ingestion via CLI | [SKILL.md § Data Ingestion via CLI](#data-ingestion-via-cli) | Inline, From Storage, From OneLake, Set-or-Append |
| Policies via CLI | [SKILL.md § Policies via CLI](#policies-via-cli) | Retention, Caching, Streaming Ingestion |
| Materialized Views via CLI | [SKILL.md § Materialized Views via CLI](#materialized-views-via-cli) | |
| Functions and Update Policies via CLI | [SKILL.md § Functions and Update Policies via CLI](#functions-and-update-policies-via-cli) | Create Function, Create Update Policy |
| Schema Evolution via CLI | [SKILL.md § Schema Evolution via CLI](#schema-evolution-via-cli) | Safe Schema Deployment Script, Export Current Schema |
| Monitoring Authoring Operations | [SKILL.md § Monitoring Authoring Operations](#monitoring-authoring-operations) | |
| Must / Prefer / Avoid / Troubleshooting | [SKILL.md § Must / Prefer / Avoid / Troubleshooting](#must--prefer--avoid--troubleshooting) | **MUST DO / AVOID / PREFER** checklists |
| Agentic Workflows | [SKILL.md § Agentic Workflows](#agentic-workflows) | Exploration Before Authoring, Script Generation Workflow |
| Examples | [SKILL.md § Examples](#examples) | |
| Agent Integration Notes | [SKILL.md § Agent Integration Notes](#agent-integration-notes) | |

---

## Tool Stack

| Tool | Purpose | Install |
|---|---|---|
| **az cli** | KQL management commands via Kusto REST API; Fabric control-plane discovery | `winget install Microsoft.AzureCLI` |
| **jq** | JSON processing and output formatting | `winget install jqlang.jq` |

---

## Connection

Use the same discovery flow as the [consumption mode](consumption.md#connection). Authoring requires elevated roles:

```bash
# Discover KQL Database query URI
WS_ID="<workspace-id>"
az rest --method GET \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WS_ID}/kqlDatabases" \
  --resource "https://api.fabric.microsoft.com" \
  | jq '.value[] | {name: .displayName, queryUri: .properties.queryServiceUri}'

# Set connection variables
CLUSTER_URI="https://<cluster>.kusto.fabric.microsoft.com"
DB_NAME="MyDatabase"

# Verify admin access
cat > /tmp/kql_body.json << EOF
{"db":"${DB_NAME}","csl":".show database ${DB_NAME} principals | where Role == 'Admin'"}
EOF
az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/mgmt" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'
```

---

## Authoring Scope

| Operation | Command Pattern |
|---|---|
| Create table | `.create-merge table T (cols)` |
| Add column | `.alter-merge table T (NewCol: type)` |
| Drop table | `.drop table T ifexists` |
| Ingest data | `.ingest into table T (...)` |
| Set retention | `.alter table T policy retention ...` |
| Set caching | `.alter table T policy caching hot = Nd` |
| Create function | `.create-or-alter function F() { ... }` |
| Create materialized view | `.create materialized-view MV on table T { ... }` |
| Create update policy | `.alter table T policy update ...` |
| Create data mapping | `.create table T ingestion csv mapping ...` |

---

## Execute KQL Command

All KQL management commands in this skill follow the same `az rest` pattern. After setting `CLUSTER_URI` and `DB`, write the JSON body to `/tmp/kql_body.json` and execute:

```bash
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":"<KQL management command>"}
EOF
az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/mgmt" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'
```

> **Nested JSON** — For commands whose KQL contains embedded JSON (policies, mappings), use `<< 'EOF'` (single-quoted) to prevent shell expansion of backslash-escaped quotes, and replace `${DB}` with the literal database name.

> **PowerShell equivalent** — `@{db=$Database;csl=$Command} | ConvertTo-Json -Compress | Out-File $env:TEMP\kql_body.json -Encoding utf8NoBOM` then `--body "@$env:TEMP\kql_body.json"`. See [PowerShell Templates](authoring/authoring-script-templates.md#powershell-templates).

---

## Table Management via CLI

### Create Table (Idempotent)

```bash
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".create-merge table Events (Timestamp: datetime, EventType: string, UserId: string, Properties: dynamic, Duration: real)"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

### Add Column

```bash
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".alter-merge table Events (Region: string)"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

### Drop Table

```bash
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".drop table Events ifexists"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

---

## Data Ingestion via CLI

### Inline Ingestion (Testing)

```bash
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".ingest inline into table Events <| 2025-01-15T10:00:00Z,Login,user1,{},0.5\n2025-01-15T10:01:00Z,Click,user2,{},0.2"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

### Ingest from Storage

```bash
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".ingest into table Events (h'https://mystorage.blob.core.windows.net/data/events.csv.gz;impersonate') with (format='csv', ingestionMappingReference='EventsCsvMapping', ignoreFirstRecord=true)"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

### Ingest from OneLake

```bash
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".ingest into table Events (h'abfss://workspace@onelake.dfs.fabric.microsoft.com/lakehouse.Lakehouse/Files/events.parquet;impersonate') with (format='parquet')"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

### Set-or-Append from Query

```bash
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".set-or-append CleanEvents <| RawEvents | where IsValid == true | project Timestamp, EventType, UserId"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

---

## Policies via CLI

### Retention

```bash
# Set 365-day retention
cat > /tmp/kql_body.json << 'EOF'
{"db":"MyDB","csl":".alter table Events policy retention '{\"SoftDeletePeriod\":\"365.00:00:00\",\"Recoverability\":\"Enabled\"}'"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

### Caching (Hot Cache)

```bash
# Keep last 30 days in hot cache
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".alter table Events policy caching hot = 30d"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

### Streaming Ingestion

```bash
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".alter table Events policy streamingingestion enable"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

---

## Materialized Views via CLI

```bash
# Create materialized view with backfill
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".create materialized-view with (backfill=true) HourlyEventCounts on table Events { Events | summarize Count = count(), LastSeen = max(Timestamp) by EventType, bin(Timestamp, 1h) }"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

```bash
# Check health
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".show materialized-view HourlyEventCounts statistics"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

---

## Functions and Update Policies via CLI

### Create Function

```bash
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".create-or-alter function with (docstring='Parse raw events', folder='ETL') ParseRawEvents() { RawEvents | extend Parsed = parse_json(RawData) | project Timestamp = todatetime(Parsed.timestamp), EventType = tostring(Parsed.eventType), UserId = tostring(Parsed.userId) }"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

### Create Update Policy

```bash
cat > /tmp/kql_body.json << 'EOF'
{"db":"MyDB","csl":".alter table ParsedEvents policy update @'[{\"IsEnabled\":true,\"Source\":\"RawEvents\",\"Query\":\"ParseRawEvents()\",\"IsTransactional\":true}]'"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

---

## Schema Evolution via CLI

### Safe Schema Deployment Script

Save management commands in a `.kql` file (one per line), then execute each command via `az rest`:

```bash
# deploy_schema.kql contains one command per line:
# .create-merge table Events (Timestamp: datetime, EventType: string, UserId: string, Properties: dynamic)
# .create-merge table ParsedEvents (Timestamp: datetime, EventType: string, UserId: string, PageName: string)
# .alter table Events policy retention '{\"SoftDeletePeriod\":\"365.00:00:00\",\"Recoverability\":\"Enabled\"}'
# .alter table Events policy caching hot = 30d

# Execute each command from the file (see "Execute KQL Command" section)
while IFS= read -r cmd; do
  [[ "$cmd" =~ ^// ]] && continue   # skip comment lines
  [[ -z "$cmd" ]] && continue        # skip blank lines
  cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":"${cmd}"}
EOF
  az rest --method POST \
    --url "${CLUSTER_URI}/v1/rest/mgmt" \
    --resource "https://kusto.kusto.windows.net" \
    --headers "Content-Type=application/json" \
    --body @/tmp/kql_body.json \
    | jq '.Tables[0].Rows'
done < deploy_schema.kql
```

### Export Current Schema

```bash
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".show database ${DB} schema as csl script"}
EOF
az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/mgmt" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq -r '.Tables[0].Rows[][0]' > current_schema.kql
```

---

## Monitoring Authoring Operations

```kql
// Recent management commands
.show commands
| where StartedOn > ago(1h)
| project StartedOn, CommandType, Text = substring(Text, 0, 100), State, Duration
| order by StartedOn desc

// Ingestion failures
.show ingestion failures
| where FailedOn > ago(24h)
| summarize FailureCount = count() by ErrorCode, Table
| order by FailureCount desc

// Materialized view health
.show materialized-views
| project Name, IsEnabled, IsHealthy, MaterializedTo
```

---

## Must / Prefer / Avoid / Troubleshooting

### Must

- **Clarify before acting on ambiguous prompts** — if the request does not specify a target table, operation type, or schema (e.g. "set up my Eventhouse", "configure my database"), ask the user what they want to do. Never infer intent and apply management commands autonomously. Irreversible side-effects (policy changes, schema mutations, data ingestion) require explicit user intent.
- **Use idempotent commands** — `.create-merge table`, `.create-or-alter function`, `.create table ifnotexists`.
- **Verify permissions** before authoring — must have `Admin` or `Ingestor` role.
- **Test update policies** by running the function independently before attaching.
- **Include `impersonate`** in storage URIs when ingesting from OneLake or Blob Storage.

### Prefer

- **`az rest` with loop** for deploying multi-command schema files.
- **Fabric KQL MCP server** for agent-integrated ingestion and management workflows.
- **`.create-merge table`** over `.create table` for safe schema evolution.
- **Materialized views** over repeated expensive aggregation queries.
- **Script-based CI/CD** — export schema with `.show database DB schema as csl script`, store in git.

### Avoid

- **`.drop table`** without `ifexists` — fails on missing tables.
- **`.alter table`** to add columns — use `.alter-merge table` instead (additive only).
- **Ingestion without mappings** for CSV/JSON — column order or field names may not match.
- **Hardcoded storage URIs** — parameterise in scripts.
- **Disabling materialized views** without understanding the re-backfill cost.

### Troubleshooting

| Symptom | Fix |
|---|---|
| `.create table` fails "already exists" | Use `.create-merge table` or `.create table ifnotexists` |
| Ingestion succeeds but table empty | Check data mappings: `.show table T ingestion csv mappings` |
| Update policy not firing | Verify function runs standalone; check `.show table T policy update` |
| `Forbidden (403)` on management commands | Request `admin` or `ingestor` database role |
| Materialized view stuck | Check `.show materialized-view MV statistics`; may need `.disable`/`.enable` |
| OneLake ingest auth error | Add `;impersonate` to `abfss://` URI |

---

## Agentic Workflows

### Exploration Before Authoring

Always check for explicit intent before doing anything:

```text
Step 0 → Is the request specific? Does it name a table, operation, and/or schema?
         → NO  → Ask: "What would you like to set up? Options: create tables,
                  configure policies, set up ingestion mappings, create materialized views."
                  STOP — do not proceed until user specifies.
         → YES → Continue to Step 1.
Step 1 → .show tables details                        // what exists?
Step 2 → .show table <TABLE> schema as json          // current columns
Step 3 → .show table <TABLE> policy retention        // current policies
Step 4 → Plan changes (create-merge, alter, etc.)
Step 5 → Execute changes
Step 6 → Verify: .show table <TABLE> schema as json  // confirm changes
```

### Script Generation Workflow

```text
Step 1 → Understand requirements from user
Step 2 → Generate KQL management commands
Step 3 → Save to .kql file
Step 4 → Deploy via az rest (one command at a time)
Step 5 → Verify deployed state matches intent
```

---

## Examples

### Example 1: Create Table with Policies and Mapping

```bash
# Create table
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".create-merge table SensorData (Timestamp: datetime, DeviceId: string, Temperature: real, Humidity: real, Location: dynamic)"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

```bash
# Set retention
cat > /tmp/kql_body.json << 'EOF'
{"db":"MyDB","csl":".alter table SensorData policy retention '{\"SoftDeletePeriod\":\"90.00:00:00\",\"Recoverability\":\"Enabled\"}'"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

```bash
# Set caching
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".alter table SensorData policy caching hot = 7d"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

```bash
# Create JSON mapping
cat > /tmp/kql_body.json << 'EOF'
{"db":"MyDB","csl":".create table SensorData ingestion json mapping 'SensorJsonMapping' '[{\"column\":\"Timestamp\",\"path\":\"$.ts\",\"datatype\":\"datetime\"},{\"column\":\"DeviceId\",\"path\":\"$.deviceId\",\"datatype\":\"string\"},{\"column\":\"Temperature\",\"path\":\"$.temp\",\"datatype\":\"real\"},{\"column\":\"Humidity\",\"path\":\"$.humidity\",\"datatype\":\"real\"},{\"column\":\"Location\",\"path\":\"$.location\",\"datatype\":\"dynamic\"}]'"}
EOF
```

> Execute `/tmp/kql_body.json` — see [Execute KQL Command](#execute-kql-command)

### Example 2: ETL with Update Policy

```kql
// 1. Target table
.create-merge table ParsedLogs (Timestamp: datetime, Level: string, Message: string, Source: string)

// 2. Transform function
.create-or-alter function ParseRawLogs() {
    RawLogs
    | extend J = parse_json(RawMessage)
    | project
        Timestamp = todatetime(J.timestamp),
        Level = tostring(J.level),
        Message = tostring(J.message),
        Source = tostring(J.source)
}

// 3. Attach update policy
.alter table ParsedLogs policy update
@'[{"IsEnabled":true,"Source":"RawLogs","Query":"ParseRawLogs()","IsTransactional":true}]'
```

---

## Agent Integration Notes

- This skill covers **authoring operations** — creating/altering database objects and ingesting data.
- For **read-only queries** and data exploration, switch to the `eventhouse-cli` consumption mode.
- For **cross-workload orchestration**, delegate to the **FabricDataEngineer** agent.
- All management commands require elevated database roles (`Admin` or `Ingestor`).
