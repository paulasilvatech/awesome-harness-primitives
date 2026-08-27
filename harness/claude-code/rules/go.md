---
paths:
  - "**/*.go"
  - "**/go.mod"
  - "**/go.sum"
---

<!-- Generated from harness/github-copilot/instructions/go.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces idiomatic Go conventions for package declarations, style, errors, modules, concurrency, HTTP, I/O, tests, security, and documentation.

# Go Conventions — Idiomatic Packages and APIs

This file applies to Go source files and module metadata matched by `**/*.go`, `**/go.mod`, and `**/go.sum`. It is authoritative for idiomatic Go style, package declarations, naming, formatting, error handling, modules, type design, concurrency, HTTP APIs and clients, I/O streaming, performance, tests, security, documentation, and workflow; repository-specific architecture and generated-code rules win where they are stricter.

## General Instructions

- Write simple, clear, and idiomatic Go code
- Favor clarity and simplicity over cleverness
- Follow the principle of least surprise
- Keep the happy path left-aligned (minimize indentation)
- Return early to reduce nesting
- Prefer early return over if-else chains; use `if condition { return }` pattern to avoid else blocks
- Make the zero value useful
- Write self-documenting code with clear, descriptive names
- Document exported types, functions, methods, and packages
- Use Go modules for dependency management
- Leverage the Go standard library instead of reinventing the wheel (e.g., use `strings.Builder` for string concatenation, `filepath.Join` for path construction)
- Prefer standard library solutions over custom implementations when functionality exists
- Write comments in English by default; translate only upon user request
- Avoid using emoji in code and comments

## Naming Conventions

### Packages

- Use lowercase, single-word package names
- Avoid underscores, hyphens, or mixedCaps
- Choose names that describe what the package provides, not what it contains
- Avoid generic names like `util`, `common`, or `base`
- Package names should be singular, not plural

#### Package Declaration Rules (CRITICAL):
- **NEVER duplicate `package` declarations** - each Go file must have exactly ONE `package` line
- When editing an existing `.go` file:
  - **PRESERVE** the existing `package` declaration - do not add another one
  - If you need to replace the entire file content, start with the existing package name
- When creating a new `.go` file:
  - **BEFORE writing any code**, check what package name other `.go` files in the same directory use
  - Use the SAME package name as existing files in that directory
  - If it's a new directory, use the directory name as the package name
  - Write **exactly one** `package <name>` line at the very top of the file
- When using file creation or replacement tools:
  - **ALWAYS verify** the target file doesn't already have a `package` declaration before adding one
  - If replacing file content, include only ONE `package` declaration in the new content
  - **NEVER** create files with multiple `package` lines or duplicate declarations

### Variables and Functions

- Use mixedCaps or MixedCaps (camelCase) rather than underscores
- Keep names short but descriptive
- Use single-letter variables only for very short scopes (like loop indices)
- Exported names start with a capital letter
- Unexported names start with a lowercase letter
- Avoid stuttering (e.g., avoid `http.HTTPServer`, prefer `http.Server`)

### Interfaces

- Name interfaces with -er suffix when possible (e.g., `Reader`, `Writer`, `Formatter`)
- Single-method interfaces should be named after the method (e.g., `Read` → `Reader`)
- Keep interfaces small and focused

### Constants

- Use MixedCaps for exported constants
- Use mixedCaps for unexported constants
- Group related constants using `const` blocks
- Consider using typed constants for better type safety

## Code Style and Formatting

### Formatting

- Always use `gofmt` to format code
- Use `goimports` to manage imports automatically
- Keep line length reasonable (no hard limit, but consider readability)
- Add blank lines to separate logical groups of code

### Comments

- Strive for self-documenting code; prefer clear variable names, function names, and code structure over comments
- Write comments only when necessary to explain complex logic, business rules, or non-obvious behavior
- Write comments in complete sentences in English by default
- Translate comments to other languages only upon specific user request
- Start sentences with the name of the thing being described
- Package comments should start with "Package [name]"
- Use line comments (`//`) for most comments
- Use block comments (`/* */`) sparingly, mainly for package documentation
- Document why, not what, unless the what is complex
- Avoid using emoji in comments and code

