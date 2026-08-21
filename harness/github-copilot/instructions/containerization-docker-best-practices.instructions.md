---
applyTo: "**/Dockerfile,**/Dockerfile.*,**/*.dockerfile,**/docker-compose*.yml,**/docker-compose*.yaml,**/compose*.yml,**/compose*.yaml"
description: "Enforces Dockerfile and Compose conventions for optimized, secure, reproducible container images and container runtime configuration."
---

# Containerization and Docker Conventions — Secure Reproducible Images

These instructions apply to Dockerfiles, Docker Compose files, and container build or runtime definitions matched by the `applyTo` globs. They are authoritative for image immutability, portability, isolation, build layering, base-image selection, secrets handling, security scanning, health checks, runtime resources, logging, storage, and networking in those files; orchestrator-specific platform primitives win where they define stricter Kubernetes, cloud, or deployment rules. Treat these as passive conventions for producing efficient, secure, maintainable container artifacts, not as a step-by-step deployment workflow.

## Core Container Principles

| Principle | Convention | Rationale |
| --- | --- | --- |
| Immutability | Build a new image for every code or configuration change; never patch a running production container. | Immutable artifacts enable rollback by switching tags and prevent untracked runtime drift. |
| Reproducible builds | Pin dependency versions, control build inputs, and avoid nondeterministic install steps. | The same inputs should produce the same image so CI, staging, and production stay aligned. |
| Image versioning | Tag production images with meaningful immutable tags such as `v1.2.3`; reserve `latest` for development only. | Operators need a clear history of what each image contains. |
| Portability | Externalize environment-specific configuration through environment variables, mounted config, or external configuration services. | The same image should run locally, in cloud environments, and on-premise without rebuilding. |
| Isolation | Run one clear primary process per container, communicate through container networks, and use named volumes for persistent state. | Process, filesystem, network, CPU, memory, and I/O isolation protect neighboring workloads. |
| Efficiency | Keep images small with multi-stage builds, minimal bases, selective copies, and no production-only debugging baggage. | Smaller images build, scan, push, pull, and start faster with fewer vulnerable packages. |

## Dockerfile Build Structure

Use multi-stage builds whenever build tools, compilers, tests, or development dependencies are not required at runtime. Name stages clearly (`AS deps`, `AS build`, `AS test`, `AS production`) and transfer only required artifacts with `COPY --from=<stage>`.

**Good:**

