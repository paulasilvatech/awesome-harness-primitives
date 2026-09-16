---
name: dotnet-windows-appservice
description: >-
  Prepare and validate legacy ASP.NET and .NET Framework workloads for Windows custom containers on
  Azure App Service without forcing a Linux rewrite. Use when rehosting IIS, Web Forms, MVC, or an
  existing Windows container to App Service and planning build, identity, state, rollout, and rollback.
---

# .NET Windows containers on App Service

Rehost a selected Windows web workload with minimal behavior change. Keep modernization optional and
separately approved. Use [the Windows hosting reference](references/windows-appservice.md) for
first-party evidence and concrete platform checks.

## When to invoke

- "Move this legacy .NET app to a Windows container on App Service."
- "Rehost our IIS/Web Forms application without rewriting it."
- "Prepare an existing Windows container for Azure App Service."

## Windows is a deliberate destination

- Preserve the existing application model for rehosting. Modern .NET is not a prerequisite.
- A .NET Framework application remains a Windows workload. ACA is not a Windows-container destination.
- Match the .NET Framework runtime, Windows base, IIS dependencies, and compatible Windows build host.
- Service eligibility is separate from container startup: validate the Windows-container plan/SKU,
  region, networking, identity, and state requirements before declaring App Service a fit.
- Windows services, desktop UI, domain joining, COM licensing, native drivers, and machine-level
  dependencies need explicit assessment; a custom container is not an unrestricted VM replacement.

## Prerequisites and context

- A reviewed result from `dotnet-modernization-assessment` (skill), selected entry application, and
  legacy characterization baseline.
- A compatible Windows container engine/runner for real build and startup verification. On macOS or
  Linux, perform static preparation only and report Windows tests as not run.
- Existing build tools appropriate to the project: legacy MSBuild/NuGet where required, not a blind
  substitution of `dotnet build`.
- Azure subscription/resource IDs, capacity checks, and permission are needed only for authorized
  cloud validation or deployment, not for authoring a proposal.

## Procedure

1. Reconfirm that the selected path is rehosting. Record out-of-scope framework, database, and UI changes.
2. Reproduce the existing build and tests. Identify IIS sites, bindings, app pools, required Windows
   features, publish artifacts, transforms, native dependencies, and authentication assumptions.
3. Select a documented supported base and record its resolved digest and runtime. Inspect an existing
   Dockerfile before modifying it; do not replace it wholesale. If creating one, use the official
   ASP.NET Framework image appropriate to the tested application and copy only sanitized published
   artifacts. Retain the image's IIS service-monitor startup unless a tested requirement changes it.
4. Build on the compatible Windows runner. Test startup, a representative route, static files,
   authentication, authorization, session continuity, serialization, and dependent-service access.
   Avoid copying source, credentials, signing keys, or private NuGet configuration into runtime layers.
5. Prepare reviewable App Service configuration using the existing IaC convention. Specify a
   Windows-container-capable plan, selected image, port, health endpoint, identity, network/DNS paths,
   storage, diagnostics, and rollout mechanism. Query live SKU/region availability only when authorized.
6. Configure registry pull through managed identity and an appropriate least-privilege role. Verify
   registry network reachability and authentication settings without enabling admin credentials or
   weakening policy. Separate registry pull permission from application data-access permission.
7. Run the image/port check owned by `dotnet-modernization-assessment` (skill). Validate real listening
   behavior, startup time, restart, scale-out, persistent state, certificate access, and logs separately.
8. Stop at **prepared** unless deployment is authorized. For an authorized deployment, use available
   Azure preparation/validation/deployment skills or a reviewed official workflow. Test a lower
   environment first, then use approved slots or blue/green where supported and verified.
9. Keep the previous image/configuration available. Verify the agreed rollback and data compatibility
   before switching production traffic; do not delete the old environment as automatic cleanup.

## Limits

- No automatic provisioning, image push, production cutover, database migration, or deletion.
- Do not claim zero downtime or slot support without testing the selected configuration.
- If Windows-specific dependencies prevent App Service hosting, return a blocker and an alternative
  platform decision instead of forcing ACA or Linux.
- Hand runtime/Linux migration to `dotnet-linux-modernization` (skill) as a separate scope.

## Output template

```markdown
## Windows App Service rehost
**Status:** prepared | deployed-and-verified | blocked
**Application/revision:**
**Preserved framework and app model:**
**Windows base/runtime/digest:**

### Configuration
- Windows build runner and host compatibility:
- Plan/SKU/region and evidence:
- IIS/listener, health checks, identity, network, state, and diagnostics:

### Validation
| Check | Evidence | Result or blocker |
| --- | --- | --- |

### Release
- Authorized actions performed:
- Rollout and rollback:
- Deferred modernization:
- Official sources and verification date:
```

## Quality gate

- [ ] Rehosting did not silently expand into a framework or app-model rewrite.
- [ ] The selected Windows base and App Service eligibility have fresh first-party evidence.
- [ ] Legacy build and Windows-container runtime tests ran or are explicitly blocked.
- [ ] Identity, network, ports, state, and scale-out behavior were tested at the claimed level.
- [ ] No credential, source secret, or private key entered a runtime image or report.
- [ ] Deployment and production changes were explicitly authorized; rollback remains available.
