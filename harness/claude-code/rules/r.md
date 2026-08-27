---
paths:
  - "**/*.R"
  - "**/*.r"
  - "**/*.Rmd"
  - "**/*.rmd"
  - "**/*.qmd"
---

<!-- Generated from harness/github-copilot/instructions/r.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces idiomatic R, R Markdown, and Quarto conventions for style, reproducibility, data wrangling, plotting, errors, security, Shiny, tooling, and tests.

# R Conventions — Reproducible Analysis Code

These instructions apply to R scripts, R Markdown, and Quarto files matched by the R globs. They are authoritative for R style, vectorization, paths, reproducibility, package qualification, data wrangling, plotting, errors, security, Shiny, documents, tooling, and Copilot suggestions; project-specific style, statistical methodology, security, and reproducibility policies win when stricter.

## Core R Style and Reproducibility

- Match the project's existing style: tidyverse vs base R, `%>%` vs `|>`, and package qualification patterns.
- Prefer clear vectorized code, small functions, and explicit returns over hidden side effects.
- Use `lower_snake_case` for objects and files; avoid dots in names.
- Qualify non-base calls in examples and snippets, such as `dplyr::mutate()` and `stringr::str_detect()`; use `library()` in project code only when that is the repository norm.
- Never call `setwd()`; use project-relative paths such as `here::here()` and portable helpers from `fs`.
- Use `withr::with_seed()` locally around stochastic operations instead of setting global seed state.
- Validate user inputs with typed checks and allowlists.
- Avoid `eval(parse())`, unvalidated shell calls, and unparameterized SQL.

## Pipes, Data Wrangling, and I/O

| Concern | Convention |
| --- | --- |
| Native pipe | Prefer `|>` in R `>= 4.1.0` when no magrittr features are needed |
| Magrittr pipe | Continue `%>%` when the project uses magrittr or needs `.`, `%T>%`, or `%$%` |
| Consistency | Do not mix `|>` and `%>%` in the same script without a clear technical reason |
| Data frames | Prefer tibbles in tidyverse-heavy files; use base `data.frame()` in base-style files |
| Iteration | Use `purrr::map_*()` in tidyverse code; use `vapply()` or `Map()` in base-style code when clearer or type-stable |
| Strings and dates | Use `stringr` and `lubridate` where present; otherwise use clear base helpers such as `nchar()`, `substr()`, and `as.Date()` with explicit formats |
| I/O | Prefer explicit typed readers such as `readr::read_csv()` and make parsing assumptions explicit |

## Performance and Tooling

- For large datasets, consider `data.table` and benchmark with the real workload.
- Use `dtplyr` when dplyr syntax should translate to data.table operations.
- Profile before optimizing with `profvis::profvis()`.
- Cache repeated expensive work with `memoise::memoise()` when inputs and invalidation are clear.
- Prefer vectorized operations over loops; use loops only when they are clearer and not a bottleneck.
- Format with `styler` using tidyverse style, two-space indents, and approximately 100-character lines.
- Lint with `lintr` configured through `.lintr`; consider `precommit` hooks to run linting and formatting.
- Document exported functions with roxygen2 tags such as `@param`, `@return`, and `@examples`.
- Manage dependencies with `renv` and snapshot after adding packages.

## Error Handling and Security

| Situation | Preferred pattern |
| --- | --- |
| Tidyverse condition | `rlang::abort()` or `rlang::warn()` |
| Base condition | `stop()` or `warning()` |
| Recoverable fallback | `purrr::possibly()` for a typed fallback value |
| Capture result and error | `purrr::safely()` |
| Fine-grained base control | `tryCatch()` |
| Shell command | `processx::run()` or `sys::exec_wait()` with validated arguments |
| SQL | Parameterized `DBI` queries |
| User path | Normalize and sanitize with helpers such as `fs::path_sanitize()` and allowlists |
| Credentials | Use `Sys.getenv()`, config outside VCS, or `keyring` |

Keep return structures consistent: use typed outputs for normal flows and structured lists only when error details are required.

## Shiny, R Markdown, and Quarto

