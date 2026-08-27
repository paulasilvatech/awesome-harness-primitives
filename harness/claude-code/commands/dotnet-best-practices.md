---
description: "Apply .NET and C# best practices to selected solution code and document required improvements."
---

<!-- Generated from harness/github-copilot/prompts/dotnet-best-practices.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /dotnet-best-practices

## Objective

Apply .NET and C# best practices to selected code so public APIs are documented, architecture is consistent, dependencies are injectable and testable, resources are localized, asynchronous work is correct, and configuration, logging, performance, security, AI integration, and code quality match the solution conventions.

## When to Invoke

Use this prompt when reviewing, refactoring, or extending C# solution code and you need a concrete best-practice checklist for ${selection} rather than a broad design-pattern-only review.

## Preconditions

- The target C# code is available in ${selection} or in a named file, project, or solution area.
- The repository's namespace structure, dependency injection style, test framework, resource files, and configuration conventions can be inspected or provided.
- Edits are permitted when the requested outcome is implementation; otherwise stay review-only.
- Existing project conventions take precedence unless they conflict with safe .NET and C# practice.

## Inputs the Team Must Provide

- `target` or selected code — the class, project, feature, or solution area to review or improve.
- Expected output mode — review notes, code edits, or both.
- Project conventions for namespaces such as `{Core|Console|App|Service}.{Feature}` and command handlers such as `CommandHandler<TOptions>`.
- Any required test command, resource-file convention, configuration source, or AI service integration detail.
- Ask the user for anything that is missing, especially when missing context would change edits.

## What I Will Do

- Inspect the selected code and preserve the repository's established architecture.
- Add or recommend XML documentation comments for public classes, interfaces, methods, and properties, including parameter and return descriptions.
- Apply primary constructor or constructor dependency injection, interface segregation, service lifetime guidance, and testable abstractions.
- Check ResourceManager localization, strongly typed configuration, async/await usage, structured logging, security, Semantic Kernel integration, and SOLID code quality.
- Validate or recommend MSTest, FluentAssertions, Moq, AAA pattern coverage, and null parameter validation tests.

## What I Will NOT Do

- Rewrite unrelated code or introduce a new architecture that conflicts with the solution's namespace and command-handler conventions.
- Replace established test, dependency injection, logging, localization, or configuration libraries without explicit approval.
- Hardcode secrets, concatenate database input into SQL, or bypass input validation and sanitization.
- Add superficial comments that repeat syntax instead of explaining public API behavior or non-obvious logic.
- Claim tests, builds, or validations passed unless the corresponding command ran or the limitation is reported.

## Output Format

Return the review or applied edits with this concrete structure:

```markdown
### .NET Best Practices Result

### Target
- `${selection}` or `<file-or-project>`

### Improvements Applied or Recommended
| Area | Finding | Action |
| --- | --- | --- |
| Documentation & Structure | Public API lacks XML docs | Add summaries, parameter descriptions, and return value descriptions |
| Design Patterns & Architecture | Handler does not follow `CommandHandler<TOptions>` | Align with the command-handler base class and `{Core|Console|App|Service}.{Feature}` namespace |
| Dependency Injection & Services | Dependency is newed directly | Use primary constructor injection and register the service lifetime |
| Resource Management & Localization | Message is hardcoded | Move to `LogMessages` or `ErrorMessages` and read with `_resourceManager.GetString("MessageKey")` |
| Async/Await Patterns | I/O method blocks synchronously | Return `Task` or `Task<T>` and use async/await |
| Testing Standards | Failure scenario missing | Add MSTest coverage with FluentAssertions, Moq, AAA, and null parameter validation |
| Configuration & Settings | Options are unvalidated | Bind `IConfiguration` to strongly typed classes with `Required` and `NotEmptyOrWhitespace` |
| Semantic Kernel & AI Integration | AI output is unstructured | Use `Microsoft.SemanticKernel` with ChatCompletion, Embedding, and structured output patterns |
| Error Handling & Logging | Log message uses concatenation | Use `Microsoft.Extensions.Logging` structured scopes and parameterized messages |
| Performance & Security | Query accepts raw input | Use parameterized queries, validation, and sanitization |
| Code Quality | Method has mixed responsibilities | Apply SOLID, reduce duplication, and extract focused utilities |

### Validation
- Command: `<existing test/build command or not run>`
- Result: `<passed, failed, or not run with reason>`
```

## Definition of Done

- [ ] Public APIs are documented with XML comments where required.
- [ ] Namespace, command-handler, factory, interface, and dependency injection patterns match the solution.
- [ ] Resources, configuration, logging, async, disposal, security, and Semantic Kernel practices are checked.
- [ ] Tests cover success, failure, and null parameter validation where changes require it.
- [ ] Validation evidence or a clear not-run reason is reported.

## Prompt Body

Follow these steps in order. Keep changes precise and solution-specific.

**Step 1 — Establish the target and conventions.** Identify the code in ${selection} or the requested target. Inspect namespace conventions such as `{Core|Console|App|Service}.{Feature}`, command-handler bases such as `CommandHandler<TOptions>`, service registration patterns, resource files, and test framework choices before recommending changes.

**Step 2 — Review documentation and structure.** Ensure public classes, interfaces, methods, and properties have XML documentation comments. Include parameter descriptions and return value descriptions. Keep names meaningful and aligned to domain concepts.

**Step 3 — Apply design and dependency patterns.** Prefer primary constructor syntax for dependency injection, for example `public class MyClass(IDependency dependency)`. Use clear `I`-prefixed interfaces, Factory pattern support for complex object creation, service interfaces for testability, `ArgumentNullException` null checks where the project style requires them, and appropriate Singleton, Scoped, or Transient registrations through `Microsoft.Extensions.DependencyInjection`.

**Step 4 — Check resources and configuration.** Use `ResourceManager` for localized messages and error strings. Keep `LogMessages` and `ErrorMessages` resource files separate. Access resources through `_resourceManager.GetString("MessageKey")`. Bind settings from `appsettings.json` through `IConfiguration` into strongly typed configuration classes (strongly-typed configuration classes) with data annotations such as `Required` and `NotEmptyOrWhitespace`.

**Step 5 — Correct async, error handling, and logging.** Use async/await for I/O operations and long-running tasks. Return `Task` or `Task<T>` from async methods. Use `ConfigureAwait(false)` where appropriate for the project type. Handle async exceptions correctly. Use `Microsoft.Extensions.Logging`, scoped logging, meaningful context, specific exceptions with descriptive messages, and try-catch blocks only for expected failure scenarios.

**Step 6 — Review Semantic Kernel, performance, and security.** Use `Microsoft.SemanticKernel` for AI operations when the code integrates AI. Check kernel configuration, service registration, ChatCompletion and Embedding model settings, and structured output patterns. Use C# 12+ features and .NET 8 optimizations where applicable. Validate and sanitize input, use parameterized queries for database operations, and follow secure coding practices for AI/ML operations.

**Step 7 — Review tests and code quality.** Use MSTest with FluentAssertions and Moq when those are the project standards. Follow AAA (Arrange, Act, Assert). Test success and failure scenarios, including null parameter validation. Check SOLID principles, duplication, cohesive methods, proper disposal patterns, base classes, and utilities.

**Step 8 — Deliver and validate.** Apply approved edits or return prioritized findings. Run the smallest existing relevant test or build command when tools permit. Report changed paths, practices applied, validation evidence, and unresolved risks.

## Invocation Example

```
/dotnet-best-practices target=src/App.Ordering selection=<selected C# code>
```
