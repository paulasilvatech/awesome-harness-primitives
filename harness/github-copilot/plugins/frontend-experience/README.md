# Frontend Experience Plugin

Build and verify product-specific frontend experiences from repository evidence instead of generic layout defaults. The plugin separates product design, implementation, and independent quality assurance while loading focused domain skills only when they apply.

## Status

Version `0.1.0` is incubating. A representative installed-plugin probe on 2026-08-25 discovered all components, invoked all three agents, confirmed their edit boundaries, and exercised the pinned Playwright MCP server against a disposable local page. This proves package activation and the tested web-browser path only; mobile, desktop packaging, native accessibility, and VS Code prompt profiles remain limited by the evidence recorded in `docs/HARNESS-VALIDATION.md`.

No `license` field is published yet. This repository does not declare one package-wide SPDX license, and the compatibility decision for every reused component must be explicit rather than inferred.

## Install

```bash
copilot plugin install frontend-experience@copilot-primitives
```

The MCP configuration uses `npx -y @playwright/mcp@0.0.79 --headless --isolated`. When the package is not cached, `npx -y` downloads and executes that exact npm package. Installation therefore requires an approved network and supply-chain boundary.

## Agents

| Agent | Responsibility | Write boundary |
| --- | --- | --- |
| `frontend-product-designer` | Turn product and repository evidence into stories, journeys, state maps, information hierarchy, and an implementation-ready design contract. | Read-only for application code; design artifacts only when explicitly approved. |
| `frontend-experience-engineer` | Implement an approved frontend slice in the repository's existing stack with complete states, accessible interactions, focused tests, and typed integration boundaries. | Frontend source, tests, directly related assets, and necessary frontend configuration only. |
| `frontend-qa-engineer` | Independently verify acceptance criteria, runtime behavior, visual quality, accessibility, integration, and release readiness. | Read-only by default; no application-source edits. |

## Skills

### Product and design

- `frontend-experience-core`
- `frontend-requirements-and-stories`
- `frontend-visual-system`
- `frontend-responsive-adaptation`
- `frontend-dashboard-visualization`
- `frontend-form-interactions`
- `frontend-conversational-ui`
- `frontend-discoverability-assets`
- `frontend-accessibility`
- `anti-ui-slop`

### Engineering and quality

- `frontend-test-strategy`
- `frontend-component-testing`
- `frontend-visual-e2e-testing`
- `frontend-backend-integration`
- `frontend-mobile-desktop-testing`
- `frontend-release-quality-gate`
- `playwright-explore-website`
- `playwright-generate-test`

### Workspace publication

- `frontend-project-setup`

The setup skill can preview and publish optional scoped instructions, VS Code prompt files, and a separately translated VS Code MCP entry into a consuming repository. These companions are not direct plugin components. The default operation is a no-write dry run, and writes require explicit approval.

## Delivery workflow

1. The product designer identifies evidence, unknowns, stories, acceptance criteria, and a design contract.
2. The experience engineer implements only the approved slice and reports changed files, tests, and unverified checks.
3. The QA engineer independently runs risk-based checks and returns `Ready`, `Ready with follow-ups`, or `Blocked`.
4. The release gate validates story-to-evidence traceability before accepting a verdict.

## Support posture

The skills detect and preserve the consuming repository's framework, versions, design system, API contracts, and test conventions. They do not install or upgrade dependencies implicitly.

- React, Next.js, Vite, Vue, Nuxt, PWA, React Native with Expo, Electron, and Tauri have explicit capability profiles, but each profile remains pilot-required until representative runtime evidence exists.
- Angular, Svelte, Astro, Flutter, SwiftUI, and Jetpack Compose are adapters. Native iOS and Android guidance is advisory until an approved implementation pilot demonstrates the target profile.
- Supporting one framework or surface never proves another.

## Safety and evidence

- Product facts, personas, research, metrics, business rules, and compatibility claims are never fabricated.
- Existing design systems and repository conventions take precedence over generic recommendations.
- Browser evidence must be redacted and must not contain credentials, personal data, customer screenshots, or production secrets.
- Automated accessibility and discoverability checks supplement manual verification; they do not establish certification, ranking, rich-result appearance, or installability by themselves.
- Runtime dependencies remain pinned, and unavailable checks are reported as evidence gaps rather than passes.
