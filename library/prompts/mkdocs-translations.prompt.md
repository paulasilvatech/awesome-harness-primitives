---
name: 'mkdocs-translations'
description: 'Generate a complete locale-specific translation workflow for an MkDocs documentation stack.'
agent: 'agent'
model: 'Claude Sonnet 4'
tools: ['codebase', 'usages', 'problems', 'changes', 'terminalSelection', 'terminalLastCommand', 'searchResults', 'extensions', 'editFiles', 'search', 'runCommands', 'runTasks']
argument-hint: 'locale=<ISO 639-1-or-locale-code>'
---

# /mkdocs-translations

## Objective

Translate every documentation file under `docs/docs/en` and `docs/docs/includes/en` into a user-specified target language and locale for an MkDocs stack, preserving directory structure, filenames, Markdown formatting, include paths, and MkDocs i18n configuration.

## When to Invoke

Use this prompt when a documentation site built with MkDocs needs a complete new locale, including translated content folders, include folders, locale-specific include references, and `mkdocs.yml` i18n plugin updates.

## Preconditions

- The user has provided a target translation language and locale code such as Spanish `es`, French `fr`, Brazilian Portuguese `pt-BR`, or Korean `ko`.
- Source folders `docs/docs/en` and `docs/docs/includes/en` exist.
- `mkdocs.yml` exists and can be modified.
- File creation and edits are approved.
- A git branch can be created before any new files are created.

## Inputs the Team Must Provide

- Target translation language.
- Target locale code using ISO 639-1 or a locale code, such as `es`, `fr`, `pt-BR`, or `ko`.
- Ask the user for the target language and locale code before proceeding. If either value remains missing, stop before creating a branch or files.

## What I Will Do

- Create a branch with `git checkout -b docs-translation-<language>` before creating any new files.
- List all files and subdirectories under `docs/docs/en` and `docs/docs/includes/en`.
- Translate every source file one by one in the listed order without skipping, reordering, or stopping after a fixed number of files.
- Mirror the exact folder and file structure under `docs/docs/<locale>` and `docs/docs/includes/<locale>`.
- Preserve headings, code blocks, metadata, links, filenames, Markdown formatting, and original structure.
- Update include references from paths such as `includes/en/introduction-event.md` to `includes/<locale>/introduction-event.md`.
- Update `mkdocs.yml` with a new `locale` entry under the `i18n` plugin, including `nav_translations` and `admonition_translations`.

## What I Will NOT Do

- Proceed without the target translation language and locale code.
- Prompt for confirmation, approval, or next steps after translation starts.
- Skip files, reorder files, stop after an arbitrary batch size, or leave unprocessed source files.
- Fix or comment on Markdown linting or formatting issues such as missing blank lines around headings or lists, trailing punctuation in headings, missing alt text for images, improper heading levels, line length, or spacing.
- Say things like `There are some linting issues, such as…` or `Would you like me to fix…`.
- Wrap translated content or translated files in Markdown code blocks.

## Output Format

Report progress and final completion using this structure:

```markdown
## MkDocs Translation Result

### Locale
- Language: Brazilian Portuguese
- Locale code: `pt-BR`
- Branch: `docs-translation-pt-BR`

### Source Inventory
| Source root | Files listed | Files translated |
| --- | ---: | ---: |
| `docs/docs/en` | 0 | 0 |
| `docs/docs/includes/en` | 0 | 0 |

### Created Folders
- `docs/docs/pt-BR`
- `docs/docs/includes/pt-BR`

### Configuration Updated
- `mkdocs.yml` i18n `locale` entry added for `pt-BR`
- `nav_translations` added
- `admonition_translations` added

### Verification
- Source file count matches translated file count: [yes/no]
- Include paths updated from `includes/en/` to `includes/pt-BR/`: [yes/no]
- Every translated file ends with: `*Translated using GitHub Copilot and GPT-4o.*`
```

Each translated file must keep its original filename and append this exact line at the end:

```markdown
*Translated using GitHub Copilot and GPT-4o.*
```

