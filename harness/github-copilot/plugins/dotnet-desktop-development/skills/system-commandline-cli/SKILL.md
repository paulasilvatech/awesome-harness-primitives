---
name: system-commandline-cli
description: >-
  Add, modify, or review .NET CLI commands built with System.CommandLine by applying project command-base conventions, options and arguments, SetAction handlers, RootCommand registration, global options, dependency injection, validation, naming, and destructive-operation confirmation. Use when the user mentions System.CommandLine, CommandBase, ParseResult, SetAction, RootCommand, subcommands, or asks to add a CLI verb.
---

# System.CommandLine CLI development

Take a .NET CLI command request, transform it into project-consistent `System.CommandLine` command classes, handlers, options, arguments, DI services, registration, validation, and tests, and return a command implementation or review that preserves the existing CLI architecture.

## When to invoke

- "Add a new System.CommandLine command."
- "Wire this command with SetAction and ParseResult."
- "Register a subcommand under RootCommand."
- "Review these CLI options and arguments."
- "Add global options to a .NET CLI."

## Applicability

Use for .NET CLI projects using `System.CommandLine` v2.x.x on `.NET 8` or later, any `.NET Standard 2.0` implementation, `.NET Framework 4.6.1` or later, or `.NET Core 2.0` or later. Do not use for general C# coding, web APIs, UI work, or non-CLI projects.

## Project structure

Preserve the repository's existing structure. When adding a conventional command layout from scratch, use this shape:

```text
<CLI Project>/
├── Program.cs
└── Commands/
    ├── CommandBase.cs
    ├── GlobalOptions.cs
    ├── RootCommand.cs
    └── <Group>/
        ├── <Group>Command.cs
        └── <Group><Verb>Command.cs
```

| File | Responsibility |
| --- | --- |
| `Program.cs` | Entry point, service registration, parser or root command invocation. |
| `Commands/CommandBase.cs` | Project-specific abstract base class for shared helpers and conventions. |
| `Commands/GlobalOptions.cs` | Static definitions for shared recursive options. |
| `Commands/RootCommand.cs` | Registers top-level command groups and root options. |
| `Commands/<Group>/<Group>Command.cs` | Parent command that registers children. |
| `Commands/<Group>/<Group><Verb>Command.cs` | Leaf command with options, arguments, handler, and service calls. |

## Command class patterns

Prefer a project-specific `CommandBase` inheriting from `System.CommandLine.Command` when shared behavior exists. Concrete command classes are `internal` and inherit the existing base class; simple applications may inherit from `Command` directly if a base class adds no value.

```csharp
internal abstract class CommandBase : Command
{
    protected CommandBase(string name, string? description = null)
        : base(name, description)
    {
    }
}

internal sealed class MyCommand : CommandBase
{
    public MyCommand(IMyService service)
        : base("command-name", "Help text shown in --help")
    {
        this.SetAction(CommandHandler);
    }

    private async Task<int> CommandHandler(
        ParseResult parseResult,
        CancellationToken cancellationToken)
    {
        return 0;
    }
}
```

| Command type | Rule |
| --- | --- |
| Leaf command | Define options/arguments, call `this.SetAction(CommandHandler)`, parse values, validate early, call services, return exit code. |
| Group command | Register children with `this.Subcommands.Add(...)`; do not call `SetAction` unless direct invocation has useful behavior. |
| Root command | Add global options once to `RootCommand.Options` and top-level groups to `Subcommands`. |

## Options, arguments, and handlers

Define options and arguments as private readonly fields so the same symbol is used for registration and parsing.

```csharp
private readonly Option<string> _myOption;
private readonly Argument<string> _fileArgument;

_myOption = new Option<string>("--my-option")
{
    Description = "Clear description of what this option does",
    Required = true,
};
_myOption.Aliases.Add("-m");
this.Options.Add(_myOption);

_fileArgument = new Argument<string>("file")
{
    Description = "Path to the input file"
};
this.Arguments.Add(_fileArgument);

this.SetAction(CommandHandler);

private async Task<int> CommandHandler(ParseResult parseResult, CancellationToken cancellationToken)
{
    var value = parseResult.GetValue(_myOption);
    var file = parseResult.GetValue(_fileArgument);
    return 0;
}
```

