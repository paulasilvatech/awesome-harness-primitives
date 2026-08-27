# Post-Migration Validation & Testing

Systematic verification that all migrated items work correctly in Fabric before cutover.

> **Script pattern**: Sections below show function signatures and key logic outlines. Generate the full runnable Python script on demand when the user needs it — this keeps the resource compact and reduces token load.

> **When to run**: Validation is designed to run **incrementally after each phase**, not only at the end. Each phase resource includes an optional validation checkpoint that cross-references the relevant section below.
>
> | After Phase | Run These Sections | Gate |
> |---|---|---|
> | Phase 0 (Environments) | V1 | Do not proceed to Phase 1 until Environments publish and libraries import |
> | Phase 1 (Lakehouses) | V2 | Do not proceed to Phase 2 until shortcuts are healthy and row counts match |
> | Phase 2 (Notebooks) | V3 | Do not proceed to Phase 3 until critical notebooks execute successfully |
> | Phase 3 (SJDs) | V4, V5, V6 | Do not cut over until SJDs pass and the full validation report is green |
>
> **Auth token**: Use the token-acquisition recipe in [COMMON-CLI § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) with audience `https://api.fabric.microsoft.com`.

---

## Validation Workflow

```
Validation:
├── V1: Environment validation (Phase 0 outputs)
├── V2: Data validation (Phase 1 outputs — Lakehouses, shortcuts, tables)
├── V3: Notebook execution testing (Phase 2 outputs)
├── V4: SJD execution testing (Phase 3 outputs)
├── V5: Query result comparison (Synapse vs. Fabric)
└── V6: Generate validation report
```

---

## V1: Environment Validation

Verify that Fabric Environments created in Phase 0 are published and usable.

### Check Environment Publish Status

```
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}
```

Check `properties.publishDetails.state` — must be `"Success"`.

### Validate Libraries

Run a test notebook attached to each Environment to confirm libraries are available:

```python
# Verify critical libraries are importable
import_errors = []
# Map PyPI package names to importable module names where they differ
required_libs = {
    "pandas": "pandas",
    "scikit-learn": "sklearn",
    "httpx": "httpx",
}  # adjust to your Environment

for pkg, module in required_libs.items():
    try:
        __import__(module)
    except ImportError as e:
        import_errors.append(f"{pkg}: {e}")

if import_errors:
    print("❌ Missing libraries:")
    for err in import_errors:
        print(f"  {err}")
else:
    print("✅ All required libraries available")
```

### Validate Spark Config

```python
# Verify critical Spark properties carried over from Synapse pool
expected_configs = {
    "spark.sql.shuffle.partitions": "200",
    "spark.executor.memory": "8g",
    # add your expected configs
}

config_errors = []
for key, expected in expected_configs.items():
    actual = spark.conf.get(key, None)
    if actual != expected:
        config_errors.append(f"{key}: expected '{expected}', got '{actual}'")

if config_errors:
    print("❌ Spark config mismatches:")
    for err in config_errors:
        print(f"  {err}")
else:
    print("✅ All Spark configs match")
```

---

## V2: Data Validation

Verify that Lakehouses, shortcuts, and tables from Phase 1 are accessible and data-complete.

### Shortcut Health Check

```python
# Check all shortcuts are accessible
import json

schemas = ["sales", "marketing", "staging"]  # adjust to your schemas

shortcut_errors = []
for schema in schemas:
    try:
        tables_files = notebookutils.fs.ls(f"Tables/{schema}/")
        files_files = notebookutils.fs.ls(f"Files/{schema}/")
        print(f"✅ {schema}: {len(tables_files)} table shortcuts, {len(files_files)} file shortcuts")
    except Exception as e:
        shortcut_errors.append(f"{schema}: {e}")

if shortcut_errors:
    print("❌ Shortcut errors:")
    for err in shortcut_errors:
        print(f"  {err}")
```

### Row Count Comparison

Compare row counts between Synapse and Fabric for every migrated table.

**Step 1 — Collect Synapse row counts** (run in a Synapse notebook or via REST API):

```python
# Run in Synapse notebook — collect row counts for all tables
synapse_counts = {}
databases = spark.sql("SHOW DATABASES").collect()

for db_row in databases:
    db = db_row.namespace
    tables = spark.sql(f"SHOW TABLES IN {db}").collect()
    for tbl_row in tables:
        table_name = f"{db}.{tbl_row.tableName}"
        count = spark.sql(f"SELECT COUNT(*) AS cnt FROM {table_name}").first().cnt
        synapse_counts[table_name] = count
        print(f"  {table_name}: {count}")

# Save for comparison
import json
with open("/tmp/synapse_counts.json", "w") as f:
    json.dump(synapse_counts, f)
```

**Step 2 — Collect Fabric row counts and compare** (run in a Fabric notebook):

