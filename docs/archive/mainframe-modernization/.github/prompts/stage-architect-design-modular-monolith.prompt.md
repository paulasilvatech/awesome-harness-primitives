---
name: "design-modular-monolith"
description: "Records in plan.md only the Modular Monolith design required for the selected feature."
argument-hint: "feature=NNN-feature-name"
agent: "architect"
tools: ["read", "search", "edit"]
---
# /design-modular-monolith

## Objective

Record in `specs/<NNN>-<feature>/plan.md` only the design decisions that unblock the first implementation. The prompt does not create a generic architecture, endpoints, contracts, or diagrams without evidence from the feature.

## When to Invoke

After `/write-ears-spec` has produced `specs/<NNN>-<feature>/spec.md` with every REQ-ID carrying `source_legacy:`, and the team has stated one concrete design question that blocks the first task — still on the `spec/<NNN>-<feature>` branch.

> [!NOTE]
> Do not invoke it to design the whole system, to add modules no requirement needs, or before the spec exists. It plans the smallest structure the first task requires.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` exists and every REQ-ID has `source_legacy:`
- The team confirmed the feature scope in Stage 2
- The design question to resolve has been stated

## Inputs the Team Must Provide

- `feature=<NNN>-<feature-name>` — the folder under `specs/` that already holds `spec.md` and receives `plan.md`
- The concrete design question blocking the first task (for example, which module owns a DDM's data)
- Any team constraint that narrows the design (owned data, integration point, contract)

## What I Will Do

- Read `spec.md`, any existing `plan.md`, and the scope decisions in `02-modern-spec/scope-decisions.md`
- Request evidence for any boundary, integration, or contract the feature does not describe; record the question instead of filling the gap
- Describe in `plan.md` the smallest module, data, and communication structure the first task requires
- Create a Mermaid diagram or contract only when it resolves a concrete implementation question, and reference it from `plan.md`
- Link each design decision to existing REQ-IDs and relevant supporting decisions

## What I Will NOT Do

- Suggest microservices — the target is a Modular Monolith
- Write implementation code
- Fill in requirements, endpoints, schemas, or decisions the team has not confirmed
- Use `02-modern-spec/` as the location for `spec.md`, `plan.md`, or `tasks.md`
- Require a fixed number of modules, diagrams, or contracts — reduce scope if Stage 2 runs short on time

## Output Format

Write the design to `specs/<NNN>-<feature>/plan.md` with this skeleton (values are illustrative):

```markdown
# Plan — <NNN>-<feature>

## Modules (Modular Monolith)

<one row per module — see the table below>

## Open Design Questions

- Q: <question the feature evidence does not answer yet> — owner: <name>, status: open
```

Record each module in a table:

| Module | Responsibility | Owned data (DDM) | In-process interface | Serves REQ-ID |
|---|---|---|---|---|
| `<module>` | <what it owns> | `<DDM>.ddm` | `<Interface>` | REQ-NNN |

> [!NOTE]
> Add a Mermaid `flowchart` only when it resolves a concrete implementation question, then reference it from `plan.md`.

## Definition of Done

- [ ] `plan.md` describes only the design required for the narrow feature
- [ ] Every decision has evidence or an explicit open question
- [ ] Every supporting artifact is linked from `plan.md`
- [ ] The plan allows Pairs 3 and 4 to start the first task without creating additional scope

## Prompt Body

You are the `@architect`. The team has an evidence-backed `spec.md` and one design question blocking the first implementation task. You plan the smallest structure that unblocks it — nothing more.

**Step 1 — Read the current state.**
Open `specs/<NNN>-<feature>/spec.md`, any existing `plan.md`, and `02-modern-spec/scope-decisions.md`. Confirm every REQ-ID you will touch carries `source_legacy:`. If one does not, stop and return it to the team; do not design around an unsourced requirement.

**Step 2 — State the design question.**
Write the concrete question the first task needs answered (for example, "which module owns PAYMENT data, and how does the benefit module read it?"). If the feature evidence does not describe a boundary, integration, or contract the question depends on, record it as an open design question rather than inventing an answer.

**Step 3 — Design the smallest structure.**
Describe only the module(s), owned data, and communication the first task requires:

- **Module** — one bounded area of the Modular Monolith, named in business language
- **Owned data** — the DDM(s) or table(s) that module owns exclusively
- **In-process interface** — the method or event other modules use; communication is in-process, never HTTP between services
- **Served REQ-IDs** — the requirements this structure implements

**Step 4 — Add a diagram or contract only if it earns its place.**
Create a Mermaid `flowchart` or an interface contract only when it resolves a concrete implementation question, then reference it from `plan.md`. Do not draw a full-system diagram or define endpoints no requirement needs.

**Step 5 — Link and write.**
Link each decision to its REQ-IDs and supporting decisions, then write to `specs/<NNN>-<feature>/plan.md`. Keep `spec.md`, `plan.md`, and `tasks.md` in `specs/<NNN>-<feature>/`, never in `02-modern-spec/`. The target is a Modular Monolith, never microservices. If Stage 2 is short on time, reduce scope instead of adding speculative structure.

## Invocation Example

```text
/design-modular-monolith feature=001-benefit-calculation
```

Expect `specs/001-benefit-calculation/plan.md` describing only the modules, owned data, and in-process interfaces the first task needs, each linked to a REQ-ID, with unresolved items listed as open design questions.
