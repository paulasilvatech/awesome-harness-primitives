---
applyTo: "**/*.{pbix,md,json,txt}"
description: "Enforces Power BI semantic model conventions for star schema design, relationships, storage modes, performance, security, governance, testing, and advanced modeling patterns."
---

# Power BI Data Modeling Conventions — Semantic Models

This file applies to Power BI semantic model artifacts, documentation, JSON metadata, and text design notes matched by the `applyTo` globs. It is authoritative for efficient, scalable, and maintainable Power BI data modeling using Microsoft guidance, star schema principles, dimensional modeling, relationships, storage mode choices, performance, security, governance, and validation; source-system contracts, enterprise security policy, and report visual design rules win when they define stricter requirements.

## Star Schema Design Principles

### 1. Fundamental Table Types
**Dimension Tables** - Store descriptive business entities:
- Products, customers, geography, time, employees
- Contain unique key columns (preferably surrogate keys)
- Relatively small number of rows
- Used for filtering, grouping, and providing context
- Support hierarchical drill-down scenarios

**Fact Tables** - Store measurable business events:
- Sales transactions, website clicks, manufacturing events
- Contain foreign keys to dimension tables
- Numeric measures for aggregation
- Large number of rows (typically growing over time)
- Represent specific grain/level of detail

```
Example Star Schema Structure:

DimProduct (Dimension)          FactSales (Fact)              DimCustomer (Dimension)
├── ProductKey (PK)             ├── SalesKey (PK)             ├── CustomerKey (PK)
├── ProductName                 ├── ProductKey (FK)           ├── CustomerName
├── Category                    ├── CustomerKey (FK)          ├── CustomerType
├── SubCategory                 ├── DateKey (FK)              ├── Region
└── UnitPrice                   ├── SalesAmount               └── RegistrationDate
                               ├── Quantity
DimDate (Dimension)             └── DiscountAmount
├── DateKey (PK)
├── Date
├── Year
├── Quarter
├── Month
└── DayOfWeek
```

### 2. Table Design Best Practices

#### Dimension Table Design
```
DO:
- Use surrogate keys (auto-incrementing integers) as primary keys
- Include business keys for integration purposes
- Create hierarchical attributes (Category > SubCategory > Product)
- Use descriptive names and proper data types
- Include "Unknown" records for missing dimension data
- Keep dimension tables relatively narrow (focused attributes)

DON'T:
- Use natural business keys as primary keys in large models
- Mix fact and dimension characteristics in same table
- Create unnecessarily wide dimension tables
- Leave missing values without proper handling
```

#### Fact Table Design
```
DO:
- Store data at the most granular level needed
- Use foreign keys that match dimension table keys
- Include only numeric, measurable columns
- Maintain consistent grain across all fact table rows
- Use appropriate data types (decimal for currency, integer for counts)

DON'T:
- Include descriptive text columns (these belong in dimensions)
- Mix different grains in the same fact table
- Store calculated values that can be computed at query time
- Use composite keys when surrogate keys would be simpler
```

## Relationship Design and Management

### 1. Relationship Types and Best Practices

#### One-to-Many Relationships (Standard Pattern)
```
Configuration:
- From Dimension (One side) to Fact (Many side)
- Single direction filtering (Dimension filters Fact)
- Mark as "Assume Referential Integrity" for DirectQuery performance

Example:
DimProduct (1) ← ProductKey → (*) FactSales
DimCustomer (1) ← CustomerKey → (*) FactSales
DimDate (1) ← DateKey → (*) FactSales
```

#### Many-to-Many Relationships (Use Sparingly)
```
When to Use:
Genuine many-to-many business relationships
When bridging table pattern is not feasible
For advanced analytical scenarios

Best Practices:
- Create explicit bridging tables when possible
- Use low-cardinality relationship columns
- Monitor performance impact carefully
- Document business rules clearly

Example with Bridging Table:
DimCustomer (1) ← CustomerKey → (*) BridgeCustomerAccount (*) ← AccountKey → (1) DimAccount
```

#### One-to-One Relationships (Rare)
```
When to Use:
- Extending dimension tables with additional attributes
- Degenerate dimension scenarios
- Separating PII from operational data

Implementation:
- Consider consolidating into single table if possible
- Use for security/privacy separation
- Maintain referential integrity
```

