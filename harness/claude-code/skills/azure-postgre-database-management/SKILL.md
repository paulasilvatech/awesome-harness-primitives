---
name: azure-postgre-database-management
description: >-
  Performs database operations and health monitoring for Open Horizons platform data services. Use
  this skill when checking PostgreSQL health, validating connections, reviewing backup settings,
  monitoring database size or active sessions, checking migrations, or troubleshooting database
  behavior.
---

<!-- Generated from harness/github-copilot/skills/azure-postgre-database-management/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure PostgreSQL Database Management

Use database access requirements and platform data-service context to run PostgreSQL health, connection, backup, and monitoring checks with concise evidence and recommendations.

## When to invoke

- "Check PostgreSQL database health."
- "Validate the Backstage database connection."
- "Review database backup retention."
- "Monitor active connections or database size."
- "Troubleshoot database connectivity or performance."

## Prerequisites and context

- Azure CLI for Azure databases.
- psql for PostgreSQL operations.
- Appropriate database credentials.

## Procedure

### Azure PostgreSQL

```bash
# List PostgreSQL servers
az postgres flexible-server list -o table

# Show server details
az postgres flexible-server show --name <server> --resource-group <rg>

# Check firewall rules
az postgres flexible-server firewall-rule list --name <server> --resource-group <rg>

# Check backup retention
az postgres flexible-server show --name <server> --resource-group <rg> --query "backup"
```

### Connection testing

```bash
# Test PostgreSQL connection
psql "host=<host> dbname=<db> user=<user> sslmode=require" -c "SELECT version();"

# Check active connections
psql -c "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"
```

### Health monitoring

```bash
# Check database size
psql -c "SELECT pg_size_pretty(pg_database_size(current_database()));"

# Check table sizes
psql -c "SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
         FROM pg_tables ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC LIMIT 10;"
```

### Best practices

1. Use private endpoints for database connectivity
2. Enable SSL/TLS for all connections
3. Configure automated backups
4. Monitor connection pool usage
5. Set up alerts for high CPU/memory

## Output template

Return exactly this structure:

```markdown
# Database management result

**Status:** PASS | FAIL | BLOCKED
**Database:** server/database name or unknown
**Summary:** One sentence describing database health or the issue found.

### Details
| Check | Result | Evidence |
| --- | --- | --- |
| Connection | PASS | `psql` response summary |
| Backup retention | PASS | Azure CLI query summary |
| Active connections | PASS | Count or threshold context |
| Size review | PASS | Database or table size summary |

### Recommendations
- Remediation or follow-up action.

### Validation evidence
- Command executed: exact command or redacted equivalent.
- Result: PASS | FAIL | BLOCKED with output summary.
```

## Limits

- Do not use this skill for Azure resource provisioning.
- Use `azure-cli` (`skill`) instead when creating or changing Azure database resources directly.
- Use `azure-terraform-cli` (`skill`) instead when database infrastructure must be changed through Terraform.
- Use `open-horizons-deploy-orchestration` (`skill`) instead when database work is part of full platform deployment sequencing.
- Use `azure-kubectl-cli` (`skill`) instead when the task is Kubernetes pod inspection.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `azure-cli` | `skill` | Azure database resource discovery or direct Azure operations are needed. |
| `azure-terraform-cli` | `skill` | Database infrastructure changes must be planned or applied as IaC. |
| `azure-kubectl-cli` | `skill` | Database troubleshooting requires Kubernetes workload inspection. |
| `azure-observability-stack` | `skill` | Metrics, dashboards, or alerts should monitor database behavior. |
| `open-horizons-deploy-orchestration` | `skill` | Database checks are part of platform deployment. |
| `open-horizons-sre-investigator` | `agent` | Database symptoms are part of an incident or reliability investigation. |
| `open-horizons-terraform` | `agent` | Database infrastructure code needs an owner. |

## Quality gate

- [ ] Database credentials are available from an approved source and never printed in full.
- [ ] SSL/TLS is required for PostgreSQL connection checks.
- [ ] Azure server, firewall, and backup checks include command evidence when in scope.
- [ ] Connection, active session, and size checks include result summaries.
- [ ] Recommendations separate immediate remediation from longer-term monitoring work.
