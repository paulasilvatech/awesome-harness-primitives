---
name: mkdocs-translations
description: >-
  Translate an MkDocs documentation stack from docs/docs/en and docs/docs/includes/en into a target ISO 639-1 or locale folder, preserving Markdown structure and updating mkdocs.yml i18n locale, nav_translations, and admonition_translations. Use when the user asks for mkdocs ai translator, MkDocs translation, docs localization, or adding a new documentation locale.
---

# MkDocs translations

Translate every English MkDocs source file into a target locale, mirror the folder structure, update include paths and `mkdocs.yml`, and continue automatically until source and translated file counts match.

## When to invoke

- "Run the mkdocs ai translator for Spanish."
- "Translate our MkDocs docs to pt-BR."
- "Add a French locale to this documentation site."
- "Localize docs/docs/en and includes/en."
- "Update mkdocs.yml for a new translated locale."

## Inputs

Use the target translation language and locale code, such as Spanish `es`, French `fr`, Brazilian Portuguese `pt-BR`, or Korean `ko`. If the user did not provide both a language and a locale code, ask for them before proceeding. Use the locale code consistently in folder names, translated include paths, and MkDocs configuration.

## Source and output layout

| Source | Target |
| --- | --- |
| `docs/docs/en/**` | `docs/docs/<locale>/**` |
| `docs/docs/includes/en/**` | `docs/docs/includes/<locale>/**` |
| Include reference `includes/en/introduction-event.md` | `includes/<locale>/introduction-event.md` |
| `mkdocs.yml` i18n plugin | Add locale entry, `nav_translations`, and `admonition_translations`. |

Create a branch before writing files:

```bash
git checkout -b docs-translation-<language>
```

## Translation procedure

1. Confirm the target language and locale code.
2. Create `docs-translation-<language>` with `git checkout -b docs-translation-<language>` before creating any new files.
3. List all files and subdirectories under `docs/docs/en`.
4. List all files and subdirectories under `docs/docs/includes/en`.
5. Translate every file one by one in the listed order; do not skip, reorder, or stop after a fixed number of files.
6. Mirror the exact folder and filename structure under `docs/docs/<locale>/` and `docs/docs/includes/<locale>/`.
7. Preserve Markdown formatting, headings, code blocks, metadata, and links.
8. Update include references from `includes/en/...` to `includes/<locale>/...`.
9. Append `*Translated using GitHub Copilot and GPT-4o.*` at the end of every translated file.
10. Update `mkdocs.yml` with the new i18n locale entry, `nav_translations`, and `admonition_translations`.
11. Count source files and translated files. If any file remains unprocessed, resume from the missing file and continue automatically.

## Translation rules

| Do | Do not |
| --- | --- |
| Use accurate, clear, technically appropriate translations. | Do not wrap translated content or whole files in Markdown code blocks. |
| Use computer industry-standard terminology, such as "Stack Tecnológica" rather than "Pila Tecnológica". | Do not comment on or fix Markdown linting issues. |
| Preserve original filenames, folder hierarchy, Markdown formatting, metadata, links, and code blocks. | Do not mention missing blank lines, trailing punctuation in headings, missing alt text, heading levels, line length, or spacing. |
| Continue automatically until all files are translated. | Do not ask for confirmation between files or before continuing. |
| Maintain original code and commands unless the prose around them requires localization. | Do not translate code identifiers, paths, or configuration keys. |

## MkDocs configuration rules

Update only the localization-related configuration required for the new locale:

- Add a `locale` entry under the `i18n` plugin using the target locale code.
- Add appropriate `nav_translations`.
- Add appropriate `admonition_translations`.
- Keep existing locales and unrelated MkDocs settings intact.

## Gotchas

- **Do not start writing before branching**: `git checkout -b docs-translation-<language>` is required first.
- **Do not stop after a sample**: every file under both English source trees must be translated.
- **Do not lint the docs**: preserve formatting and avoid unrelated Markdown cleanup.
- **Do not translate include paths partially**: every `includes/en/` reference must use the target locale.

For Spanish examples, `includes/es/introduction-event.md` is the concrete rewritten include path.

## Output template

```markdown
## MkDocs translation result

**Status:** complete | blocked
**Language:** `<language>`
**Locale:** `<locale>`
**Branch:** `docs-translation-<language>`

### File counts
| Source tree | Source files | Translated files | Status |
| --- | --- | --- | --- |
| `docs/docs/en` | `<count>` | `<count>` | `matched | missing` |
| `docs/docs/includes/en` | `<count>` | `<count>` | `matched | missing` |

### Configuration
- `mkdocs.yml` locale entry: `<added/updated>`
- `nav_translations`: `<added/updated>`
- `admonition_translations`: `<added/updated>`
```

## Quality gate

- [ ] Target language and locale code were confirmed before translation.
- [ ] `git checkout -b docs-translation-<language>` ran before creating files.
- [ ] Every file under `docs/docs/en` was translated in listed order.
- [ ] Every file under `docs/docs/includes/en` was translated in listed order.
- [ ] Target folders mirror the source structure exactly.
- [ ] Markdown formatting, metadata, links, code blocks, paths, and filenames were preserved.
- [ ] Each translated file ends with `*Translated using GitHub Copilot and GPT-4o.*`.
- [ ] `mkdocs.yml` includes the locale entry, `nav_translations`, and `admonition_translations`.
- [ ] Source and translated file counts match.
