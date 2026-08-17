---
name: 'multi-stage-dockerfile'
description: 'Create optimized multi-stage Dockerfiles that reduce image size, improve security, and preserve reproducible builds.'
agent: 'agent'
tools: ['codebase']
---

# /multi-stage-dockerfile

## Objective

Create or review an efficient multi-stage Dockerfile that uses separate build and runtime stages, minimizes image size, improves security, preserves reproducible builds, and keeps only the files and packages required at runtime.

## When to Invoke

Use this prompt when creating a Dockerfile, converting a single-stage Dockerfile to a multi-stage build, reducing image size, tightening container security, or improving build caching and reproducibility.

## Preconditions

- The application language, build command, runtime command, and package manager are known or discoverable.
- The repository contains the files needed to infer dependencies and runtime artifacts.
- The target container runtime requirements and health endpoint, if any, are known.
- Edits to Dockerfile and `.dockerignore` are permitted when implementation is requested.

## Inputs the Team Must Provide

- `target` — the application directory or existing Dockerfile to create or improve.
- Build and runtime commands, ports, environment variables, and expected artifacts.
- Preferred base image family or constraints, such as distroless, slim, Alpine, or official language images.
- Whether vulnerability scanning, test stages, or healthchecks are required.
- Ask the user for anything that is missing, especially runtime command or artifact location.

## What I Will Do

- Use a builder stage for compilation, dependency installation, and build-time operations.
- Use a separate runtime stage that contains only the artifacts and dependencies needed to run.
- Choose official minimal base images with exact version tags and meaningful stage names using `AS`, such as `FROM node:18 AS builder`.
- Optimize layers, cache behavior, `.dockerignore`, permissions, non-root execution, and final image content.
- Recommend vulnerability scanning and add a `HEALTHCHECK` instruction when appropriate for the application type.

## What I Will NOT Do

- Use floating base-image tags such as `latest` when reproducibility matters.
- Copy source, package manager caches, build tools, secrets, or unnecessary packages into the final image.
- Run containers as root unless the application requires it and the risk is documented.
- Pick Alpine or distroless images when they are incompatible with required native dependencies.
- Add unrelated orchestration, registry, or deployment configuration unless requested.

## Output Format

Return or apply the Dockerfile changes with this structure:

```markdown
### Multi-Stage Dockerfile Result

### Target
- `<application path or Dockerfile>`

### Dockerfile Outline

    FROM <official-runtime-or-sdk>:<exact-version> AS dependencies
    # install dependencies that change less frequently

    FROM dependencies AS build
    # compile, bundle, or publish the application

    FROM build AS test
    # optional test stage when requested

    FROM <official-minimal-runtime>:<exact-version> AS runtime
    # copy only runtime artifacts, set non-root USER, configure ENV, expose port, and add HEALTHCHECK when appropriate

### Practices Applied
- Builder and runtime stages are separate.
- Stage order is dependencies → build → test → runtime.
- `.dockerignore` excludes unnecessary build context.
- `COPY --chown` or equivalent sets ownership in one step.
- Related `RUN` commands are combined with `&&` where it improves layer count without harming readability.
- Runtime uses `USER` for a non-root account.

### Validation
- Command: `<docker build, scanner, or not run>`
- Result: `<passed, failed, or not run with reason>`
```

## Definition of Done

- [ ] Build-time tools stay out of the final runtime image.
- [ ] Base images are official, minimal where possible, and pinned to exact version tags.
- [ ] Layers are ordered from least to most frequently changing and `.dockerignore` is present or recommended.
- [ ] Runtime permissions, non-root user, and file ownership are handled safely.
- [ ] Runtime configuration and `HEALTHCHECK` are appropriate for the application.
- [ ] Build or validation evidence is reported, or a precise not-run reason is provided.

## Prompt Body

Follow these steps in order. Preserve the application build and runtime behavior.

**Step 1 — Identify build and runtime needs.** Inspect the application type, dependency files, build command, runtime command, artifact path, ports, environment variables, and health endpoint. Ask for missing runtime details before writing a Dockerfile.

**Step 2 — Design the Multi-Stage Structure.** Use a builder stage for compilation, dependency installation, and other build-time operations. Use a separate runtime stage with only what is needed to run. Copy only necessary artifacts from builder to runtime. Use meaningful stage names with the `AS` keyword, for example `FROM node:18 AS builder`. Place stages in logical order: dependencies → build → test → runtime.

**Step 3 — Select Base Images.** Start with official minimal base images when possible. Specify exact version tags, for example `python:3.11-slim` rather than just `python`. Consider distroless runtime images where appropriate. Use Alpine-based images for smaller footprints only when compatible. Ensure the runtime image has the minimal necessary dependencies.

**Step 4 — Optimize layers and build context.** Organize commands to maximize layer caching. Place commands that change frequently, such as code copies, after commands that change less frequently, such as dependency installation. Use `.dockerignore` to prevent unnecessary files from entering the build context. Combine related `RUN` commands with `&&` to reduce layer count. Consider `COPY --chown` to set permissions in one step.

**Step 5 — Apply security practices.** Avoid running containers as root by using `USER`. Remove build tools and unnecessary packages from the final image. Scan the final image for vulnerabilities when tooling is available. Set restrictive file permissions. Use multi-stage builds to avoid including build secrets in the final image.

**Step 6 — Tune performance and operations.** Use build arguments for configuration that changes between environments. Leverage build cache by ordering layers from least to most frequently changing. Consider parallelization in build steps when the build tool supports it. Set appropriate runtime environment variables such as `NODE_ENV=production`. Add an application-appropriate `HEALTHCHECK` instruction.

**Step 7 — Validate and report.** Run the smallest available container build or validation command when permitted. Report the generated or changed files, practices applied, image-size or security caveats, and validation result.

## Invocation Example

```
/multi-stage-dockerfile target=./app runtime="node server.js"
```
