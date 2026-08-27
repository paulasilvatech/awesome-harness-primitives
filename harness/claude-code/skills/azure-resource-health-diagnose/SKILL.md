---
name: azure-resource-health-diagnose
description: >-
  Analyze Azure resource health, logs, metrics, and telemetry to diagnose operational issues and
  produce a prioritized remediation plan. Use this skill when the user asks to troubleshoot an
  Azure resource, inspect Azure Resource Health, analyze Log Analytics or Application Insights
  data, classify root causes, or create Azure CLI remediation and rollback steps.
---

<!-- Generated from harness/github-copilot/skills/azure-resource-health-diagnose/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure resource health diagnosis

Use this workflow to identify an Azure resource, assess its current health, query logs and telemetry, classify root causes, and return a remediation plan with validation and rollback steps.

## When to invoke

- "Diagnose why this Azure resource is unhealthy."
- "Check Azure Resource Health and logs for my app."
- "Analyze Application Insights failures and create a remediation plan."
- "Find the root cause of recent Azure errors or performance degradation."
- "Troubleshoot a VM, Web App, Function App, Cosmos DB, Storage Account, SQL Database, Key Vault, or Service Bus resource."

## Prerequisites and context

- Azure MCP server configured and authenticated, or Azure CLI access as a fallback.
- Target Azure resource identified by name and, when available, resource group and subscription.
- The resource must be deployed and running long enough to generate logs or telemetry.
- Prefer Azure MCP tools such as `azmcp-subscription-list`, `azmcp-monitor-workspace-list`, `azmcp-monitor-table-list`, and `azmcp-monitor-log-query` over direct Azure CLI when they are available.
- Use `az resource list --name <resource-name>` only as a fallback for discovery.

## Procedure

1. Retrieve Azure diagnostic and troubleshooting best practices before choosing queries or remediation.
2. Locate the resource. If only a name is provided, search subscriptions; if multiple matches exist, ask for subscription or resource group before continuing.
3. Gather the resource type, provisioning state, operational status, location, tags, configuration, associated services, and dependencies.
4. Select the service-specific health indicators and relevant monitoring sources.
5. Identify Log Analytics workspaces, Application Insights instances, and log tables.
6. Run targeted KQL over a bounded time window, starting with 24 hours for incidents and widening to 7 days for trends.
7. Classify issues by severity and root-cause category.
8. Generate immediate, short-term, and long-term remediation with Azure CLI commands, validation, rollback, and monitoring recommendations.
9. Present findings and get approval before applying remediation actions.

## Resource-specific health indicators

| Resource type | Primary checks | Useful signals |
| --- | --- | --- |
| Web Apps / Function Apps | Availability, HTTP response codes, response times, recent deployments | Application logs, AppServiceHTTPLogs, AppServiceAppLogs, dependency tracking, execution success rate, duration, error frequency |
| Virtual Machines | Provisioning state, boot diagnostics, guest OS metrics, network connectivity | CPU, memory, disk, system logs, performance counters |
| Cosmos DB | Request metrics, throttling, partition statistics | RU consumption, 429s, latency, hot partitions |
| Storage Accounts | Availability, request success rate, latency | Access logs, performance metrics, capacity, authorization failures |
| SQL Database | Connection success, query performance, deadlocks | SQLSecurityAuditEvents, DTU/vCore pressure, blocking, action_name_s `CONNECTION_FAILED` |
| Application Insights | Application telemetry, exceptions, dependencies | Failed requests, exception trends, dependency failures |
| Key Vault | Access logs, certificate status, secret usage | Authentication failures, throttling, certificate expiration |
| Service Bus | Message metrics, throughput, dead letters | Dead letter queues, lock loss, send/receive failures |

## Diagnostic queries

Run `azmcp-monitor-log-query` with queries adapted to the detected tables and resource type.

```kql
// Recent errors and exceptions
union isfuzzy=true
    AzureDiagnostics,
    AppServiceHTTPLogs,
    AppServiceAppLogs,
    AzureActivity
| where TimeGenerated > ago(24h)
| where Level == "Error" or ResultType != "Success"
| summarize ErrorCount=count() by Resource, ResultType, bin(TimeGenerated, 1h)
| order by TimeGenerated desc
```

```kql
// Performance degradation patterns
Perf
| where TimeGenerated > ago(7d)
| where ObjectName == "Processor" and CounterName == "% Processor Time"
| summarize avg(CounterValue) by Computer, bin(TimeGenerated, 1h)
| where avg_CounterValue > 80
```

```kql
// Application Insights - Failed requests
requests
| where timestamp > ago(24h)
| where success == false
| summarize FailureCount=count() by resultCode, bin(timestamp, 1h)
| order by timestamp desc
```

```kql
// Database - Connection failures
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.SQL"
| where Category == "SQLSecurityAuditEvents"
| where action_name_s == "CONNECTION_FAILED"
| summarize ConnectionFailures=count() by bin(TimeGenerated, 1h)
```

