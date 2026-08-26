# frontend-web-dev

React frontend agent and Playwright test-generation skill.

## What this plugin bundles

| Component | Type | Location |
|-----------|------|----------|
| `expert-react-frontend-engineer` | Agent | [`.github/agents/expert-react-frontend-engineer.agent.md`](../../agents/expert-react-frontend-engineer.agent.md) |
| `playwright-generate-test` | Skill | [`.github/skills/playwright-generate-test/`](../../skills/playwright-generate-test/) |

## Upstream references not included

- `playwright-explore-website` (skill) — not present in this kit.
- `electron-angular-native` (agent) — not present in this kit.

## How it is enabled

Content under `.github/skills/` and `.github/agents/` is discovered natively by
Copilot in this repository, so these components work here without any plugin
install. The plugin layer packages them as a named bundle in the local
`datacorp-mm-team-kit` marketplace ([`marketplace.json`](../marketplace.json))
and is declared in
[`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugins index](../README.md) for the mechanism and its limitations.
