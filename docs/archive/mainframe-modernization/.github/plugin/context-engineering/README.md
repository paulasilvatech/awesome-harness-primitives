# context-engineering

Context mapping for maximizing GitHub Copilot effectiveness.

## What this plugin bundles

| Component | Type | Location |
|-----------|------|----------|
| `context-map` | Skill | [`.github/skills/context-map/`](../../skills/context-map/) |

## Related kit content

The workshop also maintains
[`.github/skills/context-audit/`](../../skills/context-audit/) and
[`.github/skills/refactor-safely/`](../../skills/refactor-safely/), which are the
kit's own equivalents of the upstream `what-context-needed` and `refactor-plan`
skills.

## Upstream references not included

- `refactor-plan`, `what-context-needed` (skills) — the kit uses
  `refactor-safely` and `context-audit` instead.
- `context-architect` (agent) — not present in this kit.

## How it is enabled

Content under `.github/skills/` is discovered natively by Copilot in this
repository, so this skill works here without any plugin install. The plugin
layer packages it as a named bundle in the local `datacorp-mm-team-kit`
marketplace ([`marketplace.json`](../marketplace.json)) and is declared in
[`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugins index](../README.md) for the mechanism and its limitations.
