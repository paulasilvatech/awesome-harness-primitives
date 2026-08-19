---
name: markdown-writer
description: 'Use when creating or restructuring Markdown documents such as README, ADR, specification, guide, changelog, runbook, RFC, technical documentation, or PPTX/PowerPoint-to-Markdown reading editions. Produces Markdown with YAML frontmatter, versioning, change log, table of contents, references, and quality checks. DO NOT USE FOR: editable draw.io/SVG architecture diagrams with official icons (use azure-architecture-diagrams), Mermaid architecture document validation/Definition-of-Done checks (use architecture-doc), creating PPTX presentations, Word documents, PDFs, or image-only diagrams. Triggers include "write a README", "create an ADR", "draft a guide", and "convert PPTX to Markdown".'
---

# Markdown Writer

Use this skill to create professional Markdown deliverables in English with stable structure, metadata, readable prose, and repository-aware file placement. It produces a complete document draft or rewrite, plus a quality report for frontmatter, headings, links, code fences, and references.

> [!NOTE]
> This skill depends on file-system write access for requested Markdown outputs and, for PowerPoint conversion, `markitdown` or an available MarkItDown MCP tool. It does not require cloud authentication unless the source material is stored behind an authenticated service.

## When to invoke

- "Write a README for this component."
- "Create an ADR for this architecture decision."
- "Draft a deployment guide in Markdown."
- "Convert this PowerPoint deck into a Markdown reading edition."
- "Rewrite this runbook with a table of contents and references."

## Prerequisites and context

- The document type is known: README, ADR, specification, guide, changelog, runbook, RFC, or general technical document.
- The destination path is known or can be inferred from existing repository conventions such as `docs/`, `docs/guides/`, or `docs/architecture/`.
- Source material is available in the workspace or provided by the user.
- For PPTX conversion, the source deck path exists and speaker notes are preserved when the converter exposes them.

## Procedure

### Step 1: Confirm document intent and destination

1. Identify audience, purpose, status, owner, and expected output path.
2. Inspect nearby documents under `docs/`, `docs/guides/`, and `docs/architecture/` for naming and structure conventions.
3. Do not create a new planning file unless the user requested a document artifact.

### Step 2: Select the document structure

Use one of these structures and avoid placeholder sections.

| Document type | Required sections |
| --- | --- |
| README | Overview, Quick Start, Prerequisites, Installation, Usage, Configuration, Contributing, License. |
| ADR | Status, Context, Decision, Consequences, References. |
| Specification | Overview, Scope, Requirements, Design, Security, Testing, References. |
| Guide | Overview, Prerequisites, Step-by-step Instructions, Troubleshooting, References. |
| Runbook | Overview, Symptoms, Diagnosis, Resolution, Prevention, Escalation, References. |

### Step 3: Write mandatory frontmatter

```yaml
---
title: "Document Title"
description: "One-sentence summary of the document purpose."
author: "Open Horizons"
date: "YYYY-MM-DD"
version: "1.0.0"
status: "draft"
tags: ["open-horizons"]
---
```

### Step 4: Build the Markdown body

- Use exactly one `#` H1.
- Include a change log for versioned documents.
- Include a table of contents for documents with more than three major sections.
- Keep paragraphs under four sentences.
- Use descriptive links and a `## References` section.
- Specify a language on every fenced code block.

### Step 5: Convert PPTX decks when requested

1. Use MarkItDown first when available.
2. Treat raw extraction as source material, not final output.
3. Preserve every slide in order, including speaker notes.
4. Remove extraction noise such as image placeholders, repeated headers, and page numbers.
5. Render each slide as readable prose with a short `Shown on the slide:` list only when useful.

### Step 6: Classify document risk

| Risk | Meaning |
| --- | --- |
| High | Public-facing, compliance, security, architecture, or release documentation. |
| Medium | Team guide, runbook, specification, or ADR with operational impact. |
| Low | Internal draft, formatting-only rewrite, or local conversion. |

### Step 7: Review and save

Before writing, confirm overwrite intent if the target file already exists. For new files, use the repository's existing documentation tree, not an ad hoc location.

```text
Markdown action: <create|rewrite|overwrite>
Document type: <README|ADR|Guide|Runbook|Specification|Other>
Target path: <path>
Proceed with writing the Markdown artifact? (y/n)
```

> [!IMPORTANT]
> Only create, rewrite, or overwrite Markdown files after an explicit affirmative response when the user has not already requested the exact file write. On a negative, ambiguous, or missing response, do not write the artifact; output the draft content and stop.

## Limits

- Do not use this skill for: editable draw.io/SVG architecture diagrams with official icons (use azure-architecture-diagrams), Mermaid architecture document validation/Definition-of-Done checks (use architecture-doc), creating PPTX presentations, Word documents, PDFs, or image-only diagrams.
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| Destination path is unclear | Propose the closest existing docs directory and wait for direction if multiple choices exist. |
| Source PPTX cannot be parsed | Report the converter error and preserve any partial extracted text separately in the response only. |
| Existing document would be overwritten | Ask for explicit overwrite approval or choose a new filename. |
| Missing source references | Mark claims as assumptions or omit them. |
| Broken internal link | Fix the link if the target exists; otherwise report it in the quality section. |

## Output template

Return exactly this structure:

```markdown
## Markdown Delivery Report

**Document:** <title>
**Type:** <README|ADR|Guide|Runbook|Specification|Other>
**Path:** <path>
**Status:** <draft|review|approved>

### Structure
- Frontmatter: <present|missing>
- H1 count: <count>
- Table of contents: <present|not needed|missing>
- References: <present|missing>

### Quality Findings
- <finding>

### Next Steps
1. <next step>
```

## Quality gate

- [ ] YAML frontmatter includes title, description, author, date, version, status, and tags.
- [ ] Exactly one H1 is present.
- [ ] Heading levels do not skip.
- [ ] Table of contents is present when needed.
- [ ] Code fences specify a language.
- [ ] Links are descriptive and references are cited.
- [ ] No placeholder text remains.
- [ ] No emojis or pictographs are present.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
