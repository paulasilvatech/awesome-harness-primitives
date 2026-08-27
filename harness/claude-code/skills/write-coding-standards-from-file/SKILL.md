---
name: write-coding-standards-from-file
description: >-
  Write a coding standards document by analyzing existing file or folder style. Use when asked to
  infer project rules, generate CONTRIBUTING.md or CODING_STANDARDS.md, add standards to
  README.md, find or fix style inconsistencies, choose a minimal or verbose template, or fetch
  language style references.
argument-hint: "fileName=<path> [folderName=<path>] [instructions=<text>] [configVariable=value]"
---

<!-- Generated from harness/github-copilot/skills/write-coding-standards-from-file/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Write coding standards from file

Analyze one file or a folder of files, infer the majority syntax and style conventions, optionally compare them with language style references, and output or write a project coding standards document.

## When to invoke

- "Create coding standards from this file."
- "Infer our style guide from this folder."
- "Write CODING_STANDARDS.md based on these examples."
- "Add project coding standards to README.md."
- "Find and fix inconsistencies while generating the guide."

## Inputs

Use `$ARGUMENTS` to resolve the required `fileName`, optional `folderName`, optional `instructions`, and any configuration override passed as `[configVariableAsParameter]`. If multiple files or `folderName` are supplied, aggregate their style observations into one temporary dataset before writing standards.

| Parameter | Required | Meaning |
| --- | --- | --- |
| `fileName` | Yes | File analyzed for indentation, variable naming, commenting, conditional procedures, functional procedures, and syntax style. |
| `folderName` | No | Folder whose files are aggregated and analyzed as one dataset. |
| `instructions` | No | Extra rules, procedures, or unique-case guidance. |
| `[configVariableAsParameter]` | No | Override a default such as `useTemplate`, `addToREADME`, `createNewFile`, or `newFileName`. |

## Configuration variables

| Variable | Default | Rule |
| --- | --- | --- |
| `addStandardsTest` | `false` | When true, write a test file that checks whether the analyzed files adhere to the generated standards. |
| `addToREADME` | `false` | When true, insert standards into `README.md` and set `createNewFile=false`, `outputSpecToPrompt=false`. |
| `addToREADMEInsertions` | `["atBegin", "middle", "beforeEnd", "bestFitUsingContext"]` | Default to `beforeEnd`; controls where standards are inserted in `README.md`. |
| `createNewFile` | `true` | Create a standards file and set `outputSpecToPrompt=false`, `addToREADME=false`. |
| `fetchStyleURL` | `true` | Fetch the relevant language style URL from the reference list when a language can be identified. |
| `findInconsistencies` | `true` | Count indentation, line-break, comment, conditional/function nesting, and quote-wrapper patterns; record minority deviations. |
| `fixInconsistencies` | `true` | Edit low-count categories to match the majority when safe; set to `false` when more than one file or `folderName` is used. |
| `newFileName` | candidate list | Use the first missing name from `CONTRIBUTING.md`, `STYLE.md`, `CODE_OF_CONDUCT.md`, `CODING_STANDARDS.md`, `DEVELOPING.md`, `CONTRIBUTION_GUIDE.md`, `GUIDELINES.md`, `PROJECT_STANDARDS.md`, `BEST_PRACTICES.md`, `HACKING.md`. |
| `outputSpecToPrompt` | `false` | Return standards in the response and set `createNewFile=false`, `addToREADME=false`. |
| `useTemplate` | `"verbose"` or `"v"` | Accept `[ ["v", "verbose"], ["m", "minimal"], ["b", "best fit"], ["custom"] ]`; `custom` uses the supplied instructions or template. |

## Decision rules

