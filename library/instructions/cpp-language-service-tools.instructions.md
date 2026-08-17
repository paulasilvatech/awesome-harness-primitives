---
applyTo: '**/*.cpp,**/*.h,**/*.hpp,**/*.cc,**/*.cxx,**/*.c'
description: 'Enforces C and C++ language-service tool usage for symbol definitions, references, call hierarchy, parameters, line numbers, fallback search, and recovery.'
---

# C++ Language Service Conventions — Symbol Tools First

These instructions apply to C and C++ source and header files matched by the `applyTo` globs. They are authoritative for choosing C++ language service tools, resolving symbols, finding references, analyzing call hierarchy, supplying parameters, recovering from tool errors, and deciding when manual or text search is acceptable; repository-specific build, formatting, and architecture instructions win for compilation and design rules outside symbol analysis.

## Tool Responsibilities

Use the specialized C++ tools as the primary interface to C and C++ code understanding.

| Tool | Owns | Use when |
| --- | --- | --- |
| `GetSymbolInfo_CppTools` | Symbol definitions and type information | You need to find where a symbol is defined or understand an unfamiliar type, function, method, class, variable, or member |
| `GetSymbolReferences_CppTools` | All references to a symbol | You need all usages, uses, references, usage patterns, refactoring impact, or affected sites |
| `GetSymbolCallHierarchy_CppTools` | Function call relationships | You change a function signature, analyze callers with `callsFrom=false`, or inspect outgoing calls with `callsFrom=true` |

Prefer language-service results over `vscode_listCodeUsages`, `grep_search`, `read_file`, semantic search, or manual inspection for C++ symbols because IntelliSense understands overloaded functions, template instantiations, qualified and unqualified names, member calls, inherited members, and preprocessor conditionals for the active configuration.

## Mandatory Symbol Workflows

For symbol usage searches, call `GetSymbolReferences_CppTools` by default. Fall back to text search only when the tool is unavailable, fails, or appears incomplete.

For function signature changes, call `GetSymbolInfo_CppTools` to locate the definition, then call `GetSymbolCallHierarchy_CppTools` with `callsFrom=false` to find all callers, then call `GetSymbolReferences_CppTools` to catch additional references such as function pointers. Only after that update the function definition and all call sites.

For unfamiliar code, call `GetSymbolInfo_CppTools` on key types or functions, call `GetSymbolCallHierarchy_CppTools` with `callsFrom=true` to understand what a function calls, and call it with `callsFrom=false` to understand where the function is used. Read implementation details only after the tools identify the relevant code.

## Parameters and Resolution Strategy

Start with minimal information and add context only when needed.

| Parameter | Convention |
| --- | --- |
| Symbol name | Always provide a non-empty symbol name; it may be unqualified like `MyFunction`, partially qualified like `MyClass::MyMethod`, or fully qualified like `MyNamespace::MyClass::MyMethod` |
| File path | Strongly prefer absolute file paths when available, such as `C:\Users\Project\src\main.cpp`; avoid relative paths like `src\main.cpp` when the absolute path is known |
| Line number | Use 1-based line numbers only, never 0-based numbers |

Resolution order: try symbol name only; if ambiguous, add file path; if still ambiguous, add file path and exact line number. When a line number is needed, first use file reading to locate the symbol, note the exact line number from the output, verify that the line contains the symbol, and only then call the C++ tool.

## Error Handling and Recovery

Follow tool error messages exactly.

| Message | Meaning | Recovery |
| --- | --- | --- |
| `The symbol name is not valid: it is either empty or null. Find a valid symbol name. Then call the [tool] tool again` | The symbol parameter is missing or blank | Provide a non-empty, correctly spelled symbol name and retry |
| `A file could not be found at the specified path. Compute the absolute path to the file. Then call the [tool] tool again.` | The file path cannot be resolved | Convert the path to an absolute path, verify that the file exists in the workspace, and retry |
| `No results found for the symbol '[symbol_name]'.` | The symbol was found but has no references, calls, or hierarchy results for that query | Treat the empty result as valid information and report it instead of inventing usages |

Do not ignore an error, guess a different line, or proceed with a refactor when the recovery instructions have not been followed.

## Fallbacks and Integration with Other Tools

Use `read_file` only to find exact line numbers before calling C++ tools or to read implementation details after a symbol is located. Do not use `read_file` to find symbol usages.

Use `vscode_listCodeUsages` or `grep_search` for string literals, comments, non-C++ files, and configuration patterns. Do not use them for C++ symbol usages unless `GetSymbolReferences_CppTools` is unavailable, fails, or appears incomplete.

Use semantic search for conceptual discovery and project structure, then switch to the C++ tools for precise symbol analysis. Do not batch multiple unrelated symbol operations; analyze independent symbols in parallel only when each operation has a clear target.


## Preserved Tool Vocabulary

Keep exact tool vocabulary where it maps to mandatory behavior or legacy tool names.