- Modularize Shiny UI and server logic for non-trivial apps.
- Use `eventReactive()` and `observeEvent()` for explicit dependencies.
- Validate Shiny inputs with `req()` and clear user-friendly messages.
- Use database connection pooling with `pool`; avoid long-lived global objects.
- Isolate expensive Shiny computations and use `reactiveVal()` or `reactiveValues()` for small state.
- Keep R Markdown and Quarto chunks focused with explicit options such as `echo`, `message`, and `warning`.
- Avoid global state in documents; use local helpers and `withr::with_seed()` for deterministic chunks.

## Copilot Suggestion Bias

When the current file uses tidyverse, suggest tidyverse-first patterns such as `dplyr::across()` instead of superseded verbs. When the file uses base R, suggest base idioms. Prefer small helper functions over long pipelines, type-stable code over implicit coercion, vectorized or tidy solutions over loops when idiomatic, and explain trade-offs when multiple approaches are equivalent.

## R Idioms and Example Terms

Preserve R terms from the original guidance: use `ggplot2` for `publication-quality` plots, use `apply()` family helpers where clear, and keep `purrr` patterns for tidyverse iteration. In `base-only` or `non-tidyverse` files, prefer base idioms. Sanitize `user-provided` paths, use `here` style project paths, run `lint/format` hooks where configured, and remember that `TRUE` is the R logical constant. Example documentation may include `safe_log`, `z_score`, `z-score`, and `z-scores`; examples/snippets** should qualify non-base calls. For `fine-grained` error handling, use `tryCatch()` when tidyverse condition helpers are not appropriate. Use `lower_snake_case` for `objects/files`.

## Good / Bad Examples

The examples below illustrate reproducible, qualified, type-stable transformation.

**Good:**

```r
result <- tibble::tibble(id = 1:5, x = c(1, 3, 2, 5, 4)) |>
  dplyr::mutate(z = purrr::map_dbl(x, purrr::possibly(log, otherwise = NA_real_))) |>
  dplyr::filter(z > 0)
```

Why: The code qualifies non-base functions, uses the native pipe consistently, and returns a typed numeric vector.

**Bad:**

```r
setwd('/analysis')
result <- eval(parse(text = user_input))
```

Why: The code changes global state and evaluates untrusted text.

## Conventions

| Rule | Rationale |
| --- | --- |
| Match tidyverse or base style already present in the file | Mixed idioms make R code harder to maintain |
| Use project-relative paths and local seeds | Analyses remain reproducible across machines and documents |
| Qualify non-base functions in examples | Suggestions remain clear without assuming attached packages |
| Prefer vectorized, type-stable functions | R failures often come from implicit coercion and shape changes |
| Use structured error handling and parameterized external calls | Failures stay inspectable and secure |
| Use `styler`, `lintr`, roxygen2, tests, and `renv` | Tooling keeps style, docs, quality, and dependencies reproducible |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `here::here()` and `fs` helpers | Call `setwd()` in scripts or chunks |
| Use `withr::with_seed()` around randomness | Set global seed state unnecessarily |
| Use `processx::run()` or `sys::exec_wait()` with validated args | Pass unvalidated input to `system()` |
| Use parameterized `DBI` queries | Build SQL with string concatenation from user input |
| Use `purrr::possibly()`, `purrr::safely()`, or `tryCatch()` deliberately | Return inconsistent ad hoc error shapes |
| Use `reactiveVal()`, `reactiveValues()`, and `pool` appropriately in Shiny | Store long-lived global mutable objects in Shiny apps |

## Checklist Before Opening a PR

- [ ] R code matches the file's tidyverse or base style and uses one pipe style consistently.
- [ ] Object and file names use `lower_snake_case` and avoid dot-style names.
- [ ] Paths are project-relative; no `setwd()` is introduced.
- [ ] Random operations use local seeding with `withr::with_seed()` where determinism matters.
- [ ] Inputs, shell arguments, SQL parameters, file paths, and credentials follow the security rules.
- [ ] Data wrangling, I/O, plotting, Shiny, and document chunks are explicit and reproducible.
- [ ] Exported functions have roxygen2 docs and tests where behavior changed.
- [ ] Formatting, linting, and dependency snapshots follow `styler`, `lintr`, `precommit`, and `renv` where configured.
