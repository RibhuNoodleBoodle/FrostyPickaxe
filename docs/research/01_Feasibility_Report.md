# Feasibility reassessment

Date: 2026-11-05. Research only. This report replaces prior conclusions that depended on absent binaries, two discs, a guaranteed matching update, mandatory community patches, or a known HD 620 extension profile.

## Verdicts

Confidence describes the evidence supporting the verdict, not the probability of eventual success.

| Question | Verdict | Evidence, uncertainty and blocker | Next falsifiable check | Confidence |
| --- | --- | --- | --- | --- |
| Static recompilation / guest runtime for this title | UNKNOWN UNTIL BINARY ANALYSIS | Local base XEX identity known (L1); encrypted payload, function discovery, imports and update applicability unresolved; critical | G1 accepts exact source/update pair; G2 produces audited discovery/import coverage in a later authorized implementation phase | High |
| Vulkan rendering for this title | POSSIBLE WITH MATERIAL GAPS | Pinned SDK device source exists (S-GPU); no title trace or local rendering result; high correctness risk | G3 compares menu and gameplay captures with the supplied Xbox 360 build | Low |
| PC portability using ReXGlue | POSSIBLE WITH MATERIAL GAPS | Upstream build configuration describes host support (S-BUILD); no locally selected SDK/toolchain, build or boot; high | Pin source/dependencies, then independently validate Windows and Linux build/boot paths | Medium |
| Acceptable Intel HD 620 performance | UNKNOWN UNTIL BINARY ANALYSIS | Intel lists Vulkan API support (S-INTEL); no actual driver feature dump or measurements; critical | G3 device/format checks followed by G4 representative gameplay profiling on real HD 620 | High |
| Android after PC | CURRENTLY BLOCKED | PC gates unpassed; ARM64 host support alone does not establish Android lifecycle/runtime compatibility; high | G5 starts only after PC acceptance and a separate Android platform audit | High |

**PROCEED TO ARCHITECTURAL DISCOVERY**, conditional on keeping input applicability unresolved until G1 passes. Implementation readiness is held pending evidence. Inputs now exist, but a compatible updated executable has not been demonstrated.

## What the new files change

The ISO and update ZIP permit local identity checks rather than a request for missing files. They do not prove codegen readiness. The disc XEX is Title `53510823`, Media `0A657B25`, raw version 3, disc 1/1. The update outer package is Title `53510823`, Media `2427ED57`, raw version/base version 6. Internal delta applicability is UNKNOWN. A shared Title ID cannot substitute for exact source checks. The initial task is compatibility research, not an assumed offline merge pipeline.

The observed root supports a single-disc content design with `.tiger` archives and a movies directory. Withdraw the mandatory Disc 1 install/Disc 2 play topology and its invented mount paths. The current inspection does not establish middleware, save paths, archive compression, DLC requirements or update overlay precedence.

## SDK evidence and limits

No local SDK revision is selected. Prior notes named `c94f5ebdcb3c9d1a460ca48e04f9758448f8d518`, `bd833a2ab69d`, and tag `v0.10.0`; their tag relationships and latest-release status were not re-established. The first full hash is an **inspected documentary revision**, not a project dependency pin. One source file at that revision was retrievable. Do not prescribe either revision plus a speculative patch stack as an architecture decision.

The fetched upstream build file describes Clang 18+, C++23, 64-bit hosts, Windows/Linux/macOS platform branches, and Vulkan enabled by default outside Windows. Windows defaults to D3D12; selecting Vulkan there needs an explicit future build decision (S-BUILD). This moving source is not a reproducible SDK baseline. Confirm the SDL3 submodule SHA and input bridge in the finally selected tree; the prior claimed SDL version is not revalidated.

Audit CPU code/data boundaries, exception tables, indirect branches, VMX128, atomics and fences; then map actual imports to runtime implementations including memory, TLS, threads, waits, DPCs, files, saves and timing. Neither import counts nor names establish exercised behavior. Community bugs are test hypotheses requiring revision-specific reproduction, not mandatory backports.

## Graphics and HD 620

Pinned device-selection source checks independent blending and shader stores/atomics, with geometry/non-solid requirements governed by configuration (S-GPU). Backend initialization does not demonstrate Xenos EDRAM correctness. Audit shader translation, fetch constants, formats, tiling, resolves, aliasing and CPU/GPU synchronization with title captures. Earlier specific LUT/exponent/gamma fixes are unverified hypotheses; purple output alone cannot diagnose a fetch bug.

Intel lists HD 620 under Vulkan 1.3 support (S-INTEL). That table provides no per-driver interlock, format or performance guarantee. Obtain separate Windows driver and Linux Mesa ANV capability records: API, extensions/features, relevant 16-bit color/depth formats, blend/storage support, memory budgets and limits. Interlock availability remains UNKNOWN for the user's actual device/driver. If absent, test the selected SDK's host-render-target fallback and required formats. Stop HD 620 progression if faithful rendering requires an unavailable feature and no viable fallback exists.

Shared memory, bandwidth, shader compilation, readbacks, CPU translation overhead and thermal limits are plausible bottlenecks, not measured diagnoses. Do not infer CPU model, RAM channels or sustained clocks from GPU name. Resolution/LOD/effect changes, residency tuning and shader caching are later measured options with explicit fidelity costs. Do not distribute preseeded game-derived or device-specific caches without reviewing their provenance and compatibility.

## Input, media and content

SDL3 host gamepads still need correct guest XAM semantics for polling, mapping, hotplug and rumble. Audio needs actual decoder/mixer dependency and starvation analysis; do not prescribe Wwise/FMOD or a fixed callback frequency without evidence. A `.bik` directory is evidence of assets, not proof of a host Bink decoder or mandatory YCbCr pipeline. Inventory update overlays, streaming, localization, movies, saves, offline behavior and optional content before selecting module responsibilities. Keep the commercial PC edition as a comparison only; no asset/executable substitution is justified.

## Validation and future portability

Distinguish compiles, launches, renders menu, renders scene, playable and acceptable on HD 620. Record exact content hashes and SDK/dependency revisions for each future result. G4 specifies scene, frame-time, memory and fidelity acceptance; this run measured none of those.

Preserve portable endian-aware guest memory, explicit synchronization, storage/window/input/audio boundaries and replaceable platform fibers. Android additionally needs NDK/Bionic, lifecycle/surface recreation, storage/content provisioning, packaging and mobile GPU validation. No parallel Android development is justified.

Game ownership and lawful analysis scope are user context, not a legal finding. Keep copyrighted inputs and generated derivatives private pending distribution/licensing review. No legal conclusion, clean-room certification or middleware redistribution permission is established here.