| Vocabulary | Convention |
| --- | --- |
| `ALWAYS`, `NEVER`, `MANDATORY`, `CRITICAL`, `REQUIRED`, `STRONGLY`, `PREFERRED`, `ONLY`, `EXACT`, `VERIFY`, `CORRECT`, `INCORRECT`, and `WORKFLOW` | Use these labels only when preserving hard constraints, examples, and recovery wording from tool guidance. |
| `Adding/removing` | Treat adding/removing function parameters as a signature change that requires incoming call hierarchy. |
| `references/usages/uses`, `used/called/referenced`, `references/calls`, and `references/calls/hierarchy` | Keep these phrases tied to the decision of references versus call hierarchy. |
| `text-based` | Use this term for grep-style fallback tools that do not understand C++ symbols. |
| `types/functions` | Use symbol info before assuming the meaning of unfamiliar types/functions. |
| `user-specified` | Preserve user-specified file paths exactly, then convert to absolute paths when tools require them. |
| `semantic_search` and `vscode_listCodeUsages/grep_search` | Name these as fallback or discovery tools, never as the default symbol engine. |
| `call_hierarchy` | Keep this legacy token when explaining that the call hierarchy tool is mandatory before signature edits. |

## Good / Bad Examples

The examples below illustrate the required workflow for a function signature change.

**Good:**

```text
User asks: Add bool verbose to LogMessage.
1. Call GetSymbolInfo_CppTools for LogMessage.
2. Call GetSymbolCallHierarchy_CppTools for LogMessage with callsFrom=false.
3. Call GetSymbolReferences_CppTools for LogMessage.
4. Update the definition and every caller or reference.
```

Why: The workflow locates the definition, callers, and non-call references before code changes, so overloads and function pointer uses are not missed.

**Bad:**

```text
Use grep_search for LogMessage, edit the visible definition, and update only the matches in the current file.
```

Why: Text search can miss overloads, templates, inherited calls, preprocessor-specific code, and call sites outside the visible file.

## Conventions

| Rule | Rationale |
|---|---|
| Use `GetSymbolReferences_CppTools` for C/C++ symbol usages | IntelliSense distinguishes real symbol references from textual coincidences |
| Use `GetSymbolCallHierarchy_CppTools` with `callsFrom=false` before function signature changes | Every caller must be updated to preserve build correctness |
| Use `GetSymbolCallHierarchy_CppTools` with `callsFrom=true` when analyzing outgoing dependencies | Call hierarchy reveals behavior that a local body read can miss |
| Use `GetSymbolInfo_CppTools` before working with unfamiliar symbols | Definitions and type information prevent incorrect assumptions |
| Provide absolute file paths when available | Tool resolution is faster and less ambiguous |
| Use only verified 1-based line numbers | Guessed or 0-based line numbers can bind to the wrong symbol |
| Follow recovery instructions in tool error messages exactly | The tools provide the safest retry path |
| Treat `No results found` as valid information | Empty reference or call sets can be the correct answer |
| Use text search only for non-symbol patterns or as a fallback | Grep-style tools do not understand C++ semantics |

## Do / Do Not

| Do | Do not |
|---|---|
| Think `GetSymbolReferences_CppTools` for usages, `GetSymbolCallHierarchy_CppTools` for calls, and `GetSymbolInfo_CppTools` for definitions | Start with manual inspection for symbol-related tasks |
| Use `callsFrom=false` to find callers and `callsFrom=true` to find callees | Reverse call hierarchy direction or omit it before signature changes |
| Start with a symbol name, then add file path and line number only when needed | Guess line numbers or over-specify ambiguous context |
| Use `C:\Users\Project\src\main.cpp`-style absolute paths when available | Rely on `src\main.cpp` when the absolute path is known |
| Verify a line contains the symbol before passing its 1-based line number | Use 0-based line numbers or estimates |
| Follow exact recovery instructions for invalid symbol names and missing files | Ignore tool errors and continue editing |
| Use semantic search for broad concepts, then C++ tools for precise symbols | Use `grep_search` or `vscode_listCodeUsages` as the default symbol engine |

## Checklist Before Opening a PR

- [ ] Every C/C++ symbol usage search used `GetSymbolReferences_CppTools` or has a documented fallback reason.
- [ ] Every function signature change used `GetSymbolInfo_CppTools`, incoming `GetSymbolCallHierarchy_CppTools` with `callsFrom=false`, and `GetSymbolReferences_CppTools` before edits.
- [ ] Unfamiliar symbols were checked with `GetSymbolInfo_CppTools` before assumptions were made.
- [ ] Function dependency analysis used `GetSymbolCallHierarchy_CppTools` with the correct `callsFrom` direction.
- [ ] Absolute file paths were supplied when available.
- [ ] Any line numbers passed to tools were verified as exact and 1-based.
- [ ] Tool errors were recovered according to their messages.
- [ ] `No results found` outcomes were treated as valid when appropriate.
- [ ] Text search was limited to string literals, comments, non-C++ files, configuration, or documented fallback cases.
