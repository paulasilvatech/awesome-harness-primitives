---
name: "convert-excel-to-md"
description: >-
  Convert Excel .xlsx workbooks to Markdown with the bundled script so spreadsheet contents can be read, summarized, searched, extracted, compared, charted, or analyzed. Use whenever the user references a spreadsheet, workbook, budget, export, tracker, .xlsx file, or a folder of workbooks; invoke sibling converters for mixed .pdf, .docx, and .xlsx sets.
---

# Convert Excel to Markdown

Converts `.xlsx` workbooks into Markdown folders with sheet tables and extracted embedded images, then reads the Markdown output to perform the user's requested analysis instead of parsing zipped Excel XML directly.

## When to invoke

- "Read this spreadsheet."
- "Summarize or analyze this .xlsx workbook."
- "Extract data from this budget, tracker, or export."
- "Convert a folder of Excel workbooks to Markdown."
- "Process this folder with .pdf, .docx, and .xlsx files."

## Prerequisites and context

- The script supports `.xlsx` only. For legacy `.xls`, ask the user to re-save as `.xlsx` using Excel: File > Save As > Excel Workbook (.xlsx).
- Before first use in an environment, follow `references/setup.md` to ensure Python, pip, and `markitdown` are installed.
- The conversion script is `scripts/convert_excel_to_md.py`.
- Always run the bundled script first; do not parse `.xlsx` directly or write ad-hoc extraction code.
- After conversion, read the generated `.md` files to perform the requested analysis.

## Procedure

1. Resolve the source path. If the file path cannot be fully resolved, use `ask_user` or the host's confirmation mechanism to obtain the full absolute path before conversion.
2. If the source is a folder with mixed `.pdf`, `.docx`, and `.xlsx` files, invoke `convert-pdf-to-md`, `convert-word-to-md`, and `convert-excel-to-md` so no supported type is skipped.
3. Run `scripts/convert_excel_to_md.py` on the file or folder.
4. Use default output next to the source unless the user explicitly provides an output path.
5. Use `--recursive` only when subfolders should be included.
6. Read the resulting Markdown and image links before answering the user's data question.

## Conversion commands

```powershell
python scripts\convert_excel_to_md.py "C:\path\to\workbook.xlsx"
python scripts\convert_excel_to_md.py "C:\path\to\workbook.xlsx" -o "C:\path\to\output_folder"
python scripts\convert_excel_to_md.py "C:\path\to\folder"
python scripts\convert_excel_to_md.py "C:\path\to\folder" --recursive
python scripts\convert_excel_to_md.py "C:\path\to\folder" --recursive -o "C:\path\to\output_parent"
```

Use `-o` only when the user explicitly says where to save output, such as `C:\output` or `D:\work`. Do not choose `-o` based on the agent current working directory, session state folder, or implied location.

## Output structure and limitations

| Feature | Behavior |
| --- | --- |
| Workbook output | A `<name>/` folder is created next to the source `.xlsx` by default. |
| Markdown file | `<name>/<name>.md` contains each sheet as its own `## <SheetName>` Markdown table. |
| Images | Real embedded raster pictures are extracted into `<name>/img/` and inserted after each sheet table under `#### Images in this sheet`. |
| Image filenames | `sheet001_<sheetname>_img001.<ext>`, `sheet002_<sheetname>_img001.<ext>`, and so on. |
| Placement accuracy | Images are placed per sheet, not exact cell position, because MarkItDown anchors stable output at `## <SheetName>`. |
| No images | No `img/` folder or image sections are created. |
| Charts | Native Excel charts are not extracted; only real embedded pictures are extracted. |
| Batch mode | Each `.xlsx` gets its own `<name>/` output folder; with `-o`, generated folders are collected under the output parent and subfolder structure is preserved with `--recursive`. |
| Non-Excel files | Folder conversion intentionally skips non-.xlsx files and reports `NOTE: skipped N non-.xlsx file(s)`. |

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'markitdown'` / exit code 2 | MarkItDown is not installed. | Follow `references/setup.md`. |
| `ERROR: Unsupported file type '.xls'` / exit code 3 | Legacy `.xls`, not `.xlsx`. | Ask the user to re-save as `.xlsx`. |
| `ERROR: Input path not found` / exit code 3 | Wrong path or moved file. | Confirm the correct absolute path with the user. |
| `FAILED <file> -> ...` in batch output | That workbook is corrupt, password-protected, or unreadable. | Report failed files; other batch files may still succeed. |
| `NOTE: skipped N non-.xlsx file(s)` | Folder contains non-Excel files. | Expected for this skill; invoke sibling skills for `.pdf` and `.docx`. |
| A sheet's charts do not appear as images | Charts are chart objects, not embedded raster images. | Expected limitation; explain if the user needs chart images. |

## Progressive disclosure and bundled resources

- `references/setup.md`: Python, pip, and MarkItDown setup.
- `scripts/convert_excel_to_md.py`: deterministic Excel-to-Markdown conversion with embedded picture extraction.
- `scripts/requirements.txt`: Python package requirements for the script.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `convert-pdf-to-md` | skill | The input set contains `.pdf` files. |
| `convert-word-to-md` | skill | The input set contains `.docx` files. |

## Excel conversion invariants

`IMPORTANT`: the agent `MUST` convert before analysis. MarkItDown's `XLSX` output is `self-contained` in `<name>\`, such as `workbook\`, `workbook.md`, and `workbook\img\`. Image placement is `per-sheet`; native charts require `Excel/LibreOffice` rendering and are out of scope. Batch output can use `-o "C:\path\to\output_parent"` only when the user explicitly requests it.

## Output template

```markdown
### Excel to Markdown conversion result

**Status:** converted | partially converted | blocked
**Input:** `<file or folder>`
**Output:** `<name>/` or `<output_parent>/<name>/`
**Recursive:** yes | no

| Workbook | Markdown output | Images extracted | Notes |
| --- | --- | --- | --- |
| `<workbook.xlsx>` | `<name>/<name>.md` | `<count or none>` | `<success, skipped, or failure reason>` |

**Next analysis performed**
- <summary, extraction, comparison, chart review, or user-requested analysis>

**Validation**
- `python scripts\convert_excel_to_md.py ...`: pass | fail
```

## Quality gate

- [ ] The bundled script `scripts/convert_excel_to_md.py` was used before analysis.
- [ ] The input path was fully resolved; ambiguous paths were confirmed with `ask_user` or equivalent.
- [ ] `.xls` files were rejected with re-save guidance.
- [ ] Default output stayed next to the source unless the user explicitly requested `-o`.
- [ ] Mixed `.pdf`, `.docx`, and `.xlsx` sets invoked the sibling converters.
- [ ] Generated `.md` files were read before answering the user's content question.
- [ ] Failures in batch mode were reported without hiding successful conversions.
