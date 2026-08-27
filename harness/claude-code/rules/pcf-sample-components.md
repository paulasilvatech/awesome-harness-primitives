---
paths:
  - "**/*.{ts,tsx,js,json,xml,pcfproj,csproj}"
---

<!-- Generated from harness/github-copilot/instructions/pcf-sample-components.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces conventions for using, building, packaging, and trying PowerApps-Samples PCF sample components in model-driven and canvas apps.

# PCF Sample Component Conventions — PowerApps-Samples Usage

These instructions apply to PCF sample component code, manifests, project files, and solution files matched by the PCF globs. They are authoritative for using the Microsoft PowerApps-Samples component-framework samples as learning material, restoring/building sample controls, packaging sample solutions, and importing them into model-driven or canvas apps; product-specific PCF, React platform-library, dependent-library, and Power Pages instructions win where they describe a narrower host behavior.

## Source Repository and Prerequisites

Use the official `github.com/microsoft/PowerApps-Samples` repository as the source of sample components. Download or clone the repository before modifying a sample, and install Power Platform CLI for Windows when following the documented sample workflow. Open a Developer Command Prompt for Visual Studio when commands require MSBuild and Visual Studio tooling.

| Requirement | Convention |
| --- | --- |
| Source | Use `github.com/microsoft/PowerApps-Samples/tree/master/component-framework` |
| Local setup | Download or clone `github.com/microsoft/PowerApps-Samples` |
| CLI | Install Power Platform CLI for Windows |
| Shell | Use Developer Command Prompt for Visual Studio on Windows sample workflows |
| Working folder | Navigate to `component-framework`, then the individual sample folder such as `IncrementControl` |

## Sample Build and Solution Packaging

Treat the published sample flow as a convention, not as a reusable runbook. Restore dependencies in the component folder with `npm install`, restore MSBuild projects with `msbuild /t:restore`, create a solution folder such as `IncrementControlSolution`, initialize the solution, add a reference to the `.pcfproj`, and build a solution zip.

| Command or path | Purpose |
| --- | --- |
| `npm install` | Restore package dependencies for the selected component |
| `msbuild /t:restore` | Restore MSBuild project dependencies |
| `mkdir IncrementControlSolution` | Create a solution project folder beside the control |
| `cd IncrementControlSolution` | Work inside the solution folder |
| `pac solution init --publisher-name powerapps_samples --publisher-prefix sample` | Create `IncrementControlSolution.cdsproj` with sample publisher metadata |
| `pac solution add-reference --path ../../IncrementControl` | Reference the folder containing the `.pcfproj` |
| `pac solution add-reference --path ../../IncrementControl/IncrementControl.pcfproj` | Reference the project file directly when that form is clearer |
| `msbuild /t:rebuild /restore /p:Configuration=Release` | Build a release solution package |
| `msbuild` | Build using the current project defaults |
| `IncrementControlSolution\bin\debug` | Expected sample output folder for the generated solution zip |

## Import and App Usage

Import the generated solution zip manually through `make.powerapps.com` or by using Power Apps CLI deployment commands after connecting to the target environment. Add code components to model-driven apps by configuring them on fields or entities, and add them to canvas apps through the component framework support documented for canvas apps.

## Sample Catalog

Keep sample names exact when referring to them because the repository uses these folders and topics as discoverable examples.

| Sample | Demonstrates |
| --- | --- |
| `AngularJSFlipControl` | AngularJS-based sample control pattern |
| `CanvasGridControl` | Canvas grid control behavior |
| `ChoicesPickerControl` | Choices picker UI |
| `ChoicesPickerReactControl` | React choices picker variant |
| `CodeInterpreterControl` | Code interpreter sample behavior |
| `ControlStateAPI` | Control state API usage |
| `DataSetGrid` | Dataset grid control |
| `DeviceApiControl` | Device API interactions |
| `FacepileReactControl` | React facepile control |
| `FluentThemingAPIControl` | Fluent theming API behavior |
| `FormattingAPIControl` | Formatting API usage |
| `IFrameControl` | IFrame rendering |
| `ImageUploadControl` | Image upload behavior |
| `IncrementControl` | Basic increment control and solution packaging example |
| `LinearInputControl` | Linear input behavior |
| `LocalizationAPIControl` | Localization API usage |
| `LookupSimpleControl` | Lookup sample behavior |
| `MapControl` | Map rendering |
| `ModelDrivenGridControl` | Model-driven grid behavior |
| `MultiSelectOptionSetControl` | Multi-select option set behavior |
| `NavigationAPIControl` | Navigation API usage |
| `ObjectOutputControl` | Object output binding |
| `PowerAppsGridCustomizerControl` | Grid customization |
| `PropertySetTableControl` | Property set table behavior |
| `ReactStandardControl` | Standard React control baseline |
| `TableControl` | Table control behavior |
| `TableGrid` | Table grid behavior |
| `WebAPIControl` | Web API interaction |

