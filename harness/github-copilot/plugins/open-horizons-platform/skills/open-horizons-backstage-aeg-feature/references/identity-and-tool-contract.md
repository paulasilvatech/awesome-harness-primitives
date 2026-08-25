# AEG identity and tool contract

## Trust boundary

The tool adapter authenticates the caller and the AEG service derives the actor from that authenticated
principal. Model-authored arguments must not include actor IDs, roles, tenant IDs, or claims. The service
checks authorization independently for every operation and records the resolved actor in its audit trail.

Reject an adapter that trusts request fields such as `initiated_by`, `decided_by`, or `proposed_by`.
Those fields can appear in responses or audit records, but not in model-controlled request schemas.

## Expected MCP surface

The server name is `open-horizons-aeg`. It should expose these stable operation names:

| Operation | Required input | Expected result |
| --- | --- | --- |
| `aeg_start_run` | Intent, name, need, and intent-specific domain inputs | Run ID, links, initial state, next event |
| `aeg_list_runs` | Optional bounded filters | Bounded run summaries |
| `aeg_get_run` | Run ID | Current state, transitions, gates, findings |
| `aeg_get_gate_package` | Run ID and G1 or G2 | Complete decision package |
| `aeg_decide_gate` | Run ID, G1 or G2, decision, rejection feedback when needed | Recorded decision and resulting state |
| `aeg_get_traceability` | Run ID | Requirement-to-resource links and gaps |
| `aeg_get_metrics` | Optional bounded filters | Metrics with source units and periods |
| `aeg_propose_profile` | At least two evidence run IDs | Draft proposal and review location |

## Adapter requirements

- Use authenticated transport and reject missing or expired credentials.
- Bound list results, request sizes, response sizes, timeouts, and retries.
- Mark tools as read-only, idempotent, or mutating for host approval policy.
- Keep secrets schemas and credential material outside tool definitions and model context.
- Return safe error codes and correlation IDs without raw stack traces or upstream bodies.
- Preserve server-side authorization and audit decisions; the client must not reinterpret them.
- Validate the target API contract in `assets/openapi-aeg.json` before publication.

## Unavailable or incompatible servers

If the server or operation is unavailable, report `blocked` with the missing capability. If the server
still requires actor fields in the request body, treat it as an incompatible legacy contract and route
the change to the AEG service owner. Do not fill those fields from conversation text as a workaround.
