---
applyTo: "**/*.java,**/*.gradle,**/*.gradle.kts,**/pom.xml"
description: "Enforces conventions for upgrading Java projects from JDK 17 to JDK 21, including language features, APIs, build flags, runtime warnings, GC, performance, and testing."
---

# Java 17 to Java 21 Upgrade Conventions — Modern JDK Adoption

These instructions apply to Java source and Maven/Gradle build files matched by `**/*.java`, `**/*.gradle`, `**/*.gradle.kts`, and `**/pom.xml`. They are authoritative for adopting JDK 18 through JDK 21 language features, APIs, build flags, runtime warnings, GC options, migration choices, performance checks, and testing practices; project-specific architecture, framework, and production-support primitives win where they impose stricter compatibility, release, or deployment rules.

## Major Language Features in JDK 18-21

### Pattern Matching for switch (JEP 441 - Standard in 21)

**Enhanced switch Expressions and Statements**

When working with switch constructs:
- Suggest converting traditional switch to pattern matching where appropriate
- Use pattern matching for type checking and destructuring
- Example upgrade patterns:
```java
// Old approach (Java 17)
public String processObject(Object obj) {
    if (obj instanceof String) {
        String s = (String) obj;
        return s.toUpperCase();
    } else if (obj instanceof Integer) {
        Integer i = (Integer) obj;
        return i.toString();
    }
    return "unknown";
}

// New approach (Java 21)
public String processObject(Object obj) {
    return switch (obj) {
        case String s -> s.toUpperCase();
        case Integer i -> i.toString();
        case null -> "null";
        default -> "unknown";
    };
}
```

- Support guarded patterns:
```java
switch (obj) {
    case String s when s.length() > 10 -> "Long string: " + s;
    case String s -> "Short string: " + s;
    case Integer i when i > 100 -> "Large number: " + i;
    case Integer i -> "Small number: " + i;
    default -> "Other";
}
```

### Record Patterns (JEP 440 - Standard in 21)

**Destructuring Records in Pattern Matching**

When working with records:
- Suggest using record patterns for destructuring
- Combine with switch expressions for powerful data processing
- Example usage:
```java
public record Point(int x, int y) {}
public record ColoredPoint(Point point, Color color) {}

// Destructuring in switch
public String describe(Object obj) {
    return switch (obj) {
        case Point(var x, var y) -> "Point at (" + x + ", " + y + ")";
        case ColoredPoint(Point(var x, var y), var color) -> 
            "Colored point at (" + x + ", " + y + ") in " + color;
        default -> "Unknown shape";
    };
}
```

- Use in complex pattern matching:
```java
// Nested record patterns
switch (shape) {
    case Rectangle(ColoredPoint(Point(var x1, var y1), var c1), 
                   ColoredPoint(Point(var x2, var y2), var c2)) 
        when c1 == c2 -> "Monochrome rectangle";
    case Rectangle r -> "Multi-colored rectangle";
}
```

### Virtual Threads (JEP 444 - Standard in 21)

**Lightweight Concurrency**

When working with concurrency:
- Suggest Virtual Threads for high-throughput, concurrent applications
- Use `Thread.ofVirtual()` for creating virtual threads
- Example migration patterns:
```java
// Old platform thread approach
ExecutorService executor = Executors.newFixedThreadPool(100);
executor.submit(() -> {
    // blocking I/O operation
    httpClient.send(request);
});

// New virtual thread approach
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> {
        // blocking I/O operation - now scales to millions
        httpClient.send(request);
    });
}
```

- Use structured concurrency patterns:
```java
// Structured concurrency (Preview)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser(userId));
    Future<String> order = scope.fork(() -> fetchOrder(orderId));
    
    scope.join();           // Join all subtasks
    scope.throwIfFailed();  // Propagate errors
    
    return processResults(user.resultNow(), order.resultNow());
}
```

### String Templates (JEP 430 - Preview in 21)

