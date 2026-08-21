---
name: 'java-docs'
description: 'Add or improve Javadoc documentation for Java types according to documentation best practices.'
agent: 'agent'
tools: ['read', 'search', 'edit']
argument-hint: 'target=<java-type-or-package>'
---

# /java-docs

## Objective

Add or improve Javadoc for Java types, constructors, methods, fields, packages, and complex members so public and protected APIs are clear, required tags are present, inherited documentation is used correctly, and examples are formatted with standard Javadoc conventions.

## When to Invoke

Use this prompt when Java API documentation is missing, stale, incomplete, or inconsistent, especially before publishing public APIs, reviewing library changes, or improving generated Javadoc quality.

## Preconditions

- The target Java type, package, selected code, or source tree is available.
- Documentation edits are permitted for the requested Java files.
- Existing repository documentation style and check commands are preferred over new tooling.
- The requested scope is limited enough to document accurately from source evidence.

## Inputs the Team Must Provide

- `target` — the Java type, package, selected code, or source tree to document.
- Any audience or API stability context, such as internal, public, deprecated, or newly introduced APIs.
- Version information when `@since` or `@version` values must be added.
- Ask the user for anything that is missing; stop before editing if missing intent would change public API wording.

## What I Will Do

- Inspect the target API behavior before writing Javadoc.
- Document public and protected members with Javadoc comments.
- Document package-private and private members when they are complex or not self-explanatory.
- Write a concise first sentence that summarizes what the member does and ends with a period.
- Use `@param`, `@return`, `@throws` or `@exception`, `@see`, `{@inheritDoc}`, `@param <T>`, `{@code}`, `<pre>{@code ... }</pre>`, `@since`, `@version`, `@author`, and `@deprecated` when appropriate.
- Preserve existing behavior and code formatting while editing documentation.

## What I Will NOT Do

- Change runtime behavior, signatures, visibility, exceptions, or API contracts just to improve documentation.
- Invent behavior that is not visible in code, tests, or existing documentation.
- Add noisy comments for obvious private implementation details.
- Add `@since`, `@version`, or `@author` values when the repository does not use them or the value is unknown.
- Use `{@inheritDoc}` when a subclass has a major behavior change that must be documented directly.
- Mark a member `@deprecated` without providing the alternative when one is known.

## Output Format

Return or apply documentation changes, then report in this shape:

```markdown
## Java Documentation Result

### Target
- `src/main/java/com/example/PaymentService.java`

### Documentation Added or Updated
| Member | Change |
| --- | --- |
| `PaymentService` | Added type-level summary and behavior notes. |
| `createPayment(PaymentRequest)` | Added `@param`, `@return`, and `@throws`. |

### Javadoc Practices Applied
- First sentence summary ending with a period.
- `@param` descriptions start with lowercase and do not end with a period.
- `{@code}` used for inline code snippets.
- `<pre>{@code ... }</pre>` used for code blocks.

### Validation
- Command:
- Result:

### Notes
- 
```

## Definition of Done

- [ ] Public and protected members in scope have useful Javadoc or an intentional reason for omission.
- [ ] Complex package-private and private members are documented when not self-explanatory.
- [ ] First sentences are concise summary descriptions and end with a period.
- [ ] `@param`, `@return`, `@throws` or `@exception`, `@see`, `{@inheritDoc}`, `@param <T>`, `{@code}`, `<pre>{@code ... }</pre>`, `@since`, `@version`, `@author`, and `@deprecated` are used only where appropriate.
- [ ] Documentation matches actual behavior and does not invent unsupported contracts.
- [ ] Existing documentation checks or compile commands were run when available, or the reason they could not run is reported.

## Prompt Body

Follow these steps in order. Improve documentation without changing code behavior.

**Step 1 — Confirm the documentation scope.**
Identify `${input:target:<java-type-or-package>}` or the selected Java code. Ask for missing scope before editing.

**Step 2 — Inspect behavior and style.**
Read the target code, nearby tests, and existing Javadoc style. Determine whether the repository documents only public APIs or also complex internal members.

**Step 3 — Document types and members.**
Add or improve Javadoc for public and protected members. Document package-private and private members as well when they are complex or not self-explanatory.

**Step 4 — Write correct summary sentences.**
Make the first sentence of each Javadoc comment the summary description. Keep it concise, describe what the method or type does, and end it with a period.

**Step 5 — Add required tags.**
Use `@param` for method parameters. Start each parameter description with a lowercase letter and do not end it with a period. Use `@return` for return values. Use `@throws` or `@exception` for thrown exceptions. Use `@param <T>` for type parameters in generic types or methods.

**Step 6 — Use references and inheritance carefully.**
Use `@see` for references to other types or members. Use `{@inheritDoc}` to inherit documentation from base classes or interfaces unless there is a major behavior change; document differences directly when behavior changes.

**Step 7 — Format code and metadata.**
Use `{@code}` for inline code snippets. Use `<pre>{@code ... }</pre>` for code blocks. Use `@since`, `@version`, `@author`, and `@deprecated` only when the repository standard and available facts support them. For `@deprecated`, provide an alternative when known.

**Step 8 — Validate and report.**
Run existing documentation, compile, or test checks when available and relevant. Report changed files, documentation practices applied, validation status, and any unsupported unknowns.

## Invocation Example

```
/java-docs target=src/main/java/com/example/PaymentService.java
```
