---
name: "build-evidence-map"
description: >-
  Build auditable evidence maps for contested technical choices, research synthesis, proposal review, and consequential decisions. Use this skill when GitHub Copilot must preserve supporting, contradicting, qualifying, and missing evidence with exact source regions instead of collapsing disagreement into prose.
---

# Build evidence map

Turn one contested question into a portable `.doubt.json` decision artifact that preserves the current position, evidence, counterevidence, qualifications, and unknowns with exact source regions and deterministic validation.

## When to invoke

- "Build an evidence map for this architecture decision."
- "Preserve the evidence for and against this proposal."
- "Map the sources behind this contested technical choice."
- "Show supporting, contradicting, qualifying, and missing evidence."
- "Create a .doubt.json decision artifact."

## Prerequisites and context

- Use this for contested decisions where relationships between evidence, claims, trade-offs, and missing facts matter.
- For a simple factual claim or general fact-checking request, use a verification workflow such as `doublecheck` instead.
- Validate with the bundled `scripts/validate.mjs`; it uses only Node.js built-ins and requires Node.js 18 or newer.
- Read `references/evidence-ladder.md` when source quality is disputed and `references/map-schema.md` before writing JSON.

## Procedure

1. Frame one decision: write one falsifiable question and one provisional position narrow enough that a reader can identify the action or belief being tested.
2. Collect bounded source regions. Prefer direct observations and primary sources. Record URL or absolute local path, publisher, publication date, retrieval date, section/page/line/timestamp locator, and a short checkable excerpt.
3. Atomize reasoning into exactly four node types: `position`, `claim`, `evidence`, and `unknown`.
4. Type every edge as `supports`, `contradicts`, `qualifies`, or `missing`, with a plain-language note explaining why the source node bears on the target.
5. Preserve counterevidence. Do not delete contrary evidence because the provisional verdict survives it; use `qualifies` for scope, date, or population differences.
6. Express uncertainty structurally. Do not invent confidence percentages; add an `unknown`, narrow the position, or qualify a claim.
7. Write UTF-8 JSON with a `.doubt.json` suffix following `references/map-schema.md`; keep IDs short, stable, and semantic.
8. Resolve `scripts/validate.mjs` relative to this `SKILL.md`, then run:

   ```bash
   node <skill-directory>/scripts/validate.mjs decision.doubt.json
   ```

   Fix every finding before reporting success. Only say the map is valid when the command exits `0` and prints `VALID` followed by a 64-character receipt. A file hash, node count, JSON parse, or manual schema review is not a Doubt receipt.
9. Render only when the user has already installed `doubt-ai@0.8.0`; do not install or execute a remote package implicitly:

   ```bash
   doubt map decision.doubt.json --out decision.html
   ```

10. Verify HTTP(S) source snapshots only with explicit network permission:

   ```bash
   doubt verify decision.doubt.json      --out decision.verified.doubt.json
   ```

   Never run this command implicitly. Local file verification does not use the network. Do not write a `verification` object by hand or hide a mismatch.
11. Inspect the deliverable. Confirm that the question, verdict, counterevidence, unknowns, edge notes, and exact source regions remain readable. Treat JSON as canonical; HTML is only a shareable view.

## Evidence model

| Node type | Meaning | Rule |
| --- | --- | --- |
| `position` | The single current verdict. | Exactly one position has incoming reasoning. |
| `claim` | Intermediate proposition. | Must have a directed path to the position. |
| `evidence` | Faithful statement of one bounded source region. | Names one source, includes dates and locator, and participates in an edge. |
| `unknown` | Specific missing fact that could change the verdict. | Use instead of unsupported certainty or invented percentages. |

| Edge type | Use when | Common mistake |
| --- | --- | --- |
| `supports` | The source node increases the plausibility of the target under the same scope. | Treating topical similarity as support. |
| `contradicts` | The source node directly pushes against the target under comparable scope. | Calling different date/population/scope a contradiction without explanation. |
| `qualifies` | The source narrows, conditions, or limits the target. | Deleting inconvenient evidence. |
| `missing` | An unknown facts blocks or limits the conclusion. | Hiding a decision-changing gap in prose. |

## Validation rules

- Exactly one `position` has incoming reasoning.
- Every evidence node names one source and participates in an edge.
- Every source is used and has dates, a bounded locator, and a substantive excerpt.
- Every non-position node has a directed path to the position.
- The reasoning graph has no duplicate edges or directed cycles.
- Contrary or qualifying evidence is present when the source set contains it.
- Each decision-changing gap is an explicit `unknown` node.
- Every edge note explains support, contradiction, qualification, or absence.
- The verdict is no broader than the evidence.

## Limits

- Do not use a graph to decorate an answer that has not been sourced.
- Do not describe a structurally valid map as proven true; validation establishes traceability and graph integrity, not truth.
- Do not install `doubt-ai@0.8.0` or run `doubt map` unless the user already has it installed.
- Do not run `doubt verify` against HTTP(S) sources without explicit network permission.

## Progressive disclosure and bundled resources

- `references/evidence-ladder.md`: source quality guidance when evidence strength is disputed.
- `references/map-schema.md`: canonical `.doubt.json` schema and field rules.
- `scripts/validate.mjs`: deterministic validator that prints `VALID` and a 64-character receipt on success.
- `scripts/contract.mjs`: shared validation contract used by the bundled validator.

Validation must fail-closed: if the receipt cannot be produced, report the block instead of weakening the gate.

## Output template

```markdown
## Evidence map result

**Status:** valid | draft | blocked
**Question:** <falsifiable decision question>
**Current position:** <one-sentence verdict>
**Canonical JSON:** `<path>.doubt.json`
**Rendered HTML:** `<path>.html or not rendered>`

| Required element | Result |
| --- | --- |
| Strongest counterevidence or qualification | `<summary>` |
| Most important unresolved unknown | `<unknown>` |
| Deterministic validation | `<VALID receipt or blocker>` |
| Source verification | `<explicitly run / not requested / blocked>` |

**Notes**
- <source quality or inference caveat>
```

## Quality gate

- [ ] One falsifiable decision question and one provisional position were framed.
- [ ] Every source region includes URL or absolute local path, publisher, publication date, retrieval date, locator, and excerpt.
- [ ] Only `position`, `claim`, `evidence`, and `unknown` nodes are used.
- [ ] Every edge is `supports`, `contradicts`, `qualifies`, or `missing` and has an explanatory note.
- [ ] Counterevidence and qualifications were preserved structurally.
- [ ] Unknowns capture decision-changing gaps instead of invented confidence percentages.
- [ ] The map is UTF-8 JSON, ends with `.doubt.json`, and follows `references/map-schema.md`.
- [ ] `node <skill-directory>/scripts/validate.mjs decision.doubt.json` exited `0` and printed `VALID` plus a 64-character receipt, or the blocker is reported.
- [ ] `doubt verify` was run only with explicit network permission, and no `verification` object was written by hand.