Handler sequence:

1. Read option and argument values through `parseResult.GetValue(...)`.
2. Load session settings when needed.
3. Validate configuration early with clear parse or command errors.
4. Call service methods; keep business logic out of the command handler.
5. Output results with `Console` or the project's output abstraction.
6. Return `0` for success and non-zero for failure.

## Registration and dependency injection

| Concern | Required pattern |
| --- | --- |
| Top-level command | Register in `RootCommand.cs`: `this.Subcommands.Add(new MyGroupCommand(...));`. |
| Subcommand | Register inside the parent constructor: `this.Subcommands.Add(new MyGroupCreateCommand(...));`. |
| Service logic | Put command logic in service classes behind interfaces; inject interfaces into command constructors. |
| Service registration | Register services in `Program.cs`, for example `serviceCollection.TryAddSingleton<IMyService, MyServiceImpl>();`. |
| Convenience access | Add `ServiceProviderExtensions.cs` helpers only when the project already uses that style: `provider.GetRequiredService<IMyService>()`. |

Do not instantiate service implementations directly inside command handlers. Preserve existing DI container conventions and lifetimes.

## Global options

Define shared options once in `GlobalOptions.cs` and reuse the same `Option<T>` instance for registration, validation, and parsing.

```csharp
internal static class GlobalOptions
{
    public static readonly Option<string> EndpointOption = CreateEndpointOption();

    private static Option<string> CreateEndpointOption()
    {
        var option = new Option<string>("--endpoint")
        {
            Description = "Absolute http or https endpoint.",
            Recursive = true,
            Required = true,
        };

        option.Validators.Add(result =>
        {
            var value = result.GetValueOrDefault<string>();
            if (!Uri.TryCreate(value, UriKind.Absolute, out var uri) ||
                (uri.Scheme != Uri.UriSchemeHttp && uri.Scheme != Uri.UriSchemeHttps) ||
                !string.IsNullOrEmpty(uri.Query) ||
                !string.IsNullOrEmpty(uri.Fragment))
            {
                result.AddError("--endpoint must be an absolute http or https URI without query or fragment.");
            }
        });

        return option;
    }
}
```

| Requirement | Reason |
| --- | --- |
| Set `Recursive = true` | The option is accepted for every descendant command. |
| Add each global option exactly once to `RootCommand.Options` | Leaf duplication creates alias conflicts and inconsistent parsing. |
| Read through the static `GlobalOptions` symbol | A second `Option<T>` with the same aliases will not carry the parsed value. |
| Prefer `CommandBase` helpers such as `GetEndpoint(ParseResult parseResult)` and `GetKey(ParseResult parseResult)` | Shared conversion and fallback logic stays centralized. |
| Validate through `Validators` | Invalid input becomes a parse error and the handler is not invoked. |
| Endpoint validation | Accept nonblank absolute `http` or `https` URIs; reject unsupported schemes, relative URIs, query strings, and fragments. |
| Secret option validation | Optional secrets such as `--key` may be omitted, but explicitly blank or whitespace-only values are invalid; do not log, display, trim, or mutate them. |
| Tests | Exercise root parser defaults, explicit valid values, invalid values, and option placement before and after a representative subcommand; verify invalid input prevents handler execution. |

## Destructive operations

Prompt before irreversible or destructive work unless the project has a standard `--yes` or `--force` pattern.

```csharp
Console.WriteLine("Are you sure you want to delete X? This action cannot be undone. (yes/no)");
var confirmation = Console.ReadLine();
if (confirmation?.ToLower() != "yes" && confirmation?.ToLower() != "y")
{
    Console.WriteLine("Operation cancelled.");
    return 0;
}
```

Keep confirmation in the command layer and destructive business behavior in the service layer.

## Naming conventions

