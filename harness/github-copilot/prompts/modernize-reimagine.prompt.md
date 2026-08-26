---
name: 'modernize-reimagine'
description: 'Design a target modernization architecture that preserves required behavior and names intentional changes.'
agent: 'modernization'
argument-hint: 'legacy system, rules artifact, map artifact, or target stack'
---

# /modernize-reimagine

## Objective

Design a target modernization architecture that preserves required behavior from legacy evidence while explicitly naming intentional changes across target APIs, data model, runtime, deployment model, observability, security, and migration phases.

## When to Invoke

Use this prompt after `modernize-brief`, `modernize-assess`, `modernize-extract-rules`, and `modernize-map` provide enough evidence, and before `modernize-transform` implements a bounded module.

## Preconditions

- The target legacy system, rules artifact, map artifact, or target stack is identified.
- Brief, assessment, rules, and map artifacts are available when they exist.
- Writing to `analysis/<system>/DESIGN.md` and needed diagram artifacts is permitted.
- The `code-modernization` skill is available.

## Inputs the Team Must Provide

- `target` — the legacy system, rules artifact, map artifact, or target stack to design around.
- Existing brief, assessment, rules, and map artifacts when available.
- Target stack constraints and any required runtime, deployment, observability, or security choices.
- Ask the user for anything that is missing; stop if behavior-preservation requirements or target-stack constraints are too ambiguous to design safely.

## What I Will Do

- Load the `code-modernization` skill before designing.
- Use `critical-thinking` to pressure-test material architecture assumptions before finalizing the design.
- Read the brief, assessment, rules, and map artifacts when available.
- Define target APIs, data model, runtime, deployment model, observability, security, and migration phases.
- Explicitly list what stays behaviorally identical and what changes intentionally.
- Write `analysis/<system>/DESIGN.md` and diagram artifacts as needed.

## What I Will NOT Do

- Implement the design in `modernized/**`; `modernize-transform` owns implementation.
- Harden or rank readiness findings; `modernize-harden` owns final hardening review.
- Hide behavior changes inside architecture prose; every intentional change must be explicit.
- Invent rules that are absent from `analysis/<system>/RULES.md` or inspected evidence.
- Skip architecture criticism when the design has security, migration, deployment, or data-risk trade-offs.

## Output Format

Write `analysis/<system>/DESIGN.md` with this shape:

```markdown
# Modernization Design — <system>

## Source Inputs
- Brief:
- Assessment:
- Rules:
- Map:
- Target stack:

## Design Summary
- Target architecture:
- Main migration approach:

## Target APIs
| API or interface | Purpose | Preserved behavior | Intentional change |
| --- | --- | --- | --- |

## Data Model
| Concept | Legacy source | Target model | Migration note |
| --- | --- | --- | --- |

## Runtime and Deployment Model
- Runtime:
- Deployment model:
- Configuration:

## Observability
- Logs:
- Metrics:
- Traces:
- Alerts:

## Security
- Identity:
- Secrets:
- Authorization:
- Data protection:

## Migration Phases
| Phase | Scope | Entry criteria | Exit criteria | Rollback |
| --- | --- | --- | --- | --- |

## Behavioral Compatibility
### Behaviorally Identical
- 

### Intentional Behavior Changes
| Change | Reason | Approval or SME question | Test implication |
| --- | --- | --- | --- |

## Diagram Artifacts
- 
```

## Definition of Done

- [ ] The `code-modernization` skill was loaded before design started.
- [ ] Brief, assessment, rules, and map artifacts were read when available.
- [ ] Target APIs, data model, runtime, deployment model, observability, security, and migration phases are defined.
- [ ] Required behavior that stays behaviorally identical is listed.
- [ ] Intentional behavior changes are explicit and tied to rationale, approval, or SME questions.
- [ ] `analysis/<system>/DESIGN.md` exists with diagram artifacts as needed.
- [ ] The response returns only artifact paths, design decisions, intentional behavior changes, validation status, and blockers.

## Prompt Body

Follow these steps in order. Preserve required behavior and make every intentional change visible.

**Step 1 — Load the modernization workflow.**
Load the `code-modernization` skill. Use `critical-thinking` to pressure-test material architecture assumptions before finalizing the design.

**Step 2 — Gather design inputs.**
Read `${input:target:legacy system, rules artifact, map artifact, or target stack}`. Read the brief, assessment, rules, and map artifacts when available.

**Step 3 — Define the target architecture.**
Design target APIs, data model, runtime, deployment model, observability, security, and migration phases using the supplied target stack constraints.

**Step 4 — Preserve and name behavior.**
List what stays behaviorally identical. List what changes intentionally, with rationale, approval status, SME question, and test implication.

**Step 5 — Challenge the design.**
Use architecture critique to test the design for security, operability, migration, data, and behavior-preservation risks. Resolve or record findings.

**Step 6 — Write the design artifact.**
Write `analysis/<system>/DESIGN.md` and diagram artifacts as needed.

**Step 7 — Prepare the implementation handoff.**
Identify the bounded module or behavior slice that `modernize-transform` can implement first with behavior-pinning tests.

**Step 8 — Report concisely.**
Return only artifact paths, design decisions, intentional behavior changes, validation status, and blockers.

## Invocation Example

```
/modernize-reimagine target=legacy system, rules artifact, map artifact, or target stack
```
