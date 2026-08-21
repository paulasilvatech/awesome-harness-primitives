# Synapse → Fabric Code Patterns

Before/after examples for common Synapse Analytics → Microsoft Fabric migration scenarios.

---

## Spark Notebook: Import and Session Setup

```python
# BEFORE — Synapse notebook header
from notebookutils import mssparkutils
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

# AFTER — Fabric notebook header (nothing to import or initialize)
# spark, sc, and notebookutils are pre-instantiated in every Fabric notebook
# No imports required
```

---

## Reading Data: ADLS Path → OneLake Path

```python
# BEFORE — Synapse: read from ADLS Gen2 via linked service auth
df = spark.read.format("delta") \
    .load("abfss://silver@mystorageaccount.dfs.core.windows.net/customers/")

# AFTER — Fabric: read from OneLake (after creating a shortcut or writing data to Lakehouse)
df = spark.read.format("delta") \
    .load("abfss://MyWorkspace@onelake.dfs.fabric.microsoft.com/SilverLakehouse.Lakehouse/Tables/customers")

# OR use relative path (when notebook has Lakehouse attached as default)
df = spark.read.format("delta").load("Tables/customers")
```

---

## Writing Data to Delta Lake

```python
# BEFORE — Synapse: write to ADLS Gen2
df.write.format("delta") \
    .mode("overwrite") \
    .save("abfss://gold@mystorageaccount.dfs.core.windows.net/summary/")

# AFTER — Fabric: write to Lakehouse Tables (managed Delta)
df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_summary")  # Writes to attached Lakehouse Tables/gold_summary

# Or explicit OneLake path
df.write.format("delta") \
    .mode("overwrite") \
    .save("Tables/gold_summary")
```

---

## Credentials: Linked Service → Key Vault Secret

```python
# BEFORE — Synapse: read connection string from Key Vault Linked Service
conn_str = mssparkutils.credentials.getConnectionStringOrCreds("AzureSQL_LinkedService")

jdbc_url = f"jdbc:sqlserver://myserver.database.windows.net;databaseName=mydb;password={conn_str}"

# AFTER — Fabric: read secret from Key Vault directly
password = notebookutils.credentials.getSecret(
    "https://mykeyvault.vault.azure.net/",
    "sql-password"
)

token = notebookutils.credentials.getToken("https://database.windows.net/")
jdbc_url = "jdbc:sqlserver://myserver.database.windows.net;databaseName=mydb;encrypt=true"

df = spark.read.format("jdbc") \
    .option("url", jdbc_url) \
    .option("accessToken", token) \
    .option("dbtable", "dbo.Customers") \
    .load()
```

---

## Environment Context

```python
# BEFORE — Synapse: read job/workspace context
workspace = mssparkutils.env.getWorkspaceName()
job_id = mssparkutils.env.getJobId()

# AFTER — Fabric: read from runtime context dict
ctx = notebookutils.runtime.context
workspace = ctx["currentWorkspaceName"]
job_id = ctx["activityId"]
workspace_id = ctx["currentWorkspaceId"]
```

---

## Child Notebook Execution

```python
# BEFORE — Synapse
result = mssparkutils.notebook.run(
    "silver_transform",
    timeout=600,
    arguments={"input_table": "bronze_orders", "batch_date": "2024-01-01"}
)

# AFTER — Fabric (identical API)
result = notebookutils.notebook.run(
    "silver_transform",
    timeout=600,
    arguments={"input_table": "bronze_orders", "batch_date": "2024-01-01"}
)
```

---

## Dedicated SQL Pool DDL → Fabric Warehouse

```sql
-- BEFORE — Synapse Dedicated SQL Pool
CREATE TABLE dbo.FactSales (
    SaleID INT NOT NULL,
    CustomerID INT,
    SaleDate DATE,
    Amount DECIMAL(18,2)
)
WITH (
    DISTRIBUTION = HASH(CustomerID),
    CLUSTERED COLUMNSTORE INDEX
);

-- AFTER — Fabric Warehouse (remove distribution hints; auto-managed)
CREATE TABLE dbo.FactSales (
    SaleID INT NOT NULL,
    CustomerID INT,
    SaleDate DATE,
    Amount DECIMAL(18,2)
);
-- Note: Fabric Warehouse uses Delta-backed storage with automatic distribution
```

---

## Bulk Load: PolyBase → COPY INTO

```sql
-- BEFORE — Synapse: PolyBase external table + INSERT
CREATE EXTERNAL DATA SOURCE adls_source
    WITH (TYPE = HADOOP, LOCATION = 'abfss://raw@mystorageaccount.dfs.core.windows.net/');

CREATE EXTERNAL TABLE dbo.ext_StagingOrders (...)
    WITH (DATA_SOURCE = adls_source, LOCATION = '/orders/2024/', FILE_FORMAT = CsvFormat);

INSERT INTO dbo.FactOrders SELECT * FROM dbo.ext_StagingOrders;

-- AFTER — Fabric Warehouse: COPY INTO from OneLake
COPY INTO dbo.FactOrders
FROM 'https://onelake.dfs.fabric.microsoft.com/<workspace>/<lakehouse>.Lakehouse/Files/orders/2024/'
WITH (
    FILE_TYPE = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n'
);
```

