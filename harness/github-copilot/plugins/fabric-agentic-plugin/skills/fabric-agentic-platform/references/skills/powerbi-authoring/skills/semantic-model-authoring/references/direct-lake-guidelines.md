# Direct Lake Modeling Guidelines

## Important

- Direct Lake semantic models main particularity is the use of DirectLake partitions. For regular modeling guidelines make sure to follow the [modeling-guidelines](./modeling-guidelines.md).
- Before creating any Direct Lake table, make sure there is a named expression targeting the OneLake source. 
- ALL Direct Lake table partitions use partition source type `EntityPartitionSource` targeting an entity in OneLake and use the shared named expression with the OneLake data source. Do not attempt to use Power Query expressions in entity based tables. See [partition configuration](#partition-configuration) for configuration details of a Direct Lake mode partition. 
- That expression will be used in the tables partition `expressionSource` property.
- Columns with `dataType` `binary` are not supported. If they exist in the datasource do not include them in the model.
- Direct Lake tables must still declare the tables, but directly mapping to the columns in the OneLake table using the `sourceColumn` property

## Process to create a direct lake model

- Create a named expression for the Direct Lake connection to the OneLake source using the `AzureStorage.DataLake` connector. Do not use the `Sql.Database` unless explicitly asked for.
- Analyze the schema of the tables in OneLake
- Create tables with columns and types matching the OneLake tables and using `EntityPartitionSource` type for the partition.
- If there is a development workspace, deploy to it to test

## Partition Configuration

| Property         | Value                   | Description                               |
| ---------------- | ----------------------- | ----------------------------------------- |
| Source Type      | `EntityPartitionSource` | Not `MPartitionSource` (no M/Power Query) |
| Mode             | `DirectLake`            | Required for Direct Lake partitions       |
| entityName       | String                  | Table name in data source                 |
| schemaName       | String (optional)       | Schema name (if data source supports it)  |
| expressionSource | String                  | Reference to shared named expression      |

**PowerQuery of the OneLake Data Source Named Expression**

Expression name: `DirectLake - [Model Name]`

```powerquery
let
    Source = AzureStorage.DataLake("https://onelake.dfs.fabric.microsoft.com/[WORKSPACE_ID]/[LAKEHOUSE_ID]", [HierarchicalNavigation=true])
in
    Source
```

## TMDL example of a Direct Lake table configuration

```tmdl

expression 'DL_Sales_Named_Expression' =
		let
		    Source = AzureStorage.DataLake("https://onelake.dfs.fabric.microsoft.com/[WORKSPACE_ID]/[LAKEHOUSE_ID]", [HierarchicalNavigation=true])
		in
		    Source	

table Product		

	column 'Product Key'
		dataType: int64
		formatString: 0				
		sourceColumn: product_key		

	column Product
		dataType: string							
		sourceColumn: product

	column Category
		dataType: string					
		summarizeBy: none
		sourceColumn: category

	column UnitPrice
		dataType: decimal							
		summarizeBy: none
		sourceColumn: Unit_Price

	partition partition_name = entity
		mode: directLake
		source
			entityName: Product
			schemaName: dbo
			expressionSource: DL_Sales_Named_Expression
```