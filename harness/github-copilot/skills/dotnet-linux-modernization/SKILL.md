---
name: dotnet-linux-modernization
description: >-
  Modernize legacy .NET applications to a verified supported .NET release and Linux containers for
  Azure App Service or Azure Container Apps. Use when removing Windows dependencies, migrating
  System.Web to ASP.NET Core, planning incremental modernization, or moving .NET containers to Linux or ACA.
---

# .NET modernization for Linux and Azure

Upgrade a bounded application while preserving tested behavior, then prove Linux compatibility before
selecting a release destination. Use [the Linux hosting reference](references/linux-hosting.md) for
runtime, app-model, container, and service-specific decisions.

## When to invoke

- "Modernize this .NET Framework application to the current supported .NET LTS."
- "Move this Windows .NET container to Linux."
- "Migrate this ASP.NET application to Azure Container Apps."
- "Choose Linux App Service versus ACA for our modernized application."

## Three independent gates

| Gate | Required evidence |
| --- | --- |
| Runtime/app-model modernization | Supported target selection, effective dependency graph, compatible packages, framework and behavioral tests. |
| Linux portability | No unresolved reachable Windows-only dependencies; Linux publish, startup, authentication, native-library, filesystem, and behavior tests. |
| Hosting readiness | Correct image architecture, listener/probes, identity, network, state, scale, capacity, and tested rollout/rollback. |

Modern .NET on Windows can be a useful checkpoint. It does not satisfy the Linux gate. A .NET Standard
library is not the deployable entry project, and a Windows-specific TFM is not a Linux target.

## Prerequisites and context

- A reviewed `dotnet-modernization-assessment` (skill) result, an approved target path, and a legacy
  test baseline. Reuse `legacy-characterization-testing` (skill) when installed.
- Installed SDK/build tools and existing tests appropriate to each checkpoint.
- A Linux runner/engine and the target CPU architecture for runtime checks; retain a Windows runner
  while legacy parts still require it.
- Azure access only when resource verification or deployment has been authorized.

## Procedure

1. Bound the first vertical slice and pin its observable contract. Record permitted behavior changes,
   test inputs, downtime, data compatibility, and the rollback checkpoint.
2. Reverify Microsoft's support policy. Record the selected GA/LTS release, TFM, SDK, package support,
   OS support, and runtime-image maintenance strategy. Do not choose a preview merely because it has
   the highest version number, or freeze today's patch as a permanent recommendation.
3. Use the installed Microsoft .NET upgrade workflow when available; discover its capabilities first.
   Otherwise use `dotnet-upgrade` (skill) for explicit project/package changes and validation. The
   Microsoft tool and this repository's skill are different things; neither may be assumed installed.
4. Sequence libraries and their consumers without breaking remaining .NET Framework callers. Preserve
   compatible .NET Standard 2.0 contracts or multi-target when needed. Plan `packages.config` conversion
   only for supported project types, preserving binding redirects, build assets, and restore behavior.
5. Migrate app-model dependencies deliberately. For complex System.Web applications, consider
   side-by-side incremental routing to ASP.NET Core. Prove shared authentication/session boundaries
   and secure the legacy fallback. Treat Web Forms, WCF servers, COM+, remoting, and Workflow as explicit
   workstreams, not namespace replacements.
6. Remove or isolate Windows-only APIs and native components. Run Linux tests for path casing,
   separators, file permissions, globalization/time zones, certificates, drawing/font dependencies,
   authentication, and SQL/native client behavior. Do not introduce a database or ORM migration unless
   needed and authorized.
7. Produce a Linux image with a verified runtime/base and explicit architecture. Use a non-root user
   where supported, minimal runtime artifacts, reproducible dependencies, and immutable release
   identity. Choose SDK container publishing or a Dockerfile according to the actual application,
   native libraries, and existing build convention; do not enable trimming/AOT blindly.
8. Choose the host from [the hosting criteria](references/linux-hosting.md). Align observed listeners,
   target ports and probes. For ACA, separate app/worker/job lifecycles and deliberate minimum replicas;
   for App Service, distinguish classic versus sidecar container configuration.
9. Prepare IaC, identity, private networking/DNS, external state, telemetry, and rollout settings.
   Run the HTTP image/port validator from `dotnet-modernization-assessment` (skill) where applicable,
   then test real startup, graceful shutdown, restart, scale-out, and dependency failures.
10. Stop at **implemented** or **prepared** until authorized deployment. Validate in a lower environment,
    compare against the baseline, and perform only the approved rollout. Record configuration, traffic,
    image and data rollback evidence; unresolved checks prevent a readiness claim.

## Limits

- Do not assume .NET Framework, WPF, WinForms, Web Forms, or Windows native binaries run on Linux.
- Do not treat a Compatibility Pack, SDK-style conversion, or TFM bump as Linux certification.
- No automatic image publication, Azure mutation, schema migration, or production traffic changes.
- Azure Functions-specific execution models and desktop UI modernization require separate workflows.
- When Linux is blocked, use `dotnet-windows-appservice` (skill) only after an explicit rehosting decision.

## Output template

```markdown
## .NET Linux modernization
**Status:** assessed | implemented | prepared | deployed-and-verified | blocked
**Scope/revision:**
**Runtime/SDK/TFM and dated support source:**
**Host:** Linux App Service | ACA app | ACA worker | ACA job

### Checkpoints
| Gate | Changes | Tests and evidence | Blockers | Rollback |
| --- | --- | --- | --- | --- |

### Hosting contract
- Image OS/architecture/digest:
- Listener, probes, scaling, identity, networking, state, and diagnostics:
- App Service container mode or ACA revision/job strategy:

### Remaining work
- Unverified behavior:
- Authorized deployment actions and results:
- Data/traffic rollback and retained legacy dependencies:
```

## Quality gate

- [ ] Stable target support is freshly verified and distinct from preview availability.
- [ ] Each upgrade checkpoint preserves tested contracts and remaining consumers.
- [ ] Windows-only dependencies are removed, isolated, or reported as blockers.
- [ ] Linux image architecture, runtime, listeners, permissions, and native dependencies were verified.
- [ ] Host-specific identity, state, health, scaling, and rollout settings are explicit.
- [ ] Static, local-runtime, and cloud validation results are reported separately.
- [ ] No deployment authority or rollback capability was assumed.
