# Power BI Project file (PBIP)

Power BI Project (PBIP) is the code-behind of a Power BI development. 

It can include a Semantic Model + Report or just a Report (live connect).

**PBIP Folder with both Semantic Model and Report folder:**

```text
PBIPFolder/
├── [Name].SemanticModel/
|   ├── /definition # The semantic model definition using TMDL language [REQUIRED]
|   ├── definition.pbism # The semantic model definition file [REQUIRED]
|   ├── * # Other semantic model metadata files and folders
├── [Name].Report/        
|   ├── /definition # The report definition using PBIR format
|   ├── definition.pbir # The report definition file with a byPath relative reference to the semantic model folder. [REQUIRED]
|   ├── * # Other report metadata files and folders
└── [Name].pbip # A shortcut file to the report folder
```    

**PBIP Folder with Report folder:**

```text
PBIPFolder/
├── [Name].Report/        
|   ├── /definition # The report definition using PBIR format
|   ├──  definition.pbir # The report definition file with a byConnection reference to a semantic model in a Workspace. [REQUIRED]
|   ├── * # Other report metadata files and folders
└── [Name].pbip # A shortcut file to the report folder
```   

## definition.pbism file

No modifications are needed—just create the file exactly as shown in the example.

```json
{
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
    "version": "4.2",
    "settings": {
        "qnaEnabled": true
    }
}
```
Refer to [JSON Schema](https://github.com/microsoft/json-schemas/blob/main/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json) for more details.

## definition.pbir

Overall definition of the report and core settings. Also holds the reference to the semantic model of the report, it's possible to rebind the report to a different semantic model by updating this file.

This file can be opened by Power BI Desktop.

Example of `definition.pbir` file targeting a local semantic model folder:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
  "version": "4.0",
  "datasetReference": {
    "byPath": {
      "path": "../Sales.SemanticModel"
    }
  }
}
```

Example of `definition.pbir` file targeting a semantic model in a workspace:

```json
{  
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
  "version": "4.0",
  "datasetReference": {
    "byConnection": {      
      "connectionString": "semanticmodelid=[SemanticModelId]"
    }
  }
}
```

Notes:
- Use forward slashes in byPath, only relative paths are supported.
- When using byConnection, Desktop does not open the model in edit mode.

Refer to [JSON Schema](https://github.com/microsoft/json-schemas/blob/main/fabric/item/report/definitionProperties/2.0.0/schema.json) for more details.

## .pbip file

Serves as a shortcut to a Power BI Report. 

Example of a `[name].pbip` file:

```json
{
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
    "version": "1.0",
    "artifacts": [
        {
          "report": {
              "path": "{Name of the Semantic Model}.Report"
          }
        }
    ],
    "settings": {
        "enableAutoRecovery": true
    }
}
```

Refer to [JSON Schema](https://github.com/microsoft/json-schemas/blob/main/fabric/pbip/pbipProperties/1.0.0/schema.json) for more details.

## References

**External references** (request markdown when possible):

- [PBIP docs](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
- [PBIP SemanticModel folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset)
- [PBIP Report folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report)