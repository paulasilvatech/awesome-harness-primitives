---
applyTo: "**/*.md"
description: "Enforces CommonMark 0.31.2 block, inline, escaping, link, image, and HTML syntax conventions for Markdown files."
name: "CommonMark Markdown Conventions"
---

# CommonMark Markdown Conventions — Specification-Compatible Syntax

These instructions apply to Markdown files that should parse as CommonMark 0.31.2. They are authoritative for Markdown syntax, block parsing, inline parsing, escaping, links, images, autolinks, and HTML handling in matched files; content strategy, blog metadata, and publishing workflow rules belong to the Markdown Content Creation Conventions instruction where that narrower content primitive applies.

## Responsibility Split

This file owns CommonMark syntax for `.md` files: headings, lists, block quotes, code blocks, links, images, autolinks, emphasis, raw HTML, and line breaks. Markdown Content Creation Conventions owns blog-post metadata, editorial structure, line-length policy for authored posts, category and tag requirements, and publication readiness.

## Preliminaries and Character Handling

Apply the CommonMark spec 0.31.2 as the parsing reference. Use the specification for reference only; do not download CommonMark spec content into the repository.

- Treat a line as ending at newline `U+000A`, carriage return `U+000D`, or end of file.
- Treat a blank line as a line containing only spaces or tabs.
- Interpret tabs as 4-space tab stops for block structure, without expanding tabs inside literal content.
- Replace `U+0000` with the replacement character `U+FFFD`.
- Use backslash escapes only before ASCII punctuation characters, and remember they are not recognized in code spans, code blocks, or autolinks.
- Use valid HTML5 entity and numeric character references such as `&amp;`, `&#123;`, and `&#x7B;`; do not rely on them inside code spans or code blocks, and do not use them to replace structural Markdown characters.

## Leaf Blocks

| Block | Convention |
| --- | --- |
| Thematic breaks | Use 3 or more matching `-`, `_`, or `*` characters on a line indented 0-3 spaces; keep only spaces or tabs on that line. |
| ATX headings | Use 1-6 `#` characters followed by a space or end of line; optional closing `#` sequences need a preceding space. |
| Setext headings | Underline text with `=` for level 1 or `-` for level 2; do not let a setext heading interrupt a paragraph. |
| Indented code blocks | Indent literal code 4 or more spaces and precede it with a blank line because it cannot interrupt a paragraph. |
| Fenced code blocks | Open with 3 or more backticks or tildes, close with the same character and at least the same count, and specify a language identifier. |
| HTML blocks | Respect the seven CommonMark HTML block types and their end conditions; type 6 and type 7 end at a blank line. |
| Link reference definitions | Write `[label]: destination "title"`; matching is case-insensitive by Unicode case fold, and the first duplicate label wins. |
| Paragraphs | Use consecutive non-blank lines that are not another block construct; up to 3 leading spaces are stripped. |
| Blank lines | Use blank lines to separate blocks and to determine tight versus loose lists. |

Do not put backticks in the info string after an opening backtick fence. Do not mix backticks and tildes in the same fenced code block.

## Container Blocks

- Start block quotes with `>` optionally followed by a space; allow lazy continuation only for paragraph text.
- Separate consecutive block quotes with a blank line when they are distinct quotations.
- Use bullet markers `-`, `+`, or `*`, or ordered markers with 1-9 digits followed by `.` or `)`.
- Determine list content indentation from marker width plus 1-4 spaces to the first non-whitespace character.
- Indent sublists to the content column, not to an arbitrary visual column.
- Start an ordered list that interrupts a paragraph with `1`.
- Treat a sequence as a new list when the bullet character or ordered delimiter changes.
- Treat a list as loose if any item is separated by a blank line.

## Inline Syntax

