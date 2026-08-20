# Source Connectors in Dataflow Gen2 Mashup (M)

The source-side companion to [connection-management.md](connection-management.md) (REST connection lifecycle) and [output-destinations.md](output-destinations.md) (destination-side M). Documents which Power Query M source connectors are reachable from the Fabric Dataflow Gen2 mashup engine, their argument shapes, navigation patterns, and runtime errors. All claims confirmed by `executeQuery` probing — the in-band-error contract (HTTP 200 with `{"Error":...}` in the `PQ Arrow Metadata` column) is documented at [mashup-preview.md § Error handling](mashup-preview.md#error-handling).

## Connector vs binding vs M function

| Layer | What it is | Where it lives |
|---|---|---|
| **Connection resource** | Fabric-managed credentials + parameters | `/v1/connections/{id}` — see [connection-management.md § Step 2](connection-management.md#step-2--create-connection-cloud) |
| **Dataflow binding** | `connections[]` entry in `queryMetadata.json` tying one connection to a dataflow | Dataflow definition — see [authoring-cli-quickref.md § Connection Binding Quick Patterns](authoring-cli-quickref.md#connection-binding-quick-patterns) |
| **M function call** | Source expression in `mashup.pq` — `Sql.Database(...)`, `Lakehouse.Contents(...)` | `mashup.pq` |

The function and the binding must agree on **kind**; REST casing differs from M (REST `"SQL"` ↔ M `Sql.Database`) — see [connection-management.md § Connection Type Examples](connection-management.md#connection-type-examples) and [§ Step 1](connection-management.md#step-1--list-supported-connection-types).

## Function inventory

All functions below have their symbol registered in the Fabric mashup engine (`Value.Type(<function>)` returns `[Type]`). Runtime behaviour is split into the next three sections.

| Function | Behaviour |
|---|---|
| `Lakehouse.Contents` | ✅ Fully executes against a bound Lakehouse connection — see [Lakehouse navigation](#lakehouse-navigation) |
| `Sql.Database` | 🔑 Needs SQL binding — see [Credentialed connectors](#credentialed-connectors) |
| `Fabric.Warehouse` | 🔑 Needs Warehouse binding |
| `OData.Feed` | 🔑 Needs OData binding |
| `Web.Contents` | 🔑 Needs Web binding |
| `PowerPlatform.Dataflows` | 🔑 Needs PowerPlatformDataflows binding (singleton) — see [PowerPlatform.Dataflows navigation](#powerplatformdataflows-navigation) |
| `Snowflake.Databases`, `AzureStorage.DataLake`, `Excel.Workbook` | 🔑 Symbol present; not exercised end-to-end here |
| `Html.Table`, `Csv.Document`, `Json.Document`, `Lines.FromBinary`, `#table` | ✅ Pure parsers — no binding — see [Pure-data parsers](#pure-data-parsers) |
| `Variable.Value` | 🔑 Symbol present; requires a Variable Library on the dataflow — see [Variable.Value](#variablevalue) |
| `Web.Page`, `Web.BrowserContents` | Gateway-backed in cloud dataflows; disabled in the direct `executeQuery` runtime tested here - see [Browser functions and gateway scope](#browser-functions-and-gateway-scope) |

Full enumeration at runtime via [`#shared`](#shared).

## Browser functions and gateway scope

Microsoft Learn documents `Web.Page` and `Web.BrowserContents` as available in
cloud dataflows through an on-premises data gateway. See
[Using a gateway with the Web connector](https://learn.microsoft.com/en-us/power-query/connectors/web/web-troubleshoot#using-a-gateway-with-the-web-connector).

The direct, gateway-free `executeQuery` runtime probed for this skill returned
the following errors, even for inline literals:

| Function | Verbatim engine error |
|---|---|
| `Web.BrowserContents` | `The module named 'WebBrowserContents' has been disabled in this context.` |
| `Web.Page` | `The module named 'Html' has been disabled in this context.` |

For gateway-free authoring and preview, use `Web.Contents` plus
[`Html.Table`](#pure-data-parsers). If browser rendering is required, use a
gateway-backed Web connection and validate through the supported cloud-dataflow
path rather than direct `executeQuery`.

## Lakehouse navigation

Canonical call:

```m
Lakehouse.Contents()
```

`Lakehouse.Contents(null)` and `Lakehouse.Contents([HierarchicalNavigation = null, CreateNavigationProperties = false, EnableFolding = false])` return the same navigation root. The options-record form is the form used by [output-destinations.md § Destination Type: Lakehouse](output-destinations.md#destination-type-lakehouse); not required for reads.

### Navigation shape

**Root** — workspaces visible to the bound connection (columns: `workspaceId`, `workspaceName`, `Data`, plus navigation hints `ItemKind`, `ItemName`, `IsLeaf`):

| Column | Use |
|---|---|
| `workspaceId` (string) | Index by GUID: `{[workspaceId="..."]}` |
| `workspaceName` (string) | Index by display name (fragile if duplicates) |
| `Data` (table) | Drilldown into that workspace |

**Inside a workspace** — one row per Lakehouse / SQL endpoint, columns: `lakehouseId`, `lakehouseName`, `description`, `capacityObjectId`, `extendedProperties`, `Data`, `databaseId`, `ItemKind`, `ItemName`, `IsLeaf`.

| Column | Use |
|---|---|
| `lakehouseId` (string) | Index by GUID: `{[lakehouseId="..."]}` |
| `Data` (table) | Drilldown into the lakehouse contents |

**Inside a lakehouse** — **mixed contents**, not a flat list of tables. Columns: `Name`, `Id`, `Data`, `Schema`, `ItemKind`, `ItemName`, `IsLeaf`. Rows include `ItemKind = "Table"` (user tables, `Schema = "dbo"`), `ItemKind = "View"` (built-in views in schemas `sys` and `queryinsights`), and a single `ItemKind = "Folder"` row with `Name = "Files"` for OneLake file access.

| Pattern | Use |
|---|---|
| `{[Name="MyTable"]}[Data]` | Read a specific table or view by name |
| `{[Id="Files"]}[Data]` | Drill into the Files folder (returns `Folder.Contents`-style rows: `Content`, `Name`, `Extension`, `Folder Path`, `Date modified`, …) |
| `Table.SelectRows(Lh, each [ItemKind] = "Table")` | Filter to only user tables |

### End-to-end read

```m
section Section1;

shared MyTable = let
    Source = Lakehouse.Contents(),
    Workspace = Source{[workspaceId = "<workspace-guid>"]}[Data],
    Lakehouse = Workspace{[lakehouseId = "<lakehouse-guid>"]}[Data],
    Table = Lakehouse{[Name = "Products"]}[Data]
in
    Table;
```

> **Anti-pattern.** `…{[lakehouseId=...]}[Data]{[Id="Tables"]}[Data]` is **wrong** — there is no `Tables` folder entry; tables are listed directly at the lakehouse-`[Data]` level. The engine returns `"The key didn't match any rows in the table."` (`{[Id="Files"]}[Data]` is **valid** — it's the one folder entry that exists.)

## PowerPlatform.Dataflows navigation

Read the output of another Dataflow Gen2 with the `PowerPlatform.Dataflows` connector. The argument is **required** — call `PowerPlatform.Dataflows(null)`; the no-arg form `PowerPlatform.Dataflows()` is a compile error. The result is a nav table you drill by index, the same shape pattern as [Lakehouse navigation](#lakehouse-navigation).

### Navigation shape

| Step | Expression | Returns |
|---|---|---|
| Root | `PowerPlatform.Dataflows(null)` | Nav table whose first drill key is the literal `Workspaces` entry |
| Workspaces | `{[Id = "Workspaces"]}[Data]` | One row per workspace (`workspaceId`, `Name`, `Data`) |
| A workspace | `{[workspaceId = "<guid>"]}[Data]` | One row per dataflow in that workspace (`dataflowId`, `dataflowName`, `Data`) |
| A dataflow | `{[dataflowName = "<name>"]}[Data]` | The dataflow's output table(s) |

Pass the workspace id through a Variable Library rather than hardcoding a GUID literal — see [`Variable.Value`](#variablevalue).

### End-to-end read

```m
section Section1;

shared UpstreamDataflow = let
    Source     = PowerPlatform.Dataflows(null),
    Workspaces = Source{[Id = "Workspaces"]}[Data],
    Workspace  = Workspaces{[workspaceId = Variable.Value("currentWorkspaceId")]}[Data],
    Dataflow   = Workspace{[dataflowName = "eval_authoring_basic"]}[Data]
in
    Dataflow;
```

> **Note.** The first drill is the literal `{[Id = "Workspaces"]}[Data]` entry, **not** a `workspaceId` index — `workspaceId` selection happens at the next level down. The `(null)` argument is mandatory.

## Credentialed connectors

Without a matching dataflow binding, each function below returns the in-band error `"Credentials are required to connect to the <kind> source. (Source at <source>.)"` — the credential error itself confirms parsing and arity validation succeeded.

| Function | Signature | Verbatim credential error (no binding) |
|---|---|---|
| `Sql.Database(server, database, [options])` | 2 or 3 args; 1-arg form rejected with `1 arguments were passed to a function which expects between 2 and 3.` | `Credentials are required to connect to the SQL source. (Source at <server>;<database>.)` |
| `Fabric.Warehouse([options])` / `Fabric.Warehouse(null)` | Options record or `null` | `Credentials are required to connect to the Warehouse source. (Source at Warehouse.)` |
| `OData.Feed(url, [headers], [options])` | 1–3 args | `Credentials are required to connect to the OData source. (Source at <url>.)` |
| `Web.Contents(url, [options])` | 1–2 args; returns binary | `Credentials are required to connect to the Web source. (Source at <url>.)` |
| `PowerPlatform.Dataflows(null)` | Singleton; takes `null` | `Credentials are required to connect to the PowerPlatformDataflows source. (Source at PowerPlatformDataflows.)` |

To enable any of these, bind a matching-`kind` connection per [authoring-cli-quickref.md § Connection Binding Quick Patterns](authoring-cli-quickref.md#connection-binding-quick-patterns). For multi-source documents add [`[AllowCombine = true]`](#allowcombine--true).

## Pure-data parsers

These transform in-memory values and require no binding — safe primitives for tests and for parsing payloads pulled by a credentialed connector.

### `Html.Table(html, columnNameSelectorPairs, [options])`

```m
Html.Table(Web.Contents("https://example.com/page"),
    {{"Name", ".product-name"}, {"Price", ".product-price"}},
    [RowSelector = ".product-row"])
```

- **Observed engine behavior:** in live Dataflow Gen2 refresh, supplying a `RowSelector` is needed whenever more than one `{columnName, cssSelector}` pair is given. Microsoft Learn documents the options record — including `RowSelector` — as optional and does not state this rule; treat it as behavior this skill verified live. Use `RowSelector` to group the repeating rows.
- Works on tables defined by *any* repeating CSS pattern, not just `<table>`.

### `Csv.Document(binary, [options])`

```m
Csv.Document(Web.Contents("https://example.com/data.csv"),
    [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv])
```

Both `QuoteStyle.Csv` and `QuoteStyle.None` accepted; optional `Columns = <n>` to fix arity.

### `Json.Document(text-or-binary, [encoding])`

```m
Json.Document("{""x"": 42}")
Json.Document(Text.ToBinary("{""x"":42}", 65001), 65001)
```

### `Lines.FromBinary`, `#table`

```m
Lines.FromBinary(Web.Contents("https://example.com/log.txt"))
#table(type table [Id = Int64.Type, Name = text], {{1, "A"}, {2, "B"}})
```

`Lines.FromBinary` streams a binary as a list of lines; `#table` is the standard inline-table constructor.

## `#shared`

`#shared` is the global record of every loaded function and identifier. Enumerate connectors at runtime:

```m
let
    Source = #shared,
    AsTable = Record.ToTable(Source),
    SqlFunctions = Table.SelectRows(AsTable, each Text.StartsWith([Name], "Sql."))
in
    SqlFunctions
```

Returns columns `Name` and `Value` (function/type/table/record).

## `Variable.Value`

`Variable.Value("<name>")` reads a named variable from the dataflow's Variable Library. If the variable does not exist the engine returns `"The variable '<name>' could not be found."`.

```m
section Section1;
shared CurrentWorkspaceId = Variable.Value("currentWorkspaceId");
```

Reading a variable value requires a Variable Library configured on the dataflow.

## `[AllowCombine = true]`

For documents that combine more than one credentialed source, prepend the section attribute on the first non-comment line:

```m
[AllowCombine = true]
section Section1;

shared Q = ...;
```

Without it the privacy firewall blocks evaluation when two or more sources are referenced — see [connection-management.md § Operational Pitfalls](connection-management.md#operational-pitfalls).

## MUST / PREFER / AVOID

### MUST

1. **Match the M function kind to the binding kind.** REST casing differs (REST `"SQL"` ↔ M `Sql.Database`) — see [connection-management.md § Step 1](connection-management.md#step-1--list-supported-connection-types).
2. **Use `Html.Table` for gateway-free HTML parsing.** `Web.Page` and `Web.BrowserContents` require an on-premises gateway in cloud dataflows and are disabled in the direct `executeQuery` runtime tested here.
3. **For combined-source documents, add `[AllowCombine = true]`** before `section Section1;`.
4. **Decode the Arrow stream and inspect `PQ Arrow Metadata`** when reading `executeQuery` results — 200 OK is not success.

### PREFER

1. **Index by GUID** (`workspaceId`, `lakehouseId`) over display name for Lakehouse navigation.
2. **Pure parsers** (`Csv.Document`, `Json.Document`, `Html.Table`) for in-memory data — no binding required.
3. **The verified Lakehouse navigation shape** (`workspaceId → lakehouseId → Name`) over folder-style `{[Id="Tables"]}`.

### AVOID

1. **`Web.BrowserContents` in direct `executeQuery`** - use a gateway-backed Web connection when browser rendering is required.
2. **`Web.Page` in direct `executeQuery`** - use a gateway-backed Web connection when the legacy browser function is required.
3. **`Sql.Database("server")`** (1-arg form) — engine rejects with arity error. Always supply the database name.
4. **`{[Id="Tables"]}` at the lakehouse-`[Data]` level** — there is no `Tables` folder; tables are listed directly. (`{[Id="Files"]}` IS valid — it's the only folder entry.)

## See also

- [connection-management.md](connection-management.md) — REST-side connection lifecycle, `supportedConnectionTypes`, kind casing, binding workflow.
- [mashup-preview.md](mashup-preview.md) — `executeQuery` API contract, request body, Arrow stream decoding, embedded errors.
- [output-destinations.md](output-destinations.md) — destination-side M (Lakehouse Table, Warehouse, ADX, Azure SQL writes).
- [authoring-cli-quickref.md § Connection Binding Quick Patterns](authoring-cli-quickref.md#connection-binding-quick-patterns) — binding a connection to a dataflow definition.
- [authoring-script-templates.md](authoring-script-templates.md) — end-to-end bash + PowerShell smoke; includes `OData.Feed` example.
- [dataflows-cli consumption mode § Query Evaluation](../consumption.md#query-evaluation) — Arrow → CSV / pandas decoder template.
- [common/DATAFLOWS-AUTHORING-CORE.md](../../../../common/DATAFLOWS-AUTHORING-CORE.md) — Common Connection Kinds table; 3-part definition structure.