**Safe String Interpolation**

When working with string formatting:
- Suggest String Templates for safe string interpolation (preview feature)
- Enable preview features with `--enable-preview`
- Example usage:
```java
// Traditional concatenation
String message = "Hello, " + name + "! You have " + count + " messages.";

// String Templates (Preview)
String message = STR."Hello, \{name}! You have \{count} messages.";

// Safe HTML generation
String html = HTML."<p>User: \{username}</p>";

// Safe SQL queries  
PreparedStatement stmt = SQL."SELECT * FROM users WHERE id = \{userId}";
```

### Sequenced Collections (JEP 431 - Standard in 21)

**Enhanced Collection Interfaces**

When working with collections:
- Use new `SequencedCollection`, `SequencedSet`, `SequencedMap` interfaces
- Access first/last elements uniformly across collection types
- Example usage:
```java
// New methods available on Lists, Deques, LinkedHashSet, etc.
List<String> list = List.of("first", "middle", "last");
String first = list.getFirst();  // "first"
String last = list.getLast();    // "last"
List<String> reversed = list.reversed(); // ["last", "middle", "first"]

// Works with any SequencedCollection
SequencedSet<String> set = new LinkedHashSet<>();
set.addFirst("start");
set.addLast("end");
String firstElement = set.getFirst();
```

### Unnamed Patterns and Variables (JEP 443 - Preview in 21)

**Simplified Pattern Matching**

When working with pattern matching:
- Use unnamed patterns `_` for values you don't need
- Simplify switch expressions and record patterns
- Example usage:
```java
// Ignore unused variables
switch (ball) {
    case RedBall(_) -> "Red ball";     // Don't care about size
    case BlueBall(var size) -> "Blue ball size " + size;
}

// Ignore parts of records
switch (point) {
    case Point(var x, _) -> "X coordinate: " + x; // Ignore Y
    case ColoredPoint(Point(_, var y), _) -> "Y coordinate: " + y;
}

// Exception handling with unnamed variables
try {
    riskyOperation();
} catch (IOException | SQLException _) {
    // Don't need exception details
    handleError();
}
```

### Scoped Values (JEP 446 - Preview in 21)

**Improved Context Propagation**

When working with thread-local data:
- Consider Scoped Values as a modern alternative to ThreadLocal
- Better performance and clearer semantics for virtual threads
- Example usage:
```java
// Define scoped value
private static final ScopedValue<String> USER_ID = ScopedValue.newInstance();

// Set and use scoped value
ScopedValue.where(USER_ID, "user123")
    .run(() -> {
        processRequest(); // Can access USER_ID.get() anywhere in call chain
    });

// In nested method
public void processRequest() {
    String userId = USER_ID.get(); // "user123"
    // Process with user context
}
```

## API Enhancements and New Features

### UTF-8 by Default (JEP 400 - Standard in 18)

When working with file I/O:
- UTF-8 is now the default charset on all platforms
- Remove explicit charset specifications where UTF-8 was intended
- Example simplification:
```java
// Old explicit UTF-8 specification
Files.readString(path, StandardCharsets.UTF_8);
Files.writeString(path, content, StandardCharsets.UTF_8);

// New default behavior (Java 18+)
Files.readString(path);  // Uses UTF-8 by default
Files.writeString(path, content);  // Uses UTF-8 by default
```

### Simple Web Server (JEP 408 - Standard in 18)

When needing basic HTTP server:
- Use built-in `jwebserver` command or `com.sun.net.httpserver` enhancements
- Great for testing and development
- Example usage:
```java
// Command line
$ jwebserver -p 8080 -d /path/to/files

// Programmatic usage
HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
server.createContext("/", new SimpleFileHandler(Path.of("/tmp")));
server.start();
```

### Internet-Address Resolution SPI (JEP 418 - Standard in 19)

