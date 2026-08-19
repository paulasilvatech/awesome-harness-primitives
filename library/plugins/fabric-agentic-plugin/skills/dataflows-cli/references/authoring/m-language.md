# M Language Semantics for Dataflow Gen2 Authoring

The language-side companion to [connectors.md](connectors.md) (source connectors), [output-destinations.md](output-destinations.md) (destination M), and [mashup-preview.md](mashup-preview.md) (live execution via `executeQuery`). Documents the M language pitfalls and semantics that bite during Dataflow Gen2 authoring — error wrapping, optional access, per-cell error propagation, scoping inside `each`, identifier escaping. Every claim below was reproduced live against a Fabric Dataflow Gen2 via the `executeQuery` Arrow contract.

**Not in scope.** Basic syntax (`let` / `in`, primitive types, function definition), source connectors (see [connectors.md](connectors.md)), output-destination annotations (see [output-destinations.md](output-destinations.md)), the `executeQuery` REST contract (see [mashup-preview.md](mashup-preview.md)).

## `try` and `try ... otherwise`

`try EXPR` always returns a **record**. Field set differs by outcome:

| Outcome | Record shape |
|---|---|
| Success | `[HasError = false, Value = <result>]` |
| Failure | `[HasError = true, Error = [Reason, Message, Detail]]` |

Verified shapes (`try (1 + "a")` returns the error form; `try (40 + 2)` returns the success form):

```m
let
    r = try (1 + "a")
    // r[Error][Reason]  = "Expression.Error"
    // r[Error][Message] = "We cannot apply operator + to types Number and Text."
in
    r
```

`try EXPR otherwise FALLBACK` short-circuits to the fallback value directly — no record wrapper. Use it when you only want a safe value and do not need the error details.

```m
let
    n = try Number.FromText("abc") otherwise 0
in
    n        // n = 0 (a number, not a record)
```

## Per-cell errors in column transformations

Two functions, identical per-cell error behaviour:

| Call | Behaviour on a cell that cannot be converted |
|---|---|
| `Table.TransformColumnTypes(t, {{"A", Int64.Type}})` | Cell stores an **error**: `"We couldn't convert to Number."` |
| `Table.TransformColumns(t, {{"A", Number.FromText}})` | Cell stores an **error**: `"We couldn't convert to Number."` |

Both produce error-valued cells, NOT nulls. Errored cells **serialize as `null`** in Arrow / preview output — that is what makes them look like silent data loss.

Probe against `{"1", "abc", "3"}` cast to `Int64.Type`:

```m
let
    t       = #table(type table [A = text], {{"1"}, {"abc"}, {"3"}}),
    Conv    = Table.TransformColumnTypes(t, {{"A", Int64.Type}}),
    Row0    = try Conv{0}[A],      // [HasError = false, Value = 1]
    Row1    = try Conv{1}[A]       // [HasError = true,  Error[Message] = "We couldn't convert to Number."]
in
    {Row0, Row1}
```

Implications for downstream operators:

- `Table.RowCount(Conv)` works — returns 3. It does not read cell values.
- `Conv{1}[A]` raises the cell error — surfaces as in-band `{"Error":"..."}` via `executeQuery`.
- `Table.SelectRows(Conv, each [A] > 0)` raises on row 1 — the predicate reads `[A]`.
- Aggregations that read the column (`List.Sum(Conv[A])`) raise on first errored cell.

Recovery patterns:

| Goal | Pattern |
|---|---|
| Replace errored cells with `null` | `Table.ReplaceErrorValues(Conv, {{"A", null}})` |
| Replace with a sentinel | `Table.ReplaceErrorValues(Conv, {{"A", -1}})` |
| Filter errored rows out | `Table.SelectRows(Conv, each not (try [A])[HasError])` |
| Trap then re-shape | `Table.TransformColumns(Conv, {{"A", each try _ otherwise null}})` |

## `each` scoping

`each EXPR` is sugar for `(_) => EXPR`. What `_` *means* depends on the calling context.

| Context | What `_` is | What `[Col]` means |
|---|---|---|
| `Table.SelectRows(t, each ...)` | One **row record** | Field access on the row → `_[Col]` |
| `Table.AddColumn(t, "X", each ...)` | One **row record** | Same |
| `Table.Group(t, keys, {{"agg", each ..., type}})` | The **sub-table** of rows in that group | `[Col]` (= `_[Col]`) is the **whole column as a list**, not a scalar cell |
| `List.Transform(lst, each ...)` | The current **list element** | `[Col]` only valid if the element is a record |

`[Col]` is shorthand for `_[Col]` in every context (per the M spec), so the two forms are always equivalent — Microsoft's own `Table.Group` example uses the shorthand (`each List.Sum([price])`). The thing that bites is the **type**, not the syntax: in the row contexts above `[Col]`/`_[Col]` is a scalar cell, but inside `Table.Group` it is the column as a list. For a single cell, index the sub-table first: `_{0}[Col]`. (Item access `{N}` has **no** implicit-`_` shorthand — only field access `[F]` does — so write `_{0}[Col]`, not `{0}[Col]` which parses as a list literal.)

Verified sub-table context (`Table.Group`) — the case that bites:

