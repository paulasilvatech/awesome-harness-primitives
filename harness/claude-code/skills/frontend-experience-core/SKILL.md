---
name: frontend-experience-core
description: >-
  Establish product evidence, design contracts, complete UI states, anti-generic interface gates,
  and routing for frontend work. Use this skill when a material web, PWA, mobile, or desktop
  design, implementation, or quality request begins, before loading a narrower frontend domain
  skill.
---

<!-- Generated from harness/github-copilot/skills/frontend-experience-core/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Frontend experience core

Ground frontend work in the consuming product and repository, define a concrete contract, and block completion when the result is generic, behaviorally incomplete, or unsupported by evidence.

## When to invoke

- "Design this frontend feature from the repository evidence."
- "Implement this screen without making it look generic."
- "Review this UI for complete states and product fit."
- "Plan a web, mobile, PWA, or desktop experience."
- "Route this frontend request to the right specialist."

## Evidence and precedence

Use evidence in this order:

1. User requirements, approved stories, product documentation, code, tests, schemas, tokens, runtime behavior, and actual assets.
2. Applicable normative standards and official platform or framework documentation.
3. Properly licensed user-provided references.
4. Community guidance only when authoritative evidence is unavailable and clearly labeled.

Read [references/product-evidence.md](references/product-evidence.md) when the product job, local stack, content, states, or supported surfaces are unclear. Unknowns remain unknown; do not invent users, metrics, research, analytics, business rules, or compatibility.

## Required design contract

Before a material visual or interaction decision, record:

| Field | Required decision |
| --- | --- |
| User and screen job | Who acts, in what environment, and the outcome they need. |
| Decision sequence | What must be understood first, second, and third. |
| Actions | One primary action, justified secondary actions, and access constraints. |
| Product language | Real nouns, statuses, permissions, units, and content. |
| States | Applicable loading, empty, partial, error, offline, success, disabled, and permission states. |
| Visual grammar | Existing tokens, components, density, typography, imagery, and justified additions. |
| Adaptation | Changes across viewport, input, platform, orientation, locale, zoom, and motion preference. |
| Forbidden defaults | Generic patterns that would erase product specificity. |
| Acceptance evidence | Stable IDs and the automated or manual evidence required. |

Start with [assets/design-contract.md](assets/design-contract.md) when the consuming project has no equivalent.

## Workflow routing

Load only capabilities that match the task:

| Need | Skill |
| --- | --- |
| Stories, criteria, journeys, traceability | `frontend-requirements-and-stories` |
| Typography, color, layout, density, motion | `frontend-visual-system` |
| Viewports, devices, orientation, input changes | `frontend-responsive-adaptation` |
| Dashboards, charts, tables, analytical flows | `frontend-dashboard-visualization` |
| Forms, search, filters, uploads, multi-step entry | `frontend-form-interactions` |
| Chat, streaming, citations, tools, attachments | `frontend-conversational-ui` |
| Public metadata, previews, manifests, icons | `frontend-discoverability-assets` |
| Semantic, keyboard, focus, zoom, AT behavior | `frontend-accessibility` |
| Test layers, runtime evidence, release verdict | Relevant frontend testing and release skills |

## Finish gate

Read [references/anti-generic-interface-gate.md](references/anti-generic-interface-gate.md) before declaring a material interface complete. Block completion when:

- the interface could belong to an unrelated product after changing the logo;
- hierarchy does not follow the user's decision sequence;
- cards, gradients, oversized text, blur, elevation, or animation replace information architecture;
- visible controls have no implemented result, unavailable state, or explanation;
- important states, access behavior, or recovery are absent;
- responsive behavior only stacks desktop regions;
- a new one-off token or component system conflicts with the established one;
- acceptance criteria lack executed or documented manual evidence.

Use [assets/human-review-checklist.md](assets/human-review-checklist.md) for subjective review. Record `pass`, `needs revision`, `blocked`, or `not applicable` with evidence for each item.

## Limits

- Do not replace product management, user research, branding, backend ownership, legal review, or accessibility certification.
- Do not force a framework, design system, chart library, state library, or testing tool onto an established project.
- Do not copy proprietary screens, assets, text, or exact layouts from references.
- Do not claim product-market fit, conversion, ranking, certification, compatibility, or performance outcomes without evidence.

## Output template

```markdown
## Frontend experience contract
**Status:** ready | needs revision | blocked
**Surface:** web | PWA | mobile | desktop | mixed

### Evidence
| Source | Finding | Confidence |
| --- | --- | --- |

### Contract
| Field | Decision | Evidence |
| --- | --- | --- |

### Applicable skills and gates
- <skill>: <reason>

### Unknowns and blockers
- <fact still needed, owner, and impact>
```

## Quality gate

- [ ] Product and repository evidence was inspected before design or implementation decisions.
- [ ] The design contract names the user, job, hierarchy, actions, states, visual grammar, adaptation, and forbidden defaults.
- [ ] Only relevant domain skills were selected.
- [ ] Unknowns are labeled and no product facts were fabricated.
- [ ] Visible controls and applicable states are complete or explicitly blocked.
- [ ] The anti-generic finish gate has evidence for every applicable item.
