# copilot-sdk

Build agentic applications with the GitHub Copilot SDK.

## What this plugin bundles

| Component | Type | Location |
|-----------|------|----------|
| `copilot-sdk` | Skill | [`.github/skills/copilot-sdk/`](../../skills/copilot-sdk/) |

## How it is enabled

Content under `.github/skills/` is discovered natively by Copilot in this
repository, so this skill works here without any plugin install. The plugin
layer packages it as a named bundle in the local `datacorp-mm-team-kit`
marketplace ([`marketplace.json`](../marketplace.json)) and is declared in
[`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugins index](../README.md) for the mechanism and its limitations.
