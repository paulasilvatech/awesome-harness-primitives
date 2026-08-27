---
description: Diagnose Azure resource health issues and produce a prioritized remediation plan.
argument-hint: "resource=<name-or-id> resource-group=<optional> subscription=<optional>"
allowed-tools: Read, Grep, Glob, mcp__azure-mcp
---

<!-- Generated from harness/github-copilot/prompts/azure-resource-health-diagnose.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /azure-resource-health-diagnose

## Objective

Analyze a specific Azure resource, assess health status, diagnose issues from logs and telemetry, classify root causes, and produce a prioritized remediation plan with validation, rollback, monitoring, and prevention guidance.

## When to Invoke

Use this prompt when an Azure resource is deployed and running but shows health warnings, errors, performance degradation, availability issues, failed dependencies, or unknown operational symptoms.

## Preconditions

- Azure MCP server is configured and authenticated.
- The target Azure resource is identified by name and optionally `resource group/subscription`.
- The resource is deployed and running enough to generate `logs/telemetry`.
- Prefer Azure MCP tools (`azmcp-*`) over direct Azure CLI when available.
- The user has sufficient Azure RBAC permissions to inspect health, metrics, logs, and configuration.

## Inputs the Team Must Provide

- `resource` — resource name or full resource ID.
- Optional `resource-group` and `subscription` when the name is not unique.
- Known symptom, time window, recent deployment, or configuration change.
- Any business impact, affected users, recovery time objective, or severity expectation.
- Ask the user for anything that is missing, especially when multiple matching resources exist.

## What I Will Do

- Retrieve diagnostic and troubleshooting best practices before analysis.
- Locate the target resource across subscriptions and resource groups.
- Gather resource type, current status, location, tags, configuration, dependencies, and associated services.
- Check provisioning state, operational status, availability, responsiveness, recent changes, and utilization.
- Find Log Analytics workspaces, Application Insights instances, and relevant log tables.
- Run targeted KQL queries for errors, performance degradation, failed requests, and connection failures.
- Classify issues by severity and root cause category.
- Produce immediate, short-term, and long-term remediation steps with validation and rollback.

## What I Will NOT Do

- Make remediation changes without explicit approval when the action changes Azure resources.
- Treat missing telemetry as proof of health.
- Ignore authentication, RBAC, or diagnostic-setting gaps.
- Use direct Azure CLI when an Azure MCP tool can provide the same evidence.
- Diagnose from application code alone; this workflow uses Azure health, logs, metrics, and telemetry.
- Invent resource configuration, log tables, or root causes that were not observed.

## Output Format

Return the health assessment and detailed report in this format:

````markdown
# Azure Resource Health Report: [Resource Name]

**Generated**: [Timestamp]  
**Resource**: [Full Resource ID]  
**Overall Health**: [Healthy/Warning/Critical]

## Azure Resource Health Assessment

Resource Overview:
• Resource: [Name] ([Type])
• Status: [Healthy/Warning/Critical]
• Location: [Region]
• Last Analyzed: [Timestamp]

Issues Identified:
• Critical: X issues requiring immediate attention
• High: Y issues affecting performance/reliability
• Medium: Z issues for optimization
• Low: N informational items

Top Issues:
1. [Issue Type]: [Description] - Impact: [High/Medium/Low]
2. [Issue Type]: [Description] - Impact: [High/Medium/Low]
3. [Issue Type]: [Description] - Impact: [High/Medium/Low]

Remediation Plan:
• Immediate Actions: X items
• Short-term Fixes: Y items
• Long-term Improvements: Z items
• Estimated Resolution Time: [Timeline]

## Executive Summary
[Brief overview of health status and key findings]

## Health Metrics
- **Availability**: X% over last 24h
- **Performance**: [Average response time/throughput]
- **Error Rate**: X% over last 24h
- **Resource Utilization**: [CPU/Memory/Storage percentages]

## Issues Identified

### Critical Issues
- **[Issue 1]**: [Description]
  - **Root Cause**: [Analysis]
  - **Impact**: [Business impact]
  - **Immediate Action**: [Required steps]

### High Priority Issues
- **[Issue 2]**: [Description]
  - **Root Cause**: [Analysis]
  - **Impact**: [Performance/reliability impact]
  - **Recommended Fix**: [Solution steps]

## Remediation Plan

### Phase 1: Immediate Actions (0-2 hours)
```bash
# Critical fixes to restore service
[Azure CLI commands with explanations]
```

### Phase 2: Short-term Fixes (2-24 hours)
```bash
# Performance and reliability improvements
[Azure CLI commands with explanations]
```

### Phase 3: Long-term Improvements (1-4 weeks)
```bash
# Architectural and preventive measures
[Azure CLI commands and configuration changes]
```

## Monitoring Recommendations
- **Alerts to Configure**: [List of recommended alerts]
- **Dashboards to Create**: [Monitoring dashboard suggestions]
- **Regular Health Checks**: [Recommended frequency and scope]

## Validation Steps
- [ ] Verify issue resolution through logs
- [ ] Confirm performance improvements
- [ ] Test application functionality
- [ ] Update monitoring and alerting
- [ ] Document lessons learned

## Prevention Measures
- [Recommendations to prevent similar issues]
- [Process improvements]
- [Monitoring enhancements]
````

