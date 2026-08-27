---
paths:
  - "**/*.{yml,yaml,ps1,json,pbix,pbir}"
---

<!-- Generated from harness/github-copilot/instructions/power-bi-devops-alm-best-practices.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Power BI DevOps and ALM conventions for PBIP source control, CI/CD deployment, environment promotion, testing, secrets, rollback, and monitoring.

# Power BI DevOps and ALM Conventions — PBIP, CI/CD, and Fabric Deployment

These instructions apply to Power BI project, pipeline, PowerShell, and configuration files matched by the `applyTo` globs. They are authoritative for Power BI DevOps, Application Lifecycle Management, PBIP source control, Power BI REST API deployment, Fabric REST API deployment, environment promotion, test gates, release rollback, and deployment monitoring; repository security, organization release policy, and platform-specific CI rules win where they impose stricter controls.

## PBIP Source Control and Project Shape

Keep Power BI work in source-control-friendly PBIP form whenever a report or semantic model is maintained by a team. Store model, report, and configuration changes as reviewable files instead of relying on untracked Desktop publishing.

| Area | Convention |
| --- | --- |
| Project layout | Preserve the PBIP split between `Model/`, `Report/`, and `.git/`; keep `Model/model.tmdl`, `Model/tables/`, `Model/relationships/relationships.tmdl`, `Model/measures/measures.tmdl`, `Report/report.json`, `Report/pages/`, `Report/pages/ReportSection1/page.json`, `Report/pages/ReportSection1/visuals/`, `Report/pages/pages.json`, and `Report/bookmarks/` reviewable. |
| Table files | Add new TMDL artifacts such as `Model/tables/NewTable.tmdl` on feature branches so semantic model diffs are visible. |
| Branching | Use feature branches such as `feature/new-dashboard` or `new-dashboard`, merge through review, and tag releases such as `v1.2.0` after a tested promotion. |
| Git commands | Keep `git init`, `git add .`, `git commit -m "Initial Power BI project structure"`, `git checkout -b feature/new-dashboard`, `git checkout main`, `git merge feature/new-dashboard`, and `git tag -a v1.2.0 -m "Release version 1.2.0"` as the canonical Git shape for examples and automation. |
| Anti-pattern | Do not make direct production changes, skip version control, or rely on manual audit trails; Power BI DevOps requires version-controlled model, report, and configuration changes. |

## Deployment Automation

Automate promotions through Power BI Deployment Pipelines, Azure DevOps, or Fabric REST API rather than publishing by hand. Treat deployment scripts as repeatable release assets.

| Deployment surface | Required conventions |
| --- | --- |
| Power BI Deployment Pipelines API | Use `Invoke-PowerBIRestMethod` against `pipelines/{0}/Deploy` with `sourceStageOrder`, `datasets`, `reports`, `dashboards`, `sourceId`, and `options`; set `allowCreateArtifact = $TRUE` and `allowOverwriteArtifact = $TRUE` only when controlled promotion allows create or overwrite behavior. |
| Operation polling | Read `pipelines/{0}/Operations/{1}` after deployment; poll while `Status` is `NotStarted` or `Executing`; use `Start-Sleep -s 5` rather than a tight loop. |
| Azure DevOps | Keep Power BI release stages on `windows-latest` when scripts depend on Windows PowerShell behavior; use `CopyFiles@2`, `PowerPlatformToolInstaller@2`, `PowerPlatformExportData@2`, and `PowerShell@2` with named inputs. |
| FabricPS-PBIP | Download `FabricPS-PBIP.psm1` and `FabricPS-PBIP.psd1` from `https://raw.githubusercontent.com/microsoft/Analysis-Services/master/pbidevmode/fabricps-pbip/FabricPS-PBIP.psm1` and `https://raw.githubusercontent.com/microsoft/Analysis-Services/master/pbidevmode/fabricps-pbip/FabricPS-PBIP.psd1` only when the project standard has not vendored or pinned the module elsewhere. |
| Fabric import | Use `Set-FabricAuthToken -reset`, `New-FabricWorkspace -name $workspaceName -skipErrorIfExists`, `Import-FabricItem -workspaceId $workspaceId -path $pbipSemanticModelPath`, and `Import-FabricItem -workspaceId $workspaceId -path $pbipReportPath -itemProperties @{ "semanticModelId" = $semanticModelImport.Id }` to bind reports to the imported semantic model. |
| Build variables | Preserve `$(Build.ArtifactStagingDirectory)`, `$(ProjectName).SemanticModel`, `$(ProjectName).Report`, `$(WorkspaceName)`, `$(BuildTools.EnvironmentUrl)`, `$(TestWorkspaceName)`, `$(ProdWorkspaceName)`, and `Build.SourceBranch` as environment-controlled inputs. |

