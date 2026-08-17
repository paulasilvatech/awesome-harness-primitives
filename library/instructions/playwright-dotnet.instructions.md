---
applyTo: "**/*.cs"
description: "Enforces Playwright .NET test conventions for locators, assertions, structure, fixtures, accessibility snapshots, and execution. Use when writing C# end-to-end tests with Playwright."
---

# Playwright .NET Conventions — C# Browser Tests

These instructions apply to C# files that define Playwright .NET tests using xUnit, NUnit, or MSTest. They are authoritative for locator choice, web-first assertions, test class structure, setup conventions, accessibility snapshots, and execution practices in matched files; project-specific test infrastructure, base URLs, and CI settings win where they define stricter requirements.

## Test Quality Standards

| Area | Convention |
| --- | --- |
| Locators | Prefer user-facing, role-based locators such as `GetByRole`, `GetByLabel`, and `GetByText` for resilience and accessibility. |
| Steps | Use `await Test.StepAsync()` to group interactions and make reports readable. |
| Assertions | Use auto-retrying web-first assertions through `Expect()`, such as `await Expect(locator).ToHaveTextAsync()`. |
| Visibility | Avoid checking visibility unless the behavior under test is a visibility change. |
| Waiting | Rely on Playwright auto-waiting; avoid hard-coded waits and inflated default timeouts. |
| Clarity | Use descriptive test names, step titles, and comments only for complex logic or non-obvious interactions. |

## Test Structure and Framework Integration

Start each test file with the required Playwright using directives and the chosen framework package.

- Include `using Microsoft.Playwright;` and either `using Microsoft.Playwright.Xunit;`, `using Microsoft.Playwright.NUnit;`, or `using Microsoft.Playwright.MSTest;`.
- Use `using static Microsoft.Playwright.Assertions;` when calling `Expect()` directly.
- Inherit from `PageTest` for NUnit, xUnit, and MSTest packages when the built-in fixture is sufficient.
- Use `IClassFixture<PlaywrightFixture>` for xUnit when custom fixtures are required.
- Put shared setup in `[SetUp]` for NUnit, `[TestInitialize]` for MSTest, or constructor/fixture initialization for xUnit.
- Use `[Test]`, `[Fact]`, or `[TestMethod]` with C# method names such as `SearchForMovieByTitle`.

## File Organization

Store Playwright tests where the project expects test code.

| Concern | Convention |
| --- | --- |
| Location | Put test files under `Tests/` or a feature-organized test directory. |
| Naming | Name files `<FeatureOrPage>Tests.cs`, for example `LoginTests.cs`, `SearchTests.cs`, or `MovieSearchTests.cs`. |
| Scope | Keep one test class per major application feature or page. |
| Grouping | Group related tests for a feature in the same class so setup and intent remain clear. |

## Assertions and Accessibility

Use Playwright assertions that model user-observable behavior.

| Need | Assertion |
| --- | --- |
| Accessibility tree structure | `ToMatchAriaSnapshotAsync` |
| Element count | `ToHaveCountAsync` |
| Exact text | `ToHaveTextAsync` |
| Partial text | `ToContainTextAsync` |
| Navigation result | `ToHaveURLAsync` |

Use `ToMatchAriaSnapshotAsync` for meaningful component or page structure, not as a broad snapshot of unrelated UI. Keep snapshots focused enough that failures reveal a useful accessibility or structure change.

## Execution and Maintenance

Use `dotnet test` or the IDE test runner to execute tests. Debug failures by identifying root causes, then refine locators, assertions, or test logic and validate that tests pass consistently. Report test results with any discovered product issues, but do not turn the instruction into a step-by-step workflow in test files.

## Good / Bad Examples

The examples below illustrate role locators, steps, and a focused accessibility assertion.

**Good**

