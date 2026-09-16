---
description: "Preserve .NET compatibility, container platform boundaries, identity, state, and validation during Azure modernization. Use when editing .NET projects or container configuration for Windows App Service, Linux App Service, or Azure Container Apps."
applyTo: "**/*.csproj,**/*.vbproj,**/*.fsproj,**/Directory.Build.*,**/Directory.Packages.props,**/global.json,**/packages.config,**/web.config,**/Dockerfile*,**/*.dockerfile,**/.dockerignore"
---

# .NET Azure Modernization Conventions - Explicit Platform Boundaries

These instructions govern compatibility and container-hosting invariants in matched files when a
.NET Azure migration is in scope. They do not mandate a migration for every matching file. Explicit
project targets, approved requirements, repository security policy, and verified first-party product
constraints win over examples. Ordered assessment and migration belong to
`dotnet-modernization-assessment`, `dotnet-windows-appservice`, and `dotnet-linux-modernization`
(skills), not to these passive rules.

## Runtime and App Model

- Distinguish .NET Framework from modern .NET, and a deployable application from a .NET Standard library.
- Preserve .NET Framework compatibility in projects that remain legacy. An approved target change,
  not a filename match, determines when modern .NET conventions become applicable.
- Do not replace a project's effective framework until imported properties, conditions, consumers,
  packages, build tools, and test coverage are understood.
- Keep shared libraries compatible with their remaining consumers. .NET Standard 2.1 is not a
  compatibility bridge for .NET Framework; use a verified compatible target or multi-targeting.
- Select a stable supported runtime from Microsoft's support policy and record its date, SDK, TFM,
  container runtime, and patch-maintenance strategy. A preview is not an implicit production choice.
- Do not mechanically rewrite serializers, EF6, authentication, WCF contracts, or hosting patterns
  merely because the framework changed. Require behavior tests and an explicit need.

## Container and Hosting

- .NET Framework, System.Web, and unported Windows dependencies remain Windows workloads.
- Validate the actual image's OS, architecture, and Windows OS version; tags are not sufficient.
- Rehosting on Windows App Service does not require Linux or a modern .NET rewrite.
- Apply Windows build-host and base-image compatibility separately from Azure hosting eligibility.
- For Linux, prove native-library compatibility, filesystem case sensitivity, permissions,
  globalization, time zones, certificates, and removal or isolation of Windows-only APIs.
- Align the application's observed listening address and port with the platform's target port.
  `EXPOSE` alone does not configure a listener.
- Distinguish App Service classic custom-container configuration from sidecar-enabled
  `sitecontainers`; do not apply classic `WEBSITES_PORT` guidance to sidecar-enabled apps.
- Keep an HTTP app, a continuous worker, and a finite job distinct when choosing ACA ingress,
  scaling, retry behavior, and lifecycle.

## Identity, State, and Release Safety

- Keep registry and runtime secrets out of source, build arguments, image layers, and diagnostics.
  Prefer managed identity and least-privilege registry access appropriate to its RBAC/ABAC mode.
- Externalize persistent data, uploads, session state, and cryptographic key rings where needed.
  Test restart, scale-out, and cross-revision behavior; do not rely on container-local storage.
- Separate schema migrations from replica startup; require a reviewed, recoverable data strategy.
- Preserve the previous image and configuration until the agreed rollback window closes.
- Require explicit authorization for image publication, resource changes, access-policy changes,
  production traffic switches, and resource deletion.

## Conventions

| Rule | Rationale |
| --- | --- |
| Treat rehosting, runtime upgrade, and Linux portability as separate checkpoints. | Each has different blockers and rollback evidence. |
| Use immutable release identifiers and record resolved image digests. | Mutable tags cannot reliably identify what was tested. |
| Preserve baseline failures and unrun checks. | A successful static check is not runtime readiness. |
| Reverify volatile platform facts before execution. | Image support, releases, and service capabilities change. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Build Windows images on a compatible Windows runner. | Claim a macOS/Linux run validates a Windows container. |
| Test authentication, sessions, serialization, and data behavior. | Treat a successful compilation as business equivalence. |
| Select Linux-compatible application and image targets for ACA. | Deploy a Windows image or assume ARM compatibility. |
| Keep deployment preparation separate from authorization. | Run cloud mutations because credentials are available. |

## Checklist Before Opening a PR

- [ ] App model, effective targets, dependencies, and selected migration path are recorded.
- [ ] Runtime support and image/platform compatibility have dated evidence.
- [ ] Listening ports, health checks, identity, state, and rollout configuration agree.
- [ ] Existing tests cover preserved contracts and approved changes.
- [ ] Image/runtime tests and cloud checks are reported separately from static validation.
- [ ] Secrets, unrelated changes, and destructive defaults are absent.
- [ ] Rollback includes data compatibility, not only an image switch.

## References

Platform references verified on 2026-09-15; recheck before selecting a deployment target:

- [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core)
- [App Service custom containers](https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container)
- [App Service sidecar configuration](https://learn.microsoft.com/en-us/azure/app-service/configure-sidecar)
- [ACA container requirements](https://learn.microsoft.com/en-us/azure/container-apps/containers)
