---
paths:
  - "**/*.md"
---

<!-- Generated from harness/github-copilot/instructions/markdown-gfm.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Conventions for GitHub Flavored Markdown files covering CommonMark-compatible blocks, GFM tables, task lists, links, HTML, and validation.

# GitHub Flavored Markdown Conventions — GFM Compatibility

These instructions apply to Markdown files matched by the `applyTo` glob. They are authoritative for GitHub Flavored Markdown block structure, inline syntax, tables, task lists, links, raw HTML, and validation; repository documentation templates, product-specific docs rules, and stricter accessibility or style primitives win where they impose narrower requirements.

## Preliminaries

Apply these rules per the GFM spec at https://github.github.com/gfm/ when writing or reviewing `.md` files. GFM is a strict superset of CommonMark. Use the GFM spec as reference only; do not download the GFM Spec.

- A line ends at a newline (`U+000A`), carriage return (`U+000D`), or end of file.
- A blank line contains only spaces or tabs.
- Tabs behave as 4-space tab stops for block structure but are not expanded in content.
- Replace `U+0000` with the replacement character `U+FFFD`.

## Leaf Blocks

| Construct | Convention |
| --- | --- |
| Thematic breaks | Use 3+ matching `-`, `_`, or `*` characters on a line with 0–3 spaces indent and no other characters; they may interrupt a paragraph |
| ATX headings | Use 1–6 `#` characters followed by a space or end of line; optional closing `#` must be preceded by a space; 0–3 spaces indent is allowed |
| Setext headings | Underline text with `=` (level 1) or `-` (level 2); they cannot interrupt a paragraph and need a blank line after a preceding paragraph |
| Indented code blocks | Indent lines 4+ spaces; they cannot interrupt a paragraph and content is literal text |
| Fenced code blocks | Open with 3+ backticks or tildes, do not mix fence characters, close with the same character and at least the same count, and specify a language identifier |
| HTML blocks | Preserve the seven GFM HTML block types and pass raw HTML through according to their start and end conditions |
| Link reference definitions | Use `[label]: destination "title"`; label matching is case-insensitive, first definition wins, and definitions cannot interrupt a paragraph |
| Paragraphs | Use consecutive non-blank lines not interpretable as another block; leading spaces up to 3 are stripped |
| Blank lines | Use blank lines to separate blocks and determine whether a list is tight or loose |
| Tables | Use a header row, delimiter row (`---`, `:---:`, `---:`), and zero or more data rows. Escape literal pipe as `\|`; delimit cells with `|` and keep header and delimiter column counts matching |

For HTML blocks, preserve these type rules: Type 1 starts with `<script>`, `<pre>`, or `<style>` and ends at the matching closing tag; Type 2 starts with `<!--` and ends at `-->`; Type 3 starts with `<?` and ends at `?>`; Type 4 starts with `<!` plus an uppercase letter such as `<!DOCTYPE>` and ends at `>`; Type 5 starts with `<![CDATA[` (`<![CDATA[`) and ends at `]]>`; Type 6 starts with a block-level tag such as `<div>` (`<div>`), `<table>` (`<table>`), `<p>`, `<h1>` (`<h1>`)–`<h6>`, `<ul>`, `<ol>`, or `<section>` and ends at a blank line; Type 7 is any other complete open or closing tag on its own line, ends at a blank line, and cannot interrupt a paragraph. Preserve the start/end conditions for every HTML block type.

Preserve these GFM block tokens explicitly because they name parser branches:

- `<![CDATA[`
- `<div>`
- `<table>`
- `<h1>`
- `<h6>`
- `<ul>`
- `<ol>`
- `<section>`
- `) or ordered markers (1–9 digits + `
- `. Escape literal pipe as `

## Container Blocks

- Block quotes use lines prefixed with `>` optionally followed by a space. Lazy continuation is allowed for paragraph text only, and a blank line separates consecutive block quotes.
- List items use bullet markers `-`, `+`, or `*`, or ordered markers (1–9 digits + `.` or `)`).
- Determine list item content column by marker width plus spaces to the first non-whitespace character.
- Indent sublists to the content column.
- An ordered list interrupting a paragraph must start with `1`.
- Task list items use `- [ ]` for unchecked or `- [x]` for checked at the start of a list item paragraph; the space between `-` and `[` is required and nesting is allowed.
- Lists are sequences of same-type list items. Changing the bullet character or ordered delimiter starts a new list.
- A list is loose if any item is separated by a blank line.

## Inline Syntax

