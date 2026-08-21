---
applyTo: "**/*.scala,**/build.sbt,**/build.sc"
description: "Enforces Scala Apache Spark conventions for dependencies, SparkSession setup, DataFrame and Dataset design, schemas, joins, partitioning, streaming, Delta Lake, performance, testing, and deployment."
---

# Scala Spark Conventions — Data Engineering Applications

These instructions apply to Scala Spark application code, SBT builds, and build scripts matched by the `applyTo` globs. They are authoritative for Apache Spark dependency scope, `SparkSession` usage, DataFrame/Dataset/RDD choices, schema and column-expression hygiene, joins, partitioning, caching, UDFs, Structured Streaming, Delta Lake, performance tuning, testing, packaging, and `spark-submit` settings; platform runbooks, cluster policies, and project-specific data contracts win where they define stricter runtime limits.

## Dependencies and Packaging

Keep Spark dependencies aligned with the cluster runtime and avoid bundling libraries the cluster already provides.

| Concern | Convention |
| --- | --- |
| SBT Spark version | Declare `val sparkVersion = "3.5.1"` when the project targets Spark 3.5.1. |
| SBT coordinates | Use `"org.apache.spark" %% "spark-core"`, `spark-sql`, `spark-mllib`, and `spark-streaming` as needed. |
| Dependency scope | Mark Spark artifacts `provided` because YARN, Kubernetes, Databricks, or the Spark cluster supplies them at runtime. |
| Maven coordinates | Use `<spark.version>3.5.1</spark.version>` and `<scala.binary.version>2.13</scala.binary.version>` with `spark-core_${scala.binary.version}`, `spark-sql_${scala.binary.version}`, `spark-mllib_${scala.binary.version}`, and `spark-streaming_${scala.binary.version}`. |
| Fat JARs | Bundle only application-specific libraries; do not include cluster-provided Spark libraries. |
| sbt-assembly | Add `addSbtPlugin("com.eed3si9n" % "sbt-assembly" % "2.1.5")` in `project/plugins.sbt` and configure `assembly / assemblyMergeStrategy` to discard `PathList("META-INF", _*)` before falling back to `MergeStrategy.first`. |

Use the literal Spark dependency scope `"provided"` when examples or project style include quotes; it carries the same deployment rule as `provided`.

Use `spark-submit` for cluster execution and keep cluster choices outside application code:

```bash
spark-submit \
  --class com.example.MainApp \
  --master yarn \
  --deploy-mode cluster \
  --num-executors 10 \
  --executor-memory 8g \
  --executor-cores 4 \
  --conf spark.sql.adaptive.enabled=true \
  --conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
  target/scala-2.13/my-app-assembly-1.0.jar \
  --input s3://bucket/input \
  --output s3://bucket/output
```

## SparkSession and Configuration

Use one `SparkSession` as the single entry point per JVM. Build it with `.appName(...)`, set safe defaults such as `spark.sql.shuffle.partitions` and `spark.serializer`, call `.getOrCreate()`, and then import `spark.implicits._` near the code that needs encoders. Do not hardcode `.master(...)` in production application code; pass `--master` at submit time so the same artifact runs locally, on YARN, and on Kubernetes.

| Setting | Convention | Rationale |
| --- | --- | --- |
| `spark.sql.shuffle.partitions` | Tune by data volume; start near Spark's default 200 and target roughly 128 MB per partition. | Oversized partitions spill, while too many tiny partitions waste scheduling overhead. |
| `spark.serializer` | Use `org.apache.spark.serializer.KryoSerializer` for production jobs when compatible. | Kryo reduces serialization cost for many workloads. |
| `spark.sql.crossJoin.enabled` | Set `false` unless a Cartesian product is intentional and reviewed. | Accidental cross joins create explosive data growth. |
| `spark.sql.adaptive.enabled` | Enable Adaptive Query Execution for Spark 3.x+. | AQE can coalesce partitions and mitigate skew at runtime. |
| `spark.sql.adaptive.coalescePartitions.enabled` | Enable with AQE. | Runtime partition coalescing reduces small-task overhead. |
| `spark.sql.adaptive.skewJoin.enabled` | Enable with AQE before writing manual salting. | Built-in skew handling is safer than duplicating data by hand. |

## DataFrames, Datasets, RDDs, and Schemas

Prefer the DataFrame API (`DataFrame`, untyped `Dataset[Row]`) for most analytical workloads because Catalyst can optimize it. Use typed `Dataset[Event]` only when compile-time schema safety is worth encoder and serialization overhead. Avoid raw RDDs unless the operation truly needs low-level control not expressible with DataFrames, Datasets, or Spark SQL.

