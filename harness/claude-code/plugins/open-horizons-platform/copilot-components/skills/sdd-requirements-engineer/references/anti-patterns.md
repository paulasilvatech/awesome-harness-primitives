# SDD and EARS anti-patterns

Use this catalog during repair and validation. Fix the underlying requirement, evidence, or traceability defect rather than polishing only the prose.

## Requirement defects

| Anti-pattern | Why it fails | Corrective action |
| --- | --- | --- |
| User story treated as a requirement | Intent is not a normative system response. | Preserve the story as context and derive one or more EARS requirements. |
| `should`, `may`, `will`, or vague `must` | Obligation or timing is ambiguous. | Use the appropriate EARS pattern with `shall`. |
| Compound response joined by `and` | One change or test can pass while another fails. | Split into atomic requirements with separate IDs. |
| Pronoun subject such as "it" | The responsible system boundary is unclear. | Name the system or component. |
| Hidden trigger or state | Reviewers must infer when behavior applies. | Add `when`, `while`, `where`, or `if...then` clauses. |
| Technology in a functional requirement | Behavior and implementation become coupled. | Move a sourced mandatory choice to NFRD constraints; otherwise defer to design. |
| Vague quality wording | "Fast", "secure", and "available" cannot be verified. | Add an evidence-backed measurement envelope or a blocker. |
| Invented numeric target | The document creates unsupported business or operational policy. | Cite measured workload or accountable-owner approval. |
| Missing unwanted behavior | The happy path hides error, timeout, and recovery obligations. | Add unwanted or complex EARS requirements. |
| Unstable or duplicate IDs | Traceability and change history break. | Preserve IDs and record split, merge, replacement, or retirement dispositions. |

## Artifact and workflow defects

| Anti-pattern | Why it fails | Corrective action |
| --- | --- | --- |
| Pre-populated `Approved` status | The artifact claims a review that did not occur. | Start as `Draft` or `Ready for review`; link approval evidence later. |
| Design-first without recovered requirements | Architecture choices become the unreviewed source of truth. | Derive and review requirements before handoff. |
| Feature-local constitution conflicts with repository governance | Two authorities can impose incompatible rules. | Reuse the repository constitution or record an explicit amendment. |
| Full requirement text copied into every artifact | Copies drift and create multiple normative sources. | Keep one canonical statement and link by stable ID. |
| Requirement with no design, task, or verification | The specification cannot drive implementation or evidence. | Add mappings or remove the item from active scope. |
| Task with no requirement | Work enters scope without an approved need. | Trace it to a requirement or classify it as governance/enablement with evidence. |
| `[P]` based only on task wording | Parallel work can still conflict on dependencies or files. | Verify dependency and change-surface independence. |
| Mermaid diagram with unlabeled boundaries | Reviewers cannot assess ownership or trust. | Label actors, components, data stores, external systems, and trust boundaries. |
| NFR repeated across contexts without a measurement envelope | A target may mean different things in each environment. | Define workload, environment, aggregation, window, and instrumentation. |
| Strong status without evidence | "Implemented" or "Verified" becomes success-shaped fiction. | Link repository or execution evidence and retain a weaker status otherwise. |
| Arbitrary P0 count rule | Mechanical limits hide release risk or force misclassification. | Justify each P0 and split the increment when the set is not reviewable. |
| Broken relative resource link | The skill cannot load its own guidance after installation. | Use a path relative to the current skill package and validate that it exists. |

## Review questions

1. Is there exactly one canonical normative statement per active requirement ID?
2. Can a reviewer find the primary source and accountable owner for every requirement?
3. Can a tester derive a pass/fail check without inventing missing behavior?
4. Does every downstream artifact preserve scope and meaning?
5. Are blockers visible where unsupported assumptions would otherwise appear?
