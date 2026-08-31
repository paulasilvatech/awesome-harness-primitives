---
name: "write-ears-spec"
description: "Guides the team in recording confirmed EARS requirements in spec.md with mandatory traceability."
argument-hint: "feature=NNN-feature-name rules=01-archaeology/business-rules-catalog.md"
agent: "architect"
tools: ["read", "search", "edit"]
---
# /write-ears-spec

## Objective

Transform only confirmed Stage 1 rules into formal EARS requirements in `specs/<NNN>-<feature>/spec.md`. Open questions remain questions; the prompt does not fill in requirements, acceptance criteria, or architecture through assumptions.

## When to Invoke

At the start of Stage 2, once Pair 2 has selected the narrow feature and completed the H1 handoff, working on the `spec/<NNN>-<feature>` branch cut from `develop`.

> [!NOTE]
> Do not invoke this prompt to explore the legacy system, to catalog open questions (use `/catalog-mysteries`), or to design modules (use `/design-modular-monolith`). It records requirements that already have confirmed evidence — nothing else.

## Preconditions

- `01-archaeology/business-rules-catalog.md` contains the scope evidence
- The team identified the `specs/<NNN>-<feature>/` folder
- The team read each legacy source before drafting

## Inputs the Team Must Provide

- `feature=<NNN>-<feature-name>` — the folder under `specs/` that receives `spec.md` (for example, `feature=001-benefit-calculation`)
- `rules=01-archaeology/business-rules-catalog.md` — the catalog whose **Confirmed** rows are the only promotion candidates
- The subset of confirmed rules the team agrees belong to this narrow feature
- For any capability with no legacy equivalent, the `[GREENFIELD]` justification the team stands behind

## What I Will Do

- Confirm with the team which catalog rules belong to the narrow feature; record deferrals in `02-modern-spec/scope-decisions.md`
- Validate the `.NSP`, `.NSN`, `.NSC`, `.NSA`, `.NSL`, `.jcl`, or `.ddm` source of each confirmed rule before proposing a testable EARS requirement
- Assign a unique REQ-ID and attach `source_legacy:` with the path and, when available, the line range; use `[GREENFIELD]` plus the team's justification when no legacy equivalent exists
- Record Given/When/Then criteria only for behaviors the evidence or a scope decision supports
- Preserve every not-yet-validated item from `01-archaeology/mysteries-found.md` under "Open Questions" with its evidence, impact, unconfirmed hypothesis, owner, and status
- Maintain a traceability matrix in `spec.md`

## What I Will NOT Do

- Create a requirement without `source_legacy:` or a justified `[GREENFIELD]`
- Promote a hypothesis or open question into a requirement, answer it, or change its status
- Require a fixed number of requirements, C4 diagrams, ADRs, or endpoints — reduce scope if Stage 2 runs short on time
- Write formal artifacts in `02-modern-spec/` — Spec-Kit artifacts live in `specs/<NNN>-<feature>/`
- Invent SIFAP business facts — I record only what the reviewed legacy source shows

## Output Format

Append each requirement to `specs/<NNN>-<feature>/spec.md` in this shape (values are illustrative — use the team's confirmed evidence):

```markdown
### REQ-007 — Short imperative title of the behavior

If <unwanted condition from the confirmed rule>, then the system shall <required behavior>.

- source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSN:Lstart-Lend
- Acceptance (Given/When/Then):
  - Given <precondition the evidence supports>
  - When <trigger>
  - Then <observable, testable outcome>
```

Keep a traceability matrix in the same `spec.md`:

| REQ-ID | EARS Pattern | source_legacy | Source Rule | Source File |
|---|---|---|---|---|
| REQ-007 | Unwanted | `<PROGRAM>.NSN:Lstart-Lend` | Rule 4 | `business-rules-catalog.md` |

## Definition of Done

- [ ] `specs/<NNN>-<feature>/spec.md` contains only the feature requirements
- [ ] Every requirement has EARS wording, a verifiable criterion, and a valid `source_legacy:` or justified `[GREENFIELD]`
- [ ] Open questions remain outside the requirements, unchanged in status
- [ ] The traceability matrix links each REQ-ID to the reviewed evidence

## Prompt Body

You are the `@architect`. The team is in Stage 2 and needs to promote confirmed Stage 1 rules into formal EARS requirements. You transcribe evidence into requirements; you never invent it.

**Step 1 — Confirm the feature scope.**
Open `01-archaeology/business-rules-catalog.md`. List only the rows classified as **Confirmed** that the team assigns to feature `<NNN>-<feature>`. For every confirmed rule the team defers, record it in `02-modern-spec/scope-decisions.md` with a one-line reason. Do not pull in **Inferred** or **Mystery** rows.

**Step 2 — Validate each source before writing.**
For each candidate rule, open the cited legacy member (`.NSP`, `.NSN`, `.NSC`, `.NSA`, `.NSL`, `.jcl`, or a `.ddm` DDM) and confirm the line range actually contains the logic. If the citation does not resolve, stop and return the rule to the team as an open question. Never cite a `.NSD` file — none exists in this corpus.

**Step 3 — Write the EARS requirement.**
For each validated rule, assign the next sequential `REQ-NNN` and write one EARS sentence using the matching pattern:

- Ubiquitous — "The system shall..."
- Event-driven — "When [event], the system shall..."
- State-driven — "While [state], the system shall..."
- Optional — "Where [feature], the system shall..."
- Unwanted — "If [unwanted condition], then the system shall..."

Attach `source_legacy:` with the path and line range. For a capability with no legacy equivalent, write `[GREENFIELD]` followed by the justification the team provided — never one you invented.

**Step 4 — Record acceptance criteria.**
Add Given/When/Then criteria only for behavior the evidence or a recorded scope decision supports. Do not specify acceptance for anything the source does not show.

**Step 5 — Carry open questions through untouched.**
Open `01-archaeology/mysteries-found.md`. For every item not yet validated, copy it into an "Open Questions" section of `spec.md`, preserving its evidence in `path:line` form, impact, unconfirmed hypothesis, owner, and status. Do not answer it, propose an answer, or change its status. A question is never a requirement.

**Step 6 — Build the traceability matrix.**
Maintain a `REQ-ID | EARS Pattern | source_legacy | Source Rule | Source File` table in `spec.md` with one row per requirement.

**Step 7 — Write the output.**
Write everything to `specs/<NNN>-<feature>/spec.md`. Do not place `spec.md`, `plan.md`, or `tasks.md` in `02-modern-spec/`. Do not require a fixed count of requirements; if Stage 2 is short on time, reduce scope rather than pad the spec. You record confirmed evidence in EARS form — you never fill gaps with assumptions or fabricate SIFAP business facts.

## Invocation Example

```text
/write-ears-spec feature=001-benefit-calculation rules=01-archaeology/business-rules-catalog.md
```

Expect a `specs/001-benefit-calculation/spec.md` containing only evidence-backed EARS requirements, each with `source_legacy:`, plus a traceability matrix; open questions are copied through untouched.
