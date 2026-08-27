---
paths:
  - "**/*.md"
---

<!-- Generated from harness/github-copilot/instructions/markdown-accessibility.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Markdown accessibility conventions for links, image alt text, headings, plain language, lists, emoji, multimedia, and review priority. Use when writing or reviewing Markdown documentation.

# Markdown Accessibility Conventions — Inclusive Documentation

These instructions apply to Markdown documentation and reviews. They are authoritative for accessible links, alt text, heading hierarchy, plain language, lists, emoji, multimedia, tables, and review tone in matched files; project documentation style guides and legal accessibility requirements win where they define stricter standards.

## Links and Images

Use descriptive links that make sense out of context. Flag generic link text such as `click here`, `here`, `this`, `read more`, or `link`. Flag multiple links on the same page with identical text that point to different destinations. Convert bare URLs in prose to descriptive links.

**Good:** `Read my blog post "[Crafting an accessible resume](https://example.com)"`
**Bad:** `Read my blog post [here](https://example.com)`

For images, flag empty alt text such as `![](path/to/image.png)` unless the image is explicitly decorative. Flag alt text that is a filename such as `img_1234.jpg` or a generic placeholder such as `screenshot` or `image`. Keep alt text succinct and descriptive, include text visible in the image, use `screenshot of` where relevant, and do not prefix with `image of` because screen readers announce images automatically. For charts and infographics, summarize the data in alt text and provide longer descriptions through `<details>` tags or linked content. Present alt text changes as recommendations for the author to review.

## Heading Hierarchy and Plain Language

Use only one H1 (`#`) per document as the page title. In projects where H1 is auto-generated from front matter, start content at H2. Do not skip heading levels, such as `##` followed by `####`, and flag bold text such as `**text**` used as a visual substitute for a heading. Proper heading structure helps assistive technology users navigate by section and helps sighted users scan content.

Favor short sentences, common words, and active voice. Flag unnecessarily complex or jargon-heavy language, long dense paragraphs, and UI navigation described only by visual breadcrumb notation or icon names. Write actions as sequential plain-language steps first, such as `open Settings, then select Preferences`; visual context such as `(gear icon > Preferences)` may follow only as supplemental information. Present language improvements as recommendations for the author to review.

## Lists, Emoji, Multimedia, and Tables

Use proper Markdown list syntax with `-`, `*`, `+`, or `1.`. Flag emoji or special characters used as bullets, and flag sequential plain text that should be a list. Use emoji sparingly, flag multiple consecutive emoji, and ensure emoji never carry meaning that is not also communicated in text. Provide captions for videos and transcripts for recorded audio. Do not auto-play audio or video. Prefer animations paused on page load. Avoid opening links in a new tab or window. Do not rely on bold or italics for critical information because screen readers often do not announce emphasis. Use tables for data only; avoid layout tables, nested tables, and complex tables that standard Markdown cannot represent accessibly.

## Review Priority and Tone

Prioritize issues in this order: missing or empty alt text, skipped heading levels or hierarchy issues, non-descriptive link text, emoji used as bullet points or list markers, plain language improvements, multimedia, then other issues. Explain the accessibility impact and affected users, such as screen reader users, people with cognitive disabilities, or non-native speakers. Keep suggestions actionable and specific without removing the author's personality or voice.

## Good / Bad Examples

The examples below illustrate accessible links and headings.

**Good**

```markdown
# Deployment guide

## Configure credentials

Read [GitHub's profile accessibility tips](https://github.blog/developer-skills/github/5-tips-for-making-your-github-profile-page-accessible/).
```

Why: the document has one H1, a proper H2, and descriptive link text.

**Bad**

```markdown
# Deployment guide

#### Credentials

Read more [here](https://www.smashingmagazine.com/2021/09/improving-accessibility-of-markdown/).
```

Why: the heading skips levels and the link text is not meaningful out of context.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use descriptive, unique link text and avoid bare URLs in prose. | Assistive technology can present links as an isolated list. |
| Provide succinct, contextual alt text and longer descriptions for complex images. | Screen reader users need equivalent content for visual information. |
| Keep one H1 and a logical heading hierarchy without skipped levels. | Headings provide navigation and document structure. |
| Use plain language and sequential UI instructions. | People with cognitive disabilities and non-native speakers can follow the content. |
| Use proper Markdown lists and sparing emoji with text equivalents. | Screen readers announce list context and emoji names predictably. |
| Provide captions, transcripts, and non-autoplay multimedia. | Audio and video content remains accessible to more users. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Recommend alt text changes for author review. | Invent visual meaning when image context is unclear. |
| Use `<label>`-like descriptive text in Markdown links. | Use `click here`, `here`, `this`, `read more`, or `link` as link text. |
| Break dense paragraphs into sections or lists. | Preserve jargon-heavy blocks when simpler language works. |
| Use tables only for data. | Use tables for page layout or nested complex structures. |
| Explain impact and affected users in review comments. | Remove voice or personality in the name of accessibility. |

## Checklist Before Opening a PR

- [ ] Link text is descriptive, unique when destinations differ, and not a bare URL in prose.
- [ ] Images have meaningful alt text or are explicitly decorative; complex images have longer descriptions.
- [ ] The document has one H1 and headings do not skip levels.
- [ ] Plain language, short sentences, active voice, and sequential UI instructions are used where appropriate.
- [ ] Lists use Markdown list syntax, and emoji do not carry meaning alone.
- [ ] Videos have captions, audio has transcripts, and media does not auto-play.
- [ ] Tables are for data only and avoid nested or overly complex structures.

## References

- GitHub accessibility tips: https://github.blog/developer-skills/github/5-tips-for-making-your-github-profile-page-accessible/
- Improving The Accessibility Of Your Markdown: https://www.smashingmagazine.com/2021/09/improving-accessibility-of-markdown/
