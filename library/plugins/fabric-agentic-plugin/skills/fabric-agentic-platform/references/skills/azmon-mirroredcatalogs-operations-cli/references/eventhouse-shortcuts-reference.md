# Eventhouse & OneLake shortcuts reference

How the mirrored Azure Monitor tables become **queryable** in an Eventhouse / KQL
database, and the queryability requirement that must be verified before any
correlation logic.

> **Generic Eventhouse/KQL mechanics live in common.** For cluster/query-URI
> discovery, the `az rest` query pattern, `getschema`, and `.show` commands, see
> [EVENTHOUSE-CONSUMPTION-CORE.md § Connection Fundamentals](../../../common/EVENTHOUSE-CONSUMPTION-CORE.md#connection-fundamentals).
> This reference covers only the AzMon-specific shortcut and queryability rules.

## Eventhouse / KQL database

- **Eventhouse / KQL database selection is a user decision.** Always present the
  discovered options and require explicit confirmation. Never auto-select, even
  when discovery has a recommended default.
- The Eventhouse query URI (`queryServiceUri`) is where `getschema`, sampling,
  and validation queries run during schema verification — see the common
  reference above for how to discover and query it.

## Eventhouse targeting options

The user chooses which Eventhouse hosts the LA-table shortcuts. Both options are
writable and create shortcuts; always show the target explicitly and confirm
before creating:

- **A specific existing Eventhouse** (e.g. holding business data) — create
  LA-table shortcuts there to colocate telemetry with business data.
- **A new Eventhouse** — create it + shortcuts; starts empty.

## OneLake shortcuts — the queryability requirement (CRITICAL)

In a **KQL database**, a OneLake shortcut is queried as an **external table** via
the `external_table('<name>')` function — it appears under `.show external tables`
(never `.show tables`), and `<Name> | take 1` will NOT work. The **Core Items
Shortcuts API** (`POST .../items/{itemId}/shortcuts`) creates only the OneLake
**storage link**; it does **not** register a queryable external table in the KQL
engine, so on its own the shortcut is not queryable (`external_table('<name>')`
returns `BadRequest`). Making a mirrored table queryable therefore requires
registering it as an **external Delta table** in the target KQL database (see
below). Notes:

- **Exact source table name** — keep the mirrored table's exact name so
  `external_table('<name>')` and downstream KQL match.
- **Mirrored AzMon tables live under a `dbo` schema folder** — in the mirrored
  catalog item's OneLake they are at `Tables/dbo/<TableName>`, not
  `Tables/<TableName>`. The external-table Delta URI must include the `dbo`
  segment. Confirm by listing `Tables/` first (typically a single `dbo` folder).

## Programmatic external-table registration (KQL database — no UI)

To make the mirrored LA tables queryable in the **chosen/new** Eventhouse (Stage 9)
**without the UI**, register each as an external Delta table pointing
directly at the mirrored item's OneLake path. This is the fully-programmatic
equivalent of the KQL "New → OneLake shortcut" experience, and it makes the Core
Shortcuts API step unnecessary for queryability.

1. **Read the table's real schema from its Delta log.** List
   `.../Tables/dbo/<Table>/_delta_log`, read the latest commit JSON, and parse
   `metaData.schemaString` for column names + Delta types. (Alternative:
   `evaluate infer_storage_schema(dynamic({'StorageContainers':['<abfss path>;impersonate'],'FileFormat':'delta','Mode':'any'}))`
   — convenient but may fail depending on identity/permissions; prefer the
   `_delta_log` read when it does.)
2. **Map Delta → Eventhouse scalar types:**

   | Delta type | Eventhouse type |
   |---|---|
   | `string`, `binary` | `string` |
   | `long` | `long` |
   | `integer`, `short` | `int` |
   | `byte`, `float`, `double` | `real` |
   | `decimal` | `decimal` |
   | `boolean` | `bool` |
   | `date`, `timestamp`, `timestamp_ntz` | `datetime` |
   | `struct`, `array`, `map` | `dynamic` |

3. **Register the external Delta table** in the KQL database via
   `POST {clusterUri}/v1/rest/mgmt`:

   ```kusto
   .create external table ['<Table>'] (<mapped columns>) kind=delta
   ( h@'abfss://<workspace>@onelake.dfs.fabric.microsoft.com/<mirroredItemId>/Tables/dbo/<Table>;impersonate' )
   ```

   `;impersonate` reads under the **caller's** identity — fine for the run
   identity, but any other consumer (e.g. the Operations Agent) needs its own read
   access to that OneLake path.
4. **Verify queryability** with `.show external tables` (all expected tables
   listed) and `external_table('<Table>') | take 1` (single-row probe; avoid
   `count` on large external Delta tables — it forces a full scan).

**KQL-DB shortcut limitations** (if you instead use the UI OneLake-shortcut flow):
one shortcut at a time, one subfolder/table per shortcut, shortcuts can't be
renamed, and you can't shortcut a table with `*` in a column name.

Any OneLake links created earlier via the Core Shortcuts API become **redundant**
once the external tables exist (harmless; removable).

## External delta table registration planning and creation (stage rules)

- **Registration planning happens before schema verification or join logic.** Present
  the plan and STOP for confirmation.
- **External delta table registration requires explicit confirmation.**
- **Handle "already exists" idempotently.** If external-table registration or a
  OneLake link already exists, do **not** treat it as a failure and do **not**
  overwrite. Verify the existing external table points to the intended OneLake
  source and is queryable (`.show external tables` + `external_table('<Table>') | take 1`),
  then proceed. Only recreate if it targets a different source.
- After registration, **verify queryability** with a lightweight query before
  building any correlation logic. Stage 11 validates **queryability, NOT table
  size**, so use a single-row probe rather than a full scan:

  ```kusto
  external_table('<Table>')
  | take 1
  ```

  (`| limit 1` is equivalent.) Avoid `count` here — on large external Delta tables
  a `count` forces an unnecessary full scan, causing long execution times and
  validation delays.

- If a table is not queryable → **STOP** and return to external delta table
  registration planning / creation. Do not build correlation logic on screenshots
  or assumed schema.
- A brand-new AzMon item won't surface tables until its mirror has materialized
  them (typically ~5 minutes for a first-time mirror); wait/refresh before
  expecting queryable tables.

## External delta table query acceleration policy (MUST — always `true`)

Query acceleration is a [policy on external delta tables](https://learn.microsoft.com/en-us/kusto/management/query-acceleration-policy?view=microsoft-fabric)
— applied via `.alter external table <name> policy query_acceleration …` — **not** a
property of a OneLake shortcut object. Because queryability here comes from
registering each mirrored table as an **external delta table** (above), the query
acceleration policy MUST **always be enabled** (`Acceleration Enabled = true`) on
every registered external delta table. Testing showed significant performance
improvements once acceleration was enabled — schema verification, queryability
validation, telemetry sampling, correlation analysis, and Operations Agent
preparation all became substantially faster. Acceleration = true is the required
configuration; it is not optional.

When registering ANY external delta table:

1. Determine whether acceleration is **supported**.
2. Determine the **current** acceleration status.
3. **Always enable the query acceleration policy (`true`)** — this is required for
   every external delta table, not conditional.
4. **Report** the acceleration status (expected: enabled).

During external Delta table registration planning (Stage 10), show for each table:
Table Name, Source, Target, Acceleration Supported (Yes/No), Acceleration Enabled
(always Yes). Every external delta table is registered with acceleration = true.

In the rare case the environment does **not** support acceleration for a given
external delta table, the Skill MUST surface that explicitly and explain the
potential impact on queryability validation, schema verification, telemetry
sampling, correlation analysis, and Operations Agent preparation — it MUST NOT
silently register an external delta table without applying the acceleration policy.

## Verify external table registration

After adding tables, confirm registration and queryability:

```kusto
.show external tables
```

```kusto
external_table('<Table>')
| take 1
```

Stage 11 validates queryability, NOT table size. Prefer the single-row probe
`external_table('<Table>') | take 1` (or `| limit 1`). Avoid `count`, which
forces a full scan of large external Delta tables and slows validation.

If a table is missing from `.show external tables`, it was linked but not
registered — register it as an external Delta table (see **Programmatic
external-table registration** above), keeping the exact source name.
