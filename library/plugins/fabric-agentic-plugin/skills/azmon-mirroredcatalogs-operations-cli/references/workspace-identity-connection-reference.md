# Workspace identity connection reference (Mode B option)

Agent guidance for the Stage 5 **Mode B — Workspace identity** sub-branch. Load
this only when the user chooses to authenticate the Azure Monitor connection with
the Fabric workspace identity. Do not paste verbatim to users; never expose
tokens, secrets, or auth headers.

Uses the Fabric **workspace identity** — an automatically-managed service
principal with no secret — as the connection credential. Strictly a Mode B (User
flow) option; never mix into Mode A (Service Principal) logic.

## Feasibility (verify first)

Workspace-identity connection authentication is documented for OneLake shortcuts,
pipelines, semantic models, and Dataflows Gen2; it is NOT documented for the Azure
Monitor connector. Before proceeding, confirm `WorkspaceIdentity` appears in the
Azure Monitor entry's `supportedCredentialTypes` from
`GET https://api.fabric.microsoft.com/v1/connections/supportedConnectionTypes?showAllCreationMethods=true`.
If absent, tell the user this option isn't available for this connector and offer
interactive OAuth instead — do not attempt it.

## Sequence (each Fabric-modifying step is confirmation-gated)

1. **Detect the identity.** `GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}`
   → if `workspaceIdentity` exists, reuse it (capture `applicationId` +
   `servicePrincipalId`). Identity name = workspace name. Do not re-provision.
2. **Provision if absent (confirmation-gated).** Caller must have the workspace
   **Admin** role and delegated `Workspace.ReadWrite.All`. On confirmation:
   `POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/provisionIdentity`.
   `200` returns `{ applicationId, servicePrincipalId }`; `202` is a long-running
   operation — poll the `Location` / operation id to completion before proceeding.
   Never claim success before the LRO completes.
3. **Show the identity details** to the user (non-secret): identity name,
   `applicationId`, `servicePrincipalId`.
4. **Ensure the identity has a role that lets the connection read the Log
   Analytics workspace (assign it if you can, else instruct).**
   a. **Check** the SP's current assignments at the LA workspace scope:
      `az role assignment list --assignee <servicePrincipalId> --scope <laResourceId> --query "[].roleDefinitionName" -o json`.
      An **Owner** at the LA workspace scope is required → skip to step 5 if
      already present.
   b. **If Owner is missing, determine the caller's permission** to create role
      assignments at that scope (needs
      `Microsoft.Authorization/roleAssignments/write` — i.e. **Owner** or **User
      Access Administrator** on the LA workspace / RG / subscription).
   c. **If the caller is permitted → assign it (confirmation-gated).** On
      confirmation, run (verified working):
      `az role assignment create --assignee <servicePrincipalId> --role "Owner" --scope <laResourceId>`,
      then re-run the list in (a) to confirm. `<laResourceId>` is the LA workspace
      ARM id
      (`/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.OperationalInsights/workspaces/<ws>`).
   d. **If the caller is NOT permitted (or the create fails with an authorization
      error) → do not force it.** Fall back to guidance: give the user the exact
      command above (or portal steps) for an Owner / User Access Administrator to
      run, then STOP and WAIT for them to confirm.
5. **Create the connection (confirmation-gated).** After the role is in place,
   create the Azure Monitor connection for the **same** LA workspace using
   the documented Create Connection payload (see
   [azmon-fabric-api-reference.md](azmon-fabric-api-reference.md) → "Connection API
   shapes") with `credentialDetails.credentials.credentialType = "WorkspaceIdentity"`,
   and the `type` / `creationMethod` / `parameters` read from
   `supportedConnectionTypes` (never guessed). No secret is supplied. Reuse a
   matching existing workspace-identity connection instead of duplicating. Then
   continue to Stage 6. If the connection test fails because the role hasn't
   propagated, wait and retry — do not assume a wrong role.

## Required permissions summary

- Provision workspace identity: workspace **Admin** + delegated
  `Workspace.ReadWrite.All`.
- Assign the LA role: the **Skill** performs it (confirmation-gated) when the
  caller holds `Microsoft.Authorization/roleAssignments/write` on the LA scope
  (**Owner** or **User Access Administrator**); otherwise the Skill instructs the
  user / an admin to run the assignment and waits. The workspace identity needs
  **Owner** on the LA workspace scope.
