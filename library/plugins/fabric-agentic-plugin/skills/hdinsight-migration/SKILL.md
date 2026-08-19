---
name: hdinsight-migration
description: >
  Port Azure HDInsight Spark clusters and Hive workloads to Microsoft Fabric.
  Replaces legacy HiveContext and standalone SparkContext constructors with
  the pre-instantiated SparkSession. Converts WASB and ABFS storage paths to OneLake
  abfss URLs via Shortcuts. Transforms Hive DDL (STORED AS ORC, external tables) to
  Delta Lake schemas inside Fabric Lakehouse. Maps Oozie workflow actions — spark, hive,
  shell, sqoop, coordinator — to Fabric Pipeline activities and schedule triggers.
  Introduces notebookutils for file and credential operations previously handled via
  subprocess or HDFS client calls. Use when the user wants to:
  (1) retire an HDInsight cluster and move to Fabric,
  (2) convert WASB paths or Hive DDL,
  (3) replace Oozie coordinators with Fabric Pipelines.
  Triggers: "migrate from hdinsight", "hdi to fabric", "hivecontext sparksession fabric",
  "wasb to onelake", "hive ddl to delta", "oozie to fabric pipelines",
  "migrate an oozie action", "hive metastore lakehouse", "hdinsight spark migration".
---

> **Telemetry — MANDATORY.** Every `api.fabric.microsoft.com` call must carry
> `x-ms-fabric-skill: hdinsight-migration` (`az rest`: `--headers "x-ms-fabric-skill=hdinsight-migration"`),
> including every LRO poll, `fabric_lro` and retry. Snippets omit it — add it anyway.

> **CRITICAL NOTES**
> 1. To find workspace details (including its ID) from a workspace name: list all workspaces, then use JMESPath filtering
> 2. To find item details (including its ID) from workspace ID, item type, and item name: list all items of that type in that workspace, then use JMESPath filtering
> 3. HDInsight has no `mssparkutils` or `dbutils` equivalent — `notebookutils` is net-new capability being introduced
> 4. `HiveContext` and `SQLContext` are legacy Spark 1.x/2.x APIs — Fabric uses Spark 3.x `SparkSession` exclusively
> 5. `wasb://` paths are deprecated and require a Storage Account key or SAS — replace with OneLake shortcuts
> 6. Fabric cannot read or shortcut `hdfs://` directly. Its Pipeline HDFS connector supports Anonymous authentication only; export or bridge Kerberos sources to supported storage first.