## Sample Workflow Terminology

Preserve the documented sample workflow terms: open a `developer command prompt`, run `pac solution init`, create `IncrementControlSolution.cdsproj`, and pass a valid `path` to `pac solution add-reference`. These names map to official sample instructions and should remain exact when documenting the workflow.

## Good / Bad Examples

The examples below illustrate referencing a sample control from a solution folder.

**Good:**

```bash
pac solution init --publisher-name powerapps_samples --publisher-prefix sample
pac solution add-reference --path ../../IncrementControl/IncrementControl.pcfproj
msbuild /t:rebuild /restore /p:Configuration=Release
```

Why: The solution has sample publisher metadata, references the control project explicitly, and produces a release package.

**Bad:**

```bash
pac solution add-reference --path ../../SomeUnknownFolder
msbuild
```

Why: The reference path may not contain a `.pcfproj`, and the build does not restore or request the release configuration.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use Microsoft PowerApps-Samples as the source of sample components | Keeps examples aligned with official PCF sample code |
| Restore both npm and MSBuild dependencies before building | PCF samples depend on JavaScript and solution project packages |
| Initialize a solution folder beside the selected sample control | Keeps generated `.cdsproj` artifacts separate from control source |
| Reference the folder or `.pcfproj` that contains the control | `pac solution add-reference` needs the PCF project boundary |
| Import the generated zip through maker portal or Power Apps CLI | Samples must be installed in an environment before app authors can try them |
| Preserve exact sample component names | Names map to documented folders and topics |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `npm install` and `msbuild /t:restore` before solution builds | Build a fresh sample without restoring dependencies |
| Use `pac solution init --publisher-name powerapps_samples --publisher-prefix sample` for sample walkthroughs | Invent publisher metadata that obscures sample provenance |
| Reference `../../IncrementControl` or `../../IncrementControl/IncrementControl.pcfproj` | Point to a folder that does not contain the control project |
| Build release packages with `msbuild /t:rebuild /restore /p:Configuration=Release` | Assume a default `msbuild` always produces the package you need |
| Import through `make.powerapps.com` or documented CLI deployment flow | Treat the generated zip as active before importing it |
| Add controls to model-driven or canvas apps through supported component configuration | Copy sample source files directly into an app without packaging |

## Checklist Before Opening a PR

- [ ] The sample came from `github.com/microsoft/PowerApps-Samples` under `component-framework`.
- [ ] Power Platform CLI and Visual Studio MSBuild prerequisites are acknowledged for Windows sample workflows.
- [ ] `npm install` and `msbuild /t:restore` are used before building the solution.
- [ ] The solution folder and `.cdsproj` are separate from the component source folder.
- [ ] `pac solution add-reference` points to the selected sample folder or `.pcfproj`.
- [ ] The generated solution zip is imported before testing in a model-driven or canvas app.
- [ ] Sample names remain exact and discoverable.

## References

- Sample components: https://github.com/microsoft/PowerApps-Samples/tree/master/component-framework
- PowerApps-Samples repository: https://github.com/microsoft/PowerApps-Samples
- Component README: https://github.com/microsoft/PowerApps-Samples/blob/master/component-framework/README.md
- Download source archives: https://docs.github.com/repositories/working-with-files/using-files/downloading-source-code-archives#downloading-source-code-archives-from-the-repository-view
- Clone a repository: https://docs.github.com/repositories/creating-and-managing-repositories/cloning-a-repository
- Power Platform CLI for Windows: https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction#install-power-platform-cli-for-windows
- Developer Command Prompt: https://learn.microsoft.com/visualstudio/ide/reference/command-prompt-powershell
- Import solutions: https://learn.microsoft.com/powerapps/maker/data-platform/import-update-export-solutions
- Maker portal: https://make.powerapps.com/
- Connect to your environment: https://learn.microsoft.com/powerapps/developer/component-framework/import-custom-controls#connecting-to-your-environment
- Deploy code components: https://learn.microsoft.com/powerapps/developer/component-framework/import-custom-controls#deploying-code-components
- Add components to model-driven apps: https://learn.microsoft.com/powerapps/developer/component-framework/add-custom-controls-to-a-field-or-entity
- Add components to canvas apps: https://learn.microsoft.com/powerapps/developer/component-framework/component-framework-for-canvas-apps#add-components-to-a-canvas-app
