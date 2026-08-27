---
paths:
  - "**/*.{ts,tsx,js,jsx}"
  - "**/vite.config.*"
  - "**/package.json"
  - "**/tsconfig.json"
  - "**/power.config.json"
---

<!-- Generated from harness/github-copilot/instructions/power-apps-code-apps.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Power Apps Code Apps conventions for TypeScript, React, Vite, Power Platform SDK integration, generated connector services, security, testing, deployment, and current platform limitations.

# Power Apps Code Apps Conventions — TypeScript, React, and Power Platform

These instructions apply to TypeScript, React, Vite, package, tsconfig, and Power Apps Code Apps configuration files matched by the `applyTo` globs. They are authoritative for Code Apps project shape, Power Platform SDK usage, generated connector services, React patterns, data access, security, testing, deployment, troubleshooting, and documented preview limitations; organization security policy, Power Platform DLP policy, and app-specific architecture decisions win where they are stricter.

## Project Context and Required Tooling

Build Power Apps Code Apps as code-first web apps that integrate with Power Platform through the supported SDK and PAC CLI.

| Concern | Convention |
| --- | --- |
| Stack | Use TypeScript, React, and Vite for new Code Apps unless the project has a documented exception. |
| SDK | Use `@microsoft/power-apps` at the project-approved current version such as `^1.0.3`; keep SDK calls typed and isolated behind services or hooks. |
| CLI | Use PAC CLI for project initialization, connector generation, running, environment selection, and deployment. |
| Local port | Keep local development on port `3000` because the Power Platform SDK expects that port in the supported development flow. |
| Licensing | Treat Power Apps Premium as an end-user production licensing requirement and do not imply that Code Apps remove premium licensing obligations. |
| Scripts | Preserve `"dev": "concurrently \"vite\" \"pac code run\""`, `"build": "tsc -b && vite build"`, `npm run build`, and `pac code push` as the standard local run, build, and deploy shape unless the project defines an equivalent. |
| Dependencies | Install and keep documented dependencies such as `@microsoft/power-apps`, `@fluentui/react-components`, `concurrently`, `powerbi-client-react`, `botframework-directlinejs`, `botframework-webchat`, `framer-motion`, and `react-intl` only when the corresponding integration is used. |

## Project Structure and Generated Code

Separate custom code from generated connector artifacts so PAC regeneration does not overwrite hand-written logic.

| Path or item | Convention |
| --- | --- |
| `src/` | Keep application source under `src/*` with `components/`, `hooks/`, `generated/`, `utils/`, `types/`, `PowerProvider.tsx`, and `main.tsx`. |
| Generated services | Keep PAC-generated connector services in `generated/services/` and generated TypeScript models in `generated/models/`; do not hand-edit generated output. |
| Component files | Use `kebab-case` for files and `PascalCase` for components. |
| Imports | Configure Vite and TypeScript aliases consistently with `"@": path.resolve(__dirname, "./src")`. |
| Documentation | Maintain `README.md`, troubleshooting notes, deployment requirements, changelog entries, and architectural decision records for major choices. |

## TypeScript and Vite Configuration

Use strict TypeScript while preserving SDK compatibility.

| Configuration | Convention |
| --- | --- |
| SDK compatibility | Set `verbatimModuleSyntax: false` in `tsconfig.json`; this is required for Power Apps SDK compatibility in current Code Apps patterns. |
| Compiler options | Preserve `target: ES2020`, `lib: ["ES2020", "DOM", "DOM.Iterable"]`, `module: ESNext`, `moduleResolution: bundler`, `allowImportingTsExtensions`, `resolveJsonModule`, `isolatedModules`, `noEmit`, `jsx: react-jsx`, `strict`, `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch`, `baseUrl`, and `paths`. |
| Types | Define app-specific interfaces, use generated models for connector responses, and avoid `any` for connector payloads. |
| Errors | Model error types explicitly and use React error boundaries for rendering failures. |
| Build hygiene | Keep `npm audit`, TypeScript build, and Vite build checks in CI/CD where the project already uses them. |

## Power Platform and Connector Integration

Use supported connector and SDK patterns. Keep authentication, consent, and connector calls visible and testable.

