---
name: "open-horizons-ears-validate"
description: "Use when validating requirements against EARS notation patterns. Triggers include \"EARS\", \"requirement review\", \"requirement quality\", \"shall statement\", and \"REQ-ID\"."
---
# EARS validation

## When to invoke

- "Review these requirements for EARS compliance."
- "Is this requirement testable?"
- "Classify this requirement by EARS pattern."

## EARS patterns

| Pattern | Template |
| --- | --- |
| Ubiquitous | `The <system> shall <response>.` |
| Event-driven | `When <trigger>, the <system> shall <response>.` |
| State-driven | `While <state>, the <system> shall <response>.` |
| Optional | `Where <feature is included>, the <system> shall <response>.` |
| Unwanted | `If <undesired condition>, then the <system> shall <mitigation>.` |
| Complex | `While <state>, when <trigger>, the <system> shall <response>.` |

## Validation checklist

- [ ] Exactly one pattern per requirement.
- [ ] Unambiguous subject ("the system", not "it").
- [ ] Observable and testable response.
- [ ] No hidden "and" that combines two requirements into one.
- [ ] Implementation constraints appear only when they are approved architecture or platform boundaries.
- [ ] Generated AEG-native FRD/NFRD requirements use a unique `FR-<DOMAIN>-NNN` or `NFR-<DOMAIN>-NNN` ID; a platform contract SDD may use stable domain IDs only when `DECISIONS.md` and `SOURCE_TRACEABILITY.md` define the scheme, compatibility, and supersession rules.
- [ ] Includes at least one acceptance criterion.
- [ ] Includes a source entry in `SOURCE_TRACEABILITY.md` that identifies evidence or records `[GREENFIELD]` with a justification.

## Common defects

| Defect | Example | Correction |
| --- | --- | --- |
| Ambiguous | "The system must be fast." | "When a user submits a form, the system shall respond within 500ms." |
| Compound | "Log in and send an email." | Split into two requirements. |
| Not testable | "The system shall be easy to use." | Replace with a measurable UX metric. |
| Passive | "Login shall be supported." | "The system shall accept username/password authentication." |

## Output template

```markdown
### FR-DOMAIN-NNN: <title> (<pattern>)
<EARS statement>

**Priority:** P0 / P1 / P2

**Acceptance criteria (EARS):**
- AC-FR-DOMAIN-NNN-01 (<pattern>): <criterion 1>
- AC-FR-DOMAIN-NNN-02 (<pattern>): <criterion 2>

**Source traceability:** `<evidence reference>` or `[GREENFIELD] <justification>` in `SOURCE_TRACEABILITY.md`
```

## Quality gate

- [ ] Every generated AEG-native FRD/NFRD requirement has a unique `FR-<DOMAIN>-NNN` or `NFR-<DOMAIN>-NNN` ID; platform-contract or preserved historical IDs have an explicit decision and compatibility record.
- [ ] Every requirement is classified under exactly one EARS pattern.
- [ ] Every requirement has at least one testable acceptance criterion.
- [ ] Every acceptance criterion has a unique `AC-<REQ-ID>-NN` ID and one EARS pattern.
- [ ] Every requirement is covered by `SOURCE_TRACEABILITY.md` with verifiable evidence or a justified `[GREENFIELD]` entry.
- [ ] Measurable targets come from observed evidence or an accountable-owner-approved objective; unresolved targets remain blockers instead of being invented.
- [ ] The repository's SDD and traceability validators pass for the change.
