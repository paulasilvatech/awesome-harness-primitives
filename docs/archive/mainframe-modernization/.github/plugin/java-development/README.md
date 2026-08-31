# java-development

Spring Boot scaffolding, Javadoc, JUnit 5, and Spring Boot best-practice skills.

## What this plugin bundles

Java 21 + Spring Boot 3.3 is the kit's backend stack.

| Component | Type | Location |
|-----------|------|----------|
| `create-spring-boot-java-project` | Skill | [`.github/skills/create-spring-boot-java-project/`](../../skills/create-spring-boot-java-project/) |
| `java-docs` | Skill | [`.github/skills/java-docs/`](../../skills/java-docs/) |
| `java-junit` | Skill | [`.github/skills/java-junit/`](../../skills/java-junit/) |
| `java-springboot` | Skill | [`.github/skills/java-springboot/`](../../skills/java-springboot/) |

All four upstream references resolve, so nothing was dropped.

## How it is enabled

Content under `.github/skills/` is discovered natively by Copilot in this
repository, so these skills work here without any plugin install. The plugin
layer packages them as a named bundle in the local `datacorp-mm-team-kit`
marketplace ([`marketplace.json`](../marketplace.json)) and is declared in
[`.github/copilot/settings.json`](../../copilot/settings.json). See the
[plugins index](../README.md) for the mechanism and its limitations.
