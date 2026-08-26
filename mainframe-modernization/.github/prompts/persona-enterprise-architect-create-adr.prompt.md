---
name: "create-adr"
description: "Write an ADR capturing the context, options, decision, and consequences of a SIFAP 2.0 architectural choice."
argument-hint: "feature=NNN-feature-name topic=<decision>"
agent: "enterprise-architect"
tools: ["read", "search", "edit"]
---
# /create-adr

## Objective

Produce an Architecture Decision Record using the repository's ADR template, capturing the context, at least three options, the decision, and the consequences of a cross-cutting or feature-scoped SIFAP 2.0 choice. An ADR is immutable after acceptance — corrections come as a new ADR that supersedes it.

## When to Invoke

When a decision blocks `plan.md`, is costly to reverse, affects more than one team, or locks in a technology (see the [`adr-draft`](../skills/adr-draft/SKILL.md) skill for the "should this be an ADR?" test).

## Preconditions

- The decision topic is stated
- The target location is known: project-wide -> `docs/adr/` (template `docs/adr/0000-template.md`); feature-scoped -> `specs/<NNN>-<feature>/` (template `02-modern-spec/ADR-TEMPLATE.md`)
- The next ADR number has been checked to avoid a collision
- Linked REQ-IDs and `.specify/memory/constitution.md` are accessible

## Inputs the Team Must Provide

- `topic=<decision in plain language>`
- The location or scope (project or feature)
- The linked REQ-IDs the decision affects
- The stakeholders and approvers to cite
- A draft of the chosen direction, even if vague
- Ask the user for anything that is missing.

## What I Will Do

- Choose the correct template: `docs/adr/0000-template.md` (project) or `02-modern-spec/ADR-TEMPLATE.md` (feature)
- Pick a verb-led decision title and the next non-colliding number
- Set the status correctly: Proposed, Accepted, Superseded by NNNN, or Rejected
- Write honest context (forces, constraints, prior ADRs)
- List at least three options, including the status quo, with pros, cons, and a cost/risk profile
- State the decision and rationale, and capture positive AND negative consequences
- Link REQ-IDs, prior ADRs, and the constitution rules the decision depends on
- Follow the [`adr-draft`](../skills/adr-draft/SKILL.md) skill for procedure and quality

## What I Will NOT Do

- Present only the chosen option — I always list the rejected alternatives, because half the value is there
- Rewrite an accepted ADR — I create a new one that supersedes it
- Assert what a specific legacy program does — context cites files the team read, or I ask (anti-hallucination guardrail)
- Invent REQ-IDs, approvers, or a decision the team has not made
- Define non-negotiable rules — that is the constitution via `/create-constitution`

## Output Format

A single file following the chosen template. Aligned to `docs/adr/0000-template.md`:

```markdown
# ADR-0007: Adopt Flyway for database migrations

| Field | Value |
|---|---|
| **Status** | accepted |
| **Date** | 2026-05-12 |
| **Authors** | Enterprise Architect — <name> |
| **Supersedes** | N/A |

## Context

The modernization replaces Adabas with PostgreSQL 16 and needs a versioned,
CI-enforced schema-evolution strategy. Cite the legacy programs the team read
(`path#Lstart-Lend`) that drive the schema shape; do not assume their contents.

## Decision

We will adopt Flyway. Each change is a versioned `V<N>__description.sql` file,
and CI runs `flyway:migrate` on every PR to `develop`.

## Alternatives considered

| Alternative | Why it was rejected |
|---|---|
| Liquibase | More verbose XML; steeper ramp-up for the workshop |
| Manual SQL | No traceability, rollback, or CI integration |

## Consequences

- **Easier:** every schema change is traceable and CI-verified.
- **Harder:** applied migrations are immutable; fixes need a new file.
- **Risks:** editing an applied migration breaks Flyway.
- **Mitigations:** branch protection on `develop`.

## Related

- REQ-IDs: REQ-DATA-003
- ADRs: ADR-0003
- Legacy source files: <programs the team cited>
```

## Definition of Done

- [ ] The file follows the chosen template and the `NNNN-title-slug` naming, with no number collision
- [ ] The status is Proposed, Accepted, Superseded by NNNN, or Rejected
- [ ] The date and approvers are recorded
- [ ] At least three options are listed, each with pros, cons, and a cost/risk profile
- [ ] The decision names the chosen option; consequences include positive effects, negative effects, and risks
- [ ] Linked REQ-IDs, prior ADRs, and the relevant constitution rules are cited
- [ ] The ADR is treated as immutable after acceptance — superseded, never rewritten

## Prompt Body

You are the `@enterprise-architect` recording a durable answer to "why did we do it this way?"

**Step 1 — Pick the template and location.**
Project-wide decision -> `docs/adr/` with `docs/adr/0000-template.md`; feature-scoped -> `specs/<NNN>-<feature>/` with `02-modern-spec/ADR-TEMPLATE.md`.

**Step 2 — Choose a precise title and number.**
Use a verb-led title framed as a decision ("Integrate the legacy Adabas data through a REST adapter"), and the next number that does not collide with existing files.

**Step 3 — Set the status.**
Proposed (drafted), Accepted (approved with a date), Superseded by NNNN, or Rejected (recorded to prevent rediscussion).

**Step 4 — Write the context honestly.**
Name the forces and constraints (Java 21, PostgreSQL 16, Azure-only, regulatory) and prior ADRs. Cite legacy files the team actually read; never recall their contents.

**Step 5 — List at least three options.**
Include the status quo or a "do nothing" option. Each option gets a one-line description, up to three pros, up to three cons, and a cost/risk note.

**Step 6 — State the decision and rationale.**
One paragraph each; refer to the chosen option by name.

**Step 7 — Capture consequences.**
Positive effects, negative effects, new risks, and any decisions now forced or constrained.

**Step 8 — Link and sign.**
Cite REQ-IDs, prior ADRs, and the constitution rules the decision depends on; record the date and approvers.

Always list the rejected options, supersede rather than rewrite, and cite legacy files instead of recalling them. A non-negotiable rule belongs in the constitution, not in an ADR.

## Invocation Example

```
/create-adr feature=001-pagamento-beneficio topic="Expose the legacy Adabas data through a REST adapter"
```
