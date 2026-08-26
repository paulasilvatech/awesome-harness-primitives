---
name: "spec-sync"
description: "Detect drift between spec.md and the implementation and propose a synchronizing spec update."
argument-hint: "feature=NNN-feature-name"
agent: "requirements-engineer"
tools: ["read", "search", "execute"]
---
# /spec-sync

## Objective

Detect drift between `specs/<NNN>-<feature>/spec.md` and the code, classify every REQ-ID, and propose a spec patch that closes the gap. The deliverable is a drift report plus a proposed patch — not an applied edit, and never an assumption that the code is correct.

## When to Invoke

Mid-to-late Stage 3 or Stage 4, when code has moved ahead of (or behind) the spec and the team needs to reconcile them.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` exists with REQ-IDs
- Feature code and tests exist
- The team can confirm sources for any newly discovered behavior

## Inputs the Team Must Provide

- `feature=<NNN>-<feature>`
- Optional scope: a subset of REQ-IDs or packages
- For any Undocumented behavior the team decides to keep, its `source_legacy:`
- Ask the user for anything that is missing.

## What I Will Do

- Parse the REQ-IDs from `spec.md`
- Grep the codebase for REQ-ID references in comments, test names, and commit messages
- Classify each REQ-ID: Implemented (code and test), Partial (code only), Orphaned (no code), Undocumented (code cites an unknown REQ-ID)
- Sample three representative flows and compare the spec against the actual code path
- Propose spec additions for Undocumented items, each with a proposed REQ-ID, EARS statement, and a required `source_legacy:` placeholder
- Rank the top three drifts by risk

## What I Will NOT Do

- Auto-write the spec — I propose a patch; the product owner approves it
- Mint a requirement for Undocumented code without demanding its `source_legacy:` (anti-hallucination guardrail and CI gate)
- Assume code is correct because it exists — drift can mean the code is wrong, not the spec
- Invent a legacy source for discovered behavior — the team supplies it
- Classify anything without a `file:line` citation

## Output Format

A drift table, a proposed patch, and a ranked risk list, presented to the team.

Drift table:

```markdown
## Sync report — 001-pagamento-beneficio

| REQ-ID | Status | Evidence (file:line) | Action |
|---|---|---|---|
| REQ-PAY-014 | Implemented | PaymentBatchService.java:132; PaymentBatchServiceTest.java:88 | None |
| REQ-PAY-021 | Partial | BenefitAmount.java:57 | Add a test referencing REQ-PAY-021 |
| REQ-PAY-030 | Orphaned | — | Implement or defer |
| REQ-PAY-041 | Undocumented | DuplicateFilter.java:24 | Add REQ to spec (source_legacy required) |
```

Proposed patch for each Undocumented item:

```diff
+ ### REQ-PAY-041 (unwanted)
+ If a payment line duplicates an already-imported line, then the system shall ignore the duplicate.
+ source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L<start>-L<end>
```

Then a "Top 3 drifts by risk" list, ordered by business impact and incident likelihood.

## Definition of Done

- [ ] Every REQ-ID in the spec is classified with `file:line` evidence
- [ ] Every Undocumented finding has a proposed REQ-ID, EARS statement, and a `source_legacy:` placeholder the team must fill
- [ ] The proposed patch applies cleanly to the current `spec.md` structure
- [ ] Behavioral drift was checked on at least three representative flows
- [ ] The top three drifts are ranked by risk
- [ ] No spec file was modified

## Prompt Body

You are the `@requirements-engineer` reconciling the written spec with what the code actually does.

**Step 1 — Parse REQ-IDs.**
Read `spec.md` and list every declared REQ-ID.

**Step 2 — Grep for references.**
Search the codebase for each REQ-ID in comments, test names, and commit messages. Record `file:line` for every hit.

**Step 3 — Classify each REQ-ID.**
Implemented (code and test), Partial (code only), Orphaned (no code), or Undocumented (code references a REQ-ID the spec does not declare).

**Step 4 — Sample behavioral drift.**
Pick three representative flows and compare the specified behavior against the actual code path. Note mismatches.

**Step 5 — Propose the patch.**
For each Undocumented item, draft a new REQ with an EARS statement and a `source_legacy:` placeholder the team must fill. Do not invent the source.

**Step 6 — Rank the top three by risk.**
Order by business impact and likelihood of an incident.

Propose, do not apply. Every proposed REQ needs a `source_legacy:` line the team fills, and drift is a question about which side is right — never an assumption that code wins.

## Invocation Example

```
/spec-sync feature=001-pagamento-beneficio
```
