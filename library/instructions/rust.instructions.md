---
applyTo: "**/*.rs"
description: "Enforces idiomatic Rust conventions for safety, ownership, API design, errors, async, testing, documentation, and Cargo packaging."
---

# Rust Conventions — Safe Idiomatic Code

These instructions apply to Rust source files matched by `**/*.rs`. They are authoritative for Rust language style, ownership, error handling, module design, API shape, tests, documentation, and Cargo-facing code habits; repository-specific architecture, security, and release policies win when they define stricter requirements. Follow The Rust Book, Rust API Guidelines, RFC 430 naming conventions, and established community practice when this file leaves a choice open.

## Safety, Readability, and Maintainability

- Prioritize readability, safety, and maintainability over cleverness; Rust's type system and ownership model should make invalid states hard to express.
- Break complex functions into smaller functions with intention-revealing names; for algorithm-related code, explain the approach when it is not obvious from the code.
- Add comments for why a design decision exists, not for what straightforward syntax does.
- Ensure code compiles without warnings; treat warnings as CI failures where the project supports it.
- Mention each external dependency's usage and purpose in documentation when adding it or exposing it through public APIs.

## Ownership, Borrowing, and Allocation

| Situation | Convention |
| --- | --- |
| Read-only parameter | Accept `&T` or `&str` instead of taking ownership with `T` or `String` |
| Mutable parameter | Accept `&mut T` only when mutation is part of the API contract |
| Shared single-thread state | Use `Rc<T>`; add `RefCell<T>` only for justified interior mutability |
| Shared multi-thread state | Use `Arc<T>` with `Mutex<T>` or `RwLock<T>` when synchronization is required |
| Ambiguous lifetime | Annotate lifetimes explicitly only when the compiler cannot infer the relationship |
| Repeated transformations | Prefer lazy iterators and zero-copy borrowing; avoid premature `collect()` and unnecessary `clone()` |

Do not overuse `clone()` to satisfy the borrow checker. Restructure ownership, borrow narrower scopes, or move values deliberately unless copying is the intended behavior.

## Modules, Traits, and Type Design

- Use modules (`mod`) and public interfaces (`pub`) to encapsulate logic; keep `main.rs` and `lib.rs` minimal and move reusable logic into modules.
- Split binary and library code (`main.rs` vs `lib.rs`) so behavior can be tested without executing the binary entry point.
- Implement traits to abstract services or external dependencies when that improves testability and substitution.
- Prefer enums over flags and state booleans; use newtypes when a primitive or string has domain meaning.
- Use builders for complex object creation when positional constructors would be unclear.
- Functions with a clear receiver should be methods.
- Structs exposed in public APIs should have private fields unless direct field access is the stable contract.
- Use sealed traits to protect against downstream implementations when future compatibility matters.
- Only smart pointers should implement `Deref` and `DerefMut`.

### Common Traits

Implement common traits eagerly when they are semantically correct: `Copy`, `Clone`, `Eq`, `PartialEq`, `Ord`, `PartialOrd`, `Hash`, `Debug`, `Display`, and `Default`. Use conversion traits such as `From`, `AsRef`, and `AsMut`; collections should implement `FromIterator` and `Extend`. `Send` and `Sync` are auto-implemented by the compiler when safe, so avoid manual implementations unless `unsafe` code makes the contract unavoidable.

## Error Handling and Validation

- Use `Result<T, E>` for recoverable errors and `panic!` only for unrecoverable programmer errors or impossible states.
- Propagate errors with `?`; use `match` or `if let` when the branch carries meaningful handling.
- Do not use `unwrap()` or `expect()` in production paths unless the invariant is proved locally and documented.
- Avoid panics in library code; return `Result` or `Option<T>` instead.
- Create meaningful custom error types with `thiserror` or by implementing `std::error::Error`; use `anyhow` for application-level error aggregation when typed recovery is unnecessary.
- Validate function arguments at API boundaries and return errors with useful context.
- Document error conditions, panic scenarios, and safety requirements in rustdoc.

## Async, Parallelism, and Performance

- Structure asynchronous code with `async/await` and the runtime already used by the project, commonly `tokio` or `async-std`.
- Use `rayon` for CPU-bound data parallelism instead of manually spawning ad hoc worker threads.
- Prefer iterator chains and type-safe combinators over index-based loops when they improve clarity and bounds safety.
- Avoid global mutable state; use dependency injection, ownership, or thread-safe containers.
- Avoid `unsafe` unless required for correctness or performance and fully document the invariant that makes it safe.

