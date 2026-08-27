# Git Integration: Concepts, Providers, and Supported Items

Reference for [git-integration-operations-cli](../SKILL.md). Grounds the automation
recipes in the Fabric Git integration model, the providers it supports, and the
item types that actually sync. Sourced from Microsoft Learn (see Provenance);
verify against Learn before relying on any preview or item-list detail, as the
supported-items list changes over time.

## Concepts

Git integration in Fabric operates at the **workspace level**: a workspace connects
to one Git **repository + branch + directory**, and all supported items in that
workspace version together as source files. The workspace folder structure is
mirrored in the repo (up to 10 levels deep).

**Connect and initial sync.** Connecting binds the workspace to the repo/branch/
directory. On the first sync:

- If one side is empty and the other has content, content is copied to the empty
  side automatically.
- If both sides have content, you must choose the direction. This is the
  `initializeConnection` `initializationStrategy`: `PreferWorkspace` (commit the
  workspace to Git) or `PreferRemote` (update the workspace from Git).

**The two sync directions.**

- **Commit** (workspace to Git): exports all supported workspace items as source
  files and overwrites the branch content. API `commitToGit`, `mode` `All` or
  `Selective`.
- **Update** (Git to workspace): imports the branch content and overwrites the
  workspace. This is destructive to unsynced workspace changes, so the portal asks
  for confirmation. API `updateFromGit`.

**Sync status.** `git/status` returns `workspaceHead` (the commit the workspace is
based on), `remoteCommitHash` (the branch tip), and a `changes` array. Functional
states:

| State | Meaning | Action |
|---|---|---|
| Synced | heads match, no changes | none |
| Uncommitted changes | workspace has edits not in Git | `commitToGit` |
| Update required | branch has commits the workspace lacks | `updateFromGit` |
| Conflict | the same item changed on both sides | `updateFromGit` with a `conflictResolutionPolicy` |

A folder-structure mismatch (workspace has subfolders the Git directory lacks)
shows as **uncommitted changes**: commit first, or an update overwrites the
workspace folder structure.

**Branches.** A workspace connects to exactly one branch. You can switch the branch
or **branch out** to a new workspace. Item identity across workspaces is stored as
portable **logical IDs**; whether cross-workspace references rebind versus break is
a property of the item definition format (logical vs object IDs), separate from the
Git lifecycle.

**Permissions (summary).**

- Connect / sync / disconnect / switch branch: workspace **Admin** (branch switch
  is also allowed for Member/Contributor with write access to all items when the
  workspace setting *Allow users with at least Contributor role to change Git
  branch* is on).
- Commit / update: **Contributor** with write permission on all items (update also
  needs item ownership when the tenant blocks nonowner updates, and BUILD on
  external dependencies where applicable).
- Git side: Azure Repos needs `Read` (plus `Contribute` to commit); GitHub needs
  Contents `Read` (plus `Write` to commit). Direct commit must be allowed by branch
  policy.
- The tenant admin must enable **Git integration**, and enable **cross-geo export**
  when a workspace and its *Azure* repo are in different regions (not required for
  GitHub). See Tenant admin prerequisites below for the full switch list.

## Tenant admin prerequisites

Git integration is gated by tenant admin switches (Admin portal, tenant settings).
The tenant admin can delegate each switch to the capacity or workspace admin, who
can then override it, and each switch can be scoped to the whole organization or to
a specific security group. Confirm these before a connect or sync, because a
disabled switch is a common cause of an otherwise unexplained failure:

- **Fabric admin switch** must be on. If Fabric is disabled, Git integration works
  only for Power BI items.
- **Users can synchronize workspace items with their Git repositories**: the master
  Git integration switch (covers Azure DevOps). Enabled by default.
- **Users can sync workspace items with GitHub repositories**: a separate switch for
  GitHub. **Disabled by default**, so it must be explicitly enabled before any
  GitHub connect.
- **Users can export items to Git repositories in other geographical locations**:
  required when the workspace capacity region differs from the *Azure DevOps* repo
  region (only item metadata is exported). GitHub does not enforce this switch.
- **Users can export workspace items with applied sensitivity labels to Git
  repositories**: required to export items that carry sensitivity labels (the labels
  themselves are not exported).

For service principal automation, also enable the developer/API switches that let
service principals call Fabric APIs and create connections (see
[SKILL.md § Create the Git provider connection (service principal)](../SKILL.md#create-the-git-provider-connection-service-principal)).

## Supported Git providers

All providers are **cloud-based only**:

- **Azure DevOps** (Azure Repos). Supports the automatic git credential (interactive
  user SSO) and a configured connection whose `credentialType` is either
  `ServicePrincipal` or `OAuth2`. May require the cross-geo export tenant switch when
  the workspace and repo regions differ.
- **GitHub**. Requires a Personal Access Token (PAT) stored in the configured
  connection: a fine-grained token with Contents `Read` (plus `Write` to commit), or
  a classic token with the `repo` scope. No automatic-credential mode, so a PAT is
  mandatory to connect.
- **GitHub Enterprise**.

For how these credentials attach to the connection (automatic vs configured /
service principal), see [SKILL.md § Connect a Workspace to Git](../SKILL.md#connect-a-workspace-to-git).

## Supported item types

The item types below currently support Git integration, grouped by workload.
Items marked *(preview)* are in preview. If a workspace or Git directory contains
**unsupported** items, it can still be connected, but those items are ignored: they
are not saved, synced, or deleted, and although they appear in the source control
panel you cannot commit or update them.

**Data Engineering**: Environment, GraphQL, Lakehouse, Notebooks, Spark Job
Definitions, User Data Functions.

**Data Science**: Machine learning experiments *(preview)*, Machine learning models
*(preview)*, Data Agents *(preview)*.

**Data Factory**: Copy Job, Dataflow Gen2, Pipeline, Mirrored database, Mount ADF,
Mirrored Snowflake *(preview)*.

**Real-Time Intelligence**: Activator *(preview)*, Eventhouse, Eventstream, KQL
database, KQL Queryset, Real-Time Dashboard, Event Schema Set *(preview)*, Maps,
Anomaly detection *(preview)*.

**Data Warehouse**: Warehouse *(preview)*, Mirrored Azure Databricks Catalog.

**Power BI**: Metrics Set *(preview)*, Org app *(preview)*, Paginated report
*(preview)*, Report *(preview)* (except reports connected to semantic models hosted
in Azure Analysis Services or SQL Server Analysis Services, or reports exported by
Power BI Desktop that depend on models hosted in My Workspace), Semantic model
*(preview)* (except push datasets, live connections to Analysis Services, and model
v1).

**Database**: SQL database, Cosmos database *(preview)*.

**Graph**: Graph in Microsoft Fabric *(preview)*.

**Industry solutions**: Healthcare *(preview)*, Healthcare Cohort *(preview)*.

## Provenance

Distilled from Microsoft Learn:

- [Overview of Fabric Git integration](https://learn.microsoft.com/fabric/cicd/git-integration/intro-to-git-integration) (providers, supported items; updated 2026-07-08).
- [Git integration process](https://learn.microsoft.com/fabric/cicd/git-integration/git-integration-process) (concepts, sync, folders, permissions; updated 2026-07-08).
- [Git integration admin settings](https://learn.microsoft.com/fabric/admin/git-integration-admin-settings) (tenant switches; updated 2026-07-01).
