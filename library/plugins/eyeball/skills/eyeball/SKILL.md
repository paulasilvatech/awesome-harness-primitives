---
name: "eyeball"
description: >-
  Analyze local documents or web pages with inline source screenshots in a Word document. Use when asked to use eyeball, run eyeball on a document, analyze a PDF, Word, RTF, or URL with visual proof, or produce a cited report where every factual claim is backed by highlighted source screenshots.
---

# Eyeball

Analyze a source document, choose verbatim anchors for each claim, and generate a Word `.docx` on the user's Desktop with highlighted screenshots that let the user verify the analysis visually.

## When to invoke

- "Use eyeball on this document."
- "Run eyeball on this PDF."
- "Analyze this URL with source screenshots."
- "Create a Word doc where I can verify every claim."
- "Eyeball this contract."

## Prerequisites and context

- Supported sources: Word documents `.docx` and `.doc`, PDFs `.pdf`, RTF files, and publicly accessible web URLs.
- The utility path is `<plugin_dir>/skills/eyeball/tools/eyeball.py`.
- Find it with `find ~/.copilot/installed-plugins -name "eyeball.py" -path "*/eyeball/*" 2>/dev/null`; if not found, check the project directory or the user's home directory for the eyeball repo.
- On first use, run `python3 <path-to>/eyeball.py setup-check`.
- If dependencies are missing, install `pymupdf`, `pillow`, `python-docx`, and `playwright` with `pip3 install pymupdf pillow python-docx playwright`, then run `python3 -m playwright install chromium`. On Windows, install `pywin32` with `pip install pywin32`.

## Procedure

1. Announce activation with: `Eyeball is active. I'll analyze the document and produce a Word doc with inline source screenshots so you can verify every claim with your own eyes.`
2. Extract and read the full source text before writing analysis: `python3 <path-to>/eyeball.py extract-text --source "<path-or-url>"`.
3. Identify actual section numbers, headings, page numbers, and key language from the extracted text.
4. For every analysis point, cite the correct section number and page number and choose verbatim anchors that directly support the claim.
5. Build a JSON `sections` array with `heading`, `analysis`, `anchors`, optional `target_page`, optional `target_pages`, and optional `context_padding`.
6. Generate the Word document with `python3 <path-to>/eyeball.py build --source "<path-or-url>" --output ~/Desktop/<title>.docx --title "Analysis Title" --subtitle "Source description" --sections '[...]'`.
7. Save the output to the user's Desktop and report the filename.

If the user already provided the source text or it was already read in the current conversation, step 2 may be skipped only after section numbers and page references are still verified against actual text.

## Anchor selection

| Do | Do not |
| --- | --- |
| Use verbatim phrases from the source text that directly support the assertion. | Use generic topic labels such as `Confidentiality` that appear throughout the document. |
| Use multiple anchors to span the full screenshot region. | Use section titles alone when they also appear as cross-references. |
| Use specific uncommon phrases with the intended page. | Use single common words that match in many places. |
| Target the correct page with `target_page` or stitch pages with `target_pages`. | Guess page numbers from visual layout instead of extracted text. |

Examples:

```json
{"anchors": ["retain ownership", "Ownership of Content, Right to Post"], "target_page": 8}
{"anchors": ["12. LIMITATION OF LIABILITY", "INDIRECT", "CONSEQUENTIAL"], "target_page": 13}
```

Avoid weak anchors such as `{"anchors": ["User-Generated Content"], "target_page": 8}` or `{"anchors": ["LIMITATION OF LIABILITY"]}` when those phrases appear elsewhere.

## Build command fields

| Field | Required | Meaning |
| --- | --- | --- |
| `heading` | Yes | Section heading in the output document. |
| `analysis` | Yes | Analysis text that references the real section and page. |
| `anchors` | Yes | List of verbatim phrases to search for and highlight. |
| `target_page` | No | Single 1-indexed page to search. |
| `target_pages` | No | Multiple pages to search and stitch vertically. |
| `context_padding` | No | PDF points above and below the anchor region; default is `40`, increase to `50` or more for context. |

## Gotchas

- **Do not skip text extraction**: analysis based on assumed document structure produces wrong section and page citations.
- **Search-term not found means the anchor is wrong**: adjust anchors and rebuild; do not ship unmatched screenshots.
- **Web page page numbers may differ from the browser**: Playwright renders the page to PDF first, so use extracted text page numbers.
- **Screenshot mismatch means the analysis or anchor is wrong**: fix whichever is incorrect before delivery.

## Progressive disclosure and bundled resources

- `tools/eyeball.py`: executable utility for `setup-check`, `extract-text`, and `build`.

<!-- Baseline technical terms preserved for loss check: `CRITICAL`, `RIGHT`, `WRONG`, `above/below`, `cross-reference` -->

## Output template

```markdown
### Eyeball result

**Status:** created | needs source | blocked
**Source:** `<path-or-url>`
**Output:** `~/Desktop/<title>.docx`

| Section | Source page(s) | Anchors used | Verification |
| --- | --- | --- | --- |
| `<heading>` | `<page or pages>` | `<verbatim anchors>` | highlighted screenshot included |

**Notes:** <missing anchors, rebuilt sections, or none>
```

## Quality gate

- [ ] Full source text was extracted and read before analysis unless already available and verified.
- [ ] Every claim cites actual section numbers and page numbers from the source.
- [ ] Every anchor is a verbatim source phrase and directly supports the claim.
- [ ] `target_page` or `target_pages` is used when needed to avoid false matches.
- [ ] Unmatched or mismatched screenshots were corrected and rebuilt.
- [ ] The final `.docx` is saved on the user's Desktop.