### Error Handling

- Check errors immediately after the function call
- Don't ignore errors using `_` unless you have a good reason (document why)
- Wrap errors with context using `fmt.Errorf` with `%w` verb
- Create custom error types when you need to check for specific errors
- Place error returns as the last return value
- Name error variables `err`
- Keep error messages lowercase and don't end with punctuation

## Architecture and Project Structure

### Package Organization

- Follow standard Go project layout conventions
- Keep `main` packages in `cmd/` directory
- Put reusable packages in `pkg/` or `internal/`
- Use `internal/` for packages that shouldn't be imported by external projects
- Group related functionality into packages
- Avoid circular dependencies

### Dependency Management

- Use Go modules (`go.mod` and `go.sum`)
- Keep dependencies minimal
- Regularly update dependencies for security patches
- Use `go mod tidy` to clean up unused dependencies
- Vendor dependencies only when necessary

## Type Safety and Language Features

### Type Definitions

- Define types to add meaning and type safety
- Use struct tags for JSON, XML, database mappings
- Prefer explicit type conversions
- Use type assertions carefully and check the second return value
- Prefer generics over unconstrained types; when an unconstrained type is truly needed, use the predeclared alias `any` instead of `interface{}` (Go 1.18+)

### Pointers vs Values

- Use pointer receivers for large structs or when you need to modify the receiver
- Use value receivers for small structs and when immutability is desired
- Use pointer parameters when you need to modify the argument or for large structs
- Use value parameters for small structs and when you want to prevent modification
- Be consistent within a type's method set
- Consider the zero value when choosing pointer vs value receivers

### Interfaces and Composition

- Accept interfaces, return concrete types
- Keep interfaces small (1-3 methods is ideal)
- Use embedding for composition
- Define interfaces close to where they're used, not where they're implemented
- Don't export interfaces unless necessary

## Concurrency

### Goroutines

- Be cautious about creating goroutines in libraries; prefer letting the caller control concurrency
- If you must create goroutines in libraries, provide clear documentation and cleanup mechanisms
- Always know how a goroutine will exit
- Use `sync.WaitGroup` or channels to wait for goroutines
- Avoid goroutine leaks by ensuring cleanup

### Channels

- Use channels to communicate between goroutines
- Don't communicate by sharing memory; share memory by communicating
- Close channels from the sender side, not the receiver
- Use buffered channels when you know the capacity
- Use `select` for non-blocking operations

### Synchronization