Define schemas explicitly for semi-structured sources. Use `StructType`, `StructField`, `LongType`, `StringType`, `TimestampType`, `DecimalType(18, 2)`, and `ArrayType(StringType)` for JSON/CSV inputs where inference would scan data and infer fragile types. Parquet and Delta already carry schema metadata, so explicit schemas are optional unless a contract must be enforced.

Prefer `col("name")` or `$"amount"` in transformations over string-only projection such as `df.select("name", "amount")`. Column expressions fail earlier, compose with functions, and keep expressions visible to the optimizer. Select only required columns instead of `select("*")` so column pruning can reduce scan work.

## Joins, Skew, Partitioning, and Files

Design joins and partitioning around data size, cardinality, and downstream query patterns.

| Pattern | Use | Avoid |
| --- | --- | --- |
| Broadcast join | `largeDF.join(broadcast(smallLookupDF), Seq("key"), "left")` when the lookup fits in executor memory, typically under 100 MB. | Broadcasting large or unbounded tables. |
| Skew salting | Add a `salt` column with `(rand() * saltBuckets).cast("int")`, duplicate the smaller side with `(0 until saltBuckets).toDF("salt")`, join on `Seq("join_key", "salt")`, then drop `salt`. | Salting when the right side is not small enough to tolerate the `saltBuckets` multiplier. |
| AQE skew handling | Prefer `spark.sql.adaptive.skewJoin.enabled = true` on Spark 3.x+ before custom salting. | Manual skew logic that duplicates data without measurement. |
| Write partitioning | Use `partitionBy("year", "month")` for low-cardinality filter columns such as date parts. | Partitioning by high-cardinality values such as `user ID`, which creates millions of small files. |
| Repartition | Use `repartition(100, $"key")` to increase or evenly distribute partitions through a full shuffle. | Repartitioning repeatedly without checking the plan. |
| Coalesce | Use `coalesce(10)` only to reduce partition count without a full shuffle. | `coalesce(1)` on large datasets because it funnels all data through one task. |

Use `explain(true)` before expensive jobs. Filter before joins for predicate pushdown, use columnar formats such as Parquet, Delta, or ORC over CSV/JSON for analytical workloads, and avoid `distinct()` before `groupBy` when the aggregation already produces the intended result.

## Caching, UDFs, Windows, and Error Handling

Persist only reused DataFrames. Use `persist(StorageLevel.MEMORY_AND_DISK)`, materialize with an action such as `count()`, reuse the cached DataFrame, then call `unpersist()` when done. Prefer `MEMORY_AND_DISK` over `MEMORY_ONLY` to avoid recomputation after eviction, and never cache data used once.

Prefer built-in functions from `org.apache.spark.sql.functions._`, such as `upper`, `length`, `rank`, `dense_rank`, `row_number`, `sum`, `from_json`, `rand`, and `broadcast`, over UDFs. Built-ins stay inside Catalyst; UDFs require serialization and often block predicate pushdown. When a UDF is unavoidable, define it with `udf`, handle `null` with `Option`, and register it through `spark.udf.register` when Spark SQL compatibility is required.

Use `Window.partitionBy(...).orderBy(...)` for ranking, running totals, `lag`, and `lead`. Use `Window.unboundedPreceding`, `Window.currentRow`, and `rowsBetween` for explicit frame boundaries rather than relying on accidental defaults.

Quarantine corrupt records instead of hiding them. Read with `.option("mode", "PERMISSIVE")`, `.option("columnNameOfCorruptRecord", "_corrupt_record")`, filter clean rows with `$"_corrupt_record".isNull`, and write bad rows to a quarantine location. Use `spark.sparkContext.longAccumulator("parseErrors")` only for operational monitoring; accumulators are accurate only inside actions such as `count`, `collect`, or `write` and can over-count on task retry.

## Structured Streaming and Delta Lake

Structured Streaming jobs must be restartable and explicit about offsets, output mode, trigger, and checkpointing. Read Kafka with `.format("kafka")`, `kafka.bootstrap.servers`, `subscribe`, and `startingOffsets`; parse messages with `selectExpr("CAST(value AS STRING) as json")`, `from_json`, and `select("data.*")`. Write with `.writeStream`, a durable `checkpointLocation`, `outputMode("append")`, and `Trigger.ProcessingTime("30 seconds")` or `Trigger.AvailableNow`. Avoid `Trigger.Once` in production; use `AvailableNow` for bounded catch-up processing.