## Definition of Done

- [ ] The user provided the target language and locale code.
- [ ] The branch `docs-translation-<language>` was created before any new file creation.
- [ ] All files and subdirectories under `docs/docs/en` were listed and translated.
- [ ] All files and subdirectories under `docs/docs/includes/en` were listed and translated.
- [ ] The translated file count matches the source file count.
- [ ] The exact folder and filename structure is mirrored under `docs/docs/<locale>` and `docs/docs/includes/<locale>`.
- [ ] Markdown formatting, headings, code blocks, metadata, and links are preserved.
- [ ] Include references are updated from `includes/en/...` to `includes/<locale>/...`.
- [ ] `mkdocs.yml` includes the new `i18n` `locale`, `nav_translations`, and `admonition_translations`.
- [ ] No Markdown linting commentary or unsolicited formatting fixes were introduced.

## Prompt Body

Follow these steps in order.

**Step 1 — Obtain the required locale.** Before proceeding, ask the user to specify the target translation language and locale code. Examples: Spanish (`es`), French (`fr`), Brazilian Portuguese (`pt-BR`), and Korean (`ko`). Use this value consistently in folder names, translated content paths, include path updates, and MkDocs configuration. Stop if the user does not provide it.

**Step 2 — Create the translation branch.** Before creating any new files, run `git checkout -b docs-translation-<language>`, replacing `<language>` with the provided locale code or agreed branch-safe language token.

**Step 3 — Inventory source files.** Begin by listing all files and subdirectories under `docs/docs/en`. Then list all files and subdirectories under `docs/docs/includes/en`. Keep this task list and check each item off as it is done. The list defines the translation order.

**Step 4 — Create target folders.** Create a new folder under `docs/docs/` named with the ISO 639-1 or locale code provided by the user. Examples: `es` for Spanish, `fr` for French, and `pt-BR` for Brazilian Portuguese. Create a new folder under `docs/docs/includes/` using the same target language code. Mirror the exact folder and file structure from the original `en` directories.

**Step 5 — Translate every documentation file.** Translate every file in the `docs/docs/en` list one by one in the order shown. Do not skip, reorder, or stop after a fixed number of files. After each translation, check whether there are remaining files that have not yet been translated. If there are, continue automatically with the next file. Do not prompt for confirmation, approval, or next steps. Proceed automatically until all files are translated.

**Step 6 — Translate every include file.** Translate each file under `docs/docs/includes/en` using the same rules. Maintain the same file and folder structure in the translated output. Save each translated include file in the corresponding `docs/docs/includes/<locale>` folder.

**Step 7 — Preserve Markdown exactly.** For each translated file, preserve all Markdown formatting, headings, code blocks, metadata, links, and original filename. Do not wrap translated content in Markdown code blocks. Use accurate, clear, technically appropriate translations and computer industry-standard terminology; for example, prefer `Stack Tecnológica` over `Pila Tecnológica` when translating that term into Portuguese. Append `*Translated using GitHub Copilot and GPT-4o.*` at the end of every translated file.

**Step 8 — Update include paths.** Update include references in translated files to reflect the new locale. For example, change `includes/en/introduction-event.md` to `includes/es/introduction-event.md`, replacing `es` with the actual locale code provided by the user.

**Step 9 — Update MkDocs configuration.** Modify `mkdocs.yml`. Add a new `locale` entry under the `i18n` plugin using the target language code. Provide appropriate translations for `nav_translations` and `admonition_translations`.

**Step 10 — Avoid linting detours.** Do not comment on, suggest changes for, or attempt to fix formatting or Markdown linting issues. This includes missing blank lines around headings or lists, trailing punctuation in headings, missing alt text for images, improper heading levels, line length, and spacing. Never prompt the user about linting or formatting issues.

**Step 11 — Verify completion.** Confirm that the number of translated files matches the number of source files listed. If any files remain unprocessed, resume from where you left off. Report the source counts, translated counts, created folders, configuration updates, and include path updates.

## Invocation Example

```
/mkdocs-translations locale=pt-BR
```
