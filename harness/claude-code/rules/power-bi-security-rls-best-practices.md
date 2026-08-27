---
paths:
  - "**/*.{pbix,dax,md,txt,json,csharp,powershell}"
---

<!-- Generated from harness/github-copilot/instructions/power-bi-security-rls-best-practices.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Power BI security and Row-Level Security conventions for DAX roles, dynamic security, embedded analytics identities, database RLS integration, governance, monitoring, and auditability.

# Power BI Security Conventions — Row-Level Security and Embedded Analytics

These instructions apply to Power BI models, DAX, documentation, JSON embed-token payloads, C# embedding code, and PowerShell governance scripts matched by the `applyTo` globs. They are authoritative for Power BI Row-Level Security (RLS), dynamic security, embedded analytics identities, database-level RLS integration, Power Pages embedding, multi-tenant token shape, security validation, and governance patterns; tenant identity policy, compliance requirements, and platform access-management standards win where they impose stricter controls.

## Row-Level Security Fundamentals

Write RLS predicates as explicit allow rules with default-deny behavior. Use `USERNAME()` for user-context filters, `CUSTOMDATA()` for controlled embedded custom data, and `FALSE()` when a user or role is unexpected.

| Pattern | Convention | Rationale |
| --- | --- | --- |
| Basic user filter | `[EmailAddress] = USERNAME()` | Directly binds model access to the signed-in user. |
| Role switch | Use `IF` or `SWITCH` where known roles such as `Worker`, `Manager`, `SalesPersonA`, and `SalesPersonB` map to allowed rows. | Role semantics stay visible and auditable. |
| Dynamic custom data | Set `VAR UserRole = CUSTOMDATA()` and map it with `SWITCH`. | Embedded scenarios can pass a controlled role value without changing the model. |
| Hierarchical lookup | Use `LOOKUPVALUE` against `DimUserSecurity`, `UserRoles`, or `UserRegions`. | Territory, region, and manager relationships stay data-driven. |
| Multi-value access | Use `FILTER`, `SELECTCOLUMNS`, and `IN` against a user-security table. | Users can have several allowed territories without hardcoded predicates. |
| Default deny | End predicates with `FALSE()`. | Unexpected users and roles receive no data rather than all data. |

Avoid overly permissive defaults such as `TRUE()` in the fallback branch. Keep DAX security logic readable enough that reviewers can reason about every path.

## Dynamic, Hierarchical, and Partial RLS

Use dynamic RLS when access depends on user attributes, tenant, territory, or role stored in data. Common measures and predicates include `VAR CurrentUser = USERNAME()`, `VAR UserRole = LOOKUPVALUE(UserRoles[Role], UserRoles[Email], CurrentUser)`, and `SWITCH(UserRole, "Manager", TRUE(), "Salesperson", [SalespersonEmail] = CurrentUser, "Regional Manager", [Region] IN SELECTCOLUMNS(FILTER(UserRegions, UserRegions[Email] = CurrentUser), "Region", UserRegions[Region]), FALSE())`.

Use partial RLS only when summary data is intentionally shared while detail data is restricted. Create summary tables such as `SalesRevenueSummary = SUMMARIZECOLUMNS(Sales[OrderDate], "RevenueAllRegion", SUM(Sales[Revenue]))` and apply detail filters such as `Salesperson Filter = [EmailAddress] = USERNAME()` only to the restricted detail level.

Use time-based security only when business policy requires it, and keep cutoff logic auditable. A pattern such as `SWITCH(UserRole, "Executive", DATE(1900,1,1), "Manager", TODAY() - 365, "Analyst", TODAY() - 90, TODAY())` must be documented because access changes with time.

## Embedded Analytics Identities

Generate embed tokens with explicit identities. In C#, construct `EffectiveIdentity` with `username`, `roles`, `customData` when needed, and `datasets`. For static RLS, pass roles such as `new List<string>{ "MyRole" }`; for dynamic RLS, pass `customData: "SalesPersonA"` and a role such as `MyRoleWithCustomData`.

Use `GenerateTokenRequestV2` with `GenerateTokenRequestV2Report`, `GenerateTokenRequestV2Dataset`, `GenerateTokenRequestV2TargetWorkspace`, and `identities: new List<EffectiveIdentity> { rlsIdentity }`. Generate tokens through `pbiClient.EmbedToken.GenerateToken(tokenRequest)` and return only the embed token required by the client.

For multi-dataset and multi-tenant payloads, include `accessLevel: "View"`, `identities`, `username`, `roles`, `datasets`, `reports`, `allowEdit: false`, and `datasourceIdentities` when source identity binding is required. Keep `identityBlob`, `datasourceType`, `connectionDetails`, `server`, and `database` scoped to the tenant and report. Do not reuse a single `EffectiveIdentity` across tenants unless the datasets and roles are identical and approved.