When working with custom DNS resolution:
- Implement `InetAddressResolverProvider` for custom address resolution
- Useful for service discovery and testing scenarios

### Key Encapsulation Mechanism API (JEP 452 - Standard in 21)

When working with post-quantum cryptography:
- Use KEM API for key encapsulation mechanisms
- Example usage:
```java
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-KEM");
KeyPair kp = kpg.generateKeyPair();

KEM kem = KEM.getInstance("ML-KEM");
KEM.Encapsulator encapsulator = kem.newEncapsulator(kp.getPublic());
KEM.Encapsulated encapsulated = encapsulator.encapsulate();
```

## Deprecations and Warnings

### Finalization Deprecation (JEP 421 - Deprecated in 18)

When encountering `finalize()` methods:
- Remove finalize methods and use alternatives
- Suggest Cleaner API or try-with-resources
- Example migration:
```java
// Deprecated finalize approach
@Override
protected void finalize() throws Throwable {
    cleanup();
}

// Modern approach with Cleaner
private static final Cleaner CLEANER = Cleaner.create();

public MyResource() {
    cleaner.register(this, new CleanupTask(nativeResource));
}

private static class CleanupTask implements Runnable {
    private final long nativeResource;
    
    CleanupTask(long nativeResource) {
        this.nativeResource = nativeResource;
    }
    
    public void run() {
        cleanup(nativeResource);
    }
}
```

### Dynamic Agent Loading (JEP 451 - Warnings in 21)

When working with agents or instrumentation:
- Add `-XX:+EnableDynamicAgentLoading` to suppress warnings if needed
- Consider loading agents at startup instead of dynamically
- Update tooling to use startup agent loading

## Build Configuration Updates

### Preview Features

For projects using preview features:
- Add `--enable-preview` to compiler and runtime
- Maven configuration:
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <release>21</release>
        <compilerArgs>
            <arg>--enable-preview</arg>
        </compilerArgs>
    </configuration>
</plugin>

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <argLine>--enable-preview</argLine>
    </configuration>
</plugin>
```

- Gradle configuration:
```kotlin
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

tasks.withType<JavaCompile> {
    options.compilerArgs.add("--enable-preview")
}

