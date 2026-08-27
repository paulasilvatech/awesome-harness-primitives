---
name: csharp-docs
description: >-
  Write and review C# XML documentation comments for public and complex internal APIs, including
  summaries, remarks, examples, cref links, parameters, returns, constructors, properties, and
  exceptions. Use when asked for C# documentation best practices or XML comments.
---

<!-- Generated from harness/github-copilot/skills/csharp-docs/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# C# XML documentation

Convert C# APIs into precise XML documentation comments that describe behavior, parameters, return values, examples, exceptions, and cross-references using Microsoft-style phrasing.

## When to invoke

- "Add XML docs to this C# API."
- "Review these C# documentation comments."
- "What should the `<param>` and `<returns>` text say?"
- "Document exceptions and examples for this method."

## API coverage

| API surface | Documentation expectation |
| --- | --- |
| Public types and members | Document with XML comments. |
| Internal members | Document when complex, non-obvious, or not self-explanatory, or part of a testable/internal contract. |
| Overrides and interface implementations | Use `<inheritdoc/>` unless behavior materially changes; document differences when it does. |
| Exceptions | Document exceptions thrown directly and nested exceptions users are likely to encounter. |

## Common XML tags

| Tag | Use |
| --- | --- |
| `<summary>` | Brief one-sentence description. Start with a present-tense, third-person verb. |
| `<remarks>` | Extra context, implementation notes, or usage constraints. |
| `<see langword="null" />` | `language-specific` keywords through `<see langword>` such as `null`, `true`, `false`, `int`, and `bool`. |
| `<c>` | Inline code snippets. |
| `<example>` | Usage examples. |
| `<code language="csharp">` | Code blocks inside `<example>`; the `<code>` tag should carry a `language` attribute such as `language="csharp"`. |
| `<see cref="TypeOrMember" />` | Inline reference in a sentence. |
| `<seealso cref="TypeOrMember" />` | Standalone See also reference. |
| `<inheritdoc/>` | Inherit base or interface documentation. |
| `<paramref name="name" />` | Reference a parameter in prose. |
| `<typeparamref name="T" />` | Reference a generic type parameter in prose. |

## Methods and generics

| Element | Wording rule |
| --- | --- |
| `<param>` | Use a noun phrase that does not specify the data type and begins with an introductory article. |
| Flag enum parameter | Start with "A bitwise combination of the enumeration values that specifies...". |
| Non-flag enum parameter | Start with "One of the enumeration values that specifies..." and treat it as a non-flag enum. |
| Boolean parameter | Use "`<see langword="true" />` to ...; otherwise, `<see langword="false" />`." |
| `out` parameter | Use "When this method returns, contains ... . This parameter is treated as uninitialized." |
| `<typeparam>` | Describe generic type parameters. |
| `<returns>` | Use a noun phrase that does not specify the data type and begins with an introductory article. |
| Boolean return | Use "`<see langword="true" />` if ...; otherwise, `<see langword="false" />`." |

## Constructors, properties, and exceptions

| Member | Required phrasing |
| --- | --- |
| Constructor summary | "Initializes a new instance of the `<Class>` class." or "Initializes a new instance of the `<Class>` struct." |
| Read-write property | Start `<summary>` with "Gets or sets..." for a read-write property. |
| Read-only property | Start `<summary>` with "Gets..." for a read-only property. |
| Boolean property | Start with "Gets a value that indicates whether..." or "Gets or sets a value that indicates whether...". |
| `<value>` | Describe the property value as a noun phrase; include default in a separate sentence when known. |
| Boolean `<value>` | Use "`<see langword="true" />` if ...; otherwise, `<see langword="false" />`. The default is ..." when a default is known. |
| `<exception cref="...">` | State the condition directly; omit "Thrown if" and initial "If". The baseline shorthand is `<exception cref>`. |

## Examples

### Good

```csharp
/// <summary>
/// Gets a value that indicates whether the cache contains the specified key.
/// </summary>
/// <param name="key">The key to locate.</param>
/// <returns><see langword="true" /> if the cache contains <paramref name="key" />; otherwise, <see langword="false" />.</returns>
```

### Bad

```csharp
/// <summary>Checks a string key and returns bool.</summary>
/// <param name="key">String key.</param>
/// <returns>Boolean result.</returns>
```

## Gotchas

- **Do not restate the type**: parameter and return descriptions should explain meaning, not `string`, `int`, or `bool`.
- **Do not use vague summaries**: describe observable behavior, not "Does the thing".
- **Do not overuse `<inheritdoc/>`**: document behavior differences explicitly.
- **Do not document impossible exceptions**: list exceptions users can actually encounter.

## Output template

````markdown
## C# documentation result

**Target:** `<type or member>`

```csharp
/// <summary>
/// <present-tense third-person description>.
/// </summary>
/// <param name="<name>"><noun phrase>.</param>
/// <returns><noun phrase or Boolean wording>.</returns>
/// <exception cref="<ExceptionType>"><condition>.</exception>
```

### Documentation notes
- `<summary>`: <why this wording fits>
- `<param>`: <parameter wording decisions>
- `<returns>`: <return wording decisions>
- `<exception>`: <exception coverage>
````

## Quality gate

- [ ] Public APIs have XML comments; complex internal APIs are documented when needed.
- [ ] `<summary>` starts with a present-tense, third-person verb.
- [ ] Parameters, type parameters, returns, values, and exceptions use the required wording patterns.
- [ ] Boolean, enum, flag enum, and `out` parameter wording follows the specialized rules.
- [ ] Examples use `<example>` with `<code language="csharp">` when code blocks are included in XML docs.
- [ ] Cross-references use `<see cref>`, `<seealso>`, `<paramref>`, and `<typeparamref>` where appropriate.
