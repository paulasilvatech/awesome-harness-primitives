---
applyTo: "**/.joyride/**"
description: "Enforces Joyride workspace automation conventions for REPL-driven ClojureScript, VS Code API usage, workspace activation, data-oriented design, and safe file updates."
name: "Joyride Workspace Automation Conventions"
---

# Joyride Workspace Automation Conventions — REPL-Driven ClojureScript

These instructions apply to workspace-specific Joyride automation under `.joyride/`. They are authoritative for ClojureScript style, REPL-driven validation, workspace activation, VS Code API usage, data modeling, and safe update boundaries in matched files; explicit user requests and workspace-specific team conventions win when they require narrower automation behavior.

## Workspace Context and Ownership

Use Joyride for project-specific VS Code automation that belongs with the current workspace. Keep scripts team-shareable, version-controlled, version-controllable, and context-aware.

| Automation type | Convention |
| --- | --- |
| Project-specific scripts | Tailor behavior to the current workspace's technologies, folders, and workflows. |
| Team-shareable customization | Store code under `.joyride/` so the project can version it. |
| Context-aware commands | Read workspace folders, project configuration, and team conventions through VS Code APIs. |
| Activation-driven setup | Use `workspace_activate.cljs` for automatic project setup when the workspace opens. |

Do not treat Joyride files as global personal automation when they are stored in the repository.

## REPL-Driven Development

Develop Joyride automation interactively. The REPL is the primary validation mechanism, and `joyride_evaluate_code` is the main runtime tool for testing code in VS Code's Extension Host.

- Evaluate small expressions step by step before assembling larger functions.
- Show evaluated snippets in code blocks that start with `(in-ns ...)`.
- Verify VS Code API usage in the REPL before updating files.
- Prefer evaluating sub-expressions and subexpressions over adding `println` or `js/console.log` instrumentation; `println` use is HIGHLY discouraged.
- Update files only when the user asks for persistent changes.
- Provide tested, working solutions instead of theoretical suggestions.

## ClojureScript Style and Data Modeling

Write data-oriented, functional ClojureScript that is easy to inspect at the REPL.

| Concern | Convention |
| --- | --- |
| Function shape | Prefer functions that take arguments and return results. |
| Side effects | Use side effects only at the boundary needed to interact with VS Code or the workspace. |
| Arguments | Prefer destructuring and maps for function arguments. |
| Keywords | Prefer namespaced keywords such as `:project/type`, `:build/config`, and `:team/conventions`. |
| Data shape | Prefer flatness over deeply nested structures. |
| Synthetic namespaces | Use keys such as `:workspace/folders`, `:project/scripts`, and other workspace-related synthetic namespaces to group workspace data. |

Build solutions step by small step so each expression can be verified independently.

## VS Code Runtime Boundaries

Joyride runs SCI ClojureScript in VS Code's Extension Host with access to the VS Code API and workspace context. Keep automation safe by reading the workspace state before writing, validating assumptions in the REPL, and limiting persistent changes to `.joyride/` or files explicitly requested by the user.

## Good / Bad Examples

The examples below illustrate REPL-first, data-oriented workspace inspection.

**Good:**

```clojure
(in-ns 'my-workspace.automation)

(defn workspace-summary [{:keys [vscode]}]
  {:workspace/folders (mapv #(.name %) (.-workspaceFolders (.-workspace vscode)))
   :project/type :clojure})
```

Why: The snippet starts with `(in-ns ...)`, returns data, uses namespaced keywords, and keeps VS Code interaction at a clear boundary.

**Bad:**

```clojure
(defn setup []
  (println "starting")
  (js/console.log js/process)
  (spit "settings.json" "{}"))
```

Why: The snippet lacks a namespace, relies on print debugging, reaches for globals without REPL verification, and writes a file without an explicit user request.

## Conventions

| Rule | Rationale |
| --- | --- |
| Keep Joyride automation under `.joyride/` workspace scope | The automation stays project-specific and team-shareable. |
| Use `workspace_activate.cljs` for automatic project setup | Activation behavior is discoverable and tied to the workspace. |
| Validate code with `joyride_evaluate_code` before persisting changes | VS Code API assumptions are tested in the real Extension Host. |
| Start REPL snippets with `(in-ns ...)` | Evaluations happen in the intended namespace. |
| Prefer data-oriented pure functions | Small expressions are easier to evaluate, compose, and debug. |
| Prefer destructuring, maps, namespaced keywords, and flat data | Workspace data remains explicit and inspectable. |
| Avoid `println` and `js/console.log` for routine development | REPL evaluation gives more precise feedback with less noise. |
| Update files only when requested | Workspace automation does not create unwanted persistent changes. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Evaluate small expressions with `joyride_evaluate_code` | Write a full script before testing any API call. |
| Use `(in-ns 'workspace.namespace)` in examples | Evaluate anonymous snippets with unclear namespace state. |
| Return maps with keys like `:workspace/folders` | Hide workspace facts in logs or deeply nested structures. |
| Use side effects at VS Code boundaries | Mix side effects throughout data transformation code. |
| Read workspace configuration before acting | Assume every workspace has the same folders or tools. |
| Persist changes only on explicit request | Modify files as part of exploratory REPL work. |

## Checklist Before Opening a PR

- [ ] Joyride automation remains under `.joyride/` and is workspace-specific.
- [ ] Activation behavior belongs in `workspace_activate.cljs` when automatic setup is needed.
- [ ] VS Code API usage was verified with `joyride_evaluate_code` before file changes.
- [ ] REPL examples start with `(in-ns ...)`.
- [ ] Functions are data-oriented and prefer arguments plus return values over side effects.
- [ ] Maps, destructuring, namespaced keywords, and flat data shapes are used where they clarify workspace data.
- [ ] `println` and `js/console.log` are not used for routine validation.
- [ ] Persistent file updates were explicitly requested and are limited to the requested scope.
