---
name: open-horizons-orchestration
description: >-
  Classifies and coordinates repository work across Open Horizons agents with bounded delegation,
  validation, review, and approval gates. Use when handling cross-domain maintenance, feature,
  improvement, modernization, incident, review, or explicitly requested greenfield workflows.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/open-horizons-orchestration/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Open Horizons Orchestration

Turn a repository request into an owned, dependency-aware execution flow without granting the
orchestrator implementation or deployment authority.

## When to invoke

- "Coordinate a change across multiple Open Horizons components."
- "Decide which agent should own this request."
- "Implement a feature that needs code, tests, review, and deployment handoff."
- "Fix or modernize an existing subsystem with specialist validation."

## Prerequisites and context

- Use the installed agents and skills as the routing inventory.
- Treat repository files, current diagnostics, tests, and user acceptance criteria as evidence.
- Default to brownfield work; greenfield requires explicit user intent.
- Preserve high-impact approval gates from repository and organization policy.

## Procedure

1. Classify the surface. Route application-runtime requests to the MAF/Foundry platform workflow;
   keep repository engineering requests in the GitHub Copilot harness.
2. Classify the mode as `brownfield` unless the user explicitly requests `greenfield`.
3. Classify the intent as `bugfix`, `feature`, `improvement`, `modernization`, `testing`, `review`,
   `security-remediation`, `incident`, `deployment`, or `documentation`.
4. Identify the concrete anchor, affected domains, dependencies, protected paths, risk, and
   acceptance criteria before delegation.
5. Select one owner per writable scope:

   | Domain | Primary owner |
   | --- | --- |
   | General repository code | `open-horizons-engineer` agent |
   | Cross-domain architecture | `open-horizons-architect` agent |
   | Generic Backstage | `backstage-expert` agent |
   | Open Horizons portal | `backstage-expert` agent |
   | Terraform | `open-horizons-terraform` agent |
   | Azure readiness | `open-horizons-azure-readiness` agent |
   | GitHub or Azure DevOps integration implementation | `open-horizons-engineer` agent |
   | GitHub and Azure DevOps coexistence design | `open-horizons-architect` agent |
   | GitHub Copilot primitive architecture | `open-horizons-architect` agent |
   | Security validation | `open-horizons-security-reviewer` agent |
   | Incidents and reliability | `open-horizons-sre-investigator` agent |
   | Approved live operation | `open-horizons-deployment-operator` agent |

6. Delegate objective, mode, intent, anchor, writable and protected paths, evidence, acceptance
   criteria, and required checks. Parallelize only independent scopes.
7. Require executable validation. Return a local defect to its owner no more than twice; escalate a
   falsified design or unresolved cross-domain conflict to the user.
8. Add independent review for broad or user-facing changes and security validation for identity,
   secrets, permissions, external input, or tool execution changes.
9. Consolidate completed evidence, residual risk, approval-gated operations, and the next safe step.

## Output template

Return exactly this structure:

```markdown
## Orchestration result

**Status:** completed | blocked | approval-required
**Surface:** github-copilot-harness | platform-foundry-maf
**Mode:** brownfield | greenfield
**Intent:** <classified intent>

### Ownership
| Scope | Agent | Writable paths | Required validation | Result |
| --- | --- | --- | --- | --- |

### Evidence
- <observed behavior, changed artifact, and actual check result>

### Gates and follow-up
- <approval, residual risk, blocker, or none>
```

## Limits

- Do not implement code, mutate infrastructure, deploy, publish, or approve on another user's behalf.
- Do not use this skill as the runtime orchestrator for the seven application agents; that workflow
  belongs to Microsoft Agent Framework in Microsoft Foundry.
- Do not parallelize agents that can edit the same file or stateful resource.

## Gotchas

- VS Code handoff metadata is not a portable execution graph; use explicit agent delegation when
  orchestration must run.
- A successful plan, dry run, or unit test is evidence, not authorization for a high-impact action.
- Model routing is surface-specific; never send a GitHub Copilot model name to a Foundry deployment.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-orchestrator` | `agent` | A read-only coordinator should run this procedure. |
| `brownfield-engineering` | `skill` | A repository-local implementation owner needs the edit/test loop. |
| `deploy-orchestration` | `skill` | An approved deployment operator needs execution procedure. |
| `agentic-architecture-patterns` | `skill` | The request changes model, memory, context, tool, or guardrail architecture. |

## Quality gate

- [ ] Surface, mode, and intent are explicit.
- [ ] Greenfield mode is backed by explicit user intent.
- [ ] Every writable scope has exactly one owner.
- [ ] Each delegation contains evidence, boundaries, acceptance criteria, and validation.
- [ ] Parallel work has no overlapping files or state.
- [ ] High-impact operations remain approval-gated.
- [ ] Final status reports only checks that actually ran.
