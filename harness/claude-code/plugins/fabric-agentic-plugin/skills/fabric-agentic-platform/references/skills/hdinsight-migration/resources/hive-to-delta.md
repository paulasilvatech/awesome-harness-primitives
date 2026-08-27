# Hive DDL → Delta Lake / Fabric Lakehouse Schema Migration

Reference for converting Hive DDL and metastore constructs to Microsoft Fabric Lakehouse patterns.

---

## Conceptual Mapping

| Hive Concept | Fabric Equivalent | Notes |
|---|---|---|
| **Hive Metastore** | **Fabric Lakehouse** (per lakehouse schema) | Each Lakehouse is a Delta-backed metastore namespace |
| **Hive Database** | **Lakehouse Schema** (namespace within a Lakehouse) | Create schemas with `CREATE SCHEMA` in Spark SQL |
| **Hive Table** (`STORED AS ORC/Parquet`) | **Delta Table** in Lakehouse `Tables/` | Rewrite DDL to use Delta format |
| **External Hive Table** (LOCATION) | **OneLake Shortcut** + schema reference | Create shortcut to existing storage, then read directly |
| **Hive View** | **Fabric Lakehouse View** (via Spark SQL `CREATE VIEW`) | Views are supported in Lakehouse schemas |
| **Hive Partitioning** (`PARTITIONED BY`) | **Delta partitioning** (`partitionBy`) | Same concept; Delta syntax |
| `MSCK REPAIR TABLE` | `MSCK REPAIR TABLE` — supported | Or use Delta `GENERATE SYMLINK_FORMAT_MANIFEST` |

---

## DDL Conversion Examples

### Create Table

```sql
-- BEFORE — Hive DDL
CREATE TABLE IF NOT EXISTS sales_db.fact_orders (
    order_id    BIGINT,
    customer_id INT,
    order_date  DATE,
    amount      DECIMAL(18,2)
)
STORED AS ORC
LOCATION 'wasb://silver@myaccount.blob.core.windows.net/fact_orders/'
TBLPROPERTIES ('orc.compress'='SNAPPY');

-- AFTER — Fabric Spark SQL (Delta)
-- Step 1: Create schema (maps to Hive database)
CREATE SCHEMA IF NOT EXISTS sales_db;

-- Step 2: Create Delta table in schema
CREATE TABLE IF NOT EXISTS sales_db.fact_orders (
    order_id    BIGINT,
    customer_id INT,
    order_date  DATE,
    amount      DECIMAL(18,2)
) USING DELTA;
```

For an external Hive table backed by ORC or Parquet files, use the OneLake
shortcut as the migration source, read the source format, and write a new Delta
table. Do not declare `USING DELTA LOCATION 'Files/...'` over ORC or Parquet
files; a Delta `LOCATION` is valid only when the target folder already contains
Delta data and its transaction log.

```python
source_df = spark.read.format("orc").load("Files/hive-export/fact_orders/")
source_df.write.format("delta").mode("overwrite").saveAsTable("sales_db.fact_orders")
```

### Partitioned Table

```sql
-- BEFORE — Hive: partitioned Parquet table
CREATE TABLE logs_db.app_logs (
    log_id   BIGINT,
    message  STRING,
    severity STRING
)
PARTITIONED BY (log_date DATE, app_name STRING)
STORED AS PARQUET;

-- AFTER — Fabric: Delta with partitioning
CREATE SCHEMA IF NOT EXISTS logs_db;

CREATE TABLE logs_db.app_logs (
    log_id   BIGINT,
    message  STRING,
    severity STRING,
    log_date DATE,
    app_name STRING
) USING DELTA
PARTITIONED BY (log_date, app_name);
```

### PySpark DataFrame Write (replaces HiveContext insertInto)

