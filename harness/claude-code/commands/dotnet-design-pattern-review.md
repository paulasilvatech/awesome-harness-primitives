---
description: "Review selected C# and .NET code for design pattern usage and recommend improvements."
---

<!-- Generated from harness/github-copilot/prompts/dotnet-design-pattern-review.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /dotnet-design-pattern-review

## Objective

Review selected C# and .NET code for design pattern usage, architecture fit, SOLID compliance, maintainability, testability, security, documentation, and alignment with the solution's established .NET best practices without editing code.

## When to Invoke

Use this prompt when you need a read-only design-pattern review of ${selection} or a named C#/.NET component, especially for command handlers, factories, providers, repositories, resource management, or project architecture.

## Preconditions

- The C#/.NET code to review is provided in ${selection} or a named target.
- The solution's architecture, namespace conventions, and project boundaries can be inspected or described.
- The desired output is a review, not code modification.
- Any project-specific required patterns are known or can be inferred from nearby code.

## Inputs the Team Must Provide

- `target` or ${selection} — the code, class, project, or feature to review.
- Project context — expected namespace convention, project split, and required design patterns.
- Review depth — quick findings, full checklist, or prioritized remediation plan.
- Ask the user for anything that is missing when absence would change the recommendation.

## What I Will Do

- Identify required patterns: Command, Factory, Dependency Injection, Repository, Provider, and Resource.
- Check GoF patterns such as Command, Factory, Template Method, and Strategy where they are relevant.
- Review architecture, .NET best practices, SOLID principles, performance, maintainability, testability, security, documentation, code clarity, and clean code.
- Provide specific, actionable recommendations aligned with the project's architecture.
- Stay read-only and cite the selected code or target behind each finding.

## What I Will NOT Do

- Modify code, create files, or run broad refactors.
- Recommend patterns for their own sake when a simpler implementation is clearer.
- Ignore project conventions such as `{Core|Console|App|Service}.{Feature}` or the Core/Console separation.
- Claim a pattern is missing without explaining the impact and a concrete improvement.
- Replace specific findings with generic best-practice advice.

## Output Format

Return a read-only review in this structure:

```markdown
### .NET Design Pattern Review

### Target
- `${selection}` or `<file/class/project>`

### Findings
| Severity | Area | Evidence | Recommendation |
| --- | --- | --- | --- |
| High | Command Pattern | Handler does not derive from `CommandHandler<TOptions>` | Align with `ICommandHandler<TOptions>`, `CommandHandlerOptions`, and `SetupCommand(IHost host)` |
| Medium | Factory Pattern | Object creation is spread across callers | Centralize complex creation with service provider integration and disposal rules |
| Medium | Provider Pattern | External AI or database access lacks an abstraction | Introduce provider contracts with configuration handling |
| Low | Resource Pattern | Messages are hardcoded | Move messages to `LogMessages` and `ErrorMessages` .resx files through ResourceManager |

### Checklist Coverage
- Design Patterns: Command Handler, Factory, Provider, Repository
- Architecture: `{Core|Console|App|Service}.{Feature}`, Core/Console separation, modularity
- .NET Best Practices: primary constructors, async/await, Task returns, ResourceManager, structured logging, strongly typed configuration (strongly-typed configuration)
- GoF Patterns: Command, Factory, Template Method, Strategy
- SOLID Principles: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- Performance: ConfigureAwait(false), disposal, parallel processing opportunities
- Security: input validation, secure credential handling, parameterized queries, safe exceptions

### Recommended Next Steps
1. `<specific action>`
2. `<specific action>`
```

## Definition of Done

- [ ] Review is read-only and no code is modified.
- [ ] Required patterns and checklist categories are covered or explicitly marked not applicable.
- [ ] Findings are specific, actionable, and tied to evidence from the target.
- [ ] Recommendations align with the project's architecture and .NET best practices.
- [ ] Security, testability, documentation, and maintainability are addressed.

## Prompt Body

Follow these steps in order. Do not make changes to the code.

**Step 1 — Establish review scope.** Review the C#/.NET code in ${selection} or the requested target. Identify solution/project conventions and the expected architecture. Stay read-only.

**Step 2 — Check Required Design Patterns.** Review the Command Pattern: generic base classes `CommandHandler<TOptions>`, `ICommandHandler<TOptions>` interface, `CommandHandlerOptions` inheritance, and static `SetupCommand(IHost host)` methods. Review the Factory Pattern for complex object creation and service provider integration. Review Dependency Injection for primary constructor syntax, `ArgumentNullException` checks, interface abstractions, and service lifetimes. Review Repository Pattern for async data access interfaces and provider abstractions for connections. Review Provider Pattern for external service abstractions such as database and AI, clear contracts, and configuration handling. Review Resource Pattern for ResourceManager and separate .resx files such as `LogMessages` and `ErrorMessages`.

**Step 3 — Apply the review checklist.** Identify patterns used and missing beneficial patterns. Check whether Command Handler, Factory, Provider, and Repository patterns are correctly implemented. Review architecture for namespace conventions like `{Core|Console|App|Service}.{Feature}`, separation between Core/Console projects, modularity, and readability. Review .NET best practices: primary constructors, async/await with Task returns, ResourceManager usage, structured logging, and strongly typed configuration.

**Step 4 — Assess quality attributes.** Check GoF patterns: Command, Factory, Template Method, Strategy. Evaluate SOLID: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion. Review performance: async/await, resource disposal, `ConfigureAwait(false)`, and parallel processing opportunities. Review maintainability: separation of concerns, error handling, and configuration usage. Review testability: interfaces, mockable components, async testability, and AAA pattern compatibility. Review security: input validation, credentials, parameterized queries, and safe exception handling. Review documentation and clarity: XML docs, `parameter/return` descriptions, resource-file organization, meaningful names, clear intent, self-explanatory structure, consistent style, appropriate method/class size, minimal complexity, and duplication removal.

**Step 5 — Focus improvement areas.** Prioritize Command Handlers for validation in base class, consistent error handling, and resource management. Prioritize Factories for dependency configuration, service provider integration, and disposal patterns. Prioritize Providers for connection management, async patterns, exception handling, and logging. Prioritize Configuration for data annotations, validation attributes, and secure sensitive value handling. Prioritize AI/ML Integration for Semantic Kernel patterns, structured output handling, and model configuration.

**Step 6 — Report actionable recommendations.** Provide severity, area, evidence, and recommendation. Include specific next steps aligned with the project's architecture and .NET best practices.

## Invocation Example

```
/dotnet-design-pattern-review target=src/Core.Payments selection=<selected C# code>
```
