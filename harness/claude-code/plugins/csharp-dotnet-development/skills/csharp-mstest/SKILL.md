---
name: csharp-mstest
description: >-
  Apply modern MSTest 3.x/4.x testing practices for C# projects. Use when asked to write or review
  MSTest unit tests, choose assertion APIs, convert ExpectedException tests, design data-driven
  tests, use TestContext, configure lifecycle hooks, add categories or work items, or run dotnet
  test for MSTest.
---

<!-- Generated from harness/github-copilot/plugins/csharp-dotnet-development/skills/csharp-mstest/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# C# MSTest

Write and review C# unit tests using MSTest 3.x/4.x conventions: separate test projects, sealed test classes, constructor-based setup, modern `Assert` APIs, type-safe data-driven tests, and `dotnet test` validation.

## When to invoke

- "Write MSTest unit tests for this C# class."
- "Review these MSTest 3.x/4.x tests for best practices."
- "Convert ExpectedException to Assert.Throws."
- "Add data-driven MSTest cases."
- "Use TestContext output, cancellation, or result files."

## Prerequisites and context

- Use an existing C# test project when present; otherwise prefer a separate `[ProjectName].Tests` project.
- Reference MSTest 3.x+ or 4.x NuGet packages and analyzers; consider `MSTest.Sdk` for simplified setup.
- Run tests with `dotnet test`; do not introduce another runner unless the repository already uses it.

## Test structure

| Area | Rule |
| --- | --- |
| Class | Add `[TestClass]`; seal test classes by default for performance and design clarity. |
| Method | Add `[TestMethod]`; prefer it over `[DataTestMethod]` for modern data rows. |
| Layout | Follow Arrange-Act-Assert and name tests `MethodName_Scenario_ExpectedBehavior`. |
| Lifecycle | Prefer constructors over `[TestInitialize]` so dependencies can be `readonly`; use `[TestInitialize]` only for async setup. |
| Cleanup | Use `[TestCleanup]` for cleanup that must run even when a test fails; implement `DisposeAsync` or `Dispose` for disposable resources. |
| Organization | Group by feature or component; use `[TestCategory("Category")]`, `[TestProperty("Name", "Value")]`, `[TestProperty("Bug", "12345")]`, and `[Priority(1)]` when reports or filters need metadata. |
| Analyzer | Enable relevant MSTest analyzers such as `MSTEST0020` for constructor preference. |

Execution order is `[AssemblyInitialize]`, `[ClassInitialize]`, constructor, `TestContext` property set, `[TestInitialize]`, test method, `[TestCleanup]`, `DisposeAsync`, `Dispose`, `[ClassCleanup]`, then `[AssemblyCleanup]`.

## Assertion selection

| Need | Preferred API | Avoid or note |
| --- | --- | --- |
| Equality | `Assert.AreEqual(expected, actual)`, `Assert.AreNotEqual`, `Assert.AreSame`, `Assert.AreNotSame` | Do not reverse expected and actual. |
| Null and boolean | `Assert.IsNull`, `Assert.IsNotNull`, `Assert.IsTrue`, `Assert.IsFalse` | Use `Assert.Fail` or `Assert.Inconclusive` only when the test cannot proceed. |
| Exceptions | `Assert.Throws<TException>(() => Method())`, `Assert.ThrowsExactly<TException>`, `Assert.ThrowsAsync`, `Assert.ThrowsExactlyAsync` | Avoid `[ExpectedException]`; it hides which statement threw. |
| Collections | `Assert.Contains`, `Assert.DoesNotContain`, `Assert.ContainsSingle`, `Assert.HasCount`, `Assert.IsEmpty`, `Assert.IsNotEmpty` | Prefer these over LINQ `Single()` for clearer failures. |
| Strings | `Assert.Contains("expected", actual)`, `Assert.StartsWith`, `Assert.EndsWith`, `Assert.DoesNotStartWith`, `Assert.DoesNotEndWith`, `Assert.MatchesRegex`, `Assert.DoesNotMatchRegex` | Prefer `Assert.Contains("expected", actual)` over `StringAssert.Contains(actual, "expected")` when available. |
| Comparisons | `Assert.IsGreaterThan`, `Assert.IsGreaterThanOrEqualTo`, `Assert.IsLessThan`, `Assert.IsLessThanOrEqualTo`, `Assert.IsInRange`, `Assert.IsPositive`, `Assert.IsNegative` | Keep the boundary readable in the assertion call. |
| Types | MSTest 3.x: `Assert.IsInstanceOfType<MyClass>(obj, out var typed)`; MSTest 4.x: `var typed = Assert.IsInstanceOfType<MyClass>(obj)`; also `Assert.IsNotInstanceOfType<WrongType>` | Avoid hard casts that fail with unclear exceptions. |
| Expressions | MSTest 4.0+: `Assert.That(result.Count > 0)` | Use when expression capture improves the failure message. |
| Legacy classes | `StringAssert` and `CollectionAssert` still exist; `CollectionAssert.AreEqual`, `AreEquivalent`, `IsSubsetOf`, `AllItemsAreNotNull`, `AllItemsAreUnique`, and `AllItemsAreInstancesOfType` remain useful for older APIs. | Prefer `Assert` equivalents when they provide the same intent. |

