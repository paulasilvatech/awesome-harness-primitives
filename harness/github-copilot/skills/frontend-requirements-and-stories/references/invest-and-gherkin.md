# INVEST and Given/When/Then guidance

## Story quality

| INVEST property | Check |
| --- | --- |
| Independent | The outcome can be prioritized and tested without an artificial technical sequence where feasible. |
| Negotiable | The story states value and constraints, not a frozen unapproved implementation. |
| Valuable | The actor receives an observable product outcome. |
| Estimable | Scope, states, contracts, and unknowns are bounded enough to discuss effort. |
| Small | The story has one coherent outcome; split unrelated journeys or risk boundaries. |
| Testable | Acceptance criteria describe observable results and required evidence. |

## Criterion quality

- **Given** establishes only relevant state, data, access, viewport, device, or service conditions.
- **When** describes a user or system event.
- **Then** describes visible behavior, state, data, navigation, announcement, or contract outcome.
- Avoid CSS, component names, hooks, classes, and test-tool syntax unless they are approved constraints.
- One criterion may cover a coherent behavior; split unrelated outcomes.
- Include negative and recovery behavior when the risk justifies it.

Bad: `Then the page is modern and fast.`

Better: `Then the order summary becomes visible without horizontal scrolling at the supported narrow viewport, focus moves to its heading, and the submitted values remain available after a recoverable server error.`
