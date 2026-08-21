# Variable Library -- `authoring` mode

Definition parts, variable types, and create/update by definition.

This reference covers the Variable Library item definition: definition parts, variable types, and create/update by definition. The active value set is item state, not definition, and lives in [operations.md](operations.md). It is grounded in [ITEM-DEFINITIONS-CORE.md - VariableLibrary](../../../common/ITEM-DEFINITIONS-CORE.md#variablelibrary), the [Variable Library definition REST article](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/variable-library-definition), the [Get Variable Library REST API](https://learn.microsoft.com/en-us/rest/api/fabric/variableharness/github-copilot/items/get-variable-library), the [Update Variable Library REST API](https://learn.microsoft.com/en-us/rest/api/fabric/variableharness/github-copilot/items/update-variable-library), and [Variable Library value sets](https://learn.microsoft.com/en-us/fabric/cicd/variable-harness/github-copilot/value-sets).

## Definition Parts

A Variable Library definition has these serialized parts:

| Part | Purpose | Required |
|---|---|---|
| `variables.json` | Variable names, types, default `value`, and optional `note` | Yes |
| `settings.json` | Library settings, especially `valueSetsOrder` | Yes |
| `valueSets/<name>.json` | Non-default overrides for one value set | Only when using alternate value sets |
| `.platform` | Common item metadata | Optional |

Use the plural path `valueSets/`. The REST definition article is internally inconsistent in one example that shows `valueSet/`; the canonical repo doc and the CI/CD Learn article use `valueSets/`, so use plural and tenant-verify if an API response differs.

`variables.json` uses `value` for the default value:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/variableLibrary/definition/variables/1.0.0/schema.json",
  "variables": [
    { "name": "target_path", "type": "String", "value": "Files/dev", "note": "Lakehouse folder" },
    { "name": "max_rows", "type": "Integer", "value": 1000 },
    { "name": "enable_debug", "type": "Boolean", "value": true }
  ]
}
```

`settings.json` can have an empty or partial `valueSetsOrder`. Missing valid value set names are appended by the service in alphabetical order on update.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/variableLibrary/definition/settings/1.0.0/schema.json",
  "valueSetsOrder": ["dev", "test", "prod"]
}
```