| Construct | Convention |
| --- | --- |
| Backslash escapes | `\` before any ASCII punctuation character renders the literal character; not recognized in code spans, code blocks, or autolinks |
| Entity and numeric references | Use valid HTML5 forms such as `&amp;`, `&#123;`, and `&#x7B;`; they are not recognized in code spans or code blocks and cannot replace structural characters |
| Code spans | Use backtick-delimited inline code; line endings convert to spaces; leading and trailing space are stripped when both are present; backslash escapes are literal |
| Emphasis | Use `*` or `_` for `<em>` and `**` or `__` for `<strong>` (`<strong>`); `_` is not allowed for intraword emphasis; left-flanking and right-flanking delimiter run rules apply |
| Delimiter runs | When one delimiter can both open and close, delimiter run length sum must not be a multiple of 3 unless both lengths are multiples of 3 |
| Strikethrough | Use exactly `~~text~~`; one or two tildes are recognized, it does not span paragraphs, and 3+ tildes do not create strikethrough |
| Links | Use inline `[text](url "title")`, reference `[text][label]`, collapsed `[text][]`, or shortcut `[text]`; link text may contain inlines but not other links; no whitespace before `(` or `[` |
| Images | Use `![alt](src "title")`; alt text is the plain-string content of the description |
| Autolinks | Use `<URI>` or `<email>` in angle brackets; schemes are 2–32 characters and start with an ASCII letter |
| GFM autolinks | Bare `http://`, `https://`, `www.`, and bare email addresses auto-link; trailing punctuation is excluded and parentheses are balanced |
| Raw HTML | Open and close tags (Open/close tags), comments `<!-- -->`, processing instructions `<? ?>`, declarations `<!…>`, and CDATA `<![CDATA[…]]>` pass through |

Preserve the inline token `<strong>` when documenting strong emphasis.
| Disallowed raw HTML | `<title>`, `<textarea>`, `<style>`, `<xmp>`, `<iframe>`, `<noembed>`, `<noframes>`, `<script>`, and `<plaintext>` have their leading `<` replaced with `&lt;` |
| Hard line breaks | Use two+ trailing spaces or `\` before a line ending; not recognized in code spans or HTML tags |
| Soft line breaks | A line ending not preceded by two+ spaces or `\` renders as a space in browsers |

## Good / Bad Examples

The examples below illustrate table and fenced-code requirements.

**Good:**

````markdown
| Name | Value |
| --- | --- |
| Pipe | `\|` |

```text
literal content
```
````

Why: The table has matching header and delimiter counts, escapes the literal pipe, and the fenced code block has a language identifier.

**Bad:**

````markdown
| Name | Value |
| --- |
| Pipe | | |

```
literal content
```
````

Why: The table column counts do not match, literal pipes are unescaped, and the fenced code block omits a language identifier.

## Conventions

| Rule | Rationale |
|---|---|
| Follow GFM as a strict superset of CommonMark and use the spec at https://github.github.com/gfm/ only as a reference | Markdown renders consistently on GitHub without downloading external specs |
| Use correct line endings, blank lines, tab stops, and `U+FFFD` replacement for `U+0000` | Block parsing depends on these preliminaries |
| Format headings, thematic breaks, code blocks, HTML blocks, link definitions, paragraphs, blank lines, and tables according to GFM block rules | Documents parse into the intended structure |
| Format block quotes, list items, ordered lists, task list items, and loose or tight lists according to container rules | Nested content stays stable across renderers |
| Use valid escapes, entities, code spans, emphasis, strikethrough, links, images, autolinks, raw HTML, hard breaks, and soft breaks | Inline content renders predictably |
| Avoid disallowed raw HTML tags such as `<script>`, `<style>`, `<title>`, `<textarea>`, `<xmp>`, `<iframe>`, `<noembed>`, `<noframes>`, and `<plaintext>` | GitHub sanitization changes unsafe or unsupported HTML |

## Do / Do Not

| Do | Do not |
|---|---|
| Use ATX headings with 1–6 `#` followed by a space | Omit the required space after `#` |
| Add language identifiers to fenced code blocks | Leave fences unlabeled or mix backticks and tildes |
| Keep table header and delimiter column counts matching | Let a table break on the first blank line or malformed row unintentionally |
| Write task items as `- [ ]` or `- [x]` | Omit the space between `-` and `[` |
| Use `*` for intraword emphasis | Use `_` inside words and rely on inconsistent emphasis parsing |
| Use exactly `~~` for strikethrough | Use 3+ tildes expecting strikethrough |
| Keep links adjacent to `(` or `[` | Add whitespace between link text and the destination marker |
| Escape literal table pipes as `\|` | Put unescaped `|` inside table cell text |

## Checklist Before Opening a PR

- [ ] ATX headings use 1–6 `#` followed by a space.
- [ ] Fenced code blocks specify a language identifier and use matching fence characters and counts.
- [ ] Tables include header and delimiter rows with matching column count and escape literal pipes as `\|`.
- [ ] Task list items have a space between `-` and `[ ]` or `[x]`.
- [ ] Lists, block quotes, and nested content use valid GFM indentation and marker rules.
- [ ] Emphasis uses `*` for intraword; `_` appears only at word boundaries.
- [ ] Strikethrough uses exactly `~~`, not 3+ tildes.
- [ ] Links use `[text](url)` or reference syntax with no whitespace before `(` or `[`.
- [ ] Autolinks, entity references, code spans, hard breaks, and soft breaks follow GFM rules.
- [ ] No disallowed raw HTML tags appear: `<script>`, `<style>`, `<title>`, `<textarea>`, `<xmp>`, `<iframe>`, `<noembed>`, `<noframes>`, `<plaintext>`.

## References

- GitHub Flavored Markdown specification: https://github.github.com/gfm/
