---
name: "comment-code-generate-a-tutorial"
description: "Refactor a source file, add beginner-friendly instructional comments, and generate a README tutorial, deferring the workflow to the comment-code-generate-a-tutorial skill."
argument-hint: "file=<path-to-source>"
agent: "tech-writer"
tools: ["read", "edit", "search"]
---
# /comment-code-generate-a-tutorial

## Objective

Turn a single source file into a teaching artifact: refactor it for clarity, add instructional comments that explain the reasoning, and generate a `README.md` tutorial. The full workflow lives in the [`comment-code-generate-a-tutorial`](../skills/comment-code-generate-a-tutorial/SKILL.md) skill; this prompt applies it to the SIFAP 2.0 stack without restating it.

> [!NOTE]
> The skill's example is Python; in this kit apply it to Java 21 or TypeScript and follow the matching style guide.

## When to Invoke

During Stage 3/4, when preparing a walkthrough for the workshop — for example, explaining a translated module to the rest of the team.

## Preconditions

- The target source file exists and runs (or compiles)
- The audience and the concept to teach are known
- The file contains no unmasked sensitive data

## Inputs the Team Must Provide

- `file` — the path to the source file to document
- The intended audience and the teaching goal
- Ask the user for anything that is missing.

## What I Will Do

- Follow the refactor → comment → tutorial procedure in the [`comment-code-generate-a-tutorial`](../skills/comment-code-generate-a-tutorial/SKILL.md) skill
- Apply it to the kit's languages — Java 21 (backend) or TypeScript on Next.js 15 (frontend)
- Add instructional comments that explain intent and reasoning, not syntax
- Generate a `README.md` with overview, setup, how-it-works, and example usage

## What I Will NOT Do

- Apply Python/PEP 8 conventions unless the file really is Python
- Add superficial comments that restate the code
- Put sensitive data (CPF, benefit amounts) in examples or sample output
- Write the tutorial in any language other than English

## Output Format

```markdown
### Refactored
`backend/.../PaymentRules.java` — clearer names and instructional comments added

### Tutorial (README.md)
- Project Overview
- Setup Instructions
- How It Works
- Example Usage
- Sample Output (optional)
```

## Definition of Done

- [ ] The code is refactored for clarity and follows the language's style guide
- [ ] Instructional comments explain reasoning, without noise
- [ ] `README.md` covers overview, setup, how-it-works, and example usage
- [ ] No sensitive data appears; all prose is in English

## Prompt Body

The [`comment-code-generate-a-tutorial`](../skills/comment-code-generate-a-tutorial/SKILL.md) skill owns the refactor-comment-tutorial procedure — read it, then apply it to the file.

**Step 1 — Read and refactor.**
Understand the file, then improve names and structure per its language's best practices (Java 21 or TypeScript).

**Step 2 — Apply the skill.**
Add beginner-friendly instructional comments and generate the `README.md` sections the skill prescribes.

**Step 3 — Respect the kit rules.**
Use the correct style guide for the language, write in English, and mask any sensitive data.

**Step 4 — Review.**
Confirm the comments teach intent and the tutorial stands on its own.

## Invocation Example

```
/comment-code-generate-a-tutorial file=backend/src/main/java/com/sifap/payment/PaymentRules.java
```
