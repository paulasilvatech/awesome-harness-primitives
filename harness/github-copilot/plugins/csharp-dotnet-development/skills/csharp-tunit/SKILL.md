---
name: csharp-tunit
description: >-
  Write, review, or migrate C# unit tests using TUnit. Use when the user asks for TUnit best practices, .NET test project setup, TUnit assertions, lifecycle hooks, data-driven tests, parallel execution, retries, categories, or xUnit-to-TUnit migration.
---

# C# TUnit testing

Write effective .NET tests with TUnit by using its async assertion model, lifecycle hooks, data sources, and parallel execution controls instead of copying xUnit or NUnit idioms.

## When to invoke

- "Write TUnit tests for this C# class."
- "What are TUnit best practices for data-driven tests?"
- "Migrate these xUnit tests to TUnit."
- "Use TUnit assertions and lifecycle hooks."
- "Why are my TUnit tests flaky in parallel?"

## Prerequisites and context

- Use a separate test project named `[ProjectName].Tests`.
- Reference `TUnit` and `TUnit.Assertions`.
- TUnit requires .NET 8.0 or higher.
- Run tests with the normal .NET SDK command: `dotnet test`.
- Match test class names to the class under test, for example `CalculatorTests` for `Calculator`.

## Test structure

| Concern | TUnit rule | Avoid |
| --- | --- | --- |
| Test marker | Use `[Test]` on test methods. | `[Fact]` and `[Theory]` from xUnit. |
| Class marker | No test class attribute is required. | Empty fixture attributes copied from NUnit/xUnit. |
| Test shape | Follow Arrange-Act-Assert. | Multiple behaviors in one method. |
| Name | Use `MethodName_Scenario_ExpectedBehavior`. | Vague names such as `Test1`. |
| Independence | Tests must be idempotent and runnable in any order. | Hidden dependence on previous test state. |
| Dependencies | Use `[DependsOn(nameof(OtherTest))]` only when dependence is intentional and documented. | Serializing tests to hide shared-state bugs. |

## Lifecycle hooks

| Scope | Setup | Teardown | Use for |
| --- | --- | --- | --- |
| Test session | `[Before(TestSession)]` | `[After(TestSession)]` | Process-wide one-time state. |
| Assembly | `[Before(Assembly)]` | `[After(Assembly)]` | Shared assembly context. |
| Class | `[Before(Class)]` | `[After(Class)]` | Expensive context shared by tests in a class. |
| Test | `[Before(Test)]` | `[After(Test)]` | Fresh per-test setup and cleanup. |

Prefer per-test setup unless the shared object is immutable or safely reset. Replace constructor/`IDisposable` setup from xUnit with `[Before(Test)]` and `[After(Test)]`.

## Assertions

All TUnit assertions are asynchronous and must be awaited.

| Intent | Assertion pattern |
| --- | --- |
| Value equality | `await Assert.That(value).IsEqualTo(expected)` |
| Reference equality | `await Assert.That(value).IsSameReferenceAs(expected)` |
| Boolean true/false | `await Assert.That(condition).IsTrue()` / `await Assert.That(condition).IsFalse()` |
| Collection contains | `await Assert.That(collection).Contains(item)` |
| Collection excludes | `await Assert.That(collection).DoesNotContain(item)` |
| Regex match | `await Assert.That(value).Matches(pattern)` |
| Sync exception | `await Assert.That(action).Throws<TException>()` |
| Async exception | `await Assert.That(asyncAction).ThrowsAsync<TException>()` |
| Combined assertion | `await Assert.That(value).IsNotNull().And.IsEqualTo(expected)` |
| Alternative assertion | `await Assert.That(value).IsEqualTo(1).Or.IsEqualTo(2)` |
| Tolerance | `await Assert.That(value).IsEqualTo(expected).Within(tolerance)` for `DateTime` and numeric values |

## Data-driven tests

Use `method-based` data with `[MethodData]` and `class-based` data with `[ClassData]`. Use `[DependsOn]` only as shorthand for `[DependsOn(nameof(OtherTest))]` in documentation.


| Source | Attribute | Use when |
| --- | --- | --- |
| Inline values | `[Arguments]` | A small table of literals belongs beside the test. |
| Several inline rows | Multiple `[Arguments]` attributes | The same behavior needs multiple inputs. |
| Method data | `[MethodData]` | Data needs construction or is shared. |
| Class data | `[ClassData]` | Data is large, reusable, or encapsulated. |
| Custom provider | `ITestDataSource` | Data comes from a custom generator or external source. |

