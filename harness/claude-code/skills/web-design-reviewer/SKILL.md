---
name: web-design-reviewer
description: >-
  Inspect local or remote website design, identify layout, responsive, accessibility, and visual
  consistency defects, and make source-level fixes. Use when users ask to "review website design",
  "check the UI", "fix the layout", "find design problems", or validate a web page after changes.
---

<!-- Generated from harness/github-copilot/skills/web-design-reviewer/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Web design reviewer

Inspect local or remote websites visually, identify layout, responsive, accessibility, and consistency defects, then make source-level fixes when the workspace contains the code.

## When to invoke

- "Review this website design."
- "Check the UI for layout problems."
- "Fix the responsive layout."
- "Find design problems on this page."
- "Validate the web design after my changes."

## Scope of application

- Static sites (HTML/CSS/JS)
- SPA frameworks such as React / Vue / Angular / Svelte
- Full-stack frameworks such as Next.js / Nuxt / SvelteKit
- CMS platforms such as WordPress / Drupal
- Any other web application

## Prerequisites and context

### Required

1. **Target website must be running**
   - Local development server (e.g., `http://localhost:3000`)
   - Staging environment
   - Production environment (for read-only reviews)

2. **Browser automation must be available**
   - Screenshot capture
   - Page navigation
   - DOM information retrieval

3. **Access to source code (when making fixes)**
   - Project must exist within the workspace

## Procedure

```mermaid
flowchart TD
    A[Step 1: Information Gathering] --> B[Step 2: Visual Inspection]
    B --> C[Step 3: Issue Fixing]
    C --> D[Step 4: Re-verification]
    D --> E{Issues Remaining?}
    E -->|Yes| B
    E -->|No| F[Completion Report]
```

---

## Information gathering

### 1.1 URL Confirmation

If the URL is not provided, ask the user:

> Please provide the URL of the website to review (e.g., `http://localhost:3000`)

### 1.2 Understanding Project Structure

When making fixes, gather the following information:

| Item | Example Question |
|------|------------------|
| Framework | Are you using React / Vue / Next.js, etc.? |
| Styling Method | CSS / SCSS / Tailwind / CSS-in-JS, etc. |
| Source Location | Where are style files and components located? |
| Review Scope | Specific pages only or entire site? |

### 1.3 Automatic Project Detection

Attempt automatic detection from files in the workspace:

```
Detection targets:
├── package.json     → Framework and dependencies
├── tsconfig.json    → TypeScript usage
├── tailwind.config  → Tailwind CSS
├── next.config      → Next.js
├── vite.config      → Vite
├── nuxt.config      → Nuxt
└── src/ or app/     → Source directory
```

### 1.4 Identifying Styling Method

| Method | Detection | Edit Target |
|--------|-----------|-------------|
| Pure CSS | `*.css` files | Global CSS or component CSS |
| SCSS/Sass | `*.scss`, `*.sass` | SCSS files |
| CSS Modules | `*.module.css` | Module CSS files |
| Tailwind CSS | `tailwind.config.*` | className in components |
| styled-components | `styled.` in code | JS/TS files |
| Emotion | `@emotion/` imports | JS/TS files |
| CSS-in-JS (other) | Inline styles | JS/TS files |

---

## Visual inspection criteria

### 2.1 Page Traversal

1. Navigate to the specified URL
2. Capture screenshots
3. Retrieve DOM structure/snapshot (if possible)
4. If additional pages exist, traverse through navigation

### 2.2 Inspection Items

Work through [references/visual-checklist.md](references/visual-checklist.md) during inspection and again during post-fix verification.

#### Layout Issues

| Issue | Description | Severity |
|-------|-------------|----------|
| Element Overflow | Content overflows from parent element or viewport | High |
| Element Overlap | Unintended overlapping of elements | High |
| Alignment Issues | Grid or flex alignment problems | Medium |
| Inconsistent Spacing | Padding/margin inconsistencies | Medium |
| Text Clipping | Long text not handled properly | Medium |

#### Responsive Issues

| Issue | Description | Severity |
|-------|-------------|----------|
| Non-mobile Friendly | Layout breaks on small screens | High |
| Breakpoint Issues | Unnatural transitions when screen size changes | Medium |
| Touch Targets | Buttons too small on mobile | Medium |

