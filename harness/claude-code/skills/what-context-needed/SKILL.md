---
name: what-context-needed
description: >-
  Identify the minimum files, symbols, configuration, tests, and prior context GitHub Copilot
  needs before answering a codebase question. Use this skill when the user asks what context is
  needed, what files to provide, or wants a context checklist before asking an implementation,
  debugging, review, or architecture question.
---

<!-- Generated from harness/github-copilot/skills/what-context-needed/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# What context do you need

Before answering a codebase question, produce a concise evidence request that separates must-see files from helpful files, already-seen context, and remaining uncertainty so the next answer can be grounded.

## When to invoke

- "What context do you need before answering?"
- "Which files should I send you?"
- "Tell me what you need to inspect first."
- "What code would help you debug this?"
- "What files are required for an accurate review?"

## Context selection criteria

| Question type | Must see | Should see |
| --- | --- | --- |
| Bug or exception | Failing file, stack trace location, caller, tests covering the behavior, and relevant config. | Logs with secrets removed, recent diff, related error handling utilities. |
| Feature implementation | Target module, adjacent similar feature, public interface, tests, and config or route registration. | Product spec, API docs, database schema, fixtures, UI snapshots. |
| Refactor | Current implementation, call sites, tests, type definitions, and build/lint constraints. | Architecture docs, deprecated alternatives, performance notes. |
| Code review | Diff or changed files, tests changed or omitted, risky dependencies, and validation output. | Related modules and issue/PR context. |
| Architecture question | Entry points, module boundaries, dependency wiring, configuration, and data flow. | Diagrams, ADRs, deployment files, observability setup. |

## File request rules

- Ask for paths, not pasted blobs, when repository access is available.
- Prefer the smallest set that can disprove a wrong answer.
- Include tests whenever behavior, regressions, or refactors are involved.
- Include configuration when behavior depends on routing, dependency injection, build tools, environment variables, feature flags, or package versions.
- Mark generated, vendored, build output, and dependency directories as unnecessary unless the question is specifically about them.
- Note files already seen in the conversation so the user does not resend them.
- State uncertainty explicitly instead of answering from assumptions.

## Output template

```markdown
## Files I Need

### Must See (required for accurate answer)
- `path/to/file.ts` — <why this file is required>

### Should See (helpful for complete answer)
- `path/to/file.ts` — <why this file would improve confidence>

### Already Have
- `path/to/file.ts` — <from earlier in conversation or current context>

### Uncertainties
- <what remains unknown without the requested code>

After you provide these files, ask the question again with any error text or validation output.
```

## Quality gate

- [ ] The response does not answer the underlying technical question prematurely.
- [ ] Must-see files are limited to evidence required for an accurate answer.
- [ ] Should-see files are useful but not blockers.
- [ ] Already-seen files are listed when known.
- [ ] Each requested file has a concrete reason.
- [ ] Uncertainties describe what cannot be known yet.
- [ ] The output follows the `## Files I Need` structure exactly.
