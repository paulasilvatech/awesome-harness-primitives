---
paths:
  - "**/*.genai.*"
---

<!-- Generated from harness/github-copilot/instructions/genaiscript.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Conventions for GenAIScript files covering script role, references, TypeScript ESM generation, global APIs, error handling, and maintainability.

# GenAIScript Conventions — Script Generation

These instructions apply to GenAIScript scripts and GenAIScript-focused answers in files matched by `**/*.genai.*`. They are authoritative for TypeScript generation style, API selection, reference usage, and maintainability in GenAIScript files; repository-specific runtime, security, and packaging rules win when they impose stricter constraints than the GenAIScript defaults documented at https://microsoft.github.io/genaiscript.

## Language Model and Runtime Assumptions

Generate TypeScript GenAIScript code using ESM modules for Node.JS.

- Use modern TypeScript syntax that is clear in a script context rather than building framework-style abstractions.
- Treat GenAIScript scripts as automation glue around prompts, files, model calls, and structured outputs.
- Keep scripts simple enough that a user can review the generated prompt flow, inputs, outputs, and side effects.
- Prefer explicit names for generated files, prompts, variables, and outputs; avoid clever dynamic construction when static structure communicates intent.

## GenAIScript API Usage

Prefer APIs from GenAIScript `genaiscript.d.ts` rather than Node.js imports.

| Need | Convention |
| --- | --- |
| GenAIScript globals | Use the global types and helpers already loaded from `genaiscript.d.ts`; do not import them. |
| File, prompt, and model work | Reach first for GenAIScript APIs because they express script intent and integrate with the GenAIScript runtime. |
| Node.js modules | Avoid Node.js imports unless the GenAIScript API surface does not cover the need. |
| External boundaries | Handle expected I/O and external API errors close to the boundary. |
| Unexpected failures | Let unexpected exceptions surface to the caller instead of swallowing them or returning ambiguous partial results. |

When GenAIScript documentation is needed, prefer the official `llms.txt` reference at https://microsoft.github.io/genaiscript/llms.txt.

## Structure and Maintainability

Write generated scripts for reviewability first.

- Keep the top-level script flow readable: gather inputs, build prompts, call the model or tool, validate output, then write results.
- Use small helper functions only when they remove duplication or isolate an I/O boundary.
- Add TODOs where the generated code depends on an assumption, unresolved product decision, or user-specific detail that requires review.
- Do not add TODOs for work the generated script already completes; a TODO should flag uncertainty, not excuse incomplete implementation.
- Avoid hidden side effects; name any files, commands, or external services the script touches.

## Good / Bad Examples

The examples below illustrate GenAIScript-style API preference and boundary error handling.

**Good:**

```ts
const source = await workspace.readText("README.md")
if (!source.trim()) throw new Error("README.md is empty")

const summary = await ai.generateText(`Summarize this project:

${source}`)
await workspace.writeText("SUMMARY.md", summary.text)
```

Why: The script uses GenAIScript globals, keeps the flow obvious, and lets unexpected model or write failures surface.

**Bad:**

```ts
import { readFileSync, writeFileSync } from "node:fs"

try {
  const source = readFileSync("README.md", "utf8")
  writeFileSync("SUMMARY.md", String(source))
} catch {
  // ignore
}
```

Why: The script imports Node.js APIs unnecessarily, uses synchronous I/O, and swallows failures that the caller needs to see.

## Conventions

| Rule | Rationale |
| --- | --- |
| Generate TypeScript using ESM models for Node.JS | GenAIScript scripts align with modern TypeScript and Node execution expectations |
| Prefer GenAIScript APIs from `genaiscript.d.ts` over Node.js imports | Runtime-provided APIs integrate with GenAIScript and reduce platform-specific code |
| Do not import GenAIScript global types or helpers | The global context already loads them, so imports add noise or can fail |
| Keep code simple and explicit | Users can audit generated AI automation before trusting its side effects |
| Handle expected I/O and external API errors at boundaries | Recoverable failures get useful context without hiding programming errors |
| Let unexpected exceptions surface to the caller | Silent failures make generated automation unreliable and hard to debug |
| Add TODOs only where uncertainty remains | Reviewers can distinguish real assumptions from unfinished work |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use TypeScript ESM for generated GenAIScript code | Generate CommonJS-style or untyped script fragments |
| Use GenAIScript globals and APIs from `genaiscript.d.ts` | Import GenAIScript globals or prefer raw Node.js APIs by default |
| Keep the script flow linear and reviewable | Hide prompt construction, file writes, or model calls behind opaque abstractions |
| Add TODOs for user-reviewable uncertainty | Add TODOs for known requirements that should be implemented now |
| Handle I/O and external API errors with context | Catch every error and continue with invalid or partial output |

## Checklist Before Opening a PR

- [ ] GenAIScript files use TypeScript ESM conventions for Node.JS.
- [ ] The script prefers GenAIScript APIs from `genaiscript.d.ts` and avoids unnecessary Node.js imports.
- [ ] Global GenAIScript types and helpers are used without imports.
- [ ] I/O and external API boundaries have clear error handling.
- [ ] Unexpected exceptions are not swallowed.
- [ ] TODOs mark only genuine assumptions or unresolved user decisions.
- [ ] The official GenAIScript reference was used when API behavior was uncertain.

## References

- GenAIScript documentation: https://microsoft.github.io/genaiscript
- GenAIScript llms.txt: https://microsoft.github.io/genaiscript/llms.txt
