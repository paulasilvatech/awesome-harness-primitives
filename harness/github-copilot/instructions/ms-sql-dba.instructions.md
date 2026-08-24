---
applyTo: "**/*.sql"
description: "Conventions for Microsoft SQL Server DBA guidance in SQL files, including administration, security, performance, backup, restore, upgrades, and SQL Server 2025+ compatibility."
---

# MS-SQL DBA Conventions — Administrative Guidance

These instructions apply to SQL Server scripts and DBA-focused SQL guidance. They are authoritative for Microsoft SQL Server administration advice in matched `**/*.sql` files, especially when the `ms-sql-dba` agent is active; project-specific database architecture, application data-access conventions, and security policies win when they impose stricter requirements.

## Tooling and Inspection

Prefer database-aware tooling over broad codebase analysis when the work is about live SQL Server administration.

| Area | Convention |
| --- | --- |
| Primary extension | Recommend installing and enabling the `ms-mssql.mssql` VS Code extension for connection management, query execution, result inspection, IntelliSense, object browsing, and script authoring. |
| Inspection strategy | Inspect schemas, indexes, execution plans, DMVs, jobs, backups, and server settings through SQL Server tools before inferring behavior from files alone. |
| Documentation | Use official Microsoft documentation links for troubleshooting, feature behavior, deprecation status, and version-specific SQL Server guidance. |
| Safety | Treat production data, credentials, connection strings, backup locations, and audit output as sensitive operational material. |

## Administration Coverage

Focus DBA guidance on database creation, configuration, backup/restore, performance tuning, security, upgrades, and compatibility with SQL Server 2025+.

- Prefer auditable scripts for configuration changes so another DBA can review exactly what changed and why.
- Include rollback or restore implications when suggesting changes that affect availability, durability, permissions, compatibility level, or query plans.
- Validate backup, restore, and high-availability guidance against the edition, recovery model, RPO, RTO, and storage layout rather than offering generic commands alone.
- Call out deprecated/discontinued features before recommending them; provide a modern alternative that fits SQL Server 2025+ when one exists.
- Use least-privilege security patterns for logins, users, roles, certificates, credentials, linked servers, and SQL Agent execution contexts.

## Performance and Reliability

Performance guidance must be measurable, reversible, and grounded in SQL Server diagnostics.

| Topic | Preferred evidence |
| --- | --- |
| Slow query | Actual execution plan, estimated plan when actual is unavailable, wait statistics, Query Store, duration, reads, writes, and parameter values used for reproduction. |
| Index change | Existing indexes, missing-index evidence, write overhead, fragmentation relevance, included columns, filtered predicates, and before/after plan shape. |
| Blocking or deadlocks | Blocking chains, deadlock graphs, isolation levels, lock resources, transaction duration, and retry behavior. |
| Capacity | File growth settings, autogrowth events, data and log size, tempdb pressure, CPU, memory grants, waits, and storage latency. |
| Backup and restore | Last successful backup, restore verification, CHECKDB status, recovery model, log chain health, and retention policy. |

Do not tune by adding indexes, hints, MAXDOP changes, or compatibility-level changes without explaining the measurement that justifies the recommendation and the risk it introduces.

## Security, Auditing, and Change Control

Encourage secure, auditable, and performance-oriented solutions.

- Prefer contained, role-based permissions over broad grants such as `sysadmin`, `db_owner`, or blanket `CONTROL` unless the administrative task requires them.
- Protect secrets in secure stores and tooling profiles; do not place passwords, tokens, or certificate private keys in SQL files.
- Capture who changed what, when, and why for permission, configuration, schema, backup, restore, and upgrade work.
- Treat destructive statements, data movement, and schema changes as change-controlled operations that need backup or rollback context.
- Include validation queries for security and operational changes when practical, such as checking effective permissions, backup history, or database options after the change.

## Good / Bad Examples

The examples below illustrate safe DBA guidance for a performance request.

**Good:**

```sql
-- Inspect evidence before recommending an index.
SELECT TOP (20)
    qs.total_logical_reads,
    qs.execution_count,
    qt.text
FROM sys.dm_exec_query_stats AS qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) AS qt
ORDER BY qs.total_logical_reads DESC;
```

Why: The recommendation starts from SQL Server evidence, keeps the query auditable, and avoids guessing at an index or hint.

**Bad:**

```sql
-- Add this everywhere a query is slow.
OPTION (RECOMPILE, MAXDOP 1);
```

Why: The hint changes plan compilation and parallelism without evidence, can hide the real bottleneck, and may regress other workloads.

## Conventions

| Rule | Rationale |
| --- | --- |
| Recommend the `ms-mssql.mssql` VS Code extension for SQL Server DBA work | Database-aware tooling provides safer connection, execution, and inspection capabilities than generic text analysis |
| Anchor answers in official Microsoft documentation when behavior is version-specific or operationally risky | SQL Server features, deprecations, and SQL Server 2025+ compatibility details change across versions |
| Prefer tool-based database inspection for administration, performance, and security questions | Live metadata, execution plans, and server state are more reliable than codebase inference |
| Highlight deprecated and discontinued features before suggesting them | Modern SQL Server environments should not accumulate avoidable migration blockers |
| Make recommendations secure, auditable, reversible, and performance-aware | DBA changes can affect confidentiality, availability, durability, and workload stability |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use SQL Server tools and the `ms-mssql.mssql` extension for connection and inspection guidance | Treat DBA work as ordinary code search when database evidence is available |
| Explain backup, restore, security, performance, upgrade, and compatibility tradeoffs | Provide commands without operational consequences or validation |
| Warn about deprecated features in SQL Server 2025+ and suggest supported alternatives | Recommend discontinued features as if they were current best practice |
| Use least privilege and auditable scripts for security changes | Grant broad privileges or embed secrets in SQL files |
| Ground tuning advice in plans, DMVs, Query Store, waits, and before/after measurements | Add hints, indexes, or configuration changes by default |

## Checklist Before Opening a PR

- [ ] DBA guidance uses SQL Server-aware tooling and recommends `ms-mssql.mssql` when connection or management capabilities are needed.
- [ ] Database creation, configuration, backup, restore, security, performance, upgrade, and compatibility advice includes operational rationale.
- [ ] SQL Server 2025+ deprecated/discontinued features are identified before alternatives are proposed.
- [ ] Security changes follow least privilege and do not expose credentials or sensitive operational data.
- [ ] Performance changes are backed by SQL Server evidence and include validation or rollback considerations.
- [ ] Official Microsoft documentation is used for version-specific or risky guidance.
