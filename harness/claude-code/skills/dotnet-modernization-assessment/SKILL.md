---
name: dotnet-modernization-assessment
description: >-
  Inventory legacy .NET projects, identify Windows and app-model migration risks, and check
  container platform evidence before choosing Azure hosting. Use when assessing .NET Framework,
  IIS, Web Forms, Windows containers, Windows-to-Linux migration, App Service readiness, or Azure
  Container Apps readiness.
---

<!-- Generated from harness/github-copilot/skills/dotnet-modernization-assessment/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# .NET modernization assessment

Turn a bounded application's source and runtime evidence into a migration decision without changing
the application or contacting Azure. Read [assessment criteria](references/assessment-guide.md) for
domain risks and [script contracts](references/script-contracts.md) before running the helpers.

## When to invoke

- "Assess this .NET Framework app before moving it to Azure."
- "Can this IIS application stay in a Windows container?"
- "Check whether this Windows workload can move to Linux or ACA."
- "Validate the image platform and port configuration before deployment."

## Assessment boundaries

| Question | Evidence needed |
| --- | --- |
| Can it be rehosted on Windows App Service? | Windows base and hosting support, IIS/app model, external dependencies, state, build/startup and behavior tests. |
| Can it run on modern .NET? | Effective project graph, unavailable technologies, package support, upgrade and regression tests. |
| Can it run on Linux? | Removal/isolation of Windows-only runtime dependencies, Linux build/startup and behavior tests. |
| Does the image fit the chosen service? | Actual image inspection, declared and observed ports, official service constraints, and target resource checks. |

The helpers produce **static inventory** and **platform consistency**, not deployment approval.
No missing signal, unknown project, skipped file, or absent runtime test is a pass.

## Prerequisites and context

- A user-selected application root and, ideally, the deployed entry project and source revision.
- Python 3.10 or later for the bundled standard-library scripts; no packages, SDK, network access,
  Docker engine, or Azure login are required by the scripts themselves.
- Authorization before invoking project build tools or collecting real container metadata.
- The executing agent must have command permission. A read-only agent only interprets existing output
  or returns commands as not run.

## Procedure

1. Bound the workload and record the objective: Windows rehost, runtime upgrade, Linux move, or comparison.
   Do not inventory a whole machine or upload source to a documentation service.
2. Run [the inventory script](scripts/inventory_dotnet.py) against that root. Review declared frameworks,
   shared build files, package names, project references, signals, and coverage warnings. It does not
   evaluate MSBuild, execute imports, restore packages, or print configuration values.
3. Resolve unknowns with authorized build-tool evaluation on a suitable runner. Include conditional
   targets, central package versions, transitive/native dependencies, and projects without project files.
   Establish a synthetic characterization baseline using existing tests.
4. Apply [assessment criteria](references/assessment-guide.md). Classify every signal as confirmed
   blocker, bounded remediation, acceptable constraint, false positive, or unresolved. Record the file,
   line or command evidence, owner, and next experiment.
5. Verify official runtime support and service constraints on the execution date. Prefer a stable LTS
   for a new modernization target unless the user selected another supported release. Keep .NET
   Framework runtime maintenance separate from a move to modern .NET.
6. When an HTTP image and candidate configuration exist, run
   [the target validator](scripts/validate_container_target.py) with inspection JSON, the selected
   application's TFM, and the declared listening/target ports. Check the actual listener separately.
7. Recommend one path and an alternative. Hand off to `dotnet-windows-appservice` or
   `dotnet-linux-modernization` (skills). Do not start deployment from an assessment.

## Limits

- Literal scanning does not establish effective properties, reachability, dependency closure, or
  business equivalence. A clean inventory still needs runtime evidence.
- Image validation is for a single HTTP application image. It does not certify sidecars, multi-image
  manifests, workers, jobs, registry access, runtime support, host compatibility, or Azure capacity.
- No automatic file rewriting, cloud queries, publication, credential collection, or deployment occurs.
- Preserve scoped exclusions and report unreadable, oversized, linked, or unresolved inputs explicitly.

## Output template

```markdown
## .NET migration decision
**Status:** assessed | insufficient-evidence | blocked
**Scope/revision:**
**Objective:**
**Recommended path and alternative:**

### Inventory
- Declared versus effective targets:
- Entry projects, libraries, tests, and shared build configuration:
- Scan coverage and manual evaluation still required:

### Findings
| Evidence | Classification | Impact on each path | Owner/next check |
| --- | --- | --- | --- |

### Validation and handoff
- Baseline and platform checks actually run:
- Runtime/cloud checks not run:
- Official sources and verification dates:
- Next skill, approved scope, and rollback requirements:
```

## Quality gate

- [ ] The workload is bounded and all scan limitations are visible.
- [ ] App model, runtime, OS, architecture, and hosting are separate decisions.
- [ ] Signals are reviewed rather than promoted automatically to compatibility claims.
- [ ] Official support and target constraints have dated evidence.
- [ ] Script exit codes and unrun runtime/cloud checks are reported truthfully.
- [ ] No source mutation, private-data upload, or deployment occurred during assessment.
