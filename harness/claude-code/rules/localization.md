---
paths:
  - "**/*.md"
---

<!-- Generated from harness/github-copilot/instructions/localization.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces markdown localization conventions for translated document sets, locale folders, link rewriting, completeness checks, and required disclaimers.

# Localization Conventions — Markdown Translation Sets

These instructions apply to Markdown documents that are localized into another locale. They are authoritative for translation completeness, locale folder layout, localized link targets, image link handling, and the required GitHub Copilot disclaimer in matched `**/*.md` files; project documentation style or product terminology glossaries win where they define stricter wording for a specific document set.

## Locale and Folder Layout

Place every localized document under `localization/{{locale}}` and keep the original document structure beneath that folder so source and localized paths can be compared mechanically.

| Requirement | Convention |
| --- | --- |
| Locale shape | Use `{{language code}}-{{region code}}` with the language code from ISO 639-1 and the region code from ISO 3166. |
| Locale casing | Keep locale examples lowercase, such as `en-us`, `fr-ca`, `ja-jp`, `ko-kr`, `pt-br`, and `zh-cn`, unless the project explicitly requires another casing. |
| File coverage | Localize all Markdown documents in scope; do not skip nested pages, appendices, tables, headings, notes, or list items. |
| Destination root | Write translated files only under `localization/{{locale}}`, not beside the source file. |

## Translation Completeness

Localize every heading, section, paragraph, table cell, list item, callout, caption, and code-adjacent explanation from the original document. Preserve Markdown structure, heading hierarchy, fenced code block boundaries, frontmatter that must remain machine-readable, and placeholder syntax such as `{{locale}}`, `{{language code}}`, and `{{region code}}`.

Keep technical identifiers, commands, product names, paths, and code samples unchanged unless the original document explicitly marks them as translatable text. Compare the result to the original line-by-line; if the localized file has a different line count, treat that as evidence of a potentially missing section or paragraph until reviewed.

## Links, Images, and Cross-Document Targets

| Link type | Convention |
| --- | --- |
| Image links | Point image links to the original image unless the image URL is external or a localized image asset is explicitly provided. |
| Document links | Rewrite internal document links to the localized document under `localization/{{locale}}` when the target is part of the translated set. |
| External links | Leave external links unchanged, including `https://docs.github.com/copilot/about-github-copilot/what-is-github-copilot` and `https://github.com/github/awesome-copilot/issues`. |
| Anchors | Preserve anchors when rewriting localized document links so section references continue to resolve. |

## Required Disclaimer

ALWAYS add the localized disclaimer to the end of each localized document. Keep the horizontal rule and both links, and translate the visible disclaimer text into the target locale.

```text
---

**DISCLAIMER**: This document is the localized by [GitHub Copilot](https://docs.github.com/copilot/about-github-copilot/what-is-github-copilot). Therefore, it may contain mistakes. If you find any translation that is inappropriate or mistake, please create an [issue](https://github.com/github/awesome-copilot/issues).
```

## Good / Bad Examples

The examples below illustrate preserving structure while rewriting internal document links for a `pt-br` localization.

**Good:**

```markdown
See [installation](../install.md) in the source.
See [instalação](../../localization/pt-br/install.md) in the localized document.
```

Why: The localized text translates the label, points to the localized document, and leaves the document relationship explicit.

**Bad:**

```markdown
See installation.
```

Why: The localized document dropped the link target and lost navigational behavior from the source.

## Conventions

| Rule | Rationale |
|---|---|
| Place localized Markdown under `localization/{{locale}}` | A stable folder convention lets reviewers compare source and translation sets. |
| Use ISO 639-1 language codes and ISO 3166 region codes in locale names | Standard locale names avoid ambiguous translation targets. |
| Localize every section and paragraph from the original document | Missing prose changes the document contract for localized readers. |
| Preserve code, paths, placeholders, commands, and product identifiers unless they are natural-language text | Technical content must remain executable and searchable. |
| Rewrite internal document links to localized documents and keep external links unchanged | Readers stay inside the localized set without breaking references to canonical external resources. |
| Append the localized `DISCLAIMER` with the GitHub Copilot and issue links intact | Readers receive the required quality notice and a feedback path. |

## Do / Do Not

| Do | Do not |
|---|---|
| Use locale folders such as `localization/ja-jp` and `localization/pt-br` | Write translated files beside the originals or into an ad hoc folder. |
| Translate headings, paragraphs, tables, and callouts | Leave prose untranslated because the Markdown structure looks complete. |
| Keep image links pointing to original assets unless a localized asset exists | Break images by inventing localized image paths. |
| Rewrite document links to localized targets when the target was translated | Point localized pages back to source-language documents unnecessarily. |
| Compare source and localized line counts and review differences line-by-line | Assume a different line count is harmless without checking for lost sections. |

## Checklist Before Opening a PR

- [ ] Every in-scope Markdown document has a localized counterpart under `localization/{{locale}}`.
- [ ] The locale name follows `{{language code}}-{{region code}}` using ISO 639-1 and ISO 3166.
- [ ] All source headings, sections, paragraphs, tables, lists, and callouts are represented in the localized file.
- [ ] Code, commands, paths, placeholders, and product identifiers remain technically correct.
- [ ] Image links point to valid original or explicitly localized assets.
- [ ] Internal document links point to localized documents when available, and external links remain unchanged.
- [ ] The localized `DISCLAIMER` is present at the end of every localized document with both required links intact.
- [ ] Line-count differences from the source have been reviewed line-by-line.

## References

- GitHub Copilot overview: https://docs.github.com/copilot/about-github-copilot/what-is-github-copilot
- GitHub awesome-copilot issues: https://github.com/github/awesome-copilot/issues
