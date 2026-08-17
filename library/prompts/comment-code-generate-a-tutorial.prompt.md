---
name: 'comment-code-generate-a-tutorial'
description: 'Refactor a Python script into a beginner-friendly project with instructional comments and a tutorial.'
---

# /comment-code-generate-a-tutorial

## Objective

Transform a Python script into a polished, beginner-friendly project by refactoring the code, adding clear instructional comments, and generating a complete Markdown tutorial as `README.md`.

## When to Invoke

Use this prompt when a user provides a Python script and wants it refactored for clarity, commented for beginners, and accompanied by a tutorial that explains setup, usage, logic, and output.

## Preconditions

- The Python script or selected code is available.
- Edits to the script and creation or update of `README.md` are permitted.
- Project dependencies and expected runtime behavior are known or inferable from the script.
- The tutorial audience is beginner-level.

## Inputs the Team Must Provide

- `target` — the Python script or selected code to transform.
- Any required project name, dependencies, setup constraints, and expected sample input or output.
- Whether visible sample output exists or should be omitted.
- Ask the user for anything that is missing, especially when missing information would affect setup instructions.

## What I Will Do

- Refactor the Python code using standard Python best practices and PEP 8 style.
- Rename unclear variables and functions when doing so improves clarity.
- Add beginner-friendly instructional comments that explain what the code does and why it matters.
- Avoid redundant or superficial comments that only restate syntax.
- Generate a `README.md` tutorial with project overview, setup instructions, how it works, example usage, and optional sample output.

## What I Will NOT Do

- Change the script's intended behavior without calling out the change.
- Add comments to every line when the code is already self-explanatory.
- Invent dependencies, outputs, or setup steps that cannot be inferred or verified.
- Replace the user's project with an unrelated framework or architecture.
- Omit PEP 8 and beginner-readability checks from the final review.

## Output Format

Return or apply the refactor and tutorial with this structure:

```markdown
### Commented Code Tutorial Result

### Files Updated
- `<script>.py`
- `README.md`

### Refactor Summary
- Applied standard Python best practices.
- Ensured code follows the PEP 8 style guide.
- Renamed unclear variables and functions where needed for clarity.

### Commenting Summary
- Added beginner-friendly instructional comments.
- Explained what each important part of the code is doing and why it is important.
- Focused on logic and reasoning, not just syntax.
- Avoided redundant or superficial comments.

### README.md Sections
- Project Overview: what the script does and why it is useful
- Setup Instructions: prerequisites, dependencies, and how to run the script
- How It Works: a breakdown of the code logic based on the comments
- Example Usage: a code snippet showing how to use it
- Sample Output: optional, included only if the script returns visible results

### Validation
- Command: `<python command, tests, lint, or not run>`
- Result: `<passed, failed, or not run with reason>`
```

## Definition of Done

- [ ] Python code is refactored for clarity while preserving intended behavior.
- [ ] Code follows PEP 8 style as far as the project allows.
- [ ] Instructional comments help beginners understand logic and reasoning.
- [ ] `README.md` includes all required tutorial sections and omits sample output only when not applicable.
- [ ] Validation evidence or a precise not-run reason is reported.

## Prompt Body

Follow these steps in order. Optimize for beginner understanding without changing behavior.

**Step 1 — Inspect the script.** Identify the script purpose, inputs, outputs, dependencies, side effects, and unclear names. Ask for missing runtime or dependency details when needed for setup instructions.

**Step 2 — Refactor the code.** Apply standard Python best practices. Ensure code follows the PEP 8 style guide. Rename unclear variables and functions if needed for clarity. Keep behavior stable unless a change is requested or necessary for correctness.

**Step 3 — Add instructional comments.** Add comments throughout the code using a beginner-friendly instructional tone. Explain what each important part of the code is doing and why it is important. Focus on the logic and reasoning, not just syntax. Avoid redundant or superficial comments.

**Step 4 — Generate the tutorial.** Create or update `README.md`. Include Project Overview explaining what the script does and why it is useful. Include Setup Instructions with prerequisites, dependencies, and how to run the script. Include How It Works with a breakdown of code logic based on the comments. Include Example Usage with a code snippet. Include Sample Output only if the script returns visible results. Use clear, readable Markdown formatting.

**Step 5 — Validate and report.** Run the smallest existing Python command, test, or lint check that applies when available. Report files updated, refactor summary, commenting summary, README sections, and validation.

## Invocation Example

```
/comment-code-generate-a-tutorial target=scripts/example.py
```
