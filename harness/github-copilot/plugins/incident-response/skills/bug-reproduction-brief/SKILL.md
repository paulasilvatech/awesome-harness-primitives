---
name: "bug-reproduction-brief"
description: >-
  Turn vague, intermittent, or environment-specific bug reports into minimal evidence-backed reproductions before diagnosis or repair. Use when a bug report is incomplete, mixed with an assumed cause, hard to reproduce, or needs observed failure, environment, expected/actual behavior, repeatability, and safe next hypothesis.
---

# Bug reproduction brief

Reduce a reported bug to the smallest observable, repeatable, evidence-backed failure before proposing a root cause or editing implementation code.

## When to invoke

- "Reproduce this bug before fixing it."
- "Turn this intermittent failure into a minimal reproduction."
- "Write a bug reproduction brief for checkout."
- "Separate expected and actual behavior from the suspected cause."
- "Prove this environment-specific bug with command evidence."

## Evidence to capture

| Area | Record | Avoid |
| --- | --- | --- |
| Observed failure | Exact error, incorrect output, timestamp, affected route or command, smallest known input. | Paraphrasing, screenshots without text when logs exist. |
| Logs | Relevant lines with secrets and personal data removed. | Secrets, customer records, private data, environment variables. |
| Environment | Repository and commit, runtime and package-manager versions, OS or container, lockfile, feature flags, local/test/staging/production target. | Guessed credentials or production configuration. |
| Expected vs actual | Two observable statements. | Suspected cause or implementation theory. |
| Repeatability | Commands, outputs, run count, frequency, and duration. | Calling intermittent failures deterministic without evidence. |

Use this exact separation:

```text
Expected: [observable result]
Actual:   [observable result, including status or error]
```

## Procedure

1. Record the observed failure exactly as reported or observed. Label second-hand descriptions as unverified.
2. Identify the environment from inspectable facts only.
3. Write explicit expected and actual behavior statements.
4. Start from the reported path, command, or route.
5. Remove unrelated data, services, and steps one at a time.
6. When the failure stops, restore the last removed condition and record it as necessary.
7. Prefer an isolated test, minimal script, or smallest safe request over reproducing against production.
8. Run the minimal reproduction at least twice where safe.
9. If intermittent, report observed frequency and duration.
10. Stop before repair; the deliverable is the verified reproduction brief.

## Safety boundaries

- Do not change production data merely to reproduce a bug.
- Do not publish secrets, customer records, private source, credentials, or environment variables.
- Do not claim a root cause from correlation alone.
- Use read-only or reversible discovery first.
- Do not edit implementation code while building the brief because that can destroy evidence or mix diagnosis with remediation.
- Stop after a verified reproduction; diagnosis and repair are separate workflows.

## Reduction patterns

| Report shape | Reduction tactic |
| --- | --- |
| Failing test suite | Run the smallest test selector that still fails, then reduce fixtures. |
| API or route bug | Capture the smallest safe request, headers without secrets, status, and body. |
| CLI bug | Preserve command, arguments, working directory, exit code, stdout, and stderr. |
| Intermittent behavior | Run repeated attempts with timestamps and count pass/fail frequency. |
| Environment-specific failure | Compare inspectable versions, lockfile, feature flags, OS/container, and target tier. |

## Examples

### Good

**Input:** "The checkout test fails sometimes; reproduce but do not fix."

**Expected behavior:** Produce a brief with exact command evidence, expected result, actual error, run count, frequency if intermittent, and unknowns.

### Bad

**Input:** "The checkout test fails because the cache is stale; fix the cache."

**Incorrect behavior:** Editing cache code before proving the smallest failure. Correct by first writing the reproduction brief and labeling the cache claim as an unverified hypothesis.

## Output template

```markdown
# Bug Reproduction Brief

- Target and commit:
- Environment:
- Expected:
- Actual:
- Minimal steps:
- Minimal fixture:
- Reproduced: yes / no / intermittent
- Evidence:
- Unknowns:
- Safe next hypothesis to test:
```

## Quality gate

- [ ] The observed failure includes exact error, incorrect output, timestamp, route or command, and smallest known input when available.
- [ ] Environment facts are inspectable and include repository, commit, runtime, package manager, OS/container, lockfile, feature flags, and target tier when relevant.
- [ ] Expected and actual behavior are observable and do not include suspected causes.
- [ ] The reproduction was reduced by removing unrelated steps until the smallest failing condition remained.
- [ ] The minimal reproduction was run at least twice where safe, or intermittent frequency and duration were reported.
- [ ] No production data was changed and no secrets or personal data were published.
- [ ] No implementation code was edited before the brief was delivered.

## References

- [AI agent skill preview workflow](https://github.com/skyestrela/ai-agent-skill-preview.)
