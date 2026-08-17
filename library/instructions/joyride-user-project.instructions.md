---
applyTo: "**/*.{cljs,cljc,edn}"
description: "Enforces Joyride user script conventions for SCI ClojureScript, REPL-driven VS Code automation, async evaluation, flares, disposables, and file edits."
---

# Joyride User Project Conventions — REPL-Driven VS Code Automation

These instructions apply to files matched by `**/*.{cljs,cljc,edn}`. They are authoritative for joyride user project code, configuration, examples, validation commands, API names, and runtime constraints in those files; stricter repository-specific security, deployment, testing, or platform primitives win on conflict. Treat the rules as passive conventions injected into matching files, not as a step-by-step workflow.

Use Joyride as a REPL-driven ClojureScript environment for VS Code automation in user space. Joyride runs SCI ClojureScript in VS Code's Extension Host with full access to the VS Code API. Prefer Joyride evaluation to validate code directly in the VS Code runtime; use the REPL as the primary feedback loop for tested behavior.

## Essential Information Sources

For comprehensive, up-to-date Joyride information, use the `fetch_webpage` tool to access these guides:

- **Joyride agent guide**: https://raw.githubusercontent.com/BetterThanTomorrow/joyride/master/assets/llm-contexts/agent-joyride-eval.md
  - Technical guide for LLM agents using Joyride evaluation capabilities
- **Joyride user guide**: https://raw.githubusercontent.com/BetterThanTomorrow/joyride/master/assets/llm-contexts/user-assistance.md
  - Complete user assistance guide with project structure, patterns, examples, and troubleshooting

These guides contain all the detailed information about Joyride APIs, project structure, common patterns, user workflows, and troubleshooting guidance.

## Core Philosophy: Interactive Programming (aka REPL-Driven Development)

Please start by examining `README.md` and the code in the `scripts` and `src` folders of the project.

Only update files when the user asks you to. Prefer using the REPL to evaluate features into existence.

You develop the Clojure Way, data oriented, and building up solutions step by small step.

You use code blocks that start with `(in-ns ...)` to show what you evaluate in the Joyride REPL.

The code will be data-oriented, functional code where functions take args and return results. This will be preferred over side effects. But we can use side effects as a last resort to service the larger goal.

Prefer destructuring, and maps for function arguments.

Prefer namespaced keywords. Consider using "synthetic" namespaces, like `:foo/something` to group things.

Prefer flatness over depth when modeling data.

When presented with a problem statement, you work through the problem iteratively step by step with the user.

Each step you evaluate an expression to verify that it does what you think it will do.

The expressions you evaluate do not have to be a complete function, they often are small and simple sub-expressions, the building blocks of functions.

`println` (and things like `js/console.log`) use is HIGHLY discouraged. Prefer evaluating subexpressions to test them vs using println.

The main thing is to work step by step to incrementally develop a solution to a problem. This will help me see the solution you are developing and allow the user to guide its development.

Always verify API usage in the REPL before updating files.

## AI Hacking VS Code in user space with Joyride, using Interactive Programming

When demonstrating what you can do with Joyride, remember to show your results in a visual way. E.g. if you count or summarize something, consider showing an information message with the result. Or consider creating a markdown file and show it in preview mode. Or, fancier still, create and open a web view that you can interact with through the Joyride REPL.

When demonstrating that you can create disposable items that stay in the UI, such as statusbar buttons, make sure to hold on to a reference to the object so that you can modify it and dispose of it.

Use the VS Code API via the correct interop syntax: vscode/api.method for functions and members, and plain JS objects instead of instantiating (e.g., `#js {:role "user" :content "..."}`).

Whenever in doubt, check with the user, the REPL and the docs, and iterate interactively together with the user!

## Essential APIs and Patterns

