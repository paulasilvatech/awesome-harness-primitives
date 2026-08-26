---
name: 'modernize-extract-rules'
description: 'Extract cited and testable business rule cards from legacy code, modules, or business processes.'
agent: 'modernization'
argument-hint: 'legacy folder, module, or business process'
---

# /modernize-extract-rules

## Objective

Extract cited, plain-language, and testable business rule cards from a legacy folder, module, or business process, converting calculations, validations, eligibility checks, authorizations, policies, and state transitions into rules with source evidence, Given/When/Then examples, confidence, and SME questions.

## When to Invoke

Use this prompt after `modernize-assess` has identified the relevant system or module, and before `modernize-map`, `modernize-reimagine`, or `modernize-transform` need behavior evidence.

## Preconditions

- The target legacy folder, module, or business process is available.
- Source files or process documents can be inspected for rule evidence.
- Writing to `analysis/<system>/RULES.md` is permitted.
- The `code-modernization` skill is available.
- The legacy source remains read-only unless the user separately approves changes outside this prompt.

## Inputs the Team Must Provide

- `target` — the legacy folder, module, or business process to mine for rules.
- The system name used for `analysis/<system>/RULES.md`.
- Any known terminology, SME contact path, or rule priority.
- Ask the user for anything that is missing; stop if the source location or system name cannot be determined.

## What I Will Do

- Load the `code-modernization` skill before extracting rules.
- Load `legacy-business-rule-extraction` for evidence states, rule-card shape, confidence, and SME questions.
- Locate calculations, validations, eligibility checks, authorizations, policies, and state transitions.
- Cite each rule with source file evidence.
- Convert each rule into plain language and Given/When/Then examples with concrete values.
- Mark confidence and unresolved SME questions.
- Write `analysis/<system>/RULES.md`.

## What I Will NOT Do

- Modify legacy code, modernized code, configuration, data, or tests.
- Treat an uncited behavior as an approved business rule.
- Invent concrete example values when the source gives no basis; I will label placeholders or SME questions.
- Collapse distinct calculations, validations, eligibility checks, authorizations, policies, or state transitions into one vague rule.
- Design the target architecture or implement behavior; `modernize-reimagine` and `modernize-transform` own those stages.

## Output Format

Write `analysis/<system>/RULES.md` with this shape:

```markdown
# Business Rules — <system>

## Summary
- Source scope:
- Rule count:
- Low-confidence count:

## Rule Cards

### RULE-001 — <short rule name>
- Type: calculation | validation | eligibility | authorization | policy | state-transition
- Plain language:
- Source evidence:
  - `<path>` — <line, symbol, paragraph, or inspected evidence>
- Given/When/Then examples:
  - Given <concrete state>
    When <event or input>
    Then <expected outcome>
- Confidence: high | medium | low
- SME questions:
  - 

## Cross-Rule Notes
- 

## Low-Confidence Questions
| Rule | Question | Why it matters | Owner |
| --- | --- | --- | --- |
```

## Definition of Done

- [ ] The `code-modernization` skill was loaded before extraction started.
- [ ] Calculations, validations, eligibility checks, authorizations, policies, and state transitions were searched.
- [ ] Every rule has source file evidence or is excluded from the approved rule set.
- [ ] Each rule includes plain language and at least one Given/When/Then example with concrete values when evidence supports them.
- [ ] Confidence and unresolved SME questions are recorded.
- [ ] `analysis/<system>/RULES.md` exists.
- [ ] The response returns only the artifact path, rule count, low-confidence questions, validation status, and blockers.

## Prompt Body

Follow these steps in order. Preserve behavior evidence and avoid target-design decisions.

**Step 1 — Load the modernization workflow.**
Load the `code-modernization` and `legacy-business-rule-extraction` skills before mining rules.

**Step 2 — Resolve the source scope.**
Read `${input:target:legacy folder, module, or business process}` and determine the system name for `analysis/<system>/RULES.md`. Ask for missing scope before continuing.

**Step 3 — Mine rule candidates.**
Search for calculations, validations, eligibility checks, authorizations, policies, and state transitions. Keep paths and symbols attached to every candidate.

**Step 4 — Convert candidates to rule cards.**
Write each rule in plain language. Add Given/When/Then examples with concrete values. Split unrelated behaviors into separate rule cards.

**Step 5 — Attach evidence and confidence.**
Cite source file evidence for each rule. Mark confidence as high, medium, or low. Convert ambiguous behavior into unresolved SME questions.

**Step 6 — Write the artifact.**
Write the rule cards to `analysis/<system>/RULES.md`. Keep the file structured so `modernize-map`, `modernize-reimagine`, and `modernize-transform` can consume it.

**Step 7 — Report concisely.**
Return only the artifact path, rule count, low-confidence questions, validation status, and blockers.

## Invocation Example

```
/modernize-extract-rules target=legacy folder, module, or business process
```
