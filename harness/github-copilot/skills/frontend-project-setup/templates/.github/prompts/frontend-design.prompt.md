---
name: 'frontend-design'
description: 'Create or update evidence-backed frontend stories, journeys, state maps, information hierarchy, and a product-specific design contract.'
argument-hint: 'Describe the frontend feature, target surface, and destination.'
---

# /frontend-design

## Objective

Turn the requested frontend feature into stable stories, observable acceptance criteria, a state and journey map, and an implementation-ready design contract grounded in repository and product evidence.

Deliver the result to `${input:destination:response, edit, or file path}`. Do not change application code.

## When to Invoke

Run before implementing or materially redesigning a web, PWA, mobile, or desktop experience.

## Preconditions

- A concrete product request or problem is available in `${input:topic}`.
- The relevant repository, product, design-system, and contract evidence can be inspected.
- Any file destination is an explicitly approved design or product artifact path.

If a required precondition is not met, identify it and stop before making changes.

## Inputs the Team Must Provide

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| Feature or product problem | `${input:topic}` | Yes | Use as the scope; ask and stop if undefined. |
| Selected evidence | `${selection}` | No | Treat an empty selection as absent and inspect only permitted repository evidence. |
| Destination | `${input:destination:response, edit, or file path}` | Yes | Accept `response`, an approved design-artifact edit, or an exact file path. |
| Known users, surfaces, and constraints | Prompt or repository | No | Preserve as facts only when supplied or inspected; otherwise list as unknown. |

## What I Will Do

- Use `frontend-experience-core`, `frontend-requirements-and-stories`, and relevant domain skills.
- Inventory product language, user job, data, states, design system, surfaces, tests, and unknowns.
- Produce stable `US-NNN` and `AC-NNN` identifiers plus a traceable design contract.
- Validate the anti-generic interface gate and report unresolved decisions.
- Deliver only to the selected destination.

## What I Will NOT Do

- Implement or modify application code.
- Invent personas, research, analytics, metrics, permissions, business rules, or backend behavior.
- Copy proprietary screens, branding, assets, text, or exact layouts.
- Claim the design is implemented, accessible, or release-ready without runtime evidence.

## Output Format

Use exactly one destination mode:

- **Response:** return the contract in Chat with no workspace edits.
- **Edit:** update only the explicitly approved product/design artifact.
- **File path:** write only the exact requested design-artifact path when editing is available.

```markdown
## Frontend Design Result

### Evidence and Unknowns
| Item | Classification | Source / owner |
| --- | --- | --- |

### Stories and Acceptance Criteria
#### US-001 — <value>
- AC-001: Given ... When ... Then ...

### Journey and State Map
| Step | Intent | UI state | Data/backend | Recovery |
| --- | --- | --- | --- | --- |

### Design Contract
| Area | Decision | Evidence | Forbidden default |
| --- | --- | --- | --- |

### Engineering Handoff
- Scope, constraints, stable IDs, and open decisions
```

## Definition of Done

- [ ] Evidence, inferences, unknowns, and decisions are distinguished.
- [ ] Stories and acceptance criteria use stable IDs and observable behavior.
- [ ] Applicable success, failure, access, accessibility, responsive, and recovery states are represented.
- [ ] The contract defines hierarchy, actions, visual grammar, surface adaptation, and forbidden defaults.
- [ ] The selected destination is respected and no application code changed.
- [ ] Required checks ran or are named as unavailable.

## Prompt Body

Complete frontend design for:

- **Topic:** `${input:topic}`
- **Destination:** `${input:destination:response, edit, or file path}`
- **Selected context:**
  ```text
  ${selection}
  ```

Follow these steps in order:

1. **Validate the request.** Confirm the feature, surface, scope, and destination. Stop before side effects when required context remains ambiguous.
2. **Inspect evidence.** Read only relevant product docs, routes, components, tokens, content, schemas, tests, and runtime evidence.
3. **Build the contract.** Apply `frontend-experience-core`, `frontend-requirements-and-stories`, and only the relevant visual, responsive, dashboard, form, chat, accessibility, or discoverability skills.
4. **Verify specificity and traceability.** Run the anti-generic gate, check every acceptance criterion is observable, and identify required implementation and QA evidence.
5. **Deliver conditionally.** Respect the selected destination, then report validation and open decisions.

Do not convert an unknown into a design decision without evidence or explicit approval.

## Invocation Example

1. Select relevant product or repository context.
2. Run **Chat: Run Prompt** and choose `/frontend-design`.
3. Enter `Design the account recovery experience for web and mobile browser` for `topic`.
4. Enter `response` for `destination`.
5. Verify that a traceable contract appears in Chat and no application file changes.

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `frontend-product-designer` | agent | Owns the product-design judgment and engineering handoff. |
| `frontend-experience-core` | skill | Supplies evidence, contract, routing, and anti-generic gates. |