## Environment Management

Separate development, test, and production workspaces, datasets, credentials, schedules, and labels. Environment coupling is a release risk.

| Environment item | Convention |
| --- | --- |
| Workspace IDs | Keep explicit workspace identifiers such as `dev-workspace-id`, `test-workspace-id`, and `prod-workspace-id` in environment configuration, not in scripts. |
| Data sources | Parameterize `dev-database.database.windows.net`, `test-database.database.windows.net`, and `prod-database.database.windows.net`; do not hardcode connection strings. |
| Promotion path | Promote through `dev/test/prod`; production releases should run only from `refs/heads/main`. |
| PowerShell parameters | Use `param`, `[Parameter(Mandatory=$true)]`, `[ValidateSet("dev", "test", "prod")]`, `$Environment`, `$WorkspaceName`, and optional `$DataSourceServer` for deployment entry points. |
| Configuration files | Load `.\config\$Environment.json`-style environment files or their project equivalent and compose `Data Source=...;Initial Catalog=...;Integrated Security=SSPI;` from configuration. |
| Labels and schedules | Keep `sensitivityLabel` values such as `Internal` and `Confidential`, and refresh schedules such as `manual`, `daily`, and `hourly`, environment-specific. |

## Automated Data Quality and Performance Tests

Run automated semantic-model tests before promotion. Use DAX queries and REST `executeQueries` calls for repeatable validation.

| Test type | Convention |
| --- | --- |
| Data quality | Keep `Test-PowerBIDataQuality` with `$WorkspaceId` and `$DatasetId` parameters; query `groups/$WorkspaceId/datasets/$DatasetId/executeQueries` and `WorkspaceId/datasets/` or `DatasetId/executeQueries` paths through `Invoke-PowerBIRestMethod`. |
| Row count | Preserve DAX patterns using `EVALUATE`, `ADDCOLUMNS`, `SUMMARIZE`, `COUNTROWS`, `ExpectedMin`, `PASS`, and `FAIL` to validate minimum data volume. |
| Freshness | Preserve DAX patterns using `ROW`, `MAX`, `DATEDIFF`, `TODAY`, `DAY`, and the one-day freshness threshold when validating `Sales[Date]`. |
| Performance | Keep `Test-PowerBIPerformance` with `Dashboard Load Time`, `Complex Calculation`, `TOPN(1000, Sales)`, `[Sales] * [Profit Margin %]`, `MaxDurationMs = 5000`, `MaxDurationMs = 10000`, `TotalMilliseconds`, `Passed`, and `Threshold`. |
| Test result names | Preserve `RowCountTest`, `FreshnessTest`, `TestName`, `Duration`, and `Threshold` for result contracts consumed by dashboards or release gates. |

## Configuration, Infrastructure, and Secrets

Represent workspace, dataset, refresh, credential, and access settings as declarative configuration when possible. Keep secrets in managed stores.

