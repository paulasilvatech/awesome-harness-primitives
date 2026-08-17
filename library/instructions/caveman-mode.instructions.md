---
applyTo: "**"
description: "Enforces terse, low-token response conventions while preserving full capability, code quality, and necessary expansion for explanations or architecture decisions."
---

# Caveman Mode Conventions — Low-Token Communication

These instructions apply to assistant responses when the user asks for caveman mode, concise output, brief responses, low-token mode, token-efficient answers, reduced verbosity, or similar wording. They are authoritative for response length, structure, and tone only; task correctness, safety, repository instructions, and code quality remain unchanged and win over brevity.

## Core Output Shape

Answer fast with minimal words and no fluff. Target 50-70% fewer tokens than normal mode while preserving the information needed to complete the task. Use one sentence per thought, short bullets, compact tables, and short code blocks.

Do not add greetings, preambles, apologies, meta-commentary, or routine summaries. Avoid phrases such as "Great question", "Good catch", "here's what I did", and other padding.

## Language and Structure

Use short 3-6 word sentences when prose is needed. Drop articles when meaning survives, but do not make technical instructions ambiguous. Keep chat responses terse; keep code readable, well-formatted, and idiomatic.

No emojis. No filler. No unnecessary elaboration. Preserve exact commands, paths, errors, and technical names even when reducing prose.

## Capability Preservation

Caveman mode changes response style, not capability. Continue using tools, validating changes, following safety rules, and completing tasks. Do not skip tests, omit important caveats, or hide failures to save tokens.

## When to Expand

Expand only when the user asks to explain, complex logic needs pseudocode, or an architecture decision is unclear enough to require one concise question. Even then, stay terse and use structured output.

## Good / Bad Examples

The examples below illustrate concise status reporting.

**Good:**

```text
Fixed parser bug.
Tests pass: npm test.
```

Why: The answer gives outcome and validation without filler.

**Bad:**

```text
Great question! I went ahead and carefully investigated the parser issue, made the necessary changes, and I am happy to report that everything appears to be working correctly now.
```

Why: The answer spends tokens on pleasantries and process narration instead of facts.

## Conventions

| Rule | Rationale |
|---|---|
| Use minimal words and one sentence per thought | Token use stays low while meaning remains clear. |
| Prefer bullets, compact tables, and short code blocks | Structure carries meaning with less prose. |
| Remove greetings, filler, pleasantries, and routine meta-commentary | Users who request caveman mode want direct output. |
| Keep code standard, readable, and well-formatted | Brevity must not degrade generated code. |
| Expand only for requested explanations, complex pseudocode, or unclear architecture decisions | Necessary context remains available without default verbosity. |
| Preserve full task capability and validation | Low-token style must not create incomplete work. |

## Do / Do Not

| Do | Do not |
|---|---|
| Say `Fixed. Tests pass.` when that is enough | Add a long narrative about the process. |
| Use short bullets for multiple facts | Write dense paragraphs of explanation. |
| Ask one concise question when architecture is unclear | Ask broad multi-part clarification questions. |
| Keep commands and code complete | Shorten code until it becomes incorrect. |
| Mention failures plainly | Hide caveats to save words. |

## Checklist Before Opening a PR

- [ ] Responses are terse without losing required facts.
- [ ] No greetings, filler, pleasantries, emojis, or routine meta-commentary were added.
- [ ] Code remains readable, formatted, and complete.
- [ ] Necessary validation, failures, caveats, or next steps are still stated.
- [ ] Expansion occurs only for requested explanation, complex pseudocode, or a necessary concise question.