```python
# Run in Fabric notebook — compare against Synapse counts
import json

# Load Synapse counts (upload the JSON to Lakehouse Files/ or paste inline)
synapse_counts = {
    "sales.customers": 150000,
    "sales.orders": 2340000,
    "marketing.campaigns": 5200,
    # ... paste or load from file
}

# Collect Fabric counts
validation_results = []
for synapse_table, expected_count in synapse_counts.items():
    # Map Synapse database.table to Fabric schema.table
    fabric_table = synapse_table  # adjust if schema names differ
    try:
        actual_count = spark.sql(f"SELECT COUNT(*) AS cnt FROM {fabric_table}").first().cnt
        match = actual_count == expected_count
        validation_results.append({
            "table": synapse_table,
            "synapse_count": expected_count,
            "fabric_count": actual_count,
            "match": match,
            "diff": actual_count - expected_count,
        })
        status = "✅" if match else "❌"
        print(f"  {status} {fabric_table}: Synapse={expected_count}, Fabric={actual_count}, diff={actual_count - expected_count}")
    except Exception as e:
        validation_results.append({
            "table": synapse_table,
            "synapse_count": expected_count,
            "fabric_count": None,
            "match": False,
            "diff": None,
            "error": str(e),
        })
        print(f"  ❌ {fabric_table}: ERROR — {e}")

# Summary
passed = sum(1 for r in validation_results if r["match"])
failed = len(validation_results) - passed
print(f"\nRow count validation: {passed}/{len(validation_results)} passed, {failed} failed")
```

### Schema Comparison

Verify column names, types, and order match between Synapse and Fabric:

```python
def compare_schema(synapse_schema, fabric_table):
    """
    synapse_schema: list of (column_name, data_type) from Synapse
    fabric_table: fully qualified Fabric table name
    """
    fabric_cols = [(f.name, f.dataType.simpleString()) for f in spark.table(fabric_table).schema.fields]

    mismatches = []
    for i, (syn_col, syn_type) in enumerate(synapse_schema):
        if i >= len(fabric_cols):
            mismatches.append(f"Column '{syn_col}' missing in Fabric (position {i})")
            continue
        fab_col, fab_type = fabric_cols[i]
        if syn_col != fab_col:
            mismatches.append(f"Position {i}: name mismatch — Synapse '{syn_col}' vs Fabric '{fab_col}'")
        if syn_type != fab_type:
            mismatches.append(f"Column '{syn_col}': type mismatch — Synapse '{syn_type}' vs Fabric '{fab_type}'")

    if len(fabric_cols) > len(synapse_schema):
        extra = [f.name for f in spark.table(fabric_table).schema.fields[len(synapse_schema):]]
        mismatches.append(f"Extra columns in Fabric: {extra}")

    return mismatches
```

### Partition Validation (Non-Delta Tables Retained as Original Format)

For tables migrated with Option B (retain original format + `MSCK REPAIR TABLE`):

```python
# Compare partition counts
def validate_partitions(table_name, expected_partition_count):
    partitions = spark.sql(f"SHOW PARTITIONS {table_name}").collect()
    actual = len(partitions)
    match = actual == expected_partition_count
    status = "✅" if match else "❌"
    print(f"  {status} {table_name}: expected {expected_partition_count} partitions, got {actual}")
    return match
```

---

## V3: Notebook Execution Testing

Run each migrated notebook to verify it executes without errors.

### Execute Notebook via REST API

**Endpoint**: `POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{notebookId}/jobs/instances?jobType=RunNotebook`

Key functions (generate full implementation on demand):

```python
def run_notebook(notebook_id, notebook_name, timeout_minutes=30) -> tuple[str, float, str|None]:
    """Execute a notebook and wait for completion. Returns (status, duration_seconds, error).
    - Check GET .../jobs/instances for already-running jobs before submitting
    - POST to jobType=RunNotebook, extract job_id from Location header
    - Fallback: query job history if Location header missing
    - Delegate to _poll_job() for status polling
    """

def _poll_job(notebook_id, job_id, notebook_name, timeout_minutes) -> tuple[str, float, str|None]:
    """Poll GET .../jobs/instances/{job_id} every 15s until Completed, Failed, Cancelled, or timeout."""
```

### Batch Test All Notebooks

- List notebooks: `GET .../items?type=Notebook`
- Loop and call `run_notebook()` for each; collect `{name, id, status, duration_sec, error}`
- Print pass/fail summary

### Common Failure Patterns

