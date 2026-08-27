---
name: test-data-management
description: >-
  Build reliable test data with factories, fixtures, deterministic seeding, per-test isolation,
  and safe anonymization of production data for realistic datasets. Use when the user asks about
  test data, fixtures, factories, flaky tests caused by shared state, seeding a test database,
  parallel-safe data, or anonymizing production data for testing.
license: MIT
---

<!-- Generated from harness/github-copilot/skills/test-data-management/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Test data management

Give every test the data it needs, isolated from every other test, without copying sensitive production records into lower environments.

## When to invoke

- "Our tests fail when run in parallel."
- "Set up factories instead of these fixture files."
- "How do we get realistic data into staging?"
- "Tests pass alone but fail in the suite."
- "Anonymize this production dump for testing."

## Factories over shared fixtures

Shared fixture files create hidden coupling: one test's expectations depend on data another test also uses, so any change breaks unrelated tests.

```python
# Factory: each test states only what it cares about
def make_order(**overrides):
    return Order(**{
        "id": uuid4(),
        "status": "pending",
        "total": Decimal("10.00"),
        "created_at": FIXED_CLOCK,
        **overrides,
    })

def test_refund_rejected_when_already_refunded():
    order = make_order(status="refunded")   # intent is visible in the test
```

The test declares the one attribute that matters. Everything else is a sane default that can change without touching this test.

## Isolation strategy

Pick one and apply it consistently.

| Strategy | How it works | Trade-off |
| --- | --- | --- |
| Transaction rollback | Wrap each test, roll back after | Fastest; cannot test committed behavior or multi-connection flows |
| Reset and reseed | Clear tables between tests, then reload a known baseline | Simple and thorough; slower as the schema grows |
| Unique namespacing | Every record uses a run-scoped identifier | Parallel-friendly; requires discipline everywhere |
| Ephemeral database | Fresh container per run | Strongest isolation; highest startup cost |

For parallel suites, transaction rollback or unique namespacing usually wins. Clearing shared tables across workers causes cross-test data loss.

## Determinism

Non-deterministic data is the most common source of flaky tests.

- **Seed random generators explicitly** and log the seed so a failure is reproducible.
- **Inject the clock.** Never call `now()` inside code under test; pass a fixed instant.
- **Avoid `today` boundaries.** A test that passes except near midnight or year end is already broken.
- **Do not rely on insertion order.** Assert with an explicit sort or compare as a set.
- **Beware of locale and timezone.** Fix them for the test run or assert locale-independent values.

## Parallel safety

- Namespace every externally visible identifier with a worker or run token so two workers cannot collide on a unique constraint.
- Never share a mutable account, tenant, or queue between workers.
- Give each worker its own schema, database, or key prefix when the store does not support transactional isolation.
- Confirm cleanup runs even when a test fails, or a failure leaks state into later tests.

## Anonymizing production data

Copying production data into a lower environment is a data-protection decision, not a convenience.

- **Prefer synthetic data.** If generated data can exercise the case, do not copy real records at all.
- **Anonymize at export, never after load.** A raw copy that lands in staging has already leaked.
- **Masking is not anonymization.** Replacing a name while keeping a rare postcode, birth date, and diagnosis still identifies the person.
- **Preserve referential integrity and distribution.** Transform consistently so joins still work and shapes stay realistic.
- **Remove or tokenize direct identifiers**, and reduce quasi-identifiers that re-identify in combination.
- **Never copy secrets.** Credentials, tokens, and keys must be regenerated, not masked.
- **Record the legal basis and retention** for any derived dataset, and expire it.

Verify the result: attempt re-identification on a sample before approving the dataset.

## Gotchas

- **Cleanup that only runs on success leaks state.** Use fixtures or teardown hooks that always run.
- **Cascading deletes can silently remove another test's data** in a shared database.
- **Auto-increment identifiers differ between local and CI**, so never assert on a specific numeric id.
- **A large seed dataset hides missing setup.** Tests appear to pass because unrelated data happens to satisfy them.
- **Anonymized data can still be unique.** A single outlier value can identify a person even with names removed.

## Output template

```markdown
## Test data result

**Status:** implemented | improved | blocked
**Summary:** <what changed about data creation or isolation>

### Details
| Aspect | Approach |
| --- | --- |
| Creation | <factories, fixtures, or seed> |
| Isolation | <transaction, reset, namespace, or ephemeral> |
| Determinism | <clock injection, seeding, ordering> |
| Parallel safety | <namespacing and shared-resource handling> |

Production-derived data: <none, or anonymization method and legal basis>

### Validation
- Suite passes in parallel: <checked and result>
- Cleanup runs on failure: <checked and result>
```

## Quality gate

- [ ] Tests declare only the data attributes they depend on.
- [ ] One isolation strategy is applied consistently across the suite.
- [ ] Clocks and random seeds are injected and reproducible.
- [ ] No assertion depends on generated identifiers or insertion order.
- [ ] Externally visible identifiers are namespaced for parallel runs.
- [ ] Cleanup executes even when a test fails.
- [ ] Any production-derived dataset was anonymized at export, verified against re-identification, and has a recorded legal basis and expiry.
- [ ] No credentials or secrets were copied from production.

## References

- [NIST SP 800-188: De-Identifying Government Datasets](https://csrc.nist.gov/pubs/sp/800/188/final)
- [GDPR Recital 26: anonymous information](https://gdpr-info.eu/recitals/no-26/)
- [Test Data Builder pattern](https://www.natpryce.com/articles/000714.html)
