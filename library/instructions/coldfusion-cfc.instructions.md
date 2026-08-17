---
applyTo: "**/*.cfc"
description: "Enforces ColdFusion CFC conventions for CFScript, component structure, access modifiers, dependency injection, SQL safety, input validation, error handling, documentation, and formatting."
---

# ColdFusion CFC Conventions — Component Structure and Safety

These instructions apply to ColdFusion component files (`**/*.cfc`). They are authoritative for CFC structure, CFScript usage, naming, access modifiers, dependency collaboration, SQL safety, input validation, error handling, documentation, and formatting; project framework conventions win where they define stricter application lifecycle, ORM, or dependency injection rules.

## Component Structure and CFScript

Use CFScript where possible for cleaner syntax and maintainable component logic. Group related methods logically within the component, keep setters and getters simple, and move business workflows into service methods rather than property accessors.

Use `this` scope for component properties and methods when it clarifies component-owned state or public application settings. Avoid deprecated or unnecessary `cfcomponent` attributes and deprecated tags or functions.

## Naming, Access, and Documentation

Use meaningful, descriptive names for components, methods, variables, and properties. Follow consistent naming conventions across the project, and do not rely on abbreviations that hide intent; keep `setters/getters` simple when they are needed.

Declare access modifiers for functions and variables: `public`, `private`, `package`, or `remote`. Document all functions with purpose, parameters, and return values using Javadoc-style or project-standard comments when the function is public, remote, or non-obvious.

## Collaboration and Configuration

Prefer dependency injection for component collaboration instead of constructing dependencies deep inside methods. Avoid hardcoding configuration, credentials, URLs, or environment-specific values in CFCs; inject or read them from the approved configuration mechanism.

## SQL, Input, and Output Safety

Use `cfqueryparam` for every dynamic SQL value to prevent SQL injection and preserve query plan stability. Validate and sanitize all input parameters in `public` and `remote` methods, including `public/remote` entry points, before using them in queries, file access, external calls, or rendered output.

Escape CSS hash symbols inside `<cfoutput>` blocks using `##` so ColdFusion does not treat them as expression delimiters.

## Error Handling and Formatting

Use `cftry`/`cfcatch` inside methods when the component can add context, translate exceptions, or ensure cleanup. Do not swallow errors silently.

Use consistent indentation with 2 spaces, and keep tab alignment consistent with the surrounding file. Use ternary operators where they improve clarity, but do not compress complex branching into unreadable expressions.

## Good / Bad Examples

The examples below illustrate parameterized SQL and explicit access in a CFC method.

**Good:**

```cfml
public query function getUser(required numeric userId) {
  cfquery(name = "local.result", datasource = variables.datasource) {
    echo("SELECT id, name FROM users WHERE id = ");
    cfqueryparam(value = arguments.userId, cfsqltype = "cf_sql_integer");
  }

  return local.result;
}
```

Why: The method declares access, validates the required argument shape, and uses `cfqueryparam` for the dynamic SQL value.

**Bad:**

```cfml
function getUser(userId) {
  return queryExecute("SELECT id, name FROM users WHERE id = #userId#");
}
```

Why: The method lacks an access modifier and interpolates untrusted input into SQL.

## Conventions

| Rule | Rationale |
|---|---|
| Use CFScript where possible | Component logic stays cleaner and easier to review. |
| Avoid deprecated tags, functions, and unnecessary `cfcomponent` attributes | Deprecated features reduce compatibility and future maintainability. |
| Use descriptive names and explicit access modifiers | Callers and reviewers can understand the component contract. |
| Prefer dependency injection for collaboration | Components remain testable and do not hide construction logic. |
| Use `cfqueryparam` for dynamic SQL and validate public or remote inputs | SQL injection and invalid input are blocked at the boundary. |
| Escape CSS hash symbols in `<cfoutput>` as `##` | ColdFusion interpolation does not corrupt CSS selectors or colors. |
| Keep 2-space indentation and consistent tab alignment | CFC files remain readable across editors. |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `public`, `private`, `package`, or `remote` deliberately | Leave function visibility implicit. |
| Document purpose, parameters, and return values for public or remote methods | Leave non-obvious component contracts undocumented. |
| Keep setters and getters simple | Put business logic in accessors. |
| Inject collaborators and configuration | Hardcode credentials or instantiate dependencies everywhere. |
| Wrap risky method work with useful `cftry`/`cfcatch` context | Catch errors and ignore them. |
| Use ternary operators for simple expressions | Replace clear branching with dense one-liners. |

## Checklist Before Opening a PR

- [ ] CFC logic uses CFScript where practical and avoids deprecated tags or functions.
- [ ] Components, methods, variables, and properties have meaningful consistent names.
- [ ] Functions and variables declare appropriate access modifiers.
- [ ] Public, remote, or non-obvious functions document purpose, parameters, and return values.
- [ ] Dependencies and configuration are injected or read from approved configuration, not hardcoded.
- [ ] Dynamic SQL uses `cfqueryparam` and boundary inputs are validated and sanitized.
- [ ] CSS hash symbols inside `<cfoutput>` blocks are escaped as `##`.
- [ ] Error handling adds context or cleanup and does not swallow failures.
- [ ] Indentation uses 2 spaces and tab alignment remains consistent.
