# Microsoft Store CLI commands and workflows

Moved from `../SKILL.md` for progressive disclosure. Use this reference only when the activated workflow needs the detailed material below.

## Core Commands Reference

### info - Print Configuration

Display the current credential configuration.

```bash
msstore info
```

**Options:**

| Option | Description |
| ------ | ----------- |
| `-v, --verbose` | Print verbose output |

### reconfigure - Configure Credentials

Configure or update Microsoft Store API credentials.

```bash
msstore reconfigure [options]
```

**Options:**

| Option | Description |
| ------ | ----------- |
| `-t, --tenantId` | Azure AD Tenant ID |
| `-s, --sellerId` | Partner Center Seller ID |
| `-c, --clientId` | Azure AD Application Client ID |
| `-cs, --clientSecret` | Client Secret for authentication |
| `-ct, --certificateThumbprint` | Certificate thumbprint (alternative to client secret) |
| `-cfp, --certificateFilePath` | Certificate file path (alternative to client secret) |
| `-cp, --certificatePassword` | Certificate password |
| `--reset` | Reset credentials without full reconfiguration |

**Examples:**

```bash
# Configure with client secret
msstore reconfigure --tenantId $TENANT_ID --sellerId $SELLER_ID --clientId $CLIENT_ID --clientSecret $CLIENT_SECRET

# Configure with certificate
msstore reconfigure --tenantId $TENANT_ID --sellerId $SELLER_ID --clientId $CLIENT_ID --certificateFilePath ./cert.pfx --certificatePassword MyPassword
```

### settings - CLI Settings

Change settings of the Microsoft Store Developer CLI.

```bash
msstore settings [options]
```

**Options:**

| Option | Description |
| ------ | ----------- |
| `-t, --enableTelemetry` | Enable (true) or disable (false) telemetry |

#### Set Publisher Display Name

```bash
msstore settings setpdn <publisherDisplayName>
```

Sets the default Publisher Display Name for the `init` command.

### apps - Application Management

List and retrieve application information.

#### List Applications

```bash
msstore apps list
```

Lists all applications in your Partner Center account.

#### Get Application Details

```bash
msstore apps get <productId>
```

**Arguments:**

| Argument | Description |
| -------- | ----------- |
| `productId` | The Store product ID (e.g., 9NBLGGH4R315) |

**Example:**

```bash
# Get details of a specific app
msstore apps get 9NBLGGH4R315
```

### submission - Submission Management

Manage Store submissions.

| Sub-Command | Description |
| ----------- | ----------- |
| `status` | Get submission status |
| `get` | Get submission metadata and package info |
| `getListingAssets` | Get listing assets of a submission |
| `updateMetadata` | Update submission metadata |
| `poll` | Poll submission status until complete |
| `publish` | Publish a submission |
| `delete` | Delete a submission |

#### Get Submission Status

```bash
msstore submission status <productId>
```

#### Get Submission Details

```bash
msstore submission get <productId>
```

#### Update Metadata

```bash
msstore submission updateMetadata <productId> <metadata>
```

Where `<metadata>` is a JSON string with the updated metadata. Because JSON contains characters that shells interpret (quotes, braces, etc.), you must quote and/or escape the value appropriately:

- **Bash/Zsh**: Wrap the JSON in single quotes so the shell passes it through literally.
  ```bash
  msstore submission updateMetadata 9NBLGGH4R315 '{"description":"My updated app"}'
  ```
- **PowerShell**: Use single quotes (or escape double quotes inside a double-quoted string).
  ```powershell
  msstore submission updateMetadata 9NBLGGH4R315 '{"description":"My updated app"}'
  ```
- **cmd.exe**: Escape each inner double quote with a backslash.
  ```cmd
  msstore submission updateMetadata 9NBLGGH4R315 "{\"description\":\"My updated app\"}"
  ```

