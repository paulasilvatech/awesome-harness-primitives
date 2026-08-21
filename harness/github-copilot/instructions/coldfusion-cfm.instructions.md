---
applyTo: "**/*.cfm"
description: "Enforces ColdFusion CFM conventions for CFScript, Application.cfc usage, HTMX targets, cfoutput escaping, SQL safety, includes, validation, errors, and formatting."
---

# ColdFusion CFM Conventions — Templates and Request Pages

These instructions apply to ColdFusion Markup Language template files (`**/*.cfm`). They are authoritative for CFM page structure, CFScript usage, HTMX target behavior, `<cfoutput>` hash escaping, SQL safety, input validation, includes, error handling, credentials, comments, and formatting; CFC-specific component rules and project framework conventions win where they define stricter service or application architecture.

## Template Structure and Application Boundaries

Use `Application.cfc` for application settings and request handling. Keep reusable business logic in CFCs instead of embedding it in CFM templates, and use CFM files primarily for request orchestration and rendering.

Use CFScript where possible for cleaner syntax. Prefer `cfinclude` for shared templates when it improves reuse, but avoid circular includes and hidden execution chains that make request flow hard to reason about.

## HTMX and Output Escaping

When using HTMX inside `<cfoutput>` blocks, escape hash symbols (`#`) with double hashes (`##`) to prevent unintended ColdFusion variable interpolation. Escape CSS hash symbols inside `<cfoutput>` blocks the same way.

If a file is an HTMX target file, make the top line exactly:

```cfml
<cfsetting showDebugOutput = "false">
```

This prevents debug output from corrupting partial HTML responses.

## SQL, Input, and Secrets

Use `cfqueryparam` for every dynamic SQL value to prevent SQL injection. Validate and sanitize all user input before using it in queries, file paths, external requests, or rendered output.

Avoid hardcoding credentials or sensitive data in source files. Read configuration from the approved application settings, environment, or secret store.

## Error Handling, Comments, and Formatting

Use `cftry`/`cfcatch` for error handling and logging when the page can add useful context or recover safely. Comment complex logic and document functions with purpose and parameters when functions are present in the template.

Use consistent indentation with 2 spaces and keep tab alignment consistent. Use ternary operators where possible for simple expressions, but keep complex conditional rendering readable.

## Good / Bad Examples

The examples below illustrate HTMX target and `<cfoutput>` hash handling.

**Good:**

```cfml
<cfsetting showDebugOutput = "false">

<cfoutput>
  <div id="result" hx-target="##result">Loaded</div>
  <style>.swatch { color: ##336699; }</style>
</cfoutput>
```

Why: The HTMX target disables debug output and escapes hash symbols inside `<cfoutput>`.

**Bad:**

```cfml
<cfoutput>
  <div id="result" hx-target="#result">Loaded</div>
  <style>.swatch { color: #336699; }</style>
</cfoutput>
```

Why: ColdFusion can interpret single hash symbols as interpolation delimiters and corrupt the output.

## Conventions

| Rule | Rationale |
|---|---|
| Use `Application.cfc` for application settings and request handling | Application lifecycle logic stays centralized. |
| Move reusable logic into CFCs and keep CFM templates focused on rendering | Templates remain maintainable and testable. |
| Use CFScript where possible and avoid deprecated tags or functions | Modern syntax is easier to read and more compatible. |
| Use `cfqueryparam` and validate user input | SQL injection and invalid request data are blocked early. |
| Escape `#` as `##` inside `<cfoutput>` for CSS and HTMX values | ColdFusion interpolation does not damage literals. |
| Put `<cfsetting showDebugOutput = "false">` at the top of HTMX target files | Debug output does not break partial responses. |
| Use 2-space indentation and consistent tab alignment | Templates remain readable across editors. |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `cfinclude` for simple shared templates | Create circular include chains. |
| Sanitize input before queries, rendering, or file access | Trust request parameters directly. |
| Store secrets outside CFM source files | Hardcode credentials or sensitive values. |
| Use `cftry`/`cfcatch` when adding context or logging | Swallow template errors silently. |
| Comment complex logic | Comment obvious markup or simple assignments. |
| Use ternary operators for simple choices | Compress complex rendering branches into unreadable expressions. |

## Checklist Before Opening a PR

- [ ] Application settings and request lifecycle behavior belong in `Application.cfc`.
- [ ] Reusable logic is organized into CFCs rather than duplicated in CFM templates.
- [ ] CFScript is used where practical and deprecated tags or functions are avoided.
- [ ] Dynamic SQL uses `cfqueryparam` and user input is validated and sanitized.
- [ ] Hash symbols inside `<cfoutput>` are escaped as `##` for CSS and HTMX values.
- [ ] HTMX target files begin with `<cfsetting showDebugOutput = "false">`.
- [ ] Credentials and sensitive data are not hardcoded in source files.
- [ ] Error handling logs or adds context without hiding failures.
- [ ] Indentation uses 2 spaces and tab alignment remains consistent.
