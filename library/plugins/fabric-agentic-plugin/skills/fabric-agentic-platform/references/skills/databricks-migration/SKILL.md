---
name: databricks-migration
description: >
  Port Databricks notebooks and jobs to Microsoft Fabric. Provides an exhaustive dbutils
  to notebookutils substitution table: fs operations (runtime mounts or OneLake Shortcuts),
  secret scope to Key Vault URL conversion, notebook run and exit, widget replacement with
  parameter-tagged cells, and library install replacement with Fabric Environments.
  Covers Unity Catalog three-level namespace reduction to Lakehouse two-level schemas,
  DBFS path conversion to OneLake, Databricks Jobs to Spark Job Definitions, MLflow
  tracking URI removal, and Photon to Native Execution Engine substitution. Use when the
  user wants to: (1) replace dbutils with notebookutils, (2) collapse Unity Catalog
  namespaces to Lakehouse schemas, (3) convert Databricks Jobs or Delta Live Tables.
  Triggers: "migrate from databricks", "databricks to fabric", "dbutils to notebookutils",
  "dbutils fabric", "unity catalog migration", "dbfs to onelake",
  "databricks notebook migration", "delta live tables fabric", "photon native execution".
---

> **Telemetry — MANDATORY.** Every `api.fabric.microsoft.com` call must carry
> `x-ms-fabric-skill: databricks-migration` (`az rest`: `--headers "x-ms-fabric-skill=databricks-migration"`),
> including every LRO poll, `fabric_lro` and retry. Snippets omit it — add it anyway.

> **CRITICAL NOTES**
> 1. To find workspace details (including its ID) from a workspace name: list all workspaces, then use JMESPath filtering
> 2. To find item details (including its ID) from workspace ID, item type, and item name: list all items of that type in that workspace, then use JMESPath filtering
> 3. `dbutils.widgets` has **no direct equivalent** in Fabric — use notebook parameters (cell tag `parameters`); `notebookutils.runtime.context` is execution metadata, not parameter storage. If showing context fields, use documented names such as `currentWorkspaceId`, `currentWorkspaceName`, `currentNotebookId`, `currentNotebookName`, `isForPipeline`, and `isForInteractive`; `activityId` is the Livy job ID
> 4. `dbutils.library` (runtime library install) has **no equivalent** — use Fabric Environments for reproducible library management
> 5. Unity Catalog uses a 3-level namespace (`catalog.schema.table`); Fabric Lakehouse uses 2-level (`schema.table` within a named Lakehouse)
> 6. For an under-specified workspace-wide migration, ask focused questions about inventory, workload topology, security, data locations, and runtime constraints before recommending a Fabric topology
> 7. A completed Fabric migration must not retain executable `dbutils.*` calls in dual-runtime branches or `try/except` guards — replace the calls and Databricks paths outright

# Databricks → Microsoft Fabric Migration

## Prerequisite Knowledge

Read these companion documents before executing migration tasks:

- [COMMON-CORE.md](../../common/COMMON-CORE.md) — Fabric REST API patterns, authentication, token audiences, item discovery
- [COMMON-CLI.md](../../common/COMMON-CLI.md) — `az rest`, `az login`, token acquisition, Fabric REST via CLI
- [SPARK-AUTHORING-CORE.md](../../common/SPARK-AUTHORING-CORE.md) — Notebook deployment, lakehouse creation, Spark job execution

For notebook and Lakehouse creation, see [spark-cli](../spark-cli/SKILL.md).
For Fabric Warehouse DDL/DML authoring, see [sqldw-cli](../sqldw-cli/SKILL.md).

---

## Table of Contents

