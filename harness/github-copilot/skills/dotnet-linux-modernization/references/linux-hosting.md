# Modern .NET and Linux hosting reference

First-party documentation checked **2026-09-15**. Refresh release, OS, image and service evidence
before executing a migration.

## Stable runtime target

The [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core),
updated 2026-09-08, lists **.NET 10 LTS** as active through 2028-11-14. .NET 8 and 9 are in
maintenance through 2026-11-10. .NET 11 RC1 is listed separately as a go-live pre-release, not GA.

For a new stable-LTS modernization target, the verified snapshot therefore points to `net10.0`.
Record the actual SDK and runtime patch selected at execution; do not infer SDK versions from runtime
patch numbers or treat a saved example tag as permanently current.

The [Upgrade Assistant overview](https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-overview)
marks that tool deprecated. The
[GitHub Copilot upgrade overview](https://learn.microsoft.com/en-us/dotnet/core/porting/github-copilot-upgrade/overview)
documents upgrade scenarios and supported environments. Discover the installed workflow, licensing,
permissions and project support; use reviewed manual changes if it is unavailable. Do not install an
old global tool as an automatic prerequisite.

## App-model migration

Follow the [ASP.NET Framework to ASP.NET Core guide](https://learn.microsoft.com/en-us/aspnet/core/migration/fx-to-core/?view=aspnetcore-10.0).
Incremental side-by-side migration can keep legacy routes working while moving one vertical slice.
It requires explicit trust, routing, auth, session, observability and rollout design.

- `System.Web` and Web Forms are not made cross-platform by changing a TFM.
- For a WCF server, verify CoreWCF's required bindings/features or plan a contract change. WCF client
  package availability does not establish server compatibility.
- Remoting, COM+, Workflow and AppDomain-creation dependencies require alternatives or isolation;
  consult [unavailable Framework technologies](https://learn.microsoft.com/en-us/dotnet/core/porting/net-framework-tech-unavailable).
- Native/COM/registry/drawing signals require reachability analysis and actual Linux tests.
  A Windows Compatibility Pack or a successful compilation is not portability evidence.
- Keep .NET Framework consumers on compatible shared contracts, often .NET Standard 2.0 or
  multi-targeting. Do not automatically move shared libraries to .NET Standard 2.1.
- Preserve EF6, serializers and SQL contracts unless a separate, evidenced change is necessary.
  Include Unicode, decimal/date behavior, null handling and transaction boundaries in tests.

## Container recipe choices

Use [Microsoft's container-image guidance](https://learn.microsoft.com/en-us/dotnet/core/docker/container-images)
to select `aspnet`, `runtime`, or `runtime-deps` according to deployment mode.
Choose the actual distro/architecture/tag and record its digest. Chiseled/distroless, Alpine/musl,
globalization-invariant mode, trimming, and AOT have compatibility implications; none is a blind default.

Use a non-root identity where supported and copy only published runtime artifacts. Test filesystem
permissions, native libraries, ICU/time-zone needs, trust stores, graceful termination and
case-sensitive paths. Linux `amd64` is the suite's conservative Azure image profile; local ARM image
success is not evidence that it fits ACA.

The [.NET 8 container port change](https://learn.microsoft.com/en-us/dotnet/core/compatibility/containers/8.0/aspnet-port)
sets the ASP.NET Core image default to 8080. Older `WebHost.CreateDefaultBuilder` applications may
ignore `ASPNETCORE_HTTP_PORTS`; configure a suitable `ASPNETCORE_URLS` binding when required and
verify it. Binding only to loopback or adding `EXPOSE` is insufficient.

## Host selection and configuration

| Concern | Linux App Service | Azure Container Apps |
| --- | --- | --- |
| Fit | A web application aligned with App Service operations and a selected plan. | HTTP services, workers or finite jobs with an explicitly selected execution/scaling model. |
| Image | Verified Linux image for the service/plan; this suite uses `amd64`. | [Container requirements](https://learn.microsoft.com/en-us/azure/container-apps/containers) specify `linux/amd64`; not Windows. |
| Port | Classic mode uses `WEBSITES_PORT`; sidecar-enabled mode uses the main `sitecontainers` configuration. | Ingress `targetPort` must equal the actual HTTP listener; no ingress for a worker unless needed. |
| Health | Configure a real health endpoint and startup behavior for the selected plan. | Distinct startup, readiness and liveness probes; do not destabilize liveness on every transient dependency outage. |
| Scaling | Test the chosen plan's scale behavior and externalized state. | Choose minimum/maximum replicas, triggers and cold-start tolerance deliberately; scale-to-zero is not always appropriate. |
| Release | Verified slots or blue/green for the selected configuration. | Verified revision/traffic strategy for apps; job executions have a different lifecycle. |

The [App Service sidecar reference](https://learn.microsoft.com/en-us/azure/app-service/configure-sidecar)
states that classic `DOCKER_*` and `WEBSITES_PORT` settings do not apply to sidecar-enabled apps.
The main container alone receives external traffic. Do not change the container mode as an incidental
framework-upgrade side effect.

The [ACA probe reference](https://learn.microsoft.com/en-us/azure/container-apps/health-probes)
documents HTTP(S)/TCP probes and excludes `exec` probes. Use numeric ports and tested thresholds.
Do not assume a shell, curl, or a Kubernetes probe feature exists in the image/platform.

Use [managed identity for ACA image pulls](https://learn.microsoft.com/en-us/azure/container-apps/managed-identity-image-pull)
and the appropriate [ACR RBAC/ABAC role](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-rbac-built-in-roles-overview).
Separate image-pull identity, application data access, public ingress, outbound networking, and private
registry DNS/connectivity; successful authentication does not prove network reachability.

## Release evidence

Record Linux build/startup and behavior tests, actual listener/probe results, dependency failure
behavior, restart/scale tests, image digest, vulnerability findings from existing tooling, lower
environment observations, and allowed rollout actions.

Use external durable state and a compatible shared key/session strategy when needed. Run schema
changes through a reviewed one-time workflow rather than every replica's startup. Test backward
compatibility or recovery before traffic switches. A revision rollback cannot reverse data loss.
