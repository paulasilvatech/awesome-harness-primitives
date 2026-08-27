---
name: javax-to-jakarta-migration
description: >-
  Migrate Java applications from `javax.*` APIs to `jakarta.*` APIs for Tomcat 11, Jakarta EE 10+,
  and framework upgrades. Use this skill when `javax` imports are detected, dependencies need
  Jakarta coordinates, `web.xml` namespaces must change, or compile errors follow a Jakarta
  migration.
argument-hint: File, package, or module to migrate
---

<!-- Generated from harness/github-copilot/plugins/java-kotlin-development/skills/javax-to-jakarta-migration/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# javax to jakarta migration

Convert application-owned Java EE imports, dependency coordinates, and deployment descriptors from `javax.*` to `jakarta.*` and raw `jakarta.` references while preserving JDK-owned `javax` packages that must not move.

## When to invoke

- "Migrate this module from javax to jakarta."
- "Upgrade this app for Tomcat 11 or Jakarta EE 10."
- "Find remaining `javax.*` imports."
- "Fix compile errors after Jakarta migration."
- "Update `web.xml` to the Jakarta namespace."

## Inputs

Use `$ARGUMENTS` as the file, package, module, or repository scope to migrate. If `$ARGUMENTS` is empty, scan the current workspace and report the discovered scope before changing files.

## Procedure

1. Scan Java source, descriptors, and build files for `javax.*` usage in the requested scope.
2. Classify each package as migratable Jakarta API or JDK-owned `javax` API that must remain unchanged.
3. Update dependency coordinates before or alongside source imports so compilation resolves the new packages.
4. Update deployment descriptors such as `web.xml` when present.
5. Replace source imports and fully qualified references in `.java` files.
6. Verify with the existing build and test commands, then search for remaining `javax.*` imports excluding JDK packages.

## Package migration map

| Old package | New package |
| --- | --- |
| `javax.servlet.*` | `jakarta.servlet.*` |
| `javax.persistence.*` | `jakarta.persistence.*` |
| `javax.validation.*` | `jakarta.validation.*` |
| `javax.annotation.*` | `jakarta.annotation.*` |
| `javax.inject.*` | `jakarta.inject.*` |
| `javax.enterprise.*` | `jakarta.enterprise.*` |
| `javax.faces.*` | `jakarta.faces.*` |
| `javax.ws.rs.*` | `jakarta.ws.rs.*` |
| `javax.el.*` | `jakarta.el.*` |
| `javax.json.*` | `jakarta.json.*` |
| `javax.mail.*` | `jakarta.mail.*` |
| `javax.websocket.*` | `jakarta.websocket.*` |

## Packages that stay in javax

Do not migrate JDK-owned packages:

| Keep package | Reason |
| --- | --- |
| `javax.sql.*` | JDBC/JDK API. |
| `javax.naming.*` | JNDI/JDK API. |
| `javax.crypto.*` | JDK cryptography API. |
| `javax.net.*` | JDK networking API. |
| `javax.security.auth.*` | JDK security API. |
| `javax.swing.*` | JDK desktop UI API. |
| `javax.xml.parsers.*` | JDK XML parser API. |

## Build and descriptor changes

| File | Old | New |
| --- | --- | --- |
| `pom.xml` | `javax.servlet:javax.servlet-api` | `jakarta.servlet:jakarta.servlet-api:6.0.0` |
| `pom.xml` | `javax.persistence:javax.persistence-api` | `jakarta.persistence:jakarta.persistence-api:3.1.0` |
| `pom.xml` | `javax.validation:validation-api` | `jakarta.validation:jakarta.validation-api:3.0.2` |
| `pom.xml` | `javax.annotation:javax.annotation-api` | `jakarta.annotation:jakarta.annotation-api:2.1.1` |
| `web.xml` | `http://xmlns.jcp.org/xml/ns/javaee` with `version="4.0"` on the `web-app` descriptor | `https://jakarta.ee/xml/ns/jakartaee` with `version="6.0"` on the `web-app` descriptor |

For Gradle builds, apply equivalent Jakarta coordinates in the dependency block rather than editing Maven-only syntax.

## Verification commands

| Build system | Compile | Test | Residual scan |
| --- | --- | --- | --- |
| Maven | `mvn clean compile` | `mvn test` | search for `javax.` and exclude keep-list packages. |
| Gradle wrapper | `./gradlew build` | `./gradlew test` | search for `javax.` and exclude keep-list packages. |
| Gradle command | `gradlew build` | `gradlew test` | use when the wrapper command is not available on the platform. |

## Gotchas

- **Do not migrate all `javax` text blindly**: `javax.sql`, `javax.naming`, `javax.crypto`, `javax.net`, `javax.security.auth`, `javax.swing`, and `javax.xml.parsers` remain valid.
- **Do not update imports without dependencies**: source edits fail until Jakarta artifacts are present.
- **Do not leave descriptors behind**: `web.xml` can still point to the Java EE namespace after Java compiles.

## Output template

```markdown
## javax to jakarta migration summary

**Status:** complete | needs changes | blocked
**Scope:** <file, package, module, or repository>

| File | Change | Details |
| --- | --- | --- |
| `<path>` | import | `javax.servlet.*` -> `jakarta.servlet.*` |
| `<path>` | dependency | `<old coordinate>` -> `<new coordinate>` |
| `<path>` | descriptor | `<old namespace>` -> `<new namespace>` |

### Manual steps
- <remaining dependency, server, or framework action>

### Validation
- `<compile command>`: pass | fail | not run
- `<test command>`: pass | fail | not run
- Remaining `javax.*`: <none or justified keep-list entries>
```

## Quality gate

- [ ] `$ARGUMENTS` scope was honored or an empty scope triggered a repository scan.
- [ ] Every migrated package appears in the migration map and no keep-list package was changed.
- [ ] Maven or Gradle dependencies match the Jakarta APIs used by source code.
- [ ] `web.xml` uses `https://jakarta.ee/xml/ns/jakartaee` and `version="6.0"` when present and required.
- [ ] `mvn clean compile`, `./gradlew build`, or the repository's equivalent compile command was run or explicitly blocked.
- [ ] Remaining `javax.*` matches only the keep list or is reported as work remaining.

## References

- [Legacy Java EE web.xml namespace](http://xmlns.jcp.org/xml/ns/javaee)
- [Jakarta EE XML namespace](https://jakarta.ee/xml/ns/jakartaee)
