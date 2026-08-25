---
applyTo: "backstage/**/Dockerfile,mcp-servers/Dockerfile,scripts/golden-paths/**/Dockerfile"
description: "Use when editing tracked Backstage, agent, MCP, or Golden Path Dockerfiles."
---

# Dockerfiles

## Conventions

- Pin base images to an explicit supported version; production Dockerfiles must not use `latest`.
- Use multi-stage builds so compilers, caches, tests, and development dependencies stay out of the runtime image.
- Copy dependency manifests before source to preserve cacheability and use the package manager matching the lockfile.
- Run the final process as a non-root user with only required files and writable directories.
- Keep credentials out of `ARG`, `ENV`, layers, build context, and package-manager configuration; use build secrets only in approved CI.
- Use exec-form entrypoints, propagate termination signals, and expose only documented service ports.
- Minimize packages, remove caches in the same layer, and keep runtime versions aligned with local manifests.
- Keep health behavior consistent with Compose and Kubernetes probes rather than adding a conflicting endpoint.

## Verification

- The intended target builds from a clean context.
- Image inspection confirms the non-root user, pinned base, and absence of secret material.
- The container starts and responds on its documented health endpoint.
