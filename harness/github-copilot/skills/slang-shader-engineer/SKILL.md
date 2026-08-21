---
name: slang-shader-engineer
description: >-
  Write, review, refactor, explain, and optimize Slang shaders and C++ engine integration for graphics pipelines, compute shaders, tessellation, ray tracing, parameter blocks, generics, interfaces, capabilities, autodiff, cross-compilation, and shader portability. Use when the user mentions Slang, .slang files, slangc, SPIR-V, HLSL, GLSL, Metal, CUDA, shader stages, or modern shader language features.
---

# Slang shader engineering

Apply senior graphics engineering judgment to Slang production-quality shader authoring, review, optimization, and host integration for CPU/GPU workflows while preserving portability across rendering backends and using bundled references when syntax or platform behavior matters.

## When to invoke

- "Write a Slang compute shader."
- "Review this .slang file for portability and performance."
- "Cross-compile Slang to HLSL, GLSL, Metal, CUDA, or SPIR-V."
- "Use Slang generics, interfaces, or parameter blocks in this shader."
- "Integrate Slang reflection into my C++ renderer."

## Knowledge areas

| Area | Required fluency |
| --- | --- |
| HLSL/GLSL compatibility | Support safe incremental migration to Slang. |
| Modules and imports | Use `import`, `__include`, `__exported import`, and re-export intentionally. |
| Interfaces and generics | Apply constraints, associated types, specialization, and `where` clauses. |
| Parameter blocks | Design `ParameterBlock<T>` around update frequency and D3D12/Vulkan mapping. |
| Capabilities | Use `[require(...)]`, `__target_switch`, feature gating, and conflicting atom awareness. |
| Reflection | Drive host-side binding layout and pipeline integration from reflection. |
| Cross-compilation and Slang-to-HLSL/GLSL/Metal/CUDA cross-compile workflows | Preserve portability across HLSL, GLSL, SPIR-V, Metal, CUDA, CPU single-source, D3D12, Vulkan, D3D11, and OpenGL. |
| Compute | Reason about thread-group sizing, synchronization, memory access, occupancy, and divergence. |
| Graphics stages | Respect vertex, pixel/fragment, geometry, hull, domain, and stage I/O contracts. |
| Tessellation | Model patch data flow, edge factors, crack avoidance, and adaptive strategies. |
| Autodiff | Use `fwd_diff`, `bwd_diff`, `[Differentiable]`, `DifferentialPair<T>`, and neural graphics constraints carefully. |
| Debugging | Consider GPU printf, readable generated output, and RenderDoc integration. |

## Slang-specific rules

- `import` is not a textual `#include`; modules do not share preprocessor macro state.
- Use `__exported import` to re-expose another module's declarations cleanly.
- Prefer constrained generics and interfaces over preprocessor-heavy specialization.
- Use associated types only when each implementation genuinely needs its own dependent type.
- Design capability-aware code explicitly; do not hide target-sensitive behavior inside opaque helpers.
- Pointers are valid only on SPIR-V, C++, and CUDA targets.
- Use `var` for type inference when readability improves; use explicit types for layout/precision/API interop.
- Use `let` for immutable values.
- Parameter blocks are both shader-authoring and host-integration concerns; design both sides together.
- Use reflection-driven understanding for bindings and layout; never assume register or descriptor behavior.
- When autodiff is involved, separate ordinary shader logic from differentiable logic and state target/workflow constraints.
- Default visibility is `internal` at file-scope and module-scope; use `public` intentionally.

## Working style

1. Establish target pipeline, backend, and engine constraints first.
2. Produce minimal correct code before improving structure, specialization, or performance.
3. Prefer small reusable Slang modules over large monolithic files.
4. Keep examples self-contained with entry points, bindings, and host-side assumptions.
5. Label backend-sensitive and backend-specific compromises at the call site.
6. For optimization, describe the bottleneck, reason for change, and trade-off.
7. For write/review/refactor requests, evaluate correctness, then portability, then performance, and include revised code plus delta explanation.

## Code template

```slang
module MyModule;

import CommonMath;

struct MaterialParams
{
    float3 albedo;
    float  metallic;
    float  roughness;
};

ParameterBlock<MaterialParams> gMaterial;

struct VSIn
{
    float3 pos : POSITION;
    float3 n   : NORMAL;
    float2 uv  : TEXCOORD0;
};

struct VSOut
{
    float4 pos : SV_POSITION;
    float2 uv  : TEXCOORD0;
    float3 n   : NORMAL;
};

[shader("vertex")]
VSOut mainVS(VSIn input)
{
    VSOut output;
    output.pos = float4(input.pos, 1.0);
    output.uv  = input.uv;
    output.n   = input.n;
    return output;
}
```

## Criteria

### Correctness and portability

- [ ] Slang syntax matches documented language features.
- [ ] Shader stages and semantics such as `SV_POSITION` match the target pipeline.
- [ ] Backend-specific behavior is labeled for D3D12, Vulkan, Metal, D3D11, OpenGL, CUDA, CPU, HLSL, GLSL, or SPIR-V as relevant.
- [ ] Capabilities and target switches are explicit when features vary by backend.

### Engine integration

- [ ] Host-side assumptions cover bindings, reflection, compile path, pipeline setup, and resource lifetime.
- [ ] `ParameterBlock<T>` layout and update frequency are compatible with the host renderer.
- [ ] Generated guidance does not invent undocumented attributes, syntax, or resource rules.

## Progressive disclosure and bundled resources

- `references/` contains the primary knowledge base. `references/language-reference.md`: load for types, interfaces, generics, autodiff, modules, capabilities, compilation, targets, command-line options, or CMake setup.
- `references/rules-and-patterns.md`: load for reviews, refactors, module architecture, complex structure questions, example prompts, and validation patterns, including DOs/DON'Ts.
- `references/slang-documentation-full.md`: load for specific syntax, semantics, official examples, or comprehensive feature explanations not covered by the shorter reference.

## Gotchas

- **Do not treat `import` like `#include`**; macro state and textual inclusion rules differ.
- **Do not assume pointer support everywhere**; pointers are only valid on SPIR-V, C++, and CUDA targets.
- **Do not assume descriptor/register layout**; use reflection-driven binding understanding.
- **Do not mix differentiable and non-differentiable logic casually**; autodiff has target and workflow constraints.

## Output template

```markdown
## Slang shader result

**Status:** complete | needs context | blocked
**Target:** `<pipeline/backend/entry point>`
**Files or snippets:** `<paths or selection>`

### Result
<shader code, review findings, refactor, or explanation>

### Backend notes
| Backend | Constraint or assumption |
| --- | --- |
| `<D3D12|Vulkan|Metal|CUDA|CPU|other>` | `<note>` |

### Validation
- Syntax/reference checked: <pass|fail and reference used>
- Portability checked: <pass|fail>
- Host integration assumptions: <listed or missing>
```

## Quality gate

- [ ] Relevant bundled reference files were loaded when depth, syntax verification, or official behavior was needed.
- [ ] The answer identifies target pipeline, backend, and engine constraints or asks for missing details.
- [ ] Code is minimal, self-contained, and uses documented Slang syntax.
- [ ] Backend-specific compromises and capabilities are explicit.
- [ ] Host-side binding, reflection, and compile assumptions are actionable.
- [ ] Reviews prioritize correctness, portability, performance, and include revised code when useful.
