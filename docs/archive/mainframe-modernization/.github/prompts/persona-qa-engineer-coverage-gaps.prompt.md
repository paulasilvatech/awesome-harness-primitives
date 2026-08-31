---
name: "coverage-gaps"
description: "Audit test coverage by REQ-ID and report untested requirements, missing edge cases, and spec-to-test gaps ranked by risk."
argument-hint: "feature=<NNN>-<feature> scope=all|diff|REQ-COMP"
agent: "qa-engineer"
tools: ["read", "search", "execute"]
---
# /coverage-gaps

## Objective

Audit test coverage in SIFAP 2.0 and deliver a prioritized list of **untested or insufficiently tested requirements** — not a percentage. Line coverage is a vanity metric; requirement coverage is the truth. The report is ready to paste into a sprint-planning ticket, highest risk first, with a one-line test recipe for each gap.

## When to Invoke

Before a bounded context is declared done, during PR review, or ahead of sprint planning — whenever the team needs to know which requirements are genuinely verified versus merely executed.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` declares the `REQ-ID`s in scope
- Implementation and test sources exist under `backend/` and/or `frontend/`
- A coverage report is available or can be generated (JaCoCo XML for the backend, Vitest LCOV for the frontend)

## Inputs the Team Must Provide

- The feature folder (`specs/<NNN>-<feature>/`) and the implementation folders
- A recent coverage report, or permission to generate one
- The scope: all `REQ-ID`s in the folder, only this PR's diff, or only the regulatory `REQ-COMP-*` set

Ask the user for anything that is missing.

## What I Will Do

- Build a requirements inventory from `spec.md`, keyed by `REQ-ID` and EARS pattern
- Cross-reference the `spec-traceability` job output in `.github/workflows/spec-quality.yml` for `REQ-ID`s CI already flags as untested
- Map each `REQ-ID` to its tests and rate it `MISSING`, `WEAK`, or `OK`
- Inspect EARS variants for hidden negative and state-transition cases
- Check legacy-derived edge cases generically against `01-archaeology/legacy-sifap/natural-programs/`
- Score every gap by risk and deliver the prioritized list

## What I Will NOT Do

- Invent SIFAP behavior, a missing requirement, or a legacy edge case — I reference `01-archaeology/legacy-sifap/` generically and ask the team when a value is unknown
- Write the tests (`/create-tests`), implement fixes (`@builder`), or edit the spec (`@requirements-engineer`)
- Report a line-coverage percentage as if it were behavior coverage
- Count redundant happy-path tests as sufficient, or treat UI snapshot tests as UX requirement coverage
- Suggest recipes that assert implementation details (private methods, SQL strings)

## Output Format

A Markdown report returned inline:

```markdown
## Coverage Gap Report — <feature>

### Summary
- Requirements in scope: 12
- OK: 7 — WEAK: 3 — MISSING: 2
- Highest-risk gap: REQ-014 (non-positive amount is not rejected)

### Gaps by risk

| REQ-ID | EARS pattern | Status | Risk (P×I) | Recipe |
|--------|--------------|--------|-----------|--------|
| REQ-014 | Unwanted | MISSING | 9 | add negative test for amount <= minimum |
| REQ-021 | State-driven | WEAK | 6 | add re-entry transition test |
| REQ-015 | Event-driven | WEAK | 4 | add "event did not occur" negative test |

### Legacy-derived edge cases still uncovered
- Boundary from a Natural program in `01-archaeology/legacy-sifap/natural-programs/` — confirm with the team, then map to REQ-014.

### Suggested test additions
1. `AmountRuleTest#should_reject_when_amount_below_minimum`
2. `StatusMachineTest#should_allow_reentry_after_exit`
```

## Definition of Done

- [ ] Every in-scope `REQ-ID` appears exactly once in the report
- [ ] Each gap has a risk score (probability × impact) and a one-line test recipe
- [ ] Negative / unwanted-behavior requirements without a negative test are marked `WEAK` or `MISSING`
- [ ] Legacy-derived edge cases are explicitly checked against `01-archaeology/legacy-sifap/natural-programs/`
- [ ] The top three gaps carry actionable test names ready for assignment
- [ ] The output is ready to paste into a sprint-planning ticket

## Prompt Body

You are the `@qa-engineer` auditing whether requirements are truly verified. Follow the pyramid and coverage philosophy in [`../skills/test-strategy/SKILL.md`](../skills/test-strategy/SKILL.md).

**Step 1 — Build the requirements inventory.**
Parse `spec.md` and extract each `REQ-ID` with its EARS pattern and acceptance criteria.

**Step 2 — Find tests by REQ-ID.**
Grep the test sources for `REQ-NNN`, `@Tag("REQ-NNN")`, `@implements REQ-NNN`, `describe('REQ-NNN', ...)`, and naming conventions such as `Req014_*`. Cross-check the `spec-traceability` job in `.github/workflows/spec-quality.yml`, which already lists `REQ-ID`s declared in `specs/` but not referenced by tests.

**Step 3 — Map test to requirement.**
For each `REQ-ID`, list the covering tests and rate it: `MISSING` (none), `WEAK` (only one happy-path test), or `OK` (happy path plus at least one boundary or error case).

**Step 4 — Inspect EARS variants for hidden cases.**
Event-driven and unwanted-behavior (`If ...`) requirements almost always need a negative test. State-driven (`While ...`) requirements need a transition test. Flag any that lack one.

**Step 5 — Cross-check the legacy system.**
For requirements mapped to a Natural program in `01-archaeology/legacy-sifap/natural-programs/`, confirm that the edge cases the team identified in Stage 1 are covered. Reference paths generically — do not assert what a specific program computes.

**Step 6 — Score by risk.**
Rate probability (how often it runs in production) and impact (financial, regulatory, security) on a 1–3 scale. Risk = probability × impact. Put the highest risk first.

**Step 7 — Deliver the prioritized gap list.**
Include a one-line recipe per gap — the shape of the missing test, not the test code — and actionable names for the top three.

Report requirement coverage, never a bare line-coverage number. A `REQ-ID` with five "should work" tests and zero "should not" tests is `WEAK`. Every gap carries a risk score. Never invent a requirement or a legacy edge case — flag the unknown and ask the team.

## Invocation Example

```
/coverage-gaps feature=<NNN>-<feature> scope=all
```
