---
name: webmcpify
description: >-
  Make a web app agent-ready with WebMCP by detecting app actions, building a manifest, integrating document.modelContext tools, verifying in a real browser, healing failures, and auditing diffs. Use when the user says "webmcpify", "add WebMCP", "expose app actions to AI agents", or asks to make a browser app controllable through WebMCP tools.
argument-hint: "[inventory|integrate|verify|status|full] [scope notes]"
license: MIT
metadata:
  source: "https://github.com/TueJon/webmcpify"
---

# webmcpify

Take an existing web application, inventory user-facing actions, transform approved actions into WebMCP tools registered through `document.modelContext`, verify them through the production browser surface, and deliver `.webmcpify/manifest.json` plus `.webmcpify/report.md` without touching unrelated code.

## When to invoke

- "webmcpify this app."
- "Add WebMCP tools for our checkout flow."
- "Expose app actions to AI agents."
- "Verify the WebMCP manifest and heal failures."
- "Show WebMCP integration status."

## Inputs

Use `$ARGUMENTS` as the mode and scope. Accepted modes are `inventory`, `map`, `integrate`, `verify`, `status`, and `full`; any other text is scoping guidance such as `only the checkout area` or `read-only tools only`. If `$ARGUMENTS` is empty, run `full` and resume from the current `.webmcpify/manifest.json` when it exists.

## Prerequisites and context

- Target a web app you control; backend-only MCP servers, third-party-site automation, and SEO work are out of scope.
- Prefer live WebMCP guidance before integration when the network works:

```sh
npx -y modern-web-guidance@latest retrieve "webmcp,agentic-forms,agentic-javascript-tools"
```

- WebMCP is an evolving origin-trial API from the W3C Web Machine Learning Community Group: https://webmachinelearning.github.io/webmcp/
- If offline, use bundled references under `references/` and templates under `templates/`.

## Invocation modes

| Argument | Run | Stop at |
| --- | --- | --- |
| none or `full` | DETECT, INVENTORY, GATE, INTEGRATE, VERIFY, HEAL, AUDIT | `done` |
| `inventory` / `map` | DETECT and INVENTORY loops only; zero code changes | manifest table for review |
| `integrate` | INTEGRATE loop only; requires approved manifest tools | integrated and built |
| `verify` | VERIFY and HEAL loops on integrated tools | green or skipped report |
| `status` | read `.webmcpify/manifest.json`; read-only | phase, per-status counts, next command |

## Ground rules

| Rule | Requirement |
| --- | --- |
| Unrelated changes | Every diff hunk must trace to a manifest tool or recorded one-time setup path. Never refactor, reformat, rename, modify, or revert `baselineDirty` files. |
| Mutations | Prefer read-only tools. Use `mutating: false`, `mutating: "client"`, or `mutating: "server"`. Server-mutating tools require per-tool human approval in `approval`. |
| Trust boundary | `execute()` may only call UI-owned paths: same endpoints, validation, and auth. Never create endpoints, bypass checks, or put secrets in tools. |
| Runtime | Register via `document.modelContext.registerTool()` with AbortSignal lifecycle and feature-detect deprecated `navigator.modelContext`. No third-party WebMCP runtime dependencies. |
| Forms | Never use `toolautosubmit` on state-changing forms; use it only for pure read forms such as search, filter, or availability. |
| State | Persist progress in `.webmcpify/`; write `manifest.json.tmp` and rename over `manifest.json`. |
| Commits | Never commit unless the gate records `commitPolicy`. Never use `git add -A`, `git add -u`, `git add .`, or `commit -a`. |

## State protocol

`.webmcpify/manifest.json` is the single source of truth. Resume if it exists. Merge any `.webmcpify/areas/<id>.tools.json` shard first, mark the area `inventoried`, delete the shard, then continue from `pipeline.phase`, the first `pending` area, or the first non-terminal tool. Terminal statuses are `verified`, `skipped`, and `rejected`.

| File | Purpose |
| --- | --- |
| `.webmcpify/manifest.json` | Webmcpify Manifest v3, atomically written |
| `.webmcpify/areas/<id>.tools.json` | Sub-agent shard: `{ "webmcpifyShard": 3, "area": "<id>", "tools": [] }` |
| `.webmcpify/report.md` | Human-facing running and final report |

Keep these v3 fields and values intact: `webmcpify`, `app.stack`, `app.typescript`, `app.entry`, `app.baseUrl`, `app.startCommand`, `app.authFixtures`, `pipeline.phase`, `pipeline.setup.runtimeVendored`, `harnessInstalled`, `originTrialNoted`, `baselineSha`, `baselineDirty`, `commitPolicy`, `commitWebmcpifyDir`, `blockers`, `areas`, `tools`, `id`, `kind`, `mutating`, `priority`, `description`, `inputSchema`, `annotations`, `readOnlyHint`, `untrustedContentHint`, `source`, `route`, `auth`, `examples`, `valid`, `invalid`, `expect`, `result`, `navigation`, `ui`, `cleanup`, `status`, `approval`, `productionSideEffect`, `attempts`, `batchCommit`, `notes`, and `log`.