### 2. Relationship Configuration Guidelines
```
Filter Direction:
Single Direction: Default choice, best performance
Both Directions: Only when cross-filtering is required for business logic
Avoid: Circular relationship paths

Cross-Filter Direction:
- Dimension to Fact: Always single direction
- Fact to Fact: Avoid direct relationships, use shared dimensions
- Dimension to Dimension: Only when business logic requires it

Referential Integrity:
Enable for DirectQuery sources when data quality is guaranteed
Improves query performance by using INNER JOINs
Don't enable if source data has orphaned records
```

## Storage Mode Optimization

### 1. Import Mode Best Practices
```
When to Use Import Mode:
Data size fits within capacity limits
Complex analytical calculations required
Historical data analysis with stable datasets
Need for optimal query performance

Optimization Strategies:
- Remove unnecessary columns and rows
- Use appropriate data types
- Pre-aggregate data when possible
- Implement incremental refresh for large datasets
- Optimize Power Query transformations
```

#### Data Reduction Techniques for Import
```
Vertical Filtering (Column Reduction):
Remove columns not used in reports or relationships
Remove calculated columns that can be computed in DAX
Remove intermediate columns used only in Power Query
Optimize data types (Integer vs. Decimal, Date vs. DateTime)

Horizontal Filtering (Row Reduction):
Filter to relevant time periods (e.g., last 3 years of data)
Filter to relevant business entities (active customers, specific regions)
Remove test, invalid, or cancelled transactions
Implement proper data archiving strategies

Data Type Optimization:
Text → Numeric: Convert codes to integers when possible
DateTime → Date: Use Date type when time is not needed
Decimal → Integer: Use integers for whole number measures
High Precision → Lower Precision: Match business requirements
```

### 2. DirectQuery Mode Best Practices
```
When to Use DirectQuery Mode:
Data exceeds import capacity limits
Real-time data requirements
Security/compliance requires data to stay at source
Integration with operational systems

Optimization Requirements:
- Optimize source database performance
- Create appropriate indexes on source tables
- Minimize complex DAX calculations
- Use simple measures and aggregations
- Limit number of visuals per report page
- Implement query reduction techniques
```

#### DirectQuery Performance Optimization
```
Database Optimization:
Create indexes on frequently filtered columns
Create indexes on relationship key columns
Use materialized views for complex joins
Implement appropriate database maintenance
Consider columnstore indexes for analytical workloads

Model Design for DirectQuery:
Keep DAX measures simple
Avoid calculated columns on large tables
Use star schema design strictly
Minimize cross-table operations
Pre-aggregate data in source when possible

Query Performance:
Apply filters early in report design
Use appropriate visual types
Limit high-cardinality filtering
Monitor and optimize slow queries
```

### 3. Composite Model Design
```
When to Use Composite Models:
Combine historical (Import) with real-time (DirectQuery) data
Extend existing models with additional data sources
Balance performance with data freshness requirements
Integrate multiple DirectQuery sources

Storage Mode Selection:
Import: Small dimension tables, historical aggregated facts
DirectQuery: Large fact tables, real-time operational data
Dual: Dimension tables that need to work with both Import and DirectQuery facts
Hybrid: Fact tables combining historical (Import) with recent (DirectQuery) data
```

#### Dual Storage Mode Strategy
```
Use Dual Mode For:
Dimension tables that relate to both Import and DirectQuery facts
Small, slowly changing reference tables
Lookup tables that need flexible querying

Configuration:
- Set dimension tables to Dual mode
- Power BI automatically chooses optimal query path
- Maintains single copy of dimension data
- Enables efficient cross-source relationships
```

## Advanced Modeling Patterns

### 1. Date Table Design
```
Essential Date Table Attributes:
Continuous date range (no gaps)
Mark as date table in Power BI
Include standard hierarchy (Year > Quarter > Month > Day)
Add business-specific columns (FiscalYear, WorkingDay, Holiday)
Use Date data type for date column

Date Table Implementation:
DateKey (Integer): 20240315 (YYYYMMDD format)
Date (Date): 2024-03-15
Year (Integer): 2024
Quarter (Text): Q1 2024
Month (Text): March 2024
MonthNumber (Integer): 3
DayOfWeek (Text): Friday
IsWorkingDay (Boolean): TRUE
FiscalYear (Integer): 2024
FiscalQuarter (Text): FY2024 Q3
```

