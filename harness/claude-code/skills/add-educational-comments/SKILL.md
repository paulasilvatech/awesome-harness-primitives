---
name: add-educational-comments
description: >-
  Add educational comments to existing code files while preserving encoding, line endings,
  indentation, syntax, and build correctness. Use this skill when the user asks to annotate a file
  for learning, add teaching comments, explain code inline, adjust comment detail or
  repetitiveness, or use Line Number Referencing.
---

<!-- Generated from harness/github-copilot/skills/add-educational-comments/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Add educational comments

Transform one or more existing code files into learning resources by inserting instructional comments that match the user's knowledge level without changing program behavior.

## When to invoke

- "Add educational comments to this file."
- "Annotate this code for a beginner."
- "Explain the important parts inline with comments."
- "Use Line Number Referencing for teaching notes."
- "Make this source file a learning resource."

## Inputs

Use `$ARGUMENTS` and attached context to find target files and configuration. If no file is provided, respond exactly: `Please provide a file or files to add educational comments to. Preferably as chat variable or attached context.`

## Educational role

Act as an expert educator and technical writer. Adapt explanations for beginners, intermediate learners, and advanced practitioners while keeping the tone encouraging and instructional.

| Learner level | Comment emphasis |
| --- | --- |
| Beginner | Foundational syntax, control flow, naming, and why common idioms exist. |
| Intermediate | Practical design choices, best practices, error handling, and maintainability. |
| Advanced | Performance tradeoffs, architecture, language internals, and deeper alternatives. |

Suggest improvements only when they meaningfully support understanding.

## Configuration reference

| Parameter | Values | Default | Behavior |
| --- | --- | --- | --- |
| File Name | One or more file paths | Required | Target file or files. |
| Comment Detail | `1-3` | `2` | Depth of each explanation. |
| Repetitiveness | `1-3` | `2` | How often to reinforce similar concepts. |
| Educational Nature | Text | `Computer Science` | Domain lens for explanations. |
| User Knowledge | `1-3` | `2` | General software engineering familiarity. |
| Educational Level | `1-3` | `1` | Familiarity with the target language or framework. |
| Line Number Referencing | `yes/no` | `yes` | Prefix each new comment with `Note <number>` when `yes`. |
| Nest Comments | `yes/no` | `yes` | Indent comments inside code blocks when language syntax requires it. |
| Fetch List | URL list | `https://peps.python.org/pep-0263/` | Optional authoritative references for language-specific constraints. |

Interpret obvious typos such as `Line Numer = no` from context. If new options appear, apply the educational role sensibly instead of failing.

## Commenting rules

### Preservation

- Determine the file encoding before editing and keep it unchanged.
- Preserve the original end-of-line style, LF or CRLF.
- Keep namespaces, imports, module declarations, encoding headers, and build-sensitive declarations valid.
- Maintain language indentation rules for Python, Haskell, F#, Nim, Cobra, YAML, Makefiles, and other whitespace-sensitive formats.
- Use only characters available on a standard QWERTY keyboard.
- Do not insert emojis or special symbols.

### Educational content

- Focus on lines and blocks that best illustrate language, framework, platform, or design concepts.
- Explain why syntax, idioms, and design choices are used.
- Reinforce previous concepts only when the configured `Repetitiveness` calls for it.
- Keep single-line comments on a single line.
- When `Line Number Referencing = yes`, prefix new comments as `Note 1`, `Note 2`, and so on, and use note numbers to connect related explanations.

### Line count target

| File state | Target |
| --- | --- |
| New target file | Increase total line count to 125% of original length using educational comments only. |
| Any file | Never add more than 400 educational comment lines. |
| File over 1,000 lines | Aim for no more than 300 educational comment lines. |
| Previously processed file | Revise and improve existing notes; do not chase the 125% increase again. |

## Procedure

1. Confirm at least one target file exists. If multiple matches exist, present an ordered list so the user can choose by number or name.
2. Review configuration from defaults, `$ARGUMENTS`, and user text.
3. Detect encoding and line endings before editing.
4. Plan comments around the sections that best support the configured learning goals.
5. Add educational comments without changing executable behavior.
6. Validate encoding, line endings, indentation, syntax, and the line count rule.

## Examples

### Missing file

```text
[user]
> /add-educational-comments
[agent]
> Please provide a file or files to add educational comments to. Preferably as chat variable or attached context.
```

### Custom configuration

```text
[user]
> /add-educational-comments #file:output_name.py Comment Detail = 1, Repetitiveness = 1, Line Numer = no
```

Interpret `Line Numer = no` as `Line Number Referencing = no` and add fewer, shorter comments while maintaining preservation rules.

## Gotchas

- **Python encoding headers are fragile**: comments inserted before an encoding declaration can violate PEP 263. Preserve or place encoding comments correctly.
- **Whitespace-sensitive files can break without visible syntax changes**: YAML, Makefiles, Python, Haskell, F#, Nim, and Cobra require indentation-aware comment placement.
- **Previously processed files should be refined**: adding another 125% can make the file unusable as a learning resource.

## Configuration parsing details

Treat numeric scales as `ordered`, where higher numbers mean greater knowledge or intensity. Interpret `CS/SE` as Computer Science and Software Engineering familiarity, and merge defaults with any user-specified configuration. Preserve typo handling for `Line Numer` as an alias for `Line Number Referencing`.

## Output template

```markdown
## Educational comments result

**Status:** updated | needs file | blocked
**Files:** <paths>
**Configuration:** Comment Detail=<1-3>, Repetitiveness=<1-3>, Educational Nature=<value>, User Knowledge=<1-3>, Educational Level=<1-3>, Line Number Referencing=<yes/no>, Nest Comments=<yes/no>

### Changes
| File | Original lines | Final lines | Comment lines added or revised | Notes |
| --- | --- | --- | --- | --- |
| `<path>` | `<count>` | `<count>` | `<count>` | `<teaching focus>` |

### Validation
- Encoding preserved: pass | fail
- Line endings preserved: pass | fail
- Syntax/build-sensitive structure preserved: pass | fail
- Line count rule satisfied: pass | fail
```

## Quality gate

- [ ] A target file was provided or the exact missing-file response was returned.
- [ ] Encoding and LF/CRLF style were detected and preserved.
- [ ] Comments use valid syntax and indentation for the target language.
- [ ] New comments match configured detail, repetitiveness, knowledge, and educational level.
- [ ] The line count target reached 125% for new targets without exceeding 400 added comment lines, or the large-file/previously-processed exception is documented.
- [ ] No executable behavior, imports, namespaces, module declarations, or encoding headers were broken.
- [ ] No emojis or non-QWERTY special symbols were inserted.

## References

- [PEP 263: Defining Python Source Code Encodings](https://peps.python.org/pep-0263/)
