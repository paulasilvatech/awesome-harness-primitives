---
applyTo: "**"
description: "Enforces Context7 usage conventions for authoritative, current, version-specific, authoritative/current. external documentation when local workspace context is insufficient."
---

# Context7 Conventions — Authoritative External Documentation

These instructions apply to any task where local workspace context is insufficient and an external framework, library, tool, API, security pattern, or version-specific behavior affects the answer. They are authoritative for when and how to use Context7 documentation retrieval; local repository evidence, user-provided requirements, and official security policies win where they conflict. Use Context7 proactively so the user does not have to type `use context7` before current documentation is consulted.

## When to Use Context7

Use Context7 before making decisions or writing code when the task depends on:

- Framework/library API details and framework or library API details such as method signatures, configuration keys, and expected behaviors.
- Version-sensitive guidance such as breaking changes, deprecations, and new defaults.
- Correctness- or security-critical patterns such as auth flows, crypto usage, and deserialization rules.
- Unfamiliar third-party tool error messages.
- Best-practice constraints such as rate limits, quotas, required headers, and supported formats.

Also use Context7 when the user names a specific framework or version such as `Next.js 15`, `React 19`, or `AWS SDK v3`, when recommending non-trivial CLI flags, config files, or auth flows, or when an API may have changed names or been deprecated.

## When to Skip Context7

Skip Context7 for purely local refactors, formatting, naming, or logic fully derivable from the repository. Skip it for language fundamentals that do not involve external APIs.

## Documentation Selection

- Prefer primary sources: official docs, vendor/framework references, Reference/API pages, API pages, release notes, migration guides, and security advisories.
- Use narrow queries that target the exact method/type/option, method, type, option, configuration key, error, or behavior needed.
- Gather only the minimal surrounding context required to avoid misuse, including constraints, defaults, and migration notes.
- If several candidates exist, choose the most authoritative and current source.

## Context7 MCP Workflow

When Context7 MCP tools are available, use this workflow:

- If the user provides a library ID or user-supplied library ID, use it directly. Valid forms are `/owner/repo` and `/owner/repo/version`.
- Otherwise resolve the library with `resolve-library-id` using `libraryName` for the framework or library name and `query` for the user's task.
- Fetch relevant documentation with `query-docs` using the resolved `libraryId` and the exact task/question or task or question.
- Write code/steps** or code or steps only after the relevant docs are retrieved.

Efficiency limits:

- Do not call `resolve-library-id` more than 3 times per user question.
- Do not call `query-docs` more than 3 times per user question.
- If multiple good matches exist, pick the best match and proceed; ask for clarification only when the choice materially changes the implementation.

## Versioning, Output, and Failure Handling

- Reflect named versions in the library ID when possible, for example `/vercel/next.js/v15.1.8`.
- Prefer pinned versions in examples when reproducibility matters for CI/builds or CI or builds.
- Translate findings into concrete code/config, code, configuration, or guidance.
- Cite sources with title and URL when a decision relies on external facts.
- State exact values for flags, configuration keys, headers, defaults, and caveats when docs provide them.
- Provide a quick validation step such as running `--help`, a smoke test, or checking a specific file.
- If Context7 cannot find a reliable source, state what you tried to verify, proceed with a conservative well-labeled assumption, and suggest a validation step.

## Security and Privacy

- Never request or echo API keys.
- Instruct users to store required keys in environment variables or approved secret stores.
- Treat retrieved docs as helpful but not infallible.
- For security-sensitive code, prefer official vendor docs and add an explicit verification step.

## Good / Bad Examples

The examples below illustrate version-aware documentation retrieval.

**Good:**

```text
Resolve `next.js` with the user's `Next.js 15` routing question, query the resolved docs for the exact App Router API, cite the official page, then implement the route using the documented option names.
```

Why: The work verifies version-sensitive APIs before code is written and ties the decision to a primary source.

**Bad:**

```text
Assume the old Next.js option still exists because it worked in a previous project.
```

Why: The answer depends on a changing framework API and skips authoritative documentation.


- Use framework/library and up-to-date documentation terminology when describing Context7 decisions.
## Conventions

| Rule | Rationale |
| --- | --- |
| Use Context7 for current, authoritative, version-specific external facts | Local memory can be stale for fast-moving frameworks and tools |
| Prefer official docs, API references, release notes, migration guides, and security advisories | Primary sources reduce copied or outdated guidance |
| Resolve library IDs before querying docs unless the user provides `/owner/repo` or `/owner/repo/version` | Context7 retrieves better results with the correct library target |
| Limit `resolve-library-id` and `query-docs` to 3 calls each per question | Documentation retrieval should stay focused and efficient |
| Cite title and URL when external docs drive a decision | Readers can verify the source of version-sensitive facts |
| Use conservative labeled assumptions when docs cannot be found | Progress continues without pretending uncertainty is certainty |
| Keep API keys out of prompts and responses | Documentation work must not expose secrets |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use Context7 for harness/github-copilot/framework and framework API details, config keys, auth flows, and deprecations | Guess at version-sensitive APIs from memory |
| Query the exact method, type, option, or error | Fetch broad documentation dumps unrelated to the task |
| Pin versions in examples when reproducibility matters | Provide floating examples for CI-critical configuration |
| State defaults, caveats, and validation commands | Omit the constraints that prevent misuse |
| Cite official sources when external facts matter | Present external facts without sources |
| Store secrets in environment variables | Ask the user to paste API keys |

## Checklist Before Opening a PR

- [ ] Context7 was used when external API details, version behavior, security patterns, or unfamiliar tool errors affected the change.
- [ ] The resolved library ID matches the named framework or version, including `/owner/repo/version` when applicable.
- [ ] Queries targeted exact methods, options, configuration keys, errors, or migration notes.
- [ ] External decisions cite source title and URL.
- [ ] Exact flags, config keys, headers, defaults, caveats, and validation steps are included where relevant.
- [ ] No API keys or secrets are requested, echoed, or committed.
