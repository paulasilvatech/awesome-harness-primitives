---
name: 'modernize-reimagine'
description: 'Design a target modernization architecture that preserves required behavior and names intentional changes.'
agent: 'agent'
argument-hint: 'legacy system, rules artifact, map artifact, or target stack'
---

# Modernize Reimagine

Design the target architecture for `${input:target:legacy system, rules artifact, map artifact, or target stack}`.

## First step

Load the `code-modernization` skill (Agent Skill) before designing. Use the `Architecture Critic` agent to challenge the design before finalizing it.

## Steps

1. Read the brief, assessment, rules, and map artifacts when available.
2. Define target APIs, data model, runtime, deployment model, observability, security, and migration phases.
3. Explicitly list what stays behaviorally identical and what changes intentionally.
4. Write `analysis/<system>/DESIGN.md` and diagram artifacts as needed.

## Output

Output concisely: return only artifact paths, design decisions, intentional behavior changes, validation status, and blockers.
