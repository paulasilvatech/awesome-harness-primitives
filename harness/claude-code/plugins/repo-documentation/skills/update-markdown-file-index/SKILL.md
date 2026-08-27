---
name: update-markdown-file-index
description: >-
  Update a Markdown file with an index, list, or table of files from a specified folder,
  preserving existing document structure and relative links. Use when the user asks to index a
  folder in Markdown, refresh a file table, list docs or scripts in a README, or maintain a
  contents section from filesystem files.
---

<!-- Generated from harness/github-copilot/plugins/repo-documentation/skills/update-markdown-file-index/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Update Markdown file index

Scan a target Markdown document and a source folder, derive descriptions from discovered files, then replace or add a consistent file index with valid relative links and stable ordering.

## When to invoke

- "Update this README with a table of files in `docs/`."
- "Refresh the markdown file index section."
- "Create a list of scripts from this folder."
- "Add a contents table for these Markdown files."
- "Regenerate the directory index without changing the rest of the document."

## Inputs

Use `$ARGUMENTS` or the user request to identify the target Markdown file, source folder, and optional glob pattern. If a pattern is absent, infer a safe default from the request such as `*.md` for documentation indexes or all regular files for generic folder indexes.

## Placeholder mapping

Legacy prompt placeholders map directly to runtime inputs: `${file}` is the target Markdown file, `${input:folder}` is the scanned folder, and `${input:pattern}` is the optional glob. The result may be an `index/table`, `table/index`, categorized `sub-tables`, or another `best-fit` structure using file `type/category` and other `file-related` metadata.
## Procedure

1. Read the target Markdown file to understand heading levels, existing sections, comments, and style.
2. List files in the specified folder matching the requested pattern.
3. Extract file metadata: name, type, description, optional size, and optional modified date.
4. Detect an existing index section by heading, table columns, file-link list, or HTML comment marker.
5. Choose the smallest format that matches the document: simple list, detailed table, or categorized sections.
6. Replace the existing section or insert a new section at the appropriate heading level.
7. Validate Markdown syntax, links, escaping, sort order, and preservation of surrounding content.

## Section identification

| Signal | Match examples | Action |
| --- | --- | --- |
| Heading text | "index", "files", "contents", "directory", "list" | Treat the heading subtree as the candidate replacement. |
| File table | Columns such as `File`, `Type`, `Description`, `Size`, `Modified` | Preserve column intent when regenerating rows. |
| File-link list | Bullets containing `[filename.ext](path/to/filename.ext)` | Replace only the contiguous file-list block. |
| HTML marker | Comments such as `<!-- file index -->` or generated-section markers | Prefer marker bounds over heading heuristics. |

## File analysis

| Field | Extraction rule | Fallback |
| --- | --- | --- |
| Name | Use the filename with extension unless the surrounding document omits extensions. | Preserve the existing convention. |
| Type | Use extension and category, for example `.md`, `.js`, `.py`, or `Extension`. | `file` when no extension exists. |
| Description | First Markdown heading, first meaningful comment, shebang purpose, package metadata, or inferred filename purpose. | Short inferred description in sentence case. |
| Size | Include only if the existing index includes size or the user asks. | Omit. |
| Modified | Include only if the existing index includes dates or the user asks. | Omit. |

## Table structure options

### Simple list

```markdown
## Files in <folder>

- [filename.ext](path/to/filename.ext) - Description
- [filename2.ext](path/to/filename2.ext) - Description
```

### Detailed table

```markdown
| File | Type | Description |
|------|------|-------------|
| [filename.ext](path/to/filename.ext) | Extension | Description |
| [filename2.ext](path/to/filename2.ext) | Extension | Description |
```

### Categorized sections

Group files by type, feature area, or folder when a flat table is too noisy. Keep each category alphabetized.

## Update rules

- Preserve existing Markdown structure, heading levels, frontmatter, comments, prose, and document flow outside the index block.
- Use repository-relative or target-file-relative links consistently with the surrounding document.
- Sort files alphabetically by default; use natural order when filenames contain numbered prefixes.
- Escape `|` in table cells and handle spaces, parentheses, and other special characters in filenames.
- Do not include directories unless the user asks for directory entries.
- Do not invent descriptions that claim behavior not visible from file names or contents.

## Output template

```markdown
## Markdown file index result

**Status:** updated | created | blocked
**Target file:** `<file>`
**Source folder:** `<folder>`
**Pattern:** `<pattern>`
**Format:** simple list | detailed table | categorized sections

### Files indexed
| File | Type | Description |
| --- | --- | --- |
| `<relative/path>` | `<extension or category>` | <description> |

### Validation
- Existing section found: yes | no
- Relative links valid: pass | fail
- Markdown table/list syntax valid: pass | fail
```

## Quality gate

- [ ] The target Markdown file was read before editing.
- [ ] The source folder and pattern were resolved from the user request or `$ARGUMENTS`.
- [ ] Existing index markers, headings, tables, or file-link lists were reused when present.
- [ ] File links are relative, valid, and consistently formatted.
- [ ] Files are sorted alphabetically or by justified natural order.
- [ ] Surrounding Markdown content outside the index block was preserved.
- [ ] Generated descriptions are grounded in file content, comments, headers, or conservative filename inference.
