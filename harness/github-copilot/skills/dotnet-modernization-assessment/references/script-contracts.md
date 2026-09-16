# Local assessment script contracts

Both entry points require **Python 3.10+**, use only the standard library, print JSON to stdout, and
write no files. They do not invoke .NET, MSBuild, a container engine, an SDK installer, or Azure.
Preserve the exit code if saving output to an approved evidence location.

## Inventory

Run from the installed skill directory, passing the application's root rather than the skill's root:

```sh
python3 scripts/inventory_dotnet.py /path/to/application
python3 scripts/inventory_dotnet.py /path/to/application --exclude-dir vendor --max-file-bytes 2097152
```

The [inventory implementation](../scripts/inventory_dotnet.py) finds C#, Visual Basic and F# project
files; solution names; literal targets; SDK-style markers; shared props/targets; package IDs;
project references; container-file locations; and heuristic Windows/app-model signals.
The [shared parser](../scripts/dotnet_common.py) handles framework classification and bounded input.

- JSON `schema_version` is `1`. Status is `inventory-complete` or `inventory-incomplete`.
- Exit **0** means the selected text scan completed, not that migration is safe.
- Exit **1** means no projects, unreadable/oversized/linked text, unresolved targets, or unresolved
  project references require review. Inspect `coverage.warnings`.
- Exit **2** means invalid arguments/root, malformed build XML, rejected DTD/entity declarations,
  or filesystem failure. An explicit error goes to stderr; no success-shaped JSON is emitted.
- Targets inherited from `Directory.Build.props` are reported there, never invented as the effective
  target of a child project. Conditions/imports always require authorized MSBuild evaluation.
- Package versions, transitive dependencies, NuGet credentials, and configuration values are not
  emitted. A signal records only a relative path, the first matching line, and a fixed signal name.
- Web Forms without a project file is surfaced as incomplete, not silently classified as portable.
- UTF-8 and BOM-marked UTF-16 are accepted. Other encodings require reviewed conversion of a copy or
  manual assessment. Do not silently reinterpret legacy files as a different encoding.
- Symlinked inputs are not followed; build/package directories are excluded. `.gitignore` is not
  interpreted. Review the explicit exclusion list and use a narrowly scoped root.
- XML is parsed, not executed. SDK imports, build tasks, custom targets and restore are never invoked.

## HTTP image and port consistency

Collect inspection JSON for exactly one selected image using the environment's approved container
tool. Discover the configured container command before generating or running an engine command.
Do not pass a multi-platform manifest index as though it were a resolved image.

Only `Os`, `Architecture`, and (for Windows) `OsVersion` are consumed. Environment variables,
labels, registry addresses, and other potentially sensitive inspection fields are not echoed.
Supply the selected entry application's TFM, not a library target or an inferred image-tag version.

```sh
python3 scripts/validate_container_target.py --image-inspect image-inspect.json --target aca --framework net10.0 --listen-port 8080 --target-port 8080
python3 scripts/validate_container_target.py --image-inspect image-inspect.json --target appservice-windows --framework net481 --listen-port 80 --target-port 80
```

The [validator](../scripts/validate_container_target.py) has three profiles:
`appservice-windows`, `appservice-linux`, and `aca`. The conservative profiles use `amd64`;
Windows bases are limited to the verified LTSC 2019/2022 set. An unrecognized Windows build is
**outside the verified set**, not proof that Microsoft never supports it. Reverify policy before
extending the code and tests. The returned `policy.verified_on` is a snapshot date, not a live query.

- Exit **0** / `platform-consistent`: metadata and declared ports satisfy this narrow profile.
- Exit **1** / `incompatible`: OS/architecture, application TFM, Windows base, or ports conflict.
- Exit **2**: missing/invalid fields, duplicate JSON keys, multiple images, invalid ports/TFM,
  linked/oversized files, or invalid JSON. There is no default-to-Linux fallback.
- `target-port` is the platform's **container target port**, not the public HTTPS port 443.
- Port equality is declared evidence. The script neither discovers a socket nor proves reachability.
- Runtime contents, support/patch level, image provenance/digest, Windows build-host compatibility,
  app behavior, ingress mode, probes, identities, registry pulls, state, quota and region remain
  explicitly `unchecked`.
- This is an HTTP single-image consistency check, not a worker/job validator or a deployment gate
  that may bypass human approval.

Synthetic minimal metadata for tests is an object or a one-object array:

```json
{"Os": "linux", "Architecture": "amd64"}
```

For Windows, include the actual four-part version, for example `10.0.20348.100`.
Synthetic metadata must never be presented as inspection of a real image.

## Regression tests

Run the repository's existing standard-library test runner from this skill's script directory:

```sh
python3 -m unittest test_dotnet_assessment -v
```

The [tests](../scripts/test_dotnet_assessment.py) use temporary synthetic fixtures to cover legacy and
modern targets, inherited properties, Windows paths, incomplete scans, encodings, secret omission,
unsafe input, image/TFM mismatches, ports, exit codes, and non-mutating behavior. They do not establish
Windows-container, application, or Azure runtime compatibility.
