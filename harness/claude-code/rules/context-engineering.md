<!-- Generated from harness/github-copilot/instructions/context-engineering.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces repository-wide context engineering conventions that make code, structure, naming, and Copilot interactions easier for AI assistance to understand.

# Context Engineering Conventions — AI-Readable Codebases

These instructions apply repository-wide to source code, project structure, documentation, and Copilot collaboration patterns. They are authoritative for context clarity, file organization, naming, public API surfaces, explicit types, and AI-assistance hygiene; language-specific, framework-specific, and security primitives win when they impose stricter conventions for matched files.

## Project Structure and Context Signals

Organize files so paths communicate intent to humans and AI tools.

| Practice | Convention |
| --- | --- |
| Descriptive paths | Prefer `src/auth/middleware.ts` over `src/utils/m.ts` because paths help infer purpose. |
| Colocation | Keep components, tests, types, hooks, and fixtures near the feature they support. |
| Public APIs | Export public contracts from index files and leave internal details unexported. |
| Searchability | Use one obvious search pattern to find everything related to a feature. |
| Architecture hints | Add a `COPILOT.md` file when the project needs durable architecture and convention context. |

Do not scatter related feature files across unrelated utility folders unless the project already has a documented architecture that requires it.

## Code Patterns That Carry Meaning

Write code that makes intent explicit.

- Prefer explicit types over inference where a type explains the contract, such as `function getUser(id: string): Promise<User>`; the untyped baseline shape `function getUser(id)` is insufficient at boundaries.
- Use semantic names such as `activeAdultUsers` instead of `x`.
- Define constants such as `MAX_RETRY_ATTEMPTS = 3` instead of repeating magic values.
- Name functions after behavior and outcomes, not implementation mechanics.
- Use small modules with clear inputs and outputs so nearby context is enough to understand the change.

The identifier `MAX_RETRY_ATTEMPTS` is a model pattern for named configuration-like values; do not replace it with a raw `3` when the value expresses policy.

## Working with Copilot

Provide Copilot with the files, cursor placement, and scope signals needed for accurate suggestions.

| Situation | Preferred behavior |
| --- | --- |
| Working on a feature | Keep relevant files open in tabs, especially auth-related files, model, API, tests, and examples. |
| Editing a local section | Put the cursor near the code where context matters. |
| Complex tasks | Use Copilot Chat rather than relying only on inline completions. |
| Refactors | Describe all files involved before asking for edits. |
| Unclear context | Ask what files are needed before starting a complex change. |

Inline completions have minimal context. Copilot Chat can inspect more files and maintain a broader task frame.

## Context Hints and Documentation

Use durable, concise hints where code alone is not enough.

- Add strategic comments at the top of complex modules to explain flow or purpose.
- Reference existing patterns explicitly, for example `Follow the same pattern as src/api/users.ts`.
- Keep `COPILOT.md` focused on architecture decisions, boundaries, naming, setup, and examples that remain true across tasks.
- Avoid comments that restate obvious code; comments should add context unavailable from names and types.

## Multi-File Changes and Recovery

Make multi-file work traceable.

- Describe scope first: for example, `I need to update the User model, API endpoint, and tests.`
- Work incrementally and verify each change before moving to the next when the task allows it.
- When Copilot struggles with missing context, open relevant files or provide snippets.
- When suggestions are stale, reopen files or restart the session.
- When answers are generic, add constraints, frameworks, and concrete pattern references.

## Good / Bad Examples

The examples below illustrate context-rich naming, types, and constants.

**Good:**

```ts
const MAX_RETRY_ATTEMPTS = 3;

export async function getUser(id: string): Promise<User> {
  return userRepository.findById(id, { maxAttempts: MAX_RETRY_ATTEMPTS });
}
```

Why: The path, exported function, explicit types, semantic names, and named constant communicate the contract and retry policy.

**Bad:**

```ts
export async function go(x) {
  return repo.f(x, 3);
}
```

Why: The names, missing types, and magic number hide intent from reviewers and Copilot.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use descriptive file paths and feature colocation | Paths and proximity are important context signals. |
| Export public APIs from index files | Public contracts become discoverable while internals stay private. |
| Prefer explicit types for public and boundary functions | Types tell Copilot and reviewers what values mean. |
| Use semantic names and named constants | Intent survives local edits and generated suggestions. |
| Keep relevant files open and position the cursor intentionally | Copilot prioritizes open tabs and nearby code. |
| Use Copilot Chat for complex multi-file work | Chat has more context than inline completions. |
| Add `COPILOT.md` or strategic comments for durable non-obvious context | Repeated architecture guidance becomes available across sessions. |
| Work incrementally on multi-file changes | Smaller validated steps reduce accidental drift. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use paths like `src/auth/middleware.ts` | Hide important code in vague paths like `src/utils/m.ts`. |
| Colocate a component with its tests and types | Scatter one feature across unrelated folders. |
| Write `function getUser(id: string): Promise<User>` | Leave boundary functions untyped when the type carries meaning. |
| Define `MAX_RETRY_ATTEMPTS = 3` | Repeat magic number `3` in retry logic. |
| Reference an existing pattern file explicitly | Ask Copilot to infer a pattern from the whole repository. |
| Ask what files are needed for unclear refactors | Start changing files with incomplete context. |

## Checklist Before Opening a PR

- [ ] New or changed file paths describe the feature or responsibility.
- [ ] Related code, tests, types, and hooks are colocated or follow the repository's documented structure.
- [ ] Public APIs are exported intentionally from index files.
- [ ] Public and boundary functions use explicit types where they clarify contracts.
- [ ] Names are semantic and avoid placeholder variables.
- [ ] Policy values use named constants such as `MAX_RETRY_ATTEMPTS` instead of magic numbers.
- [ ] Non-obvious architecture or flow has a concise durable hint in code or `COPILOT.md`.
- [ ] Multi-file changes were described, scoped, and verified incrementally.
