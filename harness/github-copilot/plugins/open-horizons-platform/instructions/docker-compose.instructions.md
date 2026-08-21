---
applyTo: "**/docker-compose.yml"
description: "Use when editing Docker Compose files for local Open Horizons agent, MCP, and Backstage development services."
---

# Docker Compose Conventions — Local Agent and MCP Services

This file activates when you edit `docker-compose.yml` files such as `backstage/server/docker-compose.yml`, `mcp-servers/docker-compose.yml`, and Golden Path MCP skeletons. It teaches how Open Horizons wires local agent APIs, MCP ecosystem services, ports, health checks, networks, and developer-only mounts. It does **not** cover image construction, which belongs to the `dockerfile` instructions, production Kubernetes manifests, which belong to the `kubernetes` instructions, shell orchestration around Compose, which belongs to the `shell` instructions, or TypeScript service code inside Backstage packages, which belongs to the `typescript` instructions.


## Authoritative Sources and Precedence

Follow these sources in order:

1. Repository files matched by `applyTo: "**/docker-compose.yml"` for existing local patterns.
2. This `docker-compose` instruction file for passive conventions, boundaries, and examples.
3. Official upstream documentation only when it is consistent with repository conventions.

When sources conflict, the higher-priority source wins. Do not duplicate or weaken rules owned by another primitive.

## Responsibility Split

This file owns passive conventions for docker compose conventions — local agent and mcp services. Use the `open-horizons-backstage-deployment` and `mcp-ecosystem` skills for ordered procedures, command sequences, setup, validation, or troubleshooting that goes beyond these rules.

> [!NOTE]
> Compose is for local development and validation. Production runtime configuration belongs in `backstage/k8s/`, `deploy/helm/`, and ArgoCD applications.

## Service Shape

Name services after the platform component and keep host ports local when the service is developer-facing. Existing services use names such as `agent-api`, `agent-api-maf`, `agent-api-impact`, and `mcp-ecosystem`.

```yaml
# Wrong: exposes every interface and hides service intent under a generic name.
services:
  server:
    image: node:latest
    ports:
      - "3100:3100"
```

```yaml
services:
  mcp-ecosystem:
    build: .
    container_name: mcp-ecosystem
    restart: unless-stopped
    ports:
      - "127.0.0.1:${MCP_ECOSYSTEM_PORT:-3100}:3100"
```

## Environment and Secrets

Use `env_file` for local configuration and never commit credentials in `environment`. Optional env files are acceptable when a service can run without tokens, as in the MCP ecosystem service.

```yaml
# Wrong: commits a token-shaped secret directly in the compose file.
environment:
  - GITHUB_TOKEN=ghp_exampletokenvalue
```

```yaml
env_file:
  - path: .env
    required: false
environment:
  - PORT=3100
  - CACHE_DIR=/app/cache
```

> [!WARNING]
> Do not mount writable cloud credential directories unless the local service truly needs them. Prefer read-only mounts and document why the mount exists.

## Health Checks and Networks

Every long-running local service needs a health check with explicit intervals. Agent APIs currently check FastAPI `/health` endpoints with Python and MCP checks `/health` with `wget`.

```yaml
# Wrong: no health signal, no restart policy, and an implicit default network.
services:
  agent-api:
    build: ./agent-api
```

```yaml
services:
  agent-api:
    build:
      context: ./agent-api
      dockerfile: Dockerfile
    healthcheck:
      test: ["CMD", "python", "-c", "import httpx; httpx.get('http://localhost:8008/health')"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 10s
    restart: unless-stopped
    networks:
      - agent-network
```

> [!IMPORTANT]
> If a Compose file declares `external: true` networks, document how the developer creates them or keep the command in the adjacent README/script.

## Volumes and Bind Mounts

Use named volumes for cache or application data. Bind mounts are allowed only for development workflows and credential access that cannot be represented another way.

```yaml
# Wrong: anonymous volume hides data lifecycle and is hard to clean up.
volumes:
  - /app/cache
```

```yaml
volumes:
  - mcp-cache:/app/cache

volumes:
  mcp-cache:
    driver: local
```

## Conventions

| Rule | Rationale |
|---|---|
| Use platform service names such as `agent-api` and `mcp-ecosystem` | Logs, scripts, and troubleshooting docs rely on recognizable component names. |
| Bind developer-facing ports to `127.0.0.1` unless remote access is intentional | Local services should not be exposed on every interface by default. |
| Use `env_file` and variable defaults instead of committed secret values | Developers can run locally without leaking credentials into Git. |
| Add `healthcheck`, `restart: unless-stopped`, and explicit network membership for services | Local orchestration and validation scripts need deterministic readiness signals. |
| Use named volumes for caches and data | Named volumes make cleanup and persistence explicit. |
| Keep build context scoped to the service directory | Smaller contexts avoid leaking unrelated repository files into image builds. |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `127.0.0.1:8008:8008` for local agent APIs | Publish `8008:8008` without a reason. |
| Mark optional env files with `required: false` when the service supports unauthenticated local mode | Require secrets for every local startup path. |
| Keep Docker image details in the referenced `Dockerfile` | Duplicate build logic in Compose commands. |
| Use named networks for multi-service communication | Depend on legacy `links` or implicit names. |

## Checklist Before Opening a PR

- [ ] Services have descriptive names and stable `container_name` values where existing scripts expect them.
- [ ] Host ports are localhost-bound or explicitly justified.
- [ ] No secrets, tokens, or connection strings are committed in `environment`.
- [ ] Each long-running service has a health check and restart policy.
- [ ] Volumes and external networks are named and documented.
- [ ] Related production changes are made in Kubernetes or Helm files, not only Compose.
