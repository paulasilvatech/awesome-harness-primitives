# Fabric Workspace Discovery & Capability Resolution Policy

Loaded on demand from `skills/azmon-mirroredcatalogs-operations-cli/SKILL.md`
at Stage 3. This is REQUIRED policy — read it before declaring Stage 3 blocked.

## Discovery and resolution order (REQUIRED)

Fabric workspaces are **not** Azure Resource Manager resources, so absence of an
automatic enumeration path does NOT mean no Fabric workspace exists. Before
declaring Stage 3 blocked, the Skill MUST work through this policy in order and
MUST NOT terminate the workflow early.

1. **Discover** all available Fabric workspace discovery mechanisms in the
   current environment, in order, before asking the user to hand-provide a
   workspace:
   - Fabric REST APIs, if surfaced.
   - Fabric Actions, if surfaced.
   - Fabric / OneLake / Power BI execution capabilities, if surfaced.
   - Authenticated Fabric REST **read-only** discovery via `az rest --method get`
     against `https://api.fabric.microsoft.com/...`, if Azure CLI execution is
     available and permitted under the read-only Fabric REST discovery exception
     (GET-only, no modifications, no secret/token/header exposure, capability
     path stated).
   - Any other documented capability provider available to the agent
     environment.

   If workspace discovery succeeds, list the candidate workspaces, do NOT
   auto-select, and ask the user to choose or confirm. Only if no supported
   Fabric REST read-only discovery path is available, proceed to ask the user for
   the workspace information below.

2. **Interpret** the result of discovery. Automatic enumeration being
   unavailable means one of two things — the Skill MUST distinguish them:
   - No Fabric control-plane capability is available in this agent environment,
     OR
   - Automatic workspace enumeration is unavailable, but the workflow can still
     continue using **user-provided** workspace information.

3. **Do not terminate** if automatic discovery fails or no Fabric control-plane
   capability is detected. Never assume Fabric workspaces do not exist just
   because automatic discovery failed.

4. **Ask the user** for workspace information. Explain the missing capability in
   plain terms, then request **one** of:
   - Fabric Workspace Name
   - Fabric Workspace ID
   - Fabric Workspace URL

5. **Validate** any user-provided workspace as much as the available
   tools/capabilities allow (e.g. confirm the id/name/URL resolves, or that the
   caller can access it). Continue the workflow only when it is safe to do so.
   Never fabricate a workspace, workspace id, or validation result, and never
   claim a Fabric action succeeded when the required execution capability is
   unavailable.

6. **Block only as a last resort.** Mark Stage 3 as BLOCKED only after ALL
   supported discovery mechanisms AND all user-supplied resolution paths
   (Name / ID / URL) have been exhausted.

UI-guided instructions for Fabric workspace selection are permitted ONLY as the
final fallback, after every programmatic discovery path and every user-supplied
resolution path above has failed. This is distinct from the general Portal
Guidance Policy and does not relax any other stage's portal boundary.
