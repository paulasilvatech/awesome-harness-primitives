# chromium-control-canvas

Interactive Chromium control canvas.

## What this plugin bundles

This is a **catalog-only** entry. The upstream plugin shipped a CLI *extension*
payload (an `extensions/` component), which is not vendored in this kit. The
manifest (`plugin.json`) carries metadata only.

## Upstream references not included

- `chromium-control-canvas` (CLI extension) — no `extensions/` payload is
  committed in this kit.

## How it is enabled

Plugins are declared in
[`.github/copilot/settings.json`](../../copilot/settings.json) through the local
`datacorp-mm-team-kit` marketplace
([`marketplace.json`](../marketplace.json)). This entry has no components, so it
is listed in the marketplace catalog but is not enabled. See the
[plugins index](../README.md) for the mechanism and its limitations.