```m
let
    t = #table(type table [G = text, V = Int64.Type],
               {{"a", 1}, {"a", 2}, {"a", 3}, {"b", 10}, {"b", 20}}),
    G = Table.Group(t, {"G"}, {
        {"RowCount", each Table.RowCount(_),     Int64.Type},
        {"SumV",     each List.Sum(_[V]),         Int64.Type},
        {"FirstV",   each _{0}[V],                Int64.Type}
    })
    // Row "a": RowCount=3, SumV=6,  FirstV=1
    // Row "b": RowCount=2, SumV=30, FirstV=10
in
    G
```

## Optional vs required field access

| Syntax | Missing key behaviour | Verified outcome |
|---|---|---|
| `r[key]` | Raises | `Expression.Error: "The field 'c' of the record wasn't found."` |
| `r[key]?` | Returns `null` | `null` |
| `Record.FieldOrDefault(r, "key", fallback)` | Returns `fallback` | `fallback` |

```m
let
    r           = [a = 1, b = 2],
    safe1       = r[c]?,                              // null
    safe2       = Record.FieldOrDefault(r, "c", -1),  // -1
    raisesError = r[c]                                // error
in
    {safe1, safe2}
```

Use `[?]` when scanning records that may have absent keys (common when extracting JSON or navigating connector nav tables — see [connectors.md § Lakehouse navigation](connectors.md#lakehouse-navigation)). Use `Record.FieldOrDefault` when you want a non-null fallback.

## Quoted identifiers

Use `#"..."` to wrap any identifier that contains whitespace, punctuation, or collides with a reserved keyword (`type`, `section`, `error`, `let`, `if`, etc.).

```m
let
    r = [#"weird name" = 1, #"type" = "x", #"section" = "y", normal = 2],
    a = r[#"weird name"],
    b = r[#"type"]
in
    {a, b}    // {1, "x"}
```

## Constructing errors

```m
// 1. Shorthand: text only -> Reason auto-set to "Expression.Error"
let r = try (error "boom!") in r
// r = [HasError = true,
//      Error    = [Reason = "Expression.Error", Message = "boom!", Detail = null]]
```

```m
// 2. Record form: full control
let r = try (error [Reason  = "MyReason",
                    Message = "MyMessage",
                    Detail  = [extra = "data", n = 99]]) in r
// r[Error][Reason]  = "MyReason"
// r[Error][Message] = "MyMessage"
// r[Error][Detail][extra] = "data"
// r[Error][Detail][n]     = 99
```

Use the record form when downstream code (`try ... otherwise` chains, `Table.ReplaceErrorValues`) needs to discriminate on `Reason` or read structured detail.

## `File.Contents` — exposed but unusable

`File.Contents` is registered in `#shared`, but invoking it raises:

```
Credentials are required to connect to the File source. (Source at <path>.)
```

There is no File credential type for Fabric Dataflow Gen2 cloud refresh. Use a Lakehouse, Warehouse, OData feed, or `Web.Contents` instead -- see [connectors.md Function inventory](connectors.md#function-inventory). For the gateway and direct-`executeQuery` boundary of `Web.Page` / `Web.BrowserContents`, see [connectors.md Browser functions and gateway scope](connectors.md#browser-functions-and-gateway-scope).

## MUST / PREFER / AVOID

**MUST**

1. Wrap any expression that may produce a cell error with `try` before reading the value (`Conv{i}[Col]`, `List.Sum(Conv[Col])`, predicates that reference `[Col]`).
2. Use `[?]` or `Record.FieldOrDefault` for any optional field — `r[key]` raises and propagates as in-band `{"Error":"The field 'key' of the record wasn't found."}`.
3. Quote any identifier that contains whitespace, punctuation, or a reserved keyword — `#"..."`.
4. When aggregating with `Table.Group`, remember `[Col]` (= `_[Col]`, equivalent shorthand) is the **column as a list**, not a scalar — for a single cell index the sub-table explicitly with `_{0}[Col]` (item access `{N}` has no implicit-`_` shorthand, so `{0}[Col]` is wrong).

**PREFER**

1. `try ... otherwise FALLBACK` when you only need a safe value and not the error.
2. `Table.ReplaceErrorValues(t, {{"Col", null}})` over per-row `try` wrapping when you have already projected a column and want to clean the result.

**AVOID**

1. Treating an Arrow-null cell value as "the column has nulls" without testing — it may be an errored cell. Probe with `try Conv{i}[Col]` to disambiguate.
2. `File.Contents`, plus `Web.Page` / `Web.BrowserContents` in direct `executeQuery` - see [`File.Contents`](#filecontents--exposed-but-unusable) and [connectors.md Browser functions and gateway scope](connectors.md#browser-functions-and-gateway-scope).
3. Discriminating on `Error.Reason` without setting it explicitly. Both built-in errors and `error "msg"` use `Reason = "Expression.Error"`. For custom reasons use the record form: `error [Reason = "...", Message = "..."]`.

## See also

| File | When |
|---|---|
| [connectors.md](connectors.md) | M source connectors, runtime-disabled functions, in-band error contract for `executeQuery` |
| [output-destinations.md](output-destinations.md) | Destination M and `DataDestinations` annotation |
| [mashup-preview.md](mashup-preview.md) | How `executeQuery` returns errors (in-band `{"Error":"..."}` in `PQ Arrow Metadata`) |
| [connection-management.md](connection-management.md) | Credentialed sources, including the File-credential gap that grounds `File.Contents`'s runtime failure |
