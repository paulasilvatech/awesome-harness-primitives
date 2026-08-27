---
paths:
  - "**/*.java"
  - "**/*.gradle"
  - "**/*.gradle.kts"
  - "**/pom.xml"
---

<!-- Generated from harness/github-copilot/instructions/java-21-to-java-25-upgrade.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces conventions for adopting Java 25 from Java 21 across language features, JDK APIs, build flags, deprecations, GC behavior, and validation.

# Java 21 to Java 25 Upgrade Conventions — Feature Adoption and Compatibility

These instructions apply to Java source, Maven builds, and Gradle builds being upgraded from JDK 21 toward JDK 25. They are authoritative for Java 22 through Java 25 feature adoption, preview-feature boundaries, JDK API migrations, JVM flag changes, package compatibility review, and build/test validation in matched files; project-specific architecture, security, deployment, and release policies win when they impose stricter constraints.

## Language Feature Adoption

Adopt Java 25 features only when the project build, runtime, and tests can all support the same feature level.

| Area | Convention |
| --- | --- |
| Primitive patterns | Use primitive type patterns in `instanceof` and `switch` only where they simplify existing branching; enable preview features with `--enable-preview` when the selected JDK still marks the feature as preview. |
| Guard patterns | Prefer guarded `case int i when i >= 100` branches for range logic instead of repeated calls such as `x.getYearlyFlights()`. |
| Markdown documentation comments | Convert HTML-heavy JavaDoc to `///` Markdown documentation comments when documentation is being touched; keep `@param` and `@return` tags accurate. |
| Derived record creation | Use derived record creation only in code that explicitly opts into preview features; otherwise keep explicit record copy methods such as `withAge`. |
| Stream gatherers | Use `Stream.gather()` and `java.util.stream.Gatherers` for custom intermediate stream operations such as `Gatherers.windowSliding(3)` or `Gatherers.fold(...)` when they are clearer than manual state. |

Primitive pattern examples preserve existing semantics:

```java
switch (x.getStatus()) {
    case 0 -> "okay";
    case 1 -> "warning";
    case 2 -> "error";
    case int i -> "unknown status: " + i;
}
```

```java
switch (x.getYearlyFlights()) {
    case 0 -> ...;
    case int i when i >= 100 -> issueGoldCard();
    case int i -> ...;
}
```

## JDK API Migration

Prefer standard JDK APIs over legacy or third-party APIs when Java 25 provides the required capability.

| Legacy or specialized API | Java 25 convention | Rationale |
| --- | --- | --- |
| `org.objectweb.asm`, `ClassReader`, `ClassWriter` | Use the standard Class-File API in `java.lang.classfile`, including `ClassFile.of().parse(classBytes)`, `ClassModel`, `ClassFile.of().transform(...)`, and `ClassTransform.transformingMethods(methodTransform)`. | Reduces dependency on bytecode libraries when the JDK provides a supported API. |
| `sun.misc.Unsafe`, `Unsafe.getUnsafe()`, `unsafe.getInt(object, offset)` | Use `VarHandle`, `MethodHandles.lookup().findVarHandle(...)`, or the Foreign Function & Memory API with `MemorySegment` and `ValueLayout.JAVA_INT`. | Deprecated memory-access methods carry future-removal risk. |
| JNI without explicit access | Add `--enable-native-access` for applications that still require JNI and document the modules involved, including `requires jdk.unsupported` only for remaining unsupported use. | JDK 24 introduces JNI usage warnings and tighter native-access expectations. |
| Scalar numeric loops in hot paths | Consider Vector API types from `jdk.incubator.vector`, such as `IntVector.SPECIES_PREFERRED`, `IntVector.fromArray(...)`, `va.add(vb)`, and `vc.intoArray(...)`, with `--add-modules jdk.incubator.vector`. | SIMD can improve numerical workloads, but the Vector API remains incubating. |

## Build and Preview Configuration

Keep compile-time, test-time, and runtime flags aligned.

| Build system | Convention |
| --- | --- |
| Maven | Set `<release>25</release>` in `maven-compiler-plugin`; add `<arg>--enable-preview</arg>` under `<compilerArgs>` only when preview features are used; set `maven-surefire-plugin` `<argLine>--enable-preview</argLine>` for preview tests. |
| Gradle Kotlin DSL | Configure `java.toolchain.languageVersion = JavaLanguageVersion.of(25)`, add `options.compilerArgs.add("--enable-preview")` to `tasks.withType<JavaCompile>`, and add `jvmArgs("--enable-preview")` to `tasks.withType<Test>` when needed. |
| Modules | Add `--add-modules jdk.incubator.vector` only for code that imports `jdk.incubator.vector.*`. |
| Libraries | Do not expose preview-feature APIs from library public contracts unless the project explicitly documents the preview dependency. |

