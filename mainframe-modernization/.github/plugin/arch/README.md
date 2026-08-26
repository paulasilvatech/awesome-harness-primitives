# arch

Architecture and modernization toolkit.

## What this plugin bundles

This is a **catalog-only** entry. The upstream `arch` plugin referenced a
`doc-and-modernize` skill that is not part of this kit, so no components are
vendored here. The manifest (`plugin.json`) carries metadata only.

## Related kit content

The workshop maintains its own modernization skill,
[`.github/skills/code-modernization/`](../../skills/code-modernization/), which
is discovered natively by Copilot in this repository.

## Upstream references not included

- `doc-and-modernize` (skill) — not present in this kit.

## How it is enabled

Plugins are declared in
[`.github/copilot/settings.json`](../../copilot/settings.json) through the local
`datacorp-mm-team-kit` marketplace
([`marketplace.json`](../marketplace.json)). This entry has no components, so it
is listed in the marketplace catalog but is not enabled. See the
[plugins index](../README.md) for the mechanism and its limitations.
