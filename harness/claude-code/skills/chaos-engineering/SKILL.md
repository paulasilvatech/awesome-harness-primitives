---
name: chaos-engineering
description: >-
  Design and run controlled resilience experiments with a steady-state hypothesis, limited blast
  radius, and an abort condition, covering fault injection, dependency failure, latency, and game
  days. Use when the user asks about chaos engineering, fault injection, resilience testing,
  failure injection experiments, game days, or proving a system survives dependency loss.
license: MIT
---

<!-- Generated from harness/github-copilot/skills/chaos-engineering/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Chaos engineering

Run disciplined experiments that reveal how a system behaves under failure, with a stated hypothesis, a bounded blast radius, and a way to stop.

## When to invoke

- "Run a chaos experiment on this service."
- "What happens if the database goes away?"
- "Plan a game day for the platform team."
- "Inject latency into this dependency."
- "Prove our failover actually works."

## Chaos is an experiment, not breakage

An experiment without a hypothesis is just an outage you caused.

Every experiment states:

1. **Steady state** — a measurable business or system metric that indicates health, such as checkout success rate.
2. **Hypothesis** — what you believe stays true during the fault, in measurable terms.
3. **Fault** — the specific, minimal condition you inject.
4. **Blast radius** — who and what can possibly be affected.
5. **Abort condition** — the observable trigger that stops the experiment immediately.

If any of the five is missing, do not run it.

## Prerequisites

Chaos engineering finds unknown weaknesses. Running it before the basics wastes an outage.

- **Observability first.** If you cannot see the steady state in real time, you cannot detect the impact or abort in time.
- **Known failures fixed first.** Do not inject faults while a known single point of failure is already unaddressed.
- **On-call awareness.** The responders must know an experiment is running, or you will trigger a real incident response.
- **A tested rollback.** The stop mechanism must be verified before the fault is applied.

## Fault categories

| Category | Example fault | Reveals |
| --- | --- | --- |
| Resource | CPU, memory, or disk pressure | Limits, autoscaling, noisy-neighbor effects |
| Network | Latency, packet loss, partition | Timeouts, retries, circuit breakers |
| Dependency | Service returns errors or hangs | Fallbacks, bulkheads, cascading failure |
| State | Node or pod termination | Replication, leader election, graceful shutdown |
| Time | Clock skew, certificate expiry | Token validation, scheduled jobs |

Start with **dependency latency**. It is the fault most systems handle worst and it is usually the safest to inject and reverse.

## Blast radius discipline

Expand only after each stage passes.

1. One instance in a non-production environment.
2. A small percentage of production traffic, ideally internal users.
3. A single availability zone or shard.
4. Broader production scope, only with prior results.

Never begin at stage 4 because earlier stages were "obvious".

## Timeouts, retries, and the failure you cause

Most cascading failures come from the resilience code itself.

- **A missing timeout turns a slow dependency into total outage.** Every network call needs one.
- **Naive retries amplify load** exactly when the dependency is weakest. Use exponential backoff with jitter and a retry budget.
- **Retry storms are self-inflicted denial of service.** Verify aggregate retry volume during latency experiments.
- **Circuit breakers must actually open.** Confirm the threshold triggers under the injected fault rather than assuming it.

## Game days

A game day is a scheduled, human-in-the-loop exercise, not automated injection.

- Announce scope, time window, and the abort owner in advance.
- Assign an observer to record timeline and decisions as they happen.
- Test the **human path** too: alert routing, runbook accuracy, escalation, and communication.
- Debrief blamelessly. Findings become tracked work items, not folklore.

## Limits

- Do not run chaos experiments to satisfy a compliance checkbox without acting on findings.
- Do not inject faults in production without approval, an abort owner, and stakeholder awareness.
- Do not use chaos engineering to discover capacity limits; use a stress test for that.
- Do not run experiments during a live incident, a change freeze, or a peak business event.

## Gotchas

- **The abort mechanism can fail with the system.** Verify it works independently of the component under test.
- **Automated remediation can mask the finding.** Know whether self-healing hid the impact you were measuring.
- **Steady-state metrics can lag.** A one-minute aggregation window can end the experiment before the metric moves.
- **Customer impact may be invisible in system metrics.** Watch business metrics, not only CPU and error counts.
- **A passing experiment proves one hypothesis under one condition.** It does not prove general resilience.

## Output template

```markdown
## Chaos experiment result

**Status:** hypothesis-held | weakness-found | aborted
**Summary:** <fault injected and what happened to steady state>

### Details
| Element | Value |
| --- | --- |
| Steady-state metric | <metric and healthy range> |
| Hypothesis | <what should stay true> |
| Fault injected | <specific fault and magnitude> |
| Blast radius | <scope and duration> |
| Abort condition | <trigger and whether it fired> |

Observed impact: <what actually happened, with timestamps>
Findings: <weaknesses discovered, each as a tracked item>

### Validation
- Abort mechanism verified before injection: <checked and result>
- On-call notified: <checked and result>
```

## Quality gate

- [ ] Steady state, hypothesis, fault, blast radius, and abort condition are all defined before running.
- [ ] Observability can show the steady state in real time.
- [ ] The abort mechanism was verified and does not depend on the component under test.
- [ ] On-call and stakeholders were notified for any production experiment.
- [ ] Blast radius started small and expanded only after prior stages passed.
- [ ] Findings are recorded as tracked work items, not narrative only.
- [ ] Conclusions are limited to the hypothesis actually tested.

## References

- [Principles of Chaos Engineering](https://principlesofchaos.org/)
- [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html)
- [Azure Chaos Studio](https://learn.microsoft.com/en-us/azure/chaos-studio/chaos-studio-overview)
- [Chaos Mesh](https://chaos-mesh.org/docs/)