## Runtime, GC, and Performance

Treat JVM behavior changes as compatibility inputs, not automatic rewrites.

- Use `-XX:+UseZGC` for default generational ZGC; remove explicit `-XX:-ZGenerational` unless a measured rollback requires it.
- Expect G1GC and C2 compiler improvements to require no source changes; validate performance rather than rewriting code preemptively.
- Performance-test applications that use JNI, `sun.misc.Unsafe`, Vector API, or changed GC flags before production rollout.
- Validate JavaDoc generation after adopting Markdown comments.

## Migration Discipline and Validation

Express upgrade work as incremental conventions even though the actual execution may occur project by project.

| Concern | Convention |
| --- | --- |
| Build tools | Ensure Maven or Gradle versions support JDK 25 before changing source or target levels. |
| Dependencies | Check package compatibility and update dependencies that do not support JDK 25. |
| Warnings | Address JEP 471 `sun.misc.Unsafe` deprecations and JEP 472 JNI warnings instead of suppressing them without a plan. |
| Testing | Run tests with the same `--enable-preview` and module flags used by the application. |
| Staging | Verify JNI, Unsafe replacements, GC behavior, Stream gatherers, Class-File API code, and Markdown JavaDoc in staging before production. |

## Good / Bad Examples

The examples below illustrate replacing a raw `Unsafe` memory access with a standard handle.

**Good:**

```java
VarHandle vh = MethodHandles.lookup()
    .findVarHandle(MyClass.class, "fieldName", int.class);
int value = (int) vh.get(object);
```

Why: `VarHandle` is a supported API for typed field access and avoids deprecated `sun.misc.Unsafe` memory-access methods.

**Bad:**

```java
Unsafe unsafe = Unsafe.getUnsafe();
int value = unsafe.getInt(object, offset);
```

Why: `sun.misc.Unsafe` memory access is deprecated and increases future-removal and compatibility risk.

## JEP and Compatibility Vocabulary

Retain JEP references `455/488`, `466/484`, `471/472`, and `473/485` when discussing feature provenance. Treat `Maven/Gradle`, `module-info.java`, `off-heap`, `built-in`, and `with` expressions as compatibility terms that reviewers may search for.

## Conventions

| Rule | Rationale |
|---|---|
| Align `--enable-preview` across compilation, tests, and runtime whenever preview features are used | Mixed feature flags produce code that compiles but fails at test or runtime |
| Prefer `java.lang.classfile` over `org.objectweb.asm` for supported bytecode work | Standard APIs reduce dependency and upgrade risk |
| Replace `sun.misc.Unsafe` memory access with `VarHandle` or Foreign Function & Memory API | Deprecated unsafe access is a future compatibility hazard |
| Configure native access explicitly with `--enable-native-access` when JNI remains | JDK 24 warnings become actionable migration signals |
| Use `Stream.gather()` and `Gatherers` for clear stateful stream operations | Custom stream logic stays declarative and testable |
| Remove `-XX:-ZGenerational` unless a measured ZGC regression requires it | Java 25-era ZGC defaults are generational and explicit non-generational mode warns |
| Use the Vector API only with `--add-modules jdk.incubator.vector` and performance evidence | Incubator APIs should not become accidental dependencies |

## Do / Do Not

| Do | Do not |
|---|---|
| Upgrade build tools and dependencies before relying on JDK 25 features | Change source code first and discover unsupported tooling late |
| Use primitive patterns and guards where they simplify `switch` logic | Add preview syntax to ordinary branches without readability gain |
| Convert touched HTML JavaDoc to Markdown `///` comments | Mix stale HTML docs with changed public APIs |
| Keep preview-derived record creation out of stable public library contracts | Require downstream consumers to enable preview unintentionally |
| Validate GC and JNI behavior under production-like flags | Assume JVM warning-free startup without running the application |

## Checklist Before Opening a PR

- [ ] Maven or Gradle supports JDK 25 and uses the intended toolchain or release setting.
- [ ] Preview features have `--enable-preview` in compile, test, and runtime configuration, or no preview features remain.
- [ ] `org.objectweb.asm` usages were evaluated against the Class-File API.
- [ ] `sun.misc.Unsafe` memory access was replaced or documented with a migration plan.
- [ ] JNI usage has explicit `--enable-native-access` configuration where it remains.
- [ ] ZGC flags, G1 behavior, Vector API modules, and performance-sensitive stream changes were tested.
- [ ] JavaDoc generation succeeds after Markdown documentation comment changes.
- [ ] Automated tests pass on the upgraded JDK.