# HDInsight → Microsoft Fabric Migration

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
| SparkSession & Context API Changes | [§ SparkSession API Changes](#sparksession--context-api-changes) |
| WASB / ABFS → OneLake Path Migration | [path-migration.md](resources/path-migration.md) |
| Hive DDL → Delta Lake / Lakehouse Schemas | [hive-to-delta.md](resources/hive-to-delta.md) |
| Oozie → Fabric Pipelines | [§ Oozie → Fabric Pipelines](#oozie--fabric-pipelines) |
| Introducing `notebookutils` | [§ Introducing notebookutils](#introducing-notebookutils) |
| Before/After Code Patterns | [code-patterns.md](resources/code-patterns.md) |
| Spark Configuration Differences | [§ Spark Configuration Differences](#spark-configuration-differences) |
| Must / Prefer / Avoid | [§ Must / Prefer / Avoid](#must--prefer--avoid) |
| Authentication & Token Acquisition | [COMMON-CORE.md § Authentication](../../common/COMMON-CORE.md#authentication--token-acquisition) |
| Lakehouse Management | [SPARK-AUTHORING-CORE.md § Lakehouse Management](../../common/SPARK-AUTHORING-CORE.md#lakehouse-management) |

---

## Migration Workload Map

| HDInsight Component | Fabric Target | Notes |
|---|---|---|
| **Spark cluster** (notebooks, scripts) | Fabric Spark (Lakehouse / Notebooks / SJD) | No persistent cluster — Starter Pool or Custom Pool provides on-demand Spark |
| **Hive / HiveServer2** | **Lakehouse SQL Endpoint** + Lakehouse schemas | Delta Lake replaces Hive metastore; schemas provide namespace equivalent |
| **HBase** | **Fabric Warehouse** or **Azure Cosmos DB** (separate from Fabric) | HBase has no direct Fabric equivalent — assess workload access patterns |
| **Oozie workflows** | **Fabric Data Pipelines** | Map Oozie actions to Fabric activities; see [§ Oozie → Fabric Pipelines](#oozie--fabric-pipelines) |
| **YARN Resource Manager** | **Fabric Spark monitoring** (Spark UI, Monitoring Hub) | No YARN — Fabric manages compute automatically |
| **Ambari** | **Fabric Monitoring Hub** + **Admin Portal** | Cluster health, capacity, and job monitoring |
| **WASB / ABFS storage** | **OneLake Shortcuts** → `abfss://workspace@onelake.dfs.fabric.microsoft.com/` | See [path-migration.md](resources/path-migration.md) |
| **Ranger policies** | **Fabric workspace roles** + **OneLake data access roles** | Map Ranger row/column filters to Lakehouse row-level security |
| **Livy REST server** | **Fabric Livy API** | Compatible endpoint — see SPARK-AUTHORING-CORE.md |

---

## SparkSession & Context API Changes

HDInsight Spark clusters often use legacy Spark 1.x / 2.x API styles. Replace all of these with the unified `SparkSession`:

| Legacy HDInsight Pattern | Fabric Spark 3.x Replacement |
|---|---|
| `from pyspark import SparkContext; sc = SparkContext()` | Not needed — `sc = spark.sparkContext` (pre-instantiated) |
| `from pyspark.sql import HiveContext; hc = HiveContext(sc)` | Not needed — `spark` session has Hive-compatible SQL support via Delta schemas |
| `from pyspark.sql import SQLContext; sqlc = SQLContext(sc)` | Not needed — use `spark.sql(...)` directly |
| `SparkSession.builder.enableHiveSupport().getOrCreate()` | Not needed in Fabric — `spark` is pre-built and available |
| `sc.textFile("wasb://container@account.blob.core.windows.net/path")` | `spark.read.text("abfss://workspace@onelake.dfs.fabric.microsoft.com/lh.Lakehouse/Files/path")` |
| `sqlContext.sql("CREATE TABLE ... STORED AS ORC")` | See [hive-to-delta.md](resources/hive-to-delta.md) for Delta DDL equivalent |

> In Fabric notebooks, `spark` (SparkSession) and `sc` (SparkContext) are **pre-instantiated** — do not call `SparkContext()` or `SparkSession.builder...getOrCreate()` at the top of migrated notebooks.

---

## Oozie → Fabric Pipelines

Map Oozie workflow actions to Fabric Data Pipeline activities:

| Oozie Action Type | Fabric Pipeline Activity | Notes |
|---|---|---|
| `<spark>` action | **Notebook activity** or **Spark Job Definition activity** | Pass parameters via notebook cell parameters or SJD arguments |
| `<hive>` action | **Script activity** (SQL) against Lakehouse SQL Endpoint | Convert HiveQL to Spark SQL or Delta SQL |
| `<shell>` action | **Azure Function activity** or **Web activity** | Shell scripts must be refactored; no direct shell execution in Fabric Pipelines |
| `<java>` action | **Azure Batch activity** (external) or refactor to PySpark | Java MapReduce jobs must be rewritten |
| `<sqoop>` action | **Copy Data activity** (Fabric Data Factory connector) | Sqoop import/export maps to Fabric Copy Data with JDBC source/sink |
| `<coordinator>` (time-based schedule) | **Pipeline schedule trigger** | Set recurrence in pipeline trigger; supports cron-like expressions |
| `<coordinator>` (data-triggered) | **Storage Event trigger** | Trigger on OneLake file arrival |

> **Delegate to `spark-cli`** for notebook and SJD creation after mapping pipeline activities.

---

## Introducing `notebookutils`

HDInsight Spark had no built-in utility framework equivalent to `mssparkutils` or `dbutils`. When migrating to Fabric, introduce `notebookutils` for common operations:

| Operation | Old HDInsight Approach | `notebookutils` Equivalent |
|---|---|---|
| List files | `dbutils` (N/A) / HDFS CLI | `notebookutils.fs.ls("abfss://...")` |
| Copy file | HDFS API / `shutil` | `notebookutils.fs.cp(src, dest)` |
| Read secret | Azure Key Vault REST call | `notebookutils.credentials.getSecret(keyVaultUrl, secretName)` |
| Get notebook context | Not available | `notebookutils.runtime.context` — returns workspace ID, notebook ID, etc. |
| Run child notebook | Not available | `notebookutils.notebook.run("notebook_name", timeout, {"param": "value"})` |
| Exit notebook with value | `sys.exit()` | `notebookutils.notebook.exit("value")` |
| Mount storage | WASB config in `spark-defaults.conf` | OneLake Shortcut (no runtime mount needed) |

---

## Spark Configuration Differences

| HDInsight Concept | Fabric Spark Equivalent | Migration Action |
|---|---|---|
| `spark-defaults.conf` (cluster-wide) | Fabric **Spark Workspace Settings** + **Environment** item | Move config properties to Environment or use `%%configure` in notebooks |
| `%%configure` magic | `%%configure` magic — **identical** | No change needed |
| YARN queue / resource allocation | **Fabric Spark pool** node size and autoscale settings | Map queue SLAs to Custom Pool configuration |
| Ambari service configs (HDFS, YARN tuning) | Not applicable — Fabric manages infrastructure | Remove; focus on application-level Spark configs |
| HDI Spark version (e.g., Spark 2.4) | Fabric Runtime 1.3 = Spark 3.5 (latest) | Test for deprecated API removals (e.g., `HiveContext`, RDD-style ML) |
| Conda environment / `bootstrap.sh` | **Fabric Environment** item with custom libraries | Recreate conda/pip dependencies in a Fabric Environment |
| `hive-site.xml` (metastore connection) | Not needed — Delta Lake IS the metastore in Fabric | Remove metastore config; use Lakehouse schemas for namespace organization |

---

## Must / Prefer / Avoid

### MUST DO
- **Replace all `wasb://` / `wasbs://` paths** with OneLake `abfss://` paths or OneLake Shortcuts — `wasb://` requires storage account keys which are not the Fabric-preferred auth model
- **Replace `HiveContext`, `SQLContext`, and standalone `SparkContext()`** — use the pre-instantiated `spark` session in Fabric notebooks
- **Migrate Hive DDL** (`STORED AS ORC`, `LOCATION`, `TBLPROPERTIES`) to Delta Lake DDL — see [hive-to-delta.md](resources/hive-to-delta.md)
- **Introduce `notebookutils`** for file system operations, secret retrieval, and child notebook orchestration where HDInsight used custom scripts or direct API calls
- **Replace Oozie XML workflows** with Fabric Data Pipelines — see [§ Oozie → Fabric Pipelines](#oozie--fabric-pipelines)
- **Align library management** to Fabric Environments — remove `bootstrap.sh`, conda envs, and runtime `%pip install` patterns for production workloads
- **Treat `hdfs://` as source-cluster-only** — export or ingest into ADLS Gen2 or OneLake; do not claim that a gateway adds Kerberos support to Fabric's Anonymous-only HDFS connector

### PREFER
- **OneLake Shortcuts** over copying data — mount existing ADLS Gen2 containers as shortcuts to avoid re-ingestion during migration
- **Delta Lake** for all tables migrated from Hive ORC/Parquet — ACID guarantees, time travel, and schema enforcement improve data quality
- **Fabric Starter Pool** for initial migration validation — no pool configuration overhead, fast session startup
- **Lakehouse schemas** (database namespaces) for organizing migrated Hive databases — one schema per Hive database within a single Lakehouse
- **Medallion architecture** for restructuring migrated data layers during migration — align Bronze/Silver/Gold with raw Hive → validated Delta → serving Gold patterns

### AVOID
- **Do not use `SparkContext()` or `HiveContext()` constructors** in Fabric notebooks — they conflict with the pre-instantiated `spark` session and will raise errors
- **Do not use `hive-site.xml` or external Hive metastore configuration** — Fabric's Delta Lake-backed Lakehouse IS the metastore
- **Do not assume YARN queue mappings translate to Fabric pools** — re-design resource allocation based on Fabric Spark pool SLAs
- **Do not attempt to run Oozie shell actions or Java MapReduce jobs** directly in Fabric — these must be refactored (see [§ Oozie → Fabric Pipelines](#oozie--fabric-pipelines))
- **Do not use `%sh` magic for file system operations** in production notebooks — use `notebookutils.fs.*` for portability and OneLake token-based auth

---

## Examples

See [code-patterns.md](resources/code-patterns.md) for full before/after examples. Key quick references:

**Legacy context → Fabric pre-instantiated session**

```python
# HDInsight (remove entirely)
from pyspark.sql import HiveContext
hc = HiveContext(sc)

# Fabric — use pre-instantiated spark directly
df = spark.sql("SELECT * FROM sales.fact_orders")
```

**WASB path → OneLake path (after shortcut creation)**

```python
# HDInsight
df = spark.read.parquet("wasb://raw@myaccount.blob.core.windows.net/orders/")

# Fabric
df = spark.read.parquet("Files/raw/orders/")
```

**Hive DDL → Delta DDL**

```sql
-- HDInsight
CREATE TABLE sales_db.fact_orders (...) STORED AS ORC LOCATION 'wasb://...';

-- Fabric
CREATE SCHEMA IF NOT EXISTS sales_db;
CREATE TABLE sales_db.fact_orders (...) USING DELTA;
```
