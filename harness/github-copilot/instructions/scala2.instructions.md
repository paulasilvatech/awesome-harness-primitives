---
applyTo: "**/*.scala,**/build.sbt,**/build.sc"
description: "Enforces Scala 2.12/2.13 conventions for functional style, type safety, formatting, SBT configuration, performance, concurrency, and testing."
---

# Scala 2 Conventions — Functional Production Code

This file applies to Scala source files and Scala build definitions matched by the `applyTo` globs. It is authoritative for Scala 2.12/2.13 language style, functional programming defaults, type-safety rules, SBT hygiene, performance escape hatches, concurrency patterns, and tests in those files; project-specific architecture, dependency policy, and framework instructions win where they define stricter rules. Follow the Databricks Scala Style Guide as the baseline and use these conventions when the guide leaves room for local judgment.

## Core Principles

### Write Simple Code
Code is written once but read and modified multiple times. Optimize for long-term readability and maintainability by writing simple code.

### Immutability by Default
- Always prefer `val` over `var`
- Use immutable collections from `scala.collection.immutable`
- Case class constructor parameters should NOT be mutable
- Use copy constructor to create modified instances

```scala
// Good - Immutable case class
case class Person(name: String, age: Int)

// Bad - Mutable case class
case class Person(name: String, var age: Int)

// To change values, use copy constructor
val p1 = Person("Peter", 15)
val p2 = p1.copy(age = 16)

// Good - Immutable collections
val users = List(User("Alice", 30), User("Bob", 25))
val updatedUsers = users.map(u => u.copy(age = u.age + 1))
```

### Pure Functions
- Functions should be deterministic and side-effect free
- Separate pure logic from effects
- Use explicit types for methods with effects

```scala
// Good - Pure function
def calculateTotal(items: List[Item]): BigDecimal =
  items.map(_.price).sum

// Bad - Impure function with side effects
def calculateTotal(items: List[Item]): BigDecimal = {
  println(s"Calculating total for ${items.size} items")  // Side effect
  val total = items.map(_.price).sum
  saveToDatabase(total)  // Side effect
  total
}
```

## Naming Conventions

### Classes and Objects

```scala
// Classes, traits, objects - PascalCase
class ClusterManager
trait Expression
object Configuration

// Packages - all lowercase ASCII
package com.databricks.resourcemanager

// Methods/functions - camelCase
def getUserById(id: Long): Option[User]
def processData(input: String): Result

// Constants - uppercase in companion object
object Configuration {
  val DEFAULT_PORT = 10000
  val MAX_RETRIES = 3
  val TIMEOUT_MS = 5000L
}
```

### Variables and Parameters

```scala
// Variables - camelCase, self-evident names
val serverPort = 1000
val clientPort = 2000
val maxRetryAttempts = 3

// One-character names OK in small, localized scope
for (i <- 0 until 10) {
  // ...
}

// Do NOT use "l" (Larry) - looks like "1", "|", "I"
```

### Enumerations

```scala
// Enumeration object - PascalCase
// Values - UPPER_CASE with underscores
private object ParseState extends Enumeration {
  type ParseState = Value

  val PREFIX,
      TRIM_BEFORE_SIGN,
      SIGN,
      VALUE,
      UNIT_BEGIN,
      UNIT_END = Value
}
```

## Syntactic Style

### Line Length and Spacing

```scala
// Limit lines to 100 characters
// One space before and after operators
def add(int1: Int, int2: Int): Int = int1 + int2

// One space after commas
val list = List("a", "b", "c")

// One space after colons
def getConf(key: String, defaultValue: String): String = {
  // code
}

// Use 2-space indentation
if (true) {
  println("Wow!")
}

// 4-space indentation for long parameter lists
def newAPIHadoopFile[K, V, F <: NewInputFormat[K, V]](
    path: String,
    fClass: Class[F],
    kClass: Class[K],
    vClass: Class[V],
    conf: Configuration = hadoopConfiguration): RDD[(K, V)] = {
  // method body
}

// Class with long parameters
class Foo(
    val param1: String,  // 4 space indent
    val param2: String,
    val param3: Array[Byte])
  extends FooInterface  // 2 space indent
  with Logging {

  def firstMethod(): Unit = { ... }  // blank line above
}
```

