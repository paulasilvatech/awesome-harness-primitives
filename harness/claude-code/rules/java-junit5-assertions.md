---
paths:
  - "**/*Test.java"
  - "**/*IT.java"
  - "**/*Steps.java"
  - "**/*StepDefs.java"
---

<!-- Generated from harness/github-copilot/instructions/java-junit5-assertions.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces JUnit Jupiter assertion conventions for imports, expected/actual ordering, lazy messages, grouped assertions, exception checks, timeouts, type safety, and collection comparisons.

# JUnit 5 Assertion Conventions — Jupiter Test Accuracy

These instructions apply to Java test files that use JUnit Jupiter assertions, including unit, integration, Cucumber step, and step definition tests. They are authoritative for assertion style, imports, failure messages, grouping, exception testing, timeouts, type assertions, and collection comparisons; project-specific Java testing or BDD primitives win when they define stricter naming, fixtures, or runner configuration.

## Imports and Assertion Calls

Use static imports from `org.junit.jupiter.api.Assertions` so test methods focus on behavior. Prefer explicit static imports such as `assertEquals` and `assertTrue` unless the project standard allows wildcard imports. Do not mix legacy `org.junit.Assert` JUnit 4 imports into JUnit 5 tests.

## Equality, Truthiness, and Messages

Always pass expected value first and actual value second to `assertEquals(expected, actual)`. For floating point values, provide a delta such as `assertEquals(0.3, 0.1 + 0.2, 1e-9)`. Use purpose-built assertions instead of `assertTrue(result == 42)` or broad `assertNotNull(result)` when a concrete value can be checked.

Pass expensive failure messages as `Supplier<String>`, for example `() -> "Expected %s but got %s".formatted(expected, actual)`, so message construction runs only on failure. Constant string messages such as `"User account must be active"` are acceptable when they add diagnostic value.

## Grouped Assertions and Exceptions

Use `assertAll` to check multiple properties of the same result so every related failure is reported. Use `assertThrows` when subclasses are acceptable and capture the returned exception for message or property assertions. Use `assertThrowsExactly` when the precise implementation class is part of the API contract; this requires JUnit 5.8+. Use `assertDoesNotThrow` only when absence of an exception is the explicit contract and capture its return value for follow-up checks.

## Timeouts, Type Safety, Collections, and Arrays

Use `assertTimeout` to ensure work completes within a duration while allowing the code to finish. Use `assertTimeoutPreemptively` only when hard abortion is required; it runs in a separate thread and `ThreadLocal` state such as `@Transactional` does not propagate. Use `assertInstanceOf` (JUnit 5.8+) instead of `assertTrue(result instanceof SuccessResponse)` so the assertion returns a casted object. Use `assertIterableEquals` for ordered iterable comparison and `assertArrayEquals` for arrays to get deep comparison and informative diffs.

## Technical Vocabulary

Preserve these source terms when they apply to edits in this domain: `AssertionError` `CI/CD` `EXACTLY` `GOOD` `ONLY` `actual` `assertEquals(42, result)` `assertEquals(expected, result)` `assertNotNull` `element-by-element` `expected` `hard-abortion` `hard-aborts` `instanceof` `performance-critical`.

Use concrete exception examples such as `ArithmeticException` for division by zero and `IllegalArgumentException` for validation failures when those are the API contract.

## Good / Bad Examples

The examples below show accurate assertions with useful diagnostics.

**Good:**

```java
import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;

assertAll("person",
    () -> assertEquals("Jane", person.firstName()),
    () -> assertEquals("Doe", person.lastName()),
    () -> assertEquals(30, person.age())
);
```

Why: Related properties are grouped and all failures are reported with expected values first.

**Bad:**

```java
Assertions.assertTrue(person.age() == 30);
assertEquals(person.firstName(), "Jane");
```

Why: The first assertion hides the actual value and the second swaps expected and actual, producing misleading failure output.

## Conventions

| Rule | Rationale |
|---|---|
| Use explicit static imports from `org.junit.jupiter.api.Assertions` | Test bodies stay readable and use Jupiter APIs consistently |
| Put expected before actual in `assertEquals` | Failure logs correctly report expected and observed values |
| Use `Supplier<String>` for expensive messages | Passing tests avoid unnecessary formatting or object inspection |
| Use `assertAll` for one object's related properties | Tests report complete state differences instead of stopping early |
| Choose `assertThrows`, `assertThrowsExactly`, or `assertDoesNotThrow` based on the contract | Exception tests express hierarchy, exact type, or no-throw guarantees precisely |
| Prefer `assertTimeout` over `assertTimeoutPreemptively` | Preemptive timeouts can break `ThreadLocal` and transaction context |
| Use `assertInstanceOf`, `assertIterableEquals`, and `assertArrayEquals` | Type and collection diagnostics are clearer than generic truth assertions |

## Do / Do Not

| Do | Do not |
|---|---|
| Import `assertEquals` and other assertions statically | Call `Assertions.assertEquals` everywhere unless required by convention |
| Use `assertEquals(2, calculator.add(1, 1))` | Use `assertEquals(calculator.add(1, 1), 2)` |
| Use `assertEquals(expected, actual, () -> expensiveMessage())` | Build expensive messages before knowing the assertion failed |
| Use `assertThrowsExactly` for exact API contracts | Use `assertThrows` when subclasses would hide a contract change |
| Use `assertInstanceOf(SuccessResponse.class, result)` | Use `assertTrue(result instanceof SuccessResponse)` plus a manual cast |
| Use `assertIterableEquals` and `assertArrayEquals` | Compare collections through vague truthiness or string output |
| Keep JUnit 5 tests on Jupiter imports | Mix `org.junit.Assert` into Jupiter tests |

## Checklist Before Opening a PR

- [ ] Assertions import from `org.junit.jupiter.api.Assertions`, preferably as explicit static imports.
- [ ] Equality assertions pass expected first and actual second, with deltas for floating point.
- [ ] Failure messages are useful and expensive messages use `Supplier<String>`.
- [ ] Related object property checks use `assertAll` where multiple failures should be reported together.
- [ ] Exception tests verify type, exact type, message, or no-throw behavior according to the contract.
- [ ] Timeouts avoid `assertTimeoutPreemptively` unless hard abortion and separate-thread behavior are acceptable.
- [ ] Type, iterable, and array assertions use `assertInstanceOf`, `assertIterableEquals`, and `assertArrayEquals` where applicable.
