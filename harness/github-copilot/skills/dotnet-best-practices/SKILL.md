---
name: dotnet-best-practices
description: >-
  Review or improve .NET and C# code against solution/project best practices for documentation, architecture, dependency injection, resources, async, tests, configuration, Semantic Kernel, logging, performance, security, SOLID, and code quality. Use when asked for .net/c# or .NET/C# best practices or cleanup.
---

# .NET and C# best practices

Evaluate selected .NET/C# code or a project area, identify gaps against the solution's conventions, and return actionable refactoring guidance or code changes that preserve behavior while improving maintainability, testability, security, and consistency.

Use the active solution/project. conventions as the source of truth when they are more specific than general .NET guidance.

## When to invoke

- "Review this C# code for .NET best practices."
- "Make this .NET service follow our conventions."
- "Check dependency injection, logging, and async patterns."
- "Improve Semantic Kernel integration in this project."
- "Add XML docs and tests for this C# API."

## Criteria

### Documentation and structure

- [ ] Public classes, interfaces, methods, and properties have XML documentation comments with parameter and return descriptions where applicable.
- [ ] Namespaces follow the established `{Core|Console|App|Service}.{Feature}` structure when that convention exists in the solution.
- [ ] Names reflect domain concepts instead of transport, UI, or implementation details.

### Architecture and dependency injection

| Area | Prefer | Avoid |
| --- | --- | --- |
| Construction | Primary constructor syntax such as `public class MyClass(IDependency dependency)` for dependency injection. | Service location or mutable public dependencies. |
| Handlers | Command Handler pattern with generic base classes such as `CommandHandler<TOptions>`. | Large orchestration methods that mix parsing, validation, and execution. |
| Interfaces | Interface segregation with `I`-prefixed names for test seams. | One broad interface with unrelated responsibilities. |
| Factories | Factory pattern for complex object creation. | Repeated ad hoc object graphs in callers. |
| Lifetimes | Register services as `Singleton`, `Scoped`, or `Transient` based on state and dependency lifetime. | Capturing scoped services in singletons. |
| Validation | Constructor null checks with `ArgumentNullException`. | Late null failures deep in execution. |

Use `Microsoft.Extensions.DependencyInjection` patterns and register service interfaces for testability.

### Resources, configuration, and localization

- [ ] Localized messages and error strings use `ResourceManager`.
- [ ] Log and error text are separated into `LogMessages` and `ErrorMessages` resource files.
- [ ] Resource access uses `_resourceManager.GetString("MessageKey")` with a named key, not inline display text.
- [ ] Settings use strongly-typed configuration classes bound from `IConfiguration` and `appsettings.json`.
- [ ] Configuration classes carry validation attributes such as `Required` and `NotEmptyOrWhitespace` when values are mandatory.

### Async, errors, logging, and security

| Concern | Rule |
| --- | --- |
| Async/Await I/O | Use `async`/`await` (async/await) for I/O and long-running tasks; return `Task` or `Task<T>`. |
| Context capture | Use `ConfigureAwait(false)` where appropriate for library code that does not require a captured context. |
| Exceptions | Throw specific exceptions with descriptive messages; use try-catch blocks only for expected failure scenarios. |
| Logging | Use structured logging through `Microsoft.Extensions.Logging` and scopes with meaningful context. |
| Data access | Use parameterized queries for database operations. |
| Input | Validate and sanitize external input, especially AI/ML prompts and tool outputs. |
| Disposal | Implement proper disposal patterns for owned resources. |

### Testing and AI integration

- [ ] Tests use MSTest, FluentAssertions, and Moq when those are the established project tools.
- [ ] Tests follow AAA: Arrange, Act, Assert.
- [ ] Success paths, failure paths, and null parameter validation are covered.
- [ ] AI operations use `Microsoft.SemanticKernel` with explicit kernel configuration and service registration.
- [ ] ChatCompletion, Embedding, and related model settings are handled through structured configuration.
- [ ] Structured output patterns are used where AI responses must be reliable.

## Gotchas

- **Do not add XML documentation that restates the method name**: documentation must explain behavior, parameters, return values, or constraints.
- **Do not make every service `Singleton` for speed**: lifetime must match state and dependencies.
- **Do not use `ConfigureAwait(false)` blindly in application UI or request code**: apply it where context capture is unnecessary.
- **Do not weaken tests to satisfy refactoring**: preserve behavior and add assertions for changed seams.

## Output template

```markdown
## .NET best-practices review

**Status:** pass | fixes recommended | blocked
**Scope:** `<selection/project/path>`

| Area | Finding | Severity | Recommendation |
| --- | --- | --- | --- |
| Dependency injection | <evidence> | High/Medium/Low | <specific fix> |

### Refactoring plan or changes
1. <small, behavior-preserving step>
2. <test or validation step>

### Validation
- `<command or inspection>`: pass | fail | not run, <reason>
```

## Quality gate

- [ ] Public API documentation, namespace structure, and naming were checked.
- [ ] Dependency injection, service lifetimes, interface segregation, and factory seams were evaluated.
- [ ] ResourceManager, `LogMessages`, `ErrorMessages`, and configuration binding were checked where relevant.
- [ ] Async, exception, structured logging, disposal, input validation, and parameterized query practices were checked.
- [ ] MSTest, FluentAssertions, Moq, AAA, success, failure, and null validation tests were considered.
- [ ] Semantic Kernel usage is reviewed when AI code is in scope.
- [ ] Recommendations preserve behavior and include validation evidence.
- [ ] SOLID principles, cohesion, coupling, duplication, and disposal patterns were considered.
