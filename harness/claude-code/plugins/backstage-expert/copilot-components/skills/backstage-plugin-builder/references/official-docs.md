# Official Backstage Documentation

Use these official sources as the documentation baseline for this skill. For current frontend and backend system docs, the Backstage repository source files are the most stable machine-checkable URLs.

| Topic | Official source |
| --- | --- |
| Standalone Backstage app | <https://backstage.io/docs/getting-started/> |
| New frontend plugins | <https://github.com/backstage/backstage/blob/master/docs/frontend-system/building-plugins/01-index.md> |
| New backend plugins and modules | <https://github.com/backstage/backstage/blob/master/docs/backend-system/building-plugins-and-modules/01-index.md> |
| Legacy plugin creation reference | <https://backstage.io/docs/plugins/create-a-plugin/> |
| Plugin structure reference | <https://backstage.io/docs/plugins/structure-of-a-plugin/> |
| Composability and routing reference | <https://backstage.io/docs/plugins/composability/> |
| Community plugin contribution | <https://github.com/backstage/community-plugins/blob/main/CONTRIBUTING.md> |
| Backstage repository contribution | <https://github.com/backstage/backstage/blob/master/CONTRIBUTING.md> |

## Confirmed Official Guidance

- Frontend plugins can be created with `yarn new`; current docs point new work to the new frontend system.
- New frontend plugins start from `createFrontendPlugin` from `@backstage/frontend-plugin-api`.
- Backend plugins use the new backend system and `createBackendPlugin`.
- Backend modules use `createBackendModule` and extend one plugin through extension points.
- Community publication is a contribution process to `backstage/community-plugins`; acceptance depends on maintainer review.

## Freshness Gate

Before using this cached summary for implementation guidance, validate the target behavior against an exact first-party source commit or an official web page as described in [documentation-validation.md](documentation-validation.md).

## Use With Care

Some `backstage.io/docs/plugins/*` pages are legacy documentation. Use them for maintaining older plugins, but prefer the new frontend and backend system docs for new development.