---

## File System Operations

```python
# BEFORE — Synapse
files = mssparkutils.fs.ls("abfss://raw@mystorageaccount.dfs.core.windows.net/incoming/")
for f in files:
    mssparkutils.fs.cp(f.path, f"abfss://archive@mystorageaccount.dfs.core.windows.net/{f.name}")

# AFTER — Fabric
files = notebookutils.fs.ls("Files/incoming/")
for f in files:
    notebookutils.fs.cp(f.path, f"Files/archive/{f.name}")
```

---

## Spark Catalog API — Unsupported Methods

Several `spark.catalog` methods are **not supported** in Fabric and will throw `AnalysisException`. Replace with Spark SQL equivalents.

> **Safe methods** (no change needed): `spark.catalog.createTable()`, `tableExists()`, `listTables()`, `listColumns()`, `dropTempView()`, `cacheTable()` all work normally in Fabric. Only database-level and function-level methods require refactoring.

### Database Methods

```python
# ❌ BEFORE — Synapse: list databases
dbs = spark.catalog.listDatabases()
for db in dbs:
    print(db.name)

# ✅ AFTER — Fabric: use Spark SQL
spark.sql("SHOW DATABASES").show()
# or collect as list
dbs = [row.namespace for row in spark.sql("SHOW DATABASES").collect()]
```

```python
# ❌ BEFORE — Synapse: get current database
current = spark.catalog.currentDatabase()

# ✅ AFTER — Fabric: use Spark SQL
current = spark.sql("SELECT CURRENT_DATABASE()").first()["current_database()"]
```

```python
# ❌ BEFORE — Synapse: describe a database
db_info = spark.catalog.getDatabase("sales_db")
print(db_info.locationUri)

# ✅ AFTER — Fabric: use DESCRIBE DATABASE
spark.sql("DESCRIBE DATABASE sales_db").show()
# For extended info:
spark.sql("DESCRIBE DATABASE EXTENDED sales_db").show()
```

### Function Methods

```python
# ❌ BEFORE — Synapse: list functions
funcs = spark.catalog.listFunctions()

# ✅ AFTER — Fabric: NOT SUPPORTED — remove or replace
# If listing built-in functions is needed:
spark.sql("SHOW FUNCTIONS").show()
```

```python
# ❌ BEFORE — Synapse: register function
spark.catalog.registerFunction("double_it", lambda x: x * 2)

# ✅ AFTER — Fabric: use spark.udf.register()
from pyspark.sql.types import IntegerType
spark.udf.register("double_it", lambda x: x * 2, IntegerType())
```

```python
# ❌ BEFORE — Synapse: check if function exists
if spark.catalog.functionExists("double_it"):
    df = spark.sql("SELECT double_it(value) FROM t")

# ✅ AFTER — Fabric: NOT SUPPORTED — remove check or use try/except
# Option A: just call it (will fail at runtime if not registered)
df = spark.sql("SELECT double_it(value) FROM t")

# Option B: search SHOW FUNCTIONS output
func_exists = len(spark.sql("SHOW USER FUNCTIONS").filter("function = 'double_it'").collect()) > 0
```

### Quick Reference Table

| Synapse `spark.catalog` Method | Fabric Replacement | Notes |
|---|---|---|
| `listDatabases()` | `spark.sql("SHOW DATABASES")` | Returns DataFrame |
| `currentDatabase()` | `spark.sql("SELECT CURRENT_DATABASE()")` | Returns single-row DataFrame |
| `getDatabase(name)` | `spark.sql(f"DESCRIBE DATABASE {name}")` | Returns metadata DataFrame |
| `setCurrentDatabase(name)` | `spark.sql(f"USE {name}")` | Works in both — no change needed |
| `listFunctions()` | `spark.sql("SHOW FUNCTIONS")` | |
| `registerFunction(name, fn)` | `spark.udf.register(name, fn, returnType)` | Must specify return type |
| `functionExists(name)` | `spark.sql("SHOW USER FUNCTIONS").filter(...)` | Manual check |

---

## Spark Configuration (`%%configure`)

```python
# BEFORE — Synapse: configure Spark session via magic
%%configure
{
    "conf": {
        "spark.executor.memory": "8g",
        "spark.executor.cores": 4,
        "spark.sql.shuffle.partitions": 200
    }
}

# AFTER — Fabric: identical magic cell syntax (no change required)
%%configure
{
    "conf": {
        "spark.executor.memory": "8g",
        "spark.executor.cores": 4,
        "spark.sql.shuffle.partitions": 200
    }
}
```
