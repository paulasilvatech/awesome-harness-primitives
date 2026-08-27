---
name: mutation-testing
description: >-
  Measure whether a test suite actually detects defects by injecting mutants with Stryker, PIT,
  mutmut, or Cosmic Ray, reading survived mutants, and fixing weak assertions. Use when the user
  asks about mutation testing, mutation score, whether tests are meaningful, why high line
  coverage still misses bugs, or how to prove a suite has real assertion strength.
license: MIT
---

<!-- Generated from harness/github-copilot/skills/mutation-testing/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Mutation testing

Prove a test suite detects defects instead of merely executing lines. Mutation testing changes the code on purpose and reports which changes the tests failed to catch.

## When to invoke

- "Our coverage is 90% but bugs still ship."
- "Are these tests actually testing anything?"
- "Set up Stryker / PIT / mutmut."
- "What is a good mutation score?"
- "Prove this test suite is meaningful before we refactor."

## Why line coverage is not enough

Coverage counts execution. It does not check assertions.

```python
def apply_discount(price, pct):
    return price * (1 - pct / 100)

def test_discount():
    apply_discount(100, 10)   # 100% line coverage, zero assertions
```

That test covers every line and detects nothing. Mutation testing exposes it immediately: change `-` to `+`, and the test still passes, so the mutant survives.

## How it works

1. The tool generates **mutants**: small semantic changes such as `>` to `>=`, `+` to `-`, `true` to `false`, or removing a statement.
2. The suite runs against each mutant.
3. A mutant that causes a test failure is **killed**. One that does not is **survived**.
4. **Mutation score** = killed / (total − equivalent).

A survived mutant is a concrete, reproducible gap: this exact change to production code would ship undetected.

## Tooling

| Language | Tool | Notes |
| --- | --- | --- |
| JavaScript, TypeScript | Stryker | Works with Jest, Vitest, Karma, Mocha |
| Java, Kotlin, JVM | PIT | Bytecode mutation; fast on large suites |
| Python | mutmut, Cosmic Ray | mutmut is simpler; Cosmic Ray is more configurable |
| C# and .NET | Stryker.NET | Integrates with dotnet test |

## Making it affordable

Mutation testing is expensive: the suite runs once per mutant. Naive use on a large repository is impractical.

- **Scope to changed files.** Run incrementally on the diff in pull requests, full runs on a schedule.
- **Require a fast, reliable suite first.** Flaky or slow tests multiply into an unusable run.
- **Exclude generated code, DTOs, and boilerplate** where mutants carry no signal.
- **Use the tool's incremental cache** so unchanged files are not re-analyzed.
- **Parallelize** across cores or CI shards.

## Reading survived mutants

Never chase the score. Read the mutants.

| Survived mutant means | Correct response |
| --- | --- |
| A missing assertion | Add the assertion that would have caught it |
| A missing boundary case | Add the boundary test |
| Genuinely unreachable or equivalent behavior | Mark as equivalent and record why |
| Dead or unnecessary code | Delete the code |

Each survivor is a question: *if this line were wrong in this way, would anyone notice?*

## Equivalent mutants

Some mutants change code without changing observable behavior, so no test can kill them. Example: altering a value that is later overwritten unconditionally.

Equivalent mutants are undecidable in general. Review them, exclude them deliberately with a recorded reason, and never treat 100% as an achievable target.

## Setting a target

Do not adopt an arbitrary number. Establish a baseline, then require that the score does not regress and that new code meets a higher bar than legacy code. A rising score on changed files is a stronger signal than any fixed threshold.

## Gotchas

- **Chasing the score corrupts the suite.** Tests written to kill mutants rather than express behavior become unreadable and brittle.
- **Flaky tests poison the result.** A flaky failure marks a mutant killed by accident, inflating the score.
- **Timeouts are not kills by default in every tool.** Confirm how your tool classifies a mutant that causes an infinite loop.
- **A high score on trivial code proves little.** Weight attention toward business logic.
- **It cannot detect missing features.** Mutation testing only mutates code that exists.

## Output template

```markdown
## Mutation testing result

**Status:** improved | regressed | baseline-established
**Summary:** <scope analyzed and headline score>

### Details
| Metric | Value |
| --- | --- |
| Mutants generated | <n> |
| Killed | <n> |
| Survived | <n> |
| Equivalent (excluded) | <n with reason> |
| Mutation score | <percent> |

Notable survivors:
- <file:line> — <mutation> — <what this reveals about the tests>

### Validation
- Suite stability confirmed before run: <checked and result>
- Scope and exclusions: <what was analyzed and what was skipped>
```

## Quality gate

- [ ] The test suite was stable and passing before the mutation run.
- [ ] Scope and exclusions are explicit, with reasons.
- [ ] Survived mutants are analyzed individually, not summarized only as a score.
- [ ] Each new or changed test expresses intended behavior, not mutant-chasing.
- [ ] Equivalent mutants are recorded with justification.
- [ ] The target is a non-regression baseline rather than an arbitrary fixed number.
- [ ] Runtime cost and the incremental strategy are stated.

## References

- [Stryker Mutator](https://stryker-mutator.io/docs/)
- [PIT mutation testing](https://pitest.org/)
- [mutmut](https://mutmut.readthedocs.io/)
- [Cosmic Ray](https://cosmic-ray.readthedocs.io/)
