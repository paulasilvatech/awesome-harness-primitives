---
paths:
  - "**/*.bicep"
  - "**/*.tf"
  - "**/*iot*.md"
  - "**/*smart-city*.md"
  - "**/*edge*.md"
---

<!-- Generated from harness/github-copilot/instructions/azure-iot-edge-architecture.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Azure IoT Edge architecture conventions for documentation-grounded edge applicability, runtime constraints, supported systems, operations, security, and assumptions.

# Azure IoT Edge Architecture Conventions — Documentation-Grounded Edge Design

These instructions apply to infrastructure files and architecture documents involving Azure IoT, Smart City systems, edge processing, gateway design, or disconnected edge scenarios. They are authoritative for validating IoT Edge applicability, documenting runtime and platform constraints, and explaining operational and security implications; current Azure IoT Edge documentation wins where service status, supported systems, or quickstart guidance changes.

## Documentation Review and Applicability

Review Azure IoT Edge documentation before proposing architecture recommendations. Confirm the runtime architecture, supported systems, Version/release status, and the relevant Linux/Windows quickstart path. Explicitly state that the documentation was reviewed; if it could not be consulted, continue only with clearly labeled assumptions.

Do not jump directly to a list of Azure services. First explain whether IoT Edge is required, optional, or unnecessary for the scenario based on latency, offline operation, gateway protocol translation, local processing, data residency, and device management needs.

## Runtime, Host, and Deployment Constraints

Model IoT Edge as an edge runtime with modules deployed to supported host systems, not as a generic container host. Capture host OS support, update cadence, module lifecycle, cloud-to-edge connectivity, and fallback behavior for disconnected operation.

Infrastructure guidance in `.bicep` or `.tf` files should distinguish cloud resources from edge device configuration. Do not imply that cloud IaC alone deploys or updates every edge module unless the implementation actually wires the deployment path.

## Operational Implications

Include operational implications in every IoT Edge design: update strategy, observability, support model, failure handling, and ownership boundaries between cloud services, edge gateways, and field devices.

| Concern | Convention |
| --- | --- |
| Updates | Define how runtime, modules, base images, and host OS updates are delivered and rolled back. |
| Observability | Include logs, metrics, health checks, and remote diagnostics appropriate for disconnected sites. |
| Support model | Name who owns device provisioning, field replacement, cloud configuration, and incident response. |
| Disconnection | Describe buffering, retry, data loss tolerance, and reconciliation behavior. |

## Secure Defaults

Prioritize managed identity where supported, least privilege, secret management, network isolation, and explicit trust boundaries. Avoid embedding secrets in module settings, device scripts, Terraform variables, or Bicep parameters. Treat edge devices as physically exposed unless the scenario proves otherwise.

## Good / Bad Examples

The examples below illustrate edge applicability reasoning before service selection.

**Good:**

```text
IoT Edge is required because cameras must continue local inference during WAN outages, buffer events, and forward summarized telemetry when connectivity returns.
```

Why: The recommendation ties IoT Edge to latency, disconnected operation, and gateway behavior.

**Bad:**

```text
Use IoT Hub, IoT Edge, Stream Analytics, Functions, and Storage.
```

Why: The response lists services without validating whether edge processing is needed or supportable.

## Conventions

| Rule | Rationale |
|---|---|
| Review current Azure IoT Edge documentation before recommending an edge architecture | Supported systems, release status, and quickstarts can change. |
| State whether documentation was reviewed or assumptions were used | Readers know the confidence level behind the architecture. |
| Explain why IoT Edge is or is not required before listing services | Edge runtime adds operational cost and should solve a real constraint. |
| Include update strategy, observability, and support model | Edge deployments fail operationally when ownership and telemetry are vague. |
| Prioritize managed identity, least privilege, secret management, and network isolation | Edge devices and gateways expand the attack surface. |
| Separate cloud IaC from edge runtime and module deployment responsibilities | `.bicep` and `.tf` files do not automatically manage every edge host concern. |

## Do / Do Not

| Do | Do not |
|---|---|
| Check runtime architecture, supported systems, release status, and quickstarts | Rely on stale memory for IoT Edge platform constraints. |
| Label assumptions when documentation is inaccessible | Present unverified platform claims as facts. |
| Explain edge applicability for Smart City, gateway, and disconnected scenarios | Start with a generic service list. |
| Design for updates, observability, buffering, and support | Treat edge modules as deploy-once infrastructure. |
| Use secure defaults and isolated networks | Put secrets in module settings or infrastructure parameters. |

## Checklist Before Opening a PR

- [ ] Azure IoT Edge documentation was reviewed, or assumptions were clearly labeled.
- [ ] Runtime architecture, supported systems, version or release status, and Linux or Windows quickstart relevance are captured.
- [ ] The design explains why IoT Edge is required, optional, or unnecessary.
- [ ] Operational implications cover updates, observability, support model, and disconnected behavior.
- [ ] Security guidance covers managed identity, least privilege, secret management, and network isolation.
- [ ] Cloud IaC responsibilities are separated from edge runtime, host, and module deployment responsibilities.

## References

- [Azure IoT Edge documentation](https://learn.microsoft.com/azure/iot-edge/)
- [Azure IoT Edge documentation in Spanish](https://learn.microsoft.com/es-es/azure/iot-edge/)