### Rule of 30

- A method should contain less than 30 lines of code
- A class should contain less than 30 methods

### Curly Braces

```scala
// Always use curly braces for multi-line blocks
if (true) {
  println("Wow!")
}

// Exception: one-line ternary (side-effect free)
val result = if (condition) value1 else value2

// Always use braces for try-catch
try {
  foo()
} catch {
  case e: Exception => handle(e)
}
```

### Long Literals

```scala
// Use uppercase L for long literals
val longValue = 5432L  // Do this
val badValue = 5432l   // Don't do this - hard to see
```

### Parentheses

```scala
// Methods with side-effects - use parentheses
class Job {
  def killJob(): Unit = { ... }  // Correct - changes state
  def getStatus: JobStatus = { ... }  // Correct - no side-effect
}

// Callsite should match declaration
new Job().killJob()  // Correct
new Job().getStatus  // Correct
```

### Imports

```scala
// Avoid wildcard imports unless importing 6+ entities
import scala.collection.mutable.{Map, HashMap, ArrayBuffer}

// OK to use wildcard for implicits or 6+ items
import scala.collection.JavaConverters._
import java.util.{Map, HashMap, List, ArrayList, Set, HashSet}

// Always use absolute paths
import scala.util.Random  // Good
// import util.Random     // Don't use relative

// Import order (with blank lines):
import java.io.File
import javax.servlet.http.HttpServlet

import scala.collection.mutable.HashMap
import scala.util.Random

import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD

import com.databricks.MyClass
```

### Pattern Matching

```scala
// Put match on same line if method is entirely pattern match
def test(msg: Message): Unit = msg match {
  case TextMessage(text) => handleText(text)
  case ImageMessage(url) => handleImage(url)
}

// Single case closures - same line
list.zipWithIndex.map { case (elem, i) =>
  // process
}

// Multiple cases - indent and wrap
list.map {
  case a: Foo => processFoo(a)
  case b: Bar => processBar(b)
  case _ => handleDefault()
}

// Match on type only - don't expand all args
case class Pokemon(name: String, weight: Int, hp: Int, attack: Int, defense: Int)

// Bad - brittle when fields change
targets.foreach {
  case Pokemon(_, _, hp, _, defense) =>
    // error prone
}

// Good - match on type
targets.foreach {
  case p: Pokemon =>
    val loss = math.min(0, myAttack - p.defense)
    p.copy(hp = p.hp - loss)
}
```

### Anonymous Functions

```scala
// Avoid excessive parentheses
// Correct
list.map { item =>
  transform(item)
}

// Correct
list.map(item => transform(item))

// Wrong - unnecessary braces
list.map(item => {
  transform(item)
})

// Wrong - excessive nesting
list.map({ item => ... })
```

### Infix Methods

```scala
// Avoid infix for non-symbolic methods
list.map(func)  // Correct
list map func   // Wrong

// OK for operators
arrayBuffer += elem
```

## Language Features

### Avoid apply() on Classes

```scala
// Avoid apply on classes - hard to trace
class TreeNode {
  def apply(name: String): TreeNode = { ... }  // Don't do this
}

// OK on companion objects as factory
object TreeNode {
  def apply(name: String): TreeNode = new TreeNode(name)  // OK
}
```

### override Modifier

```scala
// Always use override - even for abstract methods
trait Parent {
  def hello(data: Map[String, String]): Unit
}

class Child extends Parent {
  // Without override, this might not actually override!
  override def hello(data: Map[String, String]): Unit = {
    println(data)
  }
}
```

### Avoid Destructuring in Constructors

```scala
// Don't use destructuring binds in constructors
class MyClass {
  // Bad - creates non-transient Tuple2
  @transient private val (a, b) = someFuncThatReturnsTuple2()

  // Good
  @transient private val tuple = someFuncThatReturnsTuple2()
  @transient private val a = tuple._1
  @transient private val b = tuple._2
}
```

### Avoid Call-by-Name

```scala
// Avoid call-by-name parameters
// Bad - caller can't tell if executed once or many times
def print(value: => Int): Unit = {
  println(value)
  println(value + 1)
}

// Good - explicit function type
def print(value: () => Int): Unit = {
  println(value())
  println(value() + 1)
}
```

