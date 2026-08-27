---
name: csharp-nunit
description: >-
  Design, write, and review NUnit tests for .NET projects, including standard tests, data-driven
  tests, assertions, setup/teardown, categories, and isolation with mocks. Use this skill when the
  user asks for NUnit best practices, `dotnet test`, `[TestCase]`, `[TestCaseSource]`, or C# unit
  test structure.
---

<!-- Generated from harness/github-copilot/skills/csharp-nunit/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# C# NUnit testing

Write focused NUnit tests that follow Arrange-Act-Assert, use the NUnit constraint model, isolate units under test, and keep data-driven cases readable and deterministic.

## When to invoke

- "Show NUnit best practices for this class."
- "Write data-driven NUnit tests."
- "Convert this test to `[TestCaseSource]`."
- "How should I organize a .NET test project?"
- "Fix these NUnit assertions."

## Project setup and organization

| Concern | Rule |
| --- | --- |
| Test project | Use a separate project named `[ProjectName].Tests`. |
| Packages | Reference `Microsoft.NET.Test.Sdk`, `NUnit`, and `NUnit3TestAdapter`. |
| Test command | Run tests with `dotnet test`. |
| Class naming | Match production classes, such as `CalculatorTests` for `Calculator`. |
| Test naming | Use `MethodName_Scenario_ExpectedBehavior`. |
| Grouping | Group tests by feature or component; use `[Category("CategoryName")]` for suites. |

## Test structure and lifecycle

| NUnit feature | Use for | Caution |
| --- | --- | --- |
| `[TestFixture]` | Marking a test class when explicit fixture metadata helps. | Modern NUnit can discover many classes without it, but keep it when the project uses it consistently. |
| `[Test]` | A single focused test method. | Do not test multiple behaviors in one method. |
| `[SetUp]` / `[TearDown]` | Per-test setup and cleanup. | Avoid hidden assertions or expensive shared state; this is the per-test hook. |
| `[OneTimeSetUp]` / `[OneTimeTearDown]` | Per-class expensive setup and cleanup. | Do not mutate shared state across tests unless reset; this is the per-class hook. |
| `[SetUpFixture]` | Assembly-level setup and teardown. | Use sparingly; assembly-level fixtures can hide global coupling. |
| `[Order]` | Rarely, when an external workflow truly requires order. | Prefer independent tests that can run in any order. |
| `[Explicit]` | Tests that should not run automatically. | Explain why manual execution is required. |
| `[Ignore("Reason")]` | Temporary skip. | Include a reason and remove when fixed. |
| `[Author("DeveloperName")]` and `[Description]` | Metadata required by team conventions. | Do not use metadata instead of readable test names. |

## Data-driven tests

| Attribute | Use when | Example shape |
| --- | --- | --- |
| `[TestCase]` | Inline values are short and obvious. | `[TestCase(1, 2, 3)]` |
| `[TestCaseSource]` | Cases need objects, generated values, or descriptive names. | Static method/property returning cases. |
| `[Values]` | Simple value lists for one parameter. | Combine with `[Combinatorial]` or `[Pairwise]`. |
| `[ValueSource]` | Values come from a property, field, or method-based source. | Keep source deterministic. |
| `[Random]` | Numeric fuzzing where nondeterminism is acceptable. | Record failures and prefer bounded ranges. |
| `[Range]` | Sequential numeric inputs. | Use small ranges to keep tests fast. |
| `[Combinatorial]` | All parameter combinations matter. | Watch explosion in case count. |
| `[Pairwise]` | Broad interaction coverage with fewer cases. | Use when exhaustive combinations are unnecessary. |

## Assertions and isolation

| Need | Preferred NUnit pattern |
| --- | --- |
| General assertions | `Assert.That(actual, Is.EqualTo(expected))` using the constraint model. |
| Value equality | Use `Is.EqualTo` inside `Assert.That(actual, Is.EqualTo(expected))`. |
| Reference equality | Use `Is.SameAs` inside `Assert.That(actual, Is.SameAs(expected))`. |
| Collection contains | Use `Contains.Item` inside `Assert.That(items, Contains.Item(expected))` or `CollectionAssert` when project style uses it. |
| String-specific checks | `StringAssert` or equivalent constraints; keep string-specific assertions readable. |
| Exceptions | `Assert.Throws<T>` for sync code and `Assert.ThrowsAsync<T>` for async code. |
| Failure clarity | Add descriptive assertion messages only when the expression is not self-explanatory. |
| Mocking | Use Moq or NSubstitute through interfaces to isolate dependencies. |
| Complex setup | Prefer small factories or a DI container only when it makes dependencies clearer. |

## Gotchas

- **Do not hide behavior in `[SetUp]`**: setup should arrange shared fixtures, not perform the act being tested.
- **Do not overuse `[Order]`**: ordered tests usually indicate state leakage.
- **Do not use random data without bounds**: `[Random]` can make failures hard to reproduce if ranges and assumptions are unclear.
- **Do not assert too much**: each test should prove one behavior with the minimum assertions needed.

## Output template

```markdown
## NUnit test result

**Status:** ready | needs changes | blocked
**Target:** <class, method, or behavior>

| Test | Pattern | Assertion | Notes |
| --- | --- | --- | --- |
| `MethodName_Scenario_ExpectedBehavior` | `[Test]` or `[TestCase]` | `Assert.That(...)` | <setup/mock/data source> |

### Validation
- `dotnet test`: pass | fail | not run
```

## Quality gate

- [ ] Tests follow Arrange-Act-Assert and target one behavior each.
- [ ] Test names use `MethodName_Scenario_ExpectedBehavior` or the repository's established equivalent.
- [ ] Data-driven tests choose `[TestCase]`, `[TestCaseSource]`, `[Values]`, `[ValueSource]`, `[Random]`, `[Range]`, `[Combinatorial]`, or `[Pairwise]` intentionally.
- [ ] Assertions use `Assert.That` with constraints unless project style requires classic assertions such as `Assert.AreEqual`.
- [ ] Exception tests use `Assert.Throws<T>` or `Assert.ThrowsAsync<T>`.
- [ ] Tests are independent, idempotent, and runnable with `dotnet test`.
