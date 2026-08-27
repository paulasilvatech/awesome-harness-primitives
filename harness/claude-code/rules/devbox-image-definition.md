---
paths:
  - "**/*.yaml"
  - "**/*.yml"
---

<!-- Generated from harness/github-copilot/instructions/devbox-image-definition.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Microsoft Dev Box Team Customizations image definition conventions for task discovery, intrinsic task syntax, secrets, context placement, validation, and troubleshooting.

# Dev Box Image Definition Conventions — Team Customizations YAML

These instructions apply to YAML image definition files for Microsoft Dev Box Team Customizations. They are authoritative for Dev Box customization task discovery, intrinsic task names, system versus user task placement, Key Vault secret references, validation commands, local testing, and troubleshooting in matched YAML files; current Dev Box CLI output, selected Dev Box tools, and official Microsoft documentation win when they define a stricter or newer task contract.

## Authoritative Sources and Precedence

Follow these sources in order when authoring or reviewing image definition files:

1. The currently available Dev Box tools and the output of `devbox customizations list-tasks` for task names, parameters, examples, and availability.
2. Selected Dev Box tool generators or validators, including Customization WinGet Task Generator, Customization Git Clone Task Generator, Customization PowerShell Task Generator, Customization YAML Generation Planner, and Customization YAML Validator.
3. The official Microsoft Dev Box Team Customizations documentation listed in References.
4. These conventions for syntax, security, and review behavior when the above sources leave a choice.

## Tool and Task Discovery

Confirm tool support and available tasks before creating or modifying customization YAML.

- Prefer specialized Dev Box tools when they are enabled: Customization WinGet Task Generator for `~/winget`, Customization Git Clone Task Generator for `~/gitclone`, Customization PowerShell Task Generator for `~/powershell`, Customization YAML Generation Planner for planning, and Customization YAML Validator for validation.
- When tools are not available, recommend enabling Dev Box tools because they provide task-specific generation and validation.
- Run `devbox customizations list-tasks` before authoring YAML and use only tasks present in the output.
- If a desired task is unavailable, choose an available task or fall back to `~/powershell` when appropriate.
- Re-check available tasks when troubleshooting or when cached task data is older than 1 hour.

## Intrinsic Task Names and YAML Shape

Use the exact intrinsic task names and prefixes.

| Intrinsic task | Valid names | Convention |
| --- | --- | --- |
| WinGet | `__INTRINSIC_WinGet__`, `~/winget` | Use `name: ~/winget` for short-name YAML and package installs from the `winget` repository. |
| Git Clone | `__INTRINSIC_GitClone__`, `~/gitclone` | Use `name: ~/gitclone` for repository cloning. |
| PowerShell | `__INTRINSIC_PowerShell__`, `~/powershell` | Use `name: ~/powershell` for scripts or fallbacks. |

NEVER omit the `~/` prefix when using short intrinsic task names. `name: winget`, `name: powershell`, and `name: gitclone` can collide with custom tasks or fail to resolve.

Use literal scalar `|` for multi-line PowerShell scripts so commands remain readable and do not require newline escaping.

## System and User Task Placement

Place each task in the context that can execute it successfully.

| Section | Use for | Examples |
| --- | --- | --- |
| `tasks` | Administrative privileges, system-wide installation, or machine-level configuration | Core development tools, Git, .NET SDK, PowerShell Core, Visual C++ Redistributables, registry modifications, administrative software installations |
| `userTasks` | User profile, Microsoft Store, or user-specific configuration | Visual Studio Code extensions with `code --install-extension`, `winget` CLI msstore installs, AppX packages, user profile settings |

Start with system tasks for core tools and follow with user tasks for profile configuration. Group related operations in the same context to preserve execution order. If unsure, test in `tasks` first; move to `userTasks` when permissions or user-context requirements demand it.

## Secrets and Azure Key Vault

Do not hardcode sensitive values in image definition files.

- Store tokens, API keys, passwords, passphrases, database connection strings, and other sensitive data in Azure Key Vault.
- Reference Key Vault secrets with `{{KV_SECRET_URI}}` syntax.
- Remember that `{{}}` Key Vault syntax is resolved only at runtime; local `devbox` CLI tests do not resolve Key Vault values.
- Remove any temporarily hardcoded local-test secrets before committing.
- When helping with git operations, block or warn on commits that still contain hardcoded secrets and encourage Key Vault validation.
- Validate that secrets exist, the project Managed Identity can access them, and Key Vault networking allows the required access.

