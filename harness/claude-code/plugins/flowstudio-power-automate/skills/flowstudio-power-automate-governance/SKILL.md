---
name: flowstudio-power-automate-governance
description: >-
  Govern Power Automate flows and Power Apps at scale with the FlowStudio MCP cached store by
  classifying business impact, detecting orphaned resources, auditing connectors, enforcing
  compliance metadata, configuring notification rules, and computing archive or governance scores.
  Use when asked to tag flows, assign governance ownership, offboard makers, review compliance,
  audit security, or write governance metadata to FlowStudio.
metadata:
  source: "https://mcp.flowstudio.app."
---

<!-- Generated from harness/github-copilot/plugins/flowstudio-power-automate/skills/flowstudio-power-automate-governance/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# FlowStudio Power Automate governance

Take tenant flow and maker records from the FlowStudio MCP cached store, transform them into governance classifications or metadata updates with `update_store_flow`, and return compliance, ownership, connector, security, notification, or archive recommendations without using Dataverse, the CoE Starter Kit, or the Power Automate portal.

## When to invoke

- "Classify these Power Automate flows by business impact."
- "Find orphaned flows for this maker offboarding."
- "Audit connectors and premium flow usage in FlowStudio."
- "Set notification rules for critical flows."
- "Generate a FlowStudio governance compliance report."

## Prerequisites and context

- Requires FlowStudio for Teams or MCP Pro+ because `store_*` tools require a paid cached-store subscription. If the first `store_*` call returns 403 or 404, stop store calls, tell the user governance features require Pro+ access, and point to https://mcp.flowstudio.app/pricing
- Load real tool schemas through meta-tool discovery, not `tools/list`: use `tool_search` with `query: "skill:governance"` for the canonical bundle or `query: "select:update_store_flow"` for a single tool. If a real API response disagrees with this skill, the API wins.
- Use this skill for governance writes and classification. For health checks, failure-rate dashboards, or operational monitoring, use the `flowstudio-power-automate-monitoring` skill.

## Flow identity and cached-store semantics

`list_store_flows` returns `id` as `<environmentId>.<flowId>`. Split on the first `.` only:

```text
id = "Default-<envGuid>.<flowGuid>"
environmentName = "Default-<envGuid>"
flowName = "<flowGuid>"
```

Skip records with no `displayName` or `state=Deleted`; they are sparse cache rows or deleted flows. If a deleted flow still has `monitor=true`, suggest `update_store_flow` with `monitor=false` to free a monitoring slot.

`update_store_flow` writes Flow Studio cache metadata only. It does not change actual Power Automate ownership, Microsoft flow alerts, or portal-visible fields.

| Cache field | Governance effect | Does not do |
| --- | --- | --- |
| `ownerTeam`, `ownerBusinessUnit`, `supportGroup`, `supportEmail` | Sets Flow Studio governance contacts and escalation data | Transfer Power Automate ownership |
| `rule_notify_onfail`, `rule_notify_onmissingdays`, `rule_notify_email` | Configures Flow Studio failure and missing-run notifications | Change Microsoft built-in failure emails |
| `monitor`, `critical`, `businessImpact`, `businessJustification`, `businessValue`, `tier` | Classifies Flow Studio scanning and governance status | Change Power Automate runtime behavior |
| `description`, `tags` | Stores documentation and classifications; description hashtags are auto-extracted separately | Preserve previous tags unless you read/append/write |
| `security` | Contains structured JSON such as `{"triggerRequestAuthenticationType":"All"}` | A plain string like `"reviewed"` will overwrite structured data; use `tags` for `#security-reviewed` |

Required `update_store_flow` parameters are `environmentName` and `flowName`; all governance fields are optional and merge-only.

## Governance workflows

