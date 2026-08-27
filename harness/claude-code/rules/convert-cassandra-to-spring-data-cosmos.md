---
paths:
  - "**/*.java"
  - "**/pom.xml"
  - "**/build.gradle"
  - "**/application*.properties"
  - "**/application*.yml"
  - "**/application*.conf"
---

<!-- Generated from harness/github-copilot/instructions/convert-cassandra-to-spring-data-cosmos.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces conventions for converting Spring Boot Cassandra data access to Azure Cosmos DB with Spring Data Cosmos, including dependencies, configuration, repositories, entities, tests, and verification.

# Cassandra to Spring Data Cosmos Conventions — Spring Boot Code Migration

This file applies to Spring Boot applications that are moving Java code from Spring Data Cassandra, Cassandra DAOs, or DataStax drivers to Azure Cosmos DB with Spring Data Cosmos. It is authoritative for dependency changes, entity annotations, repository shapes, reactive service signatures, ID conversion, configuration, authentication, local verification, spring-data-cosmos usage, and known Cassandra-to-Cosmos failure modes in the matched files; project-specific architecture, data migration runbooks, and cloud provisioning instructions win where they define stricter environment or deployment rules.

## Applicability

The former Step-by-step guide content is preserved as passive rules for code migration, not as a step-by-step runbook.

This guide applies to:
- Spring Boot 2.x - 3.x applications (both reactive and non-reactive)
- Maven and Gradle-based projects
- Applications using Spring Data Cassandra, Cassandra DAOs, or DataStax drivers
- Projects with or without Lombok
- UUID-based or String-based entity identifiers
- Both synchronous and reactive (Spring WebFlux) applications

This guide does NOT cover:
- Non-Spring frameworks (Jakarta EE, Micronaut, Quarkus, plain Java)
- Complex Cassandra features (materialized views, UDTs, counters, custom types)
- Bulk data migration (code conversion only - data must be migrated separately)
- Cassandra-specific features like lightweight transactions (LWT) or batch operations across partitions

## Migration Posture

These conventions cover conversion of reactive Spring Boot applications from Apache Cassandra to Azure Cosmos DB using Spring Data Cosmos, including major issues and solutions observed in real-world conversion work.

## Runtime and Tooling Requirements

- Java 11 or higher (Java 17+ required for Spring Boot 3.x)
- Azure CLI installed and authenticated (`az login`) for local development
- Azure Cosmos DB account created in Azure Portal
- Maven 3.6+ or Gradle 6+ (depending on your project)
- For Gradle projects with Spring Boot 3.x: Ensure JAVA_HOME environment variable points to Java 17+
- Basic understanding of your application's data model and query patterns

## Cosmos DB Database and Container Setup

**CRITICAL**: Before running your application, ensure the database exists in your Cosmos DB account.

### Option 1: Manual Database Creation (Recommended for first run)
1. Go to Azure Portal → Your Cosmos DB account
2. Navigate to "Data Explorer"
3. Click "New Database"
4. Enter the database name matching your application configuration (check `application.properties` or `application.yml` for the configured database name)
5. Choose throughput settings (Manual or Autoscale based on your needs)
   - Start with Manual 400 RU/s for development/testing
   - Use Autoscale for production workloads with variable traffic
6. Click OK

### Option 2: Automatic Creation
Spring Data Cosmos can auto-create the database on first connection, but this requires:
- Proper RBAC permissions (Cosmos DB Built-in Data Contributor role)
- May fail if permissions are insufficient

### Container (Collection) Creation
Containers will be auto-created by Spring Data Cosmos when the application starts, using the `@Container` annotation settings from your entities. No manual container creation is needed unless you want to configure specific throughput or indexing policies.

## Cosmos DB Authentication

### Using DefaultAzureCredential (Recommended)
The `DefaultAzureCredential` authentication method is the recommended approach for both development and production:

**How it works**:
1. Tries multiple credential sources in order:
   - Environment variables
   - Workload Identity (for AKS)
   - Managed Identity (for Azure VMs/App Service)
   - Azure CLI (`az login`)
   - Azure PowerShell
   - Azure Developer CLI

**Setup for local development**:
```bash
# Login via Azure CLI
az login

# The application will automatically use your CLI credentials
```

**Configuration** (no key required):
```java
@Bean
public CosmosClientBuilder getCosmosClientBuilder() {
    return new CosmosClientBuilder()
        .endpoint(uri)
        .credential(new DefaultAzureCredentialBuilder().build());
}
```

**Properties file** (application-cosmos.properties or application.properties):
```properties
azure.cosmos.uri=https://<your-cosmos-account-name>.documents.azure.com:443/
azure.cosmos.database=<your-database-name>
# No key property needed when using DefaultAzureCredential
azure.cosmos.populate-query-metrics=false
```

**Note**: Replace `<your-cosmos-account-name>` and `<your-database-name>` with your actual values.

### RBAC Permissions Required
When using DefaultAzureCredential, your Azure identity needs appropriate RBAC permissions:

**Common startup error**:
```
Request blocked by Auth: Request for Read DatabaseAccount is blocked because principal
[xxx] does not have required RBAC permissions to perform action
[Microsoft.DocumentDB/databaseAccounts/sqlDatabases/write] on any scope.
```

**Solution**: Assign the "Cosmos DB Built-in Data Contributor" role:
```bash
# Get your user's object ID
PRINCIPAL_ID=$(az ad signed-in-user show --query id -o tsv)

# Assign the role (replace <resource-group> with your actual resource group)
az cosmosdb sql role assignment create \
  --account-name your-cosmos-account \
  --resource-group <resource-group> \
  --scope "/" \
  --principal-id $PRINCIPAL_ID \
  --role-definition-name "Cosmos DB Built-in Data Contributor"
```

