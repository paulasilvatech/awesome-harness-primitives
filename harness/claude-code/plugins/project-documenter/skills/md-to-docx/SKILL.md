---
name: md-to-docx
description: >-
  Convert Markdown files to professionally formatted Word .docx documents with title page
  metadata, table of contents, styled tables, code blocks, links, and embedded PNG images using
  pure JavaScript. Use when the user asks to convert Markdown to Word, produce a .docx from .md,
  embed PNG diagrams, or run the bundled Node converter without Pandoc or LibreOffice.
---

<!-- Generated from harness/github-copilot/plugins/project-documenter/skills/md-to-docx/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Markdown to Word docx

Convert a Markdown `.md` file into a styled Word `.docx` document; parse YAML front-matter, headings, tables, lists, code, links, horizontal rules, and PNG image references, then emit a portable document using the bundled Node.js script.

## When to invoke

- "Convert this Markdown file to Word."
- "Generate a `.docx` from this `.md` report."
- "Embed the PNG diagrams when creating the Word document."
- "Use the pure JavaScript markdown-to-docx converter."
- "Convert without Pandoc, LibreOffice, or native binaries."

## Prerequisites and context

- Node.js 18+ must be available.
- Dependencies are declared in `scripts/package.json`: `docx` 9+ and `marked` 15+.
- Run `npm install` from the skill's `scripts` folder before the first conversion or after dependency changes.
- The converter supports PNG image embedding; other image types should be converted to PNG first or expected to degrade.

## Procedure

1. Install dependencies once from the scripts folder:

```bash
cd skills/md-to-docx/scripts && npm install
```

2. Convert from the workspace root:

```bash
node skills/md-to-docx/scripts/md-to-docx.mjs <input.md> [output.docx]
```

3. If `[output.docx]` is omitted, expect `<input-basename>.docx` in the current directory.
4. Open or inspect the generated `.docx` only if the task requires verification beyond successful script completion.

## Conversion behavior

| Markdown feature | Word output |
| --- | --- |
| YAML front-matter | Title page values from `title`, `date`, `version`, and `audience`. |
| `title` containing `—` or `–` | Split into main title and subtitle. |
| H1-H3 headings | Document headings and generated table of contents entries. |
| Paragraphs and links | Styled body text; links preserved as link text and target where supported. |
| Tables | Styled tables with alternating row colors. |
| Code blocks | Consolas-styled code sections. |
| Lists | Word bullet or numbered lists. |
| Horizontal rules | Section separators. |
| `![alt](path)` PNG images | Embedded inline image resolved relative to the input Markdown file. |
| Missing image file | Placeholder text `[Image not found: <path>]`. |

## Image embedding

The converter resolves image paths relative to the input Markdown file, reads the PNG header to determine dimensions, and scales each image to fit within 6 inches width while preserving aspect ratio.

```markdown
![High-Level Architecture](diagrams/high-level-architecture.drawio.png)
```

## Front-matter format

```yaml
---
title: Project Name — Project Summary
date: 2025-01-15
version: 1.0
audience: Engineering Team, Architects, Stakeholders
---
```

## Styling and package notes

The skill package contains `SKILL.md` plus converter scripts; the old title used the word `SKILL`, but the runtime entry point is this Agent Skill. Installation is a `one-time` dependency step, not a `system-level` install. Heading color is `#1F3864`, default output examples may use `output.docx`, and the document styling uses Calibri headings, alternating table rows, and Consolas code blocks.
## Progressive disclosure and bundled resources

| Resource | Use when | Notes |
| --- | --- | --- |
| `scripts/md-to-docx.mjs` | Running the conversion | Pure JavaScript converter; no Pandoc, LibreOffice, or native binary required. |
| `scripts/package.json` | Installing dependencies | Contains `docx` and `marked`. |

## Gotchas

- **Install from the scripts folder**: `npm install` must run where `scripts/package.json` lives.
- **Run conversion from a predictable workspace root**: relative input and output paths are interpreted by the current shell, while images are resolved relative to `<input.md>`.
- **Only PNG images embed**: non-PNG Markdown images are not guaranteed to render as embedded Word images.
- **Missing images do not stop conversion**: the output contains `[Image not found: <path>]`, so inspect the document if image completeness matters.

## Output template

```markdown
## Markdown to docx result

**Status:** converted | blocked
**Input:** `<input.md>`
**Output:** `<output.docx>`
**Command:** `node skills/md-to-docx/scripts/md-to-docx.mjs <input.md> [output.docx]`

### Features used
- Front-matter title page: yes | no
- Table of contents: yes | no
- PNG images embedded: <count or not checked>
- Missing image placeholders: <count or not checked>

### Validation
- Dependencies installed: pass | not needed | fail
- Converter exit status: pass | fail
```

## Quality gate

- [ ] Node.js 18+ availability was checked or reasonably established.
- [ ] `npm install` was run in `skills/md-to-docx/scripts` when dependencies were missing.
- [ ] The conversion command used `node skills/md-to-docx/scripts/md-to-docx.mjs <input.md> [output.docx]`.
- [ ] The output path behavior was reported, including default `<input-basename>.docx` when omitted.
- [ ] PNG image handling and missing-image placeholders were considered when the Markdown contains images.
- [ ] The final `.docx` path was reported.
