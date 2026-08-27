---
name: docker-compose
description: Use when editing the tracked Backstage agent or MCP Docker Compose development stacks.
paths:
  - backstage/server/docker-compose.yml
  - mcp-servers/docker-compose.yml
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/instructions/docker-compose.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Docker Compose

## Conventions

- Keep Compose for local development and integration only; production runtime controls belong in Kubernetes manifests.
- Build from tracked Dockerfiles and use explicit image tags when an image is referenced.
- Pass configuration through environment variables or ignored env files; never embed credentials or production defaults.
- Add health checks for dependencies and use health-based `depends_on` conditions where startup order matters.
- Use named networks and volumes with service-specific access; avoid host networking and privileged containers.
- Bind developer ports deliberately and avoid exposing databases or internal agent services beyond localhost without a documented need.
- Keep service names, container ports, and health paths aligned with the corresponding application contracts.

## Verification

- `docker compose config` renders without unresolved required variables.
- Health checks and dependency conditions describe the actual startup behavior.
- The rendered configuration contains no committed secret or mutable `latest` tag.

## Do / Do Not

| Do | Do not |
| --- | --- |
| Keep ports, health checks, dependencies, and application contracts aligned. | Encode startup assumptions that the service does not satisfy. |
| Render configuration with explicit variables and immutable images. | Commit secrets or use mutable image tags. |

## Checklist Before Opening a PR

- [ ] The change matches this instruction's `applyTo` scope.
- [ ] `docker compose config` resolves all required variables.
- [ ] Health and dependency behavior match the application contract.
- [ ] Rendered output contains no secret or mutable image tag.
- [ ] No unrelated edits or unresolved placeholders remain.