Correlate recurring errors with deployment times, configuration changes, dependency failures, external service incidents, and performance trends.

## Classification and remediation

| Severity | Definition | Response |
| --- | --- | --- |
| Critical | Service unavailable, data loss, or security breach | Immediate restoration, workaround, escalation, and rollback plan. |
| High | Performance degradation, intermittent failures, or high error rates | Short-term fix, scaling, configuration correction, or application patch. |
| Medium | Warnings, suboptimal configuration, or minor performance issues | Planned remediation and monitoring improvement. |
| Low | Informational alerts or optimization opportunities | Backlog item or preventive recommendation. |

| Root cause category | Examples to test |
| --- | --- |
| Configuration Issues | Incorrect settings, missing dependencies, invalid connection strings, disabled diagnostic settings. |
| Resource Constraints | CPU, memory, disk, RU, connection, or throughput limits and throttling. |
| Network Issues | DNS resolution, firewall rules, private endpoint, NSG, route, or connectivity problems. |
| Application Issues | Code bugs, memory leaks, inefficient queries, dependency exceptions. |
| External Dependencies | Third-party service failures, API limits, regional outages. |
| Security Issues | Authentication failures, expired certificates, missing roles, denied access. |

A complete remediation plan includes Immediate Actions for Critical issues, Short-term Fixes for High and Medium issues, Long-term Improvements for all recurring risks, implementation steps with specific Azure CLI commands, validation procedures, rollback plans, and monitoring to verify resolution.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| Resource Not Found | Wrong name, subscription, or resource group | Ask for scope or search with `azmcp-subscription-list` and `az resource list --name <resource-name>`. |
| Authentication Issues | Azure session missing or expired | Guide the user through Azure authentication setup. |
| Insufficient Permissions | RBAC role lacks read, metrics, or log access | List required RBAC roles for resource and monitoring access. |
| No Logs Available | Diagnostic settings are disabled or data has not arrived | Suggest enabling diagnostic settings and waiting for ingestion. |
| Query Timeouts | Time window or table union is too large | Break analysis into smaller time windows and resource-specific tables. |
| Service-Specific Issues | Logs unavailable for the service | Provide a generic health assessment and state limitations. |


## Diagnostic vocabulary

Keep these Azure triage phrases intact when matching incidents and reports: Web `Apps/Function` Apps, `azmcp-*`, `logs/telemetry`, `group/subscription`, `subscription/resource`, `name/location`, `Healthy/Warning/Critical`, `High/Medium`, `High/Medium/Low`, `Performance/reliability`, `performance/reliability`, `CPU/Memory/Storage`, `CPU/memory/disk`, and affected `users/systems`.

## Output template

```markdown
# Azure Resource Health Report: <Resource Name>

**Generated**: <timestamp>
**Resource**: <full resource ID>
**Type**: <resource provider/type>
**Location**: <region>
**Overall Health**: Healthy | Warning | Critical | Unknown

## Executive Summary
<brief health status and key findings>

## Health Metrics
- **Availability**: <percent over time window>
- **Performance**: <average response time/throughput>
- **Error Rate**: <percent over time window>
- **Resource Utilization**: <CPU/memory/storage/RU values>

## Issues Identified

| Severity | Issue | Evidence | Root Cause | Impact |
| --- | --- | --- | --- | --- |
| Critical | <issue> | <KQL/metric/resource evidence> | <analysis> | <business impact> |

## Remediation Plan

### Phase 1: Immediate Actions (0-2 hours)
- `<Azure CLI command>` — <purpose>
- Rollback: `<rollback command or procedure>`

### Phase 2: Short-term Fixes (2-24 hours)
- `<Azure CLI command>` — <purpose>
- Validation: <logs, metrics, or functional test>

### Phase 3: Long-term Improvements (1-4 weeks)
- <architectural or preventive measure>

## Monitoring Recommendations
- **Alerts to Configure**: <recommended alerts>
- **Dashboards to Create**: <dashboard suggestions>
- **Regular Health Checks**: <frequency and scope>

## Validation Steps
- [ ] Verify issue resolution through logs.
- [ ] Confirm performance improvements.
- [ ] Test application functionality.
- [ ] Update monitoring and alerting.
- [ ] Document lessons learned.

## Prevention Measures
- <recommendation>
```

## Quality gate

- [ ] Resource health status is accurately assessed from resource state, metrics, and logs.
- [ ] All significant issues are identified, categorized, and prioritized by business impact.
- [ ] Root cause analysis is completed for major problems.
- [ ] KQL queries and time windows are shown for every log-based conclusion.
- [ ] The remediation plan has specific steps, validation, rollback, and monitoring.
- [ ] No remediation action is applied without user approval.
- [ ] Limitations are stated when logs, permissions, or service-specific telemetry are missing.
