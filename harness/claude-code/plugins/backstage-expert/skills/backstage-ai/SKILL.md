---
name: backstage-ai
description: >-
  Apply Backstage AI Catalog, Actions Registry, and MCP Actions conventions. Use when editing
  AiResource or mcp-server entities, backend actions, or MCP Actions configuration.
paths:
  - "**/catalog-info.yaml"
  - app-config*.yaml
  - "packages/backend/**/*.{ts,tsx}"
  - "plugins/**/*.{ts,tsx}"
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/backstage-expert/instructions/backstage-ai.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage AI and Actions Conventions

These instructions apply to Backstage AI catalog entities, registered actions, and MCP exposure.
They are authoritative for AI resource metadata, action schemas and attributes, secrets,
permissions, and action filtering in matched files; repository security policy and target-version
first-party APIs win on conflict.

## AI Catalog

- Register the AI model module before adding `AiResource` or `mcp-server` entities.
- Keep skill and rule content at `backstage.io/source-location`.
- Require stable lifecycle and ownership for every AI resource.
- Keep MCP remotes explicit and do not publish private endpoints unintentionally.

## Actions and MCP

- Give every action typed input and output schemas.
- Put external credentials in a secrets schema, not ordinary inputs.
- Set read-only, idempotent, and destructive attributes explicitly.
- Use permissions and include/exclude filters to expose the minimum action set.
- Keep namespaced tool names unless a documented compatibility requirement prevents it.

## Conventions

| Rule | Rationale |
| --- | --- |
| Exclude destructive actions from general-purpose MCP servers. | AI clients must not gain broad mutation capability by discovery. |
| Describe servers by user capabilities. | Clients select tools from descriptions. |
| Validate live action metadata. | The well-known list is intentionally non-exhaustive. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Separate action inputs from secrets. | Put tokens in tool schemas or LLM context. |
| Use OAuth/CIMD where supported. | Treat static tokens as the preferred long-term auth model. |
| Catalog source locations and ownership. | Embed full skill content in entity specs. |

## Checklist Before Opening a PR

- [ ] AI model and MCP Actions packages match the target version.
- [ ] Entity ownership, lifecycle, source locations, and remotes validate.
- [ ] Action schemas, attributes, permissions, and filters are explicit.
- [ ] Secrets remain outside tool definitions and logs.
- [ ] Read-only, denied, and destructive-action paths are tested.
- [ ] No unrelated edits or placeholders remain.

## References

- [AI in the catalog](https://backstage.io/docs/ai/ai-in-the-catalog)
- [MCP Actions Backend](https://backstage.io/docs/ai/mcp-actions)