## Database-Level and Fabric Security

Use database-level RLS as defense in depth for DirectQuery, Fabric Warehouse, or shared SQL sources. Create a dedicated `Security` schema, define predicate functions such as `Security.tvf_securitypredicate`, and apply a `CREATE SECURITY POLICY` with `ADD FILTER PREDICATE` and `WITH (STATE = ON)`.

| Source | Convention |
| --- | --- |
| SQL Server RLS | Use `CREATE FUNCTION Security.tvf_securitypredicate(@SalesRep AS nvarchar(50)) RETURNS TABLE WITH SCHEMABINDING AS RETURN SELECT 1 AS tvf_securitypredicate_result WHERE @SalesRep = USER_NAME() OR USER_NAME() = 'Manager';` then apply it to `sales.Orders`. |
| Fabric Warehouse RLS | Use `CREATE FUNCTION Security.tvf_securitypredicate(@UserName AS varchar(50)) RETURNS TABLE WITH SCHEMABINDING` and allow only `@UserName = USER_NAME()` or a controlled account such as `BatchProcess@contoso.com`. |
| Policy application | Use `CREATE SECURITY POLICY SalesFilter` or `YourSecurityPolicy` with `Security.tvf_securitypredicate(UserName_column)`. |

Database RLS does not replace Power BI model RLS. Use both when the storage layer can be queried outside the semantic model.

## Paginated Reports, Power Pages, and Tenant Boundaries

For paginated reports, pass `paginatedReportConfiguration` with `identities` and a specific `username`, for example `{"format": "PDF", "paginatedReportConfiguration": {"identities": [{"username": "john@contoso.com"}]}}`. Do not export paginated reports with a privileged service identity unless the output is already scoped for the target recipient.

For Power Pages, use a `powerbi` tag only with explicit `authentication_type:"powerbiembedded"`, `path`, and `roles`, such as `roles:"pagesuser"`. Preserve report paths like `https://app.powerbi.com/groups/00000000-0000-0000-0000-000000000000/reports/00000000-0000-0000-0000-000000000001/ReportSection` as configuration and do not hardcode production report IDs into reusable templates.

For multi-tenant security, keep dataset IDs, report IDs, workspace IDs, roles, datasource identities, and datasource connection details tenant-scoped. `YourUsername`, `YourRole`, `YourServerName.database.windows.net`, and `YourDataBaseName` are placeholders that must be replaced by validated tenant configuration.

## Validation, Monitoring, and Governance

Add security validation measures and governance scripts where they improve auditability.

| Area | Convention | APIs or identifiers to preserve |
| --- | --- | --- |
| Role validation | Create a `Security Test` measure that returns `PASS: Role applied correctly` or `FAIL: Incorrect role or multiple roles` based on `HASONEVALUE`, `VALUES`, and expected role logic. | `SecurityRoles[Role]`, `ExpectedRole`, `TestResult` |
| Data exposure audit | Compare `COUNTROWS(FactTable)` with `CALCULATE(COUNTROWS(FactTable), ALL(FactTable))` and report `AccessPercentage` with `DIVIDE` and `FORMAT`. | `FactTable`, `AccessibleRows`, `TotalRows` |
| Compliance measures | Track `Users with Data Access`, `High Privilege Users`, and `Security Violations` over `AuditLog` and `UserRoles`. | `AuditLog[AccessType]`, `AuditLog[EventType]`, `UserRoles[Email]` |
| Access analysis | Detect unusual activity with `AccessLog[Date]`, `AccessLog[AccessCount]`, `ALL(AccessLog[Username])`, and a threshold such as `AvgUserAccess * 3`. | `Unusual Access Pattern` |
| Breach detection | Flag repeated denied access with `AccessLog[AccessResult] = "Denied"` and a review threshold such as more than 10 denials per day. | `Potential Data Exposure` |
| Workspace governance | Use `Login-PowerBI`, `Get-PowerBIWorkspace`, `Get-PowerBIWorkspaceUser`, `Add-PowerBIWorkspaceUser`, `-AccessRight Member`, `-PrincipalType Group`, and `-Identifier $($SGObjectID)`. | `$SGObjectID`, `$pbiWorkspace` |

Security is layered. Combine authentication, authorization, RLS, database predicates, encryption, network controls, governance, and auditing rather than relying on a single model filter.

Keep governance placeholders explicit: `security-group-object-`, `workspace-name`, `UserPrincipalName`, `fff1a505-xxxx-xxxx-xxxx-e69f81e5b974`, and `10ce71df-xxxx-xxxx-xxxx-814a916b700d` are illustrative values that must be replaced by real tenant configuration.

## Preserved DAX, SQL, and Embedded API Vocabulary

The following names carry security semantics in common Power BI RLS examples and should survive refactors.

