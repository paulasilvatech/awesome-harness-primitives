---
name: load-performance-testing
description: >-
  Design and run load, stress, soak, and spike tests with k6, JMeter, Locust, or
  Gatling, define latency and error-rate thresholds, model realistic workloads,
  and interpret results without drawing unsupported conclusions. Use when the
  user asks to load test a service, find a breaking point, size capacity, set
  performance SLOs, tune a stress or soak profile, or explain latency percentiles.
license: MIT
---

# Load and performance testing

Turn a performance question into a workload model, an executable test with explicit pass/fail thresholds, and an interpretation that separates measured facts from inference.

## When to invoke

- "Load test this API before launch."
- "Find the breaking point of our checkout service."
- "How many users can this handle?"
- "Set up a soak test to catch memory leaks."
- "Our p99 latency looks bad, help me measure it properly."

## Choose the test type first

The question determines the profile. Running the wrong profile produces confident but meaningless numbers.

| Question | Profile | Shape |
| --- | --- | --- |
| Does it meet the SLO at expected traffic? | Load | Ramp to target, hold, ramp down |
| Where does it break? | Stress | Step up until failure, record the step |
| Does it degrade over hours? | Soak | Hold moderate load for hours |
| Can it survive a sudden surge? | Spike | Jump to peak instantly, observe recovery |
| What does one user cost? | Baseline | Single user, no contention |

Always run a baseline first. Without it you cannot separate contention from inherently slow code.

## Tool selection

| Tool | Language | Best fit | Trade-off |
| --- | --- | --- | --- |
| k6 | JavaScript | Scriptable CI-first testing, good thresholds model | No native browser workload; separate module needed |
| JMeter | GUI plus XML | Protocol breadth, teams wanting a GUI | Verbose plans; heavier per-VU cost on one node |
| Locust | Python | Complex conditional user behavior | Requires Python performance care in hot paths |
| Gatling | Scala or Java DSL | High throughput per node, expressive DSL | Steeper language ramp for non-JVM teams |

Pick the tool the team can maintain. A precise test nobody can edit is worse than a rough test they own.

## Threshold-driven tests

A test without thresholds cannot fail, so it cannot protect anything. Encode the SLO in the test.

```javascript
// k6: fail the run when the SLO is violated
export const options = {
  stages: [
    { duration: '2m', target: 100 },   // ramp
    { duration: '5m', target: 100 },   // hold
    { duration: '2m', target: 0 },     // ramp down
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],           // under 1% errors
    http_req_duration: ['p(95)<500', 'p(99)<1500'],
    checks: ['rate>0.99'],
  },
};
```

Set thresholds from the agreed SLO, not from the first result. Deriving the threshold from observed output only re-states current behavior.

## Workload modeling

Unrealistic load produces unusable data.

- **Think time.** Real users pause. Zero sleep turns 100 virtual users into a throughput far above 100 real users.
- **Data variety.** Reusing one ID makes every cache hit. Parameterize from a dataset.
- **Traffic mix.** Weight endpoints by production ratios, not by equal split.
- **Ramp, do not slam.** Except in a deliberate spike test, ramp so autoscaling and connection pools behave as in production.
- **Cold start.** Decide explicitly whether warm-up is in scope, then state it.

## Reading results honestly

- **Report percentiles, not averages.** An average hides the tail that users feel. Report p50, p95, p99, and max.
- **Check the error rate before the latency.** Fast responses that are all 500s look excellent on a latency chart.
- **Confirm the load generator was not the bottleneck.** Saturated CPU or exhausted ports on the client invalidate the run.
- **One variable per run.** Changing load and configuration together makes attribution impossible.
- **Correlate with server-side telemetry.** Client latency alone cannot distinguish network, queue, and compute time.

## Gotchas

- **The client can be the bottleneck.** Always record generator CPU, memory, and socket usage alongside results.
- **Shared environments invalidate comparisons.** Another tenant's load becomes your noise; state the environment and its isolation.
- **Connection reuse changes everything.** Keep-alive on or off can shift results by an order of magnitude.
- **DNS and TLS handshakes may dominate short tests.** Warm the pool or measure them deliberately.
- **Never load test production without written approval**, a blast-radius limit, and an abort trigger.

## Output template

```markdown
## Load test result

**Status:** met-slo | violated-slo | inconclusive
**Summary:** <profile, target load, and the headline outcome>

### Details
| Metric | Result | Threshold |
| --- | --- | --- |
| Requests/sec | <value> | <target> |
| p95 latency | <value> | <threshold> |
| p99 latency | <value> | <threshold> |
| Error rate | <value> | <threshold> |

Environment: <where it ran and how isolated>
Workload model: <think time, data variety, traffic mix>

### Validation
- Load generator saturation: <checked and result>
- Server-side telemetry correlation: <checked and result>
```

## Quality gate

- [ ] The test profile matches the question being asked.
- [ ] Thresholds come from an agreed SLO, not from observed output.
- [ ] A baseline single-user run exists for comparison.
- [ ] The workload model states think time, data variety, and traffic mix.
- [ ] Error rate was verified before latency was interpreted.
- [ ] Load generator saturation was ruled out.
- [ ] Environment and isolation are stated; unmeasured factors are called assumptions.
- [ ] Production testing, if any, had explicit approval and an abort trigger.

## References

- [k6 documentation](https://grafana.com/docs/k6/latest/)
- [Apache JMeter user manual](https://jmeter.apache.org/usermanual/index.html)
- [Locust documentation](https://docs.locust.io/en/stable/)
- [Gatling documentation](https://docs.gatling.io/)