To load namespaces/files into the REPL, instead of `load-file` (which isn't implemented) use the Joyride (async) version: `joyride.core/load-file`.

### Namespace Targeting is Critical

When using the **Joyride evaluation** tool, always specify the correct namespace parameter. Functions defined without proper namespace targeting may end up in the wrong namespace (like `user` instead of your intended namespace), making them unavailable where expected.

### VS Code API Access
```clojure
(require '["vscode" :as vscode])

;; Common patterns users need
(vscode/window.showInformationMessage "Hello!")
(vscode/commands.executeCommand "workbench.action.files.save")
(vscode/window.showQuickPick #js ["Option 1" "Option 2"])
```

### Joyride Core API
```clojure
(require '[joyride.core :as joyride])

;; Key functions users should know:
joyride/*file*                    ; Current file path
(joyride/invoked-script)          ; Script being run (nil in REPL)
(joyride/extension-context)       ; VS Code extension context
(joyride/output-channel)          ; Joyride's output channel
joyride/user-joyride-dir          ; User joyride directory path
joyride/slurp                     ; Similar to Clojure `slurp`, but is async. Accepts absolute or relative (to the workspace) path. Returns a promise
joyride/load-file                 ; Similar to Clojure `load-file`, but is async.  Accepts absolute or relative (to the workspace) path. Returns a promise
```

### Async Operation Handling
The evaluation tool has an `awaitResult` parameter for handling async operations:

- **`awaitResult: false` (default)**: Returns immediately, suitable for synchronous operations or fire-and-forget async evaluations
- **`awaitResult: true`**: Waits for async operations to complete before returning results, returns the resolved value of the promise

**When to use `awaitResult: true`:**
- User input dialogs where you need the response (`showInputBox`, `showQuickPick`)
- File operations where you need the results (`findFiles`, `readFile`)
- Extension API calls that return promises
- Information messages with buttons where you need to know which was clicked

**When to use `awaitResult: false` (default):**
- Synchronous operations
- Fire-and-forget async operations like simple information messages
- Side-effect async operations where you don't need the return value

### Promise Handling
```clojure
(require '[promesa.core :as p])

;; Users need to understand async operations
(p/let [result (vscode/window.showInputBox #js {:prompt "Enter value:"})]
  (when result
    (vscode/window.showInformationMessage (str "You entered: " result))))

;; Pattern for unwrapping async results in REPL (use awaitResult: true)
(p/let [files (vscode/workspace.findFiles "**/*.cljs")]
  (def found-files files))
;; Now `found-files` is defined in the namespace for later use

;; Yet another example with `joyride.core/slurp` (use awaitResult: true)
(p/let [content (joyride.core/slurp "some/file/in/the/workspace.csv")]
  (def content content) ; if you want to use/inspect `content` later in the session
  ; Do something with the content
  )
```

### Extension APIs
```clojure
;; How to access other extensions safely
(when-let [ext (vscode/extensions.getExtension "ms-python.python")]
  (when (.-isActive ext)
    (let [python-api (.-exports ext)]
      ;; Use Python extension API safely
      (-> python-api .-environments .-known count))))

;; Always check if extension is available first
(defn get-python-info []
  (if-let [ext (vscode/extensions.getExtension "ms-python.python")]
    (if (.-isActive ext)
      {:available true
       :env-count (-> ext .-exports .-environments .-known count)}
      {:available false :reason "Extension not active"})
    {:available false :reason "Extension not installed"}))
```

## Joyride Flares - WebView Creation

Joyride Flares provide a convenient way to create WebView panels and sidebar views.

### Basic Usage
```clojure
(require '[joyride.flare :as flare])

;; Create a flare with Hiccup
(flare/flare!+ {:html [:h1 "Hello World!"]
                :title "My Flare"
                :key "example"})

;; Create sidebar flare (slots 1-5 available)
(flare/flare!+ {:html [:div [:h2 "Sidebar"] [:p "Content"]]
                :key :sidebar-1})

;; Load from file (HTML or EDN with Hiccup)
(flare/flare!+ {:file "assets/my-view.html"
                :key "my-view"})

;; Display external URL
(flare/flare!+ {:url "https://example.com"
                :title "External Site"})
```

**Note**: `flare!+` returns a promise, use `awaitResult: true`.

### Key Points
- **Hiccup styles**: Use maps for `:style` attributes: `{:color :red :margin "10px"}`
- **File paths**: Absolute, relative (requires workspace), or Uri objects
- **Management**: `(flare/close! key)`, `(flare/ls)`, `(flare/close-all!)`
- **Bidirectional messaging**: Use `:message-handler` and `post-message!+`

**Full documentation**: [API docs](https://github.com/BetterThanTomorrow/joyride/blob/master/doc/api.md#joyrideflare)

**Comprehensive examples**: [flares_examples.cljs](https://github.com/BetterThanTomorrow/joyride/blob/master/examples/.joyride/src/flares_examples.cljs)

## Common User Patterns

### Script Execution Guard
```clojure
;; Essential pattern - only run when invoked as script, not when loaded in REPL
(when (= (joyride/invoked-script) joyride/*file*)
  (main))
```

### Managing Disposables
```clojure
;; Always register disposables with extension context
(let [disposable (vscode/workspace.onDidOpenTextDocument handler)]
  (.push (.-subscriptions (joyride/extension-context)) disposable))
```

## Editing files

Develop using the REPL. Yet, sometimes you need to edit file. And when you do, prefer structural editing tools.

## Good / Bad Examples

The examples below show the boundary between an acceptable convention and the closest common anti-pattern.

**Good:**

```clojure
(in-ns 'my.joyride.script)
(require '[promesa.core :as p] '[joyride.core :as joyride] '["vscode" :as vscode])
(p/let [choice (vscode/window.showQuickPick #js ["A" "B"])]
  (when choice (vscode/window.showInformationMessage (str "Selected " choice))))
```

Why: The evaluation targets a namespace, uses Promesa, and uses VS Code APIs asynchronously.

**Bad:**

```clojure
(println "Pick something")
(load-file "script.cljs")
```

Why: The code relies on console output and unsupported `load-file`.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use Joyride evaluation and namespace-targeted `(in-ns ...)` blocks. | The REPL verifies behavior in VS Code. |
| Use `joyride.core/load-file` and `joyride.core/slurp`. | Joyride file APIs are async and workspace-aware. |
| Register disposables with `(joyride/extension-context)`. | VS Code automation must clean up resources. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use Joyride evaluation and namespace-targeted `(in-ns ...)` blocks. | Do not ignore this rule: Use Joyride evaluation and namespace-targeted `(in-ns ...)` blocks. |
| Use `joyride.core/load-file` and `joyride.core/slurp`. | Do not ignore this rule: Use `joyride.core/load-file` and `joyride.core/slurp`. |
| Register disposables with `(joyride/extension-context)`. | Do not ignore this rule: Register disposables with `(joyride/extension-context)`. |

## Checklist Before Opening a PR

- [ ] The change stays inside the matched `applyTo` scope.
- [ ] The authoritative conventions above are applied to new or modified code.
- [ ] Named commands, paths, API names, configuration keys, and version constraints remain intact.
- [ ] Relevant validation, linting, build, or test commands from this instruction pass.
- [ ] No secrets, unsupported APIs, placeholder prompt references, or relative primitive links were added.

## References

- https://example.com
- https://github.com/BetterThanTomorrow/joyride/blob/master/doc/api.md#joyrideflare
- https://github.com/BetterThanTomorrow/joyride/blob/master/examples/.joyride/src/flares_examples.cljs
- https://raw.githubusercontent.com/BetterThanTomorrow/joyride/master/assets/llm-contexts/agent-joyride-eval.md

- https://raw.githubusercontent.com/BetterThanTomorrow/joyride/master/assets/llm-contexts/user-assistance.md

