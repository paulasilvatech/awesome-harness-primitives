---
name: "java-docs"
description: "Apply Javadoc best practices to Java types and members, deferring the full checklist to the java-docs skill."
argument-hint: "target=<file-or-package>"
agent: "tech-writer"
tools: ["read", "edit", "search"]
---
# /java-docs

## Objective

Bring the Javadoc on a Java file or package up to the project standard — summary sentences, `@param`, `@return`, `@throws`, generics, and `{@code}` blocks — so public and protected members are documented correctly and consistently. The detailed checklist lives in the [`java-docs`](../skills/java-docs/SKILL.md) skill; this prompt applies it to the SIFAP 2.0 backend without restating it.

> [!NOTE]
> Document *why*, not *what*: the summary sentence states intent, not a restatement of the method signature.

## When to Invoke

During Stage 3/4, while implementing or reviewing backend Java, once the target class or package compiles and its public surface is stable enough to document.

## Preconditions

- The target `.java` file or package exists and compiles
- The public and protected surface to document is identified
- The code follows the Java 21 conventions in [`backend.instructions.md`](../instructions/backend.instructions.md)

## Inputs the Team Must Provide

- `target` — the file or package to document (for example, `backend/src/main/java/com/sifap/payment`)
- Any domain terms that clarify intent for a summary sentence
- Ask the user for anything that is missing.

## What I Will Do

- Apply the Javadoc conventions in the [`java-docs`](../skills/java-docs/SKILL.md) skill to every public and protected member of the target
- Write a concise summary sentence for each member, then document parameters, returns, thrown exceptions, and type parameters
- Use `{@inheritDoc}` where behavior is unchanged and document the delta where it is not
- Leave the compiled behavior untouched — documentation only

## What I Will NOT Do

- Add noise comments that restate the signature or the obvious
- Change method bodies, signatures, or visibility to "make documentation easier"
- Put sensitive data (CPF, benefit amounts) in `{@code}` examples — I mask it
- Write Javadoc in any language other than English

## Output Format

The target file(s) with Javadoc added in place, plus a short summary:

```markdown
### Documented
| Member | Javadoc added |
|---|---|
| `PaymentService#approve(PaymentId)` | summary, `@param`, `@return`, `@throws` |

### Skipped
- `PaymentService#toString()` — self-explanatory, no Javadoc needed.
```

## Definition of Done

- [ ] Every public and protected member has a summary sentence ending in a period
- [ ] `@param`, `@return`, `@throws`, and `@param <T>` are present where applicable
- [ ] No sensitive data appears in any example
- [ ] All Javadoc is in English and the file still compiles

## Prompt Body

The [`java-docs`](../skills/java-docs/SKILL.md) skill owns the full Javadoc convention set — read it, then apply it to the target.

**Step 1 — Locate the surface.**
Open `target` and list every public and protected type and member that lacks correct Javadoc.

**Step 2 — Apply the skill.**
Document each member per the skill: a summary sentence first, then `@param` (lowercase, no trailing period), `@return`, `@throws`, `@param <T>`, and `{@code}`/`<pre>{@code ...}</pre>` where useful.

**Step 3 — Respect the kit rules.**
Keep behavior unchanged, write in English, and mask CPF and benefit amounts in any example.

**Step 4 — Report.**
Summarize what you documented and what you deliberately skipped.

## Invocation Example

```
/java-docs target=backend/src/main/java/com/sifap/payment
```
