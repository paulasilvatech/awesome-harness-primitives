---
name: sdd-spec-engineer
description: 'Use when orchestrating Spec-Driven Development from approved requirements into SDD artifacts: specification, design, task plan, traceability matrix, EARS acceptance criteria, Mermaid architecture, and pre-implementation quality gates. Produces SPECIFICATION, DESIGN, TASKS, and ANALYSIS-style deliverables for coding-agent handoff. DO NOT USE FOR: standalone FRD/NFRD authoring before sdd_init (use requirements-engineer), INVEST user story decomposition or GitHub Issue creation (use story-planning), Foundry runtime/provisioning detail (use ai-foundry-operations or foundry-agent-blueprint), or general agentic architecture trade-off decisions (use agentic-architecture-patterns). Triggers include "spec this", "run SDD", "create a task plan", and "write EARS requirements".'
---

# SDD Spec Engineer

Use this skill to transform approved requirements into Spec-Driven Development artifacts using EARS notation and the repository templates in `golden-paths/common/templates/`. It produces traceable specification, design, tasks with `[P]` markers, and a quality-gate analysis suitable for coding-agent handoff.

> [!NOTE]
> This skill depends on bundled `references/ears-notation.md` and `references/spec-templates.md`, plus SDD templates in `golden-paths/common/templates/`. Resolve bundled references relative to this `SKILL.md`. It does not require a CLI or MCP server by default.

## When to invoke

- "Spec this feature using SDD."
- "Create EARS requirements and a design for this change."
- "Generate a task plan with parallel markers."
- "Analyze this spec for traceability gaps."
- "Prepare implementation handoff after requirements approval."

## Prerequisites and context

- FRD/NFRD or equivalent approved requirements exist.
- Scope boundaries and non-goals are known.
- `golden-paths/common/templates/CONSTITUTION.md`, `golden-paths/common/templates/SPECIFICATION.md`, and `golden-paths/common/templates/IMPLEMENTATION_PLAN.md` exist.
- Reference files under `references/` exist.

## Procedure

### Step 1: Load SDD references

Read `references/ears-notation.md` and `references/spec-templates.md` before authoring.

### Step 2: Confirm feature scope

1. Name the feature with a sequential folder-friendly slug such as `001-feature-name`.
2. Confirm included and excluded requirements.
3. Identify constraints from the approved NFRD.

### Step 3: Write EARS requirements

Use only these patterns:

- Ubiquitous: `The <system> shall <response>.`
- Event-driven: `When <trigger>, the <system> shall <response>.`
- State-driven: `While <state>, the <system> shall <response>.`
- Unwanted behavior: `If <condition>, then the <system> shall <response>.`
- Optional feature: `Where <feature is included>, the <system> shall <response>.`

### Step 4: Produce design and task artifacts

- Design includes architecture overview, Mermaid diagram, components, data model, interfaces, risks, and trade-offs.
- Tasks are atomic, sequenced, and trace to requirements.
- Use `[P]` only for tasks that can run in parallel without file or state conflicts.

### Step 5: Classify specification findings

| Severity | Meaning |
| --- | --- |
| Critical | Requirement has no task, task has no requirement, or acceptance criteria are not testable. |
| High | Design omits security, data model, or integration needed by P0 requirements. |
| Medium | Task ordering, naming, or parallel marker issue. |
| Low | Formatting, wording, or traceability table polish. |

### Step 6: Pre-implementation gate

```text
SDD action: create or update SDD artifacts and handoff
Artifacts ready: Requirements, Design, Tasks, Analysis
Traceability: <complete|incomplete>
Open questions: <count>
Proceed with writing artifacts or implementation handoff? (y/n)
```

> [!IMPORTANT]
> Only write SDD artifacts or hand off to implementation after explicit approval and a complete traceability matrix when the user has not already requested file creation. On a negative, ambiguous, or missing response, stop at the artifact review and list unresolved gaps.

## Limits

- Do not use this skill for: standalone FRD/NFRD authoring before sdd_init (use requirements-engineer), INVEST user story decomposition or GitHub Issue creation (use story-planning), Foundry runtime/provisioning detail (use ai-foundry-operations or foundry-agent-blueprint), or general agentic architecture trade-off decisions (use agentic-architecture-patterns).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| Requirements are missing | Route to `requirements-engineer` before SDD artifact generation. |
| EARS criteria are vague | Rewrite into one atomic, observable EARS sentence. |
| Mermaid diagram is malformed | Simplify the diagram and validate syntax before delivery. |
| Task lacks traceability | Add requirement references or remove the task. |
| Too many sequential tasks | Recheck independence and mark safe tasks with `[P]`. |

## Output template

Return exactly this structure:

```markdown
## SDD Artifact Report

**Feature:** <feature-slug>
**Artifacts:** <Requirements|Design|Tasks|Analysis>
**Traceability:** <complete|incomplete>

### Findings
| Finding | Severity | Fix |
| --- | --- | --- |
| <finding> | <severity> | <fix> |

### Handoff
- Requirements approved: <yes|no>
- Design reviewed: <yes|no>
- Tasks ready: <yes|no>
- Open questions: <questions>
```

## Quality gate

- [ ] Loaded EARS and spec template references.
- [ ] Used only EARS acceptance patterns.
- [ ] Included design, tasks, and analysis where requested.
- [ ] Every requirement traces to at least one design component and task.
- [ ] Every task traces to a requirement.
- [ ] Implementation handoff is gated on explicit approval.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