**Alternative**: If you're logged in with `az login`, your account should already have permissions if you're the owner/contributor of the Cosmos DB account.

### Key-Based Authentication (Local Emulator Only)
Only use key-based authentication for local emulator development:

```java
@Bean
public CosmosClientBuilder getCosmosClientBuilder() {
    // Only for local emulator
    if (key != null && !key.isEmpty()) {
        return new CosmosClientBuilder()
            .endpoint(uri)
            .key(key);
    }
    // Production: use DefaultAzureCredential
    return new CosmosClientBuilder()
        .endpoint(uri)
        .credential(new DefaultAzureCredentialBuilder().build());
}
```

## Known Compatibility and Refactoring Rules

### Java Version Requirements (Spring Boot 3.x)
**Problem**: Spring Boot 3.0+ requires Java 17 or higher. Using Java 11 causes build failures.
**Error**:
```
No matching variant of org.springframework.boot:spring-boot-gradle-plugin:3.0.5 was found.
Incompatible because this component declares a component compatible with Java 17
and the consumer needed a component compatible with Java 11
```

**Solution**:
```bash
# Check Java version
java -version

# Set JAVA_HOME to Java 17+
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64  # Linux
# or
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home  # macOS

# Verify
echo $JAVA_HOME
```

**For Gradle projects**, always run with correct JAVA_HOME:
```bash
export JAVA_HOME=/path/to/java-17
./gradlew clean build
./gradlew bootRun
```

### Gradle-Specific Issues

#### Issue 1: Old Configuration File Conflicts
**Problem**: When renaming or replacing Cassandra configuration files, the old file may still exist, causing compilation errors:
```
error: class CosmosConfiguration is public, should be declared in a file named CosmosConfiguration.java
```

**Solution**: Explicitly delete the old Cassandra configuration file(s):
```bash
# Find and remove old Cassandra config files
find src/main/java -name "*CassandraConfig*.java" -o -name "*CassandraConfiguration*.java"
# Review the output, then delete if appropriate
rm src/main/java/<path-to-old-config>/CassandraConfig.java
```

#### Issue 2: Repository findAllById Returns Iterable
**Problem**: CosmosRepository's `findAllById()` returns `Iterable<Entity>`, not `List<Entity>`. Calling `.stream()` directly fails:
```
error: cannot find symbol
  symbol:   method stream()
  location: interface Iterable<YourEntity>
```

**Solution**: Handle Iterable properly:
```java
// WRONG - Iterable doesn't have stream() method
var entities = repository.findAllById(ids).stream()...

// CORRECT - Option 1: Use forEach to populate a collection
Iterable<YourEntity> entitiesIterable = repository.findAllById(ids);
Map<String, YourEntity> entityMap = new HashMap<>();
entitiesIterable.forEach(entity -> entityMap.put(entity.getId(), entity));

// CORRECT - Option 2: Convert to List first
List<YourEntity> entities = new ArrayList<>();
repository.findAllById(ids).forEach(entities::add);

// CORRECT - Option 3: Use StreamSupport (Java 8+)
List<YourEntity> entities = StreamSupport.stream(
    repository.findAllById(ids).spliterator(), false)
    .collect(Collectors.toList());
```

### package-info.java javax.annotation Issues
**Problem**: `package-info.java` using `javax.annotation.ParametersAreNonnullByDefault` causes compilation errors in Java 11+:
```
error: cannot find symbol
import javax.annotation.ParametersAreNonnullByDefault;
```

**Solution**: Remove or simplify the package-info.java file:
```java
// Simple version - just package declaration
package com.your.package;
```

### Entity Constructor Issues
**Problem**: Using Lombok `@NoArgsConstructor` with manual constructors causes duplicate constructor compilation errors.
**Solution**: Choose one approach:
- Option 1: Remove `@NoArgsConstructor` and keep manual constructors
- Option 2: Remove manual constructors and rely on Lombok annotations
- **Best Practice**: For Cosmos entities with initialization logic (like setting partition keys), remove `@NoArgsConstructor` and use manual constructors only.

### Business Object Constructor Removal
**Problem**: Removing `@AllArgsConstructor` or custom constructors from entity classes breaks existing code that uses those constructors.
**Impact**: Mapping utilities, data seeders, and test files will fail to compile.
**Solution**:
- After removing or modifying constructors, search ALL files for constructor calls to those entities
- Replace with default constructor + setter pattern:
  ```java
  // Before - using all-args constructor
  MyEntity entity = new MyEntity(id, field1, field2, field3);

  // After - using default constructor + setters
  MyEntity entity = new MyEntity();
  entity.setId(id);
  entity.setField1(field1);
  entity.setField2(field2);
  entity.setField3(field3);
  ```
### Data Seeder Constructor Calls
**Problem**: Data seeding or initialization code uses entity constructors that may not exist after entity conversion to Cosmos annotations.
**Solution**: Update all entity instantiations in data seeding components to use setters:
```java
// Before - constructor-based initialization
MyEntity entity1 = new MyEntity("entity-1", "value1", "value2");

// After - setter-based initialization
MyEntity entity1 = new MyEntity();
entity1.setId("entity-1");
entity1.setField1("value1");
entity1.setField2("value2");
```

**Common files to check**: DataSeeder, DatabaseInitializer, TestDataLoader, or any `@Component` implementing `CommandLineRunner`
```java
OwnerEntity owner1 = new OwnerEntity();
owner1.setId("owner-1");
```

