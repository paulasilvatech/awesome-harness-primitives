---
name: 'cobol-db2-archaeology'
description: 'Map a complete COBOL/DB2 corpus into the engineering graph, then analyze one bounded scope and write cited inventory, dependency, rule-candidate, and open-question artifacts.'
argument-hint: 'corpus=01-archaeology/legacy scope=01-archaeology/legacy/<path>'
agent: 'cobol-db2-archaeologist'
---

# /cobol-db2-archaeology

## Objective

Map the whole COBOL/DB2 corpus, then analyze one bounded scope in depth and update archaeology artifacts
without modifying legacy source.

## When to Invoke

Use during archaeology after the team selects a program, copybook area, batch flow, or bounded folder.

## Preconditions

- The corpus root and the scope exist under the target repository.
- Artifact edits outside the legacy subtree are approved.
- The `cobol-db2-context`, `cobol-db2-loop`, `cobol-db2-analysis`, and
  `legacy-business-rule-extraction` skills are available.

Stop if the corpus root or the source scope is missing or ambiguous.

## Inputs the Team Must Provide

- `corpus` - the legacy corpus root, so the whole system is mapped before one part is read.
- `scope` - exact legacy file or bounded directory to read in depth.
- The target artifact paths, or approval to use existing archaeology conventions.
- Any known domain owner for unresolved questions.

## What I Will Do

- Load the required Skills.
- Extract the complete corpus into the slice graph and report unresolved references, unreferenced members, and dependency order.
- Inspect divisions, copybooks, calls, embedded SQL, cursors, datasets, JCL steps, empty results, and error paths for the selected scope.
- Update cited inventory, dependency, rule-candidate, and open-question artifacts.
- Verify that no legacy source changed.

## What I Will NOT Do

- Modify legacy source or generate approved requirements.
- Resolve a dynamic `CALL` by guessing its target.
- Report a corpus as mapped when extraction left unresolved references unanswered.
- Create arbitrary output-count targets.
- Write outside approved archaeology artifact paths.

## Output Format

```markdown
## COBOL/DB2 archaeology update

**Status:** complete | partial | blocked
**Scope:** <path>

### Corpus coverage
| Recognized files | Graph nodes | Unresolved notes |
| --- | --- | --- |

### Artifacts changed
- <path and purpose>

### Evidence coverage
| Concern | Evidence | Result |
| --- | --- | --- |

### Open questions
| Question | Evidence | Impact | Owner |
| --- | --- | --- | --- |
```

## Definition of Done

- [ ] All required Skills were loaded.
- [ ] The selected scope and writable artifact paths are explicit.
- [ ] Every corpus member is a graph node, and unresolved extraction notes are answered or accepted.
- [ ] Claims and rule candidates cite inspected source evidence with line anchors.
- [ ] Missing dependencies and ambiguous meaning remain open questions.
- [ ] No legacy or unapproved file changed.
- [ ] Validation evidence and blockers are reported.

## Prompt Body

1. **Validate the scope.** Resolve `corpus` and `scope` plus approved destinations; stop if any is unclear.
2. **Load context and procedure.** Load the required Skills and only their task-relevant references.
3. **Map the whole corpus.** Extract every member into the graph, then review unresolved notes, `dead-legacy`, and `slice-order` before reading anything in depth.
4. **Inspect evidence.** Trace divisions, copybooks, calls, SQL access, cursors, datasets, JCL steps, and error paths for `scope`.
5. **Update artifacts.** Write only approved inventory, dependency, rule-candidate, and question files.
6. **Validate.** Confirm source citations resolve and the legacy subtree is unchanged.
7. **Report.** Return changed paths, corpus coverage, evidence coverage, questions, checks, and blockers.

## Invocation Example

```text
/cobol-db2-archaeology corpus=01-archaeology/legacy scope=01-archaeology/legacy/cobol/PAY0100.CBL
```

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `cobol-db2-archaeologist` | agent | Owns archaeology judgment and evidence coverage. |
| `cobol-db2-loop` | skill | Extracts the corpus, evaluates the archaeology gate, and records the ledger. |
| `cobol-db2-specify` | prompt | Consumes approved archaeology evidence in the architecture stage. |
