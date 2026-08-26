# RHDH Support Workflow

How support cases flow between RHDHSUPP, RHDHBUGS, and RHDHPLAN.

## Overview

1. Customer creates request on Customer Portal (access.redhat.com)
2. Support team investigates, reviews documentation and KCS articles
3. If engineering help needed → Support creates **RHDHSUPP Bug** to track discussion
4. Investigation continues until resolution
5. Resolution may produce a **RHDHBUGS Bug** (defect) or **RHDHPLAN Feature Request**

## RHDHSUPP → RHDHBUGS (Defect Path)

When a product defect is identified during support investigation:

1. Create `Bug` in **RHDHBUGS** with:
   - Priority, Component (use `Documentation` for doc defects)
   - Bug template filled out (reproduction steps, expected behavior)
   - **No customer information** - RHDHBUGS is a public project
   - Link to Customer Case via SFDC Cases Links
2. Comment on the RHDHSUPP issue with the RHDHBUGS link
3. This tells the customer when the fix is expected

```bash
# Create the bug
acli jira workitem create --project RHDHBUGS --type Bug \
  --summary "Login fails when SSO token expires during session" \
  --description-file bug_description.txt \
  --label "rhdh-customer" \
  --assignee "@me"

# Link it to the support issue
acli jira workitem link create --out RHDHSUPP-456 --in RHDHBUGS-789 --type "Related" --yes

# Comment on support issue with the link
acli jira workitem comment create --key RHDHSUPP-456 \
  --body "Defect captured in RHDHBUGS-789. Fix targeted for next y-stream release."
```

## RHDHSUPP → RHDHPLAN (Feature Request Path)

When a support case reveals a missing capability:

1. Create `Feature Request` in **RHDHPLAN** with:
   - Priority, Component
   - Feature Request template filled out
   - Link to Customer Case via SFDC Cases Links
2. Encourage customer to follow up with their account team to prioritize with Product Management

```bash
acli jira workitem create --project RHDHPLAN --type "Feature Request" \
  --summary "Support OIDC token refresh in admin console" \
  --description-file feature_request.txt

acli jira workitem link create --out RHDHSUPP-456 --in RHDHPLAN-123 --type "Related" --yes
```

## Bug Fix Prioritization

| Scenario | Target Release | Priority |
|----------|---------------|----------|
| Default | Next y-stream (e.g., 1.11.0) | As determined by triage |
| Critical to customer | Current z-stream (e.g., 1.10.4) | Set to **Blocker** |
| Customer request, not urgent | Future y-stream | As determined by triage |

For z-stream targeting, discuss with the engineer to prioritize. If committed, set Priority to Blocker and the target fix version.

## Closing RHDHSUPP Issues

Close the RHDHSUPP Bug when:

- Investigation is resolved, OR
- No response from customer within SLA

On close, set **Story Points** to capture the effort spent on the investigation. See the sizing guide for reference.

## Communication Channels

| Channel | Purpose |
|---------|---------|
| `#rhdh-support` | Engineering and Developer Hub support team communication |
| `#rhdh-support-cases` | Notification channel for new RHDHSUPP bugs from support |

## Ticket SLA

SLA depends on case severity:

| Severity | Response Time | Notes |
|----------|--------------|-------|
| Sev 1 | 1 hour | 24x7 support. Handed over between GEO teams. |
| Sev 2 | 2 hours | 24x7 support. |
| Sev 3 | 4 business hours | Business hours only. |
| Sev 4 | 1 business day | Business hours only. |

SLA may be negotiated (Negotiated Entitlement Process) or adjusted when a workaround is found.

## Special Case Types

| Type | Handling |
|------|---------|
| **Strategic customer** | Extra attention - opportunity to expand Red Hat relationship |
| **TAM customer** | Technical Account Manager assists with implementation |
| **Consulting/Partner** | Cases opened during project implementation |
| **CSE customer** | Customer Success Executive helps communication (non-technical) |
