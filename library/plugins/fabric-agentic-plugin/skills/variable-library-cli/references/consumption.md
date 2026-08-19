# Variable Library -- `consumption` mode

Wiring a Variable Library variable into a consumer item and reading its resolved value.

This reference defines the Variable Library side of the consumer contract. It cites [Variable Library overview](https://learn.microsoft.com/en-us/fabric/cicd/variable-library/variable-library-overview), [pipeline integration](https://learn.microsoft.com/en-us/fabric/data-factory/variable-library-integration-with-data-pipelines), [Set Variable activity](https://learn.microsoft.com/en-us/fabric/data-factory/set-variable-activity), [NotebookUtils variable library utilities](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-variable-library), [Dataflow Gen2 variable library integration](https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-variable-library-integration), [shortcut variable assignment](https://learn.microsoft.com/en-us/fabric/onelake/assign-variables-to-shortcuts), [Copy Job CI/CD](https://learn.microsoft.com/en-us/fabric/data-factory/cicd-copy-job), [User Data Functions variable library access](https://learn.microsoft.com/en-us/fabric/data-engineering/user-data-functions/python-programming-model#get-variables-from-fabric-variable-libraries), and [Apache Airflow jobs variable library integration](https://learn.microsoft.com/en-us/fabric/data-factory/apache-airflow-jobs-variable-library-integration).

## Scope Boundary

This skill owns:

- Creating and updating the Variable Library item and its value sets.
- Explaining how a consumer identifies a library variable: library name, library item ID where required, variable name, value type, and active value set behavior.
- Providing small VL-side snippets for supported consumers.

This skill does not own deep authoring of the consumer items. If a task requires building a full pipeline, notebook, Dataflow Gen2 mashup, Copy Job, shortcut, UDF, or Plan item, route to the relevant authoring skill or documentation after establishing the Variable Library contract.

Supported consumers listed by Learn are Data Pipeline, Lakehouse Shortcut, Notebook, Dataflow Gen2, Copy Job, User Data Functions, Apache Airflow jobs, and Plan.

## Data Pipeline Contract

Pipeline definitions consume Variable Library values through a `libraryVariables` block under pipeline `properties`, sibling to `activities`. Each entry needs `libraryName`, `libraryId`, `variableName`, and the pipeline-side `type`.

```json
{
  "properties": {
    "activities": [
      {
        "name": "UseTargetPath",
        "type": "SetVariable",
        "typeProperties": {
          "variableName": "targetPath",
          "value": {
            "value": "@pipeline().libraryVariables.target_path",
            "type": "Expression"
          }
        }
      }
    ],
    "libraryVariables": {
      "target_path": {
        "libraryName": "AppConfig",
        "libraryId": "00000000-0000-0000-0000-000000000000",
        "variableName": "target_path",
        "type": "String"
      }
    },
    "variables": {
      "targetPath": {
        "type": "String"
      }
    }
  }
}
```

The `SetVariable` activity writes to a pipeline variable, so that variable must exist. Per [Set Variable activity](https://learn.microsoft.com/en-us/fabric/data-factory/set-variable-activity), Set Variable operates on an **existing** pipeline variable, so the pipeline `properties.variables` block must declare `targetPath` (sibling to `activities` and `libraryVariables`). `libraryVariables` binds the Variable Library value; `variables` declares the pipeline-local target that the activity assigns into. Omitting the `variables` declaration makes the activity reference an undeclared variable.


The expression object is required. A bare string such as `"@pipeline().libraryVariables.target_path"` is a literal.

Map Variable Library types to pipeline types as follows:

| Variable Library type | Pipeline type |
|---|---|
| `Boolean` | `Bool` |
| `Integer` | `Int` |
| `Number` | `Double` (definition-level only; not supported in pipelines per Learn) |
| `DateTime` | `String` |
| `String` | `String` |
| `ItemReference` | `String` |

Learn currently says Number types are not supported in some pipeline UI contexts. When authoring by definition, use the documented `Double` mapping from [ITEM-DEFINITIONS-CORE.md - VariableLibrary](../../../common/ITEM-DEFINITIONS-CORE.md#variablelibrary) and tenant-verify before relying on Number in a pipeline.

> **Number is not supported in pipelines per Microsoft Learn** ([Variable library integration with pipelines](https://learn.microsoft.com/en-us/fabric/data-factory/variable-library-integration-with-data-pipelines#known-limitations)). The `Number` to `Double` row is the definition-level mapping only; do not present Number as supported pipeline behavior. If you must experiment, mark it tenant-verify and expect the pipeline to reject it.

## Notebook Contract

NotebookUtils supports two access patterns:

```python
lib = notebookutils.variableLibrary.getLibrary("AppConfig")
target_path = lib.target_path
max_rows = lib.getVariable("max_rows")
```

```python
target_path = notebookutils.variableLibrary.get("$(/**/AppConfig/target_path)")
```

Use exact library and variable names. The `$(/**/LibraryName/VariableName)` path requires the `/**/` prefix. NotebookUtils only reads libraries in the same workspace, and notebooks read the active value set in that workspace.

In the repo-verified behavior (`common/ITEM-DEFINITIONS-CORE.md#variablelibrary`), Boolean values from `getLibrary()` property access come back as the strings `"true"`/`"false"`, not Python booleans, so normalize defensively with `str(value).lower() == "true"` and never use `bool("false")` (every non-empty string is truthy). Microsoft Learn's NotebookUtils page instead describes values as automatically typed, so confirm the exact boolean behavior on your tenant (tenant-verify item).

## Other Consumer Contracts

| Consumer | VL-side contract | Notes |
|---|---|---|
| Lakehouse shortcut | Define variables and value sets first, then assign variables to shortcut properties in the Manage Shortcut UX | Learn states REST API assignment is not supported for shortcuts |
| Dataflow Gen2 | Reference `$(/**/LibraryName/VariableName)` inside `mashup.pq` using `Variable.Value` or `Variable.ValueOrDefault` | Basic types only; same workspace; values are read at run start |
| Copy Job | Parameterize source or destination connection IDs with Variable Library values, then activate the right value set per workspace | Copy Job docs describe UI selection and stage-specific active values |
| User Data Functions | Add a Variable Library connection, decorate the function with `@udf.connection`, and read through `fn.FabricVariablesClient.getVariables()` | Connection alias comes from the UDF item connection |
| Apache Airflow jobs | Select the library variables in the job's **Environment configuration** (Library variables); DAGs read them through the standard Airflow `Variable.get("<variable_name>")` API | Values do not auto-refresh: use **Sync Library variables** after the source library changes |
| Plan | Learn lists Plan as a supported consumer, but the public Plan overview does not document a code-level reference syntax | Reference syntax is undocumented, so tenant-verify before relying on it |

Dataflow Gen2 example:

```m
Variable.ValueOrDefault("$(/**/AppConfig/target_path)", "Files/dev")
```

User Data Functions example:

```python
import fabric.functions as fn

udf = fn.UserDataFunctions()

@udf.connection(argName="varLib", alias="<AppConfig alias>")
@udf.function()
def get_target_path(varLib: fn.FabricVariablesClient) -> str:
    variables = varLib.getVariables()
    return variables.get("target_path")
```

The execution context object must be named `udf` (`udf = fn.UserDataFunctions()`), so the
decorators are `@udf.connection` / `@udf.function`. Do not substitute the Azure Functions
`app = fn.App(...)` / `@app.connection` shape, it is a different SDK and does not exist here.

ConnectionReference variables are documented for Notebook and User Data Functions. The authoring shape is covered in [authoring.md - Variable Types](authoring.md#variable-types). Tenant-verify before using them in other consumers.

## Troubleshooting (consumption)

| Symptom | Likely cause | Fix |
|---|---|---|
| Pipeline expression shows literal text | Used a bare string instead of a pipeline expression object | Use `{ "value": "@pipeline().libraryVariables.x", "type": "Expression" }` |
| Pipeline variable type error | Used Variable Library type names directly where pipeline type names are required | Map Boolean to Bool, Integer to Int; Number maps to Double at definition level only (Learn: Number is not supported in pipelines, verify on tenant) |
| Notebook Boolean logic is wrong | Boolean value was returned as string `"false"` and converted with `bool()` | Compare strings with `.lower() == "true"` when values are strings |