### Avoid Multiple Parameter Lists

```scala
// Avoid multiple parameter lists (except for implicits)
// Bad
case class Person(name: String, age: Int)(secret: String)

// Good
case class Person(name: String, age: Int, secret: String)

// Exception: separate list for implicits (but avoid implicits!)
def foo(x: Int)(implicit ec: ExecutionContext): Future[Int]
```

### Symbolic Methods

```scala
// Only use for arithmetic operators
class Vector {
  def +(other: Vector): Vector = { ... }  // OK
  def -(other: Vector): Vector = { ... }  // OK
}

// Don't use for other methods
// Bad
channel ! msg
stream1 >>= stream2

// Good
channel.send(msg)
stream1.join(stream2)
```

### Type Inference

```scala
// Always type public methods
def getUserById(id: Long): Option[User] = { ... }

// Always type implicit methods
implicit def stringToInt(s: String): Int = s.toInt

// Type variables when not obvious (3 second rule)
val user: User = complexComputation()

// OK to omit when obvious
val count = 5
val name = "Alice"
```

### Return Statements

```scala
// Avoid return in closures - uses exceptions under the hood
def receive(rpc: WebSocketRPC): Option[Response] = {
  tableFut.onComplete { table =>
    if (table.isFailure) {
      return None  // Don't do this - wrong thread!
    }
  }
}

// Use return as guard to simplify control flow
def doSomething(obj: Any): Any = {
  if (obj eq null) {
    return null
  }
  // do something
}

// Use return to break loops early
while (true) {
  if (cond) {
    return
  }
}
```

### Recursion and Tail Recursion

```scala
// Avoid recursion unless naturally recursive (trees, graphs)
// Use @tailrec for tail-recursive methods
@scala.annotation.tailrec
def max0(data: Array[Int], pos: Int, max: Int): Int = {
  if (pos == data.length) {
    max
  } else {
    max0(data, pos + 1, if (data(pos) > max) data(pos) else max)
  }
}

// Prefer explicit loops for clarity
def max(data: Array[Int]): Int = {
  var max = Int.MinValue
  for (v <- data) {
    if (v > max) {
      max = v
    }
  }
  max
}
```

### Implicits

```scala
// Avoid implicits unless:
// 1. Building a DSL
// 2. Implicit type parameters (ClassTag, TypeTag)
// 3. Private type conversions within your class

// If you must use them, don't overload
object ImplicitHolder {
  // Bad - can't selectively import
  def toRdd(seq: Seq[Int]): RDD[Int] = { ... }
  def toRdd(seq: Seq[Long]): RDD[Long] = { ... }
}

// Good - distinct names
object ImplicitHolder {
  def intSeqToRdd(seq: Seq[Int]): RDD[Int] = { ... }
  def longSeqToRdd(seq: Seq[Long]): RDD[Long] = { ... }
}
```

## Type Safety

### Algebraic Data Types

```scala
// Sum types - sealed traits with case classes
sealed trait PaymentMethod
case class CreditCard(number: String, cvv: String) extends PaymentMethod
case class PayPal(email: String) extends PaymentMethod
case class BankTransfer(account: String, routing: String) extends PaymentMethod

def processPayment(payment: PaymentMethod): Either[Error, Receipt] = payment match {
  case CreditCard(number, cvv) => chargeCreditCard(number, cvv)
  case PayPal(email) => chargePayPal(email)
  case BankTransfer(account, routing) => chargeBankAccount(account, routing)
}

// Product types - case classes
case class User(id: Long, name: String, email: String, age: Int)
case class Order(id: Long, userId: Long, items: List[Item], total: BigDecimal)
```

### Option over null

```scala
// Use Option instead of null
def findUserById(id: Long): Option[User] = {
  database.query(id)
}

// Use Option() to guard against nulls
def myMethod1(input: String): Option[String] = Option(transform(input))

// Don't use Some() - it won't protect against null
def myMethod2(input: String): Option[String] = Some(transform(input)) // Bad

// Pattern matching on Option
def processUser(id: Long): String = findUserById(id) match {
  case Some(user) => s"Found: ${user.name}"
  case None => "User not found"
}

// Don't call get() unless absolutely sure
val user = findUserById(123).get  // Dangerous!

// Use getOrElse, map, flatMap, fold instead
val name = findUserById(123).map(_.name).getOrElse("Unknown")
```

