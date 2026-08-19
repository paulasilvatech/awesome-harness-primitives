#!/usr/bin/env python3
"""Generate planning artifacts for a Backstage plugin."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


PLUGIN_TYPES = {
    "frontend",
    "backend",
    "backend-module",
    "catalog",
    "scaffolder",
    "search",
    "auth",
    "permission",
    "techdocs",
    "common",
    "node",
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"wrote {path}")


def heading(title: str) -> str:
    return f"# {title}\n\nGenerated: {dt.date.today().isoformat()}\n"


def plan(args: argparse.Namespace) -> str:
    return f"""
{heading(f"{args.plugin_id} Backstage Plugin Plan")}
## Summary

- Plugin ID: `{args.plugin_id}`
- Plugin type: `{args.plugin_type}`
- Audience: `{args.audience}`
- Target Backstage version: `{args.target_version}`

## Problem

Describe the user problem and why a Backstage plugin is the right extension point.

## Users

List primary users, secondary users, and maintainers.

## Scope

- In scope: first useful feature slice.
- Out of scope: unrelated Backstage app customization.

## Acceptance Criteria

- Plugin can be installed or integrated in the target Backstage app.
- Lint, typecheck, test, and build commands pass where available.
- README, config, and ownership metadata are present.
- Security and permission requirements are documented.

## Open Questions

- Which external APIs are required?
- Which auth provider and permissions apply?
- Is this internal, private package, or community candidate?
"""


def strategy(args: argparse.Namespace) -> str:
    return f"""
{heading(f"{args.plugin_id} Strategy")}
## Build Strategy

Use official Backstage plugin APIs for `{args.plugin_type}`. Keep plugin code packaged separately from the app shell unless this is a one-off internal customization.

## Packaging Strategy

- Internal app integration: workspace package dependency.
- Private distribution: private npm package or internal registry.
- Community candidate: prepare contribution package and maintainer review.

## Configuration Strategy

Document required `app-config.yaml` keys, environment variables, and safe defaults. Do not put secrets in source or examples.

## Security Strategy

Validate input at the boundary, use Backstage identity and permission APIs where applicable, and deny by default when ownership is unknown.

## Observability Strategy

Backend plugins should log meaningful events and errors. Avoid logging tokens, profile claims, or sensitive response bodies.
"""


def adr(args: argparse.Namespace) -> str:
    return f"""
{heading("ADR 0001, Plugin Architecture")}
## Status

Proposed

## Context

The team needs a `{args.plugin_type}` plugin named `{args.plugin_id}` for `{args.audience}` use.

## Decision

Use official Backstage plugin APIs and keep the plugin package independently testable.

## Alternatives Considered

- App-only customization.
- Standalone service outside Backstage.
- Dynamic runtime packaging as the primary architecture.

## Consequences

- The plugin follows Backstage versioning and integration practices.
- Publication path depends on the selected audience.
- Community publication requires maintainer review and is not guaranteed.
"""


def architecture(args: argparse.Namespace) -> str:
    return f"""
{heading(f"{args.plugin_id} Architecture")}
## Runtime View

```mermaid
flowchart LR
  User[Backstage user] --> App[Backstage app]
  App --> Plugin[{args.plugin_id}]
  Plugin --> Config[app-config.yaml]
  Plugin --> API[External or internal API]
```

## Package Boundaries

| Package | Responsibility |
| --- | --- |
| `{args.plugin_id}` | Main plugin entry point. |
| `{args.plugin_id}-backend` | Backend API, if required. |
| `{args.plugin_id}-common` | Shared types and schemas, if required. |
| `{args.plugin_id}-node` | Backend extension points or utilities, if required. |

## Extension Points

List Backstage extension points, route refs, external route refs, permission rules, or catalog processors used by this plugin.
"""


def validation(args: argparse.Namespace) -> str:
    return f"""
{heading(f"{args.plugin_id} Validation")}
## Commands

Run commands that exist in the target package:

```bash
yarn lint
yarn tsc
yarn test
yarn build
npm pack --dry-run
```

## Checklist

- [ ] `package.json` has name, version, license, repository, scripts, and files.
- [ ] `README.md` documents purpose, install, config, auth, permissions, and development.
- [ ] `catalog-info.yaml` exists for packages intended to be cataloged.
- [ ] Tests cover the first useful feature slice.
- [ ] No secrets, internal URLs, or customer names are present.
- [ ] Community publication readiness is documented when applicable.
"""


def publication(args: argparse.Namespace) -> str:
    return f"""
{heading(f"{args.plugin_id} Publication")}
## Publication Mode

Audience: `{args.audience}`

## Paths

- Internal: integrate into the target Backstage app workspace.
- Private package: publish to private npm or internal registry.
- Community candidate: prepare issue or pull request for `backstage/community-plugins`.

## Community Warning

Official community publication depends on maintainer review. This artifact prepares the package and contribution plan; it does not guarantee acceptance.

## Community Checklist

- [ ] Existing plugins and issues checked for overlap.
- [ ] Plugin is generic beyond one company.
- [ ] Maintainer ownership is documented.
- [ ] README, license, tests, package metadata, and catalog metadata are present.
- [ ] PR follows the community repository contribution guide.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Backstage plugin planning artifacts")
    parser.add_argument("--plugin-id", required=True)
    parser.add_argument("--plugin-type", required=True, choices=sorted(PLUGIN_TYPES))
    parser.add_argument("--audience", default="internal", choices=["internal", "private", "community"])
    parser.add_argument("--target-version", default="unspecified")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    write(output / "PLAN.md", plan(args))
    write(output / "STRATEGY.md", strategy(args))
    write(output / "adr" / "0001-plugin-architecture.md", adr(args))
    write(output / "ARCHITECTURE.md", architecture(args))
    write(output / "VALIDATION.md", validation(args))
    write(output / "PUBLICATION.md", publication(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
