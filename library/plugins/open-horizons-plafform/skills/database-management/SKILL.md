---
name: database-management
description: "Use when operating Open Horizons databases, especially PostgreSQL health checks, connection testing, backup or restore validation, migration readiness, and monitoring; produces command output, health summary, findings, and recommendations. DO NOT USE FOR: Azure infrastructure provisioning (use azure-cli), Terraform IaC (use terraform-cli), or full platform deployment (use deploy-orchestration). Triggers include \"check PostgreSQL health\", \"verify database backup\", \"test the Backstage database connection\"."
---

# Database Management

This workflow performs safe database health, connectivity, backup, restore, and monitoring checks for Open Horizons services such as Backstage. It produces a health report and remediation recommendations while avoiding unapproved data mutation.

> [!NOTE]
> This skill shells out to `az` for Azure Database for PostgreSQL Flexible Server metadata and `psql` for database checks. Credentials must come from approved secret stores, and query output must not expose sensitive data.

## When to invoke
- "Check PostgreSQL health for Backstage."
- "Verify the backup retention on our database server."
- "Test whether the application can connect to the database."
- "Review database migration readiness before deployment."

## Prerequisites and context
- Azure CLI authenticated for Azure PostgreSQL metadata.
- `psql` installed for direct PostgreSQL checks.
- Database host, database name, and approved credentials available.
- Network path available from the execution environment.
- Explicit approval before restore, migration, schema mutation, or data-changing SQL.

## Procedure

### Step 1: Identify database scope
```bash
az postgres flexible-server list -o table
az postgres flexible-server show --name <server> --resource-group <resource-group> -o table
```

- [ ] Server, resource group, environment, and database are identified.
- [ ] Private endpoint and firewall posture are understood.
- [ ] Backup retention and maintenance settings are in scope.

### Step 2: Run read-only health checks
```bash
az postgres flexible-server firewall-rule list --name <server> --resource-group <resource-group> -o table
az postgres flexible-server show --name <server> --resource-group <resource-group> --query backup -o json
psql "host=<host> dbname=<database> user=<user> sslmode=require" -c "SELECT version();"
psql "host=<host> dbname=<database> user=<user> sslmode=require" -c "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"
```

### Step 3: Check size and activity without exposing data
```bash
psql "host=<host> dbname=<database> user=<user> sslmode=require" -c "SELECT pg_size_pretty(pg_database_size(current_database()));"
psql "host=<host> dbname=<database> user=<user> sslmode=require" -c "SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(format('%I.%I', schemaname, tablename))) FROM pg_tables ORDER BY pg_total_relation_size(format('%I.%I', schemaname, tablename)) DESC LIMIT 10;"
```

- [ ] Queries return metadata only, not customer rows.
- [ ] SSL is required.
- [ ] Connection pool pressure is noted.

### Step 4: Confirm before mutating data or configuration
```text
Database mutation summary:
- Server:
- Database:
- Operation: restore | migrate | schema change | data update | firewall change
- Backup or rollback plan:
Proceed with the database mutation? (y/n)
```

> [!IMPORTANT]
> Only proceed with restore, migration, schema changes, firewall changes, or data-changing SQL if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the findings and stop.

### Step 5: Validate backups and migration readiness
- [ ] Backup retention meets recovery requirements.
- [ ] Restore target and point-in-time are documented before restore.
- [ ] Migration scripts have been tested in non-production.
- [ ] Application connection strings use Key Vault or External Secrets rather than committed values.

## Risk classification
| Severity | Meaning |
|---|---|
| Critical | Data loss risk, restore without backup verification, credentials exposed, or production mutation without approval. |
| High | Backups disabled or too short, public access open, SSL disabled, or connection exhaustion. |
| Medium | Slow queries, large tables without maintenance plan, or missing monitoring alerts. |
| Low | Documentation, naming, or routine maintenance gaps. |

## Limits

- Do not use this skill for: Azure infrastructure provisioning (use azure-cli), Terraform IaC (use terraform-cli), or full platform deployment (use deploy-orchestration).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| Connection fails | Check DNS, firewall/private endpoint, SSL mode, username, and secret source. |
| Permission denied | Report the missing PostgreSQL or Azure role; do not request broader rights than needed. |
| Backup metadata unavailable | Use Azure CLI server show output and document the evidence gap. |
| Query may expose data | Replace it with aggregate or metadata-only SQL. |

## Output template

Return exactly this structure:
```markdown
# Database Health Report

## Scope
- Server:
- Database:
- Environment:

## Checks
| Check | Command | Result |
|---|---|---|

## Findings
| Severity | Finding | Recommendation |
|---|---|---|

## Backup And Recovery
- Retention:
- Last verified restore:
- Gaps:
```

## Quality gate
- [ ] All SQL is read-only unless explicit confirmation is captured.
- [ ] Secrets and row-level sensitive data are not printed.
- [ ] Backup, connectivity, SSL, and access posture are reported.
- [ ] Mutating operations include a rollback or restore plan.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