### Error Handling with Either

```scala
sealed trait ValidationError
case class InvalidEmail(email: String) extends ValidationError
case class InvalidAge(age: Int) extends ValidationError
case class MissingField(field: String) extends ValidationError

def validateUser(data: Map[String, String]): Either[ValidationError, User] = {
  for {
    name <- data.get("name").toRight(MissingField("name"))
    email <- data.get("email").toRight(MissingField("email"))
    validEmail <- validateEmail(email)
    ageStr <- data.get("age").toRight(MissingField("age"))
    age <- ageStr.toIntOption.toRight(InvalidAge(-1))
  } yield User(name, validEmail, age)
}
```

### Try vs Exceptions

```scala
// Don't return Try from APIs
// Bad
def getUser(id: Long): Try[User]

// Good - explicit throws
@throws(classOf[DatabaseConnectionException])
def getUser(id: Long): Option[User]

// Use NonFatal for catching exceptions
import scala.util.control.NonFatal

try {
  dangerousOperation()
} catch {
  case NonFatal(e) =>
    logger.error("Operation failed", e)
  case e: InterruptedException =>
    // handle interruption
}
```

## Collections

### Prefer Immutable Collections

```scala
import scala.collection.immutable._

// Good
val numbers = List(1, 2, 3, 4, 5)
val doubled = numbers.map(_ * 2)
val evens = numbers.filter(_ % 2 == 0)

val userMap = Map(
  1L -> "Alice",
  2L -> "Bob"
)
val updated = userMap + (3L -> "Charlie")

// Use Stream (Scala 2.12) or LazyList (Scala 2.13) for lazy sequences
val fibonacci: LazyList[BigInt] =
  BigInt(0) #:: BigInt(1) #:: fibonacci.zip(fibonacci.tail).map { case (a, b) => a + b }

val first10 = fibonacci.take(10).toList
```

### Monadic Chaining

```scala
// Avoid chaining more than 3 operations
// Break after flatMap
// Don't chain with if-else blocks

// Bad - too complex
database.get(name).flatMap { elem =>
  elem.data.get("address").flatMap(Option.apply)
}

// Good - more readable
def getAddress(name: String): Option[String] = {
  if (!database.contains(name)) {
    return None
  }

  database(name).data.get("address") match {
    case Some(null) => None
    case Some(addr) => Option(addr)
    case None => None
  }
}

// Don't chain with if-else
// Bad
if (condition) {
  Seq(1, 2, 3)
} else {
  Seq(1, 2, 3)
}.map(_ + 1)

// Good
val seq = if (condition) Seq(1, 2, 3) else Seq(4, 5, 6)
seq.map(_ + 1)
```

## Performance

### Use while Loops

```scala
// For performance-critical code, use while instead of for/map
val arr = Array.fill(1000)(Random.nextInt())

// Slow
val newArr = arr.zipWithIndex.map { case (elem, i) =>
  if (i % 2 == 0) 0 else elem
}

// Fast
val newArr = new Array[Int](arr.length)
var i = 0
while (i < arr.length) {
  newArr(i) = if (i % 2 == 0) 0 else arr(i)
  i += 1
}
```

### Option vs null

```scala
// For performance-critical code, prefer null over Option
class Foo {
  @javax.annotation.Nullable
  private[this] var nullableField: Bar = _
}
```

### Use private[this]

```scala
// private[this] generates fields, not accessor methods
class MyClass {
  private val field1 = ...        // Might use accessor
  private[this] val field2 = ...  // Direct field access

  def perfSensitiveMethod(): Unit = {
    var i = 0
    while (i < 1000000) {
      field2  // Guaranteed field access
      i += 1
    }
  }
}
```

### Java Collections

```scala
// For performance, prefer Java collections
import java.util.{ArrayList, HashMap}

val list = new ArrayList[String]()
val map = new HashMap[String, Int]()
```

## Concurrency

### Prefer ConcurrentHashMap

