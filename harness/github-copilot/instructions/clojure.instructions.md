---
applyTo: '**/*.{clj,cljs,cljc,bb,edn.mdx?}'
description: 'Enforces Clojure and ClojureScript conventions for Calva REPL-first development, structural editing, namespace handling, data shape, rich comment forms, and tests.'
---

# Clojure Conventions — REPL-First Development

These instructions apply to Clojure, ClojureScript, Babashka, and related EDN documentation files matched by the `applyTo` globs. They are authoritative for REPL usage, Calva Backseat Driver evaluation, structural editing, namespace reloading, indentation, inline `def`, data shapes, rich comment forms, and Clojure tests in those files; project-specific architecture, build, and security instructions win when they set stricter boundaries.

## Calva REPL and Evaluation Discipline

When guidance says to use the REPL, use the Evaluate Clojure Code tool from Calva Backseat Driver. It connects to the same REPL as the user through Calva, so stay inside that REPL instead of launching another REPL from the terminal. If there is no REPL connection, stop and tell the user to connect the REPL; do not start and connect it yourself.

Do not edit Clojure files when the REPL is unavailable. If REPL evaluation reports that the REPL is unavailable, stop immediately and let the user restore it because interactive programming requires verified evaluation and guessing creates bugs.

Do not over-escape JSON arguments for REPL tool calls. Use the current namespace, the correct `replSessionKey` such as `cljs`, and raw Clojure code strings like `(def foo "something something")`.

## Structural Editing and Namespace Handling

Develop changes in the REPL before touching files. When editing files, use structural editing tools such as Insert Top Level Form, Replace Top Level Form, Create Clojure File, and Append Code, and read each tool's instructions before using it.

Create new Clojure files with the Create Clojure File tool and initial content. Use kebab-case namespaces and matching snake_case file paths: `my.project.ns` maps to `my/project/ns.clj`. After editing a file, reload the namespace with `(require 'my.namespace :reload)` so the active REPL has the updated definitions.

Define functions before they are used. Prefer ordering over `declare`; use `declare` only when mutually recursive or unavoidable references require it.

## Forms, Indentation, and Docstrings

Docstrings belong immediately after the function name and before the argument vector.

```clojure
(defn my-function
  "This function does something."
  [arg1 arg2]
  (+ arg1 arg2))
```

Align multi-line elements vertically in vectors, maps, lists, sets, and all Clojure code-as-data. The bracket balancer relies on consistent indentation to close forms correctly. Keep conditions and bodies on separate lines, and place `and` and `or` arguments on separate aligned lines.

```clojure
(when limit
  (println "Limit set to:" limit))

(if (and condition-a
         condition-b)
  this
  that)

(select-keys m [:key-a
                :key-b
                :key-c])

{:name "Alice"
 :age 30
 :city "Oslo"}
```

## REPL Dependencies, Inline Definitions, and Return Values

Use `clojure.repl.deps/add-libs` for dynamic dependency loading during REPL sessions when using Clojure 1.12 or later. Check `*clojure-version*` before relying on it.

```clojure
(require '[clojure.repl.deps :refer [add-libs]])
(add-libs '{dk.ative/docjure {:mvn/version "1.15.0"}})
*clojure-version*
```

Prefer inline `def` debugging over `println` or `console.log` when exploring in the REPL. Inline definitions keep intermediate values inspectable and may stay in place when they continue to aid exploration. Prefer return values from evaluations over print side effects because the user does not see what you evaluate or its result unless you report it in chat.

Avoid `(read-line)` in Babashka nREPL because it lacks stdin support. If `(read-line)` blocks a REPL, ask the user to restart it.

## Data Shapes and Function Boundaries

Keep data structures as flat as practical, lean on namespaced keywords, and prefer synthetic namespaces where they make destructuring explicit. Destructure keys directly in parameter lists so function signatures reveal the data contract.

```clojure
(defn handle-user-request
  [{:user/keys [id name email]
    :request/keys [method path headers]
    :config/keys [timeout debug?]}]
  (when debug?
    (println "Processing" method path "for" name)))
```

Avoid shadowing Clojure core symbols. Rename incoming keys when needed, as with `file-name :prompt-sync.file/name` and `file-type :prompt-sync.file/type`. Keep common symbols free: `class`, `count`, `empty?`, `filter`, `first`, `get`, `key`, `keyword`, `map`, `merge`, `name`, `reduce`, `rest`, `set`, `str`, `symbol`, `type`, and `update`.

Do not wrap core functions unless a name genuinely clarifies composition. `(remove (set exclusions) items)` is clearer than a wrapper that only renames `remove`.

## Rich Comment Forms

Use Rich Comment Forms `(comment ...)`, or RCFs, in files to document usage patterns and examples after you have validated the behavior in the REPL. RCF code is not evaluated when files load, so humans can evaluate examples on demand.

```clojure
(defn process-user-data
  "Processes user data with validation"
  [{:user/keys [name email] :as user-data}]
  user-data)

(comment
  (process-user-data {:user/name "John" :user/email "john@example.com"})
  (process-user-data {:user/name "Jane"})
  (->> users
       (map process-user-data)
       (filter :valid?))
  :rcf)
```

Use direct REPL evaluation in chat examples, for example `(in-ns 'my.namespace)` followed by a `let`; use RCFs in source files to preserve validated examples.

## Testing

Run focused tests from the REPL for immediate feedback. Reload the target namespace and execute tests with `clojure.test/run-tests` or `cljs.test/run-tests`; prefer individual test vars from inside the test namespace when investigating failures.

