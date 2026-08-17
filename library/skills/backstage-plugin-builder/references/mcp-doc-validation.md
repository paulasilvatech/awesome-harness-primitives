# MCP Documentation Validation

Use this gate before recommending Backstage APIs, package versions, plugin patterns, publication steps, or migration paths. Local references are a baseline; current official documentation is the source of truth.

## Preferred Source Order

1. `mcp-ecosystem`, for current ecosystem documentation and package signals when available.
2. GitHub source lookup for `backstage/backstage` and `backstage/community-plugins`.
3. Official Backstage website pages.
4. Local cached references in this skill.

## Required Checks

| Claim type | Required current source |
| --- | --- |
| Frontend plugin API | Backstage frontend-system docs. |
| Backend plugin API | Backstage backend-system docs. |
| Backend module API | Backstage backend-system docs and extension point package docs. |
| Community publication | `backstage/community-plugins` contribution guide. |
| Version-specific claim | Backstage release notes, package metadata, or official docs. |
| Dynamic loading claim | Target runtime documentation, not generic Backstage docs alone. |

## Evidence To Record

Every plan, ADR, architecture, or publication artifact that depends on current Backstage behavior should include a documentation freshness table:

| Claim | Source | Checked at | Notes |
| --- | --- | --- | --- |
| Frontend plugin API | `mcp-ecosystem` or fallback URL | YYYY-MM-DD | `createFrontendPlugin` confirmed or not applicable. |
| Backend plugin API | `mcp-ecosystem` or fallback URL | YYYY-MM-DD | `createBackendPlugin` confirmed or not applicable. |
| Backend module API | `mcp-ecosystem` or fallback URL | YYYY-MM-DD | `createBackendModule` confirmed or not applicable. |
| Community publication | `mcp-ecosystem`, GitHub, or fallback URL | YYYY-MM-DD | Maintainer review required. |

## Failure Handling

- If `mcp-ecosystem` is unavailable or returns an error, state this clearly and continue with GitHub or official web fallback.
- Do not block the user solely because MCP is unavailable.
- Do not rely on legacy Backstage plugin docs for new plugin work unless the task is maintaining an old plugin.
- Do not promise community publication acceptance.

## Fallback Validation Script

Run the fallback URL check when MCP documentation lookup is unavailable:

```bash
python .github/skills/backstage-plugin-builder/scripts/validate_official_docs.py
```

This script confirms official source reachability. It does not replace reading the current docs before making version-specific recommendations.
