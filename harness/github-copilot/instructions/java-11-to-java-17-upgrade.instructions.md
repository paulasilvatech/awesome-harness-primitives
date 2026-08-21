---
applyTo: "**/*.java,**/*.gradle,**/*.gradle.kts,**/pom.xml"
description: "Enforces Java 11 to Java 17 upgrade conventions for language features, API migration, build configuration, removals, JVM tuning, and compatibility testing."
---

# Java 11 to Java 17 Upgrade Conventions — Modernization Without Compatibility Drift

These instructions apply to Java source and Maven or Gradle build files matched by `**/*.java,**/*.gradle,**/*.gradle.kts,**/pom.xml` when moving from JDK 11 to JDK 17. They are authoritative for adopting Java 12 through Java 17 language features, APIs, build flags, deprecation removals, JVM options, and migration testing; framework-specific, security, deployment, or style primitives with stricter project rules win for their own domains.

## Build Baseline and Preview Boundaries

Set the build to Java 17 deliberately before using Java 17 APIs or syntax. Prefer the `release` flag over separate source and target values so the compiler rejects APIs not available in the selected platform.

| Build system | Required convention |
| --- | --- |
| Maven | Set `<maven.compiler.release>17</maven.compiler.release>` and configure `maven-compiler-plugin` with `<release>17</release>`. Keep `<maven.compiler.source>17</maven.compiler.source>` and `<maven.compiler.target>17</maven.compiler.target>` only when the existing build expects them. |
| Gradle Kotlin DSL | Use `java { toolchain { languageVersion = JavaLanguageVersion.of(17) } }` and `tasks.withType<JavaCompile> { options.release.set(17) }`. |
| Tests | Use `maven-surefire-plugin` or `tasks.withType<Test> { useJUnitPlatform() }` to run the existing test framework on JDK 17. |
| Preview features | Add `--enable-preview` to compiler and test runtime only when code intentionally uses preview JEP 406 pattern matching for switch. |

Maven preview configuration must put `--enable-preview` in `<compilerArgs><arg>--enable-preview</arg></compilerArgs>` and test configuration in `<argLine>--enable-preview</argLine>`. Gradle preview configuration must use `options.compilerArgs.addAll(listOf("--enable-preview"))` and `jvmArgs("--enable-preview")`.

Keep Maven/Gradle upgrade notes explicit about compile-time and runtime flags; Java 17 preview code must be type-safe at compile time and runnable with the same preview setting in tests.

## Records and Data Carriers

Use JEP 395 records for immutable data carriers, API data transfer objects, and configuration shapes whose identity is their components. Do not convert classes with mutable state, inheritance requirements, lazy initialization, framework proxy constraints, or non-component identity.

**Good:**

```java
public record Person(String name, int age) {
    public Person {
        if (age < 0) {
            throw new IllegalArgumentException("Age cannot be negative");
        }
    }

    public boolean isAdult() {
        return age >= 18;
    }
}
```

Why: the record replaces boilerplate accessors, `equals`, `hashCode`, and `toString` while preserving validation through a compact constructor.

**Bad:**

```java
public class Person {
    private final String name;
    private final int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String name() { return name; }
    public int age() { return age; }
}
```

Why: this traditional data class is acceptable on Java 11 but keeps boilerplate that Java 17 records remove when the type is only a data carrier.

Records are more memory efficient in common data-carrier use, create less boilerplate, provide automatic equality behavior, and can participate in serialization when the project explicitly supports it.

## Sealed Hierarchies and Pattern Matching

Use JEP 409 sealed classes when the set of subtypes is intentionally closed and the compiler should enforce that boundary. Declare `sealed`, list permitted types with `permits`, and mark each subtype `final`, `sealed`, or `non-sealed`.

```java
public sealed class Shape permits Circle, Rectangle, Triangle {
    public abstract double area();
}

public final class Circle extends Shape {
    private final double radius;
    public double area() { return Math.PI * radius * radius; }
}

public final class Rectangle extends Shape {
    private final double width, height;
    public double area() { return width * height; }
}

public non-sealed class Triangle extends Shape {
    private final double base, height;
    public double area() { return 0.5 * base * height; }
}
```

Use JEP 394 pattern matching for `instanceof` to remove redundant casts and make type-specific branches clear.

```java
public String processObject(Object obj) {
    if (obj instanceof String str) {
        return str.toUpperCase();
    } else if (obj instanceof Integer num) {
        return "Number: " + num;
    } else if (obj instanceof List<?> list) {
        return "List with " + list.size() + " elements";
    }
    return "Unknown type";
}
```