```scala
// Use java.util.concurrent.ConcurrentHashMap
private[this] val map = new java.util.concurrent.ConcurrentHashMap[String, String]

// Or synchronized map for low contention
private[this] val map = java.util.Collections.synchronizedMap(
  new java.util.HashMap[String, String]
)
```

### Explicit Synchronization

```scala
class Manager {
  private[this] var count = 0
  private[this] val map = new java.util.HashMap[String, String]

  def update(key: String, value: String): Unit = synchronized {
    map.put(key, value)
    count += 1
  }

  def getCount: Int = synchronized { count }
}
```

### Atomic Variables

```scala
import java.util.concurrent.atomic._

// Prefer Atomic over @volatile
val initialized = new AtomicBoolean(false)

// Clearly express only-once execution
if (!initialized.getAndSet(true)) {
  initialize()
}
```

## Testing

### Intercept Specific Exceptions

```scala
import org.scalatest._

// Bad - too broad
intercept[Exception] {
  thingThatThrows()
}

// Good - specific type
intercept[IllegalArgumentException] {
  thingThatThrows()
}
```

## SBT Configuration

```scala
// build.sbt
ThisBuild / version := "0.1.0-SNAPSHOT"
ThisBuild / scalaVersion := "2.13.12"
ThisBuild / organization := "com.example"

lazy val root = (project in file("."))
  .settings(
    name := "my-application",

    libraryDependencies ++= Seq(
      "org.typelevel" %% "cats-core" % "2.10.0",
      "org.typelevel" %% "cats-effect" % "3.5.2",

      // Testing
      "org.scalatest" %% "scalatest" % "3.2.17" % Test,
      "org.scalatestplus" %% "scalacheck-1-17" % "3.2.17.0" % Test
    ),

    scalacOptions ++= Seq(
      "-encoding", "UTF-8",
      "-feature",
      "-unchecked",
      "-deprecation",
      "-Xfatal-warnings"
    )
  )
```

## Miscellaneous

### Use nanoTime

```scala
// Use nanoTime for durations, not currentTimeMillis
val start = System.nanoTime()
doWork()
val elapsed = System.nanoTime() - start

import java.util.concurrent.TimeUnit
val elapsedMs = TimeUnit.NANOSECONDS.toMillis(elapsed)
```

### URI over URL

```scala
// Use URI instead of URL (URL.equals does DNS lookup!)
val uri = new java.net.URI("http://example.com")
// Not: val url = new java.net.URL("http://example.com")
```

## Good / Bad Examples

The examples below illustrate the default Scala 2 stance: immutable, typed, explicit code for normal paths, and measured escape hatches only for performance-critical code.

**Good:**

```scala
import scala.util.control.NonFatal

final case class User(id: Long, name: String, email: String)

def findUserById(id: Long): Option[User] =
  Option(database.lookup(id))

def updateAge(user: User, age: Int): Either[ValidationError, User] =
  if (age < 0) Left(InvalidAge(age)) else Right(user.copy(age = age))

try {
  dangerousOperation()
} catch {
  case NonFatal(e) => logger.error("Operation failed", e)
}
```

Why: The code uses immutable case-class updates, explicit `Option` and `Either` results, a typed public method boundary, and `NonFatal` exception handling without hiding side-effects.

**Bad:**

```scala
case class User(name: String, var age: Int)

def getUser(id: Long) = database.lookup(id).get

def calculateTotal(items: List[Item]): BigDecimal = {
  println(items.size)
  saveToDatabase(items.map(_.price).sum)
  items.map(_.price).sum
}
```

Why: The code mutates a case class, relies on inferred public API types, calls `get`, mixes pure calculation with side-effects, and makes failure behavior hard to review.

## Conventions

