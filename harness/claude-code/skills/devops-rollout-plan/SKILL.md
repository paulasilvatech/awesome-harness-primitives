---
name: devops-rollout-plan
description: >-
  Generate production-ready DevOps rollout plans for infrastructure, application, configuration,
  and data changes, including preflight checks, phased deployment, verification signals, rollback
  procedures, communication plan, contingency handling, and post-deployment tasks. Use when the
  user asks for a rollout plan, deployment plan, release plan, production change plan, or go/no-go
  checklist.
---

<!-- Generated from harness/github-copilot/skills/devops-rollout-plan/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# DevOps rollout plan

Create a comprehensive step-by-step rollout plan that turns a proposed infrastructure or application change into a preflighted, observable, reversible production deployment with communication, rollback, and contingency paths.

## When to invoke

- "Generate a rollout plan for this deployment."
- "Create a production change plan."
- "Write preflight checks, rollout steps, verification, and rollback."
- "Plan this Kubernetes, VM, serverless, or container release."
- "Prepare a go/no-go checklist for an infrastructure change."

## Inputs

Use `$ARGUMENTS` as the change description, environment, or target system when provided. If details are missing, collect enough to avoid a generic plan.

| Input group | Required details |
| --- | --- |
| Change Description | What's changing: infrastructure, application, configuration; version or state transition from/to; problem solved or feature added. |
| Environment Details | Target environment: dev, staging, production, all; infrastructure type: Kubernetes, VMs, serverless, containers; affected services and dependencies; current capacity and scale. |
| Constraints & Requirements | Acceptable downtime window, change window restrictions, approval requirements, regulatory or compliance considerations. |
| Risk Assessment | Blast radius, data migrations or schema changes, rollback complexity and safety, known risks. |

## Rollout structure

| Section | Required content |
| --- | --- |
| Executive Summary | What, why, when, duration, risk level, rollback time, affected systems, user impact, expected downtime. |
| Prerequisites & Approvals | Technical lead, security, compliance, business approvals; resources, capacity, backups, monitoring, rollback automation; pre-deployment backups. |
| Preflight Checks | Infrastructure health, application health baseline, dependencies, monitoring baseline metrics, go/no-go checklist. |
| Step-by-Step Rollout Procedure | Phases for pre-deployment, deployment, progressive verification; specific commands, validation after each step, duration estimates. |
| Verification Signals | Immediate, short-term, medium-term, and long-term checks. |
| Rollback Procedure | Decision criteria, automated or manual rollback steps, infrastructure revert or full restore, post-rollback verification, stakeholder notification. |
| Communication Plan | T-24h notice, deployment start, periodic progress updates, completion, rollback notice. |
| Post-Deployment Tasks | Immediate 1h, short-term 24h, medium-term 1 week review and lessons learned. |
| Contingency Plans | Partial failure, performance degradation, data inconsistency, dependency failure. |
| Contact Information | Primary and secondary on-call, escalation path, emergency contacts for infrastructure, security, database, networking. |

## Verification windows

| Window | Time | Signals |
| --- | --- | --- |
| Immediate | 0-2 min | Deployment success, pods/containers started, health checks passing. |
| Short-term | 2-5 min | Application responding, error rates acceptable, latency normal. |
| Medium-term | 5-15 min | Sustained metrics, stable connections, integrations working. |
| Long-term | 15+ min | No degradation, capacity healthy, business metrics normal. |

## Customization rules

| Dimension | Adaptation |
| --- | --- |
| Infrastructure Type | Kubernetes plans include pods, rollout status, readiness/liveness probes, node capacity; VMs include image/version, service restart, health endpoint; serverless includes function versions, aliases, cold start, trigger health; databases include backups, migrations, locks, replication lag. |
| Risk Level | Low risk gets simplified gates; medium risk gets standard preflight, canary, rollback; high risk gets additional approvals, dry run, checkpoint, and explicit abort criteria. |
| Change Type | Code deployment, infrastructure, configuration, and data migration need different validation and rollback mechanics. |
| Environment | Production uses the full plan; staging can be simplified; development is minimal but still verifies success. |

## Rollout principles

- Always have a tested rollback plan.
- Communicate early and often.
- Monitor metrics, not just logs.
- Document everything.
- Learn from each deployment.
- Never deploy on Friday afternoon unless the change is critical.
- Never skip verification steps.
- Never assume "it should work".

## Output template

```markdown
# Rollout Plan: <change name>

## 1. Executive Summary
- What: <change>
- Why: <reason>
- When: <window>
- Duration: <estimate>
- Risk level: low | medium | high
- Rollback time: <estimate>
- Affected systems: <systems>
- User impact / expected downtime: <impact>

## 2. Prerequisites & Approvals
| Requirement | Owner | Status |
| --- | --- | --- |
| Technical lead approval | <name> | pending |

## 3. Preflight Checks
- [ ] Infrastructure health baseline captured.
- [ ] Application health baseline captured.
- [ ] Dependencies available.
- [ ] Monitoring baseline metrics captured.
- [ ] Go/no-go decision recorded.

## 4. Step-by-Step Rollout Procedure
| Phase | Step | Command/action | Validation | Duration |
| --- | --- | --- | --- | --- |
| Pre-deployment | <step> | `<command>` | <signal> | <time> |

## 5. Verification Signals
| Window | Signals | Pass criteria |
| --- | --- | --- |
| Immediate (0-2 min) | deployment, pods/containers, health checks | <criteria> |
| Short-term (2-5 min) | response, error rate, latency | <criteria> |
| Medium-term (5-15 min) | sustained metrics, connections, integrations | <criteria> |
| Long-term (15+ min) | degradation, capacity, business metrics | <criteria> |

## 6. Rollback Procedure
**Decision criteria:** <when to rollback>
**Steps:** <automated/infrastructure/full restore steps>
**Post-rollback verification:** <checks>
**Communication:** <notification>

## 7. Communication Plan
| Time | Audience | Channel | Message |
| --- | --- | --- | --- |
| T-24h | <stakeholders> | <channel> | <notice> |

## 8. Post-Deployment Tasks
- Immediate (1h): <tasks>
- Short-term (24h): <tasks>
- Medium-term (1 week): <tasks>

## 9. Contingency Plans
| Scenario | Symptoms | Response | Timeline |
| --- | --- | --- | --- |
| Partial failure | <symptoms> | <response> | <time> |

## 10. Contact Information
| Role | Primary | Secondary | Escalation |
| --- | --- | --- | --- |
| On-call | <person> | <person> | <path> |
```

## Quality gate

- [ ] Change description, environment, constraints, and risk assessment are captured.
- [ ] The plan includes all ten sections from Executive Summary through Contact Information.
- [ ] Preflight checks include infrastructure, application, dependencies, monitoring, and go/no-go.
- [ ] Rollout steps include commands/actions, validation after each step, and duration estimates.
- [ ] Verification signals cover 0-2 min, 2-5 min, 5-15 min, and 15+ min windows.
- [ ] Rollback has decision criteria, steps, post-rollback verification, and communication.
- [ ] Communication includes T-24h, deployment start, progress updates, completion, and rollback notices.
- [ ] Contingencies cover partial failure, performance degradation, data inconsistency, and dependency failure.