| Integration | Convention |
| --- | --- |
| Provider | Use the v1.0 no-initialization `PowerProvider` pattern: `import type { ReactNode } from "react"; export default function PowerProvider({ children }: { children: ReactNode }) { return <>{children}</>; }`. |
| Services | Use generated TypeScript services from PAC CLI for connector operations and keep request/response handling behind service wrappers or hooks. |
| Authentication | Use Microsoft Entra ID and the Power Platform consent flow; handle connector consent dialogs and permission management gracefully. |
| Supported connectors | Follow supported patterns for SQL Server including Azure SQL, SharePoint, Office 365 `Users/Groups`, Azure Data Explorer, OneDrive for Business, Microsoft Teams, and Dataverse `CRUD` operations. |
| PCF controls | Wrap Power Apps Component Framework controls with components such as `PCFControlWrapper` from `components/PCFControlWrapper`; handle PCF event and data binding explicitly. |
| Power BI | Use `PowerBIEmbed`, `TokenType.Aad`, `embedConfig`, `reportId`, `embedUrl`, `accessToken`, and hidden filter panes for embedded analytics when Power BI reports are part of the app. |
| AI Builder | Keep `AIBuilderService.ProcessDocument`, `AIBuilderService`, `ProcessDocument`, `FormData`, `modelId`, and `document-processing-model-id` patterns for document processing, prediction, sentiment analysis, and object detection. |
| Power Virtual Agents | Use `DirectLine`, `WebChat`, and chatbot token handling only through secure backend or connector paths; pass Code App context deliberately. |

## React, State, and UI Composition

Prefer functional components and explicit state boundaries.

| Area | Convention |
| --- | --- |
| Components | Use functional components, hooks, clear props interfaces, composition over inheritance, and single-responsibility component design. |
| State | Use React built-in state for simple cases; use context to avoid prop drilling; consider Redux Toolkit only for complex normalized state. |
| Data fetching | Use React Query or SWR when caching, deduplication, retries, and loading states justify the dependency. |
| Loading and errors | Every connector operation exposes loading, success, empty, and error states with meaningful user messages. |
| Fluent UI | Prefer Fluent UI React components from `@fluentui/react-components` when they align with the app's design system. |
| Responsive UI | Use mobile-first responsive design with CSS Grid/Flexbox, CSS modules or CSS-in-JS, CSS custom properties, and component-level styling. |
| Design systems | Use design tokens for spacing, colors, and typography; document reusable components with Storybook when a shared component library exists. |
| Theming | Implement `ThemeContext`, `ThemeContext.Provider`, and `ThemeProvider` patterns deliberately; support `theme-${theme}` classes, dark mode, and system preference detection when required. |
| Animation | Use `framer-motion`, `motion`, `AnimatePresence`, `AnimatedCard`, CSS transforms, and `will-change` only when animation improves usability and remains performant. |

## Data, Dataverse, Offline, and Performance

Treat data access as a typed integration boundary and design large apps for performance.

| Concern | Convention |
| --- | --- |
| Sensitive data | Store sensitive data in data sources or managed secret stores, never in application code or client-visible configuration. |
| Validation | Validate and sanitize input before connector calls; respect Power Platform data loss prevention policies. |
| Dataverse relationships | Model `many-to-many` relationships with junction tables and services such as `UserRoleService`; handle polymorphic lookups with `AccountService`, `ContactService`, `customerType`, and `customerId`; use `$expand` and `$filter` for efficient relationship queries. |
| Offline | Use service workers, `navigator.serviceWorker.register('/sw.js')`, `IndexedDB`, `OfflineDataStore`, background sync, and PWA capabilities only when offline support is a real requirement. |
| Performance | Use `React.memo`, `useMemo`, code splitting, lazy loading, tree shaking, pagination, efficient connector query patterns, and request deduplication for large data sets. |
| Caching | Cache frequently accessed data appropriately and handle sync conflict resolution when coming back online. |

## Accessibility, Internationalization, and UX

Code Apps are web apps and must meet web accessibility and localization expectations.

| Area | Convention |
| --- | --- |
| Accessibility | Follow `WCAG 2.1`, semantic HTML, full keyboard navigation, screen reader testing with `NVDA`, `JAWS`, and `VoiceOver`, and automated checks with `axe-core`. |
| ARIA | Use `ARIA`, `aria-modal`, `aria-labelledby`, `modal-title`, `data-autofocus`, and focus restoration only when native semantics are insufficient. |
| Modal behavior | Use modal classes such as `modal-open` and `modal-hidden` consistently and lock body scroll only while the modal is open. |
| Responsive patterns | Use `container-type: inline-size`, `.card-container`, `@container (min-width: 400px)`, `grid-template-columns`, fluid typography, and adaptive layouts where component size matters more than viewport size. |
| i18n | Use `react-intl`, `FormattedMessage`, `useIntl`, `WelcomeMessage`, locale-specific date and number formatting, language detection, RTL support, and translation management for multi-language apps. |
| RTL | Support right-to-left (`to-left`) language layouts for Arabic and Hebrew where localization is required. |

## Security and Error Handling

Keep security controls explicit and user-facing failures safe.

