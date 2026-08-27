# Development Workflow — Skill Resource

Essential workflow patterns for Spark notebook development in Microsoft Fabric.

## Recommended patterns

### Must

1. **Always validate notebook JSON structure** before deployment — malformed JSON causes deployment failures
2. **Use base64 encoding** for notebook content in Fabric API calls — required by REST API specification
3. **Test locally first** with sample data before deploying to Fabric — catch logic errors early
4. **Use parameterized notebooks** for reusability across environments — avoid hardcoded values
5. **Follow PySpark best practices** — proper DataFrame operations, avoid driver memory issues

### Prefer

1. **Local development workflow** — develop in Jupyter locally, validate, then deploy to Fabric
2. **Session reuse** over creating new sessions — faster iteration during development
3. **Incremental development** — test small changes before full deployments

### Avoid

1. **Don't hardcode connection strings** or workspace IDs — use parameters and configuration
2. **Don't skip local testing** — always validate transformation logic before deploying
3. **Don't commit secrets** to notebooks — use secure parameter passing and Azure Key Vault

---

## Notebook Lifecycle

### Development Phase
Guide LLM to generate notebooks following:
1. **Local development**: Create `.ipynb` file with Jupyter, use local Spark session for testing
2. **Cell structure**: Organize as Parameters → Setup → Logic → Validation → Cleanup
3. **Parameter cell**: First code cell should define configurable parameters with defaults
4. **Imports cell**: Import all dependencies upfront to catch missing packages early
5. **Validation cell**: Add checks at end to validate output (row counts, schema, sample data)

### Deployment Phase
Prompt LLM to generate deployment commands:
1. **Convert to JSON**: Notebook must be valid JSON with cells array
2. **Base64 encode**: Content must be base64-encoded for Fabric REST API
3. **Create notebook item**: POST to `/workspaces/{id}/items` with type="Notebook"
4. **Update definition**: POST to `/workspaces/{id}/items/{notebookId}/updateDefinition` with payload

### Execution Phase
Guide LLM for execution patterns:
1. **On-demand execution**: POST to Livy sessions endpoint to run notebook interactively
2. **Pipeline execution**: Embed notebook in pipeline activity with parameter overrides
3. **Scheduled execution**: Create a schedule via Job Scheduling in COMMON-CLI.md
4. **Monitoring**: Query Livy session state or pipeline run status to track progress

---

## Parameterization Patterns

> For parameterization patterns (when to parameterize, parameter injection methods, Variable Library, configuration management), see [context-and-params.md](../../../../../common/notebook-authoring/context-and-params.md#parameterization-patterns). The section below covers Spark-specific development patterns only.


### Spark Session Configuration & Runtime

**Agents must fetch official docs for details** — use the URLs below, not local descriptions.

| Topic | Fetch URL | Keywords |
|---|---|---|
| %%configure magic command | https://learn.microsoft.com/en-us/fabric/data-engineering/author-execute-notebook#spark-session-configuration-magic-command | `%%configure`, `driverMemory`, `executorMemory`, `driverCores`, `executorCores`, `numExecutors`, `defaultLakehouse`, `mountPoints`, `sessionTimeoutInSeconds`, `useStarterPool`, `useWorkspacePool`, `conf`, Variable Library, session restart, `-f` flag |
| Parameterized %%configure from pipeline | https://learn.microsoft.com/en-us/fabric/data-engineering/author-execute-notebook#parameterized-session-configuration-from-a-pipeline | `parameterName`, `defaultValue`, pipeline notebook activity, override %%configure, parameterized session config |
| Spark compute (pools, node sizes, autoscale) | https://learn.microsoft.com/en-us/fabric/data-engineering/spark-compute | starter pool, custom Spark pool, node size (Small/Medium/Large/XL/XXL), vCores, autoscale, dynamic allocation, capacity units, single-node pool |

---

## Local Testing Strategy

### Setup Local Environment
Prompt LLM to generate setup for:
1. **Install PySpark**: `pip install pyspark delta-spark` for local Spark session
2. **Install Jupyter**: `pip install jupyter notebook` for interactive development
3. **Sample data**: Create small CSV/Parquet files locally to simulate Fabric data
4. **Mock Fabric paths**: Use local file paths during dev, swap to `abfss://` for Fabric deployment

### Testing Transformation Logic
Guide LLM to test:
- **Create test DataFrame**: Use `spark.createDataFrame()` with sample data and explicit schema
- **Run transformation**: Execute the notebook's core logic on test data
- **Assert results**: Validate output row count, column values, schema matches expectations
- **Edge cases**: Test with nulls, empty DataFrames, duplicate keys

### Local vs Fabric Differences
Make LLM aware of:
- **Spark session**: Local requires explicit creation; Fabric provides pre-configured `spark` object
- **OneLake access**: Local can't access OneLake; use local files or mounted Azure Storage
- **Livy API**: Only available in Fabric; local testing can't validate Livy-specific features
- **Lakehouse tables**: Local uses Hive metastore; Fabric uses OneLake managed tables

---

## Debugging Patterns

### Livy Session Debugging
When errors occur in Fabric, guide LLM to:
1. **Check session state**: GET `/livyapi/versions/2023-12-01/sessions/{id}` to see if session is idle/busy/error
2. **Retrieve session log**: GET session log endpoint to see driver/executor logs
3. **Statement-level debugging**: Execute statements individually to isolate failing code
4. **Resource issues**: Check if error is memory-related (OOM), timeout, or network connectivity

### Common Error Patterns

**Schema mismatch**:
- Symptom: "Cannot merge incompatible schemas"
- Fix: Ensure source DataFrame columns match target table schema exactly
- Prevention: Define explicit schemas, validate before write

**Path not found**:
- Symptom: "Path does not exist: abfss://..."
- Fix: Verify lakehouse ID, file path, check OneLake permissions
- Prevention: Test paths with `.ls()` or simple read before complex operations

**Out of memory**:
- Symptom: "java.lang.OutOfMemoryError" or driver/executor crashes
- Fix: Add `.repartition()` or `.coalesce()`, reduce data volume, increase executor memory
- Prevention: Avoid `.collect()`, limit `.count()` calls, cache judiciously

**Livy session timeout**:
- Symptom: Session in "dead" state or statements not executing
- Fix: Recreate session, check network connectivity, verify lakehouse accessibility
- Prevention: Use session heartbeat, handle long-running operations with checkpoints

### Logging Best Practices
Prompt LLM to add logging:
- **Progress indicators**: Log after each major step (read, transform, write)
- **Row counts**: Log DataFrame counts to track data flow
- **Timing**: Record start/end timestamps for performance analysis
- **Error context**: Log input parameters, DataFrame sample when errors occur

### Incremental Debugging Strategy
Guide LLM to debug systematically:
1. **Isolate failure**: Comment out sections to identify failing cell
2. **Simplify input**: Test with small sample (`.limit(100)`) to reproduce faster
3. **Add visibility**: Insert `.show()` and `.printSchema()` to inspect intermediate state
4. **Check assumptions**: Validate data types, nulls, distributions match expectations
5. **Divide and conquer**: Break complex transformations into smaller steps with validation between
