---
applyTo: "backstage/server/docker-compose.yml,mcp-servers/docker-compose.yml"
description: "Use when editing the tracked Backstage agent or MCP Docker Compose development stacks."
---

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
