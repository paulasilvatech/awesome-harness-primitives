# Unity Catalog → Fabric Lakehouse Schema Migration

Reference for migrating Databricks Unity Catalog namespace structures to Microsoft Fabric Lakehouse schemas.

---

## Namespace Model Comparison

| Concept | Databricks Unity Catalog | Microsoft Fabric | Notes |
|---|---|---|---|
| Top-level container | **Catalog** (e.g., `prod`, `dev`) | **Lakehouse** (per-workspace item) | One Lakehouse ≈ one catalog in practice |
| Namespace level 1 | **Schema** (database within catalog) | **Schema** (within a Lakehouse) | Direct equivalent — create with `CREATE SCHEMA` |
| Namespace level 2 | **Table** | **Delta Table** in Lakehouse `Tables/` | Direct equivalent |
| Full reference | `catalog.schema.table` | `schema.table` (within a Lakehouse context) | Fabric is 2-level; switch active Lakehouse for cross-lakehouse |
| Cross-catalog access | `catalog2.schema.table` | Cross-lakehouse shortcut or explicit Lakehouse switch | Use OneLake shortcuts for cross-lakehouse table access |

---

## Mapping Strategy

### Option A: One Lakehouse per Unity Catalog

Best for: organizations with distinct catalogs for `dev`, `test`, `prod`, or `bronze`/`silver`/`gold`.

| Unity Catalog | Fabric |
|---|---|
| `prod` catalog | `ProdLakehouse` |
| `dev` catalog | `DevLakehouse` |
| `prod.finance.fact_sales` | `ProdLakehouse` → schema `finance` → table `fact_sales` |
| `prod.hr.dim_employee` | `ProdLakehouse` → schema `hr` → table `dim_employee` |

### Option B: One Lakehouse per Schema (for large orgs)

Best for: organizations where schemas represent independent domains with separate ownership.

| Unity Catalog Schema | Fabric |
|---|---|
| `prod.finance` | `FinanceLakehouse` (default schema) |
| `prod.hr` | `HRLakehouse` (default schema) |
| `prod.operations` | `OperationsLakehouse` (default schema) |

### Option C: Medallion-aligned Lakehouses

Best for: migrating Bronze/Silver/Gold Unity Catalog pattern.

| Unity Catalog | Fabric |
|---|---|
| `prod.bronze` schema | `BronzeLakehouse` |
| `prod.silver` schema | `SilverLakehouse` |
| `prod.gold` schema | `GoldLakehouse` |

---

## DDL Migration

### Create Schema (identical syntax)

```sql
-- Databricks
CREATE SCHEMA IF NOT EXISTS prod.finance
    COMMENT 'Finance domain tables'
    MANAGED LOCATION 'abfss://...';

-- Fabric Spark SQL (attach to target Lakehouse first)
CREATE SCHEMA IF NOT EXISTS finance
    COMMENT 'Finance domain tables';
-- Note: MANAGED LOCATION is controlled by the Lakehouse; remove the clause
```

### Create Table

```sql
-- BEFORE — Databricks Unity Catalog
CREATE TABLE IF NOT EXISTS prod.finance.fact_transactions (
    txn_id      BIGINT NOT NULL,
    account_id  INT,
    txn_date    DATE,
    amount      DECIMAL(18,4),
    currency    STRING
)
USING DELTA
COMMENT 'Daily financial transactions'
PARTITIONED BY (txn_date)
TBLPROPERTIES ('delta.autoOptimize.optimizeWrite' = 'true');

-- AFTER — Fabric (catalog removed; same Lakehouse assumed)
CREATE TABLE IF NOT EXISTS finance.fact_transactions (
    txn_id      BIGINT NOT NULL,
    account_id  INT,
    txn_date    DATE,
    amount      DECIMAL(18,4),
    currency    STRING
)
USING DELTA
COMMENT 'Daily financial transactions'
PARTITIONED BY (txn_date)
TBLPROPERTIES ('delta.autoOptimize.optimizeWrite' = 'true');
-- Note: TBLPROPERTIES are supported; Delta properties transfer as-is
```

### Cross-Catalog Table Reference

```python
# BEFORE — Databricks: read from another catalog
df = spark.sql("SELECT * FROM prod.silver.customers c JOIN staging.bronze.raw_events e ON c.id = e.customer_id")

# AFTER — Fabric Option A: use Spark SQL with schema-qualified names (within attached Lakehouse)
df = spark.sql("SELECT * FROM silver.customers c JOIN bronze.raw_events e ON c.id = e.customer_id")

# AFTER — Fabric Option B: create a OneLake Shortcut to the other Lakehouse's table
# Then reference it as a local table in the current Lakehouse schema
```

---

## Access Control Migration

Unity Catalog provides fine-grained RBAC, row filters, and column masks. Fabric provides workspace roles + Lakehouse permissions.

| Unity Catalog Permission | Fabric Equivalent |
|---|---|
| `GRANT SELECT ON catalog.schema.table TO user@domain.com` | Workspace **Viewer** role + Lakehouse item permissions |
| `GRANT MODIFY ON catalog.schema TO group` | Workspace **Contributor** role |
| Row-level security (row filter) | **Lakehouse row-level security** (via SQL `CREATE ROW FILTER`, preview) or Semantic Model RLS |
| Column masking | **Dynamic Data Masking** in Fabric Warehouse, or column-level security in Semantic Model |
| `REVOKE` / `DENY` | Remove workspace role assignment |
| External location access control | OneLake Shortcut permissions (workspace role-based) |

> **Governance gap**: Unity Catalog offers more granular column-level masking than Fabric's current offering. Assess governance requirements before migration and plan for interim mitigations.

---

## PySpark Code Changes

```python
# BEFORE — Databricks: 3-level namespace in all reads/writes
df = spark.read.table("prod.silver.customers")
df.write.format("delta").mode("overwrite").saveAsTable("prod.gold.customer_summary")

# AFTER — Fabric: 2-level (catalog prefix removed)
df = spark.read.table("silver.customers")
df.write.format("delta").mode("overwrite").saveAsTable("gold.customer_summary")
```

```python
# BEFORE — Databricks: set current catalog
spark.catalog.setCurrentCatalog("prod")
spark.catalog.setCurrentDatabase("finance")

# AFTER — Fabric: set current schema (catalog concept = active Lakehouse)
spark.sql("USE finance")
# To switch Lakehouse context, change the default Lakehouse attached to the notebook
```

---

## Delta Table Properties

Most Delta table properties migrate without changes. Key properties to verify:

| Property | Databricks Behavior | Fabric Behavior | Action |
|---|---|---|---|
| `delta.autoOptimize.optimizeWrite` | Auto bin-packing on write | Supported | Keep |
| `delta.autoOptimize.autoCompact` | Background compaction | Supported | Keep |
| `delta.columnMapping.mode` | Column name mapping | Supported | Keep |
| `delta.enableChangeDataFeed` | CDF / CDC | Supported | Keep |
| `delta.deletedFileRetentionDuration` | VACUUM retention | Supported | Keep |
| `delta.logRetentionDuration` | History retention | Supported | Keep |
| Unity Catalog `MANAGED LOCATION` | Catalog storage root | Remove — Fabric Lakehouse controls location | Remove clause |
| `SHALLOW CLONE` / `DEEP CLONE` | Delta clone | **SHALLOW CLONE not supported** in Fabric; use DEEP CLONE or read+write | Rewrite |
