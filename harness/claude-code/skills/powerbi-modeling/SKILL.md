---
name: powerbi-modeling
description: >-
  Guide Power BI semantic model design and optimization for well-documented models with star
  schema checks, DAX measures, relationships, RLS, naming, descriptions, calculation groups,
  performance tuning, and model validation. Use when working with Power BI semantic models,
  creating measures, adding relationships, configuring cardinality or cross-filter direction,
  documenting models, or optimizing DAX and model performance.
---

<!-- Generated from harness/github-copilot/skills/powerbi-modeling/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Power BI semantic modeling

Connect to the active Power BI semantic model first, inspect its structure, and then provide model-specific guidance or changes for measures, relationships, documentation, RLS, calculation groups, and performance.

## When to invoke

- "Create a measure in my Power BI model."
- "Add or fix a relationship and cardinality."
- "Design this as a star schema."
- "Optimize this DAX formula or model performance."
- "Configure RLS or document this semantic model."

## Prerequisites and context

- Power BI Modeling MCP Server, often exposed as `power-bi-modeling`, is required for semantic model inspection and modification. It exposes `connection_operations`, `model_operations`, `table_operations`, `column_operations`, `measure_operations`, `relationship_operations`, `dax_query_operations`, `calculation_group_operations`, and `security_role_operations`.
- Microsoft Learn MCP Server is optional for current documentation research through `microsoft_docs_search` and `microsoft_docs_fetch`.

## Procedure

1. Connect and analyze before offering guidance:

```text
connection_operations(operation: "ListConnections")
connection_operations(operation: "ListLocalInstances")
model_operations(operation: "Get")
table_operations(operation: "List")
relationship_operations(operation: "List")
measure_operations(operation: "List")
```

2. If no connection exists, connect to the Desktop or Fabric model before reading or changing metadata.
3. Evaluate model health against star schema, relationships, naming, documentation, measures, hidden fields, date table, RLS, and performance rules.
4. Use bundled references for deeper decisions: `references/STAR-SCHEMA.md`, `references/RELATIONSHIPS.md`, `references/MEASURES-DAX.md`, `references/PERFORMANCE.md`, and `references/RLS.md`.
5. Make targeted changes only after model state is known, then validate with metadata reads or DAX validation as appropriate.

## Model quality checklist

| Area | Best practice |
| --- | --- |
| Tables | Clear dimension versus fact classification. |
| Naming | Human-readable names such as `Customer Name`, not `CUST_NM`. |
| Descriptions | All tables, columns, and measures are documented. |
| Measures | Business metrics use explicit DAX measures. |
| Relationships | One-to-many relationships flow from dimension to fact. |
| Cross-filter | Use single direction unless bidirectional filtering is specifically justified. |
| Hidden fields | Hide technical keys and IDs from report view. |
| Date table | Use a dedicated marked date table. |
| RLS | Define security roles with testable filters and effective-permission checks. |

## MCP operation reference

| Category | Key operations |
| --- | --- |
| `connection_operations` | Connect, ListConnections, ListLocalInstances, ConnectFabric. |
| `model_operations` | Get, GetStats, ExportTMDL. |
| `table_operations` | List, Get, Create, Update, GetSchema. |
| `column_operations` | List, Get, Create, Update descriptions, hidden state, and format. |
| `measure_operations` | List, Get, Create, Update, Move. |
| `relationship_operations` | List, Get, Create, Update, Activate, Deactivate. |
| `dax_query_operations` | Execute, Validate. |
| `calculation_group_operations` | List, Create, Update. |
| `security_role_operations` | List, Create, Update, GetEffectivePermissions. |

## Common modeling tasks

Create a measure with description:

```text
measure_operations(
  operation: "Create",
  definitions: [{
    name: "Total Sales",
    tableName: "Sales",
    expression: "SUM(Sales[Amount])",
    formatString: "$#,##0",
    description: "Sum of all sales amounts"
  }]
)
```

Update a column description and hide a technical key:

```text
column_operations(
  operation: "Update",
  definitions: [{
    tableName: "Customer",
    name: "CustomerKey",
    description: "Unique identifier for customer dimension",
    isHidden: true
  }]
)
```

Create a relationship:

```text
relationship_operations(
  operation: "Create",
  definitions: [{
    fromTable: "Sales",
    fromColumn: "CustomerKey",
    toTable: "Customer",
    toColumn: "CustomerKey",
    crossFilteringBehavior: "OneDirection"
  }]
)
```

## Microsoft Learn usage

Use `microsoft_docs_search` and `microsoft_docs_fetch` for latest DAX functions, new Power BI features, SCD Type 2 or many-to-many modeling patterns, performance optimization, and security implementation guidance.

## Gotchas

- **Do not provide generic advice before connecting**; always inspect the active model first.
- **Do not create bidirectional relationships by default**; they can hide ambiguity and performance issues.
- **Do not expose technical keys**; hide IDs and surrogate keys from report view.
- **Do not use calculated columns for business metrics when an explicit measure is appropriate**.

## Progressive disclosure and bundled resources

- `references/STAR-SCHEMA.md`: dimension/fact table design and model shape rules.
- `references/RELATIONSHIPS.md`: relationship cardinality and cross-filter guidance.
- `references/MEASURES-DAX.md`: DAX measures, naming, and descriptions.
- `references/PERFORMANCE.md`: optimization and model performance checks.
- `references/RLS.md`: row-level security implementation patterns.

## Output template

```markdown
## Power BI modeling result

**Status:** complete | needs connection | blocked
**Model:** `<model name or connection>`

### Model observations
| Area | Finding | Recommendation |
| --- | --- | --- |
| Relationships | <finding> | <fix> |

### Changes or proposed changes
| Object | Operation | Definition |
| --- | --- | --- |
| `<measure/table/relationship>` | `<create|update|validate>` | `<details>` |

### Validation
- Connection inspected: <pass|fail>
- DAX validation: <pass|fail|not applicable>
- Metadata re-read: <pass|fail>
```

## Quality gate

- [ ] Existing connections or local instances were checked before guidance.
- [ ] Model, tables, relationships, and measures were inspected before changes.
- [ ] Star schema, naming, descriptions, measures, hidden fields, date table, RLS, and performance were considered as relevant.
- [ ] Relationship changes specify cardinality and `crossFilteringBehavior`.
- [ ] Measure changes include expression, table, format string, and description.
- [ ] Microsoft Learn research was used for current or complex scenarios when available.
