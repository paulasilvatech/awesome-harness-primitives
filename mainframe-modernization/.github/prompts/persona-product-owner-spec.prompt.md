---
name: "spec"
description: "Draft EARS requirements in spec.md from user stories, each with a mandatory legacy-traceability line."
argument-hint: "feature=NNN-feature-name stories=<path-or-inline>"
agent: "product-owner"
tools: ["read", "search", "edit"]
---
# /spec

## Objective

Turn confirmed user stories into formal EARS requirements in `specs/<NNN>-<feature>/spec.md`. Each requirement carries a unique REQ-ID, a Given/When/Then acceptance criterion, and a valid `source_legacy:` line, so the `legacy-traceability` CI job passes on the first push.

## When to Invoke

At the start of Stage 2, after the pair has read its assigned Natural programs (the HARD GATE in `01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`) and the team has agreed on one narrow feature.

## Preconditions

- `specs/<NNN>-<feature>/` exists (created by the Specify CLI)
- `.specify/memory/constitution.md` exists
- `01-archaeology/business-rules-catalog.md` holds the confirmed rules with their source line ranges
- The pair has actually read the legacy files it intends to cite

## Inputs the Team Must Provide

- `feature=<NNN>-<feature>` — the folder under `specs/`
- The user stories or confirmed business rules to formalize (a path or inline text)
- For each story, its legacy source: a `01-archaeology/legacy-sifap/natural-programs/*.{NSP,NSN,NSS,NSA,NSL,NSC,NSM,jcl}` or `01-archaeology/legacy-sifap/adabas-ddms/*.{NSD,ddm,txt}` path, or an explicit `[GREENFIELD]` justification
- Ask the user for anything that is missing.

## What I Will Do

- Read `.specify/memory/constitution.md` and list the constraints that touch this feature
- Read each cited legacy file before wording any requirement
- Refine raw stories with the [`user-story-refine`](../skills/user-story-refine/SKILL.md) skill (INVEST, vertical slices)
- Classify each requirement by EARS pattern with the [`ears-validate`](../skills/ears-validate/SKILL.md) skill
- Assign unique REQ-IDs in the `REQ-<DOMAIN>-NNN` form
- Attach a `source_legacy:` line to every requirement
- Write Given/When/Then acceptance criteria and mark out-of-scope items

## What I Will NOT Do

- Write an EARS requirement without a `source_legacy:` line — I ask for the source or a `[GREENFIELD]` marker and stop
- Invent what a Natural program or DDM field contains — I read the file or ask the team, never recall it
- Point `source_legacy:` at `legacy-docs/*.md` — the gate accepts only `natural-programs` and `adabas-ddms` paths, or `[GREENFIELD]`
- Convert an unvalidated hypothesis or open question into a requirement
- Sweep the whole spec for cross-requirement contradictions — that is `/contradiction-check` on `@requirements-engineer`

## Output Format

Append EARS blocks to `specs/<NNN>-<feature>/spec.md`. The `REQ-ID:` key and the `source_legacy:` line within 20 lines of it are what the CI gate parses.

```yaml
REQ-PAY-014:
  pattern: unwanted
  text: "If a payment line references a beneficiary that is not active, then the system shall reject the line and record the rejection reason."
  source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L<start>-L<end>
  acceptance:
    - "Given an inactive beneficiary, when the batch processes the line, then the line is rejected with reason INACTIVE_BENEFICIARY."
  priority: P0

REQ-AUTH-001:
  pattern: unwanted
  text: "If a user submits invalid credentials three times in a row, then the system shall lock the account for 15 minutes."
  source_legacy: "[GREENFIELD] Authentication and lockout have no equivalent in the batch-oriented legacy system."
  acceptance:
    - "Given three consecutive failed logins, when a fourth attempt occurs, then the system responds 423 Locked."
  priority: P1
```

> [!NOTE]
> The wording above is illustrative. The `<PROGRAM>` and `<start>`/`<end>` tokens must be replaced with the real file and line range the team read — the model never fills them from memory.

## Definition of Done

- [ ] Every story is expressed as an EARS requirement with exactly one pattern
- [ ] Every requirement has a unique REQ-ID in `REQ-<DOMAIN>-NNN` (or `REQ-NNN`) form
- [ ] Every requirement has a valid `source_legacy:` line within 20 lines of its REQ-ID (a real `natural-programs`/`adabas-ddms` path, or `[GREENFIELD]` + justification)
- [ ] Every requirement has at least one Given/When/Then acceptance criterion
- [ ] No requirement contradicts `.specify/memory/constitution.md`
- [ ] Assumptions and out-of-scope items are stated explicitly
- [ ] Open questions remain questions, not requirements

## Prompt Body

You are the `@product-owner`. The team has agreed on a narrow feature and brings user stories to formalize.

**Step 1 — Confirm the feature and read the constraints.**
Open `specs/<NNN>-<feature>/spec.md` (if it exists) and `.specify/memory/constitution.md`. List the constitutional rules that constrain this feature.

**Step 2 — Demand a legacy source for every story.**
For each story or rule, require a `natural-programs` or `adabas-ddms` path (ideally with `#L<start>-L<end>`) or an explicit `[GREENFIELD]` justification. If a story has neither, stop and ask; do not draft it.

**Step 3 — Read the cited legacy files.**
Open each cited `.NSP`, `.NSN`, `.ddm`, or `.txt` file and confirm the behavior before wording the requirement. Never infer a rule from a filename.

**Step 4 — Refine the stories.**
Apply the [`user-story-refine`](../skills/user-story-refine/SKILL.md) skill: INVEST, one outcome per story, vertical slices.

**Step 5 — Formalize in EARS.**
Use the [`ears-validate`](../skills/ears-validate/SKILL.md) patterns. Exactly one pattern per requirement. Split any hidden "and" into separate requirements.

**Step 6 — Assign REQ-IDs and traceability.**
Give each requirement a unique `REQ-<DOMAIN>-NNN`. Put the `source_legacy:` line directly under the REQ-ID, and add Given/When/Then acceptance criteria.

**Step 7 — Flag and defer.**
Record ambiguities, contradictions with the constitution, and out-of-scope items. Route a full contradiction sweep to `/contradiction-check`.

No requirement ships without a `source_legacy:` line; the `legacy-traceability` CI job rejects the PR otherwise, and `legacy-docs/*.md` is not an accepted source. Never invent legacy behavior — if you have not read the file, say so and ask.

## Invocation Example

```
/spec feature=001-pagamento-beneficio stories=02-modern-spec/user-stories.md
```
