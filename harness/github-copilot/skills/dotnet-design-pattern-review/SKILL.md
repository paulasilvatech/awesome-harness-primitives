---
name: "dotnet-design-pattern-review"
description: >-
  Review C# and .NET code for design pattern quality, SOLID principles, dependency injection, repository/provider abstractions, ResourceManager usage, async practices, testability, and maintainability. Use this skill when asked for a .NET or C# design pattern review, architecture critique, or pattern-focused code review without modifying code.
---

# .NET C# design pattern review

Review selected C#/.NET code or a solution for pattern fit, architecture, SOLID compliance, async/resource handling, configuration, security, and testability, then return actionable findings without changing files.

Use it for .NET/C# design reviews across a solution/project.

Also match user wording such as `.net/c#` or `net/c` design pattern review.

## When to invoke

- "Review this C# code for design patterns."
- "Do a .NET architecture and SOLID review."
- "Check whether these command handlers follow the pattern."
- "Review our provider and repository abstractions."
- "Suggest design-pattern improvements without editing code."

## Criteria

### Required project patterns

| Pattern | Evidence to look for | Common defect |
| --- | --- | --- |
| Command Pattern | Generic base classes such as `CommandHandler<TOptions>`, an `ICommandHandler<TOptions>` interface, `CommandHandlerOptions` inheritance, and static `SetupCommand(IHost host)` methods. | Business logic in console parsing or command setup instead of a handler. |
| Factory Pattern | Complex object creation hidden behind factories with service provider integration. | Constructors manually assemble deep dependency graphs or use service locator behavior. |
| Dependency Injection | Primary constructor syntax where appropriate, `ArgumentNullException` null checks, interface abstractions, and proper service lifetimes. | Singleton captures scoped services, concrete dependencies prevent mocking, or null checks are inconsistent. |
| Repository Pattern | Async data access interfaces and provider abstractions for connections. | Repository exposes provider-specific details or blocks on async calls. |
| Provider Pattern | External service abstractions for database, AI, and other integrations with clear contracts and configuration handling. | Provider leaks SDK types throughout the app or hides errors without structured logging. |
| Resource Pattern | `ResourceManager` usage with separate `.resx` files such as `LogMessages` and `ErrorMessages`. | User-facing or log messages are hard-coded and cannot be localized or standardized. |

### Review checklist

- [ ] **Design Patterns**: Identify patterns used. Decide whether Command Handler, Factory, Provider, Repository, Template Method, and Strategy patterns are correctly implemented or missing where beneficial.
- [ ] **Architecture**: Check namespace conventions such as `{Core|Console|App|Service}.{Feature}`, separation between Core and Console projects, modularity, and readability.
- [ ] **.NET Best Practices**: Check primary constructors, async/await with `Task` returns, `ResourceManager`, structured logging, strongly-typed configuration, and options validation.
- [ ] **SOLID Principles**: Flag Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion violations with evidence.
- [ ] **Performance**: Review async flow, resource disposal, `ConfigureAwait(false)` where library code benefits from it, batching, caching, and parallel processing opportunities.
- [ ] **Maintainability**: Check separation of concerns, error handling consistency, configuration flow, cohesive method/class size, duplication, and naming.
- [ ] **Testability**: Verify dependencies are abstracted via interfaces, components are mockable, async paths are testable, and code fits the AAA pattern.
- [ ] **Security**: Check input validation, secure credential handling, parameterized queries, and safe exception handling.
- [ ] **Documentation**: Check XML docs for public APIs, parameter and return descriptions, and resource file organization.

Also verify Core/Console boundaries, parameter/return documentation, and self-explanatory naming where public APIs are involved.

## Improvement focus areas

| Area | Recommend improvements such as |
| --- | --- |
| Command Handlers | Validation in base classes, consistent result/error handling, cancellation token flow, resource management, and a predictable `SetupCommand(IHost host)` boundary. |
| Factories | Dependency configuration, service provider integration without service locator abuse, ownership/disposal rules, and named factory methods. |
| Providers | Connection management, retry/error policy, async methods, exception logging, and clear contracts for database or AI integrations. |
| Configuration | Strongly typed options, data annotations, validation attributes, secure sensitive value handling, and startup validation. |
| AI/ML Integration | Semantic Kernel patterns, structured output handling, model configuration isolation, prompt/input validation, and predictable logging. |

## Output template

```markdown
## .NET design pattern review

**Status:** pass | improvements recommended | blocking issues
**Scope:** `<selection, project, or solution>`

| # | Area | Severity | Finding | Evidence | Recommendation |
| --- | --- | --- | --- | --- | --- |
| 1 | `Command Pattern` | High | `<pattern defect>` | `<file/member>` | `<specific change>` |

### Pattern coverage
| Pattern | Present | Quality | Notes |
| --- | --- | --- | --- |
| `Command Pattern` | yes | strong | `<evidence>` |

### Validation
- Code changed: no
- Files reviewed: `<count or list>`
```

## Quality gate

- [ ] No code changes were made.
- [ ] Every finding includes concrete evidence from a file, type, member, or selected code.
- [ ] Command Handler, Factory, Dependency Injection, Repository, Provider, and Resource patterns were explicitly considered.
- [ ] SOLID, async/resource handling, configuration, security, documentation, and testability were reviewed.
- [ ] Recommendations are specific enough to implement, not generic advice.
- [ ] The verdict distinguishes blocking issues from optional improvements.