```csharp
using Microsoft.Playwright;
using Microsoft.Playwright.Xunit;
using static Microsoft.Playwright.Assertions;

namespace PlaywrightTests;

public class MovieSearchTests : PageTest
{
    public override async Task InitializeAsync()
    {
        await base.InitializeAsync();
        await Page.GotoAsync("https://debs-obrien.github.io/playwright-movies-app");
    }

    [Fact]
    public async Task SearchForMovieByTitle()
    {
        await Test.StepAsync("Activate and perform search", async () =>
        {
            await Page.GetByRole(AriaRole.Search).ClickAsync();
            var searchInput = Page.GetByRole(AriaRole.Textbox, new() { Name = "Search Input" });
            await searchInput.FillAsync("Garfield");
            await searchInput.PressAsync("Enter");
        });

        await Test.StepAsync("Verify search results", async () =>
        {
            await Expect(Page.GetByRole(AriaRole.Main)).ToMatchAriaSnapshotAsync(@"
                - main:
                  - heading ""Garfield"" [level=1]
                  - heading ""search results"" [level=2]
                  - list ""movies"":
                    - listitem ""movie"":
                      - link ""poster of The Garfield Movie The Garfield Movie rating"":
                        - /url: /playwright-movies-app/movie?id=tt5779228&page=1
                        - img ""poster of The Garfield Movie""
                        - heading ""The Garfield Movie"" [level=2]
            ");
        });
    }
}
```

Why: the test uses framework fixtures, role locators, `Test.StepAsync`, and a web-first accessibility assertion tied to the user flow.

**Bad**

```csharp
[Fact]
public async Task Test1()
{
    await Page.WaitForTimeoutAsync(5000);
    await Page.Locator("#search").FillAsync("Garfield");
    Assert.True(await Page.Locator(".result").IsVisibleAsync());
}
```

Why: the test relies on hard-coded waits, brittle selectors, weak naming, and a visibility check that does not assert the user expectation.

## Conventions

| Rule | Rationale |
| --- | --- |
| Prefer `GetByRole`, `GetByLabel`, `GetByText`, and other user-facing locators. | Tests become resilient and reveal accessibility regressions. |
| Wrap meaningful phases in `await Test.StepAsync()`. | Reports show which user action or assertion failed. |
| Use `Expect()` web-first assertions such as `ToHaveTextAsync`, `ToContainTextAsync`, `ToHaveCountAsync`, and `ToHaveURLAsync`. | Assertions auto-retry and avoid timing races. |
| Structure tests around `PageTest`, framework setup attributes, or `IClassFixture<PlaywrightFixture>`. | Browser lifecycle stays consistent with Playwright .NET packages. |
| Keep files in `Tests/` and name them `<FeatureOrPage>Tests.cs`. | Test discovery and code review stay predictable. |
| Use `ToMatchAriaSnapshotAsync` for focused UI structure checks. | Accessibility expectations remain explicit and reviewable. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use descriptive method names like `SearchForMovieByTitle`. | Use vague names such as `Test1`. |
| Let Playwright auto-wait and retry assertions. | Add `WaitForTimeoutAsync` or global timeout increases to hide races. |
| Assert text, counts, URLs, and ARIA structure. | Assert visibility as a substitute for meaningful behavior. |
| Group tests by feature or page. | Mix unrelated user flows in one large test class. |
| Comment only non-obvious interactions. | Narrate every click or assertion with redundant comments. |

## Checklist Before Opening a PR

- [ ] Test files import the required Playwright and framework namespaces.
- [ ] Test classes use `PageTest` or the documented custom fixture pattern.
- [ ] Locators are accessible, specific, and avoid strict mode violations.
- [ ] Tests use `Test.StepAsync` for meaningful phases and descriptive titles.
- [ ] Assertions are web-first and reflect user expectations.
- [ ] Tests avoid hard-coded waits and unnecessary timeout increases.
- [ ] Files are named and grouped by feature or page under `Tests/` or the project test layout.
- [ ] `dotnet test` or the IDE runner passes for the relevant tests.
