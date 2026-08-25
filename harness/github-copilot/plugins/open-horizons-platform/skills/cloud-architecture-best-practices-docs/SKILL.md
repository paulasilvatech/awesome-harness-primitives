---
name: cloud-architecture-best-practices-docs
description: >-
  Validates Open Horizons architecture Markdown documents for required sections, required diagrams, Mermaid structure, explanation completeness, and repository copy conventions. Use this skill when reviewing or finishing an architecture document, checking {app}_Architecture.md, verifying Mermaid diagrams, or confirming the architecture Definition of Done.
---

# Cloud Architecture Best Practices Docs

This skill turns the Senior Cloud Architect's Definition of Done into an executable architecture-document check so `{app}_Architecture.md` deliverables do not ship with missing sections, incomplete diagram explanations, or broken Mermaid structure.

## When to invoke

- "Validate this architecture document before presenting it."
- "Review {app}_Architecture.md for required sections and diagrams."
- "Confirm the Mermaid diagrams and diagram explanations are complete."
- "Run the architecture document Definition of Done."

## Prerequisites and context

- Pair this with the deploy-managed architecture workflow: the responsible agent designs and writes `{app}_Architecture.md`, then runs this gate before presenting.
- The validation script is standard-library Python and self-contained; no install is needed.

## Criteria

### Required content

- [ ] Required sections are present: Executive Summary, System Context, Component Architecture, Deployment Architecture, Data Flow, Risks and Mitigations.
- [ ] The five required diagrams are present: System Context, Component, Deployment, Data Flow, Sequence.
- [ ] Each diagram's section includes the seven explanation parts: Overview, Key Components, Relationships, Design Decisions, NFR Considerations, Trade-offs, Risks and Mitigations.

### Mermaid structure

- [ ] Every Mermaid block is fenced and non-empty.
- [ ] Every Mermaid block declares a known diagram type such as `graph`, `flowchart`, `sequenceDiagram`, `erDiagram`, or `stateDiagram-v2`.
- [ ] Brackets are balanced.
- [ ] Diagram types that need edges or messages include them.

### Repository copy conventions

- [ ] No em dashes appear.
- [ ] "GitHub Copilot" is never abbreviated to bare "Copilot".
- [ ] No unfilled template placeholders remain: `{app}`, `[Diagram]`, `TODO`, or `TBD`.
- [ ] Numbers in an architecture document, including NFR targets and costs, are sourced or labeled as assumptions; the gate flags conventions, not factual accuracy, so keep the data integrity rule yourself.

### Script workflow

1. Write or update the architecture document as `{app}_Architecture.md`.
2. Run the gate:

   ```bash
   python .github/skills/architecture-doc/scripts/validate_arch.py <App_Architecture.md>
   ```

3. Fix every reported error, then rerun until it passes.
4. Record the result at the end of the document as a short "Validation" note.
5. Override the minimum diagram count only when justified: `--min-diagrams 6`.

## Output template

Return exactly this structure:

```markdown
# Architecture document validation result

**Status:** passed | failed | blocked
**Document:** <path to architecture document>
**Summary:** <one-sentence compliance summary>

### Details
- Required sections: <pass/fail and missing items>
- Required diagrams: <pass/fail and missing items>
- Diagram explanations: <pass/fail and missing parts>
- Repository copy conventions: <pass/fail and findings>

### Validation evidence
- Command: `python .github/skills/architecture-doc/scripts/validate_arch.py <App_Architecture.md>`
- Exit status: <0 or non-zero>
- Errors: <none or list>
- Warnings: <none or list>
```

## Limits

- Do not use this skill for creating cloud diagrams.
- Use `azure-draw-io-diagram-generator` (`skill`) instead when the deliverable is an editable diagram file or rendered cloud diagram.
- Use `markdown-writer` (`skill`) instead when the task is generic Markdown writing.
- Use `agentic-architecture-patterns` (`skill`) instead when designing agent architecture.
- The script cannot fully render Mermaid; it uses high-signal structural checks.

## Gotchas

- If a Mermaid diagram is very complex, simplify it rather than risk a render error.
- Do not present a document that fails the gate.

## Progressive disclosure and bundled resources

At discovery time, only `name` and `description` are loaded. Execute the script only when validating a real architecture document.

- `scripts/validate_arch.py`: architecture Markdown gate for required sections, diagrams, Mermaid structure, and conventions.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `azure-draw-io-diagram-generator` | `skill` | The task is creating or rendering professional architecture diagrams. |
| `markdown-writer` | `skill` | The task is general Markdown authoring or formatting. |
| `agentic-architecture-patterns` | `skill` | The task is designing agentic architecture decisions. |
| `open-horizons-architect` | `agent` | A persistent architecture role should own the design. |
| `open-horizons-engineer` | `agent` | Broader repository code or document review is needed. |

## Quality gate

- [ ] Required sections are present.
- [ ] The five required diagrams are present.
- [ ] Mermaid blocks are structurally valid by the script's checks.
- [ ] Every diagram section includes the seven explanation parts.
- [ ] Repository copy conventions pass.
- [ ] The validation command was run and evidence is reported.
- [ ] Any warnings are reviewed and any errors are fixed.
- [ ] The response follows `## Output template` exactly.
- [ ] Every bundled resource referenced above exists.