#### Accessibility Issues

| Issue | Description | Severity |
|-------|-------------|----------|
| Insufficient Contrast | Low contrast ratio between text and background | High |
| No Focus State | Cannot determine state during keyboard navigation | High |
| Missing alt Text | No alternative text for images | Medium |

#### Visual Consistency

| Issue | Description | Severity |
|-------|-------------|----------|
| Font Inconsistency | Mixed font families | Medium |
| Color Inconsistency | Non-unified brand colors | Medium |
| Spacing Inconsistency | Non-uniform spacing between similar elements | Low |

### 2.3 Viewport Testing (Responsive)

Test at the following viewports:

| Name | Width | Representative Device |
|------|-------|----------------------|
| Mobile | 375px | iPhone SE/12 mini |
| Tablet | 768px | iPad |
| Desktop | 1280px | Standard PC |
| Wide | 1920px | Large display |

---

## Source-level fixing

### 3.1 Issue Prioritization

```mermaid
block-beta
    columns 1
    block:priority["Priority Matrix"]
        P1["P1: Fix Immediately\n(Layout issues affecting functionality)"]
        P2["P2: Fix Next\n(Visual issues degrading UX)"]
        P3["P3: Fix If Possible\n(Minor visual inconsistencies)"]
    end
```

### 3.2 Identifying Source Files

Identify source files from problematic elements:

1. **Selector-based Search**
   - Search codebase by class name or ID
   - Explore style definitions with `grep_search`

2. **Component-based Search**
   - Identify components from element text or structure
   - Explore related files with `semantic_search`

3. **File Pattern Filtering**
   ```
   Style files: src/**/*.css, styles/**/*
   Components: src/components/**/*
   Pages: src/pages/**, app/**
   ```

### 3.3 Applying Fixes

#### Framework-specific Fix Guidelines

See [references/framework-fixes.md](references/framework-fixes.md) for details.

#### Fix Principles

1. **Minimal Changes**: Only make the minimum changes necessary to resolve the issue
2. **Respect Existing Patterns**: Follow existing code style in the project
3. **Avoid Breaking Changes**: Be careful not to affect other areas
4. **Add Comments**: Add comments to explain the reason for fixes where appropriate

---

## Re-verification

### 4.1 Post-fix Confirmation

1. Reload browser (or wait for development server HMR)
2. Capture screenshots of fixed areas
3. Compare before and after

### 4.2 Regression Testing

- Verify that fixes haven't affected other areas
- Confirm responsive display is not broken

### 4.3 Iteration Decision

```mermaid
flowchart TD
    A{Issues Remaining?}
    A -->|Yes| B[Return to Step 2]
    A -->|No| C[Proceed to Completion Report]
```

**Iteration Limit**: If more than 3 fix attempts are needed for a specific issue, consult the user

---

## Report format

```markdown
## Web design review result

## Summary

| Item | Value |
|------|-------|
| Target URL | {URL} |
| Framework | {Detected framework} |
| Styling | {CSS / Tailwind / etc.} |
| Tested Viewports | Desktop, Mobile |
| Issues Detected | {N} |
| Issues Fixed | {M} |

## Detected Issues

### [P1] {Issue Title}

- **Page**: {Page path}
- **Element**: {Selector or description}
- **Issue**: {Detailed description of the issue}
- **Fixed File**: `{File path}`
- **Fix Details**: {Description of changes}
- **Screenshot**: Before/After

### [P2] {Issue Title}
...

## Unfixed Issues (if any)

### {Issue Title}
- **Reason**: {Why it was not fixed/could not be fixed}
- **Recommended Action**: {Recommendations for user}

## Recommendations

- {Suggestions for future improvements}
```

---

## Required capabilities

| Capability | Description | Required |
|------------|-------------|----------|
| Web Page Navigation | Access URLs, page transitions | Yes |
| Screenshot Capture | Page image capture | Yes |
| Image Analysis | Visual issue detection | Yes |
| DOM Retrieval | Page structure retrieval | Recommended |
| File Read/Write | Source code reading and editing | Required for fixes |
| Code Search | Code search within project | Required for fixes |

