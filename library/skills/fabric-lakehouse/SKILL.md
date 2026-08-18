---
name: fabric-lakehouse
description: >-
  Explain, design, build, and optimize Microsoft Fabric Lakehouse solutions using OneLake, Delta tables, Files, SQL analytics endpoints, semantic models, shortcuts, schemas, materialized views, Spark views, security, lineage, ingestion, and table optimization. Use when the user asks about Fabric Lakehouse concepts, architecture, data layout, shortcuts, PySpark, loading data, or Lakehouse best practices.
metadata:
  author: tedvilutis
  version: "1.0"
---

# Fabric Lakehouse

Use Microsoft Fabric Lakehouse context to explain capabilities, choose storage patterns, organize tabular and non-tabular data, and recommend secure, performant Lakehouse designs.

## When to invoke

- "Explain what a Fabric Lakehouse is."
- "Design a Lakehouse layout for these tables and files."
- "How should I use shortcuts in Microsoft Fabric?"
- "Optimize these Delta tables for Power BI."
- "Show PySpark examples for loading data into a Lakehouse."

## Lakehouse model

A Lakehouse in Microsoft Fabric is an item that stores tabular data and non-tabular files in OneLake. It combines data lake flexibility with warehouse-style management.

| Capability | Lakehouse behavior |
| --- | --- |
| Unified storage | OneLake stores structured and unstructured data. |
| Table format | Delta Lake is the primary table format, with ACID transactions, versioning, and time travel. |
| Other tabular formats | CSV and Parquet can be stored and queried with Spark, but Delta is the managed table default. |
| SQL analytics endpoint | Auto-generated read-only SQL endpoint for T-SQL querying. |
| Semantic model | Power BI integration through the Lakehouse semantic model. |
| Files | Any file format can be stored under the `Files` folder. |
| Optimization | Table optimization, V-Order, `OPTIMIZE`, Z-ordering, and `VACUUM` support performance and maintenance. |

## Storage layout and table organization

| Area | Use for | Notes |
| --- | --- | --- |
| `Tables` | Managed tabular data | Delta tables live here by default. |
| `Tables/<schema>/<table>` | Schema-enabled table organization | Schemas are folders under `Tables`; `dbo` is the default schema and cannot be deleted or renamed. |
| `Files` | Unstructured and semi-structured data | Create folders and subfolders for any file format. |
| Internal tables | Data stored under `Tables` | Best for Lakehouse-owned data. |
| External tables | Reference under `Tables`, data elsewhere | Often backed by shortcuts. |
| Schema Shortcut | Reference to a schema in another Lakehouse | Brings all tables in the destination schema through one shortcut. |

When creating a Lakehouse, decide whether to enable schemas. Non-`dbo` schemas can be created, renamed, and deleted.

## Shortcuts and virtualization

Shortcuts create virtual links to data without copying it.

| Shortcut type | Use case |
| --- | --- |
| Internal | Link to other Fabric Lakehouses or tables, including cross-workspace sharing. |
| ADLS Gen2 | Link to Azure Data Lake Storage Gen2 containers. |
| Amazon S3 | Link to AWS S3 buckets for cross-cloud access. |
| Dataverse | Link to Microsoft Dataverse business application data. |
| Google Cloud Storage | Link to GCS buckets for cross-cloud access. |

Use shortcuts when governance, freshness, or data volume makes copying undesirable. Use managed Delta tables when the Lakehouse owns transformation output.

## Views and derived data

| Construct | Stores data | Defined with | Use when |
| --- | --- | --- | --- |
| Fabric Materialized Views | Yes, as pre-computed tables | PySpark or Spark SQL in an associated Notebook | Complex aggregations or joins need fast scheduled refresh. |
| Spark Views | No | Spark SQL, stored in the Lakehouse next to Tables | A virtual query layer is enough and storage duplication is undesirable. |
| SQL analytics endpoint objects | Read-only endpoint surface | Generated from Lakehouse tables | Consumers need T-SQL read access. |

## Security and governance

| Layer | Controls |
| --- | --- |
| Item access / control plane | Workspace roles: Admin, Member, Contributor, Viewer; Lakehouse sharing capabilities. |
| Data access / OneLake security | Microsoft Entra ID and RBAC on OneLake data. |
| Fine-grained table security | Object-level permissions plus column-level and row-level security for tables. |
| Lineage | Lakehouse lineage tracks origins and transformations for tables and files. |

Design access at both the Fabric item layer and the OneLake data layer. Do not assume workspace visibility grants every data operation.

## Performance optimization

| Technique | Use it for | Notes |
| --- | --- | --- |
| V-Order optimization | Faster reads for semantic model and common analytic access patterns | Presorts Delta data to improve query performance. |
| `OPTIMIZE` | Compact many small files into larger files | Run after high-volume ingestion or frequent updates. |
| Z-ordering | Improve queries filtered by specific columns | Apply with `OPTIMIZE` when access patterns are known. |
| `VACUUM` | Remove old files and free storage after updates/deletes | Balance cleanup with time-travel retention needs. |
| Materialized views | Precompute expensive aggregations and joins | Refresh on a schedule through the associated Notebook. |

## Progressive disclosure and bundled resources

- `references/pyspark.md`: PySpark code examples for Lakehouse operations.
- `references/getdata.md`: data ingestion approaches and loading guidance.

Use `Lakehouses/tables` wording when discussing internal shortcuts across Fabric items. Distinguish `Unstructured/semi-structured` files, `external/internal` shortcut targets, `role-based` access control, `object-level` permissions, and `fine-grained` row or column controls.

## Output template

```markdown
## Fabric Lakehouse guidance

**Status:** guidance | design | blocked
**Scenario:** `<question or workload>`

### Recommended Lakehouse shape
| Area | Recommendation | Rationale |
| --- | --- | --- |
| Storage | `<Tables/Files/shortcut layout>` | `<why>` |
| Security | `<workspace/OneLake/RLS/CLS>` | `<why>` |
| Performance | `<V-Order/OPTIMIZE/Z-order/materialized view>` | `<why>` |

### Next actions
1. `<action>`
2. `<action>`
3. `<validation>`
```

## Quality gate

- [ ] The answer distinguishes `Tables` from `Files` and Delta from CSV/Parquet where relevant.
- [ ] Schema behavior, including default `dbo`, was handled correctly when schemas are discussed.
- [ ] Shortcut recommendations name the correct source type: Internal, ADLS Gen2, Amazon S3, Dataverse, or Google Cloud Storage.
- [ ] Security guidance covers both Fabric item access and OneLake data access when access control is in scope.
- [ ] Performance advice chooses among V-Order, `OPTIMIZE`, Z-ordering, `VACUUM`, Spark Views, and Fabric Materialized Views based on workload.
- [ ] Bundled `references/pyspark.md` or `references/getdata.md` is used only when deeper examples are needed.
