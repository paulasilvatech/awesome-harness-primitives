---
name: arduino-azure-iot-edge-integration
description: >-
  Design and implement Arduino integration with Azure IoT Hub and IoT Edge, including secure
  provisioning, MQTT telemetry, gateway topologies, offline buffering, command handling, OTA
  configuration, and production guardrails. Use when connecting Arduino sensors or actuators to
  Azure IoT or edge gateways.
---

<!-- Generated from harness/github-copilot/plugins/iot-embedded-systems/skills/arduino-azure-iot-edge-integration/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Arduino Azure IoT Edge integration

Connects Arduino-class devices to Azure IoT Hub or an IoT Edge gateway with secure identity, resilient telemetry, command authorization, local buffering, and a practical firmware, gateway, and cloud backlog.

## When to invoke

- "I want to connect Arduino sensors to Azure."
- "How do I send MQTT telemetry to IoT Hub?"
- "I need an edge gateway for field devices."
- "I want cloud-to-device commands and OTA configuration updates."
- "Design Arduino telemetry with offline buffering and local actuation."

## Prerequisites and context

Before recommending IoT Edge topology or runtime behavior, review:

- https://learn.microsoft.com/azure/iot-edge/

Before proposing firmware, wiring, or communication implementation details, consult official Arduino sources first:

- https://docs.arduino.cc/learn/starting-guide/getting-started-arduino/
- https://docs.arduino.cc/
- https://docs.arduino.cc/language-reference/
- `references/arduino-official-best-practices.md`

If documentation cannot be consulted, proceed with explicit assumptions and highlight them in the output.

## Connectivity patterns

| Pattern | Use when | Design notes |
| --- | --- | --- |
| Arduino direct to IoT Hub | Connectivity is stable and cloud latency is acceptable. | Use MQTT over TLS, per-device SAS or X.509 credentials, and compact JSON with timestamp, device ID, metrics, and optional quality flags. |
| Arduino to local gateway, then IoT Edge | Links are constrained, local control is required, batching improves reliability or cost, or offline behavior matters. | Arduino communicates with a local gateway through serial, BLE, local MQTT, RS-485, or Modbus bridge; the gateway publishes through IoT Edge routes. |

## Design flow

1. Define the device contract: sensor catalog, units, sampling frequency, expected throughput, message schema versioning, desired properties, and reported properties.
2. Establish the security baseline: unique identity per device, no hardcoded secrets, credential rotation, signed firmware, and controlled update process where possible.
3. Plan reliability and offline behavior: backoff with jitter, bounded local queue, duplicate suppression, idempotent downstream processing, and fallback to last-known-good configuration.
4. Define cloud and edge routes: raw telemetry to cold storage, curated telemetry to hot analytics, alerts to operations channels, and commands/configuration back to edge or device.
5. Specify observability: heartbeat, firmware version, connectivity state transitions, message send success/error counters, gateway module health, and restart reasons.

## Message and command contract

| Field | Rule |
| --- | --- |
| `deviceId` | Stable per-device identity; do not share across devices. |
| `timestamp` | Use device time only when synchronized; otherwise include gateway receipt time. |
| `schemaVersion` | Increment on incompatible payload changes. |
| `metrics` | Include units, quality flags, and sampling frequency assumptions. |
| Commands | Authorize, audit, validate parameters, and define safe fallback for actuator scenarios. |
| OTA configuration | Use desired/reported properties for configuration state; do not use ad hoc unaudited command payloads. |

## Gotchas

- **Do not use shared credentials across devices**: shared SAS keys break revocation, auditing, and production operations.
- **Do not assume always-on connectivity**: field deployments need buffering, retries, dedupe, and last-known-good config.
- **Do not omit command authorization**: actuator scenarios require audit trails and safe failure behavior.
- **Do not choose direct-to-cloud by default**: use a gateway when local control, constrained links, or batching are load-bearing.

## Progressive disclosure and bundled resources

- `references/arduino-official-best-practices.md`: official Arduino quality baseline for firmware and hardware recommendations.
- `references/arduino-iot-checklist.md`: architecture and implementation checklist before finalizing guidance.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `azure-smart-city-iot-solution-builder` | skill | The request is city-wide architecture and phased rollout. |
| `azure-resource-visualizer` | skill | The request needs relationship diagrams. |
| `appinsights-instrumentation` | skill | The request focuses on telemetry instrumentation patterns. |

## Arduino edge vocabulary

This skill covers `edge-heavy`, `end-to-end` designs with `store-and-forward`, `queue/buffer`, `Desired/reported` twin properties, `identity/credentials/updates.`, `cost/reliability.`, and `edge/device.` routing decisions.

## Output template

````markdown
### Arduino Azure IoT integration result

**Status:** architecture ready | implementation backlog | blocked
**Scenario and assumptions:** <connectivity, board class, gateway, docs assumptions>

## 1. Recommended architecture
**Pattern:** Arduino direct to IoT Hub | Arduino to local gateway, then IoT Edge
**Rationale:** <why this pattern fits>

## 2. Device and gateway contract
**Telemetry payload:**
```json
{
  "deviceId": "<device-id>",
  "timestamp": "<ISO-8601>",
  "schemaVersion": "1.0",
  "metrics": { "<name>": { "value": 0, "unit": "<unit>", "quality": "good" } }
}
```
**Commands/configuration:** <desired/reported properties and authorization>

## 3. Security and reliability controls
- Identity and credentials: <plan>
- Retry, buffering, dedupe: <plan>
- Firmware/update controls: <plan>

## 4. Deployment plan and validation tests
| Backlog item | Owner area | Validation |
| --- | --- | --- |
| <firmware/gateway/cloud item> | <area> | <test> |
````

## Quality gate

- [ ] Azure IoT Edge and official Arduino documentation were reviewed or assumptions were stated.
- [ ] Connectivity pattern and rationale are explicit.
- [ ] Message contract includes fields, units, schema version, and sample payload.
- [ ] Security checklist covers identity, credentials, command authorization, auditing, and updates.
- [ ] Reliability plan covers retry, buffering, dedupe, and last-known-good config.
- [ ] Implementation backlog covers firmware, gateway, and cloud work.

## References

- [Azure IoT Edge](https://learn.microsoft.com/azure/iot-edge/)
- [Arduino getting started](https://docs.arduino.cc/learn/starting-guide/getting-started-arduino/)
- [Arduino documentation](https://docs.arduino.cc/)
- [Arduino language reference](https://docs.arduino.cc/language-reference/)
