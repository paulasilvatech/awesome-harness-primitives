---
name: architecture-doc
description: "Use when validating a Mermaid-based Open Horizons architecture document before presentation; produces a pass/fail report for required sections, five diagrams, Mermaid structure, seven explanation parts, and copy conventions. DO NOT USE FOR: creating editable draw.io/SVG cloud diagrams with official icons (use azure-architecture-diagrams), or writing general Markdown, README, ADR, runbook, or PPTX conversion content (use markdown-writer). Triggers include \"validate this architecture document\", \"check the Mermaid diagrams\", \"quality gate this Architecture.md\"."
---

# Architecture Doc

This workflow validates an `{app}_Architecture.md` deliverable against the Open Horizons architecture document Definition of Done. It produces a deterministic validation report using the repository script and tells the author exactly what to fix before the document is presented.

> [!NOTE]
> This skill shells out to Python through `python scripts/validate_arch.py`. The script is standard-library Python and validates Markdown structure and Mermaid syntax heuristics; it does not replace a human architecture review. Run bundled commands from this skill directory.

## When to invoke
- "Validate this architecture document before I present it."
- "Check whether the Mermaid diagrams are complete and well formed."
- "Quality gate `Payment_Platform_Architecture.md`."
- "Review this architecture doc against the Open Horizons Definition of Done."

## Prerequisites and context
- The architecture Markdown file exists in the repository.
- The file is intended to follow the `{app}_Architecture.md` convention.
- Python 3 is available.
- The validation script exists at `scripts/validate_arch.py`.

## Procedure

### Step 1: Confirm target document
1. Identify the exact Markdown file path supplied by the user.
2. Verify it is inside the repository and is not excluded by policy.
3. Confirm whether the default minimum of five diagrams applies.

### Step 2: Run the validation script
```bash
python scripts/validate_arch.py <App_Architecture.md>
```

Use the optional diagram threshold only when the document's approved scope requires it:

```bash
python scripts/validate_arch.py <App_Architecture.md> --min-diagrams 6
```

### Step 3: Review enforced checks
- [ ] Required sections: Executive Summary, System Context, Component Architecture, Deployment Architecture, Data Flow, Risks and Mitigations.
- [ ] Required diagrams: System Context, Component, Deployment, Data Flow, Sequence.
- [ ] Mermaid blocks are fenced, non-empty, declare known diagram types, and contain required edges or messages.
- [ ] Each diagram section includes Overview, Key Components, Relationships, Design Decisions, NFR Considerations, Trade-offs, Risks and Mitigations.
- [ ] Copy conventions are met: no unfilled placeholders, no bare "Copilot" for GitHub Copilot, and no unsupported template residue.

### Step 4: Classify findings
| Severity | Meaning |
|---|---|
| Error | The validator exits non-zero; the document must not be presented. |
| Warning | The document may render but has quality or convention risks. |
| Note | Optional improvement or human-review reminder. |

### Step 5: Report fixes and rerun
1. Summarize every error with the section or diagram name.
2. Fix only the architecture document if the user asked for edits.
3. Rerun the same command until it passes.
4. If adding a validation note to the document, confirm first.

```text
Validation note update:
- Target file:
- Result to record:
Proceed with updating the document? (y/n)
```

> [!IMPORTANT]
> Only modify the architecture document or add validation notes if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the validation report and stop.

## Limits

- Do not use this skill for: creating editable draw.io/SVG cloud diagrams with official icons (use azure-architecture-diagrams), or writing general Markdown, README, ADR, runbook, or PPTX conversion content (use markdown-writer).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| Target file is missing | Report the missing path and do not run the validator. |
| Python is unavailable | Report the missing runtime and provide the exact command that should be run later. |
| Validator fails | Preserve the full error summary and identify the first fix to make. |
| Mermaid still may not render | Recommend rendering in the target Markdown viewer after the structural gate passes. |

## Output template

Return exactly this structure:
```markdown
# Architecture Document Validation Report

## Target
- File:
- Command:

## Result
- Status: Pass | Fail
- Errors:
- Warnings:

## Required Fixes
| Severity | Section | Finding | Fix |
|---|---|---|---|

## Rerun Command
```bash
python scripts/validate_arch.py <App_Architecture.md>
```
```

## Quality gate
- [ ] The validation script ran against the intended file.
- [ ] Non-zero exits are treated as blocking errors.
- [ ] Every required section and diagram is accounted for.
- [ ] No repository file is modified without explicit confirmation.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