| Concern | Convention |
| --- | --- |
| Workspace config | Capture `workspace.name`, `description`, `capacityId`, `A1-capacity-id`, `users`, `emailAddress`, `accessRight`, `Admin`, `Member`, `principalType`, `App`, `settings`, `datasetDefaultStorageFormat`, `Large`, and `blockResourceKeyAuthentication` as deployable configuration. |
| Dataset config | Capture `datasets`, `name`, `Sales Analytics`, `refreshSchedule`, `enabled`, `times`, `06:00`, `12:00`, `18:00`, weekday names `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `timeZone`, `UTC`, `datasourceCredentials`, `credentialType`, `OAuth2`, and `encryptedConnection`, `Encrypted`. |
| Key Vault | Use `Get-PowerBICredentials`, `Get-AzKeyVaultSecret`, `-VaultName`, `-Name`, and `-AsPlainText` to retrieve `PowerBI-ServicePrincipal-Id-$Environment`, `PowerBI-ServicePrincipal-Secret-$Environment`, and `PowerBI-TenantId-$Environment`. |
| Authentication | Convert the secret with `ConvertTo-SecureString`, create `System.Management.Automation.PSCredential`, and call `Connect-PowerBIServiceAccount -ServicePrincipal -Credential $credential -TenantId $credentials.TenantId`. |
| Module installation | Use `Get-Module Az.Accounts -ListAvailable`, `Install-Module Az.Accounts -Scope CurrentUser -Force`, `Import-Module ".\modules\FabricPS-PBIP" -Force`, `New-Item -ItemType Directory -Path ".\modules" -ErrorAction SilentlyContinue | Out-Null`, and `Invoke-WebRequest -Uri $_ -OutFile ".\modules\$(Split-Path $_ -Leaf)"` consistently. |

## Release, Rollback, and Health Monitoring

A Power BI release is complete only after validation, rollback readiness, and health checks. Manual deployments without rollback are an anti-pattern.

| Area | Convention |
| --- | --- |
| Release stages | Keep `Build`, `DeployTest`, and `DeployProd` stages; run production only when `condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))` is satisfied. |
| Build validation | Validate `Model\model.tmdl`, `Report\report.json`, and `Model\tables`; fail with `throw "Missing required file: $file"` when required files are absent. |
| Templates | Use deployment templates such as `deploy-powerbi.yml` and parameters `environment: 'test'`, `environment: 'prod'`, and `workspaceName`. |
| Rollback | Keep `Invoke-PowerBIRollback` with `$WorkspaceId`, `$BackupVersion`, and `$BackupLocation`; create an `emergency-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')`, call `Export-PowerBIReport`, restore `$BackupVersion.pbix` with `Import-PowerBIReport -ConflictAction "Overwrite"`, then run `Test-PowerBIDataQuality`. |
| Health checks | Keep `Test-DeploymentHealth` with `$ExpectedReports` and `$ExpectedDatasets`; use `Get-PowerBIReport`, `Get-PowerBIDataset`, `RefreshState`, and statuses `Healthy`, `Unhealthy`, `Degraded`, and `Failed`. |
| Notifications | Keep `Send-DeploymentNotification`, `$TeamsWebhookUrl`, `$DeploymentResult`, `$Environment`, status colors `28A745`, `FFC107`, `DC3545`, `@type = MessageCard`, `@context = https://schema.org/extensions`, `themeColor`, `sections`, `activityTitle`, `activitySubtitle`, `facts`, `ReportsCount`, `application/json`, and `Invoke-RestMethod -ContentType 'application/json'`. |

## Operational API and Identifier Vocabulary

Preserve these Power BI DevOps identifiers because scripts, examples, and pipeline contracts commonly depend on them: `powerbi-service-principal`, `FactSales`, `DimProduct`, `GitFlow`, `CleanTargetFolder`, `TargetFolder`, `SchemaFile`, `DataFile`, `DefaultVersion`, `KeyVault`, `KeyVaultName`, `BackupName`, `FilePath`, `ReportId`, `RowCount`, `DaysOld`, `LastRefresh`, `ComplexCalc`, `ConvertFrom`, `MyInvocation`, `MyCommand`, `MyInvocation.MyCommand.Definition`, `DeploymentResult.Status`, `DeploymentResult.Duration`, and `DeploymentResult.ReportsCount`.

