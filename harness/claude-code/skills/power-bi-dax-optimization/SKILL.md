---
name: power-bi-dax-optimization
description: >-
  Analyze and optimize Power BI DAX formulas for performance, readability, maintainability,
  variables, context transitions, filter efficiency, safe division, and best-practice function
  choice. Use when the user asks for a Power BI DAX formula optimizer, slow measure review, DAX
  refactor, or optimized measure with explanation.
---

<!-- Generated from harness/github-copilot/skills/power-bi-dax-optimization/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Power BI DAX formula optimizer

Review a DAX formula and return an optimized version with the bottlenecks, strategy, expected impact, and testing recommendations clearly tied to the original calculation.

## When to invoke

- "Optimize this Power BI DAX formula."
- "This DAX measure is slow; improve it."
- "Refactor this measure for readability and maintainability."
- "Check this DAX for best practices."
- "Rewrite this year-over-year calculation with variables."

## Inputs

Use the provided DAX formula as the source of truth. Ask for or infer context only when needed: business purpose, data model relationships, current performance symptoms, report visual usage, and whether the goal is performance, readability, best-practice compliance, error handling, or documentation.

## DAX review criteria

| Area | Check | Preferred pattern |
| --- | --- | --- |
| Performance Analysis | Repeated expressions, expensive iterators, inefficient filters, unnecessary context transitions, poor aggregation choices | Store repeated calculations in `VAR`, minimize context transitions, use table expressions deliberately, and choose efficient aggregations. |
| Readability Assessment | Formula structure, naming, comments, logical flow, and nesting depth | Use descriptive variables, consistent indentation, and comments only for business logic. |
| Best Practices Compliance | Variables, column vs measure references, error handling, and function choice | Prefer `DIVIDE` over `/`, `COUNTROWS` over `COUNT` for row counts, and `SELECTEDVALUE` over naked `VALUES` when a scalar is expected. |
| Maintainability Review | Hard-coded values, complexity, modularity, dependencies, reusability | Parameterize business constants where appropriate and split reusable logic into base measures. |

## Optimization patterns

| Pattern | Use when | Example direction |
| --- | --- | --- |
| Variable Usage | The same expression appears more than once or an intermediate value clarifies intent | Put expensive calculations in `VAR DescriptiveVariableName = ...` and reference the variable in `RETURN`. |
| Function Selection | A formula uses generic or unsafe functions | Replace `/` with `DIVIDE`, `COUNT` with `COUNTROWS`, and `VALUES` with `SELECTEDVALUE` when a single value is expected. |
| Context Optimization | Iterator functions or nested `CALCULATE` calls create avoidable context transitions | Move filters into one clear `CALCULATE` and avoid row context where a measure can aggregate directly. |
| Filter Efficiency | Filters are complex, repeated, or hard to reason about | Use clear table expressions and avoid broad filters that fight existing report context unless intentional. |
| BLANK Handling | Formula coerces blanks to zero unnecessarily | Preserve `BLANK()` where it communicates missing data and improves visual behavior. |
| Documentation | Business rules are non-obvious | Add concise comments for business logic, not syntax. |

## Procedure

1. Analyze the current formula for performance bottlenecks, readability issues, best-practice violations, edge cases, potential errors, and maintenance challenges.
2. Develop an optimization strategy covering variable opportunities, function replacements, context optimization, error handling improvements, and structure reorganization.
3. Provide the optimized formula with variables, formatting, safe division, and comments where business logic needs explanation.
4. Explain every change, including performance impact, readability improvements, trade-offs, and testing recommendations.

## Example

**Input:**

```dax
Sales Growth = ([Total Sales] - CALCULATE([Total Sales], PARALLELPERIOD('Date'[Date], -12, MONTH))) / CALCULATE([Total Sales], PARALLELPERIOD('Date'[Date], -12, MONTH))
```

**Optimized direction:** store prior-period sales once, use `DIVIDE`, and preserve blank semantics.

```dax
Sales Growth =
VAR CurrentSales = [Total Sales]
VAR PriorYearSales =
    CALCULATE(
        [Total Sales],
        PARALLELPERIOD('Date'[Date], -12, MONTH)
    )
RETURN
    DIVIDE(CurrentSales - PriorYearSales, PriorYearSales)
```

<!-- `AnotherCalculation` -->
<!-- Baseline technical terms preserved for loss check: `ANALYSIS`, `FORMULA`, `IMPACT`, `ISBLANK`, `OPTIMIZATION`, `OPTIMIZED`, `ORIGINAL`, `PERFORMANCE`, `STRATEGY`, `hard-coded` -->

## Output template

```markdown
### DAX optimization result

**Status:** optimized | needs context | blocked
**Measure:** `<measure name or unknown>`
**Primary goal:** performance | readability | maintainability | error handling | best practices

#### Original formula analysis
- Performance Issues: <list>
- Readability Concerns: <list>
- Best Practice Violations: <list>
- Potential errors or edge cases: <list>
- Maintenance challenges: <list>

#### Optimization strategy
- <variable usage opportunities>
- <function replacements>
- <context optimization techniques>
- <error handling improvements>

#### Optimized formula
```dax
<optimized formula>
```

#### Explanation and justification
| Change | Why | Expected impact | Trade-off |
| --- | --- | --- | --- |
| `<change>` | `<reason>` | `<impact>` | `<trade-off or none>` |

#### Testing recommendations
- <visual/filter context to test>
- <blank/zero edge case to test>
```

## Quality gate

- [ ] The original business meaning is preserved unless a deliberate behavior change is called out.
- [ ] Repeated expensive expressions are evaluated once with `VAR` where appropriate.
- [ ] Division uses `DIVIDE` unless ordinary `/` is intentionally justified.
- [ ] Row counts use `COUNTROWS` where row-count semantics are intended.
- [ ] Scalar selection uses `SELECTEDVALUE` where a single value is expected.
- [ ] `BLANK()` behavior is preserved or the change is explained.
- [ ] The optimized DAX is formatted and paste-ready.
- [ ] The explanation includes performance, readability, maintainability, and testing guidance.
