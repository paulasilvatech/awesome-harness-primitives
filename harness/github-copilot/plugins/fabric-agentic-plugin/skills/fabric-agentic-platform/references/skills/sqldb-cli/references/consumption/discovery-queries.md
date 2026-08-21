# Extended Discovery Queries

Queries for deep schema exploration, security inspection, and table health checks in SQL database in Fabric.
All queries work on the SQL Database (OLTP) endpoint unless noted otherwise.

---

## Schema and Object Discovery

### Table and Column Metadata

```bash
# All columns across all tables with types
$SQLCMD -Q "
SELECT t.table_schema, t.table_name, c.column_name,
       c.data_type, c.character_maximum_length,
       c.numeric_precision, c.numeric_scale, c.is_nullable
FROM information_schema.tables t
JOIN information_schema.columns c
    ON t.table_schema = c.table_schema AND t.table_name = c.table_name
WHERE t.table_type = 'BASE TABLE'
ORDER BY t.table_schema, t.table_name, c.ordinal_position" -W

# Tables with row counts and column counts
$SQLCMD -Q "
SELECT s.name AS [schema], t.name AS [table],
       COUNT(DISTINCT c.column_id) AS col_count,
       SUM(p.rows) AS row_count
FROM sys.tables t
JOIN sys.schemas s ON t.schema_id = s.schema_id
JOIN sys.columns c ON t.object_id = c.object_id
JOIN sys.partitions p ON t.object_id = p.object_id AND p.index_id IN (0,1)
GROUP BY s.name, t.name
ORDER BY row_count DESC" -W

# Foreign key relationships (useful for JOIN hints)
$SQLCMD -Q "
SELECT fk.name AS fk_name,
    OBJECT_SCHEMA_NAME(fk.parent_object_id) + '.' + OBJECT_NAME(fk.parent_object_id) AS child_table,
    COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS child_column,
    OBJECT_SCHEMA_NAME(fk.referenced_object_id) + '.' + OBJECT_NAME(fk.referenced_object_id) AS parent_table,
    COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS parent_column
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
ORDER BY child_table, fk_name" -W
```

### View, Function, and Procedure Definitions

```bash
# View definitions (source SQL)
$SQLCMD -Q "
SELECT s.name AS [schema], v.name AS [view], m.definition
FROM sys.views v
JOIN sys.schemas s ON v.schema_id = s.schema_id
JOIN sys.sql_modules m ON v.object_id = m.object_id
ORDER BY s.name, v.name" -W

# Function definitions
$SQLCMD -Q "
SELECT s.name AS [schema], o.name AS [function], o.type_desc, m.definition
FROM sys.objects o
JOIN sys.schemas s ON o.schema_id = s.schema_id
JOIN sys.sql_modules m ON o.object_id = m.object_id
WHERE o.type IN ('FN','IF','TF')
ORDER BY s.name, o.name" -W

# Stored procedure definitions
$SQLCMD -Q "
SELECT s.name AS [schema], p.name AS [procedure], m.definition
FROM sys.procedures p
JOIN sys.schemas s ON p.schema_id = s.schema_id
JOIN sys.sql_modules m ON p.object_id = m.object_id
ORDER BY s.name, p.name" -W

# Procedure parameters
$SQLCMD -Q "
SELECT OBJECT_SCHEMA_NAME(p.object_id) AS [schema],
       OBJECT_NAME(p.object_id) AS [procedure],
       p.name AS param_name,
       TYPE_NAME(p.user_type_id) AS data_type,
       p.max_length, p.is_output
FROM sys.parameters p
JOIN sys.procedures pr ON p.object_id = pr.object_id
WHERE p.parameter_id > 0
ORDER BY [schema], [procedure], p.parameter_id" -W
```

### Cross-Database Discovery

Use the **SQL analytics endpoint** for cross-database queries.

```bash
# List all accessible databases in the workspace
$SQLCMD -Q "SELECT name, create_date FROM sys.databases ORDER BY name" -W

# Same sqlcmd wrapper, but configured with the SQL analytics endpoint connection variables and Entra authentication
SQLCMD_ANALYTICS="sqlcmd -S \"$SQL_ANALYTICS_SERVER\" -d \"$SQL_ANALYTICS_DATABASE\" -G"

# Tables in another database (3-part name — analytics endpoint only)
$SQLCMD_ANALYTICS -Q "SELECT table_schema, table_name FROM OtherDatabase.information_schema.tables ORDER BY table_schema, table_name" -W
```

---

## Table Health Check

Checks tables for common structural issues.