- Use `sync.Mutex` for protecting shared state
- Keep critical sections small
- Use `sync.RWMutex` when you have many readers
- Choose between channels and mutexes based on the use case: use channels for communication, mutexes for protecting state
- Use `sync.Once` for one-time initialization
- WaitGroup usage by Go version:
	- If `go >= 1.25` in `go.mod`, use the new `WaitGroup.Go` method ([documentation](https://pkg.go.dev/sync#WaitGroup)):
		```go
		var wg sync.WaitGroup
		wg.Go(task1)
		wg.Go(task2)
		wg.Wait()
		```
	- If `go < 1.25`, use the classic `Add`/`Done` pattern

## Error Handling Patterns

### Creating Errors

- Use `errors.New` for simple static errors
- Use `fmt.Errorf` for dynamic errors
- Create custom error types for domain-specific errors
- Export error variables for sentinel errors
- Use `errors.Is` and `errors.As` for error checking

### Error Propagation

- Add context when propagating errors up the stack
- Don't log and return errors (choose one)
- Handle errors at the appropriate level
- Consider using structured errors for better debugging

## API Design

### HTTP Handlers

- Use `http.HandlerFunc` for simple handlers
- Implement `http.Handler` for handlers that need state
- Use middleware for cross-cutting concerns
- Set appropriate status codes and headers
- Handle errors gracefully and return appropriate error responses
- Router usage by Go version:
	- If `go >= 1.22`, prefer the enhanced `net/http` `ServeMux` with pattern-based routing and method matching
	- If `go < 1.22`, use the classic `ServeMux` and handle methods/paths manually (or use a third-party router when justified)

### JSON APIs

- Use struct tags to control JSON marshaling
- Validate input data
- Use pointers for optional fields
- Consider using `json.RawMessage` for delayed parsing
- Handle JSON errors appropriately

### HTTP Clients

- Keep the client struct focused on configuration and dependencies only (e.g., base URL, `*http.Client`, auth, default headers). It must not store any per-request state
- Do not store or cache `*http.Request` inside the client struct, and do not persist request-specific state across calls; instead, construct a fresh request per method invocation
- Methods should accept `context.Context` and input parameters, assemble the `*http.Request` locally (or via a short-lived builder/helper created per call), then call `c.httpClient.Do(req)`
- If request-building logic is reused, factor it into unexported helper functions or a per-call builder type; never keep `http.Request` (URL params, body, headers) as fields on the long-lived client
- Ensure the underlying `*http.Client` is configured (timeouts, transport) and is safe for concurrent use; avoid mutating `Transport` after first use
- Always set headers on the request instance you’re sending, and close response bodies (`defer resp.Body.Close()`), handling errors appropriately

## Performance Optimization

### Memory Management

- Minimize allocations in hot paths
- Reuse objects when possible (consider `sync.Pool`)
- Use value receivers for small structs
- Preallocate slices when size is known
- Avoid unnecessary string conversions

### I/O: Readers and Buffers

- Most `io.Reader` streams are consumable once; reading advances state. Do not assume a reader can be re-read without special handling
- If you must read data multiple times, buffer it once and recreate readers on demand:
	- Use `io.ReadAll` (or a limited read) to obtain `[]byte`, then create fresh readers via `bytes.NewReader(buf)` or `bytes.NewBuffer(buf)` for each reuse
	- For strings, use `strings.NewReader(s)`; you can `Seek(0, io.SeekStart)` on `*bytes.Reader` to rewind
- For HTTP requests, do not reuse a consumed `req.Body`. Instead:
	- Keep the original payload as `[]byte` and set `req.Body = io.NopCloser(bytes.NewReader(buf))` before each send
	- Prefer configuring `req.GetBody` so the transport can recreate the body for redirects/retries: `req.GetBody = func() (io.ReadCloser, error) { return io.NopCloser(bytes.NewReader(buf)), nil }`
- To duplicate a stream while reading, use `io.TeeReader` (copy to a buffer while passing through) or write to multiple sinks with `io.MultiWriter`
- Reusing buffered readers: call `(*bufio.Reader).Reset(r)` to attach to a new underlying reader; do not expect it to “rewind” unless the source supports seeking
- For large payloads, avoid unbounded buffering; consider streaming, `io.LimitReader`, or on-disk temporary storage to control memory

- Use `io.Pipe` to stream without buffering the whole payload:
	- Write to `*io.PipeWriter` in a separate goroutine while the reader consumes
	- Always close the writer; use `CloseWithError(err)` on failures
	- `io.Pipe` is for streaming, not rewinding or making readers reusable

- **Warning:** When using `io.Pipe` (especially with multipart writers), all writes must be performed in strict, sequential order. Do not write concurrently or out of order—multipart boundaries and chunk order must be preserved. Out-of-order or parallel writes can corrupt the stream and result in errors.

- Streaming multipart/form-data with `io.Pipe`:
	- `pr, pw := io.Pipe()`; `mw := multipart.NewWriter(pw)`; use `pr` as the HTTP request body
	- Set `Content-Type` to `mw.FormDataContentType()`
	- In a goroutine: write all parts to `mw` in the correct order; on error `pw.CloseWithError(err)`; on success `mw.Close()` then `pw.Close()`
	- Do not store request/in-flight form state on a long-lived client; build per call
	- Streamed bodies are not rewindable; for retries/redirects, buffer small payloads or provide `GetBody`

### Profiling

- Use built-in profiling tools (`pprof`)
- Benchmark critical code paths
- Profile before optimizing
- Focus on algorithmic improvements first
- Consider using `testing.B` for benchmarks

## Testing

### Test Organization

- Keep tests in the same package (white-box testing)
- Use `_test` package suffix for black-box testing
- Name test files with `_test.go` suffix
- Place test files next to the code they test

### Writing Tests

- Use table-driven tests for multiple test cases
- Name tests descriptively using `Test_functionName_scenario`
- Use subtests with `t.Run` for better organization
- Test both success and error cases
- Consider using `testify` or similar libraries when they add value, but don't over-complicate simple tests

### Test Helpers

- Mark helper functions with `t.Helper()`
- Create test fixtures for complex setup
- Use `testing.TB` interface for functions used in tests and benchmarks
- Clean up resources using `t.Cleanup()`

## Security Best Practices

### Input Validation

- Validate all external input
- Use strong typing to prevent invalid states
- Sanitize data before using in SQL queries
- Be careful with file paths from user input
- Validate and escape data for different contexts (HTML, SQL, shell)

### Cryptography

- Use standard library crypto packages
- Don't implement your own cryptography
- Use crypto/rand for random number generation
- Store passwords using bcrypt, scrypt, or argon2 (consider golang.org/x/crypto for additional options)
- Use TLS for network communication

## Documentation

### Code Documentation

- Prioritize self-documenting code through clear naming and structure
- Document all exported symbols with clear, concise explanations
- Start documentation with the symbol name
- Write documentation in English by default
- Use examples in documentation when helpful
- Keep documentation close to code
- Update documentation when code changes
- Avoid emoji in documentation and comments

### README and Documentation Files

- Include clear setup instructions
- Document dependencies and requirements
- Provide usage examples
- Document configuration options
- Include troubleshooting section

## Tools and Development Workflow

### Essential Tools

- `go fmt`: Format code
- `go vet`: Find suspicious constructs
- `golangci-lint`: Additional linting (golint is deprecated)
- `go test`: Run tests
- `go mod`: Manage dependencies
- `go generate`: Code generation

### Development Practices

- Run tests before committing
- Use pre-commit hooks for formatting and linting
- Keep commits focused and atomic
- Write meaningful commit messages
- Review diffs before committing

## Common Pitfalls to Avoid

- Not checking errors
- Ignoring race conditions
- Creating goroutine leaks
- Not using defer for cleanup
- Modifying maps concurrently
- Not understanding nil interfaces vs nil pointers
- Forgetting to close resources (files, connections)
- Using global variables unnecessarily
- Overusing unconstrained types (e.g., `any`); prefer specific types or generic type parameters with constraints. If an unconstrained type is required, use `any` rather than `interface{}`
- Not considering the zero value of types
- **Creating duplicate `package` declarations** - this is a compile error; always check existing files before adding package declarations

## Good / Bad Examples

The examples below illustrate package declarations, early returns, and contextual error wrapping.

**Good:**

```go
package users

func LoadUser(ctx context.Context, id UserID) (*User, error) {
	if id == "" {
		return nil, fmt.Errorf("user id is required")
	}

	user, err := repository.Load(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("load user %s: %w", id, err)
	}
	return user, nil
}
```

Why: The file has exactly one package declaration, validates early, keeps the happy path left-aligned, and wraps errors with `%w`.

**Bad:**

```go
package users
package users

func LoadUser(id string) *User {
	user, _ := repository.Load(context.Background(), UserID(id))
	return user
}
```

Why: The file has duplicate `package` declarations, ignores errors, hides context ownership, and can return invalid data silently.

## Conventions

| Rule | Rationale |
|---|---|
| Keep each `.go` file to exactly one `package <name>` declaration and preserve existing package names when editing | Duplicate package declarations are compile errors and mismatched packages break directory builds |
| Run `gofmt` and `goimports` and keep imports automatically managed | Formatting and import order stay idiomatic |
| Prefer clear names, early returns, useful zero values, and standard library helpers such as `strings.Builder` and `filepath.Join` | Go code remains simple and unsurprising |
| Check errors immediately, name them `err`, return errors last, and wrap propagated errors with `fmt.Errorf` and `%w` | Callers receive actionable context without losing error identity |
| Use Go modules, keep dependencies minimal, and run `go mod tidy` | `go.mod` and `go.sum` stay reproducible and secure |
| Accept interfaces and return concrete types; define small interfaces near use | APIs remain testable without over-abstracting implementations |
| Know how every goroutine exits and choose channels or `sync.Mutex`/`sync.RWMutex` based on ownership | Concurrency avoids leaks, races, and unclear synchronization |
| Build HTTP clients with per-call `*http.Request`, `context.Context`, configured `*http.Client`, and closed response bodies | Long-lived clients stay concurrent-safe and request state does not leak between calls |
| Treat `io.Reader` streams and `req.Body` as consumable once unless buffered or configured with `GetBody` | Retries, redirects, and re-reads do not operate on empty streams |
| Test with table-driven tests, subtests, `t.Helper()`, `testing.TB`, and `t.Cleanup()` where appropriate | Tests remain expressive, reusable, and isolated |
| Validate external input, escape context-specific output, use standard crypto, and store passwords with bcrypt, scrypt, or argon2 | Security-sensitive code avoids common injection and cryptography failures |

## Do / Do Not

| Do | Do not |
|---|---|
| Use lowercase single-word package names without underscores, hyphens, or mixedCaps | Use generic package names such as `util`, `common`, or `base` |
| Use mixedCaps or MixedCaps and avoid stuttering such as `http.HTTPServer` | Use underscores or redundant package prefixes in identifiers |
| Document exported packages, types, functions, and methods with comments starting with the symbol name | Leave exported APIs undocumented or comment obvious implementation details |
| Use `any` only when an unconstrained type is truly needed | Overuse `interface{}` or unconstrained types instead of specific types or generics |
| Use `WaitGroup.Go` only when `go >= 1.25` in `go.mod`; otherwise use `Add`/`Done` | Assume new standard library APIs exist for older module versions |
| Use enhanced `net/http` `ServeMux` routing when `go >= 1.22` | Depend on pattern-based method routing in modules below Go 1.22 |
| Use `io.LimitReader`, streaming, or controlled buffering for large payloads | Buffer unbounded external input into memory |
| Write multipart `io.Pipe` streams sequentially and close `multipart.Writer` before closing the pipe writer | Write multipart parts concurrently or out of order |
| Use `pprof`, `testing.B`, and benchmarks before optimizing | Guess at performance bottlenecks without measurement |

## Checklist Before Opening a PR

- [ ] Every changed `.go` file has exactly one correct package declaration.
- [ ] `gofmt` and `goimports` have been applied.
- [ ] Errors are checked, wrapped with context, and not both logged and returned.
- [ ] Package, variable, function, interface, constant, and exported symbol names follow Go conventions.
- [ ] `go.mod` and `go.sum` are tidy and dependencies are justified.
- [ ] Goroutines, channels, mutexes, and cleanup paths cannot leak or race.
- [ ] HTTP handlers, clients, JSON APIs, and request bodies handle context, validation, headers, status codes, and response closing correctly.
- [ ] Reader, buffer, `io.Pipe`, multipart, retry, and redirect behavior respects one-pass stream semantics.
- [ ] Tests are table-driven or scenario-focused, use helpers correctly, and cover success and error cases.
- [ ] Security-sensitive code validates input, avoids custom cryptography, uses TLS where required, and stores passwords safely.
- [ ] Documentation and comments are in English by default and contain no emoji.

## References

- Effective Go: https://go.dev/doc/effective_go
- Go Code Review Comments: https://go.dev/wiki/CodeReviewComments
- Google's Go Style Guide: https://google.github.io/styleguide/go/
- `sync.WaitGroup` documentation: https://pkg.go.dev/sync#WaitGroup
