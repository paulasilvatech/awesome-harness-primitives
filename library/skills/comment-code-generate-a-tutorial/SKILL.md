---
name: "comment-code-generate-a-tutorial"
description: >-
  Transform a Python script into a polished beginner-friendly project by refactoring code, adding instructional comments, and generating a complete README.md tutorial. Use this skill when asked to explain, comment, clean up, teach, or turn a Python script into a tutorial project.
---

# Comment code generate a tutorial

Refactor a Python script for readability, add useful beginner-friendly comments that explain reasoning, and generate a tutorial-style `README.md` that teaches setup, usage, internals, and expected output.

## When to invoke

- "Turn this Python script into a tutorial."
- "Add beginner-friendly comments to this script."
- "Refactor this Python code and write a README."
- "Make this script easier for beginners to understand."
- "Generate a project tutorial from this Python file."

## Python refactoring rules

| Area | Apply | Avoid |
| --- | --- | --- |
| Style | Apply standard Python best practices and PEP 8 naming, spacing, imports, and line length conventions. | Reformatting in a way that conflicts with the repository's formatter. |
| Names | Rename unclear variables and functions when it improves clarity. | Renaming public APIs, CLI flags, files, or serialized fields without preserving compatibility. |
| Structure | Extract small functions for distinct steps such as loading input, processing data, and presenting output. | Over-engineering a short teaching script with unnecessary classes. |
| Safety | Keep behavior equivalent unless the user asks for functional changes. | Silently changing algorithms, file paths, network behavior, or output formats. |
| Entry point | Prefer a `main()` function and `if __name__ == "__main__": main()` for runnable scripts. | Running side effects at import time. |

## Instructional comment rules

- Use a beginner-friendly, instructional tone.
- Explain what each important part of the code is doing and why it matters.
- Focus on logic, reasoning, data flow, and decisions, not just syntax.
- Avoid redundant or superficial comments such as `# increment i` above `i += 1`.
- Comment non-obvious trade-offs, assumptions, input formats, error handling, and external calls.
- Prefer clear names over comments when a rename can make the explanation unnecessary.

## README tutorial requirements

Generate or update `README.md` with these sections:

| Section | Required content |
| --- | --- |
| `Project Overview` | What the script does and why it is useful. |
| `Setup Instructions` | Prerequisites, dependencies, environment setup, and how to run the script. |
| `How It Works` | A breakdown of the code logic based on the instructional comments. |
| `Example Usage` | A command or code snippet showing how to use it. |
| `Sample Output` | Include when the script returns visible results or a representative output can be shown confidently. |

Use clear, readable Markdown formatting. Keep commands copy-pasteable and avoid inventing dependencies that are not present in the script or project files.

## Gotchas

- **Do not comment every line**: beginners learn more from comments around intent and flow than from syntax narration.
- **Do not change behavior while teaching**: preserve inputs, outputs, and side effects unless the user asks for improvements.
- **Do not fabricate sample output**: if output depends on unavailable data or services, show the command and explain what kind of output to expect.
- **Do not hide prerequisites**: if the script imports third-party packages, mention installation steps or the existing dependency file.

## Output template

```markdown
## Python tutorial project result

**Status:** complete | partial | blocked
**Script:** `<path/to/script.py>`
**Tutorial:** `README.md`

| Area | Changes made | Notes |
| --- | --- | --- |
| Refactor | `<functions/names/structure>` | `<behavior preserved or changed>` |
| Comments | `<instructional comments added>` | `<focus areas>` |
| README | `<sections generated>` | `<sample output included or omitted>` |

### Validation
- Syntax check: `<command and result>`
- Run command: `<command and result, or not run with reason>`
```

## Quality gate

- [ ] Refactoring follows Python best practices and PEP 8 without unnecessary behavior changes.
- [ ] Unclear variables or functions are renamed only when compatibility is preserved or the user requested it.
- [ ] Comments explain logic and reasoning, not obvious syntax.
- [ ] `README.md` includes Project Overview, Setup Instructions, How It Works, Example Usage, and Sample Output when applicable.
- [ ] Dependency and run instructions are based on the actual script or project files.
- [ ] Validation includes a syntax check or a clear reason it could not be run.
