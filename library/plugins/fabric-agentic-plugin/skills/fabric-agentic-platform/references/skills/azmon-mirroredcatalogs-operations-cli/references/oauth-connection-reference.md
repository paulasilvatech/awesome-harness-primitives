# Mode B — OAuth connection reference

Loaded on demand from `skills/azmon-mirroredcatalogs-operations-cli/SKILL.md`
at Stage 5 when the user picks interactive sign-in (OAuth).

## Mode B — OAuth (UI-guided only, fallback)

Use this mode only when Service Principal (Mode A) is unavailable or the user
explicitly requests OAuth.

- OAuth connector **creation** is interactive, done once in **Fabric → Manage
  Connections**. The Skill does **not** create OAuth connectors through any API.
- The Skill **detects and reuses** an existing Azure Monitor OAuth connection for
  this workspace (read-only, non-destructive).
- Before classifying OAuth connection detection as "not verifiable", attempt the
  available Fabric REST **read-only** connection discovery paths, in order:
  1. A surfaced Fabric REST / Fabric Actions capability, if available.
  2. Authenticated Fabric REST read-only discovery via `az rest --method get`
     against `https://api.fabric.microsoft.com/...`, if Azure CLI execution is
     available and permitted under the read-only Fabric REST discovery exception
     (GET-only, no modifications, no secret/token/header exposure, capability
     path stated). This detection is read-only; OAuth connector **creation**
     remains UI-guided only.
- Reuse a connection ONLY if it belongs to the **same** Log Analytics workspace
  (exact data-source-path / LAW resource-id match). Any mismatch → treat as "no
  matching connection".
- If exactly one match → reuse automatically and continue.
- If multiple matches → show display names and ask the user to choose (never
  auto-pick).
- If no match → guide the user with this message as **normal chat text (not a
  code block)** and then WAIT:

  I couldn’t find an existing Azure Monitor connection for this workspace.
  Please create it once in Fabric → Manage Connections, then come back and
  continue:

  1. Open Fabric.
  2. Go to Manage Connections.
  3. Select New connection → Azure Monitor.
  4. Sign in with your organizational account.
  5. Use the same Log Analytics workspace.
  6. When done, come back here and type **Done**.

When the user resumes, re-detect and continue automatically ("Connection
detected. Continuing setup.").
