# software-engineering-team

UX/UI designer agent from the software engineering team set.

## What this plugin bundles

| Component | Type | Location |
|-----------|------|----------|
| `se-ux-ui-designer` | Agent | [`.github/agents/se-ux-ui-designer.agent.md`](../../agents/se-ux-ui-designer.agent.md) |

## Related kit content

The workshop ships its own persona and stage agents under
[`.github/agents/`](../../agents/) (for example `software-architect`,
`product-owner`, `tech-writer`, `qa-engineer`). They cover the roles the
upstream `se-*` agents addressed, so those upstream agents are not referenced
here as substitutes.

## Upstream references not included

- `se-gitops-ci-specialist`, `se-product-manager-advisor`,
  `se-responsible-ai-code`, `se-security-reviewer`,
  `se-system-architecture-reviewer`, `se-technical-writer` (agents) — not
  present in this kit.

## How it is enabled

Content under `.github/agents/` is discovered natively by Copilot in this
repository, so this agent works here without any plugin install. The plugin
layer packages it as a named bundle in the local `datacorp-mm-team-kit`
marketplace ([`marketplace.json`](../marketplace.json)) and is declared in
[`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugins index](../README.md) for the mechanism and its limitations.
