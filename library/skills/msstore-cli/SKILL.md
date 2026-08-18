---
name: msstore-cli
description: >-
  Use Microsoft Store Developer CLI (msstore) to configure Partner Center credentials, list Store apps, package and publish Windows submissions, check status, manage package flights, gradual rollouts, and CI/CD publishing for Windows App SDK/WinUI, UWP, .NET MAUI, Flutter, Electron, React Native, and PWA apps. Use when asked to configure Store credentials, publish to Microsoft Store, check submission status, or automate Store releases.
license: MIT
---

# Microsoft Store Developer CLI

Use `msstore` and its `winapp store` equivalent to authenticate with Partner Center, manage Microsoft Store apps, publish submissions, inspect flights, and automate release workflows.

## When to invoke

- "Configure msstore credentials for Partner Center."
- "Publish this Windows app to the Microsoft Store."
- "Check my Store submission status."
- "Set up CI/CD for Store publishing."
- "Manage package flights or gradual rollout with msstore."

## Prerequisites and context

| Requirement | Details |
| --- | --- |
| OS | Windows 10+, macOS, or Linux. |
| Runtime | .NET 9 Desktop Runtime on Windows, or .NET 9 Runtime on macOS/Linux. |
| Account | Partner Center account with appropriate permissions. |
| Azure app | Azure AD application with Partner Center API access. |
| Supported app types | Windows App SDK/WinUI, UWP, .NET MAUI, Flutter, Electron, React Native, and PWA applications. |
| Install options | Microsoft Store, WinGet, or manual GitHub release download. |

Install options:

```bash
winget install "Microsoft Store Developer CLI"
```

Use the Microsoft Store package at `https://www.microsoft.com/store/apps/9P53PC5S0PHJ` or manual releases at `https://aka.ms/msstoredevcli/releases` when WinGet is not appropriate.

## Partner Center setup

1. Go to `https://learn.microsoft.com/en-us/partner-center/` and open Partner Center.
2. Navigate to Account settings > User management > Azure AD applications.
3. Create an application and record Tenant ID, Client ID, and Client Secret.
4. Grant the application the Manager or Developer role.
5. Configure credentials with `msstore reconfigure` or environment variables.

## Credential configuration

| Environment variable | Description |
| --- | --- |
| `MSSTORE_TENANT_ID` | Azure AD Tenant ID. |
| `MSSTORE_SELLER_ID` | Partner Center Seller ID. |
| `MSSTORE_CLIENT_ID` | Azure AD Application Client ID. |
| `MSSTORE_CLIENT_SECRET` | Client Secret. |

Equivalent direct configuration:

```bash
msstore reconfigure --tenantId xxx --clientId xxx --clientSecret xxx
winapp store reconfigure --tenantId xxx --clientId xxx --clientSecret xxx
```

Do not print or commit `MSSTORE_CLIENT_SECRET`.

## Command map

| Task | `msstore` | `winapp store` equivalent |
| --- | --- | --- |
| Verify auth/account | `msstore info` | `winapp store info` |
| List apps | `msstore apps list` | `winapp store apps list` |
| Publish package/app folder | `msstore publish ./my-app` | `winapp store publish ./my-app` |
| Poll submission | `msstore submission poll <productId>` | `winapp store submission poll <productId>` |
| List flights | `msstore flights list <productId>` | `winapp store flights list <productId>` |

Use `winapp store` when the workflow benefits from a unified CLI for both packaging and publishing. The winapp CLI supports this integration in v0.2.0+.

## Store workflow coverage

| Workflow | What to check |
| --- | --- |
| Configure credentials | Tenant ID, Client ID, Client Secret, Seller ID, and Partner Center role. |
| List applications | Product ID and app identity from `msstore apps list`. |
| Package for submission | App package meets Store validation for the target framework. |
| Publish submission | Package path, metadata, target product, and rollout intent. |
| Package flights | Flight ID exists and target audience is correct. |
| Gradual rollout | Rollout percentage is between 0 and 100. |
| CI/CD | Secrets stored in the CI secret store, not in source files. |
| Metadata updates | Submission metadata is intentional and reviewable. |

## Troubleshooting

| Issue | Likely cause | Solution |
| --- | --- | --- |
| Authentication failed | Bad credentials or expired secret | Verify with `msstore info`; re-run `msstore reconfigure`. |
| App not found | Wrong product ID or account | Run `msstore apps list` to verify. |
| Insufficient permissions | Azure AD app lacks Partner Center role | Grant Manager or Developer in Partner Center. |
| Package validation failed | Package does not meet Store requirements | Check Partner Center validation details. |
| Submission stuck | Status needs polling or review | Run `msstore submission poll <productId>`. |
| Flight not found | Wrong flight ID | Verify with `msstore flights list <productId>`. |
| Rollout percentage invalid | Value outside allowed range | Use a value from 0 to 100. |
| Init fails for PWA | URL or manifest problem | Ensure URL is publicly accessible and has a valid web app manifest. |

## Progressive disclosure and bundled resources

- `references/commands-and-workflows.md`: detailed Microsoft Store CLI commands and publishing workflows. Open it when invoking `msstore` commands or following a publish/configuration workflow.

`msstore` is a `cross-platform` `command-line` interface; runtime wording may use `macOS/Linux`. The WinGet command may appear exactly as `winget install "Microsoft Store Developer CLI"`.

## Output template

```markdown
## Microsoft Store CLI result

**Status:** complete | blocked
**Workflow:** `configure | list apps | publish | submission status | flight | rollout | CI/CD`

### Commands
| Command | Result | Evidence |
| --- | --- | --- |
| `msstore <command>` | `<pass/fail/not run>` | `<output summary>` |

### Store context
- Product ID: `<productId or unknown>`
- Flight ID: `<flightId or not applicable>`
- Credentials source: `environment | msstore config | not configured`
```

## Quality gate

- [ ] Required runtime, Partner Center account, and Azure AD application prerequisites were checked for the requested workflow.
- [ ] Credentials used `msstore reconfigure`, `winapp store reconfigure`, or `MSSTORE_TENANT_ID`, `MSSTORE_SELLER_ID`, `MSSTORE_CLIENT_ID`, and `MSSTORE_CLIENT_SECRET`.
- [ ] Secrets were not printed, committed, or included in output.
- [ ] Product ID and flight ID were verified before status, publish, flight, or rollout operations.
- [ ] Rollout percentages were validated as 0 through 100.
- [ ] `winapp store` was used only when a unified packaging and publishing CLI was useful.

## References

- [Microsoft Store Developer CLI Documentation](https://learn.microsoft.com/windows/apps/publish/msstore-dev-cli/overview)
- [CLI Commands Reference](https://learn.microsoft.com/windows/apps/publish/msstore-dev-cli/commands)
- [GitHub Repository](https://github.com/microsoft/msstore-cli)
- [Partner Center API](https://learn.microsoft.com/windows/uwp/monetize/using-windows-store-services)
- [App Submission API](https://learn.microsoft.com/windows/uwp/monetize/create-and-manage-submissions-using-windows-store-services)
- [Package Flights Overview](https://learn.microsoft.com/windows/uwp/publish/package-flights)
- [Gradual Package Rollout](https://learn.microsoft.com/windows/uwp/publish/gradual-package-rollout)
- [Partner Center](https://learn.microsoft.com/en-us/partner-center/)
- [Microsoft Store package](https://www.microsoft.com/store/apps/9P53PC5S0PHJ)
- [Manual releases](https://aka.ms/msstoredevcli/releases)
