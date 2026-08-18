---
name: java-refactoring-remove-parameter
description: >-
  Refactor Java 17 methods by applying Remove Parameter safely. Use this skill when asked to remove unused or redundant Java method parameters, update call sites, preserve behavior, and return complete compilable refactored methods.
---

# Java remove parameter refactoring

Apply the Remove Parameter refactoring to Java methods by identifying parameters that are unused or redundant, updating signatures and internal calls, and returning complete Java 17 code that preserves behavior.

## When to invoke

- "Remove unused parameters from this Java method."
- "Refactor this Java API with Remove Parameter."
- "Clean up redundant method parameters and call sites."
- "Return the Java 17 method after removing unused parameters."
- "Assess all methods with unused parameters."

## Criteria

A parameter qualifies for removal only when at least one condition is true and no blocker applies.

| Condition | Evidence | Example |
| --- | --- | --- |
| Unused | The parameter is never referenced in the method body, nested lambdas, anonymous classes, or delegated calls. | `firstRel` and `firstProp` are not used in `NodeImpl(long id, long firstRel, long firstProp)`. |
| Redundant | The same value is already available from a trusted object, field, constant, or method call. | `isCloud` can be removed when the callee can derive cloud state from `context.getCloudCluster()`. |
| Always ignored downstream | The parameter is passed only to calls whose matching parameter is also removed. | `getGroupCommitLoadBeId(tableId, context.getCloudCluster(), isCloud)` becomes `getGroupCommitLoadBeId(tableId, context.getCloudCluster())`. |

| Blocker | Why it blocks removal |
| --- | --- |
| Public API compatibility is required | Removing a parameter changes binary/source compatibility. Provide an overload instead if compatibility is required. |
| Reflection, serialization, framework binding, or annotations depend on the signature | Frameworks may call the method by exact signature. |
| Parameter participates in overload resolution | Removing it can create ambiguity or call a different overload. |
| Parameter is documented as part of behavior | Update documentation and callers only when behavior is truly redundant. |

## Refactoring rules

- Remove the unnecessary parameter from the method or constructor definition.
- Remove the corresponding argument from all internal calls shown in the provided code.
- Preserve thrown exceptions such as `LoadException` and `DdlException`.
- Preserve all original functionality, control flow, return values, and side effects.
- Return complete and compilable Java 17 methods or constructors.
- Add a one-line comment above each modified method stating which parameter was removed and why.
- Output only one `java` code block when the user asks for code transformation.

## Examples

### Removing a redundant boolean

Before:

```java
public Backend selectBackendForGroupCommit(long tableId, ConnectContext context, boolean isCloud)
        throws LoadException, DdlException {
    if (!Env.getCurrentEnv().isMaster()) {
        try {
            long backendId = new MasterOpExecutor(context)
                    .getGroupCommitLoadBeId(tableId, context.getCloudCluster(), isCloud);
            return Env.getCurrentSystemInfo().getBackend(backendId);
        } catch (Exception e) {
            throw new LoadException(e.getMessage());
        }
    } else {
        return Env.getCurrentSystemInfo()
                .getBackend(selectBackendForGroupCommitInternal(tableId, context.getCloudCluster(), isCloud));
    }
}
```

After:

```java
// Removed isCloud because cloud state is derived from context.getCloudCluster().
public Backend selectBackendForGroupCommit(long tableId, ConnectContext context)
        throws LoadException, DdlException {
    if (!Env.getCurrentEnv().isMaster()) {
        try {
            long backendId = new MasterOpExecutor(context)
                    .getGroupCommitLoadBeId(tableId, context.getCloudCluster());
            return Env.getCurrentSystemInfo().getBackend(backendId);
        } catch (Exception e) {
            throw new LoadException(e.getMessage());
        }
    } else {
        return Env.getCurrentSystemInfo()
                .getBackend(selectBackendForGroupCommitInternal(tableId, context.getCloudCluster()));
    }
}
```

### Removing unused constructor parameters

Before:

```java
NodeImpl( long id, long firstRel, long firstProp )
{
     this( id, false );
}
```

After:

```java
// Removed firstRel and firstProp because this constructor delegates without using them.
NodeImpl(long id)
{
     this(id, false);
}
```

## Gotchas

- **Do not remove functionality with the parameter**: if the value controls behavior, the refactoring is invalid.
- **Update all visible call sites**: a compilable method signature is not enough if internal calls still pass the old argument.
- **Check overload ambiguity**: Java may bind to a different overload after an argument disappears.
- **Do not infer repository-wide callers from a snippet**: when only a snippet is provided, state that external call sites must be updated.

## Output template

```markdown
```java
// Removed <parameter> because <reason>.
<complete refactored Java 17 method or constructor>
```
```

## Quality gate

- [ ] Every removed parameter is unused or redundant by explicit evidence.
- [ ] No behavior, exception, return value, or side effect is removed.
- [ ] Method signatures and visible internal call sites are updated consistently.
- [ ] A one-line comment above each modified method explains the removed parameter and reason.
- [ ] Output is a single `java` code block containing complete compilable Java 17 code.
- [ ] Compatibility, reflection, framework binding, and overload blockers were considered.