Use this canonical sample shape when creating or migrating state:

```jsonc
{
  "webmcpify": 3,
  "app": {
    "stack": "react-vite",
    "typescript": true,
    "entry": "src/main.tsx",
    "baseUrl": "http://localhost:5173",
    "startCommand": "npm run dev",
    "authFixtures": {
      "member": { "obtain": "npm run seed:test-user, then sign in at /login", "account": "member@example.test", "env": ["TEST_MEMBER_PASSWORD"] }
    }
  },
  "pipeline": {
    "phase": "inventory",
    "setup": {
      "runtimeVendored": ["src/webmcp/webmcpify.ts", "src/webmcp/webmcp.d.ts"],
      "harnessInstalled": [".webmcpify/webmcp.spec.ts"],
      "originTrialNoted": ["README.md"]
    },
    "baselineSha": "abc1234",
    "baselineDirty": ["src/wip.ts"],
    "commitPolicy": null,
    "commitWebmcpifyDir": null,
    "blockers": ["app won't start locally: needs API_KEY"]
  },
  "areas": [{ "id": "checkout", "paths": ["src/features/checkout/"], "status": "pending" }],
  "tools": [{
    "id": "create_ticket",
    "area": "tickets",
    "kind": "imperative",
    "mutating": "server",
    "priority": 1,
    "description": "Creates a new ticket in the currently open project.",
    "inputSchema": {},
    "annotations": { "readOnlyHint": false, "untrustedContentHint": false },
    "source": ["src/features/tickets/NewTicket.tsx:42"],
    "route": "/projects/demo/tickets",
    "auth": ["role:member"],
    "examples": { "valid": { "title": "Test ticket" }, "invalid": {} },
    "expect": { "result": "created", "navigation": null, "ui": "new row appears in the ticket list" },
    "cleanup": "delete the created ticket via the UI's own delete path (test data only)",
    "status": "discovered",
    "approval": null,
    "attempts": 0,
    "batchCommit": null,
    "notes": ""
  }],
  "log": ["2026-07-12 inventory: area checkout done, 4 candidates"]
}
```

Migrate `webmcpify: 2` manifests on first write: `auth` string to array; `setup` booleans to path arrays where `false` becomes `[]` and unrecoverable `true` becomes `null`; `mutating: true` to `"server"`; add `annotations`, `blockers: []`, `commitWebmcpifyDir: null`, and `expect.navigation: null`; then bump to `3`.

## Procedure

1. DETECT: identify stack, build and dev-server commands, TypeScript, test setup, auth model, `authFixtures`, `baseUrl`, `startCommand`, `baselineSha`, and `baselineDirty`. If the app cannot start locally, append a blocker.
2. INVENTORY: map routes, pages, views, or feature modules cheaply; create `areas` with `pending`; deep-read one area per iteration; fill each tool with `route`, `auth`, `annotations`, `examples`, `expect`, and `cleanup`; mark the area `inventoried`; run a completeness pass over visible user actions.
3. GATE: present id, area, kind, mutating, priority, and one-line description. Record approved or rejected tools, per-tool approval for `mutating: "server"`, `commitPolicy` as `commit-per-batch` or `no-commit`, `commitWebmcpifyDir`, and every blocker.
4. INTEGRATE: vendor `templates/webmcpify.ts` or `templates/webmcpify.js`, `templates/webmcp.d.ts`, and when needed `templates/webmcp-jsx.d.ts`; note origin trial or flag requirements; integrate one area or no more than five approved tools per batch; build and typecheck; set tools to `integrated`.
5. VERIFY: install `templates/webmcp.spec.ts`; use real headed Chrome and the production `getTools()` / `executeTool()` surface with legacy fallback; parse stringified JSON Schema; verify `annotations`, valid and invalid examples, returned result, UI delta, navigation, auth roles, and cleanup.
6. HEAL: fix only the failed tool integration. If schema, description, `mutating`, `annotations`, or `expect` changes, return to the gate. Increment `attempts`; at `attempts = 3`, mark `skipped`. Re-run all integrated or verified tools after healing.
7. AUDIT: collect `git diff <baselineSha>..HEAD`, index changes, and untracked files for `commit-per-batch`, or working tree, index, and untracked files for `no-commit`. Map every hunk to a tool or `pipeline.setup`; flag unmapped or `baselineDirty` hunks only. Finalize `.webmcpify/report.md`.

## Progressive disclosure and bundled resources

- `references/inventory.md`: area mapping, naming, schema conventions, tool-count budgets, and overlap rules.
- `references/security.md`: mutating-tool approval and audit checklist; apply before the gate and at audit.
- `references/runtime.md`: vendoring and wiring the runtime while preserving the full MIT header.
- `references/integrate.md`: declarative attributes for standard HTML forms and imperative registration for non-form or controlled-state actions.
- `references/verify.md`: flags, Chrome setup, WebMCP surfaces, Playwright/Puppeteer checks, and dual-outcome assertions for zero-param read tools.
- `references/heal.md`: failure taxonomy and implementation-only fixes.
- `templates/webmcpify.ts`, `templates/webmcpify.js`, `templates/webmcp.d.ts`, `templates/webmcp-jsx.d.ts`, `templates/webmcp.spec.ts`: vendorable runtime and verification assets.