`Fail/Inconclusive` cases should be rare and explicit. Legacy assertion names that appear in older suites include `StringAssert.StartsWith`, `StringAssert.EndsWith`, `StringAssert.Matches`, `StringAssert.DoesNotMatch`, `DoesNotMatch`, `CollectionAssert.Contains`, `CollectionAssert.DoesNotContain`, `CollectionAssert.AreNotEqual`, `CollectionAssert.AreEquivalent`, `CollectionAssert.AreNotEquivalent`, `AreNotEquivalent`, `CollectionAssert.IsSubsetOf`, `CollectionAssert.IsNotSubsetOf`, `IsNotSubsetOf`, `CollectionAssert.AllItemsAreInstancesOfType`, `CollectionAssert.AllItemsAreNotNull`, and `CollectionAssert.AllItemsAreUnique`.

## Data-driven tests

| Source | Use when | Notes |
| --- | --- | --- |
| `[DataRow(1, 2, 3)]` | Inline cases are small and obvious. | Supports `DisplayName`; MSTest 3.8+ supports `IgnoreMessage`. |
| `IEnumerable<(T1, T2, ...)>` / `ValueTuple` | New `DynamicData` with type safety. | Preferred in MSTest 3.7+. |
| `IEnumerable<Tuple<T1, T2, ...>>` | Type safety is needed on older code. | More verbose than ValueTuple. |
| `IEnumerable<TestDataRow>` or `IEnumerable<TestDataRow<(...)>>` | Cases need display names, categories, or metadata. | Keeps test metadata close to the data. |
| `IEnumerable<object[]>` and `object[]` | Maintaining legacy tests. | Least preferred because it has no compile-time checking and can fail at runtime. |

## TestContext and advanced features

| Feature | Rule |
| --- | --- |
| Property injection | Declare `public TestContext TestContext { get; set; }`; MSTest suppresses `CS8618`, so do not make it nullable and do not assign `= null!`. |
| Constructor injection | MSTest 3.6+ can inject `TestContext` into the constructor for immutability. |
| Static lifecycle | `[ClassInitialize]`, `[ClassCleanup]`, and `[AssemblyCleanup]` can receive `TestContext`; cleanup context is optional in MSTest 3.6+. |
| Cancellation | With `[Timeout]`, pass `TestContext.CancellationToken` to async APIs instead of `CancellationToken.None`. |
| Run properties | `TestContext.TestName`, `TestDisplayName`, `CurrentTestOutcome` (`Pass/Fail/InProgress`), `TestData` (available in `TestInitialize/Cleanup`), `TestException`, and `DeploymentDirectory` support diagnostics. |
| Output and files | Use `TestContext.WriteLine`, `TestContext.AddResultFile`, and `TestContext.Properties` for Store/retrieve data across methods. |
| Retry | MSTest 3.9+ supports `[Retry(3)]` for flaky tests. |
| Conditional execution | MSTest 3.10+ supports `[OSCondition(OperatingSystems.Windows)]`, Linux/MacOS combinations, `ConditionMode.Exclude`, `[CICondition]`, and `[CICondition(ConditionMode.Exclude)]`. |
| Parallelization | At assembly level use `[assembly: Parallelize(Workers = 4, Scope = ExecutionScope.MethodLevel)]`; opt out with `[DoNotParallelize]`. |
| Work items | Use `[WorkItem(12345)]` for Azure DevOps and `[GitHubWorkItem("https://github.com/owner/repo/issues/42")]` for GitHub issues; associations flow into test results for CI/CD traceability. |