### Test File Updates Required
**Problem**: Test files reference old Cassandra DAOs and use UUID constructors.
**Critical Files to Update**:
1. Remove `MockReactiveResultSet.java` (Cassandra-specific)
2. Update `*ReactiveServicesTest.java` - replace DAO references with Cosmos repositories
3. Update `*ReactiveControllerTest.java` - replace DAO references with Cosmos repositories
4. Replace all `UUID.fromString()` with String IDs
5. Replace constructor calls: `new Owner(UUID.fromString(...))` with setter pattern

### Application Startup and DefaultAzureCredential Behavior
**Important**: DefaultAzureCredential tries multiple authentication methods in sequence, which is normal and expected.

**Expected startup log pattern**:
```
INFO c.azure.identity.ChainedTokenCredential : Azure Identity => Attempted credential EnvironmentCredential is unavailable.
INFO c.azure.identity.ChainedTokenCredential : Azure Identity => Attempted credential WorkloadIdentityCredential is unavailable.
INFO c.azure.identity.ChainedTokenCredential : Azure Identity => Attempted credential ManagedIdentityCredential is unavailable.
INFO c.azure.identity.ChainedTokenCredential : Azure Identity => Attempted credential SharedTokenCacheCredential is unavailable.
INFO c.azure.identity.ChainedTokenCredential : Azure Identity => Attempted credential IntelliJCredential is unavailable.
INFO c.azure.identity.ChainedTokenCredential : Azure Identity => Attempted credential AzureCliCredential is unavailable.
INFO c.azure.identity.ChainedTokenCredential : Azure Identity => Attempted credential AzurePowerShellCredential is unavailable.
INFO c.azure.identity.ChainedTokenCredential : Azure Identity => Attempted credential AzureDeveloperCliCredential returns a token
```

**Key points**:
- The "unavailable" messages are **NORMAL** - it's trying each credential source in order
- Once it finds one that works (e.g., AzureCliCredential or AzureDeveloperCliCredential), it will use that
- **Do not interrupt the startup process** - it takes 10-15 seconds to cycle through credential sources
- Application typically takes 30-60 seconds total to fully start and connect to Cosmos DB

**Success indicators**:
```
INFO c.a.c.i.RxDocumentClientImpl : Initializing DocumentClient [1] with serviceEndpoint [https://<your-account>.documents.azure.com:443/]
INFO c.a.c.i.GlobalEndpointManager : db account retrieved {...}
INFO c.a.c.implementation.SessionContainer : Registering a new collection resourceId [...]
INFO o.s.b.w.embedded.tomcat.TomcatWebServer : Tomcat started on port(s): 8944 (http)
INFO com.your.app.Application : Started Application in X.XXX seconds
```

**Troubleshooting startup failures**:

1. **If all credentials are "unavailable"**:
   ```bash
   # Re-authenticate with Azure CLI
   az login

   # Verify login
   az account show
   ```

2. **If you see permission errors**:
   ```
   Request blocked by Auth: principal [xxx] does not have required RBAC permissions
   ```
   - Ensure database exists in Cosmos DB account (see Database Setup section)
   - Verify RBAC permissions (see Authentication section)
   - Check that you're logged into the correct Azure subscription

3. **Port already in use**:
   ```bash
   # Find and kill the process
   lsof -ti:8944 | xargs kill -9

   # Or change the port in application.properties
   server.port=8945
   ```

### Application Startup Patience
**Problem**: Application takes 30-60 seconds to fully start (compilation + Spring Boot + Cosmos DB connection).
**Solution**:
- For Gradle: `./gradlew bootRun` (runs in foreground by default)
- For Maven: `mvn spring-boot:run`
- Use background execution if needed: `nohup ./gradlew bootRun > app.log 2>&1 &`
- **CRITICAL**: Do not interrupt the startup process, especially during credential authentication (10-15 seconds)
- Monitor logs: `tail -f app.log` or check for "Started Application" message
- Wait for Tomcat to start and show the port number before testing endpoints

### Port Configuration
**Problem**: Application may not run on default port 8080.
**Solution**:
- Check actual port: `ss -tlnp | grep java`
- Test connectivity: `curl http://localhost:<port>/petclinic/api/owners`
- Common ports: 8080, 9966, 9967

## Compilation Hygiene

Cassandra-to-Cosmos conversions commonly produce many compilation errors. Keep these compilation conventions in force until the count reaches zero:

### Residual Cassandra Files
**Problem**: Old Cassandra-specific files cause compilation errors after dependencies are removed.
**Solution**: Delete all Cassandra-specific files systematically:

```bash
# Identify and delete old DAOs
find . -name "*Dao.java" -o -name "*DAO.java"
# Delete: OwnerReactiveDao, PetReactiveDao, VetReactiveDao, VisitReactiveDao

# Identify and delete Cassandra mappers
find . -name "*Mapper.java" -o -name "*EntityToOwnerMapper.java"
# Delete: EntityToOwnerMapper, EntityToPetMapper, EntityToVetMapper, EntityToVisitMapper

# Identify and delete old configuration
find . -name "*CassandraConfig.java" -o -name "CassandraConfiguration.java"
# Delete: CassandraConfiguration.java

# Identify test utilities for Cassandra
find . -name "MockReactiveResultSet.java"
# Delete: MockReactiveResultSet.java (Cassandra-specific test utility)
```

### Incremental Compilation Checks
Compile after each major change so remaining issues stay visible:

```bash
# After deleting old files
mvn compile 2>&1 | grep -E "(ERROR|error)" | wc -l
# Expected: Number decreases with each fix

# After updating entity constructors
mvn compile 2>&1 | grep "constructor"
# Identify constructor-related compilation errors

# After fixing business object constructors
mvn compile 2>&1 | grep -E "(new Owner|new Pet|new Vet|new Visit)"
# Identify remaining constructor calls that need fixing
```

### Constructor-Related Errors
Search for constructor calls in specific file types:

