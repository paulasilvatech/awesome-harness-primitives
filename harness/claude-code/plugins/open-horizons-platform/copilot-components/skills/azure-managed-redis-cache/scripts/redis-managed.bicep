// Azure Managed Redis (Microsoft.Cache/redisEnterprise) sample.
//
// Azure Cache for Redis Enterprise is retired for NEW creations; this template
// provisions an Azure Managed Redis cluster and database. The resource type is
// still Microsoft.Cache/redisEnterprise. Verify the latest API version and the
// available SKU names on Microsoft Learn before deploying.
//
// Best practice: prefer Microsoft Entra (AAD) authentication with a managed
// identity over access keys, set publicNetworkAccess explicitly, and require TLS.

@description('Name of the Azure Managed Redis cluster.')
param name string

@description('Azure region for the cluster.')
param location string = resourceGroup().location

@description('Managed Redis SKU. Examples: Balanced_B1, Balanced_B3, MemoryOptimized_M10, ComputeOptimized_X10, FlashOptimized_A250. Verify current names on Microsoft Learn.')
param sku string = 'Balanced_B1'

@description('Whether the cluster is reachable from public networks. Set to Disabled and add a private endpoint for sensitive data.')
@allowed([
  'Enabled'
  'Disabled'
])
param publicNetworkAccess string = 'Enabled'

@description('Minimum TLS version for client connections.')
param minimumTlsVersion string = '1.2'

resource cluster 'Microsoft.Cache/redisEnterprise@2025-07-01' = {
  name: name
  location: location
  sku: {
    name: sku
  }
  properties: {
    minimumTlsVersion: minimumTlsVersion
    // publicNetworkAccess is a required property on Azure Managed Redis.
    // Harden to 'Disabled' with a private endpoint for production sensitive data.
    publicNetworkAccess: publicNetworkAccess
  }
}

resource database 'Microsoft.Cache/redisEnterprise/databases@2025-07-01' = {
  parent: cluster
  name: 'default'
  properties: {
    clientProtocol: 'Encrypted'
    clusteringPolicy: 'EnterpriseCluster'
    evictionPolicy: 'NoEviction'
    // Enable the modules you need. RediSearch powers vector search for the
    // semantic cache and vector memory patterns.
    modules: [
      {
        name: 'RediSearch'
      }
    ]
    // Prefer Microsoft Entra (AAD) authentication. Configure access policy
    // assignments for your managed identity after deployment, and avoid keys.
  }
}

@description('The Redis host name to connect to.')
output hostName string = cluster.properties.hostName