```dockerfile
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY src/ ./src/
COPY public/ ./public/
RUN npm run build

FROM build AS test
RUN npm run test
RUN npm run lint

FROM node:18-alpine AS production
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY --from=build /app/package*.json ./
USER node
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

Why: Build, test, and runtime dependencies are separated, final layers contain only runtime artifacts, and the process runs as a non-root user.

**Bad:**

```dockerfile
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
COPY . .
CMD python3 app.py
```

Why: It uses a broad base image, creates avoidable layers, loses cache efficiency, keeps cleanup in later layers, copies the whole context, and runs without an explicit non-root user.

## Base Images and Layer Caching

Prefer official, maintained, versioned base images from Docker Hub or a trusted provider. Choose minimal variants such as `alpine`, `slim`, or `distroless` when they satisfy runtime needs, and verify the image supports required architectures such as `x86_64` and `ARM64`. Use language-specific minimal images such as `node:18-alpine`, `python:3.9-slim-buster`, `openjdk:17-jre-slim`, or `gcr.io/distroless/nodejs18-debian11` instead of broad bases such as `ubuntu:20.04` unless the broader OS is required.

Order layers from least frequently changed to most frequently changed. Copy dependency manifests (`package.json`, `package-lock.json`, `requirements.txt`) before source files, run dependency installation before `COPY src/ ./src/`, and avoid `COPY . .` when only `src/`, `public/`, or `config/` is needed. Combine related package-manager commands and cleanup in the same `RUN` statement, for example `apt-get update && apt-get install -y ... && apt-get clean && rm -rf /var/lib/apt/lists/*`.

## Build Context and `.dockerignore`

Maintain a `.dockerignore` that excludes version-control data, host dependencies, generated build artifacts, local secrets, IDE files, OS files, documentation, coverage, and tests that are not needed in the build context. Include patterns such as `.git*`, `node_modules`, `vendor`, `__pycache__`, `dist`, `build`, `*.o`, `*.so`, `.env.*`, `*.log`, `coverage`, `.nyc_output`, `.vscode`, `.idea`, `*.swp`, `*.swo`, `.DS_Store`, `Thumbs.db`, `*.md`, `docs/`, `test/`, `tests/`, `spec/`, and `__tests__/` when they match the project. Keep `.dockerignore` aligned with project structure so sensitive files and unnecessary content never reach the Docker daemon.

## Runtime User, Ports, Commands, and Configuration

Run application processes as a non-root user. Create a dedicated user or use the official image's non-root user, set ownership before switching users, and make writable paths explicit with `VOLUME` only when persistence is required. Use `EXPOSE` to document the application port; publish ports with runtime configuration rather than relying on `EXPOSE` to make the service reachable.

Prefer exec-form `CMD` and `ENTRYPOINT` for signal handling: use `ENTRYPOINT ["/app/start.sh"]` with `CMD ["--config", "prod.conf"]` when the executable is fixed, or simple `CMD ["node", "dist/main.js"]` when no fixed entrypoint is needed. Keep startup scripts small and deterministic.

Externalize configuration with environment variables and mounted files. Use `ENV NODE_ENV=production`, `ENV PORT=3000`, and `ENV LOG_LEVEL=info` only for safe defaults; use `ARG BUILD_VERSION` and `ENV APP_VERSION=$BUILD_VERSION` for build metadata; validate required configuration at application startup. Never bake credentials into `ENV`, `ARG`, image files, or image history.

## Security, Supply Chain, and Secrets

| Concern | Convention | Rationale |
| --- | --- | --- |
| Non-root execution | Define `USER <non-root-user>` for production images and grant only required permissions. | Least privilege limits the impact of runtime vulnerabilities. |
| Minimal bases | Prefer `alpine`, `slim`, and `distroless` variants where compatible. | Fewer packages reduce attack surface and scan noise. |
| Dockerfile linting | Run `hadolint` on Dockerfiles. | Static checks catch insecure or inefficient instructions before images are built. |
| Image scanning | Scan built images with `Trivy`, `Clair`, or `Snyk Container`; fail builds on critical vulnerabilities. | Vulnerable base or application layers should not reach production. |
| Signing | Sign and verify production images with Notary, Docker Content Trust, or Cosign. | Signatures prove the image was not tampered with and came from a trusted pipeline. |
| Capabilities | Drop unnecessary capabilities such as `NET_RAW` and `SYS_ADMIN`; use `CAP_DROP`, `--cap-drop=ALL`, and `--security-opt=no-new-privileges` where available. | Reduced Linux capabilities limit privilege escalation. |
| Filesystem | Use read-only root filesystems and read-only mounts for sensitive data when the app allows it. | Runtime writes should be deliberate and isolated. |
| Secrets | Use Kubernetes Secrets, Docker Secrets, HashiCorp Vault, environment injection, or mounted secret files at runtime. | Files such as `secrets.txt` remain extractable from image history even if deleted later. |

Use `cosign sign -key cosign.key myregistry.com/myapp:v1.0.0` and `cosign verify -key cosign.pub myregistry.com/myapp:v1.0.0` for Cosign-managed signing. In CI, run `docker run --rm -i hadolint/hadolint < Dockerfile`, build with `docker build -t myapp .`, and scan with `trivy image myapp`.

## Health Checks and Runtime Operations

Define lightweight health checks that reflect application readiness without creating heavy load. Use Dockerfile `HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD curl --fail http://localhost:8080/health || exit 1` when `curl` is present, or an application-specific check such as `CMD node healthcheck.js || exit 1`. Distinguish liveness probes from readiness probes in orchestrators when the application can be alive but not ready for traffic.

Set CPU and memory limits in Compose or orchestrator manifests. For Docker Compose, use `deploy.resources.limits.cpus`, `deploy.resources.limits.memory`, `deploy.resources.reservations.cpus`, and `deploy.resources.reservations.memory`, for example `cpus: '0.5'`, `memory: 512M`, `cpus: '0.25'`, and `memory: 256M`. Monitor usage and tune requests, limits, and Kubernetes resource quotas rather than guessing.

Write logs to `STDOUT` and `STDERR`, prefer structured JSON logs, and integrate with aggregators such as Fluentd, Logstash, or Loki plus monitoring systems such as Prometheus and Grafana. Configure log rotation and retention outside the image.

## Storage, Networking, and Orchestration

Never store durable data in the container writable layer. Use Docker Volumes, Kubernetes Persistent Volumes, bind mounts only when appropriate, or cloud-native storage. For database containers, mount data explicitly and keep credentials in runtime secrets, for example `POSTGRES_PASSWORD_FILE: /run/secrets/db_password` with a `postgres_data:/var/lib/postgresql/data` named volume. Back up persistent volumes and validate restore procedures.

Use custom Docker networks for service isolation. Put public services on a `frontend` network and private dependencies on a `backend` network with `internal: true` when possible. Prefer platform service discovery over hardcoded addresses, and use Kubernetes network policies for pod-to-pod restrictions.

Use Kubernetes or Docker Swarm when the deployment needs scaling, self-healing, rolling updates, service discovery, and load balancing. In Kubernetes manifests, define `apiVersion: apps/v1`, `kind: Deployment`, `metadata.name`, `spec.replicas`, `selector.matchLabels`, pod `template.metadata.labels`, container `resources.requests`, and `resources.limits` with values such as `64Mi`, `128Mi`, `250m`, and `500m`.

## Troubleshooting Patterns

| Symptom | Inspect | Corrective convention |
| --- | --- | --- |
| Large image size | Run `docker history <image>` and review copied files. | Add multi-stage builds, switch to smaller bases, clean temporary files in the same layer, and remove production-unneeded tooling. |
| Slow builds | Review cache invalidation and context size. | Put stable layers first, use `.dockerignore`, and reserve `docker build --no-cache` for troubleshooting cache issues. |
| Container crash | Check `CMD`, `ENTRYPOINT`, dependencies, resource limits, and `docker logs <container_id>`. | Keep the final image self-contained and define clear startup commands. |
| Permission failure | Inspect ownership, `USER`, and mounted volume permissions. | Set `chown` before switching users and make writable paths explicit. |
| Network failure | Check `EXPOSE`, `-p` publishing, network membership, and firewall rules. | Use defined networks and explicit runtime port publishing. |

## Preserved Docker Vocabulary and Review Labels

Keep these terms recognizable when editing existing Docker guidance because they describe commands, labels, platform controls, or troubleshooting categories carried by prior examples: `.env`, `.git`, `ADD secrets.txt /app/secrets.txt`, `AppArmor/SELinux`, `AppArmor`, `SELinux`, `DevOps`, `CI/CD`, `SAST`, `GOOD`, `BETTER`, `Node.js/Python`, `build-time`, `built-in`, `development-only`, `environment-agnostic`, `inter-container`, `cluster-wide`, `large-scale`, `multi-line`, `multi-platform`, `multi-tier`, `one-time`, `zero-downtime`, `and/or`, `file/directory`, `requests/limits.`, `Starting/Crashing**`, `docker run`, `cpu_limits`, `memory_limits`, `openjdk:17`, `RUN npm ci`, `RUN apt-get update && apt-get install -y ...`, `rm -rf /var/lib/apt/lists/*`, `CMD ["executable", "param1"]`, `["command", "arg1", "arg2"]`, `app/data`, and `usr/bin/node`. Preserve them when they refer to real flags, examples, or runtime controls rather than ordinary prose.

## Good / Bad Examples

The examples below illustrate layer optimization and secure runtime defaults.

**Good:**

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY dist/ ./dist/
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && chown -R appuser:appgroup /app
USER appuser
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD node healthcheck.js || exit 1
CMD ["node", "dist/main.js"]
```

Why: Dependency layers are cacheable, runtime files are selective, permissions are explicit, the container runs non-root, and orchestration can detect health.

**Bad:**

```dockerfile
FROM node:latest
WORKDIR /app
COPY . .
ENV API_KEY=secret
RUN npm install
CMD node dist/main.js
```

Why: The base tag floats, the entire context may include secrets or tests, a secret is written to image history, dependencies are not reproducible, and shell-form `CMD` handles signals poorly.

## Conventions

| Rule | Rationale |
| --- | --- |
| Build a new immutable image for every code or configuration change. | Runtime mutation destroys provenance and makes rollback unreliable. |
| Pin base images and dependency versions; avoid `latest` for production. | Reproducibility requires stable inputs. |
| Use multi-stage builds with `COPY --from=<stage>` for compiled apps and heavy build tooling. | Build dependencies stay out of the final image. |
| Choose official minimal bases such as `alpine`, `slim`, or `distroless` when compatible. | Smaller images have fewer vulnerabilities and faster distribution. |
| Optimize layer ordering and combine cleanup in the same `RUN` command. | Cache reuse improves and deleted temporary files do not remain in earlier layers. |
| Maintain `.dockerignore` and use selective `COPY` instructions. | Build contexts stay small and sensitive files stay outside images. |
| Run as a non-root `USER` and document ports with `EXPOSE`. | Least privilege and clear runtime contracts improve security and operations. |
| Use exec-form `CMD` and `ENTRYPOINT`. | Containers receive signals correctly and stop cleanly. |
| Keep secrets out of `ENV`, `ARG`, files, and image layers. | Image history can expose deleted credentials. |
| Scan, lint, sign, and verify production images. | Supply-chain controls catch vulnerabilities and tampering before deployment. |
| Define `HEALTHCHECK`, resource limits, structured logging, persistent volumes, and isolated networks. | Operators can detect failures, contain resource usage, retain state, and limit lateral movement. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `v1.2.3`-style immutable tags for production. | Use `latest` as a production deployment contract. |
| Copy dependency manifests before source files. | Put `COPY . .` before dependency installation unless required. |
| Clean package-manager caches in the same `RUN` layer. | Delete temporary files in a later layer and assume image size shrinks. |
| Add `.git*`, `.env.*`, build artifacts, coverage, and tests to `.dockerignore` when they are not needed. | Send the entire repository and secrets to the Docker daemon. |
| Set `USER appuser` or an equivalent non-root runtime. | Run production containers as `root` for convenience. |
| Use runtime secrets such as Docker Secrets, Kubernetes Secrets, or Vault. | `COPY secrets.txt /app/secrets.txt` or pass sensitive values with `--build-arg`. |
| Drop capabilities and use read-only filesystems where possible. | Keep `NET_RAW`, `SYS_ADMIN`, or broad write access without a requirement. |
| Write container logs to `STDOUT` and `STDERR`. | Write primary logs only to files inside the container. |
| Store durable data in named volumes or Persistent Volumes. | Store persistent data in the writable container layer. |
| Use service discovery and custom networks. | Depend on host networking or hardcoded container IPs. |

## Checklist Before Opening a PR

- [ ] Dockerfiles use multi-stage builds when build tools, compilers, tests, or development dependencies are not needed at runtime.
- [ ] Base images are official, maintained, minimal where compatible, versioned, and not production `latest`.
- [ ] Layer order preserves cache efficiency; package caches and temporary files are cleaned in the same `RUN` instruction.
- [ ] `.dockerignore` excludes repository metadata, local dependencies, build artifacts, secrets, logs, coverage, IDE files, OS files, docs, and tests that the build does not need.
- [ ] `COPY` instructions are selective and do not include sensitive or unnecessary files.
- [ ] The runtime image defines a non-root `USER`, appropriate ownership, `EXPOSE`, and exec-form `CMD` or `ENTRYPOINT`.
- [ ] Configuration is externalized; `NODE_ENV`, `PORT`, `LOG_LEVEL`, `BUILD_VERSION`, and `APP_VERSION` are safe defaults or metadata, not secrets.
- [ ] Images contain no secrets, private keys, credentials, or secret-bearing layers.
- [ ] Dockerfiles and images are linted or scanned with `hadolint`, `Trivy`, `Clair`, or `Snyk Container`, and production images are signed or verified when required.
- [ ] Runtime definitions include health checks, resource limits or reservations, structured logging, persistent volumes for durable data, and isolated networks where applicable.
