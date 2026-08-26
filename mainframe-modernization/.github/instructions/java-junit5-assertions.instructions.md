---
description: "Use when writing or reviewing JUnit 5 (Jupiter) assertions in backend Java tests — expected-value ordering, lazy Supplier messages, assertAll grouping, assertThrows and assertThrowsExactly, timeouts, and assertInstanceOf."
applyTo: "**/*Test.java,**/*IT.java,**/*Steps.java,**/*StepDefs.java"
---

# JUnit 5 Assertions — Jupiter Assertion Conventions

This file activates on backend Java test files (`*Test.java`, `*IT.java`, `*Steps.java`, `*StepDefs.java`). It teaches how to use JUnit Jupiter's built-in `org.junit.jupiter.api.Assertions` correctly and precisely on Java 21: expected-value ordering, lazy failure messages, grouped assertions, exception and type checks, and timeouts. It teaches you how to assert — it does not decide your test strategy, slice choice, mocking policy, or coverage targets. Test structure and the pyramid live in the [`java-junit`](../skills/java-junit/SKILL.md) skill, Spring slice and integration testing in the [`spring-boot-testing`](../skills/spring-boot-testing/SKILL.md) skill, and traceability plus coverage in [`tests.instructions.md`](tests.instructions.md).

> [!NOTE]
> These are Jupiter's built-in `Assertions`. For fluent chains and rich object or collection checks, the kit prefers AssertJ (`assertThat(...)`), as used in [`tests.instructions.md`](tests.instructions.md) and the [`spring-boot-testing`](../skills/spring-boot-testing/SKILL.md) skill. Reach for the Jupiter assertions below for grouped, exception, timeout, and exact-type checks, and for simple equality.

## Static Imports

Import each assertion statically so test methods read as intent, not boilerplate. Prefer explicit imports over the wildcard unless your module already standardizes on it.

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertAll;

assertEquals(expected, actual);
```

Always import from `org.junit.jupiter.api.Assertions`. Never mix in `org.junit.Assert` (JUnit 4) — the argument orders differ and the two APIs are not interchangeable.

## Expected Value First

`expected` is always the **first** argument and `actual` the **second**, so the failure log reads "expected X but was Y" correctly.

```java
// Avoid — swapped; the failure message is misleading
assertEquals(resourceService.count(), 2);

// Prefer
assertEquals(2, resourceService.count());

// Unavoidable floating point (never money — that is BigDecimal): pass a delta
assertEquals(0.3, 0.1 + 0.2, 1e-9);
```

> [!WARNING]
> `assertEquals` on `BigDecimal` uses `equals`, which is scale-sensitive: `new BigDecimal("10.0")` is **not** equal to `new BigDecimal("10.00")`. For monetary values compare by value — `assertEquals(0, expected.compareTo(actual))` — or use AssertJ's `isEqualByComparingTo`.

## Failure Messages: Supplier vs String

Pass the message as a `Supplier<String>` when building it is expensive, so the string is only constructed on failure. A constant literal can stay a plain `String`.

```java
// Avoid — the formatted message is built even when the assertion passes
assertEquals(expected, actual, "expected %s but got %s".formatted(expected, actual));

// Prefer — evaluated lazily, only on failure
assertEquals(expected, actual,
    () -> "expected %s but got %s".formatted(expected, actual));

// Fine — a constant literal has zero overhead
assertTrue(account.isActive(), "account must be active");
```

## Grouping with assertAll

Use `assertAll` to check several properties of one result; every assertion runs even when an earlier one fails, so you see all mismatches at once.

```java
record PaymentView(String beneficiary, BigDecimal amount, PaymentStatus status) {}

@Test
void should_map_all_fields_when_building_view() { // REQ-042
    PaymentView view = mapper.toView(payment);
    assertAll("payment view",
        () -> assertEquals("ACME LTDA", view.beneficiary()),
        () -> assertEquals(0, new BigDecimal("1500.00").compareTo(view.amount())),
        () -> assertEquals(PaymentStatus.APPROVED, view.status())
    );
}
```

Do not hand-roll a sequence of bare assertions to check one object — the first failure hides the rest.

## Exceptions: assertThrows vs assertThrowsExactly

`assertThrows` returns the thrown exception so you can assert on it, and it accepts subtypes of the expected class. Use `assertThrowsExactly` (JUnit 5.8+) when the exact class is part of the contract.

```java
@Test
void should_reject_duplicate_label_when_it_exists() { // REQ-021
    var request = new CreateResourceRequest("alpha", new BigDecimal("5.00"));
    ResourceConflictException ex = assertThrows(
        ResourceConflictException.class,
        () -> resourceService.create(request));
    assertEquals("alpha", ex.conflictingLabel());
}

