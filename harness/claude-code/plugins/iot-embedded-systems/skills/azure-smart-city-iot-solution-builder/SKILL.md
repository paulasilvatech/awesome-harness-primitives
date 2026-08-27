---
name: azure-smart-city-iot-solution-builder
description: >-
  Design and plan end-to-end Azure IoT and Smart City solutions with requirements, architecture,
  device and edge strategy, ingestion, analytics, security, operations, cost controls, and phased
  delivery artifacts. Use when asked to build an IoT solution on Azure, design Smart City traffic,
  lighting, waste, water, energy, or public safety platforms, or create an urban IoT roadmap.
---

<!-- Generated from harness/github-copilot/plugins/iot-embedded-systems/skills/azure-smart-city-iot-solution-builder/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure Smart City IoT solution builder

Turn a high-level Smart City or Azure IoT idea into a deployable architecture, governance model, and phased implementation backlog with explicit assumptions and operational controls.

## When to invoke

- "I want to build an IoT solution on Azure."
- "Design a Smart City architecture for traffic, lighting, or waste."
- "How do I connect devices, analytics, and alerts?"
- "Create a roadmap and backlog for an urban platform."
- "Plan an Azure IoT solution with edge processing."

## Prerequisites and context

Before proposing architecture that involves edge computing, review Azure IoT Edge documentation: https://learn.microsoft.com/azure/iot-edge/

Minimum documentation topics to review are What is Azure IoT Edge, runtime architecture, supported systems, version history/release notes, and relevant Linux/Windows quickstarts for the scenario. If documentation cannot be consulted, state that explicitly and continue with marked assumptions.

## Procedure

1. Confirm scope and constraints: city domain, device count, telemetry frequency, retention, regions, latency, availability, privacy, and integrations such as SCADA, GIS, ERP, ticketing, and APIs.
2. Build the capability map across device and edge, ingestion and messaging, data and analytics, operations, and governance.
3. Select Azure services and document trade-offs instead of naming services without rationale.
4. Define non-functional design: reliability, security, cost controls, and data lifecycle.
5. Produce a phased delivery plan for pilot, multi-domain integration, and city-scale rollout.
6. Use `references/smart-city-solution-template.md` to standardize the final artifact when a full solution document is requested.

## Capability map

| Layer | Design decisions |
| --- | --- |
| Device and edge | Onboarding, device identity, firmware, OTA, edge processing, IoT Edge runtime footprint. |
| Ingestion and messaging | Command and control, event routing, buffering, back-pressure, dead-letter handling. |
| Data and analytics | Hot path versus cold path, dashboards, historical analysis, raw/curated/aggregated/archive zones. |
| Operations | Observability, incident flow, SLOs, ownership, change windows, replay strategy. |
| Governance | RBAC, secrets, policies, private networking, network isolation, encryption, data retention. |

## Azure service selection

| Need | Candidate services |
| --- | --- |
| Device connectivity | Azure IoT Hub, Azure IoT Operations, IoT Edge. |
| Event streaming | Event Hubs, Service Bus, Event Grid. |
| Storage | Blob Storage, Data Lake, Cosmos DB, SQL. |
| Analytics | Azure Data Explorer, Stream Analytics, Fabric/Synapse. |
| APIs and applications | API Management, App Service, Container Apps, Functions. |
| Monitoring | Azure Monitor, Application Insights, Log Analytics. |
| Security | Key Vault, Defender for IoT, Private Endpoints, Managed Identity. |

## Non-functional design

| Area | Required treatment |
| --- | --- |
| Reliability | `zones/regions`, retry policy, buffering, replay, dead-letter queues, failure domains. |
| Security | Zero trust, least privilege, encryption in transit and at rest, managed identities, secret rotation. |
| Cost | Retention tiers, rightsizing, autoscaling, reserved capacity where appropriate, workload scheduling. |
| Data lifecycle | Raw, curated, aggregated, and archived data with ownership and retention. |
| Privacy | Minimize personally identifiable data, define retention, and document access controls. |

## Delivery plan

| Phase | Scope | Required content |
| --- | --- | --- |
| Phase 1 | Pilot district or single use case. | Exit criteria, dependencies, risks, mitigations, KPI set. |
| Phase 2 | Multi-domain integration. | Cross-domain data model, integration dependencies, operating model. |
| Phase 3 | City-scale rollout and optimization. | Scale targets, cost optimization, resilience validation, governance controls. |

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `azure-kubernetes` | skill | AKS planning or production Kubernetes details are central to the scenario. |
| `azure-observability` | skill | Observability design needs deeper Azure Monitor or dashboard guidance. |
| `azure-rbac` | skill | RBAC and identity assignments need deeper treatment. |
| `azure-messaging` | skill | Event Hubs, Service Bus, or messaging SDK troubleshooting needs deeper treatment. |
| `azure-storage` | skill | Storage account, Data Lake, lifecycle, or access design needs detailed guidance. |
| `azure-cost` | skill | The user asks for spending, forecast, or optimization analysis. |
| `azure-validate` | skill | The solution is ready for Azure deployment validation. |
| `azure-deploy` | skill | Prepared infrastructure should be deployed. |
| `azure-architecture-autopilot` | local skill under `skills/` | Architecture generation and refinement is needed in this repository. |
| `azure-resource-visualizer` | local skill | Resource relationship diagrams are needed. |
| `azure-role-selector` | local skill | Role selection guidance is needed. |
| `az-cost-optimize` and `azure-pricing` | local skills | Cost and pricing analysis are needed in this repository. |
| `azure-deployment-preflight` | local skill | pre-deployment checks are needed. |
| `appinsights-instrumentation` | local skill | Telemetry instrumentation patterns are needed. |

## Limits

- Do not jump to deployment before validating prerequisites.
- Do not recommend single-region production for critical city workloads.
- Do not omit operational ownership, incident handling, SLAs, or change windows.
- If specialized runtime skills are unavailable, continue with this skill and mark assumptions.

## Progressive disclosure and bundled resources

- `references/smart-city-solution-template.md`: standard output structure for full scenario documents.

## Output template

```markdown
## Smart City IoT solution

**Status:** proposed | needs input | blocked
**Domain:** `<traffic|lighting|waste|water|energy|public safety|other>`
**Assumptions:** <confirmed assumptions and unknowns>

### 1. Context and objectives
<scope, constraints, stakeholders, KPIs>

### 2. Proposed architecture
<components, data flow, and service choices>

### 3. Technology decisions and trade-offs
| Decision | Choice | Alternatives | Rationale |
| --- | --- | --- | --- |

### 4. Security, operations, and cost controls
<governance checklist, observability, resilience, cost strategy>

### 5. Phased implementation plan
| Phase | Milestones | Exit criteria | Risks |
| --- | --- | --- | --- |

### 6. Risks and open questions
<items requiring confirmation>
```

## Quality gate

- [ ] Azure IoT Edge documentation was reviewed or the inability to review it is stated with assumptions.
- [ ] Scope includes domain, scale, telemetry frequency, retention, region, latency, availability, privacy, and integrations.
- [ ] Architecture covers device/edge, ingestion, data/analytics, operations, and governance.
- [ ] Service choices include rationale and trade-offs.
- [ ] Security, reliability, data lifecycle, cost, and operational ownership are documented.
- [ ] The plan includes pilot, multi-domain, and city-scale phases with exit criteria and KPIs.

## References

- [Azure IoT Edge documentation](https://learn.microsoft.com/azure/iot-edge/)
