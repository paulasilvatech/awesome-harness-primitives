# Azure & Cloud Development Plugin

Comprehensive Azure cloud development tools including Infrastructure as Code, serverless functions, architecture patterns, and cost optimization for building scalable cloud applications.

## Installation

```bash
# Using Copilot CLI
copilot plugin install azure-cloud-development@awesome-copilot
```

## What's Included

### Commands (Slash Commands)

| Command | Description |
|---------|-------------|
| `/azure-cloud-development:az-cost-optimize` | Analyze Azure IaC files and deployed Azure resources for evidence-based cost optimization, validate current costs, calculate priority scores, and draft GitHub issues. |
| `/azure-cloud-development:azure-cli` | Azure CLI operations run az commands for cloud resource discovery, subscription context, identity, AKS, ACR, Key Vault, RBAC, managed identity, and federated credential workflows. |
| `/azure-cloud-development:azure-compute` | Route Azure virtual machine and scale set work, including size and image selection, pricing comparison, autoscale and orchestration modes, capacity reservation groups, and Essential Machine Management. |
| `/azure-cloud-development:azure-enterprise-infra-planner` | Architect and provision enterprise Azure infrastructure from workload descriptions for cloud architects and platform engineers, covering networking, identity, security, compliance, and multi-resource topologies with Well-Architected alignment, and generating Bicep or Terraform directly without azd. |
| `/azure-cloud-development:azure-infrastructure` | Azure infrastructure patterns guide landing-zone, networking, identity, naming, tagging, and private connectivity decisions. |
| `/azure-cloud-development:azure-pricing` | Fetch live Azure Retail Prices API data and estimate Azure service, SKU, region, reservation, savings plan, spot, and Copilot Studio credit costs. |
| `/azure-cloud-development:azure-resource-health-diagnose` | Analyze Azure resource health, logs, metrics, and telemetry to diagnose operational issues and produce a prioritized remediation plan. |
| `/azure-cloud-development:azure-resource-lookup` | List, find, and show Azure resources across subscriptions or resource groups using Azure Resource Graph queries. |
| `/azure-cloud-development:azure-resource-visualizer` | Analyze Azure resource groups and generate Mermaid architecture diagrams and markdown documentation for their resources and relationships. |
| `/azure-cloud-development:azure-terraform-cli` | Terraform CLI operations manage Azure infrastructure as code through Terraform formatting, validation, initialization, planning, apply workflows, destroy workflows, state inspection, import workflows, module development, provider lock files, tfvars, and security scanning. |
| `/azure-cloud-development:azure-terraform-terratest-module-testing` | Creates, repairs, and runs scoped Terratest coverage for Open Horizons Terraform modules under tests/terraform. |
| `/azure-cloud-development:import-infrastructure-as-code` | Import existing Azure resources into Terraform with Azure CLI discovery, dependency mapping, Azure Verified Modules, exact import addresses, and drift-safe plans. |

### Agents

| Agent | Description |
|-------|-------------|
| `azure-principal-architect` | Provide expert Azure Principal Architect guidance using Azure Well-Architected Framework principles and Microsoft best practices. |
| `azure-saas-architect` | Provide expert Azure SaaS Architect guidance focusing on multitenant applications using Azure Well-Architected SaaS principles and Microsoft best practices. |
| `azure-logic-apps-expert` | Expert guidance for Azure Logic Apps development focusing on workflow design, integration patterns, and JSON-based Workflow Definition Language. |
| `azure-verified-modules-bicep` | Create, update, or review Azure IaC in Bicep using Azure Verified Modules (AVM). |
| `azure-verified-modules-terraform` | Create, update, or review Azure IaC in Terraform using Azure Verified Modules (AVM). |
| `terraform-azure-planning` | Act as implementation planner for your Azure Terraform Infrastructure as Code task. |
| `terraform-azure-implement` | Act as an Azure Terraform Infrastructure as Code coding specialist that creates and reviews Terraform for Azure resources. |

## Source

This plugin is part of [Awesome Copilot](https://github.com/github/awesome-copilot), a community-driven collection of GitHub Copilot extensions.

## License

MIT
