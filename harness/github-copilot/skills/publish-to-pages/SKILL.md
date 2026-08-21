---
name: publish-to-pages
description: >-
  Publish presentations and web content to GitHub Pages by converting PPTX, PDF, HTML, or Google Slides into a deployable site, creating or updating a repository, enabling Pages, and returning the live URL. Use when the user asks to publish slides, deploy HTML, share a presentation, convert a deck to GitHub Pages, or create a public Pages link.
---

# Publish to Pages

Convert a local presentation, PDF, HTML file, or Google Slides URL into `index.html`, publish it with the bundled scripts, and report the GitHub repository URL plus the GitHub Pages URL.

## When to invoke

- "Publish this PPTX to GitHub Pages."
- "Turn this PDF into a public Pages site."
- "Deploy this HTML file and give me a live URL."
- "Share this Google Slides deck through GitHub Pages."
- "Create a GitHub Pages repo for this presentation."

## Prerequisites and context

Run prerequisite checks quietly and surface only failures:

```bash
command -v gh >/dev/null || echo "MISSING: gh CLI — install from https://cli.github.com"
gh auth status &>/dev/null || echo "MISSING: gh not authenticated — run 'gh auth login'"
command -v python3 >/dev/null || echo "MISSING: python3 (needed for PPTX conversion)"
```

`poppler-utils` is optional and required only for PDF rendering through `pdftoppm`. On Debian/Ubuntu install it with `apt install poppler-utils`; on macOS use `brew install poppler`.

## Input detection

| Input | Detection | Handling |
| --- | --- | --- |
| HTML file | Extension `.html` or `.htm` | Copy or publish directly as `index.html`. |
| PPTX file | Extension `.pptx` | Convert with `scripts/convert-pptx.py`. |
| PDF file | Extension `.pdf` | Convert with `scripts/convert-pdf.py`; requires `pdftoppm`. |
| Google Slides URL | Contains `docs.google.com/presentation` | Extract `PRESENTATION_ID`, download PPTX, then convert. |

Ask for a repository name when the user did not provide one. Default to the filename without extension. Use `public` visibility unless the user explicitly requests `private`; note that GitHub Pages on private repositories requires a Pro, Team, or Enterprise plan.

## Conversion commands

Use a project-local scratch path when possible. The legacy examples below use `/tmp/output.html`; keep the generated HTML and any `assets/` directory in the same parent directory before publishing.

| Source | Command |
| --- | --- |
| HTML | `cp INPUT_FILE index.html` when the filename is not already `index.html`. |
| PPTX | `python3 SKILL_DIR/scripts/convert-pptx.py INPUT_FILE /tmp/output.html` |
| PPTX, forced external assets | `python3 SKILL_DIR/scripts/convert-pptx.py INPUT_FILE /tmp/output.html --external-assets` |
| PDF | `python3 SKILL_DIR/scripts/convert-pdf.py INPUT_FILE /tmp/output.html` |
| PDF, forced external assets | `python3 SKILL_DIR/scripts/convert-pdf.py INPUT_FILE /tmp/output.html --external-assets` |
| Google Slides download | `curl -L "https://docs.google.com/presentation/d/PRESENTATION_ID/export/pptx" -o /tmp/slides.pptx` |

If `python-pptx` is missing, tell the user to run `pip install python-pptx`. If Google Slides download fails, the deck may not be publicly accessible; ask the user to make it viewable or download the PPTX manually.

## Large file and asset rules

| Condition | Behavior |
| --- | --- |
| PPTX larger than 20MB or more than 50 images | The conversion scripts switch to external assets mode and save images under `assets/`. |
| PDF larger than 20MB or more than 50 pages | The conversion scripts save page PNGs under `assets/`. |
| File larger than 150MB | Print a warning; for PPTX, suggest converting through the PDF path. |
| Small file | Produce a single self-contained HTML file unless `--external-assets` is set. |
| Need to override detection | Use `--external-assets` or `--no-external-assets`. |

External assets mode keeps individual files below GitHub's 100MB limit. The output HTML references files in `assets/`, and `scripts/publish.sh` automatically copies the sibling `assets/` directory.

## Publishing procedure

1. Convert the input to an `index.html`-compatible file.
2. Confirm the HTML file and any sibling `assets/` directory are in the same parent directory.
3. Run the bundled publisher:

```bash
bash SKILL_DIR/scripts/publish.sh /path/to/index.html REPO_NAME public "Description"
```

Pass `private` instead of `public` only when the user requests a private repository. The script creates the repository, pushes `index.html` plus `assets/` when present, and enables GitHub Pages.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| Repo already exists | `REPO_NAME` is taken | Suggest `my-slides-2` or `my-slides-2026`. |
| Pages enablement fails | GitHub API or plan constraint | Return the repository URL and tell the user to enable Pages in repository Settings. |
| PPTX conversion fails | Missing `python-pptx` | Run `pip install python-pptx`. |
| PDF conversion fails | Missing `pdftoppm` or Poppler | Install `poppler-utils` with `apt install poppler-utils` or `brew install poppler`. |
| Google Slides download fails | Presentation is private | Make it viewable or download the PPTX manually. |
| Assets missing on Pages | `assets/` was not beside the HTML file | Move `assets/` next to `index.html` and republish. |

## Progressive disclosure and bundled resources

- `scripts/convert-pptx.py`: converts PPTX input to slide HTML, with optional external assets.
- `scripts/convert-pdf.py`: renders PDF pages to navigable HTML, using Poppler when available.
- `scripts/publish.sh`: creates or updates the GitHub repository, pushes files, and enables Pages.

Private repositories use `--private`; public repositories remain the default.

## Output template

```markdown
## GitHub Pages publish result

**Status:** published | blocked
**Repository:** `https://github.com/USERNAME/REPO_NAME`
**Live URL:** `https://USERNAME.github.io/REPO_NAME/`

### Source
- Input: `<INPUT_FILE or Google Slides URL>`
- Conversion: `html | pptx | pdf | google-slides`
- Assets mode: `self-contained | external assets`

### Validation
- `gh auth status`: `<pass/fail>`
- Conversion command: `<pass/fail/not needed>`
- Publish command: `<pass/fail>`

**Note:** GitHub Pages can take 1-2 minutes to go live.
```

## Quality gate

- [ ] `gh`, `gh auth status`, and `python3` prerequisite checks were run or explicitly blocked.
- [ ] Input type was classified as HTML, PPTX, PDF, or Google Slides.
- [ ] `PRESENTATION_ID` was extracted for Google Slides downloads.
- [ ] Large-file mode was selected correctly, including `--external-assets` or `--no-external-assets` when forced.
- [ ] The HTML file and any `assets/` directory shared the same parent before publishing.
- [ ] Repository visibility matched the user's request: `public` by default, `private` only when requested.
- [ ] The final response included both repository and live Pages URLs.

## References

- [GitHub CLI](https://cli.github.com)
