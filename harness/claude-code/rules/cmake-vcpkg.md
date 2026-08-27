---
paths:
  - "**/*.cmake"
  - "**/CMakeLists.txt"
  - "**/*.cpp"
  - "**/*.c"
  - "**/*.h"
  - "**/*.hpp"
---

<!-- Generated from harness/github-copilot/instructions/cmake-vcpkg.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Conventions for cross-platform CMake C and C++ projects that use vcpkg manifest mode, CMakePresets.json, policies, and compiler-portable build configuration.

# CMake vcpkg Conventions — Manifest Mode

These instructions apply to CMake, C, and C++ files in projects that use vcpkg in manifest mode. They are authoritative for dependency-management guidance, CMake cache configuration, policy awareness, cross-platform compiler portability, and OpenCV filesystem examples; project-specific toolchains, CI presets, and platform support matrices win when they define stricter requirements.

## vcpkg Manifest Mode

This project uses vcpkg in manifest mode, so dependency guidance must modify the manifest and build configuration rather than relying on global installs.

| Need | Convention |
| --- | --- |
| Add a library | Add or update the dependency in `vcpkg.json`, then configure with the vcpkg toolchain through the project's normal CMake preset. |
| Avoid global install advice | Do not suggest `vcpkg install library`; it does not behave as expected for manifest-mode projects. |
| Features | Use manifest features when optional dependency sets are needed instead of ad hoc install commands. |
| Versions | Respect the repository's vcpkg baseline, registry, overlay ports, and triplets when present. |
| Reproducibility | Keep dependency changes reviewable in source-controlled manifest and preset files. |

When recommending commands, prefer configure/build/test commands that flow through the project presets instead of bypassing the manifest.

## CMakePresets and Cache Variables

Prefer setting cache variables and other build configuration through `CMakePresets.json` when possible.

- Put repeatable configure options, toolchain paths, build types, generator choices, and feature toggles in presets rather than one-off command lines.
- Keep user-specific paths out of shared presets unless the project already uses a documented macro or environment variable for them.
- Use cache variables deliberately: document the expected type, default, and effect when suggesting a new `option()` or `set(... CACHE ...)` entry.
- Keep source files portable by moving platform-specific compiler flags and definitions into target-scoped CMake logic or presets.
- Prefer target-based CMake (`target_link_libraries`, `target_compile_features`, `target_compile_definitions`, `target_include_directories`) over global state.

## Policies and Portability

Give information about any CMake Policies that might affect CMake variables that are suggested or mentioned.

| Concern | Convention |
| --- | --- |
| Policy changes | Mention the relevant CMake policy when a variable, command, or behavior depends on policy state. |
| Minimum version | Do not imply a policy is active unless the project's `cmake_minimum_required()` or explicit `cmake_policy()` makes it active. |
| Compiler support | Keep code and flags portable across MSVC, Clang, and GCC. |
| Platform support | Avoid path, shell, compiler, or linker assumptions that only work on one operating system unless guarded by CMake conditions. |
| Diagnostics | Prefer compiler-feature checks and target properties over hardcoded compiler-specific flags when CMake has a portable abstraction. |

This project needs to be cross-platform and cross-compiler for MSVC, Clang, and GCC.

## C++ Samples and OpenCV File Paths

When providing OpenCV samples that use the file system to read files, always use absolute file paths rather than file names or relative file paths.

**Good:**

```cpp
cv::VideoCapture video;
video.open("C:/project/file.mp4");
```

Why: The sample does not depend on an IDE, build directory, or test runner working directory.

**Bad:**

```cpp
cv::VideoCapture video;
video.open("file.mp4");
```

Why: The sample depends on the current working directory and will fail unpredictably across presets, IDEs, and CI.

## Good / Bad Examples

The examples below illustrate manifest-mode dependency guidance.

**Good:**

```json
{
  "dependencies": [
    "opencv"
  ]
}
```

Why: The dependency is declared in `vcpkg.json`, so CMake configure restores it consistently for the selected triplet and preset.

**Bad:**

```sh
vcpkg install opencv
```

Why: A global install bypasses manifest mode and can leave CI, contributors, and presets using a different dependency graph.

## Conventions

| Rule | Rationale |
| --- | --- |
| Treat vcpkg as manifest-mode dependency management | Source-controlled manifests make dependency resolution reproducible |
| Do not suggest `vcpkg install library` for project dependencies | Global installs do not match manifest-mode configure behavior |
| Prefer `CMakePresets.json` for cache variables and configure choices | Presets keep local, CI, and IDE configuration consistent |
| Explain CMake Policies that affect suggested variables or commands | Policy state changes CMake behavior and can make advice version-dependent |
| Keep build logic cross-platform and portable across MSVC, Clang, and GCC | Compiler-specific assumptions break contributors or CI on other toolchains |
| Use absolute paths in OpenCV file-system samples such as `video.open("C:/project/file.mp4")` | Samples should not depend on the current working directory |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Add dependencies through `vcpkg.json` and configure with the project preset | Suggest `vcpkg install library` for manifest-mode dependencies |
| Put repeatable cache variables and toolchain settings in `CMakePresets.json` | Rely on undocumented one-off command lines for shared build configuration |
| Use target-scoped CMake commands | Set global include paths, definitions, or flags when target properties work |
| Mention relevant CMake Policies for policy-sensitive advice | Ignore policy state when recommending variables or commands |
| Write C and C++ examples that compile across MSVC, Clang, and GCC | Use unguarded compiler-specific extensions or flags |
| Use absolute file paths in OpenCV file-reading samples | Use bare file names or relative paths such as `video.open("file.mp4")` |

## Checklist Before Opening a PR

- [ ] Dependency guidance respects vcpkg manifest mode and updates `vcpkg.json` rather than using global install commands.
- [ ] Shared configure options and cache variables belong in `CMakePresets.json` when practical.
- [ ] Any suggested CMake variable or behavior affected by CMake Policies identifies the relevant policy state.
- [ ] CMake uses target-scoped commands and avoids unnecessary global state.
- [ ] C and C++ code and flags remain portable across MSVC, Clang, and GCC.
- [ ] OpenCV file-system samples use absolute paths such as `video.open("C:/project/file.mp4")` and not relative file names.