| Category | Identifiers |
| --- | --- |
| DAX functions | `AVERAGE`, `CONTAINS`, `DISTINCTCOUNT`, `HOUR`, `WEEKDAY` |
| Security tables and columns | `DimSalesTerritory`, `SalesTerritory`, `SalesTerritoryKey`, `UserSecurity`, `UserTerritories`, `AllowedTerritories`, `UserDepartments`, `SpecialUsers` |
| Validation variables and values | `CurrentUsername`, `TestRole`, `AllowedRoles`, `CutoffDate`, `UserAccessCount`, `UnexpectedAccess`, `DataAccess`, `SecurityViolation` |
| Embedded C# APIs | `GetEmbedToken`, `Guid.Empty`, `ToString`, `ToList`, `CountryDynamic` |
| SQL and warnings | `SCHEMA`, `AVOID`, `user-based` |

## Good / Bad Examples

The examples below illustrate secure default-deny RLS.

**Good:**

```dax
Default Security =
VAR UserPermissions =
    FILTER(UserAccess, UserAccess[Email] = USERNAME())
RETURN
    IF(
        COUNTROWS(UserPermissions) > 0,
        [Territory] IN SELECTCOLUMNS(UserPermissions, "Territory", UserAccess[Territory]),
        FALSE()
    )
```

Why: The predicate grants access only when an explicit permission row exists and denies all unexpected users.

**Bad:**

```dax
Bad Security Filter =
IF(
    USERNAME() = "SpecificUser",
    [Type] = "Internal",
    TRUE()
)
```

Why: The fallback `TRUE()` grants full access to every unexpected user, which reverses least privilege.

## Conventions

| Rule | Rationale |
| --- | --- |
| End RLS predicates with `FALSE()` for unexpected users, roles, and custom data. | Default deny prevents accidental exposure when identity data is incomplete. |
| Use `USERNAME()`, `CUSTOMDATA()`, `LOOKUPVALUE`, `FILTER`, `SELECTCOLUMNS`, and `IN` intentionally. | Security logic remains tied to auditable identity and permission tables. |
| Keep hierarchical and time-based security data-driven and documented. | Reviewers can verify manager, region, and cutoff rules without reverse-engineering DAX. |
| Pass `EffectiveIdentity` with explicit `username`, `roles`, `datasets`, and `customData` where needed. | Embedded tokens apply the intended RLS role and dataset scope. |
| Use database RLS through `Security.tvf_securitypredicate` and `CREATE SECURITY POLICY` when the source can enforce it. | Storage-layer controls reduce exposure if Power BI is bypassed. |
| Keep tenant IDs, dataset IDs, report IDs, datasource identities, and connection details tenant-scoped. | Multi-tenant embed tokens cannot leak access across customers. |
| Add validation measures and workspace audits for privileged or regulated reports. | Security behavior is observable after publication. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Model RLS as explicit allow rules. | Use permissive fallback `TRUE()` branches. |
| Use dynamic security tables for user-to-territory, user-to-role, and user-to-region mappings. | Hardcode long lists of users directly in DAX filters. |
| Use `customData` only for controlled embedded values. | Treat arbitrary client-provided custom data as trusted authorization. |
| Use `allowEdit: false` for viewer embed scenarios. | Generate broad edit-capable tokens for consumers who only view reports. |
| Apply SQL Server or Fabric Warehouse RLS where source-level enforcement is available. | Assume semantic-model RLS protects direct database access. |
| Monitor workspace users and high-privilege roles with PowerShell and audit measures. | Let access drift without review. |
| Keep Power Pages `powerbi` embeds role-scoped. | Embed reports without explicit roles or authentication type. |

## Checklist Before Opening a PR

- [ ] Every RLS predicate has explicit allow conditions and a default-deny `FALSE()` path.
- [ ] Dynamic RLS uses governed user, role, region, territory, or custom-data tables.
- [ ] Hierarchical, partial, and time-based security rules are documented and auditable.
- [ ] Embedded analytics code passes the correct `EffectiveIdentity`, roles, datasets, reports, workspaces, and datasource identities.
- [ ] Multi-tenant payloads keep tenant-specific datasets, reports, datasource connections, and identity blobs isolated.
- [ ] SQL Server or Fabric Warehouse RLS is used where storage-layer enforcement is required.
- [ ] Paginated report and Power Pages embeds include explicit identity, authentication type, path, and roles.
- [ ] Security validation measures or tests verify expected roles and visible row counts.
- [ ] Governance scripts review workspace users, groups, high-privilege roles, and access anomalies.
- [ ] No placeholder such as `YourUsername`, `YourRole`, `YourServerName.database.windows.net`, or `YourDataBaseName` remains in production configuration.

## References

- Power Pages Power BI embedded path example: https://app.powerbi.com/groups/00000000-0000-0000-0000-000000000000/reports/00000000-0000-0000-0000-000000000001/ReportSection