A value set file uses `variableOverrides`, not `values`:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/variableLibrary/definition/valueSet/1.0.0/schema.json",
  "name": "prod",
  "description": "Production overrides",
  "variableOverrides": [
    { "name": "target_path", "value": "Files/prod" },
    { "name": "max_rows", "value": 1000000 }
  ]
}
```

Include an override only where the value genuinely differs from the variable's default. An override **pins** the value for that value set: once written, a later change to the default in `variables.json` no longer reaches it. Writing `{ "name": "target_path", "value": "Files/dev" }` into a `dev` value set whose default is already `Files/dev` looks harmless, but it silently opts `dev` out of inheritance, so the next default change applies everywhere except there. A value set that overrides nothing is valid and should carry an empty `variableOverrides` array.

## Definition Plane and Item-State Plane

Variable Library authoring has two different planes:

| Plane | What changes | Serialized to Git | API shape |
|---|---|---|---|
| Definition plane | Variables, default values, value set files, value set order | Yes | `create item`, `getDefinition`, `updateDefinition` |
| Item-state plane | Which value set is active in one workspace | No | `GET/PATCH /variableLibraries/{id}` |

Editing a variable's default `value` or a value set override is a definition edit. Selecting the active value set is workspace item state. Deployment intentionally does not overwrite the selected active value set in each stage, and deployment pipeline comparison does not mark a simple active value set switch as source difference. This behavior is documented in [Variable Library CI/CD](https://learn.microsoft.com/en-us/fabric/cicd/variable-harness/github-copilot/variable-library-cicd) and [value sets](https://learn.microsoft.com/en-us/fabric/cicd/variable-harness/github-copilot/value-sets).

## Variable Types

The REST definition type table and [ITEM-DEFINITIONS-CORE.md](../../../common/ITEM-DEFINITIONS-CORE.md#variablelibrary) list these canonical types:

| Type | Value shape |
|---|---|
| `Boolean` | JSON boolean |
| `DateTime` | ISO 8601 string |
| `Number` | JSON number |
| `Integer` | JSON integer |
| `String` | JSON string |
| `ItemReference` | `{ "workspaceId": "<guid>", "itemId": "<guid>" }` |

ConnectionReference is a newer advanced type documented in [Variable library connection reference](https://learn.microsoft.com/en-us/fabric/cicd/variable-harness/github-copilot/connection-reference-variable-type). That Learn article shows `type: "connectionReference"` and `value: { "connectionId": "<id>" }`. Because it is absent from the REST definition type table, use it only with tenant verification and cite the connection reference article when doing so. Microsoft Learn's [Variable types](https://learn.microsoft.com/en-us/fabric/cicd/variable-harness/github-copilot/variable-types) page also lists a `Guid` type (mapping to pipeline `String`); it is likewise absent from the REST definition table and `common/`, so treat it as verify-on-tenant.

In `variables.json`, a variable's default `value` uses its native JSON type (`true` for Boolean, `1000` for Integer). In `valueSets/*.json`, each `variableOverrides[].value` uses the **same native JSON type as the variable it overrides** (Boolean -> `true`/`false`, Integer/Number -> a number, String -> a string). Although the [REST definition article](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/variable-library-definition) lists `VariableOverride.value` as `String`, the live API **rejects a stringified boolean/number override** with `InvalidContent (InvalidValueOrTypeMismatch)` (verified on tenant 2026-07-02). Use native types.

## Create and Update by Definition

Follow shared authentication, token, and LRO handling from [COMMON-CLI.md](../../../common/COMMON-CLI.md#fabric-control-plane-api-via-az-rest). Examples assume `WS_ID` and `VL_ID` are already resolved.

Create a `VariableLibrary` item with definition through the generic item create endpoint. Do not include `definition.format`.

```bash
python3 - <<'PY' > create-variable-library.json
import base64, json
parts = {
    "variables.json": {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/variableLibrary/definition/variables/1.0.0/schema.json",
        "variables": [
            {"name": "target_path", "type": "String", "value": "Files/dev"},
            {"name": "enable_debug", "type": "Boolean", "value": True}
        ]
    },
    "settings.json": {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/variableLibrary/definition/settings/1.0.0/schema.json",
        "valueSetsOrder": ["dev", "prod"]
    },
    "valueSets/dev.json": {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/variableLibrary/definition/valueSet/1.0.0/schema.json",
        "name": "dev",
        # dev matches both variable defaults, so it overrides nothing and keeps inheriting them
        "variableOverrides": []
    },
    "valueSets/prod.json": {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/variableLibrary/definition/valueSet/1.0.0/schema.json",
        "name": "prod",
        "variableOverrides": [
            {"name": "target_path", "value": "Files/prod"},
            {"name": "enable_debug", "value": False}
        ]
    }
}
body = {
    "displayName": "AppConfig",
    "type": "VariableLibrary",
    "definition": {
        "parts": [
            {
                "path": path,
                "payload": base64.b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode(),
                "payloadType": "InlineBase64"
            }
            for path, payload in parts.items()
        ]
    }
}
print(json.dumps(body, indent=2))
PY
```

```bash
az rest \
  --method post \
  --resource https://api.fabric.microsoft.com \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items" \
  --headers "Content-Type=application/json" \
  --body @create-variable-library.json
```

To update an existing definition, get the current definition, decode the parts, modify the relevant JSON, re-encode all required parts into `update-variable-library-definition.json` (same base64-parts structure and `> file` redirect pattern as the create snippet above), then call `updateDefinition`:

```bash
az rest \
  --method post \
  --resource https://api.fabric.microsoft.com \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$VL_ID/getDefinition" \
  --body '{}'
```

```bash
az rest \
  --method post \
  --resource https://api.fabric.microsoft.com \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$VL_ID/updateDefinition" \
  --headers "Content-Type=application/json" \
  --body @update-variable-library-definition.json
```

## Troubleshooting (authoring)

| Symptom | Likely cause | Fix |
|---|---|---|
| Definition request is rejected with a format-related error | Variable Library does not support `definition.format` | Omit the `format` field entirely, including `null` |
| Value set overrides are ignored or invalid | Used `values` instead of `variableOverrides`, or file name does not match the value set name | Use `valueSets/<name>.json` with `name` and `variableOverrides` |
| Create fails: `InvalidContent (InvalidValueOrTypeMismatch)` | A value-set `variableOverrides[].value` was a string for a Boolean/Integer/Number variable | Use the variable's native JSON type in overrides (`false`, `1000000`), not a string. The REST doc's `String` type is misleading (verified on tenant) |
| Default value is missing after create | Used `defaultValue` instead of `value` in `variables.json` | Use `value` for defaults |
| `settings.json` validation fails | `valueSetsOrder` includes a name with no matching `valueSets/<name>.json` file | Add the file or remove the name from `valueSetsOrder` |

### Verified on tenant (2026-07-02)

- Definition part path is `valueSets/<name>.json` (plural), confirmed by reading the stored definition back.
- `variableOverrides[].value` must use the variable's native JSON type; a stringified boolean/number override is rejected with `InvalidContent (InvalidValueOrTypeMismatch)`.
- Create-by-definition via `POST /workspaces/{ws}/items` (type `VariableLibrary`, no `format`) returns 202 and completes via LRO.

### Still to verify on tenant

- `ConnectionReference` (`type: "connectionReference"`, `value: { "connectionId": "<id>" }`) and `Guid` are documented but absent from the REST definition type table. Confirm the shape before automating.
- Fabric `fab` CLI exists, but this skill does not provide Variable Library `fab` syntax because the command shape is not verified here.
