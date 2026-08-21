# Backstage Documentation Validation

Use this gate before recommending Backstage APIs, package versions, plugin patterns, publication steps, or migration paths. Local references are a baseline; current official documentation is the source of truth.

## Preferred Source Order

1. Exact source files from `backstage/backstage` or `backstage/community-plugins` at a named commit or release.
2. Official Backstage website pages.
3. Local cached references in this skill, only when they match the target version.

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
| Frontend plugin API | first-party URL or exact source commit | YYYY-MM-DD | `createFrontendPlugin` confirmed or legacy mode stated. |
| Backend plugin API | first-party URL or exact source commit | YYYY-MM-DD | `createBackendPlugin` confirmed or not applicable. |
| Backend module API | first-party URL or exact source commit | YYYY-MM-DD | `createBackendModule` confirmed or not applicable. |
| Community publication | first-party contribution guide | YYYY-MM-DD | Maintainer review required. |

## Failure Handling

- If network lookup is unavailable, use an existing verified checkout or the local cached reference and state the exact source and date.
- Do not invent a current-version claim when first-party evidence is unavailable.
- Do not rely on legacy Backstage plugin docs for new plugin work unless the task is maintaining an old plugin.
- Do not promise community publication acceptance.

## Fallback Validation Script

Run the URL reachability check before relying on the listed web sources:

```bash
cd <installed-backstage-plugin-builder-skill-directory>
python3 scripts/validate_official_docs.py
```

This script confirms official source reachability. It does not replace reading the current docs before making version-specific recommendations.
