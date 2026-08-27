---
name: ai-team-orchestration
description: >-
  Bootstrap and run a lightweight multi-agent development team. Use when starting or adopting a
  project, planning multi-step work, coordinating implementation with optional QA, brainstorming
  with distinct perspectives, or preserving PROJECT_BRIEF context across sessions.
---

<!-- Generated from harness/github-copilot/plugins/ai-team-orchestration/skills/ai-team-orchestration/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# AI team orchestration

Use three stable roles to turn an ambiguous project request into a proportional plan, implementation handoff, optional independent QA, and durable context that a later GitHub Copilot session can resume.

## When to invoke

- "Start a lightweight AI team for this project."
- "Coordinate Producer, Dev, and QA for this change."
- "Create or update a project brief before we continue."
- "Run a brainstorm with separate product and engineering perspectives."
- "Recover context from the last session and continue."

## Team roles

| Role | Handle | Owns | Does not own |
| --- | --- | --- | --- |
| Producer | `@ai-team-producer` | Scope, acceptance criteria, risk, sequencing, handoffs, merge readiness | Implementation details that Dev can decide locally |
| Dev | `@ai-team-dev` | Code changes, tests, self-review, PR preparation, limitations | Independent sign-off when risk requires QA |
| QA | `@ai-team-qa` | Behavioral verification, regression checks, reproducible findings, fix verification | Routine ceremony for small obvious changes |

Nova, Sage, and Milo are perspectives inside the Dev agent, not mandatory project layers. Treat them as thinking lenses for product, architecture, and implementation tradeoffs rather than extra agents that must exist in every workflow.

## Proportional workflow

| Work shape | Coordination depth | Required artifact |
| --- | --- | --- |
| Small and obvious | Dev implements directly; Producer only clarifies if needed | Final summary and checks |
| Multi-step or cross-cutting | Producer writes a short plan, Dev executes, optional self-review | Active plan or progress note |
| Risky, ambiguous, or policy-heavy | Producer coordinates plan, Dev implements, QA independently verifies | Plan, QA findings, PR-ready verification |
| Long-lived or interrupted | Preserve durable state before ending | `PROJECT_BRIEF.md` or progress note |

Default flow: Plan -> Implement -> Test -> optional review or QA -> Merge -> update project state. Let branch protection, required checks, permissions, and merge queues enforce repository merge policy; do not embed universal Git commands when the repository already has its own policy.

## Start or adopt a project

1. Read repository instructions, README files, architecture notes, and contribution guidance before inventing process.
2. Discover the actual stack, commands, deployment model, data stores, and risks from files in the repository.
3. Create or update `PROJECT_BRIEF.md` only when durable cross-session context is useful. Start from `references/project-brief-template.md` and omit irrelevant sections.
4. For substantial work, create a concise plan from `references/sprint-plan-template.md`.
5. Use a separate branch or clone when parallel sessions could conflict, following the repository's own Git policy.
6. Keep bugs, blockers, and durable decisions in project systems, not only in chat.

## Execution rules

| Agent | Required behavior |
| --- | --- |
| Producer | Define outcome, constraints, acceptance criteria, exclusions, review need, and QA threshold. Keep durable state concise and current. |
| Dev | Follow repository conventions, implement the smallest complete solution, run relevant checks, inspect the final diff, and prepare PR summary, verification, and limitations. |
| QA | Use only when dedicated behavioral verification adds value. Test the requested behavior and important regressions, report reproducible findings, and verify fixes. |

## Brainstorming and context recovery

Use `references/brainstorm-format.md` for product or architecture decisions that benefit from competing perspectives. For ordinary implementation choices, let Dev decide using repository conventions.

Before ending a long or interrupted session:

1. Update the active plan or progress note if one exists.
2. Record material decisions, blockers, and the next action in repository context.
3. Leave a cold-start prompt:

```text
Read the repository instructions, then read whichever sources exist for this
work: the active issue or request, PROJECT_BRIEF.md, and the active plan or
progress note.
Continue from the recorded next action.
```

## Tool and model inheritance

The bundled agents intentionally omit `tools` and `model` frontmatter so available built-in, MCP, and extension tools remain usable, developers keep control of model selection, and role boundaries stay defined by instructions plus normal trust, permission, authentication, and approval controls. If the environment exposes too many tools, deselect irrelevant tools or MCP servers, or use VS Code virtual-tool management. Do not add a machine-specific plugin allowlist.

## Progressive disclosure and bundled resources

Read bundled references only when the current work needs them:

| Resource | Use it when |
| --- | --- |
| `references/project-brief-template.md` | Durable cross-session project context is useful. |
| `references/sprint-plan-template.md` | Work needs a short implementation plan. |
| `references/brainstorm-format.md` | A product or architecture question benefits from multiple perspectives. |
| `references/anti-patterns.md` | The team is drifting into process-heavy or unsafe coordination. |

## Gotchas

- **Do not turn every task into ceremony**: skip formal planning and QA when the change is small and obvious.
- **Do not treat desks or agents as permission bypasses**: repository policy, branch protection, required checks, and user authorization still control privileged actions.
- **Do not make durable files noisy**: `PROJECT_BRIEF.md` should preserve decisions and next actions, not transcript-level detail.

## Output template

```markdown
## AI team orchestration result

**Status:** planned | implemented | qa-ready | blocked
**Roles used:** Producer | Dev | QA | <combination>
**Scope:** <requested outcome and explicit exclusions>

### Plan or handoff
- <step, owner, and acceptance criterion>

### Durable context
- `PROJECT_BRIEF.md`: created | updated | not needed
- Active plan/progress note: <path or none>
- Next action: <specific next action>

### Verification
- <check performed>: <result and evidence>
```

## Quality gate

- [ ] The workflow depth matches the risk and size of the request.
- [ ] Producer, Dev, and QA responsibilities are separated only when separation adds value.
- [ ] Repository instructions and contribution policy were followed instead of replaced.
- [ ] `PROJECT_BRIEF.md` or a progress note was created or updated only when durable context is useful.
- [ ] Any referenced bundled resource exists and was used only on demand.
- [ ] The final handoff names the next action, current blocker, and verification evidence.
