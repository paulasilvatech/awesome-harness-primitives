---
name: convert-pdf-to-md
description: >-
  Convert PDF .pdf documents to Markdown with the bundled script so reports, papers, invoices,
  forms, contracts, scanned documents, and folders of PDFs can be read, summarized, searched,
  extracted, compared, or analyzed. Use whenever a user references a PDF; invoke sibling
  converters for mixed .pdf, .docx, and .xlsx sets.
---

<!-- Generated from harness/github-copilot/skills/convert-pdf-to-md/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Convert PDF to Markdown

Converts `.pdf` documents into Markdown folders with extracted embedded images, then reads the Markdown output to perform the requested analysis instead of attempting unreliable direct PDF parsing.

## When to invoke

- "Read this PDF."
- "Summarize or analyze this report, paper, invoice, form, or contract."
- "Extract data or tables from this .pdf file."
- "Convert a folder of PDFs to Markdown."
- "Process this folder with .pdf, .docx, and .xlsx files."

## Prerequisites and context

- The script supports `.pdf` only; MarkItDown has no legacy PDF-family format equivalent to `.doc` or `.xls`.
- Before first use in an environment, follow `references/setup.md` to ensure Python, pip, `markitdown`, and `pymupdf` are installed.
- The conversion script is `scripts/convert_pdf_to_md.py`.
- Always run the bundled script first; do not parse PDF content directly or write ad-hoc extraction code.
- After conversion, read the generated `.md` files to perform the requested analysis.

## Procedure

1. Resolve the source path. If the file path cannot be fully resolved, use `ask_user` or the host's confirmation mechanism to obtain the full absolute path before conversion.
2. If the source is a folder with mixed `.pdf`, `.docx`, and `.xlsx` files, invoke `convert-pdf-to-md`, `convert-word-to-md`, and `convert-excel-to-md` so no supported type is skipped.
3. Run `scripts/convert_pdf_to_md.py` on the file or folder.
4. Use default output next to the source unless the user explicitly provides an output path.
5. Use `--recursive` only when subfolders should be included.
6. Read the resulting Markdown and `## Extracted Images` appendix before answering.

## Conversion commands

```powershell
python scripts\convert_pdf_to_md.py "C:\path\to\document.pdf"
python scripts\convert_pdf_to_md.py "C:\path\to\document.pdf" -o "C:\path\to\output_folder"
python scripts\convert_pdf_to_md.py "C:\path\to\folder"
python scripts\convert_pdf_to_md.py "C:\path\to\folder" --recursive
python scripts\convert_pdf_to_md.py "C:\path\to\folder" --recursive -o "C:\path\to\output_parent"
```

Use `-o` only when the user explicitly says where to save output, such as `C:\output` or `D:\work`. Do not choose `-o` based on the agent current working directory, session state folder, or implied location.

## Output structure and limitations

| Feature | Behavior |
| --- | --- |
| Document output | A `<name>/` folder is created next to the source `.pdf` by default. |
| Markdown file | `<name>/<name>.md` contains text and tables extracted by MarkItDown. |
| Images | Real embedded images are extracted via PyMuPDF into `<name>/img/`. |
| Image filenames | `page001_img001.<ext>`, `page002_img001.<ext>`, and so on. |
| Image placement | Because MarkItDown PDF text has no reliable per-page markers, images are appended under `## Extracted Images` with `### Page N` headings. |
| No images | No `img/` folder or `Extracted Images` section is created. |
| Scanned PDFs | MarkItDown does not perform OCR; scanned/image-only PDFs may produce empty or near-empty Markdown. |
| Batch mode | Each `.pdf` gets its own `<name>/` output folder; with `-o`, generated folders are collected under the output parent and subfolder structure is preserved with `--recursive`. |
| Non-PDF files | Folder conversion intentionally skips non-.pdf files and reports `NOTE: skipped N non-.pdf file(s)`. |

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'markitdown'` or `'fitz'` / exit code 2 | MarkItDown or PyMuPDF is not installed. | Follow `references/setup.md`. |
| `ERROR: Unsupported file type '...'` / exit code 3 | Input is not a `.pdf` file. | Ask for the correct file or use the `.doc`, `.docx`, or `.xlsx` sibling skill as appropriate. |
| `ERROR: Input path not found` / exit code 3 | Wrong path or moved file. | Confirm the correct absolute path with the user. |
| `FAILED <file> -> ...` in batch output | That PDF is corrupt, password-protected, or unreadable. | Report failed files; other batch files may still succeed. |
| `NOTE: skipped N non-.pdf file(s)` | Folder contains non-PDF files. | Expected for this skill; invoke sibling skills for `.docx` and `.xlsx`. |
| Markdown body is empty or near-empty despite images being extracted | The PDF is scanned/image-only with no embedded text layer. | Tell the user OCR is not supported; extracted page images are still available to view. |
| Images appear in an appendix instead of inline with text | PDF text lacks reliable placement anchors. | Expected; cross-reference `### Page N` with surrounding context when needed. |

## Progressive disclosure and bundled resources

- `references/setup.md`: Python, pip, MarkItDown, and PyMuPDF setup.
- `scripts/convert_pdf_to_md.py`: deterministic PDF-to-Markdown conversion with embedded image extraction.
- `scripts/requirements.txt`: Python package requirements for the script.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `convert-word-to-md` | skill | The input set contains `.docx` files. |
| `convert-excel-to-md` | skill | The input set contains `.xlsx` files. |

## PDF conversion invariants

`IMPORTANT`: the agent `MUST` convert before analysis because PDF is a `layout/print` format. Output is `self-contained` in `<name>\`, such as `document\`, `document.md`, and `document\img\`. Batch output can use `-o "C:\path\to\output_parent"` only when the user explicitly requests it.

## Output template

```markdown
### PDF to Markdown conversion result

**Status:** converted | partially converted | blocked
**Input:** `<file or folder>`
**Output:** `<name>/` or `<output_parent>/<name>/`
**Recursive:** yes | no

| PDF | Markdown output | Images extracted | Notes |
| --- | --- | --- | --- |
| `<document.pdf>` | `<name>/<name>.md` | `<count or none>` | `<success, skipped, or failure reason>` |

**Next analysis performed**
- <summary, extraction, comparison, or user-requested analysis>

**Validation**
- `python scripts\convert_pdf_to_md.py ...`: pass | fail
```

## Quality gate

- [ ] The bundled script `scripts/convert_pdf_to_md.py` was used before analysis.
- [ ] The input path was fully resolved; ambiguous paths were confirmed with `ask_user` or equivalent.
- [ ] Default output stayed next to the source unless the user explicitly requested `-o`.
- [ ] Mixed `.pdf`, `.docx`, and `.xlsx` sets invoked the sibling converters.
- [ ] Generated `.md` files and the `## Extracted Images` appendix were considered before answering.
- [ ] Scanned PDFs without OCR text were reported honestly.
- [ ] Failures in batch mode were reported without hiding successful conversions.
