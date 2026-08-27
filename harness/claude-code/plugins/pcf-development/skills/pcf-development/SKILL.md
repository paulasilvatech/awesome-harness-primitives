---
name: pcf-development
description: >-
  Design, implement, review, and package Power Apps Component Framework code components for
  model-driven apps, canvas apps, and Power Pages. Use when the user asks about PCF manifests,
  lifecycle APIs, dataset or field controls, React platform libraries, PAC CLI tooling, ALM,
  performance, accessibility, security, testing, or deployment.
---

<!-- Generated from harness/github-copilot/plugins/pcf-development/skills/pcf-development/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# PCF development

Build supportable Power Apps Component Framework (PCF) code components using current Microsoft platform contracts, explicit host constraints, secure data access, and solution-aware ALM.

## When to invoke

- "Create a PCF field control for a model-driven app."
- "Review this ControlManifest.Input.xml."
- "Build a dataset component with React."
- "Why does this PCF control fail in a canvas app?"
- "Package and deploy this code component in a solution."

## Platform decisions

Confirm these decisions before generating or changing code:

| Decision | Options | Why it matters |
| --- | --- | --- |
| Host | Model-driven app, canvas app, Power Pages | API availability and authentication support differ. |
| Binding | Field, dataset, or unbound input | Determines manifest properties, lifecycle data, and outputs. |
| Rendering | Standard control or React control with platform libraries | Affects bundle size, React ownership, and initialization. |
| Data access | Bound values, dataset APIs, Dataverse Web API, connector | Canvas apps do not expose every Dataverse-dependent API. |
| Licensing | Standard or premium | Direct browser access to external services can make the component premium. |
| Delivery | Managed or unmanaged solution | Controls development, promotion, upgrade, and rollback behavior. |

Do not assume that an API available in a model-driven app is available in a canvas app. Verify host-specific support in the current PCF API reference.

## Component contract

Keep `ControlManifest.Input.xml`, TypeScript types, and runtime behavior aligned:

- Use a stable namespace, constructor, version, display keys, and description keys.
- Declare every input and output property with the correct usage, type, required state, and localization keys.
- Use a dataset only when the component truly consumes a collection; declare required columns and capabilities deliberately.
- Declare external domains under `external-service-usage` when the browser calls them directly.
- Request only the feature usage the component needs.
- Keep resource ordering deterministic and include generated type declarations.
- Validate the manifest with the installed PCF tooling instead of inventing schema elements.

Implement the lifecycle deliberately:

1. `init` stores framework callbacks and creates long-lived UI state.
2. `updateView` renders from the latest context and handles resize, visibility, dataset paging, and disabled state.
3. `getOutputs` returns only declared output properties.
4. `destroy` removes listeners, observers, timers, subscriptions, and framework resources.

Never trigger an unconditional render-update-output loop. Notify output changes only when component-owned output actually changes.

## React and dependency strategy

- Prefer React controls and Power Platform platform libraries when the target host and tooling support them.
- Do not bundle React or Fluent dependencies that the selected platform-library mode owns.
- When platform libraries are not used, bundle external dependencies into the component bundle and review size, licenses, and browser compatibility.
- Keep host integration in a thin adapter and test domain behavior outside the framework lifecycle.
- Avoid direct global DOM mutation; render inside the provided container.

## Security, privacy, and accessibility

- Do not store sensitive or durable data in `localStorage` or `sessionStorage`; Microsoft documents browser storage as insecure and unreliable for PCF state.
- Canvas PCF components must use connectors for authenticated data operations because custom authentication is not supported there.
- Treat manifest inputs, dataset values, URLs, and external responses as untrusted.
- Avoid `innerHTML`; when unavoidable, sanitize with a reviewed policy.
- Use least-privilege Dataverse access and never embed client secrets or tokens.
- Provide keyboard operation, visible focus, semantic roles, labels, sufficient contrast, zoom support, and screen-reader announcements.
- Respect high contrast, reduced motion, localization, and right-to-left layouts where applicable.

## Tooling and ALM workflow

Use the repository's installed versions and inspect `pac --version`, Node.js, package manifests, and lockfiles before changing dependencies.

Typical component flow:

```bash
pac pcf init --namespace <namespace> --name <component> --template field
npm install
npm run build
npm test
```

Typical solution flow:

```bash
pac solution init --publisher-name <publisher> --publisher-prefix <prefix>
pac solution add-reference --path <component-project>
dotnet build
```

Prefer source-controlled solution projects and environment-specific configuration. Do not publish, import, or upgrade a production solution without the target environment, solution type, dependency analysis, approval, and rollback path.

## Validation

Run the smallest existing checks that cover the component:

- TypeScript type-check and project build.
- Unit tests for state and rendering logic.
- Manifest and generated type validation through PCF tooling.
- Browser checks in every claimed host.
- Keyboard, screen reader, high contrast, responsive sizing, and localization checks.
- Solution build and import in a non-production environment.
- Performance checks for repeated `updateView`, large datasets, paging, and cleanup after navigation.

When validation cannot run, report the missing PAC CLI, environment, host, credentials, test project, or solution metadata explicitly.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Control is absent from the maker experience | Manifest type, supported host, solution import, publisher prefix, and component version. |
| Values do not persist | Output usage, `notifyOutputChanged`, `getOutputs`, bound property type, and disabled state. |
| Canvas behavior differs | Host API availability, connector use, custom-auth restriction, and dataset support. |
| Bundle is unexpectedly large | React/platform-library mode, duplicated dependencies, source maps, and bundled assets. |
| Memory or event duplication grows | Cleanup in `destroy` and idempotence of `updateView`. |
| Solution upgrade fails | Dependencies, managed properties, version ordering, publisher identity, and import logs. |

## Limits

- Use the `power-platform-expert` agent for broader Dataverse, Power Automate, governance, or architecture decisions.
- Verify licensing and tenant policies with the target administrator; do not infer them from source code.
- Do not claim an API, host, or preview feature is supported without current Microsoft documentation or target-environment evidence.

## Output template

```markdown
## PCF implementation result

**Host:** <model-driven|canvas|Power Pages>
**Binding:** <field|dataset|input>
**Status:** <implemented|reviewed|blocked>

### Contract
- Manifest changes: <summary>
- Lifecycle behavior: <summary>
- Data and licensing: <summary>

### Quality
- Security and privacy: <result>
- Accessibility: <result>
- Performance: <result>
- ALM and rollback: <result>

### Validation
- <command or host test>: <pass|fail|not run with reason>
```

## Quality gate

- [ ] Host, binding, rendering strategy, data access, licensing, and delivery model are explicit.
- [ ] Manifest declarations match TypeScript inputs, outputs, resources, and capabilities.
- [ ] Lifecycle methods are idempotent and `destroy` releases resources.
- [ ] No unsupported canvas authentication or insecure browser storage is introduced.
- [ ] Accessibility and performance behavior are validated in every claimed host.
- [ ] Solution packaging and environment promotion preserve an approval and rollback path.
- [ ] Results distinguish executed validation from recommendations.

## References

- https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview
- https://learn.microsoft.com/en-us/power-apps/developer/component-framework/limitations
- https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/
