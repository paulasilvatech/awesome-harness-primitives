---
applyTo: "**/Dockerfile"
description: "Use when editing Dockerfiles for Backstage, FastAPI agent services, MCP servers, and Golden Path containers."
---

# Dockerfile Conventions — Backstage, Agent APIs, and MCP Images

This file activates when you edit any repository `Dockerfile`, including Backstage backend, FastAPI agent APIs, Foundry gateway, MCP servers, and Golden Path skeletons. It teaches how to build secure, reproducible containers that match Open Horizons runtime expectations. It does **not** cover local service wiring, which belongs to the `docker-compose` instructions, Kubernetes deployment controls, which belong to the `kubernetes` instructions, TypeScript package code, which belongs to the `typescript` instructions, Python API code, which belongs to the `python` instructions, or build scripts, which belong to the `shell` instructions.


## Authoritative Sources and Precedence

Follow these sources in order:

1. Repository files matched by `applyTo: "**/Dockerfile"` for existing local patterns.
2. This `dockerfile` instruction file for passive conventions, boundaries, and examples.
3. Official upstream documentation only when it is consistent with repository conventions.

When sources conflict, the higher-priority source wins. Do not duplicate or weaken rules owned by another primitive.

## Responsibility Split

This file owns passive conventions for dockerfile conventions — backstage, agent apis, and mcp images. Use the `deploy-orchestration` skill for ordered procedures, command sequences, setup, validation, or troubleshooting that goes beyond these rules.

> [!NOTE]
> The Backstage backend Dockerfile is executed with `backstage/` as the build context after `yarn install --immutable`, `yarn tsc`, and `yarn build:backend`.

## Base Images and Runtimes

Pin runtime families already used by the repo: Node `24-trixie-slim` for Backstage backend images and Python slim images for FastAPI services. Never use `latest`.

```dockerfile
# Wrong: mutable base and no runtime contract.
FROM node:latest
```

```dockerfile
FROM node:24-trixie-slim
ENV NODE_ENV=production
```

## User and File Ownership

Run as a non-root user. Backstage uses the built-in `node` user; Python services create an `app` user and chown `/app`.

```dockerfile
# Wrong: leaves the service running as root.
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008"]
```

```dockerfile
RUN groupadd --system app && useradd --system --gid app --home-dir /app --shell /usr/sbin/nologin app
COPY . .
RUN chown -R app:app /app
USER app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008"]
```

> [!WARNING]
> Do not bake Azure, GitHub, OpenAI, or database credentials into images. Runtime configuration comes from Kubernetes Secrets, External Secrets, Compose env files, or platform identity.

## Dependency Installation

Install dependencies from lockfiles or declared requirements with cache-friendly ordering. Use `--no-install-recommends` for Debian packages and remove apt lists in the same layer.

```dockerfile
# Wrong: installs unpinned packages and leaves apt lists in the runtime image.
RUN apt-get update && apt-get install -y git python3-pip
RUN pip install mkdocs-techdocs-core
```

```dockerfile
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked     --mount=type=cache,target=/var/lib/apt,sharing=locked     apt-get update &&     apt-get install -y --no-install-recommends git python3-pip &&     rm -rf /var/lib/apt/lists/* &&     pip3 install --break-system-packages mkdocs-techdocs-core
```

## Build Context and Layer Ordering

Copy package manifests and skeleton bundles before source bundles so Docker cache works with Backstage workspaces. For Python services, copy `requirements.txt` before source files.

```dockerfile
# Wrong: invalidates dependency cache on every source change.
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
```

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

> [!IMPORTANT]
> Add or maintain `.dockerignore` entries when introducing new build contexts so `.git`, local caches, generated artifacts, and secrets are not sent to Docker.

## Runtime Contract

Document ports with `EXPOSE`, use exec-form `CMD`, and align health endpoints with the `kubernetes` instructions and the `docker-compose` instructions.

```dockerfile
# Wrong: shell form obscures signals and argument boundaries.
CMD uvicorn main:app --host 0.0.0.0 --port 8008
```

```dockerfile
EXPOSE 8008
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008"]
```

## Conventions

| Rule | Rationale |
|---|---|
| Pin base images to explicit runtime versions used by the repo | Mutable tags make CI and deployments non-reproducible. |
| Run production containers as non-root | AKS pod security and least-privilege requirements assume non-root workloads. |
| Copy dependency manifests before application source | Docker layer cache stays useful during frequent source edits. |
| Use `--no-install-recommends`, cache mounts, and same-layer cleanup for apt installs | Images stay smaller and reduce vulnerability surface. |
| Use exec-form `CMD` | Containers receive signals correctly during Kubernetes rollouts. |
| Keep secrets out of build args, layers, and image files | Image registries are not secret stores. |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `USER node` or a dedicated `app` user | Run FastAPI, MCP, or Backstage services as root. |
| Use `pip install --no-cache-dir -r requirements.txt` for Python services | Install Python packages after copying all source. |
| Keep Backstage image creation aligned with `yarn build:backend` outputs | Rebuild the whole monorepo inside unrelated service images. |
| Document exposed ports | Depend on implicit runtime ports. |

## Checklist Before Opening a PR

- [ ] Base image tags are explicit and compatible with repository runtime versions.
- [ ] Runtime user is non-root and copied files have appropriate ownership.
- [ ] Dependencies install from lockfiles or requirements before source copies.
- [ ] No credentials or tenant-specific values are baked into layers.
- [ ] `CMD` uses exec form and the port aligns with Compose and Kubernetes manifests.
- [ ] Build context excludes local caches, generated output, and secrets.