```bash
# Find all constructor calls in MappingUtils
grep -n "new Owner\|new Pet\|new Vet\|new Visit" src/main/java/**/MappingUtils.java

# Find all constructor calls in DataSeeder
grep -n "new OwnerEntity\|new PetEntity\|new VetEntity\|new VisitEntity" src/main/java/**/DataSeeder.java

# Find all constructor calls in test files
grep -rn "new Owner\|new Pet\|new Vet\|new Visit" src/test/java/
```

### Test Update Order
**Rationale**: Application code stays the first repair target so test-only failures are easier to isolate:

1. First: Update test repository mocks (DAO → Cosmos Repository)
2. Second: Fix UUID → String conversions in test data
3. Third: Update constructor calls in test setup
4. Finally: Run tests to verify: `mvn test`

### Zero-Error Verification
**Final Check**:
```bash
# Clean and full compile
mvn clean compile

# Should see: BUILD SUCCESS
# Should NOT see any ERROR messages

# Verify test compilation
mvn test-compile

# Run tests
mvn test
```

**Success Indicators**:
- `mvn compile`: BUILD SUCCESS
- `mvn test`: All tests pass (even if some are skipped)
- No ERROR messages in output
- No "cannot find symbol" errors
- No "constructor cannot be applied" errors

## Code Conversion Conventions

### Maven Dependencies

#### Remove Cassandra Dependencies
```xml
<!-- REMOVE these Cassandra dependencies -->
<dependency>
    <groupId>com.datastax.oss</groupId>
    <artifactId>java-driver-core</artifactId>
</dependency>
<dependency>
    <groupId>com.datastax.oss</groupId>
    <artifactId>java-driver-query-builder</artifactId>
</dependency>
```

#### Add Azure Cosmos Dependencies
```xml
<!-- Azure Spring Data Cosmos (Java 11 compatible) -->
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-spring-data-cosmos</artifactId>
    <version>3.46.0</version>
</dependency>

<!-- Azure Identity for DefaultAzureCredential authentication -->
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
    <version>1.11.4</version>
</dependency>
```

#### Critical: Add Version Management for Compatibility
Spring Boot 2.3.x has version conflicts with Azure libraries. Add this to your `<dependencyManagement>` section:

```xml
<dependencyManagement>
    <dependencies>
        <!-- Override reactor-netty version to fix compatibility with azure-spring-data-cosmos -->
        <dependency>
            <groupId>io.projectreactor.netty</groupId>
            <artifactId>reactor-netty</artifactId>
            <version>1.0.40</version>
        </dependency>
        <dependency>
            <groupId>io.projectreactor.netty</groupId>
            <artifactId>reactor-netty-http</artifactId>
            <version>1.0.40</version>
        </dependency>
        <dependency>
            <groupId>io.projectreactor.netty</groupId>
            <artifactId>reactor-netty-core</artifactId>
            <version>1.0.40</version>
        </dependency>

        <!-- Override reactor-core version to support Sinks API required by azure-identity -->
        <dependency>
            <groupId>io.projectreactor</groupId>
            <artifactId>reactor-core</artifactId>
            <version>3.4.32</version>
        </dependency>

        <!-- Override Netty versions to fix compatibility with Azure Cosmos Client -->
        <dependency>
            <groupId>io.netty</groupId>
            <artifactId>netty-bom</artifactId>
            <version>4.1.101.Final</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>

        <!-- Override netty-tcnative to match Netty version -->
        <dependency>
            <groupId>io.netty</groupId>
            <artifactId>netty-tcnative-boringssl-static</artifactId>
            <version>2.0.62.Final</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### Configuration Setup

#### Create Cosmos Configuration Class
Replace your Cassandra configuration with:

```java
@Configuration
@EnableCosmosRepositories  // Required for non-reactive repositories
@EnableReactiveCosmosRepositories  // CRITICAL: Required for reactive repositories
public class CosmosConfiguration extends AbstractCosmosConfiguration {

    @Value("${azure.cosmos.uri}")
    private String uri;

    @Value("${azure.cosmos.database}")
    private String database;

    @Bean
    public CosmosClientBuilder getCosmosClientBuilder() {
        return new CosmosClientBuilder()
            .endpoint(uri)
            .credential(new DefaultAzureCredential());
    }

    @Bean
    public CosmosAsyncClient cosmosAsyncClient(CosmosClientBuilder cosmosClientBuilder) {
        return cosmosClientBuilder.buildAsyncClient();
    }

    @Bean
    public CosmosClientBuilderFactory cosmosFactory(CosmosAsyncClient cosmosAsyncClient) {
        return new CosmosClientBuilderFactory(cosmosAsyncClient);
    }

    @Bean
    public ReactiveCosmosTemplate reactiveCosmosTemplate(CosmosClientBuilderFactory cosmosClientBuilderFactory) {
        return new ReactiveCosmosTemplate(cosmosClientBuilderFactory, database);
    }

    @Override
    protected String getDatabaseName() {
        return database;
    }
}
```

**Critical Notes:**
- **BOTH annotations required**: @EnableCosmosRepositories AND @EnableReactiveCosmosRepositories
- Missing @EnableReactiveCosmosRepositories will cause "No qualifying bean" errors for reactive repositories

#### Application Properties
Add cosmos profile configuration:

```properties
# application-cosmos.properties
azure.cosmos.uri=https://<your-cosmos-account>.documents.azure.com:443/
azure.cosmos.database=your-database-name
```

### Entity Conversion

#### Convert from Cassandra to Cosmos Annotations

**Before (Cassandra):**
```java
@Table(value = "entity_table")
public class EntityName {
    @PartitionKey
    private UUID id;

    @ClusteringColumn
    private String fieldName;

