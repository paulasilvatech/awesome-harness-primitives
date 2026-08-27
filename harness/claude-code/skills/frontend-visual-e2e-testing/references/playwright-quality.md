# Playwright quality rules

- Explore the running UI before generating code.
- Prefer role, label, accessible name, visible text, or established test IDs.
- Use web-first assertions and event-aware waits; avoid arbitrary sleeps.
- Assert the business outcome and critical intermediate state.
- Inspect console errors, failed requests, hydration warnings, unexpected requests, and redirects.
- Use safe isolated auth and deterministic fixtures.
- Close browser contexts and clean narrowly scoped data.
- Preserve traces, screenshots, and videos only under project artifact policy.
- Record first-attempt status and retries.

Blocked authentication, CAPTCHA, unavailable services, or unsafe data must remain explicit blockers.
