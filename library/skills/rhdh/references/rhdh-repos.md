## Purpose

Reference of all RHDH-related repositories, what each one is used for, and how they relate to each other. Use this when navigating between projects or understanding the overall RHDH ecosystem.

## Repository Map

### rhdh

- **Upstream:** <https://github.com/redhat-developer/rhdh>
- **Description:** The main Red Hat Developer Hub application. Enterprise Internal Developer Portal built on Backstage. Formerly `janus-idp/backstage-showcase`.
- **Tech stack:** Node.js 22, TypeScript, React, Yarn 4, Turbo monorepo
- **Key concepts:**
  - **Scalprum dynamic loading:** Frontend plugins are loaded at runtime via [Scalprum](https://github.com/scalprum/scaffolding) (federated module loader), not compiled into the app. `packages/app/` renders `<ScalprumRoot>` which fetches plugin manifests from `/api/scalprum/plugins` served by `@internal/plugin-scalprum-backend`.
  - **`app-next`:** Parallel frontend using Backstage's standard Module Federation (`@backstage/frontend-dynamic-feature-loader`). Started with `APP_CONFIG_app_packageName=app-next ENABLE_STANDARD_MODULE_FEDERATION=true`.
  - **Dynamic plugin wrappers:** `dynamic-plugins/wrappers/` contains ~48 thin wrapper packages. Frontend wrappers use `--in-place` (produce `dist-scalprum/`), backend wrappers use `--embed-package` (self-contained `dist-dynamic/`). This is a **separate Yarn workspace** with its own `yarn.lock`.
  - **Layered config:** `app-config.yaml` (base dev) -> `app-config.dynamic-plugins.yaml` (frontend plugin UI integration: mount points, routes, menu items, icons, route bindings) -> `app-config.production.yaml` (production overlay). `dynamic-plugins.default.yaml` is **generated** (do not edit manually) from `default.packages.yaml`.
  - **Service override mechanism:** Each default service factory in `packages/backend/src/defaultServiceFactories.ts` can be disabled via `ENABLE_{SERVICE_ID}_OVERRIDE=true` env var to let a dynamic plugin provide its own.
  - **Branching:** `main` for active development; `release-1.x` for maintained releases; `dependencies/backstage-latest` for tracking upstream.
- **Key paths:** `packages/app/` (frontend), `packages/backend/` (backend), `plugins/` (internal `@internal/*` plugins), `dynamic-plugins/wrappers/` (wrapper packages), `app-config.dynamic-plugins.yaml` (UI integration config), `default.packages.yaml` (master plugin manifest), `backstage.json` (upstream version tracking)

### rhdh-downstream

- **Upstream:** <https://gitlab.cee.redhat.com/rhidp/rhdh>
- **Description:** Downstream (productized) build of RHDH. Internal GitLab repository that produces the official Red Hat-supported container images published to `registry.redhat.io`. Syncs from the upstream `redhat-developer/rhdh` GitHub repo and applies Red Hat-specific patches, branding, and build configuration for Konflux/Brew pipelines.
- **Note:** Requires Red Hat VPN / internal network access.

### rhdh-cli

- **Upstream:** <https://github.com/redhat-developer/rhdh-cli>
- **Description:** CLI tool for developing, packaging, and distributing dynamic plugins for RHDH. Successor to `@janus-idp/cli`. Published as `@red-hat-developer-hub/cli` on npm. Extends/wraps `@backstage/cli`.
- **Tech stack:** Node.js 22, TypeScript, Webpack, esbuild, Commander.js, Yarn 3
- **Key concepts:**
  - **`plugin export`:** Detects plugin role from `package.json`, routes to backend or frontend export. Backend: creates `dist-dynamic/` via `productionPack()`, moves `@backstage/*` to `peerDependencies`, embeds `-common`/`-node` siblings, runs `yarn install --production`, validates entry points (`BackendFeature`/`BackendFeatureFactory` default export). Frontend: generates Scalprum assets in `dist-scalprum/` via `DynamicRemotePlugin` from `@openshift/dynamic-plugin-sdk-webpack`, plus optional Module Federation assets.
  - **`plugin package`:** Packages exported plugins as OCI container images or directories. Discovers plugins in monorepos, runs export, stages into temp dir, builds `FROM scratch` container with `io.backstage.dynamic-packages` annotation, or copies to `--export-to` directory.
  - **Embedded packages:** `--embed-package` bundles related packages into `dist-dynamic/embedded/`. Auto-detects `-common` and `-node` siblings. Versions suffixed with `+embedded`.
  - **Shared packages:** All `@backstage/*` packages are shared by default (moved to `peerDependencies`). Customizable via `--shared-package` with support for `!` exclusion and `/regex/` patterns.
  - **Versioning:** Major.minor synced with RHDH releases (CLI 1.8.x works with RHDH 1.8.z). Patch incremented independently.
  - **Branching:** `main` for active development; `release-1.x` for maintenance.
- **Key paths:** `src/commands/export-dynamic-plugin/` (export logic), `src/commands/package-dynamic-plugins/` (packaging), `src/lib/bundler/scalprumConfig.ts` (webpack config), `src/lib/schema/collect.ts` (config schema), `bin/rhdh-cli` (entry point)

### rhdh-local

- **Upstream:** <https://github.com/redhat-developer/rhdh-local>
- **Description:** Docker Compose-based local development and testing environment for RHDH. The fastest way to run RHDH locally without a Kubernetes cluster. Not for production use.
- **Tech stack:** Docker/Podman Compose, PostgreSQL (optional), Bash scripts
- **Key concepts:**
  - **Two-container architecture:** `install-dynamic-plugins` init container installs plugins into a shared `dynamic-plugins-root` volume, then `rhdh` main container starts the Backstage backend. Port `7007` for UI, port `9229` for Node.js debugger.
  - **Override-based config:** Users never edit defaults; they create git-ignored override files. `default.env` -> `.env`, `app-config.yaml` -> `app-config.local.yaml`, `dynamic-plugins.yaml` -> `dynamic-plugins.override.yaml`, `users.yaml` -> `users.override.yaml`.
  - **Four plugin sources:** (1) Local directory via `local-plugins/`, (2) OCI image via `oci://`, (3) tarball URL, (4) pre-bundled in RHDH image (`./dynamic-plugins/dist/`).
  - **Frontend hot-reload:** Use `compose-dynamic-plugins-root.yaml` override to bind-mount `./dynamic-plugins-root` as host directory, then run `npx @red-hat-developer-hub/cli plugin export --dev --dynamic-plugins-root <path>`. Re-export and refresh browser - no container restart needed.
  - **In-memory SQLite by default.** PostgreSQL can be opted into by uncommenting sections in `compose.yaml`.
  - **Branching:** `main` for active development; `release-1.x` for maintained releases.
- **Key paths:** `compose.yaml` (main compose), `configs/app-config/` (app configuration), `configs/dynamic-plugins/` (plugin configuration), `local-plugins/` (local plugin binaries), `docs/` (built-in TechDocs)

### rhdh-operator

- **Upstream:** <https://github.com/redhat-developer/rhdh-operator>
- **Description:** Kubernetes Operator for automated installation, configuration, and lifecycle management of RHDH instances on Kubernetes and OpenShift. CRD group is `rhdh.redhat.com`, primary CR kind is `Backstage` (API version `v1alpha5`).
- **Tech stack:** Go, Kubernetes client libraries, Ginkgo/Gomega testing, OpenShift API integration, kustomize
- **Key concepts:**
  - **Backstage CR spec:** `application` (appConfig configMaps, dynamicPluginsConfigMapName, extraFiles, extraEnvs, route), `database` (enableLocalDb, authSecretName), `deployment` (patch via kustomize merge2, kind: Deployment or StatefulSet), `monitoring` (ServiceMonitor toggle).
  - **Reconciliation flow:** Get CR -> preprocess spec (read ConfigMaps/Secrets, compute SHA-256 hash) -> init object model (Phase 1: load default config, Phase 2: overlay rawRuntimeConfig, Phase 3: apply CR spec) -> apply plugin dependencies -> server-side apply all objects -> clean up disabled features -> update status conditions.
  - **Auto-refresh:** External ConfigMaps/Secrets are labeled `rhdh.redhat.com/ext-config-sync=true` and watched. Config hash stored as `rhdh.redhat.com/ext-config-hash` pod annotation; hash change triggers rolling restart.
  - **PostgreSQL provisioning:** When `enableLocalDb: true` (default), creates a Secret (random password), StatefulSet (PostgreSQL 15, 1Gi PVC), and Service. Secret is immutable after creation.
  - **Platform detection:** Auto-detects OpenShift/EKS/AKS/GKE/vanilla K8s at startup. OpenShift gets Route + ClusterIP; K8s gets NodePort + fsGroup. Platform overrides use `.k8s` file suffix.
  - **Profiles:** `rhdh` (primary, default), `backstage.io` (community), `external` (no default config). Most `make` commands accept `PROFILE=`.
  - **Branching:** `main` for active development; `release-1.x` for maintained releases.
- **Key paths:** `api/v1alpha5/backstage_types.go` (CRD types), `internal/controller/` (reconciler), `pkg/model/` (runtime object model), `config/profile/rhdh/default-config/` (default manifests), `examples/rhdh-cr.yaml` (comprehensive example CR)

### rhdh-chart

- **Upstream:** <https://github.com/redhat-developer/rhdh-chart>
- **Description:** Helm chart for deploying RHDH on Kubernetes and OpenShift. Alternative deployment method to the operator. The chart is a **wrapper** around the upstream Backstage Helm chart (pulled as subchart with alias `upstream`).
- **Tech stack:** Helm 3, Kubernetes/OpenShift YAML manifests, chart-testing, KinD
- **Key concepts:**
  - **Subchart architecture:** Upstream Backstage chart aliased as `upstream` in `Chart.yaml`. All upstream values accessible under `upstream:` key. Bitnami `common` chart also included.
  - **Dynamic plugins via Helm:** `global.dynamic.includes` (default: `dynamic-plugins.default.yaml`) + `global.dynamic.plugins` (user additions). Init container `install-dynamic-plugins` installs into 5Gi ephemeral PVC. Supports OCI plugins, npm tarballs, and pre-bundled plugins.
  - **Route vs Ingress:** OpenShift Route enabled by default (`route.enabled: true`) with edge TLS. For vanilla K8s, set `route.enabled: false` + `upstream.ingress.enabled: true`.
  - **Backend auth:** `global.auth.backend.enabled: true` (default) auto-generates a secret for service-to-service auth.
  - **Branching:** `main` for active development; `release-1.x` for maintained releases; `gh-pages` for published chart index.
- **Key paths:** `charts/backstage/` (primary chart), `charts/backstage/values.yaml` (main values), `charts/backstage/templates/` (custom templates)

### rhdh-plugin-export-overlays

- **Upstream:** <https://github.com/redhat-developer/rhdh-plugin-export-overlays>
- **Description:** Metadata and automation hub for packaging community Backstage plugins as dynamic plugins for RHDH. Contains workspace definitions that point to upstream plugin repos and uses overlays/patches to customize them for dynamic loading. Automated workflows publish OCI container images to `ghcr.io`.
- **Tech stack:** GitHub Actions, YAML/JSON configuration, OCI container images, Bash scripting
- **Key concepts:**
  - **Workspaces:** Each `workspaces/<name>/` directory defines a group of related plugins with `source.json` (upstream repo/commit) and `plugins-list.yaml` (plugins to export)
  - **Overlays:** Replace/add entire files in plugin source before building (`plugins/<name>/overlay/`)
  - **Patches:** Apply line-by-line diffs at workspace level (`patches/*.patch`)
  - **OCI tags:** `bs_<backstage_version>__<plugin_version>` (e.g., `bs_1.45.3__2.4.3`)
  - **Branching:** `main` for next RHDH release; `release-x.y` branches for specific releases
- **Companion repo:** Works closely with `rhdh-plugin-export-utils`

### rhdh-plugin-export-utils

- **Upstream:** <https://github.com/redhat-developer/rhdh-plugin-export-utils>
- **Description:** Collection of reusable GitHub Actions and callable workflows for exporting, packaging, and validating Backstage plugins as dynamic plugins for RHDH. Primary consumer is `rhdh-plugin-export-overlays`.
- **Tech stack:** GitHub Actions (composite actions), Bash scripting, TypeScript (validate-metadata)
- **Key concepts:**
  - **`override-sources` action:** Applies workspace-level patches then per-plugin source overlays.
  - **`export-dynamic` action:** Iterates `plugins-list.yaml`, runs CLI export per plugin, optionally packages as OCI image. Supports skip-if-unchanged via `last-publish-commit`.
  - **`validate-metadata` action:** Validates `metadata/*.yaml` files against `plugins-list.yaml` and `package.json`.
  - **`update-overlay` action:** Proposes overlay workspace PRs via GitHub API for auto-discovered plugin versions.
  - **Callable workflows:** `export-dynamic.yaml` (single-workspace pipeline), `export-workspaces-as-dynamic.yaml` (multi-workspace orchestrator), `update-plugins-repo-refs.yaml` (npm discovery), `check-backstage-compatibility.yaml` (compatibility report).
  - **Branching:** Single `main` branch only. All consumers reference actions at `@main`.

### rhdh-plugin-catalog

- **Upstream:** <https://gitlab.cee.redhat.com/rhidp/rhdh-plugin-catalog>
- **Description:** Midstream infrastructure repository that manages building, packaging, and publishing Backstage plugins as OCI artifacts for RHDH. Syncs plugin source from `rhdh-plugin-export-overlays`, builds plugins via Konflux CI/CD, and maintains a catalog index of all available plugins. Publishes to `quay.io/rhdh/` and `registry.redhat.io/rhdh/`.
- **Tech stack:** Node.js, TypeScript, Yarn 3, Backstage CLI, Python (build scripts), Tekton/Konflux pipelines, Docker/Podman
- **Key concepts:**
  - **Workspaces:** 24 plugin workspace directories under `workspaces/`. Each is an independent monorepo with `packages/`, `plugins/`, `package.json`, `yarn.lock`, `manifest.json`, and `backstage.json`.
  - **Catalog index:** `catalog-index/index.json` is the master catalog of all plugins. Generated by `build/scripts/generateCatalogIndex.py`.
  - **Konflux pipelines:** 114 Tekton PipelineRun definitions in `.tekton/`. Each plugin has a dedicated pipeline triggered by changes to its workspace directory.
  - **Upstream sync:** `build/ci/sync-midstream.sh` syncs overlays from `rhdh-plugin-export-overlays` into `overlay-repo/`, updates `plugin_builds/` metadata, and regenerates the catalog index.
  - **Branching:** `main` for active development; `rhdh-*-rhel-9` for release-specific midstream branches.
- **Key paths:** `workspaces/` (plugin source), `plugin_builds/` (build metadata), `catalog-index/` (catalog index and default configs), `.tekton/` (Konflux pipelines), `build/scripts/` (build automation scripts)

### rhdh-plugins

- **Upstream:** <https://github.com/redhat-developer/rhdh-plugins>
- **Description:** Central repository for Backstage plugins developed by Red Hat for use with RHDH. Multi-workspace monorepo modeled after `backstage/community-plugins`. Each workspace is an independent mini-monorepo with its own `yarn.lock`, release cycle, and changeset history. Publishes to `@red-hat-developer-hub` npm namespace.
- **Tech stack:** Node.js 22, TypeScript, Yarn 4 (Berry, `node-modules` linker), Backstage plugin SDK, Jest, Playwright
- **Key concepts:**
  - **Workspace independence:** Each `workspaces/<name>/` has its own `package.json` (named `@internal/<name>`, `private: true`), `yarn.lock`, `.changeset/`, and `backstage.json`. Run `yarn install` from within the workspace, not the root.
  - **Workspace structure:** `workspaces/<name>/packages/app/` (dev frontend), `packages/backend/` (dev backend), `plugins/<plugin-name>/` (publishable plugins). Plugin packages follow `-backend`, `-common`, `-node` suffix conventions.
  - **Changesets:** `yarn changeset` from workspace root. On merge to `main`, automation creates a "Version Packages" PR on `changesets-release/<workspace>/main` branch.
  - **Notable workspaces:** `bulk-import`, `lightspeed` (AI assistant), `orchestrator` (SonataFlow), `homepage`, `theme`, `extensions`, `global-header`, `adoption-insights`, `scorecard`, `ai-integrations`, `translations`, `konflux`, `mcp-integrations`.
  - **Creating new workspace:** `yarn create-workspace` from repo root. Creating a plugin within a workspace: `cd workspaces/<name> && yarn new`.
  - **Branching:** `main` for active development; `1.2` for release maintenance; `changesets-release/<workspace>/main` for automated version PRs.
- **Key paths:** `workspaces/` (all plugin workspaces), `scripts/ci/` (CI helper scripts), `.github/CODEOWNERS` (per-workspace ownership)

### rhdh-dynamic-plugin-factory

- **Upstream:** <https://github.com/redhat-developer/rhdh-dynamic-plugin-factory>
- **Description:** Container image and tooling for building dynamic plugins locally. Provides a pre-configured build environment with all necessary dependencies (Node.js, Yarn, Backstage CLI) so plugin authors can export and package plugins without setting up a full development environment. Used via `podman` or `docker`.
- **Tech stack:** Container (Podman/Docker), Node.js, Yarn, Backstage CLI
- **Key concepts:**
  - **Container-based builds:** Run `podman run` or `docker run` with the factory image to build plugins in an isolated environment.
  - **Used by overlay workflows:** `rhdh-plugin-export-overlays` can use the factory container for local plugin builds.
- **Key paths:** `Containerfile` (image definition)

### backstage

- **Upstream:** <https://github.com/backstage/backstage>
- **Description:** The upstream Backstage framework - the CNCF open-source foundation that RHDH is built upon. Originally created by Spotify. Provides the core Software Catalog, Software Templates, TechDocs, Search, and the plugin system.
- **Tech stack:** Node.js, TypeScript, React, Yarn Berry, PostgreSQL
- **Key concepts:**
  - **New backend system (current standard):** `createBackendPlugin()`, `createBackendModule()`, `createServiceRef()`, `createExtensionPoint()` from `@backstage/backend-plugin-api`. Services are dependency-injected via `coreServices`.
  - **Plugin package sets:** A feature like "catalog" spans multiple packages: `-backend` (backend plugin), `-node` (extension points/shared backend types), `-react` (shared React hooks/components), `-common` (isomorphic shared code), `-backend-module-*` (backend modules).
  - **Software Catalog:** Central entity registry. Entity lifecycle: Ingestion (entity providers) -> Processing (processors validate/enrich/emit relations) -> Stitching (assemble final entity). Entity kinds: Component, API, Resource, System, Domain, User, Group, Location, Template.
  - **Release cadence:** Monthly minor releases (`v1.X.0`), patch releases as needed. Individual packages have their own semver; `@backstage/release-manifests` maps package versions to Backstage releases.
  - **Branching:** `master` (not `main`) is the default branch. No long-lived release branches - releases are tags from `master`.
- **Key paths:** `packages/` (core framework packages), `plugins/` (~155 plugin packages), `docs/` (documentation)

## Ecosystem Relationships

```
backstage (upstream framework)
    |
    v
rhdh (enterprise distribution, github.com)
    |
    +---> rhdh-downstream (productized build, gitlab.cee.redhat.com)
    |         builds from rhdh, produces registry.redhat.io images
    |
    +-- rhdh-cli (plugin development tooling)
    +-- rhdh-plugins (Red Hat plugin collection)
    |
    +-- rhdh-plugin-export-overlays (community plugin packaging & OCI publishing)
    |       |
    |       +-- uses rhdh-plugin-export-utils (reusable GitHub Actions)
    |
    +-- rhdh-plugin-catalog (midstream plugin builds, OCI artifacts & catalog index)
    |       syncs from rhdh-plugin-export-overlays
    |
    +-- Deployment:
    |   +-- rhdh-operator (Kubernetes/OpenShift operator)
    |   +-- rhdh-chart (Helm chart)
    |
    +-- rhdh-local (local dev/test environment)
    +-- rhdh-dynamic-plugin-factory (container for local plugin building)
```

## Common Workflows

- **Plugin development:** Work in `rhdh-plugins`, use `rhdh-cli` to export/package, test with `rhdh-local`
- **Core RHDH changes:** Work in `rhdh`, reference `backstage` for upstream behavior
- **Deployment/operator changes:** Work in `rhdh-operator` or `rhdh-chart`
- **Plugin packaging:** Work in `rhdh-plugin-export-overlays` to add/update plugins as dynamic plugins; uses actions from `rhdh-plugin-export-utils`
- **Midstream plugin builds:** Work in `rhdh-plugin-catalog` for Konflux pipeline management, catalog index updates, and OCI artifact publishing to Red Hat registries
- **CI/CD actions for plugins:** Work in `rhdh-plugin-export-utils` to modify the reusable GitHub Actions
