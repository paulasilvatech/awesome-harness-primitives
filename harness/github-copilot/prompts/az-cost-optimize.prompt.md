---
name: 'az-cost-optimize'
description: 'Analyze Azure application resources and produce cost optimization issues or recommendations.'
agent: 'agent'
tools: ['read', 'search', 'azure-mcp/*', 'github/*']
argument-hint: 'repository=<owner/repo> subscription=<optional> resource-group=<optional>'
---

# /az-cost-optimize

## Objective

Analyze Azure Infrastructure-as-Code files and deployed Azure resources, validate current monthly costs, identify evidence-based cost optimization opportunities, and produce GitHub issues plus one EPIC issue to coordinate implementation and savings tracking.

## When to Invoke

Use this prompt when Azure resources are deployed and the team wants trackable cost optimization recommendations backed by Azure configuration, usage metrics, pricing evidence, and implementation guidance.

## Preconditions

- Azure MCP server is configured and authenticated.
- GitHub MCP server is configured and authenticated.
- Target GitHub repository is identified.
- Azure resources are deployed; IaC files are optional but helpful.
- Prefer Azure MCP tools (`azmcp-*`) over direct Azure CLI when available.
- The user can approve GitHub issue creation before any issue is created.

## Inputs the Team Must Provide

- `repository` — GitHub repository where optimization issues and the EPIC should be created.
- Optional `subscription` and `resource-group` to constrain Azure discovery.
- Any known environment, application name, cost concern, or budget target.
- Permission to inspect Azure resources, metrics, costs, and IaC files.
- Ask the user for anything that is missing, especially repository identity or ambiguous Azure scope.

## What I Will Do

- Run `azmcp-bestpractices-get` to retrieve Azure optimization best practices and cite applicable guidance.
- Discover subscriptions, resource groups, resources, SKUs, tiers, settings, relationships, and dependencies.
- Scan only IaC files using `search` patterns: `**/*.bicep`, `**/*.tf`, `**/main.json`, and `**/*template*.json`.
- Stop and report no IaC files found if the IaC scan finds none.
- Use Azure MCP tools first and Azure CLI fallbacks where MCP coverage is unavailable.
- Collect usage metrics from Log Analytics and monitoring data.
- Validate current costs from discovered SKU and tier configurations using https://azure.microsoft.com/pricing/ or `az billing` commands.
- Calculate evidence-based savings and priority scores.
- Present a summary and wait for user confirmation before creating issues.
- Create one issue per optimization and one EPIC coordinating issue when approved.

## What I Will NOT Do

- Use repository files other than IaC files as a source of truth.
- Create GitHub issues before the user confirms.
- Recommend savings without current cost, target cost, pricing source, and supporting evidence.
- Treat the Azure best practices MCP output as exhaustive.
- Apply direct Azure changes, delete resources, or alter IaC files during this workflow.
- Ignore implementation risks, prerequisites, validation, or rollback planning.
- Generate a mermaid diagram without checking syntax and accessibility-oriented styling.

## Output Format

Return the summary and issue bodies in this format:

````markdown
## Azure Cost Optimization Summary

Analysis Results:
• Total Resources Analyzed: X
• Current Monthly Cost: $X
• Potential Monthly Savings: $Y
• Optimization Opportunities: Z
• High Priority Items: N

Recommendations:
1. [Resource]: [Current SKU] → [Target SKU] = $X/month savings - [Risk Level] | [Implementation Effort]
2. [Resource]: [Current Config] → [Target Config] = $Y/month savings - [Risk Level] | [Implementation Effort]
3. [Resource]: [Current Config] → [Target Config] = $Z/month savings - [Risk Level] | [Implementation Effort]

This will create:
• Y individual GitHub issues (one per optimization)
• 1 EPIC issue to coordinate implementation

Proceed with creating GitHub issues? (y/n)

## Individual Issue Template

**Title**: `[COST-OPT] [Resource Type] - [Brief Description] - $X/month savings`

```markdown
## Cost Optimization: [Brief Title]

**Monthly Savings**: $X | **Risk Level**: [Low/Medium/High] | **Implementation Effort**: X days

### Description
[Clear explanation of the optimization and why it's needed]

### Implementation

**IaC Files Detected**: [Yes/No - based on file_search results]

```bash
# If IaC files found: Show IaC modifications + deployment
# File: infrastructure/bicep/modules/app-service.bicep
# Change: sku.name: 'S3' → 'B2'
az deployment group create --resource-group [rg] --template-file infrastructure/bicep/main.bicep

