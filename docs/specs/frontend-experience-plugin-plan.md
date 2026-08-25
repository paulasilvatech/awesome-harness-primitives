# Frontend Experience Plugin Implementation Specification

| Field | Value |
| --- | --- |
| Status | Proposed implementation plan |
| Target plugin | `frontend-experience` |
| Canonical plugin path | `harness/github-copilot/plugins/frontend-experience/` |
| Canonical component paths | `harness/github-copilot/agents/` and `harness/github-copilot/skills/` |
| Initial specification date | 2026-08-25 |
| Architecture decision | One installable plugin composed from focused agents and progressively disclosed skills |
| Primary surfaces | Web, progressive web apps, mobile applications, and desktop applications |

## Executive Summary

Build one installable GitHub Copilot plugin named `frontend-experience`. The plugin must help teams define, design, implement, test, and release product-specific frontend experiences without defaulting to interchangeable AI-generated layouts.

The package must remain modular internally. Three lean agents own product design, implementation, and independent quality assurance. Focused Agent Skills own domain knowledge and workflows for visual systems, responsive behavior, dashboards, data entry, conversational UI, accessibility, discoverability, testing, backend integration, and release validation. Skills load on demand, so one plugin does not imply one monolithic context.

The plugin must support existing projects before greenfield scaffolding. It detects the repository's actual framework, versions, design system, testing tools, API contracts, and platform targets before recommending changes. It must not replace an established local system with a generic design system or force a preferred framework onto an existing application.

Quality is part of the workflow rather than a final polish pass. Every user story and acceptance criterion must map to implementation evidence and either an automated check or an explicitly documented manual verification. Browser, mobile, desktop, accessibility, performance, discoverability, and backend-integration checks apply according to the product surface and risk.

## Decision and Rationale

### Decision

Create one plugin with multiple focused components. Do not create separate plugins for dashboards, data entry, chat, SEO, accessibility, or testing in the initial release.

### Why one plugin

| Benefit | Rationale |
| --- | --- |
| One installation | A project receives one coherent product-delivery workflow rather than discovering and installing several overlapping packages. |
| Shared evidence | Product context, design decisions, stories, API contracts, and QA results use one traceability model. |
| Progressive disclosure | GitHub Copilot discovers skills from their descriptions and loads detailed guidance only when relevant. |
| Consistent quality gates | Accessibility, responsive behavior, backend failures, and test evidence do not disappear at plugin boundaries. |
| Independent evolution | Individual skills can be added, versioned, reviewed, and tested without turning agents into large knowledge dumps. |
| Reuse without duplication | Existing canonical agents and skills can be materialized into the package through `plugin-sources.json`. |

### Future split criteria

Create a separate plugin only when a capability develops an independent operational boundary. Examples include a device-lab package that requires Appium infrastructure, paid device farms, platform credentials, or a separately maintained client extension. A topic boundary alone is not enough reason to create another plugin.

## Problem Statement

Generated frontend work commonly fails in predictable ways:

- The interface could belong to any product after replacing the logo.
- Every page becomes a collection of equal-weight cards.
- Decorative gradients, blurred surfaces, oversized headings, and rounded containers substitute for information architecture.
- Controls are visible but do not implement complete behavior or failure states.
- Mobile support means stacking desktop regions instead of adapting hierarchy and interaction.
- Dashboards use visually fashionable charts without matching the analytical question or data shape.
- Data-entry experiences expose validation too late, lose user input, or fail to connect server errors to fields.
- Chat interfaces implement only a message list and input, omitting streaming control, retries, citations, tool states, and accessibility announcements.
- SEO is reduced to a title tag while canonical URLs, social previews, structured data, icons, robots policy, and sitemap behavior remain incomplete.
- Screens are declared finished without browser evidence, backend integration, accessibility checks, or realistic states.

This plugin must replace those defaults with product evidence, explicit design decisions, complete interaction states, and executable validation.

## Goals

1. Produce frontend experiences that visibly belong to the product, audience, domain, and workflow.
2. Turn product intent into testable user stories, acceptance criteria, design contracts, and traceability records.
3. Support web, PWA, mobile, and desktop surfaces without pretending that one layout or interaction model fits all platforms.
4. Provide professional guidance for operational interfaces, dashboards, data visualizations, data entry, conversational UI, public websites, and content-heavy experiences.
5. Treat WCAG 2.2 AA accessibility, keyboard behavior, focus, zoom, reduced motion, and assistive technology as correctness concerns.
6. Integrate discoverability work, including technical SEO, metadata, social previews, structured data, web manifests, and icon assets.
7. Validate frontend-to-backend behavior through mocks, contract tests, integration environments, and critical end-to-end flows.
8. Prefer the repository's established stack, design system, components, and test conventions.
9. Use official, current sources for volatile claims and record when evidence was verified.
10. Package the capability according to this repository's canonical-source, synchronization, and validation rules.

## Non-Goals

- Do not become a generic backend, database, infrastructure, branding, or product-management plugin.
- Do not promise that visual polish creates product-market fit or improved conversion.
- Do not invent personas, research findings, analytics, metrics, business rules, or user preferences.
- Do not guarantee search ranking, accessibility certification, legal compliance, performance outcomes, or usability without evidence.
- Do not force React, a component library, a charting library, or a testing tool when an existing project has an appropriate alternative.
- Do not use current visual trends as mandatory style rules.
- Do not copy proprietary screens, branding, text, assets, or exact layouts from reference products.
- Do not treat generated screenshots, Lighthouse scores, or automated accessibility scans as complete proof by themselves.
