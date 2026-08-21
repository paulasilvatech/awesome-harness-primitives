---
name: requirements-engineer
description: 'Use when eliciting, analyzing, complementing, or validating functional and non-functional requirements before SDD initialization. Produces FRD and NFRD artifacts, gap analysis, assumptions, priorities, measurable acceptance signals, and a Specky handoff block. DO NOT USE FOR: code, implementation, or `golden-paths/common/templates/CONSTITUTION.md` generation, which belongs to sdd_init or sdd-spec-engineer. Triggers include "write requirements", "create an FRD", "create an NFRD", "validate these requirements", and "prepare input for sdd_init".'
---

# Requirements Engineer

Use this skill to turn raw product input into production-grade Functional Requirements Document (FRD) and Non-Functional Requirements Document (NFRD) content ready for Spec-Driven Development. It produces gap analysis, critical questions, assumptions, prioritized requirements, validation results, and a handoff block for `sdd_init`.

> [!NOTE]
> This skill depends on user-provided product context and repository templates under `golden-paths/common/templates/` when aligning with Open Horizons SDD conventions. It does not shell out to a CLI or require an MCP server by default.

## When to invoke

- "Write the FRD and NFRD for this feature."
- "Validate these requirements before sdd_init."
- "Turn these notes into measurable requirements."
- "Find gaps in this product brief."
- "Prepare Specky input from this epic."

## Prerequisites and context

- Raw notes, problem statement, PRD, user story, or stakeholder description is available.
- The project type can be identified as greenfield, brownfield, modernization, legacy migration, API, mobile, data platform, SaaS, internal tool, CLI, or infrastructure.
- Critical scope boundaries, user roles, and primary user actions are known or can be asked as at most three questions.
- The output path is known if files are to be created.

## Procedure

### Step 1: Classify project type

| Type | Signal | Required emphasis |
| --- | --- | --- |
| Greenfield | New product or build from scratch | Success criteria and non-goals. |
| Brownfield | Existing system or extension | Current state, delta scope, backward compatibility. |
| Modernization | Rewrite, migrate, or modernize | Source system, parity, cutover, rollback. |
| API or platform | API, SDK, developer portal | Consumers, versioning, rate limits. |
| SaaS | Tenant or subscription language | Tenant isolation and onboarding. |
| Infrastructure | Platform, AKS, Terraform, environment | Operational constraints and access model. |

### Step 2: Detect critical gaps

Ask at most three questions for missing critical facts. Document all other assumptions.

| Gap | Severity | Action |
| --- | --- | --- |
| User roles and permissions | Critical | Ask before writing final requirements. |
| Primary user action | Critical | Ask before writing final requirements. |
| Scope boundary | Critical | Ask before writing final requirements. |
| Authentication strategy | High | Assume only if the user accepts the assumption. |
| Performance target | High | Propose measurable defaults and mark as assumptions. |

### Step 3: Write functional requirements

Rules for every FR:

- State what the system must do, not how it is implemented.
- Use `must` in FR text.
- Include priority P0, P1, P2, or P3.
- Include an observable acceptance signal.
- Organize by domain, not by UI screen or implementation layer.

### Step 4: Write non-functional requirements

Include measurable targets for performance, security, availability, testability, CI/CD, observability, accessibility, localization, data retention, compliance, and technology constraints.

### Step 5: Validate the artifacts

| Severity | Meaning |
| --- | --- |
| Critical | Missing role, primary action, scope boundary, or testable P0 requirement. |
| High | Vague quality target, missing security method, or no deployment context. |
| Medium | Weak assumption, missing non-goal, or unclear priority. |
| Low | Formatting or terminology issue. |

### Step 6: Produce Specky handoff

Use the existing SDD templates in `golden-paths/common/templates/` as downstream context. Do not generate `golden-paths/common/templates/CONSTITUTION.md`; hand off to `sdd-spec-engineer` or `sdd_init`.

```text
Requirements action: <create|update>
Artifacts: FRD, NFRD
Target path: <path-or-not-specified>
Proceed with writing requirements artifacts? (y/n)
```

> [!IMPORTANT]
> Only create or update FRD/NFRD files after an explicit affirmative response when the user has not already requested file creation. On a negative, ambiguous, or missing response, do not write files; output the artifact drafts and stop.

## Limits

- Do not use this skill for: code, implementation, or `golden-paths/common/templates/CONSTITUTION.md` generation, which belongs to sdd_init or sdd-spec-engineer.
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| Critical context is missing | Ask up to three focused questions and pause finalization. |
| User asks for implementation | Redirect to SDD or implementation workflow after requirements are approved. |
| Requirements include technology choices | Move them to NFRD technology constraints unless they are true business constraints. |
| Too many P0 items | Recommend scope reduction to 5-15 P0 requirements. |
| Acceptance signal is vague | Rewrite with observable pass/fail criteria. |

## Output template

Return exactly this structure:

```markdown
## Requirements Delivery Report

**Project:** <name>
**Project type:** <type>
**Artifacts:** FRD, NFRD
**Readiness for sdd_init:** <Yes|No>

### Gap Analysis
| Gap | Severity | Resolution |
| --- | --- | --- |
| <gap> | <severity> | <resolution> |

### Summary
- Functional requirements: <count>
- Non-functional requirements: <count>
- Assumptions: <count>

### Specky Handoff
FRD: <path-or-title>
NFRD: <path-or-title>
Feature name: <kebab-case>
Open questions: <questions>
```

## Quality gate

- [ ] Project type is identified.
- [ ] Critical gaps are resolved or explicitly blocked.
- [ ] Every FR uses `must` and has priority plus acceptance signal.
- [ ] NFRs are measurable and include deployment context.
- [ ] Assumptions are documented with consequences.
- [ ] Specky handoff is present and does not create `golden-paths/common/templates/CONSTITUTION.md`.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