# If no IaC files: Direct Azure CLI commands + warning
# No IaC files found. If they exist elsewhere, modify those instead.
az appservice plan update --name [plan] --sku B2
```

### Evidence
- Current Configuration: [details]
- Usage Pattern: [evidence from monitoring data]
- Cost Impact: $X/month → $Y/month
- Best Practice Alignment: [reference to Azure best practices if applicable]

### Validation Steps
- [ ] Test in non-production environment
- [ ] Verify no performance degradation
- [ ] Confirm cost reduction in Azure Cost Management
- [ ] Update monitoring and alerts if needed

### Risks & Considerations
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

**Priority Score**: X | **Value**: X/10 | **Risk**: X/10
```

## EPIC Issue Template

**Title**: `[EPIC] Azure Cost Optimization Initiative - $X/month potential savings`

```markdown
# Azure Cost Optimization EPIC

**Total Potential Savings**: $X/month | **Implementation Timeline**: X weeks

## Executive Summary
- **Resources Analyzed**: X
- **Optimization Opportunities**: Y
- **Total Monthly Savings Potential**: $X
- **High Priority Items**: N

## Current Architecture Overview

```mermaid
graph TB
    subgraph "Resource Group: [name]"
        [Generated architecture diagram showing current resources and costs]
    end
```

## Implementation Tracking

### High Priority (Implement First)
- [ ] #[issue-number]: [Title] - $X/month savings

### Medium Priority
- [ ] #[issue-number]: [Title] - $X/month savings

### Low Priority (Nice to Have)
- [ ] #[issue-number]: [Title] - $X/month savings

## Progress Tracking
- **Completed**: 0 of Y optimizations
- **Savings Realized**: $0 of $X/month
- **Implementation Status**: Not Started

## Success Criteria
- [ ] All high-priority optimizations implemented
- [ ] >80% of estimated savings realized
- [ ] No performance degradation observed
- [ ] Cost monitoring dashboard updated

## Notes
- Review and update this EPIC as issues are completed
- Monitor actual vs. estimated savings
- Consider scheduling regular cost optimization reviews
```
````

## Definition of Done

- [ ] Azure best practices were retrieved and considered.
- [ ] Azure resources, SKUs, tiers, and settings were discovered with MCP tools or documented CLI fallback.
- [ ] IaC scan used only `**/*.bicep`, `**/*.tf`, `**/main.json`, and `**/*template*.json`.
- [ ] Current monthly cost is validated against resource configurations and Azure pricing.
- [ ] Every recommendation includes current cost, target cost, monthly savings, evidence, risk, effort, and priority score.
- [ ] User confirmation is obtained before GitHub issue creation.
- [ ] Individual issues are created for each optimization and labeled `cost-optimization` and `azure`.
- [ ] The EPIC is labeled `cost-optimization`, `azure`, and `epic`, and includes an accessible mermaid architecture diagram.

## Prompt Body

Follow these steps in order.

**Step 1 — Get Azure best practices.**
Execute `azmcp-bestpractices-get` to get some of the latest Azure optimization guidelines. Treat the output as a foundation, not complete coverage. Reference best practices in recommendations from MCP output or general Azure documentation.

**Step 2 — Discover Azure infrastructure.**
Execute `azmcp-subscription-list` to find available subscriptions. Execute `azmcp-group-list --subscription <subscription-id>` to find resource groups. List all resources in relevant groups with `az resource list --subscription <id> --resource-group <name>`. For each resource type, use MCP tools first when possible, then CLI fallback: `azmcp-cosmos-account-list --subscription <id>` for Cosmos DB accounts, `azmcp-storage-account-list --subscription <id>` for Storage accounts, `azmcp-monitor-workspace-list --subscription <id>` for Log Analytics workspaces, `azmcp-keyvault-key-list` for Key Vaults, `az webapp list` for Web Apps, `az appservice plan list` for App Service Plans, `az functionapp list` for Function Apps, `az sql server list` for SQL Servers, and `az redis list` for Redis Cache.

**Step 3 — Detect IaC files only.**
Use `search` for `**/*.bicep`, `**/*.tf`, `**/main.json`, and `**/*template*.json`. Parse resource definitions to understand intended configurations. Compare against discovered resources to identify discrepancies. Note IaC presence for implementation recommendations later on. Do not use any other repository files; they are not a source of truth. If no IaC files are found, stop and report no IaC files found to the user.