| Concern | Convention |
| --- | --- |
| Secrets | Never store secrets or sensitive configuration in code; use Power Platform authentication, authorization, DLP, and managed secret stores such as Azure Key Vault when deployment automation needs secrets. |
| Web security | Use HTTPS-only communication, validate and sanitize input, and follow OWASP guidance for web applications. |
| Errors | Implement error boundaries, connector-specific error handling, retry logic for transient failures, network connectivity handling, and user-safe error messages. |
| Logging | Log enough diagnostic detail for operators without exposing tokens, connector payload secrets, or sensitive business data. |
| CSP limitation | Document that Content Security Policy (`CSP`) is not yet supported for Code Apps when that limitation affects design decisions. |

## Testing and DevOps

Test the app as TypeScript, React, and Power Platform integration code.

| Area | Convention |
| --- | --- |
| Unit tests | Write unit tests for business logic, utilities, and pure data transformations. |
| Components | Test React components with React Testing Library and mock Power Platform connectors. |
| Integration | Add integration tests for critical connector flows, authentication prompts, error cases, and edge cases. |
| CI/CD | Use GitHub Actions or Azure DevOps where appropriate; preserve `PowerPlatformToolInstaller@2`, `PowerPlatformSetConnectionVariables@2`, `PowerPlatformPublishCustomizations@2`, `PowerPlatformSPN`, `$(AppId)`, `$(ClientSecret)`, and `$(TenantId)` in pipeline examples. |
| Environments | Manage `dev/test/staging/prod` with environment-specific config such as `config/development.json` and placeholders like `https://<dev-environment>.crm.dynamics.com` and `apiVersion: 9.2`. |
| Releases | Use semantic versioning, code review, linting, formatting with ESLint and Prettier, automated tests, environment promotion, blue-green or canary deployment where supported, rollback strategies, and production monitoring. |
| Deployment commands | Build with `npm run build` before `pac code push`; inspect bundle size with `npm run build --report` when performance issues appear. |

## Current Limitations and Workarounds

Preserve current platform limitations so generated guidance does not promise unsupported behavior.

| Limitation | Convention or workaround |
| --- | --- |
| Content Security Policy | `CSP` is not yet supported; use alternative compensating controls and document the risk. |
| Storage SAS IP restrictions | Storage SAS IP restrictions are not supported; do not design security that depends on them. |
| Git integration | No Power Platform Git integration exists for Code Apps; use external Git workflows and PAC CLI automation. |
| Dataverse solution packaging | Dataverse solutions are supported, but solution packager and source code integration are limited; plan manual or pipeline-assisted packaging accordingly. |
| Application Insights | Application Insights is supported through SDK logger configuration, not built-in native integration; use alternative error tracking if needed. |

## Troubleshooting

Keep common failure commands and checks available in guidance.

| Symptom | Check or command |
| --- | --- |
| Port 3000 conflict | Find and stop the process with `netstat -ano | findstr :3000` and `taskkill /PID {PID} /F` on Windows. |
| Authentication failures | Verify PAC auth with `pac auth list`; reset with `pac auth clear` and `pac auth create` when needed. |
| Package installation failures | Clear npm cache with `npm cache clean --force`, reinstall dependencies, and rerun the build. |
| TypeScript compilation errors | Check `verbatimModuleSyntax: false`, SDK compatibility, generated models, and path aliases. |
| Connector permission errors | Verify connector setup, consent flow, admin permissions, and connection status in Power Platform. |
| PowerProvider issues | Ensure v1.0 apps do not wait on SDK initialization. |
| Vite dev server issues | Ensure host and port configuration match the Code Apps requirements. |
| Build failures | Run `npm audit`, verify dependency versions, and check Vite and TypeScript configuration. |
| Environment mismatch | Confirm the selected environment with `pac env list`. |
| App timed out | Verify `npm run build` ran successfully and deployment output is valid. |
| Data loading failures | Inspect network requests, connector permissions, generated service calls, and retry behavior. |
| UI rendering issues | Check Fluent UI compatibility, responsive layout, accessibility state, and error boundaries. |

## Implementation Vocabulary