```bash
# Tables with no indexes (heaps)
$SQLCMD -Q "
SELECT SCHEMA_NAME(t.schema_id) AS SchemaName, t.name AS TableName,
    SUM(p.rows) AS RowCount
FROM sys.tables t
LEFT JOIN sys.indexes i ON t.object_id = i.object_id AND i.index_id > 0
JOIN sys.partitions p ON t.object_id = p.object_id AND p.index_id IN (0,1)
WHERE i.object_id IS NULL
GROUP BY t.schema_id, t.name
ORDER BY RowCount DESC" -W

# Tables with no primary keys
$SQLCMD -Q "
SELECT SCHEMA_NAME(t.schema_id) AS SchemaName, t.name AS TableName
FROM sys.tables t
WHERE NOT EXISTS (
    SELECT 1 FROM sys.indexes i
    WHERE i.object_id = t.object_id AND i.is_primary_key = 1
)
ORDER BY SchemaName, TableName" -W

# Disabled indexes
$SQLCMD -Q "
SELECT SCHEMA_NAME(t.schema_id) AS SchemaName, t.name AS TableName,
    i.name AS IndexName, i.type_desc
FROM sys.indexes i
JOIN sys.tables t ON i.object_id = t.object_id
WHERE i.is_disabled = 1
ORDER BY SchemaName, TableName" -W

# Tables with triggers
$SQLCMD -Q "
SELECT SCHEMA_NAME(t.schema_id) AS SchemaName, t.name AS TableName,
    tr.name AS TriggerName, tr.is_disabled,
    CASE WHEN tr.is_instead_of_trigger = 1 THEN 'INSTEAD OF' ELSE 'AFTER' END AS TriggerType
FROM sys.triggers tr
JOIN sys.tables t ON tr.parent_id = t.object_id
ORDER BY SchemaName, TableName" -W
```

### Health Check Interpretation

| Finding | Severity | Recommendation |
|---------|----------|----------------|
| Tables with no indexes | High (if > 1000 rows) | Add indexes based on query patterns; check auto-tuning recommendations |
| Tables with no primary keys | Medium | Add PKs for data integrity (enforced in SQL database in Fabric) |
| Disabled indexes | Low | Investigate why disabled; rebuild or drop |
| Tables with triggers | Informational | Review trigger logic for performance impact |

---

## Security Discovery

```bash
# Current user identity
$SQLCMD -Q "SELECT USER_NAME() AS current_user_name, SUSER_SNAME() AS login_name" -W

# Database principals
$SQLCMD -Q "
SELECT name, type_desc, authentication_type_desc
FROM sys.database_principals
WHERE type NOT IN ('R')
ORDER BY name" -W

# Role memberships
$SQLCMD -Q "
SELECT r.name AS role_name, m.name AS member_name
FROM sys.database_role_members drm
JOIN sys.database_principals r ON drm.role_principal_id = r.principal_id
JOIN sys.database_principals m ON drm.member_principal_id = m.principal_id
ORDER BY r.name, m.name" -W

# Object-level permissions
$SQLCMD -Q "
SELECT dp.state_desc + ' ' + dp.permission_name AS permission,
    OBJECT_SCHEMA_NAME(dp.major_id) + '.' + OBJECT_NAME(dp.major_id) AS [object],
    prin.name AS grantee
FROM sys.database_permissions dp
JOIN sys.database_principals prin ON dp.grantee_principal_id = prin.principal_id
WHERE dp.major_id > 0
ORDER BY [object], grantee" -W

# High-privilege users (members of db_owner or db_securityadmin)
$SQLCMD -Q "
SELECT r.name AS role_name, m.name AS member_name, m.type_desc
FROM sys.database_role_members drm
JOIN sys.database_principals r ON drm.role_principal_id = r.principal_id
JOIN sys.database_principals m ON drm.member_principal_id = m.principal_id
WHERE r.name IN ('db_owner', 'db_securityadmin', 'db_ddladmin')
ORDER BY r.name, m.name" -W
```

---

## Database Settings Review

```bash
$SQLCMD -Q "
SELECT name,
    compatibility_level,
    collation_name,
    is_auto_create_stats_on,
    is_auto_update_stats_on,
    is_auto_update_stats_async_on,
    is_read_committed_snapshot_on,
    is_query_store_on,
    delayed_durability_desc
FROM sys.databases
WHERE name = DB_NAME()" -W
```

---

## Text Search Across Tables

Searches for a specific text value across all string columns in all tables. Use with caution on large databases.

> **Note**: Full-text search (`CONTAINS`/`FREETEXT`) is a **preview feature** in SQL database in Fabric (third-party filters and word breakers not supported). This uses `LIKE` as a fallback.

```bash
# Replace 'search_text' with the target value
$SQLCMD -Q "
DECLARE @SearchText NVARCHAR(200) = N'search_text';
DECLARE @SQL NVARCHAR(MAX) = N'';

SELECT @SQL = @SQL +
    'SELECT ''' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) + '.' + QUOTENAME(c.name) + ''' AS location, '
    + 'CAST(' + QUOTENAME(c.name) + ' AS NVARCHAR(500)) AS value '
    + 'FROM ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name)
    + ' WHERE ' + QUOTENAME(c.name) + ' LIKE ''%'' + @p + ''%'' UNION ALL '
FROM sys.tables t
JOIN sys.schemas s ON t.schema_id = s.schema_id
JOIN sys.columns c ON t.object_id = c.object_id
JOIN sys.types ty ON c.user_type_id = ty.user_type_id
WHERE ty.name IN ('char','varchar','nchar','nvarchar','text','ntext');

SET @SQL = LEFT(@SQL, LEN(@SQL) - 10);  -- Remove trailing UNION ALL
EXEC sp_executesql @SQL, N'@p NVARCHAR(200)', @p = @SearchText;
" -W
```

---

## Active Connections

```bash
$SQLCMD -Q "
SELECT DB_NAME(database_id) AS database_name,
    login_name, program_name, host_name,
    COUNT(*) AS connection_count,
    MIN(connect_time) AS earliest_connection,
    MAX(last_request_start_time) AS latest_activity
FROM sys.dm_exec_sessions
WHERE is_user_process = 1
GROUP BY database_id, login_name, program_name, host_name
ORDER BY connection_count DESC" -W
```
