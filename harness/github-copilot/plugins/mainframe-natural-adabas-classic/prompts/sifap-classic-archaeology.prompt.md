---
name: 'sifap-classic-archaeology'
description: 'Analyze one bounded SIFAP Natural/Adabas scope and write cited inventory, dependency, rule-candidate, and open-question artifacts.'
argument-hint: 'scope=01-archaeology/legacy-sifap/<path>'
agent: 'sifap-classic-archaeologist'
---

# /sifap-classic-archaeology

## Objective

Analyze one bounded SIFAP legacy scope and update Stage 1 artifacts without modifying legacy source.

## When to Invoke

Use during Stage 1 after the team selects a Natural member, DDM/FDT area, batch flow, or bounded folder.

## Preconditions

- The scope exists under the target repository's SIFAP legacy corpus.
- Stage 1 artifact edits outside the legacy subtree are approved.
- The `sifap-classic-context`, `natural-adabas-analysis`, and
  `legacy-business-rule-extraction` skills are available.

Stop if the source scope is missing or ambiguous.

## Inputs the Team Must Provide

- `scope` - exact legacy file or bounded directory.
- The target Stage 1 artifact paths, or approval to use existing Stage 1 conventions.
- Any known domain owner for unresolved questions.

## What I Will Do

- Load the three required Skills.
- Inspect declarations, dependencies, data access, mutations, errors, and negative paths.
- Update cited inventory, dependency, rule-candidate, and open-question artifacts.
- Verify that no legacy source changed.

## What I Will NOT Do

- Modify legacy source or generate approved requirements.
- Infer missing member behavior or domain meaning.
- Create arbitrary output-count targets.
- Write outside approved Stage 1 artifact paths.

## Output Format

```markdown
## SIFAP archaeology update

**Status:** complete | partial | blocked
**Scope:** <path>

### Artifacts changed
- <path and purpose>

### Evidence coverage
| Concern | Evidence | Result |
| --- | --- | --- |

### Open questions
| Question | Evidence | Impact | Owner |
| --- | --- | --- | --- |

### Validation
- Legacy source changed: no
- Artifact checks: <actual checks>
```

## Definition of Done

- [ ] All required Skills were loaded.
- [ ] The selected scope and writable artifact paths are explicit.
- [ ] Claims and rule candidates cite inspected source evidence.
- [ ] Missing dependencies and ambiguous meaning remain open questions.
- [ ] No legacy or unapproved file changed.
- [ ] Validation evidence and blockers are reported.

## Prompt Body

1. **Validate the scope.** Resolve `scope` and approved Stage 1 destinations; stop if either is unclear.
2. **Load context and procedure.** Load the three required Skills and only their task-relevant references.
3. **Inspect evidence.** Trace declarations, calls, data definitions, access, mutation, errors, and negative paths.
4. **Update artifacts.** Write only approved Stage 1 inventory, dependency, rule-candidate, and question files.
5. **Validate.** Confirm source citations resolve and the legacy subtree is unchanged.
6. **Report.** Return changed paths, evidence coverage, questions, checks, and blockers.

## Invocation Example

```text
/sifap-classic-archaeology scope=01-archaeology/legacy-sifap/natural-programs/PAYMENT.NSN
```

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `sifap-classic-archaeologist` | agent | Owns Stage 1 judgment and evidence coverage. |
| `sifap-classic-specify` | prompt | Consumes approved archaeology evidence in Stage 2. |
