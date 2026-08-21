---
name: azmon-mirroredcatalogs-operations-cli
description: "Onboard Azure Monitor / Application Insights observability data into Microsoft Fabric and guide business-impact insights by correlating telemetry with business data, Eventhouse external delta tables, verified schemas, an optional Real-Time (KQL) dashboard, and opt-in Operations Agent instructions. Triggers: onboard Azure Monitor into Fabric, correlate App Insights telemetry with business data, build a Real-Time KQL dashboard over telemetry, build an Operations Agent for business-impact alerting, determine if availability or latency impacted bookings orders or revenue, connect a Log Analytics workspace to Fabric."
---

> **Telemetry — MANDATORY.** Every `api.fabric.microsoft.com` call must carry
> `x-ms-fabric-skill: azmon-mirroredcatalogs-operations-cli` (`az rest`: `--headers "x-ms-fabric-skill=azmon-mirroredcatalogs-operations-cli"`),
> including every LRO poll, `fabric_lro` and retry. Snippets omit it — add it anyway.

# azmon-mirroredcatalogs-operations-cli

Guide a user end-to-end to (1) onboard Azure Monitor / Application Insights /
Log Analytics observability data into Microsoft Fabric as a Mirrored Catalog
(AzMon) item, and (2) turn that telemetry into **business-impact insights** by
correlating observability signals with business data (bookings, orders,
customers, flights, payments, revenue, tenants, accounts, subscriptions, usage
KPIs, SLA/availability KPIs), ending in ready-to-paste **Operations Agent**
instructions.

This is a **self-contained Skills-for-Fabric package**. It does **not** depend on
any MCP server or tool controller as the execution mechanism. Product/API
knowledge, supported flows, guardrails, and modeling rules live in this file and
in `references/*.md`.

## Prerequisite Knowledge

Before running this skill, read the shared common guidance:

