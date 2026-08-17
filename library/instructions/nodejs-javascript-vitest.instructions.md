---
applyTo: "**/*.js,**/*.mjs,**/*.cjs"
description: "Enforces Node.js 20+ JavaScript conventions with ES2022, ESM, built-in modules, async/await, Vitest tests, README updates, and concise dependency choices."
---

# Node.js JavaScript Conventions — ES2022 and Vitest

These instructions apply to JavaScript runtime files matched by `**/*.js`, `**/*.mjs`, and `**/*.cjs`. They are authoritative for Node.js 20+ JavaScript style, ES2022 usage, asynchronous patterns, dependency restraint, Vitest coverage, documentation updates, and user-facing language choices; package-specific tooling or framework instructions win when they define stricter module, build, or test requirements.

## Runtime, Modules, and Dependencies

Use JavaScript with ES2022 features and Node.js 20+ behavior. Prefer ESM modules for new code and keep CommonJS only where the existing file or package boundary requires `.cjs` compatibility.

Use Node.js built-in modules before adding external dependencies. Import built-ins with the `node:` prefix, such as `node:fs/promises` or `node:util`. Ask the user before adding a new runtime dependency unless the task explicitly authorizes dependency changes.

## Code Style

Keep code simple and maintainable. Prefer functions over classes unless stateful object behavior is clearly warranted. Use descriptive variable and function names, avoid unnecessary comments, and make code self-explanatory through structure.

Use `undefined` for optional values instead of `null`. Avoid callbacks for asynchronous control flow; use `async`/`await`, and convert callback APIs with the `node:util` `promisify` function when no promise API exists.

## Testing with Vitest

Use Vitest for tests. Write tests for all new features and bug fixes, including edge cases and error handling. NEVER change the original code to make it easier to test; test observable behavior instead.

Keep tests deterministic: avoid real network calls, time dependence, and filesystem writes outside project-controlled test fixtures. Use mocks or dependency seams already present in the code rather than weakening production behavior.

## Documentation and User Interaction

Update `README.md` when adding a feature or making a significant behavior change that users need to understand. Answer in the same language as the user's question, but generate code, comments, and documentation in English unless the repository clearly uses another language.

In non-interactive execution, make reasonable assumptions from the repository context instead of stopping for clarification; when interaction is available and requirements are ambiguous, ask a focused question before adding dependencies or changing design.

## Good / Bad Examples

The examples below illustrate asynchronous Node.js style with built-in modules.

**Good:**

```js
import { readFile } from 'node:fs/promises';

export async function readConfig(path) {
  const text = await readFile(path, 'utf8');
  return JSON.parse(text);
}
```

Why: The code uses ESM, a `node:` built-in promise API, `async`/`await`, and a function with a descriptive name.

**Bad:**

```js
const fs = require('fs');

function readConfig(path, callback) {
  fs.readFile(path, (error, data) => callback(error, JSON.parse(data)));
}
```

Why: The code uses callback flow and omits the built-in promise API available in modern Node.js.

## Conventions

| Rule | Rationale |
|---|---|
| Use ES2022 features on Node.js 20+ and prefer ESM for new code | Modern syntax reduces boilerplate and matches current Node.js behavior. |
| Prefer Node.js built-in modules and avoid external dependencies where possible | Smaller dependency graphs reduce maintenance and supply-chain risk. |
| Use `async`/`await` and `node:util` `promisify` for callback-only APIs | Asynchronous code stays readable and error handling remains linear. |
| Use `undefined` for optional values, not `null` | Optional state has one representation across the codebase. |
| Prefer functions over classes | Simple behavior stays lightweight and easier to test. |
| Test new features and bug fixes with Vitest, including edge cases and error handling | Behavior changes are protected against regressions. |
| Update `README.md` when user-visible behavior changes | Users can discover new features and changed usage. |

## Do / Do Not

| Do | Do not |
|---|---|
| Import built-ins with `node:` and use promise APIs | Add external packages for standard-library capabilities. |
| Use descriptive function and variable names | Hide intent behind terse names. |
| Keep comments rare and reserved for non-obvious logic | Comment code that is already self-explanatory. |
| Write Vitest tests against original behavior | Change production code only to make tests easier. |
| Cover edge cases and error handling | Test only the happy path. |
| Ask before adding dependencies when interaction is available | Add dependencies silently for convenience. |
| Answer the user in their language and keep generated code in English | Mix localized prose into code identifiers or comments without project precedent. |

## Checklist Before Opening a PR

- [ ] New JavaScript targets Node.js 20+ and uses ES2022 features appropriately.
- [ ] Module style matches the file boundary, with ESM preferred for new `.js` or `.mjs` code.
- [ ] Built-in modules are preferred and imported with `node:` where applicable.
- [ ] Asynchronous code uses `async`/`await` or `node:util` `promisify`, not callback chains.
- [ ] Optional values use `undefined` rather than `null`.
- [ ] New features and bug fixes have Vitest coverage for normal, edge, and error cases.
- [ ] Production code was not weakened only to make tests easier.
- [ ] `README.md` reflects user-visible feature or behavior changes.
