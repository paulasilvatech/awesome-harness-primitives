---
description: "Use when creating or reviewing automated tests, test strategy, specs, coverage gaps, regression tests, and quality gates."
applyTo: "**/*.test.*,**/*.spec.*,**/tests/**"
---

# Testing Conventions — JUnit, Vitest, and Traceability

This file activates on any test file (`*.test.*`, `*.spec.*`, or anything under a `tests/` path), backend and frontend alike. It teaches test structure, naming, the backend (JUnit 5 + Testcontainers) and frontend (Vitest + Testing Library) tooling, REQ-ID traceability, and coverage targets. Tests are written **during** implementation, never bolted on afterward.

## Test Pyramid

| Layer | Tooling | Share |
|---|---|---|
| Unit (services, pure logic) | JUnit 5 / Vitest, no I/O | Most tests |
| Integration (repositories, components) | Testcontainers / Testing Library | Fewer |
| End-to-end | Only the critical flow | Fewest |

The [`test-strategy`](../skills/test-strategy/SKILL.md) skill owns pyramid shape and coverage-target decisions.

## Structure: Arrange-Act-Assert

Each test has three visible phases and asserts one behavior. Mock only external boundaries — never the database and never the class under test.

```java
@Test
void should_reject_duplicate_label() { // REQ-021
    resourceRepository.save(Resource.of("alpha", new BigDecimal("10.00"))); // Arrange
    var request = new CreateResourceRequest("alpha", new BigDecimal("5.00"));
    assertThatThrownBy(() -> resourceService.create(request))            // Act
        .isInstanceOf(ResourceConflictException.class);                  // Assert
}
```

## Naming

Name tests `should_<expected behavior>_when_<condition>` (backend) or the same intent in a Testing Library `it(...)` (frontend).

```text
should_return_409_when_identifier_already_exists
should_render_empty_state_when_no_resources
```

## Backend: JUnit 5 + Testcontainers

Repository and integration tests run against a real PostgreSQL 16 in a container — never H2 — so behavior matches production. Bind the container with `@ServiceConnection`.

```java
@Testcontainers
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class ResourceRepositoryTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @Autowired
    ResourceRepository resourceRepository;

    @Test
    void should_find_resource_by_label_when_it_exists() { // REQ-021
        resourceRepository.save(Resource.of("alpha", new BigDecimal("10.00")));
        assertThat(resourceRepository.findByLabel("alpha")).isPresent();
    }
}
```

Backend business logic must include a happy path, a validation failure, and an auth failure.

## Frontend: Vitest + Testing Library

Query by accessible role or label — never by test-id when a role exists — and drive interaction with `user-event`. Avoid snapshot-only tests.

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { ArchiveButton } from './ArchiveButton';

describe('ArchiveButton', () => {
  it('should call onArchive when clicked', async () => { // REQ-032
    const onArchive = vi.fn().mockResolvedValue(undefined);
    render(<ArchiveButton id="1" onArchive={onArchive} />);
    await userEvent.click(screen.getByRole('button', { name: /archive/i }));
    expect(onArchive).toHaveBeenCalledWith('1');
  });
});
```

## REQ-ID Traceability

Every test that verifies a requirement names its REQ-ID in an inline comment. This feeds the non-blocking `spec-traceability` report (see [`requirements.instructions.md`](requirements.instructions.md)), which lists REQ-IDs that no test references yet.

## Coverage Targets

The repo floor is **≥ 80% line** and **≥ 70% branch**; service and business-logic classes should aim higher (~85% line). CI runs Jacoco (backend) and Vitest `--coverage` (frontend) and reports the numbers; configure the thresholds in `pom.xml` and the Vitest config so `verify`/`test` fail below the floor.

> [!NOTE]
> Coverage is a floor, not a goal. A branch with no assertion is untested even when the line is "covered" — assert the behavior, not just the call.

## Conventions

| Rule | Rationale |
|---|---|
| Arrange-Act-Assert, one behavior per test | Readable, isolate the failure |
| Mock external boundaries only | Real DB via Testcontainers catches real bugs |
| `should_<behavior>_when_<condition>` naming | Intent is obvious from the report |
| Inline `// REQ-NNN` on requirement tests | Keeps spec ↔ test traceability alive |
| Written during implementation | No untested code merges |

## Do / Do Not

| Do | Do not |
|---|---|
| Use Testcontainers PostgreSQL 16 | Substitute H2 for integration tests |
| Query by role/label | Query by `data-testid` when a role exists |
| Assert behavior and edge branches | Rely on snapshot-only or line-only coverage |
| Write the test with the code | Add tests after the feature is "done" |

## Checklist Before Opening a PR

- [ ] New behavior has unit tests; persistence has a Testcontainers integration test
- [ ] Tests follow Arrange-Act-Assert and the `should_..._when_...` naming
- [ ] Requirement-driven tests carry an inline `// REQ-NNN` comment
- [ ] Business logic covers happy path, validation failure, and auth failure
- [ ] Coverage meets the ≥ 80% line / ≥ 70% branch floor
- [ ] No external boundary is left unmocked and no real dependency is mocked away
