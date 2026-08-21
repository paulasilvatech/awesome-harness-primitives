# HDInsight Path Migration — WASB / ABFS → OneLake

Reference for converting storage path formats when migrating HDInsight workloads to Microsoft Fabric.

---

## Path Format Reference

| Format | Example | Status in Fabric |
|---|---|---|
| `wasb://` (Azure Blob, HTTP) | `wasb://container@account.blob.core.windows.net/path` | ❌ **Not supported** — use shortcut or OneLake path |
| `wasbs://` (Azure Blob, HTTPS) | `wasbs://container@account.blob.core.windows.net/path` | ❌ **Not supported** — use shortcut or OneLake path |
| `abfs://` (ADLS Gen2, non-SSL) | `abfs://container@account.dfs.core.windows.net/path` | ⚠️ Technically works but not recommended — use OneLake |
| `abfss://` (ADLS Gen2, SSL) | `abfss://container@account.dfs.core.windows.net/path` | ✅ Works for ADLS shortcuts; use `onelake.dfs.fabric.microsoft.com` for OneLake |
| **OneLake `abfss://`** | `abfss://workspace@onelake.dfs.fabric.microsoft.com/lh.Lakehouse/...` | ✅ **Preferred** — native Fabric path |
| **Lakehouse relative** | `Files/path` or `Tables/tablename` | ✅ **Preferred for notebooks** — resolved against attached Lakehouse |
| `hdfs:///` (cluster or on-premises HDFS) | `hdfs:///user/data/input/` | ❌ **Not directly accessible** — copy or ingest into OneLake first |

---

## Conversion Patterns

### WASB → OneLake (after creating a shortcut)

```python
# BEFORE — HDInsight: WASB path
sc.textFile("wasb://raw-data@mystorageaccount.blob.core.windows.net/logs/2024/")

# Migration Step 1: Create an OneLake Shortcut to the Blob container
# (Do this once in Fabric portal or via REST API — see connectivity-migration.md in synapse-migration)

# AFTER — Fabric: reference via shortcut in OneLake path
df = spark.read.text(
    "abfss://MyWorkspace@onelake.dfs.fabric.microsoft.com/BronzeLakehouse.Lakehouse/Files/raw-data/logs/2024/"
)

# Or via relative path (when shortcut is named "raw-data" under Files/)
df = spark.read.text("Files/raw-data/logs/2024/")
```

### ABFS → OneLake

```python
# BEFORE — HDInsight: ABFS path to ADLS Gen2
df = spark.read.parquet("abfss://silver@mystorageaccount.dfs.core.windows.net/customers/")

# Migration Option A: Create OneLake shortcut pointing to ADLS Gen2 container
# Then access via OneLake path:
df = spark.read.parquet(
    "abfss://MyWorkspace@onelake.dfs.fabric.microsoft.com/SilverLakehouse.Lakehouse/Files/customers/"
)

# Migration Option B: Copy/migrate data into Lakehouse Tables (Delta)
df = spark.read.format("delta").load("Tables/customers")
```

### HDFS -> OneLake

Fabric notebooks cannot access an HDInsight or on-premises `hdfs:///` namespace
directly. OneLake also does not provide a direct HDFS shortcut target. Copy,
move, export, or ingest the data into OneLake, or into a storage system that
OneLake shortcuts support, and then use a `Files/` or OneLake `abfss://` path.
For on-premises HDFS, one supported ingestion option is a Fabric Data Factory
Copy activity using the HDFS connector through an on-premises data gateway.

The [OneLake shortcut overview](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts)
lists the supported shortcut sources. The
[on-premises shortcut guidance](https://learn.microsoft.com/en-us/fabric/onelake/create-on-premises-shortcut)
limits gateway-backed shortcuts to the documented S3, S3-compatible, and Google
Cloud Storage targets; it does not add HDFS as a shortcut type.
The [HDFS for Pipeline connector](https://learn.microsoft.com/en-us/fabric/data-factory/connector-hdfs-for-pipeline-overview)
documents HDFS as a Copy activity and Copy job source with on-premises gateway
support. Its current Fabric capability table lists **Anonymous** authentication
only. Do not claim that the gateway adds Windows or Kerberos authentication; if
the source requires Kerberos, export or bridge the data through a supported
storage target before reading it from OneLake.

```python
# AFTER the source data has been copied or ingested into the Lakehouse:
df = spark.read.parquet("Files/landing/hdfs-input/")
```

---

## OneLake Path Structure

```
abfss://{workspaceName}@onelake.dfs.fabric.microsoft.com/{itemName}.{itemType}/{section}/{subpath}

Where:
  workspaceName = Fabric workspace name (URL-encoded if spaces)
  itemName      = Lakehouse name
  itemType      = "Lakehouse"
  section       = "Files" (unmanaged files) or "Tables" (Delta tables)
  subpath       = relative folder/file path
```

### Examples

```python
# List files in a Lakehouse Files section
notebookutils.fs.ls(
    "abfss://DataEngineering@onelake.dfs.fabric.microsoft.com/BronzeLakehouse.Lakehouse/Files/"
)

# Read a Delta table from Tables section
df = spark.read.format("delta").load(
    "abfss://DataEngineering@onelake.dfs.fabric.microsoft.com/SilverLakehouse.Lakehouse/Tables/customers"
)

# Write a Delta table
df.write.format("delta").mode("overwrite").save(
    "abfss://DataEngineering@onelake.dfs.fabric.microsoft.com/GoldLakehouse.Lakehouse/Tables/customer_summary"
)
```

---

## Storage Authentication Differences

| HDInsight Pattern | Fabric Pattern |
|---|---|
| Storage Account Key in `core-site.xml` | **Not used** — Fabric uses Entra ID token auth |
| SAS token in Spark config | **Not used** — replace with OneLake shortcuts (which use workspace identity) |
| Service Principal in `spark-defaults.conf` | **Not needed** for OneLake — notebook identity has access automatically |
| Kerberos (on-premises HDFS) | Not used by Fabric notebooks — copy or ingest through a supported connector and gateway |

```python
# BEFORE — HDInsight: configure storage account key
spark.conf.set(
    "fs.azure.account.key.mystorageaccount.blob.core.windows.net",
    "<storage_account_key>"
)
df = spark.read.csv("wasbs://data@mystorageaccount.blob.core.windows.net/input/")

# AFTER — Fabric: no key config needed; access is via workspace identity
# Just create a shortcut and use OneLake path directly
df = spark.read.csv("Files/data/input/")
```

---

## Batch Path Conversion Helper

When migrating a large codebase with many WASB/ABFS paths, use this pattern to identify all occurrences:

```bash
# Find all WASB/ABFS path strings in Python notebooks
grep -r "wasb\|wasbs\|abfs://" ./notebooks/ --include="*.py" --include="*.ipynb" -l

# Common regex patterns to search for
# wasb(s)://container@account.blob.core.windows.net
# abfs(s)://container@account.dfs.core.windows.net
```

Replacement mapping template (adjust to your workspace/lakehouse names):

| Old Pattern | New Pattern |
|---|---|
| `wasb://raw@myaccount.blob.core.windows.net/` | `Files/raw/` (with shortcut named `raw`) |
| `abfss://silver@myaccount.dfs.core.windows.net/` | `abfss://MyWorkspace@onelake.dfs.fabric.microsoft.com/SilverLH.Lakehouse/Files/` |
| `abfss://gold@myaccount.dfs.core.windows.net/tables/` | `Tables/` (with data migrated to Lakehouse Delta tables) |
