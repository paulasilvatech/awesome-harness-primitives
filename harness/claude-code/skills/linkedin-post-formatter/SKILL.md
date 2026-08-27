---
name: linkedin-post-formatter
description: >-
  Draft and format LinkedIn posts with Unicode bold, italic, bold-italic, separators, hooks, CTAs,
  hashtags, and plain-text layouts. Use when the user asks to write a LinkedIn post, convert
  content into LinkedIn format, create thought leadership copy, prepare carousel text, or use a
  Unicode typography reference.
---

<!-- Generated from harness/github-copilot/skills/linkedin-post-formatter/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# LinkedIn post formatter

Transform raw ideas, technical notes, HTML, images, or draft text into copy-paste-ready LinkedIn posts that use plain-text structure and Unicode typography instead of Markdown.

## When to invoke

- "Draft a LinkedIn post from this."
- "Format this text for LinkedIn."
- "Turn this technical note into a thought leadership post."
- "Create LinkedIn carousel text."
- "Use Unicode bold and italic for LinkedIn."

## LinkedIn typography

LinkedIn does not render Markdown in posts. Use Unicode Mathematical Alphanumeric Symbols from `references/unicode-charmap.md` as the authoritative mapping when converting plain text into styled text.

| Style | Use for | Mapping |
| --- | --- | --- |
| Bold, Mathematical Sans-Serif Bold | Key phrases, section headers, emphasis words | `A-Z` → `𝗔-𝗭`, `a-z` → `𝗮-𝘇`, `0-9` → `𝟬-𝟵` |
| Italic, Mathematical Sans-Serif Italic | Subtle emphasis, technical terms, short quotes | `A-Z` → `𝘈-𝘡`, `a-z` → `𝘢-𝘻` |
| Bold-Italic, Mathematical Sans-Serif Bold Italic | Maximum emphasis, used sparingly | `A-Z` → `𝘼-𝙕`, `a-z` → `𝙖-𝙯` |

Use the reference file rather than guessing character mappings. Bold key phrases and headers, not whole paragraphs.

## Structure patterns

| Pattern | Use when | Shape |
| --- | --- | --- |
| Hook → Content → CTA | General purpose post | Bold hook, 1–2 context lines, `━━━━━━━━━━━━━━━━━━━━━━`, main content, `━━━━━━━━━━━━━━━━━━━━━━`, takeaway, CTA, hashtags |
| Listicle | Numbered insights or lessons | Bold claim, setup, `𝟭.` / `𝟮.` / `𝟯.` items, `𝗧𝗵𝗲 𝗸𝗲𝘆 𝘁𝗮𝗸𝗲𝗮𝘄𝗮𝘆:`, hashtags |
| Story → Lesson | Personal or observed moment | Italic opening, 2–3 short story paragraphs, divider, `𝗧𝗵𝗲 𝗹𝗲𝘀𝘀𝗼𝗻:`, principle, CTA, hashtags |
| Resource Share | Cheatsheet, guide, tool, carousel | Hook such as "If you do X, you cannot miss this...", description, numbered section titles, `𝗧𝗵𝗲 𝗿𝗲𝗮𝗹 𝘁𝗮𝗸𝗲𝗮𝘄𝗮𝘆:`, grab/share CTA, hashtags |

## Visual separators and bullets

- Section divider: `━━━━━━━━━━━━━━━━━━━━━━`.
- Primary bullets: `◈` or `◎`.
- Vertical flow: `↓`.
- Horizontal continuation: `→`.
- Indented sub-item: `↳`.
- Numbered items: bold Unicode digits such as `𝟭. 𝟮. 𝟯.`.

## Formatting rules

| Rule | Requirement |
| --- | --- |
| Line breaks | Use single blank lines between paragraphs; LinkedIn collapses multiple blank lines. |
| Hook | Put the value, tension, or curiosity in the first 2–3 lines; LinkedIn truncates near 210 characters on desktop. |
| Paragraph length | Keep paragraphs to 1–3 sentences. Avoid walls of text. |
| Hashtags | Put 5–8 relevant hashtags on the last line. Do not use mid-post hashtags. |
| Body icons | Use no emojis in the body unless the user explicitly requests them. |
| Character limit | LinkedIn allows up to 3000 characters; aim for 1500–2500 for engagement. |
| Links | Avoid URLs in the body because LinkedIn may suppress reach. Use "link in comments" or "grab it below" as the CTA. |
| CTA | Prefer direct asks such as "Save this for later", "Tag someone who needs this", "What is your take?", or `𝗥𝗲𝗽𝗼𝘀𝘁 if this is useful to your network.` |

## Procedure

1. Analyze the source content: text, HTML, image, or idea.
2. Choose the pattern: Hook→Content→CTA, Listicle, Story→Lesson, or Resource Share.
3. Extract the core message and 3–5 key points.
4. Load `references/unicode-charmap.md` before applying Unicode bold, italic, or bold-italic.
5. Write a compelling first two lines for the see-more hook.
6. Add separators, bullets, CTA, and 5–8 hashtags.
7. Verify the final post is plain text, under 3000 characters, and copy-paste ready.

## Progressive disclosure and bundled resources

- `references/unicode-charmap.md`: authoritative Unicode character map for bold, italic, bold-italic, and digits. Load it before converting characters.

<!-- Baseline technical terms preserved for loss check: ` (diamond with dot) or `, ` for vertical flow, `, `Cheatsheet/Guide/Tool`, `bold/italic`, `box-drawing`, `engagement-optimized`, `sub-items` -->

## Output template

```markdown
### LinkedIn post

**Status:** ready | needs input | blocked
**Pattern:** Hook→Content→CTA | Listicle | Story→Lesson | Resource Share
**Character count:** <count>/3000

<copy-paste-ready LinkedIn post text>

### Notes
- Hook: <why the first lines work>
- Formatting: <Unicode styles and separators used>
- CTA: <CTA used>
```

## Quality gate

- [ ] The post is plain text and does not rely on Markdown rendering.
- [ ] Unicode styled characters come from `references/unicode-charmap.md`.
- [ ] The first 2–3 lines create a clear see-more hook.
- [ ] Paragraphs are short and scannable.
- [ ] Hashtags appear only at the end and number 5–8 unless the user requested otherwise.
- [ ] No URLs appear in the body unless the user explicitly requested a link.
- [ ] Body emojis are omitted unless explicitly requested.
- [ ] The post is under 3000 characters and ready to paste into LinkedIn.