| Element | Convention | Example |
| --- | --- | --- |
| CLI command name | lowercase kebab-case | `agent create`, `set show` |
| Command class | PascalCase plus `Command` suffix | `AgentCreateCommand` |
| Option field | private readonly `_camelCaseOption` | `_projectNameOption` |
| Option long name | kebab-case with `--` | `--project-name` |
| Option short alias | one or two characters | `-p`, `-id`, `-md` |
| Argument field | private readonly `_camelCaseArgument` | `_fileArgument` |
| Namespace | project commands namespace plus group | `MyProject.Commands.Agent`, `MyProject.CLI.Commands.<Group>` |
| Folder | `Commands/<Group>/` | `Commands/Agent/` |
| Visibility | command classes are `internal` | `internal sealed class AgentCreateCommand` |

## Checklist for new commands

- [ ] Inherits from the existing project command base, or from `Command` only when no meaningful base exists.
- [ ] Constructor passes command `name` and `description` to the base constructor.
- [ ] Options and arguments have `Description`; required inputs set `Required`.
- [ ] Handler is wired with `this.SetAction(CommandHandler)`.
- [ ] Handler signature is `async Task<int> CommandHandler(ParseResult parseResult, CancellationToken cancellationToken)`.
- [ ] Command is registered in the parent, either `RootCommand` or a group command.
- [ ] Command class is `internal` and located in `Commands/<Group>/`.
- [ ] Namespace matches the folder and existing project convention.
- [ ] Business logic lives in injected services, not the handler.
- [ ] Destructive actions require confirmation or the project's established force flag.

## Gotchas

- **Do not duplicate global options**: recursive root registration makes them available in descendants; duplicating `Option<T>` instances breaks parsing expectations.
- **Keep validation separate from derivation**: parse validation should reject invalid input before handler execution; helper methods can derive `Uri`, keys, or settings from validated values.
- **Group commands are not leaf commands**: a parent that only groups subcommands should not call `SetAction`.
- **Stable errors matter**: validation messages should name the option and accepted format so tests and users can act on them.

## Source compatibility terms

Retain these System.CommandLine symbols and examples when updating older command files: `--kebab-case`, `MyProject.Commands.<Group>`, `Options`, `RULE`, `my-group`, `new Uri(...)`, `option/argument`, `parseResult.GetValue(GlobalOptions.Endpoint)`, `GetMyService`, `GlobalOptions.Endpoint`, `GlobalOptions.EndpointOption`, `GlobalOptions.KeyOption`, `KeyOption`, `MyGroupDeleteCommand`, `MyGroupListCommand`, `MyProject.Commands`, and `ServiceProvider`.

## Output template

```markdown
## System.CommandLine result — <command or review>

**Status:** implemented | reviewed | needs changes | blocked
**Command path:** `<root> <group> <verb>`
**Files changed or reviewed:** `<Program.cs>`, `<Commands/...>`

### Command shape
| Element | Value |
| --- | --- |
| Class | `<CommandClass>` |
| Base | `CommandBase` or `Command` |
| Handler | `SetAction(CommandHandler)` |
| Options | `<Option<T> fields and aliases>` |
| Arguments | `<Argument<T> fields>` |
| Registration | `<RootCommand.cs or parent command>` |

### Validation
- Root parser global options: pass | fail | not applicable
- Handler prevents invalid input: pass | fail | not applicable
- Destructive confirmation: pass | fail | not applicable
- Tests/build: `<command and result>`
```

## Quality gate

- [ ] The command follows existing project conventions before introducing a new `CommandBase` or folder pattern.
- [ ] All `System.CommandLine` symbols are reused consistently: `Command`, `Option<T>`, `Argument<T>`, `ParseResult`, `SetAction`, `RootCommand`, `Subcommands`, `Validators`, and `Recursive`.
- [ ] Global options are defined once, registered once on `RootCommand.Options`, and read through `GlobalOptions` or `CommandBase` helpers.
- [ ] Handler code is thin: parse, validate, call service, output, return exit code.
- [ ] Services are registered through DI in `Program.cs` and resolved according to project conventions.
- [ ] Naming, folder, namespace, alias, and visibility conventions are satisfied.
- [ ] Destructive operations have confirmation or an established explicit bypass.
- [ ] Parser tests or the smallest existing build/test command validate the changed command path.
