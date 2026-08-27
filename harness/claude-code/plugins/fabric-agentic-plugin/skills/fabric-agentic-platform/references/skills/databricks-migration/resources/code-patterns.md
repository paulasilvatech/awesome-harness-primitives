# Databricks → Fabric Code Patterns

Before/after examples for common Databricks → Microsoft Fabric migration scenarios.

---

## Notebook Header: dbutils → notebookutils

```python
# BEFORE — Databricks: dbutils is built-in, no import needed
# But many notebooks have this pattern:
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

# AFTER — Fabric: everything is pre-instantiated
# Remove: SparkSession.builder... (spark is already available)
# Remove: any dbutils.* references (replace per mapping below)
# notebookutils is available globally — no import needed
```

---

## File System Operations

```python
# BEFORE — Databricks: list files on DBFS mount
files = dbutils.fs.ls("/mnt/bronze/customers/")
for f in files:
    print(f.name, f.size)

# AFTER — Fabric
files = notebookutils.fs.ls("Files/customers/")  # relative to attached Lakehouse
for f in files:
    print(f.name, f.size)
```

```python
# BEFORE — Databricks: copy file
dbutils.fs.cp("/mnt/raw/orders.csv", "/mnt/archive/orders.csv")

# AFTER — Fabric
notebookutils.fs.cp("Files/raw/orders.csv", "Files/archive/orders.csv")
```

```python
# BEFORE — Databricks: write and read temp file
dbutils.fs.put("/tmp/checkpoint.txt", "batch_id=42", overwrite=True)
content = dbutils.fs.head("/tmp/checkpoint.txt")

# AFTER — Fabric
notebookutils.fs.put("Files/checkpoints/checkpoint.txt", "batch_id=42", overwrite=True)
content = notebookutils.fs.head("Files/checkpoints/checkpoint.txt")
```

---

## Secret Retrieval

```python
# BEFORE — Databricks
jdbc_password = dbutils.secrets.get(scope="prod-secrets", key="jdbc-password")
api_token     = dbutils.secrets.get(scope="prod-secrets", key="external-api-token")

spark.conf.set("spark.hadoop.fs.azure.account.key.myaccount.dfs.core.windows.net",
               dbutils.secrets.get("prod-secrets", "storage-key"))

# AFTER — Fabric
KV_URL = "https://prod-keyvault.vault.azure.net/"
jdbc_password = notebookutils.credentials.getSecret(KV_URL, "jdbc-password")
api_token     = notebookutils.credentials.getSecret(KV_URL, "external-api-token")

# For storage access: use OneLake shortcuts — no account key needed
```

---

## DBFS Mount → OneLake Path

```python
# BEFORE — Databricks: read from mounted ADLS
df = spark.read.format("delta").load("/mnt/silver/transactions/")
df = spark.read.parquet("/mnt/raw/events/2024/01/")

# AFTER — Fabric: read from Lakehouse (after creating OneLake shortcut)
df = spark.read.format("delta").load("Tables/transactions")         # Delta table
df = spark.read.parquet("Files/events/2024/01/")                   # raw files
```

---

## Notebook Orchestration

```python
# BEFORE — Databricks
result = dbutils.notebook.run(
    "/Shared/ETL/silver_transform",
    timeout=600,
    arguments={"date": "2024-01-01", "env": "prod"}
)
status = result  # notebook's exit value

dbutils.notebook.exit("transform_complete")

# AFTER — Fabric (identical structure; name replaces path)
result = notebookutils.notebook.run(
    "silver_transform",
    timeout=600,
    arguments={"date": "2024-01-01", "env": "prod"}
)
status = result

notebookutils.notebook.exit("transform_complete")
```

---

## Widget Parameters → Notebook Parameters

```python
# BEFORE — Databricks
dbutils.widgets.text("batch_date", "2024-01-01")
dbutils.widgets.dropdown("environment", "dev", ["dev", "test", "prod"])
batch_date = dbutils.widgets.get("batch_date")
environment = dbutils.widgets.get("environment")

# AFTER — Fabric: use a "parameters" tagged cell
# Tag the cell below as "parameters" in the notebook UI
# Pipeline Base parameters or parent-notebook arguments override these defaults
# by injecting the runtime values into a generated cell.
batch_date = "2024-01-01"   # overridden by pipeline or parent notebook at runtime
environment = "dev"
```

`notebookutils.runtime.context` contains execution metadata such as workspace,
notebook, activity, and user identifiers. It does **not** store notebook
parameter values; use the variables overridden from the marked parameters cell.

---

## Unity Catalog Reads → Lakehouse Schema Reads

```python
# BEFORE — Databricks: 3-level namespace
customers = spark.read.table("prod.silver.customers")
orders    = spark.read.table("prod.silver.orders")
result    = customers.join(orders, "customer_id")
result.write.format("delta").mode("overwrite").saveAsTable("prod.gold.customer_orders")

# AFTER — Fabric: 2-level (catalog removed; Lakehouse context provides catalog)
customers = spark.read.table("silver.customers")
orders    = spark.read.table("silver.orders")
result    = customers.join(orders, "customer_id")
result.write.format("delta").mode("overwrite").saveAsTable("gold.customer_orders")
```

---

## Delta MERGE (identical — no changes needed)

```python
# Databricks Delta MERGE — works identically in Fabric
from delta.tables import DeltaTable

target = DeltaTable.forName(spark, "silver.customers")
target.alias("t").merge(
    updates.alias("s"),
    "t.customer_id = s.customer_id"
).whenMatchedUpdate(set={
    "email": "s.email",
    "updated_at": "s.updated_at"
}).whenNotMatchedInsertAll() \
 .execute()
```

---

## MLflow Tracking

```python
# BEFORE — Databricks: set tracking URI to Databricks
import mlflow
mlflow.set_tracking_uri("databricks")
mlflow.set_experiment("/Users/user@company.com/MyExperiment")

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.sklearn.log_model(model, "model")

# AFTER — Fabric: remove set_tracking_uri; use experiment name only
import mlflow
mlflow.set_experiment("MyExperiment")  # Fabric creates the Experiment item automatically

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.sklearn.log_model(model, "model")
```

---

## Cluster-Level Library → Fabric Environment

```python
# BEFORE — Databricks: runtime library install in notebook
dbutils.library.installPyPI("xgboost", version="1.7.0")
dbutils.library.restartPython()

import xgboost as xgb

# AFTER — Fabric:
# 1. Create or edit a Fabric Environment item
# 2. Add xgboost==1.7.0 to pip packages in the Environment
# 3. Attach the Environment to the notebook
# 4. Then in notebook — just import directly:
import xgboost as xgb
# No install code needed at runtime
```

---

## Spark Configuration (Photon → NEE)

```python
# BEFORE — Databricks: Photon is enabled at cluster level (no code change)
# Cluster config: "runtime_engine": "PHOTON"

# AFTER — Fabric: enable Native Execution Engine (similar vectorized execution)
# Enable in Fabric workspace Spark settings:
#   Spark compute → "Native Execution Engine" → On
# Or in notebook %%configure:
%%configure
{
    "conf": {
        "spark.microsoft.delta.nativeExecutionEngine.enabled": "true"
    }
}
```
