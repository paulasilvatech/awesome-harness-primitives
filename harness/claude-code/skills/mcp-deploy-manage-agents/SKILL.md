---
name: mcp-deploy-manage-agents
description: >-
  Guide deployment, governance, assignment, lifecycle, approval, blocking, monitoring, and
  distribution for MCP-based declarative agents in Microsoft 365 admin center. Use when asked to
  publish, deploy, approve, block, assign, govern, monitor, troubleshoot, or manage Microsoft 365
  agents, shared agents, Microsoft agents, external partner agents, or frontier agents.
---

<!-- Generated from harness/github-copilot/skills/mcp-deploy-manage-agents/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# MCP deploy and manage agents

Deploy, manage, and govern MCP-based declarative agents in Microsoft 365 by turning an agent readiness question into admin-center deployment steps, assignment decisions, governance checks, and a monitoring plan.

## When to invoke

- "Publish this Microsoft 365 agent to our organization."
- "Deploy this MCP agent to selected users or groups."
- "Block or approve a shared agent in the admin center."
- "Set up governance and monitoring for Microsoft 365 agents."
- "Why is an agent not appearing for a user?"

## Prerequisites and context

- Access the Microsoft 365 admin center at https://admin.microsoft.com/ for tenant agent registry, availability, deployment, blocking, and assignment.
- Use the Power Platform admin center at https://admin.powerplatform.microsoft.com/ when the agent is an App Builder agent, Workflows agent, agent studio agent, or flow-backed agent.
- Use Partner Center at https://learn.microsoft.com/en-us/partner-center/ only for public Agent Store submission and validation.
- Required roles: **AI Admin** for full agent management; **Global Reader** for view-only inspection. Reserve Global Administrator for emergency scenarios.
- Confirm the user has the correct Microsoft 365 agent license, group membership, and assignment before treating disappearance as a platform failure.

## Agent types and ownership

| Agent type | Source | Management posture | Watch point |
| --- | --- | --- | --- |
| Published by Organization | Built with predefined instructions and actions | Admin approval, publishing process, organization deployment | Compliance and governance requirements before publishing. |
| Shared by Creator | Created in Microsoft 365 Agent Builder or Agent Builder and shared directly | Visible to admins in the agent registry | Creator, creation date, host products, capability scope, availability status. |
| Microsoft Agents | Developed and maintained by Microsoft | Pre-approved and integrated with Microsoft 365 services | Tenant availability and user experience. |
| External Partner Agents | Verified external developers or vendors | Subject to admin approval and control | Terms of use, privacy statement, permissions, external integrations. |
| Frontier Agents | Experimental or advanced capabilities | Limited rollout and additional oversight | App Builder agent and Workflows agent may require Power Platform admin center. |

## Admin center actions

| Action | Use it when | Required decision |
| --- | --- | --- |
| View Agents | Inspect available, deployed, or blocked agents | Filter by availability, search by name, review details. |
| Publish | Make a submitted organizational agent available | Decide all users, selected security groups, or individuals. |
| Deploy | Assign an approved agent to users | Choose organization-wide, group-based, or individual scope. |
| Block | Stop unsafe or non-compliant use | Record security or compliance reason and review audit logs. |
| Remove | Delete obsolete organization availability | Confirm retirement, communication, and rollback needs. |
| Configure Access | Control what appears in the assistant surface | Map permissions per agent and user assignment. |

Users discover allowed agents in the Microsoft 365 agent hub, the agent picker in the assistant interface, the organization agent catalog, and assistant sidebar surfaces. Users can toggle agents on or off, add or remove agents from their experience, right-click agents to manage preferences, and access only admin-allowed agents.

## Procedure

1. Ask the readiness questions: is the agent ready for deployment or still in development; who should have access; what compliance or security requirements apply; whether it targets organization deployment or the public store; and what monitoring or reporting is needed.
2. Classify the agent type: organization-published, shared by creator, Microsoft, external partner, or frontier.
3. Review security: data access, API permissions, authentication, OAuth flows, external connections, MCP server URL, imported tools, and sensitive-response risk.
4. Review compliance: data residency, privacy policies, terms of use, audit logs, acceptable use policies, and required approvals.
5. Choose deployment route: Agent Store through Partner Center, IT admin organization deployment, group-based assignment, or block/remove.
6. Configure availability in the Microsoft 365 admin center Agents page; for Power Platform-based agents, also configure default environment, environment routing for agent studio, and flows in the Power Platform admin center.
7. Pilot test with a small user group, gather feedback, validate security, document capabilities and limitations, and train users.
8. Roll out in phases, monitor adoption rates, user feedback, satisfaction, error rates, performance, security incidents, and violations.
9. Post-deployment, track metrics, iterate, update, retire obsolete agents, and schedule regular security and compliance audits.

