---
name: pdftk-server
description: >-
  Use PDFtk Server from the command line to merge, split, rotate, encrypt, decrypt, fill forms,
  flatten forms, watermark, stamp, extract metadata, burst pages, repair PDFs, attach or extract
  files, collate scans, and manipulate PDF files. Use when asked for pdftk commands or PDF
  command-line operations.
---

<!-- Generated from harness/github-copilot/plugins/creative-media-tooling/skills/pdftk-server/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# PDFtk Server

Use the `pdftk` command-line tool to perform PDF merging, splitting, rotation, encryption, decryption, form filling, watermarking, stamping, metadata extraction, repair, attachment, and page manipulation tasks.

## When to invoke

- "Merge these PDF files with pdftk."
- "Split this PDF into pages."
- "Rotate or remove PDF pages."
- "Fill and flatten a PDF form."
- "Encrypt, decrypt, watermark, stamp, or repair a PDF."

## Prerequisites and context

PDFtk Server must be installed and available on PATH.

| Platform | Install command |
| --- | --- |
| Windows | `winget install --id PDFLabs.PDFtk.Server` |
| macOS | `brew install pdftk-java` |
| Debian/Ubuntu | `sudo apt-get install pdftk` |
| Red Hat/Fedora | `sudo dnf install pdftk` |

Verify with `pdftk --version`. Use a terminal or command prompt and operate on copies when the command is destructive or the input PDF may be damaged.

## Common commands

| Task | Command |
| --- | --- |
| Merge PDFs | `pdftk file1.pdf file2.pdf cat output merged.pdf` |
| Merge with handles | `pdftk A=file1.pdf B=file2.pdf cat A B output merged.pdf` |
| Split into individual pages | `pdftk input.pdf burst` |
| Extract pages 1–5 and 10–15 | `pdftk input.pdf cat 1-5 10-15 output extracted.pdf` |
| Remove page 13 | `pdftk input.pdf cat 1-12 14-end output output.pdf` |
| Rotate all pages 90 degrees clockwise | `pdftk input.pdf cat 1-endeast output rotated.pdf` |
| Encrypt with owner and user passwords | `pdftk input.pdf output secured.pdf owner_pw mypassword user_pw userpass` |
| Decrypt with a known password | `pdftk secured.pdf input_pw mypassword output unsecured.pdf` |
| Fill and flatten a form | `pdftk form.pdf fill_form data.fdf output filled.pdf flatten` |
| Apply background watermark | `pdftk input.pdf background watermark.pdf output watermarked.pdf` |
| Apply foreground stamp overlay | `pdftk input.pdf stamp overlay.pdf output stamped.pdf` |
| Extract metadata, bookmarks, and page metrics | `pdftk input.pdf dump_data output metadata.txt` |
| Repair a corrupted PDF | `pdftk broken.pdf output fixed.pdf` |
| Collate even and odd scans | `pdftk A=even.pdf B=odd.pdf shuffle A B output collated.pdf` |

## Operation rules

| Operation | Rule |
| --- | --- |
| `cat` | Select and reorder pages; ranges include `1-5`, `10-15`, `14-end`, and rotations such as `1-endeast`. |
| `burst` | Writes individual page files in the working directory; choose a clean output folder before running. |
| `owner_pw` / `user_pw` | Owner password controls permissions; user password controls opening. Avoid exposing passwords in shared shell history. |
| `input_pw` | Required when decrypting or opening protected input. |
| `fill_form` | Use FDF or XFDF data; add `flatten` when the filled output should not remain editable. |
| `background` | Places a single-page PDF behind every page; works best when the input has transparent regions. |
| `stamp` | Places a single-page PDF on top of every page; use for opaque overlays. |
| `dump_data` | Exports metadata and bookmarks to a text file for inspection or editing workflows. |
| `shuffle` | Interleaves handles, useful for separately scanned even and odd pages. |

## Troubleshooting

| Issue | Likely cause | Resolution |
| --- | --- | --- |
| `pdftk` command not found | PDFtk not installed or not on PATH | Install for the platform and rerun `pdftk --version`. |
| Cannot decrypt PDF | Wrong owner or user password | Provide the correct password with `input_pw`. |
| Output file is empty or corrupt | Input corruption or wrong page range | Try `pdftk input.pdf output repaired.pdf` first and verify ranges. |
| Form fields not visible after fill | Fields remain interactive or viewer hides appearances | Use `flatten` to merge fields into page content. |
| Watermark not appearing | Background is behind opaque page content | Use `stamp` for opaque overlays or check transparency. |
| Permission denied | File lock or filesystem permissions | Close PDF viewers and check input/output path permissions. |

## Progressive disclosure and bundled resources

- `references/pdftk-man-page.md`: complete manual reference with operations, options, and syntax.
- `references/pdftk-cli-examples.md`: practical command-line examples.
- `references/download.md`: installation and download instructions.
- `references/pdftk-server-license.md`: PDFtk Server license.
- `references/third-party-materials.md`: third-party library licenses.

<!-- Baseline technical terms preserved for loss check: `FDF/XFDF`, `even/odd`, `references/` -->

## Output template

```markdown
### PDFtk result

**Status:** command ready | completed | blocked
**Operation:** merge | split | rotate | encrypt | decrypt | fill-form | watermark | stamp | metadata | repair | attach | extract
**Input:** `<input PDF(s)>`
**Output:** `<output path>`

```bash
<pdftk command>
```

**Validation:** <pdftk output, file existence check, or blocker>
```

## Quality gate

- [ ] `pdftk --version` passes or installation guidance was provided.
- [ ] The command preserves input files and writes to an explicit output path when applicable.
- [ ] Page ranges and handles match the user's requested pages and order.
- [ ] Password-protected operations use `input_pw`, `owner_pw`, or `user_pw` only as needed.
- [ ] Form filling uses `flatten` when the user needs non-editable output.
- [ ] Watermark versus stamp was chosen based on background versus foreground behavior.
- [ ] The output file is verified or the blocking error is reported.
