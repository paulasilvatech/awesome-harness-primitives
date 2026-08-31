---
name: "translate-natural-to-java"
description: "Translates a Natural program into idiomatic Java 21 + Spring Boot 3.3 while preserving business semantics."
argument-hint: "file=01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSN context=<context> package=<java.package>"
agent: "builder"
tools: ["read", "search", "edit", "execute"]
---
# /translate-natural-to-java

## Objective

Translate a Natural program into idiomatic Java 21 + Spring Boot 3.3 while preserving business semantics (not syntax). The output is compilable Java with Javadoc that traces back to the Natural source.

## When to Invoke

At the beginning of Stage 3, when the team starts implementing bounded contexts from the Stage 2 design.

## Preconditions

- `specs/<NNN>-<feature>/plan.md` exists with the required package structure
- `specs/<NNN>-<feature>/spec.md` exists with EARS requirements
- The bounded context and target package are known
- The Natural source file is accessible in `01-archaeology/legacy-sifap/`

## Inputs the Team Must Provide

- The path to the Natural program file (for example, `01-archaeology/legacy-sifap/natural-programs/PGXXXXXX.NSN`)
- The bounded context and target Java package
- Any related EARS requirements (REQ-IDs)

## What I Will Do

- Read the Natural program block by block
- Identify the business purpose of each procedural block
- Translate it into idiomatic Java 21 (records for DTOs, sealed interfaces, constructor injection)
- Generate Javadoc linking to the Natural source file and line range
- Flag orphan logic (code without a corresponding EARS requirement) for a team decision
- Create unit test stubs for each translated method

## What I Will NOT Do

- Mirror Natural syntax line by line in Java ("JOBOL" — Java that looks like Natural)
- Silently merge multiple Natural concepts into one Java class
- Invent business meaning for unclear code — orphan logic is flagged, not interpreted
- Skip reading the EARS requirements first — every translated block must map to a REQ-ID

## Output Format

Java files under the appropriate `src/main/java/` package, plus test stubs under `src/test/java/`. Each file includes Javadoc citing the Natural source.

## Definition of Done

- [ ] Java files compile without errors
- [ ] Every public method has Javadoc citing the Natural source file and line range
- [ ] Every business rule from the relevant EARS requirements has a corresponding method
- [ ] Orphan logic (code without a REQ) is documented with `// ORPHAN: [file:line] - Team decision required`
- [ ] Unit test stubs exist for every public method
- [ ] No line-by-line Natural port — the translation uses Java 21 idioms

## Prompt Body

You are the `@builder`. The team selected a Natural program to translate into Java.

**Step 1 — Read the EARS requirements first.**
Before touching the Natural file, read `specs/<NNN>-<feature>/spec.md` and
identify all requirements relevant to this program. List them. These
requirements define what the Java code *must* do.

**Step 2 — Read the Natural program.**
Open the specified file. Read the `DEFINE DATA` section to understand the data model. Then read the main logic block by block:

- For each `IF...THEN...ELSE...END-IF`, identify the business decision
- For each `READ` or `FIND`, identify the data access pattern
- For each `CALLNAT`, note the dependency (but do not translate the target — that is a separate invocation)
- For each `PERFORM`, identify the internal subroutine

**Step 3 — Map blocks to requirements.**
For each identified block, find the EARS requirement it implements. If a block has no corresponding requirement, mark it as orphan logic:

```java
// ORPHAN: [natural-file.NSN:L42-58] - No matching REQ. Team decision required: keep, modify, or remove?
```

Ask the team what to do with orphan logic before proceeding.

**Step 4 — Translate into Java.**
For each block with a corresponding requirement, write the Java equivalent:

- `DEFINE DATA LOCAL` variables → method parameters or local variables with appropriate types
- `IF...THEN...ELSE` → Java `if/else` expressions or `switch` (Java 21 pattern matching when appropriate)
- `READ LOGICAL BY` → Spring Data JPA `findBy*` method
- `FIND WITH` → JPA `@Query` with named parameters
- `CALLNAT` → service method call (inject the dependency)
- Packed decimal calculations → `BigDecimal` with explicit scale and rounding mode
- String operations → Java `String` methods, noting charset differences

Use Java 21 idioms:

- Records for DTOs and value objects
- Sealed interfaces for discriminated unions when required by the domain
- `Optional` for nullable returns
- Constructor injection (no field-level `@Autowired`)
- `@Valid` for input validation in the controller layer
- `@Transactional` only on service methods, never repositories

**Step 5 — Generate Javadoc.**
Every public method receives Javadoc that includes:

```java
/**
 * [Business description].
 *
 * <p>Translated from: {@code [natural-file.NSN#L42-L58]}</p>
 * <p>Implements: REQ-NNN</p>
 */
```

**Step 6 — Create test stubs.**
For each public method, generate a test stub in `src/test/java/`:

```java
@Test
void should_[expected]_when_[condition]() {
    // Arrange: [describe the setup based on the Natural input parameters]
    // Act: [call the translated method]
    // Assert: [verify against the EARS acceptance criteria]
    fail("TODO: implement — see REQ-NNN acceptance criteria");
}
```

**Step 7 — Verify compilation.**
Try to compile the generated files. Report and fix any compilation errors.

If a Natural construct has no clean Java idiom, present two alternatives to the team and let them choose. Do not choose silently.

## Invocation Example

```
/translate-natural-to-java file=01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSN context=<context> package=<java.package>
```
