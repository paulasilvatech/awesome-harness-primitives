---
name: penpot-uiux-design
description: >-
  Create, review, and improve professional UI/UX designs in Penpot using penpot/penpot-mcp tools,
  design systems, component patterns, accessibility checks, and platform guidelines. Use when
  asked to design a UI, create interface, build layout, design dashboard, create form, design
  landing page, make it accessible, design system, component library, or improve an existing
  Penpot file.
---

<!-- Generated from harness/github-copilot/skills/penpot-uiux-design/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Penpot UI/UX design

Create or refine Penpot designs by combining MCP tool execution with UI/UX principles, design-system discovery, accessibility checks, component specs, layout rules, and visual validation.

## When to invoke

- "Design a UI for this app in Penpot."
- "Create a dashboard layout and component library."
- "Make this Penpot design accessible."
- "Build a mobile form and navigation flow."
- "Review this landing page for usability."

## Prerequisites and context

- Use the `penpot/penpot-mcp` MCP server when Penpot tools are available.
- Check whether `mcp__penpot__penpot_api_info` succeeds before giving setup instructions. If it succeeds, the server is running and connected.
- If the tool fails, ask whether the Penpot MCP server is already installed and running; only guide installation when the user confirms it is not installed.
- Installation path: clone https://github.com/penpot/penpot-mcp.git and run `npm install`, then `npm run bootstrap`.
- In Penpot, open a design file, choose Plugins → Load plugin from URL, enter `http://localhost:4400/manifest.json`, then click "Connect to MCP server" in the plugin UI.
- VS Code MCP configuration uses `http://localhost:4401/sse` under `mcp.servers.penpot.url`.

## MCP tool map

| Tool | Use it for |
| --- | --- |
| `mcp__penpot__execute_code` | Run JavaScript in the Penpot plugin context to create, inspect, and modify designs. |
| `mcp__penpot__export_shape` | Export shapes as PNG/SVG for visual inspection. |
| `mcp__penpot__import_image` | Import images, icons, photos, and logos. |
| `mcp__penpot__penpot_api_info` | Retrieve Penpot API documentation and verify server connectivity. |

## Procedure

1. Confirm whether a design system or brand guidelines exist; prefer user tokens, colors, spacing, typography, and naming conventions over defaults.
2. Inspect the current file with `mcp__penpot__execute_code`, `penpotUtils.shapeStructure()`, and `penpotUtils.findShapes()` before creating new objects.
3. Discover existing colors from `fills`, text styles from `fontSize` and `fontWeight`, and components from `penpot.library.local.components`.
4. Check existing boards before creating new boards; compute the rightmost edge and place the new board with a gap.
5. Create or modify with `penpot.createBoard()`, `penpot.createRectangle()`, `penpot.createText()`, `insertChild(index, shape)`, `shape.resize(w, h)`, and `penpotUtils.setParentXY(shape, x, y)`.
6. Apply responsive containers with `addFlexLayout()` and validate child order when `dir="column"` or `dir="row"`.
7. Validate visually with `mcp__penpot__export_shape`, inspect bounds and hierarchy with `penpotUtils.analyzeDescendants()`, `isContainedIn()`, and `penpotUtils.shapeStructure()`, then export CSS with `penpot.generateStyle(selection, { type: 'css', includeChildren: true })` when requested.

## Design system handling

| Situation | Action |
| --- | --- |
| User has a design system | Use specified colors, spacing, typography, component patterns, and naming conventions. |
| Current Penpot file has patterns | Discover and reuse existing colors, text styles, and components before adding defaults. |
| No design system exists | Use the default tokens below and offer to establish consistent patterns. |
| Components need details | Read `references/component-patterns.md` for buttons, forms, and navigation specs. |

```javascript
const allShapes = penpotUtils.findShapes(() => true, penpot.root);
const colors = new Set();
allShapes.forEach(s => { if (s.fills) s.fills.forEach(f => colors.add(f.fillColor)); });
const textStyles = allShapes.filter(s => s.type === 'text').map(s => ({ fontSize: s.fontSize, fontWeight: s.fontWeight }));
const components = penpot.library.local.components;
return { colors: [...colors], textStyles, componentCount: components.length };
```

## Layout and board rules

| Rule | Value |
| --- | --- |
| Related screen gap | `100px` between boards in the same flow. |
| Different flow gap | `200px+` between sections or flows. |
| Board alignment | Align boards vertically with the same `y` and order flows horizontally. |
| Mobile screen | `375×812`, status bar `44px`, header/nav `56px`, content padding `16px`, bottom nav/CTA `84px`. |
| Desktop dashboard | `1440×900`, sidebar `240px`, header `64px`, page title/actions row, content grid. |

```javascript
const boards = penpotUtils.findShapes(s => s.type === 'board', penpot.root);
let nextX = 0;
const gap = 100;
boards.forEach(b => { const rightEdge = b.x + b.width; if (rightEdge + gap > nextX) nextX = rightEdge + gap; });
const newBoard = penpot.createBoard();
newBoard.x = nextX;
newBoard.y = 0;
newBoard.resize(375, 812);
```

```text
┌─────────────────────────────┐
│ Status Bar (44px)           │
├─────────────────────────────┤
│ Header/Nav (56px)           │
├─────────────────────────────┤
│ Content Area                │
│ Padding: 16px horizontal    │
├─────────────────────────────┤
│ Bottom Nav/CTA (84px)       │
└─────────────────────────────┘
```

