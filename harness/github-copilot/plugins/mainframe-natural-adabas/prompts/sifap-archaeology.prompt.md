---
name: 'sifap-archaeology'
description: 'Analyze one bounded SIFAP Natural/Adabas scope and write cited inventory, dependency, rule-candidate, and open-question artifacts.'
argument-hint: 'corpus=01-archaeology/legacy-sifap scope=01-archaeology/legacy-sifap/<path>'
agent: 'sifap-archaeologist'
---

# /sifap-archaeology

## Objective

Analyze one bounded SIFAP legacy scope and update Stage 1 artifacts without modifying legacy source.

## When to Invoke

Use during Stage 1 after the team selects a Natural member, DDM/FDT area, batch flow, or bounded folder.

## Preconditions

- The scope exists under the target repository's SIFAP legacy corpus.
- Stage 1 artifact edits outside the legacy subtree are approved.
- The `sifap-modernization-context`, `sifap-loop`, `natural-adabas-analysis`, and
  `legacy-business-rule-extraction` skills are available.

Stop if the source scope is missing or ambiguous.

## Inputs the Team Must Provide

- `corpus` - the legacy corpus root, so the whole system is mapped before one part is read.
- `scope` - exact legacy file or bounded directory to read in depth.
- The target Stage 1 artifact paths, or approval to use existing Stage 1 conventions.
- Any known domain owner for unresolved questions.

## What I Will Do

- Load the required Skills.
- Extract the complete corpus into the slice graph and report unresolved references, unreferenced members, and dependency order.
- Inspect declarations, dependencies, data access, mutations, errors, and negative paths for the selected scope.
- Update cited inventory, dependency, rule-candidate, and open-question artifacts.
- Verify that no legacy source changed.

## What I Will NOT Do

- Modify legacy source or generate approved requirements.
- Infer missing member behavior or domain meaning.
- Report a corpus as mapped when extraction left unresolved references unanswered.
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
- [ ] Every corpus member is a graph node, and unresolved extraction notes are answered or accepted.
- [ ] Claims and rule candidates cite inspected source evidence.
- [ ] Missing dependencies and ambiguous meaning remain open questions.
- [ ] No legacy or unapproved file changed.
- [ ] Validation evidence and blockers are reported.

## Prompt Body

1. **Validate the scope.** Resolve `corpus` and `scope` plus approved Stage 1 destinations; stop if any is unclear.
2. **Load context and procedure.** Load the required Skills and only their task-relevant references.
3. **Map the whole corpus.** Extract every member into the graph, then review unresolved notes, `dead-legacy`, and `slice-order` before reading anything in depth.
4. **Inspect evidence.** Trace declarations, calls, data definitions, access, mutation, errors, and negative paths for `scope`.
5. **Update artifacts.** Write only approved Stage 1 inventory, dependency, rule-candidate, and question files.
6. **Validate.** Confirm source citations resolve and the legacy subtree is unchanged.
7. **Report.** Return changed paths, corpus coverage, evidence coverage, questions, checks, and blockers.

## Invocation Example

```text
/sifap-archaeology corpus=01-archaeology/legacy-sifap scope=01-archaeology/legacy-sifap/natural-programs/PAYMENT.NSN
```

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `sifap-archaeologist` | agent | Owns Stage 1 judgment and evidence coverage. |
| `sifap-loop` | skill | Extracts the corpus, evaluates the archaeology gate, and records the ledger. |
| `sifap-specify` | prompt | Consumes approved archaeology evidence in Stage 2. |