> **Tip:** For complex or multi-line metadata, save the JSON to a file and pass its contents instead to avoid quoting issues:
> ```bash
> msstore submission updateMetadata 9NBLGGH4R315 "$(cat metadata.json)"
> ```

**Options:**

| Option | Description |
| ------ | ----------- |
| `-s, --skipInitialPolling` | Skip initial status polling |

#### Publish Submission

```bash
msstore submission publish <productId>
```

#### Poll Submission

```bash
msstore submission poll <productId>
```

Polls until the submission status is PUBLISHED or FAILED.

#### Delete Submission

```bash
msstore submission delete <productId>
```

**Options:**

| Option | Description |
| ------ | ----------- |
| `--no-confirm` | Skip confirmation prompt |

### init - Initialize Project for Store

Initialize a project for Microsoft Store publishing. Automatically detects project type and configures Store identity.

```bash
msstore init <pathOrUrl> [options]
```

**Arguments:**

| Argument | Description |
| -------- | ----------- |
| `pathOrUrl` | Project directory path or PWA URL |

**Options:**

| Option | Description |
| ------ | ----------- |
| `-n, --publisherDisplayName` | Publisher Display Name |
| `--package` | Also package the project |
| `--publish` | Package and publish (implies --package) |
| `-f, --flightId` | Publish to a specific flight |
| `-prp, --packageRolloutPercentage` | Gradual rollout percentage (0-100) |
| `-a, --arch` | Architecture(s): x86, x64, arm64 |
| `-o, --output` | Output directory for packages |
| `-ver, --version` | Version to use when building |

**Supported Project Types:**

- Windows App SDK / WinUI 3
- UWP
- .NET MAUI
- Flutter
- Electron
- React Native for Desktop
- PWA (Progressive Web Apps)

**Examples:**

```bash
# Initialize WinUI project
msstore init ./my-winui-app

# Initialize PWA
msstore init https://contoso.com --output ./pwa-package

# Initialize and publish
msstore init ./my-app --publish
```

### package - Package for Store

Package an application for Microsoft Store submission.

```bash
msstore package <pathOrUrl> [options]
```

**Arguments:**

| Argument | Description |
| -------- | ----------- |
| `pathOrUrl` | Project directory path or PWA URL |

**Options:**

| Option | Description |
| ------ | ----------- |
| `-o, --output` | Output directory for the package |
| `-a, --arch` | Architecture(s): x86, x64, arm64 |
| `-ver, --version` | Version for the package |

**Examples:**

```bash
# Package for default architecture
msstore package ./my-app

# Package for multiple architectures
msstore package ./my-app --arch x64,arm64 --output ./packages

# Package with specific version
msstore package ./my-app --version 1.2.3.0
```

### publish - Publish to Store

Publish an application to the Microsoft Store.

```bash
msstore publish <pathOrUrl> [options]
```

**Arguments:**

| Argument | Description |
| -------- | ----------- |
| `pathOrUrl` | Project directory path or PWA URL |

**Options:**

| Option | Description |
| ------ | ----------- |
| `-i, --inputFile` | Path to existing .msix or .msixupload file |
| `-id, --appId` | Application ID (if not initialized) |
| `-nc, --noCommit` | Keep submission in draft state |
| `-f, --flightId` | Publish to a specific flight |
| `-prp, --packageRolloutPercentage` | Gradual rollout percentage (0-100) |

**Examples:**

```bash
# Publish project
msstore publish ./my-app

# Publish existing package
msstore publish ./my-app --inputFile ./packages/MyApp.msixupload

# Publish as draft
msstore publish ./my-app --noCommit

# Publish with gradual rollout
msstore publish ./my-app --packageRolloutPercentage 10
```

### flights - Package Flight Management

Manage package flights (beta testing groups).

| Sub-Command | Description |
| ----------- | ----------- |
| `list` | List all flights for an app |
| `get` | Get flight details |
| `delete` | Delete a flight |
| `create` | Create a new flight |
| `submission` | Manage flight submissions |