| Workflow | Steps | Output |
| --- | --- | --- |
| Compliance detail review | Ask which fields are required; `list_store_flows`; for each active flow split `id`, call `get_store_flow`, check `description`, `businessImpact`, `businessJustification`, `ownerTeam`, `supportEmail`, `monitor`, `rule_notify_onfail`, and `critical`; update only provided fields. | Non-compliant flows with missing fields and proposed `update_store_flow` calls. |
| Orphaned resource detection | `list_store_makers`; filter `deleted=true` and `ownerFlowCount > 0`; collect active flows; parse `owners` JSON; match `principalId`; reassign governance contact or tag for decommission. | Orphaned flows, system-generated exceptions, contacts to update, and admin-center or PowerShell ownership actions. |
| Archive score calculation | Add one point each for created≈modified, test/demo/temp/copy name, age over 12 months, stopped/suspended state, no owners, no recent runs, and `complexity.actions < 5`. | Score 5-7 archive; 3-4 `#archive-review`; 0-2 active. Confirmed archive means `set_live_flow_state(..., "Stopped")` plus `#archived`. |
| Connector audit | Prefer `list_store_flows(monitor=true)`; split ids; call `get_store_flow`; parse `connections` JSON; group by `apiName`; flag Premium tier, HTTP connectors, and custom connectors. | DLP impact and premium license inventory. `list_store_connections` lists connection instances, not usage per flow. |
| Notification rules | For critical monitored flows, set `rule_notify_onfail=true` and `rule_notify_email`; for monitored `Recurrence` flows, set `rule_notify_onmissingdays=2` when missing or zero. | Notification configuration changes and monitoring-limit warnings. |
| Classification and tagging | Read existing store tags, map connector `apiName` values to `#sharepoint`, `#teams`, `#email`, `#custom-connector`, append new tags, then write `tags=...`. | Tags preserved plus new classifications. Do not override computed `tier` unless asked. |
| Maker offboarding | `get_store_maker(makerKey="<departing-user-aad-oid>")`; check `ownerFlowCount`, `ownerAppCount`, and `deleted`; match flow owners; `list_store_power_apps`; update contacts, add to solution when needed, stop and tag retired flows. | Flows reassigned in Flow Studio, flows needing actual PA ownership transfer, apps needing manual reassignment. |
| Security review | `list_store_flows(monitor=true)`; parse `security`, `connections`, and `referencedResources` JSON; read top-level `sharingType`; append `#security-reviewed` only after review. | Trigger auth, oversharing, connector, URL, and tier findings without overwriting `security`. |
| Environment governance | `list_store_environments`; skip entries without `displayName`; flag Developer environments, non-managed environments, and `isAdmin=false`; group flows and connections by `environmentName`. | Environment sprawl and access report. |
| Governance dashboard | Use list calls for `total_flows`, monitored count, `rule_notify_onfail` count, makers, apps, envs, conns; use get calls only for detailed compliance, undocumented count, and tier breakdown. | Tenant-wide monitoring %, notification %, orphan count, high-failure count, compliance %, undocumented count. |

## Field reference

| Field | Available on list | Type | Governance use |
| --- | --- | --- | --- |
| `displayName` | yes | string | Archive score name detection |
| `state` | yes | string | Archive score and lifecycle |
| `tier` | no | string | Standard vs Premium audit |
| `monitor` | yes | bool | Active run-level scanning; standard plan includes 20 flows |
| `critical` | no | bool | Business-critical flag |
| `businessImpact` | no | string | Low / Medium / High / Critical classification |
| `businessJustification`, `businessValue` | no | string | Compliance attestation |
| `ownerTeam`, `ownerBusinessUnit`, `supportGroup`, `supportEmail` | no | string | Accountability and escalation |
| `rule_notify_onfail`, `rule_notify_onmissingdays`, `rule_notify_email` | no | bool, number, string | Failure and missing-run alerts |
| `description`, `tags` | mixed | string | Documentation and classification; store tags require `get_store_flow` to read back |
| `runPeriodTotal`, `runPeriodFailRate` | yes | number | Activity and health summary |
| `runLast`, `scanned`, `createdTime`, `lastModifiedTime` | mixed | ISO string | Freshness, age, and staleness |
| `deleted` | no | bool | Lifecycle tracking |
| `owners`, `connections`, `complexity`, `security`, `referencedResources` | no | JSON string | Parse with `json.loads()` before matching IDs, `apiName`, actions, `triggerRequestAuthenticationType`, or URLs |
| `sharingType` | no | string | Oversharing detection; top-level, not inside `security` |