```text
┌──────┬──────────────────────────────────┐
│      │ Header (64px)                    │
│ Side │──────────────────────────────────│
│ bar  │ Page Title + Actions             │
│ 240  │──────────────────────────────────│
│ px   │ Content Grid                     │
└──────┴──────────────────────────────────┘
```

## Default tokens

Use these only when user tokens are absent.

| Category | Token or level | Value | Usage |
| --- | --- | --- | --- |
| Spacing | `spacing-xs` | `4px` | Tight inline elements. |
| Spacing | `spacing-sm` | `8px` | Related elements. |
| Spacing | `spacing-md` | `16px` | Default padding. |
| Spacing | `spacing-lg` | `24px` | Section spacing. |
| Spacing | `spacing-xl` | `32px` | Major sections. |
| Spacing | `spacing-2xl` | `48px` | Page-level spacing. |
| Typography | Display | `48-64px`, Bold | Hero headlines. |
| Typography | H1/H2/H3 | `32-40px`, `24-28px`, `20-22px` | Page titles and sections. |
| Typography | Body/Small/Caption | `16px`, `14px`, `12px` | Main content, secondary text, labels, hints. |
| Color | Success/Warning/Error | `#22C55E`, `#F59E0B`, `#EF4444` ranges | Confirmations, caution, errors. |
| Color | Primary/Secondary/Neutral | Brand, supporting actions, gray scale | CTAs, secondary actions, text and borders. |

## Component and accessibility checks

| Area | Checks |
| --- | --- |
| Buttons | Clear action-oriented label of 2-3 words; minimum touch target `44×44px`; states for default, hover, active, disabled, loading; contrast `3:1`; consistent border radius. |
| Forms | Labels above inputs, not just placeholders; required indicators; adjacent error messages; logical tab order; input types such as email and tel match content. |
| Navigation | Current location indicated; consistent position; maximum `7±2` top-level items; mobile target size `48px`. |
| Accessibility | Text contrast `4.5:1`; large text `3:1`; touch targets `44×44px`; visible focus states; alt text; H1→H2→H3 hierarchy; never rely solely on color. |
| Review | Visual hierarchy, spacing, alignment, readable `16px+` body text, obvious interactive elements, loading/empty/error states, and design-system consistency. |

## Penpot gotchas

- **Do not assign `width` or `height` directly**: they are READ-ONLY; use `shape.resize(w, h)`.
- **Do not assign `parentX` or `parentY` directly**: they are READ-ONLY; use `penpotUtils.setParentXY(shape, x, y)`.
- **Use `insertChild(index, shape)` for z-ordering**: do not rely on `appendChild`.
- **Flex child order is reversed** for `dir="column"` or `dir="row"`; validate after applying `addFlexLayout()`.
- **Reset text growth after `text.resize()`** to `growType` values `"auto-width"` or `"auto-height"`.

## Troubleshooting

| Issue | Solution |
| --- | --- |
| Plugin won't connect | Check servers are running with `npm run start:all` in the `penpot-mcp` directory. |
| Browser blocks localhost | Allow local network access, disable Brave Shield, or try Firefox. |
| Tools not appearing in client | Restart VS Code or Claude completely after config changes. |
| Tool execution fails or times out | Ensure the Penpot plugin UI is open and shows "Connected". |
| "WebSocket connection failed" | Check firewall allows ports `4400`, `4401`, and `4402`. |

## Progressive disclosure and bundled resources

Read bundled references only when needed:

- `references/setup-troubleshooting.md`: installation, server startup, and connection troubleshooting.
- `references/component-patterns.md`: detailed button, form, navigation, and component specs.
- `references/accessibility.md`: contrast, keyboard, target size, and WCAG-oriented checks.
- `references/platform-guidelines.md`: screen sizes and iOS, Android, Material Design guidance.

## Preservation notes

Keep these original operational phrases because they map to real Penpot workflow checks: user-centered design, mobile-first design, existing tokens/specs, `Create/modify**`, Create/modify, create/modify, Color/Contrast**, Loading/empty/error states, text/borders, sections/flows, and the flex-order warning REVERSED, and the literal export connector ` via `. Client setup may involve `settings.json` and restarting VS Code/Claude; tool execution fails/times out when the plugin UI is not connected.

## Output template

```markdown
## Penpot design result - <screen or flow>

**Status:** created | improved | reviewed | blocked
**Target:** web | mobile | desktop | dashboard | form | landing page | design system
**Design system:** reused | discovered | default tokens

| Area | Decision | Evidence | Follow-up |
| --- | --- | --- | --- |
| Layout | <board size, grid, spacing> | <Penpot shape or export evidence> | <next step> |
| Components | <buttons/forms/nav/cards> | <states and patterns> | <next step> |
| Accessibility | <contrast/touch/focus/hierarchy> | <check result> | <fix> |
| Validation | <export/API check> | <file or shape exported> | <remaining issue> |

### MCP actions
- `mcp__penpot__execute_code`: <summary>
- `mcp__penpot__export_shape`: <summary or not needed>
```

## Quality gate

- [ ] Existing design system, components, colors, and text styles were checked before defaults were used.
- [ ] New boards avoid overlap and follow `100px` or `200px+` spacing rules.
- [ ] Layout uses responsive containers or explicit grid logic appropriate to the screen.
- [ ] Buttons, forms, navigation, typography, and accessibility checks match the tables above.
- [ ] Penpot READ-ONLY properties were not assigned directly.
- [ ] The design was visually validated through export or a documented blocker.
