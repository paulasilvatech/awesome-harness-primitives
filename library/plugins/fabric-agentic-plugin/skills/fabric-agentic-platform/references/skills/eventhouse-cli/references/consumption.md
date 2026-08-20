<!-- Mode reference for the `eventhouse-cli` skill. Loaded on demand from `skills/eventhouse-cli/SKILL.md` when the request matches the `consumption` mode. -->

> **SCOPE BOUNDARY — READ-ONLY (mandatory)**
> This mode may run read-only KQL queries and `.show` commands only. Do not
> create, alter, ingest, drop, or otherwise mutate KQL objects. If the request
> requires a write, announce the mode switch and read `authoring.md` before
> issuing the first management command.

# eventhouse-cli consumption mode — Read-Only KQL Queries via CLI

## Table of Contents

| Task | Reference | Notes |
|---|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | **Mandatory** — *READ link first* [needed for finding workspace id by its name or item id by its name, item type, and workspace id] |
| Fabric Topology & Key Concepts | [COMMON-CORE.md § Fabric Topology & Key Concepts](../../../common/COMMON-CORE.md#fabric-topology--key-concepts) | |
| Environment URLs | [COMMON-CORE.md § Environment URLs](../../../common/COMMON-CORE.md#environment-urls) | KQL Cluster URI is per-item |
| Authentication & Token Acquisition | [COMMON-CORE.md § Authentication & Token Acquisition](../../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401; read before any auth issue |
| Core Control-Plane REST APIs | [COMMON-CORE.md § Core Control-Plane REST APIs](../../../common/COMMON-CORE.md#core-control-plane-rest-apis) | |
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
| Job Execution (CLI) | [COMMON-CLI.md § Job Execution](../../../common/COMMON-CLI.md#job-execution) | |
| OneLake Shortcuts | [COMMON-CLI.md § OneLake Shortcuts](../../../common/COMMON-CLI.md#onelake-shortcuts) | |
| Capacity Management (CLI) | [COMMON-CLI.md § Capacity Management](../../../common/COMMON-CLI.md#capacity-management) | |
| Composite Recipes | [COMMON-CLI.md § Composite Recipes](../../../common/COMMON-CLI.md#composite-recipes) | |
| Gotchas & Troubleshooting (CLI-Specific) | [COMMON-CLI.md § Gotchas & Troubleshooting (CLI-Specific)](../../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping, token expiry |
| Quick Reference: `az rest` Template | [COMMON-CLI.md § Quick Reference: az rest Template](../../../common/COMMON-CLI.md#quick-reference-az-rest-template) | |
| Quick Reference: Token Audience / CLI Tool Matrix | [COMMON-CLI.md § Quick Reference: Token Audience ↔ CLI Tool Matrix](../../../common/COMMON-CLI.md#quick-reference-token-audience--cli-tool-matrix) | Which `--resource` + tool for each service |
| Connection Fundamentals | [EVENTHOUSE-CONSUMPTION-CORE.md § Connection Fundamentals](../../../common/EVENTHOUSE-CONSUMPTION-CORE.md#connection-fundamentals) | Cluster URI discovery, `az rest`, REST API |
| Schema Discovery and Security | [EVENTHOUSE-CONSUMPTION-CORE.md § Schema Discovery and Security](../../../common/EVENTHOUSE-CONSUMPTION-CORE.md#schema-discovery-and-security) | Schema Discovery, Security — workspace roles + KQL DB roles |
| Monitoring and Diagnostics | [EVENTHOUSE-CONSUMPTION-CORE.md § Monitoring and Diagnostics](../../../common/EVENTHOUSE-CONSUMPTION-CORE.md#monitoring-and-diagnostics) | |
| Performance Best Practices | [EVENTHOUSE-CONSUMPTION-CORE.md § Performance Best Practices](../../../common/EVENTHOUSE-CONSUMPTION-CORE.md#performance-best-practices) | **Read before writing KQL** — time filters, `has` vs `contains` |
| Common Consumption Patterns | [EVENTHOUSE-CONSUMPTION-CORE.md § Common Consumption Patterns](../../../common/EVENTHOUSE-CONSUMPTION-CORE.md#common-consumption-patterns) | Time-series, Top-N, percentile, dynamic fields |
| Gotchas, Troubleshooting, and Quick Reference | [EVENTHOUSE-CONSUMPTION-CORE.md § Gotchas, Troubleshooting, and Quick Reference](../../../common/EVENTHOUSE-CONSUMPTION-CORE.md#gotchas-troubleshooting-and-quick-reference) | Gotchas and Troubleshooting (12 issues), Quick Reference: Consumption Capabilities by Scenario |
| Table and Column Discovery | [discovery-queries.md § Table and Column Discovery](consumption/discovery-queries.md#table-and-column-discovery) | Table Discovery, Column Statistics |
| Function and View Discovery | [discovery-queries.md § Function and View Discovery](consumption/discovery-queries.md#function-and-view-discovery) | Function Discovery, Materialized View Discovery |
| Policy Discovery | [discovery-queries.md § Policy Discovery](consumption/discovery-queries.md#policy-discovery) | |
| External Tables and Ingestion Mappings | [discovery-queries.md § External Tables and Ingestion Mappings](consumption/discovery-queries.md#external-tables-and-ingestion-mappings) | External Table Discovery, Ingestion Mapping Discovery |
| Security Discovery | [discovery-queries.md § Security Discovery](consumption/discovery-queries.md#security-discovery) | |
| Database Overview Script | [discovery-queries.md § Database Overview Script](consumption/discovery-queries.md#database-overview-script) | |
| Tool Stack | [SKILL.md § Tool Stack](#tool-stack) | |
| Connection | [SKILL.md § Connection](#connection) | eventhouse-specific `az rest` connection steps |
| Agentic Exploration ("Chat With My Data") | [SKILL.md § Agentic Exploration](#agentic-exploration) | **Start here** for data exploration |
| Running Queries | [SKILL.md § Running Queries](#running-queries) | `az rest`, output formatting, export |
| Monitoring | [SKILL.md § Monitoring](#monitoring) | |
| Must / Prefer / Avoid / Troubleshooting | [SKILL.md § Must / Prefer / Avoid / Troubleshooting](#must--prefer--avoid--troubleshooting) | **MUST DO / AVOID / PREFER** checklists |
| Examples | [SKILL.md § Examples](#examples) | |
| Agent Integration Notes | [SKILL.md § Agent Integration Notes](#agent-integration-notes) | |

---

## Tool Stack

| Tool | Purpose | Install |
|---|---|---|
| **az cli** | KQL queries and management commands via Kusto REST API; Fabric control-plane discovery | `winget install Microsoft.AzureCLI` |
| **jq** | JSON processing and output formatting | `winget install jqlang.jq` |

## Connection

### Step 1 — Discover KQL Database Query URI

```bash
# Get workspace ID (if not known)
WS_ID=$(az rest --method GET \
  --url "https://api.fabric.microsoft.com/v1/workspaces" \
  --resource "https://api.fabric.microsoft.com" \
  | jq -r '.value[] | select(.displayName=="MyWorkspace") | .id')

# List KQL Databases and get connection properties
az rest --method GET \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WS_ID}/kqlDatabases" \
  --resource "https://api.fabric.microsoft.com" \
  | jq '.value[] | {name: .displayName, id: .id, queryUri: .properties.queryServiceUri, dbName: .properties.databaseName}'
```

### Step 2 — Set Connection Variables

```bash
CLUSTER_URI="https://<cluster>.kusto.fabric.microsoft.com"
DB_NAME="MyKqlDatabase"
```

### Step 3 — Verify Connection

> **Important — body file pattern**: KQL queries contain `|` (pipe) characters which break shell
> escaping in both bash and PowerShell. **Always write the JSON body to a temp file** and reference
> it with `--body @<file>`. This is the recommended approach for all `az rest` KQL calls.
> On PowerShell, use `@{db="X";csl="..."} | ConvertTo-Json -Compress | Out-File $env:TEMP\kql_body.json -Encoding utf8NoBOM` then `--body "@$env:TEMP\kql_body.json"`.

```bash
# Write body to temp file (avoids pipe escaping issues)
cat > /tmp/kql_body.json << 'EOF'
{"db":"MyKqlDatabase","csl":"print Message = 'Connected successfully', Cluster = current_cluster_endpoint(), Timestamp = now()"}
EOF

az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'
```

---

## Agentic Exploration

### "Chat With My Data" — Discovery Sequence

When the user asks to explore or query an Eventhouse without specifying tables:

```kql
Step 1 → .show tables                                    // discover tables
Step 2 → .show table <TABLE> schema as json              // understand columns + types
Step 3 → <TABLE> | take 10                               // see sample data
Step 4 → <TABLE> | summarize count() by bin(Timestamp, 1h) | render timechart  // shape of data
Step 5 → Formulate targeted query based on user's question
```

### Schema-Aware Query Generation

After schema discovery, generate queries using actual column names and types:

```kql
// Example: user asks "show me errors in the last hour"
// After discovering table "AppEvents" with columns: Timestamp, Level, Message, Source
AppEvents
| where Timestamp > ago(1h)
| where Level == "Error"
| summarize ErrorCount = count() by Source, bin(Timestamp, 5m)
| order by ErrorCount desc
```

---

## Running Queries

### Via `az rest`

> **Always use the temp-file pattern** for `--body` — KQL pipes (`|`) break inline shell escaping.

```bash
# Run a KQL query
cat > /tmp/kql_body.json << 'EOF'
{"db":"MyDB","csl":"Events | where Timestamp > ago(1h) | count"}
EOF

az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'
```

### Output Formatting

```bash
# Pretty-print results as a table with jq
cat > /tmp/kql_body.json << 'EOF'
{"db":"MyDB","csl":".show tables"}
EOF

az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0] | [.Columns[].ColumnName] as $cols | .Rows[] | [$cols, .] | transpose | map({(.[0]): .[1]}) | add'

# Save results to file
cat > /tmp/kql_body.json << 'EOF'
{"db":"MyDB","csl":"Events | where Timestamp > ago(1h) | summarize count() by EventType"}
EOF

az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  --output-file results.json
```

---

## Monitoring

```kql
// Active queries
.show queries

// Recent commands (last hour)
.show commands
| where StartedOn > ago(1h)
| project StartedOn, CommandType, Text = substring(Text, 0, 80), Duration, State
| order by StartedOn desc

// Ingestion failures (for context when data seems stale)
.show ingestion failures
| where FailedOn > ago(24h)
| summarize count() by ErrorCode
| top 5 by count_
```

---

## Must / Prefer / Avoid / Troubleshooting

### Must

- **Always include time filters** — `where Timestamp > ago(...)` must be present on time-series tables.
- **Discover schema before querying** — run `.show tables` and `.show table T schema as json` first.
- **Use `has` for term search** — indexed and fast; only fall back to `contains` for substring needs.
- **Verify cluster URI** — KQL Database URIs are per-item; always resolve via Fabric REST API.

### Prefer

- **`az rest`** for CLI query sessions; **Fabric KQL MCP server** for agent-integrated workflows.
- **`project` early** to drop unneeded columns before aggregation.
- **`materialize()`** when a sub-expression is used multiple times.
- **`take 100`** for initial exploration; avoid full table scans.
- **`render timechart`** for time-series; `render piechart` for distribution.

### Avoid

- **`contains`** on large tables — full scan, not indexed. Use `has` or `has_cs`.
- **`join`** without filtering both sides first — causes memory explosion.
- **`SELECT *`** equivalent (`project` all columns) on wide tables.
- **Missing `bin()`** in time-series `summarize` — produces one row per unique timestamp.
- **Hardcoded cluster URIs** — always resolve from Fabric REST API or environment variables.

### Troubleshooting

| Symptom | Fix |
|---|---|
| `az rest` auth fails | Run `az login` first; ensure `--resource "https://kusto.kusto.windows.net"` is set |
| Empty results on valid table | Check database context; may need `database("name").table` |
| Query timeout | Add tighter time filter; check `.show queries` for competing queries |
| `Forbidden (403)` | Request `viewer` role on the KQL Database |
| Results truncated | Default limit is 500K rows; add `set truncationmaxrecords = N;` before query |
| KQL pipe `\|` breaks PowerShell or bash | **Never inline KQL in `--body`**. Write JSON to a temp file and use `--body @file.json` (see [Running Queries](#running-queries)) |

---

## Examples

### Example 1: Discover and Query

```bash
# 1. Set connection variables (after discovering URI via Step 1)
CLUSTER_URI="https://<your-cluster>.kusto.fabric.microsoft.com"
DB_NAME="SalesDB"

# 2. Discover tables
cat > /tmp/kql_body.json << EOF
{"db":"${DB_NAME}","csl":".show tables"}
EOF
az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'

# 3. Explore schema
cat > /tmp/kql_body.json << EOF
{"db":"${DB_NAME}","csl":".show table Orders schema as json"}
EOF
az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'

# 4. Sample data
cat > /tmp/kql_body.json << EOF
{"db":"${DB_NAME}","csl":"Orders | take 10"}
EOF
az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'
```

```kql
// 5. Analytical query (via az rest --body @file)
Orders
| where OrderDate > ago(30d)
| summarize
    TotalOrders = count(),
    TotalRevenue = sum(Amount)
    by bin(OrderDate, 1d)
| render timechart
```

### Example 2: Cross-Database Query

```kql
// Query across KQL databases in the same Eventhouse
let orders = database("SalesDB").Orders | where OrderDate > ago(7d);
let products = database("CatalogDB").Products;
orders
| join kind=inner (products) on ProductId
| summarize Revenue = sum(Amount) by ProductName
| top 10 by Revenue desc
```

### Example 3: Export Results to File

```bash
# Run query and save results to JSON
cat > /tmp/kql_body.json << 'EOF'
{"db":"MyDB","csl":"Events | where Timestamp > ago(1d) | summarize count() by EventType"}
EOF

az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  --output-file results.json

# Convert to CSV with jq
cat results.json \
  | jq -r '.Tables[0] | (.Columns | map(.ColumnName)), (.Rows[]) | @csv' > results.csv
```

---

## Agent Integration Notes

- This skill is **read-only** — it does not create, alter, or drop database objects.
- For authoring operations (table management, ingestion, policies), switch to the `eventhouse-cli` authoring mode.
- For cross-workload orchestration (Spark + SQL + KQL), delegate to the **FabricDataEngineer** agent.
- The **Fabric KQL MCP server** (`fabric-kql` in `mcp-setup/mcp-config-template.json`) can be used as an alternative to `az rest` for agent-integrated query execution.
