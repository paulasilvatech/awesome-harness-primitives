# database-data-management

PostgreSQL code review and optimization skills.

## What this plugin bundles

| Component | Type | Location |
|-----------|------|----------|
| `postgresql-code-review` | Skill | [`.github/skills/postgresql-code-review/`](../../skills/postgresql-code-review/) |
| `postgresql-optimization` | Skill | [`.github/skills/postgresql-optimization/`](../../skills/postgresql-optimization/) |

PostgreSQL 16 is the kit's target database, so only the PostgreSQL skills are
bundled.

## Related kit content

The workshop maintains a [`dba`](../../agents/dba.agent.md) persona agent and a
[`query-optimization`](../../skills/query-optimization/) skill. These are the
kit's own artifacts, not one-to-one renames of the upstream `postgresql-dba` or
`sql-optimization` items, so they are not referenced here as substitutes.

## Upstream references not included

- `sql-code-review`, `sql-optimization` (skills) — not present in this kit.
- `ms-sql-dba`, `postgresql-dba` (agents) — not present in this kit.

## How it is enabled

Content under `.github/skills/` is discovered natively by Copilot in this
repository, so these skills work here without any plugin install. The plugin
layer packages them as a named bundle in the local `datacorp-mm-team-kit`
marketplace ([`marketplace.json`](../marketplace.json)) and is declared in
[`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugins index](../README.md) for the mechanism and its limitations.
