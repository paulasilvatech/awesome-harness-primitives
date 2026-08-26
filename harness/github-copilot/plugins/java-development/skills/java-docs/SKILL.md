---
name: "java-docs"
description: >-
  Write and review Java Javadoc comments for public, protected, generic, deprecated, and complex members. Use this skill when the user asks for Java documentation, Javadoc best practices, missing comments, API docs, or documentation cleanup in Java code.
---

# Java documentation

Add or improve Javadoc so Java APIs communicate behavior, parameters, return values, exceptions, inheritance, generics, deprecations, and examples without restating obvious implementation details.

## When to invoke

- "Add Javadoc to these Java classes."
- "Review this Java documentation for best practices."
- "Document public and protected methods with Javadoc."
- "Fix missing `@param`, `@return`, or `@throws` tags."

## Documentation coverage

| Element | Requirement | Notes |
| --- | --- | --- |
| Public types and members | Document with Javadoc comments. | Treat this as mandatory API documentation. |
| Protected members | Document with Javadoc comments. | Subclasses depend on the contract. |
| Package-private and private members | Document when complex or not self-explanatory. | Prefer clear code over comments for obvious internals. |
| Generic type parameters | Use `@param <T>`. | Describe what the type represents, not its Java syntax. |
| Exceptions | Use `@throws` or `@exception`. | Document conditions that callers can act on. |
| Deprecations | Use `@deprecated` and provide an alternative. | Pair with the Java `@Deprecated` annotation when changing code. |

## Javadoc tag rules

| Tag or construct | Use | Style rule |
| --- | --- | --- |
| Summary sentence | First sentence of every Javadoc comment. | Concise overview ending with a period. |
| `@param` | Method parameters. | Description starts with a lowercase letter and does not end with a period. |
| `@return` | Non-void return values. | Explain meaning, units, nullability, and special cases. |
| `@throws` / `@exception` | Exceptions thrown by methods. | Prefer `@throws`; include the triggering condition. |
| `@see` | References to other types or members. | Use for related APIs, not generic external reading. |
| `{@inheritDoc}` | Inherit base-class or interface documentation. | Use unless behavior materially changes; document differences when it does. |
| `{@code}` | Inline code snippets. | Use for identifiers, literals, and short expressions. |
| `<pre>{@code ... }</pre>` | Code blocks. | Preserve formatting without HTML escaping surprises. |
| `@since` | Version or release introduction. | Use only when the project tracks API versions. |
| `@version` | Member or type version. | Use only if the project already maintains version tags. |
| `@author` | Author attribution. | Use only if the project convention already uses it. |

## Content patterns

| API shape | Document |
| --- | --- |
| Mutator | Side effects, validation, idempotency, and thread-safety expectations. |
| Accessor | Units, nullability, caching, and whether returned collections are mutable. |
| Factory | Ownership, lifecycle, default values, and failure modes. |
| Async or callback API | Execution thread, ordering, cancellation, and exception propagation. |
| Collection-returning method | Ordering, duplicates, mutability, and empty-result behavior. |
| Security-sensitive method | Required permissions, input trust boundary, and logging constraints. |

## Examples

### Good

```java
/**
 * Returns the active customer names in display order.
 *
 * @param regionCode the ISO region code used to filter customers
 * @return immutable list of active customer names, never {@code null}
 * @throws IllegalArgumentException if {@code regionCode} is blank
 */
List<String> findActiveCustomerNames(String regionCode);
```

### Bad

```java
/**
 * findActiveCustomerNames method.
 * @param regionCode Region code.
 * @return list.
 */
List<String> findActiveCustomerNames(String regionCode);
```

## Gotchas

- **Do not repeat the signature**: explain the contract, not that `getName` gets a name.
- **Do not use `{@inheritDoc}` when behavior changes**: callers need the subclass-specific differences.
- **Do not add `@return` to `void` methods**: document side effects in prose instead.
- **Do not introduce `@author`, `@version`, or `@since` inconsistently**: follow existing project convention.

## Output template

```markdown
## Java documentation result

**Status:** documented | needs project decision | blocked
**Scope:** `<files or selection>`

| Element | Action | Evidence |
| --- | --- | --- |
| `<class or member>` | added/updated/reviewed | `<tags and contract details>` |

**Validation**
- Summary sentences end with periods: pass/fail
- Required tags present: pass/fail
- Project conventions preserved: pass/fail
```

## Quality gate

- [ ] Public and protected Java types and members have meaningful Javadoc comments.
- [ ] Complex package-private or private members are documented when code alone is not self-explanatory.
- [ ] The first sentence is a concise summary and ends with a period.
- [ ] Every parameter has `@param`; generic parameters use `@param <T>`.
- [ ] Non-void methods have `@return` when the return contract is not obvious.
- [ ] Exceptions are documented with `@throws` or `@exception` where callers need to know failure conditions.
- [ ] Inline code uses `{@code}` and blocks use `<pre>{@code ... }</pre>`.
- [ ] `@deprecated`, `@since`, `@version`, `@author`, and `@see` follow existing project conventions.
