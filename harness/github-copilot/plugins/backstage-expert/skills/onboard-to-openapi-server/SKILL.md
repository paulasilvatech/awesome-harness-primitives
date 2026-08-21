---
name: onboard-to-openapi-server
description: "Migrate a Backstage backend plugin from a hand-written Express router to the repository's typed OpenAPI server tooling while preserving routes, auth, permissions, errors, tests, and optional client generation. Use when onboarding createOpenApiRouter or modernizing a router with OpenAPI."
license: Apache-2.0
metadata:
  source-repository: "https://github.com/backstage/backstage"
  source-commit: "eeac444a9aba7c107525d2a726851e907418c181"
---

# Onboard a Backstage plugin to the OpenAPI server

Reverse-engineer the current router once, make the OpenAPI specification authoritative, and
preserve runtime behavior through generated server types and focused tests.

## When to invoke

- "Convert this Backstage Express router to createOpenApiRouter."
- "Generate an OpenAPI server stub for this backend plugin."
- "Add a typed client for this Backstage API."
- "Migrate router tests to the OpenAPI wrapper."

## Procedure

1. Confirm Backstage core or compatible fork mode, target plugin, green baseline, and exact source
   commit.
2. Read [the pinned upstream procedure](references/upstream/SKILL.md).
3. Keep typed client generation, test-wrapper migration, and changesets opt-in unless already
   required by the task.
4. Inventory every mounted route, parameter, body, response, error, auth check, permission check,
   and nested router.
5. Review the inventory before writing the specification.
6. Author `openapi.yaml` as the new source of truth and validate it with repository tooling.
7. Generate the server stub and switch to `createOpenApiRouter` without dropping auth,
   permissions, middleware, or error behavior.
8. Add or migrate tests for success, validation, auth, permission, and error responses.
9. Run targeted tests and exact root `yarn tsc` for Backstage core.
10. Add optional client, test-wrapper, and changeset work only when in scope.

## Output template

```markdown
## OpenAPI onboarding result

**Plugin:** <path>
**Optional work:** <client, test wrapper, changeset>

| Route | Spec operation | Auth and permission | Test | Status |
| --- | --- | --- | --- | --- |
```

## Quality gate

- [ ] A green baseline exists before migration.
- [ ] Every route and nested router is inventoried.
- [ ] OpenAPI covers parameters, bodies, responses, and errors.
- [ ] Auth, permissions, middleware, and runtime behavior are preserved.
- [ ] Generated artifacts and optional work match the approved scope.
- [ ] Targeted tests and exact root `yarn tsc` pass.
