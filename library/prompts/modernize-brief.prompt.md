---
name: 'modernize-brief'
description: 'Capture a modernization brief with scope, drivers, constraints, non-goals, risks, and success criteria.'
agent: 'agent'
argument-hint: 'legacy system folder or modernization initiative'
---

# Modernize Brief

Create a modernization brief for `${input:target:legacy system folder or modernization initiative}`.

## First step

Load the `code-modernization` skill (Agent Skill) before drafting or editing artifacts. Ask only for missing business context that cannot be inferred from files.

## Steps

1. Identify scope, business driver, stakeholders, constraints, non-goals, and success criteria.
2. Record known risks, compliance requirements, data sensitivity, runtime constraints, and timeline.
3. Write `analysis/brief.md` or `analysis/<system>/BRIEF.md`.
4. Include open questions for business and technical owners.

## Output

Output concisely: return only the artifact path, assumptions, open questions, and validation status.
