---
name: salesforce-flow-design
description: >-
  Salesforce Flow architecture decisions, flow type selection, bulk safety validation, fault
  handling, automation density, Screen Flow UX, and deployment safety. Use this skill when
  designing or reviewing Record-Triggered, Screen, Autolaunched, Scheduled, or Platform Event
  flows before activation or deployment.
---

<!-- Generated from harness/github-copilot/plugins/salesforce-development/skills/salesforce-flow-design/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Salesforce Flow design and validation

Design or review Salesforce Flows by choosing the lightest automation tool, selecting the correct flow type, checking bulk safety and fault paths, and returning an activation-ready risk report.

## When to invoke

- "Design a Salesforce Flow for this process."
- "Review this Record-Triggered Flow before activation."
- "Check this Screen Flow for UX and fault handling."
- "Is this Flow bulk safe and deployment ready?"
- "Which Salesforce automation type should I use?"

## Automation fit

Before designing a Flow, verify that a lighter-weight declarative option cannot solve the requirement.

| Requirement | Best tool | Decision rule |
| --- | --- | --- |
| Calculate a field value with no side effects | Formula field | Prefer this over Flow when no DML, notification, or related record is needed. |
| Prevent a bad record save with a user message | Validation rule | Prefer this over Flow for save-time data quality enforcement. |
| Sum or count child records on a parent | Roll-up Summary field | Prefer this when a native roll-up can express the aggregate. |
| Complex multi-object logic, callouts, or high volume | Apex (`Queueable` / `Batch`) | Use Apex when Flow would exceed governor limits or needs code-level control. |
| Everything else | Flow | Continue only when declarative alternatives do not fit. |

If a Flow can be replaced by a formula field or validation rule, ask the user to confirm the requirement is genuinely more complex.

## Flow type selection

| Use case | Flow type | Key constraint |
| --- | --- | --- |
| Update a field on the same record before it is saved | Before-save Record-Triggered | Cannot send emails, make callouts, or change related records. |
| Create/update related records, emails, callouts | After-save Record-Triggered | Runs after commit; avoid recursion traps. |
| Guide a user through a multi-step UI process | Screen Flow | Cannot be triggered by a record event automatically. |
| Reusable background logic called from another Flow | Autolaunched (Subflow) | Input/output variables define the contract. |
| Logic invoked from Apex `@InvocableMethod` | Autolaunched (Invocable) | Must declare input/output variables. |
| Time-based batch processing | Scheduled Flow | Runs in batch context; respect governor limits. |
| Respond to events, Platform Events, or CDC | Platform Event-Triggered | Runs asynchronously with eventual consistency. |

Choose before-save when only the triggering record's fields change. Move to after-save the moment related records, emails, or callouts are required.

## Bulk safety and fault paths

| Pattern | Risk | Required fix |
| --- | --- | --- |
| `Loop element` → `Create Records` / `Update Records` / `Delete Records` | DML/Get governor limit exception | Collect records in a collection variable, then run one DML operation outside the loop. |
| `Loop element` → `Get Records` | SOQL governor limit exception | Query before the loop, then loop over the collection variable. |
| Loop + Assignment used only to reshape a collection | Large, fragile Flow graph | Use the bulk-safe Transform element when the goal is mapping field values between collections. |
| Updating `$Record` in an after-save flow with no guard | Recursion or double execution | Add precise entry conditions or a recursion guard variable. |

Correct bulk pattern:

```text
Get Records — collect all records in one query
└── Loop over the collection variable
    └── Decision / Assignment (no DML, no Get Records)
└── After the loop: Create/Update/Delete Records — one DML operation
```

Elements that require fault connectors: Create Records, Update Records, Delete Records, Get Records when a required record might not exist, Send Email, HTTP Callout, External Service action, Apex action, and Subflow when the subflow can throw a fault.

```text
Fault connector → Log Error (Create Records on a logging object or fire a Platform Event)
               → Screen element with user-friendly message (Screen Flows)
               → Stop / End element (Record-Triggered Flows)
```

Never connect a fault path back to the same element that faulted.

## Activation readiness

Check automation density before deployment. Inventory other active Record-Triggered Flows on the same `Object` + `When to Run` combination, legacy Process Builder rules, Workflow Rules, and Apex triggers in the same `before insert` / `after update` context. More than 3 active automations on one object increases order-of-execution risk.

For Screen Flow UX, verify every branch reaches an End element, Back navigation or back-navigation exists on multi-step flows unless it would corrupt data, user inputs use `lightning-input` and SLDS-compliant components rather than raw HTML form elements, screen validation blocks required input gaps, and Pause elements are intentionally handled across sessions.

Use this deployment sequence:

```text
Deploy as Draft → Test with 1 record → Test with 200+ records → Activate
```

For Record-Triggered Flows, test exact entry conditions such as `ISCHANGED(Status)`. For Scheduled Flows, test a small batch in a sandbox before production.

## Anti-patterns

| Anti-pattern | Risk | Fix |
| --- | --- | --- |
| DML element inside a Loop | Governor limit exception | Move DML outside the loop. |
| Get Records inside a Loop | SOQL governor limit exception | Query before the loop. |
| No fault connector on DML/email/callout element | Unhandled exception surfaced to user | Add a fault path to every such element. |
| Updating the triggering record in an after-save flow with no recursion guard | Infinite trigger loops | Add an entry condition or recursion guard variable. |
| Looping directly on `$Record` collection | Incorrect behaviour at scale | Assign to a collection variable first, then loop. |
| Process Builder still active alongside a new Flow | Double-execution, unexpected ordering | Deactivate Process Builder before activating the Flow. |
| Screen Flow with no End element on all branches | Runtime error or stuck user | Ensure every branch resolves to an End element. |

## Output template

```markdown
## Salesforce Flow review — <flow name or process>

**Verdict:** ready | changes required | use another automation
**Recommended automation:** <Formula field | Validation rule | Roll-up Summary field | Flow type | Apex>

| Area | Finding | Risk | Required action |
| --- | --- | --- | --- |
| Type selection | <finding> | <risk> | <action> |
| Bulk safety | <finding> | <risk> | <action> |
| Fault handling | <finding> | <risk> | <action> |
| Automation density | <finding> | <risk> | <action> |
| Deployment | <finding> | <risk> | <action> |

**Activation plan:** Deploy as Draft → Test with 1 record → Test with 200+ records → Activate
```

## Quality gate

- [ ] The chosen automation is lighter than Flow when a Formula field, Validation rule, or Roll-up Summary field is sufficient.
- [ ] The Flow type matches the side effects, trigger, and execution context.
- [ ] No `Get Records`, `Create Records`, `Update Records`, or `Delete Records` element runs inside a Loop.
- [ ] Every data-changing, email, callout, Apex, and faulting Subflow element has a fault connector.
- [ ] Automation density on the same object and trigger event is inventoried.
- [ ] Screen Flow branches reach End and validate required inputs before advance.
- [ ] Deployment testing covers 1 record and 200+ records before activation.