| Topic | Reference |
|---|---|
| Migration Workload Map | [§ Migration Workload Map](#migration-workload-map) |
| Complete `dbutils` → `notebookutils` Mapping | [dbutils-to-notebookutils.md](resources/dbutils-to-notebookutils.md) |
| Unity Catalog → Fabric Lakehouse Schemas | [catalog-migration.md](resources/catalog-migration.md) |
| Before/After Code Patterns | [code-patterns.md](resources/code-patterns.md) |
| Cluster Config → Fabric Spark Pools | [§ Cluster Config → Fabric Spark Pools](#cluster-config--fabric-spark-pools) |
| Databricks Jobs → Spark Job Definitions | [§ Databricks Jobs → Spark Job Definitions](#databricks-jobs--spark-job-definitions) |
| Delta Sharing → Fabric External Data Sharing and OneLake Shortcuts | [§ Delta Sharing → Fabric External Data Sharing and OneLake Shortcuts](#delta-sharing--fabric-external-data-sharing-and-onelake-shortcuts) |
| MLflow → Fabric ML Experiments | [§ MLflow → Fabric ML Experiments](#mlflow--fabric-ml-experiments) |
| Must / Prefer / Avoid | [§ Must / Prefer / Avoid](#must--prefer--avoid) |
| Authentication & Token Acquisition | [COMMON-CORE.md § Authentication](../../common/COMMON-CORE.md#authentication--token-acquisition) |
| Lakehouse Management | [SPARK-AUTHORING-CORE.md § Lakehouse Management](../../common/SPARK-AUTHORING-CORE.md#lakehouse-management) |
| Notebook Management | [SPARK-AUTHORING-CORE.md § Notebook Management](../../common/SPARK-AUTHORING-CORE.md#notebook-management) |

---

## Migration Workload Map

| Databricks Component | Fabric Target | Notes |
|---|---|---|
| **All-purpose cluster** (notebooks, REPL) | Fabric Notebook (Starter Pool or Custom Pool) | No persistent cluster — Fabric provisions compute on session start |
| **Job cluster** (automated jobs) | **Spark Job Definition (SJD)** | SJD maps one-to-one with Databricks Jobs on job clusters |
| **Unity Catalog** | **Fabric Lakehouse** (schema per namespace) | See [catalog-migration.md](resources/catalog-migration.md) |
| **Databricks Repos** (Git-backed notebooks) | **Fabric Git Integration** | Connect workspace to Azure DevOps or GitHub; notebooks are synced |
| **Delta Live Tables (DLT)** | **Fabric Notebooks** + **Data Pipelines** | No DLT equivalent — rewrite DLT datasets as parameterized notebook cells with pipeline orchestration |
| **Databricks SQL Warehouses** | **Fabric Warehouse** or **Lakehouse SQL Endpoint** | SQL warehouse sessions → Warehouse (for write) or SQL Endpoint (for read-only) |
| **MLflow Tracking** | **Fabric ML Experiments** | MLflow SDK is supported in Fabric — see [§ MLflow](#mlflow--fabric-ml-experiments) |
| **Delta Sharing** | **OneLake Shortcuts** + **Fabric external data sharing** | See [§ Delta Sharing → Fabric External Data Sharing and OneLake Shortcuts](#delta-sharing--fabric-external-data-sharing-and-onelake-shortcuts) |
| **Databricks Feature Store** | **Fabric Feature Store** (preview) | Direct conceptual equivalent; APIs differ |
| **dbutils** (all sub-modules) | **`notebookutils`** (most sub-modules) | See [dbutils-to-notebookutils.md](resources/dbutils-to-notebookutils.md) for full mapping |

---

## `dbutils` → `notebookutils` Quick Reference

The complete side-by-side API table is in [dbutils-to-notebookutils.md](resources/dbutils-to-notebookutils.md). The key mappings are:

| `dbutils` Call | `notebookutils` Equivalent | Compatibility Note |
|---|---|---|
| `dbutils.fs.ls(path)` | `notebookutils.fs.ls(path)` | **Direct replacement** |
| `dbutils.fs.cp(src, dest)` | `notebookutils.fs.cp(src, dest)` | **Direct replacement** |
| `dbutils.fs.mv(src, dest)` | `notebookutils.fs.mv(src, dest, create_path, overwrite=False)` | ⚠️ Signature differs — see [dbutils-to-notebookutils.md](resources/dbutils-to-notebookutils.md) |
| `dbutils.fs.rm(path, recurse)` | `notebookutils.fs.rm(path, recurse)` | **Direct replacement** |
| `dbutils.fs.mkdirs(path)` | `notebookutils.fs.mkdirs(path)` | **Direct replacement** |
| `dbutils.fs.put(path, contents)` | `notebookutils.fs.put(path, contents)` | **Direct replacement** |
| `dbutils.fs.head(path, maxBytes)` | `notebookutils.fs.head(path, max_bytes)` | ⚠️ Default differs — Python/Scala 100 KB, R 64 KB. See [dbutils-to-notebookutils.md](resources/dbutils-to-notebookutils.md) |
| `dbutils.fs.mount(...)` | `notebookutils.fs.mount(source, mountPoint, extraConfigs=None)` | ✅ **Supported** — Microsoft Entra (default), `accountKey`, or `sasToken` auth. For cross-workspace / persistent sharing, prefer **OneLake Shortcuts** |
| `dbutils.secrets.get(scope, key)` | `notebookutils.credentials.getSecret(keyVaultUrl, secretName)` | Scope → Key Vault URL; key → secret name |
| `dbutils.notebook.run(path, timeout, args)` | `notebookutils.notebook.run(name, timeout, args)` | `path` → notebook `name` (relative to workspace) |
| `dbutils.notebook.exit(value)` | `notebookutils.notebook.exit(value)` | **Direct replacement** |
| `dbutils.widgets.get(name)` | See [§ Widgets Migration](#widgets-migration) | No direct equivalent |
| `dbutils.library.install(...)` | **Not available at runtime** — use **Fabric Environments** | `dbutils.library.restartPython()` → `notebookutils.session.restartPython()` |
| `dbutils.data.summarize(df)` | `display(df.summary())` | Use `display()` or pandas `describe()` |

### Widgets Migration

`dbutils.widgets` has no direct equivalent in Fabric. Use these patterns instead:

| Use Case | Fabric Pattern |
|---|---|
| Pass parameter from parent notebook | Mark a cell in the child notebook as a **parameters cell** (notebook UI: cell "..." menu → "Mark cell as parameters"). The parent calls `notebookutils.notebook.run("child", arguments={"param": "value"})` — at runtime the engine inserts a new cell beneath the parameters cell that overrides the defaults |
| Pipeline-driven parameterization | Same parameters-cell mechanism; the Fabric Pipeline notebook activity supplies override values via its **Base parameters** setting |
| Centralized cross-notebook config | Use `notebookutils.variableLibrary.getLibrary("<name>")` to read values from a Variable Library item (deployment pipelines activate the right value set per stage) |
| Interactive selection in notebook | Use `display()` with input cells, IPython widgets (Python only), or Fabric Data Activator |

> Note: `notebookutils.runtime.context` does **not** expose parameter values. It's for execution metadata (workspace/notebook/activity/user IDs, pipeline-vs-interactive flags, etc.). See [dbutils-to-notebookutils.md § Runtime Context](resources/dbutils-to-notebookutils.md#runtime-context).

---

## Cluster Config → Fabric Spark Pools

| Databricks Cluster Concept | Fabric Spark Equivalent | Notes |
|---|---|---|
| All-purpose cluster (interactive) | **Starter Pool** | Auto-provisioned; no config; ideal for notebooks |
| Job cluster (single-use for jobs) | **Custom Pool** (or Starter Pool) attached to SJD | Configure node size, autoscale in Fabric capacity settings |
| Node type (e.g., `Standard_DS3_v2`) | **Fabric node size** (Small/Medium/Large/X-Large/XX-Large) | Map by vCore/memory ratio |
| Autoscale min/max workers | Custom Pool **min/max node** settings | Available in workspace Spark settings |
| `spark.conf` in cluster settings | **Fabric Environment** Spark properties | Move to Environment item; attach to workspace or notebook |
| `init_scripts` (cluster init) | **Fabric Environment** install script | Not fully equivalent — only library installs are supported |
| Databricks Runtime version | **Fabric Runtime** (1.1 = Spark 3.3, 1.2 = Spark 3.4, 1.3 = Spark 3.5) | Choose matching Spark version; test deprecated APIs |
| Photon accelerator | **Fabric Native Execution Engine (NEE)** | Enable in workspace Spark settings; vectorized execution similar to Photon |

---

## Databricks Jobs → Spark Job Definitions

| Databricks Jobs Concept | Fabric SJD Equivalent | Notes |
|---|---|---|
| Job with single notebook task | **SJD** referencing a notebook | Attach a default Lakehouse; pass parameters via SJD args |
| Multi-task job (DAG of tasks) | **Fabric Data Pipeline** orchestrating multiple SJDs/notebooks | Pipeline activities map to job tasks; dependencies = activity dependencies |
| Job schedule (cron) | **Pipeline schedule trigger** | Cron expression → recurrence trigger in pipeline |
| Job parameters | **SJD default arguments** or **notebook cell parameters** | Parameters cell in notebook is injected at runtime |
| Job clusters per task | **Pool attached to SJD** | Each SJD can specify its Spark pool independently |
| Databricks Workflows | **Fabric Data Pipelines** | Full DAG orchestration with conditions, loops, and failure branches |

> **Delegate to `spark-cli`** for SJD creation and notebook deployment.

---

## Delta Sharing → Fabric External Data Sharing and OneLake Shortcuts

| Databricks Delta Sharing Pattern | Fabric Equivalent |
|---|---|
| Provider publishes a Delta share | Fabric **external data sharing** for cross-tenant Fabric data, or a OneLake Shortcut to ADLS Gen2 where the Delta data resides |
| Recipient reads shared data | Accept the external data share into a Lakehouse (Fabric creates a read-only OneLake Shortcut), or create a direct **OneLake Shortcut** to accessible ADLS Gen2 data |
| Cross-workspace table sharing within org | **OneLake Shortcuts** pointing to another workspace's Lakehouse tables — no data copy |
| Cross-tenant sharing | Fabric **external data sharing** — live, read-only, in-place access through a shortcut in the recipient tenant |

When producing a migration workload map, include both paths: direct OneLake Shortcuts for accessible ADLS or same-tenant OneLake data, and Fabric external data sharing for native cross-tenant recipient sharing.

---

## MLflow → Fabric ML Experiments

Fabric ML Experiments are built on the MLflow SDK — most code is directly portable:

| Databricks MLflow Pattern | Fabric Equivalent | Migration Action |
|---|---|---|
| `mlflow.set_tracking_uri("databricks")` | Remove — Fabric tracking is automatic | Delete this line in Fabric notebooks |
| `mlflow.set_experiment("/path/exp")` | `mlflow.set_experiment("experiment_name")` | Use name only (not path); Fabric creates the Experiment item |
| `mlflow.log_metric(...)` | `mlflow.log_metric(...)` — **identical** | No change |
| `mlflow.log_artifact(...)` | `mlflow.log_artifact(...)` — **identical** | No change |
| `mlflow.autolog()` | `mlflow.autolog()` — **identical** | No change |
| `mlflow.register_model(...)` | `mlflow.register_model(...)` — **identical** | Model Registry is available in Fabric ML |
| Databricks Model Serving | **Azure ML Online Endpoints** or **Fabric Data Activator** | No direct Fabric model serving yet — use Azure ML |

---

## Must / Prefer / Avoid

### MUST DO
- **Inventory before prescribing a workspace topology** — for workspace-wide requests that omit workload inventory, dependencies, security requirements, data locations, or runtime constraints, ask focused clarifying questions and present conditional choices before selecting a Fabric design
- **Replace all `dbutils.*` calls** using the mapping in [dbutils-to-notebookutils.md](resources/dbutils-to-notebookutils.md) — `dbutils` is not available in Fabric notebooks
- **Migrate `dbutils.fs.mount()` to `notebookutils.fs.mount()`** (✅ supported — Microsoft Entra default, or `accountKey` / `sasToken` from Key Vault). For cross-workspace or persistent sharing, prefer **OneLake Shortcuts** instead. Always pair `mount()` with `unmount()` in `try/finally` — Fabric mounts are not released automatically on session end
- **Replace `dbutils.secrets.get(scope, key)`** with `notebookutils.credentials.getSecret(keyVaultUrl, secretName)` — secret scopes map to Azure Key Vault URLs
- **Redesign widget-based parameter passing** using notebook **parameters cells** (cell "..." menu → "Mark cell as parameters"); use `notebookutils.variableLibrary` for centralized cross-notebook config. `notebookutils.runtime.context` does **not** expose parameter values
- **Replace `dbutils.library.install*()`** with Fabric **Environments** — runtime library installs are not supported in production. `dbutils.library.restartPython()` maps to `notebookutils.session.restartPython()` (Python / PySpark only)
- **Adapt Unity Catalog 3-level namespaces** (`catalog.schema.table`) to Fabric 2-level (`schema.table` within a Lakehouse) — see [catalog-migration.md](resources/catalog-migration.md)
- **Map Databricks cluster init scripts** to Fabric Environments — cluster-level library installs must move to Environment items

### PREFER
- **Fabric Native Execution Engine (NEE)** as the Photon equivalent — enable in workspace Spark settings for vectorized execution on Delta Lake
- **OneLake Shortcuts** over data copy for Delta tables that already exist in ADLS Gen2 — point directly without re-ingesting
- **Fabric Git Integration** as the replacement for Databricks Repos — connect workspace to ADO or GitHub for notebook version control
- **Fabric ML Experiments** for direct MLflow continuity — tracking code requires minimal changes (remove `set_tracking_uri`)
- **Medallion architecture** when restructuring migrated Databricks catalogs — align `bronze`, `silver`, `gold` Unity Catalog schemas to separate Fabric Lakehouses
- **Starter Pool** for migrating interactive notebook workflows — eliminates cluster startup time that was a common pain point in Databricks job clusters

### AVOID
- **Do not prescribe a one-size-fits-all workspace topology** when the source inventory and migration constraints are missing
- **Do not import `dbutils` or attempt `dbutils = ...` assignments** in Fabric notebooks — import attempts fail with `ModuleNotFoundError`, while unresolved `dbutils` references raise `NameError`; always use `notebookutils`
- **Do not retain `dbutils.*` calls behind runtime-detection guards** (`try/except`, `if IS_DATABRICKS`) — replace the calls and Databricks paths outright with `notebookutils` and Fabric paths
- **Do not assume Unity Catalog governance policies transfer automatically** — RBAC, row-level security, and column masking must be reconfigured in Fabric using workspace roles and Lakehouse permissions
- **Do not use `%pip install` in production Fabric notebooks** at runtime — use Fabric Environments for stable, versioned library management
- **Do not attempt to port Delta Live Tables (DLT) pipelines verbatim** — DLT has no Fabric equivalent; rewrite as parameterized notebooks orchestrated by Fabric Pipelines
- **Do not rely on Databricks-specific Spark configurations** (e.g., `spark.databricks.*`) — these are proprietary and will be silently ignored or raise errors in Fabric
- **Do not use DBFS paths** (`dbfs:/...`) — there is no DBFS in Fabric; all paths must use OneLake `abfss://` or Lakehouse-relative paths

---

## Examples

See [dbutils-to-notebookutils.md](resources/dbutils-to-notebookutils.md) and [code-patterns.md](resources/code-patterns.md) for the full mapping. Key quick references:

**`dbutils.fs` → `notebookutils.fs`**

```python
# Databricks
dbutils.fs.ls("/mnt/bronze/orders/")
dbutils.fs.cp("/mnt/raw/file.csv", "/mnt/archive/file.csv")

# Fabric (replace DBFS/mount paths with OneLake relative paths)
notebookutils.fs.ls("Files/bronze/orders/")
notebookutils.fs.cp("Files/raw/file.csv", "Files/archive/file.csv")
```

**`dbutils.secrets` → `notebookutils.credentials`**

```python
# Databricks
pwd = dbutils.secrets.get(scope="prod", key="db-password")

# Fabric (scope → Key Vault URL, key → secret name)
pwd = notebookutils.credentials.getSecret("https://myvault.vault.azure.net/", "db-password")
```

**Unity Catalog namespace → Lakehouse schema**

```python
# Databricks
df = spark.read.table("prod.silver.customers")

# Fabric (catalog dropped; Lakehouse context provides it)
df = spark.read.table("silver.customers")
```
