---
name: az-cost-optimize
description: >-
  Analyze Azure IaC files and deployed Azure resources for evidence-based cost optimization, validate current costs, calculate priority scores, and draft GitHub issues. Use when asked to "azure cost optimize", "reduce Azure spend", "find Azure cost savings", "right-size Azure resources", or "create cost optimization issues".
---

# Azure cost optimize

Analyze Azure Infrastructure-as-Code and deployed resources, transform usage and pricing evidence into prioritized cost recommendations, and output issue-ready optimization work items plus an EPIC coordination issue.

## When to invoke

- "Azure cost optimize this app."
- "Find Azure cost savings and create GitHub issues."
- "Right-size our App Service, Cosmos DB, SQL, Redis, and storage resources."
- "Review IaC for Azure cost optimization opportunities."
- "Create an EPIC for Azure monthly savings work."

## Prerequisites and context

Analyze IaC files and/or resources in a target resource group; do not broaden repository scope beyond IaC.


- Azure MCP server should be configured and authenticated; prefer Azure MCP tools such as `azmcp-*` over Azure CLI when available.
- GitHub MCP server or `gh` CLI should be authenticated when creating issues.
- Target GitHub repository and target subscription/resource group must be known or discoverable.
- Azure resources must exist; IaC files are optional for discovery but required as the source of truth for implementation recommendations.
- Do not read arbitrary application source. Only IaC files are valid repository evidence: `**/*.bicep`, `**/*.tf`, `**/main.json`, and `**/*template*.json`.
- If no IaC files are found, stop and report that no IaC files were found.

## Azure discovery and evidence

| Evidence | Preferred command or tool | Purpose |
| --- | --- | --- |
| Best practices | `azmcp-bestpractices-get` | Retrieve current Azure optimization guidance before analysis. |
| Subscriptions | `azmcp-subscription-list` | Identify available subscriptions. |
| Resource groups | `azmcp-group-list --subscription <subscription-id>` | Locate candidate groups. |
| All resources | `az resource list --subscription <id> --resource-group <name>` | Build the resource inventory. |
| Cosmos DB | `azmcp-cosmos-account-list --subscription <id>` | Find accounts and throughput settings. |
| Storage | `azmcp-storage-account-list --subscription <id>` | Review tiering and lifecycle candidates. |
| Log Analytics | `azmcp-monitor-workspace-list --subscription <id>` | Find monitoring sources. |
| Key Vault | `azmcp-keyvault-key-list` | Inventory key vault resources when no richer MCP resource tool exists. |
| Web Apps | `az webapp list` | CLI fallback when no MCP tool is available. |
| App Service Plans | `az appservice plan list` | Identify plan SKU and scale candidates. |
| Function Apps | `az functionapp list` | Detect Premium to Consumption opportunities. |
| SQL Servers | `az sql server list` | Locate SQL Database estates for tier review. |
| Redis Cache | `az redis list` | Locate cache SKU and sizing candidates. |

Use IaC parsing to compare intended configuration with deployed resources. Extract SKUs, tiers, capacity, autoscale settings, retention settings, backup settings, and deployment paths before making recommendations.

## Usage metrics and current cost validation

Use `azmcp-monitor-workspace-list --subscription <id>` and `azmcp-monitor-table-list --subscription <id> --workspace <name> --table-type "CustomLog"` to find telemetry. Use `azmcp-monitor-log-query` for predefined `recent` and `errors` queries, then run targeted KQL when tables exist:

```kql
// CPU utilization for App Services
AppServiceAppLogs
| where TimeGenerated > ago(7d)
| summarize avg(CpuTime) by Resource, bin(TimeGenerated, 1h)

// Cosmos DB RU consumption
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.DOCUMENTDB"
| where TimeGenerated > ago(7d)
| summarize avg(RequestCharge) by Resource

// Storage account access patterns
StorageBlobLogs
| where TimeGenerated > ago(7d)
| summarize RequestCount=count() by AccountName, bin(TimeGenerated, 1d)
```

Calculate CPU and memory utilization averages, database throughput patterns, storage access frequency, and Function execution rates. Validate current monthly cost before recommendations by mapping `Resource -> Current SKU -> Estimated monthly cost`; use https://azure.microsoft.com/en-us/pricing/ or `az billing` commands as the pricing source.

## Optimization patterns

Preserve strict cost terminology during analysis: Step 3 must **VALIDATE CURRENT COSTS** before recommendations; if estimates look wrong, **re-verify** pricing. Record `CPU/Memory` and `CPU/memory` evidence, each `SKU/tier`, any `error-level` logs, and whether savings are `X/month`, `Y/month`, or `Z/month`. If no IaC files are present, `STOP`. Issues may be created with `create_issue` after approval. Include `auto-scaling` and `unused/redundant` resource checks.


