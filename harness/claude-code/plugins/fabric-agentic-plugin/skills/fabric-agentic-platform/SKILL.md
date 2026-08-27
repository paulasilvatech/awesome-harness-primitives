---
name: fabric-agentic-platform
description: >-
  Route and execute Microsoft Fabric administration, data engineering, real-time intelligence,
  SQL, Spark, Power BI, Git integration, migration, cost estimation, and end-to-end architecture
  workflows. Use when a request spans Fabric workloads or needs the correct specialist guide, MCP
  server, REST/CLI path, safety gate, and verification sequence.
---

<!-- Generated from harness/github-copilot/plugins/fabric-agentic-plugin/skills/fabric-agentic-platform/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Fabric agentic platform

Select and apply the smallest Microsoft Fabric specialist guide needed for the request. Detailed imported guides are bundled as progressive resources; do not load unrelated workload material.

## When to invoke

- "Which Fabric skill should handle this request?"
- "Design an end-to-end Fabric medallion architecture."
- "Migrate Synapse, HDInsight, or Databricks to Fabric."
- "Operate Eventhouse, Eventstream, Spark, SQL DB, or Warehouse."
- "Estimate Fabric capacity and workload cost."
- "Query or author Power BI semantic models and reports."

## Specialist routing

Read the selected guide before the first Fabric API, CLI, MCP, or state-changing operation.

| Request | Bundled guide |
| --- | --- |
| Activator and Reflex alerts | [Activator CLI](references/skills/activator-cli/SKILL.md) |
| Azure Monitor mirrored catalogs | [AzMon mirrored catalogs](references/skills/azmon-mirroredcatalogs-operations-cli/SKILL.md) |
| Databricks migration | [Databricks migration](references/skills/databricks-migration/SKILL.md) |
| Dataflows | [Dataflows CLI](references/skills/dataflows-cli/SKILL.md) |
| Deployment pipelines and Git promotion | [Deployment pipelines](references/skills/deployment-pipelines-authoring-cli/SKILL.md) |
| Cost estimation and capacity sizing | [Fabric cost estimation](references/skills/e2e-fabric-cost-estimation/SKILL.md) |
| Medallion architecture | [Medallion architecture](references/skills/e2e-medallion-architecture/SKILL.md) |
| Eventhouse and KQL databases | [Eventhouse CLI](references/skills/eventhouse-cli/SKILL.md) |
| Event schema sets | [Event schema set CLI](references/skills/eventschemaset-cli/SKILL.md) |
| Eventstream | [Eventstream CLI](references/skills/eventstream-cli/SKILL.md) |
| Fabric IQ data questions | [Fabric IQ](references/skills/fabriciq/SKILL.md) |
| Fabric IQ ontology | [Fabric IQ ontology CLI](references/skills/fabriciq-ontology-cli/SKILL.md) |
| Git integration operations | [Git integration](references/skills/git-integration-operations-cli/SKILL.md) |
| HDInsight migration | [HDInsight migration](references/skills/hdinsight-migration/SKILL.md) |
| Pipeline migration | [Pipeline migration](references/skills/pipeline-migration/SKILL.md) |
| Search and discovery | [Search consumption](references/skills/search-consumption-cli/SKILL.md) |
| Semantic model authoring | [Semantic model authoring](references/skills/semantic-model-authoring/SKILL.md) |
| Spark, notebooks, and Lakehouse | [Spark CLI](references/skills/spark-cli/SKILL.md) |
| Fabric SQL Database | [SQL DB CLI](references/skills/sqldb-cli/SKILL.md) |
| Warehouse and SQL endpoint | [SQL DW CLI](references/skills/sqldw-cli/SKILL.md) |
| Synapse migration | [Synapse migration](references/skills/synapse-migration/SKILL.md) |
| Variable libraries | [Variable library CLI](references/skills/variable-library-cli/SKILL.md) |

Power BI report authoring resources are bundled under `references/skills/powerbi-authoring/skills/`. Broader Power Platform packages embedded in the source import remain reference material; use their separately installable plugins when available.