**Step 4 — Analyze configuration.**
Extract current SKUs, tiers, and settings for each resource. Identify relationships and dependencies. Map utilization patterns where available.

**Step 5 — Collect usage metrics.**
Use `azmcp-monitor-workspace-list --subscription <id>` to find Log Analytics workspaces. Use `azmcp-monitor-table-list --subscription <id> --workspace <name> --table-type "CustomLog"` to discover data. Use `azmcp-monitor-log-query` with predefined Query: `recent` for recent activity patterns and Query: `errors` for error-level logs indicating issues.

Run KQL for custom analysis when available:

```kql
AppServiceAppLogs
| where TimeGenerated > ago(7d)
| summarize avg(CpuTime) by Resource, bin(TimeGenerated, 1h)
```

```kql
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.DOCUMENTDB"
| where TimeGenerated > ago(7d)
| summarize avg(RequestCharge) by Resource
```

```kql
StorageBlobLogs
| where TimeGenerated > ago(7d)
| summarize RequestCount=count() by AccountName, bin(TimeGenerated, 1d)
```

Calculate CPU and memory utilization averages, database throughput patterns, storage access frequency, and function execution rates.

**Step 6 — Validate current costs.**
Using SKU and tier configurations from discovery, look up current Azure pricing at https://azure.microsoft.com/pricing/ or use `az billing` commands. Document `Resource → Current SKU → Estimated monthly cost`. Calculate a realistic current monthly total before recommendations.

**Step 7 — Generate optimization recommendations.**
Apply resource-specific patterns. Compute optimizations: right-size App Service Plans based on CPU and memory usage, move Function Apps from Premium to Consumption plan for low usage, and scale down oversized Virtual Machines. Database optimizations: for Cosmos DB, consider Provisioned to Serverless for variable workloads and right-size RU/s based on actual usage; for SQL Database, right-size service tiers based on DTU usage. Storage optimizations: implement lifecycle policies Hot → Cool → Archive, consolidate redundant storage accounts, and right-size storage tiers based on access patterns. Infrastructure optimizations: remove `unused/redundant` resources, implement auto-scaling where beneficial, and schedule non-production environments.

**Step 8 — Calculate evidence-based savings and priority.**
Use `Current validated cost → Target cost = Savings`. Document pricing sources for current and target configurations. Calculate priority with `Priority Score = (Value Score × Monthly Savings) / (Risk Score × Implementation Days)`. Classify High Priority when score is `> 20`, Medium Priority when score is `5-20`, and Low Priority when score is `< 5`.

**Step 9 — Validate recommendations.**
Ensure Azure CLI commands are accurate, savings calculations are verified, implementation risks and prerequisites are assessed, and every savings calculation has supporting evidence.

**Step 10 — Request user confirmation.**
Display the Azure Cost Optimization Summary with total resources analyzed, current monthly cost, potential monthly savings, optimization opportunities, high priority items, top recommendations, number of individual issues, and one EPIC. Wait for user confirmation and proceed only if the user confirms.

**Step 11 — Create individual optimization issues.**
Create a separate GitHub issue for each optimization opportunity using `create_issue`. Label each issue `cost-optimization` with green color and `azure` with blue color. Use title format `[COST-OPT] [Resource Type] - [Brief Description] - $X/month savings`. Include IaC detection, implementation commands, evidence, validation steps, risks, considerations, `Priority Score`, `Value`, and `Risk`.

**Step 12 — Create the EPIC coordinating issue.**
Create a master issue with `create_issue`. Label it `cost-optimization` with green color, `azure` with blue color, and `epic` with purple color. Use title `[EPIC] Azure Cost Optimization Initiative - $X/month potential savings`. Include total savings, timeline, executive summary, current architecture overview, implementation tracking by priority, progress tracking, success criteria, and notes. Verify mermaid syntax and use accessible styling, colors, and labels.

**Step 13 — Handle failures.**
If cost validation lacks evidence or seems inconsistent with Azure pricing, re-verify configurations and pricing sources. For Azure Authentication Failure, provide manual Azure CLI setup steps. For No Resources Found, create an informational issue about Azure resource deployment only when issue creation is approved. For GitHub Creation Failure, output formatted recommendations to console. For Insufficient Usage Data, state limitations and provide configuration-based recommendations only.

## Invocation Example

```
/az-cost-optimize repository=owner/repo subscription=00000000-0000-0000-0000-000000000000 resource-group=app-rg
```