| Resource type | Cost pattern | Evidence required | Implementation hint |
| --- | --- | --- | --- |
| App Service Plans | Right-size SKU when CPU and memory are consistently low. | Plan SKU, utilization, scaling settings. | Patch Bicep/Terraform first; use `az appservice plan update --name <plan> --sku <sku>` only when no IaC exists. |
| Function Apps | Move Premium to Consumption for low or bursty workloads. | Execution count, cold-start tolerance, VNet and always-on needs. | Confirm feature compatibility before changing plan. |
| Virtual Machines | Scale down oversized instances or schedule non-production shutdown. | CPU, memory, disk, business hours. | Document expected downtime and rollback. |
| Cosmos DB | Move provisioned to serverless or right-size RU/s. | `RequestCharge`, provisioned RU/s, peak windows. | Preserve availability and consistency requirements. |
| SQL Database | Right-size service tier based on DTU/vCore usage. | DTU/vCore utilization, storage, HA needs. | Test non-production and monitor latency. |
| Storage | Apply Hot -> Cool -> Archive lifecycle policies. | Access patterns from `StorageBlobLogs`. | Use lifecycle management through IaC. |
| Redundant resources | Remove unused or duplicate resources. | No usage, no dependencies, owner confirmation. | Open a removal issue; require explicit approval. |
| Non-production environments | Schedule shutdown or autoscale. | Environment tags and working hours. | Avoid production and shared resources. |

Compute priority for each recommendation:

```text
Priority Score = (Value Score × Monthly Savings) / (Risk Score × Implementation Days)
High Priority: Score > 20
Medium Priority: Score 5-20
Low Priority: Score < 5
```

Every savings estimate must show current validated cost, target cost, monthly savings, pricing source, implementation risk, and prerequisites.

## Procedure

1. Run `azmcp-bestpractices-get` and keep cited best-practice evidence with the analysis.
2. Discover subscriptions, resource groups, and resources with MCP tools first and Azure CLI fallback second.
3. Search only IaC files: `**/*.bicep`, `**/*.tf`, `**/main.json`, `**/*template*.json`; stop if none are found.
4. Extract deployed and intended SKUs, tiers, relationships, usage metrics, and current estimated monthly cost.
5. Apply the optimization patterns and calculate validated monthly savings and priority scores.
6. Present a summary before issue creation. In interactive contexts, wait for user approval; in non-interactive contexts, output issue-ready markdown and do not create issues.
7. Create individual issues labeled `cost-optimization` and `azure` only after approval.
8. Create one EPIC issue labeled `cost-optimization`, `azure`, and `epic` after individual issues exist.

## Issue templates

Individual issue title:

```text
[COST-OPT] [Resource Type] - [Brief Description] - $X/month savings
```

Individual issue body:

```markdown
## Cost Optimization: [Brief Title]

**Monthly Savings**: $X | **Risk Level**: [Low/Medium/High] | **Implementation Effort**: X days

### Description
[Clear explanation of the optimization and why it's needed]

### Implementation

**IaC Files Detected**: [Yes/No - based on file_search results]

```bash
# If IaC files found: show IaC modifications and deployment
# File: infrastructure/bicep/modules/app-service.bicep
# Change: sku.name: 'S3' -> 'B2'
az deployment group create --resource-group [rg] --template-file infrastructure/bicep/main.bicep

# If no IaC files: direct Azure CLI commands plus warning
# No IaC files found. If they exist elsewhere, modify those instead.
az appservice plan update --name [plan] --sku B2
```

### Evidence
- Current Configuration: [details]
- Usage Pattern: [evidence from monitoring data]
- Cost Impact: $X/month -> $Y/month
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

EPIC issue title:

```text
[EPIC] Azure Cost Optimization Initiative - $X/month potential savings
```

EPIC issue body:

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

Verify Mermaid syntax and use accessible labels and colors if styling is added.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| Savings estimate lacks evidence | Pricing source, SKU, or usage metric is missing. | Re-verify configuration and pricing before recommending. |
| Azure authentication fails | MCP or CLI profile is not authenticated. | Provide manual Azure CLI setup steps and stop resource discovery. |
| No resources found | Wrong subscription/resource group or no deployment. | Create an informational issue only if approved. |
| GitHub issue creation fails | Missing GitHub auth or repository target. | Output the formatted recommendations to console. |
| Usage data is insufficient | Monitoring tables are absent or retention is too short. | Mark recommendations as configuration-based only. |

## Output template

```markdown
## Azure cost optimization summary

**Status:** ready for approval | issues created | blocked
**Resources analyzed:** <count>
**Current monthly cost:** $<amount>
**Potential monthly savings:** $<amount>
**Optimization opportunities:** <count>
**High priority items:** <count>

| Resource | Current SKU/config | Target SKU/config | Monthly savings | Risk | Effort | Priority score | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <name> | <current> | <target> | $<amount> | Low/Medium/High | <days> | <score> | <pricing and usage source> |

**Issues**
- Individual issues: <created count or issue-ready markdown>
- EPIC issue: <created issue or issue-ready markdown>

**Validation**
- IaC scan: <patterns scanned and result>
- Cost validation: <pricing source>
- User confirmation: <approved/not requested/non-interactive>
```

## Quality gate

- [ ] `azmcp-bestpractices-get` was used or an unavailable-tool limitation was reported.
- [ ] Only IaC files were read from the repository: `**/*.bicep`, `**/*.tf`, `**/main.json`, `**/*template*.json`.
- [ ] If no IaC files were found, the workflow stopped and reported that result.
- [ ] Every current cost maps a resource to a SKU and a pricing source.
- [ ] Every recommendation includes current cost, target cost, monthly savings, risk, effort, and priority score.
- [ ] Azure CLI commands are executable and use placeholders only where values are unknown.
- [ ] GitHub issues are created only after approval; otherwise issue-ready markdown is returned.
- [ ] The EPIC references individual issue numbers when issues were actually created.
