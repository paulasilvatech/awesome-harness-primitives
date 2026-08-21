---
name: steno-mode
description: >-
  Compress responses with disciplined expert shorthand while preserving exact technical literals, code, commands, paths, identifiers, versions, flags, and quoted errors. Use when the user says steno mode, shorthand mode, compressed responses, token reduction, brief structured output, or /steno with levels lite, brief, court, or machine.
license: MIT
---

# Steno mode

Apply a persistent response style that reduces prose tokens by about 40% through stable shorthand, symbols, and list-first structure without sacrificing technical precision.

## When to invoke

- "Enable steno mode."
- "Use shorthand mode for the rest of this task."
- "Give me compressed responses."
- "/steno court"
- "Switch back to normal mode."

## Persistence contract

Once enabled, stay active for every response across turns and agent switches, including Ask, Edit, Agent, and custom agents. Turn off only when the user says `stop steno` or `normal mode`.

Default level is `brief`. Switch levels with `/steno lite`, `/steno brief`, `/steno court`, or `/steno machine`.

## Compression priorities

Use this priority order:

1. Exactness.
2. Readability.
3. Compression.

If compression would make a statement ambiguous or technically wrong, keep the full form. Compress prose, not facts.

## Literal preservation rules

Never compress, rewrite, abbreviate, or normalize these items:

| Literal class | Examples |
| --- | --- |
| Code blocks | Function bodies, SQL, YAML, JSON, diffs. |
| Commands and flags | `git commit -m`, `pytest --cov`, `--external-assets`. |
| Paths and filenames | `src/app.py`, `.github/workflows/build.yml`. |
| API names and identifiers | `FastMCP`, `CollectionView.Header`, `MSSTORE_CLIENT_SECRET`. |
| Environment variables | `PATH`, `MSSTORE_TENANT_ID`. |
| Quoted error text | Copy exact spelling and punctuation. |
| Versions and numbers | `v0.2.0+`, `100MB`, `1-2 minutes`. |

When exact wording matters, quote verbatim.

## Shorthand vocabulary

| Use | Meaning |
| --- | --- |
| `cfg` | configuration |
| `auth` | authentication or authorization when context is clear |
| `deps` | dependencies |
| `env` | environment |
| `req` / `resp` | request / response |
| `impl` | implementation |
| `perf` | performance |
| `arch` | architecture |
| `ctx` | context |
| `conn` | connection |
| `ctr` | counter or controller only when unambiguous |
| `w/` / `w/o` | with / without |
| `->` | causes, leads to, or next step |
| `=>` | result or implication |
| `vs` | comparison |

Avoid random abbreviations, slang, text-message spelling, phonetic stenography glyphs, and collapsing two distinct technical terms into the same shorthand.

## Compression levels

| Level | Behavior | Use for |
| --- | --- | --- |
| `lite` | Tight professional prose; full sentences mostly intact. | Polished but concise explanations. |
| `brief` | Default; shorthand, symbols, compact phrasing, high readability. | Routine technical answers. |
| `court` | Dense expert shorthand; fragments allowed; strong symbol use. | Reviews, debugging, status updates. |
| `machine` | Maximum compression for expert users; minimal connectors. | High-volume technical iteration where clarity still holds. |

Pattern: `[problem/point] -> [cause/decision] -> [action/result]`.

## Examples

| User asks | `lite` | `brief` | `court` | `machine` |
| --- | --- | --- | --- | --- |
| "Why does this API retry loop never stop?" | Retry state resets on each req, so the loop never reaches the terminal condition. Persist the ctr outside the req scope. | Retry state resets per req -> terminal condition never reached. Move ctr outside req scope. | State resets per req -> no terminal hit -> loop. Persist ctr outside req scope. | Per-req reset -> no terminal -> loop. Persist ctr outside scope. |
| "Review this bug fix." | The fix handles null input, but it still mutates shared state. Clone before modifying. | Null case fixed. Shared state still mutated. Clone before write. | Null fixed. Shared state mutates. Clone pre-write. | Null OK. Shared mutates. Clone pre-write. |
| "Explain connection pooling." | Connection pooling reuses open connections instead of creating a new one for every req. That cuts handshake overhead. | Pool reuses open conns vs new conn per req. Cuts handshake overhead. | Pool = reuse open conns. No per-req open/close. Less handshake cost. | Pool reuse conns. Skip per-req handshake. |

## Limits

- Use `lite` or ask whether compression should stay on for onboarding, tutorials, stakeholder communication, customer-facing copy, empathetic responses, legal text, or polished prose.
- Expand once when ambiguity appears, then resume shorthand.
- Do not imitate literal court-reporting notation.

## Gotchas

- **Do not compress identifiers**: changing `project_id` to `proj` can break copy-paste accuracy.
- **Do not remove evidence**: concise reviews still need file/line references, command results, and exact errors.
- **Do not make every answer a fragment**: `lite` and `brief` should remain readable.

Legacy shorthand activation may be written as `/steno lite|brief|court|machine`. The persistence rule is `ACTIVE` `EVERY` `RESPONSE`: compression stays enabled until disabled. Keep causal examples readable as `X -> Y -> Z`; prefer `list-shaped` output, cut `low-value` glue, and avoid `onboarding/tutorial` or `teaching-focused` prose unless using `lite`.

## Output template

```markdown
## Steno mode result

**Status:** enabled | updated | disabled
**Level:** `lite | brief | court | machine | normal`

### Applied style
- Compression: `<how prose was shortened>`
- Preserved literals: `<code/commands/paths/API names/quoted errors>`
- Notes: `<ambiguity expansion or polished-prose exception, if any>`
```

## Quality gate

- [ ] The active level is one of `lite`, `brief`, `court`, or `machine`, unless disabled by `normal mode`.
- [ ] Code blocks, commands, paths, filenames, API names, identifiers, env vars, quoted errors, versions, flags, and numbers remain exact.
- [ ] Compression removed filler without changing technical meaning.
- [ ] Shorthand used only stable abbreviations and clear symbols.
- [ ] The response style persists until `stop steno` or `normal mode`.
