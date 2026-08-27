---
name: openapi-to-application-code
description: >-
  Generate complete production-ready application code from an OpenAPI specification, including
  project structure, models, controllers, services, repositories, validation, error handling,
  tests, documentation, and environment files. Use this skill when the user asks to generate an
  application from an OpenAPI spec, scaffold an API server from OpenAPI, or turn an OpenAPI URL,
  file, or pasted spec into runnable code.
---

<!-- Generated from harness/github-copilot/skills/openapi-to-application-code/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# OpenAPI to application code

Turn an OpenAPI specification into a runnable application that follows the active framework's conventions, preserves the contract in routes and schemas, and includes tests, documentation, configuration, and clear follow-up questions for ambiguous parts.

## When to invoke

- "Generate an application from this OpenAPI spec."
- "Scaffold a server from this openapi.json file."
- "Turn https://api.example.com/openapi.json into runnable code."
- "Create controllers and DTOs from this OpenAPI definition."
- "Build a production-ready API app from this spec."

## Inputs

Accept one OpenAPI source and enough project details to generate idiomatic code.

| Input | Acceptable forms | Required handling |
| --- | --- | --- |
| OpenAPI specification | URL such as `https://api.example.com/openapi.json`, local file path, or pasted YAML/JSON content. | Validate syntax, version, paths, operations, schemas, responses, and security schemes. |
| Project name and description | User-supplied or inferred from `info.title` and `info.description`. | Normalize package, module, and README naming. |
| Target framework and version | User-supplied or inferred from repository conventions. | Follow existing structure rather than imposing a new stack. |
| Package or namespace conventions | Existing repo naming, group ID, module path, or package scope. | Keep generated code consistent. |
| Authentication method | Security schemes in OpenAPI or user clarification. | Implement JWT, OAuth2, API key, basic auth, or a documented stub when details are incomplete. |

## Procedure

1. Analyze the OpenAPI specification.
2. Design application architecture from the active framework's conventions.
3. Generate application code.
4. Add supporting files, tests, examples, and documentation.
5. Run the smallest available build or test command that validates generated code.
6. Report assumptions, unanswered questions, and exact next steps.

## Specification analysis

| Analyze | Extract or flag |
| --- | --- |
| Completeness | OpenAPI version, `info`, `servers`, `paths`, `components.schemas`, `operationId`, tags, examples. |
| Endpoints | HTTP methods, route parameters, query parameters, headers, request bodies, responses, and status codes. |
| Security | Authentication requirements, authorization scopes, per-operation security overrides. |
| Models | Request/response schemas, enums, required fields, nullable fields, formats, relationships, constraints. |
| Ambiguities | Missing examples, unclear auth, schema cycles, unsupported formats, missing error responses, undefined pagination/filtering/sorting. |

## Generated application architecture

| Layer | Generate |
| --- | --- |
| Build/package | Framework-specific files such as `pom.xml`, `build.gradle`, `package.json`, `pyproject.toml`, or equivalent. |
| Controllers/handlers | Route mappings grouped by resource, tag, or domain; validation of path/query/body inputs. |
| Services | Business logic seams with generated stubs where the specification lacks implementation detail. |
| Models/DTOs | Types from OpenAPI schemas, including enums, validation annotations, and serialization names. |
| Repositories/data access | Add only when persistence is requested or clearly implied; otherwise use in-memory/mock seams. |
| Config/startup | Application initialization, environment variables, auth middleware, logging, and error handling. |
| Tests | Unit tests for services and controllers; integration or example requests when useful. |
| Documentation | README setup, run instructions, generated API documentation files, and example requests. |

## Output structure

```text
project-name/
├── README.md
├── [build-config]
├── src/
│   ├── main/
│   │   ├── [language]/
│   │   │   ├── controllers/
│   │   │   ├── services/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   └── config/
│   │   └── resources/
│   └── test/
│       ├── [language]/
│       │   ├── controllers/
│       │   └── services/
│       └── resources/
├── .gitignore
├── .env.example
└── docker-compose.yml
```

`docker-compose.yml` is optional and should be generated only when database, queue, or containerized local dependencies are requested or implied.

## Questions to ask only if needed

- Should the application include database/ORM setup, or just in-memory/mock data?
- Do you want Docker configuration for containerization?
- Should authentication be JWT, OAuth2, API keys, or basic auth?
- Do you need integration tests or just unit tests?
- Any specific database technology preferences?
- Should the API include pagination, filtering, and sorting examples?

## Gotchas

- **Do not invent business logic**: generate service seams and TODOs when the OpenAPI contract defines shape but not behavior.
- **Security schemes are part of the contract**: do not drop auth because examples are missing.
- **Framework conventions win**: when generating inside an existing repo, follow its structure and test runner.
- **Validation must mirror schemas**: required, nullable, enum, format, min/max, and pattern constraints need code-level validation where the framework supports it.

Preserve OpenAPI vocabulary when reporting architecture: Package/namespace choices affect generated imports; build/package files are framework-specific; controller/handler, models/DTOs, repository/data access, authentication/authorization, and example requests/integration tests are separate deliverables.

## Output template

```markdown
## OpenAPI application generation result

**Status:** generated | planned | blocked
**Spec source:** `<URL, path, or pasted content>`
**Framework:** `<framework/version>`

| Artifact | Path | Source from OpenAPI |
| --- | --- | --- |
| Models | `<path>` | `<schemas>` |
| Controllers | `<path>` | `<paths/operations>` |
| Services | `<path>` | `<business seams>` |
| Tests | `<path>` | `<operations covered>` |
| Docs/config | `<path>` | `<README/env/examples>` |

**Assumptions and questions**
- <assumption or question>

**Validation**
- `<build/test command>`: <pass | fail | not run>
```

## Quality gate

- [ ] The OpenAPI source was validated and all endpoints, HTTP methods, request/response schemas, and security schemes were inventoried.
- [ ] Ambiguities and incomplete definitions were flagged before code relied on assumptions.
- [ ] Generated structure follows the target framework and existing repository conventions.
- [ ] Models/DTOs, controllers/handlers, services, repositories when applicable, config, errors, validation, logging, tests, docs, `.gitignore`, and `.env.example` were considered.
- [ ] Authentication and authorization from the OpenAPI spec were implemented or explicitly stubbed with a blocker.
- [ ] The generated code was built or tested with the smallest available command, or the missing dependency/blocker is stated.

## References

- [Example OpenAPI URL](https://api.example.com/openapi.json)