Recognize common sample names when refactoring existing tests: `CalculatorTests`, `Calculator.Add`, `ArgumentException`, `InvalidOperationException`, `HttpRequestException`, `GetAsync`, `MyHandler`, `MyService`, `ServiceTests`, `InitAsync`, `WarmupAsync`, `MyTests`, `ClassInit`, `DynamicTest`, `TestDataWithMetadata`, `LegacyTestData`, `LongRunningTest`, `FlakyTest`, `WindowsOnlyTest`, `UnixOnlyTest`, `SkipOnWindowsTest`, `LocalOnlyTest`, `SequentialTests`, `DoSomething`, and `SharedKey`. Treat OS conditions using `OperatingSystems.Linux`, `OperatingSystems.MacOS`, and `ConditionMode.Include` as valid MSTest API examples. Fully qualified `TestContext` members include `TestContext.CurrentTestOutcome`, `TestContext.DeploymentDirectory`, `TestContext.TestData`, `TestContext.TestDisplayName`, and `TestContext.TestException`.

## Gotchas

- **Do not use `[ExpectedException]` for new tests**: `Assert.Throws` and `Assert.ThrowsExactly` localize the throwing statement and return the exception for message checks.
- **Do not assert with the wrong argument order**: `Assert.AreEqual(actual, expected)` produces misleading failures; use expected first.
- **Do not use LINQ `Single()` as an assertion**: `Assert.ContainsSingle` gives a test-focused failure message.
- **Do not ignore cancellation**: `[Timeout]` works best when async code observes `TestContext.CancellationToken`.
- **Do not over-mock**: use Moq or NSubstitute behind interfaces to isolate the unit, but keep behavior assertions meaningful.

## Output template

```markdown
## MSTest result — <project or class>

**Status:** tests added | tests reviewed | blocked
**Command:** `dotnet test <project-or-solution>`

| Area | Decision | Evidence |
| --- | --- | --- |
| Project setup | `<MSTest packages or existing test project>` | `<file path>` |
| Test structure | `<sealed class, TestMethod, AAA>` | `<test names>` |
| Assertions | `<modern Assert API used>` | `<assertions>` |
| Data | `<DataRow or DynamicData source>` | `<case count>` |
| TestContext | `<used or not needed>` | `<cancellation/output/files>` |

**Validation**
- `dotnet test`: pass | fail | not run (`<reason>`)
```

## Quality gate

- [ ] Tests live in or target a `[ProjectName].Tests`-style test project when applicable.
- [ ] Test classes use `[TestClass]`, are sealed by default, and test methods use `[TestMethod]`.
- [ ] Setup favors constructors and `readonly` fields; `[TestInitialize]` is reserved for async or framework-required setup.
- [ ] Assertions use modern `Assert` APIs where available, with expected values first.
- [ ] Exceptions use `Assert.Throws` or `Assert.ThrowsExactly`, not `[ExpectedException]`.
- [ ] Data-driven tests prefer `DataRow`, `ValueTuple`, or `TestDataRow` over new `IEnumerable<object[]>` sources.
- [ ] Long-running async tests observe `TestContext.CancellationToken` when `[Timeout]` is used.
- [ ] `dotnet test` was run, or the exact blocker is reported.

## References

- [MSTest TestContext documentation](https://learn.microsoft.com/dotnet/core/testing/unit-testing-mstest-writing-tests-testcontext)
- [Example GitHub work item URL](https://github.com/owner/repo/issues/42)
