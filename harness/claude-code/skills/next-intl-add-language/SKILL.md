---
name: next-intl-add-language
description: >-
  Add a new locale to a Next.js application that uses next-intl, including message JSON, routing,
  middleware, and the language toggle UI. Use this skill when the user asks to add a language,
  locale, translation file, next-intl routing entry, or language selector option.
---

<!-- Generated from harness/github-copilot/skills/next-intl-add-language/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# next-intl add language

Add a complete locale to a Next.js + next-intl project by translating message JSON, wiring routing and middleware, updating the language toggle, and validating that every locale has the same message keys.

## When to invoke

- "Add Spanish to our next-intl app."
- "Create a new locale in `./messages`."
- "Update next-intl routing and middleware for a new language."
- "Add a language option to `src/components/language-toggle.tsx`."

## Project conventions

| Concern | Repository location | Required change |
| --- | --- | --- |
| Translation files | `./messages` | Create the new locale JSON by translating all entries from `en.json`. |
| Source locale | `./messages/en.json` | Treat keys and nesting as the complete schema. |
| Language toggle UI | `src/components/language-toggle.tsx` | Add the new language option, label, and locale value. |
| Routing | `src/i18n/routing.ts` | Add the locale to the next-intl routing configuration. |
| Middleware | `src/middleware.ts` | Add or confirm the locale is accepted by middleware matching/routing. |

## Procedure

1. Choose the locale code requested by the user, such as `es`, `fr`, `pt-BR`, or another BCP 47-style tag already consistent with the project.
2. Read `./messages/en.json` and preserve its complete key structure in the new locale file.
3. Translate every string value; do not leave English text unless it is a brand name, code literal, or user-approved untranslated term.
4. Update `src/i18n/routing.ts` so next-intl knows the new locale.
5. Update `src/middleware.ts` so requests for the new locale route correctly.
6. Update `src/components/language-toggle.tsx` so users can select the language.
7. Validate JSON syntax and compare key parity between `en.json` and the new file.

## Locale implementation rules

| Rule | Why it matters |
| --- | --- |
| Preserve every JSON key exactly. | next-intl lookups fail when keys are missing or renamed. |
| Preserve interpolation placeholders such as `{name}`. | Translations must not break runtime formatting. |
| Preserve rich-text tags or markup placeholders. | next-intl rich messages depend on matching tag names. |
| Use locale codes consistently across `./messages`, `routing.ts`, `middleware.ts`, and `language-toggle.tsx`. | Mixed `pt`/`pt-BR` values cause routing and selector bugs. |
| Keep JSON valid and sorted only if the source file is sorted. | Avoid noisy diffs unrelated to the added locale. |

## Gotchas

- **Do not partially translate**: the goal is complete translation coverage for all `en.json` entries.
- **Do not infer missing routing files**: this skill assumes routing and middleware live in `src/i18n/routing.ts` and `src/middleware.ts`.
- **Do not translate placeholders**: `{count}`, `{name}`, and tag names inside rich messages must remain intact.
- **Do not add a selector option without routing**: users can select a locale only if middleware and routing accept it.

## Output template

```markdown
## next-intl language addition

**Status:** complete | needs translation review | blocked
**Locale:** `<locale-code>`

| File | Change | Validation |
| --- | --- | --- |
| `./messages/<locale>.json` | translated from `en.json` | JSON valid; key parity pass/fail |
| `src/i18n/routing.ts` | locale added | route config includes locale pass/fail |
| `src/middleware.ts` | locale accepted | middleware includes locale pass/fail |
| `src/components/language-toggle.tsx` | language option added | UI option includes locale pass/fail |

**Human review needed:** <translation nuance, if any>
```

## Quality gate

- [ ] The new locale file exists under `./messages` and mirrors every key from `en.json`.
- [ ] All translatable content from `en.json` is translated or explicitly justified as intentionally unchanged.
- [ ] `src/i18n/routing.ts` includes the locale.
- [ ] `src/middleware.ts` accepts/routes the locale.
- [ ] `src/components/language-toggle.tsx` exposes the locale to users.
- [ ] JSON syntax is valid and interpolation placeholders are preserved.
