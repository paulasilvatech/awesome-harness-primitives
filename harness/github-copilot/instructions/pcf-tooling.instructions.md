---
applyTo: "**/*.{ts,tsx,js,json,xml,pcfproj,csproj}"
description: "Conventions for Microsoft Power Platform CLI tooling for Power Apps Component Framework creation, debugging, packaging, deployment, and ALM."
---

# Power Apps Component Framework Tooling Conventions — CLI and ALM

These instructions apply to Power Apps Component Framework source, manifest, project, and packaging files matched by `**/*.{ts,tsx,js,json,xml,pcfproj,csproj}`. They are authoritative for Microsoft Power Platform CLI tooling guidance for code components; component design, TypeScript style, Dataverse security, and organization ALM policies win when they define stricter project-specific requirements.

## Power Platform CLI Usage

Use Microsoft Power Platform CLI (command-line interface) to create, debug, and deploy code components using Power Apps Component Framework.

| Task | Convention |
| --- | --- |
| Tooling source | Direct users to install Microsoft Power Platform CLI from the official documentation. |
| Component creation | Use CLI-generated PCF structure rather than hand-assembling manifests and project files. |
| Debugging | Use CLI-supported local test harness and build commands before packaging for an environment. |
| Deployment | Deploy code components through Power Platform CLI only when the target Microsoft Dataverse environment and privileges are available. |
| ALM | Treat CLI output as part of the application life cycle management path, including solution packaging and environment promotion when applicable. |

Microsoft Power Platform CLI enables developers to create code components quickly and is expected to expand with additional development and ALM experiences.

## Environment and Privileges

To deploy a code component using Microsoft Power Platform CLI, require a Microsoft Dataverse environment with system administrator or system customizer privileges.

- Confirm the target environment before suggesting deploy or push commands.
- Do not imply deployment is possible from source files alone; Dataverse access and privileges are required.
- Keep environment-specific identifiers, connection profiles, and credentials out of source-controlled PCF files.
- Distinguish local build/debug guidance from Dataverse deployment guidance so contributors without privileges can still validate code locally.

## Component Project Hygiene

Keep PCF projects aligned with the CLI and official component framework expectations.

- Preserve CLI-managed project shape for `ControlManifest.Input.xml`, `.pcfproj`, `.csproj`, `package.json`, `tsconfig.json`, and generated solution files.
- Keep TypeScript control implementation, manifest metadata, resources, and packaging concerns separated.
- Validate manifest changes against supported property, dataset, resource, and feature declarations before packaging.
- Keep generated or tool-managed files stable unless the CLI or official documentation requires a change.
- Prefer repeatable CLI commands over manual edits when creating, rebuilding, testing, or packaging components.

## Good / Bad Examples

The examples below illustrate separating local PCF validation from Dataverse deployment.

**Good:**

```text
Use Microsoft Power Platform CLI to create the component, run the local test harness, then package or deploy only after confirming the target Dataverse environment and required system administrator or system customizer privileges.
```

Why: The guidance follows the official tooling path and does not skip the privilege requirement for deployment.

**Bad:**

```text
Copy the generated JavaScript into Dataverse manually; no environment permissions or CLI setup are needed.
```

Why: The guidance bypasses Microsoft Power Platform CLI and ignores the documented Dataverse environment and privilege requirement.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use Microsoft Power Platform CLI for PCF creation, debugging, packaging, and deployment guidance | The CLI is the supported developer path for Power Apps Component Framework code components |
| Require a Microsoft Dataverse environment with system administrator or system customizer privileges before deployment guidance | Deployment fails or becomes unsafe without the documented environment access |
| Preserve CLI-managed project and manifest structure | Manual divergence from generated files can break builds, harness behavior, or solution packaging |
| Prefer official Microsoft documentation for command installation and component workflow details | Power Platform CLI and PCF capabilities evolve with the platform |
| Treat CLI workflows as part of ALM | Components must move predictably through development, packaging, deployment, and environment promotion |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Install and use Microsoft Power Platform CLI for PCF work | Hand-create or manually deploy code components when the CLI supports the workflow |
| Confirm Dataverse environment access and privileges before deployment | Assume source access is enough to deploy a component |
| Keep `ControlManifest.Input.xml`, project files, and package files consistent with CLI expectations | Edit generated or tool-managed files without understanding packaging impact |
| Use official Microsoft documentation for CLI and PCF workflow questions | Rely on stale command snippets when the platform behavior matters |
| Separate local debug/build guidance from environment deployment guidance | Mix local harness validation with privileged Dataverse operations |

## Checklist Before Opening a PR

- [ ] PCF guidance uses Microsoft Power Platform CLI for creation, debugging, packaging, or deployment.
- [ ] Deployment guidance confirms a Microsoft Dataverse environment and system administrator or system customizer privileges.
- [ ] CLI-managed project, manifest, package, `.pcfproj`, and `.csproj` files remain consistent with supported PCF structure.
- [ ] Local debug and build guidance is separated from privileged environment deployment guidance.
- [ ] Official Microsoft documentation is cited for installation, first component creation, or PCF learning path details.

## References

- Install Microsoft Power Platform CLI: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/powerapps-cli
- Create your first code component: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/implementing-controls-using-typescript
- Learn Power Apps component framework: https://learn.microsoft.com/en-us/training/paths/use-power-apps-component-framework