### 2. Slowly Changing Dimensions (SCD)
```
Type 1 SCD (Overwrite):
- Update existing records with new values
- Lose historical context
- Simple to implement and maintain
- Use for non-critical attribute changes

Type 2 SCD (History Preservation):
- Create new records for changes
- Maintain complete history
- Include effective date ranges
- Use surrogate keys for unique identification

Implementation Pattern:
CustomerKey (Surrogate): 1, 2, 3, 4
CustomerID (Business): 101, 101, 102, 103
CustomerName: "John Doe", "John Smith", "Jane Doe", "Bob Johnson"
EffectiveDate: 2023-01-01, 2024-01-01, 2023-01-01, 2023-01-01
ExpirationDate: 2023-12-31, 9999-12-31, 9999-12-31, 9999-12-31
IsCurrent: FALSE, TRUE, TRUE, TRUE
```

### 3. Role-Playing Dimensions
```
Scenario: Date table used for Order Date, Ship Date, Delivery Date

Implementation Options:

Option 1: Multiple Relationships (Recommended)
- Single Date table with multiple relationships to Fact
- One active relationship (Order Date)
- Inactive relationships for Ship Date and Delivery Date
- Use USERELATIONSHIP in DAX measures

Option 2: Multiple Date Tables
- Separate tables: OrderDate, ShipDate, DeliveryDate
- Each with dedicated relationship
- More intuitive for report authors
- Larger model size due to duplication

DAX Implementation:
Sales by Order Date = [Total Sales]  // Uses active relationship
Sales by Ship Date = CALCULATE([Total Sales], USERELATIONSHIP(FactSales[ShipDate], DimDate[Date]))
Sales by Delivery Date = CALCULATE([Total Sales], USERELATIONSHIP(FactSales[DeliveryDate], DimDate[Date]))
```

### 4. Bridge Tables for Many-to-Many
```
Scenario: Students can be in multiple Courses, Courses can have multiple Students

Bridge Table Design:
DimStudent (1) ← StudentKey → (*) BridgeStudentCourse (*) ← CourseKey → (1) DimCourse

Bridge Table Structure:
StudentCourseKey (PK): Surrogate key
StudentKey (FK): Reference to DimStudent
CourseKey (FK): Reference to DimCourse
EnrollmentDate: Additional context
Grade: Additional context
Status: Active, Completed, Dropped

Relationship Configuration:
- DimStudent to BridgeStudentCourse: One-to-Many
- BridgeStudentCourse to DimCourse: Many-to-One
- Set one relationship to bi-directional for filter propagation
- Hide bridge table from report view
```

## Performance Optimization Strategies

### 1. Model Size Optimization
```
Column Optimization:
Remove unused columns completely
Use smallest appropriate data types
Convert high-cardinality text to integers with lookup tables
Remove redundant calculated columns

Row Optimization:
Filter to business-relevant time periods
Remove invalid, test, or cancelled transactions
Archive historical data appropriately
Use incremental refresh for growing datasets

Aggregation Strategies:
Pre-calculate common aggregations
Use summary tables for high-level reporting
Implement automatic aggregations in Premium
Consider OLAP cubes for complex analytical requirements
```

### 2. Relationship Performance
```
Key Selection:
Use integer keys over text keys
Prefer surrogate keys over natural keys
Ensure referential integrity in source data
Create appropriate indexes on key columns

Cardinality Optimization:
Set correct relationship cardinality
Use "Assume Referential Integrity" when appropriate
Minimize bidirectional relationships
Avoid many-to-many relationships when possible

Cross-Filtering Strategy:
Use single-direction filtering as default
Enable bi-directional only when required
Test performance impact of cross-filtering
Document business reasons for bi-directional relationships
```

### 3. Query Performance Patterns
```
Efficient Model Patterns:
Proper star schema implementation
Normalized dimension tables
Denormalized fact tables
Consistent grain across related tables
Appropriate use of calculated tables and columns

Query Optimization:
Pre-filter large datasets
Use appropriate visual types for data
Minimize complex DAX in reports
Leverage model relationships effectively
Consider DirectQuery for large, real-time datasets
```

## Security and Governance

### 1. Row-Level Security (RLS)
```
Implementation Patterns:

User-Based Security:
[UserEmail] = USERPRINCIPALNAME()

Role-Based Security:
VAR UserRole =
    LOOKUPVALUE(
        UserRoles[Role],
        UserRoles[Email],
        USERPRINCIPALNAME()
    )
RETURN
    Customers[Region] = UserRole

Dynamic Security:
LOOKUPVALUE(
    UserRegions[Region],
    UserRegions[Email],
    USERPRINCIPALNAME()
) = Customers[Region]

Best Practices:
Test with different user accounts
Keep security logic simple and performant
Document security requirements clearly
Use security roles, not individual user filters
Consider performance impact of complex RLS
```