## Definition of Done

- [ ] Resource health status is accurately assessed.
- [ ] Significant issues are identified, categorized, and prioritized.
- [ ] Root cause analysis is completed for major problems.
- [ ] Remediation plan includes specific steps, validation, and rollback procedures.
- [ ] Monitoring and prevention recommendations are included.
- [ ] Issues are prioritized by business impact.
- [ ] Authentication, permission, missing logs, and query timeout limitations are reported when present.

## Prompt Body

Follow these steps in order.

**Step 1 — Get Azure best practices.**
Retrieve diagnostic and troubleshooting best practices with the Azure MCP best practices tool. Focus on health monitoring, log analysis, issue resolution patterns, and remediation recommendations.

**Step 2 — Discover and identify the resource.**
If only a resource name is provided, search across subscriptions using `azmcp-subscription-list`. Use `az resource list --name <resource-name>` as Azure CLI fallback to find matching resources. If multiple matches are found, prompt the user to specify `subscription/resource group`. Gather resource type, current status, location, tags, configuration, associated services, and dependencies.

**Step 3 — Detect resource type.**
Choose the diagnostic path by resource type: Web Apps and Function Apps use application logs, performance metrics, and dependency tracking; Virtual Machines use system logs, performance counters, and boot diagnostics; Cosmos DB uses request metrics, throttling, and partition statistics; Storage Accounts use access logs, performance metrics, and availability; SQL Database uses query performance, connection logs, and resource utilization; Application Insights uses application telemetry, exceptions, and dependencies; Key Vault uses access logs, certificate status, and secret usage; Service Bus uses message metrics, dead letter queues, and throughput.

**Step 4 — Assess basic health.**
Check provisioning state and operational status. Verify service availability and responsiveness. Review recent deployment or configuration changes. Assess current resource utilization such as CPU, memory, and storage.

**Step 5 — Assess service-specific health indicators.**
For Web Apps, inspect HTTP response codes, response times, and uptime. For databases, inspect connection success rate, query performance, and deadlocks. For storage, inspect availability percentage, request success rate, and latency. For VMs, inspect boot diagnostics, guest OS metrics, and network connectivity. For Functions, inspect execution success rate, duration, and error frequency.

**Step 6 — Find monitoring sources.**
Use `azmcp-monitor-workspace-list` to identify Log Analytics workspaces. Locate Application Insights instances associated with the resource. Use `azmcp-monitor-table-list` to identify relevant log tables.

**Step 7 — Execute diagnostic KQL queries.**
Use `azmcp-monitor-log-query` with targeted KQL based on resource type. Start with recent errors and exceptions:

```kql
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

Check performance degradation patterns:

```kql
Perf
| where TimeGenerated > ago(7d)
| where ObjectName == "Processor" and CounterName == "% Processor Time"
| summarize avg(CounterValue) by Computer, bin(TimeGenerated, 1h)
| where avg_CounterValue > 80
```

For Application Insights failed requests:

```kql
requests
| where timestamp > ago(24h)
| where success == false
| summarize FailureCount=count() by resultCode, bin(timestamp, 1h)
| order by timestamp desc
```

For SQL Database connection failures:

```kql
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.SQL"
| where Category == "SQLSecurityAuditEvents"
| where action_name_s == "CONNECTION_FAILED"
| summarize ConnectionFailures=count() by bin(TimeGenerated, 1h)
```

**Step 8 — Recognize patterns and correlate events.**
Identify recurring error patterns or anomalies. Correlate errors with deployment times or configuration changes. Analyze performance trends and degradation patterns. Look for dependency failures or external service issues.

**Step 9 — Classify issues and root causes.**
Classify severity as Critical for service unavailable, data loss, or security breaches; High for performance degradation, intermittent failures, or high error rates; Medium for warnings, suboptimal configuration, or minor performance issues; Low for informational alerts or optimization opportunities. Classify root causes as configuration issues, resource constraints, network issues, application issues, external dependencies, or security issues such as authentication failures and certificate expiration.

**Step 10 — Assess impact.**
Determine business impact and affected `users/systems`. Evaluate data integrity and security implications. Assess recovery time objectives and priorities.

**Step 11 — Generate remediation phases.**
For immediate actions, include emergency fixes to restore service availability, temporary workarounds to mitigate impact, and escalation procedures for complex issues. For short-term fixes, include configuration adjustments, resource scaling, application updates, patches, and monitoring or alerting improvements. For long-term improvements, include architectural changes for resilience, preventive measures, monitoring enhancements, documentation, and process improvements. Include implementation steps with Azure CLI commands, testing, validation, rollback plans, and monitoring to verify resolution.

**Step 12 — Handle errors and limitations.**
For Resource Not Found, provide guidance on resource `name/location` specification. For Authentication Issues, guide Azure authentication setup. For Insufficient Permissions, list required RBAC roles. For No Logs Available, suggest enabling diagnostic settings and waiting for data. For Query Timeouts, break analysis into smaller time windows. For Service-Specific Issues with limited telemetry, provide a generic health assessment and state limitations.

## Invocation Example

```
/azure-resource-health-diagnose resource=/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/app-rg/providers/Microsoft.Web/sites/app-service
```
