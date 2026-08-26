---
name: open-horizons-backstage-mcp-actions
description: "Register typed Backstage backend actions and expose selected actions as authenticated MCP tools with schemas, attributes, permissions, filters, server instructions, and well-known action validation. Use when configuring the Actions Registry, Actions Service, MCP Actions Backend, or AI tool exposure."
---

# Backstage MCP actions

Expose only intentionally registered and authorized Backstage actions to AI clients.

## When to invoke

- "Install the MCP Actions Backend."
- "Register a Backstage action as an MCP tool."
- "Split catalog and scaffolder actions into focused MCP servers."
- "Review Backstage well-known actions and destructive attributes."

## Procedure

1. Confirm the Backstage version and that Actions Registry and MCP Actions APIs are available.
2. Read [the current well-known action inventory](references/well-known-actions.md) and the
   repository's registered actions.
3. Register custom actions with input, output, and optional secrets schemas.
4. Set `readOnly`, `idempotent`, and `destructive` attributes explicitly; conservative defaults
   otherwise treat actions as mutating.
5. Add a basic `visibilityPermission` when action listing or invocation needs policy control.
6. Install `@backstage/plugin-mcp-actions-backend` and register it in the backend.
7. Restrict `backend.actions.pluginSources` and configure include/exclude rules by ID and
   attributes.
8. Keep namespaced tool names unless backward compatibility requires otherwise.
9. Choose one server or multiple focused servers with capability-oriented descriptions and usage
   instructions.
10. Configure authentication. Prefer supported OAuth/CIMD for interactive users; treat static
    tokens as a temporary, restricted external-access mechanism.
11. Test list visibility, schema validation, permission denial, secrets separation, safe read-only
    invocation, and approval for destructive actions.

## Safety

- Secrets schemas stay out of tool definitions and LLM context.
- Denied actions should not be discoverable or invokable.
- Exclude destructive actions from general-purpose servers by default.
- `auth.who-am-i` requires user credentials, not service or unauthenticated credentials.

## Output template

```markdown
## Backstage MCP actions result

| Server | Included actions | Exclusions | Auth | Endpoint |
| --- | --- | --- | --- | --- |

### Action controls
| Action | Attributes | Permission | Validation |
| --- | --- | --- | --- |
```

## Progressive disclosure and bundled resources

- `references/well-known-actions.md`: action discovery, schemas, attributes, and well-known endpoint details.

## Quality gate

- [ ] Action schemas and behavioral attributes are explicit.
- [ ] Secrets are separated from ordinary inputs.
- [ ] Plugin sources and action filters implement least privilege.
- [ ] Permission visibility and denial behavior are tested.
- [ ] Server descriptions state capabilities rather than protocol identity.
- [ ] Authentication and destructive-action approvals are validated.

## References

- [MCP Actions Backend](https://backstage.io/docs/ai/mcp-actions)
- [Well-known actions](https://backstage.io/docs/ai/well-known-actions)
- [Actions Registry](https://backstage.io/docs/backend-system/core-services/actions-registry)