```python
# BEFORE — HDInsight: write to Hive table
df.write.mode("overwrite").insertInto("sales_db.fact_orders")

# OR: saveAsTable in Hive metastore
df.write.mode("overwrite").format("orc").saveAsTable("sales_db.fact_orders")

# AFTER — Fabric: write as Delta to Lakehouse
df.write.format("delta").mode("overwrite").saveAsTable("sales_db.fact_orders")

# Or with explicit partitioning
df.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("log_date", "app_name") \
    .saveAsTable("logs_db.app_logs")
```

---

## Hive UDFs → Fabric Spark UDFs

```python
# BEFORE — Hive UDF registration (via HiveContext)
hc.sql("CREATE TEMPORARY FUNCTION my_udf AS 'com.example.MyUDF'")

# AFTER — Fabric: register Python UDF with SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(returnType=StringType())
def my_udf(value):
    return value.strip().upper()

spark.udf.register("my_udf", my_udf)
df.withColumn("result", my_udf(df["input_col"]))
```

> Java/Scala UDFs must be rewritten in Python or Scala and compiled as a JAR, then included in the Fabric Environment.

---

## HiveQL → Spark SQL Compatibility

Most HiveQL is compatible with Spark SQL. Key differences:

| HiveQL Feature | Spark SQL Behavior | Action |
|---|---|---|
| `STORED AS ORC` / `STORED AS PARQUET` | Ignored or error in Delta DDL | Replace with `USING DELTA` |
| `LOCATION 'hdfs://...'` | Replace HDFS path with OneLake path or remove for managed tables | Update or remove |
| `TBLPROPERTIES (...)` | Supported for Delta properties | Keep Delta-relevant properties; remove ORC/Hive-specific ones |
| `MSCK REPAIR TABLE` | Supported | Keep as-is |
| `SHOW PARTITIONS` | Supported | Keep as-is |
| `LATERAL VIEW EXPLODE` | Supported | Keep as-is |
| `DISTRIBUTE BY` / `SORT BY` | Supported (hint) | Keep as-is |
| `TRANSFORM ... USING script.py` | **Not supported** — Hive streaming transform | Rewrite as PySpark UDF or mapPartitions |
| `LOAD DATA INPATH` | Not supported for Delta | Use `COPY INTO` (Warehouse) or Spark read+write pattern |

---

## Migrating a Hive Database to a Lakehouse Schema

Step-by-step migration of a Hive database to a Fabric Lakehouse schema:

```python
# Step 1: Create a schema in the Lakehouse (maps to Hive database)
spark.sql("CREATE SCHEMA IF NOT EXISTS sales_db")

# Step 2: For each Hive table, read its source format from the ADLS shortcut and write as Delta
hive_tables = {
    "fact_orders": "orc",
    "dim_customer": "parquet",
    "dim_product": "parquet",
}

for table, source_format in hive_tables.items():
    # Read from ADLS (via OneLake shortcut)
    df = spark.read.format(source_format).load(f"Files/hive-export/{table}/")
    
    # Write as Delta to Lakehouse schema
    df.write.format("delta").mode("overwrite").saveAsTable(f"sales_db.{table}")
    
    print(f"Migrated {table}")

# Step 3: Verify
spark.sql("SHOW TABLES IN sales_db").show()
```

---

## Schema Organization: Hive Databases → Lakehouse Schemas

Fabric Lakehouses support multiple schemas (namespaces). Use this pattern to organize migrated Hive databases:

| Hive Structure | Fabric Structure |
|---|---|
| `raw_db` Hive database | `BronzeLakehouse` with `raw` schema |
| `processed_db` Hive database | `SilverLakehouse` with `processed` schema |
| `analytics_db` Hive database | `GoldLakehouse` with `analytics` schema |
| Multiple subject area databases | Multiple schemas within a single Lakehouse, or separate Lakehouses per domain |

```sql
-- Create subject-area schemas within a Lakehouse
CREATE SCHEMA IF NOT EXISTS finance;
CREATE SCHEMA IF NOT EXISTS hr;
CREATE SCHEMA IF NOT EXISTS operations;

-- Tables are then organized as:
-- finance.fact_transactions
-- hr.dim_employee
-- operations.fact_events
```