```clojure
(require '[my.project.some-test] :reload)
(clojure.test/run-tests 'my.project.some-test)
(cljs.test/run-tests 'my.project.some-test)
```

Use a REPL-first TDD workflow: iterate with real data, capture known-good behavior, then commit tests. Keep `deftest` names descriptive in area/thing style without redundant `-test` suffixes. Attach expectation messages directly to `is`; use `testing` blocks only when grouping multiple related assertions.


## Preserved REPL Examples and Names

Keep these identifiers available in examples or prose because they carry testing, formatting, and data-shape conventions from the original guidance.

| Vocabulary | Convention |
| --- | --- |
| `current-namespace` | Use it as the placeholder namespace in REPL tool JSON examples. |
| `process-instructions` and `group-by` | Keep them as examples of inline `def` exploration around grouped instruction data. |
| `create-item`, `prompt-sync.file/keys`, `prompt-sync.file/name`, `prompt-sync.file/type` | Use them to demonstrate renaming destructured keys that would otherwise shadow core names such as `name` and `type`. |
| `sample-text`, `format-line-number`, `editor-util/format-line-number`, `line-number-formatting`, `marker-len`, `num-str`, and `total-padding` | Preserve them in line-number formatting examples and tests. |
| `context-line-extraction`, `editor-util/get-context-lines`, `get-context-lines`, `str/split-lines`, `str/includes`, and `split-lines` | Preserve them in context extraction tests that group related assertions with `testing`. |
| `test-data` | Use it in direct REPL examples where a `let` binds representative input. |
| `stdin` | Avoid stdin reads in Babashka nREPL; `(read-line)` can block because stdin is unsupported. |
| `println/console.log.` | Prefer inline `def` over println/console.log. debugging; remove the trailing period when using the exact function names in code. |

## Good / Bad Examples

The examples below illustrate aligned data, direct destructuring, and assertion messages.

**Good:**

```clojure
(deftest line-marker-formatting
  (is (= "→" (editor-util/format-line-marker true))
      "Target line gets marker")
  (is (= "" (editor-util/format-line-marker false))
      "Non-target gets empty string"))
```

Why: The test name is descriptive, each expectation message is attached to `is`, and the form is easy to evaluate in the REPL.

**Bad:**

```clojure
(deftest line-marker-formatting-test
(testing "markers"
(is (= "→" (editor-util/format-line-marker true)))))
```

Why: The redundant suffix, missing indentation, and unnecessary `testing` wrapper make REPL evaluation and bracket balancing harder.

## Conventions

| Rule | Rationale |
|---|---|
| Use the Calva Backseat Driver Evaluate Clojure Code tool for REPL work | It shares the user's active REPL and avoids split runtime state |
| Stop instead of editing when the REPL is unavailable | Clojure changes need immediate evaluation to avoid guesswork |
| Use structural editing tools for file changes | Top-level forms remain balanced and namespace-aware |
| Place docstrings after function names and before argument vectors | `defn` metadata stays idiomatic and tooling-friendly |
| Align multi-line vectors, maps, lists, sets, `and`, and `or` forms | The bracket balancer can close forms correctly |
| Use `clojure.repl.deps/add-libs` only with Clojure 1.12 or later | Dynamic dependency loading depends on that runtime capability |
| Prefer inline `def` and return values over print side effects during exploration | Intermediate values stay inspectable in the REPL |
| Keep data flat with namespaced keywords and direct destructuring | Function contracts stay transparent and easy to refactor |
| Avoid shadowing core symbols and unnecessary wrapper functions | Code remains composable and predictable |
| Use RCFs for validated examples and REPL-run tests for fast feedback | Documentation and tests reflect behavior already exercised interactively |

## Do / Do Not

| Do | Do not |
|---|---|
| Use Calva's shared REPL and report evaluated findings in chat | Launch a second terminal REPL or hide important evaluation results |
| Ask the user to connect or restart the REPL when it is unavailable or blocked | Continue editing Clojure code without evaluation |
| Reload edited namespaces with `(require 'my.namespace :reload)` | Assume file edits are active in the REPL |
| Use kebab-case namespaces and matching snake_case paths | Create namespace and file names that cannot map cleanly |
| Use inline `def` for inspectable REPL debugging | Scatter `println` or `console.log` debugging through committed code |
| Use namespaced keys like `:user/name` and direct destructuring | Pass deeply nested maps where flat namespaced data would work |
| Rename keys that would shadow `name`, `type`, `map`, or `update` | Bind core function names as locals without need |
| Add RCF examples after REPL validation | Treat RCFs as a substitute for evaluating code first |
| Put expectation messages directly on `is` forms | Use broad `testing` blocks for single assertions |

## Checklist Before Opening a PR

- [ ] Clojure changes were developed and verified in the active Calva REPL.
- [ ] No Clojure file was edited while the REPL was unavailable.
- [ ] Structural editing tools were used for top-level form edits and new files.
- [ ] Namespaces use kebab-case and file paths use matching snake_case.
- [ ] Edited namespaces were reloaded with `(require 'my.namespace :reload)`.
- [ ] Multi-line forms, maps, vectors, `and`, and `or` expressions are aligned for bracket balancing.
- [ ] Docstrings appear immediately after `defn` names and before argument vectors.
- [ ] Inline `def` usage is intentional and useful for REPL exploration.
- [ ] Data shapes use flat namespaced keywords and avoid shadowing core symbols.
- [ ] RCF examples document behavior already validated in the REPL.
- [ ] Tests were run with `clojure.test/run-tests`, `cljs.test/run-tests`, or focused REPL evaluation.
