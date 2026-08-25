---
name: azure-entra-agent-user
description: >-
  Designs and provisions a Microsoft Entra agent user linked to an Agent ID identity, including parent validation, least-privilege permissions, optional manager, usage location, licensing, and verification. Use when an agent needs a user-shaped directory identity for collaboration workloads.
---

# Microsoft Entra agent user

Create one passwordless agent user with a validated Agent ID parent and explicit governance.

## When to invoke

- Give a Microsoft Agent ID agent a user-shaped Entra identity.
- Enable approved mailbox, Teams, group, or organizational-directory scenarios.
- Validate an existing agent user's identity parent.
- Configure an optional manager, usage location, or license.

## Prerequisites and context

- Microsoft Entra tenant and an existing Agent ID service identity.
- Least-privilege Graph permission, preferably `AgentIdUser.ReadWrite.IdentityParentedBy`.
- Required delegated/admin role and explicit approval for user or license creation.
- Unique UPN and mail nickname; one agent user is allowed per parent identity.

## Criteria

- `identityParentId` is the object ID of an agent identity with
  `servicePrincipalType: ServiceIdentity`, not a regular application service principal.
- Agent users have no password; authentication is derived from the parent identity.
- `userPrincipalName` is unique in the tenant.
- Set `usageLocation` before assigning a license.
- Manager assignment is optional and uses a valid directory user reference.

## Procedure

1. Confirm business purpose, data access, lifecycle owner, UPN, manager, and license requirement.
2. Read the parent service principal and verify the Agent ID identity type.
3. Check whether the parent already has an agent user; stop on the one-to-one constraint.
4. Create the agent user with `accountEnabled`, `displayName`, `mailNickname`, unique UPN, and
   `identityParentId`.
5. Optionally assign a manager.
6. If licensing is approved, set usage location first, then assign the exact SKU.
7. Verify parent linkage, directory identity, lifecycle owner, and expected token/user behavior.

Creation shape:

```json
{
  "@odata.type": "#microsoft.graph.agentUser",
  "accountEnabled": true,
  "displayName": "<display-name>",
  "mailNickname": "<alias>",
  "userPrincipalName": "<unique-upn>",
  "identityParentId": "<agent-identity-object-id>"
}
```

## Output template

```markdown
## Microsoft Entra agent user result

**Status:** CREATED | READY | BLOCKED
**Parent identity:** <object ID and verified type>
**Agent user:** <object ID/UPN or planned value>

### Governance
- Lifecycle owner: <owner>
- Manager: <assigned/not requested>
- Usage location/license: <result/not requested>
- Permissions used: <Graph permission and role>

### Validation
- Parent type and one-to-one check: <pass/fail>
- Agent user linkage: <pass/fail/not run>
```

## Limits

- Do not use a regular app service principal as the identity parent.
- Do not create passwords, assign privileged admin roles, or add role-assignable groups.
- Do not assign licenses without approval, usage location, and a lifecycle owner.
- Do not promise immediate mailbox, Teams, or org-chart propagation; service provisioning is asynchronous.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `azure-role-selector` | `skill` | Least-privilege Azure RBAC is also required. |
| `open-horizons-security-reviewer` | `agent` | Identity scope or collaboration data needs independent review. |
| `foundry-agent-blueprint` | `skill` | The user identity belongs to a Foundry agent design. |

## Quality gate

- [ ] Parent is verified as an Agent ID service identity.
- [ ] No existing agent user is linked to the parent.
- [ ] UPN, owner, manager, and license intent are explicit.
- [ ] No password or excessive permission is introduced.
- [ ] Linkage and optional license state are verified without exposing tokens.

## References

- [Microsoft Entra Agent ID documentation](https://learn.microsoft.com/entra/agent-id/)