### 2. Data Governance
```
Documentation Requirements:
Business definitions for all measures
Data lineage and source system mapping
Refresh schedules and dependencies
Security and access control documentation
Change management procedures

Data Quality:
Implement data validation rules
Monitor for data completeness
Handle missing values appropriately
Validate business rule implementation
Regular data quality assessments

Version Control:
Source control for Power BI files
Environment promotion procedures
Change tracking and approval processes
Backup and recovery procedures
```

## Testing and Validation Framework

### 1. Model Testing Checklist
```
Functional Testing:
□ All relationships function correctly
□ Measures calculate expected values
□ Filters propagate appropriately
□ Security rules work as designed
□ Data refresh completes successfully

Performance Testing:
□ Model loads within acceptable time
□ Queries execute within SLA requirements
□ Visual interactions are responsive
□ Memory usage is within capacity limits
□ Concurrent user load testing completed

Data Quality Testing:
□ No missing foreign key relationships
□ Measure totals match source system
□ Date ranges are complete and continuous
□ Security filtering produces correct results
□ Business rules are correctly implemented
```

### 2. Validation Procedures
```
Business Validation:
Compare report totals with source systems
Validate complex calculations with business users
Test edge cases and boundary conditions
Confirm business logic implementation
Verify report accuracy across different filters

Technical Validation:
Performance testing with realistic data volumes
Concurrent user testing
Security testing with different user roles
Data refresh testing and monitoring
Disaster recovery testing
```

## Common Anti-Patterns to Avoid

### 1. Schema Anti-Patterns
```
Snowflake Schema (Unless Necessary):
- Multiple normalized dimension tables
- Complex relationship chains
- Reduced query performance
- More complex for business users

Single Large Table:
- Mixing facts and dimensions
- Denormalized to extreme
- Difficult to maintain and extend
- Poor performance for analytical queries

Multiple Fact Tables with Direct Relationships:
- Many-to-many between facts
- Complex filter propagation
- Difficult to maintain consistency
- Better to use shared dimensions
```

### 2. Relationship Anti-Patterns
```
Bidirectional Relationships Everywhere:
- Performance impact
- Unpredictable filter behavior
- Maintenance complexity
- Should be exception, not rule

Many-to-Many Without Business Justification:
- Often indicates missing dimension
- Can hide data quality issues
- Complex debugging and maintenance
- Bridge tables usually better solution

Circular Relationships:
- Ambiguous filter paths
- Unpredictable results
- Difficult debugging
- Always avoid through proper design
```

## Advanced Data Modeling Patterns

### 1. Slowly Changing Dimensions Implementation
```powerquery
// Type 1 SCD: Power Query implementation for hash-based change detection
let
    Source = Source,

    #"Added custom" = Table.TransformColumnTypes(
        Table.AddColumn(Source, "Hash", each Binary.ToText(
            Text.ToBinary(
                Text.Combine(
                    List.Transform({[FirstName],[LastName],[Region]}, each if _ = null then "" else _),
                "|")),
            BinaryEncoding.Hex)
        ),
        {{"Hash", type text}}
    ),

    #"Marked key columns" = Table.AddKey(#"Added custom", {"Hash"}, false),

    #"Merged queries" = Table.NestedJoin(
        #"Marked key columns",
        {"Hash"},
        ExistingDimRecords,
        {"Hash"},
        "ExistingDimRecords",
        JoinKind.LeftOuter
    ),

    #"Expanded ExistingDimRecords" = Table.ExpandTableColumn(
        #"Merged queries",
        "ExistingDimRecords",
        {"Count"},
        {"Count"}
    ),

    #"Filtered rows" = Table.SelectRows(#"Expanded ExistingDimRecords", each ([Count] = null)),

    #"Removed columns" = Table.RemoveColumns(#"Filtered rows", {"Count"})
in
    #"Removed columns"
```

### 2. Incremental Refresh with Query Folding
```powerquery
// Optimized incremental refresh pattern
let
  Source = Sql.Database("server","database"),
  Data  = Source{[Schema="dbo",Item="FactInternetSales"]}[Data],
  FilteredByStart = Table.SelectRows(Data, each [OrderDateKey] >= Int32.From(DateTime.ToText(RangeStart,[Format="yyyyMMdd"]))),
  FilteredByEnd = Table.SelectRows(FilteredByStart, each [OrderDateKey] < Int32.From(DateTime.ToText(RangeEnd,[Format="yyyyMMdd"])))
in
  FilteredByEnd
```