Preserve these identifiers because existing Code Apps, samples, and generated integrations commonly reference them: `AIBuilderService`, `AIBuilderService.ProcessDocument`, `PCFControlWrapper`, `CustomChartControl`, `PowerBIEmbed`, `PowerProvider`, `PowerPlatformPublishCustomizations`, `PowerPlatformSetConnectionVariables`, `PowerPlatformToolInstaller`, `PowerPlatformSPN`, `TokenType.Aad`, `React.FC`, `React.ReactNode`, `ReactNode`, `ThemeContext.Provider`, `ButtonProps`, `Button`, `DashboardComponent`, `ChatbotComponent`, `MyComponent`, `AnimatedCard`, `Modal`, `Account`, `AccountService`, `Contact`, `ContactService`, `UserRoleService`, `DirectLine`, `WebChat`, `OfflineDataStore`, `FormattedMessage`, `WelcomeMessage`, `HTMLElement`, `DOM.Iterable`, `ES2020`, `ESNext`, `HTTP`, `HTTPS`, `OWASP`, `UI/UX`, `Grid/Flexbox`, `CRUD`, `CI/CD`, `README`, `ARIA`, `WCAG`, `NVDA`, `JAWS`, `VoiceOver`, `botframework-directlinejs`, `botframework-webchat`, `powerbi-client-react`, `fluentui/react-components`, `microsoft/power-apps`, `react-components`, `react-jsx`, `framer-motion`, `react-intl`, `axe-core`, `btn-disabled`, `card-container`, `container-based`, `container-type`, `inline-size`, `min-width`, `grid-template-columns`, `many-to-many`, `to-many`, `type-safe`, `self-documenting`, `well-documented`, `well-organized`, `mobile-first`, `mobile-friendly`, `connector-specific`, `environment-specific`, `request/response`, `app-specific`, `built-in`, `blue-green`, `high-quality`, `document-processing-model-id`, `modal-open`, `modal-hidden`, `data-autofocus`, `aria-modal`, `aria-labelledby`, `modal-title`, `theme-${theme}`, `will-change`, `to-left`, `config/development.json`, `generated/models/`, `generated/services/`, `components/PCFControlWrapper`, `src/*`, `Users/Groups`, `dev-environment`, `dev/test/staging/prod`, `@fluentui/react-components`, and `@microsoft/power-apps`.

## Good / Bad Examples

The examples below illustrate the required v1.0 `PowerProvider` shape and strict TypeScript compatibility.

**Good:**

```tsx
import type { ReactNode } from "react";

export default function PowerProvider({ children }: { children: ReactNode }) {
  return <>{children}</>;
}
```

Why: The provider matches current SDK behavior and does not block rendering while waiting for initialization that v1.0 Code Apps do not require.

**Bad:**

```tsx
export default function PowerProvider({ children }: { children: any }) {
  initializePowerSdkWithSecretFromCode();
  return <>{children}</>;
}
```

Why: The component uses `any`, invents unsupported SDK initialization, and implies a secret can live in client code.

## Conventions

| Rule | Rationale |
|---|---|
| Keep generated connector services and models separate from custom source | PAC regeneration can overwrite generated files without damaging hand-written code |
| Use strict TypeScript with `verbatimModuleSyntax: false` | Code remains type-safe while staying compatible with the Power Apps SDK |
| Access Power Platform through generated services, typed hooks, and explicit consent flows | Connector calls remain testable and permission failures are handled |
| Prefer functional React components, clear props, loading states, and error boundaries | UI stays maintainable and user failures are visible |
| Store secrets outside client code and use HTTPS plus OWASP-aligned validation | Sensitive data and users are protected |
| Test utilities, components, connector flows, and deployment scripts | Code Apps combine web UI and platform integration, so both need coverage |
| Preserve documented platform limitations | Guidance does not promise unsupported Code Apps features |

## Do / Do Not

| Do | Do not |
|---|---|
| Use PAC CLI and generated services for connector operations | Hand-code connector clients that drift from generated models |
| Keep `generated/services/` and `generated/models/` isolated | Mix generated files with custom business logic |
| Set `verbatimModuleSyntax: false` and keep TypeScript strict | Disable type safety to work around SDK or connector errors |
| Use Power Platform authentication, consent, and DLP policies | Store tokens, secrets, or sensitive configuration in React code |
| Build with `npm run build` before `pac code push` | Push an app that has not compiled successfully |
| Mock connectors in tests and cover error states | Test only happy-path rendering |
| Document limitations such as missing CSP and Git integration | Claim unsupported platform features are available |

## Checklist Before Opening a PR

- [ ] Project structure keeps custom code separate from PAC-generated services and models.
- [ ] TypeScript configuration preserves strict mode and `verbatimModuleSyntax: false`.
- [ ] Power Platform connector access uses generated services, typed models, and explicit consent handling.
- [ ] React components expose loading, empty, error, and success states for connector operations.
- [ ] Secrets are absent from code and HTTPS, validation, authorization, and DLP expectations are respected.
- [ ] Accessibility, responsive behavior, theming, and localization requirements are implemented where applicable.
- [ ] Tests cover business logic, components, connector mocks, critical flows, and failure cases.
- [ ] Deployment uses `npm run build`, PAC CLI, environment-specific configuration, and rollback planning.
- [ ] Current Code Apps limitations and troubleshooting commands remain accurate.

## References

- Environment URL placeholder retained for configuration examples: https://<dev-environment>.crm.dynamics.com
