# EARS Notation

EARS (Easy Approach to Requirements Syntax) is a constrained natural-language pattern set for writing unambiguous, testable requirements. Use it for every acceptance criterion in a specification so each one is atomic, verifiable, and free of vague language.

## Why EARS

Free-form requirements ("the system should be fast and user-friendly") are ambiguous and untestable. EARS forces each requirement into one of a few sentence templates with a clear trigger and response, which makes acceptance criteria directly traceable to tests.

## The five patterns

| Pattern | Template | When to use |
| --- | --- | --- |
| Ubiquitous | The `<system>` shall `<response>`. | An always-on property with no trigger. |
| Event-driven | When `<trigger>`, the `<system>` shall `<response>`. | A response to a specific event. |
| State-driven | While `<state>`, the `<system>` shall `<response>`. | Behavior that holds during a state. |
| Unwanted behavior | If `<condition>`, then the `<system>` shall `<response>`. | Error handling and edge cases. |
| Optional feature | Where `<feature is included>`, the `<system>` shall `<response>`. | Behavior tied to an optional capability. |

Complex requirements may combine a state and an event:
`While <state>, when <trigger>, the <system> shall <response>.`

## Examples

- Ubiquitous: The API shall return responses encoded as UTF-8 JSON.
- Event-driven: When a user submits the checkout form, the system shall validate all required fields before creating an order.
- State-driven: While a payment is processing, the system shall disable the submit button.
- Unwanted behavior: If an uploaded file exceeds 10 MB, then the system shall reject it and return a 413 status.
- Optional feature: Where single sign-on is enabled, the system shall redirect unauthenticated users to the identity provider.

## Rules

- One requirement per sentence. Split compound requirements ("validate and email") into separate criteria.
- Name a concrete system or component as the subject, not "it" or "the app" generically.
- Use "shall" for the response. Avoid "should", "may", "could", "would", and "will".
- Make the response observable and testable. Avoid "fast", "easy", "robust", "user-friendly"; quantify instead (for example "within 200 ms").
- State the trigger or condition explicitly; do not leave it implied.
- No em dashes. Use commas, periods, colons, or semicolons.

## Authoring checklist

1. Does each criterion match exactly one EARS pattern?
2. Is the subject a named system or component?
3. Is the response observable and measurable?
4. Are error and edge cases captured with the `If ... then` pattern?
5. Can a tester write a pass/fail check directly from the sentence?

## References

- Mavin, A. et al., "Easy Approach to Requirements Syntax (EARS)", IEEE RE 2009. <https://doi.org/10.1109/RE.2009.9>
- Alistair Mavin, EARS overview. <https://alistairmavin.com/ears/>