## Gotchas

- **Manifest state beats memory**: read and write `.webmcpify/manifest.json` at every transition because context can be wiped.
- **Server-mutating verification can create real effects**: require `approval.productionSideEffect`, mark every payload `[webmcpify verification]`, and list the effect in `report.md`; otherwise mark `skipped`.
- **The manifest cannot contain its own commit SHA**: under `commit-per-batch`, write `batchCommit` on the next manifest write.
- **Inventory shards are not manifests**: sub-agents may write only `areas/<id>.tools.json`; the coordinator merges sequentially.

## Limits

- Do not use this skill for backend-only MCP servers, automating sites you do not control, destructive first-wave actions, irreversible payment actions, or generic SEO work.
- Do not expose a tool that bypasses the UI's existing authorization, validation, endpoint, or cleanup path.

## Source compatibility terms

Retain these WebMCP pipeline terms when reading older manifests or reports: ` paths (both `, `"client"`, `"discovered"`, `"failed"`, `"integrated"`, `"inventoried"`, `"pending"`, `"skipped"`, `"verified"`, `"webmcpify": 2`, `, or `, `/webmcpify <mode>`, `; commit `, `FIRST`, `HERE`, `HUMAN`, `LATER`, `NAMES`, `OBTAINS`, `ONLY`, `PATHS`, `Read/write`, `THREE`, `URL/pattern`, `allow-listed`, `approved`, `audit`, `audit → done`, `auto-revert`, `browser-local`, `budgets/overlap`, `client-mutating`, `created/modified`, `dependency-free`, `detect → inventory`, `dev/test`, `discovered`, `document`, `done-but-unrecorded`, `expect.navigation`, `failed`, `fan-out`, `feature-detected`, `fetch-intercepted`, `file/line`, `framework-rendered`, `gate → integrate`, `green/skipped`, `heal → audit`, `heal-fix`, `integrate → verify`, `integrated/verified`, `invalid: null`, `inventory → gate`, `mapped-or-flagged`, `naming/schema`, `navigator`, `no/empty`, `non-negotiable`, `opt-in`, `origin-trial/flag`, `per-area`, `pipeline.baselineDirty`, `pipeline.baselineSha`, `pipeline.blockers`, `pipeline.commitPolicy`, `pipeline.commitWebmcpifyDir`, `post-heal`, `re-approval`, `re-run`, `re-verify`, `review/commit`, `routes/views/feature`, `runtimeVendored: ["src/webmcp/webmcpify.ts", ...]`, `server-mutating`, `side-effect`, `skipped/rejected`, `tri-state`, `verify → heal`, `webmcp-jsx.d.ts`, `webmcp.d.ts`, `webmcpify.js`, `webmcpify.ts`, and `DevTools`.

## Output template

```markdown
## webmcpify report

**Status:** inventory | gate | integrated | verified | healed | skipped | done | blocked
**Mode:** inventory | integrate | verify | status | full
**Manifest:** `.webmcpify/manifest.json`

| Area | Tool | Kind | Mutating | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| `<area>` | `<tool_id>` | imperative | false | verified | `<route>`, schema, annotations, valid and invalid examples passed |

**Setup paths**
- `<path>`: runtimeVendored | harnessInstalled | originTrialNoted

**Security and blockers**
- `<mutating tool or blocker>`: `<approval, cleanup, skipped reason, or production side effect>`

**Audit**
- Mapped hunks: `<count>`
- Flagged hunks: `<file:line and disposition>`
- Validation: `<build/typecheck/browser verify command>` passed | failed
```

## Quality gate

- [ ] Mode from `$ARGUMENTS` is honored and unknown words are treated as scope.
- [ ] `.webmcpify/manifest.json` is written atomically and contains Webmcpify Manifest v3.
- [ ] Every absolute URL and environment variable name, including `API_KEY` and `TEST_MEMBER_PASSWORD`, is preserved without secret values.
- [ ] Every tool has `route`, `auth`, `inputSchema`, `annotations`, `examples`, `expect`, `cleanup`, `status`, and `source`.
- [ ] Server-mutating tools have explicit approval before integration or live verification.
- [ ] Verification uses the production `getTools()` and `executeTool()` browser surface.
- [ ] Every diff hunk maps to a manifest entry or `pipeline.setup`, or is flag-only in `.webmcpify/report.md`.
- [ ] Referenced files under `references/` and `templates/` exist and are read only on demand.

## References

- [WebMCP draft](https://webmachinelearning.github.io/webmcp/)
- [webmcpify source](https://github.com/TueJon/webmcpify)
