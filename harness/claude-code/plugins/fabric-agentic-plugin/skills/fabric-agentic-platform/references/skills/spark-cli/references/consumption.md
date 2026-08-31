<!-- Mode reference for the `spark-cli` skill. Loaded on demand from `skills/spark-cli/SKILL.md` when the request matches the `consumption` mode. -->

# Data Engineering Consumption — CLI Skill

## Table of Contents

| Task | Reference | Notes |
|---|---|---|
| Fabric Topology & Key Concepts | [COMMON-CORE.md § Fabric Topology & Key Concepts](../../../common/COMMON-CORE.md#fabric-topology--key-concepts) ||
| Environment URLs | [COMMON-CORE.md § Environment URLs](../../../common/COMMON-CORE.md#environment-urls) ||
| Authentication & Token Acquisition | [COMMON-CORE.md § Authentication & Token Acquisition](../../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401; read before any auth issue |
| Core Control-Plane REST APIs | [COMMON-CORE.md § Core Control-Plane REST APIs](../../../common/COMMON-CORE.md#core-control-plane-rest-apis) ||
| Pagination | [COMMON-CORE.md § Pagination](../../../common/COMMON-CORE.md#pagination) ||
| Long-Running Operations (LRO) | [COMMON-CORE.md § Long-Running Operations (LRO)](../../../common/COMMON-CORE.md#long-running-operations-lro) ||
| Rate Limiting & Throttling | [COMMON-CORE.md § Rate Limiting & Throttling](../../../common/COMMON-CORE.md#rate-limiting--throttling) ||
| OneLake Data Access | [COMMON-CORE.md § OneLake Data Access](../../../common/COMMON-CORE.md#onelake-data-access) | Requires `storage.azure.com` token, not Fabric token |
| Job Execution | [COMMON-CORE.md § Job Execution](../../../common/COMMON-CORE.md#job-execution) ||
| Capacity Management | [COMMON-CORE.md § Capacity Management](../../../common/COMMON-CORE.md#capacity-management) ||
| Gotchas & Troubleshooting | [COMMON-CORE.md § Gotchas & Troubleshooting](../../../common/COMMON-CORE.md#gotchas--troubleshooting) ||
| Best Practices | [COMMON-CORE.md § Best Practices](../../../common/COMMON-CORE.md#best-practices) ||
| Tool Selection Rationale | [COMMON-CLI.md § Tool Selection Rationale](../../../common/COMMON-CLI.md#tool-selection-rationale) ||
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | **Mandatory** — *READ link first* [needed for finding workspace id by its name or item id by its name, item type, and workspace id] |
| Authentication Recipes | [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) | `az login` flows and token acquisition |
| Fabric Control-Plane API via `az rest` | [COMMON-CLI.md § Fabric Control-Plane API via az rest](../../../common/COMMON-CLI.md#fabric-control-plane-api-via-az-rest) | **Always pass `--resource https://api.fabric.microsoft.com`** or `az rest` fails |
| Pagination Pattern | [COMMON-CLI.md § Pagination Pattern](../../../common/COMMON-CLI.md#pagination-pattern) ||
| Long-Running Operations (LRO) Pattern | [COMMON-CLI.md § Long-Running Operations (LRO) Pattern](../../../common/COMMON-CLI.md#long-running-operations-lro-pattern) ||
| OneLake Data Access via `curl` | [COMMON-CLI.md § OneLake Data Access via curl](../../../common/COMMON-CLI.md#onelake-data-access-via-curl) | Use `curl` not `az rest` (different token audience) |
| SQL / TDS Data-Plane Access | [COMMON-CLI.md § SQL / TDS Data-Plane Access](../../../common/COMMON-CLI.md#sql--tds-data-plane-access) | `sqlcmd` (Go) connect, query, CSV export |
| Job Execution (CLI) | [COMMON-CLI.md § Job Execution](../../../common/COMMON-CLI.md#job-execution) ||
| OneLake Shortcuts | [COMMON-CLI.md § OneLake Shortcuts](../../../common/COMMON-CLI.md#onelake-shortcuts) ||
| Capacity Management (CLI) | [COMMON-CLI.md § Capacity Management](../../../common/COMMON-CLI.md#capacity-management) ||
| Composite Recipes | [COMMON-CLI.md § Composite Recipes](../../../common/COMMON-CLI.md#composite-recipes) ||
| Gotchas & Troubleshooting (CLI-Specific) | [COMMON-CLI.md § Gotchas & Troubleshooting (CLI-Specific)](../../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping, token expiry |
| Quick Reference: `az rest` Template | [COMMON-CLI.md § Quick Reference: az rest Template](../../../common/COMMON-CLI.md#quick-reference-az-rest-template) ||
| Quick Reference: Token Audience / CLI Tool Matrix | [COMMON-CLI.md § Quick Reference: Token Audience ↔ CLI Tool Matrix](../../../common/COMMON-CLI.md#quick-reference-token-audience--cli-tool-matrix) | Which `--resource` + tool for each service |
| Relationship to SPARK-AUTHORING-CORE.md | [SPARK-CONSUMPTION-CORE.md § Relationship to SPARK-AUTHORING-CORE.md](../../../common/SPARK-CONSUMPTION-CORE.md#relationship-to-spark-authoring-coremd) ||
| Data Engineering Consumption Capability Matrix | [SPARK-CONSUMPTION-CORE.md § Data Engineering Consumption Capability Matrix](../../../common/SPARK-CONSUMPTION-CORE.md#data-engineering-consumption-capability-matrix) ||
| OneLake Table APIs (Schema-enabled Lakehouses) | [SPARK-CONSUMPTION-CORE.md § OneLake Table APIs (Schema-enabled Lakehouses)](../../../common/SPARK-CONSUMPTION-CORE.md#onelake-table-apis-schema-enabled-lakehouses) | Unity Catalog-compatible metadata; requires `storage.azure.com` token |
| Lakehouse Livy Session Management | [SPARK-CONSUMPTION-CORE.md § Livy Session Management](../../../common/SPARK-CONSUMPTION-CORE.md#livy-session-management) | Lakehouse Livy API: session creation, states, lifecycle, termination |
| Interactive Data Exploration | [SPARK-CONSUMPTION-CORE.md § Interactive Data Exploration](../../../common/SPARK-CONSUMPTION-CORE.md#interactive-data-exploration) | Statement execution, output retrieval, data discovery |
| PySpark Analytics Patterns | [SPARK-CONSUMPTION-CORE.md § PySpark Analytics Patterns](../../../common/SPARK-CONSUMPTION-CORE.md#pyspark-analytics-patterns) | Cross-lakehouse 3-part naming, performance optimization |
| Must/Prefer/Avoid | [SKILL.md § Must/Prefer/Avoid](#mustpreferavoid) | **MUST DO / AVOID / PREFER** checklists |
| Quick Start | [SKILL.md § Quick Start](#quick-start) | CLI-specific Lakehouse Livy session setup and data exploration |
| Key Fabric Patterns | [SKILL.md § Key Fabric Patterns](#key-fabric-patterns) | Spark pattern quick-reference table |
| Session Cleanup | [SKILL.md § Session Cleanup](#session-cleanup) | Clean up idle Lakehouse Livy sessions via CLI |

---

## Must/Prefer/Avoid

### MUST DO

- Check for existing idle sessions before creating new ones
- Use dynamic workspace/lakehouse discovery
- Follow API patterns from [COMMON-CLI.md](../../../common/COMMON-CLI.md)

### PREFER

- **sqldw-cli for simple lakehouse queries** — row counts, SELECT, schema exploration, filtering, and aggregation on lakehouse Delta tables should use the SQL Endpoint, not Spark. Only use this skill when the user explicitly requests PySpark, DataFrames, or Spark-specific features.
- SQL Endpoint for Delta tables
- Livy for unstructured/JSON data or complex Python analytics
- Session reuse over creation

### AVOID

- Hardcoded workspace IDs
- Creating unnecessary sessions
- Large result sets without LIMIT
- **Confusing Lakehouse Livy sessions with Notebook Spark sessions** — This skill covers **Lakehouse Livy sessions** (the public Livy API at `/lakehouses/{lhId}/livyapi/.../sessions`). Notebook Spark sessions are created internally when running a notebook via the Jobs API (`RunNotebook`) and are NOT managed through the Livy API. To run a notebook as a job, see SPARK-AUTHORING-CORE.md § Notebook Execution & Job Management
- **Writing or generating notebook cells** — prompts that ask for `%%sql`, `%%configure`, PySpark notebook cell code, notebook deployment, or notebook execution belong to `the `authoring` mode`, even when the cell queries data.

---

## Quick Start

### Environment Setup

Apply environment detection from COMMON-CORE.md Environment Detection Pattern to set:
- `$FABRIC_API_BASE` and `$FABRIC_RESOURCE_SCOPE`
- `$FABRIC_API_URL` and `$LIVY_API_PATH` for Livy operations

**Authentication**: Use token acquisition from [COMMON-CLI.md](../../../common/COMMON-CLI.md) Environment Detection and API Configuration

### Workspace & Item Discovery

**Preferred**: Use [COMMON-CLI.md](../../../common/COMMON-CLI.md) item discovery patterns (Finding things in Fabric) to find workspaces and items by name.

**Fallback** (when workspace is already known):
```bash
# List workspaces
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" --url "$FABRIC_API_URL/workspaces" --query "value[].{name:displayName, id:id}" --output table
read -p "Workspace ID: " workspaceId

# List lakehouses in workspace
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" --url "$FABRIC_API_URL/workspaces/$workspaceId/items?type=Lakehouse" --query "value[].{name:displayName, id:id}" --output table
read -p "Lakehouse ID: " lakehouseId
```

### Lakehouse Livy Session Management

> **Two types of Spark sessions in Fabric** — This skill manages **Lakehouse Livy sessions**, created via the public Livy API endpoint (`/lakehouses/{lhId}/livyapi/.../sessions`). These are ad-hoc interactive sessions for remote clients. **Notebook Spark sessions** are a separate mechanism — they are created internally when a Fabric Notebook is executed (via portal or Jobs API `RunNotebook`), and are managed through the notebook lifecycle, not the Livy API.

```bash
# Check for existing idle Lakehouse Livy session (avoid resource waste)
sessionId=$(az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions" --query "sessions[?state=='idle'][0].id" --output tsv)

# Create if none available - FORCE STARTER POOL USAGE
if [[ -z "$sessionId" ]]; then
    cat > /tmp/body.json << 'EOF'
{
    "name":"analysis",
    "driverMemory":"56g",
    "driverCores":8,
    "executorMemory":"56g",
    "executorCores":8,
    "conf": {
        "spark.dynamicAllocation.enabled": "true",
        "spark.fabric.pool.name": "Starter Pool"
    }
}
EOF
    sessionId=$(az rest --method post --resource "$FABRIC_RESOURCE_SCOPE" --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions" --body @/tmp/body.json --query "id" --output tsv)

    echo "⏳ Waiting for starter pool session to be ready..."
    # With starter pools, this should be 3-5 seconds
    timeout=30  # Reduced from 90s since starter pools are fast
    while [ $timeout -gt 0 ]; do
        state=$(az rest --resource "$FABRIC_RESOURCE_SCOPE" --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions/$sessionId" --query "state" --output tsv)
        if [[ "$state" == "idle" ]]; then
            echo "✅ Session ready in starter pool!"
            break
        fi
        echo "   Session state: $state (${timeout}s remaining)"
        sleep 3
        timeout=$((timeout - 3))
    done
fi
```

### Data Exploration (Fabric-Specific Patterns)
```bash
# Execute statement (LLM knows Python/Spark syntax)
cat > /tmp/body.json << 'EOF'
{
  "code": "spark.sql(\"SHOW TABLES\").show(); df = spark.table(\"your_table\"); df.describe().show()",
  "kind": "pyspark"
}
EOF
az rest --method post --resource "$FABRIC_RESOURCE_SCOPE" --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions/$sessionId/statements" --body @/tmp/body.json
```

## Key Fabric Patterns

| Pattern | Code | Use Case |
|---|---|---|
| **Table Discovery** | `spark.sql("SHOW TABLES")` | List available tables |
| **MLV Discovery** | `spark.sql("SHOW MATERIALIZED LAKE VIEWS IN <schema>")` | List Materialized Lake Views when the REST list endpoint is unavailable |
| **Cross-Lakehouse** | `spark.sql("SELECT * FROM other_workspace.table")` | Query across workspaces |
| **Delta Features** | `df.history()`, `df.readVersion(1)` | Time travel, versioning |
| **Schema Evolution** | `df.printSchema()` | Understand structure |

## Lakehouse Livy Session Cleanup
```bash
# Clean up idle Lakehouse Livy sessions (optional)
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions" --query "sessions[?state=='idle'].id" --output tsv | xargs -I {} az rest --method delete --resource "$FABRIC_RESOURCE_SCOPE" --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions/{}"
```

---

**Focus**: This skill provides Fabric-specific REST API patterns. LLM already knows Python/Spark syntax — we focus on Fabric integration, session management, and API endpoints.