### 3. Semantic Link Integration
```python
# Working with Power BI semantic models in Python
import sempy.fabric as fabric
from sempy.relationships import plot_relationship_metadata

relationships = fabric.list_relationships("my_dataset")
plot_relationship_metadata(relationships)
```

### 4. Advanced Partition Strategies
```json
// TMSL partition with time-based filtering
"partition": {
      "name": "Sales2019",
      "mode": "import",
      "source": {
        "type": "m",
        "expression": [
          "let",
          "    Source = SqlDatabase,",
          "    dbo_Sales = Source{[Schema=\"dbo\",Item=\"Sales\"]}[Data],",
          "    FilteredRows = Table.SelectRows(dbo_Sales, each [OrderDateKey] >= 20190101 and [OrderDateKey] <= 20191231)",
          "in",
          "    FilteredRows"
        ]
      }
}
```

## Conventions

| Rule | Rationale |
| --- | --- |
| Design semantic models as star schemas with clear dimension tables and fact tables at a consistent grain | Star schemas keep filtering predictable, aggregation efficient, and business meaning understandable |
| Use surrogate integer keys, business keys for integration, and `Unknown` dimension records where source data can be missing | Stable keys and explicit missing-data handling prevent orphaned facts and broken filters |
| Keep fact tables granular, numeric, and free of descriptive text columns | Facts should aggregate cleanly while dimensions provide descriptive context |
| Prefer one-to-many, single-direction relationships from dimensions to facts | This is the standard Power BI pattern for performance and unambiguous filter propagation |
| Use many-to-many, bidirectional relationships, and one-to-one relationships only with documented business justification | These patterns add ambiguity, performance cost, or security risk when used casually |
| Choose Import, DirectQuery, Dual, Hybrid, or Composite storage modes based on data size, freshness, security, and performance requirements | Storage mode controls query behavior, capacity usage, and operational complexity |
| Maintain a continuous marked date table with standard and business-specific attributes | Date intelligence, role-playing dimensions, and fiscal reporting require a reliable calendar |
| Optimize model size by removing unused rows and columns, choosing narrow data types, and preserving query folding for incremental refresh | Smaller models refresh faster, query faster, and consume less capacity |
| Implement RLS with simple, tested rules such as `USERPRINCIPALNAME()` and role tables | Security filters must be understandable, performant, and verifiable |
| Document measures, lineage, refresh schedules, security rules, and change management expectations | Semantic models are shared contracts, not private implementation details |
| Validate with business users, realistic data volumes, Power BI built-in Performance Analyzer, and DAX Studio | Correctness and performance must be proven against real usage patterns |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Model facts and dimensions separately with shared dimensions between facts | Mix fact and dimension characteristics in one large table |
| Use integer surrogate keys for relationships and keep business keys as attributes | Use high-cardinality text keys as primary relationship keys in large models |
| Keep dimensions focused, hierarchical, and descriptive | Create unnecessarily wide dimension tables full of unused attributes |
| Store facts at the most granular level needed with consistent grain | Mix daily, monthly, and transaction-level rows in the same fact table |
| Use bridge tables for genuine many-to-many relationships when possible | Connect fact tables directly or enable many-to-many without justification |
| Enable `Assume Referential Integrity` only when source data quality is guaranteed | Enable it when orphaned records can exist |
| Use `USERELATIONSHIP` for inactive role-playing date relationships | Duplicate date logic without explaining the business role |
| Keep DAX simple in DirectQuery models and pre-aggregate in the source when possible | Push complex calculated columns and cross-table operations into DirectQuery models |
| Test RLS, refresh, totals, filters, and performance with realistic roles and volumes | Ship a model validated only against a small developer sample |
| Use Performance Analyzer and DAX Studio to diagnose bottlenecks | Guess at performance issues without measurement |

## Checklist Before Opening a PR

- [ ] Star schema design is explicit, with dimension tables and fact tables at documented grain.
- [ ] Relationship keys, cardinality, filter direction, and referential integrity settings are justified.
- [ ] Storage modes are chosen intentionally across Import, DirectQuery, Dual, Hybrid, and Composite models.
- [ ] Date tables, SCD handling, role-playing dimensions, bridge tables, and partition strategies preserve business meaning.
- [ ] Model size, query performance, incremental refresh, and query folding have been tested with realistic data volumes.
- [ ] RLS, data governance, lineage, refresh schedules, and access controls are documented and validated.
- [ ] Measure totals, filters, relationships, security rules, and refresh behavior match source-system and business expectations.
- [ ] Performance Analyzer and DAX Studio have been used when optimization or debugging is required.