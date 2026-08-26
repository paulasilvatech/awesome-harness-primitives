---
name: "fix-bug"
description: "Reproduce, isolate, and fix a defect with a regression test, keeping spec.md the source of truth."
argument-hint: "bug=<observed-vs-expected> req=REQ-NNN area=<service-or-page>"
agent: "implementer"
tools: ["read", "search", "edit", "execute"]
---
# /fix-bug

## Objective

Fix a defect so that the fix is (a) reproducible with a new failing test, (b) the smallest change that makes that test pass, and (c) traceable to a real `REQ-ID`—an existing one, or a new one proposed through `/update-spec` when the bug reveals a missing requirement. The root cause is named, not patched over.

> [!WARNING]
> SIFAP must fail explicitly. Never wrap a defect in a catch-and-continue that logs the error and swallows it.

## When to Invoke

When a defect is reported against code already merged to `develop`, and the team wants a root-cause fix with a regression test rather than a symptom patch. Run it on an `impl/<NNN>-<bug-name>` branch cut from `develop`.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` exists for the affected area, to confirm the intended behavior
- The current branch is `impl/<NNN>-<bug-name>`
- The failing scenario is described well enough to reproduce, or the reporter is reachable
- The affected `backend/` or `frontend/` module has already been scaffolded

## Inputs the Team Must Provide

- A bug description: observed vs. expected behavior, exact steps, and environment
- A stack trace, log line, or screenshot, if available
- The affected service or page
- The likely related `REQ-ID` (or "unknown—please investigate")
- Ask the user for any missing item before starting.

## What I Will Do

- Reproduce the defect locally, or write the smallest test that mirrors the report
- Write the regression test before touching production code and confirm it fails for the right reason
- Diagnose the root cause by reading the code, tracing the call stack, and checking the spec
- Map the corrected behavior to an existing `REQ-ID`, or propose a new EARS requirement
- Apply the smallest fix, add one boundary test, and run the full local suite

## What I Will NOT Do

- Fix the symptom—catch the exception, swallow the null, or wrap the bug in a try/catch that logs and continues
- Ship a fix without a regression test
- Refactor the surrounding class "while here"—that is a separate `/refactor`
- Silently change behavior when the spec is ambiguous—I propose a spec update instead
- Change the schema (that is `/migration`, routed through the DBA)
- Invent a root cause I cannot demonstrate—if I cannot reproduce the defect, I stop and say what is missing

## Output Format

```markdown
### Root cause
Two `BigDecimal` values were compared with `equals`, so `10.00` and `10` never matched and the
exemption branch was skipped for scale-0 inputs. Three to five sentences, in plain language.

### Linked requirement
REQ-031 (existing) — or "PROPOSED: new REQ-XXX; see /update-spec".

### Regression + boundary tests
<complete test source, each test with an inline `// REQ-031` comment>

### Fix
<minimal production diff>

### Risk assessment
Touches the shared fee calculator used by intake and reconciliation; both paths were retested.

### Commit message
fix(fees): compare BigDecimal by value, not scale (REQ-031)

Root cause: equals() is scale-sensitive on BigDecimal. Adds a regression test.
Refs: BUG-42, REQ-031
```

## Definition of Done

- [ ] A new test fails before the fix and passes after it, carrying an inline `// REQ-NNN` comment
- [ ] The root cause is named in the commit message and the PR description
- [ ] The fix is the smallest change that makes the test pass
- [ ] At least one boundary test is added in addition to the reproduction case
- [ ] An existing `REQ-ID` is cited, or a new one is formally proposed via `/update-spec`
- [ ] No unrelated files are modified
- [ ] The full suite passes: `./mvnw verify` (backend) or `pnpm test && pnpm lint && pnpm typecheck` (frontend)

## Prompt Body

You are the `@implementer`. A defect was reported and the team wants a root-cause fix with a regression test. Read [`tdd-workflow`](../skills/tdd-workflow/SKILL.md); the same red-green discipline applies to bug fixes.

**Step 1 — Reproduce locally first.**
Run the failing scenario, or write the smallest test that mirrors the report. If you cannot reproduce it, stop and tell the user exactly what is missing.

**Step 2 — Write the regression test.**
Before changing any code, add a test named `should_<expected>_when_<condition>` in the same package as the code under test, with an inline `// REQ-NNN` comment. Confirm it fails, and read the assertion to confirm it fails for the right reason—fix the setup first if it does not.

**Step 3 — Diagnose the root cause.**
Read the related code, trace the call stack, and compare against `spec.md`. Write three to five plain-language sentences explaining the cause before showing any fix. Do not patch blindly.

**Step 4 — Map the fix to a requirement.**
If an existing `REQ-ID` covers the correct behavior, cite it. Otherwise draft a new EARS requirement and propose it through `/update-spec`—never silently change behavior.

**Step 5 — Apply the smallest fix.**
Change only what the failing test needs. Leave unrelated cleanup as a `// TODO(REQ-XXX)` or a follow-up issue.

**Step 6 — Add a boundary test.**
A happy-path test is not enough. Add an edge case: null, empty, maximum value, or off-by-one.

**Step 7 — Run the full suite.**
Run `./mvnw verify` or `pnpm test && pnpm lint && pnpm typecheck`. Do not finish until it is green.

Mask CPF and benefit amounts in any log line. If the bug exposes an ambiguous or missing requirement, escalate it to the spec; do not decide the business rule yourself.

## Invocation Example

```
/fix-bug bug="an exempt payer is still charged a fee" req=REQ-031 area=fee-service
```