| Inline | Convention |
| --- | --- |
| Code spans | Delimit with backticks; convert line endings to spaces and strip one leading and trailing space when both are present unless the content is all spaces. |
| Emphasis | Use `*` and `_` according to left-flanking and right-flanking delimiter runs; avoid `_` for intraword emphasis. |
| Strong emphasis | Use `**` or `__`; apply the delimiter run length rule when a delimiter can both open and close. |
| Links | Use inline `[text](url "title")`, reference `[text][label]`, collapsed `[text][]`, or shortcut `[text]`; do not nest links inside link text. |
| Link destinations | Use `<...>` when spaces are present; otherwise keep parentheses balanced or escaped and avoid whitespace between link text and `(` or `[`. |
| Images | Use `![alt](src "title")`; make alt text a meaningful plain-string description. |
| Autolinks | Use `<URI>` or `<email>` in angle brackets; the scheme starts with an ASCII letter and contains 2-32 characters. |
| Raw HTML | Pass through open and close tags, comments `<!-- ... -->`, processing instructions `<? ... ?>`, declarations `<! ... >`, and CDATA `<![CDATA[ ... ]]>` as literal HTML. |
| Hard line breaks | Use two or more trailing spaces or `\` before a line ending; do not expect them inside code spans or HTML tags. |
| Soft line breaks | Treat ordinary line endings as spaces in browser rendering. |

Bare URLs are not auto-linked CommonMark autolinks. Use angle brackets when the URL itself should become a link. Preserve CommonMark vocabulary for same-type lists, start/end tag conditions, Open/close tags, custom/inline-level tags, `<!--`, `), CDATA (`, `<strong>`, ` for intraword; `, ` for `, ` (level 1) or `, and `) or ordered markers (1–9 digits + ` when mapping syntax rules.

## Good / Bad Examples

The examples below illustrate fenced code, headings, links, and images that parse predictably under CommonMark.

**Good:**

```markdown
## Installation

Use the documented command:

```bash
python3 -m pip install example
```

Read the [CommonMark spec][commonmark] and include an image with alt text:

![Architecture diagram](architecture.png)

[commonmark]: https://spec.commonmark.org/0.31.2/
```

Why: The heading has a required space, the fenced code block has a language identifier and matching fences, the link has no whitespace before `(`, and the image has useful alt text.

**Bad:**

```markdown
##Installation

```bash`
python3 -m pip install example
```

Read [the spec] (https://spec.commonmark.org/0.31.2/) and see ![](architecture.png)
```

Why: The heading is not an ATX heading, the fence is malformed, whitespace breaks the inline link, and the image has empty alt text.

## Conventions

| Rule | Rationale |
| --- | --- |
| Follow CommonMark 0.31.2 syntax for block and inline parsing | Markdown renders consistently across compliant tools. |
| Use 1-6 ATX heading markers followed by a space | Headings parse as headings instead of paragraphs. |
| Give fenced code blocks a language identifier and matching fence characters | Code renders with syntax highlighting and closes predictably. |
| Use correct list marker indentation and start paragraph-interrupting ordered lists at `1` | Lists nest and continue as intended. |
| Prefer `*` for intraword emphasis and reserve `_` for word boundaries | Emphasis does not accidentally split identifiers or prose. |
| Use valid link, reference, image, and autolink syntax | Links and images survive CommonMark parsing without ambiguity. |
| Keep raw HTML within CommonMark's block and inline rules | HTML passes through intentionally instead of corrupting surrounding Markdown. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `## Heading` with a space after the marker | Write `##Heading`. |
| Use matching backtick or tilde fences with a language | Mix fence characters or omit the language identifier. |
| Put a blank line before indented code blocks | Let indented code attempt to interrupt a paragraph. |
| Use `[text](url)` or reference syntax without whitespace before delimiters | Write `[text] (url)` or unbalanced bare destinations. |
| Use `![descriptive alt](image.png)` | Use empty image alt text. |
| Use `<https://example.com>` for CommonMark autolinks | Assume bare URLs are autolinked by the CommonMark parser. |
| Use HTML entities outside code when they represent text | Use entities to replace Markdown structure. |

## Checklist Before Opening a PR

- [ ] ATX headings use 1-6 `#` characters followed by a space.
- [ ] Fenced code blocks specify a language identifier and use matching fence characters and counts.
- [ ] Backtick fence info strings do not contain backtick characters.
- [ ] Indented code blocks are preceded by a blank line.
- [ ] Lists use valid bullet or ordered markers, content-column indentation, and `1` for ordered paragraph interruption.
- [ ] Emphasis uses `*` for intraword cases and `_` only at word boundaries.
- [ ] Links use `[text](url)` or reference syntax with no whitespace before `(` or `[`.
- [ ] Images include non-empty alt text.
- [ ] Autolinks use angle brackets such as `<URL>`; bare URLs are not treated as CommonMark autolinks.
- [ ] HTML block type 7 is preceded by a blank line when it follows a paragraph.

## References

- CommonMark 0.31.2: https://spec.commonmark.org/0.31.2/
