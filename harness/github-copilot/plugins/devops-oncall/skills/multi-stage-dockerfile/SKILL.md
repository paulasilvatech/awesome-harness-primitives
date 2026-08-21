---
name: "multi-stage-dockerfile"
description: >-
  Create or improve optimized multi-stage Dockerfiles with builder, dependency, test, and runtime stages. Use when the user asks for a multi-stage structure, smaller image, secure runtime image, Docker layer cache improvements, non-root container, .dockerignore, HEALTHCHECK, or Dockerfile best practices.
---

# Multi-stage Dockerfile

Design a Dockerfile that separates build-time work from runtime execution, minimizes the final image, preserves reproducibility, and avoids leaking tools or secrets into production layers.

## When to invoke

- "Create a multi-stage Dockerfile for this app."
- "Make this Docker image smaller and more secure."
- "Split the Dockerfile into builder and runtime stages."
- "Add .dockerignore, non-root USER, and HEALTHCHECK best practices."

## Stage design

| Stage | Purpose | Common contents | Must not contain |
| --- | --- | --- | --- |
| `deps` | Restore dependency manifests before source changes. | `package-lock.json`, `requirements.txt`, `.csproj`, lockfiles. | Full source when not needed for restore. |
| `builder` | Compile, bundle, transpile, or publish artifacts. | SDK image, compiler, build tools, source code. | Runtime-only secrets. |
| `test` | Optional validation when tests should run during image build. | Test runner and test dependencies. | Production entrypoint assumptions. |
| `runtime` | Run the app with the minimum required files. | Published artifacts, runtime libraries, config defaults, non-root user. | Compilers, package caches, source not needed at runtime. |

Use meaningful names with `AS`, for example `FROM node:18 AS builder`, and order stages as dependencies → build → test → runtime.

## Base image and reproducibility rules

| Decision | Rule |
| --- | --- |
| Image source | Prefer official base images or trusted distroless runtime images. |
| Tags | Pin exact version tags such as `python:3.11-slim`; do not use floating tags like `latest` or bare `python`. |
| Alpine | Use Alpine only when native dependencies, libc assumptions, and debugging needs are compatible. |
| Distroless | Use distroless when the app does not need a shell or package manager at runtime. |
| Runtime dependencies | Install only libraries required to launch the application. |

## Layer, cache, and context patterns

| Pattern | Why it matters |
| --- | --- |
| Copy dependency manifests before source files. | Dependency restore layers remain cached when application code changes. |
| Put frequently changing `COPY . .` late. | Avoid invalidating expensive install/build layers. |
| Add `.dockerignore`. | Exclude `.git`, local build output, caches, secrets, test reports, and dependency directories that should be restored inside the image. |
| Combine related `RUN` commands with `&&`. | Reduce layer count and allow cleanup in the same layer. |
| Use `COPY --chown=<user>:<group>`. | Set ownership without an extra `RUN chown` layer. |
| Use build arguments intentionally. | Keep environment-specific values configurable without baking secrets into layers. |

## Security and runtime practices

- Run as a non-root user with `USER`; create only the required UID/GID and directories.
- Remove build tools, package manager caches, and unnecessary packages from the final image.
- Do not use build secrets through `ARG` or `ENV`; use BuildKit secrets when secrets are unavoidable during build.
- Set restrictive file permissions for copied artifacts.
- Set runtime optimization variables such as `NODE_ENV=production` when they are correct for the framework.
- Add a `HEALTHCHECK` that validates the application process or HTTP endpoint without requiring privileged tools.
- Scan the final image for vulnerabilities with the repository's existing scanner or platform.

## Output template

````markdown
## Multi-stage Dockerfile result - <app>

**Status:** created | updated | recommendation only | blocked
**Runtime image:** `<image:tag>`

### Dockerfile
```dockerfile
FROM <base>:<version> AS deps
<dependency restore commands>

FROM <base>:<version> AS builder
<build commands>

FROM <runtime>:<version> AS runtime
<copy artifacts, configure USER, EXPOSE, HEALTHCHECK, ENTRYPOINT/CMD>
```

### Companion files
```dockerignore
<entries such as .git, build output, caches, secrets, dependency directories>
```

### Validation
- Build command: `docker build -t <image> .` - <pass/fail/not run>
- Runtime check: `<docker run or healthcheck evidence>` - <pass/fail/not run>
````

## Quality gate

- [ ] Build-time tools are absent from the runtime stage.
- [ ] Base images use explicit version tags and the runtime image is minimal for the app.
- [ ] Dependency restore layers are ordered before frequently changing source layers.
- [ ] `.dockerignore` excludes local caches, VCS data, secrets, and generated output.
- [ ] The final stage uses a non-root `USER` unless a documented platform constraint prevents it.
- [ ] Secrets are not stored in `ARG`, `ENV`, image layers, or copied files.
- [ ] `NODE_ENV=production` or equivalent runtime optimization is used only when appropriate.
- [ ] A meaningful `HEALTHCHECK` is included or a reason for omission is documented.
