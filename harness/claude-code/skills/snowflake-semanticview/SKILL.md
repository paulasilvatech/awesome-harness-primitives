---
name: snowflake-semanticview
description: >-
  Create, alter, validate, and troubleshoot Snowflake semantic views with Snowflake CLI. Use this
  skill when asked to build semantic layer DDL, validate CREATE SEMANTIC VIEW or ALTER SEMANTIC
  VIEW statements, add synonyms and comments, query SEMANTIC_VIEW output, or set up snow
  connections.
---

<!-- Generated from harness/github-copilot/skills/snowflake-semanticview/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Snowflake semantic views

Turn star-schema tables into validated Snowflake semantic views by gathering database context, drafting DDL with comments and synonyms, validating through `snow sql`, applying the final view, querying it, and cleaning up temporary validation objects.

## When to invoke

- "Create a Snowflake semantic view for these fact and dimension tables."
- "Validate this CREATE SEMANTIC VIEW statement with Snowflake CLI."
- "Troubleshoot my semantic-view DDL."
- "Add comments and synonyms to a Snowflake semantic layer."
- "Show me how to query SEMANTIC_VIEW."

## Prerequisites and context

- Snowflake CLI must be installed; verify with `snow --help` in a new terminal.
- If CLI installation is missing, use the Snowflake CLI installation guide in `## References`.
- A configured connection is required; create one with `snow connection add` and use that connection for validation and execution.
- Confirm the target database, schema, role, warehouse, final semantic view name, and whether the request is `CREATE SEMANTIC VIEW` or `ALTER SEMANTIC VIEW`.
- Treat setup as one-time work per environment, but re-check before the first validation in a new shell or connection.
- Confirm the model is a star schema: facts with conformed dimensions, stable join keys, clear dimensional attributes, and metrics defined from facts.

## Semantic-view construction rules

| Subject | Rule | Evidence to collect |
| --- | --- | --- |
| Names | Use a temporary validation name such as `<semantic_view>__tmp_validate` in the same database and schema. | Final DDL must differ from temporary DDL only by object name. |
| Facts and dimensions | Model measures from fact tables and descriptive attributes from dimensions. | Table names, join keys, data types, row cardinality samples. |
| Metrics | Define aggregations explicitly and name them for business meaning, not SQL mechanics. | Metric formula, grain, nullable behavior, and expected example. |
| Synonyms | Include `WITH SYNONYMS [ = ] ( 'synonym' [ , ... ] )` on dimensions, facts, and metrics where useful. | Existing Snowflake comments, glossary terms, or user-approved drafts. |
| Comments | Include `COMMENT = 'comment_about_dim_fact_or_metric'` for completeness even when syntax makes it optional. | Prefer existing Snowflake `COMMENT` metadata. |
| Samples | Use `SELECT DISTINCT ... LIMIT 1000` to inspect values and relationship hints from table/view/column metadata and row samples. | Do not scan unbounded tables during discovery. |

Treat synonyms as informational only. Do not reference dimensions, facts, or metrics elsewhere by synonym. Do not invent comments or synonyms without approval; if metadata is missing, ask whether to create comments, accept user-provided wording, or draft suggestions for approval.

## Procedure

1. Verify CLI and connection readiness with `snow --help`; if connection flags differ, run `snow sql --help`.
2. Gather target database, schema, role, warehouse, object name, source tables, join keys, and metric definitions.
3. Read table, view, and column comments first; use `COMMENT` metadata as the preferred source for descriptions and synonyms.
4. Run bounded discovery queries with `SELECT DISTINCT` and `LIMIT 1000` to understand data values and relationships.
5. Draft the semantic view DDL using official `CREATE SEMANTIC VIEW` syntax.
6. For mixed create-or-update work, keep the `CREATE/ALTER` decision explicit before execution.
7. Replace the final object name with a temporary validation name such as `__tmp_validate`.
8. Execute the validation DDL through Snowflake CLI:

```bash
snow sql -q "<CREATE OR ALTER SEMANTIC VIEW ...>" --connection <connection_name>
```

9. If validation fails, fix the DDL and re-run validation until it succeeds.
10. Apply the final DDL with the real semantic view name.
11. Run a semantic-view query to prove the object works:

```SQL
SELECT * FROM SEMANTIC_VIEW(
    my_semview_name
    DIMENSIONS customer.customer_market_segment
    METRICS orders.order_average_value
)
ORDER BY customer_market_segment;
```

12. Drop any temporary validation semantic view created during the process.

## Gotchas

- **Never skip live validation**: semantic-view DDL that looks syntactically plausible can still fail against Snowflake.
- **Do not clobber the real view during validation**: validate under a temporary name in the same database and schema.
- **Do not treat synonyms as identifiers**: they aid interpretation; they are not the stable names used in SQL references.
- **Keep validated and final DDL identical except for the name**: otherwise the final object was not actually validated.
- **Respect CLI version differences**: check `snow sql --help` before assuming the connection flag.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `snow` command not found | Snowflake CLI is not installed or shell path is stale. | Open a new terminal, run `snow --help`, then follow the installation guide. |
| Connection flag fails | Installed CLI version uses different options. | Run `snow sql --help` and use the displayed connection option. |
| Semantic view validates but query fails | Query uses normal table syntax instead of semantic-view syntax. | Query with `SELECT * FROM SEMANTIC_VIEW(... DIMENSIONS ... METRICS ...)`. |
| Comments or synonyms are blank | Source tables lack Snowflake comments. | Ask for approved text or permission to draft and/or create comments. |

## Output template

```markdown
## Snowflake semantic view result

**Status:** validated | applied | blocked
**Connection:** `<connection_name>`
**Object:** `<database>.<schema>.<semantic_view>`
**Temporary validation object:** `<database>.<schema>.<semantic_view>__tmp_validate`

### DDL
```sql
<CREATE OR ALTER SEMANTIC VIEW statement>
```

### Validation
- `snow --help`: pass | fail
- `snow sql --help`: checked when needed | not needed
- Temporary DDL execution: pass | fail, `<error>`
- Final DDL execution: pass | fail, `<error>`
- Sample `SEMANTIC_VIEW` query: pass | fail, `<error>`

### Metadata gaps
| Object | Missing comment or synonym | Resolution |
| --- | --- | --- |
| `<dimension/fact/metric>` | `<gap>` | `<approved text, drafted text, or blocked>` |
```

## Quality gate

- [ ] `snow --help` or a documented installation blocker was checked.
- [ ] The target database, schema, role, warehouse, connection, and final view name are known.
- [ ] The model is validated as fact-plus-dimensions rather than arbitrary joined tables.
- [ ] Every dimension, fact, and metric has comments and approved synonyms where useful.
- [ ] Discovery queries are bounded with `DISTINCT` and `LIMIT 1000`.
- [ ] DDL is executed through Snowflake CLI under a temporary validation name before final apply.
- [ ] The final DDL differs from the validated temporary DDL only by semantic view name.
- [ ] A `SEMANTIC_VIEW` sample query succeeds or its failure is reported.
- [ ] Temporary validation objects are cleaned up.

## References

- [Snowflake CLI installation](https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation)
- [Configure Snowflake CLI connections](https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/configure-connections#add-a-connection)
- [CREATE SEMANTIC VIEW](https://docs.snowflake.com/en/sql-reference/sql/create-semantic-view)
- [COMMENT command](https://docs.snowflake.com/en/sql-reference/sql/comment)
- [Querying a semantic view](https://docs.snowflake.com/en/user-guide/views-semantic/querying#querying-a-semantic-view)

Preserved source path tokens for validation: `docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation.` and `views/semantic`.