Use meaningful parameter names. Keep the assertion focused on the behavior represented by each row, not on the mechanics of the data source.

## Parallelism and reliability

| Feature | Use | Warning |
| --- | --- | --- |
| Default parallelism | TUnit runs tests in parallel by default. | Shared mutable state causes flakiness. |
| `[NotInParallel]` | Disable parallel execution for a specific test. | Use sparingly; fix state isolation first. |
| `[ParallelLimit<T>]` | Control concurrency through a custom limit class. | Useful for scarce external resources. |
| `[Repeat(n)]` | Repeat a test multiple times. | Good for stress checks, not for hiding nondeterminism. |
| `[Retry(n)]` | Retry transient failures. | Do not mask deterministic bugs. |
| `[Timeout(milliseconds)]` | Bound slow or hanging tests. | Set realistic values to avoid CI-only failures. |
| `[Skip("reason")]` | Skip with a reason. | Do not leave unexplained skips. |

Tests in the same class run sequentially by default. Use `[Category("CategoryName")]`, `[DisplayName("Custom Test Name")]`, `TestContext`, and conditional attributes such as custom `[WindowsOnly]` to organize diagnostics and platform-specific coverage.

## Migration from xUnit

Migration inventory tokens: `Assert.Equal`, `Assert.True`, `Assert.Throws<T>`, `constructor/IDisposable`, `await Assert.That()`, `await Assert.That(value).IsTrue()`, `await Assert.That(value).IsFalse()`, `.And`, and `.Within(tolerance)`.


| xUnit | TUnit |
| --- | --- |
| `[Fact]` | `[Test]` |
| `[Theory]` | `[Test]` with data attributes |
| `[InlineData]` | `[Arguments]` |
| `[MemberData]` | `[MethodData]` |
| `Assert.Equal(expected, actual)` | `await Assert.That(actual).IsEqualTo(expected)` |
| `Assert.True(condition)` | `await Assert.That(condition).IsTrue()` |
| `Assert.Throws<T>(action)` | `await Assert.That(action).Throws<T>()` |
| Constructor / `IDisposable` | `[Before(Test)]` / `[After(Test)]` |
| `IClassFixture<T>` | `[Before(Class)]` / `[After(Class)]` |

TUnit's value is modern async assertions, refined lifecycle hooks, flexible data-driven testing, and useful execution controls. Do not migrate by only renaming attributes; rewrite tests to be isolated, awaited, and behavior-focused.

## Gotchas

- **Always await assertions**: omitting `await` can produce tests that pass without evaluating the assertion.
- **Do not use xUnit attributes**: `[Fact]`, `[Theory]`, `[InlineData]`, and `[MemberData]` are not TUnit test markers.
- **Default parallelism exposes shared state**: prefer fresh fixtures over `[NotInParallel]` unless serialization is genuinely required.
- **Retries are not correctness**: use `[Retry(n)]` only for known transient external dependencies.

## Output template

```markdown
## TUnit test plan - <subject>

**Status:** ready | implemented | blocked
**Project:** `<ProjectName>.Tests`
**Command:** `dotnet test`

| Test | Attributes | Behavior | Assertions |
| --- | --- | --- | --- |
| `MethodName_Scenario_ExpectedBehavior` | `[Test]` | <single behavior> | `await Assert.That(...).IsEqualTo(...)` |

### Migration notes
- <xUnit/NUnit API replaced, or "none">

### Validation
- `dotnet test`: pass | fail | not run (<reason>)
```

## Quality gate

- [ ] Test methods use `[Test]` and do not use xUnit or NUnit test markers.
- [ ] Every TUnit assertion is awaited.
- [ ] Tests follow Arrange-Act-Assert and cover one behavior each.
- [ ] Data-driven tests use `[Arguments]`, `[MethodData]`, `[ClassData]`, or `ITestDataSource` appropriately.
- [ ] Lifecycle hooks match the required scope and do not leak shared mutable state.
- [ ] Parallel execution, retries, skips, dependencies, and timeouts are justified when used.
- [ ] `dotnet test` is run for implemented tests or a concrete blocker is reported.