## Deployment patterns

| Pattern | Developer steps | Admin steps |
| --- | --- | --- |
| Publish to Organization | Build with Microsoft 365 Agents Toolkit, test in development, submit for approval, wait for admin review | Review in admin center, validate compliance and security, approve, configure deployment settings, publish to selected users or organization-wide. |
| Deploy via Agent Store | Complete development and testing, package for submission, submit to Partner Center, await validation process, receive approval notification | Discover in agent store, review details and permissions, assign to organization or user groups, monitor usage and feedback. |
| Deploy Organizational Agent | Provide tested package and documentation | Navigate to Agents page, select agent, choose all users, specific security groups, or individual users, set availability status, configure permissions if applicable, deploy and monitor. |

Organization-wide means all employees with a agent license automatically see the agent in the assistant. Group-based means specific departments, teams, security group assignments, or role-based access control.

## MCP-specific validation

| Check | Pass condition |
| --- | --- |
| MCP server URL | Accessible from the expected network and tenant path. |
| Authentication | OAuth 2.0 or SSO configuration is secure and testable. |
| Tools imported | Each MCP tool is appropriate for the agent task and least-privilege. |
| Response data | Tool responses do not expose sensitive info beyond the user's entitlement. |
| Server security | MCP server follows secure hosting, logging, and rate-limit practices. |
| Deployment parity | Same process as REST API agents: review, validate, test authentication flow, deploy to users/groups, monitor performance. |

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| Agent Not Appearing | Deployment status, group assignment, blocked status, license, or stale UI | Check deployment status in admin center, verify assigned group, confirm not blocked, check agent license, refresh assistant interface. |
| Authentication Failures | Invalid OAuth credentials, missing permissions, inaccessible MCP server, broken auth flow | Verify OAuth credentials, check user permissions, confirm MCP server is reachable, test authentication independently. |
| Performance Issues | Slow MCP server, network connectivity, admin-center errors, rate-limited backend | Monitor response times, check network, review error logs, validate rate limits. |
| Compliance Violations | Unsafe behavior or unauthorized data access | Block agent immediately, review audit logs, investigate access patterns, update policies. |

## Governance vocabulary

Keep tenant-management language precise: M365, agent-management, by-step deployment guide, all/groups/individuals assignment, Add/remove and on/off user controls, Enable/disable tenant creation settings, external developers/vendors, and legacy prompt tool names search/codebase plus edit/editFiles only as migration vocabulary, not CLI allowed-tools.

## Output template

```markdown
## MCP agent deployment plan - <agent name>

**Status:** ready | needs remediation | blocked
**Deployment route:** organization deployment | Agent Store | shared-agent governance | block/remove
**Access scope:** all users | security groups | individuals | not assigned

| Area | Decision | Evidence | Action |
| --- | --- | --- | --- |
| Agent type | <published/shared/Microsoft/external/frontier> | <source> | <management action> |
| Admin role | <AI Admin/Global Reader/other> | <available role> | <next step> |
| Security | <pass/fail> | <data/API/auth/MCP review> | <mitigation> |
| Compliance | <pass/fail> | <residency/privacy/audit evidence> | <mitigation> |
| Rollout | <pilot/phased/org-wide> | <target users or groups> | <communication and training> |
| Monitoring | <metrics> | <logs/reports> | <review cadence> |

### Admin center steps
1. <step>
2. <step>
3. <step>

### User communication
<short announcement, access instructions, and support channel>
```

## Quality gate

- [ ] The agent type and deployment route are explicit.
- [ ] Access scope names all users, groups, or individual assignment criteria.
- [ ] AI Admin or Global Reader role requirements are stated.
- [ ] Security review covers data access, API permissions, authentication, external connections, MCP server URL, and tool appropriateness.
- [ ] Compliance review covers data residency, privacy policies, terms of use, and audit logs.
- [ ] Troubleshooting covers Agent Not Appearing, Authentication Failures, Performance Issues, and Compliance Violations when relevant.
- [ ] The output includes deployment steps, governance checklist, assignment recommendations, monitoring plan, and user communication.

## References

- [Microsoft 365 admin center](https://admin.microsoft.com/)
- [Power Platform admin center](https://admin.powerplatform.microsoft.com/)
- [Partner Center for agent submissions](https://learn.microsoft.com/en-us/partner-center/)
- [Microsoft Agent 365 Overview](https://learn.microsoft.com/en-us/microsoft-agent-365/overview)
- [Agent Registry Documentation](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/agent-registry)
