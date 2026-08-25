---
name: "open-horizons-backstage-assess"
description: "Assess one Open Horizons Backstage scope from repository evidence and report findings in Chat without making changes."
argument-hint: "scope=<Open Horizons Backstage subsystem or question>"
agent: "open-horizons-backstage-expert"
tools: ["read", "search", "web"]
---

# Open Horizons Backstage assessment

## Objective

Assess `${input:scope}` and return an evidence-based, read-only report in Chat.

## When to Invoke

Use when a bounded Open Horizons Backstage question must be answered before planning or implementation.

## Preconditions

- `${input:scope}` is specific enough to bound the assessment.
- The relevant repository content is readable.

If either condition fails, identify the missing input in Chat and stop.

## Inputs the Team Must Provide

- Scope or question: `${input:scope}`.
- Optional selected evidence: `${selection}`.

## What I Will Do

- Use the `open-horizons-backstage-expert` agent's assessment behavior within the supplied scope.
- Distinguish inspected evidence, inference, and unknowns.
- Return prioritized findings and validation gaps to Chat.

## What I Will NOT Do

- Edit files, run mutating commands, or change external systems.
- Expand the assessment beyond `${input:scope}`.
- Present static inspection as runtime proof.

## Output Format

```markdown
## Open Horizons Backstage assessment

**Scope:** <subsystem>
**Mode/version:** <value and evidence, or unknown>

### Findings
| Priority | Finding | Evidence | Recommended next step |
| --- | --- | --- | --- |

### Validation gaps
- <unrun check and reason, or none>
```

## Definition of Done

- [ ] Findings answer `${input:scope}` and cite repository evidence.
- [ ] Unknowns and unrun checks are explicit.
- [ ] The result is returned only in Chat.
- [ ] No workspace or external-system change occurred.

## Prompt Body

Ask for a missing scope, otherwise have `open-horizons-backstage-expert` assess only
`${input:scope}` using `${selection}` when present. Remain read-only and return the required report
in Chat.

## Invocation Example

Run **Chat: Run Prompt**, select `open-horizons-backstage-assess`, and enter
`catalog entity ownership and discovery configuration`. Verify that the response stays in Chat and
the workspace remains unchanged.
