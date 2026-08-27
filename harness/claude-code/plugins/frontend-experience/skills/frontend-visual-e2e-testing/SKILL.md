---
name: frontend-visual-e2e-testing
description: >-
  Explore and verify frontend journeys with Playwright, representative states and viewports,
  screenshots, visual regression, console and network evidence, stable fixtures, and reproducible
  defects. Use this skill when material browser UI behavior or rendered quality needs runtime
  proof.
---

<!-- Generated from harness/github-copilot/plugins/frontend-experience/skills/frontend-visual-e2e-testing/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Frontend visual and E2E testing

Use real browser behavior to prove critical journeys, state transitions, responsive boundaries, visual stability, console health, and network outcomes.

## When to invoke

- "Validate this frontend flow with Playwright."
- "Run visual and responsive QA for this screen."
- "Add or review screenshot regression coverage."
- "Check console and network failures during this journey."
- "Produce a reproducible browser QA report."

## Prerequisites and context

- A safe running URL or approved startup command, critical flow, fixtures, and expected acceptance IDs are required.
- Use the installed Playwright MCP server for exploration evidence when available.
- Use `playwright-explore-website` before generating a new browser test and `playwright-generate-test` when code generation is requested.
- Never enter real secrets, payment data, or private personal data.

## Procedure

1. Detect existing Playwright configuration, projects, fixtures, auth state, base URL, artifact paths, screenshot policy, and commands.
2. Read [references/playwright-quality.md](references/playwright-quality.md) and explore the exact flow before generating selectors or tests.
3. Exercise representative success and risk states, keyboard and focus behavior, console errors, failed requests, and unexpected network calls.
4. Inspect material screens near narrow mobile, common mobile, intermediate/tablet, standard desktop, and supported wide conditions plus actual breakpoint boundaries.
5. Apply [references/visual-regression.md](references/visual-regression.md) before creating or updating baselines.
6. Record the environment and produce [assets/qa-report.md](assets/qa-report.md) with evidence, defects, limitations, and retest.

## Runtime requirements

- Use realistic long and localized content plus loading, empty, partial, error, success, disabled, and restricted states when applicable.
- Check overflow, clipping, overlap, occlusion, unstable dimensions, layout shift, real assets, fonts, charts, canvases, and media.
- Pair screenshot differences with behavioral assertions.
- Record browser, OS, viewport, device scale, fonts, timezone, locale, color scheme, reduced motion, data, build, and service revisions.

## Limits

- Do not use screenshots as the only accessibility, usability, or behavioral assertion.
- Do not update baselines mechanically or mask stable product content.
- Do not assume visual results transfer across OS, browser, headless mode, hardware, or fonts.
- Do not claim a flow passed when a required service or state was unavailable.

## Progressive disclosure and bundled resources

- [references/playwright-quality.md](references/playwright-quality.md): exploration, selectors, assertions, console, and network rules.
- [references/visual-regression.md](references/visual-regression.md): stable baseline policy.
- [assets/qa-report.md](assets/qa-report.md): browser QA template.
- [evals/evals.json](evals/evals.json): representative output evaluations.

## Output template

```markdown
## Browser QA result
**Status:** passed | failed | blocked

### Environment and flows
| Build | Browser/OS | Viewport/state | Flow/acceptance |
| --- | --- | --- | --- |

### Evidence and defects
| Scenario | Behavior | Visual | Console/network | Result |
| --- | --- | --- | --- | --- |

### Retest
- <exact setup and flow>
```

## Quality gate

- [ ] Existing Playwright configuration and commands were reused.
- [ ] The flow was explored before selectors or tests were generated.
- [ ] Representative states, boundary viewports, keyboard/focus, console, and network behavior were inspected.
- [ ] Screenshots use stable fixtures and are paired with behavioral assertions.
- [ ] Baseline updates are reviewed product changes with documented masks.
- [ ] Environment, defects, redaction, limitations, and retest steps are reproducible.