For sealed types, use pattern matching to describe domain state, for example `describeShape(Shape shape)` with `Circle circle`, `Rectangle rect`, and `Triangle triangle`. Pattern matching reduces redundant type checks, removes casting overhead, and gives the JVM clearer optimization opportunities.

## Switch Expressions and Preview Switch Patterns

Use JEP 361 switch expressions for expression-shaped decisions. Prefer arrow labels, group related constants, and use `yield` only when a branch needs multiple statements.

```java
public String getDayType(DayOfWeek day) {
    return switch (day) {
        case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "Workday";
        case SATURDAY, SUNDAY -> "Weekend";
    };
}

public int calculateScore(Grade grade) {
    return switch (grade) {
        case A -> 100;
        case B -> 85;
        case C -> 70;
        case D -> {
            System.out.println("Consider improvement");
            yield 55;
        }
        case F -> {
            System.out.println("Needs retake");
            yield 0;
        }
    };
}
```

Treat JEP 406 pattern matching for switch as preview in Java 17. Code such as `formatValue(Object obj)` with `case String s`, `case Integer i`, `case null`, and `default`, or `categorizeNumber(Object obj)` with guarded cases such as `case Integer i when i < 0`, `case Double d when d.isNaN()`, and `case Number n`, requires `--enable-preview` at compile time and runtime. Do not introduce preview switch patterns unless the project accepts preview-source maintenance cost.

## Text Blocks and Multi-line Content

Use JEP 378 text blocks for SQL, HTML, JSON, and configuration snippets where the multi-line structure matters. Keep indentation intentional and use `.formatted(name, age, city)` when injecting values.

```java
String sql = """
             SELECT p.id, p.name, p.email,
                    a.street, a.city, a.state
             FROM person p
             JOIN address a ON p.address_id = a.id
             WHERE p.active = true
             ORDER BY p.name
             """;

String json = """
              {
                "name": "%s",
                "age": %d,
                "city": "%s"
              }
              """.formatted(name, age, city);
```

Prefer text blocks over concatenated strings for readable multi-line content such as `<html>`, `<body>`, `<h1>Hello World</h1>`, `<p>Welcome to Java 17!</p>`, SQL joins, JSON templates, and configuration files.

## Runtime Diagnostics and Core APIs

Java 17 includes API and runtime improvements that should be used only where they fit the application.

| JEP | API or behavior | Convention |
| --- | --- | --- |
| JEP 358 | Helpful `NullPointerException` messages | Keep null handling explicit, but use the default richer messages to debug expressions such as `person.getName().length()` and `groups.get("admins").get(0).getName().length()`. |
| JEP 371 | Hidden classes | Leave `MethodHandles.Lookup`, `Proxy.newProxyInstance`, `InvocationHandler`, and generated class isolation to frameworks unless writing proxy or bytecode infrastructure. |
| JEP 334 | JVM Constants API | Use `java.lang.constant.*`, `DynamicConstantDesc<String>`, `ConstantDescs.BSM_INVOKE`, `ConstantDescs.CD_String`, and a constant such as `COMPUTED_CONSTANT` only in compiler, tooling, or metaprogramming code. |
| JEP 415 | Context-specific deserialization filters | Configure `ObjectInputFilter`, `ObjectInputFilter.Config.createFilter`, `ObjectInputFilter.Config.setSerialFilter`, and `ois.setObjectInputFilter(contextFilter)` for object deserialization; allow expected packages such as `java.base/*` only when the filter needs them. |
| JEP 356 | Enhanced pseudo-random number generators | Prefer `RandomGenerator` and `RandomGeneratorFactory` for high-quality, splittable, or streamable random values; keep `Random` only when compatibility or determinism requires it. |

For random generation, named generators such as `Xoshiro256PlusPlus` and `L64X128MixRandom` support scenarios like parallel processing, statistical applications, gaming, simulation, `RandomGenerator.SplittableGenerator`, `splits(4)`, `parallel()`, `mapToInt`, `nextInt(1000)`, `forEach(System.out::println)`, and `generator.ints(10, 1, 101)`.

Retain the relevant Java API names when refactoring examples: `PersonProcessor` illustrates Helpful NullPointerExceptions, `DynamicProxyExample` illustrates hidden-class-adjacent proxy generation, `ConstantExample` illustrates constants, and `SecureDeserialization` illustrates `ByteArrayInputStream`, `ObjectInputStream`, `ClassNotFoundException`, and expected-type casting.

## I/O, Networking, and Persistent Memory

Use Java 17 I/O improvements only when the deployment platform supports them.