// Exact type required — a subclass must NOT satisfy this assertion
assertThrowsExactly(IllegalArgumentException.class, () -> ResourceLabel.of(""));
```

## assertDoesNotThrow

Use `assertDoesNotThrow` only when the absence of an exception is the contract under test; it returns the value for further assertions.

```java
BigDecimal total = assertDoesNotThrow(() -> invoiceService.total(batch));
assertEquals(0, new BigDecimal("2500.00").compareTo(total));
```

## Timeouts

Use `assertTimeout` to check a duration without interrupting the work. Use `assertTimeoutPreemptively` only when a hard abort is required.

```java
assertTimeout(Duration.ofSeconds(1), () -> reportService.generate(batch));

assertTimeoutPreemptively(Duration.ofMillis(500), () -> validator.check(payload));
```

> [!WARNING]
> `assertTimeoutPreemptively` runs the code on a **separate thread**, so `ThreadLocal` state does not propagate — a `@Transactional` test's bound `EntityManager` and any security context are absent inside it. Never wrap a transactional persistence call in it.

## Type Checks: assertInstanceOf

Prefer `assertInstanceOf` (JUnit 5.8+) over `assertTrue(x instanceof T)`; it fails with a useful message and returns the value already cast — a natural fit for the kit's sealed result types.

```java
sealed interface PaymentResult permits Approved, Rejected {}

Approved approved = assertInstanceOf(Approved.class, paymentService.process(request));
assertEquals(42L, approved.paymentId());
```

## Collections and Arrays

Use the dedicated assertions so failures show an element-by-element diff instead of an opaque `false`.

```java
assertIterableEquals(List.of("alpha", "beta"), resourceService.labels()); // ordered deep diff
assertArrayEquals(expectedBytes, actualBytes);
```

## Conventions

| Rule | Rationale |
|---|---|
| `expected` first, `actual` second in `assertEquals` | The failure log reads "expected X but was Y" correctly |
| Compare `BigDecimal` by value, not `equals` | `equals` is scale-sensitive and silently fails on money |
| Wrap expensive failure messages in a `Supplier<String>` | The message is only built when the assertion fails |
| Group related checks with `assertAll` | Every property is reported, not just the first mismatch |
| `assertThrows` for a hierarchy, `assertThrowsExactly` for a precise class | Matches how strictly the exception type is part of the contract |
| `assertInstanceOf` over `assertTrue(... instanceof ...)` | Returns the cast value and fails with a useful message |
| Import from `org.junit.jupiter.api.Assertions` only | JUnit 4 `org.junit.Assert` has different argument orders |

## Do / Do Not

| Do | Do not |
|---|---|
| Put `expected` before `actual` | Swap them and get misleading failure logs |
| Compare money with `compareTo` or `isEqualByComparingTo` | Assert `BigDecimal` equality with scale-sensitive `equals` |
| Use `assertEquals(2, result)` for values | Use `assertTrue(result == 2)` and lose both values in the log |
| Assert the value when you can | Settle for `assertNotNull` when a real check is possible |
| Use a `Supplier` for costly messages | Build a formatted message that runs on every pass |
| Keep `assertTimeoutPreemptively` off transactional code | Wrap a `@Transactional` persistence call and lose the `EntityManager` |
| Let assertions fail loudly | Catch `AssertionError` to hide a failure |

## Checklist Before Opening a PR

- [ ] Every `assertEquals` lists `expected` first and `actual` second
- [ ] `BigDecimal` and other monetary values are compared by value, not scale-sensitive `equals`
- [ ] Multi-property checks use `assertAll`; expensive messages use a `Supplier<String>`
- [ ] Exception tests pick `assertThrows` or `assertThrowsExactly` deliberately and assert on the returned exception
- [ ] `assertTimeoutPreemptively` is not wrapped around transactional or `ThreadLocal`-bound code
- [ ] Imports are Jupiter-only; no `org.junit.Assert` (JUnit 4) is mixed in
- [ ] Requirement-driven tests keep their inline `// REQ-NNN` comment (see [`tests.instructions.md`](tests.instructions.md))
