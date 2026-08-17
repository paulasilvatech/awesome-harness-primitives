---
name: "msstore-cli"
description: >-
  Microsoft Store Developer CLI (msstore) for publishing Windows applications to the Microsoft Store.
  Use when asked to configure Store credentials, list Store apps, check submission status, publish
  submissions, manage package flights, set up CI/CD for Store publishing, or integrate with Partner
  Center. Supports Windows App SDK/WinUI, UWP, .NET MAUI, Flutter, Electron, React Native, and PWA
  applications.
license: "MIT"
---
# Microsoft Store Developer CLI (msstore)

The Microsoft Store Developer CLI (`msstore`) is a cross-platform command-line interface for publishing and managing applications in the Microsoft Store. It integrates with Partner Center APIs and supports automated publishing workflows for various application types.

## When to Use This Skill

Use this skill when you need to:

- Configure Store credentials for API access
- List applications in your Store account
- Check the status of a submission
- Publish submissions to the Store
- Package applications for Store submission
- Initialize projects for Store publishing
- Manage package flights (beta testing)
- Set up CI/CD pipelines for automated Store publishing
- Manage gradual rollouts of submissions
- Update submission metadata programmatically

## Prerequisites

- Windows 10+, macOS, or Linux
- .NET 9 Desktop Runtime (Windows) or .NET 9 Runtime (macOS/Linux)
- Partner Center account with appropriate permissions
- Azure AD app registration with Partner Center API access
- msstore CLI installed via one of these methods:
  - **Microsoft Store**: [Download](https://www.microsoft.com/store/apps/9P53PC5S0PHJ)
  - **WinGet**: `winget install "Microsoft Store Developer CLI"`
  - **Manual**: Download from [GitHub Releases](https://aka.ms/msstoredevcli/releases)

### Partner Center Setup

Before using msstore, you need to create an Azure AD application with Partner Center access:

1. Go to [Partner Center](https://learn.microsoft.com/en-us/partner-center/)
2. Navigate to **Account settings** > **User management** > **Azure AD applications**
3. Create a new application and note the **Tenant ID**, **Client ID**, and **Client Secret**
4. Grant the application appropriate permissions (Manager or Developer role)

## Bundled Resources

- [Microsoft Store CLI commands and workflows](references/commands-and-workflows.md) — When invoking msstore commands or following a publish/configuration workflow, open this command reference.

## Integration with winapp CLI

The winapp CLI (v0.2.0+) integrates with msstore via the `winapp store` subcommand:

```bash
# These commands are equivalent:
msstore reconfigure --tenantId xxx --clientId xxx --clientSecret xxx
winapp store reconfigure --tenantId xxx --clientId xxx --clientSecret xxx

# List apps
msstore apps list
winapp store apps list

# Publish
msstore publish ./my-app
winapp store publish ./my-app
```

Use `winapp store` when you want a unified CLI experience for both packaging and publishing.

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| Authentication failed | Verify credentials with `msstore info`; re-run `msstore reconfigure` |
| App not found | Ensure the product ID is correct; run `msstore apps list` to verify |
| Insufficient permissions | Check Azure AD app role in Partner Center (needs Manager or Developer) |
| Package validation failed | Ensure package meets Store requirements; check Partner Center for details |
| Submission stuck | Run `msstore submission poll <productId>` to check status |
| Flight not found | Verify flight ID with `msstore flights list <productId>` |
| Rollout percentage invalid | Value must be between 0 and 100 |
| Init fails for PWA | Ensure URL is publicly accessible and has valid web app manifest |

## Environment Variables

The CLI supports environment variables for credentials:

| Variable | Description |
| -------- | ----------- |
| `MSSTORE_TENANT_ID` | Azure AD Tenant ID |
| `MSSTORE_SELLER_ID` | Partner Center Seller ID |
| `MSSTORE_CLIENT_ID` | Azure AD Application Client ID |
| `MSSTORE_CLIENT_SECRET` | Client Secret |

## References

- [Microsoft Store Developer CLI Documentation](https://learn.microsoft.com/windows/apps/publish/msstore-dev-cli/overview)
- [CLI Commands Reference](https://learn.microsoft.com/windows/apps/publish/msstore-dev-cli/commands)
- [GitHub Repository](https://github.com/microsoft/msstore-cli)
- [Partner Center API](https://learn.microsoft.com/windows/uwp/monetize/using-windows-store-services)
- [App Submission API](https://learn.microsoft.com/windows/uwp/monetize/create-and-manage-submissions-using-windows-store-services)
- [Package Flights Overview](https://learn.microsoft.com/windows/uwp/publish/package-flights)
- [Gradual Package Rollout](https://learn.microsoft.com/windows/uwp/publish/gradual-package-rollout)