---

## Browser automation options

### Implementation with Playwright MCP

[Playwright MCP](https://github.com/microsoft/playwright-mcp) is recommended as the reference implementation for this skill.

| Capability | Playwright MCP Tool | Purpose |
|------------|---------------------|---------|
| Navigation | `browser_navigate` | Access URLs |
| Snapshot | `browser_snapshot` | Retrieve DOM structure |
| Screenshot | `browser_take_screenshot` | Images for visual inspection |
| Click | `browser_click` | Interact with interactive elements |
| Resize | `browser_resize` | Responsive testing |
| Console | `browser_console_messages` | Detect JS errors |

#### Configuration Example (MCP Server)

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest", "--caps=vision"]
    }
  }
}
```

### Other Compatible Browser Automation Tools

| Tool | Features |
|------|----------|
| Selenium | Broad browser support, multi-language support |
| Puppeteer | Chrome/Chromium focused, Node.js |
| Cypress | Easy integration with E2E testing |
| WebDriver BiDi | Standardized next-generation protocol |

The same workflow can be implemented with these tools. As long as they provide the necessary capabilities (navigation, screenshot, DOM retrieval), the choice of tool is flexible.

---

## Gotchas

### Do

- Always save screenshots before making fixes
- Fix one issue at a time and verify each
- Follow the project's existing code style
- Confirm with user before major changes
- Document fix details thoroughly

### Do not

- Large-scale refactoring without confirmation
- Ignoring design systems or brand guidelines
- Fixes that ignore performance
- Fixing multiple issues at once (difficult to verify)

---

## Troubleshooting

### Problem: Style files not found

1. Check dependencies in `package.json`
2. Consider the possibility of CSS-in-JS
3. Consider CSS generated at build time
4. Ask user about styling method

### Problem: Fixes not reflected

1. Check if development server HMR is working
2. Clear browser cache
3. Rebuild if project requires build
4. Check CSS specificity issues

### Problem: Fixes affecting other areas

1. Rollback changes
2. Use more specific selectors
3. Consider using CSS Modules or scoped styles
4. Consult user to confirm impact scope


## Progressive disclosure and bundled resources

Read bundled references only when the task needs that depth.

- `references/visual-checklist.md`: detailed inspection checklist for layout, responsive, accessibility, and visual consistency passes.
- `references/framework-fixes.md`: framework-specific source fix guidance for React, Vue, Angular, Svelte, Next.js, Nuxt, SvelteKit, Tailwind CSS, CSS Modules, and CSS-in-JS.

## Output template

```markdown
## Web design review result

**Status:** complete | needs fixes | blocked
**Target URL:** `<http://localhost:3000 or remote URL>`
**Framework:** `<React/Vue/Angular/Svelte/Next.js/Nuxt/SvelteKit/CMS/unknown>`
**Styling:** `<CSS/SCSS/Sass/Tailwind CSS/CSS Modules/styled-components/Emotion/unknown>`
**Tested viewports:** `375px`, `768px`, `1280px`, `1920px`

| Priority | Page | Element | Issue | Evidence | Fixed file | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | `<path>` | `<selector or description>` | `<overflow/overlap/contrast/focus/etc.>` | `<screenshot or DOM evidence>` | `{File path}` | `<Before/After result>` |

**Unfixed issues**
- `<issue>`: `<reason and recommended action>`
```

## Quality gate

- [ ] `name` is `web-design-reviewer` and matches the parent directory.
- [ ] The target URL is reachable, including `http://localhost:3000` when the local server is running.
- [ ] Screenshots or DOM snapshots were inspected before any edit.
- [ ] `references/visual-checklist.md` is used for inspection and post-fix verification when detailed review is requested.
- [ ] `references/framework-fixes.md` is used before framework-specific edits.
- [ ] Mobile `375px`, tablet `768px`, desktop `1280px`, and wide `1920px` viewports are tested when responsive behavior is in scope.
- [ ] Fixes are minimal, source-level, and verified with screenshots or DOM evidence after reload/HMR/rebuild.
- [ ] More than three failed fix attempts on one issue are reported instead of continuing blindly.

## References

- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
