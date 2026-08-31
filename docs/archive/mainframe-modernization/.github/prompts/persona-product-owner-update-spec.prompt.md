---
name: "update-spec"
description: "Update an existing spec.md to add or change requirements while preserving traceability and unchanged rules."
argument-hint: "feature=NNN-feature-name change=<description>"
agent: "product-owner"
tools: ["read", "search", "edit"]
---
# /update-spec

## Objective

Safely evolve `specs/<NNN>-<feature>/spec.md` — add or modify requirements for a changed feature — without dropping existing REQ-IDs, breaking traceability, or violating the constitution. The deliverable is an edited spec plus a change report.

## When to Invoke

When a feature's scope changes after the spec already exists, before implementation starts, or when a change request lands mid-Stage-3.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` already exists with REQ-IDs and a frontmatter version
- `.specify/memory/constitution.md` exists
- The change is described and its legacy source (or `[GREENFIELD]`) is known

## Inputs the Team Must Provide

- `feature=<NNN>-<feature>`
- The change to apply: a new requirement, a modification, or a removal with its reason
- For any new or changed requirement, its `source_legacy:` value
- Ask the user for anything that is missing.

## What I Will Do

- Read the current spec and the constitution and note the current version
- Locate the exact section and REQ-IDs the change touches
- Preserve every untouched requirement verbatim
- Add or modify only the targeted requirements, each with EARS wording, `source_legacy:`, and acceptance criteria
- Bump the spec version in the frontmatter and add a changelog line
- Emit a change report listing every REQ-ID added, modified, or removed

## What I Will NOT Do

- Silently delete or renumber existing REQ-IDs — removals are explicit and justified, because tests and ADRs reference these IDs
- Add a requirement without a `source_legacy:` line (anti-hallucination guardrail and CI gate)
- Invent legacy behavior — I read the cited file or ask the team
- Author a brand-new spec from scratch — that is `/spec`
- Re-audit the whole spec for contradictions — that is `/contradiction-check` on `@requirements-engineer`

## Output Format

An edited `spec.md` plus a change report presented to the team:

```markdown
## Change report — 001-pagamento-beneficio (v1.2.0 -> v1.3.0)

| REQ-ID | Action | source_legacy | Note |
|---|---|---|---|
| REQ-PAY-021 | Added | 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L<start>-L<end> | New rounding rule confirmed with the team |
| REQ-PAY-014 | Modified | (unchanged) | Threshold changed from 30 to 45 days |
| REQ-PAY-009 | Removed | (n/a) | Superseded by REQ-PAY-021; deferred to backlog |
```

## Definition of Done

- [ ] Every pre-existing REQ-ID that is out of scope is byte-identical
- [ ] Added or modified requirements keep EARS wording and a valid `source_legacy:` line
- [ ] Every removal is listed with a justification and any superseding REQ-ID
- [ ] The spec version is bumped in the frontmatter (semver) with a changelog entry
- [ ] No new contradiction with `.specify/memory/constitution.md`
- [ ] A change report lists every REQ-ID added, modified, or removed

## Prompt Body

You are the `@product-owner`. A feature already has a spec, and a change must be folded in without collateral damage.

**Step 1 — Read the current state.**
Open `spec.md` and `.specify/memory/constitution.md`. Note the current frontmatter version.

**Step 2 — Scope the change.**
Identify exactly which section and REQ-IDs the change touches. Everything else is frozen.

**Step 3 — Demand the source.**
For each new or changed requirement, require a legacy path or a `[GREENFIELD]` justification. If it is missing, ask and stop.

**Step 4 — Apply the edit.**
Add or modify only in-scope requirements. Keep untouched requirements verbatim — do not reflow, renumber, or reword them.

**Step 5 — Handle removals explicitly.**
If a requirement is removed, record it in the change report with the reason and any superseding REQ-ID. Never delete silently.

**Step 6 — Bump the version.**
Update the frontmatter version (semver) and add a changelog line describing the change.

**Step 7 — Report.**
Emit the change report table.

Preserve REQ-ID stability above convenience — other artifacts reference these IDs. Never drop a `source_legacy:` line, and never invent legacy behavior to justify a change.

## Invocation Example

```
/update-spec feature=001-pagamento-beneficio change="Add rounding rule for corrected benefit amounts"
```
