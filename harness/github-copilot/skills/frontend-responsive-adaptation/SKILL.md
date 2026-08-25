---
name: frontend-responsive-adaptation
description: "Specify and verify hierarchy, layout, content, navigation, and interaction adaptations across viewports, containers, orientation, input methods, foldables, mobile browsers, tablets, desktop windows, and native surfaces. Use this skill when responsive or cross-device frontend work is requested."
---

# Frontend responsive adaptation

Adapt the product job across changing space, input, platform, content, and user settings instead of merely stacking desktop regions.

## When to invoke

- "Make this workflow responsive across mobile, tablet, and desktop."
- "Define behavior around our actual content breakpoints."
- "Adapt this interface for touch, keyboard, pointer, and orientation changes."
- "Review this PWA, mobile, or desktop layout for cross-device behavior."
- "Test long content, zoom, safe areas, or foldable postures."

## Adaptation matrix

Read [references/adaptive-layouts.md](references/adaptive-layouts.md) and define, for each applicable condition:

- information priority and progressive disclosure;
- navigation and control placement;
- density, pane, table, chart, and media behavior;
- touch, pointer, hover, keyboard, and virtual-keyboard behavior;
- safe areas, browser chrome, orientation, resizing, minimum windows, or hinges;
- long content, localization, RTL, zoom, dynamic type, and motion settings;
- loading, offline, interruption, and recovery behavior.

Use content-driven breakpoints and container queries when the installed stack supports them. Validate immediately before and after actual layout transitions.

## Input and device behavior

Read [references/input-and-device-matrix.md](references/input-and-device-matrix.md). Hover is an enhancement, gestures require alternatives, keyboard focus remains visible, and controls must remain reachable when virtual keyboards or browser chrome change available space.

Representative web widths may include near `320`, `375`, `768`, and `1280` CSS pixels plus a supported wide state. These are evidence points, not universal breakpoints or proof of fluid behavior between them.

## Criteria

- The primary task and critical controls remain discoverable.
- Priority changes are explicit; secondary regions may collapse, move, summarize, or become progressive.
- Tables, charts, boards, editors, media, and toolbars have domain-specific narrow behavior.
- Orientation, resizing, split view, safe areas, and lifecycle changes preserve progress when applicable.
- No content clips, overlaps, becomes unreachable, or requires unintended two-dimensional scrolling.
- Accessibility behavior survives zoom, reflow, dynamic type, high contrast, forced colors, and reduced motion.

Use [assets/human-review-checklist.md](assets/human-review-checklist.md) for subjective review.

## Limits

- Do not infer supported devices or native profiles from a single web viewport.
- Do not add breakpoints from a framework default without content evidence.
- Do not call a desktop stack responsive when mobile only changes column order.
- Do not claim simulator, device, screen-reader, or installability evidence unless it ran.

## Output template

```markdown
## Responsive adaptation result
**Status:** ready | needs revision | blocked

### Supported conditions
| Profile | Space/input/platform | Required |
| --- | --- | --- |

### Adaptation decisions
| Transition or condition | Hierarchy | Layout/content | Controls/input | State preservation |
| --- | --- | --- | --- | --- |

### Boundary verification
| Viewport/container/device | State and content | Result | Evidence |
| --- | --- | --- | --- |
```

## Quality gate

- [ ] Supported profiles and input methods come from evidence.
- [ ] Breakpoints are content-driven and boundary conditions are identified.
- [ ] Hierarchy, navigation, content, and controls adapt rather than only stack.
- [ ] Long content, localization, RTL, zoom, keyboard, touch, orientation, and safe areas are considered when applicable.
- [ ] State and progress survive relevant resize, lifecycle, offline, and interruption events.
- [ ] Unrun device or assistive-technology checks are explicit.
