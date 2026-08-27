---
name: convert-word-to-md
description: >-
  Convert Word .docx documents into Markdown with extracted images using the bundled script. Use
  this skill when a user asks to read, summarize, review, compare, analyze, extract data from, or
  batch-process Word documents, resumes, reports, contracts, or proposals, including mixed folders
  that also require sibling PDF or Excel conversion skills.
---

<!-- Generated from harness/github-copilot/plugins/convert-to-md/skills/convert-word-to-md/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Convert Word to Markdown

Convert `.docx` files into Markdown and image folders with the bundled script, then read the generated `.md` output to perform the user's requested analysis.

## When to invoke

- "Read this Word document."
- "Summarize this .docx file."
- "Extract data from these Word reports."
- "Convert this folder of Word documents to Markdown."
- "Analyze these mixed PDF, Word, and Excel files."

## Prerequisites and context

- This skill supports `.docx` only. For legacy `.doc`, tell the user to re-save as `.docx` with Word: File > Save As > Word Document (.docx).
- Use `scripts/convert_word_to_md.py`; do not parse `.docx` XML directly and do not write ad-hoc conversion code.
- Before first use in an environment, follow `references/setup.md` to ensure Python, pip, and `markitdown` are installed.
- If `ModuleNotFoundError: No module named 'markitdown'` appears, follow `references/setup.md`.
- IMPORTANT: the agent MUST convert first; if the path is ambiguous, use `ask_user`-style confirmation instead of guessing.

## Procedure

1. Resolve the full source path. If the user provides only a filename or an ambiguous path, ask for the full absolute path before conversion.
2. If the input set includes `.pdf`, `.docx`, and `.xlsx`, invoke `convert-pdf-to-md`, `convert-word-to-md`, and `convert-excel-to-md` so no supported file type is silently skipped.
3. Run `scripts/convert_word_to_md.py` on the `.docx` file or folder.
4. Use the default output location next to the source unless the user explicitly provides an output path.
5. Read the generated Markdown file or files and complete the requested summary, extraction, review, comparison, or analysis.

## Conversion commands

| Task | Command |
| --- | --- |
| Single file on Windows | `python scripts\convert_word_to_md.py "C:\path\to\document.docx"` |
| Single file on macOS / Linux | `python scripts/convert_word_to_md.py "/path/to/document.docx"` |
| Explicit output folder | `python scripts\convert_word_to_md.py "C:\path\to\document.docx" -o "C:\path\to\output_folder"` |
| Folder batch mode | `python scripts\convert_word_to_md.py "C:\path\to\folder"` |
| Recursive folder batch mode | `python scripts\convert_word_to_md.py "C:\path\to\folder" --recursive` |
| Collect outputs under a parent | `python scripts\convert_word_to_md.py "C:\path\to\folder" --recursive -o "C:\path\to\output_parent"` |

MarkItDown emits truncated `data:image/png;base64...` placeholders, so the script extracts real images from the `.docx` and creates one folder per document:

```text
<name>/
    img/
        img001.<ext>
        img002.<ext>
        ...
    <name>.md
```

On Windows this corresponds to `<name>\`, `document\`, `document.md`, and `document\img\`. The folder is self-contained.

Image references in Markdown are relative, for example `img/imgNNN.ext`. If no embedded images exist, no `img/` folder is created.

## Output location rules

- Default to a `<name>/` folder next to the source `.docx`.
- Use `-o` only when the user explicitly provides an output path such as "save the output to `C:\output`" or "put the results in `D:\work`".
- Do not infer output from the current working directory, a session-state folder, or the agent's location.
- In recursive mode, preserve subfolder structure under the output parent.
- The flags `--recursive` and `-o "C:\path\to\output_parent"` keep their original meanings.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'markitdown'` / exit code 2 | MarkItDown not installed | Follow `references/setup.md`. |
| `ERROR: Unsupported file type '.doc'` / exit code 3 | Legacy `.doc`, not `.docx` | Ask the user to re-save as `.docx`. |
| `ERROR: Input path not found` / exit code 3 | Wrong path, or file moved | Confirm the correct path with the user. |
| `FAILED <file> -> ...` in batch output | File is corrupt, password-protected, or unreadable | Report failed file names; other batch files still succeed. |
| `NOTE: skipped N non-.docx file(s)` | Folder contains non-Word files | Expected for unsupported types; invoke sibling skills for supported PDF and Excel files. |
| `WARNING: found N image placeholder(s) ... but extracted M image file(s)` | Placeholder count differs from `word/media/` images in an unusual/malformed document | Leave placeholders unreplaced and inspect media manually if images are needed. |

## Progressive disclosure and bundled resources

- `references/setup.md`: environment setup for Python, pip, and MarkItDown.
- `scripts/convert_word_to_md.py`: required converter for single-file and batch conversion.
- `scripts/requirements.txt`: Python package requirements for the converter.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `convert-pdf-to-md` | skill | The input set includes `.pdf` files. |
| `convert-excel-to-md` | skill | The input set includes `.xlsx` files. |

## Output template

```markdown
## Word conversion result

**Status:** converted | partially converted | blocked
**Input:** `<file or folder>`
**Output:** `<generated Markdown path or folder>`

| Source | Markdown | Images | Notes |
| --- | --- | --- | --- |
| `<document.docx>` | `<name>/<name>.md` | `<count or none>` | `<success, skipped, or failure reason>` |

### Requested analysis
<summary, extraction, comparison, or next result based on the generated Markdown>
```

## Quality gate

- [ ] Every `.docx` was converted with `scripts/convert_word_to_md.py` before analysis.
- [ ] Legacy `.doc` files were rejected with re-save guidance.
- [ ] Mixed `.pdf`, `.docx`, and `.xlsx` sets invoked the sibling conversion skills.
- [ ] The default output stayed next to the source unless the user explicitly supplied `-o`.
- [ ] Generated `.md` files were read before summarizing, reviewing, comparing, or extracting.
- [ ] Conversion failures were reported per file without hiding successful batch outputs.