## Useful CLI Operations and Local Discovery

Use Dev Box CLI commands for validation and diagnostics.

| Command | Purpose |
| --- | --- |
| `devbox customizations list-tasks` | List available customization tasks, descriptions, parameters, and examples. |
| `devbox customizations apply-tasks --filePath "{image definition filepath}"` | Apply a customization file locally for testing and read console output. |
| `winget search "Visual Studio Code"` | Discover package IDs such as `Microsoft.VisualStudioCode` when WinGet is installed locally. |

When WinGet is missing and local package discovery is needed, install it with PowerShell using `$progressPreference = 'silentlyContinue'`, `Invoke-WebRequest -Uri https://aka.ms/getwinget -OutFile Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle`, and `Add-AppxPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle`, or download the latest `.msixbundle` from GitHub releases.

If saving `devbox customizations list-tasks` output for reuse, use `customization_tasks.json` outside source control and refresh it after 1 hour or when troubleshooting suggests task availability changed. Do not place this cache in the repository.

## PowerShell and Download Practices

Keep inline PowerShell robust in the Dev Box task environment.

- Prefer single quotes inside inline PowerShell where possible; escape double-quotes carefully when interpolation or command syntax requires them.
- Test long or complex PowerShell in a standalone file first, then adapt it into YAML.
- Extract repeated or large scripts into custom tasks when reuse, error handling, or maintainability justifies it.
- Put `$progressPreference = 'SilentlyContinue'` before `Invoke-WebRequest` or `Start-BitsTransfer` downloads to reduce progress overhead.
- For large downloads, prefer Azure Storage with `azcopy` or Azure CLI, or clone files with `~/gitclone`, instead of downloading individual large files through inline PowerShell.

## WinGet and Microsoft Store Constraints

Use the intrinsic `~/winget` task for normal `winget` repository packages. The built-in task does not support non-`winget` sources such as `msstore`.

When installing from `msstore` is required:

- Use `~/powershell` to invoke the `winget` CLI directly.
- Place the task in `userTasks` because Microsoft Store installs require user context.
- Ensure the `winget` CLI is available in the user context `PATH`.
- Include `--accept-source-agreements` and `--accept-package-agreements` to avoid interactive prompts.

## Troubleshooting

Use logs and isolation to diagnose failed customization tasks.

- Find logs under `C:\ProgramData\Microsoft\DevBoxAgent\Logs\customizations`.
- Use the most recent timestamp folder in `yyyy-MM-DDTHH-mm-ss` format.
- Inspect the `tasks` subfolder and each task subfolder for `stderr.log`.
- Treat an empty `stderr.log` as likely success and non-empty content as failure evidence.
- Test tasks individually when the failing task is unclear.
- For `System tasks are not allowed in standard usercontext`, move administrative work to `tasks` and test with appropriate privileges.
- If the current task cannot satisfy the requirement, evaluate alternatives from `devbox customizations list-tasks` and consider `~/powershell` as the fallback.

## Good / Bad Examples

The examples below illustrate intrinsic task naming, context placement, and readable PowerShell.

**Good:**

```yaml
tasks:
  - name: ~/winget
    parameters:
      packageId: Microsoft.VisualStudioCode
userTasks:
  - name: ~/powershell
    parameters:
      command: |
        $progressPreference = 'SilentlyContinue'
        winget install --id Microsoft.WindowsTerminal --source msstore --accept-source-agreements --accept-package-agreements
```

Why: Intrinsic task names use `~/`, system and user tasks are separated, and the Microsoft Store install runs in user context.

**Bad:**

```yaml
tasks:
  - name: winget
  - name: powershell
    parameters:
      command: "winget install --source msstore Microsoft.WindowsTerminal"
```

Why: The intrinsic names omit `~/`, the Store install is in the wrong context, and the command can prompt interactively.

## Dev Box Tooling Vocabulary

Retain these Dev Box terms because documentation, tools, and troubleshooting output use them directly.