- [Authentication & token acquisition](../../common/COMMON-CORE.md#authentication--token-acquisition)
- [Authentication recipes](../../common/COMMON-CLI.md#authentication-recipes)

## Trigger phrases

- onboard Azure Monitor data into Fabric
- create Azure Monitor item in Fabric
- connect Application Insights to Fabric
- correlate App Insights telemetry with business data
- onboard my LA workspace to Fabric
- onboard Log Analytics workspace to Fabric
- connect Log Analytics workspace to Fabric
- understand if service availability impacted bookings
- understand if latency impacted conversion
- correlate exceptions with revenue or orders
- build Operations Agent for Azure Monitor business impact
- create business impact insights from Log Analytics data

## When to use this skill (and related skills)

`azmon-mirroredcatalogs-operations-cli` is for onboarding Azure Monitor /
Application Insights / Log Analytics telemetry into Microsoft Fabric
(mirroredCatalogs endpoint), correlating that telemetry with business data, and
generating Operations Agent instructions. For general Eventhouse / KQL querying
unrelated to Azure Monitor onboarding, use `eventhouse-cli` consumption mode;
for authoring Eventhouse items and databases, use its authoring mode.

## Reference index

Read these when the corresponding stage needs product/API detail. Do not paste
them wholesale into user responses — they are guidance for you, the agent.

| Reference | Use it for |
|-----------|-----------|
| [references/azmon-fabric-api-reference.md](references/azmon-fabric-api-reference.md) | Supported vs UI-only flows; connector modes; Fabric item/agent surfaces |
| [references/workspace-identity-connection-reference.md](references/workspace-identity-connection-reference.md) | Mode B workspace-identity connection: provision/detect identity, user-granted LA RBAC, WorkspaceIdentity connection |
| [references/workspace-discovery-policy-reference.md](references/workspace-discovery-policy-reference.md) | Stage 3 Fabric workspace discovery order, interpretation, user-supplied resolution, block-as-last-resort |
| [references/oauth-connection-reference.md](references/oauth-connection-reference.md) | Mode B OAuth connection: read-only detection order, reuse rules, UI-guided creation steps |
| [references/mirrored-catalog-reference.md](references/mirrored-catalog-reference.md) | Mirrored Catalog item CRUD, definition, discovery, monitoring, refresh |
| [references/eventhouse-shortcuts-reference.md](references/eventhouse-shortcuts-reference.md) | Eventhouse/KQL, OneLake shortcuts, queryability requirement |
| [references/operations-agent-reference.md](references/operations-agent-reference.md) | Operations Agent instruction template, validation, troubleshooting |
| [references/telemetry-table-reference.md](references/telemetry-table-reference.md) | App Insights / OpenTelemetry / custom security telemetry tables and business meaning |
| [references/app-insights-dynamic-fields-reference.md](references/app-insights-dynamic-fields-reference.md) | Dynamic fields (Properties/CustomDimensions) and hidden business keys |
| [references/dashboard-reference.md](references/dashboard-reference.md) | Real-Time (KQL) Dashboard create/update mechanics; generic tile patterns |
| [references/business-analysis-workflow.md](references/business-analysis-workflow.md) | Full detail for the business-analysis half — Stages 13–17 (incl. correlation patterns & modeling appendices); load at the Stage 12 handoff |

## Secrecy & scope guardrails

- Do NOT expose Azure Log Analytics backend APIs to the user.
- Do NOT expose Fabric / DMTS / Gateway connection internals or internal
  endpoints to the user.
- Do NOT request or disclose tokens, OAuth redirect codes, OAuth nonce values,
  cookies, secrets, or internal implementation details.
- Do NOT mention MCP, MCP servers, or MCP connectivity/troubleshooting anywhere
  in the user-facing flow. This Skill is self-contained.
- Do NOT present undocumented / browser-inspected / internal connector APIs as
  supported public APIs.
- Do NOT claim OAuth Azure Monitor connector creation is available through a
  public API — OAuth connector creation is **UI-guided only**.
- Do NOT fabricate workspace names, table names, schema, item IDs, connection
  IDs, or query results. Use only values returned by real discovery/queries; use
  clearly-labelled placeholders otherwise.
- Do NOT ask the user for JOIN logic, KQL, bins, or thresholds upfront.
- If the request is about SQL / Data Warehouse or Lakehouse ingestion, warehouse
  performance, or general Fabric DW best practices **unrelated** to Azure Monitor /
  Application Insights / Log Analytics onboarding, state that it is **out of scope**
  for this Azure Monitor skill and point the user to the appropriate warehouse
  skill; do NOT act on it, run queries, or create resources.

### Domain-agnostic rule

Business entities named anywhere in this Skill or its references — bookings,
orders, customers, flights, revenue, tenants, payments, and similar — are
**EXAMPLES ONLY**. The Skill MUST NOT infer the user's business domain from these
examples. The user's actual business entities MUST be discovered from real Fabric
data (Eventhouse / KQL database / Warehouse / Lakehouse / shortcuts) and confirmed
with the user before use.

To be explicit:

- **Examples are illustrative only.** Every business-entity name in this Skill
  and its references (e.g. bookings, orders, customers, revenue, flights,
  tenants, payments) is a non-normative illustration, not a required or expected
  entity.
- **The Skill is domain-agnostic.** It applies to any business domain and assumes
  none.
- **The Skill MUST NOT infer or assume the user's business domain** from the
  illustrative examples, from table or column names that happen to resemble an
  example, or from any prior context.
- **Business entities MUST be discovered from the user's actual data** and, until
  discovered and confirmed, MUST be referred to generically — as *business
  entities*, *business datasets*, *business KPIs*, or *business outcomes* — rather
  than by any assumed domain-specific name.

## EXECUTION CAPABILITY POLICY

The Skill is a guided staged workflow.

Actual execution depends on capabilities available in the current environment.

Portal-guided instructions are allowed ONLY for OAuth Azure Monitor connector creation.

The Skill MUST NOT switch the entire onboarding flow to portal-guided instructions as a generic fallback.

For all non-OAuth stages, the Skill MUST first attempt to discover whether a supported execution path exists in the current environment.

Supported execution paths may include:

- Fabric REST APIs
- Azure REST APIs
- Fabric Actions
- Azure CLI
- Azure Resource Graph
- Fabric REST **read-only** discovery via authenticated `az rest --method get`
  against `https://api.fabric.microsoft.com/...` (discovery/read-only only)
- Other documented supported capabilities available to the agent

**Log Analytics REST API reference (agent-facing).** When the Skill needs to perform or validate Azure Log Analytics operations, it may consult the official [Log Analytics REST APIs](https://learn.microsoft.com/en-us/rest/api/loganalytics/) reference to identify supported Log Analytics management, workspace, table, ingestion, and query APIs. This is agent-facing guidance only and does not relax the secrecy rule above.

These execution paths are distinct and MUST NOT be conflated:

1. **Kusto / KQL data-plane execution** — telemetry queries; optional, and MUST
   NOT be used when disabled.
2. **Azure ARM control-plane discovery** — resource/metadata enumeration.
3. **Fabric REST control-plane discovery** — a surfaced Fabric REST / Fabric
   Actions capability.
4. **Arbitrary shell / CLI execution** — out of scope (see Out-of-scope
   constraints).
5. **Fabric REST read-only discovery via authenticated `az rest --method get`** —
   a narrow, permitted exception used ONLY for Fabric discovery/read against
   `https://api.fabric.microsoft.com/...`. It is GET-only, never creates,
   updates, deletes, or modifies anything, and never exposes tokens, secrets,
   auth headers, or sensitive payloads. This is NOT general shell/CLI access.

MCP unavailability alone does NOT mean execution capability is unavailable.

Unavailability of any single execution path does NOT automatically imply the
capability is unavailable. Before declaring a capability unavailable, the Skill
MUST evaluate ALL supported execution paths listed above and confirm that none is
available. Capability unavailable may be reported only after every supported
execution path has been evaluated.

If no supported execution path exists, the Skill MUST:

1. Stop.
2. Identify the missing capability.
3. Explain why it is required.
4. Identify which stage is blocked.
5. Wait for user confirmation.

The Skill MUST NOT:

- Replace validation with portal guidance.
- Replace Mirrored Catalog creation with portal guidance.
- Replace discovery, monitoring, refresh, shortcut creation, schema verification, or Operations Agent creation with portal guidance.
- Claim an action completed when execution capability is unavailable.


## PORTAL GUIDANCE POLICY

The Skill SHOULD prefer automated execution paths over UI-guided instructions:

- Fabric REST APIs
- Azure REST APIs
- Fabric Actions
- Azure CLI
- Other supported automation mechanisms

Before providing UI-guided instructions the Skill MUST:

1. Evaluate the available execution paths.
2. Attempt supported execution paths where available.
3. Explain which execution paths were evaluated.
4. Explain why they cannot be used.

Only after those steps may the Skill provide UI-guided guidance.

OAuth Azure Monitor connector creation remains an explicitly supported UI-guided
scenario and does not require the above evaluation.


## STRICT STAGED WORKFLOW CONTROLLER (ENFORCED)

The Skill MUST operate as a strict staged workflow controller.

### Stages

1. Intent and scope
2. Log Analytics workspace selection
3. Fabric workspace selection
4. Identity selection and validation
5. Connection resolution
6. AzMon / Mirrored Catalog item creation or reuse
7. **Business Insight Capture** (optional here; may be deferred — intent MUST be
   captured/confirmed before schema verification, Stage 12)
8. Azure Monitor table discovery
9. Eventhouse / KQL database **target** selection (default auto endpoint vs a
   specific/new Eventhouse)
10. External Delta table registration planning
11. External Delta table registration
12. Schema and data verification
13. Business data discovery and scoring
14. Correlation planning
15. Optional dashboard suggestion and creation
16. Operations Agent instruction generation (optional — gated: only if the user
    wants an agent)
17. Optional Operations Agent creation / validation

### Execution rules

- The Skill MUST track and enforce the current stage.
- The Skill MUST NOT skip stages.
- The Skill MUST NOT move to the next stage without completing the current one.

### Stage visibility (REQUIRED in every user-facing response)

Begin every response with this structure, written as **normal chat text (not a
code block)**:

- **Current stage:** <stage name>
- **What I found:** <short summary>
- **Next step:** <one clear action>

Then close with a line inviting the user to confirm before continuing (e.g.
*“Waiting for your confirmation to continue.”*).

If the current stage is unclear → **STOP** and ask the user where to resume.

### Hard stop behavior

After presenting any step that requires confirmation:

- **STOP.**
- **WAIT** for explicit user confirmation.
- Do **not** continue automatically.

### Confirmation gates (explicit confirmation REQUIRED before)

- Selecting the identity for the flow (Stage 4) — recommend Service Principal,
  but WAIT for the user's choice before validating.
- Creating or reusing any resource that modifies Fabric.
- Provisioning the Fabric workspace identity and assigning its Log Analytics
  role (Stage 5, Mode B workspace-identity option) — WAIT before each write.
- Selecting the Eventhouse target (a specific existing Eventhouse, or a new one).
- Creating shortcuts in the chosen / new Eventhouse — explicitly show the target
  Eventhouse and exactly what will be created.
- Proceeding from schema verification (Stage 12) to correlation planning
  (Stage 14).
- Creating or modifying a dashboard (present suggestions and WAIT for approval
  first).
- Building an Operations Agent at all (Stage 16) — explicitly ask whether the
  user wants an agent before generating any instructions. If they do not, skip
  Stages 16–17; the flow may end after the dashboard.
- Generating final Operations Agent instructions if the correlation model has
  not been confirmed.
- Creating or modifying an Operations Agent.

### Stage guardrails

- External Delta table registration planning (Stage 10) MUST occur before schema verification or join
  logic. If schema/join is attempted early → STOP and return to Stage 10.
- External Delta table registration (Stage 11) MUST complete before schema verification.
- Schema verification (Stage 12) MUST complete before correlation planning
  (Stage 14).
- If data is not queryable in Eventhouse via the registered external delta tables
  → STOP → return to Stage 10/11.
- Correlation planning MUST NOT begin until external-table queryability is
  confirmed.
- Business Insight Capture (Stage 7) MAY be answered early or **deferred** so the
  user can explore their data first, but intent MUST be captured/confirmed
  (intent provided OR a suggested direction explicitly selected) **before schema
  verification (Stage 12)** and correlation planning. Never assume intent.

### Out-of-scope constraints

The Skill MUST NOT run arbitrary shell/CLI/az/PowerShell commands, perform network
debugging, investigate server connectivity, or execute infrastructure
troubleshooting. These are out of scope unless explicitly part of the current
stage.

**Narrow exception — Fabric REST read-only discovery.** The Skill MAY use an
authenticated `az rest --method get` call ONLY for Fabric REST read-only
discovery, and ONLY when ALL of the following hold:

- The endpoint is `https://api.fabric.microsoft.com/...`.
- The HTTP method is **GET** only.
- The operation is discovery / read-only only.
- Nothing is created, updated, deleted, or modified (no Fabric items, shortcuts,
  mirrored catalog items, or connectors via CLI).
- No tokens, secrets, raw auth headers, or sensitive payloads are exposed.
- The Skill clearly states the capability path used.

This exception does NOT permit arbitrary shell/CLI execution, non-GET `az rest`
calls, or use of the Kusto / KQL data-plane when disabled.

**Narrow exception — Fabric workspace-identity provisioning + LA role assignment
(Mode B only).** In the Mode B workspace-identity option, the Skill MAY use
authenticated `az` calls to detect/provision the workspace identity and, when the
caller is permitted, assign its Log Analytics role, limited to:

- `GET https://api.fabric.microsoft.com/v1/workspaces/{id}` (detect), and
- `POST https://api.fabric.microsoft.com/v1/workspaces/{id}/provisionIdentity`
  (provision) plus GET polling of its long-running operation, and
- `az role assignment list` (check) and `az role assignment create` at the Log
  Analytics workspace scope to grant the identity **Owner**, but ONLY when the
  caller holds `Microsoft.Authorization/roleAssignments/write` there.

Each write is confirmation-gated (Stage 5), touches only the workspace identity
and its LA role (nothing else), exposes no tokens/secrets/auth headers, and
the Skill states the capability path used. If the caller lacks role-assignment
permission, the Skill MUST NOT force it — it instructs the user / an admin to run
the assignment instead. This does NOT permit any other non-GET `az rest` calls or
any broader `az` usage.

### Response style (ENFORCED)

Behave like a **guided product experience**, not a backend debugger.

- Use concise, business-friendly language.
- Never show internal implementation steps (CLI, REST, tokens, API calls) unless
  the user explicitly asks and the API is documented/supported.
- Never expose internal limitations ("public API limitation", "CredentialType
  not supported", "headless OAuth failure") in user-facing output.
- Never ask for secrets, OAuth codes, cookies, redirect URLs, tokens, or nonce
  values.
- Summarize findings. Do NOT expose endpoint experimentation, API probing,
  OpenAPI / schema exploration, retry investigations, or low-level debugging
  details in user-facing output unless the user explicitly asks for them.
- After each stage: present a short summary, ask for explicit confirmation,
  STOP and WAIT.

---

## Stage 1 — Intent and scope

Confirm what the user wants: onboard observability data into Fabric, explore a
business insight, or both. Capture (in plain language) any workspace names or
business outcome they already mention — but do not yet drive correlation.

## Stage 2 — Log Analytics workspace selection

Application Insights telemetry is queried through its backing Log Analytics
workspace (workspace-based Application Insights). Help the user pick the correct
Log Analytics / Application Insights-backed workspace.

- If the user did not provide a workspace, ask for the subscription, then present
  a concise list of supported workspaces (name + resource group + location).
  Never expose raw API responses.
- Prefer a case-insensitive name filter over listing everything when the
  subscription has many workspaces.

### Exact-name-not-found fallback (REQUIRED)

When the user names a workspace and no **exact** match exists, the Skill MUST NOT
fail. Instead:

1. Ask for the subscription if not provided (do not guess).
2. Offer similar workspaces (names that **contain** the term or are a close
   case-insensitive/partial match). Broaden the search if a narrow filter returns
   nothing.
3. Present candidates as a concise numbered list (name + resource group +
   location), then STOP and wait for the user to pick.
4. If exactly one similar workspace is found, still confirm before proceeding.
5. If none is found, say so plainly and ask for a different subscription or term.

Never fabricate a workspace name or GUID — only offer real discovered
workspaces.

## Stage 3 — Fabric workspace selection

Help the user choose the target Fabric workspace (display name + id). Use a
case-insensitive substring filter when helpful. Read-only; nothing is created
here. Never expose raw API responses or tokens.

### Fabric Workspace Discovery & Capability Resolution Policy (REQUIRED)

Fabric workspaces are **not** Azure Resource Manager resources, so absence of an
automatic enumeration path does NOT mean no Fabric workspace exists. **Never
terminate the workflow early**: if automatic discovery fails, ask the user for a
Fabric Workspace **Name**, **ID**, or **URL**, validate it as far as the available
capabilities allow, and continue. Never auto-select a workspace, never fabricate a
workspace or a validation result, and mark Stage 3 BLOCKED only after every
discovery mechanism AND every user-supplied resolution path has been exhausted.

Follow the full discovery order, the interpretation rules, and the UI-guided
last-resort boundary in
[references/workspace-discovery-policy-reference.md](references/workspace-discovery-policy-reference.md).

## Stage 4 — Identity selection and validation

### Identity selection (REQUIRED first — WAIT for the user)

Validation MUST run against the **identity that will actually perform the flow**,
so the identity is chosen **before** any validation check — not deferred to
Stage 5. Do NOT silently reuse whatever `az` happens to be signed in as.

Present the choice and STOP — ask this as **normal chat text (a plain numbered
list, not a code block)**:

Which identity should I use for this onboarding?

1. **Service Principal (recommended)** — automated, non-interactive; best for
   repeatable runs and CI. Requires tenant id, app/client id, and a securely
   provided secret/certificate.
2. **Your user account (interactive sign-in)** — if you prefer to run as
   yourself, or a Service Principal is not available.

Invite the user to reply **1** or **2**; note that Service Principal is
recommended.

- **Recommend Service Principal**, but let the user choose. If the user asks to
  sign in as themselves, allow interactive user login and continue as the user.
- After the choice, confirm the effective identity (e.g. `az account show`) so
  validation runs against the right principal. If it does not match the chosen
  identity, stop and resolve the sign-in before validating.
- Carry the chosen identity forward: Stage 5 connection resolution and all later
  Fabric-modifying actions use this same identity.

### Validate against the chosen identity

Before any creation, verify **for that identity**:

- The workspace exists.
- The **chosen identity** has the required Log Analytics access.
- The **chosen identity** has sufficient Fabric workspace permission to operate
  (and, for a Service Principal, that the tenant setting *"Service principals can
  use Fabric APIs"* is enabled).
- Surface early that connection detection/reuse will later need the chosen
  identity to hold **a role** on the Azure Monitor connection (a **User** role is
  enough; **Owner** is not required), so a permission gap is caught here rather
  than at Stage 5.
- For the Mode B **workspace-identity** connection option (Stage 5), the chosen
  identity must be a workspace **Admin** (required to provision the workspace
  identity). The Skill can assign the identity's Log Analytics role itself
  when the caller holds role-assignment permission (**Owner** / **User Access
  Administrator**) on the LA scope; otherwise it instructs the user. Surface both
  early.

If validation fails, summarize which checks passed/failed in user terms, explain
the missing capability, and offer to try another workspace, grant the missing
permission, or switch identity. See
`references/azmon-fabric-api-reference.md` for supported-scope rules.

### Validation capability discovery (REQUIRED)

Before declaring validation capability unavailable, the Skill MUST determine whether the environment provides one of the following:

- Fabric REST APIs
- Azure REST APIs
- Fabric Actions
- Azure CLI
- Azure Resource Graph

MCP availability is only one possible execution path.

The Skill MUST report validation capability unavailable only after evaluating all supported execution paths and finding none.

Before declaring validation capability unavailable, the Skill MUST:

1. Determine whether another supported execution path exists.
2. Attempt capability discovery using all supported mechanisms available
   in the current environment.
3. Only after all supported mechanisms have been evaluated and none are
   available may the Skill declare the capability unavailable.

## Stage 5 — Connection resolution

Two connection modes are supported. **Prefer Service Principal (Mode A)** — the
automated, non-interactive path — as the default. Fall back to **OAuth (Mode B)**
only when Service Principal is unavailable or the user explicitly requests it.
Keep the two modes **separate**. Never route OAuth through Service Principal
logic, and never route Service Principal through OAuth / interactive sign-in
logic. See
[references/azmon-fabric-api-reference.md](references/azmon-fabric-api-reference.md)
for the authoritative connector rules **and the exact documented connection API
endpoints and payload shapes** (List / Get / Create Connection + List Supported
Connection Types). Use those documented shapes — do **not** guess a connection
payload or go searching general docs. When the Azure Monitor connector's exact
`type` / `creationMethod` / `parameters` are unknown, resolve them from the
`supportedConnectionTypes` endpoint rather than assuming.

### Mode selection (REQUIRED order)

The identity was already chosen and validated in **Stage 4 (Identity selection)**.
Use that identity here — do not re-prompt unless the user changes it. Map the
chosen identity to its connection mode:

1. **Service Principal → Mode A.** If a matching Service Principal connector
   already exists for the same Log Analytics workspace, reuse it. Otherwise, when
   the required Service Principal inputs are available (tenant id, app/client id,
   and a securely-provided secret/certificate reference), create-or-reuse the
   Service Principal connector automatically — no UI step.
2. **User / interactive → Mode B.** Use when the user chose to sign in as
   themselves, the Service Principal is unavailable, or the tenant disallows it.
   In Mode B, first prompt the user to choose the connection authentication method
   — interactive OAuth or workspace identity (see "Mode B — choose connection
   authentication" below) — then route to that sub-branch.

### Connection visibility caveat (applies to BOTH modes)

To be **discoverable**, a connection must have **at least one role assigned to the
calling identity** — whether the **Service Principal** (Mode A) or the **user**
(Mode B). Any assigned role makes it appear in the listing and reusable; a
**User** role is enough for detection and reuse, and **Owner** is only needed to
**manage / modify / delete** it. If the caller holds **no role** on a connection,
the API will **not** return it — that is **by design**, not a failure.

Therefore, if the search finds **no** matching connection, the Skill MUST NOT
immediately conclude the connection does not exist. It MUST first consider that
the connection may exist but simply be **invisible to the current identity
because it holds no role on it**, and:

- State that a matching connection was not found **for the current identity**,
  and that this can mean either (a) no such connection exists, or (b) one exists
  but the calling Service Principal / user holds **no role** on it.
- Advise assigning the Service Principal or user **a role** on the existing Azure
  Monitor connection (for the same Log Analytics workspace) — a **User** role is
  enough for detection and reuse — then re-run detection. (If a Service Principal
  still can't see it after a lower role is granted, see the Service Principal note
  in
  [references/azmon-fabric-api-reference.md](references/azmon-fabric-api-reference.md).)
- Only after this permission possibility has been surfaced may the Skill proceed
  to create a new connector (Mode A) or the OAuth create-once guidance (Mode B).

Never fabricate a connection or claim one exists without a real listing match.

### Portal guidance boundary

Portal-guided instructions are permitted ONLY for OAuth Azure Monitor connector creation.

Portal guidance is NOT an allowed fallback for:

- LAW validation
- Fabric workspace validation
- Connection detection
- Connection reuse
- Service Principal connector creation
- Mirrored Catalog item creation
- Discovery
- Monitoring
- Refresh
- Eventhouse shortcut creation
- Schema verification
- Operations Agent creation

If execution capability for these actions is unavailable, the Skill MUST stop and identify the missing capability.

### Mode A — Service Principal (automated create-or-reuse, default)

Present this as **"connect using Service Principal"** — the automated,
non-interactive path (no user login, no UI step). This is the **preferred**
default; attempt it before OAuth.

- **Idempotent create-or-reuse**: if a matching Azure Monitor Service Principal
  connector already exists for the same Log Analytics workspace (same data source
  path + Service Principal credential type), reuse it — never create a duplicate.
- Only **one** connector is created per run.
- **Never** reuse a non-Service-Principal (e.g. OAuth) connector in this mode.
- **Never** ask the user to paste a client secret into chat. Secrets come from
  **environment variables or Key Vault references** only, are never echoed,
  logged, exposed, or included in generated instructions.
- If required Service Principal inputs are missing, describe **what** is missing
  (tenant id, app/client id, and a securely-provided secret reference) using
  presence checks only — never request the secret value in chat. Only when
  Service Principal inputs cannot be provided, fall back to OAuth (Mode B).

Automation boundary: infrastructure (connector create-or-reuse, mirrored item
creation) is automated; **business decisions** (Eventhouse/KQL DB selection,
shortcut creation) always require explicit user confirmation.

### Mode B — choose connection authentication (REQUIRED prompt)

When the chosen identity is User / interactive (Mode B), the connection can be
created two ways. Before detecting or creating anything, present this choice as
**normal chat text (a plain numbered list, not a code block)** and STOP for the
user's answer:

How should I authenticate the Azure Monitor connection?

1. **Interactive sign-in (OAuth)** — you sign in once in Fabric → Manage
   Connections; the connection uses your organizational account.
2. **Workspace identity (no secrets)** — Fabric's automatically-managed workspace
   identity is used as the credential; you grant it access on your Log
   Analytics workspace. No secret to handle.

Route to the matching sub-branch below — **1 → Mode B (OAuth)**, **2 → Mode B
(Workspace identity)**. Keep the two strictly separate. If the user has no
preference, note that workspace identity avoids interactive sign-in and secret
handling, but WAIT for their choice — never auto-select.

### Mode B — OAuth (UI-guided only, fallback)

Use this sub-branch when the user picked option 1 above, i.e. only when Service
Principal (Mode A) is unavailable or the user explicitly requests OAuth. OAuth
connector **creation** is UI-guided only (Fabric → Manage Connections) — the Skill
never creates one through an API; it only **detects and reuses** an existing
connection, read-only, and only when the Log Analytics workspace matches exactly.

Follow the full detection order, reuse rules, and user-facing wording in
[references/oauth-connection-reference.md](references/oauth-connection-reference.md).
Keep this strictly separate from Mode A.

### Mode B — Workspace identity (no secrets)

Use this sub-branch when the user picked option 2 above. Fabric's
automatically-managed **workspace identity** is used as the connection credential
(no secret). This flow provisions the identity if needed, ensures it has a
sufficient Log Analytics role — **assigning it automatically when the caller is
permitted, otherwise instructing the user** — then creates the connection.

Follow the full sequence, endpoints, gates, and payloads in
[references/workspace-identity-connection-reference.md](references/workspace-identity-connection-reference.md).
Key gates: provisioning the identity is confirmation-gated (caller must be
workspace **Admin**); the LA role is assigned by the Skill when the caller
holds role-assignment permission (else the Skill instructs and WAITs for
confirmation) — both writes are confirmation-gated; then create the connection
using the `WorkspaceIdentity` credential type. Keep this strictly separate from
Mode A.

## Stage 6 — AzMon / Mirrored Catalog item creation or reuse

Create the Azure Monitor **Mirrored Catalog** item in the target Fabric
workspace, or reuse an existing matching item. This is a Fabric-modifying action
→ confirm first. Supported Mirrored Catalog operations (item CRUD, definition,
discovery, monitoring, refresh) are documented in
[references/mirrored-catalog-reference.md](references/mirrored-catalog-reference.md).

### Service Principal item-creation (IMPORTANT — prefer reuse; observed fallback)

Per Microsoft Learn, the **Create Mirrored Catalog** API lists **service principals
and managed identities** as supported identities for create, so a Service Principal
create is **documented as supported** and is not an absolute platform limitation.

> **Observed fallback.** Some Service Principal runs have nonetheless seen the
> item **create** rejected under an application-only token (the underlying
> item-creation path can run **on-behalf-of** a signed-in user). Treat this as
> **observed** tenant behavior, not a documented rule, and keep the docs-accurate
> default: attempt create under the SP, and only fall back to a user (delegated) /
> UI context if the create call is actually **denied or unavailable**.

Get, list, **update**, discovery, monitoring, refresh, and shortcut operations all
work under an application-only SP token once the item exists.

Consequently, when running under a Service Principal, the Skill MUST:

- **Prefer reuse** — reuse an existing Azure Monitor Mirrored Catalog item (and
  its existing connection) that the SP can see and operate on. This is the
  preferred path: build on an already-created item + connection rather than
  creating a new one. The SP can then **update** and operate that item normally.
- If no reusable item exists, **attempt to create the item under the SP** (the
  create API documents SP/managed-identity support). Only if that create is
  **denied or unavailable** (the observed fallback above), **create the item in a
  user context** — either from the **Fabric UI**, or via a **user (delegated)
  sign-in** — preferably seeded from an existing item and connection. After the
  item exists, the Service Principal can resume the automated flow (update,
  discovery, monitoring, refresh, shortcuts) on that item.
- Never claim the item was created by the SP when the create actually occurred in
  a user/UI context.

Downstream Mirrored Catalog operations (update, discovery, monitoring, refresh)
remain available to the Service Principal once the item exists.

### Table selection via scope (choosing which tables the item mirrors)

The item does **not** take a free-form list of table names — it mirrors by
**`scope`** (a namespace hierarchy path in the definition), and that scope MUST be
a **`Selectable`** value returned by the **List Scopes** discovery API. To target
only the tables the user wants:

- Call **List Scopes** and choose a `Selectable` scope for the item. If the user
  already knows the target tables, pick the **narrowest `Selectable` scope** that
  covers them. If there is no intent yet (the user wants to explore first),
  create with a **broader scope** and optionally **re-scope** narrower later —
  updating the item definition — once intent is captured. Use only real returned
  scope values — never fabricate a scope or table name.
- If the narrowest available `Selectable` scope is **broader** than the requested
  set, the item **will also mirror the extra sibling tables** under that scope —
  mirroring cannot exclude individual siblings. State this plainly and get
  explicit confirmation before creating.
- For an existing/reused item, read its current definition scope before assuming
  it matches the request; do not fabricate definition fields.

### Default mirror set (REQUIRED starting point)

Unless the user specifies otherwise, the **default set of tables to mirror** is
every table that (a) appears in real **List Scopes / Discovery** output and (b)
matches one of these name prefixes (case-insensitive; tolerate the `_CL`
custom-table suffix):

- `App*` — Application Insights tables
- `OTel*` — OpenTelemetry-native tables (e.g. `OTelLogs`)
- `XD*` — custom, security-related log tables

Then **ask the user whether they want any additional tables** before creating
(confirmation gate — present the resolved set and WAIT).

- Match prefixes against **real discovered tables only** — never invent a table.
  If a prefix matches nothing, omit it silently.
- Resolve the default set to the **narrowest single `Selectable` scope that covers
  all matched tables**. If that scope also pulls in **extra sibling tables** beyond
  the default set, **list the extras explicitly**, explain that siblings cannot be
  individually excluded, and get confirmation before creating. Once confirmed, the
  extras are **expected** — they are not failures at the Stage 8 equality check.
- Adding user-requested tables may widen the chosen scope — re-resolve and
  re-disclose.
- If **none** of `App*` / `OTel*` / `XD*` match any discovered table, fall back to
  presenting all/representative discovered tables (explore-first) and let the user
  choose.
- **`XD*` security tables** are only considered **after** the workspace has passed
  Stage 4's validation (a supported, validated workspace); an unsupported-workspace
  block takes precedence and table selection MUST NOT be used to bypass it.
- **On reuse:** read the existing item's current scope and compare its mirrored
  set to the default set. If not fully covered, offer to **re-scope** (update the
  item definition) to add the missing `App*`/`OTel*`/`XD*` tables, disclosing any
  extra siblings — never re-scope silently; confirm first.

The confirmed set (default + confirmed siblings + any tables the user adds) becomes
the **expected set** for the Stage 8 requested-vs-mirrored equality check.

### First-time mirroring latency (disclosure — REQUIRED)

For a **first-time mirrored workspace**, tell the user upfront that mirrored
tables and data typically take **around 5 minutes** to materialize and become
queryable after the item is created. Until then, discovery/queries may return
empty or partial results — this is **expected**, not an error. Do not declare
tables missing during this window: verify mirror/refresh status, wait, and
re-check before concluding anything.

After the item is created or reused, optionally capture business intent now
(Stage 7) if the user already has a goal; otherwise proceed to table discovery
and exploration and capture intent before schema verification (Stage 12).

## Stage 7 — Business Insight Capture (optional here; deferrable)

If the user already has a business question, capture it now so table discovery
(Stage 8) and Eventhouse scoring (Stage 9) can be guided by it. If they don't,
this stage is **optional right now** — the user may explore their data first
(Stages 8–11) and provide intent later. Either way, intent is **MANDATORY before
schema verification (Stage 12)** and correlation (Stage 14); capturing it early is
just an optimization that focuses discovery.

When capturing intent, ask in business language, e.g.:

- Did service availability issues impact bookings?
- Did request latency reduce customer conversions?
- Did exceptions affect revenue or orders?
- Did dependency failures impact specific customers, tenants, regions, or
  flights?
- Did incidents affect SLA, usage, or customer activity?
- Did traffic drops correlate with usage KPI degradation?

### Enforcement

The Skill MUST NOT proceed to schema verification (Stage 12) or business
**correlation** (Stage 14) without either:

- (a) user-provided business intent, OR
- (b) explicit user selection from suggested directions.

Intent may be provided here or after exploration, but it MUST exist before
Stage 12. Never assume intent.

### Fallback (when the user is unsure / vague / no exact match)

Suggest 3–5 directions, each framed as **observability signal → business
impact**, and ask the user to choose one:

1. Availability failures → booking completion impact.
2. Request latency → conversion or checkout drop.
3. Exceptions → failed orders or revenue at risk.
4. Dependency failures → customer / tenant / region impact.
5. Traffic drops → usage KPI degradation.

### Important distinction

Capturing intent early is **allowed but optional** — it MUST exist before schema
verification (Stage 12). Either way, the Skill MUST NOT generate correlation logic
yet. Correlation logic only comes after shortcuts exist, schema is verified, data
is queryable, dynamic fields are inspected, join candidates are validated, and
data freshness is checked (Stages 10–14).

## Stage 8 — Azure Monitor table discovery

Browse candidate Azure Monitor / Application Insights tables. **If a business goal
was captured (Stage 7),** filter to the tables relevant to it. **If there is no
intent yet (explore-first),** present all/representative discovered tables so the
user can browse. Use only real discovered scope/table values — never fabricate
table names. Use
[references/telemetry-table-reference.md](references/telemetry-table-reference.md)
to explain what each table means in business terms and which tables best fit the
stated goal (or what each table offers when exploring).

### Discovery API fallback policy (REQUIRED)

The **primary** discovery mechanism is the Mirrored Catalog Discovery APIs. If
discovery appears incomplete, do NOT immediately conclude tables are missing or
switch to alternative metadata paths. First:

1. Verify mirror status.
2. Verify refresh / sync status.
3. Verify discovery scope.
4. Retry discovery.

Only after these checks may the Skill evaluate alternative metadata paths. See
[references/mirrored-catalog-reference.md](references/mirrored-catalog-reference.md).

### Requested-vs-mirrored set-equality check (REQUIRED once a specific table set is requested)

This check applies once a **requested table set exists** — whether specified up
front or after intent is captured later. When the **default mirror set** (Stage 6)
or a user-adjusted set is in effect, that set is the **requested set** for this
check, and any sibling tables disclosed and confirmed under the narrowest-common-
scope rule are **expected** (compare against the chosen scope's expected contents,
not a bare table list — do not report confirmed siblings as failures). When the
user asked for a specific set of
tables, verify the item mirrors
**exactly** that set — use **equality, not subset** ("my tables are present" is not
enough). Compare the **actually-mirrored** table set (from Discovery / Monitoring)
against the **requested** set and report the result:

- **Extra tables present** → the chosen scope is broader than requested. Report the
  extras and, if a narrower `Selectable` scope exists, offer to re-scope; otherwise
  state that the source only exposes a broader scope and the extras are
  unavoidable.
- **Requested tables missing** → the mirror may not have materialized yet. Verify
  mirror/refresh status, run a **Refresh/sync**, wait, then re-check — do not
  declare them absent prematurely.
- **Exact match** → confirm and proceed.

Never fabricate the mirrored table set; enumerate it from real Discovery /
Monitoring results only.

## Stage 9 — Eventhouse / KQL database target selection

Ask the user which Eventhouse should host the LA-table shortcuts. Present these
options as **normal chat text (not a code block)** and require explicit
confirmation:

- **A — A specific existing Eventhouse** (e.g. one that already holds business
  data you want to correlate with). The Skill creates LA-table shortcuts
  **there**, colocating telemetry with the business data.
- **B — A new Eventhouse.** The Skill creates it and the LA-table shortcuts;
  starts empty.

Both options are writable and support the Operations Agent path (they can host
`IncidentBins` materialization).

Run **Eventhouse Recommendation Mode** to inform the choice — discover available
Eventhouses, inspect their contents (tables, shortcuts, KQL databases), and score
each by relevant business tables, relevant telemetry tables, existing shortcuts,
queryable tables, KQL database availability, and data freshness. **When the
user's goal is correlating telemetry with existing business data, recommend
option A** (colocation); otherwise a new Eventhouse is a clean starting point.
Present as normal chat text:

- **Recommended target:** <A ‹EventhouseName› | B new>
- **Reason:** <why>
- **Alternatives:** <list>

The Skill MUST NOT auto-select. Present the recommendation, state exactly what
will be created, and require explicit confirmation. See
[references/eventhouse-shortcuts-reference.md](references/eventhouse-shortcuts-reference.md).

## Stage 10 — External Delta table registration planning

Plan **external Delta table registrations** for the resolved table set into the
**chosen/new Eventhouse** — name the target Eventhouse in the plan header —
**before** any schema verification or join logic. Present the plan and STOP for
confirmation.

Key rules (see the shortcuts reference for detail):

- Queryability in a KQL database comes from registering each table as an
  **external Delta table** pointing at the mirrored item's OneLake
  `Tables/dbo/<Table>` path — **not** from the Core Shortcuts API (which creates a
  link only). Query via `external_table('<name>')`.
- Plan, per table: exact name, OneLake `Tables/dbo/<Table>` path, target KQL
  database, and that the schema will be read from the table's Delta log.

### Query acceleration policy — external delta tables (MUST — always `true`)

Query acceleration is a **policy on external delta tables** (set via
`.alter external table … policy query_acceleration`), **not** a shortcut-object
property. Every registered external delta table gets **acceleration enabled
(`true`)** — not optional. Include an `Acceleration Enabled (always Yes)` plan-table
column; if the environment can't support it, surface that rather than registering
without the policy. Full policy in
[references/eventhouse-shortcuts-reference.md](references/eventhouse-shortcuts-reference.md#external-delta-table-query-acceleration-policy-must--always-true).

## Stage 11 — External Delta table registration

Only after explicit confirmation, register each table as an **external Delta
table** in the target KQL database (report which one): read the table's schema
from its Delta log, map Delta → Eventhouse types, and run `.create external table
['<Table>'] (<cols>) kind=delta ( h@'<OneLake Tables/dbo/<Table> path>;impersonate' )`
via `POST {clusterUri}/v1/rest/mgmt`. Then verify with `.show external tables` +
`external_table('<Table>') | take 1`. The Core Shortcuts API is **not** required
for queryability (it creates a link only). If a table is not queryable → STOP and
return to planning / registration. See
[references/eventhouse-shortcuts-reference.md](references/eventhouse-shortcuts-reference.md)
for the schema-read, type mapping, and command template.

When registering ANY external delta table, **always enable the query acceleration
policy (`true`)** per the
[Query acceleration policy](references/eventhouse-shortcuts-reference.md#external-delta-table-query-acceleration-policy-must--always-true),
and report the resulting status (expected: enabled).

## Stage 12 — Schema and data verification (REQUIRED before correlation)

Never build correlation logic on assumptions or screenshots. Before proposing any
join, bin, or threshold, verify against the **actual** KQL database. Business
intent MUST already be captured/confirmed before this stage — if it was deferred
at Stage 7, capture it now (using the Stage 7 questions/fallback) before
proceeding, since the telemetry-source selection below is scored by goal
relevance. Never assume intent.

### Preconditions

1. Operational telemetry tables are available in the Eventhouse / KQL database.
2. Business tables are available in the same database or queryable via shortcuts.
3. Tables are **queryable**, not just visible in OneLake.
4. Schema retrieved via `getschema`.
5. Dynamic fields inspected and sampled.
6. Candidate join keys extracted from top-level **and** dynamic columns.
7. Join keys validated with **non-zero** match results (when a direct join is
   proposed).
8. Data freshness verified.
9. Time window aligned to the real data range.
10. Relevant categorical values confirmed from real data where rules depend on
    them.

### Steps

> **Query convention.** Mirrored telemetry tables are **external tables** — query
> them via `external_table('<name>')` (they do not appear in `.show tables`);
> business tables that are **managed** in an Eventhouse use their bare
> name.

1. **Retrieve real schema.** For each table:
   `external_table('<TableName>') | getschema | project ColumnName, ColumnType`.
   Use authoritative column names/types — not names guessed from screenshots or
   table names.
2. **Inspect and sample dynamic fields.** Business join keys are often nested in
   dynamic columns (`Properties`, `CustomDimensions`, `Details`, `Measurements`,
   `Payload`, `Context`). Sample rows and inspect keys. See
   [references/app-insights-dynamic-fields-reference.md](references/app-insights-dynamic-fields-reference.md).
3. **Extract candidate business identifiers** with explicit KQL
   (`tostring(Properties.BookingId)`, with casing fallbacks via `coalesce`).
4. **Validate join keys against real data.** Prove a candidate joins — run the
   join and confirm non-zero matches:

   ```kusto
   external_table('AppEvents')
   | extend BookingId = tostring(Properties.BookingId)
   | where isnotempty(BookingId)
   | join kind=inner (Bookings | project BookingId = tostring(BookingId)) on BookingId
   | summarize MatchedRows=count(), DistinctBookings=dcount(BookingId)
   ```

   Non-zero → **direct join, high confidence**. Zero → the key is wrong or data
   doesn't overlap; find the real one.
5. **Check freshness and align the window.**
   `external_table('<TableName>') | summarize Rows=count(), MinTime=min(TimeGenerated), MaxTime=max(TimeGenerated)`.
   Do not assume `ago(1h)`; use a window covering the actual data range and
   explain it in user terms.
6. **Confirm categorical values** used by rules
   (`external_table('<Table>') | summarize count() by <field>`) so impact rules
   use real categories.

### Telemetry source selection framework (REQUIRED)

Telemetry source selection MUST be **data-driven**. Before selecting a correlation
model, the Skill MUST inspect ALL candidate telemetry sources discovered (e.g.
AppEvents, AppExceptions, AppRequests, AppDependencies, AppTraces, AppPageViews,
AppBrowserTimings, AvailabilityResults, and any other telemetry source present) —
not just one.

Score each candidate telemetry source by:

1. Business identifiers discovered.
2. Dynamic-field richness.
3. Direct-join confidence.
4. Validated match count.
5. Business-process context.
6. Relevance to the selected business goal.

Select the highest-scoring telemetry source. The Skill MUST NOT automatically
prioritize AppExceptions, and MUST NOT automatically prioritize AppEvents — the
winner is whichever source scores highest against real data.

### Exit criteria (MANDATORY)

Before Stage 14, ALL must hold: schema retrieved via `getschema`; join keys
validated with non-zero matches (when a direct join is used); freshness verified
and window aligned; relevant categorical values confirmed. If any fails → STOP,
do not proceed.

### Handoff (MANDATORY)

Present a concise summary (verified join keys, match results, business impact if
any, data time window). Then ask: "Do you want to continue to business analysis
(impact modeling, a dashboard, and optionally an Operations Agent) based on this
verified model?" HARD STOP and wait. On confirmation, continue with Stages 13–17
as defined in
[references/business-analysis-workflow.md](references/business-analysis-workflow.md).

## Stages 13–17 — Business-oriented analysis (defined in the reference)

The business-oriented analysis half (business data discovery/scoring, correlation
planning, an optional Real-Time KQL dashboard, and an optional gated Operations
Agent) is defined authoritatively in
[references/business-analysis-workflow.md](references/business-analysis-workflow.md)
(with Appendices A–B) and loaded only when the user opts in at the Stage 12
handoff. On opt-in, **do not work from memory** — open that file and follow
Stages 13–17 exactly; the controller still tracks and enforces these stages, their
order, hard stops, and confirmation gates (including dashboard-before-agent and
the Stage 16 "do we even want an agent?" gate).

## Troubleshooting (user-facing)

- **"No playbook generated" / cannot compute a field** → the instructions
  described fields conceptually. Add the explicit KQL materialization query, add
  per-field KQL definitions, ensure alert rules reference actual output columns,
  add dynamic-field extraction, and clarify join keys/identifiers. Do not just
  reword prose.
- **Start succeeds but no Teams alert arrives** → likely no data matched the
  rule. Switch to POC/debug thresholds; explain no data may have matched. Do not
  imply platform failure without evidence.

## Must / Prefer / Avoid

### Must
- Enforce stages, hard stops, and confirmation gates.
- Keep OAuth (UI-guided) and Service Principal (automated create-or-reuse)
  strictly separate.
- Validate permissions before creation.
- Verify schema, dynamic fields, join matches, and freshness before correlation.
- Provide explicit KQL in Operations Agent instructions.

### Prefer
- Service Principal (automated) over OAuth (UI-guided) for connection
  resolution; fall back to OAuth only when Service Principal is unavailable.
- Direct joins over time-window correlation.
- Real discovered values over anything guessed.
- Business-language confirmation over technical questions.

### Avoid
- Do not depend on or mention MCP in the user-facing flow.
- Do not present internal/undocumented APIs as supported.
- Do not claim OAuth connector creation via public API.
- Do not fabricate workspaces, tables, schema, IDs, or query results.
- Do not ask for secrets, OAuth codes, tokens, cookies, or nonces.
- Do not claim causality when only time-window correlation exists.

## Examples

### Example 1 — Onboard Azure Monitor observability data, then check business impact
**User:** "In my `Observability` workspace, onboard our Azure Monitor / Log Analytics observability data (it holds our Application Insights tables) into Fabric, then tell me whether last week's latency spike hurt checkout conversions."

**Skill behavior:** Runs the staged workflow — confirms the target workspace and checks onboarding prerequisites (a reachable Azure Monitor / Log Analytics source or connection), stopping with an explicit list of what is missing if any prerequisite is absent. Once the observability data (including the Application Insights telemetry tables) is onboarded and queryable, it discovers the real business dataset in the workspace, correlates the latency signal against the conversion KPI using discovered keys, and reports a specific business-impact conclusion (or an error if the required data is unavailable). It never fabricates workspace names, tables, or query results, and never exposes tokens or connection internals.

### Example 2 — Out-of-scope authoring request
**User:** "Create a new Spark notebook and build a Delta table pipeline to load my business dataset."

**Skill behavior:** Declines the out-of-scope authoring request, creates nothing in Fabric, and directs the user to the appropriate authoring mode in `spark-cli` rather than taking over the task.
