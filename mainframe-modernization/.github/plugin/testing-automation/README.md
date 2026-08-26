# testing-automation

JUnit 5 and Playwright test-generation skills.

## What this plugin bundles

| Component | Type | Location |
|-----------|------|----------|
| `java-junit` | Skill | [`.github/skills/java-junit/`](../../skills/java-junit/) |
| `playwright-generate-test` | Skill | [`.github/skills/playwright-generate-test/`](../../skills/playwright-generate-test/) |

## Related kit content

The workshop maintains testing skills such as
[`tdd-workflow`](../../skills/tdd-workflow/),
[`test-strategy`](../../skills/test-strategy/), and
[`spring-boot-testing`](../../skills/spring-boot-testing/), which cover the
roles of the upstream `tdd-*` agents.

## Upstream references not included

- `ai-prompt-engineering-safety-review`, `csharp-nunit`,
  `playwright-explore-website` (skills) — not present in this kit.
- `playwright-tester`, `tdd-red`, `tdd-green`, `tdd-refactor` (agents) — not
  present in this kit.

## How it is enabled

Content under `.github/skills/` is discovered natively by Copilot in this
repository, so these skills work here without any plugin install. The plugin
layer packages them as a named bundle in the local `datacorp-mm-team-kit`
marketplace ([`marketplace.json`](../marketplace.json)) and is declared in
[`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugins index](../README.md) for the mechanism and its limitations.
