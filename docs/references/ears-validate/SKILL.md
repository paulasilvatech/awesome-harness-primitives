---
name: "ears-validate"
description: "Use when validating requirements against EARS notation patterns. Triggers include \"EARS\", \"requirement review\", \"requirement quality\", \"shall statement\", and \"REQ-ID\"."
---
# EARS validation

## When to invoke

- "Review these requirements for EARS compliance."
- "Is this requirement testable?"
- "Classify this requirement by EARS pattern."

## EARS patterns

| Pattern | Template |
|---|---|
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
- [ ] No implementation details ("use Redis"), only behavior.
- [ ] Includes a REQ-ID in the `REQ-NNN` format.
- [ ] Includes at least one acceptance criterion.
- [ ] **Includes a non-empty `source_legacy:` pointing to `01-archaeology/legacy-sifap/natural-programs/*.NSN`, `01-archaeology/legacy-sifap/adabas-ddms/*.ddm`, or `[GREENFIELD] + justification`.**

## Common defects

| Defect | Example | Correction |
|---|---|---|
| Ambiguous | "The system must be fast." | "When a user submits a form, the system shall respond within 500ms." |
| Compound | "Log in and send an email." | Split into two requirements. |
| Not testable | "The system shall be easy to use." | Replace with a measurable UX metric. |
| Passive | "Login shall be supported." | "The system shall accept username/password authentication." |

## Output template

```markdown
### REQ-NNN (<pattern>)
<EARS statement>

source_legacy: 01-archaeology/legacy-sifap/natural-programs/<FILE>.NSN#L<start>-L<end>
_(or `[GREENFIELD] <justification>` when there is no legacy equivalent)_

**Acceptance criteria**
- <criterion 1>
- <criterion 2>

**Traced from**: US-NNN, ADR-NNN
**Priority**: P0 / P1 / P2
**Status**: proposed / approved / implemented / verified
```

## Quality gate

- [ ] Every requirement has a unique REQ-ID in `REQ-NNN` format.
- [ ] Every requirement is classified under exactly one EARS pattern.
- [ ] Every requirement has at least one testable acceptance criterion.
- [ ] Every requirement has a `source_legacy:` line pointing to a real legacy file or `[GREENFIELD] <justification>`.
- [ ] The `legacy-traceability` job in `.github/workflows/spec-quality.yml` passes for the PR.
