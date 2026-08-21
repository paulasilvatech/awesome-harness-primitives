# Backstage Plugin Types

Choose the plugin type before scaffolding or writing code.

| Type | Use for | Primary API or package pattern |
| --- | --- | --- |
| Frontend plugin | Pages, cards, tabs, entity content, dashboards, UI extension points | `createFrontendPlugin` |
| Backend plugin | New backend API or service owned by the plugin | `createBackendPlugin` |
| Backend module | Extending an existing backend plugin | `createBackendModule` |
| Catalog provider or processor | Ingesting or processing catalog entities | Catalog extension points |
| Scaffolder action or module | Custom Software Template actions | Scaffolder extension points |
| Search collator or module | Indexing custom content into Search | Search plugin extension points |
| Auth provider or resolver | Login provider, sign-in resolver, auth integration | Auth backend extension points |
| Permission policy or rule | Authorization policy and resource rules | Permission framework |
| TechDocs addon | Documentation rendering or publishing extension | TechDocs extension APIs |
| Common package | Shared types, schemas, clients, and helpers | `plugin-<id>-common` |
| Node package | Backend extension points or node utilities | `plugin-<id>-node` |

## Decision Rules

- If it renders in the browser, start with frontend plugin.
- If it exposes an API or talks to external services server-side, start with backend plugin.
- If it extends Catalog, Scaffolder, Search, Auth, Permissions, or TechDocs, prefer a module for that plugin.
- If both browser and backend need shared types, create a common package.
- If modules need extension points or backend utilities, create a node package.
