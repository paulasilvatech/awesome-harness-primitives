# External Connections — Data Source Access & Credentials from Notebooks

How to connect to external data sources from Fabric Notebook cells using `notebookutils.connections` and `notebookutils.credentials`.

## Connection Pattern

Fabric Notebooks use `notebookutils.connections` to retrieve credentials for configured Fabric connections. The general pattern:

1. Get credentials: `credential = notebookutils.connections.getCredential("{connectionId}")`
2. Extract auth fields (varies by credential type — see below)
3. Connect using standard Python libraries

**Credential types**: `Basic` (username/password), `Key`, `SAS`, `ServicePrincipal`, `WorkspaceIdentity`, `Token`

---

## Credentials & Secrets

### Azure Key Vault (Preferred for Secrets)

```python
# Direct secret retrieval (preferred)
secret = notebookutils.credentials.getSecret("https://{vaultName}.vault.azure.net/", "{secretName}")

# Via connection
secret = notebookutils.connections.getSecretWithConnection("{connectionId}", "{secretName}")
```

### Azure Service Tokens

```python
# Get AAD token for a specific resource
token = notebookutils.credentials.getToken("{resource}")
# Example: token = notebookutils.credentials.getToken("https://storage.azure.com")
```

**Rules:**
- **Never hardcode secrets** — always use `notebookutils.credentials.getSecret()` from Azure Key Vault.
- **Prefer AAD token authentication** for Azure services — use `notebookutils.credentials.getToken()`.
- Configure Fabric connections in the workspace settings before using these patterns.

**Documentation**: [Credentials utilities](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-credentials)

---

## Database Connections

### PostgreSQL

```python
# pip install psycopg2-binary
import psycopg2
cred = notebookutils.connections.getCredential("{connectionId}")
conn = psycopg2.connect(host="{serverName}", database="{databaseName}", user=cred["username"], password=cred["password"])
```

### MySQL

```python
# pip install mysql-connector-python
import mysql.connector
cred = notebookutils.connections.getCredential("{connectionId}")
conn = mysql.connector.connect(host="{serverName}", database="{databaseName}", user=cred["username"], password=cred["password"])
```

### Azure SQL / Azure SQL MI

```python
# pip install pyodbc
import pyodbc
cred = notebookutils.connections.getCredential("{connectionId}")
conn = pyodbc.connect(f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={'{serverName}'};DATABASE={'{databaseName}'};UID={cred['username']};PWD={cred['password']}")
```

---

## Cloud Storage

### Azure Blob Storage / ADLS Gen2

```python
from azure.storage.blob import BlobServiceClient
cred = notebookutils.connections.getCredential("{connectionId}")
client = BlobServiceClient(account_url="https://{accountName}.blob.core.windows.net", credential=cred["key"])
```

### Amazon S3

```python
# pip install boto3
import boto3
cred = notebookutils.connections.getCredential("{connectionId}")
s3 = boto3.client("s3", aws_access_key_id=cred["key"], aws_secret_access_key=cred["secret"])
```

---

## Analytics & NoSQL

### Azure Data Explorer (Kusto)

```python
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
token = notebookutils.credentials.getToken("kusto")
kcsb = KustoConnectionStringBuilder.with_aad_user_token_authentication("{clusterUri}", token)
client = KustoClient(kcsb)
```

### Cosmos DB

```python
from azure.cosmos import CosmosClient
cred = notebookutils.connections.getCredential("{connectionId}")
client = CosmosClient("{accountUri}", credential=cred["key"])
```

---

**Note**: Replace `{connectionId}`, `{serverName}`, `{databaseName}`, etc. with actual values.
