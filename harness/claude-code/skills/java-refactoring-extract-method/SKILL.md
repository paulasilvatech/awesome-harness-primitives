---
name: java-refactoring-extract-method
description: >-
  Refactor Java 17 methods with the Extract Method technique to improve readability, testability,
  maintainability, reusability, modularity, cohesion, low coupling, and consistency. Use when the
  user asks to identify long or complex Java methods, extract helper methods, preserve behavior,
  and return complete compilable refactored code.
---

<!-- Generated from harness/github-copilot/skills/java-refactoring-extract-method/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Java extract method refactoring

Analyze Java 17 methods for extractable responsibilities, then return behavior-preserving code that introduces focused helper methods with descriptive names while keeping the refactored method complete and compilable.

## When to invoke

- "Refactor this Java method using Extract Method."
- "This Java method is too long; split it into helper methods."
- "Improve readability and testability of this Java 17 method."
- "Extract methods from high-complexity Java code without changing behavior."

## Criteria

Refactor only methods that exceed at least one threshold, unless the user explicitly requests extraction for a smaller method.

| Metric | Threshold | What to inspect |
| --- | --- | --- |
| LOC | `> 15` | Executable method lines, excluding blank lines and comments. |
| NOM | `> 10` | Number of statements, including assignments, returns, calls, and control statements. |
| CC | `> 10` | Branching from `if`, `else if`, loops, `catch`, `case`, ternaries, and boolean operators. |

Prefer extraction candidates that are cohesive and nameable: validation, conversion, lookup, branch-specific construction, collection copying, error handling, or object creation.

## Extraction rules

| Rule | Apply it | Avoid |
| --- | --- | --- |
| Preserve behavior | Keep return values, exceptions, side effects, ordering, null semantics, and visibility constraints. | Changing a guard clause from `>` to `>=` or swallowing an exception. |
| Use descriptive helper names | Name helpers after intent, such as `bpartnerIdIfNotNull` or `newExpander`. | `handleStuff`, `processData`, or names that reveal implementation only. |
| Keep helpers focused | One helper should perform one coherent operation and accept only needed parameters. | Extracting a helper that still contains unrelated branches. |
| Control coupling | Pass values explicitly; use instance state only when the original method already depends on it. | Introducing mutable fields to share temporary state. |
| Return complete `java` code | Include the refactored original method and every new helper needed to compile. | Returning only a diff fragment. |
| Comment new helpers | Add a one-line comment above each new method describing its purpose. | Commenting obvious statements inside the method body. |

## Examples

### Repository ID to domain ID extraction

**Before**

```java
public FactLineBuilder setC_BPartner_ID_IfValid(final int bpartnerId) {
    assertNotBuild();
    if (bpartnerId > 0) {
        setC_BPartner_ID(bpartnerId);
    }
    return this;
}
```

**After**

```java
// Applies the partner id when a valid domain id is available.
public FactLineBuilder bpartnerIdIfNotNull(final BPartnerId bpartnerId) {
    if (bpartnerId != null) {
        return bpartnerId(bpartnerId);
    } else {
        return this;
    }
}

public FactLineBuilder setC_BPartner_ID_IfValid(final int bpartnerRepoId) {
    return bpartnerIdIfNotNull(BPartnerId.ofRepoIdOrNull(bpartnerRepoId));
}
```

### Factory seam extraction

**Before**

```java
public DefaultExpander add(RelationshipType type, Direction direction) {
    Direction existingDirection = directions.get(type.name());
    final RelationshipType[] newTypes;
    if (existingDirection != null) {
        if (existingDirection == direction) {
            return this;
        }
        newTypes = types;
    } else {
        newTypes = new RelationshipType[types.length + 1];
        System.arraycopy(types, 0, newTypes, 0, types.length);
        newTypes[types.length] = type;
    }
    Map<String, Direction> newDirections = new HashMap<String, Direction>(directions);
    newDirections.put(type.name(), direction);
    return new DefaultExpander(newTypes, newDirections);
}
```

**After**

```java
public DefaultExpander add(RelationshipType type, Direction direction) {
    Direction existingDirection = directions.get(type.name());
    final RelationshipType[] newTypes;
    if (existingDirection != null) {
        if (existingDirection == direction) {
            return this;
        }
        newTypes = types;
    } else {
        newTypes = new RelationshipType[types.length + 1];
        System.arraycopy(types, 0, newTypes, 0, types.length);
        newTypes[types.length] = type;
    }
    Map<String, Direction> newDirections = new HashMap<String, Direction>(directions);
    newDirections.put(type.name(), direction);
    return (DefaultExpander) newExpander(newTypes, newDirections);
}

// Creates the expander instance for the updated type and direction state.
protected RelationshipExpander newExpander(RelationshipType[] types,
        Map<String, Direction> directions) {
    return new DefaultExpander(types, directions);
}
```

## Gotchas

- **Do not extract across hidden side effects**: preserve order when calls mutate state, validate builders, or depend on lazy initialization.
- **Do not over-extract trivial one-liners**: extraction should improve naming, reuse, testability, or complexity.
- **Keep Java 17 compatibility**: do not introduce APIs or syntax beyond Java 17.
- **Do not remove functionality**: every branch in the original method must still be reachable unless it was provably dead and the user asked for cleanup.

## Output template

````markdown
## Java extract-method result

**Status:** refactored | no qualifying method | blocked
**Thresholds checked:** LOC > 15, NOM > 10, CC > 10
**Methods changed:** <method names>

```java
<complete compilable refactored method and helper methods>
```

### Notes
- <behavior preservation or validation note>
````

## Quality gate

- [ ] LOC, NOM, and CC thresholds were assessed before extraction.
- [ ] At least one cohesive helper method was extracted for each qualifying method, unless no method qualified.
- [ ] Each new helper has a descriptive name and a one-line purpose comment.
- [ ] The returned Java code is complete and compilable on Java 17 in its original class context.
- [ ] Original behavior, side effects, exceptions, and return values are preserved.
- [ ] The output follows `## Output template` exactly.
