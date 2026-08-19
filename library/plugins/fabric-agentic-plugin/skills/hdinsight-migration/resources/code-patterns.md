# HDInsight → Fabric Code Patterns

Before/after examples for common HDInsight Spark → Microsoft Fabric migration scenarios.

---

## Session Setup: Legacy Context → SparkSession

```python
# BEFORE — HDInsight: legacy Spark 1.x/2.x context setup
from pyspark import SparkContext, SparkConf
from pyspark.sql import HiveContext, SQLContext

conf = SparkConf().setAppName("MyJob")
sc = SparkContext(conf=conf)
hc = HiveContext(sc)
sqlc = SQLContext(sc)

# AFTER — Fabric: nothing to initialize
# spark (SparkSession), sc (SparkContext) are pre-instantiated
# Just use them directly:
df = spark.read.format("delta").load("Tables/my_table")
```

---

## Reading Data: WASB → OneLake

```python
# BEFORE — HDInsight: read CSV from WASB
df = spark.read.csv(
    "wasb://raw@mystorageaccount.blob.core.windows.net/customers/2024/",
    header=True,
    inferSchema=True
)

# AFTER — Fabric: read from Files section (after shortcut or data ingestion)
df = spark.read.csv(
    "Files/customers/2024/",
    header=True,
    inferSchema=True
)

# Or with explicit OneLake path
df = spark.read.csv(
    "abfss://MyWorkspace@onelake.dfs.fabric.microsoft.com/BronzeLakehouse.Lakehouse/Files/customers/2024/",
    header=True,
    inferSchema=True
)
```

---

## Hive Table Read → Delta Table Read

```python
# BEFORE — HDInsight: query Hive table via HiveContext
df = hc.sql("SELECT * FROM sales_db.fact_orders WHERE order_date >= '2024-01-01'")

# AFTER — Fabric: query Delta table via SparkSession
df = spark.sql("SELECT * FROM sales_db.fact_orders WHERE order_date >= '2024-01-01'")
# Note: sales_db is now a schema within the Fabric Lakehouse
```

---

## Writing Delta Tables

```python
# BEFORE — HDInsight: save as ORC to HDFS/WASB
df.write.format("orc") \
    .mode("overwrite") \
    .partitionBy("order_date") \
    .save("abfss://silver@mystorageaccount.dfs.core.windows.net/fact_orders/")

# AFTER — Fabric: save as Delta to Lakehouse
df.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("order_date") \
    .saveAsTable("sales_db.fact_orders")
```

---

## MERGE / Upsert

```python
# BEFORE — HDInsight (no native MERGE in older Hive; workaround with overwrite)
# Partition overwrite was common
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
df_updates.write.format("orc").mode("overwrite").partitionBy("order_date") \
    .save("abfss://silver@myaccount.dfs.core.windows.net/fact_orders/")

# AFTER — Fabric: use Delta MERGE for proper upserts
from delta.tables import DeltaTable

delta_table = DeltaTable.forName(spark, "sales_db.fact_orders")
delta_table.alias("target").merge(
    df_updates.alias("source"),
    "target.order_id = source.order_id"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()
```

---

## File System Operations (Introducing notebookutils)

```python
# BEFORE — HDInsight: use subprocess or HDFS client
import subprocess
files = subprocess.check_output(
    ["hdfs", "dfs", "-ls", "wasb://data@myaccount.blob.core.windows.net/incoming/"]
).decode()

# AFTER — Fabric: use notebookutils.fs
files = notebookutils.fs.ls("Files/incoming/")
for f in files:
    print(f.name, f.size, f.isDir)
```

```python
# BEFORE — HDInsight: copy file via HDFS API
from hdfs import InsecureClient
client = InsecureClient("http://namenode:50070")
client.copy("/data/input/file.csv", "/data/archive/file.csv")

# AFTER — Fabric
notebookutils.fs.cp("Files/input/file.csv", "Files/archive/file.csv")
```

---

## Secret / Credential Access

```python
# BEFORE — HDInsight: read storage key from config
storage_key = sc._jsc.hadoopConfiguration().get(
    "fs.azure.account.key.mystorageaccount.blob.core.windows.net"
)

# AFTER — Fabric: read secret from Azure Key Vault
db_password = notebookutils.credentials.getSecret(
    "https://mykeyvault.vault.azure.net/",
    "database-password"
)
```

---

## Spark Configuration

```python
# BEFORE — HDInsight: set config via SparkConf or spark-defaults.conf
spark.conf.set("spark.executor.memory", "8g")
spark.conf.set("spark.sql.shuffle.partitions", "400")

# AFTER — Fabric: identical (no change needed for session-level config)
spark.conf.set("spark.sql.shuffle.partitions", "400")
# For persistent config, use Fabric Environment Spark properties
```

---

## Oozie Shell Action → Fabric Pipeline Web Activity

```xml
<!-- BEFORE — Oozie: shell action to trigger downstream process -->
<action name="trigger-api">
    <shell>
        <exec>curl</exec>
        <argument>-X POST https://api.example.com/trigger</argument>
    </shell>
    <ok to="end"/>
    <error to="fail"/>
</action>
```

```json
// AFTER — Fabric Pipeline: Web activity
{
  "name": "TriggerAPI",
  "type": "WebActivity",
  "typeProperties": {
    "url": "https://api.example.com/trigger",
    "method": "POST",
    "headers": { "Content-Type": "application/json" },
    "body": "{}"
  }
}
```

---

## Child Notebook Orchestration (New Capability)

```python
# HDInsight had no native notebook orchestration equivalent
# In Fabric, use notebookutils to run child notebooks in sequence or parallel:

# Sequential
result1 = notebookutils.notebook.run("bronze_ingest", timeout=600, arguments={"date": "2024-01-01"})
result2 = notebookutils.notebook.run("silver_transform", timeout=600, arguments={"date": "2024-01-01"})
result3 = notebookutils.notebook.run("gold_aggregate", timeout=600, arguments={"date": "2024-01-01"})

# Exit current notebook with a value for orchestration use
notebookutils.notebook.exit("success")
```