| Feature | APIs to preserve | Rule |
| --- | --- | --- |
| JEP 380 Unix-domain socket channels | `UnixSocketExample`, `UnixDomainSocketAddress`, `ServerSocketChannel.open(StandardProtocolFamily.UNIX)`, `SocketChannel.open(address)`, `SocketChannel client`, `ByteBuffer.allocate(1024)`, `client.read(buffer)`, `handleClient(client)`, and legacy comparison to `InetSocketAddress` TCP sockets | Use for local IPC when Unix domain sockets are supported. Do not hardcode a transient path such as `/tmp/my-app.socket`; configure an application runtime path instead. |
| JEP 352 Non-Volatile Mapped Byte Buffers | `PersistentMemoryExample`, `MappedByteBuffer`, `FileChannel.open`, `StandardOpenOption.READ`, `StandardOpenOption.WRITE`, `StandardOpenOption.CREATE`, `FileChannel.MapMode.READ_WRITE`, `ExtendedMapMode.READ_WRITE_SYNC`, `buffer.putLong`, `buffer.putInt`, `buffer.force()` | Use only for persistent-memory deployments such as `Path.of("/mnt/pmem/data.bin")`, and keep crash-consistency requirements explicit. |

## Deprecations, Removals, and Security

Remove or replace APIs that are deprecated for removal or gone by Java 17.

| JEP | Change | Migration rule |
| --- | --- | --- |
| JEP 411 | Security Manager deprecated for removal | Remove `SecurityManager sm = System.getSecurityManager()` checks and replace permission assumptions such as `sm.checkPermission(new RuntimePermission("shutdownHooks"))` with application-level security, containers, or process isolation. |
| JEP 398 | Applet API deprecated for removal | Migrate `Applet` code such as `MyApplet extends Applet` to a standalone `JFrame` application like `MyApplication extends JFrame`, or to web technology. Preserve desktop behavior with `setTitle`, `setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)`, `SwingUtilities.invokeLater`, `setVisible(true)`, and `main(String[] args)` when Swing remains appropriate. |
| JEP 372 | Nashorn removed | Replace `new ScriptEngineManager().getEngineByName("nashorn")` with a supported option such as `getEngineByName("graal.js")`, external Node execution through `ProcessBuilder("node", "script.js")`, or a web-based or embedded-browser approach. |

Do not depend on removed Nashorn JavaScript behavior, a `ScriptEngine` from the old engine, Applet lifecycle methods such as `start()`, or broad Security Manager checks during the JDK 17 migration.

## JVM and Performance Options

Prefer correctness and compatibility first; then tune garbage collection or startup behavior with measured evidence.

| Area | Java 17 convention |
| --- | --- |
| JEP 377 ZGC | Use `-XX:+UseZGC` for low-latency applications after measurement. `-XX:+UnlockExperimentalVMOptions` is not needed in Java 17. Monitor with `-XX:+LogVMOutput` and `-XX:LogFile=gc.log` if the project uses those diagnostics. |
| JEP 379 Shenandoah | Use `-XX:+UseShenandoahGC` for consistent latency after measurement. Tune with `-XX:ShenandoahGCHeuristics=adaptive` only with evidence. |
| JEP 341 Default CDS Archives and JEP 350 Dynamic CDS Archives | CDS is enabled by default. Use custom archives only when startup measurements justify `java -XX:DumpLoadedClassList=classes.lst -cp myapp.jar com.example.Main`, `java -Xshare:dump -XX:SharedClassListFile=classes.lst -XX:SharedArchiveFile=myapp.jsa -cp myapp.jar`, and `java -XX:SharedArchiveFile=myapp.jsa -cp myapp.jar com.example.Main`. |

Records, pattern matching, and switch expressions can improve memory use, type checks, bytecode generation, constant folding, branch prediction, and exhaustiveness, but do not rewrite working code solely for theoretical performance.

## Migration Strategy and Testing

Keep migration incremental and test-driven rather than treating Java 17 adoption as a blind syntax conversion.

| Phase | Convention |
| --- | --- |
| Foundation | Update Maven or Gradle, CI/CD pipelines, and dependency compatibility before using Java 17-only features. |
| Removals | Address Nashorn, Applet API, and Security Manager dependencies before feature refactors. |
| Records | Convert stable data classes and test serialization compatibility where serialization matters. |
| Pattern matching | Replace `instanceof` chains where it reduces casting and improves clarity. |
| Switch expressions | Convert switch statements to expressions where the result is a value and branch coverage is clear. |
| Text blocks | Replace concatenated SQL, HTML, JSON, and configuration strings where formatting improves maintainability. |
| Sealed classes | Design sealed hierarchies for domain modeling, state machines, algebraic data types, and API evolution control. |
| Validation | Run comprehensive tests, performance benchmarking, and compatibility verification before claiming the upgrade complete. |

