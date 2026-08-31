---
name: "generate-equivalence-tests"
description: "Generates JUnit tests that validate whether the modern Java implementation produces the same outputs as the original Natural program for the same inputs."
argument-hint: "class=<java.package>.<Service> method=<method>"
agent: "builder"
tools: ["read", "search", "edit", "execute"]
---
# /generate-equivalence-tests

## Objective

Generate parameterized JUnit 5 tests that verify whether a translated Java method produces business results equivalent to the original Natural program for the same inputs.

## When to Invoke

After a Natural program has been translated to Java (`/translate-natural-to-java`), to verify equivalence.

## Preconditions

- The Java translation exists and compiles
- The original Natural source is accessible in `01-archaeology/legacy-sifap/`
- The Javadoc in the translated code references the Natural source file and lines

## Inputs the Team Must Provide

- The Java class and method to test
- The path to the original Natural file (usually found in the method's Javadoc)
- Any test data or edge cases known from the team's Stage 1 analysis

## What I Will Do

- Read the original Natural program to identify input parameters and expected outputs
- Identify every branch (IF/ELSE, DECIDE) to determine test cases
- Generate parameterized JUnit 5 tests covering the happy path, branches, boundaries, and nulls
- Run the tests and report results
- List any uncovered branch

## What I Will NOT Do

- Mark a method as "equivalent" without at least one test per identified branch
- Skip boundary conditions for numeric inputs
- Fabricate expected values — every expected value must be derivable from the Natural code logic
- Ignore error paths — rejection and error branches also receive tests

## Output Format

Test file at `src/test/java/.../[ClassName]EquivalenceTest.java`

## Definition of Done

- [ ] At least one test per branch identified in the Natural program
- [ ] Parameterized tests cover: happy path, each branch, boundary values, and null/empty inputs
- [ ] Tests compile and run
- [ ] Pass/fail results are reported with branch coverage
- [ ] Failing tests identify which branch diverged from the Natural logic

## Prompt Body

You are the `@builder`. The team translated a Natural program to Java and needs equivalence tests.

**Step 1 — Locate the Natural source.**
Read the Javadoc on the specified Java method. Extract the Natural file reference and line range. Open that Natural file.

**Step 2 — Identify branches in the Natural code.**
For the referenced line range, list every conditional branch:

- Each `IF...THEN...ELSE` creates 2+ paths
- Each `DECIDE ON` value creates N paths
- Each `AT BREAK` creates a control-break path

For each branch, note:

- The condition (what triggers this path)
- The expected action/output
- The input values that would trigger this path (derived from the condition)

**Step 3 — Derive test cases.**
For each branch, create at least one test case:

```java
@ParameterizedTest
@CsvSource({
    "input1, input2, expectedOutput",  // Branch 1: [description]
    "input3, input4, expectedOutput",  // Branch 2: [description]
})
void should_produce_equivalent_output(Type param1, Type param2, Type expected) {
    // Arrange
    var service = new ServiceUnderTest(/* dependencies */);
    // Act
    var result = service.methodUnderTest(param1, param2);
    // Assert
    assertThat(result).isEqualTo(expected);
}
```

Add more tests for:

- **Boundary values**: min/max for numeric fields, empty strings, and single-character strings
- **Null/empty inputs**: what happens when optional parameters are null?
- **Packed decimal precision**: verify that `BigDecimal` calculations match Natural packed decimal arithmetic

**Step 4 — Handle edge cases.**
If the Natural code has a branch that depends on data state (for example, "if record exists"), generate separate tests with mocked repository responses:

- Record exists → expected behavior
- Record does not exist → expected error/alternative

**Step 5 — Run the tests.**
Run the test suite using the `runTests` tool. Report:

- Total tests: N
- Passed: N
- Failed: N (with details for each failure)
- Branch coverage estimate (branches with tests / total identified branches)

**Step 6 — Document discovered branches.**
If any identified branch does not have a test (because of unclear logic or missing context), document it:

```java
@Test
@Disabled("MYSTERY: Branch at [nat-file:L73] — unclear condition; cannot derive expected output")
void should_handle_mystery_branch() {
    fail("Needs team investigation — see MYS-NNN");
}
```

## Invocation Example

```
/generate-equivalence-tests class=<java.package>.<Service> method=<method>
```
