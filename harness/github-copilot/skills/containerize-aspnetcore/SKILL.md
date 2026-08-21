---
name: containerize-aspnetcore
description: >-
  Containerize an ASP.NET Core project for a Linux Docker container by creating a multi-stage Dockerfile, .dockerignore, optional health check, environment-variable configuration, and build verification. Use this skill when asked to dockerize, containerize, or create Docker assets for an ASP.NET Core or .NET web project.
---

# ASP.NET Core containerization

Convert an ASP.NET Core project and its containerization settings into Docker-ready Linux artifacts, verify the image builds, and report every configuration choice and remaining blocker.

## When to invoke

- "Containerize this ASP.NET Core project."
- "Create a Dockerfile and .dockerignore for this .NET web app."
- "Dockerize my ASP.NET Core API for Linux containers."
- "Make this .NET 8 or .NET 9 app run as a non-root Docker container."
- "Add a Docker health check and verify docker build succeeds."

## Containerization settings

Use the user's request and the repository to identify the project path and settings. Defaults apply when the user omits a setting: .NET `8.0`, Linux distribution `debian`, no custom build/run base image, primary HTTP port `8080`, `ASPNETCORE_URLS=http://+:8080`, user `$APP_UID`, and no extra packages, libraries, tools, copies, volumes, or health check unless specified.

| Setting | Accepted values or examples |
| --- | --- |
| Project to containerize | Path to `ProjectName.csproj` |
| .NET version | `8.0` or `9.0`; prefer detected `TargetFramework` from the `.csproj` |
| Linux distribution | `debian`, `alpine`, `ubuntu`, `chiseled`, Azure Linux / Mariner |
| Custom base images | `None` or explicit SDK/runtime image for build stage and run stage |
| Ports | Primary HTTP port such as `8080`; additional ports or `None` |
| User account | `$APP_UID` unless the user requires another account |
| Build steps | Custom steps before or after image build |
| NuGet package sources | `NuGet.config` and private feeds; do not commit authentication details |
| Dependencies | System packages, native libraries, additional .NET tools |
| Environment variables | Variables and values, or `Use defaults` |
| File system | Extra files/directories to copy, container target paths, excluded paths, volume mount points |
| Health check | URL path, interval, timeout, or `None` |
| Known issues | Specific requirements or blockers to address |

Keep the original settings vocabulary when translating user input: `[square brackets]`, `File/directory`, `Files/directories`, `[ProjectName (provide path to .csproj file)]`, `[8.0 or 9.0 (Default 8.0)]`, `[Specify base image to use for build stage (Default None)]`, `[Specify base image to use for run stage (Default None)]`, `[e.g., 8080]`, `[List any additional ports, or "None"]`, `[User account, or default to "$APP_UID"]`, `[Specify ASPNETCORE_URLS, or default to "http://+:8080"]`, `[List any specific build steps, or "None"]`, `[Package names for the chosen Linux distribution, or "None"]`, `[Library names and paths, or "None"]`, `[Tool names and versions, or "None"]`, `[Variable names and values, or "Use defaults"]`, `[Paths relative to project root, or "None"]`, `[Container paths, or "Not applicable"]`, `[Paths to exclude, or "None"]`, `[Volume paths for persistent data, or "None"]`, `[List any additional patterns, or "None"]`, `[Health check URL path, or "None"]`, `[Interval and timeout values, or "Use defaults"]`, `[Specific requirements, or "None"]`, and `[Describe any known issues, or "None"]`. Mandatory items MUST appear in the final files.

## Prerequisites and context

- Docker must be available to run `docker build -t aspnetcore-app:latest .`.
- The project must contain at least one ASP.NET Core `.csproj` with `TargetFramework` or an equivalent user-provided version.
- Use only changes required for Linux Docker container execution: app configuration, `Dockerfile`, `.dockerignore`, dependencies, health checks, and container-specific file copies.
- Do not perform infrastructure setup, deployment setup, or unrelated application rewrites.

## Procedure

1. Review the containerization settings and discover the target `.csproj`.
2. Create `progress.md` in the project directory and update every task from `[ ]` to `[x]` as it completes.
3. Determine the .NET version by checking `TargetFramework`; map `net8.0` to `8.0` and `net9.0` to `9.0` unless the user overrides it.
4. Select valid Microsoft base images unless custom images are specified. Preserve these documentation sources when choosing tags:
   - SDK image tags: https://github.com/dotnet/dotnet-docker/blob/main/README.sdk.md
   - ASP.NET Core runtime image tags: https://github.com/dotnet/dotnet-docker/blob/main/README.aspnet.md
   - .NET runtime image tags: https://github.com/dotnet/dotnet-docker/blob/main/README.runtime.md
