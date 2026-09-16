# Windows App Service hosting reference

Documentation verified **2026-09-15**. Recheck the linked first-party pages before selecting a base,
plan, region, authentication mechanism, or production rollout.

## Base image and build environment

The [App Service custom-container reference](https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container)
lists these useful cached examples:

| App runtime | Documented example |
| --- | --- |
| ASP.NET on .NET Framework 4.8 | `mcr.microsoft.com/dotnet/framework/aspnet:4.8-windowsservercore-ltsc2019` |
| ASP.NET on .NET Framework 4.8.1 | `mcr.microsoft.com/dotnet/framework/aspnet:4.8.1-windowsservercore-ltsc2022` |

These are mutable source tags, not immutable production pins. Resolve and record the digest used,
apply current security patches, and test the runtime against the application's target and dependencies.
Do not upgrade an application's TFM to 4.8.1 merely because that image exists.

The same reference explicitly states that **Windows Server 2025 base images are not supported by
App Service**. General Windows-container compatibility does not override a service-specific limit.
The helper's known builds are LTSC 2019 (`17763`) and LTSC 2022 (`20348`); it rejects other builds for
manual policy review rather than treating their absence as a universal unsupported-product claim.

Use the [Windows host/image compatibility matrix](https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility)
for the build/test host and isolation mode. The
[Windows custom-container quickstart](https://learn.microsoft.com/en-us/azure/app-service/quickstart-custom-container)
uses a Windows container engine and an ASP.NET Framework image. A Linux engine on macOS cannot perform
this runtime test.

## Container recipe requirements

- Build/publish the legacy application with its actual MSBuild/NuGet toolchain. Pin the build tools
  and record targeting-pack requirements rather than assuming SDK-style project support.
- Inspect the existing Dockerfile and IIS configuration. Use the smallest compatible Windows base
  that contains the app model and required features; Nano Server is not a replacement for a
  System.Web/IIS .NET Framework application.
- Copy reviewed publish artifacts into the runtime image, not the entire repository. Inspect
  transformed `web.config`, publish profiles, certificates and native assets for embedded secrets.
- Preserve the official image's IIS lifecycle/service monitor unless a tested design replaces it.
  A successful process exit or a sleeping container is not a working website.
- Review startup download cost, health/startup timeouts, memory, cold start and recovery behavior.
  Test the actual app instead of copying limits from a different plan.

## Hosting, identity and state

Record an actual Windows-container-capable plan/SKU/region and capacity result when cloud validation
is authorized. Do not infer availability or price from the application language or a sample SKU.

For classic custom containers, App Service defaults to port 80; configure `WEBSITES_PORT` if the
application uses another port. The selected target port must match the observed listener and the
health endpoint. Authentication must not turn the platform health check into a false success.

The custom-container reference recommends managed identity for ACR pulls and states that service
principal authentication for **Windows image pulls** is no longer supported. This does not mean all
service-principal control-plane authentication is unsupported.

Use the registry's actual permission mode. The
[ACR role reference](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-rbac-built-in-roles-overview)
distinguishes `AcrPull` for conventional RBAC from `Container Registry Repository Reader` for
ABAC-enabled repository access. Do not grant broad roles or change registry authentication/network
policy merely to make a failing pull work. Check ARM-audience-token requirements against policy.

Keep network-protected ACR pull connectivity separate from application outbound connectivity; verify
VNet integration, private DNS and image-pull routing as applicable. Keep persistent files, session
state, machine/data-protection keys and uploaded documents outside disposable runtime layers where
the app requires durability or multiple replicas. Validate restart and scale-out explicitly.

## Acceptance and rollback

- Legacy baseline and image build/startup passed on the compatible Windows runner.
- Expected routes, static assets, authentication/authorization, session, native libraries and data
  access passed with synthetic inputs.
- Image pull, health checks, restart, scaling, diagnostics and performance passed in the actual lower
  environment before claiming Azure readiness.
- Rollout uses only supported and verified slots or blue/green behavior for the chosen plan.
- Previous image digest and configuration are retained; data remains backward-compatible or has a
  separate tested recovery plan.
- No source environment, identity, registry policy, database or production traffic is changed without
  explicit authorization.
