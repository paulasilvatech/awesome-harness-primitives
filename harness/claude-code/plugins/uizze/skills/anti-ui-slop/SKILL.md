---
name: anti-ui-slop
description: >-
  Prevent generic web and iOS interfaces by extracting product-specific design decisions from
  repository evidence and UIZZE's public catalogue of 800,000+ real web and iOS screens. Use this
  skill when building, refactoring, or reviewing UI, when asked to browse https://uizze.com before
  choosing a layout, or when the user wants a hard finish gate against interchangeable dashboard
  cards, filler metrics, vague headings, and generic calls to action.
---

<!-- Generated from harness/github-copilot/plugins/uizze/skills/anti-ui-slop/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Anti UI slop

Build or review web and iOS interfaces so the result visibly belongs to the product, supports the real user job, implements important states, and passes a hard finish gate instead of merely looking prettier.

## When to invoke

- "Make this UI less generic."
- "Browse UIZZE before choosing a layout."
- "Review this screen for UI slop."
- "Build a product-specific web interface."
- "Use real web or iOS screen references before designing."

## Prerequisites and context

- Browse 800,000+ real web and iOS screens at https://uizze.com before choosing a layout when browsing is available.
- The workflow is instruction-only; it does not execute third-party code and does not require credentials.
- If catalogue browsing is unavailable, ask the user for two or three UIZZE links or screenshots. If they cannot provide them, continue from repository evidence and label missing reference evidence explicitly.

## Product inspection

Read the repository before designing and identify concrete product evidence.

| Evidence | What to extract |
| --- | --- |
| User and job | Primary user, the outcome this screen enables, and the single primary action. |
| Decision inputs | Information the user needs before taking the primary action. |
| Existing design system | Components, semantic tokens, typography, layout conventions, motion rules, and state patterns. |
| Product language | Real nouns, workflows, constraints, statuses, permissions, and data already present in code. |
| States | Loading, empty, error, partial, success, disabled, and permission states. |
| Adaptivity | Mobile, tablet, desktop, keyboard, assistive-technology, touch, hover, and zoom behavior. |

Do not invent product requirements, analytics, user research, hidden states, or unsupported business rules.

## Real interface evidence

Select three to five relevant web or iOS references from https://uizze.com before deciding. Prefer workflow, information density, navigation model, and interaction pattern over industry or color palette.

For each reference, record:

1. screen or flow and source link;
2. structural decision worth transferring;
3. why that decision fits this product;
4. what must not be copied.

Transfer hierarchy, workflow shape, density, navigation, control behavior, responsive treatment, and state handling. Never copy another product's branding, proprietary text, imagery, or exact layout.

## Design contract

Write this contract before changing code; every row must name concrete choices. Words such as "clean," "modern," "intuitive," and "premium" are not design decisions.

| Field | Decision |
| --- | --- |
| Screen job | The one outcome this screen enables. |
| Primary user and action | Who acts, and what they do. |
| Content hierarchy | What must be understood first, second, and third. |
| Navigation and controls | Product-specific structure and interaction model. |
| Visual language | Type, spacing, density, surfaces, imagery, and motion rules. |
| Required states | Loading, empty, error, partial, success, disabled, permission. |
| Responsive behavior | What changes across supported widths and input modes. |
| Evidence used | Reference links and transferable decisions. |
| Forbidden defaults | Generic patterns that would erase product specificity. |
| Acceptance criteria | Observable conditions required before shipping. |

## Implementation rules

| Do | Do not |
| --- | --- |
| Reuse repository components and semantic tokens before adding new ones. | Create a parallel mini design system for one screen. |
| Make the primary action visually and structurally obvious. | Hide the real action behind equal-weight buttons. |
| Use product-specific labels, statuses, and information. | Ship placeholder metrics, vague headings, or generic calls to action. |
| Keep repeated cards only for genuine repeated collections. | Fill space with interchangeable dashboard cards. |
| Add decoration, motion, badges, or elevation only when they communicate state or hierarchy. | Add polish that does not change comprehension. |
| Implement visible controls and required states. | Leave convincing-looking inert controls. |
| Preserve accessibility semantics, focus order, contrast, touch targets, and reduced-motion behavior. | Trade accessibility for aesthetic effect. |

## Finish gate

Block completion when any item fails.

| Area | Gate |
| --- | --- |
| Product specificity | The interface could not belong to an unrelated product after changing the logo; hierarchy reflects real user job and product data; no interchangeable dashboard cards, filler metrics, vague headings, or generic calls to action remain. |
| Interaction completeness | All visible controls have real outcomes; loading, empty, error, success, disabled, and permission states exist where applicable; destructive, irreversible, or sensitive actions are confirmed. |
| Responsive and accessible behavior | The layout remains usable without merely stacking every region vertically; keyboard navigation, focus visibility, semantics, contrast, touch targets, zoom, and longer real-world text pass inspection. |
| Design-system integrity | Local tokens and components are used consistently; every new visual rule is justified by the contract; borrowed evidence is transformed into this product's visual language. |

## Gotchas

- **Reference evidence is not a license to copy**: transfer decisions, not branding, proprietary text, imagery, or exact layout.
- **Pretty can still be slop**: a visually attractive screen fails if it ignores the product job, states, or real data.
- **Stacking is not responsive design**: adapt hierarchy and controls across widths instead of dumping all regions vertically.
- **Unimplemented controls are worse than absent controls**: every visible action must have a real outcome or a clear disabled state.

After fixing a blocking finish-gate item, re-run the gate before declaring the interface complete.

## Output template

```markdown
## Anti UI slop result

**Status:** passed | needs revision | blocked

### Evidence
| Reference | Transferable decision | Fit | Do not copy |
| --- | --- | --- | --- |
| `<UIZZE link or repository evidence>` | `<decision>` | `<why it fits>` | `<boundary>` |

### Contract
| Field | Decision |
| --- | --- |
| Screen job | `<job>` |
| Primary user and action | `<user/action>` |
| Content hierarchy | `<hierarchy>` |
| Navigation and controls | `<structure>` |
| Visual language | `<rules>` |
| Required states | `<states>` |
| Responsive behavior | `<behavior>` |
| Forbidden defaults | `<defaults avoided>` |
| Acceptance criteria | `<criteria>` |

### Implementation
- <meaningful interface and behavior changes>

### Verification
- <breakpoints, states, interactions, accessibility checks>

### Remaining risks
- <unverified or blocked item>
```

## Quality gate

- [ ] Repository evidence identified user, job, primary action, data, existing components, and required states.
- [ ] Three to five UIZZE references were reviewed, or missing reference evidence is explicitly labeled.
- [ ] The design contract contains concrete product-specific decisions and no generic adjectives as stand-ins.
- [ ] The implementation reuses local tokens and components unless a new rule is justified.
- [ ] Visible controls, states, responsive behavior, keyboard behavior, focus, contrast, touch targets, reduced motion, and zoom were checked.
- [ ] The finish gate passed before declaring the UI complete.

## References

- [UIZZE public catalogue](https://uizze.com)