- ` folder) called `
- ` label in the dev box tools. For example, `
- `), Git Clone (`
- `), and PowerShell (`
- `devbox_customization_winget_task_generator`, `Task Generator`, `Customization {task_name} Task Generator`, `task_name`, `Customization YAML Generation Planner`, and `Customization YAML Validator`.
- `FIRST`, `SECOND`, `STEP`, `PREREQUISITE`, `MANDATORY`, `IMPORTANT`, `NOTE`, `CRITICAL`, `SECURITY`, `INFORMATION`, `TROUBLESHOOTING`, `MUST`, `ALWAYS`, `TEMP`, and `JSON`.
- `Azure CLI`, `.msixbundle`, `--source msstore`, `winget install`, `winget search`, `single-quotes`, `hard-coded`, `runtime-only`, `inner-loop`, `ad-hoc`, `up-to-date`, `and/or`, `recommendations-on-validating-key-vault-setup`, and keeping-track-of-the-available-customization-tasks-for-use-during-prompting.

## Conventions

| Rule | Rationale |
|---|---|
| Run `devbox customizations list-tasks` before authoring YAML | Available tasks vary by Dev Box environment |
| Use selected Dev Box generators and validators when available | Specialized tools know intrinsic task schemas better than generic YAML generation |
| Prefix intrinsic short names with `~/` | Avoids collisions and unresolved task names |
| Place administrative work in `tasks` and user-profile work in `userTasks` | Wrong context causes permission and access failures |
| Use `{{KV_SECRET_URI}}` for Key Vault secrets and remove local hardcoded values | YAML files must not commit secrets |
| Use `|` for multi-line PowerShell | Scripts remain readable and safer to edit |
| Check `stderr.log` files under Dev Box Agent logs when apply-tasks fails | Task-level logs identify root causes |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `name: ~/winget`, `name: ~/gitclone`, and `name: ~/powershell` | Use `name: winget`, `name: gitclone`, or `name: powershell` |
| Validate with `devbox customizations apply-tasks --filePath "{image definition filepath}"` when feasible | Assume syntactically valid YAML applies successfully |
| Use Azure Key Vault and Managed Identity for sensitive values | Commit tokens, passwords, passphrases, or connection strings |
| Put msstore `winget` CLI installs in `userTasks` with agreement flags | Use intrinsic `~/winget` for non-`winget` sources |
| Inspect logs before guessing at a failed customization | Rewrite unrelated tasks without evidence |

## Checklist Before Opening a PR

- [ ] `devbox customizations list-tasks` was reviewed for the target environment.
- [ ] Every task name exists in the available task list or is an approved custom task.
- [ ] Intrinsic short task names use `~/winget`, `~/gitclone`, or `~/powershell`.
- [ ] Administrative operations are in `tasks`; user-profile, Store, and extension operations are in `userTasks`.
- [ ] Multi-line PowerShell uses `|` and avoids fragile quoting.
- [ ] Secrets use `{{KV_SECRET_URI}}`; no hardcoded secrets remain.
- [ ] Key Vault access, Managed Identity, and network configuration were considered for runtime secret resolution.
- [ ] `devbox customizations apply-tasks --filePath "{image definition filepath}"` or the selected validator was run when available.
- [ ] Troubleshooting notes reference `C:\ProgramData\Microsoft\DevBoxAgent\Logs\customizations` when failures occurred.

## References

- [Team Customizations docs](https://learn.microsoft.com/azure/dev-box/concept-what-are-team-customizations?tabs=team-customizations)
- [Write an image definition file for Dev Box Team Customizations](https://learn.microsoft.com/azure/dev-box/how-to-write-image-definition-file)
- [Create an image definition file with Copilot](https://learn.microsoft.com/azure/dev-box/how-to-use-copilot-generate-image-definition-file)
- [Use Azure Key Vault secrets in customization files](https://learn.microsoft.com/azure/dev-box/how-to-use-secrets-customization-files)
- [Use Team Customizations](https://learn.microsoft.com/azure/dev-box/quickstart-team-customizations)
- [Example YAML customization file](https://aka.ms/devcenter/preview/imaging/examples)
- [System tasks and user tasks](https://learn.microsoft.com/azure/dev-box/how-to-configure-team-customizations#system-tasks-and-user-tasks)
- [Create a customization task](https://learn.microsoft.com/azure/dev-box/how-to-configure-customization-tasks#what-are-tasks)
- [Transfer data using AzCopy](https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-v10?tabs=dnf#transfer-data)
- [Download a file from Azure Storage](https://learn.microsoft.com/azure/dev-box/how-to-customizations-connect-resource-repository#example-download-a-file-from-azure-storage)
- [WinGet install package](https://aka.ms/getwinget)
- [WinGet CLI releases](https://github.com/microsoft/winget-cli/releases)