    @Column("column_name")
    private String anotherField;
}
```

**After (Cosmos):**
```java
@Container(containerName = "entities")
public class EntityName {
    @Id
    private String id;  // Changed from UUID to String

    @PartitionKey
    private String fieldName;  // Choose appropriate partition key

    private String anotherField;

    // Generate String IDs
    public EntityName() {
        this.id = UUID.randomUUID().toString();
    }
}
```

#### Key Changes:
- Replace `@Table` with `@Container(containerName = "...")`
- Change `@PartitionKey` to Cosmos partition key strategy
- Convert all IDs from `UUID` to `String`
- Remove `@Column` annotations (Cosmos uses field names)
- Remove `@ClusteringColumn` (not applicable in Cosmos)

### Repository Conversion

#### Replace Cassandra Data Access Layer with Cosmos Repositories

**If your application uses DAOs or custom data access classes:**

**Before (Cassandra DAO pattern):**
```java
@Repository
public class EntityReactiveDao {
    // Custom Cassandra query methods
}
```

**After (Cosmos Repository):**
```java
@Repository
public interface EntityCosmosRepository extends ReactiveCosmosRepository<EntityName, String> {

    @Query("SELECT * FROM entities e WHERE e.fieldName = @fieldName")
    Flux<EntityName> findByFieldName(@Param("fieldName") String fieldName);

    @Query("SELECT * FROM entities e WHERE e.id = @id")
    Mono<EntityName> findEntityById(@Param("id") String id);
}
```

**If your application uses Spring Data Cassandra repositories:**

**Before:**
```java
@Repository
public interface EntityCassandraRepository extends ReactiveCassandraRepository<EntityName, UUID> {
    // Cassandra-specific methods
}
```

**After:**
```java
@Repository
public interface EntityCosmosRepository extends ReactiveCosmosRepository<EntityName, String> {
    // Convert existing methods to Cosmos queries
}
```

**If your application uses direct CqlSession or Cassandra driver:**
- Replace direct driver calls with repository pattern
- Convert CQL queries to Cosmos SQL syntax
- Implement repository interfaces as shown above

#### Key Points:
- **CRITICAL**: Use `ReactiveCosmosRepository<Entity, String>` for reactive programming (NOT CosmosRepository)
- Use `CosmosRepository<Entity, String>` for non-reactive applications
- **Repository Interface Change**: If converting from existing Cassandra repositories/DAOs, ensure all repository interfaces extend ReactiveCosmosRepository
- **Common Error**: "No qualifying bean of type ReactiveCosmosRepository" = missing @EnableReactiveCosmosRepositories
- **If using custom data access classes**: Convert to repository pattern for better integration
- **If already using Spring Data**: Change interface extension from ReactiveCassandraRepository to ReactiveCosmosRepository
- Implement custom queries with `@Query` annotation using SQL-like syntax (not CQL)
- All query parameters must use `@Param` annotation

### Service Layer Updates

#### Update Service Classes for Reactive Programming (If Applicable)

**If your application has a service layer:**

**CRITICAL**: Service methods must return Flux/Mono, not Iterable/Optional

```java
@Service
public class EntityReactiveServices {
    private final EntityCosmosRepository repository;

    public EntityReactiveServices(EntityCosmosRepository repository) {
        this.repository = repository;
    }

    // CORRECT: Returns Flux<EntityName>
    public Flux<EntityName> findAll() {
        return repository.findAll();
    }

    // CORRECT: Returns Mono<EntityName>
    public Mono<EntityName> findById(String id) {
        return repository.findById(id);
    }

    // CORRECT: Returns Mono<EntityName>
    public Mono<EntityName> save(EntityName entity) {
        return repository.save(entity);
    }

    // Custom queries - MUST return Flux/Mono
    public Flux<EntityName> findByFieldName(String fieldName) {
        return repository.findByFieldName(fieldName);
    }

    // WRONG PATTERNS TO AVOID:
    // public Iterable<EntityName> findAll() - Will cause compilation errors
    // public Optional<EntityName> findById() - Will cause compilation errors
    // repository.findAll().collectList() - Unnecessary blocking
}
```

**If your application uses direct repository injection in controllers:**
- Consider adding a service layer for better separation of concerns
- Update controller dependencies to use new Cosmos repositories
- Ensure proper reactive type handling throughout the call chain

**Common Issues:**
- **Compilation Error**: "Cannot resolve method" when using Iterable return types
- **Runtime Error**: Attempting to call .collectList() or .block() unnecessarily
- **Performance**: Blocking reactive streams defeats the purpose of reactive programming

### Controller Updates

#### Update REST Controllers for String IDs

**If your application has REST controllers:**

**Before:**
```java
@GetMapping("/entities/{entityId}")
public Mono<EntityDto> getEntity(@PathVariable UUID entityId) {
    return entityService.findById(entityId);
}
```

**After:**
```java
@GetMapping("/entities/{entityId}")
public Mono<EntityDto> getEntity(@PathVariable String entityId) {
    return entityService.findById(entityId);
}
```

**If your application doesn't use controllers:**
- Apply the same UUID → String conversion principles to your data access layer
- Update any external APIs or interfaces that accept/return entity IDs

### Data Mapping Utilities

#### Update Mapping Between Domain Objects and Entities

**If your application uses mapping utilities or converters:**

```java
public class MappingUtils {

    // Convert domain object to entity
    public static EntityName toEntity(DomainObject domain) {
        EntityName entity = new EntityName();
        entity.setId(domain.getId()); // Now String instead of UUID
        entity.setFieldName(domain.getFieldName());
        entity.setAnotherField(domain.getAnotherField());
        // ... other fields
        return entity;
    }

