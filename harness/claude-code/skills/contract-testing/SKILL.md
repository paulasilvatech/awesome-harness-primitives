---
name: contract-testing
description: >-
  Design consumer-driven contract tests with Pact or provider schema verification so services can
  deploy independently without integration-wide end-to-end suites. Use when the user asks about
  contract testing, Pact, consumer-driven contracts, breaking API changes between services,
  provider verification, a contract broker, or can-i-deploy checks in CI.
license: MIT
---

<!-- Generated from harness/github-copilot/skills/contract-testing/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Contract testing

Replace slow, flaky cross-service end-to-end suites with fast tests that prove a consumer and a provider still agree on the messages they exchange.

## When to invoke

- "Set up Pact between our services."
- "How do we stop the provider from breaking consumers?"
- "Can we deploy this service independently?"
- "Our end-to-end suite is too slow and flaky."
- "Add provider verification to CI."

## What a contract test actually proves

A contract test verifies **the interaction between two services**, not the behavior of either one.

| Test type | Proves | Does not prove |
| --- | --- | --- |
| Unit | Internal logic | Anything about integration |
| Contract | Consumer and provider agree on request and response shape | That the business outcome is correct |
| End-to-end | A real flow works | Which service caused a failure |

Contract tests do not replace unit tests or a small end-to-end smoke suite. They replace the large, brittle middle layer.

## Consumer-driven flow

The consumer states what it actually uses. The provider proves it still delivers that.

1. **Consumer test runs** against a mock provider and records expectations.
2. **A pact file is produced** describing each request and expected response.
3. **The pact is published** to a broker, tagged with branch and version.
4. **Provider verification replays** every interaction against the real provider.
5. **`can-i-deploy` gates the release** by checking verification results for the target environment.

```javascript
// Consumer expectation: only the fields this consumer reads
await provider.addInteraction({
  state: 'user 42 exists',
  uponReceiving: 'a request for user 42',
  withRequest: { method: 'GET', path: '/users/42' },
  willRespondWith: {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
    body: { id: like(42), email: like('a@b.com') },
  },
});
```

Use matchers such as `like` for types rather than exact literals. Asserting exact values couples the contract to fixture data and produces false failures.

## Provider states

Each interaction declares the precondition it needs. The provider implements a handler that establishes it.

- Keep state handlers **fast and isolated**; they run once per interaction.
- Set up data through the fastest safe path, not through the public API.
- Never let one state handler depend on another having run first.

## Only specify what you consume

The strongest rule in contract testing: a consumer must assert **only the fields it actually reads**.

Over-specifying makes the provider unable to add fields without breaking a consumer that never used them. That converts an additive, backward-compatible change into a false breakage and destroys trust in the suite.

## CI integration

| Stage | Action | Gate |
| --- | --- | --- |
| Consumer build | Run consumer tests, publish pact with version and branch tag | Fail on consumer test failure |
| Provider build | Verify all pacts for relevant tags, publish results | Fail on unverified interaction |
| Either deploy | Run `can-i-deploy` for the target environment | Block deploy when incompatible |

Publish verification results back to the broker. Without them, `can-i-deploy` has no evidence and either blocks everything or nothing.

## Limits

- Do not use contract testing for **performance, authorization depth, or business-rule correctness**; those need their own tests.
- Do not use it to test a third-party API you do not control; you cannot run provider verification there. Use recorded integration tests instead.
- Do not use it as the only integration signal for **asynchronous flows** without also verifying message ordering and delivery semantics.

## Gotchas

- **A pact is not an API specification.** It captures only observed interactions from real consumers, so it is deliberately incomplete.
- **Unpublished verification results silently disable the gate.** Confirm results reach the broker.
- **Branch and tag hygiene drives correctness.** Verifying only `main` while deploying a feature branch proves nothing about that branch.
- **Exact-value matchers create false failures.** Prefer type matchers except where the exact value is genuinely part of the contract.
- **Removing a consumer does not remove its pact.** Stale pacts block providers; retire them deliberately.

## Output template

```markdown
## Contract testing result

**Status:** verified | broken-contract | not-configured
**Summary:** <consumer, provider, and the outcome>

### Details
| Interaction | Provider state | Result |
| --- | --- | --- |
| <description> | <state> | <pass or fail with reason> |

Broker: <where pacts and results are published>
Deploy gate: <can-i-deploy outcome for the target environment>

### Validation
- Consumer asserts only consumed fields: <checked and result>
- Verification results published: <checked and result>
```

## Quality gate

- [ ] The consumer asserts only fields it actually reads.
- [ ] Type matchers are used except where an exact value is part of the contract.
- [ ] Every interaction has a fast, isolated provider state handler.
- [ ] Pacts are published with meaningful version and branch tags.
- [ ] Provider verification results are published back to the broker.
- [ ] A deploy gate consults verification results for the target environment.
- [ ] Scope boundaries are stated; contract tests are not presented as end-to-end proof.

## References

- [Pact documentation](https://docs.pact.io/)
- [Pact Broker](https://docs.pact.io/pact_broker)
- [can-i-deploy](https://docs.pact.io/pact_broker/can_i_deploy)
