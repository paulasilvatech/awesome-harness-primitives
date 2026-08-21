---
applyTo: "**/Makefile,**/makefile,**/*.mk,**/GNUmakefile"
description: "Enforces GNU Make conventions for Makefile layout, variables, prerequisites, recipes, phony targets, portability, and diagnostics."
---

# Makefile Conventions — GNU Make Hygiene

This file applies to `Makefile`, `makefile`, `GNUmakefile`, and `*.mk` files. It is authoritative for GNU Make file structure, variables, rules, recipes, phony targets, includes, conditionals, generated prerequisites, diagnostics, clean targets, portability, performance, comments, and special targets; language-specific build instructions and repository build scripts win when they define stricter target names or validation commands.

## General Principles

- Write clear and maintainable makefiles that follow GNU Make conventions
- Use descriptive target names that clearly indicate their purpose
- Keep the default goal (first target) as the most common build operation
- Prioritize readability over brevity when writing rules and recipes
- Add comments to explain complex rules, variables, or non-obvious behavior

## Naming Conventions

- Name your makefile `Makefile` (recommended for visibility) or `makefile`
- Use `GNUmakefile` only for GNU Make-specific features incompatible with other make implementations
- Use standard variable names: `objects`, `OBJECTS`, `objs`, `OBJS`, `obj`, or `OBJ` for object file lists
- Use uppercase for built-in variable names (e.g., `CC`, `CFLAGS`, `LDFLAGS`)
- Use descriptive target names that reflect their action (e.g., `clean`, `install`, `test`)

## File Structure

- Place the default goal (primary build target) as the first rule in the makefile
- Group related targets together logically
- Define variables at the top of the makefile before rules
- Use `.PHONY` to declare targets that don't represent files
- Structure makefiles with: variables, then rules, then phony targets

```makefile
# Variables
CC = gcc
CFLAGS = -Wall -g
objects = main.o utils.o

# Default goal
all: program

# Rules
program: $(objects)
	$(CC) -o program $(objects)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Phony targets
.PHONY: clean all
clean:
	rm -f program $(objects)
```

## Variables and Substitution

- Use variables to avoid duplication and improve maintainability
- Define variables with `:=` (simple expansion) for immediate evaluation, `=` for recursive expansion
- Use `?=` to set default values that can be overridden
- Use `+=` to append to existing variables
- Reference variables with `$(VARIABLE)` not `$VARIABLE` (unless single character)
- Use automatic variables (`$@`, `$<`, `$^`, `$?`, `$*`) in recipes to make rules more generic

```makefile
# Simple expansion (evaluates immediately)
CC := gcc

# Recursive expansion (evaluates when used)
CFLAGS = -Wall $(EXTRA_FLAGS)

# Conditional assignment
PREFIX ?= /usr/local

# Append to variable
CFLAGS += -g
```

## Rules and Prerequisites

- Separate targets, prerequisites, and recipes clearly
- Use implicit rules for standard compilations (e.g., `.c` to `.o`)
- List prerequisites in logical order (normal prerequisites before order-only)
- Use order-only prerequisites (after `|`) for directories and dependencies that shouldn't trigger rebuilds
- Include all actual dependencies to ensure correct rebuilds
- Avoid circular dependencies between targets
- Remember that order-only prerequisites are omitted from automatic variables like `$^`, so reference them explicitly if needed

The example below shows a pattern rule that compiles objects into an `obj/` directory. The directory itself is listed as an order-only prerequisite so it is created before compiling but does not force recompilation when its timestamp changes.

```makefile
# Normal prerequisites
program: main.o utils.o
	$(CC) -o $@ $^

# Order-only prerequisites (directory creation)
obj/%.o: %.c | obj
	$(CC) $(CFLAGS) -c $< -o $@

obj:
	mkdir -p obj
```

## Recipes and Commands

- Start every recipe line with a **tab character** (not spaces) unless `.RECIPEPREFIX` is changed
- Use `@` prefix to suppress command echoing when appropriate
- Use `-` prefix to ignore errors for specific commands (use sparingly)
- Combine related commands with `&&` or `;` on the same line when they must execute together
- Keep recipes readable; break long commands across multiple lines with backslash continuation
- Use shell conditionals and loops within recipes when needed

