# Connector-Specific Refactoring — Kusto, Cosmos DB, Token Library, ADLS OAuth

Detailed before/after patterns for migrating Synapse connector code to Fabric. These go beyond the general linked-service replacement covered in [connectivity-migration.md](connectivity-migration.md).

> **Pre-check**: Run the [pre-refactoring audit](spark-item-migration.md#pre-refactoring-audit--search-patterns) to find affected notebooks. The search patterns below map to specific connectors.

---

## Azure Data Explorer (Kusto) Connector

**Search pattern**: `kusto.spark.synapse` or `spark.synapse.linkedService.*DataExplorer`

### Reading from Kusto

```python
# ❌ BEFORE — Synapse: Kusto via linked service
kustoDF = (spark.read
    .format("com.microsoft.kusto.spark.synapse.datasource")
    .option("spark.synapse.linkedService", "AzureDataExplorer1")
    .option("kustoCluster", "https://mycluster.kusto.windows.net")
    .option("kustoDatabase", "mydb")
    .option("kustoQuery", "MyTable | take 100")
    .load())

# ✅ AFTER — Fabric: Kusto via access token
kustoDF = (spark.read
    .format("com.microsoft.kusto.spark.synapse.datasource")
    .option("accessToken", notebookutils.credentials.getToken("https://mycluster.kusto.windows.net"))
    .option("kustoCluster", "https://mycluster.kusto.windows.net")
    .option("kustoDatabase", "mydb")
    .option("kustoQuery", "MyTable | take 100")
    .load())
```

### Writing to Kusto

```python
# ❌ BEFORE — Synapse
(df.write
    .format("com.microsoft.kusto.spark.synapse.datasource")
    .option("spark.synapse.linkedService", "AzureDataExplorer1")
    .option("kustoCluster", "https://mycluster.kusto.windows.net")
    .option("kustoDatabase", "mydb")
    .option("kustoTable", "MyTargetTable")
    .option("tableCreateOptions", "CreateIfNotExist")
    .mode("Append")
    .save())

# ✅ AFTER — Fabric
(df.write
    .format("com.microsoft.kusto.spark.synapse.datasource")
    .option("accessToken", notebookutils.credentials.getToken("https://mycluster.kusto.windows.net"))
    .option("kustoCluster", "https://mycluster.kusto.windows.net")
    .option("kustoDatabase", "mydb")
    .option("kustoTable", "MyTargetTable")
    .option("tableCreateOptions", "CreateIfNotExist")
    .mode("Append")
    .save())
```

**Changes**:
1. Remove `.option("spark.synapse.linkedService", "...")`
2. Add `.option("accessToken", notebookutils.credentials.getToken("<cluster_url>"))`
3. All other options (`kustoCluster`, `kustoDatabase`, `kustoQuery`, `kustoTable`) remain unchanged

---

## Cosmos DB Connector (OLTP)

**Search pattern**: `cosmos.oltp` or `spark.synapse.linkedService.*Cosmos` or `getSecretWithLS.*cosmos`

### Reading from Cosmos DB

```python
# ❌ BEFORE — Synapse: Cosmos DB via linked service
cosmosDF = (spark.read
    .format("cosmos.oltp")
    .option("spark.synapse.linkedService", "CosmosDbLS")
    .option("spark.cosmos.container", "mycontainer")
    .option("spark.cosmos.read.inferSchema.enabled", "true")
    .load())

# ✅ AFTER — Fabric: Cosmos DB via Key Vault secret
cosmos_key = notebookutils.credentials.getSecret(
    "https://mykeyvault.vault.azure.net/", "cosmos-account-key"
)

cosmosDF = (spark.read
    .format("cosmos.oltp")
    .option("spark.cosmos.accountEndpoint", "https://mycosmosaccount.documents.azure.com:443/")
    .option("spark.cosmos.accountKey", cosmos_key)
    .option("spark.cosmos.database", "mydb")
    .option("spark.cosmos.container", "mycontainer")
    .option("spark.cosmos.read.inferSchema.enabled", "true")
    .load())
```

### Writing to Cosmos DB

```python
# ❌ BEFORE — Synapse
(df.write
    .format("cosmos.oltp")
    .option("spark.synapse.linkedService", "CosmosDbLS")
    .option("spark.cosmos.container", "mycontainer")
    .option("spark.cosmos.write.strategy", "ItemOverwrite")
    .mode("Append")
    .save())

# ✅ AFTER — Fabric
cosmos_key = notebookutils.credentials.getSecret(
    "https://mykeyvault.vault.azure.net/", "cosmos-account-key"
)

(df.write
    .format("cosmos.oltp")
    .option("spark.cosmos.accountEndpoint", "https://mycosmosaccount.documents.azure.com:443/")
    .option("spark.cosmos.accountKey", cosmos_key)
    .option("spark.cosmos.database", "mydb")
    .option("spark.cosmos.container", "mycontainer")
    .option("spark.cosmos.write.strategy", "ItemOverwrite")
    .mode("Append")
    .save())
```

**Changes**:
1. Remove `.option("spark.synapse.linkedService", "...")`
2. Add `.option("spark.cosmos.accountEndpoint", "...")`
3. Retrieve account key from Key Vault: `notebookutils.credentials.getSecret(vaultUrl, secretName)`
4. Add `.option("spark.cosmos.accountKey", cosmos_key)`
5. Add `.option("spark.cosmos.database", "...")` — linked service auto-resolved this; now explicit

> **Cosmos DB analytics connector** (`azure-cosmos-analytics-spark`): This JAR is missing from Fabric Runtime 1.3. If your SJDs use `com.azure.cosmos.spark` with the analytics store, upload the JAR to your Fabric Environment. See [library-compatibility.md](library-compatibility.md).

---

## Cosmos DB Connector — Spark Config Style

Some notebooks set Cosmos DB connection at the Spark config level rather than per-read/write:

```python
# ❌ BEFORE — Synapse: Spark config with linked service
spark.conf.set("spark.cosmos.linkedService", "CosmosDbLS")
spark.conf.set("spark.cosmos.container", "events")

df = spark.read.format("cosmos.oltp").load()

# ✅ AFTER — Fabric: Spark config with direct credentials
cosmos_key = notebookutils.credentials.getSecret(
    "https://mykeyvault.vault.azure.net/", "cosmos-account-key"
)
spark.conf.set("spark.cosmos.accountEndpoint", "https://mycosmosaccount.documents.azure.com:443/")
spark.conf.set("spark.cosmos.accountKey", cosmos_key)
spark.conf.set("spark.cosmos.database", "mydb")
spark.conf.set("spark.cosmos.container", "events")

df = spark.read.format("cosmos.oltp").load()
```

---

## ADLS Gen2 OAuth — LinkedServiceBasedTokenProvider → ClientCredsTokenProvider

**Search pattern**: `LinkedServiceBasedTokenProvider` or `spark.storage.synapse` or `getPropertiesAsMap`

This is the most common pattern for ADLS Gen2 access using a service principal through a Synapse linked service.

### Python

```python
# ❌ BEFORE — Synapse: OAuth via linked service token provider
spark.conf.set("spark.storage.synapse.linkedServiceName", "MyADLSLinkedService")
spark.conf.set(
    "fs.azure.account.oauth.provider.type.mystorageaccount.dfs.core.windows.net",
    "com.microsoft.azure.synapse.tokenlibrary.LinkedServiceBasedTokenProvider"
)

df = spark.read.parquet("abfss://container@mystorageaccount.dfs.core.windows.net/data/")

# ✅ AFTER — Fabric: OAuth via standard ClientCredsTokenProvider
storage_account = "mystorageaccount"
client_id = notebookutils.credentials.getSecret("https://mykeyvault.vault.azure.net/", "sp-client-id")
client_secret = notebookutils.credentials.getSecret("https://mykeyvault.vault.azure.net/", "sp-client-secret")
tenant_id = notebookutils.credentials.getSecret("https://mykeyvault.vault.azure.net/", "tenant-id")

spark.conf.set(f"fs.azure.account.auth.type.{storage_account}.dfs.core.windows.net", "OAuth")
spark.conf.set(f"fs.azure.account.oauth.provider.type.{storage_account}.dfs.core.windows.net",
               "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set(f"fs.azure.account.oauth2.client.id.{storage_account}.dfs.core.windows.net", client_id)
spark.conf.set(f"fs.azure.account.oauth2.client.secret.{storage_account}.dfs.core.windows.net", client_secret)
spark.conf.set(f"fs.azure.account.oauth2.client.endpoint.{storage_account}.dfs.core.windows.net",
               f"https://login.microsoftonline.com/{tenant_id}/oauth2/token")

df = spark.read.parquet(f"abfss://container@{storage_account}.dfs.core.windows.net/data/")
```

### Scala

```scala
// ❌ BEFORE — Synapse (Scala): linked service token provider
val linked_service_cfg = "MyADLSLinkedService"
val conexion = TokenLibrary.getPropertiesAsMap(linked_service_cfg)
val my_account = conexion("Endpoint").toString.substring(8)

spark.conf.set(s"fs.azure.account.oauth.provider.type.${my_account}.dfs.core.windows.net",
  "com.microsoft.azure.synapse.tokenlibrary.LinkedServiceBasedTokenProvider")
spark.conf.set("spark.storage.synapse.linkedServiceName", linked_service_cfg)

// ✅ AFTER — Fabric (Scala): standard OAuth
val storageAccount = "mystorageaccount"
val clientId = notebookutils.credentials.getSecret("https://mykeyvault.vault.azure.net/", "sp-client-id")
val clientSecret = notebookutils.credentials.getSecret("https://mykeyvault.vault.azure.net/", "sp-client-secret")
val tenantId = notebookutils.credentials.getSecret("https://mykeyvault.vault.azure.net/", "tenant-id")

spark.conf.set(s"fs.azure.account.auth.type.${storageAccount}.dfs.core.windows.net", "OAuth")
spark.conf.set(s"fs.azure.account.oauth.provider.type.${storageAccount}.dfs.core.windows.net",
  "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set(s"fs.azure.account.oauth2.client.id.${storageAccount}.dfs.core.windows.net", clientId)
spark.conf.set(s"fs.azure.account.oauth2.client.secret.${storageAccount}.dfs.core.windows.net", clientSecret)
spark.conf.set(s"fs.azure.account.oauth2.client.endpoint.${storageAccount}.dfs.core.windows.net",
  s"https://login.microsoftonline.com/${tenantId}/oauth2/token")
```

**Changes**:
1. Remove `spark.storage.synapse.linkedServiceName` — not supported in Fabric
2. Remove `TokenLibrary.getPropertiesAsMap()` — not available in Fabric
3. Replace `LinkedServiceBasedTokenProvider` with `ClientCredsTokenProvider`
4. Configure `client.id`, `client.secret`, `client.endpoint` per storage account
5. Store credentials in Key Vault; retrieve via `notebookutils.credentials.getSecret()`

> **Preferred alternative**: If the ADLS Gen2 data only needs to be read, create an **OneLake Shortcut** instead. This eliminates OAuth config entirely — the shortcut handles authentication. See [connectivity-migration.md](connectivity-migration.md).

---

## Token Library (Synapse-only)

**Search pattern**: `TokenLibrary` or `getPropertiesAsMap`

Synapse's `TokenLibrary` provides two capabilities, both replaced differently:

### Token Acquisition

```python
# ❌ BEFORE — Synapse: get access token via linked service
token = TokenLibrary.getAccessToken("https://database.windows.net/")

# ✅ AFTER — Fabric: use notebookutils
token = notebookutils.credentials.getToken("https://database.windows.net/")
```

### Linked Service Property Extraction

```scala
// ❌ BEFORE — Synapse: extract linked service properties
val props = TokenLibrary.getPropertiesAsMap("MyLinkedService")
val endpoint = props("Endpoint")
val accountName = endpoint.toString.substring(8)

// ✅ AFTER — Fabric: no linked services — hardcode or parameterize
val accountName = "mystorageaccount"  // or read from notebook parameters
// If dynamic, store in Key Vault:
// val accountName = notebookutils.credentials.getSecret("https://myvault.vault.azure.net/", "storage-account-name")
```

### Secret Retrieval via Linked Service

```python
# ❌ BEFORE — Synapse: get secret via Key Vault linked service
secret = mssparkutils.credentials.getSecretWithLS("MyKeyVaultLS", "my-secret-name")
# or
secret = TokenLibrary.getSecret("MyKeyVaultLinkedService", "my-secret-name")

# ✅ AFTER — Fabric: reference Key Vault URL directly (no linked service)
secret = notebookutils.credentials.getSecret(
    "https://mykeyvault.vault.azure.net/",
    "my-secret-name"
)
```

**Key change**: In Fabric, `getSecret()` takes the **full Key Vault URL** as the first parameter, not a linked service name. The Key Vault must have an access policy granting your Fabric workspace identity `Get` permission on secrets.

---

## `spark.read.synapsesql()` — Synapse SQL Connector

**Search pattern**: `synapsesql`

This Synapse-specific connector reads from Dedicated SQL Pool. It has no Fabric equivalent.

```python
# ❌ BEFORE — Synapse: read from Dedicated SQL Pool
df = spark.read.synapsesql("mypool.dbo.FactSales")

# ✅ AFTER (Option A) — Fabric: read from migrated Lakehouse Delta table
df = spark.read.format("delta").load("Tables/FactSales")

# ✅ AFTER (Option B) — Fabric: read from Fabric Warehouse via JDBC
token = notebookutils.credentials.getToken("https://database.windows.net/")
jdbc_url = "jdbc:sqlserver://mywarehouse-endpoint.datawarehouse.fabric.microsoft.com:1433;database=mywarehouse"

df = (spark.read
    .format("jdbc")
    .option("url", jdbc_url)
    .option("accessToken", token)
    .option("dbtable", "dbo.FactSales")
    .load())
```

**Decision guide**:
- **Data migrated to Lakehouse** (most common): Use Option A — direct Delta read, fastest
- **Data in Fabric Warehouse**: Use Option B — JDBC with Entra ID token

---

## Connector Refactoring Checklist

| Search Pattern | Connector | What Changes |
|---|---|---|
| `spark.synapse.linkedService.*DataExplorer` | Kusto/ADX | Replace linked service with `accessToken` via `getToken()` |
| `spark.synapse.linkedService.*Cosmos` | Cosmos DB | Replace linked service with `accountEndpoint` + `accountKey` from Key Vault |
| `cosmos.oltp` + `getSecretWithLS` | Cosmos DB | Replace `getSecretWithLS()` with `getSecret(vaultUrl, name)` |
| `LinkedServiceBasedTokenProvider` | ADLS Gen2 OAuth | Replace with `ClientCredsTokenProvider` + SP creds from Key Vault |
| `spark.storage.synapse.linkedServiceName` | ADLS Gen2 | Remove entirely — not supported in Fabric |
| `TokenLibrary.getPropertiesAsMap` | Any linked service | Remove; hardcode or parameterize values |
| `TokenLibrary.getSecret` | Key Vault | Replace with `notebookutils.credentials.getSecret(vaultUrl, name)` |
| `getSecretWithLS` | Key Vault | Replace with `getSecret(vaultUrl, name)` — use full vault URL |
| `synapsesql` | Dedicated SQL Pool | Replace with Delta read or JDBC with `accessToken` |

> **DMTS note**: DMTS Connections (Data Management Trusted Service) are supported in Fabric **notebooks only** — not yet in Spark Job Definitions. If your SJD code uses DMTS, refactor to direct endpoint authentication.
