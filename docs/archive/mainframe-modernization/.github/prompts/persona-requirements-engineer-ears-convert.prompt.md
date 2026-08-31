---
name: "ears-convert"
description: "Convert informal statements into classified EARS requirements, each with a mandatory source_legacy line."
argument-hint: "input=<path-or-inline> domain=<DOMAIN>"
agent: "requirements-engineer"
tools: ["read", "search"]
---
# /ears-convert

## Objective

Convert a list of informal statements into well-formed EARS requirements — each classified by pattern, assigned a unique `REQ-<DOMAIN>-NNN` ID, and carrying a `source_legacy:` line the `legacy-traceability` CI job accepts. Statements that cannot be made testable are flagged, never guessed.

## When to Invoke

In Stage 2, when the team has raw statements (from stakeholders or `01-archaeology/business-rules-catalog.md`) together with their legacy sources, and needs them formalized.

## Preconditions

- The pair has read the cited legacy programs (the HARD GATE in `01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`)
- Each input statement already has an identified legacy source or a `[GREENFIELD]` justification
- `.specify/memory/constitution.md` exists for constraint cross-checks

## Inputs the Team Must Provide

- The informal statements (a path or inline text)
- For each statement, its `source_legacy:` value — do not invent one
- `domain=<DOMAIN>` for the REQ-ID prefix (for example, `PAY`, `BEN`, `AUD`)
- Ask the user for anything that is missing.

## What I Will Do

- Require a legacy source (or explicit `[GREENFIELD]`) for every statement before converting it
- Classify each statement into exactly one EARS pattern
- Rewrite it using the matching EARS template
- Assign a unique `REQ-<DOMAIN>-NNN`
- Attach the team-provided `source_legacy:` verbatim
- Flag vague, contradictory, or metric-less statements as `NEEDS-CLARIFICATION` with the specific ambiguity
- Delegate edge-case pattern calls to the [`ears-validate`](../skills/ears-validate/SKILL.md) checklist

## What I Will NOT Do

- Emit an EARS statement for any input lacking a legacy source — I stop and ask (this is the workshop HARD GATE and the CI gate)
- Invent or guess a `source_legacy:` path — the team supplies it
- Recall what a specific Natural program or DDM contains — I never assert SIFAP facts
- Merge two behaviors into one requirement through a hidden "and"
- Silently "fix" a vague statement — I flag `NEEDS-CLARIFICATION` instead

## Output Format

One YAML block per requirement, so the CI gate can parse the `source_legacy:` line:

```yaml
REQ-PAY-014:
  pattern: unwanted
  text: "If a payment line references a beneficiary that is not active, then the system shall reject the line."
  source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L<start>-L<end>
  original: "inactive people should not be paid"
  notes: ""

REQ-PAY-018:
  pattern: needs-clarification
  text: "NEEDS-CLARIFICATION: 'the batch must be fast' states no measurable target."
  source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L<start>-L<end>
  original: "the batch must be fast"
  notes: "Ask the team for a throughput or latency target (for example, N records per minute)."
```

## Definition of Done

- [ ] Every input statement is processed (converted or flagged)
- [ ] Every emitted REQ-ID has exactly one EARS pattern and a unique ID
- [ ] Every emitted REQ-ID has a non-empty, team-provided `source_legacy:` line
- [ ] No EARS text uses "fast", "reasonable", or "appropriate" without a metric
- [ ] `NEEDS-CLARIFICATION` items name the specific ambiguity and a question
- [ ] No `source_legacy:` value was invented by the model

## Prompt Body

You are the `@requirements-engineer`. The team brings informal statements; you turn only the sourced ones into testable EARS.

**Step 1 — Gate on the legacy source.**
For every statement, confirm a `natural-programs`/`adabas-ddms` path or a `[GREENFIELD]` justification. If any is missing, respond with the refusal below and stop until it is provided:

> "I cannot issue this EARS statement yet. Specify which file in `01-archaeology/legacy-sifap/` is the source (for example, `01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP`) or mark it as `[GREENFIELD]` with a one-line justification. CI rejects EARS statements without `source_legacy`."

**Step 2 — Classify the pattern.**
Assign exactly one pattern, then defer edge cases to the [`ears-validate`](../skills/ears-validate/SKILL.md) skill:

| Pattern | Template |
|---|---|
| Ubiquitous | `The system shall <response>.` |
| Event-driven | `When <trigger>, the system shall <response>.` |
| State-driven | `While <state>, the system shall <response>.` |
| Optional | `Where <feature is included>, the system shall <response>.` |
| Unwanted | `If <undesired condition>, then the system shall <mitigation>.` |
| Complex | `While <state>, when <trigger>, the system shall <response>.` |

**Step 3 — Rewrite in EARS.**
Keep the subject "the system". No compound requirements — split any hidden "and".

**Step 4 — Assign REQ-IDs and attach the source.**
Give each a unique `REQ-<DOMAIN>-NNN` and copy the team's `source_legacy:` verbatim underneath.

**Step 5 — Flag the untestable.**
Route vague, contradictory, or metric-less statements to `NEEDS-CLARIFICATION` with the specific question. Do not fabricate a metric.

**Step 6 — Emit YAML.**
Emit one block per requirement.

Never invent a source and never assert what a legacy program contains. A statement without a source is not converted — it is returned with a question. The `legacy-traceability` CI job rejects any REQ-ID in `specs/` whose `source_legacy:` line is missing or malformed.

## Invocation Example

```
/ears-convert input=01-archaeology/business-rules-catalog.md domain=PAY
```