```makefile
# Silent command
clean:
	@echo "Cleaning up..."
	@rm -f $(objects)

# Ignore errors
.PHONY: clean-all
clean-all:
	-rm -rf build/
	-rm -rf dist/

# Multi-line recipe with proper continuation
install: program
	install -d $(PREFIX)/bin && \
		install -m 755 program $(PREFIX)/bin
```

## Phony Targets

- Always declare phony targets with `.PHONY` to avoid conflicts with files of the same name
- Use phony targets for actions like `clean`, `install`, `test`, `all`
- Place phony target declarations near their rule definitions or at the end of the makefile

```makefile
.PHONY: all clean test install

all: program

clean:
	rm -f program $(objects)

test: program
	./run-tests.sh

install: program
	install -m 755 program $(PREFIX)/bin
```

## Pattern Rules and Implicit Rules

- Use pattern rules (`%.o: %.c`) for generic transformations
- Leverage built-in implicit rules when appropriate (GNU Make knows how to compile `.c` to `.o`)
- Override implicit rule variables (like `CC`, `CFLAGS`) rather than rewriting the rules
- Define custom pattern rules only when built-in rules are insufficient

```makefile
# Use built-in implicit rules by setting variables
CC = gcc
CFLAGS = -Wall -O2

# Custom pattern rule for special cases
%.pdf: %.md
	pandoc $< -o $@
```

## Splitting Long Lines

