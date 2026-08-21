---
applyTo: '**'
description: 'Prevents prompt instructions, rationale, meta-commentary, scaffold labels, and local personal data from leaking into generated documentation, comments, or code.'
---

# Exclude Prompt Data Conventions — Output Hygiene

These instructions apply to every file produced or modified from a prompt. They are authoritative for separating requested output from prompt framing, rationale, acknowledgments, scaffold labels, and local personal or organization data; explicit user requests for verbatim insertion, prompt/instruction artifacts, and changelog conventions are the only exceptions, and stricter repository privacy or documentation rules win on conflict.

## Core Rule

Never echo prompt content into the file being changed. Write only the outcome. Strip meta-commentary, rationale, framing, and acknowledgments that originated in the prompt so the output reads as if it always belonged in the file.

## Prompt Data Boundaries

Prompt data is content the user provides as instruction or context rather than intended file content.

| Prompt data type | Exclude from generated files |
| --- | --- |
| Change descriptions | Phrases such as `add a --verbose flag that...` when they are instructions rather than documentation text. |
| Rationale or motivation | Text such as `because the old behavior caused...` unless it documents the product behavior itself. |
| Prompt references | `as requested`, `per the prompt`, `the new feature has been added as`, and similar acknowledgments. |
| Meta-commentary | Sentences such as `This section has been updated to reflect...`. |
| Change-narrating comments | Comments such as `// Added email validation as requested` or `// Now validates the input per the new requirement`. |
| Scaffold labels | Template slot words such as `this` in `## this Title` when the word is a marker, not heading text. |

## Output Content

The output file may contain only the resulting feature, fix, or content, written in polished production-ready form.

- Write documentation or code that is useful without knowing how the change was requested.
- Use generic placeholder data such as `Jane Doe`, `jane.doe@example.com`, `Acme Corp`, and `example.com` instead of real names, emails, domains, or organization identifiers pulled from the prompt or local configuration.
- Preserve language formatting when it is part of the intended result, such as backticks around a flag or a specific syntax convention.
- Improve grammar, capitalization, punctuation, and clarity instead of copying informal or sloppy prompt phrasing.
- Keep code comments about what the code does, its constraints, or its intent; do not narrate why the edit was made.

## Exceptions

| Exception | Boundary |
| --- | --- |
| Verbatim transcription requested | When the user explicitly asks to paste prompt text as-is, insert exactly what was requested and nothing more. |
| Prompt, skill, or instruction artifacts | Instructional content is the intended payload, but do not add meta-commentary about the current edit. |
| Changelog or release notes | A short factual line such as `Added --verbose flag` is acceptable; `Added --verbose flag as requested by user` is not. |

## Examples

The examples below illustrate documenting a requested flag without leaking prompt framing.

**Good:**

```text
### --new-opt

Enables extended output. Requires a value argument. Example:

    file --new-opt foo
```

Why: The documentation states the resulting behavior directly.

**Bad:**

```text
### --new-opt

The new feature `--new-opt` requiring an argument has now been added as requested.
The feature is documented as such.
```

Why: The text reports back to the requester instead of documenting the feature.

**Good:**

```js
function createUser(name, email) {
  // Rejects addresses missing a local part, @ sign, or domain.
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    throw new Error('Invalid email address.');
  }
}
```

Why: The comment describes the validation behavior.

**Bad:**

```js
// Added email validation as requested in the prompt
function createUser(name, email) {
  // Per the instruction, we now validate that email must be a valid format
}
```

Why: The comments leak the prompt and narrate the change.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Output contains `as requested` or `per the prompt` | Remove the phrase and document the subject directly. |
| Docs announce a change instead of documenting it | Rewrite as stable product or project documentation. |
| Code comments narrate the change | Describe the code's behavior, constraint, or intent. |
| Prompt scaffold labels appear in output headings | Replace the scaffold word with the intended heading text. |
| Verbatim request text appears in the file | Keep it only when the user explicitly requested transcription. |

## Prompt-Leak Vocabulary

Reject prompt-leak strings including `"// Added email validation as requested"`, `"// Now validates the input per the new requirement"`, `"The feature is documented as such"`, `"This section has been updated to reflect..."`, `"add a --verbose flag that..."`, `"as requested"`, `"because the old behavior caused..."`, `"has now been added as requested"`, `"per the prompt"`, and `"the new feature has been added as"`. Treat `## Notice`, `README`, `features.md`, `release-note`, `draft-quality`, and `self-contained` as content-shaping terms that must not be copied from a prompt unless they are intended output.


## Conventions

| Rule | Rationale |
| --- | --- |
| Write the result, not the story of how it was requested | Files remain natural and useful to readers without prompt context |
| Remove prompt references such as `as requested`, `per the prompt`, and `per your instruction` | Prompt acknowledgments expose process instead of product behavior |
| Keep examples generic with `Jane Doe`, `jane.doe@example.com`, `Acme Corp`, and `example.com` | Local personal or organization data does not leak into reusable content |
| Preserve intended syntax formatting from the prompt | Flags, identifiers, and code terms remain accurate |
| Rewrite low-quality prompt wording into polished output | The prompt's writing quality does not set the standard for generated files |
| Treat prompt/instruction artifacts as payload only when editing those artifacts | Instructional files can contain instructions without narrating the edit |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Document `--new-opt` as a supported option | Say the option was added `as requested` |
| Write comments that explain validation behavior | Write comments that say validation was added due to a prompt |
| Use generic placeholder identities in examples | Copy real names, emails, domains, or organization identifiers from prompt context |
| Insert verbatim text only when explicitly requested | Treat every prompt sentence as intended file content |
| Scan the diff for prompt leakage before saving | Leave scaffold markers or acknowledgments in headings, comments, or docs |

## Checklist Before Opening a PR

- [ ] No generated file contains `as requested`, `per the prompt`, `per your instruction`, or similar prompt acknowledgments.
- [ ] Documentation states current behavior instead of announcing that a change was made.
- [ ] Code comments describe behavior, constraints, or intent, not the edit request.
- [ ] Prompt scaffold labels were replaced with natural headings or content.
- [ ] Examples use generic placeholder data and do not copy local personal, domain, or organization details.
- [ ] Any verbatim prompt text in a file is justified by an explicit transcription request or by the file being a prompt, skill, or instruction artifact.