    // Convert entity to domain object
    public static DomainObject toDomain(EntityName entity) {
        DomainObject domain = new DomainObject();
        domain.setId(entity.getId());
        domain.setFieldName(entity.getFieldName());
        domain.setAnotherField(entity.getAnotherField());
        // ... other fields
        return domain;
    }
}
```

**If your application doesn't use explicit mapping:**
- Ensure consistent ID type usage throughout your codebase
- Update any object construction or copying logic to handle String IDs

### Test Updates

#### Update Test Classes

**Critical**: All test files must be updated to work with String IDs and Cosmos repositories:

```java
**If your application has unit tests:**

```java
@ExtendWith(MockitoExtension.class)
class EntityReactiveServicesTest {

    @Mock
    private EntityCosmosRepository entityRepository; // Updated to Cosmos repository

    @InjectMocks
    private EntityReactiveServices entityService;

    @Test
    void testFindById() {
        String entityId = "test-entity-id"; // Changed from UUID to String
        EntityName mockEntity = new EntityName();
        mockEntity.setId(entityId);

        when(entityRepository.findById(entityId)).thenReturn(Mono.just(mockEntity));

        StepVerifier.create(entityService.findById(entityId))
            .expectNext(mockEntity)
            .verifyComplete();
    }
}
```

**If your application has integration tests:**
- Update test data setup to use String IDs
- Replace Cassandra test containers with Cosmos DB emulator (if available)
- Update test queries to use Cosmos SQL syntax instead of CQL

**If your application doesn't have tests:**
- Consider adding basic tests to verify the conversion works correctly
- Focus on testing ID conversion and basic CRUD operations
```

### Common Issues and Solutions

#### Issue 1: NoClassDefFoundError with reactor.core.publisher.Sinks
**Problem**: Azure Identity library requires newer Reactor Core version
**Error**: `java.lang.NoClassDefFoundError: reactor/core/publisher/Sinks`
**Root Cause**: Spring Boot 2.3.x uses older reactor-core that doesn't have Sinks API
**Solution**: Add reactor-core version override in dependencyManagement (see Step 1)

#### Issue 2: NoSuchMethodError with Netty Epoll methods
**Problem**: Version mismatch between Spring Boot Netty and Azure Cosmos requirements
**Error**: `java.lang.NoSuchMethodError: 'boolean io.netty.channel.epoll.Epoll.isTcpFastOpenClientSideAvailable()'`
**Root Cause**: Spring Boot 2.3.x uses Netty 4.1.51.Final, Azure requires newer methods
**Solution**: Add netty-bom version override (see Step 1)

#### Issue 3: NoSuchMethodError with SSL Context
**Problem**: Netty TLS native library version mismatch
**Error**: `java.lang.NoSuchMethodError: 'boolean io.netty.internal.tcnative.SSLContext.setCurvesList(long, java.lang.String[])'`
**Root Cause**: netty-tcnative version incompatible with upgraded Netty
**Solution**: Add netty-tcnative-boringssl-static version override (see Step 1)

#### Issue 4: ReactiveCosmosRepository beans not created
**Problem**: Missing @EnableReactiveCosmosRepositories annotation
**Error**: `No qualifying bean of type 'ReactiveCosmosRepository' available`
**Root Cause**: Only @EnableCosmosRepositories doesn't create reactive repository beans
**Solution**: Add both @EnableCosmosRepositories and @EnableReactiveCosmosRepositories to configuration

#### Issue 5: Repository interface compilation errors
**Problem**: Using CosmosRepository instead of ReactiveCosmosRepository
**Error**: `Cannot resolve method 'findAll()' in 'CosmosRepository'`
**Root Cause**: CosmosRepository returns Iterable, not Flux
**Solution**: Change all repository interfaces to extend ReactiveCosmosRepository<Entity, String>

#### Issue 6: Service layer reactive type mismatches
**Problem**: Service methods returning Iterable/Optional instead of Flux/Mono
**Error**: `Required type: Flux<Entity> Provided: Iterable<Entity>`
**Root Cause**: Repository methods return reactive types, services must match
**Solution**: Update all service method signatures to return Flux/Mono

#### Issue 7: Authentication failures with DefaultAzureCredential
**Problem**: DefaultAzureCredential not finding credentials
**Error**: `All credentials in the chain are unavailable` or specific credential unavailable messages
**Root Cause**: No valid Azure credential source available

**Solutions**:
1. **For local development**: Ensure Azure CLI login
   ```bash
   az login
   # Verify login
   az account show
   ```

2. **For Azure-hosted applications**: Ensure Managed Identity is enabled and has proper RBAC permissions

3. **Check credential chain order**: DefaultAzureCredential tries in this order:
   - Environment variables → Workload Identity → Managed Identity → Azure CLI → PowerShell → Developer CLI

#### Issue 8: Database not found errors
**Problem**: Application fails to start with database not found errors
**Error**: `Database 'your-database-name' not found` or `Resource Not Found`
**Root Cause**: Database doesn't exist in Cosmos DB account

**Solution**: Create the database before first run (see Database Setup section):
```bash
# Via Azure CLI
az cosmosdb sql database create \
  --account-name your-cosmos-account \
  --name your-database-name \
  --resource-group your-resource-group

# Or via Azure Portal (recommended for first-time setup)
# Portal → Cosmos DB → Data Explorer → New Database
```

**Note**: Containers (collections) will be auto-created from entity `@Container` annotations, but the database itself may need to exist first depending on your RBAC permissions.

#### Issue 9: RBAC permission errors
**Problem**: Application fails with permission denied errors
**Error**:
```
Request blocked by Auth: principal [xxx] does not have required RBAC permissions
to perform action [Microsoft.DocumentDB/databaseAccounts/sqlDatabases/write]
```

**Root Cause**: Your Azure identity lacks required Cosmos DB permissions

**Solution**: Assign "Cosmos DB Built-in Data Contributor" role:
```bash
# Get resource group
RESOURCE_GROUP=$(az cosmosdb show --name your-cosmos-account --query resourceGroup -o tsv 2>/dev/null)

