---
name: "az-cost-optimize"
description: "Analyze Azure resources and Terraform IaC for cost savings and open tracking GitHub issues, deferring the workflow to the az-cost-optimize skill."
argument-hint: "rg=<resource-group> repo=<owner/name>"
agent: "devops-engineer"
tools: ["read", "search", "execute"]
---
# /az-cost-optimize

## Objective

Analyze deployed Azure resources and their Terraform IaC, produce evidence-based cost-optimization recommendations, and open one GitHub issue per opportunity plus a coordinating EPIC. The full workflow lives in the [`az-cost-optimize`](../skills/az-cost-optimize/SKILL.md) skill; this prompt applies it to the SIFAP 2.0 kit without restating it.

> [!IMPORTANT]
> The kit's IaC is Terraform only. Treat the skill's Bicep/ARM references as out of scope, and never open an issue on a saving you cannot back with validated pricing.

## When to Invoke

During Stage 4 (Evolution), once the team has provisioned Azure resources and wants to track cost reductions as GitHub issues.

## Preconditions

- The team is authenticated to Azure and to the target GitHub repository
- Terraform for the modern system exists under `infra/` (created by the team in Stage 3/4)
- The target resource group and subscription are known

## Inputs the Team Must Provide

- `rg` — the target Azure resource group
- `repo` — the `owner/name` of the GitHub repository for the issues
- Ask the user for anything that is missing.

## What I Will Do

- Follow the discovery, metrics, and recommendation workflow in the [`az-cost-optimize`](../skills/az-cost-optimize/SKILL.md) skill
- Read only the Terraform under `infra/` as the IaC source of truth
- Validate each current cost and target cost against Azure pricing before recommending
- Open one GitHub issue per optimization plus an EPIC, using the `gh` CLI

## What I Will NOT Do

- Parse Bicep or ARM templates — out of scope for this kit
- Invent resources or savings when no Terraform exists (I report and stop)
- Open issues before the team confirms the summary
- Recommend a change without validated evidence and a rollback consideration

## Output Format

```markdown
### Summary
Resources analyzed: 7 · Current: $X/mo · Potential savings: $Y/mo · Opportunities: 4

### Issues to create
- [COST-OPT] App Service plan S3 → B2 — $X/mo (Low risk)
- [EPIC] Azure Cost Optimization — $Y/mo potential
```

## Definition of Done

- [ ] Every saving is validated against the resource's SKU/tier and Azure pricing
- [ ] Recommendations reference the Terraform under `infra/`, not Bicep/ARM
- [ ] One issue per opportunity plus an EPIC are created via `gh` after confirmation
- [ ] Each issue carries evidence, risk, and validation steps

## Prompt Body

The [`az-cost-optimize`](../skills/az-cost-optimize/SKILL.md) skill owns the discovery, metrics, scoring, and issue-templating procedure — read it, then apply it to the target resource group.

**Step 1 — Discover.**
Enumerate resources in `rg` and read the Terraform under `infra/` as the intended configuration.

**Step 2 — Apply the skill.**
Collect usage metrics, validate current costs, and generate scored recommendations per the skill.

**Step 3 — Respect the kit rules.**
Ignore Bicep/ARM; if no Terraform exists, report that and stop. Keep GitHub as the source of truth.

**Step 4 — Confirm, then create.**
Present the summary, wait for approval, and open the issues and EPIC with `gh`.

## Invocation Example

```
/az-cost-optimize rg=sifap-prod-rg repo=my-org/sifap-2
```
