---
name: em-dash
description: >-
  Review and rewrite code, comments, documentation, and data files to avoid em dashes and en dashes by default. Use this skill when the user asks to remove em dashes, replace Unicode dashes with hyphens, review punctuation in code comments, or enforce ASCII-safe punctuation.
---

# Em dash

Detect em dash `U+2014` (`\u2014`), en dash `U+2013` (`\u2013`), Unicode replacement character `U+FFFD`, and risky punctuation in code-facing text, then replace or preserve them according to file purpose.

## When to invoke

- "Remove em dashes from these files."
- "Replace en dashes with hyphens in comments."
- "Review this code for punctuation that should not be in source files."
- "Make this text ASCII-safe for config or data files."
- "Explain when to use an em dash here."

## Dash policy

| Context | Rule | Action |
| --- | --- | --- |
| Code files and code comments | Never use em or en dashes. Tone is not important enough to justify non-keyboard punctuation in executable files. | Replace `—` and `–` with `-`. |
| Raw data or text files | Default to never. | Replace unless the user clearly says the text is literature, news, or source data where original punctuation must remain. |
| Literature or news | Preserve when the punctuation is intentionally part of the content. | Leave existing em dashes if instructed. |
| Unknown purpose | Fail toward compatibility. | Use hyphen-minus `-`. |

The em dash is historically a typesetting mark named for the width of the capital letter "M"; the en dash is named for "N" width. Typewriters used `--` because they lacked a true em dash. Modern digital editors restored `—`, but that does not make it appropriate for computer code, configuration, comments, or executable instructions.

## Punctuation guide for code-facing text

| Mark | Keyboard character | Programming syntax | Code-comment guidance | Example |
| --- | --- | --- | --- | --- |
| Period `.` | `true` | `true` | End complete statements. | `<?php echo "a" . "b" . "c"; ?>` |
| Question mark `?` | `true` | `true` | Use for direct questions only. | `condition ? expression_if_true : expression_if_false` |
| Exclamation point `!` | `true` | `true` | Avoid hype; acceptable when syntax or a real warning needs it. | `setlocal enabledelayedexpansion && set "_a=a" && echo !_a! && endlocal` |
| Comma `,` | `true` | `true` | Separate list items and clauses. | `fn(a, b)` |
| Semicolon `;` | `true` | `true` | Use for closely related independent clauses or syntax. | `var foobar = "foo-bar";` |
| Colon `:` | `true` | `true` | Introduce a list or explanation after a complete sentence. | `{"age": 26}` |
| Apostrophe `'` | `true` | `true` | Use for possessives or contractions when style allows. | `char letter = 'A';` |
| Quotation marks `"` | `true` | `true` | Enclose quoted text or literals. | `char abc[] = "abc";` |
| Hyphen `-` | `true` | `true` | Use for compound words and as the replacement dash. | `count--` |
| Slash `/` | `true` | `true` | Use for alternatives or syntax. | `/* comment */ || 10/2 || 5//2` |
| Parentheses `( )` | `true` | `true` | Enclose non-essential clarification. | `if (5 > 2)` |
| Brackets `[ ]` | `true` | `true` | Enclose inserted clarification or syntax. | `var arr = [1, 2, 3];` |
| En dash `–` | `false` | `false` | Do not use in code-facing text. | Replace with `-`. |
| Em dash `—` | `false` | `false` | Do not use in code-facing text. | Replace with `-`. |
| Replacement character `�` | `false` | `false` | Treat as encoding damage. | Replace with a space or recover original text. |

## Replacement commands

```bash
# Replace Unicode en dash (U+2013) and em dash (U+2014) with hyphen-minus (-)
perl -CS -pe 's/\x{2013}|\x{2014}/-/g'

# Remove the Unicode replacement character (U+FFFD) if it appears in pasted text
perl -CS -pe 's/\x{FFFD}/ /g'

# Pseudo-code reminder for en dash and em dash
printf '%s\n' '-' | sed 's/-/-/g'
```

Use a file-safe in-place command only after reviewing the target paths and repository conventions. Preserve line endings and encoding where possible.

## Gotchas

- **Do not replace meaningful minus signs with prose**: the target replacement is hyphen-minus `-`, not a word like "minus".
- **Do not preserve Unicode dashes in comments for tone**: code comments exist to clarify behavior, not to imitate literary rhythm.
- **Do not rewrite source data blindly**: if the file is a fixture, corpus, or pasted article where punctuation is the data, preserve it unless the user asks for normalization.
- **Do not introduce `--` as an em dash substitute**: in many languages and CLIs `--` has syntax meaning.

## Historical and syntax vocabulary

The historical context includes `self-interruption`, `long-form`, `stream-of-consciousness`, and `HTML` usage claims, but the code policy remains `NEVER` for em and en dashes in source. Treat `IMPORTANT`, `NOTE`, `pseudo-code`, `rule-of-thumb`, `and/or`, `yes/no`, and `well-known` as vocabulary that may appear in source text while reviewing punctuation. Preserve exact syntax examples when relevant: `<?php echo "a" . "b" . "c"; ?>`, `condition ? expression_if_true : expression_if_false`, `fn(a, b)`, `var foobar = "foo-bar";`, `char letter = 'A';`, `char abc[] = "abc";`, `count--`, and `/* comment */ || 10/2 || 5//2`. Use `false` for non-keyboard or non-syntax punctuation values.

## Output template

```markdown
### Em dash review result

**Status:** clean | changed | blocked
**Scope:** `<files or text reviewed>`

| Finding | Count | Action |
| --- | ---: | --- |
| Em dash `U+2014` / `\u2014` | <count> | replaced with `-` | preserved with reason |
| En dash `U+2013` / `\u2013` | <count> | replaced with `-` | preserved with reason |
| Replacement character `U+FFFD` | <count> | replaced with space | preserved with reason |

**Commands or edits used**
- `<command or manual edit summary>`
```

## Quality gate

- [ ] Code files and code comments contain no `U+2014` em dash or `U+2013` en dash unless explicitly justified as data.
- [ ] Replacements use hyphen-minus `-`.
- [ ] `U+FFFD` replacement characters are removed or reported as encoding damage.
- [ ] Literature, news, and raw-data exceptions are preserved only when the user clearly requested preservation.
- [ ] No `--` substitute was introduced where it could conflict with code or CLI syntax.
- [ ] The final result reports counts, scope, and action taken.

## References

- [Case for the em dash](https://www.hardingproject.com/p/the-case-for-the-em-dash)
- [em dash guide](https://www.thebookrefinery.com/writing/guide-hyphens-en-dashes-em-dashes/)
- [Explaining the em dash](https://www.reddit.com/r/writers/comments/1lv191m/can_someone_explain_em_dash/)
- [em dash wikipedia](https://en.wikipedia.org/wiki/Dash)
- [Verbose em dash history](https://www.linkedin.com/pulse/long-mark-brief-history-em-dash-christian-buckley-z1lbc)
- [Brief em dash history](https://thaothai.substack.com/p/a-brief-history-of-the-em-dash)
- [em dash punctuation](https://www.nytimes.com/2019/08/14/style/em-dash-punctuation.html)
- [em dash in retrospective](https://medium.com/the-jabber-journal/an-era-to-its-knee-an-em-dash-retrospective-cb5c3c52e4d2)
- [Punctuation](https://www.niu.edu/writing-tutorial/punctuation/index.shtml)
- [Punctuation Guide](https://www.thepunctuationguide.com/)