Use Delta Lake APIs deliberately. Use `DeltaTable.forPath(spark, "data/customers")`, `target.as("t").merge(updatesDF.as("s"), "t.id = s.id")`, `whenMatched.updateAll()`, `whenNotMatched.insertAll()`, and `execute()` for upserts. Use `.format("delta")`, `.option("timestampAsOf", "2025-01-15")`, and `.load(...)` for time travel. Use `target.optimize().executeCompaction()` and `target.vacuum(168)` only when the retention policy allows seven-day cleanup.

## Dynamic Allocation

Enable dynamic allocation for shared clusters where fixed executors waste capacity during idle stages.

| Config or flag | Purpose |
| --- | --- |
| `spark.dynamicAllocation.enabled=true` | Allows Spark to scale executors with workload demand. |
| `spark.dynamicAllocation.minExecutors=2` | Keeps a floor of executors available. |
| `spark.dynamicAllocation.maxExecutors=50` | Caps cluster usage to prevent monopolizing shared capacity. |
| `spark.dynamicAllocation.initialExecutors=5` | Sets the starting executor count before auto-scaling reacts. |
| `spark.dynamicAllocation.executorIdleTimeout=60s` | Removes idle executors after this duration; default is 60s. |
| `spark.dynamicAllocation.schedulerBacklogTimeout=1s` | Requests new executors when tasks are pending this long. |
| `spark.shuffle.service.enabled=true` | Required on YARN/Mesos so removed executors do not lose shuffle files. |
| `spark.dynamicAllocation.shuffleTracking.enabled=true` | Use on Kubernetes instead of an external shuffle service. |

Do not combine `--num-executors` with dynamic allocation because fixed and elastic executor policies conflict.

## Testing and Observability

Test pure transformation functions without Spark when possible. For DataFrame-level tests, share a local `SparkSession` in a base trait such as `SparkTestBase extends AnyFunSuite with BeforeAndAfterAll`, set `.master("local[2]")`, `.appName("test")`, `.config("spark.sql.shuffle.partitions", "2")`, import `spark.implicits._`, and call `spark.stop()` in `afterAll()`.

Use small deterministic inputs such as `Seq(Event(1L, "active", "US"), Event(2L, "inactive", "EU")).toDS()` and assert behavior with `count()`, `collect().head.status`, and named transformation functions such as `filterActive`. Avoid production-scale fixtures in unit tests; validate scale with integration or performance tests on representative data.

Keep example class names such as `TransformationsTest` and `EventPipelineTest` obviously illustrative. Do not copy placeholder application names such as `MyApplication` into production packages unless the project already uses that name.

## Preserved Spark API and Configuration Vocabulary

The following identifiers remain valid Spark vocabulary and should be preserved when refactoring examples or prose.

| Category | Identifiers |
| --- | --- |
| Status parsing examples | `ACTIVE`, `INACTIVE`, `UNKNOWN`, `DISABLED` |
| Column and window aliases | `adjusted_amount`, `name_length`, `hire_date`, `running_total` |
| Output and checkpoint paths | `checkpoints/events`, `data/quarantine` |
| Driver-safe inspection | `take(n)`, `show()`, `collect()` only for small or test data |
| Dynamic allocation keys | `minExecutors`, `maxExecutors`, `initialExecutors`, `executorIdleTimeout`, `schedulerBacklogTimeout` |
| Optimizer and design vocabulary | `select`, `join`, `lag/lead`, `type-checked`, `pre-partition`, `production-ready` |

## Good / Bad Examples

The examples below illustrate keeping Spark work optimizer-visible, schema-aware, and bounded.

**Good:**

```scala
import org.apache.spark.sql.functions._
import org.apache.spark.storage.StorageLevel

val schema = StructType(Seq(
  StructField("id", LongType, nullable = false),
  StructField("status", StringType, nullable = true),
  StructField("amount", DecimalType(18, 2), nullable = true)
))

val events = spark.read.schema(schema).json("data/events/*.json")
val activeByRegion = events
  .filter($"status" === "active")
  .select($"region", $"amount")
  .persist(StorageLevel.MEMORY_AND_DISK)

activeByRegion.count()
activeByRegion.groupBy($"region").agg(sum($"amount").as("total")).write.parquet("output/events")
activeByRegion.unpersist()
```

Why: The job declares its schema, filters and projects early, uses built-in aggregations, persists only reused data, and releases the cache.