5. Create the `Dockerfile` in the project root with a build stage and final stage.
6. Create `.dockerignore` in the project root with the mandatory patterns plus user-specified additional patterns.
7. Add health check support only when an endpoint is specified; install `curl` or `wget` only if the selected final image supports and needs it.
8. Verify requirements, run `docker build -t aspnetcore-app:latest .`, fix build failures, and continue until the image builds or a concrete environmental blocker remains.

## Dockerfile rules

| Concern | Rule |
| --- | --- |
| Stage naming | Use `AS build` for SDK publish and `AS final` for the runtime image; use `--from=build` to copy `/app/publish` |
| Build stage | Copy project files first for better caching, copy `NuGet.config` if present, run `dotnet restore`, copy the rest of the source, then `dotnet build` and `dotnet publish` to `/app/publish` |
| Final stage | Set `WORKDIR /app`, copy publish output, set environment variables, expose ports, configure optional volumes and health checks, switch to non-root user, set `ENTRYPOINT` |
| Build configuration | Use `ARG BUILD_CONFIGURATION=Release`; pass `$BUILD_CONFIGURATION` to `dotnet build` and `dotnet publish` |
| Runtime user | Use `USER $APP_UID` by default. Do not create a new user unless the settings require it |
| URL binding | Set `ASPNETCORE_URLS=http://+:8080` unless the settings provide a different value |
| Entry point | Use `ENTRYPOINT ["dotnet", "<ProjectName>.dll"]` with the actual assembly name |
| Secrets | Do not bake connection strings, passwords, private feed credentials, or certificate passwords into the image |

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0-bookworm-slim AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["YourProject/YourProject.csproj", "YourProject/"]
COPY ["YourOtherProject/YourOtherProject.csproj", "YourOtherProject/"]
COPY ["NuGet.config", "."]
RUN dotnet restore "YourProject/YourProject.csproj"
COPY . .
WORKDIR "/src/YourProject"
RUN dotnet build "YourProject.csproj" -c $BUILD_CONFIGURATION -o /app/build
RUN dotnet publish "YourProject.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:8.0-bookworm-slim AS final
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_ENVIRONMENT=Production
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
USER $APP_UID
ENTRYPOINT ["dotnet", "YourProject.dll"]
```

Use actual values in place of `YourProject.csproj`, `YourProject.dll`, `YourOtherProject`, `YourOtherProject/YourOtherProject.csproj`, `your-connection-string`, and `your_password`. For named stages, `AS stage-name` enables `--from=stage-name`; the production stage should still be named `final`. If the application also needs HTTPS or SSL/TLS, expose the HTTPS port and configure certificates through environment variables or mounted secrets.

## Base image selection

| Distribution | SDK example | ASP.NET runtime example | Package manager note |
| --- | --- | --- | --- |
| Debian 12 | `mcr.microsoft.com/dotnet/sdk:8.0-bookworm-slim` or `9.0-bookworm-slim` | `mcr.microsoft.com/dotnet/aspnet:8.0-bookworm-slim` or `9.0-bookworm-slim` | `apt-get update && apt-get install -y curl wget ca-certificates libgdiplus && rm -rf /var/lib/apt/lists/*` |
| Ubuntu 24.04 | `mcr.microsoft.com/dotnet/sdk:8.0-noble` or `9.0-noble` | `mcr.microsoft.com/dotnet/aspnet:8.0-noble` or `9.0-noble` | Use `apt-get` |
| Alpine Linux | `mcr.microsoft.com/dotnet/sdk:8.0-alpine` or `9.0-alpine` | `mcr.microsoft.com/dotnet/aspnet:8.0-alpine` or `9.0-alpine` | `apk update && apk add --no-cache curl ca-certificates` |
| Ubuntu chiseled | Build with a normal SDK image | `mcr.microsoft.com/dotnet/aspnet:8.0-noble-chiseled`, `8.0-jammy-chiseled`, or `9.0-noble-chiseled` | Minimal packages; use a different base if extra dependencies or shell health checks are required |
| Azure Linux / Mariner | Standard SDK image or approved custom image | `mcr.microsoft.com/dotnet/aspnet:8.0-azurelinux3.0` or `9.0-azurelinux3.0` | `tdnf update -y && tdnf install -y curl ca-certificates && tdnf clean all` |

All official examples come from the `mcr.microsoft.com/dotnet` repository family. Distinguish `build/publish`, `pre-build`, and `post-build` steps in the report, and state build success/failure.

## .dockerignore minimum

The `.dockerignore` file must include these patterns plus any additional patterns from settings:

```gitignore
bin/
obj/
.dockerignore
Dockerfile
.git/
.github/
.vs/
.vscode/
**/node_modules/
*.user
*.suo
**/.DS_Store
**/Thumbs.db
```

## Progress tracking

Create and maintain this `progress.md` structure:

```markdown
# Containerization Progress

