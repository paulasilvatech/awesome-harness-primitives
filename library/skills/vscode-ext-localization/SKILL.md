---
name: "vscode-ext-localization"
description: >-
  Localize VS Code extensions across package.json contributions, walkthrough markdown, and user-facing JavaScript/TypeScript strings using VS Code l10n conventions. Use when adding or updating localized settings, commands, menus, views, walkthroughs, messages, or string resources shown to extension users.
---

# VS Code extension localization

Identify user-facing VS Code extension strings, map each string to the correct localization file type, and produce complete locale updates for package contributions, walkthrough markdown, and runtime source messages.

## When to invoke

- "Localize this VS Code extension."
- "Add Brazilian Portuguese strings for commands and settings."
- "Localize package.json contributions."
- "Move extension messages into VS Code l10n files."
- "Update walkthrough markdown localization."

## Localization targets

VS Code extension localization uses three different approaches. When a new localizable resource is created or updated, update the corresponding localization for all currently available languages.

| Resource | Source location | Localization artifact | Example |
| --- | --- | --- | --- |
| Contributed configurations | `package.json` settings, commands, menus, views, `ViewsWelcome / `viewsWelcome``, walkthrough titles and descriptions | `package.nls.LANGID.json` | `package.nls.pt-br.json` for Brazilian Portuguese `pt-br` |
| Walkthrough content | Markdown files referenced by walkthrough steps | Locale-specific Markdown file beside the source | `walkthrough/someStep.pt-br.md` |
| Runtime messages | JavaScript or TypeScript strings displayed to the end user | `bundle.l10n.LANGID.json` | `bundle.l10n.pt-br.json` |

## Package contribution rules

| Contribution | Localize | Do not localize |
| --- | --- | --- |
| Configuration title/description | Human-readable labels and setting descriptions. | Setting keys, enum values used by code, default values unless they are display text. |
| Commands | `title`, `category`, menu-visible labels. | Command IDs such as `extension.doThing`. |
| Menus and views | User-visible group labels, view names, welcome text. | Context keys, `when` clauses, view IDs. |
| Walkthrough metadata | Titles, descriptions, button labels. | Stable IDs and file paths. |

Use `%key%` placeholders in `package.json` for localized contribution strings and define matching keys in every `package.nls.LANGID.json` file that the extension ships.

## Runtime string rules

| Pattern | Use | Notes |
| --- | --- | --- |
| `vscode.l10n.t('Message')` | User-facing runtime text in TypeScript/JavaScript. | Prefer stable messages with placeholders over concatenation. |
| `vscode.l10n.t('Open {0}', name)` | Values inserted into localized messages. | Keeps grammar flexible for translators. |
| `bundle.l10n.pt-br.json` | Translated runtime messages for Brazilian Portuguese. | Keep keys synchronized with extracted or source messages. |
| Non-user logs | Keep unlocalized unless they appear in UI. | Developer diagnostics can remain English if not user-facing. |

## Coverage checklist

- Settings, commands, menus, views, `ViewsWelcome / `viewsWelcome``, and walkthrough titles/descriptions in `package.json` have corresponding entries in `package.nls.LANGID.json` files.
- Walkthrough Markdown files have matching localized Markdown files, such as `walkthrough/someStep.pt-br.md`, for each currently available language.
- User-facing JavaScript or TypeScript messages are represented in `bundle.l10n.LANGID.json`, such as `bundle.l10n.pt-br.json`.
- All existing locales receive updates when a new localizable resource is added or created/updated.
- Placeholder order and meaning are preserved across languages.
- IDs, command names, configuration keys, file paths, and `when` expressions remain stable and unlocalized.

## Gotchas

- **Do not translate identifiers**: command IDs, setting keys, view IDs, context keys, and file paths are API surface.
- **Do not update only one locale**: every currently available language must be created or updated for the changed resource.
- **Do not concatenate translated sentences**: use placeholders so translators can reorder grammar.
- **Do not put walkthrough body text in `package.nls.LANGID.json`**: localize walkthrough Markdown with locale-specific Markdown files.

## Output template

````markdown
## VS Code extension localization result

**Status:** complete | needs translations | blocked
**Locales updated:** <LANGID list>

| Resource | Source | Localization file | Action |
| --- | --- | --- | --- |
| package contribution | `package.json` | `package.nls.pt-br.json` | added keys |
| walkthrough markdown | `walkthrough/someStep.md` | `walkthrough/someStep.pt-br.md` | updated file |
| runtime message | `src/extension.ts` | `bundle.l10n.pt-br.json` | added translation |

### Validation
- <check performed>: pass | fail
````

## Quality gate

- [ ] `package.json` contribution strings are localized through `package.nls.LANGID.json` files.
- [ ] Walkthrough `Markdown` content is localized through matching locale-specific Markdown files.
- [ ] User-facing JavaScript or TypeScript strings are localized through `bundle.l10n.LANGID.json` files.
- [ ] Every currently available language was created or updated for each changed localizable resource.
- [ ] Identifiers, keys, paths, `when` clauses, and defaults that are not display text remain unlocalized.
- [ ] Placeholder counts and meanings match between source and translated strings.