# If the above fails, list all Cosmos accounts to find it
az cosmosdb list --query "[?name=='your-cosmos-account'].{name:name, resourceGroup:resourceGroup}" -o table

# Assign role
az cosmosdb sql role assignment create \
  --account-name your-cosmos-account \
  --resource-group $RESOURCE_GROUP \
  --scope "/" \
  --principal-id $(az ad signed-in-user show --query id -o tsv) \
  --role-definition-name "Cosmos DB Built-in Data Contributor"
```

**Alternative**: Portal → Cosmos DB → Access Control (IAM) → Add role assignment → "Cosmos DB Built-in Data Contributor"

#### Issue 10: Partition key strategy differences
**Problem**: Cassandra clustering keys don't map directly to Cosmos partition keys
**Error**: Cross-partition queries or poor performance
**Root Cause**: Different data distribution strategies
**Solution**: Choose appropriate partition key based on query patterns, typically the most frequently queried field

#### Issue 10: UUID to String conversion issues
**Problem**: Test files and controllers still using UUID types
**Error**: `Cannot convert UUID to String` or type mismatch errors
**Root Cause**: Not all occurrences of UUID were converted to String
**Solution**: Systematically search and replace all UUID references with String

### Data Seeding

#### Implement Data Population

**If your application needs initial data:**

```java
@Component
public class DataSeeder implements CommandLineRunner {

    private final EntityCosmosRepository entityRepository;

    @Override
    public void run(String... args) throws Exception {
        if (entityRepository.count().block() == 0) {
            // Seed initial data
            EntityName entity = new EntityName();
            entity.setFieldName("Sample Value");
            entity.setAnotherField("Sample Data");

            entityRepository.save(entity).block();
        }
    }
}
```

**If your application has existing data migration needs:**
- Create migration scripts to export from Cassandra and import to Cosmos DB
- Consider data transformation needs (UUID to String conversion)
- Plan for any schema differences between Cassandra and Cosmos data models

**If your application doesn't need data seeding:**
- Skip this step and proceed to verification

### Application Profiles

#### Update application.yml for Cosmos profile
```yaml
spring:
  profiles:
    active: cosmos

---
spring:
  profiles: cosmos