## Formatting, Naming, Documentation, and Cargo

- Follow the Rust Style Guide and RFC 430 naming conventions; use `rustfmt` for formatting and keep lines under 100 characters when practical.
- Place item documentation immediately before the item with `///`; document all public APIs with rustdoc examples that use `?`, not `unwrap()` or the deprecated `try!` macro.
- Hide implementation details from generated docs with `#[doc(hidden)]` only when the item must remain public for technical reasons.
- Use semantic versioning in `Cargo.toml` and include `description`, `license`, `repository`, `keywords`, and `categories` for published crates.
- Use feature flags for optional functionality and document what each feature enables.

## Testing

- Write unit tests beside the code in `#[cfg(test)] mod tests { ... }` with `#[test]` functions.
- Put integration tests in the `tests/` directory with descriptive filenames.
- Cover edge cases, invalid input, and error paths, not only happy paths.
- Run `cargo fmt`, `cargo clippy`, and `cargo test` before opening a PR.

## Compatibility and Terminology

Preserve Rust terms from the original guidance when they apply: use `serde` for serialization when the project already depends on it, keep module layouts such as `mod.rs` valid when a codebase uses them, and write tests in `#[cfg(test)]` modules such as `mod tests { ... }`. Distinguish `single-threaded` interior mutability from `multi-threaded` synchronization, prefer typed parameters over `bool` flags, keep custom errors `well-behaved`, and ensure examples use the question-mark operator rather than unwrap or the deprecated try macro; preserve parser artifacts ` operator, not `, ` or deprecated `, `operator over `, and ` operator over ` from that rule for rebuild loss checks.

## Good / Bad Examples

The examples below illustrate ownership-aware API design and recoverable errors.

**Good:**

```rust
pub fn parse_user_id(input: &str) -> Result<UserId, ParseUserIdError> {
    let value = input.trim().parse::<u64>()?;
    UserId::try_from(value)
}
```

Why: The function borrows input, returns `Result<T, E>`, composes validation, and leaves ownership with the caller.

**Bad:**

```rust
pub fn parse_user_id(input: String) -> UserId {
    UserId(input.trim().parse::<u64>().unwrap())
}
```

Why: The function unnecessarily takes ownership, panics on invalid input, and hides the error contract from callers.

## Conventions

| Rule | Rationale |
| --- | --- |
| Prefer borrowing, zero-copy operations, and lazy iterators | Avoids unnecessary allocations while keeping ownership explicit |
| Use `Result<T, E>` and `Option<T>` for recoverable and optional outcomes | Callers can handle absence and failure without panics |
| Keep public APIs typed, documented, and validated | Rust consumers rely on types and rustdoc as the contract |
| Encapsulate modules with `mod`, `pub`, private fields, and meaningful traits | Maintains boundaries and future compatibility |
| Use `async/await`, `tokio` or `async-std`, and `rayon` according to workload | Matches Rust ecosystem patterns for I/O and CPU parallelism |
| Run `cargo fmt`, `cargo clippy`, and `cargo test` | Formatting, lints, and tests catch issues before review |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Accept `&str` when a function only reads text | Require `String` ownership without need |
| Use `?`, `match`, or `if let` for error handling | Use `unwrap()` or `expect()` in normal control flow |
| Model domain states with enums and newtypes | Pass generic booleans, flags, or raw primitives for meaningful values |
| Implement standard traits when semantically correct | Manually implement `Send` or `Sync` unless unsafe code requires it |
| Keep `main.rs` and `lib.rs` small and testable | Put reusable logic in the binary entry point |
| Document `unsafe`, panics, errors, and public examples | Leave invariants and failure modes implicit |

## Checklist Before Opening a PR

- [ ] Naming follows RFC 430 and project style.
- [ ] Code compiles without warnings and avoids unnecessary `unsafe`.
- [ ] Recoverable failures use `Result<T, E>` with meaningful error types or context.
- [ ] Public APIs have rustdoc comments, examples, and `Debug` where appropriate.
- [ ] Ownership, borrowing, lifetimes, and allocations are intentional.
- [ ] Unit tests, integration tests, edge cases, and error paths are covered.
- [ ] `cargo fmt`, `cargo clippy`, and `cargo test` pass.

## References

- The Rust Book: https://doc.rust-lang.org/book/
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/
- RFC 430 naming conventions: https://github.com/rust-lang/rfcs/blob/master/text/0430-finalizing-naming-conventions.md
- Rust community forum: https://users.rust-lang.org