| Error | Cause | Fix |
|---|---|---|
| `ImportError: No module named 'xxx'` | Missing library in Environment | Add to Environment → publish. See [library-compatibility.md](library-compatibility.md) |
| `AnalysisException: Table or view not found` | Lakehouse not attached or table not migrated | Check lakehouse binding (Phase 2, Step 4) or re-run Phase 1 |
| `AnalysisException: ... listDatabases` | Unsupported `spark.catalog` method | Refactor to Spark SQL. See [code-patterns.md](code-patterns.md#spark-catalog-api--unsupported-methods) |
| `Py4JJavaError: ... LinkedServiceBasedTokenProvider` | Synapse token provider not replaced | Refactor to `ClientCredsTokenProvider`. See [connector-refactoring.md](connector-refactoring.md) |
| `getSecretWithLS ... not supported` | Linked service secret method not replaced | Replace with `getSecret(vaultUrl, name)`. See [connector-refactoring.md](connector-refactoring.md) |
| `spark.read.synapsesql ... not found` | Synapse SQL connector not available | Replace with Delta read or JDBC. See [connector-refactoring.md](connector-refactoring.md) |
| `FileNotFoundException` or `403 Forbidden` on `abfss://` | Old Synapse storage path not updated | Update to OneLake path or create shortcut. See [code-patterns.md](code-patterns.md) |
| `DefaultLakehouse: missing name` | Notebook lakehouse binding incomplete | Re-bind with both `id` and `name` |

---

## V4: SJD Execution Testing

Run each migrated Spark Job Definition to verify it completes successfully.

### Execute SJD via REST API

**Endpoint**: `POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{sjdId}/jobs/instances?jobType=SparkJob`

Key functions (generate full implementation on demand — same pattern as V3 `run_notebook`):

```python
def run_sjd(sjd_id, sjd_name, timeout_minutes=60) -> tuple[str, float, str|None]:
    """Execute an SJD and wait for completion. Same submit+poll pattern as run_notebook but with jobType=SparkJob."""
```

- Batch test: `GET .../items?type=SparkJobDefinition`, loop `run_sjd()` for each, print pass/fail

### SJD-Specific Checks

| Check | How |
|---|---|
| Main file accessible | Verify the `.py`/`.jar` reference file exists in the Lakehouse or ADLS path |
| Reference files accessible | Check all auxiliary files listed in the SJD definition |
| Lakehouse context set | SJD must have at least one lakehouse associated |
| Environment bound | If the Synapse SJD used a non-default pool, verify the Environment is attached |

---

## V5: Query Result Comparison

For critical tables, compare actual query results (not just row counts) between Synapse and Fabric.

### Checksum Comparison

Compute a hash of key columns to detect data differences without transferring full datasets.

Key functions (generate full PySpark implementation on demand):

```python
def table_checksum(table_name, key_columns, value_columns) -> dict:
    """Compute a deterministic checksum for a table. Returns {table, row_count, checksum}.
    - Read spark.table(), sort by key_columns
    - md5(concat_ws) each row on key+value columns
    - Aggregate: count(*) + md5(concat(sort_array(collect_list(row_hash))))
    Run in BOTH Synapse and Fabric, compare checksum values.
    """

def compare_samples(synapse_df, fabric_df, key_columns, sample_size=100):
    """For mismatched checksums: sample keys from source, join both sides, subtract to find diffs."""
```

---

## V6: Generate Validation Report

Combine all validation results into a single report.

Generate the full report script on demand. It should accept these inputs and produce a markdown report:

```python
def generate_validation_report(
    workspace_id: str,
    env_results: list,      # [{name, publish_status, lib_check, config_check}]
    data_results: list,      # [{table, synapse_count, fabric_count, match}]
    notebook_results: list,  # [{name, status, duration_sec, error}]
    sjd_results: list,       # [{name, status, duration_sec, error}]
) -> str:
    """Build a markdown validation report with sections for V1–V4 + summary table.
    - Per-category tables with pass/fail icons
    - Summary row: READY FOR CUTOVER if all passed, else ISSUES REMAIN
    - Write to validation_report.md and print
    """
```

---

## Cutover Readiness Criteria

Do **not** decommission Synapse until all of the following are true:

| Criterion | Check |
|---|---|
| All Environments published successfully | V1 — publish status = Success |
| All required libraries available | V1 — no ImportError in test notebooks |
| All table row counts match | V2 — 0 mismatches |
| All shortcuts accessible | V2 — no FileNotFoundException or 403 errors |
| All notebooks execute without errors | V3 — 100% Completed |
| All SJDs execute without errors | V4 — 100% Completed |
| Critical query results match (checksums) | V5 — checksums equal for key tables |
| Downstream consumers rerouted | Power BI, APIs, scheduled pipelines point to Fabric |
| Monitoring active | Fabric Monitoring Hub showing successful runs for 1–2 weeks |

> **Parallel run recommended**: Run migrated workloads in Fabric alongside Synapse for at least 1–2 weeks before cutover. Compare outputs daily to catch edge cases (time-dependent logic, incremental loads, schema evolution).
