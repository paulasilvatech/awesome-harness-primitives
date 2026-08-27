---
name: python-azure-iot-edge-modules
description: >-
  Build and operate Python Azure IoT Edge modules with reliable messaging, deployment manifests,
  observability, security, and production readiness checks. Use when creating Python IoT Edge
  modules, deploying edge manifests, processing telemetry at the edge, handling disconnected
  operation, or validating IoT Edge readiness.
---

<!-- Generated from harness/github-copilot/plugins/iot-embedded-systems/skills/python-azure-iot-edge-modules/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Python Azure IoT Edge modules

Designs, implements, and validates Python-based Azure IoT Edge modules for telemetry processing, local inference, protocol translation, command orchestration, and edge-to-cloud integration.

## When to invoke

- "quiero crear un modulo Python para IoT Edge"
- "como despliego modulos edge con manifest"
- "necesito filtrar/agregar telemetria antes de subirla"
- "como manejo desconexiones y reintentos en edge"
- "Validate this Python IoT Edge module for production readiness."

## Prerequisites and context

Before recommending runtime behavior or deployment decisions, review current Azure IoT Edge documentation:

- https://learn.microsoft.com/azure/iot-edge/
- https://learn.microsoft.com/es-es/azure/iot-edge/

Before proposing Python implementation details, consult official Python sources:

- https://www.python.org/
- https://docs.python.org/3/
- https://docs.python.org/3/reference/
- https://docs.python.org/3/harness/github-copilot/
- `references/python-official-best-practices.md`

If documentation cannot be fetched, proceed with explicit assumptions and flag them clearly.

## Procedure

1. Define the contract: module inputs, outputs, message schema, schema versioning, routes, priorities, and desired properties.
2. Specify runtime and packaging: Python version target, base image, container footprint, CVE hygiene, CPU and memory bounds, startup checks, and health checks.
3. Design reliability: retries with exponential backoff and jitter, graceful degradation, bounded local queueing, and idempotent replay handling.
4. Define security controls: no plaintext secrets, least-privilege behavior, secure transport, trusted certificate chain handling, and command traceability.
5. Describe deployment and operations: environment-specific manifests, pilot/staged/broad rollout, rollback criteria, SLOs, alerts, and observability.
6. Validate with a test matrix covering functional, chaos, performance, and rollback scenarios.

## Module design areas

| Area | Required decisions |
| --- | --- |
| Use case | Protocol adapter for serial/Modbus/OPC-UA, telemetry enrichment, local anomaly detection or inference, command orchestration, or local actuator control. |
| Inputs and outputs | Named inputs, output routes, schema version, critical telemetry priority, and normal telemetry route. |
| Configuration | Desired properties for dynamic config; reported properties for status and current config. |
| Packaging | Python runtime, image base, dependency pinning, startup command, health probe, and restart behavior. |
| Resources | CPU and memory bounds that match the edge device. |
| Operations | SLOs, alert conditions, logs, metrics, and rollout/rollback stages. |

## Reliability and security rules

| Concern | Rule |
| --- | --- |
| Network variability | Use exponential backoff with jitter; avoid tight retry loops. |
| Offline mode | Buffer locally only with a bounded queue and clear drop policy. |
| Replay | Make processing idempotent for repeated messages. |
| Upstream failure | Degrade gracefully and preserve local control paths when required. |
| Secrets | Never embed secrets in Dockerfiles, source, or deployment manifests. |
| Transport | Use secure transport and validate the trusted cert chain. |
| Commands | Authorize and trace command handling and state changes. |
| Rollout | Never recommend direct production rollout without a pilot stage. |

## Progressive disclosure and bundled resources

- `references/python-edge-module-template.md`: output structure for implementation proposals and reviews.
- `references/python-official-best-practices.md`: baseline Python quality criteria.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `azure-smart-city-iot-solution-builder` | skill | The request is platform-level smart city IoT architecture and phased rollout. |
| `appinsights-instrumentation` | skill | The request focuses on telemetry instrumentation patterns. |
| `azure-resource-visualizer` | skill | The request needs architecture diagrams or dependency mapping. |

## Edge module quality vocabulary

Keep designs `production-focused`, include `error-handling`, and check current `release/version` guidance before making runtime recommendations.

## Output template

```markdown
### Python Azure IoT Edge module result

**Status:** design ready | implementation plan | review findings | blocked
**Context and assumptions:** <runtime, device, connectivity, documentation assumptions>

## 1. Module design brief
- Purpose: <module purpose>
- Inputs: <module inputs>
- Outputs: <module outputs>
- Message schema/version: <schema and versioning policy>

## 2. Deployment model
- Image: <base image and tag policy>
- Manifest settings: <routes, env, desired properties>
- Resource limits: <CPU/memory>

## 3. Reliability and error handling
- Retries: <backoff and jitter>
- Offline behavior: <queue, bounds, drop policy>
- Idempotency: <replay handling>

## 4. Security and operations checklist
- <identity, secrets, cert chain, command audit, health, SLOs>

## 5. Test matrix
| Test | Method | Expected result |
| --- | --- | --- |
| Functional | <case> | <result> |
| Chaos | <disconnect/restart> | <result> |
| Performance | <load> | <result> |
| Rollback | <rollback condition> | <result> |
```

## Quality gate

- [ ] Azure IoT Edge and Python official documentation were reviewed or assumptions were stated.
- [ ] Module inputs, outputs, message schema, routes, and desired properties are defined.
- [ ] Deployment model covers image, manifest, env settings, health probes, and restart behavior.
- [ ] Reliability strategy includes backoff with jitter, bounded buffering, and idempotency.
- [ ] No plaintext secrets are placed in Dockerfiles, source, or manifests.
- [ ] Rollout includes pilot, staged, broad, and rollback criteria.
- [ ] Test matrix covers functional, chaos, performance, and rollback tests.

## References

- [Azure IoT Edge](https://learn.microsoft.com/azure/iot-edge/)
- [Azure IoT Edge Spanish documentation](https://learn.microsoft.com/es-es/azure/iot-edge/)
- [Python](https://www.python.org/)
- [Python 3 documentation](https://docs.python.org/3/)
- [Python language reference](https://docs.python.org/3/reference/)
- [Python standard library](https://docs.python.org/3/harness/github-copilot/)