## Gotchas

- **Split ids on the first dot only**: environment ids contain hyphenated values and flow ids follow the first `.`.
- **Tags overwrite**: read existing tags before writing; append rather than replacing unless the user explicitly asks.
- **`security` is structured JSON**: never write `"reviewed"`; append `#security-reviewed` to `tags` instead.
- **Actual ownership changes are external**: use Power Automate admin center or PowerShell for real owner transfer.
- **Store freshness matters**: `scanned` defines cache recency; stale data weakens compliance claims.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `flowstudio-power-automate-monitoring` | skill | The task is health, failure-rate, inventory, or operational monitoring and should stay read-only. |
| `flowstudio-power-automate-mcp` | skill | The task is connection setup, MCP helper usage, or tool discovery. |
| `flowstudio-power-automate-debug` | skill | The task requires action-level inputs, outputs, or deep run diagnosis. |
| `flowstudio-power-automate-build` | skill | The task is building or deploying flow definitions. |

## Source compatibility terms

Compatibility keys: `security.triggerRequestAuthenticationType`, `tags=`.

Retain these FlowStudio governance terms when reconciling old reports or tool output: ` and `, ` are also available on `, `#hashtags`, `** to get `, `0/missing`, `STOP`, `add_live_flow_to_solution`, `bulk-enabling`, `business-critical`, `critical=true`, `description-extracted`, `failure/missing-run`, `get_live_flow`, `inputs/outputs`, `list_store_makers/list_store_power_apps/list_store_environments/list_store_connections`, `makers/apps/envs/conns`, `manual/admin-center`, `meta-tools`, `non-compliant`, `orphaned-looking`, `ownerTeam/supportEmail/rule_notify_email`, `read/append/write.`, `security.triggerRequestAuthenticationType`, `security/connections/referencedResources`, `stop/tag`, `tags=`, `tenant-level`, `tenant-wide`, `test/demo`, and `with_onfail`.

## Output template

```markdown
## FlowStudio governance report — <tenant, environment, maker, or policy>

**Status:** complete | needs approval | blocked
**Scope:** <flows, environments, makers, apps>
**Cache freshness:** <scanned timestamps or limitation>

| Flow/App | Environment | Finding | Severity | Recommended action | Write performed |
| --- | --- | --- | --- | --- | --- |
| `<displayName>` | `<environmentName>` | Missing `businessImpact` | Medium | `update_store_flow(..., businessImpact="High")` | yes/no |

### Metadata updates
- `<environmentName>.<flowName>`: `<fields changed or proposed>`

### Manual follow-up
- <Power Automate ownership, DLP policy, portal deletion, or admin action>
```

## Quality gate

- [ ] Flow ids from `list_store_flows` are split into `environmentName` and `flowName` on the first `.`.
- [ ] Deleted or sparse records are skipped, except for recommending `monitor=false` on deleted monitored flows.
- [ ] Every `update_store_flow` call includes only intended merge fields and never overwrites structured `security` with a plain string.
- [ ] Existing `tags` are read before appended tags are written.
- [ ] Governance-contact changes are not misrepresented as actual Power Automate ownership transfers.
- [ ] Pro+ 403/404 failures stop further store calls and are reported with https://mcp.flowstudio.app/pricing
- [ ] The report distinguishes cache metadata changes from manual portal, admin center, or PowerShell actions.

## References

- [FlowStudio MCP](https://mcp.flowstudio.app.)
- [FlowStudio pricing](https://mcp.flowstudio.app/pricing)
