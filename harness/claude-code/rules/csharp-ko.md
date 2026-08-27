---
paths:
  - "**/*.cs"
---

<!-- Generated from harness/github-copilot/instructions/csharp-ko.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** C# coding conventions for naming, formatting, language features, performance, exception handling, security, and documentation.

# C# Coding Conventions — Korean Team Style

These instructions apply to C# files matched by the `applyTo` glob. They are authoritative for Korean-language C# style expectations around naming, formatting, readability, language features, exception handling, performance, security, and XML documentation; project `.editorconfig`, framework-specific primitives, and public API compatibility rules win when they define stricter constraints.

## Naming Conventions

Follow Microsoft-style naming so code is predictable across the application.

| Element | Convention | Example |
| --- | --- | --- |
| Interfaces | Prefix `I` plus `PascalCase` | `IAsyncRepository`, `ILogger` |
| Public members | `PascalCase` | `public int MaxCount;`, `public void GetData()` |
| Parameters and local variables | `camelCase` | `int userCount`, `string customerName` |
| Private and internal fields | `_` plus `camelCase` | `private string _connectionString;` |
| Constants | `PascalCase` | `public const int DefaultTimeout = 5000;` |
| Generic type parameters | Prefix `T` plus a descriptive name | `TKey`, `TValue`, `TResult` |
| Async methods | Add the `Async` suffix | `GetUserAsync`, `DownloadFileAsync` |

Use names that communicate purpose without abbreviations. Keep Korean comments acceptable when the team context requires them, but keep identifiers idiomatic C#.

Preserve the naming examples `ILogger`, `TKey`, `TValue`, and `TResult` as standalone examples when documenting C# conventions.

## Formatting and Readability

- Indent `.cs` files with 4 spaces, not tabs.
- Always use braces `{}` for control statements such as `if`, `for`, and `while`, even when the body is one line.
- Add blank lines between method definitions, property definitions, and logical code blocks.
- Write one statement per line.
- Use `var` only when the type is obvious from the right-hand side.
- Use file-scoped namespaces in C# 10 or later to reduce unnecessary indentation.
- Add XML documentation comments for classes and functions when they are authored or changed.

## Language Features

Use modern C# features where they improve clarity and the target framework supports them.

| Feature | Convention | Example |
| --- | --- | --- |
| Async programming | Use `async`/`await` (`async/await`) for I/O-bound work | `async Task<string> GetDataAsync()` |
| `ConfigureAwait` | Use `.ConfigureAwait(false)` in library code where context capture is unnecessary | `await SomeMethodAsync().ConfigureAwait(false)` |
| LINQ | Use LINQ for clear collection querying and transformation | `users.Where(u => u.IsActive).ToList()` |
| Expression-bodied members | Use for simple methods or properties | `public string Name => _name;` |
| Nullable Reference Types | Enable nullable analysis to catch `NullReferenceException` risks | `#nullable enable` |
| `using` declarations | Use concise disposal for `IDisposable` objects | `using var stream = new FileStream(...);` |

## Exceptions and Performance

- Catch only specific exceptions that the code can handle.
- Avoid `catch (Exception)` unless the boundary is intentionally translating or logging unexpected failures.
- Do not use exceptions for ordinary control flow.
- Use `StringBuilder` instead of repeated `+` concatenation in loops or hot paths.
- Use Entity Framework Core `.AsNoTracking()` for read-only queries.
- Avoid unnecessary object allocations, especially inside loops.

## Security and Configuration

| Security area | Rule | Rationale |
| --- | --- | --- |
| Input validation | Validate all external data from users, APIs, files, and services | External input cannot be trusted |
| SQL injection prevention | Use parameterized queries or an ORM such as Entity Framework | SQL text must not contain concatenated untrusted values |
| Sensitive data | Store passwords, connection strings such as `private string _connectionString;`, and API keys in Secret Manager, Azure Key Vault, environment variables, or another configuration management tool | Secrets must not be hardcoded in source |

Integrate these rules into `.editorconfig` and code review so style and safety stay consistent over time.

## Good / Bad Examples

The examples below illustrate naming, async suffixes, braces, and specific exception handling.

**Good:**

```csharp
public async Task<string> GetUserNameAsync(int userId)
{
    try
    {
        return await _userService.GetNameAsync(userId).ConfigureAwait(false);
    }
    catch (UserNotFoundException)
    {
        return string.Empty;
    }
}
```

Why: The method uses `PascalCase`, an `Async` suffix, braces, `ConfigureAwait(false)` for library-style code, and a specific exception.

**Bad:**

```csharp
public async Task<string> getname(int id)
{
    try { return await svc.Get(id); }
    catch (Exception) { return ""; }
}
```

Why: The method violates C# naming, omits clear dependency naming, compresses statements, and catches every exception indiscriminately.

## Conventions

| Rule | Rationale |
|---|---|
| Use `PascalCase`, `camelCase`, `_camelCase`, `I` interfaces, `T` generic parameters, and `Async` suffixes as defined | Naming communicates role and follows C# expectations |
| Format `.cs` files with 4 spaces, braces, blank logical separation, and one statement per line | Consistent formatting makes code easy to parse visually |
| Use `var` only when the type is obvious and prefer file-scoped namespaces in C# 10+ | Readability improves without unnecessary verbosity |
| Document classes and functions with XML comments when authored or changed | Public and team-facing APIs remain understandable |
| Use `async`/`await`, LINQ, expression-bodied members, nullable reference types, and `using` declarations where appropriate | Modern language features reduce boilerplate and runtime mistakes |
| Catch specific exceptions and avoid exceptions for flow control | Error handling stays intentional and debuggable |
| Use `StringBuilder`, `.AsNoTracking()`, and allocation awareness in hot paths | Performance issues are prevented before profiling |
| Validate external data, parameterize SQL, and store secrets outside source | Common security failures are avoided |

## Do / Do Not

| Do | Do not |
|---|---|
| Name interfaces like `IAsyncRepository` and async methods like `GetUserAsync` | Use unclear abbreviations or omit `Async` on asynchronous methods |
| Use 4-space indentation and braces on all control statements | Mix tabs or write brace-less one-line control flow |
| Use file-scoped namespaces in C# 10+ | Add unnecessary namespace indentation in modern projects |
| Enable `#nullable enable` where the project supports nullable analysis | Ignore nullable warnings that can become `NullReferenceException` |
| Catch `UserNotFoundException` or another specific exception | Use broad `catch (Exception)` as routine flow |
| Use Secret Manager, Azure Key Vault, or environment variables for secrets | Hardcode passwords, connection strings, or API keys |

## Checklist Before Opening a PR

- [ ] C# names follow the interface, public member, local, field, constant, generic, and async conventions.
- [ ] `.cs` formatting uses 4 spaces, braces, blank logical separation, and one statement per line.
- [ ] `var`, file-scoped namespaces, XML comments, and modern language features are used where appropriate.
- [ ] Async I/O uses `async`/`await` and library code avoids unnecessary context capture with `.ConfigureAwait(false)` where applicable.
- [ ] Exception handling catches specific exceptions and does not use exceptions for normal flow.
- [ ] String concatenation, Entity Framework Core read queries, and loop allocations are performance-aware.
- [ ] External input is validated, SQL is parameterized or handled by Entity Framework, and secrets are not hardcoded.