| Condition | Action |
| --- | --- |
| `${fileName}.length > 1 || ${folderName} != undefined` | Toggle `fixInconsistencies` to `false`. |
| `${addToREADME} == true` | Insert into `README.md`; disable `createNewFile` and `outputSpecToPrompt`. |
| `${addToREADMEInsertions} == "atBegin"` | Insert after the title in `README.md`. |
| `${addToREADMEInsertions} == "middle"` | Insert near the middle and adapt the standards heading to the README composition. |
| `${addToREADMEInsertions} == "beforeEnd"` | Insert at the end after a new line. |
| `${addToREADMEInsertions} == "bestFitUsingContext"` | Insert at the best fitting line based on README context and flow. |
| `${addStandardsTest} == true` | Write a standards adherence test after the standards file is complete. |
| `${createNewFile} == true` | Create a file from `newFileName`; disable README insertion and prompt-only output. |
| `${fetchStyleURL} == true` | For the detected language, fetch the relevant URL from `### Fetch Links` style references. |
| `${findInconsistencies} == true` | Categorize syntax patterns, count majority/minority forms, and store inconsistencies. |
| `${fixInconsistencies} == true` | Fix minority syntax categories using stored inconsistency evidence. |
| `typeof ${newFileName} == "string"` | Create exactly that file. |
| `typeof ${newFileName} != "string"` | Iterate the candidate list and use the first file that does not exist, then `break`. |
| `${outputSpecToPrompt} == true` | Return the standards instead of writing a file or README update. |
| `${useTemplate} == "v" || ${useTemplate} == "verbose"` | Use the verbose template. |
| `${useTemplate} == "m" || ${useTemplate} == "minimal"` | Use the minimal template. |
| `${useTemplate} == "b" || ${useTemplate} == "best"` | Pick the minimal or verbose template based on observed project complexity. |
| `${useTemplate} == "custom" || ${useTemplate} == "<ANY_NAME>"` | Use the custom prompt, instructions, template, or data supplied by the user. |


## Compatibility tokens

Keep these original configuration labels recognizable when translating older requests: `boolean`, `string[]`, `string`, `object`, `quasi-configuration`, `as-is`, `and/or`, ` or `, `top-level`, `well-known`, `line-breaks`, `${fileName}`, `${folderName}`, `${instructions}`, `${addToREADME}`, `${createNewFile}`, `${fixInconsistencies}`, `${newFileName}`, `${outputSpecToPrompt}`, `${useTemplate}`, `${fileName} == [<Language> Style Guide]`, `#fetch ${item}`, and `#fetch (URL)`. The template selectors may appear as `[ ["v", "verbose"], ["m", "minimal"], ["b", "best fit"] ]`, `[["v", "verbose"], ["m", "minimal"], ["b", "best fit"]]`, `"m", "minimal"`, `"v", verbose"`, `### "m", "minimal"`, `### "v", "verbose"`, `## Coding Standards Templates`, and `## Variable and Parameter Configuration Conditions` in source material.

When demonstrating spacing or braces, include examples such as `if (x)`, not `if(x)`, and sample calls like `do_something` and `do_something_else` only as illustrative placeholders.

## Standards content

| Section | Infer from source |
| --- | --- |
| Introduction | Purpose, scope, language, package, and project context. |
| Naming conventions | Variables such as `camelCase` or `lower_snake_case`, functions/methods, classes/structs, constants like `UPPER_SNAKE_CASE`, and file naming. |
| Formatting and style | Indentation, line length, braces such as K&R or Allman, blank lines, UTF-8/no BOM, final newline. |
| Comments and documentation | Docstrings, inline comments, file headers, `TODO`, `FIXME`, and `NOTE` practices. |
| Error handling | Exception types, returned errors, logging expectations, cleanup requirements. |
| Best practices and anti-patterns | Global variables, magic numbers, repetition, unused code, and language-specific rules. |
| Examples | One correct and one corrected bad example when useful. |
| Contribution and enforcement | Code review expectations, tests, and guide maintenance. |

## Style reference map

When `fetchStyleURL` is true, use only the relevant language or ecosystem links:

| Language or ecosystem | URL |
| --- | --- |
| C Style Guide | `https://users.ece.cmu.edu/~eno/coding/CCodingStandard.html` |
| C# Style Guide | `https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions` |
| C++ Style Guide | `https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines` |
| Go Style Guide | `https://github.com/golang-standards/project-layout` |
| Java Style Guide | `https://coderanch.com/wiki/718799/Style` |
| AngularJS App Style Guide | `https://github.com/mgechev/angularjs-style-guide` |
| jQuery Style Guide | `https://contribute.jquery.org/style-guide/js/` |
| JavaScript Style Guide | `https://www.w3schools.com/js/js_conventions.asp` |
| JSON Style Guide | `https://google.github.io/styleguide/jsoncstyleguide.xml` |
| Kotlin Style Guide | `https://kotlinlang.org/docs/coding-conventions.html` |
| Markdown Style Guide | `https://cirosantilli.com/markdown-style-guide/` |
| Perl Style Guide | `https://perldoc.perl.org/perlstyle` |
| PHP Style Guide | `https://phptherightway.com/` |
| Python Style Guide | `https://peps.python.org/pep-0008/` |
| Ruby Style Guide | `https://rubystyle.guide/` |
| Rust Style Guide | `https://github.com/rust-lang/rust/tree/HEAD/src/doc/style-guide/src` |
| Swift Style Guide | `https://www.swift.org/documentation/api-design-guidelines/` |
| TypeScript Style Guide | `https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html` |
| Visual Basic Style Guide | `https://en.wikibooks.org/wiki/Visual_Basic/Coding_Standards` |
| Shell Script Style Guide | `https://google.github.io/styleguide/shellguide.html` |
| Git Usage Style Guide | `https://github.com/agis/git-style-guide` |
| PowerShell Style Guide | `https://github.com/PoshCode/PowerShellPracticeAndStyle` |
| CSS | `https://cssguidelin.es/` |
| Sass Style Guide | `https://sass-guidelin.es/` |
| HTML Style Guide | `https://github.com/marcobiedermann/html-style-guide` |
| Linux kernel Style Guide | `https://www.kernel.org/doc/html/latest/process/coding-style.html` |
| Node.js Style Guide | `https://github.com/felixge/node-style-guide` |
| SQL Style Guide | `https://www.sqlstyle.guide/` |
| Angular Style Guide | `https://angular.dev/style-guide` |
| Vue Style Guide | `https://vuejs.org/style-guide/rules-strongly-recommended.html` |
| Django Style Guide | `https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/` |
| SystemVerilog Style Guide | `https://github.com/lowRISC/style-guides/blob/master/VerilogCodingStyle.md` |

## Examples

### Minimal template

Use for small projects or when `useTemplate` is `"m"` or `"minimal"`.

```markdown
## 1. Introduction
* **Purpose:** Briefly explain why the coding standards are being established.
* **Scope:** Define which languages, projects, or modules this specification applies to.

## 2. Naming Conventions
* **Variables:** `camelCase`
* **Functions/Methods:** `PascalCase` or `camelCase`.
* **Classes/Structs:** `PascalCase`.
* **Constants:** `UPPER_SNAKE_CASE`.

## 3. Formatting and Style
* **Indentation:** Use 4 spaces per indent or tabs.
* **Line Length:** Limit lines to a maximum of 80 or 120 characters.
* **Braces:** Use K&R or Allman style.
* **Blank Lines:** Specify separation between logical blocks.

## 4. Commenting
* **Docstrings/Function Comments:** Describe purpose, parameters, and return values.
* **Inline Comments:** Explain complex or non-obvious logic.
* **File Headers:** Specify author, date, and file description if the project uses them.

## 5. Error Handling
* **General:** How to handle and log errors.
* **Specifics:** Which exception types to use and what to include in error messages.

## 6. Best Practices and Anti-Patterns
* **General:** Avoid global variables and magic numbers.
* **Language-specific:** Add project-specific recommendations.

## 7. Examples
* Provide correct and incorrect examples.

## 8. Contribution and Enforcement
* Explain review and enforcement.
```

### Verbose template

Use for larger projects, or when `useTemplate` is `"v"` or `"verbose"`.

```markdown
# Style Guide

This document defines the style and conventions used in this project.
All contributions should follow these rules unless otherwise noted.

## 1. General Code Style
- Favor clarity over brevity.
- Keep functions and methods small and focused.
- Avoid repeating logic; prefer shared helpers/utilities.
- Remove unused variables, imports, code paths, and files.

## 2. Naming Conventions
| Item | Convention | Example |
| --- | --- | --- |
| Variables | `lower_snake_case` | `buffer_size` |
| Functions | `lower_snake_case()` | `read_file()` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Types/Structs | `PascalCase` | `FileHeader` |
| File Names | `lower_snake_case` | `file_reader.c` |

## 3. Formatting Rules
- Indentation: **4 spaces**
- Line length: **max 100 characters**
- Encoding: **UTF-8**, no BOM
- End files with a newline

## 4. Comments & Documentation
- Explain why, not what, unless intent is unclear.
- Keep comments up-to-date as code changes.
- Public functions should include a short description of purpose and parameters.
- Tags: `TODO: follow-up work`, `FIXME: known incorrect behavior`, `NOTE: non-obvious design decision`.

## 5. Error Handling
- Handle error conditions explicitly.
- Avoid silent failures.
- Clean up resources before returning on failure.

## 6. Commit & Review Practices
- One logical change per commit.
- Write clear commit messages.
- Keep pull requests reasonably small.

## 7. Tests
- Write tests for new functionality.
- Tests should be deterministic.
- Prefer readable test cases over complex test abstraction.

## 8. Changes to This Guide
Style evolves. Propose improvements by updating this document.
```