| Rule | Rationale |
| --- | --- |
| Prefer simple, immutable Scala 2.12/2.13 code using `val`, immutable collections, and case-class `copy` updates. | Readability and value semantics survive long-term maintenance better than mutation. |
| Keep pure functions deterministic and isolate side-effect boundaries with explicit result types. | Tests stay predictable and reviewers can see where effects occur. |
| Use `PascalCase`, `camelCase`, lowercase ASCII packages, and `UPPER_CASE` companion-object constants such as `DEFAULT_PORT`, `MAX_RETRIES`, and `TIMEOUT_MS`. | Names match the Databricks style guide and avoid ambiguous local conventions. |
| Format with 100-character lines, 2-space blocks, 4-space wrapped parameter indentation, spaces around operators, uppercase `L` long literals, and braces for multi-line blocks and try-catch. | Consistent layout prevents style churn and hard-to-read parser edge cases. |
| Keep methods under 30 lines and classes under 30 methods. | The Rule of 30 keeps review units small enough to reason about. |
| Use absolute imports, ordered import groups, and wildcard imports only for implicits or six or more imported names. | Imports stay deterministic and do not hide dependency sources. |
| Avoid non-symbolic infix calls, class-level `apply`, constructor destructuring, call-by-name, multiple parameter lists except implicits, overloaded implicits, and unnecessary symbolic methods. | These features make call sites harder to trace in production Scala 2 code. |
| Type public, implicit, and non-obvious values explicitly; rely on inference only when the type is clear within three seconds. | Public contracts remain stable and compiler errors stay localized. |
| Model absence and validation with `Option` and `Either`; use `@throws` for Java-facing exception contracts and catch `NonFatal` before interruption-sensitive exceptions. | Failure behavior is explicit without swallowing thread interruption or process-control signals. |
| Prefer immutable collections and readable chains; switch to `while`, `null`, `private[this]`, Java collections, or atomic/concurrent primitives only in measured performance-critical paths. | Normal code stays safe while hot paths can avoid avoidable allocation and accessor overhead. |
| Configure SBT with explicit `scalaVersion`, `organization`, `libraryDependencies`, and `scalacOptions` including `-encoding UTF-8`, `-feature`, `-unchecked`, `-deprecation`, and `-Xfatal-warnings`. | Build settings document the supported Scala line and fail risky compiler warnings early. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `val`, immutable `List`/`Map`, and `copy` for updates. | Put `var` in case class constructor parameters or expose mutable collections by default. |
| Keep pure calculations separate from logging, persistence, and network effects. | Hide side-effects inside methods that look like pure value calculations. |
| Declare side-effecting methods with parentheses and call them with parentheses. | Declare state-changing methods as nullary accessors. |
| Use `Option()` to guard nullable values and `getOrElse`, `map`, `flatMap`, or `fold` to consume them. | Wrap nullable values with `Some()` or call `.get` unless the invariant is proven locally. |
| Use sealed traits and case classes for algebraic data types. | Encode closed variants as raw strings or unvalidated primitives. |
| Use `@scala.annotation.tailrec` on tail-recursive methods. | Use recursion for ordinary loops or leave tail recursion unchecked. |
| Use `java.util.concurrent.ConcurrentHashMap`, synchronized maps, or `AtomicBoolean` for shared mutable state. | Prefer `@volatile` or unsynchronized mutable maps for compound concurrent updates. |
| Measure before using `while`, `null`, `private[this]`, or Java collections for speed. | Optimize ordinary business code before profiling. |
| Intercept specific exceptions in ScalaTest. | Use broad `intercept[Exception]` assertions. |
| Use `System.nanoTime()` with `TimeUnit.NANOSECONDS` for durations and `java.net.URI` instead of `java.net.URL`. | Measure elapsed time with `currentTimeMillis` or rely on `URL.equals` DNS behavior. |

## Checklist Before Opening a PR

- [ ] Public and implicit APIs have explicit result types.
- [ ] New values default to `val` and immutable collections; any `var`, `null`, Java collection, or `while` loop is justified by performance or interoperability.
- [ ] Methods stay under 30 lines, classes stay under 30 methods, and lines stay within 100 characters.
- [ ] Imports are absolute, grouped, and avoid wildcard imports except for implicits or six or more entities.
- [ ] Absence, validation, and errors use `Option`, `Either`, `@throws`, and `NonFatal` according to the conventions above.
- [ ] Concurrency uses explicit synchronization, concurrent collections, or atomic variables.
- [ ] SBT settings preserve Scala 2.12/2.13 compatibility and strict compiler options.
- [ ] Tests intercept specific exceptions and cover behavior rather than implementation noise.

## References

- Databricks Scala Style Guide: https://github.com/databricks/scala-style-guide
- Example URI literal preserved for URL/URI guidance: http://example.com