azure:
  cosmos:
    uri: ${COSMOS_URI:https://<your-account>.documents.azure.com:443/}
    database: ${COSMOS_DATABASE:your-database}
```

## Verification Gates

- **Compile Check**: `mvn compile` should succeed without errors
- **Test Check**: `mvn test` should pass with updated test cases
- **Runtime Check**: Application should start without version conflicts
- **Connection Check**: Application should connect to Cosmos DB successfully
- **Data Check**: CRUD operations should work through the API
- **UI Check**: Frontend should display data from Cosmos DB

## Cosmos Migration Practices

1. **ID Strategy**: Always use String IDs instead of UUIDs for Cosmos DB
2. **Partition Key**: Choose partition keys based on query patterns and data distribution
3. **Query Design**: Use @Query annotation for custom queries instead of method naming conventions
4. **Reactive Programming**: Stick to Flux/Mono patterns throughout the service layer
5. **Version Management**: Always include dependency version overrides for Spring Boot 2.x projects
6. **Testing**: Update all test files to use String IDs and mock Cosmos repositories
7. **Authentication**: Use DefaultAzureCredential for production-ready authentication

## Troubleshooting Commands

```bash
# Check dependencies and version conflicts
mvn dependency:tree | grep -E "(reactor|netty|cosmos)"

# Verify specific problematic dependencies
mvn dependency:tree | grep "reactor-core"
mvn dependency:tree | grep "reactor-netty"
mvn dependency:tree | grep "netty-tcnative"

# Test connection
curl http://localhost:8080/api/entities

# Check Azure login status
az account show

# Clean and rebuild (often fixes dependency issues)
mvn clean compile

# Run with debug logging for dependency resolution
mvn dependency:resolve -X

# Check for compilation errors specifically
mvn compile 2>&1 | grep -E "(ERROR|error)"

# Run with debug for runtime issues
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005"

# Check application logs for version conflicts
grep -E "(NoSuchMethodError|NoClassDefFoundError|reactor|netty)" application.log
```

## Typical Error Sequence and Resolution

Based on real conversion experience, you'll likely encounter these errors in this order:

### **Phase 1: Compilation Errors**
1. **Missing dependencies** → Add azure-spring-data-cosmos and azure-identity
2. **Configuration class errors** → Create CosmosConfiguration (if not already present)
3. **Entity annotation errors** → Convert @Table to @Container, etc.
4. **Repository interface errors** → Change to ReactiveCosmosRepository (if using repository pattern)

### **Phase 2: Bean Creation Errors**
5. **"No qualifying bean of type ReactiveCosmosRepository"** → Add @EnableReactiveCosmosRepositories
6. **Service layer type mismatches** → Change Iterable to Flux, Optional to Mono (if using service layer)

### **Phase 3: Runtime Version Conflicts** (Most Complex)
7. **NoClassDefFoundError: reactor.core.publisher.Sinks** → Add reactor-core 3.4.32 override
8. **NoSuchMethodError: Epoll.isTcpFastOpenClientSideAvailable** → Add netty-bom 4.1.101.Final override
9. **NoSuchMethodError: SSLContext.setCurvesList** → Add netty-tcnative-boringssl-static 2.0.62.Final override

### **Phase 4: Authentication & Connection**
10. **ManagedIdentityCredential authentication unavailable** → Run `az login --use-device-code`
11. **Application starts successfully** → Connected to Cosmos DB!

**Critical**: The phases are diagnostic dependencies. Earlier compilation and bean-creation failures mask later runtime, authentication, and connection failures.

## Performance Considerations

1. **Partition Strategy**: Design partition keys to distribute load evenly
2. **Query Optimization**: Use indexes and avoid cross-partition queries when possible
3. **Connection Pooling**: Cosmos client automatically manages connections
4. **Request Units**: Monitor RU consumption and adjust throughput as needed
5. **Bulk Operations**: Use batch operations for multiple document updates
## Conventions

| Rule | Rationale |
|---|---|
| Use Spring Data Cosmos as the replacement data-access abstraction for Spring Data Cassandra, Cassandra DAOs, DataStax drivers, direct `CqlSession`, and CQL query code | The conversion succeeds only when Cassandra-specific access paths are removed consistently |
| Keep Spring Boot 3.x builds on Java 17+ and Spring Boot 2.x Cosmos conversions on compatible `reactor-core`, `reactor-netty`, Netty, and `netty-tcnative-boringssl-static` versions | Version mismatches produce the documented `NoClassDefFoundError` and `NoSuchMethodError` failures |
| Prefer `DefaultAzureCredential` with Azure RBAC for real environments and reserve key-based authentication for a local emulator | Managed identity, workload identity, Azure CLI, Azure PowerShell, and Azure Developer CLI credentials avoid committed keys |
| Create or verify the Cosmos database before first application startup and let Spring Data Cosmos create containers from `@Container` metadata | Containers can be derived from entities, but missing databases and RBAC gaps block startup |
| Convert persisted identifiers from `UUID` to `String` across entities, repositories, controllers, mappers, seeders, and tests | Mixed ID types cause compile errors, mapping failures, and broken API contracts |
| Use `ReactiveCosmosRepository<Entity, String>`, `Flux`, and `Mono` end-to-end for reactive applications; use `CosmosRepository<Entity, String>` only for non-reactive applications | Mixing reactive and blocking repository contracts creates bean, type, and runtime failures |
| Replace Cassandra annotations and query language with Cosmos annotations and SQL-like `@Query` methods using `@Param` | Cassandra `@Table`, `@ClusteringColumn`, `@Column`, and CQL semantics do not apply to Cosmos documents |
| Search and update constructor calls after changing Lombok annotations or entity constructors | Mapping utilities, data seeders, and tests frequently compile against removed all-args or UUID constructors |
| Fix application code before tests, then run compile, test-compile, and tests | A stable production path exposes the remaining test-only DAO, UUID, and constructor issues clearly |
| Monitor RU consumption, partition-key distribution, and cross-partition queries after conversion | Cosmos performance depends on partition strategy and request-unit economics rather than Cassandra clustering keys |

## Do / Do Not

| Do | Do not |
|---|---|
| Replace Cassandra dependencies with `azure-spring-data-cosmos` and `azure-identity` | Leave `java-driver-core`, `java-driver-query-builder`, or other DataStax dependencies in active code |
| Enable both `@EnableCosmosRepositories` and `@EnableReactiveCosmosRepositories` when both repository styles exist | Expect reactive repositories to appear when only non-reactive repository scanning is enabled |
| Use `DefaultAzureCredentialBuilder().build()` or `DefaultAzureCredential` with `az login` for local development | Commit Cosmos keys or rely on key-based auth outside the local emulator |
| Choose a Cosmos partition key from query patterns and data distribution | Treat Cassandra clustering keys or LWT behavior as directly portable |
| Convert `findAllById()` results from `Iterable` before streaming in non-reactive code | Call `.stream()` directly on `Iterable<Entity>` |
| Validate startup logs until the application reports Tomcat started and Cosmos account retrieval succeeded | Interrupt startup while the credential chain cycles through unavailable providers |
| Use setter-based setup where entity constructors were removed | Keep calls such as `new Owner(UUID.fromString(...))` after IDs become strings |
| Run `mvn clean compile`, `mvn test-compile`, and `mvn test` or the Gradle equivalents after conversion | Stop after dependency edits without compiling repositories, services, controllers, seeders, and tests |

## Checklist Before Opening a PR

- [ ] The matched Spring Boot code no longer depends on Cassandra DAOs, DataStax drivers, Spring Data Cassandra repositories, CQL, or Cassandra-only annotations.
- [ ] Maven or Gradle dependencies include Spring Data Cosmos, Azure Identity, and any required Reactor/Netty compatibility overrides for the Spring Boot baseline.
- [ ] `JAVA_HOME` and the build JDK satisfy the Spring Boot version requirement, including Java 17+ for Spring Boot 3.x.
- [ ] Cosmos configuration uses `DefaultAzureCredential`, the required repository-enable annotations, and `azure.cosmos.uri` plus `azure.cosmos.database` properties.
- [ ] The Cosmos database exists, containers match `@Container` names, and the Azure principal has `Cosmos DB Built-in Data Contributor` or equivalent RBAC.
- [ ] Entity IDs, controller path variables, mapping utilities, seed data, and tests use `String` IDs consistently instead of `UUID`.
- [ ] Reactive applications return `Flux` and `Mono` through repositories and services without blocking or converting to `Iterable` and `Optional`.
- [ ] Constructor, Lombok, `package-info.java`, and data seeder changes compile cleanly.
- [ ] `mvn clean compile`, `mvn test-compile`, and `mvn test` or the corresponding Gradle commands pass for the converted project.
- [ ] Runtime smoke testing reaches the configured port and verifies at least one CRUD path against Cosmos DB.