## Output template

```markdown
## Coding standards result

**Status:** created file | updated README.md | output only | blocked
**Source:** `<fileName or folderName>`
**Template:** minimal | verbose | best fit | custom

### Style evidence
| Category | Majority pattern | Exceptions |
| --- | --- | --- |
| Indentation | <tabs/2/4 spaces> | <files or none> |
| Naming | <observed conventions> | <exceptions or none> |
| Comments | <docstring/comment style> | <exceptions or none> |
| Error handling | <observed approach> | <exceptions or none> |

### Artifact
- `<CONTRIBUTING.md or STYLE.md or CODE_OF_CONDUCT.md or CODING_STANDARDS.md or DEVELOPING.md or CONTRIBUTION_GUIDE.md or GUIDELINES.md or PROJECT_STANDARDS.md or BEST_PRACTICES.md or HACKING.md or README.md>`

### Inconsistencies
- <fixed or reported inconsistency>

### Validation
- `fetchStyleURL`: true | false, <URL or not applicable>
- `findInconsistencies`: true | false
- `fixInconsistencies`: true | false
```

## Quality gate

- [ ] `fileName` is present or `folderName` provides a real file set to analyze.
- [ ] Multiple files are aggregated before standards are written.
- [ ] `fixInconsistencies` is disabled for multi-file or folder analysis unless the user explicitly accepts edits.
- [ ] The output location honors `addToREADME`, `createNewFile`, and `outputSpecToPrompt` precedence.
- [ ] `newFileName` uses the first missing candidate or the exact string supplied by the user.
- [ ] Style rules are backed by observed source evidence, fetched reference guidance, or explicit user `instructions`.
- [ ] Every inconsistency that is fixed or reported is tied to a counted minority pattern.

## References

- [C Style Guide](https://users.ece.cmu.edu/~eno/coding/CCodingStandard.html)
- [C# Style Guide](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [C++ Style Guide](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [Go Style Guide](https://github.com/golang-standards/project-layout)
- [Java Style Guide](https://coderanch.com/wiki/718799/Style)
- [AngularJS App Style Guide](https://github.com/mgechev/angularjs-style-guide)
- [jQuery Style Guide](https://contribute.jquery.org/style-guide/js/)
- [JavaScript Style Guide](https://www.w3schools.com/js/js_conventions.asp)
- [JSON Style Guide](https://google.github.io/styleguide/jsoncstyleguide.xml)
- [Kotlin Style Guide](https://kotlinlang.org/docs/coding-conventions.html)
- [Markdown Style Guide](https://cirosantilli.com/markdown-style-guide/)
- [Perl Style Guide](https://perldoc.perl.org/perlstyle)
- [PHP Style Guide](https://phptherightway.com/)
- [Python Style Guide](https://peps.python.org/pep-0008/)
- [Ruby Style Guide](https://rubystyle.guide/)
- [Rust Style Guide](https://github.com/rust-lang/rust/tree/HEAD/src/doc/style-guide/src)
- [Swift Style Guide](https://www.swift.org/documentation/api-design-guidelines/)
- [TypeScript Style Guide](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
- [Visual Basic Style Guide](https://en.wikibooks.org/wiki/Visual_Basic/Coding_Standards)
- [Shell Script Style Guide](https://google.github.io/styleguide/shellguide.html)
- [Git Usage Style Guide](https://github.com/agis/git-style-guide)
- [PowerShell Style Guide](https://github.com/PoshCode/PowerShellPracticeAndStyle)
- [CSS](https://cssguidelin.es/)
- [Sass Style Guide](https://sass-guidelin.es/)
- [HTML Style Guide](https://github.com/marcobiedermann/html-style-guide)
- [Linux kernel Style Guide](https://www.kernel.org/doc/html/latest/process/coding-style.html)
- [Node.js Style Guide](https://github.com/felixge/node-style-guide)
- [SQL Style Guide](https://www.sqlstyle.guide/)
- [Angular Style Guide](https://angular.dev/style-guide)
- [Vue Style Guide](https://vuejs.org/style-guide/rules-strongly-recommended.html)
- [Django Style Guide](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
- [SystemVerilog Style Guide](https://github.com/lowRISC/style-guides/blob/master/VerilogCodingStyle.md)
