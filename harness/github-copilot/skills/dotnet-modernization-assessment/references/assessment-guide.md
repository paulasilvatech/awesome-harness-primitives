# .NET assessment criteria

First-party documentation checked on **2026-09-15**. These are decision criteria, not a claim that an
application or Azure subscription has been tested.

## Choose a path, not just a version

| Evidence | Windows App Service rehost | Modern .NET and Linux |
| --- | --- | --- |
| ASP.NET Framework MVC/Web API and System.Web | Preserve IIS/app model if the platform assessment passes. | Migrate request pipeline, configuration, authentication and session behavior to ASP.NET Core. |
| Web Forms pages and controls | A candidate for preserving the Windows application. | Explicit UI/application migration; no TFM-only conversion. |
| WCF server | Verify protocol, bindings, network and hosting requirements. | Assess CoreWCF or a contract migration per binding/feature; do not equate WCF client packages with server support. |
| COM+, remoting, Workflow, native DLLs | Verify container operation, licensing and external dependencies. | Replace or isolate; a modern .NET target does not provide these features automatically. |
| Windows authentication, impersonation, domain assumptions | Verify actual identity flows and hosting restrictions. | Redesign or explicitly validate the supported identity flow; do not assume Kerberos/NTLM parity. |
| Local files, registry, in-memory session, machine keys | Test durable state and multi-instance behavior. | Externalize required state and test permissions, case sensitivity and cross-replica keys/sessions. |
| WPF/WinForms or interactive desktop dependencies | Not a web-hosting fit without decomposition. | Desktop frameworks remain Windows-specific; separate the service boundary first. |
| Modern .NET without obvious Windows dependencies | Rehosting may not need a framework change. | Candidate only; native dependencies, runtime behavior and image architecture still need tests. |

## Evidence checklist

1. Record the selected application, source revision, deployed entry point, current framework/runtime,
   IIS/app model, OS/image, architecture, workload type, and current hosting.
2. Enumerate solution, project, shared properties/targets, package and native dependencies. Inspect
   effective build properties and conditional graph on a trusted build runner; static XML is not MSBuild.
3. Identify `packages.config`, central package management, private feeds, binding redirects, build
   tasks, Web Site projects, C++/CLI, and vendor binaries that require manual analysis.
4. Capture behavior tests for routes, error codes, auth/authorization, cookies/session, serialization,
   dates/numbers, data updates, scheduled work, file output, and external-service interactions.
5. Record RTO/RPO, peak/idle load, cold-start tolerance, minimum instances, regional/data-residency
   constraints, network topology, and dependency failure modes.
6. For each signal, record confirmed usage or false-positive evidence, affected migration paths,
   remediation, owner, validation experiment, and rollback implications.

Use public documentation queries that contain only product/topic names. Do not submit repository
content, private package names, connection strings, credentials, or production payloads.

## Runtime selection evidence

The [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core),
updated 2026-09-08 and fetched 2026-09-15, lists .NET 10 as active LTS with support through 2028-11-14.
.NET 8 and 9 are in maintenance through 2026-11-10; .NET 11 RC1 appears separately as a go-live
pre-release, not GA. Use the policy again when executing; do not treat this snapshot as a release resolver.

The [porting overview](https://learn.microsoft.com/en-us/dotnet/core/porting/) still describes an
18-month STS period, while the support policy describes two years. For lifecycle decisions, the
support policy's per-release dates take precedence over that older overview text.

The [Upgrade Assistant overview](https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-overview)
marks .NET Upgrade Assistant deprecated. Prefer the documented
[GitHub Copilot upgrade workflow](https://learn.microsoft.com/en-us/dotnet/core/porting/github-copilot-upgrade/overview)
when installed and appropriate, or reviewed manual changes. Tool support is not proof that every
application or migration is automatic.

## Platform evidence

- [App Service custom containers](https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container):
  documents LTSC-based Windows parents, including ASP.NET Framework 4.8/LTSC 2019 and 4.8.1/LTSC 2022;
  explicitly excludes Windows Server 2025 base images.
- [Windows container compatibility](https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility):
  host/image build and isolation mode matter separately from Azure service support.
- [ACA containers](https://learn.microsoft.com/en-us/azure/container-apps/containers):
  documents Linux x86-64 (`linux/amd64`) images. Windows images are not an ACA migration target.
- [ASP.NET migration](https://learn.microsoft.com/en-us/aspnet/core/migration/fx-to-core/?view=aspnetcore-10.0):
  app-model differences and incremental migration need explicit design and tests.
- [Unavailable .NET Framework technologies](https://learn.microsoft.com/en-us/dotnet/core/porting/net-framework-tech-unavailable):
  details remoting, COM+, Workflow and other migration constraints.
