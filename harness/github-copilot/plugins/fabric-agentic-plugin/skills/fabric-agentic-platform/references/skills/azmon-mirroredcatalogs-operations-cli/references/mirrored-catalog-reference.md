# Mirrored Catalog reference

Supported Fabric Mirrored Catalog operations for onboarding Azure Monitor /
Application Insights / Log Analytics data as an AzMon item. All operations below
are documented REST APIs.

> **Preview / beta status:** The Azure Monitor Mirrored Catalog item is in
> **Preview**, and its Discovery, Monitoring, and Refresh operations are `(beta)`
> — they require the `beta=true` query parameter. Treat this surface as subject
> to change and confirm the current shape against Microsoft Learn before relying
> on it.

## What a Mirrored Catalog (AzMon) item is

A Fabric item that mirrors an external catalog (here, Azure Monitor / Log
Analytics) into Fabric so its tables become discoverable and, via Eventhouse
shortcuts, queryable in a KQL database. The item is created in a target Fabric
workspace and bound to a connection (OAuth or Service Principal) for the source
Log Analytics workspace.

## Operation groups

### Item CRUD

Create, get, update, list, and delete the Mirrored Catalog item in a Fabric
workspace. Creating the item requires a valid connection for the source Log
Analytics workspace and sufficient Fabric workspace permission. Capture the
returned item id for later monitoring/refresh calls.

> **Service Principal item creation (prefer reuse; observed fallback).** Per
> Microsoft Learn, the **Create Mirrored Catalog** API lists **service principals
> and managed identities** as supported identities for create, so SP create is
> **documented as supported**. Some Service Principal runs have nonetheless
> **observed** the item **create** rejected under an application-only token (the
> underlying item-creation path can run **on-behalf-of** a signed-in user). Keep
> the docs-accurate default: **prefer reusing** an existing item + connection;
> otherwise **attempt create under the SP**, and only fall back to a **user
> (delegated) sign-in / Fabric UI** create if that create is **denied or
> unavailable**. Get, list, **update**, discovery, monitoring, and refresh remain
> available to the SP once the item exists.

- [Items - REST API (MirroredCatalog)](https://learn.microsoft.com/en-us/rest/api/fabric/mirroredcatalog/items)

### Item definition

The item definition describes the mirrored catalog configuration (source binding,
selected scope/tables where applicable). Read the current definition before
editing; do not fabricate definition fields.

- [Mirrored Catalog item definition](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/mirrored-catalog-definition)

### Discovery

Browse available source **scopes** (namespaces) and **tables** after the
connection/item is available. Use only returned scope/table values — never
fabricate table names. Discovery is read-only.

> **Scope-based table selection (not per-table).** The item mirrors by `scope` —
> a namespace hierarchy path that MUST be a `Selectable` value from the List
> Scopes API — not by a free-form list of table names. To mirror only specific
> tables, pick the **narrowest `Selectable` scope** that covers them. When there
> is no intent yet (explore-first), create with a **broader scope** and re-scope
> narrower later once intent is known. If the narrowest available scope is broader
> than the requested set, every sibling
> table under it is mirrored too (siblings cannot be individually excluded) —
> surface this and confirm before creating. After create/reuse, verify the
> mirrored table set equals the requested set (**equality, not subset**): extras
> mean the scope is too broad; missing tables mean the mirror has not
> materialized yet (verify status, refresh/sync, wait, re-check).

- [Discovery - REST API (MirroredCatalog)](https://learn.microsoft.com/en-us/rest/api/fabric/mirroredcatalog/discovery)

#### Discovery API fallback policy

The Mirrored Catalog Discovery APIs are the **primary** discovery mechanism. If
discovery appears incomplete, do NOT immediately switch to alternative metadata
paths. First:

1. Verify mirror status.
2. Verify refresh / sync status.
3. Verify discovery scope.
4. Retry discovery.

Only after these checks may alternative metadata paths be evaluated.

### Monitoring

Report readiness/status of the mirrored item and of individual tables rather than
guessing readiness. A brand-new item will not surface tables until its mirror has
materialized them (typically ~5 minutes for a first-time mirror).

- [Monitoring - REST API (MirroredCatalog)](https://learn.microsoft.com/en-us/rest/api/fabric/mirroredcatalog/monitoring)

### Refresh / run sync job

Trigger a catalog metadata refresh / sync after item creation to bring table
metadata up to date. Do not claim refresh completed unless the service confirms
it.

- [Refresh - REST API (MirroredCatalog)](https://learn.microsoft.com/en-us/rest/api/fabric/mirroredcatalog/refresh)

## Guardrails

- These APIs cover item CRUD, definition, discovery, monitoring, and
  refresh/sync. They do **not** document OAuth Azure Monitor connector creation —
  treat OAuth connector creation as UI-guided (see azmon-fabric-api-reference.md).
- Discovery/monitoring output is authoritative for names/status; do not invent
  values.
- Mirroring metadata into the catalog is **not** the same as a table being
  queryable in Eventhouse. Queryability requires an Eventhouse shortcut that
  registers the table (see eventhouse-shortcuts-reference.md).
- Business tables are **not** expected in Log Analytics. They may exist in an
  Eventhouse, KQL database, Warehouse, Lakehouse, or via Fabric shortcuts. Their
  absence in Log Analytics does NOT mean business data is absent.