## Environment Detection
- [ ] .NET version detection (version: ___)
- [ ] Linux distribution selection (distribution: ___)

## Configuration Changes
- [ ] Application configuration verification for environment variable support
- [ ] NuGet package source configuration (if applicable)

## Containerization
- [ ] Dockerfile creation
- [ ] .dockerignore file creation
- [ ] Build stage created with SDK image
- [ ] csproj file(s) copied for package restore
- [ ] NuGet.config copied if applicable
- [ ] Runtime stage created with runtime image
- [ ] Non-root user configuration
- [ ] Dependency handling (system packages, native libraries, tools, etc.)
- [ ] Health check configuration (if applicable)
- [ ] Special requirements implementation

## Verification
- [ ] Review containerization settings and make sure that all requirements are met
- [ ] Docker build success
```

## Configuration patterns

| Requirement | Dockerfile pattern |
| --- | --- |
| Additional .NET tools | `RUN dotnet tool install --global dotnet-ef --version 8.0.0` and `ENV PATH="$PATH:/root/.dotnet/tools"` only when needed |
| Extra app files | `COPY ./config/appsettings.Production.json .` or `COPY ./certificates/ ./certificates/` with actual paths |
| Environment variables | `ENV CONNECTIONSTRINGS__DEFAULTCONNECTION="..."` only as a placeholder or non-secret local value; use `ENV FEATURE_FLAG_ENABLED=true` for safe flags |
| Kestrel certificates | `ASPNETCORE_Kestrel__Certificates__Default__Path=/app/certificates/app.pfx`; never commit `ASPNETCORE_Kestrel__Certificates__Default__Password` with a real secret |
| Volumes | `VOLUME ["/app/data", "/app/logs"]` only when persistent data is required |

## Gotchas

- **Do not use `latest`**: specific image tags make builds reproducible.
- **Do not install build dependencies in the final image**: multi-stage builds should keep SDK and tooling out of runtime.
- **Do not add `curl` to chiseled images blindly**: chiseled images are minimal and may not support package installation; choose a compatible base or different health check strategy.
- **Do not pause for confirmation** when the user asked to containerize; proceed methodically until all progress checkboxes are marked or a real blocker is documented.
- **Completion is binary**: preserve the original rule that you are not `DONE` `UNTIL` all `CHECKBOXES` are `MARKED`, unless a documented blocker prevents completion.

## Output template

```markdown
## ASP.NET Core containerization result — <project>

**Status:** complete | build failed | blocked
**Project file:** `<path/to/project.csproj>`
**Detected .NET version:** `<8.0|9.0|other>`
**Linux distribution:** `<debian|alpine|ubuntu|chiseled|azurelinux|custom>`
**Base images:** `<sdk image>` → `<runtime image>`

### Files changed
- `Dockerfile`: <summary>
- `.dockerignore`: <summary>
- `progress.md`: <all tasks marked or blocker>
- `<app config file>`: <environment variable support, if changed>

### Settings applied
| Setting | Value |
| --- | --- |
| Ports | `<ports>` |
| User | `<user>` |
| ASPNETCORE_URLS | `<value>` |
| Health check | `<endpoint or none>` |
| Extra packages/libraries/tools | `<list or none>` |
| Volumes/copies | `<list or none>` |

### Validation
- `docker build -t aspnetcore-app:latest .`: pass | fail
- Remaining blocker: <none or exact error>
```

## Quality gate

- [ ] The Dockerfile uses multi-stage build and publish, then copies `/app/publish` into `AS final`.
- [ ] The selected SDK and runtime images match the detected .NET version and requested Linux distribution or custom image settings.
- [ ] `ASPNETCORE_ENVIRONMENT`, `ASPNETCORE_URLS`, `APP_UID`, `BUILD_CONFIGURATION`, and any safe custom variables such as `FEATURE_FLAG_ENABLED` are handled deliberately.
- [ ] `.dockerignore` includes all mandatory patterns and requested additional patterns.
- [ ] Health check, system packages, native libraries, .NET tools, volumes, and extra file copies are implemented only when required.
- [ ] No secrets or private feed credentials are baked into the image.
- [ ] `progress.md` exists and all checkboxes are marked `[x]` or a blocker is documented.
- [ ] `docker build -t aspnetcore-app:latest .` was run and passed, or the exact environmental blocker is reported.

## References

- [Microsoft .NET SDK image tags](https://github.com/dotnet/dotnet-docker/blob/main/README.sdk.md)
- [Microsoft ASP.NET Core runtime image tags](https://github.com/dotnet/dotnet-docker/blob/main/README.aspnet.md)
- [Microsoft .NET runtime image tags](https://github.com/dotnet/dotnet-docker/blob/main/README.runtime.md)
