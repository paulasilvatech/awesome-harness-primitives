---
applyTo: "**"
description: "Enforces self-explanatory code comments that explain why, constraints, and risks while avoiding obvious, redundant, stale, decorative, or historical comments."
---

# Self-Explanatory Code Commenting Conventions — Explain Why, Not What

These instructions apply to comments in any programming language and to committed examples that include comments. They are authoritative for when comments add value, when code should be refactored instead, and which comment annotations are acceptable; language-specific documentation, public API, and generated-code conventions win when they require stricter doc comment formats.

## Core Principle

Write code that speaks for itself. Comment only when necessary to explain why a decision exists, what external constraint applies, or which non-obvious risk a maintainer must preserve. Do not comment ordinary mechanics that better names or simpler structure could make clear.

## Comments to Avoid

Avoid obvious comments such as `let counter = 0; // Initialize counter to zero`, redundant comments such as `return user.name; // Return the user's name`, outdated comments that contradict code, dead-code comments such as `// const oldFunction = () => { ... };`, changelog comments such as `Modified by John on 2023-01-15`, and decorative divider comments such as `//=====================================`. Remove stale comments instead of updating code around them.

## Comments to Write

Write comments for complex business logic, non-obvious algorithms, regex patterns, external API constraints, operational gotchas, configuration rationale, and constants whose value comes from a contract or risk tradeoff. Examples include progressive tax brackets, Floyd-Warshall all-pairs shortest paths, email regex intent, GitHub API rate limit: 5000 requests/hour for authenticated users, `MAX_RETRIES = 3`, and `API_TIMEOUT = 5000` when the timeout leaves buffer against an AWS Lambda 15s limit.

Use public API documentation comments when consumers need parameter, return, exception, or usage information. For example, a compound-interest API can document `principal`, `rate`, `time`, `compoundFrequency`, and the returned final amount.

## Decision Framework

Before writing a comment, ask whether the code is self-explanatory, whether a better variable or function name would remove the need, whether the comment explains why rather than what, and whether it will help future maintainers. If a rename or extraction solves the problem, refactor instead of commenting.

## Annotation Tags

Use annotations sparingly and keep each one actionable.

| Tag | Use |
| --- | --- |
| `TODO` | Planned follow-up with enough context to act |
| `FIXME` | Known defect that needs correction |
| `HACK` | Temporary workaround for a named constraint, such as a library v2.1.0 bug |
| `NOTE` | Non-obvious assumption, such as UTC timezone behavior |
| `WARNING` | Dangerous behavior, such as mutation of the original array |
| `PERF` | Hot-path or caching consideration |
| `SECURITY` | Security-critical constraint, such as validating input before SQL use |
| `BUG` | Reproducible edge-case failure |
| `REFACTOR` | Known extraction or design cleanup |
| `DEPRECATED` | Replacement API and removal expectation, such as `newApiFunction()` before v3.0 |

## Technical Vocabulary

Preserve these source terms when they apply to edits in this domain: `AVOID` `FUNCTIONS` `UTILITY` `WHAT` `WRITE` `variable/function`.

Examples may use JavaScript, but the rule applies to any language that supports comments.

## Good / Bad Examples

The examples below show when a comment adds durable context.

**Good:**

```javascript
// Apply progressive tax brackets: 10% up to 10k, 20% above.
const tax = calculateProgressiveTax(income, [0.10, 0.20], [10000]);
```

Why: The comment explains business policy that is not fully visible from the call.

**Bad:**

```javascript
let counter = 0; // Initialize counter to zero
counter++; // Increment counter by one
```

Why: The comments repeat syntax and add maintenance noise.

## Conventions

| Rule | Rationale |
|---|---|
| Prefer self-documenting names and small functions over explanatory comments | Clear code ages better than prose attached to unclear code |
| Comment why, constraints, and risks rather than what the next line does | Maintainers need intent that code cannot express alone |
| Keep comments accurate, grammatical, professional, and close to the code they describe | Misleading comments are worse than no comments |
| Use public API docs for externally consumed contracts | Consumers need stable parameter and return information |
| Use annotation tags only when actionable | Marker comments without context become permanent clutter |
| Delete commented-out code and changelog comments | Version control already preserves history |

## Do / Do Not

| Do | Do not |
|---|---|
| Explain a non-obvious algorithm choice like Floyd-Warshall | Narrate a simple loop increment |
| Document external constraints such as API rate limits | Copy implementation details already obvious from names |
| Explain constants such as `MAX_RETRIES` and `API_TIMEOUT` when derived from policy | Leave magic numbers unexplained |
| Use `TODO`, `FIXME`, `HACK`, `SECURITY`, or `DEPRECATED` with context | Drop vague marker comments without an action |
| Remove stale or contradictory comments | Preserve comments that no longer match the code |
| Refactor names before adding comments | Use comments to compensate for confusing names |

## Checklist Before Opening a PR

- [ ] New comments explain why, constraints, risks, public API contracts, or non-obvious behavior.
- [ ] Obvious, redundant, stale, decorative, dead-code, and changelog comments were removed.
- [ ] Variable, function, and type names were improved where naming could replace a comment.
- [ ] Annotation comments are actionable and use the approved tags.
- [ ] Public API comments are accurate and useful to callers.
- [ ] Comments are grammatically correct, professional, and placed next to the code they describe.