## Shared prerequisites

- Confirm the tenant, capacity, workspace, item type, item ID, and requested read/write scope.
- Use Microsoft Entra authentication for the target Fabric audience.
- Confirm the required MCP tool is visible before choosing an MCP-first path.
- Read [common Fabric CLI guidance](references/common/COMMON-CLI.md) for authentication, pagination, long-running operations, telemetry, and shell-safe invocation.
- Read [common Fabric core guidance](references/common/COMMON-CORE.md) for topology, capacities, workspaces, items, and REST behavior.
- Use [item definition guidance](references/common/ITEM-DEFINITIONS-CORE.md) before authoring definition parts.

## Procedure

1. Classify the request by workload and by read, author, operate, migrate, or analyze intent.
2. Select one specialist guide from the routing table. If two guides are required, execute them sequentially and keep ownership explicit.
3. Read the selected guide and only the shared references it names.
4. Resolve tenant, workspace, item, capacity, and authentication context with read-only calls.
5. State assumptions, required permissions, expected cost or capacity impact, and rollback path.
6. Ask before create, update, delete, deployment, capacity, permission, or production-impacting operations.
7. Execute the smallest approved operation using the exact tool available in the session.
8. Verify by reading the resulting item, definition, job, query result, or deployment state.
9. Report commands or tools used, identifiers, result, remaining risk, and any unverified step.

## Safety and telemetry

- Never invent workspace IDs, item IDs, capacities, endpoints, schemas, or credentials.
- Never expose access tokens, connection strings, service principal secrets, or customer data.
- Preserve telemetry headers required by the selected guide on every Fabric API call and long-running-operation poll.
- Treat destructive calls, permission changes, Git promotion, capacity scaling, and production writes as approval-gated.
- Keep consumption modes read-only.
- Use bounded pagination, query limits, and retries; report truncation and throttling.
- Prefer current Microsoft Fabric documentation when API versions, limits, item definitions, or MCP tools may have changed.

## MCP configuration

The plugin registers:

- `FabricIQ` for Fabric AI Hub and Power BI data exploration.
- `fabric-sqlendpoint` for SQL endpoint query execution.

If a required tool is not visible, report it and use a documented CLI or REST fallback only when the selected guide provides one. See [MCP setup](references/mcp-setup/README.md).

## Limits

- Do not load every bundled guide into context.
- Do not treat imported specialist guides as separate discovered skills; they are progressive resources owned by this skill.
- Use separately packaged Power BI or Power Platform plugins when the request is confined to those domains.
- Do not claim current Fabric API behavior without Microsoft documentation or observed target-environment evidence.

## Output template

```markdown
## Fabric operation result

**Specialist guide:** <guide>
**Workspace/item:** <resolved identifiers>
**Mode:** <read|author|operate|migrate|analyze>
**Status:** <completed|blocked|needs approval>

### Evidence
- Authentication and target: <result>
- Tool or endpoint: <result>
- Operation: <result>
- Readback or verification: <result>

### Safety and operations
- Approval: <not required|received|missing>
- Cost/capacity impact: <result>
- Rollback: <path or not applicable>
- Remaining risk: <result>
```

## Progressive disclosure and bundled resources

- `references/common/`: shared Fabric REST, CLI, item-definition, workload, and notebook guidance.
- `references/skills/`: imported specialist guides and their own references.
- `references/mcp-setup/README.md`: plugin MCP availability and fallback guidance.

## Quality gate

- [ ] Exactly one primary specialist guide is selected.
- [ ] Tenant, workspace, item, capacity, and authentication context are resolved rather than assumed.
- [ ] Required guide and shared references were read before execution.
- [ ] State-changing or production-impacting work has explicit approval.
- [ ] Tokens, secrets, and customer data are absent from output.
- [ ] Telemetry, pagination, long-running operations, limits, and throttling follow the selected guide.
- [ ] A readback or explicit verification blocker is reported.
- [ ] Current platform claims cite Microsoft documentation or observed evidence.
