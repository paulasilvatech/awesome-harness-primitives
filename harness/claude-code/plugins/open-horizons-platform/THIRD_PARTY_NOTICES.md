# Third-party notices

The package references external MCP implementations that are resolved by the adopter's
runtime. Their source code is not copied into this package.

| Integration | Runtime reference | Project |
| --- | --- | --- |
| Microsoft Learn MCP | Remote HTTPS endpoint | <https://learn.microsoft.com/api/mcp> |
| Azure MCP | `@azure/mcp` | <https://github.com/microsoft/mcp> |
| Infrastructure MCP | Container image declared in `mcp.json` | <https://github.com/hashicorp/terraform-mcp-server> |
| Playwright MCP | `@playwright/mcp` | <https://github.com/microsoft/playwright-mcp> |

Some bundled skills contain upstream reference material under their own `references/`
or license files. Those package-local source references and notices govern the copied
material. Shared component ownership and synchronization are recorded in
`harness/github-copilot/manifests/plugin-sources.json` in the source repository.

## References

- [GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
- [Agent Plugins specification](https://agent-plugins.org/)
