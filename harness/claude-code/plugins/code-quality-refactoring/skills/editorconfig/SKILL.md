---
name: editorconfig
description: >-
  Generate or update a comprehensive .editorconfig from repository file types and formatting
  preferences, including indentation, line endings, charset, whitespace, final newline, language
  globs, and rule-by-rule explanations. Use when asked to create, standardize, or explain
  EditorConfig.
---

<!-- Generated from harness/github-copilot/plugins/code-quality-refactoring/skills/editorconfig/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# EditorConfig

Analyze project file types and user formatting preferences, then produce a complete `.editorconfig` plus a rule-by-rule explanation that makes editor behavior consistent across contributors.

## When to invoke

- "Create a .editorconfig for this repository."
- "Standardize indentation and line endings with EditorConfig."
- "Update our EditorConfig for JavaScript, Python, and Markdown."
- "Explain every rule in this .editorconfig."

## Inputs

Use the repository tree, existing `.editorconfig` content, and explicit user preferences. Default to spaces with `indent_size = 2` when the user gives no contrary preference because the original directive set requested spaces, not tabs, and 2 spaces.

## Rule selection

| Rule | Default | Why |
| --- | --- | --- |
| `root = true` | At file top | Stops EditorConfig search from walking into parent directories. |
| `[*]` | Always include | Defines universal defaults for all files. |
| `indent_style = space` | Universal unless project proves tabs are required | Aligns with the stated user preference. |
| `indent_size = 2` | Universal unless language conventions require another size | Aligns with the stated user preference. |
| `end_of_line = lf` | Universal | Prevents cross-platform version-control churn. |
| `charset = utf-8` | Universal | Keeps text portable across editors and build tools. |
| `trim_trailing_whitespace = true` | Universal | Avoids noisy diffs. |
| `insert_final_newline = true` | Universal | Preserves POSIX-friendly file endings and safer concatenation. |
| `[*.md]` with `trim_trailing_whitespace = false` | Include when Markdown exists | Markdown uses trailing spaces for hard line breaks. |

## File-type coverage

Add sections only for file types present in the project or explicitly requested.

| Glob | Typical settings | Notes |
| --- | --- | --- |
| `[*.{js,jsx,ts,tsx,json,yml,yaml,css,scss,html,md}]` | `indent_size = 2` | Common web and configuration files. |
| `[*.py]` | `indent_size = 4` when the project follows PEP 8 | Do not override an existing Python style without evidence. |
| `[*.{cs,csx}]` | `indent_size = 4` | Typical C# convention unless repository uses 2 spaces. |
| `[*.{java,kt,kts}]` | `indent_size = 4` | Typical JVM convention. |
| `[Makefile]` | `indent_style = tab` | Make recipes require tabs. |
| `[*.{bat,cmd,ps1,sh}]` | `end_of_line = crlf` only if the repository standard requires it | Prefer `lf` unless scripts or tooling prove otherwise. |
| `[*.md]` | `trim_trailing_whitespace = false` | Preserve intentional hard breaks. |

## Directive vocabulary

Older EditorConfig prompts used headings such as DIRECTIVES, USER PREFERENCES, and EXECUTION. Preserve their intent: project analysis and explicit preferences MUST be honored, generated configuration WILL go beyond basics with universal defaults, and explanations should be well-structured, best-practice-oriented, and easy-to-understand.

## Procedure

1. Inspect the project structure and identify relevant file extensions, generated folders, and existing style files.
2. Preserve explicit user preferences even when they conflict with a common best practice; call out the conflict in the explanation.
3. Build a top-level universal section first, then add narrower glob sections that override only necessary rules.
4. Avoid adding rules for languages absent from the repository unless the user explicitly asks for them.
5. Return the `.editorconfig` code block first, followed by the rule-by-rule explanation.

## Gotchas

- **Glob syntax matters**: use `*` for one path segment and brace groups such as `[*.{js,ts}]` for related extensions.
- **Markdown whitespace is special**: do not globally trim meaningful Markdown hard breaks without a `[*.md]` override.
- **Makefiles need tabs**: `indent_style = space` can break recipe lines unless `[Makefile]` overrides it.
- **User preference wins**: if a user asks for tabs or 4 spaces, apply it and explain the trade-off.

## Output template

````markdown
Here is the `.editorconfig` file tailored to your project:

```editorconfig
# .editorconfig

# Top-most EditorConfig file
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false
```

### Rule-by-Rule Explanation

- `root = true`: <what it does and why it is included>
- `[*]`: <scope of universal rules>
- `indent_style = space`: <preference or project evidence>
- `indent_size = 2`: <preference or project evidence>
- `end_of_line = lf`: <cross-platform reason>
- `charset = utf-8`: <encoding reason>
- `trim_trailing_whitespace = true`: <diff cleanliness reason>
- `insert_final_newline = true`: <POSIX/tooling reason>
- `[*.md]`: <Markdown-specific scope>
- `trim_trailing_whitespace = false`: <hard line-break reason>
````

## Quality gate

- [ ] The repository file types were considered before choosing glob sections.
- [ ] Explicit user preferences, including spaces and `indent_size = 2` when requested, are honored.
- [ ] The output contains one complete `.editorconfig` code block before the explanation.
- [ ] Every emitted rule has a rule-by-rule explanation.
- [ ] Markdown, Makefile, and language-specific overrides are included only when relevant.
- [ ] The configuration avoids contradictory rules at the same specificity.