## Good / Bad Examples

The examples below illustrate Java 17 adoption that improves clarity without introducing preview dependencies.

**Good:**

```java
public sealed interface Result permits Success, Failure {}

public record Success(String value) implements Result {}
public record Failure(String message) implements Result {}

public String render(Result result) {
    if (result instanceof Success success) {
        return success.value();
    }
    if (result instanceof Failure failure) {
        return "Error: " + failure.message();
    }
    throw new IllegalStateException("Unknown result");
}
```

Why: the code uses sealed types, records, and `instanceof` pattern variables that are stable in Java 17 without requiring preview switch patterns.

**Bad:**

```java
public String render(Object result) {
    return switch (result) {
        case Success s -> s.value();
        case Failure f -> "Error: " + f.message();
        case default -> "Unknown";
    };
}
```

Why: pattern matching for switch is preview in Java 17 and requires `--enable-preview`; using it without an explicit preview policy creates build and runtime drift.

## Conventions

| Rule | Rationale |
| --- | --- |
| Configure Java 17 with toolchains and `release` before changing source | The compiler and CI must enforce the target platform before new APIs appear. |
| Use records only for immutable data carriers | Records remove boilerplate but are wrong for mutable, proxied, or identity-rich objects. |
| Use sealed classes for intentionally closed hierarchies | The compiler can enforce permitted subtypes and support exhaustive reasoning. |
| Replace verbose `instanceof` plus casts with pattern matching | Type-specific logic becomes shorter and less error-prone. |
| Use switch expressions for value-returning decisions | Arrow labels and exhaustiveness reduce fall-through and assignment bugs. |
| Treat switch pattern matching as preview in Java 17 | Preview features require explicit compile and runtime flags and future maintenance. |
| Use text blocks for structured multi-line strings | SQL, HTML, JSON, and configuration become readable without concatenation noise. |
| Replace removed or deprecated APIs before feature refactors | Nashorn, Applets, and Security Manager dependencies can block the runtime upgrade. |
| Use new JVM, random, I/O, constants, and deserialization APIs only for matching needs | Specialty APIs add value only when their operational assumptions hold. |
| Validate with tests, benchmarks, and compatibility checks | A JDK upgrade is complete only when behavior and performance remain acceptable. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Set Maven `<release>17</release>` or Gradle `options.release.set(17)` | Rely only on a local IDE JDK selection. |
| Add `--enable-preview` only for deliberate JEP 406 usage | Accidentally introduce preview syntax into normal Java 17 code. |
| Convert simple immutable data classes to records | Convert framework entities or mutable domain objects just because records exist. |
| Model closed domain alternatives with `sealed`, `permits`, `final`, and `non-sealed` | Leave unrestricted inheritance when the subtype set is a compatibility contract. |
| Use `obj instanceof String str` style pattern variables | Cast manually after every `instanceof` check. |
| Use text blocks with `.formatted(...)` for structured literals | Keep long SQL, HTML, or JSON strings as fragile concatenations. |
| Configure `ObjectInputFilter` for object deserialization | Deserialize untrusted object streams without context-specific filters. |
| Replace Nashorn, Applet, and Security Manager usage | Assume Java 11-era deprecated APIs keep working unchanged. |
| Tune ZGC, Shenandoah, or CDS with measurements | Change garbage collectors or archive settings without performance evidence. |

## Checklist Before Opening a PR

- [ ] Maven or Gradle compiles with Java 17 toolchains and release settings.
- [ ] Preview features are absent, or `--enable-preview` is configured for compile and test runtime with an explicit justification.
- [ ] Records replace only suitable immutable data carriers and preserve validation, serialization, and framework compatibility requirements.
- [ ] Sealed hierarchies declare all permitted subtypes and each subtype is `final`, `sealed`, or `non-sealed`.
- [ ] Pattern matching for `instanceof`, switch expressions, and text blocks are used only where they improve clarity.
- [ ] Nashorn, Applet API, and Security Manager dependencies are removed or replaced.
- [ ] Deserialization code uses `ObjectInputFilter` when object streams remain necessary.
- [ ] Random, Unix-domain socket, persistent-memory, constants, hidden-class, GC, and CDS APIs are used only with matching runtime requirements.
- [ ] Existing tests, compatibility checks, and any relevant benchmarks pass on JDK 17.
- [ ] The PR avoids unrelated syntax churn outside the Java 11 to Java 17 migration scope.