#### List Flights

```bash
msstore flights list <productId>
```

#### Get Flight Details

```bash
msstore flights get <productId> <flightId>
```

#### Create Flight

```bash
msstore flights create <productId> <friendlyName> --group-ids <group-ids>
```

**Options:**

| Option | Description |
| ------ | ----------- |
| `-g, --group-ids` | Flight group IDs (comma-separated) |
| `-r, --rank-higher-than` | Flight ID to rank higher than |

#### Delete Flight

```bash
msstore flights delete <productId> <flightId>
```

#### Flight Submissions

```bash
# Get flight submission
msstore flights submission get <productId> <flightId>

# Publish flight submission
msstore flights submission publish <productId> <flightId>

# Check flight submission status
msstore flights submission status <productId> <flightId>

# Poll flight submission
msstore flights submission poll <productId> <flightId>

# Delete flight submission
msstore flights submission delete <productId> <flightId>
```

#### Flight Rollout Management

```bash
# Get rollout status
msstore flights submission rollout get <productId> <flightId>

# Update rollout percentage
msstore flights submission rollout update <productId> <flightId> <percentage>

# Halt rollout
msstore flights submission rollout halt <productId> <flightId>

# Finalize rollout (100%)
msstore flights submission rollout finalize <productId> <flightId>
```

## Common Workflows

### Workflow 1: First-Time Store Setup

```bash
# 1. Install the CLI
winget install "Microsoft Store Developer CLI"

# 2. Configure credentials (get these from Partner Center)
msstore reconfigure --tenantId $TENANT_ID --sellerId $SELLER_ID --clientId $CLIENT_ID --clientSecret $CLIENT_SECRET

# 3. Verify configuration
msstore info

# 4. List your apps to confirm access
msstore apps list
```

### Workflow 2: Initialize and Publish New App

```bash
# 1. Navigate to project
cd my-winui-app

# 2. Initialize for Store (creates/updates app identity)
msstore init .

# 3. Package the application
msstore package . --arch x64,arm64

# 4. Publish to Store
msstore publish .

# 5. Check submission status
msstore submission status <productId>
```

### Workflow 3: Update Existing App

```bash
# 1. Build your updated application
dotnet publish -c Release

# 2. Package and publish
msstore publish ./my-app

# Or publish from existing package
msstore publish ./my-app --inputFile ./artifacts/MyApp.msixupload
```

### Workflow 4: Gradual Rollout

```bash
# 1. Publish with initial rollout percentage
msstore publish ./my-app --packageRolloutPercentage 10

# 2. Monitor and increase rollout
msstore submission poll <productId>

# 3. (After validation) Finalize to 100%
# This completes via Partner Center or submission update
```

### Workflow 5: Beta Testing with Flights

```bash
# 1. Create a flight group in Partner Center first
# Then create a flight
msstore flights create <productId> "Beta Testers" --group-ids "group-id-1,group-id-2"

# 2. Publish to the flight
msstore publish ./my-app --flightId <flightId>

# 3. Check flight submission status
msstore flights submission status <productId> <flightId>

# 4. After testing, publish to production
msstore publish ./my-app
```

### Workflow 6: CI/CD Pipeline Integration

```yaml
# GitHub Actions example
name: Publish to Store

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '9.0.x'
      
      - name: Install msstore CLI
        run: winget install "Microsoft Store Developer CLI" --accept-package-agreements --accept-source-agreements
      
      - name: Configure Store credentials
        run: |
          msstore reconfigure --tenantId ${{ secrets.TENANT_ID }} --sellerId ${{ secrets.SELLER_ID }} --clientId ${{ secrets.CLIENT_ID }} --clientSecret ${{ secrets.CLIENT_SECRET }}
      
      - name: Build application
        run: dotnet publish -c Release
      
      - name: Publish to Store
        run: msstore publish ./src/MyApp
```

