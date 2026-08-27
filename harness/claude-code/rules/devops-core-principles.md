<!-- Generated from harness/github-copilot/instructions/devops-core-principles.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces foundational DevOps conventions for CALMS culture, automation, lean flow, measurement, sharing, and DORA delivery metrics.

# DevOps Core Principles Conventions — CALMS and DORA

These instructions apply to DevOps-related code, pipelines, infrastructure, runbooks, documentation, operational advice, and delivery-process changes. They are authoritative for foundational DevOps culture, automation, lean flow, measurement, sharing, and DORA metric guidance; repository-specific CI/CD, cloud, security, incident, and infrastructure primitives win when they define concrete tools, commands, environments, or compliance gates.

## DevOps Definition and Operating Model

Treat DevOps as a cultural, philosophical, and technical shift that combines software development and IT operations to shorten the systems development life cycle while delivering features, fixes, and updates frequently in close alignment with business objectives. It is not a methodology like Agile; it is a set of principles and practices that improves communication, collaboration, integration, automation, reliability, security, customer satisfaction, and time to market.

When generating or reviewing code, pipeline changes, infrastructure, monitoring, or documentation, evaluate how the work improves flow from commit to production and how it supports shared ownership after release.

## CALMS Framework

| Pillar | Convention | Copilot guidance |
| --- | --- | --- |
| Culture | Foster collaboration, shared responsibility, trust, blameless post-mortems, continuous learning, and feedback loops across development, operations, security, and business. | Add context about why changes matter, investigate across the pipeline, write accessible docs, recommend shared channels, and make runbooks executable by anyone. |
| Automation | Automate builds, tests, deployments, monitoring, alerts, infrastructure provisioning, configuration management, and security scans. | Prefer CI/CD pipelines, IaC with Terraform, Ansible, or Pulumi, automated tests, SAST, DAST, SCA, blue/green deployments, canary deployments, rollback hooks, and operational scripts. |
| Lean | Eliminate waste, reduce batch size, maximize flow, build quality in, map value streams, and deliver MVPs iteratively. | Suggest smaller tasks, smaller PRs, iterative deployments, modularity, testability, and bottleneck removal. |
| Measurement | Track KPIs, DORA, metrics, logs, traces, dashboards, alerts, experiments, A/B tests, and capacity planning signals. | Recommend request latency, error rates, deployment frequency, lead time, mean time to recovery, change failure rate, structured logging, tracing, Prometheus, and Grafana where appropriate. |
| Sharing | Share tools, platforms, practices, runbooks, ADRs, wikis, communication channels, cross-functional work, pairing, mob programming, meetups, workshops, and lessons learned. | Generate clear documentation, ADR/runbook templates, and internal explanations for complex logic. |

## Delivery Automation and Operational Safety

Automate every repeatable activity that affects delivery or operations. CI/CD should build, test, integrate, deploy, validate, and surface failures with actionable logs. IaC should make environments consistent and versioned. Configuration management with Ansible, Puppet, Chef, or equivalent tools should replace undocumented manual setup. Monitoring and alerting must collect metrics, logs, and traces and notify teams about anomalies before customers report them. Security automation belongs in the delivery path so vulnerable code or dependencies fail before production.

## Lean Flow and Continuous Improvement

Reduce waiting, unnecessary approvals, manual handoffs, excessive documentation, and defect re-work. Smaller commits, smaller PRs, frequent deployments, and feature flags reduce risk per change. Value stream mapping should identify bottlenecks across development, testing, review, deployment, and operations. Use feedback and data to adjust the process continuously.

## DORA Metrics

| Metric | Definition | Goal | Improvement levers |
| --- | --- | --- | --- |
| Deployment Frequency (DF) | How often production releases succeed | High; elite performers deploy multiple times per day | Small batches, automated tests, blue/green deployments, feature flags |
| Lead Time for Changes (LTFC) | Time from commit to production | Low; elite performers are under one hour | Smaller PRs, faster builds, automation, efficient review, fewer handoffs |
| Change Failure Rate (CFR) | Percentage of deployments causing degradation, rollback, hotfix, or outage | Low; elite performers are 0-15% | Robust tests, automated rollback, monitoring, static analysis, dynamic analysis, security scanning, health checks |
| Mean Time to Recovery (MTTR) | Time to restore service after degradation or outage | Low; elite performers are under one hour | Observability, alerts, runbooks, automated incident response, rollback, structured logging, metrics, distributed tracing |

Use circuit breakers, retries, graceful degradation, automated notifications, centralized logging, tracing, dashboards, one-click rollback where feasible, and post-deployment validation to improve CFR and MTTR.

## Technical Vocabulary

Preserve these source terms when they apply to edits in this domain: `CI/CD.` `auto-scaling` `cross-training` `end-of-cycle` `end-to-end` `high-quality` `non-value-adding` `pre-deployment` `problem-solving` `stand-ups` `up-to-date` `well-documented`.

## Good / Bad Examples

The examples below show pipeline guidance aligned with DevOps principles.

**Good:**

```yaml
name: ci
on: [push, pull_request]
jobs:
  verify:
    steps:
      - run: npm ci
      - run: npm test
      - run: npm run lint
```

Why: The pipeline automates repeatable verification and creates fast feedback before merge.

**Bad:**

```text
Build locally, ask operations to deploy manually, and check production later.
```

Why: Manual handoffs slow lead time, hide failures, and increase deployment risk.

## Conventions

| Rule | Rationale |
|---|---|
| Treat DevOps as culture plus practices, not a tool purchase | Tools cannot fix silos or missing ownership by themselves |
| Prefer shared ownership and blameless learning | Teams reveal systemic issues faster when incident response is safe |
| Automate repeatable build, test, deploy, security, and operational work | Automation reduces human error and accelerates feedback |
| Reduce batch size with small PRs and frequent deployments | Smaller changes are easier to review, release, and roll back |
| Measure DORA and operational health metrics | Improvement requires data rather than anecdotes |
| Document runbooks, ADRs, processes, and lessons learned | Knowledge sharing reduces dependency on individual experts |

## Do / Do Not

| Do | Do not |
|---|---|
| Investigate across code, pipeline, infrastructure, and runtime | Treat incidents as only a developer or only an operations problem |
| Build CI/CD gates for tests, deployments, and security scans | Depend on manual release checklists for repeatable work |
| Use IaC for repeatable infrastructure | Make untracked manual production changes |
| Use metrics, logs, traces, and dashboards for decisions | Debug by guessing without telemetry |
| Use feature flags and small batches | Couple deployment to large risky releases |
| Write runbooks executable by non-experts | Keep operational knowledge in one person's memory |

## Checklist Before Opening a PR

- [ ] The change supports shared responsibility across development, operations, and security.
- [ ] Repeatable build, test, deploy, security, or operational work is automated where practical.
- [ ] The change reduces or avoids manual handoffs, excessive batch size, and avoidable waiting.
- [ ] Relevant delivery, runtime, or business metrics are emitted, tracked, or documented.
- [ ] Runbooks, ADRs, dashboards, alerts, or other shared knowledge are updated when behavior changes.
- [ ] DORA impacts on DF, LTFC, CFR, and MTTR were considered.
