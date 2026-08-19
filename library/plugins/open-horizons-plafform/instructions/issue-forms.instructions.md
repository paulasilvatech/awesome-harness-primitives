---
applyTo: ".github/ISSUE_TEMPLATE/*.yml"
description: "Use when editing GitHub Issue Forms for Open Horizons agent routing, IssueOps metadata, and safe request intake."
---

# Issue Form Conventions — Agent Routing and Safe Intake

This file activates when you edit YAML issue forms under `.github/ISSUE_TEMPLATE/`. It teaches how Open Horizons collects structured deployment, infrastructure, security, SRE, and portal requests for Agent Router and IssueOps. It does **not** cover workflow implementation, which belongs to the `github-actions` instructions, agent and prompt schemas, which belong to the `agent-files` instructions, shell automation invoked by IssueOps, which belongs to the `shell` instructions, or Terraform and Kubernetes implementation details, which belong to the `terraform` instructions and the `kubernetes` instructions.


## Authoritative Sources and Precedence

Follow these sources in order:

1. Repository files matched by `applyTo: ".github/ISSUE_TEMPLATE/*.yml"` for existing local patterns.
2. This `issue-forms` instruction file for passive conventions, boundaries, and examples.
3. Official upstream documentation only when it is consistent with repository conventions.

When sources conflict, the higher-priority source wins. Do not duplicate or weaken rules owned by another primitive.

## Responsibility Split

This file owns passive conventions for issue form conventions — agent routing and safe intake. Use the `issue-ops` skill for ordered procedures, command sequences, setup, validation, or troubleshooting that goes beyond these rules.

> [!IMPORTANT]
> Issue forms are public intake surfaces in many repositories. Never ask users to paste secrets, tokens, passwords, private keys, kubeconfigs, or connection strings.

## Routing Metadata

Use labels that the Agent Router and workflows understand: `agent:<id>` labels match `.github/agents/*.agent.md`, while `workflow:<name>` labels map to workflow automation.

```yaml
# Wrong: free-form labels cannot be routed reliably.
labels: ["please deploy", "AI"]
```

```yaml
labels: ["deployment", "agent:deploy", "workflow:full-deployment"]
```

## Required Fields

Ask for machine-readable environment, horizon, region, platform, and approval inputs when the operation depends on them. Keep options canonical so agents do not need fuzzy parsing.

```yaml
# Wrong: free-form production intent with no validation.
- type: input
  id: environment
  attributes:
    label: Environment
```

```yaml
- type: dropdown
  id: environment
  attributes:
    label: Environment
    description: Target deployment environment
    options:
      - dev
      - staging
      - prod
  validations:
    required: true
```

> [!NOTE]
> Use text areas for narrative requirements, but keep routing-critical fields as dropdowns, checkboxes, or required inputs.

## Safe Placeholders

Placeholders should show format, not real customer values or secrets.

```yaml
# Wrong: placeholder resembles a real credential.
placeholder: "ghp_exampletoken1234567890"
```

```yaml
placeholder: "e.g., my-company"
```

## Cost and Risk Language

If a form includes cost bands, risk levels, or production approvals, make them explicit and objective. The deployment request form uses T-shirt sizing and approver fields for staged environments.

```yaml
# Wrong: unclear risk signal for an agent.
description: "Is this big?"
```

```yaml
description: "List GitHub handles of approvers (required for staging/prod)"
```

> [!WARNING]
> Do not auto-trigger destructive or production operations from a form without an explicit approval, environment, and workflow label gate.

## Core Conventions

| Rule | Rationale |
|---|---|
| Use canonical `agent:<id>` labels | Agent Router can dispatch to the right deploy-managed assistant. |
| Use canonical `workflow:<name>` labels only when a workflow supports them | IssueOps should not infer nonexistent automation. |
| Prefer dropdowns and checkboxes for environment, horizon, and feature choices | Structured values reduce ambiguous agent interpretation. |
| Keep placeholders synthetic and non-sensitive | Forms should educate without leaking examples that look real. |
| Make production and staging approval fields visible | Higher-risk environments require explicit human context. |
| Keep body IDs stable | Downstream workflows parse `id` values from issue payloads. |

## Do / Do Not

| Do | Do not |
|---|---|
| Ask for GitHub org names, Azure regions, and target environments | Ask for PATs, passwords, or private keys. |
| Use required validations for fields needed by automation | Make agents infer required deployment inputs from prose. |
| Keep issue titles machine-scannable, such as `[DEPLOY]` | Use ambiguous titles that hide request type. |
| Link related guides in markdown blocks when needed | Paste long operational runbooks into every form. |

## Verification Checklist

- [ ] Labels use canonical `agent:<id>` and supported `workflow:<name>` values.
- [ ] Required fields cover routing, environment, scope, and approval needs.
- [ ] No field requests or examples include secrets or credentials.
- [ ] Options are canonical and parseable by IssueOps automation.
- [ ] Body field IDs remain stable unless workflow consumers are updated.
- [ ] Strict Copilot primitive validation passes.