**Bad:**

```scala
val df = spark.read.option("inferSchema", "true").json("data/events")
val upperUdf = udf((s: String) => s.toUpperCase)
val rows = df.collect()
val oneFile = df.withColumn("upper_name", upperUdf($"name")).coalesce(1)
oneFile.write.mode("overwrite").json("output/events")
```

Why: The job infers a fragile schema, uses a UDF for a built-in operation, collects data to the driver, and forces all output through one task.

## Conventions

| Rule | Rationale |
| --- | --- |
| Keep Spark dependencies `provided` and match `sparkVersion`, `<spark.version>`, and `<scala.binary.version>` to the runtime. | Cluster-supplied Spark libraries should not be duplicated in the application JAR. |
| Use one `SparkSession` per JVM and set `--master` at submit time. | Runtime topology stays configurable and the application avoids competing Spark contexts. |
| Prefer DataFrames, use Datasets for meaningful type safety, and avoid raw RDDs. | Catalyst can optimize declarative plans better than opaque low-level transformations. |
| Define explicit schemas for CSV/JSON and use embedded schemas for Parquet and Delta. | Jobs avoid expensive inference and schema drift. |
| Use `col()` or `$"..."`, built-in functions, predicate pushdown, and column pruning. | The optimizer sees the work and minimizes scans, shuffles, and serialization. |
| Broadcast only small lookup tables and use AQE or measured salting for skew. | Join performance improves without creating accidental data explosions. |
| Partition by low-cardinality filters and never use `coalesce(1)` on large data. | Output remains queryable without single-task bottlenecks or small-file storms. |
| Cache only reused data with `MEMORY_AND_DISK` and always `unpersist()`. | Cache memory stays available and recomputation is bounded. |
| Set Structured Streaming checkpoints and use `Trigger.ProcessingTime` or `Trigger.AvailableNow`. | Streams can recover safely and production jobs avoid deprecated one-shot semantics. |
| Enable dynamic allocation with the correct shuffle service or shuffle tracking for the cluster manager. | Shared clusters scale efficiently without losing shuffle data. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `spark-submit` flags such as `--class`, `--deploy-mode`, `--executor-memory`, and `--conf` for deployment settings. | Hardcode cluster `master` or executor sizing in application code. |
| Use `StructType` and typed columns for semi-structured sources. | Rely on `inferSchema=true` for large CSV/JSON inputs. |
| Use `broadcast`, AQE, and selective filters to reduce shuffle cost. | Allow accidental cross joins or ignore skewed keys. |
| Use `repartition` to increase or rebalance partitions and `coalesce` only to reduce them. | Use `coalesce(1)` to make output easier to browse. |
| Use built-in Spark SQL functions and `Window` expressions. | Write UDFs for `upper`, `length`, ranking, totals, or other built-in operations. |
| Quarantine corrupt records with `_corrupt_record`. | Count parse errors only with accumulators and drop bad data silently. |
| Use Delta `merge`, time travel, compaction, and `vacuum(168)` according to retention policy. | Vacuum or optimize without considering retention and reader requirements. |
| Use shared local Spark sessions for integration tests. | Start and stop a new Spark JVM for every assertion. |

## Checklist Before Opening a PR

- [ ] `build.sbt`, `build.sc`, or Maven coordinates keep Spark artifacts `provided` and aligned with the target runtime.
- [ ] Application code creates only one `SparkSession` and leaves `--master` to submission configuration.
- [ ] DataFrame, Dataset, or RDD choices are justified by optimizer visibility and type-safety needs.
- [ ] Semi-structured reads define schemas; Parquet or Delta reads rely on embedded schemas only when the contract allows it.
- [ ] Joins avoid accidental Cartesian products, handle skew, and broadcast only measured small inputs.
- [ ] Partition counts, `repartition`, `coalesce`, and output `partitionBy` settings match data volume and query patterns.
- [ ] Caches use `MEMORY_AND_DISK`, are materialized, and are released with `unpersist()`.
- [ ] UDFs are absent unless built-ins cannot express the logic, and unavoidable UDFs handle nulls.
- [ ] Streaming queries define `checkpointLocation`, `outputMode`, and a production-safe trigger.
- [ ] Delta operations preserve retention requirements and use merge/time-travel/compaction APIs intentionally.
- [ ] Tests cover pure transformations and DataFrame behavior with deterministic local Spark inputs.
- [ ] `spark-submit` or cluster config does not mix `--num-executors` with dynamic allocation.