tasks.withType<Test> {
    jvmArgs("--enable-preview")
}
```

### Virtual Threads Configuration

For applications using Virtual Threads:
- No special JVM flags required (standard feature in 21)
- Consider these system properties for debugging:
```bash
-Djdk.virtualThreadScheduler.parallelism=N  # Set carrier thread count
-Djdk.virtualThreadScheduler.maxPoolSize=N  # Set max pool size
```

## Runtime and GC Improvements

### Generational ZGC (JEP 439 - Available in 21)

When configuring garbage collection:
- Try Generational ZGC for better performance
- Enable with: `-XX:+UseZGC -XX:+ZGenerational`
- Monitor allocation patterns and GC behavior

## Migration Strategy

Treat the upgrade as a compatibility-preserving modernization. Ensure Maven/Gradle supports JDK 21 before changing source, prefer standard Java 21 features before preview features, adopt pattern matching for switch and record patterns where they simplify existing code, consider Virtual Threads only for I/O-heavy concurrency, and benchmark GC or threading changes before claiming performance improvements.

### Upgrade Review Signals

When reviewing code for Java 21 upgrade:
- [ ] Convert appropriate instanceof chains to switch expressions
- [ ] Use record patterns for data destructuring
- [ ] Replace ThreadLocal with ScopedValues where appropriate
- [ ] Consider Virtual Threads for high-concurrency scenarios
- [ ] Remove explicit UTF-8 charset specifications
- [ ] Replace finalize() methods with Cleaner or try-with-resources
- [ ] Use SequencedCollection methods for first/last access patterns
- [ ] Add preview flags only for preview features in use

### Common Migration Patterns

1. **Switch Enhancement**:
   ```java
   // From instanceof chains to switch expressions
   if (obj instanceof String s) return processString(s);
   else if (obj instanceof Integer i) return processInt(i);
   // becomes:
   return switch (obj) {
       case String s -> processString(s);
       case Integer i -> processInt(i);
       default -> processDefault(obj);
   };
   ```

2. **Virtual Thread Adoption**:
   ```java
   // From platform threads to virtual threads
   Executors.newFixedThreadPool(200)
   // becomes:
   Executors.newVirtualThreadPerTaskExecutor()
   ```

3. **Record Pattern Usage**:
   ```java
   // From manual destructuring to record patterns
   if (point instanceof Point p) {
       int x = p.x();
       int y = p.y();
   }
   // becomes:
   if (point instanceof Point(var x, var y)) {
       // use x and y directly
   }
   ```

## Performance Considerations

- Virtual Threads excel with blocking I/O but may not benefit CPU-intensive tasks
- Generational ZGC can reduce GC overhead for most applications
- Pattern matching in switch is generally more efficient than instanceof chains
- SequencedCollection methods provide O(1) access to first/last elements
- Scoped Values have lower overhead than ThreadLocal for virtual threads

## Testing Recommendations

- Test Virtual Thread applications under high concurrency
- Verify pattern matching covers all expected cases
- Performance test with Generational ZGC vs other collectors
- Validate UTF-8 default behavior across different platforms
- Test preview features thoroughly before production use



## Good / Bad Examples

The examples below illustrate a safe Java 21 refactor from type checks to pattern matching for switch.

**Good:**

```java
public String processObject(Object obj) {
    return switch (obj) {
        case String s when s.length() > 10 -> "Long string: " + s;
        case String s -> s.toUpperCase();
        case Integer i -> i.toString();
        case null -> "null";
        default -> "unknown";
    };
}
```

Why: The switch is exhaustive, handles `null`, preserves guarded pattern behavior, and removes unsafe casts.

**Bad:**

```java
public String processObject(Object obj) {
    if (obj instanceof String) {
        String s = (String) obj;
        return s.toUpperCase();
    } else if (obj instanceof Integer) {
        Integer i = (Integer) obj;
        return i.toString();
    }
    return "unknown";
}
```

Why: The pre-Java 21 form repeats type checks and casts, hides `null` behavior, and is harder to extend safely.

## Conventions

| Rule | Rationale |
|---|---|
| Prefer standard Java 21 features such as pattern matching for switch, record patterns, virtual threads, sequenced collections, UTF-8 defaults, `jwebserver`, and the KEM API before preview features | Standard features do not require preview flags and carry production compatibility guarantees |
| Use pattern matching for switch with `case null`, `default`, guarded `when` clauses, and record patterns where they simplify existing `instanceof` chains | Exhaustive switch logic removes casts and documents unmatched cases |
| Use record patterns such as `Point(var x, var y)` and nested patterns such as `ColoredPoint(Point(var x, var y), var color)` only when destructuring clarifies the code | Destructuring should expose data shape without obscuring intent |
| Use `Executors.newVirtualThreadPerTaskExecutor()` and `Thread.ofVirtual()` for high-throughput blocking I/O, not CPU-bound work | Virtual Threads scale blocking operations but do not make CPU work faster |
| Treat `StructuredTaskScope.ShutdownOnFailure`, string templates `STR`, `HTML`, `SQL`, unnamed patterns `_`, and `ScopedValue` as preview features in Java 21 | Preview APIs require `--enable-preview` at compile time, test time, and runtime |
| Use `SequencedCollection`, `SequencedSet`, `SequencedMap`, `getFirst`, `getLast`, `addFirst`, `addLast`, and `reversed` when code needs first/last or reverse-order access | The Java 21 collection interfaces remove collection-specific branching |
| Remove redundant `StandardCharsets.UTF_8` only when UTF-8 was the intended default | Java 18's default charset is UTF-8, but explicit non-UTF-8 behavior must remain explicit |
| Use `jwebserver -p 8080 -d /path/to/files` or `com.sun.net.httpserver` only for testing and development servers | The simple web server is not a production application server |
| Implement `InetAddressResolverProvider` only for custom DNS resolution scenarios such as service discovery or tests | Custom address resolution changes core networking behavior |
| Replace `finalize()` with `Cleaner` or try-with-resources | Finalization is deprecated and unreliable for resource cleanup |
| Use `-XX:+EnableDynamicAgentLoading` only when dynamic instrumentation is required and prefer startup agent loading where possible | Java 21 warns on dynamic agent loading and future releases may restrict it further |
| Configure Maven `maven-compiler-plugin` with `<release>21</release>` and preview `<arg>--enable-preview</arg>` only when preview code exists | Build flags should match source usage and avoid unnecessary preview coupling |
| Configure Gradle `JavaLanguageVersion.of(21)`, `options.compilerArgs.add("--enable-preview")`, and `jvmArgs("--enable-preview")` only when preview code exists | Compile and test tasks must agree on preview mode |
| Use `-Djdk.virtualThreadScheduler.parallelism=N` and `-Djdk.virtualThreadScheduler.maxPoolSize=N` only for debugging or tuned deployments | Scheduler settings can mask or create concurrency bottlenecks |
| Evaluate Generational ZGC with `-XX:+UseZGC -XX:+ZGenerational` through benchmarks and GC monitoring | GC selection depends on allocation patterns and latency goals |
| Keep `USER_ID` and `ScopedValue.where(USER_ID, "user123")` scoped to request context examples rather than global mutable state | Scoped values are meant for bounded context propagation |

## Do / Do Not

| Do | Do not |
|---|---|
| Convert clear `instanceof` chains to pattern matching switch expressions | Rewrite simple conditionals when switch reduces readability |
| Use record patterns for records that are already part of the domain model | Create records solely to force destructuring syntax |
| Use virtual threads for blocking HTTP, database, or file I/O workloads | Expect virtual threads to speed up CPU-intensive loops |
| Enable `--enable-preview` consistently for compile, test, and runtime when preview features are used | Enable preview flags globally when no preview feature is present |
| Use `SequencedCollection` methods for uniform first/last access | Keep hand-written collection-type branches for first or last element access |
| Remove `finalize()` in favor of `Cleaner` or try-with-resources | Add new finalizers or rely on finalization for correctness |
| Load Java agents at startup when possible | Suppress dynamic agent warnings without understanding the tool behavior |
| Benchmark Generational ZGC and virtual-thread changes under representative load | Claim performance wins from syntax-only migrations |
| Validate UTF-8 behavior across platforms after removing explicit charsets | Remove charset arguments where a non-UTF-8 encoding was intentional |

## Checklist Before Opening a PR

- [ ] Build files target JDK 21 with Maven or Gradle toolchains and avoid preview flags unless preview features are present.
- [ ] Pattern matching switch changes handle `null`, defaults, guarded `when` cases, and expected record shapes.
- [ ] Record patterns, unnamed patterns, string templates, structured concurrency, and scoped values are used only with the required preview configuration.
- [ ] Virtual Thread changes target blocking I/O and have concurrency tests or benchmarks.
- [ ] Sequenced collection changes preserve ordering semantics and first/last behavior.
- [ ] Charset changes preserve intended UTF-8 or explicit non-UTF-8 behavior.
- [ ] `finalize()` usages are removed or isolated for follow-up replacement with `Cleaner` or try-with-resources.
- [ ] Dynamic-agent warnings are addressed with startup agents or a justified `-XX:+EnableDynamicAgentLoading` flag.
- [ ] GC changes such as `-XX:+UseZGC -XX:+ZGenerational` have benchmark or monitoring evidence.
- [ ] Tests cover concurrency, pattern matching exhaustiveness, platform charset behavior, and any preview feature used before production deployment.
