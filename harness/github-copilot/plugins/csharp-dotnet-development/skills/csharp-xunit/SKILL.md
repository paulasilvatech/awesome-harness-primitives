---
name: "csharp-xunit"
description: >-
  Apply xUnit best practices for C# unit tests, including test project setup, Fact and Theory
  structure, data-driven tests, assertions, fixtures, mocking, categorization, diagnostics, and
  dotnet test execution. Use when asked for xUnit guidance or to write .NET unit tests.
---

# C# xUnit testing

Guide C# test design by turning a class, behavior, or test request into focused xUnit tests that use idiomatic setup, data sources, assertions, isolation, and `dotnet test` validation.

## When to invoke

- "Write xUnit tests for this C# class."
- "Show xunit best practices for data-driven tests."
- "Convert these cases into `[Theory]` and `[InlineData]`."
- "How should I organize fixtures in xUnit?"

## Project setup

| Concern | Rule |
| --- | --- |
| Test project | Use a separate `[ProjectName].Tests` project. |
| Packages | Reference `Microsoft.NET.Test.Sdk`, `xunit`, and `xunit.runner.visualstudio`. |
| Test class names | Match the class under test, for example `CalculatorTests` for `Calculator`. |
| Command | Run tests with `dotnet test`; narrow with `--filter` for targeted validation. |
| Visibility | Prefer testing public behavior; use `InternalsVisibleTo` only when the project already exposes internals for tests. |

## Test structure

| Pattern | Use it for | Notes |
| --- | --- | --- |
| `[Fact]` | One fact-based scenario with no external data rows. | No class-level test attribute is required in xUnit, unlike `MSTest/NUnit`. |
| `[Theory]` | Same behavior over multiple inputs. | Pair with one data source attribute. |
| Arrange-Act-Assert | Every test body. | Keep setup, action, and assertions visually separable. |
| `MethodName_Scenario_ExpectedBehavior` | Test method naming. | Example: `Divide_ByZero_ThrowsDivideByZeroException`. |
| Constructor | Per-test setup. | xUnit creates a new test class instance for each test. |
| `IDisposable.Dispose()` | Per-test teardown. | Release files, handles, or mocks that require cleanup. |
| `IAsyncLifetime` | Async setup or teardown. | Use `InitializeAsync` and `DisposeAsync` instead of blocking on tasks. |

## Data-driven tests

| Source | Best use | Example shape |
| --- | --- | --- |
| `[InlineData]` | Small scalar cases that fit on one line. | `[InlineData(2, 3, 5)]` |
| `[MemberData]` | Generated, named, reusable, or method-based test data. | Static property or method returning `IEnumerable<object[]>`. |
| `[ClassData]` | Larger reusable or class-based datasets. | Class implements `IEnumerable<object[]>`. |
| Custom `DataAttribute` | Dynamic or domain-specific data creation. | Keep deterministic; avoid network calls and current time. |

Use meaningful parameter names. Keep the assertion intent identical across all rows; split into separate theories when rows prove different behaviors.

## Assertions and exceptions

| Need | Assertion |
| --- | --- |
| Value equality | `Assert.Equal(expected, actual)`; baseline form `Assert.Equal`. |
| Reference identity | `Assert.Same(expected, actual)`; baseline form `Assert.Same`. |
| Boolean | `Assert.True(condition)` or `Assert.False(condition)` with a clear message when helpful; baseline forms `Assert.True` and `Assert.False`. |
| Collections | `Assert.Contains`, `Assert.DoesNotContain`, `Assert.Collection`, or `Assert.All`. |
| Regex | `Assert.Matches` or `Assert.DoesNotMatch`. |
| Exceptions | `Assert.Throws<T>` or `await Assert.ThrowsAsync<T>`. |
| Readability | Use a fluent assertions library only if the project already uses one or accepts the dependency. |

## Fixtures, mocking, and organization

| Technique | Use when | Avoid |
| --- | --- | --- |
| `IClassFixture<T>` | Expensive context shared by tests in one class. | Storing mutable state that leaks between tests. |
| `ICollectionFixture<T>` | Shared context across multiple test classes. | Using it as a global singleton for unrelated tests. |
| Moq or NSubstitute | Isolate dependencies behind interfaces. | Mocking the class under test or framework primitives unnecessarily. |
| DI container | Complex object graphs already use dependency injection. | Rebuilding the production container when a direct constructor call is clearer. |
| `[Trait("Category", "CategoryName")]` | Filtering smoke, integration, or slow tests. | Encoding ordering dependencies as categories. |
| `ITestOutputHelper` | Diagnostics that should appear only on failure or in test output. | Replacing assertions with log inspection. |
| `Skip = "reason"` | Temporarily disabled tests with a specific reason in fact/theory attributes. | Silent or permanent skips. |

## Gotchas

- **xUnit creates a new test class instance per test**: constructor state is not shared; use fixtures for intentional sharing.
- **Do not depend on test order**: tests must be independent and idempotent even when run in parallel.
- **Avoid broad assertions**: one focused behavior with the minimum useful assertions is easier to diagnose than a scenario that checks everything.
- **Keep data rows readable**: complex object graphs in `[InlineData]` usually belong in `[MemberData]` or builders.

## Output template

```markdown
## xUnit test plan

**Target:** `<class or behavior>`
**Command:** `dotnet test <project-or-solution> --filter <optional-filter>`

| Test | Attribute | Data source | Behavior verified |
| --- | --- | --- | --- |
| `<MethodName_Scenario_ExpectedBehavior>` | `[Fact]` or `[Theory]` | `<none / InlineData / MemberData / ClassData>` | `<single behavior>` |

### Notes
- Fixtures: `<IClassFixture<T> / ICollectionFixture<T> / none>`
- Assertions: `<key Assert.* calls>`
- Isolation: `<mocks, fakes, or real collaborators>`
```

## Quality gate

- [ ] Tests use `[Fact]` for single cases and `[Theory]` with data attributes for data-driven cases.
- [ ] Each test follows Arrange-Act-Assert and verifies one behavior.
- [ ] Names follow `MethodName_Scenario_ExpectedBehavior` or the project's established equivalent.
- [ ] Shared setup uses constructor, `IDisposable.Dispose()`, `IClassFixture<T>`, or `ICollectionFixture<T>` appropriately.
- [ ] Assertions use the most specific `Assert.*` API and cover exception paths with `Assert.Throws<T>` or `Assert.ThrowsAsync<T>`.
- [ ] Tests are independent, idempotent, and runnable with `dotnet test`.