## Good / Bad Examples

The examples below illustrate automated deployment with explicit artifact, workspace, and binding inputs instead of untracked Desktop publishing.

**Good:**

```powershell
Set-FabricAuthToken -reset
$workspaceId = New-FabricWorkspace -name $workspaceName -skipErrorIfExists
$semanticModelImport = Import-FabricItem -workspaceId $workspaceId -path $pbipSemanticModelPath
Import-FabricItem -workspaceId $workspaceId -path $pbipReportPath -itemProperties @{ "semanticModelId" = $semanticModelImport.Id }
```

Why: The release is repeatable, creates or reuses the workspace, imports the semantic model first, and binds the report to the exact semantic model ID.

**Bad:**

```powershell
Write-Host "Publish the PBIX from Desktop, then change production settings manually."
```

Why: Manual Desktop publishing loses version history, skips validation, creates configuration drift, and leaves no reliable rollback path.

## Conventions

| Rule | Rationale |
|---|---|
| Use PBIP source files for team-owned reports and models | PBIP makes model, report, and configuration changes reviewable in Git |
| Keep deployment scripts parameter-driven by workspace, item path, dataset, and environment | The same automation can promote through dev, test, and production without hardcoded values |
| Poll Power BI deployment operations until terminal status | Promotion is not complete when the initial REST call returns an operation ID |
| Gate releases with data quality, freshness, and performance tests | Broken or stale semantic models are caught before users see them |
| Store service principal credentials in Azure Key Vault or equivalent managed secret storage | Secrets stay out of repository files, logs, and build artifacts |
| Treat rollback as a first-class release requirement | Failed deployments can be restored quickly with a known backup and validation path |
| Send structured deployment notifications to Teams or another alerting surface | Operators receive status, duration, and artifact counts without parsing logs |

## Do / Do Not

| Do | Do not |
|---|---|
| Commit PBIP model and report files such as `Model/model.tmdl` and `Report/report.json` | Treat `.pbix` Desktop publishing as the only release record |
| Use `Invoke-PowerBIRestMethod`, Fabric REST API helpers, or deployment pipeline APIs for promotion | Manually change workspace artifacts in production |
| Keep `dev/test/prod` settings in environment-specific configuration | Hardcode workspace IDs, data source URLs, or refresh schedules in scripts |
| Retrieve `ServicePrincipalId`, `ServicePrincipalSecret`, and `TenantId` from Key Vault | Put service principal secrets in YAML, JSON, or PowerShell source |
| Run data quality and performance tests with explicit thresholds | Promote without checking row counts, freshness, or query duration |
| Keep emergency backups and restore commands tested | Discover rollback mechanics during an outage |

## Checklist Before Opening a PR

- [ ] PBIP model, report, and configuration changes are source-controlled and reviewable.
- [ ] Deployment automation uses parameterized workspace, report, semantic model, dataset, and environment values.
- [ ] Power BI Deployment Pipelines or Fabric deployment calls poll operation status before declaring success.
- [ ] Environment configuration separates development, test, and production workspace IDs, data sources, labels, and schedules.
- [ ] Data quality, freshness, and performance tests preserve their DAX queries, REST paths, and thresholds.
- [ ] Service principal secrets come from Azure Key Vault or managed secret storage and are not committed.
- [ ] Release stages include validation, production branch gating, rollback, health checks, and deployment notification.

## References

- FabricPS-PBIP module file: https://raw.githubusercontent.com/microsoft/Analysis-Services/master/pbidevmode/fabricps-pbip/FabricPS-PBIP.psm1
- FabricPS-PBIP manifest file: https://raw.githubusercontent.com/microsoft/Analysis-Services/master/pbidevmode/fabricps-pbip/FabricPS-PBIP.psd1
- MessageCard schema context: https://schema.org/extensions
