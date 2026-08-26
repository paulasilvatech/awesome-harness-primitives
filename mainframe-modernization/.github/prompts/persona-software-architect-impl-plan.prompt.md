---
name: "impl-plan"
description: "Structure a feature's plan.md into dependency-ordered phases with parallelism markers, capability profiles, and measurable exit criteria."
argument-hint: "feature=NNN-feature-name"
agent: "software-architect"
tools: ["read", "search", "edit"]
---
# /impl-plan

## Objective

Turn the tasks for one feature into a sequenced, phased implementation section
inside `specs/<NNN>-<feature>/plan.md`. Each task is ordered by dependency, marked
parallelizable where safe, tagged with the capability profile it needs, and gated
by measurable exit criteria. The result lets Pairs 3 and 4 start work without
inventing scope.

## When to Invoke

In Stage 2, after `spec.md` and the initial `plan.md` design exist, and before
Stage 3 implementation begins.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` exists and every REQ-ID has `source_legacy:`
- `specs/<NNN>-<feature>/plan.md` exists with the Modular Monolith design (from `/design-modular-monolith`)
- `specs/<NNN>-<feature>/tasks.md` exists or the task list is agreed

## Inputs the Team Must Provide

- The feature identifier (for example, `014-registration`)
- The task list, if it is not already in `tasks.md`

Ask the user for anything that is missing.

## What I Will Do

- Read `spec.md`, `plan.md`, and `tasks.md` for the feature
- Group tasks into phases by dependency order: foundation, then features, then hardening
- Mark a task `[P]` only when it touches disjoint files and has no runtime dependency, verified with grep
- Assign each task a capability profile — deep reasoning, implementation, or mechanical — per [`../../09-cheat-sheets/model-routing.md`](../../09-cheat-sheets/model-routing.md)
- Define a measurable Definition of Done per phase (tests passing, docs updated, review complete)
- Record a global risks table with mitigations

## What I Will NOT Do

- Pin a specific model or provider — the capability profile is guidance; the user chooses the execution context
- Mark a task `[P]` without verifying that its files are disjoint
- Write implementation code — I structure the plan, not the solution
- Invent tasks or REQ-IDs the team has not agreed
- Design the architecture — that is redirected to `/design-modular-monolith`, with decisions recorded through [`../skills/adr-draft/SKILL.md`](../skills/adr-draft/SKILL.md)

## Output Format

An implementation section appended to `specs/<NNN>-<feature>/plan.md`. Example
(illustrative):

```markdown
## Implementation plan

### Phase 1 — Foundation (est. 2h)
Objective: schema and module skeleton in place.
Exit criteria: migration applies, module compiles, CI green.

| Task ID | Title | [P] | Capability Profile | Est. Effort | Traces To |
|---------|-------|-----|--------------------|-------------|-----------|
| T-01 | Create registration table migration |  | mechanical | 1h | REQ-015 |
| T-02 | Scaffold registration module package | [P] | implementation | 1h | REQ-014 |

### Phase 2 — Features (est. 4h)
Exit criteria: acceptance tests pass for REQ-014 and REQ-015.

### Global risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Legacy rule for REQ-015 unconfirmed | Wrong behavior | Block T-04 until archaeology confirms |
```

## Definition of Done

- [ ] Every task traces to at least one REQ-ID
- [ ] `[P]` tasks are verified to touch independent files (grep evidence noted)
- [ ] Each phase has measurable exit criteria
- [ ] Each task has a capability profile
- [ ] No task exceeds one day of effort without being decomposed
- [ ] A global risks table with mitigations is present

## Prompt Body

You are the `@software-architect`. The team needs the feature's work sequenced
into an executable plan.

**Step 1 — Read the feature artifacts.**
Open `spec.md`, `plan.md`, and `tasks.md` for the feature. List the REQ-IDs and
the agreed tasks. If `tasks.md` is missing, ask the team for the task list.

**Step 2 — Order into phases.**
Group tasks by dependency into foundation (schema, module skeleton, shared
types), features (the REQ-bearing behavior), and hardening (tests, observability,
security review). A task belongs to the earliest phase whose predecessors it does
not depend on.

**Step 3 — Mark safe parallelism.**
Mark a task `[P]` only when it touches a disjoint set of files and has no runtime
dependency on another in-flight task. Verify disjointness with grep and note the
evidence. When in doubt, do not mark it.

**Step 4 — Assign capability profiles.**
Tag each task deep reasoning (architectural judgment), implementation (writing
code and tests), or mechanical (bulk edits, formatting), following the model
routing card. State the profile as guidance only — never pin a model.

**Step 5 — Define phase exit criteria.**
For each phase write measurable exit criteria: which tests pass, which docs
update, and that review is complete. "Done" must be checkable, not aspirational.

**Step 6 — Record risks.**
Add a global risks table: risk, impact, mitigation. Include any task blocked by an
unconfirmed legacy rule or open question.

Keep every task under one day of effort; decompose anything larger. Do not add
scope the team has not agreed.

## Invocation Example

```
/impl-plan feature=014-registration
```