- Use backslash-newline (`\`) to split long lines for readability
- Be aware that backslash-newline is converted to a single space in non-recipe contexts
- In recipes, backslash-newline preserves the line continuation for the shell
- Avoid trailing whitespace after backslashes

### Splitting Without Adding Whitespace

If you need to split a line without adding whitespace, you can use a special technique: insert `$ ` (dollar-space) followed by a backslash-newline. The `$ ` refers to a variable with a single-space name, which doesn't exist and expands to nothing, effectively joining the lines without inserting a space.

```makefile
# Concatenate strings without adding whitespace
# The following creates the value "oneword"
var := one$ \
       word

# This is equivalent to:
# var := oneword
```

```makefile
# Variable definition split across lines
sources = main.c \
          utils.c \
          parser.c \
          handler.c

# Recipe with long command
build: $(objects)
	$(CC) -o program $(objects) \
	      $(LDFLAGS) \
	      -lm -lpthread
```

## Including Other Makefiles

- Use `include` directive to share common definitions across makefiles
- Use `-include` (or `sinclude`) to include optional makefiles without errors
- Place `include` directives after variable definitions that may affect included files
- Use `include` for shared variables, pattern rules, or common targets

```makefile
# Include common settings
include config.mk

# Include optional local configuration
-include local.mk
```

## Conditional Directives

- Use conditional directives (`ifeq`, `ifneq`, `ifdef`, `ifndef`) for platform or configuration-specific rules
- Place conditionals at the makefile level, not within recipes (use shell conditionals in recipes)
- Keep conditionals simple and well-documented

```makefile
# Platform-specific settings
ifeq ($(OS),Windows_NT)
    EXE_EXT = .exe
else
    EXE_EXT =
endif

program: main.o
	$(CC) -o program$(EXE_EXT) main.o
```

## Automatic Prerequisites

- Generate header dependencies automatically rather than maintaining them manually
- Use compiler flags like `-MMD` and `-MP` to generate `.d` files with dependencies
- Include generated dependency files with `-include $(deps)` to avoid errors if they don't exist

```makefile
objects = main.o utils.o
deps = $(objects:.o=.d)

# Include dependency files
-include $(deps)

# Compile with automatic dependency generation
%.o: %.c
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@
```

## Error Handling and Debugging

- Use `$(error text)` or `$(warning text)` functions for build-time diagnostics
- Test makefiles with `make -n` (dry run) to see commands without executing
- Use `make -p` to print the database of rules and variables for debugging
- Validate required variables and tools at the beginning of the makefile

```makefile
# Check for required tools
ifeq ($(shell which gcc),)
    $(error "gcc is not installed or not in PATH")
endif

# Validate required variables
ifndef VERSION
    $(error VERSION is not defined)
endif
```

## Clean Targets

- Always provide a `clean` target to remove generated files
- Declare `clean` as phony to avoid conflicts with a file named "clean"
- Use `-` prefix with `rm` commands to ignore errors if files don't exist
- Consider separate `clean` (removes objects) and `distclean` (removes all generated files) targets

```makefile
.PHONY: clean distclean

clean:
	-rm -f $(objects)
	-rm -f $(deps)

distclean: clean
	-rm -f program config.mk
```

## Portability Considerations

- Avoid GNU Make-specific features if portability to other make implementations is required
- Use standard shell commands (prefer POSIX shell constructs)
- Test with `make -B` to force rebuild all targets
- Document any platform-specific requirements or GNU Make extensions used

## Performance Optimization

- Use `:=` for variables that don't need recursive expansion (faster)
- Avoid unnecessary use of `$(shell ...)` which creates subprocesses
- Order prerequisites efficiently (most frequently changing files last)
- Use parallel builds (`make -j`) safely by ensuring targets don't conflict

## Documentation and Comments

- Add a header comment explaining the makefile's purpose
- Document non-obvious variable settings and their effects
- Include usage examples or targets in comments
- Add inline comments for complex rules or platform-specific workarounds

```makefile
# Makefile for building the example application
#
# Usage:
#   make          - Build the program
#   make clean    - Remove generated files
#   make install  - Install to $(PREFIX)
#
# Variables:
#   CC       - C compiler (default: gcc)
#   PREFIX   - Installation prefix (default: /usr/local)

# Compiler and flags
CC ?= gcc
CFLAGS = -Wall -Wextra -O2

# Installation directory
PREFIX ?= /usr/local
```

## Special Targets

- Use `.PHONY` for non-file targets
- Use `.PRECIOUS` to preserve intermediate files
- Use `.INTERMEDIATE` to mark files as intermediate (automatically deleted)
- Use `.SECONDARY` to prevent deletion of intermediate files
- Use `.DELETE_ON_ERROR` to remove targets if recipe fails
- Use `.SILENT` to suppress echoing for all recipes (use sparingly)

```makefile
# Don't delete intermediate files
.SECONDARY:

# Delete targets if recipe fails
.DELETE_ON_ERROR:

# Preserve specific files
.PRECIOUS: %.o
```

## Common Patterns

### Standard Project Structure

```makefile
CC = gcc
CFLAGS = -Wall -O2
objects = main.o utils.o parser.o

.PHONY: all clean install

all: program

program: $(objects)
	$(CC) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	-rm -f program $(objects)

install: program
	install -d $(PREFIX)/bin
	install -m 755 program $(PREFIX)/bin
```

### Managing Multiple Programs

```makefile
programs = prog1 prog2 prog3

.PHONY: all clean

all: $(programs)

prog1: prog1.o common.o
	$(CC) -o $@ $^

prog2: prog2.o common.o
	$(CC) -o $@ $^

prog3: prog3.o
	$(CC) -o $@ $^

clean:
	-rm -f $(programs) *.o
```

## Anti-Patterns to Avoid

- Don't start recipe lines with spaces instead of tabs
- Avoid hardcoding file lists when they can be generated with wildcards or functions
- Don't use `$(shell ls ...)` to get file lists (use `$(wildcard ...)` instead)
- Avoid complex shell scripts in recipes (move to separate script files)
- Don't forget to declare phony targets as `.PHONY`
- Avoid circular dependencies between targets
- Don't use recursive make (`$(MAKE) -C subdir`) unless absolutely necessary

## Good / Bad Examples

The examples below illustrate default-goal structure, variables, automatic variables, and phony cleanup.

**Good:**

```makefile
CC ?= gcc
CFLAGS += -Wall -Wextra
objects := main.o utils.o

.PHONY: all clean
all: program

program: $(objects)
	$(CC) -o $@ $^

clean:
	-rm -f program $(objects)
```

Why: The default goal is first, configurable variables are explicit, `$@` and `$^` keep the rule generic, and `clean` is declared `.PHONY`.

**Bad:**

```makefile
program:
    gcc -o program main.o utils.o
clean:
	rm -rf *
```

Why: The recipe starts with spaces, hardcodes tool choices and inputs, omits prerequisites, omits `.PHONY`, and uses an unsafe cleanup pattern.

## Conventions

| Rule | Rationale |
|---|---|
| Put the default goal first and keep it the most common build operation | `make` without arguments should do the expected thing |
| Use `Makefile` or `makefile`; reserve `GNUmakefile` for GNU Make-specific features | Contributors can find the build entrypoint and understand portability requirements |
| Define variables before rules and use `$(VARIABLE)` references, `:=`, `=`, `?=`, and `+=` intentionally | Expansion behavior stays predictable and override-friendly |
| Declare action targets such as `all`, `clean`, `test`, `install`, and `distclean` with `.PHONY` | File names cannot accidentally suppress recipes |
| Use normal prerequisites for build inputs and order-only prerequisites after `|` for directories | Directory timestamp changes do not force unnecessary rebuilds |
| Start recipe lines with tabs unless `.RECIPEPREFIX` is deliberately changed | Make parses recipes correctly |
| Generate dependencies with `-MMD`, `-MP`, dependency variables such as `deps`, and `-include $(deps)` when compiling C-family code | Header changes trigger correct rebuilds without brittle manual lists |
| Use diagnostics such as `$(error text)`, `$(warning text)`, `make -n`, `make -p`, and `make -B` during authoring | Build failures become explainable before they reach CI |
| Use `.DELETE_ON_ERROR`, `.SECONDARY`, `.INTERMEDIATE`, and `.PRECIOUS` only when their lifecycle semantics are intended | Intermediate files and failed targets are preserved or removed for clear reasons |
| Prefer `$(wildcard ...)` over `$(shell ls ...)` and avoid unnecessary recursive make | Builds stay faster, safer, and easier to parallelize with `make -j` |

## Do / Do Not

| Do | Do not |
|---|---|
| Use uppercase built-in variables such as `CC`, `CFLAGS`, `LDFLAGS`, and `EXE_EXT` | Hide tool choices in hardcoded recipe commands |
| Keep object lists in standard names such as `objects`, `OBJECTS`, `objs`, `OBJS`, `obj`, or `OBJ` | Invent unclear names for common build artifacts |
| Use automatic variables `$@`, `$<`, `$^`, `$?`, and `$*` in reusable rules | Repeat target and prerequisite names in recipes |
| Use `include`, `-include`, or `sinclude` for shared or optional makefiles | Duplicate common variables and rules across files |
| Use make-level `ifeq`, `ifneq`, `ifdef`, and `ifndef` for configuration | Put make conditionals inside shell recipes |
| Use `install -d`, `install -m 755`, and `PREFIX ?= /usr/local` for install targets | Assume system paths or permissions without exposing overrides |
| Split long lines with backslash-newline and avoid trailing whitespace after `\` | Create unreadable one-line recipes or broken continuations |
| Use `-` before cleanup commands only when missing files are acceptable | Blanket-ignore errors that should fail the build |

## Checklist Before Opening a PR

- [ ] The first rule is the intended default goal.
- [ ] Variables are defined before rules and use the correct expansion operator.
- [ ] Recipe lines start with tabs or an explicitly documented `.RECIPEPREFIX`.
- [ ] Phony action targets are declared with `.PHONY`.
- [ ] Normal and order-only prerequisites are separated correctly.
- [ ] Automatic dependency generation uses `-MMD`, `-MP`, and `-include` where header dependencies matter.
- [ ] `clean` and `distclean` remove only generated files and tolerate absent outputs deliberately.
- [ ] `make -n` or the repository's documented dry-run/build validation has been checked for changed targets.
- [ ] GNU Make-specific constructs are documented when portability matters.

## References

- GNU Make manual: https://www.gnu.org/software/make/manual/
